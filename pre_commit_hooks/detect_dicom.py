#!/usr/bin/python
from __future__ import print_function
import magic
import sys
import argparse

def detect_dicom(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)

    dicom_files = []

    for filename in args.filenames:
        if magic.from_file(filename,mime=True) == 'application/dicom':
            dicom_files.append(filename)

    if dicom_files:
        for dicom_file in dicom_files:
            print('DICOM file found: {}'.format(dicom_file))
        sys.exit(1)
    sys.exit(0)

if __name__ == '__main__':
    detect_dicom()
