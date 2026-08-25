## REPORT (w2b-09-mujconnect.md)
OSINT assessment of mujconnect.in, its identity, data flows, and separation from MUJ SLCM. No authentication or endpoint probing. Verdict: unattributed social PWA; SLCM integration and API inventory unproven. 256 lines, 36510 chars, read to EOF, truncated: false.

## ANSWER SUMMARY
- mujconnect.in presents as "MUJ's Own Social Place", a campus companion PWA with anonymous posting, confession or report features, and an AI food chatbot claim.
- The builder or operator is not publicly named; footer says only "2024 MUJ Connect". WHOIS was blocked by a security-check page.
- The historical Android app MUJ Connect (package naman.com.muj, Naman Khator, 2015, 1,000+ downloads, delisted) is a separate artifact with no link to the current domain.
- Login shows "Email or Username" plus "Forgot your password?" and an unnamed "Or continue with" control. Google, phone, and Microsoft 365 login are not confirmed.
- No domain-linked API base URL or endpoint was recovered; the JavaScript asset was not readable through text extraction and the source-map path returned the app shell.
- DNS differs from SLCM (mujconnect.in A records 98.84.224.111 and 18.208.88.157; mujslcm A record 98.70.14.50), consistent with separate placement but not proof of separate ownership.
- No privacy policy was located; "100% Anonymous", "Secure & Private", and "99.9% Uptime" are marketing claims, not verified controls.

## KEY FACTS
- https://mujconnect.in/ - landing page: social networking, anonymous posts, confessions, food chatbot, uptime and anonymity claims.
- https://mujconnect.in/login - Email or Username login, forgot-password affordance, unnamed continuation control.
- https://mujconnect.in/register - Full Name, Username, Email, avatar default or upload, unnamed continuation.
- https://mujconnect.in/manifest.json - PWA manifest: standalone display, portrait, start URL /, campus companion description.
- https://mujconnect.in/robots.txt - references /assets/index-C0ndPmj2.js, CSS, manifest, and service-worker registration.
- https://mujconnect.in/assets/index-C0ndPmj2.js.map - source-map request returned the application shell, no source map.
- https://r.jina.ai/http://mujconnect.in/assets/index-C0ndPmj2.js - extraction blocked by application/javascript content type.
- https://www.appbrain.com/app/muj-connect/naman.com.muj - historical package naman.com.muj, version 1.0, April 18 2015, 4.45 rating, 102 reviews, 1,000+ downloads, no longer on Play.
- https://dns.google/resolve?name=mujconnect.in&type=A - observed A records 98.84.224.111 and 18.208.88.157, 120s TTL.
- https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=A - observed SLCM A record 98.70.14.50.
- https://crt.sh/?q=mujconnect.in&output=json - Let's Encrypt certificate, validity beginning July 30 2026.
- https://mujslcm.jaipur.manipal.edu/Home/Index - SLCM institutional surface with @muj.manipal.edu wording.
- https://github.com/MUJ-Connect/muj-connect - 2021 Node-style repo with server.js; no domain linkage.
- https://github.com/princenaman/MUJ-Connect - Naman Khator 2015 repo; historical association only.
- https://www.whois.com/whois/mujconnect.in - registrant data blocked.

## ACTIONABLE LEADS
- Ask the operator through any published support channel: legal identity, MUJ affiliation, identity providers, data fields, retention, deletion, chatbot provider, vulnerability contact, official app package IDs.
- Monitor crt.sh and DNS for issuing-identity changes and infra drift.
- Request official source disclosure or an authorized review instead of guessing paths like /api/login or /api/posts.
- Model MUJ Connect as a separate trust zone from SLCM; do not assume shared auth or data.
- Do not reverse-engineer the JS bundle, probe endpoints, or create accounts without written scope.

## FLAGS
- Builder attribution is unverified; Naman Khator, GitHub repos, and the @muj_connect Instagram account are false-match risks.
- "100% Anonymous", "Secure & Private", "99.9% Uptime", and "24/7 Support" are product page claims.
- DNS and certificate observations are time-sensitive single captures.
- No privacy policy found; searches surfaced unrelated policies (Manipal Hospitals, Google) that must not be attributed.
- Negative API result means no endpoint recovered, not proof no API exists.
- The 2015 reviews apply to the old Android app, not the current PWA.

## COVERAGE
- File read to EOF: 256 lines, 36510 chars (file_size 36510), truncated: false. Confirmed EOF at line 256, final reference.