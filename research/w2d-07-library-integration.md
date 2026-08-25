# MUJ Library and SLCM Public Exposure Report

## Executive Summary

- **Official Library Stack**: The official Manipal University Jaipur library page identifies Koha LMS as the system holding bibliographic records, describes a Web OPAC, names DSpace for the institutional repository, and names Knimbus for off-campus access to subscribed content. [3] [3] -> Treat these as the authoritative baseline and publish one canonical inventory of library services.

- **Public OPAC**: The official page links a Single Window Search Box at `http://manipal-koha.informindia.co.in/`, and the destination identifies itself as the Manipal University Jaipur Library OPAC. [3] [12] -> The URL is a supported public catalog entry point, but the direct page does not explicitly name its software brand, so the Koha mapping should be described as supported by the official page rather than as a direct software fingerprint.

- **Student Identity**: MUJ documentation says that a University Identity Card enables borrowing and other library services, that members swipe a University Smart ID Card at the entrance, and that borrowing, renewal, reservation, and return require a valid RFID-enabled MUJ ID card. [3] [3] -> Protect the ID number and card-linked circulation records as sensitive account data, even though no legal classification is inferred here.

- **Checkout and Fines**: The official circulation table gives PG and UG students five books for 14 days, with a fine of Rs. 2 per day for the first week after the due date and Rs. 5 per day thereafter. [3] The rules also say that overdue items can block further issue until the items are returned and fines are paid. [2] -> Review authorization around loan, fine, renewal, and clearance functions; the public research did not establish an online fine-payment endpoint.

- **Digital Access Split**: A public RemotLog page describes MUJ Libraries, separates offline students using RemotLog from online students using E-Library, and uses a MUJ email address as the username. [5] It also describes off-campus access to subscribed content through RemotLog. [6] -> Do not assume that a MUJ email login is the same as SLCM single sign-on.

- **SLCM Link Not Proven**: The public MUJ SLCM landing page exposes MUJ Portal branding and student/parent sign-in, but the extracted public page contains no visible library hyperlink, library module, shared token, or explicit library integration. [10] -> Treat a direct SLCM-to-library integration as unverified until MUJ publishes or confirms an interface, data flow, or SSO relationship.

- **Repository Exposure**: A publicly indexed, IP-based DSpace/JSPUI page identifies itself as a MUJ repository and exposes previous-year-question-paper metadata. [8] Its page title also contains a credential-like access instruction; the value is intentionally redacted here. [8] -> Treat the value as an exposed secret: revoke or rotate it, remove it from public titles and metadata, and do not attempt to use or validate it.

- **Third-Party Portal Risk**: `https://www.mujlibrary.live/` claims to be a MUJ DigiLibrary, offers email OTP access using MUJ email domains, and claims book tracking, renewals, and catalog access. [4] No official MUJ linkage, privacy notice, SLCM relationship, or API documentation was established. -> Users should not submit university email addresses until MUJ confirms ownership and data handling.

- **API Finding**: Passive review of the official library page, linked OPAC, repository page, RemotLog pages, SLCM landing pages, and the unverified DigiLibrary landing page found no documented MUJ-specific library API or anonymous endpoint that exposes individual student-related records. This is bounded negative evidence, not proof that no private or undiscovered endpoint exists. -> Further testing should occur only under written authorization and preferably in a staging environment.

- **Overall Verdict**: Confidence is high for the official library software, card requirements, loan rules, fine schedule, and linked OPAC; medium for the relationship between MUJ and RemotLog; and low for any direct SLCM/library backend integration or the official status of `mujlibrary.live` and the IP-based repository.

## Scope, Evidence Model, and Auditable Reasoning Summary

This report addresses the library side of the MUJ SLCM ecosystem using public pages, public documents, and public landing-page content observed during the research snapshot. It does not use credentials, submit login forms, enumerate student identifiers, test hidden paths, invoke undocumented APIs, or attempt access to protected resources. It also does not reproduce any credential-like value visible in a public repository title.

The request supplied an application-stack description for `mujslcm.jaipur.manipal.edu`, including ASP.NET MVC, .NET Framework, IIS, Akamai, and Microsoft 365 identity. Those details are treated as scope context supplied by the requester, not as independently verified findings in this report. The public SLCM evidence used here establishes only the visible MUJ Portal and sign-in roles. [10]

I cannot provide private chain-of-thought. The following is a concise, reproducible reasoning record instead: first, rank first-party MUJ pages and MUJ-hosted documents above search-result claims; second, separate the catalog, repository, remote-resource gateway, and SLCM as different public services; third, compare their identity artifacts without assuming that similar MUJ email or card identifiers imply shared authentication; fourth, inspect only anonymous landing states for exposure; and fifth, mark absence claims as bounded conclusions rather than proof of nonexistence.

