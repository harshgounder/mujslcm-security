# MIT Manipal Signals for Defending MUJ SLCM

## Executive Summary

- **Shared Academic Core**: MAHE's own ICT report describes SLCM as the replacement for its older Academic Management System and as a single-window suite for attendance, internal marks, external marks, results, circulars, students, and parents [7]. This is the strongest evidence that MIT Manipal experience is relevant to MUJ, but it does not prove that the two deployments share code, databases, configurations, administrators, or vulnerabilities. Treat MIT findings as test hypotheses, never as confirmed MUJ defects.

- **Multiple Front Doors**: MAHE's official student-portal page points users to `sis.manipal.edu`, while the separate `slcm.manipal.edu` site is branded as MAHE SLCM [2][1]. The distinction matters: a security review must inventory redirects, identity handoffs, session boundaries, student and parent roles, and older compatibility paths rather than treating "SLCM" as one URL.

- **Broad Identity and Learning Ecosystem**: MAHE documents institution-wide Microsoft Office 365 access for faculty and students, Microsoft Teams, Brightspace, Impartus, Coursera, SWAYAM, and NPTEL; it also records department-specific use of Moodle and EduNxt [7]. MUJ risk therefore cannot be reduced to one ASP.NET login page. Account lifecycle, password recovery, session revocation, and data sharing across connected services deserve equal attention.

- **Automation Is Demonstrably Attractive**: Public repositories target marks, attendance, admission-profile details, CGPA, timetable data, and credential validation. One 2020 API was deprecated after SLCM introduced CAPTCHA, while a 2025 project states that it automates digit-based CAPTCHA handling [22][4]. This does not establish a vulnerability, but it is direct evidence of sustained demand for unofficial automation.

- **Third-Party Credential Risk Is More Concrete Than a Published Exploit**: A 2025 MUJ-oriented Flutter/FastAPI app advertises custom email/password authentication and automatic retrieval of grades and attendance, but its repository states no explicit privacy policy or credential-storage rule [21]. The defensible response is to provide a sanctioned, scoped integration model or explicitly prohibit credential delegation, not to assume every independent project is malicious.

- **No Verified Manipal Vulnerability Disclosure Was Found**: Targeted searches for Manipal SLCM vulnerabilities, data exposure, incidents, bug-bounty records, and researcher disclosures did not produce a report attributable to the MAHE/MIT or MUJ student systems. This is a bounded OSINT result, not proof that no security issue has ever existed.

- **The Supplied Stack Needs Qualification**: The public login page supports an ASP.NET MVC-style inference because its HTML contains unobtrusive validation and an anti-forgery field, but public evidence did not verify "ASP.NET MVC 5.3." The Microsoft package located publicly is `Microsoft.AspNet.Mvc 5.2.9`, while Microsoft's support policy distinguishes Framework-bundled components from separately shipped packages [33][12]. Version 5.3 should therefore remain unverified until MUJ supplies an internal software bill of materials.

- **Priority Is Control Validation, Not Exploitation**: Microsoft recommends blocking legacy authentication because its analysis associates more than 97 percent of credential-stuffing attacks and more than 99 percent of password-spray attacks with legacy authentication; Microsoft also recommends beginning Conditional Access changes in Report-only mode [9]. The club should propose owner-run tests of MFA coverage, role isolation, session revocation, recovery workflows, logging, and origin restriction, without attempting them against production itself.

**Decision-ready insight:** the public record supports a **medium-high confidence defensive relationship** between MIT/MAHE SLCM experience and MUJ SLCM. It does **not** support claiming a shared vulnerability, a current breach, or an exact MVC 5.3 component.

## 1. Scope, Ethics, and Auditable Reasoning

This report uses only public pages, public documentation, indexed login pages, and public GitHub repositories. It does not log in, submit credentials, enumerate accounts, solve a live CAPTCHA, test authorization, scan ports, attempt origin bypass, or reproduce request formats and bypass instructions. Any active validation described below is a recommendation for MUJ's authorized security personnel in a controlled environment.

