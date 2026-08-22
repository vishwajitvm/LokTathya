from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
import re

class URLCanonicalizer:
    """
    Priority 2A: URL Canonicalization Engine.
    Strips noise, preserves meaningful parameters, handles tracking params,
    and normalizes structure to determine true webpage identity.
    """
    
    # Common tracking parameters to unconditionally strip
    TRACKING_PARAMS = {
        'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
        'gclid', 'fbclid', 'msclkid', 'mc_eid', '_hsenc', '_hsmi',
        'ref', 'source', 'src'
    }

    # Parameters that control session state but not content
    SESSION_PARAMS = {
        'session_id', 'sid', 'PHPSESSID', 'jsessionid'
    }

    @staticmethod
    def canonicalize(url: str) -> str:
        """
        Produce the canonical form of a given URL.
        """
        if not url:
            return url

        # Ensure http/https
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url

        parsed = urlparse(url)
        
        # Lowercase scheme and netloc
        scheme = parsed.scheme.lower()
        netloc = parsed.netloc.lower()
        
        # Remove default ports
        if scheme == 'http' and netloc.endswith(':80'):
            netloc = netloc[:-3]
        elif scheme == 'https' and netloc.endswith(':443'):
            netloc = netloc[:-4]
            
        # Normalize path
        path = parsed.path
        # Collapse multiple slashes
        path = re.sub(r'//+', '/', path)
        # Remove trailing slash
        if path == '/':
            path = ''
        elif path.endswith('/'):
            path = path[:-1]
            
        # Filter query params
        query_params = parse_qsl(parsed.query, keep_blank_values=True)
        filtered_params = []
        for k, v in query_params:
            if k.lower() not in URLCanonicalizer.TRACKING_PARAMS and k.lower() not in URLCanonicalizer.SESSION_PARAMS:
                filtered_params.append((k, v))
                
        # Sort query params for deterministic output
        filtered_params.sort(key=lambda x: x[0])
        query = urlencode(filtered_params)
        
        # We explicitly discard fragments (parsed.fragment) as they are client-side navigation
        return urlunparse((scheme, netloc, path, parsed.params, query, ''))
