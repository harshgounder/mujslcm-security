# MUJ Exam Portal: Public Evidence, Gaps, and Risk

## Executive Summary

- **Purpose Is Not Publicly Proven**: MUJ's official material documents exam schedules, make-up applications, hall-ticket requirements, certificates, grading, and result declaration, but none of the reviewed official documents names `exam.jaipur.manipal.edu` or assigns those functions to it [2][15][16] -> treat "exam forms," "hall tickets," and "results" as hypotheses until MUJ confirms the service catalog.
- **NIB Hosting Is Strongly Corroborated**: Hurricane Electric reports `59.91.192.0/20` announced by AS9829 and identifies BSNL, while Netcraft maps the exact hostname to `59.91.192.229`, AS9829, and NIB [7][10] -> record the exam host as a directly addressed BSNL/NIB asset with high confidence.
- **The SLCM Comparison Contains A Tension**: the requester-supplied baseline says SLCM is Akamai-fronted, but current passive reports place `mujslcm.jaipur.manipal.edu` at `98.70.14.50` in Microsoft AS8075 and report first sighting in 2022 [18][19] -> do not assume the supplied CDN path is current or universal; validate it from owner-side DNS and edge inventories.
- **Credential Reuse Is Unverified**: official onboarding material says SLCM credentials are issued by Admissions and ties the password to the official Outlook identity, but the examination handbook and manual provide no SLCM authentication instructions or separate exam-host URL [14][13][15] -> never tell students that the exam host accepts SLCM credentials without a current MUJ instruction.
- **Public Technical Evidence Is Sparse**: URLScan has no scan results for the exam host, Shodan says no information is available for its IP, and Netcraft leaves title, first-seen date, and technology blank [3][8][10] -> classify exact framework, IIS version, TLS posture, and login implementation as unknown.
- **Archive Evidence Is A Negative Result, Not A History**: the exact-host Wayback CDX query returned an empty list, whereas SLCM has archived 200-status pages and assets -> conclude only that the queried archive contains no exact-host captures, not that the service never existed.
- **User-Impact Evidence Is Anecdotal**: one Reddit user reported that a password believed to be correct was rejected by SLCM, with no visible reply or resolution [1] -> use it as a case study in support friction, not as evidence of an exam-host outage or systemic failure.
- **Governance Is More Visible Than Technology**: MUJ publishes a Controller of Examinations, deputies, assistants, and examination helpdesk addresses, while its contact page identifies the Jaipur campus and main telephone number [2][4] -> route confirmation and responsible disclosure through MUJ's official examination and IT channels.
- **Defensive Action Should Stay Owner-Authorized**: Microsoft reports that MFA and blocking legacy authentication stop more than 99.9 percent of common identity attacks, and Conditional Access requires Entra ID P1 in the ordinary case [20][21] -> MUJ, not external researchers, should validate MFA, legacy-auth blocking, headers, patch state, logs, and decommissioning.

## Scope, Method, and Evidence Boundaries

This report examines public information about `exam.jaipur.manipal.edu` and its relationship to the broader MUJ SLCM ecosystem. The research cutoff is 2026-08-25. Collection was passive and non-authenticated: public search results, official MUJ pages and PDFs, passive network intelligence, certificate/archive indexes, and one public user report. No password was entered, no form was submitted, no endpoint was guessed, no port was scanned, and no attempt was made to bypass access controls.

I cannot provide private chain-of-thought or hidden deliberation. In its place, the report gives an auditable evidence trail: each conclusion is marked as verified, contradicted, unknown, or an explicit inference; tables expose the source and confidence behind each finding; and the final verdict separates what the evidence proves from what it merely suggests.

### Evidence and confidence model

| Level | Meaning in this report | Typical evidence |
|---|---|---|
| High | Two or more independent public sources agree on the exact fact | AS/prefix and IP mappings from HE, IPinfo, and Netcraft |
| Medium | An official source establishes the surrounding process, but not the exact host implementation | MUJ handbook, examination manual, and SLCM onboarding guide |
| Low | A plausible interpretation lacks direct host-specific confirmation | The exam host serves forms, hall tickets, or results |
| Unknown | The reviewed public record does not expose the answer | Exact framework version, login route, launch date, TLS configuration |

