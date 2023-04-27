from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import NdashNode


def test_ndash_node_renders_as_an_en_dash(tmp_path):
    xml = """<ndash/>"""

    asciidoc = NdashNode(BeautifulSoup(xml, "xml").ndash, xmldir=tmp_path).to_asciidoc()

    assert asciidoc == "–"
