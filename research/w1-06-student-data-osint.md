# MUJ SLCM Public Exposure: Evidence, Limits, and Risk

## Executive Summary

- **Exposure Is Real but Uneven**: MUJ's public footprint exposes substantial institutional metadata, staff contact information, SLCM login structure, and several official PhD applicant and scholar lists. The strongest student-level exposure is not an open SLCM database; it is a set of ordinary, search-reachable PDFs under `jaipur.manipal.edu/img/pdf/` containing names, application or registration identifiers, departments, candidature status, email addresses in some lists, and research-history fields [26][27][32] -> MUJ should treat document publishing as a data-governance problem, not only an application-security problem.

- **A 500-Scale Researcher Dataset Is Public**: The official PhD awardee compilation exposes candidate names, faculty, department, registration number, thesis title, supervisor, co-supervisor, degree-award date, and viva date; the visible serial sequence reaches 502, although the source does not state a formal row count [32] -> This document deserves immediate purpose-and-retention review because it joins identity, academic history, and supervisory relationships at unusually high density.

- **Applicant Emails Appear in Official Result Lists**: The July 2026 PhD interview-shortlist PDF includes application number, department, applicant name, email ID, candidature type, and examination-exemption status [27] -> Public result notices should use masked application references and omit email addresses unless a documented legal or operational requirement demands publication.

- **No General Undergraduate Marks or Attendance Spill Was Verified**: The official examination page and targeted searches did not yield a verified MUJ-hosted undergraduate marks sheet, attendance roster, exam-room seating list, hostel-allotment roster, or seat-allotment list. The hostel document reviewed is guidance rather than a roster [9] -> Treat this as a bounded negative finding, not proof that no such document exists anywhere.

- **The Proposed `24JTEECS001` Format Is Unsubstantiated**: MUJ's official SLCM FAQ instead shows a login username constructed from a name and a numeric registration number; it does not publish a field-by-field explanation of year, campus, faculty, branch, or sequence components [6] -> Do not assert that `24`, `JT`, `EECS`, or `001` encode specific properties without an authoritative MUJ source.

- **Public Code Does Not Prove a No-Auth University API**: Open-source projects describe retrieving marks, attendance, timetable, CGPA, and profile data, but the reviewed projects require a registration number and password, validate supplied credentials, or perform an authenticated login [4][20][24][30][31] -> The evidence supports an ecosystem of credentialed scrapers, not a confirmed MUJ or MAHE endpoint returning student data without authentication.

- **Routes Are Indexed, Records Are Not**: Current public pages expose `Home/Index`, `Student`, sign-in, and parent-login structure, while the extracted landing pages show no pre-login student record [22][21]. Internet Archive inventories add historical route names and front-end asset structure but do not themselves contain student records [12][13] -> Reduce unnecessary route indexing, but prioritize authorization and document governance over route-name secrecy.

- **Staff Contacts Are Public by Design**: MUJ publishes an institutional contact directory spanning academic, examination, hostel, finance, HR, IT, library, registrar, welfare, placement, and webmaster functions [8]. Individual faculty profiles can disclose a name, institutional email, and LinkedIn URL, while displayed telephone numbers may be generic admissions contacts rather than personal faculty numbers [10] -> Keep role-based contacts public, but distinguish office numbers from personal contact data and prevent bulk harvesting where possible.

- **No Open Folder Index Was Verified**: Public documents are reachable through curated pages and predictable content paths such as `/img/pdf/`; the evidence did not establish an Apache-style `Index of` listing for `/uploads/`, `/documents/`, or `/files/` -> MUJ should still disable directory indexing everywhere and inventory every public object-store or web-root path.

- **Overall Risk Is Moderate-High for Privacy, Not a Proven Live SLCM Breach**: The public footprint enables correlation across candidate identities, registration or application numbers, departments, emails, research topics, supervisors, and portal conventions. It does not establish unauthenticated access to current marks, attendance, fees, or profiles -> Remediation should begin with public-document minimization, search de-indexing, archive-aware cleanup, and authorization testing using institution-controlled test accounts.

## Scope, Safety Boundary, and Reasoning Transparency

This review covers information reachable without credentials through public search results, ordinary page and PDF retrieval, public GitHub repository descriptions, and Internet Archive URL inventories. It does not log into SLCM, submit identifiers, test passwords, call a suspected private endpoint, defeat a CAPTCHA, enumerate student numbers, or retrieve any non-public record. No individual student value is reproduced in this report, even where a public document contains it.

The report separates four evidence states:

