## REPORT (w1-06-student-data-osint)

## ANSWER SUMMARY
- Exposure is real but uneven: the strongest verified student-level data sits in official PhD PDFs under jaipur.manipal.edu/img/pdf/, not in SLCM itself.
- The PhD awardee compilation is a ~500-scale dataset (visible serial reaches 502): names, faculty, department, registration number, thesis title, supervisors, award and viva dates.
- Applicant emails appear in official shortlist PDFs (July 2026 and July 2025), joined to application number, department, candidature and exemption status.
- No verified undergrad marks list, attendance roster, exam seating, hostel room roster or fee balances; the hostel PDF is guidance and the fee notice is non-personal.
- The 24JTEECS001 format is unsubstantiated; the official SLCM FAQ shows a numeric registration number, contradicting the alphanumeric claim.
- All open-source scrapers require credentials; no evidence of a no-auth university API, ASMX/WCF service or /api/ route.
- Routes are indexed (mujslcm /Home/Index, /Student) but show no pre-login records; web archives add structure only.
- Verdict: moderate-high public-data exposure via documents, with no proven live SLCM breach.

## KEY FACTS
- https://jaipur.manipal.edu/img/pdf/List-of-PhD-Awarded-%28till-2025%29.pdf - 500-scale awardee dataset joining identity, reg numbers, theses, supervisors and dates.
- https://jaipur.manipal.edu/img/pdf/List-of-Candidates-Eligible-for-PhD-Interview-%28July-2026%29.pdf - highest-risk PDF: name, email, application number, department, candidature and exemption status together.
- https://jaipur.manipal.edu/img/pdf/Shortlisted-Candidates-PhD-Exam-July-18072025.pdf - July 2025 shortlist with application number, roll/name and registered email.
- https://jaipur.manipal.edu/img/pdf/PhD-ADMISSIONS-JAN-2026-INTERVIEW-RESULT-LIST-OF-SELECTED-CANDIDATES.pdf - Jan 2026 selected candidates with names and application/registration numbers.
- https://jaipur.manipal.edu/img/pdf/PhD-Interview-Results-July-2026.pdf - July 2026 selected candidates with application number, department and candidature.
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - official SLCM FAQ: portal URL, username convention, helpline; contradicts the 24JTEECS001 specimen.
- https://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf - onboarding guide describing SLCM purpose and profile registration.
- https://jaipur.manipal.edu/research-phd.php - discovery hub linking the whole PhD result and shortlist PDF series.
- https://www.scribd.com/document/881889937/Eligible-Students-MUJ-1 - third-party claim of a multi-field MUJ student list; provenance unverified.
- https://www.scribd.com/document/792426451/Book4 - unverified Scribd candidate file; field categories not established.
- https://web.archive.org/cdx/search/cdx?url=mujslcm.jaipur.manipal.edu/*&output=json&fl=timestamp,original,statuscode,mimetype&filter=statuscode:200&collapse=urlkey - archive captures of / and /Home/Index from 2025-2026.
- https://web.archive.org/cdx/search/cdx?url=slcm.manipal.edu/*&output=json&fl=timestamp,original,statuscode,mimetype&filter=statuscode:200&collapse=urlkey - legacy routes incl loginForm.aspx, Print.aspx, WebForm1.aspx and password-change pages.
- https://jaipur.manipal.edu/contact-university.php - role-based contact directory across academic, exam, hostel, finance, HR, IT, library, registrar, welfare and webmaster.
- https://mujslcm.jaipur.manipal.edu/Home/Index - indexed public login landing page; no pre-login student record in extracted body.
- https://www.manipal.edu/content/dam/manipal/mu/hostel/pdf/Hostel%20Allotment.pdf - hostel allotment guidance only; no roster, room assignments or student list.

## ACTIONABLE LEADS
- Pull all PhD result, shortlist and awardee PDFs and inventory fields internally; confirm which contain emails and internal identifiers.
- Validate the Scribd Eligible-Students-MUJ-1 file internally for authenticity and provenance; request removal if real; do not amplify it.
- Replace result PDFs with masked application references, add noindex and request search cache removal after replacement.
- Probe /img/pdf/, /uploads/, /documents/ and /files/ for directory indexing; no Index of listing verified yet.
- Run an authorized object-level authorization test with synthetic accounts covering student, parent, staff and admin roles.
- Include retired routes (Print.aspx, WebForm1.aspx, StudentChangePassword.aspx, ParentChangePassword.aspx) in decommission and asset reviews.
- Review retention policy for the awardee list with registrar and research office; push for removal of registration numbers.
- Verify the @muj.manipal.edu email convention claim against official documentation before relying on it.
- Monitor for re-uploads of the same PDF data on third-party hosts; set up alerting on new scribd/paste hits.
- If a default or working password is discovered, report it privately to MUJ; never reproduce it in public.

## FLAGS
- 24JTEECS001 decomposition (year, campus, branch, sequence) is unverified; the official FAQ numeric example contradicts it.
- Scribd documents: authenticity, date and source chain unknown; titles can mislabel; both are leads, not confirmed spills.
- The "502" figure is the visible serial number in the awardee PDF, not a stated row count.
- @muj.manipal.edu is a medium-confidence inference from portal branding, not a documented email standard.
- Negative findings (marks lists, attendance rosters, directory indexes, phone lists) are moderate confidence only.
- Faculty profile phone links appear to be generic admissions numbers, not personal faculty numbers.
- Archive inventory proves route existence only; auth state and function at capture time are unknown.
- muj.slcm.jaipur.manipal.edu returned no archived captures in the reviewed CDX result.

## COVERAGE
Source read in full: /home/liebert511/mujslcm-recon/research/w1-06-student-data-osint.md. File char count as read: 43659 (326 lines). Read pagination reached line 326 of 326; EOF confirmed (truncated: false).