from textwrap import dedent
from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import DataStructureNode


def test_to_asciidoc(tmp_path):
    xml = """\
      <compounddef id="structalarm__pool" kind="struct" language="C++" prot="public">
        <compoundname>alarm_pool</compoundname>
          <sectiondef kind="public-attrib">
          <memberdef kind="variable" id="structalarm__pool_1af2a37ab928d6f7b6469be2223950478f" prot="public" static="no" mutable="no">
            <type><ref refid="structpheap" kindref="compound">pheap_t</ref> *</type>
            <definition>pheap_t* alarm_pool::heap</definition>
            <argsstring></argsstring>
            <name>heap</name>
            <qualifiedname>alarm_pool::heap</qualifiedname>
            <briefdescription>
            </briefdescription>
            <detaileddescription>
            </detaileddescription>
            <inbodydescription>
            </inbodydescription>
            <location file="pico_time/time.c" line="26" column="13" bodyfile="pico_time/time.c" bodystart="26" bodyend="-1"/>
          </memberdef>
          </sectiondef>
        <briefdescription>
        </briefdescription>
        <detaileddescription>
        </detaileddescription>
        <collaborationgraph>
          <node id="5">
            <label>absolute_time_t</label>
            <link refid="structabsolute__time__t"/>
          </node>
          <node id="1">
            <label>alarm_pool</label>
            <link refid="structalarm__pool"/>
            <childnode refid="2" relation="usage">
              <edgelabel>heap</edgelabel>
            </childnode>
            <childnode refid="4" relation="usage">
              <edgelabel>entries</edgelabel>
            </childnode>
          </node>
          <node id="4">
            <label>alarm_pool_entry</label>
            <link refid="structalarm__pool__entry"/>
            <childnode refid="5" relation="usage">
              <edgelabel>target</edgelabel>
            </childnode>
          </node>
          <node id="2">
            <label>pheap</label>
            <link refid="structpheap"/>
            <childnode refid="3" relation="usage">
              <edgelabel>nodes</edgelabel>
            </childnode>
          </node>
          <node id="3">
            <label>pheap_node</label>
            <link refid="structpheap__node"/>
          </node>
        </collaborationgraph>
        <location file="pico_time/time.c" line="25" column="1" bodyfile="pico_time/time.c" bodystart="25" bodyend="35"/>
        <listofallmembers>
          <member refid="structalarm__pool_1af2a37ab928d6f7b6469be2223950478f" prot="public" virt="non-virtual"><scope>alarm_pool</scope><name>heap</name></member>
        </listofallmembers>
      </compounddef>
    """
    asciidoc = DataStructureNode(
        BeautifulSoup(xml, "xml").compounddef, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        [#structalarm_pool]
        ==== alarm_pool

        ===== Variable Documentation

        [#structalarm_pool_1af2a37ab928d6f7b6469be2223950478f]
        ====== heap

        `pheap_t++*++ alarm_pool::heap`"""
    )
