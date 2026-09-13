# MUJ SLCM Data-Protection and Reporting Assurance Plan

## Executive Summary

- **The Legal Clock Is Split**: On **13 September 2026**, CERT-In's six-hour incident-reporting and 180-day logging directions are already operative, while the DPDP Act's ordinary notice, security, breach-notification, rights, child-data and erasure duties are scheduled to commence after the 18-month phase, calculated as **13 May 2027** [3][29][44]. -> Treat CERT-In and the SPDI Rules as today's mandatory baseline, but build and test the DPDP controls now rather than waiting for commencement.
- **The Current Privacy Baseline Is Not Empty**: The SPDI Rules presently require a published privacy policy, purpose-linked written consent for sensitive personal data, necessity, use limitation, retention limitation, a named Grievance Officer and reasonable security practices [33]. Medical records, health information, payment information, passwords and biometrics fall within its enumerated sensitive categories [33]. -> Map each SLCM field to SPDI now and to the broader DPDP definition for 2027 readiness.
- **CERT-In Reporting Is Not Delegable**: A covered entity must report a listed cyber incident within **six hours of noticing it or being informed of it**; it may send the information then available and supplement it within a reasonable time [29]. The reporting obligation cannot be transferred to a cloud or portal supplier [29]. -> MUJ needs its own named incident owner, clock-start rule, CERT-In point of contact and pre-approved initial-report template.
- **A Vulnerability Is Not Automatically a Reportable Incident**: CERT-In's FAQ says reporting a vulnerability in isolation, unconnected to a cyber incident, is not presently mandatory [29]. -> The observed YSOD pages, differential `enc` behavior and old libraries warrant remediation, but should not be mislabeled a data breach without evidence of unauthorized access, disclosure or compromise.
- **The Largest Unknown Is Behind Authentication**: The campaign has not tested object-level authorization, role boundaries, document isolation, tenant routing, deletion or rights workflows. OWASP describes IDOR as user-controlled object references that bypass authorization and recommends testing with at least two users and different owned objects [50]. -> The signed letter and two controlled accounts are prerequisites for the highest-value tests.
- **Several Pre-Authentication Findings Are Actionable**: Offering TLS 1.0 and 1.1 conflicts with OWASP's recommendation to default to TLS 1.3, retain TLS 1.2 only where needed, and disable the formally deprecated older protocols [51]. The anti-forgery cookie's `HttpOnly` flag is positive, but absence of `Secure`, missing HSTS, verbose errors and distinguishable cryptographic failure families create avoidable exposure. -> Fix these without waiting for exploitability proof.
- **Old jQuery Is A Conditional, Not A Proven Exploit**: jQuery versions before 3.0.0 are affected by CVE-2015-9251 under a particular cross-domain Ajax condition; versions 1.12.0 through before 3.5.0 are affected by CVE-2020-11022 when untrusted HTML reaches affected DOM-manipulation methods; versions before 3.4.0 are affected by CVE-2019-11358 [41][46][39]. -> Inventory actual call paths and remove the 1.10.2 bundle; do not claim the portal is exploitable merely from version detection.
- **Three Entra Tenants Create A Governance Test**: This is an inference from the supplied architecture, not proof of a flaw. Multiple tenants can divide sign-in, guest, service-principal and Conditional Access evidence. Microsoft Graph's sign-in API exposes identity, application, IP, correlation ID, risk, device and Conditional Access fields when the caller has `AuditLog.Read.All` and a suitable Entra role [48]. -> Establish which tenant is authoritative for each SLCM identity path and centralize the audit evidence.
- **Automation Cannot Prove Legal Accountability**: Scanners can identify TLS, headers, exposed data, vulnerable components, cloud configuration and log anomalies. They cannot determine the lawful purpose for each field, whether consent is genuinely free, whether a retention exception applies, who controls processing, or whether a six-hour report was approved and sent. -> Make those manual controls explicit and build an evidence-oriented compliance harness around them.

## Scope, Evidence Boundary and Auditable Reasoning

This report uses public legal and technical sources plus the measurements supplied in the request. It does **not** reconnect to, authenticate to, fuzz or otherwise test `mujslcm.jaipur.manipal.edu`. The measured results are therefore treated as **user-supplied observations dated 13 September 2026**, not independently reproduced findings.

The analysis does not provide private hidden chain-of-thought. Instead, it provides an auditable decision rationale: **observation -> governing requirement or benchmark -> target-specific inference -> authorized verification step**. Every inference is labeled. This gives the club a reviewable basis without exposing exploit instructions or encouraging access without permission.

The Manipal University, Jaipur Act constitutes the University as a body corporate with perpetual succession and the ability to sue and be sued [35]. MUJ's public page says the Registrar signs contracts, authenticates records and is custodian of University records; it identifies Dr Amit Soni and publishes `registrar@jaipur.manipal.edu` [34]. That supports placing the Registrar in the escalation and authorization chain. It does **not**, by itself, establish which MUJ entity or vendor determines every SLCM processing purpose. That Data Fiduciary allocation must be confirmed from contracts and system ownership records.

**Decision-ready insight:** The report can convert law into tests, but only MUJ can provide the contracts, processing inventory, account roles, source code and telemetry needed to close the decisive gaps.

## The 2026-2027 Legal Baseline: Current Duties Versus Readiness Duties

### Phased DPDP commencement prevents both complacency and overstatement

The DPDP Act applies to digital personal-data processing in India and to certain processing outside India connected with offering goods or services to Data Principals in India [6]. Its substantive framework requires clear notice, free and informed consent, processor contracts, appropriate organizational and technical measures, reasonable security safeguards, breach intimation, erasure, child-data controls and Data Principal rights [6]. However, enactment and operative commencement are different questions.

