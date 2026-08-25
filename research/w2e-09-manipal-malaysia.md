# MIU SLCM Public Footprint and Shared-Codebase Verdict

## Executive Summary

- **Entity Attribution Is The First Security Finding**: Malaysia's qualifications register identifies MILA University as "Previously known as: Manipal International University (MIU)" and places it at Persiaran MIU in Putra Nilai [12]. Meanwhile, the operational helpdesk under `manipal.edu.my` identifies itself as "MUCM Helpdesk" [7]. -> Treat `student.manipal.edu.my` as a Manipal Malaysia portal whose current institutional owner must be confirmed internally; do not automatically equate it with the former MIU in Nilai.

- **The Malaysian Portal Is Publicly Reachable But Reveals Little Branding**: The login surface exposes student sign-in using a "Scholar E-Mail ID," a separate parent username/password flow, forgot-password functionality, and self-registration [5]. -> This is enough to map public user journeys, but not enough to identify the back-end framework, tenant, or current legal operator.

- **The Registration Surface Collects Identity Data**: Publicly rendered fields include username, first name, last name, email, phone number, password confirmation, and agreement to terms [1]. -> Because the workflow handles personal data before an authenticated session exists, ownership, privacy notice, consent text, abuse controls, and data-retention behavior deserve priority review.

- **Microsoft-Oriented Login Does Not Prove Microsoft 365 Architecture**: The public page labels the student flow "Scholar E-Mail ID" [5], and the served markup displays a Microsoft-branded button. -> This supports a Microsoft-oriented sign-in hypothesis, but it does not prove a particular Entra tenant, protocol, MFA policy, or any relationship to MUJ's Microsoft 365 configuration.

- **Presentation-Layer Divergence Is Stronger Than Code-Reuse Evidence**: MUJ presents "WELCOME TO MUJ PORTAL" and a parent-login choice [2], while Malaysia exposes `/auth/registration`, a client-rendered shell, and a generic portal presentation [5][1]. -> The sites may belong to one SLCM product family, but the public evidence does not establish an identical deployment or shared source tree.

- **Complaint Evidence Is Sparse And Geographically Misleading**: The one attributable public complaint located in this review is titled "Slcm portal issue," concerns Manipal Jaipur, and reports a correct password being rejected; no resolution is visible [11]. -> Do not mislabel it as Malaysian evidence, and do not interpret the lack of indexed Malaysia complaints as proof that the portal is reliable.

- **Analytics Creates A Concrete Governance Question**: Microsoft describes Clarity as behavior analytics with session recordings, heatmaps, and machine-learning insights [27]. Microsoft also says Clarity should not be used on sites or apps targeting users under 18 [27]. -> Confirm whether analytics runs only on the public login shell, whether any Malaysian users are minors, and whether strict masking and institutional notice requirements are satisfied.

- **The Correct Security Response Is Verification, Not Internet Testing**: NIST says AAL2 applications must offer a phishing-resistant option, while OTP is not phishing-resistant [23]. OWASP calls for full-session TLS, secure cookies, session renewal after privilege changes, server-side expiration, and session-event logging without logging raw session IDs [20]. -> Conduct an owner-authorized assessment in staging, backed by source review and identity-policy review; do not probe the production portal without written authorization.

## 1. Scope, Method, And Evidence Boundaries

This report examines public information about `https://student.manipal.edu.my/`, compares that surface with the MUJ SLCM ecosystem, and assesses what can and cannot be inferred about shared code. It uses only ordinary public pages, indexed search results, published client-side markup, official regulatory material, public documentation, and one public discussion. It does not use credentials, submit registration data, test passwords, enumerate accounts, invoke hidden APIs, scan ports, fuzz routes, bypass authentication, or attempt exploitation.

The MUJ stack description in the brief - ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 identity - is treated as a **user-supplied baseline**, not as a newly verified result. The central question is whether the Malaysian portal independently demonstrates the same implementation. It does not.