The critical methodological distinction is between an **ecosystem fact** and an **exact-host fact**. MUJ's official examination page proves that the university operates examination schedules, application formats, certificate services, and academic-record workflows [2]. It does not prove that `exam.jaipur.manipal.edu` delivers any particular one of them. Likewise, the SLCM landing page proves that the visible MUJ portal offers student and parent sign-in choices under the `@muj.manipal.edu` identity label [12]. It does not prove that the exam host shares the same session, password database, or identity provider.

Absence is handled narrowly. An empty Wayback response proves only that the specific CDX query returned no records. A URLScan page with zero results proves only that URLScan has no indexed scan result for the exact hostname [3]. These findings constrain confidence; they do not prove that the site was never online, private, intranet-only, DNS-limited, or excluded from crawling.

**Decision-ready insight:** the evidence is sufficient to map ownership context and network placement, but insufficient to publish a definitive product description or application fingerprint. The club should preserve that distinction in any presentation.

## What the Public Record Actually Establishes

MUJ's official examination material establishes a broad administrative system. The university describes continuous assessment through participation, assignments, labs, class tests, in-semester tests, quizzes, and end-semester examinations [2]. Its examination page exposes sections for the examination process, student information, schedules, application formats, the National Academic Depository, and APAAR/ABC IDs [2]. That is a substantial functional perimeter, but it is a perimeter around the **Examination Office**, not a service map for the target hostname.

The examination manual makes the operating model clearer. It says examination conduct, grade awards, and result processing are decentralized under the Controller of Examinations [15]. MTE and ETE schedules follow the annual academic calendar; the Office of CoE schedules some common and open-elective courses, while departments schedule others [15]. The Office of CoE declares results within 15 days after grade moderation and approval, and results can be held for unpaid dues or disciplinary matters [15]. These are verified business processes.

The 2023-24 Student Examinations Handbook also mentions hall tickets, but only as required identification. Students must carry authentic identification or an exam hall ticket; the handbook does not say how a hall ticket is generated, where it is downloaded, or which hostname serves it [16]. It describes GPA/CGPA, relative versus absolute grading, and the result-declaration timeline, yet contains no `exam.jaipur.manipal.edu` URL [16]. The manual likewise names an exam hall ticket in malpractice guidance but gives no issuance workflow [15].

### Function attribution matrix

| Candidate function | Public evidence | Exact-host attribution | Confidence |
|---|---|---|---|
| Examination schedules | MUJ publishes schedule sections and timetable PDFs [2] | No reviewed source assigns them to the exam host | Medium for MUJ process; low for host |
| Exam forms | MUJ publishes application formats and a make-up application process [2] | No exact-host URL is named | Medium for MUJ process; low for host |
| Hall tickets | Handbook/manual require an exam hall ticket or authentic ID [16][15] | Issuance and download location are not stated | Medium for existence; low for host |
| Results | Office of CoE declares results after moderation and approval [15] | Publication channel is not stated | High for process; low for host |
| Certificates/transcripts | Official page lists transcripts, provisional certificates, duplicate documents, grade reports, and other services [2] | Workflow uses forms, online payment, and examination email addresses, not the target host [2] | High for process; low for host |
| NAD/ABC/DigiLocker | Official page links those named external portals [2] | They are separate services, not evidence about the exam host | High |

**Inference - low confidence:** the hostname label `exam` and MUJ's documented exam workflows make a student examination application plausible. However, the public evidence does not justify narrowing that application to exam registration, hall-ticket delivery, result publication, or all three. The correct OSINT answer is "not publicly established," not a guessed feature list.

**Case study - hall ticket ambiguity:** two official documents independently establish that an exam hall ticket exists as a student credential [15][16]. Neither gives a download URL, and neither mentions the exact host. This is a useful warning against an OSINT failure mode: converting a business artifact's existence into an unsupported claim about the system that produces it.

**Decision-ready insight:** describe the target as "an MUJ-domain host plausibly related to examinations, with no publicly verified feature assignment." Anything more specific needs a current first-party notice or authorized operator confirmation.