| Evidence class | Exact source | What it supports | Confidence treatment |
|---|---|---|---|
| First-party MUJ library page | `https://jaipur.manipal.edu/central-library.php` | Koha LMS, Web OPAC, DSpace, Knimbus, student ID and RFID functions, circulation categories, and official library contact details. [3] [3] [3] [3] | High for the statements printed on the page. |
| MUJ library rules document | `https://www.manipal.edu/content/dam/manipal/muj/documents/Library%20Rules-%20Ver1%20for%20Website.pdf` | Membership, entry restrictions, bar-coded ID use, overdue charges, renewal conditions, and blocking of further issues. [2] [2] [2] [2] | High for the rules as published; operational currency should be confirmed by MUJ. |
| Publicly linked MUJ OPAC | `http://manipal-koha.informindia.co.in/` | The destination identifies itself as Manipal University Jaipur Library and OPAC, with login and password prompts. [12] | High that the public URL and page labeling exist; medium for current operational status and software fingerprint. |
| Public RemotLog page | `https://muj.remotlog.com/` and `https://jaipur-manipal-edu.muj.remotlog.com/login` | Self-described MUJ library remote-resource access, offline/online routing, MUJ email username, and resource descriptions. [5] [6] | Medium because the pages self-identify as MUJ Libraries but are vendor-style subdomains. |
| Public SLCM landing page | `https://mujslcm.jaipur.manipal.edu/` | MUJ Portal branding and visible sign-in roles. [10] | High for the visible landing state; insufficient to prove or disprove backend integration. |
| IP-based repository | `http://20.219.59.68:8080/jspui/handle/123456789/1` | MUJ Repository JSPUI/DSpace labeling, public community metadata, and credential-like title exposure. [8] | Medium for what the page displays; low-to-medium for current ownership and authorization. |
| Unverified DigiLibrary | `https://www.mujlibrary.live/` | MUJ branding claims, OTP form, catalog and renewal claims, and a claimed book count. [4] | Low for official ownership because no authoritative MUJ link was found. |
| Other Manipal catalog | `https://maheblropac.koha.manipal.edu/` | A separate MAHE Bengaluru Koha catalog with public bibliographic and account UI. [9] [9] | High that it is MAHE BLR; it must not be treated as a MUJ endpoint. |

The key analytical distinction is between a public *description* of a system and evidence of a public *data interface*. A page can mention student access or show a login form without exposing student records. Conversely, a public title or metadata field can expose a secret without exposing student records. That distinction drives the API and exposure assessment below.

## exact_tables: Canonical Public URL and Function Inventory

The following table lists URLs discovered in official MUJ material or in public pages that identify themselves as MUJ-related. "Official" is reserved for the MUJ university domain or a MUJ-hosted document. A vendor-style or IP-based URL is labeled separately even when its page uses MUJ branding.

| System or page | Exact URL | Publicly observed function | Authority and status |
|---|---|---|---|
| MUJ Central Library | `https://jaipur.manipal.edu/central-library.php` | Official library information, software names, circulation rules, resource links, and contact information. [3] [3] | Official MUJ page. |
| FOA Library page | `https://jaipur.manipal.edu/foa-library.php` | A MUJ faculty or school library page carrying library information and membership references. [1] [1] | Official MUJ page. |
| Library Rules PDF | `https://www.manipal.edu/content/dam/manipal/muj/documents/Library%20Rules-%20Ver1%20for%20Website.pdf` | Rules for membership, entry, card use, borrowing, fines, renewal, and overdue controls. [2] [2] [2] | MUJ-hosted document; operational date should be confirmed. |
| MUJ single-window catalog | `http://manipal-koha.informindia.co.in/` | Public destination linked as the Single Window Search Box for Library Resources. [3] The page labels itself Manipal University Jaipur Library and OPAC. [12] | Publicly linked MUJ catalog; HTTP URL and current status merit owner confirmation. |
| MUJ institutional repository link | `http://20.219.59.68:8080/jspui/` | The official library page lists this as the MUJ Institutional Repository. [3] | IP-based public link; ownership and current management not independently confirmed. |
| Repository collection handle | `http://20.219.59.68:8080/jspui/handle/123456789/1` | Public DSpace/JSPUI page for previous-year question papers and faculty communities. [8] | Public page; credential-like title exposure should be treated as an incident. |
| RemotLog landing page | `https://muj.remotlog.com/` | Remote access to subscribed resources, with MUJ Libraries branding and offline/online routing. [6] | Self-described MUJ library service; vendor ownership and SLCM linkage not established. |
| RemotLog login page | `https://jaipur-manipal-edu.muj.remotlog.com/login` | Login to resources; username described as the user's MUJ email address. [5] | Public login page; no login attempt was made. |
| MUJ SLCM primary landing page | `https://mujslcm.jaipur.manipal.edu/` | MUJ Portal branding and student/parent sign-in. [10] | Public MUJ SLCM landing state. |
| MUJ SLCM alternate hostname | `https://muj.slcm.jaipur.manipal.edu/` | Public page with MUJ Portal branding in the extracted view. [11] | Alternate public hostname; no library function was visible. |
| Claimed MUJ DigiLibrary | `https://www.mujlibrary.live/` | Claims catalog access, book tracking, renewals, digital access, and email OTP. [4] | Unverified ownership; not treated as official. |
| MAHE Bengaluru Koha catalog | `https://maheblropac.koha.manipal.edu/` | Public Koha catalog with title, author, subject, ISBN, ISSN, series, and call-number search fields. [9] | MAHE BLR, not MUJ. |

The direct OPAC finding corrects an important ambiguity. The official MUJ library page does publish a public catalog destination, but the page calls it a Single Window Search Box rather than documenting a complete API. The destination calls itself an OPAC, yet its extracted landing state shows login and password prompts and no catalog results or individual student records. [12]

## 1. Official MUJ Library Footprint and Software Roles

