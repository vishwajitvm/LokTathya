# Privacy Policy

**Effective Date:** August 22, 2026
**Last Updated:** August 23, 2026

LokTathya ("LokTathya", "Platform", "we", "us", or "our") is a civic technology platform designed to improve public access to structured information concerning elected representatives, candidates, public officials, civic records, and related public-interest information.

We are committed to responsible data handling, transparency, security, and privacy. This Privacy Policy explains what information LokTathya may collect, how it is used, how it is protected, and the choices available to users.

This policy is intended to provide a clear description of the Platform's current data practices and may be updated as the Platform's architecture, services, and legal requirements evolve.

---

## 1. Scope of This Policy

This Privacy Policy applies to information processed through:

* The LokTathya web application.
* LokTathya APIs and backend services.
* The LokTathya civic data and search infrastructure.
* The LokTathya AI-assisted search and question-answering functionality.
* Publicly accessible civic datasets processed and presented by the Platform.
* Technical logs, telemetry, and operational information generated while using the Platform.

This policy does not apply to third-party websites, services, APIs, or external resources that may be linked from LokTathya.

Those services maintain their own privacy policies and terms.

---

# 2. Information We Process

LokTathya follows a data-minimization approach and seeks to process only information necessary to operate, secure, maintain, and improve the Platform.

Information processed by the Platform may include the following categories.

## 2.1 Technical & Operational Information

When a user interacts with the Platform or its APIs, the infrastructure may generate limited technical information such as:

* Request path or API endpoint.
* HTTP method.
* HTTP response status.
* Request processing time.
* Timestamp.
* Service or component involved in processing.
* `X-Request-ID` / TraceNest request identifier.
* Application and infrastructure error information.
* Basic operational telemetry required for security and reliability.

These records are primarily used for:

* Debugging.
* Security monitoring.
* Performance analysis.
* Reliability engineering.
* Incident investigation.
* Request tracing.
* Abuse prevention.

LokTathya does not intentionally collect unnecessary information about users merely because they visit the Platform.

---

# 3. Cookies & Browser Storage

LokTathya is designed to minimize the use of tracking technologies.

## 3.1 Analytics & Advertising Cookies

LokTathya does not currently use advertising cookies or third-party behavioral tracking cookies for profiling users or serving targeted advertisements.

## 3.2 Local Browser Storage

The Platform may use browser `localStorage` for non-sensitive client-side preferences, such as:

* Dark mode / light mode preference.
* User-interface preferences required to provide a consistent experience.

`localStorage` should not be used by the Platform to store passwords, API keys, private credentials, or other highly sensitive authentication secrets.

---

# 4. Civic Data & Public-Interest Information

LokTathya provides structured access to information relating to elected representatives, candidates, public officials, and other civic records.

Much of this information may originate from publicly accessible government records or other authoritative public sources.

Examples may include:

* Election-related disclosures.
* Candidate affidavits.
* Declared assets and liabilities.
* Educational qualifications.
* Publicly disclosed court or case information.
* Electoral information.
* Public office and term information.
* Government publications and official records.

The purpose of presenting this information is to improve public accessibility, searchability, transparency, and civic awareness.

---

# 5. Sources & Data Accuracy

LokTathya aims to prioritize authoritative and publicly available sources when collecting civic information.

Potential sources may include:

* Election Commission of India publications.
* Official election affidavits and disclosures.
* Parliament and State Legislature publications.
* Government gazettes.
* Government departments and official portals.
* Other authoritative public records.

Where practical, source information and provenance should be retained internally so that records can be reviewed and corrected when necessary.

LokTathya does not guarantee that every publicly available record is complete, current, or error-free.

Information presented by LokTathya should not be interpreted as an official government record unless explicitly identified as such.

---

# 6. Personal Information in Civic Records

Public availability of information does not mean that every associated piece of personal information should be reproduced.

LokTathya follows a privacy-conscious approach when processing civic records.

## 6.1 Information We Aim to Exclude or Redact

Where not required for the legitimate public-interest purpose of the Platform, LokTathya aims to avoid exposing information such as:

