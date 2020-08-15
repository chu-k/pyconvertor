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
    parser.add_argument('--replace', '-r', help='force overwrite without prompt', action="store_true")
    parser.add_argument('--virial', '-v', help='look for matching virial files', action="store_true")
    parser.add_argument('--force', '-f', help='look for matching force files', action="store_true")

    return(parser.parse_args())

def run():
    args = read_args()
    # TODO: detect input filetype from extension
    in_ext = helpers.get_format(args.input)
    out_ext = helpers.get_format(args.output)

    base_format = base.Selector(in_ext, args.virial, args.force)
    formatted = base_format.create(args.input)

    getattr(formatted, f"to_list_{out_ext}")()

    helpers.write_to_file(formatted.get_list(), args.output, args.replace)

if __name__ == '__main__':
    run()