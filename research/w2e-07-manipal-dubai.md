# MAHE Dubai Student Systems: A MUJ SLCM Security Comparison

## Executive Summary

- **Official Dubai Portal Identified**: MAHE Dubai's official website links its "Student Portal" directly to `https://slcm.manipaldubai.com/` [3]. The public login page exposes a password-recovery option and a link back to the institutional site [2]. -> Treat this hostname as the authoritative public entry point for Dubai SLCM awareness, anti-phishing education, and authorized asset ownership checks.

- **Two ASP.NET Generations, Not One Proven Codebase**: Passive HTML observation indicates that Dubai uses classic ASP.NET Web Forms constructs, while MUJ exposes MVC-style anti-forgery and unobtrusive-validation constructs. The MUJ page independently confirms the student and parent login modes and the `@muj.manipal.edu` suffix [18]. -> Classify a shared backend, database, or deployment pipeline as **unproven**; resemblance at the brand or workflow layer is not proof of code equivalence.

- **Strong Dubai Product-Line Evidence**: The Android listing identifies **MAHE DUBAI-SLCM**, developer **UNIKUL Dev Team**, more than **1K downloads**, and an update date of **August 29, 2025** [4]. Its advertised functions include attendance, schedules, marks, grade sheets, GPA, teacher feedback, and announcements [4]. -> Include the mobile vendor, support channels, privacy notice, and release process in the Dubai system boundary.

- **Microsoft 365 Must Not Be Inherited Across Campuses**: The research brief supplies Microsoft 365 identity as part of the MUJ baseline, and MUJ's public page shows an institutional email suffix and password-recovery path [18]. The cleaned Dubai page, however, displays no explicit Microsoft identity-provider or SSO wording [2]. -> Verify the Dubai identity provider with the system owner before applying MUJ assumptions about federation, conditional access, password reset, or tenant boundaries.

- **Mobile Privacy Governance Needs Review**: The app listing declares that no data is collected and no data is shared with third parties [4], yet it points users to a privacy URL on `timbernile.com` rather than a MAHE Dubai domain [4]. That linked page supplies generic website terms, no contact, and no app-specific collection explanation [9]. -> Ask MAHE Dubai and UNIKUL to reconcile the app's functions, Google Play declaration, privacy notice, support ownership, and institutional data-processing terms.

- **No Attributable Dubai Cyber Incident Was Found**: This review did not identify a verified public breach, ransomware report, vulnerability disclosure, or SLCM compromise attributable specifically to MAHE Dubai. This is a bounded negative search result, not evidence that no incident occurred. -> Maintain an "unknown public incident history" classification rather than issuing a clean bill of health.

- **Policy Scope Extends Beyond Students**: MAHE states that its IT policies govern systems, networks, information, and digital assets [1], cover faculty, staff, students, and third parties across MAHE institutions [1], and include acceptable-use, information-security, and communications-security categories [1]. -> Assess vendors, mobile applications, administrators, parents, and support personnel, not only student accounts.

- **Dubai and Jaipur Require Different Compliance Runbooks**: UAE Federal Decree-Law No. 45 of 2021 contains dedicated provisions for processing controls, processor duties, breach reporting, data-protection officers, impact assessments, and cross-border transfers [13]. The UAE strategy also calls for streamlined incident detection and reporting, a standardized severity matrix, and coordinated response [8]. -> Use one technical escalation bridge across campuses, but keep jurisdiction-specific notification, evidence-retention, and regulator decision trees.

## Scope, Safety, and Evidence Method

This report is an OSINT and application-security assessment based only on public webpages, search indexes, official policies, public application-store listings, and passive inspection of HTML returned by ordinary page retrieval. It does not include credential use, form submission, account creation, brute force, automated vulnerability scanning, access-control testing, endpoint enumeration behind authentication, or attempts to bypass any control.

The focus is the publicly visible relationship among three layers:

| Evidence layer | Question answered | What it cannot prove |
|---|---|---|
| Institutional naming and links | Which portal does MAHE Dubai publicly endorse? | Who hosts the backend or which database is shared |
| Passive client-side artifacts | Which application family does the public page resemble? | Exact patch level, server version, or exploitable condition |
| Store and policy records | Who publishes the mobile app and what functions and privacy claims are advertised? | Runtime data flows, source-code quality, or independent validation of developer declarations |
| Incident and regulator sources | What has been publicly reported? | Events handled privately, unreported incidents, or sealed investigations |