I cannot provide hidden chain-of-thought or private deliberative reasoning. Instead, the following evidence ledger exposes the decision logic at a level another analyst can audit.

| Evidence class | Meaning in this report | Example | Allowed conclusion |
|---|---|---|---|
| Confirmed public fact | Directly stated by an official page or repository | MAHE says SLCM covers attendance, marks, results, and messages [7] | The named function exists in the documented MAHE system |
| Passive page observation | Visible in public HTML without interaction | MUJ presents separate student and parent login choices [3] | Role separation is part of the public interface |
| Repository claim | What a project says it does, not independently executed | `slcmAPI` says it retrieves marks, attendance, and profile data [22] | Developers intended those data flows |
| Analyst inference | A hypothesis derived from evidence and explicitly labeled | Parent and student roles may create authorization-boundary risk | MUJ should test the boundary under authorization |
| Not established | Evidence was missing, ambiguous, or contradicted | Maintainers' MIT Manipal student status | Do not describe them as MIT students |

MAHE's information-security policy supplies an institutional baseline. It commits to confidentiality, integrity, and availability, periodic risk assessment, need-to-know and need-to-perform access, and investigation of compliance violations [8]. The public policy does not state a vulnerability-disclosure address, detailed authentication standard, logging standard, or third-party application rule. That gap does not mean those controls are absent internally; it means they are not established by the public policy reviewed here.

The report also distinguishes MAHE from MUJ. MIT Manipal is presented on an official MAHE-domain page as an engineering institution offering bachelor's, master's, and research programs [24]. MUJ has its own portal, branding, email suffixes, and operational context. Shared naming and business functions increase transferability of **test cases**, but only direct technical evidence can establish shared implementation.

**Section insight:** use this report to prioritize an authorized assessment and policy review. Do not use it as a finding notice, vulnerability claim, or permission to test a live service.

## 2. MIT Manipal and MAHE Student-System Map

The official architecture visible to a student is layered. MAHE's public student-portal page routes to `sis.manipal.edu` [2]. The SIS page describes itself as meeting information needs of students and parents and limits services to bona fide members of MAHE [20]. A separate SIS payment page directs eligible students and parents to enter through SIS and use "Fee Kart" for academic-fee payment [10]. Meanwhile, `slcm.manipal.edu` carries MAHE SLCM branding [1].

The strongest functional description comes from MAHE's ICT-tools report. It says SLCM replaced an older Academic Management System and includes attendance, internal and external marks, result publication, and broadcast messages. It calls SLCM a single-window academic system for students and parents [7]. That functional scope explains why unofficial clients concentrate on marks, attendance, profiles, and schedules.

### Exact system inventory

| System or service | Exact public URL | Publicly documented purpose | MIT relevance | Confidence and limitation |
|---|---|---|---|---|
| MAHE Student Portal | https://www.manipal.edu/mu/academics/student-portal.html | Official landing page links to SIS [2] | Strong, because MIT is within the MAHE web estate | High for link; no authentication-flow details |
| MAHE SIS | https://sis.manipal.edu/ | Student and parent information services for bona fide MAHE users [20] | Strong inference for MIT students | High for purpose; deployment internals unknown |
| MAHE SLCM | https://slcm.manipal.edu/ | MAHE-branded SLCM endpoint [1] | Strong family relevance | High for existence; code relationship to MUJ unknown |
| SLCM functional suite | http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf | Attendance, marks, results, circulars, student/parent academic window [7] | Directly relevant to MIT/MAHE workflows | High for documented scope |
| Microsoft Teams | Same official MAHE ICT report | Meetings, teaching, chat, conferencing, file storage, and application integration [7] | MAHE-wide evidence, not MIT-exclusive | High for MAHE; medium for every MIT unit |
| Office 365 | Same official MAHE ICT report | Subscription extended to all faculty and students [7] | Strong identity and lifecycle relevance | High for MAHE availability |
| Brightspace | Same official MAHE ICT report | Licensed LMS supporting personalized learning and collaboration [7] | Adjacent service, not proven MIT default | Medium |
| Impartus | Same official MAHE ICT report | Lecture recording and repository for presentations, notes, and quizzes [7] | Plausibly available to MIT classrooms | Medium because use is described MAHE-wide |
| Coursera, SWAYAM, NPTEL | Same official MAHE ICT report | External course and learning resources [7] | Account/data-sharing context | High for MAHE program; per-user integration unknown |
| Moodle and EduNxt | Same official MAHE ICT report | Department-specific LMS use [7] | Do not generalize to MIT | High for named departments, low for MIT |
| MAHE Library Portal | https://libportal.manipal.edu/ | MAHE library entry point maintained by Digital and Information Technology [34] | Adjacent authenticated resource | High for existence; SSO relationship unknown |
| MIT Examly administration | https://admin.mit659.examly.io/login | Publicly indexed MIT-branded admin/staff login [6] | Potential MIT assessment platform | Medium-low; official ownership and current use not independently established |
| MUJ SLCM | https://mujslcm.jaipur.manipal.edu/ | Public MUJ portal with student and parent entry choices [3] | Target system | High for public interface |

