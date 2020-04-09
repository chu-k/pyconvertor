
class FormatClass(object):
# This base class simply maps to the child class constructors, based on file extension
    def __init__(self, path, fmt):
        self.SIZES = {0: (1, 'Atom'), 1: (8, 'Eight_Node')}
        self.path = path
        self.format = fmt

    def get_list(self):
        return(self.list_data)

    def __str__(self):
        return(self.fmt)

