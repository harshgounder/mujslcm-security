# MUJ SLCM Public-Indexing and Dork Assessment

## Executive Summary

This report records the results of a passive, public-information review of the Manipal University Jaipur student lifecycle management ecosystem. The review was limited to search-engine discovery and reading publicly returned pages or documents. No authentication was attempted, no credentials were tested, no hidden route was enumerated, no vulnerability scan was run, and no personal student data is reproduced.

- **Official Portal Discovery**: Search results consistently return `https://mujslcm.jaipur.manipal.edu/` as a page titled "muj portal - Manipal University" and show the public labels "WELCOME TO MUJ PORTAL," "Sign In," "Sign In Parent Login," and "Sign In Student Login" [1]. -> Treat the root URL as an indexed login surface, not as evidence that student records are publicly accessible.
- **Indexed Route Discovery**: The URL `https://mujslcm.jaipur.manipal.edu/Home/Index` is also returned, but its visible public content is limited to a login-oriented page and "Forgot Password?" [3]. -> Record the path as an indexed public route, but do not infer that other MVC routes exist or attempt to enumerate them.
- **Official SLCM Documentation**: MUJ's publicly indexed SLCM FAQ gives the registration link `https://mujslcm.jaipur.manipal.edu/` [12]. -> The FAQ is the strongest official link between the university's public website and the SLCM host.
- **Fee-Related Artifacts**: The official payment page identifies the MUJ student portal URL as `https://mujslcm.jaipur.manipal.edu/` [20], while an official annual-fee notice is dated June 24, 2025 and states July 18, 2025 as the deadline for the 2025-26 annual course fee [18]. -> Fee dorks return useful public administrative information, but not observed student-specific receipts or payment records.
- **Academic-Record Dorks**: Searches for MUJ-hosted PDFs involving marks, marksheets, register numbers, student lists, and enrollment did not produce a confirmed first-party student-specific marksheet or register-number file in the observed result set. -> Report this as "no confirmed hit observed," not as proof that no such file exists.
- **Spreadsheet Dorks**: Searches for `XLSX` across MUJ and Manipal domains returned no confirmed MUJ-hosted XLSX workbook in the observed results. Several results were PDFs whose search titles contained `.xlsx`, while other hits were third-party pages or repositories. -> Validate file type by URL and content type before treating a result as an exposed workbook.
- **Technology Fingerprints**: The supplied descriptions of ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 identity were not independently established by the public indexed pages reviewed. -> Keep those details as unverified scope assumptions unless the owner confirms them or a permitted asset-inventory source documents them.
- **Privacy Risk**: A third-party Scribd result claims to contain student registration numbers, email addresses, genders, departments, names, and degrees [19]. -> This is not a first-party MUJ-domain artifact, was not used as evidence of MUJ exposure, and should not be downloaded, copied, or redistributed by the security club.
- **Operational Recommendation**: The university should review search-engine indexing, remove or restrict any student-specific documents, use `noindex` or authenticated delivery where appropriate, and provide a coordinated disclosure channel. -> The club should share only URLs, timestamps, query strings, and redacted screenshots with the university's authorized security contact.

## Scope, Ethics, and Evidence Model

The assessment question concerns a university portal that may contain educational, financial, and identity-linked information. Those categories create a heightened privacy and authorization boundary. A search-engine result is not permission to access an application, submit a login form, guess a password, test a reset workflow, or retrieve a document that appears to contain personal data. Accordingly, this report treats search result snippets and publicly readable pages as the evidence boundary.

The evidence model has three levels. First, an **observed indexed artifact** is a search result or publicly readable document with an exact URL and a snippet or extracted passage. Second, an **unconfirmed possibility** is a claim suggested by a title, a third-party page, or a requester-supplied technology description but not established by the reviewed public evidence. Third, an **inference** is an analyst interpretation, such as the likelihood that the host is used for student lifecycle services because the official FAQ and payment page point to it. Inferences are labeled as such rather than presented as facts.

