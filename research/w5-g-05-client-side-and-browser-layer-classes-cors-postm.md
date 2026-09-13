# MUJ SLCM Browser-Layer Security Research Report

## Executive Summary

- **Primary Exposure Question**: The absent campaign brief is justified. CORS must be assessed separately from ordinary header review because the browser decides whether cross-origin JavaScript may read a response, and credentialed access requires an explicit allowed origin rather than `*` [16]. -> Add a dedicated CORS workstream before any authenticated API testing.
- **Highest-Value Safe First Step**: A passive inventory of scripts, frames, fetch/XHR calls, response headers, and public JavaScript can be performed without logging in or modifying the target. -> Establish an endpoint and origin inventory before sending any active cross-origin probes.
- **Authentication Risk**: The supplied target facts identify Microsoft 365/Entra identity and a portal campaign that has never authenticated. This does not prove that a particular endpoint is credentialed or CORS-enabled. It does mean that a permissive policy, if present on a session-bearing endpoint, could be materially more serious than a policy on public content. This is an inference from the supplied architecture and the browser rules, not a finding about MUJ.
- **Tooling Reality**: CORS has the strongest mature command-line coverage through CORScanner, Corsy, Nuclei, and ZAP. Web messaging and client-side prototype pollution have better browser instrumentation through Burp DOM Invader than through ordinary HTTP scanners [14][17]. -> Use complementary tools rather than treating one scanner result as coverage of the whole class.
- **CSP Boundary**: CSP tools can evaluate headers and policy weaknesses, but a missing or weak policy is not equivalent to an exploitable XSS. CSP is defense in depth and does not replace input sanitization [8][3]. -> Report CSP posture separately from exploitability.
- **Main Automation Gap**: No public tool identified in this review reliably correlates all four layers - CORS policy, authenticated browser state, postMessage trust, prototype-pollution source/gadget/sink, and CSP enforcement - into one evidence chain. -> Build a consent-gated browser harness that emits raw request/response evidence and replayable, non-destructive observations.
- **Authorization Gate**: Public, unauthenticated observation and inspection are appropriate pre-authorization only when limited to ordinary browsing and low-rate retrieval of public resources. Credentialed requests, origin-manipulation experiments, replay, controlled payloads, CSP enforcement checks, and any test-account workflow require the signed scope letter and two test accounts.
- **Current Verdict**: No CORS, postMessage, prototype-pollution, or CSP vulnerability is established by the supplied facts. The correct status is **unassessed / absent from the campaign**, with **high confidence** that a dedicated brief is warranted and **low confidence** about the target's actual exposure until authorized browser-layer testing is completed.

## Scope, Evidence, and Safety Rules

The target profile and live measurements in the request are treated as supplied observations dated 2026-09-13: IIS 10, ASP.NET MVC 5.3, .NET Framework 4.7.4136.0, jQuery 1.10.2 plus bundled jQuery 3.4.1, Azure AS8075, Microsoft 365 identity, three Entra tenants, no attributable edge control, no HSTS, TLS 1.0 through 1.3 offered, 443 as the only reachable port, verbose YSOD behavior, antiforgery behavior, error-page sizes, method behavior, the `enc` oracle, and clean host-header/trust-bypass attempts. Those are campaign measurements supplied by the requester, not independently re-run here. The report does not convert them into new findings.

The public evidence establishes the security mechanisms, not the MUJ configuration. OWASP describes CORS testing as identifying endpoints that implement CORS and determining whether their configuration is secure or harmless [16]. The browser uses the preflight result to decide whether a cross-origin request is permitted [16]. Therefore, ordinary header review that did not vary `Origin`, inspect preflight behavior, or observe browser readability is incomplete for this question. That is an analytical conclusion from the cited browser behavior, not a claim that MUJ is vulnerable.

The safety model has three tiers:

