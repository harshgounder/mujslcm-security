# MUJ SLCM Logic Testing Roadmap

## Executive Summary

- **Coverage Deficit**: The campaign baseline says business-logic coverage is **ABSENT**, with only **1 of 11** WSTG business-logic tests touched; OWASP WSTG 4.10 enumerates business-logic topics from data validation through malicious uploads, including integrity checks, process timing, function-use limits, workflow circumvention, and application misuse [13]. -> Treat the next authorized campaign as a state-machine and invariant campaign, not as another header, port, or generic scanner pass.

- **Target-Specific Workflow Risk**: MUJ documentation describes SLcM as a one-stop portal for academic information [40], provides the official SLCM URL [40], and documents onboarding steps in which students view declaration descriptions, are redirected to policy pages, return to SLCM, and have declaration checkboxes automatically ticked [40]. -> Prioritize workflow-order, acknowledgement, callback, and idempotency tests for declarations, fee payment, attendance, and marks only after authorization.

- **Public Exposure Is Narrow, But Logic Exposure Is Authenticated**: Public URLScan data for `mujslcm.jaipur.manipal.edu` shows HTTPS status 200, Microsoft-IIS/10.0, IP `98.70.14.50`, apex domain `manipal.edu`, ASN AS8075, and an Entrust DV TLS issuer [7]. The public login page presents MUJ portal sign-in text, an `@muj.manipal.edu` sign-in path, and parent login [12]. -> Pre-authorization work should remain OSINT, documentation review, and lab design; live workflow, account, parent, and fee tests require the signed letter and test accounts.

- **Race Conditions Are Logic Bugs, Not Just Load Bugs**: PortSwigger defines race conditions as vulnerabilities closely related to business-logic flaws that occur when websites process requests concurrently without adequate safeguards, allowing distinct threads to interact with the same data at the same time [32]. -> Tools that send parallel traffic are useful only when paired with a business invariant, such as one fee receipt per payment, one declaration acknowledgement per policy version, or one attendance mutation per authorized actor.

- **Tooling Can Synchronize Requests, But Cannot Know The Rules**: Burp Repeater group send is documented as sending grouped requests at once and being useful for identifying race conditions [39]; Turbo Intruder is a Burp extension for sending large numbers of HTTP requests and analyzing results [30]; Race The Web is a race-condition tester with REST API integration and an MIT license [50]. -> Use tools as traffic and evidence engines, not as proof engines; build a target-specific oracle that decides whether the final state violates MUJ rules.

- **Idempotency Is The Payment And Retry Control To Prove**: RFC 9110 defines idempotent methods as methods where multiple identical requests have the same intended server effect as one request [48], and Stripe documents idempotency keys as a way to retry requests without accidentally performing the same operation twice [53]. -> Any authorized fee-flow testing should verify server-side idempotency, duplicate callback handling, cancellation rollback, and reconciliation before and after concurrent retries.

- **Detection Must Mirror The Test Plan**: OWASP Logging guidance says applications should centrally log security-related events [44] and lists events that should be logged where possible [54]. -> Before running authenticated logic tests, agree with MUJ owners on expected log events for duplicate transitions, blocked workflow skips, anti-forgery failures, OTP failures, parent/student role mismatches, and payment reconciliation anomalies.

- **No-Tool Gaps Are The Main Opportunity**: OWASP notes that business-logic testing resembles finite-state testing and requires security professionals to develop abuse and misuse cases [24]. -> The security club should build lightweight state-graph, invariant, idempotency, and two-account choreography tools rather than expecting any scanner to discover target-specific academic and fee workflow violations.

- **Authorization Boundary Is Non-Negotiable**: The requester states that the prior campaign never authenticated and that aggressive work is gated behind a signed scope letter plus two test accounts. -> Safe pre-authorization work is limited to public-source review, passive metadata, lab reproduction, and written test plans; any live authenticated state change, parallel request group, fee workflow, OTP workflow, or parent/student role test must wait for written scope and test credentials.


## Scope, Evidence, And Safety Gates

This report is a defensive research plan for a university security club. It uses public sources plus the requester-provided measurement summary, and it intentionally omits endpoint-specific payloads, exploit reproduction strings, credential acquisition instructions, and live-test recipes that would enable unauthorized access. The public evidence base confirms the official SLCM URL, login surface, official student guidance, public scan metadata, OWASP methodology, PortSwigger race-condition concepts, and tool documentation [40][12][7][13][32]. The requester-provided measurement pack is treated as campaign context, not as independently reproduced public evidence.

The most important constraint is authorization. The public guide says users access the Student Lifecycle Management portal at `https://mujslcm.jaipur.manipal.edu` [40], and the public login page presents sign-in and parent-login paths [12]. Any test that changes authenticated state, submits a declaration, touches a fee workflow, probes marks or attendance, tests parent/student separation, sends repeated anti-forgery-protected requests, or generates parallel traffic against live authenticated endpoints is outside safe pre-authorization activity. Those tests need the signed scope letter, written test windows, rate limits, named test accounts, and rollback or reconciliation contacts.

### Safety Gate Matrix

