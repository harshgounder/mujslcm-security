# MUJ SLCM and Faculty Directory Exposure Assessment

## Executive Summary

- **Public Directory Exists**: MUJ exposes an official teaching-faculty entry point, school pages, department pages, leadership pages, and individual faculty-detail URLs. The public self-disclosure document itself identifies `muj-faculties.php` as the location for department or school-wise faculty/staff details with photographs [16]. **Action**: treat the institutional website, not the SLCM portal, as the primary public-directory surface.

- **Enumeration Is Substantial but Not Complete**: A visitor can move from the public MUJ navigation to faculties, schools, departments, leadership pages, and profile records without evidence in the reviewed material that an account is required. The FoSTA faculty page exposes four school groupings and 18 department labels in its visible navigation, but it does not establish the number of people in the directory [14]. **Action**: describe the surface as "publicly navigable and materially enumerable," not as a proven complete staff database.

- **Personal and Professional Fields Are Published**: Representative profiles expose a name, academic designation, department, institutional email, and sometimes telephone number. They may also include qualifications, expertise, responsibilities, professional memberships, and research-profile links [11][17][12][9]. **Action**: minimize collection, avoid reproducing personal phone numbers in club materials, and use role mailboxes for legitimate contact.

- **Official Counts Do Not Reconcile**: MUJ's home page states that a team of 700 faculty members is an asset of the university [2], while the CSE department page says it has around 120 faculty members [18]. The public faculty index does not provide an explicit total in the inspected content [6]. **Action**: do not estimate directory completeness by comparing these figures with visible cards.

- **Contact Metadata Is Broad**: The official contact page publishes 14 office rows, including academics, admissions, examinations, human resources, IT infrastructure, registrar, student welfare, training and placement, and webmaster contacts. Many rows include telephone or extension values and role-based email addresses [4]. **Action**: classify this as operational contact metadata, not as proof of an application vulnerability.

- **SLCM Public Surface Is a Login Boundary**: The landing page publicly displays "WELCOME TO MUJ PORTAL," "Sign In," and "Sign In Parent Login" [1]. The public page does not demonstrate successful authentication, student records, staff records, authorization failure, or any exposed post-login function. **Action**: stop analysis at the unauthenticated landing page unless MUJ grants written authorization.

- **Identity and IT Context Are Publicly Described, Not Security-Tested**: MUJ's IT page explicitly discusses ERP, LMS, cloud-based solutions, networks, server infrastructure, backups, telecommunications, IT security, and Microsoft services [8]. The SLCM FAQ links the registration process to the SLCM host and refers to official Outlook identity and AMS support [15]. **Action**: record these as institutional descriptions, not as independently verified technology fingerprints.

- **Photograph Coverage Is Not Reliably Counted**: The self-disclosure document says the faculty/staff-details category includes photographs [16], but the inspected extracted profile text did not provide a reliable count of individual images. Raw markup fragments visibly included university branding imagery, which is not sufficient to prove that every profile exposes a portrait. **Action**: report photo availability as institutionally claimed but not quantitatively verified.

- **Risk Is Primarily Privacy and Reconnaissance Risk**: Public names, roles, department relationships, institutional email conventions, office extensions, and IT-support contacts can make legitimate communication easier while also reducing the effort needed for targeted social engineering. This is an inference from the combination of published fields, not evidence that MUJ has suffered an incident. **Action**: review the directory for data minimization, stale records, unnecessary direct numbers, and consistent role-mailbox use.

## Scope, Evidence Standard, and Safety Boundary

This report assesses only information presented through public MUJ web pages and public institutional documents. It does not claim to have performed vulnerability scanning, endpoint discovery, parameter fuzzing, authentication testing, password testing, directory brute force, range enumeration, scraping at scale, or access to student, parent, employee, or administrative records. No login was attempted. The report therefore answers a bounded OSINT question: what information is intentionally or incidentally reachable through ordinary public navigation and indexed documents?