1. **Verified public exposure** means the field category was visible in an openly retrievable source.
2. **Public structural metadata** means routes, login roles, domains, or document paths were visible, but no student record was returned.
3. **Third-party claim** means a non-MUJ host describes or republishes data whose provenance cannot be established from the page alone.
4. **Not verified** means targeted research did not produce defensible evidence. It does not mean the condition is impossible.

I cannot provide private chain-of-thought or hidden internal reasoning. Instead, the report supplies a reproducible evidence trail: exact URLs, source-by-source classifications, contradictions, confidence levels, and the limited inference connecting each observation to its risk. This is more useful for an audit because another analyst can check the evidence without relying on undisclosed mental steps.

The official onboarding guide establishes that SLCM is intended as a central platform for academic information [3]. The public FAQ identifies the registration portal and publishes the username-construction convention plus support contacts [6]. Those facts define the ecosystem, but neither source is itself a student-record spill.

**Decision-ready insight:** The footprint is broad enough to support privacy-risk correlation, but the highest-impact verified exposure comes from public documents rather than a demonstrated pre-authentication SLCM flaw.

## Exposure Matrix: What Is Publicly Reachable

| Data category | Verified public location | Exposure status | Evidence strength | Practical interpretation |
|---|---|---:|---:|---|
| Student or candidate names | Official PhD result and award PDFs | Yes | High | Multiple official lists publish names with academic or application context [26][28][32]. |
| Registration or application numbers | Official PhD result and award PDFs | Yes | High | January 2026 selected-candidate and awardee files include application or registration identifiers [26][32]. |
| Marks | Public GitHub scraper descriptions | Capability described, but no public record verified | Medium | Repositories describe credentialed retrieval of marks; this is not proof of open marks data [4]. |
| Attendance | Public GitHub scraper descriptions | Capability described, but no public record verified | Medium | Attendance scraping is documented, with credentials expected [20][30]. |
| Student email addresses | July 2026 and July 2025 PhD shortlist PDFs; one third-party list claim | Yes | High for official PhD lists; medium for third party | Official shortlist headings include email ID or registered email [27][29]. |
| Student phone numbers | None verified | Not verified | Moderate negative finding | None of the reviewed official candidate PDFs exposed a phone field [26][28][27]. |
| Hostel room assignments | Official hostel PDF | No roster verified | High for reviewed file | The file is guidance, not a room-assignment roster [9]. |
| Staff names and professional emails | MUJ faculty directory and profile pages | Yes, intended publication | High | Individual profiles may publish name, institutional email, and professional profile link [10]. |
| Generic office phone numbers | MUJ contact and hostel pages | Yes, intended publication | High | University offices and hostel contacts are openly listed [8][9]. |
| SLCM route structure | Search-indexed pages and Internet Archive | Yes | High | Current login routes and historic ASP.NET-era routes are visible [22][21][13]. |
| Unauthenticated SLCM API returning records | None verified | Not verified | High confidence in reviewed evidence, not universal absence | Reviewed code requires credentials or login [4][24][31]. |

The table shows an important divergence: identity-linked application and research data are directly public, whereas marks and attendance appear in public descriptions of authenticated tooling rather than in verified open records. That difference controls the verdict.

## Official Document Spill: The PhD Publication Pipeline Is the Main Exposure

### Exact document inventory

| Document or page | Exact public URL | Public fields or function | Assessment |
|---|---|---|---|
| First-Year Student Profile Registration Guide | `https://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf` | SLCM purpose and onboarding instructions | Public institutional guidance, not a roster [3]. |
| SLCM FAQ | `https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf` | Portal URL, username convention, helpline, support emails | Structural and contact exposure, not a bulk student list [6]. |
| PhD research and results page | `https://jaipur.manipal.edu/research-phd.php` | Links to interview results, entrance results, shortlisted candidates, regulations, and supervisors | A discovery hub for multiple candidate documents [19]. |
| January 2026 selected PhD candidates | `https://jaipur.manipal.edu/img/pdf/PhD-ADMISSIONS-JAN-2026-INTERVIEW-RESULT-LIST-OF-SELECTED-CANDIDATES.pdf` | Candidate name, application number, PhD registration/application number, discipline, full-time or part-time mode | Verified identity and academic-status exposure [26]. |
| July 2026 selected PhD candidates | `https://jaipur.manipal.edu/img/pdf/PhD-Interview-Results-July-2026.pdf` | Candidate name, application number, department, proposed candidature, selection/list status | Verified identity and application-status exposure [28]. |
| July 2026 candidates eligible for interview | `https://jaipur.manipal.edu/img/pdf/List-of-Candidates-Eligible-for-PhD-Interview-%28July-2026%29.pdf` | Application number, department, applicant name, email ID, candidature, exemption status | Highest-risk current document because email is joined to identity and application data [27]. |
| July 2025 shortlisted candidates | `https://jaipur.manipal.edu/img/pdf/Shortlisted-Candidates-PhD-Exam-July-18072025.pdf` | Application number, name or roll number, registered email, exemption indicator, interview-shortlist status, department | Verified multi-field applicant exposure [29]. |
| PhD awardee compilation | `https://jaipur.manipal.edu/img/pdf/List-of-PhD-Awarded-%28till-2025%29.pdf` | Name, faculty, department, registration number, thesis title, supervisors, degree-award date, viva date | Broad longitudinal scholar dataset; visible serial numbering reaches 502 [32]. |
| Annual fee notice | `https://jaipur.manipal.edu/img/pdf/Notification_Annual-Fee-Payment-AY-2025-26.pdf` | Course and batch fee schedule plus payment deadline | Institutional financial information, not student-specific balances [16]. |
| Hostel-allotment guidance | `https://www.manipal.edu/content/dam/manipal/mu/hostel/pdf/Hostel%20Allotment.pdf` | Hostel philosophy, registration, allotment process, arrival, operations, and contacts | Not a student or room roster; it does publish hostel contact channels [9]. |
| NAAC document hub | `https://www.jaipur.manipal.edu/NAAC-documents.php` | Curated evidence on linkages, MoUs, exchanges, internships, projects, courses, outgoing students, and staff development | Large institutional document surface; not an open folder index [18]. |

