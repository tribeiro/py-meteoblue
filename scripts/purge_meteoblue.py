#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
from py_meteoblue.src.meteoblue import MeteoBlue

def main(argv):

    import argparse

    parser = argparse.ArgumentParser(description='Sort files from an observing night and generate configuration'
                                                 'scripts.')

    parser.add_argument('-c', '--configuration',
                        help='Configuration file.',
                        type=str)

    parser.add_argument('-o', '--output',
                        help='Output name.',
                        type=str)

    parser.add_argument('--format',
                        help='Format of the output file. Same as astropy.io.ascii',
                        type=str,
                        default='ascii.csv')

    parser.add_argument('--verbose', '-v', action='count')

    args = parser.parse_args(argv[1:])

    mb = MeteoBlue(args.configuration)

    data = mb.query()
    data.write(args.output,
               format=args.format)

    return 0


if __name__ == '__main__':
    main(sys.argv)
