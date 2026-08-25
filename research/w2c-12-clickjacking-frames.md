# MUJ SLCM Clickjacking Exposure and Safe Validation Plan

## Executive Summary

- **Confirmed Header Split**: A public SecurityHeaders capture dated **25 August 2026** shows `X-Frame-Options: SAMEORIGIN` on `mujslcm.jaipur.manipal.edu`, while the corresponding `slcm.manipal.edu` capture shows neither XFO nor CSP [17][15]. -> Treat the first host as partially protected and the second as having a confirmed framing-control gap on its public landing response.
- **Modern Policy Gap**: The MUJ response has no Content-Security-Policy header, and the MAHE SLCM response lacks both CSP and XFO [17][15]. Browsers allow embedding when neither XFO nor `frame-ancestors` is delivered [4]. -> Deploy an explicit `frame-ancestors` policy on every HTML response, with XFO retained as legacy defense in depth.
- **Stack Fingerprint Confirmed, Edge Assumption Not Confirmed**: The MUJ scan discloses `Microsoft-IIS/10.0`, `x-aspnetmvc-version: 5.3`, `x-aspnet-version: 4.0.30319`, and `x-powered-by: ASP.NET` [17]. The SLCM scan discloses IIS 10 and ASP.NET 4.0.30319 [15]. Public urlscan records map both hosts to Microsoft AS8075 and Azure DNS, not to an Akamai ASN [14][13]. -> Configure the origin first; treat Akamai as an unverified architecture input until the owner supplies the property and request-flow diagram.
- **Identity Link Is Partial**: The MUJ landing page publicly exposes general and parent/student sign-in choices [12], and an official MUJ document describes Office 365 email setup and MFA, but those facts do not prove that SLCM authentication itself is Microsoft Entra based. -> Include Entra callback and silent-iframe behavior in the owner interview, but do not report "Microsoft 365 identity" as independently confirmed for SLCM.
- **Keen Theme Is Context, Not Causation**: The user's Keen-theme premise was consistent with a public raw-markup spot check at `https://mujslcm.jaipur.manipal.edu/`, but the authenticated action inventory was not publicly visible. -> Do not equate an old-looking theme with exploitability; enumerate actual state-changing controls only inside an authorized test account.
- **Frame Busting Is Not a Primary Control**: RFC 7034 documents historical variation in ancestor-chain treatment and warns that XFO alone is not sufficient for every attack vector [8]. A Stanford study found widespread script-based frame-busting weaknesses [22]. -> Test JavaScript busting for regression evidence, but fix the response policy rather than trying to perfect client-side scripts.
- **Drag-And-Drop Risk Is Conditional**: Clickjacking requires a victim to interact with hidden or disguised actionable content [6][9]. -> Mark drag-and-drop as "not demonstrated" unless an authorized session reveals a draggable source or drop target that changes data, discloses data, uploads a file, or confirms an action.
- **Double-Frame Testing Has Standards Value**: Modern `frame-ancestors` checks every ancestor and cancels the load if any ancestor is not allowed [2], while RFC 7034 records inconsistent historical XFO behavior [8]. -> Use two tester-controlled origins and a nested-frame matrix to verify current supported browsers without publishing an exploit page.
- **Cookies Reduce Some Paths, Not the Policy Gap**: The public SLCM response sets its ASP.NET session cookie `HttpOnly; SameSite=Lax` [15]. Lax generally excludes iframe navigations from authenticated cross-site cookie delivery [21], but this one unauthenticated response does not reveal every authentication cookie or same-site subdomain condition. -> Record every cookie on the authorized account and retain framing controls regardless of cookie behavior.
- **Priority Is Consistency, Then Workflow Hardening**: The highest-value change is one centrally managed policy across success, redirect, login, error, download, and legacy routes. -> Prefer `frame-ancestors 'none'` where no legitimate embedding exists; use a minimal allowlist only where the business owner identifies a real embedding dependency.

**Bottom line:** the report confirms a real control inconsistency, not a completed account-impact exploit. `slcm.manipal.edu` has the clearest public clickjacking exposure because the captured landing response lacks both browser-enforced framing controls. MUJ is better because it sends XFO SAMEORIGIN, but it still lacks the modern CSP directive and needs route-wide verification.

