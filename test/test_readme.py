'''
Test suite to verify that all Python code examples in README.md work correctly.
Helps prevent regressions when the API changes.
'''

import pytest
from amara.iri import I, iri
from amara.uxml import parse
from amara.uxml import html5


class TestIRIProcessing:
    '''Test IRI Processing examples from README.md'''

    def test_create_and_manipulate_iris(self):
        '''Test: Create and manipulate IRIs'''
        url = I('http://example.org/path/to/resource')
        assert url.scheme == 'http'
        assert url.host == 'example.org'

    def test_join_relative_paths(self):
        '''Test: Join relative paths with base URLs'''
        joined = iri.join('http://example.org/a/b', '../c')
        assert str(joined) == 'http://example.org/a/c'

    def test_percent_encoding(self):
        '''Test: Percent encoding/decoding'''
        encoded = iri.percent_encode('hello world!')
        assert encoded == 'hello%20world%21'


class TestXMLProcessing:
    '''Test XML Processing examples from README.md'''

    SAMPLE_XML = '''<monty>
  <python spam="eggs">What do you mean "bleh"</python>
  <python ministry="abuse">But I was looking for argument</python>
</monty>'''

    def test_parse_xml(self):
        '''Test: Parse XML'''
        root = parse(self.SAMPLE_XML)
        assert root.xml_name == 'monty'

    def test_access_children_and_attributes(self):
        '''Test: Access children and attributes'''
        root = parse(self.SAMPLE_XML)
        children = list(root.xml_children)
        # Filter to only element children (skip text nodes)
        element_children = [ch for ch in children if hasattr(ch, 'xml_attributes')]
        
        assert len(element_children) == 2
        assert element_children[0].xml_name == 'python'
        assert element_children[0].xml_attributes.get('spam') == 'eggs'
        assert element_children[1].xml_name == 'python'
        assert element_children[1].xml_attributes.get('ministry') == 'abuse'

    def test_iterate_through_all_elements(self):
        '''Test: Iterate through all elements'''
        root = parse(self.SAMPLE_XML)
        elements = list(root.xml_descendants())
        element_names = [elem.xml_name for elem in elements]
        # xml_descendants() returns only descendant elements, not the root itself
        # Should find both python elements
        assert element_names.count('python') == 2
        assert len(elements) == 2


class TestHTML5Processing:
    '''Test HTML5 Processing examples from README.md'''

    HTML_DOC = '''<!DOCTYPE html>
<html>
  <head><title>Example</title></head>
  <body><p class="plain">Hello World</p></body>
</html>'''

    def test_parse_html5(self):
        '''Test: Parse HTML5'''
        doc = html5.parse(self.HTML_DOC)
        assert doc.xml_name == 'html'


class TestXPathQueries:
    '''Test XPath-like Queries (MicroXPath) examples from README.md'''

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

    def test_find_all_book_titles(self):
        '''Test: Find all book titles'''
        root = parse(self.SAMPLE_XML)
        titles = root.xml_xpath('//book/title')
        title_values = [title.xml_value for title in titles]
        assert 'Python Programming' in title_values
        assert 'Web Development' in title_values

    def test_find_book_by_id(self):
        '''Test: Find book by ID'''
        root = parse(self.SAMPLE_XML)
        book = list(root.xml_xpath("//book[@id='2']"))
        assert len(book) > 0
        # Find the title element among children (skip whitespace text nodes)
        title_elem = None
        for child in book[0].xml_children:
            if hasattr(child, 'xml_name') and child.xml_name == 'title':
                title_elem = child
                break
        assert title_elem is not None
        assert title_elem.xml_value == 'Web Development'