| Activity | Pre-authorization status | Reason and evidence | Output to retain |
|---|---|---|---|
| Read public pages and ordinary public static assets at low rate | Generally safe, subject to university policy and robots/rules | Passive observation does not require authentication; OWASP describes passive inspection of requests, responses, origins, and CORS headers [16] | URL, timestamp, status, selected headers, hash of public asset |
| Inspect downloaded JavaScript locally; run CodeQL or dependency analysis against an authorized code copy | Safe when the code copy is lawfully obtained | Static analysis does not send traffic to MUJ; CodeQL provides queries for missing origin checks and prototype-polluting patterns [34][27] | Query version, commit, findings, source location |
| Vary `Origin`, send preflight, replay messages, use DOM Invader, test `enc`, use test accounts, or submit controlled payloads | Requires signed scope letter; authenticated work also requires the two test accounts | These actions create target traffic or interact with authentication state. CSP validation may involve controlled payloads [8]; DOM Invader can generate and send messages or pollution proofs [14][17] | Full raw exchange, authorization reference, account identifier, rollback notes |

Do not use the report as permission. Do not attempt to obtain credentials, bypass Entra controls, enumerate tenant access, alter data, or use a third-party origin to read authenticated content. A browser-layer finding should be demonstrated with the minimum authorized request and a synthetic or non-sensitive response wherever possible.

## Technique Universe

### CORS

CORS is a browser-controlled mechanism that allows selected cross-origin requests. The key questions are: which endpoints return CORS headers; whether `Access-Control-Allow-Origin` is fixed, reflected, wildcarded, or pattern-based; whether credentials are accepted; whether preflight permits methods and headers beyond the endpoint's need; whether `Vary: Origin` is present when the response changes by origin; and whether sensitive responses are actually readable by an authorized browser context. OWASP specifically warns that `Access-Control-Allow-Origin: *` is unsafe for sensitive responses [16]. Credentialed responses require an explicit origin, and credentials cannot be combined with wildcard ACAO [16].

The test universe includes simple requests, preflighted requests, redirects, error responses, JSON and non-JSON endpoints, public and session-bearing resources, dynamic origin reflection, `null`, subdomain and suffix/prefix matching, scheme and port changes, allowed methods, allowed request headers, exposed response headers, cache variation, and failure behavior. A positive ACAO header alone is not proof of data exposure: the browser may refuse credentials, the endpoint may be public, or the response may contain no sensitive data. Conversely, a clean unauthenticated result does not clear an authenticated API.

For MUJ, the first authorized question should be whether the portal page or its JavaScript calls same-origin MVC endpoints only, or whether it calls tenant, identity, API, CDN, or third-party origins. The second should be whether any authenticated session is represented by cookies, bearer tokens, or both. The third should be whether any allowed origin is an untrusted origin in the real deployment model. These are prioritization questions, not instructions to attack.

### postMessage and Web Messaging

`window.postMessage()` enables cross-origin communication between windows, frames, and popups. OWASP says the receiver should restrict messages to trusted domains, specify an expected target origin instead of `*`, validate the sender before manipulating data, and treat message data as untrusted [7]. The origin comprises scheme, hostname, and port; URL path and fragment are not part of the origin [7].

The universe includes sender-side wildcard `targetOrigin`, receiver-side missing or weak `event.origin` checks, unsafe substring or suffix checks, failure to validate `event.source`, message type confusion, JSON parsing and schema confusion, sensitive data sent to an unexpected frame, navigation or redirect races, sandboxed or opaque `null` origins, messages that flow into `innerHTML`, `eval`, URL navigation, storage, DOM sinks, or API calls, and messages crossing an identity popup or embedded tenant boundary. OWASP gives a concrete example of an unsafe substring check that can accept an attacker-controlled suffix domain [7].

A message listener existing is not a vulnerability. The evidence chain must show an untrusted sender or target, inadequate validation, and a security-relevant consequence. Safe pre-authorization work is local source review and observing message names in an ordinary public browser session without sending modified messages. Replay, forged-origin simulation, message modification, or proof-of-concept generation waits for authorization.

### Client-Side Prototype Pollution

Prototype pollution occurs when attacker-controlled keys modify a shared JavaScript prototype, commonly `Object.prototype`; CodeQL notes that most JavaScript objects inherit from it, allowing polluted properties to affect application logic. The source universe includes URL query strings and fragments, form serializers, JSON objects, web-message data, deep merge or extend utilities, and configuration objects. OWASP identifies URL bracket/dot notation and JSON bodies that are deserialized and merged or cloned as important review areas [search result 65 snippet].

