# Digest: w2e-08-sikkim-manipal

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