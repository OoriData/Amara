Amara is a general-purpose web data processing library with IRI handling and MicroXML/XML processing

# Features

- **IRI (Internationalized Resource Identifier) processing** - Complete implementation for handling IRIs, including percent encoding/decoding, joining, splitting, and validation
- **MicroXML/XML parsing and processing** - Simplified XML data model based on MicroXML, with support for full XML 1.0
- **HTML5 parsing** - Parse HTML5 documents with modern html5lib-modern
- **XPath-like queries** - MicroXPath support for querying XML documents
- **Command-line tool** - `microx` for rapid XML/MicroXML processing and extraction

[![PyPI - Version](https://img.shields.io/pypi/v/amara.svg)](https://pypi.org/project/Amara)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/amara.svg)](https://pypi.org/project/Amara)

# Installation

Requires Python 3.12 or later.

```bash
pip install amara
```

Or with uv (recommended):

```bash
uv pip install amara
```

You can also install directly from the latest source version:

```bash
git clone https://github.com/OoriData/Amara.git
cd Amara
pip install -U .
```

# Quick Start

## IRI Processing

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

## XML Processing

```python
from amara.uxml import parse

SAMPLE_XML = '''<monty>
  <python spam="eggs">What do you mean "bleh"</python>
  <python ministry="abuse">But I was looking for argument</python>
</monty>'''

# Parse XML
root = parse(SAMPLE_XML)
print(root.xml_name)  # "monty"

# Access children and attributes
for child in root.xml_children:
    if hasattr(child, 'xml_attributes'):
        print(f'Element: {child.xml_name}')
        print(f'Spam attr: {child.xml_attributes.get('spam')}')
        print(f'Text: {child.xml_value}')

# Iterate through all elements
for elem in root.xml_descendants():
    print(f'Found element: {elem.xml_name}')
```

## "MicroXML?" What's that?

[MicroXML is a W3C Community Project and spec](https://dvcs.w3.org/hg/microxml/raw-file/tip/spec/microxml.html). A lot of XML veterans, including Uche, Amara's founder, had become fed up with the levels of unnecessary complexity in the XML stack, including XML Namespaces, which charges a huge technical cost in order to solve an overstated problem. Amara implements the MicroXML data model, and allows you to parse into this from tradiional XML and the MicroXML serialization.

In reality, most of the XML-like data you’ll be dealing with is full XML
1.0, so Amara package provides capabilities to parse legacy XML and reduce it to MicroXML. In many cases the biggest implication of this is that
namespace information is stripped. You can get very far by just ignoring this, and it opens up the much simpler processing encouraged by MicroXML.

## HTML5 Processing

```python
from amara.uxml import html5

HTML_DOC = '''<!DOCTYPE html>
<html>
  <head><title>Example</title></head>
  <body><p class="plain">Hello World</p></body>
</html>'''

doc = html5.parse(HTML_DOC)
print(doc.xml_name)  # "html"
```

## XPath-like Queries (MicroXPath)

```python
from amara.uxml import parse

SAMPLE_XML = '''<catalog>
  <book id="1">
    <title>Python Programming</title>
    <author>John Doe</author>
  </book>
  <book id="2">
    <title>Web Development</title>
    <author>Jane Smith</author>
  </book>
</catalog>'''

root = parse(SAMPLE_XML)

# Find all book titles
titles = root.xml_xpath('//book/title')
for title in titles:
    print(title.xml_value)

# Find book by ID
book = list(root.xml_xpath("//book[@id='2']"))
if book:
    # First child is whitespace. 2nd is the "title" element
    print(f'Found: {book[0].xml_children[1].xml_value}')
```

## Command-Line Tool

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

# Requirements

- Python 3.12+
- Dependencies: [`ply`](https://www.dabeaz.com/ply/ply.html), [`html5lib-modern`](https://github.com/ashleysommer/html5lib-modern), [`nameparser`](https://pypi.org/project/nameparser/)

# Development

<table><tr>
  <td><a href="https://oori.dev/"><img src="https://www.oori.dev/assets/branding/oori_Logo_FullColor.png" width="64" /></a></td>
  <td>Amara is primarily developed by the crew at <a href="https://oori.dev/">Oori Data</a>. We offer LLMOps, data pipelines and software engineering services around AI/LLM applications.</td>
</tr></table>

<!-- 
```bash
git clone https://github.com/OoriData/Amara.git
cd Amara
pip install -U .
``` -->

## History

Amara was originally an open source project I created, renaming and expanding on [Anobind 2003](https://www.xml.com/pub/a/2003/08/13/py-xml.html), looking to simplify and rethink XML and related technology processing, with an eye to Python. It went through a few evolutions and progress had slowed down since the late 2010s.

Quote from the [revival ticket](https://github.com/uogbuji/amara3-xml/issues/28):

> The Amara saga continues! I don't exactly remember why I decided to dead end the [Amara PyPI project](https://pypi.org/project/Amara/) when it hit 2.0, but I moved to a series of Amara 3 generation projects ([amara3.iri](https://pypi.org/project/amara3.iri/), [amara3.xml](https://pypi.org/project/amara3.xml/) & [amara3-names](https://github.com/uogbuji/amara3-names/)). Those were far more lone wolf efforts, but at [Oori Data](https://www.oori.dev/) we're seeing a lot of need for the sorts of capability that's inchoate in Amara 3.
