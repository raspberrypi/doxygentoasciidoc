from textwrap import dedent
from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import GroupNode


def test_to_asciidoc(tmp_path):
    xml = """\
  <compounddef id="group__hardware__base" kind="group">
    <compoundname>hardware_base</compoundname>
    <title>hardware_base</title>
      <sectiondef kind="func">
      <memberdef kind="function" id="group__hardware__base_1ga625e737a57f12211cf1f634ca5095ae4" prot="public" static="yes" const="no" explicit="no" inline="no" virt="non-virtual">
        <type><ref refid="group__pico__platform_1ga23eadd8d1642fb8fe4600708c36e116a" kindref="member">__force_inline</ref> void</type>
        <definition>static __force_inline void hw_set_bits</definition>
        <argsstring>(io_rw_32 *addr, uint32_t mask)</argsstring>
        <name>hw_set_bits</name>
        <param>
          <type>io_rw_32 *</type>
          <declname>addr</declname>
        </param>
        <param>
          <type>uint32_t</type>
          <declname>mask</declname>
        </param>
        <briefdescription>
<para>Atomically set the specified bits to 1 in a HW register. </para>
        </briefdescription>
        <detaileddescription>
<para><parameterlist kind="param"><parameteritem>
<parameternamelist>
<parametername>addr</parametername>
</parameternamelist>
<parameterdescription>
<para>Address of writable register </para>
</parameterdescription>
</parameteritem>
<parameteritem>
<parameternamelist>
<parametername>mask</parametername>
</parameternamelist>
<parameterdescription>
<para>Bit-mask specifying bits to set </para>
</parameterdescription>
</parameteritem>
</parameterlist>
</para>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="hardware_base/include/hardware/address_mapped.h" line="121" column="28" bodyfile="hardware_base/include/hardware/address_mapped.h" bodystart="121" bodyend="123"/>
      </memberdef>
      </sectiondef>
    <briefdescription>
    </briefdescription>
    <detaileddescription>
<para>Low-level types and (atomic) accessors for memory-mapped hardware registers</para>
<para><computeroutput>hardware_base</computeroutput> defines the low level types and access functions for memory mapped hardware registers. It is included by default by all other hardware libraries.</para>
    </detaileddescription>
  </compounddef>"""
    asciidoc = GroupNode(
        BeautifulSoup(xml, "xml").compounddef, xmldir=tmp_path
    ).to_asciidoc(depth=3)

    assert asciidoc == dedent(
        """\
        [#group_hardware_base,reftext="hardware_base"]
        ==== hardware_base

        ===== Detailed Description

        Low-level types and (atomic) accessors for memory-mapped hardware registers

        `hardware_base` defines the low level types and access functions for memory mapped hardware registers. It is included by default by all other hardware libraries.

        ===== Functions

        `static <<group_pico_platform_1ga23eadd8d1642fb8fe4600708c36e116a,++__force_inline++>> void <<group_hardware_base_1ga625e737a57f12211cf1f634ca5095ae4,hw_set_bits>> (io_rw_32 ++*++addr, uint32_t mask)`:: Atomically set the specified bits to 1 in a HW register.

        ===== Function Documentation

        [#group_hardware_base_1ga625e737a57f12211cf1f634ca5095ae4]
        ====== hw_set_bits

        [.memname]`static <<group_pico_platform_1ga23eadd8d1642fb8fe4600708c36e116a,++__force_inline++>> void hw_set_bits (io_rw_32 ++*++ addr, uint32_t mask) [static]`

        Atomically set the specified bits to 1 in a HW register.

        *Parameters*

        [horizontal]
        `addr`:: Address of writable register
        `mask`:: Bit-mask specifying bits to set"""
    )