## Hosting and Technology: NIB Origin Versus The SLCM Baseline

The strongest exact-host evidence concerns network placement. Hurricane Electric reports that `59.91.192.229` falls in `59.91.192.0/20`, announced by AS9829, and labels the announcer BSNL [7]. IPinfo independently identifies AS9829 as National Internet Backbone and places the address in a broader `59.91.192.0/20` context [5]. Netcraft maps `http://exam.jaipur.manipal.edu` to IPv4 `59.91.192.229`, AS9829, hosting company Bharat Sanchar Nigam, and netblock owner NIB [10]. This supports the NIB statement with high confidence.

Geolocation is less reliable and internally inconsistent. IPinfo shows Hoshiarpur, Punjab [5], while URLScan's domain summary associates the address with Dehradun [6]. These are database geolocations, not proof of server-rack location. **Inference - medium confidence:** the disagreement is a reason to report only country and network ownership, not a precise physical city.

The exact technology fingerprint is not established. Shodan returns `404: Not Found` and says no information is available for the IP [8]. URLScan reports no results for the hostname [3]. Netcraft leaves site title, first-seen date, and description blank and shows its technology field as loading rather than naming IIS, ASP.NET, .NET, or an MVC version [10]. Netcraft also labels the queried HTTP URL as not an HTTPS site [10], but that statement does not prove that TCP/443 is closed or that no other TLS hostname exists.

### Infrastructure comparison

| Dimension | `exam.jaipur.manipal.edu` | `mujslcm.jaipur.manipal.edu` | Security implication |
|---|---|---|---|
| Public IPv4 | `59.91.192.229` [10] | `98.70.14.50` [18] | Distinct delivery stacks |
| ASN | AS9829 [7][10] | AS8075 [18][19] | NIB/BSNL versus Microsoft network |
| Hosting label | Bharat Sanchar Nigam; NIB [10] | Microsoft India Central; Microsoft Corporation [18] | Different operational dependencies |
| Passive first seen | Not present in Netcraft [10] | July 2022 in Netcraft [18] | Exam-host age remains unknown |
| URLScan observations | Zero exact-host results [3] | Not observed as a scan, though CT-derived hostnames are listed [19] | Sparse third-party visibility for both |
| Technology/version | Not shown [10] | Netcraft technology still "Loading..." [18] | Do not publish exact versions from these sources |
| HTTPS statement | Netcraft says the queried URL is not an HTTPS site [10] | Certificate details are still loading [18] | Owner-side TLS validation is required |

The requester supplied an SLCM baseline of ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 identity. This research found official and passive support for a Microsoft-linked identity context, but not public, citation-grade confirmation of all those exact software versions. It also found a current passive IP in Microsoft AS8075 rather than an Akamai ASN [18][19]. **Inference - medium confidence:** this could reflect a changed architecture, an origin exposed by one data source, split DNS, or a baseline captured at another time. It cannot be resolved from the current public record.

**Decision-ready insight:** inventory the exam host as a separate NIB/BSNL asset. Do not automatically inherit SLCM's claimed CDN, framework, patch status, or identity controls onto it.

## Login and Identity: SLCM Is Documented, Exam Integration Is Not

The public SLCM flow is clear at a high level. The landing page presents the MUJ portal, `@muj.manipal.edu`, a student sign-in, a parent-login choice, and a forgot-password option [12]. The official first-year guide calls SLCM a one-stop platform for academic information and directs students to `https://mujslcm.jaipur.manipal.edu` [14]. It says Admissions sends the SLCM username and password to the student's personal Gmail account and supplies a procedure for resetting the official email password [14].

A separate official FAQ adds more detail. It gives the SLCM registration link, shows a username format based on name plus registration number, and says the password is "as per official outlook ID" [13]. For a non-working MUJ Outlook account, it tells users to reset the password [13]. The Microsoft Online Password Reset page itself asks for an email address or username to begin account recovery [22]. Taken together, these sources support a Microsoft/Outlook-linked SLCM credential workflow.

