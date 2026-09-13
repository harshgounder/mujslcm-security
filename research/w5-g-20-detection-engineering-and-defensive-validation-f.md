# From Findings to Signals: MUJ SLCM Detection Plan

## Executive Summary

- **Campaign Blindness**: The supplied campaign observed verbose ASP.NET errors, stable response-size families, method differentials, and a three-branch `enc` oracle, but it produced no evidence that any control logged, alerted on, or triaged the activity. That makes the detection result **ABSENT**, not "clean." -> Treat an alert, an incident record, and a reconciled server log as mandatory exit criteria for every future security test.

- **Error Oracle Priority**: Different server responses can disclose hidden state; MITRE classifies this pattern as an observable response discrepancy [24], while OWASP recommends client errors that do not expose implementation details [7]. The supplied 4,942-byte, 5,084-byte, and empty-value branches are therefore both a remediation target and an unusually useful defensive canary. -> Normalize the external status/body while logging a server-side reason code and correlation ID.

- **Authorization Remains Unknown**: The campaign never authenticated. CSRF, horizontal authorization, role enforcement, logout, session rotation, and object ownership were therefore not validated. IDOR/BOLA occurs when user-controlled object references reach data without sufficient authorization [32][19]. -> Do not infer safety from the unauthenticated results; require a signed scope letter and two controlled accounts before testing these controls.

- **Transport Is Measurable but Not Yet Defensible**: The supplied observation says TLS 1.0 through 1.3 are offered and HSTS is absent. OWASP states that public web applications should default to TLS 1.3, may retain TLS 1.2 for compatibility, and must disable TLS 1.0 and 1.1 [25]; HSTS makes supporting browsers consistently request HTTPS and prevents bypass of certificate warnings [25]. -> Disable legacy protocol negotiation and stage HSTS only after confirming every required hostname supports HTTPS.

- **Layered Telemetry Is Necessary**: IIS W3C logs can record client IP, method, URI, query, status, substatus, byte counts, latency, user agent, and referrer [12]. Application Insights can correlate requests through `operation_Id`, `operation_Name`, and `operation_ParentId` [2]. -> Join edge, IIS, application, and identity evidence with one sanitized correlation ID rather than expecting one product to see the whole sequence.

- **Three Tenants Multiply Blind Spots**: Microsoft Entra risk reporting covers risky users, risky sign-ins, risky workload identities, and risk detections, with CSV export or SIEM integration [5]. A three-tenant identity arrangement can split evidence and ownership. -> Assign a named log owner in each tenant, stream the applicable sign-in and audit categories centrally, and test cross-tenant correlation with designated canary accounts.

- **Tools Do Not Prove Detection**: ZAP, Nuclei, Burp, ffuf, TLS scanners, and authorization extensions can reproduce test traffic, but none proves that MUJ personnel received or acted on an alert. ZAP's Automation Framework supports job assertions and meaningful exit codes [10], which makes it useful for repeatability, not as a substitute for blue-team evidence. -> Pair every permitted test case with an expected log source, analytic rule, owner, and maximum triage time.

- **Pre-Authorization Work Must Stay Passive**: Public-document research, DNS and certificate-transparency review, offline examination of supplied captures, local lab reproduction, and review of vendor documentation do not require sending security-test traffic to the portal. -> Run all scanners, altered requests, exception triggers, header mutations, and authentication tests only under the signed authorization described below.

- **Highest-Value Build Candidate**: General scanners compare status, length, words, or signatures, but they do not understand that the three `enc` branches should collapse to one public response while remaining distinguishable in protected telemetry. -> Build a small, rate-limited response-shape and log-reconciliation harness rather than adding another broad scanner.

## Scope, Provenance, and Authorization Boundary

This report treats the portal characteristics and measurements in the request as **user-supplied observations dated 2026-09-13**. They were not independently retested for this report. No conclusion below should be read as confirmation that the target is exploitable, that an edge control is absent, or that the three Entra tenants have a particular trust relationship. "No attributable edge control" means that the supplied campaign did not attribute one; it does not prove that no reverse proxy, managed gateway, or provider-side control exists.

The report uses public vendor documentation and established security guidance. It does not provide private chain-of-thought. Instead, the next table gives the decision rationale needed for review: observation, bounded interpretation, uncertainty, and defensive action. This is more auditable than an unverifiable internal monologue.

