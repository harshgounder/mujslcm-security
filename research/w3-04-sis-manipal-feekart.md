# MAHE SIS Risk and MUJ SLCM Trust Boundaries

## Executive Summary

- **Two Portals, One Human Trust Zone**: The official MAHE SIS page serves students and parents, exposes a separate administrator/faculty choice, and directs logged-in users to Fee Kart, while the MUJ portal presents student and parent sign-in under the Manipal brand [2][8] -> manage these as separate technical trust zones but one social-engineering and support ecosystem.
- **Fee Kart Is Confirmed, Its Back End Is Not**: SIS explicitly says to log in and select Fee Kart; public payment pages collect application, name, amount, email, and mobile details and say a receipt will be emailed [2][1][4] -> document the authenticated handoff, payment-processor redirect, callback validation, and reconciliation flow internally rather than assuming the public pages reveal it.
- **Session Internals Remain Unpublished**: The public SIS login content shows a date field and CAPTCHA, but the reviewed official pages do not publish timeout, rotation, cookie, or server-side logout behavior [3] -> test those controls only under written university authorization and compare them with OWASP rotation, expiry, and logout guidance [22].
- **Complaints Signal Friction, Not Compromise**: Individual Reddit posts report registration-number login failures, a correct password being rejected, and recurring crashes, but these are unverified anecdotes [18][15][17] -> use them to prioritize support telemetry and availability review, not to allege a breach.
- **Legacy Routes Are Still Publicly Observable**: Known `.aspx` pages include the landing page, student login, payment pages, an RTGS-named login route, and a mess-change page; the Wayback CDX record shows captures of the main SIS page beginning in 2013 [24][2][25][28] -> inventory and retire obsolete routes, but do not equate an old-looking URL with a vulnerability.
- **Third-Party Tools Expand Credential Risk**: Unofficial repositories claim to submit SLCM logins, retrieve academic data, and require logout; another is explicitly deprecated after CAPTCHA appeared [13][11] -> publish a clear policy against entering university credentials into unapproved tools and provide sanctioned alternatives.
- **Microsoft 365 Linkage Is Only Partly Proven Publicly**: MAHE says its Microsoft Office 365 subscription extends to faculty and students, and the MUJ page displays an `@muj.manipal.edu` sign-in suffix [10][8] -> treat federated identity, MFA, and account-recovery coupling as verification targets, not as established facts about SIS.
- **Overall Verdict Is Moderate Confidence**: Official sources strongly establish SIS roles, Fee Kart instructions, public payment fields, and route history, but not session implementation, payment callback security, database sharing, credential synchronization, or SSO between MAHE SIS and MUJ SLCM -> prioritize an authorized architecture review before any live security testing.

## Scope, Safety, and Evidence Method

This report is a passive OSINT and defensive application-security assessment. It uses public pages, public archives, official policy material, Microsoft and OWASP guidance, public source-code repository descriptions, and public user comments. No authentication attempt, CAPTCHA bypass, form submission, payment action, cookie collection, port scan, vulnerability scan, or error elicitation was performed. The requester-supplied stack details - including the IP address, IIS version, Akamai placement, ASP.NET MVC version, .NET Framework version, and Microsoft 365 identity description - are treated as hypotheses unless independently supported below.

I cannot provide private chain-of-thought. Instead, the report makes the auditable reasoning explicit in the useful form: **observation -> labeled inference -> defensive implication**. This preserves reproducibility without publishing hidden reasoning or operational attack instructions.

| Evidence class | What it can establish | What it cannot establish | Treatment in this report |
|---|---|---|---|
| Official MAHE or MUJ page | Published role, visible field, instruction, policy, or portal branding | Hidden authorization logic, database design, callback signing, or session configuration | Treated as strong evidence for the visible claim only |
| Microsoft or OWASP guidance | Platform lifecycle or recommended control behavior | Whether the university deployed the control correctly | Used as a defensive benchmark, never as proof of a defect |
| Wayback CDX metadata | A URL was captured at listed times | That the old application remains active or vulnerable | Used to establish historical visibility only |
| Public GitHub repository | What an outside developer claimed a tool did | Production architecture, institutional approval, or current behavior | Labeled unofficial and non-authoritative |
| Reddit post | A person publicly reported an experience | Frequency, root cause, impact, or breach status | Labeled anecdotal and used only as a lead |

