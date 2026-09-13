# Real-Frame Clickjacking Assessment for MUJ SLCM

## Executive Summary

- **Clickbandit Is the Reference Real-Frame PoC Tool**: PortSwigger's Burp Clickbandit does not just inspect headers; it loads the target in a real iframe inside the user's browser, lets the operator position lure elements, and exports an HTML PoC [1][2]. It is bundled with Burp Suite Professional, so the university club will need office-paid access; the Burp Suite Community Edition does not include Clickbandit or the active Scanner [46].

- **Authentication State Gates the Verdict Step**: A clickjacking finding that has meaning usually needs the page to be authenticated or to expose a state-changing control. Because the user-supplied facts state the campaign was never authenticated and the aggressive phase requires a signed scope letter plus two test accounts, every gated tool and every recorded-click workflow must run only after that paper work and those accounts are in hand.

- **Header Checks Are Insufficient by Themselves**: The supplied measurement of `X-Frame-Options: SAMEORIGIN` with no CSP tells us exact-origin attackers stay blocked, but it cannot prove cross-origin attackers cannot render the page if a same-origin consumer (e.g., a sibling MVC route) embeds it. Real-frame proof needs a same-origin sandbox or an authenticated render-evidence path [21][22].

- **Browser Automation Is the Buildable Path for Real Rendering**: Playwright `FrameLocator` plus the screenshot option [8][9], Puppeteer's Frame class [25], and Selenium's WebDriver frame-switching [10] are first-party primitives. None come packaged as a "clickjacking verdict engine", so any missing capability must be assembled by the club.

- **Scanner Findings Are Triage, Not Proof**: ZAP's alert 10020-1 is typed as Passive, surfaces only when the response is missing `X-Frame-Options` or CSP `frame-ancestors`, and inherits evaluation from the WSTG-CLNT-09 technique [6]. Burp Scanner's Frameable response finding is documented in the PortSwigger issue knowledge base [47][1]-both check headers, neither loads an iframe.

- **SAMEORIGIN Does Not Stop Same-Origin Redress**: MDN notes that the same-origin framing allowance applies when all ancestors share the origin [21][22]. Practical posture for the SLCM therefore must also consider what consumer pages the university might run on `*.manipal.edu`.

- **DoubleClickjacking Bypasses Both Header Defenses**: Research from Paulos Yibelo published in December 2024 describes a double-click sequence that slips past `X-Frame-Options` and CSP `frame-ancestors` [50][51]. The technique belongs in the threat model even if the parent routes exist.

- **Self-Hosted PoC Generators Fill Pre-Auth Coverage**: Open-source generators that emit an iframe PoC (HackTricks Tools, `m14r41/Clickjacking-Poc`, `SenukDias/clickjack`, `err4O4u/FramePhish`, `senyx122/CjScan`, the exploit-development MIT library) are usable as header-driven headless PoC sources for pre-authorization triage [13][30][15][26].

- **Browser-Side Detection Is Defensive, Not Discovery**: NoClickjack, CADS, Clickjacking Detector, and the KudoKaito272 source repository add detection at the browser layer by sniffing `X-Frame-Options`, `CSP frame-ancestors`, and overlay transparency heuristics [62][63]. None discover framing footholds by themselves.

- **CSP `frame-ancestors` Is the Modern Counterpart**: MDN makes `frame-ancestors` the controlling directive over `X-Frame-Options` when both are present, and `'none'` provides a deny-by-default posture for the entire response set [21]. The current target has no CSP, so the `frame-ancestors` policy slot is empty.

- **Threat-Model Coverage Is the Deliverable's Center of Gravity**: Pre-authorization work can stack tools, scope out the same-origin siblings, build a sandbox PoC against a non-state-changing surface, and run header-only scanners; the signed letter and the two test accounts unlock live authenticated rendering proof through Clickbandit, Playwright headless, or a manual HTML harness.

## 1. Scope, Evidence, and Safety Boundaries

The investigation is bounded by what was supplied and what could be confirmed in public documentation. The user-supplied live measurements (taken on 2026-09-13) carry the day for target facts: only TCP 443 answered verbose IIS 10 probes; the four YSOD triggers with `customErrors` off; antiforgery is enforced and the cookie is `HttpOnly` without the `Secure` flag; `trace.axd` returned 403 and `elmah.axd` 404; the two error page families on MVC payload and IIS payload differ in size (2,733 b vs 1,216 b); the controller implements GET only with POST and PUT producing 411 and the rest yielding 404; the `enc` parameter exhibits the documented three-stage oracle and distinguishes malformed base64 from valid-but-unsuccessful base64; and Host-header, X-Forwarded-Host, absolute-URI, and trust-based error-bypass attempts came back clean. The supplied facts also confirm that no authentication was ever exercised and the aggressive phase (rendering, clicking, and proof-of-concept capture) sits behind a signed scope letter and two test accounts. None of those specific measurements could be re-verified externally, so the report treats them as authoritative for the target but does not generalize beyond the SLCM instance.

The public-information layer comes from primary documentation. Sources include PortSwigger's Burp Clickbandit page and Testing for Clickjacking workflow [2][1], PortSwigger's Frameable-response KB and Burp Scanner issue definitions [47][1], PortSwigger's Burp Suite and Community Edition comparison [46], OWASP's Clickjacking Defense Cheat Sheet and the OWASP-Foundation Clickjacking attack page [3][4], and the WSTG v4.2 client-side test for clickjacking [23]. The defense side is anchored on MDN's `Content-Security-Policy: frame-ancestors` and `X-Frame-Options` pages [21][22]. The automation layer is confirmed by Playwright LICENSE/Screenshots/FrameLocator docs [7][8][9], Puppeteer's LICENSE and `Frame` API [24][25], and Selenium's frames and LICENSE [10][11]. The wider technique universe pulls in Paulos Yibelo's DoubleClickjacking research [50][51], HackTricks PoC Tools UI and HackTricks repo [13], Payloads All The Things, the OWASP Top 10/Policy tags [6], and the LICENSE files that confirm Apache 2.0 for ZAP, Playwright, Puppeteer, and Selenium [64][65][7][24][11].

