from textwrap import dedent
from bs4 import BeautifulSoup, NavigableString
from doxygentoasciidoc.nodes import Node, BoldNode, EmphasisNode


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

    assert node.previous_node().name == "emphasis"


def test_next_node_returns_the_first_non_text_node(tmp_path):
    xml = """\
    <para>Foo <title>Bar</title> Baz <emphasis>Qux</emphasis> Quux <bold>Corge</bold></para>
    """
    node = Node(BeautifulSoup(xml, "xml").para.title, xmldir=tmp_path)

    assert node.next_node().name == "emphasis"


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


def test_text_returns_the_stripped_text_of_the_node():
    xml = "<para> Hello world </para>"
    node = Node(BeautifulSoup(xml, "xml").para)

    assert node.text() == "Hello world"


def test_text_returns_the_stripped_text_of_a_given_child():
    xml = "<para>Hello <bold> world </bold></para>"
    node = Node(BeautifulSoup(xml, "xml").para)

    assert node.text("bold") == "world"


def test_text_returns_nothing_if_the_child_does_not_exist():
    xml = "<para>Hello <bold> world </bold></para>"
    node = Node(BeautifulSoup(xml, "xml").para)

    assert node.text("emphasis") is None


def test_child_returns_the_first_given_child():
    xml = "<para>Hello <bold> world </bold></para>"
    node = Node(BeautifulSoup(xml, "xml").para)

    assert isinstance(node.child("bold"), BoldNode)


def test_child_returns_nothing_if_the_given_child_does_not_exist():
    xml = "<para>Hello <bold> world </bold></para>"
    node = Node(BeautifulSoup(xml, "xml").para)

    assert node.child("emphasis") is None


def test_children_returns_all_child_nodes_wrapped_in_node_classes():
    xml = "<para>Hello <bold><emphasis>world</emphasis></bold></para>"
    node = Node(BeautifulSoup(xml, "xml").para)
    children = list(node.children())

    assert isinstance(children[0], Node)
    assert isinstance(children[1], BoldNode)
    assert isinstance(children[1], Node)


def test_children_only_returns_children_with_the_given_selector():
    xml = "<para>Hello <bold> world </bold></para>"
    node = Node(BeautifulSoup(xml, "xml").para)
    children = list(node.children("bold"))

    assert len(children) == 1
    assert isinstance(children[0], BoldNode)


def test_children_passes_extra_kwargs_to_beautiful_soup():
    xml = """<para>Hello <bold>world</bold> <bold kind="personal">you</bold></para>"""
    node = Node(BeautifulSoup(xml, "xml").para)
    children = list(node.children("bold", kind="personal"))

    assert len(children) == 1
    assert isinstance(children[0], BoldNode)


def test_descendants_returns_matching_descendants_with_the_given_selector():
    xml = "<para>Hello <bold><emphasis>world</emphasis></bold></para>"
    node = Node(BeautifulSoup(xml, "xml").para)
    descendants = list(node.descendants("emphasis"))

    assert len(descendants) == 1
    assert isinstance(descendants[0], EmphasisNode)


def test_descendants_passes_extra_kwargs_to_beautiful_soup():
    xml = """<para>Hello <bold><emphasis>world</emphasis> <emphasis kind="personal">you</emphasis></bold></para>"""
    node = Node(BeautifulSoup(xml, "xml").para)
    descendants = list(node.descendants("emphasis", kind="personal"))

    assert len(descendants) == 1
    assert isinstance(descendants[0], EmphasisNode)


def test_id_returns_sanitized_id():
    xml = """<para id="group__hardware__base">Hello</para>"""
    node = Node(BeautifulSoup(xml, "xml").para)

    assert node.id == "group_hardware_base"


def test_attributes_are_preserved():
    xml = """<memberdef const="no" explicit="no" id="group__hardware__gpio_1ga5d7dbadb2233e2e6627e9101411beb27" inline="no" kind="function" prot="public" role="contextspecific" static="no" tag="TAG" type="TYPE" virt="non-virtual">
    <type>void</type>
    <definition>void foo</definition>
    <argsstring>()</argsstring>
    <name>foo</name>
    <briefdescription>
    <para>A function.</para>
    </briefdescription>
    <detaileddescription>
    </detaileddescription>
    <inbodydescription>
    </inbodydescription>
    <location column="6" declcolumn="6" declfile="include/hardware/gpio.h" declline="232" file="include/hardware/gpio.h" line="232"/>
    </memberdef>"""
    node = Node(BeautifulSoup(xml, "xml").memberdef)

    assert (
        node.attributes()
        == "#group_hardware_gpio_1ga5d7dbadb2233e2e6627e9101411beb27,role=contextspecific,tag=TAG,type=TYPE"
    )


def test_attributes_are_preserved_except_skipped():
    xml = """<memberdef const="no" explicit="no" id="group__hardware__gpio_1ga5d7dbadb2233e2e6627e9101411beb27" inline="no" kind="function" prot="public" role="contextspecific" static="no" tag="TAG" type="TYPE" virt="non-virtual">
    <type>void</type>
    <definition>void foo</definition>
    <argsstring>()</argsstring>
    <name>foo</name>
    <briefdescription>
    <para>A function.</para>
    </briefdescription>
    <detaileddescription>
    </detaileddescription>
    <inbodydescription>
    </inbodydescription>
    <location column="6" declcolumn="6" declfile="include/hardware/gpio.h" declline="232" file="include/hardware/gpio.h" line="232"/>
    </memberdef>"""
    node = Node(BeautifulSoup(xml, "xml").memberdef)

    assert node.attributes(skip=["id"]) == "role=contextspecific,tag=TAG,type=TYPE"


def test_nodes_are_subscriptable():
    xml = """<para kind="group" id="not__sanitized">Hello</para>"""
    node = Node(BeautifulSoup(xml, "xml").para)

    assert node["kind"] == "group"
    assert node["id"] == "not__sanitized"


def test_indexpage():
    xml = """<?xml version="1.0" encoding="utf-8"?>
    <doxygen version="1.10.0" xml:lang="en-US" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="compound.xsd">
    <compounddef id="indexpage" kind="page">
    <compoundname>index</compoundname>
    <title>Page Title</title>
    <briefdescription>
    </briefdescription>
    <detaileddescription>
    <para><anchor id="my_anchor"/> First paragraph.</para>
    <sect1 id="a_section">
    <title>Section Head</title><para>Second paragraph.</para>
    </sect1>
    </detaileddescription>
    </compounddef>
    </doxygen>"""

    asciidoc = Node(BeautifulSoup(xml, "xml").doxygen).to_asciidoc()

    assert asciidoc == dedent(
        """\
        [#indexpage]
        == Page Title

         [[my_anchor]] First paragraph.

        [#a_section]
        === Section Head

        Second paragraph."""
    )