The official Dubai site is the highest-confidence source for portal attribution because it links to `https://slcm.manipaldubai.com/` as its Student Portal [3]. The Google Play record is the strongest public source for the Android product's developer, advertised features, update date, support channel, and privacy URL [4]. MAHE's IT policy supplies organization-level scope, but its public overview does not state password rules, incident deadlines, or detailed cloud controls [1].

A transparency limitation is necessary: private internal chain-of-thought is not provided. In its place, each conclusion below gives a compact evidence rationale, confidence level, and explicit inference label. This is more reproducible and avoids presenting unobservable deliberation as evidence.

Confidence terms mean:

| Rating | Meaning in this report |
|---|---|
| High | Directly stated or linked by an official first-party source |
| Moderate | Supported by multiple compatible public artifacts, but important implementation details remain unverified |
| Low | A plausible hypothesis based on resemblance or absence of evidence |

No technology name, framework generation, or shared-vendor clue should be interpreted as a vulnerability. A framework becomes security-relevant only after an authorized owner establishes the exact version, configuration, exposure, and control effectiveness.

## Exact Inventory of MAHE Dubai Student-System Surfaces

The public evidence supports a small but important Dubai ecosystem rather than a single isolated login page.

| Surface | Exact URL | Publicly evidenced purpose | Authentication or ownership evidence | Confidence |
|---|---|---|---|---|
| MAHE Dubai institutional site | `https://www.manipaldubai.com/` | Official public site and source of the Student Portal link | First-party MAHE Dubai branding and institutional contacts [3] | High |
| Dubai SLCM web portal | `https://slcm.manipaldubai.com/` | Student sign-in and password recovery | Public page exposes "Forgot Password?" and a return link to the Dubai site [2] | High |
| MAHE DUBAI-SLCM Android app | `https://play.google.com/store/apps/details?id=com.unikul.manipaldubai&hl=en-US` | Attendance, schedule, marks, grades, GPA, feedback, and announcements | Published under UNIKUL Dev Team; package `com.unikul.manipaldubai` [4] | High |
| M-Campus Android app | `https://play.google.com/store/apps/details?id=com.unikul.mahedubai&hl=en-US` | Another SLCM-branded mobile experience with attendance, timetable, grades, notifications, and alerts | Published under UNIKUL Dev Team; 50+ downloads and updated August 6, 2026 [10] | High that the listing exists; moderate as to its present institutional role |
| Student policies page | `https://www.manipaldubai.com/student-policies` | Public policy navigation and institutional contact path | Repeats the official Student Portal link [16] | High |
| Student services page | `https://www.manipaldubai.com/student-services` | Public student-services navigation | Repeats the same SLCM destination [15] | High |
| How-to-apply page | `https://www.manipaldubai.com/how-to-apply` | Public admissions guidance | Also repeats the Student Portal link, but the extracted content did not identify a separate authenticated application system [17] | High for page; low for any inferred backend |
| MAHE Dubai privacy page | `https://www.manipaldubai.com/privacy-policy` | Website cookie and contact notice | States that only necessary and functional cookies are used and that no tracking, analytics, or marketing cookies are used [11] | High for the published statement, not runtime validation |
| MAHE Dubai terms | `https://www.manipaldubai.com/terms-and-conditions` | Rules for voluntarily supplied contact data and external links | Says MAHE Dubai may use supplied contact data itself or through designees, permits modification or deletion requests, and says it will not sell the data [14] | High for the published terms |

Two boundaries deserve emphasis. First, the evidence reviewed did not confirm a Dubai-specific online fee-payment endpoint. A generic MAHE payment portal found in search results should not be attributed to Dubai without an official Dubai link. Second, the public site labels admissions and enquiry pathways, but the evidence did not establish whether the underlying form is a MAHE-hosted service, a third-party admissions platform, or a simple contact workflow. Those are ownership questions for MAHE Dubai, not facts to guess from branding.

### Case study: the two UNIKUL listings

The **MAHE DUBAI-SLCM** listing reports 1K+ downloads and an August 29, 2025 update [4]. **M-Campus**, also from UNIKUL Dev Team, reports 50+ downloads and a later August 6, 2026 update [10]. Both use substantially similar SLCM language and advertise overlapping academic-record functions [10][4].