### Case study: A normal admissions notice becomes a correlation dataset

The January and July result PDFs appear to serve a legitimate administrative purpose: telling PhD applicants whether they are selected or eligible for interview. The privacy issue is the granularity of publication. A selected-candidate document joins a person's name to an application number, internal PhD identifier, discipline, and candidature mode [26]. A shortlist adds the applicant's email and examination-exemption status [27]. These fields are more revealing together than separately.

The mechanism is straightforward. Search engines index the public results page, the page links stable PDF objects, and the PDF headings expose machine-readable columns. A person searching one candidate's name can discover an application context; a person starting from an email can discover department and candidature type. No SLCM vulnerability is needed. The public web server is performing exactly as configured.

The PhD awardee compilation increases the time horizon. Its fields cover identity, department, registration number, thesis topic, supervisors, and award dates [32]. The visible serial sequence reaches 502 [32], making this a 500-scale institutional history rather than a small announcement. Thesis titles and supervisors are commonly public in research contexts, but publishing them beside internal registration numbers creates a broader correlation key than necessary.

The appropriate remedy is not to hide all academic achievements. MUJ can publish names, thesis titles, and award years where there is a clear scholarly purpose while removing internal identifiers, personal email addresses, and unnecessary application metadata. Admissions results can use a masked application token, authenticated applicant portal, or short-lived notice with a documented retention period.

### Negative findings: marks, attendance, seating, and hostels

Targeted searches did not verify an official MUJ-hosted undergraduate marks list, attendance sheet, seat plan, or hostel-room list. The official hostel PDF reviewed is explicitly procedural and does not contain a student roster, registration-number list, specific room assignments, marks, or attendance [9]. It does contain public hostel email and phone contacts [9], which are institutional contact data rather than student records.

The official annual-fee notice is similarly non-personal. It announces the 2025-26 payment deadline and provides course-wise and admission-year-wise amounts [16]. No evidence reviewed showed individual fee balances. These are important counterexamples: not every indexed PDF with words such as "allotment," "student," or "fee" is a personal-data spill.

**Decision-ready insight:** The confirmed official spill is concentrated in PhD applicant and scholar publication. General undergraduate marks, attendance, seating, hostel assignments, and fee balances remain unverified and should not be claimed as exposed.

## Third-Party Document Spill: Credible Signal, Uncertain Provenance

One indexed Scribd page titled as an MUJ-eligible-students document claims fields including registration numbers, emails, gender, department, names, and degree, across programs such as Data Science, CSE, IT, and ECE [33]. Its exact public URL is `https://www.scribd.com/document/881889937/Eligible-Students-MUJ-1`. Because the host is Scribd rather than a Manipal domain, this is evidence of public reachability but not evidence that MUJ intentionally published or currently controls the file.

A second Scribd page, `https://www.scribd.com/document/792426451/Book4`, is described as downloadable or viewable in spreadsheet, PDF, or text form, but the available excerpt did not establish its field categories [23]. It should therefore be classified as an unverified candidate, not counted as a confirmed student-data spill.

This distinction matters. Search-engine snippets can mislabel uploads, third parties can upload stale or fabricated lists, and a file title alone does not prove institutional origin. Conversely, a third-party host does not remove the privacy impact if the data are authentic. MUJ's incident-response team should obtain and validate such files internally, determine provenance, and send appropriate removal requests without amplifying the records publicly.

