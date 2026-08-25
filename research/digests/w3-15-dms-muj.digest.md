# Digest: w3-15-dms-muj.md

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