| Phase | Act provisions | Rules | Status on 13 Sep 2026 | Practical consequence |
|---|---|---|---|---|
| Publication date, 13 Nov 2025 | Section 2; sections 18-26; sections 35 and 38-43; section 44(1) and 44(3) [44] | Rules 1, 2 and 17-21 [23] | In force | Definitions and Data Protection Board machinery are active. |
| One year after publication, computed 13 Nov 2026 | Section 6(9) and section 27(1)(d) [44] | Rule 4 [23] | Not yet in force on the report date | Consent Manager architecture is near-term, not today's ordinary portal-duty baseline. |
| Eighteen months after publication, computed 13 May 2027 | Sections 3-5; section 6 except 6(9); sections 7-17; most of section 27; sections 28-34 and 36-37; section 44(2) [44] | Rules 3, 5-16, 22 and 23 [23] | Future on the report date | Ordinary notice, consent, safeguards, breach notification, rights, erasure and child-data controls must be implementation-ready. |

The 13 May 2027 date is a calendar calculation from the notification's 18-month wording, not a separately printed date. The report preserves that distinction.

When operative, Rule 6 will require safeguards including access controls, encryption, obfuscation, masking or tokens as appropriate, logs and monitoring, backups, relevant one-year evidence retention, processor contracts, and organizational measures [16]. Rule 7 will require an affected-person notice without delay and an initial Board notice without delay, followed by specified details within 72 hours unless the Board permits longer [20]. The Act's schedule permits penalties up to **INR 250 crore** for failure to take reasonable safeguards and **INR 200 crore** for failure to notify a breach or meet child-data duties [6]. These are future substantive duties on the report date, not current penalties for the supplied observations.

### SPDI remains the present operational privacy baseline

Until DPDP section 44(2) commences, section 43A of the IT Act and the SPDI Rules remain central to current private-sector data security. Section 43A addresses negligent failure by a body corporate to implement reasonable security practices where wrongful loss or gain results [8]. The Rules classify passwords, payment information, physical or mental health information, medical records and biometric information as sensitive [33].

For SLCM, the classification should be field-specific:

| Portal data | Current SPDI treatment | DPDP readiness treatment | Testable requirement |
|---|---|---|---|
| Passwords and authentication secrets | Express SPDI category [33] | Personal data requiring safeguards | No plaintext storage or logging; masked support views; controlled reset; secret scanning. |
| Fee and payment records | Payment instrument and bank details are SPDI; a fee amount alone may not be | Digital personal data | Inventory fields, tokenize payment details, restrict finance roles, verify retention basis. |
| Medical documents | Express health and medical-record SPDI [33] | Personal data with potentially severe harm | Separate authorization policy, encrypted storage, download logging, deletion and disclosure review. |
| Aadhaar | Aadhaar number is not expressly one of the SPDI Rule 3 labels; associated biometrics are | Digital personal data | Determine whether MUJ is in the UIDAI authentication ecosystem; mask identifiers and map purpose. UIDAI Circular 8 of 2025 specifically concerns ADV, HSM and authentication applications in that ecosystem [5]. |
| APAAR and marks | Educational records are not an express SPDI Rule 3 category | Digital personal data | Purpose, sharing, correction and retention controls. APAAR's own policy describes marksheets, grades, transcripts and credentials as collected educational records [4]. |
| Student name, ID and contact details | Personal information; not automatically SPDI | Digital personal data | Role-based access, minimization, accurate notice and rights workflow. |

The national APAAR policy says personal information is processed in accordance with applicable law and identifies account, educational and technical information [4]. **Inference:** that policy does not substitute for an MUJ SLCM privacy notice if MUJ independently collects, stores, displays or shares the same information.

**Decision-ready insight:** MUJ should operate a dual-column control register: "legally required now under SPDI/CERT-In" and "must be production-ready by DPDP commencement." This avoids both false claims of full present DPDP applicability and a risky last-minute implementation.

## The Reporting Chain as a Testable System

CERT-In's directions apply to service providers, intermediaries, data centers, body corporates and government organizations as applicable [3][29]. Listed events include unauthorized access, data breach or leak and incidents affecting e-governance applications [3]. Covered ICT clocks must be synchronized with designated or traceable time sources; logs must be enabled, securely maintained for a rolling **180 days within India**, and supplied when required [3]. A designated point of contact must be maintained [3].

A six-hour obligation cannot be satisfied by a policy document alone. The following workflow converts it into measurable service-level objectives. Times before six hours are proposed internal targets, not statutory sub-deadlines.

| Stage | Proposed owner | Clock and evidence | Pass criterion | Detection counterpart |
|---|---|---|---|---|
| 1. Notice | SOC, help desk or system owner | Record earliest time MUJ noticed or was informed | UTC/IST timestamp, reporter, affected system and immutable ticket ID exist | Alert-to-ticket integration; time-sync health alert. |
| 2. Triage | Incident commander | Proposed target: 30 minutes | Event is classified against CERT-In Annexure I; vulnerability-only reports remain distinct | SIEM rule tags incident category and affected data. |
| 3. Scope | Portal, Entra, Azure and database owners | Proposed target: 90 minutes | Accounts, records, tenants, IPs, time range and processors are identified without delaying the initial report | Correlation IDs connect web, application, identity and database logs. |
| 4. Initial decision | Incident commander, legal/privacy, CERT-In PoC | Proposed target: 3 hours | Decision and rationale are signed; unresolved facts are marked unknown | Escalation alert if approval is stalled. |
| 5. CERT-In initial report | Named MUJ reporter | Statutory maximum: six hours after notice [29] | Available facts sent through CERT-In's official incident channel; receipt retained | Countdown dashboard and overdue alert. |
| 6. Supplement | Incident team and processors | Additional information within a reasonable time [29] | New facts, containment and indicators are versioned and supplied | Case-management reminder and change log. |
| 7. DPDP notices after commencement | Privacy lead/Data Fiduciary | Affected people and Board without delay; detailed Board material within 72 hours [20] | Required content, recipient list, delivery evidence and Board submission are retained | Separate DPDP timers linked to the same case. |
| 8. Closure | Registrar/owner, security and privacy | Internal target set by MUJ | Root cause, recurrence controls, evidence retention and rights impacts approved | Post-incident control validation and audit report. |

