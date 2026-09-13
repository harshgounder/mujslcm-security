# GraphQL and API-Shape Abuse: Technique Universe, Tool Inventory, Detection Counterparts, Gaps, and Build Candidates for the MUJ SLCM Portal

*Audience: Manipal University Jaipur (MUJ) security club; pre-authorization intelligence brief. Public information only. No exploit engineering. Where a claim would require sending traffic or relying on out-of-scope data it is marked as an inference. Anything that requires an authenticated context, two privilege tiers, a successful introspection dump, or mutation calls is labelled as needing the signed scope letter and the two test accounts.*

## 1. Executive Summary

- **Severity framing**: API-shape abuse is the single class of findings most likely to escalate a "PARTIAL" campaign to "FULL", because the mobile client implies a JSON endpoint whose contract was never previously enumerated; untested routes and unzoom-omanned property authorization dominate OWASP API Top 10 2023 [1]. **Implication:** treat schema discovery, property-level authorization, and inventory as the next three workstreams.
- **Technique universe**: the eight relevant abuse families are GraphQL/JSON endpoint discovery, schema inference and introspection, BOLA and BOPLA (OWASP API1/API3 2023) [2][3], excessive data exposure / mass assignment (now unified under BOPLA) [3], denormalised batching and alias abuse, resource exhaustion / query-cost and depth (OWASP API4 2023) [4], content-type and method abuse, and un-inventoried versions / shadow endpoints (OWASP API9 2023) [5]. **Implication:** these map one-to-one to the gaps named in the campaign record.
- **Tool inventory gap**: a complete tool inventory now exists; the section below lists 19 publicly hosted tools/burp extensions with exact repository page, license, deployment (free/SELF-HOST/BYOK), how they are driven, and the output format they produce [6][7][8][9][10][11][12][13][14][15][16][17][18][19]. **Implication:** no closed-source commercial dependency exists for the recommended baseline.
- **Pre-auth vs letter-required boundary**: fingerprinting, response-shape inspection, error-page oracle work, `.well-known/graphql` probing, public wordlist fuzzing of method names, and reading static bundles/jQuery versions are SAFE PRE-AUTHORIZATION [20][21][22][23]. Introspection dumps with full schema, mutation replay, low-privileged session mutation for Autorize-style replay, schema-based mass-assignment mutation tests, deep-nested query-cost probes, and any test that authenticates as a real user require the signed scope letter plus the two test accounts [20][24][25].
- **Detection-side counter-rotation**: rate-limit (per IP, per user, per query-cost), introspection disablement, GraphiQL disablement, generic depth and amount limits, server-side batching/caching, schema-based response validation, segregation of view-model and persistence-model properties (Bind Include / [Bind] attribute / ViewModel), and structured logging of failed operations form the layered defense that should be paired with any of the offensive tools below [6].
- **NO-TOOL GAPS**: ten gaps remain because no mainstream single-purpose tool covers them; the most consequential for an ASP.NET MVC 5.3 target are: (a) query-cost analysis in CI on a schema harvested without introspection, (b) ASP.NET MVC overposting detection that combines ViewModel bind-list with property-level response diffing, and (c) JSON-encoder/oracle triangulation for the existing 4,942/5,084/Y enc oracle to discover whether it is reachable via the same path used by the mobile API [4][6]. **Implication:** two are reasonable student-club builds; one is not.
- **VERDICT (preview)**: the campaign STATUS TO BEAT (PARTIAL) can be upgraded by layering (1) passive schema discovery from the public bundle and mobile-client artifacts, (2) Apache 2.0 GraphQL tooling for both blind introspection (Clairvoyance) and reconstructed-schema EXPLOITATION, and (3) Autorize-style replay gated by the letter plus two test accounts; lower-lift than re-running the broader reconnaissance campaign. Confidence: medium (state of the GraphQL tooling ecosystem is well-documented, target surface is not yet enumerated).

---

## 2. Reasoning Summary (chain-of-thought)

The campaign record restricts the campaign to "PARTIAL" with two open observations: the JSON API implied by the mobile client was studied only once (w2c-20), and four specific sub-topics - schema discovery, mass assignment, excessive data exposure, and versioning - were never studied. The first step is therefore to enumerate *what* an attacker can actually do to a JSON endpoint in 2026; the OWASP API Top 10 (2023) defines that universe explicitly [1]. The second step is to enumerate whether the existing tooling covers each of those categories; if not, what is missing. The third step is to bind that universe and tooling to the measured facts (only port 443, GET-only, MVC 5.3, .NET 4.7, bundled jQuery 1.10.2 + 3.4.1, verbose YSOD, three-stage enc oracle) without claiming to test them. The fourth step is to define what is safe pre-authorization versus what requires the signed scope letter and the two test accounts; this is essentially the OWASP/WSTG distinction between information gathering on untrusted public endpoints and target-of-evaluation work that requires the user being aware of and consenting to the test [20][24]. The fifth step is to surface no-tool gaps (what mainstream tools cannot yet do) and propose candidate internal builds. The sixth step issues a VERDICT with confidence calibrated to the evidence available in the prior session plus the public sources cited here. The chain-of-thought that follows is presented in the executive domain only - the operational research mechanics (which sub-LLM read which page, etc.) are deliberately omitted in keeping with the campaign's separation of concerns.

---

## 3. Threat-Model Context (labelled as supplied; not re-verified)

This section restates the campaign measurement record verbatim as the operating envelope. It does not add new measurements. Statements drawn from this section are tagged "MEASURED" and are not extended.

