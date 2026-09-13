# MUJ SLCM SQL and NoSQL Injection Research Plan

## Executive Summary

- **Campaign Status Remains Absent**: The supplied measurements establish verbose ASP.NET error handling and a differential `enc` processing oracle, but they do not show that attacker-controlled data reached a SQL or NoSQL query sink. SQL injection exists when input changes a database SQL query [2], while NoSQL injection requires interference with a NoSQL query [1]. -> Record the present result as **not tested to an evidentiary standard**, not as "not vulnerable."
- **Authorization Is The Immediate Gate**: OWASP's Rules of Engagement model calls for explicit authorization, target boundaries, allowed and prohibited actions, credentials, rate limits, approval requirements, and kill-switch contacts before testing [51]. -> Before the signed letter and two test accounts arrive, perform no more active requests against the portal; restrict work to public documentation, local laboratories, source review supplied by the owner, and test-plan preparation.
- **The `enc` Oracle Is A Routing Clue, Not SQLi Evidence**: The club reports three response classes for empty, invalid-Base64, and valid-Base64-but-invalid-ciphertext values. **Inference:** input probably encounters decoding and cryptographic processing before any possible data-access sink. -> Generic scanners may only measure the crypto boundary; an owner-provided staging key, test-only encoder, or source-level trace is needed to test the post-decryption value safely.
- **Verbose Errors Increase Diagnostic Value**: ASP.NET's `customErrors` mode controls whether custom or detailed error pages are shown and supports `On`, `Off`, and `RemoteOnly` [43]. The supplied observation of remote YSODs with `customErrors` off can reveal processing stages and stack detail. -> Remediate error disclosure independently and retain full exceptions only in protected server telemetry.
- **SQL Has The Stronger Prior, But The Backend Is Unproven**: .NET Framework and MVC commonly support relational data access, and Microsoft warns that Entity SQL can be injectable when user data is combined with command text [15]. However, IIS, Azure AS8075, and MVC do not prove SQL Server, Azure SQL, MongoDB, or any other database. -> Test SQL and NoSQL hypotheses separately and do not select DBMS-specific exploit modes until code, configuration, or controlled fingerprinting confirms a backend.
- **Automation Must Follow Authenticated Mapping**: sqlmap covers boolean, time, error, UNION, and stacked-query techniques across more than 40 database backends [24], while NoSQLMap and `nosqli` target NoSQL or MongoDB-oriented injection [14][11]. -> First capture owner-authorized, valid requests through both test accounts; then replay only approved endpoints at a rate and technique level fixed by the letter.
- **Source-Level Controls Offer The Highest Assurance**: ADO.NET parameters are treated as literal values rather than executable code [10], and Microsoft recommends parameterized Entity SQL instead of combining input with command text [15]. -> Pair black-box DAST with review of controllers, model binders, decryption code, repositories, stored procedures, and raw-query calls.
- **NoSQL Requires Different Test Shapes**: PortSwigger separates NoSQL injection into syntax injection and operator injection [1]. OWASP recommends driver query objects, rejecting raw client JSON as executable queries, restricting operator keys, least privilege, and audit logging [22]. -> Include JSON type, key, and operator validation tests rather than assuming SQL punctuation will exercise NoSQL paths.
- **Detection Must Be Layered**: ZAP and Wapiti can find runtime symptoms; Semgrep and CodeQL can find source-to-sink flows; application logging should record the when, where, who, and what of security events [52]; WAF, database auditing, and Defender are additional layers. -> Treat WAF alerts as signals, not proof of safety, and correlate HTTP, application, identity, and database events using a shared test correlation ID.
- **Best Build Candidate Is An Application-Aware Replay Harness**: Generic tools do not understand the portal's `enc` cryptographic envelope, authenticated antiforgery lifecycle, response-family clustering, or tenant-specific business semantics. -> Build a staging-only adapter that creates valid encrypted test values, refreshes authorized tokens, rate-limits requests, labels every mutation, and stops on instability.

## 1. Scope, Evidence Status, And Safety Boundary

This report addresses SQL and NoSQL injection research for `https://mujslcm.jaipur.manipal.edu/`. It does not authorize testing. It uses the measurements in the prompt as club-supplied observations dated **2026-09-13**; they were not independently reproduced for this report and have no public evidence URL. All target-specific conclusions based on them are explicitly labeled as observations or inferences.

I cannot provide private hidden chain-of-thought. Instead, the report provides an audit-ready decision rationale: what evidence exists, what it can support, what it cannot support, the competing hypotheses, and the threshold for advancing to each test phase.

| Activity | Safe before written authorization? | Required conditions | Reason |
|---|---:|---|---|
| Read public OWASP, Microsoft, and tool documentation | Yes | No interaction with the target | Pure public-information research |
| Build local vulnerable SQL and NoSQL labs | Yes | Use owned systems and synthetic data | Exercises tools without touching MUJ assets |
| Draft request templates, evidence schemas, and stop rules | Yes | Do not send them to the portal | Planning only |
| Review source, logs, architecture, or SBOM voluntarily supplied by MUJ | Yes, if formally supplied for review | Respect confidentiality and the owner's handling rules | Owner-controlled evidence, not target probing |
| DNS, TLS, HTTP, port, header, or error-page rechecks against the live portal | **No further runs recommended** | Signed letter must name the host and techniques | Even "benign" requests alter target logs and extend an active campaign |
| Authenticated browsing and proxy capture | No | Signed letter, two designated accounts, testing window, test records | Creates realistic request corpus and state transitions |
| SQLi or NoSQLi DAST, fuzzing, timing tests, or differential mutations | No | Letter, accounts, rate limits, endpoint allowlist, stop rules | Sends attack-like inputs; ZAP itself warns that its full scan performs actual attacks [34] |
| Out-of-band callbacks, stacked queries, data enumeration, write tests, OS interaction, or denial-of-service techniques | No by default | Separate explicit approval for each class, isolated data, named callback domain | Disproportionate impact and third-party interaction risk |
| Production data extraction as "proof" | No | Prefer owner-seeded canaries; any exception needs explicit data-handling approval | A vulnerability can be proven without collecting real student data |

