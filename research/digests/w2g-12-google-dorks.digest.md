# Digest: w2g-12-google-dorks.md

## REPORT
Source file: w2g-12-google-dorks.md. Passive public-indexing and search-dork assessment for the MUJ SLCM ecosystem. Search-engine discovery only; no authentication, credential testing, route enumeration, or vulnerability scanning. 23 references.

## ANSWER SUMMARY
- Verdict: informational OSINT finding. No confirmed public student-record exposure in observed first-party results. Confidence: High for observed search-result classifications, Moderate for negative findings, Low for unverified stack claims.
- Indexed surfaces: mujslcm.jaipur.manipal.edu (title "muj portal - Manipal University", "WELCOME TO MUJ PORTAL", Sign In Student/Parent Login) and /Home/Index (login-oriented, "Forgot Password?").
- Official linkage: the SLCM FAQ and the official payment page (pay-fee-online.php) both identify the SLCM root as the student portal; the annual-fee notice is dated June 24, 2025 with July 18, 2025 as the 2025-26 payment deadline.
- Register-number, marks, and student-list dorks produced no confirmed first-party student-specific marksheet or register-number file; the report uses the wording "no confirmed hit observed," not proof of absence.
- XLSX dorks: no confirmed MUJ-hosted XLSX workbook. Results with .xlsx titles resolve to .pdf URLs (e.g. List of Patent Status_01.04.2024.pdf); cross-scope hits (cia.manipal.edu TOX STAT workbook, a GitHub call-centre workbook) were excluded.
- Privacy lead: a third-party Scribd result claims to contain student registration numbers, emails, genders, departments, names, and degrees. Not treated as MUJ-domain evidence, not to be downloaded, copied, or redistributed.
- Technology claims (ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai, M365) are unverified by indexed pages; /Home/Index is MVC-shaped only as an inference. Technology dorks returned generic vendor documentation.
- Hostname hygiene: muj.slcm.jaipur.manipal.edu and slcm.manipal.edu (MAHE footer) must not be merged with the target without owner confirmation.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/ - indexed root; page titled "muj portal - Manipal University" with sign-in and parent/student login labels.
- https://mujslcm.jaipur.manipal.edu/Home/Index - indexed public login route; "Forgot Password?" visible.
- https://muj.slcm.jaipur.manipal.edu/ - alternate MUJ-looking host with similar sign-in text; canonical ownership unconfirmed.
- https://slcm.manipal.edu/ - "MU SLcM" page with MAHE, Manipal footer; cross-institutional false positive.
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - official FAQ; strongest official link between the university site and the SLCM registration URL.
- https://jaipur.manipal.edu/pay-fee-online.php - payment page that explicitly identifies the SLCM root as the student portal.
- https://jaipur.manipal.edu/img/pdf/Notification_Annual-Fee-Payment-AY-2025-26.pdf - fee notice; June 24, 2025 date, July 18, 2025 deadline for AY 2025-26.
- https://jaipur.manipal.edu/fee-structure.php - public course-fee page with school and department links; intended public data.
- https://jaipur.manipal.edu/examination.php - public description of assessment components; policy, not a marksheet.
- https://www.jaipur.manipal.edu/administration-registrar.php - official registrar page; no student-specific list observed.
- https://jaipur.manipal.edu/img/pdf/research/muj/List%20of%20Patent%20Status_01.04.2024.pdf - .xlsx search title with a .pdf URL; file-type mismatch example.
- https://cia.manipal.edu/content/dam/manipal/mu/kmc-manipal/Documents/TOX%20STAT%20whole%20year.xlsx - real XLSX URL but KMC Manipal scope, not MUJ SLCM.
- https://github.com/Nikhilshetty1/Manipal-call-centre-analysis/blob/master/final_revenue.xlsx - third-party-hosted workbook; not an official MUJ artifact.
- https://www.scribd.com/document/881889937/Eligible-Students-MUJ-1 - third-party claim of student registration data; unverified privacy lead, not first-party evidence.
- https://www.getmyuni.com/college/manipal-university-jaipur-result?page=result - third-party result page claiming MUJ results; secondary description, not a marksheet URL.

## ACTIONABLE LEADS
- Owner-side review: MUJ web and identity teams should check Search Console and server logs for the root host, alternate host, /Home/Index, FAQ PDF, fee documents, and document directories; confirm whether any authenticated response was ever cached or indexed.
- Document owners: inspect PDF, XLSX, CSV, DOCX, and image repositories for names, registration numbers, emails, marks, fee receipts, attendance, or student identifiers; confirm actual file type and contents, not titles; use the approved takedown process for stale copies.
- Application owners: minimize login-page disclosure, make password recovery non-enumerating, and prevent authenticated pages from caching as public content; these belong in an authorized test plan.
- Club practice: keep a dated log of query, result title, exact URL, classification; redact all personal data; share only URLs, timestamps, query strings, and redacted screenshots with the university's authorized security contact.
- Disclosure split: first-party evidence (FAQ, payment page) vs third-party leads (Scribd items); report the Scribd material privately as an unverified lead, never redistribute content.
- Ask MUJ to confirm canonical ownership and redirect policy for the two similar hostnames.

## FLAGS
- All negatives are search-time, location-, and account-state-bound; "no confirmed hit observed" is deliberate wording, not proof of absence.
- The Scribd student-data claims are third-party and unverified; opening, copying, or redistributing them is explicitly discouraged; they establish nothing about MUJ publication.
- Search titles can embed original spreadsheet names while URLs end in .pdf; always validate file type by URL and content type.
- Alternate and MAHE hostnames are not confirmed equivalent to the target; merging them into one asset is unsupported.
- The stack and identity claims stay unverified; /Home/Index only supports an MVC-style inference from URL shape.
- The report notes noindex is not a substitute for authorization; indexing of an entry point is not an authorization failure.
- One reference (Statute-MUJ.pdf under muj.onlinemanipal.com, http) appears in the list without body discussion; low relevance.

## COVERAGE
- File: w2g-12-google-dorks.md.
- 185 lines total; 32,175 bytes on disk; 32,175 chars read.
- Method: read_file offset 1, limit 2000, single call.
- EOF confirmed: final call returned truncated: false, last content line 185 equals total_lines 185.