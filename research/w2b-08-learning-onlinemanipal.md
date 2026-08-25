# Brightspace and MUJ SLCM Public-Posture Assessment

## Executive Summary

- **Brightspace Attribution**: D2L's own Manipal University Jaipur case study identifies D2L Brightspace as the LMS selected for MUJ Online and describes a 2020 digital-learning initiative that reached 85,000 students in five years [5] [5] -> treat `learning.onlinemanipal.com` as a Brightspace tenant with high confidence, while keeping customer-reported scale and outcomes separate from an independent security assessment.

- **Tenant and Org-Unit Boundary**: The public route `https://learning.onlinemanipal.com/d2l/home/14042` is indexed as a Manipal University Jaipur login page, and the page exposes a username field and password-reset link [7] [7] -> record org unit 14042 as a public routing identifier, not as proof that course, grade, roster, or administrative data is public.

- **Hosted Subdomain Posture**: A public URLScan record maps the hostname to the registered domain `onlinemanipal.com`, records the DNS CNAME `muj.brightspace.com`, and shows an Amazon ASN observation, but also warns that the snapshot is historical and not controlled by URLScan [17] [17] [17] [17] [17] -> the CNAME is strong attribution evidence, but the GeoIP, ASN, scan status, and any apparent absence of hits must not be treated as a current security or availability verdict.

- **Microsoft 365 SSO**: The retrieved public Brightspace login content does not name Microsoft, Microsoft 365, Entra, Azure AD, SAML, or OIDC [7]. D2L documents customer-managed SAML administration and identity-provider registration as a product capability [1] -> the requested Microsoft 365 federation remains unconfirmed; an administrator must verify it from authorized identity-provider configuration and sign-in logs.

- **Version and Patch Posture**: The public evidence reviewed here does not establish the tenant's Brightspace release, patch level, enabled modules, or security configuration -> do not map a historical CVE to this tenant merely because the hostname is Brightspace.

- **Known Brightspace Vulnerability**: NVD records CVE-2021-43129 as a bypass of Brightspace's quiz "Disable Right Click" option, allowing browser print and copy functionality, with no NVD CVSS assessment in the retrieved record [4] [4] -> use it as a configuration and disclosure lesson, not as evidence of unauthorized access to MUJ.

- **Public Complaints**: The complaint evidence located in this review concerns campus SLCM fee visibility and fee-status lag, not Brightspace. One post reports that a fee portal was unavailable to the poster while peers could see it, and another reports a fee payment still shown as pending [14] [14] [14] [16] [16] -> these are useful reliability signals for SLCM/payment workflows but do not establish a Brightspace outage or grade-sync failure.

- **Grades Synchronization**: D2L publicly documents optional IPSIS final-grade export from Brightspace to a SIS, including an export initiated in Brightspace or a SIS pull using IMS LIS v2.0 [9]. MUJ's public SLCM documentation describes attendance, internal and external marks, result publication, and broadcast messages [21] -> a Brightspace-to-SIS/SLCM flow is technically plausible, but no public source reviewed confirms that MUJ has enabled it, which direction it uses, or whether grades actually synchronize.

- **Data Governance and Support**: The MAHE-wide policy describes collection of identity, contact, financial, health, browsing, and server-log data, third-party service sharing, retention, and safeguards [18] [18] [18] [18] [18]. Online Manipal's Help Center says LMS access follows enrollment and fee payment, login details are emailed, and technical issues should go through the Help Center or student portal [2] [2] -> use official support and privacy channels for validation rather than probing production systems.

- **Research Safety**: D2L's disclosure policy requires authorization for testing customer instances, prohibits disruptive testing and unauthorized data access, and says researchers must stop if they encounter sensitive data [6] [6] -> a university club should limit work to passive public evidence unless MUJ and D2L grant written authorization.

## Scope, Method, and Evidence Standard

This report examines public information about the Online Manipal Brightspace service at `learning.onlinemanipal.com`, the public MUJ SLCM ecosystem, and the relationship that can or cannot be established between them. It does not attempt to log in, submit credentials, enumerate authenticated objects, alter parameters, bypass access controls, scrape private records, or test the supplied infrastructure. The target is an evidence-based posture assessment, not a penetration test.

The research brief supplied four SLCM technology descriptors - ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10 behind Akamai, and Microsoft 365 identity. Those descriptors are treated here as leads supplied by the requester, not as independently confirmed findings. A Brightspace cloud tenant and an institutional SLCM portal can have different vendors, hosting boundaries, identity paths, deployment lifecycles, and security owners. The report therefore does not transfer a stack claim from `mujslcm.jaipur.manipal.edu` to `learning.onlinemanipal.com`.

The evidence model has four labels. "Observed" means a public page or record states the fact directly. "Generic capability" means D2L or MAHE documents what a product or policy can support, without proving that MUJ enabled it. "Inference" means a cautious architecture interpretation from multiple observations. "Unknown" means the public record reviewed does not establish the claim. This distinction is essential for SSO, release versions, grade synchronization, and vulnerability exposure.

The report also treats vendor-authored marketing material differently from independent or user-generated evidence. D2L's MUJ case study is valuable for customer attribution and for understanding the intended learning use case, but its outcome percentages are claims presented by the vendor and customer story. Reddit posts are valuable signals of user experience, but they are anecdotes rather than incident tickets, monitoring records, or root-cause analyses. A complaint can justify authorized investigation without proving a defect.

### Auditable reasoning summary, not private chain of thought

The requested `cot_explicit` requirement is addressed through a reproducible reasoning summary rather than hidden internal chain-of-thought. The table below records the observation, the permitted inference, and the decision boundary.

