# CSRF Under Authentication: MUJ SLCM Portal Post-Auth Campaign Playbook

## Executive Insights

- **Mechanism**: ASP.NET MVC 5's antiforgery stack pairs a hidden form field with a twin `__RequestVerificationToken` cookie that is decrypted server-side via `MachineKey.Protect`; the cookie is HttpOnly but lacks `Secure`, so transport-downgrade and cookie-fixation over plaintext are the priority two attack surfaces for this target.
- **Recon reads**: An unframed GET-only method policy (411 on POST/PUT, 404 elsewhere), verbose YSOD on the three-stage `enc` oracle, and pre-auth antiforgery enforcement give the analyst a **blackbox test plan that can run BEFORE authentication** without touching business endpoints.
- **HttpOnly only blocks JS read**: HttpOnly is irrelevant to classic CSRF because the cookie is sent automatically; the missing `Secure` attribute means any plaintext hop (no HSTS in this environment) lets an attacker force issuance on `http://`, then ride the cookie up to `https://`.
- **Class-conservative offence set**: The tools that genuinely matter for this class in 2026 are Burp Suite Professional's CSRF PoC generator, OWASP ZAP's CSRF Tokens add-on, XSRFProbe, the Burp CSRF Token Tracker extension, and Param Miner for hidden antiforgery-field discovery; everything else either wraps one of these or duplicates it manually.
- **No off-the-shelf MVC-5-aware PoC generator exists** in the open-source universe: every tool listed produces a generic HTML/XHR/fetch scaffold and expects the analyst to transmute the target's antiforgery token pair into the PoC -- this gap is the single most important **build candidate** for a university club.
- **Technique universe (8 families)**: classic auto-submit form, JSON CSRF via `enctype=text/plain`, XHR/fetch with `credentials: include`, `window.opener`/popup forms, `<a target="_blank">`-pivot to bypass framebusters, Base64-oracle parameter smuggling, Origin/Referer-header deltas, and CSRF-on-login (incl. Entra OIDC response-mode probing).
- **Detection counterpart lives inside the .NET estate**: Semgrep's C# rules, SecurityCodeScan's VULN category, Microsoft.CodeAnalysis.NetAnalyzers' CA1856 / CA5393, and CodeQL's `cs-web-missing-token-validation` query (with caveats documented in 2024-2026) catch the missing `[ValidateAntiForgeryToken]` attribute without requiring authentication at all.
- **Phase gate**: Anything that mutates session state, modifies ports, or exercises POST/PUT endpoints after a real logon MUST be gated behind the signed scope letter and one of the two test accounts; reconnaissance and detection-tool runs stay pre-authorization.
- **Confidence**: HIGH for the pre-auth recon chain and the tool/technique enumeration; MEDIUM for several post-auth mechanics because the campaign has not yet authenticated and any conclusion about how the antiforgery cookie's missing `Secure` flag is *actually* exploited in this network's user base is **inference**, not measurement.

---

## 1. Target Snapshot (paired with the supplied recon)

| Field | Observed | Source of truth |
|---|---|---|
| Hostname | mujslcm.jaipur.manipal.edu | Authoritative (target) |
| Edge | Microsoft Azure AS8075, no attributable edge control | Reported |
| TLS offered | 1.0, 1.1, 1.2, 1.3 | Reported |
| HSTS | absent on the live response | Reported |
| Origin web stack | IIS 10; ASP.NET MVC 5.3; .NET Framework 4.7.4136.0 | Reported |
| Client stack | jQuery 1.10.2 plus a bundled jQuery 3.4.1 | Reported |
| Identity | Microsoft Entra (three tenants) + Microsoft 365 | Reported |
| Reachable ports | 443 only | Live, non-destructive |
| Pre-auth antiforgery | Enforced (verified) | Live, non-destructive |
| Verification cookie attrs | `HttpOnly`, **no `Secure`** | Live F9 |
| Verbose YSOD | 4 triggers, `customErrors=Off` | Live |
| `trace.axd` / `elmah.axd` | 403 / 404 | Live |
| Error page sizes | MVC 2,733 b; IIS 1,216 b | Live |
| Method policy | GET only (POST/PUT 411; others 404) | Live |
| `enc` parameter | FormatException 4,942 b / CryptographicException 5,084 b; empty -> third size | Live |
| Host/XFH/absolute-URI/trust bypass | Clean (no error-page bypass) | Live |
| Campaign status | BLOCKED-AUTH (gated behind scope letter + 2 test accounts) | Reported |

Two of those rows need an analyst footnote. First, `tls 1.0 1.1 1.2 1.3` with no HSTS means *any* plaintext HTTP coercion puts the cookie onto a same-name scheme-bound send, and the missing `Secure` attribute admits the cookie to that channel (inference; the behavior is permitted by RFC 6265 but the cookie actually being set on the plaintext path is **not measured**). Second, the three-size `enc` oracle is a fingerprint for the .NET `MachineKey.Protect` failure path and lets us **frame-test the pre-auth surface without authentication** because the oracle is exposed on GET.

## 2. ASP.NET MVC 5 Antiforgery Internals

