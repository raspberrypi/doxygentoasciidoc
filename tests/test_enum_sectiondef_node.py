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
    ).to_asciidoc(depth=4)

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
    ).to_asciidoc(depth=4)

    assert asciidoc == dedent(
        """\
        ===== Enumerations

        `enum <<group_hardware_clocks_1ga7ac25aa331f7c2624795b6088f87d133,clock_index>> { <<group_hardware_clocks_1gga7ac25aa331f7c2624795b6088f87d133a8c35a604478e413afed2b3c558df5c64,clk_gpout0>> = 0 }`:: {empty}"""
    )


def test_to_details_asciidoc(tmp_path):
    xml = """\
      <sectiondef kind="enum">
      <memberdef kind="enum" id="group__hardware__exception_1ga504f1c3a5a6959d430665f5d72cf335a" prot="public" static="no" strong="no">
        <type></type>
        <name>exception_number</name>
        <enumvalue id="group__hardware__exception_1gga504f1c3a5a6959d430665f5d72cf335aa6e8a4e796361d59517c80affc6e93cd7" prot="public">
          <name>NMI_EXCEPTION</name>
          <initializer>= -14</initializer>
          <briefdescription>
          </briefdescription>
          <detaileddescription>
          </detaileddescription>
        </enumvalue>
        <briefdescription>
<para>Exception number definitions. </para>
        </briefdescription>
        <detaileddescription>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="hardware_exception/include/hardware/exception.h" line="50" column="1" bodyfile="hardware_exception/include/hardware/exception.h" bodystart="50" bodyend="56"/>
      </memberdef>
      </sectiondef>
    """

    asciidoc = EnumSectiondefNode(
        BeautifulSoup(xml, "xml").sectiondef, xmldir=tmp_path
    ).to_details_asciidoc(depth=4)

    assert asciidoc == dedent(
        """\
        ===== Enumeration Type Documentation

        [#group_hardware_exception_1ga504f1c3a5a6959d430665f5d72cf335a]
        ====== exception_number

        [.memname]`enum exception_number`

        Exception number definitions."""
    )


def test_to_asciidoc_with_anonymous_enum(tmp_path):
    xml = """\
      <sectiondef kind="user-defined">
      <memberdef kind="enum" id="group__cyw43__ll_1gadf764cbdea00d65edcd07bb9953ad2b7" prot="public" static="no" strong="no">
        <type></type>
        <name></name>
        <enumvalue id="group__cyw43__ll_1ggadf764cbdea00d65edcd07bb9953ad2b7a01beff8333d8764c54b44bf2297a1f52" prot="public">
          <name>CYW43_ITF_STA</name>
          <briefdescription>
<para>Client interface STA mode. </para>
          </briefdescription>
          <detaileddescription>
          </detaileddescription>
        </enumvalue>
        <enumvalue id="group__cyw43__ll_1ggadf764cbdea00d65edcd07bb9953ad2b7add57ac73ff47f04da4f09a7aaeb7eb90" prot="public">
          <name>CYW43_ITF_AP</name>
          <briefdescription>
<para>Access point (AP) interface mode. </para>
          </briefdescription>
          <detaileddescription>
          </detaileddescription>
        </enumvalue>
        <briefdescription>
<para>Network interface types <anchor id="group__cyw43__ll_1CYW43_ITF_"/>. </para>
        </briefdescription>
        <detaileddescription>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="cyw43_ll.h" line="207" column="1" bodyfile="cyw43_ll.h" bodystart="207" bodyend="210"/>
      </memberdef>
      </sectiondef>
    """

    asciidoc = EnumSectiondefNode(
        BeautifulSoup(xml, "xml").sectiondef, xmldir=tmp_path
    ).to_asciidoc(depth=4)

    assert asciidoc == dedent(
        """\
        ===== Enumerations

        `enum { <<group_cyw43_ll_1ggadf764cbdea00d65edcd07bb9953ad2b7a01beff8333d8764c54b44bf2297a1f52,CYW43_ITF_STA>>, <<group_cyw43_ll_1ggadf764cbdea00d65edcd07bb9953ad2b7add57ac73ff47f04da4f09a7aaeb7eb90,CYW43_ITF_AP>> }`:: Network interface types [[group_cyw43_ll_1CYW43_ITF_]]."""
    )
