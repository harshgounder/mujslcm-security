# AGGRESSIVE-PLAYBOOK — target-specific methods per gap (auth-club phase)

Methods below are keyed to VERIFIED observations on mujslcm.jaipur.manipal.edu
(see ATTACK-SURFACE-MAP + FINDINGS-W0). Run with club seniors + university
authorization, throwaway accounts only, non-destructive PoCs, stop-and-report
on first proof. Tiers: [P] passive/recon anytime, [A] needs authorization,
[X] do not do on production (lab clone only).

## GAP-1 Verbose YSOD (F1, customErrors off) [A]

- Error-injection ladder to map controllers/actions: bad enc base64 (DONE,
  FormatException), valid-base64 garbage (expect CryptographicException:
  padding/decryption trace, reveals crypto path), oversized form body, wrong
  content types (application/xml POST to /), malformed query on /Home/Index
  params, Unicode overlong routes, doubled slashes, %00 encoded chars,
  .NET path tricks (/. and /.. variations) on /Student/* routes.
- Every 500 body: save raw. Extract: stack frames = internal class names,
  method names, assembly hints; version line; machine name (Common YSOD shows
  Server Name in older ASP.NET); connection strings never in stack, but
  file paths leak app layout.
- RemoteOnly bypass test: customErrors RemoteOnly shows detail to REMOTE
  too from our vantage (we ARE remote). If a future fix flips to RemoteOnly,
  retest with X-Forwarded-For: 127.0.0.1 and Host: localhost to probe
  trust-based bypass. Single requests only.
- Deliverable: controller/action route map from stack traces, patch level
  confirmation, one screenshot per trigger.

## GAP-2 trace.axd 403 (F2) [A]

- 403 = tracing enabled, access-restricted. Test from campus network (club
  lab IP); if IIS restriction is IP-based, campus IP may pass. GET
  /trace.axd with query ?id=0..N once authorized to enumerate request
  traces. Traces include cookies, session IDs, query strings. That is a
  critical leak if reachable.
- Do not brute force id range; probe a handful (0,1,2,10,100).
- Also probe /elmah.axd?Authorization-Failed and /trace.axd?date= variants
  only if the first responds.

## GAP-3 IDOR (P1 class, needs 2 accounts) [A]

- Method: student A logs in, grabs own object URLs (notification IDs,
  document download links, fee receipt IDs, marks views). Swap numeric IDs
  to student B's values. One changed variable, one request. HEAD or small
  Range GET first; stop on first cross-user hit; evidence = both accounts'
  responses side by side.
- Known-surface candidates after auth: /Student/Academic/
  AttendanceSummaryForStudent, TimeTableForStudent, GradesForStudent
  (route NAMES from third-party client code w2c-20 + reports; pre-auth
  302 does NOT prove existence, the catch-all gate redirects every
  <=3-segment path, see REAUDIT-2026-08-25), /Student/Profile,
  document handlers under /Student/ (uploaded docs per onboarding guide),
  /api/* if any appears in post-login traffic.
- Look for GUIDs vs sequential ints vs registration-number-keyed objects
  (reg numbers are public, so regnum-keyed objects are explosive).
- If download handler takes ?f=filename: test traversal with
  filename variants only on OUR OWN docs, never reading others' files.

## GAP-4 Role confusion: EmailFor/LoginFor hidden fields [A]

- Login as student. Replay the POST with LoginFor=Staff or =Parent and
  EmailFor set to a staff email format. Server must re-derive role from
  identity store; if navigation or API responses change, that is a
  privilege boundary finding.
- Test both hostnames' login flows against each other's session values
  (mujslcm vs muj.slcm are sibling surfaces; only with authorization to
  touch the sibling).

## GAP-5 Session handling [A]

- Cookie flags: __RequestVerificationToken HttpOnly only; check Secure on
  the session cookie after login (ASP.NET_SessionId on the MAHE family;
  is there a session cookie on mujslcm after auth?).
- Fixation: before login, set ASP.NET_SessionId=custom value; after login
  check if the SAME value persists (fixation) or rotates (good).
- Role-change rotation: student -> parent mode, does session id change?
- Logout: reuse the session cookie after logout, does it still serve
  pages? (invalidation test)
- Sliding expiry: leave session idle 20-30 min, check timeout behavior.
- All on one throwaway account.

## GAP-6 CSRF on post-login actions [A]

- Find any state-changing action (declarations tick flow per onboarding
  guide Step 7, profile updates, settings). Replay the request WITHOUT the
  __RequestVerificationToken field and with a fixed cookie. If it goes
  through: CSRF.
- Verify the token binds to session (token from session A fails on
  session B) and to user (cross-user token fails).

## GAP-7 File upload surface (onboarding Step 6) [A]

- Upload module accepts PDF (max 1MB) + JPG photo. Test on OUR account:
  - extension bypass: .pdf w/ HTML content, .pdf.aspx, double extension,
    case variants (.PDF), trailing dot, %00, unicode dot (U+FF0E)
  - content-type mismatch, polyglot files
  - filename with ../ to test storage path traversal on the DOWNLOAD
    handler (never request other users' files)
  - stored XSS via filename rendered in document list
  - photo EXIF: GPS/device metadata persists in stored jpg (privacy
    finding for the university, not just the app)
- Any success = report, do not chain into RCE attempts on production.

## GAP-8 Fee flow manipulation [A, X on real money]

- Capture the full browser flow Burp-side from the fee module (login ->
  fee -> gateway redirect). Inspect params BEFORE redirect: amount, order
  id, student id, currency, return URL, checksum fields.
- Replay a MODIFIED amount at the pre-authorization step ONLY. If the app
  accepts and forwards a tampered amount/order id to the gateway, that is
  a business-logic finding. NEVER complete a payment, NEVER complete 3DS,
  NEVER replay callbacks.
- Check the success callback URL for verifiable signature; if the return
  checksum is missing or client-visible, that is reportable.

## GAP-9 Rate limit / lockout [A, sacrificial account]

- Use a dedicated throwaway account at exercise END. 15-20 wrong-password
  attempts, one attempt per 2-3 seconds. Log: response code, any lockout
  message, time-to-lockout, unlock behavior (auto? manual?).
- NEVER spread attempts across many usernames (that is spraying: X).

## GAP-10 Subdomain takeover (dangling CNAMEs) [A, REPORT ONLY]

- Confirmed dangling candidates (passive): mycampus.jaipur.manipal.edu and
  testmycampus.jaipur.manipal.edu CNAME to edtech366.azurewebsites.net
  (NXDOMAIN). Verify the Azure resource is truly gone, then REPORT.
- Verb doc: certificate issuance on the dangling names would complete a
  takeover proof, but DO NOT do it without authorization; the finding
  stands on CNAME + NXDOMAIN evidence alone.

## GAP-11 Email spoofing (DMARC p=none) [P/A]

- Passive: DMARC p=none on jaipur.manipal.edu, muj.manipal.edu (inherits)
  and manipal.edu. SPF -all hard fail (good) but DMARC p=none means
  spoofed mail still delivers.
- Demo (authorized, own mailbox): craft an SPF-aligned spoof? No, easy
  path: use the club's own domain or a won't-be-blocked sender to show a
  fake "Fee Pending" email renders in a mailbox. Evidence: header shows
  missing DMARC enforcement. This is the phishing-story finding.
- The INR 487,000 fee-pending Reddit complaint is the real-world hook.

## GAP-12 Entra identity surface [A]

- Authorized-only: GetCredentialType enumeration with synthetic accounts
  (5 requests max), SSPR config review per tenant, Conditional Access
  policy review from admin side, banned-password list, legacy auth
  blocking, sign-in logs around reset events.
- Client-side demo (safe): show the two-tenant split (jaipur vs muj
  tenants have different GUIDs) means app-level issuer validation must
  exist; a token accepted across tenants would be a confused-deputy bug.
- M365 tenant: no password resets, no MFA toggling, no messaging. Ever.

## GAP-13 jQuery 1.10.2 reachability [A]

- Range membership is confirmed (CVE-2015-9251, CVE-2019-11358). Prove
  reachability: post-login pages, find sinks where user-controlled input
  reaches .html()/.append()/DOM manipulation. Grep the app's script
  bundles (scripts.bundle.js is theme; app JS may be minified on pages).
  Evidence = data flow from input to sink, not just version match.

## GAP-14 MachineKey / enc param [X live, lab only]

- The enc param is Base64 then (likely) decrypted with MachineKey data.
  Forging enc values = attempting to craft valid encrypted payloads; that
  is exploit development, keep it in a lab clone with a COPY of the app.
  Live: only note behavior (valid-base64 garbage -> different exception
  vs invalid base64 -> FormatException). That behavioral split is enough
  to characterize the crypto layer for the report.

## GAP-15 IIS 8.3 short names / WebDAV / smuggling [X live]

- 8.3 tilde enumeration: 10-20 requests, stop if WAF engages. WebDAV:
  OPTIONS already 404. Request smuggling: do NOT test on production; Azure
  Front Door + IIS desyncs are a lab-clone exercise.

## TRAPS (avoid)

- WAF/edge changes: any 403/406 shift mid-test likely means the edge
  started flagging; stop, wait, re-baseline.
- Never authenticate as a real student. Never use real fee data.
- Screenshot every step: the club report needs evidence, not memory.
- Two-account IDOR tests: both accounts must be created by the
  authorization holder, not scraped or borrowed.

## What I (Hermes) will not do myself

1. No credential stuffing, password spraying, or Guessing against any
   real account (IT Act 43/66; spray risk is real: usernames are public).
2. No exploitation payloads on production: SQLi, XSS weaponized, RCE,
   deserialization, forged enc tokens.
3. No account creation, data modification, deletion, or state changes
   on the live system.
4. No session hijacking of real users, no cookie theft.
5. No payment transactions or gateway callbacks, even "test" ones.
6. No DoS, volume fuzzing, or scanners that hammer the origin.
7. No subdomain takeover claiming (cert issuance on campus domains).
8. No access to out-of-scope hosts: muj.slcm, mujerp, mujone, rms,
   helpdesk, admissions, MAHE SIS/slcm, Microsoft tenant, apps.
9. No public posting of any finding without written university consent.
10. No targeting of individuals (staff, students) for access.

I WILL: run the full recon/OSINT pipeline, all passive probes, build the
tooling, docs, test plans, run the auth-phase tests ONCE written
authorization + throwaway accounts exist, and write the disclosure-grade
report. That is the same line any professional penetration tester draws.