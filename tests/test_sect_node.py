from textwrap import dedent
from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import SectNode


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
        == Interrupt Numbers

        Interrupts _are_ numbered as follows."""
    )


def test_sect_node_with_attributes(tmp_path):
    xml = """\
    <sect1 id="foo" role="contextspecific" tag="PICO_2040" type="PICO_2040">
    <title>Interrupt Numbers</title>
    <para>Interrupts <emphasis>are</emphasis> numbered as follows.</para>
    </sect1>"""

    asciidoc = SectNode(BeautifulSoup(xml, "xml").sect1, xmldir=tmp_path).to_asciidoc()

    assert asciidoc == dedent(
        """\
        [#foo,role=contextspecific,tag=PICO_2040,type=PICO_2040]
        == Interrupt Numbers

        Interrupts _are_ numbered as follows."""
    )