The official MUJ website describes examination processes and assessment components, including class or tutorial participation, assignments, laboratory work, tests, quizzes, and end-semester examinations [10]. That public explanation establishes the sensitivity of the subject area, but it is not itself a student marksheet. Similarly, the public fee page lists course-related fee information [4], but a public course-fee page is not equivalent to an individual student's ledger, receipt, balance, or payment history.

The search results also contain unrelated or cross-scope Manipal systems. For example, `https://slcm.manipal.edu/` is identified as "MU SLcM" and includes a Manipal Academy of Higher Education footer [6], while `https://muj.slcm.jaipur.manipal.edu/` is an alternate MUJ-looking host with similar sign-in text [2]. These should not be merged into one asset without owner confirmation. The same naming convention appears across different Manipal institutions, so domain ownership and institutional scope matter.

This report does not provide a hidden chain of thought or private internal reasoning. Instead, it provides a reproducible high-level methodology: define the public-only boundary, run narrowly scoped search queries, compare returned URLs and snippets, read only public official documents, classify each hit, and avoid retrieving or reproducing sensitive records. That method is sufficient for an authorized club report without exposing private deliberation or giving instructions for unauthorized access.

## Requested Dork Matrix and Observed Results

The table below converts the requested discovery themes into passive search strings. These are intended for use in an ordinary search engine by an authorized researcher. They should be run without automated crawling, login attempts, parameter manipulation, or follow-up access to documents that appear to contain personal data.

| Discovery objective | Passive search string | Observed result | Useful indexed artifact | Exact URL or result | Assessment |
|---|---|---|---|---|---|
| MUJ PDF discovery | `site:jaipur.manipal.edu filetype:pdf` | Official PDFs and PDF-like results | Yes, public administrative and policy material | `https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf` | Useful for official documentation, not evidence of student-record exposure |
| Register-number discovery | `site:jaipur.manipal.edu filetype:pdf register number` | Official administrative pages, but no confirmed student-specific register list | No confirmed first-party student-record hit observed | `https://www.jaipur.manipal.edu/administration-registrar.php` | No confirmed sensitive artifact in observed results |
| Marks discovery | `site:jaipur.manipal.edu filetype:pdf marks marksheet result` | Examination page and third-party result pages | No confirmed MUJ-hosted individual or bulk marksheet PDF observed | `https://www.jaipur.manipal.edu/examination.php` | Public examination information only |
| Fee discovery | `site:jaipur.manipal.edu filetype:pdf fee fees` | Official fee notices and fee pages | Yes, public fee notice | `https://jaipur.manipal.edu/img/pdf/Notification_Annual-Fee-Payment-AY-2025-26.pdf` | Useful public administrative artifact |
| Fee-page discovery | `site:jaipur.manipal.edu fee structure` | Official course fee page | Yes | `https://jaipur.manipal.edu/fee-structure.php` | Public course-fee information, not individual payment data |
| Spreadsheet discovery on Manipal | `filetype:xlsx site:manipal.edu` | Mixed results, including unrelated or cross-scope content | No confirmed MUJ student workbook observed | `https://cia.manipal.edu/content/dam/manipal/mu/kmc-manipal/Documents/TOX%20STAT%20whole%20year.xlsx` | Cross-scope result; not MUJ SLCM evidence |
| Spreadsheet discovery on MUJ | `filetype:xlsx site:jaipur.manipal.edu` | Search titles containing `.xlsx`, but returned URLs ending in `.pdf` | No confirmed XLSX file observed | `https://jaipur.manipal.edu/img/pdf/research/muj/List%20of%20Patent%20Status_01.04.2024.pdf` | Search-title/file-extension mismatch |
| SLCM URL discovery | `inurl:slcm Manipal Jaipur` | MUJ portal, MAHE SLCM, Dubai SLCM, and third-party material | Yes | `https://mujslcm.jaipur.manipal.edu/` and `https://slcm.manipal.edu/` | Requires institutional disambiguation |
| MUJ SLCM URL discovery | `inurl:mujslcm` | MUJ root and `/Home/Index` | Yes | `https://mujslcm.jaipur.manipal.edu/Home/Index` | Public login route observed |
| Portal title discovery | `intitle:"MUJ portal"` | Exact official title appears in result output as "muj portal - Manipal University" | Yes | `https://mujslcm.jaipur.manipal.edu/` | Strong discovery query for the portal root |
| Target-host discovery | `site:mujslcm.jaipur.manipal.edu` | Root and `/Home/Index` login-oriented results | Yes | `https://mujslcm.jaipur.manipal.edu/` and `https://mujslcm.jaipur.manipal.edu/Home/Index` | No public record artifact observed |
| SLCM documentation | `MUJ SLCM FAQ registration link` | Official FAQ PDF | Yes | `https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf` | Strong official corroboration |
| Payment integration | `MUJ annual fee payment student portal` | Official payment page | Yes | `https://jaipur.manipal.edu/pay-fee-online.php` | Explicitly links to the SLCM URL [20] |