The official MUJ Central Library page presents a multi-system library environment rather than a single application. It says that bibliographic holdings are entered in Koha LMS and that the OPAC is updated and made available as a Web OPAC through the university intranet and Internet. [3] This is the strongest public evidence for the catalog brand and search function.

The same page names DSpace as the software used for the institutional repository and Knimbus as the software used for off-campus access to subscribed content. [3] It also lists Turnitin as a plagiarism-checking system. [3] These names describe roles, not necessarily a unified identity architecture. In particular, the official page's Knimbus reference and the separate RemotLog page's RemotLog reference should not be silently collapsed into one product or one authentication service.

| Named component | Publicly stated role | Student-related boundary | Security interpretation |
|---|---|---|---|
| Koha LMS | Holds bibliographic data and supports the Web OPAC. [3] | The public catalog is bibliographic; the reviewed page did not display student records. [12] | Separate anonymous discovery from authenticated borrower-account functions. |
| Web OPAC | Allows users to search library resources through the campus-wide network and Internet. [3] | Public availability does not establish public circulation history. | Verify that account-only fields are authorization-protected. |
| DSpace | Used for the institutional repository. [3] | Repository metadata and academic documents are distinct from borrower records. [8] | Review metadata and document access for accidental credentials or personal data. |
| Knimbus | Provides off-campus access to subscribed contents. [3] | The page does not state that Knimbus is SLCM or that it shares SLCM tokens. | Confirm the actual identity provider and redirect boundaries with the owner. |
| Turnitin | Named as a plagiarism-checking web system. [3] | No student record was observed in the public library page. | Keep submission and academic-integrity data outside public catalog responses. |

The official page also lists external research resources such as DELNET, INFLIBNET's e-ShodhSindhu, Shodhganga, Current Science, British Council Library, and the American Spaces collection. [3] These are useful discovery or research destinations, but their listing on the MUJ page does not make them MUJ-operated systems.

The operational lesson is architectural: MUJ's public material identifies distinct applications for bibliographic discovery, repository content, remote resource access, and plagiarism checking. The SLCM page, by contrast, publicly shows only a portal sign-in state. [10] Therefore, a security review should start from separate trust zones and prove any connection rather than assuming that the common MUJ name means a common backend.

## 2. OPAC Brands, Public Search, and a Near-Miss Catalog

The public MUJ catalog path is unusually useful for attribution because two different sources align. The official library page links `http://manipal-koha.informindia.co.in/` with the label "Single Window Search Box for Library Resources." [3] When read directly, the destination identifies itself as "MANIPAL UNIVERSITY JAIPUR LIBRARY" and "OPAC (Online Public Access Catalogue)." [12]

The direct page's anonymous state exposes a login/password interface. It says that users without a password should visit the circulation desk to have one set up, and it separately references library-card registration. [12] [12] That is evidence of an authenticated borrower-account capability, not evidence that borrower records are anonymously accessible. No student name, registration number, checkout history, fine balance, or other individual student record appeared in the reviewed public content. [12]

The software attribution should be stated carefully. The official MUJ page explicitly names Koha LMS for holdings and Web OPAC operations. [3] The linked catalog page itself does not explicitly print the Koha brand in the extracted text. The defensible wording is therefore "MUJ's official page identifies Koha LMS and links the MUJ OPAC at the following URL," not "the direct page independently fingerprints Koha."

| Candidate catalog | Institution shown | Public features observed | MUJ conclusion |
|---|---|---|---|
| `http://manipal-koha.informindia.co.in/` | Manipal University Jaipur Library. [12] | OPAC label, login/password fields, circulation-desk password instruction, and library-card instruction. [12] | Strong MUJ catalog candidate because the official MUJ page links it. |
| `https://maheblropac.koha.manipal.edu/` | MAHE BLR Central Library and MAHE Bengaluru libraries. [9] [9] | Search by title, author, subject, ISBN, ISSN, series, and call number; account UI includes login, lists, cart, and search history. [9] | Not a MUJ endpoint. It is a useful false-positive control. |
| `https://www.mujlibrary.live/` | Page claims Manipal University Jaipur and MUJ DigiLibrary. [4] | Claims catalog, renewals, book tracking, and email OTP. [4] | Unverified; no official MUJ link was established. |

The MAHE BLR page is a particularly important case study because the shared Manipal name and Koha branding could cause an analyst to misattribute it to MUJ. The page names MAHE BLR, says that the catalog covers eight MAHE BLR libraries, and lists Bengaluru library locations. [9] [9] It is a genuine public Koha-style catalog page, but it does not mention MUJ. [9]

This contrast demonstrates why hostname similarity is not enough. A security club should record the institution named inside the application, the official page that links it, and the functions visible in the anonymous state. Those three checks distinguish the MUJ OPAC candidate from the unrelated MAHE BLR catalog without attempting account access.

## 3. Student ID, Email Identity, and the SLCM Relationship

The official MUJ library page establishes a physical and transactional identity model. It says that a University Identity Card enables students, faculty members, and research scholars to use library services, including borrowing. [3] It further says that members swipe a University Smart ID Card at the entrance. [3] Borrowing, renewal, reservation, and return are stated to require a valid RFID-enabled MUJ ID card. [3]

The MUJ rules PDF supplies a second formulation. Entry is restricted to MUJ ID or Library Membership Card holders. [2] The document also says that bar-coded MUJ ID cards must be submitted during checkout and check-in transactions. [2] These are consistent signs that the physical card is a library control point, but they do not show that the card identifier is accepted by SLCM or that the library calls an SLCM API.