The report deliberately does not reproduce any row or identify a student. The correct OSINT conclusion is categorical: at least one third-party indexed page claims a multi-field MUJ student list, but authenticity, date, completeness, consent, and source chain are unresolved.

**Decision-ready insight:** Treat the Scribd list as a potential incident lead requiring internal validation, not as proof of an official leak or as a source for further student enumeration.

## Registration-Number Intelligence: What Is Known and What Is Not

The official SLCM FAQ is the strongest available source. It states that the registration portal is `https://mujslcm.jaipur.manipal.edu/` and shows a username built from a name plus a registration number [6]. The example registration number is numeric. The report does not repeat the example value because the format, not the value, is relevant.

No authoritative source reviewed explains an alphanumeric pattern such as `24JTEECS001`. In particular, the research did not verify that:

- `24` means year of entry;
- `J` means Jaipur;
- `T` means a faculty, program type, or campus;
- `EECS` is an official branch code; or
- `001` is a sequential student number.

Those interpretations are plausible-looking but unsupported. The current official FAQ also creates a contradiction: its numeric example does not match the proposed alphanumeric specimen [6]. Possible explanations include different cohorts, different systems, application numbers versus registration numbers, or an entirely incorrect example. Without a policy document, registrar notice, or data dictionary, selecting one explanation would be speculation.

### Defensive relevance without enumeration

Identifier structure matters because predictable identifiers should never function as authorization secrets. If an identifier embeds admission year, campus, branch, and sequence, it can reduce the number of guesses needed to find a valid-looking identifier. When the login name also incorporates the registration number, public disclosure of that number can make username construction more predictable.

That observation does not justify testing real students. An authorized MUJ assessment should use synthetic or institution-controlled accounts representing several cohorts and programs. The test objective should be whether every record request enforces server-side ownership and role checks, not whether analysts can discover a real student's identifier. Rate limits, generic authentication errors, MFA, monitoring, and object-level authorization should make identifier predictability harmless.

The public-data action is simpler: remove internal registration numbers from result lists when they are not required, never treat the number as confidential authentication material, and ensure password reset does not reveal whether a constructed username exists.

**Decision-ready insight:** The defensible finding is username-pattern exposure plus an official numeric example. The `24JTEECS001` decomposition remains unverified, and no production enumeration should be attempted.

## Directories, Public Folders, and Web Archives

### Curated repositories are not open directory listings

MUJ publishes many documents under `/img/pdf/`, including SLCM guidance, fee notices, PhD results, and mandatory disclosures. The NAAC page links categories covering institutional collaborations, internships, field projects, courses, outgoing students, and staff-development activities [18]. This is a large discoverable document surface.

However, the evidence did not show an Apache or IIS directory index for `/img/pdf/`, `/uploads/`, `/documents/`, or `/files/`. A curated HTML page linking many files is not the same as a server-generated folder listing. Similarly, the public Document Management System landing page found in search required sign-in; its presence is institutional metadata, not proof that its contents are public.

The operational risk remains meaningful because predictable file paths and long-lived links can keep documents discoverable after navigation changes. Removing a link from a page does not remove the object, search cache, or archived copy. MUJ should maintain an object-level inventory of public documents rather than relying only on a crawl of current menus.

### Historical SLCM structure in the Internet Archive

The Internet Archive CDX inventory for `mujslcm.jaipur.manipal.edu` shows archived captures of `/` and `/Home/Index`, together with login-related CSS and JavaScript and ordinary static assets. The visible timestamps span 2025 through 2026 in the retrieved inventory [12]. Exact inventory URL:

`https://web.archive.org/cdx/search/cdx?url=mujslcm.jaipur.manipal.edu/*&output=json&fl=timestamp,original,statuscode,mimetype&filter=statuscode:200&collapse=urlkey`

The historical `slcm.manipal.edu` inventory reaches farther back and includes `/loginForm.aspx`, `/Print.aspx`, `/WebForm1.aspx`, `/StudentChangePassword.aspx`, and `/ParentChangePassword.aspx`, plus front-end resources, CAPTCHA images, and a historical uploaded-file path [13]. Exact inventory URL:

`https://web.archive.org/cdx/search/cdx?url=slcm.manipal.edu/*&output=json&fl=timestamp,original,statuscode,mimetype&filter=statuscode:200&collapse=urlkey`

These archives reveal framework and navigation history, not a student database. A route name such as `Print.aspx` says nothing about whether it was public, authenticated, vulnerable, or even functional at the time of capture. The inventory for the alternate host `muj.slcm.jaipur.manipal.edu` returned no archived URL set in the reviewed result.