| Reasoning step | Public observation | Permitted inference | Decision boundary |
|---|---|---|---|
| 1. Attribute the LMS | D2L names MUJ Online as a Brightspace customer and the host has a CNAME to `muj.brightspace.com` [5] [17] | The hostname is very likely a D2L Brightspace tenant | Do not infer that every Manipal portal uses the same tenant or backend |
| 2. Separate public routing from public data | The `/d2l/home/14042` route is an indexed login page [7] | 14042 is a public route or org-unit identifier | It does not prove that course objects, grades, or rosters are unauthenticated |
| 3. Evaluate SSO | The visible login evidence shows Username and Forgot your password, while naming no Microsoft or SAML provider [7] | SSO may be hidden, conditional, or absent from the unauthenticated page | Microsoft 365 integration remains unknown |
| 4. Evaluate CVEs | NVD records a Brightspace quiz-control bypass but not a tenant version or exposure [4] [4] [4] | The record is a product-level historical risk | Do not claim MUJ is vulnerable without authorized version and configuration evidence |
| 5. Evaluate data flow | D2L documents generic IPSIS grade export [9]; SLCM documentation lists marks and results [21] | A grade exchange is technically plausible | No public proof of a live MUJ Brightspace-SLCM synchronization |
| 6. Evaluate complaints | Public posts describe SLCM fee visibility and pending-payment symptoms [14] [14] [16] | SLCM/payment reconciliation deserves operational attention | Do not relabel an SLCM complaint as a Brightspace incident |

**Decision-ready insight:** the strongest public conclusion is tenant attribution, not tenant compromise. The report should be used to obtain authorized configuration evidence, not to fill unknowns with assumptions.

## What the Public Record Establishes About MUJ Brightspace

D2L's customer story supplies the clearest public attribution. It says Manipal University Jaipur was addressing a shift toward online education and needed a robust LMS for learners and instructors [5]. It states that MUJ began establishing a digital learning ecosystem in 2020 [5], and identifies D2L Brightspace as the selected solution [5]. The page further presents a customer statement that Brightspace helped MUJ scale from zero to 85,000 students in five years [5]. These claims support a high-confidence conclusion that Online Manipal's learning service is associated with a D2L Brightspace deployment.

The story describes the intended operating model, not just a product name. It says that the LMS needed to work across 2,000 towns and be available anytime and anywhere [5]. It names progress tracking, assignment submission, multimedia delivery, content creation, and interactive learning design as relevant capabilities [5]. Online Manipal's own public site similarly describes a fully online experience covering admission, orientation, classes, projects, examinations, and placement drives, and calls the service an advanced LMS providing e-tutorials, virtual programming labs, case studies, and e-libraries [13].

The two sources are complementary. The D2L page is vendor and customer evidence for the institutional deployment; the Online Manipal page is institutional marketing evidence for the service's educational role. Neither page supplies a security architecture diagram, a federation metadata document, a Brightspace release number, a list of enabled integrations, a data-retention schedule specific to the tenant, or an independent assurance report. The public record establishes what the service is for, not how every control is configured.

The vendor case study reports several outcomes: discussion participation increased by 30 percent, course completion by 15 percent, average academic performance by 10 percent, faculty time savings from automated grading by 30 percent, and administrative workload reduction by 40 percent [5]. These figures should be retained as reported case-study outcomes, not recast as independently audited measurements. They are useful because they identify the business processes likely to matter in a security or availability incident: learner identity, course access, assessment submission, gradebook processing, notifications, and administrative workflows.

### MUJ Brightspace case study: scale without public control evidence

The specific entity is Manipal University Jaipur Online. The decision was to adopt D2L Brightspace while expanding online delivery; the stated outcome was growth from zero to 85,000 students over five years, with reported engagement, completion, performance, grading, and administrative benefits [5] [5]. What this reveals is an important risk concentration: the LMS is not merely a content website. It is positioned as a high-scale learning and assessment service, so identity errors, course-enrollment errors, grade-display errors, or service disruption could affect academic operations.

The same case study also reveals what remains outside the public evidence. Its cited implementation and outcome sections do not disclose the Microsoft tenant, the SAML claims, the source-of-truth system for enrollment, the grade-export schedule, or the tenant's Brightspace release. The absence is not proof that the controls do not exist. It means a security club cannot use the case study as evidence of configuration, patching, or integration.

**Decision-ready insight:** use D2L's case study to prioritize business-impact questions - identity, assessment integrity, grade integrity, and availability - but require administrator evidence before making technical claims.

## Subdomain and Passive Hosting Posture

The public host is a subdomain of `onlinemanipal.com`, not a hostname under `manipal.edu`. URLScan's public record identifies `learning.onlinemanipal.com` and states that the registered domain is `onlinemanipal.com` [17] [17]. It records a DNS CNAME of `muj.brightspace.com` [17]. Combined with D2L's independent customer story, this is strong passive evidence that the host is a MUJ-branded Brightspace tenant or tenant alias. The wording should remain precise: it is evidence of hostname mapping, not proof of the internal account, tenant identifier, or all related services.

URLScan also reports an age of five years for when the hostname or domain was first observed, a Sydney, Australia GeoIP, and AS16509 AMAZON-02 [17]. Those fields are historical observations from URLScan. They are not a current DNS measurement, a service-level agreement, a statement of data residency, or proof that every request is served from the same place. URLScan explicitly warns that the snapshot is live and that it does not host or control the website [17]. It also displays caveats including no direct hits, nothing hosted on the domain, no incoming hits, and nothing talking to the domain [17]. Such UI labels can reflect the scan corpus and observation method; they should not be converted into claims that the service is down, empty, or secure.