| Activity | Safe Before Signed Scope? | Needs Letter And Test Accounts? | Why | Allowed Output |
|---|---:|---:|---|---|
| Read official MUJ pages, PDFs, public URLScan, crt.sh, OWASP, PortSwigger, and tool docs | Yes | No | It uses public information only; MUJ guide and portal pages are public [40][12]. | Notes, threat model, test design. |
| Build a local lab that imitates MVC anti-forgery, declaration acknowledgement, payment callback, and duplicate-submit behavior | Yes | No | Lab work does not touch MUJ systems. Microsoft documents MVC anti-forgery as a CSRF defense area for ASP.NET MVC [62]. | Code, state diagrams, detection rules, sample findings. |
| Passive certificate and scan-metadata review | Yes | No | URLScan and crt.sh are public metadata sources; URLScan shows the MUJ SLCM host, server, IP, AS, and TLS issuer [7], while crt.sh lists certificate names and validity periods for MUJ-related hostnames [36]. | Asset inventory and risk hypotheses. |
| One-off browser visit to the public login page | Usually yes, if institutional policy permits | No, if no authentication, no fuzzing, no volume | The public page contains only welcome and sign-in text in the extracted source [12]. | Screenshot or page note. |
| Header, TLS, and status checks against live target | Prefer written permission | Yes if repeated, automated, or outside normal browsing | Even non-destructive probes can be interpreted as scanning; the requester already has measured facts. | Limited baseline only under policy. |
| Authenticated workflow mapping with student and parent test accounts | No | Yes | It touches live authenticated state and role boundaries. | State graph and invariant table. |
| Burp Repeater group-send, Turbo Intruder, Race The Web, k6, Locust, JMeter, or any parallel traffic against MUJ | No | Yes | PortSwigger race testing relies on concurrent requests [32], which can create duplicate or inconsistent state if run against production. | Agreed test evidence only. |
| Fee payment, callback, cancellation, and reconciliation tests | No | Yes | Payment tests can affect ledgers and reconciliation; OWASP treats payment functionality as a business-logic testing area [34]. | Test-account receipts and owner-verified reconciliations. |
| Declaration acknowledgement and OTP workflow tests | No | Yes | MUJ guide documents policy-page redirects, automatic tick behavior, and OTP verification [40]. | Test-account-only audit trail. |

**Decision-ready insight:** Do not spend the next campaign on another unauthenticated scan. The safe pre-authorization deliverable is a test plan and lab harness; the live deliverable begins only after the written scope letter and accounts are issued.


## Target Model: Why MUJ SLCM Is A State-Machine Target

The public MUJ guide frames SLcM as the one-stop platform for academic information throughout a student's time at the university [40]. It also states that login credentials are sent to a personal Gmail account by Admissions [40], while the FAQ gives a registration link and says the password is as per the official Outlook ID [33]. The public page itself shows `WELCOME TO MUJ PORTAL`, `Sign In`, `@muj.manipal.edu`, and `Parent Login` [12]. Those facts matter because the portal is not just a static information site; it is an identity-mediated workflow application.

The declaration workflow is the clearest public state machine. The guide instructs students to view each declaration description, says the user will be redirected to the relevant policy page, says the user should read the instructions and return to SLCM, and says the checkbox will be automatically ticked [40]. It also says the parent mobile number will be verified by OTP [40]. **Inference:** a portal implementing those steps must maintain state across at least four boundaries: the SLCM session, the policy-page redirect, the declaration acknowledgement flag, and the OTP verification result. That inference is not a claim that a vulnerability exists; it is a test-planning observation derived from the documented flow.

The requester-provided measurements add the technical context: IIS 10, ASP.NET MVC 5.3, .NET Framework 4.7.4136.0, jQuery 1.10.2 plus bundled jQuery 3.4.1, Microsoft Azure AS8075, Microsoft 365 identity, three Entra tenants, no attributable edge control, no HSTS, TLS 1.0 through 1.3 offered, verbose YSOD on four triggers with `customErrors` off, MVC anti-forgery enforcement, an anti-forgery cookie that is HttpOnly but not Secure, two error page families, GET-only method policy, and a three-stage `enc` oracle. These are prompt-supplied campaign facts, not re-tested here. **Inference:** because the unauthenticated surface appears narrow and because the previous campaign did not authenticate, the highest-yield remaining work is not another unauthenticated endpoint hunt; it is a scoped, account-based workflow campaign.

Public scan data supports the narrow-surface view. URLScan observed `https://mujslcm.jaipur.manipal.edu/` with status 200, Microsoft-IIS/10.0, IP `98.70.14.50`, apex domain `manipal.edu`, AS8075, and Entrust DV TLS issuer metadata [7]. Certificate transparency results show MUJ SLCM-related names and Entrust-issued certificates for `muj.slcm.jaipur.manipal.edu` and `mujslcm.jaipur.manipal.edu` [36]. Those public facts do not prove the absence of hidden authenticated routes; they only show that publicly visible metadata is consistent with a centralized web application behind the MUJ domain.

The portal's business impact should be modeled in terms of invariants. For declarations, an acknowledgement should map to the correct user, policy version, time, and parent or student actor. For fees, a payment should map to one order, one receipt, one ledger posting, one gateway callback sequence, and one final status. For attendance and marks, a read or update should map to the correct role and record owner; an unofficial public repository describes an SLCM API for retrieving attendance and marks data from a Manipal University SLCM portal [70]. **Inference:** even when anti-forgery blocks basic CSRF and direct replay, bugs can remain in ordering, idempotency, role binding, and server-side reconciliation.

**Decision-ready insight:** Model MUJ SLCM as a set of finite-state workflows with academic, payment, identity, and acknowledgement invariants. The public evidence justifies planning those tests, but live validation must wait for authorization.


## Technique Universe Mapped To WSTG Business Logic

OWASP says business-logic testing is similar to logical or finite-state testing and requires misuse cases rather than only generic scanner checks [24]. PortSwigger says business logic vulnerabilities arise from flawed assumptions about user behavior and can have real impact [38]. For MUJ SLCM, that means the technique universe should be organized around state, actor, timing, and reconciliation rather than around individual HTTP parameters.