They do not establish the exact backend identity pattern. The pages do not state whether SLCM uses password-hash synchronization, pass-through authentication, federation, an app-local password check against Outlook-derived credentials, or another integration. Microsoft describes password-hash synchronization as synchronizing a hash from on-premises Active Directory to Entra ID and allowing the same password for Microsoft 365 [23]. That is an available architecture pattern, not evidence that MUJ selected it.

### Login-flow evidence matrix

| Question | SLCM evidence | Exam-host evidence | Assessment |
|---|---|---|---|
| Where does a student start? | Official guide names the SLCM URL [14] | No public landing content or instruction was found | SLCM verified; exam unknown |
| What username is used? | FAQ gives name plus registration-number format [13] | No source states a username | Unknown for exam |
| What password is used? | FAQ ties it to official Outlook ID [13] | No source says "use SLCM credentials" | Credential reuse unverified |
| Who issues credentials? | Department of Admissions sends them to personal Gmail [14] | No issuing authority is named | Unknown for exam |
| How is password recovery handled? | Official material references reset of the MUJ Outlook password [13] | No reset route is documented | Unknown for exam |
| Are parent accounts separate? | Public SLCM page shows a parent-login option [12] | No parent flow is visible | SLCM-only evidence |
| Does SSO exist between the two hosts? | No official document states this | No redirect/session evidence is public | Not established |

**Inference - medium confidence:** SLCM is connected operationally to MUJ's Outlook/Microsoft identity because the official FAQ explicitly ties the password to the Outlook ID. **Inference - low confidence:** that does not prove modern SSO. A page can accept the same password without sharing an Entra session, and a separate application can maintain its own authentication path.

**Case study - onboarding versus exam access:** the first-year guide is detailed enough to specify who sends credentials, where they are sent, and where SLCM starts [14]. Yet it says nothing about exam registration, hall tickets, results, or `exam.jaipur.manipal.edu` [14]. The silence is meaningful for confidence calibration: when MUJ intends to document a portal, it can name it precisely. No equivalent first-party instruction was found for the exam host.

**Decision-ready insight:** the club should publish a red warning beside any credential-reuse claim: "No reviewed MUJ source confirms that exam.jaipur.manipal.edu accepts SLCM credentials or shares SLCM sessions."

## Indexed Surface and Archive History: Sparse By Every Public Measure

The exact host has a notably thin public footprint. URLScan's API search returns zero results [3]. Its domain summary nevertheless associates the hostname with `59.91.192.229` and AS9829, but reports no direct or incoming hits [6]. Shodan says no information is available for the IP [8]. Netcraft provides network ownership but no title, description, rank, first-seen date, or technology name [10].

The Wayback CDX query for `exam.jaipur.manipal.edu/*`, filtered to status 200 and collapsed by digest, returned an empty JSON array. That is the most precise archive finding available here. It does not establish a launch date, retirement date, historical page title, or past feature set.

By contrast, the SLCM host has publicly indexed archive rows for its root, `/Home/Index`, a favicon, login CSS, theme assets, and fonts. The passive SLCM report also says Netcraft first saw the site in July 2022 [18]. URLScan says it has not observed a scan but lists CT-derived hostnames dated 2022 and 2024 [19]. This contrast shows that sparse visibility is host-specific rather than universal across MUJ's ecosystem.

### Public-footprint ledger

| Source | Exact exam-host result | What it proves | What it does not prove |
|---|---|---|---|
| General web indexing | No exact-host page with purpose or login instructions surfaced | Search discoverability is poor | Site absence or access policy |
| URLScan API | Zero results [3] | No indexed URLScan result | No web service exists |
| URLScan domain summary | Host/IP/ASN mapping; no direct or incoming hits [6] | Passive association exists | Page content or technology |
| Shodan | No information for the IP [8] | Shodan has no public host record | Ports are closed |
| Netcraft | IP, ASN, hoster, and netblock owner [10] | Network placement | Framework or current response behavior |
| Wayback CDX | Empty array | No rows matched this query | Site never existed |
| Official MUJ PDFs | No exact-host URL in guide, manual, or handbook [14][15][16] | Reviewed documents do not name it | No internal or newer instruction exists |

