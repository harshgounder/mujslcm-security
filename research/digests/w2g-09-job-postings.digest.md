# Digest: w2g-09-job-postings.md

## REPORT
Source file: w2g-09-job-postings.md. Job-board OSINT across LinkedIn, Naukri, Indeed, plus official MUJ and MAHE career pages, looking for postings that bind MUJ to SLCM, Manipal ERP, or student-portal maintenance. Bounded negative finding dated 2026-08-25.

## ANSWER SUMMARY
- Verdict: no direct, publicly indexed MUJ job posting explicitly mentions SLCM, Manipal ERP, student-portal maintenance, ASP.NET MVC, SQL Server, IIS, Microsoft 365 identity, a portal-operations team, or a vendor. Confidence Moderate for the bounded negative; low for any architecture or vendor claim.
- Strongest Naukri MUJ results are a Library Assistant listing (library management, record keeping, library software, MS Office) and a Lab Technician/Instructor - 3D Lab listing (3D CAD, DFAM, 3D printing). Neither mentions SLCM or the requested stack; neither supports a "technical SLCM role" reading.
- Official MUJ careers page (career-community.php) groups vacancies into academic, research, and non-academic categories and names schools and Quality and Compliance functions; no portal-operations or technical support role visible.
- Indeed results are keyword/location search pages populated with unrelated employers (Foxoso Hospitality, Selenite Organisation, ATHARVA ORGANISATION, real-estate sales roles). A query term is not employer attribution.
- LinkedIn public queries returned zero MUJ jobs in the United States for the "Manipal University Jaipur" query; treated as no-confirmation only, because results are location-, login-, and personalization-dependent.
- Entity-separation findings: Sikkim Manipal University (Majhitar), Manipal Technologies (Udupi), Manipal Dot Net, MAHE, and Manipal Dubai all appear in the corpus; none substitutes for MUJ SLCM evidence.
- Stack matrix: every requested field (ASP.NET MVC, .NET Framework 4.x, SQL Server, IIS, M365 identity, Manipal ERP, vendor, team) is rated "not publicly stated" in reviewed postings. Only the portal name "WELCOME TO MUJ PORTAL" is publicly confirmed.
- Recommended follow-up is a periodic targeted watch of the official MUJ careers page and the Naukri MUJ company page using role families such as application support, enterprise applications, MIS, systems administrator, and software developer.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/ - live portal; confirms "WELCOME TO MUJ PORTAL" and sign-in/parent-login labels only.
- https://jaipur.manipal.edu/career-community.php - official MUJ vacancy index; academic, research, non-academic categories; no stack disclosure.
- https://www.naukri.com/manipal-university-jobs-in-jaipur - Naukri MUJ Jaipur search page; visible MUJ roles are Library Assistant and 3D Lab Instructor.
- https://www.naukri.com/job-listings-library-manipal-university-jaipur-jaipur-0-to-5-years-040826029330 - Library Assistant posting; B.L.I.S/M.L.I.S, library software, MS Office; no SLCM or stack.
- https://www.naukri.com/manipal-university-jaipur-jobs-careers-4408504 - Naukri MUJ company page; two jobs listed including the 3D Lab role.
- https://in.indeed.com/q-manipal-university%2C-jaipur-l-jaipur%2C-rajasthan-jobs.html - Indeed keyword page; results are unrelated employers and sales/management roles.
- https://in.indeed.com/q-manipal-university%2C-jaipur-l-jaipur%2C-rajasthan-jobs.html?start=10 - second Indeed results page; a real-estate Associate role visible, no MUJ SLCM evidence.
- https://in.indeed.com/jobs?q=Manipal+University+Jaipur - general Indeed query page; discovery only.
- https://www.linkedin.com/jobs/search/?keywords=Manipal%20University%20Jaipur - LinkedIn public query; zero jobs in the United States for MUJ.
- https://www.linkedin.com/jobs/search/?keywords=Manipal%20University%20IT - broader LinkedIn query; mixed search context, no direct MUJ technical posting.
- https://www.linkedin.com/company/manipal-university-jaipur/ - MUJ company page inspected; no SLCM vacancy extracted.
- https://www.manipal.edu/mu/important-links/careers-mu/jobs-at-mahe-current-vacancies-.html - MAHE vacancy index; faculty/research/non-academic categories; MAHE, not MUJ.
- https://www.manipal.edu/mu/academics/student-portal.html - MAHE student-portal page; portal context for another Manipal entity.
- https://jaipur.manipal.edu/career-veiw.php?url=77%2Fapplications-now-open-for-faculty - TAPMI School of Business faculty posting; MUJ but non-technical.
- https://web.manipal.net/mdn/careers/currentOpenings/applyforjob.php - Manipal Dot Net Pvt Ltd careers; corporate Manipal entity excluded as vendor evidence.

## ACTIONABLE LEADS
- Set up a dated-snapshot watch: periodically capture jaipur.manipal.edu/career-community.php plus the Naukri MUJ company page and check for role families application support, enterprise applications, MIS, systems administrator, software developer.
- When a positive lead appears, preserve the direct posting URL with employer, location, date, and full description; enter the evidence table only when the posting names MUJ and the relevant system or duties.
- Request official confirmation from MUJ of the system owner, support contact, application stack (authorized documentation or procurement records), database, identity integration, CDN, and vendor; the job corpus cannot answer any of these.
- Search public procurement or tender notices for a vendor relationship; the report explicitly suggests this as the safe channel.
- Treat the portal as visible-surface-only evidence: banner and login labels confirm identity, not framework; do not convert the supplied stack into independent fact.

## FLAGS
- The finding is "not found in the public corpus reviewed as of 2026-08-25", not proof of nonexistence; the report itself warns that boards are dynamic, incompletely indexed, and location/login dependent.
- LinkedIn results are US-location bound in the cited pages; zero US jobs do not cover India-based listings, internal postings, or recruiter-only roles.
- The Library Assistant's "library software" and "MS Office" must not be read as Microsoft 365 identity or SLCM access; the report explicitly blocks that inference.
- Naukri page counts (e.g. 12,277 "Manipal University" vacancies) are brand-aggregate search counts across Sikkim Manipal, Manipal Technologies, and others, not MUJ technical vacancy counts.
- The L&D Executive reference is expired or search-context only; do not treat it as an active MUJ role.
- Reference table repeats citation numbers ([12] twice, [18] three times, [16] twice) in one row each, which hints at extracted search output; the underlying URLs are consistent and were verified against the body text.
- All stack items remain sourced only from the user-supplied brief; this report must not be cited as stack evidence.

## COVERAGE
- File: w2g-09-job-postings.md.
- 174 lines total; 25,798 bytes on disk; 25,696 chars read.
- Method: read_file offset 1, limit 2000, single call.
- EOF confirmed: final call returned truncated: false, last content line 174 equals total_lines 174.