| Identity artifact | Publicly documented use | Direct SLCM relationship shown? | Assessment |
|---|---|---|---|
| University Identity Card | Enables student, faculty, and research-scholar library use, including borrowing. [3] | No. | Confirmed library identity artifact; SLCM linkage unproven. |
| University Smart ID Card | Swiped at the library entrance. [3] | No. | Confirmed entrance-control artifact; backend destination unknown. |
| RFID-enabled MUJ ID card | Required for borrowing, renewal, reservation, and return. [3] | No. | Confirmed circulation artifact; do not infer SSO. |
| Bar-coded MUJ ID card | Presented during checkout and check-in. [2] | No. | Confirmed desk workflow; no API or data schema shown. |
| MUJ email address | Used as the username described on the RemotLog login page. [5] | No. | Remote-resource login identifier; not proof of SLCM identity federation. |
| SLCM student or parent sign-in | Visible on the MUJ Portal landing page. [10] | No library link visible. | Separate public portal surface in the evidence reviewed. |
| OPAC password | Public OPAC page provides login/password fields and a circulation-desk setup instruction. [12] | No. | Catalog-account authentication surface; provider not documented on the page. |

The RemotLog page adds a separate digital identity clue. It labels the service MUJ LIBRARIES, instructs offline students to select RemotLog and online students to select E-Library, and identifies the MUJ email as the username. [5] The root page says that off-campus access to subscribed contents is provided through username and password using RemotLog. [6]

The SLCM landing page does not expose a library link or a library function in the extracted public state. [10] This is a limited observation, not proof that no authenticated SLCM module exists. It does mean that public evidence cannot currently support claims of shared SSO, account synchronization, or a student-ID-to-Koha token exchange.

The correct inference is therefore narrow: MUJ library and SLCM appear to coexist within the same institutional environment and use institutional identity artifacts, but the reviewed public evidence does not establish a direct system-to-system link. Similar names, MUJ email domains, and physical card identifiers are identifiers; they are not, by themselves, evidence of a shared authentication protocol.

## 4. Checkout, Overdue, Fine, and Renewal Flows

The official MUJ page provides a role-based circulation table. Faculty members may borrow eight books for one semester with no overdue charge; non-teaching staff may borrow four books for one semester with no overdue charge; research scholars may borrow eight books for 90 days with no overdue charge. [3] PG and UG students may borrow five books for 14 days, with the published student fine schedule of Rs. 2 per day for one week and Rs. 5 per day after one week. [3]

The same page lists non-book material rules: faculty and students may borrow two items for two days, and the student overdue charge follows the same Rs. 2 and Rs. 5 progression. [3] The PDF says borrowing and returning occur at the circulation counter from 8:30 AM to 5:30 PM, with service unavailable on Sundays and holidays. [2]

| Borrower category | Material or loan allowance | Loan period | Overdue charge stated publicly |
|---|---|---|---|
| Faculty | Eight books. [3] | One semester. [3] | No overdue charge stated in the table. [3] |
| Non-teaching staff | Four books. [3] | One semester. [3] | No overdue charge stated in the table. [3] |
| Research scholars | Eight books. [3] | 90 days. [3] | No overdue charge stated in the table. [3] |
| PG and UG students | Five books. [3] | 14 days. [3] | Rs. 2 per day for one week, then Rs. 5 per day. [3] |
| Students borrowing non-book material | Two items. [3] | Two days. [3] | Rs. 2 per day for one week, then Rs. 5 per day. [3] |

The rules PDF adds important enforcement behavior. A book may be renewed only if it is not in demand or reserved by another user; overdue items cannot be renewed; a borrowed book cannot be renewed more than once; and the borrower must bring the material physically to the library for renewal. [2] If a book is not returned within the loan period, further issue may be stopped until the overdue items are returned and fines are paid. [2]

This creates a clear control flow: the card identifies the borrower at circulation, the item and due date produce an overdue state, the overdue state produces a fine, and the fine can block later borrowing. The rules also state that circulation transactions close 30 minutes before closing and can be suspended during a power or system failure. [2] No reviewed MUJ source documents an online fine-payment API, a SLCM fee module, or an automatic SLCM clearance callback. The safe conclusion is that the public material establishes dues and blocking rules, not a digital payment integration.

From an application-security perspective, the most important data boundary is not the public bibliographic search. It is the authenticated mapping among card identifier, borrower account, loan history, due date, fine, renewal status, and borrowing block. That mapping is an analytical risk classification, not a claim that MUJ has a vulnerability. Any review of those functions should be authorized and should test authorization decisions using synthetic accounts, not real student identifiers.

## 5. Digital Resources, RemotLog, and the Repository Case Study

The public RemotLog landing page describes the MUJ Libraries as an academic information service and reports nearly 75,000 books, about 2.30 lakh e-books, 350 print periodicals, 1,000 back volumes of journals, 325 Ph.D. theses, and about 3,000 CD/DVD-ROMs. [6] It also reports access to 32,960 e-journals and names providers including IEL Online, Springer Journals, EBSCO Business Source Elite, JGate, JSTOR, Manupatra, Lexis India, Supreme Court Cases, Corporate Law Advisor, and CMIE Database. [6]

