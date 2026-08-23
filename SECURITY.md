# Security Policy

LokTathya treats security, privacy, data integrity, and service availability as core engineering requirements. As a civic infrastructure platform, we follow a defense-in-depth approach across the application, APIs, data layer, infrastructure, authentication, and deployment pipeline.

We welcome responsible security research and encourage security researchers, contributors, and users to report vulnerabilities privately so they can be investigated and remediated before public disclosure.

---

## Supported Versions

Security fixes are currently provided for the latest active release and the actively maintained development branch.

| Version                         | Supported |
| ------------------------------- | --------- |
| Latest stable release           | Yes       |
| `development`                   | Yes       |
| Older releases                  | No        |
| Unreleased / abandoned branches | No        |

Security support may be discontinued for older versions when a new major release replaces them.

---

## Reporting a Vulnerability

### Do Not Open a Public Issue

If you discover a potential security vulnerability, **do not create a public GitHub issue, pull request, discussion, or social-media post**.

Public disclosure before remediation could expose citizen-facing services, public records, credentials, infrastructure, or internal systems to unnecessary risk.

### Private Security Report

Send vulnerability reports to:

`security@loktathya.org`

Please include as much of the following information as possible:

* Vulnerability title and severity
* Affected component or endpoint
* Affected version, branch, or commit
* Detailed vulnerability description
* Reproduction steps or proof of concept
* Expected and actual behavior
* Potential security impact
* Required privileges or attack prerequisites
* Relevant request/response examples
* Screenshots or logs where appropriate
* Suggested remediation, if available

Please **never include real passwords, API keys, access tokens, private credentials, personal data, or production secrets** in a security report.

---

## Security Response Process

Security reports will follow the general process below:

1. **Acknowledgement**
   The security team aims to acknowledge valid reports within **24 hours**.

2. **Initial Assessment**
   The report will be evaluated for validity, severity, affected components, exploitability, and potential impact.

3. **Containment**
   Where necessary, affected functionality, credentials, endpoints, or infrastructure may be temporarily restricted while investigation takes place.

4. **Remediation**
   A security fix will be developed, reviewed, tested, and validated before deployment.

5. **Release**
   A patched release or security update will be published where applicable.

6. **Disclosure Coordination**
   Public disclosure will be coordinated with the reporter whenever appropriate, while avoiding unnecessary exposure of exploit details or sensitive information.

Our target is to address confirmed critical vulnerabilities as quickly as operationally possible and generally aim for remediation within **7 days**, depending on severity and complexity.

---

## Severity Classification

Security issues are evaluated based on exploitability, affected assets, required privileges, and potential impact.

| Severity | Examples                                                                                       |
| -------- | ---------------------------------------------------------------------------------------------- |
| Critical | Remote code execution, authentication bypass, unrestricted access to sensitive systems or data |
| High     | Privilege escalation, significant authorization bypass, sensitive data exposure                |
| Medium   | Limited data exposure, CSRF, meaningful API abuse, security-control bypass                     |
| Low      | Minor information disclosure, hardening issues, low-impact weaknesses                          |

Severity may be adjusted after technical investigation.

---

# Security Controls

## 1. Authentication & Authorization

LokTathya services must enforce authentication and authorization consistently across protected resources.

* Authentication must be required for protected API endpoints.
* Authorization must be enforced server-side.
* Client-side authorization checks must never be considered sufficient.
* Users must only access resources they are authorized to access.
* Administrative functionality must require appropriate privileges.
* Privilege escalation through manipulated request parameters must be prevented.
* Authentication tokens must have appropriate expiration and validation.
* Sensitive authentication material must never be logged.
* Passwords must never be stored in plaintext.
* Authentication failures should be handled without unnecessarily revealing account information.

---

## 2. API Security

The FastAPI backend must treat all incoming requests as untrusted input.

API endpoints should implement:

* Strict request validation.
* Pydantic schema validation.
* Authentication and authorization checks.
* Rate limiting for sensitive or abuse-prone endpoints.
* Appropriate HTTP security headers.
* Request-size limits.
* Safe error handling.
* Consistent status codes.
* Protection against injection attacks.
* Protection against unauthorized object access.
* Input sanitization where required.
* Pagination and resource limits for large queries.

Internal implementation details, stack traces, database errors, credentials, and infrastructure information must not be exposed through production API responses.

---

## 3. Database Security

LokTathya uses PostgreSQL as a primary relational data store.

Database security requirements include:

