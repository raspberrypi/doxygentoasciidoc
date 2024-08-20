from textwrap import dedent
from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import VariableMemberdefNode


def test_to_asciidoc(tmp_path):
    xml = """\
      <memberdef kind="variable" id="group__hardware__i2c_1ga56c7844696c095a3ad088100df011fd2" prot="public" static="no" mutable="no">
        <type><ref refid="structi2c__inst" kindref="compound">i2c_inst_t</ref></type>
        <definition>i2c_inst_t i2c0_inst</definition>
        <argsstring></argsstring>
        <name>i2c0_inst</name>
        <briefdescription>
        </briefdescription>
        <detaileddescription>
<para>The I2C identifiers for use in I2C functions.</para>
<para>e.g. i2c_init(i2c0, 48000) </para>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="hardware_i2c/include/hardware/i2c.h" line="65" column="19" bodyfile="hardware_i2c/i2c.c" bodystart="15" bodyend="-1" declfile="hardware_i2c/include/hardware/i2c.h" declline="65" declcolumn="19"/>
      </memberdef>
    """

    asciidoc = VariableMemberdefNode(
        BeautifulSoup(xml, "xml").memberdef, xmldir=tmp_path
    ).to_asciidoc(depth=5)

    assert asciidoc == dedent(
        """\
        [#group_hardware_i2c_1ga56c7844696c095a3ad088100df011fd2]
        ====== i2c0_inst

        [.memname]`i2c_inst_t i2c0_inst`

        The I2C identifiers for use in I2C functions.

        e.g. i2c_init(i2c0, 48000)"""
    )


def test_to_asciidoc_with_no_name(tmp_path):
    xml = """\
      <memberdef kind="variable" id="structirq__handler__chain__slot_1a75f171191a7a92cb2eb1b4cf1569690a" prot="public" static="no" mutable="no">
        <type>union <ref refid="structirq__handler__chain__slot" kindref="compound">irq_handler_chain_slot</ref></type>
        <definition>union irq_handler_chain_slot irq_handler_chain_slot</definition>
        <argsstring></argsstring>
        <name></name>
        <qualifiedname>irq_handler_chain_slot</qualifiedname>
        <briefdescription>
        </briefdescription>
        <detaileddescription>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="hardware_irq/irq.c" line="99" column="5"/>
      </memberdef>
    """

    asciidoc = VariableMemberdefNode(
        BeautifulSoup(xml, "xml").memberdef, xmldir=tmp_path
    ).to_asciidoc(depth=5)

    assert asciidoc == dedent(
        """\
        [#structirq_handler_chain_slot_1a75f171191a7a92cb2eb1b4cf1569690a]
        ====== irq_handler_chain_slot

        [.memname]`union irq_handler_chain_slot irq_handler_chain_slot`"""
    )


def test_to_asciidoc_with_initializer(tmp_path):
    xml = """\
      <memberdef kind="variable" id="pico__flash_2flash_8c_1a61d721f8bcbcf9ae65e69369b870ec4d" prot="public" static="yes" mutable="no">
        <type><ref refid="structflash__safety__helper__t" kindref="compound">flash_safety_helper_t</ref></type>
        <definition>flash_safety_helper_t default_flash_safety_helper</definition>
        <argsstring></argsstring>
        <name>default_flash_safety_helper</name>
        <initializer>= {
        .core_init_deinit = default_core_init_deinit,
        .enter_safe_zone_timeout_ms = default_enter_safe_zone_timeout_ms,
        .exit_safe_zone_timeout_ms = default_exit_safe_zone_timeout_ms
}</initializer>
        <briefdescription>
        </briefdescription>
        <detaileddescription>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="pico_flash/flash.c" line="43" column="30" bodyfile="pico_flash/flash.c" bodystart="43" bodyend="-1"/>
      </memberdef>
    """

    asciidoc = VariableMemberdefNode(
        BeautifulSoup(xml, "xml").memberdef, xmldir=tmp_path
    ).to_asciidoc(depth=5)

    assert asciidoc == dedent(
        """\
        [#pico_flash_2flash_8c_1a61d721f8bcbcf9ae65e69369b870ec4d]
        ====== default_flash_safety_helper

        [source,c]
        ----
        flash_safety_helper_t default_flash_safety_helper = {
                .core_init_deinit = default_core_init_deinit,
                .enter_safe_zone_timeout_ms = default_enter_safe_zone_timeout_ms,
                .exit_safe_zone_timeout_ms = default_exit_safe_zone_timeout_ms
        }
        ----"""
    )