OWASP's Rules of Engagement template supports a default-deny posture when required scope information is missing or ambiguous [51]. Its control fields include authorization, targets, time windows, rate limits, credential restrictions, prohibited actions, approval gates, escalation, and emergency contacts [51]. For this campaign, the letter should additionally identify the legal owner of the application, cloud and identity dependencies that are in scope, source IPs, maximum concurrency, permitted accounts, permitted test records, callback domains, evidence retention, and the person authorized to halt testing.

**Decision-ready insight:** Until that document and the two accounts exist, the highest-value work is not another probe. It is preparing a deterministic test matrix and building safe local tooling so that the authorized window produces evidence instead of exploratory traffic.

## 2. What The Supplied Measurements Establish

| Supplied observation | What it supports | What it does not support |
|---|---|---|
| TCP 443 was the only reachable port | The observed public attack surface was HTTPS-only at measurement time | It does not describe private services, databases, origin paths, or later changes |
| Four triggers produced verbose YSODs with `customErrors` off | Detailed ASP.NET exception handling is remotely visible under the tested conditions | It does not establish a database error or injection sink |
| MVC antiforgery was enforced; cookie was HttpOnly without Secure | An antiforgery lifecycle must be preserved in authenticated testing; cookie hardening needs review | Antiforgery does not prevent server-side query injection |
| `trace.axd` returned 403 and `elmah.axd` returned 404 | Those two paths were not publicly usable in the measured state | It does not prove tracing or ELMAH is absent internally |
| MVC and IIS error families were approximately 2,733 and 1,216 bytes | Response clustering may distinguish pipeline stages | Length alone is not vulnerability proof and can change with content or deployment |
| POST and PUT without the expected framing returned 411; other methods returned 404 | The tested requests followed different server paths | **Inference:** 411 can reflect request framing or missing length, so it does not prove a GET-only application policy |
| `enc` produced three response-size classes | The parameter is a strong candidate for staged differential analysis | It does not prove that decrypted data reaches SQL, NoSQL, or any database |
| Host and forwarding-header bypass attempts were clean | No issue was demonstrated by those exact attempts | It does not establish a universal absence of routing or trust-boundary weaknesses |
| Campaign never authenticated | Existing evidence is limited to unauthenticated paths | It says little about student, faculty, administrative, or tenant-scoped data access |

The tension between "GET only" and enforced MVC antiforgery is important. Antiforgery is normally relevant to state-changing authenticated requests, while the recorded 411 responses may merely show malformed or incomplete request framing. **Inference:** authenticated forms or AJAX calls may expose POST endpoints that the unauthenticated campaign never reached. The two accounts are therefore not a convenience; they are necessary to map the actual application.

The YSOD observation matters because detailed exceptions can shorten root-cause analysis. Microsoft documents that `customErrors` chooses the displayed error behavior and that a custom page can replace the runtime YSOD [43]. It still does not turn every exception into injection evidence. A `FormatException` is evidence of failed representation handling; a `CryptographicException` is evidence of a later crypto failure. Only a database-specific exception, a controlled query-logic difference, or a verified source-to-sink flow would materially strengthen the SQLi/NoSQLi case.

The missing `Secure` attribute and missing HSTS are adjacent transport/session findings rather than injection findings. OWASP recommends HTTPS for the entire session and the `Secure` cookie attribute [37]. HSTS tells browsers to use HTTPS for the domain and helps prevent protocol downgrade after policy is established [36]. These should be fixed, but neither fix substitutes for parameterized queries.

**Case study - the `enc` boundary:** Generic DAST mutates a visible parameter and interprets the response. Here, the three supplied error classes imply that malformed mutations can terminate in decoding or decryption before reaching business logic. A scanner could report "not injectable" simply because none of its values crossed the cryptographic envelope.

The safer solution is architectural. In a staging clone, the owner can expose a test-only encoder or provide a helper library that accepts synthetic plaintext and returns a valid `enc` value. Instrumentation should then record only stage transitions and query-template identifiers, not secrets. This turns an opaque precondition into a controlled source-to-sink experiment without disclosing a production key.

## 3. SQL And NoSQL Injection Technique Universe

OWASP groups SQL injection into in-band, out-of-band, and inferential or blind classes [2]. Its testing guide identifies UNION, boolean, error-based, out-of-band, and time-delay techniques [2]. Successful SQLi can read or modify data, perform database administration, interact with files, and in some configurations reach operating-system commands [2]. Those are impact categories, not approved test actions.

PortSwigger defines NoSQL injection as interference with queries made to a NoSQL database and notes possible authentication bypass, data access or modification, denial of service, and server-side code execution [1]. Its primary split is syntax injection versus operator injection [1].

