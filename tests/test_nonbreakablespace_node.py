from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import NonbreakablespaceNode


def test_sp_node_renders_as_a_space(tmp_path):
    xml = """<nonbreakablespace/>"""

    asciidoc = NonbreakablespaceNode(
        BeautifulSoup(xml, "xml").nonbreakablespace, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == "{nbsp}"