* Personal telephone numbers.
* Personal email addresses.
* Private bank account numbers.
* Authentication credentials.
* Financial account credentials.
* Tax identifiers such as PAN numbers where unnecessary.
* Private residential addresses where unnecessary.
* Identity-document numbers.
* Other sensitive personal information that is not necessary for the civic purpose of the Platform.

## 6.2 Public-Interest Information

Depending on the underlying public record and applicable requirements, LokTathya may retain and present information such as:

* Declared asset totals.
* Declared liability totals.
* Educational qualifications.
* Public office held.
* Election information.
* Publicly disclosed case identifiers.
* Publicly disclosed case categories.
* Election or representative term periods.
* Other information contained in legitimate public-interest disclosures.

The exact information displayed may vary depending on the source document and the purpose for which the information is presented.

---

# 7. AI Assistant & LLM Processing

LokTathya provides AI-assisted functionality to help users search, understand, summarize, and navigate civic information.

When a user submits a query to an AI-powered feature:

1. The request is received by LokTathya's backend.
2. The relevant application or retrieval pipeline processes the request.
3. Where required, relevant civic information may be retrieved.
4. The query and necessary contextual information may be sent to an external model provider.
5. The model generates a response.
6. The response is returned to the user.

## 7.1 Data Minimization

Only information reasonably necessary to process the request should be forwarded to an external AI provider.

LokTathya should not intentionally send:

* Passwords.
* Authentication tokens.
* API credentials.
* Internal secrets.
* Unnecessary personal information.

to an external model provider.

## 7.2 Third-Party AI Providers

Depending on the deployment configuration, LokTathya may use third-party or self-hosted AI/LLM services.

The handling of information by an external provider is also subject to that provider's applicable terms, security controls, and privacy commitments.

Where external providers are used for production processing, LokTathya intends to select configurations and providers that minimize retention and secondary use of submitted content.

---

# 8. Data Sharing

LokTathya is designed as a non-commercial civic technology platform.

We do not sell personal information or user activity data as a commercial product.

Information may nevertheless be processed or disclosed when reasonably necessary for:

* Operating the Platform.
* Providing AI-assisted functionality.
* Maintaining infrastructure.
* Preventing abuse or security incidents.
* Investigating technical failures.
* Complying with applicable legal obligations.
* Responding to lawful requests from competent authorities.
* Protecting the rights, safety, and security of the Platform and its users.

Any third-party service used by LokTathya should receive only the information necessary for the relevant service to function.

---

# 9. Data Retention

LokTathya follows a data-minimization and purpose-based retention approach.

Different categories of information may have different retention periods.

For example:

| Data Category      | General Purpose                                      |
| ------------------ | ---------------------------------------------------- |
| Request metadata   | Security, debugging, tracing                         |
| Application logs   | Reliability and incident investigation               |
| AI query context   | Request processing                                   |
| Civic records      | Public-interest information and historical reference |
| Security events    | Security monitoring and incident response            |
| Client preferences | User-interface functionality                         |

Technical logs and telemetry should not be retained indefinitely when they are no longer necessary for their operational or security purpose.

Public civic records may require longer retention because historical information can have continuing public-interest value.

---

# 10. Data Security

LokTathya applies technical and organizational safeguards designed to protect information against unauthorized access, modification, disclosure, destruction, and misuse.

Security measures may include:

* Authentication and authorization controls.
* Role-based access controls where applicable.
* Secure API validation.
* Database access controls.
* Network isolation.
* Secret management.
* Container isolation.
* Secure deployment configuration.
* Request tracing.
* Security logging.
* Dependency monitoring.
* Vulnerability management.
* Backup and recovery controls.
* Least-privilege infrastructure access.

Internal services such as PostgreSQL, Redis, MinIO, and worker infrastructure should not be unnecessarily exposed to the public internet.

Additional security requirements are documented in the LokTathya security policy.

---

# 11. Data Integrity & Provenance

For civic information, maintaining the relationship between a displayed record and its underlying source is an important part of the Platform.

Where technically feasible, LokTathya should maintain:

* Source references.
* Source URLs or document identifiers.
* Retrieval timestamps.
* Processing metadata.
* Record provenance.
* Data version information.

Automated ingestion and transformation processes should be designed to minimize accidental alteration of source information.

---

# 12. Data Corrections & Accuracy Requests

