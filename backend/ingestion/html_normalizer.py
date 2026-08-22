import hashlib
from typing import Dict, Any, List, Optional
try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

class HTMLNormalizer:
    """
    Priority 2 - HTML Normalization Pipeline.
    Strips boilerplate (nav, footers, scripts) to produce a stable content representation
    for deterministic change detection and hashing.
    """

    NOISE_TAGS = [
        'script', 'style', 'noscript', 'meta', 'link', 
        'nav', 'footer', 'header', 'aside', 'iframe',
        'button', 'form'
    ]
    
    NOISE_CLASSES = [
        'nav', 'navigation', 'footer', 'header', 'sidebar',
        'cookie', 'banner', 'ads', 'promo', 'menu', 'social'
    ]

    def __init__(self, raw_html: str):
        self.raw_html = raw_html
        if BeautifulSoup:
            self.soup = BeautifulSoup(raw_html, 'html.parser')
        else:
            self.soup = None
            
    def normalize(self) -> Dict[str, Any]:
        """
        Produce a normalized text representation and its SHA-256 hash.
        """
        if not self.soup:
            return {"hash": hashlib.sha256(self.raw_html.encode('utf-8')).hexdigest(), "text": self.raw_html}
            
        # 1. Remove noise tags
        for tag in self.NOISE_TAGS:
            for el in self.soup.find_all(tag):
                el.decompose()
                
        # 2. Remove noise classes/ids
        for element in self.soup.find_all(class_=lambda x: x and any(n in x.lower() for n in self.NOISE_CLASSES)):
            element.decompose()
            
        # 3. Extract text cleanly
        text_content = self.soup.get_text(separator='\n', strip=True)
        
        # 4. Hash normalized content
        content_hash = hashlib.sha256(text_content.encode('utf-8')).hexdigest()
        
        return {
            "hash": content_hash,
            "text": text_content,
            "title": self._extract_title()
        }
        
    def _extract_title(self) -> Optional[str]:
        if self.soup and self.soup.title:
            return self.soup.title.string.strip()
        return None

    def extract_tables(self) -> List[Dict[str, Any]]:
        """
        Extract structural tables from the normalized HTML.
        """
        if not self.soup:
            return []
            
        tables = []
        for idx, table in enumerate(self.soup.find_all('table')):
            caption = table.caption.text.strip() if table.caption else None
            
            headers = []
            for th in table.find_all('th'):
                headers.append(th.get_text(strip=True))
                
            rows = []
            for tr in table.find_all('tr'):
                cells = [td.get_text(strip=True) for td in tr.find_all('td')]
                if cells:
                    rows.append(cells)
                    
            if headers or rows:
                tables.append({
                    "table_index": idx,
                    "caption": caption,
                    "headers": headers,
                    "rows": rows
                })
                
        return tables
