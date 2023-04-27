from textwrap import dedent
from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import ProgramlistingNode


def test_programlisting_node_renders_as_a_verbatim_code_block(tmp_path):
    xml = """\
    <programlisting><codeline lineno="1"><highlight class="normal">2 * 2 = 4</highlight></codeline>
<codeline><highlight class="normal"></highlight></codeline>
<codeline lineno="2"><highlight class="normal">2 + 2 = 5</highlight></codeline></programlisting>"""

    asciidoc = ProgramlistingNode(
        BeautifulSoup(xml, "xml").programlisting, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        [source,c,linenums]
        ----
        2 * 2 = 4

        2 + 2 = 5
        ----"""
    )


def test_programlisting_node_includes_filename_as_comment_if_present(tmp_path):
    xml = """
    <programlisting filename="hello.c"><codeline lineno="1"><highlight class="normal">print("Hello world")</highlight></codeline>
    </programlisting>"""

    asciidoc = ProgramlistingNode(
        BeautifulSoup(xml, "xml").programlisting, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        // hello.c
        [source,c,linenums]
        ----
        print("Hello world")
        ----"""
    )