**Inference, moderate confidence:** these listings look like members of the same mobile product family or a migration/rebranding sequence. They do not prove that both are currently authorized for the same population, that they connect to the same production backend, or that either has replaced the other. The safe institutional action is to publish an authoritative app directory naming the current app, publisher, package ID, minimum version, privacy notice, and deprecation status of older packages.

## Technology and Identity: What Is Evidenced and What Is Not

The supplied research brief characterizes MUJ SLCM as ASP.NET MVC 5.3 on .NET Framework 4.x and IIS 10, behind Akamai, with Microsoft 365 identity. Those items are useful hypotheses, but the exact version, server, and CDN claims were not independently attested by an official or citable passive-scanner source in this review. They must therefore remain **client-supplied baseline assertions**, not verified findings.

The public MUJ page does independently establish the visible portal identity: "WELCOME TO MUJ PORTAL," an `@muj.manipal.edu` suffix, and student and parent login modes [18]. Passive source inspection also observed an MVC-style anti-forgery field, jQuery validation resources, and a Microsoft Online password-reset destination. **Inference, moderate confidence:** these observations are consistent with an ASP.NET MVC front end integrated with an institutional Microsoft account lifecycle. They do not prove MVC 5.3, the .NET Framework patch level, IIS 10, Akamai delivery, or that every authentication exchange is federated.

Dubai presents a different public implementation profile. Its source snapshot contained classic ASP.NET Web Forms markers, including page-state and event-validation fields, Web Forms JavaScript resources, and a local postback-style sign-in form. The visible page exposes username, password, sign-in, and password-recovery controls, while its cleaned public content does not explicitly name Microsoft, Azure AD, Entra ID, SAML, OAuth, or another external identity provider [2].

| Technical dimension | MUJ public evidence | Dubai public evidence | Assessment |
|---|---|---|---|
| Portal naming | MUJ Portal and institutional suffix [18] | SLCM is officially linked by MAHE Dubai [3] | Same business category, different public branding |
| Login roles | Student and parent modes [18] | Student-facing sign-in; no parent mode evidenced in cleaned content [2] | Workflow overlap is partial |
| ASP.NET generation | MVC-style passive artifacts observed | Web Forms-style passive artifacts observed | **Inference:** different front-end generations |
| Microsoft identity | Supplied baseline plus Microsoft password-reset observation | No explicit Microsoft identity-provider wording in cleaned page [2] | Do not assume tenant or federation equivalence |
| Exact framework and server versions | Client supplied, not independently verified | Not established | Unknown |
| CDN or edge provider | Akamai supplied in the brief, not independently verified here | Not established | Unknown |
| Mobile publisher | No public MUJ-to-UNIKUL link confirmed in targeted searches | UNIKUL Dev Team is named on both Dubai-related listings [10][4] | Strong evidence only on Dubai side |

The security implication is architectural, not exploitative. Web Forms applications often maintain server-side page state and MVC applications often use route/controller patterns, but neither pattern is intrinsically insecure. An authorized owner should validate supported framework versions, patch status, TLS and security headers, session-cookie settings, anti-CSRF enforcement, account-lockout behavior, and error handling through internal review or a formally scoped assessment. A university club should not test those controls against production without written authorization.

## Three Layers of Family Resemblance to MUJ SLCM

"Family resemblance" should be separated into institutional, product, and technical layers. Collapsing them into a single yes/no conclusion would overstate the evidence.

| Resemblance layer | Supporting evidence | Counterevidence or gap | Conclusion |
|---|---|---|---|
| Institutional family | Both are Manipal-affiliated student portals; the Dubai site officially links an SLCM service [3], while MUJ identifies its own portal and email suffix [18] | MUJ is a separate Jaipur institution and Dubai operates in a different jurisdiction | Strong branding and business-process resemblance |
| Functional family | Dubai mobile apps advertise attendance, schedules, marks, grades, GPA, feedback, and announcements [10][4] | The unauthenticated MUJ page does not publicly enumerate post-login functions | Moderate functional resemblance, partly based on the common SLCM category |
| Vendor/product family | Dubai apps name UNIKUL Dev Team [10][4] | Targeted public searches did not establish that UNIKUL operates MUJ's portal | Strong for Dubai, unproven across Dubai and MUJ |
| Front-end technology | Both public portals are in the Microsoft web-application ecosystem by passive appearance | Dubai resembles Web Forms; MUJ resembles MVC | Resemblance at platform family, divergence at application generation |
| Identity | MUJ displays `@muj.manipal.edu` and separate login roles [18] | Dubai does not publicly identify Microsoft federation or an equivalent email suffix [2] | Identity equivalence is unproven |
| Shared backend or database | None in the public evidence | No citable architecture diagram, vendor contract, network statement, or data-flow notice | Unknown; do not infer |
| Shared incident history | None found | Public silence is incomplete evidence | Unknown |

