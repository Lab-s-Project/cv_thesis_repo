#==============================#
# Author: KONG Vungsovanreach  #
# Date: 2024-04-25             #
#==============================#

#import all required modules
import cv2, time

#base class for plotting result
class XPlot(object):
    def __init__(self, result, bb_color = (0, 181, 6), bb_thickness=2):
        self.result = result
        # self.danger_detail = danger_detail
        self.bb_color = bb_color
        self.bb_thickness = bb_thickness
        self.text_color = (255, 255, 255)
        self.text_thickness = 2
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 1.2
        self.center_color = (0, 0, 255)
        
    @property
    def boxes(self): #return all predicted boxes
        return self.result.boxes

    @property
    def xboxes(self):
        return self.result.xboxes

    @property
    def img(self): #return original input image
        return self.result.img

    def plot(self):
        #iterate over all boxes and plot detail
        for idx, box in enumerate(self.boxes):
            x1, y1, x2, y2 = self.result.xyxy[idx]
            x, y, w, h = self.result.xyxy[idx]
            xc, yc = self.result.xcyc[idx]
            class_id = self.result.cls[idx]
            class_name = self.result.names[class_id]
            cv2.rectangle(self.img, (x1, y1), (x2, y2), self.bb_color, thickness=self.bb_thickness, lineType=cv2.LINE_AA)
            if class_id == 0:
                cv2.rectangle(self.img, (xc-10, yc-20), (xc+130, yc+15), self.bb_color, -1)
            elif class_id == 2:
                cv2.rectangle(self.img, (xc-10, yc-20), (xc+60, yc+15), self.bb_color, -1)
            cv2.putText(self.img, class_name, (xc-5, yc+5), self.font, self.font_scale, self.text_color, self.text_thickness)
            # time.sleep(0.010)
            if self.xboxes[idx].danger:
                cv2.circle(self.img, (xc, yc), 5, self.center_color, -1, cv2.LINE_AA)
        return self.img