If you believe that a civic record presented by LokTathya is inaccurate, incomplete, outdated, incorrectly attributed, or improperly processed, you may contact us.

Please include:

* The relevant record or representative.
* The specific information in question.
* The reason you believe it is inaccurate.
* Supporting documentation or authoritative source material, where available.
* A way for the team to identify the affected record.

We will review credible correction requests and, where appropriate, investigate the underlying source and update the Platform.

Correction of information does not necessarily mean removal of historically accurate public-interest information.

---

# 13. Privacy Requests

For privacy-related questions or requests, contact:

**Email:** `wolverinevm001@gmail.com`

Depending on the nature of the request and applicable law, you may contact us regarding:

* Personal-data processing questions.
* Data correction requests.
* Privacy concerns.
* Unnecessary exposure of personal information.
* Questions about data sources.
* Questions regarding AI-assisted processing.
* Security or confidentiality concerns.

We may request sufficient information to verify and appropriately process a request.

---

# 14. Children's Privacy

LokTathya is a civic information platform and does not intentionally design its services to collect personal information from children.

Users should not submit unnecessary personal information belonging to minors through public forms, chat interfaces, GitHub issues, or other public communication channels.

If information relating to a minor is discovered where it should not have been publicly exposed, please contact us so that the matter can be reviewed.

---

# 15. Third-Party Services

LokTathya may depend on third-party infrastructure, APIs, model providers, hosting providers, authentication systems, or other services.

Examples may include services used for:

* AI inference.
* Hosting.
* Storage.
* Monitoring.
* Authentication.
* Infrastructure management.

These providers may process information necessary to provide their respective services.

LokTathya does not control the independent privacy practices of third-party providers. Users should review the applicable privacy policies of those services where relevant.

---

# 16. External Links

The Platform may contain links to government websites, public records, documentation, or third-party resources.

Following an external link may take you to a service outside LokTathya's control.

LokTathya is not responsible for the privacy practices, security, availability, or content of external websites.

Users should review the privacy policies applicable to those services.

---

# 17. Security Incidents

If LokTathya becomes aware of a security incident involving personal information or other protected information, the Platform will assess the incident and take appropriate steps based on the nature, scope, and potential impact of the event.

Response activities may include:

* Containing the incident.
* Investigating affected systems.
* Revoking compromised credentials.
* Applying security patches.
* Restoring affected services.
* Preserving relevant security evidence.
* Assessing affected information.
* Making notifications where required by applicable law or operational circumstances.

Security vulnerabilities should be reported privately rather than through public GitHub issues.

---

# 18. Changes to This Privacy Policy

LokTathya may update this Privacy Policy when:

* Platform functionality changes.
* Data-processing practices change.
* Infrastructure changes.
* New services are introduced.
* Security requirements evolve.
* Applicable laws or regulations change.

When material changes are made, the **Last Updated** date will be updated accordingly.

The latest version published with the Platform will govern the applicable processing practices from its effective date.

---

# 19. Applicable Legal Framework

LokTathya operates with consideration for applicable Indian laws and regulations concerning privacy, cybersecurity, information technology, and protection of digital personal data.

The Digital Personal Data Protection Act, 2023 and the Digital Personal Data Protection Rules, 2025 establish India's evolving framework for processing digital personal data. The Rules were notified by the Ministry of Electronics and Information Technology in November 2025 and include a phased commencement framework.

LokTathya's privacy and data-handling practices will be updated as applicable provisions become effective and as the Platform's operational model develops.

This Privacy Policy should not be interpreted as a representation that every provision of every applicable law is currently applicable to every Platform activity.

---

# 20. Contact

For privacy questions, data correction requests, or concerns regarding personal information:

**LokTathya Privacy Contact**

`vishwajitmall50@gmail.com`

For security vulnerabilities, please use the security reporting process described in `SECURITY.md` rather than publicly disclosing the vulnerability.

---

## Commitment to Privacy

LokTathya's objective is to make civic information more accessible without unnecessarily compromising individual privacy.

We aim to maintain a balance between:

**Public Transparency + Data Accuracy + Privacy + Security + Responsible Technology**

The Platform will continue to evolve its data governance, security controls, and privacy practices as LokTathya grows.
