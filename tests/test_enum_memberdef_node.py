from textwrap import dedent
from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import EnumMemberdefNode


def test_to_asciidoc(tmp_path):
    xml = """\
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
        <enumvalue id="group__hardware__exception_1gga504f1c3a5a6959d430665f5d72cf335aadf88404244d6cf50e5103848de3892e2" prot="public">
          <name>HARDFAULT_EXCEPTION</name>
          <initializer>= -13</initializer>
          <briefdescription>
          </briefdescription>
          <detaileddescription>
          </detaileddescription>
        </enumvalue>
        <enumvalue id="group__hardware__exception_1gga504f1c3a5a6959d430665f5d72cf335aa1e7d691476a041fb59915e046e85d586" prot="public">
          <name>SVCALL_EXCEPTION</name>
          <initializer>=  -5</initializer>
          <briefdescription>
          </briefdescription>
          <detaileddescription>
          </detaileddescription>
        </enumvalue>
        <enumvalue id="group__hardware__exception_1gga504f1c3a5a6959d430665f5d72cf335aae6e5980728dbb2ff717a7867bdb25a3a" prot="public">
          <name>PENDSV_EXCEPTION</name>
          <initializer>=  -2</initializer>
          <briefdescription>
          </briefdescription>
          <detaileddescription>
          </detaileddescription>
        </enumvalue>
        <enumvalue id="group__hardware__exception_1gga504f1c3a5a6959d430665f5d72cf335aa05ced3409f791060c7eab53bc557c333" prot="public">
          <name>SYSTICK_EXCEPTION</name>
          <initializer>=  -1</initializer>
          <briefdescription>
          </briefdescription>
          <detaileddescription>
          </detaileddescription>
        </enumvalue>
        <briefdescription>
<para>Exception number definitions. </para>
        </briefdescription>
        <detaileddescription>
<para>Note for consistency with irq numbers, these numbers are defined to be negative. The VTABLE index is the number here plus 16.</para>
<para><table rows="6" cols="3"><row>
<entry thead="yes"><para>Name   </para>
</entry><entry thead="yes"><para>Value   </para>
</entry><entry thead="yes"><para>Exception    </para>
</entry></row>
<row>
<entry thead="no"><para>NMI_EXCEPTION   </para>
</entry><entry thead="no"><para>-14   </para>
</entry><entry thead="no"><para>Non Maskable Interrupt    </para>
</entry></row>
<row>
<entry thead="no"><para>HARDFAULT_EXCEPTION   </para>
</entry><entry thead="no"><para>-13   </para>
</entry><entry thead="no"><para>HardFault    </para>
</entry></row>
<row>
<entry thead="no"><para>SVCALL_EXCEPTION   </para>
</entry><entry thead="no"><para>-5   </para>
</entry><entry thead="no"><para>SV Call    </para>
</entry></row>
<row>
<entry thead="no"><para>PENDSV_EXCEPTION   </para>
</entry><entry thead="no"><para>-2   </para>
</entry><entry thead="no"><para>Pend SV    </para>
</entry></row>
<row>
<entry thead="no"><para>SYSTICK_EXCEPTION   </para>
</entry><entry thead="no"><para>-1   </para>
</entry><entry thead="no"><para>System Tick   </para>
</entry></row>
</table>
</para>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="hardware_exception/include/hardware/exception.h" line="50" column="1" bodyfile="hardware_exception/include/hardware/exception.h" bodystart="50" bodyend="56"/>
      </memberdef>
    """

    asciidoc = EnumMemberdefNode(
        BeautifulSoup(xml, "xml").memberdef, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        [#group_hardware_exception_1ga504f1c3a5a6959d430665f5d72cf335a]
        ====== exception_number

        [.memname]`enum exception_number`

        Exception number definitions.

        Note for consistency with irq numbers, these numbers are defined to be negative. The VTABLE index is the number here plus 16.

        |===
        |Name |Value |Exception

        |NMI_EXCEPTION
        |-14
        |Non Maskable Interrupt

        |HARDFAULT_EXCEPTION
        |-13
        |HardFault

        |SVCALL_EXCEPTION
        |-5
        |SV Call

        |PENDSV_EXCEPTION
        |-2
        |Pend SV

        |SYSTICK_EXCEPTION
        |-1
        |System Tick
        |==="""
    )


def test_to_asciidoc_generates_a_table_if_enumvalues_have_descriptions(tmp_path):
    xml = """\
      <memberdef kind="enum" id="group__hardware__gpio_1ga14eba84c1c8f80b08a770775d3bf060a" prot="public" static="no" strong="no">
        <type></type>
        <name>gpio_drive_strength</name>
        <enumvalue id="group__hardware__gpio_1gga14eba84c1c8f80b08a770775d3bf060aa04d31285e4f4921102485e775e55e295" prot="public">
          <name>GPIO_DRIVE_STRENGTH_2MA</name>
          <initializer>= 0</initializer>
          <briefdescription>
<para>2 mA nominal drive strength </para>
          </briefdescription>
          <detaileddescription>
          </detaileddescription>
        </enumvalue>
        <enumvalue id="group__hardware__gpio_1gga14eba84c1c8f80b08a770775d3bf060aa5c9d0b430fd44ee7688d58cf94f47de6" prot="public">
          <name>GPIO_DRIVE_STRENGTH_4MA</name>
          <initializer>= 1</initializer>
          <briefdescription>
<para>4 mA nominal drive strength </para>
          </briefdescription>
          <detaileddescription>
          </detaileddescription>
        </enumvalue>
        <enumvalue id="group__hardware__gpio_1gga14eba84c1c8f80b08a770775d3bf060aa3cc28353572b5f8e8bb2eb80f884a98d" prot="public">
          <name>GPIO_DRIVE_STRENGTH_8MA</name>
          <initializer>= 2</initializer>
          <briefdescription>
<para>8 mA nominal drive strength </para>
          </briefdescription>
          <detaileddescription>
          </detaileddescription>
        </enumvalue>
        <enumvalue id="group__hardware__gpio_1gga14eba84c1c8f80b08a770775d3bf060aa418f6be7649c316bab248b91c2eb1716" prot="public">
          <name>GPIO_DRIVE_STRENGTH_12MA</name>
          <initializer>= 3</initializer>
          <briefdescription>
<para>12 mA nominal drive strength </para>
          </briefdescription>
          <detaileddescription>
          </detaileddescription>
        </enumvalue>
        <briefdescription>
<para>Drive strength levels for GPIO outputs. </para>
        </briefdescription>
        <detaileddescription>
<para>Drive strength levels for GPIO outputs. <simplesect kind="see"><para><ref refid="group__hardware__gpio_1ga0ffe0ddabcd081b513731275df97e7ca" kindref="member">gpio_set_drive_strength</ref> </para>
</simplesect>
</para>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="hardware_gpio/include/hardware/gpio.h" line="164" column="1" bodyfile="hardware_gpio/include/hardware/gpio.h" bodystart="164" bodyend="169"/>
      </memberdef>
    """

    asciidoc = EnumMemberdefNode(
        BeautifulSoup(xml, "xml").memberdef, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        [#group_hardware_gpio_1ga14eba84c1c8f80b08a770775d3bf060a]
        ====== gpio_drive_strength

        [.memname]`enum gpio_drive_strength`

        Drive strength levels for GPIO outputs.

        Drive strength levels for GPIO outputs.

        --
        *See also*

        <<group_hardware_gpio_1ga0ffe0ddabcd081b513731275df97e7ca,gpio_set_drive_strength>>
        --

        .Enumerator
        [cols="h,1"]
        |===
        |[[group_hardware_gpio_1gga14eba84c1c8f80b08a770775d3bf060aa04d31285e4f4921102485e775e55e295]]GPIO_DRIVE_STRENGTH_2MA
        |2 mA nominal drive strength

        |[[group_hardware_gpio_1gga14eba84c1c8f80b08a770775d3bf060aa5c9d0b430fd44ee7688d58cf94f47de6]]GPIO_DRIVE_STRENGTH_4MA
        |4 mA nominal drive strength

        |[[group_hardware_gpio_1gga14eba84c1c8f80b08a770775d3bf060aa3cc28353572b5f8e8bb2eb80f884a98d]]GPIO_DRIVE_STRENGTH_8MA
        |8 mA nominal drive strength

        |[[group_hardware_gpio_1gga14eba84c1c8f80b08a770775d3bf060aa418f6be7649c316bab248b91c2eb1716]]GPIO_DRIVE_STRENGTH_12MA
        |12 mA nominal drive strength
        |==="""
    )


def test_to_asciidoc_with_anonymous_enum(tmp_path):
    xml = """\
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
    """

    asciidoc = EnumMemberdefNode(
        BeautifulSoup(xml, "xml").memberdef, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        [#group_cyw43_ll_1gadf764cbdea00d65edcd07bb9953ad2b7]
        ====== anonymous enum

        [.memname]`anonymous enum`

        Network interface types [[group_cyw43_ll_1CYW43_ITF_]].

        .Enumerator
        [cols="h,1"]
        |===
        |[[group_cyw43_ll_1ggadf764cbdea00d65edcd07bb9953ad2b7a01beff8333d8764c54b44bf2297a1f52]]CYW43_ITF_STA
        |Client interface STA mode.

        |[[group_cyw43_ll_1ggadf764cbdea00d65edcd07bb9953ad2b7add57ac73ff47f04da4f09a7aaeb7eb90]]CYW43_ITF_AP
        |Access point (AP) interface mode.
        |==="""
    )