| Technique class | Mechanism to assess | Safe evidence objective | Tool strength | Important constraint for MUJ SLCM |
|---|---|---|---|---|
| SQL error-based | Input changes query parsing or evaluation and causes a database-specific error | Confirm a controlled DB-layer exception without exposing data | Strong in sqlmap, Ghauri, Burp, ZAP, Wapiti | YSODs can help classification, but current exceptions appear pre-database |
| SQL boolean blind | Two semantically paired inputs produce repeatable true/false response differences | Demonstrate a stable logical split using synthetic test records | Strong in sqlmap and blind frameworks | Normalize dynamic page content and compare status, structure, length, and authenticated state |
| SQL time-based blind | A condition produces a bounded, repeatable latency difference | Statistical separation with a low delay and strict request ceiling | Strong in sqlmap, Ghauri, BBQSQL | Needs rate approval; Azure/network variance can create false positives |
| SQL UNION/in-band | Query results can be combined into the application response | Use an owner-seeded canary, not real data | Strong in sqlmap and jSQL | Must not enumerate student records |
| SQL stacked query | The driver accepts an additional statement | Prefer source review or transaction-rolled-back canary | Tool support varies by DBMS | High impact; separately approve or exclude |
| SQL out-of-band | Database behavior triggers DNS or another callback | A single callback to an owner-approved domain | Supported by some SQL Server-oriented tooling | Prohibit unless egress and callback ownership are explicitly scoped |
| Dynamic SQL in stored procedures | Procedure parameters are concatenated into dynamic command text | Source review plus unit test around the procedure | Often missed by endpoint-only scanning | A stored procedure is not automatically safe; dynamic SQL still requires parameterization [2] |
| Identifier or sort injection | User input controls a column, table, sort, or other non-parameterizable identifier | Verify strict allowlisting | Primarily manual or SAST | Databases do not parameterize schema identifiers [50] |
| ORM/raw-query injection | A safe ORM is bypassed by raw SQL or unsafe string construction | Trace controller input into raw query APIs | Stronger in CodeQL/Semgrep and code review | EF's raw APIs require special review [50] |
| Second-order SQLi | Stored input is later incorporated into a different query | Seed, trigger, and correlate synthetic values | Weak in generic DAST | Needs workflow knowledge, test records, and cleanup |
| NoSQL syntax injection | Input breaks the native query syntax | Demonstrate parser or logic change with no data collection | Burp/manual tools; backend-dependent | The NoSQL backend and query language are unknown |
| NoSQL operator injection | Client-controlled object keys introduce query operators | Confirm keys are rejected or treated as data | NoSQLMap, `nosqli`, Burp/manual | Test JSON objects, arrays, duplicate keys, and model binding, not only string punctuation |
| NoSQL type confusion | A scalar field accepts an object, array, null, number, or boolean that changes query construction | Verify schema and type enforcement | Mostly manual or property-based testing | ASP.NET model binding and custom deserialization can transform the input first |
| NoSQL server-side expression | Query features evaluate an expression, script, regex, or aggregation stage | Prefer configuration/source review; avoid expensive expressions | Limited and backend-specific | Potential denial of service; exclude from production unless separately approved |
| NoSQL second-order injection | Stored document content becomes a later filter, pipeline, or script input | Controlled multi-step workflow with synthetic data | Weak automated coverage | Requires authenticated business workflows |

**Case study - identifiers versus values:** A team can parameterize every ordinary value and still concatenate a requested sort field. Microsoft notes that column names and other schema elements cannot be represented as database parameters [50]. The correct control is a server-side mapping from a small user-facing enum to known identifiers, not ad hoc escaping. Microsoft separately recommends allowlisting expected identifiers and rejecting unexpected ones [49].

This case explains why a clean sqlmap result is not complete assurance. A scanner excels when a parameter reaches a conventional value position. It may not understand that a UI sort token, report column selector, or export field becomes query structure after several transformations. Code review and property-based tests around the mapping are the better evidence.

## 4. Active Tool Matrix

No finite report can literally enumerate every private scanner, fork, one-off script, or future tool. The table below is the material public tool universe found for this campaign: prominent SQLi and NoSQLi engines, general DAST products that exercise the class, and target-relevant specialist tools. "BYOK" is marked not applicable where a tool does not use an external model or API key.

