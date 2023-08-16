from textwrap import dedent
from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import DefineMemberdefNode


def test_to_asciidoc(tmp_path):
    xml = """\
      <memberdef kind="define" id="group__hardware__pio_1ga916d05e71da7f2173cd22b46bbfa0a11" prot="public" static="no">
        <name>pio0</name>
        <initializer>pio0_hw</initializer>
        <briefdescription>
        </briefdescription>
        <detaileddescription>
<para>Identifier for the first (PIO 0) hardware PIO instance (for use in PIO functions).</para>
<para>e.g. pio_gpio_init(pio0, 5) </para>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="hardware_pio/include/hardware/pio.h" line="77" column="9" bodyfile="hardware_pio/include/hardware/pio.h" bodystart="77" bodyend="-1"/>
      </memberdef>
    """

    asciidoc = DefineMemberdefNode(
        BeautifulSoup(xml, "xml").memberdef, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        [#group_hardware_pio_1ga916d05e71da7f2173cd22b46bbfa0a11]
        ====== pio0

        `#define pio0 pio0_hw`

        Identifier for the first (PIO 0) hardware PIO instance (for use in PIO functions).

        e.g. pio_gpio_init(pio0, 5)"""
    )


def test_to_asciidoc_with_no_initializer(tmp_path):
    xml = """\
      <memberdef kind="define" id="group__hardware__pio_1ga923a261ba19804c404900228e99c9522" prot="public" static="no">
        <name>pio1</name>
        <briefdescription>
        </briefdescription>
        <detaileddescription>
<para>Identifier for the second (PIO 1) hardware PIO instance (for use in PIO functions).</para>
<para>e.g. pio_gpio_init(pio1, 5) </para>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="hardware_pio/include/hardware/pio.h" line="85" column="9" bodyfile="hardware_pio/include/hardware/pio.h" bodystart="85" bodyend="-1"/>
      </memberdef>
    """

    asciidoc = DefineMemberdefNode(
        BeautifulSoup(xml, "xml").memberdef, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        [#group_hardware_pio_1ga923a261ba19804c404900228e99c9522]
        ====== pio1

        `#define pio1`

        Identifier for the second (PIO 1) hardware PIO instance (for use in PIO functions).

        e.g. pio_gpio_init(pio1, 5)"""
    )


def test_to_asciidoc_with_multiline_initializer(tmp_path):
    xml = """\
      <memberdef kind="define" id="group__lock__core_1ga627a09221ed61634d6dfea6f406e104e" prot="public" static="no">
        <name>lock_internal_spin_unlock_with_best_effort_wait_or_timeout</name>
        <param><defname>lock</defname></param>
        <param><defname>save</defname></param>
        <param><defname>until</defname></param>
        <initializer>    ({ \\
    <ref refid="group__hardware__sync_1ga281ce69786da23cab7ba6c42537d4e87" kindref="member">spin_unlock</ref>((lock)-&gt;spin_lock, save);                                                \\
    <ref refid="group__sleep_1gaedc0ed51a5e908ddd660a5d279009abc" kindref="member">best_effort_wfe_or_timeout</ref>(until);                                                   \\
})</initializer>
        <briefdescription>
<para>Atomically unlock the lock&apos;s spin lock, and wait for a notification or a timeout. </para>
        </briefdescription>
        <detaileddescription>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="pico_sync/include/pico/lock_core.h" line="175" column="9" bodyfile="pico_sync/include/pico/lock_core.h" bodystart="175" bodyend="-1"/>
      </memberdef>
      """

    asciidoc = DefineMemberdefNode(
        BeautifulSoup(xml, "xml").memberdef, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        [#group_lock_core_1ga627a09221ed61634d6dfea6f406e104e]
        ====== lock_internal_spin_unlock_with_best_effort_wait_or_timeout

        [source,c]
        ----
        #define lock_internal_spin_unlock_with_best_effort_wait_or_timeout(lock, save, until) ({ \\
            spin_unlock((lock)->spin_lock, save);                                                \\
            best_effort_wfe_or_timeout(until);                                                   \\
        })
        ----

        Atomically unlock the lock's spin lock, and wait for a notification or a timeout."""
    )
