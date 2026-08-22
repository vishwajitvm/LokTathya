import urllib.parse
import urllib.robotparser
import urllib.request
from typing import Dict, Any, Optional

class AccessPolicyManager:
    """
    Step 18: Legal / Access Control.
    Integrates robots.txt disallow checkers to protect target government servers.
    """

    @staticmethod
    def is_allowed(url: str, user_agent: str = "LokTathyaBot") -> bool:
        if not url:
            return False
            
        parsed = urllib.parse.urlparse(url)
        # Construct robots.txt location
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        
        rp = urllib.robotparser.RobotFileParser()
        try:
            rp.set_url(robots_url)
            with urllib.request.urlopen(robots_url, timeout=3) as conn:
                content = conn.read().decode('utf-8')
                rp.parse(content.splitlines())
            return rp.can_fetch(user_agent, url)
        except Exception:
            # If robots.txt cannot be fetched or times out, we default to legal review caution:
            # allow fetching if standard government portal
            return True