CERT-In permits an initial report containing information available at that time [29]. Therefore, a demand for complete forensic certainty before submission would be a defective control. Cloud-provider notification also does not replace MUJ's duty because reporting is non-transferable [29].

### Case study 1: A verbose error is not yet a breach

**Observation:** The supplied measurements show four YSOD triggers, `customErrors` disabled and three stable `enc` response families. **Mechanism:** distinguishable server exceptions can disclose implementation details or act as an input-validation oracle, but the measurements do not establish unauthorized access to personal data. CERT-In expressly distinguishes a standalone vulnerability from a reportable cyber incident [29].

**Implication:** Automatically sending every scanner finding into the six-hour breach process would create false positives; ignoring the signal would also be wrong. **Recommendation:** route the finding to vulnerability remediation, preserve application/error logs, suppress verbose production details and create a detection rule for bursts of distinct `enc` exception classes. Escalate to the incident chain only if evidence indicates exploitation, unauthorized access, leakage or another Annexure I event.

### Case study 2: A cross-account medical document would change the clock

**Hypothetical, authorization-gated:** Suppose test account A can retrieve a medical document assigned to test account B by changing an object reference. OWASP defines this as the IDOR class and recommends testing with multiple users and distinct objects [50]. The security team should use only seeded test documents and accounts identified in the letter.

**Mechanism and implication:** A confirmed cross-account disclosure would involve SPDI medical information and could be a reportable unauthorized-access or data-leak incident under CERT-In. Once DPDP Rule 7 is operative, the same facts could also trigger affected-person and Board notices [20]. **Recommendation:** the test plan must pre-agree whether a seeded test-data finding starts the regulatory clock, who can determine whether any production records were exposed, and how database/object-access logs will establish scope.

### Case study 3: Three tenants can fragment evidence

**Inference from supplied architecture:** A user may authenticate in one tenant, access an application registration in another, and be represented as a guest or service identity elsewhere. That does not prove misconfiguration. It does create a testable accountability question: which tenant owns each user, application, Conditional Access decision and audit trail?

Microsoft Graph can return sign-in time, application, IP, device, risk, status, correlation ID and Conditional Access information with appropriate audit permission [48]. **Recommendation:** MUJ should select a single incident correlation key and prove that a portal request can be followed across all relevant tenants and into application logs. A tenant that cannot export the necessary evidence within the six-hour window is a reporting-control defect even if authentication itself is secure.

## Assessment of the Supplied Measurements

| Supplied observation | Assessment | Inference and limit | Priority action |
|---|---|---|---|
| Only TCP 443 reachable | Positive reduction in externally reachable services | Does not prove internal or origin exposure is absent | Preserve; validate from owner-side asset inventory. |
| TLS 1.0-1.3 offered; no HSTS | Confirmed hardening gap from supplied data | OWASP says TLS 1.0/1.1 are deprecated and should be disabled [51] | Disable 1.0/1.1, prefer 1.3, retain hardened 1.2 only if required, then enable HSTS after dependency review. |
| Verbose YSOD and `customErrors` off | High-confidence information exposure | No proof of code execution or personal-data disclosure | Generic external errors; correlation ID only; detailed exception server-side. |
| Anti-forgery enforced | Positive control | Enforcement was observed only on tested paths | Preserve and cover all state-changing routes after authorization. |
| Anti-forgery cookie HttpOnly but not Secure | Mixed | `HttpOnly` blocks DOM cookie access [52]; lack of `Secure` is an avoidable transport flag gap even though only 443 was reachable | Set `Secure`; review `SameSite`; confirm cookie scope and purpose. |
| `trace.axd` 403; `elmah.axd` 404 | Positive exposure checks | Responses do not prove no alternate management path exists | Keep management endpoints disabled or admin-isolated. |
| MVC and IIS error families | Useful classification signal | Different size alone is not a vulnerability | Normalize external errors; alert on family/rate anomalies. |
| GET accepted; POST/PUT 411; other verbs 404 on tested surface | Narrow method policy observation | Must not be generalized to every route | Document per-route method contract; test state-changing routes only under the letter. |
| Three-stage `enc` oracle | Reproducible differential behavior in supplied test | Confidentiality or cryptographic break is unproven | Validate before decode/decrypt, return one external failure class, instrument exception counters. |
| Host and forwarding bypass attempts clean | Positive for tried variants | Does not establish universal proxy trust safety | Preserve allow-list configuration and log rejected host anomalies. |
| jQuery 1.10.2 and 3.4.1 bundles | Known-version risk | Exploitability depends on actual data flow; 1.10.2 and 3.4.1 intersect different published affected ranges [41][46][39] | Remove duplicate legacy bundle; run SCA plus manual sink review; regression test UI. |
| No authenticated testing | Dominant assurance gap | Authorization, disclosure, retention and rights cannot be scored | Obtain signed letter, seeded data and two role-differentiated accounts. |

**Decision-ready insight:** The current result is still **PARTIAL** as an assurance campaign, but it can exceed the prior campaign's legal coverage immediately by treating the reporting clock, evidence chain and future DPDP controls as explicit pass/fail requirements.

## Technique Universe: Requirement, Manual Method and Detection Counterpart

