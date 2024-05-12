#==============================#
# Author: KONG Vungsovanreach  #
# Date: 2024-05-07             #
#==============================#

#import all required modules
import numpy as np

class XResult():
    def __init__(self, results):
        self.result = results[0]

    @property
    def xboxes(self):
        return [XBoxes(boxes) for boxes in self.result.boxes]

    @property
    def boxes(self):
        return self.result.boxes
        
    @property
    def img(self):
        return self.result.orig_img

    @property
    def cls(self):
        return self.boxes.cls.cpu().numpy()

    @property
    def conf(self):
        return self.boxes.conf

    @property
    def ids(self):
        return self.boxes.id.cpu().numpy().astype(int) if self.boxes.id is not None else None

    @property
    def names(self):
        return self.result.names

    @property
    def xyxy(self):
        return self.boxes.xyxy.cpu().numpy().astype(int)
    
    @property
    def xywh(self):
        return self.boxes.xywh.cpu().numpy().astype(int)

    @property
    def xcyc(self):
        xcyc = np.empty((len(self.boxes), 2), dtype=int)
        for i, row in enumerate(self.xyxy):
          x1, y1, x2, y2 = row
          xc = int((x1 + x2) / 2)
          yc = int((y1 + y2) / 2)
          xcyc[i, 0] = xc
          xcyc[i, 1] = yc
        return xcyc

class XBoxes(object):
    def __init__(self, boxes):
        self.boxes = boxes
        self.danger = False