The sink universe includes DOM XSS gadgets, script or URL construction, request configuration, authorization or feature flags, sanitization bypasses, and library options that become dangerous when an inherited property appears. A source is not enough. DOM Invader documentation explicitly says a source is useful only when a controllable property reaches a gadget and then a sink without proper sanitization [14]. That source-gadget-sink distinction is essential for avoiding inflated findings.

For MUJ, the bundled jQuery versions and any other client libraries are a triage clue, not proof of a vulnerable merge path. Static inspection of locally obtained scripts is safe. Injecting pollution keys into live URLs, messages, or authenticated requests, or allowing an instrumented browser to generate a proof of concept, requires the signed scope and should use a test account and synthetic data.

### CSP

CSP is a declarative allow-list policy delivered mainly by the `Content-Security-Policy` response header or a meta element. It restricts resource sources and provides defense in depth against XSS and data injection [8]. The universe includes absence of CSP; report-only without enforcement; overly broad `default-src`, `script-src`, `connect-src`, `frame-src`, `frame-ancestors`, and `object-src`; unsafe-inline and unsafe-eval; wildcard, scheme, data, blob, or broad third-party sources; nonce and hash lifecycle errors; ineffective `strict-dynamic`; missing coverage on sensitive responses; weak reporting; and inconsistent policies across redirects, errors, and authenticated pages.

A policy should be evaluated, not merely detected. OWASP says testing requires determining whether the policy meaningfully reduces attack surface and is properly enforced [8]. Report-only monitors violations without enforcing them [3]. A controlled enforcement test can be appropriate under authorization, but it must not use a destructive or data-exfiltrating payload. CSP is not input sanitization and should not be reported as a substitute for it [3].

## Tool Matrix

The table separates tools that send HTTP traffic, tools that instrument a browser, static-analysis engines, policy evaluators, and repositories that are references rather than scanners.