## Scope, Ethics, and Evidence Grades

This is a public-information assessment for a university security club. It does not authorize testing. NIST SP 800-115 treats a security assessment as a planned project and calls for a documented assessment plan, scope, roles, logistics, sensitive-data handling, and incident procedures [18]. Therefore, every interactive test below is conditional on written permission from the system owner. Permission should name both hostnames, permitted paths, test dates, source addresses, test accounts, contacts, prohibited actions, data-retention rules, and a stop-work condition.

I cannot provide private internal chain-of-thought. Instead, the report provides an auditable evidence-to-conclusion rationale: source, observation, uncertainty, inference label, and decision. That is more reproducible than hidden reasoning and lets club reviewers challenge each step.

| Evidence grade | Meaning in this report | Examples | Permitted conclusion |
|---|---|---|---|
| Confirmed public observation | A dated public response capture or first-party page states the fact | XFO on MUJ; missing XFO on SLCM; IIS and ASP.NET headers | May be stated as confirmed for the captured URL and time |
| Standards-backed behavior | MDN, RFC, W3C, OWASP, NIST, Microsoft, or Akamai documents the mechanism | Ancestor checking; cookie SameSite behavior; header deployment | May explain expected browser or platform behavior |
| Analyst inference | Facts support a conclusion, but the conclusion is not directly observed | Azure indicators fail to corroborate Akamai | Must be prefixed with **Inference:** and kept conditional |
| Working hypothesis | User premise or raw observation lacks independent target-specific corroboration | Keen theme age; Microsoft 365 as the actual IdP; many authenticated actions | Must not be reported as a vulnerability |
| Not tested | Would require authorization, credentials, or state-changing interaction | Overlay success, drag/drop impact, nested-frame bypass | Must remain "not demonstrated" |

The club should avoid password guessing, account creation without approval, scraping authenticated pages, submitting forms, uploading files, altering profile or registration data, triggering email or MFA prompts, or hosting a public proof of concept. A valid demonstration uses a designated test account and a harmless, reversible action chosen by the owner. If no harmless action exists, stop after proving whether the browser renders the page in the test frame.

**Decision-ready insight:** the publicly verified issue is policy inconsistency. Impact beyond visual framing is unknown until authorized testing establishes an authenticated, consequential action and the browser/cookie conditions required to reach it.

## Asset and Trust-Boundary Map

The two public hosts should not be treated as one origin. `https://mujslcm.jaipur.manipal.edu` and `https://slcm.manipal.edu` have different hosts, IPs, response headers, cookies, and likely deployment paths. The MUJ landing page publicly offers sign-in and parent/student entry choices [12]. The SLCM landing page exposes sign-in-related visible content and a confirmation dialog, but public text alone does not show what action the dialog confirms [11].

| Component or boundary | Public evidence | Status | Security implication |
|---|---|---|---|
| MUJ landing response | IIS 10, MVC 5.3, ASP.NET 4.0.30319, XFO SAMEORIGIN [17] | Confirmed at 2026-08-25 11:44:58 UTC [17] | Cross-origin framing should be blocked by current XFO-aware browsers, subject to route consistency |
| SLCM landing response | IIS 10, ASP.NET 4.0.30319, no XFO or CSP shown [15] | Confirmed at 2026-08-25 11:45:00 UTC [15] | Browser has no captured framing policy for this response |
| MUJ cookies on public response | Anti-forgery cookie is `HttpOnly`, but the capture shows no SameSite attribute [17] | Confirmed only for that cookie | Does not reveal the authenticated session-cookie policy |
| SLCM cookies on public response | `ASP.NET_SessionId` is `HttpOnly; SameSite=Lax` [15] | Confirmed only for that response | Cross-site framed requests may omit this cookie, but other cookies and same-site cases remain unknown |
| Public hosting/DNS indicators | Both records map to Microsoft AS8075; Azure name servers are listed [14][13] | Confirmed passive observation | Does not corroborate the supplied Akamai claim |
| Akamai layer | No target-specific Akamai evidence was found; Akamai documentation only shows that its platform can modify downstream headers [16] | Unverified | Do not deploy an edge-only fix until path ownership is confirmed |
| Microsoft 365 | Official MUJ material covers Office 365 email setup and MFA | Confirmed institutional use, not SLCM IdP use | Test callback and iframe interactions only if the owner confirms Entra integration |
| Keen UI | User premise plus non-citable public-markup observation | Working hypothesis | UI age does not establish clickjacking; actual controls and actions matter |
| Authenticated functions | No first-party public inventory was found | Unknown | Do not claim profile, fee, grade, registration, or other impact without owner-approved evidence |

