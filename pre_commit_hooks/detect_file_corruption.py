#!/usr/bin/python
from __future__ import print_function
import argparse
import os
import sys
import magic
import identify
from util import cmd_output

def check_mp3(filename):
    try:
        cmd_output('mp3check','-s','-e',filename)
    except:
        return False
    return True

def main(argv=None):
    if argv is None:
        argv=sys.argv
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--mp3',
        action='store_true',
        default=True,
        dest='mp3',
        help='Check MP3 file integrity.',
    )
    parser.add_argument(
        '--no-mp3',
        action='store_false',
        default=True,
        dest='mp3',
        help='Disable MP3 file integrity check.',
    )

    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    for fname in args:
        if fname.endswith('.mp3')
            if not check_mp3(fname):
                return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
