# FINDINGS-DEEPROBE.md — round 2 findings (2026-08-25 late)

Methods: single low-rate requests, synthetic data, no scanners, no auth
attempts. Evidence in recon/probes/. Complements FINDINGS-W0.md (F1-F5).

## F6. Password echo on failed login [P4, VERIFIED]

The server re-renders the submitted password into the password field on a
failed login. Evidence: /tmp capture diff, recon/probes/pw-pw8.html vs
pw-pw300.html, the ONLY body difference (after token strip) is the echoed
value attribute. Echo is HTML-encoded (recon/probes/pw-x-1.html shows
&quot;), so no direct XSS. Impact: passwords remain in the DOM after a
failed attempt; any later XSS or malicious extension reads them. Deviation
from OWASP guidance (clear password server-side on failure). Also: no
server-side maxlength: 300-char password accepted silently.

## F7. Request validation triggers F1-class YSOD [P3, VERIFIED]

Passwords containing angle brackets return HTTP 500 instead of the login
page (recon/probes/pw-x-2.html). ASP.NET request validation rejects the
input, customErrors is off, so each such input is another full stack-trace
leak. F1 now has 4 confirmed trigger families: missing CSRF token,
invalid-base64 enc, valid-base64 enc (decrypt failure), dangerous form
input. The YSOD class is systemic, not one route.

## F8. ReturnUrl "enc" parameter is machineKey-protected [P3(appears), VERIFIED]

/Home/Index?enc=zz -> FormatException (base64 decode). enc with 16 or 48
valid base64 bytes -> HTTP 500 CryptographicException (decrypt step runs).
Proof the enc blob is encrypted with the app key (machineKey/DPAPI). If
the machineKey ever leaks (GitHub search: slcm/mujslcm machineKey, see
w2g-07), encrypted-dataset tampering and code injection become possible.
Keep this conditional finding in the disclosure: ML-KEYS risk register.

## F9. Anti-CSRF cookie: HttpOnly, no Secure flag [P4, VERIFIED]

__RequestVerificationToken set with path=/ and HttpOnly only (recon/
probes/home-headers.txt). Missing Secure on an HTTPS-only portal is a
hardening gap (cookie would transmit over plaintext if any http endpoint
exists; http://mujslcm resolves and returns, see wayback note).

## F10. Edge posture probes, all CLEAN [VERIFIED, no issue]

- PROPFIND / -> 404 (WebDAV off). OPTIONS * -> 400 (locked).
- X-Original-URL / X-Rewrite-URL on /Home/Index -> inert (no rewrite
  bypass; body identical to normal login page).
- trace.axd with X-Forwarded-For 127.0.0.1 -> 403 (IP restriction not
  bypassable via XFF).
- IIS 8.3 tilde probes /~1*/, /C*~1*/, /Content/*~1*/* -> 400 (8.3
  short-name enumeration disabled).
- robots.txt, sitemap.xml, security.txt, .well-known/security.txt ->
  302 to the auth gate (no security.txt: no VDP signal on target).
- aspxerrorpath hint -> standard gate redirect.

## Passive round (keyless public sources)

- urlscan.io: 3 captures of the target (latest 2026-06-16); odd legacy
  capture https://mujslcm.jaipur.manipal.edu:122/ dated 2024-11-20.
- HSTS preload: not preloaded (both domains), consistent with missing
  HSTS header (F-group from wave 2).
- NuGet: only PortableTestAppSLCM1 (non-relevant). No slcm/manipal
  internal packages published.
- Common Crawl latest index: no rows for the target host.
- favicon hash a94f8a8553caea84 (sha256 of favicon.ico, 32038 bytes,
  4 sizes) recorded for Shodan/Fofa lookups with club accounts.

## Net view

The portal is well-gated at the edge (no WebDAV, no tilde, no rewrite
bypass, no trace unlock). Its weakness class is the ASP.NET app layer:
verbose errors everywhere (F1/F7), password echo (F6), cookie hardening
(F9), legacy TLS/headers, and the machineKey-protected blob that makes
key leakage dangerous (F8). Auth-phase tests remain the untapped half:
BOLA on the 13 API routes, session/role confusion, upload handling,
fee-flow integrity, with the registrar-authorized accounts.