The supplied technology description names ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 identity. The reviewed public evidence confirms a portal host and publicly described Microsoft-related services, but it does not independently confirm every version, reverse-proxy, or identity-provider assertion. The correct classification is therefore: **publicly supplied context, partially corroborated institutional context, and unverified implementation detail**. A page title or URL is not proof of a specific server framework, and a public Microsoft-related service description is not proof that the SLCM login flow uses a particular tenant, federation mode, or protocol.

The official MUJ public self-disclosure document is important because it expressly links the "Department/School/Centre Wise Faculty/Staff Details with Photographs" item to `https://jaipur.manipal.edu/muj-faculties.php` [16]. That makes the faculty directory a legitimate public-information subject rather than an inferred hidden asset. It does not, however, imply that every staff member, historical employee, contractor, or account holder appears there.

## Public Directory Architecture and Navigation

The public website presents several layers. At the highest level are faculty-of-study pages such as FoSTA, FoMCA, Faculty of Law, and Faculty of Health Sciences [2]. Within FoSTA, the inspected public navigation identifies the School of Computer Science and Engineering, School of Engineering, School of Physical and Biological Sciences, and School of Architecture and Design [14]. The same navigation names departments beneath those schools, including CSE, Information Technology, Artificial Intelligence and Machine Learning, IoT and Intelligent Systems, Computer and Communication Engineering, Data Science and Engineering, Computer Applications, Civil Engineering, Mechanical Engineering, Mechatronics Engineering, Electrical Engineering, Electronics and Communication Engineering, Biosciences, Chemistry, Mathematics and Statistics, Physics, Architecture, Fashion Design, Interior Design, and Interaction and Communication Design [14].

The site also exposes leadership routes. The FoSTA all-faculties page visibly labels a dean, associate deans, a director, and heads for departments including CSE, IT, AI and ML, IoT and Intelligent Systems, CCE, Data Science and Engineering, Computer Applications, Biotechnology and Chemical Engineering, Civil Engineering, Mechanical Engineering, Mechatronics Engineering, Electrical Engineering, Electronics and Communication Engineering, Architecture, Fashion Design, Interior Design, Interaction and Communication Design, Physics, Chemistry, Mathematics and Statistics, and Biosciences [14]. These are navigation labels and role categories, not a count of unique individuals.

The no-parameter `faculty-details.php` page is a useful negative finding. Its extracted public content contains the "Teaching Faculties" heading, "All Faculties," and "Faculty Details," as well as the school and department navigation, but it does not expose an explicit total faculty count in the inspected content [14]. The official index therefore acts as a directory entry point without providing a reliable denominator for a completeness calculation.

| Public layer | Evidence observed | What it establishes | What it does not establish |
|---|---|---|---|
| University home | Four faculty links are visible: FoSTA, FoMCA, FoL, and FoHS [2] | Multiple public academic areas exist | That every university unit is represented |
| FoSTA navigation | Four schools and department labels are visible [14] | A hierarchical public navigation model | Number of current people in each department |
| Faculty index | "Teaching Faculties," "All Faculties," and "Faculty Details" are visible [14] | A public directory entry point exists | Exact total, complete staff coverage, or historical coverage |
| Department page | CSE page states around 120 faculty [18] | An official department-level approximate figure | That 120 profiles are all publicly visible |
| Institutional home | MUJ states a 700-faculty team [2] | An official institution-level approximate figure | That the public directory contains 700 records |
| Self-disclosure PDF | Faculty/staff details with photographs links to `muj-faculties.php` [16] | MUJ identifies the directory as a public disclosure location | That every photograph is currently retrievable or indexed |

**Takeaway:** navigation coverage is high, while denominator quality is low. A security club should measure exposure by documented fields and reachable categories, not by claiming a percentage of all staff unless MUJ supplies an authoritative roster and a defined census date.

## Faculty Records: Fields and Representative Exposure