These figures are self-published service-description content, not independently reconciled inventory data. The unverified DigiLibrary page claims "25,000+ Books," which does not match the nearly 75,000 books claimed by RemotLog. [4] The discrepancy may reflect different collections, different dates, or different systems, but the public evidence does not establish which explanation is correct. It should be recorded as an unresolved inventory divergence rather than normalized into one number.

| Digital or repository surface | Public content | Student-related exposure observed | Priority interpretation |
|---|---|---|---|
| RemotLog landing page | MUJ Libraries description, remote access explanation, resource counts, and named e-resource providers. [6] | No individual student record visible in the reviewed page. | Medium: verify ownership, identity provider, and vendor data handling. |
| RemotLog login page | Username/password form; MUJ email identified as username; offline and online learner routing. [5] | No student record visible; login was not attempted. | Medium: protect email namespace and ensure authentication boundaries. |
| DSpace institutional repository as described by MUJ | DSpace named as the institutional-repository software. [3] | Official page does not show student borrower data. | Medium: review public repository metadata and document permissions. |
| IP-based MUJ repository page | MUJ Repository JSPUI, DSpace branding, previous-year-question-paper collection, and faculty communities. [8] | No individual student personal data identified in the reviewed content. [8] | High for secret exposure because the page title contains a credential-like instruction. [8] |
| Unverified DigiLibrary | MUJ branding, OTP email form, catalog, renewals, and a claimed 25,000+ books. [4] | No student record visible in the landing page. | High uncertainty: verify ownership before email submission. |

The repository is the clearest public-exposure case study. Its page calls itself "MUJ Repository JSPUI," uses DSpace branding, and presents a previous-year-question-paper community with faculty sub-communities. [8] That is ordinary public academic-content metadata. However, the page title also contains a credential-like access instruction. [8] The secret is not reproduced in this report because publication would increase risk.

The appropriate response is not to test the credential or attempt a download. The appropriate response is to preserve only the minimum evidence needed for a responsible report, redact the value, notify the owner through an official channel, revoke or rotate the value, remove it from the title and metadata, and review repository logs for unauthorized use. The official MUJ library page identifies the Chief Librarian and a MUJ email address, which provides a starting point for notification. [3]

The divergence between the official page's domain-linked service model and the IP-based repository is also analytically important. The official library page publishes a domain-based OPAC link and names its software stack, while the repository link uses an IP address and a non-TLS HTTP URL. [3] This is not proof of a security flaw, but it is a governance and lifecycle signal: asset ownership, TLS coverage, metadata review, and canonical-link management should be made explicit.

## 6. Public API and Student-Data Exposure Assessment

The public review found no documented MUJ-specific library API, API documentation page, or anonymous search endpoint that returned individual student-related records. The conclusion is bounded because only public landing pages and linked documents were reviewed. No hidden-path enumeration, API fuzzing, credential testing, or form submission was performed.

| Candidate surface | Publicly exposed content | Individual student data observed? | API conclusion |
|---|---|---|---|
| MUJ OPAC `http://manipal-koha.informindia.co.in/` | MUJ Library and OPAC labels, login/password fields, and circulation-desk password instructions. [12] | No. [12] | Public catalog/account surface; no documented API was identified in the reviewed page. |
| Official MUJ Web OPAC description | Koha LMS holdings, Web OPAC availability, campus-wide search, and digital/print resource descriptions. [3] | No individual record in the page description. | Documentation of a search service, not API documentation. |
| MUJ DSpace/JSPUI repository | Public repository label, collections, faculty communities, and academic-content metadata. [8] | No individual student personal data identified in the reviewed content. [8] | Public repository page, not evidence of a student-data API; credential-like title exposure is a separate incident. [8] |
| RemotLog root and login | Public service description, MUJ email username convention, and resource-access explanation. [5] [6] | No individual record in the anonymous state. | No public MUJ library API documentation identified. |
| `https://www.mujlibrary.live/` | MUJ DigiLibrary claims, OTP form, catalog, tracking, and renewal language. [4] | No individual record in the landing page. | No API documentation or ownership confirmation identified. |
| MUJ SLCM landing page | MUJ Portal branding and student/parent sign-in. [10] | No library or student record in the public landing state. | No public library integration endpoint identified. |
| MAHE BLR Koha page | Catalog search fields, account UI, OpenAthens audience statement, and MAHE BLR identity. [9] | No individual student record in the reviewed page. | A separate Manipal catalog; not evidence about MUJ. |

The phrase "exposing student-related data" should be separated into three levels. First, the pages expose *service metadata*: that students use MUJ IDs, MUJ email addresses, OPAC accounts, and SLCM sign-in. [3] [5] [10] Second, they expose *institutional content metadata*, such as collections, question-paper communities, and e-resource descriptions. [8] [6] Third, they would expose *individual records* if they showed a person's name, ID, loan history, fines, reservation, grades, or authentication tokens. No individual record was observed in the public material reviewed for this report.

The most material public finding is therefore not a student-record API. It is the repository's credential-like title exposure. A second concern is identity ambiguity: the same MUJ email namespace appears in a RemotLog login description and in the unverified DigiLibrary OTP form, but there is no public evidence that the two services share an identity provider or that either one is SLCM. [5] [4]

