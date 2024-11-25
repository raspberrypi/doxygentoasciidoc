from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import Node


def test_to_asciidoc(tmp_path):
    xml = """
    <para>Hello<linebreak/>
    </para>
    """

    asciidoc = Node(BeautifulSoup(xml, "xml").para, xmldir=tmp_path).to_asciidoc()

    assert asciidoc == "Hello +\n"