| Technique Family | Primary Standard Anchor | MUJ-Specific Authorized Test Question | Manual Or Tool-Driven? | Detection Counterpart |
|---|---|---|---|---|
| Workflow-order enforcement | WSTG workflow circumvention [13], plus OWASP advice to attempt skipping or reordering identified logic flows [34] | Can a declaration, fee, OTP, attendance, or marks workflow reach a final state without required prior states? | Manual first; then Playwright, Selenium, Cypress, Burp Repeater. | Log out-of-order transitions and reject them with a single terminal reason. |
| Business data validation | WSTG data validation [13]; OWASP says to identify data injection points and validate that checks occur on the back end [65] | Are hidden, disabled, client-controlled, or derived fields revalidated server-side? | Burp, ZAP fuzzer, ffuf, custom harness. | Log validation failures with field, workflow, actor, and correlation ID. |
| Request forgery and parameter derivation | WSTG ability to forge requests [13]; OWASP warns not to depend on non-editable controls or hidden fields for business logic processing [66] | Can a request be syntactically valid but semantically inconsistent with the authenticated user or workflow? | Burp Repeater, Autorize, AuthMatrix, ZAP. | Compare authenticated subject, route, record owner, and business role. |
| Integrity checks | WSTG integrity checks [13]; OWASP says applications should use strict access controls on how data and artifacts can be modified and read [66] | Can stored academic, payment, declaration, or profile data be changed into a logically invalid state? | Manual invariant tests plus AuthMatrix and Autorize. | Log unauthorized modification attempts and final-state conflicts. |
| Function-use limits | WSTG function-use limits [13]; OWASP says testers should identify functions that must set limits and verify those limits [59] | Can a one-time action be repeated by refresh, retry, back-button, double submit, or parallel submit? | Burp parallel send, Turbo Intruder, Race The Web, custom idempotency harness. | Duplicate-key, duplicate-transition, and per-user counter alerts. |
| Process timing | WSTG process timing [13]; OWASP says attackers may manipulate designed process flows by keeping sessions open outside expected timing [37] | Does a fee quote, declaration window, OTP window, or reserved state expire and roll back correctly? | Manual timed scenarios; k6/Locust/JMeter only under scope. | Expiry, timeout, rollback, and stale-state events. |
| Race conditions | PortSwigger says races occur when websites process requests concurrently without adequate safeguards [32] | Can simultaneous valid requests create duplicate receipts, duplicate acknowledgement, double use, stale result, or role mismatch? | Burp Repeater group send, Turbo Intruder, Race The Web, k6/Locust/JMeter. | Atomicity violation detection and post-test reconciliation. |
| Payment and reconciliation | OWASP payment guidance includes testing transaction cancellation or reduction after points or credits are applied [34] | Does the fee workflow record one final status, handle duplicate callbacks, and roll back failed or canceled steps? | Manual owner-witnessed test plus idempotency checks. | Gateway callback idempotency, ledger reconciliation, duplicate receipt alerts. |
| Anti-abuse and rate limits | WSTG application misuse [13]; OWASP recommends hard controls to prevent limit abuse [59] | Are OTP, declaration acknowledgement, parent login, and fee actions rate-limited by account and workflow state? | ZAP, Burp, k6/Locust only with scope. | Rate-limit counters, anomaly alerts, and lockout review. |
| Error-oracle resilience | Prompt-measured YSOD and `enc` behavior; OWASP logic testing asks testers to analyze how applications handle broken expected data [65] | Do error families leak state-machine distinctions or cryptographic branch information? | Pre-auth only if explicitly scoped; otherwise lab reproduction. | Aggregate exception family, size, and route without exposing stack traces. |

**Decision-ready insight:** The test universe is larger than race testing. Race is a timing amplifier for invariants already identified by WSTG: validation, forgery, integrity, use limits, workflow order, timing, and payment reconciliation.


## Tool Universe: What Performs These Tests And What It Produces

No tool can declare a university workflow correct by itself. The following matrix is the practical tool universe for this class of work: tools that can drive requests, coordinate users, fuzz parameters, traverse workflows, generate concurrency, or compare authorization outcomes. The safest use before authorization is local lab work and documentation review. Live use against MUJ requires scope except where the activity is purely passive public documentation review.