The security-club conclusion should remain conservative: no public student-data endpoint was identified, but the absence of an observed endpoint is not evidence that authenticated APIs are correctly authorized. The correct next step for the owner is an authorized review of account endpoints, authorization checks, object-level access controls, token audience restrictions, and logging, using synthetic accounts and written scope.

## 7. Four Case Studies and the Main Contradictions

### Case Study A: Official OPAC Attribution Versus Software Fingerprinting

The official MUJ library page provides the strongest attribution chain: it names Koha LMS, describes a Web OPAC, and links the Single Window Search Box. [3] [3] The linked page independently labels itself as the MUJ Library OPAC. [12] The outcome is a high-confidence public catalog candidate.

The limitation is equally important. The linked page does not explicitly print the Koha brand in the extracted content. [12] The correct security-report language is therefore that the official MUJ page identifies Koha and links the OPAC, not that the direct page alone proves its implementation. This case reveals why attribution and fingerprinting should be reported separately.

### Case Study B: MAHE BLR as a False Positive

The MAHE BLR page is visibly a Koha catalog and includes account features such as login, lists, cart, and search history. [9] It also identifies MAHE BLR and Bengaluru libraries rather than MUJ. [9] [9] If an analyst searches for "Manipal Koha" without checking the named campus, this page could be incorrectly placed in a MUJ attack-surface inventory.

The outcome is a useful negative control. Shared group branding and shared product choice do not establish shared data, shared infrastructure, or shared identity. A hostname, page title, and official parent-page link must be checked together.

### Case Study C: Public Academic Repository With a Secret-Like Title

The IP-based repository exposes ordinary DSpace/JSPUI collection metadata and faculty communities. [8] The page title also contains a credential-like instruction. [8] This is a public exposure even though the page does not show student borrower records.

The outcome is a priority remediation item: revoke or rotate the exposed value, remove it from public metadata, and review access logs. This case shows that a library assessment must cover repository metadata hygiene, not only student-record endpoints.

### Case Study D: Unverified DigiLibrary and Email Namespace Risk

The DigiLibrary landing page uses MUJ branding, claims catalog and renewal functions, and asks for a MUJ-domain email address followed by an OTP action. [4] No official MUJ page linkage, legal ownership statement, privacy terms, SLCM relationship, or API documentation was established in the reviewed material.

The outcome is an attribution and data-minimization risk, not a finding that the site is malicious. Users should wait for MUJ confirmation before submitting an email address. MUJ should publish canonical links and an ownership notice if the service is legitimate, or warn users if it is not.

## 8. Safe Recommendations for MUJ and the Security Club

The recommendations below are defensive and assume written authorization for any deeper assessment. They do not instruct readers to log in, use exposed credentials, enumerate IDs, or probe undocumented endpoints.

| Priority | Defensive action | Evidence or reason | Safe implementation boundary |
|---|---|---|---|
| P0 | Revoke or rotate the credential-like value displayed in the repository title and remove it from all public titles, metadata, search indexes, and documents. | The public repository title contains a credential-like access instruction. [8] | Do not reproduce or test the value; use a redacted screenshot or URL-only incident report. |
| P0 | Confirm ownership and canonical links for the IP-based repository, OPAC, RemotLog, and DigiLibrary. | MUJ has a domain-based official page, an IP-based repository link, vendor-style RemotLog hosts, and an unverified DigiLibrary domain. [3] [5] [4] | Perform confirmation through MUJ library or IT channels, not through unapproved login attempts. |
| P1 | Publish one official library-systems page with canonical URLs, named operators, privacy contacts, and a statement of which systems are or are not connected to SLCM. | The public evidence names several services but does not establish the SLCM relationship. [3] [10] [6] | Treat the official MUJ domain as the source of truth for links. |
| P1 | Document the identity flow for RFID/bar-coded card, OPAC account, RemotLog, and SLCM separately. | MUJ documents multiple identity artifacts and login surfaces. [2] [2] [3] [5] [10] | Use architecture diagrams and synthetic accounts; do not collect real student data. |
| P1 | Review authorization around loans, renewals, fines, reservations, and borrowing blocks. | The rules explicitly tie overdue items and paid fines to further issue eligibility. [2] | Test only in an authorized staging environment with synthetic borrowers and books. |
| P1 | Ensure anonymous catalog and repository responses contain bibliographic or academic-content metadata only, not borrower names, IDs, fines, tokens, or circulation history. | The reviewed public pages did not show individual student records, but the desired boundary should be explicit. [12] [8] | Use response-schema review and access-control tests under written scope. |
| P2 | Reconcile public collection counts and dates. | RemotLog reports nearly 75,000 books while the unverified DigiLibrary claims 25,000+ books. [6] [4] | Label each figure by system, collection scope, and publication date rather than merging totals. |
| P2 | Review transport security and lifecycle status for HTTP links. | The official links to the OPAC and IP repository are published with HTTP URLs. [3] | Confirm redirects, certificates, and legacy decommissioning with the owner; do not infer a vulnerability from the URL alone. |
| P2 | Establish a responsible-disclosure route. | The official library page identifies the Chief Librarian and a MUJ email contact. [3] | Send only redacted evidence and do not include any exposed secret in ordinary email. |

For the university security club, a safe project deliverable would be a passive asset register, an evidence table, and a data-flow diagram. It should not include credential replay, endpoint brute force, account enumeration, or attempts to retrieve private circulation data. The repository title issue should be handled as a responsible disclosure rather than as an opportunity to validate access.