**Inference:** Microsoft-owned IP and DNS observations make Azure-hosted origin or front-end infrastructure plausible. They do not prove that Akamai is absent because split-horizon DNS, geographic routing, chained CDNs, or a separate property for authenticated routes could exist. The remediation plan therefore has two branches: origin enforcement is mandatory; edge enforcement is optional defense in depth after architecture confirmation.

The trust boundary also includes redirects. Every 200, 3xx, 4xx, and 5xx HTML response can have a separate framing policy. An IdP may refuse framing while the post-login application accepts it. Conversely, a silent-token callback may intentionally run inside an iframe: Microsoft documents that MSAL.js uses hidden iframes and loads the registered redirect URI after a 302 [5]. That general Microsoft behavior must not be assumed to describe MUJ, but it shows why the owner must identify callback-only pages before selecting `'none'` globally.

**Decision-ready insight:** manage framing by response class and trust boundary, not by homepage. The owner should produce an endpoint inventory before rollout and explicitly distinguish human-facing pages, callbacks, downloadable content, and intentionally embedded components.

## Why XFO Alone Leaves a Policy Gap

Clickjacking is an interface-based attack in which a user believes they are interacting with a decoy but actually activates content on a concealed framed page [6][9]. The critical prerequisite is renderability: if the sensitive page cannot load inside the hostile ancestor chain, opacity, positioning, dragging, and timing tricks have nothing to act on.

XFO remains useful. `DENY` blocks framing regardless of origin, while `SAMEORIGIN` allows embedding only when all ancestors share the protected page's origin in modern MDN guidance [4]. MUJ's `SAMEORIGIN` value is therefore a meaningful positive control. The limitation is policy expressiveness and deployment consistency. XFO cannot express a modern list of permitted partner origins, and obsolete `ALLOW-FROM` is ignored by modern browsers [4]. It must be delivered as an HTTP response header; a meta tag has no effect [4].

CSP `frame-ancestors` is the modern control. It identifies which parents may embed a page using frame, iframe, object, or embed [2]. It checks each ancestor and cancels loading if any ancestor is not allowed [2]. `'none'` is analogous to XFO DENY; `'self'` is broadly analogous to SAMEORIGIN; a source list can permit narrowly defined external parents [2]. Importantly, `frame-ancestors` does not inherit from `default-src`, so a policy that says only `default-src 'none'` can still leave framing open [2]. It also cannot be delivered through a meta element [2].

### Case study: MUJ versus SLCM

MUJ sends XFO SAMEORIGIN but no CSP [17]. SLCM sends neither [15]. The observation is not merely two scanner grades, D and F [17][15]. The mechanism is that current browsers receive an explicit framing decision from MUJ but no such decision from the captured SLCM response.

**Inference:** assuming no unobserved browser-side frame-buster blocks it, the SLCM landing page is frameable from an unrelated origin because MDN says embedding is allowed when neither XFO nor another restriction such as `frame-ancestors` is sent [4]. This inference is strong for visual rendering of that specific public response. It is not proof that an authenticated action can be completed, because authentication cookies, JavaScript navigation, confirmation steps, and per-route headers may differ.

### Case study: historical frame-buster failure

The Stanford "Busting Frame Busting" study describes clickjacking as session hijacking through frames and analyzes client-side frame-busting defenses [22]. RFC 7034 separately records that implementations historically differed over whether SAMEORIGIN was evaluated against the top page, immediate framer, or whole nested chain [8], and notes that some implementations did not check every ancestor [8]. These sources explain why a double-frame test belongs in regression work even though modern CSP behavior is clearer.