MAHE's own security policy says information confidentiality, integrity, and availability are paramount, calls for periodic risk assessment, and requires access to be controlled, monitored, and authorized by job function and need [9]. It also calls for annual review and review after major environmental changes [9]. That policy makes a documented SIS-to-MUJ trust-boundary review institutionally aligned, not merely a technical preference.

**Decision-ready insight:** the evidence is sufficient for a defensive risk model and control roadmap, but insufficient for a finding of exploitable vulnerability or actual compromise.

## Asset Boundaries: MAHE SIS Is Not Proven to Be MUJ SLCM

The official MAHE SIS landing page describes SIS as meeting the information needs of MAHE students and parents. It restricts services to bona fide students and parents, presents student/parent and administrator/faculty login choices, and tells users to log in and select Fee Kart [2]. The official MAHE student-portal page links users to `https://sis.manipal.edu/index.aspx`, reinforcing that SIS is an institutionally promoted portal [6].

The public MUJ page is visibly different. It says "WELCOME TO MUJ PORTAL," displays `@muj.manipal.edu`, and offers parent login [8]. Separately, MAHE documentation says SLCM replaced an older Academic Management System and includes attendance, internal marks, external marks, result publication, and broadcast messages; it calls SLCM a single window for students and parents [10]. These facts establish overlapping user populations and academic functions, not a shared database, shared password store, or shared session.

| Surface | Publicly supported purpose | Identity clue | Trust conclusion |
|---|---|---|---|
| `sis.manipal.edu` | MAHE student/parent information and Fee Kart access; separate admin/faculty choice [2] | Date field plus CAPTCHA visible on the student login page [3] | A credentialed academic and payment-adjacent application |
| `mujslcm.jaipur.manipal.edu` | MUJ portal with parent and student-oriented sign-in presentation [8] | `@muj.manipal.edu` suffix [8] | A distinct MUJ-branded identity entry point |
| MAHE SLCM documentation | Attendance, marks, results, and circulars for students and parents [10] | No architecture or SSO claim in the cited document | Functional overlap, not proof of technical coupling |
| Microsoft 365 at MAHE | Subscription extended to faculty and students [10] | Organization-managed productivity identity exists | Potential identity context; SIS federation is unproven |
| Public payment pages | Initiation/contact fields and receipt email behavior [1][4] | Email and mobile are transaction-contact attributes | Payment and identity data intersect operationally |

**Inference, clearly labeled:** Because the portals share the Manipal brand, student/parent populations, academic context, and support expectations, users are likely to perceive them as one trust ecosystem even if the back ends are separate. That human trust overlap can make a compromise or convincing impersonation of one portal useful against the other. The public evidence does **not** prove automatic lateral movement.

**Decision-ready insight:** create and maintain a signed-off data-flow diagram showing identity provider, account source, password-reset owner, parent-account source, SIS/SLCM API links, and payment callbacks. Until that exists, treat the systems as independent at the network and session layers but connected at the fraud and social-engineering layers.

## SIS Login Flows: What Is Visible and What Is Missing

The strongest public description is the SIS landing page. It separates a student/parent path from an administrator/faculty path and limits the service to bona fide MAHE students and parents [2]. The student login page's extracted visible text contains a login control, a date formatted as `dd/mm/yyyy`, and CAPTCHA [3]. A second public route, `SLCMRTGS01.aspx`, repeats the SIS description and exposes a student/parent login, date field, and CAPTCHA [24].

The extracted pages do not establish whether the date is a password substitute, a second factor, or merely another identifier. They also do not reveal lockout thresholds, generic-error behavior, password hashing, account recovery, MFA, session-cookie attributes, or whether the administrator/faculty path uses separate authentication infrastructure. Any stronger statement would be speculation.

