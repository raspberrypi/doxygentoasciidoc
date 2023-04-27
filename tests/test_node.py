from textwrap import dedent
from bs4 import BeautifulSoup, NavigableString
from doxygentoasciidoc.nodes import Node


def test_it_renders_escaped_text(tmp_path):
    asciidoc = Node(NavigableString("Hello * there"), xmldir=tmp_path).to_asciidoc()

    assert asciidoc == "Hello ++*++ there"


def test_it_renders_unescaped_text_when_programlisting_is_true(tmp_path):
    asciidoc = Node(NavigableString("Hello * there"), xmldir=tmp_path).to_asciidoc(
        programlisting=True
    )

    assert asciidoc == "Hello * there"


def test_it_strips_leading_whitespace_if_preceded_by_a_verbatim_block(tmp_path):
    xml = """\
    <para>Hello <verbatim>world</verbatim> there</para>
    """

    asciidoc = Node(
        BeautifulSoup(xml, "xml").para.verbatim.next_sibling, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == "there"


def test_it_strips_leading_whitespace_if_preceded_by_a_simplesect(tmp_path):
    xml = """\
    <para>Hello <simplesect kind="note">world</simplesect> there</para>
    """

    asciidoc = Node(
        BeautifulSoup(xml, "xml").para.simplesect.next_sibling, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == "there"


def test_it_strips_leading_whitespace_if_preceded_by_an_itemizedlist(tmp_path):
    xml = """\
    <para>Hello <itemizedlist><listitem>world</listitem></itemizedlist> there</para>
    """

    asciidoc = Node(
        BeautifulSoup(xml, "xml").para.itemizedlist.next_sibling, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == "there"


def test_it_strips_leading_whitespace_if_preceded_by_an_orderedlist(tmp_path):
    xml = """\
    <para>Hello <orderedlist><listitem>world</listitem></orderedlist> there</para>
    """

    asciidoc = Node(
        BeautifulSoup(xml, "xml").para.orderedlist.next_sibling, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == "there"


def test_previous_node_returns_the_first_non_text_node(tmp_path):
    xml = """\
    <para>Foo <title>Bar</title> Baz <emphasis>Qux</emphasis> Quux <bold>Corge</bold></para>
    """
    node = Node(BeautifulSoup(xml, "xml").para.bold, xmldir=tmp_path)

    assert node.previous_node.name == "emphasis"


def test_next_node_returns_the_first_non_text_node(tmp_path):
    xml = """\
    <para>Foo <title>Bar</title> Baz <emphasis>Qux</emphasis> Quux <bold>Corge</bold></para>
    """
    node = Node(BeautifulSoup(xml, "xml").para.title, xmldir=tmp_path)

    assert node.next_node.name == "emphasis"


def test_empty_node_outputs_nothing(tmp_path):
    xml = """\
    <detaileddescription>
    </detaileddescription>
    """

    asciidoc = Node(
        BeautifulSoup(xml, "xml").detaileddescription, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == ""


def test_whitespace_is_processed_like_html(tmp_path):
    xml = """\
    <detaileddescription>   Hello 
    <bold> world</bold>  </detaileddescription>
    """

    asciidoc = Node(
        BeautifulSoup(xml, "xml").detaileddescription, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == "Hello *world*"


def test_whitespace_with_multiple_blocks(tmp_path):
    xml = """\
<detaileddescription>
  <para>  Hello  </para>

   <para>  World!  </para>  
</detaileddescription>
    """

    asciidoc = Node(
        BeautifulSoup(xml, "xml").detaileddescription, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == "Hello\n\nWorld!"


def test_mixed_blocks_and_inline_elements(tmp_path):
    xml = """<para><simplesect kind="note"><para>This is important</para></simplesect> Hello <bold>world</bold></para>"""
    asciidoc = Node(BeautifulSoup(xml, "xml").para, xmldir=tmp_path).to_asciidoc()

    assert asciidoc == dedent(
        """\
        [NOTE]
        ====
        This is important
        ====

        Hello *world*"""
    )


def test_mixed_list_and_text(tmp_path):
    xml = """\
<para><itemizedlist>
<listitem><para>Updates whether the specified events for the specified GPIO causes an interrupt on the calling core based on the enable flag.</para>
</listitem>
</itemizedlist>
<itemizedlist>
<listitem><para>Sets the callback handler for the calling core to callback (or clears the handler if the callback is NULL).</para>
</listitem>
</itemizedlist>
<itemizedlist>
<listitem><para>Enables GPIO IRQs on the current core if enabled is true.</para>
</listitem>
</itemizedlist>
This method is commonly used to perform a one time setup, and following that any additional IRQs/events are enabled via <ref refid="group__hardware__gpio_1ga08b1f920beba446c4d4385de999cf945" kindref="member">gpio_set_irq_enabled</ref>. All GPIOs/events added in this way on the same core share the same callback; for multiple independent handlers for different GPIOs you should use <ref refid="group__hardware__gpio_1ga2e78fcd487a3a2e173322c6502fe9419" kindref="member">gpio_add_raw_irq_handler</ref> and related functions.</para>"""
    asciidoc = Node(BeautifulSoup(xml, "xml").para, xmldir=tmp_path).to_asciidoc()

    assert asciidoc == dedent(
        """\
        * {empty}
        +
        --
        Updates whether the specified events for the specified GPIO causes an interrupt on the calling core based on the enable flag.
        --

        * {empty}
        +
        --
        Sets the callback handler for the calling core to callback (or clears the handler if the callback is NULL).
        --

        * {empty}
        +
        --
        Enables GPIO IRQs on the current core if enabled is true.
        --

        This method is commonly used to perform a one time setup, and following that any additional IRQs/events are enabled via <<group_hardware_gpio_1ga08b1f920beba446c4d4385de999cf945,gpio_set_irq_enabled>>. All GPIOs/events added in this way on the same core share the same callback; for multiple independent handlers for different GPIOs you should use <<group_hardware_gpio_1ga2e78fcd487a3a2e173322c6502fe9419,gpio_add_raw_irq_handler>> and related functions."""
    )


def test_soup_returns_beautiful_soup(tmp_path):
    xml = "<para>Hello <bold>world</bold></para>"
    soup = BeautifulSoup(xml, "xml")
    node = Node(soup.bold, xmldir=tmp_path)

    assert node.soup() == soup
