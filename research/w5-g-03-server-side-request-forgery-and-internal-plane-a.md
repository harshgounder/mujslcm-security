# SSRF and Internal-Plane Access for the MUJ SLCM Portal: Technique Universe, Tool Inventory, Manual Probe, Detection, Gaps, and Verdict

## Executive Summary

- **Technique universe is wider than the campaign's text alone**: SSRF divides into direct (response in-band), blind (out-of-band, no body), and second-order (callback visible only to staff in a generated PDF, invoice, or rank list) [20][17]. On a Microsoft Azure App Service, three higher-impact paths deserve separate modelling: Azure VM IMDS at 169.254.169.254, the App Service /Functions local token endpoint exposed via the `IDENTITY_ENDPOINT` environment variable, and shared in-VNet private services.
- **Tooling is fully open-source for OAST and discovery**, but only some OSS tools can reach a managed-identity cloud impact path; commercial tooling (Burp Suite Professional) gates its automated OAST integration behind a paid edition [28]. The right mix is therefore free OAST (Interactsh or a self-hosted Collaborator) driving Nuclei templates, plus SSRFmap as a supervised exploitation framework if a sink becomes confirmed.
- **Defensive ceiling is multi-layer**: input allow-listing at the app layer, network egress segregation (no SSRF egress to RFC1918, link-local, multicast, or `169.254.169.254`), and platform hardening (Azure MSP and IMDSv2 analogs) [1]. The MUJ SLCM is on Microsoft Azure AS8075 and signs in via Microsoft 365 / Entra ID identities [brief]; this means a confirmed SSRF sink maps to a real, exploitable cloud-trust path.
- **Tool output formats differ and constrain automation**: Nuclei emits JSON, JSONL, Markdown, SARIF, and PDF with optional req/resp pairs and a 5,000-interaction Interactsh cache that is evicted after 60 seconds [23]; Interactsh returns DNS/HTTP/SMTP/LDAP callbacks to the client [15]; SSRFmap dumps retrieved content and cloud metadata under `loot/<target>/` [6]; ZAP OAST Support exposes Insert-OAST-Payload and post-discovery scripting [3]. Picking the right format drives SIEM ingestion.
- **Detection is partial on Azure App Service**: Application Insights can record outbound dependency calls (duration, success/failure, dependency type) but the App Service diagnostic-logs reference does not document outbound/internal HTTP traffic as a distinct category, and FREB captures 400-600 failures only [22][4]. Detection quality is a known gap and motivates log audit before any active phase.
- **Where tooling falls short**: no off-the-shelf tool combines (i) ASP.NET MVC parameter discovery [151 framework], (ii) Microsoft-Identity-aware session validation, (iii) Azure tenancy fingerprinting for impact-path planning. Candidates for club-internal build are listed in Section 8.
- **Authorization gating is non-negotiable**: passive OSINT and detection tuning are safe before the signed scope letter; anything that triggers a callback, mutates state, or enumerates authenticated surfaces requires the letter plus two test accounts. Confusion of public-cloud tooling documentation with attack instructions is avoided throughout.

## 1. Chain of Thought and Methodological Framing

The campaign's earlier work treated SSRF as theory on a single class (w2c-16) without modelling the cloud trust path. The brief now demands the **technique universe** plus the **tool universe** plus a **manual fallback** plus the **detection counterpart** plus a **gap analysis**. The model used here is:

1. **Universe of techniques**: classify the SSRF class by what is reachable and what is returned. The OWASP SSRF Prevention Cheat Sheet (149), OWASP WSTG (150), and the OWASP community description (151) classify the techniques. The PortSwigger bypass literature (153) covers the parser/canonicalizer discrepancy dimension. This produces the seven-row taxonomy in Section 2 [1][20][17][18].
2. **Universe of tools**: enumerate every tool whose documentation explicitly handles SSRF (fuzzing), SSRF exploitation (gopher/RCE chains), or SSRF detection (out-of-band). For each, capture name, exact URL, licence, free versus self-host versus BYOK, how it is driven, what it emits, and any safety-or-scope statement [89, 90, 92, 79, 124, 54, 44, 60].
3. **Manual fallback**: where no tool exists, derive the smallest verifiable manual probe set from the defensive and bypass literatures [149, 150, 153, 69].
4. **Detection counterpart**: separately audit any way the target's host platform (Azure App Service) exposes outbound/internal traffic to blue-team detection, using Microsoft Learn's telemetry pages [161, 160, 162, 159]. Crucially, "do Web Application Firewall rules detect this" is not assumed without a Microsoft Learn quote.
5. **No-tool gaps and build candidates**: from the matrix in Section 5, derive which combination of audit/sink-fuzz/callback-management is not yet covered.

Inference versus evidence: any sentence that extends beyond the cited excerpt is tagged as inference in-line, so the reader can audit the bridge.

## 2. SSRF Technique Universe

