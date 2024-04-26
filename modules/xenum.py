#==============================#
# Author: KONG Vungsovanreach  #
# Date: 2024-04-25             #
#==============================#

#import all required modules
from enum import Enum

#enum for type of stream
class StreamType(Enum):
    usb = 'usb'
    csi = 'csi'
    file = 'file'

    def __str__(self):
        return self.value