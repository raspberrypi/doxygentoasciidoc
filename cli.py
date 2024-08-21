import os
import argparse

from bs4 import BeautifulSoup
from .nodes import Node, DoxygenindexNode


def main():
    """Convert the given Doxygen index.xml to AsciiDoc and output the result."""
    parser = argparse.ArgumentParser(
        prog="doxygentoasciidoc", description="Convert Doxygen XML to AsciiDoc"
    )
    parser.add_argument(
        "file",
        type=argparse.FileType("r", encoding="utf-8"),
        help="The path of the Doxygen XML file to convert",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Write to file instead of stdout",
    )
    parser.add_argument(
        "-c",
        "--child",
        help="Is NOT the root index file",
        action="store_true",
    )

    args = parser.parse_args()

    with args.file as file:
        xmldir = os.path.dirname(file.name)

        if args.child:
            result = Node(
                BeautifulSoup(file, "xml").doxygen, xmldir=xmldir
            ).to_asciidoc(depth=1)
        else:
            result = DoxygenindexNode(
                BeautifulSoup(file, "xml").doxygenindex, xmldir=xmldir
            ).to_asciidoc(depth=2)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as output:
                output.write(result)
        else:
            print(result)