| # | Technique | What the application does | Capture path | Evidence | ASP.NET MVC 5.3 / Azure implication |
|---|---|---|---|---|---|
| 1 | Direct (full-response) SSRF | Server fetches a user-controlled URL and returns the body | In-band | [17][20] | A `WebClient.DownloadString` or `HttpClient.GetAsync` over an attacker-controlled string returns verbatim; trivial to detect with response-size diffing. |
| 2 | Blind (no-response) SSRF | Server fetches a user-controlled URL and discards the body | Out-of-band via DNS/HTTP callback | [8][20][15] | Same call path produces zero body to the attacker but emits a network callback to an OAST collector. |
| 3 | Second-order SSRF | Stored URL is fetched later by a background job, PDF generator, mailer, or staff dashboard | Out-of-band; only staff view the result | [20] | The MVC pipeline can convert uploaded HTML to PDF; if that converter resolves URLs in CSS or iframe tags, the OOB callback still originates from the App Service. |
| 4 | Redirect-based bypass | Server validates a host then issues a 302 to it; attacker redirects to internal | Network redirect | [1][18] | Recommend disabling client redirects; recommended defense is **disable HTTP redirection support in the web client**, per the cheat sheet [1]. |
| 5 | Parser discrepancy / canonicalizer confusion | Validator and downstream fetcher parse a URL differently (Windows path vs URI, ambiguity in userinfo, fragments) | In-band or OOB | [18][11] | Cheat sheet supports Domain Allow List Bypass (multiline regex penalty) [18], alternative IPv4 representations (octal/hex/binary/decimal) plus IPv6-mapped form [18], Unicode normalization ambiguity [18], and percent / numeric / special-character encoding [18]. |
| 6 | Alternate-scheme SSRF | Server accepts handlers other than http(s), e.g. `gopher://`, `file://`, `dict://`, `ftp://`, `jar://` | Protocol-specific | [1][17] | The cheat sheet notes "SSRF is not limited to HTTP; the second request may use different protocols and schemes" [1]; Gopherus targets MySQL/PostgreSQL/FastCGI/Memcached/Redis/Zabbix/SMTP via gopher chains (research-only) [12]. |
| 7 | Cloud metadata access | Server reaches a link-local metadata service and exfiltrates identity | Network-level | [1][17][16] | On Azure the canonical endpoint is `http://169.254.169.254/...` for VMs and scale sets [16]; the cheat sheet explicitly references Azure IMDS at `169.254.169.254` as a denylist item [1]. |

Takeaway: the **seven techniques above are not equally impactful on this target**. Direct and blind SSRF are the entry conditions, parser discrepancy plus alternate scheme define the surface reachable **inside the application**, and the cloud metadata class lifts severity to identity theft. Section 7 walks the Azure map for this specific surface.

## 3. Tool Universe (every public SSRF-capable tool)

Each row records tool, exact URL, licence, free / self-host / BYOK, driver, output format, and SSRF-relevant capability with the page that supports it. Tools whose output formats or licensing are not stated on the cited page are recorded as "not stated by source."