## 9. What Is Answered and What Remains Unanswered

| Question | Answer supported by public evidence | Remaining uncertainty |
|---|---|---|
| What is the MUJ library portal? | The official library information page is `https://jaipur.manipal.edu/central-library.php`; a linked public OPAC is `http://manipal-koha.informindia.co.in/`. [3] [3] [12] | The current operational status, TLS behavior, and ownership details of the external OPAC host should be confirmed by MUJ. |
| What OPAC brand is involved? | The official page names Koha LMS and Web OPAC. [3] | The direct OPAC page does not explicitly print the software brand in the reviewed anonymous content. [12] |
| How is student identity used? | University, Smart, RFID-enabled, and bar-coded MUJ ID cards are used for library access and circulation. [3] [3] [2] [2] | The public material does not show whether the card record is synchronized with SLCM. |
| What are student loan and fine rules? | Five books for 14 days; Rs. 2 per day for the first week overdue and Rs. 5 per day after one week. [3] | The public material does not document an online payment API or a payment-provider integration. |
| Is RemotLog linked to SLCM? | RemotLog publicly describes MUJ library remote-resource access and MUJ email login. [5] [6] | No public SLCM link, shared token, or SSO assertion was found. |
| Is the repository official? | The official library page lists an IP-based MUJ Institutional Repository link, and the destination identifies itself as a MUJ DSpace/JSPUI repository. [3] [8] | Current ownership, maintenance, and authorization of the IP host are not independently confirmed. |
| Is `mujlibrary.live` official? | It claims MUJ DigiLibrary, OTP access, catalog, and renewals. [4] | Official ownership, privacy handling, and SLCM relationship are unverified. |
| Is there a public API exposing student records? | None was identified in the passive public review. | This is not proof of absence and says nothing about protected APIs or authorization quality. |

The most important unanswered question is the actual integration boundary. Public material supports several independent identity and library surfaces, but it does not disclose whether SLCM provisions library users, whether Koha consumes a student master record, whether RemotLog delegates to Microsoft 365, or whether any service exchanges signed tokens with another. Those questions require owner confirmation or an authorized architecture review.

## 10. Synthesis: One Institution, Several Trust Boundaries

The systems can be compared along mechanism, scope, evidence quality, and data sensitivity. The comparison shows why a single "MUJ SLCM ecosystem" label should not be interpreted as a single application.

| Entity or strategy | Primary mechanism | Scope | Public evidence strength | Main trade-off |
|---|---|---|---|---|
| MUJ SLCM | Portal sign-in with student and parent roles visible on the public page. [10] | Student lifecycle portal surface. | High for visible branding; low for library integration. | Central-looking identity surface, but public library linkage is not shown. |
| MUJ Koha/Web OPAC | Bibliographic holdings and public catalog search. [3] | Library discovery and borrower-account entry point. | High because the official page links the catalog and names Koha. [3] | Public discovery is useful, while borrower functions require account controls. |
| MUJ card/RFID workflow | Smart, RFID, and bar-coded card use at entry and circulation. [3] [2] | Physical access and checkout, return, renewal, and reservation. | High from two MUJ sources. | Strong physical control, but it does not prove digital SSO. |
| RemotLog | Username/password remote access using MUJ email convention. [5] [6] | Off-campus subscribed resources. | Medium because the service self-describes as MUJ Libraries. | Convenient remote access, but operator and identity federation need confirmation. |
| DSpace/JSPUI repository | Public academic-content repository and collections. [8] | Question papers and institutional digital content. | Medium for displayed content; lower for current ownership. | Open scholarship/content access can coexist with serious metadata-secret exposure. |
| Unverified DigiLibrary | Email OTP claim plus book tracking, renewals, and catalog language. [4] | Claimed student library account service. | Low for official ownership. | Convenience claim versus unresolved provenance and data-handling risk. |
| MAHE BLR Koha | Public Koha catalog and account UI for Bengaluru libraries. [9] | MAHE BLR, not MUJ. | High for its own identity. | Valuable comparison, but dangerous as a hostname or brand false positive. |

Three tensions emerge. First, MUJ uses both physical identifiers and digital identifiers. The card controls entrance and circulation, while RemotLog uses a MUJ email username and SLCM shows a portal sign-in. [3] [5] [10] This may be operationally convenient, but the evidence does not show whether those identifiers converge in one identity provider.

Second, the public architecture mixes open discovery with gated account functions. The official page intentionally describes a Web OPAC that can be searched through the Internet, while the OPAC landing state presents password-based account functions. [3] [12] This is a sound conceptual boundary if enforced correctly: bibliographic discovery can be public, while circulation history and fines remain private. The reviewed material does not prove how the boundary is implemented behind authentication.

Third, formal institutional linking and informal or legacy exposure diverge. The official page names software and publishes links, but the repository uses an IP-based HTTP address and exposes a credential-like title, while the unverified DigiLibrary uses a separate domain and makes student-email OTP claims. [3] [8] [4] The non-obvious risk is therefore governance fragmentation: a library can have no public student-data API in its visible pages and still have serious exposure through stale metadata, ambiguous domains, or leaked access instructions.

The combined implication is that the highest-value next step is not indiscriminate endpoint hunting. It is an authoritative service map that states which system owns which data, which identity artifact is accepted, which links are canonical, and whether SLCM is actually connected. That map would resolve more risk than treating every Manipal-branded page as one application.