| Class | Tool and exact URL | Licence / operating model | How driven | Output | Coverage and limitation |
|---|---|---|---|---|---|
| CORS | CORScanner, https://github.com/chenjj/CORScanner | MIT; free and self-hosted Python tool [4] | CLI or Python library; accepts URL, URL-list, headers, proxy, timeout, and threads [4] | Console/verbose output, JSON file, or Python dict with URL, type, credentials, origin, status [4] | Tests reflection, prefix/suffix, dot, substring, null, scheme, subdomain, and special-character cases [4]. No complete limitation list is stated by its page. |
| CORS | Corsy, https://github.com/s0md3v/Corsy | GPL-3.0; free/self-hosted repository [1] | Python CLI with URL, file, stdin, threads, delay, headers, and JSON export [1] | JSON including description, severity, exploitation fields [1] | Tests wildcard, reflection, null, prefix/post-domain, dot, underscore, HTTP and third-party patterns [1]. It does not establish authenticated browser readability by itself. |
| CORS | ZAP CORS posture, https://www.zaproxy.org/docs/alerts/200017/ | ZAP is free/open source; exact alert page does not state a separate licence. | Passive Recon while traffic passes through ZAP | Alert indicators | Detects dynamic ACAO without `Vary: Origin`, broad methods, and broad headers [13]. It is posture analysis, not a complete credentialed CORS proof. |
| CORS | Nuclei `cors-misconfig`, https://github.com/projectdiscovery/nuclei-templates/blob/main/http/vulnerabilities/generic/cors-misconfig.yaml | Template repository licence must be checked for the particular template; Nuclei engine is MIT [39]. Self-hosted CLI; no BYOK needed for ordinary templates. | `-u` or `-l` targets and `-t` template; supports URL, host, IP, CIDR, ASN, OpenAPI, Swagger, Burp and JSONL inputs [5] | Console and structured JSON/JSONL, Markdown, or SARIF are supported [203-204] | Reproducible HTTP assertions, but template coverage and false positives depend on template content and do not prove browser credential exposure. |
| Web messaging / PP | Burp DOM Invader, https://portswigger.net/burp/documentation/desktop/tools/dom-invader | Available in Burp Professional and Community Edition, in the built-in browser. Burp Community is free; Professional is commercial. | Enable web-message interception or prototype pollution in DOM Invader settings, reload, browse, inspect, and use Messages/DOM views [14][17] | DevTools/DOM view, severity/confidence indicators, modified/replayed messages, HTML PoC clipboard output, source/gadget/sink information [17] | Strong browser instrumentation for messages and client-side pollution. Features are disabled by default and can cause side effects; an origin/source access check does not prove secure validation [17]. |
| Web messaging | postMessage Detector Burp Extension, https://github.com/mariuszpoplawski/postMessage-Detector-Burp-Extension | Page says it is for Burp Professional and requires JPython; no licence is established by the cited page. | Install as a Burp extension; passively inspect HTTP history and responses | Burp Issues for potential risks | Detects message references in responses and attempts variable discovery, but the repository itself says important exploit automation was not implemented. Treat as auxiliary and unmaintained-risk tooling. |
| Web messaging | postMessage-tracker, https://github.com/fransr/postMessage-tracker | Repository licence not stated in the cited evidence; self-installed Chrome extension | Load extension and browse; tracks URL, domain, stack and listeners | Browser indicator/logs | Observation and inventory, not a vulnerability verdict. A second tracker, https://github.com/iliyadindar/postMessage-tracker, advertises origin, JSON data, timestamp, and direction. Verify code before use. |
| Static messaging | CodeQL `js/missing-origin-check`, https://codeql.github.com/codeql-query-help/javascript/js-missing-origin-check/ | Query repository MIT; CodeQL CLI/engine licensing is separate. Deployment may be local or GitHub-integrated subject to product terms. | Build a JavaScript/TypeScript database and run the security query suite | Path problems with severity, precision, and source locations [30] | Finds missing origin verification in message handlers. It cannot prove runtime exploitability, policy correctness, or authenticated data impact. |
| Static PP | CodeQL `js/prototype-pollution` and utility queries, https://codeql.github.com/codeql-query-help/javascript/js-prototype-pollution/ | Query source is public; exact engine/product terms remain separate. | Analyze source or authorized bundle | Path problems, warnings/errors, source paths | Finds unsafe recursive merge/assignment patterns and recommends safe dependencies or guards [27]. Dynamic sources and gadgets may be missed. |
| CSP | Google CSP Evaluator, https://csp-evaluator.withgoogle.com/ and https://github.com/google/csp-evaluator | Apache License 2.0 [37]; web UI is free; self-hostable core is public. No BYOK required. | Paste a policy into UI or integrate the core library | Policy warnings and bypass-oriented analysis | Reviews policy strength and subtle bypasses [11]. It evaluates policy text, not live endpoint consistency or XSS exploitability. |
| CSP | Google CSP Validator, https://github.com/google/CSP-Validator | Repository contains a licence file, but the exact licence was not established in the cited excerpt. | Local Python/Sublime-oriented validator according to repository files | Validation messages | Syntax/policy validation; not a live authenticated scanner. Licence should be verified before redistribution. |
| Headers/CSP | Mozilla HTTP Observatory, https://github.com/mozilla/http-observatory and CLI https://github.com/mozilla/http-observatory-cli | Public repositories and CLI; exact licence was not established in the cited excerpt. | Web service, CLI, or API; API documentation is public [130-133] | Scores and JSON-like API results | Broad HTTP security posture, useful for CSP and headers. It is not designed as a complete API-endpoint CORS or browser-message assessor. |
| Headers/CSP | ZAP CSP alert, https://www.zaproxy.org/docs/alerts/10038-1/ | ZAP free/open source [85-86]; page does not state a separate alert licence. | Passive or active ZAP scan | ZAP alert/report; report generation supports automation [199-200] | Flags CSP header not set. It can miss meta-policy nuance and does not prove effective XSS protection. |
| Header templates | Nuclei weak CSP, https://github.com/projectdiscovery/nuclei-templates/blob/main/http/misconfiguration/weak-csp-detect.yaml | Template repository terms apply; engine MIT [39] | Nuclei CLI and YAML template | Console/JSON/JSONL/Markdown/SARIF | Fast policy assertions. Coverage is template-specific and should be independently reviewed. |

A licence marked "not established" is deliberately not guessed. The university club should retain the repository commit and licence text before bundling any project into a distributable lab image.

## Manual Method and Detection Counterpart

The manual detection workflow should proceed in a controlled sequence.