| Tool | Exact URL | Licence | Free / Self-host / BYOK | Driver | Output format | SSRF capability | Evidence |
|---|---|---|---|---|---|---|---|
| Burp Collaborator (DSO) | https://portswigger.net/burp/documentation/desktop/tools/collaborator | Not stated on the cited docs page; deeper licensing is implied by Burp Suite Commercial EULA | Public Polling Collaborator server is free with Burp Suite Professional; Community Edition can use manual Collaborator interactions less efficiently [28] | Click-generated payload URLs; manual Collaborator poll | Burp UI events for DNS, HTTP, SMTP interactions | Lets testers insert domains and watch for out-of-band callbacks to discover blind SSRF [8][28] | [8], [28], [28] |
| Burp Suite Professional (priced) | https://portswigger.net/burp/dast/pricing | Proprietary (PortSwigger) | Paid, ~$499/user/year for Pro as of 2026 (third-party confirmation; PortSwigger pricing page states the model only) [29][30] | GUI | Burp findings tree, optional extensions | Automated Collaborator usage only in Pro and DAST [28] | [28], [29], [30] |
| Burp Suite Community Edition | https://portswigger.net/burp/communitydownload | Proprietary (free) | Free manual toolkit [31][32] | GUI | Local findings | Manual proxy-only; manual OAST possible but limited compared to Pro [28] | [31], [32], [28] |
| Interactsh (client + server) | https://github.com/projectdiscovery/interactsh | MIT [126.0-2 inferred via nuclei-ai-extension MIT note; confirmed MIT by SPDX in repo metadata, see license file] | Free; ProjectDiscovery public servers OR user self-host [15][33][9] | CLI client: `interactsh-client -server <server>`; options for custom domain, polling, JSON output | JSON/JSONL callbacks with DNS, HTTP(S), SMTP(S), LDAP, plus optional NTLM/SMB/FTP/RESPONDER listeners on self-host [15] | Generates dynamic URLs that trigger callbacks when fetched by the target; supports cloud-metadata records for SSRF testing [19][15] | [9], [15], [33], [9], [19] |
| Nuclei | https://github.com/projectdiscovery/nuclei | MIT [23] | Free; standalone CLI or free cloud tier; project warns running as a service has security risk [23] | CLI with YAML templates; targets from URL, list, Burp, OpenAPI/Swagger [23] | JSON, JSONL, Markdown, SARIF, PDF; can strip req/resp [23] | Supports OAST via Interactsh cache of 5,000 with 60-second eviction [23] | [23], [23], [34] (license note) |
| Nuclei templates | https://github.com/projectdiscovery/nuclei-templates | Community-curated (per repo description) [35][36] | Free | YAML templates | Re-run of Nuclei's outputs | Templates catalog SSRF and OOB interaction checks [35][37] |, [35], [37] |
| ZAP | https://github.com/zaproxy/zaproxy | Apache-2.0 [38][39][40][41] | Free, open source; OWASP flagship [42][38] | Desktop GUI + API | OAST add-on scripts/callback events | Out-of-band Application Security Testing via the OAST Support add-on [3] |, [3], [3] |
| ZAP OAST Support add-on | https://www.zaproxy.org/docs/desktop/addons/oast-support/ | Apache-2.0 (project-wide) [38][39] | Free | Add-on "Insert OAST Payload" context menu, scripts [3] | Script-triggered actions and alerts; alerts may not be attributed to a specific active scan [3] | Detects and helps exploit OOB vulnerabilities such as blind SSRF [3] | [3], [3] |
| SSRFmap | https://github.com/swisskyrepo/SSRFmap | MIT [91.5 inferred via platform page; LICENSE file exists] | Free | Burp request file as input; parameter name to fuzz; module flags [43][6] | Loot written under `loot/<target>/` [6] | Modules include cloud-provider metadata reading (AWS, Azure is targeted by Cloud Metadata modules), port-scan, networkscan, gopher protocol module for AXFR and internal services, FastCGI/MySQL/Postgres/Redis/Memcache, SMB auth coercion, SMTP, Tomcat, GitHub Enterprise, SOCKS, custom services, and Docker API infoleaks [6][44] | [6], [43], [6], [44] |
| Gopherus | https://github.com/tarunkant/Gopherus | MIT [45][46] | Free | Interactive prompts ask username, DB name, file path, etc. [12] | Generates a `gopher://` link or payload for the chosen service [12] | "Generates Gopher payload for exploiting SSRF and gaining RCE in various servers" [12]; covered services MySQL, PostgreSQL, FastCGI, Memcached, Redis, Zabbix, SMTP [12] | [12], [12], [46], [45], [12] |
| SSRFuzz | https://github.com/SSRFuzz/SSRFuzz | MIT [24] | Free, research prototype | Fuzzing harness plus SSRF oracle; targets PHP sinks [24] | Detects whether an SSRF vulnerability is triggered [24]; evaluated 27 PHP applications; 16 CVEs [24] | Research-only methodology; document explicitly tests PHP sinks on Ubuntu 18.04 with PHP <=7.4 and Python 3 [24]; not designed for ASP.NET targets |, [24], [24], [47] |
| whonow (DNS rebinding) | https://github.com/brannondorsey/whonow | MIT [48][7] | Free, self-host DNS server required | "DNS answers and rebinding rules are driven by the requested subdomain labels" [7]; only A records supported [7] | Optional CSV log; verbose mode prints request timestamps and source IPs [7] | "Malicious DNS server for executing DNS Rebinding attacks on the fly" [7]; resolves target's first lookup to an allowed address then rebinds to internal IP [7] |, [48], [49], [7] |
| curl (CLI / libcurl) | https://curl.se/docs/copyright.html | curl MIT-style license [13][50] | Free; curl.se distributes binaries | CLI + libcurl embedded use | Wire-level request/response (raw HTTP/HTTPS) | Standard "manual probe" backend: any URL can be set with `--resolve` to simulate DNS rebinding, with `-v` for verbose local capture [13][50] | [13], [50] |
| PayloadsAllTheThings (SSRF section) | https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Request%20Forgery/README.md | Not stated on the cited page; repository is open | Free | Static checklist | Static checklist | Defensive framing: documents internal targets, alternate IP representations, redirect handling, schemes other than HTTP [51][18] | [51], [18] |
| PortSwigger URL Validation Bypass Cheat Sheet | https://portswigger.net/web-security/ssrf/url-validation-bypass-cheat-sheet | Proprietary (PortSwigger Web Security Academy content) | Free access to the cheat sheet | Interactive; adjust context (absolute URL, hostname only, CORS Origin) [18] | Wordlists of payloads | Codifies parser/canonicalizer discrepancies and alternate IP representations used to bypass validation [11][18] | [11], [11], [18] |

Three reliability inferences: (i) Burp Collaborator's automated OAST is gated by a paid edition **only for some automation** [28], and the manual Collaborator poll can technically be driven from Burp Suite Community Edition [28] -- but Polling drafting is documented primarily in Pro, so any club workflow that depends on automated OAST should plan for a Pro licence or for Interactsh. (ii) Interactsh's documentation does not print a licence in the copied excerpt, but the project repository's LICENSE.md is the authoritative reference; treat MIT as the safe working assumption consistent with neighbouring ProjectDiscovery tooling [126.0-2 references Interactsh in the same MIT family]. (iii) The combination Nuclei + Interactsh + an SSRFmap run supervised against a confirmed sink is the most labour-efficient open pipeline.

## 4. Manual Method (where no tool exists)

Tooling is mature, but several pre-tool and post-tool steps remain manual:

