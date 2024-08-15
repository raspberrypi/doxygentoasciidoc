# pylint: disable=line-too-long

from textwrap import dedent
from bs4 import BeautifulSoup
from doxygentoasciidoc.nodes import PageNode


def test_page_node_with_example_page(tmp_path):
    xml = """\
    <compounddef id="examples_page" kind="page">
    <compoundname>examples_page</compoundname>
    <title>Examples Index</title>
    <briefdescription>
    </briefdescription>
    <detaileddescription>
    <para><anchor id="examples_page_1md__2_users_2mudge_2_work_2raspberrypi_2databooks_2lib_2pico-sdk_2docs_2examples"/></para>
    <para>This page links to the various example code fragments in this documentation. For more complete examples, please see the <ulink url="https://github.com/raspberrypi/pico-examples">pico-examples</ulink> repository, which contains complete buildable projects.</para>
    <para><itemizedlist>
    <listitem><para><ref kindref="member" refid="group__hardware__rtc_1rtc_example">RTC example</ref></para>
    </listitem><listitem><para><ref kindref="member" refid="group__hardware__uart_1uart_example">UART example</ref></para>
    </listitem><listitem><para><ref kindref="member" refid="group__hardware__adc_1adc_example">ADC example</ref></para>
    </listitem><listitem><para><ref kindref="member" refid="group__hardware__i2c_1i2c_example">I2C example</ref></para>
    </listitem><listitem><para><ref kindref="member" refid="group__hardware__clocks_1clock_example">Clock example</ref></para>
    </listitem><listitem><para><ref kindref="member" refid="group__hardware__timer_1timer_example">Timer example</ref></para>
    </listitem><listitem><para><ref kindref="member" refid="group__hardware__flash_1flash_example">Flash programming example</ref></para>
    </listitem><listitem><para><ref kindref="member" refid="group__hardware__watchdog_1watchdog_example">Watchdog example</ref></para>
    </listitem><listitem><para><ref kindref="member" refid="group__hardware__divider_1divider_example">Divider example</ref></para>
    </listitem><listitem><para><ref kindref="member" refid="group__hardware__pwm_1pwm_example">PWM example</ref></para>
    </listitem><listitem><para><ref kindref="member" refid="group__pico__multicore_1multicore_example">Multicore example</ref></para>
    </listitem><listitem><para><ref kindref="member" refid="group__hardware__resets_1reset_example">Reset example</ref></para>
    </listitem></itemizedlist>
    </para>
    <para>All examples are "Copyright (c) 2020 Raspberry Pi (Trading) Ltd", and are released under a 3-Clause BSD licence. Briefly, this means you are free to use the example code as long as you retain the copyright notice. Full details on the licence can be found <ulink url="https://opensource.org/licenses/BSD-3-Clause">here</ulink>. </para>
    </detaileddescription>
    <location file="/Users/mudge/Work/raspberrypi/databooks/lib/pico-sdk/docs/examples.md"/>
    </compounddef>
    """

    asciidoc = PageNode(
        BeautifulSoup(xml, "xml").compounddef, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        [#examples_page]
        == Examples Index

        [[examples_page_1md_2_users_2mudge_2_work_2raspberrypi_2databooks_2lib_2pico-sdk_2docs_2examples]]

        This page links to the various example code fragments in this documentation. For more complete examples, please see the https://github.com/raspberrypi/pico-examples[pico-examples] repository, which contains complete buildable projects.

        * {empty}
        +
        --
        <<group_hardware_rtc_1rtc_example,RTC example>>
        --

        * {empty}
        +
        --
        <<group_hardware_uart_1uart_example,UART example>>
        --

        * {empty}
        +
        --
        <<group_hardware_adc_1adc_example,ADC example>>
        --

        * {empty}
        +
        --
        <<group_hardware_i2c_1i2c_example,I2C example>>
        --

        * {empty}
        +
        --
        <<group_hardware_clocks_1clock_example,Clock example>>
        --

        * {empty}
        +
        --
        <<group_hardware_timer_1timer_example,Timer example>>
        --

        * {empty}
        +
        --
        <<group_hardware_flash_1flash_example,Flash programming example>>
        --

        * {empty}
        +
        --
        <<group_hardware_watchdog_1watchdog_example,Watchdog example>>
        --

        * {empty}
        +
        --
        <<group_hardware_divider_1divider_example,Divider example>>
        --

        * {empty}
        +
        --
        <<group_hardware_pwm_1pwm_example,PWM example>>
        --

        * {empty}
        +
        --
        <<group_pico_multicore_1multicore_example,Multicore example>>
        --

        * {empty}
        +
        --
        <<group_hardware_resets_1reset_example,Reset example>>
        --

        All examples are "Copyright (c) 2020 Raspberry Pi (Trading) Ltd", and are released under a 3-Clause BSD licence. Briefly, this means you are free to use the example code as long as you retain the copyright notice. Full details on the licence can be found https://opensource.org/licenses/BSD-3-Clause[here]."""
    )


def test_page_node_with_indexpage(tmp_path):
    xml = """\
    <compounddef id="indexpage" kind="page">
    <compoundname>index</compoundname>
    <title>Raspberry Pi Pico SDK</title>
    <briefdescription>
    </briefdescription>
    <detaileddescription>
    <para><anchor id="index_1md__2_users_2mudge_2_work_2raspberrypi_2databooks_2lib_2pico-sdk_2docs_2mainpage"/></para>
    <para>The Raspberry Pi Pico SDK (Software Development Kit), henceforth SDK, provides the headers, libraries and build system necessary to write programs for RP-series microcontroller devices such as the Raspberry Pi Pico in C, C++ or assembly language. The SDK is designed to provide an API (Application Programming Interface) and programming environment that is familiar both to non-embedded C developers and embedded C developers alike.</para>
    <para>A single program runs on the device at a time with a conventional <computeroutput>main()</computeroutput> method. Standard C/C++ libraries are supported along with APIs for accessing the microcontroller's hardware, including DMA, IRQs, and the wide variety of fixed-function peripherals and PIO (Programmable IO).</para>
    <para>Additionally the SDK provides higher-level libraries for dealing with timers, USB, synchronization and multi-core programming, along with additional high-level functionality built using PIO, such as audio. The SDK can be used to build anything from simple applications, or full-fledged runtime environments such as MicroPython, to low-level software such as the microcontroller's on-chip bootrom itself.</para>
    <para>This documentation is generated from the SDK source tree using Doxygen. It provides basic information on the APIs used for each library, but does not provide usage information. Please refer to the Databooks for usage and more technical information.</para>
    <sect1 id="index_1autotoc_md3">
    <title>SDK Design</title><para>The RP-series microcontroller range are powerful chips, however they are used in an embedded environment, so both RAM and program space are at premium. Additionally the trade-offs between performance and other factors (e.g. edge-case error handling, runtime vs compile-time configuration) are necessarily much more visible to the developer than they might be on other higher-level platforms.</para>
    <para>The intention within the SDK has been for features to just work out of the box, with sensible defaults, but also to give the developer as much control and power as possible (if they want it) to fine-tune every aspect of the application they are building and the libraries used.</para>
    </sect1>
    <sect1 id="index_1autotoc_md4">
    <title>The Build System</title><para>The SDK uses CMake to manage the build. CMake is widely supported by IDEs (Integrated Development Environments), and allows a simple specification of the build (via <computeroutput>CMakeLists.txt</computeroutput> files), from which CMake can generate a build system (for use by <computeroutput>make</computeroutput>, <computeroutput>ninja</computeroutput> or other build tools) customized for the platform and by any configuration variables the developer chooses.</para>
    <para>Apart from being a widely-used build system for C/C++ development, CMake is fundamental to the way the SDK is structured, and how applications are configured and built.</para>
    <para>The SDK builds an executable which is bare-metal, i.e. it includes the entirety of the code needed to run on the device (other than device specific floating-point and other optimized code contained in the bootrom within the microcontroller).</para>
    </sect1>
    <sect1 id="index_1autotoc_md5">
    <title>Examples</title><para>This SDK documentation contains a number of example code fragments. An index of these examples can be found <ref kindref="compound" refid="examples_page">here</ref>. These examples, and any other source code included in this documentation, is Copyright <copy/> 2020 Raspberry Pi Ltd and licensed under the <ulink url="https://opensource.org/licenses/BSD-3-Clause">3-Clause BSD</ulink> license. </para>
    </sect1>
    </detaileddescription>
    <location file="/Users/mudge/Work/raspberrypi/databooks/lib/pico-sdk/docs/mainpage.md"/>
    </compounddef>
    """

    asciidoc = PageNode(
        BeautifulSoup(xml, "xml").compounddef, xmldir=tmp_path
    ).to_asciidoc()

    assert asciidoc == dedent(
        """\
        [#indexpage]
        == Raspberry Pi Pico SDK

        [[index_1md_2_users_2mudge_2_work_2raspberrypi_2databooks_2lib_2pico-sdk_2docs_2mainpage]]

        The Raspberry Pi Pico SDK (Software Development Kit), henceforth SDK, provides the headers, libraries and build system necessary to write programs for RP-series microcontroller devices such as the Raspberry Pi Pico in C, C++ or assembly language. The SDK is designed to provide an API (Application Programming Interface) and programming environment that is familiar both to non-embedded C developers and embedded C developers alike.

        A single program runs on the device at a time with a conventional `main()` method. Standard C/C++ libraries are supported along with APIs for accessing the microcontroller's hardware, including DMA, IRQs, and the wide variety of fixed-function peripherals and PIO (Programmable IO).

        Additionally the SDK provides higher-level libraries for dealing with timers, USB, synchronization and multi-core programming, along with additional high-level functionality built using PIO, such as audio. The SDK can be used to build anything from simple applications, or full-fledged runtime environments such as MicroPython, to low-level software such as the microcontroller's on-chip bootrom itself.

        This documentation is generated from the SDK source tree using Doxygen. It provides basic information on the APIs used for each library, but does not provide usage information. Please refer to the Databooks for usage and more technical information.

        [#index_1autotoc_md3]
        === SDK Design

        The RP-series microcontroller range are powerful chips, however they are used in an embedded environment, so both RAM and program space are at premium. Additionally the trade-offs between performance and other factors (e.g. edge-case error handling, runtime vs compile-time configuration) are necessarily much more visible to the developer than they might be on other higher-level platforms.

        The intention within the SDK has been for features to just work out of the box, with sensible defaults, but also to give the developer as much control and power as possible (if they want it) to fine-tune every aspect of the application they are building and the libraries used.

        [#index_1autotoc_md4]
        === The Build System

        The SDK uses CMake to manage the build. CMake is widely supported by IDEs (Integrated Development Environments), and allows a simple specification of the build (via `CMakeLists.txt` files), from which CMake can generate a build system (for use by `make`, `ninja` or other build tools) customized for the platform and by any configuration variables the developer chooses.

        Apart from being a widely-used build system for C/C++ development, CMake is fundamental to the way the SDK is structured, and how applications are configured and built.

        The SDK builds an executable which is bare-metal, i.e. it includes the entirety of the code needed to run on the device (other than device specific floating-point and other optimized code contained in the bootrom within the microcontroller).

        [#index_1autotoc_md5]
        === Examples

        This SDK documentation contains a number of example code fragments. An index of these examples can be found <<examples_page,here>>. These examples, and any other source code included in this documentation, is Copyright © 2020 Raspberry Pi Ltd and licensed under the https://opensource.org/licenses/BSD-3-Clause[3-Clause BSD] license."""
    )