| Step | Manual observation | Detection counterpart | Authorization |
|---|---|---|---|
| 1 | Build a public route and script inventory from ordinary browsing, browser network logs, and downloaded assets | URL collector, script parser, ZAP passive history, Nuclei input list | Pre-authorization if low-rate and public |
| 2 | Record response status, `Origin` behavior, ACAO, credentials, methods, headers, exposed headers, and `Vary` without reading protected data | CORScanner/Corsy/Nuclei/ZAP; compare raw exchanges | Passive pre-authorization; origin variation requires scope approval |
| 3 | For each cross-origin candidate, determine whether the browser would expose a synthetic response and whether credentials are involved | Authorized browser harness with two test accounts and synthetic data | Letter and accounts |
| 4 | Enumerate frames, popups, message listeners, sender/receiver origins, schemas, and sinks | DOM Invader, tracker extensions, CodeQL missing-origin query | Observation can be pre-auth; replay/modification requires letter |
| 5 | Trace URL/fragment/message/JSON keys into merges and inherited properties; then identify a gadget and sink | DOM Invader, CodeQL PP queries, local library review | Static local review pre-auth; live pollution proof requires letter |
| 6 | Collect CSP on initial, redirect, error, static, and sensitive responses; distinguish enforce from report-only and assess directives | CSP Evaluator, ZAP, Nuclei, Observatory | Header collection pre-auth; payload/enforcement checks require letter |
| 7 | Reproduce only the minimum finding with synthetic data, preserve raw evidence, and stop | Structured evidence collector and human review | Letter and accounts |

The detection counterpart is not merely "run a scanner." For CORS, it is a browser-readability assertion tied to an endpoint, origin, credential state, and response sensitivity. For postMessage, it is a source-to-sink trace tied to a sender and receiver. For prototype pollution, it is source-gadget-sink correlation. For CSP, it is policy parsing plus enforcement and application-context review.

## Target-Specific Priorities

The supplied architecture makes CORS the first priority because the campaign has no existing CORS brief and because Entra-backed applications commonly have a separation between browser-facing pages, identity redirects, APIs, and tenant or third-party origins. This is not evidence that MUJ has a vulnerable CORS policy. It is an inference about where an authorization-approved review is likely to deliver the most decision value.

The supplied MVC and jQuery facts support two separate workstreams. First, inspect public JavaScript for `fetch`, XHR, JSONP-like legacy patterns, `postMessage`, event listeners, URL parsing, deep merge, and DOM sinks. Second, determine whether the bundled libraries are actually loaded on the relevant page and whether their versions are exploitable in the deployed code path. A version string alone is not a vulnerability.

The supplied lack of HSTS and TLS 1.0 availability belong primarily to transport/configuration reporting, not to this browser-layer brief. They may affect risk prioritization, but they do not prove CORS, messaging, prototype pollution, or CSP exposure. Likewise, the YSOD, method policy, antiforgery cookie attribute, and `enc` oracle should be kept as separate campaign findings. They should not be used as payload carriers or bypass hypotheses in this workstream without explicit authorization.

The clean host-header and trust-bypass attempts reduce concern about those specific observations, but they do not answer whether a browser can read a cross-origin response. The campaign's unauthenticated status is particularly important: a negative CORS result on public pages cannot clear authenticated MVC/API routes. The two test accounts should be used to compare least-privilege roles, not to access real student data.

## No-Tool Gaps and Build Candidates

### No-tool gaps

| Gap | Why existing tools are insufficient | Required result |
|---|---|---|
| Credential-aware CORS proof | HTTP scanners can observe headers, but do not know whether a response contains sensitive data for a specific role or whether the real browser session exposes it | Role-scoped, synthetic-data browser assertion with raw evidence |
| Entra-aware origin graph | Generic scanners do not model three tenants, login redirects, issuer boundaries, cookie scope, token audience, or same-site behavior as one graph | Identity/origin inventory with tenant and audience labels |
| Message-to-CORS correlation | DOM tools observe messages, CORS tools observe HTTP; neither automatically joins a message carrying a token or URL to the resulting API response | Correlated browser trace with secrets redacted |
| Prototype-pollution runtime confidence | Static queries identify patterns; DOM Invader identifies sources and gadgets, but no universal tool proves application-specific impact without runtime interaction | Source-gadget-sink evidence and clean rollback |
| CSP route consistency | Header scanners sample URLs and may miss redirects, errors, authenticated routes, and dynamically inserted policies | Route matrix showing effective policy per response family |
| Version-to-reachability mapping | Dependency/version databases do not establish that a vulnerable function is loaded, reachable, and exploitable in MUJ's page flow | Bundle inventory, call path, and authorized runtime confirmation |
| Evidence and authorization chain | General tools do not bind each request to a scope-letter clause and test-account role | Signed evidence manifest and redacted reproducibility package |

