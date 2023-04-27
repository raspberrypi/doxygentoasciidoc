from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import BoldNode


def test_bold_node_renders_nested_nodes_as_bold(tmp_path):
    xml = """<bold>Hello <emphasis>world</emphasis></bold>"""

    asciidoc = BoldNode(BeautifulSoup(xml, "xml").bold, xmldir=tmp_path).to_asciidoc()

    assert asciidoc == "*Hello _world_*"