Two cautions follow from this table. First, "used by MAHE" is not synonymous with "used in every MIT course." The official report itself limits Moodle and EduNxt statements to named schools or departments [7]. Second, different front doors can converge on shared identity or student records without sharing sessions or application code. That distinction must be tested internally rather than inferred from branding.

**Section insight:** the defensible MIT-to-MUJ transfer unit is the **business workflow** - attendance, marks, results, messaging, parent access, and identity lifecycle - not an assumed common codebase.

## 3. Public Developer Artifacts: What They Show and What They Do Not

No search result established that the maintainers below were MIT Manipal students. Their public profiles either omit affiliation or mention only project relationships. The artifacts are therefore described as public Manipal-targeting developer projects, not as verified student security writeups [29][31][30][32]. This is an important correction to the requested premise.

### Exact artifact table

| Artifact | Date and stated purpose | Data or behavior claimed | Security-relevant observation | Attribution limit |
|---|---|---|---|---|
| `canaryGrapher/slcmAPI` | Created 2020-05-22; open REST API for Manipal SLCM [22] | Marks, attendance, admission-profile details, and credential checking [22] | Deprecated after CAPTCHA appeared [22] | Profile does not state MIT/MAHE/MUJ affiliation [32] |
| `nikeplusdash/SLCM-api` | Created 2020-05-31; API for `slcm.manipal.edu` [5] | Login plus basic user-data retrieval [5] | Repository says it does not store user data and advises session logout [5] | Profile does not state institutional affiliation [30] |
| `sankalp2004/SLCM-is-Dumb` | Created 2025-06-17; CGPA scraper [4] | Selenium/OCR workflow and multiple CGPA extraction approaches [4] | States that it automates digit-based CAPTCHA handling [4] | Profile contains an MIT Bengaluru project reference, not a verified MIT Manipal affiliation [31] |
| `DK10WS/SLCM_APP` | Created 2025-06-18; app version for MUJ SLCM [21] | Attendance, grades, GPA/CGPA, timetable, student and parent login [21] | Flutter frontend, FastAPI backend, custom email/password logic; no explicit repository privacy or credential-storage rule [21] | Profile does not state MUJ or MIT affiliation [29] |
| MUJStella | Public independent student platform | Public landing page describes an installable student platform | Explicitly says it is independent and not affiliated with MUJ [23] | It should not be mistaken for an official university service |

### Case study 1: CAPTCHA changed the integration, not the demand

`canaryGrapher/slcmAPI` records a progression from marks to attendance, profile details, and credential validation. It later marks itself deprecated because CAPTCHA was introduced [22]. The mechanism is straightforward: adding an anti-automation step increased friction for an unofficial client, but the underlying demand for programmatic access remained.

The 2025 `SLCM-is-Dumb` repository then advertises digit-CAPTCHA automation and CGPA extraction [4]. **Inference:** CAPTCHA alone is unlikely to be a durable control where users are willing to run full browser automation and OCR. This is not evidence that the production CAPTCHA is vulnerable in a legal or cryptographic sense. It is evidence that the threat model should include determined automation operating through a user's own session.

