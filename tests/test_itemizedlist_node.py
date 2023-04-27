from textwrap import dedent
from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import ItemizedlistNode


def test_to_asciidoc(tmp_path):
    xml = """
    <itemizedlist>
    <listitem><para>Item the first</para>
    </listitem></itemizedlist>"""

    asciidoc = ItemizedlistNode(
        BeautifulSoup(xml, "xml").itemizedlist, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        * {empty}
        +
        --
        Item the first
        --"""
    )


def test_to_asciidoc_with_nested_list(tmp_path):
    xml = """
    <itemizedlist>
    <listitem><para>5 input mux:<itemizedlist>
    <listitem><para>4 inputs that are available</para>
    </listitem></itemizedlist>
    </para>
    </listitem></itemizedlist>"""

    asciidoc = ItemizedlistNode(
        BeautifulSoup(xml, "xml").itemizedlist, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        * {empty}
        +
        --
        5 input mux:

        ** {empty}
        +
        4 inputs that are available
        --"""
    )


def test_to_asciidoc_with_mixed_nested_list(tmp_path):
    xml = """
    <itemizedlist>
    <listitem><para>5 input mux:<orderedlist>
    <listitem><para>4 inputs that are available</para>
    </listitem></orderedlist>
    </para>
    </listitem></itemizedlist>"""

    asciidoc = ItemizedlistNode(
        BeautifulSoup(xml, "xml").itemizedlist, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        * {empty}
        +
        --
        5 input mux:

        . {empty}
        +
        4 inputs that are available
        --"""
    )


def test_to_asciidoc_with_multiple_paras_in_a_list(tmp_path):
    xml = """\
<itemizedlist>
<listitem><para>List:
</para>
<para>This paragraph</para>
</listitem></itemizedlist>
    """

    asciidoc = ItemizedlistNode(
        BeautifulSoup(xml, "xml").itemizedlist, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        * {empty}
        +
        --
        List:

        This paragraph
        --"""
    )


def test_to_asciidoc_with_multiple_paras_in_a_nested_list(tmp_path):
    xml = """\
<itemizedlist>
    <listitem>
        <para>
            1
            <itemizedlist>
                <listitem>
                    <para>1.1</para>
                    <para>1.2</para>
                </listitem>
            </itemizedlist>
        </para>
    </listitem>
    <listitem>
        <para>2</para>
    </listtem>
</itemizedlist>
    """

    asciidoc = ItemizedlistNode(
        BeautifulSoup(xml, "xml").itemizedlist, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        * {empty}
        +
        --
        1

        ** {empty}
        +
        1.1
        +
        1.2
        --

        * {empty}
        +
        --
        2
        --"""
    )


def test_to_asciidoc_with_para_after_nested_list(tmp_path):
    xml = """\
<itemizedlist>
    <listitem>
        <para>
            Before
            <itemizedlist>
                <listitem>
                    <para>1</para>
                </listitem>
            </itemizedlist>
            After
        </para>
    </listitem>
</itemizedlist>
    """

    asciidoc = ItemizedlistNode(
        BeautifulSoup(xml, "xml").itemizedlist, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        * {empty}
        +
        --
        Before

        ** {empty}
        +
        1

        After
        --"""
    )
