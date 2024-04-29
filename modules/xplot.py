#==============================#
# Author: KONG Vungsovanreach  #
# Date: 2024-04-25             #
#==============================#

#import all required modules
import cv2

class XPlot(object):
    def __init__(self, results, bb_color = (0, 255, 255), bb_thickness=1):
        self.result = results[0]
        self.bb_color = bb_color
        self.bb_thickness = bb_thickness
        self.text_color = (0, 255, 255)
        self.text_thickness = 2
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 1
        self.center_color = (0, 255, 255)
        
    @property
    def boxes(self):
        return self.result.boxes

    @property
    def img(self):
        return self.result.orig_img

    def plot(self):
        for box in self.boxes:
            x1, y1, x2, y2 = [int(i) for i in box.xyxy.cpu().numpy()[0]]
            xc, yc = int((x1+x2)/2), int((y1+y2)/2)
            class_id = int(box.cls.cpu().numpy()[0])
            class_name = self.result.names[class_id]
            cv2.rectangle(self.img, (x1, y1), (x2, y2), self.bb_color, thickness=self.bb_thickness)
            cv2.putText(self.img, class_name, (x1, y1-5), self.font, self.font_scale, self.text_color, self.text_thickness)
            cv2.circle(self.img, (xc, yc), 5, self.center_color, -1)
        return self.img