The main result is not that every dork found a sensitive file. The main result is that the dorks separate public administrative material from login surfaces and from noisy third-party material. The most useful official artifacts are the SLCM FAQ, the payment page, the annual-fee notice, the public course-fee page, and the examination page.

## Official SLCM and Portal Artifacts

The strongest official evidence is the SLCM FAQ hosted on the MUJ domain. Its search result identifies it as "Frequently Asked Questions and Contacts for SLCM Registration" and explicitly displays the registration link `https://mujslcm.jaipur.manipal.edu/` [12]. The extracted document confirms the same registration link [12]. This makes the relationship between MUJ's official web presence and the SLCM host directly observable rather than merely inferred from naming.

The target root is indexed as a page titled "muj portal - Manipal University". The visible text includes "WELCOME TO MUJ PORTAL," "Sign In," parent login, student login, and a password-recovery prompt [1]. The extracted landing page likewise shows the public welcome and sign-in labels [1]. These are account-entry functions. They do not establish that any student data, grades, fee receipts, or profile information is exposed without authentication.

The `/Home/Index` path is separately returned in search results with the title "Manipal University - mujslcm.jaipur.manipal.edu" and visible sign-in labels [3]. A separate search result shows the same path with only a "Forgot Password?" snippet [3]. Because the application appears to expose an MVC-style route in its public URL, an analyst might infer a conventional server-side web application, but that is only an inference from URL shape. It is not proof of ASP.NET MVC 5.3, .NET Framework 4.x, or a particular server configuration.

The alternate host `https://muj.slcm.jaipur.manipal.edu/` is also indexed with MUJ portal text [2]. The existence of two similar hostnames is operationally important because users, search engines, and incident responders could confuse them. It is not safe to assume that both are current, equivalent, owned by the same service, or configured identically. The club should report the URLs separately and ask MUJ to confirm canonical ownership and redirect policy.

The broader `https://slcm.manipal.edu/` result is labeled "MU SLcM" and includes a footer identifying Manipal Academy of Higher Education, Manipal [6]. That page is therefore relevant to the wider Manipal naming ecosystem but is not, based on the observed text, proof of the MUJ deployment. Cross-institutional results are a major source of false positives in `inurl:slcm` searches.

## Fee and Examination Dorks: Useful but Not Student-Specific

Fee-related searches produced several useful official pages. The MUJ payment page states that existing students can pay online and identifies the student portal URL as `https://mujslcm.jaipur.manipal.edu/` [20]. This is a direct official relationship between a public payment-information page and the SLCM host. It does not expose a receipt, balance, transaction history, or student identity in the returned public content.

The official annual-fee notice is a more concrete public artifact. Its extracted text identifies the date as June 24, 2025 and states that the last date for payment of the annual course fee for academic year 2025-26 was July 18, 2025 [18]. The notice is an administrative communication to enrolled students, not a student-specific account record. Its presence is therefore a useful positive result for the fee dork, but it should be categorized as low sensitivity public information compared with individualized payment data.

