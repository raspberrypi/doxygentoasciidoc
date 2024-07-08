import os
import sys
import argparse
import yaml

from bs4 import BeautifulSoup
from .nodes import DoxygenindexNode


def main():
    """Convert the given Doxygen index.xml to AsciiDoc and print the result."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="The path of the file to convert", default=None)
    args = parser.parse_args()
    filename = args.file
    if filename:
        xmldir = os.path.dirname(filename)
        with open(filename, encoding="utf-8") as xml:
            print(
                DoxygenindexNode(
                    BeautifulSoup(xml, "xml").doxygenindex, xmldir=xmldir
                ).to_asciidoc()
            )
    else:
        sys.exit(1)