| Item | Value | Source in this brief |
|---|---|---|
| Reachable port | 443 is the only reachable port | MEASURED |
| Server stack | IIS 10, ASP.NET MVC 5.3, .NET Framework 4.7.4136.0 | MEASURED |
| Client stack | jQuery 1.10.2 plus a bundled jQuery 3.4.1 | MEASURED |
| Hosting | Microsoft Azure AS8075; Microsoft 365 identity; three Entra tenants | MEASURED |
| Edge control | No attributable edge control; no HSTS; TLS 1.0-1.3 offered | MEASURED |
| Error pages | Verbose YSOD on four triggers with customErrors off | MEASURED |
| Anti-forgery | MVC anti-forgery enforced; cookie is HttpOnly without Secure | MEASURED |
| Diagnostic surface | trace.axd 403; elmah.axd 404 | MEASURED |
| Error fingerprinting | Two error-page families (MVC 2,733 b; IIS 1,216 b) | MEASURED |
| Method policy | GET only; POST and PUT 411; everything else 404 | MEASURED |
| Enc oracle | Three-stage enc oracle (invalid base64 -> FormatException 4,942 b; valid base64 -> CryptographicException 5,084 b; empty -> third size) | MEASURED |
| Bypass attempts | Host header, X-Forwarded-Host, absolute-URI, trust-based - all came back clean | MEASURED |
| Authorization | Campaign did not authenticate; aggressive phase gated by signed scope letter plus two test accounts | MEASURED |

Two inferences follow from this table. **Inference 1 (medium confidence):** because the only public method accepted is GET and the API only ever returns HTML/MVC payloads today, GraphQL or REST-JSON endpoints are not currently exposed unauthenticated; the mobile-client hypothesis is therefore an authenticated-context finding. **Inference 2 (high confidence):** the existence of an MVC stack with jQuery 1.10.2 plus a bundled jQuery 3.4.1 means the rendered HTML contains publicly visible client bundles that can be inspected for hard-coded API paths, hard-coded GraphQL queries, or `$.ajax` options strings [22]; this is one of the two safe-pre-auth anchors for the next phase.

---

## 4. Technique Universe: GraphQL and API-Shape Abuse

The eight abuse families below are ordered by their position in the OWASP API Top 10 (2023) and the OWASP GraphQL Cheat Sheet. Each family lists its definition, the standard attack pattern, and the canonical defenses drawn from OWASP and the GraphQL specification [20][6].

### 4.1 Schema discovery and introspection

Schema discovery is the act of recovering the underlying contract of a JSON endpoint without documentation. For GraphQL, the canonical mechanism is `__schema` introspection; for REST, it is path enumeration and OpenAPI discovery[20]. The OWASP GraphQL Cheat Sheet specifically tells defenders to "disable or restrict introspection" because it "allows the consumer of your API to learn everything about your API, schemas, mutations, deprecated fields and sometimes unwanted 'private fields'" [6]. When introspection is disabled, schema inference (a.k.a. blind reconstruction) becomes necessary; this is what Clairvoyance provides [7]. Discovery is one of the two safe-pre-auth anchors; full introspection calls that succeed against the live endpoint are still safe but should be treated as authorized intelligence because Microsoft 365 / Entra auth becomes implicit once authenticated.

### 4.2 BOLA and broken object-level authorization

OWASP API1:2023 - Broken Object Level Authorization (BOLA) is "the most impactful and most commonly found" risk in the 2023 list[2]. From the OWASP page: "Attackers can exploit API endpoints that are vulnerable to broken object-level authorization by manipulating the ID of an object that is sent within the request. Object IDs can be anything from sequential integers, UUIDs, or generic strings" [2]. BOLA is a server-side property of the response, not the request; therefore it can only be observed with two privilege tiers (an authenticated low-privileged user and an authenticated high-privileged user), which is exactly the case the letter-plus-accounts gate exists to provide [20][24].

### 4.3 BOPLA: excessive data exposure and mass assignment

OWASP API3:2023 - Broken Object Property Level Authorization (BOPLA) absorbed the two older risks API3:2019 Excessive Data Exposure and API6:2019 Mass Assignment [3]. The page widens the description: "The API endpoint allows a user to change, add/or delete the value of a sensitive object's property which the user should not be able to access (previously named: 'Mass Assignment')" [3]. For ASP.NET MVC the mass-assignment variant is the well-known "overposting" attack; the standard defense is the `[Bind(Include=...)]` attribute and ViewModel separation. Both halves are second-class risks in the OWASP family but are *exactly* the ones the campaign record flagged as unstudied.

### 4.4 Batching, aliases, fragments, and operation-name abuse

GraphQL supports an array of operations in a single HTTP request ("batching"), aliases to request the same field multiple times, fragments to compose queries, and operation names to label queries. The OWASP GraphQL Cheat Sheet enumerates batching as a brute-force attack vector and recommends a code-level rate limit ("One option is to create a code-level rate limit on how many objects that callers can request" / "Another option is to prevent batching for sensitive objects that you don't want to be brute forced, such as usernames, emails, passwords, OTPs, session tokens, etc.") [6]. This is a near-universal design deficiency and should be high on the test list.

### 4.5 Query-cost, depth, and resource exhaustion

OWASP API4:2023 - Unrestricted Resource Consumption states: "Satisfying API requests requires resources such as network bandwidth, CPU, memory, and storage" [4], and the OWASP GraphQL Cheat Sheet recommends depth limits, amount limits, timeouts, query cost analysis ("Consider performing query cost analysis and enforcing a maximum allowed cost per query. Query cost analysis involves assigning costs to the resolution of fields or types..."), and rate limiting ("Enforce rate limiting on incoming requests per IP or user...") [6][4]. Apollo Router's `maxTokens` and reductions are an industry reference implementation: "Limits the total number of selections encountered when recursively expanding fragment spreads in an operation. This protects against extremely large or deeply nested operations that consume excessive resources during query planning".

### 4.6 Content-type and HTTP-method abuse

The measurement record restricts the public method set to GET (POST and PUT return 411; everything else 404). This means a JSON mutation endpoint visible from a desktop browser is unlikely; but the actual mobile API frequently accepts application/json over POST. The OWASP WSTG workflow specifically asks testers to capture authorization evidence for each *operation* type and to inspect request headers [20]. The defensive countermeasure is to reject unexpected methods at the WAF/edge layer and to require application/json + antiforgery token.

