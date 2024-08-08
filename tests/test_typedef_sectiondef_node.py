from textwrap import dedent
from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import TypedefSectiondefNode


def test_to_asciidoc(tmp_path):
    xml = """\
      <sectiondef kind="typedef">
      <memberdef kind="typedef" id="group__hardware__clocks_1ga60fddc9bfe13c979c8e3a777d0d89037" prot="public" static="no">
        <type>void(*</type>
        <definition>typedef void(* resus_callback_t) (void)</definition>
        <argsstring>)(void)</argsstring>
        <name>resus_callback_t</name>
        <briefdescription>
<para>Resus callback function type. </para>
        </briefdescription>
        <detaileddescription>
<para>User provided callback for a resus event (when clk_sys is stopped by the programmer and is restarted for them). </para>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="hardware_clocks/include/hardware/clocks.h" line="222" column="9" bodyfile="hardware_clocks/include/hardware/clocks.h" bodystart="222" bodyend="-1"/>
      </memberdef>
      </sectiondef>
    """

    asciidoc = TypedefSectiondefNode(
        BeautifulSoup(xml, "xml").sectiondef, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        ===== Typedefs

        `typedef void(++*++ <<group_hardware_clocks_1ga60fddc9bfe13c979c8e3a777d0d89037,resus_callback_t>>)(void)`:: Resus callback function type."""
    )


def test_to_asciidoc_with_no_description(tmp_path):
    xml = """\
      <sectiondef kind="typedef">
      <memberdef kind="typedef" id="group__hardware__clocks_1ga60fddc9bfe13c979c8e3a777d0d89037" prot="public" static="no">
        <type>void(*</type>
        <definition>typedef void(* resus_callback_t) (void)</definition>
        <argsstring>)(void)</argsstring>
        <name>resus_callback_t</name>
        <briefdescription>
        </briefdescription>
        <detaileddescription>
<para>User provided callback for a resus event (when clk_sys is stopped by the programmer and is restarted for them). </para>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="hardware_clocks/include/hardware/clocks.h" line="222" column="9" bodyfile="hardware_clocks/include/hardware/clocks.h" bodystart="222" bodyend="-1"/>
      </memberdef>
      </sectiondef>
    """

    asciidoc = TypedefSectiondefNode(
        BeautifulSoup(xml, "xml").sectiondef, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        ===== Typedefs

        `typedef void(++*++ <<group_hardware_clocks_1ga60fddc9bfe13c979c8e3a777d0d89037,resus_callback_t>>)(void)`:: {empty}"""
    )


def test_to_asciidoc_with_refs_in_type(tmp_path):
    xml = """\
      <sectiondef kind="typedef">
      <memberdef kind="typedef" id="group__mutex_1gaa0676aca346799845ab75d3fb6d96ff6" prot="public" static="no">
        <type>struct <ref refid="struct____packed__aligned" kindref="compound">__packed_aligned</ref> <ref refid="structmutex" kindref="compound">mutex</ref></type>
        <definition>typedef struct __packed_aligned mutex mutex_t</definition>
        <argsstring></argsstring>
        <name>mutex_t</name>
        <briefdescription>
<para>regular (non recursive) mutex instance </para>
        </briefdescription>
        <detaileddescription>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="pico_sync/include/pico/mutex.h" line="63" column="9"/>
      </memberdef>
      </sectiondef>
    """

    asciidoc = TypedefSectiondefNode(
        BeautifulSoup(xml, "xml").sectiondef, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        ===== Typedefs

        `typedef struct <<struct_packed_aligned,++__packed_aligned++>> <<structmutex,mutex>> <<group_mutex_1gaa0676aca346799845ab75d3fb6d96ff6,mutex_t>>`:: regular (non recursive) mutex instance"""
    )


def test_to_details_asciidoc(tmp_path):
    xml = """\
      <sectiondef kind="typedef">
      <memberdef kind="typedef" id="group__hardware__clocks_1ga60fddc9bfe13c979c8e3a777d0d89037" prot="public" static="no">
        <type>void(*</type>
        <definition>typedef void(* resus_callback_t) (void)</definition>
        <argsstring>)(void)</argsstring>
        <name>resus_callback_t</name>
        <briefdescription>
<para>Resus callback function type. </para>
        </briefdescription>
        <detaileddescription>
<para>User provided callback for a resus event (when clk_sys is stopped by the programmer and is restarted for them). </para>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="hardware_clocks/include/hardware/clocks.h" line="222" column="9" bodyfile="hardware_clocks/include/hardware/clocks.h" bodystart="222" bodyend="-1"/>
      </memberdef>
      </sectiondef>
    """

    asciidoc = TypedefSectiondefNode(
        BeautifulSoup(xml, "xml").sectiondef, xmldir=tmp_path
    ).to_details_asciidoc()

    assert asciidoc == dedent(
        """\
        ===== Typedef Documentation

        [#group_hardware_clocks_1ga60fddc9bfe13c979c8e3a777d0d89037]
        ====== resus_callback_t

        [.memname]`typedef void(++*++ resus_callback_t) (void)`

        Resus callback function type.

        User provided callback for a resus event (when clk_sys is stopped by the programmer and is restarted for them)."""
    )