The D2L cloud page says AWS is D2L's primary strategic cloud infrastructure provider [12]. This generic vendor statement is consistent with URLScan's Amazon ASN observation, but it does not prove that this particular tenant, data set, or current request path is located in a particular AWS region. The safe conclusion is that the public evidence points to a hosted Brightspace delivery model, with a public CNAME and an Amazon-associated passive observation. The safe non-conclusion is that it does not prove network segmentation, WAF policy, origin protection, TLS settings, or tenant isolation.

The URL also contains the D2L route `/d2l/home/14042`. Search indexing shows a Manipal University Jaipur login page at that route with the text "Welcome to Manipal University Jaipur Centre for Distance and Online Education" and an instruction to log in to view courses and use e-learning features [7]. The extracted public page shows a Username field and a Forgot your password link [7]. These are normal login-surface observations. They do not disclose a course, a grade, a student record, or a bypass.

The supplied brief describes the SLCM host as ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai-fronted, and Microsoft 365-linked. That stack description should not be projected onto Brightspace. The MUJ SLCM page itself only exposes a welcome and sign-in surface in the evidence used here [19], while the older MAHE SLCM page is a separate hostname and likewise does not create a technical equivalence with the D2L host [20]. A hostname, product path, and institutional brand are not enough to merge the two applications.

### Passive posture table

| Surface or observation | Evidence | Confidence | Security meaning |
|---|---|---:|---|
| Brightspace tenant attribution | D2L customer story identifies MUJ Online and Brightspace [5] | High | Vendor relationship is publicly supported |
| Tenant alias | URLScan records CNAME `muj.brightspace.com` [17] | High for the historical record | Strong mapping signal; not a current control assessment |
| Registered domain | URLScan identifies `onlinemanipal.com` [17] | High for the record | Distinguishes Online Manipal branding from the SLCM `manipal.edu` host |
| Hosting observation | URLScan shows Sydney GeoIP and AS16509 AMAZON-02 [17] | Moderate and historical | Consistent with hosted delivery; not data-residency proof |
| Public route | `/d2l/home/14042` is indexed as a MUJ login route [7] | High for the public page | Route visibility does not make authenticated data public |
| Visible login content | Username and password-reset link; no named IdP in the retrieved content [7] | High for the retrieved page | SSO method remains unresolved |
| Akamai attribution for Brightspace | No cited Brightspace evidence establishes Akamai | Unknown | Do not transfer the SLCM premise to the LMS |

**Decision-ready insight:** the public attack surface that can be responsibly described is a branded Brightspace login alias and its passive hosting relationship. No public observation here justifies probing the origin, altering URL parameters, or claiming authenticated-data exposure.

## Microsoft 365 SSO and Identity Boundary

The Microsoft 365 question is the most important unresolved identity issue. The retrieved Brightspace login page exposes a Username field and a Forgot your password link, but the focused extraction names no Microsoft, Microsoft 365, Entra, Azure AD, SAML, or OIDC provider [7]. The indexed page tells a user to log in to view courses, but it does not publish a federation URL, tenant ID, SAML metadata endpoint, or identity-provider logo [7]. This is a negative observation about the public unauthenticated page, not proof that Microsoft federation is absent.

D2L's own SAML documentation explains why the public page may not settle the question. It says that SSO is a customer-managed workflow and that D2L provides an administrative front end to configure, troubleshoot, and maintain it [1]. It also says the guide covers registering an identity provider without engaging D2L Support [1]. This establishes that Brightspace can support customer-managed identity-provider configuration. It does not identify MUJ's identity provider, claim that MUJ uses Microsoft 365, or disclose the claims and groups sent to Brightspace.

The identity boundary should therefore be represented as a set of hypotheses, not a fact. Hypothesis A is that a user reaches a Microsoft Entra or Microsoft 365 sign-in flow after entering a username or choosing an undisplayed sign-in action. Hypothesis B is that the LMS uses a separate local or institution-managed identity service that may be connected to Microsoft accounts elsewhere. Hypothesis C is that the page has conditional or tenant-specific behavior that a public anonymous retrieval cannot see. All three remain possible from the public evidence; none is confirmed.

This distinction matters operationally. If Microsoft 365 is the identity provider, account disablement, multifactor authentication, conditional access, group-to-role mapping, name and email claims, clock tolerance, certificate rotation, and logout behavior become part of the Brightspace trust chain. If it is not, the relevant controls may instead be D2L-managed or handled by another service. These are defensive review questions, not instructions to test the service. The administrator should answer them from authorized Entra enterprise-application settings, D2L SAML administration, provisioning records, and sign-in logs.

### Identity evidence matrix

| Identity question | Public evidence | Status | Authorized verification source |
|---|---|---|---|
| Is the host a Brightspace service? | D2L names MUJ Online as a Brightspace customer [5]; URLScan records `muj.brightspace.com` [17] | Confirmed with high confidence | D2L customer contract or tenant administration |
| Is Microsoft 365 named on the public login page? | Focused extraction shows Username and password-reset link but no Microsoft, Entra, Azure AD, SAML, or OIDC name [7] | Not observed | Authorized page flow and IdP configuration |
| Does Brightspace support SAML IdPs? | D2L says SSO is customer managed and documents identity-provider registration [1] | Generic capability | D2L Brightspace SAML administration |
| Is MUJ using Microsoft Entra? | No tenant-specific public evidence identified in the reviewed corpus | Unknown | MUJ identity administrator and Entra sign-in logs |
| Is there automated provisioning? | No public provisioning configuration or directory mapping was found in the reviewed evidence | Unknown | Authorized provisioning connector or SIS/identity records |
| Are SLCM and Brightspace accounts the same? | Separate public hostnames and login surfaces are observed [19] [7] | Unknown | Authorized account lifecycle documentation |