The implication is not that a current bypass definitely exists. **Inference:** the historical evidence raises a verification requirement, not a present exploit claim. The recommendation is to make the server-declared policy authoritative and use any JavaScript frame buster only as compatibility defense in depth.

**Decision-ready insight:** MUJ's XFO is good but incomplete governance; SLCM's missing pair is the immediate defect. The durable target state is a consistent CSP ancestor policy plus compatible XFO on all relevant responses.

## Clickjacking Surface and Abuse Cases

A security finding needs more than a frameable page. It needs a visible or hidden target, a realistic user gesture, a session state, and an effect. The public evidence establishes the first element only for SLCM's landing response, and even that remains an inference from absent headers until an authorized browser renders it. The following table separates testable scenarios from unsupported impact claims.

| Scenario | Required preconditions | Safe authorized proof | Current status | Risk interpretation |
|---|---|---|---|---|
| Basic overlay clickjacking | Target renders cross-origin; actionable control is alignable; user is authenticated if required | Show opaque framing first, then align a harmless owner-selected control without activating it | SLCM header gap confirmed; rendering and action not tested | Candidate exposure, impact unknown |
| Login UI redressing | Login page renders; victim can be deceived; credentials would enter the real or decoy page | Do not capture credentials; verify only whether login UI renders and whether browser/IdP blocks framing | Not tested | Avoid credential demonstrations |
| One-click state change | Authenticated cookie reaches frame; a single click changes data; no effective re-auth or confirmation | Use a marked test record and reversible action approved in writing | No public evidence of such an action | Do not claim account impact |
| Multi-step clickjacking | Multiple controls can be aligned in sequence and state persists between gestures | Stop at a harmless sequence using dummy data | Not tested | Higher complexity lowers likelihood but does not remove risk |
| Drag-and-drop UI redressing | A draggable source or drop target exists; drag gesture transfers data or triggers an action | Use inert text or a dummy record; prohibit file, PII, token, and cross-origin data extraction | No target-specific drag/drop control observed | Hypothesis only |
| Double-frame or nested-ancestor bypass | Outer and middle ancestors differ; policy or script examines the wrong ancestor | Two tester-owned origins, visible frames, no opacity, no action activation | Not tested | Regression check for historical implementation/script weaknesses |
| Same-site sibling framing | Tester has an approved sibling subdomain; browser treats sites as same-site but origins differ | Use only an owner-provided lab sibling; never seek a subdomain weakness | Not tested | Relevant because SameSite and same-origin are different boundaries |
| Callback or silent-iframe conflict | Identity integration intentionally loads a redirect page in an iframe | Owner identifies callback URI; verify policy on callback separately | Microsoft behavior is general, SLCM integration unconfirmed [5] | Availability risk if policy is too broad |

### Drag-and-drop analysis

Drag-and-drop clickjacking is not simply "click twice." The mechanism would require an actual drag source or drop target and a browser-permitted data/action path. The club should first inventory UI widgets by semantics: upload zones, sortable lists, selected-course baskets, document viewers, text selections, and confirmation targets. That inventory must come from an authorized account, not public guessing.

**Inference:** a legacy or template-heavy UI can increase alignment complexity and expose more interactive widgets, but theme age does not make those widgets frameable. Header policy, cookie delivery, browser behavior, and workflow confirmation still control exploitability. Therefore, record the Keen theme as maintenance context, not as a severity multiplier.

### Double-frame analysis

A nested test uses an outer tester page, a middle tester page on a different authorized origin, and the target as the leaf. Modern CSP should evaluate every ancestor [2]. Historical XFO implementations were less uniform [8]. A failure means the leaf visibly renders where policy says it should not; it does not require clicking anything.

**Decision-ready insight:** classify risk by demonstrated effect. "Frameable landing page" is a real configuration issue; "student data can be changed" remains unsupported until a safe, authorized test reproduces the complete chain.

## Authorized Test Plan With Safe Pass/Fail Criteria

NIST recommends documenting scope, authorized systems, personnel, logistics, data handling, and incident procedures before assessment work [18]. The owner, not the club, must choose the test account and harmless action. Store no real passwords in HTML, screenshots, repositories, issue trackers, or browser recordings.