* Database credentials must never be committed to Git.
* Production databases must not be publicly exposed.
* Application users should receive only the minimum database privileges required.
* Parameterized queries or ORM-safe query mechanisms must be used.
* Raw SQL must be reviewed for injection risks.
* Database migrations must be reviewed before production deployment.
* Sensitive database operations must be auditable.
* Backups must be protected against unauthorized access.
* Database connections must use secure credentials and appropriate transport security in production.

### Transaction Tracing

Database transactions should propagate the request correlation identifier through SQL comments where supported:

```sql
/* request_id: <request-id> */
```

This allows database activity to be correlated with application-level audit and observability data without exposing sensitive request content.

---

## 4. Redis Security

Redis is treated as an internal infrastructure component.

* Redis must not be exposed directly to the public internet.
* Redis authentication must be enabled where required by the deployment environment.
* Production credentials must be injected securely.
* Sensitive information must not be stored in Redis unnecessarily.
* Redis data and queues must be protected from unauthorized application access.
* Queue payloads must not contain unnecessary sensitive information.

---

## 5. MinIO & Object Storage Security

MinIO is used for object and file storage and must remain protected as an internal infrastructure service.

* MinIO management interfaces must not be publicly exposed without appropriate security controls.
* Access keys and secret keys must never be committed to the repository.
* Buckets should use the least-privilege access model.
* Public object access must be explicitly required and reviewed.
* Uploaded files must be validated before processing.
* File names and paths must not be trusted as filesystem paths.
* Upload size limits must be enforced.
* Executable or dangerous file types should be rejected where not required.
* Stored objects must not expose sensitive metadata unnecessarily.

---

## 6. Docker & Network Isolation

LokTathya services are deployed using containerized infrastructure.

The following infrastructure services must remain isolated from the public network:

* PostgreSQL
* Redis
* MinIO
* Celery workers
* Internal service endpoints

The internal Docker network:

```text
loktathya_net
```

should be used for service-to-service communication.

Only explicitly required public-facing services should publish host ports.

A production deployment should follow a topology similar to:

```text
Internet
   |
   v
Reverse Proxy / Gateway
   |
   +---- Next.js Frontend
   |
   +---- FastAPI API
             |
             +---- PostgreSQL
             +---- Redis
             +---- MinIO
             +---- Celery Worker
```

Internal services should never be directly reachable from the public internet.

---

## 7. Environment Variables & Secrets

Secrets must never be committed to the repository.

This includes:

* Database passwords
* API keys
* JWT signing secrets
* OAuth client secrets
* MinIO credentials
* Redis credentials
* Cloud credentials
* Encryption keys
* Third-party service credentials
* Private certificates
* Production `.env` files

Use environment variables or a dedicated secret-management system for production deployments.

The repository should contain only safe example configuration such as:

```text
.env.example
```

Example files must contain placeholders rather than real credentials.

If a secret is accidentally committed:

1. Revoke or rotate it immediately.
2. Remove it from active configuration.
3. Investigate potential exposure.
4. Remove it from repository history where appropriate.
5. Document the incident internally.

Removing a secret from the latest commit alone does **not** make a previously exposed credential safe.

---

## 8. Logging & Observability

LokTathya uses application and infrastructure observability to detect operational and security issues.

Logs must not contain:

* Passwords
* Authentication tokens
* API keys
* Session secrets
* Private keys
* Unnecessary personal information
* Full sensitive request bodies

Logs should contain appropriate correlation information such as:

```text
request_id
timestamp
service
endpoint
status
latency
```

Security-relevant events should be traceable without exposing sensitive information.

---

## 9. Request Tracing

Every externally initiated request should receive a unique request identifier where applicable.

Example:

```text
X-Request-ID: <unique-request-id>
```

The identifier should propagate through relevant application components, workers, database operations, and observability systems.

Request identifiers must be treated as correlation metadata and must not contain secrets or sensitive personal information.

---

## 10. Frontend Security

The Next.js frontend must not be treated as a trusted security boundary.

Security-sensitive decisions must always be enforced by the backend.

Frontend security requirements include:

* Do not expose server-side secrets to browser code.
* Do not embed private API credentials in client-side JavaScript.
* Avoid unsafe HTML rendering.
* Validate external URLs before navigation where applicable.
* Protect authentication state appropriately.
* Avoid storing sensitive credentials in insecure browser storage.
* Apply appropriate Content Security Policy and security headers in production.
* Keep frontend dependencies regularly updated.

---

## 11. Dependency Security

Application and infrastructure dependencies must be reviewed regularly.

Security practices include:

