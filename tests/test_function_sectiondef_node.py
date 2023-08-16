from textwrap import dedent
from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import FunctionSectiondefNode


def test_to_asciidoc(tmp_path):
    xml = """\
      <sectiondef kind="func">
      <memberdef kind="function" id="group__hardware__adc_1ga2b815e6730e8723a6d1d06d9ef8f31c0" prot="public" static="no" const="no" explicit="no" inline="no" virt="non-virtual">
        <type>void</type>
        <definition>void adc_init</definition>
        <argsstring>(void)</argsstring>
        <name>adc_init</name>
        <param>
          <type>void</type>
        </param>
        <briefdescription>
<para>Initialise the ADC HW. </para>
        </briefdescription>
        <detaileddescription>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="hardware_adc/include/hardware/adc.h" line="60" column="6" bodyfile="hardware_adc/adc.c" bodystart="11" bodyend="23" declfile="hardware_adc/include/hardware/adc.h" declline="60" declcolumn="6"/>
      </memberdef>
      <memberdef kind="function" id="group__hardware__adc_1gab15d6e804715935b4e9b5027a2940910" prot="public" static="yes" const="no" explicit="no" inline="yes" virt="non-virtual">
        <type>void</type>
        <definition>static void adc_gpio_init</definition>
        <argsstring>(uint gpio)</argsstring>
        <name>adc_gpio_init</name>
        <param>
          <type>uint</type>
          <declname>gpio</declname>
        </param>
        <briefdescription>
<para>Initialise the gpio for use as an ADC pin. </para>
        </briefdescription>
        <detaileddescription>
<para>Prepare a GPIO for use with ADC by disabling all digital functions.</para>
<para><parameterlist kind="param"><parameteritem>
<parameternamelist>
<parametername>gpio</parametername>
</parameternamelist>
<parameterdescription>
<para>The GPIO number to use. Allowable GPIO numbers are 26 to 29 inclusive. </para>
</parameterdescription>
</parameteritem>
</parameterlist>
</para>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="hardware_adc/include/hardware/adc.h" line="69" column="20" bodyfile="hardware_adc/include/hardware/adc.h" bodystart="69" bodyend="76"/>
      </memberdef>
      </sectiondef>
    """

    asciidoc = FunctionSectiondefNode(
        BeautifulSoup(xml, "xml").sectiondef, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        ===== Functions

        `void <<group_hardware_adc_1ga2b815e6730e8723a6d1d06d9ef8f31c0,adc_init>> (void)`:: Initialise the ADC HW.
        `static void <<group_hardware_adc_1gab15d6e804715935b4e9b5027a2940910,adc_gpio_init>> (uint gpio)`:: Initialise the gpio for use as an ADC pin."""
    )


def test_to_asciidoc_with_no_description(tmp_path):
    xml = """\
      <sectiondef kind="func">
      <memberdef kind="function" id="group__hardware__adc_1ga2b815e6730e8723a6d1d06d9ef8f31c0" prot="public" static="no" const="no" explicit="no" inline="no" virt="non-virtual">
        <type>void</type>
        <definition>void adc_init</definition>
        <argsstring>(void)</argsstring>
        <name>adc_init</name>
        <param>
          <type>void</type>
        </param>
        <briefdescription>
        </briefdescription>
        <detaileddescription>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="hardware_adc/include/hardware/adc.h" line="60" column="6" bodyfile="hardware_adc/adc.c" bodystart="11" bodyend="23" declfile="hardware_adc/include/hardware/adc.h" declline="60" declcolumn="6"/>
      </memberdef>
      </sectiondef>
    """

    asciidoc = FunctionSectiondefNode(
        BeautifulSoup(xml, "xml").sectiondef, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        ===== Functions

        `void <<group_hardware_adc_1ga2b815e6730e8723a6d1d06d9ef8f31c0,adc_init>> (void)`:: {empty}"""
    )


def test_to_asciidoc_with_ref_in_type(tmp_path):
    xml = """\
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
    """

    asciidoc = FunctionSectiondefNode(
        BeautifulSoup(xml, "xml").sectiondef, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        ===== Functions

        `static <<group_pico_platform_1ga23eadd8d1642fb8fe4600708c36e116a,++__force_inline++>> void <<group_hardware_base_1ga625e737a57f12211cf1f634ca5095ae4,hw_set_bits>> (io_rw_32 ++*++addr, uint32_t mask)`:: Atomically set the specified bits to 1 in a HW register."""
    )