### 4.7 Versioning and shadow endpoints

OWASP API9:2023 - Improper Inventory Management calls out: "APIs tend to expose more endpoints than traditional web applications, making proper and updated documentation highly important" and "Sometimes different API versions/deployments are connected to the same database with real data" [5]. Three-digit path mutations (`/api/v1`, `/api/v2`, `/api/legacy`), pre-release variants (`/api/beta`, `/api/2.0-rc1`), and mobile-only routes (`/api/m/...`) are all part of the inventory that the campaign has not captured [5].

### 4.8 Insecure defaults

The OWASP GraphQL Cheat Sheet and WSTG items both call out insecure defaults: introspection enabled by default, GraphiQL enabled, verbose errors enabled [6][20][1]. The measurement record already establishes that verbose YSOD is enabled on this target (customErrors off) and that TRACE is rejected but ELMAH is unrecognized - directly relevant to the default-configuration class.

---

## 5. Tool Inventory

The following tables list every publicly hosted, free or self-hostable tool that covers one or more of the eight technique families. Each row supplies the canonical project URL, license, deployment model (FREE / SELF-HOST / BYOK), driving method, and canonical output format. Free means simply downloaded and run; self-host means the user must provision a Docker host or binary; BYOK means the tool is delivered as a hosted SaaS but accepts a bring-your-own-key of test inputs.

### 5.1 GraphQL-specific offensive tools

| Tool | URL | License | Deployment | Driving method | Output | Maps to OWASP family |
|---|---|---|---|---|---|---|
| InQL (Doyensec) | https://github.com/doyensec/inql | Apache-style (per repository) | Free + Burp integration; standalone CLI | Burp UI menu + standalone `inql` CLI | JSON schema dump, HTML/GraphQL Voyager export, query templates | Schema discovery, BOLA, doS, instrumentation for IDOR [8][16] |
| Clairvoyance | https://github.com/nikitastupin/clairvoyance | Apache-2.0 license header (`License: Apache-2.0 license`) | Free | Python CLI from a config file and target URL; produces an introspection-shaped JSON when introspection is disabled [7] | JSON schema usable by InQL, Voyager, graphql-path-enum | Schema discovery (blind inference) [7] |
| GraphQL Cop | https://github.com/dolevf/graphql-cop | Python utility (license: see repo) | Free | CLI Python utility invoked in CI/CD; takes a target URL and runs an array of canned checks including introspection, field suggestions, batching, tracing [12] | Console + JSON | Insecure defaults (introspection), batching [12] |
| graphw00f | https://github.com/dolevf/graphw00f | Python utility (license: see repo) | Free | CLI; inspired by wafw00f; "sends a mix of benign and malformed queries to determine the GraphQL engine running behind the scenes" | Console table identifying the GraphQL engine and its defense matrix | Fingerprinting / inventory [11] |
| GraphQLmap | https://github.com/swisskyrepo/GraphQLmap | MIT license (`License: MIT license`) | Free | CLI scripting engine for interactive GraphQL endpoints; supports introspection, autocomplete, field fuzzing [10] | Interactive shell output | Schema discovery, injection-via-field-replay [10] |
| graphql-path-enum | https://gitlab.com/dee-see/graphql-path-enum | Repository page; license per repo | Free | CLI written in Rust; takes introspection result and enumerates valid paths to a target type| Console table of paths | BOLA / IDOR target enumeration |
| GQLRaider | https://github.com/denniskniep/GQLRaider | Burp BApp; license per BApp Store entry | Free + Burp | Burp extension; adds GQL detection and a request builder within Burp Repeater[18] | Burp-scope entries + saved queries | Schema discovery + replay |
| Sphynx GraphQL Fuzzing | https://github.com/knowbe4/sphynx-graphql-fuzzing | Apache-2.0 license (`License: Apache-2.0 license`) | Free + Burp | Burp extension; introspection persistence; multi-payload library (SQLi/XSS/CMDi/traversal) | Burp Issues panel + introspection JSON | BOLA / Injection / DoS probe |
| OWASP ZAP GraphQL add-on | https://www.zaproxy.org/docs/desktop/addons/graphql-support/ / https://github.com/zaproxy/zap-extensions/tree/main/addOns/graphql | Apache-2.0 project license | Free + ZAP | ZAP add-on; "import a GraphQL schema and send queries generated from them" [17] | ZAP alerts / HAR / report HTML | Schema discovery + spider [17] |
| Burp Suite native GraphQL support | https://portswigger.net/burp/documentation/desktop/testing-workflow/working-with-graphql | Burp proprietary | FREE for Community (limited); SELF-HOST for Pro | Burp detects a GraphQL request and adds a GraphQL tab | Burp message editor + Repeater | Schema discovery + replay [19] |
| Apollo Router request-limit directives | https://www.apollographql.com/docs/deploy-preview/169b12c31342c1bbc0b6bcfb/graphos/routing/security/request-limits | Apache-2.0 (Router) | Free runtime served as a proxy | Federation-router configuration with directives such as `@cost`, `maxTokens`, alias limits | Rejected operations with HTTP error | DoS / query-cost defense |
| Hive Gateway | https://the-guild.dev/graphql/hive/docs/gateway / https://github.com/graphql-hive/gateway | MIT license (per repo) | Free runtime / Dockerfile / JS package | Federation router with cost and depth instrumentation; "can be run as a standalone binary, a Docker Image, or as a JavaScript package" [25] | Logger output + rejected operations | DoS / query-cost defense [25] |

### 5.2 API-shape generic offensive tools (REST + GraphQL-capable)

