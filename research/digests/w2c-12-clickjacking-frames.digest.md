# Digest: w2c-12-clickjacking

## REPORT
Source file: w2c-12-clickjacking-frames.md (243 lines, 37717 bytes). Framing control comparison between mujslcm.jaipur.manipal.edu and slcm.manipal.edu with an authorized test plan.

## ANSWER SUMMARY
- SecurityHeaders captures 2026-08-25: MUJ sends X-Frame-Options SAMEORIGIN with no CSP (grade D); SLCM sends neither XFO nor CSP (grade F).
- Stack headers confirmed on MUJ: Microsoft-IIS/10.0, x-aspnetmvc-version 5.3, x-aspnet-version 4.0.30319, x-powered-by ASP.NET.
- SLCM public response sets ASP.NET_SessionId HttpOnly with SameSite=Lax; MUJ anti-forgery cookie is HttpOnly with no SameSite shown; Lax excludes iframe navigations but does not fix visual framing.
- urlscan maps both hosts to Microsoft AS8075 and Azure DNS; Akamai claim unverified.
- Office 365 use is confirmed institutionally via a public SOP, but Entra as the SLCM IdP is not proven; MSAL hidden-iframe callbacks are a real pattern that affects policy scope.
- Browsers allow embedding when neither XFO nor frame-ancestors is present, so SLCM's landing response is likely frameable from an unrelated origin.
- Verdict: confirmed policy inconsistency, unproven authenticated impact; fix with CSP frame-ancestors plus aligned XFO at the origin.

## KEY FACTS
- https://securityheaders.com/?q=https%3A%2F%2Fmujslcm.jaipur.manipal.edu%2F&followRedirects=on : XFO SAMEORIGIN, no CSP, full stack headers, grade D.
- https://securityheaders.com/?q=https%3A%2F%2Fslcm.manipal.edu%2F&followRedirects=on : no XFO, no CSP, session cookie Lax, grade F.
- https://slcm.manipal.edu/ : SLCM landing with sign-in content and a confirmation dialog of unknown purpose.
- https://mujslcm.jaipur.manipal.edu/ : MUJ portal landing with sign-in and parent/student choices.
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-ancestors : checks every ancestor, cancels load on disallowed ancestor, no default-src inheritance.
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Frame-Options : DENY/SAMEORIGIN semantics; ALLOW-FROM ignored; meta delivery has no effect.
- https://www.rfc-editor.org/rfc/rfc7034 : historical XFO ancestor-chain divergence; header-only delivery.
- https://crypto.stanford.edu/~dabo/pubs/papers/framebust.pdf : Stanford study of script frame-busting weaknesses.
- https://learn.microsoft.com/en-us/entra/identity-platform/msal-js-avoid-page-reloads : MSAL hidden iframe token renewal and redirect URI loading pattern.
- https://learn.microsoft.com/en-us/iis/configuration/system.webserver/httpprotocol/customheaders/ : IIS customHeaders site-wide baseline control.
- https://techdocs.akamai.com/property-mgr/docs/modify-outgoing-response-header : edge can alter headers only if Akamai is actually in path.
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie : SameSite Lax excludes iframe navigation from cross-site exceptions.
- https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf : requires documented assessment plan, scope, and incident procedures.
- https://urlscan.io/domain/mujslcm.jaipur.manipal.edu : Microsoft AS8075 and Azure DNS attribution record.
- https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf : official MUJ Office 365 and MFA setup material.

## ACTIONABLE LEADS
- Deploy enforced frame-ancestors 'none' plus aligned XFO on SLCM first, then on MUJ while retaining SAMEORIGIN.
- Build a response-class inventory (200, 3xx, 4xx, 5xx, downloads, callbacks) before rollout; identify callback-only pages before choosing 'none'.
- Authorized tests: header baseline, opaque visible-frame check, cookie matrix with test account, JavaScript-off frame-buster check, double-frame matrix on two tester origins, conditional drag-and-drop with dummy data.
- Confirm Entra and edge architecture with owners; origin enforcement is mandatory, edge normalization optional.
- Add CI gates asserting CSP/XFO across route classes; use report-only during discovery.

## FLAGS
- Keen theme is a user premise; theme age does not establish exploitability.
- Akamai confidence 0.25, Entra-as-IdP 0.45, frameability of SLCM 0.70, authenticated impact 0.30; these are analyst labels, not measured probabilities.
- SLCM frameability is inferred from absent headers, not from a render test.
- Drag-and-drop impact is not demonstrated; no target-specific widget observed publicly.
- Captures are single point-in-time responses; per-route headers may vary.

## COVERAGE
Chars read: 37717 (full file to EOF, truncated false).