The public examination page describes how student performance is assessed. It lists class or tutorial participation, assignments, laboratory work, class tests, in-semester tests, quizzes, and end-semester examinations as contributors to the final grade [10]. This is useful context for understanding why marks-related search terms are sensitive, but the page itself is not a marksheet and does not establish that marks are indexed in a public PDF.

The public course-fee page is also indexed under the MUJ domain and presents course-related fee information. The extracted page contains school and department links and public fee-structure content [4]. The search result describes tuition fee, registration fee, and caution-deposit information [4]. These pages are appropriate examples of legitimate public indexing. A security review should distinguish a university's intended fee schedule from an unintended individual fee receipt.

| Artifact category | Public evidence observed | Sensitive student record observed? | Recommended classification |
|---|---|---:|---|
| SLCM FAQ | Official FAQ links to the SLCM registration URL [12] | No | Public administrative document |
| Annual fee notice | Date and 2025-26 payment deadline are stated [18] | No | Public administrative notice |
| Payment information page | Public page links existing students to the SLCM URL [20] | No | Public service information |
| Course-fee page | Public course and fee-structure information [4] | No | Public fee schedule |
| Examination page | Public description of assessment components [10] | No | Public academic policy information |
| Individual receipt or ledger | Not observed in confirmed official hits | No confirmed hit | Requires immediate owner review if found |
| Individual marksheet or bulk marks list | Not observed in confirmed official hits | No confirmed hit | Requires immediate owner review if found |

The decision-ready conclusion is that fee and examination dorks are useful for mapping intended public information, but the observed evidence does not support a claim of publicly indexed individual academic or financial records.

## Register Numbers, Marks, and Student-List Results

The register-number searches were the most privacy-sensitive. A focused search for official MUJ PDFs containing register numbers or student identifiers returned the official registrar page, the examination page, and a third-party Scribd result. The third-party result claims that a document contains student registration numbers, emails, genders, departments, names, and degrees [19]. That result was not treated as an official MUJ-domain artifact, was not used to establish a MUJ exposure, and should not be copied or redistributed.

The difference between a third-party claim and a confirmed official exposure is material. A search engine may index a user-uploaded copy, a scraped document, a student-created list, or a mislabeled file. None of those possibilities proves that MUJ published the data or that the data is current. The correct incident-response treatment is to preserve the result URL and timestamp, avoid opening or downloading sensitive content unless explicitly authorized for evidence collection, and notify the institution through a coordinated channel.

Marks-related searches returned the public examination page and third-party result guides. One third-party result page claims that MUJ results include student marks, but that is a secondary description, not a confirmed first-party marksheet URL in the observed results [21]. The official MUJ examination page provides assessment policy information [10], while the official homepage result mentions a PhD entrance-exam result and interview notice [9]. Those are public announcements and should not be conflated with bulk semester marks or personal scorecards.

The result status is therefore **no confirmed official student-record hit observed**. This wording is deliberate. Search-engine indexing changes over time, results vary by location and account state, and an unreturned result does not prove absence. It only records what was visible during this passive review. The university's own web, document-management, and search-console logs are better sources for determining whether a record was ever indexed.

The club should also avoid publishing query output that includes names, email addresses, registration numbers, or other identifiers. Even if a document is already searchable, republication increases harm and may breach university policy or applicable privacy obligations. A safe club report can state the category, URL, result title, and redacted evidence without reproducing the underlying data.

## XLSX and File-Type Findings

The requested spreadsheet query was `filetype:xlsx site:manipal.edu`, with additional MUJ-focused variants. The results were noisy. One official-domain result was a URL ending in `.xlsx` under `cia.manipal.edu`, but it related to a KMC Manipal document rather than MUJ SLCM [22]. Another result was a GitHub repository containing a workbook about Manipal call-centre analysis [23]. Those are not confirmed MUJ SLCM artifacts.