| Tool | Exact URL | Licence / Cost Model | Free, Self-Hosted, BYOK | How It Is Driven | Output Format | Best Fit For MUJ Logic Work | Live MUJ Gate |
|---|---|---|---|---|---|---|---|
| Burp Suite Repeater Group Send | https://portswigger.net/burp/documentation/desktop/tools/repeater/send-group | PortSwigger proprietary product; Community is free for core manual testing and Professional is commercial per official edition pages [71] | Desktop client; no BYOK required | Intercept authenticated requests, group them, and send the group in parallel | Burp project history, response comparisons, issue notes | Small, carefully scoped race probes and duplicate-submit checks | Needs letter and test accounts |
| Burp Suite Intruder / Logger / Comparer | https://portswigger.net/burp | Proprietary commercial/free-edition mix; official Burp page positions Burp as a web security testing toolkit [3] | Desktop client; no BYOK required | Manual request mutation, payload positions, response comparison | Burp UI, project file, exports | Parameter tamper, hidden-field, and response-delta review | Needs letter and test accounts for live authenticated flows |
| Turbo Intruder | https://github.com/PortSwigger/turbo-intruder | AGPL-3.0 license [30] | Free, self-hosted Burp extension; no BYOK | Python/Jython-style Burp extension scripts send many HTTP requests and analyze responses [30] | Results table and scripted analysis inside Burp | High-precision concurrency and timing tests once invariants are known | Needs letter, accounts, and rate limit |
| Race The Web | https://github.com/TheHackerDev/race-the-web | MIT license [50] | Free, self-hosted; no BYOK | Sends a user-specified number of simultaneous requests and includes a REST API for CI use [50] | Response uniqueness and API results | Dedicated duplicate-state race checks in a lab or scoped window | Needs letter and accounts |
| OWASP ZAP Access Control Testing | https://www.zaproxy.org/docs/desktop/addons/access-control-testing/ | ZAP project Apache-2.0 license [16] | Free, open source, self-hosted; no BYOK | Configure users, contexts, and access rules; ZAP compares accessible sections [29] | ZAP alerts, reports, session data | Student vs parent vs role access matrix | Needs letter and test accounts |
| ZAP Fuzzer / Scripts | https://www.zaproxy.org/docs/desktop/addons/fuzzer/ | Apache-2.0 ZAP project license [16] | Free, self-hosted; no BYOK | Fuzzer payloads and scripts through proxy | ZAP alerts, messages, reports | Server-side validation and hidden-field checks | Needs letter for live authenticated endpoints |
| AuthMatrix | https://portswigger.net/bappstore/30d8ee9f40c041b0bfec67441aad158e | MIT-style license grant in GitHub license text [9] | Free Burp extension; self-hosted; no BYOK | Define users, roles, and requests in an access-control matrix [28] | Matrix pass/fail and response diffs | Parent/student/administrator authorization matrix | Needs letter and multiple test accounts |
| Autorize | https://github.com/Quitten/Autorize | Repository/BApp extension; license must be checked from the current repository before campaign use [20] | Free Burp extension; self-hosted; no BYOK | Replays requests with lower-privilege or unauthenticated cookies to detect authorization enforcement gaps [20] | Burp extension table and response comparisons | IDOR and role-binding checks for marks, attendance, declarations | Needs letter and test accounts |
| Schemathesis | https://schemathesis.readthedocs.io/en/stable/explanations/stateful/ | MIT license [10] | Free, self-hosted; no BYOK | Property-based API testing; stateful mode chains API calls using response data [25] | CLI output, JUnit-style integrations, failure cases | If MUJ exposes documented APIs or captured schema can be modeled in lab | Live use needs letter; schema modeling can be pre-auth in lab |
| Newman | https://github.com/postmanlabs/newman | Apache-2.0 license per repository license notes [26] | Free, self-hosted CLI; Postman cloud optional; no BYOK for CLI | Runs Postman collections from CLI | CLI, JSON, JUnit, HTML via reporters | Repeatable workflow regression after manual capture | Needs letter and accounts for live runs |
| REST Assured | https://github.com/rest-assured/rest-assured | Apache-2.0 license [6] | Free, code library, self-hosted; no BYOK | Java tests express requests and assertions | Test framework output, CI reports | Custom invariant tests for API-like flows | Needs letter for live; safe in lab |
| k6 | https://grafana.com/docs/k6/latest/ | k6 is documented as open-source performance testing tooling [21]; repository license page should be checked for current AGPL terms [8] | Free OSS runner; self-hosted; Grafana Cloud optional; no BYOK for local | JavaScript scenarios with virtual users | End-of-test summaries and external outputs [57] | Scoped concurrency and retry pattern simulation | Needs letter, accounts, and low-rate window |
| Locust | https://docs.locust.io/en/stable/ | MIT license [2] | Free, self-hosted; no BYOK | Python user tasks and web UI | CSV exports and stats retrieval [47] | Multi-step user journeys with several test accounts | Needs letter and rate limits |
| Apache JMeter | https://jmeter.apache.org/usermanual/get-started.html | Apache ecosystem tooling under Apache License 2.0 [51] | Free, self-hosted; no BYOK | GUI or JMX test plans, thread groups, assertions | JTL, dashboard reports [52] | Controlled load and replay in staging or a written test window | Needs letter and rate limits |
| Vegeta | https://github.com/tsenart/vegeta | MIT license [15] | Free, self-hosted CLI/library; no BYOK | CLI attack files or Go library send fixed-rate requests | Text, JSON, histogram, plot/report formats per project docs [27] | Low-level request replay in a lab; less suited to anti-forgery workflows | Needs letter for live |
| hey | https://github.com/rakyll/hey | Apache-style project license page [19] | Free, self-hosted CLI; no BYOK | CLI HTTP load generator | Text statistics | Very simple idempotent endpoint timing in lab | Do not use live without scope |
| ffuf | https://github.com/ffuf/ffuf | MIT license [55] | Free, self-hosted CLI; no BYOK | Go-based web fuzzer with wordlists and matchers [55] | CLI plus structured output options [11] | Discovery of hidden parameters in a lab or explicitly scoped target | Needs letter for live fuzzing |
| Playwright Test | https://playwright.dev/docs/intro | Apache-2.0 license from Microsoft repository [4] | Free, self-hosted; no BYOK | TypeScript/JavaScript tests across Chromium, WebKit, Firefox; bundles runner, assertions, isolation, parallelization, and tooling [35] | Built-in reporters and custom reporters [56] | Browser-real workflow state graphs, declarations, parent/student flows | Needs letter and accounts for live |
| Selenium WebDriver | https://www.selenium.dev/documentation/webdriver/ | Apache-2.0 license from Selenium repository [17] | Free, self-hosted; no BYOK | Language bindings drive real browsers through WebDriver [49] | Test framework reports | Cross-browser workflow regression and role checks | Needs letter and accounts for live |
| Cypress | https://docs.cypress.io/app/tooling/reporters | MIT license from Cypress repository [14] | Free OSS runner; paid cloud optional; no BYOK for local | JavaScript browser tests | Built-in/custom reporters [58] | Developer-friendly workflow tests in a lab or staging | Needs letter and accounts for live |

