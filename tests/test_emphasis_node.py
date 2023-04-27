from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import EmphasisNode


def test_emphasis_node_renders_nested_nodes_as_italic(tmp_path):
    xml = """<emphasis>Hello <bold>world</bold></emphasis>"""

    asciidoc = EmphasisNode(
        BeautifulSoup(xml, "xml").emphasis, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == "_Hello *world*_"