The MUJ-focused search returned results whose titles included `IPRDetails (6).xlsx` and `Details of External Grants and Industry_DoR_Dr. Manish_01.04.2024.xlsx`, but the actual URLs ended in `.pdf`, including the patent-status PDF and research-project PDFs. This is a useful false-positive pattern. Search indexes may derive titles from embedded document metadata, a source filename, or a conversion pipeline. A title containing `.xlsx` is not sufficient to establish that the retrieved object is an Excel workbook.

The official public PDFs were classified as research or administrative documents rather than student records. The patent-status result and research-project results are not evidence of exposed registration numbers or marks. The report should therefore state that no confirmed MUJ-hosted XLSX workbook was observed in the tested result set, while acknowledging that official MUJ PDFs with spreadsheet-like titles were returned.

| Result pattern | Example | Why it matters | Safe conclusion |
|---|---|---|---|
| Actual XLSX URL, cross-scope | `https://cia.manipal.edu/content/dam/manipal/mu/kmc-manipal/Documents/TOX%20STAT%20whole%20year.xlsx` [22] | File extension and host are visible, but institution is not MUJ SLCM | Cross-scope Manipal artifact, not MUJ evidence |
| GitHub workbook | `https://github.com/Nikhilshetty1/Manipal-call-centre-analysis/blob/master/final_revenue.xlsx` [23] | Public workbook is third-party hosted | Not an official MUJ artifact |
| XLSX-like title, PDF URL | `https://jaipur.manipal.edu/img/pdf/research/muj/List%20of%20Patent%20Status_01.04.2024.pdf` | Metadata or title can differ from URL extension | Treat as PDF, not XLSX |
| Official research PDF with XLSX-like title | `https://jaipur.manipal.edu/img/pdf/research/muj/List%20of%20Research%20Projects_Industry_01.04.2024.pdf` | Search result may preserve an original spreadsheet name | Public research document, not student data |
| Confirmed MUJ student workbook | None observed | No first-party hit confirmed | Do not claim exposure |

The recommended remediation is to inventory official document directories, confirm MIME types and access controls, and remove or restrict any workbook containing personal data. Search-engine operators alone should not be treated as the university's complete document inventory.

## Technology and Identity Claims

The requested scope names ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 identity. The public search and page evidence gathered in this review does not independently establish those exact versions or deployment components. A URL containing `/Home/Index` can be consistent with an MVC-style application, but it does not prove a particular framework version. Likewise, a login page or Microsoft-branded identity reference would not by itself prove the complete identity architecture.

The technology-focused searches returned generic Microsoft documentation and unrelated results rather than a public MUJ-specific fingerprint. The ASP.NET MVC search returned Microsoft Learn and .NET documentation, not a MUJ page that states MVC 5.3. The .NET Framework search returned generic version and installation documentation. The IIS search returned general IIS pages and the MUJ `/Home/Index` result, but no MUJ-specific statement of IIS 10. The Akamai search returned Akamai corporate pages without a MUJ-specific association. The Microsoft 365 search returned Microsoft product pages rather than evidence tied to the MUJ host.

These are negative or inconclusive findings, not proof of absence. Infrastructure headers, CDN configuration, application versions, and identity-provider relationships should be validated only through authorized internal asset inventories, vendor dashboards, configuration management, or an explicitly approved assessment. The club should not attempt to force error pages, inspect authenticated responses, probe version-specific routes, or test password-recovery behavior to obtain a fingerprint.

From a defensive perspective, the supplied stack assumptions are still useful as a risk-review checklist. If the owner confirms an older ASP.NET MVC or .NET Framework application, the owner should verify patch status, secure cookie settings, anti-forgery protections, output caching rules, error handling, and separation of authenticated content from public indexing. If Akamai is confirmed, the owner should review origin shielding, cache keys, authenticated-response caching, and purge procedures. If Microsoft 365 is used for identity, the owner should verify conditional access, MFA, sign-in risk controls, and correct redirect URI handling. These are recommendations, not findings about the live system.