### Case study: visual and functional similarity versus implementation divergence

An analyst looking only at names could reasonably group `mujslcm.jaipur.manipal.edu`, `slcm.manipaldubai.com`, and `slcm.manipal.edu` into one SLCM family. The Dubai and main MAHE pages also expose similarly simple sign-in and password-recovery experiences; the main MAHE SLCM page presents the same confirmation-style recovery interaction [12].

The implementation artifacts complicate that picture. The Dubai page looks like classic Web Forms, while MUJ looks like a more modern MVC front end. **Inference, moderate confidence:** MAHE may have retained a common student-lifecycle concept while campuses adopted different releases, customizations, or integration layers. That is common in long-lived university systems, but the public evidence cannot distinguish a shared product with separate skins from unrelated applications using the same SLCM label.

The decision-ready consequence is to model the ecosystem as **related but independently governed**. Reuse threat models and control requirements across campuses, but do not reuse conclusions about versions, identity tenants, vulnerabilities, session behavior, or remediation status without campus-specific evidence.

## Public Incident Record and Defensive Threat Cases

No verified public report reviewed for this assignment named MAHE Dubai or `slcm.manipaldubai.com` as the victim of a breach, ransomware event, exposed database, account compromise, or publicly disclosed application vulnerability. Searches covered combinations of the institution name, portal hostname, SLCM, breach, ransomware, vulnerability, outage, regulator, and incident terminology. Official UAE sources were also reviewed for incident-response context.

This result must be stated narrowly. It means **no attributable report was identified in the reviewed public corpus as of August 25, 2026**. It does not mean there was no incident, no private notification, no student account takeover, no fraud, and no availability outage. Many educational incidents are resolved internally, reported only to affected people or regulators, or described without naming the affected system.

The UAE's national strategy calls for a coordinated incident-response plan that streamlines detection and reporting, uses a standardized severity matrix, and builds response capability [8]. TDRA's aeCERT page describes monitoring and response based on threat, incident, and vulnerability data, as well as vulnerability-assessment services [7]. Those sources provide national context, not evidence of a MAHE Dubai event.

| Defensive threat case | Publicly visible condition | Potential impact | Safe club activity |
|---|---|---|---|
| Credential phishing | A recognizable SLCM sign-in brand and password-recovery workflow are public [2] | Theft of student credentials or redirection to a look-alike portal | Publish the exact official hostname and teach students to use bookmarks; do not create realistic credential-collection simulations without approval |
| Identity-boundary confusion | MUJ visibly uses an institutional suffix [18], while Dubai's provider is not stated [2] | Students may trust the wrong recovery path or disclose credentials to unofficial support | Ask IT to publish official login and recovery URLs for each campus |
| Mobile-app ambiguity | Two UNIKUL listings advertise overlapping SLCM functions [10][4] | Installation of an obsolete or unintended app; fragmented patch and support coverage | Request an authoritative supported-app list and deprecation notice |
| Academic-record exposure | The apps advertise marks, attendance, GPA, feedback, and announcements [10][4] | Privacy, integrity, and availability consequences if an account or API is compromised | Build a data-classification and incident tabletop using synthetic records only |
| Third-party privacy mismatch | The app points to a generic external privacy page [4][9] | Confusion over controller, processor, contact, retention, and deletion responsibility | Perform a document review and request an app-specific notice; do not inspect private traffic |
| Silent outage or account issue | No public status page or incident archive was identified | Students cannot distinguish a service outage from an account compromise | Recommend a status page and authenticated support process |

### Case study: privacy declaration tension without overclaiming

The MAHE DUBAI-SLCM listing says that no data is shared with third parties and no data is collected [4]. The same listing advertises access to attendance, schedules, marks, grade sheets, GPA, feedback, and announcements [4]. These statements are not automatically contradictory: an app may display institution-controlled data without the developer treating it as collection under a store taxonomy.

