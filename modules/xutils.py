#==============================#
# Author: KONG Vungsovanreach  #
# Date: 2024-04-25             #
#==============================#

#import all required modules

#print in message format
def xmsg(msg):
    print(f'[msg]: {msg}')

#print in error format
def xerr(error):
    print(f'[err]: {error}')

#class for storing global variable across module scope
class Config():
    def __init__(self):
        self.__dynamic_vars = {}

    def __getattr__(self, name):
        if name in self.__dynamic_vars:
            return self.__dynamic_vars[name]
        else:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name == '__dynamic_vars':
            super().__setattr__(name, value)
        else:
            self.__dynamic_vars['name'] = value