**Inference - medium confidence:** the target may be intended for a narrow authenticated population, may be dormant, may reject automated retrieval, or may have little crawl exposure. The public evidence cannot choose among those explanations. Calling it "hidden," "internal," or "dead" would overstate the data.

**Decision-ready insight:** preserve the negative results as dated evidence. Repeating passive checks later can reveal change without turning the club's work into active probing.

## Operator, Support, and Governance

The hostname is under `jaipur.manipal.edu`, and Netcraft lists the registered domain organization as Manipal Academy of Higher Education at Madhav Nagar, Manipal, Karnataka [10]. The target's institutional context is Manipal University Jaipur: the official contact page identifies MUJ at Dehmi Kalan, off the Jaipur-Ajmer Expressway, Jaipur, Rajasthan 303007, with main phone `+91 141-3999100` [4]. These facts distinguish domain-level registration context from campus-level operations.

MUJ's official examination page names the Controller of Examinations, Dr. Dasari Nagaraju; Deputy CoE Dr. Pooja Sharma; and several Assistant Controllers, with extensions and university email addresses [2]. It also publishes `exam.helpdesk@jaipur.manipal.edu` and `exam.store@jaipur.manipal.edu` for examination-document processing [2]. The SLCM FAQ identifies `it.support@jaipur.manipal.edu`, the main helpline, Admissions, DMS, and Academic Section contacts [13].

### Governance and contact map

| Role or channel | Publicly documented responsibility/context | Appropriate use |
|---|---|---|
| Controller of Examinations and CoE team | Examination governance and named roles [2] | Confirm the exam host's business purpose and owner |
| `exam.helpdesk@jaipur.manipal.edu` | Examination applications/document process [2] | Student-facing process questions |
| `exam.store@jaipur.manipal.edu` | Receipt of forms and payment receipts for document services [2] | Certificate/document processing |
| `it.support@jaipur.manipal.edu` | IT Infra contact in SLCM FAQ [13] | Technical ownership or responsible-disclosure routing |
| Admissions | Sends first-year SLCM credentials [14] | Credential issuance/onboarding questions |
| Main campus contact | `+91 141-3999100`, Jaipur campus [4] | Escalation when the correct owner is unclear |

**Inference - medium-high confidence:** MUJ operates the exam-related business process and is the most likely campus-level operator of the host. **Unknown:** the public sources do not identify the server administrator, application vendor, data owner, SOC, hosting contract, or change-management authority. Netcraft's domain organization should not be mistaken for proof that MAHE directly administers this particular server.

A responsible disclosure should be minimal and non-invasive: exact URL, UTC timestamp, browser-visible behavior, and business impact, without credentials, student records, exploit payloads, or data samples. The club should ask MUJ for a written testing scope before any activity beyond ordinary public browsing.

**Decision-ready insight:** governance attribution is stronger than technical attribution. Address findings to MUJ Examination and IT; phrase server-operator identity as an inference until MUJ confirms it.

## Public Complaints and User Impact

The only directly relevant public complaint surfaced in this review concerns SLCM, not `exam.jaipur.manipal.edu`. In a Reddit post on `r/manipaljaipur`, a user wrote, "My password is showing error even though ik that is correct" and asked whether others faced the issue [1]. The indexed content shows no visible reply or resolution [1]. This verifies that at least one user publicly reported authentication friction; it does not establish root cause, duration, scope, or prevalence.

The official support material anticipates similar categories of difficulty. The SLCM FAQ advises users with AMS login problems to re-verify credentials and then contact DMS or AMS addresses if the issue remains [13]. It directs users whose MUJ Outlook account is not working to reset the password [13]. The first-year guide tells students with technical issues to contact the University Helpdesk or Admissions [14]. Those instructions show that MUJ has support routes, but not that any one route resolves the Reddit user's case.

### Complaint evidence table