| Phase | Authorized activity | Evidence to record | Pass condition | Fail condition | Stop condition |
|---|---|---|---|---|---|
| 0. Rules of engagement | Obtain signed scope for both hosts, paths, test origins, browsers, dates, accounts, and contacts | Approval, owner, window, source IP, emergency contact | Written authorization complete | Any ambiguity | No test begins |
| 1. Route inventory | With the owner, list HTML pages, redirects, errors, callbacks, downloads, and intentional embeds | URL, method, status, owner, sensitivity, embed requirement | Every in-scope response classified | Unknown or orphan route | Encountering out-of-scope path |
| 2. Header baseline | Inspect browser Network response headers without changing state | Status, final URL, redirect chain, XFO, CSP, cookies | Expected policy appears on every protected response | Missing, conflicting, duplicate, or malformed policy | Unexpected production behavior |
| 3. Opaque frame check | Load each approved URL in a plainly visible local frame on a tester-controlled unrelated origin | Screenshot, console message, browser/version, network trace | Browser blocks protected page | Page visibly renders | Any sensitive data appears |
| 4. Classic alignment check | In a private local harness, align only a harmless owner-selected control; keep frame visibly outlined | Coordinates, zoom, viewport, result | Protected page never renders or harmless action cannot be confused | A realistic gesture reaches the target control | Before irreversible action |
| 5. Cookie matrix | Repeat only with approved test account across cross-site and approved same-site lab origins | Cookie name, Domain, Path, Secure, HttpOnly, SameSite; whether sent | Sensitive page remains blocked independent of cookies | Authenticated page renders where policy forbids | Any real-user cookie observed |
| 6. Frame-buster check | Compare JavaScript enabled/disabled and record navigation/console behavior | Top URL, frame URL, console, DOM outcome | Server policy blocks before script matters | Protection depends only on client script | Script causes loop or instability |
| 7. Double-frame matrix | Use two tester-owned origins; vary outer/middle origin and visible nesting | Ancestor chain, policy, browser/version, rendered result | Any disallowed ancestor cancels load | Leaf renders despite disallowed ancestor | Any attempt to source an unapproved origin |
| 8. Drag-and-drop check | Only if owner identifies a real widget; use dummy text or a marked test record | Gesture, source, destination, before/after state | Framing blocked or no unintended transfer/action | Dummy data/action crosses the intended UI boundary | File, PII, token, payment, or real record involved |
| 9. Confirmation and re-auth | Check whether sensitive actions require clear confirmation or fresh authentication | UI prompt, server response, audit event | High-impact action needs deliberate confirmation/re-auth | Single disguised gesture suffices | Do not submit a real action |
| 10. Regression | Re-run after origin and edge changes across supported browsers and all route classes | Automated header results plus manual browser evidence | Stable policy and no legitimate embed breakage | Any protected route regresses | Production errors exceed agreed threshold |

### Exact test logic without an exploit payload

For the basic frame check, the tester creates a private local page containing a normal, fully opaque frame whose URL is the approved target. The frame must be visibly labeled and outlined. This confirms rendering without deception. If the browser blocks it and reports XFO or CSP in the console, collect that evidence and stop for that route. OWASP's testing objective is to determine whether a page can be loaded in a frame and whether defenses are present [9].

For frame busting, repeat with JavaScript disabled. A secure server policy should still block framing because XFO and CSP are response controls. If protection disappears only when JavaScript is disabled, record "client-side-only defense" and do not attempt bypass tricks. RFC 7034 says XFO is delivered as an HTTP header and meta delivery is ignored [8].

For drag-and-drop, first establish that an approved widget exists. Keep the target frame visible, use synthetic data, and avoid extraction. The pass/fail question is whether a user gesture can cross the visual boundary or trigger the dummy action while the user is shown a materially different instruction. There is no need to weaponize the result.

For double framing, use an outer page on test origin A and a middle page on test origin B. The target is the leaf. Run the matrix with no opacity and no target interaction. CSP should reject any chain containing an ancestor outside the allowlist [2]. A current-browser render despite a disallowed ancestor is sufficient evidence for escalation.