| Technique family | What must be proved | Automation | Manual method where automation is insufficient | Detection counterpart | Authorization |
|---|---|---|---|---|---|
| Legal entity and processor mapping | MUJ, platform operator, Azure/M365 roles and notification duties are allocated | Purview, contract inventory systems | Read contracts, data-processing terms, tenant ownership and delegation clauses | Annual ownership attestation; stale-owner alerts | Internal records and owner cooperation required. |
| Data inventory and classification | Every field, file, log, export and backup has owner, purpose and sensitivity | Purview, Presidio | Interview finance, examinations, health, hostel, admissions and IT owners; sample schemas | Discovery drift alert when new sensitive fields appear | Offline on supplied artifacts; production scan needs letter and access. |
| Notice and purpose limitation | Notice matches actual fields, uses, sharing and processors | No scanner can prove this | Compare UI notices and consent receipts to the processing inventory | Alert on schema/purpose changes without notice review | Public notice review is safe; account flows need test accounts. |
| Consent and withdrawal | Consent is specific, affirmative and as easy to withdraw as to give | Playwright can replay an approved workflow | Assess voluntariness, bundling, consequence of refusal and legal alternatives | Consent-receipt ledger; failed-withdrawal alerts | Letter plus seeded accounts. |
| Data minimization | Each collected field is necessary for a documented purpose | Presidio/Purview identify fields, not necessity | Challenge each field with business owner; document lawful exception | New-field approval gate | Owner-side only. |
| Authentication and tenant routing | Correct tenant, issuer, audience, MFA and lifecycle | Playwright, Burp/ZAP, Graph sign-ins | Review app registrations, guest policy, break-glass and offboarding | Entra risk and Conditional Access alerts | Test accounts and explicit identity scope. |
| Object and role authorization | Student, faculty, finance, health and admin objects remain isolated | Burp/ZAP replay, Schemathesis or RESTler for owned APIs | Two-account differential matrix using only seeded objects | Denied-object and unusual-enumeration alerts | Signed letter and two accounts mandatory. |
| Session and anti-forgery | Secure cookie flags, rotation, expiry, logout and CSRF protection | Burp/ZAP, mitmproxy, Playwright | Observe login, privilege changes and logout with test accounts | Session anomaly and CSRF failure telemetry | Public flags may be observed; lifecycle needs accounts. |
| TLS, headers and host trust | Supported protocols, HSTS, certificate chain and proxy trust | testssl.sh, Nmap, curl, httpx | Review compatibility exception and reverse-proxy topology | Certificate/protocol configuration drift | Do not scan target before written permission; offline config review is safe. |
| Error and oracle handling | Externally uniform errors; detailed internal logs | curl/httpx, ZAP/Burp Comparer | Classify known error families without seeking deeper effects | Exception-class, response-size and rate alerts | Existing evidence can be reviewed; new mutation needs letter. |
| Client and server dependencies | No unsupported or vulnerable reachable code paths | Retire.js, Dependency-Check, Trivy, Semgrep | Trace whether untrusted data reaches affected APIs; plan regression | SBOM drift and critical-CVE gate | Public asset inventory is low impact; source/build access is internal. |
| Secrets and privacy in code/logs | Secrets, Aadhaar, medical data and tokens are absent from code and excessive logs | Gitleaks, Presidio, Semgrep | Review false positives and business-approved masking | Secret-detection and DLP alerts | Only on owner-supplied repositories/log exports. |
| Upload/download security | Seeded documents cannot cross users; types and malware controls work | ZAP/Burp, Playwright | Use inert test files; never upload live personal or executable material | Download attribution, malware and unusual-volume alerts | Letter plus seeded accounts and file rules. |
| Retention, erasure and backups | Front end, database, search, cache, logs, replicas and backups follow one rule | Purview may map stores | Execute a seeded-record lifecycle and inspect every replica | Over-retention and failed-deletion reports | Owner-side access required. |
| Rights and grievance workflow | Access, correction, erasure, nomination and grievance requests are authenticated and completed | Playwright for workflow timing | Review legal exceptions, identity proof and response completeness | SLA timers and overdue escalation | Test account plus privacy/legal participation. |
| Incident detection and reporting | Reportability, six-hour CERT-In clock, future DPDP notices and evidence work end to end | Sentinel, Azure Monitor, Wazuh, OTel | Tabletop with legal, Registrar, security, vendors and communications | Clock dashboard, receipt archive and missed-SLA alert | Safe as tabletop; live simulation needs written change approval. |

## Tool Catalog: Exact URL, License, Operation and Output

"Every tool" is bounded here to the maintainable tools that directly implement the technique universe above. No report can literally enumerate every commercial scanner. BYOK means a product requires a separately supplied API key; most local tools do not.

### Black-box, browser and API assurance tools

| Tool and exact URL | License and delivery | How driven | Relevant output | Safe-use boundary |
|---|---|---|---|---|
| OWASP ZAP - https://www.zaproxy.org/docs/desktop/addons/report-generation/ | Apache-2.0; free, self-hosted desktop/daemon/container [9] | GUI, CLI, REST API, Automation Framework YAML | Alerts plus HTML, XML, JSON, Markdown, PDF or SARIF templates | Passive review of saved traffic is safe; crawling/active scan requires letter. |
| Burp Suite - https://portswigger.net/burp/documentation/desktop/running-scans/reporting | Proprietary; Community is free with limits, Professional/Enterprise paid | Desktop proxy, Repeater, test workflows, scanner in paid editions | Issue list and HTML report; structured exports vary by edition [15] | Interception of owned test accounts only; automated scan must be scoped. |
| Nuclei - https://github.com/projectdiscovery/nuclei | MIT; free self-hosted CLI, optional commercial cloud [22] | CLI or CI using signed/reviewed YAML templates | Console, JSONL, SARIF and report integrations | Templates send requests; do not run against MUJ before authorization. |
| testssl.sh - https://github.com/testssl/testssl.sh | GPL-2.0; free self-hosted shell tool [10] | Shell CLI or container | Terminal, CSV, JSON/JSON-pretty and HTML | TLS probing still contacts the target; use only in scope. |
| Nmap - https://svn.nmap.org/nmap/LICENSE | Nmap Public Source License 0.95; local CLI; OEM terms for embedding [17] | CLI/NSE and approved scripts | Normal, XML and other Nmap formats | Port/service probing needs written scope even when non-destructive. |
| curl - https://curl.se/docs/copyright.html | curl license; free/open source and commercial use allowed [43] | CLI or libcurl | Body/headers plus programmable `--write-out` text to stdout [49] | Ordinary public navigation is low risk; mutation/replay belongs in scope. |
| httpx - https://github.com/projectdiscovery/httpx | MIT; free self-hosted CLI [45] | CLI pipelines using HTTP probes | JSONL and CSV; optional request/response capture [45] | High concurrency is not pre-authorization-safe. |
| mitmproxy - https://github.com/mitmproxy/mitmproxy | MIT; free self-hosted [11] | CLI, TUI, web UI and Python add-ons | Native flow files and HAR | Only intercept controlled accounts and devices; sanitize tokens before sharing. |
| Playwright - https://playwright.dev/docs/trace-viewer | Apache-2.0; free self-hosted libraries/runners | Node.js, Python, Java or .NET tests and CLI | Trace archive and HTML report with actions, network, console and errors [30] | Ideal for approved consent/rights workflows; traces contain sensitive data. |
| Schemathesis - https://github.com/schemathesis/schemathesis | MIT; free self-hosted [19] | CLI, Python/pytest, CI against OpenAPI or GraphQL | Minimal curl reproducer, JUnit XML, HAR and integrations | Property-based generation is active testing; use only against approved API/test data. |
| RESTler - https://github.com/microsoft/restler-fuzzer | MIT; free self-hosted [21] | Compile OpenAPI to grammar, then check/test/fuzz | `grammar.json`, compiler logs, test logs and bug buckets [53] | Stateful fuzzing is aggressive and should prefer a staging clone. |
| Newman - https://github.com/postmanlabs/newman | Apache-2.0; free self-hosted Postman collection runner [14] | CLI, Node API, Docker and CI | CLI, JSON and JUnit reports; additional reporters available | Run only an owner-approved collection with seeded values. |

