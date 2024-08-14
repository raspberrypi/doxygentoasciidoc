from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import Node, NoneNode


def test_none_node(tmp_path):
    xml = """<compoundname>examples_page</compoundname>"""

    asciidoc = NoneNode(
        BeautifulSoup(xml, "xml").compoundname, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == ""