**Decision-ready insight:** For MUJ, the best stack is not one tool. Use Burp for capture and small races, Playwright or Selenium for stateful browser journeys, AuthMatrix or ZAP for role matrices, and a custom invariant checker for final-state correctness.


## Manual Method Where No Tool Exists

A business-logic tool can send traffic, but it cannot infer the university's rules. OWASP explicitly says testers should consider the business function, limits on behavior, and whether the application enforces those rules [24]. The manual method is therefore the core method, and tooling should be added only after the rules are written down.

Start with a **state inventory**. For each workflow, list states, transitions, actors, irreversible side effects, and rollback rules. A declaration workflow might include `not viewed`, `policy opened`, `returned`, `acknowledged`, `submitted`, and `locked`; that is an inference based on the guide's redirect, return, auto-tick, and submission language [40]. A fee workflow might include `quote`, `order created`, `gateway pending`, `callback received`, `receipt issued`, `ledger posted`, and `failed`; that is an inference based on normal payment architecture and OWASP's payment functionality guidance, not a claim about MUJ internals [34]. Attendance and marks workflows should distinguish read-only student access, parent visibility, staff update paths if scoped, and record ownership.

Next write **invariants**. Examples: one declaration acknowledgement per student per policy version; parent OTP verification cannot mark a student declaration complete; a fee receipt cannot exist without a settled payment; a canceled fee order cannot later become paid without a valid callback; a student cannot view another student's marks or attendance; replaying a final submit does not duplicate side effects; stale anti-forgery tokens fail without changing state. These are defensive test assertions. They are not instructions to bypass controls, and they must be tested only with agreed test accounts.

Then create **misuse cases**. OWASP workflow guidance says testers should review documentation for ways to skip steps or execute them in a different order and attempt to circumvent identified logic flows [34]. For MUJ, the authorized tester should ask: what happens if a user repeats a submit after success, returns after timeout, opens two tabs, uses parent and student sessions in parallel, or receives a gateway retry? OWASP process-timing guidance says some processes are dependent on time windows and that automation is better suited to precise timing analysis [37]. That supports careful timed tests in a written window, not uncontrolled load.

Finally define **evidence rules** before running anything. Each test should produce a before-state, request group ID, correlation ID, expected invariant, observed final state, logs requested from the owner, and cleanup status. If a test fails to produce owner-visible logs, that is itself a detection gap. If a test produces inconsistent UI but consistent server state, record it as a UX or cache issue, not as a business-logic vulnerability.

**Decision-ready insight:** The manual deliverable is a state model plus invariants. Without that, race tools will only generate traffic and screenshots, not defensible findings.


## Detection Counterpart: What MUJ Owners Should See

Detection must be designed at the same time as testing. OWASP Logging guidance is explicitly about building application logging mechanisms for security logging [54], and it states that applications should log security-relevant events where possible [54]. RFC 9110 also notes that servers commonly append request information to access logs when each response completes [48], but access logs alone will not prove business correctness. A reverse proxy log can show repeated requests; only the application can show whether the second request changed academic, declaration, or payment state.

| Detection Need | Event To Capture | Why It Matters | Implementation Direction | Authorization Stage |
|---|---|---|---|---|
| Workflow order | Rejected transition with current state, requested transition, actor, role, and correlation ID | Workflow bypass is a WSTG business-logic category [13] | Application event log, not only IIS access log | Before authorized test window |
| Duplicate submit | Same user, same workflow object, repeated final action, same or absent idempotency key | Function-use limits are a WSTG category [13] | Unique server-side transition key plus duplicate alert | Before race testing |
| Payment idempotency | Order ID, gateway event ID, idempotency key, amount, status, callback sequence | Stripe saves the first status code and body for an idempotency key and returns the same result on later uses [53] | Idempotency table and reconciliation job | Before fee testing |
| Parameter integrity | Hidden or client-derived field mismatch against server record | OWASP warns against relying on hidden, disabled, or non-editable controls for business logic [66] | Server-side lookup and reject log | Before authenticated tamper tests |
| Role boundary | Student, parent, staff role, target record owner, decision, and policy | Strict access controls are required for data modification and reading [66] | Authorization decision logging | Before parent/student tests |
| OTP abuse | OTP request count, verification count, failure reason, expiry, actor | The MUJ guide documents parent mobile OTP verification [40] | Rate-limit and failure telemetry | Before OTP testing |
| Anti-forgery failures | Token missing, malformed, expired, wrong session, and no state change | Microsoft documents XSRF/CSRF prevention for ASP.NET MVC and web pages [62] | Security event plus state-change assertion | Before replay tests |
| Error oracle | Exception family, route, correlation ID, authenticated state, response class | Prompt measurements reported verbose YSOD and distinct error families; do not reproduce without scope | Central exception handling and sanitized client response | Before any retest |

The detection program should also use HTTP idempotency correctly. RFC 9110 defines idempotent methods by intended server effect, not by response identity [48]. Stripe's implementation guidance adds the operational pattern: the server recognizes retries using a unique idempotency key and compares later parameters to the original request to prevent accidental misuse [53]. **Inference:** for MUJ fee-like workflows, an idempotency table should bind user, order, amount, term, gateway reference, and final state. A duplicate retry should be harmless, and a mismatched retry should be rejected and logged.