**Decision-ready insight:** Archive captures increase structural visibility and preserve retired paths, but the reviewed captures do not prove student-record exposure. MUJ should still include historical hostnames and retired applications in asset management and decommissioning reviews.

## Public SLCM Code and API Claims: Scrapers, Not a Verified Open University API

| Public project | Exact URL | Data described | Authentication evidence | No-auth verdict |
|---|---|---|---|---|
| `tejaskash/slcm-api` | `https://github.com/tejaskash/slcm-api` | Attendance and marks; configurable retrieval of attendance, marks, or both [4] | Requests require username and password [4] | Does not prove a no-auth university endpoint. |
| `manipalthetalk/App-Backend` | `https://github.com/manipalthetalk/App-Backend` | Marks, attendance, timetable [20] | Documented use requires registration number and password [20] | Credentialed scraping, not verified open access. |
| `frozenparadox99/slcmScraper` | `https://github.com/frozenparadox99/slcmScraper` | Internal marks [24] | Requires registration number and password [24] | No no-auth exposure demonstrated. |
| `canaryGrapher/slcmAPI` | `https://github.com/canaryGrapher/slcmAPI` | Marks, attendance, and admission-profile details [30] | Includes checking whether supplied credentials are correct; later affected by CAPTCHA [30] | Helper API around authenticated scraping, not proof of an open university API. |
| `sankalp2004/SLCM-is-Dumb` | `https://github.com/sankalp2004/SLCM-is-Dumb` | CGPA and grade-sheet data [31] | Environment variables hold SLCM username and password; workflow attempts login or prompts for manual login [31] | Explicitly login-dependent. |

### Case study: The word "API" can misstate the exposure

The `slcm-api` repository calls itself a RESTful API and retrieves attendance and marks [4]. That wording could be read as evidence that the university operates a public JSON endpoint. The repository documentation instead expects a username and password [4]. Its API is an intermediary created by the project, not proof that MUJ or MAHE exposes an unauthenticated institutional `/api/` service.

The same pattern appears across the other projects. One project adds marks, attendance, and profile scraping over time but also checks supplied user credentials [30]. Another describes automated or manual login and stores a username and password [31]. These repositories are relevant because they reveal which SLCM data users value and that the web interface has been automated. They are not evidence that an arbitrary outsider can request a student's data without authentication.

No reviewed source established an MUJ or MAHE ASMX/WCF `.asmx` endpoint, a university `/api/` JSON route, or another service that returns student data pre-authentication. No live endpoint testing was performed. The correct status is **not verified**, not "secure" and not "exposed."

The risk mechanism is indirect. Public automation code can become unsafe if users provide credentials to an untrusted deployment, if a third-party server logs them, or if sessions are mishandled. Those are software-supply-chain and credential-trust issues. They should not be confused with a university-side authorization defect.

**Decision-ready insight:** The public repository ecosystem proves credentialed automation of marks, attendance, timetable, CGPA, and profile data. It does not prove a current no-auth SLCM web service.

## Email and Phone Patterns: Institutional Publication Versus Student Leakage

The public footprint supports two distinct identity conventions. First, MUJ's SLCM FAQ publishes a username formed from a name and registration number and points users to the MUJ portal [6]. Search-indexed portal branding also associates the current login with the `@muj.manipal.edu` environment, although the clean static landing-page extraction itself exposed only the portal title and role options [22]. This makes the `@muj.manipal.edu` suffix a medium-confidence portal observation rather than a fully documented student-email naming standard.

Second, official public staff and office contacts use `@jaipur.manipal.edu`. An individual faculty profile exposes a name, an institutional address following a `first.last@jaipur.manipal.edu` form, and a LinkedIn link [10]. The central contact page publishes role-based addresses for academics, admissions, examinations, administration, finance, student services, HR, IT, library, registrar, welfare, placement, and webmaster functions [8].

Phone exposure is mostly organizational. The central directory includes university and office contact numbers [8]. The reviewed faculty profile's phone links lead to admissions contacts rather than a clearly personal faculty number [10]. Hostel guidance publishes hostel contact emails and telephone numbers [9]. No public student phone-number list was verified.

This is a legitimate publication surface, but it can support spear phishing when combined with faculty names, departments, and SLCM terminology. Role accounts such as admissions or examinations are preferable to unnecessary personal contact publication because personnel can change without leaving stale identity data online.

**Decision-ready insight:** Staff and office contact exposure is largely intentional and role-related. Student email exposure is verified in particular PhD shortlist PDFs, while a public student phone directory was not found.

