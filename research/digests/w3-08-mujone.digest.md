# Digest: w3-08-mujone.md

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