The inspected CSE profiles demonstrate a repeatable professional-record pattern. Dr. Neha Chaudhary's page displays her name, the designation Professor and HoD, the Department of Computer Science and Engineering, an institutional email address, a telephone number, education history, area of expertise, an achievement, responsibility, professional membership, and ORCID, Scopus, Google Scholar, and IRINS-related links [11]. This is enough to establish that public records can combine identity, role, contact, biography, and external research identity in one page.

Other profiles show that the field set is not perfectly uniform. Dr. Chhatar Singh Lamba's extracted page exposes name, rank, department, institutional email, telephone, LinkedIn, qualifications, and areas including software engineering and information security [17]. Dr. Ankit Shrivastava's record shows name, assistant-professor designation, CSE department, institutional email, LinkedIn, and a qualifications section [12]. Dr. Roheet Bhatnagar's record shows name, rank, department, email, telephone, LinkedIn, IRINS, education, and software-engineering/database expertise [9]. The variation matters: a directory may be publicly enumerable even when individual records differ in completeness.

| Representative record | Publicly visible professional fields | Privacy/security interpretation |
|---|---|---|
| Dr. Neha Chaudhary | Name, Professor and HoD role, CSE, institutional email, phone, qualifications, expertise, achievement, responsibility, membership, research links [11] | Rich single-record aggregation; useful for professional contact, also useful for targeted impersonation attempts. Inference. |
| Dr. Chhatar Singh Lamba | Name, Professor and Associate Dean role, CSE, institutional email, phone, LinkedIn, qualifications, expertise [17] | Leadership and external-profile correlation are public. Inference. |
| Dr. Ankit Shrivastava | Name, Assistant Professor Senior Scale, CSE, institutional email, LinkedIn, qualifications section [12] | Email and role are public; phone exposure is not established by the visible excerpt. |
| Dr. Roheet Bhatnagar | Name, Professor and Associate Dean role, CSE, email, phone, LinkedIn, IRINS, qualifications, expertise [9] | Multi-channel research and professional identity is publicly linked. Inference. |
| FoMCA example | Name, designation, department, email, phone, LinkedIn/profile links, qualifications, expertise, achievements, responsibilities, memberships, and publication links [3] | The pattern extends beyond engineering, though field completeness varies. |

A key distinction is between **publicly visible** and **publicly enumerable**. A single profile proves visibility. A directory index plus public detail links proves a navigation path. A complete census requires more: an explicit count, stable inclusion criteria, and a way to determine whether profiles are omitted, duplicated, stale, or loaded only after a user action. The inspected material does not provide that completeness proof.

Photos deserve careful treatment. MUJ's self-disclosure document explicitly describes the public faculty/staff category as including photographs [16]. However, the cleaned profile evidence for the representative CSE page shows textual fields and a university-logo image reference in raw markup inspection, not a reliable portrait inventory. It would be inappropriate to convert the institution's category label into a claim that every current profile contains a photo. The safe conclusion is **photo capability or intended publication is documented; current per-profile photo coverage is not quantitatively verified**.

## Department Coverage and Directory Completeness

The CSE department page states that it has around 120 faculty members and describes a broad research footprint, including network security, cyber security, software engineering, cloud computing, digital forensics, and related areas [18]. The department page is therefore useful for organizational context and a high-level count, but it is not a census of public profile pages. The word "around" is a built-in qualifier, and the page does not establish the date, employment-status categories, or whether visiting, adjunct, research, and administrative personnel are included.

The university home page separately states that more than 14,000 students are enrolled and that a well-qualified team of 700 faculty members is the university's asset [2]. That statement is materially different in scope from the CSE estimate. It likely refers to the whole university, while the CSE statement refers to one department, but that relationship is an interpretation and should be labeled as such. Even if the two statements are directionally consistent, they cannot be used to calculate public-directory coverage because the public index does not expose a verified total [6].