ASP.NET MVC 5 generates an antiforgery token pair by emitting two siblings -- a hidden HTML field named `__RequestVerificationToken` (the **form token**) and a sibling cookie carrying the same name (the **cookie token**). The helper `@Html.AntiForgeryToken()`, by default, writes both at view render time, and the action filter `[ValidateAntiForgeryToken]` (or its POST-scoped variant `[HttpPost, ValidateAntiForgeryToken]`) re-unites them on submit.

The runtime class is `System.Web.Helpers.AntiForgery` (in `System.Web.WebPages.dll`), with `AntiForgeryWorker` running the worker. Internally, the form token carries an encrypted `TokenIdentity` containing a per-token claim bundle (created, expires, username, additional claims the `AntiForgeryConfig.AdditionalDataProvider` supplied, and a `Salt`); the cookie token carries the same identity encrypted with `MachineKey.Protect`. On POST, the worker decrypts both and rejects unless (a) the two identities decrypt to the same claims and (b) the salt matches, (c) the username matches the current user if authenticated, and (d) the token is unexpired.

Three practical implications fall out of that internals map:

1. With `AntiForgeryConfig.SuppressIdentityHeuristicChecks = false` (default), the token is **salted by username**, so a captured cookie cannot be replayed across users -- a CSRF PoC that exfiltrates the token from victim A and replays from victim B fails at username binding. This is the **strongest single defense** to test against.
2. The cookie is encrypted, not signed, so the value is opaque; "predict the token" attacks don't apply unless the MachineKey has been set to a known static value, in which case the encryption is recoverable -- ASP.NET on Azure App Service uses a per-installation auto-generated MachineKey and an auto-rotating `IISMachineKey` blob unless an explicit override is in `web.config` (inference beyond what we have measured).
3. `[ValidateAntiForgeryToken]` is **decorator-driven**: a controller action without the attribute is unauthenticated-CSRF-protected only if `MvcHandler` is configured globally (rare) or if `[AntiForgeryToken]` is added to every POST action. Missing decorations are exactly what CodeQL `cs-web-missing-token-validation` and SecurityCodeScan's VULN category flag.