## Defensive Recommendations for MUJ and the Security Club

**For MUJ web and identity owners:** review Search Console and server logs for the root host, the alternate host, the `/Home/Index` path, the FAQ PDF, fee documents, and any document directories. Confirm whether any authenticated response has ever been cached or indexed. Ensure that student-specific documents are delivered only after authorization and are not linked from public pages. Where indexing is not needed, apply appropriate access control and `noindex` directives, while recognizing that `noindex` is not a substitute for authorization.

**For document owners:** inspect PDF, XLSX, CSV, DOCX, and image repositories for names, registration numbers, email addresses, marks, fee receipts, attendance, or student identifiers. Remove stale copies and search-engine cache exposure through the institution's approved takedown process. Do not rely on filenames or titles alone; confirm the actual file type and contents.

**For application owners:** verify that public login pages reveal minimal information, that password-recovery responses do not disclose account existence, and that authenticated pages cannot be cached as public content. These checks belong in an authorized test plan, not in an unsolicited club exercise.

**For the security club:** retain a dated log of each query, result title, exact URL, and classification. Redact all personal data. Do not download a suspected student list, attempt to open an exposed receipt, submit credentials, or use search results as a springboard for route enumeration. Send a concise report to the university's official IT or security contact and offer to provide the redacted evidence privately.

**For disclosure handling:** distinguish confirmed first-party MUJ evidence from third-party claims. The official SLCM FAQ and payment page are confirmed first-party references [12] [20]. The Scribd student-list claim is third-party and should be treated as an unverified privacy lead, not as a confirmed MUJ publication [19]. This distinction prevents both under-reporting and over-claiming.

## Synthesis

The ecosystem separates into three layers. The first is the **public institutional layer**, consisting of MUJ's official website, fee pages, examination information, notices, and the SLCM FAQ. It is intentionally indexable and supplies useful administrative context. The second is the **portal-entry layer**, represented by the MUJ SLCM root and `/Home/Index`, which are searchable but visibly login-oriented [1] [3]. The third is the **private student-service layer**, including the records that might exist after authentication, but for which this review found no confirmed publicly indexed MUJ artifact.

Across three dimensions, the findings diverge. In terms of evidence strength, official MUJ documents are strong for portal linkage and public fee information, while third-party pages are weak for proving institutional publication. In terms of sensitivity, general fee schedules and examination policies are low-risk public artifacts, whereas marks, registration numbers, email addresses, and individualized receipts would be high-risk. In terms of technology attribution, the URL and page text provide limited clues, but they do not establish the exact requester-supplied stack.

The most important tension is that a login page can be publicly indexed without the protected data being indexed. Indexing of an entry point is not equivalent to an authorization failure. Conversely, a third-party search result claiming to contain student information should not be ignored merely because it is not on the MUJ domain; it should be reported privately as a lead, with no redistribution of the content. The correct response combines restraint with owner-side verification.

The practical decision is therefore not to expand the dork list toward more invasive discovery. The useful next step is a controlled owner review: confirm canonical MUJ SLCM hostnames, inspect index coverage and cache behavior, audit document repositories, and validate the supplied technology assumptions through authorized records. The club's public report should preserve the distinction between what search engines displayed, what official MUJ pages stated, and what remains unknown.

## VERDICT

**Overall confidence: High for the observed search-result classifications; Moderate for the negative findings; Low for the unverified technology-stack claims.**

The public-only review confirms that MUJ SLCM login surfaces are indexed at the root and `/Home/Index`, that MUJ's official SLCM FAQ links to the root, and that the official payment page also identifies the root as the student portal [12] [20]. It confirms useful public fee and examination artifacts, including the 2025-26 annual-fee notice and its stated date and deadline [18].

