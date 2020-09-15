# this constructs child parsers based on the format
# inferred from the input file extension
#
# See: https://www.oodesign.com/factory-pattern.html

# import newly created formats here
from .nodal import Nodal
from .dump import Dump
from .cac import Cac
#from .modulename import ClassName

class Selector(object):
# factory pattern to create instatiations of format parsers
    def __init__(self, fmt, vir=False, force=False):
        self.fmt = fmt
        self.vir_bool = vir
        self.f_bool = force
    def create(self, fpath):
        if self.fmt == 'nodal':
            return Nodal(fpath, self.fmt, self.vir_bool, self.f_bool)
        elif self.fmt == 'dump':
            return Dump(fpath, self.fmt)
        elif self.fmt == 'cac':
            return Cac(fpath, self.fmt, self.vir_bool, self.f_bool)
        #elif NEW FORMAT CLASS DEFINITIONS HERE
        else:
            pass
