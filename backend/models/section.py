##############################
# Model for Course Section given UIUC Course Explorer API
# See https://courses.illinois.edu/cisdocs/explorer
#
# Matt Hokinson, 12/26/22
##############################

import requests
import xml.etree.ElementTree as ET

from os.path import exists

import models.utils as utils
from models.meeting import Meeting
from utils.utils import log, LoggingMode

class Section: 
    def __init__(self, sectionID, year, semester, subjectCode, courseNumber):
        # Args needed for making course explorer query (and checking cache) 
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
        def __try_get(field):
            try:
                return root.findall(field)[0].text
            except IndexError:
                return ""
            except:
                log(f"Exception raised in parsing field {field} of meeting", mode=LoggingMode.ERROR)

        log(f"Parsing section {self.sectionNumber}", mode=LoggingMode.DEBUG)
        # Should only be on element in the file for each item, save meetings
        self.sectionCode = __try_get("sectionNumber")
        self.statusCode = __try_get("statusCode")
        self.partOfTerm = __try_get("partOfTerm")
        self.sectionStatusCode = __try_get("sectionStatusCode")
        self.enrollmentStatus = __try_get("enrollmentStatus")

        # Fetch the section IDs, then fetch and parse section endpoints 
        for m in root.findall('meetings/meeting'):
            meeting = Meeting()
            meeting.parse_xml_object(m)
            self.meetings.append(meeting)

        # if there are no meetings, report 
        if len(self.meetings) == 0:
            log(f"Warning: No meetings found for section {self.sectionNumber}", mode=LoggingMode.WARNING)

    def __read_local_file(self, year, semester, subjectCode, courseNumber):
        with open(utils.get_local_section_file_path(year, semester, subjectCode, courseNumber, self.sectionNumber), 'r') as f:
            # Read in file text as XML object 
            root = ET.fromstring(f.read())
            self.__parse_xml_object(root)

    def __fetch_remote_data(self, year, semester, subjectCode, courseNumber):
        # Fetch the XML file from the Course Explorer API
        remote_endpoint = utils.get_remote_endpoint(year, semester, subjectCode, courseNumber, sectionID=self.sectionNumber)
        response = requests.get(remote_endpoint)
        if response.status_code != 200:
            log(f"Error fetching course info from {remote_endpoint}", mode=LoggingMode.ERROR)
            log(f"Error message: {response.text}", mode=LoggingMode.ERROR)
            return

        root = ET.fromstring(response.text)
        self.__parse_xml_object(root)

        # Write the XML file to the local cache 
        with open(utils.get_local_section_file_path(year, semester, subjectCode, courseNumber, self.sectionNumber), 'w') as f:
            f.write(response.text)