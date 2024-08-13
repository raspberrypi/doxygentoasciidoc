# doxygentoasciidoc: A Doxygen > Asciidoc Converter

This project converts doxygen XML output to asciidoc.

Allowed args:

`-f`: the full path to the file to be converted

`-o`: the full path the the output file (will print to STDOUT if not specified)

`-c`: process a node other than `doxygenindex`

The following attributes from the XML will be preserved in the generated asciidoc: role, tag, type.