**Decision-ready insight:** The detection counterpart is a duplicate-transition and invariant-violation program, not just a WAF rule. If MUJ owners cannot observe final-state invariants in logs, the security club should treat that as a prerequisite remediation before running concurrency tests.


## No-Tool Gaps And Build Candidates

The largest gap is semantic: existing tools cannot know whether a specific SLCM final state is allowed. OWASP's guidance to develop abused and misused cases explains why generic scanning underperforms here [24]. PortSwigger's race methodology and Burp tooling can improve timing precision, but the proof still comes from the application's final state and logs [32]. The security club can make the next campaign materially better by building small tools that encode MUJ-specific rules without embedding live secrets or endpoint payloads.

| No-Tool Gap | Why Existing Tools Miss It | Build Candidate | Inputs | Outputs | Safe Pre-Auth? |
|---|---|---|---|---|---|
| State-graph drift | Proxies record requests, not intended workflow states | **SLCM StateGraph Recorder** | Manually labeled steps from lab or test account sessions | DOT graph, transition table, missing-state report | Yes in lab; live needs scope |
| Business invariant oracle | Race tools compare responses, not ledgers or declarations | **Invariant DSL** | Rules such as one receipt per order or one acknowledgement per policy version | Pass/fail with before and after evidence | Yes in lab; live needs owner data |
| Idempotency visibility | Load tools cannot see server dedupe tables | **Idempotency Auditor** | Request group IDs, order IDs, expected final state | Duplicate, mismatch, and replay classification | Yes in lab; live needs fee-test scope |
| Two-account choreography | AuthMatrix helps roles, but not simultaneous parent/student timing | **Two-Actor Runner** | Student and parent test sessions, scripted state labels | Timeline, role-decision matrix, collision notes | Live only after scope |
| Declaration acknowledgement semantics | Browser tools can click, but cannot prove policy-version binding | **Declaration Version Checker** | Policy ID, visible declaration, acknowledgement result | Evidence that acknowledgement maps to correct policy version | Lab now; live with test accounts |
| Payment gateway callback safety | Generic tools should not hit real gateways | **Payment Callback Simulator** | Lab-only callback schemas and fake gateway events | Duplicate callback, reversal, and mismatch tests | Yes in lab only |
| Error-oracle regression | Scanners flag errors, but not branch-size families over time | **Exception Family Monitor** | Owner-approved status, length, and family labels | Regression chart and sanitized exception class counts | Pre-auth only with public data; live needs scope |
| Detection-as-code | Logs are usually reviewed after the fact | **Logic Detection Pack** | Expected events for blocked skip, duplicate submit, stale token, role mismatch | SIEM rules, test event catalog, dashboard | Yes if synthetic; live needs owner logs |
| Evidence bundle quality | Tools scatter screenshots, proxy history, and logs | **Finding Packager** | Test ID, invariant, request group, screenshots, log extracts | Owner-ready report with cleanup status | Yes |

**Decision-ready insight:** Build candidates should avoid exploit automation against MUJ. The useful artifacts are state labels, invariant assertions, deduplication keys, and evidence packaging that make authorized testing safer and more reviewable.


## Synthesis: How The Strategies Fit Together

The evidence points to a staged campaign. Public information establishes that MUJ SLCM is an authenticated student portal with official SLCM and parent-login entry points [40][12]. OWASP establishes that business-logic testing is finite-state and misuse-case driven [24]. PortSwigger establishes that race conditions are a concurrency subclass of business-logic flaws [32]. Tool documentation establishes that modern tooling can drive synchronized requests, role matrices, stateful API chains, browser journeys, and load patterns [30][29][25][35]. The non-obvious conclusion is that the next MUJ campaign should begin with documentation and lab models, not with traffic.

| Strategy | Mechanism | Scope | Trade-Off | Evidence Base | Best Time Horizon |
|---|---|---|---|---|---|
| Public OSINT | Uses official PDFs, portal page, URLScan, crt.sh | Asset and workflow hypothesis | Cannot validate authenticated behavior | Official guide and public scan metadata [40][7][36] | Now |
| Manual WSTG state modeling | Converts workflows into states, transitions, and misuse cases | Declarations, fees, attendance, marks, roles | Slow, but highest semantic accuracy | OWASP finite-state and misuse-case guidance [24] | Now in lab; live after scope |
| Burp and race tooling | Sends precise repeated or simultaneous requests | Known high-value transitions | Can cause duplicate state if uncontrolled | PortSwigger race definition and Turbo Intruder docs [32][30] | After scope, low-rate window |
| Role-matrix tooling | Replays requests across actors and roles | Student, parent, staff if provided | Requires clean test accounts and owner-approved roles | ZAP access-control add-on and AuthMatrix docs [29][28] | After accounts issued |
| Browser workflow automation | Replays realistic UI state machines | Declarations, OTP, payment UI | Brittle unless states are labeled | Playwright and Selenium workflow automation docs [35][49] | Lab now; live after scope |
| Detection-as-code | Mirrors tests in logs, idempotency, and alerts | Duplicate transitions, stale tokens, workflow skips | Needs owner cooperation | OWASP logging and idempotency sources [54][53] | Before live concurrency |

The central tension is precision versus safety. Race tools are precise at timing, but low in semantic awareness. Browser automation is high in workflow realism, but it may hide request-level invariants unless paired with proxy capture and server logs. Role-matrix tools are strong for access control, but they do not automatically prove payment or declaration state correctness. Manual WSTG modeling is slow, but it is the only method that turns university policy into testable security rules.

