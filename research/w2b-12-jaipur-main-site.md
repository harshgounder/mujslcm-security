# MUJ SLCM Public Surface and Defensive OSINT Report

## Executive Summary

- **Primary University Surface**: The official MUJ site uses a large family of human-readable `.php` URLs, including `about-muj.php`, `pay-fee-online.php`, `examination.php`, `faculty-list.php`, and department pages. This establishes a stable public URL convention, but it does **not** independently prove that the whole site runs PHP or that the SLCM application shares the same stack [5] [3]. Action: maintain separate technology inventories for the main website and the SLCM host.
- **SLCM Linkage**: MUJ's own fee page explicitly identifies `https://mujslcm.jaipur.manipal.edu/` as the student-portal URL for online payment and separately states that hostel and mess fees can be paid through SpaceBasic [5]. Action: treat the MUJ SLCM hostname and SpaceBasic as distinct service dependencies.
- **Public Crawl Surface**: `https://jaipur.manipal.edu/sitemap.xml` is publicly retrievable and contains institutional, academic, admissions, faculty, event, compliance, and service routes. Action: use the sitemap as a passive inventory source, not as evidence that every server route is public or reachable.
- **Robots and Asset Policy**: The official robots file disallows `/admin/`, `/common/`, and `/content/`, points crawlers to the sitemap, and states that images and PDFs may be indexed [1]. Action: review whether PDF indexing is intentional and ensure public documents contain no student, staff, payment, or internal metadata.
- **Document Spill Locations**: Observed public asset families include `/img/pdf/exam/`, `/img/announcement/`, fee-page documents under `/img/pdf/`, and department newsletter or program assets under faculty-specific image directories [5] [6] [7] [10]. Action: apply document classification, metadata scrubbing, retention, and link-integrity review to each repository.
- **Staff Exposure**: MUJ exposes a general teaching-faculty page, faculty and school hierarchy, and department pages with names and links to professional profiles such as LinkedIn, IRINS, ORCID, Scopus, Google Scholar, and portfolios [9] [10] [8]. Action: minimize unnecessary personal data and treat public staff information as phishing-enablement data without assuming compromise.
- **System Separation**: The MUJ-specific fee instructions point to `mujslcm.jaipur.manipal.edu`, while a broader MAHE student-portal page points to `https://sis.manipal.edu/index.aspx`; the two pages are different institutional contexts [5] [2]. Action: do not merge MUJ SLCM, MAHE SIS, the online-learning platform, and unrelated Manipal portals into one asset or identity boundary.
- **Technology-Fingerprint Limit**: The supplied brief describes SLCM as ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 identity. The public evidence collected here confirms the portal hostname and visible login labels, but does not independently verify every version, proxy, or identity assertion [16] [17]. Action: validate these details through authorized configuration, asset-management, and vendor records only.
- **Risk Priority**: The most actionable public-surface risks are document governance, cross-domain identity confusion, stale portal links, public staff metadata, and inconsistent canonical hostnames. Action: prioritize inventory and governance before any intrusive testing.

This report is limited to public information and passive collection. It does not provide instructions for authentication bypass, route enumeration against live systems, vulnerability exploitation, credential testing, rate-limit testing, or unauthorized access. References to security implications are labeled **Inference** when they go beyond a direct statement in a source.

## Scope, Evidence Standard, and Safe Reasoning Summary

The research scope is the public MUJ web property at `https://jaipur.manipal.edu/`, its official sitemap and robots files, public pages linked from that property, the MUJ SLCM hostname, and the broader Manipal student-portal page needed to avoid confusing institutions. The principal evidence consists of official MUJ HTML pages, official XML/robots resources, and official portal pages. Third-party search results were used only to locate candidates and were not treated as authoritative when official sources were available.

The reasoning process was: first identify official domains; second collect the sitemap and robots files; third group URLs into institutional, academic, faculty, service, and document families; fourth read official fee, examination, faculty, library, timetable, and disclosure pages; fifth compare the MUJ-specific portal instruction with the MAHE portal page; and finally separate direct observations from inferences. This is a reproducible research summary, not hidden chain-of-thought. The report does not claim that a page's existence proves a vulnerability.