A requested private chain-of-thought transcript is not provided. Instead, the report supplies the reproducible form that an OSINT review actually needs: source observation, bounded inference, alternatives, confidence, and a decision consequence.

| Evidence class | What was examined | What it can support | What it cannot support |
|---|---|---|---|
| Direct public UI | Login labels, registration fields, role choices, visible routes [5][1] | Public workflows and data requested before login | Server framework, authorization correctness, or vulnerability status |
| Public markup | Root container, static asset naming, Microsoft-branded control, and analytics references at the exact portal URL | Front-end architecture hypotheses and third-party service presence | Secret configuration, back-end language, or tenant ownership |
| Regulatory and institutional pages | MQA's former-name record and Manipal's historical description [12][10] | Entity disambiguation and historical context | Current ownership of every legacy subdomain |
| Public support material | MUCM-branded ticket workflow [7] | Current support identity on the same parent domain | Proof that every `manipal.edu.my` host serves MUCM |
| Public complaints | One Jaipur post reporting a password error [11] | A narrowly scoped user report | Root cause, prevalence, exploitability, or Malaysia impact |
| Security standards | NIST, OWASP, Microsoft, Malaysian PDPA, and Akamai documentation [23][18][20][21] | A defensive verification checklist | Proof that the live portals pass or fail any control |

The key methodological rule is simple: a common name, logo, or business function establishes relationship at the product or organizational level only weakly. Shared binaries, repositories, release identifiers, API schemas, deployment manifests, or synchronized defects would be much stronger evidence. None of those stronger artifacts was established here.

## 2. Malaysia Entity Attribution: Former MIU Is Now MILA

Entity resolution materially changes the interpretation of the hostname. The Malaysian Qualifications Register lists **MILA University** as previously known as **Manipal International University (MIU)** [12]. The same regulatory record gives the location as `1, Persiaran MIU, 71800 Putra Nilai, Negeri Sembilan` [12]. A Manipal institutional page describes the historical MIU as a member of the Manipal Global Education Group offering multidisciplinary programs focused on science and engineering, management, and business [10].

The operational support site under the different but related `manipal.edu.my` namespace calls itself **MUCM Helpdesk** [7]. It provides a support-ticket system, unique ticket numbers, online response tracking, archives of prior requests, and requires a valid email address [7]. This is evidence of a current MUCM support operation on the parent domain, but it is not a conclusive ownership record for the student subdomain.

| Malaysian entity or artifact | Direct evidence | Security interpretation |
|---|---|---|
| Former Manipal International University, Nilai | MQA says MILA University was previously Manipal International University [12] | References to "MIU Malaysia" may describe a historical institution rather than the current portal operator |
| Historical MIU business profile | Manipal describes MIU as multidisciplinary, with science, engineering, management, and business programs [10] | This profile differs from the MUCM label now exposed by the support service |
| `helpdesk.manipal.edu.my` | The service identifies itself as MUCM Helpdesk [7] | Strong evidence that MUCM operates at least part of the current parent namespace |
| `student.manipal.edu.my` | The public login uses generic portal wording and "Scholar E-Mail ID" rather than an explicit institution name [5] | The login page alone does not resolve whether stewardship is MUCM, a legacy Manipal service, or a shared central team |
| MQA location | The former MIU/MILA record points to Putra Nilai, Negeri Sembilan [12] | Location should be checked against the population using the portal before attributing incidents or complaints |

**Inference - moderate confidence:** The namespace and MUCM helpdesk make current MUCM stewardship of `student.manipal.edu.my` plausible. That remains an inference because the login page does not explicitly say MUCM, and the former MIU has a regulator-documented successor identity. A university security club should therefore label the target "Manipal Malaysia SLCM at `student.manipal.edu.my`" until the institution confirms ownership.