| Supplied observation | Bounded interpretation | Important uncertainty | Defensive decision |
|---|---|---|---|
| Port 443 alone was reachable | The observed public surface was narrow | Other addresses, private services, or conditional listeners were not assessed | Maintain an asset inventory and compare it with passive exposure data |
| Four verbose YSOD triggers, `customErrors` reportedly off | Error handling exposes implementation detail | The exact configuration and whether responses differ by client location are unverified | Return a generic public error and retain detailed diagnostics only in protected logs |
| Antiforgery enforcement; cookie HttpOnly but not Secure | A CSRF control exists, while cookie transport policy may be incomplete | Token binding, rotation, SameSite behavior, and all state-changing actions remain untested | Add `Secure`, verify SameSite and HTTPS-only operation, then test with controlled accounts |
| `trace.axd` 403 and `elmah.axd` 404 | Those two unauthenticated requests did not disclose diagnostic content | A 403/404 does not prove the handlers are removed or unreachable through every route | Remove or tightly restrict diagnostic handlers and alert on attempts to reach them |
| MVC 2,733-byte and IIS 1,216-byte error families | Two processing layers appear externally distinguishable | Body size alone does not identify the exact component | Normalize public errors; use server-side layer/reason fields for operations |
| POST/PUT 411; other non-GET methods 404 | Method handling is inconsistent by verb or pipeline stage | **Inference:** 411 can mean a required message length, not proof that the route is safely GET-only | Review route and IIS verb policy from configuration; do not perform broader method tests without authorization |
| Three `enc` branches with FormatException/CryptographicException | Input validation and cryptographic processing appear externally distinguishable | The data purpose, cryptographic construction, and security impact remain unknown | Collapse external responses and instrument branch-specific protected events |
| Host and forwarding-header attempts were clean | The tested cases did not demonstrate a trust-boundary bypass | Detection was not demonstrated, and untested routing paths may exist | Enforce a host allowlist and alert on rejected or forwarded-host anomalies |
| Campaign never authenticated | Authenticated attack classes were not covered | The most consequential authorization and session controls are unknown | Gate all authenticated validation behind the letter and two test accounts |

Authentication only establishes identity; authorization determines what an authenticated party may access or do [33]. An antiforgery token addresses a different question: whether a browser request was intentionally initiated within the application context. Microsoft describes the MVC pattern as a random cookie token plus a form token, both of which must return for validation [34]. Neither control substitutes for object-level authorization on every request.

### What is safe before authorization

Safe pre-authorization work is limited to public-source and offline activity: public DNS, registration and certificate-transparency records; published technology documentation; review of the supplied response samples; development of rules against synthetic logs; local training labs; code review of software that the university has deliberately provided; and tabletop exercises. A normal student visiting a page for its intended purpose is not a penetration test, but the club should not turn ordinary access into systematic measurement without institutional approval.

### What requires the letter

Any security-motivated connection to the portal should be treated as in-scope only after the signed letter: TLS enumeration, header comparison, technology fingerprinting, method changes, known-path checks, parameter mutation, spidering, forced browsing, automated scanning, replay, or validation of the supplied error triggers. The letter should name source IPs, dates, rate and concurrency ceilings, routes, prohibited payloads, emergency contacts, data handling, stop conditions, and expected telemetry.

CSRF, session, object authorization, role comparison, and identity validation require both the letter and the two designated test accounts. Entra sign-in canaries additionally require approval from the owner of each affected tenant. Password spraying, real-student account testing, MFA fatigue, lockout induction, and access to another person's records remain prohibited.

## Technique Universe: Eleven Classes, Eleven Detection Counterparts

The following is the coverage-complete technique universe for the supplied campaign. It is not a claim that every possible web attack is listed; it covers every observed technology or behavior named in the request and the major defensive test classes that follow from them.

| Class | Defensive validation objective | Manual or automated method under authorization | Detection counterpart | Required gate |
|---|---|---|---|---|
| 1. Exposure and service posture | Confirm intended public addresses, ports, certificates, and ownership | Compare asset inventory with a narrowly scoped network/TLS result; avoid broad address sweeps | Alert when an unmanaged IP, certificate, hostname, or listener appears | Letter for active validation; passive records before it |
| 2. TLS and HTTPS policy | Verify TLS 1.0/1.1 rejection, certificate chain, HTTPS redirect, HSTS, and secure cookies | TLS scanner plus browser/header review; config review is preferred | Scheduled configuration drift check; certificate-expiry and legacy-protocol alert | Letter for target scanning |
| 3. Technology and dependency inventory | Reconcile IIS, MVC, .NET, and both jQuery bundles with owned build artifacts | Remote fingerprint only as a hint; authoritative SBOM/SCA runs against the build | New component/version or vulnerable dependency creates a ticket | Letter for remote checks; build review can be internal |
| 4. Error handling and YSOD | Ensure malformed or unexpected input yields a generic public response | Replay only the pre-agreed benign canaries and compare status, type, length, hash, and latency | Cluster exceptions and response shapes by route, source, and short window | Letter; staging preferred |
| 5. Diagnostic and hidden-resource exposure | Verify diagnostic handlers are removed or strongly restricted | Check only an approved path list; no general content discovery unless explicitly scoped | Alert on requests for diagnostics, backups, source maps, and known administration paths | Letter |
| 6. HTTP method and request filtering | Confirm allowed methods from configuration and safely validate representative denials | Inspect MVC routes and IIS `<verbs>` first; send a tiny approved method matrix second | Baseline `cs-method`; alert on rare methods and denial bursts | Letter |
| 7. Structured-input and cryptographic oracle | Make invalid encoding, invalid ciphertext, empty input, and semantic rejection externally indistinguishable | A custom differential harness is preferable to a general fuzzer | Detect three or more response/exception classes for one parameter and source | Letter; use inert test data |
| 8. Host, proxy, and absolute-URI trust | Verify a canonical-host allowlist and trusted-proxy boundary | Config review followed by a small pre-agreed header matrix | Reject and log non-allowlisted Host values, unexpected forwarded headers, and absolute-form anomalies | Letter |
| 9. CSRF and session protection | Verify antiforgery enforcement, cookie flags, SameSite, session rotation, logout, and origin policy | Browser proxy with one test account; negative controls on designated harmless actions | Log token validation failures, origin/referrer mismatch, and state-change attempts without valid context | Letter plus account |
| 10. BOLA/IDOR and role enforcement | Prove that account A cannot read or modify account B's test objects | Build a role-object-action matrix and compare two test accounts | Join authenticated principal, route, action, object owner, decision, and policy reason | Letter plus two accounts |
| 11. Entra and campaign detectability | Prove that web and identity canaries create central evidence and an owned incident | Designated successful/failed canaries only; reconcile every sent event with logs and alerts | Entra risk/sign-in analytics plus cross-layer correlation and SOC workflow | Letter, test accounts, and tenant-owner consent |