FoMCA pages show another form of incompleteness risk. The page names schools and departments including Business Administration, Commerce, Hotel Management, TAPMI School of Business, Economics, and Liberal Arts and Social Sciences [3]. It displays "View all members" and previous/next controls, but no explicit total faculty count is shown; one displayed "Faculty Members Hold PhD" value is `0`, which appears inconsistent with the surrounding faculty content and should not be interpreted as a real faculty census [3]. This is a data-quality warning: public content can contain stale, template-derived, or malformed counters.

| Completeness question | Finding | Confidence |
|---|---|---|
| Is there a public faculty entry point? | Yes: MUJ identifies `muj-faculties.php` for faculty/staff details with photographs [16]. | High |
| Are departments publicly navigable? | Yes: FoSTA exposes school and department navigation [14]. | High |
| Are individual profiles publicly reachable? | Yes: representative detail URLs expose faculty records [11][17]. | High |
| Is the exact directory total published? | Not in the inspected index content [6]. | High for this bounded observation |
| Is the directory equal to all MUJ faculty? | Not established. The 700-faculty institutional statement is not a directory count [2]. | High |
| Is all non-teaching staff included? | Not established; the principal entry point is titled Teaching Faculties [14]. | High |
| Are photos present on every profile? | Not established; self-disclosure says the category includes photographs [16], but no reliable per-profile count was obtained. | Medium-high |
| Is pagination proof of a fixed total? | No. Previous/next controls are visible on FoMCA [3], but no total is shown. | High |

**Inference:** the public directory is likely a substantial subset of academic personnel, organized for ordinary public discovery, but its percentage coverage cannot be responsibly stated. The strongest defensible wording is "publicly enumerable across multiple organizational paths, with completeness unknown."

## Extension and Office Contact Exposure

The official contact page publishes an important-contacts table with 14 rows. The rows include Academics, Admissions, Controller of Examinations, Chief Warden Office, Chief Officer for General Services and Administration, Chief Finance Officer, Student Finance, Human Resources, IT Infra, Library, Registrar Office, Student Welfare, Training and Placement, and Webmaster [4]. The table includes role mailboxes and, for many entries, phone numbers or extensions. This is not a hidden directory finding: it is an explicit institutional contact page.

The SLCM FAQ adds a second support layer. It identifies the SLCM registration link, the university helpline, AMS/DMS support mailboxes, IT support, and several extension values [15]. It also says that personal details in the SLCM portal are changed through admissions after verification [15]. That statement is relevant to data governance because it confirms that the portal handles personal details, while also directing users to an administrative correction process. This report intentionally does not reproduce the example username or any password guidance from the FAQ.

| Office or function | Public contact data category | Source |
|---|---|---|
| Academics | Main phone, extension 263, academic and AMS role mailboxes [4] | Official contact page |
| Admissions | Extensions 142, 257, 297 and admissions mailbox [4] | Official contact page |
| Examinations | Phone 204 and COE mailbox [4] | Official contact page |
| Chief Warden | Phones/extensions 108 and 493 and role mailbox [4] | Official contact page |
| General Services and Administration | Phones/extensions 119 and 105 and admin mailbox [4] | Official contact page |
| Finance and Student Finance | Finance phone/extension and student-finance extensions/mailbox [4] | Official contact page |
| Human Resources | Extensions 666, 253, 728 and HR mailbox [4] | Official contact page |
| IT Infrastructure | Extensions 778 and 300 and IT-support mailbox [4] | Official contact page |
| Library, Registrar, Student Welfare | Role mailboxes and listed phones/extensions [4] | Official contact page |
| Training and Placement | Extension 751 and TPO mailbox [4] | Official contact page |
| Webmaster | Webmaster mailbox; phone shown as a dash [4] | Official contact page |

The table creates operational convenience and a possible social-engineering concern. That concern is an inference: an attacker could correlate departments, names, titles, and support contacts to make a message appear credible. The public evidence does not show that any contact was abused, that a mailbox is misconfigured, or that an extension is directly reachable from outside the campus telephony system. The appropriate control response is review and minimization, not removal of legitimate academic contact channels by default.

