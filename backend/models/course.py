##############################
# Model for Single Course given UIUC Course Explorer API
# https://courses.illinois.edu/cisdocs/explorer
#
# Matt Hokinson, 12/26/22
##############################

from ariadne import QueryType
from uuid import uuid4

import requests
import xml.etree.ElementTree as ET

from os.path import exists

import models.utils as utils
from models.section import Section

courseQuery = QueryType()

# Define the Course Object 
class Course: 
    def __init__(self, year, semester, subjectCode, courseNumber):
        # Fields needed for making course explorer query (and checking cache) 
        self.id = uuid4() # TODO: Keep?
        self.year = year
        self.semester = semester
        self.subjectCode = subjectCode # Subject code (ex. CS, MATH)
        self.courseNumber = courseNumber # Course ID (ex. 101, 445)

        self.label = ""
        self.description = ""
        self.creditHours = 0

        self.sections = [] # List of section IDs for the course, need to read in section XML files

        # Check if the file is cached, then populate the rest of the object 
        if exists(utils.get_local_course_file_path(self.year, self.semester, self.subjectCode, self.courseNumber)):
            self.__read_local_file()
        else:
            self.__fetch_remote_data()

    #########################
    # Fetching course explorer data
    # Either checking local cache or fetching from Course Explorer API 
    #########################
    def __parse_xml_object(self, root):
        self.description = root.findall('description')[0].text
        self.label = root.findall('label')[0].text
        # Take the first character to int of the credit hours string 
        self.creditHours = int(root.findall('creditHours')[0].text[:1])

        # Fetch the section IDs, then fetch and parse section endpoints 
        for s in root.findall('sections/section'):
            self.sections.append(Section(s.attrib['id'], self.year, self.semester, self.subjectCode, self.courseNumber))

    def __read_local_file(self):
        with open(utils.get_local_course_file_path(self.year, self.semester, self.subjectCode, self.courseNumber), 'r') as f:
            # Read in file text as XML object 
            root = ET.fromstring(f.read())

            self.__parse_xml_object(root)
    
    def __fetch_remote_data(self):
        # Fetch data from course explorer API 
        remote_endpoint = utils.get_remote_endpoint(self.year, self.semester, self.subjectCode, self.courseNumber)
        courseInfoResponse = requests.get(remote_endpoint) # no extra auth required 
        print(f"Response: {courseInfoResponse}")
        # TODO: Add error handling

        # Parse the XML file to build out the rest of the object 
        root = ET.fromstring(courseInfoResponse.text)
        self.__parse_xml_object(root)

        # Cache the response 
        with open(utils.get_local_course_file_path(self.year, self.semester, self.subjectCode, self.courseNumber), 'w') as f:
            f.write(courseInfoResponse.text)

@courseQuery.field("courseInfo")
def resolve_course_info(_, info, year, semester, subjectCode, courseNumber):
    # Cache flush - TODO: Better cache flushing policy 
    utils.check_cache_and_flush()
    
    # Fields from course with matching names to GQL schema are used by default 
    # TODO: Figure out how to use courseQuery file 
    course = Course(year, semester, subjectCode, courseNumber)
    return course