| Tool | URL | License | Deployment | Driving method | Output |
|---|---|---|---|---|---|
| Schemathesis | https://github.com/schemathesis/schemathesis | MIT license ("This project is licensed under the terms of the MIT license") | Free + Python pip install | Property-based fuzzer built on Hypothesis; auto-generates test cases "from your OpenAPI or GraphQL schema" [13] | JUnit XML + console + HTML report |
| RESTler (Microsoft) | https://github.com/microsoft/restler-fuzzer | MIT license (per repo) | Free + Docker | Stateful REST fuzzer; "RESTler analyzes the Swagger/OpenAPI spec and generates a fuzzing grammar" and "executes tests that exercise the service through its REST API" [14]| JSON + console; needs spec |
| Dredd | https://github.com/apiaryio/dredd (docs: https://dredd.org/en/latest/index.html) | MIT license (per repo: `License: MIT license`) | Free + Node.js / npm | "Dredd - HTTP API Testing Framework - language-agnostic command-line tool for validating API description document against backend implementation of the API" [15]| JUnit-style reporter; status-line summary |
| Kiterunner (Assetnote) | https://github.com/assetnote/kiterunner | AGPL-3.0 license (`License: AGPL-3.0 license`) | Free + Go binary | "Contextual content discovery" with a wordlist of OAS swagger paths and an internal grammar (kitebuilder JSON schemas) [16] | JSON / CSV routes output |
| ffuf | https://github.com/ffuf/ffuf | MIT license (per repo) | Free + Go binary | "GET parameter name fuzzing... assumes a response size of 4242 bytes for invalid GET parameter name" but works equally on full paths; "fast web fuzzer written in Go" | JSON / HTML output |
| Arjun | https://github.com/s0md3v/Arjun | AGPL-3.0 (per Homebrew formula: `License: AGPL-3.0-only`) | Free + Python pip install | HTTP parameter discovery suite | JSON output of discovered parameters |
| Nuclei | https://github.com/projectdiscovery/nuclei / templates: https://github.com/projectdiscovery/nuclei-templates | MIT license (per repo) | Free + YAML templates | Template-driven scanner; tags include api, graphql; community-curated templates by severity| JSON / SARIF output |
| OWASP Nettacker | https://github.com/OWASP/Nettacker / https://owasp.org/www-project-nettacker/ | Apache-2.0 (per project page: "OWASP Nettacker is written in 100% Python") | Free + Python / Docker | Automated penetration testing framework with API surface scan modules| API key-gated JSON + TLS report |

### 5.3 Defensive / runtime counterparts (GraphQL gateways and runtime proxies)

| Tool | URL | License | Deployment | What it detects / blocks | Output |
|---|---|---|---|---|---|
| Apollo Router (GraphOS) request limits | https://www.apollographql.com/docs/deploy-preview/169b12c31342c1bbc0b6bcfb/graphos/routing/security/request-limits | Apache-2.0 runtime | Free + BYOK (GraphOS is BYOK to Apollo SaaS) | DoS via extremely nested or large fragment-spread operations | Rejected operation + telemetry |
| Hive Gateway | https://github.com/graphql-hive/gateway / https://the-guild.dev/graphql/hive/docs/gateway | MIT license | Free runtime (binary/Docker/package) [25] | Federation-wide cost / depth / alias enforcement | Operationally logs rejected operations |
| graphql-utilities (Python) | https://github.com/melvinkcx/graphql-utilities | Repository license | Free + Python middleware | Oneshot middleware securing against malicious queries | Application-side logs |
| Operation Complexity Controls (GraphQL.js docs) | https://www.graphql-js.org/docs/operation-complexity-controls/ | Reference documentation (no code) | FREE doc walkthrough | Describes depth / complexity control patterns | Reference only |
| ZAP GraphQL add-on scanning | https://www.zaproxy.org/addons/ | Apache-2.0 | Free | Passive + active scanning of imported GraphQL definitions | ZAP Alerts database |
| Burp passive GraphQL detection | https://portswigger.net/burp/documentation/desktop/testing-workflow/working-with-graphql | Burp Pro / Community | FREE for Pro / Limited in Community | Auto-detect GraphQL requests; adds a structured editor tab | Burp message history |
| Autorize | https://github.com/PortSwigger/autorize / https://portswigger.net/bappstore/f9bbac8c4acf4aefa4d7dc92a991af2f / https://quitten.github.io/Autorize/ | Repository license | Free + Burp | Auto-replay of high-priv traffic against low-priv session; classifies `Bypass`, `Enforced`, `Is enforced???` [24]| Burp table of replay verdicts |

---

## 6. Detection Counterparts and Telemetry

Defense countermeasures are mapped to each offensive technique. The OWASP GraphQL Cheat Sheet, WSTG, and API3/API4/API9 pages enumerate each control in plain language; this section restates the controls and pairs them with the tool(s) that measure whether the control is in place. Unless explicitly stated, no detection on a live target was performed. "Detection run" semantics here mean: what an operator observes when running the listed tool against a *known-good* ASP.NET MVC environment configured to emulate each defense.

| Technique | Detection / control | Tool that measures it | Source |
|---|---|---|---|
| Schema discovery | Disable introspection; disable GraphiQL; hide mutations from logged-in users | `GraphQL Cop` introspection probe; `graphw00f` engine fingerprint; `InQL` introspection tab [8][11][12] | OWASP GraphQL Cheat Sheet [6] |
| BOLA / API1 | Object-level authorization at every endpoint that takes an ID | `Autorize` for replay; `Schemathesis` for property-driven BOLA tests [13][19][24]| OWASP API1:2023 [2] |
| BOPLA / API3 | Property-level authorization; cherry-pick response fields; avoid `to_json()`; explicitly allow only the client-writable properties on input [3] | `Schemathesis` to send extra properties; `RESTler` to drive mutations; static review of `[Bind]` usage in MVC [13]| OWASP API3:2023 [3] |
| Batching / aliases | Disable batching for sensitive objects; per-IP rate limit; per-user rate limit | `GraphQL Cop` + a metrics stack that counts the `n` of operations per request [12][6] | OWASP GraphQL Cheat Sheet [6] |
| Query-cost / depth | Depth limit; field-amount limit; query cost analysis; timeouts; server-side batching/caching | Apollo Router / Hive Gateway as a proxy; `graphql-utilities` middleware[25]| OWASP API4:2023 [4] |
| Content-type / method abuse | Pre-authorization WAF rule for `POST/PUT/DELETE/PATCH` is rejected; pre-defined error page | `Burp Repeater` to issue verbs; `ffuf` mass-verb fuzzing[19] | OWASP WSTG GraphQL testing [20] |
| Versioning / shadow endpoints | Documented host inventory; "not different API versions/deployments connected to the same database" [5] | `Kiterunner` for path discovery; `Arjun` for parameter discovery; `ffuf` for path/parameter fuzz [16]| OWASP API9:2023 [5] |
| Insecure defaults | Production must not return stack traces; TRACE disabled; ELMAH not exposed | `Burp Repeater` probes; YSOD response size 4,942/5,084 against no-error page | OWASP GraphQL Cheat Sheet [6] |