| Flow stage | Public observation | Confidence | Defensive question for an authorized review |
|---|---|---|---|
| Entry | Official SIS landing page distinguishes student/parent and administrator/faculty [2] | High | Are role-specific entry points backed by separate policies and privilege boundaries? |
| Eligibility | Only bona fide MAHE students/parents are described as eligible [2] | High | How are enrollment termination, alumni status, and parent access revoked? |
| Student authentication | Login, `dd/mm/yyyy`, and CAPTCHA are visible [3] | High for visible UI, low for semantics | Is the date sensitive authentication data or only an identifier? |
| Alternate public route | `SLCMRTGS01.aspx` presents similar student/parent login elements [24] | High for route content | Is it intentionally supported, an alias, or a legacy entry point? |
| Post-login payment | SIS directs the user to click Fee Kart after login [2] | High | Does the payment handoff use a short-lived, signed, user-bound transaction? |
| Recovery and MFA | No reviewed official page documents these controls [3] | Low knowledge, not evidence of absence | Which identity system owns reset, step-up, lockout, and help-desk verification? |

OWASP warns that overly specific authentication errors can enable account enumeration and recommends a generic response [19]. For this ecosystem, the defensive requirement is consistency across old and new routes: the same generic error semantics, throttling, CAPTCHA policy, logging, and account-recovery verification should apply everywhere. This is a recommendation, not a claim that SIS currently fails it.

**Inference, clearly labeled:** A date-based field can be low entropy or socially discoverable if it represents date of birth. The page does not label the field clearly enough in the extracted content to prove that interpretation, so this report does not call it a vulnerability. The university should internally confirm the field's meaning and ensure it is not treated as a secret if it is biographical data.

**Decision-ready insight:** the immediate task is not public testing. It is owner-assisted documentation of every login route, identity attribute, reset path, and role transition, followed by a controlled assessment under written authorization.

## Fee Kart and Payment Trust: Confirmed Handoff, Unknown Reconciliation

SIS explicitly tells authenticated users to click "Fee Kart" and pay academic fees online [2]. The public `OnlinePayment01.aspx` page asks for a valid email address and mobile number and says the payment receipt will be emailed [1]. A public MAHE course-fee page lists MAHE application number, name, fee amount, email address, and mobile number [4]. These facts show that academic identity, transaction amount, and contact data meet in the payment journey.

An undated public fee page also states that transaction fees are borne by the cardholder, that those fees are not reversed for refunds, reversals, or chargebacks, and that users should check charges before payment [4]. The same page lists Atom and HDFC columns, including card and net-banking charges, and says convenience charges attract 18 percent GST [4]. Because the page is undated, those gateway names and rates should be treated as page content, not proof of the current processor contract.

| Payment element | Public evidence | Security significance | Status |
|---|---|---|---|
| Authenticated entry | SIS says login, then select Fee Kart [2] | The account-to-transaction binding begins inside SIS | Confirmed instruction; implementation unknown |
| Payer contact | Email and mobile are collected; receipt is emailed [1] | Contact changes or injection could misdirect receipts or aid fraud | Confirmed fields; validation unknown |
| Academic identity | Application number and name are collected [4] | Transaction must be bound to the correct applicant/student | Confirmed fields; authoritative source unknown |
| Amount | Fee amount is a visible input/field [4] | Server-side amount integrity and reconciliation are critical | Confirmed field; editability and validation unknown |
| Processor references | Atom and HDFC appear in a gateway-charge table [4] | Multiple processor paths can create configuration and callback complexity | Historical/current status not established |
| Receipt | Receipt is sent to the supplied email [1] | Receipt delivery is not the same as authoritative ledger posting | Confirmed message; reconciliation logic unknown |

**Inference, clearly labeled:** The most consequential failure modes are not necessarily card theft. A compromised SIS account or weak transaction binding could support wrong-account posting, altered contact details, false receipt narratives, or convincing fee-payment phishing. This inference is based on the confirmed combination of authenticated Fee Kart access and public collection of application, amount, email, and mobile data [2][1][4]. No such failure is demonstrated here.

The public evidence does not reveal whether cardholder data ever touches MAHE systems, whether the browser is fully redirected to a hosted processor, how callbacks are authenticated, whether transaction identifiers are replay-protected, how duplicate payments are handled, or which system is authoritative for the student ledger. It also does not show whether Fee Kart shares the SIS session or exchanges a signed one-time token.