### Severity rubric

| Demonstrated result | Suggested severity | Rationale |
|---|---|---|
| Missing header but page does not render because another effective control blocks it | Informational to Low | Configuration gap with compensating control |
| Public or low-impact page renders; no authenticated action | Low | Visual framing confirmed, consequential effect absent |
| Authenticated page renders but no meaningful action can be induced | Low to Medium | Session exposure exists, exploit chain incomplete |
| Harmless test proves one-click reversible state change | Medium, context dependent | Complete UI-redress chain demonstrated |
| Owner-approved test proves sensitive data transfer, security-setting change, payment, registration, or equivalent high-impact action | Escalate for formal risk scoring | Impact depends on exact action, privileges, re-auth, and recovery |

**Decision-ready insight:** the test program seeks the minimum evidence needed at each stage. Stop once policy failure is proven; do not keep interacting merely to make the demonstration dramatic.

## Remediation Architecture and Regression Controls

The preferred default is `Content-Security-Policy: frame-ancestors 'none'` when no legitimate embedding exists. If same-origin framing is required, use `'self'`. If an approved external parent is required, list only exact HTTPS origins and verify the complete ancestor chain. Keep `X-Frame-Options: DENY` or `SAMEORIGIN` aligned with the CSP for older clients. Do not use `ALLOW-FROM`, which modern browsers ignore [4].

| Layer | Recommended control | Deployment note | Failure mode to prevent | Verification |
|---|---|---|---|---|
| ASP.NET MVC application | Apply a global response filter or middleware-equivalent for all HTML responses | Exclude only documented callback/embed endpoints | Controller or error route omits policy | Integration tests by route class |
| IIS | Use `system.webServer/httpProtocol/customHeaders` for a site-wide baseline | IIS custom headers are returned with server responses; `add`, `remove`, and `clear` manage the collection [3] | Duplicate or inherited conflicting values | Inspect effective config and raw response |
| CDN/edge, if confirmed | Add or normalize downstream CSP/XFO after cache retrieval | Akamai can add, remove, modify, or pass downstream headers [16] | Edge and origin disagree; duplicate header semantics | Compare direct-origin and edge-approved test paths |
| Identity callbacks | Give callback-only pages a separately reviewed policy | MSAL may load a registered redirect URI in a hidden iframe [5] | Global `'none'` breaks silent token renewal | Owner-approved SSO regression suite |
| Cookies | Explicitly set Secure, HttpOnly, and justified SameSite values | Lax excludes iframe navigations from its cross-site exceptions [21] | Cookie setting becomes the only anti-clickjacking control | Browser cookie matrix |
| Sensitive actions | Require anti-CSRF validation, explicit confirmation, and re-auth where impact warrants | MUJ's public anti-forgery cookie indicates ASP.NET anti-forgery machinery but not route-wide enforcement [17] | One disguised gesture completes a high-impact action | Server-side negative tests and audit logs |
| Monitoring | Log CSP violations during staged rollout and monitor header drift | Report-only is useful for discovery but does not enforce framing | Team mistakes telemetry for protection | Enforced header check after observation period |
| CI/CD | Assert CSP/XFO on representative 200, 3xx, 4xx, and 5xx responses | Test values, not only header names | Legacy route or deployment slot regresses | Release gate plus scheduled external check |

### Case study: origin versus edge ownership

The public records show Microsoft AS8075 addresses and Azure DNS for both hosts [14][13]. The user supplied "behind Akamai," but no target-specific public evidence in this research confirmed that path. Akamai's own documentation shows that its Property Manager can alter headers after retrieving an origin or cached response and immediately before sending it to the client [16].

**Inference:** if Akamai is actually present on another route or geography, an edge rule could efficiently normalize legacy applications. The trade-off is hidden coupling: an edge-only fix can disappear on an origin-bypass path, while an origin-only fix can be removed or duplicated at the edge. The recommendation is origin enforcement as the source of truth and edge normalization only after the owner confirms architecture.

### Rollout sequence