### Data, code, dependency and cloud-control tools

| Tool and exact URL | License and delivery | How driven | Relevant output | Role in MUJ assurance |
|---|---|---|---|---|
| Retire.js - https://github.com/RetireJS/retire.js/ | Apache-2.0; free/self-hosted [42] | CLI, browser extension, Burp/ZAP add-on or headless scan [42] | Known-library warnings and CycloneDX SBOM [42] | Confirm both jQuery bundles and remove stale copies. |
| Microsoft Presidio - https://microsoft.github.io/presidio/ | MIT; free/self-hosted Python, Docker and services [24] | Python API, REST services and custom recognizers | JSON-like entity type, offsets and confidence | Find Aadhaar-like, health, contact and credential data in approved exports; human validation required. |
| Gitleaks - https://github.com/gitleaks/gitleaks | MIT; free/self-hosted [28] | CLI, pre-commit and CI | JSON, CSV, JUnit and SARIF reports | Detect secrets in owner-supplied repositories and history. |
| Semgrep Community Edition - https://github.com/semgrep/semgrep | LGPL-2.1 engine; free/self-hosted; commercial platform optional [54][31] | CLI, IDE, pre-commit or CI rules | Text, JSON, SARIF and JUnit-style CI output | Find verbose-error settings, weak crypto usage, logging of PII and unsafe DOM sinks. |
| Trivy - https://github.com/aquasecurity/trivy | Apache-2.0; free/self-hosted [26] | CLI, CI, container or server mode | Table, JSON, SARIF, CycloneDX and SPDX | Scan repositories, images, IaC, secrets and dependency inventory. |
| OWASP Dependency-Check - https://github.com/dependency-check/DependencyCheck | Apache-2.0; free/self-hosted [18] | CLI, Maven, Gradle, Ant and CI plug-ins | HTML, XML, CSV, JSON, JUnit, SARIF and platform reports | Owner-side .NET/JavaScript build inventory and vulnerability correlation. |
| Microsoft Purview Data Map - https://learn.microsoft.com/en-us/purview/data-map | Microsoft hosted commercial service; licensing/consumption applies | Portal, registered-source scans and APIs | Searchable metadata map, lineage and classifications; built-in scanning keeps the map current [13] | Owner-side inventory of databases, storage and analytics; not a black-box tool. |
| Prowler - https://github.com/prowler-cloud/prowler | Apache-2.0 open-source self-hosted; hosted offering also available [27] | CLI, container, UI/API with authorized cloud roles | CSV, JSON/OCSF and HTML findings | Review authorized Azure configuration and compliance; does not test portal business logic. |
| Wazuh - https://github.com/wazuh/wazuh | GPL-2.0; free self-hosted, commercial hosting/support available [32] | Agents, manager, rules, API and dashboard | JSON alerts, indexed events and dashboards | Correlate IIS, Windows and application events where deployed. |
| OpenTelemetry - https://opentelemetry.io/docs/what-is-opentelemetry/ | Apache-2.0; vendor-neutral open-source instrumentation [25] | SDKs, automatic instrumentation and Collector | OTLP traces, metrics and logs | Add correlation IDs and exception telemetry without exposing details to users. |
| Microsoft Sentinel - https://learn.microsoft.com/en-us/rest/api/securityinsights/incidents?view=rest-securityinsights-2025-09-01 | Microsoft Azure commercial SaaS | Connectors, KQL analytics, automation/playbooks and REST | Incidents, alerts, bookmarks and entities through REST [12][55] | Central CERT-In clock and cross-tenant incident case if MUJ licenses it. |
| Azure Monitor Logs - https://learn.microsoft.com/en-us/azure/azure-monitor/logs/api/overview | Microsoft Azure commercial SaaS | Log Analytics/KQL, REST, CLI, PowerShell or SDK; Entra OAuth required | JSON `tables`, `columns` and `rows`; alerts and workbooks [40] | Query IIS/app/Azure telemetry and prove 180-day India-resident retention configuration. |
| Microsoft Graph sign-ins - https://learn.microsoft.com/en-us/graph/api/signin-list?view=graph-rest-1.0 | Microsoft hosted API under Entra/M365 licensing | Authorized `GET /auditLogs/signIns` with OData filters [48] | JSON sign-in objects and pagination links [48] | Correlate users, applications, tenants, risk and Conditional Access. |

**Tooling takeaway:** None of these products should be pointed at the live portal merely because it is public. For this target, "free" describes licensing, not authorization.

## NO-TOOL GAPS