### Build candidates

1. **Consent-gated browser harness.** Build a Playwright- or Chromium-based harness that records URL, frame, origin, request method, selected headers, response policy, message event metadata, and redacted payload hashes. It should default to public unauthenticated mode, require an explicit scope token for origin variation or authenticated mode, rate-limit itself, and refuse real-data collection.

2. **CORS policy differential engine.** Feed it a route list and a finite set of approved synthetic origins. Compare ACAO, ACAC, allowed methods, allowed headers, exposed headers, status, body classification, and `Vary`. The engine should distinguish a header anomaly from browser-readable credentialed data and output JSON plus an analyst-readable table.

3. **Message provenance recorder.** Instrument `postMessage`, message listeners, frame relationships, `event.origin`, `event.source`, and target origins. Emit a graph, not just a list: sender frame -> receiver frame -> data field -> sink/API call. It should mark origin validation as exact, allow-listed, pattern-based, missing, or unobserved.

4. **Prototype-pollution source-gadget-sink mapper.** Combine CodeQL-style static findings with browser observations of URL, fragment, JSON, and message sources. Require a controllable property and a benign canary before escalating a finding. Do not generate an exploit automatically against a live target.

5. **CSP route evaluator.** Parse enforcing and report-only policies, normalize directives, identify nonces/hashes and broad sources, and compare policies across route classes. Integrate browser violation reports only to a club-controlled collector during an authorized test.

6. **Evidence normalizer.** Convert CORScanner, Corsy, ZAP, Nuclei, Burp, CodeQL, CSP Evaluator, and Observatory results into a common schema: target route, timestamp, tool/version, authorization reference, request hash, response hash, finding type, confidence, sensitivity, and reproduction status. This addresses the current fragmentation without claiming that normalized findings are equivalent.

## Synthesis

The four classes differ in mechanism, evidence, and trade-off. CORS is primarily a response-policy and browser-readability problem; it is the most amenable to HTTP automation but requires authenticated context for impact. postMessage is a runtime trust-boundary problem; browser instrumentation is more valuable than a port scanner because the relevant evidence is frame, origin, source, data, and sink. Prototype pollution is a data-flow problem; source discovery is easier than proving a reachable gadget and meaningful sink. CSP is a policy and enforcement problem; evaluators can identify weak directives, but policy weakness alone does not establish an application exploit.

| Dimension | CORS | postMessage | Prototype pollution | CSP |
|---|---|---|---|---|
| Primary control | ACAO, credentials, preflight, Vary | Exact target and sender-origin validation | Safe key handling and merge behavior | Enforced resource policy |
| Best first tool | CORScanner/Corsy/ZAP/Nuclei | DOM Invader plus tracker | DOM Invader plus CodeQL | CSP Evaluator plus ZAP/Nuclei |
| Main false-positive source | Public endpoint or unreadable credential state | Listener with no sensitive sink | Source with no gadget | Weak-looking policy that still blocks the relevant path |
| Main evidence gap | Authenticated browser readability | Runtime source-to-sink consequence | Reachable gadget and sink | Effective enforcement on all route classes |
| Safe pre-auth work | Public headers and local scripts | Passive observation and source review | Local static analysis | Header/policy collection and evaluation |
| Authorized work | Origin variation and test accounts | Modified/replayed messages | Benign runtime canary | Controlled enforcement test |

The non-obvious tension is that automation is strongest where the target is least contextual. A CORS scanner can quickly find reflection but cannot know whether the response is a student record. A CSP evaluator can flag `unsafe-inline` but cannot know whether the application has a reachable injection. DOM Invader can generate a useful proof of concept but its own documentation warns that browser instrumentation can interfere with site behavior [14][17]. Therefore, the club should optimize for evidence quality, not the number of alerts.