| Stage | Change | Exit criterion |
|---|---|---|
| 1 | Inventory legitimate framing and identity callbacks | Every exception has an owner and business reason |
| 2 | Add CSP Report-Only for broader CSP discovery, but separately test an enforced `frame-ancestors` candidate in staging | No required embed is unexplained |
| 3 | Enforce `frame-ancestors` and aligned XFO at origin | All protected staging routes block hostile framing |
| 4 | Normalize at edge if an edge exists | Edge and origin return one consistent effective policy |
| 5 | Deploy by route group with rollback | No SSO, parent portal, download, or accessibility regression |
| 6 | Add CI and scheduled production checks | Drift causes an actionable alert |

**Decision-ready insight:** do not postpone SLCM's missing control while redesigning a full CSP. `frame-ancestors` is independent of `default-src` [2], so the team can deploy a narrow framing policy first, then mature the rest of CSP separately.

## Synthesis

| Dimension | XFO only | CSP `frame-ancestors` | JavaScript frame buster | SameSite cookies | Confirmation or re-auth |
|---|---|---|---|---|---|
| Mechanism | Browser response policy with DENY/SAMEORIGIN | Browser response policy evaluating every ancestor | Client script tries to escape or hide a frame | Controls cookie delivery by site context | Adds an application-level user-intent check |
| Scope | Framing decision, limited allowlist flexibility | Framing decision with explicit source list | Depends on script execution and browser behavior | Session attachment, not rendering itself | Selected actions only |
| Strongest use | Legacy compatibility | Primary modern framing control | Last-resort compatibility layer | Defense in depth against some authenticated cross-site frames | Limit impact when UI deception reaches an action |
| Main trade-off | Historical implementation variation; obsolete ALLOW-FROM | Can break legitimate embeds or silent callbacks if scoped poorly | Historically bypass-prone and disabled with JavaScript | Same-site and `None` cases remain; cookie inventory may vary | Adds friction and may not cover every action |
| MUJ status | SAMEORIGIN confirmed [17] | Missing in captured response [17] | Unknown | Public anti-forgery cookie lacks shown SameSite [17] | Unknown |
| SLCM status | Missing [15] | Missing [15] | Unknown | Public session cookie is Lax [15] | A public confirmation dialog exists, purpose unknown [11] |
| Recommended decision | Retain, align with CSP | Deploy as primary control | Do not rely on it | Configure explicitly, but never substitute for framing policy | Apply proportionately to high-impact actions |

Three non-obvious tensions matter.

First, MUJ's better header does not automatically mean lower end-to-end identity risk. A protected login page can redirect to an unprotected application route, or a broad `'none'` policy can break a callback intentionally loaded in an iframe. Microsoft's general MSAL documentation demonstrates that hidden iframe token renewal and redirect URI loading are real architectural patterns [5]. **Inference:** owner confirmation of the identity flow is necessary before global enforcement, but uncertainty is not a reason to leave ordinary application pages unprotected.

Second, SLCM's `SameSite=Lax` session cookie may block that particular cookie in a cross-site iframe because Lax exceptions require top-level safe navigation, excluding iframe navigation [21]. That could reduce the most obvious authenticated clickjacking path. Yet it does not fix visual framing, does not describe every cookie, and does not address approved same-site sibling origins. The mechanism differs: cookies determine session context; XFO/CSP determine whether the UI renders. They are complementary, not interchangeable.

Third, the older RFC and modern MDN guidance differ in emphasis. RFC 7034 preserves historical implementation caveats about nested ancestors [8]; modern `frame-ancestors` explicitly checks each ancestor [2]. This divergence justifies a double-frame regression test without supporting a claim that current browsers are bypassable.

The combined conclusion is a defense-in-depth architecture: CSP `frame-ancestors` as the primary browser policy, aligned XFO for compatibility, explicit cookies, application-level confirmation for important actions, and CI coverage for all response classes. The exposure finding should be written narrowly: confirmed missing framing headers on SLCM's captured landing response, partial protection on MUJ, and unverified authenticated impact.

## VERDICT

**Verdict: Confirmed configuration weakness with unproven authenticated impact.**