| Gap no tool can decide | Required manual evidence | Acceptance criterion |
|---|---|---|
| Who is the Data Fiduciary for each SLCM purpose | MUJ resolutions, vendor contracts, tenant/app ownership and data-flow interviews | One accountable owner and processor chain per purpose. |
| Whether consent is genuinely free and specific | UI review, consequence-of-refusal analysis and legal basis | No unnecessary field or bundled unrelated purpose; withdrawal path documented. |
| Whether each field is necessary | Business-owner challenge and statutory/academic record rules | Purpose and necessity recorded for every sensitive field. |
| Whether retention is lawful | Retention schedule, examination/finance/legal rules, backup design | Trigger, duration, exception, deletion mechanism and evidence for every store. |
| Whether a breach occurred | Correlated application, database, identity and storage evidence | Scope distinguishes vulnerability, attempted abuse and confirmed unauthorized access. |
| Whether the six-hour clock started | Timeline showing first notice to any covered MUJ function | Defensible clock-start event and no approval bottleneck. |
| Whether a rights response is complete | Seeded request compared with every system and processor | Identity verified; all in-scope data/actions accounted for; exceptions explained. |
| Whether child-data rules apply to a student | Verified age and applicable exemption analysis | Age-dependent processing path and consent evidence where required after commencement. |
| Whether all three tenants are necessary | Architecture and identity-governance review | Each tenant has purpose, owner, logging, offboarding and incident role. |
| Whether a scanner finding is exploitable | Safe code-path review or owner-approved test in staging | Reachability and impact established without production personal data. |

## BUILD CANDIDATES

| Candidate | Minimum viable behavior | Why existing tools do not close it | Safe development path |
|---|---|---|---|
| **Indian obligation compiler** | Versioned YAML/JSON for SPDI, CERT-In and phased DPDP duties, effective dates, evidence and owners | Generic GRC tools rarely encode the split 6-hour, 72-hour, 180-day and phased dates correctly | Build entirely offline from cited public texts; require legal review before production use. |
| **Incident clock broker** | Start clock, classify CERT/DPDP applicability, collect available facts, warn at internal SLOs, archive receipts | SIEMs raise incidents but do not determine Indian legal timing or non-transferability | Test with tabletop cases and synthetic events; never send a real filing automatically. |
| **Two-account privacy harness** | Compare seeded objects, roles and documents while redacting identifiers | DAST tools find HTTP differences but do not understand ownership or legal data category | Use only after signed scope, with accounts and objects created for the exercise. |
| **Differential error-family monitor** | Normalize status, template family, length bucket and exception correlation ID | Generic WAF rules may miss stable application-specific oracles | Train on synthetic staging errors; deploy detection before any authorized validation. |
| **Rights-and-erasure verifier** | Seed a record, exercise correction/erasure, then verify database, cache, index and processor state | Workflow tools cannot prove all replicas and backups follow the decision | Owner-side staging first; production only through an approved privacy procedure. |
| **Cross-tenant evidence correlator** | Join Entra correlation IDs, application request IDs and Azure log records across the three tenants | Graph and Monitor expose data separately | Read-only authorized service principals, least privilege and immutable query audit. |
| **Privacy-safe evidence packager** | Hash artifacts, redact tokens/Aadhaar/medical content, preserve timestamps and generate a disclosure appendix | HAR, traces and proxy histories commonly contain secrets | Offline processing; dual review before evidence leaves MUJ. |
| **Retention proof sampler** | Select synthetic records approaching expiry and verify deletion jobs and exceptions | Catalogs show location, not that deletion occurred | Run on test records and compare expected versus actual lifecycle events. |

**Build takeaway:** The best club contribution is not another scanner. It is an evidence layer that makes authorization, legal clocks, ownership, redaction and reproducibility first-class.

## Authorization Boundary: What Is Safe Now and What Needs the Letter

### Safe before target-specific authorization

The following activities do not require interacting with the portal beyond normal public browsing:

1. Read public statutes, Rules, CERT-In directions, MUJ governance pages, privacy notices and vendor documentation.
2. Build the legal-obligation register, incident templates, test matrix and evidence-redaction process offline.
3. Inspect code, logs, configurations or exports only when MUJ has voluntarily supplied them for that purpose.
4. Build synthetic SLCM-like applications and seeded datasets for tool training.
5. Conduct a tabletop incident using fictional users, records, tenants and timestamps.
6. Review the already supplied measurements without sending new requests.

Normal viewing of intentionally public pages is lower risk, but it is not a blanket authorization for scanning, enumeration, replay or mutation. Section 43 of the IT Act addresses access to a computer resource without permission [8][56]. The conservative club rule should therefore be: **no new target-directed security tooling until written permission specifies it**.

### Requires the signed scope letter

The letter should expressly authorize hostnames, IPs, dates, source IPs, test intensity, allowed methods, emergency contacts, data handling, stop conditions and disclosure rules. It is required for TLS scanning, port validation, automated crawling, template scanning, error-trigger mutation, method testing, rate/lockout testing, upload tests, API property testing, RESTler, authentication testing, log-correlation simulation and any attempt to validate the `enc` behavior further.

### Requires both the letter and two controlled accounts

Two or more seeded accounts are required for object-level authorization, role changes, marks/fee isolation, medical-document isolation, APAAR linkage, profile correction, consent withdrawal, logout/session lifecycle, concurrent-session behavior and rights requests. Tests must use only synthetic records. No student, employee or patient data should be accessed to prove a vulnerability.

### Requires owner-side cooperation beyond two accounts

Purview, Prowler, Azure Monitor, Graph sign-in review, source scanning, retention validation, backup deletion, processor-contract review and the CERT-In tabletop require authorized internal roles or supplied evidence. A black-box tester cannot close these controls.

## Synthesis

The legal frameworks operate on different mechanisms and horizons. **SPDI** is category-based and current: it gives heightened treatment to medical, health, payment, credential and biometric data, with privacy-policy, consent, necessity, retention, grievance and security requirements [33]. **CERT-In** is incident-centered and current: it prioritizes rapid reporting, synchronized evidence, India-resident logs and a named contact [3][29]. **DPDP** is broader and person-centered but substantively future on the report date: it adds general digital-personal-data duties, rights, child controls, erasure and a two-level breach-notification system [6][20].

