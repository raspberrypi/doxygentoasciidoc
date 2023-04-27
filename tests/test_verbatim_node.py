from textwrap import dedent
from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import VerbatimNode


def test_verbatim_node_renders_a_code_block(tmp_path):
    xml = """\
    <verbatim>*some_memory_location = var_a;
__compiler_memory_barrier();
</verbatim>"""

    asciidoc = VerbatimNode(
        BeautifulSoup(xml, "xml").verbatim, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        [source,c]
        ----
        *some_memory_location = var_a;
        __compiler_memory_barrier();
        ----"""
    )