This is not pedantry. A mistaken entity label can send vulnerability reports, privacy questions, or incident notifications to the wrong legal entity. It can also cause false correlations between complaints made by students in Nilai, Melaka, Jaipur, Manipal, or Dubai. The first recommended action is administrative: ask the university's IT or security owner to confirm the service owner, data controller, support queue, and authorized disclosure channel.

## 3. Public Portal Behavior And Data Flows

The unauthenticated login journey is compact. The page offers "Create an Account," identifies a student sign-in path, labels the student identifier "Scholar E-Mail ID," and presents a separate parent flow with username, password, forgot-password, and continue controls [5]. These labels establish at least two user populations and two authentication experiences. They do not show whether both flows terminate in the same identity service or application session.

The registration path is more consequential. It asks for username, first name, last name, email, phone number, and password confirmation [1]. It displays the instruction, "Use 8 or more characters with a mix of letters, numbers & symbols," and requires agreement to terms before submission [1]. The wording is a user-interface prompt; it is not evidence that server-side validation, breached-password screening, rate limiting, proofing, email verification, or duplicate-account controls are effective.

| Public workflow | Exact visible elements | Direct conclusion | Security question for the owner |
|---|---|---|---|
| Student login | "Sign in as Student" and "Scholar E-Mail ID" [5] | Students use an email-oriented identifier | Which identity provider, tenant, protocol, and MFA policy are authoritative? |
| Parent login | "Sign in as Parent," username, password, forgot-password, continue [5] | A password-based non-student path exists publicly | Are parent accounts separately governed, rate-limited, and revoked when relationships end? |
| Account creation | "New Here? Create an Account" [5] | Self-service registration is intentionally discoverable | Who is eligible, and how is identity or invitation status verified? |
| Registration identity data | Username, first name, last name, email, and phone number [1] | The public form requests personal and contact data | Is the data controller named, and what are purpose, retention, correction, and deletion rules? |
| Password prompt | Confirmation plus an 8-character mixed-character message [1] | A composition rule is communicated | Is the rule enforced server-side, and does the policy support password managers and compromised-password blocking? |
| Consent control | Agreement to terms plus submit/cancel controls [1] | Acceptance is part of registration | Are the exact terms accessible, versioned, recorded, and suitable for Malaysian users? |

**Inference - high confidence:** This is not merely a static information page. It is the public entry point to identity-related workflows and personal-data collection. The risk concentration is therefore at authentication, registration, password recovery, role assignment, session establishment, and data governance - not at the cosmetic landing page.

**Inference - moderate confidence:** The separate student and parent experiences suggest that SLCM models role-specific identity. That pattern also appears at MUJ, whose public page identifies itself as "WELCOME TO MUJ PORTAL" and exposes a parent-login option [2]. Similar roles are consistent with a shared product concept, but common university requirements can independently produce the same design.

The existence of a public registration route is not itself a defect. It becomes a security concern only if authorization, verification, abuse controls, or data handling are inadequate. No such inadequacy was demonstrated by this public-only review.

## 4. Technology Assessment: What Is Visible And What Is Not

The Malaysian site differs visibly from the MUJ baseline supplied in the brief. Publicly served markup for the Malaysian login contains a client-side root container and hashed `main` JavaScript and CSS assets, a pattern consistent with a compiled single-page application. The page's structure uses Bootstrap-like classes and `kt_`-style component identifiers. **Inference - moderate confidence:** this is likely a React-style front end built from a commercial dashboard or portal theme. The evidence supports a front-end hypothesis, not a back-end identification.

The student control is Microsoft-branded in the served markup, while the visible text says "Scholar E-Mail ID" [5]. **Inference - moderate confidence:** the student path probably delegates to a Microsoft-oriented identity flow. It could be Entra ID, another Microsoft-backed broker, or a custom flow using Microsoft branding. No public tenant identifier, authority URL, signed-token metadata, or completed redirect was collected, so this report does not claim Microsoft 365 tenant parity with MUJ.