## VERDICT

**Overall confidence: Moderate-to-high for the core library findings; moderate for service attribution outside the MUJ domain; low for claims of direct SLCM/library integration.**

The public evidence supports the following final assessment:

1. MUJ's official library documentation identifies Koha LMS and a Web OPAC, and the official page links the public MUJ catalog at `http://manipal-koha.informindia.co.in/`. [3] [3] The linked page identifies itself as the Manipal University Jaipur Library OPAC and exposes account-login prompts but no individual student records in the reviewed anonymous state. [12]
2. MUJ student library identity is explicitly tied to University, Smart, RFID-enabled, and bar-coded MUJ ID cards for entry and circulation. [3] [3] [2] [2]
3. Student circulation rules are explicit: five books for 14 days, followed by the published Rs. 2 and Rs. 5 overdue schedule, with overdue/fine status capable of stopping further issue. [3] [2]
4. DSpace and RemotLog are publicly associated with MUJ library content and remote access, but the reviewed pages do not prove that either is integrated with SLCM. [3] [5] [6] [10]
5. A public repository page contains a credential-like title exposure and should be remediated immediately without reproducing or testing the value. [8]
6. No public MUJ-specific API or anonymous search endpoint exposing individual student-related records was identified in the passive review. This conclusion is bounded and must not be expanded into a claim that protected APIs are secure or nonexistent.

The report's most defensible security-club conclusion is: **MUJ has a publicly documented library catalog and card-based circulation model alongside separate digital-resource and SLCM login surfaces, but a direct library-to-SLCM data or authentication link is not publicly established. The immediate actionable exposure is the repository's credential-like public metadata, not a demonstrated public student-record API.**

## References: Exact URLs

| Citation source | Exact URL |
|---|---|
| MUJ Central Library page | `https://jaipur.manipal.edu/central-library.php` |
| MUJ FOA Library page | `https://jaipur.manipal.edu/foa-library.php` |
| MUJ Central Library Rules and Regulations PDF | `https://www.manipal.edu/content/dam/manipal/muj/documents/Library%20Rules-%20Ver1%20for%20Website.pdf` |
| MUJ Single Window Search Box and OPAC | `http://manipal-koha.informindia.co.in/` |
| MUJ institutional repository link listed by the official library page | `http://20.219.59.68:8080/jspui/` |
| Public MUJ repository collection page | `http://20.219.59.68:8080/jspui/handle/123456789/1` |
| MUJ RemotLog landing page | `https://muj.remotlog.com/` |
| MUJ RemotLog login page | `https://jaipur-manipal-edu.muj.remotlog.com/login` |
| MUJ SLCM primary landing page | `https://mujslcm.jaipur.manipal.edu/` |
| MUJ SLCM alternate hostname | `https://muj.slcm.jaipur.manipal.edu/` |
| Claimed MUJ DigiLibrary | `https://www.mujlibrary.live/` |
| MAHE Bengaluru Koha catalog, not MUJ | `https://maheblropac.koha.manipal.edu/` |
| DELNET, listed as an external library resource | `https://delnet.in/` |
| e-ShodhSindhu, listed as an external resource | `https://ess.inflibnet.ac.in/` |
| Shodhganga, listed as an external repository resource | `https://shodhganga.inflibnet.ac.in/` |
| Current Science, listed as an external resource | `https://www.currentscience.ac.in/` |
| British Council Library, listed as an external resource | `https://www.britishcouncil.in/library` |
| American Spaces collection, listed as an external resource | `https://in.usembassy.gov/education-culture/american-spaces/american-space-new-delhi/collection/` |
| Turnitin, listed as an external tool | `http://turnitin.com/` |

## References

1. *FOA Library - Manipal University Jaipur *. https://jaipur.manipal.edu/foa-library.php
2. *Central Library Manipal University Jaipur Rules and Regulations*. https://www.manipal.edu/content/dam/manipal/muj/documents/Library%20Rules-%20Ver1%20for%20Website.pdf
3. *Library - Manipal University Jaipur *. https://jaipur.manipal.edu/central-library.php
4. *Library Portal | Student Portal*. https://www.mujlibrary.live/
5. *Login | Register | RemotLog | MUJ LIBRARIES (Offline Students - Select Remotlog; Username: Your MUJ Email ID  ) (Online Students - Select E-Library; Username: Your MUJ Email ID )*. https://jaipur-manipal-edu.muj.remotlog.com/login
6. *RemotLog | MUJ LIBRARIES (Offline Students - Select Remotlog; Username: Your MUJ Email ID  ) (Online Students - Select E-Library; Username: Your MUJ Email ID )*. https://muj.remotlog.com/
7. *Online Bachelor and Master Programmes | Online Degree Programs in India | Online Manipal*. https://muj.onlinemanipal.com/
8. *Manipal University Jaipur Repository: Previous Year Question Papers                                            (For downloading the papers kindly use: dspace@muj.manipal.edu | password: Mujlibrary@123 )*. http://20.219.59.68:8080/jspui/handle/123456789/1
9. *Koha online catalog*. https://maheblropac.koha.manipal.edu/
10. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
11. *Manipal University*. https://muj.slcm.jaipur.manipal.edu/
12. [

    Log in to your account
 ›
 Manipal University Jaipur catalog
](http://manipal-koha.informindia.co.in/)
