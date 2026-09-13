# Authorization Assurance for the MUJ SLCM Portal

## Executive Summary

This report addresses authorization assurance for the MUJ SLCM portal without performing, proposing, or enabling unauthorized access. The supplied campaign record says the portal is reachable on HTTPS only, exposes thirteen API routes discovered from a public Flutter client, uses publicly predictable reference numbers, and has not yet been authenticated against. Those facts make authorization the most consequential untested control area, but they do not prove a vulnerability. The observations are treated as analyst-provided measurements, not independently verified public facts, because no public URL for the campaign record was supplied.

- **Primary Risk Surface**: Predictable identifiers make broken object-level authorization, or BOLA, a high-priority hypothesis because OWASP explicitly describes object-ID manipulation as the relevant attack pattern and notes that IDs may be sequential integers, UUIDs, or strings [3] (https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/). -> Build a two-account, read-only authorization matrix before any mutation test.
- **Authorization Is Broader Than IDOR**: OWASP's testing guide separates authorization-schema bypass, privilege escalation, direct-object references, and OAuth weaknesses [12] (http://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/README). -> Test route, method, field, tenant, workflow, and session context as separate dimensions.
- **Authentication Block Is a Valid Stop Condition**: The campaign has never authenticated and is marked BLOCKED-AUTH. -> Pre-authorization work should remain passive and public; replay, differential testing, and account-context comparisons require the signed scope letter and two test accounts.
- **Best Immediate Tooling**: ZAP Access Control Testing, Burp Autorize, and Burp AuthMatrix are the closest purpose-built tools. ZAP requires an access-rule model [5] (https://www.zaproxy.org/docs/desktop/addons/access-control-testing/); Autorize replays privileged traffic in lower-privilege or unauthenticated contexts [9] (https://github.com/PortSwigger/autorize); AuthMatrix evaluates a role/request matrix and provides color-coded results [4] (https://github.com/PortSwigger/auth-matrix). -> Use one as the primary detector and another for regression confirmation.
- **Automation Has a Schema Dependency**: RESTler and Schemathesis can generate stateful or property-based API activity, but both work best with an OpenAPI or GraphQL description [11] (https://github.com/microsoft/restler-fuzzer) [7] (https://github.com/schemathesis/schemathesis). -> Treat the Flutter client as an inventory source, not as proof of a complete or safe schema.
- **The Main Gap Is Business Authorization**: General scanners can compare responses, but they do not know whether a student may view another student's record, whether an approver may execute a later workflow step, or whether a field is writable for one role but not another. -> Build a domain-specific oracle and an auditable access-control matrix.
- **Configuration Findings Are Not Authorization Findings**: The supplied verbose error pages, missing HSTS, legacy TLS support, antiforgery-cookie flag, and method behavior matter, but they do not demonstrate BOLA or broken function-level authorization. -> Keep them as separate hardening workstreams.
- **Confidence**: High for the methodology and tool capability claims, medium for prioritization because the supplied portal facts are not independently linked, and low for any claim that MUJ SLCM is actually vulnerable until authorized tests produce evidence. -> Do not publish a vulnerability conclusion before controlled differential testing.

## Scope, Safety, and Evidence Boundary

The portal-specific facts in the brief are reported as measured on 2026-09-13: HTTPS on port 443, IIS 10, ASP.NET MVC 5.3, .NET Framework 4.7.4136.0, jQuery versions, Azure AS8075, Microsoft 365 identity, three Entra tenants, no attributable edge control, no HSTS, TLS 1.0 through 1.3 offered, verbose YSOD behavior, antiforgery behavior, trace and ELMAH responses, method responses, the three-stage `enc` oracle, and clean host-header and trust-bypass attempts. Because the brief supplies no public URL for those measurements, they are labeled here as **campaign-record facts** rather than independently citable public claims.

The safe pre-authorization boundary is narrow. Public-information research, source-code and package analysis of a publicly distributed Flutter client, passive documentation of route names already disclosed by that client, local construction of an access-control matrix, review of public identity configuration documentation, and testing against a local lab or a deliberately provided mock service are safe candidates, subject to applicable law and institutional policy. Even public-client analysis should avoid extracting or using secrets, tokens, personal data, or undocumented credentials.

The signed scope letter and two test accounts are required before sending authenticated requests to the portal, replaying a request under a second identity, changing an object reference, probing role boundaries, exercising a mutation, testing workflow ordering, comparing tenant contexts, or running automated concurrency. The letter should identify hostnames, routes, permitted methods, account roles, time windows, rate limits, data-handling rules, emergency contacts, and whether production data is excluded. A tool's free license does not make target activity authorized.

The report does not provide a private chain of thought. The decision reasoning is summarized transparently: identify the authorization dimensions, map each dimension to an observable security property, select tools that can replay or compare authorized contexts, identify what requires business knowledge, and reserve all state-changing or authenticated activity for written authorization. That summary is sufficient for auditability without exposing hidden internal deliberation.

## Technique Universe Beyond the Planned IDOR Sweep

| Technique family | Security question | Safe evidence target | MUJ relevance | Detection oracle |
|---|---|---|---|---|
| Object-level authorization, BOLA/IDOR | Does identity A receive or change object B? | A controlled object created for account B | High, because reference numbers are reported predictable | Same authorized identity, object ownership, status code, body, and side effect must agree |
| Function-level authorization, BFLA | Can a lower role invoke an operation reserved for a higher role? | Route and method inventory from permitted traffic | High, because thirteen routes are known but role coverage is unknown | Expected deny response and no side effect for unauthorized role |
| Object-property authorization, BOPLA | Can a user read or write fields outside their permission set? | Field-level allow/deny map | High for profile, status, marks, approvals, or identity fields if present | Compare returned and persisted fields against role policy |
| Vertical escalation | Can student or ordinary staff perform administrator or approver functions? | Two approved role accounts | High if the application has multiple university roles | Role A request must not produce role B capability |
| Horizontal escalation | Can one peer access another peer's object? | Two same-role test accounts with isolated fixtures | Highest direct consequence of predictable references | Account A and B must obtain only their own fixtures |
| Tenant isolation | Can an identity or token cross one of the three Entra tenant contexts? | Explicitly separated tenant test identities | High but unproven; tenant count alone is not a vulnerability | Tenant claim, issuer, audience, and server-side data scope must align |
| Workflow authorization | Can a caller skip, repeat, or reorder approval steps? | State-machine fixture and permitted sequence | High for student-life workflows | Every transition requires server-side state and role checks |
| Method and verb authorization | Is authorization applied consistently to GET, POST, PUT, DELETE, and alternate verbs? | Authorized route/method pairs | Relevant because campaign-record method policy is GET-only | Denied methods do not fall through to another handler or alter state |
| Context and session binding | Are permissions bound to current identity, tenant, audience, and session? | Fresh test sessions and rotated tokens | Relevant to Microsoft identity integration | Changing context must invalidate or deny the request |
| Client-side enforcement | Does the server enforce rules rather than merely hide UI controls? | Direct request from an approved test client | High for a public Flutter client | Server result remains denied when UI restrictions are bypassed |
| Token and claim authorization | Are issuer, audience, expiry, signature, role, and tenant claims enforced? | Tokens issued to approved test accounts | Relevant to Entra and Microsoft 365 identity | Altered, expired, wrong-audience, or wrong-tenant tokens are rejected |
| Resource exhaustion as authorization abuse | Can one identity batch or enumerate sensitive objects? | Rate-limited, approved small sample | Secondary, not a license to brute force | Rate limit, uniform denial, and no sensitive enumeration |

OWASP ASVS frames the baseline as valid credentials, well-defined roles and privileges, and protection of role and permission metadata from replay or tampering [8] (https://github.com/OWASP/ASVS/blob/master/4.0/en/0x12-V4-Access-Control.md). OWASP's GraphQL guidance expresses the same server-side principle: the requester must be authorized to view or mutate the requested data [1] (https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html). The inference for this MVC application is that authorization must be tested at the server boundary for every route and relevant field, not inferred from Flutter navigation or visible controls.

The key distinction is between a **security property** and a **test payload**. The property is, for example, that account A cannot read account B's record. The payload is an authorized, minimal request against a synthetic fixture. This distinction keeps the club's work educational and non-destructive.

## Tool Inventory and Detection Counterparts

| Tool | Exact URL | License | Free, self-host, or BYOK | How it is driven | Output and authorization fit |
|---|---|---|---|---|---|
| OWASP ZAP Access Control Testing | https://www.zaproxy.org/docs/desktop/addons/access-control-testing/ | ZAP core is Apache License 2.0 [13] (https://github.com/zaproxy/zaproxy/blob/main/LICENSE) | Free and self-hosted | Configure users or contexts, define access rules, capture permitted traffic, then run the add-on's testing procedure | Access-rule test results in the ZAP UI/reporting model; strong for role/request comparisons, but requires an accurate rule model [5] |
| Burp Autorize | https://portswigger.net/bappstore/f9bbac8c4acf4aefa4d7dc92a991af2f | Extension source is publicly available; verify repository terms before redistribution | Runs inside Burp; Community is free, Professional is commercial; no external BYOK requirement | Browse with a higher-privilege approved session; Autorize repeats traffic with a low-privilege or unauthenticated context | Per-request authorization indicators and response comparisons; it passively monitors high-privilege traffic and replays it [9] |
| Burp AuthMatrix | https://portswigger.net/bappstore/30d8ee9f40c041b0bfec67441aad158e | Repository has a license file; confirm the current license before institutional packaging [14] (https://github.com/PortSwigger/auth-matrix/blob/master/LICENSE) | Extension is free; Burp host edition may be free or commercial | Define users, roles, and requests in an access-control matrix, then run combinations | Color-coded authorization results and save/load configuration for regression [4] |
| Auth Analyzer | https://portswigger.net/bappstore/7db49799266c4f85866f54d9eab82c89 | Repository license should be checked before redistribution; public repository and disclaimer are at https://github.com/GitHubNull/my_auth_analyzer | Burp extension; deployment is local; licensing and maintenance should be treated as unverified until reviewed | Navigate with a high-privilege user; configure non-privileged sessions and parameter extraction/replacement | Repeated requests and response comparison intended to flag authorization bypasses [15] (https://portswigger.net/bappstore/7db49799266f54d9eab82c89) |
| RESTler | https://github.com/microsoft/restler-fuzzer | Repository provides a license file [16] (https://github.com/microsoft/restler-fuzzer/blob/main/LICENSE); confirm exact terms for the selected release | Self-hosted; authentication is supplied by a separate token-generation program [17] (https://github.com/microsoft/restler-fuzzer/blob/main/docs/user-guide/Authentication.md) | Supply an OpenAPI specification, compile dependencies, provide an approved authentication helper, and run bounded stateful tests | Generated request sequences and logs for security/reliability bugs; it analyzes the specification and executes sequences [11] |
| Schemathesis | https://github.com/schemathesis/schemathesis | MIT [18] (https://schemathesis.readthedocs.io/) | Free and self-hosted; cloud options are optional; credentials are supplied by the tester | Supply OpenAPI or GraphQL schema, configure approved authentication, generate property-based cases, and run against a test target | Test reports and reproducible failing cases; it chains operations into realistic workflows [7] and deliberately removes or alters auth in some security checks [19] (https://schemathesis.readthedocs.io/en/latest/guides/auth/) |
| mitmproxy | https://docs.mitmproxy.org/stable/addons/overview/ | License file is public; official repository describes the tool [20] (https://github.com/mitmproxy/mitmproxy) | Free and self-hosted | Run as an intercepting proxy and load a local addon; addons implement event handlers such as request handling [2] | Flow logs, modified/replayed requests, and custom JSON/CSV output produced by the addon; useful as a programmable harness, not an authorization oracle by itself |
| Nuclei | https://github.com/projectdiscovery/nuclei | MIT [21] (https://github.com/projectdiscovery/nuclei/blob/dev/LICENSE.md) | Free and self-hosted; optional ProjectDiscovery cloud services; templates can use approved credentials | Write a narrowly scoped YAML template with safe matchers and run against an authorized host | Structured findings, commonly JSON, JSONL, or text; excellent for deterministic exposure checks, weak for business-specific role matrices [22] |
| Flutter client and local proxy capture | Public client source or distribution URL must be recorded by the club; no URL was supplied in the brief | Depends on the client repository and dependencies | Local analysis; no portal execution required for static review | Extract route strings, request models, serializers, and claim names without using credentials | Route inventory, parameter map, and evidence table; discovery only, not proof of authorization behavior |

The term “every tool” needs a scope qualification. No finite public list can contain every script, commercial product, fork, or custom harness that can send HTTP. The table therefore covers the publicly documented, materially relevant tools located for this report and distinguishes purpose-built authorization detectors from generic programmable clients. A tool not listed is not necessarily ineffective; it is simply outside the documented set reviewed here.

ZAP, Autorize, and AuthMatrix are detection counterparts rather than substitutes for policy analysis. ZAP's access rules describe what each user is supposed to access [5]. Autorize compares a high-privilege request with lower-context replay [9]. AuthMatrix makes the role/request combinations explicit and preserves them for regression [4]. The recommended detection design is to use at least two independent signals: response semantics and state verification. A `403` is useful, but it is not enough if an unauthorized request still changes a record.

## Manual Method When Automation Is Insufficient

Manual testing is required where the oracle depends on university business rules. It should be conducted only after the scope letter and two test accounts are available. The following is a controlled method, not an instruction to access the live portal without authorization.

First, create a **policy register**. For each of the thirteen already-known routes, record intended audience, issuer and tenant, role, object type, allowed methods, readable fields, writable fields, expected state transitions, sensitivity, and whether the route is read-only. Mark unknown rather than guessing. The public Flutter client can populate route and model fields, but only an application owner can confirm intended permissions.

Second, create two synthetic fixtures owned by the two approved accounts. Use non-production records if the owner can provide them. Record a fixture identifier, owner, tenant, initial state, and permitted operations. Do not enumerate live reference numbers. The supplied predictability observation is a prioritization clue, not permission to scan.

Third, capture one benign baseline request per route as account A, preserving method, URL, headers, body, cookies, token claims, response status, response length, content type, and a normalized body hash. Repeat the same operation as account B only where the policy register says it is permitted. The comparison should account for dynamic fields such as timestamps, correlation IDs, and anti-forgery values.

Fourth, perform a **matrix comparison**. For each route, compare A's fixture, B's fixture, an object neither should access, and the unauthenticated state if explicitly in scope. For each role, compare read, create, update, approve, reject, delete, export, and administrative operations only if those actions exist and are permitted for testing. Use one request at a time, low rate, and a stop condition after any unexpected data exposure or state change.

Fifth, test field boundaries. If a permitted update changes a profile or workflow record, change one approved field at a time and leave all other values constant. Confirm that disallowed fields are rejected or ignored server-side and that the persisted record remains unchanged. A client-side field omission is not evidence of server-side enforcement.

Sixth, test workflow state. Build a state table such as draft, submitted, reviewed, approved, and closed only if those states are part of the application. Attempt only documented, approved transitions using synthetic records. The expected result is not merely an error response: the record must remain in its original state and no notification or downstream action should occur.

Seventh, verify token context. Record issuer, audience, tenant, role claim, expiry, and session identifiers from approved tokens without publishing token contents. Microsoft Entra app roles can be assigned to users or groups and emitted in a `roles` claim [6] (https://learn.microsoft.com/en-us/entra/identity-platform/howto-add-app-roles-in-apps). The safe test is to compare owner-provided identities and server behavior, not to forge or tamper with tokens.

Finally, reproduce every candidate finding. A finding needs a request identifier, account role, fixture, expected policy, observed status and body classification, state-before/state-after evidence, timestamp, and remediation recommendation. Redact personal data and secrets. A response difference alone is a lead; an authorization finding requires a demonstrated policy violation or a strong owner-confirmed mismatch.

## Pre-Authorization Versus Authorized Activities

| Activity | Pre-authorization status | Why |
|---|---|---|
| Review OWASP, ASVS, Microsoft identity, and tool documentation | Safe | It does not contact the portal |
| Static review of publicly distributed Flutter code | Generally safe if lawfully obtained | Discovery only; do not use secrets or personal data |
| Build a route, role, field, and workflow spreadsheet | Safe | Local planning artifact |
| Configure ZAP, Burp, mitmproxy, RESTler, Schemathesis, or Nuclei against localhost | Safe | Use a mock or lab target |
| Passive review of already published pages and public metadata | Usually safe, subject to policy | No authenticated or state-changing activity |
| Send unauthenticated requests to the portal | Not automatically safe | Written authorization should define even reconnaissance boundaries |
| Replay a captured request with another session | Requires scope letter and two accounts | It tests authorization directly |
| Change object references or fields | Requires scope letter, synthetic fixtures, and explicit permission | It may expose data or alter state |
| Test role, tenant, workflow, or method boundaries | Requires scope letter and approved accounts | It exercises protected behavior |
| Run automated fuzzing, concurrency, or stateful sequences | Requires explicit rate and route authorization | Availability and data-integrity risk |
| Publish raw requests, tokens, IDs, or personal data | Prohibited unless explicitly approved and redacted | Privacy and credential risk |

## No-Tool Gaps

| Gap | Why the listed tools do not solve it | Required evidence or owner input |
|---|---|---|
| Correct business policy | Tools replay requests but do not know whether a student should see a particular academic object | Signed route-role-object policy |
| Field-level semantics | Response comparison cannot tell whether a field is intentionally public, read-only, or privileged | Field classification and write policy |
| Tenant meaning | A token issuer or role claim does not by itself define data partitioning | Tenant mapping, expected issuer/audience, and test fixtures |
| Workflow legitimacy | Stateful fuzzers can generate sequences but cannot infer which transitions are institutionally valid | State diagram and allowed transition matrix |
| Side effects | A status response may miss email, approval, audit, or downstream changes | Before/after database or application-owner verification |
| Legacy MVC behavior | Generic API tooling may not model antiforgery, MVC forms, redirects, custom error pages, or unusual `enc` processing correctly | Authorized adapter and normalized response parser |
| Flutter serialization | The client may transform identifiers, encrypt parameters, or derive headers in code that a generic OpenAPI tool does not understand | Local static analysis and owner-provided test fixtures |
| Entra multi-tenant policy | Tools can send tokens, but cannot decide whether three tenants are intentional or accidentally trusted | Identity architecture diagram and test accounts |
| Negative-result confidence | A blocked unauthenticated campaign cannot establish that authenticated authorization is sound | Authorized role matrix execution |
| Safe automation | Tools may follow links or generate volume beyond the letter's limits | Rate-limited runner with allowlist and kill switch |

The most important gap is the authorization oracle. A generic tool can report “response changed” or “status differs.” It cannot reliably distinguish an expected difference from a breach. This is why a small, owner-approved policy register is more valuable than a large unauthenticated scan.

## Build Candidates

| Candidate | Purpose | Minimum design | Priority |
|---|---|---|---|
| Authorization Matrix Runner | Execute approved route-role-object combinations | CSV/YAML policy, two session providers, request allowlist, rate limiter, response normalizer, JSON and CSV output | P0 |
| MVC/Flutter Request Adapter | Make the harness understand client serialization and antiforgery without bypassing controls | Pluggable request builder, local-only key/parameter handling, no secret persistence, fixture IDs | P0 |
| Business Authorization Oracle | Convert policy into pass/fail decisions | Status plus normalized body plus side-effect callback plus field diff | P0 |
| Tenant and Claim Guard | Detect wrong issuer, audience, tenant, role, or expiry acceptance | Read-only token metadata parser, approved identities, redacted logs | P1 |
| Workflow State Machine Checker | Validate allowed and forbidden transitions | Explicit state graph, transition fixtures, idempotency and rollback checks | P1 |
| Regression Evidence Packager | Make results repeatable for a university club | Immutable test manifest, hashes, timestamps, redaction, HTML/JSON/CSV summaries | P1 |
| Safe Nuclei/ZAP Template Set | Detect static or deterministic exposure patterns | Strict host and route allowlists, no destructive payloads, JSON output | P2 |

The preferred build sequence is P0 matrix runner, P0 request adapter, and P0 oracle. RESTler and Schemathesis should be added only after an approved schema or a carefully constructed local specification exists. RESTler's documented model is an OpenAPI-driven stateful fuzzer [11], and Schemathesis generates schema-derived inputs and chains operations [7]; neither should be pointed at a production portal merely because a route list exists.

The runner should fail closed. Unknown route, unknown role, missing fixture, missing scope approval, or missing rate limit should result in “not run,” not an attempted request. The output should include `policy_id`, `route_id`, `role`, `fixture_id`, `expected`, `observed`, `state_before`, `state_after`, `evidence_hash`, and `review_status`. This structure supports teaching, peer review, and remediation without distributing sensitive responses.

## Interpretation of the Existing Campaign Findings

The supplied campaign record shows useful reconnaissance discipline: the campaign remained unauthenticated, destructive testing was not performed, host and forwarding-header bypass attempts were clean, and the aggressive phase is gated. Those are process strengths. They also explain why the principal authorization questions remain unanswered.

The verbose YSOD and differential `enc` responses may reveal error-handling or input-validation weaknesses, but they are not evidence that one user can access another user's object. The GET-only observation may indicate routing or method policy, but it does not show that function-level authorization is correct. The antiforgery cookie's missing Secure flag is a session and transport-hardening issue, while MVC antiforgery enforcement is a positive observation for the tested path; neither establishes role authorization. These are inferences from the supplied measurements and should be reported separately from authorization results.

The public Flutter route list is valuable for coverage. It can identify request names, parameters, serializers, and likely object references. It cannot establish the server's intended policy, and it may omit routes, administrative paths, or server-side workflow behavior. The appropriate next step is not broad enumeration; it is owner-confirmed route classification followed by two-account differential tests under the letter.

## Synthesis

Across the techniques, tools, and evidence boundary, three tensions matter. First, breadth versus safety: RESTler and Schemathesis can generate workflows, but a small explicit matrix is safer and more meaningful for a blocked-auth campaign. Second, automation versus semantics: ZAP, Autorize, and AuthMatrix detect response and access differences, while only the university owner can define whether the difference violates policy. Third, discovery versus proof: public Flutter routes and predictable references justify priority, but only authorized cross-account and cross-role evidence can establish BOLA or BFLA.

| Dimension | Manual matrix | ZAP Access Control | Burp Autorize/AuthMatrix | RESTler/Schemathesis |
|---|---|---|---|---|
| Primary strength | Business-policy accuracy | Reusable access rules | Fast differential replay and role matrix | Stateful or property-based generation |
| Main input | Owner policy and fixtures | Access rules and captured users | Sessions, roles, and requests | OpenAPI or GraphQL schema |
| Best MUJ use | Field, tenant, and workflow authorization | Regression of known route-role rules | First authorized pass over thirteen routes | Later bounded coverage expansion |
| Main trade-off | Labor intensive | Requires correct model | Can produce false positives without side-effect checks | Schema and safety dependency |
| Pre-authorization value | Planning only | Local lab only | Local lab only | Local lab only |

The non-obvious conclusion is that BLOCKED-AUTH is not merely a limitation; it is a control boundary. It prevents the club from converting a strong prioritization hypothesis into an unauthorized experiment. The highest-value deliverable before approval is therefore a test-ready evidence pack: route inventory, policy questions, fixtures plan, tool configuration, redaction scheme, stop conditions, and acceptance criteria.

## VERDICT

**Verdict: Authorization assurance is currently unproven, not demonstrably vulnerable.** Confidence is **high** that BOLA, BFLA, BOPLA, role escalation, tenant isolation, workflow authorization, method authorization, and token-context enforcement are the correct technique families to cover. Confidence is **high** in the documented capabilities of ZAP Access Control Testing, Autorize, AuthMatrix, RESTler, Schemathesis, and mitmproxy, based on their cited documentation. Confidence is **medium** in the prioritization for MUJ SLCM because the portal measurements and Flutter-client observations are supplied campaign facts without public URLs in the brief. Confidence is **low** for any finding about the portal's actual authorization behavior because no authenticated test has occurred.

The club may proceed now with public-source research, static client analysis, local tool setup, policy and matrix design, and mock-target testing. It must not replay authenticated requests, change identifiers or fields, compare user or tenant contexts, test protected workflow transitions, or run automated traffic against the portal until the signed scope letter, two test accounts, synthetic fixtures, route allowlist, rate limits, and emergency contact are in place. After authorization, use a fail-closed matrix runner plus one purpose-built detector, verify side effects, and report only reproducible, redacted, owner-confirmed policy violations.

## References

1. *GraphQL - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html
2. *Addons - mitmproxy*. https://docs.mitmproxy.org/stable/addons/overview/
3. *API1:2023 Broken Object Level Authorization - OWASP API ...*. https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/
4. *GitHub - PortSwigger/auth-matrix: AuthMatrix is a Burp Suite ...*. https://github.com/PortSwigger/auth-matrix
5. *Access Control Testing - ZAP*. https://www.zaproxy.org/docs/desktop/addons/access-control-testing/
6. *Add app roles and get them from a token - Microsoft identity ...*. https://learn.microsoft.com/en-us/entra/identity-platform/howto-add-app-roles-in-apps
7. *GitHub - schemathesis/schemathesis: Catch API bugs before ...*. https://github.com/schemathesis/schemathesis
8. *ASVS/4.0/en/0x12-V4-Access-Control.md at master · OWASP/ASVS*. https://github.com/OWASP/ASVS/blob/master/4.0/en/0x12-V4-Access-Control.md
9. *GitHub - PortSwigger/autorize: Automatic authorization ...*. https://github.com/PortSwigger/autorize
10. *WSTG - Latest - OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/03-Testing_for_Privilege_Escalation
11. *GitHub - microsoft/restler-fuzzer: RESTler is the first ...*. https://github.com/microsoft/restler-fuzzer
12. *WSTG - Latest | OWASP Foundation*. http://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/README
13. *zaproxy/LICENSE at main - GitHub*. https://github.com/zaproxy/zaproxy/blob/main/LICENSE
14. *auth-matrix/LICENSE at master · PortSwigger/auth-matrix · GitHub*. https://github.com/PortSwigger/auth-matrix/blob/master/LICENSE
15. *Auth Analyzer - PortSwigger*. https://portswigger.net/bappstore/7db49799266c4f85866f54d9eab82c89
16. *restler-fuzzer/LICENSE at main · microsoft/restler-fuzzer*. https://github.com/microsoft/restler-fuzzer/blob/main/LICENSE
17. *restler-fuzzer/docs/user-guide/Authentication.md at ... - GitHub*. https://github.com/microsoft/restler-fuzzer/blob/main/docs/user-guide/Authentication.md
18. *Schemathesis*. https://schemathesis.readthedocs.io/
19. *API Authentication - Schemathesis*. https://schemathesis.readthedocs.io/en/latest/guides/auth/
20. *mitmproxy/LICENSE at main - GitHub*. https://github.com/mitmproxy/mitmproxy/blob/main/LICENSE
21. *nuclei/LICENSE.md at dev · projectdiscovery/nuclei · GitHub*. https://github.com/projectdiscovery/nuclei/blob/dev/LICENSE.md
22. *GitHub - projectdiscovery/nuclei: Nuclei is a fast ...*. https://github.com/projectdiscovery/nuclei
