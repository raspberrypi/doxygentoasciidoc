from textwrap import dedent
from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import ParameterlistNode


def test_to_asciidoc(tmp_path):
    xml = """
    <parameterlist kind="param"><parameteritem>
    <parameternamelist>
    <parametername>slice_num</parametername>
    </parameternamelist>
    <parameterdescription>
    <para>PWM slice number </para>
    </parameterdescription>
    </parameteritem>
    <parameteritem>
    <parameternamelist>
    <parametername>c</parametername>
    </parameternamelist>
    <parameterdescription>
    <para>Value to set the PWM counter to </para>
    </parameterdescription>
    </parameteritem>
    </parameterlist>
    """

    asciidoc = ParameterlistNode(
        BeautifulSoup(xml, "xml").parameterlist, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        *Parameters*

        [horizontal]
        `slice_num`:: PWM slice number
        `c`:: Value to set the PWM counter to"""
    )


def test_to_asciidoc_with_no_description(tmp_path):
    xml = """
    <parameterlist kind="param"><parameteritem>
    <parameternamelist>
    <parametername>slice_num</parametername>
    </parameternamelist>
    <parameterdescription>
    </parameterdescription>
    </parameteritem>
    </parameterlist>
    """

    asciidoc = ParameterlistNode(
        BeautifulSoup(xml, "xml").parameterlist, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        *Parameters*

        [horizontal]
        `slice_num`:: {empty}"""
    )