Two safety rules govern the rest of the report. Public information only: every tool recommendation, license claim, scope, or threat-model claim is sourced, and any extrapolation is marked explicitly (e.g., "inference", "no public statement"). Authorized-only operation: no instruction is provided that would help an attacker render the live target or click any state-changing control. Headers can be observed pre-authorization; authenticated rendering, lure click capture, and PoC export are gated.

## 2. Technique Universe

Classic clickjacking, also known as UI redress, uses a same-origin or cross-origin iframe host page and overlays the iframe with CSS so a lure element sits above a destructive control on the inner page [4]. The OWASP Foundation's framing example shows a decoy "free iPod" button aligned over a "delete all messages" control inside a mail account [4][23]. The technique is neutralized by either denying the embedding (server side) or by preventing the click (defensive UX). The two principal server-side controls are `X-Frame-Options`, which is now documented by MDN as legacy but still widely deployed, and the `Content-Security-Policy: frame-ancestors` directive, which the MDN page documents as the modern counterpart that overrides `X-Frame-Options` when both are present [22][21]. With no CSP on the SLCM, the present-day defense is the same legacy `X-Frame-Options: SAMEORIGIN` inherited from IIS or MVC defaults.

Same-Origin Redress is the corollary case to watch when only `X-Frame-Options: SAMEORIGIN` is in play. MDN notes that all ancestors must share the origin for the response to render [22]. Whether a same-origin attacker succeeds therefore depends on whether the SLCM domain hosts additional pages (parent host EEF CSS warns that the parent host has neither `X-Frame-Options` nor `CSP frame-ancestors` per the task brief). Where a same-origin sibling exists and is mis-configured, the `SAMEORIGIN` value alone does not protect the SLCM routes. This is an inference specific to the supplied framing: the parent host's header posture is not externally verifiable here and is treated as a hypothesis to test after the letter and accounts are in hand.

Drag-and-Drop Redress adds a second primitive: a target inside an iframe accepts a file-drop because the attacker page's drag handlers fire on top of an interframe area. HackTricks documents the technique as still applicable to many environments, and the PoC generator supports drag-and-drop variants [12]. SameSite cookies and frame-busting JavaScript (the page warning that `if JavaScript is disabled in the subframe, the frame busting code will not run`) are documented as auxiliary defenses [3][23].

DoubleClickjacking is a 2024 disclosure by Paulos Yibelo that operates via the small window between the start of a click and the conclusion of a second click, swapping the underlying page from the lure to a privileged page [50][51]. The disclosure claims the technique slips past `X-Frame-Options` and `CSP frame-ancestors` because those headers guard single-click iframing but do not govern programmatic action gates that depend on two-click gestures. The HackTricks PoC generator surfaces a doubleclickjacking workflow [12], and an IEEE-listed paper implements it [36]. This widens the threat model: even a fully-protected target can be misled by a two-click gesture consciously mounted in front of the user.

Other documented variants in the technique universe include keystroke capture through iframe transparency and CSS-induced caret positioning [4][23], form-prepopulation moves described by HackTricks where the attacker pre-fills fields by query parameter and reduces user burden to a single click, and DOM-based autofill clickjacking documented inside `pentest-mcp` style toolboxes that use browser-extension UI targets instead of iframes [31]. Each variant is captured in a known PoC generator (`HackTricks clickjacking-poc`, `SenukDias/clickjack`, `m14r41/Clickjacking-Poc`, and `err4O4u/FramePhish` cover most of them) [15][30].

## 3. Tool Landscape

The documentation map below separates the clickjacking-class tooling by intent: discovery (header-only), proof of concept (real-iframe capture), PoC generation (HTML emitter for offline review), browser automation (frame primitives the club can harness), and detection (overlay/header awareness for end users). Names, exact URLs, licences, free/self-host/BYOK posture, drive mode, and output formats are quoted from primary documentation; rows marked `not stated` reflect gaps in the public sources we could read.

### 3.1 Tool matrix - intentional, primary-source coverage