| Tool and exact URL | Injection coverage | License and access model | How it is driven | Output | MUJ use and gate |
|---|---|---|---|---|---|
| **sqlmap** - https://sqlmap.org/ | Automated SQLi detection/exploitation; boolean, time, error, UNION, stacked; 40+ backends [24] | GPLv2 community use plus a commercial embedding license [24]; free local/self-hosted; BYOK N/A | CLI with URL/request files and extensive switches | Console/session evidence and the exact confirming payload are documented [24]; retain sanitized logs | Primary SQLi engine after authenticated request capture; signed letter required |
| **Ghauri** - https://github.com/r0oth3x49/ghauri | Cross-platform SQLi detection and exploitation [18] | MIT [18]; free local/self-hosted; BYOK N/A | Python CLI, installed with pip or from source [18] | Repository page does not state a formal report format | Useful second engine for differential confirmation; letter and accounts required |
| **jSQL Injection** - https://github.com/ron190/jsql-injection | Automatic SQL database injection [5] | GPL-2.0 [5]; free local desktop; BYOK N/A | Java application/JAR on Windows, Linux, or macOS [5] | Interactive GUI results; formal export not stated on cited page | Secondary visual validation; authorization required |
| **DSSS** - https://github.com/stamparm/DSSS | Small SQLi scanner for GET and POST parameters [13] | Public domain [13]; free local; BYOK N/A | Python 3 CLI [13] | Formal output format not stated | Fast lab triage, but not a substitute for authenticated mapping |
| **BBQSQL** - https://github.com/CiscoCXSecurity/bbqsql | Blind SQLi framework [45] | Royalty-free open source under BSD-derived conditions [35]; local; BYOK N/A | Python configuration/framework with binary and frequency search modes [45] | CSV output option [45] | Specialist blind confirmation only after rate and latency limits are approved |
| **sqlninja** - https://sqlninja.sourceforge.net/ | Legacy Microsoft SQL Server injection/takeover and extraction tool [46] | GPLv3 [46]; free local; BYOK N/A | Perl CLI plus configuration file [46][40] | Local SQLite database for extracted information [46] | Do not run takeover modes; consider only if SQL Server is confirmed and a narrow mode is separately approved |
| **NoSQLMap** - https://github.com/codingo/NoSQLMap | NoSQL database enumeration and web application exploitation [14] | GPL-3.0 [14]; source-hosted locally; BYOK N/A | Menu-driven attack builder or CLI scripting [14] | Formal output format not stated | Use in a MongoDB-style lab first; production use needs explicit NoSQL scope |
| **nosqli** - https://github.com/Charlie-belmer/nosqli | MongoDB-oriented NoSQL injection discovery [11] | AGPL-3.0 [11]; free local; BYOK N/A | Command-line tool [11] | Formal output format not stated | Useful only after a MongoDB/query-object hypothesis exists |
| **Burp Scanner** - https://portswigger.net/burp/vulnerability-scanner | General automated web scanning based on PortSwigger research [9] | Vendor product; cited page states a free trial but not exact license terms [9]; BYOK N/A | Automated scans plus Burp's authenticated/manual workflow | Standard Burp reports [9] | Best for account-aware mapping and carefully selected checks; signed scope and accounts required |
| **ZAP** - https://github.com/zaproxy/zaproxy | Automated and manual web vulnerability testing [30], including SQLi alert 40018 [16] | Apache-2.0, free and open source [30]; local/Docker; BYOK N/A | Desktop, automation framework, or Docker full-scan script | HTML, JSON, Markdown, PDF, and XML templates [32] | Passive proxying can begin only after account authorization; active scan requires explicit approval |
| **Wapiti** - https://github.com/wapiti-scanner/wapiti | Black-box web fuzzer that checks errors, strings, and abnormal behavior [20] | GPL-2.0 [20]; free local; BYOK N/A | Python CLI against a deployed application | HTML, XML, JSON, TXT, CSV, Markdown [20] | Broad DAST complement; run only on allowlisted routes under the letter |
| **Nuclei** - https://github.com/projectdiscovery/nuclei | YAML-template scanner across HTTP and other protocols [3] | MIT [3]; standalone CLI and optional cloud tiers; BYOK not stated | CLI plus selected YAML templates [3] | CLI, JSON, JSONL, Markdown, SARIF, PDF [3] | Use only reviewed injection templates; never point the full community set at production |
| **Invicti SQL Injection Scanner** - https://www.invicti.com/sql-injection-scanner/ | DAST detection and proof-based confirmation of SQLi [6] | Vendor product; exact license, hosting, and BYOK terms not stated on cited page | External DAST using crafted HTTP requests [6] | Formal format not stated on cited page | Proof-based extraction may exceed the club's safe evidence threshold; configure canaries and limits |
| **Acunetix SQL Injection Scanner** - https://www.acunetix.com/vulnerability-scanner/sql-injection-scanner/ | SQLi and general web vulnerability scanning [28] | On-premises for Windows/Linux/macOS or online service; exact license/BYOK terms not stated [28] | Managed scanner workflow | Reports including PCI DSS and HIPAA formats [28] | Owner-operated alternative where data residency or authenticated scanning is required |

Tools that "perform injection" should not all be run. sqlninja's takeover objective, for example, is much broader than this campaign needs. The correct strategy is minimum necessary capability: Burp or ZAP for valid request capture, one primary SQL engine, one independent confirmation engine, and NoSQL-specific tooling only if architecture evidence supports it.

## 5. Manual Method For Tool Gaps

### 5.1 Authorized endpoint and data-flow map

After the letter is signed, log in through each test account and use only ordinary, owner-approved workflows. Capture complete requests in an intercepting proxy, including route values, query strings, form fields, JSON bodies, cookies, antiforgery fields, content types, redirects, and account role. Do not mutate anything during this mapping pass.

For every input, create a row containing: endpoint, HTTP method, authentication state, account, expected type, encoding/encryption stage, server-side model property, likely repository method, response family, state change, and cleanup procedure. If source is available, trace the field from MVC model binding through validation and decryption into ADO.NET, Entity SQL/LINQ, raw SQL, stored procedures, or a NoSQL driver.

### 5.2 Differential SQL method

Use one mutation at a time and compare it with a matched control. Start with harmless syntax-boundary and type-boundary cases, not extraction. A candidate requires repeatability across fresh authenticated sessions and must survive normalization of tokens, timestamps, and page-specific noise. Evidence can be a database-specific exception, a controlled true/false split, or a bounded latency split that is absent in controls.

Do not progress automatically from detection to enumeration. Stop after proving that query semantics are controllable. If stronger assurance is required, have the owner place a unique synthetic canary in a test-only row and authorize retrieval of that canary alone. Stacked statements, file functions, OS interaction, credential access, and production-record extraction remain prohibited unless independently named in the letter.

### 5.3 Differential NoSQL method

Begin from the declared schema. For a field expected to be a string, verify that objects, arrays, nulls, numbers, booleans, duplicate keys, and unexpected nested fields are rejected before the query layer. Then verify that keys resembling query operators cannot be introduced through JSON, form-to-object conversion, or custom model binding. PortSwigger's syntax/operator distinction [1] should structure the evidence, but the exact test values must be tailored to the confirmed database and tested in the lab first.