**Decision-ready insight:** do not write "Microsoft 365 SSO is confirmed." Write "D2L supports customer-managed SAML, but the public MUJ Brightspace page does not identify Microsoft 365; tenant-specific federation is unverified." That wording preserves both the evidence and the uncertainty.

## Brightspace Vulnerability Record and Safe Research Boundary

The principal product-level vulnerability located in the public record is CVE-2021-43129. NVD describes a bypass in the Brightspace quizzing feature's "Disable Right Click" option, allowing a quiz-taker to use browser print and copy functions through the right-click menu even when the option is enabled [4]. The behavior concerns a client-side deterrent and exam-content handling. It is not, on the face of the NVD description, a claim of account takeover, server-side authorization bypass, grade modification, or access to another student's record.

NVD's record does not state an affected version in the extracted evidence; it shows CPE data still loading [4] [4]. It also shows N/A for the CVSS/severity field and says the NVD assessment has not been provided [4]. The record was published on 04/19/2022 and last modified on 06/17/2026 [4]. Those dates describe the CVE record, not the MUJ tenant's deployment date or patch date. NVD's listed references do not prove exposure of `learning.onlinemanipal.com` [4].

This is a useful case study in correlation discipline. The entity is D2L Brightspace; the decision or feature was to offer a browser-side quiz restriction; the reported outcome was that the restriction could be bypassed; and the lesson is that a UI control is not equivalent to a cryptographic or server-side content-protection boundary [4]. The case does not justify trying the behavior against a live MUJ quiz. A responsible club can discuss the limitation conceptually and recommend that course owners use assessment settings and controls appropriate to their threat model.

The D2L disclosure policy is explicit about the research boundary. It says testing customer instances requires authorization from the associated customer [6]. It excludes unauthorized testing of connected services and says active research should be limited to systems and services covered by the policy [6]. It prohibits denial-of-service testing, physical testing, social engineering, and other non-technical vulnerability testing [6]. It also instructs researchers to avoid privacy violations, production disruption, data destruction, and data manipulation, and limits exploit use to what is necessary to confirm a vulnerability without compromising or exfiltrating data, establishing persistence, or pivoting [6].

D2L states that reports can be sent to `incident@d2l.com`, including anonymously, and asks researchers to notify it promptly and provide reasonable remediation time before disclosure [6] [6] [6]. It says that, when contact details are provided, it will acknowledge receipt within three business days and aims to maintain an open dialogue [6] [6]. Those instructions are appropriate for a club only when the club has a genuine report and follows the scope. They are not permission to test the MUJ customer instance.

### Vulnerability relevance table

| Record or issue | What the source states | Relevance to MUJ Brightspace | Safe conclusion |
|---|---|---|---|
| CVE-2021-43129 | Quiz "Disable Right Click" can be bypassed for browser print/copy [4] | Product-level historical issue; tenant version and configuration unknown | Do not claim exposure or reproduce it on production |
| NVD severity | CVSS is N/A and NVD assessment not provided [4] | No authoritative NVD severity to import into a tenant risk score | Treat impact as context-dependent |
| NVD version mapping | Affected version is not stated in the extracted record [4] [4] | Cannot compare with MUJ release | Obtain authorized release and advisory data |
| Customer-instance testing | D2L requires associated-customer authorization [6] | Directly applies to a university customer tenant | Passive OSINT only unless written permission exists |
| Data handling during research | Stop and notify D2L if a vulnerability or sensitive data is encountered [6] | Protects students and the institution | Do not copy, retain, or disclose data |

**Decision-ready insight:** the vulnerability finding is a lesson about control design and disclosure, not a finding against MUJ. The highest-value next step is an authorized vendor and tenant advisory review, not public exploit reproduction.

## Public Student Complaints and Reliability Signals

The strongest complaint evidence located concerns SLCM rather than Brightspace. A public Reddit post titled "Fees not showing in slcm" is marked "2mo ago" and reports that the poster could not view the fee portal in SLCM 1.0 despite having the required credits, while peers could see it [14] [14] [14]. The extracted post includes a later request for an update, but no stated resolution [14]. The platform named in the evidence is SLCM; Brightspace and Online Manipal's D2L host are not named [14] [14].

A second public post titled "Paid my Fees But Still Showing as Pending on SLCM" is marked "1y ago" [16] [16]. It reports that payment had been deducted but the fee status remained pending and that a receipt existed [16]. The post asks whether to contact accounts or finance or wait, and the extracted content states no resolution [16] [16]. Again, the named platform is SLCM, not Brightspace.

These cases are not evidence of a security incident. They are evidence of perceived state inconsistency in a student-facing business process. The symptoms could arise from payment reconciliation, delayed status propagation, account association, UI caching, a permissions issue, or an ordinary support backlog. The public posts do not identify a root cause. They also do not show that a grade was altered, that another user's data was accessible, or that the Brightspace tenant was unavailable.

They are nevertheless relevant to the LMS-SLCM question because the official Help Center says students receive LMS access after completing enrollment and fee payment and receive login details by email [2]. That creates a business dependency between payment/enrollment status and LMS access, even though the public evidence does not reveal the API, queue, batch job, or source-of-truth database. If a payment state is stale in SLCM, a downstream access or enrollment state could potentially be delayed. That sentence is an inference about a possible dependency, not a claim that the reported posters were affected in Brightspace.

Online Manipal's official notices describe the LMS as the portal for video tutorials, live interactive classes, recorded sessions, discussion forums, quizzes, and exams [3]. D2L's case study describes assignment submission, progress tracking, multimedia content, and notifications [5] [5]. These functions explain why an access or synchronization issue would matter academically, but they do not convert a fee complaint into a grade-sync incident.

