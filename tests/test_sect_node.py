from textwrap import dedent
from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import Node, SectNode


def test_sect_node(tmp_path):
    xml = """\
    <sect1 id="foo">
    <title>Interrupt Numbers</title>
    <para>Interrupts <emphasis>are</emphasis> numbered as follows.</para>
    </sect1>"""

    asciidoc = SectNode(BeautifulSoup(xml, "xml").sect1, xmldir=tmp_path).to_asciidoc()

    assert asciidoc == dedent(
        """\
        [#foo]
        .Interrupt Numbers

        Interrupts _are_ numbered as follows."""
    )


def test_compounddef_kind_page_is_processed_as_sect(tmp_path):
    xml = """\
    <compounddef id="examples_page" kind="page">
    <compoundname>examples_page</compoundname>
    <title>Examples Index</title>
    <briefdescription>
    </briefdescription>
    <detaileddescription>
    <para><anchor id="my_anchor"/> First paragraph.</para>
    </detaileddescription>
    </compounddef>"""

    asciidoc = Node(BeautifulSoup(xml, "xml").compounddef, xmldir=tmp_path).to_asciidoc()

    assert asciidoc == dedent(
        """\
        == Examples Index

         [[my_anchor]] First paragraph."""
    )
