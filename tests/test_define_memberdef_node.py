from textwrap import dedent
from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import DefineMemberdefNode


def test_to_asciidoc(tmp_path):
    xml = """\
      <memberdef kind="define" id="group__hardware__pio_1ga916d05e71da7f2173cd22b46bbfa0a11" prot="public" static="no">
        <name>pio0</name>
        <initializer>pio0_hw</initializer>
        <briefdescription>
        </briefdescription>
        <detaileddescription>
<para>Identifier for the first (PIO 0) hardware PIO instance (for use in PIO functions).</para>
<para>e.g. pio_gpio_init(pio0, 5) </para>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="hardware_pio/include/hardware/pio.h" line="77" column="9" bodyfile="hardware_pio/include/hardware/pio.h" bodystart="77" bodyend="-1"/>
      </memberdef>
    """

    asciidoc = DefineMemberdefNode(
        BeautifulSoup(xml, "xml").memberdef, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        [#group_hardware_pio_1ga916d05e71da7f2173cd22b46bbfa0a11]
        ====== pio0

        `#define pio0 pio0_hw`

        Identifier for the first (PIO 0) hardware PIO instance (for use in PIO functions).

        e.g. pio_gpio_init(pio0, 5)"""
    )


def test_to_asciidoc_with_no_initializer(tmp_path):
    xml = """\
      <memberdef kind="define" id="group__hardware__pio_1ga923a261ba19804c404900228e99c9522" prot="public" static="no">
        <name>pio1</name>
        <briefdescription>
        </briefdescription>
        <detaileddescription>
<para>Identifier for the second (PIO 1) hardware PIO instance (for use in PIO functions).</para>
<para>e.g. pio_gpio_init(pio1, 5) </para>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="hardware_pio/include/hardware/pio.h" line="85" column="9" bodyfile="hardware_pio/include/hardware/pio.h" bodystart="85" bodyend="-1"/>
      </memberdef>
    """

    asciidoc = DefineMemberdefNode(
        BeautifulSoup(xml, "xml").memberdef, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        [#group_hardware_pio_1ga923a261ba19804c404900228e99c9522]
        ====== pio1

        `#define pio1`

        Identifier for the second (PIO 1) hardware PIO instance (for use in PIO functions).

        e.g. pio_gpio_init(pio1, 5)"""
    )