### Complaint evidence table

| Public report | Platform named | Reported symptom | Resolution stated | What it can support |
|---|---|---|---|---|
| "Fees not showing in slcm"; 2mo ago [14] [14] | SLCM | Fee portal not visible to the poster while peers could see it [14] | No; later comment asks for an update [14] | A user-reported availability or entitlement symptom in SLCM |
| "Paid my Fees But Still Showing as Pending on SLCM"; 1y ago [16] [16] | SLCM | Payment deducted but status still pending; receipt mentioned [16] | No; asks whether to contact finance or wait [16] [16] | A user-reported payment-reconciliation or status-lag symptom |
| Public Brightspace-specific complaint in reviewed evidence | Not established | No complaint in the cited records names `learning.onlinemanipal.com` or Brightspace | Not applicable | Do not claim a Brightspace incident from these SLCM posts |

**Decision-ready insight:** route these reports to SLCM/payment and student-support owners first. Correlate them with Brightspace only through authorized timestamps, enrollment records, and audit logs; do not infer a D2L defect from a public SLCM symptom.

## LMS-SLCM Data Flows and the Grades-Sync Question

The public evidence supports two separate facts. First, MUJ's SLCM documentation describes a student-life-cycle suite with attendance, internal marks, external marks, result publication, broadcast messages, and a single-window experience for students and parents [21]. Second, D2L documents a Brightspace capability called IPSIS Grades Export. The D2L page says it is an add-on to the Grades tool, enables final-grade export to a SIS supporting IMS LIS v2.0, and can be initiated from Brightspace or pulled by a process initiated from the SIS [9].

Those facts establish a plausible integration pattern but not a live MUJ data flow. A generic D2L higher-education page says integrating Brightspace with a SIS can share information such as classes taken and grades achieved across two systems [11]. The wording is product-level and promotional. It does not name MUJ's SIS, identify SLCM as that SIS, state that the Online Manipal tenant uses IPSIS, or say whether the flow is real-time, scheduled, manual, one-way, or bidirectional.

The official Online Manipal Help Center adds a different dependency. It says LMS access follows enrollment and fee payment, login details are shared by email, and technical support is available through the Help Center or student portal [2] [2]. This supports an enrollment-to-access business sequence. It does not say that SLCM performs provisioning, that Brightspace calls SLCM, or that Microsoft 365 is the provisioning authority.

A cautious architecture model therefore has three evidence layers. The confirmed SLCM layer contains attendance, marks, results, and broadcast functions [21]. The confirmed Brightspace layer contains online learning, assignments, progress, multimedia, discussions, quizzes, exams, and reported grading automation [3] [5] [5]. The generic integration layer contains D2L's optional final-grade export capability [9]. The missing bridge is tenant-specific evidence linking the second layer to the first.

### Data-flow matrix

| Candidate flow | Public evidence | Direction supported by public evidence | MUJ status |
|---|---|---|---|
| Enrollment and fee completion to LMS access | Help Center says LMS access follows enrollment and fee payment and login details are emailed [2] | Business sequence only; technical transport not stated | Confirmed as a support/process statement; implementation unknown |
| Brightspace learning content to learner | Online Manipal lists tutorials, classes, recordings, forums, quizzes, and exams [3] | LMS to learner | Confirmed at functional level |
| Brightspace assignments and progress to instructor/admin views | D2L customer story names assignment submission, progress tracking, and performance metrics [5] [5] | LMS to authorized institutional users | Confirmed as described capability/use case; exact tenant configuration unknown |
| Brightspace final grades to a SIS | IPSIS Grades Export supports final-grade export and SIS-initiated pull using IMS LIS v2.0 [9] | Brightspace to SIS, or SIS pull from Brightspace | Generic D2L capability |
| SIS/SLCM to Brightspace enrollment | Generic higher-ed page mentions classes and grades across systems [11] | Not enough detail to establish enrollment direction | Unknown for MUJ |
| SLCM attendance/marks/results to students | SLCM documentation lists attendance, marks, results, and broadcast messages [21] | SLCM to student/parent-facing portal | Confirmed at functional level |
| SLCM to Brightspace gradebook or Brightspace to SLCM results | No cited MUJ document identifies a connector, job, endpoint, or mapping | Direction and cadence not established | Unknown |
| Payment status to SLCM | Public complaints report fee visibility and pending-status symptoms [14] [14] [16] | User-visible status relationship only | Symptom reported; backend flow unknown |

The direct answer to "grades sync?" is therefore: **not publicly confirmed**. The evidence supports that D2L has a grade-export mechanism and that MUJ SLCM handles marks and results. It does not support the stronger statement that grades are synchronized between `learning.onlinemanipal.com` and `mujslcm.jaipur.manipal.edu`, nor does it identify which system is authoritative. That distinction matters. A learner may see assignment grades in Brightspace, final results in SLCM, or both, without the public record revealing whether the values are copied, recalculated, manually approved, or independently entered.

### Inferred flow to test only with authorization

The following is an inference, not a public finding: enrollment or payment completion may be consumed by an institutional service; a user may then be provisioned or enabled in Brightspace; learning activity and assessment results may remain in Brightspace; and final grades may be exported or pulled into a student-record platform such as SLCM. Each arrow in that model needs an owner, an interface, an identifier mapping, a schedule, an error queue, and an audit trail. None of those implementation details is established by the cited public evidence.

An authorized review should ask for data-flow diagrams, interface-control documents, IPSIS configuration, SAML claims, provisioning mappings, grade schemas, reconciliation reports, failed-job alerts, and a documented source of truth for final results. It should use test identities and synthetic grades in a non-production environment. It should not attempt to discover these mechanisms by changing identifiers or submitting live data.