The supplied technology description is an input hypothesis, not a result of this passive collection. A `.php` suffix proves only that the public URL ends in `.php`; it does not prove the server-side framework, PHP version, database, or deployment architecture. Similarly, the presence of an SLCM hostname and MVC-style-looking route such as `/Home/Index` is consistent with an MVC application but does not independently establish the exact MVC, .NET, IIS, Akamai, or Microsoft 365 versions [17] [16].

| Evidence class | Exact public source | What it supports | What it does not support |
|---|---|---|---|
| Main site pages | `https://jaipur.manipal.edu/` | MUJ navigation, services, public notices, external links | A complete server inventory or confirmed framework version |
| Sitemap | `https://jaipur.manipal.edu/sitemap.xml` | Publicly declared URL inventory and route families | That every route is live, indexed, or accessible |
| Robots | `https://jaipur.manipal.edu/robots.txt` | Published crawler directives and sitemap location | Effective access control or security assurance |
| Fee instructions | `https://jaipur.manipal.edu/pay-fee-online.php` | MUJ SLCM link, SpaceBasic reference, payment workflow and contacts | That the linked portals share infrastructure or identity |
| Examination page | `https://jaipur.manipal.edu/examination.php` | Public examination handbook and timetable document paths | That documents are current, private, or free of metadata |
| Faculty list | `https://jaipur.manipal.edu/faculty-list.php` | Public academic hierarchy and service links | That all personnel or accounts are represented |
| SLCM landing page | `https://mujslcm.jaipur.manipal.edu/` | Public portal label, student/parent sign-in labels, forgot-password label | Authenticated functionality or security posture |
| MAHE student portal | `https://manipal.edu/mu/academics/student-portal.html` | Separate MAHE SIS link | That SIS is MUJ's current student system |

The table's central decision insight is that source authority and scope matter more than search-result volume. A public page can establish a link or label, but not the security properties of the linked service.

## Main MUJ Website: URL Conventions and Public Information Architecture

The main MUJ site exposes a broad navigation structure covering architecture and design, arts and humanities, basic sciences, business and commerce, computer applications, engineering, journalism and communication, law, management, and allied health sciences [7]. The homepage also identifies schools such as the School of Computer Science and Engineering, School of Engineering, School of Arts, TAPMI School of Business, and the Faculty of Science, Technology, and Architecture [7].

A repeated public convention is the `.php` suffix. Examples include `about-muj.php`, `pay-fee-online.php`, `examination.php`, `faculty-list.php`, `muj-faculties.php`, `central-library.php`, `mess-fees.php`, `time-table.php`, and department URLs such as `fosta/department-of-information-technology.php` [5] [3] [9] [10]. **Direct observation:** these URLs use `.php`. **Inference:** the site may use PHP-backed routing or legacy file-style URLs, but a URL suffix alone cannot establish the actual runtime, framework, patch level, or hosting model.

The sitemap adds an important structural layer. Representative institutional routes include `about-muj.php`, `board-of-management.php`, `recognition-accrediation.php`, and `vision.php`. Academic routes include `time-table.php`, `academic-rules-regulations.php`, `academics-calender.php`, and `examination.php`. Admissions routes include `admissions.php`, `fee-structure.php`, `indian-program-offered-eligibility.php`, and `admission-contact.php` [3]. Faculty routes include `fosta/faculty-list.php`, `muj-faculties.php`, and `human-resource.php` [3].

The sitemap is therefore useful for defensive asset management. It provides a declared inventory that can be compared with the university's CMS, DNS records, redirect policy, content ownership, and retirement process. It should not be treated as a vulnerability oracle. **Inference:** a sitemap that contains legacy or outdated URLs can increase confusion and maintenance cost, but the evidence gathered here does not establish that any listed route is vulnerable.

## Sitemap, Robots, and Crawlable Surface

The official sitemap is at `https://jaipur.manipal.edu/sitemap.xml`. Its visible contents include URL entries and metadata such as change frequency and priority for at least some routes, including the homepage and institutional pages [3]. The collected document was long and the focused extraction did not provide a reliable exact total of entries, so this report does not claim a precise sitemap count. A local parsing attempt produced noisy false matches because the extracted text included XML metadata and adjacent values; that result is not used as a count.

