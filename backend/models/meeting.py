##############################
# Model for single section Meeting given UIUC Course Explorer API
# See https://courses.illinois.edu/cisdocs/explorer
#
# Matt Hokinson, 12/26/22
##############################

from uuid import uuid4

import xml.etree.ElementTree as ET

from utils.utils import log, LoggingMode 

class Meeting: 
    def __init__(self):
        self.id = uuid4() # TODO: Keep?

        self.start = ""
        self.end = "" # Timestamps 
        self.daysOfWeek = ""
        self.roomNumber = ""
        self.buildingName = ""

        self.isOnline = False

    def parse_xml_object(self, root):
        # Should only be on element in the file for each item, save meetings 
        # All fields seem to be optional, so if they exist we set otherwise nothing 
        def __try_get(field):
            try:
                return root.findall(field)[0].text
            except IndexError:
                return ""
            except:
                log(f"Exception raised in parsing field {field} of meeting", mode=LoggingMode.ERROR)

        self.isOnline = "online" in __try_get('type').lower()
        self.start = __try_get('start')
        self.end = __try_get('end')
        self.daysOfWeek = __try_get('daysOfTheWeek')
        self.roomNumber = __try_get('roomNumber')
        self.buildingName = __try_get('buildingName')