The recommended sequence is: public inventory, local static review, passive tool baselining, signed-scope browser testing, two-account least-privilege comparison, minimum reproducibility, and remediation-oriented reporting. That sequence directly addresses the campaign's absent CORS brief while avoiding unauthorized access and avoiding conflation with the already measured server-side issues.

## VERDICT

**Finding status:** No client-side or browser-layer vulnerability is established. CORS, postMessage, prototype pollution, and CSP are currently **unassessed in the campaign**, not proven absent.

**Priority:** High for a dedicated authorized CORS review; medium-high for web messaging and CSP; medium for client-side prototype pollution pending the actual loaded bundle and route inventory.

**Confidence:** **High confidence** in the technique taxonomy, safety boundaries, and tool capability comparison because they are grounded in OWASP, MDN, WHATWG, PortSwigger, CodeQL, ZAP, Nuclei, Google, and Mozilla documentation. **Low confidence** in any target-specific exposure claim because no authenticated browser session, origin-variation result, message trace, source-gadget-sink proof, or effective CSP matrix was supplied.

**Decision:** Approve a signed, narrowly scoped work package. Permit public passive inventory and local analysis first. Require the letter and two test accounts before origin variation, credentialed requests, message replay or modification, runtime pollution checks, controlled CSP payloads, or any action that could expose or alter data. Report the result as a four-track evidence matrix, with CORS given first execution priority and all conclusions limited to the exact route, origin, account role, and response observed.

## References