IIS supports explicit allow/deny configuration for HTTP verbs [21], but a status-code pattern alone does not prove which setting produced the result. Likewise, an unguessable object ID is only defense in depth; the application still must deny unauthorized access regardless of identifier predictability [35]. Authorization checks must execute on the server or another trusted enforcement layer, not only in client code [36].

**Case study - the `enc` differential.** The campaign's three response branches are a compact example of observation -> mechanism -> implication -> recommendation. Observation: invalid base64, valid base64 with invalid cryptographic content, and empty input reportedly produce distinct failures and sizes. Mechanism, stated as inference: parsing and decryption exceptions appear to cross the public error boundary before a common error mapper runs. Implication: an outsider may classify internal processing state, while defenders should see a similarly distinctive sequence. Recommendation: return one stable client response, record internal classifications such as `ENC_FORMAT`, `ENC_CRYPTO`, and `ENC_EMPTY` in protected telemetry, and alert when one source exercises multiple classes rapidly. MITRE notes that response discrepancies can reveal information even when each response seems individually harmless [24].

## Tool Coverage Matrix: Complete Surveyed Set

A literal list of "every tool" cannot be made finite: generic HTTP clients, scripting languages, commercial scanners, browser extensions, and private frameworks can all perform overlapping operations. The defensible interpretation is a **coverage-complete surveyed set**: every technique class above has at least one repeatable tool, a manual fallback, and a detection counterpart. Tool URLs are written exactly so the club can verify current licensing before deployment.