The official robots file states `User-agent: *`, disallows `/admin/`, `/common/`, and `/content/`, and names the sitemap URL [1]. It also says that images and PDFs are allowed to be indexed for search visibility [1]. **Direct observation:** those directives are published. **Inference:** the policy appears designed to reduce indexing of selected directories while allowing public media and PDF discovery. Robots directives are crawler guidance, not authentication, authorization, network filtering, or confidentiality controls.

| Public control or surface | Exact observed value | Defensive interpretation | Recommended authorized action |
|---|---|---|---|
| Sitemap | `https://jaipur.manipal.edu/sitemap.xml` | Declared route inventory | Reconcile against CMS and retirement records |
| User agent | `*` | Applies broadly to compliant crawlers | Confirm intended scope and ownership |
| Disallowed path | `/admin/` | Administrative path is not requested for indexing | Verify real access control independently and authorizedly |
| Disallowed path | `/common/` | Shared asset/path family is not requested for indexing | Check whether any public files are unintentionally exposed |
| Disallowed path | `/content/` | Content path is not requested for indexing | Confirm no sensitive content is reachable through alternate URLs |
| Asset indexing | Images and PDFs allowed | Documents may appear in search engines | Classify, scrub, expire, and monitor documents |
| Sitemap declaration | `Sitemap: https://jaipur.manipal.edu/sitemap.xml` | Search engines are given a route source | Check canonical host and redirect consistency |

The decision insight is that robots and sitemap should be governed together. If a document is not intended for public discovery, removing it from a sitemap is not enough when the robots policy allows PDF indexing; conversely, disallowing a path does not remove an already indexed document. The correct control is publication authorization plus server-side access control, with search removal procedures where appropriate.

## PDF and Document Spill Locations

The strongest public document evidence comes from official pages that link to exact files. The fee page links an annual fee-payment notification for academic year 2026-27, an NRI fee document, and a transaction-details format. The extracted paths include `https://jaipur.manipal.edu/img/pdf/Annual-Fee-Payment-for-the-AY-2026-2027.pdf`, `https://jaipur.manipal.edu/img/pdf/Annual-Fee-Payment-AY-2026-2027-NRI.pdf`, and a Word document described as `https://jaipur.manipal.edu/img/pdf/Required Transaction details.docx` [5] [5] [5]. The exact links are evidence of public publication, not evidence that the files contain confidential information.

The examination page exposes a more extensive document family under `/img/pdf/exam/`. It links the Student Examination Handbook 2023-24 and component documents such as `1. Cover Front.pdf`, `2. Legacy & Contents.pdf`, `3. Manual Exam Process.pdf`, `4. Appendix I Examination manual MUJ 03 Apr 19.pdf`, `5. Appendix II, III, IV & V.pdf`, `6. Degree nomenclature-Revised-2022.pdf`, and `7. Cover Back.pdf` [6]. It also links examination timetables, including M.Tech and B.Tech higher-semester timetable files for April-May 2025 [6].

The homepage exposes announcement PDFs under `/img/announcement/`, including `Public-Notice-17-10-2025.pdf`, `Public Notice_GULF.pdf`, and `Anant-Ram-UGC.pdf`, as well as a research-facilities PDF under `/img/pdf/research/` [7]. The IT department page shows newsletter assets under a faculty-specific image path, including a file named `IT-COMPENDIUM-JAN-JUNE-2026.pdf` [10]. Search also surfaced official program brochures under `fosta/img-fos/programs/brochure/`, including MCA, BCA, and an MSc Cyber Security booklet.