The governance weakness is that the linked privacy page does not explain those distinctions. It contains generic website-use terms, disclaims responsibility for external sites, names UAE law, and supplies no contact [9]. **Inference, high confidence:** the public documentation is insufficient for a reader to understand which entity controls student records, what the app transmits, where support data goes, how deletion requests work, or whether telemetry exists. The appropriate response is documentation and vendor assurance, not reverse engineering or interception of student traffic.

## Privacy, Governance, and Jurisdiction

MAHE's institutional policy overview says its IT policies govern the use and security of computing systems, networks, information, and digital assets [1]. It covers faculty, staff, students, and third parties across MAHE institutions [1], and states that users must comply with applicable policies [1]. This broad scope supports treating UNIKUL, mobile support channels, administrators, and other service providers as part of the governance boundary.

The Dubai website's public privacy content is narrower. It states that only strictly necessary and functional cookies are used and that no tracking, analytics, or marketing cookies are used [11]. Its terms say voluntarily supplied name, email, physical address, telephone number, or other data may be used by MAHE Dubai or its designees to communicate with the person [14]. Users may request modification or deletion, and the institution says it will not sell that information [14]. These are useful website statements, but they are not a complete student-record or SLCM privacy notice.

| Governance topic | Public source | What the source establishes | Remaining question |
|---|---|---|---|
| Institutional IT scope | MAHE IT policy | Systems, networks, information, digital assets, users, and third parties are covered [1] | Which detailed policy and incident procedure applies to Dubai? |
| Dubai website cookies | MAHE Dubai privacy page | Necessary and functional cookies only; no tracking, analytics, or marketing cookies claimed [11] | Has runtime behavior been audited against the statement? |
| Contact information | MAHE Dubai privacy page | `info@manipaldubai.com`, `admissions@manipaldubai.com`, and institutional telephone numbers [11] | Which contact handles privacy incidents or security reports? |
| Voluntary contact data | Dubai terms | Communications use by MAHE Dubai or designees, modification/deletion requests, and no sale [14] | Does this cover SLCM and mobile academic records? |
| Processor duties and breach reporting | UAE PDPL | Dedicated provisions exist for processor obligations and personal-data breach reporting [13] | Which entity is controller and which is processor for each app and portal? |
| DPO and impact assessment | UAE PDPL | Dedicated DPO and impact-assessment provisions exist [13] | Has the Dubai SLCM/mobile processing been assessed under applicable thresholds? |
| Cross-border processing | UAE PDPL | Dedicated rules address transfers with and without an adequate protection level [13] | Where are SLCM, support, backups, analytics, and vendor access located? |
| National incident coordination | UAE strategy and TDRA | Detection, reporting, severity assessment, response, intelligence, and assessment services [8][7] | What is MAHE Dubai's internal escalation path before external reporting? |

For MUJ, the operating and reporting context is Indian rather than UAE. The CERT-In directions are issued under Section 70B of India's Information Technology Act and address information-security practices, prevention, response, and reporting [5]. This report does not assume that an Indian deadline automatically applies to Dubai or vice versa.

**Inference, high confidence:** a shared technical incident can create two legal workstreams. For example, if a common vendor or identity integration affects both campuses, the technical containment team may be unified while notification analysis, regulator engagement, cross-border evidence handling, and student communications remain jurisdiction-specific.

## Authorized Security-Club Action Plan

The following plan is intentionally non-intrusive. Any dynamic assessment of production must be initiated by the asset owner under written rules of engagement, named targets, approved test windows, data-handling rules, and an emergency stop process.

| Priority | Action | Owner | Evidence or deliverable | Authorization boundary |
|---|---|---|---|---|
| 1 | Publish the canonical web and mobile directory | MAHE Dubai IT and communications | Exact SLCM URL, current app title, package ID, publisher, support contact, and retired-app list | Public documentation only |
| 2 | Establish asset and vendor ownership | IT governance and procurement | Named business owner, technical owner, UNIKUL contract owner, hosting owner, identity owner, and privacy owner | Internal records review |
| 3 | Resolve identity ambiguity | Identity team | Written statement of Dubai identity provider, tenant, MFA policy, recovery process, and parent/support-account model | Configuration review by administrators only |
| 4 | Reconcile mobile privacy records | Privacy, legal, and UNIKUL | App-specific notice covering controller, processor, categories, purposes, retention, transfers, deletion, security contact, and SDKs | Document and code-owner review; no interception of user traffic |
| 5 | Validate technology inventory | Authorized application owner | Exact framework, runtime, server, CDN, WAF, libraries, support dates, and patch status | Internal configuration and software-composition analysis |
| 6 | Review authentication controls | Authorized security team | MFA coverage, lockout, password reset, session lifetime, cookie flags, CSRF protection, and privileged-account controls | Staging first; production only under written scope |
| 7 | Build an incident matrix | Security, privacy, legal, student affairs | Severity levels, internal contacts, UAE decision points, Jaipur decision points, vendor SLA, evidence custody, and communications templates | Tabletop exercise using synthetic data |
| 8 | Create a status and disclosure channel | IT and communications | Public status page, security contact, intake acknowledgement, safe-harbor language, and escalation SLA | Governance action, not testing |
| 9 | Run student anti-phishing education | Security club with IT approval | Canonical-hostname card, mobile-app verification guide, reporting path, and recovery checklist | No credential harvesting or realistic impersonation without formal approval |
| 10 | Reassess annually and after major changes | Governance committee | Dated evidence register, app-store review, vendor attestation, privacy update, and deprecation review | Passive OSINT plus authorized internal assurance |