| Tool and exact URL | Licence and access model | How it is driven | Relevant use and output | Safety classification |
|---|---|---|---|---|
| Nmap - https://nmap.org/ | Nmap Public Source License; free source-available builds; commercial terms may apply to redistribution; self-hosted; no BYOK | CLI and NSE scripts | Service/port validation; normal, XML, grepable, and script output | Active network traffic; letter required |
| curl - https://curl.se/ | curl license; free/open source; self-hosted; no BYOK | CLI or libcurl | Precisely controlled HTTP request; response body/headers, trace text, and `--write-out` measurements | Letter for altered target requests |
| httpx - https://github.com/projectdiscovery/httpx | MIT; free/self-hosted; no BYOK [23] | CLI with host lists, raw requests, or Burp input [23] | Status, content length/type, hash, latency, server, technology, IP/ASN/CDN; CSV or JSONL, optionally with request/response [23] | Letter; set low thread and rate limits [23] |
| WhatWeb - https://github.com/urbanadventurer/WhatWeb | GPL-2.0; free/self-hosted; no BYOK [15] | CLI with selectable aggression | Identifies servers, frameworks, JavaScript libraries, versions, and error clues; JSON, XML, SQL, and other formats [15] | Level 1 still makes a request; letter required for the portal |
| testssl.sh - https://github.com/testssl/testssl.sh | GPLv2; free/self-hosted or container; no BYOK [16] | Standalone CLI or container | TLS protocols, ciphers, and selected cryptographic flaws; CSV, two JSON formats, and HTML [16] | Letter; one approved hostname only |
| SSLyze - https://github.com/nabla-c0d3/sslyze | AGPL; free/self-hosted; no BYOK [17] | CLI or Python API [17] | Certificate, cipher, curve, and known TLS weakness analysis; JSON [17] | Letter; rate ceiling required |
| Retire.js - https://github.com/RetireJS/retire.js | Apache-2.0; free/self-hosted; no BYOK | CLI, build integration, and supported scanner integrations | Offline or approved-page JavaScript dependency findings; console/JSON-oriented output | Prefer build-artifact scanning; remote page retrieval needs letter |
| OWASP Dependency-Check - https://owasp.org/www-project-dependency-check/ | Apache-2.0; free/self-hosted; optional vulnerability-data integrations; no AI BYOK | CLI, Maven/Gradle/Ant plugins, and CI integrations | Dependency inventory and vulnerability reports including HTML, JSON, XML, SARIF, and JUnit | Safe on owned source/build artifacts |
| OWASP ZAP - https://github.com/zaproxy/zaproxy | Apache-2.0, free/open source [14]; desktop, daemon, Docker, or CI; no BYOK | GUI/API or one YAML Automation Framework plan [10] | Proxy, spider, passive/active scan, authentication, scripted requests, and reports. Framework jobs include requestor, spiders, active scan, passive scan, imports, and reporting [10] | Passive proxying of approved traffic or active scanning; letter required against portal |
| Nuclei - https://github.com/projectdiscovery/nuclei | MIT; free/self-hosted; optional ProjectDiscovery cloud integrations; no key needed locally [37] | CLI with YAML templates/workflows | Exact-match checks for HTTP, TLS, files, and configuration patterns; console, JSONL, and SARIF-oriented automation | Template behavior varies; permit only reviewed templates under letter |
| ffuf - https://github.com/ffuf/ffuf | MIT; free/self-hosted; no BYOK [20] | CLI with a `FUZZ` position in URL, header, or data [20] | Differential input/path/header testing; filters for status, lines, regex, size, and words; JSON/eJSON/HTML/Markdown/CSV/eCSV [20] | High misuse/noise potential; explicit path/parameter scope and letter required |
| Burp Suite Community - https://portswigger.net/burp/communitydownload | Proprietary; Community Edition is a free manual toolkit [38]; desktop self-hosted; no BYOK | GUI proxy, Repeater, Decoder, Comparer, and extensions | Raw request/response evidence and manual differential testing; project/export capabilities depend on edition | Letter; test accounts for authenticated work |
| Burp Suite Professional/DAST - https://portswigger.net/burp | Proprietary paid products; Professional and DAST are distinct products [11] | Desktop GUI for Professional; DAST server plus CI Docker job | DAST writes JUnit or Burp XML and exposes results in CI or its dashboard [8] | Letter, approved scan configuration, and emergency stop |
| ZAP Access Control Testing - https://www.zaproxy.org/docs/desktop/addons/access-control-testing/ | ZAP add-on under the ZAP open-source ecosystem; self-hosted | Configure context, users, authentication, authorization indicators, and Allowed/Denied/Unknown rules [27] | Compares each approved URL from each user's perspective and reports potential authorization mismatches [27] | Letter plus two test accounts; tightly bound object set |
| AuthMatrix - https://github.com/PortSwigger/auth-matrix | MIT; free Burp extension; self-hosted | GUI matrix of users, roles, requests, expected access, and optional request chains | Replays selected requests per user and records pass/fail authorization comparisons | Letter plus accounts; manually verify semantic ownership |
| Autorize - https://github.com/Quitten/Autorize | Apache-2.0 repository; free Burp/Jython extension; self-hosted | Supply a low-privilege session and let the extension replay captured authorized requests | Highlights likely enforcement differences in an extension results table | Letter plus accounts; response similarity is not proof of data equivalence |
| MDN HTTP Observatory - https://developer.mozilla.org/en-US/observatory/ | Free hosted service/API; no BYOK; service terms apply | Web UI or v2 HTTP API | Header-policy checks with grade, score, status, and result details; the v2 API returns concise JSON [39] | It causes a third party to scan the host; use only with written permission |

**Tooling takeaway.** ZAP is the strongest open-source orchestrator because one YAML plan can include authentication, exact requests, spiders, passive checks, active checks, tests, and a report [10]. Its report job can select risk/confidence, sites, sections, destination, and an installed template [30]. Burp remains strong for analyst-guided comparison, while ffuf and Nuclei are better viewed as narrowly reviewed request generators, not default "scan everything" choices.

**Dependency case study.** The supplied dual jQuery observation should not be converted directly into a vulnerability claim. Remote fingerprinting may misidentify a library, and a file can be present without being reachable in a sensitive path. The authoritative method is to generate an SBOM from the owned build, run Retire.js or Dependency-Check offline, identify which bundle each page actually loads, and remove duplicate or unused versions. A remote WhatWeb result is supporting evidence only; its own documentation describes different aggression levels that trade stealth/speed for reliability [15].

## Detection Architecture: IIS to Three Entra Tenants

The minimum viable architecture has four evidence planes and one workflow plane.

| Plane | Required data | Primary analytics | Evidence of success |
|---|---|---|---|
| Edge or first receiving proxy | Timestamp, source, destination host, original Host, forwarded-host chain, method, path, query-key names, status, bytes, TLS version, rule/action, request ID | Legacy TLS, host allowlist violation, diagnostic-path request, method anomaly, scanning cadence | Raw event plus gateway/WAF action and shared request ID |
| IIS | `c-ip`, `cs-method`, `cs-uri-stem`, sanitized `cs-uri-query`, `sc-status`, `sc-substatus`, `sc-bytes`, `cs-bytes`, `time-taken`, user agent, referrer [12] | Error-family clustering, 403/404/411 burst, route/parameter entropy, rare methods | W3C record queryable centrally within the agreed latency |
| ASP.NET MVC application | Route/action, authenticated subject, session/test tag, object ID hash, object owner hash, authorization decision, antiforgery result, exception class, internal reason, correlation ID | YSOD suppression verification, oracle branch sequence, CSRF failure, cross-account denial | Generic client error tied to detailed protected exception/event |
| Application Insights/Azure Monitor | Request `name`, URL, success, result code, duration [2]; exception type/method/details [2]; operation and parent IDs [2]; authenticated user/session identifiers [2] | Join request -> exception -> dependency; threshold and sequence analytics | Correlated trace visible without exposing sensitive values |
| Entra/Sentinel and SOC | Applicable sign-in, service-principal, managed-identity, audit, provisioning, and risk logs; tenant ID; application ID; controlled-account tag | Risky sign-in, unusual failures, cross-tenant sequence, canary alert | Incident with owner, timestamps, affected tenant, and test-case ID |

