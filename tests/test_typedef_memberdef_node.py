from textwrap import dedent
from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import TypedefMemberdefNode


def test_to_asciidoc(tmp_path):
    xml = """\
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
    """

    asciidoc = TypedefMemberdefNode(
        BeautifulSoup(xml, "xml").memberdef, xmldir=tmp_path
    ).to_asciidoc(depth=5)

    assert asciidoc == dedent(
        """\
        [#group_hardware_clocks_1ga60fddc9bfe13c979c8e3a777d0d89037]
        ====== resus_callback_t

        [.memname]`typedef void(++*++ resus_callback_t) (void)`

        Resus callback function type.

        User provided callback for a resus event (when clk_sys is stopped by the programmer and is restarted for them)."""
    )
