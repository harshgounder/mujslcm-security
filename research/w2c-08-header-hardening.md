# MUJ SLCM Security Headers: Closing Six Browser-Side Gaps

## Executive Summary

- **Observed Baseline**: A passive Shodan observation for `mujslcm.jaipur.manipal.edu`, dated **2026-08-22**, recorded `Microsoft-IIS/10.0`, `X-AspNetMvc-Version: 5.3`, `X-AspNet-Version: 4.0.30319`, and `X-Frame-Options: SAMEORIGIN`. Its displayed response-header block did not contain CSP, HSTS, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`, or COOP [27]. This supports the requested baseline for that one public response, but it does not prove that every route, error, redirect, authentication callback, or CDN response has the same headers.

- **CSP Is The Highest-Value Browser Control**: CSP controls which resources a document may load and is a defense-in-depth layer against exploitation of content injection; OWASP explicitly warns that it is not a substitute for preventing XSS [17][16]. Its absence also leaves MUJ without CSP `frame-ancestors`, the modern framing control, on pages where XFO is missing. Start with `Content-Security-Policy-Report-Only`, inventory real dependencies, and progress to a nonce-based enforced policy rather than deploying a permissive policy containing `unsafe-inline`.

- **HSTS Closes A Transport State Gap**: HTTPS alone does not tell a browser to rewrite future HTTP attempts before sending them. HSTS does, but only after the browser receives it over HTTPS; the initial HTTP visit remains exposed unless preloading or a previously learned parent-domain policy applies [22]. Stage a short `max-age`, confirm all covered hosts support HTTPS, and only then consider `includeSubDomains` or preload.

- **`nosniff` Is A Low-Risk, High-Confidence Fix**: `X-Content-Type-Options: nosniff` directs browsers to respect declared media types. For script and style destinations, a mismatched JavaScript or CSS MIME type is blocked [8]. Add it after correcting any inaccurate `Content-Type` responses; otherwise it can expose existing server misconfiguration by blocking resources that previously worked through browser tolerance.

- **Framing Protection Is Present But Not Proven Complete**: `SAMEORIGIN` permits embedding only when all ancestor frames have the same origin as the protected page [6]. It materially reduces cross-origin clickjacking for the observed login response, but an interactive route that omits both XFO and CSP `frame-ancestors` remains potentially frameable. CSP must explicitly include `frame-ancestors` because that directive does not inherit from `default-src`; omitting it allows framing [12].

- **Not Every Missing Header Has Equal Urgency**: The absence of an explicit `Referrer-Policy` does not normally mean full cross-origin URL leakage in current browsers. The default is `strict-origin-when-cross-origin`, which sends the full path and query on same-origin requests, only the origin on same-security cross-origin requests, and no referrer on an HTTPS-to-HTTP downgrade [21]. An explicit header remains valuable for consistency and deliberate privacy posture, but its risk is lower than CSP, HSTS, or `nosniff`.

- **Permissions Policy And COOP Need Compatibility-Led Deployment**: Permissions Policy restricts features such as camera, microphone, or geolocation, while each unlisted feature otherwise uses its own default allowlist of `*`, `self`, or `none` [15]. COOP defaults to `unsafe-none`, permitting browsing-context-group sharing; stricter values can sever opener relationships [13]. Because the brief identifies Microsoft 365 identity, popup and redirect behavior must be tested before enforcing COOP. Microsoft states that MSAL Browser v5 includes COOP support, but the public evidence does not establish that MUJ uses MSAL Browser v5 [25].

- **Akamai Must Have An Explicit Ownership Model**: Akamai Property Manager can add, remove, modify, find-and-replace, or pass downstream response headers [4]. However, neither passive MUJ capture displayed an Akamai identifier [26][27]. Therefore, Akamai is treated in this report as a **brief-supplied architecture assertion**, not an independently verified path for the sampled responses. If Akamai is in the production path, choose whether the application, IIS, or Akamai owns each header and validate both cache hits and origin fetches.

**Decision-ready insight:** Remediate in this order: **(1) CSP in Report-Only followed by enforcement, (2) HSTS after domain-wide HTTPS validation, (3) `nosniff`, (4) complete framing coverage, (5) explicit Referrer-Policy, (6) Permissions-Policy, and (7) COOP after identity-flow testing**. Implement low-risk static headers centrally, but retain application ownership of nonce-bearing CSP.

## Scope, Evidence, And Analytical Method

### Public-information boundary

This report uses passive public artifacts and vendor documentation only. It does not log in, submit credentials, enumerate authenticated routes, probe for vulnerabilities, bypass controls, or direct anyone to do so. Any future validation against the live service should be performed only by MUJ personnel or researchers holding explicit written authorization.

The public page body confirms that both `mujslcm.jaipur.manipal.edu` and the alternate `muj.slcm.jaipur.manipal.edu` expose a page labelled **"WELCOME TO MUJ PORTAL"** with a sign-in interface [10][1]. A public markup extraction also shows the `@muj.manipal.edu` login label [1]. Those observations establish portal identity, not its entire authentication protocol.

### Exact evidence tiers

| Tier | Evidence | What it establishes | What it does not establish |
|---|---|---|---|
| Direct public body | MUJ portal page | Portal identity and publicly displayed sign-in interface [10][1] | Response headers, authenticated behavior, or backend ownership |
| Passive service observation | Shodan record for `98.70.14.50` | Exact-host snapshot on 2026-08-22: IIS 10, MVC 5.3, ASP.NET 4.0.30319, XFO SAMEORIGIN, and displayed response-header block [27] | Uniformity across every route, user state, edge location, or time |
| Corroborating passive observation | Shodan record for `20.244.94.89` | Alternate-host snapshot on 2026-08-18 with the same principal stack identifiers and XFO value [26] | That the two hostnames share every configuration rule |
| Public infrastructure artifact | urlscan domain page | The registered domain and a Microsoft ASN association in that artifact [11] | A captured MUJ response-header set or an Akamai delivery path |
| Vendor and standards guidance | MDN, OWASP, Microsoft, Akamai | Browser semantics and supported implementation controls | MUJ's private configuration or business requirements |
| Brief-supplied assertion | "behind Akamai" and "Microsoft 365 identity" | Defines compatibility scenarios that the requested audit must cover | Independent proof that the sampled response traversed Akamai or used a particular Microsoft authentication library |

### Reproducible reasoning summary

The audit rationale is evidence-to-conclusion rather than private scratchpad chain-of-thought:

1. The exact-host passive observation lists XFO but not the six focus headers [27]. Therefore, those six are classified as **not observed in that response**, not as globally absent from the whole application.
2. Each missing control is mapped to documented browser behavior. The report distinguishes "creates a vulnerability" from the more accurate "removes a mitigation or policy boundary."
3. Controls are prioritized by exploit preconditions, blast radius, and deployment risk. CSP and HSTS address broader classes of browser behavior, while Referrer-Policy has a comparatively safe modern default.
4. Implementation ownership is separated across MVC, IIS, and the possible Akamai edge. Dynamic CSP nonces belong near view rendering; static headers can be centralized.
5. Recommendations remain conditional where MUJ-specific requirements are unknown. This is especially important for parent/student framing, legacy inline JavaScript, Microsoft identity popups, subdomains, and edge-generated responses.

**Case study - the two-hostname snapshot:** The exact `mujslcm` record and alternate `muj.slcm` record both report the same IIS, MVC, ASP.NET, and XFO values [26][27]. This consistency raises confidence in the technology baseline. It does not justify assuming route-wide header consistency because both observations concern a public `200 OK` HTML response. The correct operational outcome is to treat the finding as a strong baseline and then ask authorized owners to test a representative response matrix.

## Exact Header Audit: One Present, Six Not Observed

| Header | Snapshot status | Exact recommended starting value | Security function | What the gap permits or fails to prevent | Priority | Important qualification |
|---|---|---|---|---|---|---|
| `X-Frame-Options` | **Present: `SAMEORIGIN`** [27] | Keep `SAMEORIGIN` during migration; consider `DENY` only if no legitimate same-origin framing exists | Restricts framing by ancestor origins [6] | On a response that omits XFO and CSP `frame-ancestors`, a hostile site may attempt UI redressing or clickjacking | High coverage check | XFO in a `<meta>` tag has no effect [6]. It is useful mainly for renderable, interactive content, not non-rendered API data [18] |
| `Content-Security-Policy` | **Not observed** [27] | Report-Only first; eventual strict policy using per-response nonces, `object-src 'none'`, `base-uri 'self'`, and explicit `frame-ancestors` | Restricts resource loading and provides defense in depth against XSS exploitation [17] | No CSP source allowlist, no CSP framing policy, and no CSP-driven insecure-request upgrading | **Critical** | CSP does not repair an injection flaw. `unsafe-inline` defeats much of its purpose [17][16] |
| `Strict-Transport-Security` | **Not observed** [27] | Begin with `max-age=86400`; increase only after validation; add subdomain or preload directives deliberately | Teaches browsers to use HTTPS for future requests and reject bypass of certificate errors [22] | Initial or unlearned HTTP navigation remains exposed to downgrade or redirect interception | **High** | HSTS is ignored over HTTP and has a first-visit gap [22] |
| `X-Content-Type-Options` | **Not observed** [27] | `nosniff` | Requires declared MIME types to be respected; blocks script/style responses with mismatched types [8] | Removes an explicit defense against MIME sniffing and type confusion | **High, low rollout cost** | Correct `Content-Type` values first to avoid blocking legitimate resources |
| `Referrer-Policy` | **Not observed** [27] | `strict-origin-when-cross-origin`, or `no-referrer` if business requirements permit | Controls how much `Referer` information accompanies requests [21] | Leaves behavior to browser defaults and may retain full path/query on same-origin requests | Medium | The modern default is already `strict-origin-when-cross-origin`; absence is not equivalent to `unsafe-url` [21] |
| `Permissions-Policy` | **Not observed** [27] | Begin with unused features disabled, for example `camera=(), microphone=(), geolocation=()` | Allows or denies browser capabilities in the document and child frames [15] | Leaves each feature at its specification-defined default allowlist rather than MUJ's least-privilege policy [15] | Medium | The technology remains partly experimental; test browser compatibility [15] |
| `Cross-Origin-Opener-Policy` | **Not observed** [27] | Evaluate `same-origin-allow-popups` for popup-dependent identity; use `same-origin` if no cross-origin opener relationship is needed | Controls browsing-context-group separation and opener relationships [13] | Leaves the default `unsafe-none`, so cross-origin documents may retain a shared opener relationship where platform rules allow | Medium | A strict value may break authentication or payment popups; this requires authorized workflow testing |

The table deliberately says **not observed**, not "universally missing." The Shodan evidence is a recent and valuable passive snapshot, but headers can vary by route, status code, hostname, cache state, authentication state, and edge rule.

## What Each Gap Actually Enables

### 1. Missing CSP: no application-defined browser content boundary

CSP is the broadest missing defense. A site can use it to restrict scripts, styles, images, fonts, frames, connections, form destinations, base URLs, and embedding parents. MDN states that controlling JavaScript resources is CSP's primary use case [17]. A nonce must be unpredictable and different for every response, and the server must place the same nonce in the policy and approved script or style elements [17].

**What absence enables:** If an independent injection flaw exists, the browser has no MUJ-defined CSP source policy to block many injected resource loads or unapproved inline scripts. Absence does **not** create XSS by itself, and a weak CSP containing broad hosts or `unsafe-inline` may provide little protection. OWASP recommends a strict CSP as a second layer while continuing normal XSS prevention [16].

CSP also matters to the requested clickjacking and mixed-content analysis. `frame-ancestors` checks every ancestor and cancels the load if one fails to match; critically, it does not fall back to `default-src` [12]. Thus, even `default-src 'none'` does not stop framing unless `frame-ancestors` is present [12]. `upgrade-insecure-requests` tells user agents to treat insecure resource URLs as HTTPS URLs [7].

**Mixed-content qualification:** Missing CSP does not mean every HTTP subresource will load. Modern browsers independently upgrade some mixed-content categories and block others. The defensible finding is that MUJ lacks a centrally declared CSP mechanism to upgrade insecure URLs and constrain all resource origins. The root fix remains eliminating HTTP dependencies rather than relying only on automatic upgrading.

### 2. Missing HSTS: HTTPS is reactive rather than precommitted

HSTS changes future request construction. After a valid HTTPS response sets the policy, the browser rewrites matching HTTP URLs to HTTPS before network transmission and prevents users from bypassing certificate errors [22]. A normal HTTP-to-HTTPS redirect occurs only after an HTTP request reaches a server or edge, so it cannot provide the same pre-request guarantee.

**What absence enables:** A first-time user, fresh browser profile, or user without a parent-domain HSTS policy may initiate an HTTP request that an on-path party could manipulate. HSTS itself has the same first-contact limitation until learned; preload can mitigate that gap [22]. Preload and `includeSubDomains` are not safe first moves for an institution with many subdomains because they can make HTTP-only systems unreachable. OWASP warns that preload can have lasting consequences and recommends short initial `max-age` values during rollout [5].

### 3. Missing `nosniff`: browser interpretation can diverge from server intent

`X-Content-Type-Options: nosniff` states that the server's declared MIME type is authoritative [8]. Browsers block a script or stylesheet whose declared type is incompatible with JavaScript or CSS [8]. For other resources, sniffing is disabled and the supplied type is used as-is [8].

**What absence enables:** Depending on browser behavior and response content, a resource may be interpreted differently from its declared type. This can magnify upload, static-file, or error-response mistakes. It does not create malicious content, and it does not compensate for unsafe upload handling. The practical sequence is to inventory MIME types, correct errors, then enforce `nosniff` everywhere.

### 4. Missing explicit Referrer-Policy: inconsistent privacy rather than total failure

The header controls the amount of `Referer` data sent on navigation and subresource requests [21]. With no valid policy, current browsers use `strict-origin-when-cross-origin`: full origin, path, and query for same-origin requests; origin only for HTTPS-to-HTTPS cross-origin requests; no referrer for HTTPS-to-HTTP requests [21].

**What absence enables:** It delegates policy to browser defaults and does not hide potentially sensitive paths or query strings from same-origin destinations, including logs and same-origin analytics. It does not normally disclose the full path to ordinary cross-origin HTTPS destinations under the current default. An explicit policy makes intended behavior auditable and stable.

### 5. Missing Permissions-Policy: no MUJ-specific browser feature budget

Permissions Policy can deny capabilities in the top document and embedded frames [15]. The header uses `<directive>=<allowlist>` syntax, and violations may be reported using the Reporting API [15]. Each directive has a default allowlist of `*`, `self`, or `none` [15].

**What absence enables:** Features remain governed by their individual defaults rather than an institutional least-privilege policy. It is incorrect to say absence automatically grants every origin camera, microphone, or geolocation access: permissions prompts, secure-context requirements, origin rules, and each feature's default still apply. The gain is reduction of unnecessary capability, particularly in compromised or embedded content.

### 6. Missing COOP: default opener and process relationship

COOP controls whether documents share a browsing context group. Its default `unsafe-none` permits sharing and opts out of COOP process isolation [13]. `same-origin` shares a group only when both documents are same-origin and use compatible policy, while stricter isolation can sever script connections between opener and opened document [13].

**What absence enables:** It leaves opener relationships at the default rather than actively isolating the portal from cross-origin windows. This can matter to cross-window attacks and advanced isolation requirements, but COOP is not a general XSS, CORS, or framing control.

**Microsoft identity inference:** If MUJ opens Microsoft authentication in a popup and depends on an opener relationship, strict `same-origin` could interrupt the return path. The brief says Microsoft 365 identity, while Microsoft states that MSAL Browser v5 includes COOP support [25]. Public evidence does not establish MUJ's exact library or flow, so `same-origin-allow-popups` is a test candidate, not a blind production prescription.

## IIS 10 And MVC 5 Deployment Blueprint

### Split static and dynamic ownership

Microsoft documents IIS custom response headers under `system.webServer/httpProtocol/customHeaders`; the collection supports `add`, `remove`, and `clear` [24]. This is appropriate for static values such as `nosniff`, an explicit referrer policy, a tested Permissions-Policy, and a tested COOP value.

A defensive starting pattern is shown below. It is an illustrative template and must be adapted to actual MUJ requirements:

```xml
<configuration>
  <system.webServer>
    <httpProtocol>
      <customHeaders>
        <remove name="X-Content-Type-Options" />
        <add name="X-Content-Type-Options" value="nosniff" />

        <remove name="Referrer-Policy" />
        <add name="Referrer-Policy" value="strict-origin-when-cross-origin" />

        <remove name="Permissions-Policy" />
        <add name="Permissions-Policy"
             value="camera=(), microphone=(), geolocation=(), payment=(), usb=()" />

        <!-- Select only after Microsoft identity and popup testing. -->
        <remove name="Cross-Origin-Opener-Policy" />
        <add name="Cross-Origin-Opener-Policy" value="same-origin-allow-popups" />

        <!-- Preserve existing framing behavior during CSP migration. -->
        <remove name="X-Frame-Options" />
        <add name="X-Frame-Options" value="SAMEORIGIN" />
      </customHeaders>
    </httpProtocol>
  </system.webServer>