The markup also references Microsoft Clarity. Microsoft describes Clarity as a user-behavior analytics service with session recordings, heatmaps, and machine-learning insights [27]. Microsoft says website owners control content sent to Clarity and should use dashboard settings to block confidential content [27]. It also states that Clarity should not be used on websites or apps targeting users under 18 [27].

| Technology question | Malaysia public evidence | Assessment | Confidence |
|---|---|---|---|
| Client architecture | Compiled static assets and a client-rendered root at the exact login URL | Modern single-page front end is likely | Moderate |
| Microsoft identity | Microsoft-branded student button plus "Scholar E-Mail ID" [5] | Microsoft-oriented SSO is plausible; tenant and protocol are unverified | Moderate |
| Parent authentication | Username/password and forgot-password controls [5] | A local or separately brokered password flow exists | High for UI, low for back end |
| Analytics | Public markup references Clarity; Microsoft documents recordings, heatmaps, and ML insights [27] | Privacy configuration and age suitability require owner review | High for service reference, unknown for captured data |
| Registration framework | Public route `/auth/registration` and client-rendered form [1] | Front-end routing differs from MUJ's `/Home/Index` presentation | High |
| ASP.NET MVC 5.3 | No direct Malaysian evidence located | Do not transfer the MUJ version claim to Malaysia | Low/unknown |
| .NET Framework 4.x | No direct Malaysian evidence located | A SPA can call any of several back-end stacks | Unknown |
| IIS 10 | No direct Malaysian evidence located | Edge behavior cannot establish the origin server | Unknown |
| Akamai | No direct Malaysian evidence located in this review | Do not assume Malaysia shares MUJ's delivery tier | Unknown |
| Shared Microsoft tenant | No tenant-specific evidence collected | Common branding does not prove tenant sharing | Unknown |

A front-end/back-end split is entirely possible: a React-style shell could call an ASP.NET API. It could also call Java, Node.js, PHP, Salesforce, or another service. **Inference - high confidence:** front-end modernization can coexist with legacy business logic, but the public page does not tell us which arrangement applies here.

Akamai documentation says its WAF behavior blocks threatening HTTP and HTTPS requests [14]. Even if MUJ is behind Akamai, that is an edge-control statement rather than proof of secure application logic. A WAF cannot establish correct student-versus-parent authorization, safe object access, appropriate registration eligibility, secure session invalidation, or privacy compliance. The Malaysia deployment's edge controls remain unverified.

## 5. Public Complaints: One Jaipur Report, No Malaysia Corpus

The search for public complaints produced a significant negative result: no reliable, attributable complaint about `student.manipal.edu.my` or the Malaysia SLCM workflow was located in the indexed sources reviewed. That is a statement about this review's evidence set, not a claim that complaints do not exist.

The only narrowly attributable SLCM complaint located is a Reddit post titled "Slcm portal issue" concerning Manipal Jaipur. It says the user's password shows an error despite being correct, and no resolution is visible in the retrieved discussion [11]. This report does not treat the user's belief that the password was correct as technical proof. Possible explanations include an outage, stale credentials, account state, user error, identity synchronization delay, lockout, or application failure.

| Complaint evidence | Campus | Reported issue | Resolution | Permissible conclusion |
|---|---|---|---|---|
| Reddit post, "Slcm portal issue" [11] | Manipal Jaipur [11] | Password reported as rejected despite being correct [11] | None visible [11] | One user reported an authentication problem; root cause and prevalence are unknown |
| Indexed Malaysia-specific complaints | Malaysia portal | None reliably located in this review | Not applicable | Absence of indexed evidence is not evidence of absence |
| MUCM helpdesk | Parent domain support service | Ticketing exists, but tickets are not publicly readable [7] | Private to users/support | Operational complaints may be concentrated in a non-public channel |

