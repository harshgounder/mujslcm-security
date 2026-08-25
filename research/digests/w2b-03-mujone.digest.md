# Digest: w2b-03-mujone.md

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