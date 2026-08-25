# Digest: w3-04-sis-manipal-feekart.md

## REPORT
Source file: /home/liebert511/mujslcm-recon/research/w3-04-sis-manipal-feekart.md (AI deep-research output, claims UNVERIFIED). Topic: MAHE SIS risk and MUJ SLCM trust boundaries. Passive OSINT and defensive assessment; no authentication, CAPTCHA, or payment testing.

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