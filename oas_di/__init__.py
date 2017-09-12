from argparse import ArgumentParser, Namespace
import os
from .process import process_file as _process_file


def __main__():
    parser = ArgumentParser()
    parser.add_argument("filename", help="OAS File location", type=str)
    parser.add_argument("--models-library", dest="models_lib", help="Common models python-lib", type=str, default=None)
    parser.add_argument("--lib", dest="lib2", help="Common models python-lib", type=list, default=None)

    args = parser.parse_args()
    __internal_run(args)


def process_file(filename, **argv):
    args = Namespace()
    setattr(args, 'filename', filename)
    setattr(args, 'models_lib', argv.get('models_lib', None))
    __internal_run(args)


def __internal_run(args):
    # checking if file exists
    if not os.path.exists(args.filename):
        print("OAS file is missing")
        exit(1)

    # processing file
    _process_file(args)
