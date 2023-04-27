from textwrap import dedent
from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import TableNode


def test_table_node_renders_tables(tmp_path):
    xml = """
    <table><row>
    <entry thead="yes"><para>IRQ   </para>
    </entry><entry thead="yes"><para>Interrupt Source    </para>
    </entry></row>
    <row>
    <entry thead="no"><para>0   </para>
    </entry><entry thead="no"><para>TIMER_IRQ_0    </para>
    </entry></row>
    </table>
    """

    asciidoc = TableNode(BeautifulSoup(xml, "xml").table, xmldir=tmp_path).to_asciidoc()

    assert asciidoc == dedent(
        """\
        |===
        |IRQ |Interrupt Source

        |0
        |TIMER_IRQ_0
        |==="""
    )
