from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import CodelineNode


def test_codeline_node_ends_with_a_newline(tmp_path):
    xml = """<codeline lineno="1"><highlight class="normal"><sp/><sp/>assert(fbdiv<sp/>&gt;=<sp/>16)</highlight></codeline>"""

    asciidoc = CodelineNode(
        BeautifulSoup(xml, "xml").codeline, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == "  assert(fbdiv >= 16)"