IIS W3C fields are necessary but insufficient. They usually do not express MVC exception class, antiforgery result, object ownership, or the application's authorization reason. Failed Request Tracing can be enabled with a bounded log directory and maximum file count [9], but it should be scoped to selected failures because indiscriminate tracing adds volume and can capture sensitive data. Application logging must not record passwords or access tokens [40]. Store parameter names and normalized reason codes where possible; hash test object IDs with a controlled key rather than ingesting student data.

If an Azure Web Application Firewall exists, its logs can preserve performance, access, and other monitoring data [1]. Because the campaign did not attribute an edge control, the first task is a resource and traffic-flow inventory, not immediate WAF tuning. **Inference:** an origin reachable directly around an edge would fragment detection and enforcement. The university should identify the authoritative first receiver, restrict origin ingress to it where architecture permits, and make its request ID available downstream.

Microsoft documents a built-in Sentinel connector for Entra data [4], and Entra diagnostic settings can integrate activity logs with SIEM tools [26]. Repeat that configuration and ownership check for all three tenants. A central rule should retain the originating tenant rather than flattening it away.

### Recommended analytics

| Rule ID | Detection logic | Tuning and response |
|---|---|---|
| WEB-ERR-01 | Same source and route produces at least 3 distinct `(status, byte bucket, exception class)` combinations in 5 minutes | Exclude synthetic monitoring; investigate for oracle discovery |
| WEB-ERR-02 | Public response contains YSOD/stack signatures, or an exception lacks a mapped generic response | Page application owner immediately; preserve correlation ID, not full sensitive body |
| WEB-PATH-01 | Requests for approved diagnostic/admin path indicators, especially mixed 403 and 404 sequences | One event may be reconnaissance; correlate with route entropy and source history |
| WEB-METHOD-01 | Rare or denied methods, or multiple method values against one route | Baseline deployment/monitoring agents; look for 404/411/405 diversity |
| WEB-HOST-01 | Host outside allowlist, unexpected `X-Forwarded-Host`, or proxy chain not issued by trusted receiver | Reject early; inspect direct-origin exposure and cache/reset links |
| WEB-CSRF-01 | Antiforgery validation failure on a state-changing route, grouped by user/session/source | Never log token values; correlate origin/referrer and subsequent success |
| WEB-AUTHZ-01 | Access denied across multiple test objects, or same object requested by multiple principals with inconsistent ownership decisions | Requires application authorization events, not HTTP status alone |
| ID-ENTRA-01 | Controlled-account failure/success/risk sequence or cross-tenant activity outside the exercise window | Attach tenant, app, device, IP, and test case; route to identity owner |
| DET-HEALTH-01 | A scheduled authorized canary was sent but no expected event or alert arrived | This is a monitoring failure, not a passed security test |

OWASP explicitly recommends testing authorization mechanisms and preventing deployment when those tests fail [19]. The same standard should apply to detection: a change that drops the canary event, breaks correlation, or suppresses an expected alert should fail release validation.

## Controlled Validation Playbooks

### Phase 0: Pre-authorization, zero target testing

Build synthetic W3C, application, WAF, and Entra records that represent the supplied campaign. Write the analytics above and confirm that they generate incidents in a lab workspace. Review IIS, MVC, TLS, cookie, logging, Azure, and Entra configuration with the system owners. Generate an SBOM from a controlled build and resolve the two jQuery observations there. This phase can answer whether the detection design is coherent, but it cannot establish whether production telemetry is complete.

### Phase 1: Signed letter, unauthenticated low-impact validation

Use one club-controlled source IP and a unique test-case header or approved query tag that the application strips before business processing. Start with one ordinary baseline request, then only the exact low-impact canaries approved in the letter. Appropriate cases are certificate/TLS policy, canonical host handling, approved diagnostic paths, one representative denied method, and the already known benign error triggers. Do not broaden into wordlists, template packs, recursive spidering, or new parameter discovery.

For each event, the blue team should record five checkpoints: edge received, IIS received, application classified, analytic fired, human acknowledged. A test passes only if the expected controls act and all required evidence appears within the service-level objective. If a response changes unexpectedly, errors increase, latency degrades, or the emergency contact requests a stop, testing stops.

**Case study - clean host-header responses.** The supplied campaign says Host, `X-Forwarded-Host`, absolute-URI, and trust-based error-bypass cases came back clean. That is useful prevention evidence for those exact samples. It is not detection evidence. Replaying only the approved canaries while defenders observe should produce a rejected/normalized request and a searchable event. If the user receives a safe response but no event exists, prevention may have worked while situational awareness still failed.

### Phase 2: Letter plus two test accounts