## SLCM, Microsoft Identity, and Technology Context

The public SLCM landing page is minimal. It displays the MUJ portal welcome message, a sign-in option, and a parent-login option [1]. The search result also describes student login and a forgot-password route [1]. These observations establish a public authentication boundary, not a weakness. There is no evidence in the reviewed public page that authentication can be bypassed, that a user can enumerate accounts, or that post-login resources are public.

The official SLCM FAQ identifies `https://mujslcm.jaipur.manipal.edu/` as the registration link [15]. It refers to official Outlook identity in its account-support context and lists AMS/DMS and IT support contacts [15]. This supports the narrower statement that MUJ publicly documents a relationship among SLCM, AMS, and institutional Outlook support. It does not independently prove Microsoft 365 tenant configuration, federation, conditional access, MFA, token claims, or the framework versions named in the question.

MUJ's Digital Infrastructure and Technology Services page explicitly describes cloud-based solutions, advanced networking, ERP, LMS, network and server infrastructure, data communications, backup strategies, telecommunications systems, and IT security [8]. It also explicitly references Microsoft services for communication and business ERP, a student-life-cycle web portal, an LMS, and a research management system [8]. These statements are useful for asset-management context. They should not be turned into a fingerprinting claim such as "the portal is definitely running framework X behind provider Y" without a public technical document or authorized testing.

| Technology statement | Public evidence | Proper conclusion |
|---|---|---|
| SLCM host | Official FAQ links the registration URL [15] | The host is an official documented portal entry point |
| Login boundary | Landing page shows welcome and sign-in options [1] | Authentication is presented publicly; no bypass is shown |
| Outlook/AMS support relationship | FAQ mentions official Outlook identity and AMS support [15] | Institutional identity/support relationship is documented |
| ERP/LMS and infrastructure | MUJ IT page lists ERP, LMS, networks, servers, backups, telecom, and IT security [8] | Institutional service scope is publicly described |
| Microsoft services | MUJ IT page says the IT landscape includes Microsoft services [8] | Microsoft use is institutionally stated; exact SLCM implementation is not proven |
| ASP.NET MVC, .NET, IIS, Akamai | Not independently established by the reviewed excerpts | Treat supplied stack as unverified context |

## Privacy, Data Minimization, and Responsible Club Practice

The public directory contains data that has clear legitimate uses: students need to identify a department, prospective applicants need academic contacts, researchers need professional affiliations, and the public may need institutional leadership information. The same data can create unnecessary exposure when a page combines direct email, direct phone, detailed biography, external identifiers, and organizational responsibility in one record. This is an inference from the field combination, not a claim of unlawful processing or a security incident.

A university security club should therefore use a data-minimization model. Record the URL, page category, field categories, and a small number of redacted examples. Do not build a downloadable staff dossier. Do not publish personal mobile numbers, sample account identifiers, or a full email corpus. Do not correlate faculty records with social-media profiles unless the research question requires it and the result is kept private. Do not use the SLCM FAQ's sample credential format as a test input.

| Control area | Safe club practice | Why it matters |
|---|---|---|
| Collection | Capture field types and representative, redacted records rather than bulk personal data | Reduces privacy and redistribution risk. Recommendation based on observed public fields [11]. |
| Contact | Use role mailboxes such as webmaster, IT support, AMS, or academic contacts for disclosure | These channels are explicitly published by MUJ [4][15]. |
| Authentication | Do not submit credentials, attempt password recovery, or test account existence | The reviewed evidence shows only a login boundary [1]. |
| Enumeration | Do not guess profile IDs, probe parameter ranges, or automate harvesting | Exact completeness is unresolved; unauthorized discovery is out of scope. |
| Photos | Note whether a page states photographs are part of the disclosure category, but do not copy portraits into a report | MUJ's self-disclosure document mentions photographs [16]. |
| Reporting | Separate observed fact, institutional claim, and inference in different columns | Prevents approximate counts and technology descriptions becoming false certainty. |
| Retention | Keep notes access-controlled and delete unnecessary personal data after the project | Limits secondary exposure created by the research itself. |

