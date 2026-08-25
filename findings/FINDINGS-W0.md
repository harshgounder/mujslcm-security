# FINDINGS — Wave 0 (hands-on recon) — 2026-08-25

Target: https://mujslcm.jaipur.manipal.edu/
Method: single low-rate HTTP requests + public OSINT. Non-destructive.

## VERIFIED FINDINGS

### F1. Verbose .NET error pages (YSOD) — information disclosure, MULTIPATH [P3]

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
- NOT probed (out of stated scope). Club should ask the university what
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

## INTEL (for the club's testing plan)

- Username format is PUBLIC in the official SLCM FAQ PDF
  (https://www.jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf):
  "name.registration-number" e.g. garv.2506040062. Register numbers are
  10-digit, batch-prefixed, and appear in university documents, so
  account names are derivable. This makes account-lockout and rate-limit
  controls critical. Check them with the club's test account.
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
- Auth-context testing (IDOR, session handling) requires the club's
  test credentials — club lead to supply.