import argparse
from .formats import base
from .utils import helpers

def read_args():
    parser = argparse.ArgumentParser(description='''
        convert between various CAC formats based on extension
        *.cac
        *.lmp
        *.nodal
        ''')
    parser.add_argument('--input', '-i', help='input file for conversion', required=True)
    parser.add_argument('--output', '-o', help='output file name', required=True)
    return(parser.parse_args())

def run():
    args = read_args()
    # TODO: detect input filetype from extension
    in_ext = helpers.get_format(args.input)
    out_ext = helpers.get_format(args.output)

    base_format = base.Selector(in_ext)
    formatted = base_format.create(args.input)

    getattr(formatted, f"to_list_{out_ext}")()

    helpers.write_to_file(formatted.get_list(), args.output)

if __name__ == '__main__':
    run()