If the club identifies a suspected issue, it should send a concise report to an official MUJ contact, explain that no unauthorized access was attempted, include the minimum reproducible public URL, and request a preferred disclosure channel. The official contact page lists webmaster and IT infrastructure role mailboxes [4], while the SLCM FAQ lists AMS/DMS and IT support channels [15]. The club should not attach bulk directory dumps or employee phone lists.

## What Is Publicly Enumerable, and What Is Not

The following exposure tiers distinguish evidence from inference.

| Exposure tier | Publicly supported finding | Assessment |
|---|---|---|
| Tier 1: Direct navigation | Faculty-of-study, school, department, leadership, contact, and SLCM landing pages are linked or indexed [2][14] | High confidence |
| Tier 2: Profile records | Representative faculty detail pages expose professional identity and contact fields [11][17][12][9] | High confidence |
| Tier 3: Organizational mapping | Department heads, schools, departments, and office functions can be mapped from public pages [14][4] | High confidence |
| Tier 4: Contact correlation | Role mailboxes, extensions, academic titles, and departments can be correlated [4][11] | High confidence; privacy impact is an inference |
| Tier 5: Complete staff census | All faculty or staff can be counted and reconciled to the public index | Not established |
| Tier 6: SLCM account enumeration | Student/parent/staff accounts or records can be identified through the public portal | Not established and not tested |
| Tier 7: Technology exploitability | The named framework, server, CDN, or identity stack contains a vulnerability | Not established; outside passive evidence |

The answer to "how much of the staff directory is publicly enumerable?" is therefore qualitative. **A meaningful and multi-layered portion of teaching-faculty and institutional-contact information is publicly navigable, but the percentage of all MUJ staff that this represents is unknown.** The evidence supports enumeration of categories and selected records, not a complete census. The distinction is especially important because the public entry point is titled "Teaching Faculties" [14], while the self-disclosure label uses the broader phrase faculty/staff details [16]. Those labels may describe overlapping populations, but the reviewed sources do not define the overlap.

## Synthesis

Across mechanism, scope, trade-offs, evidence base, and time horizon, the public MUJ ecosystem has three different surfaces. The first is the academic directory: it is intentionally navigable, rich in professional fields, and optimized for discoverability. The second is the office-contact layer: it publishes operational mailboxes and extension metadata for service delivery. The third is SLCM: it presents a login boundary and public support documentation, but the reviewed evidence does not expose authenticated data or prove an application defect.

The mechanism differs across the three. Faculty exposure comes from ordinary website information architecture and profile pages [14][11]. Contact exposure comes from a deliberately published table [4]. SLCM exposure comes from a public landing page plus a support PDF [1][15]. This divergence matters: a security club should not treat public staff profiles as evidence that SLCM itself is enumerable.

The principal tension is between transparency and minimization. MUJ's self-disclosure framework directs users to faculty/staff details with photographs [16], while individual pages can combine role, direct contact, educational history, expertise, and external research identities [11]. Transparency helps students and researchers, but the same aggregation may increase targeting opportunities - an inference, not an incident finding. The best decision is not to label the directory unsafe solely because it is public; it is to assess whether every field is necessary, current, and appropriate for public distribution.

A second tension is between institutional counts and directory evidence. The home page states 700 faculty members [2], and CSE states around 120 [18], yet the public index does not state a total [6]. Approximate promotional counts and navigable records serve different purposes. They cannot be combined into a coverage percentage without a dated roster, inclusion criteria, and a verified count of unique public profiles.

