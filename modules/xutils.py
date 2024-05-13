#==============================#
# Author: KONG Vungsovanreach  #
# Date: 2024-04-25             #
#==============================#

#import all required modules
import cv2
import numpy as np

#print in message format
def xmsg(msg: str):
    print(f'[msg]: {msg}')

#print in error format
def xerr(error: str):
    print(f'[err]: {error}')

#store configuration/variable for inner/outer function use
class Config():
    def __init__(self):
        #dictionary to store dynamic variables
        self._dynamic_variables = {}

    def __getattr__(self, name):
        #this method is called when an attribute is not found
        if name in self._dynamic_variables:
            return self._dynamic_variables[name]
        else:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        #this method is called when an attribute is set
        if name == '_dynamic_variables':
            #allow setting the _dynamic_variables attribute directly
            super().__setattr__(name, value)
        else:
            #set a dynamic variable
            self._dynamic_variables[name] = value

#redraw the polygon
def add_polygon(frame, polygons, color=(255, 0, 0)):
    for polygon_coords in polygons:
        pts = np.array(polygon_coords, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(frame, [pts], isClosed=True, color=color, thickness=1, lineType=cv2.LINE_AA)
    return frame