For authentication and record-selection endpoints, use only the two provided accounts and pre-seeded records. A result is meaningful when the same authorized request, changed in exactly one structural property, crosses a record-selection or authorization boundary. Do not use broad regular expressions or expensive server-side expressions in production; they can create denial-of-service conditions even when no data is returned.

### 5.4 Source-assisted method

ADO.NET parameters provide type checking and cause inputs to be treated as literal values rather than executable code [10]. Entity SQL should never combine user input with command text; parameterized queries or query-builder methods are recommended [15]. LINQ to Entities query composition uses an object model rather than string concatenation and is not susceptible to traditional SQL injection in the same way [15].

Review every escape hatch. `FromSql` and `FromSqlInterpolated` parameterize values, while improper `FromSqlRaw` use can be vulnerable [50]. `ExecuteSqlRaw`, dynamic stored-procedure text, report builders, export modules, and schema identifiers need separate scrutiny. For NoSQL, use driver query objects, reject raw client JSON as a query, allowlist keys, and disallow client-controlled operators unless strictly necessary and validated [22].

**Decision-ready insight:** For this portal, a source-assisted review is likely to produce more assurance per request than blind production fuzzing because it can show whether decrypted `enc` plaintext ever reaches query construction.

## 6. Detection And Prevention Counterpart

| Layer | Control | Evidence produced | Limitation |
|---|---|---|---|
| Controller/model | Strict type, length, format, range, and key validation | Rejected-input tests and validation logs | Validation alone must not replace safe query APIs |
| Data access | ADO.NET/ORM parameterization | Unit tests and query templates with separate parameters | Identifiers and raw SQL remain special cases |
| NoSQL driver | Typed query objects and operator/key allowlists | Schema-validation failures and driver-level tests | Backend-specific features can bypass generic rules |
| SAST | Semgrep plus CodeQL C# SQLi query | Source location and source-to-sink trace | Needs source/build context; sanitizers can cause false positives or negatives |
| DAST | Burp, ZAP, Wapiti, sqlmap/Ghauri, selected Nuclei templates | Request/response evidence and reproducible test ID | Cannot see unreachable, second-order, or crypto-wrapped sinks reliably |
| Application telemetry | Structured security events with account, route, correlation ID, stage, validation result, and exception class | Cross-layer timeline | Must not log secrets, tokens, ciphertext keys, or sensitive query values |
| Database telemetry | Query/audit events, denied actions, unusual latency or volume | DB-side confirmation | Only available if configured and accessible to the owner |
| WAF | SQLi managed rules in detection or prevention mode | Rule ID, request metadata, action | Compensating control; can miss custom encodings and does not prove safe code |
| Error handling | Generic remote errors, protected detailed logs | Reduced disclosure plus diagnostic trace | Must preserve enough internal detail for incident response |
| Least privilege | Read/write separation and narrow service account permissions | Denied canary action or permission review | Reduces impact but does not remove injection |

Semgrep is an open-source static analyzer whose Community Edition runs locally by default [12]. CodeQL's C# SQL-injection query identifies SQL built from user-controlled sources and recommends parameterized queries [7]; its CLI can emit CSV, SARIF, Graphtext, DGML, or DOT [29]. Run both in CI if MUJ provides source, and triage every flow into `SqlCommand.CommandText`, Entity SQL, raw ORM methods, stored-procedure construction, or custom NoSQL query builders.

Application logging should capture the "when, where, who and what" of each event [52], including authentication and authorization failures [52]. For authorized testing, add a correlation ID to every test request and propagate it into application and database telemetry. Protect logs from unauthorized access, modification, deletion, and tampering in transit [52]. Never record plaintext passwords, session tokens, encryption keys, or full student records.

If the backend is Azure SQL, Azure SQL auditing can track database events and write them to configured destinations [21]. Defender for SQL can add vulnerability assessment and threat detection, but its applicability depends on the actual database deployment. **Inference:** AS8075 hosting does not establish that either Azure SQL or Defender is present.

Azure WAF includes SQL-injection rule groups [23], but the club reports no attributable edge control. Do not infer that Azure Front Door or Application Gateway WAF exists merely because the host is on Microsoft infrastructure. If the owner deploys WAF later, begin in detection mode, baseline false positives, then block selected high-confidence rules. Continue fixing query construction underneath it.

## 7. NO-TOOL GAPS And BUILD CANDIDATES

