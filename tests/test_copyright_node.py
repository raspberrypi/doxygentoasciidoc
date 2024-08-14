from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import CopyrightNode


def test_copyright_node(tmp_path):
    xml = """<copy/>"""

    asciidoc = CopyrightNode(
        BeautifulSoup(xml, "xml").copy, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == "©"
