from textwrap import dedent
from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import ListitemNode


def test_to_asciidoc(tmp_path):
    xml = """
    <listitem><para>Item the first</para>
    </listitem>"""

    asciidoc = ListitemNode(
        BeautifulSoup(xml, "xml").listitem, xmldir=tmp_path
    ).to_asciidoc(unordereddepth=1)

    assert asciidoc == dedent(
        """\
        * {empty}
        +
        --
        Item the first
        --"""
    )


def test_to_asciidoc_when_nested(tmp_path):
    xml = """
    <listitem><para>Item the first</para>
    </listitem>"""

    asciidoc = ListitemNode(
        BeautifulSoup(xml, "xml").listitem, xmldir=tmp_path
    ).to_asciidoc(unordereddepth=2)

    assert asciidoc == dedent(
        """\
        ** {empty}
        +
        Item the first"""
    )


def test_block_separator_at_top_level(tmp_path):
    xml = """
    <listitem><para>Item the first</para>
    </listitem>"""

    separator = ListitemNode(
        BeautifulSoup(xml, "xml").listitem, xmldir=tmp_path
    ).block_separator(unordereddepth=1)

    assert separator == "\n\n"


def test_block_separator_when_nested(tmp_path):
    xml = """
    <listitem><para>Item the first</para>
    </listitem>"""

    separator = ListitemNode(
        BeautifulSoup(xml, "xml").listitem, xmldir=tmp_path
    ).block_separator(unordereddepth=2)

    assert separator == "\n+\n"
