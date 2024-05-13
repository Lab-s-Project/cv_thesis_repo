#==============================#
# Author: KONG Vungsovanreach  #
# Date: 2024-05-07             #
#==============================#

#class for max size list
class MSL:
    """
    A custom list class that limits the maximum number of elements and
    automatically removes the front element on overflow.
    """

    def __init__(self, max_size):
        """
        Initializes the custom list with a specified maximum size.

        Args:
            max_size (int): The maximum number of elements the list can hold.
        """
        self.max_size = max_size
        self.elements = []

    def __len__(self):
        """
        Returns the current length of the list.
        """
        return len(self.elements)

    def is_full(self):
        """
        Checks if the list has reached its maximum size.

        Returns:
            bool: True if the list is full, False otherwise.
        """
        return len(self.elements) == self.max_size

    def push(self, element):
        """
        Appends a new element to the end of the list.

        Args:
            element: The element to be added.

        Raises:
            IndexError: If the list is already full.
        """
        if self.is_full():
            self.elements.pop(0)  # Remove the front element if full

        self.elements.append(element)

    def empty(self):
        self.elements = []

    def get_list(self):
        """
        Returns a copy of the current list elements.

        Returns:
            list: A copy of the internal list elements.
        """
        return self.elements.copy()