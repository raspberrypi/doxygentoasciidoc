from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import InnergroupNode


def test_to_asciidoc(tmp_path):
    with open(
        f"{tmp_path}/group__channel__config.xml", "w", encoding="utf-8"
    ) as innergroup:
        innergroup.write(
            """\
<?xml version='1.0' encoding='UTF-8' standalone='no'?>
<doxygen xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="compound.xsd" version="1.9.7" xml:lang="en-US">
  <compounddef id="group__channel__config" kind="group">
    <compoundname>channel_config</compoundname>
    <title>channel_config</title>
    <briefdescription>
<para>DMA channel configuration. </para>
    </briefdescription>
  </compoundef>
</doxygen>
            """
        )
    xml = """\
    <innergroup refid="group__channel__config">channel_config</innergroup>
    """

    asciidoc = InnergroupNode(
        BeautifulSoup(xml, "xml").innergroup, xmldir=tmp_path
    ).to_asciidoc()

    assert (
        asciidoc
        == "<<group_channel_config,channel_config>>:: DMA channel configuration."
    )


def test_to_asciidoc_with_no_description(tmp_path):
    with open(
        f"{tmp_path}/group__channel__config.xml", "w", encoding="utf-8"
    ) as innergroup:
        innergroup.write(
            """\
<?xml version='1.0' encoding='UTF-8' standalone='no'?>
<doxygen xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="compound.xsd" version="1.9.7" xml:lang="en-US">
  <compounddef id="group__channel__config" kind="group">
    <compoundname>channel_config</compoundname>
    <title>channel_config</title>
    <briefdescription>
    </briefdescription>
  </compoundef>
</doxygen>
            """
        )
    xml = """\
    <innergroup refid="group__channel__config">channel_config</innergroup>
    """

    asciidoc = InnergroupNode(
        BeautifulSoup(xml, "xml").innergroup, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == "<<group_channel_config,channel_config>>:: {empty}"
