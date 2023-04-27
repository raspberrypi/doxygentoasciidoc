from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import MdashNode


def test_mdash_node_renders_as_an_em_dash(tmp_path):
    xml = """<mdash/>"""

    asciidoc = MdashNode(BeautifulSoup(xml, "xml").mdash, xmldir=tmp_path).to_asciidoc()

    assert asciidoc == "—"