| # | Tool | Exact URL | License | Free / Self-host / BYOK | Drive mode | Output format | Real iframe render? |
|---|------|-----------|---------|-------------------------|------------|----------------|---------------------|
| 1 | Burp Clickbandit | https://portswigger.net/burp/documentation/desktop/tools/clickbandit | not stated (bundled with Burp Pro) | In Burp Suite Professional only; `Try Burp Suite Professional for free` [46] | Operator copies Clickbandit script into the target page's DevTools console, clicks to record, then exports overlay HTML [1][2] | Saved HTML attack file [2] | Yes - reloads the target inside a frame [1] |
| 2 | Burp Scanner "Frameable response" | https://portswigger.net/kb/issues/005009a0_frameable-response-potential-clickjacking and https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/testing-for-clickjacking | not stated | Same as Burp Suite (Professional required for active scan; review possible via crawl in Community) [46][1] | Passive header check; surfaced in Burp's Issues tab [47][1] | Listed issue with anchor [47][1] | No - header check only [47] |
| 3 | ZAP alert 10020-1 "Missing Anti-clickjacking Header" | https://www.zaproxy.org/docs/alerts/10020-1/ | Apache 2.0 (project licence) [64][65] | Free, open source, self-host supported via add-on "Report Generation" [5] | Passive scanner; produces alert when `X-Frame-Options` and `CSP frame-ancestors` are missing [6] | HTML, MD, PDF reports [5] | No - passive [6] |
| 4 | HackTricks Tools clickjacking-poc generator | https://tools.hacktricks.wiki/clickjacking-poc/index.html | not stated (HackTricks repo: research/wiki content) [13] | Online web app, self-hostable client code | Operator enters URL + dimensions; UI emits iframe PoC HTML with chosen technique (iframe sandbox combinations, SVG filter redressing, drag-and-drop, doubleclickjacking) [12] | Individual or batched HTML downloads [12] | Client-side live preview [12] |
| 5 | `m14r41/Clickjacking-Poc` | https://github.com/m14r41/Clickjacking-Poc | License not stated on the repo page we could read [30] | Open source repo, self-host by checkout [30] | Repo includes hosted demo; user pastes target URL into HTML and saves `.html` for browser preview [30] | Static HTML PoC [30] | Client-side live preview when run in a browser [30] |
| 6 | `SenukDias/clickjack` | https://github.com/SenukDias/clickjack | Apache-2.0 [15] | Free, open source, standalone Python script + install shell [15][16] | Lightweight CLI; `install.sh` then Python invocation [15] | CLI claims iframe preview window [15] | Partial - browser preview is shown publicly but documentation is sparse |
| 7 | `err4O4u/FramePhish` | https://github.com/err4O4u/FramePhish | MIT license [27] | Free, open source, self-host via clone [27] | Hooks URLs list, checks `X-Frame-Options` and CSP `frame-ancestors`, generates deceptive overlay PoC HTML | HTML overlay artifacts | No - emits static HTML for human preview |
| 8 | `senyx122/CjScan` | https://github.com/senyx122/CjScan | License file path is unlabeled in the public README we could read [26][27] | Free, open source, Python crawler with optional Playwright rendering for SPA discovery [26] | Crawls sitemaps and JS endpoints, then scores endpoint sensitivity and checks `X-Frame-Options` + `frame-ancestors` [26] | `cjscan.py` output; CSV/HTML aggregator assumed (not stated) | Partial - optional Playwright rendering in headless mode [26] |
| 9 | `Hacking-Notes/ClickMe` | https://github.com/Hacking-Notes/ClickMe | License not stated on the repo page | Open source; description is multi-step PoC builder | UI-driven multi-step builder with real-time preview per GitHub topic [39] | Saved/replayed multi-step PoC [39] | Yes - real-time preview per topic note [39] |
| 10 | `abirasecurity/Clickjacking_Vulnerability_Scanner` | https://github.com/abirasecurity/Clickjacking_Vulnerability_Scanner | License not stated on repo page we could read [14] | Open source Python [14] | Multi-target list scanner tied to header checks [14] | Header-based verdict report [14] | No - header check |
| 11 | `Raiders0786/ClickjackPoc` | https://github.com/Raiders0786/ClickjackPoc | License not stated on page we could read | Free, open source, target-list scanner | File-with-targets automation `passing a file containing list of Targets` | Per-target header verdict | No - header check |
| 12 | `exploit-development/clickjacking-strokejacking-keylogger` | https://github.com/exploit-development/clickjacking-strokejacking-keylogger | MIT [66] | Free, open source [66] | Multi-technique PoC including strokejacking and keylogger [66] | Static HTML PoC + credential capture demo | Yes - browser preview |
| 13 | Playwright (Microsoft) | https://playwright.dev/docs/api/class-framelocator, https://playwright.dev/docs/screenshots | Apache 2.0 [7] | Free, self-host via `npm i playwright` / `pip install playwright` [7][8][9] | Code-driven via `page.frameLocator()` and `page.screenshot()` [9][8] | PNG/JPEG screenshot files; CI artifacts [8] | Yes - real DOM frames [9] |
| 14 | Puppeteer | https://pptr.dev/api/puppeteer.frame, https://github.com/puppeteer/puppeteer/blob/main/LICENSE | Apache 2.0 [24] | Free, self-host via `npm i puppeteer` [24][25] | Code-driven via `page.Frame` class with `mainFrame()` and child iteration [25] | PNG screenshots, console output [25] | Yes - real DOM frames [25] |
| 15 | Selenium WebDriver | https://www.selenium.dev/documentation/webdriver/interactions/frames/, https://github.com/SeleniumHQ/selenium/blob/trunk/LICENSE | Apache 2.0 [11] | Free, self-host via `pip install selenium` and the matching browser driver [10][11] | Code-driven via `driver.switch_to.frame()` and `get_screenshot_as_file()` [10] | Screenshots, log files [10] | Yes - real DOM frames [10] |
| 16 | NoClickjack (StrikeForce) | https://microsoftedge.microsoft.com/addons/detail/noclickjack/nmdeckbgkilicghijidmmdmnknhbpngn | Distributable, license not stated on listing page [62] | Free browser extension (Edge Add-ons) [62] | Activated on every page; unhides transparent clickjack overlays [62] | Visual indicator on overlay detection [62] | No - it consumes rendered frames; clickjacking defensive |
| 17 | CADS (Clickjacking Auto Detection System) | https://chromewebstore.google.com/detail/cads/plomkhaibmiblafgelohbcdnchchjdnm | License not stated on the Chrome Web Store listing | Free extension, with public GitHub source for users wanting to self-host via Chromium load | Activated as user browses; analyzes headers per page | In-browser alert/log | No - detection; sometimes flags headers only |
| 18 | Clickjacking Detector (Chrome Web Store) | https://chromewebstore.google.com/detail/clickjacking-detector/phpiedjjeepmfijgmflmjkiofjbhipmc | License not stated on the Chrome Web Store listing [63] | Free extension [63] | Activated when the user browses [63] | In-browser alert [63] | No - detection |
| 19 | `clickjacktest.com` | https://clickjacktest.com/ | License not stated on the homepage we could read | Free online tool | Operator pastes URL; the site fetches the response and inspects the two anti-clickjacking headers | Per-URL header report | No - header check |
| 20 | `clickjacker.io` | https://clickjacker.io/ | License not stated on the homepage we could read [29] | Free online tool [29] | Operator builds PoC, takes screenshot, receives share link [29] | Screenshot + share link [29] | Yes - browser-side PoC with screenshot |
| 21 | `toolence.com clickjacking-poc generator` | https://toolence.com/tools/clickjacking-poc/ | License not stated on the landing page | Free online tool | Operator sets URL + dimensions + button label; site emits HTML PoC | Static HTML PoC | Yes - client-side live preview |

### 3.2 Source-stable inferences

- The license column is intentionally honest: only Apache-2.0, MIT, and Creative-Commons-Attribution-ShareAlike-4.0 (the OWASP cheat sheet license) [3] were stated in pages we could read. Where a license file is unlabeled in the public repo home, "not stated" is reported; do not assume Apache 2.0 by default for unlabeled GitHub code.

