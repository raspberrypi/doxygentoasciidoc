from textwrap import dedent
from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import SimplesectNode, Node


def test_simplesect_with_return_kind(tmp_path):
    xml = """<simplesect kind="return"><para>Clock frequency in <emphasis>Hz</emphasis> </para></simplesect>"""

    asciidoc = SimplesectNode(
        BeautifulSoup(xml, "xml").simplesect, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        --
        *Returns*

        Clock frequency in _Hz_
        --"""
    )


def test_simplesect_with_note_kind(tmp_path):
    xml = """<simplesect kind="note"><para>This does <emphasis>not</emphasis> work</para></simplesect>"""

    asciidoc = SimplesectNode(
        BeautifulSoup(xml, "xml").simplesect, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        [NOTE]
        ====
        This does _not_ work
        ===="""
    )


def test_two_sibling_simplesects_with_note_kind(tmp_path):
    xml = """<para><simplesect kind="note"><para>This does <emphasis>not</emphasis> work</para></simplesect>
    <simplesect kind="note"><para>But this does</para></simplesect></para>"""

    asciidoc = Node(BeautifulSoup(xml, "xml").para, xmldir=tmp_path).to_asciidoc()

    assert asciidoc == dedent(
        """\
        [NOTE]
        ====
        This does _not_ work

        But this does
        ===="""
    )


def test_two_sibling_simplesects_with_see_kind(tmp_path):
    xml = """\
    <para><simplesect kind="see"><para><ref refid="foo" kindref="member">foo()</ref></para>
    </simplesect>
    <simplesect kind="see"><para><ref refid="bar" kindref="member">bar()</ref></para>
    </simplesect>
    </para>"""

    asciidoc = Node(BeautifulSoup(xml, "xml").para, xmldir=tmp_path).to_asciidoc()

    assert asciidoc == dedent(
        """\
        --
        *See also*

        <<foo,foo()>>

        <<bar,bar()>>
        --"""
    )
