##############################
# Model for Single Course given UIUC Course Explorer API
# https://courses.illinois.edu/cisdocs/explorer
#
# Matt Hokinson, 12/26/22
##############################

from ariadne import QueryType

import requests
import xml.etree.ElementTree as ET
import time 
from os.path import exists

import models.utils as utils
from models.section import Section
from utils.utils import log, LoggingMode

courseQuery = QueryType()

# Define the Course Object 
class Course: 
    def __init__(self, year: str, semester: str, subjectCode: str, courseNumber: str):
        # Fields needed for making course explorer query (and checking cache) 
        self.year = year
        self.semester = semester
        self.subjectCode = subjectCode # Subject code (ex. CS, MATH)
        self.courseNumber = courseNumber # Course ID (ex. 101, 445)

        self.exists = True # Assume exists, set to false if we fail to find the course endpoint 

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
        def __try_get(field):
            try:
                return root.findall(field)[0].text
            except IndexError:
                return ""
            except:
                log(f"Exception raised in parsing field {field} of course {self.subjectCode} {self.courseNumber}", mode=LoggingMode.ERROR)

        self.description = __try_get("description")
        self.label = __try_get("label")
        # Take the first character to int of the credit hours string 
        self.creditHours = int(__try_get("creditHours")[:1])

        # Fetch the section IDs, then fetch and parse section endpoints 
        for s in root.findall('sections/section'):
            self.sections.append(Section(s.attrib['id'], self.year, self.semester, self.subjectCode, self.courseNumber))

        if len(self.sections) == 0:
            log(f"No sections found for {self.subjectCode} {self.courseNumber} in {self.semester} {self.year}", mode=LoggingMode.WARNING)

    def __read_local_file(self):
        with open(utils.get_local_course_file_path(self.year, self.semester, self.subjectCode, self.courseNumber), 'r') as f:
            # Read in file text as XML object 
            root = ET.fromstring(f.read())

            self.__parse_xml_object(root)
    
    def __fetch_remote_data(self):
        # Fetch data from course explorer API 
        log(f"Fetching course info for {self.subjectCode} {self.courseNumber} in {self.semester} {self.year}", mode=LoggingMode.DEBUG)
        remote_endpoint = utils.get_remote_endpoint(self.year, self.semester, self.subjectCode, self.courseNumber)
        courseInfoResponse = requests.get(remote_endpoint) # no extra auth required 
        
        if courseInfoResponse.status_code != 200:
            log(f"Error fetching course info from {remote_endpoint}", mode=LoggingMode.ERROR)
            log(f"Error code: {courseInfoResponse.status_code} Message: {courseInfoResponse.text}", mode=LoggingMode.ERROR)

            if courseInfoResponse.status_code == 404:
                self.exists = False
            return

        # Parse the XML file to build out the rest of the object 
        root = ET.fromstring(courseInfoResponse.text)
        self.__parse_xml_object(root)

        # Cache the response 
        with open(utils.get_local_course_file_path(self.year, self.semester, self.subjectCode, self.courseNumber), 'w') as f:
            f.write(courseInfoResponse.text)

@courseQuery.field("courseInfo")
# TODO: Handle generic vs. specific courseNumber input, use same field both ways 
# TODO: Add way to handle tracking non-existent courses faster, or query at subject level first and then filter for proper level
def resolve_course_info(_, info, year, semester, subjectCode, courseNumber):
    log(f"Resolving courseInfo query for {subjectCode} {courseNumber} in {semester} {year}", mode=LoggingMode.INFO)
    # For metrics, measure time to process query 
    currTime = time.time()

    # Cache flush - TODO: Better cache flushing policy 
    utils.check_cache_and_flush()

    # Fetch the courses for all available classes at said level
    # Filter those which don't exist 
    courseLevel = int(courseNumber[:1]) * 100 
    courseNumbers = range(courseLevel, courseLevel + 100)

    courses = []
    for c in courseNumbers:
        # Fields from course with matching names to GQL schema are used by default 
        course = Course(year, semester, subjectCode, str(c))
        if course.exists:
            courses.append(course)

    endTime = time.time()
    log(f"Query processed in {endTime - currTime} seconds", mode=LoggingMode.INFO)
    
    return courses