Create two synthetic users with deliberately different ownership and, if needed, roles. Create only synthetic records. Write an access matrix before sending requests: subject A/B, action read/update/delete, object A/B, and expected allow/deny. ZAP Access Control, AuthMatrix, or Autorize can replay that finite matrix, but a human must verify that an apparent 200 response does not contain another user's data and that a denial is not hidden inside a 200 template.

For CSRF, select a harmless reversible action. Verify a valid request, then controlled negative cases such as missing or mismatched antiforgery context. Do not attempt to affect a real account. CSRF is an attack in which a malicious site causes a logged-in browser to send an unwanted request [34]; anti-forgery does not test whether account A is authorized to change account B's object. Permission must be validated on every request regardless of whether it originates from AJAX, server-side code, or another source [36].

### Phase 3: Entra canaries

Obtain tenant-owner consent separately. Use only the designated accounts and an agreed success/failure sequence that cannot cause lockout or MFA fatigue. Verify that the event appears in the correct tenant and central workspace, that risk and conditional-access context are retained where licensed, and that the incident routes to the correct owner. Identity Protection reports can be exported as CSV or integrated with a SIEM [5], so evidence reconciliation should not depend on screenshots.

### Evidence pack

Every case should produce a small, redacted evidence pack: authorization ID, test-case ID, UTC timestamps, source IP, expected control, client result, edge/IIS/application/identity event IDs, alert ID, ticket/incident ID, responder, and disposition. Keep raw bodies only when necessary and approved. This turns "we scanned it" into a repeatable purple-team control test.

## No-Tool Gaps and Build Candidates

General tools cover request generation well. The most important gaps concern semantics, correlation, and safe governance.

| Gap | Why existing tools are insufficient | Build candidate | Minimum safe design |
|---|---|---|---|
| Three-stage `enc` semantics | Scanners see length/status differences but do not know the expected internal reason model | **SLCM ErrorDiff** | Finite approved cases; rate 1; compare status/type/length/hash/latency; never store plaintext secrets; emit JSONL |
| Response-to-log reconciliation | DAST reports findings but cannot prove IIS, app, SIEM, and incident evidence all exist | **Telemetry Reconciler** | Input test-case ID and UTC window; query read-only APIs; output a five-checkpoint pass/fail record |
| Semantic BOLA validation | Response similarity cannot prove object ownership or absence of another user's data | **AuthZ Twin** | Two synthetic users/objects; explicit allow/deny matrix; content assertions supplied by app owner; hard request ceiling |
| Three-tenant ownership | One query may miss another tenant or lose tenant identity | **Tenant Correlation Pack** | Per-tenant connectors, immutable tenant field, common canary tag, central incident routing test |
| Scope enforcement | Powerful tools can exceed approved routes, methods, templates, or rates | **ScopeGuard Proxy** | Signed allowlist, deny by default, request counter, wall-clock window, kill switch, append-only audit log |
| Error-family drift | Fixed byte lengths vary after deployments, localization, or compression | **Shape Baseline** | Learn from approved synthetic tests; bucket length and normalized DOM/hash; version baseline with release ID |
| Safe analyst evidence | Raw logs may contain tokens, cookies, student identifiers, or exception details | **EvidencePack Redactor** | Field allowlist, token/cookie removal, keyed hashes for object IDs, retention label, reviewer sign-off |
| Unknown edge path | Remote responses cannot establish the actual resource chain | **Traffic-Flow Inventory** | Azure resource graph/config export, DNS/certificate mapping, origin ACL review, owner attestation; no probing needed |

The best first build is **Telemetry Reconciler**, not another fuzzer. The campaign already generated differentiable traffic. The organizational failure is that nobody can show whether each event entered the logging pipeline, matched an analytic, and reached a person. A reconciler directly measures that missing property.

The second build is **SLCM ErrorDiff**. Its public assertion should be narrow: all approved invalid `enc` categories return one generic public class. Its protected assertion should be the opposite: each category produces the correct internal reason code under one operation ID. That tension is intentional. Public uniformity limits disclosure; private specificity enables operations.

No custom tool should include exploit payload libraries, credential acquisition, brute force, discovery outside the allowlist, or automatic expansion from discovered links. Code should run first against a local MVC training application and then staging. Production use remains a signed-scope activity.

## Remediation and 30/60/90-Day Plan

### Days 0-30: Remove disclosure and establish evidence

1. Enable production-safe custom error handling and ensure all four supplied YSOD triggers return a generic response. OWASP states that implementation details should not appear in error messages [7]. Preserve detailed exception type, route, release, and operation ID only in protected telemetry.
2. Set `Secure` on the antiforgery cookie and all authentication/session cookies; retain `HttpOnly` where appropriate. Verify SameSite behavior and HTTPS-only operation before rollout.
3. Disable TLS 1.0 and 1.1, retain TLS 1.2 only where required, and prefer TLS 1.3 [25]. Stage HSTS carefully after checking every required hostname.
4. Verify `trace.axd` and ELMAH exposure from configuration, not only 403/404 responses. Remove unused handlers; otherwise restrict them by network and strong administration authorization.
5. Centralize IIS W3C fields and add a correlation ID at the first trusted receiver. Enable selected application request, authorization, antiforgery, and exception events.
6. Inventory the actual Azure traffic path and the owners of all three Entra tenants.

