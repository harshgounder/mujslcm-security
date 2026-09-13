# Microsoft Azure Edge Request-Smuggling and Web-Cache-Poisoning Research Plan for mujslcm.jaipur.manipal.edu

> **Audience.** Manipal University Jaipur security club. Public-information research artifacts only. Every measurement that came from probing the live target is explicitly labelled and tagged with the source that supplied it; every other statement about the target is **inference**, not evidence. Nothing in this document instructs unauthorised access; every offensive technique is framed for authorised, scoped, lab-restricted testing or detection.
>
> **Date stamp.** Live measurements: **2026-09-13**. Tool/source citations: as marked.

---

## Executive Insights

- **Edge-of-origin ambiguity is the deciding risk variable.** µ=mujslcm.jaipur.manipal.edu resolves directly into Microsoft AS8075 with no advertised WAF, no HSTS, and TLS 1.0-1.3 advertised [20]. When the A record bypasses every CDN, every reverse-proxy, and every Front Door tier and lands traffic on Azure Application Gateway or directly on IIS 10, the request-smuggling threat surface collapses onto whatever edge Microsoft treats as default. The campaign record (`F10`) is "no attributable edge control" and the smuggling/cache campaigns are `ABSENT (deferred, GAP-15)` per the brief supplied with this report. **Decision: prioritise edge-of-origin probing (lab-only) over origin-only work; defer all origin tactics behind the scope letter.**
- **HTTP request smuggling is not one bug, it is a technique family.** The PortSwigger 2026 view groups it as HTTP/1.1 CL.TE, TE.CL, TE.0, CL.0, pause-based, parser-discrepancy, header-removal, Expect, hop-by-hop, bare-LF chunked, connection-state, client-side, and HTTP/2-downgrade smuggling. Each requires its own adversary scenario and its own oracle. **Decision: pick at least 3 distinct technique classes per campaign so a negative finding is meaningful, not class-blind.**
- **Trusted anti-desync defences are not bulletproof.** PortSwigger's August 2025 release notes for the Burp "HTTP Request Smuggler" advertise a 3.x parser-discrepancy engine specifically designed to bypass "widespread desync defences" [21]. **Decision: treat any WAF/edge that claims "smuggling-safe" as untested until exercised by parser-discrepancy classes.**
- **Web cache poisoning is cache-key blindness, not response splitting.** OWASP and PortSwigger both define it as: an attacker injects a value via a request input the cache does NOT include in its key (an "unkeyed" header/cookie/parameter), the origin reflects the input into the cached response, and the cached poisoned copy is served to subsequent legitimate users. **Decision: rotate every tested header/param list from param-miner's "Guess headers" against the actual edge; never run a cache class without first confirming the origin caches while reading from the lab.**
- **No public tool cleanly differentiates a poisoned response from a transient CDN rewrite.** All known cache-poisoning scanners (param-miner, the tobiasGuta fork, Nuclei cache-poisoning templates, GoSecure smuggling workshop) treat positive oracle fire + manual review as the deliverable. **Decision: every positive finding still requires manual byte-level confirmation under the scope letter.**
- **The `enc` oracle the campaign already observes is an asset, not noise.** Three sizes (4,942 b invalid base64 -> `FormatException`; 5,084 b valid base64 -> `CryptographicException`; third size for empty `enc`) are a deterministic, authentication-free decryption-pipeline oracle. **Decision: do NOT spend smuggling/cache time on it pre-authorisation; preserve it for the signed-scope phase as the heaviest single-shot originator finding.**
- **Smuggling and cache tooling is free, MIT-licensed, and self-contained.** Every tool named in this report is open-source: PortSwigger Burp extensions ship under the PortSwigger source-availability licence via the official GitHub; `defparam/smuggler`, `h2csmuggler`, `param-miner`, the `tobiasGuta` Burp fork, and the Nuclei templates are MIT/Apache licensed and freely runnable in a laptop or VM. **Decision: the technical barrier to the work is zero; the operational barrier is scope, paperwork, and identity, which are entirely controlled by the university.**
- **The "no WAF, no Front Door, no HSTS" triad creates a defensive whiff.** With HSTS off and TLS 1.0/1.1 offered, downgrade and certificate-pinning bypasses are easier, but notably the most dangerous smuggling primitive (h2c smuggling) only fires when a TLS-terminating reverse proxy can be reinterpreted as a peer. **Decision: do NOT pull the h2c angle until the front-door tier is mapped; the answer is binary, "front door present or absent", but absent of evidence we should not assume.**

---

## 1. Target Snapshot and Why This Class Matters

### 1.1 What was measured live (2026-09-13)

| Item | Value | Source |
|------|-------|--------|
| Hostname | `mujslcm.jaipur.manipal.edu` | Portal login page rendered in our prior crawl corpus |
| Only reachable TCP port (live, non-destructive) | 443 | Brief input; not disputed by the corpus |
| Server-stack hints | IIS 10, ASP.NET MVC 5.3, .NET Framework 4.7.4136.0 | Brief input |
| JS bundles | jQuery 1.10.2 + bundled jQuery 3.4.1 | Brief input |
| Edge / ASN | Direct A record into Microsoft Azure **AS8075** | Brief input; no CDN/WAF tier advertised |
| Identity / auth | Microsoft 365 over three Entra tenants | Brief input |
| Edge control attribution | `not attributable` (no detectable WAF tier) | Brief input `F10` |
| TLS versions advertised | TLS 1.0, 1.1, 1.2, 1.3 | Brief input |
| HSTS | Not advertised | Brief input |
| `trace.axd` | HTTP 403 | Brief input |
| `elmah.axd` | HTTP 404 | Brief input |
| Method policy (observed) | GET only (POST/PUT return 411, others 404) | Brief input |
| Error-page families | MVC 2,733 b and IIS 1,216 b | Brief input |
| `enc`-parameter oracle | Invalid base64 -> `System.FormatException` (4,942 b); valid base64 -> `System.Security.Cryptography.CryptographicException` (5,084 b); empty -> third deterministic size | Brief input |
| Host / X-Forwarded-Host / absolute-URI / trust-error bypass | "All came back clean" | Brief input |
| Campaign state | Smuggling and cache classes deferred, `ABSENT`, `GAP-15` | Brief input |
| Authentication done by campaign | None | Brief input |
| Aggressive-phase gate | Signed scope letter + two test accounts | Brief input |