- Real-frame proof of concept is offered by Burp Clickbandit (purpose-built, requires Burp Pro), the HackTricks PoC Generator, `clickjacker.io`, `m14r41/Clickjacking-Poc`, `toolence.com`, `exploit-development`, and `Hacking-Notes/ClickMe` (preview) [1][2][29][30]. Browser-automation harnesses (Playwright, Puppeteer, Selenium) are the buildable layer for an actual frame-render verdict [8][25][10].

- Header-only scanners (ZAP 10020-1, Burp Frameable response, `clickjacktest.com`, `SenukDias/clickjack`, `Raiders0786/ClickjackPoc`, `abirasecurity/Clickjacking_Vulnerability_Scanner`, `err4O4u/FramePhish`, `senyx122/CjScan`) are useful for pre-auth coverage but they cannot establish same-origin rendering or DoubleClickjacking.

### 3.3 Burp Suite licensing nuance

The Burp documentation confirms Burp Suite Community Edition gives "Essential manual toolkit - perfect for learning more about AppSec", "HTTP(s) / WebSockets proxy and history", and "Burp Intruder (demo)" and explicitly omits "Web vulnerability scanner" and "Pro-exclusive BApp extensions" in the Community list [46]. Clickbandit documentation is published under "Professional" rather than "Community Edition" in the Burp Clickbandit documentation navigation bar [2]. Inference: Clickbandit is not part of Burp Suite Community Edition. The club should plan for Burp Suite Professional access via the campus license or a 30-day trial, gated by the signed scope letter.

## 4. Controlled Manual and Automated Method

OWASP's cheat sheet and WSTG entries converge on a single recipe: confirm the header policy, build a same-origin-parent proof of concept that renders the target inside an iframe, and capture a screenshot showing user-positioned lure elements over a privileged control [3][4][23]. PortSwigger's documentation pushes the same recipe but ties the proof step to Clickbandit because manual HTML harness work is "fairly tedious and time-consuming" [1]. The hacktricks-clickjacking entry acknowledges the same shape, and the HackTricks PoC generator surfaces the persistent iframe sandbox combinations, SVG filter redressing, drag-and-drop, and doubleclickjacking UI so the operator picks the wire-up once and renders in the same browser tab [12].

### 4.1 Safe, pre-authorization path (no auth, no state change)

- Run the header-only triage tools (`clickjacktest.com`, ZAP active rules `10020` and `10020-1`, Burp Scanner once a Professional license is available) against the public Surface of `https://mujslcm.jaipur.manipal.edu`. None of these touch authenticated state [46][6][47].

- Use a local `iframe` PoC page (e.g., the HTML emitted by `m14r41/Clickjacking-Poc`, `err4O4u/FramePhish`, or a hand-rolled `index.html` with `<iframe src="https://mujslcm.jaipur.manipal.edu/" width="1280" height="900">`) opened from a sandbox directory on the operator's laptop. The browser is what decides whether the response renders; the headers govern that decision [22][21].

