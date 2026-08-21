# Security Architecture

## Principles
- No hard-coded secrets or API keys in Git.
- Secure API endpoints with authentication and rate limiting where appropriate.

## Ingestion Security
- Never allow arbitrary user input to trigger unrestricted server-side URL fetching (SSRF protection).
- Validate all incoming files and handle malicious documents securely.

## Privacy
- Do not expose unnecessary personal/private information.
