from textwrap import dedent
from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import DoxygenindexNode


def test_to_asciidoc(tmp_path):
    with open(f"{tmp_path}/group__hardware.xml", "w", encoding="utf-8") as hardware:
        hardware.write(
            """\
<?xml version='1.0' encoding='UTF-8' standalone='no'?>
<doxygen xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="compound.xsd" version="1.9.7" xml:lang="en-US">
  <compounddef id="group__hardware" kind="group">
    <compoundname>hardware</compoundname>
    <title>Hardware APIs</title>
    <innergroup refid="group__hardware__base">hardware_base</innergroup>
    <briefdescription>
    </briefdescription>
    <detaileddescription>
<para>This group of libraries provides a thin and efficient C API / abstractions to access the RP2040 hardware without having to read and write hardware registers directly. </para>
    </detaileddescription>
  </compounddef>
</doxygen>
            """
        )
    with open(
        f"{tmp_path}/group__hardware__base.xml", "w", encoding="utf-8"
    ) as hardware_base:
        hardware_base.write(
            """\
<?xml version='1.0' encoding='UTF-8' standalone='no'?>
<doxygen xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="compound.xsd" version="1.9.7" xml:lang="en-US">
  <compounddef id="group__hardware__base" kind="group">
    <compoundname>hardware_base</compoundname>
    <title>hardware_base</title>
    <innergroup refid="group__channel__config">channel_config</innergroup>
    <briefdescription>
    </briefdescription>
    <detaileddescription>
<para>Low-level types and (atomic) accessors for memory-mapped hardware registers</para>
<para><computeroutput>hardware_base</computeroutput> defines the low level types and access functions for memory mapped hardware registers. It is included by default by all other hardware libraries.</para>
    </detaileddescription>
  </compounddef>
</doxygen>
            """
        )
    with open(
        f"{tmp_path}/group__channel__config.xml", "w", encoding="utf-8"
    ) as channel_config:
        channel_config.write(
            """\
<?xml version='1.0' encoding='UTF-8' standalone='no'?>
<doxygen xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="compound.xsd" version="1.9.7" xml:lang="en-US">
  <compounddef id="group__channel__config" kind="group">
    <compoundname>channel_config</compoundname>
    <title>channel_config</title>
    <briefdescription>
<para>DMA channel configuration. </para>
    </briefdescription>
    <detaileddescription>
    </detaileddescription>
  </compoundef>
</doxygen>
            """
        )
    xml = """\
<?xml version='1.0' encoding='UTF-8' standalone='no'?>
<doxygenindex xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="index.xsd" version="1.9.7" xml:lang="en-US">
<compound refid="group__hardware" kind="group"><name>hardware</name>
</compound>
<compound refid="group__hardware__base" kind="group"><name>hardware_base</name>
</compound>
<compound refid="group__channel__config" kind="group"><name>channel_config</name>
</compound>
</doxygenindex>
    """

    asciidoc = DoxygenindexNode(
        BeautifulSoup(xml, "xml").doxygenindex, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        [[group_hardware,Hardware APIs]]
        === Hardware APIs

        This group of libraries provides a thin and efficient C API / abstractions to access the RP2040 hardware without having to read and write hardware registers directly.

        [cols="1,4"]
        |===
        |<<group_hardware_base,hardware_base>>
        |

        |{nbsp}{nbsp}{nbsp}{nbsp}<<group_channel_config,channel_config>>
        |DMA channel configuration.
        |===

        [[group_hardware_base,hardware_base]]
        ==== hardware_base

        ===== Detailed Description

        Low-level types and (atomic) accessors for memory-mapped hardware registers

        `hardware_base` defines the low level types and access functions for memory mapped hardware registers. It is included by default by all other hardware libraries.

        ===== Modules

        <<group_channel_config,channel_config>>:: DMA channel configuration.

        [[group_channel_config,channel_config]]
        ===== channel_config

        DMA channel configuration."""
    )