The second tension is public visibility versus true risk. Public scans can show IIS, IP, certificate, and login-page metadata [7][12]. They cannot show whether a student can double-submit a fee action, whether a declaration acknowledgement is policy-version-bound, or whether parent login creates a confused-deputy condition. That is why the campaign status to beat is not a missing port or header finding; it is missing authenticated business-logic coverage.

**Decision-ready insight:** The best next step is a two-track plan. Track 1, before authorization, produces the state model, lab harness, tool selection, and detection requirements. Track 2, after the signed letter and two test accounts, runs low-volume, owner-observed tests against the highest-impact invariants.


## VERDICT

**Verdict:** The next MUJ SLCM campaign should prioritize authenticated business-logic, state-machine, idempotency, and race-condition testing over additional unauthenticated scanning. Public sources confirm that SLCM is an official student portal and login surface [40][12], and OWASP/PortSwigger sources confirm that the relevant defect class is finite-state, misuse-case, and concurrency-sensitive [24][32]. The requester-provided measurement pack indicates that the previous campaign did not authenticate and that aggressive testing is gated; therefore, live testing must not begin until the signed scope letter, test accounts, test windows, owner log access, and rollback contacts are in place.

**Confidence level:** **High** for the methodology, safety gates, and tool taxonomy because they are grounded in OWASP, PortSwigger, official MUJ public pages, and official tool documentation. **Medium** for target-specific prioritization because key live facts, such as verbose error triggers, `enc` oracle behavior, HSTS, TLS offerings, Microsoft 365 tenant structure, and jQuery versions, come from the requester-provided measurement pack and were not re-tested in this report. **Low** for any hidden authenticated workflow detail not visible in public documents; those details must be validated only with authorized test accounts.

**Bottom line:** Beat the **ABSENT** business-logic baseline by producing, in order, a state graph, invariant list, detection plan, scoped tool harness, and owner-observed two-account test run. Do not run live parallel, fee, OTP, declaration, attendance, marks, or role-boundary tests without the signed authorization package.

## References

