# Amara

General-purpose web data processing library with IRI handling and MicroXML/XML processing

## Features

- **IRI (Internationalized Resource Identifier) processing** - Complete implementation for handling IRIs, including percent encoding/decoding, joining, splitting, and validation
- **MicroXML/XML parsing and processing** - Simplified XML data model based on MicroXML, with support for full XML 1.0
- **HTML5 parsing** - Parse HTML5 documents with modern html5lib-modern
- **XPath-like queries** - MicroXPath support for querying XML documents
- **Command-line tool** - `microx` for rapid XML/MicroXML processing and extraction

## Installation

Requires Python 3.12 or later.

```bash
pip install amara
```

Or with uv:

```bash
uv pip install amara
```

## Quick Start

### IRI Processing

```python
from amara.iri import I, iri

# Create and manipulate IRIs
url = I('http://example.org/path/to/resource')
joined = iri.join('http://example.org/a/b', '../c')
# Result: 'http://example.org/a/c'
```

### XML Processing

```python
from amara.uxml import xml

SAMPLE_XML = """<monty>
  <python spam="eggs">What do you mean "bleh"</python>
  <python ministry="abuse">But I was looking for argument</python>
</monty>"""

builder = xml.treebuilder()
root = builder.parse(SAMPLE_XML)
print(root.xml_name)  # "monty"

# Access children
for child in root.xml_children:
    if hasattr(child, 'xml_attributes'):
        print(child.xml_attributes.get('spam'))
```

### HTML5 Processing

```python
from amara.uxml import html5

HTML_DOC = """<!DOCTYPE html>
<html>
  <head><title>Example</title></head>
  <body><p class="plain">Hello World</p></body>
</html>"""

doc = html5.parse(HTML_DOC)
```

### Command-Line Tool

The `microx` command provides powerful XML/MicroXML querying:

```bash
# Extract elements by name
microx file.xml --match=item

# XPath-like expressions
microx file.xml --expr="//item[@id='2']"

# Extract text content
microx file.xml --match=name --foreach="text()"
```



# History

Amara was originally an open source project I created, renaming and expanding on [Anobind 2003](https://www.xml.com/pub/a/2003/08/13/py-xml.html), looking to simplify and rethink XML and related technology processing. It went through a few evolutions and progress had slowed down since the late 2010s.

Quote from the [revival ticket](https://github.com/uogbuji/amara3-xml/issues/28):

> The Amara saga continues! I don't exactly remember why I decided to dead end the [Amara PyPI project](https://pypi.org/project/Amara/) when it hit 2.0, but I moved to a series of Amara 3 generation projects ([amara3.iri](https://pypi.org/project/amara3.iri/), [amara3.xml](https://pypi.org/project/amara3.xml/) & [amara3-names](https://github.com/uogbuji/amara3-names/)). Those were far more lone wolf efforts, but at [Oori Data](https://www.oori.dev/) we're seeing a lot of need for the sorts of capability that's inchoate in Amara 3.