| Evidence | Target | Symptom | Resolution visible? | Weight |
|---|---|---|---|---|
| Reddit post | SLCM | Password rejected despite user's belief it was correct [1] | No [1] | Single anecdote |
| Official SLCM FAQ | SLCM/AMS/Outlook | Credential and account-access troubleshooting [13] | Contact/reset instructions | Official process, not incident data |
| Exact-host searches | `exam.jaipur.manipal.edu` | No indexed complaint specifically naming the host surfaced | Not applicable | Negative search result only |

**Inference - low confidence:** the anecdote could reflect a mistyped credential, password synchronization lag, account state, service outage, or another cause. No public evidence selects among them. It would be misleading to call it an SLCM security failure, and still more misleading to transfer it to the exam host.

A useful club case study is the support burden created when one identity appears across multiple academic systems. Even if credentials are shared, users may not know whether to contact Admissions, IT, DMS, the Academic Section, or Examination. That ambiguity can increase insecure behaviors such as repeated password entry on look-alike pages. The corrective action is organizational: publish a canonical portal directory, owner, purpose, identity method, and support channel for each hostname.

**Decision-ready insight:** report the complaint as one unresolved SLCM login anecdote. State explicitly that no public exact-host complaint trend was established.

## Defensive Risk Review and Authorized Research Agenda

Because the exact stack and login flow are unknown, a vulnerability list would be speculative. A safer approach is an owner-run control review organized around confidentiality, integrity, availability, and identity assurance. The direct NIB placement and sparse public footprint make asset ownership and lifecycle management the first questions, not exploitation.

### Owner-authorized control plan

| Priority | Owner-only validation | Why it matters | Public evidence motivating it |
|---|---|---|---|
| 1 | Confirm whether the hostname is active, its business owner, data classification, and retirement date | Prevents forgotten or orphaned academic assets | No public first-seen date or purpose [10] |
| 2 | Inventory DNS, reverse proxy/CDN, origin, firewall, certificates, and approved exposure | Resolves NIB versus Microsoft/Akamai architecture uncertainty | Exam host maps to AS9829; SLCM passive data maps to AS8075 [10][18] |
| 3 | Document the exact identity protocol and credential authority for each portal | Stops unsafe assumptions about password reuse and SSO | Official material documents SLCM credentials but not exam-host integration [14][13] |
| 4 | Enforce MFA and appropriate Conditional Access on modern identity paths | Reduces password-spray, phishing, and replay exposure | Microsoft says MFA plus blocking legacy authentication stops more than 99.9 percent of common identity attacks [20] |
| 5 | Block legacy authentication where compatible and monitor exceptions | Legacy protocols are disproportionately used in password spray and credential stuffing | Microsoft reports more than 97 percent of credential stuffing and more than 99 percent of password spray use legacy authentication [24] |
| 6 | Validate TLS, HSTS, secure cookies, CSRF defenses, CSP, frame protections, and error handling | Academic records and credentials require transport and session protection | Netcraft labels the queried exam URL non-HTTPS, while exact TLS details remain unverified [10] |
| 7 | Patch the OS, IIS/.NET/runtime, dependencies, and application according to an owner-maintained SBOM | Exact public version claims are not trustworthy enough for risk decisions | Passive sources expose no exam-host technology version [8][10] |
| 8 | Centralize sign-in, admin, export, result-change, and document-access logs with alerting | Supports incident detection and grade-record integrity | Results and grade processing are formal CoE functions [15] |
| 9 | Publish a canonical portal directory and anti-phishing guidance | Helps students distinguish MUJ, SLCM, exam, NAD, ABC, and DigiLocker services | MUJ's exam page links several separate record portals [2] |
| 10 | Test backup, restore, peak-exam capacity, and support escalation | Exam periods create availability and deadline risk | Schedules and result timelines are time-bound [15] |

Conditional Access is not a universal free control: Microsoft says the feature ordinarily requires Entra ID P1, while risk-based policies require P2 [21]. Security defaults may be an alternative for tenants without P1/P2, but Microsoft says they are probably not appropriate for organizations that already have those licenses [20]. This licensing distinction should be part of the university's design decision.

