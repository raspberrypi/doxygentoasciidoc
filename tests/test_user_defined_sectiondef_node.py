from textwrap import dedent
from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import UserDefinedSectiondefNode


def test_to_asciidoc():
    xml = """\
      <sectiondef kind="user-defined">
      <header>Authorization types</header>
      <description><para>Used when setting up an access point, or connecting to an access point <anchor id="group__cyw43__ll_1CYW43_AUTH_"/></para>
</description>
      <memberdef kind="define" id="group__cyw43__ll_1ga6f0d5ac786e2c0a86b360310c3d5e25c" prot="public" static="no">
        <name>CYW43_AUTH_OPEN</name>
        <initializer>(0)</initializer>
        <briefdescription>
<para>No authorisation required (open) </para>
        </briefdescription>
        <detaileddescription>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="cyw43_ll.h" line="173" column="9" bodyfile="cyw43_ll.h" bodystart="173" bodyend="-1"/>
      </memberdef>
      </sectiondef>
    """
    asciidoc = UserDefinedSectiondefNode(
        BeautifulSoup(xml, "xml").sectiondef
    ).to_asciidoc(depth=4)

    assert asciidoc == dedent(
        """\
        ===== Authorization types

        Used when setting up an access point, or connecting to an access point [[group_cyw43_ll_1CYW43_AUTH_]]

        [#group_cyw43_ll_1ga6f0d5ac786e2c0a86b360310c3d5e25c]
        ====== CYW43_AUTH_OPEN

        [.memname]`#define CYW43_AUTH_OPEN (0)`

        No authorisation required (open)"""
    )
