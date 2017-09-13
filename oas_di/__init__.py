from argparse import ArgumentParser, Namespace
import os
from .process import process_file as _process_file


def __main__():
    parser = ArgumentParser()
    parser.add_argument("filename", help="OAS File location", type=str)
    parser.add_argument("--models-library", dest="models_lib", help="Common models python-lib", type=str, default=None)
    parser.add_argument("--target_filename", dest="target_filename",
                        help="Target filename. If not specified, will add '_pp' to filename", type=str, default=None)

    args = parser.parse_args()
    __internal_run(args)


def entrypoint_viacode(filename, **argv):
    args = Namespace()
    setattr(args, 'filename', filename)
    setattr(args, 'models_lib', argv.get('models_lib', None))
    setattr(args, 'target_filename', argv.get('target_filename', None))
    __internal_run(args)


def __internal_run(args):
    # checking if file exists
    if not os.path.exists(args.filename):
        print("OAS file is missing")
        exit(1)

    # processing file
    _process_file(args)
