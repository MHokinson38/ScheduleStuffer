##############################
# Utility functions for model classes and 
# remote lookups/queries 
#
# Matt Hokinson, 12/26/22
##############################

import os 
import shutil 

from utils.utils import log, LoggingMode

# Constants 
CACHE_DIR = "cachedCourseInfo/"
COURSE_EXPLORER_ENDPOINT = "http://courses.illinois.edu/cisapp/explorer/schedule/"

# Local filepaths 
def get_local_course_file_path(year, semester, subjectCode, courseNumber):
    return CACHE_DIR + year + "_" + semester + "_" + subjectCode + "_" + courseNumber + ".xml"

def get_local_section_file_path(year, semester, subjectCode, courseNumber, sectionID):
    """Generate the local file path for a class section XML file 

    * Note: Not sure if sectionID is unique across all courses, so we aren't using sectionID only

    Returns:
        string: file path
    """
    return CACHE_DIR + year + "_" + semester + "_" + subjectCode + "_" + courseNumber + "_" + sectionID + ".xml"

# Remote Endpoints 
def get_remote_endpoint(year, semester, subjectCode, courseNumber, sectionID=None):
    if sectionID is not None:
        return COURSE_EXPLORER_ENDPOINT + year + "/" + semester + "/" + subjectCode + "/" + courseNumber + "/" + sectionID + ".xml"
    
    return COURSE_EXPLORER_ENDPOINT + year + "/" + semester + "/" + subjectCode + "/" + courseNumber + ".xml"

# Cache handling 
def check_cache_and_flush():
    """Flush the cache directory, if the size of the directory is above a certain size 
    """
    MAX_SIZE = 10000000 # 10 MB
    if os.path.getsize(CACHE_DIR) > MAX_SIZE:
        log(f"Cache size is above threshold ({os.path.getsize(CACHE_DIR)}), flushing cache", mode=LoggingMode.INFO)

        shutil.rmtree(CACHE_DIR)
        os.mkdir(CACHE_DIR)
    