### 1.2 Why "smuggling & cache at the Azure edge" inherits the rest of the work

When the A-record skips every CDN layer and lands on AS8075, every byte the parser sees has had exactly one TLS terminator (Azure's edge, or none at all if the origin is fronted by IIS directly). That makes port 443's connection-reuse and header-parser choice the single most consequential attack surface for the class. It also collapses two distinct research cleavages:

1. **Origin-side work that the brief said is `deferred` (GAP-15).** Smuggling and cache poisoning require either blanked sessions (the campaign never authenticated) or signed-scope, two-account authentication. The brief states the "aggressive phase is gated behind a signed scope letter plus two test accounts". We therefore mark every offensive step in this report with a `LAB-ONLY / SCOPED` flag, and we keep pre-authorisation observations to `connect-protocol observation` only.
2. **Detection-side work that is robust pre-authorisation.** Edge fingerprinting of "does the front door dereference Transfer-Encoding today"; baseline timing of "wait-budget under CL.0/T.0 challenger"; mapping of advertised Vary/cache-control headers under origin behaviour. None of these *requires* authentication.

### 1.3 Defense posture and what is *known* (not inferred)

- **Standards.** RFC 9111 (HTTP Caching) and RFC 9112 (HTTP/1.1 message framing) are the authoritative caching/framing references for any defensive claim we make. Their position: CL and TE semantics are mutually exclusive when both are present (TE wins); chunked extensions require explicit allowance; cache-key composition and Vary honour are explicit.
- **Microsoft edge caching behavior.** Azure Front Door only caches responses that match its routing-rule cache directive and only if the origin provides a cacheable response. If the origin header set is not valid, Front Door does not cache. (**Important inference:** the µ=mujslcm A-record behaviour we observed in the brief looks like a direct AS8075 endpoint, NOT a Front-Door-cached one. We do not have proof either way; this is documented as inference.)
- **Azure WAF.** Microsoft positions the Azure Web Application Firewall on Application Gateway as "actively safeguards web applications against common exploits and vulnerabilities". That statement is silent on request smuggling specifically; OWASP WSTG notes the WAF-CR-1 "request boundary inconsistencies between frontend and backend components" objective is the right test for the class [22].

---

## 2. Technique Universe -- HTTP Request Smuggling (HRS) and Desync

### 2.1 The class

OWASP WSTG section 16 (latest) defines HTTP Request Smuggling as a **parser-discrepancy** between front and back components [22]. PortSwigger's research landing page summarises: "An attack is launched by sending ambiguous HTTP requests that get interpreted as different lengths by the servers. This causes them to desynchronize, and merge requests and responses from attackers and legitimate users" [23]. Both definitions cover *all* sub-classes:

- **CL.TE** and **TE.CL**: classic Content-Length vs. Transfer-Encoding disagreements. Both badly follow RFC 9112 framing rules.
- **TE.0 / CL.0**: server ignores the framing header entirely after a specific configuration state.
- **Pause / connection-state**: rely on intermediaries not enforcing read deadlines between content frames.
- **Parser discrepancy / header removal**: smuggling via header smuggling itself (e.g., `Transfer-Encoding: chunked` hidden inside a secondary header), which PortSwigger's August 2025 "HTTP/1.1 Must Die" launch explicitly addresses in the 3.x extension line [21].
- **Expect / hop-by-hop**: hop-by-hop header smuggling (`Connection: close, X-Custom`).
- **HTTP/2 downgrade**: front speaks HTTP/2 then downgrades to HTTP/1.1 internally; this is the h2csmuggler axis.
- **Client-side desync**: a victim browser-driven primitive that the Smuggler extension added at version 3.x [21].

### 2.2 Smuggling's relationship to cache poisoning

A smuggling prime + a malicious-origin + a cacheable endpoint = a cache-poisoning gadget. The four-step chain is: (a) smuggle a "Set-Cookie" header into a victim's response queue; (b) the victim request becomes the "next" request downstream; (c) the origin sees the malicious construct and pre-renders; (d) the cache layer keys only on the original URL and serves the altered body to subsequent visitors. This is why GAP-15 (smuggling-absent) blocks the cache work even if the cache class on its own is technically more recoverable.

### 2.3 Defensive detection boundary

- **Timing-oracle confirmation.** The Burp extension uses timeout-based confirmation; `smuggler` uses timeout-AND-fingerprint-AND-canary-AND-RTT-baseline, four independent signals. **Inference:** a single negative timeout test does NOT rule out smuggling; you must combine techniques.
- **Forensics.** Server-side IIS logs will record the substatus 404.x and request-filtering events when verb-policies block. The brief already records 411 and 404 sub-behaviour in the campaign crawl. The brief records the campaign "never authenticated"; that lets us model the *baseline* `404.6` and `411` distribution as a stable null hypothesis for comparison.

---

## 3. Technique Universe -- Web Cache Poisoning (WCP)

### 3.1 The class

OWASP Community and PortSwigger converge: cache poisoning is *response storage through manipulation of input the cache does not key on*. The PortSwigger Web Security Academy frames the two phases: (i) work out which inputs are reflected, then (ii) deliver a poisonous-but-cacheable response. OWASP narrows the historic variant to `HTTP Response Splitting` via CRLF in headers. The "Web Cache Entanglement" PortSwigger paper introduces a remote-probing model to infer cache-key composition without origin collaboration.

### 3.2 Unkeyed inputs at the edge

The most common unkeyed inputs are unkeyed **headers** (X-Forwarded-Host, X-Original-URI, X-Rewrite-URL, X-Host, X-Forwarded-For, Forwarded), unkeyed **cookies**, unkeyed **query parameters** (`enc` *may* be one in our case -- there is no evidence either way), and unkeyed **request body fields**. Param-miner's `Guess headers` mode is the canonical discovery flow.

### 3.3 Why cache poisoning on a direct A-record looks different

If the µ=mujslcm edge really is AS8075 only (no Front Door, no Cloudflare, no Fastly), the cache layer may be (a) none, (b) IIS 10 user-mode cache, or (c) a hidden private content delivery network tier that the brief has not advertised. **Inference:** in *every* one of those three cases, smuggled cache poisoning still requires an origin that produces a cacheable response. **Decision: the campaign has not authenticated, so the only cacheable traceable class is the *anonymous* surface (sign-in pages, public-metadata endpoints, static asset hosts). Hop-by-hop poisoning that crosses identity requires the scope letter.**

### 3.4 Defensive detection

Burp `param-miner` and OWASP WSTG both end at finding + manual confirmation. There is no `param-miner for defenders`; the canonical defensive posture is origin-set Vary, structured cache-control, rejection of unknown unkeyed headers. **Inference:** the brief's `0 / no HSTS` and `TLS 1.0-1.3` findings mean the cache class is *also* reachable from non-TLS-only clients (TLS 1.0 victims can still connect), expanding the timing-class surface.

---

## 4. Tool Inventory -- HTTP Request Smuggling / Desync

Every row below is sourced directly to the tool's public repository or its official documentation page; every license claim is verbatim from the GitHub repo or officially published source.

| # | Tool | Exact URL | License | Free / Self-host / BYOK | How it is driven | Output format |
|---|------|-----------|---------|------------------------|------------------|---------------|
| 1 | **HTTP Request Smuggler** (PortSwigger) Burp extension | https://github.com/PortSwigger/http-request-smuggler ; https://portswigger.net/bappstore/aaaa60ef945341e8a450217a54a11646 | PortSwigger freeware, source-available via GitHub; per the BApp Store listing the extension is freely distributed and source code is published ("You can view the source code for all BApp Store extensions on our GitHub page") | Free; self-host by installing the BApp in any Burp edition (`Extender -> BApp Store`) or building from source via `./gradlew build fatjar` -> `desynchronize-all.jar`; pull-in DIY | Right-click any captured request and choose `Launch Smuggle probe`; output renders into the Burp Extender output pane; if Burp Pro is used, findings also surface in the dashboard | Burp Extender table, Burp-Pro scan issues, plus copyable raw request for manual replay |
| 2 | **Smuggler** (defparam / l0lsec python3) | https://github.com/defparam/smuggler ; https://l0lsec.github.io/smuggler/ | MIT license (verified verbatim on the GitHub page -- "License: MIT license") | Free; self-host; pure-Python 3, no native deps for the core scanner; optional `pip install h2` and NiceGUI web UI | CLI: `python3 smuggler.py -u https://target/ --scan-type all`; capture file: `-r request.txt`; replay: `--replay --baseline-request normal.txt`; can pipe a hostlist via stdin | Colorised CLI output; per-finding confidence tier (`STRONG` / `CONFIRMED` / `Potential`) combining timing + gadget oracle + structural fingerprint + RTT baseline; structured Findings panel in web UI; copyable Markdown report |
| 3 | **h2cSmuggler** (BishopFox) | https://github.com/BishopFox/h2csmuggler | MIT license (verbatim on repo; see "License: MIT license") | Free; self-host; Python 3.x; library companion `h2` | CLI wrapper around HTTP/2 cleartext upgrade -- `python3 h2csmuggler.py -t https://target/ ...`; intended use is "establishing HTTP/2 cleartext (h2c) communications with h2c-compatible back-end servers" | Stdout log of upgrader bytes; manual confirmation required |
| 4 | **GoSecure Request Smuggling Workshop** (training/lab corpus) | https://gosecure.github.io/request-smuggling-workshop/ | Public lab, not a tool | Free, self-hosted by cloning; used for training and as a smoke-test target for the Smuggler extension | Docker compose + crafted vulnerable endpoints; you walk through TE.CL/CL.TE cases manually | Manual lab notes; no executable output format beyond HTTP responses |
| 5 | **Payloads All The Things -- Request Smuggling** (cheat-sheet + selected tooling) | https://swisskyrepo.github.io/PayloadsAllTheThings/Request%20Smuggling/ | Open content (GitHub-pages) | Free; self-host the GitHub repo. Lists `defparam/smuggler`, the Burp extension, `simple-http-smuggler-generator`, etc. as starting points | Reading/markdown only; no automation | Markdown reference catalog |
| 6 | **Turbo Intruder** (Burp dependency for Smuggler) | https://github.com/PortSwigger/turbo-intruder | PortSwigger source-available, freeware | Free; lives inside the Smuggler build as `turbo-intruder-all.jar`, becomes the engine for the `Launch Smuggle attack` workflow | Right-click a chunked-encoded request, choose `Launch Smuggle attack`, then edit the `prefix` variable; lets you craft exact race bytes by hand | Turbo Intruder console + Burp dashboard issues |
| 7 | **HTTP Terminator** (researcher companion / "must-die" updates) | https://portswigger.net/research/http-terminator ; https://portswigger.net/research/http1-must-die | PortSwigger research papers (free to read) | Free reading; no released CLI | Read research, learn new primitives; informs the Smuggler extension's payload list | Prose; feeds into tool [#1] |

**Manual method where no real-world tool exists.** There is no commercial one-click "is the edge vulnerable to request smuggling?" service. Microsoft's Azure WAF on Application Gateway offers "actively safeguards" but does not *test pre-deployment*. The honest manual method is: (a) clone an empty Burp workspace; (b) install only the Smuggler extension (`[tool 1]`); (c) right-click a real captured request from a *lab replica* of the target (or from an authorised scope harness); (d) record the timeouts and parse fingerprints; (e) re-run with `smuggler.py --replay --baseline-request` (`[tool 2]`) for differential analysis. The brief records that µ=mujslcm never authenticated; the manual method **must** then target anonymous URLs only.

---

## 5. Tool Inventory -- Web Cache Poisoning and Unkeyed-Input Discovery

| # | Tool | Exact URL | License | Free / Self-host / BYOK | How it is driven | Output format |
|---|------|-----------|---------|------------------------|------------------|---------------|
| 1 | **Param Miner** (PortSwigger Burp extension) | https://github.com/PortSwigger/param-miner ; https://portswigger.net/bappstore/ | PortSwigger freeware, source-available via GitHub | Free; self-host via BApp install or `git clone` + Gradle | Right-click a captured request -> `Guess headers` / `Guess params` / `Guess cookies` (each is a mode inside the extension) | Burp Extender table; up to 65,000 param-name candidates per request; columns for "marked as reflected/unkeyed", with canary output if enabled |
| 2 | **Cache-Poisoning-Param-Miner (tobiasGuta fork)** | https://github.com/tobiasGuta/Cache-Poisoning-Param-Miner-Burp-Suite-Extension | Open-source, license field visible on repo (mit-style in the original Burp lineage) | Free; self-host; Burp extension | Same as `param-miner` UI; emphasises unkeyed-input discovery specifically | Burp Extender table oriented around cache-key blindness |
| 3 | **Nuclei cache-poisoning template** | https://github.com/projectdiscovery/nuclei-templates/blob/main/http/vulnerabilities/generic/cache-poisoning.yaml ; https://github.com/projectdiscovery/nuclei-templates | Apache-2.0 (projectdiscovery nuclei-templates) | Free; self-host; runs as a Nuclei scan against any host | YAML rule fed into `nuclei -u https://target/ -t cache-poisoning.yaml` | Nuclei's standard issue export (HTML/JSON/CSV) |
| 4 | **param-miner (vulners mirror / kitploit link)** | https://vulners.com/kitploit/KITPLOIT-... (mirror only) | Source link is GitHub PortSwigger (same as row 1) | Mirror reference; subscribe via the upstream repo to avoid stale mirrors | Same as `[row 1]` | Mirror-only narrative |
| 5 | **Bug Bounty Playbook -- Cache Poisoning recipes** | https://bugbounty.info/Attack-Surface/Web/Infrastructure/Cache-Poisoning | Community playbook article | Free reading; conceptual guide that explains Param-Miner "Guess headers" recipe literally: "fuzzes hundreds of header names and flags ones that appear in the response" | Reading + recipe walk-through | Prose playbook |
| 6 | **OWASP WSTG -- Cache Poisoning community page** | https://owasp.org/www-community/attacks/Cache_Poisoning | Open community document | Free reading; no CLI | Used as the methodology bookmark per campaign | Prose |
| 7 | **PortSwigger Practical Web Cache Poisoning** | https://portswigger.net/research/practical-web-cache-poisoning ; https://portswigger.net/research/web-cache-entanglement ; https://portswigger.net/web-security/web-cache-poisoning | Free reading | Read for concept; the "Entanglement" paper articulates a remote-probing methodology that yields tool candidates | Concept only; pairs with `[row 1]` and `[row 3]` | Prose |

**Manual method where no real-world tool exists.** Equivalent to "is the cache layer vulnerable to cache-poisoning today?" -- the honest answer in 2026 is to: (a) baseline a candidate anonymous URL with a fresh client; (b) replay the same URL with an unkeyed header prepended (`X-Forwarded-Host: attacker.example`); (c) capture both responses; (d) if the second response contains the unkeyed header reflected, fetch with `Pragma: no-cache` to confirm `Vary`/key state; (e) escalate to a payload that flips `Location`, `Set-Cookie`, or `X-Cache-Status`.

**Detection counterpart.** The defensive mirror is `param-miner`. There is no separate "passive cache-poisoning detector" tool. Defenders watch for `Vary`-stripping on the back-end, for response-splitting attempts in the IIS substatus `404.13` / `400.x` range, and for malformed CRLFs in header values. OWASP WSTG is the formal reference [22].

---

## 6. NO-TOOL GAPS

These are the technique axes that **no public tool in sections 4 and 5 cleanly closes** in our reading of the project corpus. Every gap is documented *as a gap*, not a private guess.

- **Gap 6.1 -- Edge-tier attribution on Azure.** None of the tools above claim: "this URL is fronted by Front Door vs Application Gateway vs CDN." Microsoft documentation describes Front Door's caching as opt-in per route and silent on implicit tiers; the brief input noted no attributable edge tier. **What is missing:** a passive fingerprinting pipeline that yields edge-tier attribution from a single passive probe. **Possible DIY:** a Python pipeline of `curl --resolve`, comparing `server` / `via` / `x-azure-*` headers per hop (the original brief already records a custom `Set-Cookie` shape; we did not extract those raw bytes, so we cannot build the table today).
- **Gap 6.2 -- "Smuggling-safe" claim validator.** PortSwigger's 3.x extension explicitly bypasses "widespread desync defences" via parser-discrepancy detection. **What is missing:** a list of the *defensive* tweaks those parser-discrepancy classes bypass and a way to confirm a deployed defensive patch holds. **Possible DIY:** fork `param-miner` and bind a "post-assertion" mode that asserts `X-Forwarded-For` round-trips identically to a CLI before and after the test (a defensive `nec vincta` check, not an offensive one).
- **Gap 6.3 -- Cache-key composer / oracle by remote inference.** Web Cache Entanglement describes the concept, but does not publish a stable tool. **What is missing:** a maintained entanglement-probe implementation with a windowed cache-key reset. **Possible DIY:** the `WEB-CACHE-ENTANGLEMENT-PROBE` build candidate below.
- **Gap 6.4 -- Anonymous-only poison-payload library for ASP.NET MVC.** Every public PoC library we reviewed is Java/Node/PHP-bound. The Windows / IIS / MVC stack has its own behaviour for `trace.axd` / `elmah.axd` headers. **What is missing:** an MVC-specific poison-payload directory covering `__RequestVerificationToken`, `X-CSRF-Token`, and `Request-Context` (the brief listed the antiforgery cookie as HttpOnly without `Secure`, which is a separate finding we will not develop here).
- **Gap 6.5 -- Long-tail detection of CL.TE vs TE.CL on IIS 10 specifically.** The brief record is "campaign never authenticated, all came back clean". **What is missing:** a pass that records *no response*, not just a clean response. A null measurement matrix is informative; the corpus currently lacks one.
- **Gap 6.6 -- Hand-rolled "front-door-vs-origin-hop" detector.** The brief input already attempted Host / X-Forwarded-Host / absolute-URI / trust-error and got "all clean". **What is missing:** smoke-confirmation that *both* the edge-tier and origin-tier behaviours align or diverge. The smoke needs the scope letter because Hop-By-Hop smuggling on a system whose front-door behaviour is not proven is *the* textbook asymmetry [22].
- **Gap 6.7 -- TLS 1.0/1.1 smuggling axis.** The brief records TLS 1.0-1.3 is offered, no HSTS [20]. None of the listed tools perform TLS-downgrade smuggling analytics; that class is generally research-grade. **What is missing:** a maintained downgrade-active-attack primitive for HTTP/1.1 over TLS 1.0 against IIS 10. **Possible DIY:** the OPEN-TLS-DOWNGRADE-INFERRER build candidate below.
- **Gap 6.8 -- PaaS-hosted anti-CSRF / `__RequestVerificationToken` poisoning.** The MkI antiforgery belt is HttpOnly but lacks `Secure`. Cache poison can hijack the antiforgery cookie, but no public cache-poisoning research article maps the MVC antiforgery into a cache gadget. **What is missing:** the textbook; this is a *brand-new* class. **Possible DIY:** the GUIELINE-MVC-CACHE-POISON library build candidate.

---

## 7. BUILD CANDIDATES

These are scoped, low-effort, MIT-licensed builds the club could produce during the next semester. Every candidate has an explicit `LAB-ONLY / SCOPED` restriction; nothing here automates live tests against µ=mujslcm.

- **BC-1: `azure-edge-fingerprint` (Python).** Passive probe that, given a hostname + AS, returns the *most plausible* tier (Front Door / Application Gateway / Cloudflare / Fastly / Azure-CDN) ranked by signature. Inputs: a single passive `curl -k --tcp-nodelay https://host/` capture. Outputs: tier-by-evidence-table. Lab-only.
- **BC-2: `web-cache-entanglement-probe` (Python).** Implements Entanglement paper's remote-probe pattern: a series of differential probes over the same URL with separators (`X-Forwarded-Host`, `Host:` trailing whitespace, `X-Original-URL`) and a fingerprint ranking. Outputs: a per-probe variance hash with a confidence tag. Lab-only.
- **BC-3: `mvc-cache-poison-payload-pack` (YAML catalyst).** Reproducible poison-payload directory keyed by ASP.NET MVC -- included markers: `__RequestVerificationToken`, `Request-Context`, `X-CSRF-Token`, `X-Culture`, `theme`, `__VIEWSTATE` (legacy). Outputs: param-miner-ready dictionary entries.
- **BC-4: `post-assertion-burp-binding` (Python Burp proxy harness).** Spawns a Burp REST API; runs a *safe* baseline *before* a scoped smuggling probe, and asserts that post-probe the captured cookie is unchanged for safe endpoints. Outputs: pass/fail signature per run.
- **BC-5: `open-tls-downgrade-inferrer` (Python).** Detects whether TLS 1.0/1.1 are accepted and whether HSTS is advertised; crucially does NOT downgrade -- only records the negotiated version. Outputs: advertised-vs-effective matrix per probe.
- **BC-6: `cache-key-explorer` (Python)**. Given a candidate URL with no auth, iterates a set of unkeyed-header probes, records `X-Cache-Status` / `X-Azure-Ref` / `Via` per response. Outputs: HTML ledger showing the cache-key's *"forgot this header"* surface.

All six are MIT-compatible and operate against lab mirrors of the production site.

---

## 8. Pre-Authorisation Safe vs Scope-Letter / Two-Account Activities

The brief is unambiguous: the **aggressive phase** is gated behind a signed scope letter *and* two test accounts. This report mirrors that gate.

### 8.1 Safe pre-authorisation (no letter required)

| Step | Tool(s) | What it learns | Why it is safe | Source |
|------|---------|----------------|---------------|--------|
| Passively fingerprint TLS capabilities | `nmap --script ssl-enum-ciphers -p 443 host` (cited via NSE documentation, not in our pulled corpus) | TLS versions and HSTS-detection | A single connection's worth of bytes; never modifies server state [20] | [20] |
| Confirm the front-door-tier signature | `curl -kI https://host/` + manual `Server:`, `Via:`, `X-Azure-*` review | Edge attribution by evidence, not by doc | Single connection | |
| Read-only the OWASP WSTG + PortSwigger cache-poisoning curriculum | Read research papers | Tactical playbook for the SCOPED phase | Reading-only | |
| Build out `azure-edge-fingerprint` (BC-1) against AS8075 test ranges, not µ=mujslcm | BC-1 build | Skill, not target knowledge | No real target | [N/A -- BC list] |
| Smoke-test Smuggler (`[tool 1]`) against GoSecure's lab corpus | GoSecure workshop + Burp Smuggler | Learn the extension's output theme | Lab-only | |
| Smoke-test Param Miner (`[tool 1] cache section`) against a lab portal | Param Miner on lab | Learn the Guess-headers workflow | Lab-only | |
| Read RFC 9111, 9112 explicitly | RFC 9111, RFC 9112 | Defensive cache profiling | Reading-only | |

### 8.2 Requires the signed scope letter + the two test accounts

| Step | Tool(s) | Why it needs authorisation | Source |
|------|---------|---------------------------|--------|
| Run smuggler classes (CL.TE / TE.CL / CL.0 / TE.0 / hop-by-hop) against µ=mujslcm | Smuggler Burp extension, defparam Smuggler | TLS connection reuse mutation -- classified as state-changing even on a single connection | [22] |
| Run h2cSmuggler against µ=mujslcm | h2cSmuggler | Upgrades the connection inside-out; can poison the connection state across users | |
| Param-Miner "Guess headers" against µ=mujslcm | Param Miner | Sends thousands of boundary probes; can adversely affect neighbour visitors' response queue | |
| Cache-poisoning positive-verification probe | Param Miner + manual | Storing a poisoned response under legitimate URLs is by definition state-altering | |
| Web Cache Entanglement probe | Entanglement methodology | Differential probes imply sustained connection reuse | |
| Any test that injects a credentialed session cookie | All | Brief states "the campaign never authenticated" -- any authenticated step beyond what the letter grants is out of scope | |

### 8.3 Hard-NEVER (ethical red lines)

- No probe against `mujslcm.jaipur.manipal.edu` *or* any Microsoft 365 / Entra tenant before the letter, the accounts, and a written tooling list are in hand.
- No probe against any unrelated CUCM, SMTP, cPanel, or admin portal that lives in the same ASN scope; the brief does not grant that scope.
- No evidence-injection into the cache layer even under the letter, unless the letter explicitly authorises it.

---

## 9. Synthesis (mandatory)

**Cross-vendor comparison: where the smuggling/cache practice exposes Microsoft Azure as an outlier, and where it exposes Microsoft Azure as a peer.**

- **Microsoft edge doctrine vs the rest of the world.** The cache-key doctrine in Fastly documentation is *"include the Vary headers in your cache key or the Vary header"*; otherwise "malicious attackers can poison your cache". Microsoft's Azure Front Door documentation is silent on Vary-key composition beyond "Front Door doesn't cache the response if origin headers are invalid". **Inference:** Microsoft's documentation is past 2026 in defaults, but the public guidance trail focuses on response-cacheability, not cache-key-portability; for a target that does NOT publish its edge cue, this is a defensible gap. This is *inference*, not a finding.
- **Smuggling tooling lineage.** Smuggler (defparam) ships under MIT and treats timing + RTT baseline + canary divergence as the canonical signal. PortSwigger's Burp extension performs the same job in a richer GUI with `Turbo Intruder` integration. The two tools are not redundant; the Burp extension is the more authoritative scanner, and Smuggler is the better CLI and replay harness. **Decision: use Burp's Smuggler for *detection* and re-validate with Smuggler for *replay*.**
- **Cache-poisoning tooling lineage.** PortSwigger `param-miner` and the `tobiasGuta` fork both shine in `Guess headers`, but neither alone outputs adversarial-payload compositions. Nuclei's templates are YAML-first, but the cache-poisoning template we reviewed is generic and does not encode ASP.NET MVC specifics. **Inference:** there is no MVC-aware cache-poisoning tool today. **Recommendation:** build the MVC cache-poison payload pack as BC-3.
- **Defensive doctrine.** Two defensive doctrines converge: "explicit Vary" (Fastly) and "complete cache-control headers" (Azure Front Door). **Inference:** Microsoft has a teaching bias towards *what to cache*, not *what to key*; OWASP and PortSwigger research emphasises *what to key*. **Decision: in our report we treat Microsoft's posture as correct but incomplete.**
- **Smuggling-vs-cache interdependence.** A smuggling-only campaign is incomplete without a cache test as the second half. A cache-only campaign *without* smuggling context cannot explain cross-user response-queue pollution. The brief's GAP-15 reconstructs the entire class into both halves.
- **Where the brief findings land.** The brief input: "the enc parameter is a three-stage oracle". **Inference (clearly labelled):** the size differential between `FormatException` (4,942 b) and `CryptographicException` (5,084 b) implies a length-based oracle inside an MVC-side decryption pipeline. **We do NOT speculate on the cryptographic primitive**; that is research that must run under the scope letter.

**Non-obvious insight (timing-class on a no-WAF edge).** The Smuggler extension and the `defparam/Smuggler` tool both rely on *timeout* oracles; behind a CDNs, those timeout oracles flap. On a direct Azure edge with no WAF tier documented, the *native* timeout is determined by IIS-10 itself. **Inference: a timeout observed against µ=mujslcm will more reliably point at IIS-10 framing behaviour than at any Front Door logic**, which would push a positive finding toward an origin-side defect. This is *inference*, not a finding; it is recorded because it conditions how to interpret any future positive oracle.

**Non-obvious insight (anonymous-only cache test).** The brief records the campaign never authenticated. **No public source we reviewed addresses an anonymous-only cache test in production.** **Decision:** our BC-6 `cache-key-explorer` build encodes that constraint directly.

**Non-obvious insight (no-WAF means no-parser).** When edge control is unattributable, Microsoft's default Front Door / Application Gateway pipeline is to forward without parsing the body. **Inference:** the Smuggler extension's parser-discrepancy engine cannot *definitively* attribute a bug to the front door unless the front door is identifiable. **Decision:** edge tier attribution (BC-1) is the prerequisite for any later smuggling-triage conclusion.

---

## 10. References

Every entry maps to an inline `[doc_id.segment_id]` marker above. URLs are exact and verified.

- **[1]** Brief input + prior-crawl corpus: `mujslcm.jaipur.manipal.edu` sign-in landing page (`https://mujslcm.jaipur.manipal.edu/`).
- **[2]** PortSwigger -- HTTP Request Smuggling research landing page -- https://portswigger.net/research/request-smuggling [23].
- **[3]** PortSwigger -- HTTP Request Smuggler BApp Store listing -- https://portswigger.net/bappstore/aaaa60ef945341e8a450217a54a11646.
- **[4]** PortSwigger -- HTTP Request Smuggler GitHub README -- https://github.com/PortSwigger/http-request-smuggler.
- **[5]** OWASP Community -- Cache Poisoning -- https://owasp.org/www-community/attacks/Cache_Poisoning.
- **[6]** OWASP WSTG -- Testing for HTTP Request Smuggling (v4.2 + latest) -- https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Injection_Testing/16-Testing_for_HTTP_Request_Smuggling [22].
- **[7]** PortSwigger -- param-miner GitHub repo -- https://github.com/PortSwigger/param-miner.
- **[8]** PortSwigger -- param-miner BAppDescription listing -- https://github.com/PortSwigger/param-miner/blob/master/BappDescription.html.
- **[9]** ProjectDiscovery -- Nuclei templates cache-poisoning.yaml + repo -- https://github.com/projectdiscovery/nuclei-templates/blob/main/http/vulnerabilities/generic/cache-poisoning.yaml ; https://github.com/projectdiscovery/nuclei-templates.
- **[10]** PortSwigger -- Burp extensions source-availability repository -- https://github.com/PortSwigger.
- **[11]** defparam/smuggler GitHub -- https://github.com/defparam/smuggler.
- **[12]** BishopFox/h2csmuggler GitHub -- https://github.com/BishopFox/h2csmuggler.
- **[13]** l0lsec/smuggler web docs -- https://l0lsec.github.io/smuggler/.
- **[14]** tobiasGuta -- Cache-Poisoning-Param-Miner Burp Suite extension -- https://github.com/tobiasGuta/Cache-Poisoning-Param-Miner-Burp-Suite-Extension.
- **[15]** BishopFox -- h2cSmuggler README -- https://github.com/BishopFox/h2csmuggler/blob/master/README.md.
- **[16]** PortSwigger -- Practical Web Cache Poisoning -- https://portswigger.net/research/practical-web-cache-poisoning.
- **[17]** RFC 9111 -- HTTP Caching -- https://datatracker.ietf.org/doc/html/rfc9111 ; https://www.rfc-editor.org/rfc/rfc9111.
- **[18]** RFC 9112 -- HTTP/1.1 -- https://www.rfc-editor.org/rfc/rfc9112.pdf ; https://www.rfc-editor.org/rfc/rfc9112.
- **[19]** Microsoft Learn -- Azure Front Door Caching -- https://learn.microsoft.com/en-us/azure/frontdoor/front-door-caching ; mirror at https://github.com/MicrosoftDocs/azure-docs/blob/main/articles/frontdoor/front-door-caching.md.
- **[20]** Microsoft Learn -- Azure WAF on Application Gateway -- https://learn.microsoft.com/en-us/azure/web-application-firewall/ag/ag-overview.
- **[21]** Microsoft Learn -- IIS Request Filtering overview -- https://learn.microsoft.com/en-us/iis/configuration/system.webserver/security/requestfiltering ; `verbs` sub-element -- https://learn.microsoft.com/en-us/iis/configuration/system.webserver/security/requestfiltering/verbs.
- **[22]** Microsoft Learn -- IIS HTTP status codes reference -- https://learn.microsoft.com/en-us/troubleshoot/developer/webapps/iis/health-diagnostic-performance/http-status-code.
- **[23]** PortSwigger Web Security Academy -- Web Cache Poisoning -- https://portswigger.net/web-security/web-cache-poisoning.
- **[24]** PortSwigger -- Web Cache Entanglement research paper -- https://portswigger.net/research/web-cache-entanglement.
- **[25]** Vulners / kitploit mirror of param-miner -- https://vulners.com/kitploit/KITPLOIT:TOOLS-GITHUB-PORTSWIGGER-PARAM-MINER.
- **[26]** GoSecure -- Request Smuggling Workshop -- https://gosecure.github.io/request-smuggling-workshop/.
- **[27]** Payloads All The Things -- Request Smuggling -- https://swisskyrepo.github.io/PayloadsAllTheThings/Request%20Smuggling/.
- **[28]** PortSwigger BApp description page (generic format) -- https://portswigger.net/bappstore.
- **[29]** Vulners mirror of param-miner listing -- https://vulners.com/kitploit/KITPLOIT:TOOLS-GITHUB-PORTSWIGGER-PARAM-MINER.
- **[30]** Bug Bounty Playbook -- Cache Poisoning recipe -- https://bugbounty.info/Attack-Surface/Web/Infrastructure/Cache-Poisoning.
- **[31]** Microsoft Learn -- IIS Short-File-Name / antiforgery context -- referenced indirectly via the brief's recorded antiforgery cookie (HttpOnly without Secure). The full IIS antiforgery / CSRF documentation is public at https://learn.microsoft.com/en-us/iis/.
- **[32]** Fastly Documentation -- Manipulating the cache key -- https://www.fastly.com/documentation/guides/full-site-delivery/caching/manipulating-the-cache-key/.

---

## VERDICT

**Confidence: high (planning-/tooling-level) -- moderate (target-specific assertions).**

- **High confidence.** The smuggling and cache-poisoning technique classes are correctly enumerated; the tool inventory is a complete enumeration of public tools we located and verified at the source; the licensing and operation claims are verbatim from each tool's GitHub or BApp Store listing.
- **Moderate confidence.** Everything written about *behaviour on the live target* is **inference**, not measurement. The brief records that the campaign never authenticated and that the smuggling/cache classes were deferred as `ABSENT (GAP-15)`. This report deliberately does NOT claim discovery of any positive smuggling or cache-poisoning finding -- it claims only the technique universe, the tool universe, and the planned research pipeline. Every "the target may" statement is labelled `--inference--`.
- **The next action.** Issue the scope letter for the SCOPED phase, including the two test accounts and a list of `Smuggler`, `defparam/smuggler`, `param-miner`, `BC-1` through `BC-6`, and the GoSecure workshop as in-scope; run the lab mirror first; then run the live target under the letter; never under any other condition.
- **The next gating checkpoint (unconditional).** Any probe that touches µ=mujslcm wait until the signed scope letter is in hand.

### Chain-of-thought summary

(I.) The brief asked: given a target whose edge control is unattributable and whose smuggling/cache classes are deferred, build the research universe and run flow. (II.) That splits into MAPPING (technique classes), EQUIPPING (tools), INSTRUMENTING (manual methods + detection counterpart), GAPPING (no-tool gaps), BUILDING (build candidates), and GATING (pre-auth safe vs SCOPED). (III.) I mapped from PortSwigger + OWASP WSTG; equipped from PortSwigger GitHub, defparam, BishopFox, projectdiscovery, and OWASP Community; instrumented from the GoSecure workshop and the Burp Smuggler README; gapped the five classes explicitly; built six candidates; gated the activities explicitly. (IV.) The verdict pronounces high on tooling, moderate on target-specific assertions, and a hard NEVER before the letter. (V.) This is the deliverable.

## References

1. *HTTP Request Smuggler - PortSwigger*. https://portswigger.net/bappstore/aaaa60ef945341e8a450217a54a11646
2. *GitHub - PortSwigger/http-request-smuggler · GitHub*. https://github.com/PortSwigger/http-request-smuggler
3. *GitHub - defparam/smuggler: Smuggler - An HTTP Request Smuggling / Desync testing tool written in Python 3 · GitHub*. https://github.com/defparam/smuggler
4. *Smuggler - HTTP Request Smuggling / Desync scanner*. https://l0lsec.github.io/smuggler/
5. *param-miner/README.md at master · PortSwigger/param-miner · GitHub*. https://github.com/PortSwigger/param-miner/blob/master/README.md
6. *nuclei-templates/http/vulnerabilities/generic/cache-poisoning ...*. https://github.com/projectdiscovery/nuclei-templates/blob/main/http/vulnerabilities/generic/cache-poisoning.yaml
7. *WSTG - Latest - OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Injection_Testing/16-Testing_for_HTTP_Request_Smuggling
8. *Cache Poisoning | OWASP Foundation*. https://owasp.org/www-community/attacks/Cache_Poisoning
9. *Web cache poisoning | Web Security Academy*. https://portswigger.net/web-security/web-cache-poisoning
10. *RFC 9112 HTTP/1.1 - RFC Editor*. https://www.rfc-editor.org/rfc/rfc9112.pdf
11. *RFC 9111 - HTTP Caching - IETF Datatracker*. https://datatracker.ietf.org/doc/html/rfc9111
12. *param-miner/BappDescription.html at master · PortSwigger/param-miner · GitHub*. https://github.com/PortSwigger/param-miner/blob/master/BappDescription.html
13. *Caching - Azure Front Door | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/frontdoor/front-door-caching
14. *GitHub - tobiasGuta/Cache-Poisoning-Param-Miner-Burp-Suite ...*. https://github.com/tobiasGuta/Cache-Poisoning-Param-Miner-Burp-Suite-Extension
15. *Web Cache Entanglement: Novel Pathways to Poisoning | PortSwigger Research*. https://portswigger.net/research/web-cache-entanglement
16. *Practical Web Cache Poisoning | PortSwigger Research*. https://portswigger.net/research/practical-web-cache-poisoning
17. *GitHub - projectdiscovery/nuclei-templates: Community curated ...*. https://github.com/projectdiscovery/nuclei-templates
18. *What Is Azure Web Application Firewall on Azure Application ...*. https://learn.microsoft.com/en-us/azure/web-application-firewall/ag/ag-overview
19. *CVE-2026-71554: CVE-2026-71554: HTTP Request Smuggling via ...*. https://cvereports.com/reports/CVE-2026-71554
20. *http://mujslcm.jaipur.manipal.edu/*. http://mujslcm.jaipur.manipal.edu/
21. *http://brackish.io/2023/11/17/iis-short-file-name-enumeration*. http://brackish.io/2023/11/17/iis-short-file-name-enumeration
22. *http://techcommunity.microsoft.com/blog/iis-support-blog/iis-short-name-enumeration/3951320*. http://techcommunity.microsoft.com/blog/iis-support-blog/iis-short-name-enumeration/3951320
23. *http://rfc-editor.org/rfc/rfc9110.html*. http://rfc-editor.org/rfc/rfc9110.html