## Google- and Archive-Indexed SLCM Routes

| Host or route | Exact URL | What is publicly visible | Record exposure finding |
|---|---|---|---|
| MUJ portal root | `https://mujslcm.jaipur.manipal.edu/` | MUJ portal sign-in landing page and parent/student role cues | No pre-login record verified [34]. |
| MUJ Home controller | `https://mujslcm.jaipur.manipal.edu/Home/Index` | "WELCOME TO MUJ PORTAL," sign-in, and parent login | No student record in extracted body [22]. |
| MUJ Student route | `https://mujslcm.jaipur.manipal.edu/Student` | Same public login landing content | No student record in extracted body [21]. |
| Alternate Jaipur SLCM host | `https://muj.slcm.jaipur.manipal.edu/` | MUJ portal sign-in branding | Structural metadata only [35]. |
| MAHE SLCM root | `https://slcm.manipal.edu/` | Public SLCM landing shell; clean extraction exposed confirmation text but no record | No student data in extracted body [25]. |
| Historic MAHE login | `https://slcm.manipal.edu/loginForm.aspx` | Route preserved in archive inventory | Historical structure only [13]. |
| Historic print route | `https://slcm.manipal.edu/Print.aspx` | Route preserved in archive inventory | Function and authentication state not established [13]. |
| Historic generic form | `https://slcm.manipal.edu/WebForm1.aspx` | Route preserved in archive inventory | Function and authentication state not established [13]. |
| Historic password-change routes | `https://slcm.manipal.edu/StudentChangePassword.aspx` and `https://slcm.manipal.edu/ParentChangePassword.aspx` | Role-specific route names preserved in archive inventory | No account or record exposure shown [13]. |
| Searched `/Staff/`, `/Examination/`, and `/Fee/` controller families | No independently indexed current MUJ route verified | Searches returned the root or public MUJ information pages rather than those SLCM controllers | Treat as not verified, not absent. |

Route indexing primarily helps an observer understand controller naming and roles. It is low severity by itself. Attempting to hide all route names offers little protection because authorization must hold even when every URL is known. Nonetheless, search-engine exclusions can reduce noise and automated probing, especially for retired or non-content routes.

**Decision-ready insight:** `/Home/Index` and `/Student` are confirmed current public entry routes. `/Staff/`, `/Examination/`, and `/Fee/` were not independently verified as indexed SLCM pages, while older ASP.NET routes survive in web archives.

## Risk Analysis and Remediation Priorities

### 1. Remove high-density applicant fields first

The fastest privacy reduction comes from the PhD shortlist and result PDFs. Email addresses, internal application numbers, registration numbers, exam-exemption status, and candidature mode should not be published together unless each field is necessary. Replace the files with minimized versions, use masked application references, add `noindex` where public posting remains necessary, and request search-engine cache removal after replacement.

Deleting the current file is not enough. MUJ should search its web roots, content-management system, caches, CDN, backup publication paths, and archive history for duplicates. The PhD page links result documents across multiple admission cycles [19], so remediation should cover the series rather than one PDF.

### 2. Separate scholarly transparency from internal identifiers

The awardee list may have a defensible public purpose: documenting completed research. Keep candidate name, thesis title, department, supervisors, and award year if policy and consent support them. Remove internal registration numbers and full administrative dates unless they serve a clear public function. The current combined fields create a reusable correlation table [32].

### 3. Govern documents like database exports

A PDF or spreadsheet should pass the same privacy review as an API response. MUJ should create a publishing checklist that detects names, registration numbers, application numbers, emails, phones, marks, attendance, fee status, room assignment, and disability or exemption indicators. File metadata and hidden spreadsheet sheets should also be checked before conversion.

### 4. Keep role contacts, reduce personal-contact sprawl

The role-based directory is operationally useful [8]. Preserve those channels, document ownership, and rotate addresses when functions change. Faculty profiles should publish professional contact information only with a clear institutional purpose. Generic admissions telephone numbers should be labeled as such so readers do not mistake them for personal faculty contacts [10].

### 5. Test authorization without enumerating real students

MUJ should commission a controlled assessment using synthetic accounts supplied by the institution. Cover student, parent, staff, and administrator roles; several programs and cohorts; session expiry; password reset; export and print functions; and object ownership. The assessment should verify that changing an object reference never changes the returned student's record unless the role is authorized.

Do not use public registration-number patterns to probe production students. Identifier predictability is a design consideration, not permission to enumerate. Rate limiting, MFA, generic errors, alerting, and object-level checks should ensure that knowing a valid identifier has no security consequence.

### 6. Review third-party code and credential handling