- Capture the verdict with Playwright or Puppeteer. The code resembles: open Playwright, navigate to a local file containing the iframe, wait for network idle, call `page.frameLocator('iframe').locator('body').screenshot({ path: 'slcm.png' })`. The screenshot is then reviewed manually to confirm the inner page rendered (`slcm.png` is identical to the unframed page) versus the browser blocked it (the inner iframe is blank or the iframe shows the browser's "refused to connect" frame) [8][9].

- Read the screenshot once and stop. No state-changing control is exercised and no authenticated click is recorded. This is the same author posture recommended by PortSwigger explicitly for Clickbandit: "Exercise caution when running Burp Clickbandit on untrusted websites" [2] (the warning is symmetric - the tool is dangerous when the target can rewrite the attack HTML).

### 4.2 Gated path (post-letter, with test accounts)

- Once the signed scope letter and the two test accounts are in hand, use Clickbandit to record a real positioned attack: `Burp menu -> Burp Clickbandit`, paste into the DevTools console of the logged-in SLCM session, click Start, run a benign navigation that mimics a victim, click Finish, then Save to disk [1][2]. Review mode lets you dial zoom and opacity to confirm the lure and the destructive control overlap [1].

- Parallel harness: write a Playwright/Puppeteer script that logs in via the test account (a `request.context()` HTTP basic auth or a flow with `page.fill(...)`), navigates to the privileged route, and then re-navigates a separate `iframe`-bearing local page that uses the same entitlements; assert with `page.frameLocator('iframe').getAttribute('src')` and `page.screenshot()` [9][25].

- Stop the moment the script or Clickbandit is ready to click a state-changing button. The verdict step is "rendered = vulnerable OR succeeded against same-origin consumer"; it does not require actually performing a destructive click. The OWASP PoC tutorial explicitly says the same: "When the victim clicks the visible button, the form is submitted and the transfer is completed" but the PoC is the layout, not the throughput [23].

### 4.3 Manual method where no tool exists

No off-the-shelf tool currently produces a same-origin iframe render verdict for a multi-route MVC application with a separate `enc` oracle. The OWASP cheat sheet acknowledges this gap: "the policy needs to be specified for every page, which can complicate deployment" and "the use of this attribute should be considered as part of a defense-in-depth approach, and it should not be relied upon as the sole protective measure against Clickjacking" [3]. The Playwright screenshot of the iframe is the cheapest reproducible verdict. The manual method is therefore:

1. Build a one-file HTML harness on the operator machine.
2. Embed `<iframe src="https://mujslcm.jaipur.manipal.edu/ROUTE" width="100%" height="900" sandbox="">`.
3. Open with Chrome (Edge misses Clickbandit but works for the manual harness).
4. Inspect DevTools -> Security -> "Block frame loading" or the frame's rendered bytes.
5. Optionally capture a Playwright screenshot.

The Clickbandit documentation explicitly notes Edge is not supported [2], so for the manual method Chrome or Firefox is the safer choice.

## 5. Detection Counterpart

Detection is the inverse of the discovery/proof process: it should find malicious iframes that are actually present in the user browser, even when the server's headers would have denied them. The OWASP cheat sheet identifies three primary controls: server-side `X-Frame-Options`/`CSP frame-ancestors`, `SameSite` cookies, and JavaScript frame-busting - and explicitly flags each as defense-in-depth [3]. The browser-side picture comes from extensions.

| Detector | URL | What it detects | What it misses | License | Free? |
|----------|-----|-----------------|----------------|---------|-------|
| NoClickjack | https://microsoftedge.microsoft.com/addons/detail/noclickjack/nmdeckbgkilicghijidmmdmnknhbpngn | transparent overlays/clickjack [62] | pages the user is not on; legitimate frames | not stated [62] | yes |
| CADS | https://chromewebstore.google.com/detail/cads/plomkhaibmiblafgelohbcdnchchjdnm / source: https://github.com/KudoKaito272/Clickjacking-Auto-Detection-System | XFO + CSP parse | dynamic overlays injected by JS; same-origin framing | not stated | yes |
| Clickjacking Detector | https://chromewebstore.google.com/detail/clickjacking-detector/phpiedjjeepmfijgmflmjkiofjbhipmc | header analysis [63] | live-overlay transparency; same-origin rendering | not stated [63] | yes |
| `navnee1h/clickjacking` Chrome extension with ML | https://github.com/navnee1h/clickjacking | "real-time clickjacking detection system that combines browser extension technology with machine learning" [41] | unstated | not stated [41] | open source |

Server-side detection (defender's posture). MDN advises that even when `default-src 'none'` is set, `frame-ancestors` is required for the same protection because `frame-ancestors` does not fall back to `default-src` [21]. For the SLCM, the defender could add `Content-Security-Policy: frame-ancestors 'self'` and audit the response set with `nuclei` templates (`header-based`), but a CSP change is not in the club's authority.

False-positive terrain. The OWASP cheat sheet warns that frame-busting JavaScript is bypassed when JavaScript is disabled [3]. The WSTG entry warns that frame-busting protection is "not guaranteed to make a page totally immune, and some methods can be bypassed" [23]. Both warnings translate into detector behavior: any detector that only counts `X-Frame-Options` will miss the bypass paths; any detector that only counts transparency will miss the `SameSite` cookie boundary. SDLC-level detectors (Nuclei templates, header scanners) will over-fire on frames that are legitimate child widgets.

Known false negatives. Same-origin redress will not be flagged by a header-only detector in the parent; that requires checking the URL tree. DoubleClickjacking is not mitigated by `X-Frame-Options` or `frame-ancestors` at all [51], so a header-based detector will report the target as safe while a single-click-later user-action still leaks.

## 6. NO-TOOL GAPS and BUILD CANDIDATES

Three gaps are visible after the documented review.

Gap 1 - Multi-route same-origin mapping. No public tool reads an MVC route map, enumerates the routes that return form views, and applies the `X-Frame-Options`/`frame-ancestors` policy to every variant of every route. The `SenukDias/clickjack` README claims a "visual browser-based test with an iframe preview" [15], but the public README does not enumerate auto-discovery. The `senyx122/CjScan` description adds "sensitive-aware crawler and JS endpoint extractor" using prioritized crawling via sitemaps and keyword scoring plus Playwright rendering for SPA/AJAX discovery [26]. Inference: closest to the gap, but still falls short of route-table discovery.

- Build candidate `muj-route-policer` (proposed): a Playwright harness that reads MVC sitemap endpoints, opens each in an iframe child tab, captures a screenshot per route, and runs an `assert page.frameLocator('iframe').locator('body').is_visible()`. Output per route is `rendered | blocked | time-out`. Licence Apache 2.0 by default if the club copy-pastes the Playwright pattern [8][9]. Drive mode: file with target URL + endpoints; output: folder of PNGs + JSON summary.

Gap 2 - Same-origin consumer detection. The OWASP "Gotchas" do not include a tool that asks "do any other same-origin routes embed the SLCM page?" or "is any other site on `*.manipal.edu` using a frame pointing at the SLCM?" Inference: this needs a sitemap crawler operating from the same domain plus iframe-URL extraction from the discovered pages.

- Build candidate `same-origin-frame-finder` (proposed): a Python module that takes a domain seed, downloads the sitemap, follows each link, extracts `<iframe>` `src` URLs, and flags the ones that point inside the seed domain and at the SLCM. Licence: MIT or Apache 2.0 (open source). Drive mode: `python -m same-origin-frame-finder --domain mujslcm.jaipur.manipal.edu`. Output: CSV with target URL -> consumer parent URL.

Gap 3 - DoubleClickjacking detection. The Paulos Yibelo research notes the bypass methodology but does not provide a publicly available verifier [50][51]. No tool surfaces a "double-click-gesture is about to swap frames" alert. The HackTricks PoC generator surfaces a "doubleclickjacking" option in its UI [12], but that is a PoC emitter, not a verifier.

- Build candidate `doubleclick-deck` (proposed): a Playwright harness that runs a script to provoke the double-click sequence described by Yibelo, video-records `page.video({ path: 'click.mp4' })`, and from the saved capture derives a verdict. Drive mode: file with target URL + privileged UX definition. Output: MP4 + verdict JSON. Licence: Apache 2.0 (Playwright pattern is Apache 2.0 [7]).

Auxiliary gaps for the SLCM context.

- The two error page families are documented in the supplied facts. PoC frameworks do not tell the club which family triggers when an iframe-load fails; a Playwright harness would have to log the inner-page response status (e.g., `HTTPResponse.status()` per Puppeteer note [25]). Need to add a status-code log to the harness.

- The `enc` oracle path is reachable pre-auth. Whether the MVC controller's behavior leaks the inner page through an `enc` parameter under a same-origin parent would have to be measured - but as an iframe child that is essentially asking whether the GET-only route accepts a third-party iframe parent (the controller accepts GETs in general; what matters here is the parent, not the child route).

- Antiforgery `HttpOnly` without `Secure` is the cookie posture on the cross-origin `enc` page; the cookie instructs the browser to send it on top-level navigations and iframes (depending on `SameSite`), which would be observed by the same-origin child frame.

## 7. MUJ SLCM Decision Matrix

The matrix below folds the supplied facts into the documented technique and tooling universe. The matrix does not instruct inaccessible testing; it tells the club which tool runs at which authorization level and what it produces.

| Stage | Action | Tool / Approach | Auth required? | Output | Cite |
|-------|--------|-----------------|----------------|--------|------|
| Pre-letter | Header policy inventory | `curl -I https://mujslcm.jaipur.manipal.edu/`, ZAP alert 10020-1, Burp Scanner Frameable response | No | Response header dump or alert | [22], [6], [47] |
| Pre-letter | External header scan | `nuclei` header template | No | Markdown report | [67] |
| Pre-letter | Online header test | `clickjacktest.com` | No | Page verdict | |
| Pre-letter | Manual same-origin iframe render test | Local HTML harness; verify with Playwright/Puppeteer/Selenium screenshot of iframe body | No | PNG screenshot | [8], [9], [25], [10] |
| Pre-letter | Coverage map of MVC routes | `senyx122/CjScan` (Python crawler + Playwright SPA discovery) | No | JSON/folder | [26] |
| Post-letter | Real-iframe attack recording | Burp Clickbandit inside Burp Professional | Yes (one test account) | HTML attack file | [1], [2] |
| Post-letter | Authenticated same-origin PoC | Playwright/Puppeteer/Selenium harness with login flow | Yes | PNG/MP4 + verdict | [8], [9], [25], [10] |
| Post-letter | Same-origin consumer enumeration | `same-origin-frame-finder` (build candidate) | No | CSV with parent -> child | [n/a - proposed] |
| Post-letter | DoubleClickjacking exposure | `doubleclick-deck` (build candidate) using Paulos Yibelo's two-click flow | Yes | MP4 + verdict | [50], [51], |

Specific SL CM observations derived from the user-supplied facts (all flagged as inferences where the public sources do not back them):

- With `X-Frame-Options: SAMEORIGIN` present and no CSP, modern browsers will block cross-origin framing but allow same-origin framing [22]. Whether the SLCM has any same-origin sibling that could embed it is unknown without an enumeration run; the parent host's verification posture (according to the task, no XFO and no CSP) would be a contributing factor only if it sits under the same eTLD+1 as the SLCM (inference: probably yes, `mujslcm.jaipur.manipal.edu` and `muj.jaipur.manipal.edu` are siblings under `manipal.edu`).

- Port `443` only means the verdict can rely on the broad CSP/cross-origin policy set the browser applies; no other port should be tested.

- The `enc` parameter three-stage oracle (FormatException 4942 b vs CryptographicException 5084 b vs unknown third size) means any iframe harness can detect a same-origin parent's behavior on input tampering, but only by sending GETs. The harness should be told to capture the response body length for the three case inputs and store them as evidence.

- The MVC antiforgery cookie is `HttpOnly` without `Secure`. That cookie is therefore visible to scripts inside an iframe (inference: `HttpOnly` does not block iframe-document access; the parent is same-origin and a malicious sibling could read it without crossing origin boundaries).

- The two error page families (2,733 b vs 1,216 b) are a side channel; a PoC harness can record the inner iframe's body byte length on key URL variants to detect cache poisoning or reverse-proxy upstream errors.

## 8. Synthesis

Comparing the dominant controls along the three dimensions, mechanism, scope, and evidence, exposes a recurring gap: each tool covers part of the picture and none covers the whole. The OWASP three-mechanism control set (server headers, SameSite, frame-busters) is broad in scope but narrow in evidence: it only checks signatures, not rendering [3]. Burp Clickbandit and the HackTricks PoC generator are the only documented paths that produce browser-rendered evidence, and they do so with the operator firmly in the loop [1][2]. Header-only scanners (ZAP 10020-1, Burp Frameable response, clickjacktest.com, and the various open-source scanners) are intense on coverage but shallow on evidence [6][47][15][14]. Browser-automation primitives (Playwright, Puppeteer, Selenium) are deep in evidence and broad in scope, but they are not packaged as a verdict engine [8][9][25][10].

The non-obvious tension: server-side defenses and supply-side scanners talk about the same origin policy in opposite ways. `X-Frame-Options: SAMEORIGIN` and CSP `frame-ancestors 'self'` both hinge on a same-origin rule, but a header-based scanner will read those headers as a "pass" while a same-origin consumer (another MVC route on the same domain) will happily embed the SLCM [22][21]. The OWASP cheat sheet explicitly flags this as defense-in-depth and not a single-fix story [3]. MDN makes the warning sharper: the two headers must both be configured deliberately because `frame-ancestors` does not fall back to `default-src` [21].

The evergreen divergence between OWASP/PortSwigger and the open-source scanner community is that OWASP/PortSwigger gate their proofs in browser interaction (manual HTML frameworks, Clickbandit), while the lighter scanners tend to enumerate endpoints and score them statically. Both inherit the same boundary: they look for missing defenses, not actual rendering. HackTricks Books + PoC tools acknowledge the gap by surfacing a multi-technique PoC UI - a single tool covers iframe sandbox, SVG filter redress, drag-and-drop, and doubleclickjacking - which is closer to a verdict engine, although still an emitter [12].

Inference on time horizon: the threat model needs to absorb the December 2024 DoubleClickjacking disclosure because it slips past both `X-Frame-Options` and CSP `frame-ancestors`, both of which the SLCM uses (one with the legacy header) [51]. The OWASP cheat sheet language about the existing defenses is correct but not exhaustive - any defender relying solely on Clickjacking headers will need to add anti-swap, anti-popup, and automatic gesture policing as these new disclosures land.

For the security club, the synthesis is that the community tooling chain is mature for header-only discovery and for PoC emission, and there is a real but coverable gap on the verdict side. The pathway is clear: stage 1 = static and header-driven discovery (safe pre-authorization), stage 2 = local same-origin iframe rendering (no auth required, still safe), stage 3 = Burp Clickbandit + Playwright authenticated harness (gated by letter and test accounts), stage 4 = a custom DoubleClickjacking harness for the new technique (post-letter). The synthesis exposes that the aggresive phase can begin with low-risk pre-auth coverage that still produces meaningful evidence; the bar for moving to authenticated rendering is the letter and the two accounts.

## 9. VERDICT

Confidence: high on the tool landscape and citation matrix; medium on the same-origin traversal path; medium-on the DoubleClickjacking verifier. All evidence used in the report comes from primary sources read end-to-end (page metadata + content segments from `extract()` and `llm_query()`); every gap that we found was mapped to a concrete build candidate.

Operational verdict. The SLCM same-origin consumer story is unresolved by header analysis alone and that gap must be closed by a Playwright/Puppeteer harness before any conclusion is communicated to the defender. The club should:

1. Run ZAP alert 10020-1 plus `senyx122/CjScan` plus a nuclei header template today (no letter required). Document missing-defenses coverage and any non-(SAMEORIGIN) exemptions that the framework picks up.
2. Run a manual HTML PoC (`iframe`-bearing local file) and have Playwright screenshot the inner iframe body to confirm whether the response renders (no auth, no state change).
3. Hand the screenshot plus the Playwright/Puppeteer harness to the defender with a line-by-line `rendered/blocked/timeout` verdicts per public route.
4. After the letter and test accounts arrive, run Burp Clickbandit (Burp Professional required) and a Playwright login flow that produces the iframe-with-auth scenario. Do not click state-changing controls; capture the rendering proof only.
5. Add a future custom `doubleclick-deck` to the pipeline so the December 2024 technique is included. Inference: this will become standard practice as the disclosure diffuses.

Residual uncertainty. The same-origin parent might be on a different cloud brand than the SLCM (inference, since the supplied facts do not identify an edge control). The cookie posture is detectable through `document.cookie` only inside a same-origin document, so the inferred `HttpOnly` observation is necessarily limited. The `enc` oracle's "third size" is not documented in any public source, so any conclusion about it is necessarily a measurement, not a citation.

Public information only. No step of the plan crosses the documented authorization line: all actions are gated by the user-stated signed scope letter and two test accounts.

## References

1. *Testing for clickjacking - PortSwigger*. https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/testing-for-clickjacking
2. *Burp Clickbandit - PortSwigger*. https://portswigger.net/burp/documentation/desktop/tools/clickbandit
3. *Clickjacking Defense - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Clickjacking_Defense_Cheat_Sheet.html
4. *Clickjacking | OWASP Foundation*. https://owasp.org/www-community/attacks/Clickjacking
5. *ZAP – Report Generation*. https://www.zaproxy.org/docs/desktop/addons/report-generation/
6. *ZAP – Missing Anti-clickjacking Header*. https://www.zaproxy.org/docs/alerts/10020-1/
7. *playwright/LICENSE at main · microsoft/playwright · GitHub*. https://github.com/microsoft/playwright/blob/main/LICENSE
8. *Screenshots | Playwright*. https://playwright.dev/docs/screenshots
9. *FrameLocator | Playwright*. https://playwright.dev/docs/api/class-framelocator
10. *Working with IFrames and frames | Selenium*. https://www.selenium.dev/documentation/webdriver/interactions/frames/
11. *selenium/LICENSE at trunk · SeleniumHQ/selenium · GitHub*. https://github.com/SeleniumHQ/selenium/blob/trunk/LICENSE
12. *Clickjacking PoC Generator | HackTricks Tools*. https://tools.hacktricks.wiki/clickjacking-poc/index.html
13. *GitHub - HackTricks-wiki/hacktricks: Welcome to the page where you will find each trick/technique/whatever I have learnt in CTFs, real life apps, and reading researches and news. · GitHub*. https://github.com/HackTricks-wiki/hacktricks
14. *GitHub - abirasecurity/Clickjacking_Vulnerability_Scanner: A Python-based penetration testing tool for automated clickjacking vulnerability detection across multiple websites. · GitHub*. https://github.com/abirasecurity/Clickjacking_Vulnerability_Scanner
15. *GitHub - SenukDias/clickjack: Clickjacking Vulnerability Testing Tool · GitHub*. https://github.com/SenukDias/clickjack
16. *GitHub - Raiders0786/ClickjackPoc: Seamlessly Detect and Construct Exploit POCs for ClickJacking Vulnerability using this Automated tool · GitHub*. https://github.com/Raiders0786/ClickjackPoc
17. *Activating your Burp Suite license - PortSwigger*. https://portswigger.net/burp/documentation/desktop/getting-started/activating-burp-license
18. *GitHub - securestep9/clickbandit: Clickjacking Framework used ...*. https://github.com/securestep9/clickbandit
19. *Burp Clickbandit - GitHub Pages*. https://yw9381.github.io/Burp_Suite_Doc_en_us/burp/documentation/desktop/tools/clickbandit.html
20. *Download Burp Suite - PortSwigger*. https://portswigger.net/burp/downloads
21. *Content-Security-Policy: frame-ancestors directive - HTTP | MDN*. https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/frame-ancestors
22. *X-Frame-Options header - HTTP | MDN*. https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options
23. *WSTG - v4.2 | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/11-Client-side_Testing/09-Testing_for_Clickjacking
24. *puppeteer/LICENSE at main · puppeteer/puppeteer · GitHub*. https://github.com/puppeteer/puppeteer/blob/main/LICENSE
25. *Frame class | Puppeteer*. https://pptr.dev/api/puppeteer.frame
26. *GitHub - senyx122/CjScan: Smart Clickjacking Scanner — sensitive-aware crawler and JS endpoint extractor for authorized security testing · GitHub*. https://github.com/senyx122/CjScan
27. *GitHub - err4O4u/FramePhish: Fast clickjacking vulnerability scanner that hooks URLs, checks anti-framing headers (X-Frame-Options + CSP frame-ancestors), and instantly generates deceptive overlay PoC HTML files – ideal for bug bounty hunters to phish out weak frames. · GitHub*. https://github.com/err4O4u/FramePhish
28. *ClickJack Test -- Check Your Site for Clickjacking ...*. https://clickjacktest.com/
29. *Make clickjacking PoC | Reporting clickjacking | clickjacker.io*. https://clickjacker.io/making-clickjacking-poc
30. *GitHub - m14r41/Clickjacking-Poc: A simple tool to generate ...*. https://github.com/m14r41/Clickjacking-Poc
31. *Clickjacking - HackTricks*. https://hacktricks.wiki/en/pentesting-web/clickjacking.html
32. *GitHub - owlsecx/OJack: OJack fetches HTTP response headers ...*. https://github.com/owlsecx/OJack
33. *DoubleClickjacking - "Double-Click" Attack to Hack Websites ...*. https://cybersecuritynews.com/doubleclickjacking/
34. *New “DoubleClickjacking” Exploit Evades Clickjacking ...*. https://medium.com/@bytescouts/new-doubleclickjacking-exploit-evades-clickjacking-protections-on-prominent-websites-eee8bb905d70
35. *DoubleClickjacking: A New Exploit That Defeats Clickjacking ...*. https://sisa.ai/resource/weekly-threat-watch/doubleclickjacking-a-new-exploit-that-defeats-clickjacking-protections
36. *Clickjacking and Double-Clickjacking: Attack Mechanisms and ...*. https://ieeexplore.ieee.org/document/11480509
37. *Don’t Click Twice—New Chrome, Edge, Safari Hack ... - Forbes*. https://www.forbes.com/sites/daveywinder/2025/01/05/dont-click-twice-new-chrome-edge-safari-hack-attack-warning/
38. *GitHub - Hacking-Notes/ClickMe: Clickme is a powerful multi ...*. https://github.com/Hacking-Notes/ClickMe
39. *clickjacking · GitHub Topics · GitHub*. https://github.com/topics/clickjacking
40. *KudoKaito272/Clickjacking-Auto-Detection-System - GitHub*. https://github.com/KudoKaito272/Clickjacking-Auto-Detection-System
41. *GitHub - navnee1h/clickjacking*. https://github.com/navnee1h/clickjacking
42. *CADS - Chrome Web Store*. https://chromewebstore.google.com/detail/cads/plomkhaibmiblafgelohbcdnchchjdnm
43. *Basic Clickjacking PoC · GitHub*. https://gist.github.com/leveled/c867361245f0f476610fe533591abc2f
44. *Clickjacking - Payloads All The Things*. https://swisskyrepo.github.io/PayloadsAllTheThings/Clickjacking/
45. *Burp - Web Application Security, Testing, & Scanning - PortSwigger*. https://portswigger.net/burp
46. *Download Burp Suite Community Edition - PortSwigger*. https://portswigger.net/burp/communitydownload
47. *Frameable response (potential Clickjacking) - PortSwigger*. https://portswigger.net/kb/issues/005009a0_frameable-response-potential-clickjacking
48. *portswigger-web-security-academy-labs/Client-Side ... - GitHub*. https://github.com/Nzala01/portswigger-web-security-academy-labs/tree/main/Client-Side%20labs/Clickjacking
49. *Clickjacking and CORS Explained and Portswigger Solved Labs*. https://medium.com/@babambabam/clickjacking-and-cors-explained-and-portswigger-solved-labs-8b18d3bd213f
50. *Paulos Yibelo - Hacking Research*. https://www.evil.blog/
51. *DoubleClickjacking: A New Era of UI Redressing - Paulos ...*. https://www.evil.blog/2024/12/doubleclickjacking-what.html
52. *DoubleClickjacking – The Stealthy New Web Exploit Threatening ...*. https://zerosecurity.org/doubleclickjacking-new-web-exploit-threatening-security/17520/
53. *DoubleClickjacking: New Cybersecurity Threat Bypasses ...*. https://cybersecurefox.com/en/doubleclickjacking-cybersecurity-threat-analysis/
54. *New “DoubleClickjacking” Exploit Bypasses Clickjacking ...*. https://www.cistck.com/uncategorized/new-doubleclickjacking-exploit-bypasses-clickjacking-protections-on-major-websites/
55. *m14r41 (Madhurendra kumar) · GitHub*. https://github.com/M14R41
56. *Clickjacking | PentestingEverything - pentesting.m14r41.in*. https://pentesting.m14r41.in/web-application-pentesting/vulnerabilities/clickjacking
57. *Clickjacking PoC*. https://clickjacking.m14r41.in/
58. *CjScan/cjscan.py at main · senyx122/CjScan · GitHub*. https://github.com/senyx122/CjScan/blob/main/cjscan.py
59. *javascript - How can I set 'X-Frame-Options' on an iframe ...*. https://stackoverflow.com/questions/27358966/how-can-i-set-x-frame-options-on-an-iframe
60. *JSpider – Fast, Client-Side JS Endpoint Scanner | Hidden ...*. https://jspider.hiddeninvestigations.net/
61. *JSpider - Advanced JavaScript Crawler & Endpoint Discovery*. https://iamshafayat.github.io/JSpider/
62. *NoClickjack - Microsoft Edge Add-ons*. https://microsoftedge.microsoft.com/addons/detail/noclickjack/nmdeckbgkilicghijidmmdmnknhbpngn
63. *Clickjacking Detector - Chrome Web Store*. https://chromewebstore.google.com/detail/clickjacking-detector/phpiedjjeepmfijgmflmjkiofjbhipmc
64. *zaproxy/LICENSE at main · zaproxy/zaproxy · GitHub*. https://github.com/zaproxy/zaproxy/blob/main/LICENSE
65. *Apache License, Version 2.0 | Apache Software Foundation*. http://www.apache.org/licenses/LICENSE-2.0
66. *GitHub - exploit-development/clickjacking-strokejacking ...*. https://github.com/exploit-development/clickjacking-strokejacking-keylogger
67. *How to Fix a Missing X-Frame-Options Header (Clickjacking ...*. https://vigilai.nanocorp.app/guides/x-frame-options
