"""
Tests for IRI reference attribute access (scheme, authority, path, query, fragment, etc.)

These tests ensure that all components from split_uri_ref are accessible
as attributes on iriref objects.
"""
import pytest
from amara.iri import I, split_uri_ref, split_authority


# Test cases for basic IRI component attributes
# Format: (iri_string, expected_components_dict)
iri_attr_test_cases = [
    # Full URI with all components
    (
        'http://user:pass@example.org:8080/a/b/c?x=1&y=2#frag',
        {
            'scheme': 'http',
            'authority': 'user:pass@example.org:8080',
            'auth': 'user:pass@example.org:8080',
            'path': '/a/b/c',
            'query': 'x=1&y=2',
            'fragment': 'frag',
            'frag': 'frag',
            'userinfo': 'user:pass',
            'host': 'example.org',
            'port': '8080',
        }
    ),
    # Simple HTTP URI
    (
        'http://example.org/a/b/c',
        {
            'scheme': 'http',
            'authority': 'example.org',
            'auth': 'example.org',
            'path': '/a/b/c',
            'query': None,
            'fragment': None,
            'frag': None,
            'userinfo': None,
            'host': 'example.org',
            'port': None,
        }
    ),
    # URI with query and fragment
    (
        'http://example.org/a/b/c?x=1#frag',
        {
            'scheme': 'http',
            'authority': 'example.org',
            'path': '/a/b/c',
            'query': 'x=1',
            'fragment': 'frag',
            'host': 'example.org',
        }
    ),
    # URI with port only
    (
        'http://example.org:80/path',
        {
            'scheme': 'http',
            'authority': 'example.org:80',
            'path': '/path',
            'host': 'example.org',
            'port': '80',
        }
    ),
    # URI with userinfo only
    (
        'http://user@example.org/path',
        {
            'scheme': 'http',
            'authority': 'user@example.org',
            'path': '/path',
            'userinfo': 'user',
            'host': 'example.org',
            'port': None,
        }
    ),
    # Relative URI (no scheme)
    (
        '/a/b/c?x=1#frag',
        {
            'scheme': None,
            'authority': None,
            'auth': None,
            'path': '/a/b/c',
            'query': 'x=1',
            'fragment': 'frag',
            'userinfo': None,
            'host': None,
            'port': None,
        }
    ),
    # URI with empty path
    (
        'http://example.org?query#frag',
        {
            'scheme': 'http',
            'authority': 'example.org',
            'path': '',
            'query': 'query',
            'fragment': 'frag',
            'host': 'example.org',
        }
    ),
    # URI with empty query
    (
        'http://example.org/path?#frag',
        {
            'scheme': 'http',
            'authority': 'example.org',
            'path': '/path',
            'query': '',
            'fragment': 'frag',
            'host': 'example.org',
        }
    ),
    # URI with empty fragment
    (
        'http://example.org/path?query#',
        {
            'scheme': 'http',
            'authority': 'example.org',
            'path': '/path',
            'query': 'query',
            'fragment': '',
            'frag': '',
            'host': 'example.org',
        }
    ),
    # HTTPS URI
    (
        'https://secure.example.org:443/api/v1/data',
        {
            'scheme': 'https',
            'authority': 'secure.example.org:443',
            'path': '/api/v1/data',
            'host': 'secure.example.org',
            'port': '443',
        }
    ),
    # File URI (empty authority component)
    (
        'file:///path/to/file.txt',
        {
            'scheme': 'file',
            'authority': '',  # Empty string, not None, because // indicates authority exists
            'path': '/path/to/file.txt',
            'host': None,  # Empty authority means no host
        }
    ),
    # Mailto URI
    (
        'mailto:user@example.org?subject=Hello',
        {
            'scheme': 'mailto',
            'authority': None,
            'path': 'user@example.org',
            'query': 'subject=Hello',
            'host': None,
        }
    ),
]


