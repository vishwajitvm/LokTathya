from core.url_utils import URLCanonicalizer

def test_canonicalize_basic():
    assert URLCanonicalizer.canonicalize("http://gov.in/") == "http://gov.in"
    assert URLCanonicalizer.canonicalize("https://gov.in:443/data//") == "https://gov.in/data"

def test_canonicalize_tracking_params():
    url = "https://gov.in/budget?utm_source=twitter&page=2&utm_medium=social"
    canonical = URLCanonicalizer.canonicalize(url)
    assert canonical == "https://gov.in/budget?page=2"

def test_canonicalize_fragment():
    url = "https://gov.in/policy#section-3"
    canonical = URLCanonicalizer.canonicalize(url)
    assert canonical == "https://gov.in/policy"

def test_canonicalize_sorting():
    url = "https://gov.in/search?b=2&a=1"
    canonical = URLCanonicalizer.canonicalize(url)
    assert canonical == "https://gov.in/search?a=1&b=2"