| No-tool gap | Why standard tools miss it | Build candidate | Safe deployment model |
|---|---|---|---|
| Valid `enc` envelope | Random mutations fail in decoding or crypto before business logic | **Staging Enc Adapter**: owner-supplied encoder API/library that wraps synthetic plaintext and never exposes production keys | Local or staging only; signed test values; audit every use |
| Three response families plus dynamic pages | Simple length comparison can confuse framework, auth, and application errors | **Response Oracle Classifier**: normalize volatile fields and cluster status, headers, DOM shape, exception family, size, and latency | Passive on saved responses pre-authorization; live replay only after letter |
| Antiforgery and session refresh | Replays fail when cookies/tokens expire or bind to an account | **Account-Aware Replay Broker**: refresh tokens through approved flows and lock each job to one account | Two test accounts; no credential export; emergency stop |
| Second-order injection | Source and trigger occur in different workflows | **Seed-Trigger-Cleanup Runner**: use tagged synthetic records and an explicit cleanup state machine | Staging preferred; production only with seeded records |
| Raw SQL hidden behind repository abstractions | DAST sees only behavior and may never reach rare branches | **MVC Source-to-Sink Rule Pack** for Semgrep/CodeQL covering controller input, decryption helpers, `CommandText`, raw ORM calls, and dynamic stored procedures | CI or local source clone |
| NoSQL backend uncertainty | MongoDB payloads are irrelevant to Cosmos, Elasticsearch, Redis, or a relational backend | **Dependency/SBOM Classifier**: inventory NuGet packages, connection providers, and driver call sites before selecting tests | Source/config review; redact credentials |
| Identifier injection | Values may be parameterized while sort/report identifiers are concatenated | **Identifier Mapping Tests**: generate all accepted enum values plus rejected unknown values | Unit/property tests, no production fuzzing required |
| Cross-account and tenant state | Generic scanners do not understand which record each account should see | **Authorization-Aware Comparator**: compare owner-seeded resources and expected access matrices, not real user data | Requires both test accounts and written role expectations |
| Async jobs, exports, and queues | The injection sink may execute after the HTTP response | **Correlation Propagator** across web, job, and database logs | Owner-operated telemetry only |
| Tool overreach | Exploitation engines can enumerate or write after detection | **Policy Wrapper**: compile RoE into hard-deny switches, request ceilings, endpoint allowlists, and callback restrictions | Default deny; signed configuration; immutable run manifest |

### Case study - building the staging `enc` adapter

The adapter should accept a test case ID and synthetic plaintext, validate that the destination is staging, call the application's existing encryption routine inside the trusted environment, and return a short-lived test value. It should not accept arbitrary target hosts, reveal keys, decrypt production values, or run requests itself. Every generated value should be tied to an approved test ID.

The replay broker then inserts that value into a previously captured authorized request, refreshes antiforgery state, sends one request, and emits a structured record: test ID, account alias, endpoint alias, mutation class, response class, latency bucket, and server correlation ID. The database side records only the query-template identifier and whether parameters remained separate. This design tests the post-decryption sink while minimizing sensitive data and request volume.

### Case study - response classification without false confidence

The existing page-size differences are useful seeds, but a fixed byte threshold is fragile. Authentication redirects, changing view state, timestamps, and framework banners can all change length. The classifier should remove volatile tokens, hash a normalized DOM or text skeleton, identify MVC versus IIS error signatures, and compare repeated controls before labeling a semantic split.

A candidate becomes actionable only when the difference repeats across several matched pairs and aligns with protected telemetry. A length change alone stays "unexplained differential," not "SQL injection." This evidence discipline prevents the verbose YSOD from turning ordinary exceptions into false positives.

## 8. Authorization-Gated Campaign Plan

| Phase | Work | Exit criterion | Authorization status |
|---|---|---|---|
| 0. RoE | Finalize host, accounts, routes, times, rates, techniques, data rules, callbacks, escalation, and stop conditions | Signed letter and machine-readable run policy | Required before target interaction |
| 1. Passive preparation | Public research, local labs, tool installation, test manifests, response classifier on saved samples | Reproducible lab runs and reviewed payload classes | Safe pre-authorization |
| 2. Authenticated mapping | Normal use with both accounts; proxy capture; seed test records; source/architecture interview | Complete endpoint and data-flow inventory | Letter plus accounts required |
| 3. Low-impact DAST | Passive proxy analysis, then selected error/boolean/type tests at low rate | Candidate confirmed twice or rejected with telemetry | Letter required |
| 4. Specialist tests | sqlmap/Ghauri or NoSQL tools only on confirmed sinks; bounded time tests; no automatic enumeration | Minimal proof with synthetic canary | Separate technique approval recommended |
| 5. Manual gaps | `enc` adapter, identifier checks, second-order workflows, account-aware comparison | Source-to-sink evidence and clean rollback | Owner/staging participation required |
| 6. Detection validation | Correlate HTTP, app, identity, WAF, and DB events; verify alerts and redaction | Each test ID traceable without sensitive log content | Owner telemetry access required |
| 7. Remediation and retest | Parameterize, allowlist identifiers/operators, reduce privileges, disable remote detail, harden cookies/HSTS | Negative unit, SAST, DAST, and telemetry results | Controlled retest window |

Stop immediately on instability, unexpected data, account lockout, cross-user content, material latency, log saturation, or any response suggesting a write. Do not "continue to see how far it goes." Preserve the request, response hash, timestamps, tool version, configuration, and correlation ID; notify the named contact.

The two accounts should have deliberately documented roles and owner-seeded records. If they are equivalent student accounts, they support horizontal-access and data-partition checks. If they have different roles, they support role-specific endpoint mapping. Do not infer permission expectations from observed behavior; the owner must provide the expected access matrix.

## 9. Synthesis

| Dimension | Conventional SQLi | NoSQL injection | MUJ `enc`-wrapped path |
|---|---|---|---|
| Core mechanism | User data changes SQL command semantics | User data changes NoSQL syntax, operators, types, or query objects | User input must first survive representation and cryptographic processing; downstream sink is unknown |
| Current target evidence | No database-specific evidence supplied | No NoSQL technology or query evidence supplied | Three pre-business-logic response classes supplied |
| Best black-box tools | sqlmap, Ghauri, Burp, ZAP, Wapiti | Burp, NoSQLMap, `nosqli`, manual JSON testing | Generic tools need an application-aware encoder/replay adapter |
| Best white-box evidence | ADO.NET/EF parameterization, raw-query and procedure review | Driver query objects, schema/key/operator validation | Trace decrypted plaintext into controller/service/repository calls |
| Strongest detection | SAST flow plus application/DB telemetry and bounded DAST | Schema/operator rejection plus SAST/logging and bounded DAST | Stage-specific correlation IDs and normalized response clustering |
| Main false-positive risk | Framework errors or unstable time measurements | Type-validation errors mistaken for query manipulation | Crypto errors mistaken for database errors |
| Main false-negative risk | Raw SQL, identifiers, second-order and rare workflows | Backend-specific operators and object conversion | Scanner values never reach the sink |
| Production risk of testing | Enumeration, writes, expensive delays, stacked statements | Broad selectors, expensive regex/scripts, auth bypass | Account/session disruption and repeated crypto exceptions |
| Recommended order | Architecture -> authenticated map -> source review -> bounded DAST | Confirm backend -> schema review -> structural tests -> specialist tool | Owner-provided staging adapter -> trace -> narrow query tests |