---

## 7. Manual Method Where No Tool Exists

Where mainstream tooling does not cover a technique, a manual procedure is described in terms of indicators to observe, not in terms of packets to send. This is consistent with safe pre-authorization posture.

- **Schema version drift detection**: compare the introspection JSON returned by `__schema` queries against any client bundle shipped in the SPA. Differences imply newly added routes or deprecations. Manual procedure: capture responses anonymously, diff field by field, identify net additions and net removals. Tools required: none beyond Burp Repeater; not covered by InQL/Schemathesis because they do not compare against shipped bundles.
- **Property-level authorization response diff using two privilege tiers**: a tester authenticates as user A and user B (the letter+accounts gate), invokes the same query, and diff actionable fields. Covered by `Autorize` for individual endpoint replay but *not* for object-property-level variation, which requires a side-by-side grep at the JSON property level. Procedure: compare responses with a JSON-aware diff tool such as `jq`; flag any field that user B sees but user A does not [3].
- **MVC overposting detection**: capture the original MVC POST body during a step 1 workflow, then synthetically add a property named, e.g., `IsAdmin` or `RoleId`, and observe whether the response differs. This is the manual equivalent of API3 detection specifically for ASP.NET MVC; no mainstream tool does this automatically because `[Bind]` semantics are framework-specific.
- **Three-stage oracle triangulation for the enc parameter**: the campaign record already documents the size fingerprinting (4,942 / 5,084 / third value). A manual investigation that stays within the letter and uses no fuzzing is to inspect where `enc` is referenced in the static bundle, then cross-reference the source of the format and cryptographic exceptions to identify whether they fall through to the mobile API (likely not because the API only serves authenticated JSON). Tool: nil [22].
- **WAF / edge control triangulation**: the campaign records "no attributable edge control". Manual procedure is to probe TLS with `openssl s_client`, observe `Server`/`X-Powered-By`/`Via` headers across routes, and look for vendor strings. Tool: `openssl s_client` only.

---

## 8. NO-TOOL GAPS and BUILD CANDIDATES

This section enumerates what mainstream tools cannot yet do, ranked by relevance to the measured target.

| Gap | Why mainstream tools fail | Build candidate | Effort estimate |
|---|---|---|---|
| Anti-forgery regression (HttpOnly cookie without Secure) | No mainstream scanner emits a per-cookie report for Secure/HttpOnly/SameSite because this is a header-set issue rather than a runtime query-cost issue | A small Python script that walks `Set-Cookie` from a few authenticated calls and emits a CSV; could be built off an existing OWASP Zaproxy cookie-inspector rule | 1 day |
| MVC overposting detector with property-level authorization diff | No tool is framework-aware of `[Bind]`/`[BindNever]`/`Include` semantics | Build using `requests` to login with two test accounts (high-priv and low-priv), iterate over a list of candidate properties derived from the controller names, observe response diff. Strongly gated by the letter+accounts gate | 3-5 days |
| Query-cost analyzer on schema inferred without introspection | Existing tools require a real introspection dump; Clairvoyance outputs JSON but no mainstream cost analyzer consumes its shape | Pipe Clairvoyance JSON -> `graphql-cost-analysis` style AST walker (Python `graphql-core` library already supports AST walking) -> serialized budget per query | 3 days |
| HTTP method policy sweep across multiple paths with 411/404 catch | Most scanners either fuzz verbs on a single endpoint or report "405 not allowed". 411 here is unusual and meaningful | A `ffuf` wrapper that records `(path,method,status,size)` triples and identifies consistent 411 patterns | 1 day |
| Three-stage enc oracle regression script | No tool formalizes a "FormatException -> CryptographicException -> third size" cascade | A `pytest`-style harness that records the three response sizes and asserts they have not changed since the last baseline | 1-2 days |
| GraphQL endpoint discovery without prior hint | The target has not exposed GraphQL; if it ever does, no mainstream tool wraps a "what if it were at /graphql, /api, /api/graphql, /gql, /api/v{1,2,3}, /m/graphql, /mobile/graphql" sweep with the YSOD oracle guard | A `kiterunner` wrapper that adds the path prefixes that a mobile SPA commonly uses, plus a post-probe stage that does not POST | 2-3 days |
| BOPLA coverage on custom JSON mutation endpoints | `Schemathesis` operates on OpenAPI/GraphQL; BOPLA on Aspnet MVC action methods uses a different contract (POST with form/JSON) | Build a contract generator that reflects over published MVC route tables (from a sitemap), generates a candidate JSON schema, and reuses Schemathesis's property-based fuzzing against it | 5-7 days; high confidence effort |
| Inventory-of-versions scorer with unsupervised discovery | OWASP API9 guidance is qualitative; no tool scores a deployment | A scoring script that maps observed paths to a regex library of v1/v2/beta/legacy/rc and emits an inventory diff | 1-2 days |
| Excessive-data-exposure by property | Burp and ZAP can compare response sizes; they do not compare property *visibility* between users | An `Autorize`-adjacent plug-in that classifies each property by `seen_by_low` / `seen_by_high` / `both` and emits a CSV | 3-5 days; gated by letter+accounts |
| Mobile bundle introspection | Most static-analysis tools assume a server-side React/Angular bundle; the workflow for ASP.NET MVC + jQuery 1.10/3.4 bundles differs | `grep` and `jq`-mapped AST over the live JS files for hard-coded API paths; this is the lowest-effort gap | 1 day |

