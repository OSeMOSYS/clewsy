# -*- coding: utf-8 -*-
"""
This is the CLEWs building command line script for clewsy.
"""

import argparse
import sys
import logging

from clewsy import __version__
from clewsy.model_building import build

__author__ = "Taco Niet"
__copyright__ = "Taco Niet"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def get_parser():
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="CLEWsy tools for CLEWs models")
    parser.add_argument(
        "--version",
        action="version",
        version="clewsy {ver}".format(ver=__version__))
    
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO)
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG)
    subparsers = parser.add_subparsers()
    
    # Parser for building a clews model
    build_parser = subparsers.add_parser("build", help="build a CLEWs model from clustering data and a yaml model description file")
    build_parser.add_argument(
        "yamlfile",
        help="Please provide the yaml model description file",
    )
    build_parser.set_defaults(func=build)
    
    
    return parser


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    parser = get_parser()
    args = parser.parse_args(sys.argv[1:])
    if args.loglevel == "INFO":
        logging.basicConfig(level=logging.INFO)
    if args.loglevel == "DEBUG":
        logging.basicConfig(level=logging.DEBUG)

    def exception_handler(
        exception_type, exception, traceback, debug_hook=sys.excepthook
    ):
        if args.loglevel:
            debug_hook(exception_type, exception, traceback)
        else:
            print("{}: {}".format(exception_type.__name__, exception.message))

    sys.excepthook = exception_handler

    if "func" in args:
        args.func(args)
    else:
        parser.print_help()
    
    
    #setup_logging(args.loglevel)
   # _logger.debug("Starting crazy calculations...")
    
    
    
    #print("The {}-th Fibonacci number is {}".format(args.n, fib(args.n)))
    #_logger.info("Script ends here")


def run():
    """Entry point for console_scripts
    """
    print("clewsy CLEWs Model Building Script.")
    print("When using clewsy please reference:")
    print("T. Niet and A. Shivakumar (2020):  clewsy:  Script for building CLEWs models.")
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