The non-obvious conclusion is that verbose errors both help and mislead. They help identify execution stages, but they can reward a scanner for finding any exception rather than a query-control condition. The remedy is not to suppress evidence collection; it is to move detailed evidence into protected telemetry and demand matched controls.

A second tension is automation versus completeness. sqlmap has broad, mature technique coverage, yet it cannot infer the business meaning of an encrypted parameter, a student-record lifecycle, or a cross-account expectation. Manual and source-assisted methods cover those gaps. Conversely, manual intuition should not replace automated repeatability; every candidate should become a small deterministic regression test.

A third tension is SQL likelihood versus NoSQL scope. The Microsoft stack makes SQL-oriented review sensible, but it does not prove SQL Server. NoSQL testing without dependency or runtime evidence can create noise and risk. The efficient strategy is technology-neutral mapping first, followed by the narrow tool whose query model matches the confirmed sink.

The integrated control objective is simple: untrusted input remains typed data from MVC binding through decryption, service logic, query construction, and database execution. Parameters handle values; allowlists handle identifiers and operator keys; least privilege limits consequences; generic remote errors reduce disclosure; and correlated telemetry proves that defenses operated as intended.

## 10. VERDICT

**Verdict: The SQL/NoSQL injection campaign status is still ABSENT, and no vulnerability conclusion is justified.**

The current material establishes an important prerequisite finding: remotely visible detailed ASP.NET errors and a repeatable `enc` processing differential. It does **not** establish a SQL query sink, a NoSQL query sink, a database technology, query-semantic control, data access, authentication bypass, or a clean negative test. The correct status is therefore:

| Question | Finding | Confidence |
|---|---|---:|
| Has a competent SQLi/NoSQLi campaign been completed? | **No** | **High** |
| Is SQL injection present? | **Unknown** | Low confidence in either direction |
| Is NoSQL injection present? | **Unknown; backend itself is unconfirmed** | Low |
| Are verbose errors present according to supplied measurements? | **Yes, as reported by the club** | Moderate, because not independently verified here |
| Does `enc` create a useful diagnostic oracle? | **Yes for processing-stage classification; not yet for database injection** | Moderate |
| Should active testing proceed now? | **No. Wait for the signed scope letter and two test accounts.** | **High** |
| Best next step | Owner-approved authenticated mapping plus source-assisted tracing and a staging `enc` adapter | **High** |

**Overall confidence: Moderate.** Confidence is high about the campaign gap and authorization requirement, but intentionally low about actual vulnerability state because authentication, backend identification, source-to-sink tracing, and controlled query tests have not occurred.

Before authorization, the club may safely study the cited materials, build owned SQL/NoSQL labs, install tools locally, write test manifests, and develop the response classifier using saved synthetic samples. It should not send more discovery, header, method, timing, fuzzing, or injection traffic to the live portal.

After authorization, begin with the least invasive evidence: normal authenticated request capture, owner-seeded records, architecture/source review, and telemetry. Only then run bounded DAST. Stop at minimal proof, never collect real student data, and treat any destructive, stacked, out-of-band, takeover, or denial-of-service capability as prohibited unless the letter names it explicitly.

## References