| Repository family | Exact example | Evidence source | Main governance concern |
|---|---|---|---|
| Fee PDFs | `https://jaipur.manipal.edu/img/pdf/Annual-Fee-Payment-for-the-AY-2026-2027.pdf` | Fee page | Current-year accuracy and payment-data handling |
| Fee attachment | `https://jaipur.manipal.edu/img/pdf/Required Transaction details.docx` | Fee page | Office-document metadata and accidental internal fields |
| Examination PDFs | `https://jaipur.manipal.edu/img/pdf/exam/Student%20Examination%20Handbook%202023-24%20%2811.08.2023%29.pdf` | Examination page | Legacy documents and policy versioning |
| Announcement PDFs | `https://jaipur.manipal.edu/img/announcement/Public-Notice-17-10-2025.pdf` | Homepage | Public notice retention and search indexing |
| Research PDF | `https://jaipur.manipal.edu/img/pdf/research/Flyer-Central%20Research%20Facilities_11zon.pdf` | Homepage | Public institutional information and metadata |
| Faculty newsletter | `https://jaipur.manipal.edu/fosta/img/programs/news-letter/IT-COMPENDIUM-JAN-JUNE-2026.pdf` | IT department page | Department ownership and stale content |
| Program brochures | `https://jaipur.manipal.edu/fosta/img-fos/programs/brochure/MSc%20-%20Cyber%20Secqurity%20Booklet_compressed.pdf` | Search result from official domain | Naming quality, accessibility, and retention |

**Inference:** predictable asset directories and descriptive filenames improve discoverability for legitimate users but also make document governance important. The safe response is not to hide public documents with robots alone. It is to ensure that every file is approved for publication, contains no credentials or personal records, has a clear owner and review date, and is removed or replaced when obsolete.

## Faculty, Staff, and Academic Profile Surface

The official faculty-list page identifies four broad faculties: Faculty of Science, Technology and Architecture; Faculty of Management, Commerce and Arts; Faculty of Law; and Faculty of Health Sciences [9]. It lists schools and departments including Computer Science and Engineering, Information Technology, Artificial Intelligence and Machine Learning, Internet of Things and Information Systems, Data Science and Engineering, Computer Applications, Civil Engineering, Mechanical Engineering, Electrical Engineering, Electronics and Communication Engineering, Management, Commerce, Hotel Management, Law, Psychology, and allied health areas [9].

The same page links public institutional functions including campus tour, online grievance registration, Radio Manipal Jaipur, degree verification, online courses, anti-ragging measures, equal opportunity resources, teaching faculty details, timetable, academic rules, and the academic calendar [9]. This makes the faculty page more than a directory: it is also a service-navigation node.

The teaching-faculty page is explicitly titled “MUJ Teaching Faculty Members” and publicly lists faculty names [8]. Department pages add profile metadata and external professional links. The IT page identifies academic staff and links to LinkedIn, IRINS, ORCID, Scopus, Google Scholar, and a portfolio for some profiles [10]. The CSE page likewise exposes public faculty metadata and external profile links [11].

| Public staff surface | Exact URL | Directly observed content | Defensive implication, labeled inference |
|---|---|---|---|
| General faculty hierarchy | `https://jaipur.manipal.edu/faculty-list.php` | Faculties, schools, departments, service links | **Inference:** useful for role-based phishing reconnaissance; minimize excess data |
| Teaching faculty | `https://jaipur.manipal.edu/muj-faculties.php` | Names and faculty listing | **Inference:** stale names or roles can create impersonation risk |
| IT department | `https://jaipur.manipal.edu/fosta/department-of-information-technology.php` | Staff profiles and external research links | **Inference:** link governance and privacy review are appropriate |
| CSE department | `https://jaipur.manipal.edu/fosta/department-of-Computer-Science-Engineering.php` | Department and faculty profile fields | **Inference:** public academic metadata should be separated from operational account data |

No evidence collected here establishes that staff pages reveal passwords, authentication tokens, private phone numbers, or administrative credentials. The security club should avoid collecting more personal information than necessary. For a defensive inventory, role, department, public page URL, and official contact channel are generally sufficient.

## Campus Systems and Portal Instructions

The MUJ fee page is the clearest official SLCM instruction. It labels an “Existing Students” section, gives the “Online mode of payment Student Portal URL” as `https://mujslcm.jaipur.manipal.edu/`, and says hostel and mess fees can be paid through the SpaceBasic app [5]. It also gives a payment workflow involving transfer details and asks students or parents to email transaction details to `student.finance@jaipur.manipal.edu`, including UTR number, debit-account-holder name, transaction date, and amount [5]. Because these are financial instructions, the page should be treated as a high-value integrity target.

