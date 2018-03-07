#!/usr/bin/env python

"""
unit_test script is a script to test the parser_paper class.
Future to be implementated, this is file is from an old
implementation for a different problem.

Use:
    python 



"""

__author__ = "Tiago Botari"
__copyright__ = ""
__version__ = "1.0"
__maintainer__ = "Tiago Botari"
__email__ = "tiagobotari@gmail.com"
__date__ = "May 20 2017"

import unittest
import argparse


class test1_offline(query_mp_database.query_mp_database):
    # Test a list of html files from paper of different publishers, future...

    files = []


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""unit_test is a script that test the ParserPaper class""",
        epilog="""Author: {}
            Version: {}
            Last updated: {}""".format(__author__, __version__, __date__))
    parser.add_argument(
        "-ARG1",
        help="""descriptions of ARG1 .""")
    args = parser.parse_args()
    if args.ARG1 is None:
        ARG1 = args.ARG1
    if len(ARG1) > 0:
        print("Performing online test!")
    else:
        print("Performing just offline test!")
    print("\nPerforming offline test!")
    suite = unittest.TestLoader().loadTestsFromTestCase(test1_offline)
    unittest.TextTestRunner().run(suite)