1. *NoSQL injection | Web Security Academy*. https://portswigger.net/web-security/nosql-injection
2. *WSTG - Latest | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05-Testing_for_SQL_Injection
3. *GitHub - projectdiscovery/nuclei: Nuclei is a fast, customizable vulnerability scanner powered by the global security community and built on a simple YAML-based DSL, enabling collaboration to tackle trending vulnerabilities on the internet. It helps you find vulnerabilities in your applications, APIs, networks, DNS, and cloud configurations. · GitHub*. https://github.com/projectdiscovery/nuclei
4. *ZAP – Report Generation*. https://www.zaproxy.org/docs/desktop/addons/report-generation/
5. *GitHub - ron190/jsql-injection: jSQL Injection is a Java application for automatic SQL database injection. · GitHub*. https://github.com/ron190/jsql-injection
6. *SQL Injection Scanner*. https://www.invicti.com/sql-injection-scanner/
7. *SQL query built from user-controlled sources — CodeQL query help  documentation*. https://codeql.github.com/codeql-query-help/csharp/cs-sql-injection/
8. *Query Parameterization - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Query_Parameterization_Cheat_Sheet.html
9. *Burp Scanner - Web Vulnerability Scanner from PortSwigger*. https://portswigger.net/burp/vulnerability-scanner
10. *Configuring Parameters And Parameter Data Types*. https://learn.microsoft.com/en-us/dotnet/framework/data/adonet/configuring-parameters-and-parameter-data-types
11. *GitHub - Charlie-belmer/nosqli: NoSql Injection CLI tool, for finding vulnerable websites using MongoDB. · GitHub*. https://github.com/Charlie-belmer/nosqli
12. *GitHub - semgrep/semgrep: Lightweight static analysis for many languages. Find bug variants with patterns that look like source code. · GitHub*. https://github.com/semgrep/semgrep
13. *GitHub - stamparm/DSSS: Damn Small SQLi Scanner · GitHub*. https://github.com/stamparm/DSSS
14. *GitHub - codingo/NoSQLMap: Automated NoSQL database enumeration and web application exploitation tool. · GitHub*. https://github.com/codingo/NoSQLMap
15. *Security Considerations (Entity Framework) - ADO.NET | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/framework/data/adonet/ef/security-considerations
16. *ZAP – SQL Injection*. https://www.zaproxy.org/docs/alerts/40018/
17. *GitHub - CiscoCXSecurity/bbqsql: SQL Injection Exploitation Tool · GitHub*. https://github.com/Neohapsis/bbqsql
18. *GitHub - r0oth3x49/ghauri: An advanced cross-platform tool that automates the process of detecting and exploiting SQL injection security flaws · GitHub*. https://github.com/r0oth3x49/ghauri
19. *License · sqlmapproject/sqlmap Wiki · GitHub*. https://github.com/sqlmapproject/sqlmap/wiki/License
20. *GitHub - wapiti-scanner/wapiti: Web vulnerability scanner written in Python3 · GitHub*. https://github.com/wapiti-scanner/wapiti
21. *Auditing - Azure SQL Database and Azure Synapse Analytics | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/azure-sql/database/auditing-overview?view=azuresql
22. *NoSQL Security - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/NoSQL_Security_Cheat_Sheet.html
23. *CRS and DRS rule groups and rules - Azure Web Application Firewall | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/web-application-firewall/ag/application-gateway-crs-rulegroups-rules
24. *sqlmap — automatic SQL injection and database takeover tool*. https://sqlmap.org/
25. *GitHub - github/codeql: CodeQL: the libraries and queries that power security researchers around the world, as well as code scanning in GitHub Advanced Security · GitHub*. https://github.com/github/codeql
26. *Benefits and Features of Defender for Azure SQL Databases - Microsoft Defender for Cloud | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-sql-introduction
27. *GitHub - projectdiscovery/nuclei-templates: Community curated list of templates for the nuclei engine to find security vulnerabilities. · GitHub*. https://github.com/projectdiscovery/nuclei-templates
28. *SQL Injection Scanner | Acunetix*. https://www.acunetix.com/vulnerability-scanner/sql-injection-scanner/
29. *database analyze - GitHub Docs*. https://docs.github.com/en/code-security/codeql-cli/codeql-cli-manual/database-analyze
30. *GitHub - zaproxy/zaproxy: The ZAP by Checkmarx Core project · GitHub*. https://github.com/zaproxy/zaproxy
31. *404 - Content not found*. https://learn.microsoft.com/en-us/previous-versions/aspnet/y123fsf7(v=vs.100)
32. *ZAP – Report Templates*. https://www.zaproxy.org/docs/desktop/addons/report-generation/templates/
33. *OWASP Secure Headers Project | OWASP Foundation*. https://owasp.org/www-project-secure-headers/
34. *ZAP – ZAP - Full Scan*. https://www.zaproxy.org/docs/docker/full-scan/
35. *bbqsql/LICENSE.md at master · CiscoCXSecurity/bbqsql · GitHub*. https://github.com/CiscoCXSecurity/bbqsql/blob/master/LICENSE.md
36. *HTTP Headers - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html
37. *Session Management - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
38. *sqlninja - a SQL Server injection & takeover tool*. https://sqlninja.sourceforge.net/
39. *bbqsql/LICENSE.md at master · CiscoCXSecurity/bbqsql · GitHub*. https://github.com/Neohapsis/bbqsql/blob/master/LICENSE.md
40. *sqlninja download | SourceForge.net*. https://sourceforge.net/projects/sqlninja/
41. *codeql/LICENSE at main · github/codeql · GitHub*. https://github.com/github/codeql/blob/main/LICENSE
42. *Running Nuclei - ProjectDiscovery Documentation*. https://docs.projectdiscovery.io/tools/nuclei/running
43. *Displaying A Custom Error Page Cs*. https://learn.microsoft.com/en-us/aspnet/web-forms/overview/older-versions-getting-started/deploying-web-site-projects/displaying-a-custom-error-page-cs
44. *404 - Content not found*. https://learn.microsoft.com/en-us/aspnet/core/security/error-handling?view=aspnetcore-9.0
45. *GitHub - CiscoCXSecurity/bbqsql: SQL Injection Exploitation Tool · GitHub*. https://github.com/CiscoCXSecurity/bbqsql
46. *sqlninja - a SQL Server injection & takeover tool*. https://sqlninja.sourceforge.net/sqlninja-howto.html
47. *CLI reference | Semgrep*. https://semgrep.dev/docs/cli-reference
48. *OWASP Web Security Testing Guide | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/
49. *Writing secure dynamic SQL in SQL Server - ADO.NET Provider for SQL Server | Microsoft Learn*. https://learn.microsoft.com/en-us/sql/connect/ado-net/sql/writing-secure-dynamic-sql?view=sql-server-ver17
50. *SQL Queries - EF Core | Microsoft Learn*. https://learn.microsoft.com/en-us/ef/core/querying/sql-queries
51. *Rules Of Engagement Template*. https://owasp.org/APTS/standard/appendix/Rules_of_Engagement_Template.html
52. *Logging - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
53. *WSTG - Latest | OWASP Web Security Testing Guide*. https://wstg.owasp.org/latest/