**Decision-ready insight:** the university should document four controls: server-derived amount and student identity, a short-lived signed handoff, authenticated and idempotent processor callbacks, and ledger reconciliation independent of browser-visible success. Students should be told that an emailed receipt is evidence of a message, while the authoritative fee status remains the university ledger.

## Public Complaints: Availability and Identity Friction, Not Breach Evidence

The public complaint record found in this review is small and anecdotal. One post says that after an intra-sliding update, both the old and new registration numbers were rejected [18]. A MUJ-related post says a password was shown as wrong even though the user believed it was correct [15]. Another user complained that SLCM crashed "every other day" [17]. These statements are useful signals about user experience, but they do not establish root cause.

| Public report | Reported symptom | What it may justify | What it does not prove |
|---|---|---|---|
| `Slcm login.` | Old registration number became invalid after an update; new number was also rejected [18] | Review identity lifecycle and registration-number migration | Account takeover, data corruption, or systemic failure |
| `Slcm portal issue` | User believed the correct password was rejected [15] | Review error messaging, reset support, and identity synchronization | Password compromise or authentication defect |
| `SLCM IS LITERALLY ASS` | User alleged recurring crashes [17] | Review uptime telemetry, peak-load behavior, and status communication | Measured outage rate or security incident |

No credible public source located in the targeted searches established a breach of `sis.manipal.edu`, Fee Kart, or MUJ SLCM. That is a bounded research result, not proof that no incident has occurred. Search engines miss private disclosures, internal incident records, deleted material, and reports under different product names.

The complaint pattern does expose a support risk. When students encounter ambiguous credential errors or identity changes, they are more likely to seek informal help. **Inference:** that increases susceptibility to fake support accounts, credential-harvesting pages, and misleading payment assistance. The inference is consistent with the reported login friction [18][15], but no phishing campaign is proven.

The best response is operational: publish one canonical status page, one official support path, and screenshots of legitimate domain and redirect patterns. Log identity-renaming events, failed login reason categories, reset attempts, and help-desk verification outcomes without exposing sensitive details. Correlate complaint spikes with deployment, enrollment, fee, and examination windows.

**Decision-ready insight:** complaints should drive reliability and anti-fraud controls, not public vulnerability claims. The security club can help classify reports and improve user guidance without testing other people's accounts.

## Session Behavior: Evidence Is Thin, So Controls Matter More

The official public pages do not document session timeout, renewal, cookie scope, concurrent-session policy, remember-me behavior, or server-side invalidation [3]. The `studloginSLCM.aspx` content confirms CAPTCHA and a login interface but not post-authentication behavior [3]. A separate public route returns menu labels including virtual-account details, hostel dues, receipt reprint, hostel vacating form, and logout, but its purpose and authorization state are not established by the visible content alone [25].

Unofficial repositories add historical context but cannot prove production behavior. One README says its API logged into `slcm.manipal.edu`, fetched basic user data, stored no user data, required `/login` before other routes, and told users always to log out [13]. Another project says it scraped marks, attendance, and profile details, then became deprecated when CAPTCHA was introduced [11]. A newer unofficial project claims automated CAPTCHA handling; this report omits operational details and does not endorse bypassing access controls [12].

| Session question | Public answer | Confidence | Required authorized verification |
|---|---|---|---|
| Is CAPTCHA present? | Visible on the SIS student login page [3] | High | Confirm server-side validation and accessibility fallback |
| Is logout present? | A public route exposes a logout menu label; an unofficial API tells users to log out [25][13] | Medium for presence, low for semantics | Confirm server-side invalidation and back-button/cache behavior |
| Are sessions rotated after login? | Not publicly documented | Unknown | Verify session identifier renewal at authentication and role changes |
| Are idle and absolute timeouts enforced? | Not publicly documented | Unknown | Measure only in an authorized test account and approved window |
| What is cookie scope? | Not publicly documented | Unknown | Review `Secure`, `HttpOnly`, `SameSite`, path, domain, and host-only scope |
| Are MAHE SIS and MUJ sessions shared? | No public proof | Unknown | Trace identity and cookie boundaries in architecture documentation |