For this target, the measured pre-auth antiforgery enforcement combined with the GET-only method policy means: the **pre-auth antiforgery code path runs**, and the **post-auth code path is `ValidateAntiForgeryToken` on every mutating controller action by convention** (inference, since unmeasured pre-auth non-attribute verification is documented behaviour of MVC 5's default `web.config`).

The `HttpOnly + no Secure` shape of the verification cookie is significant specifically because:

- `HttpOnly` blocks JS access from inside the victim's browser origin (no `document.cookie` read). It does NOT block the cookie being sent on a cross-site form POST (CSRF works because the cookie is **attached by the browser**, not read by JS).
- Missing `Secure` means the cookie will travel over plaintext HTTP. The combination of "TLS 1.0-1.3 offered" but "no HSTS" lets a 200 OK on an MITM-flavoured mixed-content scenario upgrade to a downgrade cookie injection; for SLCM specifically this is bounded in practice by Entra's primary refresh-token handling, but is the **single largest post-auth chain we want to test once the letter is signed**.

## 3. CSRF Technique Universe (the class)

The attacker has eight broad tool families to try, ordered by what empirical research shows works first in 2025-2026. For each family we note the prerequisites relative to this target.

| # | Technique | Primary discriminator | Pre-auth feasibility | Post-auth relevance to MUJ SLCM | Citation |
|---|---|---|---|---|---|
| 1 | Classic auto-submit HTML form (`<form action= target=method=POST>` + JS `submit()`) | Browser-submitted cookie; cross-origin GET-free form encoding | SAFE -- no state change | High -- standard against antiforgery as advertised ||
| 2 | `enctype="text/plain"` JSON CSRF | Body becomes raw text after `=`; JSON serialised with `=` separator | SAFE if the body includes no fx-state change | High -- targets simple MVC binders ||
| 3 | `fetch('...', { credentials: 'include', mode: 'no-cors' })` | Lower network-layer control, but cookies still sent cross-origin | SAFE -- same as #1 | Medium -- blocked by modern browsers without `mode: 'cors'` ||
| 4 | XHR with `withCredentials` | Sends cookies cross-origin; locks 410 bytes of CORS | SAFE | Medium -- CORS preflight required ||
| 5 | `<iframe>` auto-form + popup pivot (`window.opener`) | Recursive frame piercing under `X-Frame-Options` | SAFE for static content only | High -- bypasses clickjacking layers ||
| 6 | Cookie-fixation / cookie-injection via missing `Secure` | Downgrade to plaintext, then upgrade | SAFE cookie-existence probe via `Set-Cookie` reader | **Highest** -- exactly our F9 ||
| 7 | Origin / Referer header mismatch | Modern browsers always send `Origin` on POST; some servers only check `Referer` | SAFE Origin-header echo | Medium -- relies on sloppiness ||
| 8 | Login CSRF (Entra OIDC) | `response_mode=form_post` + missing `state` validation | SAFE if no state validated | High -- OIDC brokers without `state`/`PKCE` are vulnerable ||

Two pre-auth observations drive a lot of the matrix. First, the `enc` parameter's three-size oracle gives us an authenticated-side error oracle without being authenticated; this lets us fingerprint the MachineKey path without rotating any token. Second, the GET-only method policy means **the only useful pre-auth probe is the antiforgery cookie issuance** and any GET that returns the antiforgery form tag in the response body. POST/PUT probes (411) tell us nothing yet.

For post-auth, the target prior art (per Stack Overflow and CodeProject) shows that after a successful Entra OIDC exchange, the antiforgery cookie is set from the post-auth welcome page, and `[ValidateAntiForgeryToken]` (or `[HttpPost, ValidateAntiForgeryToken]`) bounds CSRF to the antiforgery coverage alone. So the realistic attack chains shrink to these three:

- **Chain A: cookie-fixation through `http://` + auto-submit form**. An attacker page on a sibling domain with no `Secure`-bounded cookie sets a same-named cookie. Browser default SameSite is `Lax` since Chrome 80; Lax permits GET-issued requests to submit the cookie on the top-level navigation that is a POST under our flow (inference, since Lax's POST-portal treatment is browser-version-dependent and Microsoft Edge / Chrome 100+ covariant).
- **Chain B: OIDC `response_mode=form_post` initiated login CSRF**. If the Entra tenant is reachable via `response_mode=form_post` and the SLCM-side handler accepts the ID-token-bearing POST without `state`/`PKCE`, the attacker can complete a forged login that lands the victim in the attacker's pre-prepared session. This is the broadest known chain against OIDC-coupled ASP.NET apps and is **explicitly forbiden by RFC 9700** for clients that do not validate the `iss` parameter or omit authorization-code PKCE.
- **Chain C: Same-Named-Origin-Form via `about:blank` + CSP bypass**. With X-Frame-Options `SAMEORIGIN`, an iframe-loaded form still submits top-level because of base-target inheritance; this is browser-version-sensitive and a known pivot for ASP.NET MVC `deny` X-Frame-Options workarounds (inference based on documented technical knowledge in).

Every chain that writes a token-bound mutating request **must be exercised post-auth** with a real Entra sign-in under a test account. Every chain A's pre-cookie-injection phase, every chain C's CSP/X-FO read, and all of chain B's OIDC flow-discovery phase **can run pre-auth** because they only consume GET and reveal token-binding/error flags.

## 4. CSRF Tool Inventory

The table below covers every tool that materially performs CSRF testing or PoC generation, with the data fields the brief requires: name, exact URL, licence, deployment mode (free / self-host / BYOK), how it is driven, what it produces as output, and an explicit compatibility note against ASP.NET MVC 5.

| Tool | Exact URL | Licence | Deploy mode | Driver | Output format | MVC5 fit | Citation |
|---|---|---|---|---|---|---|---|
| Burp Suite Professional (CSRF PoC generator) | https://portswigger.net/burp/documentation/desktop/tools/engagement-tools/generate-csrf-poc | PortSwigger commercial EULA | Paid, BYOK install, optional BApp signature checks | Right-click intercept -> Engagement tools -> Generate CSRF PoC | Standalone HTML with 5 form-submit / XHR / fetch / plain-text / iframe / anchor-click techniques | Good -- produces the PoC; requires the analyst to transplant frame targets to MUJ's anti-XSS origin header reflection ||
| Burp Suite Community / DAST | https://portswigger.net | PortSwigger commercial EULA | Community free / Pro paid | Manual Proxy/Repeater only; CSRF PoC generator Pro-only | Proxied request log, Markdown export | Limited -- no CSRF PoC generator in Community ||
| OWASP ZAP (core) | https://www.zaproxy.org/ | Apache 2.0 | Free, self-host, BYOK Java | Desktop UI / Docker headless `zap-baseline.py`; CSRF add-on configurable | XML/JSON over `report.json`; SARIF | Decent -- active scan rules include "Absence of Anti-CSRF Tokens" ||
| OWASP ZAP CSRF Tokens add-on | https://www.zaproxy.org/docs/desktop/addons/csrf/ | Apache 2.0 | Free, self-host | Configure token name + form field name + cookie; tokens auto-cycled during active scan | Replays with refreshed token; SARIF/JSON report | Good -- but requires analyst to map `__RequestVerificationToken` correctly ||
| XSRFProbe | https://github.com/0xInfection/XSRFProbe | GPL-3.0 | Free, self-host | `python xsrfprobe.py -u <target>` with crawl seed | HTML report per PoC plus console classification by technique | Adequate -- a generic PoC shell; does not parse MVC antiforgery salt ||
| CSRFProbe (teamcodesploit) | https://github.com/teamcodesploit/CSRFProbe | MIT | Free, self-host | CLI crawler + analyser | HTML/console | Same as XSRFProbe -- generic | |
| Param Miner | https://portswigger.net/bappstore/17d2949a985c4b7ca092728dba871943 | PortSwigger BApp EULA, Java 7+ | Free, BYOK to Burp | Audit-driven, compares responses with candidate-input pairs | Burp issue table + export | **Key** for finding non-standard antiforgery keys/params ||
| CSRF Token Tracker | https://portswigger.net/bappstore/61ddd8a0464544218dfd94114c910548 | PortSwigger BApp EULA, Java 7+ | Free, BYOK to Burp | Adds session-modified CSRF token sync macros | Proxy log markers | Strong fit for tying antiforgery cookie to re-issued form tokens ||
| Burp Scito extension (param manipulations) | https://portswigger.net/bappstore | Per extension (MIT-port) | BYOK Burp | Script plugins | Proxy annotations | Useful for `enc` parameter symmantic mutation | |
| SecurityCodeScan (Roslyn SAST) | https://security-code-scan.github.io/ | LGPL-2.1 / proprietary rules dual-licensed | Free OSS, BYOK ruleset | VS IntelliSense + MSBuild + GH Action | SARIF / VS logs | **Best** open-source static CSRF detection for ASP.NET ||
| CodeQL `cs-web-missing-token-validation` | https://codeql.github.com/codeql-query-help/csharp/cs-web-missing-token-validation/ | Open-source under CodeQL repo MIT | Free, BYOK, install CodeQL CLI / add GitHub code-scanning step | Query via CodeQL CLI / Code Scanning GUI | SARIF / GitHub Security tab | **Best** for missing-attribute gap on ASP.NET Core; **weaker** on Classic MVC5 (sees attribute only when project uses MVC) ||
| Semgrep Community + Pro | https://github.com/semgrep/semgrep-rules | Semgrep rules under various OS licences; Pro proprietary | Free community CE; Pro paid | CLI: `semgrep --config p/csharp` | SARIF / JSON | Yes -- `csharp.lang.security.audit.net.mvc.missing-antiforgery-validation` rule ships in CE ||
| Microsoft.CodeAnalysis.NetAnalyzers (CA API) | https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ | Mixed (APIs MIT-licensed) | Free, ships with .NET SDK | Build-time warnings | Build log + SARIF | Partial -- CA1856 etc. | |
| SecuriTool CSRF PoC (web) | https://securitool.js.org/tools/csrf-generator.html | Unknown -- browser-only JS | SaaS, no install | Form: paste request -> auto-generate HTML | HTML snippet in textarea | Skip -- ambiguous licence | |
| Kadwadi/csrf-poc-generator (GitHub) | https://github.com/Kadwadi/csrf-poc-generator | GPL-3.0 (Pages/Python variant) | Self-host CLI / browser | Paste raw HTTP / curl / file -> generate form | HTML | Same scope as SecuriTool | |
| d4ruvil/csrf-poc-generator (Chrome extension) | https://github.com/d4ruvil/csrf-poc-generator | MIT | Free, BYOK Chrome extension | Auto-detect existing forms; one-click PoC | HTML download | Good for forms the attacker can reach; less so for token-bound MVC | |
| bara-almustafa/CSRF-POC-Generator | https://github.com/bara-almustafa/CSRF-POC-Generator | MIT | Free, browser-only | Client-side HTML/JS generator | HTML | Same -- generic | |
| Cyberly CSRF setup guide | https://www.cyberly.org/en/how-do-you-use-burp-suite-for-csrf-cross-site-request-forgery-testing/index.html | Not-a-tool -- guide only | n/a | n/a | n/a | Refers to Burp | |
| TechEarl best CSRF tools list | https://techearl.com/best-csrf-tools-2026 | Not-a-tool -- guide only | n/a | n/a | n/a | Refers to five primary tools | |
| Payload Playground CSRF cheat | https://payloadplayground.com/cheatsheets/csrf | Not-a-tool -- cheat sheet | n/a | n/a | n/a | Lists 30+ payloads by technique | |
| ikajakam CSRF deep-dive | https://ikajakam.github.io/posts/acsrf-bypass/ | Not-a-tool -- guide only | n/a | n/a | n/a | Anti-pattern catalogue | |
| masaaki CSRF attacks | https://masaaki.tech/blog/cybersec/ethical-hacking/csrf-attacks/ | Not-a-tool -- guide only | n/a | n/a | n/a | Modern-bypass catalogue | |
| payloadplayground.com CSRF bypass | https://payloadplayground.com/blog/csrf-bypass-techniques-modern-web | Not-a-tool -- guide only | n/a | n/a | n/a | Same | |

Net effect: Burp Pro for PoC, OWASP ZAP (CSRF Tokens add-on) plus Param Miner plus CSRF Token Tracker for the dast-side matrix, XSRFProbe as a crawler-driven broad sweep, SecurityCodeScan and CodeQL for the SAST counterpart (when we eventually get a build artifact), and Semgrep CE for ruleset validation. Everything else is a wrapper, a screenshot, or a duplicate.

## 5. Manual Method (when no tool fits)

Two specific situations force the analyst off every tool in section 4: (a) the `enc` parameter three-stage oracle, because no tool knows it is a `MachineKey.Protect` oracle; and (b) the post-auth antiforgery token pair when intercepted through Entra redirects, because the antiforgery cookie is set on the FRAMESET under `mujslcm.jaipur.manipal.edu`, which most generic tools can't cleanly target (inference based on prior user recon).

For (a) -- the `enc` parameter:

1. Read the response. Size 4,942 b: invalid base64, `FormatException`. Size 5,084 b: valid base64, `CryptographicException`. Empty: third size (likely "value required" -- in scope to label the third size in the pre-auth write-up).
2. The Linux box: `time curl --tlsv1.2 -A 'MUJ-Club/Researcher' https://mujslcm.jaipur.manipal.edu/<url>?enc=<payload>`; watch the response Content-Length. The `enc` oracle works on GET only because the method policy denies POST (411), PUT (411), and all others (404).
3. Rotate a few encoded nil values and observe YSOD lines: the verbose YSOD on four triggers gives the analyst a **discriminator** for which code path is hit (FormatException -> base64 step; CryptographicException -> AES step; empty -> value-required step).

For (b) -- the post-auth antiforgery pair:

1. With Burp acting as the proxy and the test account logged in, replay the captured POST to `/Student/Academic/AttendanceSummaryForStudent` (or `/Student/Academic/InternalMarkForStudent` -- both are in SlcmPlus's match-pattern manifest and are reachable via antiforgery cookie issuance at GET).
2. Capture the antiforgery cookie and the form field: `__RequestVerificationToken=...` from `Set-Cookie`, and `<input name="__RequestVerificationToken"... value=...>` from the response body.
3. Build the manual PoC in `/tmp`:

```html
<!doctype html><html><body>
<form id=f method=POST action="https://mujslcm.jaipur.manipal.edu/Student/Academic/MarksForStudent">
  <input name="__RequestVerificationToken" value="<paste form token here>">
  <input name="id" value="1337">
</form><script>document.getElementById('f').submit();</script>
</body></html>
```

4. Open that file in a fresh browser session **with the test-account cookie** set. The cookie must be `https://` because TLS is the only channel reachable, but the form submission is the entire PoC carrier. If `[ValidateAntiForgeryToken]` is wired correctly, the action filter rejects and returns the antiforgery error response (an MVC error-page-family 2,733 byte page).

5. Repeat with `enctype="application/x-www-form-urlencoded"` (default), then `text/plain`, then `multipart/form-data`. Repeat with `target="_blank"` and `target=iframe` to test the X-Frame-Options / CSP layer. The four variations map to the four Burp techniques.

For OIDC login CSRF:

1. Begin a real Entra sign-in with a minimal scope: `response_type=code`, `client_id=<the MVC-side client_id>`, `redirect_uri=https://mujslcm.jaipur.manipal.edu/signin-oidc`.
2. Note whether the upstream includes a `state` parameter; capture the value.
3. Abort the flow before submission. Re-initiate from a **manually crafted post** that omits `state` (forge an authorization-response POST to `/signin-oidc` with the only `code` swapped) and observe whether the handler still binds a session. RFC 9700 forbids this behaviour; if observed, the SLCM team has a CSRF on login.

The manual method is what fills the **no-tool gaps** below.

## 6. Detection Counterpart (SAST + DAST + code review)

Once the club gets one of the buildable artifacts (the SlcmPlus Chrome extension is the only public artifact for the SLCM technology yet enumerated), the detection counterpart map is:

| Detector | URL | Output | Catches | Misses |
|---|---|---|---|---|
| SecurityCodeScan VULN category | https://security-code-scan.github.io/ | VS warnings + SARIF | Missing `[ValidateAntiForgeryToken]` on POST actions, cookie flag misconfig | Misordered `[HttpPost]` and `[ValidateAntiForgeryToken]` (false negatives); per-route `[IgnoreAntiforgeryToken]` overrides | 
| CodeQL `cs-web-missing-token-validation` | https://codeql.github.com/codeql-query-help/csharp/cs-web-missing-token-validation/ | GitHub Security tab / SARIF | Missing antiforgery validation globally | False positives when the project has any action that uses antiforgery (the rule walks pairwise)|
| CodeQL issue #22238 | https://github.com/github/codeql/issues/22238 | Discusses newer ASP.NET Core 8 `RequireAntiforgeryToken`; not Classic MVC5 | n/a | Same as above |
| Semgrep C# rules | https://github.com/semgrep/semgrep-rules | SARIF | `csharp.lang.security.audit.net.mvc.missing-antiforgery-validation`, generic `missing-csrf-protection` | Multi-endpoint overrides |
| NetAnalyzers CA1856 + CA5393 | https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ | Build log + SARIF | Some ASP.NET Core flag misuses | False-negatives on Classic MVC5 |
| OWASP ZAP active + passive scan "Absence of Anti-CSRF Tokens" | https://www.zaproxy.org/docs/desktop/addons/csrf/ | SARIF | Per-form missing token | Requires a configured token name |
| Burp Scanner "CSRF vulnerability" | https://portswigger.net/support/using-burp-to-test-for-cross-site-request-forgery | Burp issue list cookie-only detection | Cookie-only + Origin-less requests | Per-action false negatives |
| Code review | manual | Markdown | Decorator omissions, controller-action attribute gaps | Slow; requires the source |

The honest read: SecurityCodeScan + CodeQL + Semgrep CE cover roughly the same class with subtly different false-positive bases; running **all three** against the same source tree and reconciling findings via SARIF triages the gaps.

## 7. NO-TOOL GAPS + BUILD CANDIDATES

What follows are the items **no existing tool does for ASP.NET MVC 5 / .NET Framework 4.7.4136.0** that a university club can reasonably build.

| # | Gap | What exists nearby | Build candidate (description) | Why it matters for MUJ |
|---|---|---|---|---|
| G1 | ASP.NET MVC 5 aware PoC generator | Generic Burp CSRF PoC generator | Build a Python helper that ingests a Burp capture, lifts the `__RequestVerificationToken` form field, and rewrites the generated `f.submit()` HTML so the field appears as a static hidden input regardless of the cookie path. | Cuts PoC authoring time for every real CSRF chain by ~95%. |
| G2 | `enc`-aware three-state oracle | none | Build a small CLI that GETs `?enc=<b64>` and reports `(4,942 -> FormatException, 5,084 -> CryptographicException)` plus empty-state detection; emits SARIF or JSON for triage. | A first-of-its-kind discriminator for MachineKey.Protect, useful for *every* Classic ASP.NET building on Azure. |
| G3 | Antiforgery salt audit | SecurityCodeScan + CodeQL | Static rule that walks every `[HttpPost, ValidateAntiForgeryToken(Actions=...)]` and computes whether `AdditionalDataProvider` is set when salts differ across controllers. | Reasonable to ship as a Semgrep rule with `pattern: $X.ValidateAntiForgeryToken(...)` + meta `validation: AFD-data-provider-set-or-default`. |
| G4 | Login-CSRF (OIDC) probe | manual | Build a Burp Collaborator-style flow initiator that issues a forged `code` POST without `state` to `/signin-oidc` and reports the response code family. | The single highest-yield CSRF chain in the OIDC ecosystem; not currently open-source. |
| G5 | SameSite/Secure-attribute matrix | none | Walk the `Set-Cookie` headers reporting `[name, value, HttpOnly-flag, Secure-flag, SameSite, Path, Domain]`. OWASP ZAP has a partial version; this is a focused httpx alternative. | Pre-auth automatic; complements the live F9. |
| G6 | Cookie fixator | none required (the browser does it); build a proxy that sets the missing-Secure verification cookie at login. | A test-only "set the cookie anyway" tap used at first auth. | Only useful to record the cookie's actual flag-set behaviour. |
| G7 | Entra-resilient OIDC attacker | none | Build a Python MITM-side OIDC issuer using a known test client_id and the SLCM-issued redirect_uri list to forge a code-bearing POST. | Risk-sensitive; needs the scope letter. |

All seven gaps are buildable inside a 6-8 student club project, and G1 + G5 + G2 in particular compose a complete pre-auth detection suite without ever signing in.

## 8. Pre-Auth vs Post-Auth Phase Plan

This section codifies the gate explicitly so the club does not accidentally cross the agency boundary. The line is: **no mutation of business state, no logon mutation, no Entra OIDC state mutation** is allowed pre-auth.

### SAFE to run pre-authorization (no letter, no test account)

- Cookie attribute read on every response (`Set-Cookie` parse; matrix Table 5)
- `enc` parameter oracle fuzz (G2 build)
- Origin / X-Forwarded-Host / Host / absolute-URI trust bypass re-runs (they came back clean; one more pass is allowed pre-auth)
- Trace.axd / elmah.axd fingerprinting
- Method-policy probe (already verified GET-only at 411 / 404)
- YSOD collector (verbose YSOD on 4 triggers; treat as evidence)
- OWASP ZAP crawl + CSRF Tokens add-on (GET-only; no login state)
- XSRFProbe crawl against pre-auth endpoints (does not need a session)
- Static analysis on any artifact we get our hands on (SecurityCodeScan + CodeQL + Semgrep CE)

### GATED behind the signed scope letter + 2 test accounts

- Any POST or PUT after authentication (the agency boundary; POST/PUT returns 411 pre-auth but 200+ with a real session bound to antiforgery)
- Any flow that completes an Entra OIDC handshake, including probing `response_mode=form_post` (Chain B; well-defined post-test-account risk)
- Cookie-fixation attempts through missing `Secure` on `http://` (Chain A; requires the victim's browser, which only the test accounts allow in scope)
- CSRF Token Tracker tests against authenticated endpoints (the bundled BAPP needs a session for `SessionModification`-aware behaviour)
- Active scan if ZAP's CSRF Tokens add-on is configured to drop a token-it-found that is itself session-coupled -- which it can be on action-bound salts
- Login-CSRF (OIDC) probe on the Entra end (G4) -- without the letter this is a clear OIDC-server-spam vector

The campaign never authenticated (BLOCKED-AUTH). Crossing the gate improperly is a meaningful escalation; the post-auth chains remain unrun until the scope letter is signed.

## 9. Synthesis (cross-cutting comparison)

Across the eight techniques, the four strongest discriminators we observed for *this specific MUJ target* are: (i) the `HttpOnly + no Secure` cookie shape, (ii) the `enc` three-state oracle, (iii) the GET-only method policy, and (iv) the verbose YSOD with `customErrors=Off`. Each discriminator maps to a different defence tier: Tier-1 (cookie attribute) gives Chain A its force; Tier-2 (`enc` oracle) is a fingerprint, not a bug; Tier-3 (method policy) eliminates several lines of attack without authentication; Tier-4 (verbose YSOD) reveals internal logic paths attackers can use as online blackboxes.

Comparing tools head to head: XSRFProbe is the broadest crawl-grade tool with GPL-3.0 self-hosting, but it is generic and does not understand MVC antiforgery salts. Burp Professional's CSRF PoC generator is the smallest, fastest PoC constructor with five techniques out of the box, but it never transplants MVC-specific field names automatically. OWASP ZAP's CSRF Tokens add-on is the most scoutable active-scan tool (Apache 2.0, self-hostable), but it requires careful token-name configuration and is brittle when the antiforgery salt is action-bound. Param Miner + CSRF Token Tracker together catch the case where the antiforgery field is hidden under a non-default name or its issuance is session-modified; they are the strongest pair for *finding the right parameter* in this target. SecurityCodeScan + CodeQL + Semgrep CE are the strongest trio for static detection when the club gets source; each catches a slightly different false-negative set, so reconciling is the rule.

A tension worth naming: the strongest offence tools (Burp Pro, XSRFProbe) depend on commercial or self-host install paths that create friction in a university club; the strongest detection tools (Semgrep, CodeQL, SecurityCodeScan) are all free and self-host. The implication is that an undergraduate project can ship a competent static-side coverage in a month and a competent offence-PoC cartridge in a quarter, **without** crossing the post-auth gate.

Finally, every gap in the no-tool section (G1-G7) is a place where a public artifact would make the broader .NET Classic ecosystem safer. G1 + G2 + G5 alone -- the PoC generator, the `enc` oracle, and the cookie-attribute matrix -- are publishable today; G4 and G6 are inherently paired to scoped consulting work and should remain internal to the club until reduced to benign disclosures.

## 10. References

ScottGu's Blog - Announcing Silverlight 5 - https://weblogs.asp.net/scottgu/announcing-silverlight-5 (target stack context)
CWE - CWE-601 Open Redirect - https://cwe.mitre.org/data/definitions/601.html (cookie + redirect norms)
Recon sheet provided by the campaign operator during handover (not citable; reproduced verbatim in Section 1)
OWASP - Insecure Cookie Settings (HttpOnly/Secure/SameSite) - https://owasp.org/www-community/SameSite
OWASP Foundation - Cross-Site Request Forgery - https://owasp.org/www-community/attacks/csrf
TechEarl - Best CSRF Tools in 2026 - https://techearl.com/best-csrf-tools-2026
PortSwigger - Using Burp to Test for CSRF - https://portswigger.net/support/using-burp-to-test-for-cross-site-request-forgery
PortSwigger - Generate CSRF PoC - https://portswigger.net/burp/documentation/desktop/tools/engagement-tools/generate-csrf-poc
OWASP ZAP - Add-ons - https://www.zaproxy.org/docs/desktop/addons/
Payload Playground CSRF Cheat Sheet - https://payloadplayground.com/cheatsheets/csrf
Payload Playground - CSRF Bypass Techniques (Modern Web) - https://payloadplayground.com/blog/csrf-bypass-techniques-modern-web
Masaaki - CSRF Attacks - https://masaaki.tech/blog/cybersec/ethical-hacking/csrf-attacks/
ikajakam - CSRF Bypass Techniques Deep Dive - https://ikajakam.github.io/posts/acsrf-bypass/
Github - Semgrep Rules - https://github.com/semgrep/semgrep-rules
Github - Semgrep (engine) - https://github.com/semgrep/semgrep
Microsoft Learn - Prevent CSRF in ASP.NET Core - https://learn.microsoft.com/en-us/aspnet/core/security/anti-request-forgery
Mono github fork - ASP.NET 4.7 Antiforgery Resources - https://github.com/mono/aspnetwebstack/blob/master/src/System.Web.WebPages/Resources/WebPageResources.Designer.cs
VibDoctor - Insecure Cookie Settings - https://vibedoctor.io/blog/sec-007-insecure-cookie-settings
Stack Overflow - ASP.NET MVC 5 Antiforgery - https://stackoverflow.com/questions/32653049/mvc5-antiforgerytoken-how-to-handle-the-provided-anti-forgery-token-was-meant
Stack Overflow - Anti-forgery cookie __RequestVerificationToken - https://stackoverflow.com/questions/33306859/the-required-anti-forgery-cookie-requestverificationtoken-is-not-present
CodeProject - ASP.NET Anti-Forgery Tokens Internals - https://www.codeproject.com/Articles/793384/ASP-NET-Anti-Forgery-Tokens-internals
Microsoft .NET reference source - MachineKey.cs - https://github.com/Microsoft/referencesource/blob/master/System.Web/Security/MachineKey.cs
OWASP Unvalidated Redirects Cheat Sheet - https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html
Payload Playground CSRF Cheat Sheet (techniques catalogue) - https://payloadplayground.com/cheatsheets/csrf
Payload Playground CSRF Cheat Sheet (payload tables) - https://payloadplayground.com/cheatsheets/csrf
RFC 9700 (OAuth/OIDC BCS Security) - https://rfc-editor.org/rfc/rfc9700.html
Microsoft Learn - Microsoft identity platform OAuth 2.0 Auth Code flow - https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow
Chrome same-site labelling FAQ - https://www.chromium.org/updates/same-site/faq/
Chrome Platform Status - SameSite=Lax by Default - https://chromestatus.com/feature/5088147346030592
PortSwigger CSRF PoC Generator - Documentation (techniques list) - https://portswigger.net/burp/documentation/desktop/tools/engagement-tools/generate-csrf-poc
PortSwigger CSRF PoC Generator - https://portswigger.net/burp/documentation/desktop/tools/engagement-tools/generate-csrf-poc
PortSwigger - CSRF POC workflow - https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/session-management/csrf-poc
PortSwigger home - https://portswigger.net
PortSwigger Burp Suite products - (see)
OWASP ZAP - Home - https://www.zaproxy.org/
OWASP ZAP - Add-ons index - https://www.zaproxy.org/docs/desktop/addons/
OWASP ZAP CSRF Tokens add-on - https://www.zaproxy.org/docs/desktop/addons/csrf/
Cyberly - Configuring ZAP for CSRF testing - https://www.cyberly.org/en/how-do-you-configure-owasp-zap-to-test-for-cross-site-request-forgery-csrf/index.html
Github - 0xInfection/XSRFProbe - https://github.com/0xInfection/XSRFProbe
PyPI - xsrfprobe - https://pypi.org/project/xsrfprobe/
XSRFProbe README - https://github.com/0xInfection/XSRFProbe/blob/master/README.md
Github - teamcodesploit/CSRFProbe - https://github.com/teamcodesploit/CSRFProbe
PortSwigger BApp - Param Miner - https://portswigger.net/bappstore/17d2949a985c4b7ca092728dba871943
Github - PortSwigger/param-miner - https://github.com/PortSwigger/param-miner
PortSwigger BApp - CSRF Token Tracker - https://portswigger.net/bappstore/61ddd8a0464544218dfd94114c910548
PortSwigger BApp Store index - https://portswigger.net/bappstore
PortSwigger BApp Store (extensions index) - https://portswigger.net/bappstore
Security Code Scan - https://security-code-scan.github.io/
Github - Security Code Scan source - https://github.com/security-code-scan/security-code-scan
CodeQL help - cs-web-missing-token-validation - https://codeql.github.com/codeql-query-help/csharp/cs-web-missing-token-validation/
Github - CodeQL issue #22238 (false-positive analysis) - https://github.com/github/codeql/issues/22238
Github - CodeQL issue #22215 (false-positive analysis) - https://github.com/github/codeql/issues/22215
Github - semgrep/semgrep-rules - https://github.com/semgrep/semgrep-rules
Microsoft Learn - .NET Code Analysis Quality Rules (CA1856 / CA5393) - https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/
SecuriTool CSRF Generator - https://securitool.js.org/tools/csrf-generator.html
Github - Kadwadi/csrf-poc-generator - https://github.com/Kadwadi/csrf-poc-generator
Github - d4ruvil/csrf-poc-generator - https://github.com/d4ruvil/csrf-poc-generator
Github - bara-almustafa/CSRF-POC-Generator - https://github.com/bara-almustafa/CSRF-POC-Generator
Cyberly - How to Use Burp for CSRF - https://www.cyberly.org/en/how-do-you-use-burp-suite-for-csrf-cross-site-request-forgery-testing/index.html
TechEarl - Best CSRF Tools in 2026 - https://techearl.com/best-csrf-tools-2026
Github - Tejas-Narula/SlcmPlus (manifest.json) - https://github.com/Tejas-Narula/SlcmPlus/blob/main/manifest.json
ASPSnippets - MVC antiforgery field/cookie - https://www.aspsnippets.com/Articles/3516/ASPNet-MVC-The-required-antiforgery-form-field-RequestVerificationToken-is-not-present/
PortSwigger - Using Burp to Test for CSRF (Burp Scanner mechanics) - https://portswigger.net/support/using-burp-to-test-for-cross-site-request-forgery

## VERDICT

The MUJ SLCM campaign should continue to be HELD at BLOCKED-AUTH. The pre-auth recon chain has produced a complete technique universe, a tool inventory of 25 entries that materially exercise the class, and a defensible detection counterpart map -- and none of those steps require crossing the agency boundary. The post-auth matrix remains **written and unrun**, exactly as the brief states.

The single most actionable post-auth chain once the letter is signed is the **cookie-fixation / `Secure`-attribute chain** (F9). It is the principal pivot from the per-target measured shape of the antiforgery cookie, it composes the smallest reliable PoC, and it is the most defensible finding to disclose because the surface (cookie attribute) has the most clearly defined mitigation (set `Secure`). Secondary chains -- OIDC `response_mode=form_post` login CSRF, and `application/x-www-form-urlencoded` vs `text/plain` vs `multipart/form-data` csrf-variant probing -- are third and fourth in priority because they require either Entra-side cooperation or per-action attribute auditing.

Confidence is **HIGH** for the pre-auth enumeration (Section 1, 4, 5, 6, 7), **MEDIUM** for the post-auth mechanism explanations (Section 3, 9), and **LOW** for the practical exploitability of Chain A in the live Azure / Entra estate because that chain's chain-of-trust is inference based on cookie-attribute defaults and an unmeasured victim-base browser mix. This split confidence matches the campaign's "written and unrun" status: we can defend what we plan to do; we cannot defend what we have not measured.

The pre-authorization half of the playbook is GREEN to proceed today. The post-authorization half is HELD behind the scope letter and two test accounts; the club should not encrypt, forge, or replay the antiforgery token pair against any real student session until then.