### Case study 2: A better interface can create a new trust boundary

`SLCM_APP` presents a modern mobile interface and custom credential logic around MUJ data [21]. The positive user goal is clear: easier access to attendance, grades, and schedules. The security tension is equally clear: any unofficial intermediary that receives institutional credentials or session material can become a new processor of education records.

**Inference:** the university's control choice is not simply "block apps." A sanctioned read-only API with delegated authorization, narrow scopes, revocable tokens, rate limits, and a documented acceptable-use policy could reduce pressure to share primary credentials. If MUJ does not intend to support integrations, it should state that clearly and warn students against entering university passwords into independent services.

**Section insight:** public projects reveal product demand and trust-boundary pressure. They do not establish authorization flaws, data leakage, or malicious intent.

## 4. Public Security Findings and Transferability

### Direct findings versus hypotheses

The research did not locate a public, reproducible vulnerability report tied to MAHE SLCM, MIT SIS, or MUJ SLCM. There was no attributable advisory for SQL injection, cross-site scripting, insecure direct object reference, account takeover, exposed student data, or an Akamai-origin bypass. Accordingly, none of those should be reported as a known Manipal flaw.

What the public record does establish is a set of **security signals**:

1. SLCM handles high-value education records and parent/student workflows [7].
2. Independent projects have attempted to retrieve marks, attendance, profiles, schedules, and CGPA [4][22][21].
3. Some integrations necessarily reason about user credentials or authenticated sessions [5][21].
4. CAPTCHA altered one integration and was later targeted by browser/OCR automation [22][4].
5. The MUJ page publicly exposes separate student and parent choices [3].
6. MAHE gives students and faculty Office 365 access, creating an account-lifecycle dependency beyond SLCM [7].

### Exact transferability matrix

| Candidate risk | Public basis | Transfer to MUJ | What is not established | Defensive priority |
|---|---|---|---|---|
| Credential stuffing or password spraying | Microsoft links legacy authentication to more than 97 percent of credential stuffing and more than 99 percent of password spraying in its analysis [9] | High where the same university account is reused across services | No attack against MUJ is shown | Critical |
| Student/parent authorization confusion | Both MAHE SIS and MUJ expose student/parent functions [20][3] | High at the workflow level | No broken authorization is shown | Critical |
| Unofficial credential delegation | Public apps describe login or custom credential logic [5][21] | High if students enter institutional passwords into third-party tools | Actual storage or misuse is not shown | High |
| Automated extraction | Repositories claim marks, attendance, profile, and CGPA extraction [22][4] | High for abuse monitoring and rate design | Bulk scraping of MUJ is not shown | High |
| CAPTCHA overreliance | One API stopped after CAPTCHA; a later tool claims OCR handling [22][4] | Medium-high | No live bypass was verified | High |
| CSRF coverage gaps | Public MUJ HTML contains an anti-forgery field on the observed login form | Medium | Presence on one form does not prove full application coverage | High |
| Legacy client dependency | Public MUJ HTML loads jQuery 1.10.2 | Medium | A library filename alone does not prove exploitability or patch state | Medium-high |
| Framework lifecycle ambiguity | Microsoft separates ASP.NET Framework components from external packages; public MVC package evidence points to 5.2.9 [12][33] | High for inventory governance | "MVC 5.3" is not verified | High |
| Edge/origin control gap | User supplied "behind Akamai" as context; Akamai publishes Origin IP ACL setup guidance [35] | Potentially high if an origin accepts direct traffic | No MUJ origin bypass was tested or established | High |
| Monitoring blind spots | OWASP says failed authentication attempts are critical early indicators of brute force, credential stuffing, and password spraying [27] | High | MUJ logging coverage is unknown | Critical |

### Case study 3: positive controls should not be overread