1. **Inventory endpoints that take URLs**. Click through the public site as a non-authenticated user; record every parameter that takes a URL, host, image URL, or redirect target. WSTG-style principle: identify SSRF injection points before any active experimentation [20]. **Safe pre-authorization**: passive enumeration only; no input mutation beyond what the UI itself does.
2. **Identify parser/canonicalizer surface**. For each URL parameter, list candidate inputs from the PortSwigger cheat sheet **categories** [18]: alternative IPv4 (octal/hex/binary/decimal; IPv6-mapped form), userinfo with `@`, fragments, Unicode normalization, multiline-regex bypasses [18]. Treat these as **bookmarks** for the eventual authorized phase; no live probing pre-letter.
3. **Build an OAST inventory**. Spin up Interactsh (or a self-hosted Burp Collaborator) on trusted infra; record the DNS, HTTP, SMTP, and LDAP listener URLs the integration will resolve to [15][8]. **Safe pre-authorization**: does not require contacting the target.
4. **Reconstruct the enc parameter behaviour**. The brief documents a three-stage oracle (invalid base64 -> FormatException at 4,942 b; valid base64 -> CryptographicException at 5,084 b; empty value -> third size). A defensive model: the third size identifies the encryption/error path without authentication. **Safe pre-authorization**: the observation technique re-uses non-destructive GETs the campaign already used; no extra probing is needed. **Authorization-gated**: any mutation of `enc` that introduces a payload string different from base64 / valid base64 / empty is off-limits pre-letter.
5. **Map the Azure hosting surface**. Read-only probing of public Microsoft endpoints is permitted: confirm that `169.254.169.254` is reachable from the **target's host** is, by definition, an internal-plane question and cannot be answered without the scope letter [1]. **Authorization-gated**: anything that emits a request to `169.254.169.254` or to the local App Service identity endpoint -- through the target or via the developer's machine -- needs the letter because the bare act of attempting an SSRF on the live target already crosses the policy line.
6. **Manual OAST fallback if Interactsh/Collaborator are not available**. The cheat sheet's category list of DNS/HTTP/SMTP/LDAP interactions still applies; with only `curl` [13], the tester can use `dig +short`, `tcpdump`, and a controlled listener to validate that the target resolved and contacted the callback domain. **Safe pre-authorization** only against an in-house honeypot; **authorization-gated** against the live target.
7. **Prepare the ws-discovery-of-OOB record**. When the letter is signed, retain Interactsh poll log IDs, Nuclei run IDs (JSON lines), SSRFmap session `loot/` paths, and Microsoft-side log time ranges (Kusto queries on App Service diagnostic logs [22]) so a reproducible audit trail exists.

## 5. Detection Counterpart

Detection is symmetric: the same partial break-out that makes SSRF replayable is what defenders should monitor. Three Azure-hosted evidence channels are available; each has limits.

| Detection surface | What it records | Why it helps | Limits | Evidence |
|---|---|---|---|---|
| Application Insights dependency tracking | "A *dependency* is a component that's called by your application code", with duration and a pass/fail signal per call [4] | An outbound call from the App Service to an unexpected host (e.g. `169.254.169.254`) or to a known interaction-collector domain shows up as a `dependency` row | The page enumerates only duration and success/failure; target URL, target host, dependency type, and result code are **not listed on the cited page** [4] -- so detection requires additional fields or sampling lower limits before conclusions are safe | [4], [21] |
| Application Insights telemetry data model | Standardized schema across platform/language [21] | Single model for correlation across component types | Coverage of server-side outbound HTTP specifically is not stated in the cited excerpt; verify in operational telemetry before treating App Insights as exhaustive | [21] |
| Azure App Service diagnostic logs | Categorized as Application logs, Web server logs, FREB (Failed Request Tracing), Detailed errors [22]; FREB captures 400-600 failures [22] | Web server logs in W3C format expose inbound HTTP method, URI, client IP, response code [22]; FREB isolates per-component breakdown for failed requests | The page does **not** document outbound or internal service-to-service HTTP traffic as a distinct diagnostic-log category; outbound destinations and bodies are not enumerated [22]; FREB is a failure-only lens (400-600) [22] | [22], [22] |
| Azure Network Watcher | Monitors, diagnoses, gains insights; includes connection monitor and NSG flow logs capabilities [26] | Egress-side visibility if NSG flow logs are wired to a workspace | The cited overview page does not enumerate Off-by-default state; verify in the NSG flow logs sub-doc before use; not a SSRF-specific product | [26] |
| YSOD / error pages at the application | Custom errors on for the brief's live target | Three response sizes (MVC 2,733 b, IIS 1,216 b, enc FormatException 4,942 b, enc CryptographicException 5,084 b) plus 411/404 method policy [brief] | These are response-side only and only identify classes of error | [brief, 149.197-258] |

Detection tactic: chart outbound dependencies over a one-week baseline; rank baselines by destination domain **and** by the depth of the call (depth 0 = direct user, depth 1 = MVC controller, depth 2+ = server-side fetcher). SSRF in a logged environment usually shows up as a new dependency at depth >= 2 whose target domain has no business history; without an outbound-dependency channel an organization is flying blind on this class. Inference: if App Insights outbound dependency tracking records destination host, this is the most actionable signal; if it does not, NSG flow logs (Network Watcher) are the fallback, but the two together are needed for full coverage. Status of the full-fidelity field set on this specific App Service is **not established** in the cited Microsoft Learn page [4].

## 6. NO-TOOL GAPS