### Days 31-60: Make detections operational

Deploy WEB-ERR-01, WEB-PATH-01, WEB-METHOD-01, WEB-HOST-01, and DET-HEALTH-01 in monitor mode. Generate synthetic log events before any production canary. Tune expected scanners, monitoring agents, and deployment traffic, but do not suppress on broad user-agent strings alone.

Create the finite authorized validation plan and obtain sign-off from application, network, identity, privacy, and incident-response owners. Assign severity and response targets. A single request to `trace.axd` may be informational; a sequence combining diagnostics, rare methods, parameter-shape changes, and multiple error families should raise priority.

### Days 61-90: Validate authenticated and identity controls

Provision two test accounts and synthetic objects. Run the written access matrix and one harmless CSRF workflow in staging, then production only if approved. Create the Entra canary in each participating tenant. Reconcile every event and open a formal gap for missing telemetry, failed analytics, or ownership ambiguity.

Add the resulting checks to release governance. Automated access-control testing complements, but does not replace, a dedicated security test [36]. The release should fail if generic error mapping regresses, TLS policy drifts, test authorization expectations change unexpectedly, or a detection canary disappears.

## Synthesis: Prevention, Detection, and Proof Are Different

The supplied findings expose three distinct questions that should not be collapsed.

| Dimension | Prevention question | Detection question | Proof question |
|---|---|---|---|
| Verb handling | Was the unwanted method rejected? | Was the unusual method and reason visible? | Can the team link client result to IIS/app event? |
| Host/proxy trust | Was an untrusted host value ignored or rejected? | Was the anomaly recorded at the first receiver? | Can the event be found with the exercise ID? |
| Error oracle | Did the client receive a uniform generic response? | Did protected telemetry preserve the internal branch? | Did a multi-branch sequence create an alert and ticket? |
| CSRF | Was missing/mismatched context rejected? | Was the failure tied to route and session without token leakage? | Did the SOC recognize the authorized canary? |
| BOLA/IDOR | Did account A fail to access B's object? | Was the policy denial recorded with subject/action/object? | Does the access matrix and event trail demonstrate the boundary? |
| Entra | Did identity policy allow or deny correctly? | Did the correct tenant produce sign-in/risk/audit evidence? | Did central triage retain tenant and owner context? |

The campaign provides some prevention evidence: certain host-trust cases were clean, diagnostic paths did not disclose content, and antiforgery was reportedly enforced. It also provides disclosure evidence: verbose YSOD and response differentials. It provides almost no detection proof. This divergence is the central finding.

The error oracle creates a non-obvious design tension. Remediation should make public responses less distinguishable, but detection needs more internal distinction. The correct architecture does both: generic external responses plus structured, access-controlled reason codes. Simply suppressing exceptions without internal telemetry would improve appearance while worsening detection.

The second tension is automation versus semantics. ZAP, AuthMatrix, and Autorize can efficiently replay approved requests, but authorization is a relationship among subject, action, object, and context. OWASP notes that IDOR arises from a missing object-level authorization check [35], and testing is stronger with multiple accounts that have different scopes [35]. A scanner's green row is therefore not enough; the application owner must define the access matrix and synthetic object ownership.

The third tension is edge ambiguity. Adding a WAF may improve visibility, but a WAF cannot compensate for an origin that accepts direct traffic or for application logs that omit authorization decisions. Conversely, application telemetry cannot observe TLS negotiation rejected before IIS. The layers are complementary, not competing.

The fourth tension is three-tenant identity. Centralization is useful, but flattening tenant context can route incidents to the wrong team. Preserve tenant ID and application/resource context through the SIEM and incident workflow. Identity and web canaries should share an exercise ID, never a credential or token.

The practical conclusion is straightforward: **repeat fewer tests, instrument them better, and require a closed evidence loop**. One carefully authorized canary that proves edge -> IIS -> application -> analytic -> responder is more valuable to detection engineering than thousands of uncorrelated scan requests.

## VERDICT

**Verdict: DETECTION READINESS UNPROVEN - CAMPAIGN STATUS ABSENT.**

The available record supports a strong conclusion about the campaign process: it produced technical observations without detection evidence. It does **not** support a conclusion that MUJ has no logging, that the portal is broadly exploitable, that host-header attacks work, or that authenticated authorization is secure or insecure. Those would exceed the supplied evidence.

**Confidence: High** that the prior campaign failed to demonstrate detection, because that absence is an explicit premise of the request. **Confidence: High** in the recommended layered telemetry and controlled-validation design, because it follows documented IIS fields, Application Insights correlation, Entra/Sentinel integration, and OWASP authorization/error guidance. **Confidence: Moderate** in the target-specific risk prioritization, because the live measurements were supplied rather than independently verified. **Confidence: Low to unknown** for CSRF completeness, BOLA/IDOR, session management, and three-tenant policy effectiveness, because the campaign never authenticated.

The minimum condition to change the verdict from ABSENT to PRESENT is not another scanner finding. It is a signed, safely executed canary with two-sided evidence: the expected client control result and a timely, correlated alert or incident acknowledged by an assigned defender.

## References

