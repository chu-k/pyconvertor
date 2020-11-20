import numpy as np
import os.path
import sys

from ..utils import helpers as hp
from .parent import FormatClass

class Nodal(FormatClass):
# (modified) lmpcac nodal output data that includes box bounds, extra info
    def __init__(self, *args):
        super(Nodal, self).__init__(*args)
        self.read_header()
        self.read_body()

        if self.vir_bool :
            self.read_virial()
        if self.f_bool:
            self.read_force()




    def read_header(self):
    # parse header info
        input = self.path
        self.header = [hp.read_line_number(input, 0).split(),
                        hp.read_line_number(input, 1).split(),
                        hp.read_line_number(input, 2).split(),
                        [hp.read_line_number(input, n+4).split() for n in range(3)],
                      ]
        try:
            self.nnodes = int(self.header[0][4])
        except ValueError: # catch header line with no comment flag
            self.nnodes = int(self.header[0][3])

        self.nelements = int(self.header[1][0])
        self.ntypes = int(self.header[2][0])
        self.box = [a[:2] for a in self.header[3]]
        self.header.append([hp.read_line_number(input, n+10).split() for n in range(self.ntypes)])
        self.masses = self.header[4][:]

    def read_body(self):
    # reads in cac/nodal 8-node data into a numpy array
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
            for _ in range(12 + self.ntypes): #skips header lines
                next(in_fp)
            for line in in_fp:
                line_arr = line.split()
                if is_info: # contains id, element type/scale
                    eid = int(line_arr[0]) - 1
                    info[eid] = line_arr[1:]
                    esize = int(info[eid][0])
                    is_info = False
                    remaining = self.SIZES[esize][0]
                else:
                    poly_i = int(line_arr[0]) - 1
                    # esize != 0 is an element
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
        print(f"Read ({nread}/{self.nnodes}) positions")
        print(f"{nat} atoms, {nele} elements")
        try:
            assert(nread == self.nnodes)
            assert(nat + nele*8 == self.nnodes)
            assert(nat + nele == self.nelements)
        except AssertionError:
            print("Failed tests")
            sys.exit(1)
        self.info = info
        self.positions = positions
        self.atypes = atypes

    def read_virial(self):
    # reads in cac/virial 8-node data into a numpy array
    # filename should be *.virial, matching timestep *.nodal
        virial = np.zeros((self.nelements, 8, 6))

        basename, step = os.path.split(self.path)
        virial_path = os.path.join(basename,os.path.splitext(step)[0] + ".virial")
        if not os.path.exists(virial_path):
            print(f"ERROR: Could not find a virial file matching {step}")
            sys.exit(1)

        eid = 0
        is_info = True
        lines_remaining = 0


        nread = 0
        nat = 0
        nele = 0
        with open(virial_path) as in_fp:
        # Determine if the next element info has been read
        #   if it's an element, 8 lines follow
        #   else just one
            for _ in range(1): #skips header lines
                next(in_fp)
            for line in in_fp:
                line_arr = line.split()
                if is_info: # contains id, element type/scale
                    eid = int(line_arr[0]) - 1
                    esize = int(self.info[eid][0])
                    is_info = False
                    remaining = self.SIZES[esize][0]
                else:
                    poly_i = int(line_arr[0]) - 1
                    # esize != 0 is an element
                    if esize:
                        virial[eid][poly_i] = [i for i in line_arr[3:]]
                        remaining -= 1
                        # step through all DOF lines in an element
                        if not remaining:
                            is_info = True
                            nele += 1
                    else:
                        virial[eid][poly_i] = [i for i in line_arr[3:]]
                        is_info = True
                        nat += 1

                    nread += 1
        # basic lines read check
        print(f"-- read virial stresses")

        try:
            assert(nread == self.nnodes)
            assert(nat + nele*8 == self.nnodes)
            assert(nat + nele == self.nelements)
        except AssertionError:
            print("mismatch in nodal/virial file")
            sys.exit(1)
        self.virial = virial

    def to_list_cac(self):
    # convert all data to a single list in cac format
        a = []
        a.append(f"# read from {self.format}\n\n")

        a.append(f"\t{self.nelements} cac elements\n")
        a.append(f"\t{self.ntypes} atom types\n\n")

        a.append("\t" + " ".join(self.box[0]) + " xlo xhi\n")
        a.append("\t" + " ".join(self.box[1]) + " ylo yhi\n")
        a.append("\t" + " ".join(self.box[2]) + " zlo zhi\n")

        a.append("Masses\n\n")
        [a.append("{}\t{}\n".format(*m)) for m in self.masses]

        a.append("\nCAC Elements\n\n")

        for id in range(self.nelements):
            st = self.info[id]
            etype = int(st[0])
            curr_p = self.positions[id]

            a.append(f'\t{id+1}\t{self.SIZES[etype][1]}\t{"    ".join(str(a) for a in st[1:].astype(int))}\n')

            for p in range(self.SIZES[etype][0]):
                atype = int(self.atypes[id][p])
                a.append(f'\t{p+1}\t1\t{atype}\t{"    ".join(str(c) for c in curr_p[p])}\n')

        self.list_data = a

    def to_list_last(self):
    # convert to xyz format required by CAC-neb
        a = []
        a.append(f"# read from {self.format}\n\n")
        a.append(f"{self.nelements}\n")

        for id in range(self.nelements):
            st = self.info[id]
            etype = int(st[0])
            curr_p = self.positions[id]

            a.append(f'{id+1}\t{self.SIZES[etype][1]}\t{"    ".join(str(a) for a in st[1:].astype(int))}\n')

            for p in range(self.SIZES[etype][0]):
                a.append(f'{p+1}\t1\t1\t{"    ".join(str(c) for c in curr_p[p])}\n')

        self.list_data = a

    def to_list_cacovito(self):
        """the *.cacovito format is simply xyz but with an element tag column"""
        a = []
        a.append(f"{self.nnodes}\n")
        a.append(f"# read from {self.format}\n")

        for id in range(self.nelements):
            st = self.info[id]
            etype = int(st[0])
            curr_p = self.positions[id]
            if self.vir_bool:
                curr_v = self.virial[id]

            for p in range(self.SIZES[etype][0]):
                atype = int(self.atypes[id][p])
                if self.vir_bool:
                    a.append(f'{id} {etype} {atype} {"    ".join(str(c) for c in curr_p[p])} \
                                                {"    ".join(str(v) for v in curr_v[p])}\n')
                else:
                    a.append(f'{id} {etype} {atype} {"    ".join(str(c) for c in curr_p[p])}\n')

        self.list_data = a

    def to_list_xyz(self):
        """ extended XYZ allows for definition of header info, box info, column tags"""
        a = []
        lx, ly, lz = self.box
        # EXYZ
        if self.vir_bool:
            header_string = (f'{self.nnodes}\n' 
                         f'Lattice="'
                         f'{float(lx[1]) + abs(float(lx[0]))} 0.0 0.0 0.0 '
                         f'{float(ly[1]) + abs(float(ly[0]))} 0.0 0.0 0.0 '
                         f'{float(lz[1]) + abs(float(lz[0]))} 0.0 0.0 0.0" '
                         f'Origin="{lx[0]} {ly[0]} {lz[0]}" '
                         f'Properties=id:I:1:'
                         f'molecule_type:I:1:species:I:1:pos:R:3:stress:R:6\n')
        else:
            header_string = (f'{self.nnodes}\n' 
                         f'Lattice="'
                         f'{float(lx[1]) + abs(float(lx[0]))} 0.0 0.0 0.0 '
                         f'{float(ly[1]) + abs(float(ly[0]))} 0.0 0.0 0.0 '
                         f'{float(lz[1]) + abs(float(lz[0]))} 0.0 0.0 0.0" '
                         f'Origin="{lx[0]} {ly[0]} {lz[0]}" '
                         f'Properties=id:I:1:'
                         f'molecule_type:I:1:species:I:1:pos:R:3\n')
        a.append(header_string)

        for id in range(self.nelements):
            st = self.info[id]
            etype = int(st[0])
            curr_p = self.positions[id]
            if self.vir_bool:
                curr_v = self.virial[id]

            for p in range(self.SIZES[etype][0]):
                atype = int(self.atypes[id][p])
                if self.vir_bool:
                    a.append(f'{id} {etype} {atype} {"    ".join(str(c) for c in curr_p[p])} \
                                                {"    ".join(str(v) for v in curr_v[p])}\n')
                else:
                    a.append(f'{id} {etype} {atype} {"    ".join(str(c) for c in curr_p[p])}\n')

        self.list_data = a