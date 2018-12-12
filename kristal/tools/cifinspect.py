"""Commandline tool for inspecting CIF files.

The purpose of this tool is for debugging of Kristal's CIF grammar.
"""
import argparse
from pkg_resources import resource_filename
import lark

GRAMMAR_PATH = 'io/cifgrammar.lark'

def main():
    """Entry point of this script."""
    parser = argparse.ArgumentParser(
        description='Inspect elements found in CIF file.')
    parser.add_argument(
        'input',
        help='Input CIF file',
        type=argparse.FileType('r'))

    args = parser.parse_args()
    cif_content = args.input.read()
    args.input.close()

    with open(resource_filename('kristal', GRAMMAR_PATH)) as grammar_file:
        grammar = grammar_file.read()

    cif_parser = lark.Lark(grammar, start='cif', parser='earley')
    tree = cif_parser.parse(cif_content)
    print(tree.pretty())

if __name__ == '__main__':
    main()