1. *turbo-intruder/LICENSE at master · PortSwigger/turbo-intruder · GitHub*. https://github.com/PortSwigger/turbo-intruder/blob/master/LICENSE
2. *locust/LICENSE at master · locustio/locust · GitHub*. https://github.com/locustio/locust/blob/master/LICENSE
3. *Burp - Web Application Security, Testing, & Scanning - PortSwigger*. https://portswigger.net/burp
4. *playwright/LICENSE at main · microsoft/playwright · GitHub*. https://github.com/microsoft/playwright/blob/main/LICENSE
5. *Locust Documentation*. https://docs.locust.io/en/stable/
6. *rest-assured/LICENSE at master · rest-assured/rest-assured · GitHub*. https://github.com/rest-assured/rest-assured/blob/master/LICENSE
7. *urlscan.io*. https://urlscan.io/api/v1/search?q=domain:mujslcm.jaipur.manipal.edu
8. *k6/LICENSE.md at master · grafana/k6 · GitHub*. https://github.com/grafana/k6/blob/master/LICENSE.md
9. *auth-matrix/LICENSE at master · PortSwigger/auth-matrix · GitHub*. https://github.com/PortSwigger/auth-matrix/blob/master/LICENSE
10. *schemathesis/LICENSE at master · schemathesis/schemathesis · GitHub*. https://github.com/schemathesis/schemathesis/blob/master/LICENSE
11. *ffuf/LICENSE at master · ffuf/ffuf · GitHub*. https://github.com/ffuf/ffuf/blob/master/LICENSE
12. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
13. *WSTG - v4.2 | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/10-Business_Logic_Testing/README
14. *cypress/LICENSE at develop · cypress-io/cypress · GitHub*. https://github.com/cypress-io/cypress/blob/develop/LICENSE
15. *vegeta/LICENSE at master · tsenart/vegeta · GitHub*. https://github.com/tsenart/vegeta/blob/master/LICENSE
16. *zaproxy/LICENSE at main · zaproxy/zaproxy · GitHub*. https://github.com/zaproxy/zaproxy/blob/main/LICENSE
17. *selenium/LICENSE at trunk · SeleniumHQ/selenium · GitHub*. https://github.com/SeleniumHQ/selenium/blob/trunk/LICENSE
18. *GitHub - PortSwigger/auth-matrix: AuthMatrix is a Burp Suite extension that provides a simple way to test authorization in web applications and web services. · GitHub*. https://github.com/PortSwigger/auth-matrix
19. *GitHub - rakyll/hey: HTTP load generator, ApacheBench (ab) replacement · GitHub*. https://github.com/rakyll/hey
20. *GitHub - Quitten/Autorize: Automatic authorization enforcement detection extension for burp suite written in Jython developed by Barak Tawily in order to ease application security people work and allow them perform an automatic authorization tests · GitHub*. https://github.com/Quitten/Autorize
21. [Grafana k6 | Grafana k6 documentation
](https://grafana.com/docs/k6/latest/)
22. *newman/LICENSE.md at develop · postmanlabs/newman · GitHub*. https://github.com/postmanlabs/newman/blob/develop/LICENSE.md
23. *hey/LICENSE at master · rakyll/hey · GitHub*. https://github.com/rakyll/hey/blob/master/LICENSE
24. *WSTG - v4.2 | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/10-Business_Logic_Testing/00-Introduction_to_Business_Logic
25. *Understanding Stateful Testing*. https://schemathesis.readthedocs.io/en/stable/explanations/stateful/
26. *GitHub - postmanlabs/newman: Newman is a command-line collection runner for Postman · GitHub*. https://github.com/postmanlabs/newman
27. *GitHub - tsenart/vegeta: HTTP load testing tool and library. It's over 9000! · GitHub*. https://github.com/tsenart/vegeta
28. *AuthMatrix - PortSwigger*. https://portswigger.net/bappstore/30d8ee9f40c041b0bfec67441aad158e
29. *ZAP – Access Control Testing*. https://www.zaproxy.org/docs/desktop/addons/access-control-testing/
30. *GitHub - PortSwigger/turbo-intruder: Turbo Intruder is a Burp Suite extension for sending large numbers of HTTP requests and analyzing the results. · GitHub*. https://github.com/PortSwigger/turbo-intruder
31. *Autorize - PortSwigger*. https://portswigger.net/bappstore/f9bbac8c4acf4aefa4d7dc92a991af2f
32. *Race conditions | Web Security Academy*. https://portswigger.net/web-security/race-conditions
33. *Frequently Asked Questions and Contacts for SLCM Registration*. https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf
34. *WSTG - v4.2 | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/10-Business_Logic_Testing/06-Testing_for_the_Circumvention_of_Work_Flows
35. *Installation | Playwright*. https://playwright.dev/docs/intro
36. *crt.sh*. https://crt.sh/?output=json&q=%.jaipur.manipal.edu
37. *WSTG - v4.2 | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/10-Business_Logic_Testing/04-Test_for_Process_Timing
38. *Business logic vulnerabilities | Web Security Academy*. https://portswigger.net/web-security/logic-flaws
39. *Sending grouped HTTP requests - PortSwigger*. https://portswigger.net/burp/documentation/desktop/tools/repeater/send-group
40. *Manipal University Jaipur First-Year Student Profile Registration Guide*. https://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf
41. *Smashing the state machine: the true potential of web race conditions | PortSwigger Research*. https://portswigger.net/research/smashing-the-state-machine
42. *The Selenium Browser Automation Project | Selenium*. https://www.selenium.dev/documentation/
43. [Apache JMeter
          -
          User's Manual: Getting Started](https://jmeter.apache.org/usermanual/get-started.html)
44. *Burp Suite Professional - PortSwigger*. https://portswigger.net/burp/pro
45. *Schemathesis CLI Reference*. https://schemathesis.readthedocs.io/en/stable/reference/cli/
46. *GitHub - schemathesis/schemathesis: Catch API bugs before your users do · GitHub*. https://github.com/schemathesis/schemathesis
47. *Retrieve test statistics in CSV format*. https://docs.locust.io/en/stable/retrieving-stats.html
48. *RFC 9110: HTTP Semantics*. https://www.rfc-editor.org/rfc/rfc9110.html
49. *WebDriver | Selenium*. https://www.selenium.dev/documentation/webdriver/
50. *GitHub - TheHackerDev/race-the-web: Tests for race conditions in web applications. Includes a RESTful API to integrate into a continuous integration pipeline. · GitHub*. https://github.com/TheHackerDev/race-the-web
51. *Apache License, Version 2.0 | Apache Software Foundation*. https://www.apache.org/licenses/LICENSE-2.0
52. [Apache JMeter
          -
          User's Manual: Generating Dashboard Report](https://jmeter.apache.org/usermanual/generating-dashboard.html)
53. *Idempotent requests*. https://docs.stripe.com/api/idempotent_requests
54. *Logging - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
55. *GitHub - ffuf/ffuf: Fast web fuzzer written in Go · GitHub*. https://github.com/ffuf/ffuf
56. *Reporters | Playwright*. https://playwright.dev/docs/test-reporters
57. [Results output | Grafana k6 documentation
](https://grafana.com/docs/k6/latest/results-output/)
58. *Built-in and custom reporters in Cypress: setup guide | Cypress Documentation*. https://docs.cypress.io/app/tooling/reporters
59. *WSTG - v4.2 | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/10-Business_Logic_Testing/05-Test_Number_of_Times_a_Function_Can_Be_Used_Limits
60. *Security, Authentication, and Authorization with ASP.NET MVC | Microsoft Learn*. https://learn.microsoft.com/en-us/aspnet/mvc/overview/security/
61. *WSTG - v4.2 | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/10-Business_Logic_Testing/02-Test_Ability_to_Forge_Requests
62. *XSRF/CSRF Prevention in ASP.NET MVC and Web Pages | Microsoft Learn*. https://learn.microsoft.com/en-us/aspnet/mvc/overview/security/xsrfcsrf-prevention-in-aspnet-mvc-and-web-pages
63. *WSTG - v4.2 | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/10-Business_Logic_Testing/07-Test_Defenses_Against_Application_Misuse
64. *Business Logic Security - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Business_Logic_Security_Cheat_Sheet.html
65. *WSTG - v4.2 | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/10-Business_Logic_Testing/01-Test_Business_Logic_Data_Validation
66. *WSTG - v4.2 | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/10-Business_Logic_Testing/03-Test_Integrity_Checks
67. *OWASP Application Security Verification Standard (ASVS) | OWASP Foundation*. https://owasp.org/www-project-application-security-verification-standard/
68. *WSTG - v4.2 | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/10-Business_Logic_Testing/08-Test_Upload_of_Unexpected_File_Types
69. *WSTG - v4.2 | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/10-Business_Logic_Testing/09-Test_Upload_of_Malicious_Files
70. *http://github.com/tejaskash/slcm-api*. http://github.com/tejaskash/slcm-api
71. *Download Burp Suite - PortSwigger*. https://portswigger.net/burp/downloads