The public MUJ login HTML includes an anti-forgery token. That is a positive implementation signal for the observed form. It cannot demonstrate that every state-changing route validates a token, that the token is correctly bound to the user session, or that authenticated APIs have equivalent protection.

The same rule applies to Akamai and CAPTCHA. A WAF can filter malicious HTTP traffic [14], and CAPTCHA can raise automation cost, but neither replaces authorization, session security, credential-abuse monitoring, or origin restriction. **Inference:** MUJ should treat these as layers in a defense-in-depth model rather than proof of application security.

**Section insight:** the transferable finding is not "MIT had vulnerability X." It is that the same academic workflows attract automation, credentials, multiple roles, and third-party clients, making specific control tests highly valuable.

## 5. MUJ Architecture: Confirmed Signals and Unverified Premises

The supplied brief characterizes MUJ SLCM as ASP.NET MVC 5.3 on .NET Framework 4.x and IIS 10, behind Akamai, with Microsoft 365 identity. Public evidence supports only part of that statement.

| Architecture claim | Public evidence | Assessment |
|---|---|---|
| ASP.NET MVC family | MVC-style route structure, unobtrusive validation assets, and an anti-forgery field appear in the public HTML | **Plausible passive inference**, not version proof |
| ASP.NET MVC 5.3 | Public official package result found `Microsoft.AspNet.Mvc 5.2.9` [33] | **Unverified and potentially mislabeled**; confirm through internal SBOM |
| .NET Framework 4.x | Consistent with classic ASP.NET MVC, but no exact runtime was established publicly | **Unverified version** |
| IIS 10 | Supplied by the requester; public page content did not establish it | **Unverified externally** |
| Akamai edge | Supplied by the requester; no conclusive public Akamai marker was established | **Unverified externally** |
| Microsoft 365 identity | MAHE officially provides Office 365 to students and faculty [7]; MUJ's public page links password recovery to Microsoft's online reset service | **Strong ecosystem evidence**, but local login, federation, and password-hash ownership remain unclear |
| Student and parent roles | Visible public choices on the MUJ portal [3] | **Confirmed interface fact** |
| Login anti-forgery control | Visible in public HTML for the observed form | **Confirmed passive observation**, coverage unknown |
| Legacy jQuery filename | Public HTML references jQuery 1.10.2 | **Confirmed asset signal**, exploitability unknown |

Microsoft says IIS follows the Component Lifecycle Policy [25]. Its .NET Framework lifecycle page notes that 4.5.2, 4.6, and 4.6.1 retired on April 26, 2022 [26]. Therefore, "4.x" is too broad for a security conclusion: a supported, OS-bound Framework release and a retired release can both satisfy that label.

The same precision problem affects MVC. Microsoft states that ASP.NET combines components shipped inside .NET Framework with external packages [12]. An accurate review needs the operating-system edition, IIS role version, exact .NET Framework release, MVC NuGet package, authentication middleware, jQuery package and patches, and deployment date. A banner or filename is not a software bill of materials.

### Case study 4: the identity-recovery seam

MAHE documents Office 365 access for students and faculty [7], while the MUJ login page exposes institutional suffixes and Microsoft-hosted password recovery. **Inference:** identity lifecycle may cross a boundary between Microsoft 365 and a local SLCM application. The risk is not necessarily weak Microsoft authentication; it is inconsistent enforcement among login, recovery, account disablement, parent access, and active SLCM sessions.

Microsoft recommends staging legacy-authentication blocking in Report-only mode before enforcement and excluding emergency accounts to avoid administrative lockout [9]. For MUJ, the analogous safe approach is an owner-run mapping of every authentication path before policy enforcement.

**Section insight:** architecture labels are useful only when they lead to exact inventory. The most important current finding is uncertainty, especially around "MVC 5.3," not a version-based vulnerability claim.

## 6. Safe Validation and Remediation Priorities

The following work should be performed only by MUJ/MAHE personnel or a contractor with written scope, test accounts, approved hours, data-handling rules, and incident contacts. The university security club can help write test cases, review public policy, or build a lab clone. It should not exercise these cases against production.

