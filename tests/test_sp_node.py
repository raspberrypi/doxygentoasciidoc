from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import SpNode


def test_sp_node_renders_as_a_space(tmp_path):
    xml = """<sp/>"""

    asciidoc = SpNode(BeautifulSoup(xml, "xml").sp, xmldir=tmp_path).to_asciidoc()

    assert asciidoc == " "