**Case study - direct origin versus managed edge:** the target maps to AS9829/NIB, while the current SLCM passive record maps to Microsoft AS8075 [10][18]. If the exam host is genuinely direct-to-origin, owner-side review should ask whether a reverse proxy, WAF, rate limiting, DDoS protection, and centralized certificate management are intentionally absent or simply invisible to passive data. This is a question for MUJ's administrators, not an invitation for the club to probe the server.

**Decision-ready insight:** the club's next step should be a written, owner-approved architecture interview and evidence request. External testing should begin only after scope, authorization, test windows, data-handling rules, and emergency contacts are documented.

## Synthesis

The evidence produces a three-system picture rather than one homogeneous portal stack. The official Examination Office owns the academic process; SLCM owns documented student onboarding and Outlook-linked credentials; the exact exam hostname is a sparsely indexed NIB-hosted asset whose application role remains unverified.

### Cross-system comparison

| Dimension | Official examination process | SLCM portal | Exact exam host |
|---|---|---|---|
| Scope | Schedules, grading, results, certificates, applications [2] | Academic-information onboarding and account access [14] | Unknown application scope |
| Mechanism | Decentralized academic process under CoE [15] | Named URL, student/parent login, Outlook-linked password [13][12] | No public login flow |
| Infrastructure | Public MUJ web/PDF publishing | Microsoft AS8075 in current passive reports [18] | BSNL/NIB AS9829 [7][10] |
| Identity evidence | None in handbook/manual [15][16] | Admissions-issued credentials and Outlook reset process [14][13] | No proven credential bridge |
| Historical evidence | Dated handbook and schedules [16][2] | First seen July 2022 by Netcraft [18] | Wayback query empty; Netcraft first seen absent [10] |
| Trade-off | Strong governance detail, little system architecture | Better user documentation, identity concentration risk | Low discoverability, high uncertainty |
| Evidence base | First-party official sources | First-party guides plus passive records | Mostly passive third-party network data |

The non-obvious tension is that the best-documented exam functions do not point to the exam hostname, while the best-documented identity flow points only to SLCM. Another tension is infrastructure: the supplied SLCM baseline invokes Akamai and a classic ASP.NET stack, but the current passive record points to Microsoft AS8075 and does not expose exact software versions [18]. Neither tension can be solved by assuming all `jaipur.manipal.edu` applications share one architecture.

The strongest holistic conclusion is therefore about **separation**. Business-process ownership, identity ownership, and network hosting appear in different evidence layers. This separation can be healthy if intentional, documented, and monitored. It becomes risk when students reuse credentials without a clear trust boundary, administrators lose track of a direct origin, or support teams cannot identify the owner of a failing portal.

**Inference - medium confidence:** `exam.jaipur.manipal.edu` is probably institutionally connected to MUJ examinations because of its name and domain, and MUJ's Examination Office is the logical business owner. **Inference - low confidence:** it hosts forms, hall tickets, results, or SLCM-authenticated workflows. The evidence supports the former much more than the latter.

**Decision-ready insight:** treat the host as an unverified, potentially sensitive academic asset. Ask MUJ to publish a purpose statement, canonical URL, identity method, support owner, privacy notice, and retirement status. Until then, students should rely only on current first-party instructions.

## VERDICT

**Overall confidence: Medium.** Confidence is high for network placement, medium-high for institutional context, medium for the surrounding examination and SLCM processes, and low for the target application's exact purpose, technology, login flow, archive history, and credential integration.

| Verdict question | Finding | Confidence |
|---|---|---|
| Is the hostname tied to `59.91.192.229` on NIB/BSNL AS9829? | Yes, corroborated by HE and Netcraft [7][10] | High |
| Who is the likely institutional operator? | Manipal University Jaipur, probably through its Examination/IT governance; direct server administration is not public [2][4] | Medium-high inference |
| Does it serve exam forms? | Not publicly established | Low |
| Does it deliver hall tickets? | Hall tickets exist in MUJ policy, but the delivery host is not named [16] | Low |
| Does it publish results? | MUJ's CoE declares results, but the publication host is not named [15] | Low |
| What technology does it run? | Unknown from the reviewed citation-grade public sources | Low |
| Is HTTPS/TLS confirmed? | Netcraft labels the queried HTTP site non-HTTPS; live TLS posture was not independently established [10] | Low |
| Does it accept SLCM credentials or share SSO? | No reviewed first-party source confirms either | Low |
| Are there systemic complaints? | No. One indexed anecdote concerns SLCM password rejection, not the exam host [1] | Low for prevalence |
| What is its archive history? | Exact-host Wayback CDX returned no rows; launch and change history remain unknown | High for query result; low for history |