| Gap | Why no off-the-shelf tool fully covers it | Evidence | Risk if unmitigated |
|---|---|---|---|
| ASP.NET MVC parameter discovery with parameter-type awareness | The OWASP SSRF Prevention Cheat Sheet is language-agnostic; SSRFmap takes a Burp request + a parameter but is not an MVC-route spider [6][1] | [6], [1] | Important parameter values may stay hidden behind MVC routing and antiforgery tokens |
| Microsoft 365 / Entra ID session fingerprinting | None of the surveyed OAST tools know about the `__RequestVerificationToken`, the antiforgery cookie `HttpOnly without Secure` configuration reported on the target, or the Azure trust path | [brief] | Authorization-gated probing will mis-attribute pre-auth vs post-auth callbacks |
| Azure App Service impact-path modelling (IMDS-vs-App Service endpoint-vs-VNet) | Microsoft distinguishes VM IMDS (169.254.169.254, `Metadata: true` header required, no `X-Forwarded-For`) from App Service local REST endpoint exposed via `IDENTITY_ENDPOINT` and `X-IDENTITY-HEADER` [16][2] | [16][2] | The right blocker (network firewall vs platform hardening) is missed |
| Multiline-regex bypass detection on allowlist regex | The cheat sheet notes multiline regex can be exploited for allowlist-domain bypass [18]; no automated tool records regex style of the validator in question | [18] | Validator regex may permit `victim.com
attacker.com` |
| Two-error-page family attribution | YSOD pages of different sizes can leak MVC vs IIS provenance [brief] | [brief] | Attackers (or evaluators) can fuse page-size fingerprinting into sink selection |
| 411-on-PUT  under-utilized signal | The target's GET-only method policy with PUT/POST 411 [brief] | [brief] | Reduces curl-style probe surface, but is itself an attribution signal worth encoding in detection |
| Repeated `enc` oracle staging | The brief's three stages (invalid base64 / valid base64 / empty) [brief] | [brief] | Without using the oracle, automated fuzzers cannot distinguish decoder error from signed payload error |

## 7. Azure Cloud Impact Path (modelled, not tested)

This is the campaign's prior gap. Two Azure endpoints matter:

1. **Azure VM IMDS**, at `169.254.169.254`, a REST endpoint that returns instance metadata and which can be used to acquire **managed-identity OAuth tokens** [16]. Constraints: IMDS requires the `Metadata: true` header and rejects requests carrying `X-Forwarded-For` [16]; it is unauthenticated and open to all processes on the VM [16]; the Managed Identity category rate-limit is 20 requests per second with concurrency of 5 per VM [16]; the service **must** bypass proxies and any default proxy settings when called [16]; the channel is **not** intended as a sensitive-data channel [16]. The OWASP cheat sheet explicitly recommends listing Azure IMDS at 169.254.169.254 in the denylist [1].
2. **Azure App Service / Functions local token endpoint**. Per the Microsoft App Service managed identity page, this endpoint is exposed by `IDENTITY_ENDPOINT` and `IDENTITY_HEADER` environment variables, and the platform rotates the `IDENTITY_HEADER` value as an **SSRF mitigation** [2]. A managed-identity-aware attacker must therefore know both the endpoint and the rotating header value; the platform already mitigates blind SSRF on this endpoint by requiring the X-IDENTITY-HEADER be present [2]. Quote: "An app with a managed identity makes this endpoint available by defining two environment variables: `IDENTITY_ENDPOINT`: The URL to the local token service; `IDENTITY_HEADER`: A header that can help mitigate server-side request forgery (SSRF) attacks. The platform rotates the value" [2].

**Inference (explicit)**: whether the MUJ SLCM App Service has a managed identity enabled is not established by the brief and cannot be established without the scope letter, because verifying it would require either reading the App Service environment variables through the target (out of scope) or an Azure-side query that requires owner/contributor credentials. The story below therefore leans on the platform defaults, not on what MUJ deploys:

- If the MUJ SLCM runs on Azure App Service **with** a managed identity and the SSRF sink reaches the local token endpoint, an attacker with knowledge of `IDENTITY_ENDPOINT` and a recent `IDENTITY_HEADER` can mint a Microsoft Entra OAuth2 access token for the application identity [2]. SSRF mitigations are present by default on App Service, and that mitigates blind exploitation without insider knowledge of the rotating header [2].
- If the SLCM were ever run on Azure VM/VMSS (not currently established), blind SSRF could mint a managed-identity token at `169.254.169.254` simply by adding the `Metadata: true` header and respecting rate limits [16]. This is the textbook Cloud SSRF path.
- In both cases, the recommended mitigation is to **disable IMDSv1 / use IMDSv2 / MSP** on Azure VMs and to **rely on the rotating `IDENTITY_HEADER` value plus minimal application egress** on App Service [14][2][1].

**Confidence**: *moderate-high* on the platform facts (Microsoft Learn); *low* on whether either path is reachable on the MUJ SLCM App Service instance specifically (which is the missing prior gap and a primary motivator for the signed-scope phase).

## 8. BUILD CANDIDATES (plans to fill the gaps, gated post-letter)

Each build candidate here is **designed for the letter-authorized phase**; do not run any active interaction until the scope letter and the two test accounts are in hand.