The MUCM helpdesk's design helps explain why open-web complaint volume may be low. It assigns unique ticket numbers, supports online tracking, and preserves a request history for users [7]. **Inference - moderate confidence:** service problems may be handled privately instead of appearing in search results. The same mechanism also means an external OSINT analyst cannot responsibly estimate incident frequency from public material.

For the security club, the right next evidence source is not more aggressive probing. It is an authorized, privacy-preserving review of aggregated helpdesk categories: login failures, password recovery, account activation, parent access, registration errors, and outage duration. Aggregate counts and time-to-resolution can reveal operational risks without exposing student tickets.

## 6. What The Malaysia Instance Says About A Shared SLCM Codebase

The evidence supports a **shared product family** more strongly than it supports a **shared codebase**. Several Manipal-affiliated services use the SLCM or SLcM label, including the public MAHE page titled "MU SLcM" [4]. Malaysia exposes student and parent identities [5], and MUJ exposes a portal-branded login with a parent role [2]. These are real similarities.

However, the implementation signals diverge. Malaysia uses `/auth/...` routes, a client-rendered shell, hashed static assets, public account creation, and Microsoft-oriented student sign-in. MUJ presents a `/Home/Index` style entry point and the "WELCOME TO MUJ PORTAL" branding [2]. The supplied MUJ baseline describes classic ASP.NET MVC on .NET Framework and IIS, while the Malaysian back end is unknown.

| Comparison dimension | Malaysia `student.manipal.edu.my` | MUJ `mujslcm.jaipur.manipal.edu` | Shared-code implication |
|---|---|---|---|
| Product name and purpose | SLCM student portal context | MUJ SLCM ecosystem | Supports a common business/product family |
| Public branding | Generic sign-in presentation; institution not explicit [5] | "WELCOME TO MUJ PORTAL" [2] | Suggests campus-specific presentation |
| Student identity | Scholar email-oriented flow [5] | Microsoft 365 identity is supplied in the brief, not independently reverified here | Possible common identity strategy, not tenant proof |
| Parent identity | Username/password and forgot password [5] | Parent-login role is public [2] | Shared role model is plausible |
| Self-registration | Public account-creation and registration path [5][1] | Not established from the retrieved MUJ page | Potentially different onboarding policy or release branch |
| Front-end delivery | Client-rendered compiled shell, based on public markup | Server-rendered Keen-style presentation, based on public markup | Strong evidence of front-end divergence |
| Back-end stack | Unknown | ASP.NET MVC 5.3/.NET 4.x/IIS 10 supplied by the requester | No basis for version inheritance |
| Edge/CDN | Not established | Akamai supplied by the requester | No basis for shared edge policy |
| Current entity | Ambiguous between current MUCM namespace and legacy Manipal history | MUJ branding is explicit [2] | Central governance may coexist with distinct legal operators |

### Auditable evidence-to-conclusion reasoning

| Observation | Alternative explanations | Bounded inference | Confidence |
|---|---|---|---|
| Both surfaces serve student lifecycle functions and expose parent-related access [5][2] | Universities often need these roles independently | Common functional specification or product lineage is plausible | Moderate-high |
| Malaysia and MUJ use different route structures and rendering patterns | A single product can have multiple front ends or versions | Identical deployed front-end code is unlikely | High |
| Malaysia shows a Microsoft-oriented student path [5] | Branding could front a broker or custom integration | Microsoft identity involvement is plausible; shared tenant is not established | Moderate |
| Malaysia has self-registration [5][1] | The route may serve admissions or invitation-based onboarding | Onboarding policy differs or is exposed differently | Moderate |
| Former MIU is regulator-listed as MILA, while the domain helpdesk says MUCM [12][7] | Legacy domains may have been reassigned within the group | Portal governance may have changed over time | Moderate |
| No shared release identifiers, API schemas, or repository artifacts were found | Such artifacts may be private | Common source code cannot be demonstrated from public evidence | High |

