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

Or with uv (recommended):

```bash
uv pip install amara
```

**Note**: This package is currently in development. For the latest features and bug fixes, you can install directly from source:

```bash
git clone https://github.com/OoriData/Amara.git
cd Amara
pip install -U .
```

## Quick Start

### IRI Processing

```python
from amara.iri import I, iri

# Create and manipulate IRIs
url = I('http://example.org/path/to/resource')
print(url.scheme)  # 'http'
print(url.host)    # 'example.org'

# Join relative paths with base URLs
joined = iri.join('http://example.org/a/b', '../c')
print(joined)  # 'http://example.org/a/c'

# Percent encoding/decoding
encoded = iri.percent_encode('hello world!')
print(encoded)  # 'hello%20world%21'
```

### XML Processing

```python
from amara.uxml import xml

SAMPLE_XML = """<monty>
  <python spam="eggs">What do you mean "bleh"</python>
  <python ministry="abuse">But I was looking for argument</python>
</monty>"""

# Parse XML
builder = xml.treebuilder()
root = builder.parse(SAMPLE_XML)
print(root.xml_name)  # "monty"

# Access children and attributes
for child in root.xml_children:
    if hasattr(child, 'xml_attributes'):
        print(f"Element: {child.xml_name}")
        print(f"Spam attr: {child.xml_attributes.get('spam')}")
        print(f"Text: {child.xml_text}")

# Iterate through all elements
for elem in root.xml_iter():
    print(f"Found element: {elem.xml_name}")
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
print(doc.xml_name)  # "html"
```

### XPath-like Queries

```python
from amara.uxpath import xpath

SAMPLE_XML = """<catalog>
  <book id="1">
    <title>Python Programming</title>
    <author>John Doe</author>
  </book>
  <book id="2">
    <title>Web Development</title>
    <author>Jane Smith</author>
  </book>
</catalog>"""

builder = xml.treebuilder()
root = builder.parse(SAMPLE_XML)

# Find all book titles
titles = xpath.select(root, '//book/title')
for title in titles:
    print(title.xml_text)

# Find book by ID
book = xpath.select(root, "//book[@id='2']")
if book:
    print(f"Found: {book[0].xml_children[0].xml_text}")
```

### Command-Line Tool

The `microx` command provides powerful XML/MicroXML querying and processing:

```bash
# Extract elements by name
microx file.xml --match=item

# XPath-like expressions
microx file.xml --expr="//item[@id='2']"

# Extract text content from specific elements
microx file.xml --match=name --foreach="text()"

# Process multiple files
microx *.xml --match=title --foreach="text()"

# Pretty-print XML
microx file.xml --pretty

# Convert to MicroXML
microx file.xml --microxml
```

For more options, run:
```bash
microx --help
```

## Requirements

- Python 3.12+
- Dependencies: [`ply`](https://www.dabeaz.com/ply/ply.html), [`html5lib-modern`](https://github.com/ashleysommer/html5lib-modern), [`nameparser`](https://pypi.org/project/nameparser/)

## Development

This project is actively developed by [Oori Data](https://www.oori.dev/). For development setup:

```bash
git clone https://github.com/OoriData/Amara.git
cd Amara
pip install -U .
```

## History

Amara was originally an open source project I created, renaming and expanding on [Anobind 2003](https://www.xml.com/pub/a/2003/08/13/py-xml.html), looking to simplify and rethink XML and related technology processing. It went through a few evolutions and progress had slowed down since the late 2010s.

Quote from the [revival ticket](https://github.com/uogbuji/amara3-xml/issues/28):

> The Amara saga continues! I don't exactly remember why I decided to dead end the [Amara PyPI project](https://pypi.org/project/Amara/) when it hit 2.0, but I moved to a series of Amara 3 generation projects ([amara3.iri](https://pypi.org/project/amara3.iri/), [amara3.xml](https://pypi.org/project/amara3.xml/) & [amara3-names](https://github.com/uogbuji/amara3-names/)). Those were far more lone wolf efforts, but at [Oori Data](https://www.oori.dev/) we're seeing a lot of need for the sorts of capability that's inchoate in Amara 3.