@pytest.mark.parametrize('iri_string,expected', iri_attr_test_cases)
def test_iri_attributes(iri_string, expected):
    """Test that all IRI components are accessible as attributes"""
    url = I(iri_string)
    
    # Test all expected attributes
    for attr_name, expected_value in expected.items():
        actual_value = getattr(url, attr_name)
        assert actual_value == expected_value, \
            f"Attribute {attr_name} mismatch for {iri_string}: expected {expected_value!r}, got {actual_value!r}"


def test_iri_attributes_match_split_uri_ref():
    """Test that attributes match the output of split_uri_ref"""
    test_uris = [
        'http://example.org/a/b/c',
        'http://user:pass@example.org:8080/path?query#frag',
        'https://secure.example.org/api',
        '/relative/path?q=1#f',
        'file:///absolute/path',
    ]
    
    for uri_string in test_uris:
        url = I(uri_string)
        scheme, auth, path, query, frag = split_uri_ref(str(url))
        
        assert url.scheme == scheme, f"scheme mismatch for {uri_string}"
        assert url.authority == auth, f"authority mismatch for {uri_string}"
        assert url.auth == auth, f"auth alias mismatch for {uri_string}"
        assert url.path == path, f"path mismatch for {uri_string}"
        assert url.query == query, f"query mismatch for {uri_string}"
        assert url.fragment == frag, f"fragment mismatch for {uri_string}"
        assert url.frag == frag, f"frag alias mismatch for {uri_string}"


def test_iri_authority_components():
    """Test that authority subcomponents (userinfo, host, port) are correctly extracted"""
    test_cases = [
        ('http://example.org/path', None, 'example.org', None),
        ('http://example.org:80/path', None, 'example.org', '80'),
        ('http://user@example.org/path', 'user', 'example.org', None),
        ('http://user:pass@example.org:8080/path', 'user:pass', 'example.org', '8080'),
        ('http://example.org/path', None, 'example.org', None),
        ('/relative/path', None, None, None),
    ]
    
    for uri_string, expected_userinfo, expected_host, expected_port in test_cases:
        url = I(uri_string)
        userinfo, host, port = split_authority(url.authority) if url.authority else (None, None, None)
        
        assert url.userinfo == userinfo, \
            f"userinfo mismatch for {uri_string}: expected {userinfo!r}, got {url.userinfo!r}"
        assert url.host == host, \
            f"host mismatch for {uri_string}: expected {host!r}, got {url.host!r}"
        assert url.port == port, \
            f"port mismatch for {uri_string}: expected {port!r}, got {url.port!r}"


def test_iri_attributes_caching():
    """Test that attributes are cached and don't cause repeated parsing"""
    url = I('http://example.org/a/b/c?x=1#frag')
    
    # Access attributes multiple times
    scheme1 = url.scheme
    scheme2 = url.scheme
    host1 = url.host
    host2 = url.host
    
    # They should be the same (cached)
    assert scheme1 == scheme2 == 'http'
    assert host1 == host2 == 'example.org'
    
    # Verify the cached components are accessible
    assert hasattr(url, '_cached_components')
    assert hasattr(url, '_cached_authority_parts')


def test_iri_attributes_with_call():
    """Test that attributes work correctly after using the call syntax"""
    base = I('http://example.org/')
    url = base('a/b/c?x=1#frag')
    
    assert url.scheme == 'http'
    assert url.authority == 'example.org'
    assert url.path == '/a/b/c'
    assert url.query == 'x=1'
    assert url.fragment == 'frag'
    assert url.host == 'example.org'


def test_iri_attributes_edge_cases():
    """Test edge cases for IRI attributes"""
    # Empty string (should be valid per RFC 3986)
    url = I('')
    assert url.scheme is None
    assert url.authority is None
    assert url.path == ''
    
    # Fragment only
    url = I('#fragment')
    assert url.scheme is None
    assert url.fragment == 'fragment'
    
    # Query only (relative)
    url = I('?query=value')
    assert url.scheme is None
    assert url.query == 'query=value'
    
    # Authority only
    url = I('//example.org')
    assert url.scheme is None
    assert url.authority == 'example.org'
    assert url.host == 'example.org'


if __name__ == '__main__':
    pytest.main([__file__])