**Inference - moderate-high confidence:** "SLCM" appears to be an institutional product umbrella or family used across Manipal environments. **Inference - moderate confidence:** deployments likely share requirements, terminology, or integration patterns. **Inference - low confidence:** they share the same back-end repository, framework version, deployment pipeline, database, Entra tenant, or vulnerability set.

This distinction matters for vulnerability propagation. A defect found in one campus should become a hypothesis for authorized regression testing elsewhere, not a public accusation that every SLCM instance is vulnerable. Shared business logic can propagate even when front ends differ, but proving that requires owner-approved source comparison, software-bill-of-materials review, API inventory, and test evidence.

## 7. Defensive Priorities For The University Owner

The Malaysian Personal Data Protection Standard describes its controls as minimum requirements for security, storage, and integrity [18]. It requires practical measures against loss, misuse, modification, unauthorized or accidental access, disclosure, alteration, or destruction [18]. It also calls for permanent deletion when data is no longer processed and reasonable steps to keep data accurate, complete, not misleading, and current [18]. These requirements are directly relevant to the public registration fields.

| Priority | Owner-authorized action | Evidence or standard | Expected outcome |
|---|---|---|---|
| 1. Confirm service ownership | Record the legal operator, data controller, system owner, incident contact, and disclosure channel for `student.manipal.edu.my` | Entity ambiguity is documented by MQA and MUCM support branding [12][7] | Correct routing of incidents, privacy requests, and changes |
| 2. Inventory identity paths | Document student SSO, parent login, account creation, recovery, invitation, role assignment, and deprovisioning | Public UI exposes all of these entry points or role concepts [5][1] | Complete authentication and authorization threat model |
| 3. Apply phishing-resistant authentication | Offer a phishing-resistant option at AAL2-equivalent risk; do not treat OTP as phishing-resistant | NIST guidance [23] | Lower credential-phishing exposure |
| 4. Govern Conditional Access | Cover every application, begin in report-only mode, monitor sign-ins, and preserve break-glass access | Microsoft recommends application coverage, report-only rollout, and emergency exclusions [21] | Safer policy deployment without tenant lockout |
| 5. Harden sessions | Use full-session TLS, `Secure` cookies, narrow scope, renewal after privilege changes, server-side idle/absolute expiry, and safe logging | OWASP guidance [20] | Reduced fixation, hijacking, and persistence risk |
| 6. Review registration privacy | Validate purpose, notice, terms, retention, correction, and deletion for name, email, and phone fields | Public fields [1] and Malaysian standard [18] | Defensible personal-data lifecycle |
| 7. Review Clarity governance | Determine whether Clarity is necessary on authentication pages, apply strict masking, prevent confidential capture, and assess under-18 use | Microsoft describes recordings/heatmaps and warns about under-18 targeting [27] | Reduced analytics and consent risk |
| 8. Compare deployments internally | Compare repositories, SBOMs, API contracts, dependency locks, identity app registrations, release manifests, and defect tickets | Public evidence cannot prove code identity | Reliable blast-radius analysis across campuses |
| 9. Test only with authorization | Use staging, synthetic accounts, written scope, rate limits, rollback, and coordinated disclosure | No vulnerability was demonstrated publicly | Evidence without student harm or unauthorized access |

NIST further requires periodic reauthentication and discusses step-up authentication when a higher assurance level is needed [23]. That supports stronger checks before high-impact functions such as identity changes, sensitive academic records, financial actions, or parent-account linking. It does not imply that every page needs repeated MFA.

OWASP says session identifiers should be renewed after privilege changes to prevent session fixation [20]. It also recommends logging session creation, renewal, destruction, timeout, and invalid-session events without recording the raw session ID [20]. For SLCM, those logs should be correlated with identity-provider sign-ins and support tickets under documented retention and access rules.

If Akamai protects MUJ, its WAF can block threatening HTTP and HTTPS requests [14]. That remains complementary to application controls. Authorization, identity proofing, business-rule enforcement, secure recovery, privacy, and data minimization must be verified in the application and identity layers.

