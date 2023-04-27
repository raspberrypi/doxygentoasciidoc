from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import ComputeroutputNode


def test_computeroutput_node_renders_nested_nodes_in_monospace(tmp_path):
    xml = """<computeroutput>Hello <emphasis>world</emphasis></computeroutput>"""

    asciidoc = ComputeroutputNode(
        BeautifulSoup(xml, "xml").computeroutput, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == "`Hello _world_`"
