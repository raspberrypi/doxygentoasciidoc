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

    asciidoc = VariableSectiondefNode(
        BeautifulSoup(xml, "xml").sectiondef
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        ===== Variables

        `uint32_t <<float_init_rom_8c_1aea98df4cf9adff2a025dc4a09c814986,sf_table>>`:: {empty}"""
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
    ).to_details_asciidoc()

    assert asciidoc == dedent(
        """\
        ===== Variable Documentation

        [#float_init_rom_8c_1aea98df4cf9adff2a025dc4a09c814986]
        ====== sf_table

        [.memname]`uint32_t sf_table[SF_TABLE_V2_SIZE/2]`"""
    )
