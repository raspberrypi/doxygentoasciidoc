from textwrap import dedent
from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import DetaileddescriptionNode


def test_to_asciidoc_includes_title(tmp_path):
    xml = """\
    <detaileddescription>
    <para>The main <computeroutput><bold>pico_lwip</bold> library</computeroutput></para>
    </detaileddescription>"""

    asciidoc = DetaileddescriptionNode(
        BeautifulSoup(xml, "xml").detaileddescription, xmldir=tmp_path
    ).to_asciidoc(depth=2)

    assert asciidoc == dedent(
        """\
        === Detailed Description

        The main `*pico_lwip* library`"""
    )


def test_to_asciidoc_respects_depth(tmp_path):
    xml = """\
    <detaileddescription>
    <para>The main <computeroutput><bold>pico_lwip</bold> library</computeroutput></para>
    </detaileddescription>"""

    asciidoc = DetaileddescriptionNode(
        BeautifulSoup(xml, "xml").detaileddescription, xmldir=tmp_path
    ).to_asciidoc(depth=5)

    assert asciidoc == dedent(
        """\
        ====== Detailed Description

        The main `*pico_lwip* library`"""
    )


def test_to_asciidoc_writes_nothing_if_the_description_is_empty(tmp_path):
    xml = """\
    <detaileddescription>
    </detaileddescription>"""

    asciidoc = DetaileddescriptionNode(
        BeautifulSoup(xml, "xml").detaileddescription, xmldir=tmp_path
    ).to_asciidoc(depth=2)

    assert asciidoc == ""


def test_to_asciidoc_does_not_include_title_if_documentation_is_true(tmp_path):
    xml = """\
    <detaileddescription>
    <para>The main <computeroutput><bold>pico_lwip</bold> library</computeroutput></para>
    </detaileddescription>"""

    asciidoc = DetaileddescriptionNode(
        BeautifulSoup(xml, "xml").detaileddescription, xmldir=tmp_path
    ).to_asciidoc(depth=2, documentation=True)

    assert asciidoc == "The main `*pico_lwip* library`"


def test_to_asciidoc_handling_whitespace(tmp_path):
    xml = """\
    <detaileddescription>
<para>The I2C identifiers for use in I2C functions.</para>
<para>e.g. i2c_init(i2c0, 48000) </para>
    </detaileddescription>
    """

    asciidoc = DetaileddescriptionNode(
        BeautifulSoup(xml, "xml").detaileddescription, xmldir=tmp_path
    ).to_asciidoc(depth=2, documentation=True)

    assert asciidoc == dedent(
        """\
        The I2C identifiers for use in I2C functions.

        e.g. i2c_init(i2c0, 48000)"""
    )
