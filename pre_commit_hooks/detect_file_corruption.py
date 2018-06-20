#!/usr/bin/python
from __future__ import print_function
import argparse
import os
import sys
import magic
from util import cmd_output
import mimetypes

IGNORE_LIST_MAGIC = ['.bib','.yml','.yaml','.sh','Makefile']


def check_shell_files(fn):
    try:
        cmd_output('shellcheck',fn)
    except:
        print('  Shellcheck error. Run "shellcheck {}" for details.'.format(fn,))
        return False
    return True

def check_optimal_png(fn, simulation=True):
    if simulation:
        _, serr= cmd_output('optipng','-simulate','-v',fn)
    else:
        _, serr= cmd_output('optipng','-preserve','-clobber',fn)
    c = serr.find('optimized')

    if c<0:
        print('  Suboptimal png. Try "optipng {}"'.format(fn))
        return False
    return True

def check_general(ftype, fn, cmds):
    try:
        cmd_output(*cmds)
    except:
        print('  Corrupt {} file: {}'.format(ftype, fn))
        return False
    return True


def check_mp3(fn):
    return check_general('mp3', fn, ['mp3check', '-s', '-e', fn])


def check_zip(fn):
    return check_general('zip', fn, ['zip', '-T', fn])


def check_gzip(fn):
    return check_general('gzip', fn, ['gzip', '-t', fn])


def check_bzip(fn):
    return check_general('bzip2', fn, ['bzip2', '-t', fn])


def check_xz(fn):
    return check_general('xz', fn, ['xz', '-t', fn])


def check_zstd(fn):
    return check_general('zstd', fn, ['zstd', '-t', fn])


def check_zstd(fn):
    return check_general('tar', fn, ['tar', '-tf', fn])


def check_general_image(fn):
    return check_general('image', fn, ['convert', fn, '/dev/null'])


def check_with_ffmpeg(ftype,fn):
    try:
        sout, serr = cmd_output('ffmpeg', '-v', 'error', '-i', fn, '-f', 'null', '-',)
        if len(serr.trim()) > 0:
            print('  Corrupt {} file: {}'.format(ftype,fn))
            return False
    except:
        print('  Corrupt {} file: {}'.format(ftype,fn))
        return False
    return True


def check_jpeg(fn):
    try:
        sout, serr = cmd_output('jpeginfo', fn)
        if len(serr.trim()) > 0:
            print('  Corrupt JPEG file: {}'.format(fn))
            return False
    except:
        print('  Corrupt JPEG file: {}'.format(fn))
        return False
    return True


def main(argv=None):
    return_code = 0
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--opti-png-check',
        action='store_true',
        default=True,
        dest='optipng',
        help='Check if PNG files are compressible.',
    )
    parser.add_argument(
        '--opti-png-compress',
        action='store_true',
        default=False,
        dest='compresspng',
        help='Perform PNG compression, if possible.',
    )

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
    parser.add_argument(
        '--magic',
        action='store_true',
        default=True,
        dest='magic',
        help='Check consistency betwen file type and extenstion.',
    )
    parser.add_argument(
        '--no-magic',
        action='store_false',
        default=True,
        dest='magic',
        help='Disable file extension consistency check.',
    )
    parser.add_argument(
        '--general-image',
        action='store_true',
        default=True,
        dest='image',
        help='Check general image file (ImageMagick).',
    )
    parser.add_argument(
        '--no-general-image',
        action='store_false',
        default=True,
        dest='image',
        help='Disable general image file integrity test.',
    )
    parser.add_argument(
        '--general-compressed',
        action='store_true',
        default=True,
        dest='compress',
        help='Check general compressed file. (zip,bz2,gz,xz,zstd).',
    )
    parser.add_argument(
        '--no-general-compressed',
        action='store_false',
        default=True,
        dest='compress',
        help='Disable general image file integrity test.',
    )
    parser.add_argument(
        '--video',
        action='store_true',
        default=True,
        dest='video',
        help='Check video file integrity (FFMPEG)',
    )
    parser.add_argument(
        '--no-video',
        action='store_false',
        default=True,
        dest='video',
        help='Disable video file integrity check.',
    )
    parser.add_argument(
        '--audio',
        action='store_true',
        default=True,
        dest='audio',
        help='Check audio file integrity (FFMPEG)',
    )
    parser.add_argument(
        '--no-audio',
        action='store_false',
        default=True,
        dest='audio',
        help='Disable audio file integrity check.',
    )
    parser.add_argument(
        '--jpeg',
        action='store_true',
        default=True,
        dest='jpeg',
        help='Check video file integrity (mp4,mkv,avi)',
    )
    parser.add_argument(
        '--no-jpeg',
        action='store_false',
        default=True,
        dest='jpeg',
        help='Disable JPEG file integrity check.',
    )

    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    for fname in args.filenames:
        low = fname.lower()
        extension = "."+(low.split('.')[-1])
        mime = magic.from_file(fname, mime=True)
        ftype = mime.split('/')[0]

        if args.magic:
            if extension not in IGNORE_LIST_MAGIC:
                all_ext = mimetypes.guess_all_extensions(mime)
                if extension not in all_ext:
                    print('  Mismatched type ({}) and extension: {}'.format(mime, fname))
                    return_code = 1
                    continue

            if args.image:
                if ftype == 'image':
                    if not check_general_image(fname):
                        return_code = 1

            if args.video:
                if ftype == 'video':
                    if not check_with_ffmpeg('video', fname):
                        return_code = 1

            if args.audio:
                if ftype == 'audio':
                    if not check_with_ffmpeg('audio', fname):
                        return_code = 1

            if args.compress:
                if ftype == 'application/gzip':
                    if not check_with_gzip(fname):
                        return_code = 1
                if ftype == 'application/zip':
                    if not check_with_gzip(fname):
                        return_code = 1
                if ftype == 'application/x-bzip2':
                    if not check_with_bzip2(fname):
                        return_code = 1
                if ftype == 'application/x-xz':
                    if not check_with_xz(fname):
                        return_code = 1
                if ftype == 'application/x-zstd':
                    if not check_with_zstd(fname):
                        return_code = 1
                if ftype == 'application/x-tar':
                    if not check_with_zstd(fname):
                        return_code = 1

        if extension=='.sh':
            if not check_shell_files(fname):
                return_code = 1

        if args.mp3 and extension == '.mp3':
            if not check_mp3(fname):
                return_code = 1
        if extension == '.png':
            if not check_optimal_png(fname,not args.compresspng):
                return_code = 1

    sys.exit(return_code)



if __name__ == '__main__':
    main()
