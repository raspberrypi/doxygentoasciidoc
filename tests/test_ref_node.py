from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import RefNode


def test_ref_node_renders_a_link(tmp_path):
    xml = """<ref refid="group__hardware__irq_1interrupt_nums" kindref="member">Interrupt Numbers</ref>"""

    asciidoc = RefNode(BeautifulSoup(xml, "xml").ref, xmldir=tmp_path).to_asciidoc()

    assert asciidoc == "<<group_hardware_irq_1interrupt_nums,Interrupt Numbers>>"


def test_ref_node_only_renders_as_text_when_inside_a_programlisting(tmp_path):
    xml = """<ref refid="group__hardware__irq_1interrupt_nums" kindref="member">Interrupt Numbers</ref>"""

    asciidoc = RefNode(BeautifulSoup(xml, "xml").ref, xmldir=tmp_path).to_asciidoc(
        programlisting=True
    )

    assert asciidoc == "Interrupt Numbers"
