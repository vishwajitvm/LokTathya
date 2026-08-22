from core.url_canonical import URLCanonicalizer

def test_url_canonicalizer_edge_cases():
    assert URLCanonicalizer.canonicalize("HTTP://GOV.IN:80/path//subpath/") == "http://gov.in/path/subpath"
    assert URLCanonicalizer.canonicalize("https://gov.in/index.html?utm_source=feed&id=123#section") == "https://gov.in/index.html?id=123"
    assert URLCanonicalizer.canonicalize("https://gov.in:443/") == "https://gov.in/"