The public projects document user-supplied SLCM credentials [4][24][31]. MUJ should warn students not to enter credentials into untrusted hosted tools, provide supported read-only integration methods if there is legitimate demand, and monitor for credential phishing. A sanctioned OAuth or scoped API would reduce pressure for password-based scraping, but it should expose only the authenticated user's authorized data.

### 7. Manage search and archive persistence

Use `robots.txt` and `X-Robots-Tag` only as secondary controls. They do not revoke a document already copied or archived. Remove or restrict the source object, replace it with a minimized version, request de-indexing, and document legal or policy decisions regarding archives. Retired hosts and historic routes should remain in the asset inventory until DNS, certificates, storage, and application components are fully decommissioned.

**Decision-ready insight:** The remediation order should be applicant emails and identifiers, 500-scale awardee metadata, document-publishing controls, then SLCM authorization and third-party credential governance.

## Synthesis

The evidence divides into three mechanisms with different risk profiles.

First, **official document publication** creates direct, persistent exposure. Its scope is applicant and scholar identity, application or registration identifiers, department, candidature, email in selected lists, thesis history, and supervisory relationships. Its evidence base is strong because the files are hosted on the official MUJ domain. Its time horizon is long because PDFs remain searchable and archivable. Its trade-off is administrative transparency versus privacy. This is the highest-priority risk.

Second, **public portal and archive structure** exposes route names, login roles, framework history, and static assets. Its scope is institutional metadata, not verified student content. Its mechanism is ordinary indexing and archiving. Its evidence base is strong for route existence but weak for any conclusion about vulnerability. The key tension is that route visibility looks technical and alarming, while the actual privacy damage demonstrated in this review comes from documents the university intentionally served.

Third, **public third-party tools and uploads** show demand for SLCM automation and possible redistribution of student lists. Their scope can include marks, attendance, timetable, CGPA, profile details, registration numbers, emails, gender, department, and degree. Their evidence base varies: repository documentation is clear about capabilities and credentials, while Scribd provenance is uncertain. Their trade-off is convenience versus credential trust and data authenticity. They warrant policy and incident review, but they do not prove a no-auth university API.

Across the three mechanisms, the non-obvious divergence is decisive: the most detailed verified data are available without exploiting SLCM at all, while the code that accesses marks and attendance generally requires credentials. This suggests that MUJ's public-exposure program should not be owned only by application security. Registrar, research office, admissions, communications, records management, privacy, and IT operations all control parts of the risk.

The second tension concerns identifiers. Public registration numbers are valuable correlation keys, but the proposed alphanumeric format was not verified. Overstating its semantics could misdirect testing and wrongly associate people or cohorts. The safer policy is format-agnostic: internal identifiers may be predictable, must not act as secrets, and should be removed from public documents when unnecessary.

Finally, the evidence distinguishes **public-by-design professional information** from **unnecessary personal linkage**. A role-based examination email or university switchboard number supports legitimate contact. A candidate email joined to application number, department, candidature, and exemption status creates avoidable privacy exposure. Remediation should preserve the former while minimizing the latter.

## VERDICT

**Overall verdict: MODERATE-HIGH public-data exposure, with HIGH confidence in the verified document and directory findings and MODERATE confidence in the ecosystem-wide completeness.**

The verified exposure includes:

- several official PhD candidate lists containing names and application or registration identifiers;
- email addresses in at least the July 2026 and July 2025 PhD shortlist structures;
- a 500-scale PhD awardee compilation with research and supervisory metadata;
- public SLCM login roles, route names, username-construction guidance, and historical route structure;
- intended staff names, professional emails, office contacts, and hostel contacts; and
- third-party code documenting credentialed retrieval of marks, attendance, timetable, CGPA, and profile information.

The review did **not** verify:

- a current unauthenticated MUJ or MAHE API returning student records;
- a public ASMX/WCF service returning student data without authentication;
- an official undergraduate marks or attendance roster;
- an official hostel-room, seat-allotment, or exam-seating roster;
- a public list of student phone numbers;
- an open `/uploads/`, `/documents/`, or `/files/` directory index; or
- an authoritative explanation of `24JTEECS001` or its alleged year, campus, branch, and sequence components.

The confidence in these negative findings is **moderate**, because search indexes are incomplete, results change, and inaccessible or unindexed public objects may exist. They should be reported as "not verified in this review," never as a guarantee of absence.

The immediate action is clear: minimize or retire official PhD PDFs that expose applicant emails and internal identifiers, review the 500-scale awardee list, validate the third-party student-list claim internally, and perform an authorized object-level access-control assessment with synthetic accounts. Nothing in this report requires or justifies accessing non-public student data.

## References