The MUJ portal landing page publicly shows “WELCOME TO MUJ PORTAL,” student and parent sign-in labels, a `@muj.manipal.edu` label, and “Forgot Password?” [16] [17]. A second hostname, `https://muj.slcm.jaipur.manipal.edu/`, also appears in public search results with MUJ portal labels [18]. **Inference:** the two hostnames may be aliases or related deployment names, but the collected evidence does not prove canonicalization, ownership, or whether they have identical behavior. Those questions belong in authorized DNS, certificate, CDN, and application inventory work.

The broader MAHE student-portal page points to `https://sis.manipal.edu/index.aspx` [2]. That page is titled for MAHE, not specifically MUJ. Therefore, it should not be used to claim that MUJ's campus students use SIS. The research also found an online-learning login at `https://learning.onlinemanipal.com/d2l/home/14042`, described as the MUJ Centre for Distance and Online Education login [19], and MUJ online education at `https://muj.onlinemanipal.com/` [20]. These are distinct services and should be represented separately.

| System or service | Exact URL | Institutional scope from evidence | Inventory treatment |
|---|---|---|---|
| MUJ SLCM portal | `https://mujslcm.jaipur.manipal.edu/` | Directly linked by MUJ fee instructions | MUJ student/parent portal candidate; verify ownership internally |
| Alternate SLCM hostname | `https://muj.slcm.jaipur.manipal.edu/` | Publicly labeled MUJ portal | Track as related hostname until canonical relationship is confirmed |
| SpaceBasic | App named on MUJ fee page; no exact app URL in evidence | Hostel and mess fee workflow | Third-party dependency; document owner and integration boundary |
| MAHE SIS | `https://sis.manipal.edu/index.aspx` | Linked from broader MAHE student-portal page | Do not assume MUJ scope |
| Online learning | `https://learning.onlinemanipal.com/d2l/home/14042` | MUJ online education login | Separate learning-service asset |
| Online Manipal | `https://muj.onlinemanipal.com/` | MUJ online education | Separate domain and identity dependency |
| Admissions | `https://admissions.jaipur.manipal.edu/` | Homepage Apply Now destination | Separate admissions asset |
| Degree verification | `https://muj.onlinemanipal.com/degree-verification` | Listed as a public service link | Track workflow and data owner separately |

The decision insight is that the public ecosystem is a service graph, not a single application. Confusing domains can lead users to disclose credentials or payment information to the wrong destination. The university should publish a canonical service directory with service name, official hostname, purpose, owner, identity provider, support channel, and retirement status.

## Security-Relevant Observations and Defensive Actions

**Inference - document exposure:** Since the robots file permits PDF indexing and official pages publish many predictable document paths, public files may be easy for search engines to discover [1]. This is not a vulnerability by itself. The control objective is content governance: scan approved documents before publication, remove hidden author and revision metadata, check embedded links, ensure no student identifiers or internal paths are present, assign expiry dates, and maintain a takedown process.

**Inference - identity confusion:** The ecosystem contains MUJ SLCM, an alternate-looking SLCM hostname, MAHE SIS, Online Manipal, an online-learning host, admissions, degree verification, SpaceBasic, and a WhatsApp destination [5] [7]. Multiple services are normal for a university, but inconsistent labels or redirects could increase user confusion. The defensive control is a verified service catalog, canonical HTTPS URLs, consistent branding, explicit login warnings, and support guidance that never asks users to send passwords.

**Inference - financial integrity:** The fee page publishes payment instructions, bank details, a student-finance email address, and a request for transaction details [5]. This makes integrity and change control important. The university should use monitored page ownership, dual approval for payment-instruction changes, cryptographic or administrative integrity monitoring, prominent “last reviewed” labels, and an independent support channel for payment verification. The club should not attempt to validate bank details through live transactions.

**Inference - staff metadata:** Public faculty pages and external profile links can help legitimate students but can also support targeted social engineering [9] [10]. Recommended controls include limiting personal contact fields, using role-based institutional addresses, reviewing departed-staff profiles, separating public research links from operational account identifiers, and providing phishing-awareness training to faculty and finance staff.