OWASP says session identifiers must be renewed after privilege changes, especially authentication, to prevent fixation [22]. It also says applications should provide an accessible logout, invalidate sessions server-side, and enforce idle and absolute timeouts on the server [22]. OWASP recommends cookies for session exchange, explicit `SameSite=Strict` or `Lax`, and `Secure` when `SameSite=None`; it treats SameSite as defense in depth rather than a CSRF replacement [22].

For state-changing actions, OWASP recommends server-generated, secret, unpredictable CSRF tokens and rejecting missing or mismatched values [23]. It also says not to use GET for state changes and to add validated CSRF tokens where the framework lacks built-in protection [23]. These are benchmarks, not findings that SIS fails them.

**Decision-ready insight:** session confidence is low because implementation evidence is absent. The correct conclusion is "unknown and high priority for authorized validation," not "vulnerable."

## Archive Routes and Historical Exposure

The SIS surface has accumulated public routes over time. The Wayback CDX response for `index.aspx` contains captures beginning on October 3, 2013, followed by repeated HTTP and HTTPS captures [28]. This establishes a long public history for the landing page. It does not establish how long the current code has been deployed or whether archived responses contained authenticated data.

| Public route | Visible role or content | Historical interpretation | Security interpretation |
|---|---|---|---|
| `/index.aspx` | SIS purpose, eligible users, role choices, Fee Kart instruction [2] | Main landing route; archived from 2013 [28] | Expected public entry point |
| `/studloginSLCM.aspx` | Login, date field, CAPTCHA [3] | Legacy-style `.aspx` naming | Public authentication route; no flaw established |
| `/OnlinePayment01.aspx` | Email/mobile collection and emailed receipt statement [1] | Public payment-support route | Validate ownership, freshness, and redirect integrity internally |
| `/admissions/CourseFeesMAHE01.aspx` | Application, name, amount, email, and mobile fields [5] | Admissions payment route | Public fields do not reveal server-side validation |
| `/admissions/CourseFeesMAHE02.aspx` | Similar fields plus gateway-charge terms [4] | Parallel or versioned payment route | Possible duplication; intended status is undocumented |
| `/SLCMRTGS01.aspx` | SIS description and student/parent login elements [24] | RTGS-named alternate entry point | Filename alone does not prove payment logic or exposure |
| `/SLCMMessChange04Blocked.aspx` | Virtual-account, hostel, receipt, vacating, logout, and mess-change labels [25] | Function-specific legacy route | Menu text alone is not authorization bypass or data disclosure |

The key risk is governance, not the age of `.aspx`. Old routes can escape modern controls if they are excluded from centralized authentication, logging, CSRF protection, WAF policy, or release management. **Inference:** duplicated payment and login pages increase the chance of configuration drift. This is plausible from the parallel public routes, but no drift was observed [4][5][24].

A defensive archive review should start from the university's own source control, IIS configuration, route inventory, DNS history, and payment-processor records. Public Wayback pages are useful for naming and branding history, but they must not be used to submit credentials or payments. Retired pages should return a clear terminal status or redirect only to a canonical official route; sensitive responses should set appropriate cache controls.

**Decision-ready insight:** route age is a prioritization signal. Authorization, session, and callback behavior determine risk.

## How a SIS Breach Could Affect MUJ SLCM Trust

No breach is established. The following is a scenario model, and every cross-system step is explicitly an inference unless the source proves it.

