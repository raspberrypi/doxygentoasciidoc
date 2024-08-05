import os
import sys
import argparse
import yaml

from bs4 import BeautifulSoup
from .nodes import Node, DoxygenindexNode


def main():
    """Convert the given Doxygen index.xml to AsciiDoc and print the result."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="The path of the file to convert", default=None)
    parser.add_argument("-c", "--child", help="Is NOT the root index file", default=False, action='store_true')
    args = parser.parse_args()
    filename = args.file
    is_child = args.child
    if filename:
        xmldir = os.path.dirname(filename)
        with open(filename, encoding="utf-8") as xml:
            if is_child:
                print(
                    Node(
                        BeautifulSoup(xml, "xml").doxygen, xmldir=xmldir
                    ).to_asciidoc()
                )
            else:
                print(
                    DoxygenindexNode(
                        BeautifulSoup(xml, "xml").doxygenindex, xmldir=xmldir
                    ).to_asciidoc()
                )
                
    else:
        sys.exit(1)
