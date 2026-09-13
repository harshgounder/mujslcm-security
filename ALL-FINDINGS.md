# MUJ SLCM portal: complete findings record

**Target:** https://mujslcm.jaipur.manipal.edu (MUJ Student Life Cycle Management portal).
One target only. Sibling hosts, test instances and the Microsoft 365 tenant were never
probed. Compiled 2026-09-13 from hands-on reconnaissance, a live layer-mapping pass, and a
research corpus of 135 launches (5,585,870 characters of reports and syntheses, all read to
end of file).

## What this file is

Every finding recorded about the target to date, in one place, including:

- the verified hands-on findings, with their reproduction detail and raw evidence paths
- the low-severity and one-line observations, no threshold applied
- the negative results (probes that came back clean, which are findings of absence)
- the corrections made to our own earlier claims, kept rather than quietly edited
- the research-tier leads that were never live-verified, each labelled as such
- what was never tested at all, named

Sections run strongest evidence first. Read section 1 for the index and stop there if you
only need the picture; sections 2 to 5 are the verified record; section 6 is the long tail
of research-tier material; sections 7 and 8 carry coverage and provenance.

## Method

Single low-rate HTTP requests, public DNS and certificate transparency queries, public
OSINT, and read-only fetches of official documents. No scanners, fuzzers or wordlist tools
ran against the target. No authentication was attempted. No state-changing request was
sent to the target or to any sibling host. Synthetic data only.

Nothing in this file is an exploit. Every item is information disclosure, transport or
cookie hardening, design observation, or an absence.

## Authorization position, binding

Reconnaissance grade throughout. The authenticated phase (IDOR sweeps, session handling,
upload handling, fee-flow inspection, lockout measurement) requires a signed scope letter
from the university plus dedicated test accounts. Everything behind that gate is
deliberately excluded from this file, together with the offensive method pack and the
authenticated test suite that go with it.

## What is deliberately excluded

- The authorization-gated offensive method pack and the authenticated test scripts.
- The raw capture store and the research pipeline source. This file carries findings and
  names the evidence file for each one; it does not duplicate the captures.
- Credential values. Where a source publishes a password or key, the value reads
  `[value withheld]` here and the source is named instead.
- Every fact about the environment this assessment ran from. No addresses, hostnames,
  accounts, tool configuration or assessing-side timestamps appear anywhere below. Only
  target-side observations do.

## Confidence labels

| label | meaning |
|---|---|
| VERIFIED-LIVE | measured by direct observation, reproduced, raw capture on disk |
| VERIFIED-REPO | measured earlier in the campaign and re-confirmed where stated, or taken from an official university document |
| INFERRED | reasoning from observed facts, stated as reasoning |
| UNKNOWN | not observable from outside the host |
| UNVERIFIED-LEAD | appears in the research layer only, never reproduced by hand |

## Severity scale

P1 critical (direct compromise or bulk data access), P2 high (authenticated or
cross-account impact), P3 medium (targeting information or a real but conditional
weakness), P4 low (hardening gap or minor disclosure), INFO (observation, no issue).

## A note on finding identifiers

The campaign's first-pass document numbered the alternate-host observation as F5. The
status board and every later document use F5 for the credential-design observation. Both
are real and both are below: the alternate host is carried as **F5a** and the credential
design as **F5b**, with the original numbering quoted so nothing is lost. Flagging the
collision rather than silently renumbering.

# 1. Findings at a glance

## 1.1 Hands-on findings, campaign and layer pass

| id | finding | sev | status |
|---|---|---|---|
| F1 | Verbose .NET error pages (YSOD) with full stack trace and exact runtime build, customErrors off. Four reproducible trigger families: missing antiforgery token, invalid-base64 `enc`, valid-base64 `enc` (decrypt failure), dangerous form input. Reproduces byte-identically (8,319 bytes, build 4.7.4136.0 / 4.0.30319) | P3 | VERIFIED, byte-level repro |
| F2 | `/trace.axd` returns 403, so ASP.NET tracing is enabled and access-restricted; `/elmah.axd` returns 404 (ELMAH absent). 403 rather than 404 is what proves the handler exists | P4 (first-pass doc wrote P3) | VERIFIED |
| F3 | Version banners: `server: Microsoft-IIS/10.0`, `x-aspnet-version: 4.0.30319`, `x-aspnetmvc-version: 5.3`, `x-powered-by: ASP.NET` | P4 | VERIFIED |
| F4 | Legacy client library: jQuery 1.10.2 (2013) served as its own file alongside jQuery 3.4.1 inside the theme bundle. Two generations on one page | P4 | VERIFIED |
| F5a | Alternate SLCM host `muj.slcm.jaipur.manipal.edu` exists (certificate transparency plus search indexes), resolves to Azure, never probed. Original F5 in the first-pass document | INFO | VERIFIED-REPO (existence), not tested |
| F5b | Credential design: the portal password is the campus Microsoft 365 password, the username grammar is published in the official FAQ, and reset is delegated to Entra SSPR with no local forgot-password flow | P3 | VERIFIED-REPO, official PDFs |
| F6 | The server echoes the submitted password back into the password field on a failed login, producing a response-size oracle (292-byte delta, stable across usernames). Echo is HTML-encoded, so no direct XSS. Also: no server-side maximum length, a 300-character password is accepted silently | P4 | VERIFIED |
| F7 | ASP.NET request validation turns hostile form input into an F1-class YSOD, so the verbose-error class is systemic rather than one route | P3 | VERIFIED |
| F8 | The `enc` parameter is a machineKey-protected blob. Live work refined it into a three-stage oracle: two exception classes and two body sizes separate "not base64" from "base64 but not a valid protected payload" | P3 conditional | VERIFIED |
| F9 | Antiforgery cookie `__RequestVerificationToken` is set HttpOnly with no `Secure` and no observed `SameSite` on an HTTPS-only portal | P4 | VERIFIED-LIVE |
| F10 | Edge posture battery: WebDAV off, OPTIONS locked, no rewrite-header bypass, no tilde short-name enumeration, no trust-based error-detail bypass, no security.txt. Amended: WAF status is UNKNOWN from outside, not absent | INFO | VERIFIED, amended |
| L1 | The full layer stack of the portal, L0 to L13, measured live, each row citing its raw capture (section 4) | INFO | VERIFIED-LIVE 2026-09-13 |

## 1.2 New facts from the lie-hunt recheck

| id | fact | sev | status |
|---|---|---|---|
| N1 | Legacy origin: a 2024-11-20 third-party capture shows the host served from a different address entirely on HTTPS port 122. Both 443 and 122 on that address time out today. Recorded as a migration marker, not a live claim | INFO | VERIFIED-REPO |
| N2 | Route-surface definition corrected: the pre-auth gate absorbs every path of three segments or fewer, so a redirect never proved a route existed (see E1) | INFO | VERIFIED |
| N3 | The port-122 legacy form is a stale-instance risk marker if that origin ever returns | INFO | INFERRED |

## 1.3 Corrections to our own claims

| id | what was wrong | how it was caught | corrected statement |
|---|---|---|---|
| E1 | "302 means the route exists" route oracle. Junk three-segment paths also redirect | live re-probe of 5 path classes | Every path up to three segments redirects to the gate. Only four-segment paths and `.axd` handlers diverge. Route candidates now come from third-party client code, not from redirects |
| E2 | A first re-check of F8 used 24 base64 characters plus two equals signs, an invalid length, so it produced FormatException | the `enc` oracle ladder separated decode failure from decrypt failure | Padding must make the length a multiple of 4, or decoding rejects the input before any crypto runs |
| E3 | testssl reported TLS 1.3 as not offered | its bundled client is OpenSSL 1.0.2, which cannot speak TLS 1.3 | TLS 1.3 IS offered; system OpenSSL 3.x completes a 1.3 handshake |
| E4 | wafw00f scored a WAF from the app's own 500 response | request validation (F7) explains the 500; the redirect loop comes from the auth gate | No attributable WAF; the tool was fingerprinting the application's own error handling |
| E5 | The WAF wording in the first-pass document implied absence | the layer pass could not observe the provider plane | WAF status is UNKNOWN from outside. Recorded as the amendment on the F10 row and on the status board; the layer map's numbered register carries E2 to E4 |

## 1.4 Negative results (probed, no issue found)

These are findings too. Each one is a control that was tested and held.

| # | probe | result |
|---|---|---|
| 1 | Login POST without an antiforgery token | enforced server-side (the 500 is the filter firing), not a bypass |
| 2 | User enumeration by response difference, existing vs random username | byte-identical pages, only the per-request token differs |
| 3 | Server-side validation with empty credentials | field errors rendered server-side; no enumeration signal |
| 4 | Open redirect through `ReturnUrl` | folded into the encrypted `enc` parameter on the same host, no direct open redirect observed |
| 5 | HTTP verb tampering | TRACE/DELETE/PATCH/OPTIONS/PROPFIND/SEARCH 404, PUT 411, GET only in practice |
| 6 | ELMAH | not deployed |
| 7 | Route gate | every guessed application route redirects to the login gate, centralized auth |
| 8 | WebDAV (PROPFIND) | 404, disabled |
| 9 | `OPTIONS *` | 400, locked |
| 10 | `X-Original-URL` / `X-Rewrite-URL` | inert, body identical to the normal login page |
| 11 | `trace.axd` with `X-Forwarded-For: 127.0.0.1` | still 403, IP restriction not bypassable that way |
| 12 | IIS 8.3 tilde short-name probes | 400, short-name enumeration disabled |
| 13 | `robots.txt`, `sitemap.xml`, `security.txt`, `.well-known/security.txt` | all redirect to the auth gate; no VDP signal |
| 14 | `aspxerrorpath` hint | standard gate redirect |
| 15 | Host header override (`Host: evil.example`) | 200, same page, no reflection, no redirect |
| 16 | `X-Forwarded-Host: evil.example` | 200, same page, not consumed |
| 17 | Absolute-URI request target | 200, same page, proxy-style injection ignored |
| 18 | Trust-based error-detail bypass (loopback forwarded-for plus loopback host on the error trigger) | unchanged exception, no bypass |
| 19 | POST with a valid token and empty credentials | 200 with validation messages, no enumeration signal |
| 20 | Port posture | 443 the only reachable port; 80 and 8080 filtered |
| 21 | Static tree | `/Scripts/jquery-1.10.2.min.js` served (94,140 b); `/Scripts/` 403 so the directory exists and listing is denied |
| 22 | Protected paths | `/web.config`, `/Global.asax`, `/bin/`, `/App_Data/`, `/packages.config` all 404 |
| 23 | Package registry | no internal SLCM or Manipal package published on the public registry |
| 24 | Common Crawl index for the host | no rows |
| 25 | HSTS preload status | not preloaded on either domain, consistent with the missing header |

## 1.5 External-report grading, summary

An externally supplied deep-dive on the same target was graded claim by claim against
primary sources. 18 claims checked: 9 VERIFIED, 4 PARTIAL, 3 UNVERIFIED, 1 WRONG and 1
STALE. The report's own ratio, roughly 30 percent verified-valuable, 30 percent stale, 20
percent unsupported and 20 percent unverified, held up. The verified third (fee-page bank
details, repository sprawl, Salesforce instances, library proxy, a deleted repository,
third-party credential harvesters) was adopted into the corpus. Its SAP section is marked
do-not-present: those CVEs do not apply to this stack, and citing them would discredit the
work in front of the university's IT team. The full grading table is in section 5.

## 1.6 Research-tier leads, never live-verified

Carried here so the record is complete. Every row is a lead from the research layer
(section 6), not a verified observation of this repository.

| lead | source | confidence |
|---|---|---|
| 13 named API routes recovered from a public Flutter client (attendance, marks, grades, timetable, OTP, profile families) | w2c-20, w2c-04, w2c-05 | VERIFIED as route names in public client code, UNVERIFIED as server behaviour |
| Dangling CNAMEs on two campus hostnames pointing at an App Service host that no longer resolves | w2c-11, layer pass | VERIFIED (CNAME plus NXDOMAIN) |
| DMARC `p=none` on two of the three family domains, with SPF present, so spoofed mail still delivers | w2c-10, layer pass | VERIFIED posture, abuse not demonstrated |
| A shared credential published in plaintext on a public institutional repository page, naming itself in the page title | w2d-07 | VERIFIED (page content), value withheld here |
| A public document appears to carry campus-network credentials connected to a named department | external review | UNVERIFIED, value withheld, never testable off campus |
| Student-facing third-party sites that ask for portal credentials (four hosts, all resolving) | external review | VERIFIED (existence) |
| Library remote proxy in use, with a reported registration-number-as-password login policy | external review, w2d-07 | host VERIFIED, policy UNVERIFIED |
| Fee page publishes bank account and SWIFT details for manual transfer | external review | VERIFIED |
| Two Salesforce Communities in the student-facing estate | external review | VERIFIED |
| A student-built repository that mirrored SLCM API calls was deleted, so its content is unrecoverable from the platform | external review | VERIFIED (404 today) |
| A commercial leak-tracking service reports 59,820 domain-associated credential records, with its own caveat against breach attribution | w1-04 | VERIFIED as a report, attribution unsupported |
| A secondary-source claim of a library-portal database release with no hash, count or victim confirmation | w1-04 | UNVERIFIED |
| No product-specific CVE for the SLCM product in the public databases searched; the absence evidence is weak, not proof | w1-04 | bounded negative |
| 3000-plus disclosed signing keys from a 2024 vendor incident make key handling a live class if any server-side form remnants exist | w2c-17, w2c-19 | VERIFIED incident, conditional to this target |
| Contradiction: jQuery CVE range membership and KEV status disagreed between two reports | w2f-03 vs w2x-00 | unresolved, do not cite a CVE count |
| MFA is documented as mandatory before Office 365 use in a June 2025 university SOP, with enforcement and coverage unproven | w1-10, w2f-07 | VERIFIED document, enforcement UNKNOWN |

# 2. Verified findings, full text

The two campaign finding documents, verbatim. F1 to F5 come from the first-pass hands-on
reconnaissance; F6 to F10 from the deep-probe round later the same day.

Target: https://mujslcm.jaipur.manipal.edu/
Method: single low-rate HTTP requests + public OSINT. Non-destructive.

## VERIFIED FINDINGS

### F1. Verbose .NET error pages (YSOD)  -  information disclosure, MULTIPATH [P3]

Two confirmed trigger paths, both 500 with full stack trace + versions:

- POST / with UserName+Password but NO __RequestVerificationToken:
  HttpAntiForgeryException (0x80004005), full MVC 5 async stack,
  ".NET Framework Version:4.0.30319; ASP.NET Version:4.7.4136.0"
- GET /Home/Index?enc=zz (garbage in the protected-route param):
  FormatException "Invalid length for a Base-64 char array or string"
  in System.Convert.FromBase64String, full stack. enc is Base64-
  decoded then processed; valid-base64 garbage would hit the
  decryption layer next (machineKey-adjacent surface, do not forge).

Implication: customErrors is off; ANY unhandled exception leaks stack
+ exact patch level (CWE-209). Helps precise exploit targeting.
- Fix: customErrors On / redirect error pages, remove x-powered-by.
- Evidence: recon/mujslcm-post500.html + recon/enc500.html (saved raw)

### F2. trace.axd returns 403 (exists, restricted) [P3]

- GET /trace.axd -> HTTP 403 (not 404). ELMAH.axd -> 404 (clean).
- 403 vs 404 implies ASP.NET tracing is enabled but access-restricted
  (localhost-only is the common config). If ever reachable from an allowed
  network, request traces leak query strings, cookies, session ids.
- Fix: trace enabled="false".
- Evidence: probe table in recon/notes-2026-08-25.md

### F3. Version disclosure headers [P4]

- server: Microsoft-IIS/10.0, x-aspnet-version: 4.0.30319,
  x-aspnetmvc-version: 5.3, x-powered-by: ASP.NET
- Fix: remove x-powered-by, hide version details in IIS.

### F4. Legacy client-side library: jQuery 1.10.2 (2013) [P4]

- Loaded on the login page along with jquery.validate +
  jquery.validate.unobtrusive.
- jQuery 1.x has known issues (CVE-2015-9251 etc: XSS via .html()
  with untrusted input, prototype pollution class). Client-side only here;
  real impact depends on server-side rendering of user data.
- Fix: bump to a maintained 3.x, re-test validation plugins.

### F5. https://muj.slcm.jaipur.manipal.edu exists (alternate SLCM host) [INFO]

- From cert transparency + search engine index; resolves to Azure
  (20.244.94.89) while mujslcm resolves directly to AS8075 Azure
  (98.70.14.50; corrected: NOT Akamai, see REAUDIT-2026-08-25).
- NOT probed (out of stated scope). The team should ask the university what
  this host is; same-codebase risk applies if it is a dev/alt instance.
- Evidence: recon/notes-2026-08-25.md

## TESTED CLEAN (no finding)

- Anti-CSRF on login POST: enforced server-side (the F1 500 is the
  filter firing). Hidden field + cookie both present. GOOD.
- User enumeration: POST with random vs "admin" usernames returns
  byte-identical pages (only per-request CSRF token differs). No server
  side message difference. GOOD.
- Server-side validation: empty UserName/Password POST renders
  "Please enter your User Name" + "Enter Password" field errors
  (client-side bypass does not skip server checks). GOOD.
- Open redirect: ReturnUrl is folded into an encrypted "enc" parameter
  appended to /Home/Index on the same host; no direct open redirect
  observed. VERIFY later with auth context.
- HTTP verbs: TRACE/DELETE/PATCH = 404, PUT = 411/404, OPTIONS = 404.
  No verb tampering surface found. GOOD.
- ELMAH.axd = 404. GOOD.
- Route gate: every guessed app route (/Student/*, /Staff/*,
  /Account/Login, /api/values) 302s to /Home/Index login. Centralized
  auth gate. GOOD.

## INTEL (for the the team's testing plan)

- Username format is PUBLIC in the official SLCM FAQ PDF
  (https://www.jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf):
  "name.registration-number" e.g. garv.2506040062. Register numbers are
  10-digit, batch-prefixed, and appear in university documents, so
  account names are derivable. This makes account-lockout and rate-limit
  controls critical. Check them with the the team's test account.
- Password = "as per official outlook ID": SLCM credentials are the
  Microsoft 365 credentials. Password reset flows to
  passwordreset.microsoftonline.com (Entra SSPR). No SLCM-local
  forgot-password observed. Identity risk sits in Entra integration.
- Contacts (disclosure path, from FAQ PDF):
  - AMS: dms@jaipur.manipal.edu / ams@jaipur.manipal.edu,
    extensions 784 (Rahul Kumawat), 738 (Dinesh Sain), 481 (Rithik
    Chaudhary), Helpline 0141-3999100
  - IT Infra: it.support@jaipur.manipal.edu, ext 144
  - Academic: academic@jaipur.manipal.edu ext 263
- Related public surfaces (evidence only, NOT in scope to test):
  student.mujonline.com (MUJ online student portal), learning.onlinemanipal.com
  (Brightspace/D2L LMS), mujconnect.in (campus companion app),
  sis.manipal.edu/studloginSLCM.aspx (MAHE SIS, WebForms aspx),
  student.manipal.edu.my (Malaysia campus SLCM), mujerp.jaipur.manipal.edu
  (MUJ ERP), mujone.jaipur.manipal.edu (MUJ One), rms.jaipur.manipal.edu,
  helpdesk.jaipur.manipal.edu, admissions.jaipur.manipal.edu
  (NoPaperForms CRM), www.jaipur.manipal.edu/pay-fee-online.php (fees).
- Campus domain stack (DNS): Microsoft 365 mail (MX outlook) + SPF
  includes Brightspace + Cisco Webex domain verification. SLCM sits on
     IIS served from Microsoft Azure AS8075 (corrected: NOT Akamai, see
     REAUDIT-2026-08-25); cert Entrust DV, issued 2025-12-22, one SAN.
- Wayback: first mujslcm capture 2025-01-10 (Home/Index). Jan 2025
  build had a Faculty login tab (dvFacultyLogin) that the current build
  dropped. Faculty/authz flows changed since launch.

## NEXT

- Wait for wave 1 research reports (10 angles, 6/10 landed), write
  synthesis digest.
- Auth-context testing (IDOR, session handling) requires the the team's
  test credentials  -  the engagement owner to supply.

### Deep-probe round (F6 to F10)

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
  4 sizes) recorded for Shodan/Fofa lookups with team accounts.

## Net view

The portal is well-gated at the edge (no WebDAV, no tilde, no rewrite
bypass, no trace unlock). Its weakness class is the ASP.NET app layer:
verbose errors everywhere (F1/F7), password echo (F6), cookie hardening
(F9), legacy TLS/headers, and the machineKey-protected blob that makes
key leakage dangerous (F8). Auth-phase tests remain the untapped half:
BOLA on the 13 API routes, session/role confusion, upload handling,
fee-flow integrity, with the registrar-authorized accounts.

# 3. Lie-hunt recheck and the correction register

A second pass on the same day assumed the first was wrong. Every load-bearing claim was
re-derived from raw responses: 20 of 20 rechecks confirmed, one real error found (E1), and
three new facts added.

Method: second pass assumes the first was wrong. Every load-bearing claim
re-derived from raw responses 2026-08-25 ~22:45 IST. Bodies saved in
recon/reaudit/. Findings docs corrected in place.

## Verified claim recheck (live, all PASS)

| Claim | Live re-probe | Verdict |
|---|---|---|
| F1 tokenless POST -> 500 YSOD HttpAntiForgeryException, 8319 bytes, build 4.7.4136.0/4.0.30319 | same: 500, 8319 B, ysod+build in body | CONFIRMED, byte-identical |
| F1b enc=zz -> 500 FormatException | 500, FormatException | CONFIRMED |
| F8 valid base64 enc -> 500 CryptographicException | 500, CryptographicException (b64 48B) | CONFIRMED |
| F6 pw echo: 300-8 char delta = 292 | delta 292 (20584 vs 20876), echo exact | CONFIRMED (base sizes shift with username, delta stable) |
| F6c echo encoded | value contains &quot; | CONFIRMED |
| F7 angle brackets -> 500 | 500 | CONFIRMED |
| F9 cookie HttpOnly, no Secure | path=/; HttpOnly only | CONFIRMED |
| F10a trace.axd 403 | 403 | CONFIRMED |
| F10b elmah.axd 404 | 404 | CONFIRMED |
| Headers IIS 10.0 / MVC 5.3 / XFO / x-powered-by | exact match | CONFIRMED |
| No user enum (2 usernames same size) | 20584 vs 20584 | CONFIRMED |
| 98.70.14.50 = Azure AS8075 | ip-api + ipwho.is both AS8075 Microsoft, Pune | CONFIRMED (2 sources) |
| 20.244.94.89 / 20.244.0.229 Azure; 59.91.192.229 BSNL AS9829; api.manipal.edu AWS AS16509 | dig + ipwho.is | CONFIRMED |
| 3 Entra realms jaipur 7d0726e8 / muj 27282fdd / manipal 29bebd42 | openid-configuration live | CONFIRMED (GUID prefixes match) |
| mycampus/testmycampus dangling CNAME edtech366.azurewebsites.net | CNAME present, A empty (NXDOMAIN @1.1.1.1) | CONFIRMED |
| uat.manipal.edu = Azure Front Door | CNAME -> uat-ci-mahe-ep-...azurefd.net | CONFIRMED |
| DNS A records (mujslcm, muj.slcm, mujerp, exam) | dig, unchanged | CONFIRMED |
| urlscan 3 captures, 2024-11-20 on port 122 | full JSON: _id, IP 202.131.155.150 (NOT 98.70.14.50) | CONFIRMED + upgraded |

## Errors found and corrected

E1. ROUTE ORACLE WAS WRONG (the one real error). Earlier docs claimed
    "302 = route exists, 404 = route does not exist". Live re-probe:
    /api/values, /zzz.aspx, /Content/nonexistent.css, /zzz/zzz/zzz,
    /Home/zzz ALL 302 to the gate; only 4-segment paths (/Foo/Bar/Baz/
    Quux) and .axd handlers diverge (404/403). The pre-auth gate
    absorbs every <=3-segment path. Consequences:
    - "AttendanceSummaryForStudent route EXISTS" claim is no longer
      supported pre-auth. Route names remain good leads from third-party
      client code (w2c-20), not from 302s.
    - Fixed in: AGGRESSIVE-PLAYBOOK.md, ATTACK-SURFACE-MAP.md, EXEC-
      SUMMARY (this doc becomes the correction record).
E2. FINDINGS-W0 had 2 stale "behind Akamai" phrasings (first-read notes).
    Corrected to AS8075 Azure + pointer to this doc.
E3. EXEC-SUMMARY corpus numbers: runs launched 110 (10+84+15+1), unique
    saved reports 109, digests 109, chars measured 4.3M (was 4.2M est).
    Updated.

## New facts from the recheck (added to map + exec)

N1. Legacy origin: urlscan 2024-11-20 capture shows mujslcm previously
    served from 202.131.155.150 (Ibus on-prem family) on https port 122.
    Today: 443 and 122 on that IP both TIMEOUT (unreachable from our
    network). Old origin inert or decommissioned; do not claim alive.
N2. Route surface definition corrected (E1).
N3. Port-122 legacy form noted as a migration marker; if the old origin
    ever comes back, it would be a stale-instance risk.

## Remaining unverified (kept labeled, not upgraded)

- All wave-2/3 report claims without a live re-probe stay UNVERIFIED.
- machineKey composition (only the crypto-protected enc blob is proven).
- jQuery CVE range contradiction (w2f-03 vs w2x-00) stays open.
- "MFA mandatory June 2025" (from public SOP) not re-fetched live;
  originally cited from university SOP, treat as INFERENCE pending recheck.

## Verdict

1 documented error (E1) with cascade fixed; 20/20 live rechecks
confirmed; zero fabricated numbers found in deliverable docs; all
labeled-UNVERIFIED claims remained labeled.

# 4. The layer map, L0 to L13

The target decomposed layer by layer, measured live on 2026-09-13, every row naming the raw
capture it comes from. Layer sections L0 to L13 first, then the round-3 live measurements,
the clean probes, the corrections, the unknowns, and the summary of what this host is.

Built 2026-09-13 by hands-on probing plus the campaign's verified findings. Every row names the
raw evidence file it comes from, under `recon/layers-2026-09-13/`, `recon/`, or `findings/`.
Confidence labels: VERIFIED-LIVE (measured today), VERIFIED-REPO (measured 2026-08-25 and
re-confirmed where stated), INFERRED (stated as such), UNKNOWN (not observable from outside).

Target: https://mujslcm.jaipur.manipal.edu (MUJ Student Life Cycle Management portal).
Main target only. Nothing was run against the sibling hosts.

## 1. The layer stack

### L0 People and process
| what | value | evidence | confidence |
|---|---|---|---|
| owner | MUJ academic management services, IT infrastructure | FaQs-SLCM.txt, F5 | VERIFIED-REPO |
| disclosure path | the engagement owner, nodal officer, AMS, IT Infra, then CERT-In at 90 days | TEST-PLAN.md | VERIFIED-REPO |
| security.txt | absent (`/security.txt`, `/.well-known/security.txt` both 302 to the gate) | BATTERY-SUMMARY.json | VERIFIED-LIVE |
| bug bounty or VDP | none found for the portal | w2e-02, w2e-12 | VERIFIED-REPO |

Implication: no channel exists for a stranger to report a bug, which is the usual reason low-severity
findings on portals like this stay unpatched for years.

### L1 Domain and DNS
| what | value | evidence | confidence |
|---|---|---|---|
| target host | single A record, 98.70.14.50, no AAAA, no CNAME | dns.json, dns-doh.json | VERIFIED-LIVE |
| parent zones | jaipur.manipal.edu, muj.manipal.edu, manipal.edu all on Microsoft 365 mail | dns-parents.json | VERIFIED-LIVE |
| SPF, jaipur | two v=spf1 records: outlook + Brightspace, and a second with a /32 ip4 + SendGrid + outlook | dns-parents.json | VERIFIED-LIVE |
| SPF, muj | `v=spf1 include:spf.protection.outlook.com -all` | dns-parents.json | VERIFIED-LIVE |
| SPF, manipal.edu | outlook only, `-all` | dns-parents.json | VERIFIED-LIVE |
| DMARC, jaipur | `p=none` with rua | dns-parents.json | VERIFIED-LIVE |
| DMARC, muj | not published | dns-parents.json | VERIFIED-LIVE |
| DMARC, manipal.edu | `p=reject; pct=100` | dns-parents.json | VERIFIED-LIVE |
| DKIM tenancy | jaipur to mujcampus.onmicrosoft.com, muj to mujmanipal.onmicrosoft.com, manipal.edu to learnermanipal.onmicrosoft.com | dns-parents.json | VERIFIED-LIVE |
| nameservers | manipal.edu on Azure DNS (ns1-36.azure-dns.com and siblings), SOA hostmaster contact is awsdns-hostmaster.amazon.com | dns-parents.json | VERIFIED-LIVE |
| tenant verification | two MS= records on jaipur, four on manipal.edu, plus amazonses and an MS=DD record | dns-parents.json | VERIFIED-LIVE |

Two v=spf1 records on one domain is an SPF permerror under RFC 7208, so the jaipur domain effectively
has no enforced SPF at receivers that follow the spec. The zone was built by one provider and hosted
by another, which usually means nobody owns it end to end.

### L2 Edge and ingress
| what | value | evidence | confidence |
|---|---|---|---|
| public IP | 98.70.14.50, AS8075 Microsoft Azure, central India (Pune) | nmap.txt, probes | VERIFIED-LIVE |
| open ports | 443 only. 80 filtered, 8080 filtered | nmap.txt | VERIFIED-LIVE |
| HTTP versions | HTTP/2 and HTTP/1.1 via ALPN | http2-check.txt, testssl.txt | VERIFIED-LIVE |
| reverse proxy or CDN | no reverse-proxy banner, no CDN headers, IP is a plain Azure address | testssl.txt | VERIFIED-LIVE |
| WAF | none attributable. wafw00f's positive verdict is a false positive, see 3.4 | wafw00f.txt | VERIFIED-LIVE |
| edge cache | `cache-control: private` on the login page | home-headers.txt | VERIFIED-LIVE |

### L3 TLS and PKI
| what | value | evidence | confidence |
|---|---|---|---|
| certificate | Entrust DV TLS Issuing RSA CA 2, RSA 2048, single SAN `mujslcm.jaipur.manipal.edu` | tls-cert.txt, testssl.txt | VERIFIED-LIVE |
| chain | Entrust intermediate, Sectigo Public Server Authentication Root R46, USERTrust | tls-chain.txt | VERIFIED-LIVE |
| validity | 2025-12-22 to 2026-12-21, 99 days remaining at probe time | testssl.txt | VERIFIED-LIVE |
| protocols | TLS 1.0, 1.1, 1.2, 1.3 all complete a handshake | tls-protocols.txt, tls-v2.txt | VERIFIED-LIVE |
| suites | 3DES and CBC suites offered, AEAD with forward secrecy offered, no RC4, no export, no NULL | testssl.txt | VERIFIED-LIVE |
| OCSP | stapling offered, not revoked | testssl.txt | VERIFIED-LIVE |
| HSTS | not offered | testssl.txt | VERIFIED-LIVE |
| fallback protection | TLS_FALLBACK_SCSV NOT supported | testssl.txt | VERIFIED-LIVE |
| grading side effects | SWEET32 reported vulnerable (64-bit block ciphers), LUCKY13 potentially vulnerable | testssl.txt | VERIFIED-LIVE |

Legacy protocol support plus 3DES plus no downgrade protection plus no HSTS is the classic
legacy-friendly configuration of an IIS box that has never had a TLS review.

### L4 Host and operating system
| what | value | evidence | confidence |
|---|---|---|---|
| server banner | `Microsoft-IIS/10.0` | home-headers.txt | VERIFIED-LIVE |
| OS | Windows Server with IIS 10 (Windows Server 2016 or later family) | INFERRED from banner | INFERRED |
| patch state | not observable. The verbose error page leaks the ASP.NET patch level, not the OS level | enc-trigger.txt | UNKNOWN |
| response behaviour | no reverse proxy, no ARR headers, direct responder | testssl.txt, home-headers.txt | VERIFIED-LIVE |

### L5 Web server configuration
| what | value | evidence | confidence |
|---|---|---|---|
| error handling | customErrors off. Four reproducible verbose-error triggers | F1, enc-oracle.txt | VERIFIED-LIVE |
| tracing | `trace.axd` returns 403, so ASP.NET tracing is enabled and access restricted. `elmah.axd` 404 | trace-axd.txt, elmah-axd.txt | VERIFIED-LIVE |
| static tree | `/Scripts/jquery-1.10.2.min.js` served (94,140 b). `/Scripts/` returns 403 so the directory exists and listing is denied | BATTERY-SUMMARY.json | VERIFIED-LIVE |
| protected paths | `/web.config`, `/Global.asax`, `/bin/`, `/App_Data/`, `/packages.config` all 404 | BATTERY-SUMMARY.json | VERIFIED-LIVE |
| error pages | two families. MVC error view (2,733 b) for `/Views/`, IIS error page (1,216 b) for unmapped deep paths | body-404-views.html, body-404-app.html | VERIFIED-LIVE |
| method policy | GET 200. HEAD 404. POST and PUT 411. OPTIONS, TRACE, DELETE, PATCH, PROPFIND, SEARCH all 404 | BATTERY-SUMMARY.json, ROUND3.json | VERIFIED-LIVE |
| directory browsing | denied | BATTERY-SUMMARY.json | VERIFIED-LIVE |

### L6 Application framework
| what | value | evidence | confidence |
|---|---|---|---|
| framework | ASP.NET MVC 5.3 on .NET Framework 4.7.4136.0 (patch level leaked in the YSOD) | enc-trigger.txt | VERIFIED-LIVE |
| antiforgery | MVC antiforgery enforced server-side. Empty POST without a token returns 500 HttpAntiForgeryException. Empty POST with a token returns 200 with validation messages | POST_empty_no_token.body, ROUND3.json | VERIFIED-LIVE |
| session cookie | `__RequestVerificationToken`, HttpOnly present, Secure absent, no SameSite attribute seen | home-headers.txt, testssl.txt | VERIFIED-LIVE |
| route gate | every path up to three segments 302s to `/Home/Index`. Deeper paths and handlers diverge | ATTACK-SURFACE-MAP, ROUND3.json | VERIFIED-LIVE |
| enc parameter | a machineKey-protected blob. Three failure stages, two exception classes, two distinct response sizes. See 3.5 | ENC-ORACLE.json | VERIFIED-LIVE |
| post-login routes | 13 route names derived from the public Flutter client, not from probing | w2c-20 | VERIFIED-REPO |
| auth surface | never exercised. Six test scripts exist and are dry-run only | TRACKER.md | VERIFIED-REPO |

### L7 Client layer
| what | value | evidence | confidence |
|---|---|---|---|
| theme | Keenthemes Keen, demo1 tree, served from `/keen/themes/keen/theme/demo1/dist/` | asset-list.txt | VERIFIED-LIVE |
| jQuery | 1.10.2 loaded as its own file (94,140 b) AND 3.4.1 inside `plugins.bundle.js` (4,239,112 b). Two generations on one page | asset-versions.json | VERIFIED-LIVE |
| plugins with versions | Idle Timer 1.0, Waypoints 4.0.1, autosize 4.0.2, bootstrap-timepicker 0.5.2, nouislider 13.1.5 | bundle-components.txt | VERIFIED-LIVE |
| validation plugins | jquery.validate plus jquery.validate.unobtrusive | asset-list.txt | VERIFIED-LIVE |
| source maps | `jquery-1.10.2.min.js.map` 302 (gate), `plugins.bundle.js.map` 404 | sourcemaps.txt | VERIFIED-LIVE |
| client security headers | absent: CSP, HSTS, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, COOP | home-headers.txt, testssl.txt | VERIFIED-LIVE |
| framing | `x-frame-options: SAMEORIGIN` present | home-headers.txt | VERIFIED-LIVE |

### L8 Identity and federation
| what | value | evidence | confidence |
|---|---|---|---|
| portal accounts | username is `name.registrationNumber`, published in the official FAQ PDF | F5, FaQs-SLCM.txt | VERIFIED-REPO |
| password | the user's Microsoft 365 password. Reset delegates to Entra SSPR | F5 | VERIFIED-REPO |
| tenants | jaipur.manipal.edu, muj.manipal.edu, manipal.edu, all federated none, all Managed | oidc-*.json, getuserrealm.xml | VERIFIED-LIVE |
| SSO into the portal | not proven. The login is a local form, the reset link is Microsoft | ATTACK-SURFACE-MAP | VERIFIED-REPO |
| MFA | claimed enforced since June 2025 in the student SOP, not independently verified | w2f-09 | VERIFIED-REPO |
| mail | M365 for all three domains, DKIM per tenant, SPF and DMARC as in L1 | dns-parents.json | VERIFIED-LIVE |

### L9 Data layer
| what | value | evidence | confidence |
|---|---|---|---|
| engine | not observable from outside. MSSQL is the default for this stack | INFERRED | UNKNOWN |
| data classes | marks, results, fee receipts and documents, exam circulars, hostel and transport, library, placement, staff directory, onboarding documents | w2d-01 to w2d-09 | VERIFIED-REPO |
| PII character | student identity plus academic records plus fee records, which is regulated personal data under the DPDP Act 2023 | INFERRED from data classes | INFERRED |
| storage of documents | served through the app, path shape unknown. Downloads are a named post-auth target | TEST-PLAN.md | VERIFIED-REPO |

### L10 Integrations
| what | value | evidence | confidence |
|---|---|---|---|
| admissions CRM | NoPaperForms, `jaipurmanipal.nopaperforms.com`, behind an AWS ELB in ap-south-1 | ct-liveness.json | VERIFIED-LIVE |
| LMS | Brightspace D2L at learning.onlinemanipal.com, plus an SPF authorisation for `a._spf.brightspace.com` | dns-parents.json | VERIFIED-LIVE |
| lecture capture | Impartus, `a.impartus.com` behind an AWS ECS load balancer | ct-liveness.json | VERIFIED-LIVE |
| mail senders | Microsoft 365 plus SendGrid plus Amazon SES | dns-parents.json | VERIFIED-LIVE |
| conferencing | Webex domain verification TXT present | F5 | VERIFIED-REPO |
| mobile app | MUJ Connect (mujconnect.in), a Flutter client whose route names leak the post-auth surface | w1-07, w2c-20 | VERIFIED-REPO |

### L11 Observability and monitoring
| what | value | evidence | confidence |
|---|---|---|---|
| app tracing | ASP.NET tracing enabled and restricted (trace.axd 403) | trace-axd.txt | VERIFIED-LIVE |
| error logging | ELMAH not deployed (404) | elmah-axd.txt | VERIFIED-LIVE |
| SIEM or WAF telemetry | unknown. No sign of an edge control in front of the host | INFERRED | UNKNOWN |
| uptime and change monitoring | the certificate is the only change signal we can watch from outside | tls-cert.txt | INFERRED |

### L12 Estate around the target
| what | value | evidence | confidence |
|---|---|---|---|
| certificate names | 30 names on the jaipur wildcard and host certificates | ct-names.txt | VERIFIED-LIVE |
| names that resolve | 18 of 30 | ct-liveness.json | VERIFIED-LIVE |
| Azure plane | mujslcm 98.70.14.50, muj.slcm and npfslcm 20.244.94.89, mujerp 20.244.0.229, mujone 52.172.36.15, mycampus and testmycampus on edtech366.azurewebsites.net | ct-liveness.json | VERIFIED-LIVE |
| AWS plane | jaipur.manipal.edu and www 3.108.105.201, admissions on a NoPaperForms ELB, lcs on an Impartus ECS ELB, all ap-south-1 | ct-liveness.json | VERIFIED-LIVE |
| on-prem plane | rms 202.131.155.153, testerp 202.131.155.152, dms 1.186.160.28, dmsmuj 1.186.160.19, idp and pms 1.186.160.23 | ct-liveness.json | VERIFIED-LIVE |
| test instances | testerp and testmycampus both resolve and both were left untouched | ct-liveness.json | VERIFIED-LIVE |

### L13 Legal and regulatory
| what | value | evidence | confidence |
|---|---|---|---|
| reporting duty | CERT-In Directions 70B, six-hour reporting for specified incidents | cert-in-directions-70B.pdf | VERIFIED-REPO |
| personal data law | DPDP Act 2023, student records are personal data with a breach notification duty | dpdp_act_2023_b.pdf | VERIFIED-REPO |
| authorization position | recon only. Nothing state-changing ran. The aggressive phase needs a signed letter and two test accounts | standing orders | VERIFIED-REPO |

## 2. Evidence index

| file | proves |
|---|---|
| home-headers.txt | server and app banners, cookie flags, cache control, no HSTS or CSP |
| home.html, asset-list.txt, asset-versions.json, bundle-components.txt, plugins.bundle.js | client layer, theme, dual jQuery, plugin versions |
| tls-cert.txt, tls-chain.txt, tls-protocols.txt, tls-v2.txt, testssl.txt | TLS and PKI layer |
| nmap.txt, ports.txt | port posture |
| wafw00f.txt | the edge verdict and its false positive |
| enc-oracle.txt, ENC-ORACLE.json, enc-*.body | the enc parameter oracle, three stages |
| BATTERY-SUMMARY.json, ROUND3.json | method matrix, path classes, host header handling, validation recheck |
| body-404-views.html, body-404-app.html | the two error-page families |
| dns.json, dns-doh.json, dns-parents.json, ct-names.txt, ct-liveness.json | DNS layer and the estate |
| nuclei-lab.txt | the scanner toolchain exercised against a local lab only |

## 3. Round 3, live, 2026-09-13

All rows below come from the scripts in `scripts/` and the captures listed above. Single requests,
1.6 s apart, target only.

### 3.1 The estate has three hosting planes, not one
| host | resolves to | plane | note |
|---|---|---|---|
| mujslcm.jaipur.manipal.edu | 98.70.14.50 | Azure AS8075 | the target, central India |
| muj.slcm.jaipur.manipal.edu | 20.244.94.89 | Azure | alternate SLCM host |
| npfslcm.jaipur.manipal.edu | 20.244.94.89 | Azure | NoPaperForms SLCM naming |
| mujerp.jaipur.manipal.edu | 20.244.0.229 | Azure | ERP |
| mujone.jaipur.manipal.edu | 52.172.36.15 | Azure south India | MUJ One |
| mycampus.jaipur.manipal.edu | edtech366.azurewebsites.net | Azure App Service | direct azurewebsites host, no Front Door |
| testmycampus.jaipur.manipal.edu | edtech366.azurewebsites.net | Azure App Service | test instance shares the app service |
| jaipur.manipal.edu and www | 3.108.105.201 | AWS | CloudFront range, not Azure |
| admissions.jaipur.manipal.edu | NoPaperForms, then a prodvpc web LB in ap-south-1 | AWS ELB plus vendor | third party CRM |
| lcs.jaipur.manipal.edu | Impartus, then a prod ECS LB in ap-south-1 | AWS ECS plus vendor | lecture capture vendor |
| rms.jaipur.manipal.edu | 202.131.155.153 | on-prem, Jaipur ISP | not cloud |
| testerp.jaipur.manipal.edu | 202.131.155.152 | on-prem, Jaipur ISP | test ERP, adjacent IP to RMS |
| dms.jaipur.manipal.edu, dmsmuj.jaipur.manipal.edu | 1.186.160.28, 1.186.160.19 | on-prem | document management |
| idp.jaipur.manipal.edu | 1.186.160.23 | on-prem | an identity provider host, role not established |
| pms.jaipur.manipal.edu | 1.186.160.23 | on-prem | shares the IP with idp, role not established |

The portal is not a standalone box. It lives in an estate that spans Azure, AWS and on-prem ranges,
with two separate test-instance hosts and an identity provider host whose role is still open. Anything
learned about the SLCM host has to be re-checked wherever the same code runs, and the test instances
are the likeliest place a same-codebase instance is reachable.

### 3.2 DNS layer, parents done properly
The first pass queried the host label for MX and TXT records, which is empty by design. Corrected
against the parent domains, in the table in L1.

Two v=spf1 records on one domain is an SPF permerror, which means the domain effectively has no
working SPF policy at receivers that follow RFC 7208.

### 3.3 Edge and protocol posture, measured
- 443 open, 80 filtered, 8080 filtered (dockerised nmap 7.98)
- TLS 1.0, 1.1, 1.2 and 1.3 all complete a handshake
- 3DES and CBC suites offered, which produces the SWEET32 verdict. LUCKY13 reported as potentially vulnerable. TLS_FALLBACK_SCSV not supported, so downgrade prevention is absent
- OCSP stapling offered, not revoked. Certificate is Entrust DV, RSA 2048, single SAN, valid to 2026-12-21
- No HSTS, no public key pinning, no reverse-proxy banner
- No WAF is attributable, see 3.4

### 3.4 The wafw00f result is a false positive, explained
wafw00f 2.4.2 reports the site "seems to be behind a WAF or some sort of security solution", with the
reason that a normal request returns 200 and an XSS string returns 500. That 500 is ASP.NET request
validation, already recorded as F7. The same run then failed with an exceeded-redirect loop caused by
the app's catch-all gate. Four requests total. The honest reading is no attributable WAF, and a
fingerprinting tool scoring the app's own error handling as an edge control. This agrees with F10 and
adds the mechanism.

### 3.5 The enc parameter is a three-stage oracle
Refines F8 from a two-case observation into a graded oracle. All live, all reproducible.

| enc value | status | body | exception | stage |
|---|---|---|---|---|
| absent | 200 | 20,045 b | none | normal login page |
| empty string | 500 | 5,509 b | CryptographicException | base64 ok, decrypt fails |
| 1, 2 or 3 chars | 500 | 4,942 b | FormatException | base64 decode rejects the input |
| length not a multiple of 4 | 500 | 4,942 b | FormatException | base64 decode rejects the input |
| url-safe characters or whitespace | 500 | 5,532 b | FormatException | base64 decode rejects the input |
| `AAA=` or `AAAA` | 500 | 5,084 b | CryptographicException | base64 ok, decrypt fails |
| 32 characters, no padding | 500 | 5,084 b | CryptographicException | base64 ok, decrypt fails |
| 24 characters plus two equals signs | 500 | 4,942 b | FormatException | padding invalid for that length, decode rejects it |

Two response sizes and two exception classes separate "not base64" from "base64 but not a valid
protected blob". The second class is the machineKey-adjacent surface recorded as F8. The oracle is
useful for confirming what kind of data the parameter carries without ever attempting to forge it.

### 3.6 Probes that came back clean, now closed
| probe | result | reading |
|---|---|---|
| Host: evil.example | 200, same page, no reflection, no redirect | no host-header impact at the login page |
| X-Forwarded-Host: evil.example | 200, same page | not consumed |
| absolute-URI request target | 200, same page | proxy-style injection ignored |
| X-Forwarded-For 127.0.0.1 and Host localhost on the enc trigger | 500 FormatException, unchanged | no trust-based error-detail bypass |
| X-Original-URL: /trace.axd | 200 login page | header not honoured by IIS here |
| POST with a valid antiforgery token and empty credentials | 200, 20,167 b, validation messages | server-side validation active, no enumeration signal |
| static file /Scripts/jquery-1.10.2.min.js | 200, 94,140 b | static handler serves the tree |
| /Scripts/ directory | 403 | directory exists, listing denied |
| /Views/ | 404, 2,733 b, MVC error view | a second error-page family |
| /Home/NoSuchAction/extra/seg | 404, 1,216 b, IIS error page | IIS answers, not the MVC pipeline |

Two error-page families means two handlers answer an unmapped path, which is a routing detail worth
knowing before any post-auth work.

### 3.7 Tool log for this pass
| tool | version | where it ran | outcome |
|---|---|---|---|
| curl battery | 8.x | target | 46 targeted requests, all saved |
| wafw00f | 2.4.2 | target | generic verdict, false positive, 4 requests |
| testssl.sh | 3.3dev | target | protocols, suites, vulnerabilities, headers |
| nmap | 7.98 in docker | target | 443 open, 80 and 8080 filtered |
| openssl s_client | 3.x | target | handshake per protocol, chain, ALPN |
| Cloudflare DoH, crt.sh | API | passive | parent DNS and 30 certificate names |
| nuclei | 3.11.1 in docker, 1,654 templates | local lab only | 12 findings on a plain local server, 2,114 requests, 3 min |

The scanner class (nuclei, ffuf, sqlmap, nikto) stays off the target under standing order 3.1. The lab
run is the same toolchain exercised end to end, so the templates and the invocation are proven ready
for the authorized phase. That satisfies the instruction to use the tools without breaking the order
that protects the target.

## 4. Corrections register, this pass

| id | what was wrong | how it was caught | corrected statement |
|---|---|---|---|
| E2 | my first F8 re-check used 24 base64 characters plus two equals signs, an invalid length, so it produced FormatException | the enc oracle ladder separated decode failure from decrypt failure | padding must make the length a multiple of 4, or the decode rejects it before any crypto runs |
| E3 | testssl reports TLS 1.3 as not offered | its bundled client is OpenSSL 1.0.2, which cannot speak TLS 1.3 | TLS 1.3 is offered. System OpenSSL 3.x completes a 1.3 handshake |
| E4 | wafw00f scores a WAF from the app's own 500 | request validation F7 explains the 500, the redirect loop comes from the auth gate | no attributable WAF |

## 5. Unknowns, and how each one gets resolved

| unknown | why it matters | how to resolve it |
|---|---|---|
| Windows and IIS patch level | decides which IIS or .NET CVEs apply | auth phase, or a banner-safe authenticated probe |
| whether any WAF or IPS sits in front at the provider level | changes what a scan would trip | measured negative from outside; ask the university, or check inside the letter |
| the identity provider host `idp.jaipur.manipal.edu` | could be the SSO component of the same stack | ask, then test inside scope |
| whether the portal federates to Entra or keeps local forms auth | decides whether Entra attacks apply to the portal path | post-auth token inspection on a test account |
| database engine and version | decides SQL injection impact | auth phase |
| what `enc` packs (machineKey protect vs DPAPI vs a wrapper) | decides whether a key compromise is a real path | post-auth code review or the vendor's docs |
| deployment pipeline and whether Kudu or SCM is reachable | App Service style deployment creds are a classic full-takeover path | ask, then test in scope |
| logging and detection coverage | decides whether testing is visible | cooperative: ask the university |
| the sibling and test hosts | same code elsewhere is the usual soft entry | out of scope now. intel only |

## 6. What we are facing

A single-host, legacy-friendly, verbose ASP.NET application on Azure with no edge control in front of
it, no security.txt, no VDP, and three separate families of test and sibling hosts around it. The
identity design means the portal password is the campus Microsoft 365 password, and usernames are
derivable from public documents, so account-level controls (lockout, rate limiting, MFA) carry the
weight. Inside the app the observable weak spots are the verbose error path, the machineKey-adjacent
`enc` parameter, the missing transport hardening and the missing client-side policy headers. None of
that is an exploit, and none of it was pushed further.

This document is research and preparation. Nothing here authorizes testing of the portal or any
sibling host. The aggressive phase stays behind the signed letter and the two test accounts.

# 5. Externally supplied deep-dive, graded

Every load-bearing claim in an externally supplied report on the same target, re-checked
against primary sources (host APIs, DNS, live fetches, keyless search) and graded. Kept in
full because two of its claims would have been embarrassing to restate, and because the
verified third is now part of the corpus.

Date: 2026-08-25 late. Source: externally supplied externally supplied deep-dive on the
same target. Method: every load-bearing claim re-checked against primary
sources live (GH API, DNS, page fetches, keyless search). Verdict scale:
VERIFIED, PARTIAL, UNVERIFIED, STALE, WRONG.

## Graded claims

| # | External claim | Live check | Verdict |
|---|---|---|---|
| 1 | Scribd doc "SOP for Matlab 2018 Installation" exists and covers SMB UNC install setup | Doc indexed on Scribd (id 406368004, title matches), snippet shows RUN-command UNC instructions | PARTIAL: doc VERIFIED, exact creds ([account withheld] / [value withheld]) NOT confirmable (Scribd bot-wall, search throttled) |
| 2 | Portal runs SAP SLcM, SAP CVEs 2024-42373/45284/34690 apply | Our headers: Microsoft-IIS/10.0, X-AspNet-Mvc 5.3, X-AspNet 4.0.30319, ASP.NET antiforgery. SAP NetWeaver never serves these | WRONG for this instance. SAP lineage is historical (w1-03), not current. Do NOT cite these CVEs |
| 3 | CAPTCHA bypass repos matter (L3thal14 etc.) | Current login form has ZERO captcha (captured 2026-08-25). Repos are 2021-era | STALE: no captcha to bypass today |
| 4 | canaryGrapher/slcmAPI archived | Verified via GH API: archived, pushed 2024-02 | VERIFIED |
| 5 | nikeplusdash/SLCM-api + Heroku app live | Repo exists (archived). herokuapp.com resolves; app returns 404 on / and /docs | PARTIAL: repo VERIFIED, app effectively dead (404) |
| 6 | utk3012/SLCM exists | GH API: exists, pushed 2018 | VERIFIED |
| 7 | KrishGoel/slcm-feedback-automation exists | GH API: exists, pushed 2025-04 | VERIFIED |
| 8 | Karan-Palan/web3-muj-slcm now 404 | GH API: Not Found | VERIFIED (deleted; history not confirmable) |
| 9 | fee page exposes bank details | pay-fee-online.php: Canara Bank, account 120030244406, SWIFT CNRBINBBBFD, student.finance@ all present | VERIFIED |
| 10 | Library portal muj.remotlog.com, reg-num password | DNS: AWS ELB ap-south-1 (proxy vendor). Login policy NOT independently confirmable | PARTIAL: host VERIFIED, policy unconfirmed |
| 11 | Third-party surfaces: mujstella.in, slcm.vercel.app, mujguide.in, arcadiaslcm.vercel.app | All resolve (Cloudflare/Vercel) | VERIFIED (existence) |
| 12 | student.onlinemanipal.com = Salesforce | CNAME to live.siteforce.com (Salesforce Communities) | VERIFIED |
| 13 | manipaluniversity.my.site.com exists | Resolves (Salesforce communities via Cloudflare) | VERIFIED |
| 14 | csd-test.manipal.edu/MUJ-RMS | Resolves 45.112.150.248 = Ibus /24 (our portal.manipal.edu family) | VERIFIED (host) |
| 15 | Personnel emails (Anshuman Mohanty CIO etc.) | NONE found on jaipur.manipal.edu homepage | UNVERIFIED (may exist deeper; not confirmed) |
| 16 | Sikkim Manipal 2012 pastebin breach | Not re-verifiable keylessly today | UNVERIFIED |
| 17 | No MFA for students | Consistent with all our evidence (Entra MFA SOP exists for staff; student SLCM = single password) | PARTIAL/consistent |
| 18 | Reddit complaints (login copy-paste, timeouts) | Community noise | UNVERIFIED, low value |

## Net-new intel this review adds (adopted into the corpus)

- Fee page bank data VERIFIED (account 120030244406, SWIFT CNRBINBBBFD):
  disclosure-relevant only, social-engineering angle for students.
- Deleted-repo evidence: Karan-Palan/web3-muj-slcm existed, now gone
  (404). Deleted repos are a real history risk; GitHub API cannot see
  past content without a prior capture.
- Third-party credential-processor sprawl: mujstella.in, mujguide.in,
  slcm.vercel.app, arcadiaslcm.vercel.app (all verified resolving).
  Each asks students for MUJ creds. Risk = harvesting + pan-cameral
  breach. Goes into the IT Infra advisory.
- Salesforce backbone confirmed: student.onlinemanipal.com (live.siteforce
  CNAME) and manipaluniversity.my.site.com (Cloudflare) = two Communities.
- Library remote proxy live on AWS ELB ap-south-1 (muj.remotlog.com):
  login-policy and reg-num-as-password stay UNVERIFIED until someone
  with an account checks the policy page (documented in TEST-PLAN).
- csd-test.manipal.edu resolves 45.112.150.248: same Ibus /24 as
  portal.manipal.edu. Test-labeled host in production IP space.
- External report claimed port-scanning and scanning-style checks as the
  "AGENT MODE" plan: identical items to our TEST-PLAN, no new classes.

## Standing line on the leaked SMB credentials

The Scribd doc, if it contains live campus-network credentials, is the
single most reportable OSINT item of the whole engagement. Handling:
- NEVER test the credentials, from here or from campus. A leaked
  password is still an authorization boundary; connected testing is
  illegal access even inside the the team's letter (the letter scopes the
  web portal only).
- Verify the doc content on campus (Scribd is bot-walled off-campus),
  then include it in the FIRST disclosure to IT Infra with doc ID and
  captured evidence. The university can rotate the account and purge
  the document. This is the kind of finding that makes the team look
  like a security operation.
- The library reg-number-as-password pattern (if confirmed) and the
  third-party harvesters go in the same report as user-facing advisories.

## Corrections to our own corpus

- w1-07 said slcm-app.herokuapp.com "defunct": the host resolves but the
  app returns 404, so "dead in effect" stands, phrasing corrected here.
- No captcha on the CURRENT login form: all captcha-related research
  angles (w2c-06, L3thal14) should be treated as stale background, not
  current surface. Rate limiting and lockout remain untested pre-auth
  (auth-phase item, needs the letter).

## Bottom line

The external report is roughly 30 percent verified-valuable, 30 percent
stale, 20 percent unsupported (SAP CVEs), 20 percent unverified. The
verified 30 percent (bank data, repo sprawl, Salesforce instances,
library proxy, deleted repo, third-party harvesters) is real and now
adopted into the corpus. The SAP section would embarrass the team in
front of IT Infra; do not present it. The Scribd item is the one to
pursue, on campus, as evidence for the first disclosure.[truncated]

# 6. The research layer: domain syntheses and per-run digests

Everything below is research-grade: produced by the report corpus, distilled, and NOT
re-verified by hand. Findings here carry their own confidence labels in the source files.
The syntheses come first because they deduplicate the rest, then the wave indexes, then all
109 per-run digests in filename order, then the wave-5 gap answers in summary form.

## 6.1 Domain syntheses (3)

### 6.1.1 Vulnerability-class synthesis

Source: 35 digest files in research/digests/ (22 w2c, 12 w2f, 1 w2x), each read fully to EOF 2026-08-25. Digest files already carry FLAGS; this synthesis re-verifies no primary sources. Evidence labels: VERIFIED (multiple digests agree on observed data), UNVERIFIED (supplied, single source, or not reproduced), INFERENCE (reasoning chain, not observation).

Target: mujslcm.jaipur.manipal.edu (98.70.14.50, AS8075 Microsoft, IIS 10).

## 1) CROSS-CUTTING THEMES

### Auth model
- Login form exposes '@muj.manipal.edu' label, UserName, Password, hidden __RequestVerificationToken, EmailFor, LoginFor, Forgot Password link to Microsoft password reset (w2c-03, w2c-06, w2f-12).
- Username grammar is public: name.registration-number with official FAQ example garv.2506040062; register number is MUJ-generated and non-editable (w2c-05, w2c-03).
- Two confirmed Entra tenants, both Managed realms, organization Manipal University Jaipur: jaipur.manipal.edu (7d0726e8-bf4b-4ac1-99f1-010fb11f1d3f) and muj.manipal.edu (27282fdd-4c0b-4dfb-ba91-228cd83fdf71) (w2f-07).
- Portal split: target advertises @muj.manipal.edu while sibling muj.slcm.jaipur.manipal.edu advertises @jaipur.manipal.edu (w2f-07).
- M365 confirmed at service level via official MUJ SOP; MFA documented as mandatory before Office 365 use, enforcement and coverage unknown (w2c-22, w2f-07).
- Where SLCM validates passwords is Unknown: PHS, PTA, SAML, writeback, or independent local store all possible (w2f-09). Entra Smart Lockout applies only if passwords reach Entra (w2c-06).
- M365 authenticates the subject, not record ownership, parent delegation, or finance scope (w2c-04).

### Session handling
- Cookie-session model with __RequestVerificationToken pair plus ASP.NET_SessionId; no bearer or JWT found in third-party clients (w2c-20, w2c-21).
- Anti-forgery cookie observed HttpOnly with no SameSite and no Secure on MUJ (w2c-12, w2f-06). Parent slcm.manipal.edu session cookie is HttpOnly with SameSite=Lax (w2x-00, w2c-12).
- SLCM session specifics (cookie names, rotation, timeouts, logout invalidation) Unknown (w2c-02, w2c-21).
- Framework defaults (20 min session, 30 min Forms auth sliding, HttpOnly false, RequireSSL false) must not be reported as MUJ findings (w2c-02).
- Entra cannot directly revoke application-issued session tokens (w2c-02, w2c-07).
- Missing anti-forgery token produces HTTP 500 YSOD with full stack trace: token enforcement present, the defect is verbose error disclosure (w2x-00).

### Upload surface
- No public upload endpoint; FAQ confirms only a mandatory-document question (w2c-14).
- Orientation page lists marksheets, certificates, passport photo, Aadhaar, APAAR ID, affidavits, medical certificate: the highest-privacy document set on the portal (w2c-14).
- 2019 third-party manual: mandatory JPEG/PDF uploads to 2 MB, general Files area, profile picture to 250 KB (w2c-14). Hypotheses, not MUJ proof.
- Layer limits: ASP.NET MaxRequestLength default 4096 KB, IIS maxAllowedContentLength default ~30 MB (w2c-14).
- Downloads must re-authorize per retrieval and serve attachment plus nosniff from an isolated origin (w2c-14).

### Fee flow
- Gateway vendor unverified; Razorpay, BillDesk, CCAvenue patterns are references only (w2c-15).
- jaipur.manipal.edu/pay-fee-online.php exists: SLCM fee entry, SpaceBasic hostel/mess, bank transfer channels (w2c-22).
- No public evidence of fee manipulation, receipt IDOR, callback forgery, or refund abuse (w2c-15).
- CCAvenue does not enforce order_id uniqueness; merchant responsibility (w2c-15).
- Testing is sandbox-only: server-created orders, sub-unit amounts, HMAC signature, webhook idempotency (w2c-15).

### machineKey / ViewState exposure
- No public key exposure on either hostname (w2c-19, w2c-17).
- Default key mode is AutoGenerate,IsolateApps; a public AutoGenerate literal is not a leaked secret (w2c-19).
- MVC anti-forgery tokens are MachineKey.Protect blobs (purpose AntiForgeryToken.v1); Katana SystemWeb data protection delegates to MachineKey. Key risk is not ViewState-only (w2c-19, w2c-01).
- ViewState is a WebForms mechanism; relevant only if .aspx remnants exist. None identified publicly (w2c-17).
- Dec 2024 Microsoft incident: one public static key used for code injection; 3000+ disclosed keys flagged (w2c-17, w2c-19).
- Key equality between mujslcm and muj.slcm hostnames Unknown (w2c-19).

### WAF posture
- Direct A record 98.70.14.50, AS8075 Microsoft (Pune) inside 98.70.0.0/15, no PTR, no CNAME to an Akamai edge hostname (w2x-00, w2f-06, w2c-11, w2f-11, w2c-22).
- Akamai premise contradicted at DNS and BGP layer; a historical Akamai layer is possible but not established (w2x-00, w2f-06).
- WAF presence and rules not publicly verifiable; a 403 or Access Denied body is not attribution to any layer (w2f-12).
- Lockout threshold, counter key, duration, CAPTCHA state indeterminate; no visible initial CAPTCHA in the captured form (w2c-06).
- IIS Request Filtering substatus codes (404.5-404.15) are the telemetry path (w2c-03, w2x-00).
- Supplied PUT 411 and OPTIONS/DELETE 404 observations are not reproduced; 411 proves only framing enforcement, not WebDAV (w2c-18).

## 2) TOP VERIFIED LEADS

1. Verbose YSOD error disclosure on auth failures. Supporting: w2x-00 (supplied F1 observation 2026-08-25), w2c-01 (token mechanics). Label: VERIFIED per repo context, single-hand observation. Why: full stack traces expose internals and versions that tune every other test; reachable pre-auth.
2. Obsolete jQuery on the login asset tree. Supporting: w2f-03, w2f-05, w2x-00 (Wayback CDX: Keen demo1 tree with jquery-1.10.2.min.js plus 3.4.1 in the plugin bundle). Label: VERIFIED (asset presence), INFERENCE (reachability). Why: CVE-2015-9251, CVE-2019-11358, CVE-2020-11023 cover 1.10.2 (w2f-03); CVE-2020-11023 KEV-listed per w2x-00; no CSP means any confirmed sink is directly exploitable (w2c-08).
3. Version banner exposure. Supporting: w2c-08 (Shodan), w2c-12 (SecurityHeaders), w2f-06 (hackertarget), w2x-00 (SSL Labs). Label: VERIFIED. IIS 10, X-AspNetMvc-Version 5.3, X-AspNet-Version 4.0.30319, X-Powered-By ASP.NET. Why: enables precise CVE mapping (w2f-02, w2f-01); 4.7.4136.0 maps to .NET 4.7.2 servicing lineage, patch state indeterminate (w2f-02).
4. Public username grammar and register numbers in official PDFs. Supporting: w2c-05, w2c-03 (FAQ example garv.2506040062), w2c-06 (login POST fields). Label: VERIFIED (grammar), INFERENCE (exploitation). Why: account discovery and credential stuffing are the direct consequences (w2c-05); MFA coverage unknown so stuffing may land (w2c-06, w2f-07).
5. Thirteen named API routes from a third-party client. Supporting: w2c-20 (SLCM_APP redirects.dart, marks fields MTE1/MTE2/CWS/ETE/PRS/Total, timetable Year/Month/Type/Dated/PreNext, OTP route), w2c-04 (object families), w2c-05 (SlcmPlus attendance/marks/grades). Label: VERIFIED (route names in public client code), UNVERIFIED (server behavior). Why: BOLA is the top authorization risk (w2c-20); marks, fee receipts, documents, timetable, profile are the sensitive object families (w2c-04).
6. Direct origin exposure, no Akamai edge. Supporting: w2x-00, w2f-06, w2c-11, w2f-11, w2c-09, w2c-22. Label: VERIFIED. Why: if 98.70.14.50 is the origin it is plainly disclosed and edge WAF cannot be assumed; test front-door and origin parity, do not frame as an Akamai bypass (w2x-00).
7. Missing security headers, partial clickjacking control. Supporting: w2c-08, w2f-06, w2c-12 (grade D; XFO SAMEORIGIN only; no CSP, HSTS, nosniff, Referrer-Policy, Permissions-Policy, COOP). Label: VERIFIED (headers), INFERENCE (frameability). Why: no CSP means no frame-ancestors; parent slcm.manipal.edu has neither XFO nor CSP, is likely frameable from an unrelated origin (w2c-12), and is a separate MUJ SLCM login surface (w2x-00).
8. Legacy TLS: TLS 1.0/1.1, 3DES, static-RSA, BEAST, no HSTS. Supporting: w2c-09, w2x-00 (grade B on both hosts). Label: VERIFIED. Why: downgrade and MITM enabling on a credential portal; HSTS absence opens the first-visit downgrade window (w2c-08, w2c-09).
9. Email spoofing allowed: DMARC p=none on jaipur and manipal, SPF hard-fail, no DNSSEC. Supporting: w2c-10, w2f-11, w2f-07. Label: VERIFIED (posture), UNVERIFIED (abuse). Why: phishing to students and parents is the realistic social vector into the M365 credentials the portal depends on (w2f-07, w2f-09).
10. machineKey and WebForms surface. Supporting: w2c-19, w2c-17. Label: UNVERIFIED (no exposure found), INFERENCE (conditional risk). Why: if any .aspx or __VIEWSTATE appears post-login, MachineKey becomes the single gate to code injection per the Dec 2024 incident (w2c-17, w2c-19); MVC antiforgery also rides on MachineKey, so farm consistency matters for CSRF diagnosis (w2c-01, w2f-04 issue #328).

## 3) CONTRADICTION CLUSTERS

1. Akamai presence. w2f-01, w2f-02, w2f-03, w2f-04 run on the externally supplied "behind Akamai" premise; w2x-00, w2f-06, w2c-11, w2c-22, w2f-11, w2c-09 contradict it with a direct A record, AS8075 ownership, and no edge CNAME. w2f-12 and w2c-08 keep attribution unresolved pending telemetry. Resolution: treat Akamai as an unverified claim and test against Microsoft/Azure topology (w2x-00).
2. CVE-2020-11022 range for jQuery 1.10.2. w2x-00 counts it in range (NVD record >=1.2, <3.5.0); w2f-03 excludes it (current CVE.org record >=1.12.0, <3.5.0). Both cite canonical records. Resolve before any final CVE count (w2f-03 FLAGS, w2x-00 FLAGS).
3. KEV status of CVE-2020-11023. w2f-03 states none of the four jQuery CVEs appears in the CISA KEV catalog; w2x-00 states CISA added CVE-2020-11023 to KEV on 2025-01-23, citing the CISA alert. Direct conflict, both dated 2026-08. Re-check KEV before citing either.
4. Shared password claim. w2c-05 and w2c-03 attribute "password is the official Outlook ID" to the SLCM FAQ; w2f-09 says no citable FAQ copy was found and treats it as a supplied premise; w2c-07 could not independently locate the sentence. w2c-05 also did not re-fetch the PDF. Resolution: re-fetch FaQs-SLCM.pdf once before relying on the claim (w2f-09, w2c-05 FLAGS).
5. jQuery version inventory. w2f-05 shows jquery 3.4.1 inside the Keen plugin bundle while w2x-00 and w2f-03 key on jquery-1.10.2.min.js; both archived under the same Keen demo1 tree. Dual load and execution order unresolved (w2f-05).
6. Digest count on disk vs task brief. 35 files exist (22 w2c + 12 w2f + w2x-00) not 34 (21 + 13). w2c-22 exists beyond the stated 21; w2f-12 plus w2x-00 complete the stated 13.
7. Supplied verb observations. w2c-18 reports PUT 411 and OPTIONS/DELETE 404 as supplied but not reproduced; w2f-01 and w2c-18 agree these prove nothing about WebDAV. No cross-digest conflict, but do not cite as findings (w2c-18 FLAGS).

## 4) WHAT TO TEST FIRST (once team test credentials exist)

Ordered by information gain per request, following w2x-00's authorized test order and the per-class digests.

1. Error handling baseline with a valid session. Token omission, swap, replay, identity-change cases (w2c-01 L1-L12, P1-P10); check whether F1 YSOD persists behind login and on JSON/AJAX endpoints (w2x-00). Reason: free recon, confirms the enforcement model, exposes internals that tune every later test.
2. Session lifecycle (SLCM-01 to SLCM-11, w2c-02). Compare pre vs post-login identifiers for the auth cookie and ASP.NET_SessionId separately, rotation, real Set-Cookie attributes, logout replay, concurrent sessions, idle and absolute timeouts. Reason: two-cookie mismatch is the false-pass trap; Entra cannot revoke app sessions, so SLCM must.
3. BOLA/IDOR on the 13 known routes. Synthetic students A and B, pre-seeded non-owned references only, 403 vs 404 consistency, semester and role-change scope (w2c-20, w2c-04). Empty StudentCode and Enrollment fields in third-party POSTs make server-side scoping the key question (w2c-20). Reason: marks, fee receipts, documents, and parent delegation carry the highest impact (w2c-04).
4. jQuery sink reachability. Source-to-sink for KTDatatable, KTQuickSearch, error and quick-search HTML sinks; login.js flow; dual jQuery load order (w2f-05, w2f-03). Inert, non-executing markers only in staging (w2f-03). Reason: no CSP means any confirmed sink is directly exploitable (w2c-08).
5. Upload surface discovery and negative matrix. Locate mandatory-document uploads, Files area, profile picture; extension/MIME mismatch, size boundaries, re-encode, cross-account opaque IDs, download re-authorization (w2c-14). Reason: highest-privacy payload (Aadhaar, marksheets) and a 2019 manual documents the surface (w2c-14).
6. Enumeration diffs at login and reset. Preapproved synthetic accounts only, response equivalence for existing vs nonexistent, capped at five consecutive failures with 30-second spacing (w2c-06 Phase B, w2c-05). Reason: confirms or kills the account-discovery lead cheaply and safely.
7. IIS path normalization parity on authenticated routes. Trailing dot/space, backslash, Unicode forms, case, extensionless; staging only (w2c-03 equivalence classes, w2c-18). Reason: auth bypass depends on handler policy parity, not raw request tricks.
8. Alternate-host parity. Run the same battery on muj.slcm.jaipur.manipal.edu (20.244.94.89); same-day Entrust issuance suggests shared infrastructure (w2x-00, w2f-10). Reason: a weaker twin doubles findings at zero discovery cost.
9. machineKey/ViewState. Only if __VIEWSTATE or .aspx appears; then fingerprint keys against the Microsoft disclosed-key hash list owner-side, never publish values (w2c-17, w2c-19). Reason: conditional, but RCE-class when true.
10. Fee flow. Identify the gateway from pay-fee-online.php and receipt pages; sandbox order binding, amount/currency mismatch, webhook signature, receipt IDOR (w2c-15). No production payment mutation. Reason: highest financial impact, lowest feasibility.

## 5) COVERAGE TABLE

All 35 digest files read with read_file offset 1, truncated: false on final call, last content line equals total_lines.

| digest | chars read | EOF |
|---|---|---|
| w2c-01-csrf-mvc5.digest.md | 6885 | confirmed |
| w2c-02-session-management.digest.md | 6165 | confirmed |
| w2c-03-authn-bypass-mvc.digest.md | 7470 | confirmed |
| w2c-04-idor-university-erp.digest.md | 6288 | confirmed |
| w2c-05-register-number-enum.digest.md | 5924 | confirmed |
| w2c-06-rate-limit-lockout.digest.md | 6217 | confirmed |
| w2c-07-password-reset-flows.digest.md | 6729 | confirmed |
| w2c-08-header-hardening.digest.md | 6145 | confirmed |
| w2c-09-tls-config.digest.md | 4482 | confirmed |
| w2c-10-email-spoofing.digest.md | 4276 | confirmed |
| w2c-11-subdomain-takeover.digest.md | 4872 | confirmed |
| w2c-12-clickjacking-frames.digest.md | 4602 | confirmed |
| w2c-13-open-redirect-mvc.digest.md | 4850 | confirmed |
| w2c-14-file-upload-surfaces.digest.md | 5005 | confirmed |
| w2c-15-payment-flow-manipulation.digest.md | 5760 | confirmed |
| w2c-16-ssrf-mvc.digest.md | 4553 | confirmed |
| w2c-17-deserialization-net.digest.md | 4547 | confirmed |
| w2c-18-iis-shortname-webdav.digest.md | 4139 | confirmed |
| w2c-19-machinekey-viewstate.digest.md | 4601 | confirmed |
| w2c-20-api-security.digest.md | 4579 | confirmed |
| w2c-21-jwt-session-tokens.digest.md | 4304 | confirmed |
| w2c-22-third-party-integrations.digest.md | 4460 | confirmed |
| w2f-01-iis10-cve-sweep.digest.md | 5978 | confirmed |
| w2f-02-dotnet-patch-level.digest.md | 5427 | confirmed |
| w2f-03-jquery-cve-sweep.digest.md | 5219 | confirmed |
| w2f-04-mvc53-known-issues.digest.md | 6053 | confirmed |
| w2f-05-keen-theme-cve.digest.md | 5955 | confirmed |
| w2f-06-akamai-edge.digest.md | 5329 | confirmed |
| w2f-07-entra-tenant-enum.digest.md | 5915 | confirmed |
| w2f-08-brightspace-security.digest.md | 6158 | confirmed |
| w2f-09-campus-ad-patterns.digest.md | 6088 | confirmed |
| w2f-10-ct-cert-patterns.digest.md | 5781 | confirmed |
| w2f-11-dns-hygiene.digest.md | 6003 | confirmed |
| w2f-12-waf-fingerprint.digest.md | 6463 | confirmed |
| w2x-00-tech-stack-redo.digest.md | 6741 | confirmed |

Note: chars read are the digest file sizes on disk; each digest internally reports the larger source-report char count. All reads returned truncated: false.

---

## Surface synthesis

Source: 38 digest files, research/digests/, prefixes w2b (14), w2d (9), w3 (15). Every claim below carries its digest name. All digests read to EOF, see COVERAGE table.

## 1) INFRASTRUCTURE MAP

### Target
- **mujslcm.jaipur.manipal.edu** (primary). Role verified: SLCM student/parent portal, official registration link per FAQ (w2b-01, w3-14). Tech: Microsoft-IIS/10.0, ASP.NET MVC 5.3, ASP.NET 4.0.30319 headers (w2d-06, w3-06, w3-14); Keen theme login assets, jQuery 1.10.2 (w2b-03); 2024 scan showed IIS 8.5 and port 122, 2026 scans IIS 10 (w3-14); 2025-26 fee notice also prints :122 URL form (w2d-03). Cloud: A record 98.70.14.50, AS8075 Microsoft (w2b-01, w3-06, w3-14); 2024 address 202.131.155.150 (w3-14). Forgot Password link to passwordreset.microsoftonline.com (w2b-03, w3-14). Threat relevance: the target; Microsoft-linked recovery present, federation unproven.

### Sibling hosts
- **muj.slcm.jaipur.manipal.edu** (alternate). Role unverified: same portal family, "WELCOME TO MUJ PORTAL", @jaipur.manipal.edu context; FAQ names only the primary (w2b-01, w3-03). Tech: none confirmed, zero URLScan coverage (w2b-01). Cloud: A record 20.244.94.89, AS8075 Microsoft, Pune (w2b-01). Threat: unknown alias, migration or staging surface; no shared backend proven (w2b-01).
- **mujerp.jaipur.manipal.edu** (ERP). Role verified as Dynamics 365 Business Central sign-in, /MUJWEB/SignIn POST (w2b-02, w3-09). Tech: ms-nav layout, Business Central title (w3-09); MVC 5.3/.NET 4.x/IIS 10/Akamai unconfirmed (w2b-02, w3-09). Cloud: A record 20.244.0.229 (w3-09), Azure family unverified region (w3-09). Threat: staff/finance surface, no SLCM linkage proven (w2b-02, w3-09).
- **mujone.jaipur.manipal.edu** (HR). Role verified: "MUJ HR SYSTEM", HR/Login.aspx with employee code, DOB, captcha, policy acknowledgements, PAS Portal link to pas.muj.edu.in (w2b-02, w2b-03, w3-08). Tech: no reliable header capture, archives 2022-08-17 to 2024-08-28 (w3-08). Cloud: A record 52.172.36.15, AS8075 Microsoft, Chennai (w2b-03, w3-08). Threat: staff credential surface; third-party apps (MUJ GO, MUJstella) create phishing surface (w3-08).
- **rms.jaipur.manipal.edu** (Research Data Management System). Role verified by title and notices; not a results system (w2b-04, w3-10). Tech: Login.aspx, WebResource.axd, aspnetForm, Web Forms family (w3-10); MVC/IIS/Akamai unverified (w2b-04). Cloud: A record 202.131.155.153, AS134039 Ibus, convergentindia reverse DNS (w3-10). Threat: Outlook-credential wording exists only on central rms.manipal.edu, not Jaipur host (w3-10); login wall with @jaipur.manipal.edu (w3-10).
- **helpdesk.jaipur.manipal.edu** (ticketing). Role unverified: NXDOMAIN now, certificates logged 2026-01-08 to 2027-01-08, Entrust (w2b-05, w3-11). Tech: none observed; vendor unattributable, osTicket proven only for helpdesk.manipal.edu.my and Freshworks only for servicedesk.manipal.edu (w2b-05, w3-11). Cloud: none resolved (w2b-05). Threat: likely prepared-for-TLS asset, production status unproven (w3-11).
- **hms.manipal.edu** (Hostel Management System, MAHE). Role verified: hostel booking by block and capacity; Jaipur not on campus list (w3-07). Tech: Azure Application Gateway v2 snapshot, no origin headers (w3-07); archive paths include Authorization.aspx, Atom_PayResponse.aspx, HDFCResponse.aspx (w3-07). Cloud: A record 20.44.49.205, AS8075 Microsoft (w3-07). Threat: separate MAHE service; historic payment routes; no MUJ link, MUJ room booking never names hms (w3-07).
- **portal.manipal.edu** (EPF). Role verified: Employee Provident Fund app with user, resigned-employee, admin logins, MAHE ISD footer (w3-06). Tech: IIS 10 and ASP.NET disclosed via 403 on root (w3-06); 2022 archive served generic IIS landing page (w3-06). Cloud: A record 45.112.150.155, AS134039 Ibus (w3-06). Threat: employee surface, separate from SLCM; per-path policy difference root 403 vs reachable /epf (w3-06).
- **webmail.manipal.edu** (mail). Role unverified now: current indexed page titled "VPN Portal", Sophos strings in 2022 archive (w3-05). Tech: historical Exchange 2003 OWA (2006), OWA Light (2012), Outlook Web App (2015/2016) (w3-05). Cloud: A record 218.248.47.16, block 218.248.47.0/26 netname MAHE, covering route AS9829 BSNL-NIB (w3-05); parent domain mail is Microsoft 365 (w3-05). Threat: legacy mail/VPN surface, credential acceptance unestablished (w3-05).
- **exam.jaipur.manipal.edu** (exam). Role unverified: no official source names it (w3-01). Tech: none, URLScan/Shodan/Wayback empty, Netcraft blank (w3-01). Cloud: A record 59.91.192.229, AS9829 BSNL NIB (w3-01). Threat: low-visibility asset with unknown purpose, stack, login flow; not linked to SLCM credentials (w3-01).
- **uat.manipal.edu** (staging). Role verified as MAHE institutional frontend, marketing content, Apply Now (w3-02). Tech: Next.js asset paths, branded Error 500 fallback (w3-02). Cloud: CNAME to uat-ci-mahe-ep-bzgfhcehh0fvhafs.a01.azurefd.net, Azure Front Door, resolver 150.171.109.183 (w3-02). Threat: staging origin outside edge; origin isolation unknown, top control question (w3-02).
- **api.manipal.edu** (API). Role verified: JSON root with one opaque data string, Express (w3-03). Tech: nginx 1.18.0, Ubuntu, Node.js, Express, X-Powered-By, wildcard CORS, Let's Encrypt (w3-03). Cloud: A record 43.205.223.7, Amazon EC2 ap-south-1, AS16509 (w3-03). Threat: SLCM backing unproven, treat as separate trust zone (w3-03); nine api-labeled MAHE hosts exist (w3-03).
- **sis.manipal.edu** (MAHE SIS). Role verified: student/parent portal, studloginSLCM.aspx with date field and captcha, redirects to Fee Kart after login (w3-04, w2b-10). Tech: Web Forms .aspx, legacy routes public (w3-04). Cloud: not fingerprinted (w2b-10). Threat: separate from MUJ SLCM, no shared backend proven; payment routes collect application number, name, email, mobile (w3-04).
- **learning.onlinemanipal.com** (LMS). Role verified: D2L Brightspace tenant, "Powered by D2L Brightspace" (w2b-07, w2b-08, w3-13). Tech: CNAME muj.brightspace.com, /d2l/home/14042 (w2b-08, w3-13); learner-mahe.onlinemanipal.com CNAME manipalonline.brightspace.com (w3-13). Cloud: AWS, IPs 13.55.178.159, 15.134.178.12 (w2b-08, w3-13); D2L states AWS primary (w2b-08). Threat: SAML/Entra unverified, grade sync to SIS unknown, CVE-2021-43129 relevance unknown (w2b-08, w3-13).
- **admissions.jaipur.manipal.edu** (NoPaperForms). Role verified: CNAME to jaipurmanipal.nopaperforms.com through AWS ELB ap-south-1 (w2b-06, w3-12). Tech: vendor SaaS, Meritto rebrand June 2023 (w3-12); vendor API modules Lead, Opportunity, Activity, Form, Payment (w2b-06). Cloud: AWS (w2b-06, w3-12). Threat: fields include identity, contact, guardian, documents, payment; admission-to-SLCM bridge undisclosed (w2b-06, w3-12).
- **student.mujonline.com** (online student portal). Role unverified: sparse "Student Portal" shell with Email label and help-desk text (w2b-07). Tech: Angular-style assets, auth protocol unknown (w2b-07). Cloud: none established (w2b-07). Threat: portal auth unknown; separate from campus SLCM (w2b-07).
- **mujconnect.in** (social PWA). Role unverified: "MUJ's Own Social Place", anonymous posts, food chatbot claim; operator unnamed, no privacy policy (w2b-09). Tech: PWA manifest, Let's Encrypt cert from July 2026 (w2b-09). Cloud: A records 98.84.224.111, 18.208.88.157 (w2b-09). Threat: collects full name, username, email, avatar at register; treat as separate trust zone, possible impersonation risk (w2b-09).
- **pay-fee-online** (fee routes). Role verified as directory page: SLCM for academic fees, SpaceBasic for hostel and mess, Canara Bank transfer with MUVAN account rule (w2b-11, w2d-03). Tech: muj-payservices.nttdatapay.com/DirectPay/MUFee is unconfirmed integration lead (w2b-11). Cloud: none for gateway, gateway attribution unknown for all five vendors (w2b-11). Threat: phishing surface via published MUVAN rule and refund bands (w2b-11).

### Other observed assets
- **mujslcm.manipal.edu** (parent). Unverified: A 202.131.155.151, no other records, zero URLScan/Wayback; best hypothesis orphaned or legacy (w3-14).
- **dms.jaipur.manipal.edu / dmsmuj.jaipur.manipal.edu**. Unverified current role: Wayback only, dmsmuj root 2022 read "MUJ API TESTING!", loginForm.aspx titled "MU SLcM" (w3-15); dms@ / ams@ mailboxes are verified escalation contacts in FAQ (w3-15).
- **slcm.manipal.edu** (MAHE SLcM). Verified separate brand, 2017 copyright (w2b-10, w2b-14); shared product family only, shared code/DB/identity unproven (w2b-10).
- **muj.tracmarks.com**. Unverified: MeritTrac branded login, purpose unknown (w2d-02).
- **Library assets**: manipal-koha.informindia.co.in OPAC, DSpace at 20.219.59.68:8080, muj.remotlog.com, mujlibrary.live (unverified) (w2d-07).
- **pas.muj.edu.in** (PAS Portal link from mujone), **muj.irins.org** (research profiles) (w2b-03, w3-10).

## 2) DATA-EXPOSURE HIGHLIGHTS

Public classes found, with digest names. None of these are inside the SLCM auth boundary; SLCM public surface is a login wall only (w2b-02, w2d-09).

- **Faculty and staff directory**: name, designation, department, institutional email, phone, qualifications, external research links (LinkedIn, IRINS, ORCID, Scopus, Scholar), photos claimed; intentional per Public Self Disclosure-U1 (w2d-09, w2b-12). Contact table with 14 role mailboxes and extensions, T&P ext 751 (w2d-09). SLCM FAQ names AMS staff and extensions (Rahul Kumawat 784, Dinesh Sain 738, Rithik Chaudhary 481) (w3-15).
- **SLCM username template and example identifier**: name.registration number, example garv.2506040062, published in official FAQ (w2d-01, w2b-02, w2b-03, w2d-06). Digit split is analyst inference only (w2d-01).
- **PhD admissions result lists**: names, departments, registration mode, NFS/ABSENT status, selected candidates, Jan 2025, Jul 2024, Jan 2026 (w2d-02).
- **Applicant field schema** (admissions SaaS): identity, contact, academic, guardian, employment, uploaded documents, payment, status, refund rules (2022 manual) (w2b-06).
- **Parent OTP workflow**: OTP to registered parent mobile, unregistered numbers told to email admissions@ (w2b-13).
- **Fee artifacts**: hostel and mess amounts, refund bands, Canara Bank IFSC CNRB0003563 and MUVAN account-number construction rule, reconciliation fields UTR, holder, date, amount (w2b-11, w2d-03).
- **Placement data**: NIRF 2025 median salaries with placed-student counts, stipend range INR 15,000 to 1,25,000; conflicting third-party headlines, keep source-labelled (w2d-08).
- **Exam scheduling metadata**: timetable PDFs with course codes, dates, slots, discipline headings (w2d-04).
- **SIS payment pages**: application number, name, amount, email, mobile; receipt emailed; gateway charge table Atom/HDFC 18% GST, undated (w3-04).
- **Credential-like value in library DSpace page title** at 20.219.59.68:8080, value redacted, treated as exposure incident, P0 disclosure (w2d-07).
- **M365 tenant metadata public**: tenant 27282fdd-4c0b-4dfb-ba91-228cd83fdf71, WS-Fed and OIDC endpoints (w3-13, w3-07).
- **mujconnect.in registration**: full name, username, email, avatar, no privacy policy (w2b-09).
- **Historical webmail**: Domain\user name fields in 2006 Exchange OWA capture (w3-05), historical only.

## 3) TOP LEADS

1. Credential-like value exposed in DSpace repository page title, 20.219.59.68:8080. Evidence: P0 exposure incident, redacted (w2d-07).
2. Fee gateway muj-payservices.nttdatapay.com/DirectPay/MUFee, MUJ-branded, integration unconfirmed. Evidence: search-result lead (w2b-11).
3. mujconnect.in unattributed PWA collecting name and email with anonymity claims, no privacy policy. Evidence: page and manifest captures (w2b-09).
4. dmsmuj.jaipur.manipal.edu 2022 root "MUJ API TESTING!" plus loginForm.aspx titled MU SLcM. Evidence: Wayback captures (w3-15).
5. npfslcm.jaipur.manipal.edu in CT with common name mujslcm.jaipur.manipal.edu. Evidence: CT record 2025-11-16 (w3-12).
6. muj.slcm.jaipur.manipal.edu alternate host 20.244.94.89, zero URLScan coverage, FAQ silent. Evidence: DNS + CT + FAQ gap (w2b-01).
7. api.manipal.edu wildcard CORS and opaque root JSON; nginx 1.18.0 (EOL). Evidence: Shodan and live responses (w3-03), observation not vulnerability (w3-03).
8. helpdesk.jaipur.manipal.edu exact-host certs 2026-01-08 while DNS is NXDOMAIN. Evidence: crt.sh IDs 23628924661, 23628923708 (w3-11, w2b-05).
9. faculty-details.php?url=N sequential IDs. Evidence: passive pattern, testing requires authorization (w2d-09).
10. SIS legacy public routes /OnlinePayment01.aspx, /SLCMRTGS01.aspx, /SLCMMessChange04Blocked.aspx. Evidence: live routes with Wayback from 2013 (w3-04).

## 4) HOSTS WITH GAPS

- **mujslcm**: exact stack versions, Akamai claim (unverified everywhere), M365 or Entra federation, port :122 legacy form, backend and database, grade-to-RMS data flow (w2b-01, w2d-03, w3-14).
- **muj.slcm**: role, purpose, alias vs separate deployment, SSL SANs, migration status (w2b-01).
- **mujerp**: audience, enabled modules, tenant, credential mode, MFA status, Azure region, SLCM relation (w2b-02, w3-09).
- **mujone**: SSO role, PAS portal meaning, backend identity, mobile app ownership (w2b-03, w3-08).
- **rms**: Jaipur tenant ownership, credential protocol (Outlook claim is central-host only), CDN placement, result role (none found) (w2b-04, w3-10).
- **helpdesk**: ticketing vendor, production activation, retirement reason, split DNS (w2b-05, w3-11).
- **hms**: MUJ room-booking linkage, current payment provider, origin behind Azure gateway, legacy hostel.manipal.edu status (w3-07).
- **portal**: EPF data scope, deployment date, stack beyond IIS/ASP.NET (w3-06).
- **webmail**: current live markup, Sophos portal confirmation, legacy OWA path state, /26 announcement (w3-05).
- **exam**: purpose, owner, stack, TLS state, SLCM credential bridge (w3-01).
- **uat**: origin bypassability, service-tag and X-Azure-FDID enforcement, datastore lineage, production data presence (w3-02).
- **api**: owner, route inventory, auth policy, SLCM backing, CORS justification (w3-03).
- **sis**: meaning of date field, session internals, federation with MUJ SLCM, current payment processor (w3-04).
- **learning.onlinemanipal.com**: SAML and Entra config, IPSIS grade sync, brightness release level, CVE-2021-43129 applicability (w2b-08, w3-13).
- **admissions**: current form schema (2022 manual baseline), SLCM provisioning trigger, payment processor and tokenization (w2b-06, w3-12).
- **student.mujonline.com**: auth protocol, identity provider, ownership (w2b-07).
- **mujconnect.in**: operator legal identity, MUJ affiliation, data retention, chatbot provider (w2b-09).
- **pay-fee-online**: gateway attribution (all five vendors unknown), callback design, transaction template, receipt layout (w2b-11).
- **dms/dmsmuj**: current DNS and TLS state, DMS expansion, AMS relationship (w3-15).
- **mujslcm.manipal.edu parent**: application identity, ownership, orphan or legacy status (w3-14).

## 5) COVERAGE TABLE

All files read in full, EOF confirmed (truncated false on every read). Chars read equals digest file size in bytes.

| Digest | Chars read | EOF |
|---|---|---|
| w2b-01-muj-slcm-alt.digest.md | 4,771 | true |
| w2b-02-mujerp.digest.md | 4,550 | true |
| w2b-03-mujone.digest.md | 5,058 | true |
| w2b-04-rms.digest.md | 3,540 | true |
| w2b-05-helpdesk.digest.md | 4,800 | true |
| w2b-06-admissions-nopaperforms.digest.md | 5,201 | true |
| w2b-07-student-mujonline.digest.md | 4,690 | true |
| w2b-08-learning-onlinemanipal.digest.md | 5,059 | true |
| w2b-09-mujconnect.digest.md | 4,527 | true |
| w2b-10-sis-manipal.digest.md | 4,737 | true |
| w2b-11-pay-fee-online.digest.md | 5,880 | true |
| w2b-12-jaipur-main-site.digest.md | 4,428 | true |
| w2b-13-parents-campus-life.digest.md | 4,724 | true |
| w2b-14-manipal-edu-group.digest.md | 4,745 | true |
| w2d-01-regnum-format.digest.md | 4,250 | true |
| w2d-02-marks-results.digest.md | 4,806 | true |
| w2d-03-fee-documents.digest.md | 5,537 | true |
| w2d-04-exam-circulars.digest.md | 5,484 | true |
| w2d-05-hostel-transport.digest.md | 5,260 | true |
| w2d-06-orientation-docs.digest.md | 4,844 | true |
| w2d-07-library-integration.digest.md | 4,563 | true |
| w2d-08-placement-data.digest.md | 4,847 | true |
| w2d-09-staff-directory.digest.md | 4,846 | true |
| w3-01-exam-jaipur.digest.md | 5,454 | true |
| w3-02-uat-manipal.digest.md | 5,261 | true |
| w3-03-api-manipal.digest.md | 5,491 | true |
| w3-04-sis-manipal-feekart.digest.md | 5,794 | true |
| w3-05-webmail-manipal.digest.md | 5,789 | true |
| w3-06-portal-manipal.digest.md | 5,278 | true |
| w3-07-hms-manipal.digest.md | 4,710 | true |
| w3-08-mujone.digest.md | 4,776 | true |
| w3-09-mujerp.digest.md | 4,244 | true |
| w3-10-rms-jaipur.digest.md | 4,492 | true |
| w3-11-helpdesk-jaipur.digest.md | 4,487 | true |
| w3-12-npfslcm.digest.md | 4,644 | true |
| w3-13-lms-brightspace-muj.digest.md | 4,516 | true |
| w3-14-mujslcm-parent-level.digest.md | 4,563 | true |
| w3-15-dms-muj.digest.md | 4,995 | true |

Total: 38 files, 185,641 chars, all EOF confirmed.

---

## Context synthesis

Scope: 26 digests (w2e-01..12, w2g-01..14) read in full, all EOF confirmed. Target: https://mujslcm.jaipur.manipal.edu. Every claim below cites its digest. Stack facts marked unverified stay unverified; header observation in w2g-14 is the only independent fingerprint.

## 1) PRECEDENT SUMMARY

What other Indian universities, VDPs, and disclosures say about running this engagement safely and getting credit.

- IISc is the only verified first-party campus-wide Indian university VDP: wildcard *.iisc.ac.in, public APIs, mobile apps, no cash bounty, 5-working-day acknowledgment target, ciso@iisc.ac.in (w2e-03). No surveyed university expressly names a student portal in a verified VDP; IISc portal coverage is an inference from the wildcard (w2e-03).
- CERT-In RVDCP coordinates voluntary disclosure: 72-working-hour acknowledgment, 120-day resolution window, no safe harbor, no blanket testing permission, finder stays responsible (w2e-02, w2e-03, w2e-12). The 2022 Directions impose a six-hour incident-reporting clock and 180-day India-resident log retention on covered entities; that duty does not name independent researchers (w2e-01, w2e-02, w2e-11).
- Indian reception varies sharply. IIT Roorkee publicly praised a 16-year-old who found a JEE Advanced portal flaw (w2e-02). CBSE drew an alleged months-long silence before a containment statement (w2e-02). Zomato fixed in a day and published after the fix (w2e-02). IRCTC insurance portal went via CERT-In: report July 23, fix confirmed July 30 (w2e-02).
- University breach history is marks- and identity-centric: Bengaluru North marks tampering via registrar credentials (60+ students, INR 15,000-20,000 per student, three arrests), Bangalore University OTP bypass (55 students), Gauhati cash-for-marks via outsourced data entry (50+ students, 9 arrests) (w2e-01). Payments: fake receipt forgery at Sri Venkateswara University and look-alike domain diversion at Sai Nath (w2e-01). AIIMS ransomware: 5 of 140 servers infected, theft claims reported baseless; infection does not equal exfiltration (w2e-01).
- Disclosures finish weak: 5 of 7 core cases reached police, none published a full technical postmortem; credential acquisition paths remain unknown (w2e-01).
- IITK B.Cyber Pingala case is the direct defensive lesson: client-side CAPTCHA and per-browser OTP limit were reported and allegedly patched with server-side validation and rate limits; a client-visible control must not be the sole enforcement point (w2g-02).
- 90 days is a Project Zero coordination norm, not law and not MUJ policy; publication must be negotiated separately (w2e-02). Model clocks: 3-business-day acknowledgment, 14-day triage, 45-day critical target, 90-day ceiling, separate publication decision; track acknowledgment, technical confirmation, containment, and credit as four separate outcomes (w2e-02).
- Legal boundary: IT Act Sections 43 and 66 make authorization the hard line; written, asset-specific scope is required before any active validation (w2e-02). No safe harbor exists anywhere in the Indian path (w2e-02, w2e-12).
- Practical posture consensus across all digests: policy design and passive OSINT now, no active testing until written authorization; ask MUJ for a named security intake first (w2e-02, w2e-03, w2e-06, w2e-11).

## 2) VENDOR/PRODUCT-FAMILY PICTURE

What SLCM is, who may own it, sibling instances worldwide.

- SLCM = Student Life Cycle Management, an ecosystem label, not one product. MAHE defines it as the single-window suite for attendance, internal and external marks, results, and circulars for students and parents; it replaced the older Academic Management System (w2e-02, w2e-05, w2e-06, w2e-08).
- The vendor behind the current MUJ backend is not publicly established (w2e-04). Model it as layers: portal, ERP core, identity, hosting, integrator (w2e-04).
- Historical packaged-core lead: SAP Student Lifecycle Management, self-reported implementation across Manipal Education entities in 2012 and configuration from 2011 (LinkedIn self-reports, no first-party contract; w2e-04).
- Modernization: Salesforce (Agentforce Education, Data 360, MuleSoft, Tableau) with Deloitte as integrator, announced for MAHE-wide SLCM in March 2026; five AI agents placed in SLCM under the MAGIC program. MAHE-wide, does not prove the MUJ host is Salesforce-based (w2e-04, w2g-08).
- Front end: MUJ login is confirmed Keen product lineage via archived asset paths /keen/themes/keen/theme/demo1/dist/ with login-v1.css and bundles; exact release unverified. demo1 is a layout/build identifier, not a version, staging flag, or default-account evidence (w2e-10). Metronic-family comparators: Netkampuss ERP (sch-avms.netkampus.in) and Avenu Learning LMS India (learn-india.avenulearning.com), versions undisclosed (w2e-10).
- Runtime fingerprint (25 Aug 2026 public header observation): Microsoft-IIS/10.0, X-AspNetMvc-Version: 5.3, X-AspNet-Version: 4.0.30319, X-Powered-By: ASP.NET, X-Frame-Options: SAMEORIGIN. Supports the supplied IIS/MVC 5.3/.NET-family stack for that one observed response only; X-AspNet-Version 4.0.30319 is a version family, not a patch-level inventory (w2g-14). The "MVC 5.3" vs NuGet Microsoft.AspNet.Mvc 5.2.9 discrepancy stands (w2e-06). ".NET Framework 4.x" spans retired releases; only 4.8.1 stays supported (w2e-05, w2e-11).
- Two implementation eras: legacy slcm.manipal.edu shows 2017-2026 Web Forms vocabulary (.aspx routes, MicrosoftAjax assets, jQuery 2.0.3); the MUJ host appears 2025+ with MVC-shaped /Home/Index and Keen assets (w2g-14). Separate hosts, separate timelines; shared backend unproven.
- Sibling instances worldwide: slcm.manipal.edu (MAHE, Web Forms), slcm.manipaldubai.com (Dubai, moderate-high confidence of a separate application generation; UNIKUL-built Android apps MAHE DUBAI-SLCM package com.unikul.manipaldubai, 1K+ downloads, and M-Campus com.unikul.mahedubai, 50+ downloads) (w2e-04, w2e-07), student.manipal.edu.my (Malaysia; entity ambiguity MILA/MUCM/MIU; React-style shell, Clarity analytics; shared family plausible, shared codebase not demonstrated) (w2e-09), muj.slcm.jaipur.manipal.edu (alternate MUJ host; alias or separate deployment unconfirmed) (w2e-04, w2e-11, w2g-03, w2g-12), maheslcmtech.manipal.edu (modernization endpoint with Microsoft tenant SAML path) (w2e-04).
- Outside MAHE but same label family: SMUERP v5 + Vidya (KEN, SMU O365) at Sikkim Manipal (w2e-08), Amizone as the MVC-family near peer (w2e-11).
- Non-attributions to drop: Comviva, Manipal Technologies, JAIN/JGI, Unikul for MUJ, Saral, MasterSoft, Serosoft, TCS iON, Samarth, Hexad, Fedena (w2e-04, w2e-05). Fedena 2.3 open source has the only strong product-level vulnerability record in the set, inapplicable to MUJ unless a tenant is ever confirmed (w2e-05).

## 3) PUBLIC FOOTPRINT

Code, credentials, app stores, communities.

- Top credential finding: KrishGoel/slcm-feedback-automation .env.example carries a populated name, registration number, and password-like value instead of placeholders; treat as potentially compromised, rotate through the university process, clean git history, never test the value (w2g-07, w2g-11).
- Secondary: vikrant500/college_portal_web_and_dbms holds an HTTrack cookies.txt with a populated __RequestVerificationToken entry for the MUJ host; validity unknown (w2g-07).
- Route map: DK10WS/SLCM_APP (SLCM SWITCH, Flutter/FastAPI, 71 commits, created Jun 18 2025) discloses MUJ base URL, Student/Academic/GetAttendanceSummaryList, parent OTP paths, dashboard, change-password flow; session cookie held in a static string, username/password saved via shared preferences (w2g-06, w2g-07).
- Extension cluster: Tejas-Narula/SlcmPlus is DOM-only MV3 augmentation on exact MUJ attendance/marks/grades pages, no credential or network call visible; Chrome Web Store listing unconfirmed (w2g-06, w2g-07, w2g-11). AddisionS/slcm-feedback-form-filler declares <all_urls> and *://*/*, broader than its MUJ description (w2g-07). Firefox SLCM Feedback Auto-Fill requests all-websites access; Detain Shield claims MUJ-only attendance use; both are publisher disclosures, not audits (w2g-04).
- Legacy wrappers target slcm.manipal.edu, not Jaipur: manipalthetalk/App-Backend interpolates regno and password into a shell command (inferred command-injection risk) with wildcard CORS; canaryGrapher/slcmAPI is archived/deprecated; nikeplusdash/SLCM-api advises session logout; sankalp2004/SLCM-is-Dumb runs Selenium/OCR CAPTCHA automation with an .env warning, high sensitivity (w2g-06, w2g-07, w2g-11).
- Registries: zero-object response for mujslcm on npm; no PyPI listings; the only clear published SLCM utility is npm yemit (MIT Manipal, not MUJ). MUJ footprint lives in source channels (GitHub, extensions, APKs, demos), not registries (w2g-11).
- Decoys and non-affiliated: MUJStella, betterSLCM (slcm.vercel.app), slcm-client-unoff.vercel.app, muj.onlinemanipal.com, student.mujonline.com, MUJ-Central, SlcmAndLms-aggregator, Geervan demo (w2g-03, w2g-05, w2g-06, w2g-11).
- App stores: UNIKUL Dubai apps above; SpaceBasic is the official hostel/mess fee channel per the MUJ fee page (w2e-07, w2g-05).
- Communities: Telegram @manipaljaipurfresher (447 direct vs 1,572 directory, counts diverge, do not merge), Discord servers at 1,142 and 1,902 members with no confirmed university endorsement (w2g-13). Reddit: availability complaints (SLCM "crashing every other day"), registration-number rejection after intra-sliding, fee-paid-but-pending, removed results tab, grades decreased; the CGPA leak allegation is unverified with a single commentator's patch claim (w2g-01, w2g-02, w2g-04). Quora footprint is thin, one anonymous attendance answer (w2g-03). X: @Jaipur_Manipal posts are routine campus content; direct X search returned no tweet cards (w2g-04).
- Documents: Scribd hosts a 2025 grade sheet with an SLCM-derived path in the title and a third-party "Eligible Students MUJ-1" claim of registration data; provenance unknown, report privately, never redistribute (w2g-04, w2g-12). Stack Overflow: zero literal mujslcm hits; two Manipal SMTP samples expose a BOPSERVER/Project connection string and a 584-vs-587 port discrepancy, no MUJ-host evidence (w2g-10). Dorks found no confirmed first-party student-record exposure; XLSX-titled results resolving to PDF URLs are a recurring trap (w2g-12).
- Closest security-adjacent official items: FAQ names dms@jaipur.manipal.edu and ams@jaipur.manipal.edu for login trouble and the SLCM registration link (w2g-04); Office 365 SOP v1.0 June 2025 documents mandatory MFA (w2e-11, w2g-08).

## 4) DISCLOSURE PATH

Best practice for MUJ.

- Two parallel tracks for a real finding: confidential notice to MUJ IT and Registrar, plus a direct RVDCP report to vdisclose@cert-in.org.in. Do not wait for a publicly listed nodal officer; none was found (w2e-12).
- MUJ contacts: it.support@jaipur.manipal.edu (IT Infrastructure, extensions 778/300), registrar@jaipur.manipal.edu (Dr Amit Soni, ext 102), registrar.office@jaipur.manipal.edu, admin.office@jaipur.manipal.edu, plus dms@ and ams@ for login-trouble routing (w2e-03, w2e-12, w2g-04). No public security mailbox, VDP, or conforming security.txt exists; the RFC 9116 location returns the portal sign-in page (w2e-03).
- CERT-In lanes: vdisclose@ (RVDCP voluntary coordination, 72-hour ack, 120-day resolution), incident@ for suspected Annexure I incidents (six-hour clock), info@ for general contact; the linked certinvulnform.pdf returned not found at research time, email is the reliable mechanism (w2e-12). Route by ownership: MSRC only for demonstrable Microsoft product flaws, security@akamai.com only for Akamai platform defects; MAHE information-security policy must not be presented as MUJ policy without confirmation (w2e-12).
- 90-day norm: cite Project Zero policy (90-day vendor window, 30-day post-patch disclosure, seven-day for active exploitation) as the coordination model, not as permission; publication is a separate negotiated decision (w2e-02).
- What to document: a report envelope with subject, classification, timing, prior disclosure, researcher preference; a reproducible CVSS v4.0 vector plus an MUJ-specific impact statement; redacted evidence only (no cookies, tokens, credentials, grades, or student identifiers); a timeline tracking acknowledgment, technical confirmation, containment, and credit separately (w2e-02, w2e-12).
- First move: governance request for written scope from MUJ IT, then a proposed MUJ VDP modeled on IISc (policy URL, valid security.txt, named assets, explicit portal status, prohibited techniques, response targets, safe-harbor wording) (w2e-03). No active testing until written authorization exists (w2e-02).
- Stop conditions in team rules: stop at first sensitive record, unexpected privilege, or instability (w2e-02).

## 5) TOP GAPS IN KNOWLEDGE

- Vendor identity of the MUJ SLCM backend: unconfirmed. SAP historical, Salesforce future, current Jaipur backend unknown (w2e-04, w2g-08).
- Is muj.slcm.jaipur.manipal.edu a live alias or a separate deployment? Every digest flags it; owner confirmation required (w2e-04, w2e-05, w2g-03, w2g-04, w2g-12).
- Exact software bill of materials: MVC 5.3 header observed once; .NET patch level, IIS build, NuGet packages, jQuery/Bootstrap versions, Akamai presence all unverified (w2e-05, w2e-06, w2e-10, w2g-14).
- Whether the CERT-In 2022 Directions apply to MUJ as a covered entity: not legally resolved; MUJ counsel should confirm (w2e-12).
- Identity and tenant equivalence across Manipal campuses: Dubai (Microsoft not named on login), Malaysia (MUCM/MILA ambiguity), MUJ (managed Microsoft tenant, MFA SOP). Do not assume one tenant, one flow, or shared codebase (w2e-07, w2e-09, w2e-11).
- Validity and ownership of the KrishGoel credential-like values and the vikrant500 token file: exposure proven, exploitability unknown (w2g-07).
- Provenance of Scribd artifacts (grade sheet, "Eligible Students" list): user upload, misconfiguration, or unrelated posting; unknown (w2g-04, w2g-12).
- Personnel who own or maintain the Jaipur host: four direct SLCM leads (Upadhyay, Vishwaradhya, Khalandar, Muthamadhu) and MUJ-local candidates, none publicly tied to the Jaipur host (w2g-08).
- Salesforce migration timing and effect on the current portal: MAHE-wide announcement only; no MUJ-host evidence (w2e-04, w2g-08).
- No public security intake, no nodal officer, no security.txt: the disclosure routing itself is unconfirmed beyond registrar and IT Infrastructure forwarding points (w2e-03, w2e-12).

## 6) COVERAGE TABLE

All files read via read_file to EOF (truncated: false on every final read). Chars = bytes on disk.

| Digest | Chars read | EOF |
|---|---|---|
| w2e-01-india-uni-breach-history | 5,477 | yes |
| w2e-02-india-uni-vdp | 4,852 | yes |
| w2e-03-disclosure-case-studies | 4,301 | yes |
| w2e-04-slcm-vendor-id | 4,438 | yes |
| w2e-05-india-erp-vendors | 4,392 | yes |
| w2e-06-mit-manipal-systems | 4,468 | yes |
| w2e-07-manipal-dubai | 4,988 | yes |
| w2e-08-sikkim-manipal | 4,759 | yes |
| w2e-09-manipal-malaysia | 4,708 | yes |
| w2e-10-keentheme-portals | 4,658 | yes |
| w2e-11-iis-mvc-student-portals | 4,988 | yes |
| w2e-12-certin-bugbounty | 5,042 | yes |
| w2g-01-reddit-r-manipal | 4,665 | yes |
| w2g-02-reddit-india-academics | 4,958 | yes |
| w2g-03-quora-manipal | 4,247 | yes |
| w2g-04-twitter-x | 4,906 | yes |
| w2g-05-youtube-tutorials | 4,635 | yes |
| w2g-06-github-orgs-teams | 5,031 | yes |
| w2g-07-github-code-muj | 7,656 | yes |
| w2g-08-linkedin-sicm-devs | 7,700 | yes |
| w2g-09-job-postings | 7,009 | yes |
| w2g-10-stackoverflow | 8,125 | yes |
| w2g-11-npm-pypi | 7,309 | yes |
| w2g-12-google-dorks | 6,604 | yes |
| w2g-13-telegram-discord | 7,707 | yes |
| w2g-14-wayback-family | 8,490 | yes |
| TOTAL | 146,113 | 26/26 EOF |

## 6.2 Wave indexes

### 6.2.1 Wave 1 synthesis (10 reports)

Merged 2026-08-25 from research/w1-*.md via review-pass digests (each read to
EOF, coverage audit inline). w1-08 subdomain-surface pending (CT heavy).
All claims below are EVIDENCE TRIAGE: read the parent report before acting.

## Coverage audit

w1-01 39,357 (full) | w1-02 12,321 (full, THIN report, redo launched as
w2x-00) | w1-03 37,324 (full) | w1-04 40,265 (full) | w1-05 47,931 (full)
| w1-06 43,659 (full) | w1-07 37,483 (full) | w1-09 46,547 (full) |
w1-10 44,955 (full)

## Verified platform facts (cross-report consensus)

- Product: SLCM = student life-cycle management (attendance, marks,
  results, broadcasts; MAHE ICT inventory doc). NOT an LMS. Admission
  -> profile -> every student admin function.
- MUJ front-end: ASP.NET MVC 5.3 / .NET 4.x / IIS 10 on Azure central
  india (AS8075, edge IP 98.70.14.50). Form posts UserName/Password +
  EmailFor/LoginFor to "/", MVC antiforgery enforced (F1 verified).
- Legacy MAHE family: WebForms (.aspx): loginForm.aspx, GradeSheet.aspx,
  Print.aspx, WebForm1.aspx, StudentChangePassword.aspx + __VIEWSTATE/
  __EVENTVALIDATION + txtCaptcha. Different generation, same product.
- Two near-identical MUJ entrances: mujslcm.jaipur.manipal.edu and
  muj.slcm.jaipur.manipal.edu (alias/sibling; OUT OF SCOPE to touch).
- Identity: 3 Entra tenants, all Managed (no AD FS); SLCM pw = M365 pw;
  reset via passwordreset.microsoftonline.com; MFA mandatory per
  internal SOP (June 2025) yet published publicly.
- Email posture: SPF -all; DMARC p=none on all domains; Exchange Online
  MX. Spoofing possible (phishing risk to students, not a portal bug).
- Client: jQuery 1.10.2 (2013) + validate 1.11.1; Keen demo1 theme;
  X-Frame-Options only; no CSP/HSTS/nosniff (SecurityHeaders D grade,
  SSL Labs B, TLS 1.0/1.1 live, BEAST warnings).

## Highest-value findings per report

- w1-01: exact attendance route /Student/Academic/AttendanceSummaryForStudent
  (login-gated); fee split SLCM (academic, processor undisclosed) /
  SpaceBasic (hostel+mess) / NTT DATA (mess form) / Razorpay (certificates).
  First-Year-Students-Profile-Registration-Guide.pdf not extractable,
  re-OCR it. Contact tree: registrar (Dr Amit Soni, ext 102), dms@, ams@,
  it.support@, student.finance@, exam.store@, exam.helpdesk@.
- w1-02: header/exposure audit; TLS weak config; jquery CVEs range
  membership (CVE-2015-9251, CVE-2019-11358, CVE-2020-11023); no exact
  theme version; report thin (12K) so full redo launched.
- w1-03: SAP SLcM lineage (2 Manipal Global employee profiles); MAHE
  2026 Salesforce modernization (Deloitte, Agentforce, MuleSoft; MUJ not
  named); public repos model the auth flow: canaryGrapher/slcmAPI
  (archived), DK10WS/SLCM_APP (Flutter + public google-services.json),
  AddisionS/slcm-feedback-form-filler, Anushkakumar10/muj_slcm (
  Django SECRET_KEY + DEBUG=True PUBLIC).
- w1-04: NO confirmed breach anywhere in public record. Brinztech
  2026-02-18 libportal.manipal.edu leak ALLEGATION (unsubstantiated,
  tier 2). LeakRadar 59,820 manipal.edu-associated credentials (not
  attribution). CERT-In 70B: 6h incident reporting, 180d logs. URLScan:
  mujslcm NOT observed; slcm clean x2. No CVEs in NVD/Exploit-DB.
- w1-05: slashdot-level code intel: 4 GitHub repos + npm yemit automate
  SLCM flows; credentials accepted via GET-able handlers (slcmAPI);
  LeakIX 117 service records incl dev-api/dev-techtatva/dev-register;
  CertSpotter 103 manipal.edu names incl dev/uat/preprod; slcm-api.ml +
  slcm-app.herokuapp.com = historic credential-phish vectors still
  possibly live (verify).
- w1-06: biggest PUBLIC data exposure = official PhD PDFs under
  jaipur.manipal.edu/img/pdf/: awardee list (500-scale: names + reg
  numbers + theses) and shortlist PDFs (names + EMAILS + application
  numbers). Register format numeric (FAQ) contradicts 24JTEECS001 claim.
  Retired MAHE routes (Print.aspx etc.) in archives. No marks/hostel/
  fee rosters found.
- w1-07: CampusAdda (com.app.campusadda, Razorpay, OTP, deep links incl
  carpool share tokens; AASA/assetlinks verified) is the clearest native
  app surface; MUJStella (PWA+Android, unaffiliated, SLCM tracker);
  MTTN (10K+, attendance/grades, push); MUJ gym app by Gayatri Software
  (credentials+diet data). NO verified /api/ or Swagger for mujslcm.
- w1-09: FULL test playbook (see TEST-PLAN.md): IDOR method (2 accounts,
  1 variable), role confusion via EmailFor/LoginFor (server must re-
  derive role), machineKey campaign reference (Feb 2025 Microsoft blog:
  leaked machineKeys -> code injection), disclosure = registrar first,
  CERT-In RVDCP coordination, 90d window. FLAG: projectzero.google URL
  likely fabricated in that report.
- w1-10: 3 Entra tenants mapped (GUIDs + aliases above); DMARC p=none;
  SSPR two-step; SLCM fed unproven; confused-deputy risk: suffix-only
  trust across tenants; SOP PDF "For Internal Use Only" but public
  (real finding).

## Cross-cutting attack leads (for THE team report)

1. YSOD verbose errors (F1) -> customErrors misconfig: with auth creds,
   probe other error triggers for deeper leaks (connection strings,
   paths, machine names).
2. trace.axd 403 (F2): tracing enabled + restricted; Azure-level or
   IIS-level access control to test from allowed networks (team scope).
3. Legacy family teach-in: MAHE WebForms endpoints (.aspx) hint at
   what MUJ's MVC replaced; endpoint names from archives are checking
   leads IF the same app serves both (no evidence yet).
4. Public Django secret + Firebase config: if any of these prototypes
   was ever wired to live services, that is a finding class. Verify
   deployment scope before claiming anything.
5. Fee flows: multiple processors (SLCM, SpaceBasic, NTT DATA, Razorpay)
   = fragmented payment surface; tamper tests belong to auth phase.
6. Email spoofing (p=none) enables targeted "fee pending" phishing
   against students; the INR 487,000 Reddit complaint proves the hook.
7. Third-party app layer (CampusAdda deep links, MUJStella, MTTN) is
   unmanaged attack surface FROM the user side; team can demo the risk
   without touching MUJ assets.
8. Username predictability (name.regnum from public PDFs) + M365
   password = spray risk; that is a disclosure-path finding for MUJ,
   not something we execute.

## w1-08 subdomain-surface (landed, digested)

- MUJ dual portals ARE distinct identity surfaces: mujslcm (98.70.14.50,
  @muj.manipal.edu) vs muj.slcm (20.244.94.89, @jaipur.manipal.edu),
  both IIS10/ASP.NET on AS8075. My live digs confirm both A records
  (report's NODATA rows for these, mujerp, rms are wrong rows; A table
  is correct).
- Dangling CNAMEs: mycampus + testmycampus.jaipur.manipal.edu ->
  edtech366.azurewebsites.net (NXDOMAIN). Subdomain-takeover class:
  report + we recommend REPORT ONLY, no claiming.
- uat.manipal.edu live via Azure Front Door (uat-ci-mahe-ep-….azurefd.net
  -> 150.171.110.195); exam.jaipur.manipal.edu on NIB (59.91.192.229);
  webmail.manipal.edu NIB; api.manipal.edu AWS Node/Express; lms ->
  Brightspace; sis.manipal.edu -> Fee Kart; hms/portal/mujslcm.manipal.edu
  unproven purposes.
- CT history: 25 jaipur names incl npfslcm, lcs, dms, dmsmuj, pms, idp,
  helpdesk (NXDOMAIN today, watch reactivation).

## Open items

- w2x-00 tech-stack redo (launched; w1-02 was too thin)
- Wave 2 fleet: 84 runs in flight, 11 landed at write time (families
  B-G + redo); digest batches after bulk lands
- Verify: projectzero.google URL, Brinztech claim, Scribd student-list
  files, slcm-api.ml/slcm-app.herokuapp.com status, async details
- Re-OCR: First-Year-Students-Profile-Registration-Guide.pdf (DONE
  successfully, see recon/profile-guide.txt)
- Wave 1 coverage: 10/10 reports read to EOF + digested (audit above)

### 6.2.2 Wave 2 and 3 synthesis

Merged 2026-08-25. Pipeline: 98 reports -> 98 digests (each read to EOF,
style-gated, evidence-labelled) -> 3 domain syntheses -> this index.

## Read the three syntheses first

- research/VULN-CLASS-SYNTHESIS.md (16.2K, 35 digests: w2c-* + w2f-* +
  w2x-00): cross-cutting themes (cookie-session auth, M365 intent,
  register-number grammar, header gaps, TLS grade B, DMARC p=none,
  machineKey unproven, Akamai refuted), top leads, contradiction clusters,
  what to test first with credentials.
- research/SURFACE-SYNTHESIS.md (17.2K, 38 digests: w2b-* + w2d-* + w3-*):
  infrastructure map of 23 hosts with cloud attribution, 13 public
  data-exposure classes, 10 leads (DSpace credential exposure, NTT DATA
  Pay URL, mujconnect.in, dmsmuj API TESTING, npfslcm CT), per-host gaps.
- research/CONTEXT-SYNTHESIS.md (15.9K, 26 digests: w2e-* + w2g-*):
  precedent (IISc only verified India-university VDP; CERT-In RVDCP;
  90-day norm), vendor picture (SLCM = ecosystem label, SAP historical
  lead, Keen front end, Salesforce/Deloitte 2026 modernization), public
  footprint (KrishGoel .env.example with populated credentials top,
  vikrant500 cookies.txt, DK10WS route map, SlcmPlus), disclosure path,
  8 knowledge gaps.

Plus wave 1: research/DIGEST-W1.md (10 ultra8x reports, same discipline).

## Pipeline totals

- 110 runs launched, 109 saved (w2c-03 relaunched after server-side fail)
- 109 digests, all EOF-confirmed, zero style violations (programmatic sweep)
- 3 synthesis docs, all EOF/coverage-tabled, style-clean
- 110 replayable briefs in briefs/; launcher + watcher in scripts/

## Open items (tracked)

- Verify KrishGoel + vikrant500 artifacts (do not touch, document only)
- Confirm mujlibrary credential-like title (P0, team check with librarian)
- w2c-20 API routes: the 13-route BOLA test list is the auth-phase core
- Monitor dmsmuj, helpdesk, npfslcm reactivation (cron candidate)
- Phase 2 needs: written team authorization + 2 test accounts

## 6.3 Per-run digests, all 109

One digest per research launch, each read to end of file in the source file. Verbatim.

---

## w1-01-platform-overview.digest

## REPORT (w1-01-platform-overview.md)
## ANSWER SUMMARY
- SLCM is an authenticated student administration portal, not a proven LMS. No public MUJ source calls it a course-content or teaching platform.
- Public root shows username/password login, Student Login, Parent Login, Forgot Password. The form posts to /; Forgot Password exits to passwordreset.microsoftonline.com. This proves Microsoft credential linkage, not SAML/OAuth/Entra SSO.
- Documented onboarding chain: Office 365 activation, mandatory MFA, SLCM profile completion, two signed Student Profile Form copies, in-person document verification.
- Public feature evidence is uneven: attendance route exists and is login-gated; timetable and grades candidate routes return only the login page. Post-login screens are unproven.
- Payments split by purpose: academic fees enter via SLCM with processor undisclosed; hostel/mess goes to SpaceBasic; a mess-fee form exists on NTT DATA Payment Services; certificates use a Razorpay rzp.io link. Canara Bank transfer is the alternative.
- Escalation follows data ownership: DMS/AMS for SLCM/AMS login, IT Infra for Office 365, Admissions for source data, Student Finance for fees, examination helpdesk for exam documents.
- Ecosystem is fragmented: DigiLibrary, SpaceBasic, Online Manipal, MAHE SIS and slcm.manipal.edu are separate services with separate audiences. No core-campus LMS or SLCM mobile app verified.
- Overall confidence 0.86; full authenticated feature inventory only 0.45.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/ | canonical login surface; welcome, sign-in, parent login labels.
- https://mujslcm.jaipur.manipal.edu/Home/Index | indexed route serving the same login surface; no public dashboard proven.
- https://muj.slcm.jaipur.manipal.edu/ | alternate MUJ-branded sign-in hostname; different email domain association.
- https://mujslcm.jaipur.manipal.edu/Student/Academic/AttendanceSummaryForStudent | exact attendance route; login-gated, strongest feature route evidence.
- https://mujslcm.jaipur.manipal.edu/Student/Academic/TimeTableForStudent | candidate timetable route; returns login only.
- https://mujslcm.jaipur.manipal.edu/Student/Academic/GradesForStudent | candidate grades route; returns login only.
- https://passwordreset.microsoftonline.com/ | Forgot Password destination; Microsoft recovery boundary.
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf | username pattern name.registration number, Outlook password, escalation contacts.
- https://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf | officially linked profile guide; text not extractable, existence link-verified only.
- https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf | Office 365 SOP, mandatory MFA, effective June 2025.
- https://jaipur.manipal.edu/pay-fee-online.php | splits academic fees to SLCM and hostel/mess to SpaceBasic.
- https://muj-payservices.nttdatapay.com/DirectPay/MUMessFee | NTT DATA mess-fee form; relationship to current instruction undated.
- https://rzp.io/l/lCB8nGo7Wj | Razorpay certificate/document payment; UPI/Paytm named.
- https://jaipur.manipal.edu/examination.php | exam hub; handbooks, application formats, schedules.
- https://mujlibrary.live/ | DigiLibrary; separate portal accepting both MUJ email domains.

## ACTIONABLE LEADS
- Probe the three named /Student/Academic/* routes for differential auth behavior (redirect, status, body size) across logged-out states before any authenticated test.
- Pull a behavior diff between canonical host and muj.slcm.jaipur.manipal.edu; also /Home/Index vs root.
- Inspect LoginFor/EmailFor hidden fields on the login form: test whether Student vs Parent mode changes the POST target or server behavior.
- Verify the Forgot Password redirect target, tenant branding, generic responses, and any open redirect behavior on recovery.
- Intercept the SLCM academic-fee checkout pre-gateway for amount, order id, student id, return URL fields (authorized testing only); processor is undisclosed so payment endpoint discovery is open.
- Re-fetch and OCR the SLCM Profile Registration Guide PDF; text was not extractable and it may carry endpoint details.
- Fetch the two Annual Fee PDFs (AY 2026-27 main and NRI) from the fee page; check bank instruction detail and form fields.
- Use independent guides (slcm.vercel.app, mujstella.in) as leads for real post-login functions; verify later under authorization.
- Disclosure contacts: registrar@jaipur.manipal.edu, dms@ and ams@ for SLCM ops, it.support@ for identity, student.finance@ for fees, exam.store@ and exam.helpdesk@ for exam documents; help extensions 738/784/481/263.

## FLAGS
- All post-login feature claims are unverified; only the unauthenticated login boundary was observed.
- Reference 26 is a Scribd copy of the grades route claiming 2025 grade sheet content; third-party, unverified, do not trust.
- References 20 and 24 (Annual Fee PDFs) carry garbled mojibake titles ("• �r� JIV/1;�·. ·\*"); URL content unverified.
- Profile-guide PDF existence rests on a link alone; no extractable text found.
- NTT DATA form undated; relation to the current SpaceBasic mess instruction is unclear.
- Alternative hostname email-domain association comes from search results, not first-party pages.
- Absence findings (no LMS, no transport, no staff dashboard) are bounded to public surfaces only.
- Confidence numbers (0.93/0.82/0.45/0.86) are model outputs, not measurements.
- Report labels SLCM administrative, not LMS; do not carry an LMS label forward without first-party proof.

## COVERAGE
- 39357 chars read; verified to EOF (336/336 lines, read_file truncated: false).

---

## w1-02-tech-stack.digest

## REPORT (w1-02-tech-stack.md)
## ANSWER SUMMARY
- MUJ root discloses Microsoft-IIS/10.0, X-AspNet-Version 4.0.30319, X-AspNetMvc-Version 5.3, X-Powered-By ASP.NET: IIS 10 plus ASP.NET MVC 5.3 on .NET Framework 4.x; exact Windows build and patch level not proven.
- MUJ login DOM has a local form posting to / with hidden __RequestVerificationToken, EmailFor, LoginFor, UserName, Password. Parent slcm.manipal.edu exposes ASP.NET_SessionId and no MVC version header: related but not identical stacks.
- jQuery 1.10.2 plus validate and unobtrusive scripts still loaded; validation plugin v1.11.1 from 2013. In CVE-2015-9251, CVE-2019-11358, CVE-2020-11023 ranges; CVE-2020-11022 does not apply (starts at 1.12.0).
- Keen/Metronic theme evidence strong from asset paths (keen/themes/keen/theme/demo1/dist/assets/...); exact version absent from public source.
- SSL Labs: IP 98.70.14.50, grade B, h2 and http/1.1 ALPN, TLS 1.0/1.1/1.2 enabled, BEAST/CBC/3DES warnings, no HSTS.
- SecurityHeaders: MUJ D, parent F. MUJ has X-Frame-Options SAMEORIGIN; both miss HSTS, CSP, X-Content-Type-Options, Referrer-Policy, Permissions-Policy.
- DNS via dns.google resolves MUJ to 98.70.14.50, parent to 104.211.226.160; RIPEstat maps both to Microsoft AS8075; PTR queries return status 3, no hostnames. No Cloudflare or Akamai evidence in this report.
- Backend DB unknown; parent /Home/Index returns a generic IIS 404 with no leak. Do not assume SQL Server.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/ | source of the full header fingerprint (IIS 10.0, ASP.NET 4.0.30319, MVC 5.3).
- https://api.hackertarget.com/httpheaders/?q=https://mujslcm.jaipur.manipal.edu/ | instrument behind the MUJ header claim.
- https://api.hackertarget.com/httpheaders/?q=https://slcm.manipal.edu/ | parent header report; ASP.NET_SessionId, no MVC version header.
- https://api.ssllabs.com/api/v3/analyze?host=mujslcm.jaipur.manipal.edu&fromCache=on&all=done&maxAge=168 | grade B scan; TLS 1.0/1.1/1.2 live, BEAST/CBC/3DES, no HSTS.
- https://securityheaders.com/?q=https%3A%2F%2Fmujslcm.jaipur.manipal.edu%2F&followRedirects=on | D grade; missing HSTS, CSP, nosniff, referrer, permissions.
- https://securityheaders.com/?q=https%3A%2F%2Fslcm.manipal.edu%2F&followRedirects=on | F grade; parent also lacks X-Frame-Options.
- https://mujslcm.jaipur.manipal.edu/Scripts/jquery-1.10.2.min.js | exact old jQuery asset served by the portal.
- https://mujslcm.jaipur.manipal.edu/Scripts/jquery.validate.min.js | jQuery Validation v1.11.1 (2013).
- https://mujslcm.jaipur.manipal.edu/Scripts/jquery.validate.unobtrusive.min.js | unobtrusive validation script.
- https://mujslcm.jaipur.manipal.edu/keen/themes/keen/theme/demo1/dist/assets/css/pages/login/login-v1.css | Keen demo1 login stylesheet; theme evidence.
- https://mujslcm.jaipur.manipal.edu/keen/themes/keen/theme/demo1/dist/assets/js/pages/custom/user/login.js | Keen demo1 login script; theme evidence.
- https://github.com/advisories/GHSA-rmxg-73gg-4p98 | CVE-2015-9251 advisory; jQuery before 3.0.0 cross-domain Ajax condition.
- https://github.com/advisories/GHSA-6c3j-c64m-qhgq | CVE-2019-11358 advisory; jQuery before 3.4.0 deep extension.
- https://github.com/advisories/GHSA-jpcq-cgw6-v4j6 | CVE-2020-11023 advisory; jQuery 1.x and 2.x range.
- https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=A | resolves 98.70.14.50; input to the AS8075 mapping.

## ACTIONABLE LEADS
- Enumerate sibling static assets under /Scripts/, /Content/, /keen/ for versioned bundles; look for a manifest or source map naming the Keen version.
- Recheck headers after a fix cycle: X-Powered-By, X-AspNet-Version, X-AspNetMvc-Version removal; HSTS, CSP, nosniff, Referrer-Policy, Permissions-Policy addition.
- Retest TLS after disabling 1.0/1.1 and 3DES/CBC via SSL Labs; confirm h2 ALPN behavior.
- Treat parent slcm.manipal.edu as a separate test surface: classic ASP.NET session cookie, possible .aspx/WebForms/ViewState endpoints, no MVC header.
- Use the two crt.sh queries referenced (slcm.manipal.edu, mujslcm.jaipur.manipal.edu) for certificate transparency subdomain discovery.
- Review MS15-099, MS14-059, CVE-2015-2526, CVE-2014-4075 references for .NET Framework patch relevance to the disclosed 4.0.30319 runtime.
- Confirm whether any CDN or Akamai layer sits in front (report found none); compare Server header and connection behavior directly.
- Check /elmah.axd, /trace.axd, and error behavior given the verbose header disclosure profile.
- Verify HTTP/2 with a direct curl --http2 test; IIS 10 HTTP/2 works only over TLS.

## FLAGS
- Report says no Cloudflare or Akamai evidence, but the parent task context states the target is Akamai-fronted. Direct contradiction; verify live before trusting either.
- Parent-stack front-end details are not fully citable because only one browser capture was allowed (MUJ only).
- The sentence "The key fingerprint is not just" ends abruptly before References; the report body is truncated mid-thought (generation artifact).
- Exact Keen/Metronic version unverified; ref 29 title says Metronic while body evidence is Keen, a naming mismatch.
- CVE mapping for older .NET bulletins (MS15-099, MS14-059) is listed but never explained in the body.
- Windows build and .NET patch level not proven by headers; IIS 10 only implies Server 2016 or newer.
- SSL Labs result used fromCache=on; single snapshot, grade can drift.
- All CVE claims are range membership only; no sink or reachability proof.

## COVERAGE
- 12321 chars read; verified to EOF (98/98 lines, read_file truncated: false).

---

## w1-03-vendor-family.digest

## REPORT (w1-03-vendor-family.md: Tracing Manipal's SLCM Vendor, Instances, and Shared Risk)

## ANSWER SUMMARY
- Historical product is SAP Student Lifecycle Management (SAP SLcM); two independent Manipal Global employee profiles name SAP SLcM implementation across Manipal Education entities (configuration, migration, development, deployment, support).
- No public evidence names MUJ's current builder or maintainer; group lineage is strong, MUJ-specific ownership is an open item.
- Internal Manipal support is real: a MAHE project manager leads the SLCM support-development team; MIT attendance routes to central slcm.manipal.edu and the SIS page is credited to MAHE Department of Digital and Information Technology.
- MUJ has two near-identical public entrances (mujslcm.jaipur.manipal.edu and muj.slcm.jaipur.manipal.edu); identical branding and matching HTML make them near-certain aliases or sibling deployments.
- MUJ does not share the MAHE classic login template; MAHE classic and Dubai share a classic-template family; Malaysia is a visibly separate framework; MIT is a consumer of the central host, not a separate instance.
- MAHE's 2026 modernization is Salesforce (Agentforce Education, Agentforce, MuleSoft, Tableau) with Deloitte as announced integrator; MUJ is not named in the announcement.
- Public code (REST wrapper, feedback auto-filler, mobile app) shows integration surfaces and third-party credential handling, not proven vulnerabilities; no CVE, SQLi, bypass, or breach was established.
- Student complaints (password rejection, pending fee after payment) are anecdotal reliability issues, not verified vulnerabilities.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/ - primary MUJ target; "WELCOME TO MUJ PORTAL" sign-in.
- https://muj.slcm.jaipur.manipal.edu/ - second MUJ entrance; near-certain alias or coupled deployment of the same front end.
- https://slcm.manipal.edu/ - MAHE classic SLCM; strongest template sibling is Dubai, not MUJ.
- https://slcm.manipaldubai.com/ - Dubai classic SLCM; same confirmation-dialog family as MAHE classic.
- http://salesforce.com/in/news/press-releases/2026/03/26/manipal-university-ai-transformation - MAHE Salesforce modernization announcement; Deloitte integrator; 50+ AI agents over two years; MUJ not named.
- http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf - official MAHE ICT inventory defining SLCM modules (attendance, internal/external marks, results, broadcasts).
- https://sis.manipal.edu/AtdMIT.aspx - MIT attendance page that routes users to central SLCM; evidence of internal estate architecture.
- https://github.com/canaryGrapher/slcmAPI - authenticated REST wrapper for marks, attendance, profile; deprecated after CAPTCHA appeared; documents stable authenticated workflows.
- https://github.com/AddisionS/slcm-feedback-form-filler - MUJ feedback form auto-filler with "All Yes"/"All No"; client-side workflow integrity risk on the MUJ form.
- https://github.com/DK10WS/SLCM_APP - third-party MUJ mobile client replicating login, timetable, grades, attendance with custom auth; credential-handling surface.
- https://www.d2l.com/en-in/why-d2l/customers/manipal-university-jaipur-online - D2L publicly identifies itself as the MUJ Online LMS; distinct from campus SLCM.
- https://linkedin.com/in/adrija-sen-91631110 - Manipal Global profile naming SAP SLcM implementation across Manipal Education entities.
- https://linkedin.com/in/poornima-vishwaradhya-a0b95b22 - second Manipal Global profile naming SAP SLcM configuration scope (admissions, academic structure, records, graduation).
- https://student.manipal.edu.my/ - Malaysia student portal; different portal framework, shared SLCM code not proven.
- https://maheslcm.manipal.edu/login/ - MAHE newer email-oriented login portal; separate from the classic and MUJ families.

## ACTIONABLE LEADS
- Operate the two MUJ hostnames as one risk domain: compare login flow, session cookies, form targets, and feedback endpoints across both aliases; confirm whether they share one auth backend.
- Component-level fingerprint comparison (asset paths, jQuery version, form names, state markers) between slcm.manipal.edu and slcm.manipaldubai.com before transferring any finding; ask for an SBOM comparison.
- Test the MUJ feedback form for server-side abuse controls (rate limits, duplicate-submission detection, response-quality gates); the auto-filler proves client-side controls only.
- Review the public student repos (slcmAPI, SLCM_APP, muj_slcm, SLCM_API) for supported endpoints, session handling patterns, and accidentally committed secrets; they model real credential workflows.
- Check https://slcm.manipal.edu/StudentChangePassword.aspx behavior (old/new/confirmation fields) and session invalidation on password change in the classic family.
- Monitor the Salesforce/Deloitte modernization for MUJ-specific announcements, new login surfaces, and MuleSoft integration endpoints; a second Salesforce SIT URL (maheslcmtech--sit.sandbox.my.site.com) sits in the references untouched.
- Use the named MAHE SLCM project manager profile (https://linkedin.com/in/himanshuupadhyay) as a routing lead for coordinated disclosure; the linkedin.com and reddit URLs are the only human contact points in the report.

## FLAGS
- SAP lineage rests on two self-reported LinkedIn-style profiles; no first-party contract or MUJ statement confirms SAP SLcM on MUJ today.
- The two-MUJ-host equivalence is inferred from static HTML similarity; not owner-confirmed.
- Salesforce announcement URL is unverified in this digest; confirm the press release exists before citing the program details.
- "Crucia, ITL, Jain Group, Manipal Technologies" candidates were searched with no results; absence is not proof of non-involvement, so absence claims are weak-negative.
- Reddit complaints are Tier 3 anecdotal; no root cause or exploitability shown.
- The report cites a Salesforce SIT sandbox login URL but never analyzes it as a surface; reachability and exposure are unverified.
- No CVE, SQL injection, authentication bypass, or breach is established anywhere in the report; any parent-level claim of one would be unsupported.

## COVERAGE (37324 chars as read, read verified to EOF, 286 lines)

---

## w1-04-security-history.digest

## REPORT (w1-04-security-history.md: Manipal SLCM Security History: Evidence, Gaps, and Risk)

## ANSWER SUMMARY
- No confirmed breach of slcm.manipal.edu or mujslcm.jaipur.manipal.edu in the public record reviewed through August 25, 2026; claims that "SLCM was breached" are unsubstantiated.
- The only concrete leak allegation is Brinztech's February 18, 2026 claim of a Manipal Library Portal database release; it names no SLCM system, supplies no forum URL, dataset hash, record count, or MAHE confirmation, and says no student credentials appeared in the data.
- LeakRadar reports 59,820 leaked credentials associated with manipal.edu; the provider's own FAQ says domain-associated records do not mean the organization's infrastructure was breached (stealer logs, Telegram, dark-web, forum sources are common).
- HIBP domain search requires verified domain ownership (unverified returns HTTP 403); DeHashed exposed no target-specific result; both are inconclusive without authorized queries.
- No product-specific CVE for SLCM or the named hosts was found in NVD, CVE.org, Exploit-DB, or VulDB; NVD query URLs fell back to the full corpus (382,361 records) and unrelated Chrome CVEs, so the absence evidence is weak.
- Four Reddit reliability complaints (INR 487,000 fee pending after deduction, correct password rejected, fee module absent for one eligible user, old and new registration numbers rejected) are Tier 3 complaints with no attacker evidence.
- URLScan has seen slcm.manipal.edu twice with no malicious or phishing verdict; mujslcm.jaipur.manipal.edu was "not observed"; no verifiable phishing clone surfaced in PhishTank or OpenPhish.
- Testing boundaries are real: CERT-In Directions 70B require 6-hour incident reporting and 180-day in-India log retention for covered entities; IT Act Sections 43/66 make unauthorized access and extraction criminal (up to 3 years and INR 500,000 fine).

## KEY FACTS
- https://leakradar.io/en/report/manipal.edu - 59,820 domain-associated credential records; provider caveat blocks breach attribution.
- https://www.brinztech.com/breach-alerts/brinztech-alert-database-of-manipal-library-portal-leaked/ - the February 2026 library leak allegation; single unconfirmed secondary source.
- https://libportal.manipal.edu/ - library portal in the alleged leak; designed and maintained by MAHE Department of Digital and Information Technology.
- https://slcm.manipal.edu/ - MAHE SLCM target; URLScan seen twice, no malicious verdict.
- https://mujslcm.jaipur.manipal.edu/ - MUJ target host; not observed in URLScan.
- https://urlscan.io/domain/slcm.manipal.edu - host associated with Microsoft ASN AS8075 and IPv4 104.211.226.160; no phishing verdict.
- https://urlscan.io/domain/mujslcm.jaipur.manipal.edu - "Not observed"; no direct or incoming hits; inconclusive, not a safety rating.
- http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf - official document showing SLCM handles attendance, marks, result publication, broadcasts (high-integrity functions).
- https://haveibeenpwned.com/API/v3 - HIBP domain search is authenticated and plan-dependent; unverified domains get HTTP 403.
- https://dehashed.com/ - no target-specific Manipal result in accessible public material; inconclusive.
- https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf - mandatory 6-hour incident reporting and 180-day log retention for covered entities.
- https://www.indiacode.nic.in/bitstream/123456789/13116/1/it_act_2000_updated.pdf - IT Act Section 43/66 text defining unauthorized access and extraction penalties.
- https://www.cert-in.org.in/RVDCP.jsp - CERT-In responsible disclosure coordination policy; no Manipal-specific safe harbor.
- https://www.manipal.edu/mu/about-us/grievances.html - official grievance route with Ombudsman; no security-incident contact exposed.
- https://nvd.nist.gov/vuln/search/results?form_type=Basic&results_type=overview&query=Manipal&search_type=all&isCpeNameSearch=false - NVD query fell back to the unfiltered corpus; do not cite NVD absence as proof.

## ACTIONABLE LEADS
- Authorized identity investigation: MAHE/MUJ should run HIBP, DeHashed, and LeakRadar source-level queries under verified ownership, deduplicate identities, expire exposed passwords, revoke sessions, and correlate with SLCM sign-in logs.
- Library leak validation: preserve application, API, database, identity-provider, and export logs around February 18, 2026; obtain any sample through counsel or CERT-In, hash it, and compare against libportal schema; search for unusual export activity on that date.
- Origin-exposure check: slcm.manipal.edu sits on Azure IP 104.211.226.160; the target is Akamai-fronted, so test whether the origin answers directly on that IP with a Host header, bypassing WAF.
- Review libportal.manipal.edu for CMS/API endpoints and keys in public JavaScript; it is the only host with a concrete (alleged) incident.
- Set up brand monitoring: certificate transparency, lookalike domains, and fake "fee pending" campaigns; the INR 487,000 complaint shows the social-engineering hook. Preserve any clone as URL, screenshot, headers, timestamp, transaction destination before takedown.
- Disclosure path: use CERT-In RVDCP coordination plus MAHE's grievance route; push MAHE to publish a security.txt and a named security contact.
- Operational fixes implied by complaints: expose transaction IDs and expected posting times in fee workflows; end-to-end identity-lifecycle monitoring for registration changes; step-up auth and dual control for mark, result, and fee changes.
- Reddit threads identify affected populations for outreach; do not use them as test accounts.

## FLAGS
- Brinztech article is Tier 2: publication is verified, event is not. No hash, count, forum URL, or victim confirmation.
- 59,820 is domain-associated, not 59,820 stolen SLCM accounts; the report itself warns against the stronger claim.
- All four Reddit complaints are Tier 3 first-person reports; none demonstrates cyberattack.
- "No CVE found" is a bounded search result; NVD UI failures and dynamic Exploit-DB pages make the negative weak. Do not repeat as "platform has no vulnerabilities".
- URLScan "not observed" for the MUJ host is an absence in one index, not a security rating.
- HIBP absence claims are invalid without verified domain access; an outside researcher cannot certify the domain as clean.
- Display ages ("1y ago", "2mo ago", "3y ago") are approximate; do not quote as exact incident dates.
- PhishTank/OpenPhish checks were search-index based; authenticated or per-URL API lookups may find records the static search missed.

## COVERAGE (40265 chars as read, read verified to EOF, 284 lines)

---

## w1-05-code-leaks.digest

## REPORT (w1-05-code-leaks)

## ANSWER SUMMARY
- 4 GitHub repos plus 1 npm package (yemit) automate SLCM login, attendance, marks, grades, profile and timetable; portal flow must be treated as public knowledge.
- No verified live credential found: no SLCM password, private key, DB connection string or bearer token in reviewed default branches; .env.example holds placeholders only.
- Credential-handling risk is real: wrappers accept username/password as request parameters, and slcmAPI routes support GET and POST, which can leak credentials via logs, history and referrers.
- Two secret-bearing configs are public: Firebase google-services.json (DK10WS/SLCM_APP) and a Django SECRET_KEY with DEBUG=True (Anushkakumar10/muj_slcm); operational impact untested.
- Flutter client (SLCM SWITCH) shows cookie + request-verification + parent OTP + session persistence; no JWT evidence exists in any reviewed artifact.
- Cert Spotter CT data yields 103 manipal.edu hostnames, 11 Jaipur-scoped (incl muj.slcm.jaipur.manipal.edu, mujerp, mujone, rms) and 7 with dev/uat/preprod labels.
- LeakIX service index lists 117 records incl dev-* names; the leak-scoped query hit a login wall, so no usable leak record was confirmed.
- Verdict: material public technical exposure exists, but no verified live SLCM credential compromise was established.

## KEY FACTS
- https://github.com/sankalp2004/SLCM-is-Dumb - end-to-end Selenium/OCR login and CGPA automation; exposes portal flow and CAPTCHA handling.
- https://github.com/sankalp2004/SLCM-is-Dumb/blob/master/config.py - names exact routes loginForm.aspx and GradeSheet.aspx.
- https://github.com/canaryGrapher/slcmAPI - archived Express/Puppeteer API that receives SLCM credentials; archived Oct 17, 2024.
- https://github.com/canaryGrapher/slcmAPI/blob/master/routes/getattendance.js - GET and POST handlers accept username/password, the core unsafe pattern.
- https://github.com/canaryGrapher/slcmAPI/blob/master/routes/getmarks.js - credentials in a GET-compatible handler with semester input.
- https://github.com/tejaskash/slcm-api - Flask wrapper; POST /api/v1/get takes credentials plus ATTENDANCE, MARKS or ALL.
- https://github.com/DK10WS/SLCM_APP - Flutter SLCM SWITCH client with student/parent login, OTP path and session handling.
- https://github.com/DK10WS/SLCM_APP/blob/main/android/app/google-services.json - public Firebase client configuration; rules, not key secrecy, decide risk.
- https://github.com/DK10WS/SLCM_APP/blob/main/lib/pages/login.dart - shows request-verification material, cookie combining and parent OTP flow.
- https://github.com/DK10WS/SLCM_APP/blob/main/lib/session_manager.dart - nullable session-cookie value persisted for later use.
- https://github.com/Anushkakumar10/muj_slcm/blob/main/muj_slcm/muj_slcm/settings.py - public Django SECRET_KEY and DEBUG=True; value redacted in report.
- https://github.com/slcm-manipal/slcm-manipal.github.io/blob/master/index.html - authenticated-looking snapshot with ASP.NET state fields and personal or academic content.
- https://www.npmjs.com/package/yemit - CasperJS attendance tool targeting slcm.manipal.edu, published about 8 years before the indexed snapshot.
- https://api.certspotter.com/v1/issuances?domain=manipal.edu&include_subdomains=true&expand=dns_names - 103 distinct CT hostnames including dev/uat/preprod labels.
- https://leakix.net/search?scope=service&q=manipal.edu - 117 indexed service records incl dev-api, dev-techtatva and dev-register-techtatva names.

## ACTIONABLE LEADS
- Search repo history and forks of the four projects for removed .env files or real secret commits (medium confidence).
- Check whether muj_slcm Django prototype was ever deployed; rotate SECRET_KEY if so, disable DEBUG, strip secrets from history.
- Contact owners of slcm-manipal.github.io to remove or redact the snapshot's personal and academic content.
- Map CT names to owners, focusing on dev-api, dev-crm, dev-payment, content-uat, content-preprod, uat, preprod.
- Re-query LeakIX leak scope via API/auth; validate any record at record level before calling it a breach.
- Test the Firebase project's Realtime Database, Storage, Auth and App Check rules internally for the google-services.json project.
- Audit cookie flags, CSRF enforcement, OTP rate limits and session rotation on mujslcm.jaipur.manipal.edu using institution-controlled accounts.
- Verify whether historical deployments slcm-api.ml and slcm-app.herokuapp.com are still live; treat them as credential-phishing vectors.
- Monitor npm registry, GitHub and paste sites for new SLCM credential material; keep the negative findings re-checkable.
- If a working credential is ever found, report it privately to MUJ IT and the platform; never reproduce it.

## FLAGS
- crt.sh direct queries returned 404 in this environment; the 103-name count rests on Cert Spotter alone (single source).
- GitHub candidate madhav-manchanda/SlcmAndLms-aggregator returned 404 and was excluded from the inventory.
- Postman workspace overview showed no requests, auth or variables; scope unverified, not tied to SLCM.
- yemit is roughly 8 years old; its selectors and host assumptions may be stale.
- LeakIX 117 service records are an index, not breach evidence; dev-* names are inventory leads only.
- Firebase client API key is an identifier; its presence proves no unauthorized database access.
- GitLab, Pastebin, gist and RaonData negatives are moderate confidence; unindexed or deleted pastes cannot be ruled out.
- Behaviors quoted from old source code may not match current portal markup or auth flow.

## COVERAGE
Source read in full: research/w1-05-code-leaks.md. File char count as read: 47931 (330 lines). Read pagination reached line 330 of 330; EOF confirmed (truncated: false).

---

## w1-06-student-data-osint.digest

## REPORT (w1-06-student-data-osint)

## ANSWER SUMMARY
- Exposure is real but uneven: the strongest verified student-level data sits in official PhD PDFs under jaipur.manipal.edu/img/pdf/, not in SLCM itself.
- The PhD awardee compilation is a ~500-scale dataset (visible serial reaches 502): names, faculty, department, registration number, thesis title, supervisors, award and viva dates.
- Applicant emails appear in official shortlist PDFs (July 2026 and July 2025), joined to application number, department, candidature and exemption status.
- No verified undergrad marks list, attendance roster, exam seating, hostel room roster or fee balances; the hostel PDF is guidance and the fee notice is non-personal.
- The 24JTEECS001 format is unsubstantiated; the official SLCM FAQ shows a numeric registration number, contradicting the alphanumeric claim.
- All open-source scrapers require credentials; no evidence of a no-auth university API, ASMX/WCF service or /api/ route.
- Routes are indexed (mujslcm /Home/Index, /Student) but show no pre-login records; web archives add structure only.
- Verdict: moderate-high public-data exposure via documents, with no proven live SLCM breach.

## KEY FACTS
- https://jaipur.manipal.edu/img/pdf/List-of-PhD-Awarded-%28till-2025%29.pdf - 500-scale awardee dataset joining identity, reg numbers, theses, supervisors and dates.
- https://jaipur.manipal.edu/img/pdf/List-of-Candidates-Eligible-for-PhD-Interview-%28July-2026%29.pdf - highest-risk PDF: name, email, application number, department, candidature and exemption status together.
- https://jaipur.manipal.edu/img/pdf/Shortlisted-Candidates-PhD-Exam-July-18072025.pdf - July 2025 shortlist with application number, roll/name and registered email.
- https://jaipur.manipal.edu/img/pdf/PhD-ADMISSIONS-JAN-2026-INTERVIEW-RESULT-LIST-OF-SELECTED-CANDIDATES.pdf - Jan 2026 selected candidates with names and application/registration numbers.
- https://jaipur.manipal.edu/img/pdf/PhD-Interview-Results-July-2026.pdf - July 2026 selected candidates with application number, department and candidature.
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - official SLCM FAQ: portal URL, username convention, helpline; contradicts the 24JTEECS001 specimen.
- https://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf - onboarding guide describing SLCM purpose and profile registration.
- https://jaipur.manipal.edu/research-phd.php - discovery hub linking the whole PhD result and shortlist PDF series.
- https://www.scribd.com/document/881889937/Eligible-Students-MUJ-1 - third-party claim of a multi-field MUJ student list; provenance unverified.
- https://www.scribd.com/document/792426451/Book4 - unverified Scribd candidate file; field categories not established.
- https://web.archive.org/cdx/search/cdx?url=mujslcm.jaipur.manipal.edu/*&output=json&fl=timestamp,original,statuscode,mimetype&filter=statuscode:200&collapse=urlkey - archive captures of / and /Home/Index from 2025-2026.
- https://web.archive.org/cdx/search/cdx?url=slcm.manipal.edu/*&output=json&fl=timestamp,original,statuscode,mimetype&filter=statuscode:200&collapse=urlkey - legacy routes incl loginForm.aspx, Print.aspx, WebForm1.aspx and password-change pages.
- https://jaipur.manipal.edu/contact-university.php - role-based contact directory across academic, exam, hostel, finance, HR, IT, library, registrar, welfare and webmaster.
- https://mujslcm.jaipur.manipal.edu/Home/Index - indexed public login landing page; no pre-login student record in extracted body.
- https://www.manipal.edu/content/dam/manipal/mu/hostel/pdf/Hostel%20Allotment.pdf - hostel allotment guidance only; no roster, room assignments or student list.

## ACTIONABLE LEADS
- Pull all PhD result, shortlist and awardee PDFs and inventory fields internally; confirm which contain emails and internal identifiers.
- Validate the Scribd Eligible-Students-MUJ-1 file internally for authenticity and provenance; request removal if real; do not amplify it.
- Replace result PDFs with masked application references, add noindex and request search cache removal after replacement.
- Probe /img/pdf/, /uploads/, /documents/ and /files/ for directory indexing; no Index of listing verified yet.
- Run an authorized object-level authorization test with synthetic accounts covering student, parent, staff and admin roles.
- Include retired routes (Print.aspx, WebForm1.aspx, StudentChangePassword.aspx, ParentChangePassword.aspx) in decommission and asset reviews.
- Review retention policy for the awardee list with registrar and research office; push for removal of registration numbers.
- Verify the @muj.manipal.edu email convention claim against official documentation before relying on it.
- Monitor for re-uploads of the same PDF data on third-party hosts; set up alerting on new scribd/paste hits.
- If a default or working password is discovered, report it privately to MUJ; never reproduce it in public.

## FLAGS
- 24JTEECS001 decomposition (year, campus, branch, sequence) is unverified; the official FAQ numeric example contradicts it.
- Scribd documents: authenticity, date and source chain unknown; titles can mislabel; both are leads, not confirmed spills.
- The "502" figure is the visible serial number in the awardee PDF, not a stated row count.
- @muj.manipal.edu is a medium-confidence inference from portal branding, not a documented email standard.
- Negative findings (marks lists, attendance rosters, directory indexes, phone lists) are moderate confidence only.
- Faculty profile phone links appear to be generic admissions numbers, not personal faculty numbers.
- Archive inventory proves route existence only; auth state and function at capture time are unknown.
- muj.slcm.jaipur.manipal.edu returned no archived captures in the reviewed CDX result.

## COVERAGE
Source read in full: research/w1-06-student-data-osint.md. File char count as read: 43659 (326 lines). Read pagination reached line 326 of 326; EOF confirmed (truncated: false).

---

## w1-07-mobile-app-apis.digest

## REPORT (w1-07-mobile-app-apis)

## ANSWER SUMMARY
- No verified first-party "MUJ" or "Manipal App" store listing exists; treat publisher, package ID and privacy policy as the trust anchor, not the app title.
- The only verified first-party surface is the web portal mujslcm.jaipur.manipal.edu with institutional, parent and student login choices.
- No official Swagger/OpenAPI spec, no verified MUJ Postman collection, and no evidence for a mujslcm /api/... pattern; that pattern is not documented.
- Legacy MAHE SLCM is ASP.NET Web Forms: txtUserid, txtpassword, txtCaptcha, __VIEWSTATE, __EVENTVALIDATION and session cookies; not JWT or OAuth.
- Community wrappers (slcm-api.ml, slcm-app.herokuapp.com, canaryGrapher, tejaskash) are credential-handling scrapers, not API documentation; historic deployments should be treated as untrusted.
- CampusAdda (com.app.campusadda, App ID 6465745096) is the clearest native surface: Razorpay/wallet payments, OTP delivery, and valid AASA and assetlinks files.
- Push capability is verified for MTTN and mentioned by CampusAdda, but Firebase and OneSignal attribution is unverified.
- MUJ fees: SLCM portal for existing students, SpaceBasic for hostel/mess; BillDesk, CCAvenue, Razorpay and SBI ePay are not attributable to MUJ tuition.

## KEY FACTS
- https://play.google.com/store/apps/details?id=com.app.campusadda&hl=en_US - CampusAdda Android, updated Apr 3 2026, 10K+ downloads, Razorpay and wallet advertised.
- https://campus-adda.com/.well-known/apple-app-site-association - verified AASA binding U7WSBR3A3J.com.app.campusadda to restaurant, product, order, campaign, event and carpool paths.
- https://campus-adda.com/.well-known/assetlinks.json - Android App Links delegation to com.app.campusadda with two signing-certificate SHA-256 fingerprints.
- https://apps.apple.com/us/app/campusadda/id6465745096 - CampusAdda iOS v3.2.2; purchases, location, contacts, identifiers and diagnostics linked to user.
- https://mujslcm.jaipur.manipal.edu/ - only verified first-party MUJ surface; public login choices for institutional, parent and student roles.
- https://play.google.com/store/apps/details?id=com.yourcompany.mujstellaapp&hl=en_US - MUJStella Android, independent, 1K+ downloads, timetable, attendance and SLCM tracker.
- https://mujstella.in/mujslcm - installable PWA, explicitly not affiliated with MUJ, sign-in required.
- https://apps.apple.com/in/app/manipal-university-jaipur-gym/id6757078406 - MUJ-branded gym app published by Gayatri Software Services; gym credentials, plans, measurements, diet data.
- https://play.google.com/store/apps/details?id=com.mttn.android&hl=en_IN - MTTN Android, 10K+ downloads, SLCM attendance and grade features, push and low-attendance alerts.
- https://slcm.manipal.edu/loginForm.aspx - legacy MAHE login page referenced by community code; not an MUJ Jaipur surface.
- https://raw.githubusercontent.com/nikeplusdash/SLCM-api/master/SLCM.py - shows form fields txtUserid, txtpassword, txtCaptcha and ASP.NET hidden state in a persistent session.
- https://raw.githubusercontent.com/canaryGrapher/slcmAPI/master/routes/validateuser.js - credential-validation routine returning credentialsValid true/false; an avoidable oracle pattern.
- https://www.postman.com/harshalsangole/manipal-api-collection/overview - public workspace with no visible requests, auth or SLCM relationship.
- https://jaipur.manipal.edu/pay-fee-online.php - official fee page: existing students to SLCM portal, hostel/mess to SpaceBasic; no gateway named for tuition.
- https://apkpure.com/slcm-manipal/com.wSLcMManipal_10192522 - archived 2020 third-party wrapper APK; a tier-3 block target for credential safety.

## ACTIONABLE LEADS
- Build a three-tier allow-list: verified MUJ domains; vendor/community apps with verified IDs, publishers and policies; archived APKs and credential wrappers to block.
- Test CampusAdda deep links (carpool share token, order, campaign, event) for open redirects or payment-state tampering before trusting links.
- Enumerate campus-adda.com routes surfaced by the app-link files for any public API or misconfigured endpoints.
- Confirm the current status of slcm-api.ml and slcm-app.herokuapp.com; treat as defunct until proven otherwise and warn students off them.
- Ask CampusAdda, MUJStella and MTTN vendors for attestation or SBOM on Firebase/OneSignal, analytics and payment SDKs.
- Review the SpaceBasic redirect boundary on the MUJ fee page; check for link-injection or lookalike domains.
- Ask MUJ Online/D2L about the Brightspace API surface and the Microsoft-account auth callback failure described in App Store reviews.
- Check alternate stores (Huawei AppGallery, Galaxy Store) for MUJ-branded apps under vendor publishers.
- Report credential-forwarding wrappers to MUJ IT as phishing vectors; consider takedown requests where they solicit portal credentials.
- Never submit credentials to archived APKs such as com.wSLcMManipal_10192522 or any historic wrapper.

## FLAGS
- CampusAdda iOS publisher (Sujit Sonune) differs from Android publisher (Campusadda Technologies Private Limited); resolve before trusting the pair.
- MUJStella package id com.yourcompany.mujstellaapp is a template-style namespace suggesting low maturity; verify developer and build provenance.
- Play "no data collected" claims for MUJStella and MTTN sit uneasily beside SLCM-linked attendance and grade features; unresolved.
- CampusAdda Play listing says data is not encrypted while its policy claims reasonable safeguards; the store declaration should dominate risk assessment.
- Reddit posts about Outlook password changes and Microsoft Authenticator are anecdotes, not proof of Entra OAuth, OIDC or token issuance.
- The Brightspace App Store review is user feedback, not vendor documentation.
- MAHE Dubai-SLCM (UNIKUL) and D2L Brightspace are separate ecosystems; do not conflate them with MUJ Jaipur.
- No .asmx/.svc endpoint and no verified /api/ base was found; both absences are search-based and moderate confidence only.

## COVERAGE
Source read in full: research/w1-07-mobile-app-apis.md. File char count as read: 37483 (244 lines). Read pagination reached line 244 of 244; EOF confirmed (truncated: false).

---

## w1-08-subdomain-surface.digest

## REPORT (w1-08-subdomain-surface.md)
Passive public attack-surface mapping of jaipur.manipal.edu + manipal.edu subdomains, dated 2026-08-25. Sources: crt.sh CT, dns.google, Wayback, Shodan public pages, ipinfo.io, fetched public pages. No active probing, no auth, no port scans. 362 lines, 41643 chars, read to EOF.

## ANSWER SUMMARY
- Two live MUJ SLCM generations: `mujslcm.jaipur.manipal.edu` (A 98.70.14.50, IIS 10/ASP.NET MVC 5.3, `@muj.manipal.edu`, separate parent/student login) and `muj.slcm.jaipur.manipal.edu` (A 20.244.94.89, IIS 10, ASP.NET 4.0.30319, jQuery 1.10.2, `@jaipur.manipal.edu`). Both sit in Microsoft AS8075 space; report treats them as distinct production identity surfaces.
- Shared MAHE core: `slcm.manipal.edu` (A 104.211.226.160, IIS 10/ASP.NET, Microsoft AS8075) and `sis.manipal.edu` (A 218.248.47.25, IIS 10, National Internet Backbone AS9829, fee payment routed to Fee Kart).
- Hosting estate is split, not one stack: Azure DNS at parent apex, AWS EC2 ap-south-1 for `jaipur.manipal.edu` apex (3.108.105.201) and `api.manipal.edu` (43.205.223.7, nginx 1.18.0/Node.js/Express), D2L Brightspace for `lms.manipal.edu`, Microsoft 365 mail on both apexes, Google Sites for `library.jaipur.manipal.edu`.
- Jaipur CT history holds 25 unique names including non-obvious `mujerp`, `mujone`, `npfslcm`, `rms`, `lcs`, `helpdesk`, `idp`, `dms`, `pms`, `mycampus`, `testmycampus`; CT is treated strictly as historical inventory, not proof of live DNS.
- Dictionary guesses under jaipur (`lms`, `erp`, `portal`, `mail`, `api`, `dev`, `test`, `staging`) are mostly NXDOMAIN; exceptions: `exam` (59.91.192.229, NIB) and `uat` (103.139.159.141, Seans Media).
- `mycampus.jaipur.manipal.edu` and `testmycampus.jaipur.manipal.edu` keep CNAMEs to `edtech366.azurewebsites.net` whose terminal target is NXDOMAIN (dangling aliases).
- `uat.manipal.edu` is a labeled Azure Front Door route via `uat-ci-mahe-ep-bzgfhcehh0fvhafs.a01.azurefd.net` to 150.171.110.195.
- Group-wide `*.manipal.edu` CT completeness not achieved: crt.sh truncates the broad search to a random subset.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/ - primary target; A 98.70.14.50; parent/student login, Forgot Password, `@muj.manipal.edu`.
- https://muj.slcm.jaipur.manipal.edu/ - second live MUJ portal; A 20.244.94.89; MUJ Portal, Sign In, `@jaipur.manipal.edu`.
- https://slcm.manipal.edu/ - shared MAHE SLcM; A 104.211.226.160; IIS 10/ASP.NET, Microsoft AS8075; earliest Wayback capture 2020-11-18.
- https://sis.manipal.edu/studlogin.aspx - SIS for students/parents; A 218.248.47.25; AS9829; points fee payment to Fee Kart.
- https://api.manipal.edu/ - AWS EC2 43.205.223.7; nginx 1.18.0, Node.js, Express; root emits opaque JSON `data` field.
- https://lms.manipal.edu/ - D2L Brightspace via CNAME `learner-mahe.onlinemanipal.com` -> `manipalonline.brightspace.com`; A 15.134.178.12, 13.55.178.159.
- https://uat.manipal.edu/ - labeled UAT; CNAME via `uat-ci-mahe-ep-bzgfhcehh0fvhafs.a01.azurefd.net` to 150.171.110.195.
- https://uat.jaipur.manipal.edu/ - A 103.139.159.141 in Seans Media space; no claim on app state.
- https://exam.jaipur.manipal.edu/ - A 59.91.192.229 on National Internet Backbone space; exam-labeled.
- https://mycampus.jaipur.manipal.edu/ and https://testmycampus.jaipur.manipal.edu/ - CNAMEs to `edtech366.azurewebsites.net`; terminal target NXDOMAIN.
- https://dev.manipal.edu/ - A 4.247.242.9 (Microsoft space) but serves ordinary MAHE site with Apply Now, not a dev console.
- manipal.edu apex - Azure DNS NS `ns1-36.azure-dns.com/net/org/info`; A 18.160.46.89/123/45/127; MX `0 manipal-edu.mail.protection.outlook.com`.
- jaipur.manipal.edu apex - A 3.108.105.201 (AWS EC2 ap-south-1); MX `0 jaipur-manipal-edu.mail.protection.outlook.com`; no child NS delegation.
- https://webmail.jaipur.manipal.edu/ - CNAME chain into Microsoft 365/Outlook; high-confidence M365 webmail alias.
- https://webmail.manipal.edu/ - A 218.248.47.16 on NIB space; webmail-labeled endpoint, behavior untested.

## ACTIONABLE LEADS
- `mujerp.jaipur.manipal.edu` - ERP-labeled, CT starts 2025-04-11; report claims current A 20.244.0.229 but that is contradicted elsewhere (see FLAGS); verify DNS directly.
- `rms.jaipur.manipal.edu` - acronym host, claimed A 202.131.155.153 (also contradicted); `lcs`, `npfslcm`, `dms`, `dmsmuj`, `pms`, `idp` are NODATA/legacy; monitor for reactivation.
- `helpdesk.jaipur.manipal.edu` - fresh CT 2026-01-08 but NXDOMAIN today; watch for activation.
- https://hms.manipal.edu/ - A 20.44.49.205 Microsoft space; acronym meaning unstated, worth identifying.
- https://portal.manipal.edu/ - A 45.112.150.155; generic name, function unproven.
- `mujslcm.manipal.edu` (parent level, no jaipur) - A 202.131.155.151; purpose unproven, likely MUJ by label only.
- `exam.jaipur.manipal.edu` - live NIB-hosted exam endpoint; scope its content.
- `uat.manipal.edu` + `uat.jaipur.manipal.edu` - non-prod labels, both live; authorized testing only.
- `admissions.jaipur.manipal.edu` and `apply.jaipur.manipal.edu` - CT-validated names, NODATA now; old admission surfaces.
- `mycampus`/`testmycampus` dangling CNAMEs - confirm the Azure resource is gone before any action; report explicitly does not recommend claiming the target.

## FLAGS
- Internal contradiction: `mujslcm.jaipur.manipal.edu` (ref 85) and `muj.slcm.jaipur.manipal.edu` (ref 90) are listed with A records in the naming matrix and inventory, but as NOERROR/NODATA in the CT-to-DNS state table citing the same refs. Both cannot be right; re-verify with dns.google before trusting either table.
- Same pattern for `mujerp` (A 20.244.0.229 vs NODATA, both ref 96) and `rms` (A 202.131.155.153 vs NODATA, both ref 97).
- Report lists a fetched page for https://mycampus.jaipur.manipal.edu/ (ref 9, titled "Manipal University Jaipur") while also reporting its CNAME terminal target is NXDOMAIN; both cannot hold on the same day from the same resolver.
- All evidence is third-party and dated (Shodan observations 2026-08-18/22/23, DNS 2026-08-25); unverified until live re-check. Report self-assigns 0.35 confidence to acronym host purposes and 0.20 to group CT completeness.
- Wayback "earliest capture" (2020-11-18 slcm, 2025-05-27 mujslcm) is not a launch date; the report itself rejects launch-date claims.
- NOERROR/NODATA means only no A/CNAME answer; hosts may carry other record types. CT entries never prove ownership or current DNS.
- crt.sh `*.manipal.edu` search is truncated to a random subset; this report contains no exhaustive group list, so do not treat any group inventory as complete.
- Odd filler: report answers a "cot_explicit" chain-of-thought demand; template-reuse or prompt-injection residue, irrelevant to findings.
- No Censys evidence exists; report says public Censys pages yielded nothing and it did not manufacture data. Shodan banner versions may be stale or proxied.

## COVERAGE
- File read to EOF: 362 lines, 41643 chars (file_size 41643), truncated: false. Confirmed EOF at line 362 (final reference, ref 107).

---

## w1-09-attack-surface-checklist.digest

## REPORT (w1-09-attack-surface-checklist.md)
## ANSWER SUMMARY
- Verdict: GO only with signed university authorization and synthetic test identities; otherwise NO-GO. Sections 43 and 66 of India's IT Act make permission the controlling gate.
- Priority order: horizontal/vertical authorization and IDOR first, payment and record business logic second, session/CSRF and identity controls third, diagnostics and config review fourth, headers/TLS baseline last.
- IDOR method: two accounts, two owned objects, one changed variable, one request, stop on first proof; never guess production IDs.
- Session: ASP.NET_SessionId must renew after login and role change; __RequestVerificationToken variants (missing, mutated, cross-session, expired) go only against a no-op action.
- Legacy ASP.NET review over exploitation: customErrors, compilation debug=false, elmah.axd, trace.axd, WebDAV, 8.3 short names, .aspx/.asmx/.svc inventory, machineKey provenance, ViewState MAC; never forge cookies or deserialization payloads.
- Role confusion: EmailFor/LoginFor are attacker-controlled hints; the server must re-derive role from the identity store.
- Disclosure: registrar@jaipur.manipal.edu (Dr Amit Soni) first, CERT-In RVDCP for coordination, 90-day window as practice only. No dedicated MUJ PSIRT found (confidence 0.74 on that route).
- jQuery 1.10.2 falls in CVE-2015-9251 and CVE-2019-11358 ranges; range membership is a finding, reachability must be proven separately.

## KEY FACTS
- https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References | IDOR definition and two-user method basis.
- https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/03-Identity_Management_Testing/04-Testing_for_Account_Enumeration_and_Guessable_User_Account | enumeration needs material response difference, not client markup.
- https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html | session renewal after privilege change; cookie flag requirements.
- https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html | header removal and hardening baselines.
- https://www.indiacode.nic.in/bitstream/123456789/13116/1/it_act_2000_updated.pdf | IT Act sections 43, 66, 66C, 66D quoted for the authorization gate.
- https://www.jaipur.manipal.edu/administration-registrar.php | Dr Amit Soni, Registrar; registrar@jaipur.manipal.edu; +91 141-3999100 ext 102; disclosure first contact.
- https://www.cert-in.org.in/RVDCP.jsp | CERT-In responsible vulnerability disclosure and coordination policy.
- https://projectzero.google/vulnerability-disclosure-policy.html | Project Zero 90-day policy cited; see FLAGS, URL looks malformed.
- https://nvd.nist.gov/vuln/detail/CVE-2015-9251 | jQuery XSS before 3.0.0, cross-domain Ajax condition.
- https://nvd.nist.gov/vuln/detail/CVE-2019-11358 | jQuery deep-extension XSS before 3.4.0.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.configuration.customerrorsmode?view=netframework-4.8.1 | Off/On/RemoteOnly error mode semantics.
- https://elmah.github.io/a/securing-error-log-pages/ | ELMAH remote access default-disabled; secure via authorization when enabled.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.security.machinekey?view=netframework-4.8.1 | machineKey algorithms shared with Forms Auth and ViewState.
- https://www.microsoft.com/en-us/security/blog/2025/02/06/code-injection-attacks-using-publicly-disclosed-asp-net-machine-keys | real-world leaked machineKey code injection campaign.
- https://owasp.org/www-project-top-10-for-business-logic-abuse | business logic abuse framing for fee and record tests.

## ACTIONABLE LEADS
- Route matrix on approved assets: /Home/Index, /Student/*, /Staff/*, /Account/*; one GET each as logged out, Student A, Student B, Staff A; record status, size, protected-data presence.
- IDOR replay on document paths with synthetic canaries (TA-001 / TB-001 pattern); HEAD first, small Range GET if needed; stop on first cross-user hit.
- Hidden field test: same credentials with LoginFor=Student vs Staff; check navigation and API authorization results, not just login success.
- Fee flow: capture pre-redirect request, change one field (amount, order id, student id), send only to the pre-authorization step; never complete 3DS or replay callbacks.
- Reset flow: verify target host, tenant branding, generic responses, token lifetime and single-use, rate controls; one test account only.
- Diagnostic probes: one GET each to /elmah.axd and /trace.axd; one malformed param on an approved field; one OPTIONS for WebDAV; config review for customErrors, debug, machineKey provenance.
- Lockout: sacrificial account only, at exercise end, known threshold, stop at first throttle; never spread attempts across usernames.
- Disclosure sequence: encrypted report to registrar@jaipur.manipal.edu with engagement ID; CERT-In RVDCP only for coordination or a real incident; 90-day timeline with day-2 ack target; joint publication timing.

## FLAGS
- Ref 7 URL https://projectzero.google/vulnerability-disclosure-policy.html uses a domain that likely does not exist; the real Project Zero policy is hosted elsewhere. Treat as unverified, possibly fabricated link.
- The report states no live requests were made; route names, hidden fields, jQuery version, reset destination, and stack are hypotheses from the brief, not verified observations.
- Ref 6 uses http://cert-in.org.in/SecurityIncident.jsp while the body cites https://www.cert-in.org.in/; two different CERT-In URLs, content unverified.
- Refs 29 and 31 both point at NIST SP 800-115 via different URLs; duplicate oddity, content unverified.
- IT Act quotes are a research summary, not legal advice; verify language against the PDF before relying on it.
- "5 to 10 attempts typical lockout threshold" is a generic OWASP note, not a portal measurement.
- Confidence splits (0.89 methodology, 0.74 route) are model outputs.
- The report leans on the brief's claim that the portal is ASP.NET MVC 5.3 / .NET 4.x / IIS 10; w1-02 headers corroborate that stack.

## COVERAGE
- 46547 chars read; verified to EOF (295/295 lines, read_file truncated: false).

---

## w1-10-sso-entra.digest

## REPORT (w1-10-sso-entra.md: MUJ Identity Federation: Verified Surface and Defensible Inferences)

## ANSWER SUMMARY
- Microsoft OpenID metadata resolves three separate Entra tenants: jaipur.manipal.edu (7d0726e8-bf4b-4ac1-99f1-010fb11f1d3f, alias mujcampus.onmicrosoft.com), muj.manipal.edu (27282fdd-4c0b-4dfb-ba91-228cd83fdf71, alias mujmanipal.onmicrosoft.com), and the manipal.edu root (29bebd42-f1ff-4c3d-9688-067e3460dc1f, alias learnermanipal.onmicrosoft.com).
- Both MUJ namespaces return NameSpaceType=Managed with brand "Manipal University Jaipur" and no external AuthURL; evidence favors Microsoft cloud authentication and does not support a current AD FS claim.
- SLCM federation is unproven: both indexed SLCM pages show a local form submission plus a passwordreset.microsoftonline.com link, with no public OIDC, SAML, or WS-Fed authorization redirect.
- MUJ's publicly reachable June 2025 Office 365 SOP (IT-SOP-O365-001, version 1.0) documents mandatory MFA setup before Office 365 use and a two-step SSPR flow; it is a strong enrollment signal, not proof of Conditional Access enforcement on every login.
- Mail is verified Microsoft 365: Exchange Online Protection MX for all three domains, SPF ending in -all, Microsoft DKIM selector CNAMEs published; DMARC is monitoring-only (p=none explicit for jaipur and manipal.edu; muj.manipal.edu NXDOMAIN inherits the root p=none per RFC 7489).
- The three domains map to different tenant GUIDs, so email-suffix-based authorization is unsafe; exact issuer, tid, and audience validation is the highest-value control.
- Enumeration, password spraying, and token tampering are not authorized by public metadata; the report's safe path is synthetic accounts, staging, and admin-side log and policy review.

## KEY FACTS
- https://login.microsoftonline.com/jaipur.manipal.edu/.well-known/openid-configuration - resolves tenant 7d0726e8-bf4b-4ac1-99f1-010fb11f1d3f with sts.windows.net issuer.
- https://login.microsoftonline.com/muj.manipal.edu/.well-known/openid-configuration - resolves second MUJ tenant 27282fdd-4c0b-4dfb-ba91-228cd83fdf71, distinct from the first.
- https://login.microsoftonline.com/manipal.edu/.well-known/openid-configuration - root domain tenant 29bebd42-f1ff-4c3d-9688-067e3460dc1f, brand Manipal Academy of Higher Education.
- https://login.microsoftonline.com/mujcampus.onmicrosoft.com/.well-known/openid-configuration - alias returns the same GUID as jaipur.manipal.edu, confirming the tenant mapping.
- https://login.microsoftonline.com/mujmanipal.onmicrosoft.com/.well-known/openid-configuration - alias returns the same GUID as muj.manipal.edu.
- https://login.microsoftonline.com/getuserrealm.srf?login=probe@jaipur.manipal.edu&xml=1 - realm response: Managed, brand Manipal University Jaipur, no external AuthURL.
- https://login.microsoftonline.com/getuserrealm.srf?login=probe@muj.manipal.edu&xml=1 - same Managed classification for the second namespace.
- https://login.microsoftonline.com/jaipur.manipal.edu/federationmetadata/2007-06/federationmetadata.xml - WS-Fed metadata is Microsoft Entra STS output, not proof of an MUJ AD FS farm.
- https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf - MUJ Office 365 SOP; documents mandatory MFA registration and two-step SSPR; marked "For Internal Use Only" yet public.
- https://dns.google/resolve?name=jaipur.manipal.edu&type=MX - MX target jaipur-manipal-edu.mail.protection.outlook.com, verifying Exchange Online Protection.
- https://dns.google/resolve?name=jaipur.manipal.edu&type=TXT - SPF includes spf.protection.outlook.com and a._spf.brightspace.com, hard-fail -all.
- https://dns.google/resolve?name=_dmarc.jaipur.manipal.edu&type=TXT - DMARC p=none with aggregate report mailbox dmarc@jaipur.manipal.edu.
- https://dns.google/resolve?name=_dmarc.muj.manipal.edu&type=TXT - NXDOMAIN, so RFC 7489 discovery falls back to the organizational domain policy.
- https://mujslcm.jaipur.manipal.edu/ - target portal exposing @muj.manipal.edu suffix, student/parent modes, local form, and the Microsoft reset link.
- https://www.rfc-editor.org/rfc/rfc7489.html - the DMARC subdomain fallback rule that makes muj.manipal.edu inherit p=none.

## ACTIONABLE LEADS
- Authorized browser trace with one synthetic test account on both SLCM hostnames: record the full HTTP 302 chain to see whether it hits login.microsoftonline.com /authorize or /wsfed, a SAML IdP, or stays on the local form.
- Once the protocol is known, staging tests: wrong issuer, wrong audience, expired or replayed tokens, missing nonce or InResponseTo, and cross-tenant token acceptance (a token minted for the other MUJ tenant presented to SLCM).
- Check whether SLCM authorization binds tenant/object identifiers or mutable mail aliases; the two-tenant finding makes suffix-only trust the main confused-deputy risk.
- Entra admin-side review: Conditional Access coverage for both MUJ tenants, smart lockout, banned password list, legacy authentication blocking, Identity Protection, and sign-in logs around reset events; no live spraying.
- SSPR tests with dedicated synthetic accounts per tenant: method registration, reset audit events, notification behavior, help-desk override paths, and post-reset session revocation.
- Parent/student role boundary tests with paired authorized accounts: role claims, object-level authorization, session rotation, and client-side role parameter tampering.
- Email follow-up: collect DMARC aggregate reports (rua dmarc@jaipur.manipal.edu), inventory all legitimate senders, verify SPF/DKIM alignment with controlled messages, then phase DMARC from p=none toward quarantine and reject.
- Re-check the SOP PDF: it is an internal-use document on a public URL, which is an information-disclosure observation, and its content may drift from live configuration.

## FLAGS
- SLCM federated login (OIDC, SAML, or WS-Fed) is unverified; the reset link alone is not proof of SSO. Any parent-level claim that SLCM "uses Entra SSO" would be overreach.
- AD FS absence is inferred from Managed realm responses; password hash sync or pass-through authentication behind the cloud UI cannot be excluded from public data.
- MFA evidence is enrollment language from a single June 2025 SOP; universal Conditional Access enforcement is Low to moderate confidence.
- The SOP PDF is marked "For Internal Use Only" but is public; flag as a real finding, but it does not prove current production settings.
- muj.manipal.edu DMARC inheritance depends on RFC 7489 logic and the root record having no sp override; re-verify DNS before citing.
- Tenant GUIDs, aliases, MX, and SPF are point-in-time public answers; they can change and are not secrets.
- Two reference URLs are German and Thai locale variants of Microsoft ID-token docs (learn.microsoft.com/de-de, /th-th); content equivalence with the English pages is unverified and they look like search artifacts.
- No live probing was performed by the report; any enumeration, spraying, or token manipulation done downstream would require separate written authorization.

## COVERAGE (44955 chars as read, read verified to EOF, 307 lines)

---

## w2b-01-muj-slcm-alt.digest

## REPORT
Source: w2b-01-muj-slcm-alt.md (MUJ SLCM Alternate Host OSINT Assessment)

## ANSWER SUMMARY
- Alternate host muj.slcm.jaipur.manipal.edu is a MUJ-branded SLCM-family login endpoint, same visible portal family as the primary; nothing proves dev, staging, backend, or origin role.
- A record observed: 20.244.94.89, TTL 3600; RIPEstat, ARIN, and IPinfo all attribute it to AS8075 Microsoft, prefix 20.192.0.0/10, Pune geolocation.
- Primary mujslcm.jaipur.manipal.edu resolves 98.70.14.50 in the same snapshots, also AS8075 but prefix 98.70.0.0/15.
- Official SLCM FAQ names only the primary hostname as the registration link; the alternate is not mentioned in the visible FAQ extract.
- HTML similarity (Keen theme assets, "User login example" description, Microsoft password-reset destination, EmailFor/LoginFor fields) supports a shared application family, not a shared backend or database.
- URLScan coverage asymmetry: public API search for the alternate returns zero results; the primary has a public scan record identifying 98.70.14.50.
- Email-domain text differs between pages: alternate shows @jaipur.manipal.edu, primary shows @muj.manipal.edu; report treats this as configuration or role difference, not proof of separate apps.
- The brief's "Akamai-fronted" claim was not independently verified by this pass; no target-specific Akamai DNS, header, or authoritative statement was recovered.

## KEY FACTS
- https://muj.slcm.jaipur.manipal.edu/ - alternate host; "WELCOME TO MUJ PORTAL" sign-in page, @jaipur.manipal.edu context.
- https://mujslcm.jaipur.manipal.edu/Home/Index - primary page capture; same branding and parent/student sign-in labels.
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - official FAQ; only primary URL named as SLCM registration link, AMS support, dms@ and ams@ contacts.
- https://dns.google/resolve?name=muj.slcm.jaipur.manipal.edu&type=A - observed A record 20.244.94.89.
- https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=A - observed A record 98.70.14.50.
- https://stat.ripe.net/data/network-info/data.json?resource=20.244.94.89 - RIPEstat maps address to AS8075, prefix 20.192.0.0/10.
- https://ipinfo.io/20.244.94.89/json - IPinfo labels AS8075 Microsoft Corporation, Pune, Maharashtra geolocation.
- https://whois.arin.net/rest/ip/20.244.94.89 - ARIN record for range 20.192.0.0/10, name MSFT, handle NET-20-192-0-0-1.
- https://urlscan.io/api/v1/search/?q=domain:muj.slcm.jaipur.manipal.edu - zero public scan results for the alternate.
- https://urlscan.io/result/019ed038-c4af-765c-9499-2da69a77e30a/ - primary public scan record identifying 98.70.14.50.
- http://mujslcm.jaipur.manipal.edu/ - primary capture showing ASP.NET-style request-verification field and EmailFor, LoginFor, UserName, Password inputs.
- https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf - MUJ M365 SOP v1.0 June 2025; mandatory MFA context, not SLCM topology.
- https://github.com/vikrant500/college_portal_web_and_dbms/tree/main/mujslcm.jaipur.manipal.edu_122 - third-party saved directory named after primary host with Home/Scripts/Keen assets; provenance unverified.
- http://github.com/Anushkakumar10/muj_slcm - third-party repo, single commit, README/requirements.txt; unverified reference.
- https://dns.google/resolve?name=muj.slcm.jaipur.manipal.edu&type=CNAME - no CNAME answer in queried snapshot.

## ACTIONABLE LEADS
- Compare server-returned HTML of both hosts across login paths (student, parent) in a passive pass to find divergence or identity-tenant hints.
- Check certificate transparency and TLS SANs for both names to test same-certificate binding.
- Ask MUJ IT to confirm what 20.244.94.89 is (App Service, VM, gateway, or shared address) and whether the alternate is production, migration, staging, or retired.
- Add both hostnames to the team asset inventory with role marked "unconfirmed"; document the canonical URL per the FAQ.
- Disclosure step: submit an asset-relationship report to MUJ with exact URLs, DNS snapshots, and timestamps; no credential or access tests.

## FLAGS
- "Akamai-fronted" for the primary is an unverified input from the brief; report explicitly declines to assert it.
- Classifying the alternate as dev/staging/backend bypasses is unsupported; report itself rejects those labels.
- GitHub directories from vikrant500 and Anushkakumar10 may be scraped content; not official MUJ repositories.
- Zero URLScan results for the alternate is a coverage difference, not proof the host is private or unused.
- Email-domain difference is ambiguous; report warns against overinterpretation.
- No vulnerability established anywhere in this report.

## COVERAGE
Chars read: 26,232. EOF confirmed: true.

---

## w2b-02-mujerp.digest

## REPORT
Source: w2b-02-mujerp.md (MUJ SLCM and ERP public OSINT assessment)

## ANSWER SUMMARY
- mujerp.jaipur.manipal.edu/MUJWEB/ publicly presents a Dynamics 365 Business Central sign-in surface; username/password fields and /MUJWEB/SignIn POST form observed.
- MUJ's official IT page describes Microsoft "Business ERP" and a "Student life cycle via Web portal" as separate landscape items; it never maps the mujerp hostname.
- ERP audience (staff, faculty, finance), enabled modules, and data are unknown; no public module list, role matrix, or owner statement.
- SLCM is better documented: official FAQ names the registration link and username pattern; first-year guide describes one-stop academic platform handling identity, admission, contact, education, document data.
- Attendance route /Student/Academic/AttendanceSummaryForStudent is publicly indexed but a GET returned the generic login wall, no records.
- Payroll exists as an MUJ Finance service for faculty and staff; no source places payroll inside mujerp.
- Separate MUJ HR login surface exists at mujone.jaipur.manipal.edu/HR/Login.aspx with email, employee code, DOB, captcha fields.
- Supplied technology claims (ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, Azure 20.244.0.229) remain unconfirmed by public evidence.

## KEY FACTS
- https://mujerp.jaipur.manipal.edu/MUJWEB/ - ERP landing; "Welcome to Dynamics 365 Business Central" title, user-name and password labels.
- https://mujerp.jaipur.manipal.edu/MUJWEB/SignIn - public markup shows form POST to this endpoint; no SSO button or role selector observed.
- https://mujslcm.jaipur.manipal.edu/ - SLCM landing; WELCOME TO MUJ PORTAL, Sign In and Parent Login controls, @muj.manipal.edu suffix.
- https://mujslcm.jaipur.manipal.edu/Student/Academic/AttendanceSummaryForStudent - indexed attendance route; retrieval returned login wall only.
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - official FAQ; registration link, name-plus-registration-number username, Outlook ID password, AMS support.
- http://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf - official onboarding guide; SLCM academic purpose, identity/admission fields, parent OTP, document uploads.
- https://www.jaipur.manipal.edu/administration-it.php - official IT page; Microsoft Business ERP vs student life cycle portal, IT security remit.
- https://www.jaipur.manipal.edu/administration-finance.php - Finance page; payroll services to faculty and staff, accounting and reporting duties.
- https://jaipur.manipal.edu/human-resource.php - HR page; employee lifecycle, compensation, benefits, leave management.
- https://mujone.jaipur.manipal.edu/HR/Login.aspx - separate MUJ HR login surface; employee-oriented fields.
- https://slcm.vercel.app/guides/check-attendance-muj - betterSLCM guide; claims attendance display and prediction, third-party.
- http://github.com/DK10WS/SLCM_APP - third-party app README; claims attendance, grades, GPA/CGPA, timetable; not official.
- https://mujstella.in/ - independent student platform; explicit non-affiliation with MUJ.
- https://learn.microsoft.com/en-us/dynamics365/business-central/finance - generic product docs; finance capabilities and payroll transaction imports, not MUJ configuration.
- https://www.microsoft.com/en-us/dynamics-365/products/business-central - generic product context for Business Central.

## ACTIONABLE LEADS
- Verify the 20.244.0.229 mapping claim by resolving mujerp DNS and checking attribution; report currently holds it unconfirmed.
- In an authorized environment only, test whether /MUJWEB/SignIn failure responses distinguish valid users; note the surface in inventory.
- Inventory SLCM routes named by third-party tools (attendance, grades paths) and check which are publicly indexed.
- Keep ERP and SLCM as separate boxes in team diagrams with an unverified relationship label.
- Disclosure step: ask MUJ IT for an official hostname-to-system mapping and Business Central tenant documentation.

## FLAGS
- "mujerp is staff/faculty-facing" is an inference; page states no audience.
- Payroll inside mujerp is unproven; generic Business Central docs do not prove enabled modules.
- Azure IP 20.244.0.229, ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai, M365 identity are unconfirmed inputs.
- Attendance/grades claims come from third-party sources, not official MUJ specs.
- Route discoverability does not equal data exposure; retrieval hit the login boundary.

## COVERAGE
Chars read: 36,398. EOF confirmed: true.

---

## w2b-03-mujone.digest

## REPORT
Source: w2b-03-mujone.md (MUJ One and SLCM public-facing ecosystem assessment, dated 2026-08-25)

## ANSWER SUMMARY
- MUJ One is publicly evidenced as an MAHE-credited HR system: root page titled "MUJ HR SYSTEM", HR path credits ISD/CSD, MAHE; not a confirmed student super-app.
- Observed HR surface: Email entry, Reset Password, Employee Code, Date of Birth, captcha, change-password fields, Code of Conduct and POSH policy acknowledgements, and a "Visit PAS Portal" link to http://pas.muj.edu.in/.
- SLCM is a distinct student/parent portal ("WELCOME TO MUJ PORTAL", Sign In, Parent Login, Student Login); no official link, API, or shared-login handoff between MUJ One and SLCM found.
- No dedicated MUJ One listing in the captured Google Play search; Apple search returned no preserved listing (lower confidence). MUJStella is separate: 4.4 stars, 21 reviews, 1K+ downloads, updated 2026-01-21, explicitly independent.
- MUJguide claims its own service fetches timetable, attendance, marks, grades, CGPA, transcript from SLCM; operated solely by Bharath G; third-party integration evidence only.
- M365 identity context is real (SOP IT-SOP-O365-001 v1.0, June 2025, mandatory MFA, login.microsoftonline.com), but Entra SSO or token flow for MUJ One or SLCM is unproven.
- MUJ One A record 52.172.36.15, AS8075 Microsoft, AS type hosting; no CNAME answer observed; Akamai and exact stack versions unverified.
- Credential conflict: official FAQ gives name.registration number username; unofficial guide says full @muj.manipal.edu email address. Report does not reconcile them.

## KEY FACTS
- https://mujone.jaipur.manipal.edu/ - root; "MUJ HR SYSTEM" title and pre-sign-in policy notice.
- https://mujone.jaipur.manipal.edu/HR/ - employee fields, captcha, policy acknowledgement, ISD/CSD MAHE credit, PAS Portal link.
- http://pas.muj.edu.in/ - PAS Portal link target from HR page; PAS purpose not expanded in extract.
- https://mujslcm.jaipur.manipal.edu/ - SLCM; student/parent sign-in, POST form with UserName and Password, forgot-password link to passwordreset.microsoftonline.com.
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - official FAQ; username grammar name.registration number with example garv.2506040062, Outlook ID password, AMS/IT contacts.
- https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf - M365 SOP; Microsoft sign-in, mandatory MFA, Authenticator/phone/email options.
- https://dns.google/resolve?name=mujone.jaipur.manipal.edu&type=A - captured A record 52.172.36.15.
- https://ipinfo.io/52.172.36.15 - AS8075 Microsoft Corporation, AS type hosting.
- https://dns.google/resolve?name=mujone.jaipur.manipal.edu&type=CNAME - no CNAME answer; CDN absence inconclusive.
- http://mujslcm.jaipur.manipal.edu/keen/themes/keen/theme/demo1/dist/assets/js/pages/custom/user/login.js - public Keen login script asset; jQuery 1.10.2, Validate, unobtrusive validation clues.
- https://dns.google/resolve?name=muj.manipal.edu&type=TXT - TXT includes spf.protection.outlook.com and Microsoft verification material.
- https://www.mujguide.in/ - third-party super-app; claims SLCM timetable, attendance, marks, grades, CGPA, transcript; credentials stored on device.
- https://play.google.com/store/apps/details?hl=en-US&id=com.yourcompany.mujstellaapp - MUJStella listing; SLCM Attendance and Timetable Tracker update note.
- https://mujstella.in/ - site says independent and not affiliated with MUJ.
- https://www.myandroid.org/apps/com-manipal-muj-go - secondary directory showing package com.manipal.muj.go, app name MUJ GO; publisher and current status unverified.
- https://www.reddit.com/r/manipaljaipur/search/?q=SLCM&restrict_sr=1 - anecdotal SLCM downtime/login discussion titles; no validated timeline.

## ACTIONABLE LEADS
- Asset map: record MUJ One, SLCM, PAS, HR login, and student tools as separate records with owner/credit and audience fields.
- Monitor MUJguide and MUJStella public claims as indicators of live SLCM behavior (they track attendance/grades features).
- Verify MUJ GO package attribution before adding it to inventory; store publisher, package name, privacy info.
- Check web archives for mujone paths to see if an older surface exposed different modules.
- Disclosure step: ask MUJ whether PAS portal and MUJ One are separate assets and whether the FAQ username grammar is current.

## FLAGS
- "MUJ One super-app" assumption is contradicted by the HR-only public surface.
- Username convention conflict between FAQ and unofficial guide is unresolved.
- Apple app search was not preserved as a listing record; lower confidence negative.
- Akamai, ASP.NET MVC 5.3, .NET 4.x, IIS 10 unverified; response markup and asset clues only.
- Reddit posts are anecdotal signals, not reliability data.
- MUJStella package id com.yourcompany.mujstellaapp looks placeholder-like; listing metadata should be re-checked before citation.
- Shared domain does not imply shared backend or SSO.

## COVERAGE
Chars read: 44,845. EOF confirmed: true.

---

## w2b-04-rms.digest

## REPORT
Source: w2b-04-rms.md (research status: MUJ SLCM and RMS)

## ANSWER SUMMARY
- rms.jaipur.manipal.edu publicly presents as a Research Data Management System, not a student examination-result system.
- Landing page shows research-performance announcements (April and May 2025), an MUJ IRINS link, username/password labels, a Chrome browser recommendation, and a footer crediting MSIS and ISD, MAHE.
- DNS maps the hostname to 202.131.155.153; the numeric host served the same research-announcement content.
- The main Manipal RMS site (rms.manipal.edu) covers login access, publication, APC, conference-entry, grants, seed money, and open-access queries, and says RMS uses the same credentials as the Outlook account.
- No public result PDF format, marks data, or result-fetching JavaScript endpoint was established; the SLCM page exposes only sign-in and parent-login labels.
- RMS-to-SLCM marks relationship is not documented; no source says RMS stores or publishes student marks.
- Note: file is a status report from a mid-research pass; it lists unanswered questions and safe next steps rather than a full verdict table.

## KEY FACTS
- https://rms.jaipur.manipal.edu/ - RMS landing; Research Data Management System title, research announcements, IRINS link.
- https://202.131.155.153/ - numeric host; same research-performance announcement type of content.
- https://rms.jaipur.manipal.edu/Login.aspx - public Login.aspx path; visible content repeats announcements, no result index.
- https://rms.manipal.edu/ - main RMS; publication, APC, conference, grants, open-access research administration functions, Outlook-credential guidance.
- https://mujslcm.jaipur.manipal.edu/ - SLCM entry; MUJ portal sign-in and parent-login option.
- https://mujslcm.jaipur.manipal.edu/Home/Index - indexed SLCM home path with "Manipal University" and "Forgot Password?".
- https://jaipur.manipal.edu/examination.php - official examination page; continuous assessment via participation, assignments, lab work, class tests, in-semester tests.
- https://dns.google/resolve?name=rms.jaipur.manipal.edu&type=A - public DNS answer 202.131.155.153.
- http://web.archive.org/cdx/search/cdx?collapse=urlkey&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&output=json&url=mujslcm.jaipur.manipal.edu/* - archived SLCM URL inventory for historical asset review.
- http://jaipur.manipal.edu/research.php - MUJ Directorate of Research page; broader research context.

## ACTIONABLE LEADS
- Review the Wayback CDX inventory of mujslcm paths for explicitly named result, grade, or marks paths.
- Compare server-returned public HTML of the RMS and SLCM landing pages in a passive pass.
- Search MUJ's own site for "grade card", "marksheet", "semester result", "result declaration", "examination result".
- Verify whether any candidate "result" PDF belongs to RMS, admissions, or another Manipal service before use.
- Keep the RMS word in quotes and always qualify it as research administration in team material.

## FLAGS
- RMS acronym conflation risk: Research Data Management System vs a guessed Result Management System.
- No indexed RMS result PDF is a bounded negative finding, not proof of absence.
- Supplied stack claims (ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai, M365 identity) unverified for this host.
- Historic crawlable assets do not prove application routes or data fetching.
- Status-report format leaves some claims open; treat all as unverified.

## COVERAGE
Chars read: 11,445. EOF confirmed: true.

---

## w2b-05-helpdesk.digest

## REPORT
Source: w2b-05-helpdesk.md (MUJ SLCM helpdesk OSINT assessment)

## ANSWER SUMMARY
- Ticketing vendor for helpdesk.jaipur.manipal.edu is unattributable from public evidence; Freshworks is visible on servicedesk.manipal.edu and osTicket on helpdesk.manipal.edu.my, both different domains.
- Google DoH returned Status 3 with no Answer for A, AAAA, and CNAME queries; resolver observation only, not proof of permanent decommissioning.
- Certificate-transparency shows exact certificates for the name: Entrust DV TLS Issuing RSA CA 2, valid 2026-01-08 through 2027-01-08, which conflicts with weak current DNS and archive visibility.
- urlscan reports the hostname as not observed; Wayback CDX query returned an empty array; public discovery footprint is very small.
- SLCM is separate and better observed: official onboarding guide names mujslcm.jaipur.manipal.edu as the Student Life Cycle Management portal, credentials sent to personal Gmail, technical issues routed to University Helpdesk or Admissions.
- urlscan for SLCM records HTTP 200, Microsoft-IIS/10.0, ASP.NET, and a Forgot Password? link to passwordreset.microsoftonline.com; older scan shows IIS/8.5 with different IP and ASN.
- No public ticket workflow, KB article, API, or attachment route evidenced on the target; Zendesk and Freshdesk docs are comparators only.
- User reports (not official records): invalid registration number after intra-sliding, and password error despite believed-correct password.

## KEY FACTS
- https://urlscan.io/domain/helpdesk.jaipur.manipal.edu - no direct hits, nothing hosted, no incoming hits, nothing talked to the domain.
- https://dns.google/resolve?name=helpdesk.jaipur.manipal.edu&type=A - Status 3, no Answer section.
- https://dns.google/resolve?name=helpdesk.jaipur.manipal.edu&type=AAAA - Status 3, no Answer section.
- https://dns.google/resolve?name=helpdesk.jaipur.manipal.edu&type=CNAME - Status 3, no Answer section.
- https://crt.sh/?q=%25.jaipur.manipal.edu&output=json - exact helpdesk name in CT records; Entrust issuer, 2026-01-08 to 2027-01-08 validity.
- https://web.archive.org/cdx/search/cdx?url=helpdesk.jaipur.manipal.edu/*&output=json&filter=statuscode:200 - empty array, no matching 200 captures.
- https://servicedesk.manipal.edu/support/tickets/new - Freshworks visible, but a different Manipal hostname.
- https://helpdesk.manipal.edu.my/ - MUCM Helpdesk, powered by osTicket, separate domain.
- https://mujslcm.jaipur.manipal.edu/ - SLCM public surface; Sign In, Parent Login, Student Login, Forgot Password?, @muj.manipal.edu.
- https://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf - official guide; SLCM URL, one-stop academic platform, Gmail credential delivery, helpdesk/admissions escalation path.
- https://urlscan.io/result/019ed038-c4af-765c-9499-2da69a77e30a/ - SLCM scan; IIS/10.0, ASP.NET, Microsoft password-reset link, IP 98.70.14.50 AS8075.
- https://www.jaipur.manipal.edu/contact-university.php - official IT support contact it.support@jaipur.manipal.edu, extensions 778 and 300.
- https://www.onlinemanipal.com/help-center - online-program help center; helpdesk@mujonline.edu.in, +91-7996 600 444; enrolled-learner context.
- https://www.reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue - user-reported SLCM password error.
- https://www.reddit.com/r/Manipal_Academics/comments/1993mdc/slcm_login - user-reported invalid registration number after intra-sliding.
- https://developers.google.com/speed/public-dns/docs/doh/json - DoH docs; the excerpt defines Status 0 and 2 but not value 3, so the report avoids overstating NXDOMAIN.

## ACTIONABLE LEADS
- Re-run DNS checks periodically; Status 3 may reflect temporary record state, split DNS, or retirement.
- Query CT logs for other jaipur.manipal.edu subdomains to find candidate helpdesk aliases or vendor domains.
- Watch crt.sh for certificate renewal on the name; renewal timing indicates lifecycle intent.
- Use official channels (it.support@jaipur.manipal.edu) to ask the owner which ticketing product serves MUJ.
- Do not test Zendesk, Freshdesk, or osTicket routes against the target; vendor docs are comparators only.

## FLAGS
- Contradiction preserved: valid 2026-2027 certificate vs no current DNS answer; explanation (migration, retirement, split DNS) unknown.
- DoH Status 3 meaning is not defined in the cited documentation excerpt; treated as "unresolved at observation point".
- SLCM IIS/ASP.NET evidence must not be transferred to the helpdesk hostname.
- Scribd reference (SLcM MIT user manual) belongs to another Manipal SLCM context, unrelated to the MUJ target.
- urlscan "not observed" is a coverage statement, not proof of nonexistence.

## COVERAGE
Chars read: 30,166. EOF confirmed: true.

---

## w2b-06-admissions-nopaperforms.digest

## REPORT (w2b-06-admissions-nopaperforms.md)
MUJ admissions and NoPaperForms/Meritto SaaS link to SLCM. Public DNS and document analysis only, no testing. Verdict: hostname delegation confirmed, technical hand-off to SLCM not publicly documented. 228 lines, 37678 chars, read to EOF, truncated: false.

## ANSWER SUMMARY
- DNS resolves admissions.jaipur.manipal.edu as CNAME to jaipurmanipal.nopaperforms.com, then through an AWS ELB chain in ap-south-1. Delegation is confirmed; record storage, schema, and SLCM sync are not.
- The 2022 online-program manual documents identity, contact, academic, guardian, employment, uploaded document, payment, and status data, plus refund rules. It is an archived example, not the current schema for every program.
- Payment is online only (card, net banking, UPI), success triggers email and SMS, fee receipt via student portal. Processor name and tokenization are not stated.
- Statuses named: Application Downloaded, Under Review, Admission Approved, Provisional Admission, Re Submission Required, Rejected.
- SLCM FAQ: registration URL, username from name plus registration number, password based on the official Outlook ID, and Admission-only correction of admission-time details.
- No public source names an API, webhook, SSO assertion, database feed, or provisioning trigger between NoPaperForms and SLCM. The bridge is undisclosed.
- Meritto says the customer is controller or fiduciary and Meritto is processor; Trust Center lists SOC 2, ISO 27001, GDPR claims. These are vendor-wide, not MUJ-tenant evidence.

## KEY FACTS
- https://dns.google/resolve?name=admissions.jaipur.manipal.edu&type=CNAME - the core delegation proof: owner admissions.jaipur.manipal.edu, target jaipurmanipal.nopaperforms.com.
- https://dns.google/resolve?name=jaipurmanipal.nopaperforms.com&type=A - resolution chain through an AWS ELB name in ap-south-1, several addresses.
- https://admissions.jaipur.manipal.edu/ - current 2026-27 branded admissions landing page.
- https://muj.onlinemanipal.com/wp-content/uploads/2022/01/MUJ-Admission-Manual-Online-Programmes-V5.pdf - the detailed field, status, payment, and refund spec.
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - SLCM registration URL, username convention, Outlook-based password, Admission-controlled correction.
- https://www.meritto.com/privacy-policy/ - controller/processor split, subprocessors, contacts data@meritto.com, ticket@meritto.com, grievance@meritto.com.
- http://trustcenter.nopaperforms.com/ - SOC 2, ISO 27001 (surveillance audit May 21 2025), GDPR renewal (June 5 2026) claims.
- http://developer.nopaperforms.com/ - vendor module list: Lead, Opportunity, Activity, Form, Payment, User Role Permission, Query, Application.
- https://mujslcm.jaipur.manipal.edu/Home/Index - SLCM login surface with student and parent sign-in choices.
- https://jaipur.manipal.edu/admissions.php?p=UG - Apply Now and Track Application links, WhatsApp enquiry fields (Name, Phone, Email ID, Course, City, State).
- https://www.jaipur.manipal.edu/pay-fee-online.php - Pay Fee Online link, separate from the application flow in the report's view.
- http://manipal.edu/mu/important-links/privacy-and-cookie-policy.html - MAHE-wide privacy policy, not a MUJ-specific DPA.
- https://www.jaipur.manipal.edu/admission-contact.php - admission contact channel.
- https://apply.manipal.edu/ - separate application login surface, distinct from admissions.jaipur.manipal.edu.
- http://jaipur.manipal.edu/admissions.php - admissions index page.

## ACTIONABLE LEADS
- Re-run the two dns.google queries fresh; record answers and dates as point-in-time evidence.
- Check cdn.npfs.co asset references on the current UG route as SaaS presentation corroboration.
- Map the public admissions workflow: Apply Now, Track Application, Pay Fee Online, WhatsApp enquiry, admission contact.
- Treat the SLCM FAQ account convention as the onboarding boundary spec: name plus registration number, Outlook-based password, Admission-only corrections.
- Ask MUJ for a sanitized admissions-to-SLCM data-flow diagram, field-mapping document, tenant DPA, payment architecture summary, upload-deletion policy, and a non-production test account.
- Do not submit fake applications, enumerate applicants, or probe IIS, ASP.NET, Akamai, or M365 behavior without written scope.

## FLAGS
- The detailed field inventory comes from a 2022 archived online-program manual; the current form schema is not proven identical.
- The extractor failed to produce a stable text document of the current form; form labels seen in server HTML are not values.
- Application number is not equated with SLCM registration number anywhere in the reviewed sources; do not conflate them.
- No public integration mechanism exists in the record; absence of documentation is not proof of absence of an integration.
- Trust Center dates are vendor-level attestation only, no tenant-specific audit evidence.
- DNS observations are time-sensitive; E.g. style citations in the report mix sources but all listed references were preserved.

## COVERAGE
- File read to EOF: 228 lines, 37678 chars (file_size 37678), truncated: false. Confirmed EOF at line 228, final reference.

---

## w2b-07-student-mujonline.digest

## REPORT (w2b-07-student-mujonline.md)
Public OSINT comparison: MUJ Online student portal versus MUJ SLCM, plus Brightspace, M365 identity, and stack claims. No authentication attempted. Verdict: multi-application ecosystem, portal auth protocol unknown, no vulnerability claims. 242 lines, 36739 chars, read to EOF, truncated: false.

## ANSWER SUMMARY
- student.mujonline.com exposes a sparse shell: "Student Portal", "Welcome!", "To student portal", an Email label, and a help-desk message. Password, OTP, and provider are not shown.
- SLCM is separately documented as an institutional portal: registration URL, name-plus-registration-number username, Outlook-linked password, DMS/AMS and IT Infra support split, Admission-only corrections.
- D2L Brightspace is publicly identified as the LMS: "Powered by D2L Brightspace" on the login route plus a D2L customer case study. The student portal itself is not proven to be Brightspace.
- MUJ Office 365 SOP documents university mail IDs and mandatory MFA (Authenticator, phone SMS OTP, personal email). It does not prove federation for student.mujonline.com.
- One public Reddit report of an SLCM password error exists; no credible portal-specific breach report was found for MUJ Online.
- Supplied stack (ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai, M365 identity) is treated as an input hypothesis; public evidence confirms only fragments (jQuery 1.10.2 assets on SLCM, Angular-style assets on the portal).
- iLearn page looks like an enquiry or enrolment flow with four-digit OTP, not an enrolled-student login.

## KEY FACTS
- https://student.mujonline.com/ - public portal shell; Email label and help-desk text only.
- https://student.mujonline.com/login - same sparse shell on the login route.
- https://learning.onlinemanipal.com/d2l/home/14042 - Brightspace login route with visible product branding.
- https://muj.onlinemanipal.com/student-experience - UNext Labs (Python, R, MySQL, Java, PHP), mock exams, slot booking, practical exams, evaluation.
- https://muj.onlinemanipal.com/help-center - enrolled-student support: helpdesk@mujonline.edu.in, +91 7996 600 444.
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - SLCM registration URL, username format, Outlook-based password, support contacts.
- https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf - first-time setup, temporary password, mandatory MFA, verification methods.
- https://mujslcm.jaipur.manipal.edu/Home/Index - SLCM surface with student and parent choices.
- https://www.d2l.com/en-in/why-d2l/customers/manipal-university-jaipur-online - D2L case study naming Brightspace, scale, and learning capabilities.
- https://muj.onlinemanipal.com/ilearn-login - enrolment-style page with consent checks and OTP, not confirmed as student login.
- https://muj.onlinemanipal.com/ - programme delivery page describing LMS features and remote exams.
- https://www.reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue - the single public credential complaint, SLCM-specific.
- https://www.manipal.edu/mu/academics/student-portal.html - MAHE portal page linking sis.manipal.edu; not evidence about MUJ Online.
- http://muj.onlinemanipal.com/notifications - official notices describing the LMS learning workflow.
- https://learning.onlinemanipal.com/d2l/home/14201 - second D2L route with generic system-experience wording.

## ACTIONABLE LEADS
- Passive collection only: capture response headers, certificates, and DNS for student.mujonline.com, learning.onlinemanipal.com, and mujslcm.jaipur.manipal.edu.
- Research backlog: official user guide for the portal, explicit SSO documentation, recovery and lockout procedures, disclosure instructions (none found yet).
- Build a portal ownership matrix: who owns identity, records, course content, labs, exams, and support per domain.
- Model SLCM and portal as separate incident categories; do not merge failures into one "MUJ login problem".
- Authorized follow-up only: verify headers, certs, and deployment relationships under written permission.

## FLAGS
- Brightspace "may not be getting an optimal system experience" wording is generic, not an outage.
- Angular-style and jQuery observations are passive markup clues, not confirmed frameworks.
- The Office 365 SOP proves M365 identity exists university-wide, not that the portal delegates to it.
- iLearn classification is based on visible controls only.
- No breach evidence is absence of incident reports, not proof of security.
- Akamai was not independently confirmed in this pass.

## COVERAGE
- File read to EOF: 242 lines, 36739 chars (file_size 36739), truncated: false. Confirmed EOF at line 242, final reference.

---

## w2b-08-learning-onlinemanipal.digest

## REPORT (w2b-08-learning-onlinemanipal.md)
Brightspace tenant and MUJ SLCM posture assessment. Passive public evidence only. Verdict: Brightspace attribution high, Microsoft 365 SSO unconfirmed, grades sync unknown, no vulnerability finding against MUJ. 314 lines, 54600 chars, read to EOF, truncated: false.

## ANSWER SUMMARY
- D2L's own case study names MUJ Online as a Brightspace customer and describes a 2020 initiative scaling to 85,000 students in five years; URLScan records CNAME muj.brightspace.com. Tenant attribution is high confidence.
- Route /d2l/home/14042 is an indexed MUJ login page with Username and Forgot your password; no Microsoft, Entra, SAML, or OIDC naming on the public page.
- D2L documents customer-managed SAML as a capability; that says SAML is possible, not that MUJ uses it. Microsoft 365 federation remains unverified.
- Brightspace release and patch level are unknown; CVE-2021-43129 is a quiz right-click bypass with no NVD CVSS, product-level and historical only.
- Grades sync is not publicly confirmed. D2L documents generic IPSIS final-grade export (IMS LIS v2.0), SLCM documentation lists attendance, marks, and results; no connector, direction, or schedule is public.
- Public complaints are SLCM fee-state issues (fee portal not visible; paid fee pending), not Brightspace incidents.
- D2L disclosure policy requires customer authorization to test instances and accepts reports at incident@d2l.com.

## KEY FACTS
- https://learning.onlinemanipal.com/d2l/home/14042 - MUJ login route, org-unit identifier 14042, no IdP named.
- https://urlscan.io/domain/learning.onlinemanipal.com - historical record: CNAME muj.brightspace.com, AS16509 AMAZON-02, Sydney GeoIP, with explicit snapshot caveats.
- https://www.d2l.com/en-in/why-d2l/customers/manipal-university-jaipur-online - vendor and customer attribution, reported outcomes (30% discussion, 15% completion, 10% performance, 30% grading, 40% admin workload).
- https://nvd.nist.gov/vuln/detail/CVE-2021-43129 - Brightspace right-click bypass record, no affected version, CVSS N/A.
- https://community.d2l.com/brightspace/kb/articles/23533-d2l-vulnerability-disclosure-policy - authorization rule and incident@d2l.com reporting contact.
- https://community.d2l.com/brightspace/kb/articles/23729-overview-of-grades-and-ipsis - generic IPSIS final-grade export to a SIS using IMS LIS v2.0.
- https://community.d2l.com/brightspace/kb/articles/4843-saml-administration-overview - customer-managed SAML and IdP registration capability.
- http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf - SLCM ICT description: attendance, internal/external marks, results, broadcasts.
- https://www.reddit.com/r/Manipal_Academics/comments/1u8476b/slcm_portal_issue - fee portal visibility complaint, SLCM named, no resolution.
- https://www.reddit.com/r/Manipal_Academics/comments/1lzf0ht/paid_my_fees_but_still_showing_as_pending_on_slcm - deducted payment still pending, receipt mentioned.
- http://mahe.onlinemanipal.com/help-center - LMS access follows enrollment and fee payment; login details emailed.
- http://manipal.edu/mu/important-links/privacy-and-cookie-policy.html - MAHE policy: data categories, sharing, retention, privacy.mahe@manipal.edu.
- https://www.d2l.com/cloud - D2L states AWS is its primary strategic cloud provider.
- https://www.d2l.com/solutions/higher-education/d2l-brightspace-and-sis-integrations-for-higher-education/ - generic SIS integration wording, not MUJ-specific.
- https://muj.onlinemanipal.com/ - Online Manipal programme page describing LMS functions.

## ACTIONABLE LEADS
- Ask MUJ or D2L for: tenant release, IPSIS enablement status, SAML and Entra settings, claims mapping, deprovisioning flow, grade source of truth, incident history.
- Reconcile enrollment, payment, provisioning, and support timestamps to check the fee-to-access dependency.
- Route SLCM fee complaints to SLCM and payment owners; correlate with Brightspace only via authorized logs.
- Preserve URLScan, case study, and Reddit excerpts with retrieval dates in the evidence register.
- For a genuine D2L issue, report through the D2L policy; do not test the MUJ instance without customer authorization.

## FLAGS
- URLScan fields are historical observations; ASN, GeoIP, and hit-count labels are not current availability or security verdicts.
- Case study outcome percentages are vendor-published claims, not audited measurements.
- CVE-2021-43129 lacks an affected version and CVSS in the retrieved NVD record; do not map it to the tenant.
- Fee complaints may be reconciliation or support issues; not renamed as security incidents.
- The vendor case study wording quoted in the source praises the LMS chosen; the report repeats vendor claims, no tenant posture claim rests on them.
- Reference 20 in the report is a malformed markdown link to https://slcm.manipal.edu/.

## COVERAGE
- File read to EOF: 314 lines, 54600 chars (file_size 54600), truncated: false. Confirmed EOF at line 314, final reference.

---

## w2b-09-mujconnect.digest

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

---

## w2b-10-sis-manipal.digest

## REPORT (w2b-10-sis-manipal.md)
MAHE SIS/SLCM WebForms architecture and defensive OSINT. Public observation only. Verdict: SIS login surface confirmed, WebForms-era hypothesis medium confidence, shared-code and vulnerability claims unproven. 260 lines, 39488 chars, read to EOF, truncated: false.

## ANSWER SUMMARY
- MAHE's official Student Portal page links to https://sis.manipal.edu/index.aspx; the login route studloginSLCM.aspx shows Login, a (dd/mm/yyyy) hint, Captcha, and an MAHE Information Systems Department footer.
- .aspx is consistent with ASP.NET Web Forms but does not prove runtime, version, IIS config, auth protocol, or topology. ViewState, request validation, and CAPTCHA are review questions, not findings.
- Portal family: MAHE SLCM (MU SLcM), MUJ (WELCOME TO MUJ PORTAL), and Manipal Dubai (slcm.manipaldubai.com) share SLCM vocabulary; shared code, database, or identity is unproven. Label it "shared SLCM product-family hypothesis".
- A public Salesforce sandbox login (maheslcmtech--sit.sandbox.my.site.com) plus a Salesforce announcement about SLCM modernization support a hybrid legacy-plus-modern scenario, not complete migration.
- Supplied claims of MVC 5.3, .NET 4.x, IIS 10, Akamai, and Microsoft 365 identity remain unverified for SIS; Microsoft and Akamai documentation cited is generic.
- One Reddit SLCM password complaint is a symptom for service-desk correlation, not evidence of a security defect.

## KEY FACTS
- https://sis.manipal.edu/studloginSLCM.aspx - the analyzed login surface: Login, date hint, Captcha label, MAHE Information Systems footer.
- https://www.manipal.edu/mu/academics/student-portal.html - official MAHE page linking to sis.manipal.edu/index.aspx.
- https://sis.manipal.edu/ - SIS Portal root, sparse visible text.
- https://slcm.manipal.edu/ - MU SLcM portal, MAHE identity, 2017 copyright in search result.
- http://slcm.manipal.edu/StudentChangePassword.aspx - public password-change route under the same host.
- https://slcm.manipaldubai.com/ - Manipal Dubai SLCM sign-in page.
- http://manipaldubai.com/about-us - official Dubai page linking the campus Student Portal.
- http://maheslcmtech--sit.sandbox.my.site.com/login?locale=us - public Salesforce sandbox login named "Login | SLCM".
- https://mujslcm.jaipur.manipal.edu/ - MUJ portal welcome and sign-in surface.
- https://muj.slcm.jaipur.manipal.edu/ - secondary MUJ student-login result with Forgot Password wording.
- https://learn.microsoft.com/en-us/previous-versions/aspnet/ms178472%28v%3Dvs.100%29 - WebForms page lifecycle: initialization, control instantiation, state restoration.
- https://owasp.org/www-community/ASP-NET_Request_Validation - request validation scoped as defense in depth, not a substitute for output encoding and authorization.
- https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-framework - .NET Framework 4.8 listed as active; generic support status only.
- http://reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue - user-reported SLCM password rejection.
- https://techdocs.akamai.com/cloudlets/docs/proxy - Akamai proxy concept doc; does not prove any Manipal hostname uses Akamai.

## ACTIONABLE LEADS
- Build a public-OSINT evidence register: URL, collection date, title, wording, fact or inference or unknown class.
- Ask the owner: SIS and SLCM team ownership, production versus test domains, retirement or modernization plans, authoritative identity systems, supported runtime baseline, login-fault reporting path.
- Deliver a control map over the login boundary: identity, session, state, bot mitigation, logging, monitoring, recovery.
- For authorized technical work: written scope naming domains, dates, source IPs, test accounts, allowed methods, stop conditions; use a non-production replica with synthetic identities.
- Do not test password-reset flows, craft ViewState, or measure rate limits against production.

## FLAGS
- The report's reference citations degrade into opaque bracket tokens inside tables (for example [114.0; 35.0]); verify each cited URL directly before reuse.
- Salesforce sandbox login is public but does not prove production use or API-led integration status.
- Shared product family is an inference; shared code, shared databases, and shared identity are "Very low" or "Low" confidence in the report's own table.
- CAPTCHA presence says nothing about server-side enforcement or monitoring.
- The Reddit password complaint has multiple benign explanations; do not treat it as a compromise signal.
- .NET 4.8 active status is product policy, not evidence of the deployed runtime.

## COVERAGE
- File read to EOF: 260 lines, 39488 chars (file_size 39488), truncated: false. Confirmed EOF at line 260, final reference.

---

## w2b-11-pay-fee-online.digest

## REPORT
Source file: w2b-11-pay-fee-online.md (MUJ SLCM Fee Payments: Public-Evidence Security Report)

## ANSWER SUMMARY
- Official pay-fee page routes existing students to https://mujslcm.jaipur.manipal.edu/ for online academic fee payment; hostel and mess fees are routed through the SpaceBasic app as a separate journey.
- No public MUJ page names BillDesk, Razorpay, CCAvenue, SBI ePay, or Cashfree as the academic fee provider; gateway attribution stays Unknown for all five.
- A MUJ-branded NTT DATA Pay URL exists in search evidence, but no public SLCM linkage, checkout fields, or API evidence was found; treat as an unconfirmed integration lead.
- Bank transfer path is fully documented: Canara Bank, IFSC CNRB0003563, account number built from "MUVAN" plus registration or application number, with email reconciliation of UTR, debit account holder name, date, and amount to student.finance@jaipur.manipal.edu.
- Refund policy: full refund to 30 September 2026, Rs 1,000 deduction from 1 to 31 October 2026, then 100/90/80/50/nil bands; eligible refunds paid within 45 days of hard-copy application; original receipt, ID card surrender, and dues clearance required.
- Annual fee PDF for AY 2026-27 extracts only as a garbled hostel annexure (SpaceBasics-only wording, 5 July 2026 deadline); document tells nothing reliable about course fees.
- Comparator incidents (JMI fake fee emails and QR codes, Sai Nath clone site, CYFIRMA unnamed clone, CSJMU five fake sites) argue for canonical domain lists and verification controls; none proves a MUJ incident.
- Public evidence exposes no authenticated fee screen, receipt layout, transaction template, callback design, or payment incident; those remain Unknown.

## KEY FACTS
- https://www.jaipur.manipal.edu/pay-fee-online.php - official payment route directory; source of SLCM, SpaceBasic, bank, NRI, and reconciliation wording
- https://mujslcm.jaipur.manipal.edu/ - student portal named for online fee payment; landing shows Parent Login and Student Login only
- https://muj-payservices.nttdatapay.com/DirectPay/MUFee - MUJ-branded NTT DATA Pay URL; strongest gateway lead, integration unconfirmed
- https://jaipur.manipal.edu/fee-structure.php - programme directory only, not a complete fee schedule
- https://jaipur.manipal.edu/indian-fee-structure.php - fee policy: amount changes possible, registration non-refundable, caution deposit refundable, demand draft accepted
- https://www.jaipur.manipal.edu/indian-refund-policy.php - dated refund bands and document requirements
- https://jaipur.manipal.edu/hostel-fees.php - AY 2026-27 hostel amounts, payment modes behind room-booking portal, gateway charges possible
- https://www.jaipur.manipal.edu/img/pdf/Annual-Fee-Payment-for-the-AY-2026-2027.pdf - linked annual notification; OCR-incomplete hostel annexure only
- https://jaipur.manipal.edu/img/pdf/Annual-Fee-Payment-AY-2026-2027-NRI.pdf - NRI notification; extracted content largely duplicated the hostel annexure
- https://www.ugc.gov.in/pdfnews/1857727_Fee-Refund-Policy-2025-26.pdf - UGC refund policy reference for band comparisons
- https://www.jmi.ac.in/upload/menuupload/Advisory%20Regarding%20Fee%20Payment.pdf - JMI advisory on fake fee emails, fake QR codes, and official-channel rules
- https://the420.in/sai-nath-university-fake-website-student-fraud-agra/ - lookalike university site case; media-reported allegations only
- https://www.cyfirma.com/research/weaponization-of-indian-student-data-an-ecosystem-for-phishing-social-engineering-and-financial-fraud/ - student data weaponization report; unnamed university clone
- https://the420.in/kanpur-csjmu-5-fake-websites/ - CSJMU warning against five fake sites and third-party payment portals
- http://in.nttdatapay.com/docs - NTT DATA provider documentation with PCI-DSS claims; provider level only, no MUJ specifics

## ACTIONABLE LEADS
- Re-extract the AY 2026-27 fee PDFs with a real PDF text tool to recover the course fee schedule and installment structure.
- Retrieve the linked "Required Transaction details" document (report says extraction failed) to inventory reconciliation fields; do not invent fields.
- Monitor pay-fee-online.php for unauthorized changes; archive snapshots with hashes as an integrity baseline.
- Verify whether muj-payservices.nttdatapay.com/DirectPay/MUFee is linked from any authenticated SLCM page, only in an authorized session.
- Confirm Canara Bank details and the MUVAN account-number rule through institutional channels; never validate via live transfers.
- Authorized, non-production test cases: successful payment, user cancellation, merchant timeout, duplicate callback, refund initiation and failure, reconciliation mismatch, with synthetic identities.
- Publish a canonical payment-route inventory naming provider, merchant name, receipt identifier, refund owner, and escalation contact; provide a public incident-reporting address.
- Watch for lookalike domains and fake QR or email fee requests against the MUJ brand.

## FLAGS
- NTT DATA Pay URL is a search-result lead; the report itself classifies it "public lead, not confirmed end-to-end integration."
- Annual fee PDF figures (Rs 182,750, Rs 261,750) are OCR-garbled hostel annexure values, not course fee schedules.
- Requester stack description (ASP.NET MVC 5.3, IIS 10, Akamai, M365) is externally supplied context, not verified by this report.
- Comparator incidents are not MUJ evidence; no confirmed MUJ payment incident exists in the record.
- The MUVAN account-number construction rule is published on the page; a phishing narrative could reuse it, so verification guidance matters.
- Transaction-details DOCX was unreadable; any claim about its fields would be fabrication.

## COVERAGE
32,089 chars read (file_size bytes), read to EOF, truncated=false confirmed.

DONE w2b-11-pay-fee-online.digest.md

---

## w2b-12-jaipur-main-site.digest

## REPORT
Source file: w2b-12-jaipur-main-site.md (MUJ SLCM Public Surface and Defensive OSINT Report)

## ANSWER SUMMARY
- The official MUJ site uses a large family of human-readable .php URLs; the suffix proves the URL convention only, not a PHP runtime or the SLCM stack.
- The sitemap at https://jaipur.manipal.edu/sitemap.xml is publicly retrievable and lists institutional, academic, admission, faculty, event, compliance, and service routes.
- robots.txt disallows /admin/, /common/, and /content/ for crawlers but explicitly allows images and PDFs to be indexed.
- Public document families: /img/pdf/ (fee documents), /img/pdf/exam/ (examination handbook and timetables), /img/announcement/, and faculty-specific brochure and newsletter paths.
- The fee page names https://mujslcm.jaipur.manipal.edu/ as the student portal and SpaceBasic for hostel and mess fees; the MAHE SIS page (sis.manipal.edu) is a different institutional context.
- A second hostname, https://muj.slcm.jaipur.manipal.edu/, appears in search results with MUJ portal labels; alias or separate deployment is unproven.
- Staff pages publish names plus LinkedIn, IRINS, ORCID, Scopus, Google Scholar, and portfolio links; treated as phishing-enablement data, not proof of compromise.
- Supplied stack fingerprint (ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai, M365) remains unverified; the report calls for a governance-first program.

## KEY FACTS
- https://jaipur.manipal.edu/robots.txt - published crawler directives; PDF and image indexing allowed
- https://jaipur.manipal.edu/sitemap.xml - declared route inventory; exact entry count not established
- https://jaipur.manipal.edu/pay-fee-online.php - SLCM link, SpaceBasic reference, bank details, finance email workflow
- https://jaipur.manipal.edu/examination.php - examination handbook and timetable PDF family under /img/pdf/exam/
- https://jaipur.manipal.edu/faculty-list.php - faculties, schools, departments, and service navigation
- https://jaipur.manipal.edu/muj-faculties.php - publicly listed teaching faculty names
- https://jaipur.manipal.edu/fosta/department-of-information-technology.php - staff profiles with external research links
- https://mujslcm.jaipur.manipal.edu/ - primary portal with "WELCOME TO MUJ PORTAL" and login labels
- https://muj.slcm.jaipur.manipal.edu/ - alternate SLCM hostname; relationship to primary unconfirmed
- https://sis.manipal.edu/index.aspx - MAHE student portal; do not attribute to MUJ
- https://learning.onlinemanipal.com/d2l/home/14042 - MUJ online education login; separate service
- https://muj.onlinemanipal.com/ - Online Manipal MUJ domain; separate identity dependency
- https://admissions.jaipur.manipal.edu/ - homepage Apply Now destination; separate admissions asset
- https://jaipur.manipal.edu/img/pdf/Annual-Fee-Payment-for-the-AY-2026-2027.pdf - public fee PDF path under /img/pdf/
- https://jaipur.manipal.edu/img/pdf/Required Transaction details.docx - fee attachment; office-document metadata risk

## ACTIONABLE LEADS
- Verify whether /admin/, /common/, and /content/ are actually inaccessible, under written authorization only; robots is crawler guidance, not access control.
- Run metadata scrubbing checks on the public PDF families: fee PDFs, exam handbook, announcement PDFs, IT compendium, program brochures.
- Passive DNS and certificate review to test the relationship between mujslcm.jaipur.manipal.edu and muj.slcm.jaipur.manipal.edu (alias vs separate deployment).
- Reconcile the sitemap against CMS and retirement records; look for legacy or orphaned routes.
- Build a canonical service catalog: hostname, service, owner, identity provider, data class, support contact, retirement status.
- Monitor the fee page for unauthorized content changes; set up dual approval and a takedown process for stale documents.

## FLAGS
- .php suffixes do not prove PHP; SLCM runtime claims need authorized evidence.
- Sitemap entry count is intentionally not claimed; the report rejected a noisy parser count.
- The alternate SLCM hostname relationship is an unverified inference; do not report as fact.
- MAHE SIS, Online Manipal, and learning.onlinemanipal.com must stay separate inventory items.
- robots disallow directives provide no confidentiality guarantees.

## COVERAGE
33,142 chars read (file_size bytes), read to EOF, truncated=false confirmed.

DONE w2b-12-jaipur-main-site.digest.md

---

## w2b-13-parents-campus-life.digest

## REPORT
Source file: w2b-13-parents-campus-life.md (MUJ SLCM Parent Surface: Public Evidence and Safe Review)

## ANSWER SUMMARY
- parents.php is a pre-authentication information layer: programs, student affairs, hostels, safety, anti-ragging, helplines, grievance registration, academic calendar; it contains no parent login link.
- The official Parent Portal Login Manual (hosted at /admin/photo/annoncement/49.pdf) documents OTP-based parent access: OTP goes to the registered parent mobile, and unregistered numbers are told to email admissions@jaipur.manipal.edu.
- The manual confirms only academics and examination information on the dashboard under Reports; attendance, fees, hostel, transport, notices, and messaging permissions stay unknown.
- The SLCM login form carries Parent Login and Student Login plus EmailFor, LoginFor, UserName, Password, and a request-verification token; role fields are presentation metadata, not proof of broken authorization.
- A Microsoft password-reset destination is visible in the form capture; consistent with Microsoft identity but not proof of a specific federation design.
- Hostel rules give parents a physical and operational role only: no room entry, cafeteria cash-and-carry meals, city visits need Chief Warden approval plus parent consent, night out needs a parent request on the out-pass.
- Transport evidence is route-to-campus information (distances and RSRTC buses); no dedicated transport page exists in the reviewed sitemap.
- The manual PDF sits under a crawler-disallowed /admin/ path; a documentation and discoverability inconsistency, not an access-control bypass.

## KEY FACTS
- https://jaipur.manipal.edu/parents.php - parent landing page; public info layer before login
- https://jaipur.manipal.edu/admin/photo/annoncement/49.pdf - Parent Portal Login Manual; OTP workflow authority
- https://mujslcm.jaipur.manipal.edu/ - SLCM landing with Parent Login and Student Login
- https://mujslcm.jaipur.manipal.edu/Home/Index - login form structure and @muj.manipal.edu identity label
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - student FAQ; username format, Outlook ID password, admissions-only record changes; do not project onto parents
- https://jaipur.manipal.edu/chiefwardensmessage.php - Chief Warden message and public contacts
- https://jaipur.manipal.edu/faqs-regarding-hostel.php - parent room access ban, cafeteria rule, night-out and medical notification rules
- https://jaipur.manipal.edu/hostel-fees.php - 2026-27 fee table and the no-individual-intimation rule for rule changes
- https://jaipur.manipal.edu/contact-university.php - bus stand, railway, and airport distances; arrival planning only
- https://www.jaipur.manipal.edu/announcement.php - general notice board that hosts the parent manual link
- https://jaipur.manipal.edu/events.php - public events with dates and venues
- https://jaipur.manipal.edu/academics-calender.php - public academic calendar entries
- https://jaipur.manipal.edu/robots.txt - disallows /admin/ while allowing PDF indexing; context for the manual location oddity

## ACTIONABLE LEADS
- Authorized test cases for the parent flow: parent can see only the correctly associated child, role field changes do not grant student rights, OTP retry and lockout behavior, old sessions invalidated at logout.
- Request from the owner a parent role matrix separating grades, attendance, fees, hostel, out-pass, transport, circulars, and messaging per action type.
- Confirm the phone-number update and verification process; the admissions fallback is a social-engineering surface.
- Reconcile the /admin/ robots disallow with the manual hosted under /admin/photo/annoncement/ so the official manual stays reachable and indexed.
- Establish whether night-out and out-pass requests touch any digital system before assuming a portal function.
- Ask General Services or the transport owner about any student bus service; absence from the sitemap is not proof of nonexistence.

## FLAGS
- EmailFor and LoginFor are client-visible routing inputs; the report explicitly refuses any server authorization conclusion.
- Student credential formats from the SLCM FAQ must not be reused to infer parent credentials.
- Parent dashboard scope beyond academics and examination is undocumented; do not add categories.
- The manual is hosted under the crawler-disallowed /admin/ path; that is a governance observation, not a bypass opportunity.
- Alternate SLCM hostname muj.slcm.jaipur.manipal.edu appears in search results; canonical relationship unproven.

## COVERAGE
45,231 chars read (file_size bytes), read to EOF, truncated=false confirmed.

DONE w2b-13-parents-campus-life.digest.md

---

## w2b-14-manipal-edu-group.digest

## REPORT
Source file: w2b-14-manipal-edu-group.md (Manipal Group Portals and the MUJ SLCM Boundary)

## ANSWER SUMMARY
- MAHE's ICT inventory defines SLcM as Student Life Cycle Management replacing the older Academic Management System, with attendance, internal and external marks, result publication, broadcast messages, and a student-and-parent single window.
- The MUJ portal shows student and parent login labels, @muj.manipal.edu wording, and a same-host form with an anti-forgery token; MVC-consistent, but exact versions and Akamai placement are unverified.
- IMA resolves to ICICI Manipal Academy for Banking and Insurance, a joint venture of ICICI Bank and Manipal Global Education Services; not an evidenced SLCM front end.
- CIA currently serves MAHE institutional content with an Apply Now link to apply.manipal.edu; CareerNext serves MIT and MAHE admissions and student-team pages.
- Smart Achievers (HDFC Life) and Young Achievers (Tata AIG) are program-specific EduNxt login surfaces; archived paths for Smart suggest a historical Drupal-style deployment with Seckit.
- Manipal Matters is an e-newsletter with historical WordPress paths (wp-admin, wp-content, xmlrpc.php, category and post parameters).
- No public evidence reviewed proves common SLCM code, tenant, API, or database linking any of the six portals to MUJ SLCM; the correct wording is "not publicly evidenced," not "proven separate."
- Microsoft 365 MX records and MicrosoftOnline realm responses show mail routing and identity management, but do not prove shared application SSO or data.

## KEY FACTS
- http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf - SLCM definition and module inventory baseline
- https://mujslcm.jaipur.manipal.edu/ - MUJ portal labels, form fields, and Microsoft password-reset link
- https://ima.manipal.edu/ - IMA academy identity and contact
- https://cia.manipal.edu/ - current MAHE institutional content surface
- https://careernext.manipal.edu/mitblr.html - MIT admissions content path
- https://edunxt.smartachievers.manipal.edu/ - User Login MAB surface
- https://edunxt.youngachievers.manipal.edu/ - User Login EduNxt surface
- https://manipalbfsi.com/job-ready-programs/hdfc-life-smart-achievers-program - HDFC program purpose
- https://manipalbfsi.com/job-ready-programs/tata-aig-young-achievers-program - Tata AIG program purpose
- https://slcm.manipal.edu/ - MU SLcM branding with 2017 MAHE copyright
- https://sis.manipal.edu/studloginSLCM.aspx - MAHE Information Systems login surface
- https://web.archive.org/cdx/search/cdx?url=edunxt.smartachievers.manipal.edu/*&output=json&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&collapse=urlkey - archived HDFC route and Drupal-style asset paths
- https://web.archive.org/cdx/search/cdx?url=manipalmatters.manipal.edu/*&output=json&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&collapse=urlkey - archived WordPress-era paths
- http://dns.google/resolve?name=muj.manipal.edu&type=MX - Microsoft protection MX record evidence
- http://login.microsoftonline.com/getuserrealm.srf?login=probe@jaipur.manipal.edu&xml=1 - MicrosoftOnline realm response for the Jaipur domain

## ACTIONABLE LEADS
- Ask each portal owner the exact architecture question: is the portal an SLCM client, and if so is it an API integration, SSO trust, replicated data feed, or shared database?
- Passive corroboration for the six hosts: certificate transparency, DNS records, and wayback captures for ownership and retirement timelines.
- Check whether CareerNext .html paths are static files or CMS-generated via passive header inspection, not probing.
- Confirm whether cia.manipal.edu is a redirect, reverse-proxy alias, or separate app through official redirect inventories.
- Archive the NAAC ICT PDF as the SLCM functional baseline for future comparisons.
- Record the supplied stack fingerprint as unverified assessment input until an owner-approved asset inventory confirms it.

## FLAGS
- EduNxt and WordPress path evidence is historical (2014, 2018, 2022 captures); it does not fingerprint current servers.
- MX and realm records establish Microsoft mail or identity management only; shared SSO, tenant, and database remain unproven.
- The report's negative finding is bounded: absence of public integration evidence is not proof of technical separation.
- Exact stack claims (MVC 5.3, .NET 4.x, IIS 10, Akamai) stay requester-supplied hypotheses.
- Similar branding under one parent domain must not be read as shared code or data.

## COVERAGE
43,661 chars read (file_size bytes), read to EOF, truncated=false confirmed.

DONE w2b-14-manipal-edu-group.digest.md

---

## w2c-01-csrf-mvc5.digest

## REPORT (w2c-01-csrf-mvc5.md)
Defensive CSRF assurance assessment for mujslcm.jaipur.manipal.edu, ASP.NET MVC 5 family. No active testing by the report; stack fingerprint and token observation are externally supplied. Verdict INDETERMINATE. 337 lines, 56898 chars, read to EOF, truncated: false.

## ANSWER SUMMARY
- Verdict INDETERMINATE: no MUJ CSRF vulnerability established, safety not established either. A visible `__RequestVerificationToken` cookie and field pair is consistent with correct MVC design but proves nothing by itself.
- MVC requires a correlated pair: session-form cookie token plus non-session form token, matching 128-bit security values, correct roles, username or claim UID binding, MachineKey purpose string AntiForgeryToken.v1. "Field exists" is not the security property.
- Token reuse is expected (per-session generation allowed, serialized format has no timestamp). A finding requires a failed boundary: acceptance after logout, under a second identity, or after a controlled key or deployment change.
- JSON bodies are not covered by the native Request.Form store. Documented contract for Web API style is a custom header plus AntiForgery.Validate with both halves. Test each JSON or AJAX action independently.
- Local login CSRF and Microsoft identity CSRF are separate controls. OIDC needs state, nonce, PKCE where applicable; native MVC forms need local anti-forgery. Neither substitutes for the other.
- Sibling-subdomain cookie planting is a conditional risk multiplier, not an automatic MVC bypass: a valid field token is still required unless a weaker custom handler exists.
- Akamai, SameSite, and IIS are defense in depth. Token-bearing pages should be uncacheable or cache-isolated; multi-node MachineKey consistency matters; SameSite is partial protection only.
- No rejected proposal: report supplies an authorized negative-test matrix (L1-L12 login, M1-M5 identity, P1-P10 post-login) as the decisive evidence path.

## KEY FACTS
- https://github.com/aspnet/AspNetWebStack/tree/main/src/System.Web.WebPages/Helpers/AntiXsrf - reference implementation of the MVC anti-forgery mechanism cited throughout the lifecycle analysis.
- https://github.com/aspnet/AspNetWebStack/blob/main/src/System.Web.WebPages/Helpers/AntiXsrf/TokenValidator.cs - enforces token roles, embedded value match, and identity binding; grounds tests L2-L6 and P2-P3.
- https://github.com/aspnet/AspNetWebStack/blob/main/src/System.Web.WebPages/Helpers/AntiXsrf/AntiForgeryTokenStore.cs - reads cookie and the Request.Form field, so JSON properties are invisible to native validation.
- https://github.com/aspnet/AspNetWebStack/blob/main/src/System.Web.WebPages/Helpers/AntiXsrf/MachineKey45CryptoSystem.cs - MachineKey.Protect with purpose AntiForgeryToken.v1; basis for calling the token protected data, not a bare HMAC.
- https://learn.microsoft.com/en-us/aspnet/web-api/overview/security/preventing-cross-site-request-forgery-csrf-attacks - Microsoft guidance for token pairs and the custom-header transport for Web API style requests.
- https://learn.microsoft.com/en-us/aspnet/mvc/overview/security/xsrfcsrf-prevention-in-aspnet-mvc-and-web-pages - Microsoft warning that built-in anti-XSRF routines do not by themselves prevent login XSRF; RequireSsl control.
- https://github.com/aspnet/AspNetWebStack/blob/main/src/System.Web.WebPages/Helpers/AntiXsrf/AntiForgeryTokenSerializer.cs - serialized token format has no timestamp, supporting the reuse analysis.
- https://github.com/aspnet/AspNetWebStack/blob/main/src/System.Web.WebPages/Helpers/AntiXsrf/AntiForgeryWorker.cs - cookie token reuse and generation behavior across rendered forms.
- https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html - per-session or per-request generation accepted; signed double-submit must bind to the session; caches must Vary on header-based decisions.
- https://portswigger.net/web-security/csrf/bypassing-token-validation - documented flawed patterns: global token pool and cookie-only validation, mapped into the bypass table.
- https://mujslcm.jaipur.manipal.edu/ - the target entry point every test in the matrix is designed against.
- https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow - random state plus equality verification for the authorization-code flow.
- https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html - roles of state, nonce, PKCE; open redirectors can expose authorization codes.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.security.machinekey?view=netframework-4.8.1 - Protect encrypts or signs, so "machine key HMAC" is called an incomplete description.
- https://datatracker.ietf.org/doc/html/rfc6265 - cookie Domain scope and absence of sibling-host integrity guarantees, basis for the subdomain combined-risk model.

## ACTIONABLE LEADS
- Run the login negative matrix on an authorized host: omit field only, omit cookie only, swap roles (L4), cross-profile pair (L5), one-character tamper (L6), pre-login to post-login boundary (L8), duplicate token fields (L11), and record cookie attributes (L12).
- Identity flow checks M1-M5: random state, state rejection before local login, nonce or PKCE, registered callback destinations, SameSite behavior across supported browsers.
- Post-login P1-P10: per-route omission tests, method coverage GET/POST/PUT/PATCH/DELETE, alternate content types, AJAX header transport, token after logout, cache isolation, failure atomicity.
- Inventory every JSON or AJAX endpoint and determine which component extracts the token and whether it calls two-token validation before any side effect.
- Capture wire-level cookie attributes on HTTPS responses and Akamai cache headers (Cache-Control, Age, Vary) for token-bearing pages.
- Confirm MachineKey consistency across origin nodes with the owner before diagnosing intermittent anti-forgery failures.

## FLAGS
- Stack fingerprint (MVC 5.3, Akamai, M365 identity, token pair) is externally supplied; the report performed no live validation.
- Report self-assigns High confidence to framework mechanics and Low to current MUJ status; do not cite it as a vulnerability finding.
- Reuse observations are inconclusive by design: differing ciphertext does not prove one-time semantics and identical strings do not prove insecurity.
- Referenced Akamai docs (refs 30-32) appear in the reference list but are not meaningfully analyzed in the body; RFC 9110 is listed twice (refs 33 and 37).
- The JSON-in-body conclusion is labeled Inference pending an actual handler contract; the report does not claim MUJ has one.
- No live evidence that Akamai shares tokenized responses or that cookies carry broad Domain; those remain test hypotheses.

## COVERAGE
- File read to EOF: 337 lines, 56898 chars (file_size 56898), truncated: false. Confirmed EOF at line 337, final reference.

---

## w2c-02-session-management.digest

## REPORT (w2c-02-session-management.md)
Session-security assessment for mujslcm.jaipur.manipal.edu. Public evidence limited to the landing page; architecture labels externally supplied. Verdict NOT VERIFIED, HIGH PRIORITY TO TEST. 261 lines, 44638 chars, read to EOF, truncated: false.

## ANSWER SUMMARY
- Verdict NOT VERIFIED, HIGH PRIORITY TO TEST. No public evidence of a session defect and no proof that controls are configured correctly. The public page shows only the portal title and sign-in choices.
- Architecture labels are scope assumptions. ".NET Framework 4.x" is too broad for SameSite conclusions because patched 4.7.2 and 4.8 added 2019 SameSite support in December 2019.
- HttpOnly, Secure, and SameSite solve different problems and must be inspected per cookie. Generic System.Web defaults are false for HttpOnly and RequireSSL; session timeout defaults to 20 minutes, Forms Authentication to 30 minutes sliding.
- Fixation is the highest-value lifecycle test: new binding at authentication and privilege change, rejection of unissued and URL-carried IDs. Compare the auth cookie and ASP.NET_SessionId separately because two-cookie rotation can create a false pass.
- Three lifecycles exist: local authentication, System.Web session state, and the Entra SSO session. Passing one layer does not terminate the others; Entra cannot directly revoke an application-issued session token.
- Concurrent login is a policy decision, not automatically a defect. OWASP wants documented rules, active-session visibility, alerts, and remote termination.
- Store choice changes failure mode: InProc loses state on restart, StateServer and SQLServer persist and support farms, Custom is provider-defined. Configuration review beats black-box guessing.
- Proposed plan SLCM-01 through SLCM-11 covers baseline, cookie inventory, regeneration, transport rejection, timeouts, logout replay, concurrency, revocation, store review, and logging.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/Home/Index - the only verified MUJ fact in the report: portal title and sign-in choices.
- https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html - renewal on auth and privilege change, idle and absolute timeouts, session lifecycle logging requirements.
- https://github.com/OWASP/ASVS/blob/master/4.0/en/0x12-V3-Session-management.md - ASVS session requirements used as pass or fail criteria for fixation, logout, and renewal tests.
- https://owasp.org/www-community/attacks/Session_fixation - fixation definition and the new-token-on-authentication requirement.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.sessionstate.sessionidmanager?view=netframework-4.8.1 - ASP.NET_SessionId default name, random 24-character value, and cookieless URL transport capability.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.configuration.sessionstatesection.timeout?view=netframework-4.8.1 - 20-minute session-state default, a review prompt only.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.configuration.formsauthenticationconfiguration.timeout?view=netframework-4.8.1 - 30-minute Forms Authentication default.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.configuration.formsauthenticationconfiguration.slidingexpiration?view=netframework-4.8.1 - sliding renewal after half the configured interval.
- https://learn.microsoft.com/en-us/aspnet/samesite/system-web-samesite - SameSite behavior in classic ASP.NET and the SameSite=None plus Secure pairing rule.
- https://learn.microsoft.com/en-us/entra/identity/users/users-revoke-access - Entra cannot directly revoke application-issued session tokens.
- https://learn.microsoft.com/en-us/previous-versions/aspnet/ms178586%28v%3Dvs.100%29 - four session-state modes: InProc, StateServer, SQLServer, Custom.
- https://pages.nist.gov/800-63-4/sp800-63b/session/ - idle and absolute termination, logout invalidates the binding secret.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.httpcookie.httponly?view=netframework-4.8.1 - HttpOnly semantics and its false default.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.configuration.httpcookiessection.requiressl?view=netframework-4.8.1 - RequireSSL false default.
- http://jaipur.manipal.edu/administration-registrar.php - public registrar contact identified as a reporting channel, not the security owner.

## ACTIONABLE LEADS
- Execute SLCM-01 to SLCM-11 under written authorization: HTTP versus HTTPS baseline, Set-Cookie inventory across the lifecycle, pre and post-login identifier comparison, alternate transport rejection, idle and sliding timeout measurements, absolute timeout, logout replay, concurrent sessions in two owned profiles, password change plus Entra revocation, store configuration review, logging review.
- Record for every sensitive cookie: name, issuing response, Domain, Path, HttpOnly, Secure, SameSite, Expires, Max-Age, and value change at each lifecycle event.
- Check for session identifiers in paths, query strings, hidden fields, or ad hoc headers; require cookie-only transport.
- Verify the old pre-login identifier is unusable after login and that privilege elevation rotates the binding.
- Ask the owner for Web.config sessionState mode and origin topology before inferring a provider from black-box behavior.

## FLAGS
- One citation is broken: "InProc session loss when the AppDomain or worker process is recycled [119 source]" cites reference 119, which does not exist in a reference list ending at 23.
- Row for password change cites "[185 snippet; 200.35]" inside ASVS wording, likely index residue; verify against the actual ASVS text.
- Reference 9 (CAE) uses an http:// scheme while sibling links use https; minor inconsistency.
- All SLCM-specific outcomes are labeled Observed, externally supplied, or Inference; no live testing was performed.
- Concurrency severity is explicitly conditional on MUJ's declared policy, which is unknown.
- Framework defaults (20 and 30 minutes) must not be reported as MUJ findings.

## COVERAGE
- File read to EOF: 261 lines, 44638 chars (file_size 44638), truncated: false. Confirmed EOF at line 261, final reference.

---

## w2c-03-authn-bypass-mvc.digest

## REPORT
Source file: w2c-03-authn-bypass-mvc.md. Authorization and authentication-bypass risk analysis for the MUJ SLCM ecosystem. Framework-reasoning report built from Microsoft and OWASP documentation plus public MUJ pages. Treats all MUJ-specific bypass scenarios as INFERENCE, not findings.

## ANSWER SUMMARY
- Verdict: no publicly substantiated MUJ SLCM authentication bypass identified. Confidence High that public evidence is insufficient to claim a vulnerability; Low to Very Low that any individual pattern is exploitable on MUJ.
- Tech stack (ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Azure AS8075, M365 identity) is a externally supplied premise; the research run did not independently establish versions or AS8075 origin.
- Public login form exposes UserName, Password, hidden __RequestVerificationToken, EmailFor, LoginFor, plus a Forgot Password link to passwordreset.microsoftonline.com; page distinguishes Student and Parent login choices.
- MUJ FAQ confirms SLCM registration URL, name.registration-number username pattern, official Outlook-ID password, and university helpline. Office 365 SOP directs users to Microsoft login with phone, email, and Authenticator security methods.
- Microsoft realm response for probe@muj.manipal.edu returns Microsoft Online federation fields; evidence of M365 identity dependency only, not proof of where final authorization happens.
- Core framework facts: [Authorize] restricts action or controller with [AllowAnonymous] exceptions, conventional MVC route is {controller}/{action}/{id}, Web API uses api/{controller}/{id}, IIS Request Filtering can govern sequences, extensions, hidden segments, verbs, double escaping, and high-bit characters before MVC runs.
- Eight requested bypass patterns (route-parameter tricks, trailing slash, trailing dot/space, backslash, Unicode normalization, case gap, extensionless conflict, static-handler shadow, direct action without [Authorize]) map to /Home/, /Student/, /Staff/, /api/ route guesses, each with a safe verification invariant.
- Recommended next decision: obtain written authorization and source/config access, then build a machine-readable inventory of every MVC action, Web API action, anonymous exception, static handler, and effective policy. No operational payloads appear in the report by design.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/ - the login surface; form field names and Student/Parent choices define the visible trust boundary.
- http://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - FAQ confirming registration URL, name.registration-number username pattern, Outlook-ID password, helpline.
- http://login.microsoftonline.com/getuserrealm.srf?login=probe@muj.manipal.edu&xml=1 - realm probe showing Microsoft Online federation fields for the domain.
- http://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf - Office 365 SOP: Microsoft login service and MFA/security-info methods.
- https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html - deny-by-default, application-wide access control, per-request validation; basis for P0 remediation priorities.
- http://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References - IDOR definition driving the /Student/ ownership analysis.
- https://learn.microsoft.com/en-us/previous-versions/aspnet/dd460317%28v%3Dvs.118%29 - AuthorizeAttribute scope: controller-level, action-level, inheritance, AllowAnonymous.
- https://learn.microsoft.com/en-us/aspnet/mvc/overview/older-versions-1/controllers-and-routing/asp-net-mvc-routing-overview-cs - conventional route with defaults; basis for trailing-separator and extensionless analysis.
- https://learn.microsoft.com/en-us/aspnet/web-api/overview/web-api-routing-and-actions/routing-in-aspnet-web-api - Web API route model; justifies a separate API endpoint inventory.
- https://learn.microsoft.com/en-us/iis/configuration/system.webserver/security/requestfiltering - IIS Request Filtering layers; high-bit character setting documented default true.
- https://learn.microsoft.com/en-us/iis/manage/configuring-security/configure-request-filtering-in-iis - substatus codes 404.5, 404.6, 404.7, 404.8, 404.11, 404.12, 404.14, 404.15 for denial telemetry.
- https://learn.microsoft.com/en-us/dotnet/standard/base-types/best-practices-strings - ordinal comparison recommended for access-control filtering.
- http://learn.microsoft.com/en-us/dotnet/api/system.string.normalize?view=netframework-4.8.1 - Unicode normalization forms C, D, KC, KD.
- https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file - Windows path semantics: backslash separator, terminal space/period warnings.
- https://learn.microsoft.com/en-us/iis/configuration/system.webserver/security/requestfiltering/denyurlsequences - denyUrlSequences configuration for rejected URL sequences.

## ACTIONABLE LEADS
- Request from application owner: effective web.config, URL Rewrite rules, request-filtering configuration, route registrations, reverse-proxy rules; then compute effective policy per action including inheritance and anonymous behavior.
- Follow the 8-phase authorized validation plan: architecture inventory, effective-policy analysis, canonicalization specification, generated route tests, object-authorization tests with synthetic principals and disjoint fixtures, static/dynamic parity review, logging with IIS substatus, CI regression gate that fails unclassified actions.
- Test equivalence classes (trailing slash, trailing dot/space, backslash, Unicode forms, case variants, extensionless routes) only in local or staging environments; capture endpoint, handler, policy, principal, and status before redirect rewriting.
- Keep MVC and Web API inventories separate and make them consume the same service-layer authorization so policy parity is testable.
- Validate M365 claims (issuer, audience, freshness, intended user type) before any local role or object authorization; document the identity-to-role handoff.
- Disclosure trigger: report findings only if source review shows path-prefix authorization, unclassified actions, API filter gaps, or protected files under public roots.

## FLAGS
- Every MUJ-specific mapping (/Home/, /Student/, /Staff/, /api/) is an INFERENCE; the report repeats this label and never claims an observed vulnerability. Do not cite any route family as confirmed.
- Stack premise (MVC 5.3, .NET 4.x, IIS 10, AS8075) is unverified by this report; headers and login-page appearance do not establish application versions.
- References 17-20 cite ASP.NET Core and Kestrel host-filtering docs inside a classic MVC report; refs 18 and 19 are the same Kestrel page in English and Arabic variants, a weak fit and a possible source-list artifact.
- No source code, route table, filter registration, rewrite rules, handler map, or test results were available; framework capability facts do not show MUJ enabled or misconfigured anything.
- Text contains zero operational bypass payloads by design; the report explicitly forbids testing malformed variants against production.

## COVERAGE
- File: w2c-03-authn-bypass-mvc.md.
- 263 lines total; 49,031 bytes on disk; 49,029 chars read.
- Method: read_file offset 1, limit 2000, single call.
- EOF confirmed: final call returned truncated: false, last content line 263 equals total_lines 263.

---

## w2c-04-idor-university-erp.digest

## REPORT (w2c-04-idor-university-erp.md)
Defensive IDOR and BOLA assurance map for an SLCM-class university portal. No public evidence of a MUJ IDOR; no vulnerability finding. Six synthetic test families proposed. 287 lines, 43462 chars, read to EOF, truncated: false.

## ANSWER SUMMARY
- Verdict: IDOR and BOLA is a high-priority defensive assurance area for the described portal class, but public evidence does not prove MUJ uses sequential IDs or has an authorization flaw. The report must not be presented as a penetration-test result.
- Authorization, not identifier shape, is the decision: every endpoint accepting an object reference needs a per-object check. GUIDs are defense in depth, never proof of authority. A sequential ID with a scoped query can be safe.
- Parameterized queries do not solve IDOR (CWE-639 invoice example stays vulnerable without an ownership check). Query safety and authorization safety are separate properties.
- Six object families matter: marks, fee receipts, notifications, documents, timetable, profile. Each has a different subject-object relationship; one generic "logged-in user" rule is insufficient.
- India-linked writeups are mechanism case studies only: the numeric userid increment case (author is a Jamal Mohamed College student, target institution unnamed) and the anonymized financial-records case. Neither establishes proof against MUJ or a named Indian university.
- Microsoft 365 identity authenticates the subject; it does not know local record ownership, parent delegation, course assignment, or finance scope. Authorization must be enforced by the application.
- Validation is safe only with synthetic data: seed records, cross-object negative substitution, no enumeration of live identifiers.
- Regression gates: response confidentiality, state integrity, operation isolation, relationship expiry, property control, alternate representation, error consistency, cache isolation, auditability, CI enforcement.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/Home/Index - public page with separate sign-in and parent-login options, the only verified MUJ fact.
- https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html - per-object access checks, dataset-scoped lookups, avoid identifiers in URLs and POST bodies.
- https://cwe.mitre.org/data/definitions/639.html - user-controlled key selects a record without verifying entitlement; horizontal and vertical escalation.
- https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization - API1 requirement for object-level checks on every object action.
- https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization - API3 property-level authorization, used for the profile-field control.
- https://medium.com/@itcsafsar/idor-vulnerability-exposing-sensitive-student-information-responsible-disclosure-b49694354c6e - numeric userid increment case study for document and record exposure.
- https://in.linkedin.com/in/itcsafsar - author page establishing the Jamal Mohamed College affiliation for attribution limits.
- https://medium.com/@vickyrohith70/how-i-found-an-idor-vulnerability-a-responsible-disclosure-story-def2885bbe0c - anonymized financial-records portal case, no institution or fix status.
- https://hackerone.com/indian_institute_of_techn - IIT response-policy page; proves a disclosure channel exists, not any IDOR case.
- https://www.nuget.org/packages/Microsoft.AspNet.Mvc/5.3.0 - package existence verified; deployment on MUJ not verified.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.mvc.authorizeattribute?view=aspnet-mvc-5.2 - AuthorizeAttribute is a coarse user or role gate; it does not promise record ownership.
- https://learn.microsoft.com/en-us/aspnet/core/security/authorization/resource-based?view=aspnetcore-10.0 - resource-based authorization principle; page documents ASP.NET Core, not MVC 5, so APIs must not be copied.
- http://learn.microsoft.com/en-us/entra/identity-platform/authentication-vs-authorization - authentication versus authorization distinction.
- https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References - two-user and privilege-level testing method.
- https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html - log authorization failures with correlation references, not record contents.

## ACTIONABLE LEADS
- Build AUTHZ-MARK-01 through AUTHZ-PROFILE-01 with synthetic Students A and B, parent A, assigned and unassigned faculty, finance operator, registrar. Substitute only pre-seeded non-owned references; never guess IDs.
- Test operation isolation: read permission must not grant export, update, approve, publish, or delete. Test property-level control on profile fields and mark fields.
- Check file delivery paths: direct storage URLs, pre-signed retrieval links, preview versus download authorization, and cache privacy for personalized responses.
- Test 403 versus 404 consistency to avoid an existence oracle.
- Encode one positive and one negative test per policy row in CI as a release-blocking gate.
- Inventory where object references appear: path, query, form field, JSON body, hidden field, filename, workflow state.

## FLAGS
- Case study 1: target institution unnamed, no independently corroborated remediation; author affiliation is the only India link. Do not cite as a proven Indian university case.
- Case study 2: institution, country, identifier format, and fix status all absent from the cited material.
- Case study 3: IIT HackerOne page establishes policy existence only; no published IDOR case was established.
- MVC 5.3, IIS 10, Akamai, and Microsoft 365 deployment claims are externally supplied; only the NuGet package existence is verified.
- Role matrix and CDN cache claims are explicitly labeled Inference; they are a recommended baseline, not MUJ policy.
- Report intentionally contains no MUJ route names or live identifiers, so all actionable leads are hypothetical object families pending authorization.

## COVERAGE
- File read to EOF: 287 lines, 43462 chars (file_size 43462), truncated: false. Confirmed EOF at line 287, final reference.

---

## w2c-05-register-number-enum.digest

## REPORT (w2c-05-register-number-enum.md)
Register-number predictability assessment for MUJ SLCM based on public PDFs, GitHub projects, and open metadata. Verdict: MATERIAL DEFENSIVE EXPOSURE, NO VERIFIED ENUMERATION OR IDOR. 241 lines, 35582 chars, read to EOF, truncated: false.

## ANSWER SUMMARY
- Username derivation confirmed: official SLCM FAQ publishes `Username: name.registration number` with example garv.2506040062 and ties the password to the official Outlook ID. A register number is part of a predictable login name, not an authentication secret.
- Digit semantics are NOT verified: no legend explains 25, 06, 04, or 0062. Predictability is high at the syntax and username layers, low at the enrollment-allocation layer. Do not publish a decoder.
- Public exposure is narrow but material: one full example sits in an official PDF; the onboarding guide documents the registration-number field and its profile context (name, branch, DOB, phone, email, addresses, parent details, uploaded documents, OTP via parent mobile).
- No bulk register-number lists were verified in circulars, result PDFs, placement pages, or LinkedIn. That negative result is not proof of absence; those channels should be monitored.
- SlcmPlus does local DOM math on attendance, marks, and grades pages without external transmission; it proves sensitive page categories exist, not an IDOR.
- The threat is compositional: public name plus number completes the username; consequences depend on response behavior, MFA, rate limits, and object authorization.
- Account discovery and credential stuffing are more direct consequences than IDOR because the username grammar is public.
- Safe validation uses only synthetic accounts and preapproved identities; no neighboring-number tests, no guessed usernames against production.

## KEY FACTS
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - official FAQ with the username formula, example garv.2506040062, and Outlook password guidance.
- https://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf - registration number is MUJ-generated and non-editable; profile data model with parent mobile OTP.
- https://github.com/Tejas-Narula/SlcmPlus/blob/main/manifest.json - manifest naming three MUJ SLCM page categories: attendance summary, internal marks, grades.
- https://github.com/Tejas-Narula/SlcmPlus/blob/main/content.js - reads attendance counts, marks, credits, letter grades from rendered tables; no external transmission call.
- https://github.com/DK10WS/SLCM_APP - third-party Flutter and FastAPI mobile project advertising schedules, grades, GPA, attendance, custom authentication.
- http://github.com/AddisionS/slcm-feedback-form-filler - automation of the MUJ SLCM feedback form.
- http://github.com/sankalp2004/SLCM-is-Dumb/blob/master/config.py - targets slcm.manipal.edu, not the MUJ Jaipur host; use only as ecosystem context.
- http://github.com/canaryGrapher/slcmAPI/blob/master/package.json - separate Manipal SLcM scraping API, same attribution caveat.
- http://login.microsoftonline.com/muj.manipal.edu/.well-known/openid-configuration - public OpenID metadata linking the muj.manipal.edu namespace to Microsoft login infrastructure.
- https://owasp.org/www-community/attacks/Credential_stuffing - stuffing uses breached username and password pairs; MFA recommended.
- https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html - login, reset, and recovery must not disclose whether an account exists; throttling controls.
- https://pages.nist.gov/800-63-4/sp800-63b.html - controls against online guessing: attempt limits, progressive delays, bot detection, adaptive signals.
- https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html - IDOR definition and per-object access check requirement.
- https://learn.microsoft.com/en-us/entra/identity/authentication/concept-mfa-howitworks - MFA overview used as the primary compensating control argument.
- https://learn.microsoft.com/en-us/entra/identity/authentication/howto-password-smart-lockout - Entra smart lockout as a candidate hardening reference.

## ACTIONABLE LEADS
- Re-verify the FAQ PDF and the example; request replacement of realistic examples with synthetic placeholders and removal of cached copies.
- Run offline scans of jaipur.manipal.edu PDFs, text layers, spreadsheets, public shares, and repository history for name-number pairs.
- Compare login, reset, and recovery responses for preapproved existing versus nonexistent synthetic accounts for message, status, and timing equivalence.
- Authorized review of attendance, marks, grades, profile, document, and parent-facing routes for object-level authorization with synthetic students.
- Ask MUJ for a redacted registration-number legend under authorization; do not infer digit meanings from one example.
- Evaluate MFA coverage, throttling, and breach-based password protection with owner-observed test accounts only.

## FLAGS
- The example number 2506040062 came from the user plus the FAQ; the phrase "password as per official outlook ID" is FAQ-attributed but the report did not re-fetch the PDF. Re-verify before citing.
- All digit-field meanings are Inference or Unknown; the report explicitly forbids presenting a decoder as fact.
- Bulk exposure channels are Not verified; absence in this review is not proof of absence.
- Third-party repos may be stale; anything targeting slcm.manipal.edu must not be attributed to mujslcm.jaipur.manipal.edu.
- Reference 13 is a garbled Devanagari text layer of a MeitY PDF cited for the DPDP Act; the report disclaims legal advice.
- SlcmPlus claims are based on public manifest and content.js only; extension behavior on real pages was not executed by this report.

## COVERAGE
- File read to EOF: 241 lines, 35582 chars (file_size 35582), truncated: false. Confirmed EOF at line 241, final reference.

---

## w2c-06-rate-limit-lockout.digest

## REPORT (w2c-06-rate-limit-lockout.md)
Login-controls assessment for mujslcm.jaipur.manipal.edu based on a passive form capture, framework source, and vendor docs. Verdict INDETERMINATE. 313 lines, 45600 chars, read to EOF, truncated: false.

## ANSWER SUMMARY
- Verdict INDETERMINATE: deployed lockout threshold, counter key, duration, and adaptive logic are unknown. Do not report a vulnerability from framework fingerprints or the absence of a visible initial CAPTCHA.
- Classic ASP.NET Identity 2 provides no turnkey threshold: the lockout duration starts at TimeSpan.Zero and AccessFailedAsync enforces only configured values; PasswordSignInAsync counts failures only when shouldLockout is true.
- Stock EntityFramework UserStore uppercases both sides before lookup and updates failure state by resolved user ID, so ASCII case variants normally converge on one counter. A bypass becomes plausible only if custom code counts on the raw string before resolution.
- Unicode is a separate risk: no normalization in the classic store; UTS #39 confusables are not automatic equality. Unicode tests belong in staging with administrator-created accounts only.
- IP and edge controls are friction, not account protection: OWASP wants account-keyed failure counters because attackers can vary addresses. Akamai documents burst and two-minute average thresholds and a ten-minute penalty box; IIS Dynamic IP Restrictions can block by rate or concurrency.
- Entra Smart Lockout (default ten attempts, initial one-minute lockout, separate familiar and unfamiliar counters) applies only if SLCM actually submits passwords to Entra, which is unproven.
- ASVS 5.0 requires documented controls (6.1.1), implemented controls (6.3.1), and responses that do not reveal valid users (6.3.8). Framework defaults are benchmarks, not MUJ policy.
- Response-only black-box testing cannot attribute a block to any layer; the plan requires correlation IDs and log review before testing.

## KEY FACTS
- http://mujslcm.jaipur.manipal.edu/ - the captured login form: POST with username, password, hidden EmailFor and LoginFor fields, anti-forgery token, Microsoft reset link, @muj.manipal.edu suffix.
- https://github.com/aspnet/AspNetIdentity/blob/main/src/Microsoft.AspNet.Identity.Core/UserManager.cs - lockout properties, zero default duration, AccessFailedAsync logic.
- https://github.com/aspnet/AspNetIdentity/blob/main/src/Microsoft.AspNet.Identity.Owin/SignInManager.cs - shouldLockout gate on the failure path.
- https://github.com/aspnet/AspNetIdentity/blob/main/src/Microsoft.AspNet.Identity.EntityFramework/UserStore.cs - ToUpper username comparison in FindByNameAsync.
- https://learn.microsoft.com/en-us/entra/identity/authentication/howto-password-smart-lockout - Entra defaults, familiar and unfamiliar counters, last three bad password hashes do not increment the counter.
- https://learn.microsoft.com/en-us/iis/manage/configuring-security/using-dynamic-ip-restrictions - IIS Dynamic IP Restrictions and X-Forwarded-For proxy mode.
- https://techdocs.akamai.com/cloud-security/docs/set-protections - rate policy burst and two-minute average thresholds, ten-minute deny, /32 and /64 client scoping.
- https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/03-Testing_for_Weak_Lock_Out_Mechanism - WSTG 3/4/5 attempt progression and the lockable-account rule.
- https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md - ASVS 5.0 items 6.1.1, 6.3.1, and 6.3.8.
- https://github.com/OWASP/ASVS/blob/master/4.0/en/0x11-V2-Authentication.md - ASVS 4.0.3 item 2.2.1, layered controls, no more than 100 failed attempts per hour per account.
- https://pages.nist.gov/800-63-4/sp800-63b.html - 100 consecutive failure ceiling and failure-count reset after successful authentication.
- https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html - account-keyed throttling, generic responses, exponential delay alternative, CAPTCHA as defense in depth.
- http://unicode.org/reports/tr39 - Unicode confusables framework for staging tests.
- https://learn.microsoft.com/en-us/dotnet/standard/base-types/best-practices-strings - Ordinal and OrdinalIgnoreCase guidance and the Turkish i example.
- http://login.microsoftonline.com/getuserrealm.srf?login=probe@muj.manipal.edu&xml=1 - realm metadata probe tying the muj.manipal.edu namespace to Microsoft Online.

## ACTIONABLE LEADS
- Ask the owner for four artifacts before black-box work: login controller call, lockout configuration, user-store implementation, sanitized failure-event log.
- Phase B: with a documented threshold T run T-1 failures plus one valid login, then T failures plus one valid attempt. Production discovery stops at five consecutive failures with 30-second spacing.
- Phase C: after a confirmed lockout measure unlock at 5, 10, and 15 minutes with at most three valid attempts.
- Phase D: ASCII case aggregation, two exact, two uppercase, one mixed-case failure, then a valid attempt; pass requires one account-level counter.
- Phase E: Unicode NFC and NFD equivalence tests in staging only, never production confusables.
- Phase F: two pre-registered institutional egress addresses in staging to prove account-state persistence; never spoof X-Forwarded-For.
- Phase G: observe CAPTCHA trigger stage without solving it; compare responses against an administrator-reserved nonexistent identifier.

## FLAGS
- References 13 and 21 are raw.githubusercontent.com duplicates of references 10 and 2.
- Reference 12 (Akamai terraform rate policy) is listed but the body analysis cites refs 14 and 11; mapping unclear.
- Stack labels are externally supplied; the token name alone does not establish MVC, .NET, or IIS versions.
- "No visible CAPTCHA" supports only the single captured state; adaptive challenges could still exist.
- Entra Smart Lockout behavior applies only if the SLCM password check reaches Entra, which is not established.
- The 30-second spacing and failure caps are plan controls, not claimed MUJ thresholds.

## COVERAGE
- File read to EOF: 313 lines, 45600 chars (file_size 45600), truncated: false. Confirmed EOF at line 313, final reference.

---

## w2c-07-password-reset-flows.digest

## REPORT (w2c-07-password-reset-flows.md)
Password-reset security assessment for the MUJ SLCM portal with Microsoft Entra SSPR delegation. Verdict: recovery entry point verified, delegate and tenant state not established. Overall confidence Moderate. 275 lines, 37774 chars, read to EOF, truncated: false.

## ANSWER SUMMARY
- Verdict: public evidence supports a recovery entry point and a supplied design delegating recovery to Microsoft Entra SSPR. It does not establish an exploitable weakness, nor SSPR scope, methods, role assignments, Conditional Access, writeback, or session revocation.
- SSPR is not enabled for ordinary users by default; scope can be None, Selected, or All. Eligibility and registered methods are checked only after the user enters an identifier and passes CAPTCHA.
- The claimed FAQ sentence (Outlook password equals SLCM password) was not independently located in reviewed public material and must be treated as supplied. If current, one reset spans academic and collaboration services; this drives the highest-severity inference.
- Security questions are a legacy weak point: SSPR-only, prohibited for administrators, guessable, reusable, and OSINT-able. Remove where possible; never the sole recovery gate.
- SMS and voice are restricted by NIST and last-resort per CISA. Method independence and phishing resistance matter more than counting channels on one device.
- AiTM case: stolen session cookies replay past MFA. Reset handling must cover session state, factor binding, and post-reset containment, not just the password.
- Admin reset planes: Password Administrator is the baseline, Global Administrator carries maximum blast radius, temporary passwords never expire until first sign-in. Separate requester proof, password reset, and factor replacement.
- Entra cannot directly revoke application-issued session tokens; containment requires application session invalidation. A Sept 7, 2026 SSPR explicit-registration enforcement is upcoming as of the report date.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/ - portal with @muj.manipal.edu, parent and student login, and a visible Forgot Password option, the only verified MUJ-facing fact.
- https://passwordreset.microsoftonline.com/ - supplied reset destination; the report says the page extraction did not expose the link destination.
- https://learn.microsoft.com/en-us/entra/identity/authentication/concept-sspr-howitworks - SSPR deep dive: enablement defaults, ID plus CAPTCHA first, method registration checks.
- https://learn.microsoft.com/en-us/entra/identity/authentication/tutorial-enable-sspr - None, Selected, All scoping and the admin two-method default.
- https://learn.microsoft.com/en-us/entra/identity/authentication/concept-sspr-policy - administrator policy: two authentication data pieces, security questions prohibited for admins.
- https://learn.microsoft.com/en-us/entra/identity/authentication/concept-authentication-security-questions - question risks, 3 to 40 character answers, no question or answer reuse, migration encouragement.
- https://learn.microsoft.com/en-us/entra/fundamentals/users-reset-password-azure-portal - administrator reset roles and the temporary password that never expires until first sign-in.
- https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/permissions-reference - Helpdesk, User, and Authentication Administrator capabilities and target-dependent limits.
- https://learn.microsoft.com/en-us/entra/identity/users/users-revoke-access - Entra cannot directly revoke an application-issued session token.
- https://www.microsoft.com/en-us/security/blog/2022/07/12/from-cookie-theft-to-bec-attackers-use-aitm-phishing-sites-as-entry-point-to-further-financial-fraud/ - AiTM campaign: password and session cookie theft, MFA bypassed by replay.
- https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html - uniform responses, side channels, rate limits, high-entropy single-use tokens, no auto-login after reset.
- https://pages.nist.gov/800-63-4/sp800-63b/authenticators - PSTN restricted status, one-time out-of-band secrets, authenticator binding on phone replacement.
- https://www.cisa.gov/sites/default/files/publications/fact-sheet-implementing-phishing-resistant-mfa-508c.pdf - CISA guidance: SMS and voice as last resort, push fatigue with number matching.
- https://learn.microsoft.com/en-us/entra/identity/authentication/howto-sspr-reporting - audit event categories and the temporary block after five reset attempts in 24 hours.
- https://techcommunity.microsoft.com/blog/microsoft-entra-blog/whats-new-in-microsoft-entra-june-2026/4517885 - September 7, 2026 explicit-method enforcement and the July 6, 2026 registration campaign.

## ACTIONABLE LEADS
- MUJ-owned configuration review: verify each portal hyperlink, tenant, and Conditional Access; export SSPR scope and administrator policy; inventory Password, Helpdesk, User, Authentication, Privileged Authentication, and Global Administrator assignments.
- Validate the claimed FAQ wording against a current official page and publish a recovery matrix naming each population, identity store, destination, and reset effect.
- Remove security questions; minimize email, SMS, and voice; require number matching on push; prepare for September 2026 explicit method registration.
- Route SSPR and role events to the SIEM with alerts on policy changes, method registration and replacement, blocked attempts, and admin resets.
- Build a compromise playbook: reset, MFA re-registration, token revocation, application session invalidation, mailbox rule and app registration review.
- Review temporary-password delivery: independent identity proofing, never an untrusted or circular channel, and monitoring that the password is replaced at first sign-in.

## FLAGS
- Shared Outlook and SLCM password claim: supplied in the prompt, not independently located in reviewed public material; the report rates it Low to Moderate confidence.
- Reset link delegation: supplied fact; the text extraction did not expose the destination, so the redirect target is not verified from the page itself.
- AiTM, OTP interception, SIM swap, and push-bombing are generic threat patterns, not findings against MUJ.
- Reference 19 duplicates reference 1 under /Home/Index and reference 9 uses an http scheme; minor consistency issues.
- The September 2026 date is forward-dated from the report date of August 25, 2026; re-verify Microsoft guidance before citing.
- All tenant-level conclusions require MUJ administrator confirmation; nothing was tested by the report.

## COVERAGE
- File read to EOF: 275 lines, 37774 chars (file_size 37774), truncated: false. Confirmed EOF at line 275, final reference.

---

## w2c-08-header-hardening.digest

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

---

## w2c-09-tls-config.digest

## REPORT
Source file: w2c-09-tls-config.md (297 lines, 37383 bytes). Public TLS posture of mujslcm.jaipur.manipal.edu from SSL Labs, CT, urlscan, Akamai docs, RFCs.

## ANSWER SUMMARY
- SSL Labs public assessment 2026-08-25: grade B with warnings, endpoint 98.70.14.50, Microsoft-IIS/10.0, TLS 1.0/1.1/1.2 enabled, TLS 1.3 not listed.
- Leaf cert: RSA-2048/SHA-256, single SAN, valid 2025-12-22 to 2026-12-21, issuer Entrust DV TLS Issuing RSA CA 2, chain through Sectigo root R46; OCSP stapling on, CAA absent.
- BEAST true, HSTS absent, compression 0, secure renegotiation on; multiple integer oracle fields (value 1) mean not vulnerable, only BEAST is a positive boolean.
- HTTP/2 via ALPN h2 http/1.1 works, but legacy TLS branches stay; 3DES and static RSA suites offered under TLS 1.0/1.1/1.2.
- Akamai attribution not corroborated: 2026 urlscan records and the SSL Labs test converge on Microsoft AS8075 at 98.70.14.50.
- Modern client simulations pick TLS 1.2 AES-GCM; older profiles pick TLS 1.0 CBC; posture defined by weakest negotiable path.
- Remediation priority: High for protocol hardening, Medium for HSTS/governance, Investigative for architecture attribution.

## KEY FACTS
- https://api.ssllabs.com/api/v3/analyze?host=mujslcm.jaipur.manipal.edu&fromCache=on&maxAge=1000000&all=done&startNew=off : primary machine evidence, grade B, protocol/suite arrays, cert fields.
- https://urlscan.io/api/v1/search/?q=domain:mujslcm.jaipur.manipal.edu : IP/ASN/server history; 2024 record on port 122 with D-Vois, 2026 records on Microsoft AS8075.
- https://api.certspotter.com/v1/issuances?domain=mujslcm.jaipur.manipal.edu&include_subdomains=false&expand=dns_names&expand=issuer&expand=cert : CT record matching SAN, validity start, fingerprints.
- https://mujslcm.jaipur.manipal.edu/Home/Index : landing page with login choices; does not name M365, MVC, or .NET versions.
- https://techdocs.akamai.com/cps/docs/cipher-profiles : Akamai profile scopes; ak-akamai-2020q1 is TLS 1.2/1.3 only, conditional target if property confirmed.
- https://www.rfc-editor.org/rfc/rfc8996.html : TLS 1.0 and 1.1 MUST NOT be negotiated.
- https://datatracker.ietf.org/doc/rfc9113 : h2 requires TLS 1.2+, required GCM suite is present at MUJ.
- https://csrc.nist.gov/pubs/sp/800/52/r2/final : NIST TLS 1.2/1.3 baseline used as modern comparison.
- https://github.com/ssllabs/research/wiki/SSL-Server-Rating-Guide : B cap for TLS 1.0/1.1 and BEAST; guide 2009r dated 2025-05-16.
- https://github.com/ssllabs/ssllabs-scan/blob/master/ssllabs-api-docs-v4.md : field enumeration semantics, vulnBeast definition, 0-RTT value -1 means not performed.
- https://www.sectigo.com/resource-library/sectigo-acquires-entrust-public-certificate-business : explains Entrust issuer naming under Sectigo ownership.
- https://certificate.transparency.dev/ : CT limits; logging is not proof of correct issuance or safety.
- https://urlscan.io/domain/mujslcm.jaipur.manipal.edu : domain-level urlscan listing used for attribution checks.
- https://cabforum.org/working-groups/server/baseline-requirements/requirements : CA/Browser Forum baseline requirements reference.
- https://www.ssllabs.com/projects/ssllabs-apis/index.html : SSL Labs API documentation for method notes.

## ACTIONABLE LEADS
- Owner-authorized retest gate: only TLS 1.2/1.3 listed, no 3DES or TLS_RSA_* suites, vulnBeast false, HSTS valid, CAA present.
- Reconcile DNS, load balancer, Azure/IIS, and any Akamai property before changing policy; attribution precedes remediation.
- If Akamai property confirmed, migrate profile to ak-akamai-2020q1; otherwise harden the Microsoft/IIS termination point.
- Verify M365 and MVC/.NET claims separately via configuration records; do not infer from the TLS dataset.
- Keep automated renewal and CT monitoring; add CAA plus CT alerting.

## FLAGS
- Akamai premise unverified; current public records point to Microsoft, not Akamai.
- Microsoft 365 identity, ASP.NET MVC 5.3, .NET 4.x not established by TLS or landing-page evidence.
- Criteria version mismatch (result 2009q vs guide 2009r) may explain the 3DES/B-grade tension.
- 2024 urlscan used nonstandard port 122 and another provider; not a like-for-like predecessor.
- "Issued 2025-12-22" is notBefore; exact CA transaction time not exposed.
- All findings point-in-time for one resolved endpoint; split-horizon DNS could yield other paths.

## COVERAGE
Chars read: 37383 (full file to EOF, truncated false).

---

## w2c-10-email-spoofing.digest

## REPORT
Source file: w2c-10-email-spoofing.md (297 lines, 41616 bytes). Point-in-time 2026-08-25 passive DNS review of SPF, DKIM, DMARC for jaipur.manipal.edu, manipal.edu, and SLCM.

## ANSWER SUMMARY
- Both domains publish DMARC p=none, so neither requests quarantine or rejection; RFC 9989 tree walk applies Jaipur p=none to mail visible From mujslcm.jaipur.manipal.edu.
- SPF hard fail (-all) on both domains; Jaipur authorizes Outlook plus Brightspace (3 lookup terms), parent adds SendGrid, Salesforce, fixed IPv4 (7 terms).
- Jaipur TXT carries non-versioned SPF-like fragments (ip4:103.139.159.150/32, SendGrid, Outlook, Brightspace text); SPF evaluators discard them, leaving administrative ambiguity.
- MX for both domains points to Microsoft protection hosts; Jaipur selector1 and selector2 return nonempty RSA DKIM keys; manipal.edu selector2 returns a key, selector1 has CNAME but no target TXT key at collection.
- SLCM host: A 98.70.14.50, no TXT answer, no direct _dmarc record; parent DMARC also lacks rua, and RFC 9989 suppresses aggregate reports when rua is absent.
- Lookalikes: manipal-edu.com resolves with p=quarantine and no SPF; manipaledu.com resolves with v=spf1 -all and parked CNAME; .in/.org/.net variants NXDOMAIN.
- Recommended path: measured none to quarantine to reject after reporting and sender inventory, per Microsoft staged guidance.

## KEY FACTS
- https://dns.google/resolve?name=jaipur.manipal.edu&type=TXT : hard-fail SPF plus confusing non-versioned fragments.
- https://dns.google/resolve?name=_dmarc.jaipur.manipal.edu&type=TXT : p=none with rua mailbox, monitoring only.
- https://dns.google/resolve?name=manipal.edu&type=TXT : parent SPF with four third-party includes.
- https://dns.google/resolve?name=_dmarc.manipal.edu&type=TXT : p=none, no rua destination.
- https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=A : SLCM resolves to 98.70.14.50.
- https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=TXT : NOERROR with no answers, no direct policy.
- https://dns.google/resolve?name=_dmarc.mujslcm.jaipur.manipal.edu&type=TXT : NXDOMAIN, no direct DMARC owner name.
- https://dns.google/resolve?name=jaipur.manipal.edu&type=MX : jaipur-manipal-edu.mail.protection.outlook.com.
- https://dns.google/resolve?name=selector1._domainkey.jaipur.manipal.edu&type=TXT : nonempty RSA DKIM key returned.
- https://dns.google/resolve?name=selector2._domainkey.manipal.edu&type=TXT : parent selector2 key returned.
- https://dns.google/resolve?name=selector1._domainkey.manipal.edu&type=TXT : CNAME present, no key returned; rotation review item.
- https://dns.google/resolve?name=manipal-edu.com&type=A : lookalike resolves to two addresses.
- https://dns.google/resolve?name=_dmarc.manipal-edu.com&type=TXT : lookalike publishes p=quarantine with onsecureserver.net reporting.
- https://www.rfc-editor.org/rfc/rfc9989.html : parent policy discovery and rua suppression rules.
- https://learn.microsoft.com/en-us/defender-office-365/email-authentication-dmarc-configure : staged none to quarantine to reject migration framework.

## ACTIONABLE LEADS
- Add an authorized rua destination to _dmarc.manipal.edu before any enforcement step.
- Inventory every legitimate sender under the parent SPF; validate SPF result, DKIM d=, and DMARC alignment on real outbound headers.
- Resolve intent of Jaipur TXT fragments with mail-flow owners, then remove or consolidate.
- For confirmed non-sending hosts such as SLCM, publish explicit v=spf1 -all and a direct enforcing DMARC record after dependency checks.
- Stage Jaipur to quarantine then reject using existing rua telemetry; revisit parent later due to broader scope.
- Bounded lookalike monitoring plus FIDO/WebAuthn for high-risk identities per CISA.

## FLAGS
- Parent selector1 missing TXT key may be a normal inactive/rotation state; DNS alone cannot decide.
- SPF lookup-term counts are point-in-time; provider policy changes shift them.
- Lookalike ownership and intent unknown; NXDOMAIN results are volatile.
- No claim of observed abuse; this is posture analysis only.
- DNS is volatile; records should be re-queried before remediation or publication.

## COVERAGE
Chars read: 41616 (full file to EOF, truncated false).

---

## w2c-11-subdomain-takeover.digest

## REPORT
Source file: w2c-11-subdomain-takeover.md (243 lines, 37007 bytes). Dangling DNS and subdomain takeover eligibility review for MUJ SLCM and admissions hosts.

## ANSWER SUMMARY
- mujslcm.jaipur.manipal.edu has a direct A record to 98.70.14.50 (TTL 3600), no CNAME answer, and serves a live MUJ portal; no dangling-CNAME pattern.
- admissions.jaipur.manipal.edu CNAMEs to jaipurmanipal.nopaperforms.com, resolving through prodvpc-web-lb4-593721465.ap-south-1.elb.amazonaws.com to three A addresses; official MUJ admissions page is live.
- NoPaperForms custom-hostname verification, quarantine, and release rules are not publicly documented; ownership must be confirmed in writing by vendor and MUJ.
- Akamai premise not established by current SLCM DNS; Akamai docs describe property hostname to edge hostname CNAME mapping, and the observed record is a direct A.
- No named Indian university takeover was substantiated from the public record; Abusix 2024 article supplies international analogues (UC San Diego, UCLA, Georgetown, UC Davis, Alicante, La Verne), all via expired external target domains.
- Provider controls differ: Azure asuid TXT and GitHub custom-domain verification reduce re-binding; Heroku frees custom domains on app destroy.
- Verdict: no present reportable takeover; residual risk is future offboarding and vendor lifecycle, plus DNS-first decommissioning gaps.

## KEY FACTS
- https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=A : direct A answer 98.70.14.50, TTL 3600.
- https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=CNAME : successful query, no CNAME answer.
- https://dns.google/resolve?name=admissions.jaipur.manipal.edu&type=CNAME : CNAME to jaipurmanipal.nopaperforms.com, TTL 2387.
- https://dns.google/resolve?name=admissions.jaipur.manipal.edu&type=A : chain terminates via AWS ELB at three addresses.
- https://admissions.jaipur.manipal.edu/ : live MUJ UG/PG/PhD admissions page for 2026-27.
- https://mujslcm.jaipur.manipal.edu/ : live portal with sign-in and parent login options.
- https://learn.microsoft.com/en-us/azure/security/fundamentals/subdomain-takeover : Azure dangling DNS definition and asuid TXT ownership control.
- https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages : disabled Pages site with DNS left in place is takeover risk.
- https://devcenter.heroku.com/articles/custom-domains : destroying an app frees its custom domains for reassignment.
- https://cheatsheetseries.owasp.org/cheatsheets/Subdomain_Takeover_Prevention_Cheat_Sheet.html : orphaned reference plus provider claimability are the two necessary conditions.
- https://abusix.com/blog/dangling-cname-attacks-and-sub-domain-takeovers : international higher-education analogues via expired target domains.
- https://hackerone.com/reports/665398 : datacafe-cert.starbucks.com Azure reclamation case, rated High 7.5, disclosed August 2019.
- https://dns.google/resolve?name=selector1._domainkey.jaipur.manipal.edu&type=CNAME : Microsoft 365 DKIM CNAME to mujcampus.onmicrosoft.com, a mail control, not a web app CNAME.
- https://cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf : covered entities report Annexure I incidents within six hours; legal category is counsel's call.
- https://techdocs.akamai.com/property-mgr/reference/modify-property-hostnames : documented property hostname to edge hostname mapping model.

## ACTIONABLE LEADS
- Ask NoPaperForms five control questions: ownership proof, competing tenant requests, tenant deletion behavior, quarantine or reservation, certificate/log/approval handling; get answers naming the MUJ tenant.
- Inventory all CNAME, NS, MX, and external registrable-domain dependencies under jaipur.manipal.edu with owners and expiry.
- Enforce DNS-first decommissioning gate: remove DNS, wait TTL, then delete the resource.
- Retain Azure asuid and GitHub verification TXT records as long as hostnames are delegated; eliminate wildcard DNS.
- Monitor CNAME chains, response codes, certificate transparency, and content hashes; keep evidence packages ready for incident response.
- Do not register expired targets, create cloud resources, or publish proof content without written authorization.

## FLAGS
- Akamai, ASP.NET MVC 5.3, .NET 4.x, IIS 10 are externally supplied context, not verified in this DNS dataset.
- NoPaperForms controls are Unknown; absence of documentation is not proof of claimability.
- Indian takeover stories cited only from unattributed posts; do not repeat them as cases.
- Active DNS chain does not prove durable tenant reservation; only vendor and owner confirmation can.
- A valid certificate on a hijacked subdomain is possible; TLS is corroboration, not a verdict.

## COVERAGE
Chars read: 37007 (full file to EOF, truncated false).

---

## w2c-12-clickjacking-frames.digest

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

---

## w2c-13-open-redirect-mvc.digest

## REPORT
Source file: w2c-13-open-redirect-mvc.md (292 lines, 41318 bytes). Analysis of the reported ReturnUrl to enc to /Home/Index login flow in an ASP.NET MVC context.

## ANSWER SUMMARY
- No publicly demonstrated open redirect; the ReturnUrl to enc flow is a brief-supplied observation with no raw samples or server source, so implementation status is UNKNOWN.
- enc token syntax cannot reveal semantics: Base64, base64url, and ASP.NET UrlTokenEncode look alike; candidates include plaintext, MachineKey.Protect output, HMAC, forms ticket, opaque server-side handle.
- Url.IsLocalUrl rejects null, empty, absolute URLs, //host, and /\host forms; accepts / and ~/; it does no host comparison, so a route allowlist must follow it.
- Microsoft's classic MVC case: Redirect(returnUrl) without validation is the vulnerable pattern; the repair is Url.IsLocalUrl plus a fixed Home/Index fallback.
- Cryptographic protection proves tamper evidence, not destination safety; validation must happen after the final decode, before the redirect sink.
- Entra redirect_uri must match a registered value; callback handoff and post-callback continuation are two separate boundaries, and RFC 9700 bars open redirectors in OAuth clients.
- Escalation requires owner-authorized source or staging proof of an external redirect; otherwise report as a review item only.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/Home/Index : public landing showing "WELCOME TO MUJ PORTAL" and sign-in options.
- https://github.com/Tejas-Narula/SlcmPlus/blob/main/manifest.json : third-party extension manifest naming attendance, internal marks, and grades routes; client-side only.
- https://learn.microsoft.com/en-us/aspnet/mvc/overview/security/preventing-open-redirection-attacks : vulnerable and repaired MVC redirect patterns.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.security.machinekey.protect?view=netframework-4.8.1 : purpose-bound byte protection; unprotect requires matching purpose.
- https://github.com/aspnet/AspNetWebStack/blob/main/src/System.Web.WebPages/RequestExtensions.cs : IsUrlLocalToHost string-prefix logic, the core of Url.IsLocalUrl.
- https://github.com/aspnet/AspNetWebStack/blob/main/src/System.Web.Mvc/RedirectResult.cs : constructor only rejects null or empty; no safety wrapper.
- https://github.com/aspnet/AspNetWebStack/blob/main/src/System.Web.Mvc/UrlHelper.cs : delegation of IsLocalUrl to RequestExtensions.
- https://learn.microsoft.com/en-us/entra/identity-platform/reply-url : responses go only to registered reply URIs.
- https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow : state should be a random unique value, not URLs or sensitive data.
- https://www.rfc-editor.org/rfc/rfc9700.html : OAuth clients must not expose open redirectors; code or token exfiltration risk in relevant flows.
- https://www.rfc-editor.org/rfc/rfc4648.html : Base64 encodes arbitrary octets; base64url uses - and _.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.httpserverutility.urltokenencode?view=netframework-4.8.1 : URL-token encoding for arbitrary bytes.
- https://url.spec.whatwg.org/ : backslash treated specially for HTTP(S)-style URLs, the parser differential behind the /\ rule.
- https://owasp.org/www-community/attacks/open_redirect : open redirect defined as redirection to a externally supplied unvalidated destination.
- https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html : route ID or token mapped server-side with warning page.

## ACTIONABLE LEADS
- Owner-authorized server code review: find the enc assignment (serializer, Protect call, purpose strings) and the consumption path (decode, unprotect, expiry, IsLocalUrl, redirect sink).
- Offline classification of already-held samples: length, alphabet, padding, URL escaping; local decode only.
- Local or staging unit tests across the full separator matrix (null, /, ~/, //host, /\host, absolute, encoded forms).
- Verify farm-wide MachineKey protection state without leaking configuration values.
- Preferred design: protected route ID to server mapping to RedirectToAction with fixed fallback; log reason codes, never raw tokens.
- Without authorization, publish a framework-level risk assessment, not a vulnerability claim.

## FLAGS
- MachineKey, Base64, and HMAC hypotheses all rated Low for evidence; framework analysis is High, MUJ implementation is Low.
- Third-party extension is client-side and carries no server redirect logic.
- No raw samples supplied; the reported flow was not reproduced.
- Public client repositories are not substitutes for server code.
- Same-host absolute URL exceptions add parser risk; the classic helper rejects absolute form deliberately.

## COVERAGE
Chars read: 41318 (full file to EOF, truncated false).

---

## w2c-14-file-upload-surfaces.digest

## REPORT
Source file: w2c-14-file-upload-surfaces.md (327 lines, 39635 bytes). Upload risk assessment for MUJ SLCM based on public pages, a 2019 comparative manual, and OWASP/Microsoft/IETF guidance.

## ANSWER SUMMARY
- No public vulnerability is established; the MUJ FAQ confirms SLCM registration and mandatory-document questions but exposes no upload endpoint or route.
- Orientation page lists marksheets, certificates, passport photo, Aadhaar, APAAR ID, affidavits, and medical certificate; the workflow is the highest-privacy document set if any part is digitized.
- A third-party 2019 SLCM manual describes mandatory JPEG/PDF uploads up to 2 MB, view/delete/re-upload, a general Files area, and a JPEG profile picture up to 250 KB; comparative hypotheses only.
- Client filenames and declared Content-Type are untrusted: HttpPostedFileBase.FileName carries the client path, OWASP says Content-Type is spoofable; use opaque server IDs plus escaped display metadata.
- ASP.NET defaults: max request 4 MB (MaxRequestLength 4096 KB), 256 KB disk buffer threshold; IIS maxAllowedContentLength default 30,000,000 bytes; limits must be aligned per layer.
- Download side: RFC 6266 filenames are advisory; resolve as record ID to server key with re-authorization on every retrieval; serve with attachment and nosniff from an isolated origin.
- Verdict: high-priority authorized internal review; no demonstrated bypass, traversal, malware, or unauthorized access at MUJ.

## KEY FACTS
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf : SLCM FAQ; portal URL, Outlook-linked credentials, mandatory-document question, no upload route described.
- https://www.jaipur.manipal.edu/induction-orientation-program.php : mandatory document list with privacy and impersonation significance.
- https://idoc.pub/documents/slcm-mit-usermanual-x4e6zjd7v8n3 : 2019 comparative manual; 2 MB JPEG/PDF, Files area, 250 KB profile picture.
- https://mujslcm.jaipur.manipal.edu/Home/Index : public landing only; no upload surface visible.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.httppostedfilebase.filename?view=netframework-4.8.1 : FileName is the fully qualified client name including path.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.httppostedfilebase.saveas?view=netframework-4.8.1 : SaveAs writes to the application-chosen destination name.
- https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html : layered validation; Content-Type spoofing, signature limits, CDR, storage outside web root.
- https://learn.microsoft.com/en-us/iis/configuration/system.webServer/security/requestFiltering/requestLimits/ : IIS maxAllowedContentLength default around 28.6 MB.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.configuration.httpruntimesection.maxrequestlength?view=netframework-4.8.1 : HttpRuntime default 4096 KB, units in kilobytes.
- https://www.rfc-editor.org/rfc/rfc7578 : multipart forms may carry arbitrary executable content.
- https://www.rfc-editor.org/rfc/rfc6266 : received filename is advisory; discard path components and special names.
- https://mimesniff.spec.whatwg.org/ : image versus HTML misread can lead to script execution.
- https://docs.gitlab.com/releases/patches/patch-release-gitlab-16-0-1-released/ : GitLab 16.0.0 attachment traversal CVSS 10.0, unauthenticated arbitrary file read, fixed 16.0.1.
- https://nvd.nist.gov/vuln/detail/cve-2021-41773 : Apache 2.4.49 normalization flaw, RCE when CGI enabled.
- https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload : attachment content-disposition and nosniff for static file responses.

## ACTIONABLE LEADS
- Authorized staging feature inventory per role: upload, preview, download, replace, delete, export, and transformation paths.
- Negative matrix: extension and MIME mismatch, ambiguous names, image re-encode, PDF active-feature policy, request-size boundaries, archive entry and expansion budgets, cross-account opaque ID, role matrix, download headers, scanner outage fail-closed, CSRF, retention and legal hold.
- Quarantine, AV, sandbox/CDR pipeline with explicit state machine; isolated delivery origin without portal cookies.
- Align IIS, ASP.NET, and business size limits per document type; one business limit per feature.
- Governance: retention by document type, deletion propagation, reviewer access, exception approval.
- No production testing and no real student documents without written authorization.

## FLAGS
- 2019 manual is third-party, dated, and not current MUJ proof; current digital upload capability rated Medium-low.
- Fee-proof upload is unverified; no first-party MUJ page confirms it.
- MVC 5.3 is plausible via NuGet Microsoft.AspNet.Mvc 5.3.0, not proof of MUJ deployment.
- IIS 10, Akamai, and Microsoft 365 details not independently confirmed.
- GitLab and Apache cases are regression lessons, not evidence against MUJ.

## COVERAGE
Chars read: 39635 (full file to EOF, truncated false).

---

## w2c-15-payment-flow-manipulation.digest

## REPORT
Source file: w2c-15-payment-flow-manipulation.md (316 lines, 43158 bytes). Defensive fee-payment integrity assessment for MUJ SLCM based on vendor docs, OWASP guidance, and Indian education case reports.

## ANSWER SUMMARY
- No evidence in cited public material that MUJ SLCM is vulnerable to fee manipulation, receipt IDOR, callback forgery, or refund abuse; the only supported target fact is three sign-in choices on the portal.
- Razorpay pattern: server-created order, amount in smallest currency sub-unit, mandatory HMAC-SHA256 completion signature, service only after capture; webhooks can duplicate and arrive out of order, identified by x-razorpay-event-id.
- BillDesk pattern from a WhatsApp-specific Meta guide: HMAC or JOSE client auth with JOSE preferred, unique merchant order, transaction object posted to return URL; guide is illustrative only.
- CCAvenue Integration Document v3.3 (Nov 2021): merchant working key, encrypted request, order_id uniqueness is merchant responsibility because the vendor does not check it.
- Indian cases: CBSE June 2026 official release says attacks mitigated and no data breach while Telegraph reports unauthorized payment access involving about 50 students; Sai Nath clone diverted INR 32,000; GBU FIR alleges over INR 5 crore with fake UPI entries; none prove an MUJ defect.
- IT Act Sections 43 and 66 tie testing legality to owner permission and intent; written scope and staging are mandatory.
- Verdict: staging-only assessment with synthetic identities and a gateway sandbox; production returns, receipts, orders, callbacks, and refunds are off limits.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/ : portal shows Sign In @muj.manipal.edu, Parent Login, Student Login.
- https://razorpay.com/docs/payments/server-integration/java/integration-steps/ : server order creation, sub-unit amount, mandatory signature verification, captured status before delivery.
- https://razorpay.com/docs/webhooks/validate-test/ : raw-body HMAC, duplicate events, unordered delivery.
- https://razorpay.com/docs/api/refunds/ : refunds only for captured payments; uncaptured authorizations auto-refund after three days.
- https://links.avenues.info/downloads/CCAvenue_Integration_Ver_3_3.pdf : merchant_id, order_id, currency, amount, redirect_url, cancel_url fields; vendor does not enforce order uniqueness.
- https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/upi-intent/pg-guide-billdesk : BillDesk HMAC or JOSE, unique order ID, return URL mechanics; WhatsApp-specific.
- https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html : deny by default, permission validation on every request, relationship-aware checks.
- https://cheatsheetseries.owasp.org/cheatsheets/Business_Logic_Security_Cheat_Sheet.html : idempotency key stored with result, cached result on retry.
- https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References : IDOR definition, direct object access via externally supplied identifiers.
- https://www.cbse.gov.in/cbsenew/documents/Press_Release_Complaint_PVR_05062026.pdf : CBSE June 2026 statement, mitigated attacks, no data compromise.
- https://www.telegraphindia.com/india/cbse-revaluation-portal-system-hit-by-malicious-attack-of-50-students-with-unauthorised-access/cid/2163149 : secondary report of unauthorized payment-system access by about 50 students.
- https://the420.in/sai-nath-university-fake-website-student-fraud-agra/ : cloned university site allegedly diverted INR 32,000.
- https://timesofindia.indiatimes.com/city/noida/fir-against-ex-gbu-registrar-accounts-officer-for-rs-5-crore-fee-fraud/articleshow/130197794.cms : GBU FIR, fake UPI entries in university software; allegation only.
- https://www.indiacode.nic.in/bitstream/123456789/13116/1/it_act_2000_updated.pdf : IT Act Sections 43 and 66 permission and intent conditions.
- https://www.cert-in.org.in/RVDCP.jsp : CERT-In responsible vulnerability disclosure and coordination policy.

## ACTIONABLE LEADS
- Run an architecture review first: actual gateway from contracts, role-to-object matrix, sequence diagrams, and a single agreed data-flow diagram.
- Sandbox test matrix: order creation from ledger, amount and currency mismatch, cross-account order binding, non-authoritative browser return, raw-body webhook signature, duplicate and out-of-order replay, receipt IDOR, refund limits with maker-checker, concurrency, callback outage reconciliation.
- Implement one server-side settlement service with unique internal, gateway, payment, and processed-event keys and a monotonic state machine ending in Posted or Refunded.
- Monitoring signals: amount or currency mismatch, unknown or reused order, invalid signature, repeated event ID, refund near original amount, gateway captured but ERP pending, lookalike payment domains.
- Disclose through the university-approved channel and CERT-In when applicable; do not share without university approval.

## FLAGS
- Gateway vendor for MUJ is unverified; Razorpay, BillDesk, and CCAvenue patterns are references, not findings.
- CBSE narrative conflict: official no-breach statement versus Telegraph unauthorized access reporting; do not infer a technical root cause.
- GBU FIR is an allegation, not a technical finding or adjudication.
- BillDesk guide is WhatsApp-specific and not comprehensive.
- CCAvenue document is from 2021; it does not prove MUJ's current configuration.
- No authorized dynamic testing was performed; MUJ-specific vulnerability status is not assessed.

## COVERAGE
Chars read: 43158 (full file to EOF, truncated false).

---

## w2c-16-ssrf-mvc.digest

## REPORT
Source: research/w2c-16-ssrf-mvc.md

## ANSWER SUMMARY
- No public evidence that MUJ SLCM offers image-by-URL import, webhooks, URL-to-PDF, or XML processing. SSRF not established.
- Four candidate sink classes: image URL import, webhook/callback, URL-to-PDF renderer, XML external resource. Each has a different failure mode.
- .NET Framework 4.x details decide risk: AllowAutoRedirect defaults true, XmlResolver null default since 4.5.2, XmlTextReader 4.0-4.5.2 defaults DtdProcessing.Parse.
- IIS ARR and Akamai are ingress controls; neither constrains application-originated egress. Deny-by-default routing required.
- Redirect validation gap: first-URL-only checks fail when HttpWebRequest follows redirects by default.
- Test policy is authorization-first: written scope, passive inventory, static review, isolated unit tests, one owner-controlled staging callback per sink.
- Hard-deny destination classes: loopback, RFC 1918, link-local, IPv6 ULA/link-local, cloud metadata, third-party hosts.
- Verdict: SSRF review justified as defensive design exercise; no vulnerability claim against MUJ.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/Home/Index : only target-specific evidence, portal with institutional and parent sign-in.
- https://mujslcm.jaipur.manipal.edu/ : root page, same evidence boundary.
- https://owasp.org/Top10/2021/A10_2021-Server-Side_Request_Forgery_%28SSRF%29 : SSRF definition, positive allowlist and deny-by-default guidance.
- https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html : image and webhook sink patterns, IPAddress.TryParse and DNS rebinding caveats.
- https://learn.microsoft.com/en-us/dotnet/api/system.net.httpwebrequest.allowautoredirect?view=netframework-4.8.1 : redirects on by default, MaximumAutomaticRedirections.
- https://learn.microsoft.com/en-us/dotnet/api/system.net.httpwebrequest.proxy?view=netframework-4.8.1 : proxy inheritance, local bypass, direct connection paths.
- https://learn.microsoft.com/en-us/dotnet/api/system.xml.xmlreadersettings.xmlresolver?view=netframework-4.8.1 : null resolver default since 4.5.2.
- https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html : XXE prevention, parser defaults by framework version.
- https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#security : renderer retrieves HTTPS and file:// resources, custom fetcher advice.
- https://www.iana.org/assignments/iana-ipv4-special-registry/iana-ipv4-special-registry.xhtml : IPv4 loopback, private, link-local classification for deny policy.
- https://www.iana.org/assignments/iana-ipv6-special-registry/iana-ipv6-special-registry.xhtml : IPv6 loopback, ULA, link-local classification.
- https://learn.microsoft.com/en-us/iis/extensions/url-rewrite-module/reverse-proxy-with-url-rewrite-v2-and-application-request-routing : IIS ARR is inbound reverse proxying only.
- https://www.akamai.com/glossary/what-is-server-side-request-forgery : Akamai describes SSRF as server-side pivot.
- https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf : NIST SP 800-115 plan requirements.
- https://csrc.nist.gov/pubs/sp/800/115/final : assessment plan, scope, prohibited activities, incident handling.

## ACTIONABLE LEADS
- Under authorization only: trace MVC action params, model-bound fields, webhook settings, queue messages into outbound request and XML APIs.
- Source review for WebRequest.Create, HttpWebRequest, WebClient, HttpClient, renderer and XML resolver sinks.
- Staging policy tests with mocks: redirects, schemes, IPv4/IPv6 answers, DNS changes.
- Owner-run benign callback once per sink with ROE limits: image, webhook, PDF render, XML mock.
- Inspect proxy and egress config; verify AllowAutoRedirect and XmlResolver settings in deployed config.
- Akamai/WAF rules for detection only; never the sole SSRF control.

## FLAGS
- All four sink features unverified at target; report says no public evidence any exists.
- Stack labels (MVC 5.3, .NET 4.x, IIS 10, Akamai, M365) requester-supplied, not independently verified.
- WeasyPrint and wkhtmltopdf cited as generic renderer examples; no evidence MUJ uses either.
- Report explicitly rejects converting technology fingerprint into vulnerability claim; treat all target conclusions Low confidence.
- Reference [18] wkhtmltopdf URL present but not used in body claims.

## COVERAGE
- Chars read: 37745. EOF confirmed via read_file truncated:false.

---

## w2c-17-deserialization-net.digest

## REPORT
Source: research/w2c-17-deserialization-net.md

## ANSWER SUMMARY
- No confirmed MUJ deserialization vulnerability. Public evidence is a portal landing page with sign-in and parent login.
- BinaryFormatter is unsafe by design per Microsoft, cannot be made secure, causes DoS, disclosure, or RCE in process context.
- MVC 5.3 does not prove BinaryFormatter or ViewState use; package existence verified, deployment not.
- ViewState is a WebForms .aspx mechanism; relevant only if .aspx remnants exist or share machineKey config.
- ViewState MAC enforcement is non-disableable since advisory 2905247; machineKey integrity is the gate.
- Microsoft Dec 2024 incident: one public static key used for code injection in IIS worker process; 3000+ disclosed keys flagged.
- Observed value 4.7.4136.0 is not a patch inventory; registry Release DWORD is the supported method.
- ysoserial.net formatter support is capability evidence, not target evidence.
- Verdict: plausible conditional risk, no confirmed MUJ deserialization vulnerability.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/ : only target-specific evidence.
- https://learn.microsoft.com/en-us/dotnet/standard/serialization/binaryformatter-security-guide : BinaryFormatter danger, removal guidance.
- https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca2300 : CA2300 insecure deserializer rule.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.ui.losformatter?view=netframework-4.8.1 : LosFormatter serializes WebForms ViewState, insecure.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.ui.objectstateformatter?view=netframework-4.8.1 : can fall back to BinaryFormatter for ISerializable types.
- https://github.com/pwntester/ysoserial.net : formatter and gadget capability evidence only.
- https://support.microsoft.com/en-US/servicing/DotNetFramework/troubleshooting/resolving-view-state-message-authentication-code-mac-errors : ViewState MAC behavior, farm key consistency.
- https://www.microsoft.com/en-us/security/blog/2025/02/06/code-injection-attacks-using-publicly-disclosed-asp-net-machine-keys : Dec 2024 incident, 3000+ disclosed keys, rotation advice.
- https://learn.microsoft.com/en-us/security-updates/securityadvisories/2013/2905247 : MAC validation made non-disableable.
- https://learn.microsoft.com/en-us/dotnet/framework/install/how-to-determine-which-versions-are-installed : registry Release method, Environment.Version warning.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.ui.page.viewstateuserkey?view=netframework-4.8.1 : ViewStateUserKey binding, Page_Init requirement.
- https://www.nuget.org/packages/Microsoft.AspNet.Mvc : MVC 5.3.0 package exists, targets .NET 4.5+.
- https://learn.microsoft.com/en-us/dotnet/standard/serialization/binaryformatter-migration-guide : migration to System.Text.Json, DataContractSerializer, MessagePack, protobuf-net.
- https://learn.microsoft.com/en-us/iis/configuration/system.applicationhost/sites/site/tracefailedrequestslogging : failed request tracing requires role service and enablement.
- https://www.akamai.com/products/app-and-api-protector : WAF is compensating control, not a serializer fix.

## ACTIONABLE LEADS
- Owner-authorized SAST inventory for BinaryFormatter, IFormatter, Deserialize, ISerializable, SerializationBinder, SoapFormatter, NetDataContractSerializer, LosFormatter, ObjectStateFormatter.
- Data-flow trace from HTTP, cookies, files, queues, caches, databases into each sink.
- WebForms remnant inventory: .aspx list, master pages, PageStatePersister subclasses, effective ViewState config.
- machineKey provenance review: repository history, secret scans, compare fingerprints with Microsoft hash list, rotate exposed keys.
- Verify framework via registry Release, OS build, cumulative updates; banner is correlation only.
- IIS failed-request tracing as detection with privacy and retention policy.

## FLAGS
- 4.7.4136.0 is a supplied observation with no authoritative mapping; report refuses CVE or patch verdicts from it.
- MVC 5.3 verified only as NuGet package existence; IIS 10, Akamai, M365 requester-supplied.
- No public WebForms remnant identified; all ViewState claims conditional.
- Reference [15] NuGet link has malformed markdown (line break in label) but URL itself valid.
- Report states no exploit attempt was made and no payload details were included.

## COVERAGE
- Chars read: 40390. EOF confirmed via read_file truncated:false.

---

## w2c-18-iis-shortname-webdav.digest

## REPORT
Source: research/w2c-18-iis-shortname-webdav.md

## ANSWER SUMMARY
- Public evidence confirms only the portal landing page with general, parent, and student sign-in paths.
- 8.3 short-name disclosure is a real IIS/NTFS risk class; MUJ affected status Unknown, not demonstrated.
- Mitigation is two-stage: stop new 8.3 creation and strip existing aliases via fsutil 8dot3name, with compatibility testing first.
- PUT 411 proves only message-framing enforcement, not WebDAV, write access, or file creation.
- OPTIONS/DELETE 404 is deliberately ambiguous under RFC 9110; cannot prove disablement.
- WebDAV requires an installed module plus per-URI inherited authoring rules; DAV header is per-resource.
- Edge attribution: externally observed status must be correlated with Akamai logs and IIS W3C logs before assigning a layer.
- Verdict: no confirmed IIS vulnerability; owner-authorized hardening review warranted.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/ : only target-specific verified fact.
- https://techcommunity.microsoft.com/blog/iis-support-blog/iis-short-name-enumeration/3951320 : tilde requests reveal 8.3 names, NtfsDisable8dot3NameCreation.
- https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/fsutil-8dot3name : query, scan, test, strip aliases; registry breakage warnings.
- https://brackish.io/2023/11/17/iis-short-file-name-enumeration : side channel works without directory listing.
- https://www.rfc-editor.org/rfc/rfc9110.html : 411 and 404 semantics, OPTIONS intermediary scope.
- https://www.rfc-editor.org/rfc/rfc4918.html : DAV header compliance classes per resource.
- https://learn.microsoft.com/en-us/iis/configuration/system.webserver/webdav/authoringrules : per-URI authoring rules, Read/Write/Source, inheritance.
- https://learn.microsoft.com/en-us/iis/publish/using-webdav/how-to-configure-webdav-with-request-filtering : applyToWebDAV treats WebDAV traffic differently.
- https://learn.microsoft.com/en-us/iis/configuration/system.webserver/security/requestfiltering/verbs : verb filtering gate.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.configuration.httpruntimesection.enableversionheader?view=netframework-4.8.1 : X-AspNet-Version default true, disable for production.
- https://learn.microsoft.com/en-us/iis/configuration/system.webserver/httpprotocol/customheaders/ : X-Powered-By ASP.NET default header.
- https://learn.microsoft.com/en-us/iis/manage/configuring-security/ensure-security-isolation-for-web-sites : one pool per site, shared identity risk.
- https://learn.microsoft.com/en-us/iis/configuration/system.webServer/directoryBrowse/ : directory browsing default disabled.
- https://learn.microsoft.com/en-us/iis/configuration/system.applicationhost/sites/site/logfile/ : W3C fields for edge/origin correlation.
- https://techdocs.akamai.com/property-mgr/docs/behs : edge behaviors govern attribution decisions.

## ACTIONABLE LEADS
- Owner-side: installed IIS role services, effective webdav config, authoring rules, request filtering, handlers, app pools, NTFS 8.3 state.
- Correlate reported 411/404 with Akamai property logs and IIS sc-status, sc-substatus, Win32 status.
- Run fsutil 8dot3name query and compatibility scan before any alias cleanup; keep backups.
- Check X-Powered-By and X-AspNet-Version suppression at edge and origin.
- No 8.3 enumeration, no PUT/DELETE content tests on production; use non-production resources and disposable principals.

## FLAGS
- Report cautions MVC "5.3" label is unverified against official release pages (MVC 5.2 is the latest public release page found).
- Supplied verb observations (PUT 411, OPTIONS/DELETE 404) were not independently reproduced.
- Reference [9] login.microsoftonline.com federationmetadata URL appears in references but is not used in body claims; unverified.
- Akamai presence is requester-supplied; report found no target-specific proof.
- No target-specific 8.3 or WebDAV evidence exists in the report.

## COVERAGE
- Chars read: 41686. EOF confirmed via read_file truncated:false.

---

## w2c-19-machinekey-viewstate.digest

## REPORT
Source: research/w2c-19-machinekey-viewstate.md

## ANSWER SUMMARY
- No public proof of MUJ key exposure. Both mujslcm.jaipur.manipal.edu and muj.slcm.jaipur.manipal.edu show branded login pages only.
- ASP.NET default key mode is AutoGenerate,IsolateApps with random material; a public AutoGenerate literal is not a leaked secret.
- Web farms need consistent manual keys; independent auto keys cause ViewState MAC failures across nodes.
- MVC 4.5+ anti-forgery tokens use MachineKey.Protect; Katana SystemWeb data protection delegates too. Key risk is not ViewState-only.
- Microsoft Dec 2024 incident: one public static key used for code injection; 3000+ disclosed keys flagged. Hash list comparison is the safe defensive method.
- Key equality between the two MUJ hostnames is Unknown; DNS names do not prove IIS topology or AppDomain sharing.
- Framework45 crypto behavior is opt-in via targetFramework; installing 4.5 does not change legacy apps automatically.
- Verdict: unverified deployment risk, moderate overall confidence; P0 owner-authorized key fingerprint review.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/ : portal A-side, branded login only.
- https://muj.slcm.jaipur.manipal.edu/ : second portal hostname, topology unknown.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.configuration.machinekeysection.validationkey?view=netframework-4.8.1 : validationKey default AutoGenerate,IsolateApps.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.configuration.machinekeysection.decryptionkey?view=netframework-4.8.1 : decryptionKey default and role.
- https://support.microsoft.com/en-US/servicing/DotNetFramework/troubleshooting/resolving-view-state-message-authentication-code-mac-errors : ViewState MAC, farm key coordination.
- https://www.microsoft.com/en-us/security/blog/2025/02/06/code-injection-attacks-using-publicly-disclosed-asp-net-machine-keys : incident, 3000+ disclosed keys, hash comparison script, rotation advice.
- https://github.com/Microsoft/referencesource/blob/master/System.Web/Configuration/MachineKeySection.cs : IsolateApps path hash, IsolateByAppId behavior.
- https://learn.microsoft.com/en-us/aspnet/mvc/overview/security/xsrfcsrf-prevention-in-aspnet-mvc-and-web-pages : MVC anti-forgery uses MachineKey.Protect.
- https://github.com/aspnet/AspNetKatana/blob/main/src/Microsoft.Owin.Host.SystemWeb/DataProtection/MachineKeyDataProtector.cs : Katana SystemWeb delegates to MachineKey APIs.
- https://devblogs.microsoft.com/dotnet/cryptographic-improvements-in-asp-net-4-5-pt-2/ : Framework45 opt-in mode, KDF, purpose separation.
- https://github.com/Tejas-Narula/SlcmPlus/tree/main : third-party Chrome extension, not authoritative config.
- https://github.com/Anushkakumar10/muj_slcm : third-party Python project, not authoritative config.
- https://github.com/blacklanternsecurity/badsecrets : known-secrets detection library for defensive matching.
- https://docs.github.com/en/enterprise-cloud%40latest/code-security/how-tos/secure-your-secrets/customize-leak-detection/define-custom-patterns : GitHub secret scanning custom patterns for machineKey search.
- https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html : secret rotation and revocation guidance.

## ACTIONABLE LEADS
- Map both hostnames to IIS site IDs, app IDs, physical paths, pools, origins before drawing key conclusions.
- Fingerprint fixed keys and compare with Microsoft disclosed-key hash list; never publish raw values.
- Repository history scan for machineKey, validationKey, decryptionKey, compatibilityMode with non-capturing patterns.
- Inventory all MachineKey.Protect consumers: ViewState, MVC anti-forgery, forms auth tickets, OWIN/Katana, custom blobs.
- Coordinated farm-wide rotation with logout planning and incident response if a public match appears.
- Check ViewStateUserKey assignment at Page_Init during WebForms code review.

## FLAGS
- Reference [15] in the report is a 404 page (viewstate-mac-enforced link); not usable as a source.
- Third-party repos are client-side material; no authoritative server config found. Absence of finding is not proof of safety.
- Similar branding on the two hostnames is E0-class evidence only; one-app conclusion is inference.
- Report reproduces no raw candidate keys; hash-list method is the stated safe path.
- AutoGenerate,IsolateApps literals are posture, not secrets; report warns against mislabeling them.

## COVERAGE
- Chars read: 40518. EOF confirmed via read_file truncated:false.

---

## w2c-20-api-security.digest

## REPORT
Source: research/w2c-20-api-security.md

## ANSWER SUMMARY
- Public third-party Flutter code names 13 MUJ routes on mujslcm.jaipur.manipal.edu: attendance, grades, marks, CGPA/GPA, calendar, directory, OTP, dashboard.
- Client model is cookie-session with __RequestVerificationToken; no bearer token use found in examined files.
- BOLA is the top authorization risk per OWASP API1:2023; server-side ownership and role checks required on every object.
- CORS is unmeasured, not cleared. Wildcard origin is invalid with credentials; per-endpoint allowed-origin policy needed.
- __RequestVerificationToken is anti-CSRF evidence, not a Microsoft identity access token.
- No indexed .asmx or .svc service found. WCF metadata is off by default; configuration-backed inventory beats URL guessing.
- Akamai Site Shield works only if origin allowlists Akamai ranges; forwarded-header trust must be bounded.
- Verdict: substantial and sensitive API-like surface publicly inferable, no live exploitable vulnerability established.

## KEY FACTS
- https://raw.githubusercontent.com/DK10WS/SLCM_APP/main/lib/pages/redirects.dart : 13 route constants, strongest route evidence.
- https://raw.githubusercontent.com/DK10WS/SLCM_APP/main/lib/utils/login.dart : login GET/POST flow, token and cookie extraction.
- https://raw.githubusercontent.com/DK10WS/SLCM_APP/main/lib/pages/Attendance.dart : POST attendance with empty StudentCode field.
- https://raw.githubusercontent.com/DK10WS/SLCM_APP/main/lib/pages/grades.dart : grades POST with empty Enrollment field.
- https://raw.githubusercontent.com/DK10WS/SLCM_APP/main/lib/pages/marks.dart : marks response fields MTE1, MTE2, CWS, ETE, PRS, Total.
- https://raw.githubusercontent.com/DK10WS/SLCM_APP/main/lib/pages/timetable.dart : timetable POST fields Year, Month, Type, Dated, PreNext.
- https://raw.githubusercontent.com/DK10WS/SLCM_APP/main/lib/pages/login.dart : third-party client stores credentials in SharedPreferences.
- https://raw.githubusercontent.com/DK10WS/SLCM_APP/main/lib/session_manager.dart : session cookie manager, clears on logout.
- https://github.com/AddisionS/slcm-feedback-form-filler : feedback extension, supply-chain concern.
- https://raw.githubusercontent.com/AddisionS/slcm-feedback-form-filler/main/chrome/manifest.json : scripting, activeTab, all_urls permissions.
- https://mujslcm.jaipur.manipal.edu/Home/Index : first-party landing page, only direct evidence.
- https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization : BOLA definition, server-side object checks.
- https://learn.microsoft.com/en-us/aspnet/web-api/overview/security/enabling-cross-origin-requests-in-web-api : CORS dimensions, wildcard plus credentials invalid.
- https://learn.microsoft.com/en-us/aspnet/web-api/overview/security/preventing-cross-site-request-forgery-csrf-attacks : cookie-auth CSRF and anti-forgery mitigation.
- https://techdocs.akamai.com/site-shield/docs/welcome-site-shield : Site Shield ranges must be allowlisted at origin perimeter.

## ACTIONABLE LEADS
- Reconcile the 13 public routes with internal route registration and assign owners and data classifications.
- Synthetic-account BOLA matrix: endpoint by role by object, semester and event scope changes, immediate role-change effect.
- Cookie review: Secure, HttpOnly, SameSite, rotation after login, logout invalidation, anti-forgery coverage on state-changing POSTs.
- CORS review with approved university origins only, including preflight, headers, redirects, cache variation.
- Error contract review across MVC, Web API, WCF, IIS layers with correlation IDs and redaction.
- Origin closure check: Akamai ranges, direct-origin reachability, X-Forwarded-For trust boundaries.
- If official mobile support is added, use authorization-code flow with PKCE and scoped tokens.

## FLAGS
- All routes come from third-party code and may be stale, incomplete, or wrong; not official API declarations.
- No bearer use found, but absence in examined client files is not proof of server behavior.
- Report names token taxonomy confusion as a trap: anti-forgery token is not an access token.
- Akamai, MVC 5.3, .NET 4.x, M365 identity are requester-supplied assumptions, not OSINT findings.
- SharedPreferences credential storage is a third-party client issue, not a MUJ server finding.
- Report states no active testing was performed and real student identifiers were not enumerated.

## COVERAGE
- Chars read: 46857. EOF confirmed via read_file truncated:false.

---

## w2c-21-jwt-session-tokens.digest

## REPORT
Source: research/w2c-21-jwt-session-tokens.md

## ANSWER SUMMARY
- No public JWT finding for SLCM. Landing page shows student and parent sign-in paths only.
- Ecosystem splits into four trust zones: SLCM (session unknown), Microsoft 365 (JWT ID tokens, opaque access tokens), MUJ Connect (token design unknown), Brightspace (OAuth bearer plus LTI 1.3 signed JWTs).
- Brightspace access-token lifetime configurable 1800-72000 seconds; Microsoft access tokens randomized 60-90 minutes.
- Algorithm policy is verifier-side: RFC 8725 fixed algorithm set, one key one algorithm, no alg=none.
- Signature success is not sufficient; issuer, audience, subject, exp, nbf, type checks required.
- Stateless JWT revocation needs jti denylists; ASP.NET sessions keep central server state for immediate termination.
- Historical library failures (CVE-2015-9235, CVE-2023-48238) show the mechanism; they do not name a MUJ dependency.
- Verdict: ecosystem is not one JWT-based system; no MUJ vulnerability established.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/ : SLCM landing page, only SLCM-specific evidence.
- https://mujconnect.in/login : MUJ Connect login, email or username only.
- https://learning.onlinemanipal.com/d2l/home/14042 : MUJ-branded Brightspace login page.
- http://d2l.com/why-d2l/customer-corner/d2l-brightspace-in-india-a-success-story : D2L case study, 85,000 online learners in five years.
- https://docs.valence.desire2learn.com/basic/oauth2.html : OAuth bearer tokens, 1800-72000 second lifetime range.
- https://community.d2l.com/brightspace/kb/articles/23730-about-lti-1-3-launch-and-authentication : LTI 1.3 OIDC launch, kid-selected public key verification.
- https://datatracker.ietf.org/doc/html/rfc8725 : algorithm pinning, explicit typing, issuer-key binding, no alg=none.
- https://datatracker.ietf.org/doc/html/rfc7519 : exp and nbf enforcement with small clock skew.
- https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens : access tokens opaque to clients, 60-90 minute randomized lifetime.
- https://learn.microsoft.com/en-us/previous-versions/aspnet/ms178581%28v%3Dvs.100%29 : ASP.NET SessionID maps to server-maintained state.
- https://learn.microsoft.com/en-us/aspnet/mvc/overview/security/xsrfcsrf-prevention-in-aspnet-mvc-and-web-pages : anti-forgery pair is not an authentication token.
- https://portswigger.net/web-security/jwt/algorithm-confusion : asymmetric-to-symmetric algorithm confusion mechanism.
- https://nvd.nist.gov/vuln/detail/CVE-2015-9235 : jsonwebtoken before 4.2.2 verification bypass.
- https://nvd.nist.gov/vuln/detail/CVE-2023-48238 : json-web-token before 4.0.0 RS256/HS256 confusion.
- https://www.imsglobal.org/spec/lti/v1p3 : LTI claims contract, deployment id, target link checks.

## ACTIONABLE LEADS
- Owner questionnaire for SLCM: cookie name, Secure, HttpOnly, SameSite, idle and absolute timeout, rotation, logout invalidation, CSRF coverage.
- Brightspace admin review: OAuth lifetime setting, refresh-token rotation, LTI tool registrations, JWKS, nonce replay window.
- MUJ Connect: document auth protocol, issuer, token format, storage, lifetimes, revocation before any security claim.
- Staging verifier regression suite: alg none, wrong algorithm family, wrong issuer, wrong audience, unknown kid, expired token, replayed nonce.
- Check cross-protocol acceptance: Brightspace API tokens must never validate as LTI ID tokens or vice versa.
- Publish a coordinated disclosure channel so team reports stay inside authorization.

## FLAGS
- urlscan.io record says the host was not observed in scan corpus; it does not confirm IIS, MVC, .NET, or Akamai (report cites it only as passive observation).
- Builtwith and Wappalyzer URLs appear in references without body claims; fingerprint data unverified.
- Reference [17] is a 404 page on learn.microsoft.com; report does not rely on it.
- 85,000 learner figure is D2L marketing material, not independent.
- SLCM cookie details and MUJ Connect token internals remain Unknown by the report's own evidence classes.
- Report explicitly rejects calling MUJ Connect JWT-vulnerable without first-party evidence.

## COVERAGE
- Chars read: 37606. EOF confirmed via read_file truncated:false.

---

## w2c-22-third-party-integrations.digest

## REPORT
Source: research/w2c-22-third-party-integrations.md

## ANSWER SUMMARY
- Microsoft 365 identity confirmed at service level via official setup SOP; account provisioning source and direction remain Unknown.
- Apex TXT on jaipur.manipal.edu shows Microsoft verification strings, Cisco Webex verification strings, SPF includes for Outlook and Brightspace mail.
- NoPaperForms is the strongest third-party attribution: official admissions page routes to admissions.jaipur.manipal.edu, CNAME to jaipurmanipal.nopaperforms.com, then AWS load balancer.
- Brightspace relation proven by SPF include and CDOE-branded tenant page; residential-campus SLCM sync is Inference, not fact.
- D2L grade-sync capability (SIS-pull, push-export, permission-scoped grade APIs) documented; no MUJ flow confirmed.
- Webex TXT proves domain verification, not claiming, licenses, SSO, or directory sync.
- SLCM names return direct A records with no CNAME; Akamai claim not corroborated by public DNS.
- Verdict: multi-vendor ecosystem with ungoverned state transitions as the top risk; no vulnerabilities found.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/ : institutional, parent, student login paths.
- https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf : official M365 setup flow, temporary password.
- https://dns.google/resolve?name=jaipur.manipal.edu&type=TXT : Microsoft, Cisco, Brightspace SPF and verification values.
- https://jaipur.manipal.edu/admissions.php : official admissions page, Track Application and Apply Now links.
- https://dns.google/resolve?name=admissions.jaipur.manipal.edu&type=CNAME : CNAME to jaipurmanipal.nopaperforms.com.
- https://dns.google/resolve?name=admissions.jaipur.manipal.edu&type=A : resolves to AWS load-balancer name.
- http://developer.nopaperforms.com/ : API areas and Secret Key/Access Key credential model.
- https://learning.onlinemanipal.com/d2l/home/14042 : MUJ CDOE Brightspace tenant page.
- https://community.d2l.com/brightspace/kb/articles/4825-ways-to-initiate-grades-export : push and pull grade export with initiator and failure records.
- https://docs.valence.desire2learn.com/res/grade.html : grade read and write scopes, 403 on missing permission.
- https://community.d2l.com/brightspace/kb/articles/23807-about-the-ipsis-platform : IPSIS SIS import mechanism.
- https://help.webex.com/en-us/article/cd6d84/Manage-Your-Domains : verification token in DNS, verified versus claimed states.
- https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=CNAME : no CNAME answer for main SLCM name.
- https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=A : direct A record, no Akamai CNAME naming.
- https://jaipur.manipal.edu/pay-fee-online.php : SLCM fee entry, SpaceBasic hostel/mess, bank transfer channels.

## ACTIONABLE LEADS
- Owner workshop demanding one redacted artifact per seam: Entra app list, IPSIS connections, Webex domain state, NoPaperForms field map, payment reconciliation.
- Audit SPF and verification TXT entries for stale artifacts; Cisco token may be removable after verification.
- Build applicant-to-student state machine: correlation IDs, duplicate detection, failure states, reconciliation across NoPaperForms, finance, SLCM, Entra.
- Webhook design review as hypothesis only: HMAC or asymmetric signatures, idempotency keys, replay windows, constant-time compare.
- Reconcile Akamai claim with property-manager evidence; do not publish edge findings without it.
- Identity lifecycle matrix: source of truth, creation event, role mapping, deprovisioning deadline per population.

## FLAGS
- Akamai attribution contradicted by current DNS shape (direct A, no CNAME); report says DNS alone does not exclude every Akamai config.
- No MUJ webhook endpoint identified anywhere; webhook risks are labeled review hypotheses.
- Temporary-password workflow implies admin account creation but is labeled Inference.
- NoPaperForms API key custody, accepted-student handoff, and retention are undocumented; Unknown, not negative findings.
- Brightspace campus sync, Webex sync, and grade return to SLCM are all Unconfirmed or Inference per the report's evidence classes.
- Report finds no public evidence of any exploit; the risk model is governance and state-transition integrity.

## COVERAGE
- Chars read: 45130. EOF confirmed via read_file truncated:false.

---

## w2d-01-regnum-format.digest

## REPORT
Source: w2d-01-regnum-format.md (MUJ SLCM register number evidence and enumeration risk)

## ANSWER SUMMARY
- Official SLCM FAQ publishes the username template name.registration number with example garv.2506040062; this is the only direct public example found.
- Registration No. is a MUJ-generated, non-editable Student Details field per the official onboarding guide; separate fields exist for Academic Year, Program/Branch, and Year of Admission.
- Digit split 25|06|04|0062 is an analyst inference; no reviewed MUJ source assigns meaning to any chunk. Batch, stream, branch, and campus mappings stay unknown.
- Cross-year, cross-batch persistence of the format is not established; one example cannot confirm a sequence.
- Candidate-space math is bounded only: 10^10 raw ten-digit strings, 9x10^9 without leading zero, 10^8 with fixed 25 prefix, 10^6 with 2506, 10^4 with 250604. None equals a count of valid or active accounts.
- Onboarding guide: first-year credentials go to the personal Gmail address; official address pattern name.XXXXXX@muj.manipal.edu; same password used for SLcM and official email. Architecture behind the coupling is unknown.
- Verdict: identifier predictability is a moderate information-disclosure concern; no live authentication behavior was tested, no access or compromise evidence exists.

## KEY FACTS
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - username template, garv.2506040062 example, Outlook ID password rule, support contacts.
- https://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf - Registration No. "(Generated by MUJ)", credential delivery, same-password statement, document upload list.
- https://mujslcm.jaipur.manipal.edu/Home/Index - public login context and parent-login label.
- https://jaipur.manipal.edu/fosta/b-tech-computer-science-engineering.php - curriculum year labels (2019-23, 2023-27, 2025 onwards); control against using program dates as a codebook.
- https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html - OWASP requirement for generic authentication failure responses and timing awareness.
- https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md - ASVS L2 MFA requirement and secure-recovery rules.
- https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/03-Identity_Management_Testing/04-Testing_for_Account_Enumeration_and_Guessable_User_Account - WSTG on user-ID disclosure via timing and external forgot-password services.
- https://pages.nist.gov/800-63-3/sp800-63b.html - NIST rate-limiting requirement for secrets under 64 bits entropy.
- https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html - consistent recovery responses and anti-automation guidance.
- http://linkedin.com/in/hitansh-mehndiratta-7013a6179 - public profile cited only as context, explicitly not registrar evidence.

## ACTIONABLE LEADS
- Ask MUJ Registrar, Admissions, DMS, or IT security for a sanctioned data dictionary or confirmation of whether the number is opaque or structured.
- Confirm identifier lifecycle questions: stability across program changes, campus changes, readmission.
- In a MUJ-owned staging environment, verify generic failure responses, timing uniformity, rate limits, and MFA posture.
- Report the public FAQ example exposure to MUJ so the owner can decide whether it should remain published.
- Do not build or test candidate username lists; keep evidence in a redacted ledger with source URL, quote, confidence, and open question.

## FLAGS
- garv.2506040062 carries an "eg:" marker and may be purely illustrative; do not treat it as an active account.
- Every digit-meaning claim (25 batch, 06 stream, 04 branch/campus, 0062 serial) is unverified inference.
- LinkedIn profile is not authoritative identity data; admission letters and application numbers are separate namespaces from SLCM registration numbers.
- Scribd "Registration Form Muj" reference is unverified third-party material.
- Same-password instruction may describe an initial credential handoff, credential reuse, or federation; the report cannot choose.

## COVERAGE
Chars read: 35,369. EOF confirmed: true.

---

## w2d-02-marks-results.digest

## REPORT
Source: w2d-02-marks-results.md (MUJ public results: evidence, formats, and data-flow limits)

## ANSWER SUMMARY
- The public corpus does not document an unauthenticated campus semester-result lookup, a public rank list, a marksheet field schema, or an SLCM-to-RMS interface.
- Academic Handbook model: theory and laboratory courses out of 100 marks, 60 in-semester (two 20-mark sessionals + 20 CWS) and 40 end-semester; 10-point grade scale A+ to E with AP/F/I/DT at zero; 35% pass threshold with 35% end-semester minimum; attendance entered in grade sheet.
- Official result PDFs are PhD admissions artifacts only: entrance and interview results and selected-candidate lists for January 2025, July 2024, January 2026; fields are identifiers, names, departments, registration mode, and status (NFS/ABSENT), not ranked marks tables.
- RMS is Research Data Management System on both rms.manipal.edu and rms.jaipur.manipal.edu (publications, APC, grants, open access, IPR); no student-result role visible.
- Governance flow documented: assessment, grade finalization, result processing and declaration by Controller of Examinations, records custody and authentication by Registrar; software handoffs undocumented.
- TracMARKS (muj.tracmarks.com) is a MeritTrac-branded login surface; purpose, ownership, and marks relation unverified.
- CGPA equivalence notice: grades relative, no fixed percentage mapping; approved conversion Percentage = CGPA x 10 for organizational demand.
- Online MUJ (onlinemanipal.com) is a separate proctored-online program ecosystem; must not be merged with campus SLCM.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/Home/Index - SLCM public sign-in boundary; no marks visible.
- https://jaipur.manipal.edu/examination.php - examination page; continuous assessment, Revised Grade Report Card mention, application formats.
- http://jaipur.manipal.edu/fomca/img/pdf/Academic%20Handbook%202022-23.pdf - 100-mark model, 60/40 split, 20/20/20 in-semester components, grade table, GPA/CGPA definitions, CoE declaration.
- https://www.jaipur.manipal.edu/announcement.php - official announcement archive linking the PhD result PDFs and calendar.
- https://jaipur.manipal.edu/img/pdf/PhD-ADMISSIONS-JAN-2026-INTERVIEW-RESULT-LIST-OF-SELECTED-CANDIDATES.pdf - January 2026 PhD interview selected-candidate list.
- https://www.jaipur.manipal.edu/admin/photo/annoncement/35.pdf - January 2025 PhD entrance result and interview shortlist; Result Awaited candidates must show final marksheet.
- https://jaipur.manipal.edu/img/pdf/Result_Interview%20for%20PhD%20Admission_January%202025.pdf - January 2025 interview result with NFS/ABSENT status labels.
- https://jaipur.manipal.edu/img/pdf/Announcements/PhD%20Interview%20Result%20July%20-%202024%20session.pdf - July 2024 selected-candidate list, dated 3 August 2024.
- https://rms.manipal.edu/ - central RMS research administration description.
- https://rms.jaipur.manipal.edu/ - MUJ RMS research-performance notices and IRINS link.
- https://muj.tracmarks.com/ - TracMARKS login with MeritTrac branding; unverified purpose.
- https://muj.tracmarks.com/ScriptMovement - extra TracMARKS path; unverified.
- https://jaipur.manipal.edu/img/pdf/exam/Equivalence-Certificate-of-CGPA-with-Percentage-of-Marks.pdf - relative grades and CGPA x 10 conversion policy.
- https://jaipur.manipal.edu/administration-registrar.php - Registrar as custodian of records and common seal.
- https://articles.findmycollege.com/manipal-university-jaipur-result/ - secondary source claiming SLCM semester results, grade cards, SGPA/CGPA; lead only.

## ACTIONABLE LEADS
- Pull the announcement archive repeatedly and classify newly linked PDFs by visible fields; archive may add result artifacts over time.
- Search MUJ's own site for "grade card", "marksheet", "semester result", "result declaration" to hunt for official specimens.
- Obtain an intentionally public specimen grade card or an official statement naming the result service before documenting layout.
- Check whether TracMARKS is named anywhere in official MUJ examination communications.
- Keep SLCM, RMS, TracMARKS, and the online portal as separate records in team diagrams; mark all cross-links unresolved.

## FLAGS
- GetMyUni, CollegeDunia, and FindMyCollege claims are secondary and possibly stale; not official schema or public-access proof.
- TracMARKS branding alone does not establish ownership, purpose, or data exchange.
- "No rank list found" is a bounded corpus finding, not proof none exists.
- RMS acronym conflation risk; research data vs guessed result management.
- PhD admissions PDFs are selection lists, not marks statements; do not extrapolate a campus marksheet from them.

## COVERAGE
Chars read: 44,845. EOF confirmed: true.

---

## w2d-03-fee-documents.digest

## REPORT
Source: w2d-03-fee-documents.md (MUJ fee artifacts: public evidence and SLCM exposure)

## ANSWER SUMMARY
- MUJ publishes a large but fragmented public fee record: program pages, hostel and mess tables, annual circulars, refund policy, scholarship waivers; the SLCM landing page itself exposes only a login boundary and no fee UI.
- 2026-27 hostel double occupancy: INR 167,372 accommodation, INR 15,378 housekeeping, INR 25,475 refundable security deposit, INR 208,225 total including deposit; optional laundry INR 8,810 and health team INR 12,750.
- Hostel continuation circular reconciles with the hostel page: residential dwelling INR 182,750 (accommodation + housekeeping), mess INR 79,000, full-year total INR 261,750, deadline 5 July 2026, SpaceBasic-only payment, non-refundable once paid.
- Payment page routes existing students to the SLCM portal for course fees and to SpaceBasic for hostel and mess; post-payment email must include UTR number, debit-account holder, transaction date, amount, using a linked format.
- 12% per annum late-fee rate appears only in the 2025-26 annual notice (deadline 18 July 2025) and must be treated as historical, not applied to 2026-27; the 2026-27 academic calendar gives 16 July as the fee-payment date.
- Refund table runs from full refund to nil based on withdrawal timing; scholarships grant tuition-fee waivers (Visvesvaraya, TMA Pai, Rajasthan merit, local-region, sibling, MUJ graduate, disability, MBA bands).
- Unanswered: transport fee schedule, current recurring-student late-fee rule, validated receipt-template contents, authenticated fee-module screenshot.
- Notable: the 2025-26 notice prints the portal as https://mujslcm.jaipur.manipal.edu:122/ while the 2026 payment page prints the bare hostname; the report flags this as an observable URL-form difference, inference only.

## KEY FACTS
- https://jaipur.manipal.edu/hostel-fees.php - 2026-27 hostel table with component amounts, login-gated payment modes, receipt retention advice.
- https://jaipur.manipal.edu/mess-fees.php - mess fee INR 79,000 with revision warning for fuel/market/inflation pressure.
- https://jaipur.manipal.edu/pay-fee-online.php - payment routing (SLCM vs SpaceBasic) and UTR/account-holder/date/amount email workflow with Download the Format link.
- https://jaipur.manipal.edu/indian-fee-structure.php - official course-fee index across programs; registration non-refundable, caution deposit refundable.
- https://jaipur.manipal.edu/fol/bachlor-LLB.php#Program-Fee - LLB fees: INR 108,000 tuition, INR 10,000 registration, INR 10,000 deposit, INR 128,000 at admission (USD columns shown).
- https://jaipur.manipal.edu/foe/m-tech-structural.php#Program-Fee - M.Tech Structural: INR 181,000 tuition, INR 206,000 at admission; applies to students admitted till academic year 2025.
- https://jaipur.manipal.edu/img/pdf/Annual-Fee-Payment-for-the-AY-2026-2027.pdf - hostel continuation circular; 5 July 2026 deadline, SpaceBasic only, OCR-garbled fields in mess and final-year rows.
- https://jaipur.manipal.edu/img/pdf/academicrules/AC-calender-2026-27.pdf - academic calendar; 16 July as last fee-payment date.
- https://jaipur.manipal.edu/img/pdf/Notification_Annual-Fee-Payment-AY-2025-26.pdf - 18 July 2025 deadline, 12% per annum late fee, Annexure 1 course-wise and batch-wise amounts, portal URL with :122 port.
- https://jaipur.manipal.edu/indian-refund-policy.php - withdrawal refund table (full to nil), 45-day refund window, dues-clearance certificate requirement.
- https://jaipur.manipal.edu/indian-scholarship.php - waiver categories and CGPA continuity conditions for scholarships.
- https://mujslcm.jaipur.manipal.edu/Home/Index - SLCM login boundary; no fee balances or module UI in public extract.
- http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf - MUJ ICT inventory; SLCM described as replacing AMS with attendance, internal/external marks, result publication, broadcast modules.
- https://github.com/DK10WS/SLCM_APP - student-built app describing login, timetable, grades, attendance; not official fee evidence.
- https://mujstella.in/ - independent platform explicitly not affiliated with MUJ.

## ACTIONABLE LEADS
- Build a versioned artifact register: source URL, retrieval date, academic-year label, component, amount, currency, provider route, confidence, redaction status.
- Locate a current 2026-27 recurring-student late-fee circular and any separately titled transport fee notice.
- Investigate the :122 URL form found only in the 2025 notice; treat any port-based inference as unverified.
- Track reconciliation checks (hostel components vs circular totals) as analyst calculations, labeled as such.
- Do not submit payment forms, probe the portal, or replay transaction references; public-only boundary.

## FLAGS
- OCR corruption in the annual circular (mess and final-year fields) must not be repaired by guesswork; the clean mess page supports INR 79,000.
- 12% late fee is historical 2025-26 only; clause extraction was truncated.
- 5 July (hostel circular) vs 16 July (calendar) is a scope difference, not a contradiction.
- Scribd "Updated Payment Receipt" failed to load in review; very low reliance.
- Garbled PDF titles in references (mojibake) indicate extraction artifacts.
- The :122 portal URL form may indicate a legacy document or old deployment; inference only, no connection tests performed.

## COVERAGE
Chars read: 43,755. EOF confirmed: true.

---

## w2d-04-exam-circulars.digest

## REPORT (w2d-04-exam-circulars.md)
Public MUJ exam artifacts and safe SLCM risk map. Public pages and PDFs only, no portal testing. Verdict: exam process spine documented, hall-ticket format and marks-update path not publicly established. 224 lines, 41818 chars, read to EOF, truncated: false.

## ANSWER SUMMARY
- MUJ publishes an examination landing page, Student Examinations Handbook, Examination Manual with appendices, and timetable PDF families; use these as the baseline corpus.
- "Make-up" is the documented terminology: F or I in ETE allows a make-up exam in the respective course; no standalone "back paper" page or current deadline was found.
- Grade flow: answer books evaluated, marks lists submitted, marks uploaded to AMS/DMS, initial grades calculated there, Grade Moderation Committees may adjust boundaries, results declared after approvals within 15 days.
- Hall-ticket and identity requirements are documented as conduct rules, but no hall-ticket template or field spec is public; report the format as unknown.
- Timetable PDFs expose course codes, dates, slots, and discipline headings (public scheduling metadata), dated April-May 2025, May 2025, December 2024; no 2026 timetable link on the retrieved page.
- Grievance routes: online form on Microsoft Forms, UGC Samadhaan, USGRC committee; two separate 15-day clocks (USGRC report target, Ombudsperson appeal) must not be merged with result declaration timing.
- No attributable, verified MUJ marks-dispute case was found; the evidence gap is reported as a gap.

## KEY FACTS
- https://jaipur.manipal.edu/examination.php - central examination index: handbook, manual, application formats, timetable links, make-up application at Rs 1000 per course.
- https://jaipur.manipal.edu/img/pdf/exam/Student%20Examination%20Handbook%202023-24%20%2811.08.2023%29.pdf - eligibility thresholds (UG 35%, PG 40% ETE and overall), F/I/DT outcomes, make-up rules, result timing, conduct controls.
- https://jaipur.manipal.edu/img/pdf/exam/3.%20Manual%20Exam%20Process.pdf - evaluation, marks-list submission, AMS/DMS upload, grade moderation, approvals, result declaration.
- https://jaipur.manipal.edu/img/pdf/exam/4.%20Appendix%20I%20Examination%20manual%20MUJ%2003%20Apr%2019.pdf - answer-book and attendance chain of custody, fees Rs 1000 regular and Rs 700 online per subject.
- https://jaipur.manipal.edu/img/pdf/exam/B.Tech_Higher%20Sem_ETE_APRIL-MAY_2025.pdf - discipline columns, course names and codes, Slot-1 09:30-12:30, Monday 28-04-2025.
- https://jaipur.manipal.edu/img/pdf/exam/FOMC_ETE%20Timetable%20Dec%202024.pdf - faculty timetable with BBA and semester columns.
- https://jaipur.manipal.edu/img/pdf/exam/M.TECH_II%20SEM_ETE%20TT_%20APRIL-MAY%202025_.pdf - M.Tech second-semester timetable.
- https://jaipur.manipal.edu/img/pdf/academicrules/AC-calender-2026-27.pdf - 2026-27 milestone labels: MTE, ETE, re-sessional, make-up; visible July dates without complete label pairing.
- https://www.jaipur.manipal.edu/online-grevience-registration.php - grievance submission via Microsoft Forms, UGC Samadhaan, USGRC document links.
- https://www.jaipur.manipal.edu/img/pdf/Committee_USGRC.pdf - June 26 2026 notice: school-level escalation, quorum of three, two-year terms, 15-day report target, 15-day Ombudsperson appeal.
- https://mujslcm.jaipur.manipal.edu/ - portal landing: welcome, Sign In, Sign In Parent Login only.
- https://jaipur.manipal.edu/academic-rules-regulations.php - academic rules index, related context.
- http://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References - IDOR definition used for the control recommendation.
- http://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html - session IDs as untrusted input, session renewal after privilege changes.

## ACTIONABLE LEADS
- Maintain a document map: title, academic year, event type, audience, date, PDF or page; compare future revisions against it.
- Check newly published timetable PDFs for accidental student-level data and stale-file exposure.
- Ask the owner for a control description of marks-list to AMS/DMS reconciliation and grade-moderation approval records; propose a tabletop exercise, not a live manipulation.
- Route genuine complaints through the official grievance channels; keep a dispute-evidence register with three labels (verified process, student allegation needing consent, unverified hit).
- Verify current 2026 timetable and make-up notice availability through the examination page before claiming publication gaps.

## FLAGS
- Handbook is 2023-24; it is not silently treated as current 2026 rules.
- Fee wording differs across sources: landing page Rs 1000 per course, Appendix I Rs 1000 regular and Rs 700 online per subject; preserve, do not harmonize.
- "Marks uploaded to AMS/DMS" is an operational noun, not evidence of a student-editable path or public endpoint.
- Two 15-day clocks are distinct: result declaration after moderation and approvals, versus Ombudsperson appeal after USGRC decision.
- Stack labels (ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai, Microsoft 365) are supplied scope, not independently verified.
- No verified student marks-dispute case exists in the corpus; absence is not proof no dispute ever occurred.

## COVERAGE
- File read to EOF: 224 lines, 41818 chars (file_size 41818), truncated: false. Confirmed EOF at line 224, final reference.

---

## w2d-05-hostel-transport.digest

## REPORT (w2d-05-hostel-transport.md)
MUJ SLCM hostel and transport artifacts: public exposure and privacy risk. Public pages, regulations, and defensive guidance only. Verdict: no MUJ allotment or transport rosters located publicly; privacy-risk review supported. 181 lines, 31510 chars, read to EOF, truncated: false.

## ANSWER SUMMARY
- Repeated searches located no MUJ-specific public allotment list with student names and register numbers, and no student transport route roster. This is a bounded negative finding, not proof of absence behind login or in unindexed channels.
- Hostel rules are public: allotment after fee payment on a first-come-first-served basis; room changes only in exceptional circumstances with prior Chief Warden permission.
- Public facility and fee data: twin-sharing rooms, 10,000+ beds, flap-barrier access control; 2026-27 double-occupancy fee INR 167,372 plus housekeeping INR 15,378 and refundable deposit INR 25,475; forfeiture on late non-payment.
- Transport public data is campus access only: Dehmi Kalan address, Jaipur bus stand 25 km, railway station 24 km, airport 27 km. No shuttle routes, stops, or timetables were located.
- Under DPDP Act definitions, a PDF joining name, register number, room, and route would be personal-data processing, not a neutral notice.
- CERT-In Directions require covered entities to report listed incidents within six hours and keep ICT logs for a rolling 180 days in India.
- Recommended publication model: individual portal views, expiring links, pseudonymous references, aggregate vacancy statistics; no public name plus register number plus room or route combinations.

## KEY FACTS
- https://jaipur.manipal.edu/hostel-facility.php - allotment rule: fee payment, first-come-first-served, Chief Warden permission for changes.
- https://jaipur.manipal.edu/room-description.php - double-seater rooms, beds, wardrobes, study furniture, universal sockets.
- https://jaipur.manipal.edu/hostel-overview.php - separate boys' and girls' blocks, 10,000+ beds, flap-barrier access control.
- https://jaipur.manipal.edu/hostel-fees.php - 2026-27 fee breakdown, confirmation after full fee receipt, forfeiture terms, refund rules with INR 5,000 processing deduction.
- https://jaipur.manipal.edu/mess-fees.php - mess charge INR 79,000, two-month allotment windows, revision notice language.
- https://jaipur.manipal.edu/faqs-regarding-hostel.php - annual vacancy for maintenance, possible same-room continuity, allocation-day luggage help.
- https://jaipur.manipal.edu/chiefwardensmessage.php - 24-hour security and medical facility, Wi-Fi, mess, gym.
- https://www.jaipur.manipal.edu/contact-university.php - campus location and intercity distances; no shuttle data.
- http://manipal.edu/mu/important-links/privacy-and-cookie-policy.html - MAHE policy: data categories, sharing, retention, 30-day grievance window.
- https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf - DPDP Act text: personal data, processing definition, breach definition, rights (sections 11-13).
- http://pib.gov.in/PressReleasePage.aspx?PRID=2190655 - DPDP Rules 2025 notified November 14 2025.
- https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf - six-hour incident reporting, 180-day log retention, time synchronization.
- https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html - least privilege, deny-by-default, server-side permission validation.
- https://owasp.org/www-project-application-security-verification-standard - ASVS as the control baseline reference.
- https://www.hilliardschools.org/departments/transportation/busstop - comparative design: individualized route login instead of public roster (not MUJ policy).

## ACTIONABLE LEADS
- Build a synthetic artifact inventory with fake names, register numbers, rooms, and routes; never collect or redistribute real student PII.
- Request an authorized non-production review: role matrix, publication workflow, room-change and transport assignment workflows, retention schedule, incident contacts.
- Propose a two-tier publication model: public policy tier, private individual-view tier with staff aggregate dashboards.
- Run a pre-publication privacy review checklist: identifiability, residence or movement disclosure, field necessity, less identifying alternatives, audience limits, link expiry, cacheability.
- If a real public document is found, notify MUJ through its privacy or security contact and do not redistribute it.

## FLAGS
- Negative search findings are medium confidence for the corpus, low confidence for universal absence.
- Stack labels (ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai, Microsoft 365) are not independently verified in this report.
- The MAHE privacy policy is institutional, not MUJ-specific in every operational detail.
- DPDP Rules were notified November 14 2025; the report does not claim uniform commencement or enforcement status.
- Reference 8 is a Gazette PDF with garbled title text; legal claims are cited from it and need counsel confirmation.
- The Hilliard City Schools example is comparative only.

## COVERAGE
- File read to EOF: 181 lines, 31510 chars (file_size 31510), truncated: false. Confirmed EOF at line 181, final reference.

---

## w2d-06-orientation-docs.digest

## REPORT (w2d-06-orientation-docs.md)
MUJ SLCM orientation and onboarding evidence. Official PDFs, pages, one header observation, one non-official repost. No authentication attempts. Verdict: onboarding workflow well documented; provisioning actor and timing, and default SLCM password, not publicly documented. 189 lines, 32453 chars, read to EOF, truncated: false.

## ANSWER SUMMARY
- The First-Year Student Profile Registration Guide says the Department of Admissions sends the SLCM username and password to the personal Gmail address supplied during admission. Delivery office and channel are documented; the technical account creator is not.
- No reviewed official artifact publishes a default SLCM password value. The FAQ says the password is aligned with the official Outlook ID; the guide says credentials are emailed by Admissions.
- No first-login SLCM password change is stated. The Office 365 SOP (v1.0, June 2025) explicitly documents a temporary-password flow and forced change for university email, plus mandatory MFA.
- Provisioning timing is not documented: when the SLCM or email account is created or activated is unknown; orientation reporting times (9:00 AM report, 9:15 AM verification) are physical events, not activation timestamps.
- A third-party header observation records HTTP 200, IIS/10.0, ASP.NET MVC 5.3, ASP.NET 4.0.30319, X-Powered-By ASP.NET. Akamai is not present in that record.
- The 2026 orientation page ties reporting, document verification, SLCM profile registration, and Office 365/Outlook help into one support path; support ownership is split between Admissions, SLCM support, and IT for Outlook.
- A College Sidekick repost mislabeled as BITS Pilani Goa is non-official, uploaded August 4 2024, and must not be treated as current MUJ policy.

## KEY FACTS
- http://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf - primary onboarding artifact: profile workflow, credential delivery via personal Gmail, non-editable admission-seeded fields, parent-mobile OTP for parent login.
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - registration link, username convention, password per official Outlook ID, DMS/AMS and IT Infra support routing.
- https://jaipur.manipal.edu/induction-orientation-program.php - 2026 orientation: reporting 9:00 AM, verification 9:15 AM, venues (Old Food Court, Smt. Vasanti R Pai Auditorium), help documents.
- https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf - v1.0 effective June 2025: temporary password, forced change, MFA mandatory, setup password policy (13+ chars), reset minimum (16 chars).
- https://mujslcm.jaipur.manipal.edu/ - public SLCM landing surface.
- https://mujslcm.jaipur.manipal.edu/Home/Index - portal surface with student identity hint, parent login, and a Microsoft password-reset destination in the HTML.
- http://api.hackertarget.com/httpheaders?q=https://mujslcm.jaipur.manipal.edu/ - point-in-time header fingerprint: Microsoft-IIS/10.0, MVC 5.3, ASP.NET 4.0.30319.
- https://www.collegesidekick.com/study-docs/16707539 - misattributed repost (BITS Pilani Goa label), August 4 2024 upload, historical only.
- https://jaipur.manipal.edu/img/pdf/Registration-Form.pdf - UG/PG registration form, related onboarding document.

## ACTIONABLE LEADS
- Catalogue onboarding artifacts with retrieval dates, titles, version or date metadata, and confidence classes; track revisions.
- Ask MUJ through official channels: account-lifecycle owner, activation timing definition, current SLCM and Office 365 onboarding documents, whether SLCM and Microsoft credentials are synchronized.
- Preserve the header observation as secondary evidence; do not use it to claim patch level or backend topology.
- Use the FAQ's username convention only to describe the pattern; never derive or guess real student identifiers.
- No credential guessing, no password-reset flows on accounts not owned, no route enumeration, without written scope.

## FLAGS
- The SLCM FAQ is undated; guide currency should be confirmed with Admissions before operational reliance.
- Passwords: do not infer a password formula from the Outlook-ID wording; sync, separate generation, and temporary-password interpretations all remain possible.
- Physical reporting and verification times are not account-activation times.
- The header record is third-party, point-in-time, and shows no Akamai; Akamai remains unverified, not proven absent.
- The College Sidekick document is externally hosted and misattributed; it is useful only as a lead for version comparison.
- The Microsoft reset link proves recovery affordance at the interface, not federation or credential-store sharing.

## COVERAGE
- File read to EOF: 189 lines, 32453 chars (file_size 32453), truncated: false. Confirmed EOF at line 189, final reference.

---

## w2d-07-library-integration.digest

## REPORT
Source file: w2d-07-library-integration.md (MUJ Library and SLCM Public Exposure Report)

## ANSWER SUMMARY
- The official library page names Koha LMS for holdings, a Web OPAC, DSpace for the institutional repository, Knimbus for off-campus access, and Turnitin for plagiarism checking.
- The official page links the Single Window Search Box at http://manipal-koha.informindia.co.in/; the destination self-identifies as the Manipal University Jaipur Library OPAC with login and password prompts and shows no student records anonymously.
- Library identity runs on physical cards: University Identity Card, Smart ID Card swiped at entry, and RFID-enabled and bar-coded ID cards for borrowing, renewal, reservation, and return.
- Circulation rules: PG and UG students borrow five books for 14 days, fines are Rs 2 per day for the first overdue week then Rs 5 per day, and unpaid overdue items block further issue; no online fine payment is documented.
- RemotLog pages describe MUJ Libraries with the MUJ email address as the username for remote resource access; no SLCM SSO or shared token is shown.
- An IP-based DSpace/JSPUI repository (20.219.59.68:8080) exposes a credential-like access instruction in its page title; the report redacts the value and treats it as an exposure incident.
- https://www.mujlibrary.live/ claims a MUJ DigiLibrary with email OTP, catalog, tracking, and renewals, but no official MUJ linkage exists; users should not submit university emails until ownership is confirmed.
- No public MUJ library API or anonymous endpoint returning student records was identified; a bounded negative, not proof of endpoint absence.

## KEY FACTS
- https://jaipur.manipal.edu/central-library.php - official library page naming Koha, Web OPAC, DSpace, Knimbus, Turnitin and linking the OPAC
- https://jaipur.manipal.edu/foa-library.php - faculty-level library page
- https://www.manipal.edu/content/dam/manipal/muj/documents/Library%20Rules-%20Ver1%20for%20Website.pdf - rules PDF: card use, fines, renewal limits, blocking
- http://manipal-koha.informindia.co.in/ - single-window OPAC entry point
- http://20.219.59.68:8080/jspui/handle/123456789/1 - repository collection page with credential-like title exposure
- http://20.219.59.68:8080/jspui/ - IP-based repository root linked from the official page
- https://muj.remotlog.com/ - RemotLog landing with resource counts and e-resource provider names
- https://jaipur-manipal-edu.muj.remotlog.com/login - RemotLog login; MUJ email as username
- https://www.mujlibrary.live/ - unverified DigiLibrary with OTP form and claimed 25,000+ books
- https://mujslcm.jaipur.manipal.edu/ - SLCM landing with no visible library link
- https://muj.slcm.jaipur.manipal.edu/ - alternate SLCM hostname, no library function visible
- https://maheblropac.koha.manipal.edu/ - MAHE Bengaluru Koha catalog; false positive control, not MUJ

## ACTIONABLE LEADS
- P0 disclosure: notify MUJ library leadership (Chief Librarian contact on central-library.php) about the credential-like repository title using redacted evidence; revoke or rotate, scrub titles and metadata, review access logs; do not test the value.
- Authorized review of OPAC borrower-account authorization with synthetic accounts: loan, renewal, fine, and blocking logic.
- Confirm ownership and canonical links for the OPAC, IP-based repository, RemotLog, and mujlibrary.live through official library channels.
- Reconcile collection counts: RemotLog reports nearly 75,000 books while mujlibrary.live claims 25,000+; label each figure by system and date.
- Verify identity boundaries: whether RFID card records, OPAC accounts, RemotLog, and SLCM share any provisioning or SSO path.
- Ask MUJ to publish an official library-systems page stating which systems are or are not connected to SLCM.

## FLAGS
- The credential-like value in the repository title is intentionally redacted in the report; reproducing or testing it is out of bounds.
- Koha attribution rests on the official page statement; the OPAC page itself does not print the Koha brand.
- mujlibrary.live ownership is unverified; treat as impersonation or squatting risk until MUJ confirms.
- RemotLog is a vendor-style subdomain with self-identification only; operator and federation unknown.
- HTTP (non-TLS) links for OPAC and repository are governance and lifecycle signals, not confirmed vulnerabilities.

## COVERAGE
49,692 chars read (file_size bytes), read to EOF, truncated=false confirmed.

DONE w2d-07-library-integration.digest.md

---

## w2d-08-placement-data.digest

## REPORT
Source file: w2d-08-placement-data.md (MUJ Placement Data and SLCM Public-Surface Assessment)

## ANSWER SUMMARY
- MUJ runs a public Directorate of Corporate Relations and Placements surface: overview, process, statistics, top recruiters, recruiter contact, and T&P team pages; recruiter-facing, not a student placement dashboard.
- The official statistics page states paid internship stipends range from INR 15,000 to INR 1,25,000 per month, but attaches no cohort, year, sample size, or methodology.
- The NIRF 2025 institution PDF (IR-O-U-0749) is the most traceable dataset: 2023-24 median salaries of INR 5,25,000 (three-year UG), INR 7,50,000 (four-year UG), INR 5,75,000 (five-year UG), INR 5,35,000 (one-year PG), and INR 6,00,000 (two-year PG), with placed-student counts per line.
- Careers360 reports 2025 headline figures (64 LPA engineering highest, 8.2 LPA engineering average, 7.6 LPA overall average, 94% placement rate, 2,100+ total offers, 1,663 unique offers); these must stay source-labelled and separate from NIRF medians.
- Third-party figures conflict: Collegedunia shows INR 88 lakhs highest while a 2022 student review on the same page reports INR 16 lakhs highest; FreeJobAlert shows INR 85 LPA highest; do not merge.
- The SLCM landing page shows student and parent sign-in with the @muj.manipal.edu label but no placement reference; placement authentication status is undetermined.
- The placement process names Placement Registration as a stage but never identifies the system; visible Apply Now and Track Application links point to the admissions domain.
- "Brochure" and "Get Placement Report" labels appear on the statistics page without any downloadable URL; leads only.

## KEY FACTS
- https://jaipur.manipal.edu/placement.php - Directorate overview and advisory scope
- https://jaipur.manipal.edu/placement-inernship.php - nine-stage process and three internship durations
- https://jaipur.manipal.edu/placement-statistics.php - stipend range and brochure or report labels
- https://jaipur.manipal.edu/placement-team-training.php - T&P team and Director Dr Sandeep Chaurasia contacts
- https://jaipur.manipal.edu/placement-contact-us.php - recruiter contact surface
- https://jaipur.manipal.edu/contact-university.php - T&P extension 751 and tpo@jaipur.manipal.edu
- https://www.nirfindia.org/nirfpdfcdn/2025/pdf/University/IR-O-U-0749.pdf - primary structured placement and median salary evidence
- https://www.careers360.com/university/manipal-university-jaipur/placement - 2025 headline statistic set
- https://collegedunia.com/college/57229-manipal-university-school-of-business-and-commerce-sbc-jaipur/placement - conflicting highest and average figures
- https://colleges.freejobalert.com/colleges/manipal-university-jaipur/placements - different latest-cycle headline set (85 LPA)
- https://www.collegedekho.com/colleges/manipal-university-placement - Udupi Manipal page, not MUJ Jaipur
- https://mujslcm.jaipur.manipal.edu/ - public login surface with no placement reference
- https://mujalumni.in/ - alumni platform described separately from T&P and SLCM
- https://jaipur.manipal.edu/nirf-home.php - NIRF index page
- https://jaipur.manipal.edu/mandatory-disclosure.php - reviewed extract shows no placement PDF link

## ACTIONABLE LEADS
- Ask T&P (tpo@jaipur.manipal.edu) for the canonical placement report or brochure URL instead of guessing filenames or probing directories.
- Archive the NIRF PDF with URL and hash as the primary placement document.
- Enforce an evidence register with source_type, reporting_year, programme_scope, metric_type, value, qualifier, and confidence fields.
- Track the discrepancy between Careers360 2025 headlines and FreeJobAlert's different cycle; reconcile with the official site when published.
- Check the admissions application flow for placement registration references (passive; it is not T&P authentication evidence).
- Authorized session testing only: determine whether Placement Registration lives inside SLCM, and whether placement uses the SLCM account.
- Include campus identity checks (city and institution match) for every collected figure.

## FLAGS
- NIRF median salary is not average package; total offers (2,100+) are not unique offers (1,663) and not placed students.
- Collegedunia figures are scoped to the School of Business and Commerce; scope loss is a stated risk.
- CollegeDekho data is for Udupi Manipal; keyword-only collection is a documented failure case.
- The Reddit "MUJ Placement Stats 2025" post is from a deleted account with no usable data.
- Stack and Microsoft 365 SSO claims are not verified; authentication status is Unknown, not same and not separate.

## COVERAGE
33,769 chars read (file_size bytes), read to EOF, truncated=false confirmed.

DONE w2d-08-placement-data.digest.md

---

## w2d-09-staff-directory.digest

## REPORT
Source file: w2d-09-staff-directory.md (MUJ SLCM and Faculty Directory Exposure Assessment)

## ANSWER SUMMARY
- MUJ's public self-disclosure document explicitly maps "Department/School/Centre Wise Faculty/Staff Details with Photographs" to https://jaipur.manipal.edu/muj-faculties.php, making the directory an intentional disclosure surface rather than a hidden asset.
- Navigation is layered: four faculties (FoSTA, FoMCA, Law, Health Sciences), four FoSTA schools, 18 department labels, and leadership routes naming deans, associate deans, directors, and HoDs.
- Representative faculty profiles publish name, designation, department, institutional email, sometimes phone, qualifications, expertise, responsibilities, memberships, and external research links (LinkedIn, IRINS, ORCID, Scopus, Google Scholar).
- Official counts do not reconcile: the home page claims 700 faculty members and the CSE page says around 120, while the faculty index exposes no total; directory completeness is unknown.
- The contact page lists 14 official rows with role mailboxes and extensions, including academics, admissions, examinations, HR, IT infrastructure, registrar, student welfare, T&P (extension 751), and webmaster.
- The SLCM landing page is only a login boundary: welcome message, Sign In, Parent Login; no evidence of bypass, account enumeration, or exposed post-login data.
- The IT page publicly describes ERP, LMS, cloud, networks, servers, backups, telecom, IT security, and Microsoft services; the SLCM FAQ links registration to the SLCM host and references Outlook and AMS support.
- Photo coverage is institutionally claimed but not quantitatively verified per profile; the FoMCA page even shows a "Faculty Members Hold PhD" counter of 0, a likely stale template artifact.

## KEY FACTS
- https://jaipur.manipal.edu/img/pdf/Public%20Self%20Disclosure-U1.pdf - official disclosure mapping faculty and staff details with photos to muj-faculties.php
- https://jaipur.manipal.edu/muj-faculties.php - teaching faculty listing entry point
- https://jaipur.manipal.edu/fosta/faculty-details.php - department-wise index; no explicit total count
- https://jaipur.manipal.edu/fosta/faculty-details.php?url=149/ - Dr Neha Chaudhary profile (Professor and HoD, CSE)
- https://jaipur.manipal.edu/fosta/faculty-details.php?url=157/ - Dr Chhatar Singh Lamba profile (Professor and Associate Dean)
- https://jaipur.manipal.edu/fosta/faculty-details.php?url=186/ - Dr Ankit Shrivastava profile (Assistant Professor Senior Scale)
- https://jaipur.manipal.edu/fosta/faculty-details.php?url=151/ - Dr Roheet Bhatnagar profile
- https://jaipur.manipal.edu/fosta/ - FoSTA home with school and department navigation
- https://jaipur.manipal.edu/fosta/department-of-Computer-Science-Engineering.php - around-120 faculty claim and research footprint
- https://jaipur.manipal.edu/contact-university.php - 14-row office contact table with role mailboxes and extensions
- https://jaipur.manipal.edu/administration-it.php - IT services description including Microsoft services and ERP and LMS
- http://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - SLCM registration FAQ; Outlook and AMS support contacts
- https://jaipur.manipal.edu/ - home page with 700-faculty institutional claim
- http://jaipur.manipal.edu/fomca - FoMCA directory with view-all controls and the anomalous zero PhD counter

## ACTIONABLE LEADS
- Directory review: field necessity, stale profiles, unnecessary direct numbers, and role-mailbox adoption, with redacted examples only.
- Owner-authorized reconciliation of the 700-faculty claim and CSE's around-120 figure against a dated roster.
- Note the faculty-details.php?url=N pattern as a potential sequential enumeration surface; testing requires written authorization.
- Use published role mailboxes (webmaster, IT infrastructure, AMS or DMS support) as the disclosure channel; no bulk directory dumps or phone lists.
- Flag the FoMCA zero PhD counter as a data-quality issue for the site owner.
- Do not reproduce the SLCM FAQ sample credential format in any team material.

## FLAGS
- 700 and 120 are approximate institutional statements with no defined scope or census date; the index total is not published.
- Photos are claimed in the disclosure category but per-profile coverage is unverified; do not count portraits.
- The ?url=N profile ID pattern suggests enumeration; passive observation only until authorized.
- Stack claims (ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai) are not independently confirmed; Microsoft service descriptions are institutional context.
- SLCM analysis stops at the unauthenticated landing page; no account or record claims are supported.

## COVERAGE
33,172 chars read (file_size bytes), read to EOF, truncated=false confirmed.

DONE w2d-09-staff-directory.digest.md

---

## w2e-01-india-uni-breach-history.digest

## REPORT
Source file: w2e-01-india-uni-breach-history.md (Indian University Portal Incidents: Lessons for MUJ SLCM)

## ANSWER SUMMARY
- Dominant risk class in 7 core Indian university incidents is privileged identity and trusted workflow abuse (4 of 7 cases), not confirmed IDOR or exposed APIs.
- Marks tampering recurred: Bengaluru North (60+ students, registrar credentials, INR 15,000-20,000 per student), Bangalore University (55 students, reported OTP bypass), Gauhati (50+ students, outsourced data entry).
- IIT Roorkee exposure of 30,000+ records via enrollment number is BOLA-like by inference, not source-confirmed IDOR.
- Payment fraud spans fake receipt forgery (Sri Venkateswara University, INR 65,686) and look-alike domain diversion (Sai Nath Educational, INR 32,000).
- Disclosure outcomes are enforcement-led: 5 of 7 core cases reached police, none published a full technical postmortem.
- AIIMS Delhi is the strongest ransomware comparator: 5 of 140 servers infected, 3-4 crore patient records hosted, theft claims reported as baseless.
- CERT-In Directions 2022 impose a six-hour incident reporting clock and 180-day in-India log retention on covered entities.

## KEY FACTS
1. https://www.thehindu.com/news/national/karnataka/uucms-portal-of-bengaluru-north-university-hacked-and-marks-of-students-tampered-with/article68740901.ece - Bengaluru North marks tampering, registrar credentials, three arrests.
2. https://m.economictimes.com/news/new-updates/how-marks-of-55-bangalore-university-students-were-illegally-changed-inside-uucms-breach-thats-shaking-karnatakas-education-system/articleshow/122039174.cms - Bangalore University OTP bypass detail, restoration of original marks.
3. https://www.ndtv.com/india-news/gauhati-university-marsheet-scam-marksheet-tampering-scam-detected-at-assams-gauhati-university-6003115 - Gauhati cash-for-marks, 9 arrests, ITI Limited data entry end.
4. https://timesofindia.indiatimes.com/city/dehradun/iit-roorkee-data-breach-exposes-personal-details-of-30k-alumni/articleshow/123220043.cms - IIT Roorkee 30k+ records, enrollment-number retrieval, ~10 year exposure.
5. https://www.cyberx9.com/physicswallah-millions-students-defense-data-exposed-blog - explicit IDOR researcher account with disclosure timeline, adjacent comparator only.
6. https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization - OWASP BOLA definition; every object ID endpoint needs an entitlement check.
7. https://www.thehindu.com/news/national/andhra-pradesh/fake-fee-receipt-scam-unearthed-in-sv-university/article71041791.ece - SVU fake receipts with forged seals and signatures.
8. https://the420.in/sai-nath-university-fake-website-student-fraud-agra/ - look-alike domain payment diversion of INR 32,000.
9. https://indianexpress.com/article/cities/delhi/aiims-cyber-attack-at-least-five-servers-infected-have-data-of-3-4-crore-patients-8297028 - AIIMS ransomware comparator; infection without proven exfiltration.
10. https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf - six-hour reporting and 180-day log retention obligations.
11. https://www.csk.gov.in/documents/IndiaRansomwareReport2022.pdf - 53% year-over-year ransomware rise, offline backup and 3-2-1 guidance.
12. https://learn.microsoft.com/en-us/entra/fundamentals/security-defaults - Microsoft security defaults: MFA registration, admin MFA, legacy auth blocking.
13. https://www.deccanherald.com/india/gujarat-technological-university-system-hacked-1200-students-personal-data-leaked-867789.html - GTU 1,200 student identity data leak, root cause undisclosed.
14. https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf - DPDP Act text; penalty maxima of INR 250 crore and INR 200 crore.
15. http://mujslcm.jaipur.manipal.edu/ - target portal, public sign-in surfaces for institutional, parent, student users.

## ACTIONABLE LEADS
- Treat marks changes as financial-grade transactions for MUJ: dual approval, step-up auth, append-only audit, after-hours and bulk-change alerts.
- Use the UUCMS precedent to argue for registrar and exam-staff identity hardening, separate admin accounts, Controlled Access review.
- Test object authorization only with authorized synthetic accounts; never change identifiers against live data.
- Prebuild a canonical payment domain list, DMARC/SPF/DKIM posture, and domain monitoring for admission season.
- Rehearse the six-hour CERT-In reporting decision and 180-day log retention for SLCM identity, app, and payment logs.
- Run a tabletop ransomware scenario covering identity, SLCM, exams, payment reconciliation, and backups.

## FLAGS
- IIT Roorkee IDOR is analyst inference; the article does not name the flaw class.
- PhysicsWallah is a researcher's account about an education company, not an independently verified university case.
- AIIMS theft claims were reported as having no factual basis; infection does not equal exfiltration.
- SVU and Sai Nath outcomes are open cases and allegations, not adjudicated facts.
- Sample is purposive and media-selected; counts do not generalize to a national rate.
- No full technical postmortem exists for any core case; credential acquisition paths are unknown.
- Reference list contains uncited entries (femtosec.io, undercoverist.org items), a possible research-noise artifact.

## COVERAGE
Chars read: 46413. EOF confirmed: yes (truncation flag false on full read).

---

## w2e-02-india-uni-vdp.digest

## REPORT
Source file: w2e-02-india-uni-vdp.md (MUJ SLCM Responsible Disclosure Playbook for India)

## ANSWER SUMMARY
- IT Act Sections 43 and 66 make authorization the hard boundary; written, asset-specific scope is required before any active validation.
- SLCM is documented as a single-window system for attendance, marks, results, and circulars, so confidentiality and exam integrity outrank technical curiosity.
- The detailed stack (ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai, M365) is a externally supplied premise, unverified by the report.
- 90 days is a coordination norm from Project Zero, not testing permission; publication must be negotiated separately.
- Indian reception varies: IIT Roorkee praised a 16-year-old finder, CBSE drew an alleged months-long silence, Zomato fixed in a day, IRCTC via CERT-In in seven days.
- CERT-In has two distinct roles: voluntary coordinated disclosure and the 2022 six-hour statutory incident duty, which does not name independent researchers.
- Severity needs two layers: a reproducible CVSS v4.0 vector plus an MUJ-specific impact statement.
- Recommended posture: policy design and passive OSINT now, no active testing until written authorization exists.

## KEY FACTS
1. http://indiacode.nic.in/bitstream/123456789/13116/1/it_act_2000_updated.pdf - IT Act text; Sections 43 and 66 define access, copying, alteration, and dishonest or fraudulent conduct.
2. https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf - six-hour incident reporting duty for specified organizations, not researchers.
3. https://www.cert-in.org.in/VulnerIncident.jsp - CERT-In voluntary coordination channel for researchers and academic institutions.
4. http://cert-in.org.in/RVDCP.jsp - CERT-In responsible disclosure and coordination policy.
5. https://projectzero.google/vulnerability-disclosure-policy.html - 90-day vendor window, 30-day post-patch disclosure, seven-day for active exploitation.
6. https://www.firstpost.com/tech/meet-the-16-year-old-who-spotted-and-fixed-a-jee-advanced-portal-flaw-before-cybercriminals-could-ws-e-14019184.html - IIT Roorkee JEE Advanced case: public praise plus disagreement over exposure scale.
7. https://www.ndtv.com/education/cbse-osm-portal-had-critical-vulnerabilities-ethical-hacker-told-ndtv-he-alerted-board-months-earlier-11550090 - CBSE researcher account of weak follow-up.
8. https://www.ndtv.com/education/cbse-admits-vulnerabilities-after-ethical-hacker-flags-alleged-exposure-11571388 - CBSE containment statement and thanks to ethical hackers.
9. https://www.thenewsminute.com/atom/zomato-hack-security-breach-its-system-not-first-time-user-information-was-compromised-62317 - Zomato reported one-day fix with post-fix publication.
10. https://certpro.com/irctc-data-breach - IRCTC insurance portal case: CERT-In report July 23, fix confirmed July 30.
11. https://www.cisa.gov/vulnerability-disclosure-policy-template - CISA model policy: 3-business-day acknowledgment, stop-on-sensitive-data rule, safe harbor for compliant work.
12. https://www.first.org/cvss/v4.0/specification-document - CVSS v4.0 bands and Base, Threat, Environmental, Supplemental metric groups.
13. https://whitehat.olacabs.com/ - Ola VDP as a first-party scope example excluding staging and sandbox.
14. http://mujslcm.jaipur.manipal.edu/ - target hostname; no public VDP or security.txt verified.
15. http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf - MAHE ICT document describing SLCM functions and high-impact records.

## ACTIONABLE LEADS
- Ask MUJ IT for a named security intake and written scope before any testing; escalate to CERT-In only for lawful coordination.
- Use the report template fields with a CVSS v4.0 vector plus an SLCM-specific impact statement.
- Propose a coordination clock: 3-business-day acknowledgment, 14-day triage, 45-day critical target, 90-day ceiling, separate publication decision.
- Track acknowledgment, technical confirmation, containment, and credit as four separate outcomes.
- Build stop conditions into team rules: stop at first sensitive record, unexpected privilege, or instability.

## FLAGS
- CBSE chronology is the researcher's claim; the board statement came later and no independent audit exists.
- Zomato and IRCTC accounts are secondary commercial or journalistic sources.
- Stack details remain unverified; do not base exploit selection on them.
- IT Act analysis is general risk guidance, not legal advice.
- The 90-day norm is a private research-team policy, not Indian law or MUJ policy.
- Reference list is noisy (Amity, Ricoh, Nokia, WHO, EFF, Red Hat entries), a possible deep-research artifact; treat body citations as the evidence core.

## COVERAGE
Chars read: 48255. EOF confirmed: yes (truncation flag false on full read).

---

## w2e-03-disclosure-case-studies.digest

## REPORT
Source file: w2e-03-disclosure-case-studies.md (India's Thin University VDP Landscape: Lessons for MUJ)

## ANSWER SUMMARY
- IISc is the only verified first-party campus-wide Indian university VDP: wildcard *.iisc.ac.in, public APIs, mobile apps, no cash bounty.
- No surveyed university expressly names a student portal in a verified VDP; IISc portal coverage is an inference from the wildcard.
- IIT Kanpur C3i research is outbound disclosure to industrial OEMs, not an inbound campus program.
- SRM Sonepat's bug bounty is an offline educational competition with no named production target and no stated prize.
- HackerOne pages for Amrita and IIT Madras are external, community-moderated directory entries that deny affiliation and validation.
- CERT-In RVDCP coordinates and may credit finders but gives no safe harbor and no blanket testing permission.
- MUJ publishes no conforming security.txt at the standard location (portal sign-in returned) and no labeled security channel; it.support@jaipur.manipal.edu is IT Infrastructure only.
- Recommended first move: governance request for written scope, then a proposed MUJ VDP modeled on IISc.

## KEY FACTS
1. https://iso.iisc.ac.in/wp-content/uploads/2025/08/RVDP.pdf - IISc VDP policy: scope, exclusions, ciso@iisc.ac.in, 5-working-day acknowledgment, no cash reward.
2. https://www.cert-in.org.in/RVDCP.jsp - CERT-In RVDCP: 72-hour acknowledgment target, 120-day resolution window, no safe harbor.
3. https://mujslcm.jaipur.manipal.edu/.well-known/security.txt - checked RFC 9116 location returns the portal sign-in page, not a security file.
4. https://jaipur.manipal.edu/contact-university.php - MUJ contact table listing it.support@jaipur.manipal.edu, extensions 778 and 300.
5. https://www.rfc-editor.org/rfc/rfc9116.html - security.txt standard; Contact and Expires are required fields.
6. https://security.cse.iitk.ac.in/responsible-disclosure - C3i page tabling Rockwell and Schneider advisories; not a campus VDP.
7. https://unstop.com/competitions/bug-bounty-srm-university-delhi-ncr-sonepat-1647952 - SRM competition listing with no target, no prize amount, and a registration fee.
8. https://hackerone.com/amrita_university - Amrita directory page: no guidelines, community-moderated, unaffiliated.
9. https://hackerone.com/indian_institute_of_techn - IIT Madras directory page with the same explicit caveats.
10. https://hackerone.com/hacktivity/overview - Hacktivity feed: searchable report metadata, evidence only, not scope.
11. https://www.bugcrowd.com/products/vulnerability-disclosure/ - Bugcrowd VDP model and safe-harbor discussion for disclosure.
12. https://www.openbugbounty.org/faq/ - hosted programs versus generic non-intrusive reporting; platform pays no bounties.
13. http://yeswehack.com/programs - YesWeHack directory checked; no Indian university program verified in the snapshot.
14. https://hackerone.com/directory/programs - Directory context: presence is not authorization.
15. https://www.hackerone.com/bug-bounty-programs - HackerOne bounty program background page.

## ACTIONABLE LEADS
- Email MUJ IT Infrastructure asking whether a private VDP exists and who owns SLCM security intake; do not test while waiting.
- Draft a MUJ VDP on the IISc model: policy URL, valid security.txt, named assets, explicit portal status, prohibited techniques, response targets, safe-harbor wording.
- Have MUJ classify Akamai, M365 identity, payment services, parent login, APIs, and vendor backends before any scoped test.
- Use CERT-In only for post-discovery coordination, never as pre-authorization.
- Treat Hacktivity and Open Bug Bounty records for academic domains as disclosure history, not scope.

## FLAGS
- IISc portal coverage is a labeled inference; the policy excludes third-party services and automated-tool findings.
- SRM listing shows no target or prize; its registration fee is not a bounty.
- Amrita and IITM pages explicitly deny affiliation and validation.
- "Not found" for other universities is a survey result, not proof of absence; no authoritative national registry exists.
- The security.txt check is a single observed URL state; content may change.

## COVERAGE
Chars read: 35627. EOF confirmed: yes (truncation flag false on full read).

---

## w2e-04-slcm-vendor-id.digest

## REPORT
Source file: w2e-04-slcm-vendor-id.md (Identifying the Vendor Behind Manipal's SLCM)

## ANSWER SUMMARY
- The vendor behind the current MUJ SLCM backend is not publicly established; SLCM is best modeled as an ecosystem label with separate layers (portal, ERP core, identity, hosting, integrator).
- MAHE SIS pages carry direct in-house credits: "Information Systems Department, Manipal Academy of Higher Education" and "Department of Digital and Information Technology".
- SAP Student Lifecycle Management is the strongest historical packaged-core lead: self-reported implementation across Manipal Education entities in 2012 and configuration from 2011.
- Salesforce (Agentforce Education, Data 360, MuleSoft, Tableau) and Deloitte (implementation) are confirmed 2026 modernization roles for MAHE.
- Comviva, Manipal Technologies, JAIN/JGI, and Unikul are unsupported for MUJ; an Unikul Dubai customer story remains unconfirmed.
- Passive clues (RequestVerificationToken, jQuery validation, Microsoft password reset) show framework conventions, not ERP authorship.
- Recommended safe wording separates the SIS layer, historical SAP core, current MUJ backend (unconfirmed), and Salesforce modernization.

## KEY FACTS
1. https://mujslcm.jaipur.manipal.edu/ - MUJ portal, no vendor credit, form fields and Microsoft password-reset link observed.
2. https://sis.manipal.edu/ - current MAHE SIS, footer credits Department of Digital and Information Technology.
3. https://sis.manipal.edu/studloginSLCM.aspx - SIS login route with the older Information Systems Department attribution.
4. https://slcm.manipal.edu/ - classic MAHE SLCM endpoint, no vendor credit in reviewed content.
5. https://slcm.manipaldubai.com/ - Dubai student portal host linked from the official campus page.
6. https://student.manipal.edu.my/ - Malaysia portal using Scholar E-Mail ID language.
7. https://maheslcmtech.manipal.edu/ - modernization endpoint exposing a Microsoft tenant SAML path.
8. https://www.salesforce.com/in/news/press-releases/2026/03/26/manipal-university-ai-transformation/ - Salesforce MAHE announcement naming products and Deloitte as integrator.
9. https://www.manipal.edu/mu/news-events/mahe-introduces--magic--to-power-ai-driven-academic-and-administ.html - MAGIC program, five AI agents placed in SLCM.
10. http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf - MAHE ICT inventory defining SLCM as the single-window academic suite.
11. https://linkedin.com/in/adrija-sen-91631110 - profile reporting SAP SLcM implementation across Manipal Education entities in 2012.
12. https://linkedin.com/in/poornima-vishwaradhya-a0b95b22 - profile reporting SAP SLcM configuration at Manipal Global from March 2011.
13. http://sap.com/products/erp/student-lifecycle-management-for-sap-s4hana-cloud-private-edition.html - SAP SLCM product scope across the student journey.
14. https://unikul.com/overview - Unikul Dynamics 365-based SLCM product page with no Manipal reference.
15. https://campusdynamix.com/slcm-for-universities - unnamed Dubai Academic City customer that replaced SAP; possible MAHE Dubai link, unconfirmed.

## ACTIONABLE LEADS
- Request an approved architecture summary and software bill of materials from MUJ's authorized IT or data-protection contact.
- Ask for procurement records, contracts, and privacy notices to settle attribution without touching protected functions.
- Keep MUJ, MAHE SIS, Dubai, Malaysia, and maheslcmtech in separate evidence buckets.
- Verify LinkedIn-derived leads against first-party documents before any claim.
- Confirm whether the alternate host muj.slcm.jaipur.manipal.edu (seen in other reports) is a live alias or a stale entry.

## FLAGS
- LinkedIn profiles are self-reported; no first-party MUJ-to-SAP contract or architecture document exists.
- The Unikul customer story names no customer; geographic fit with Dubai Academic City is a low-confidence inference.
- In-house footers appear on MAHE SIS pages, not on the MUJ page; extension to MUJ is inference.
- "MVC 5.3" and the rest of the stack are externally supplied; the page capture does not establish package versions.
- Reference 16 is titled "login.microsoftonline.com" while its URL is maheslcmtech.manipal.edu, a labeling oddity worth rechecking.

## COVERAGE
Chars read: 34493. EOF confirmed: yes (truncation flag false on full read).

---

## w2e-05-india-erp-vendors.digest

## REPORT
Source file: w2e-05-india-erp-vendors.md (MUJ SLCM and India's University ERP Risk Landscape)

## ANSWER SUMMARY
- No reviewed public source attributes MUJ SLCM to Saral, GateWay, Hexad, Simpliance, Jeewane, MasterSoft, Serosoft, Fedena, TCS iON, or Samarth.
- The named list mixes categories: Saral and MasterSoft are real education ERPs, Simpliance is compliance SaaS, Hexad shows no university ERP, GateWay and Jeewane do not resolve.
- Fedena 2.3 open-source is the only strong product-specific vulnerability record: seven findings including auth bypass and RCE, unsupported with no patches planned.
- ".NET portal" is an architectural class, not a vendor identity; historical Fedena used Ruby, Rails 2.3.5, and MySQL.
- Strong identity does not replace application authorization: Entra and phishing-resistant MFA cannot stop IDOR without per-object checks.
- Akamai protects a boundary, not the whole application; origin TLS and authorization are origin obligations.
- ".NET Framework 4.x" spans retired releases (4.5.2, 4.6, 4.6.1 retired April 2022) and 4.6.2 (listed end January 2027); the label is too broad for support decisions.
- The immediate mission should be authorized inventory, role-matrix testing, and supplier assurance, not unapproved probing.

## KEY FACTS
1. https://mujslcm.jaipur.manipal.edu/ - target portal; discloses no product or framework version.
2. http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf - MAHE document listing SLCM functions.
3. http://erp.saral.in/sch - SARAL School Soft ERP by Saral Computers, in service since 1990.
4. https://cimsstudentnewui.mastersofterp.in/ - MasterSoft student portal with credential warning text.
5. http://iitms.co.in/ - MasterSoft Education ERP for schools and higher education.
6. https://serosoft.com/solutions - Academia by Serosoft product family.
7. https://www.hexad.in/ - Hexad corporate page; no university ERP product shown.
8. https://www.aparajitha.com/products/vendor-audit - Simpliance Vendor, compliance-audit SaaS, category mismatch.
9. https://www.tcsion.com/institutions/higher-education - TCS iON higher-education suite scope.
10. https://samarth.edu.in/ - Samarth eGov digital-campus initiative.
11. https://pentest.co.uk/labs/research/fedena-school-management-software/ - seven Fedena 2.3 findings with named CVEs and remediation stance.
12. https://pentest.co.uk/labs/fedena-authentication-bypass-cve-2021-27980/ - default client-side sessions with a static public secret, admin-level access.
13. https://github.com/projectfedena/projectfedena_v2.0 - Fedena 2.0 source showing Ruby, Rails 2.3.5, MySQL.
14. https://learn.microsoft.com/en-us/lifecycle/products/microsoft-net-framework - lifecycle dates separating supported from retired 4.x releases.
15. https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html - per-object server-side authorization requirement.

## ACTIONABLE LEADS
- Ask MUJ IT for a versioned SBOM covering Windows, IIS, CLR, MVC packages, NuGet, database, Akamai configuration, and identity integration.
- Obtain contracts and data-flow diagrams to resolve GateWay, Jeewane, and Hexad attribution; wrong vendor contact is itself a risk.
- Review Entra Conditional Access exports, phishing-resistant MFA coverage, and privileged-role policies.
- Build a role-object-action matrix (student, parent, faculty, examiner, finance, helpdesk, admin) and test only in an approved tenant.
- If an exact Fedena 2.3 tenant exists anywhere, isolate and migrate; WAF mitigation was declared incomplete.
- Collect supplier assurance packs: pentest summaries, remediation SLAs, disclosure policies, subprocessor records.

## FLAGS
- All vendor attributions to MUJ are unverified; "no advisory found" is an evidence gap, not proof of safety.
- Fedena findings apply to the unsupported 2.3 open-source branch, not current Fedena and not MUJ.
- The supplied stack remains a externally supplied hypothesis; SQL Server is only an ecosystem guess.
- ViewState and machine-key discussion is reference architecture, not a MUJ finding.
- The alternate hostname muj.slcm.jaipur.manipal.edu appears in references as a portal surface; treat as unverified alias.

## COVERAGE
Chars read: 40473. EOF confirmed: yes (truncation flag false on full read).

---

## w2e-06-mit-manipal-systems.digest

## REPORT
Source file: w2e-06-mit-manipal-systems.md (MIT Manipal Signals for Defending MUJ SLCM)

## ANSWER SUMMARY
- MIT/MAHE public evidence transfers as workflow test cases, not as confirmed MUJ vulnerabilities; overall confidence rated 0.78, medium-high.
- MAHE ICT report defines SLCM: attendance, internal and external marks, results, circulars, single window for students and parents.
- Front doors differ: sis.manipal.edu, slcm.manipal.edu, and the MUJ portal; reviews must inventory redirects, identity handoffs, and role boundaries.
- Unofficial automation demand is documented: slcmAPI (2020, deprecated after CAPTCHA), SLCM-is-Dumb (2025, digit CAPTCHA automation), SLCM_APP (2025, Flutter/FastAPI with custom credential logic).
- No public Manipal SLCM vulnerability disclosure was located; that is a bounded OSINT result, not proof of absence.
- "ASP.NET MVC 5.3" is unverified; public NuGet evidence points to Microsoft.AspNet.Mvc 5.2.9, and 4.5.2/4.6/4.6.1 retired in April 2022.
- Office 365 is MAHE-wide; identity lifecycle crosses the Microsoft and SLCM boundary, making recovery and session revocation key controls.
- Priority is control validation (MFA coverage, role isolation, session revocation, origin restriction) in owner-run environments, not exploitation.

## KEY FACTS
1. https://mujslcm.jaipur.manipal.edu/ - target portal with student and parent entry choices.
2. https://slcm.manipal.edu/ - MAHE-branded SLCM endpoint, family relevance.
3. https://sis.manipal.edu/ - SIS limited to bona fide MAHE members.
4. http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf - ICT report: SLCM functions plus O365, Teams, Brightspace, Impartus, Moodle, EduNxt.
5. https://github.com/sankalp2004/SLCM-is-Dumb - 2025 CGPA scraper advertising digit-CAPTCHA automation.
6. http://github.com/canaryGrapher/slcmAPI - 2020 API, deprecated after CAPTCHA was introduced.
7. http://github.com/DK10WS/SLCM_APP - 2025 MUJ mobile app with custom email/password logic and no stated credential-storage rule.
8. https://github.com/nikeplusdash/SLCM-api - API for slcm.manipal.edu that advises session logout.
9. https://mujstella.in/ - independent student platform with an explicit non-affiliation disclaimer.
10. https://www.manipal.edu/mit.html - MIT official presence inside the MAHE domain.
11. https://www.nuget.org/packages/Microsoft.AspNet.Mvc/5.2.9 - public MVC package evidence that contradicts the "5.3" label.
12. https://learn.microsoft.com/en-us/entra/identity/conditional-access/policy-block-legacy-authentication - legacy auth linked to 97%+ of credential stuffing and 99%+ of password spraying; Report-only staging guidance.
13. https://techdocs.akamai.com/origin-ip-acl/docs/welcome - Origin IP ACL guidance for restricting direct-origin traffic.
14. https://libportal.manipal.edu/ - library portal maintained by Digital and Information Technology.
15. https://admin.mit659.examly.io/login - publicly indexed MIT-branded Examly admin login; ownership and current use unverified.

## ACTIONABLE LEADS
- Produce an exact SBOM for OS, IIS, .NET Framework, MVC packages, jQuery, and authentication middleware.
- Run Conditional Access changes in Report-only mode first; keep emergency accounts outside blocking policies.
- Test student/parent authorization boundaries with synthetic accounts in an approved environment.
- Verify anti-forgery coverage on every state-changing route and session renewal, logout, and revocation behavior.
- Restrict origin acceptance to Akamai paths and monitor for direct-origin traffic.
- Decide between a sanctioned read-only API and an explicit no-integration policy; warn students against giving passwords to third-party tools.
- Keep CAPTCHA but layer rate, risk, session, and anomaly controls on top.

## FLAGS
- Repository maintainers' MIT Manipal student status is unverified (report assigns 0.15 confidence).
- MVC 5.2.9 versus 5.3 discrepancy; IIS 10 and Akamai are requester-supplied premises.
- Repository claims are self-descriptions; nothing was executed or verified.
- No attributable Manipal vulnerability disclosure exists; do not claim one.
- MUJStella is independent and not affiliated with MUJ.
- Examly admin login ownership is medium-low confidence; do not treat as an official MIT system without confirmation.

## COVERAGE
Chars read: 36693. EOF confirmed: yes (truncation flag false on full read).

---

## w2e-07-manipal-dubai.digest

## REPORT
Source file: w2e-07-manipal-dubai.md (MAHE Dubai Student Systems: A MUJ SLCM Security Comparison)

## ANSWER SUMMARY
- Official MAHE Dubai site links its Student Portal to https://slcm.manipaldubai.com/; the login page exposes password recovery and a return link to the institution.
- Dubai public markup shows classic ASP.NET Web Forms artifacts; MUJ shows MVC-style anti-forgery and validation artifacts. A shared backend or database is unproven.
- Two UNIKUL Dev Team Android listings exist: MAHE DUBAI-SLCM (package com.unikul.manipaldubai, 1K+ downloads, updated Aug 29 2025) and M-Campus (package com.unikul.mahedubai, 50+ downloads, updated Aug 6 2026), with overlapping academic functions.
- Dubai's cleaned login content names no Microsoft or external identity provider; MUJ displays @muj.manipal.edu and student and parent modes. Identity and tenant equivalence must not be assumed.
- The app listing declares no data collection or sharing yet links a generic timbernile.com privacy page with no contact and no app-specific terms; a governance gap.
- No attributable public cyber incident for MAHE Dubai was found. This is a bounded negative, not a clean bill of health.
- The MUJ stack (MVC 5.3, .NET 4.x, IIS 10, Akamai, M365) stays a client-supplied baseline; this review did not independently verify it.
- Verdict: moderate-high confidence that Dubai is a separate application generation or implementation; recommend documentation, phishing education, synthetic tabletop, and owner-approved assurance only.

## KEY FACTS
1. https://slcm.manipaldubai.com/ - official Dubai SLCM student portal; password recovery and sign-in surface.
2. https://www.manipaldubai.com/ - institutional site that publishes the Student Portal link.
3. https://play.google.com/store/apps/details?id=com.unikul.manipaldubai&hl=en-US - MAHE DUBAI-SLCM app listing, 1K+ downloads.
4. https://play.google.com/store/apps/details?id=com.unikul.mahedubai&hl=en-US - M-Campus app listing, 50+ downloads, later update.
5. https://timbernile.com/privacy%20policy.php - external generic privacy page linked by the app; no contact details.
6. https://www.manipaldubai.com/privacy-policy - Dubai site claims only necessary and functional cookies.
7. https://www.manipaldubai.com/terms-and-conditions - terms cover voluntary contact data, no sale, deletion requests.
8. https://www.manipaldubai.com/student-policies - repeats the official Student Portal destination.
9. https://www.manipaldubai.com/student-services - repeats the same SLCM destination.
10. https://www.manipaldubai.com/how-to-apply - admissions guidance; no separate auth system identified.
11. https://slcm.manipal.edu/ - main MAHE SLCM login, same SLCM label family, Web Forms-style recovery.
12. https://www.manipal.edu/mu/policies/it-policy.html - MAHE IT policy scope covers faculty, staff, students, and third parties.
13. https://mujslcm.jaipur.manipal.edu/ - MUJ portal with @muj.manipal.edu suffix; comparison baseline.
14. https://www.uaelegislation.gov.ae/en/legislations/1972 - UAE Federal Decree-Law 45/2021 (PDPL) processor duties, DPO, breach reporting.
15. http://cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf - Indian CERT-In context relevant to the MUJ side.

## ACTIONABLE LEADS
- Ask MAHE Dubai IT to publish a canonical asset directory: SLCM URL, current app, package ID, support contact, retired apps.
- Verify Dubai identity provider, tenant, MFA, and recovery with the owner before applying MUJ identity assumptions.
- Request an app-specific privacy notice from UNIKUL covering controller, processor, purposes, retention, deletion, security contact, SDKs.
- Check both Play Store packages for deprecation status and which one is endorsed for current students.
- Authorized staging review only: password recovery enumeration resistance, session cookie flags, CSRF, lockout, error handling.
- Build a joint incident matrix with UAE and Jaipur decision trees; no public security or privacy mailbox exists on reviewed pages.
- Run a synthetic-data tabletop (grade change reports after a mobile release) with no real accounts.

## FLAGS
- The "no data collected, no data shared" app claim sits in tension with advertised academic-record functions; report calls it not automatically contradictory but weakly documented.
- M-Campus update date of Aug 6 2026 and MAHE DUBAI-SLCM update of Aug 29 2025 come from store listings; snapshot values.
- Reference 2 in the source is a malformed citation (empty label pointing at slcm.manipaldubai.com); citation-number reliability is inconsistent.
- Web Forms vs MVC divergence is an inference from passive artifacts, moderate confidence.
- No Dubai incident found is absence-of-evidence; some incidents are resolved privately.
- Slcm.manipal.edu and slcm.manipaldubai.com are separate hosts; do not merge findings across them.

## COVERAGE
- Chars read: 36,253
- EOF confirmed: yes (truncated: false on final page, 242 of 242 lines)

---

## w2e-08-sikkim-manipal.digest

## REPORT
Source file: w2e-08-sikkim-manipal.md (SMU Student Systems OSINT: Exposure, Evidence, and MUJ Similarity)

## ANSWER SUMMARY
- SMU exposes three current surfaces: SMUERP v5 (erp.smu.edu.in) with student, employee, and email logins, Vidya (vidya.smu.edu.in) powered by KEN with an SMU O365 sign-in, and an admissions portal at apply.smu.edu.in. Treat as separate applications.
- SMUERP v5 publishes .aspx student and payment routes and describes a modular common-database ERP; this points to a legacy Web Forms style, not an evidenced MVC clone of MUJ. Exact versions unknown.
- Vidya is vendor-backed (KEN) and offers "Login with SMU O365"; identity-layer similarity to MUJ is strong, shared codebase is unproven.
- The official examination manual assigns staff roles for marks entry, watermarked password-protected scanned scripts, backups to virtual server and external drive, and online result publication; a higher control tier.
- Legacy SMU-DE inventory: EduNxt, an Azure-hosted exam booking system, results.smude.edu.in, myzone.smude.edu.in, and an SMUDE app; phishing residue risk after decommissioning.
- No confirmed public SMU cyber incident found. A 2020 Change.org petition (236 supporters) alleges examination delays, not a portal exploit.
- The official students page links an external domain ecm.org.in as one Student Login destination; ownership unverified, not proven malicious.
- Ports were not tested and are marked "Not established".

## KEY FACTS
1. https://erp.smu.edu.in/ - SMUERP v5 home with student, employee, and email login choices.
2. https://erp.smu.edu.in/common/loginstd.aspx - student path using registration number with password recovery.
3. http://erp.smu.edu.in/GenPay/QuickPay.aspx - Quick Pay collects user type, phone, email, amount, description; published as HTTP.
4. https://vidya.smu.edu.in/ - Vidya login, student email, Remember Me, Forgot Password, SMU O365, powered by KEN.
5. https://apply.smu.edu.in/ - admissions session portal, separate from the continuing-student ERP.
6. https://smu.onlinemanipal.com/ - SMU online degree marketing umbrella (BBA, MBA, MCA, BA, MA, M.Com/B.Com).
7. https://edunxt.smude.edu.in/?q=MULNLogin/edunxtlogin - historical EduNxt existing-student login link.
8. http://smu-oebs-lb.centralindia.cloudapp.azure.com/SMUOEBS/Default.aspx - historical Azure-hosted Examination Booking System.
9. http://results.smude.edu.in/ - historical SMU-DE results destination.
10. http://myzone.smude.edu.in/ - historical re-registration/re-sit workflow surface.
11. https://ecm.org.in/ - external Student Login link from the official students page; ownership anomaly.
12. https://learning.onlinemanipal.com/d2l/home/12169 - D2L-style route with unsupported-browser page; no SMU branding, unattributed.
13. https://www.smu.edu.in/students.php - official students page publishing ERP, login, fee, and grievance links including HTTP URLs.
14. https://www.smu.edu.in/img/content/dam/manipal/smu/IQAC/Examination-Manual-of-SMU-Tadong-Campus.pdf - exam manual documenting marks, scripts, backups, publication.
15. https://www.change.org/p/dr-ramesh-pokhriyal-nishank-online-exams-should-also-be-conducted-cancelled-for-smu-de-as-already-declared-for-regular-smu-students - 2020 petition, 236 supporters, operational grievance.

## ACTIONABLE LEADS
- Canonicalize HTTPS for published HTTP ERP and Quick Pay links; validate HSTS and redirects with the owner.
- Verify ecm.org.in ownership and purpose through SMU IT; monitor for domain and certificate changes.
- Inventory legacy SMU-DE DNS, Azure resources, certificates, and support identities for phishing residue.
- Authorized review of Quick Pay input validation, reconciliation, fraud monitoring, and privacy controls.
- Correlate O365, Vidya, ERP, and helpdesk identity events; enforce MFA and conditional access for SMU O365.
- Test IDOR and account enumeration resistance only under written scope, given registration-number logins.
- Propose a SMU vulnerability-disclosure policy; none was found. MUJ-side reports can route to registrar@jaipur.manipal.edu.

## FLAGS
- Web Forms inference for SMUERP is medium confidence, based on .aspx routes and ERP description only.
- ecm.org.in is anomalous but not proven malicious, misconfigured, or obsolete.
- Scribd manuals and FAQ are user-uploaded; provenance and completeness limited.
- Historical SMU-DE endpoints: current status not claimed; do not treat as live.
- Petition allegations are unverified by the source; not evidence of a security defect.
- MUJ baseline (MVC 5.3, .NET 4.x, IIS 10, Akamai, M365) is supplied input, not revalidated here.

## COVERAGE
- Chars read: 37,861
- EOF confirmed: yes (truncated: false on final page, 286 of 286 lines)

---

## w2e-09-manipal-malaysia.digest

## REPORT
Source file: w2e-09-manipal-malaysia.md (MIU SLCM Public Footprint and Shared-Codebase Verdict)

## ANSWER SUMMARY
- student.manipal.edu.my exposes student sign-in labeled "Scholar E-Mail ID", a separate parent username/password flow, forgot-password, and public account creation at /auth/registration.
- Entity attribution is ambiguous: the MQA register lists MILA University as formerly Manipal International University (Nilai), while the manipal.edu.my helpdesk brands itself MUCM. Confirmed ownership of the student subdomain is needed.
- The registration form requests username, first name, last name, email, phone, and password confirmation; consent, privacy notice, and retention deserve priority review.
- Public markup shows a client-rendered shell, hashed static assets, kt_ style identifiers, and a Microsoft-branded student control; a React-style SPA front end is plausible, back end unknown.
- Microsoft Clarity references in markup raise analytics governance and under-18 targeting questions.
- The only attributable SLCM complaint found concerns Manipal Jaipur ("Slcm portal issue", password rejected), not Malaysia; no Malaysia complaint corpus was located.
- The MUJ stack (MVC 5.3, .NET 4.x, IIS 10, Akamai, M365) is not evidenced for Malaysia; do not transfer version claims.
- Verdict: shared SLCM product family is plausible, shared codebase is not demonstrated, and back-end technology is low confidence/unknown.

## KEY FACTS
1. https://student.manipal.edu.my/ - Malaysian portal login; student and parent flows.
2. https://student.manipal.edu.my/auth/registration - public registration route collecting identity and contact data.
3. https://helpdesk.manipal.edu.my/ - MUCM Helpdesk branding with ticketing on the parent namespace.
4. https://www2.mqa.gov.my/mqr/english/eakrKPList.cfm?IDAkrIPTS=629 - regulator record: MILA University previously known as MIU.
5. https://manipal.edu.my/ - parent domain serving a generic "One moment, please..." page.
6. http://reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue - the single attributable SLCM complaint, Jaipur, password rejected.
7. https://mujslcm.jaipur.manipal.edu/ - MUJ portal with /Home/Index style entry and parent login; comparison baseline.
8. https://slcm.manipal.edu/sendtoportal - MAHE "MU SLcM" send-to-portal artifact in the same product family.
9. https://mila.edu.my/about-us/ - MILA site page not found, supporting the entity change.
10. https://www.manipal.edu/mu/important-links/world-wide-manipal/manipal-international-university.html - historical MIU business profile.
11. https://www.pdp.gov.my/ppdpv1/en/personal-data-protection-standard-2015 - Malaysian PDP standard for storage, security, deletion.
12. https://learn.microsoft.com/en-us/clarity/faq - Clarity session recordings, heatmaps, under-18 warning.
13. https://pages.nist.gov/800-63-4/sp800-63b.html - AAL2 phishing-resistant authentication guidance.
14. https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html - session controls baseline for the owner review.
15. https://techdocs.akamai.com/property-mgr/docs/web-app-firewall - Akamai WAF capability context; edge controls are not application proof.

## ACTIONABLE LEADS
- Confirm with university IT the legal operator, data controller, incident contact, and disclosure channel for student.manipal.edu.my before any report routing.
- Authorized check of registration abuse controls: eligibility, email verification, rate limits, breached-password screening, duplicate accounts.
- Verify Clarity presence, masking settings, and age suitability with the operator.
- Review parent-account lifecycle: governance, rate limiting, revocation when relationships end.
- Request aggregated helpdesk categories (login failures, recovery, registration errors) instead of probing live systems.
- Internal comparison of repositories, SBOMs, API contracts, and identity app registrations before assuming defect propagation across campuses.

## FLAGS
- React-style SPA hypothesis is moderate confidence from markup only; back end could be ASP.NET, Java, Node, PHP, or other.
- Microsoft branding does not prove an Entra tenant, protocol, or MFA posture, and no tenant metadata was collected.
- Clarity reference is in public markup; what is captured is unknown.
- MILA/MIU/MUCM attribution ambiguity can misroute disclosures and complaints.
- No Malaysia complaints found is absence of indexed evidence, not evidence of absence.
- Registration password hint (8+ mixed characters) is UI text; server-side enforcement unproven.

## COVERAGE
- Chars read: 37,184
- EOF confirmed: yes (truncated: false on final page, 256 of 256 lines)

---

## w2e-10-keentheme-portals.digest

## REPORT
Source file: w2e-10-keentheme-portals.md (What Keen Demo1 Paths Reveal About MUJ SLCM)

## ANSWER SUMMARY
- MUJ's login front end is confirmed as Keen product lineage via archived asset paths /keen/themes/keen/theme/demo1/dist/ with login-v1.css, style.bundle.css and plugin bundles.
- Exact Keen release is unknown; no version banner or manifest. Defensible label: "Keen, legacy generation, exact release unverified".
- demo1 is a layout/build identifier, not a version number, not a staging flag, and not evidence of default accounts or an exposed admin panel.
- Two high-confidence Metronic-family comparators: Netkampuss ERP (sch-avms.netkampus.in, HOST_URL to the Metronic preview tool) and Avenu Learning LMS India (learn-india.avenulearning.com); neither discloses a version.
- No gov.in portal is confirmed as Keen/Metronic in this evidence set; Assam University and LFMEAB pages are excluded as false positives.
- OBB-4445862 (XSS on preview.keenthemes.com, reported Jan 12 2026, unpatched at review) is labeled Custom Code, not distributed theme JavaScript; it does not prove a MUJ theme XSS.
- Bootstrap and jQuery CVEs (2019-8331, 2020-11022, 2020-11023, 2019-11358) are conditional on exact deployed versions and data flows; not MUJ findings.
- Recommended next step is an owner-approved source and SBOM review, not Internet-side testing.

## KEY FACTS
1. https://mujslcm.jaipur.manipal.edu/ - visible MUJ PORTAL login, the theme target page.
2. http://web.archive.org/cdx/search/cdx?collapse=urlkey&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&output=json&url=mujslcm.jaipur.manipal.edu/* - archive inventory proving the /keen/.../demo1/dist/ asset paths.
3. https://mujslcm.jaipur.manipal.edu/Home/Index - /Home/Index route, MVC-convention compatible.
4. https://keenthemes.com/metronic/changelog - Metronic changelog showing dependency security fixes; no version bridge to MUJ.
5. https://preview.keenthemes.com/keen/demo1 - official Keen demo1 preview; product naming source.
6. https://www.openbugbounty.org/reports/4445862/ - preview.keenthemes.com XSS, component labeled Custom Code.
7. https://sch-avms.netkampus.in/ - Netkampuss ERP page with KT globals and Metronic preview HOST_URL.
8. https://learn-india.avenulearning.com/ - Avenu Learning LMS India login with canonical KT bundle paths.
9. https://ausexamination.ac.in/ - Assam University exam page; excluded, generic bundle filename only.
10. https://demo-compliance.smart-office365.com/ - LFMEAB styled page; excluded, not an official gov.in domain.
11. https://nvd.nist.gov/vuln/detail/CVE-2019-8331 - Bootstrap tooltip/popover XSS; conditional check only.
12. https://nvd.nist.gov/vuln/detail/CVE-2020-11022 - jQuery DOM-manipulation XSS; conditional check only.
13. https://nvd.nist.gov/vuln/detail/CVE-2020-11023 - jQuery option-element XSS; conditional check only.
14. https://nvd.nist.gov/vuln/detail/CVE-2019-11358 - jQuery Object.prototype pollution; conditional check only.
15. https://owasp.org/www-project-dependency-check - tool for automated component inventory in the authorized review.

## ACTIONABLE LEADS
- Ask the MUJ owner for the licensed Keen package version, source repo tag, build job, package.json, and lockfile.
- Generate an internal SBOM for the deployed front-end build; map only version-applicable CVEs.
- Compare deployed static-file hashes against approved builds to find drift and stale bundles.
- Inventory deployed sample pages and source maps; remove unnecessary vendor material.
- Review custom JavaScript DOM sinks (URL, message, profile, server data) before claiming XSS conditions.
- Verify CSP, cookies, anti-forgery, login throttling, and identity config under written authorization.
- Assign ownership and update cadence for the theme to prevent orphaned vendor assets.

## FLAGS
- Any Keen v1.x, Bootstrap 4, or patch-level claim in the wild would be unsupported; the report explicitly avoids guessing versions.
- OBB-4445862 concerns preview-host custom code; do not generalize to the distributed theme or to MUJ.
- urlscan.io API query (reference 9) is cited as supporting evidence but no results are shown in the report; treat as weak secondary support.
- devs.keenthemes.com forum answer (reference 8) is unverified community content.
- demo1 must not be treated as a routable application route, dev environment, or authentication bypass.
- Generic filenames like style.bundle.css alone are not distinctive (Assam case demonstrates the false-positive boundary).

## COVERAGE
- Chars read: 33,727
- EOF confirmed: yes (truncated: false on final page, 251 of 251 lines)

---

## w2e-11-iis-mvc-student-portals.digest

## REPORT
Source file: w2e-11-iis-mvc-student-portals.md (Benchmarking MUJ SLCM Against Indian ASP.NET Portals)

## ANSWER SUMMARY
- Amizone is the strongest MVC-family near peer; LPU UMS, Chandigarh CUIMS, and MAHE SLCM show classic Web Forms markers; Sharda eSharda and Manav Rachna remain stack-unverified functional candidates.
- Identity is MUJ's clearest positive signal: realm discovery marks muj.manipal.edu and jaipur.manipal.edu as managed Microsoft tenants, and the June 2025 MUJ SOP documents mandatory Office 365 MFA.
- MVC 5.3.0 is a real NuGet package (.NET 4.5+, last update Oct 23 2023); the real lifecycle risk is the vague ".NET Framework 4.x" label, since only 4.8.1 remains supported on supported Windows.
- Three incident cases frame the benchmark: Kashmir 2022 alleged data sale, Surya Shakti Infotech admissions ransomware (June 2025), and the JEE Advanced cloud misconfiguration (June 2026); none ties to MUJ SLCM.
- The LPU plaintext-credential claim is uncorroborated first-person reporting with no institutional confirmation or remediation record.
- Eight defensive classes frame the checklist: runtime ambiguity, split identity and weak recovery, authorization, session and CSRF, upload/export, errors and headers, CDN-to-origin trust, logging and disclosure.
- CERT-In 2022 Directions impose six-hour incident reporting for listed incidents and 180-day India-resident log retention; rehearse the clock in a tabletop.
- A 90-day roadmap starts with asset and identity inventory and ends with an authorized assessment; the report authorizes no testing.

## KEY FACTS
1. https://mujslcm.jaipur.manipal.edu/ - target portal with student and parent login paths.
2. https://muj.slcm.jaipur.manipal.edu/ - alternate MUJ front door ("WELCOME TO MUJ PORTAL").
3. https://student.amizone.net/ - Amizone; MVC-family near peer with parent visibility.
4. https://ums.lpu.in/lpuums - LPU legacy UMS; home-grown ERP with Web Forms state markers.
5. https://studentums.lpu.in/login - separate modern LPU login, coexistence case.
6. https://uims.cuchd.in/ - Chandigarh CUIMS student and parent ERP; Web Forms markers, old jQuery filename.
7. https://slcm.manipal.edu/ - MAHE SLCM; Web Forms markers and jQuery 2.0.3 asset path, closest organizational comparator.
8. https://www.nuget.org/packages/Microsoft.AspNet.Mvc - MVC 5.3.0 package facts, .NET 4.5+ target.
9. https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-framework - .NET Framework support policy; 4.8.1 supported, earlier 4.x retired.
10. http://login.microsoftonline.com/getuserrealm.srf?login=probe@muj.manipal.edu&xml=1 - realm discovery result: managed tenant for muj.manipal.edu.
11. http://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf - MUJ SOP; MFA mandatory before Office 365 use.
12. https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf - six-hour reporting, 180-day logs, clock sync duties.
13. https://kashmirobserver.net/2022/08/10/kashmir-university-hacking-data-of-1-million-students-found-on-dark-web/ - Kashmir 2022 alleged sale case, unconfirmed database.
14. https://timesofindia.indiatimes.com/city/kolkata/ransomware-targets-it-firm-handling-college-admissions/articleshow/122119513.cms - admissions-provider ransomware case, June 2025.
15. https://www.rfc-editor.org/rfc/rfc9116.html - security.txt standard for the disclosure route.

## ACTIONABLE LEADS
- Resolve exact .NET and Windows builds, then grade lifecycle support; do not accept ".NET 4.x" as sufficient.
- Confirm MFA coverage for every SLCM role including parent and any local fallback paths.
- Build a role-object authorization matrix with staging denial tests for cross-user and cross-role access.
- Audit session cookies, CSRF coverage on every state-changing form, uploads, exports, and bulk downloads.
- Verify Akamai-to-origin TLS, origin ACL, trusted client-IP headers, and cache behavior with the infra owner.
- Publish and monitor /.well-known/security.txt with valid Contact and Expires.
- Run a tabletop covering account takeover, record exposure, vendor ransomware, and Akamai-origin anomaly inside the six-hour window.

## FLAGS
- MUJ stack remains brief-supplied; MVC-family signals are passive observations, not vulnerability findings.
- Realm probe uses a constructed probe@muj.manipal.edu address; result supports a managed-tenant claim only.
- Kashmir figures (1M+ records, $250) come from one news report; the university never confirmed legitimacy.
- Surya Shakti facts partly rest on "reportedly" and "believed" wording.
- LPU plaintext claim is uncorroborated; keep as a claim, not a finding.
- IIT Roorkee denied mass extraction on the record; report preserves the denial.
- The stated confidence "Moderate-high, 0.78" is a presented number with no derivation shown; treat as presentation.

## COVERAGE
- Chars read: 42,854
- EOF confirmed: yes (truncated: false on final page, 238 of 238 lines)

---

## w2e-12-certin-bugbounty.digest

## REPORT
Source file: w2e-12-certin-bugbounty.md (Reporting MUJ SLCM Vulnerabilities Through CERT-In)

## ANSWER SUMMARY
- Use two parallel tracks: a confidential notice to MUJ IT and Registrar, plus a direct RVDCP report to vdisclose@cert-in.org.in. Do not wait for a publicly listed nodal officer; none was found.
- Three clocks differ: 72 working hours for acknowledgement, 120 days from initial vendor contact as a resolution target, and six hours for covered entities to report Annexure I incidents. Do not conflate them.
- The researcher route is email-based; the linked certinvulnform.pdf returned "requested URL is not found", so submit the RVDCP field list by email, PGP-encrypted when sensitive.
- RVDCP offers no safe harbor; it requires lawful conduct and leaves the finder responsible. Stop at minimum lawful evidence; no scanning or exploitation without written authorization.
- MUJ public channels: it.support@jaipur.manipal.edu, registrar@jaipur.manipal.edu (Dr Amit Soni, +91 141-3999100, extension 102), registrar.office@jaipur.manipal.edu, admin.office@jaipur.manipal.edu. No public security mailbox or CERT-In PoC found.
- Route by ownership: MUJ for application and configuration defects, MSRC only for demonstrable Microsoft product flaws, security@akamai.com only for Akamai platform defects.
- NCRP and helpline 1930 are cybercrime lanes, Chakshu handles fraudulent communications, TRAI handles spam; none is a vulnerability lane.
- The MAHE information-security policy must not be presented as MUJ's disclosure policy without MUJ confirmation.

## KEY FACTS
1. https://cert-in.org.in/RVDCP.jsp - RVDCP policy page; fields, 72-hour acknowledgement, 120-day target.
2. https://www.cert-in.org.in/PDF/RFC2350.pdf - CERT-In RFC 2350 contact lanes: vdisclose@, incident@, info@.
3. https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf - 2022 Directions; six-hour reporting, PoC duty, 180-day logs.
4. https://www.cert-in.org.in/PDF/certinvulnform.pdf - linked vulnerability form PDF, observed not found at research time.
5. http://jaipur.manipal.edu/contact-university.php - MUJ contact page with IT Infrastructure and Registrar Office channels.
6. https://www.jaipur.manipal.edu/administration-registrar.php - Registrar page; Dr Amit Soni, registrar@, phone extension 102.
7. https://msrc.microsoft.com/report/vulnerability - MSRC Researcher Portal for Microsoft product defects.
8. https://www.microsoft.com/en-us/msrc/faqs-report-an-issue - MSRC guidance; one-business-day receipt, configuration findings often excluded.
9. https://www.akamai.com/global-services/support/vulnerability-reporting - Akamai reporting channel, security@akamai.com.
10. http://jaipur.manipal.edu/about-muj.php - MUJ self-description as a self-financed State Private University.
11. https://www.manipal.edu/mu/policies/it-policy/information-security-policy.html - MAHE information security policy; separate from MUJ unless confirmed.
12. http://i4c.mha.gov.in/ncrp.aspx - NCRP cybercrime complaint lane.
13. http://sancharsaathi.gov.in/ - Chakshu lane for fraudulent calls, SMS, WhatsApp; not for cybercrime.
14. http://trai.gov.in/complain-or-report-against-ucc - TRAI unsolicited communication complaint lane.
15. https://www.jaipur.manipal.edu/mandatory-disclosure.php - mandatory disclosures page, context for MUJ statutory claims.

## ACTIONABLE LEADS
- Send the sanitized report to it.support@ and registrar@ with registrar.office@ as fallback; ask for forwarding to security, legal/privacy, and the CERT-In PoC.
- Submit the same report to vdisclose@cert-in.org.in following RVDCP fields; ask for acknowledgement and a case reference.
- For suspected Annexure I events, alert MUJ by phone and use the incident@ lane; do not impersonate MUJ's authorized officer.
- Preserve only redacted evidence: no cookies, tokens, credentials, grades, or student identifiers.
- Use the provided report envelope template (subject, classification, timing, prior disclosure, researcher preference).
- Ask MUJ to name an authorized security owner and a secure follow-up channel; treat IT/Registrar as forwarding points only.
- Do not retest, publish, or expand scope without written agreement and coordinated approval.

## FLAGS
- Whether the 2022 Directions apply to MUJ is not legally resolved in the report; MUJ counsel should confirm applicability.
- certinvulnform.pdf failure is a transient availability observation; email remains the reliable mechanism.
- Registrar and IT Infrastructure are documented escalation points, not confirmed members of MUJ's security team.
- The MAHE information security policy applies to MAHE assets; presenting it as MUJ policy would create false assurance.
- No safe harbor exists; all steps assume lawful minimal observation already performed.
- High confidence applies to CERT-In primary-source facts; moderate confidence applies to internal MUJ routing.

## COVERAGE
- Chars read: 45,129
- EOF confirmed: yes (truncated: false on final page, 336 of 336 lines)

---

## w2f-01-iis10-cve-sweep.digest

## REPORT
Source file: w2f-01-iis10-cve-sweep.md (IIS 10 Risk Boundaries Behind Akamai)

## ANSWER SUMMARY
- Verdict: UNVERIFIED / CONFIGURATION-DEPENDENT. No public evidence reviewed proves MUJ SLCM vulnerable or safe to any listed IIS, HTTP/2, smuggling, short-name, WebDAV, or TLS issue.
- An IIS 10 banner is not a patch inventory. CVE-2021-31166 and CVE-2022-21907 have exact Windows build cutoffs; OS release, build, and cumulative-update status are unknown without owner evidence.
- Akamai creates two hops (client to edge, edge to origin). Edge mitigations count only if all public traffic is forced through Akamai and the origin is ACL'd to Akamai prefixes.
- HTTP/2 exposure depends on where HTTP/2 terminates. IIS protocol-version logging can answer this without hostile traffic, but the field is disabled by default.
- Request smuggling is parser disagreement (CL.TE, TE.CL, TE.TE, duplicate headers, HTTP/2 downgrade), per RFC 9112 where Transfer-Encoding overrides Content-Length. Review the whole Akamai to HTTP.sys to IIS chain, not a single CVE.
- IIS short names root in NTFS 8.3 aliases. Disabling future creation (NtfsDisable8dot3NameCreation) and removing existing aliases are separate actions; edge filtering is defense in depth only.
- WebDAV is a state, not a banner fact: module install, enablement, authoring rules, and SSL are independent switches. Defaults are enabled=false and requireSsl=false.
- TLS has two independent configurations: Schannel on the origin, Akamai policy on the edge. A strong public TLS grade does not prove origin TLS.

## KEY FACTS
- https://nvd.nist.gov/vuln/detail/CVE-2021-31166 - HTTP.sys RCE, CVSS 9.8, CISA KEV; fixed-build thresholds (19041.982 / 19042.982) show why a banner is not a patch verdict.
- https://nvd.nist.gov/vuln/detail/CVE-2022-21907 - HTTP.sys RCE with separate build cutoffs (17763.2452, 20348.469, 19042.1466 family).
- https://learn.microsoft.com/en-us/iis/get-started/whats-new-in-iis-10/http2-on-iis - IIS 10 HTTP/2 support and the disabled-by-default protocol logging field.
- https://www.cisa.gov/news-events/alerts/2023/10/10/http2-rapid-reset-vulnerability-cve-2023-44487 - Rapid Reset exploited Aug-Oct 2023; forces the termination-point question.
- https://www.rfc-editor.org/info/rfc9112 - Transfer-Encoding overrides Content-Length when both appear; the parsing basis for smuggling review.
- https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/16-Testing_for_HTTP_Request_Smuggling - OWASP parser-disagreement model of smuggling.
- https://vulners.com/mscve/MS:ADV200008 - Microsoft ADV200008 request-smuggling filter guidance; MUJ filter state unknown.
- https://techcommunity.microsoft.com/blog/iis-support-blog/iis-short-name-enumeration/3951320 - 8.3 short-name disclosure and NtfsDisable8dot3NameCreation as root control.
- https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/fsutil-8dot3name - fsutil 8dot3name policy values 0-3; per-volume behavior.
- https://learn.microsoft.com/en-us/iis/configuration/system.webserver/webdav - WebDAV authoring defaults (enabled=false, requireSsl=false); site-level config only, web.config attempts ignored.
- https://techdocs.akamai.com/origin-ip-acl/docs/welcome - Origin IP ACL restricts origin to Akamai prefixes; operator must install addresses in origin-side controls.
- https://techdocs.akamai.com/property-mgr/docs/origin-server - Origin Server config: port, host header, SNI, TLS verification; the edge-origin hop is a separate assessment.
- https://learn.microsoft.com/en-us/windows/win32/secauthn/tls-cipher-suites-in-windows-server-2022 - Server 2022 TLS 1.3 suites; 3DES/DHE removed from defaults; cipher changes can need reboot.
- https://learn.microsoft.com/en-us/windows-server/security/tls/tls-registry-settings - Schannel client/server protocol subkeys; protocol support varies by Windows release.
- http://sei.cmu.edu/documents/1945/2017_003_001_503340.pdf - CERT/CC coordinated disclosure: research only on authorized equipment, disclosure with mitigations.

## ACTIONABLE LEADS
- Request the 10-item owner evidence package: Windows build + cumulative updates, Akamai origin behavior export, firewall/Site Shield/Origin IP ACL policy, IIS protocol logging, HTTP.sys and request-filter state, NTFS 8.3 policy and alias inventory, WebDAV feature + ApplicationHost.config export, Schannel protocol/cipher inventory, Entra app review, isolated clone for parser conformance.
- Enable IIS protocol-version logging through change control to learn whether HTTP/2 reaches the origin.
- Verify Windows servicing and ADV200008-related filtering state before any smuggling claim; reproduce parser conformance only in an isolated clone.
- Passive evidence only on production: response headers, Akamai headers, protocol telemetry. No hostile traffic.
- Use denyUrlSequences rules at the edge as defense in depth for short-name probes; root fix is NTFS alias cleanup.
- Disclosure: privately coordinate any confirmed weakness with Manipal University Jaipur and providers; no public experimentation.

## FLAGS
- "Behind Akamai" is a externally supplied assumption here; cross-report conflict: w2x-00-tech-stack-redo later disputes Akamai attribution using AS8075 evidence.
- References 19, 20, 21 in the source are titled "404 - Content not found" (dead Microsoft Learn URLs) yet are cited in text; treat those claims as weakened.
- Reference 3 is a "How to Bypass Akamai Bot Detection 2026" blog (voidmob.com), low quality and unused in conclusions; odd inclusion.
- Several NVD references are raw services.nvd.nist.gov JSON endpoints, valid but not human pages.
- Report itself declares low confidence for every target-specific conclusion; do not cite as proof of exposure.

## COVERAGE
Chars read: 39,999 (file size), 277 lines. EOF confirmed: true (truncated false).

DONE w2f-01-iis10-cve-sweep.digest.md

---

## w2f-02-dotnet-patch-level.digest

## REPORT
Source file: w2f-02-dotnet-patch-level.md (MUJ SLCM .NET 4.7.4136.0 Security Assessment)

## ANSWER SUMMARY
- 4.7.4136.0 maps with high confidence to the System.Web.dll file version from branch NET472REL1LAST_B, a .NET Framework 4.7.2 servicing lineage. It is not a unique KB, patch date, or install date.
- The same file version and hashes appear in Windows Server 2016 build 14393 packages from October 2025 through July 2026. A serviced host can still expose this value, so "eight years unpatched" claims are false positives.
- Authoritative installed-version check is local: HKLM\SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full Release DWORD. Minimums: 461808 (4.7.2), 528040 (4.8), 533320 (4.8.1).
- Framework 4.5.2+ is a Windows component that follows the parent OS lifecycle; 4.8.1 is the latest release. An active-support label does not prove updates were deployed.
- Serious history includes CVE-2018-8421 (CVSS 9.8 RCE, NVD names 4.7.2) and CVE-2021-24111 (network DoS, 4.7.2 in NVD config). 2026 NVD records add local code execution, code injection, relative path traversal, and network-based privilege elevation.
- Verdict: patch state indeterminate from public evidence. Conditional high remediation priority only if the owner confirms missing applicable cumulative updates.
- CVE-2024-29187 was excluded because it concerns the WiX installer toolset, not the Framework; keyword-only CVE aggregation overstates exposure.
- ASP.NET ships external components separately from the Framework; MVC, OWIN/Katana, JSON, and identity packages need a separate composition inventory.

## KEY FACTS
- https://winbindex.m417z.com/ - third-party binary index mapping 4.7.4136.0 to NET472REL1LAST_B and to build 14393 packages through July 2026.
- https://learn.microsoft.com/en-us/dotnet/framework/install/how-to-determine-which-versions-are-installed - Release DWORD method and documented minimum values.
- https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-framework - 4.5.2+ follows parent Windows lifecycle; 4.8.1 latest; ASP.NET external components note.
- https://learn.microsoft.com/en-us/dotnet/framework/release-notes/release-notes - Framework updates are cumulative security and reliability improvements.
- https://nvd.nist.gov/vuln/detail/CVE-2018-8421 - CVSS 9.8 RCE; NVD explicitly names Framework 4.7.2.
- https://nvd.nist.gov/vuln/detail/CVE-2021-24111 - network-reachable DoS CVSS 7.5; NVD configuration explicitly includes 4.7.2.
- https://nvd.nist.gov/vuln/detail/CVE-2026-62872 - incorrect authorization lets an authorized attacker elevate privileges over a network.
- https://nvd.nist.gov/vuln/detail/CVE-2026-50646 - protection-mechanism failure permits unauthorized local code execution.
- https://nvd.nist.gov/vuln/detail/CVE-2026-65810 - relative path traversal permits local privilege elevation.
- https://nvd.nist.gov/vuln/detail/CVE-2024-21409 - RCE family advisory with CWE-416 use-after-free; exact version not shown in captured text.
- https://nvd.nist.gov/vuln/detail/CVE-2024-29187 - WiX toolset CVE, excluded; example of keyword-only aggregation error.
- https://nvd.nist.gov/vuln/detail/CVE-2025-21176 - January 2025 RCE in .NET, .NET Framework, and Visual Studio family.
- https://mujslcm.jaipur.manipal.edu/ - the only independently verified host fact: public portal with sign-in and parent-login choices.
- https://learn.microsoft.com/en-us/troubleshoot/developer/dotnet/framework/general/assembly-version-assembly-file-version - AssemblyVersion versus AssemblyFileVersion distinction; file metadata is not used for referencing.
- https://nvd.nist.gov/vuln/detail/CVE-2020-1147 - XML source markup RCE across .NET Framework, SharePoint, and Visual Studio.

## ACTIONABLE LEADS
- Owner-side evidence: Release DWORD, Windows edition/build/support state, installed KB list with pending reboot, signed binary metadata as corroboration only, and an application-local assembly inventory.
- Map every candidate CVE through the MSRC applicability matrix (exact OS, Framework release, KB supersedence, architecture, enabled feature) into a dated worksheet.
- Patch in staging first: sign-in, parent access, sessions, uploads, reports, integrations. Upgrade to 4.8 or 4.8.1 only where the parent OS supports it.
- Review version disclosure (headers, error pages) only after servicing; hiding a banner is not patching.
- The team-safe work: public source map, CVE applicability worksheet, owner checklist. No error induction, origin hunting, header manipulation, account enumeration, or role-boundary tests.

## FLAGS
- The repeated-file result contradicts any unique-KB inference; the report explicitly warns against calling all 4.7-era hosts unpatched.
- Most 2021-2026 CVE rows lack exact affected Framework releases in captured NVD text; they are family-level records, applicability unresolved.
- 2026-dated NVD CVEs (CVE-2026-50646, CVE-2026-62872, CVE-2026-65810) are future-dated claims from the source; unverified, treat as record citations only.
- winbindex is third-party; Microsoft publishes no such mapping. Confirm against owner inventory before any claim.
- Verdict split: high confidence on branch mapping, low/unsupported on MUJ being unpatched or affected; do not cite as exposure proof.

## COVERAGE
Chars read: 35,282 (file size), 271 lines. EOF confirmed: true (truncated false).

DONE w2f-02-dotnet-patch-level.digest.md

---

## w2f-03-jquery-cve-sweep.digest

## REPORT
Source file: w2f-03-jquery-cve-sweep.md (jQuery 1.10.2 Risk Across MUJ SLCM Trust Boundaries)

## ANSWER SUMMARY
- jQuery 1.10.2 is an unsupported 1.x branch. Only the latest jQuery is supported; 1.x and 2.x are unsupported, 3.x gets critical fixes only, 4.0.0 is current.
- Three confirmed range matches: CVE-2015-9251 (before 3.0.0), CVE-2019-11358 (1.1.4 to before 3.4.0), CVE-2020-11023 (1.0.3 to before 3.5.0).
- CVE-2020-11022 is NOT in the current formal range for 1.10.2. Current CVE.org record says >=1.12.0, <3.5.0. A 2025 NASA VDP disclosure listed it against jQuery 1.8.2, showing scanner drift; the canonical record controls the formal count.
- CVE-2020-23064 is a rejected duplicate of CVE-2020-11023 and must not be double counted. CVE-2020-7656 affects only versions before 1.9.0, so 1.10.2 is excluded.
- Presence is not exploitability. Each CVE needs a reachable sink: implicit-type cross-origin Ajax, deep merge of attacker-influenced objects, or option-bearing HTML into DOM manipulation methods.
- Login page rating: Medium risk pending reachability review. Post-auth rating: Medium-High potential impact, unknown likelihood (attendance, marks, results, circulars per official SLCM documentation).
- None of the four CVEs appears in the CISA KEV catalog; the report does not claim in-the-wild exploitation.
- Upgrade path: staged move to a current 3.x build with jQuery Migrate 3.x, then decide on 4.x (released 2026-01-17, breaking changes, drops older browsers).

## KEY FACTS
- https://nvd.nist.gov/vuln/detail/CVE-2015-9251 - affected before 3.0.0; cross-origin text/javascript execution when dataType is omitted.
- https://github.com/advisories/GHSA-rmxg-73gg-4p98 - GitHub advisory for CVE-2015-9251, CVSS 6.1.
- https://nvd.nist.gov/vuln/detail/CVE-2019-11358 - prototype pollution via jQuery.extend(true,...); 1.1.4 to before 3.4.0.
- https://github.com/advisories/GHSA-6c3j-c64m-qhgq - XSS/prototype pollution advisory for CVE-2019-11358, CVSS 6.1.
- https://www.cve.org/CVERecord?id=CVE-2020-11022 - canonical current range >=1.12.0, <3.5.0; excludes 1.10.2.
- https://nvd.nist.gov/vuln/detail/CVE-2020-11023 - 1.0.3 to before 3.5.0; option-element HTML passed to manipulation methods.
- https://github.com/advisories/GHSA-jpcq-cgw6-v4j6 - CVSS 6.9 advisory for CVE-2020-11023; DOMPurify jQuery-safe mode as workaround.
- https://github.com/jquery/jquery/issues/2432 - original cross-origin Ajax proof of concept for CVE-2015-9251; not an incident report.
- https://www.drupal.org/sa-core-2019-006 - Drupal backport of the fix; mechanism-versus-gadget lesson.
- https://bugcrowd.com/disclosures/c6f29ef2-5930-4100-83f4-ea5f66546169/vulnerable-jquery-library-v1-8-2-outdated-components-leading-to-multiple-vulnerabilities - NASA VDP disclosure, closed P5 informational with accepted risk; listed 2020-11022 against 1.8.2.
- https://jquery.com/support/ - lifecycle truth: only latest supported, 1.x/2.x unsupported, 3.x critical fixes only.
- https://blog.jquery.com/2026/01/17/jquery-4-0-0/ - jQuery 4.0.0 release date and breaking changes (Trusted Types, older browser drops).
- https://www.cisa.gov/known-exploited-vulnerabilities-catalog - none of the four CVEs listed; no KEV-backed exploitation claim.
- https://blog.jquery.com/2020/04/10/jquery-3-5-0-released/ - 3.5.0 htmlPrefilter security fix; warns the fix can break legacy parsing behavior.
- https://www.cert-in.org.in/RVDCP.jsp - CERT-In coordinated reporting route for any confirmed flaw.

## ACTIONABLE LEADS
- Inventory every jQuery core copy, bundle, plugin, and template; produce a hash-based SBOM across login and post-auth builds.
- Authorized static source-to-sink search: cross-origin $.ajax/$.get/$.post/$.load without explicit dataType; jQuery.extend(true,...) fed untrusted objects; .html()/.append()/innerHTML with attacker-controlled strings.
- Use inert fixtures and non-executing marker strings in local or staging DOM tests; never send executable payloads to production.
- Upgrade staged: 3.x with Migrate 3.x, resolve compatibility warnings, then evaluate 4.x; keep a rollback plan.
- Layer controls: strict nonce/hash CSP in report-only first, DOMPurify for required HTML, textContent over HTML sinks.
- Validate identity flow and post-auth roles with synthetic test accounts; preserve minimum evidence and report privately to the university owner, with CERT-In RVDCP as the coordination route.

## FLAGS
- Contradiction: NASA VDP listed CVE-2020-11022 for jQuery 1.8.2 while the current CVE.org range starts at 1.12.0; the report uses the canonical record for the formal count. Cross-report conflict: w2x-00-tech-stack-redo counts 2020-11022 as in range for 1.10.2 using the NVD range.
- Rejected duplicate CVE-2020-23064 risks double counting in scanner output.
- KEV absence is not proof exploitation never occurred; the report says so explicitly.
- jQuery 1.10.2 label is scope-supplied and passively consistent, not an owner-verified inventory.
- All reachability ratings are explicit analyst inferences, not test results.

## COVERAGE
Chars read: 37,536 (file size), 250 lines. EOF confirmed: true (truncated false).

DONE w2f-03-jquery-cve-sweep.digest.md

---

## w2f-04-mvc53-known-issues.digest

## REPORT
Source file: w2f-04-mvc53-known-issues.md (MVC 5.3 Risk Map for MUJ SLCM)

## ANSWER SUMMARY
- MVC 5.3.0 is a real release: NuGet published on 2023-10-23, Web Stack v3.3.0 on 2023-10-24. Microsoft lists MVC 5.x as supported under its external ASP.NET tool policy with no end date. Not EOL, but legacy System.Web.
- WebGrease is NOT a direct MVC 5.3 dependency. It enters through the separate Microsoft.AspNet.Web.Optimization 1.1.3 package (deprecated, no longer maintained), which requires WebGrease >=1.5.2.
- The only confirmed historical MVC advisory, MS14-059 / CVE-2014-4075 (input-encoding XSS), enumerates affected releases through MVC 5.1. MVC 5.3 is not in the bulletin.
- CVE-2018-8171 is a package-level advisory (CVSS 7.5, login-attempt validation) whose consulted record gives no affected range or fixed version. Applicability to 5.3 is unresolved, not assumed.
- The "unsafe reflection" issue #428 is an open, version-unspecified Veracode CWE-470 report on System.Net.Http.Formatting.dll, unconfirmed by maintainers. It is not a UrlHelper advisory.
- Core JsonResult defaults to DenyGet; no core JsonpResult was found. Any JSONP behavior on MUJ is custom or third-party until its assembly is identified.
- Antiforgery community issues (#48, #157, #162, #328) are closed operational failures (IIS classic pipeline, load-balanced token decryption, MachineKey coupling, Google Web Light), not CVEs.
- Verdict: no public evidence proves an MVC 5.3 flaw on MUJ. Evidence justifies an owner-authorized review of deployment inventory, legacy optimization chain, build imports, redirects, JSON behavior, antiforgery topology, sessions, and controller authorization.

## KEY FACTS
- https://www.nuget.org/packages/Microsoft.AspNet.Mvc/5.3.0 - package record; direct deps Razor >=3.3.0 and WebPages >=3.3.0; no WebGrease in the direct list.
- https://dotnet.microsoft.com/en-us/platform/support/policy/aspnet - MVC 5.x supported, classified as a Tool, no end date.
- https://learn.microsoft.com/en-us/security-updates/SecurityBulletins/2014/ms14-059 - MS14-059; affected MVC 2.0 through 5.1, so 5.3 is not enumerated.
- https://www.nuget.org/packages/Microsoft.AspNet.Web.Optimization/1.1.3 - legacy, no longer maintained; requires WebGrease >=1.5.2.
- https://www.nuget.org/packages/WebGrease/1.6.0 - last updated 2014-01-23; floors on Antlr 3.4.1.9004 and Newtonsoft.Json 5.0.4 (declared minimums, not deployed versions).
- https://advisories.gitlab.com/pkg/nuget/microsoft.aspnet.mvc/ - CVE-2018-8171 CVSS 7.5 advisory; no version range in the consulted record.
- https://api.github.com/repos/aspnet/AspNetWebStack/issues/428 - open Veracode reflection finding on System.Net.Http.Formatting.dll; label Needs: Author Feedback; no maintainer confirmation.
- https://github.com/aspnet/AspNetWebStack/blob/main/src/System.Web.Mvc/UrlHelper.cs - ObjectToDictionary route-value conversion; no request-controlled class instantiation shown.
- https://github.com/aspnet/AspNetWebStack/blob/main/src/System.Web.Mvc/JsonResult.cs - DenyGet default; JavaScriptSerializer for non-null data.
- https://learn.microsoft.com/en-us/aspnet/mvc/overview/security/preventing-open-redirection-attacks - open-redirect pattern and IsLocalUrl mitigation.
- https://api.github.com/repos/aspnet/AspNetWebStack/issues/162 - classic pipeline PlatformNotSupportedException after 5.2.3 to 5.2.6 upgrade.
- https://api.github.com/repos/aspnet/AspNetWebStack/issues/328 - token decryption failure across two Windows Server 2019 IIS nodes behind a load balancer; root cause unresolved.
- https://api.github.com/repos/aspnet/AspNetWebStack/issues/157 - antiforgery serializer used MachineKey only; no OWIN data-protector integration point.
- https://api.github.com/repos/aspnet/AspNetWebStack/issues/48 - Google Web Light removed the token field; intermediary transformation failure case.
- https://learn.microsoft.com/en-us/nuget/consume-packages/package-references-in-project-files - PackageReference asset controls (IncludeAssets, ExcludeAssets, PrivateAssets) and packages.lock.json locked restore.

## ACTIONABLE LEADS
- Export the resolved package graph (project files, packages.config, project.assets.json, lock files, DLL hashes); confirm whether Web Optimization is installed and used; plan retirement of the legacy optimization branch.
- Review imported .props and .targets, constrain NuGet sources, lock restores in CI, and generate an SBOM.
- Static review targets: returnUrl handling with IsLocalUrl, JsonResult AllowGet opt-ins, JSONP callbacks, antiforgery coverage on every state-changing route, object-level authorization on student and parent records.
- Test CSRF across the real topology: multi-node farm consistency, proxy/CDN behavior, cookie flags, identity transitions. A 500 on token omission means enforcement, not bypass.
- Track issue #428 and reproduce only in an isolated test project using the exact deployed binary.
- Release gates: version provenance, build provenance, redirects, JSON exposure, CSRF, authorization, session policy, authentication errors, monitoring.

## FLAGS
- CVE-2018-8171 has no affected range in the consulted advisory; a package-name match alone must not be called a 5.3 vulnerability.
- Issue #428 is a reporter-submitted scanner finding without maintainer confirmation; high hallucination risk if cited as a confirmed flaw.
- Many references are raw API endpoints (api.github.com, api.nuget.org); valid evidence but not human-readable pages.
- MVC 5.3, .NET 4.x, IIS 10, Akamai, and Microsoft 365 are externally supplied premises; host-specific conclusions are conditional.
- Open-issue searches returned zero results; bounded negative results, not proof of no defects.
- MS14-059 is historical provenance only; citing it as current MUJ exposure would be an error the report explicitly warns against.

## COVERAGE
Chars read: 50,421 (report text extracted from JSON-persisted tool output), 388 lines. EOF confirmed: true (truncated false).

DONE w2f-04-mvc53-known-issues.digest.md

---

## w2f-05-keen-theme-cve.digest

## REPORT
Source file: w2f-05-keen-theme-cve.md (35,154 bytes, 248 lines, read to EOF)

## ANSWER SUMMARY
- MUJ login page and Internet Archive records show the Keen demo1 asset family under `/keen/themes/keen/theme/demo1/dist/`. Exact Keen release is unknown.
- Archived bundles identify Bootstrap 4.4.1 and jQuery 3.4.1. jQuery 3.4.1 sits in the affected ranges of CVE-2020-11022 and CVE-2020-11023. Dependency exposure is verified; MUJ exploitability is unproved.
- `scripts.bundle.js` holds `innerHTML` and `.html()` sinks in datatable, error, filename, message, and quick-search paths, with conditional DOMPurify use. `login.js` shows no demonstrated attacker-controlled flow.
- IIS 10 is corroborated by two 2026 urlscan observations (98.70.14.50, Microsoft AS8075). ASP.NET MVC 5.3, .NET Framework 4.x, Akamai, and Microsoft 365 federation remain unverified supplied labels.
- A urlscan four-filename query returns 2,684 candidate scan results, not 2,684 sites. A Common Crawl August 2026 exact-path query returned no capture. Exact global reuse count is unknown.
- Commercial license status is indeterminate from public artifacts. The MIT banner in `style.bundle.css` covers the Bootstrap dependency, not a Keen purchase.
- Recommended response is defensive modernization: SBOM, jQuery replacement, source-to-sink review of KTDatatable and KTQuickSearch, report-only CSP, retained license evidence, CERT-In disclosure route.

## KEY FACTS
1. http://web.archive.org/cdx/search/cdx?collapse=urlkey&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&output=json&url=mujslcm.jaipur.manipal.edu/* - CDX provenance proving the Keen demo1 assets were archived with HTTP 200.
2. https://web.archive.org/web/20250110135955id_/https://mujslcm.jaipur.manipal.edu/keen/themes/keen/theme/demo1/dist/assets/css/style.bundle.css - archived stylesheet carries the Bootstrap 4.4.1 MIT banner.
3. https://web.archive.org/web/20250110135958id_/https://mujslcm.jaipur.manipal.edu/keen/themes/keen/theme/demo1/dist/assets/plugins/global/plugins.bundle.js - archived plugin bundle identifies jQuery 3.4.1, dated May 1 2019.
4. https://web.archive.org/web/20250110135958id_/https://mujslcm.jaipur.manipal.edu/keen/themes/keen/theme/demo1/dist/assets/js/scripts.bundle.js - archived general bundle with HTML insertion sinks and conditional DOMPurify.
5. https://web.archive.org/web/20250110135959id_/https://mujslcm.jaipur.manipal.edu/keen/themes/keen/theme/demo1/dist/assets/js/pages/custom/user/login.js - archived login script uses validation, ajaxSubmit, and a fixed error message with no untrusted flow shown.
6. https://web.archive.org/web/20250110135958id_/https://mujslcm.jaipur.manipal.edu/Scripts/jquery-1.10.2.min.js - second version-named jQuery asset; raises a duplicate-load and execution-order question.
7. https://nvd.nist.gov/vuln/detail/CVE-2020-11022 - jQuery 1.12.0 to before 3.5.0 XSS range that covers the bundled 3.4.1.
8. https://nvd.nist.gov/vuln/detail/CVE-2020-11023 - jQuery 1.0.3 to before 3.5.0 option-element range that also covers the 1.10.2 asset.
9. https://urlscan.io/api/v1/search/?q=domain%3Amujslcm.jaipur.manipal.edu&size=100 - three scans; the 2026 pair reports Microsoft-IIS/10.0 on AS8075 at 98.70.14.50, the 2024 scan reports IIS 8.5 on AS45769.
10. https://urlscan.io/api/v1/search/?q=filename%3Alogin-v1.css%20AND%20filename%3Astyle.bundle.css%20AND%20filename%3Ascripts.bundle.js%20AND%20filename%3Aplugins.bundle.js&size=10000 - 2,684 candidate scan results with no more indicated; scan documents, not unique sites.
11. https://urlscan.io/api/v1/search/?q=filename%3Alogin-v1.css&size=10000 - 10,000 hits with more available; shows a single basename is severely overbroad.
12. https://index.commoncrawl.org/CC-MAIN-2026-34-index?url=%2A%2Fkeen%2Fthemes%2Fkeen%2Ftheme%2Fdemo1%2Fdist%2Fassets%2Fcss%2Fpages%2Flogin%2Flogin-v1.css&output=json&filter=status%3A200&collapse=urlkey - no capture in the August 2026 crawl; a bounded zero for that index only.
13. https://preview.keenthemes.com/keen/demo1 - current vendor demo1 is a Bootstrap 5 dashboard, distinct from MUJ's archived Bootstrap 4 era assets.
14. https://mujslcm.jaipur.manipal.edu/Home/Index - public welcome page with sign-in and parent-login choices.
15. http://cert-in.org.in/RVDCP.jsp - CERT-In vulnerability-reporting channel for routing any confirmed finding.

## ACTIONABLE LEADS
- Review the archived URLs above for exact byte evidence; compare SHA-256 hashes against retained Keen installation media in the university repo.
- Owner-side review targets: KTDatatable and KTQuickSearch source-to-sink flows in `scripts.bundle.js`.
- Verify current live asset paths and headers before treating the January 2025 archive as current state.
- Request an SBOM, single jQuery load, and report-only CSP rollout.
- License step: retain invoice, account statement, download archive, version-specific license text, and transfer records.
- Disclosure step: route any confirmed finding via CERT-In RVDCP; nothing confirmed to report yet.

## FLAGS
- No contradiction between 0 Common Crawl captures and 2,684 urlscan results; the datasets, predicates, and time windows differ.
- Supplied labels MVC 5.3, .NET 4.x, Akamai, M365 federation are not verified by this report; do not publish as fact.
- 2,684 is a bounded candidate-scan count; repeated domains and subdomains are present in the result set.
- CVE-2024-6485 has no affected version range; CVE-2024-6531 and CVE-2024-6484 were marked not Bootstrap security issues; do not use as evidence.
- CVE-2019-8331 does not cover Bootstrap 4.4.1.
- No public purchase record exists; absence of a license file is not proof of infringement.
- All archive, scan, and vendor URLs are point-in-time and unverified by this digest.

## COVERAGE
Chars read: 35,154 (full file, 248 lines). EOF confirmed: truncated false on the complete read.

DONE w2f-05-keen-theme-cve.md.digest.md

---

## w2f-06-akamai-edge.digest

## REPORT
Source file: w2f-06-akamai-edge.md (41,547 bytes, 315 lines, read to EOF)

## ANSWER SUMMARY
- `mujslcm.jaipur.manipal.edu` resolves directly to 98.70.14.50; RIPE maps covering prefix 98.70.0.0/15 to Microsoft AS8075. No CNAME to an Akamai edge hostname is returned.
- The supplied "IIS 10 behind Akamai" premise is unsupported: Akamai onboarding docs describe CNAME mapping to edgesuite.net, edgekey.net, or akamaized.net; none observed.
- Headers expose Server Microsoft-IIS/10.0, X-AspNetMvc-Version 5.3, X-AspNet-Version 4.0.30319, and X-Powered-By ASP.NET. These favor a Microsoft stack, not an Akamai edge.
- WAF status is not publicly verifiable. Akamai attack groups are collections of Kona Rule Set rules with configurable actions: alert, deny, custom deny, or none.
- If 98.70.14.50 is the backend, the origin is plainly disclosed; if it is an Azure front end, the backend is unknown. No separate hidden origin was verified.
- Sibling addresses are leads, not origins: muj.slcm.jaipur.manipal.edu at 20.244.94.89, dms.jaipur.manipal.edu at 1.186.160.28, slcm.manipal.edu at 104.211.226.160.
- Browser hardening is incomplete: SecurityHeaders grade D; HSTS, CSP, X-Content-Type-Options, Referrer-Policy, and Permissions-Policy missing; X-Frame-Options SAMEORIGIN present; request-verification cookie HttpOnly without Secure or SameSite.
- Portal links to Microsoft password reset; full Microsoft 365 federation is not proven.

## KEY FACTS
1. https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=A - A record 98.70.14.50 with TTL 3600; the current public service endpoint.
2. http://stat.ripe.net/data/prefix-overview/data.json?resource=98.70.14.50 - 98.70.0.0/15 aligns to AS8075 Microsoft Corporation; the address is Microsoft evidence, not Akamai evidence.
3. https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=CNAME - no CNAME answer, only zone authority; no Akamai edge mapping visible.
4. http://api.hackertarget.com/httpheaders?q=https://mujslcm.jaipur.manipal.edu/ - observed IIS 10, ASP.NET MVC and runtime banners, X-Powered-By, XFO SAMEORIGIN, HttpOnly cookie without Secure or SameSite.
5. http://securityheaders.com/?followRedirects=on&q=https://mujslcm.jaipur.manipal.edu/ - grade D; missing HSTS, CSP, nosniff, referrer, and permissions headers.
6. http://crt.sh/?output=json&q=mujslcm.jaipur.manipal.edu - CT shows the MUJ hostname, a www variant, and a historical dms.jaipur.manipal.edu certificate relationship.
7. https://dns.google/resolve?name=muj.slcm.jaipur.manipal.edu&type=A - 20.244.94.89; sibling address with unproven backend linkage.
8. https://dns.google/resolve?name=dms.jaipur.manipal.edu&type=A - 1.186.160.28; sibling address with unproven backend linkage.
9. https://dns.google/resolve?name=slcm.manipal.edu&type=A - 104.211.226.160; central SLCM address that also exposes an IIS/ASP.NET response.
10. https://passwordreset.microsoftonline.com/ - Microsoft recovery touchpoint linked from the portal; not proof of full federation.
11. http://techdocs.akamai.com/ion/docs/define-property-hostnames - documented Akamai onboarding model: customer DNS CNAME to an Akamai edge hostname.
12. http://techdocs.akamai.com/terraform/docs/pm-rc-edge-hostname - edge hostname classes at edgesuite.net, edgekey.net, and akamaized.net; none match the MUJ DNS.
13. https://techdocs.akamai.com/edge-diagnostics/docs/pragma-headers - X-Cache, X-Cache-Remote, and X-Akamai-Request-ID are context-dependent diagnostics absent from the ordinary MUJ response.
14. https://techdocs.akamai.com/terraform/docs/as-ds-attack-groups - KRS attack-group actions are customer-configurable; a policy does not imply blocking.
15. https://techdocs.akamai.com/site-shield/docs/welcome-site-shield - Site Shield CIDR allowlisting is explicitly not a substitute for authentication.

## ACTIONABLE LEADS
- Re-run the DNS A, CNAME, and AAAA queries and the RIPE prefix call to confirm the 2026-08-25 snapshot still holds.
- Fetch crt.sh JSON for the current certificate list and owner names.
- Compare sibling posture: http headers and securityheaders checks for slcm.manipal.edu.
- Owner-side asks: Azure resource mapping for 98.70.14.50, Akamai property and edge hostname if any, Site Shield or Origin IP ACL map, KRS/ASE mode, and attack-group actions.
- Hardening steps: strip version banners, add HSTS, CSP, nosniff, referrer, and permissions headers, and review cookie attributes.
- Do not probe candidate IPs or run Host-header bypass tests without written authorization.

## FLAGS
- The supplied Akamai premise is contradicted by current DNS and BGP evidence; treat it as an unverified design claim.
- The role of 98.70.14.50 is unresolved: origin, Azure load balancer, application gateway, or other service; public data cannot decide.
- Absence of an Akamai CNAME does not rule out an Azure-layer proxy or WAF at the same address.
- Missing Akamai diagnostic headers in an ordinary request prove nothing by themselves.
- CT records reveal names, not backend IPs; sibling addresses are entity-conflation risks.
- All DNS, RIPE, header, and CT observations are time-bound and unverified by this digest.

## COVERAGE
Chars read: 41,547 (full file, 315 lines). EOF confirmed: truncated false on the complete read.

DONE w2f-06-akamai-edge.md.digest.md

---

## w2f-07-entra-tenant-enum.digest

## REPORT
Source file: w2f-07-entra-tenant-enum.md (44,454 bytes, 294 lines, read to EOF)

## ANSWER SUMMARY
- Two Entra tenants are confirmed via public OIDC discovery: jaipur.manipal.edu maps to tenant 7d0726e8-bf4b-4ac1-99f1-010fb11f1d3f and muj.manipal.edu maps to tenant 27282fdd-4c0b-4dfb-ba91-228cd83fdf71. Region scope AS.
- Both realm lookups classify the domains as Managed with organization Manipal University Jaipur. The federationmetadata URLs publish Microsoft STS and WS-Federation endpoints, not a third-party IdP.
- Portal split: mujslcm.jaipur.manipal.edu advertises @muj.manipal.edu while muj.slcm.jaipur.manipal.edu advertises @jaipur.manipal.edu. Migration, segmentation, or legacy overlap are possible; public data cannot decide.
- Tenant enumeration is confirmed as platform behavior. GetCredentialType is described in the literature as an account-enumeration vector; Microsoft calls it an internal endpoint. MUJ per-user behavior is deliberately untested and unknown.
- MUJ's June 2025 Office 365 SOP says MFA is mandatory before Office 365 use and documents Authenticator, SMS phone, and personal-email registration. Enrollment intent is proven; enforcement, coverage, and strength are unknown.
- Mail posture: both domains on Outlook MX and Autodiscover; DKIM selectors alias into mujcampus.onmicrosoft.com and mujmanipal.onmicrosoft.com. DMARC is monitoring-only: child p=none for jaipur, no child record for muj, parent manipal.edu p=none.
- Context not proof: Seqrite reports 4.92M Education and Training detections, 18.45% of India detections, Oct 2024 to Sep 2025; CERT-In 2023 handled 1,592,917 incidents nationally.

## KEY FACTS
1. https://login.microsoftonline.com/jaipur.manipal.edu/v2.0/.well-known/openid-configuration - issuer, token, authorization, and JWKS endpoints embed tenant GUID 7d0726e8-bf4b-4ac1-99f1-010fb11f1d3f.
2. https://login.microsoftonline.com/muj.manipal.edu/v2.0/.well-known/openid-configuration - same metadata class for tenant GUID 27282fdd-4c0b-4dfb-ba91-228cd83fdf71; separate policy boundary.
3. http://login.microsoftonline.com/getuserrealm.srf?login=probe@jaipur.manipal.edu&xml=1 - realm response Managed, organization Manipal University Jaipur.
4. http://login.microsoftonline.com/getuserrealm.srf?login=probe@muj.manipal.edu&xml=1 - realm response Managed for the muj domain.
5. https://login.microsoftonline.com/jaipur.manipal.edu/federationmetadata/2007-06/federationmetadata.xml - Microsoft STS entity ID and passive wsfed endpoint; retrieval is not proof of external federation.
6. http://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf - first-party MUJ SOP; MFA described as mandatory before Office 365 use.
7. http://dns.google/resolve?name=jaipur.manipal.edu&type=MX - MX to jaipur-manipal-edu.mail.protection.outlook.com.
8. http://dns.google/resolve?name=muj.manipal.edu&type=MX - MX to muj-manipal-edu.mail.protection.outlook.com; distinct Exchange Online namespaces.
9. http://dns.google/resolve?name=selector1._domainkey.jaipur.manipal.edu&type=CNAME - DKIM selector aliases into mujcampus.onmicrosoft.com.
10. http://dns.google/resolve?name=selector1._domainkey.muj.manipal.edu&type=CNAME - DKIM selector aliases into mujmanipal.onmicrosoft.com; corroborates the two-namespace split.
11. https://dns.google/resolve?name=_dmarc.jaipur.manipal.edu&type=TXT - v=DMARC1; p=none; rua mailto:dmarc@jaipur.manipal.edu; reporting without enforcement.
12. https://dns.google/resolve?name=_dmarc.manipal.edu&type=TXT - parent manipal.edu also publishes p=none.
13. http://dns.google/resolve?name=jaipur.manipal.edu&type=TXT - SPF includes spf.protection.outlook.com plus Brightspace sender authorization; a link to the LMS research thread.
14. http://muj.slcm.jaipur.manipal.edu/ - sibling SLCM portal advertises the @jaipur.manipal.edu suffix, in contrast to the target portal.
15. https://www.seqrite.com/documents/en/threat-reports/india-cyber-threat-report-2026.pdf - 4.92M education detections or 18.45% share; sector context only.

## ACTIONABLE LEADS
- Passive recheck: both OIDC docs, both realm probes, MX, DKIM selectors, DMARC, and Autodiscover CNAMEs; watch for issuer or realm changes.
- Owner-side: GUID-keyed comparison of Conditional Access, authentication methods, SSPR scope, guest policy, and legacy flows in both tenants; maintain monitored cloud-only emergency accounts.
- Apply phishing-resistant authentication strength to privileged roles; register methods before enforcement.
- If MUJ authorizes tests, use synthetic canary identities for GetCredentialType and SSPR validation with a documented rate limit; never test real identities.
- Stage DMARC: sender inventory, SPF/DKIM alignment review, then quarantine and reject decisions.
- Clarify portal lifecycle: canonical login suffix and retirement criteria for the legacy path.
- Disclosure: escalate policy drift findings through a university-approved channel; no active probing.

## FLAGS
- Two tenants are confirmed; cross-tenant policy drift is an inference, not a demonstrated gap.
- Realm probes used the invented identity probe@; behavior for real identities is untested.
- GetCredentialType output is ambiguous for guests, alternate sign-in identifiers, and consumer accounts; Microsoft warns it is not an onboarding decision API.
- MFA mandatory is documentation of intent; coverage, exclusions, and authentication strength remain unknown.
- p=none does not prove spoofing occurs; an absent child record for muj means parent behavior applies.
- Seqrite and CERT-In figures are vendor and national telemetry, not university-specific measures.
- All OIDC, realm, and DNS observations are point-in-time and unverified by this digest.

## COVERAGE
Chars read: 44,454 (full file, 294 lines). EOF confirmed: truncated false on the complete read.

DONE w2f-07-entra-tenant-enum.md.digest.md

---

## w2f-08-brightspace-security.digest

## REPORT
Source file: w2f-08-brightspace-security.md (43,853 bytes, 315 lines, read to EOF)

## ANSWER SUMMARY
- The public Brightspace CVE record is narrow: one result, CVE-2021-43129, a bypass of the "Disable Right Click" quiz control. NVD has no CVSS score, CPE range, or named patched version. MUJ applicability is unknown.
- The most concrete public incident is identity-led: REN-ISAC reports criminals using compromised institutional accounts and permissive Brightspace email defaults for bulk phishing. Not a D2L code vulnerability.
- SAML is evidenced at the student portal: a passive fetch of student.onlinemanipal.com/s/ produced a tenant-specific login.microsoftonline.com saml2 flow. OIDC is a D2L-supported option that requires Implementation Services; no MUJ evidence of OIDC use.
- Grade sync is the highest-integrity boundary. Brightspace APIs can create, update, replace, recalculate, and set adjusted final grades under scopes. OneRoster 1.2 gradebook uses OAuth 2.0 Client Credentials and TLS 1.2 or 1.3. No public source proves MUJ uses any of these flows with SLCM.
- Identity mapping guidance: use stable sub or oid values, not mutable email, phone, or UPN. A grade-bearing integration needs an immutable institutional person key.
- learning.onlinemanipal.com publicly says powered by D2L Brightspace. www robots.txt is permissive with a sitemap; the security.txt response looked like homepage content with no RFC-style contact shown.
- D2L's disclosure policy covers specified D2L systems; customer-instance testing requires customer authorization and excludes DoS, phishing, exfiltration, persistence, and pivoting.
- Overall verdict: no public evidence reviewed establishes a presently exploitable MUJ Brightspace, SLCM, or Online Manipal vulnerability. Confidence moderate.

## KEY FACTS
1. https://nvd.nist.gov/vuln/detail/CVE-2021-43129 - the only Brightspace CVE found; quiz right-click bypass, no severity or version range on the record.
2. https://app.opencve.io/cve/?product=brightspace&vendor=d2l - catalog query returned one result, Page 1 of 1.
3. https://www.ren-isac.net/services/publications/alerts/Brightspace_Email_Fraud.html - documented abuse pattern: compromised accounts plus permissive email defaults, cloud email bypassing institutional mail controls.
4. https://learning.onlinemanipal.com/d2l/home/14042 - public learning page with username field and "Powered by D2L Brightspace" attribution.
5. https://student.onlinemanipal.com/s/ - passive fetch redirected into a tenant-specific Microsoft SAML flow.
6. https://community.d2l.com/brightspace/kb/articles/4843-saml-administration-overview - SAML self-service with Azure certification; OIDC, LDAP, GUID SSO, and CAS lack self-service and require Implementation Services.
7. https://community.d2l.com/brightspace/kb/articles/23832-getting-ready-for-oneroster-integration - IPSIS scheduled pulls, optional grade passback during daily sync, manual faculty sync, OAuth credentials, and IPSIS Audit Log review.
8. https://docs.valence.desire2learn.com/res/grade.html - grade object and grade value write scopes, recalculation, and adjusted final grade operations.
9. https://www.imsglobal.org/spec/oneroster/v1p2/gradebook/bind/rest - OneRoster 1.2 gradebook REST binding: OAuth 2.0 Client Credentials, scopes, TLS 1.2 or 1.3, read and write operations.
10. https://learn.microsoft.com/en-us/entra/identity-platform/id-token-claims-reference - rejects mutability of email, phone, and UPN; recommends stable sub or oid with tid context.
11. https://community.d2l.com/brightspace/kb/articles/23533-d2l-vulnerability-disclosure-policy - safe harbor scope and the customer-authorization boundary for instance testing.
12. https://status.d2l.com/ - global status page; all services operational when checked, with warnings that it is not a direct uptime monitor.
13. https://www.onlinemanipal.com/robots.txt - permissive crawl directives plus sitemap URL; ordinary public discovery, no access-control value.
14. https://www.onlinemanipal.com/.well-known/security.txt - parsed response resembled homepage material; RFC-style security contact not demonstrated.
15. https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-session-lifetime - sign-in frequency default of a rolling 90 days; local cookies and token caching can outlive intended session behavior.

## ACTIONABLE LEADS
- Passive: re-fetch learning.onlinemanipal.com, both robots files, and www security.txt; monitor D2L status categories Authentication, APIs, Grades Tool, Quizzing, Integrations.
- Owner-side: D2L tenant release history and advisory mapping, redacted SAML claims configuration, SOC report, subprocessor list, session and logout design.
- Grade integrity: data dictionary, directionality matrix, reconciliation runbook, and before/after provenance for every official grade.
- Email controls per REN-ISAC: active-course-only contacts, recipient limits, BCC and role-based permissions.
- Disclosure: use D2L's reporting channel for vendor issues; the university should publish an RFC 9116-style security contact.
- No credential testing, SAML replay, API calls, fuzzing, or content bypass without written authorization and a non-production plan.

## FLAGS
- One public CVE is a weak risk proxy; private advisories, non-CVE defects, and tenant misconfigurations can exist outside the catalog.
- Any SLCM-to-Brightspace grade flow is an inference in this report, not a finding; no public source ties OneRoster, IPSIS, or Grades API use to MUJ.
- The security.txt observation may be routing or parsing fallback; missing RFC fields do not prove the absence of a contact.
- The SAML redirect was observed once and not decoded; it does not prove login success, claim mapping, MFA, or Brightspace linkage.
- D2L ISO 27001 and control claims describe vendor posture, not the MUJ tenant configuration.
- All page fetches and status checks are point-in-time and unverified by this digest.

## COVERAGE
Chars read: 43,853 (full file, 315 lines). EOF confirmed: truncated false on the complete read.

DONE w2f-08-brightspace-security.md.digest.md

---

## w2f-09-campus-ad-patterns.digest

## REPORT
Source file: w2f-09-campus-ad-patterns.md (MUJ SLCM Identity Risk: Evidence, Inference, and Controls)

## ANSWER SUMMARY
- Report analyzes the claim "Outlook password equals SLCM password" and finds it is a supplied premise, not a recovered fact. No citable public FAQ copy was found. Treat as unverified, needs MUJ confirmation.
- Public portal evidence is narrow: shows `@muj.manipal.edu` suffix, Parent Login, Student Login, Forgot Password text. This proves login audiences exist, not where passwords validate or whether MFA runs.
- Six architectures can produce one-password UX: PHS, PTA, SAML federation, Application Proxy, password writeback, or independent local store with coordinated passwords. MUJ status for all six is Unknown.
- Key decision question: does SLCM receive a password or an identity-provider token? Token input supports centralized MFA; password input needs a second question about validating directory and compensating MFA.
- Stack labels (ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai) are unverified scope assumptions, not findings from first-party text.
- No public basis to declare MFA absent or passwords duplicated. Recommended next step is an authorized administrator evidence review, not external testing.
- Incident duties: CERT-In 2022 directions require six-hour incident reporting and 180-day in-India log retention for covered entities. Shared credential makes mail and ERP one blast radius.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/Home/Index - First-party portal page, the only verified MUJ surface in the report.
- http://mujslcm.jaipur.manipal.edu/ - Indexed portal entry showing Parent Login, Student Login, Forgot Password labels.
- https://muj.slcm.jaipur.manipal.edu/ - Alternate dotted hostname cited alongside the main portal, naming ambiguity.
- https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/whatis-phs - Microsoft PHS mechanism, explains same-password UX without password storage in Entra.
- https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-pta - PTA validates cloud sign-in against on-premises AD, alternative trust boundary.
- https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/add-application-portal-setup-sso - SAML SSO lets SLCM accept Entra tokens instead of passwords.
- https://learn.microsoft.com/en-us/entra/fundamentals/security-defaults - Free baseline MFA policy, contextual prompting for ordinary users.
- https://learn.microsoft.com/en-us/entra/identity/conditional-access/overview - Conditional Access engine, evaluated after first factor, needs P1/P2 tiers.
- https://learn.microsoft.com/en-us/entra/identity/authentication/tutorial-enable-sspr-writeback - Password writeback, explains same-password-after-reset patterns.
- https://learn.microsoft.com/en-us/entra/identity/conditional-access/policy-block-legacy-authentication - Legacy protocols do not support MFA, blocking recommended in Report-only mode.
- https://www.cisa.gov/topics/cybersecurity-best-practices/multifactor-authentication - CISA MFA definition and 99% account-takeover reduction claim.
- https://www.cisa.gov/news-events/alerts/2025/04/16/cisa-releases-guidance-credential-risks-associated-potential-legacy-oracle-cloud-compromise - CISA reset and review guidance for credential incidents.
- https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf - CERT-In 70B directions, six-hour reporting and 180-day log retention.
- https://studentclearinghouse.org/about/trust/security - Higher-ed comparison showing published MFA, zero-trust, and SOC 2 claims.
- http://support.msjc.edu/support/solutions/articles/20000040321 - MSJC MFA enrollment guidance, transparency benchmark for universities.
- https://msjc.edu/mymsjc/pg.html - MSJC SSO moved to Microsoft 365 My Apps, shows what MUJ could publish.

## ACTIONABLE LEADS
- Ask MUJ for the current FAQ or policy text that states Outlook password equals SLCM password; this resolves the key premise.
- Submit an authorized evidence request covering: Entra Connect config (PHS/PTA/federation), verified-domain status, enterprise-application record for SLCM, Security Defaults and Conditional Access assignments, legacy auth policy, parent identity lifecycle, deprovisioning workflow, log retention and time sync.
- Determine whether SLCM receives a password or a token; this drives the whole conclusion.
- Check whether Parent Login is a local credential store or covered by Entra policy; do not label it an MFA bypass without config evidence.
- Verify stack labels (MVC 5.3, .NET 4.x, IIS 10, Akamai) from dependency manifests, CMDB, and edge config, not banners.
- Build one identity incident playbook spanning M365, SLCM, parent access, and on-premises directory, mapped to CERT-In reporting duties.
- Follow-up test surface: Exchange legacy protocol status and mailbox-recovery pivots, only with written authorization.

## FLAGS
- Contradiction risk: report says portal display proves `@muj.manipal.edu` usage, but the shared-password FAQ was never recovered; the two claims have different evidence strength.
- Suspicious claim: "MFA makes accounts 99% less likely to be hacked" is vendor/government stat, cited as conditional, not a guarantee.
- Unverified URLs: the FAQ with the shared-password statement is absent from references; the report admits no citable copy was found.
- Hallucination risk: reference [24] MSJC My Apps and the NSC security page are repeated across many source numbers (5, 9, 13, 30, 31, 47 all map to studentclearinghouse.org/about/trust/security), suggesting noisy citation indexing rather than distinct sources.
- Reference 1 in the full list is a "404 - Content not found" page; that source is dead.
- All MUJ architecture rows in Table 4 and Table 6 are Unknown; any reader inference that MUJ uses a specific pattern would be fabrication.
- Overall verdict calls confidence MODERATE for the risk model but LOW for backend configuration claims.

## COVERAGE
- Chars read: 47231
- EOF confirmed: true (read_file truncated=false, 323 lines)

---

## w2f-10-ct-cert-patterns.digest

## REPORT
Source file: w2f-10-ct-cert-patterns.md (MUJ SLCM Certificate Transparency Exposure and Defensive Priorities)

## ANSWER SUMMARY
- Two live naming conventions exist in CT and public pages: `mujslcm.jaipur.manipal.edu` and `muj.slcm.jaipur.manipal.edu`. Distinct DNS names, both active as of 2026-08-25 with current Entrust certificates.
- `mujslcm` exact-name query returns 10 unique serials, 9 expired, one current (Entrust DV, valid to 2026-12-21). Six certs cluster around December 22-23, 2024, likely reissues or managed rollover, not malicious issuance.
- `muj.slcm` has 4 serials, one current (valid to 2026-12-22), issued same day as the mujslcm cert by the same Entrust DV CA, suggesting coordinated renewal.
- Nine expired wildcards `*.jaipur.manipal.edu` span 2020-05-07 to 2023-12-16, issued by Amazon CAs. Wildcard retirement needs internal verification.
- Test-labeled names seen: five `testmycampus`, one `testerp`, plus `npfslcm` as an SAN beside `mujslcm` on serial 540dddb8fc45abd142751ef840ba2878. Labels prove issuance, not environment status.
- Cross-family SAN grouping pairs Jaipur wildcard SANs with CNs `*.manipalglobal.com`, `*.manipaldubai.com`, `manipal.edu`, `apply.manipal.edu`. Grouping is an inference, not proof of compromise.
- Verdict: High confidence in CT facts, Medium-Low for cluster explanations. CT shows governance sprawl, not a demonstrated vulnerability.

## KEY FACTS
- https://crt.sh/?q=%25.jaipur.manipal.edu&output=json - Family snapshot with 27 name strings, wildcard history, cross-domain SANs. Core evidence source.
- https://crt.sh/?q=mujslcm.jaipur.manipal.edu&output=json - Exact-name query, 10 serials including the December 2024 cluster and current 2026 cert.
- https://crt.sh/?q=slcm.manipal.edu&output=json - Legacy `slcm.manipal.edu` history, 9 serials, 5 with CN `sis.manipal.edu`.
- https://mujslcm.jaipur.manipal.edu/Home/Index - Portal page showing WELCOME TO MUJ PORTAL branding.
- https://muj.slcm.jaipur.manipal.edu/ - Dotted-name portal, also shows MUJ PORTAL branding, public identity of the parallel name.
- https://slcm.manipal.edu/ - Legacy MU SLcM page, lineage link to the current names.
- https://letsencrypt.org/docs/ct-logs/ - CT definition and append-only submission requirement from a CA.
- https://certificate.transparency.dev/logs/ - Official CT log directory, grounds the monitoring approach.
- https://www.digicert.com/faq/public-trust-and-certificates/what-are-ct-logs - DigiCert explanation of CT as public auditable issuance record.
- https://developers.cloudflare.com/ssl/edge-certificates/additional-options/certificate-transparency-monitoring/ - Documented CT monitoring limits: shared-cert alerts, no lookalike detection.
- https://www.nccoe.nist.gov/tls-server-certificate-management - NIST TLS cert management guidance, basis for the 8-stage workflow.
- https://www.nccoe.nist.gov/publication/1800-16/VolA/index.html - NIST SP 1800-16 volume on certificate management, inventory and monitoring emphasis.
- https://letsencrypt.org/docs/challenge-types/ - DNS-01 wildcard issuance and API credential risk guidance.
- https://crt.sh/?q=testmycampus.jaipur.manipal.edu&output=json - Returns 404 Not Found title in references, yet data is used in the testmycampus table.
- https://crt.sh/?q=npfslcm.jaipur.manipal.edu&output=json - Also titled 404 Not Found in references while npfslcm appears as an SAN elsewhere.
- https://crt.sh/?q=testerp.jaipur.manipal.edu&output=json - Titled 404 Not Found while the testerp serial is presented as evidence.
- https://www.rfc-editor.org/rfc/rfc9162 - RFC 9162 CT v2, standards anchor for log behavior.

## ACTIONABLE LEADS
- Reconcile all 10 mujslcm serials against Entrust order history and internal deployment records; unknown serials become certificate-governance incidents.
- Decide the canonical relationship between `mujslcm` and `muj.slcm`; both are current, same-day issued, one-day-differing expiry.
- Verify retirement of the nine wildcards and the `testmycampus`, `testerp`, `npfslcm` names through CA accounts, CMDB, DNS, load balancers, and repos.
- Check whether the 2022 `dms.jaipur.manipal.edu` CN with mujslcm SAN implies shared infra; confirm from deployment records.
- Assign ownership to all 27 observed name strings: current, retired, alias, third-party, unknown.
- Set up continuous CT monitoring with a normalization and serial-dedup step; alert on unknown issuer, new label, or unusual SAN grouping. Report anomalies to MUJ's security contact, never attempt revocation.
- Disclosure step: submit findings through MUJ's approved security-reporting channel only.

## FLAGS
- Contradiction: several crt.sh reference URLs are titled "404 Not Found" while the report still cites their data; results may have been collected earlier and links re-fetched later. Data provenance is weakened.
- Unverified: all cluster and grouping explanations are labeled inference; CT cannot show cause.
- Suspicious claim: same-day issuance of both current certs implies coordination, but this is inference pending CA orders.
- Hallucination risk: serials and dates are specific and internally consistent across tables, but the report is AI deep-research output; treat every serial as needing independent crt.sh re-query before use.
- The claim "five testmycampus serials" depends on the family snapshot; collection date and dedup method are stated but not reproducible inline.
- Cross-domain SAN pairs (manipalglobal, manipaldubai) are presented as fact of grouping; intent remains unknown.
- Verdict label "no demonstrated vulnerability" should keep scope: CT alone cannot prove reachability of any listed name.

## COVERAGE
- Chars read: 38419
- EOF confirmed: true (read_file truncated=false, 318 lines)

---

## w2f-11-dns-hygiene.digest

## REPORT
Source file: w2f-11-dns-hygiene.md (MUJ DNS Hygiene and Spoofing Exposure Assessment)

## ANSWER SUMMARY
- `manipal.edu` uses four Azure nameservers (ns1-36 through ns4-36 across .com/.net/.org/.info). Independent checks agree all respond authoritatively on different network ranges. Good resilience.
- `jaipur.manipal.edu` is not separately delegated: NS and SOA queries return the parent `manipal.edu` SOA. Jaipur records live inside the parent zone; MUJ DNS security is a parent-zone problem.
- DNSSEC is absent: no DS at .edu, no DNSKEY, no RRSIG; Google and Verisign DNSSEC Debugger agree as of 2026-08-25. This is the top gap.
- Public AXFR is closed: HackerTarget reports Transfer failed on all four parent nameservers. Jaipur returns "no results found", not an independent refusal.
- TXT records expose a vendor map: parent has SPF for Microsoft 365, Brightspace, SendGrid, Salesforce plus Microsoft, Google, SES, Facebook, OpenAI verification markers. Jaipur has Cisco CI, Microsoft MS= markers, malformed SPF-like fragments.
- Mail auth posture: SPF hard-fail, two Microsoft DKIM selectors per domain, MX to Microsoft 365. But both DMARC policies are p=none, so exact-domain spoofing is monitored, not blocked.
- CT shows 27 unique names in the Jaipur snapshot, 25 in-namespace, spanning 2014-2026, including test labels and two external wildcard SANs.
- Verdict: MODERATE DNS and spoofing risk, HIGH confidence in observable findings.

## KEY FACTS
- https://dns.google/resolve?name=manipal.edu&type=NS - Four Azure NS answers, the authoritative topology evidence.
- https://dns.google/resolve?name=manipal.edu&type=DS - No DS answer; .edu SOA returned, DNSSEC delegation absent.
- https://dns.google/resolve?name=manipal.edu&type=DNSKEY - No DNSKEY answered, zone unsigned.
- https://dns.google/resolve?name=manipal.edu&type=RRSIG - No RRSIGs returned, no signatures.
- https://dnssec-debugger.verisignlabs.com/manipal.edu - Independent Verisign debugger confirmation of unsigned status.
- https://api.hackertarget.com/zonetransfer/?q=manipal.edu - Public AXFR check, Transfer failed on all four authoritative NS.
- https://api.hackertarget.com/zonetransfer/?q=jaipur.manipal.edu - Jaipur check returns no results, consistent with no child zone.
- https://dns.google/resolve?name=manipal.edu&type=TXT - Parent TXT map: SPF, verification markers, opaque strings.
- https://dns.google/resolve?name=jaipur.manipal.edu&type=TXT - Jaipur TXT: Cisco CI, two MS= values, malformed SPF fragments.
- https://dns.google/resolve?name=_dmarc.manipal.edu&type=TXT - Parent DMARC p=none, no rua address visible.
- https://dns.google/resolve?name=_dmarc.jaipur.manipal.edu&type=TXT - Jaipur DMARC p=none with rua to dmarc@jaipur.manipal.edu.
- https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=A - SLCM A record 98.70.14.50; direct A, no CNAME evidence for the Akamai claim.
- https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=CNAME - No CNAME answer, contradicts the supplied Akamai-fronted assumption at DNS layer.
- https://dns.google/resolve?name=manipal.edu&type=SOA - SOA with awsdns-hostmaster.amazon.com responsible name, migration residue signal.
- https://learn.microsoft.com/en-us/azure/dns/dnssec - Azure DNSSEC docs: parent DS required for validation chain.
- https://viewdns.info/dnsreport/?domain=manipal.edu - Independent NS agreement and NO GLUE note.
- https://intodns.com/manipal.edu - Second independent report of nameserver consistency across subnets.
- https://datatracker.ietf.org/doc/html/rfc7208 - RFC 7208 SPF rules, basis for judging the malformed Jaipur fragments.
- https://crt.sh/?q=%25.jaipur.manipal.edu&output=json - CT snapshot with 27 name strings and external wildcard SANs.
- https://crt.sh/?q=%25.manipal.edu - Parent CT history with api, crm, payment, online, lms, sis names.

## ACTIONABLE LEADS
- Deploy DNSSEC on the Azure-hosted `manipal.edu` zone and publish the provider DS at the .edu delegation, with rollback ownership.
- Move DMARC from p=none to quarantine then reject using aggregate report data; add rua for the parent domain.
- Build an authoritative sender register covering Outlook, Brightspace, SendGrid, Salesforce, and the direct IPv4 sender.
- Clean Jaipur TXT residue: the Brightspace-only fragment and the ip4: fragment without v=spf1 are RFC 7208-noncompliant and should be removed or corrected.
- Reconcile all 25 Jaipur CT names plus parent history against asset inventory; disposition each as current, non-production, redirect, retired, unknown.
- Verify the SLCM A record 98.70.14.50 against the Akamai premise; check origin of the awsdns-hostmaster SOA field.
- Add CAA policy for parent and Jaipur zones; both return no CAA answer.
- Monitor CT continuously for new serials, issuers, and SAN groups; report anomalies through MUJ channels.

## FLAGS
- Contradiction: report says Akamai is a supplied premise and DNS shows a direct A record with no CNAME; the Akamai-fronted architecture is not confirmed at DNS layer.
- Suspicious claim: `awsdns-hostmaster.amazon.com` SOA field implies past Route 53 use; labeled inference, needs owner confirmation.
- Unverified: DNSSEC absence is dated 2026-08-25; DNS state can change, treat as point-in-time.
- Hallucination risk: TXT verification token details are redacted on purpose; counts are claims from a single resolver query. Re-query dns.google to confirm before relying on exact values.
- The "no results found" Jaipur AXFR result must not be read as Jaipur refusing transfers; no Jaipur zone exists publicly.
- Malformed SPF fragment judgment depends on RFC 7208 interpretation; the fragment text is quoted but partly redacted.
- Verisign debugger result is cited without a saved copy; re-run before publishing findings.
- CT name classification (role labels like ERP, DMS) is inference from acronyms, not verified function.

## COVERAGE
- Chars read: 40122
- EOF confirmed: true (read_file truncated=false, 326 lines)

---

## w2f-12-waf-fingerprint.digest

## REPORT
Source file: w2f-12-waf-fingerprint.md (Distinguishing Akamai WAF From MUJ Application Responses)

## ANSWER SUMMARY
- A 403 status or Access Denied body is not attribution. Akamai can deny, craft custom error pages, and rewrite status and headers at the edge. Response appearance alone cannot name the deciding layer.
- Three decision planes exist on the MUJ path: Akamai edge, IIS/application origin, Microsoft 365 identity. A user-visible denial can come from any of them; one screenshot cannot identify the plane.
- Strongest Akamai fingerprint is a correlation handle, not a logo: the error reference string (Translate Error String tool can return WAF, origin, client, edge details), X-Akamai-Request-ID, and SIEM events with policyId, rule IDs, actions.
- OWASP CRS on MUJ is unproven. CRS uses anomaly scoring (default inbound 5, outbound 4), but Akamai's own vocabulary is Kona Rule Set and Adaptive Security Engine; no source equates them.
- IP allowlist is unproven. Akamai Client IP criteria exist (address, range, CIDR, connecting IP or X-Forwarded-For), but only config or matched-event evidence establishes MUJ policy. Campus-vs-residential difference has many explanations.
- Microsoft identity is verified context: realm check labels muj.manipal.edu a managed MUJ realm, MX routes to Microsoft, and MUJ's published Office 365 SOP uses login.microsoftonline.com.
- Recommended path is passive capture plus log correlation, budget of one ordinary baseline navigation per approved context, stop on challenge or 429.
- Verdict: Medium confidence in architecture assessment, very high confidence in attribution methodology.

## KEY FACTS
- http://mujslcm.jaipur.manipal.edu/ - Public portal surface, WELCOME TO MUJ PORTAL, parent/student/forgot-password routes.
- http://login.microsoftonline.com/getuserrealm.srf?login=probe@muj.manipal.edu&xml=1 - Realm probe evidence that muj.manipal.edu is a managed MUJ realm.
- http://dns.google/resolve?name=muj.manipal.edu&type=MX - MX to muj-manipal-edu.mail.protection.outlook.com, Microsoft 365 mail routing.
- http://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf - MUJ Office 365 SOP, documents Microsoft login flow and account security steps.
- https://techdocs.akamai.com/edge-diagnostics/docs/translate-error-string - Official translator for Akamai error reference codes, returns WAF and origin details.
- https://techdocs.akamai.com/edge-diagnostics/docs/pragma-headers - X-Cache, X-Cache-Remote, X-Check-Cacheable, X-Akamai-Request-ID diagnostic headers.
- https://techdocs.akamai.com/cloud-security/docs/app-api-protector - Akamai WAF can alert or deny based on configured actions.
- https://techdocs.akamai.com/terraform/docs/as-rc-custom-deny - Custom deny pages and redirects, why bodies are not invariant fingerprints.
- https://techdocs.akamai.com/edgeworkers/docs/response-object - EdgeWorkers can set status codes and modify headers, edge-transformed responses.
- https://techdocs.akamai.com/property-mgr/docs/client-ip - Client IP criterion, 300 addresses/ranges/CIDRs, connecting IP or X-Forwarded-For option.
- https://techdocs.akamai.com/terraform/docs/as-rc-rate-policy - Rate policies with average, burst, penalty-box parameters.
- https://coreruleset.org/docs/2-how-crs-works/2-1-anomaly_scoring/ - CRS cumulative anomaly scoring with documented thresholds.
- https://coreruleset.org/docs/2-how-crs-works/2-2-paranoia_levels/ - CRS paranoia levels, PL1 low false alarms.
- https://techdocs.akamai.com/terraform/docs/as-rc-rule-upgrade - KRS and ASE modes, automatic vs manual rule upgrades.
- https://www.akamai.com/resources/solution-brief/adaptive-security-engine - ASE combines threat scoring, behavior, anomaly detection.
- http://akamai.com/products/bot-manager - Bot Manager scores 0 to 100, tuned responses, intentionally opaque.
- https://techdocs.akamai.com/powershell/docs/siem - SIEM events carry configId, policyId, rule IDs, actions, requestId, status.
- https://www.rfc-editor.org/rfc/rfc9110.html - HTTP semantics reference for status code attribution limits.
- https://learn.microsoft.com/en-us/iis/configuration/system.webserver/httperrors/ - IIS httpErrors, origin-side custom error possibility.

## ACTIONABLE LEADS
- Preserve full incident bundles from any reported denial: complete reference string, headers, body hash, screenshot, redirect chain, UTC time, URL, public client IP, browser version, auth state.
- Have an authorized Akamai operator translate error reference strings and search SIEM by requestId or narrow UTC/client/host/path tuple.
- Ask the Akamai admin for security mode, custom-deny definitions, Bot Manager status, rate policies, Client IP criteria, evaluation-mode availability.
- Correlate three ways before classifying: client artifact, Akamai event, IIS/application log. Classify outcomes as edge security, origin response, edge-transformed, identity-provider, or indeterminate.
- One baseline navigation per approved context maximum; stop on challenge, 429, latency rise, or operator request.
- Confirm the Microsoft identity plane via realm check and MX before blaming WAF.
- Refer any positive-control rule testing to evaluation mode or staging under owner control.

## FLAGS
- Contradiction: Akamai presence is a team-supplied premise, while the report itself says no collected first-party source confirms it; all Akamai statements are conditional.
- Suspicious claim: intensity of "Akamai-style reference string" as strong evidence assumes the translator is real and accessible; verify before treating it as a finding.
- Unverified URLs: realm probe uses a probe@muj.manipal.edu address; the report claims it labels the domain as managed, but the raw XML output is not reproduced.
- Hallucination risk: Bot Manager, allowlist, and rate policy statements are product capability citations, not MUJ observations; do not convert them into MUJ findings.
- The exact MUJ deny page template, ruleset, thresholds, and allowlist are unknown; any concrete claim about them would be fabricated.
- Two competing explanations for every observed pattern (WAF, bot score, rate policy, app logic) are retained deliberately; readers must not pick one without telemetry.
- The report contains no actual MUJ 403 capture; every 403 claim in it is hypothetical scenario language.

## COVERAGE
- Chars read: 41800
- EOF confirmed: true (read_file truncated=false, 290 lines)

---

## w2g-01-reddit-r-manipal.digest

## REPORT
Source file: w2g-01-reddit-r-manipal.md (MUJ SLCM Reddit OSINT: Findings, Gaps, and Safe Actions)

## ANSWER SUMMARY
- Recurring availability complaints: SLCM described as crashing every other day and a MUJ site unusable for much of a semester.
- Identity lifecycle friction: a registration number changed after intra-sliding and both old and new identifiers were rejected.
- Payment reconciliation failures: fee paid with receipt while SLCM showed pending; a stale due blocked an admit card until proof and escalation.
- Academic data reports: missing or wrong-term attendance, removed results tab, grades decreased, SLCM 2.0 preference and subject regressions.
- CGPA exposure allegation is unverified: site later returned 404, a commenter claimed IT patched within a week, no institutional confirmation found.
- Public GitHub projects document ongoing automation interest, one advertising CAPTCHA solving; existence is not evidence of a current vulnerability.
- The supplied stack remains an unverified inventory hypothesis; Reddit evidence does not confirm it.
- Coverage is a high-confidence sample, not exhaustive; some threads lacked recoverable permalinks or dates.

## KEY FACTS
1. https://www.reddit.com/r/manipal/comments/17anbg2/slcm_is_literally_ass/ - leading availability complaint from 2023.
2. https://www.reddit.com/r/manipal/comments/17usdb4/attendance_lock_for_slcm/ - attendance lock thread; comment claims the lock is about one week earlier.
3. https://www.reddit.com/r/manipal/comments/1qa5h99/slcm_20_manipal_situation_summarised/ - SLCM 2.0 regression reports.
4. https://www.reddit.com/r/manipal/comments/1ncl5xy/cgpa_data_leak_of_all_branch_students/ - CGPA exposure allegation with 404 edit and patch claim.
5. https://www.reddit.com/r/Manipal_Academics/comments/1993mdc/slcm_login/ - intra-sliding registration number rejection.
6. https://www.reddit.com/r/Manipal_Academics/comments/1lzf0ht/paid_my_fees_but_still_showing_as_pending_on_slcm/ - fee paid but pending with receipt available.
7. https://www.reddit.com/r/manipal/comments/1m23kxi/one_of_the_worst_departments_in_the_college/ - stale SLCM due blocking an admit card.
8. https://www.reddit.com/r/manipal/comments/1cyd4xv/what_is_casual_term_fee_on_slcm/ - casual term fee concern, fee pending Rs 6,000.
9. https://www.reddit.com/r/manipal/comments/1m0ofr4/has_anyone_used_the_emi_option/ - GrayQuest EMI receipt concern in SLCM.
10. https://www.reddit.com/r/Manipal_Academics/comments/1plljtw/it_appears_they_have_removed_the_results_tab_from/ - removed results tab and non-working academics tab report.
11. https://www.reddit.com/r/Manipal_Academics/comments/1pny6zb/grades_decreased_on_slcm/ - grades decreased report, details unrecovered.
12. https://www.reddit.com/r/Manipal_Academics/comments/1s8mhsd/can_someone_please_share_me_the_parent_slcm_link/ - parent link request; user-ID format intentionally withheld in the report.
13. https://github.com/tejaskash/slcm-api - Flask REST API for attendance and marks from SLCM.
14. https://github.com/sankalp2004/SLCM-is-Dumb - CGPA extraction with CAPTCHA automation and credential warnings.
15. https://mujslcm.jaipur.manipal.edu/ - public portal surface: "WELCOME TO MUJ PORTAL", Sign In, Parent Login, @muj.manipal.edu.

## ACTIONABLE LEADS
- Build a measurement plan for availability, login success by lifecycle state, payment reconciliation age, and attendance freshness.
- Create a finance-to-SLCM reconciliation queue with immutable transaction IDs, idempotent updates, and visible escalation status.
- Preserve evidence of the CGPA allegation privately and ask the owner to confirm scope, containment, and fix status.
- Model identity as a state machine (admitted, intra-slid, provisioned, parent-linked, active) and test sync with synthetic accounts.
- Scan public SLCM repositories for exposed secrets and rotate any compromised credentials.
- Publish status labels for attendance and marks ("not yet uploaded", "pending validation", "frozen", "corrected") and correction tickets.

## FLAGS
- The CGPA allegation is unverified; the patch claim is a single commenter with no institutional confirmation.
- Dates are partial: some threads have Unix timestamps, others only relative ages.
- Reddit indexing is incomplete; deleted and unindexed threads mean the corpus is a sample.
- Student workarounds (lab switching, credential advice) are not official procedures.
- A 404 is not a security conclusion; only authorized tests with synthetic records can prove object-level controls.

## COVERAGE
Chars read: 38929. EOF confirmed: yes (truncation flag false on full read).

---

## w2g-02-reddit-india-academics.digest

## REPORT
Source file: w2g-02-reddit-india-academics.md (Reddit OSINT Findings for the MUJ SLCM Ecosystem)

## ANSWER SUMMARY
- No confirmed MUJ SLCM incident was located in r/Indian_Academia or r/developersIndia; the negative result is bounded to the reviewed index.
- Manipal posts in both communities are mostly education-choice discussions (VIT vs Manipal 2021, DU vs Manipal 2026, Online BCA from MUJ).
- One out-of-scope MUJ SLCM password complaint was found in r/manipaljaipur: password rejected despite the poster believing it correct.
- The most technical item is the IITK B.Cyber Pingala report: client-side CAPTCHA and per-browser OTP limit, reported and allegedly patched with server-side validation and rate limits.
- Generic Indian education portals show recurring themes: failed logins, upload errors, an HTML-as-JSON error, Aadhaar already registered, and spam-call privacy concerns.
- The Pingala case transfers as a defensive lesson: a client-visible control must not be the sole enforcement point.
- No Reddit item in scope maps to a specific MUJ component; treat the corpus as risk themes, not findings.

## KEY FACTS
1. https://www.reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue - out-of-scope MUJ SLCM login complaint, password rejected.
2. https://www.reddit.com/r/developersIndia/comments/1ug3qpw/ironically_the_iitk_bcyber_application_portal/ - Pingala CAPTCHA/OTP disclosure and claimed remediation.
3. https://www.reddit.com/r/Indian_Academia/comments/ny1o91/ysk_factors_to_take_into_account_while_choosing/ - 2021 VIT vs Manipal comparison, education choice only.
4. https://www.reddit.com/r/Indian_Academia/comments/1u1osy9/manipal_online_scammed_me_and_refused_to_refund/ - Manipal Online refund complaint; consumer service, not portal security.
5. https://www.reddit.com/r/developersIndia/comments/1ut6xh8/need_advice_regarding_online_manipal_university/ - Online BCA from Manipal University Jaipur discussion.
6. https://www.reddit.com/r/Indian_Academia/comments/1q2l1f9/unable_to_candidate_login_to_download_admit_card/ - UGC NET candidate login failure with password reset loop.
7. https://www.reddit.com/r/Indian_Academia/comments/1ub0ira/pmrc_portal_is_full_of_bugs_and_does_not_work_help/ - PMRC upload error returning HTML where JSON was expected.
8. https://www.reddit.com/r/Indian_Academia/comments/1npirgk/nats_portal_aadhaar_misuse_blocking_my_drdo/ - Aadhaar already registered on NATS, blocked a DRDO internship.
9. https://www.reddit.com/r/Indian_Academia/comments/1ocym4m/vidyalaxmi_portal_doesnt_have_my_institute_listed/ - PM Vidyalaxmi form coverage gap.
10. https://www.reddit.com/r/Indian_Academia/comments/1crm5bh/swayam_portal_nta_hall_ticket_download/ - Swayam/NTA navigation failure report.
11. https://www.reddit.com/r/developersIndia/comments/1cv6qy3/built_this_result_portal_for_my_university/ - result portal architecture context (ASP.NET Core, Dapper, PostgreSQL, 50k+ PDF pages).
12. https://www.reddit.com/r/developersIndia/comments/1m4qbhe/is_tcs_candstatus_inspect_portal_code_trick_true/ - TCS portal status-code inspection thread, excluded as recruitment context.
13. https://www.reddit.com/r/Indian_Academia/search.rss?q=SLCM&restrict_sr=1&sort=relevance&t=all - SLCM search feed in the requested subreddit, no result.
14. https://www.reddit.com/r/developersIndia/search.json?q=SLCM&restrict_sr=1&sort=relevance&t=all&raw_json=1 - SLCM search in developersIndia, no relevant result.
15. https://www.reddit.com/r/Indian_Academia/comments/1t2e3jg/spent_hours_just_trying_to_get_my_photo_and/ - government exam portal timeout and signature "too large" complaint.

## ACTIONABLE LEADS
- Record the r/manipaljaipur login complaint as an out-of-scope UX lead for MUJ support and provisioning review.
- Use the Pingala case as a cross-portal study for server-side CAPTCHA and OTP enforcement, rate limits, and telemetry.
- Review reset token expiry, account-state leaks in error messages, and server-side rate limits.
- Review upload workflows: content types, size bounds, file-type validation, malware scanning, and non-sensitive errors.
- Treat the Aadhaar reuse case as an identity-binding lesson for dispute, unlink, and re-verification paths; never test on MUJ without authorization.
- Do not label MUJ SLCM vulnerable on the basis of generic portal themes.

## FLAGS
- The Pingala before/after states are user-reported; no independent validation exists in the corpus.
- The negative search result is index-limited, not proof of absence.
- One reference (ref 39) pairs a deleted-comment title labeled r/HairyAssGirls with an r/Indian_Academia URL; treat the reference list as noisy.
- "Manipal Online scammed me" is a consumer complaint, not security evidence.
- The TCS thread was intentionally excluded; do not count it as university evidence.

## COVERAGE
Chars read: 35311. EOF confirmed: yes (truncation flag false on full read).

---

## w2g-03-quora-manipal.digest

## REPORT
Source file: w2g-03-quora-manipal.md (MUJ SLCM Quora Footprint and Safe OSINT Assessment)

## ANSWER SUMMARY
- The Quora footprint is thin: one accessible anonymous answer on MUJ attendance publication and a two-day lock.
- Official sources carry more weight: the onboarding guide says credentials go to a personal Gmail account, parent mobile OTP enables Parent login, and documents are verified at physical reporting.
- The marks-sharing question is discoverable but its answer fields are unavailable; the CGPA page is blocked; neither supports any conclusion.
- No confirmed MUJ SLCM insider was found; visible Quora profile labels are affiliation signals only.
- Two MUJ-labelled hostnames are indexed (mujslcm.jaipur.manipal.edu and muj.slcm.jaipur.manipal.edu); hostname confusion is a documentation and phishing topic.
- The supplied stack (ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai, M365) remains unverified by Quora evidence; "official outlook ID" wording proves nothing.
- The right output is a defensive data-flow and privacy checklist plus authorized questions, not a test recipe.

## KEY FACTS
1. https://mujslcm.jaipur.manipal.edu/ - official portal: Student Login, Parent Login, Forgot Password.
2. https://muj.slcm.jaipur.manipal.edu/ - alternate MUJ-labelled hostname with similar page labels.
3. http://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf - guide: credential delivery via personal Gmail, parent OTP, document upload and verification.
4. http://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - FAQ: registration link, login wording, support channels, helpline.
5. https://www.quora.com/How-is-the-attendance-calculated-at-MUJ - the only accessible relevant answer; unattributed, undated.
6. https://www.quora.com/Are-End-Semester-marks-shared-with-parents-at-MUJ - relevant question URL; answer fields unavailable.
7. https://www.quora.com/How-is-CGPA-calculated-at-Manipal-University - blocked page, error only.
8. https://www.quora.com/How-do-I-maintain-my-CGPA-at-MUJ - generic study advice snippet only.
9. https://www.quora.com/Is-Manipal-University-a-fraud - contextual page with visible profile labels and broad claims.
10. https://www.quora.com/profile/Prajay-Vats - profile label, BTech in IT at MIT, 2021; affiliation signal only.
11. http://manipal.edu/mu/academics/student-portal.html - MAHE student portal page linking to SIS at sis.manipal.edu.
12. https://student.mujonline.com/login - MUJ student portal result with helpdesk wording.
13. https://srmuniversity.quora.com/Which-is-better-CS-at-MUJ-or-CS-at-SRM-KTR - experience snippet only.
14. https://www.quora.com/What-is-the-procedure-for-getting-the-MUJ-outpass-signed - title only, no answer content.
15. https://www.quora.com/How-is-manipal-university - error-only output ("Something went wrong").

## ACTIONABLE LEADS
- Verify current attendance publication and lock policy through official MUJ channels before quoting the anonymous claim.
- Ask the owner how parent number changes are reverified, how mistaken parent links are revoked, and whether students see link status.
- Publish one canonical MUJ SLCM link and a clear support route to reduce hostname confusion and impersonation risk.
- Document onboarding data flows: Gmail delivery, OTP, document upload, physical verification.
- Request policy and sample audit records for attendance change control; do not attempt to replay or bypass locks.
- Keep MAHE SIS, MUJ SLCM, and student.mujonline.com in separate evidence buckets.

## FLAGS
- The attendance answer is anonymous, undated ("from this year"), and uncorroborated; it is not current policy.
- Marks and CGPA pages are inaccessible; do not reconstruct remembered or implied answers.
- Named profiles (Prajay Vats, Harshit Anand, Supriya Prem Kumar, Rohan Krishna, Nikita Kishore) are affiliation signals, not insider evidence; do not contact or profile them.
- "Official outlook ID" does not establish a Microsoft 365 authentication architecture.
- No Quora result with the literal hostname and both question and answer text was recovered; this is a collection limitation.

## COVERAGE
Chars read: 52298. EOF confirmed: yes (truncation flag false on full read).

---

## w2g-04-twitter-x.digest

## REPORT
Source file: w2g-04-twitter-x.md (MUJ SLCM Public-Source OSINT Report: Evidence, Gaps, and Risk Signals)

## ANSWER SUMMARY
- Direct X search pages for mujslcm, slcm.manipal, Manipal portal, and MUJ portal returned only an auth/cookie/navigation shell with no visible tweet cards; a coverage-limited negative, not proof posts do not exist.
- Four @Jaipur_Manipal post URLs were found dated Aug 15, 18, 21, 24 2026; all concern campus events or a secure-cloud training, none is an SLCM outage or security report.
- The official MUJ FAQ names https://mujslcm.jaipur.manipal.edu/ as the SLCM registration link and gives dms@jaipur.manipal.edu and ams@jaipur.manipal.edu for login trouble; the strongest attribution source in the report.
- Two public complaints exist: password rejected despite the user believing it correct (r/manipaljaipur) and fee paid but still marked pending (r/Manipal_Academics); both show relative dates "1y ago" and no resolution.
- Extension ecosystem: SLCM Feedback Auto-Fill requests access to all websites; Detain Shield claims MUJ-only attendance use. Both are publisher disclosures, not audits.
- Publicly indexed academic artifacts (2025 grade sheet, BTech transcript on Scribd) are provenance concerns, not proof of breach; preserve URLs, do not redistribute.
- Unofficial projects (muj_slcm repo, SLCM-api, MUJStella, Arcadia) must be kept separate from official assets in any asset register.
- The supplied stack (MVC 5.3, .NET 4.x, IIS 10, Akamai, M365) was not independently confirmed by this public-source pass.

## KEY FACTS
1. https://mujslcm.jaipur.manipal.edu/ - target portal, "WELCOME TO MUJ PORTAL" branding.
2. https://muj.slcm.jaipur.manipal.edu/ - alternate hostname displaying @jaipur.manipal.edu identity label.
3. https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - official SLCM FAQ; registration link and support contacts.
4. https://x.com/Jaipur_Manipal/status/2091866801852613107 - Aug 24 2026 Azure secure-cloud training post; closest security-adjacent item, not a portal incident.
5. https://x.com/Jaipur_Manipal/status/2088634410635759649 - Aug 15 2026 Independence Day post; provenance only.
6. https://x.com/Jaipur_Manipal/status/2089600565877821835 - Aug 18 2026 IAESTE culinary workshop post.
7. https://x.com/Jaipur_Manipal/status/2090688741627285837 - Aug 21 2026 Pitch Fest post.
8. https://www.reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue - public login complaint, no verified root cause.
9. https://www.reddit.com/r/Manipal_Academics/comments/1lzf0ht/paid_my_fees_but_still_showing_as_pending_on_slcm - fee-status sync complaint, no resolution shown.
10. https://addons.mozilla.org/en-US/firefox/addon/slcm-feedback-auto-fill/ - extension automating feedback forms; broad all-websites permission.
11. https://chromewebstore.google.com/detail/detain-shield/mjedocjcijmphjgbfnkpceiblklpalpp - extension scoped to MUJ SLCM attendance claims.
12. https://www.scribd.com/document/983177245/Https-Mujslcm-jaipur-manipal-edustudentAcademicGradesForStudent - 2025 grade sheet artifact with SLCM-derived path in title.
13. https://github.com/Anushkakumar10/muj_slcm - repo created Jul 13 2025, zero stars, one commit, no affiliation claim.
14. https://mujstella.in/ - independent platform, expressly not affiliated with MUJ.
15. https://muj.onlinemanipal.com/notifications - official notices page; dated notices with no outage or security incident text.

## ACTIONABLE LEADS
- Monitor @Jaipur_Manipal with date-stamped records for future SLCM outage or security mentions.
- Report the Scribd artifact URLs and data categories to MUJ via dms@ or ams@; do not download, mirror, or enumerate more records.
- Treat both extensions as a trust boundary; review publisher, permissions, update history before any use on university accounts.
- Next pass should capture canonical Reddit timestamps; "1y ago" must not be converted to invented dates.
- Clarify with the owner whether mujslcm.jaipur.manipal.edu and muj.slcm.jaipur.manipal.edu are aliases or separate deployments.
- Watch unofficial projects (muj_slcm, SLCM-api, MUJStella, Arcadia) for credential handling; no testing.

## FLAGS
- X search pages showed no tweet content; any "there are no posts" statement would be unsupported.
- "1y ago" relative dates on both Reddit pages; exact dates not established.
- Scribd artifacts: how they became indexed is unknown; could be user upload, misconfiguration, or unrelated posting.
- Extension permissions and data claims are publisher disclosures, not independent audits.
- MUJStella and Arcadia are explicitly non-affiliated; do not attribute their behavior to MUJ.
- The Aug 24 training post mentions Azure security; institutional training language is not evidence of production architecture.

## COVERAGE
- Chars read: 32,908
- EOF confirmed: yes (truncated: false on final page, 229 of 229 lines)

---

## w2g-05-youtube-tutorials.digest

## REPORT
Source file: w2g-05-youtube-tutorials.md (MUJ SLCM Public-Video OSINT Report)

## ANSWER SUMMARY
- The only clearly MUJ-SLCM-specific walkthrough located is a Facebook video by JS Group of Institutions: 1:42 duration, 142 views, dated Oct 7 2021. Metadata is confirmed; no transcript or screen inventory.
- A YouTube video (9R1mCmnhD6Y, 10:39, published Sep 5 2025, creator "dear dashu") describes a MUJ student portal and LMS walkthrough but was unavailable to the extractor; SLCM identity and screen content unverified.
- No verified MUJ-specific YouTube fee-payment, timetable, or developer-tools/network-traffic video exists in this pass; a bounded negative, not proof of absence.
- The official fee page states existing-student online payment uses https://mujslcm.jaipur.manipal.edu/ and that hostel and mess fees are paid via the SpaceBasic app.
- The official MUJ YouTube channel shows institutional and programme content only; no SLCM or portal tutorials visible in the extracted listing.
- Third-party how-to material exists (slcm.vercel.app attendance guide, MUJStella) but is expressly non-affiliated with MUJ.
- The SLCM-api repository targets slcm.manipal.edu, not mujslcm.jaipur.manipal.edu; not evidence about the MUJ host.
- Stack assertions (MVC 5.3, .NET 4.x, IIS 10, Akamai, M365) are unverified; the Microsoft identity link is only an inference from domain and federation context.

## KEY FACTS
1. https://www.facebook.com/watch/?v=3067261673486711 - MUJ-SLCM Student Portal Walkthrough, JS Group, 1:42, 142 views, Oct 7 2021.
2. https://www.youtube.com/watch?v=9R1mCmnhD6Y - MUJ student portal/LMS explainer, 10:39, Sep 5 2025; unavailable to extractor.
3. https://www.youtube.com/channel/UCFbeX4UJyd4fHTCnCVGob_Q - official MUJ YouTube channel; no tutorial listings visible.
4. https://jaipur.manipal.edu/pay-fee-online.php - fee page; SLCM URL for existing students, SpaceBasic for hostel/mess.
5. https://mujslcm.jaipur.manipal.edu/Home/Index - portal landing with MUJ PORTAL labels and @muj.manipal.edu wording.
6. https://www.jaipur.manipal.edu/time-table.php - official timetable page; no SLCM navigation tutorial extracted.
7. https://slcm.vercel.app/guides/check-attendance-muj - betterSLCM third-party attendance guide, not university-owned.
8. https://mujstella.in/ - independent student platform, expressly not affiliated.
9. https://github.com/nikeplusdash/SLCM-api - API project for slcm.manipal.edu; separate host from MUJ.
10. https://www.manipal.edu/mu/academics/student-portal.html - MAHE student portal page pointing to sis.manipal.edu; separate service label.
11. https://www.nuget.org/packages/Microsoft.AspNet.Mvc - generic package page; not host-specific MUJ evidence.
12. http://login.microsoftonline.com/getuserrealm.srf?login=probe@muj.manipal.edu&xml=1 - federation-related realm response; inference only.
13. https://www.youtube.com/watch?v=1v0QXkIpkGo - Trent University timetable walkthrough; excluded false positive.
14. https://www.reddit.com/r/manipaljaipur/comments/1uaqh0g/muj_fee_deadline - unrelated fee-deadline discussion; not a payment walkthrough.
15. https://jaipur.manipal.edu/ - MUJ main site; institutional context.

## ACTIONABLE LEADS
- Review the Facebook walkthrough manually in an ordinary browser; catalog visible screens without logging in or reproducing personal data.
- Search title variants, course and department terms, Hindi phrasing, and academic-year posts for the missing tutorial types.
- Record access dates, URLs, titles, and hashes where lawful for both videos; metadata may change.
- Use the official MUJ channel as a provenance control; do not treat third-party videos as official productions.
- If a developer-tools or network-traffic video surfaces, do not replay captured requests, tokens, or identifiers.
- Monitor the fee page for payment-channel changes between SLCM and SpaceBasic.

## FLAGS
- Facebook video evidence is title and metadata only; no transcript, so screen-level claims would be inference.
- The YouTube video was unavailable to the extractor; description claims are unverified.
- The getuserrealm lookup is an indexed probe result; it supports an enterprise identity inference, not proof of the SLCM login flow.
- The Trent University video is an excluded false positive; name collisions are a recurring risk in this topic.
- Views, durations, and dates are snapshot values and may change.
- The SpaceBasic statement comes from fee-page text; the app itself was not assessed.

## COVERAGE
- Chars read: 29,140
- EOF confirmed: yes (truncated: false on final page, 187 of 187 lines)

---

## w2g-06-github-orgs-teams.digest

## REPORT
Source file: w2g-06-github-orgs-teams.md (MUJ SLCM Ecosystem: Public GitHub Intelligence and Defensive Findings)

## ANSWER SUMMARY
- Strongest direct SLCM artifact: DK10WS/SLCM_APP (SLCM SWITCH), a Flutter/Dart + FastAPI/Python app with student and parent login and retrieval of grades, GPA/CGPA, and attendance; 71 commits in snapshot, created Jun 18 2025. Authorization and deployment unresolved.
- Integration patterns are diverse: a mobile client, a Chrome extension (SlcmPlus with a MUJ SLCM host match), a SLCM+LMS aggregator (SlcmAndLms-aggregator), and server-side scrapers (Manipal The Talk App-Backend, SLCM-is-Dumb).
- a campus technical org and MUJ ACM are verified MUJ anchors via the official teams page; their GitHub footprints are website and education projects with no cited SLCM link.
- MUJ Central is a student-services portal candidate: OTP to an authorized Manipal ID, dashboard with attendance and timetable, resources, event registration; no explicit SLCM integration in the cited README.
- SLCM-is-Dumb documents automated login and captcha/OCR and warns contributors not to commit .env files; treat as credential-sensitive, review offline only.
- HackX3.0 is event infrastructure (official event website repo, 355 commits), not a participant submission; the IIC listing says GitHub links are optional.
- The supplied stack (ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai, M365) is not confirmed by this corpus; @muj.manipal.edu on the landing page proves a domain, not an identity provider.
- No vulnerability findings; the pass was passive and no repository was executed or tested.

## KEY FACTS
1. https://github.com/DK10WS/SLCM_APP - SLCM SWITCH app; direct MUJ SLCM client with login and academic retrieval.
2. https://github.com/DK10WS/SLCM_APP/blob/main/README.md - README documenting Flutter, FastAPI, custom email/password auth.
3. https://github.com/madhav-manchanda/SlcmAndLms-aggregator/tree/main - aggregator combining MUJ SLCM and LMS data.
4. https://github.com/Tejas-Narula/SlcmPlus/tree/main - Chrome extension enhancing the MUJ SLCM experience.
5. https://github.com/Tejas-Narula/SlcmPlus/blob/main/manifest.json - manifest with MUJ SLCM host match and attendance handling.
6. https://github.com/manipalthetalk/App-Backend - scraper backend for marks, attendance, timetable; Manipal Karnataka, not MUJ.
7. https://github.com/sankalp2004/SLCM-is-Dumb - CGPA scraper with Selenium/OCR, automated login language, .env warning.
8. https://github.com/raghavkapoor-prog/MUJ-Central - student-services portal; OTP login, attendance and timetable dashboard.
9. https://github.com/mujcentral - MUJ Central organization profile, seven repositories in snapshot.
10. https://[campus org repository] - team profile pinning the official team website.
11. https://[campus org repository] - Next.js team site with Vercel deployment reference.
12. https://github.com/orgs/MUJ-ACM-SCHAP/repositories - MUJ ACM Student Chapter organization, 19 repositories in snapshot.
13. https://muj.acm.org/ - ACM chapter site; GMC certificate manager, coding platform, AI chatbot.
14. https://github.com/AwesomeSam9523/HackX3.0 - official MUJ HackX 3.0 website repo; 355 commits in snapshot.
15. https://github.com/slcm-manipal/slcm-manipal.github.io - grades website with MU SLcM_files directory; MUJ link unresolved.

## ACTIONABLE LEADS
- Authorized static review of SLCM_APP and SlcmPlus: credential handling, token storage, API endpoint references.
- Scan SLCM-is-Dumb history for committed .env secrets offline; rotate confirmed secrets through owners; never try credentials.
- Ask each repository owner and MUJ which projects are approved, deployed, and current.
- Request a data-flow diagram from MUJ Central maintainers: where dashboard attendance and timetable data originate.
- Under written scope, compare SlcmPlus-referenced routes and page handling against live portal structure.
- Keep hackathon submission provenance separate: no repo is a submission without an explicit public link.
- Route any likely issue found in static review through responsible disclosure; no live testing.

## FLAGS
- Snapshot discrepancy: the campus org website repo shows 71 commits in one snapshot and 46 commits in another; activity counts are context, not live values.
- a second similarly named repo and the campus org website repo are two similarly named repos; identity must be reconciled before ownership assumptions.
- manipalthetalk is Manipal, Karnataka, not MUJ; do not merge into the MUJ set.
- slcm-manipal organization does not identify MUJ; string "MU" alone is not attribution.
- Repository descriptions are intent, not proof of deployment, authorization, or security.
- The IIC listing appears with two URLs in the report (1702074 and 1702624); listing URLs are volatile.
- SLCM-is-Dumb targets slcm.manipal.edu per its own description; captcha language plus credentials make it high-sensitivity.

## COVERAGE
- Chars read: 51,994
- EOF confirmed: yes (truncated: false on final page, 273 of 273 lines)

---

## w2g-07-github-code-muj.digest

## REPORT
Source file: w2g-07-github-code-muj.md. Public GitHub exposure assessment for the MUJ SLCM vocabulary (mujslcm, mujslcm.jaipur.manipal.edu, slcm.manipal.edu, jaipur.manipal.edu, muj.manipal.edu). Source-inventory report with a full 76-entry reference table; no live testing performed.

## ANSWER SUMMARY
- Overall confidence: High for public artifact identification, medium for exposure severity, low for live compromise or exploitability. A repo page proves a public artifact was visible, not deployment or current validity.
- Top finding: KrishGoel/slcm-feedback-automation .env.example shows populated name, registration number, and password-like value instead of placeholders. Values redacted in the report; treat as potentially compromised, rotate through the university process, clean git history, do not test the value.
- Secondary finding: vikrant500/college_portal_web_and_dbms portal-clone dir holds an HTTrack cookies.txt with a populated __RequestVerificationToken entry for the MUJ host. Classified as sensitive token-like artifact, validity unknown.
- DK10WS/SLCM_APP (Flutter) is the richest route map: MUJ base URL, Student/Academic/GetAttendanceSummaryList, parent OTP paths, dashboard, GitHub release-check; cookie-bearing POSTs, CSRF token parsing, JSON response parsing, change-password flow. Session cookie held in a static string; username and password saved through shared preferences.
- Tejas-Narula/SlcmPlus is DOM-only Chrome MV3 augmentation on exact MUJ attendance, marks, and grades pages; computes attendance, internal marks, GPA. No credential or external API client visible in cited excerpts.
- AddisionS/slcm-feedback-form-filler sets feedback controls to all-Yes or all-No and clicks submit; manifest declares <all_urls>, *://*/*, scripting, activeTab, broader than the MUJ-specific description.
- Legacy wrappers manipalthetalk/App-Backend, canaryGrapher/slcmAPI, nikeplusdash/SLCM-api target slcm.manipal.edu, not Jaipur. App-Backend server.go interpolates regno and password into a shell command (inferred command-injection risk) and sets wildcard CORS with a regno-keyed cache.
- GitHub artifacts do not independently verify ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai, or Microsoft 365 federation; those stay requester-supplied context. Client code is not a server fingerprint.

## KEY FACTS
- https://github.com/KrishGoel/slcm-feedback-automation/blob/main/.env.example - populated credential-like values; highest-priority public secret finding.
- https://github.com/vikrant500/college_portal_web_and_dbms/blob/main/mujslcm.jaipur.manipal.edu_122/cookies.txt - public HTTrack cookie file with verification-token entry for the MUJ host.
- https://github.com/DK10WS/SLCM_APP/blob/main/lib/pages/redirects.dart - MUJ base URL plus attendance, parent-OTP, dashboard, and release-check route constants.
- https://github.com/DK10WS/SLCM_APP/blob/main/lib/pages/login.dart - parses hidden __RequestVerificationToken, posts EmailFor, LoginFor, UserName, Password for student and parent modes, handles redirects and OTP.
- https://github.com/DK10WS/SLCM_APP/blob/main/lib/session_manager.dart - session cookie in a static string; presence of the string equals login state.
- https://github.com/DK10WS/SLCM_APP/blob/main/lib/utils/util.dart - adds Cookie headers and reads saved username/password from shared preferences.
- https://github.com/DK10WS/SLCM_APP/blob/main/lib/pages/Attendance.dart - cookie-bearing POST to the attendance constant; parses AttendanceSummaryList with course id, percentage, total and attended classes.
- https://github.com/Tejas-Narula/SlcmPlus/blob/main/manifest.json - MV3 content script matching exact MUJ academic page URLs.
- https://github.com/Tejas-Narula/SlcmPlus/blob/main/content.js - table-cell reads, marks and GPA calculations, mutation observer; no network call or credential visible.
- https://github.com/AddisionS/slcm-feedback-form-filler/blob/main/chrome/manifest.json - broad host permissions incl. <all_urls> and *://*/*.
- https://github.com/AddisionS/slcm-feedback-form-filler/blob/main/chrome/content.js - sets radio/dropdown values, dispatches change events, can click btnSubmit.
- https://github.com/manipalthetalk/App-Backend/blob/master/server.go - forms a shell command from externally supplied regno and password; wildcard CORS; cache keyed by regno.
- https://github.com/canaryGrapher/slcmAPI/blob/master/server.js - archived Puppeteer REST wrapper with /getscores, /getattendance, /getprofile, /validateuser; deprecated after portal CAPTCHA.
- https://github.com/sankalp2004/SLCM-is-Dumb/blob/master/.env.example - placeholder-only credentials (low signal); targets non-Jaipur slcm.manipal.edu.
- https://github.com/KrishGoel/slcm-feedback-automation/blob/main/script.py - Selenium flow: opens MUJ root, fills UserName and Password, filters pending feedback, enters fixed comment, submits.

## ACTIONABLE LEADS
- Disclosure steps: notify the KrishGoel and vikrant500 repository owners plus the university security or identity team through an established channel; rotate the account password, revoke active sessions, remove values from current files and git history, run repository secret scanning. Never use any exposed value against the service.
- GitHub governance: enable secret scanning and push protection, review forks and historical commits, and create a disclosure playbook covering passwords, session cookies, CSRF tokens, screenshots, logs, and downloaded HTML.
- Use DK10WS route names (Student/Academic/GetAttendanceSummaryList, dashboard, parent OTP, change-password) as an endpoint inventory to reconcile against the live portal during authorized review; treat the route existence as code-level map only.
- Review the vikrant500 clone tree (cookies.txt, hts-log.txt, Scripts, Home/Index.html) for additional downloaded browser state; treat all of it as sensitive historical material.
- Code-review targets from legacy wrappers: shell interpolation, CORS, regno-keyed cache isolation, CAPTCHA control boundaries, session expiry, logging of headers.
- Engineering actions for the Flutter client: platform secure storage, no long-lived password retention, short-lived refreshable sessions, centralized expiry, clear all cached headers on logout.

## FLAGS
- Credential and token values are redacted in the report; validity, account ownership, session binding, and expiry are unknown. Exposure is proven, exploitability is not.
- Repos are student projects, not university-owned; deployment and production build matching are unverified (explicitly unknown for the Flutter app).
- slcm.manipal.edu artifacts (App-Backend, slcmAPI, SLCM-api, SLCM-is-Dumb) are a different host and older ecosystem; reusing their routes against the Jaipur host would be an unsupported inference. SLCM-is-Dumb README even mentions CAPTCHA, and slcmAPI is archived/deprecated.
- Documentation drift: KrishGoel README says run main.py while the tree and cited source identify script.py; report flags it as maintenance, not a vulnerability.
- Several reference URLs use http:// (AddisionS, canaryGrapher, nikeplusdash) instead of https://; verify redirects before relying on the link form.
- The broader Manipal ecosystem (AttendanceSummaryList-style routes, .aspx paths in legacy code) is used only as comparison evidence; the report says it cannot verify the MUJ server stack.

## COVERAGE
- File: w2g-07-github-code-muj.md.
- 257 lines total; 48,461 bytes on disk; 48,321 chars read.
- Method: read_file offset 1, limit 2000, single call.
- EOF confirmed: final call returned truncated: false, last content line 257 equals total_lines 257.

---

## w2g-08-linkedin-sicm-devs.digest

## REPORT
Source file: w2g-08-linkedin-sicm-devs.md. Mapping public LinkedIn and institutional signals to SLCM and campus-portal engineering at MUJ. People-lead inventory with four evidence classes (direct SLCM, MUJ-local role, technology-adjacent, context only) and 43 numbered references.

## ANSWER SUMMARY
- Verdict: the public OSINT search found credible Manipal SLCM and campus-portal engineering leads, but no confirmed named builder or maintainer of mujslcm.jaipur.manipal.edu. Confidence: HIGH for ecosystem mapping, LOW for exact MUJ-host personnel attribution, LOW for the supplied stack as a verified public finding.
- Direct SLCM leads: Himanshu Upadhyay (Project Manager, MAHE Udupi; led and mentored the SLCM support-development team), Poornima Vishwaradhya (SAP SLcM configuration and implementation, Manipal Global Education Services), Zeeshan Khalandar (IT Manager MAHE Dubai; in-house apps and SLCM), Manju Muthamadhu (MAHE Dubai; SLCM application management plus ASP.NET MVC, ASP.NET Core, SQL Server skills). None of the four profiles names the Jaipur host.
- MUJ-local engineering leads: Nitin Agarwal, Sharma Rahul, DEVESH MEENA listed as Software Developer or Software Engineer at Manipal University Jaipur; Rakesh Sharma as IT Engineer with Active Directory, Windows Server, DNS, DHCP, VMware skills. Indexed rows contain no SLCM, portal, or stack language.
- Technology-adjacent leads: Rashmi Acharya (Software Developer, Manipal University Manipal; SQL, C++, ASP.NET, C) and Sumanth Suvarna (Dotnet Developer, MAHE Manipal; ASP.NET MVC, Web Forms, Web API, ADO.NET). Neither is publicly tied to the Jaipur host. Lavi Chauhan is flagged as a portal/".NET MVC" false positive (bank eKYC portal, Manipal Business Solutions).
- Public MUJ pages confirm: portal page at /Home/Index with title "Manipal University", "WELCOME TO MUJ PORTAL", Parent Login, and @muj.manipal.edu labels; FAQ tying SLCM registration to AMS login terminology; Office 365 SOP (v1.0, June 2025) documenting mail setup, sign-in, and MFA.
- Stack verification gap: meta description "User login example" and title only; no framework, server, or CDN version disclosed. ASP.NET MVC 5.3, .NET 4.x, IIS 10, and Akamai remain unverified by the reviewed sources.
- Platform context: a Salesforce press release (March 2026) announces MAHE-wide collaboration to modernize SLCM; it does not establish that the MUJ host is Salesforce-based or migrated.
- False-positive discipline: the token SLCM alone returns unrelated organizations (SLCM Pvt. Ltd., schools, childcare providers); three-way alignment of identity, employer/campus, and explicit SLCM language is required before escalating a candidate.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/Home/Index - public MUJ portal page; "Manipal University" title, "WELCOME TO MUJ PORTAL", Sign In, Parent Login, @muj.manipal.edu labels.
- https://muj.slcm.jaipur.manipal.edu/ - alternate shorter host form surfaced by public search; distinct hostname worth mapping.
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - SLCM registration FAQ; connects login support with AMS terminology.
- https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf - Office 365 SOP v1.0 June 2025; M365 mail identity and MFA documented for students and employees.
- https://in.linkedin.com/in/himanshuupadhyay - Project Manager at MAHE; explicitly led support-development team for the SLCM project.
- https://linkedin.com/in/poornima-vishwaradhya-a0b95b22 - SAP SLcM configuration, master data, implementation, testing, training lead.
- https://ae.linkedin.com/in/zeeshan-khalandar-865920136 - IT Manager MAHE Dubai; SLCM among in-house applications under his IT operations.
- https://linkedin.com/in/manju-muthamadhu - MAHE Dubai ERP and Applications; SLCM operations with ASP.NET MVC, ASP.NET Core, SQL Server skills; strongest combined signal.
- https://in.linkedin.com/in/nitin-agarwal-aa9549209 - Software Developer at MUJ Jaipur; institutional validation candidate, no SLCM wording.
- https://in.linkedin.com/in/sharma-rahul-929b06218 - Software Engineer at MUJ Jaipur; validation candidate.
- https://linkedin.com/in/devesh-meena-a1a37a377 - Software Engineer at MUJ Jaipur; validation candidate.
- https://linkedin.com/in/rakesh-sharma-76890172 - IT Engineer at MUJ Jaipur; Windows/AD/VMware infrastructure adjacency.
- https://linkedin.com/in/rashmi-acharya-54900528 - historical Manipal software developer; ASP.NET, SQL, C++, C.
- https://linkedin.com/in/sumanth-suvarna-212738199 - Dotnet Developer MAHE Manipal; headline lists ASP.NET MVC, Web Forms, Web API, ADO.NET.
- http://salesforce.com/in/news/press-releases/2026/03/26/manipal-university-ai-transformation - Salesforce-MAHE SLCM modernization announcement; MAHE-wide, not MUJ-host evidence.

## ACTIONABLE LEADS
- Build an asset-and-owner matrix: public service URL, institutionally confirmed owner, application/identity/CDN/hosting dependencies, evidence date, confidence. Put LinkedIn names in a candidate-contact column only, never an owner column without institutional confirmation.
- Take the confidence-ranked lead register (Upadhyay, Vishwaradhya, Khalandar, Muthamadhu, then MUJ-local: Agarwal, Rahul, Meena, Sharma; technology: Acharya, Suvarna) to an authorized MUJ or MAHE system owner for confirmation of service, application, identity, CDN owners, and change-control process.
- Terminology normalization: map SLCM, SLcM, Student Life Cycle Management, AMS, portal, ERP, admission life cycle, LMS to distinct services; do not assume one application.
- Turn Manju Muthamadhu's public operations vocabulary (development, configuration, code review, UAT, production movement, monitoring) into authorized owner-interview questions about change approval, UAT records, backup/restore tests, and owner separation.
- Institutional context sources: http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf states SLCM replaced the older Academic Management System; verify the Jaipur instance history through authorized records.
- Track the Salesforce MAHE modernization announcement for migration signals, but do not probe the public login service; disclosure questions go through MUJ IT or published channels.

## FLAGS
- No profile names the Jaipur host; every maintainership inference is explicitly unsupported by the report itself. Treat all people as ecosystem leads for authorized validation.
- Reference list contains multiple same-name records (several Himanshu Upadhyay, Rakesh Sharma, Nitin Sharma, Rahul Sharma variants incl. a Red Hat SRE, a Manhattan consultant, a Pens.com director, an MIT student). URL-suffix disambiguation is required; conflation risk is high.
- Two distinct Sumanth Suvarna profile URLs are cited (212738199 and 767a82171); identity equivalence is unverified.
- Salesforce announcement is MAHE-wide; citing it as MUJ-host platform evidence would overclaim.
- The "User login example" meta description on the live portal page is a generic-template artifact, not a framework fingerprint.
- LinkedIn index snapshots may be stale; a role at an institution does not prove current access or responsibility. The report publishes no personal contact data.
- One search-derived item (Software Development Centre at MUJ, "[534 search result]") lacks a stable URL; reproducibility limited.

## COVERAGE
- File: w2g-08-linkedin-sicm-devs.md.
- 262 lines total; 41,143 bytes on disk; 41,113 chars read.
- Method: read_file offset 1, limit 2000, single call.
- EOF confirmed: final call returned truncated: false, last content line 262 equals total_lines 262.

---

## w2g-09-job-postings.digest

## REPORT
Source file: w2g-09-job-postings.md. Job-board OSINT across LinkedIn, Naukri, Indeed, plus official MUJ and MAHE career pages, looking for postings that bind MUJ to SLCM, Manipal ERP, or student-portal maintenance. Bounded negative finding dated 2026-08-25.

## ANSWER SUMMARY
- Verdict: no direct, publicly indexed MUJ job posting explicitly mentions SLCM, Manipal ERP, student-portal maintenance, ASP.NET MVC, SQL Server, IIS, Microsoft 365 identity, a portal-operations team, or a vendor. Confidence Moderate for the bounded negative; low for any architecture or vendor claim.
- Strongest Naukri MUJ results are a Library Assistant listing (library management, record keeping, library software, MS Office) and a Lab Technician/Instructor - 3D Lab listing (3D CAD, DFAM, 3D printing). Neither mentions SLCM or the requested stack; neither supports a "technical SLCM role" reading.
- Official MUJ careers page (career-community.php) groups vacancies into academic, research, and non-academic categories and names schools and Quality and Compliance functions; no portal-operations or technical support role visible.
- Indeed results are keyword/location search pages populated with unrelated employers (Foxoso Hospitality, Selenite Organisation, ATHARVA ORGANISATION, real-estate sales roles). A query term is not employer attribution.
- LinkedIn public queries returned zero MUJ jobs in the United States for the "Manipal University Jaipur" query; treated as no-confirmation only, because results are location-, login-, and personalization-dependent.
- Entity-separation findings: Sikkim Manipal University (Majhitar), Manipal Technologies (Udupi), Manipal Dot Net, MAHE, and Manipal Dubai all appear in the corpus; none substitutes for MUJ SLCM evidence.
- Stack matrix: every requested field (ASP.NET MVC, .NET Framework 4.x, SQL Server, IIS, M365 identity, Manipal ERP, vendor, team) is rated "not publicly stated" in reviewed postings. Only the portal name "WELCOME TO MUJ PORTAL" is publicly confirmed.
- Recommended follow-up is a periodic targeted watch of the official MUJ careers page and the Naukri MUJ company page using role families such as application support, enterprise applications, MIS, systems administrator, and software developer.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/ - live portal; confirms "WELCOME TO MUJ PORTAL" and sign-in/parent-login labels only.
- https://jaipur.manipal.edu/career-community.php - official MUJ vacancy index; academic, research, non-academic categories; no stack disclosure.
- https://www.naukri.com/manipal-university-jobs-in-jaipur - Naukri MUJ Jaipur search page; visible MUJ roles are Library Assistant and 3D Lab Instructor.
- https://www.naukri.com/job-listings-library-manipal-university-jaipur-jaipur-0-to-5-years-040826029330 - Library Assistant posting; B.L.I.S/M.L.I.S, library software, MS Office; no SLCM or stack.
- https://www.naukri.com/manipal-university-jaipur-jobs-careers-4408504 - Naukri MUJ company page; two jobs listed including the 3D Lab role.
- https://in.indeed.com/q-manipal-university%2C-jaipur-l-jaipur%2C-rajasthan-jobs.html - Indeed keyword page; results are unrelated employers and sales/management roles.
- https://in.indeed.com/q-manipal-university%2C-jaipur-l-jaipur%2C-rajasthan-jobs.html?start=10 - second Indeed results page; a real-estate Associate role visible, no MUJ SLCM evidence.
- https://in.indeed.com/jobs?q=Manipal+University+Jaipur - general Indeed query page; discovery only.
- https://www.linkedin.com/jobs/search/?keywords=Manipal%20University%20Jaipur - LinkedIn public query; zero jobs in the United States for MUJ.
- https://www.linkedin.com/jobs/search/?keywords=Manipal%20University%20IT - broader LinkedIn query; mixed search context, no direct MUJ technical posting.
- https://www.linkedin.com/company/manipal-university-jaipur/ - MUJ company page inspected; no SLCM vacancy extracted.
- https://www.manipal.edu/mu/important-links/careers-mu/jobs-at-mahe-current-vacancies-.html - MAHE vacancy index; faculty/research/non-academic categories; MAHE, not MUJ.
- https://www.manipal.edu/mu/academics/student-portal.html - MAHE student-portal page; portal context for another Manipal entity.
- https://jaipur.manipal.edu/career-veiw.php?url=77%2Fapplications-now-open-for-faculty - TAPMI School of Business faculty posting; MUJ but non-technical.
- https://web.manipal.net/mdn/careers/currentOpenings/applyforjob.php - Manipal Dot Net Pvt Ltd careers; corporate Manipal entity excluded as vendor evidence.

## ACTIONABLE LEADS
- Set up a dated-snapshot watch: periodically capture jaipur.manipal.edu/career-community.php plus the Naukri MUJ company page and check for role families application support, enterprise applications, MIS, systems administrator, software developer.
- When a positive lead appears, preserve the direct posting URL with employer, location, date, and full description; enter the evidence table only when the posting names MUJ and the relevant system or duties.
- Request official confirmation from MUJ of the system owner, support contact, application stack (authorized documentation or procurement records), database, identity integration, CDN, and vendor; the job corpus cannot answer any of these.
- Search public procurement or tender notices for a vendor relationship; the report explicitly suggests this as the safe channel.
- Treat the portal as visible-surface-only evidence: banner and login labels confirm identity, not framework; do not convert the supplied stack into independent fact.

## FLAGS
- The finding is "not found in the public corpus reviewed as of 2026-08-25", not proof of nonexistence; the report itself warns that boards are dynamic, incompletely indexed, and location/login dependent.
- LinkedIn results are US-location bound in the cited pages; zero US jobs do not cover India-based listings, internal postings, or recruiter-only roles.
- The Library Assistant's "library software" and "MS Office" must not be read as Microsoft 365 identity or SLCM access; the report explicitly blocks that inference.
- Naukri page counts (e.g. 12,277 "Manipal University" vacancies) are brand-aggregate search counts across Sikkim Manipal, Manipal Technologies, and others, not MUJ technical vacancy counts.
- The L&D Executive reference is expired or search-context only; do not treat it as an active MUJ role.
- Reference table repeats citation numbers ([12] twice, [18] three times, [16] twice) in one row each, which hints at extracted search output; the underlying URLs are consistent and were verified against the body text.
- All stack items remain sourced only from the externally supplied brief; this report must not be cited as stack evidence.

## COVERAGE
- File: w2g-09-job-postings.md.
- 174 lines total; 25,798 bytes on disk; 25,696 chars read.
- Method: read_file offset 1, limit 2000, single call.
- EOF confirmed: final call returned truncated: false, last content line 174 equals total_lines 174.

---

## w2g-10-stackoverflow.digest

## REPORT
Source file: w2g-10-stackoverflow.md. Stack Overflow exposure assessment for the MUJ SLCM ecosystem using the public Stack Exchange API (search/advanced, questions, answers endpoints) with literal-body validation. 28 references, all public API or question/answer pages.

## ANSWER SUMMARY
- Verdict: no direct MUJ SLCM Stack Overflow disclosure was verified in the inspected public corpus. Exact `mujslcm` search returned no question records; the hostname mujslcm.jaipur.manipal.edu appears in no retrieved title, body, image source, route, callback, or connection string.
- The two literal `slcm` matches are token collisions, not MUJ evidence: question 77021984 is a MongoDB/Mongoose aggregation question with identifiers getQCResultSLcmExcel and isSLCMQcInspection; question 53239398 is a MarkLogic error trace with a $slcm variable beside $slch and $slchr.
- Three verified Manipal ASP.NET questions: 17420085 (ASPX tabs, external image http://eduvark.com/images/Manipal-University-Application-Form.jpg, local jQuery asset paths), and 19374708 plus 19510663 (C#/ASP.NET SMTP samples with a Manipal-related Gmail sender and an "MCIS,Manipal" signature).
- SMTP sample artifacts: smtp.gmail.com, ports 587 (question 19374708) and 584 versus 587 (question 19510663), EnableSsl true, UseDefaultCredentials false, NetworkCredential construction, a connection string Data Source=BOPSERVER; Initial Catalog=Project, and a TrackingFaculty_det update keyed by FID.
- No web.config block, Microsoft 365 identity configuration, Akamai control, IIS setting, or target-host route appears in any inspected record; the supplied ASP.NET MVC 5.3 / .NET 4.x / IIS 10 / Akamai / M365 stack is not corroborated by Stack Overflow.
- The answer corpus (IDs 19375158, 19374980, 19515503, 19510816, plus 17420085 answers) adds only generic guidance: SmtpException classes, GridView iteration, async send helpers, jQuery UI and AjaxControlToolkit tabs. No answer adds a MUJ artifact.
- Confidence: High for classification of the inspected records; Moderate that the Manipal ASP.NET cluster is generic rather than MUJ-specific; Low for any global-absence claim about the public Internet, deleted posts, or private content.
- Recommended label: direct MUJ SLCM linkage not observed in inspected corpus; generic Manipal/.NET references verified; live-service impact not established.

## KEY FACTS
- https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q=mujslcm&site=stackoverflow&filter=withbody&pagesize=100 - zero literal matches; the strongest negative result in the report.
- https://stackoverflow.com/questions/17420085/creating-tabs-in-aspx-for-application-forms - ASPX tab question; only verified question with a Manipal-branded external image.
- https://stackoverflow.com/questions/19374708/exception-handling-while-send-a-mail-using-smtp-port - SMTP sample with Manipal sender, MCIS,Manipal signature, Gmail host, BOPSERVER connection string.
- https://stackoverflow.com/questions/19510663/try-catch-block-used-while-smtp-exception-need-to-display-an-error-message-in-th - repeated SMTP sample; port shown as 584 in question code and 587 in answer code.
- http://eduvark.com/images/Manipal-University-Application-Form.jpg - third-party illustrative image URL inside question 17420085; contextual, not MUJ-host evidence.
- https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q=slcm&site=stackoverflow&filter=withbody - returns the MongoDB (77021984) and MarkLogic (53239398) collisions.
- https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q=manipal&tagged=asp.net&site=stackoverflow&filter=withbody&pagesize=100 - the query that produced the three verified Manipal questions.
- https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q=manipal&tagged=asp.net-mvc&site=stackoverflow&filter=withbody&pagesize=100 - empty for the requested literal; no MVC-specific Manipal match.
- https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q=manipal&tagged=.net&site=stackoverflow&filter=withbody&pagesize=100 - no literal proper-name match after validation.
- https://api.stackexchange.com/2.3/questions/17420085;19374708;19510663;17353152?site=stackoverflow&filter=withbody - question-bodies endpoint for the candidate set (17353152 is the unrelated Node.js Twitter thread).
- https://api.stackexchange.com/2.3/questions/17420085;19374708;19510663;17353152/answers?order=desc&sort=votes&site=stackoverflow&filter=withbody&pagesize=100 - answer corpus; no target artifact added.
- https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q=manipal&tagged=iis&site=stackoverflow&filter=withbody&pagesize=100 - no literal match; no IIS evidence.
- https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q=manipal&tagged=web-config&site=stackoverflow&filter=withbody&pagesize=100 - no match; no web.config artifact anywhere in the inspected set.
- https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q=manipal&tagged=asp.net-identity&site=stackoverflow&filter=withbody&pagesize=100 - no match; no identity configuration evidence.
- http://www.asp.net/ajaxlibrary/ajaxcontroltoolkitsamplesite/tabs/tabs.aspx - ASP.NET AJAX sample link in a 17420085 answer; documentation URL, not an application endpoint.

## ACTIONABLE LEADS
- Preserve a reproducible evidence ledger per item: exact URL, query scope, retrieval date, question ID, answer IDs, matching literal, classification; record text-match confidence separately from ownership confidence.
- Code-hygiene review targets: the two SMTP posts (Gmail host, ports, NetworkCredential construction, BOPSERVER/Project connection string, TrackingFaculty_det/FID data flow). If an authorized owner identifies the source, check git history for committed secrets, rotate any real credentials, move SMTP settings to secret-backed config.
- Report the port discrepancy 584 versus 587 to the code owner as a configuration-verification cue; do not treat either public value as the live setting.
- Keep question 17420085 as a contextual reference only (image URL and local jQuery paths are client-side samples, not deployed routes).
- Education value: use the corpus as a secure-coding case study on overreading brand names; require two independent anchors (target-owned domain or organization name plus application/technology signal) before escalation.
- Owner notification path: contact through an authorized channel only; do not attempt SMTP authentication, database connection, or live probing.

## FLAGS
- Attribution is the open question: no inspected record proves the Manipal-related code belongs to MUJ SLCM; the two SMTP posts may be related, copied, or coincidental. The report calls this an inference boundary.
- Collision question IDs 77021984 and 53239398 appear without direct question URLs in the reference list; their evidence URL is the API search, so reproduction goes through the API, not a stable direct link.
- The Manipal-related Gmail address is deliberately redacted in the report prose; the full identifier exists only in the source posts. Do not reproduce it in downstream material.
- The 584 versus 587 port difference may be a transcription error, an answer correction, or an extraction artifact; the report explicitly refuses to treat it as a vulnerability.
- The Node.js question 17353152 (Twitter streaming with track:'manipal') is retained only as a search-control example and is not .NET evidence.
- Supplied stack claims stay uncorroborated: no MVC version, framework target, IIS setting, Akamai header, OAuth callback, or web.config section appears in the corpus.
- This report does not state its research run date (unlike w2g-09 and w2g-11); all negatives are corpus- and search-time-bound.

## COVERAGE
- File: w2g-10-stackoverflow.md.
- 244 lines total; 38,900 bytes on disk; 38,900 chars read.
- Method: read_file offset 1, limit 2000, single call.
- EOF confirmed: final call returned truncated: false, last content line 244 equals total_lines 244.

---

## w2g-11-npm-pypi.digest

## REPORT
Source file: w2g-11-npm-pypi.md. Public package-registry and source-ecosystem assessment for the MUJ SLCM vocabulary (Manipal, MUJ, SLCM, mujslcm) across npm, PyPI, crates.io, RubyGems, NuGet, Maven Central, pub.dev, and GitHub, research date 2026-08-25. 50 references.

## ANSWER SUMMARY
- Verdict: no directly named MUJ SLCM package was found in the tested public npm, PyPI, crates.io, RubyGems, NuGet, Maven, or pub.dev searches as of 2026-08-25. The only clear published SLCM utility is npm `yemit`, which is MIT Manipal, not MUJ Jaipur.
- `yemit` (v0.1.5, author Rohit Sarkar): attendance utility for MIT Manipal SLCM, CLI binary, dependencies casperjs, cli-table, underscore; repository caveat says the utility can break if SLCM is down or the site is modified. Useful supply-chain comparator, not a MUJ artifact.
- MUJ-specific footprint sits in source and distribution channels, not registries: SlcmPlus Chrome extension (Manifest V3, version 1.1, content-script matches for MUJ SLCM attendance and marks pages; Chrome Web Store listing unconfirmed), krishgoel/slcm-feedback-automation (python-dotenv==1.0.1, selenium==4.20.0), DK10WS/SLCM_APP (Flutter frontend, FastAPI backend, APK and web-app release paths), MUJ-Central, SlcmAndLms-aggregator, plus public demos slcm-client-unoff.vercel.app and geervan.github.io/sample.
- npm registry API for `mujslcm` returned an explicit zero-object response; PyPI pages for `mujslcm` and `slcm` show no matching listings; collisions such as `muj-input`, `@mujo/plugins`, and the npm package named `manipal` ("this is my first module") were excluded as non-evidence.
- PyPI `manipal` search surfaces mit-cod, a "Course Outcome Digitizer for MIT, Manipal" course-outcome tool; relevant to MIT Manipal only, excluded from MUJ evidence.
- Feedback automation is a recurring category: vocarista/slcm_feedback_automation is a second public SLCM feedback script; automated submission changes institutional records, so authorization, user confirmation, rate limits, auditability, and rollback procedures matter.
- Unofficial API/scraper cluster (tejaskash/slcm-api Flask, canaryGrapher/slcmAPI, manipalthetalk/App-Backend Python 2.7 + Go, nikeplusdash/SLCM-api) targets the broader Manipal SLCM and would concentrate credentials if deployed as intermediaries. sankalp2004/SLCM-is-Dumb is recorded as a high-sensitivity CAPTCHA-automation artifact without operational detail.
- Confidence: High for the observed search results; moderate for the broader absence claim. No evidence proves compromise, unauthorized access, or vulnerability in the MUJ SLCM service.

## KEY FACTS
- https://registry.npmjs.org/-/v1/search?text=mujslcm&size=250 - explicit zero-object, total 0 response; the anchor negative for npm.
- https://www.npmjs.com/package/yemit - the only clear published SLCM utility; MIT Manipal, not MUJ.
- https://registry.npmjs.org/yemit - registry metadata: v0.1.5, Rohit Sarkar, casperjs/cli-table/underscore dependencies.
- https://github.com/rsarky/yemit - source repo; warning that SLCM changes or downtime break the utility.
- https://pypi.org/search/?q=mujslcm - no matching project listings.
- https://pypi.org/search/?q=slcm - no matching project listings.
- https://pypi.org/project/mit-cod/ - Course Outcome Digitizer for MIT, Manipal; retained as related-but-excluded.
- https://github.com/Tejas-Narula/SlcmPlus - MUJ-specific Chrome extension repository.
- https://raw.githubusercontent.com/Tejas-Narula/SlcmPlus/main/manifest.json - Manifest V3, version 1.1, content-script matches on MUJ SLCM academic pages.
- https://github.com/Tejas-Narula/SlcmPlus/releases - releases page found; Chrome Web Store publication not confirmed.
- https://github.com/krishgoel/slcm-feedback-automation - MUJ SLCM semester-end feedback automation; MIT license, 3 stars, 6 forks, visible .env.example.
- https://raw.githubusercontent.com/krishgoel/slcm-feedback-automation/main/requirements.txt - python-dotenv==1.0.1 and selenium==4.20.0 pinned.
- https://github.com/DK10WS/SLCM_APP - Flutter and FastAPI mobile application for MUJ SLCM; README points to Android APK and a web-app path.
- https://slcm-client-unoff.vercel.app/ - public web demo: "SLCM Mobile Client for Attendance, Timetable & Grades at Manipal University Jaipur".
- https://github.com/madhav-manchanda/SlcmAndLms-aggregator - dashboard combining MUJ SLCM and LMS data; full-stack source project.

## ACTIONABLE LEADS
- Maintain separate supply-chain inventories per channel: registry packages, GitHub source, browser extensions, APKs, and deployed demos; record exact URL, commit or release identifier, version, maintainer, license, dependencies, collection date.
- For SlcmPlus: verify whether any distributed build matches the GitHub source byte-for-byte, inspect the full manifest permissions offline, enumerate external network destinations; check the store manually without installing or signing in.
- For DK10WS/SLCM_APP: validate release provenance, APK signing, backend ownership, and whether the web-app path is still controlled by the same maintainers.
- For krishgoel and vocarista feedback scripts: in an authorized lab only, review credential handling, logging, debug output, cookies, tokens, HTTP destinations, and secret persistence using synthetic accounts and a mock service; never submit real student credentials to third-party code.
- For the API/scraper cluster: treat each as a separate data processor; require ownership, retention, and incident-contact clarity before any institutional use; prefer read-only, locally executed, source-auditable tools.
- Registry monitoring: repeat periodic exact-term searches (npm, PyPI, crates, pub.dev) and also search repository manifests and metadata, since source-only projects never surface as packages.
- Responsible disclosure: on a real vulnerability, preserve minimum evidence, redact credentials and personal identifiers, notify the owner and MUJ through official channels, follow university rules.

## FLAGS
- All negative registry results are bounded: private, deleted, unindexed, renamed, or future packages are outside the conclusion, and embedded dependencies in source-only projects are invisible to lexical searches.
- `yemit` and `mit-cod` are MIT Manipal artifacts; citing either as MUJ supply-chain evidence overclaims. Entity resolution: "Manipal" alone never identifies the Jaipur campus.
- SlcmPlus store publication, current maintenance, and safety are unconfirmed; content-script URL matches prove page targeting, nothing about distribution.
- DK10WS/SLCM_APP source may not match distributed binaries; README release claims were not independently validated.
- The report explicitly makes no maliciousness determination for any listed project; all security statements about credential handling are labeled risk inferences.
- Two GitHub reference URLs use http:// (Anushkakumar10/muj_slcm, canaryGrapher/slcmAPI); harmless but inconsistent with the https corpus.
- Findings are time-bound to 2026-08-25 registry state.

## COVERAGE
- File: w2g-11-npm-pypi.md.
- 190 lines total; 33,803 bytes on disk; 33,740 chars read.
- Method: read_file offset 1, limit 2000, single call.
- EOF confirmed: final call returned truncated: false, last content line 190 equals total_lines 190.

---

## w2g-12-google-dorks.digest

## REPORT
Source file: w2g-12-google-dorks.md. Passive public-indexing and search-dork assessment for the MUJ SLCM ecosystem. Search-engine discovery only; no authentication, credential testing, route enumeration, or vulnerability scanning. 23 references.

## ANSWER SUMMARY
- Verdict: informational OSINT finding. No confirmed public student-record exposure in observed first-party results. Confidence: High for observed search-result classifications, Moderate for negative findings, Low for unverified stack claims.
- Indexed surfaces: mujslcm.jaipur.manipal.edu (title "muj portal - Manipal University", "WELCOME TO MUJ PORTAL", Sign In Student/Parent Login) and /Home/Index (login-oriented, "Forgot Password?").
- Official linkage: the SLCM FAQ and the official payment page (pay-fee-online.php) both identify the SLCM root as the student portal; the annual-fee notice is dated June 24, 2025 with July 18, 2025 as the 2025-26 payment deadline.
- Register-number, marks, and student-list dorks produced no confirmed first-party student-specific marksheet or register-number file; the report uses the wording "no confirmed hit observed," not proof of absence.
- XLSX dorks: no confirmed MUJ-hosted XLSX workbook. Results with .xlsx titles resolve to .pdf URLs (e.g. List of Patent Status_01.04.2024.pdf); cross-scope hits (cia.manipal.edu TOX STAT workbook, a GitHub call-centre workbook) were excluded.
- Privacy lead: a third-party Scribd result claims to contain student registration numbers, emails, genders, departments, names, and degrees. Not treated as MUJ-domain evidence, not to be downloaded, copied, or redistributed.
- Technology claims (ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai, M365) are unverified by indexed pages; /Home/Index is MVC-shaped only as an inference. Technology dorks returned generic vendor documentation.
- Hostname hygiene: muj.slcm.jaipur.manipal.edu and slcm.manipal.edu (MAHE footer) must not be merged with the target without owner confirmation.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/ - indexed root; page titled "muj portal - Manipal University" with sign-in and parent/student login labels.
- https://mujslcm.jaipur.manipal.edu/Home/Index - indexed public login route; "Forgot Password?" visible.
- https://muj.slcm.jaipur.manipal.edu/ - alternate MUJ-looking host with similar sign-in text; canonical ownership unconfirmed.
- https://slcm.manipal.edu/ - "MU SLcM" page with MAHE, Manipal footer; cross-institutional false positive.
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - official FAQ; strongest official link between the university site and the SLCM registration URL.
- https://jaipur.manipal.edu/pay-fee-online.php - payment page that explicitly identifies the SLCM root as the student portal.
- https://jaipur.manipal.edu/img/pdf/Notification_Annual-Fee-Payment-AY-2025-26.pdf - fee notice; June 24, 2025 date, July 18, 2025 deadline for AY 2025-26.
- https://jaipur.manipal.edu/fee-structure.php - public course-fee page with school and department links; intended public data.
- https://jaipur.manipal.edu/examination.php - public description of assessment components; policy, not a marksheet.
- https://www.jaipur.manipal.edu/administration-registrar.php - official registrar page; no student-specific list observed.
- https://jaipur.manipal.edu/img/pdf/research/muj/List%20of%20Patent%20Status_01.04.2024.pdf - .xlsx search title with a .pdf URL; file-type mismatch example.
- https://cia.manipal.edu/content/dam/manipal/mu/kmc-manipal/Documents/TOX%20STAT%20whole%20year.xlsx - real XLSX URL but KMC Manipal scope, not MUJ SLCM.
- https://github.com/Nikhilshetty1/Manipal-call-centre-analysis/blob/master/final_revenue.xlsx - third-party-hosted workbook; not an official MUJ artifact.
- https://www.scribd.com/document/881889937/Eligible-Students-MUJ-1 - third-party claim of student registration data; unverified privacy lead, not first-party evidence.
- https://www.getmyuni.com/college/manipal-university-jaipur-result?page=result - third-party result page claiming MUJ results; secondary description, not a marksheet URL.

## ACTIONABLE LEADS
- Owner-side review: MUJ web and identity teams should check Search Console and server logs for the root host, alternate host, /Home/Index, FAQ PDF, fee documents, and document directories; confirm whether any authenticated response was ever cached or indexed.
- Document owners: inspect PDF, XLSX, CSV, DOCX, and image repositories for names, registration numbers, emails, marks, fee receipts, attendance, or student identifiers; confirm actual file type and contents, not titles; use the approved takedown process for stale copies.
- Application owners: minimize login-page disclosure, make password recovery non-enumerating, and prevent authenticated pages from caching as public content; these belong in an authorized test plan.
- The team practice: keep a dated log of query, result title, exact URL, classification; redact all personal data; share only URLs, timestamps, query strings, and redacted screenshots with the university's authorized security contact.
- Disclosure split: first-party evidence (FAQ, payment page) vs third-party leads (Scribd items); report the Scribd material privately as an unverified lead, never redistribute content.
- Ask MUJ to confirm canonical ownership and redirect policy for the two similar hostnames.

## FLAGS
- All negatives are search-time, location-, and account-state-bound; "no confirmed hit observed" is deliberate wording, not proof of absence.
- The Scribd student-data claims are third-party and unverified; opening, copying, or redistributing them is explicitly discouraged; they establish nothing about MUJ publication.
- Search titles can embed original spreadsheet names while URLs end in .pdf; always validate file type by URL and content type.
- Alternate and MAHE hostnames are not confirmed equivalent to the target; merging them into one asset is unsupported.
- The stack and identity claims stay unverified; /Home/Index only supports an MVC-style inference from URL shape.
- The report notes noindex is not a substitute for authorization; indexing of an entry point is not an authorization failure.
- One reference (Statute-MUJ.pdf under muj.onlinemanipal.com, http) appears in the list without body discussion; low relevance.

## COVERAGE
- File: w2g-12-google-dorks.md.
- 185 lines total; 32,175 bytes on disk; 32,175 chars read.
- Method: read_file offset 1, limit 2000, single call.
- EOF confirmed: final call returned truncated: false, last content line 185 equals total_lines 185.

---

## w2g-13-telegram-discord.digest

## REPORT
Source file: w2g-13-telegram-discord.md. Public community risk map for MUJ SLCM and adjacent LMS: Telegram, Discord, Reddit, official MUJ pages, and general threat-intelligence context. Public-only review; no joining groups, no portal authentication, no credential testing. 25 references.

## ANSWER SUMMARY
- Verdict: Moderate confidence for the public ecosystem map; High that public MUJ-branded community listings and isolated public SLCM problem reports exist; Low for any leak, credential-sharing, compromise, or stack-attribution conclusion.
- Telegram: direct page for @manipaljaipurfresher shows "Manipal University Jaipur", a "MUJ Freshers group", 447 members and 7 online; a Telemetrio page for the apparent same handle shows 1,572 subscribers and a restricted-by-Telegram status. Counts are treated as time- and source-dependent; the report refuses to average or reconcile them.
- Discord: invite 7a5D7KKNFf shows "Manipal Jaipur" with 1,142 members and 27 online; invite manipal-university-jaipur-1008377907057545269 shows "Manipal University Jaipur" with 1,902 members and 32 online and an official-sounding listing title; discord.do describes a student-made community with department-wise study channels, voice channels, a cafeteria, fun zone, and peer discussion. No university endorsement is confirmed for any server.
- Portal friction: two deleted-author Reddit posts: r/Manipal_Academics "Slcm login" (old and new registration numbers both rejected after an intra-sliding update) and r/manipaljaipur "Slcm portal issue" (password error despite the poster believing it correct). Archived posts, no verified resolution.
- Official support path: the SLCM FAQ directs AMS login trouble to re-verify credentials then contact institutional DMS or AMS support, with a separate Outlook-account troubleshooting path. The FAQ's credential-format example is deliberately omitted by the report.
- Leak status: "not located in the reviewed public corpus" for leaked SLCM screenshots, credential dumps, or credential-sharing conversations. The urlscan "Live Screenshot" is a scanner interface feature, not leak evidence; urlscan states it does not manage the displayed sites.
- Stack claims (ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai, M365) remain unverified requester-supplied hypotheses; the FAQ's Outlook references provide context only.
- General infostealer and identity-risk sources (flare.io, Constella, Have I Been Pwned) explain threat mechanisms but attribute nothing to MUJ.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/ - public portal page; sign-in and parent-login options with an @muj.manipal.edu label.
- https://muj.slcm.jaipur.manipal.edu/ - alternate public rendering with an @jaipur.manipal.edu identity label.
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - official FAQ: registration link, AMS login re-verify step, DMS or AMS support, separate Outlook troubleshooting path.
- https://t.me/manipaljaipurfresher - direct Telegram landing page; MUJ Freshers group, 447 members, 7 online.
- https://telemetr.io/en/channels/1394408318-manipaljaipurfresher - Telemetrio directory for the same apparent handle; 1,572 subscribers, channel restricted by Telegram; visible rows are welcome/general topics.
- https://discord.com/invite/7a5D7KKNFf - public invite page; "Manipal Jaipur", 1,142 members, 27 online.
- https://discord.com/invite/manipal-university-jaipur-1008377907057545269 - public invite page; "Manipal University Jaipur", 1,902 members, 32 online.
- https://discord.do/manipal-university-jaipur/ - directory description: student-made community, study and voice channels, peer discussion.
- https://www.reddit.com/r/Manipal_Academics/comments/1993mdc/slcm_login - archived post, deleted author; old and new registration numbers rejected after an intra-sliding update.
- https://www.reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue - deleted-author report of a password error despite believed-correct password.
- https://urlscan.io/domain/mujslcm.jaipur.manipal.edu - passive scan page; scanner metadata only, disclaims management of displayed sites.
- https://muj.onlinemanipal.com/ - Online Manipal LMS description (e-tutorials, virtual labs, e-libraries); adjacent service context, not proof of shared backend.
- https://www.d2l.com/en-in/why-d2l/customers/manipal-university-jaipur-online - D2L customer page naming MUJ Online as an LMS context.
- http://flare.io/flare-data-explorer/stealer-logs - general infostealer capability (credentials, session cookies, screenshots); threat model, not MUJ evidence.
- http://haveibeenpwned.com/API/v3 - general breach/stealer-log context; no MUJ-specific record cited.

## ACTIONABLE LEADS
- Governance confirmation: ask community administrators for public moderation and reporting statements; publish an official recognized-channel directory and a policy that all other groups are independent unless confirmed.
- Anti-phishing messaging: state across SLCM, Outlook onboarding, LMS pages, and official social accounts that staff never need passwords, OTPs, cookies, or private screenshots; provide a report address and push official password-reset flows.
- Registration-change messaging: give students a controlled status message naming the active identifier, expected synchronization timing, and the owning official unit (triggered by the reg-number rejection report).
- Incident-validation protocol for future leak claims: preserve public URL, timestamp, channel name, redacted description; escalate to university security and legal contacts; ask platforms to preserve or remove material; publish only confirmed facts.
- Evidence ledger discipline: record source type, timestamp, confidence, redaction status; do not merge divergent Telegram counts or the two Discord invite counts.
- Passive surface check: the urlscan domain page can be reviewed for scan history and subdomain results as an authorized passive step only.
- Direct support routing: point students to FAQ DMS/AMS escalation instead of crowdsourced password exchange.

## FLAGS
- Membership counts diverge across sources (447 direct vs 1,572 directory; a nearGroups entry shows 3,903 members and 55 online without a matching handle). The report explicitly forbids averaging or assuming identity; the nearGroups entry is not used as a third count.
- The two Discord invite pages may be different servers or overlapping communities; nothing proves they are the same object, so counts are not added.
- Reddit posts are deleted-author, archived user reports; they prove reports, not systemic outage, password validity, or compromise.
- "Official Public Listed Community of MUJ Students" is a self-description; no MUJ institutional page confirms sponsorship or operation.
- The urlscan screenshot feature is scanner UI; the page itself says displayed websites are not managed by urlscan. Treating it as a leaked screenshot would be a category error.
- The FAQ's credential-related example and Outlook identity reference are omitted from the report; do not reconstruct or reproduce them.
- Infostealer, Constella, and HIBP material is general context with no MUJ attribution; a public leak claim would still need provenance, date, affected service, and institutional validation.
- The supplied technical stack remains requester-supplied hypothesis; no verified version, CDN, or identity architecture appears in the reviewed evidence.

## COVERAGE
- File: w2g-13-telegram-discord.md.
- 334 lines total; 52,591 bytes on disk; 52,583 chars read.
- Method: read_file offset 1, limit 2000, single call.
- EOF confirmed: final call returned truncated: false, last content line 334 equals total_lines 334.

---

## w2g-14-wayback-family.digest

## REPORT
Source file: w2g-14-wayback-family.md. Archive evidence and codebase evolution study for the Manipal SLCM ecosystem: Wayback CDX queries, archived replays, current public pages, official FAQ, MAHE student-portal page, a public header observation, and Microsoft OpenID metadata. Evidence labels: Observed, Strong inference, Working inference, Unknown. 29 references.

## ANSWER SUMMARY
- Verdict: Medium-high confidence for the historical surface and the current public technology fingerprint; medium for the migration narrative; low-to-medium for removed pages, direct Microsoft SSO, and Akamai. The public ecosystem shows at least two implementation eras.
- Legacy host slcm.manipal.edu (2017-2026 corpus): .aspx route vocabulary including loginForm.aspx, StudentChangePassword.aspx, ParentChangePassword.aspx, Academicdashboard.aspx, ClassAttendance.aspx, CourseFeedback.aspx, CreateTimeTable.aspx, GradeSheet.aspx, Pre-Registration.aspx, Results.aspx, mostly with 302/303 records; MicrosoftAjax Web Forms assets (Jan 2019); Bootstrap and jQuery 2.0.3 assets (Apr 2018); later Print.aspx and PaymentResponse.aspx captures (query values omitted).
- MUJ host mujslcm.jaipur.manipal.edu (2025+): public login shell only. Home/Index captured 10 Jan 2025, root captured 27 May 2025 with "WELCOME TO MUJ PORTAL" and Sign In; Keen login-v1.css, pages/custom/user/login.js, scripts.bundle.js; current form exposes txtUserName, txtPassword, hidden login-context fields, a verification-token field, and Forgot Password linking to passwordreset.microsoftonline.com.
- WebForm1.aspx lesson: the CDX row shows status 200 (30 Mar 2022) but the replay body is an explicit 404 Error Page; archive metadata must always be read with body and timestamp.
- Header fingerprint (25 August 2026, public API observation): HTTP 200, Microsoft-IIS/10.0, X-AspNetMvc-Version: 5.3, X-AspNet-Version: 4.0.30319, X-Powered-By: ASP.NET, X-Frame-Options: SAMEORIGIN. Supports the supplied IIS/MVC 5.3/.NET-family stack for the observed response only.
- Identity: the FAQ says the SLCM password follows the official Outlook ID and documents AMS and Outlook support routes; the public OpenID configuration endpoint for muj.manipal.edu returns Microsoft tenant metadata. Direct SLCM OIDC use is unproven: no client identifier, redirect URI, callback, or token exchange is cited.
- 404 and 302 patterns coexist for the same route families (including misspellings like gardesheet.aspx), so intentional removal is unproven; "removed page" claims require a before-and-after body comparison.
- Akamai is not independently confirmed in this corpus; it stays an external research premise.

## KEY FACTS
- https://web.archive.org/cdx/search/cdx?url=mujslcm.jaipur.manipal.edu/*&from=2025&output=json&filter=statuscode:200&collapse=urlkey - MUJ 200 corpus; Home/Index (10 Jan 2025) and root (27 May 2025) HTML captures.
- https://web.archive.org/web/20170714034235id_/http://slcm.manipal.edu:80/loginForm.aspx - 2017 legacy login replay; branded page with incomplete replay body.
- https://web.archive.org/web/20170720030733id_/http://slcm.manipal.edu:80/StudentChangePassword.aspx - student password-change page; old, new, and confirmation labels.
- https://web.archive.org/web/20170813123113id_/http://slcm.manipal.edu:80/ParentChangePassword.aspx - separate parent password-change page with the same labels.
- https://web.archive.org/cdx/search/cdx?url=slcm.manipal.edu/*&from=2017&output=json&filter=statuscode:3..&filter=urlkey:.*(academic|dashboard|attendance|timetable|result|grade|registration|course|login|parent|student).*&collapse=urlkey - 302/303 route-vocabulary corpus for the legacy academic route family.
- https://web.archive.org/cdx/search/cdx?url=slcm.manipal.edu/*&from=2017&output=json&filter=statuscode:404&filter=mimetype:text/html&collapse=urlkey - legacy 404 corpus including GradeSheet, Grade.Sheet, Gradsheet, gardesheet, marksheet, Result, Results, Re_Registration variants.
- https://web.archive.org/web/20220330054426id_/https://slcm.manipal.edu/WebForm1.aspx - CDX 200 row whose body is a 404 Error Page; the report's central status-versus-body case study.
- https://web.archive.org/cdx/search/cdx?url=slcm.manipal.edu/Scripts/*&from=2017&output=json&filter=statuscode:200&collapse=urlkey - MicrosoftAjax.js and MicrosoftAjaxWebForms.js captures, a Web Forms-era signal (Jan 2019).
- https://web.archive.org/cdx/search/cdx?url=slcm.manipal.edu/assets/*&from=2017&output=json&filter=statuscode:200&collapse=urlkey - Bootstrap CSS/JS, jQuery 2.0.3, and MU-branded image assets (24 Apr 2018).
- https://web.archive.org/web/20250527044058id_/https%3A//mujslcm.jaipur.manipal.edu/ - 27 May 2025 MUJ root replay; "WELCOME TO MUJ PORTAL" and Sign In.
- https://mujslcm.jaipur.manipal.edu/Home/Index - current MUJ surface; student and parent login labels, @muj.manipal.edu.
- http://api.hackertarget.com/httpheaders?q=https://mujslcm.jaipur.manipal.edu/ - 25 Aug 2026 header observation: IIS 10.0, MVC 5.3, ASP.NET 4.0.30319, SAMEORIGIN.
- http://login.microsoftonline.com/muj.manipal.edu/.well-known/openid-configuration - Microsoft identity metadata (issuer, auth/token endpoints, Graph hosts) for the domain; tenant-level, not SLCM-level.
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - official FAQ: registration link, Outlook-ID password wording, AMS contact routes, Outlook troubleshooting via Team IT Infra.
- https://web.archive.org/cdx/search/cdx?url=slcm.manipal.edu/*&from=2017&output=json&filter=statuscode:200&filter=mimetype:text/html&collapse=urlkey - legacy HTML 200 corpus; contains Print.aspx and PaymentResponse.aspx in later captures.

## ACTIONABLE LEADS
- Archival next phase (recommended): preserve exact CDX query URLs, replay URLs, capture timestamps, response status, and visible page text; keep two fields per row: archive_status and body_interpretation.
- Build before-and-after tables per exact URL before claiming removal; a removal claim needs a documented body-level comparison, not a status row.
- Use the legacy route vocabulary as historical ecosystem context only; the report is explicit that route names are not an attack-surface list.
- High-value future artifact: an official migration or architecture document connecting the two hostnames and explaining identity integration; ask MUJ for it through authorized channels.
- Authorized-only verification items: current reachability of historical endpoints, whether the MUJ response headers hold across endpoints, OIDC client registration and callback config, Akamai path via DNS/CDN records.
- Track archived 2025+ MUJ assets (Keen login CSS, custom login JS, scripts.bundle.js) for drift against the live page during authorized review.
- Report hygiene: separate host timelines, label every architectural bridge as inference, never replay tokens or reproduce query values from PaymentResponse.aspx.

## FLAGS
- The header fingerprint is one point-in-time public observation via a third-party API (hackertarget); banners can be altered by proxies or spoofing and are not a source-code audit. X-AspNet-Version 4.0.30319 is the version-family value, not a patch-level inventory.
- CDX status alone is not truth: WebForm1.aspx (200 row, 404 body) is the report's own worked example; a nominal 200 can be a custom error document.
- PaymentResponse.aspx query strings and verification-cookie values are deliberately omitted; do not reconstruct or replay captured tokens.
- Redirect records (302/303) do not reveal destinations or whether the cause was authentication, authorization, routing, or an error.
- Microsoft OpenID metadata proves tenant configuration only; "Microsoft-linked identity and recovery workflow" is the safe wording, not "proven Microsoft SSO."
- Removal, full-rewrite, and shared-backend conclusions are explicitly unproven; the report says a route name is not a vulnerability and a public 404 is not misconfiguration.
- The crt.sh certificate-metadata URL appears in the scope description but receives no body-level analysis in the report.
- Corpus asymmetry: legacy data is route-rich but body-poor; MUJ data is front-door-only. Raw capture counts must not be compared as application size.

## COVERAGE
- File: w2g-14-wayback-family.md.
- 323 lines total; 55,156 bytes on disk; 55,154 chars read.
- Method: read_file offset 1, limit 2000, single call.
- EOF confirmed: final call returned truncated: false, last content line 323 equals total_lines 323.

---

## w2x-00-tech-stack-redo.digest

## REPORT
Source file: w2x-00-tech-stack-redo.md (MUJ SLCM Stack, Exposure, and Infrastructure Assessment)

## ANSWER SUMMARY
- Stack confirmed from public evidence: IIS 10.0, X-AspNet-Version 4.0.30319, X-AspNetMvc-Version 5.3 on MUJ; the parent slcm.manipal.edu independently reports IIS 10.0 and ASP.NET 4.0.30319.
- The YSOD value 4.7.4136.0 is an ASP.NET/System.Web assembly servicing version, not an installed-runtime or Windows patch inventory. Exact patch state is not publicly determinable.
- jQuery 1.10.2 with jquery.validate and jquery.validate.unobtrusive sits in the archived Keen demo1 asset tree used by the login page. This report counts 1.10.2 inside all four requested CVE ranges.
- CVE-2020-11023 has a concrete real-world signal: CISA added it to the KEV catalog on 2025-01-23. Exploitability at MUJ still depends on data flow.
- The "Akamai edge" label is contradicted: MUJ resolves to 98.70.14.50, AS8075 Microsoft (Pune), inside 98.70.0.0/15, with no PTR. Sibling muj.slcm.jaipur.manipal.edu is 20.244.94.89, also AS8075. A historical Akamai layer is possible but not established.
- TLS: both hosts grade B on SSL Labs. Both offer TLS 1.0, 1.1, 1.2, 3DES, static-RSA and CBC suites, negotiate HTTP/2 via ALPN, and lack HSTS. MUJ cert is an Entrust DV RSA cert for a single name (issued 2025-12-22, expiry 2026-12-21); parent uses a *.manipal.edu Sectigo OV wildcard.
- Missing anti-forgery token produces an HTTP 500 YSOD with a full stack trace. The exception is consistent with token enforcement, not a CSRF bypass; the defect is detailed remote error disclosure.
- Verdict: legacy ASP.NET MVC/IIS deployment with material hardening gaps, one obsolete client library, and an unproven runtime patch level. No server-side RCE, CSRF bypass, session fixation, ViewState exploit, path traversal, or MUJ-specific XSS demonstrated.

## KEY FACTS
- https://api.ssllabs.com/api/v3/analyze?host=mujslcm.jaipur.manipal.edu&publish=off&all=done&fromCache=on - MUJ grade B, TLS 1.0/1.1/1.2, h2 ALPN, MVC/IIS headers, no HSTS.
- https://api.ssllabs.com/api/v3/analyze?host=slcm.manipal.edu&publish=off&all=done&fromCache=on - parent grade B, classic ASP.NET session cookie (HttpOnly, SameSite=Lax), no XFO in capture.
- https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=A - current A record 98.70.14.50.
- https://ipinfo.io/98.70.14.50 - AS8075 Microsoft, Pune, marked hosting.
- https://bgp.he.net/ip/98.70.14.50 - route 98.70.0.0/15 owned by Microsoft.
- https://dns.google/resolve?name=muj.slcm.jaipur.manipal.edu&type=A - sibling hostname resolves to 20.244.94.89 (AS8075).
- http://web.archive.org/cdx/search/cdx?collapse=urlkey&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&output=json&url=mujslcm.jaipur.manipal.edu/* - archived asset inventory with Keen demo1 tree and jquery-1.10.2.min.js.
- https://crt.sh/?q=mujslcm.jaipur.manipal.edu&output=json - Entrust DV RSA certificate, single DNS name, 2025-12-22 to 2026-12-21.
- https://nvd.nist.gov/vuln/detail/CVE-2020-11023 - option-element HTML XSS; 1.10.2 in range; KEV-listed.
- https://www.cisa.gov/news-events/alerts/2025/01/23/cisa-adds-one-known-exploited-vulnerability-catalog - CVE-2020-11023 added to KEV on 2025-01-23.
- https://learn.microsoft.com/en-us/aspnet/mvc/overview/security/xsrfcsrf-prevention-in-aspnet-mvc-and-web-pages - two-token antiforgery model; missing, unreadable, or swapped tokens throw, which explains the YSOD.
- https://learn.microsoft.com/en-us/iis/get-started/whats-new-in-iis-10/http2-on-iis - IIS 10 HTTP/2 over TLS with HTTP/1.1 fallback, matching ALPN h2 http/1.1.
- https://learn.microsoft.com/en-us/iis/manage/configuring-security/use-request-filtering - IIS filter rejection codes 404.6/404.7/404.8/404.11/404.14/404.15 for verb, extension, hidden segment, double-encoding, and size rules.
- https://urlscan.io/api/v1/search/?q=filename%3A%22keen%2Fthemes%2Fkeen%2Ftheme%2Fdemo1%2Fdist%2Fassets%2Fcss%2Fpages%2Flogin%2Flogin-v1.css%22 - exact-path query returned MUJ scans only; no unrelated deployment asserted.
- https://dns.google/resolve?name=manipal.edu&type=TXT - SPF references Microsoft 365 protection, Brightspace, SendGrid, Salesforce; DMARC published at p=none via https://dns.google/resolve?name=_dmarc.manipal.edu&type=TXT.

## ACTIONABLE LEADS
- Authorized test order: DOM XSS and prototype pollution sinks; error handling (generic pages plus correlation IDs); antiforgery semantics (omission, swap, replay, identity change); session fixation and rotation; IIS path normalization parity; header and framing policy; TLS hardening; conditional ViewState/machineKey only where __VIEWSTATE appears; alternate-host parity for 20.244.94.89.
- Do not frame testing as an Akamai bypass. Establish the actual Azure service, load balancer, WAF, or direct-IIS topology from owner records first, then test front-door and origin parity.
- TLS remediation order: disable TLS 1.0/1.1 and 3DES/static-RSA, keep TLS 1.2 with modern suites, add TLS 1.3 where the platform allows, then staged HSTS starting with a short max-age.
- Suppress Server, X-Powered-By, X-AspNet-Version, and X-AspNetMvc-Version headers where operationally possible; this is recon reduction, not a patch.
- Confirm Secure and SameSite flags on the antiforgery cookie and session cookie; verify token pair binding and rotation on login.
- No YSOD corpus hunting or index probing; report privately to the university owner via coordinated disclosure.

## FLAGS
- Contradicts the "behind Akamai" premise used by w2f-01/w2f-02/w2f-03/w2f-04: AS8075 ownership and absent PTR contradict current Akamai edge attribution. Historical Akamai involvement is not ruled out.
- Cross-report CVE-2020-11022 conflict: this report counts 1.10.2 in range (>=1.2, <3.5.0 per NVD), while w2f-03 excludes it using the current CVE.org range (>=1.12.0). Both range sources are cited; canonical-record conflict must be resolved before the final count.
- 52.172.36.15 and 202.131.155.153 have no established portal relationship; naming them as origins would be speculation (the report says so explicitly).
- The YSOD observation is supplied hands-on evidence for 2026-08-25, not independently reproduced in this repo; treat as externally supplied.
- Keen demo1 fingerprint is high confidence for product, low for release; no exact Keen/Metronic version claim is supported.
- NVD keyword searches for Keenthemes and Keen theme returned zero; the single Metronic NVD hit was a name collision and was not assigned.
- SSL Labs grades and profiles are point-in-time cached scans; they can drift.

## COVERAGE
Chars read: 45,130 (file size), 373 lines. EOF confirmed: true (truncated false).

DONE w2x-00-tech-stack-redo.digest.md

---

## w3-01-exam-jaipur.digest

## REPORT
Source file: research/w3-01-exam-jaipur.md (AI deep-research output, claims UNVERIFIED). Topic: public evidence on `exam.jaipur.manipal.edu` in the MUJ SLCM ecosystem. Research cutoff 2026-08-25, passive non-authenticated collection.

## ANSWER SUMMARY
- Exam host network placement is the only high-confidence finding: `59.91.192.229` in `59.91.192.0/20`, AS9829, BSNL/National Internet Backbone, corroborated by Hurricane Electric, IPinfo, and Netcraft.
- No reviewed MUJ official source names `exam.jaipur.manipal.edu` or assigns any function to it; exam forms, hall tickets, results, and credentials are unverified hypotheses.
- Tension with supplied baseline: passive data puts `mujslcm.jaipur.manipal.edu` at `98.70.14.50` in Microsoft AS8075 (first seen July 2022), not Akamai; do not inherit the Akamai/ASP.NET MVC assumption.
- Credential reuse with SLCM is unverified; the SLCM FAQ ties the SLCM password to the official Outlook ID, but no document says the exam host accepts SLCM credentials.
- Public footprint is sparse: URLScan zero results, Shodan no IP record, Netcraft tech blank, Wayback CDX for the exact host returned an empty array.
- Governance is documented: Controller of Examinations, Deputy CoE, exam helpdesk and store emails, plus `it.support@jaipur.manipal.edu`; responsible disclosure should route there.
- One Reddit anecdote (SLCM password rejected) is a single unresolved support-friction case, not exam-host outage evidence.
- Verdict is Medium confidence; defensible line: low-visibility MUJ-domain asset on NIB with unknown purpose, stack, and login flow.

## KEY FACTS
- https://bgp.he.net/ip/59.91.192.229 - HE maps the IP into 59.91.192.0/20, AS9829, BSNL; core of the NIB claim.
- https://sitereport.netcraft.com/?url=http://exam.jaipur.manipal.edu - Netcraft: host to 59.91.192.229, AS9829, NIB owner; title/tech/first-seen blank; labels site non-HTTPS.
- https://ipinfo.io/59.91.192.229 - IPinfo: AS9829 NIB; geolocation Hoshiarpur, which conflicts with URLScan's Dehradun label.
- https://urlscan.io/api/v1/search/?q=domain:exam.jaipur.manipal.edu - zero scan results for the exact host.
- https://urlscan.io/domain/exam.jaipur.manipal.edu - domain summary associates host with 59.91.192.229/AS9829, no hits.
- https://www.shodan.io/host/59.91.192.229 - Shodan: no information available for the IP.
- https://jaipur.manipal.edu/examination.php - official MUJ exam page; CoE names, `exam.helpdesk@jaipur.manipal.edu`, `exam.store@jaipur.manipal.edu`.
- https://jaipur.manipal.edu/contact-university.php - MUJ campus identity, Dehmi Kalan, main phone +91 141-3999100.
- https://mujslcm.jaipur.manipal.edu/Home/Index - SLCM landing: MUJ portal, `@muj.manipal.edu`, student and parent login.
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - SLCM FAQ: username pattern, password "as per official outlook ID", `it.support@jaipur.manipal.edu`.
- https://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf - Admissions sends SLCM credentials to personal Gmail; names the SLCM URL, never the exam host.
- https://jaipur.manipal.edu/img/pdf/exam/3.%20Manual%20Exam%20Process.pdf - exam manual: CoE decentralization, 15-day result declaration; no exam-host URL.
- https://jaipur.manipal.edu/img/pdf/exam/Student%20Examination%20Handbook%202023-24%20%2811.08.2023%29.pdf - hall ticket required as ID but download venue not stated.
- https://sitereport.netcraft.com/?url=https://mujslcm.jaipur.manipal.edu - SLCM passive report: AS8075 Microsoft, first seen July 2022, tech still loading.
- http://reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue - only directly relevant complaint: SLCM password rejected, no visible resolution.

## ACTIONABLE LEADS
- Re-run passive checks (URLScan, Shodan, Wayback CDX, Netcraft) later to detect change in the exam-host record.
- Confirm purpose, owner, and retirement status with MUJ Examination and IT via `exam.helpdesk@jaipur.manipal.edu` and `it.support@jaipur.manipal.edu`.
- Validate the supplied SLCM baseline from owner-side DNS and edge inventories; never carry Akamai/IIS claims onto the exam host.
- Have MUJ confirm TLS and HTTPS posture; Netcraft's non-HTTPS label does not prove TCP/443 closed.
- In team output, label any claim that the host serves forms, hall tickets, or results as unverified inference.

## FLAGS
- Contradiction: supplied Akamai SLCM baseline versus passive AS8075 Microsoft address; report says unresolved architecture question.
- Contradiction: IPinfo Hoshiarpur versus URLScan Dehradun geolocation; only country and network ownership are safe to state.
- Unverified: exam-host purpose, technology, login flow, HTTPS state, and any SLCM credential bridge; no first-party source names the host.
- Negative results (empty URLScan, Shodan, Wayback CDX, blank Netcraft fields) prove absent indexed evidence, not an absent service.
- Anecdote is single-user, SLCM-targeted, unresolved; not exam-host evidence.
- Hall-ticket and exam-document findings never mention the hostname; converting business artifacts into host claims is the flagged OSINT failure mode.
- References 8, 9, and 17 appear as bare URL lines; claims tied to them lean on unverified AI output.

## COVERAGE
37,148 chars read on disk (wc -m), 279/279 lines, single read pass, final page returned truncated=false, EOF confirmed; file_size 37149 bytes; digests dir exists.

---

## w3-02-uat-manipal.digest

## REPORT
Source file: research/w3-02-uat-manipal.md (AI deep-research output, claims UNVERIFIED). Topic: exposure of `uat.manipal.edu` in the MUJ SLCM ecosystem. Passive sources observed 2026-08-25.

## ANSWER SUMMARY
- Application identity: the UAT shell is a MAHE institutional/marketing frontend (MAHE logo, programmes, campuses, Apply Now) with a branded Error 500 fallback; it does not publicly mirror MUJ SLCM or MAHE SLCM.
- Frontend markers `/_next/image` and `/_next/static` indicate a Next.js deployment, not the supplied ASP.NET MVC/IIS baseline; threat models must stay separate.
- Azure Front Door is confirmed: CNAME to `uat-ci-mahe-ep-bzgfhcehh0fvhafs.a01.azurefd.net`; anycast makes the supplied 150.171.110.195 versus current resolver 150.171.109.183 compatible, not contradictory.
- Archive presence is extensive: 1,811 successful CDX rows, 1,322 unique URLs, 2022-12-07 to 2023-10-02; historic content stays discoverable.
- No public secret leak found: generic Error 500 only, no stack traces, config files, or source-map names in the reviewed CDX inventory; bounded negative result.
- `robots.txt` disallows all crawlers while `sitemap.xml` returns the HTML app shell instead of XML; crawler policy is not access control.
- Microsoft guidance drives the main risk question: origins should reject non-Front-Door traffic (service tag `AzureFrontDoor.Backend` plus `X-Azure-FDID` check, or Private Link on Premium); origin isolation is unknown and owner-side.
- Verdict: High confidence in edge and app identity, Moderate in the bounded no-leak claim, Low for production-data status; risk rated Medium, escalating conditionally.

## KEY FACTS
- https://dns.google/resolve?name=uat.manipal.edu&type=CNAME - CNAME to `uat-ci-mahe-ep-bzgfhcehh0fvhafs.a01.azurefd.net`.
- https://dns.google/resolve?name=uat.manipal.edu&type=A - resolver chain through Front Door to 150.171.109.183.
- https://uat.manipal.edu/ - MAHE-branded shell, title "Top Higher Education Institution in India | Manipal University (MAHE)".
- https://uat.manipal.edu/sitemap.xml - returns branded HTML/error shell rather than an XML sitemap.
- https://uat.manipal.edu/mu.html - branded Error 500 body, `Apply Now` pointing to apply.manipal.edu.
- https://uat.manipal.edu/robots.txt - `User-agent: * Disallow: /`.
- https://crt.sh/?q=uat.manipal.edu - dedicated UAT certificates logged for 2025 and 2026, hostname actively maintained.
- https://web.archive.org/cdx/search/cdx?url=uat.manipal.edu%2F*&output=json&filter=statuscode%3A200&fl=timestamp%2Coriginal%2Cstatuscode%2Cmimetype%2Cdigest&collapse=digest - 1,811 rows / 1,322 unique URLs, Dec 2022 to Oct 2023.
- https://learn.microsoft.com/en-us/azure/frontdoor/origin-security - requires service-tag filtering plus profile-specific X-Azure-FDID validation for public origins.
- https://learn.microsoft.com/en-us/azure/frontdoor/private-link - Front Door Premium alternative so origins need no public address.
- https://learn.microsoft.com/en-us/azure/frontdoor/front-door-overview - Microsoft states Front Door is a global anycast CDN.
- https://mujslcm.jaipur.manipal.edu/Home/Index - MUJ portal "WELCOME TO MUJ PORTAL", sign-in and parent login.
- https://slcm.manipal.edu/ - MAHE SLCM "MU SLcM Sign in to your account".
- https://manipal.edu/mu/academics/student-portal.html - MAHE public student portal page linking to sis.manipal.edu/index.aspx.
- http://uat.manipal.edu/muj/admission/international-students/how-to-apply.html - historical UAT admissions route, supports the marketing-staging read.

## ACTIONABLE LEADS
- Owner-side proof of origin isolation: Private Link approval or combined service-tag plus X-Azure-FDID verification; treat origin bypass as the top control question.
- Classify UAT datastores and integrations; map data lineage for CMS content, forms, CRM connectors, and test accounts before any data claim.
- Fix routing anomalies: correct status codes at /sitemap.xml, monitor the branded 500 fallback, document robots.txt as crawler guidance only.
- Track CT and DNS for uat.manipal.edu; plan promotion or decommission with cache, certificate, and archive-aware review.
- Keep two models in team work: Next.js institutional UAT behind Front Door versus authenticated student-lifecycle hosts; do not merge.

## FLAGS
- Supplied IP 150.171.110.195 versus observed 150.171.109.183: report treats as anycast variance; no migration proven either way.
- CDX counts were computed locally from one provider response; no independent census.
- Origin hostname and address not present in public evidence; bypassability is unknown.
- No public evidence of production student data; absence of a leak is not proof of clean data separation.
- Next.js classification is an inference from asset paths, high confidence but not owner-confirmed.
- robots.txt disallow is voluntary crawler policy, not authorization.
- No-leak, no-source-map, no-config findings are bounded reviews, not exhaustive.
- All claims rest on AI deep-research output; treat every citation as unverified until rechecked.

## COVERAGE
36,195 chars read on disk (wc -m), 243/243 lines, single read pass, final page returned truncated=false, EOF confirmed; file_size 36195 bytes.

---

## w3-03-api-manipal.digest

## REPORT
Source file: research/w3-03-api-manipal.md (AI deep-research output, claims UNVERIFIED). Topic: `api.manipal.edu` exposure and its relationship to MUJ SLCM. Passive sources only.

## ANSWER SUMMARY
- Verified infrastructure: `api.manipal.edu` resolves to `43.205.223.7`; urlscan PTR and Shodan agree on Amazon EC2 ap-south-1, AS16509; Shodan records nginx 1.18.0, Ubuntu, Node.js, Express, and a Let's Encrypt cert (July 14 to October 12, 2026).
- Root behavior: HTTP 301 to HTTPS; HTTPS returns 200 JSON with one opaque `data` string; headers include `Access-Control-Allow-Origin: *` and `X-Powered-By: Express`.
- No official Swagger/OpenAPI located; the one found `api.yaml` belongs to a Vedic-Technologies physiotherapy project, a false positive.
- The SLCM relationship is unproven: no official source names `api.manipal.edu` as the MUJ SLCM backend; separate trust zones are the safe model.
- Archive shows four distinct root digests (2024-06-21, 2024-12-27, two on 2025-03-19), so the public representation changed over time.
- Community wrappers (nikeplusdash/SLCM-api, canaryGrapher/slcmAPI, manipalthetalk App-Backend) document legacy form-login scraping of `slcm.manipal.edu` with CAPTCHA; they are not current MUJ or API documentation.
- HackerTarget hostsearch lists nine API-labeled Manipal hosts; the bounded `jaipur.manipal.edu` response has no api-labeled name.
- Verdict: Moderate; the case is an API-governance and exposure concern, not a confirmed vulnerability.

## KEY FACTS
- https://dns.google/resolve?name=api.manipal.edu&type=A - A record 43.205.223.7, TTL 300.
- https://api.manipal.edu/ - HTTPS root returns JSON object with a single opaque `data` member.
- https://www.shodan.io/host/43.205.223.7 - nginx 1.18.0, Ubuntu, Node.js, Express, X-Powered-By header, wildcard CORS, Let's Encrypt cert.
- https://urlscan.io/domain/api.manipal.edu - AS16509, PTR `ec2-43-205-223-7.ap-south-1.compute.amazonaws.com`, Mumbai, CT observed 2022-04-05.
- https://api.hackertarget.com/hostsearch/?q=manipal.edu - nine API-labeled hosts (ams-api, api-convocation, api-invictus, api-mangaloreconvocation, api-mlrconv, api-summer, api-techtatva, api-timetracker, api).
- https://api.hackertarget.com/hostsearch/?q=jaipur.manipal.edu - bounded Jaipur host list with no api-labeled name.
- https://web.archive.org/cdx/search/cdx?url=api.manipal.edu%2F*&output=json&fl=timestamp,original,mimetype,statuscode,digest,length&filter=statuscode%3A200&collapse=digest - four distinct root digests, record lengths 607/717/720/718.
- https://raw.githubusercontent.com/nikeplusdash/SLCM-api/master/README.md - wrapper claims login to slcm.manipal.edu, /docs, no data storage, logout advice.
- https://raw.githubusercontent.com/nikeplusdash/SLCM-api/master/SLCM.py - requests.Session, ASP.NET fields, CAPTCHA, then profile and academics pages.
- https://raw.githubusercontent.com/canaryGrapher/slcmAPI/master/server.js - Express routes /getscores, /getattendance, /getprofile, /validateuser.
- https://github.com/Vedic-Technologies/manipal-server/blob/main/api.yaml - Swagger 2.0 physiotherapy project, false positive for SLCM attribution.
- https://mujslcm.jaipur.manipal.edu/Home/Index - MUJ portal with `@muj.manipal.edu` and parent login.
- https://muj.slcm.jaipur.manipal.edu/ - second MUJ host whose sign-in label uses `@jaipur.manipal.edu`.
- https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf - official SOP: login.microsoftonline.com, password change, MFA setup.
- https://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf - official onboarding: Admissions sends SLCM credentials to personal Gmail; parent login via mobile OTP.

## ACTIONABLE LEADS
- Internal review of `api.manipal.edu`: named owner, route and method inventory, auth policy, data schema, gateway config; compare deployed routes to source.
- Header hygiene: evaluate X-Powered-By exposure and wildcard CORS against an approved client-origin inventory.
- Reconcile the nine API-labeled hosts with cloud accounts, certificates, and owners; retire stale event systems (convocation, techtatva, invictus, summer).
- Produce a signed trust-boundary diagram for SLCM, parent OTP, Microsoft 365, and the API; do not assume federation.
- Versioned contract and change records for the root response; four digests show drift without release notes.
- nginx 1.18.0 is Shodan-tagged end-of-life; trigger an authenticated patch review, not a public exploit claim.

## FLAGS
- The supplied ASP.NET MVC/IIS/Akamai fingerprint is not corroborated; community VIEWSTATE/StudentProfile.aspx artifacts belong to legacy slcm.manipal.edu, not the MUJ portal.
- No official source proves api.manipal.edu backs SLCM; merging threat models is flagged.
- Shodan fingerprints are passive and time-bounded (last seen 2026-08-23); the report itself caps confidence by observed date.
- Wayback digests prove representation change, not semantic versions or reasons.
- CORS wildcard and header disclosure are observations, not vulnerabilities on their own.
- HackerTarget output is discovery evidence, not an authoritative CMDB.
- Reference numbering uses unusual bracket citation forms; all claims come from AI research and need verification before use.

## COVERAGE
35,260 chars read on disk (wc -m), 246/246 lines, single read pass, final page returned truncated=false, EOF confirmed; file_size 35262 bytes.

---

## w3-04-sis-manipal-feekart.digest

## REPORT
Source file: research/w3-04-sis-manipal-feekart.md (AI deep-research output, claims UNVERIFIED). Topic: MAHE SIS risk and MUJ SLCM trust boundaries. Passive OSINT and defensive assessment; no authentication, CAPTCHA, or payment testing.

## ANSWER SUMMARY
- SIS (`sis.manipal.edu/index.aspx`) serves MAHE students and parents, offers a separate administrator/faculty path, and directs logged-in users to Fee Kart; it is not proven to share a backend with MUJ SLCM.
- Fee Kart handoff is confirmed as an instruction; public payment pages collect application number, name, amount, email, and mobile and say a receipt will be emailed.
- Gateway charge tables name Atom and HDFC with 18 percent GST on convenience fees, but the page is undated, so current processor status is unverified.
- Session internals are unpublished: the student login shows a date field (`dd/mm/yyyy`) and CAPTCHA, with no public data on timeout, rotation, cookie scope, or server-side logout.
- Legacy routes remain public: /index.aspx, /studloginSLCM.aspx, /OnlinePayment01.aspx, /CourseFeesMAHE01/02.aspx, /SLCMRTGS01.aspx, /SLCMMessChange04Blocked.aspx; Wayback captures of the main SIS page start in 2013.
- Reddit anecdotes report registration-number rejection, a rejected correct password, and recurring crashes; all are unverified and unproven as breach signals.
- Microsoft 365 linkage is partly proven: MAHE extends O365 to faculty and students and the MUJ page shows `@muj.manipal.edu`; federation between SIS and MUJ SLCM is not established.
- Verdict: Moderate; the case is trust-management risk and authorized-review work, not a demonstrated breach; cross-system blast radius is social and identity-based, not proven technical.

## KEY FACTS
- https://sis.manipal.edu/index.aspx - SIS landing: student/parent role split, admin/faculty choice, Fee Kart instruction after login.
- https://sis.manipal.edu/studloginSLCM.aspx - student login with date field and CAPTCHA visible.
- https://sis.manipal.edu/OnlinePayment01.aspx - collects email and mobile; receipt is emailed.
- https://sis.manipal.edu/admissions/CourseFeesMAHE01.aspx - collects application, name, fee amount, email, mobile.
- https://sis.manipal.edu/admissions/CourseFeesMAHE02.aspx - same fields plus gateway-charge table (Atom, HDFC, 18% GST); undated.
- https://sis.manipal.edu/SLCMRTGS01.aspx - RTGS-named alternate route repeating SIS description and login elements.
- https://sis.manipal.edu/SLCMMessChange04Blocked.aspx - menu labels: virtual account, hostel dues, receipt reprint, vacating form, logout, mess change.
- https://mujslcm.jaipur.manipal.edu/Home/Index - MUJ portal "WELCOME TO MUJ PORTAL", `@muj.manipal.edu`, parent login.
- https://manipal.edu/mu/academics/student-portal.html - official MAHE page linking users to SIS.
- https://manipal.edu/mu/policies/it-policy/information-security-policy.html - MAHE security policy: controlled, monitored, authorized access by job function and need.
- https://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf - MAHE ICT list: SLCM functions (attendance, marks, results, circulars) and O365 for faculty and students.
- https://github.com/sankalp2004/SLCM-is-Dumb - unofficial tool that extracts CGPA and passes CAPTCHA; operational details omitted by report.
- https://github.com/nikeplusdash/SLCM-api - unofficial API logging into slcm.manipal.edu, retrieving data, requiring logout.
- https://github.com/canaryGrapher/slcmAPI - community REST API deprecated after CAPTCHA was introduced.
- https://web.archive.org/cdx/search/cdx?url=sis.manipal.edu/index.aspx%26output=json%26filter=statuscode:200%26fl=timestamp,original%26collapse=digest - SIS index.aspx captures from 2013-10-03.

## ACTIONABLE LEADS
- Build the SIS-MUJ-M365 identity and recovery map: IdP, account source, reset owner, parent-account source, SSO status; treat federation as unverified until owner confirms.
- Inventory every `.aspx` login and payment route; check parallel pages (/CourseFeesMAHE01 vs 02, /SLCMRTGS01) for config drift and retirement.
- Payment review under authorization: server-derived amount and student identity, short-lived signed handoff, authenticated idempotent callbacks, ledger reconciliation independent of the emailed receipt.
- Validate session controls against OWASP Session Management and CSRF cheat sheets (rotation at auth, idle/absolute timeouts, logout invalidation, Secure/HttpOnly/SameSite).
- Correlate complaint spikes with enrollment, fee, and examination windows; standardize identity-change and password-failure handling.
- Publish canonical domain, status, and payment-origin guidance for students facing login friction.

## FLAGS
- The date field's meaning is unknown (identifier, second factor, or biographical data); the report refuses to call it a vulnerability.
- Atom/HDFC names and rates come from an undated page; current processor contract unverified.
- Reddit posts are anonymous anecdotes with no root cause, frequency, or resolution data.
- Shared-brand and shared-population evidence yields only inferred social/identity spillover; no shared session, password store, database, or key is proven.
- CAPTCHA presence is a UI fact, not a control assessment; OWASP references are benchmarks, not findings against SIS.
- MAHE policy citations establish institutional intent, not actual deployment.
- References 16, 26, and 27 contain malformed raw-ampersand CDX URLs; treat related claims as weak.
- Full report is AI output; every citation needs independent verification.

## COVERAGE
39,523 chars read on disk (wc -m), 275/275 lines, single read pass, final page returned truncated=false, EOF confirmed; file_size 39527 bytes.

---

## w3-05-webmail-manipal.digest

## REPORT
Source file: research/w3-05-webmail-manipal.md (AI deep-research output, claims UNVERIFIED). Topic: evidence-based assessment of `webmail.manipal.edu`. Public DNS, routing, archives, official MUJ documents, vendor docs; no credential testing.

## ANSWER SUMMARY
- Network identity: `webmail.manipal.edu` resolves to `218.248.47.16` (TTL 14,400); RIPEstat shows the host block `218.248.47.0/26` with netname MAHE, while the covering route `218.248.32.0/20` is AS9829 BSNL-NIB; the /26 itself is not directly announced in the cited result.
- Parent-domain mail is Microsoft 365: MX `manipal-edu.mail.protection.outlook.com`, autodiscover CNAME to `autodiscover.outlook.com`, DKIM selectors into `learnermanipal.onmicrosoft.com`, corroborated by ViewDNS.
- Historical identity is Exchange/OWA: 2006 capture names Exchange Server 2003 OWA with `Domain\user name` fields, 2012 OWA Light (CookieAuth), 2015 and 2016 Outlook Web App.
- The 2022 archive replay at `/userportal/webpages/myaccount/login.jsp` contains "Sophos" and locale strings, and the current indexed page is titled "VPN Portal" with a JavaScript fallback message; current live markup was not extractable.
- Credential acceptance is not established for any source; the parent MX and M365 DNS do not prove the webmail host redirects to or shares Microsoft identity.
- The MUJ O365 SOP makes MFA mandatory and documents Microsoft Authenticator, phone, and email verification; the SLCM FAQ ties the SLCM password to the Outlook ID but never names the webmail host as a backend.
- Verdict: High confidence for historical OWA/Exchange lineage and parent-domain Microsoft 365, Medium for a later Sophos-style portal inference, Low for current legacy OWA status, none for credential acceptance.

## KEY FACTS
- https://dns.google/resolve?name=webmail.manipal.edu&type=A - A record 218.248.47.16, TTL 14400.
- https://stat.ripe.net/data/whois/data.json?resource=218.248.47.16 - 218.248.47.0/26 netname MAHE, ASSIGNED NON-PORTABLE, country IN.
- https://stat.ripe.net/data/prefix-overview/data.json?resource=218.248.47.0/24 - aligned to 218.248.32.0/20 announced by AS9829; queried /24 not itself announced.
- https://stat.ripe.net/data/as-overview/data.json?resource=AS9829 - holder BSNL-NIB National Internet Backbone.
- https://dns.google/resolve?name=manipal.edu&type=MX - MX preference 0 to manipal-edu.mail.protection.outlook.com.
- https://dns.google/resolve?name=autodiscover.manipal.edu&type=CNAME - autodiscover.outlook.com.
- https://dns.google/resolve?name=selector1._domainkey.manipal.edu&type=CNAME - DKIM delegation into learnermanipal.onmicrosoft.com.
- https://urlscan.io/domain/webmail.manipal.edu/ - IP 218.248.47.16, AS9829/BSNL-NIB, GeoIP Bhubaneswar, not observed on urlscan.
- https://web.archive.org/web/20060903020056id_/https://webmail.manipal.edu/exchweb/bin/auth/owalogon.asp?url=https%3A%2F%2Fwebmail.manipal.edu%2FExchange%26reason=0 - 2006 OWA explicitly on Exchange Server 2003.
- https://web.archive.org/web/20120113021334id_/https://webmail.manipal.edu/CookieAuth.dll?GetLogon?curl=Z2Fexchange%26reason=0%26formdir=1 - 2012 Exchange OWA Light capture.
- https://web.archive.org/web/20150605035251id_/https://webmail.manipal.edu/owa/auth/logon.aspx - 2015 Outlook Web App login path.
- https://web.archive.org/web/20220303013019/https://webmail.manipal.edu/userportal/webpages/myaccount/login.jsp - 2022 replay with Sophos text and locale list.
- https://webmail.manipal.edu/ - current indexed page titled "VPN Portal" with JavaScript-required message.
- https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf - official MUJ SOP: Microsoft 365 sign-in, mandatory MFA, recovery options.
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - SLCM FAQ: username pattern, password as per official Outlook ID; no webmail-host link.

## ACTIONABLE LEADS
- Ask MAHE IT whether the hostname is retired, redirected, or required; obtain a purpose statement and service generation record.
- Owner-side check that legacy OWA paths (/exchweb, /owa, /CookieAuth.dll) are disabled or access-controlled.
- Confirm whether a Sophos user/VPN portal is current, which identity provider it uses, and its port/posture (Sophos default port 4443 is vendor documentation, not host evidence).
- Verify Microsoft 365 is the only sanctioned mail authentication path and that MFA enforcement covers it.
- Track the 218.248.47.0/26 announcement question internally; report routing ownership separately from address assignment.
- Do not test credentials in any form; the report explicitly forbids it and states account-lock and incident-alert risks.

## FLAGS
- The /26 block is not directly announced in the cited RIPEstat response; claiming direct /26 announcement would overstate the data.
- "Not observed on urlscan.io" is a coverage statement, not a negative security finding.
- Archive captures are historical, not live-state evidence; 2015/2016 login fields do not prove current reachability or authentication.
- Sophos attribution is an inference from one 2022 replay plus current indexed wording; no version, port, live markup, or vendor certificate observed.
- The 2022 cleaned replay lacks a complete login form; that absence is an extraction limitation.
- CertSpotter's empty issuance array is a coverage result, not proof of no certificate.
- The current "VPN Portal" claim rests on indexed text because direct extraction returned no readable markup.
- All claims come from AI research output and are unverified until rechecked against the cited sources.

## COVERAGE
25,275 chars read on disk (wc -m), 146/146 lines, single read pass, final page returned truncated=false, EOF confirmed; file_size 25281 bytes.

---

## w3-06-portal-manipal.digest

## REPORT
Source file: w3-06-portal-manipal.md (280 lines, 46,620 bytes)
Report title: MUJ SLCM and Portal Public OSINT Assessment

## ANSWER SUMMARY
- MUJ SLCM is an academic student and parent system. Official ICT inventory names it as replacement for the older Academic Management System, covering attendance, internal marks, external marks, result publication, and broadcast messages. High confidence.
- portal.manipal.edu currently exposes an EPF application with user, resigned-employee, and admin login routes; footer credits MAHE Information Systems. It is a separate employee or administrative surface, not SLCM.
- Two separate public endpoints: SLCM resolves to 98.70.14.50, portal to 45.112.150.155 (TTL 300). Portal address is announced by AS134039, label Ibus Virtual Network Services Private Limited.
- Third-party header scan of SLCM shows IIS 10.0, ASP.NET MVC 5.3, ASP.NET 4.0.30319, grade D; X-Frame-Options present, HSTS, CSP, X-Content-Type-Options, Referrer-Policy, Permissions-Policy missing.
- Portal root returned HTTP 403 in its scan but still discloses IIS 10.0 and ASP.NET; grade F. The error response limits the value of that fingerprint.
- Wayback shows the portal root served a generic IIS Windows Server landing page on 18 April 2022; no archive proof of when EPF was deployed.
- Akamai is unconfirmed: portal CNAME and HTTPS DNS queries returned no answer, no Akamai label in the header report. Absence is not proof of no CDN.
- Microsoft SSO is unconfirmed: OpenID metadata proves a jaipur.manipal.edu tenant exists, not that SLCM federates.

## KEY FACTS
1. https://mujslcm.jaipur.manipal.edu/ : primary target; MUJ Portal sign-in and parent login surface.
2. http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf : official ICT inventory; SLCM function and module list.
3. https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=A : SLCM A record, 98.70.14.50.
4. http://securityheaders.com/?followRedirects=on&q=https://mujslcm.jaipur.manipal.edu/ : IIS 10, MVC 5.3, ASP.NET 4.0.30319 fingerprint, grade D.
5. https://portal.manipal.edu/epf/userlogin.aspx : EPF user login with email and password form, MAHE ISD footer.
6. https://portal.manipal.edu/epf/rtlogin.aspx : resigned-employee login route with employee-ID label.
7. https://portal.manipal.edu/epf/admlogin.aspx : admin login route with @manipal.edu email cue.
8. https://dns.google/resolve?name=portal.manipal.edu&type=A : portal A record, 45.112.150.155, TTL 300.
9. https://bgp.he.net/ip/45.112.150.155 : AS134039 announces 45.112.150.0/24, Ibus label.
10. https://urlscan.io/domain/portal.manipal.edu : passive metadata; AS134039, Udupi GeoIP, first observed 4 January 2019.
11. https://web.archive.org/cdx/search/cdx?url=portal.manipal.edu&output=json&filter=statuscode:200&fl=timestamp,original,statuscode,digest&collapse=digest : root 200 captures on 18 April 2022.
12. https://web.archive.org/web/20220418001040/https://portal.manipal.edu/ : archived generic IIS Windows Server landing page.
13. https://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf : SLCM credentials sent to personal Gmail during admission.
14. https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf : SLCM password described as per official Outlook ID; AMS support contacts.
15. http://login.microsoftonline.com/jaipur.manipal.edu/.well-known/openid-configuration : Microsoft tenant metadata exists; SLCM integration not stated.

## ACTIONABLE LEADS
- Enumerate EPF child routes passively: /epf, /epf/Home.aspx, userlogin, rtlogin, admlogin are search-indexed; review indexing policy, not credentials.
- Compare header sets across portal / and /epf routes in an authorized review; root 403 vs reachable child routes suggests per-path policy.
- Re-query DNS A, CNAME, HTTPS records for both hosts at later dates to track edge or CDN changes.
- Check /.well-known/security.txt on mujslcm: retrieved response looked like portal content, not an RFC 9116 record with a Contact field.
- Map the identity chain from written docs only: Gmail delivery, Outlook-ID password wording, Office 365 MFA mandate; do not assert SSO.
- Use listed governance contacts (MUJ contact page, SLCM FAQ AMS and IT Infra, MAHE student portal) for ownership confirmation.
- Record related surfaces: sis.manipal.edu, hms.manipal.edu/login.aspx, libportal.manipal.edu, apply.manipal.edu, mufc.manipal.edu.

## FLAGS
- Akamai claim from the brief: unconfirmed by this report.
- Microsoft 365 SSO claim: unconfirmed; tenant metadata is not integration proof.
- security.txt response is not a structured record; do not claim absence of a reporting process.
- Time-bound observations: SecurityHeaders scans dated 25 August 2026 (12:27 UTC portal, 12:34 UTC MUJ).
- Prefix discrepancy between sources: BGP.HE reports 45.112.150.0/24, urlscan reports route 45.112.148.0/22; both list AS134039.
- urlscan shows zero direct or incoming hits for the domain; report treats the counters as telemetry limits, not proof of disuse.
- References 11 and 12 (crt.sh, Wappalyzer) appear in the reference list but are not used as evidence in the body.

## COVERAGE
- Chars read: 46,620; lines 280; truncated false; EOF confirmed.

---

## w3-07-hms-manipal.digest

## REPORT
Source file: w3-07-hms-manipal.md (280 lines, 33,341 bytes)
Report title: HMS Manipal OSINT Report: Identity, Exposure, and MUJ Separation

## ANSWER SUMMARY
- HMS means Hostel Management System. hms-admin.manipal.edu explicitly expands HMS and describes room and seat booking by block, capacity, and availability.
- Scope is MAHE: landing page lists Manipal, Health Science, Mangalore, and Bangalore hostel contacts. No Jaipur or MUJ references.
- hms.manipal.edu resolves to 20.44.49.205, AS8075 Microsoft Corporation; Shodan snapshot reports Microsoft Azure Application Gateway v2, last seen 23 August 2026.
- Edge masks the origin: header snapshot shows gateway affinity cookies and no Server, X-AspNet-Version, X-AspNetMvc-Version, or X-Powered-By values.
- SecurityHeaders snapshot dated 25 August 2026: grade A for hms; X-Frame-Options, HSTS, CSP, X-Content-Type-Options, X-XSS-Protection, X-Download-Options present; Referrer-Policy and Permissions-Policy missing.
- IIS 10.0, MVC 5.3, ASP.NET 4.0.30319 fingerprint is evidenced for MUJ SLCM only, not for HMS.
- Akamai is not substantiated for hms.manipal.edu; no DNS alias, header, certificate, or passive record located.
- No hostname-specific incident: Open Bug Bounty record is manipal.edu.np XSS, Brinztech is the library portal, LeakRadar is a domain-level aggregator.

## KEY FACTS
1. https://hms.manipal.edu/ : hostel landing page, "Your Home Away From Home", campus contacts.
2. https://hms-admin.manipal.edu/ : explicit HOSTEL MANAGEMENT SYSTEM label and booking description.
3. https://hms.manipal.edu/Login.aspx : login labels: learner email, mobile OTP, employee auth, guest, application and roll numbers.
4. https://dns.google/resolve?name=hms.manipal.edu&type=A : A record 20.44.49.205, TTL 3600.
5. https://ipinfo.io/20.44.49.205/json : AS8075 Microsoft, Chennai geolocation.
6. https://www.shodan.io/host/20.44.49.205 : Azure Application Gateway v2 product snapshot.
7. http://securityheaders.com/?followRedirects=on&q=https://hms.manipal.edu/ : grade A snapshot, two headers missing.
8. http://api.hackertarget.com/httpheaders?q=https://mujslcm.jaipur.manipal.edu/ : MUJ stack fingerprint (IIS 10, MVC 5.3, ASP.NET 4.0.30319).
9. http://web.archive.org/cdx/search/cdx?collapse=urlkey&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&output=json&url=hms.manipal.edu/* : historical paths including Authorization.aspx, Atom_PayResponse.aspx, HDFCResponse.aspx.
10. https://login.microsoftonline.com/muj.manipal.edu/.well-known/openid-configuration : tenant ID 27282fdd-4c0b-4dfb-ba91-228cd83fdf71; no HMS client evidence.
11. https://jaipur.manipal.edu/hostel-facility.php : MUJ hostels, first-come-first-served allotment, SpaceBasic maintenance link.
12. https://jaipur.manipal.edu/hostel-fees.php : 2026-27 double occupancy fees, room booking portal, pay-fee-online destination.
13. https://www.openbugbounty.org/reports/2160625/ : manipal.edu.np XSS, patched; not HMS.
14. https://www.brinztech.com/breach-alerts/brinztech-alert-database-of-manipal-library-portal-leaked/ : library portal claim, not HMS.
15. https://hostel.manipal.edu/indexICAS.aspx : legacy indexed "Hostel Management System" login with CAPTCHA.

## ACTIONABLE LEADS
- Passive recheck of the login page over time to see if a login.microsoftonline.com redirect or client ID ever appears; none observed so far.
- Verify the payment surface: archive paths Atom_PayResponse.aspx and HDFCResponse.aspx exist; current provider unknown.
- Compare header behavior across hms root, Home.aspx, and Login.aspx under authorized review; gateway may add affinity cookie markers.
- Treat hms.manipal.edu, hms-admin.manipal.edu, and legacy hostel.manipal.edu/indexICAS.aspx as three surfaces of one service.
- Confirm whether the MUJ room-booking portal (fee page) is the same service; MUJ pages do not name hms.
- Treat missing Referrer-Policy and Permissions-Policy as hardening signals only; grade A snapshot is not a security verdict.

## FLAGS
- Citation markers like [295.38] and [288.0-8] appear to be extract line ranges; the mapping cannot be verified from the report text alone.
- Shodan and SecurityHeaders are third-party snapshots, time-bound to August 2026.
- CSP in the hms snapshot permits unsafe-inline and unsafe-eval for scripts; noted as observation, not a finding.
- PTR and CNAME queries returned nothing: bounded negative results.
- RMS page statement "RMS uses Outlook credentials" must not be reused as HMS evidence.
- MUJ fee figures (Rs 167,372, Rs 15,378, Rs 25,475) are for 2026-27 and apply to MUJ hostels, not HMS.

## COVERAGE
- Chars read: 33,341; lines 280; truncated false; EOF confirmed.

---

## w3-08-mujone.digest

## REPORT
Source file: w3-08-mujone.md (192 lines, 30,002 bytes)
Report title: MUJ SLCM Ecosystem: Public Evidence, Identity Boundaries, and Technology Risk

## ANSWER SUMMARY
- mujone.jaipur.manipal.edu publicly presents as "MUJ HR SYSTEM": employee code, date of birth, CAPTCHA, password change, policy acknowledgement, PAS Portal link, ISD/CSD MAHE attribution.
- SLCM, not MUJ One, is the student and parent portal: "WELCOME TO MUJ PORTAL", sign in and parent login, @muj.manipal.edu label.
- MUJ One resolves to 52.172.36.15, AS8075 Microsoft, geolocated to Chennai by IPinfo. Azure South India region is not proven.
- Outlook and Microsoft 365 coupling is documented: FAQ ties the SLCM password to the official Outlook ID; SOP makes MFA mandatory for Office 365. Federated SSO is not proven.
- Akamai is unverified; URLScan observations for SLCM show Microsoft-IIS/10.0 and 8.5, with no framework or Akamai signal.
- No official MUJ One mobile app was found on Google Play or Apple search; located apps (MUJ GO, MUJstella, CampusAdda, MUJ Gym) are third-party or independent, CampusAdda disclaims affiliation.
- Archive bounds: MUJ One HTML captures 2022-08-17 to 2024-08-28; SLCM captures 2025-01-10 to 2026-08-05.
- Header collection attempts via SecurityHeaders and HackerTarget timed out; report treats timeouts as collection failures, not findings.

## KEY FACTS
1. https://mujone.jaipur.manipal.edu/HR/Login.aspx : HR branding, CAPTCHA, policy screens.
2. https://mujone.jaipur.manipal.edu/HR/ : PAS Portal link, employee code and DOB fields.
3. https://mujslcm.jaipur.manipal.edu/ : MUJ Portal branding, @muj.manipal.edu, sign-in and parent login.
4. https://mujslcm.jaipur.manipal.edu/Student/Academic/AttendanceSummaryForStudent : publicly indexed attendance route, login surface when unauthenticated.
5. https://dns.google/resolve?name=mujone.jaipur.manipal.edu&type=A : A record 52.172.36.15.
6. https://ipinfo.io/52.172.36.15/json : AS8075, Chennai, Tamil Nadu.
7. https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf : registration URL, username pattern, Outlook-aligned password wording.
8. https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf : Office 365 SOP, mandatory MFA, Version 1.0 effective June 2025.
9. https://www.jaipur.manipal.edu/administration-it.php : IT landscape: Microsoft services, business ERP, student lifecycle portal, LMS.
10. https://web.archive.org/cdx/search/cdx?url=mujone.jaipur.manipal.edu/*&output=json&filter=statuscode:200&filter=mimetype:text/html&fl=timestamp,original,statuscode,mimetype&collapse=digest&limit=100 : MUJ One capture bounds 2022-08-17 to 2024-08-28.
11. https://web.archive.org/cdx/search/cdx?url=mujslcm.jaipur.manipal.edu/*&output=json&filter=statuscode:200&filter=mimetype:text/html&fl=timestamp,original,statuscode,mimetype&collapse=digest&limit=100 : SLCM capture bounds 2025-01-10 to 2026-08-05.
12. https://urlscan.io/api/v1/search/?q=domain:mujslcm.jaipur.manipal.edu : IIS 10 and 8.5 observations; no Akamai signal.
13. https://www.myandroid.org/apps/com-manipal-muj-go : MUJ GO listing, package com.manipal.muj.go, unverified publisher.
14. https://play.google.com/store/search?q=MUJ%20One&c=apps : negative search result for MUJ One.
15. https://web.archive.org/web/20240828092621id_/https://mujone.jaipur.manipal.edu/HR/Login.aspx?AspxAutoDetectCookieSupport=1 : archived 302 capture of the HR login.

## ACTIONABLE LEADS
- Monitor root and /HR/ of mujone for non-HR routes via archives and search indexes; report found none publicly.
- Re-run header collection at later dates; prior attempts timed out, a gap, not a negative finding.
- Check CNAME and authority records; Azure DNS nameservers appeared in zone authority material.
- Document the muj.slcm.jaipur.manipal.edu variant and slcm.manipal.edu relationship from official sources before any claims.
- Ask the university for a canonical app list; third-party apps using MUJ branding create a phishing surface.
- Clarify PAS Portal meaning with the IT owner; report does not classify it.

## FLAGS
- App store searches are bounded negatives; apps can be delisted or region-restricted.
- MUJstella package id com.yourcompany.mujstellaapp is a placeholder-style identifier; publisher claims are unverified.
- URLScan shows IIS 8.5 and 10.0 in different observations; do not collapse into one version claim.
- Azure South India, MVC 5.3, .NET Framework 4.x, Akamai: all unverified for both hosts.
- Azure DNS nameservers in authority data prove DNS hosting only, not application hosting.
- Report treats "domain label One implies SSO" as a common OSINT error; the SSO role of MUJ One stays unverified.

## COVERAGE
- Chars read: 30,002; lines 192; truncated false; EOF confirmed.

---

## w3-09-mujerp.digest

## REPORT
Source file: w3-09-mujerp.md (194 lines, 29,860 bytes)
Report title: What MUJ's ERP Host Reveals About SLCM Boundaries

## ANSWER SUMMARY
- http://mujerp.jaipur.manipal.edu/MUJWEB/ self-identifies as "Welcome to Dynamics 365 Business Central" with a User name and Password form posting to /MUJWEB/SignIn.
- Product reading: Business Central is ERP per Microsoft documentation; the host is a Business Central web front end, not proof of SLCM linkage.
- SLCM is a separate service: one-stop academic-information portal per the first-year guide, with student and parent entry points.
- MUJ IT page names ERP, student life-cycle web portal, LMS, and research management as separate landscape items; adjacency, not integration.
- DNS-over-HTTPS returns an A record of 20.244.0.229 for mujerp, TTL 3600; region and ownership unverified.
- Business Central supports many credential modes (Windows, NavUserPassword, AccessControlService via Entra); a username and password form does not reveal identity architecture.
- Staff use is plausible from public finance and IT pages, but no public source names a staff member using mujerp.
- Supplied claims: ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, Azure Central India, CT since April 2025: none independently confirmed.

## KEY FACTS
1. https://mujerp.jaipur.manipal.edu/MUJWEB/ : Business Central title, ms-nav layout, /MUJWEB/SignIn form action.
2. https://mujslcm.jaipur.manipal.edu/Home/Index : SLCM portal with parent login.
3. https://mujslcm.jaipur.manipal.edu/ : SLCM markup with Keen theme assets and @muj.manipal.edu write-in.
4. https://www.microsoft.com/en-us/dynamics-365/products/business-central : Microsoft describes Business Central as ERP software.
5. https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/administration/users-credential-types : credential types incl AccessControlService backed by Entra ID.
6. https://dns.google/resolve?name=mujerp.jaipur.manipal.edu&type=A : A record 20.244.0.229, TTL 3600.
7. http://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf : SLCM onboarding workflow, non-editable admission fields, parent OTP.
8. http://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf : SLCM URL, username pattern, Outlook ID password guidance.
9. https://www.jaipur.manipal.edu/administration-it.php : IT landscape wording places ERP and student lifecycle side by side.
10. https://jaipur.manipal.edu/administration-finance.php : fee collections, payroll, accounting, audits; does not name mujerp.
11. https://mujone.jaipur.manipal.edu/HR/ : separate MUJ HR SYSTEM surface with employee fields.
12. https://www.microsoft.com/en-us/download/details.aspx?id=56519 : Azure IP ranges file; general, cannot prove Central India for one address.
13. http://web.archive.org/cdx/search/cdx?collapse=urlkey&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&output=json&url=mujslcm.jaipur.manipal.edu/* : archived SLCM HTML and Keen theme assets.
14. https://www.manipal.edu/mu/policies/it-policy/information-security-policy.html : related MUJ policy context cited by the report.

## ACTIONABLE LEADS
- Passive re-fetch of /MUJWEB/ at intervals; any redirect to login.microsoftonline.com would change the identity assessment.
- Query CNAME and HTTPS records for mujerp to test for CDN or gateway layers.
- Re-run CT log queries for mujerp.jaipur.manipal.edu; the report got no usable result.
- Match the exact Azure IP ranges file to 20.244.0.229 before any region claim.
- Request from the owner: tenant, credential mode, MFA status, module list, user population.
- Verify whether the SignIn form enforces double-submit only client-side; do not test server behavior without authorization.

## FLAGS
- Report wording: product label proves product family, not modules, tenant, or users.
- MVC 5.3, .NET 4.x, IIS 10, Akamai, Central India, CT date: all supplied and unverified.
- CT search failure for the exact hostname is a bounded negative.
- Staff-use and finance-system claims are inference from public role and finance pages.
- The first-year guide and FAQ describe SLCM, not Business Central usage.

## COVERAGE
- Chars read: 29,860; lines 194; truncated false; EOF confirmed.

---

## w3-10-rms-jaipur.digest

## REPORT
Source file: w3-10-rms-jaipur.md (219 lines, 31,637 bytes)
Report title: RMS Jaipur: Public Surface, Provenance, and Unknowns

## ANSWER SUMMARY
- RMS on the target page explicitly means Research Data Management System; it links to MUJ IRINS and shows research-performance notices.
- "Result Management System" is not supported by any reviewed evidence and must not be published as fact.
- Login.aspx shows User Name, Password, the @jaipur.manipal.edu suffix, a Chrome note, and a footer crediting MSIS and ISD at MAHE.
- Central RMS (rms.manipal.edu) documents research workflows and support mailboxes and says RMS uses the same login credentials as the Outlook account; that statement is about the central page, not automatically the Jaipur host.
- Network: resolves to 202.131.155.153; BGP and IPinfo agree on AS134039, Ibus Virtual Network Services Private Limited; reverse DNS 202.131.155.153.convergentindia.com; IPinfo geolocates to Delhi.
- Legacy ASP.NET Web Forms-style indicators: Login.aspx, WebResource.axd, aspnetForm; MVC 5.3, .NET 4.x, IIS 10, Akamai remain unverified for RMS.
- Archive: root captured 2024-03-22 (February 2024 notice), Error.aspx captured 2024-08-28, WebResource.axd and assets from August 2024.
- No RMS-specific public complaint found in the searched indexes; bounded negative.

## KEY FACTS
1. https://rms.jaipur.manipal.edu/ : target root, Research Data Management System title, IRINS link, notices.
2. https://rms.jaipur.manipal.edu/Login.aspx : login fields, suffix, footer, Chrome note.
3. https://rms.manipal.edu/ : central RMS, support mailboxes, Outlook credential statement.
4. https://muj.irins.org/ : MUJ research profile portal with nodal officer and faculty login links.
5. https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf : SLCM registration URL, username pattern, AMS contacts.
6. https://mujslcm.jaipur.manipal.edu/Home/Index : SLCM portal surface for comparison.
7. https://bgp.he.net/ip/202.131.155.153 : AS134039, 202.131.155.0/24, Ibus, convergentindia reverse DNS.
8. https://ipinfo.io/202.131.155.153 : AS134039, Ibus, Delhi classification.
9. http://dns.google/resolve?name=rms.jaipur.manipal.edu&type=A : A record 202.131.155.153.
10. http://web.archive.org/cdx/search/cdx?collapse=urlkey&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&output=json&url=rms.jaipur.manipal.edu/* : root, Error.aspx, WebResource.axd records.
11. https://web.archive.org/web/20240322052206/https://rms.jaipur.manipal.edu/ : archived homepage with February 2024 DBT-Chemical Engineering notice.
12. https://web.archive.org/web/20240828150521/https://rms.jaipur.manipal.edu/Error.aspx : archived generic error page.
13. https://www.jaipur.manipal.edu/online-grevience-registration.php : grievance channels, named officials.
14. http://jaipur.manipal.edu/recognition-accrediation.php : MUJ established by Act No. 21 of 2011, UGC Act section 22.
15. https://rms.manipal.edu/PublicationEntry/Reports/Login.aspx : publication route with generic error wording.

## ACTIONABLE LEADS
- Passive route inventory from archive: Error.aspx, WebResource.axd, Styles/Style.css, image assets; watch the current route tree via indexing only.
- Watch the login flow passively for any login.microsoftonline.com redirect, given the central RMS Outlook credential statement.
- Cross-check whether the Jaipur RMS and central RMS share branding and mailboxes; ownership of the Jaipur tenant is unconfirmed.
- Confirm CDN and proxy placement against SLCM in an internal inventory; no public evidence exists.
- Later archive checks can show notice continuity; the current page shows April and May 2025 notices.
- Use the grievance page contacts only as institutional escalation, not as RMS-specific evidence.

## FLAGS
- "Result Management System" hypothesis: unsupported, report warns against publishing it.
- Outlook credential wording comes from rms.manipal.edu, not the Jaipur host; protocol unknown for both.
- Ibus is network attribution only; "Ibus Jaipur ISP" is shorthand, physical location not proven.
- IPinfo Delhi geolocation is database output, not proof of server location.
- Web Forms-style assessment is mid-high confidence on family, not version.
- BGP view "hosted-domain count 0" is tool output; not evidence about virtual hosts.
- Error.aspx archive shows only that the route existed; no current behavior can be inferred.

## COVERAGE
- Chars read: 31,637; lines 219; truncated false; EOF confirmed.

---

## w3-11-helpdesk-jaipur.digest

## REPORT
Source file: w3-11-helpdesk-jaipur.md (reconstructing the MUJ helpdesk host from public signals)

## ANSWER SUMMARY
- helpdesk.jaipur.manipal.edu is NXDOMAIN now. dns.google returns status 3 for both A and CNAME queries, no answer, SOA authority for manipal.edu.
- Two crt.sh certificates exist for the exact hostname, Entrust DV TLS Issuing RSA CA 2, CT entries 2026-01-08 09:35:53-54 UTC, validity 2026-01-08 to 2027-01-08. Cert IDs 23628924661 and 23628923708.
- All tested content archives are empty for the target: Internet Archive CDX and availability API, Common Crawl 2026 collections, URLScan, Mnemonic passive DNS.
- Vendor attribution is unresolved. osTicket is proven only for the separate MUCM host helpdesk.manipal.edu.my, not for the MUJ hostname.
- MUJ official FAQ and ICT documents confirm SLCM and support contacts (dms@, ams@, it.support@jaipur.manipal.edu, helpline 0141-3999100) but never mention the helpdesk hostname or a ticketing system.
- Verdict: likely MUJ-related hostname prepared for TLS around 2026-01-08; application identity, vendor, and production activation are unproven.

## KEY FACTS
- https://dns.google/resolve?name=helpdesk.jaipur.manipal.edu&type=A - current A query is NXDOMAIN, no answer.
- https://dns.google/resolve?name=helpdesk.jaipur.manipal.edu&type=CNAME - current CNAME query is NXDOMAIN, no target recovered.
- https://crt.sh/?q=%25.helpdesk.jaipur.manipal.edu&output=json - the only strong target signal: two exact-host CT records logged 2026-01-08.
- https://web.archive.org/cdx/search/cdx?url=helpdesk.jaipur.manipal.edu%2F*&output=json&fl=timestamp%2Coriginal%2Cstatuscode%2Cmimetype%2Cdigest%2Clength - empty array, no Wayback captures in tested views.
- https://archive.org/wayback/available?url=helpdesk.jaipur.manipal.edu%2F&timestamp=20260108 - no archived snapshot for the certificate date.
- https://urlscan.io/api/v1/search/?q=domain%3Ahelpdesk.jaipur.manipal.edu - zero URLScan results, total 0.
- https://api.mnemonic.no/pdns/v3/helpdesk.jaipur.manipal.edu - passive DNS count 0, empty data array.
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - official FAQ: registration link, Outlook ID password, AMS/DMS/IT Infra escalation contacts.
- https://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf - SLCM replaces AMS; attendance, marks, results, circulars; no helpdesk product named.
- https://helpdesk.manipal.edu.my/login.php - MUCM comparator with osTicket footer and Microsoft Work or School sign-in wording.
- https://www.jaipur.manipal.edu/administration-it.php - MUJ IT landscape page; Microsoft services, ERP, mixed in-house and outsourced support.
- https://urlscan.io/domain/mujslcm.jaipur.manipal.edu - SLCM scan records with IIS 10.0, AS8075 Microsoft, Azure DNS nameservers.
- https://www.onlinemanipal.com/help-center - Online Manipal help center with helpdesk@mujonline.edu.in and +91-7996 600 444.
- https://support.freshdesk.com/support/solutions/articles/37590-set-up-a-custom-portal-url-and-verify-dns - Freshdesk custom-URL capability; generic, not target evidence.

## ACTIONABLE LEADS
- Preserve cert IDs 23628924661 and 23628923708; poll crt.sh periodically for renewed certificates on the exact hostname.
- Re-run dns.google A and CNAME checks on a schedule to catch re-publication of the hostname.
- Review newly published official MUJ documents (FAQ, ICT lists, contact pages) for a direct helpdesk URL.
- Keep passive only: no login, no ticket creation, no endpoint enumeration, no origin discovery; MUJ IT policy governs information assets.
- Retain the hostname as an unresolved historical asset, not a confirmed vulnerability or ticketing platform.

## FLAGS
- Certificate existence proves CT logging only, not that a listener ever served traffic.
- NXDOMAIN at one resolver is a point-in-time observation, not proof of global DNS state or deletion cause.
- Freshdesk and Zendesk appear only as generic vendor capabilities; citing them as candidates is not target evidence.
- crt.sh exact query for mujslcm returned 404 (ref 23 in report); that is an unavailable result, not proof of absence.
- Common Crawl collection CC-MAIN-2026-18 was unavailable; it cannot count as evidence either way.
- Report is AI deep-research output; every claim needs independent verification before use.

## COVERAGE
Read 27,094 chars (204 lines), single pagination pass, EOF confirmed (truncated false).

---

## w3-12-npfslcm.digest

## REPORT
Source file: w3-12-npfslcm.md (MUJ SLCM and NoPaperForms evidence-bounded risk map)

## ANSWER SUMMARY
- CT shows npfslcm.jaipur.manipal.edu as certificate name_value on a record whose common name is mujslcm.jaipur.manipal.edu, Entrust OV CA, validity 2025-03-07 to 2025-12-22, logged 2025-11-16.
- admissions.jaipur.manipal.edu CNAMEs to jaipurmanipal.nopaperforms.com, which resolves through prodvpc-web-lb4-593721465.ap-south-1.elb.amazonaws.com to 65.1.79.226, 13.206.4.210, 65.0.244.41.
- SLCM = Student Life Cycle Management per MUJ ICT list; it replaced the older Academic Management System.
- "npf means NoPaperForms" is a medium-confidence inference. No MUJ or vendor source explicitly confirms the acronym.
- NoPaperForms rebranded its flagship product to Meritto on 2023-06-26; older OSINT sources use the old name.
- No credible first-hand public complaint ties a MUJ admissions failure to NoPaperForms. Reviews are mostly positive: G2 4.8/5 (21 reviews), Meritto G2 4.8/5 (20), Software Advice 4.6 (619).
- Public evidence does not prove a direct admissions-to-SLCM data pipeline, database sharing, Microsoft 365 federation, or Akamai in front.

## KEY FACTS
- https://crt.sh/?q=npfslcm.jaipur.manipal.edu&output=json - exact CT records: npfslcm as name_value, mujslcm as common name.
- https://dns.google/resolve?name=admissions.jaipur.manipal.edu&type=CNAME - direct CNAME to jaipurmanipal.nopaperforms.com, TTL 2387.
- https://dns.google/resolve?name=admissions.jaipur.manipal.edu&type=A - resolver chain to AWS ELB hostname and three IPv4s.
- https://www.ipaddress.com/website/admissions.jaipur.manipal.edu - independent DNS lookup page reporting the same CNAME target.
- https://urlscan.io/domain/admissions.jaipur.manipal.edu - domain first observed six years prior, Mumbai GeoIP, Amazon AS16509.
- http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf - defines SLCM and its academic modules.
- https://mujslcm.jaipur.manipal.edu/ - login boundary with @muj.manipal.edu identity domain; no SSO protocol visible.
- http://api.ssllabs.com/api/v3/analyze?all=done&fromCache=on&host=mujslcm.jaipur.manipal.edu&maxAge=168 - point-in-time scan showing Microsoft-IIS/10.0 and ASP.NET MVC 5.3.
- http://developer.nopaperforms.com/ - vendor API docs: Lead, Opportunity, Activity, Form, Master Data, Payment, Application areas.
- https://www.meritto.com/application-automation/admission-form-payment-manager - vendor payment claims including split payment and CSV export.
- https://www.nopaperforms.com/press-release/nopaperforms-rebrands-its-flagship-product-to-meritto-signifying-expanding-platform-and-markets - documents the June 2023 rebrand.
- https://login.nopaperforms.io/privacy-policy - vendor collection statement; no MUJ-specific admissions privacy notice exists in reviewed pages.
- https://www.g2.com/products/meritto/reviews - 4.8/5 from 20 reviews with usability and reporting criticisms.
- https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/Subdomain_takeover - MDN CNAME deprovisioning guidance behind the monitoring recommendation.

## ACTIONABLE LEADS
- Set up CT and DNS monitoring: watch for npfslcm re-issuance and for drift of the admissions CNAME target.
- Request from the owner a sanctioned data-flow diagram: fields, controller and processor roles, retention, payment tokenization, SSO protocol.
- Build a passive asset register; do not test credentials, enumerate endpoints, or attempt any takeover.
- Watch the rebrand split: search both NoPaperForms and Meritto names when correlating historical records.
- Do not claim subdomain takeover: the CNAME chain currently resolves through a live-looking path.

## FLAGS
- Hudson Rock ref (11486 infostealer credentials for nopaperforms.com) sits in references but is never analyzed in the body; treat as unverified third-party claim.
- Two shodan.io host links (98.70.14.50, 20.244.94.89) appear malformed in references with no body discussion; exclude as evidence.
- One reference is a goo.gl redirect URL (Google Lens link); junk, ignore.
- CT record entered 2025-11-16 with validity starting 2025-03-07 is an unusual backdated window; do not infer issuance date from validity start.
- The admissions CNAME proves DNS routing, not data flow, contract, or database ownership.
- Microsoft 365 as SLCM identity provider is not established; the supplied premise is unverified.
- Report is AI deep-research output; all claims need independent verification.

## COVERAGE
Read 42,098 chars (351 lines), single pagination pass, EOF confirmed (truncated false).

---

## w3-13-lms-brightspace-muj.digest

## REPORT
Source file: w3-13-lms-brightspace-muj.md (MUJ SLCM and Brightspace public-exposure assessment)

## ANSWER SUMMARY
- MUJ learning login is a D2L Brightspace tenant. learning.onlinemanipal.com CNAMEs to muj.brightspace.com; learner-mahe.onlinemanipal.com CNAMEs to manipalonline.brightspace.com; both A responses share IPs 13.55.178.159 and 15.134.178.12.
- The login page shows "Powered by D2L Brightspace" for Manipal University Jaipur Centre for Distance and Online Education.
- Microsoft metadata for muj.manipal.edu is public: tenant 27282fdd-4c0b-4dfb-ba91-228cd83fdf71 with WS-Fed and OIDC endpoints. No proof Brightspace uses that tenant as relying party.
- The App Store callback-failure claim is unverified. Play store search returned only Manipal Hospitals apps, no Online Manipal education app.
- The MUJ iLearn page shows an OTP flow; it names no Microsoft, Entra ID, Brightspace, SAML, or OIDC.
- The supplied SLCM stack fingerprint (ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai) is not confirmed by Wappalyzer, urlscan, or raw markup checks.
- Only one Brightspace CVE found: CVE-2021-43129, quiz right-click control bypass, CVSS 6.5, medium. MUJ exposure unknown.
- D2L documents a broad permissioned API surface (users, grades, content, org units, courses, calendar) with OAuth scopes.

## KEY FACTS
- https://learning.onlinemanipal.com/d2l/home/14042 - public login page, "Powered by D2L Brightspace" label.
- https://dns.google/resolve?name=learning.onlinemanipal.com&type=CNAME - CNAME to muj.brightspace.com, TTL 3600.
- https://dns.google/resolve?name=learner-mahe.onlinemanipal.com&type=CNAME - CNAME to manipalonline.brightspace.com, TTL 600.
- https://dns.google/resolve?name=muj.brightspace.com&type=A - A records 13.55.178.159 and 15.134.178.12.
- http://login.microsoftonline.com/muj.manipal.edu/.well-known/openid-configuration - public tenant metadata and OIDC endpoints.
- http://login.microsoftonline.com/muj.manipal.edu/federationmetadata/2007-06/federationmetadata.xml - public WS-Federation metadata for the namespace.
- https://muj.onlinemanipal.com/ilearn-login - lead-capture and OTP flow page; no SSO vendor named.
- https://muj.onlinemanipal.com/privacy-policy - MUJ policy: AWS hosting in India and Singapore; SPDI categories; sharing with vendors.
- https://nvd.nist.gov/vuln/detail/CVE-2021-43129 - the relevant Brightspace CVE, CVSS 6.5.
- https://app.opencve.io/cve/?product=brightspace&vendor=d2l - OpenCVE shows one matching CVE, updated 2024-11-21.
- https://docs.valence.desire2learn.com/basic/oauth2.html - OAuth 2.0 authorization-code flow and scope model.
- https://community.d2l.com/brightspace/kb/articles/23533-d2l-vulnerability-disclosure-policy - customer-instance testing needs customer authorization.
- https://community.d2l.com/brightspace/kb/articles/4537-sessions-and-system-access-data-sets - Session History and System Access data set definitions.
- https://www.d2l.com/cloud - D2L says AWS is primary cloud provider and D2L handles LMS updates.
- https://play.google.com/store/search?q=Online%20Manipal&c=apps&hl=en_IN - store search found no Online Manipal education app.

## ACTIONABLE LEADS
- Ask the service owner for the sanctioned Brightspace relying-party configuration, redirect URI inventory, claims mapping, MFA policy, deprovisioning process.
- Ask whether the quiz "Disable Right Click" setting is used so CVE-2021-43129 remediation can be confirmed through the managed service.
- Run a team exercise on a local mock Brightspace integration; no token requests against the MUJ tenant.
- Re-capture DNS snapshots for both aliases over time; do not infer tenant identity from shared IPs.
- Keep the App Store callback allegation labeled unverified until a real listing or review is found.

## FLAGS
- Supplied Akamai/IIS/.NET fingerprint is unverified; collected Wappalyzer and markup evidence showed none of it.
- /d2l/home/14042 and /d2l/home/14201 paths are not proof those numbers are course or tenant IDs.
- Reference 42 is a Manipal Hospitals YouTube video mislabeled as a passive raw-markup check; discard as evidence.
- References 43 and 44 (Supabase callback docs) are unrelated to MUJ; ignore.
- Shared Brightspace IPs and public tenant metadata support inference only, not confirmed SSO or shared tenancy.
- Report is AI deep-research output; all claims need independent verification.

## COVERAGE
Read 30,487 chars (226 lines), single pagination pass, EOF confirmed (truncated false).

---

## w3-14-mujslcm-parent-level.digest

## REPORT
Source file: w3-14-mujslcm-parent-level.md (MUJ SLCM hostname attribution and exposure report)

## ANSWER SUMMARY
- Parent mujslcm.manipal.edu resolves to 202.131.155.151 (A only, TTL 300). No AAAA, CNAME, HTTPS, TXT, MX, or NS answers appear in queried responses.
- The Jaipur child mujslcm.jaipur.manipal.edu is the officially documented SLCM registration link in the MUJ FAQ.
- Child scans across Nov 2024, Jan 2026, Jun 2026 return HTTP 200 with x-aspnetmvc-version 5.3, x-aspnet-version 4.0.30319, Microsoft-IIS/10.0 (IIS 8.5 in 2024), IP 98.70.14.50 (202.131.155.150 in 2024).
- Akamai is not demonstrated in any public scan. Observed network is Microsoft IIS and AS8075.
- A passwordreset.microsoftonline.com link titled "Forgot Password?" exists on the child; that is Microsoft-linked recovery, not proof of Microsoft 365 federation.
- Parent has zero URLScan results, zero Wayback captures, empty Certificate Spotter result. Child has Wayback 200 captures from 2025-01-10 and 2025-05-27.
- Verdict: parent is an unattributed DNS-present asset, best working hypothesis orphaned or legacy infrastructure; not proven to be old SLCM, backup, alias, or squat.

## KEY FACTS
- https://dns.google/resolve?name=mujslcm.manipal.edu&type=A - parent A record 202.131.155.151.
- https://dns.google/resolve?name=mujslcm.manipal.edu&type=AAAA - no AAAA answer, only SOA authority for manipal.edu.
- https://urlscan.io/api/v1/search/?q=domain:mujslcm.manipal.edu&size=100 - parent URLScan results: [], total 0.
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - first-party source naming mujslcm.jaipur.manipal.edu as the SLCM registration link.
- https://urlscan.io/result/019ed038-c4af-765c-9499-2da69a77e30a/ - Jun 2026 scan: MVC 5.3, ASP.NET 4.0.30319, IIS 10.0, 98.70.14.50.
- https://urlscan.io/result/019bc028-d1ec-72f5-b0df-647554467edb/ - Jan 2026 scan: IIS 10, AS8075, Forgot Password link to Microsoft.
- https://urlscan.io/result/17a4443c-7b48-46f7-9b83-c207114b958f/ - Nov 2024 scan: port 122, HTTP 200, IIS 8.5, 202.131.155.150.
- https://web.archive.org/cdx/search/cdx?collapse=urlkey&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&output=json&url=mujslcm.jaipur.manipal.edu/* - child 200 captures 20250527044058 and 20250110135954.
- https://api.hackertarget.com/reversedns/?q=202.131.155.151 - parent reverse DNS maps to convergentindia.com naming.
- https://api.hackertarget.com/reversedns/?q=202.131.155.150 - sibling historical address maps to the same Convergent India pattern.
- https://slcm.manipal.edu/ - separate MAHE-branded portal, not usable as MUJ parent evidence.
- https://crt.sh/?q=mujslcm.manipal.edu&output=json - returned 404; treat as unavailable query, not proof of certificate absence.
- https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-framework - .NET Framework 4.0 end of support 2016-01-12; header alone does not prove runtime.
- http://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf - NIST CSF 2.0 inventory requirements behind the governance recommendation.
- https://www.cisa.gov/resources-tools/resources/secure-by-design - owner accountability guidance for reducing exposure.

## ACTIONABLE LEADS
- Owner-side: reconcile DNS zone records, certificates, load balancer and CDN configs, and CMDB entries for both hostnames.
- Classify the parent as "unattributed - DNS present - application and ownership unconfirmed" in the asset register.
- Passive follow-up: re-check parent HTTP/HTTPS reachability and certificate issuance over time; do not fuzz or probe.
- If the parent is retired, remove stale DNS and certificates after dependency review; if required, publish an owner-approved canonical URL.
- Do not copy the child's MVC/IIS fingerprint onto the parent; the parent has no recovered application fingerprint.

## FLAGS
- Child moved from 202.131.155.150/IIS 8.5 (2024) to 98.70.14.50/IIS 10 (2026); observed change, not proof of migration.
- .150/.151 adjacency and shared reverse-DNS naming are suggestive only; not proof of common ownership.
- The Akamai assertion from the supplied research brief is unverified by every cited public source.
- Header 4.0.30319 is not proof of exact .NET Framework release; Microsoft lists 4.0 as EOL 2016-01-12.
- Reference 24 (learn.microsoft.com ASP.NET MVC overview) returned 404; dead reference in the report.
- Report is AI deep-research output; all claims need independent verification.

## COVERAGE
Read 34,839 chars (201 lines), single pagination pass, EOF confirmed (truncated false).

---

## w3-15-dms-muj.digest

## REPORT
Source file: w3-15-dms-muj.md (MUJ SLCM and DMS public surface and operations report)

## ANSWER SUMMARY
- MUJ's first-year guide calls SLCM a one-stop academic information platform; onboarding runs through mujslcm.jaipur.manipal.edu, credentials go to the personal Gmail supplied at admission, and OTP verification of the parent mobile enables Parent login.
- The official SLCM FAQ routes unresolved AMS login problems to dms@jaipur.manipal.edu or ams@jaipur.manipal.edu, with named AMS staff and extensions (Rahul Kumawat 784, Dinesh Sain 738, Rithik Chaudhary 481). DMS as an escalation contact is high confidence.
- dms.jaipur.manipal.edu has Wayback captures from 2018 through 2022, including IIS Windows Server defaults and 2022 GenerateCaptcha.aspx records.
- dmsmuj.jaipur.manipal.edu has a Dec 2022 root capture reading "MUJ API TESTING!" and an Aug 2022 loginForm.aspx capture titled "MU SLcM".
- Central dms.manipal.edu is a live Document Management System sign-in shell with captcha and @manipal.edu branding; no proof it is the MUJ AMS/SLCM service.
- A 2026-06-16 urlscan record for mujslcm reports HTTPS-only redirect, HTTP 200, Microsoft-IIS/10.0, 98.70.14.50, AS8075. MVC 5.3, .NET Framework 4.x, and Akamai are not established.
- The Office 365 SOP (v1.0, June 2025) documents mandatory MFA but never mentions SLCM or AMS. urlscan has zero records for either DMS Jaipur hostname.

## KEY FACTS
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - FAQ: AMS login failures go to dms@ and ams@; Outlook ID password; IT Infra ext 144; Admissions ext 142/257/297.
- https://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf - official SLCM purpose and onboarding workflow with OTP parent verification.
- https://dms.manipal.edu/ - live central Document Management System sign-in shell with captcha.
- https://web.archive.org/web/20221210094938id_/http://dmsmuj.jaipur.manipal.edu/ - archived root reading "MUJ API TESTING!".
- https://web.archive.org/web/20220815043240id_/https://dmsmuj.jaipur.manipal.edu/loginForm.aspx - archived login form titled MU SLcM.
- https://web.archive.org/web/20180806141738id_/http://dms.jaipur.manipal.edu:80/ - earliest 2018 IIS Windows Server capture.
- https://web.archive.org/web/20220418023042id_/http://dms.jaipur.manipal.edu/ - 2022 root capture, HTTP 200 text/html.
- https://web.archive.org/cdx/search/cdx?url=dms.jaipur.manipal.edu/GenerateCaptcha.aspx*&output=json&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype - captcha route captures from 2022.
- https://crt.sh/?q=%25.jaipur.manipal.edu&output=json - CT names include dms, www.dms, dmsmuj, muj.slcm, and mujslcm Jaipur hostnames.
- http://urlscan.io/api/v1/search?q=domain:mujslcm.jaipur.manipal.edu - Jun 2026 scan: HTTPS redirect, 200, IIS 10.0, 98.70.14.50, AS8075.
- https://urlscan.io/api/v1/search/?q=domain:dms.jaipur.manipal.edu - zero public urlscan records for the MUJ DMS hostname.
- https://urlscan.io/api/v1/search/?q=domain:dmsmuj.jaipur.manipal.edu - zero public urlscan records for dmsmuj.
- https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf - Office 365 setup SOP, mandatory MFA, no SLCM or AMS wording.
- https://jaipur.manipal.edu/about-directorate-of-academic-administration.php - directorate page names an AMS Office and dms@ but never expands DMS.
- https://web.archive.org/cdx/search/cdx?url=dms.jaipur.manipal.edu/&output=json&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype - repeated root captures 2018 to 2022.

## ACTIONABLE LEADS
- Inventory the three DMS surfaces separately: dms.manipal.edu, dms.jaipur.manipal.edu, dmsmuj.jaipur.manipal.edu.
- Passive follow-up on current status of both Jaipur DMS hostnames: DNS, certificate issuance, archive re-checks.
- Ask the owner whether the dmsmuj test host was decommissioned and whether DMS has an official expansion for MUJ Jaipur.
- Map support routes to business functions (Admissions, IT Infra, AMS, DMS) in the asset register; route suspected issues through MUJ published security contact.
- Do not interact with captcha or login surfaces; all findings so far are informational, no verified vulnerability.

## FLAGS
- "MUJ API TESTING!" is test wording; weak evidence of any production integration.
- crt.sh exact-host query for dmsmuj returned a 404-titled page while the wildcard query showed DMS names; an output distinction, not a contradiction, but cite the wildcard query.
- Central DMS calling itself Document Management System does not prove the Jaipur mailbox or hostname means the same.
- The Digital Media Services expansion is unsupported; keep it as a hypothesis only.
- MVC 5.3, .NET Framework 4.x, and Akamai are unconfirmed by cited evidence; only IIS 10 is observed.
- Report is AI deep-research output; all claims need independent verification.

## COVERAGE
Read 32,747 chars (230 lines), single pagination pass, EOF confirmed (truncated false).

## 6.4 Wave 5: the gap register answered

25 gap-derived reports, 1,186,037 characters, fired to cover what the campaign never
touched. The tool matrices are omitted here (472 tool rows live in the source digest); what
follows is the per-gap verdict and the counts.

| brief | chars | tool rows | no-tool gaps | build candidates |
|---|---:|---:|---:|---:|
| w5-g-01-reflected-stored-and-dom-cross-site-scripting | 47,244 | 38 | 0 | 0 |
| w5-g-02-sql-and-nosql-injection | 50,978 | 14 | 11 | 0 |
| w5-g-03-server-side-request-forgery-and-internal-plane-a | 44,561 | 16 | 7 | 0 |
| w5-g-04-cross-site-request-forgery-under-authentication | 40,569 | 30 | 0 | 0 |
| w5-g-05-client-side-and-browser-layer-classes-cors-postm | 38,004 | 14 | 0 | 0 |
| w5-g-06-xml-external-entities-and-file-format-parsing | 49,758 | 19 | 0 | 0 |
| w5-g-07-server-side-template-injection-and-expression-la | 41,731 | 20 | 0 | 0 |
| w5-g-08-request-smuggling-and-cache-poisoning-at-the-azu | 45,689 | 15 | 0 | 0 |
| w5-g-09-business-logic-state-machines-and-race-condition | 49,951 | 20 | 10 | 0 |
| w5-g-10-deserialisation-beyond-machinekey-and-viewstate | 34,742 | 10 | 0 | 0 |
| w5-g-11-file-inclusion-path-traversal-and-upload-bypass | 36,576 | 12 | 1 | 0 |
| w5-g-12-access-control-beyond-the-planned-idor-sweep | 33,319 | 8 | 0 | 7 |
| w5-g-13-graphql-and-api-shape-abuse | 49,556 | 27 | 10 | 0 |
| w5-g-14-authentication-and-token-abuse-beyond-the-login- | 48,127 | 11 | 8 | 0 |
| w5-g-15-web-application-firewall-and-edge-control-bypass | 50,670 | 22 | 0 | 0 |
| w5-g-16-subdomain-takeover-verification-to-the-provider- | 49,940 | 16 | 0 | 6 |
| w5-g-17-clickjacking-with-real-frame-rendering | 49,831 | 26 | 0 | 0 |
| w5-g-18-the-azure-control-plane-under-the-app | 53,218 | 26 | 0 | 8 |
| w5-g-19-the-entra-and-m365-identity-control-plane | 48,103 | 0 | 8 | 0 |
| w5-g-20-detection-engineering-and-defensive-validation-f | 48,629 | 17 | 8 | 0 |
| w5-g-21-data-protection-law-and-the-reporting-chain-as-t | 53,104 | 25 | 0 | 8 |
| w5-g-22-supply-chain-and-dependency-handling-for-a-net-a | 53,717 | 28 | 12 | 0 |
| w5-g-23-mobile-client-static-analysis | 52,956 | 22 | 0 | 10 |
| w5-g-24-social-engineering-and-human-vector-classes | 56,147 | 15 | 9 | 8 |
| w5-g-25-fix-verification-and-the-retest-loop | 58,206 | 21 | 0 | 0 |

### Per-gap verdicts

- verdict head: **Confidence: High (overall).** Specifically:
- verdict head: **Verdict: The SQL/NoSQL injection campaign status is still ABSENT, and no vulnerability conclusion is justified.**
- verdict head: **Confidence**:
- verdict head: The MUJ SLCM campaign should continue to be HELD at BLOCKED-AUTH. The pre-auth recon chain has produced a complete technique universe, a tool inventory of 25 entries that materially exercise the class, and a defensible detection counterpart map -- and none of those steps require crossing the agency 
- verdict head: **Finding status:** No client-side or browser-layer vulnerability is established. CORS, postMessage, prototype pollution, and CSP are currently **unassessed in the campaign**, not proven absent.
- verdict head: **Confidence**: HIGH that the technique universe, tool inventory, manual method, detection counterpart, and no-tool gaps are accurate for the *public information*. MEDIUM that the inferences specific to the live target (e.g., the `enc` oracle being a parser entry point) hold once the signed scope le
- verdict head: **Campaign status: TO BEAT ABSENT -- ACHIEVABLE WITH THIS PLAYBOOK (confidence: HIGH).**
- verdict head: **Confidence: high (planning-/tooling-level) -- moderate (target-specific assertions).**
- verdict head: **Verdict:** The next MUJ SLCM campaign should prioritize authenticated business-logic, state-machine, idempotency, and race-condition testing over additional unauthenticated scanning. Public sources confirm that SLCM is an official student portal and login surface [40][12], and OWASP/PortSwigger so
- verdict head: **Confidence: HIGH** that the campaign access surface stands at:
- verdict head: **Confidence**: **medium** on the technique universe (high on the inventoried tools, high on the OWASP / PAT coverage, medium on MUJ-specific IIS-10 idiosyncrasies without source access); **high** on the policy blocker (GET-only is documented and reproducible from the campaign [Recap]); **medium** o
- verdict head: **Verdict: Authorization assurance is currently unproven, not demonstrably vulnerable.** Confidence is **high** that BOLA, BFLA, BOPLA, role escalation, tenant isolation, workflow authorization, method authorization, and token-context enforcement are the correct technique families to cover. Confiden
- verdict head: | Dimension | Verdict |
- verdict head: **Confidence: High for the technique universe and tool capability mapping; medium for prioritization against the reported MUJ architecture; low for any claim that MUJ is currently vulnerable.**
- verdict head: Confidence levels use: **HIGH** = multi-source verified; **MEDIUM** = single-source verified + multi-source consistent inference; **LOW** = best-effort inference from one source.
- verdict head: **Verdict: PARTIAL - fingerprint/dangling-CNAME evidence only.**
- verdict head: Confidence: high on the tool landscape and citation matrix; medium on the same-origin traversal path; medium-on the DoubleClickjacking verifier. All evidence used in the report comes from primary sources read end-to-end (page metadata + content segments from `extract()` and `llm_query()`); every gap
- verdict head: **Verdict: The Azure control-plane campaign is ABSENT, not clean and not compromised.**
- verdict head: **Verdict: DETECTION READINESS UNPROVEN - CAMPAIGN STATUS ABSENT.**
- verdict head: **Verdict: PARTIAL technically, but LEGALLY UPGRADED and ready for an authorized second phase.**
- verdict head: **Overall confidence in the technique universe and tool catalog: High.** The core capabilities, formats, source-mapping limits, signature behavior, .NET/NuGet input types, and SBOM functions are grounded in official Microsoft, OWASP, vendor, or project documentation cited above. The catalog distingu
- verdict head: **Overall confidence: HIGH in the methodology and authorization boundary; LOW in any SLCM_APP-specific security conclusion because the APK has not yet been statically analyzed.**
- verdict head: **Overall confidence: High for the technique taxonomy, safety boundary, and detection architecture; Medium for tool inventory completeness and current commercial licensing details.** The public sources clearly establish the T1566, T1598, and T1204 universe, the distinction between delivery, informat
- verdict head: **Verdict: CAMPAIGN STATUS TO BEAT remains ABSENT.** The available facts show a useful initial non-destructive baseline, but they do not yet constitute a retest harness or a university-acceptable closure system. The immediate decision is to build the P0 ReTestSpec, safe runner, response fingerprint

# 7. Coverage: what was never tested, named

The research layer graded the campaign against an external field universe and produced 25
gaps. That register is the honest boundary of this work. Named plainly, the campaign holds
no verified finding for any of the following:

- cross-site scripting (reflected, stored, DOM), SQL and NoSQL injection
- server-side request forgery and the internal plane
- cross-site request forgery under authentication
- client-side and browser-layer classes (CORS, postMessage, DOM clobbering)
- XML external entities and file-format parsing
- server-side template injection and expression language
- request smuggling and cache poisoning at the edge
- business-logic state machines and race conditions
- deserialisation beyond the key-and-viewstate question
- file inclusion, path traversal and upload bypass
- access control beyond the planned IDOR sweep (BOLA, BFLA, property-level)
- GraphQL and API shape abuse
- authentication and token abuse beyond the login form
- WAF and edge-control bypass
- subdomain takeover verification to the provider layer
- clickjacking with real frame rendering
- the Azure control plane under the application
- the Entra and Microsoft 365 identity control plane
- detection engineering and defensive validation
- data-protection obligations and the reporting chain
- supply chain and dependency handling for the .NET and front-end stack
- mobile client static analysis
- social engineering and human-vector classes
- fix verification and the retest loop
- anything at all behind the login: post-authenticated surface is entirely unwritten

Also untested by name: rate limiting and lockout behaviour, the fee flow, the document
upload and download handlers, role switching between student, parent and staff, session
fixation and logout invalidation, and the two sibling or test instances reachable in the
estate.

# 8. Evidence and how to re-verify

Every verified row above names a file in `recon/`, `recon/layers-2026-09-13/` or `findings/`.
The evidence index inside the layer map (section 4) is the map from claim to capture.

To re-check the two cheapest load-bearing claims, both single requests:

1. The `enc` ladder: an invalid-base64 value returns HTTP 500 with a 4,942-byte body and
   FormatException; a valid-base64 but undecryptable value returns HTTP 500 with a
   5,084-byte body and CryptographicException.
2. Port posture: 443 open, 80 and 8080 filtered.

If either has changed, the layer map needs an amendment, not a quiet edit. That rule is the
reason this file lists corrections next to findings instead of replacing them.

# Appendix D: the authorized-phase test plan (unchanged)

Included because it is the next action and it is non-destructive by construction. It runs
only under a signed scope letter and a dedicated test account.

Status: PRE-AUTH phase done (recon). AUTH phase needs team test credentials.
Severity scale: P1 critical, P2 high, P3 medium, P4 low.

## Principles (from README, binding)

- Non-destructive only. No data modification, no deletion, no DoS, no
  volume spraying. Low request rates, manual pacing.
- One throwaway test account (team-provided) for all auth tests.
- Anything live-exploitable: minimal PoC on our own account, document,
  STOP, report. Never chain further.
- Every finding: repro steps, expected vs actual, evidence saved.

## Phase 1: PRE-AUTH (done  -  see FINDINGS-W0.md)

- F1 verbose YSOD (missing CSRF on login POST) P3
- F2 trace.axd 403 (exists, restricted) P3
- F3 version headers (IIS/ASP.NET/MVC versions exposed) P4
- F4 jQuery 1.10.2 legacy client lib P4
- F5 alternate SLCM host (intel, out of scope to test) INFO
- Clean: anti-CSRF enforced, no user enum via login response diff,
  server-side validation active, no open redirect observed (enc param),
  verbs locked, ELMAH 404, centralized auth gate.

## Phase 2: AUTH-CONTEXT (needs credentials)

Priority order (class -> test -> expected evidence):

1. IDOR sweep (P1). After login: enumerate own resources by ID:
   notifications, documents, fee receipts, timetable views, marks API.
   Try neighbor IDs. Evidence: another student's data visible.
   Where: /Student/*, /api/*, document download handlers.
2. Role/privilege boundaries (P1). EmailFor/LoginFor hidden fields:
   student vs parent vs staff. Does a student token access staff
   endpoints? Test with student account against /Staff/*-guessed URLs.
3. Session handling (P2). Session cookie flags (Secure? HttpOnly?),
   session fixation (login with pre-set ASP.NET_SessionId value),
   session timeout, concurrent sessions, logout invalidation.
4. CSRF on post-login state changes (P2). Any action without the
   __RequestVerificationToken check: profile update, settings.
   Test with token removed + cookie fixed.
5. File upload (P2). Document upload module: extension filtering,
   content-type trust, filename handling, path traversal on download.
   Upload only inert test files on our own account.
6. Fee module (P2). Only if team approved: inspect POST fields for
   tamperable amount/currency. Do NOT submit a real payment.
   Document field names from page source, no modification.
7. Rate limiting / lockout (P3). NEVER against real accounts: only our
   throwaway account, small batches (10-20 attempts), log server
   responses (lockout message? 429? nothing?).
8. Parameter tampering on own data (P3). Marks display? No write
   attempts. Only reads with modified IDs.
9. Path traversal / IIS quirks (P3). Dot-segment and backslash URL
   variants on document URLs (IIS normalization), short-name 8.3 scan
   is active-ish: keep to 10-20 requests, skip if WAF blocks.
10. Header/behavior re-checks after auth (P3). Cache-Control on
    student pages (private data caching), Referrer leakage of tokens.

## Phase 3: DISCLOSURE (fixes + report)

- All findings: repro, impact, proposed fix, screenshots/artifacts.
- Disclosure path: the engagement owner -> university nodal officer; CC AMS team
  (dms@ / ams@jaipur.manipal.edu) and IT Infra (it.support@...);
  CERT-In only if university does not respond in 90 days.
- No public disclosure ever without written university consent.

## Out of bounds (do not touch)

- muj.slcm.jaipur.manipal.edu, mujerp, mujone, rms, helpdesk,
  admissions, any other hostname. One target only.
- slcm.manipal.edu and any sibling campus systems (reference only).
- Microsoft 365 tenant: no password resets, no MFA toggling, no
  enumeration beyond public discovery, no messaging.
- Third-party services (NoPaperForms, Brightspace, Webex): read-only.
