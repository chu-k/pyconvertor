import numpy as np

from .parent import FormatClass
from ..utils import helpers as hp

class Dump(FormatClass):
# this is template for defining methods of new input file formats
    def __init__(self, *args):
    # call the parent constructor, also initialize any instance variables
        super(Dump, self).__init__(*args)
        self.read_header()
        self.read_body()

    def read_header(self):
    # parse header info into desired format
        input = self.path
        self.header = self.header = [hp.read_line_number(input, 1).split(),
                        hp.read_line_number(input, 3).split(),
                        [hp.read_line_number(input, n+5).split() for n in range(3)],
                      ]
        self.timestep = int(self.header[0][0])
        self.natoms = int(self.header[1][0])
        self.box = [a[:2] for a in self.header[2]]
        self.cols = hp.read_line_number(input,8).split()[2:]

    def read_body(self):
    # read coordinate data from file into desired data structures
    # set the appropriate class attributes for later formatting
        positions = np.zeros((self.natoms, len(self.cols)))

        nread = 0

        with open(self.path) as in_fp:
            for _ in range(9): #skips header lines
                next(in_fp)
            for line in in_fp:
                positions[nread] = np.array(line.split())
                nread += 1
        print(f"Read ({nread}/{self.natoms}) atoms")

        try:
            assert(nread == self.natoms)
        except AssertionError:
            print("Failed tests")
            sys.exit(1)

        self.positions = positions

    def to_list_last(self):
    # convert to xyz format required by normal NEB
        a = []
        a.append(f"# read from {self.format}\n")
        a.append(f"{self.natoms}\n")

        for i in range(self.natoms):
            curr = self.positions[i]
            atomid = int(curr[2])
            atomxyz = curr[3:6]
            a.append(f'{atomid}\t{"     ".join(str(a) for a in atomxyz)}\n')

        self.list_data = a