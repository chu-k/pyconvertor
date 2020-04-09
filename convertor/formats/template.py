
from .parent import FormatClass

class TemplateClass(FormatClass):
# this is template for defining methods of new input file formats
    def __init__(self, *args):
    # call the parent constructor, also initialize any instance variables
        super(TemplateClass, self).__init__(*args)

    def read_header(self):
    # parse header info into desired format
        #self.header = ...
        pass

    def read_body(self):
    # read coordinate data from file into desired data structures
    # set the appropriate class attributes for later formatting
        pass

    def to_list_cac(self):
    # convert the header and body data into a single list of lines
    # can be formatted however you want

    def to_list_ext(self):
    # getattr will match the extension type to format to desired output list