#==============================#
# Author: KONG Vungsovanreach  #
# Date: 2024-04-25             #
#==============================#

#import all required modules
from shapely.geometry import Polygon, Point
import sys
#change dir to import modules
sys.path.append('..')
from modules.xutils import xmsg, xerr
from modules.xcustom_class import MSL

#base class for danger detection
class DangerDetection(object):
    def __init__(self, risk_areas):
        self.risk_areas = Polygon(risk_areas[0])
        self.track_hist = MSL(max_size=5)
        self.in_polygon_cls = MSL(max_size=50) #list of all object that locates in the polygon
        xmsg(f'polygon: {self.risk_areas}')

    
    def detect(self, result):
        self.result = result
        self.track_hist.push(self.result)
        for idx, (cl, xbox) in enumerate(zip(self.result.cls, self.result.xboxes)):
            leg_xc, leg_yc = self.result.leg_xcyc[idx]
            
            #if it is a person and step into the polygon
            if Point((leg_xc, leg_yc)).within(self.risk_areas):
                self.in_polygon_cls.push(int(cl))
                if int(cl) == 0:
                    self.result.xboxes[idx].is_danger = True
                    self.result.danger_level.append(1)
        
        if len(list(set(self.in_polygon_cls.get_list()))) == 2: self.result.danger_level.append(2)
        # for hist in [self.track_hist.get_list()[i] for i in (0, -1)]:
        #     print(hist.ids)
        self.in_polygon_cls.empty()
        return result
