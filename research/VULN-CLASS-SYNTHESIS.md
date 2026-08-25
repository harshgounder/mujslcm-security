# VULN-CLASS SYNTHESIS

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

1. Akamai presence. w2f-01, w2f-02, w2f-03, w2f-04 run on the user-supplied "behind Akamai" premise; w2x-00, w2f-06, w2c-11, w2c-22, w2f-11, w2c-09 contradict it with a direct A record, AS8075 ownership, and no edge CNAME. w2f-12 and w2c-08 keep attribution unresolved pending telemetry. Resolution: treat Akamai as an unverified claim and test against Microsoft/Azure topology (w2x-00).
2. CVE-2020-11022 range for jQuery 1.10.2. w2x-00 counts it in range (NVD record >=1.2, <3.5.0); w2f-03 excludes it (current CVE.org record >=1.12.0, <3.5.0). Both cite canonical records. Resolve before any final CVE count (w2f-03 FLAGS, w2x-00 FLAGS).
3. KEV status of CVE-2020-11023. w2f-03 states none of the four jQuery CVEs appears in the CISA KEV catalog; w2x-00 states CISA added CVE-2020-11023 to KEV on 2025-01-23, citing the CISA alert. Direct conflict, both dated 2026-08. Re-check KEV before citing either.
4. Shared password claim. w2c-05 and w2c-03 attribute "password is the official Outlook ID" to the SLCM FAQ; w2f-09 says no citable FAQ copy was found and treats it as a supplied premise; w2c-07 could not independently locate the sentence. w2c-05 also did not re-fetch the PDF. Resolution: re-fetch FaQs-SLCM.pdf once before relying on the claim (w2f-09, w2c-05 FLAGS).
5. jQuery version inventory. w2f-05 shows jquery 3.4.1 inside the Keen plugin bundle while w2x-00 and w2f-03 key on jquery-1.10.2.min.js; both archived under the same Keen demo1 tree. Dual load and execution order unresolved (w2f-05).
6. Digest count on disk vs task brief. 35 files exist (22 w2c + 12 w2f + w2x-00) not 34 (21 + 13). w2c-22 exists beyond the stated 21; w2f-12 plus w2x-00 complete the stated 13.
7. Supplied verb observations. w2c-18 reports PUT 411 and OPTIONS/DELETE 404 as supplied but not reproduced; w2f-01 and w2c-18 agree these prove nothing about WebDAV. No cross-digest conflict, but do not cite as findings (w2c-18 FLAGS).

## 4) WHAT TO TEST FIRST (once club test credentials exist)

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