import os
import sys

from bs4 import BeautifulSoup
from .nodes import DoxygenindexNode


def main():
    """Convert the given Doxygen index.xml to AsciiDoc and print the result."""
    if sys.argv[1:]:
        filename = sys.argv[1]
        xmldir = os.path.dirname(sys.argv[1])
        with open(filename, encoding="utf-8") as xml:
            print(
                DoxygenindexNode(
                    BeautifulSoup(xml, "xml").doxygenindex, xmldir=xmldir
                ).to_asciidoc()
            )
    else:
        sys.exit(1)