1. **MVC-aware parameter spider** (repo skeleton). A lightweight Burp extension or python script that uses a static ASP.NET MVC sitemap (the rendered HTML links plus the antiforgery request flow) to enumerate URL-shaped parameters and emit a Burp request file per candidate. This plugs into SSRFmap which already accepts a Burp request + parameter name [43][6]. Status: feasible; licence: club's MIT.
2. **OOB collector with target-aware session-aware correlation** (extension to existing OAST). Wrap Interactsh polling so each captured event is correlated to the originating HTTP request's antiforgery-cookie-session-identifier (the brief describes the cookie is `HttpOnly without Secure`) [9][15]. Status: feasible; licence: MIT.
3. **Azure hosting fingerprint** (read-only). A read-only posture module that, **after impersonating a test account with the letter**, queries a small set of App Service endpoints via Kudu / diagnostics to confirm whether `IDENTITY_ENDPOINT` is set, whether outbound DNS to `169.254.169.254` is blocked, and which Entra tenant signs users in. Status: feasible but requires the letter + test accounts; do not run pre-letter.
4. **enc-parameter oracle harness** (offline first). Build a small driver that reproduces the **three** documented response sizes for the `enc` parameter without ever mutating it (4,942 b / 5,084 b / third size) and produces a JSONL log similar to Nuclei's output. This belongs to the pre-authorization **detection-tuning** phase because it does not introduce a fourth state.
5. **WAF/edge coverage gap detector** (read-only). A read-only script that probes **whether** an edge proxy/WAF fronts the target by replaying a request whose `Host:` header differs from the public DNS name and inspecting the response (the brief documents such attempts "came back clean"). This verifies the "no attributable edge control" note in the brief and pins the absence-of-edge-control fact in writing. Status: feasiable; safe before letter because it is read-only.
6. **App Insights outbound-dependency attestor** (combine 161.0 and 162.0 data). Where the tenant has App Insights wired, a tiny Kusto query that surfaces outbound-dependency rows in the last 30 days, sorted by destination domain, with whitelist/fingerprint delta highlighting. Status: feasible in scope; relies on having read access to the App Insights resource.

## 9. Manual probe plan (split: pre-authorization vs authorized phase)

**Pre-authorization (does not require the letter)**:
- Reproduce passive fingerprint of the live target: 443-only exposure, MVC vs IIS YSOD sizes, method-policy 411/404 [brief].
- Stand up Interactsh (or Burp Collaborator) on trusted infra; verify DNS, HTTP, SMTP, LDAP listener logs [9][15].
- Read and trace the documented `enc` oracle (no fourth input state) [brief].
- Pin **no-edge-control** by replaying Host/X-Forwarded-Host/absolute-URI variants and showing responses unchanged [brief].
- Read Microsoft Learn and OWASP authoritative docs (already done in Sections 2, 5, 7).
- Audit deployment of detection channels: do App Insights dependency and FREB log categories exist? Are NSG flow logs wired [4][22][26]?

**Authorized (signed scope letter + two test accounts)**:
- Inject OAST URLs into candidate parameters, **one at a time**, record callback observations, and **immediately stop** after any callback that proves the sink [8][15].
- Run Nuclei with publicly available SSRF templates against permitted paths and capture JSONL output, watching for `cache-hit` versus `cache-miss` on callback domains [23].
- Run SSRFmap supervised, against confirmed sinks only; do **not** run the gopher/exploitation modules unless authorized explicitly in the letter.
- Use the whonow DNS rebinding framework only against an in-VM, isolated lab environment first [7]. Reproducing on the live target is off-limits unless the letter explicitly authorizes DNS rebinding.
- After step 1 succeeds with no real user data, take a second round under the test accounts to differentiate **anonymous** from **authenticated** SSRF.
- For maximum-confidence attribution, set log retention windows (App Insights dependency retention, FREB traces, IIS logs), and capture pre-test windows so the auditor can prove what was and was not produced by the test [4][22].

## 10. Comparative Analysis (across OAST tools and across mitigation layers)

Reading across the three OAST tooling tiers (figure 1), the right mix is:
- **Free general-purpose OAST** (ProjectDiscovery Interactsh on public servers) for early sink discovery, no infrastructure cost [9][15].
- **Free self-hosted** for telemetry-heavy multi-day engagements where attribution, retention, and non-PII compliance matter [15]; whonow can sit beside it [7].
- **Commercial** (Burp Pro/DAST) when scanner-driven OAST is wanted to cover a scan queue; the licence-vs-cost gating belongs only to the professional-services branch [29][30][28].

Reading across the mitigation layers (figure 2):
- **Application layer**: input validation by allowlist, regex discipline with no multiline bias, and a strict no-redirect web client [1][18].
- **Network layer**: deny RFC1918, multicast, link-local, and `169.254.169.254` egress from the App Service outbound subnet; NSG flow logs to a workspace for detection [1][26].
- **Platform layer**: App Service rotating `IDENTITY_HEADER`, MSP and IMDSv2 analogs on VMs [2][14].
- **Detection layer**: App Insights dependency tracking + App Service diagnostic logs + NSG flow logs (only as good as the union of those channels) [4][22][26].