The defensible final statement is: **`exam.jaipur.manipal.edu` is a low-visibility MUJ-domain asset mapped by multiple passive sources to `59.91.192.229` in BSNL/National Internet Backbone AS9829. Public sources do not establish its application purpose, software stack, active login flow, use of SLCM credentials, or historical timeline.** Any claim that it is the hall-ticket, exam-form, or result portal should be labeled an unverified inference.

No unauthorized access is necessary or appropriate to close these gaps. The correct next step is operator confirmation and, if MUJ wants technical assurance, a separately authorized assessment with written scope.

## References

1. *Reddit - The heart of the internet*. http://reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue
2. *Examination - Manipal University Jaipur *. https://jaipur.manipal.edu/examination.php
3. *urlscan.io*. https://urlscan.io/api/v1/search/?q=domain:exam.jaipur.manipal.edu
4. *Contact Us - Manipal University Jaipur *. https://jaipur.manipal.edu/contact-university.php
5. *59.91.192.229 | Hoshiārpur, AS9829, VPN Not Detected | IPinfo*. https://ipinfo.io/59.91.192.229
6. *exam.jaipur.manipal.edu - urlscan.io*. https://urlscan.io/domain/exam.jaipur.manipal.edu
7. *59.91.192.229 - bgp.he.net*. https://bgp.he.net/ip/59.91.192.229
8.(https://www.shodan.io/host/59.91.192.229)
9. [
        EXAM.JAIPUR.MANIPAL.EDU
    ](https://builtwith.com/exam.jaipur.manipal.edu)
10. *Site report for http://exam.jaipur.manipal.edu | Netcraft*. https://sitereport.netcraft.com/?url=http://exam.jaipur.manipal.edu
11. *Redirecting to Censys Platform*. https://search.censys.io/hosts/59.91.192.229
12. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
13. *Frequently Asked Questions and Contacts for SLCM Registration*. https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf
14. *Manipal University Jaipur First-Year Student Profile Registration Guide*. http://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf
15. *EXAMINATION MANUAL*. https://jaipur.manipal.edu/img/pdf/exam/3.%20Manual%20Exam%20Process.pdf
16. *Student Examinations Handbook*. https://jaipur.manipal.edu/img/pdf/exam/Student%20Examination%20Handbook%202023-24%20%2811.08.2023%29.pdf
17. [
        MUJSLCM.JAIPUR.MANIPAL.EDU
    ](https://builtwith.com/mujslcm.jaipur.manipal.edu)
18. *Site report for https://mujslcm.jaipur.manipal.edu | Netcraft*. https://sitereport.netcraft.com/?url=https://mujslcm.jaipur.manipal.edu
19. *mujslcm.jaipur.manipal.edu - urlscan.io*. https://urlscan.io/domain/mujslcm.jaipur.manipal.edu
20. *http://learn.microsoft.com/en-us/entra/fundamentals/security-defaults*. http://learn.microsoft.com/en-us/entra/fundamentals/security-defaults
21. *http://learn.microsoft.com/en-us/entra/identity/conditional-access/overview*. http://learn.microsoft.com/en-us/entra/identity/conditional-access/overview
22. [
	Microsoft Online Password Reset
](https://passwordreset.microsoftonline.com/)
23. *http://learn.microsoft.com/en-us/entra/identity/hybrid/connect/whatis-phs*. http://learn.microsoft.com/en-us/entra/identity/hybrid/connect/whatis-phs
24. *http://learn.microsoft.com/en-us/entra/identity/conditional-access/policy-block-legacy-authentication*. http://learn.microsoft.com/en-us/entra/identity/conditional-access/policy-block-legacy-authentication
