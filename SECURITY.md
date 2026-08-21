# Security Policy

We take security seriously at LokTathya. As a national civic infrastructure project, maintaining the security, integrity, and trust of the platform is our highest priority.

## Supported Versions

Only the latest active release of LokTathya is currently supported with security updates.

| Version | Supported |
| ------- | --------- |
| 1.0.x   | Yes       |
| < 1.0   | No        |

## Reporting a Vulnerability

If you discover a security vulnerability in LokTathya, please do **not** open a public GitHub issue. Public disclosures can expose sensitive public records or deployment environments to exploitation before a fix is available.

Instead, please report the vulnerability through the following process:

1. **Email the Report**: Send a detailed description of the vulnerability, reproduction steps, and potential impacts to `security@loktathya.org`.
2. **Acknowledgement**: A project maintainer will acknowledge receipt of your report within 24 hours.
3. **Assessment & Patch**: We will evaluate the report and aim to patch the issue within 7 days.
4. **Coordination**: We will coordinate with you regarding the public announcement and credit.

## Security Controls & Best Practices

1. **Network Boundary Isolation**: Database instances (PostgreSQL, Redis, MinIO) must always remain isolated on the internal virtual Docker network (`loktathya_net`) and must never map their ports to the external public interface of the host machine.
2. **Environment Secrets**: Do not check-in configuration credentials or `.env` files. Access must be managed via production orchestration configurations or securely injected secrets.
3. **Audit Comments**: SQL statements in database transactions must propagate `X-Request-ID` variables as SQL comments (`/* request_id: <id> */`) for transaction tracing.