</configuration>
```

The explicit `remove` before `add` is intended to avoid duplicate local collection entries; Microsoft documents both operations [24]. Administrators must also check parent-level IIS configuration and any edge rule because this snippet alone cannot prevent another layer from adding a second field.

### CSP belongs near MVC rendering

A strict nonce-based CSP cannot be a single static Web.config string. MDN states that the nonce must be unpredictable and different for every response [17]. MVC should generate the nonce once per HTML response, place it in the CSP header, and apply it only to trusted script and style elements. Do not use middleware that blindly adds a nonce to every script element after rendering; OWASP warns that such behavior can also bless attacker-injected elements [16].

A safe rollout candidate is:

```http
Content-Security-Policy-Report-Only:
  default-src 'self';
  base-uri 'self';
  object-src 'none';
  frame-ancestors 'self';
  form-action 'self';
  script-src 'self' 'nonce-{PER_RESPONSE_RANDOM_VALUE}';
  style-src 'self' 'nonce-{PER_RESPONSE_RANDOM_VALUE}';
  img-src 'self' data:;
  font-src 'self';
  connect-src 'self';
  upgrade-insecure-requests;
  report-to csp-endpoint
```

This is not deploy-as-is production policy. Authorized maintainers must inventory the portal's actual Microsoft identity, analytics, CDN, image, font, API, and report endpoints. Report-Only does not block content but can generate console and endpoint violation reports, making it suitable before enforcement [16]. A temporary looser enforced policy can coexist with a stricter report-only policy during migration [16].

### HSTS implementation choices

IIS has a native `<hsts>` site element only in **IIS 10.0 version 1709 and later** [23]. It supports `enabled`, `max-age`, `includeSubDomains`, `preload`, and `redirectHttpToHttps` [23]. Therefore, "IIS 10" alone is insufficient to assume native support; confirm the Windows/IIS servicing version.

Use a staged plan:

| Stage | Value or action | Exit condition |
|---|---|---|
| 0 | Inventory HTTP dependencies, aliases, callback hosts, and subdomains | No required target depends on cleartext HTTP |
| 1 | `Strict-Transport-Security: max-age=86400` on HTTPS responses | No availability or certificate failures during monitored window |
| 2 | Increase to several weeks or months | Stable operation across browsers, campuses, and identity callbacks |
| 3 | Increase toward one year | Operations accepts rollback delay |
| 4 | Add `includeSubDomains` only after subdomain inventory | Every covered subdomain supports valid HTTPS |
| 5 | Consider preload as a separate governance decision | Long-term commitment approved; submission requirements verified |

The native IIS redirect option replaces the scheme with HTTPS and expects TLS on port 443 [23]. HSTS itself must appear only on HTTPS responses because browsers ignore it over HTTP [22]. If Akamai terminates TLS, edge ownership may provide broader coverage, but the origin should still be configured consistently for any authorized direct-origin or alternate path.

## Akamai Edge Interactions

### What Akamai can do

Akamai's **Modify Outgoing Response Header** behavior processes headers traveling downstream to the client. It can add, remove, modify, find-and-replace, or pass response headers; custom names and variable expressions are supported [4]. This makes the edge a viable enforcement point for static headers and a viable source of accidental override or duplication.

Akamai also documents an **HTTP to HTTPS Upgrade** behavior, but its stated purpose is to convert traffic **between the Akamai edge and the origin** to HTTPS [9]. Akamai separately says that end-to-end HTTPS may require a redirect from the original HTTP URL [9]. Therefore, this behavior is not a substitute for client-facing HTTPS redirects or HSTS.

### Evidence tension: claimed Akamai path versus observed Microsoft endpoint

The passive exact-host record associates `mujslcm.jaipur.manipal.edu` with `98.70.14.50` and Microsoft infrastructure, and its captured header block contains no explicit Akamai identifier [27]. The alternate hostname record behaves similarly [26]. This does not prove that Akamai is absent: the capture could reflect a direct origin, a DNS state at that time, an unbranded edge response, or a split path. Those are **inferences**, not observations.

The operational implication is important. Before changing Akamai, the team should verify from authoritative MUJ DNS, Property Manager, and application ownership records whether the exact hostname and every alias traverse that property. A header rule applied to the wrong property gives a false sense of remediation.

### Cache and precedence failure modes

Akamai states that GET content is cacheable by default, that `Vary` can affect cacheability, and that a fresh cached object is served without a new origin retrieval [19]. When stale, the edge may revalidate with the origin and either retrieve a newer object or reset the cached object's TTL [19].

| Failure mode | Mechanism | Consequence | Defensive decision |
|---|---|---|---|
| Origin adds, edge removes | Downstream edge rule deletes the field [4] | Origin appears fixed internally while clients remain unprotected | Treat client-visible edge response as the acceptance criterion |
| Origin and edge both add | No single owner | Duplicate or conflicting policy fields | Assign one owner and use remove-then-add semantics at the chosen final layer |
| Cache hit differs from miss | Fresh object can be served without origin retrieval [19] | Validation of only one cache state may miss drift | Compare authorized hit, miss, and revalidated responses |
| Redirect omits policy | Redirect generated at a different rule or layer | HSTS or framing coverage can vary by status | Include `3xx` responses in the matrix; remember HSTS is accepted only over HTTPS |
| Edge error or challenge differs | **Inference:** edge-generated content may not traverse application header logic | Branded interactive error page may lack controls | Apply edge-level baseline where supported and validate representative edge responses |
| Dynamic CSP set at edge | Static edge policy cannot create and synchronize an MVC view nonce by itself | Scripts break, or policy is weakened to `unsafe-inline` | Keep nonce CSP in MVC; use Akamai only to preserve or conditionally pass it |
| Multiple hostnames use different properties | Alternate names may have independent routing | One portal entry point remains weak | Include both public hostnames and canonical redirects in authorized validation |

**Case study - apparent origin-edge disagreement:** The user brief says Akamai, while both passive captures show Microsoft-hosted IIS responses with no explicit Akamai marker [26][27]. The correct conclusion is not "Akamai is absent" or "Shodan bypassed Akamai." It is that edge participation is unresolved from public evidence. This tension makes configuration ownership, not merely header syntax, the central deployment problem.

## Safe Validation And Rollout Plan

All activities in this section are intended for authorized MUJ administrators or a formally scoped assessment. The university security club should not test authenticated or non-public routes without written permission.

### Exact authorized response matrix

| Dimension | Required representative cases | Pass condition |
|---|---|---|
| Hostname | `mujslcm.jaipur.manipal.edu`, `muj.slcm.jaipur.manipal.edu`, and the approved canonical host | One documented canonical redirect and consistent final policy |
| Scheme | HTTP entry and HTTPS destination | HTTP safely redirects; HTTPS supplies intended HSTS after rollout |
| Status | `200`, normal `3xx`, authorized `4xx`, authorized `5xx` sample | Interactive HTML receives framing and content controls consistently |
| Route type | Public login, password recovery, Microsoft identity callback, parent login, student login, static asset | Policy matches content type and workflow requirements |
| Identity mode | Full-page redirect and popup, if both are supported | No COOP or CSP breakage; opener behavior matches design |
| Cache state | Known miss, fresh hit, and revalidated object where operators can control them | Same intended client-visible headers |
| Browser family | Current supported Chromium, Firefox, Safari, and institutional managed browser | No functional regression and expected console behavior |
| Rendering context | Direct navigation and an approved local framing test page | XFO/CSP block or allow exactly the documented institutional use case |

### Phased change program

| Phase | Change | Why this order | Rollback trigger |
|---|---|---|---|
| 1 | Add `nosniff` and explicit Referrer-Policy | Low complexity and predictable semantics | Legitimate asset fails due to incorrect MIME type |
| 2 | Deploy CSP Report-Only with reporting governance | Discovers legacy inline code and external dependencies without blocking | Report volume contains sensitive data or overwhelms operations |
| 3 | Establish complete XFO and `frame-ancestors` coverage | Closes non-XFO interactive-page framing gaps | A documented same-origin or approved cross-origin frame stops working |
| 4 | Enforce a nonce-based CSP progressively | Provides broad browser-side defense in depth | Critical workflow blocked with no safe narrow allowlist |
| 5 | Enable short-age HSTS, then extend | Limits rollback cost while transport inventory matures | Any covered host lacks valid HTTPS or identity callback fails |
| 6 | Add a minimal Permissions-Policy | Reduces unnecessary browser capabilities | Required feature is denied |
| 7 | Introduce COOP in report-only or controlled mode | Highest popup compatibility uncertainty | Microsoft identity, payment, or support popup loses its return channel |
| 8 | Consolidate IIS/Akamai ownership | Prevents drift and duplicate policy | Client response differs across cache, status, or hostname matrix |

CSP reporting must be privacy-reviewed. Violation reports can include URLs and document metadata, so the reporting endpoint needs access controls, retention limits, and redaction appropriate to student systems. This is a governance recommendation based on the sensitivity of an academic portal, not a claim about MUJ's current reports.

## Synthesis: One Policy, Three Enforcement Layers

| Dimension | MVC 5 application | IIS 10 | Akamai edge, if confirmed |
|---|---|---|---|
| Best use | Dynamic nonce generation, route-aware CSP, identity-aware exceptions | Static response headers and native HSTS on supported IIS versions | Uniform public baseline, redirect policy, final downstream normalization |
| Scope | Application-generated responses | Site/server responses under IIS configuration | Client-visible responses matching edge property rules |
| Main strength | Knows view markup and workflow context | Central for a legacy application without editing every controller | Can normalize responses before client delivery [4] |
| Main weakness | Misses responses generated before or outside MVC | Cannot safely generate synchronized per-view CSP nonces as a static value | Public evidence does not verify that sampled MUJ traffic traversed Akamai |
| Cache interaction | Produces origin response | Supplies origin metadata | May serve fresh cached objects without origin retrieval [19] |
| Failure mode | Partial route coverage | Duplicate inherited/static headers | Override, delete, duplicate, or property mismatch |
| Recommended ownership | Enforced nonce CSP | `nosniff`, explicit referrer policy, fallback XFO; HSTS if IIS is authoritative | Preserve CSP; add/normalize static headers only under an approved ownership matrix |

The non-obvious tension is that the broadest control, CSP, is the least suitable for blind edge centralization. The edge can add a CSP field, but MVC is the layer that can generate and bind a fresh nonce to trusted elements. Conversely, `nosniff` and an explicit Referrer-Policy gain little from route-level customization and are easier to own centrally.

A second tension is between security strength and institutional compatibility. `frame-ancestors 'none'`, COOP `same-origin`, HSTS preload, and an ultra-strict CSP may score well in automated tools, yet each can break a legitimate portal dependency. The correct objective is not the highest scanner grade. It is a documented, minimally permissive policy that survives student, parent, identity, error, redirect, cache, and browser workflows.

A third tension is the observed hosting evidence. The technology baseline is strongly corroborated, but the alleged Akamai layer is not visible in the two passive response captures [26][27]. This lowers confidence only in the edge-specific topology, not in the browser semantics or proposed IIS/MVC remediation.

## VERDICT

**Verdict: Materially incomplete browser-side hardening, with one effective but potentially route-limited framing control.**

The exact-host passive snapshot supports the requested finding that `X-Frame-Options: SAMEORIGIN` is present while CSP, HSTS, `X-Content-Type-Options`, Referrer-Policy, Permissions-Policy, and COOP are not visible in the sampled `200 OK` response [27]. XFO materially reduces cross-origin framing on that response, but it does not replace CSP and does not protect any interactive response on which it is omitted.

The most consequential gaps are CSP, HSTS, and `nosniff`. CSP supplies a broad defense-in-depth content and framing policy; HSTS closes future cleartext-navigation opportunities after policy acquisition; and `nosniff` is a comparatively simple defense against MIME interpretation errors. Referrer-Policy, Permissions-Policy, and COOP remain worthwhile, but they require nuanced severity: modern referrer defaults already limit ordinary cross-origin disclosure, feature defaults vary, and COOP can disrupt Microsoft identity popups.

**Overall confidence: High for header semantics and implementation guidance; Medium-High for the sampled MUJ header finding; Medium-Low for Akamai topology.**

| Confidence component | Level | Basis |
|---|---|---|
| IIS/MVC/ASP.NET identification | High | Two recent passive observations report matching values [26][27] |
| XFO presence on public login response | High | Exact `SAMEORIGIN` value appears in both displayed captures [26][27] |
| Six headers not present on sampled exact-host response | Medium-High | The complete displayed snapshot block omits them [27], but only one route/time/state is represented |
| Application-wide absence | Low to Medium | Public evidence does not cover authenticated routes, errors, redirects, or all hostnames |
| Akamai participation and rule precedence at MUJ | Medium-Low | Akamai is stated in the brief but no Akamai identifier appears in the passive captures [26][27] |
| Recommended browser behavior | High | Grounded in MDN, OWASP, Microsoft IIS, and Akamai documentation |

**Final decision:** MUJ should treat this as a prioritized hardening project rather than evidence of a demonstrated compromise. The university should first establish configuration ownership, deploy low-risk static headers, run CSP in Report-Only, validate transport coverage, and then enforce CSP and HSTS through an authorized change process. No exploitation is required to remediate these findings.

## References

1. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
2. *Add an HTTP response header to a web site - Internet Information Services | Microsoft Learn*. https://learn.microsoft.com/en-us/troubleshoot/developer/webapps/iis/www-administration-management/add-http-response-header-web-site
3. *Get to know the request flow*. https://techdocs.akamai.com/property-mgr/docs/understand-the-request-flow
4. *Modify Outgoing Response Header*. https://techdocs.akamai.com/property-mgr/docs/modify-outgoing-response-header
5. *HTTP Strict Transport Security - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Strict_Transport_Security_Cheat_Sheet.html
6. *X-Frame-Options header - HTTP | MDN*. https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Frame-Options
7. *Content-Security-Policy: upgrade-insecure-requests directive - HTTP | MDN*. https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/upgrade-insecure-requests
8. *X-Content-Type-Options header - HTTP | MDN*. https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Content-Type-Options
9. *HTTP to HTTPS Upgrade*. https://techdocs.akamai.com/property-mgr/docs/http-to-https-upgrade
10. *Manipal University*. https://muj.slcm.jaipur.manipal.edu/
11. *mujslcm.jaipur.manipal.edu - urlscan.io*. https://urlscan.io/domain/mujslcm.jaipur.manipal.edu
12. *Content-Security-Policy: frame-ancestors directive - HTTP | MDN*. https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-ancestors
13. *Cross-Origin-Opener-Policy (COOP) header - HTTP | MDN*. https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Opener-Policy
14. *Clickjacking Defense - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Clickjacking_Defense_Cheat_Sheet.html
15. *Permissions-Policy header - HTTP | MDN*. https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Permissions-Policy
16. *Content Security Policy - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html
17. *Content Security Policy (CSP) - HTTP | MDN*. https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP
18. *HTTP Headers - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html
19. *Learn about Akamai's caching*. https://techdocs.akamai.com/property-mgr/docs/know-caching
20. *Mixed content - Security | MDN*. https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Mixed_content
21. *Referrer-Policy header - HTTP | MDN*. https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Referrer-Policy
22. *Strict-Transport-Security header - HTTP | MDN*. https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security
23. *HSTS settings for a Web Site &lt;hsts&gt; | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/configuration/system.applicationhost/sites/site/hsts
24. *Custom Headers &lt;customHeaders&gt; | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/configuration/system.webserver/httpprotocol/customheaders/
25. *Migrate from MSAL Browser v4 to v5 - learn.microsoft.com*. https://learn.microsoft.com/en-us/entra/msal/javascript/browser/v4-migration
26.(http://shodan.io/host/20.244.94.89)
27.(http://shodan.io/host/98.70.14.50)