1. *GitHub - s0md3v/Corsy: CORS Misconfiguration Scanner · GitHub*. https://github.com/s0md3v/Corsy
2. *nuclei-templates/http/vulnerabilities/generic/cors-misconfig.yaml at main · projectdiscovery/nuclei-templates · GitHub*. https://github.com/projectdiscovery/nuclei-templates/blob/main/http/vulnerabilities/generic/cors-misconfig.yaml
3. *Content Security Policy (CSP) - HTTP | MDN*. https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP
4. *GitHub - chenjj/CORScanner: 🎯 Fast CORS misconfiguration vulnerabilities scanner · GitHub*. https://github.com/chenjj/CORScanner
5. *Running Nuclei*. https://docs.projectdiscovery.io/opensource/nuclei/running
6. *GitHub - mozilla/http-observatory: Mozilla HTTP Observatory · GitHub*. https://github.com/mozilla/http-observatory
7. *WSTG - Latest | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/11-Client-side_Testing/11-Testing_Web_Messaging
8. *WSTG - Latest | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/12-Test_for_Content_Security_Policy
9. *GitHub - mariuszpoplawski/postMessage-Detector-Burp-Extension: Burp extension to detect postMessages - alert for potential issues · GitHub*. https://github.com/mariuszpoplawski/postMessage-Detector-Burp-Extension
10. *http-observatory/httpobs/docs/api.md at main · mozilla/http-observatory · GitHub*. https://github.com/mozilla/http-observatory/blob/master/httpobs/docs/api.md
11. *csp-evaluator.withgoogle.com*. https://csp-evaluator.withgoogle.com/
12. *GitHub - google/csp-evaluator · GitHub*. https://github.com/google/csp-evaluator
13. *ZAP – Passive Recon: CORS Posture Indicators*. https://www.zaproxy.org/docs/alerts/200017/
14. *Testing for client-side prototype pollution - PortSwigger*. https://portswigger.net/burp/documentation/desktop/tools/dom-invader/prototype-pollution
15. *ZAP – Content Security Policy (CSP) Header Not Set*. https://www.zaproxy.org/docs/alerts/10038-1/
16. *WSTG - Latest | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/11-Client-side_Testing/07-Testing_Cross_Origin_Resource_Sharing
17. *Testing for DOM XSS using web messages - PortSwigger*. https://portswigger.net/burp/documentation/desktop/tools/dom-invader/web-messages
18. *Testing for prototype pollution with DOM Invader - PortSwigger*. https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/input-validation/prototype-pollution
19. *GitHub - fransr/postMessage-tracker: A Chrome Extension to track postMessage usage (url, domain and stack) both by logging using CORS and also visually as an extension-icon · GitHub*. https://github.com/fransr/postMessage-tracker
20. *nuclei-templates/LICENSE.md at main · projectdiscovery/nuclei-templates · GitHub*. https://github.com/projectdiscovery/nuclei-templates/blob/main/LICENSE.md
21. *GitHub - projectdiscovery/nuclei: Nuclei is a fast, customizable vulnerability scanner powered by the global security community and built on a simple YAML-based DSL, enabling collaboration to tackle trending vulnerabilities on the internet. It helps you find vulnerabilities in your applications, APIs, networks, DNS, and cloud configurations. · GitHub*. https://github.com/projectdiscovery/nuclei
22. *ZAP – Report Generation*. https://www.zaproxy.org/docs/desktop/addons/report-generation/
23. *DOM Invader settings - PortSwigger*. https://portswigger.net/burp/documentation/desktop/tools/dom-invader/settings
24. *GitHub - google/CSP-Validator: CSP-Validator · GitHub*. https://github.com/google/CSP-Validator
25. *nuclei-templates/http/misconfiguration/weak-csp-detect.yaml at main · projectdiscovery/nuclei-templates · GitHub*. https://github.com/projectdiscovery/nuclei-templates/blob/main/http/misconfiguration/weak-csp-detect.yaml
26. *GitHub - BlackFan/client-side-prototype-pollution: Prototype Pollution and useful Script Gadgets · GitHub*. https://github.com/BlackFan/client-side-prototype-pollution
27. *codeql/javascript/ql/src/Security/CWE-915/PrototypePollutingFunction.ql at main · github/codeql · GitHub*. https://github.com/github/codeql/blob/main/javascript/ql/src/Security/CWE-915/PrototypePollutingFunction.ql
28. *DOM Invader - PortSwigger*. https://portswigger.net/burp/documentation/desktop/tools/dom-invader
29. *Prototype-polluting function — CodeQL query help  documentation*. https://codeql.github.com/codeql-query-help/javascript/js-prototype-pollution-utility/
30. *Missing origin verification in postMessage handler — CodeQL query help  documentation*. https://codeql.github.com/codeql-query-help/javascript/js-missing-origin-check/
31. *GitHub - d3ng03/PP-Auto-Detector: Team NodeBoB Prototype Pollution Auto Detection Tool in Node.js npm package · GitHub*. https://github.com/d3ng03/PP-Auto-Detector
32. *Prototype-polluting merge call — CodeQL query help  documentation*. https://codeql.github.com/codeql-query-help/javascript/js-prototype-pollution/
33. *GitHub - yeswehack/pp-finder: PP-finder Help you find gadget for prototype pollution exploitation · GitHub*. https://github.com/yeswehack/pp-finder
34. *codeql/javascript/ql/src/Security/CWE-020/MissingOriginCheck.ql at main · github/codeql · GitHub*. https://github.com/github/codeql/blob/main/javascript/ql/src/Security/CWE-020/MissingOriginCheck.ql
35. *Client-side prototype pollution vulnerabilities | Web Security Academy*. https://portswigger.net/web-security/prototype-pollution/client-side
36. *GitHub - mozilla/http-observatory-cli: The command line tool for the HTTP Observatory*. https://github.com/mozilla/http-observatory-cli
37. *csp-evaluator/LICENSE at master · google/csp-evaluator · GitHub*. https://github.com/google/csp-evaluator/blob/master/LICENSE
38. *Content-Security-Policy (CSP) header - HTTP | MDN*. https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy
39. *nuclei/LICENSE.md at main · projectdiscovery/nuclei · GitHub*. https://github.com/projectdiscovery/nuclei/blob/main/LICENSE.md
40. *Tutorial: Prepare a web application for authentication - Microsoft identity platform | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity-platform/scenario-web-app-sign-user-overview
41. *Microsoft identity platform and OAuth 2.0 authorization code flow - Microsoft identity platform | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow
42. *Window: postMessage() method - Web APIs | MDN*. https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage
43. *zaproxy/LICENSE at main · zaproxy/zaproxy · GitHub*. https://github.com/zaproxy/zaproxy/blob/main/LICENSE
44. *Cross-Origin Resource Sharing (CORS) - HTTP | MDN*. https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS
