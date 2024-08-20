from textwrap import dedent
from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import FunctionMemberdefNode


def test_to_asciidoc_with_multiple_args(tmp_path):
    xml = """\
  <memberdef kind="function" id="group__interp__config_1ga30d763b581c679c02cefe2fa90d8c8a7" prot="public" static="yes" const="no" explicit="no" inline="yes" virt="non-virtual">
    <type>void</type>
    <definition>static void interp_config_set_shift</definition>
    <argsstring>(interp_config *c, uint shift)</argsstring>
    <name>interp_config_set_shift</name>
    <param>
      <type><ref refid="structinterp__config" kindref="compound">interp_config</ref> *</type>
      <declname>c</declname>
    </param>
    <param>
      <type>uint</type>
      <declname>shift</declname>
    </param>
    <briefdescription>
<para>Set the interpolator shift value. </para>
    </briefdescription>
    <detaileddescription>
<para>Sets the number of bits the accumulator is shifted before masking, on each iteration.</para>
<para><parameterlist kind="param"><parameteritem>
<parameternamelist>
<parametername>c</parametername>
</parameternamelist>
<parameterdescription>
<para>Pointer to an interpolator config </para>
</parameterdescription>
</parameteritem>
<parameteritem>
<parameternamelist>
<parametername>shift</parametername>
</parameternamelist>
<parameterdescription>
<para>Number of bits </para>
</parameterdescription>
</parameteritem>
</parameterlist>
</para>
    </detaileddescription>
    <inbodydescription>
    </inbodydescription>
    <location file="hardware_interp/include/hardware/interp.h" line="121" column="20" bodyfile="hardware_interp/include/hardware/interp.h" bodystart="121" bodyend="125"/>
  </memberdef>
    """

    asciidoc = FunctionMemberdefNode(
        BeautifulSoup(xml, "xml").memberdef, xmldir=tmp_path
    ).to_asciidoc(depth=5)

    assert asciidoc == dedent(
        """\
        [#group_interp_config_1ga30d763b581c679c02cefe2fa90d8c8a7]
        ====== interp_config_set_shift

        [.memname]`static void interp_config_set_shift (<<structinterp_config,interp_config>> ++*++ c, uint shift) [inline], [static]`

        Set the interpolator shift value.

        Sets the number of bits the accumulator is shifted before masking, on each iteration.

        *Parameters*

        [horizontal]
        `c`:: Pointer to an interpolator config
        `shift`:: Number of bits"""
    )


def test_to_asciidoc_with_see_also(tmp_path):
    xml = """\
      <memberdef kind="function" id="group__repeating__timer_1ga9ad5a07a3f2300cc9d46c1c847fae6f1" prot="public" static="no" const="no" explicit="no" inline="no" virt="non-virtual">
        <type>bool</type>
        <definition>bool cancel_repeating_timer</definition>
        <argsstring>(repeating_timer_t *timer)</argsstring>
        <name>cancel_repeating_timer</name>
        <param>
          <type><ref refid="structrepeating__timer" kindref="compound">repeating_timer_t</ref> *</type>
          <declname>timer</declname>
        </param>
        <briefdescription>
<para>Cancel a repeating timer. </para>
        </briefdescription>
        <detaileddescription>
<para><parameterlist kind="param"><parameteritem>
<parameternamelist>
<parametername>timer</parametername>
</parameternamelist>
<parameterdescription>
<para>the repeating timer to cancel </para>
</parameterdescription>
</parameteritem>
</parameterlist>
<simplesect kind="return"><para>true if the repeating timer was cancelled, false if it didn&apos;t exist </para>
</simplesect>
<simplesect kind="see"><para><ref refid="group__alarm_1gaa593548569c182a0d65d2e06a9c3493b" kindref="member">alarm_id_t</ref> for a note on reuse of IDs </para>
</simplesect>
</para>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="pico_time/include/pico/time.h" line="778" column="6" bodyfile="pico_time/time.c" bodystart="359" bodyend="366" declfile="pico_time/include/pico/time.h" declline="778" declcolumn="6"/>
      </memberdef>
    """

    asciidoc = FunctionMemberdefNode(
        BeautifulSoup(xml, "xml").memberdef, xmldir=tmp_path
    ).to_asciidoc(depth=5)

    assert asciidoc == dedent(
        """\
        [#group_repeating_timer_1ga9ad5a07a3f2300cc9d46c1c847fae6f1]
        ====== cancel_repeating_timer

        [.memname]`bool cancel_repeating_timer (<<structrepeating_timer,repeating_timer_t>> ++*++ timer)`

        Cancel a repeating timer.

        *Parameters*

        [horizontal]
        `timer`:: the repeating timer to cancel

        --
        *Returns*

        true if the repeating timer was cancelled, false if it didn't exist
        --

        --
        *See also*

        <<group_alarm_1gaa593548569c182a0d65d2e06a9c3493b,alarm_id_t>> for a note on reuse of IDs
        --"""
    )


def test_to_asciidoc_with_ref_in_type(tmp_path):
    xml = """\
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
    """

    asciidoc = FunctionMemberdefNode(
        BeautifulSoup(xml, "xml").memberdef, xmldir=tmp_path
    ).to_asciidoc(depth=5)

    assert asciidoc == dedent(
        """\
        [#group_hardware_base_1ga625e737a57f12211cf1f634ca5095ae4]
        ====== hw_set_bits

        [.memname]`static <<group_pico_platform_1ga23eadd8d1642fb8fe4600708c36e116a,++__force_inline++>> void hw_set_bits (io_rw_32 ++*++ addr, uint32_t mask) [static]`

        Atomically set the specified bits to 1 in a HW register.

        *Parameters*

        [horizontal]
        `addr`:: Address of writable register
        `mask`:: Bit-mask specifying bits to set"""
    )