## 8. Synthesis: One Product Family, Multiple Security Boundaries

Across the evidence, three layers need to be separated.

First, the **business layer** is visibly related. Manipal institutions use SLCM terminology, student lifecycle functions, scholar or institutional identities, and parent access [5][2][4]. This layer likely drives common requirements and may create similar classes of operational failure.

Second, the **presentation and deployment layer** diverges. Malaysia exposes public self-registration and a modern client shell; MUJ presents a differently branded, differently routed login. That divergence means a front-end issue, dependency defect, or route-specific weakness should not be assumed to transfer. Conversely, different front ends can still call common services, so divergence does not rule out shared APIs or business logic.

Third, the **governance layer** is fragmented or at least publicly ambiguous. The former MIU is now regulator-listed under the MILA name [12], while a current support service on the `manipal.edu.my` namespace is branded MUCM [7]. MUJ is explicit about its own portal branding [2]. The strongest cross-campus risk may therefore be governance inconsistency: unclear service ownership, different release branches, varied identity policies, and incomplete central knowledge of which defects affect which deployment.

| Dimension | Shared-family interpretation | Independent-deployment interpretation | Best current judgment |
|---|---|---|---|
| Mechanism | Central SLCM requirements or components reused across campuses | Similar university needs produced parallel portals | Shared product lineage is plausible |
| Scope | Student, parent, registration, academic, and support workflows may be related | Each legal entity may configure only a subset | Functions overlap, implementation scope differs |
| Trade-off | Reuse lowers cost but can widen defect blast radius | Separation limits blast radius but increases configuration drift | Both risks should be assumed until internal inventory resolves them |
| Evidence base | Common naming and role concepts [5][2][4] | Different routes, shells, branding, and registration behavior | Public evidence favors family-level relation, not binary identity |
| Time horizon | Legacy lineage may persist for years | Rebrands and modernization create forks | Historical ownership makes current attribution especially important |
| Security implication | A confirmed defect should trigger cross-campus regression review | Findings still require deployment-specific reproduction under authorization | Test centrally, conclude locally |

The non-obvious tension is that the Malaysia portal can look more modern while still revealing less about governance. A compiled front end and Microsoft-branded sign-in may improve user experience, yet the generic branding and entity ambiguity make incident routing harder. At the same time, MUJ's older-looking presentation does not prove weaker security; secure behavior depends on maintained dependencies, authorization, identity policy, session controls, and operational monitoring.

The practical model is therefore **federated SLCM governance**: maintain a central catalog of services, owners, repositories, SBOMs, identity applications, data classes, release branches, and known defects, while requiring each campus to verify local configuration. This model accommodates both reuse and divergence without assuming either.

## VERDICT

**Overall confidence: Moderate-high for the public-surface findings; moderate for shared-product inference; low for identical-code or shared-back-end claims.**

1. **Portal existence and behavior - High confidence.** `student.manipal.edu.my` publicly exposes student sign-in, parent credentials, forgot-password, account creation, and a registration form requesting identity and contact information [5][1].

2. **Current entity attribution - Moderate confidence.** The former Manipal International University in Nilai is regulator-listed as the prior name of MILA University [12]. The parent-domain helpdesk identifies itself as MUCM [7]. Therefore, calling the student portal simply "the MIU portal" is potentially outdated or ambiguous.

3. **Microsoft identity involvement - Moderate confidence.** The student experience is Microsoft-branded in public markup and uses a "Scholar E-Mail ID" label [5]. This is not enough to identify the tenant, protocol, MFA posture, or relationship to MUJ's Microsoft 365 environment.

4. **Malaysia back-end technology - Low confidence/unknown.** The front end appears to be a compiled client application, but there is no reliable public proof in this review that Malaysia uses ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, or MUJ's exact back end.

5. **Public complaints - Low-volume evidence.** No attributable Malaysia-specific complaint was located. The single verified public complaint concerns Jaipur and reports a password error without a visible resolution [11]. It must not be generalized to Malaysia.