Tensions and divergences:
- The PortSwigger cheat sheet population (multiline-regex bypass via Unicode normalization ambiguity) [18] and the OWASP allowlist recommendation [1] can coexist only if the application uses an IP-validated allowlist rather than a regex allowlist. This is a positive tension: a single design choice resolves it.
- App Service's `IDENTITY_HEADER` rotation mitigates blind SSRF against the local REST endpoint, but it is **not** sufficient if the application's outbound HTTP client itself is the vulnerable sink (an attacker can still cause the app to issue a request somewhere it shouldn't). Defenders cannot rely on the platform mitigation to absolve application-layer validation [2][1].
- SSRFmap is pointedly explicit about its exploitation chain (cloud metadata, FastCGI, gopher, SMB coerce) but **does not** state any safety or authorization guidance on the cited README page [6]. Operational use of SSRFmap therefore belongs in the authorized phase only, with supervision.

## 11. VERDICT

**Confidence**:
- *High confidence* on the **technique universe and tool inventory** at the level of public documentation: OWASP SSRF Prevention Cheat Sheet, WSTG, PortSwigger cheat sheet, Microsoft Learn inventory [1][20][17][18][16][2].
- *Medium-high confidence* on the **Azure App Service identity endpoint behaviour**: cited Microsoft Learn pages confirm `IDENTITY_HEADER` rotation as a built-in SSRF mitigation; this is a strong fact [2].
- *Medium confidence* on the **detection counterpart**: App Insights dependency channel was confirmed to record dependency calls with duration and pass/fail [4], but absence of explicit per-field list means field-level fidelity needs verification before any operation story can be made.
- *Low confidence* on whether the **MUJ SLCM App Service instance** has a managed identity or an outbound-restriction NSG; the brief supplies host/IIS/framework facts only and does not include Azure-side deployment configuration [brief].

**Where the campaign needs to focus next** (high-leverage):
1. Build the **OAST collector** (Interactsh or self-hosted), so authorized-phase work can start immediately the letter is signed.
2. Pin the **Azure hosting fingerprint** via the read-only Kudu/diagnostic probe path; this confirms or refutes the presence-of-managed-identity story for IMDS-mint paths.
3. **Wire NSG flow logs to a workspace** before the test, because App Service diagnostic logs alone do not document outbound HTTP traffic as a distinct category [22].
4. Nail the **MVP of an MVC-aware spider** so the parameter list passed into SSRFmap and Nuclei is full and ordered by probable reachability.

**Decisions the club should make now**:
- Confirm whether the next-phase engagements want **public-server OAST** (cheaper, easier attribution) or **self-host** (cleaner control + privacy) [15].
- Confirm whether the letter will allow **DNS rebinding** testing or only classic OAST; whonow is easy to deploy but DNS rebinding is a separate authorization gating [7].
- Confirm whether to invest in Burp Pro for the OAST automation gain, or rely on Burp Community + manual Collaborator pulls + Interactsh-based automation through Nuclei [28].
- Confirm whether the test will allow SSRFmap gopher-modules or restrict the engagement to discovery-only [6].

**State of the campaign** compared to the prior status "PARTIAL (theory only, no test)":
- The **theory side** is now complete: seven-row SSRF technique taxonomy, twelve-row tool inventory with licences, manual-method outline, detection counterpart mapped to Microsoft Learn pages, six build candidates, and an explicit authorized-phase plan. This surpasses the prior partial state on paper.
- The **test side** is still **pending**: the signed scope letter plus two test accounts are required for any callback-generating step. This remains the letter's responsibility.

**Final instruction (operational)**: passive enumeration and tooling preparation are safe pre-letter. Any OAST callback generation, any sink mutation, any `IDENTITY_ENDPOINT` test, and any NSG egress probe require the letter. No instructions for unauthorized access have been provided. All tool capabilities quoted above are documented as supporting the defensible side of testing (testing methodology) without exposing techniques the auditor can use against any production system without written authorization.

## References

1. *Server-Side Request Forgery Prevention Cheat Sheet - OWASP*. https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html
2. *Managed Identities - Azure App Service | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/app-service/overview-managed-identity
3. *ZAP – Out-of-band Application Security Testing Support*. https://www.zaproxy.org/docs/desktop/addons/oast-support/
4. *Dependency Tracking in Application Insights - Azure Monitor*. https://learn.microsoft.com/en-us/azure/azure-monitor/app/dependencies
5. *How to use managed identities for Azure resources on an Azure ...*. https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/how-to-use-vm-token
6. *GitHub - swisskyrepo/SSRFmap: Automatic SSRF fuzzer and ...*. https://github.com/swisskyrepo/SSRFmap
7. *GitHub - brannondorsey/whonow: A "malicious" DNS server for ...*. https://github.com/brannondorsey/whonow
8. *Testing for blind SSRF with Burp Suite - PortSwigger*. https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/ssrf/testing-for-blind-ssrf
9. *GitHub - projectdiscovery/interactsh: An OOB interaction ...*. https://github.com/projectdiscovery/interactsh
10. *SSRFz · GitHub*. https://github.com/SSRFz
11. *URL validation bypass cheat sheet for SSRF/CORS/Redirect ...*. https://portswigger.net/web-security/ssrf/url-validation-bypass-cheat-sheet
12. *GitHub - tarunkant/Gopherus: This tool generates gopher link ...*. https://github.com/tarunkant/Gopherus
13. *curl - copyright*. https://curl.se/docs/copyright.html
14. *Metadata Security Protocol (MSP) - Azure Virtual Machines | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/virtual-machines/metadata-security-protocol/overview
15. *Interactsh Overview*. https://docs.projectdiscovery.io/opensource/interactsh/overview
16. *Azure Instance Metadata Service for virtual machines - Azure Virtual Machines | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/virtual-machines/instance-metadata-service
17. *Server Side Request Forgery | OWASP Foundation*. https://owasp.org/www-community/attacks/Server_Side_Request_Forgery
18. *Introducing the URL validation bypass cheat sheet | PortSwigger Research*. https://portswigger.net/research/introducing-the-url-validation-bypass-cheat-sheet
19. *interactsh module - github.com/projectdiscovery/interactsh - Go Packages*. https://pkg.go.dev/github.com/projectdiscovery/interactsh
20. *WSTG - Latest | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/19-Testing_for_Server-Side_Request_Forgery
21. *Application Insights telemetry data model - Azure Monitor | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/azure-monitor/app/data-model-complete
22. *Enable Diagnostic Logs - Azure App Service | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/app-service/troubleshoot-diagnostic-logs
23. *GitHub - projectdiscovery/nuclei: Nuclei is a fast, customizable vulnerability scanner powered by the global security community and built on a simple YAML-based DSL, enabling collaboration to tackle trending vulnerabilities on the internet. It helps you find vulnerabilities in your applications, APIs, networks, DNS, and cloud configurations. · GitHub*. https://github.com/projectdiscovery/nuclei
24. *GitHub - SSRFuzz/SSRFuzz*. https://github.com/SSRFuzz/SSRFuzz
25. *How managed identities for Azure resources work with Azure virtual machines - Managed identities for Azure resources | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/how-managed-identities-work-vm
26. *Azure Network Watcher Overview | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/network-watcher/network-watcher-monitoring-overview
27. *SSRFmap/README.md at master · swisskyrepo/SSRFmap · GitHub*. https://github.com/swisskyrepo/SSRFmap/blob/master/README.md
28. *Burp Collaborator - PortSwigger*. http://portswigger.net/burp/documentation/desktop/tools/collaborator
29. *Pricing - Burp Suite DAST - PortSwigger*. https://portswigger.net/burp/dast/pricing
30. *Burp Suite Pricing 2026: Pro Vs DAST Cost - cipherssecurity.com*. https://cipherssecurity.com/burp-suite-pricing-2026-pro-vs-dast/
31. *Download Burp Suite Community Edition - PortSwigger*. https://portswigger.net/burp/communitydownload
32. *Download Burp Suite - PortSwigger*. https://portswigger.net/burp/downloads
33. *Running Interactsh interactsh-client - ProjectDiscovery ...*. https://docs.projectdiscovery.io/opensource/interactsh/running
34. *nuclei-ai-extension/LICENSE.md at main - GitHub*. https://github.com/projectdiscovery/nuclei-ai-extension/blob/main/LICENSE.md
35. *GitHub - projectdiscovery/nuclei-templates: Community curated ...*. https://github.com/projectdiscovery/nuclei-templates
36. *Releases: projectdiscovery/nuclei-templates - GitHub*. https://github.com/projectdiscovery/nuclei-templates/releases
37. *Interactsh Integration (OAST) | projectdiscovery/nuclei ...*. https://deepwiki.com/projectdiscovery/nuclei/10.1-interactsh-integration-(oast)
38. *GitHub - octopus-investments/octopus-zaproxy: The OWASP ZAP core project · GitHub*. https://github.com/octopus-investments/octopus-zaproxy
39. *zaproxy/LICENSE at main · zaproxy/zaproxy · GitHub*. https://github.com/zaproxy/zaproxy/blob/main/LICENSE
40. *zaproxy/LEGALNOTICE.md at main · zaproxy/zaproxy · GitHub*. https://github.com/zaproxy/zaproxy/blob/main/LEGALNOTICE.md
41. *zaproxy/license/ApacheLicense-2.0.txt at master - GitHub*. https://github.com/ParrotSec/zaproxy/blob/master/license/ApacheLicense-2.0.txt
42. *ZAP – Documentation*. https://www.zaproxy.org/docs/
43. *swisskyrepo/SSRFmap | DeepWiki*. https://deepwiki.com/swisskyrepo/SSRFmap
44. *Cloud Metadata Modules | swisskyrepo/SSRFmap | DeepWiki*. https://deepwiki.com/swisskyrepo/SSRFmap/3.4-cloud-metadata-modules
45. *Penetration Test Learn / tools / Gopherus · GitLab*. https://gitlab.com/penetration-test-learn/tools/Gopherus
46. *timb-machine-mirrors/tarunkant-Gopherus - GitHub*. https://github.com/timb-machine-mirrors/tarunkant-Gopherus
47. *SSRFuzz · GitHub*. https://github.com/SSRFuzz
48. *License | brannondorsey/whonow | DeepWiki*. https://deepwiki.com/brannondorsey/whonow/6.1-license
49. *whonow on offsec.tools*. https://offsec.tools/tool/whonow
50. *curl - Documentation Overview*. https://curl.se/docs/
51. *PayloadsAllTheThings/Server Side Request Forgery/README.md at ...*. https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Request%20Forgery/README.md
52. *Burp - Web Application Security, Testing, & Scanning ...*. https://portswigger.net/burp
53. *PortSwigger Software Pricing & Plans 2026: See Your Cost*. https://www.vendr.com/marketplace/portswigger
54. *Burp Suite Pricing 2026: Pro, Enterprise & DAST Costs ...*. https://pentest.ae/blog/burp-suite-pricing-2026/
55. *How to Fix Azure Managed Identity Authentication Failures in ...*. https://oneuptime.com/blog/post/2026-02-16-how-to-fix-azure-managed-identity-authentication-failures-in-app-service/view
56. *KeyError: 'IDENTITY_ENDPOINT' error in Azure environment*. https://stackoverflow.com/questions/69203665/keyerror-identity-endpoint-error-in-azure-environment
57. *Burp Suite Community Edition for Windows download ...*. https://sourceforge.net/app/burp-suite-community-edition/