**Decision-ready insight:** classify grades synchronization as an unverified integration risk, not as a confirmed feature or confirmed failure. The immediate control objective is reconciliation: prove which system owns enrollment, assessment grades, final results, and publication status.

## Privacy, Governance, and Support Channels

The MAHE privacy policy is the broadest public governance source located. It says the policy explains how MAHE gathers, defines, uses, stores, and processes personal data provided through its websites and services, and applies to students, parents, visitors, and others who provide data [18] [18]. It lists examples including names, contact details, postal addresses, email addresses, gender, age, date of birth, usernames, and passwords, and says health and financial information may be processed in relevant circumstances [18].

The policy also says automatic collection may include IP address, browser and operating-system details, pages and links visited, advertisements viewed, bandwidth speed, installed-software information, and standard server-log information [18]. It describes purposes including enrollment, service provision, customized content, recommendations, statements, payment reminders, communications, statistics and research, service improvement, enquiries and complaints, security, and fraud prevention [18]. For an LMS assessment, those categories suggest that identity, usage, academic-service, and payment workflows should be considered together in a privacy review.

The policy says MAHE does not sell or trade personal data, but may share it with third parties that assist with business operations, website operation, or servicing, subject to confidentiality [18]. It further describes service providers supporting maintenance, analysis, audit, marketing, and development, with limited access and confidentiality obligations [18]. It says users can make certain privacy choices and lists rights for EU GDPR data subjects, including access, correction, erasure, restriction, portability, objection, and limits on automated decision-making; it gives `privacy.mahe@manipal.edu` for requests [18].

The policy states that data is retained only as long as necessary for collection purposes and legal, accounting, or reporting requirements, after which MAHE says it will securely destroy data under internal policy. It also describes physical and technical safeguards, including secure socket layers, firewalls, encryption, reviews, and physical security measures [18]. These are policy statements, not an independent audit of the Brightspace tenant. The evidence does not establish Brightspace-specific retention, D2L contractual roles, regional storage, grade data export scope, or Microsoft 365 processing.

Support evidence is clearer and more operational. The Help Center says it provides support from admission to enrollment and beyond [2]. For MUJ enrolled learners it lists `helpdesk@mujonline.edu.in` and `+91-7996 600 444` [2]. It directs users with technical issues to the Help Center section or student portal [2]. The Online Manipal notices page includes a student-help contact form but the extracted content does not provide a dated maintenance notice or a specific incident explanation [3].

MAHE also publishes a grievance page that describes a Grievance Redressal Committee and Ombudsman and links to a student grievance system [22]. The general MAHE student portal page separately tells users to register and log in for everyday student web services [10]. These sources should not be treated as substitutes for an LMS incident response process, but they provide legitimate channels for students to report access, payment, or grade-display problems without resorting to public probing.

### Governance evidence table

| Governance area | Public statement | Limitation |
|---|---|---|
| Privacy scope | MAHE policy covers personal data used through MAHE websites and services and applies to students and other data subjects [18] [18] | Not Brightspace-tenant-specific |
| Data categories | Identity, contact, account, health, financial, browsing, and server-log categories are described [18] | Does not map fields to SLCM or Brightspace interfaces |
| Third parties | Sharing with service providers is described subject to confidentiality and limited access [18] [18] | Does not name D2L, Microsoft, or an integration contract in the cited excerpts |
| Retention and safeguards | Retention, secure destruction, SSL, firewalls, encryption, reviews, and physical security are described [18] | Policy statement, not independent assurance evidence |
| MUJ technical support | Help Center gives MUJ helpdesk details and routes technical issues to support [2] [2] | Support contact does not reveal root cause or data flow |
| Grievance path | MAHE publishes grievance and Ombudsman information [22] | A grievance channel is not a security testing authorization |
| D2L vulnerability reporting | D2L accepts reports at `incident@d2l.com` and permits anonymous reporting [6] | Scope and authorization rules still apply |

**Decision-ready insight:** privacy and support statements are sufficient to define responsible escalation channels, but insufficient to prove Brightspace-specific data handling. The institution should publish or provide an authorized data-flow and controller/processor summary for the LMS and SLCM.

## Risk Register and Defensive Work Program

The public evidence supports a risk register focused on uncertainty and dependency rather than speculative exploitation. The highest-confidence finding is that MUJ Online uses or used a D2L Brightspace tenant. The highest-impact unknowns are identity federation, provisioning, patch status, and grade authority. The complaint evidence adds an operational signal around payment and SLCM state reconciliation. The historical CVE adds a product-control lesson, but not a tenant finding.

