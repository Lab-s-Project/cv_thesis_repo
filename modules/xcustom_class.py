#==============================#
# Author: KONG Vungsovanreach  #
# Date: 2024-05-07             #
#==============================#

#class for max size list
class MSL:
    def __init__(self, max_size):
        self.max_size = max_size
        self.elements = []

    def __len__(self):
        return len(self.elements)

    def is_full(self):
        return len(self.elements) == self.max_size

    def push(self, element):
        if self.is_full():
            self.elements.pop(0)  # Remove the front element if full
        self.elements.append(element)

    def empty(self):
        self.elements = []

    def get_list(self):
        return self.elements.copy()