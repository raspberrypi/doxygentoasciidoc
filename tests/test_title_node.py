from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import TitleNode


def test_title_node(tmp_path):
    xml = """<title>Interrupt Numbers</title>"""

    asciidoc = TitleNode(BeautifulSoup(xml, "xml").title, xmldir=tmp_path).to_asciidoc()

    assert asciidoc == ".Interrupt Numbers"
