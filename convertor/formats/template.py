
from .parent import FormatClass
from ..utils import helpers as hp

class TemplateClass(FormatClass):
# this is template for defining methods of new input file formats
    def __init__(self, *args):
    # call the parent constructor, also initialize any instance variables
        super(TemplateClass, self).__init__(*args)

    def read_header(self):
    # parse header info into desired format
        #self.header = ...
        '''
        - the helper function 
                >hp.read_line_number(filename, N)
          returns the line number N for further manipulation.
        - save instance information as:
            >self.natoms = ____
            >self.box = ___
        '''
        pass

    def read_body(self):
    # read coordinate data from file into desired data structures
    # set the appropriate class attributes for later formatting
        pass

    '''
    The "to_list_FMT" functions should format the header and coordinate 
    data into one single list, with each each new line as a separate list 
    element. 
    '''
    def to_list_cac(self):
    # convert the header and body data into a single list of lines
    # can be formatted however you want

    def to_list_ext(self):
    # getattr will match the extension type to format to desired output list