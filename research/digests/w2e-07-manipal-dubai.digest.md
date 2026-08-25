# Digest: w2e-07-manipal-dubai

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