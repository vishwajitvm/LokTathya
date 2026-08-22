import re
from typing import List, Dict, Any
from urllib.parse import urljoin
try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

class DocumentLinkExtractor:
    """
    Priority 2A: Extracts attached documents and API links from government pages.
    """
    
    DOCUMENT_EXTENSIONS = {
        '.pdf': 'PDF',
        '.csv': 'CSV',
        '.xls': 'XLS',
        '.xlsx': 'XLSX',
        '.xlsm': 'XLSM',
        '.zip': 'ZIP',
        '.geojson': 'GEOJSON',
        '.kml': 'KML',
        '.kmz': 'KMZ',
        '.json': 'JSON',
        '.xml': 'XML'
    }

    def __init__(self, raw_html: str, base_url: str):
        self.raw_html = raw_html
        self.base_url = base_url
        if BeautifulSoup:
            self.soup = BeautifulSoup(raw_html, 'html.parser')
        else:
            self.soup = None

    def extract_links(self) -> List[Dict[str, Any]]:
        discovered_links = []
        
        if self.soup:
            tags = [(a['href'], a.get_text(strip=True)) for a in self.soup.find_all('a', href=True)]
        else:
            # Fallback regex if bs4 is missing in docker
            tags = []
            for match in re.finditer(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', self.raw_html, re.IGNORECASE | re.DOTALL):
                href = match.group(1).strip()
                text = re.sub(r'<[^>]+>', '', match.group(2)).strip() # strip inner html
                tags.append((href, text))

        for href, link_text in tags:
            if not href or href.startswith('javascript:') or href.startswith('mailto:') or href.startswith('tel:'):
                continue
                
            absolute_url = urljoin(self.base_url, href)
            
            lower_href = href.lower()
            detected_type = "RELATED_PAGE"
            
            for ext, doc_type in self.DOCUMENT_EXTENSIONS.items():
                if lower_href.endswith(ext) or (f"{ext}?" in lower_href):
                    detected_type = doc_type
                    break
            
            if '/api/' in lower_href or lower_href.endswith('.json'):
                detected_type = "API"

            discovered_links.append({
                "url": absolute_url,
                "text": link_text,
                "type": detected_type
            })
            
        return discovered_links
