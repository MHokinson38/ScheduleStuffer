##############################
# Model for Course Section given UIUC Course Explorer API
# See https://courses.illinois.edu/cisdocs/explorer
#
# Matt Hokinson, 12/26/22
##############################

from uuid import uuid4

import requests
import xml.etree.ElementTree as ET

from os.path import exists

import models.utils as utils
from models.meeting import Meeting

class Section: 
    def __init__(self, sectionID, year, semester, subjectCode, courseNumber):
        # Args needed for making course explorer query (and checking cache) 
        self.id = uuid4() # TODO: Keep?

        self.sectionNumber = sectionID # The uuid for the section (I think unique) 

        self.sectionCode = "" # The code for the section - AL1, ADX, etc.
        self.parentCode = ""
        self.statusCode = ""
        self.partOfTerm = ""
        self.sectionStatusCode = ""
        self.enrollmentStatus = ""
        self.meetings = [] 

        if exists(utils.get_local_section_file_path(year, semester, subjectCode, courseNumber, self.sectionNumber)):
            self.__read_local_file(year, semester, subjectCode, courseNumber)
        else:
            self.__fetch_remote_data(year, semester, subjectCode, courseNumber)

    #########################
    # Fetching course explorer data
    # Either checking local cache or fetching from Course Explorer API
    #########################
    def __parse_xml_object(self, root):
        # Should only be on element in the file for each item, save meetings 
        self.sectionCode = root.findall('sectionNumber')[0].text  
        self.statusCode = root.findall('statusCode')[0].text
        self.partOfTerm = root.findall('partOfTerm')[0].text
        self.sectionStatusCode = root.findall('sectionStatusCode')[0].text
        self.enrollmentStatus = root.findall('enrollmentStatus')[0].text

        # Fetch the section IDs, then fetch and parse section endpoints 
        for m in root.findall('meetings/meeting'):
            meeting = Meeting()
            meeting.parse_xml_object(m)
            self.meetings.append(meeting)

    def __read_local_file(self, year, semester, subjectCode, courseNumber):
        with open(utils.get_local_section_file_path(year, semester, subjectCode, courseNumber, self.sectionNumber), 'r') as f:
            # Read in file text as XML object 
            root = ET.fromstring(f.read())
            self.__parse_xml_object(root)

    def __fetch_remote_data(self, year, semester, subjectCode, courseNumber):
        # Fetch the XML file from the Course Explorer API
        r = requests.get(utils.get_remote_endpoint(year, semester, subjectCode, courseNumber, sectionID=self.sectionNumber))
        root = ET.fromstring(r.text)
        self.__parse_xml_object(root)

        # Write the XML file to the local cache 
        with open(utils.get_local_section_file_path(year, semester, subjectCode, courseNumber, self.sectionNumber), 'w') as f:
            f.write(r.text)