#==============================#
# Author: KONG Vungsovanreach  #
# Date: 2024-04-25             #
#==============================#

#import all required modules

class DangerDetection(object):
    def __init__(self, risk_areas):
        self.risk_areas = risk_areas
    
    def detect(self, results):
        for box in results[0].boxes:
            print(box)