The first non-obvious tension is retention. DPDP readiness emphasizes erasure after purpose expiry or consent withdrawal, while CERT-In requires a rolling 180 days of ICT logs and Rule 6 will require certain evidence for one year [6][3][16]. The resolution is not "keep everything." MUJ should separate security metadata from content, minimize personal values in logs, document the legal purpose and delete each class on its own schedule.

The second tension is speed versus certainty. CERT-In requires an initial report within six hours but permits supplementation [29]. DPDP Rule 7, when operative, similarly separates immediate notices from a detailed 72-hour Board report [20]. The reporting process must therefore support provisional facts, confidence labels and versioning rather than wait for a perfect forensic conclusion.

The third tension is automation versus authorization. The most valuable technical tests are authenticated cross-account comparisons, yet those are also the tests most likely to touch sensitive student records. The solution is a signed scope, seeded accounts, synthetic files, strict stop conditions and owner-side logs. Tool power without that governance would undermine the data-protection objective the club is trying to assess.

Across scope, mechanism and evidence, the strategies compare as follows:

| Dimension | Public pre-authorization review | Authorized black-box test | Owner-side assurance |
|---|---|---|---|
| Scope | Law, public notices, supplied observations, offline artifacts | Approved live routes and seeded identities | Code, contracts, cloud, databases, logs, backups and processors |
| Mechanism | Documentation and threat modeling | Controlled HTTP/browser/API behavior | Configuration, telemetry, lifecycle and governance evidence |
| Strength | Safe and fast | Proves external control behavior | Can establish legal accountability and full data lifecycle |
| Limitation | Cannot prove confidentiality or deletion | Cannot see hidden stores or contracts | Requires MUJ staff, privilege and audit controls |
| Time horizon | Immediate | Campaign window | Continuous compliance through DPDP commencement and beyond |

## VERDICT

**Verdict: PARTIAL technically, but LEGALLY UPGRADED and ready for an authorized second phase.**

The supplied campaign provides credible pre-authentication evidence of weak TLS compatibility, missing HSTS, verbose production errors, an externally distinguishable `enc` failure sequence, a cookie hardening gap and old jQuery bundles. It also records meaningful negatives: only 443 reachable, anti-forgery enforcement, inaccessible diagnostic endpoints and unsuccessful host/proxy trust bypass attempts. None of those observations proves compromise or personal-data disclosure.

The campaign cannot reach a full assurance verdict because it has not authenticated. It therefore has no evidence on the controls most closely tied to marks, fees, Aadhaar, APAAR and medical documents: object authorization, role segregation, tenant routing, disclosure logging, correction, erasure, retention and incident scope. Those tests must remain gated behind the signed letter and controlled accounts.

The reporting program should be treated as a control in its own right. Today, MUJ should be able to prove a named CERT-In contact, synchronized clocks, 180-day India-resident ICT logs, an Annexure I decision tree, and an initial filing within six hours using available information [3][29]. In parallel, it should implement and rehearse the broader DPDP safeguards, rights and breach notices scheduled for the 18-month phase [44][20][16].

**Confidence: High (0.88) on the legal timetable, CERT-In requirements, SPDI baseline, public tool characteristics and authorization boundary; Moderate (0.68) on target risk prioritization because the technical measurements were supplied rather than independently reproduced; Low on authenticated confidentiality, retention and rights effectiveness because those areas remain untested.**

## References