### Exact 30/60/90-day defensive plan

| Time | Owner-authorized action | Evidence driving it | Success criterion |
|---|---|---|---|
| 0-30 days | Produce an exact SBOM for OS, IIS, .NET Framework, MVC packages, JavaScript libraries, authentication middleware, and Akamai controls | MVC 5.3 and .NET 4.x are not precise enough for lifecycle decisions [12][25] | Every production component has version, support status, owner, and patch source |
| 0-30 days | Map student, parent, faculty, admin, service-account, and recovery flows | SLCM and SIS explicitly serve student and parent workflows [7][20] | Data-flow and trust-boundary diagrams approved by system and identity owners |
| 0-30 days | Review failed-login, recovery, lockout, and unusual-download telemetry | Failed authentication attempts are early credential-attack indicators [27] | Central alerting covers every login path with privacy-safe retention |
| 0-30 days | Publish a vulnerability-reporting channel and safe-harbor statement | MAHE's public policy requires investigation but gives no specific reporting contact in the reviewed text [8] | A monitored security address, acknowledgement SLA, and disclosure process are public |
| 31-60 days | Validate MFA and Conditional Access coverage using Report-only rollout | Microsoft recommends Report-only staging before activation [9] | No unmanaged legacy path bypasses intended MFA policy |
| 31-60 days | Test role and object authorization with synthetic student and parent accounts | Separate parent/student functions and sensitive academic modules create a high-value boundary [3][7] | Every object access decision is enforced server-side and logged |
| 31-60 days | Review session renewal, logout, revocation, timeout, and recovery-session invalidation | Public wrappers depend on authenticated sessions [5] | Password reset, role change, and account disablement invalidate relevant sessions |
| 31-60 days | Verify anti-forgery coverage for every state-changing action | One public form carries a token, but coverage is unknown | Framework validation is mandatory and regression-tested across state changes |
| 31-60 days | Restrict origin acceptance to intended Akamai paths and monitor exceptions | Akamai publishes Origin IP ACL setup and origin-update guidance [35] | Direct-origin traffic is denied except documented health and administration paths |
| 61-90 days | Decide on a sanctioned API or explicit no-integration policy | Public clients repeatedly target marks, attendance, profiles, and schedules [22][21] | Students never need to give a third party their primary university password |
| 61-90 days | Add abuse controls beyond CAPTCHA | CAPTCHA stopped one client but later automation claimed to handle it [22][4] | Layered controls include rate, risk, session, authorization, and anomaly signals |
| 61-90 days | Run tabletop exercises for account compromise and grade/privacy incidents | SLCM contains marks, attendance, results, and messages [7] | Identity, registrar, IT, legal, communications, and student-support roles are rehearsed |

A sanctioned integration model deserves emphasis. If the university wants to support student innovation, it can offer delegated authorization, read-only scopes, short-lived tokens, clear rate limits, test data, and rapid revocation. If it does not, it should publish an explicit warning that independent tools are not official and must not collect institutional passwords. MUJStella's own public disclaimer demonstrates the value of clearly distinguishing independent services from official ones [23].

The reporting channel also matters. MAHE's policy says violations should be documented, reported, and investigated [8], but the reviewed public text supplies no dedicated disclosure address. A clear channel reduces the chance that a well-intentioned student posts sensitive details publicly or experiments further because no owner responds.

**Section insight:** the highest-value controls are exact asset inventory, role-aware authorization, identity/session consistency, credential-abuse visibility, safe origin configuration, and a legitimate path for student innovation and disclosure.

## 7. Synthesis: What Transfers, What Diverges, and Why

The evidence reveals three different systems of trust: the official MAHE/MIT academic estate, the separate MUJ deployment, and independent developer clients. Their goals overlap, but their control models differ.