A useful first deliverable is a one-page "Know Your Official SLCM" card. It should identify `https://slcm.manipaldubai.com/` as the Dubai web entry point, list the currently supported app and package ID, state that staff will never request passwords, and provide an institutional incident contact. The official site already supplies general and admissions contacts [11], but the reviewed public pages do not identify a dedicated security or privacy incident mailbox.

A second deliverable is a synthetic-data tabletop. A scenario might state that students report unexpected grade changes and phishing messages after a mobile release. Participants would decide how to distinguish account compromise from application error, contact the vendor, preserve logs, assess personal-data impact, notify leadership, and communicate with students. No real accounts, credentials, or student records are needed.

## Synthesis: Related Ecosystem, Separate Trust Decisions

The evidence supports a nuanced conclusion. MAHE Dubai and MUJ clearly occupy the same broad institutional and student-lifecycle domain. Both expose branded portals with sign-in and recovery concepts, and the Dubai mobile apps implement the familiar SLCM functions of attendance, scheduling, marks, grades, feedback, and announcements [10][4]. That is enough to reuse high-level threat categories such as credential theft, academic-record integrity, vendor access, and availability.

It is not enough to reuse technical findings. The MUJ page exposes student and parent modes and an institutional email suffix [18]. Dubai's public page does not expose an equivalent Microsoft identity statement [2]. Passive artifacts also place the two pages in different ASP.NET generations. **Inference, moderate confidence:** the systems probably share concepts and perhaps product ancestry, but their front ends, integrations, and upgrade paths have diverged.

| Dimension | MUJ | MAHE Dubai | Integrated conclusion |
|---|---|---|---|
| Mechanism | MVC-style portal plus supplied Microsoft 365 baseline | Web Forms-style portal plus UNIKUL mobile applications | Similar service objective, different evidenced implementation |
| Scope | Student and parent login modes [18] | Student web portal plus multiple mobile listings [3][10][4] | Dubai's publicly visible mobile supply chain is broader |
| Evidence base | Official portal content; exact versions supplied but not independently verified | Official link, login page, store records, website terms, UAE law | Dubai claims can be made more specifically from public evidence |
| Principal trade-off | Centralized institutional identity can improve control but concentrates account risk | Local-looking portal and vendor apps may increase integration and documentation complexity | Do not choose controls by appearance; verify ownership and data flow |
| Time horizon | Exact upgrade and support history unknown | One app updated in 2025 and another in 2026 [10][4] | App migration or coexistence requires owner clarification |
| Incident evidence | Not the primary focus of this report | No attributable public incident identified | Public silence should trigger readiness, not complacency |
| Legal context | Indian cyber and data obligations | UAE PDPL and national incident-response context [8][13] | Shared technical bridge, separate legal decision trees |

The most important non-obvious tension is between **strong functional resemblance** and **weak architectural proof**. The same SLCM vocabulary and student workflows can arise from a common vendor, historical product family, campus customization, or merely a generic university label. Conversely, visibly different Web Forms and MVC front ends can still call common services. Public presentation alone cannot resolve the topology.

The second tension is between **mobile functionality** and **privacy transparency**. The app-store pages describe rich access to academic records but declare no data collection or sharing [10][4]. That may be technically valid under store definitions, yet the external privacy page does not explain the processing model [4][9]. The remedy is a precise, institution-approved notice and vendor data-flow inventory.