| Risk or question | Evidence basis | Confidence in finding | Potential impact | Defensive action requiring authorization |
|---|---|---:|---|---|
| Tenant identity and ownership | D2L customer story plus `muj.brightspace.com` CNAME [5] [17] | High | Misrouting of reports or incorrect system ownership | Maintain an asset register with D2L, MUJ, and support owners |
| Microsoft 365 federation unknown | Public login content does not name an IdP; D2L says SAML is customer managed [7] [1] | Low confidence about configuration | Account lifecycle, MFA, role-mapping, and logout failures may cross systems | Review authorized SAML/Entra settings, claims, certificate expiry, and sign-in logs |
| Brightspace release unknown | NVD record lacks an affected version and public page does not disclose tenant release [4] [4] | High confidence that version is unknown | Cannot accurately assess advisories or patch exposure | Request current release and security-advisory status from D2L/MUJ |
| Browser-side quiz control | CVE-2021-43129 describes right-click print/copy bypass [4] | High for product record; low for MUJ applicability | Assessment-content copying or weak deterrence | Review assessment policy and approved configuration in a test course |
| Enrollment-to-LMS dependency | Help Center links LMS access to enrollment and fee payment [2] | Moderate | Delayed access after payment or enrollment changes | Reconcile payment, enrollment, provisioning, and support timestamps |
| Grades authority and export | SLCM handles marks/results; IPSIS can export final grades generically [21] [9] | High that the question is unresolved | Wrong, stale, duplicated, or unreconciled academic results | Document source of truth, mapping, approvals, error handling, and audit trails |
| SLCM payment-state reliability | Two public posts report missing or pending fee states [14] [14] [16] | Moderate as user-reported signal | Students may lose access or require manual intervention | Monitor reconciliation and publish incident status through support |
| Privacy mapping gap | MAHE policy is broad and does not establish Brightspace-specific controls [18] [18] | High that public mapping is incomplete | Unclear roles, retention, sharing, and data-subject handling | Provide an authorized system/data inventory and processing map |
| Unauthorized research risk | D2L requires customer authorization and prohibits disruptive or data-access activity [6] | High | Student privacy, service disruption, legal and disciplinary exposure | Use passive OSINT, written scope, synthetic accounts, and responsible disclosure |

A defensible club work program has three phases. Phase one is passive documentation: preserve public URLs, timestamps, page titles, D2L statements, URLScan caveats, and complaint excerpts without collecting personal identifiers. Phase two is owner-led validation: ask MUJ for the tenant owner, identity architecture, current release, privacy contact, grade-system source of truth, and incident escalation path. Phase three, only if written authorization exists, is controlled validation in a non-production environment using synthetic accounts and pre-agreed test cases.

The verification questions should be narrow. For identity, ask whether Microsoft Entra is the IdP, whether SAML or another protocol is used, which claims map to the Brightspace username, how deprovisioning works, and whether MFA is enforced upstream. For enrollment, ask which system creates or disables Brightspace users and courses, what happens after fee reversal, and how failures are reconciled. For grades, ask whether IPSIS is enabled, whether final grades are exported or pulled, whether SLCM is the receiving SIS, how human approval works, and which system publishes the official result.

For privacy, ask which organization is the controller for each data class, which D2L and Microsoft services receive identifiers or learning telemetry, how long activity and assessment records are retained, and how access or correction requests are handled. For availability, ask for historical incidents and maintenance communication, not for a public stress test. For security, request D2L advisories and customer confirmation rather than relying on generic CVE searches.

**Decision-ready insight:** convert uncertainty into owner-assigned questions. A written answer from the system owner about IdP, release, provisioning, grade authority, and retention would reduce risk more effectively than additional unauthorised scanning.

## Comparative Analysis: Brightspace, SLCM, and the Integration Boundary

The three major elements have different evidence bases and different roles. Brightspace is supported by a D2L customer story, a Brightspace-branded CNAME, and an indexed login route [5] [17] [7]. SLCM is supported by Manipal portal surfaces and an official ICT-tools description listing attendance, internal and external marks, result publication, and broadcast messages [19] [21]. The integration boundary is supported only by generic D2L capabilities and an Online Manipal process statement linking LMS access to enrollment and fee payment [9] [2].

The mechanism differs across the systems. Brightspace is the learning-delivery and assessment environment described by D2L and Online Manipal, with content, activities, progress, notifications, and grading workflows [5] [5]. SLCM is the student-life-cycle surface described as holding attendance, marks, results, and broadcasts [21]. A possible integration would move identity, enrollment, or final-grade data across a boundary, but the public record does not identify the mechanism. That uncertainty is the central finding.

Scope also differs. A Brightspace login route can reveal a product and organizational label without revealing a course or grade. An SLCM portal can expose a separate student-facing workflow without proving that its database is the Brightspace SIS. The two platforms may share institutional identifiers, but the public pages do not establish whether they share usernames, unique student IDs, APIs, queues, or administrators. Treating the brand as the integration is a category error.

The trade-offs differ as well. Brightspace's vendor-hosted model may reduce the institution's direct responsibility for underlying infrastructure, while increasing the importance of vendor configuration, customer-managed SSO, data-processing terms, and release coordination. SLCM's direct role in marks, results, fees, or attendance may make reconciliation and support more visible to students, as suggested by the public complaints. A bridge between them can reduce duplicate entry, which D2L markets as a benefit of SIS integration [11], but it can also create synchronization, mapping, and failure-recovery dependencies.

### Comparative table

| Dimension | Brightspace tenant | MUJ SLCM | Integration boundary |
|---|---|---|---|
| Public identity | D2L customer story and Brightspace CNAME [5] [17] | MUJ portal welcome/sign-in surface [19] | No public document identifies a connector |
| Primary public role | Online learning, activities, progress, notifications, assessments [3] [5] | Attendance, marks, results, broadcasts, student/parent window [21] | Generic IPSIS final-grade export is documented [9] |
| Identity evidence | Username and reset link visible; IdP not named [7] | Sign-in surface visible; federation not established [19] | Microsoft 365 relationship unknown |
| Data authority | Gradebook and learning activity are described, but official-result authority is not stated [5] | Marks and results are listed as SLCM functions [21] | Source of truth and reconciliation are unknown |
| Evidence time horizon | D2L case study describes adoption and reported outcomes [5] | Official ICT description and current public portal surfaces | Current connector status is not publicly documented |
| Main trade-off | Hosted scale and centralized product capability versus customer configuration dependence | Student-lifecycle visibility versus fee/status reconciliation concerns | Reduced duplicate entry may create mapping and failure dependencies |

