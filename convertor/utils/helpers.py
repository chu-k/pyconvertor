import os.path as path
import sys

def read_line_number(file, lineno):
# return the whitespace-stripped line at 'lineno'
    with open(file) as f_fp:
        for _ in range(lineno):
            next(f_fp)
        return(next(f_fp).strip())


def write_to_file(string_list, output_file):
# write every element of a list to a specified output file
# prompt on overwrite
    if path.isfile(output_file):
        ow = input(f"{output_file} exists, overwrite? y/n(default): ")
        if ow == 'y' or ow == 'yes':
            print(f"Replacing {output_file}")
        else:
            print("Will not overwrite, exit conversion...")
            sys.exit(1)

    with open(output_file, 'w+') as out_fp:
        for line in string_list:
            out_fp.write(line)

def get_format(file):
# wrapper for splitExt
    return(path.splitext(file)[-1].split('.')[-1])
