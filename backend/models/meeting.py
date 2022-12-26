##############################
# Model for single section Meeting given UIUC Course Explorer API
# See https://courses.illinois.edu/cisdocs/explorer
#
# Matt Hokinson, 12/26/22
##############################

from uuid import uuid4

import xml.etree.ElementTree as ET

class Meeting: 
    def __init__(self):
        self.id = uuid4()

        self.start = ""
        self.end = "" # Timestamps 
        self.daysOfWeek = ""
        self.roomNumber = ""
        self.buildingName = ""

    def parse_xml_object(self, root):
        # Should only be on element in the file for each item, save meetings 
        self.start = root.findall('start')[0].text
        self.end = root.findall('end')[0].text
        self.daysOfWeek = root.findall('daysOfTheWeek')[0].text
        self.roomNumber = root.findall('roomNumber')[0].text
        self.buildingName = root.findall('buildingName')[0].text