**Inference - stale documents and routes:** Examination materials include documents from different academic years, such as 2023-24 handbooks and 2025 timetables [6]. This is not evidence of a flaw. It does create a governance question: users may mistake an old handbook or timetable for a current one. Use explicit academic-year labels, archive banners, content owners, and automatic review queues.

| Priority | Defensive issue | Evidence | Safe remediation |
|---|---|---|---|
| High | Payment-instruction integrity | Fee page contains portal, bank, email, and transaction workflow [5] | Dual approval, change monitoring, independent verification channel |
| High | Document governance | PDF indexing is allowed and multiple asset families are public [1] [6] | Publication review, metadata scrubbing, expiry and takedown process |
| High | Service/identity confusion | MUJ, MAHE, online, admissions, and third-party services coexist [5] [2] | Canonical service catalog and consistent branding |
| Medium | Staff-profile exposure | Faculty and external profile links are public [9] [10] | Minimize data, review departures, train against impersonation |
| Medium | Stale academic content | Mixed-year examination documents are linked [6] | Academic-year labeling and owner review queues |
| Medium | Hostname ambiguity | MUJ SLCM appears under related hostnames [16] [18] | Confirm canonical hostname and redirect policy internally |

## What Remains Unanswered

The public evidence does not independently verify the supplied claims that SLCM uses ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, or Microsoft 365 identity. Those may be accurate internal or previously observed facts, but they are not established by the official pages collected here. The report therefore treats them as supplied hypotheses. Confirming them safely requires authorized configuration records, CMDB data, vendor documentation, approved headers or telemetry, and identity-architecture diagrams.

The evidence also does not establish whether `/admin/`, `/common/`, or `/content/` are actually inaccessible, whether PDFs contain sensitive metadata, whether the portal has vulnerabilities, whether authentication is federated, whether the alternate SLCM hostname is a redirect or separate deployment, or whether the sitemap lists every current route. No claim of security weakness should be made from these gaps. They are verification tasks for the university's authorized security team.

The exact count of sitemap entries is also unanswered. The sitemap is visibly extensive, but the extracted preview did not yield a reliable count, and this report intentionally avoids presenting a noisy parser result as fact. The public material likewise does not provide a complete official campus-systems directory, a definitive owner for every third-party link, or a current retention schedule for all documents.

## Synthesis

Across four dimensions, the ecosystem is best understood as distributed rather than monolithic. **Scope:** the main MUJ site is a content and navigation surface; SLCM is a student/parent portal; MAHE SIS belongs to a broader institutional context; online learning and admissions are separate services; and SpaceBasic is named for hostel and mess fees [5] [2] [19]. **Mechanism:** the main site publishes links and documents, while the portals provide sign-in or workflow destinations. **Trade-off:** centralizing navigation helps users, but cross-domain dependencies increase the chance of stale links, inconsistent branding, and unclear data ownership.

The most important tension is between discoverability and confidentiality. MUJ's robots file expressly allows images and PDFs to be indexed, and the site publishes detailed examination, fee, announcement, research, program, and newsletter assets [1] [5] [6]. Discoverability supports students, applicants, and researchers. The same mechanism can expose obsolete documents or metadata if publication review is weak. The correct conclusion is not that public PDFs are inherently unsafe; it is that publication permission, retention, classification, and metadata hygiene must be treated as security controls.

A second tension is between transparency and staff-targeting risk. Faculty pages provide academic structure and professional links that are useful for legitimate engagement [9] [10]. They may also make impersonation more credible. The balanced strategy is not to remove all faculty information. It is to publish only what serves an educational purpose, prefer institutional contact channels, remove stale profiles, and train staff to treat payment or Microsoft 365 credential requests as suspicious.

A third tension concerns technology certainty. The user-supplied SLCM fingerprint is specific, but the public evidence is mostly application labels and URLs [17] [16]. Treating a reported fingerprint as verified would risk conflating historical, edge, or unrelated infrastructure. The security club should record it as an unverified hypothesis until authorized evidence confirms it. This distinction is especially important when planning remediation: framework patching, IIS hardening, Akamai policy, and Microsoft 365 identity controls are different workstreams.

