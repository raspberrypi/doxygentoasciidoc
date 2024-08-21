# doxygentoasciidoc: A Doxygen to AsciiDoc Converter

```
usage: doxygentoasciidoc [-h] [-o OUTPUT] [-c] file

Convert Doxygen XML to AsciiDoc

positional arguments:
  file                  The path of the Doxygen XML file to convert

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Write to file instead of stdout
  -c, --child           Is NOT the root index file
```

## Development

Install the development dependencies:

```console
$ pip install -r dev.txt
```

Run the test suite:

```console
$ pytest
```

Ensure code is formatted consistently:

```console
$ black --check .
```

Ensure code passes linting:

```console
$ pylint doxygentoasciidoc
```