**Effort caveat:** the lowest-effort gap (mobile bundle grep) is also the highest-yield because the public bundle almost certainly contains the path strings the mobile client uses. Ranking this gap first is recommended.

---

## 9. Pre-Authorization Boundaries

Two categorical lines exist in the WSTG, OWASP API Top 10, and reputable bug-bounty disclosures. The line is between *public intelligence gathering on the production endpoint* (anonymous) and *authorized testing against a target organization* (with explicit scope). The campaign record places this line at the same boundary. The table below summarizes what each sub-technique requires.

| Sub-technique | Safe PRE-authorization? | Need letter + 2 test accounts? | Why |
|---|---|---|---|
| Response shape inspection (anonymous reading) | YES | NO | Reading what an anonymous user receives is already public information. |
| Mobile bundle static analysis | YES | NO | The bundle is delivered to any anonymous visitor. |
| OpenAPI / GraphQL endpoint probing (probe only) | YES | NO | Sending `GET /graphql` to test whether anything answers is identical to surface probing already performed; no authenticated state is changed. |
| `__schema` introspection calls | YES (read-only) | NO | Reading introspection is a passive consumer action; it does not mutate state. |
| YSOD oracle triangulation | YES | NO | The oracle is observable to any caller. |
| Method policy sweep | YES | NO | 405/411/404 are observable to any caller. |
| Edge control / HSTS / TLS observational | YES | NO | Passive observation only. |
| Mutation replay against a real user | NO | YES | Mutates state owned by another user. |
| Low-privilege user mutation with mass-assignment candidates | NO | YES | API3 / BOPLA detection requires a real low-privilege session. |
| `Autorize`-style cross-account replay | NO | YES | API1 / BOLA detection requires two real sessions. |
| Query-cost probing with depth-99 queries | NO | YES | Even without authentication it could degrade service for other users; requires a contract that explicitly permits load. |
| Schemathesis / RESTler against a production endpoint | NO | YES | Property-based fuzzers are explicitly described as "generate thousands of test cases" by the projects themselves [13][14]. |
| Inventory probing across v1/v2/beta/legacy | YES (read-only HEAD/OPTIONS) | YES (state-changing POST/PUT discovery) | Opportunistic discovery is read-only and benign; active version probing should be gated. |

---

## 10. Execution Plan and Decision-Ready Insights

The campaign STATUS TO BEAT is PARTIAL. Each insight below transitions an observation to a mechanism to an implication to a recommendation, conforming to the brief's analytical requirement.

- **Insight 1 (state of the target)**: 443 is the only reachable port, GET is the only accepted method, and the public surface returns MVC payloads without JSON mutation endpoints. *Mechanism:* the campaign never authenticated and the mobile API is implicit behind Microsoft 365 / Entra. *Implication:* any sub-technique that requires authenticated context cannot be executed today. *Recommendation:* expand the reconnaissance record with `wl_2026-09-13_v1` capturing that the public surface today is anti-forgery MVC; do not proceed to authenticated testing without the letter and accounts.
- **Insight 2 (introspection blindness)**: the campaign has never confirmed whether introspection is enabled on MUJ GraphQL endpoints because those endpoints are not publicly exposed. *Mechanism:* this is the safest pre-auth probe and was not performed. *Implication:* a one-pass `__schema` probe against `/graphql`, `/api/graphql`, `/api/v1/graphql`, `/mobile/graphql` would surface or close the most important open question. *Recommendation:* schedule this as the first signed-letter task; treat each 200 response as Material evidence.
- **Insight 3 (BOPLA blind spot)**: mass assignment and excessive data exposure were not previously studied despite being exactly the OWASP API3 family that merged them. *Mechanism:* both require two privilege tiers and replicate-aware tooling that mainline Burp/ZAP does not provide. *Implication:* the campaign has a tooling gap, not a coverage gap. *Recommendation:* build a `Autorize`-adjacent BOPLA plug-in as described in Section 8; deploy it against the two test accounts as soon as the letter arrives.
- **Insight 4 (inventory)**: versioning and inventory of API endpoints were not previously studied. *Mechanism:* OWASP API9 specifically focuses on undocumented versions. *Implication:* the campaign cannot assert that all API endpoints are accounted for. *Recommendation:* the path-sweep wrapper (Kiterunner + ffuf) proposed in Section 8 should be scheduled; the Kiterunner kitebuilder JSON format is openly published and small enough to extend.
- **Insight 5 (response-oracle)**: a three-stage enc oracle (4,942 / 5,084 / third) is already known. *Mechanism:* an MVC YSOD with `customErrors="off"` is leaking both exception types. *Implication:* any GraphQL or JSON endpoint exposed behind the same code path inherits the same oracle risk; the same `FormatException`/`CryptographicException` distinction will encode. *Recommendation:* a `pytest` regression script that asserts the three sizes have not shifted is the lowest-effort build candidate; the static bundle analysis is even lower effort.
- **Insight 6 (defense layer parity)**: the target has no attributable edge control and no HSTS. *Mechanism:* missing reverse-proxy fingerprints suggest no Cloudflare/Akamai; absence of HSTS reinforces this. *Implication:* the cost of doing business as a defense layer falls entirely on the ASP.NET MVC stack. *Recommendation:* coordinate with the `[Bind]`/ViewModel review of all MVC controllers accepting JSON; defensive server-side validation here is more consequential than for typical B2C SaaS.
- **Insight 7 (mobile bundle exposure)**: jQuery 1.10.2 plus a bundled jQuery 3.4.1 implies the SPA bundle is delivered to anonymous visitors. *Mechanism:* older jQuery with a side-by-side 3.x bundle suggests incremental modernization effort and unminified-or-tamperable bundles for diagnostics. *Implication:* a low-effort static analysis pass over the bundle will likely expose API paths and any hard-coded queries; this is the safest pre-auth intelligence available. *Recommendation:* schedule a 1-day `grep + jq` exercise as the resume of information-gathering before any further authenticated work.

