# pylint: disable=line-too-long

from textwrap import dedent
from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import VariableSectiondefNode


def test_to_asciidoc():
    xml = """\
      <sectiondef kind="var">
      <memberdef kind="variable" id="float__init__rom_8c_1aea98df4cf9adff2a025dc4a09c814986" prot="public" static="no" mutable="no">
        <type>uint32_t</type>
        <definition>uint32_t sf_table[SF_TABLE_V2_SIZE/2]</definition>
        <argsstring>[SF_TABLE_V2_SIZE/2]</argsstring>
        <name>sf_table</name>
        <briefdescription>
        </briefdescription>
        <detaileddescription>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="pico_float/float_init_rom.c" line="13" column="10" bodyfile="pico_float/float_init_rom.c" bodystart="13" bodyend="-1"/>
      </memberdef>
      </sectiondef>
    """

    asciidoc = VariableSectiondefNode(BeautifulSoup(xml, "xml").sectiondef).to_asciidoc(
        depth=4
    )

    assert asciidoc == dedent(
        """\
        ===== Variables

        `uint32_t <<float_init_rom_8c_1aea98df4cf9adff2a025dc4a09c814986,sf_table>>[SF_TABLE_V2_SIZE/2]`:: {empty}"""
    )


def test_to_details_asciidoc():
    xml = """\
      <sectiondef kind="var">
      <memberdef kind="variable" id="float__init__rom_8c_1aea98df4cf9adff2a025dc4a09c814986" prot="public" static="no" mutable="no">
        <type>uint32_t</type>
        <definition>uint32_t sf_table[SF_TABLE_V2_SIZE/2]</definition>
        <argsstring>[SF_TABLE_V2_SIZE/2]</argsstring>
        <name>sf_table</name>
        <briefdescription>
        </briefdescription>
        <detaileddescription>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="pico_float/float_init_rom.c" line="13" column="10" bodyfile="pico_float/float_init_rom.c" bodystart="13" bodyend="-1"/>
      </memberdef>
      </sectiondef>
    """

    asciidoc = VariableSectiondefNode(
        BeautifulSoup(xml, "xml").sectiondef
    ).to_details_asciidoc(depth=4)

    assert asciidoc == dedent(
        """\
        ===== Variable Documentation

        [#float_init_rom_8c_1aea98df4cf9adff2a025dc4a09c814986]
        ====== sf_table

        [.memname]`uint32_t sf_table[SF_TABLE_V2_SIZE/2]`"""
    )


def test_bug():
    xml = """\
        <sectiondef kind="var">
          <memberdef kind="variable" id="group__cyw43__driver_1gafe7528793baa39a05a1c4ff55f5b5807" prot="public" static="no" extern="yes" mutable="no">
            <type><ref refid="struct__cyw43__t" kindref="compound">cyw43_t</ref></type>
            <definition>cyw43_t cyw43_state</definition>
            <argsstring></argsstring>
            <name>cyw43_state</name>
            <briefdescription>
            </briefdescription>
            <detaileddescription>
            </detaileddescription>
            <inbodydescription>
            </inbodydescription>
            <location file="cyw43.h" line="154" column="16" bodyfile="cyw43_ctrl.c" bodystart="68" bodyend="-1" declfile="cyw43.h" declline="154" declcolumn="16"/>
          </memberdef>
          <memberdef kind="variable" id="group__cyw43__driver_1ga65550517babd8db2d2a052f41de6ae33" prot="public" static="no" extern="yes" mutable="no">
            <type>void(*</type>
            <definition>void(* cyw43_poll) (void)</definition>
            <argsstring>)(void)</argsstring>
            <name>cyw43_poll</name>
            <briefdescription>
            </briefdescription>
            <detaileddescription>
            </detaileddescription>
            <inbodydescription>
            </inbodydescription>
            <location file="cyw43.h" line="155" column="8" bodyfile="cyw43_ctrl.c" bodystart="69" bodyend="-1" declfile="cyw43.h" declline="155" declcolumn="8"/>
          </memberdef>
          <memberdef kind="variable" id="group__cyw43__driver_1ga8345872c237308a5e4e984060f9f399f" prot="public" static="no" extern="yes" mutable="no">
            <type>uint32_t</type>
            <definition>uint32_t cyw43_sleep</definition>
            <argsstring></argsstring>
            <name>cyw43_sleep</name>
            <briefdescription>
            </briefdescription>
            <detaileddescription>
            </detaileddescription>
            <inbodydescription>
            </inbodydescription>
            <location file="cyw43.h" line="156" column="17" bodyfile="cyw43_ctrl.c" bodystart="70" bodyend="-1" declfile="cyw43.h" declline="156" declcolumn="17"/>
          </memberdef>
        </sectiondef>
      """

    asciidoc = VariableSectiondefNode(BeautifulSoup(xml, "xml").sectiondef).to_asciidoc(
        depth=4
    )

    assert asciidoc == dedent(
        """\
        ===== Variables

        `<<struct_cyw43_t,cyw43_t>> <<group_cyw43_driver_1gafe7528793baa39a05a1c4ff55f5b5807,cyw43_state>>`:: {empty}
        `void(++*++ <<group_cyw43_driver_1ga65550517babd8db2d2a052f41de6ae33,cyw43_poll>>)(void)`:: {empty}
        `uint32_t <<group_cyw43_driver_1ga8345872c237308a5e4e984060f9f399f,cyw43_sleep>>`:: {empty}"""
    )