| Scenario | Confirmed starting fact | Inferred cross-system mechanism | Potential consequence | Defensive break point |
|---|---|---|---|---|
| Credential reuse | SIS and MUJ both serve student/parent populations [2][8] | **Inference:** some users may reuse passwords | Compromised SIS credentials might be tried against MUJ or email | Enforce distinct IdP policy, MFA, breached-password screening, and rate limits |
| Academic-data phishing | SLCM covers attendance, marks, results, and circulars [10] | **Inference:** stolen SIS/SLCM context could make messages highly convincing | Targeted fake grade, attendance, or result notices | Signed communications, canonical links, and user education |
| Fee fraud | Fee Kart follows SIS login; payment pages combine identity, amount, email, and mobile [2][1][4] | **Inference:** compromised data could support a plausible payment-redirection story | Wrong-destination payment or fraudulent support contact | Canonical payment origin, signed handoff, ledger confirmation, out-of-band warnings |
| Parent impersonation | Both ecosystems expose parent-oriented access [2][8] | **Inference:** family contact data or trust could be abused in recovery calls | Help-desk-assisted account takeover | Role-specific recovery scripts and verified parent-student linkage |
| Microsoft 365 pivot | MAHE provides Office 365 to faculty and students [10] | **Inference:** if identifiers or recovery channels overlap, SIS data could aid M365 phishing | Mailbox compromise, malicious reset messages, wider institutional fraud | Phishing-resistant MFA, conditional access, and recovery separation |
| Session crossover | Both are web portals | **Inference only:** shared cookie domain, SSO token, or API trust could create direct movement | Cross-application session abuse | Host-only cookies, audience-restricted tokens, separate signing keys, no implicit trust |
| Brand-trust spillover | Both use Manipal branding and academic workflows [2][8] | **Inference:** users may not distinguish domains | A compromise of one portal damages trust in legitimate prompts from the other | Consistent domain guidance, status communication, and incident messaging |

The most important distinction is between **identity compromise** and **technical lateral movement**. Identity compromise can cross boundaries through reused secrets, shared recovery channels, or persuasive context even when networks and databases are isolated. Technical lateral movement would require a concrete trust link such as shared credentials, SSO tokens, APIs, keys, cookies, or administrative infrastructure. None of those links is proven publicly.

MAHE's security policy requires monitored, authorized access based on job function and need [9]. Applied here, parent, student, faculty, administrator, payment-service, and support roles should be separately modeled. Payment support should not be able to reset academic identity; SIS administrators should not automatically hold MUJ or Microsoft 365 privileges; parent recovery should not rely solely on information visible in SIS.

**Decision-ready insight:** assume social and identity blast radius across the brand, but require evidence before asserting network, database, or session blast radius.

## Defensive Priorities for the University Security Club

The club should work through university sponsors, written scope, test accounts, and a defined disclosure channel. Public OSINT can support asset ownership, documentation quality, and user education. Any active authentication, scanning, payment simulation, CAPTCHA testing, or session measurement requires explicit authorization.

| Priority | Owner | Defensive action | Evidence-based rationale | Safe club contribution |
|---|---|---|---|---|
| 1 | Identity/IAM | Produce an authoritative SIS-MUJ-M365 identity and recovery map | Public sources prove overlapping populations but not the trust links [2][10][8] | Create a documentation template and review public login wording |
| 2 | SIS application team | Inventory every `.aspx` login, payment, and functional route | Multiple current and archived routes are public [24][2][25][28] | Maintain a passive URL catalog from official and archived sources only |
| 3 | Payment and finance | Document signed handoff, callback authentication, idempotency, and ledger reconciliation | Fee Kart and payment fields are confirmed; back-end integrity is unknown [2][1][4] | Review student-facing payment guidance, not payment mechanics |
| 4 | Application security | Validate rotation, timeout, logout, cookie, cache, and CSRF controls | Official session behavior is unpublished; OWASP defines the baseline [22][23] | Build equivalent checks in a local lab application |
| 5 | Support operations | Standardize identity-change and password-failure handling | Public anecdotes show registration and password friction [18][15] | Draft anti-phishing and escalation guidance |
| 6 | Security operations | Correlate login, reset, payment, and M365 alerts | The human trust zone spans academic, payment, and productivity contexts [1][10] | Design a privacy-preserving event taxonomy |
| 7 | Governance | Publish approved-client and credential-handling policy | Third-party tools claim credentialed access and academic-data retrieval [13][11] | Inventory public tools and send neutral notices to owners |
| 8 | Communications | Publish canonical domains, status, and incident messages | Complaints and multiple portals can drive informal support-seeking [18][17] | Create user-facing domain verification material |

The platform lifecycle also needs nuance. Microsoft says ASP.NET includes components in .NET Framework, including Web Forms, while MVC and several other packages can ship separately [20]. Microsoft also says IIS follows the lifecycle of the Windows operating system and lists different IIS 10 support dates for Windows Server 2016 and 2019 [21]. Therefore, an IIS 10 banner alone cannot determine support status; the underlying Windows edition and patch level must be verified internally.