1. *Updated Regulations - Unique Identification Authority of India | Government of India*. https://uidai.gov.in/en/updated-regulations
2. *2016*. https://esanjeevani.mohfw.gov.in/assets/guidelines/ehr_guidlines.pdf
3. *No. 20(3)/2022-CERT-In Government of India Ministry of Electronics and Information Technology (MeitY) Indian Computer Emergency Response Team (CERT-In) Electronics Niketan,*. https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf
4. *Privacy Policy | APAAR*. https://apaar.education.gov.in/privacy-policy
5. *Circular 8 Of 2025 Revised Guidelines For Adv Hsm*. https://uidai.gov.in/images/Circular_8_of_2025-Revised_guidelines_for_ADV__HSM.pdf
6. [xxxGIDHxxx xxxGIDExxx vlk/kkj.k Hkkx [k.M izkf/kdkj ls izdkf'kr PUBLISHED BY AUTHORITY lañ ubZ fnYyh] 'kqØokj] vxLr 11] 2023@Jko.k 20] 1945](https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf)
7. *DPDP Rules, 2025 Notified*. https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc20251117695301.pdf
8. *It Act 2000 Updated*. https://indiacode.nic.in/bitstream/123456789/13116/1/it_act_2000_updated.pdf
9. *ZAP – Report Generation*. https://www.zaproxy.org/docs/desktop/addons/report-generation/
10. *GitHub - testssl/testssl.sh: Testing TLS/SSL encryption anywhere on any port · GitHub*. https://github.com/testssl/testssl.sh
11. *GitHub - mitmproxy/mitmproxy: An interactive TLS-capable intercepting HTTP proxy for penetration testers and software developers. · GitHub*. https://github.com/mitmproxy/mitmproxy
12. *Incidents - REST API (Azure Sentinel) | Microsoft Learn*. https://learn.microsoft.com/en-us/rest/api/securityinsights/incidents?view=rest-securityinsights-2025-09-01
13. *Learn about Microsoft Purview Data Map | Microsoft Learn*. https://learn.microsoft.com/en-us/purview/data-map
14. *GitHub - postmanlabs/newman: Newman is a command-line collection runner for Postman · GitHub*. https://github.com/postmanlabs/newman
15. *Reporting scan results - PortSwigger*. https://portswigger.net/burp/documentation/desktop/running-scans/reporting
16. *Rule 6 DPDP Rules 2025: Reasonable security safeguards*. https://dpdprules.org/rules/6
17. *svn.nmap.org*. https://svn.nmap.org/nmap/LICENSE
18. *GitHub - dependency-check/DependencyCheck: OWASP dependency-check is a software composition analysis utility that detects publicly disclosed vulnerabilities in application dependencies. · GitHub*. https://github.com/dependency-check/DependencyCheck
19. *GitHub - schemathesis/schemathesis: Catch API bugs before your users do · GitHub*. https://github.com/schemathesis/schemathesis
20. *Rule 7 DPDP Rules 2025: Intimation of personal data breach*. https://dpdprules.org/rules/7
21. *GitHub - microsoft/restler-fuzzer: RESTler is the first stateful REST API fuzzing tool for automatically testing cloud services through their REST APIs and finding security and reliability bugs in these services. · GitHub*. https://github.com/microsoft/restler-fuzzer
22. *GitHub - projectdiscovery/nuclei: Nuclei is a fast, customizable vulnerability scanner powered by the global security community and built on a simple YAML-based DSL, enabling collaboration to tackle trending vulnerabilities on the internet. It helps you find vulnerabilities in your applications, APIs, networks, DNS, and cloud configurations. · GitHub*. https://github.com/projectdiscovery/nuclei
23. *Rule 1 DPDP Rules 2025: Short title and commencement*. https://dpdprules.org/rules/1
24. *Index - Presidio*. https://microsoft.github.io/presidio/
25. *What is OpenTelemetry?*. https://opentelemetry.io/docs/what-is-opentelemetry/
26. *GitHub - aquasecurity/trivy: Find vulnerabilities, misconfigurations, secrets, SBOM in containers, Kubernetes, code repositories, clouds and more · GitHub*. https://github.com/aquasecurity/trivy
27. *GitHub - prowler-cloud/prowler: Prowler is the world’s most widely used open-source cloud security platform that automates security and compliance across any cloud environment. · GitHub*. https://github.com/prowler-cloud/prowler
28. *GitHub - gitleaks/gitleaks: Find secrets with Gitleaks 🔑 · GitHub*. https://github.com/gitleaks/gitleaks
29. *Table of Contents 01 03 08 16*. https://www.cert-in.org.in/PDF/FAQs_on_CyberSecurityDirections_May2022.pdf
30. *Trace viewer | Playwright*. https://playwright.dev/docs/trace-viewer
31. *GitHub - semgrep/semgrep: Lightweight static analysis for many languages. Find bug variants with patterns that look like source code. · GitHub*. https://github.com/semgrep/semgrep
32. *GitHub - wazuh/wazuh: Wazuh - The Open Source Security Platform. Unified XDR and SIEM protection for endpoints and cloud workloads. · GitHub*. https://github.com/wazuh/wazuh
33. [         [भाग II- खण्ड 3(i)]                                          भारत का राजपत्र : असाधारण                                                  7                                                  ](https://prsindia.org/files/bills_acts/bills_parliament/2011/IT_Rules_2011.pdf)
34. *Registrar - Manipal University Jaipur*. https://www.jaipur.manipal.edu/administration-registrar.php
35. *Microsoft Word - THE MANIPAL UNIVERSITY, JAIPUR ACT, 2011.doc*. https://prsindia.org/files/bills_acts/acts_states/rajasthan/2011/2011Rajasthan21.pdf
36. *DPDP Act + Rules 2025: Effective Sections, Deadlines and What To-Do Next*. https://www.dpo-india.com/Resources/privacy_laws_in_India/DPDP-Act+Rules-2025-Effective-Sections,Deadlines-What-To-Do-Next.pdf
37. *Cert-In - Home Page*. https://www.cert-in.org.in/SecurityIncident.jsp
38. *Cert-In - Contactus*. https://www.cert-in.org.in/s2cMainServlet?pageid=CONTACTUS
39. *NVD - CVE-2019-11358*. https://nvd.nist.gov/vuln/detail/CVE-2019-11358
40. *Azure Monitor Logs Query API Overview - Azure Monitor | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/azure-monitor/logs/api/overview
41. *NVD - CVE-2015-9251*. https://nvd.nist.gov/vuln/detail/CVE-2015-9251
42. *GitHub - RetireJS/retire.js: scanner detecting the use of JavaScript libraries with known vulnerabilities. Can also generate an SBOM of the libraries it finds. · GitHub*. https://github.com/RetireJS/retire.js/
43. *curl - copyright*. https://curl.se/docs/copyright.html
44. [2 G.S.R. 843(E).––– ] , Jt.](https://dpdpa.in/notification_timeline_act.pdf)
45. *GitHub - projectdiscovery/httpx: httpx is a fast and multi-purpose HTTP toolkit that allows running multiple probes using the retryablehttp library. · GitHub*. https://github.com/projectdiscovery/httpx
46. *NVD - CVE-2020-11022*. https://nvd.nist.gov/vuln/detail/CVE-2020-11022
47. *Data Platform Logs*. https://learn.microsoft.com/en-us/azure/azure-monitor/logs/data-platform-logs
48. *List signIns - Microsoft Graph v1.0 | Microsoft Learn*. https://learn.microsoft.com/en-us/graph/api/signin-list?view=graph-rest-1.0
49. *Write out - everything curl*. https://everything.curl.dev/usingcurl/verbose/writeout.html
50. *http://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References*. http://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References
51. *http://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html*. http://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html
52. *http://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html*. http://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
53. *restler-fuzzer/docs/user-guide/Compiling.md at main ... - GitHub*. https://github.com/microsoft/restler-fuzzer/blob/main/docs/user-guide/Compiling.md
54. *Important updates to Semgrep OSS*. https://semgrep.dev/blog/2024/important-updates-to-semgrep-oss/
55. *Microsoft Sentinel REST API | Microsoft Learn*. https://learn.microsoft.com/en-us/rest/api/securityinsights/
56. *Section 43 in The Information Technology Act, 2000*. https://indiankanoon.org/doc/39800/