The non-obvious tension is that the public record is strongest about scale and weakest about the controls that make scale trustworthy. D2L reports rapid growth and improved operational outcomes [5] [5], while the public SLCM complaints show that students can still experience inconsistent fee-state visibility [14] [14] [16]. These facts do not contradict each other because they concern different systems and different evidence types. They do show why a high-level success story cannot substitute for end-to-end reconciliation evidence.

A second tension is between product capability and tenant configuration. D2L supports SAML administration and IPSIS grade export [1] [9], but capability does not prove activation. A third is between a visible login route and a hidden trust boundary: students can be directed to a public Brightspace route [7] without the public page revealing whether authentication is local, federated, or conditional [7].

**Decision-ready insight:** the correct architecture label is "Brightspace tenant plus separate SLCM portal, with integration unverified." That label is more useful and more defensible than declaring a grade sync or Microsoft federation from product documentation alone.

## VERDICT

**Overall confidence: Moderate-high for Brightspace attribution and public functional role; low-to-moderate for identity and integration conclusions.**

The public evidence supports the following verdict. `learning.onlinemanipal.com` is very likely a Manipal University Jaipur Online D2L Brightspace tenant. D2L's own customer story identifies MUJ Online as a Brightspace customer, describes the 2020 digital-learning initiative, and reports growth and learning-workflow outcomes [5] [5] [5]. URLScan's historical record adds a CNAME to `muj.brightspace.com` [17]. The route `/d2l/home/14042` is publicly indexed as a MUJ login route [7].

The public evidence does **not** confirm Microsoft 365 or Microsoft Entra SSO for this tenant. The visible login evidence names no such provider [7], while D2L's SAML page establishes only that customer-managed identity-provider configuration exists as a product capability [1]. The supplied Microsoft 365 description should remain an unverified lead until MUJ or an authorized identity administrator confirms it.

The public evidence does **not** confirm that Brightspace grades synchronize with MUJ SLCM. D2L documents generic IPSIS final-grade export [9], and Manipal's SLCM documentation lists marks and results [21]. That combination makes a bridge technically plausible, but no reviewed public source identifies the connector, direction, schedule, identifier mapping, error handling, or source of truth. The answer to "grades sync?" is therefore **unknown, not publicly confirmed**.

The public complaints found are SLCM-specific and concern fee visibility or pending payment state [14] [14] [16]. They should be treated as reliability and support signals, not as evidence of a Brightspace vulnerability, data breach, or grade-integrity failure. The one historical Brightspace CVE located concerns a quiz right-click restriction bypass and carries no NVD severity assessment in the retrieved record [4] [4]. It does not establish exposure of MUJ.

For the university security club, the recommended disposition is **passive OSINT complete; tenant configuration validation pending authorization**. The club should preserve the public evidence, request written answers from MUJ and D2L, use synthetic identities in any approved test environment, and report genuine D2L issues through the vendor's disclosure process. It should not attempt authentication, exploit reproduction, parameter tampering, enumeration, denial of service, or retrieval of student data. D2L's policy requires customer authorization and prohibits disruptive testing, data access, persistence, and pivoting [6].

## References

1. *SAML Administration Overview - Brightspace*. https://community.d2l.com/brightspace/kb/articles/4843-saml-administration-overview
2. *Help Center - Get Answers to All Your Queries | Online Manipal*. http://mahe.onlinemanipal.com/help-center
3. *Online Manipal | UGC Entitled Online UG & PG Degree Courses*. http://muj.onlinemanipal.com/notifications
4. *NVD - CVE-2021-43129*. https://nvd.nist.gov/vuln/detail/CVE-2021-43129
5. *Manipal University Jaipur (Online) | D2L*. https://www.d2l.com/en-in/why-d2l/customers/manipal-university-jaipur-online
6. *D2L Vulnerability Disclosure Policy - Brightspace*. https://community.d2l.com/brightspace/kb/articles/23533-d2l-vulnerability-disclosure-policy
7. *Login - Manipal University Jaipur*. https://learning.onlinemanipal.com/d2l/home/14042
8. *Brightspace End User License Agreement*. https://www.d2l.com/legal/brightspace-eula
9. *Overview of Grades and IPSIS - Brightspace - community.d2l.com*. https://community.d2l.com/brightspace/kb/articles/23729-overview-of-grades-and-ipsis
10. *Student Portal Login- MAHE (Manipal Academy Of Higher ...*. http://manipal.edu/mu/academics/student-portal.html
11. *D2L Brightspace and SIS Integrations for Higher Education*. https://www.d2l.com/solutions/higher-education/d2l-brightspace-and-sis-integrations-for-higher-education/
12. *Brightspace Cloud Based Learning Platform*. https://www.d2l.com/cloud
13. *Online Bachelor and Master Programmes | Online Degree Programs in India | Online Manipal*. https://muj.onlinemanipal.com/
14. *Fees not showing in slcm : r/Manipal_Academics*. https://www.reddit.com/r/Manipal_Academics/comments/1u8476b/slcm_portal_issue
15. *Reddit - The heart of the internet*. https://www.reddit.com/r/Manipal_Academics/comments/1993mdc/slcm_login
16. *Reddit - The heart of the internet*. https://www.reddit.com/r/Manipal_Academics/comments/1lzf0ht/paid_my_fees_but_still_showing_as_pending_on_slcm
17. *learning.onlinemanipal.com - urlscan.io*. https://urlscan.io/domain/learning.onlinemanipal.com
18. *Privacy & Cookie Policy | MAHE*. http://manipal.edu/mu/important-links/privacy-and-cookie-policy.html
19. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
20. [
	MU SLcM
](https://slcm.manipal.edu/)
21. *http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf*. http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf
22. *http://manipal.edu/mu/about-us/grievances.html*. http://manipal.edu/mu/about-us/grievances.html