The club should not label Web Forms, MVC 5.3, `.aspx`, or IIS 10 as vulnerable merely because they are mature technologies. Risk comes from patch state, configuration, application logic, dependency versions, identity design, and operational controls. The productive case study is the route inventory itself: multiple public entry and payment pages reveal where governance must ensure identical controls, but they do not prove a control failure.

**Decision-ready insight:** use passive OSINT to improve ownership and communication, then hand the unresolved technical questions to an authorized assessment team.

## Synthesis

The ecosystem combines a visibly legacy MAHE SIS surface, a distinct MUJ login experience, a university-wide Microsoft 365 entitlement, and payment-adjacent workflows. The systems differ in mechanism and evidence base, yet converge in the user's mental model.

| Dimension | MAHE SIS | MUJ SLCM | Payment boundary | Cross-cutting implication |
|---|---|---|---|---|
| Primary scope | Student/parent information, role-separated login, Fee Kart [2] | MUJ-branded student/parent portal [8] | Application/identity/contact/amount collection [1][4] | One user journey spans several trust owners |
| Authentication evidence | Date field and CAPTCHA visible; internals unknown [3] | `@muj.manipal.edu` visible; federation internals unknown [8] | SIS login precedes Fee Kart [2] | Shared brand does not prove shared authentication |
| Data sensitivity | Academic and role data by system purpose [2] | SLCM documentation includes marks, attendance, results, circulars [10] | Identity, amount, email, mobile, receipt [1][4] | A breach can amplify fraud without direct system-to-system access |
| Time horizon | Main route archived since 2013 [28] | Current public portal presentation | Undated gateway terms may be historical [4] | Documentation must distinguish current, legacy, and retired paths |
| Evidence strength | High for visible flows, low for implementation | Moderate for UI, low for identity architecture | High for fields, low for callback and reconciliation | Unknowns should become authorized review questions |
| Main trade-off | Backward compatibility vs consistent modern controls | Identity convenience vs recovery and federation complexity | Payment convenience vs transaction integrity and fraud resistance | Central governance must not collapse technical isolation |

The central tension is that technical separation can coexist with social coupling. Separate cookies, databases, and networks would reduce direct lateral movement, but users may still reuse credentials or trust a message because it contains accurate academic or fee context. Conversely, a common identity provider may improve MFA and lifecycle management while increasing the importance of token audience, recovery security, conditional access, and administrative separation.

A second tension is CAPTCHA. Public and third-party evidence indicates CAPTCHA became a barrier to unofficial automation [11], yet CAPTCHA does not replace MFA, session rotation, server-side authorization, callback integrity, or abuse monitoring. It can reduce some automated login attempts while increasing accessibility and support friction. The right evaluation is control composition, not whether CAPTCHA exists.

A third tension is archival visibility. Long-lived and parallel routes help students with bookmarks and old workflows, but they can also create inconsistent policy enforcement. The evidence supports governance review, not a public exploit claim.

**Holistic conclusion:** the highest-value security work is to make hidden trust explicit. Map who authenticates whom, what data crosses each boundary, which event authorizes a payment, which ledger is authoritative, which help desk can reset which account, and how an incident in one portal changes risk decisions in the others.

## VERDICT

**Confidence level: MODERATE overall.**

| Finding area | Confidence | Verdict |
|---|---|---|
| SIS audience and role choices | High | Officially documented student/parent and administrator/faculty entry points [2] |
| Fee Kart existence and visible payment fields | High | Official pages confirm the instruction, contact fields, amount, application details, and receipt email [2][1][4] |
| Gateway names and charge table | Medium | Atom and HDFC appear on an undated page; current contractual status is unverified [4] |
| Public complaint themes | Low to medium | Anecdotes support friction signals, not prevalence, root cause, or breach [18][15][17] |
| Session implementation | Low | Timeout, cookie, rotation, and invalidation behavior are not publicly documented [3] |
| Archive and route history | High for listed evidence | Main SIS route has Wayback captures from 2013; several public `.aspx` routes remain visible [28][24][25] |
| Direct SIS-to-MUJ technical trust | Low | No public evidence proves shared sessions, passwords, databases, APIs, or signing keys |
| Cross-system fraud and identity risk | Moderate as inference | Shared users, branding, academic context, payment data, and M365 entitlement create plausible social and identity spillover [2][10][8] |

