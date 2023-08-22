from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import AnchorNode


def test_to_asciidoc(tmp_path):
    xml = """<anchor id="group__cyw43__driver_1CYW43_VERSION_"/>"""

    asciidoc = AnchorNode(
        BeautifulSoup(xml, "xml").anchor, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == "[[group_cyw43_driver_1CYW43_VERSION_]]"