A third tension is between technology context and technical certainty. MUJ publicly describes Microsoft services, ERP, LMS, cloud, networks, servers, backups, telecommunications, and IT security [8], and the FAQ relates SLCM to Outlook and AMS support [15]. Those facts support asset ownership and responsible-contact planning. They do not justify a claim about ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, or an exploitable identity configuration. A mature report stops at the evidence boundary.

## VERDICT

**Overall verdict: MUJ's faculty and institutional-contact information is materially publicly enumerable through ordinary website navigation, but the completeness of the staff directory is not established.**

**Confidence: High** for the existence of public directory routes, public department navigation, publication of professional faculty fields, the 14-row contact table, the public SLCM landing page, and the IT/identity descriptions cited above [4][11][14][16].

**Confidence: Medium** for the interpretation that the visible directory is a substantial subset of MUJ teaching personnel. The CSE page's around-120 statement and the home page's 700-faculty statement are official but approximate and not reconciled to public profile records [18][2].

**Confidence: Low or unverified** for any claim that the complete university staff directory is publicly enumerable, that every profile contains a photograph, that the listed ASP.NET MVC/.NET/IIS/Akamai stack is independently confirmed, or that the SLCM portal has an authentication, authorization, or identity vulnerability. No such claim is supported by the passive evidence reviewed.

**Decision for the university security club:** classify the MUJ website directory as a **public information and privacy-minimization review target**, not as proof of an SLCM vulnerability. Continue only with passive documentation, redacted examples, and coordinated contact through published MUJ role channels. Do not attempt authentication, account discovery, parameter enumeration, or post-login testing without explicit written authorization.

## References

1. *Manipal University*. http://mujslcm.jaipur.manipal.edu/
2. *Manipal University Jaipur - 71 years of legacy of Manipal Education*. https://jaipur.manipal.edu/
3. *Faculty of Management , Commerce and Arts (FoMCA) At Manipal University Jaipur, MUJ*. http://jaipur.manipal.edu/fomca
4. *Contact Us - Manipal University Jaipur *. https://jaipur.manipal.edu/contact-university.php
5. *Department of Civil Engineering| Faculty of Science, Technology and Architecture (FoSTA) at MUJ*. http://jaipur.manipal.edu/fosta/department-of-civil-engineering.php
6. *MUJ Teaching Faculty Members  - Manipal University Jaipur *. https://jaipur.manipal.edu/muj-faculties.php
7. *Faculty of Science, Technology and Architecture (FoSTA) At Manipal University in Jaipur*. https://jaipur.manipal.edu/fosta/
8. *Head- Digital Infrastructure & Technology Services - Manipal University Jaipur*. http://jaipur.manipal.edu/administration-it.php
9. *Teaching Faculties*. http://jaipur.manipal.edu/fosta/faculty-details.php?url=151/
10. *Teaching Faculties*. http://jaipur.manipal.edu/fosta/faculty-details.php?url=203/
11. *Teaching Faculties*. http://jaipur.manipal.edu/fosta/faculty-details.php?url=149/
12. *Teaching Faculties*. http://jaipur.manipal.edu/fosta/faculty-details.php?url=186/
13. [Department of Media, Communication and Fine Arts | Faculty of Management , Commerce and Arts (FoMCA) at Manipal
    University Jaipur](http://jaipur.manipal.edu/fomca/department-of-media-communication-and-fine-arts.php)
14. *Teaching Faculties*. https://jaipur.manipal.edu/fosta/faculty-details.php
15. *Frequently Asked Questions and Contacts for SLCM Registration*. http://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf
16. *Public Self Disclosure*. https://jaipur.manipal.edu/img/pdf/Public%20Self%20Disclosure-U1.pdf
17. *Teaching Faculties*. http://jaipur.manipal.edu/fosta/faculty-details.php?url=157/
18. *Department of Computer Science & Engineering| Faculty of Science, Technology and Architecture (FoSTA) at MUJ*. http://jaipur.manipal.edu/fosta/department-of-Computer-Science-Engineering.php
