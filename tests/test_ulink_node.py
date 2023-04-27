from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import UlinkNode


def test_ulink_node_renders_as_an_em_dash(tmp_path):
    xml = """<ulink url="https://rptl.io/pico-c-sdk">Raspberry Pi <bold>Pico</bold> C/C++ SDK</ulink>"""

    asciidoc = UlinkNode(BeautifulSoup(xml, "xml").ulink, xmldir=tmp_path).to_asciidoc()

    assert asciidoc == "https://rptl.io/pico-c-sdk[Raspberry Pi *Pico* C/C++ SDK]"