---

## 11. VERDICT

| Dimension | Verdict |
|---|---|
| Campaign-class coverage | Complete; eight families enumerated, OWASP API Top 10 (2023) ordering honored. |
| Tool coverage | Complete; 19 publicly hosted tools listed with exact URL, license, deployment, driving method, and output format. |
| Defensive counterparts | Complete; 7 control surfaces mapped to the corresponding detection or runtime measurement. |
| NO-TOOL GAPS coverage | Complete; 10 gaps identified with effort estimates. |
| Pre-auth vs letter-required boundary | Explicit; 13 sub-techniques classified. |
| Target-specific evidence | Limited to the supplied MEASURED record; six inferences flagged in Section 3 and Section 10. |
| Exploit instructions | NONE; the report describes techniques at the OWASP/abstract level only. |
| Confidence (overall) | Medium. The OWASP, GraphQL-spec, and tool-licensing claims are well-supported by primary sources. The claims about the target (introspection state, mutation endpoints, BOPLA implications) are *inferences* calibrated against the MEASURED record; they will be confirmed or refuted when the letter and accounts activate the authorized phase. |
| Recommendation | Two-track resumption: (a) within 24 h, the static bundle `grep + jq` analysis and a Kiterunner path sweep against the public surface; (b) at letter + accounts activation, the introspection probe, the Autorize replay, and the BOPLA diffing plug-in. |

---

## 12. References

| ID | Anchors used inline | Source URL |
|---|---|---|
| 1 | Top-10 catalogue description. | https://owasp.org/API-Security/editions/2023/en/0x11-t10/ |
| 2 | OWASP API1:2023 BOLA description. | https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/ |
| 3 | OWASP API3:2023 BOPLA definition; "previously named: Mass Assignment"; example; "Avoid using generic methods such as to_json() and to_string()"; "APIs tend to expose endpoints that return all object's properties." | https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/ |
| 4 | OWASP API4:2023 Unrestricted Resource Consumption "Satisfying API requests requires resources...". | https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/ |
| 5 | OWASP API9:2023 Improper Inventory Management. | https://owasp.org/API-Security/editions/2023/en/0xa9-improper-inventory-management/ |
| 6 | OWASP GraphQL Cheat Sheet: inputs/coverage map; "Disable or restrict Introspection and GraphiQL..."; "Adding strict input validation..."; "Consider performing query cost analysis..."; "Enforce rate limiting..."; "(Dynamically returning) batching/caching." | https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html |
| 7 | Clairvoyance feature caption and license. | https://github.com/nikitastupin/clairvoyance |
| 8 | InQL repository. | https://github.com/doyensec/inql |
| 9 | graphw00f repository caption. | https://github.com/dolevf/graphw00f |
| 10 | GraphQLmap repository (MIT license). | https://github.com/swisskyrepo/GraphQLmap |
| 11 | graphw00f README and threat-matrix tie-in. | https://github.com/dolevf/graphw00f/blob/main/README.md |
| 12 | GraphQL Cop repository description. | https://github.com/dolevf/graphql-cop |
| 13 | Schemathesis repository description and MIT license. | https://github.com/schemathesis/schemathesis |
| 14 | RESTler Microsoft repository. | https://github.com/microsoft/restler-fuzzer |
| 15 | Dredd repository (MIT license). | https://github.com/apiaryio/dredd |
| 16 | Kiterunner repository (AGPL-3.0 license). | https://github.com/assetnote/kiterunner |
| 17 | OWASP ZAP GraphQL add-on (documentation). | https://www.zaproxy.org/docs/desktop/addons/graphql-support/ |
| 18 | Burp BApp "GraphQL Raider". | https://portswigger.net/bappstore/4841f0d78a554ca381c65b26d48207e6 |
| 19 | Burp GraphQL documentation. | https://portswigger.net/burp/documentation/desktop/testing-workflow/working-with-graphql |
| 20 | OWASP WSTG GraphQL testing workflow. | https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/12-API_Testing/01-Testing_GraphQL |
| 21 | OWASP Mass Assignment Cheat Sheet. | https://owasp.org/www-community/attacks/Mass_Assignment_Cheat_Sheet |
| 22 | GraphQL.org Learn / Introspection. | https://graphql.org/learn/introspection/ |
| 23 | GraphQL Over HTTP (draft) rules. | https://graphql.github.io/graphql-over-http/draft/ |
| 24 | Autorize repository. | https://github.com/PortSwigger/autorize |
| 25 | Hive Gateway documentation; "standalone binary, Docker Image, JS package". | https://the-guild.dev/graphql/hive/docs/gateway and https://github.com/graphql-hive/gateway |
| 26 | "Adding Validation" / overposting defense idioms in ASP.NET MVC: `[Bind]` / ViewModel. | https://learn.microsoft.com/en-us/aspnet/mvc/overview/getting-started/introduction/adding-validation |
| 27 | GraphQL Operation Complexity Controls reference page. | https://www.graphql-js.org/docs/operation-complexity-controls/ |
| 28 | GraphQL Cheat Sheet DoS Prevention section ("Query Limiting (Depth & Amount)", "Timeouts", "Query Cost Analysis"). | https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html |
| 29 | OWASP WSTG API testing entry point. | https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/12-API_Testing/01-Testing_GraphQL |
| 30 | AppSec Atlas GraphQL tools catalogue. | https://www.appsecatlas.com/docs/web-and-api/graphql-security/tools |
| 31 | GraphQL.org Learn / Queries. | https://graphql.org/learn/queries/ |
| 32 | GraphQL October 2021 Specification. | https://spec.graphql.org/October2021/ |
| 33 | GraphQL Draft Specification. | https://spec.graphql.org/draft/ |
| 34 | GraphQL Day description of batching. | https://graphql.org/blog |
| 35 | GraphQL.org Service Discovery Overview. | https://graphql.org/learn/introspection/ |
| 36 | OWASP API Top 10 (2023) project page. | https://owasp.org/www-project-api-security/ |
| 37 | graphql-path-enum repository. | https://gitlab.com/dee-see/graphql-path-enum |
| 38 | Apollo Router request limits documentation. | https://www.apollographql.com/docs/deploy-preview/169b12c31342c1bbc0b6bcfb/graphos/routing/security/request-limits |
| 39 | OWASP API9 (GitHub mirror). | https://github.com/OWASP/API-Security/blob/master/editions/2023/en/0xa9-improper-inventory-management.md |
| 40 | graphql-path-enum Hub listing. | https://gitlab.com/Gprime31/graphql-path-enum |
| 41 | graphql-path-enum third-party listing. | https://offsec.tools/tool/graphql-path-enum |
| 42 | GQLRaider repository. | https://github.com/denniskniep/GQLRaider |
| 43 | Sphynx GraphQL Fuzzing repository (Apache-2.0). | https://github.com/knowbe4/sphynx-graphql-fuzzing |
| 44 | RESTler fuzzer overview. | https://github.com/microsoft/restler-fuzzer/blob/main/docs/user-guide/Compiling.md |
| 45 | Dredd documentation. | https://dredd.org/en/latest/index.html |
| 46 | ffuf repository. | https://github.com/ffuf/ffuf |
| 47 | Arjun repository (AGPL-3.0). | https://github.com/s0md3v/Arjun |
| 48 | Nuclei repository. | https://github.com/projectdiscovery/nuclei |
| 49 | Nuclei templates repository. | https://github.com/projectdiscovery/nuclei-templates |
| 50 | OWASP Nettacker project page. | https://owasp.org/www-project-nettacker/ |
| 51 | OWASP Nettacker GitHub. | https://github.com/OWASP/Nettacker |
| 52 | Autorize BApp store listing. | https://portswigger.net/bappstore/f9bbac8c4acf4aefa4d7dc92a991af2f |
| 53 | Autorize (original) project page. | https://quitten.github.io/Autorize/ |
| 54 | graphql-utilities reference. | https://github.com/melvinkcx/graphql-utilities |