`slcm.manipal.edu` has the stronger finding: its public response captured on **25 August 2026** received a SecurityHeaders grade F and showed neither XFO nor CSP [15]. Under standard browser behavior, absence of both controls permits embedding unless another mechanism intervenes [4]. This supports reporting a clickjacking exposure on the captured public route, but not a claim that student records, fees, grades, registration, or credentials can be affected.

`mujslcm.jaipur.manipal.edu` is partially protected: `X-Frame-Options: SAMEORIGIN` was present [17], while CSP was absent [17]. The exact framework premise is confirmed by the exposed IIS, MVC, and ASP.NET version headers [17]. The supplied Akamai and Microsoft-365-as-SLCM-IdP premises are not independently established. Passive records point to Microsoft AS8075 and Azure DNS [14], and official MUJ material confirms Office 365 use but not the SLCM authentication path.

**Confidence: High (0.90) for the landing-page header divergence; High (0.90) for the disclosed MUJ/IIS/ASP.NET stack values; Medium (0.70) for the inference that SLCM's public landing page is frameable; Low (0.30) for any authenticated action impact; Low (0.25) for Akamai being in the currently observed path; Medium-Low (0.45) for Microsoft Entra being the SLCM IdP.** These are analytical confidence labels, not calculated probabilities.

**Priority order:** (1) add enforced `frame-ancestors` and aligned XFO to SLCM, (2) add `frame-ancestors` to MUJ while retaining SAMEORIGIN, (3) verify every response class and redirect, (4) confirm identity and edge architecture with owners, (5) run the authorized visible-frame, cookie, frame-buster, double-frame, and conditional drag-and-drop tests, and (6) add deployment regression gates.

No unauthorized interaction is recommended or implied. If written authorization is unavailable, the club should stop at this public evidence report and disclose the issue through the university's approved security contact.

## References

1. *Content Security Policy Level 3*. https://www.w3.org/TR/CSP3/
2. *Content-Security-Policy: frame-ancestors directive - HTTP | MDN*. https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-ancestors
3. *Custom Headers &lt;customHeaders&gt; | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/configuration/system.webserver/httpprotocol/customheaders/
4. *X-Frame-Options header - HTTP | MDN*. https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Frame-Options
5. *Avoid page reloads (MSAL.js) - Microsoft identity platform | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity-platform/msal-js-avoid-page-reloads
6. *What is Clickjacking? Tutorial & Examples | Web Security Academy*. https://portswigger.net/web-security/clickjacking
7. *Single sign-on (MSAL.js) - Microsoft identity platform | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity-platform/msal-js-sso
8. *RFC 7034: HTTP Header Field X-Frame-Options | RFC Editor*. https://www.rfc-editor.org/rfc/rfc7034
9. *WSTG - Latest | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/11-Client-side_Testing/09-Testing_for_Clickjacking
10. *Clickjacking Defense - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Clickjacking_Defense_Cheat_Sheet.html
11. [
	MU SLcM
](https://slcm.manipal.edu/)
12. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
13. *slcm.manipal.edu - urlscan.io*. https://urlscan.io/domain/slcm.manipal.edu
14. *mujslcm.jaipur.manipal.edu - urlscan.io*. https://urlscan.io/domain/mujslcm.jaipur.manipal.edu
15. *Scan results for https://slcm.manipal.edu/*. https://securityheaders.com/?q=https%3A%2F%2Fslcm.manipal.edu%2F&followRedirects=on
16. *Modify Outgoing Response Header*. https://techdocs.akamai.com/property-mgr/docs/modify-outgoing-response-header
17. *Scan results for https://mujslcm.jaipur.manipal.edu/*. https://securityheaders.com/?q=https%3A%2F%2Fmujslcm.jaipur.manipal.edu%2F&followRedirects=on
18. *Technical guide to information security testing and assessment*. https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf
19. *SameSite cookies explained  |  Articles  |  web.dev*. https://web.dev/articles/samesite-cookies-explained
20. *SameSite | OWASP Foundation*. https://owasp.org/www-community/SameSite
21. *Set-Cookie header - HTTP | MDN*. https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie
22. *crypto.stanford.edu*. https://crypto.stanford.edu/~dabo/pubs/papers/framebust.pdf
23. *Standard Operating Procedure - Manipal University Jaipur*. https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf
