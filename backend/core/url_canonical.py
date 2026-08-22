import urllib.parse
import re

class URLCanonicalizer:
    """
    Step 3: URL Canonicalization.
    Normalises schemas, hostnames, ports, duplicate slashes, fragments, and tracking query params.
    """

    TRACKING_PARAMS = {
        "utm_source", "utm_medium", "utm_campaign", "utm_term",
        "utm_content", "fbclid", "gclid", "sessionid"
    }

    @classmethod
    def canonicalize(cls, url: str) -> str:
        if not url:
            return ""
            
        # Clean white space
        url = url.strip()
        
        # Parse URL
        parsed = urllib.parse.urlparse(url)
        
        # Normalize scheme and netloc to lowercase
        scheme = parsed.scheme.lower()
        netloc = parsed.netloc.lower()
        
        # Remove default ports
        if scheme == "http" and netloc.endswith(":80"):
            netloc = netloc[:-3]
        elif scheme == "https" and netloc.endswith(":443"):
            netloc = netloc[:-4]
            
        # Normalize duplicate slashes in path
        path = re.sub(r'/{2,}', '/', parsed.path)
        
        # Remove trailing slash if path is not root
        if len(path) > 1 and path.endswith("/"):
            path = path[:-1]
            
        # Clean query parameters: strip UTM/tracking keys
        query_params = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
        filtered_params = [
            (k, v) for k, v in query_params
            if k.lower() not in cls.TRACKING_PARAMS
        ]
        
        # Rebuild query string
        query = urllib.parse.urlencode(sorted(filtered_params))
        
        # Fragments must be discarded
        fragment = ""
        
        # Re-construct canonical URL
        canonical = urllib.parse.urlunparse((scheme, netloc, path, parsed.params, query, fragment))
        return canonical