The review did **not** confirm a publicly indexed MUJ-hosted marksheet, register-number list, individualized fee receipt, or student spreadsheet. It did identify a third-party student-data claim, but that result is not sufficient to attribute publication to MUJ and should not be reproduced [19]. It also identified search-title/file-extension mismatches in which official MUJ results appeared to have `.xlsx` titles while their URLs ended in `.pdf`.

The exact claims that ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 identity are present remain **unverified by the public evidence collected here**. They should be retained as owner-supplied hypotheses for an authorized defensive review, not published as independently confirmed findings.

**Recommended final disposition:** Informational OSINT finding, no confirmed public student-record exposure in the observed first-party results, monitor and remediate any third-party personal-data lead through coordinated disclosure, and ask MUJ to validate indexing, document access control, canonical hostnames, caching, and technology inventory.

## References

1. *muj portal - Manipal University*. https://mujslcm.jaipur.manipal.edu/
2. *Manipal University*. https://muj.slcm.jaipur.manipal.edu/
3. *Manipal University - mujslcm.jaipur.manipal.edu*. https://mujslcm.jaipur.manipal.edu/Home/Index
4. *Course Fee*. https://jaipur.manipal.edu/fee-structure.php
5. *Hostel Fee*. https://jaipur.manipal.edu/hostel-fees.php
6. [
	MU SLcM
](https://slcm.manipal.edu/)
7. *Student Portal Login- MAHE (Manipal Academy Of Higher Education)*. https://www.manipal.edu/mu/academics/student-portal.html
8. *Manipal University Jaipur | Manipal Academy of Higher Education*. https://www.manipal.edu/mu/important-links/world-wide-manipal/manipal-university-jaipur.html
9. *Manipal University Jaipur - 71 years of legacy of Manipal Education*. https://jaipur.manipal.edu/
10. *Examination - Manipal University Jaipur *. https://jaipur.manipal.edu/examination.php
11. *IPRDetails (6).xlsx*. https://jaipur.manipal.edu/img/pdf/research/muj/List%20of%20Patent%20Status_01.04.2024.pdf
12. *Frequently Asked Questions and Contacts for SLCM Registration*. https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf
13. *List Of Research Projects Industry 01.04.2024*. https://jaipur.manipal.edu/img/pdf/research/muj/List%20of%20Research%20Projects_Industry_01.04.2024.pdf
14. *List Of Research Projects Govt. 01.04.2024*. https://jaipur.manipal.edu/img/pdf/research/muj/List%20of%20Research%20Projects_Govt._01.04.2024.pdf
15. *Untitled*. http://muj.onlinemanipal.com/wp-content/uploads/sites/2/2024/10/Statute-MUJ.pdf
16. *MUJ CSE Faculty List and Details | PDF | Machine Learning ...*. https://www.scribd.com/document/632880872/Faculty-list-xlsx
17. *Manipal University Jaipur Student List | PDF - Scribd*. https://www.scribd.com/document/895442035/Manipal-Off-Campus-Stage-1-Selects
18. *Annual Fee Payment for the Academic Year 2025-26*. https://jaipur.manipal.edu/img/pdf/Notification_Annual-Fee-Payment-AY-2025-26.pdf
19. *Student Registration Data Overview | PDF - Scribd*. https://www.scribd.com/document/881889937/Eligible-Students-MUJ-1
20. *Pay Fee Online - Manipal University Jaipur *. https://jaipur.manipal.edu/pay-fee-online.php
21. *Manipal University Jaipur Results 2026 (Released): Check UG ...*. https://www.getmyuni.com/college/manipal-university-jaipur-result?page=result
22. *cia.manipal.edu*. https://cia.manipal.edu/content/dam/manipal/mu/kmc-manipal/Documents/TOX%20STAT%20whole%20year.xlsx
23. *Manipal-call-centre-analysis/final_revenue.xlsx at master ...*. https://github.com/Nikhilshetty1/Manipal-call-centre-analysis/blob/master/final_revenue.xlsx
