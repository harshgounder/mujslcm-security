# ATTACK-SURFACE-MAP — mujslcm.jaipur.manipal.edu

Status: verified hands-on 2026-08-25 (recon phase). Evidence: recon/ dir.

## Identity & entry (wave-1 research: 3 separate Entra tenants)

- Login: https://mujslcm.jaipur.manipal.edu/ (single page, POST to "/")
- Fields: UserName, Password, hidden EmailFor + LoginFor (role switch:
  student/parent/staff), __RequestVerificationToken (cookie + field)
- Username scheme (PUBLIC, official FAQ): name.registrationNumber,
  e.g. garv.2506040062; register numbers appear in public PDFs/docs
- Password: the user's Microsoft 365 password (per FAQ); password
  reset delegated to https://passwordreset.microsoftonline.com (Entra)
- Tenants: jaipur.manipal.edu -> 7d0726e8-bf4b-4ac1-99f1-010fb11f1d3f
  (alias mujcampus.onmicrosoft.com); muj.manipal.edu ->
  27282fdd-4c0b-4dfb-ba91-228cd83fdf71 (mujmanipal.onmicrosoft.com);
  manipal.edu -> 29bebd42-f1ff-4c3d-9688-067e3460dc1f. All Managed
  (no AD FS). SLCM federation unproven: local form, reset link only.
- DMARC p=none on all three domains (spoofing possible); SPF -all hard
  fail; Microsoft DKIM selectors published
- No local forgot-password observed; no account registration (accounts
  provisioned by university)
- Post-login redirect target: /Home/Index; protected URLs sealed into
  encrypted "enc" parameter (not a raw open redirect as tested)

## Edge & origin

- Azure edge: A 98.70.14.50 = AS8075 Microsoft Azure Cloud (central
  india, Pune); HTTP/2; TLS via Azure layer (Front Door/App Gateway
  likely edge termination, NOT Akamai; corrected from first read)
- Same Azure region hosts the sibling portals (muj.slcm 20.244.94.89,
  mujerp 20.244.0.229 = Azure central india; mujone 52.172.36.15 and
  parent slcm 104.211.226.160 = Azure south india); RMS on Ibus
  (202.131.155.153, Jaipur ISP). Organic Azure-native estate.
- Certificate: Entrust DV, CN mujslcm.jaipur.manipal.edu only,
  notBefore 2025-12-22, notAfter 2026-12-21
- TLS (SSL Labs grade B, w1-02): TLS 1.0/1.1/1.2 enabled, BEAST/CBC/
  3DES warnings, no HSTS
- Alternate host (CT logs): muj.slcm.jaipur.manipal.edu A 20.244.94.89
  (Azure) - OUT OF SCOPE to test; intel only

## App stack (fingerprinted)

- Microsoft-IIS/10.0; x-aspnet-version 4.0.30319;
  x-aspnetmvc-version 5.3 (MVC 5.3, .NET Framework 4.x)
- ASP.NET Version:4.7.4136.0 leaked via YSOD (F1)
- Anti-CSRF: MVC antiforgery, validated server-side (verified firing)
- Sessions: __RequestVerificationToken cookie on mujslcm;
  ASP.NET_SessionId on slcm.manipal.edu (family reference)
- Client: jQuery 1.10.2 (2013) + jquery.validate + unobtrusive
- UI: Keenthemes "keen" theme demo1 asset tree
- HEADERS present: X-Frame-Options SAMEORIGIN, HttpOnly CSRF cookie
- HEADERS missing: CSP, HSTS, X-Content-Type-Options, Referrer-Policy,
  Permissions-Policy, COOP
- x-powered-by: ASP.NET exposed (F3)

## Route surface (observed) — CORRECTED 2026-08-25 (REAUDIT E1)

- /Home/Index : login page
- ALL <=3-segment paths 302 to the auth gate, including junk
  (/zzz.aspx, /Content/nonexistent.css, /api/values, /Home/zzz):
  302 does NOT prove a route exists. Only 4+ segment paths 404
  (/Foo/Bar/Baz/Quux) and .axd handlers diverge (trace 403, elmah 404).
- /Home/Index?enc=... : enc parameter injection (studied: F1b/F8:
  FormatException on non-base64, CryptographicException on valid
  base64 = machineKey-protected blob)
- /elmah.axd : 404 (clean)
- /trace.axd : 403 (exists, restricted) (F2)
- Route-name candidates after auth come from third-party client code
  (w2c-20: 13 routes incl. attendance/marks/timetable/OTP), NOT probes.
- /robots.txt : redirects to /Home/Index
- Verbs: GET/POST normal; PUT 411/404, TRACE/DELETE/PATCH 404,
  OPTIONS 404

## Behavior notes

- Login POST without CSRF token: 500 YSOD, full stack trace (F1)
- Failed login with valid token: 200 re-render, no distinct user
  message (no user enumeration by response diff; CONFIRMED CLEAN)
- Empty creds: server-side validation messages rendered (CLEAN)
- Response sizes differ only by echoed username (no enum signal)

## Campus ecosystem (evidence only, NOT in scope)

- Mail: Microsoft 365 (MX outlook). SPF includes outlook + Brightspace;
  Cisco Webex domain verification TXT present
- lms.jaipur.manipal.edu -> Brightspace D2L (learning.onlinemanipal.com)
- Admissions CRM: admissions.jaipur.manipal.edu CNAME NoPaperForms
- mujone.jaipur.manipal.edu (Azure), mujerp.jaipur.manipal.edu (Azure),
  rms.jaipur.manipal.edu, helpdesk.jaipur.manipal.edu
- MUJ Connect app: mujconnect.in
- Fee instructions: www.jaipur.manipal.edu/pay-fee-online.php
- MAHE family: slcm.manipal.edu (IIS10, no XFO), sis.manipal.edu (aspx),
  student.manipal.edu.my (Malaysia)

## Exposure history

- Wayback first capture: 2025-01-10 (/Home/Index); Jan 2025 build had a
  Faculty login tab (dvFacultyLogin) removed in current build
- No CVEs/breach reports surfaced in open search for the SLCM product
  (w1-04 report covers depth)

## Highest-value next probes (with auth)

1. IDOR in post-login resources (marks/fee/docs/notifications)
2. Role switch (EmailFor/LoginFor) privilege boundary
3. Session flags + fixation + logout invalidation
4. CSRF on state-changing post-login actions
5. Rate limiting on our own test account only