1. *GitHub - akjha992/MU-SLCM-APP*. https://github.com/akjha992/MU-SLCM-APP
2. *GitHub - Anushkakumar10/muj_slcm*. https://github.com/Anushkakumar10/muj_slcm
3. *Manipal University Jaipur First-Year Student Profile ...*. https://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf
4. *GitHub - tejaskash/slcm-api: A RESTful API to get attendance ...*. https://github.com/tejaskash/slcm-api
5. *slcm-manipal · GitHub*. https://github.com/slcm-manipal
6. *Frequently Asked Questions and Contacts for SLCM Registration*. https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf
7. *Examination - Manipal University Jaipur *. https://jaipur.manipal.edu/examination.php
8. *Contact Us - Manipal University Jaipur *. https://jaipur.manipal.edu/contact-university.php
9. *Hostel Allotment Final.cdr*. https://www.manipal.edu/content/dam/manipal/mu/hostel/pdf/Hostel%20Allotment.pdf
10. *Teaching Faculties*. https://jaipur.manipal.edu/fosta/faculty-details.php?url=69%2F
11. *Teaching Faculties*. https://jaipur.manipal.edu/fosta/faculty-details.php?url=667%2F
12. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=mujslcm.jaipur.manipal.edu/*&output=json&fl=timestamp,original,statuscode,mimetype&filter=statuscode:200&collapse=urlkey
13. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=slcm.manipal.edu/*&output=json&fl=timestamp,original,statuscode,mimetype&filter=statuscode:200&collapse=urlkey
14. *MUJ Teaching Faculty Members  - Manipal University Jaipur *. https://jaipur.manipal.edu/muj-faculties.php
15. *Teaching Faculties*. https://jaipur.manipal.edu/fosta/faculty-details.php
16. *Notification Annual Fee Payment Ay 2025 26*. https://jaipur.manipal.edu/img/pdf/Notification_Annual-Fee-Payment-AY-2025-26.pdf
17. *Pay Fee Online - Manipal University Jaipur *. https://www.jaipur.manipal.edu/pay-fee-online.php
18. *NAAC DOCUMENTS - Manipal University Jaipur*. https://www.jaipur.manipal.edu/NAAC-documents.php
19. *PhD in MUJ - Manipal University Jaipur*. https://jaipur.manipal.edu/research-phd.php
20. *GitHub - manipalthetalk/App-Backend: Scrapes the SLCM for : Marks, Attendance, Timetable, etc. · GitHub*. https://github.com/manipalthetalk/App-Backend
21. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Student
22. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
23. *Manipal University Jaipur Student List | PDF - Scribd*. https://www.scribd.com/document/792426451/Book4
24. *GitHub - frozenparadox99/slcmScraper: Scrapes the slcm manipal portal to give the internal marks after entering the registration number and password · GitHub*. https://github.com/frozenparadox99/slcmScraper
25. [
	MU SLcM
](https://slcm.manipal.edu/)
26. *Phd Admissions Jan 2026 Interview Result List Of Selected Candidates*. https://jaipur.manipal.edu/img/pdf/PhD-ADMISSIONS-JAN-2026-INTERVIEW-RESULT-LIST-OF-SELECTED-CANDIDATES.pdf
27. *Shortlisted candidates list For interview July 2026 compiled.pdf*. https://jaipur.manipal.edu/img/pdf/List-of-Candidates-Eligible-for-PhD-Interview-%28July-2026%29.pdf
28. *elele*. https://jaipur.manipal.edu/img/pdf/PhD-Interview-Results-July-2026.pdf
29. *PhD Entrance Examination – July 2025 List of Shortlisted Candidates Eligible for Interview Exepmt (NET/ Shortlisted Application No. Name Roll*. https://jaipur.manipal.edu/img/pdf/Shortlisted-Candidates-PhD-Exam-July-18072025.pdf
30. *GitHub - canaryGrapher/slcmAPI: The API for SLcM, Manipal. Get your marks, your attendance and your profile details · GitHub*. https://github.com/canaryGrapher/slcmAPI
31. *GitHub - sankalp2004/SLCM-is-Dumb: This extracts cgpa from https://slcm.manipal.edu/ directly and passes captcha · GitHub*. https://github.com/sankalp2004/SLCM-is-Dumb
32. *Total PhD Degree Awardee till date (April-2024)_.xlsx*. https://jaipur.manipal.edu/img/pdf/List-of-PhD-Awarded-(till-2025).pdf
33. *Student Registration Data Overview*. https://www.scribd.com/document/881889937/Eligible-Students-MUJ-1
34. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
35. *Manipal University*. https://muj.slcm.jaipur.manipal.edu/
