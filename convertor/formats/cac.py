import numpy as np
import sys
from .parent import FormatClass
from ..utils import helpers as hp

class Cac(FormatClass):
# this is template for defining methods of new input file formats
    def __init__(self, *args):
    # call the parent constructor, also initialize any instance variables
        super(Cac, self).__init__(*args)
        self.read_header()
        self.read_body()

    def read_header(self):
    # parse header info into desired format
        input = self.path
        self.header = [hp.read_line_number(input, 2).strip().split(),
                        hp.read_line_number(input, 3).strip().split(),
                        [hp.read_line_number(input, n+5).split() for n in range(3)],
                      ]
        self.nelements = int(self.header[0][0])
        self.ntypes = int(self.header[1][0])
        self.box = [a[:2] for a in self.header[2]]
        self.header.append([hp.read_line_number(input, n+10).split() for n in range(self.ntypes)])
        self.masses = self.header[3][:2]

    def read_body(self):
    # reads in cac format data into a numpy array
    # sets the size array and the position array, ordered by id
        info = np.zeros((self.nelements,5))
        atypes = np.zeros((self.nelements,8))
        positions = np.zeros((self.nelements, 8, 3))

        eid = 0
        is_info = True
        lines_remaining = 0


        nread = 0
        nat = 0
        nele = 0
        with open(self.path) as in_fp:
        # Determine if the next element info has been read
        #   if it's an element, 8 lines follow
        #   else just one
            for _ in range(13 + self.ntypes): #skips header lines
                next(in_fp)
            for line in in_fp:
                line_arr = line.strip().split()
                if is_info: # contains id, element type/scale
                    eid = int(line_arr[0]) - 1
                    etype = line_arr[1:][0]
                    # .cac format uses "Eight_Node" and "Atom"
                    if etype == 'Eight_Node':
                        esize = 1
                    elif etype == 'Atom':
                        esize = 0
                    line_arr[1] = esize
                    info[eid] = line_arr[1:]
                    is_info = False
                    remaining = self.SIZES[esize][0]
                else:
                    poly_i = int(line_arr[0]) - 1
                    if esize:
                        positions[eid][poly_i] = [i for i in line_arr[3:]]
                        atypes[eid][poly_i] = line_arr[2]
                        remaining -= 1
                        # step through all DOF lines in an element
                        if not remaining:
                            is_info = True
                            nele += 1
                    else:   
                        positions[eid][poly_i] = [i for i in line_arr[3:]]
                        atypes[eid][poly_i] = line_arr[2]                        
                        is_info = True
                        nat += 1
                    nread += 1
        # basic lines read check
        print(f"{nat} atoms, {nele} elements, {nread} total DOF")
        try:
            assert(nread - 7*nele == self.nelements)
            assert(nat + nele == self.nelements)
        except AssertionError:
            print("Failed tests")
            sys.exit(1)


        self.info = info
        self.positions = positions
        self.atypes = atypes
        self.nnodes = nread

    def to_list_cacovito(self):
        """the *.cacovito format is simply xyz but with an element tag column"""
        a = []
        a.append(f"{self.nnodes}\n")
        a.append(f"# read from {self.format}\n")

        for id in range(self.nelements):
            st = self.info[id]
            etype = int(st[0])
            curr_p = self.positions[id]

            for p in range(self.SIZES[etype][0]):
                atype = int(self.atypes[id][p])
                a.append(f'{id} {etype} {atype} {"    ".join(str(c) for c in curr_p[p])}\n')

        self.list_data = a

    def to_list_xyz(self):
        """ extended XYZ allows for definition of header info, box info, column tags"""
        a = []
        lx, ly, lz = self.box
        # EXYZ
        header_string = (f'{self.nnodes}\n' 
                         f'Lattice="'
                         f'{float(lx[1]) + abs(float(lx[0]))} 0.0 0.0 0.0 '
                         f'{float(ly[1]) + abs(float(ly[0]))} 0.0 0.0 0.0 '
                         f'{float(lz[1]) + abs(float(lz[0]))} 0.0 0.0 0.0" '
                         f'Origin="{lx[0]} {ly[0]} {lz[0]}" '
                         f'Properties=id:I:1:'
                         f'molecule_type:I:1:species:I:1:pos:R:3\n')
        a.append(header_string)
        # main elemnt info
        for id in range(self.nelements):
            st = self.info[id]
            etype = int(st[0])
            curr_p = self.positions[id]

            for p in range(self.SIZES[etype][0]):
                atype = int(self.atypes[id][p])
                a.append(f'{id} {etype} {atype} {"    ".join(str(c) for c in curr_p[p])}\n')
        self.list_data = a