| Dimension | MAHE/MIT official estate | MUJ SLCM | Independent clients | Integrated conclusion |
|---|---|---|---|---|
| Scope | SIS/SLCM plus Office 365, Teams, LMS, library, and learning platforms [2][7] | Public student and parent portal [3] | Grades, attendance, profiles, CGPA, schedules [4][22][21] | Protect workflows and identity links, not only one hostname |
| Identity mechanism | MAHE-wide Office 365 availability plus SIS/SLCM accounts [7][20] | Microsoft recovery link plus local-looking login form | Some projects accept credentials or manage sessions [5][21] | Primary credential delegation is the clearest cross-cutting risk |
| Security mechanism | Institutional policy and role-based need-to-know principle [8] | Anti-forgery signal, CAPTCHA context, asserted Akamai edge | Browser automation, OCR, custom app logic | Layered server-side controls must assume client automation |
| Evidence quality | Official documentation | Passive public observation plus requester-supplied stack | Repository self-description | Do not assign equal confidence to all three |
| Time horizon | Long-lived academic system | Current target deployment | Projects from 2020 and 2025 [5][4][21][22] | Automation demand persists even as controls change |
| Main trade-off | Access and integration versus governance | Usability versus role and session assurance | Convenience versus credential and privacy trust | A scoped official API can reduce unsafe workarounds |
| Transferability | Business workflows are well documented | Same general student-lifecycle domain | Tools reveal desired data and friction | Test cases transfer strongly; vulnerability claims do not |

The most important non-obvious tension is CAPTCHA versus accessibility. One project was deprecated when CAPTCHA arrived [22], while a later project says it automates digit CAPTCHA [4]. The mechanism suggests an arms race: friction suppresses simple clients but encourages more complex automation. The implication is not to remove CAPTCHA automatically, but to avoid treating it as the principal account-defense control.

A second tension is integration versus credential safety. Students want concise views of attendance, marks, and schedules, while unofficial clients may need to imitate a browser session. The official system can reduce this pressure through delegated, revocable access. Without that option, users may rationally choose convenience over security.

A third tension is shared family versus separate deployment. MAHE and MUJ have aligned academic functions, but the public record does not show shared code, identity tenants, databases, or patch management. This makes workflow-driven testing appropriate and exploit transfer inappropriate.

A fourth tension is visible control versus actual coverage. An anti-forgery token, CAPTCHA, WAF, or Microsoft reset link can be a useful control. None independently answers whether all routes enforce authorization, all sessions revoke correctly, or all origins reject unintended traffic.

**Synthesis insight:** the defensible analytical chain is **observation -> mechanism -> bounded implication -> owner action**. Public automation shows demand; high-value records explain the demand; shared workflows make defensive test cases portable; uncertainty about implementation prevents vulnerability attribution.

## VERDICT

**Verdict:** MIT/MAHE public evidence is useful for building a MUJ SLCM defensive assessment, but it does not establish a transferable vulnerability.

**Overall confidence: Medium-High (0.78).**

| Proposition | Confidence | Verdict |
|---|---:|---|
| MIT/MAHE and MUJ belong to the same broad SLCM problem family | 0.95 | Supported by official SLCM functions and both portal estates [7][3] |
| MIT students use SIS/SLCM for academic workflows | 0.85 | Strong institutional inference from MIT's MAHE context and the official MAHE student portal [24][2] |
| MAHE students and faculty have Office 365 access | 0.98 | Explicitly documented [7] |
| MUJ uses Microsoft-linked password recovery | 0.90 | Visible in passive public HTML; exact federation model remains unknown |
| MUJ runs ASP.NET MVC family software | 0.75 | Passive framework signals support the inference |
| MUJ runs "ASP.NET MVC 5.3" | 0.25 | Not verified; official package evidence located 5.2.9 instead [33] |
| MUJ is securely isolated behind Akamai | 0.40 | Requester-supplied premise; no authorized origin validation was performed |
| A public Manipal SLCM vulnerability has been verified | 0.10 | No attributable disclosure was found in the bounded research |
| Automation and third-party credential handling are relevant threats | 0.95 | Multiple independent repositories directly support this conclusion [4][5][21][22] |
| Maintainers of the reviewed repositories are MIT Manipal students | 0.15 | Public profiles did not establish that affiliation [29][31][30][32] |

