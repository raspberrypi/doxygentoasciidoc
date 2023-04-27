from textwrap import dedent
from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import EnumSectiondefNode


def test_to_asciidoc(tmp_path):
    xml = """\
      <sectiondef kind="enum">
      <memberdef kind="enum" id="group__hardware__clocks_1ga7ac25aa331f7c2624795b6088f87d133" prot="public" static="no" strong="no">
        <type></type>
        <name>clock_index</name>
        <enumvalue id="group__hardware__clocks_1gga7ac25aa331f7c2624795b6088f87d133a8c35a604478e413afed2b3c558df5c64" prot="public">
          <name>clk_gpout0</name>
          <initializer>= 0</initializer>
          <briefdescription>
<para>GPIO Muxing 0. </para>
          </briefdescription>
          <detaileddescription>
          </detaileddescription>
        </enumvalue>
        <enumvalue id="group__hardware__clocks_1gga7ac25aa331f7c2624795b6088f87d133aa1515365ea7f6fc7815d71ac584fcc65" prot="public">
          <name>clk_gpout1</name>
          <briefdescription>
<para>GPIO Muxing 1. </para>
          </briefdescription>
          <detaileddescription>
          </detaileddescription>
        </enumvalue>
        <enumvalue id="group__hardware__clocks_1gga7ac25aa331f7c2624795b6088f87d133af90ddb857bd03e8e8ad086da78dd634b" prot="public">
          <name>CLK_COUNT</name>
          <briefdescription>
          </briefdescription>
          <detaileddescription>
          </detaileddescription>
        </enumvalue>
        <briefdescription>
<para>Enumeration identifying a hardware clock. </para>
        </briefdescription>
        <detaileddescription>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="hardware_structs/include/hardware/structs/clocks.h" line="27" column="1" bodyfile="hardware_structs/include/hardware/structs/clocks.h" bodystart="27" bodyend="39"/>
      </memberdef>
      </sectiondef>
    """

    asciidoc = EnumSectiondefNode(
        BeautifulSoup(xml, "xml").sectiondef, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        ===== Enumerations

        `enum <<group_hardware_clocks_1ga7ac25aa331f7c2624795b6088f87d133,clock_index>> { <<group_hardware_clocks_1gga7ac25aa331f7c2624795b6088f87d133a8c35a604478e413afed2b3c558df5c64,clk_gpout0>> = 0, <<group_hardware_clocks_1gga7ac25aa331f7c2624795b6088f87d133aa1515365ea7f6fc7815d71ac584fcc65,clk_gpout1>>, CLK_COUNT }`:: Enumeration identifying a hardware clock."""
    )


def test_to_asciidoc_with_no_description(tmp_path):
    xml = """\
      <sectiondef kind="enum">
      <memberdef kind="enum" id="group__hardware__clocks_1ga7ac25aa331f7c2624795b6088f87d133" prot="public" static="no" strong="no">
        <type></type>
        <name>clock_index</name>
        <enumvalue id="group__hardware__clocks_1gga7ac25aa331f7c2624795b6088f87d133a8c35a604478e413afed2b3c558df5c64" prot="public">
          <name>clk_gpout0</name>
          <initializer>= 0</initializer>
          <briefdescription>
<para>GPIO Muxing 0. </para>
          </briefdescription>
          <detaileddescription>
          </detaileddescription>
        </enumvalue>
        <briefdescription>
        </briefdescription>
        <detaileddescription>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="hardware_structs/include/hardware/structs/clocks.h" line="27" column="1" bodyfile="hardware_structs/include/hardware/structs/clocks.h" bodystart="27" bodyend="39"/>
      </memberdef>
      </sectiondef>
    """

    asciidoc = EnumSectiondefNode(
        BeautifulSoup(xml, "xml").sectiondef, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        ===== Enumerations

        `enum <<group_hardware_clocks_1ga7ac25aa331f7c2624795b6088f87d133,clock_index>> { <<group_hardware_clocks_1gga7ac25aa331f7c2624795b6088f87d133a8c35a604478e413afed2b3c558df5c64,clk_gpout0>> = 0 }`:: {empty}"""
    )
