## REPORT (w2c-08-header-hardening.md)
Security-header audit for mujslcm.jaipur.manipal.edu from passive Shodan snapshots and vendor docs. Verdict: MATERIALLY INCOMPLETE browser-side hardening with one effective but possibly route-limited framing control. 320 lines, 38580 chars, read to EOF, truncated: false.

## ANSWER SUMMARY
- Exact-host Shodan record dated 2026-08-22 (98.70.14.50) shows Microsoft-IIS/10.0, X-AspNetMvc-Version 5.3, X-AspNet-Version 4.0.30319, and X-Frame-Options SAMEORIGIN. CSP, HSTS, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, and COOP were not observed in the displayed header block. Alternate host 20.244.94.89 matched on 2026-08-18.
- "Not observed in one snapshot" is not proof of global absence: headers can vary by route, status, hostname, cache state, and edge rule. Application-wide absence confidence is Low to Medium.
- CSP is the highest-value gap: nonce-based, roll out Report-Only first, never unsafe-inline. frame-ancestors does not inherit from default-src, so absent CSP also means absent modern framing control.
- HSTS closes the first-visit and downgrade window but is ignored over HTTP; start short, then extend, and treat includeSubDomains and preload as deliberate later steps. Native IIS hsts requires IIS 10.0 version 1709 or later.
- nosniff is the low-risk high-confidence fix but only after Content-Type values are corrected, or legitimate resources will break.
- Referrer-Policy absence is lower urgency because the modern default is strict-origin-when-cross-origin. Permissions-Policy and COOP need compatibility testing, especially COOP against Microsoft identity popups.
- Akamai can add, remove, modify, or pass downstream headers, but neither passive capture shows an Akamai identifier; edge participation is unresolved and the report downgrades Akamai topology to a brief-supplied assertion.
- Ownership split: MVC owns nonce CSP, IIS owns static headers, Akamai preserves or normalizes only under an approved ownership matrix.

## KEY FACTS
- http://shodan.io/host/98.70.14.50 - exact-host snapshot 2026-08-22: IIS 10, MVC 5.3, ASP.NET 4.0.30319, XFO SAMEORIGIN, six headers absent from displayed block.
- http://shodan.io/host/20.244.94.89 - alternate-host snapshot 2026-08-18 with the same principal stack values and XFO value.
- https://mujslcm.jaipur.manipal.edu/ - canonical target, WELCOME TO MUJ PORTAL with @muj.manipal.edu sign-in label.
- https://muj.slcm.jaipur.manipal.edu/ - alternate live hostname with the same public page label.
- https://urlscan.io/domain/mujslcm.jaipur.manipal.edu - domain artifact showing registered domain and a Microsoft ASN association.
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP - CSP purpose, nonce unpredictability and per-response requirement.
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-ancestors - frame-ancestors checks all ancestors and has no default-src fallback.
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security - HSTS semantics and the first-contact gap.
- https://learn.microsoft.com/en-us/iis/configuration/system.applicationhost/sites/site/hsts - native IIS hsts element with the 1709 version requirement.
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Content-Type-Options - nosniff behavior for script and style MIME mismatches.
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Opener-Policy - COOP unsafe-none default, same-origin and same-origin-allow-popups effects.
- https://techdocs.akamai.com/property-mgr/docs/modify-outgoing-response-header - edge add, remove, modify, find-and-replace, and pass behavior for downstream headers.
- https://techdocs.akamai.com/property-mgr/docs/http-to-https-upgrade - Akamai upgrade behavior runs edge-to-origin only and is not a client redirect or HSTS substitute.
- https://learn.microsoft.com/en-us/iis/configuration/system.webserver/httpprotocol/customheaders/ - Web.config customHeaders add, remove, and clear semantics.
- https://learn.microsoft.com/en-us/entra/msal/javascript/browser/v4-migration - MSAL Browser v5 COOP support cited; the report notes MUJ's library is unverified.

## ACTIONABLE LEADS
- Fetch live headers from both hostnames across 200, normal 3xx, authorized 4xx and 5xx, login, password recovery, Microsoft identity callback, parent login, student login, static assets, and cache hit, miss, and revalidated states.
- Confirm the IIS servicing version before assuming native hsts support; verify HSTS presence and max-age on HTTPS responses only.
- Deploy in the proposed order: nosniff and explicit Referrer-Policy, CSP Report-Only, complete XFO plus frame-ancestors coverage, enforced nonce CSP, staged HSTS, minimal Permissions-Policy, COOP last after identity popup testing.
- Verify Akamai property membership from authoritative DNS and Property Manager before writing edge rules; otherwise an edge rule can give false confidence.
- Test framing with an approved local framing page and record XFO and CSP decisions per use case.
- Privacy-review any CSP reporting endpoint for URLs and document metadata before go-live.

## FLAGS
- Akamai assertion versus observation: no Akamai identifier appears in either Shodan capture; the report keeps topology unresolved and rates confidence Medium-Low.
- The six missing headers are "not observed" in one response block; the report explicitly refuses to claim application-wide absence (Low to Medium confidence).
- Shodan banners may be stale or proxied; both observations are dated 2026-08-18 and 2026-08-22.
- Reference 25 points to an MSAL v3 to v4 migration page while the body cites it for MSAL v5 COOP support; verify the version mapping.
- Included Web.config and CSP snippets are labeled illustrative templates, not MUJ production policy.
- Header semantics confidence is High; sampled MUJ finding Medium-High; Akamai topology Medium-Low, per the report's own scoring.

## COVERAGE
- File read to EOF: 320 lines, 38580 chars (file_size 38580), truncated: false. Confirmed EOF at line 320, final reference.