**Final verdict:** Public evidence supports a real **trust-management risk**, not a demonstrated breach or exploitable flaw. SIS is clearly an academic and payment-adjacent portal with legacy-looking public routes; MUJ SLCM is a distinct portal serving a related population; and Microsoft 365 broadens the identity context. A SIS compromise could materially increase phishing, recovery fraud, fee-payment deception, and credential-reuse risk against MUJ users. Direct lateral movement into MUJ SLCM, however, remains **unproven** and depends on private architecture facts that must be verified under authorization.

The security club should classify the ecosystem as **high impact, incomplete evidence, authorized review required**. The immediate deliverables should be a trust-boundary diagram, route inventory, payment data-flow and reconciliation map, identity/recovery matrix, approved-client policy, and incident playbook. No public-source evidence justifies unauthorized access, CAPTCHA bypass, credential testing, payment testing, or claims that either institution has been breached.

## References

1. [
	SIS
](https://sis.manipal.edu/OnlinePayment01.aspx)
2. [
	SIS Portal
](https://sis.manipal.edu/index.aspx)
3. [
	SIS
](https://sis.manipal.edu/studloginSLCM.aspx)
4. [
	Online payment
](https://sis.manipal.edu/admissions/CourseFeesMAHE02.aspx)
5. [
	Online payment
](https://sis.manipal.edu/admissions/CourseFeesMAHE01.aspx)
6. *Student Portal Login- MAHE (Manipal Academy Of Higher Education)*. https://manipal.edu/mu/academics/student-portal.html
7. *Manipal University*. https://muj.slcm.jaipur.manipal.edu/
8. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
9. *Information Security Policy*. https://manipal.edu/mu/policies/it-policy/information-security-policy.html
10. *Contents*. https://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf
11. *GitHub - canaryGrapher/slcmAPI: The API for SLcM, Manipal. Get your marks, your attendance and your profile details · GitHub*. https://github.com/canaryGrapher/slcmAPI
12. *GitHub - sankalp2004/SLCM-is-Dumb: This extracts cgpa from https://slcm.manipal.edu/ directly and passes captcha · GitHub*. https://github.com/sankalp2004/SLCM-is-Dumb
13. *GitHub - nikeplusdash/SLCM-api: An api for https://slcm.manipal.edu · GitHub*. https://github.com/nikeplusdash/SLCM-api
14. *GitHub - DK10WS/SLCM_APP: App Version for MUJ SLCM · GitHub*. https://github.com/DK10WS/SLCM_APP
15. *Reddit - The heart of the internet*. https://www.reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue
16. *Reddit - The heart of the internet*. http://reddit.com/r/manipaljaipur/comments/1m2bgru/any_one_facing_issue_with_slcm_portal
17. *Reddit - The heart of the internet*. https://www.reddit.com/r/manipal/comments/17anbg2/slcm_is_literally_ass
18. *Reddit - The heart of the internet*. https://www.reddit.com/r/Manipal_Academics/comments/1993mdc/slcm_login
19. *Authentication - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
20. *ASP.NET official support policy | .NET*. https://dotnet.microsoft.com/en-us/platform/support/policy/aspnet
21. *Internet Information Services (IIS) - Microsoft Lifecycle | Microsoft Learn*. https://learn.microsoft.com/en-us/lifecycle/products/internet-information-services-iis
22. *Session Management - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
23. *Cross-Site Request Forgery Prevention - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
24. [
	SIS
](https://sis.manipal.edu/SLCMRTGS01.aspx)
25. [
	SIS
](https://sis.manipal.edu/SLCMMessChange04Blocked.aspx)
26. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=sis.manipal.edu/studloginSLCM.aspx%26output=json%26filter=statuscode:200%26fl=timestamp,original%26collapse=digest
27. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=sis.manipal.edu/OnlinePayment01.aspx%26output=json%26filter=statuscode:200%26fl=timestamp,original%26collapse=digest
28. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=sis.manipal.edu/index.aspx%26output=json%26filter=statuscode:200%26fl=timestamp,original%26collapse=digest
