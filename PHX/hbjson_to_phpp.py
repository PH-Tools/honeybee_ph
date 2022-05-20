# from rich import print
import pathlib
import sys

from PHX.from_HBJSON import read_HBJSON_file, create_project
from PHX.to_PHPP import phpp_app
from PHX.to_PHPP.phpp_localization.shape_model import PhppShape

try:  # import the core honeybee dependencies
    from honeybee.config import folders as hb_folders
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

import xlwings as xw

if __name__ == '__main__':
    print("- " * 50)
    print(sys.argv[2])
    print(xw.books)
