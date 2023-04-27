from textwrap import dedent
from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import OrderedlistNode


def test_to_asciidoc(tmp_path):
    xml = """
    <orderedlist>
    <listitem><para>Item the <emphasis>first</emphasis></para>
    </listitem><listitem><para>Item the <bold>second</bold></para>
    </listitem></orderedlist>"""

    asciidoc = OrderedlistNode(
        BeautifulSoup(xml, "xml").orderedlist, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        . {empty}
        +
        --
        Item the _first_
        --

        . {empty}
        +
        --
        Item the *second*
        --"""
    )


def test_to_asciidoc_with_nested_list(tmp_path):
    xml = """
    <orderedlist>
    <listitem><para>5 input mux:<orderedlist>
    <listitem><para>4 inputs that are available</para>
    </listitem></orderedlist>
    </para>
    </listitem></orderedlist>"""

    asciidoc = OrderedlistNode(
        BeautifulSoup(xml, "xml").orderedlist, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        . {empty}
        +
        --
        5 input mux:

        .. {empty}
        +
        4 inputs that are available
        --"""
    )