* Keep Python dependencies updated.
* Keep Node.js dependencies updated.
* Review dependency advisories.
* Remove unused dependencies.
* Pin or constrain production dependencies appropriately.
* Scan container images for known vulnerabilities.
* Review new dependencies before introducing them into security-sensitive components.

Automated dependency scanning should be integrated into CI/CD where practical.

---

## 12. CI/CD Security

CI/CD pipelines must follow least-privilege principles.

* Secrets must be stored using secure CI/CD secret storage.
* Credentials must never be hard-coded in workflow files.
* Pull requests should undergo automated validation.
* Security-sensitive changes should receive code review.
* Production deployment credentials should be separated from development credentials.
* CI jobs should receive only the permissions they require.
* Third-party GitHub Actions should be reviewed before use.

---

## 13. Data Protection

LokTathya may process information associated with civic services and public-facing records.

Contributors must:

* Collect only required information.
* Avoid unnecessary storage of sensitive information.
* Prevent unauthorized data access.
* Avoid exposing private information through logs or error responses.
* Apply appropriate access controls to protected resources.
* Avoid including real personal data in tests or development fixtures.

Production data must never be copied into development environments unless explicitly authorized and appropriately anonymized.

---

## 14. Error Handling

Production applications must return safe, controlled error responses.

Do not expose:

* Stack traces
* Internal filesystem paths
* Database connection strings
* SQL statements containing sensitive information
* Internal service addresses
* Authentication secrets
* Infrastructure credentials
* Debug configuration

Detailed diagnostic information should remain available through protected internal logging and observability systems.

---

## 15. Security Testing

Security testing should be performed throughout the development lifecycle.

Recommended checks include:

* Static analysis
* Dependency vulnerability scanning
* Container image scanning
* API security testing
* Authentication and authorization testing
* Input-validation testing
* Injection testing
* Access-control testing
* Rate-limit testing
* Secret scanning
* Configuration review

Security-critical changes should receive additional review before deployment.

---

## 16. Responsible Disclosure

Security researchers who report vulnerabilities responsibly are encouraged to:

* Give LokTathya reasonable time to investigate and remediate the issue.
* Avoid accessing, modifying, deleting, or downloading data that does not belong to them.
* Avoid disrupting production services.
* Avoid automated scanning that could cause service degradation.
* Avoid social engineering attacks against project contributors.
* Avoid publicly disclosing the vulnerability before coordinated remediation.

We will make reasonable efforts to credit researchers who responsibly disclose valid vulnerabilities, subject to their preference and applicable disclosure requirements.

---

## 17. Out-of-Scope Reports

The following generally do not qualify as security vulnerabilities unless they demonstrate a meaningful security impact:

* Self-XSS without a realistic attack path.
* Missing security headers with no demonstrated impact.
* Informational dependency warnings without an exploitable path.
* Issues requiring compromised user accounts without additional impact.
* Denial-of-service testing against production infrastructure without prior authorization.
* Automated vulnerability scans that generate excessive traffic.
* Cosmetic or non-security-related bugs.

Reports will still be reviewed when they identify a credible security risk.

---

## 18. Security Incident Response

If a confirmed security incident affects LokTathya infrastructure, maintainers may:

1. Isolate affected services.
2. Revoke or rotate compromised credentials.
3. Preserve relevant logs and forensic information.
4. Identify affected systems and data.
5. Deploy mitigations.
6. Patch the underlying vulnerability.
7. Restore affected services safely.
8. Review the incident and identify preventive actions.
9. Communicate material security impacts through appropriate channels.

Incident response priorities are:

**Containment → Investigation → Remediation → Recovery → Prevention**

---

## 19. Contributor Security Guidelines

Before submitting a contribution:

* Never commit secrets.
* Never commit production credentials.
* Never include real sensitive user data in fixtures.
* Validate all external input.
* Review authorization boundaries.
* Avoid unnecessary privilege escalation.
* Review database queries for injection risks.
* Review file-upload functionality carefully.
* Review authentication and session handling.
* Ensure security-sensitive changes include appropriate tests.

---

## Contact

For responsible disclosure of security vulnerabilities:

**Security Team:** `security@loktathya.org`

For general project discussions, feature requests, and non-sensitive bugs, use the appropriate public GitHub issue or discussion channels.

**Do not use public GitHub issues for undisclosed security vulnerabilities.**

---

## Security Policy Maintenance

This policy is reviewed periodically and may be updated as LokTathya's architecture, infrastructure, threat model, and operational requirements evolve.

Security is a continuous process. Every contributor is responsible for helping maintain the confidentiality, integrity, and availability of the LokTathya platform.