The third tension is between **no public incident report** and **non-zero risk**. The absence of a named report lowers confidence in any historical claim, but it does not reduce the sensitivity of credentials, attendance, grades, or student contact data. Readiness should be based on asset value and credible threat cases, not on whether an incident has reached the press.

## VERDICT

| Question | Verdict | Confidence |
|---|---|---|
| Is `slcm.manipaldubai.com` an official MAHE Dubai student portal? | **Yes.** The official institutional site links it as "Student Portal" [3]. | High |
| Does MAHE Dubai have a publicly identifiable SLCM mobile ecosystem? | **Yes.** MAHE DUBAI-SLCM and M-Campus are public UNIKUL Dev Team listings with overlapping student-lifecycle functions [10][4]. | High |
| Is Dubai technologically identical to MUJ SLCM? | **Not established.** Passive artifacts indicate Web Forms for Dubai and MVC-style behavior for MUJ. | Moderate confidence that they differ at the public front-end layer; low confidence about backend relationships |
| Does Dubai publicly prove Microsoft 365 identity integration? | **No.** The public cleaned login content does not name Microsoft or an external identity provider [2]. | Moderate |
| Are ASP.NET MVC 5.3, .NET 4.x, IIS 10, and Akamai independently verified for MUJ here? | **No.** They remain supplied baseline assertions, not independently corroborated version findings. | High |
| Is there a verified public MAHE Dubai cyber incident? | **None identified in this review.** This is not proof that none occurred. | Moderate confidence in the bounded search result; low confidence about complete historical absence |
| Is there meaningful family resemblance? | **Yes at institutional, workflow, and broad Microsoft-web-platform levels; unproven at vendor, database, identity-tenant, and shared-backend levels.** | Moderate-high |
| What is the leading security priority? | **Clarify asset ownership, identity architecture, current mobile-app status, privacy processing, and incident contacts before deeper testing.** | High |

**Final verdict: MODERATE-HIGH CONFIDENCE.** MAHE Dubai operates an official SLCM web portal and a clearly attributable UNIKUL mobile product family. It resembles MUJ SLCM strongly in purpose and institutional context, but public evidence does not justify calling it the same application, deployment, identity tenant, database, or security boundary. The Dubai Web Forms evidence and MUJ MVC-style evidence instead suggest separate application generations or implementations.

For the university security club, the responsible path is documentation, phishing-resistance education, synthetic-data tabletop exercises, and owner-approved assurance. Do not scan, submit crafted inputs, test credentials, intercept mobile traffic, or probe authenticated functions without written authorization.

## References

1. *IT Policies*. https://www.manipal.edu/mu/policies/it-policy.html
2. [

](https://slcm.manipaldubai.com/)
3. *Manipal University Dubai | CAA-Accredited International University in UAE*. https://www.manipaldubai.com/
4. *MAHE DUBAI-SLCM - Apps on Google Play*. https://play.google.com/store/apps/details?id=com.unikul.manipaldubai&hl=en-US
5. *http://cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf*. http://cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf
6. *United Arab Emirates Legislations | Federal Decree by Law Concerning the Protection of Personal Data*. https://www.uaelegislation.gov.ae/en/legislations/1972
7. *Home - TDRA*. https://tdra.gov.ae/en/aecert
8. *National Cybersecurity strategy 2019  | The Official Platform of the UAE Government*. https://u.ae/en/about-the-uae/strategies-initiatives-and-awards/strategies-plans-and-visions/strategies-plans-and-visions-untill-2021/national-cybersecurity-strategy-2019
9. *Privacy Policy*. https://timbernile.com/privacy%20policy.php
10. *M-Campus - Apps on Google Play*. https://play.google.com/store/apps/details?id=com.unikul.mahedubai&hl=en-US
11. *Privacy Policy*. https://www.manipaldubai.com/privacy-policy
12. [
	MU SLcM
](https://slcm.manipal.edu/)
13. *Federal Decree by Law No. (45) of 2021 Concerning the Protection of Personal Data*. https://www.uaelegislation.gov.ae/en/legislations/1972/download
14. *Terms & Conditions*. https://www.manipaldubai.com/terms-and-conditions
15. *Student Services*. https://www.manipaldubai.com/student-services
16. *Manipal Dubai Student Policies | Academic & Campus Guidelines*. https://www.manipaldubai.com/student-policies
17. [How to Apply for Manipal University Dubai Admissions
](https://www.manipaldubai.com/how-to-apply)
18. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