1. *Monitor logs for Azure Web Application Firewall | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/web-application-firewall/ag/web-application-firewall-logs
2. *Application Insights telemetry data model - Azure Monitor*. https://learn.microsoft.com/en-us/azure/azure-monitor/app/data-model-complete
3. *Cross-Site Request Forgery Prevention Cheat Sheet - OWASP*. https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
4. *Send Microsoft Entra ID data to Microsoft Sentinel*. https://learn.microsoft.com/en-us/azure/sentinel/connect-azure-active-directory
5. *Investigate risk with Microsoft Entra ID Protection ...*. https://learn.microsoft.com/en-us/entra/id-protection/howto-identity-protection-investigate-risk
6. *GitHub - projectdiscovery/nuclei: Nuclei is a fast ...*. https://github.com/projectdiscovery/nuclei
7. *Error Handling - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html
8. *Integrating with CI/CD platforms - PortSwigger*. https://portswigger.net/burp/documentation/dast/user-guide/ci-cd
9. *Trace Failed Requests Logging for a Site ...*. https://learn.microsoft.com/en-us/iis/configuration/system.applicationhost/sites/site/tracefailedrequestslogging
10. *Automation Framework - ZAP*. https://www.zaproxy.org/docs/automate/automation-framework/
11. *Burp Suite subscription model - PortSwigger*. https://portswigger.net/support/burp-suite-licensing-model
12. *W3C Logging - Win32 apps | Microsoft Learn*. https://learn.microsoft.com/en-us/windows/win32/http/w3c-logging
13. *Getting started with Burp Suite Professional / Community Edition - PortSwigger*. https://portswigger.net/burp/documentation/desktop/getting-started
14. *GitHub - zaproxy/zaproxy: The ZAP by Checkmarx Core project · GitHub*. https://github.com/zaproxy/zaproxy
15. *GitHub - urbanadventurer/WhatWeb: Next generation web scanner · GitHub*. https://github.com/urbanadventurer/WhatWeb
16. *GitHub - testssl/testssl.sh: Testing TLS/SSL encryption anywhere on any port · GitHub*. https://github.com/testssl/testssl.sh
17. *GitHub - nabla-c0d3/sslyze: Fast and powerful SSL/TLS scanning library. · GitHub*. https://github.com/nabla-c0d3/sslyze
18. [CWE -

    CWE-209: Generation of Error Message Containing Sensitive Information (4.20)
    ](https://cwe.mitre.org/data/definitions/209.html)
19. *API1:2023 Broken Object Level Authorization - OWASP API Security Top 10*. https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/
20. *GitHub - ffuf/ffuf: Fast web fuzzer written in Go · GitHub*. https://github.com/ffuf/ffuf
21. *Verbs &lt;verbs&gt; | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/configuration/system.webserver/security/requestfiltering/verbs/
22. *GitHub - PortSwigger/auth-matrix: AuthMatrix is a Burp Suite extension that provides a simple way to test authorization in web applications and web services. · GitHub*. https://github.com/PortSwigger/auth-matrix
23. *GitHub - projectdiscovery/httpx: httpx is a fast and multi-purpose HTTP toolkit that allows running multiple probes using the retryablehttp library. · GitHub*. https://github.com/projectdiscovery/httpx
24. [CWE -

    CWE-204: Observable Response Discrepancy (4.20)
    ](https://cwe.mitre.org/data/definitions/204.html)
25. *Transport Layer Security - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html
26. *How to configure Microsoft Entra diagnostic settings - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/monitoring-health/howto-configure-diagnostic-settings
27. *ZAP – Access Control Testing*. https://www.zaproxy.org/docs/desktop/addons/access-control-testing/
28. *Configure Logging in IIS | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/manage/provisioning-and-managing-iis/configure-logging-in-iis
29. *Authorization Testing Automation - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Testing_Automation_Cheat_Sheet.html
30. *ZAP – Report Generation Automation Framework Support*. https://www.zaproxy.org/docs/desktop/addons/report-generation/automation/
31. *GitHub - Quitten/Autorize: Automatic authorization enforcement detection extension for burp suite written in Jython developed by Barak Tawily in order to ease application security people work and allow them perform an automatic authorization tests · GitHub*. https://github.com/Quitten/Autorize
32. *http://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References*. http://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References
33. *http://learn.microsoft.com/en-us/entra/identity-platform/authentication-vs-authorization*. http://learn.microsoft.com/en-us/entra/identity-platform/authentication-vs-authorization
34. *http://learn.microsoft.com/en-us/aspnet/web-api/overview/security/preventing-cross-site-request-forgery-csrf-attacks*. http://learn.microsoft.com/en-us/aspnet/web-api/overview/security/preventing-cross-site-request-forgery-csrf-attacks
35. *http://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html*. http://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html
36. *http://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html*. http://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
37. *GitHub - projectdiscovery/nuclei-burp-plugin: Nuclei plugin ...*. https://github.com/projectdiscovery/nuclei-burp-plugin
38. *Download Burp Suite Community Edition - PortSwigger*. https://portswigger.net/burp/communitydownload
39. *FAQ | HTTP Observatory*. https://developer.mozilla.org/en-US/observatory/docs/faq
40. *http://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html*. http://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