6. **Shared SLCM codebase - Not proven.** Common naming, roles, and institutional lineage support a shared SLCM product family. Different public architectures and routes argue against treating the live deployments as identical. The defensible conclusion is: **related ecosystem, probable shared requirements, possible shared components, unknown shared back end, and no demonstrated common vulnerability**.

7. **Recommended next step.** Obtain written authorization and perform an internal deployment comparison using repositories, SBOMs, API specifications, identity app registrations, configuration baselines, release manifests, and staging tests. Until then, public observations should guide questions, not justify production testing or vulnerability claims.

## References

1. *Portal Framework*. https://student.manipal.edu.my/auth/registration
2. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
3. *Manipal University*. https://muj.slcm.jaipur.manipal.edu/
4. [
	MU SLcM
](https://slcm.manipal.edu/)
5. *Portal Framework*. https://student.manipal.edu.my/
6. *One moment, please...*. https://manipal.edu.my/
7. *MUCM Helpdesk*. https://helpdesk.manipal.edu.my/
8. *MUCM Helpdesk*. https://helpdesk.manipal.edu.my/open.php
9. *List of Private Higher Education Qualifications*. http://www2.mqa.gov.my/MQR/english/eakrbyiptsku.cfm?CodeID=24&OrderBy=NamaIPTSBM
10. *Manipal International University | Manipal Academy of Higher Education*. https://www.manipal.edu/mu/important-links/world-wide-manipal/manipal-international-university.html
11. *Slcm portal issue : r/manipaljaipur*. http://reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue
12. [
	MILA University (Previously Known As : Manipal International University (MIU))
      	
](https://www2.mqa.gov.my/mqr/english/eakrKPList.cfm?IDAkrIPTS=629)
13. *Page not found – MILA University*. https://mila.edu.my/about-us/
14. *Web Application Firewall*. https://techdocs.akamai.com/property-mgr/docs/web-app-firewall
15. *What Is a Web Application Firewall (WAF)? | Akamai*. https://www.akamai.com/glossary/what-is-a-waf
16. *Personal Data Protection (Amendment) Act 2024 • Personal Data Protection*. https://www.pdp.gov.my/ppdpv1/en/akta/personal-data-protection-amendment-act-2024
17. *Principles of Personal Data Protection​ • Personal Data Protection*. https://www.pdp.gov.my/ppdpv1/en/principles-of-personal-data-protection
18. *Personal Data Protection Standard 2015​ • Personal Data Protection*. https://www.pdp.gov.my/ppdpv1/en/personal-data-protection-standard-2015
19. *Configure your firewall*. https://techdocs.akamai.com/etp/docs/configure-your-firewall
20. *Session Management - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
21. *Plan Your Microsoft Entra Conditional Access Deployment - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/conditional-access/plan-conditional-access
22. *Clarity client API | Microsoft Learn*. https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-api
23. *NIST Special Publication 800-63B*. https://pages.nist.gov/800-63-4/sp800-63b.html
24. *Authentication - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
25. *Block legacy authentication with Conditional Access - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/conditional-access/policy-block-legacy-authentication
26. *Masking content | Microsoft Learn*. https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-masking
27. *Frequently asked questions | Microsoft Learn*. https://learn.microsoft.com/en-us/clarity/faq
28. *Microsoft Entra Conditional Access: Zero Trust Policy Engine - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/conditional-access/overview
29. *OWASP Application Security Verification Standard (ASVS) | OWASP Foundation*. https://owasp.org/www-project-application-security-verification-standard
30. *Digital Identity Guidelines: Authentication and Lifecycle Management*. https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-63b.pdf
31. *NIST Special Publication 800-63B*. https://pages.nist.gov/800-63-3/sp800-63b.html
32. [
	MU SLcM
](https://slcm.manipal.edu/sendtoportal)