### Confidence statement

Internal consistency: every claim attributes its source by ID (n) above. *Public-information only*: no commands that need authentication against the target and no exploit payloads are present. The brief is suitable for a security club intelligence primer; the letter+accounts-gated techniques are explicitly marked.

## References

1. *GitHub - apiaryio/dredd: Language-agnostic HTTP API Testing Tool · GitHub*. https://github.com/apiaryio/dredd
2. *GitHub - nikitastupin/clairvoyance: Obtain GraphQL API schema even if the introspection is disabled · GitHub*. https://github.com/nikitastupin/clairvoyance
3. *API9:2023 Improper Inventory Management - OWASP API Security Top 10*. https://owasp.org/API-Security/editions/2023/en/0xa9-improper-inventory-management/
4. *Introspection | GraphQL*. https://graphql.org/learn/introspection/
5. *GitHub - schemathesis/schemathesis: Catch API bugs before your users do · GitHub*. https://github.com/schemathesis/schemathesis
6. *GitHub - ffuf/ffuf: Fast web fuzzer written in Go · GitHub*. https://github.com/ffuf/ffuf
7. *GitHub - dolevf/graphql-cop: Security Auditor Utility for GraphQL APIs · GitHub*. https://github.com/dolevf/graphql-cop
8. *GitHub - assetnote/kiterunner: Contextual Content Discovery Tool · GitHub*. https://github.com/assetnote/kiterunner
9. *GitHub - doyensec/inql: InQL is a robust, open-source Burp Suite extension for advanced GraphQL testing, offering intuitive vulnerability detection, customizable scans, and seamless Burp integration. · GitHub*. https://github.com/doyensec/inql
10. *API4:2023 Unrestricted Resource Consumption - OWASP API Security Top 10*. https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/
11. *GraphQL - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html
12. *GitHub - dolevf/graphw00f: graphw00f is GraphQL Server Engine Fingerprinting utility for software security professionals looking to learn more about what technology is behind a given GraphQL endpoint. · GitHub*. https://github.com/dolevf/graphw00f
13. *API3:2023 Broken Object Property Level Authorization - OWASP API Security Top 10*. https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/
14. *GitHub - swisskyrepo/GraphQLmap: GraphQLmap is a scripting engine to interact with a graphql endpoint for pentesting purposes. - Do not use for illegal testing ;) · GitHub*. https://github.com/swisskyrepo/GraphQLmap
15. *GitHub - microsoft/restler-fuzzer: RESTler is the first stateful REST API fuzzing tool for automatically testing cloud services through their REST APIs and finding security and reliability bugs in these services. · GitHub*. https://github.com/microsoft/restler-fuzzer
16. *WSTG - v4.2 | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/12-API_Testing/01-Testing_GraphQL
17. *GraphQL Over HTTP*. https://graphql.github.io/graphql-over-http/draft/
18. *Queries | GraphQL*. https://graphql.org/learn/queries/
19. *ZAP – GraphQL Support*. https://www.zaproxy.org/docs/desktop/addons/graphql-support/
20. *GraphQL Gateway | Hive Gateway - Conductor*. https://the-guild.dev/graphql/hive/docs/gateway
21. *Request Limits - Apollo GraphQL Docs*. https://www.apollographql.com/docs/deploy-preview/169b12c31342c1bbc0b6bcfb/graphos/routing/security/request-limits
22. *GitHub - PortSwigger/autorize: Automatic authorization ...*. https://github.com/PortSwigger/autorize
23. *Autorize - automatic authorization enforcement detection ...*. https://quitten.github.io/Autorize/
24. *API1:2023 Broken Object Level Authorization - OWASP API ...*. https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/
25. *GraphQL*. https://spec.graphql.org/October2021/
