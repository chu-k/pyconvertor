# this constructs child parsers based on the format
# inferred from the input file extension
#
# See: https://www.oodesign.com/factory-pattern.html

# import newly created formats here
from .nodal import Nodal
from .dump import Dump
#from .modulename import ClassName

class Selector(object):
# factory pattern to create instatiations of format parsers
    def __init__(self, fmt):
        self.fmt = fmt
    def create(self, fpath):
        if self.fmt == 'nodal':
            return Nodal(fpath, self.fmt)
        elif self.fmt == 'dump':
            return Dump(fpath, self.fmt)
        #elif NEW FORMAT CLASS DEFINITIONS HERE
        else:
            pass