The club should present its work to MUJ as a **defensive hypothesis register**, not a vulnerability report. The immediate request should be for an internal SBOM, identity and role-flow diagrams, a sanctioned test environment, a public disclosure channel, and permission for a scoped assessment. Until those exist, the correct statement is: **public evidence identifies likely control priorities, but no production weakness has been demonstrated.**

## References

1. *Manipal Academy of Higher Education - MU SLcM*. https://slcm.manipal.edu/
2. *Student Portal Login- MAHE (Manipal Academy Of Higher ...*. https://www.manipal.edu/mu/academics/student-portal.html
3. *muj portal - Manipal University*. https://mujslcm.jaipur.manipal.edu/
4. *GitHub - sankalp2004/SLCM-is-Dumb: This extracts cgpa from ...*. https://github.com/sankalp2004/SLCM-is-Dumb
5. *GitHub - nikeplusdash/SLCM-api: An api for https://slcm ...*. https://github.com/nikeplusdash/SLCM-api
6. *MIT*. https://admin.mit659.examly.io/login
7. *Fetched web page*. http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf
8. *Information Security Policy - Manipal*. https://www.manipal.edu/mu/policies/it-policy/information-security-policy.html
9. *Block legacy authentication with Conditional Access ...*. https://learn.microsoft.com/en-us/entra/identity/conditional-access/policy-block-legacy-authentication
10. *SIS - Manipal Academy of Higher Education*. https://sis.manipal.edu/SLCMRTGS01.aspx
11. *SIS - Manipal Academy of Higher Education*. https://sis.manipal.edu/studloginSLCM.aspx
12. *ASP.NET official support policy | .NET*. https://dotnet.microsoft.com/en-us/platform/support/policy/aspnet
13. *Origin Server*. https://techdocs.akamai.com/property-mgr/docs/origin-server
14. *What Is a Web Application Firewall (WAF)?*. https://www.akamai.com/glossary/what-is-a-waf
15. *Session Management - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
16. *Conditional Access adaptive session lifetime policies - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-session-lifetime
17. *Authentication - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
18. *Cross-Site Request Forgery Prevention - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
19. *HTTP Headers - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html
20. *Manipal Academy of Higher Education - SIS Portal*. https://sis.manipal.edu/
21. *GitHub - DK10WS/SLCM_APP: App Version for MUJ SLCM · GitHub*. http://github.com/DK10WS/SLCM_APP
22. *GitHub - canaryGrapher/slcmAPI: The API for SLcM, Manipal. Get your marks, your attendance and your profile details · GitHub*. http://github.com/canaryGrapher/slcmAPI
23. *MUJStella - Student Platform for Manipal University Jaipur*. https://mujstella.in/
24. *Manipal Institute of Technology (MIT) | MAHE*. https://www.manipal.edu/mit.html
25. *Internet Information Services (IIS) - Microsoft Lifecycle*. https://learn.microsoft.com/en-us/lifecycle/products/internet-information-services-iis
26. *Microsoft .NET Framework - Microsoft Lifecycle*. https://learn.microsoft.com/en-us/lifecycle/products/microsoft-net-framework
27. *Logging Cheat Sheet*. https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
28. *Credential Stuffing Prevention - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Credential_Stuffing_Prevention_Cheat_Sheet.html
29. *DK10WS (Dhruv Kunzru) · GitHub*. https://github.com/DK10WS
30. *nikeplusdash (Nikesh Kumar) · GitHub*. https://github.com/nikeplusdash
31. *sankalp2004 · GitHub*. https://github.com/sankalp2004
32. *canaryGrapher (Yash) · GitHub*. https://github.com/canaryGrapher
33. *NuGet Gallery | Microsoft.AspNet.Mvc 5.2.9*. https://www.nuget.org/packages/Microsoft.AspNet.Mvc/5.2.9
34. *Library Portal*. https://libportal.manipal.edu/
35. *Welcome to Origin IP ACL*. https://techdocs.akamai.com/origin-ip-acl/docs/welcome
