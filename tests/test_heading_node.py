from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import HeadingNode


def test_heading_node(tmp_path):
    xml = """<sect1><title>Examples Index</title></sect1>"""

    asciidoc = HeadingNode(
        BeautifulSoup(xml, "xml").title, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == "=== Examples Index"