The practical synthesis is a governance-first program: maintain one authoritative asset register; map each hostname to service, owner, identity provider, data class, and support contact; review documents before publication; monitor payment pages for unauthorized changes; and preserve clear boundaries between public observation and authorized testing. The public surface is substantial but understandable, and its main defensive value lies in making ownership and publication decisions explicit.

## VERDICT

**Overall confidence: High for the public-surface findings; medium for ecosystem relationships; low for unverified technology-version claims.**

High-confidence findings are the exact public URLs, visible portal labels, official fee-page linkage to MUJ SLCM, SpaceBasic reference, sitemap location, robots directives, faculty-page existence, and documented PDF path families. These are directly supported by official MUJ or Manipal pages [5] [1] [9].

Medium-confidence findings include the interpretation that the alternate SLCM hostname is related to the primary MUJ SLCM host, that predictable document paths materially increase discoverability, and that multiple domains create identity confusion risk. These are explicitly labeled inferences, not findings of exploitation or compromise.

Low-confidence or unresolved claims include the exact SLCM framework and server versions, Akamai deployment details, Microsoft 365 identity integration, authenticated route behavior, access-control effectiveness, vulnerability status, and the exact sitemap entry count. The public research performed here does not establish those facts. They should be confirmed only through authorized internal evidence.

**Final decision:** the collected material is sufficient for a university security club's passive, public-information inventory and defensive prioritization. It is not sufficient to declare a vulnerability, infer unauthorized access, or validate the supplied runtime fingerprint. The next safe step is an owner-approved internal review of the asset register, document repositories, canonical hostnames, identity boundaries, and payment-page change controls.

## References

1. *jaipur.manipal.edu*. https://jaipur.manipal.edu/robots.txt
2. *Student Portal Login- MAHE (Manipal Academy Of Higher Education)*. https://manipal.edu/mu/academics/student-portal.html
3. *jaipur.manipal.edu*. https://jaipur.manipal.edu/sitemap.xml
4. *About MUJ - Manipal University Jaipur*. https://jaipur.manipal.edu/about-muj.php
5. *Pay Fee Online - Manipal University Jaipur *. https://jaipur.manipal.edu/pay-fee-online.php
6. *Examination - Manipal University Jaipur *. https://jaipur.manipal.edu/examination.php
7. *Manipal University Jaipur - 71 years of legacy of Manipal Education*. https://jaipur.manipal.edu/
8. *MUJ Teaching Faculty Members  - Manipal University Jaipur *. https://jaipur.manipal.edu/muj-faculties.php
9. *Faculty List | Faculty of Arts(FOA) At  Manipal University Jaipur, MUJ*. https://jaipur.manipal.edu/faculty-list.php
10. *Department of Information Technology| Faculty of Science, Technology and Architecture (FoSTA) At MUJ*. https://jaipur.manipal.edu/fosta/department-of-information-technology.php
11. *Department of Computer Science & Engineering| Faculty of Science, Technology and Architecture (FoSTA) at MUJ*. https://jaipur.manipal.edu/fosta/department-of-Computer-Science-Engineering.php
12. *Mandatory Disclosures & Reports - Manipal University Jaipur *. https://jaipur.manipal.edu/mandatory-disclosure.php
13. *Time Table - Manipal University Jaipur *. https://jaipur.manipal.edu/time-table.php
14. *MESS FEE - Manipal University Jaipur*. https://jaipur.manipal.edu/mess-fees.php
15. *Library - Manipal University Jaipur *. https://jaipur.manipal.edu/central-library.php
16. *muj portal - Manipal University*. http://mujslcm.jaipur.manipal.edu/
17. *Manipal University - mujslcm.jaipur.manipal.edu*. https://mujslcm.jaipur.manipal.edu/Home/Index
18. *Manipal University*. https://muj.slcm.jaipur.manipal.edu/
19. *Login - Manipal University Jaipur*. https://learning.onlinemanipal.com/d2l/home/14042
20. *Manipal University Jaipur - Online Manipal*. https://muj.onlinemanipal.com/
