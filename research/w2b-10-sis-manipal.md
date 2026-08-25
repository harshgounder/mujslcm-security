# MAHE SIS/SLCM WebForms Architecture and Defensive OSINT

## Executive Summary

This report examines the publicly visible MAHE Student Information System (SIS) surface at `https://sis.manipal.edu/studloginSLCM.aspx`, its relationship to other Manipal-branded SLCM portals, and the security meaning of an `.aspx` login endpoint. It is written for a university security club and is limited to public information and ordinary, non-authenticated observation. It does not provide instructions for bypassing authentication, enumerating accounts, testing credentials, manipulating requests, or reaching a protected origin.

The strongest public fact is narrow but useful: MAHE's official Student Portal page directs students to `https://sis.manipal.edu/index.aspx` [5]. The linked SIS login endpoint is publicly titled `SIS` and visibly contains a login control, a date-format hint `(dd/mm/yyyy)`, a CAPTCHA label, and a footer stating that it was designed and developed by the Information Systems Department of Manipal Academy of Higher Education [3]. The page is therefore a real, branded student-information login surface, not merely an unverified hostname.

The `.aspx` suffix is consistent with an ASP.NET Web Forms-era presentation layer, but it is not proof of a particular .NET Framework version, IIS configuration, database, authentication protocol, or deployment topology. Microsoft describes the Web Forms page lifecycle as a sequence that includes initialization, control instantiation, state restoration, and later processing [6]. That model explains why a legacy-looking page can depend on hidden state, postback processing, session state, cookies, and validation. It does not establish that any particular weakness exists on the MAHE service.

Public comparison shows a family resemblance across portals. The MAHE SLCM page is branded `MU SLcM` and identifies Manipal Academy of Higher Education in its title and footer [4]. The MUJ page says `WELCOME TO MUJ PORTAL` and exposes sign-in and parent-login language [1]. The official Manipal Dubai site links its Student Portal to `https://slcm.manipaldubai.com/` [7]. These are meaningful indicators of common institutional vocabulary and possibly common product lineage. They are not proof that the portals share code, infrastructure, databases, identity tenants, or security settings.

A separate public Salesforce announcement is important context: it says that MAHE is collaborating with Salesforce to modernize its Student Life Cycle Management platform, connect existing student, learning, and document systems through API-led integration, and deploy AI agents over a stated future period [7]. This supports the conclusion that SLCM is a broad institutional capability rather than just a login page. It also warns analysts not to assume that a legacy WebForms front end represents the whole current architecture. A hybrid estate can contain older presentation pages, newer services, cloud identity, integration layers, and campus-specific portals at the same time.

The appropriate security conclusion is therefore risk-based, not sensational. The public evidence supports a legacy-compatible WebForms hypothesis and a shared SLCM product-family hypothesis, both with medium confidence. It does not support claims that MAHE uses a specific Microsoft 365 tenant, Microsoft Entra federation, a particular IIS version, a particular Akamai configuration, a vulnerable ViewState implementation, a shared database, or an exposed origin. The club should focus on authorized documentation review, defensive configuration assurance, dependency and lifecycle management, identity-boundary review, logging, and coordinated disclosure.

**Decision insight:** treat the page as an important public authentication boundary and a likely integration point, but do not treat surface fingerprints as a vulnerability finding. The next safe step is an owner-approved architecture and control review, not exploratory testing.

## Publicly Observable MAHE SIS Surface

The official MAHE student-portal page is the best public source for the intended relationship between the institutional website and SIS. Its extracted content calls the destination `Student Portal`, presents a `Link to Student Portal`, and identifies `https://sis.manipal.edu/index.aspx` as the student-portal destination [5]. This is stronger evidence than a search-engine result alone because the link is published on the institution's own website.

The target login route is `https://sis.manipal.edu/studloginSLCM.aspx`. Its visible content is sparse. The page exposes `Login`, a `(dd/mm/yyyy)` hint, `Captcha`, and the institutional development footer [3]. Sparse output is itself a useful OSINT observation: the page does not publicly explain its backend, release history, database, identity provider, tenant, hosting origin, or supported application version. A security analyst should record that absence rather than fill it with assumptions.

### Table 1. Public MAHE SIS evidence

| Public item | Exact URL | What is directly visible or stated | Confidence | What it does not prove |
|---|---|---|---|---|
| Official student portal link | https://www.manipal.edu/mu/academics/student-portal.html | The page labels the destination Student Portal and links to `https://sis.manipal.edu/index.aspx` [5] | High | It does not disclose implementation details |
| SIS login route | https://sis.manipal.edu/studloginSLCM.aspx | The page presents `Login`, a date-format hint, `Captcha`, and an MAHE Information Systems footer [3] | High for visible text | It does not prove a framework version or vulnerability |
| SIS root | https://sis.manipal.edu/ | Search identifies the public page as `SIS Portal`; the extracted root has little visible text [2] | Medium | It does not prove that the root and login route have identical code |
| Institutional ownership signal | https://sis.manipal.edu/studloginSLCM.aspx | The footer names the Information Systems Department of MAHE [3] | High | It does not identify a vendor, hosting provider, or administrator |

The CAPTCHA label is a positive sign in the limited sense that the public login design anticipates automated-abuse resistance. It is not evidence that rate limiting, bot management, account lockout, risk-based authentication, or monitoring are correctly implemented. Those controls cannot be assessed from the label alone. Likewise, a date-format hint may indicate a student verification or account-recovery workflow, but its purpose is not stated publicly. It should not be interpreted as an instruction to test candidate personal data.

The official student-portal page also includes a general `Contact Us` label [5]. That matters operationally: students and researchers should use institutional support or an authorized security contact for access problems and suspected issues. Public community discussion reports at least one user saying that an SLCM password was rejected despite being believed correct [8]. That is anecdotal evidence of a user-reported login problem, not proof of a security defect, outage, account compromise, or identity-system failure. The correct treatment is to preserve it as a lead for service-desk correlation, not to reproduce it against real accounts.

**Decision insight:** the MAHE SIS login is a confirmed public-facing institutional boundary with limited public metadata. A security review should begin with ownership, data classification, support escalation, and control objectives, not with framework guessing.

## MUJ and Other SLCM Surfaces

The MUJ portal provides a useful comparison because it uses a distinct campus identity while retaining the SLCM vocabulary. The public page at `https://mujslcm.jaipur.manipal.edu/` says `WELCOME TO MUJ PORTAL` and includes `Sign In` and `Sign In Parent Login` [1]. Another public result for the same MUJ family includes `Sign In Student Login` and `Forgot Password?` [9]. The difference in visible wording is consistent with campus-specific branding or configuration.

The MAHE SLCM portal is separately branded `MU SLcM`. Its public result identifies it as `Manipal Academy of Higher Education - MU SLcM` and displays a footer stating `©2017 Manipal Academy of Higher Education, manipal.edu, Madhav Nagar, Manipal-576104, Karnataka` [4]. A public password-change route also appears under the same host and uses a conventional change-password presentation with old-password, new-password, and confirmation fields [10]. The existence of a password-change route is not a vulnerability finding; it simply shows that account lifecycle functions are represented in the public route vocabulary.

The Manipal Dubai site adds a third comparison point. Its official about page identifies Manipal Dubai as a branch campus of Manipal Academy of Higher Education and links the campus Student Portal to `https://slcm.manipaldubai.com/` [7]. The portal itself is publicly titled `Sign in to your account` [11]. This supports a broad institutional pattern in which campus or institutional portals use SLCM naming while presenting different public shells.

### Table 2. Public portal comparison

| Portal or surface | Exact URL | Visible identity and functions | Shared-family signal | Safe interpretation |
|---|---|---|---|---|
| MAHE SIS | https://sis.manipal.edu/studloginSLCM.aspx | `Login`, `(dd/mm/yyyy)`, `Captcha`, MAHE Information Systems footer [3] | `SLCM` in route name; official MAHE ownership | A WebForms-era-looking SIS login surface; backend unknown |
| MAHE SLCM | https://slcm.manipal.edu/ | `MU SLcM`; MAHE title/footer [4] | Same institutional SLCM term | A separate public SLCM-branded portal; implementation relationship unproven |
| MUJ | https://mujslcm.jaipur.manipal.edu/ | `WELCOME TO MUJ PORTAL`, sign-in and parent-login language [1] | SLCM in hostname; Manipal campus branding | A MUJ campus portal using SLCM vocabulary |
| Manipal Dubai | https://slcm.manipaldubai.com/ | Sign-in page; official campus site links to it [114.0; 35.0] | Official branch-campus link and SLCM hostname | A campus SLCM entry point; code and identity relationship unknown |
| Salesforce SLCM environment | https://maheslcmtech--sit.sandbox.my.site.com/login?locale=us | Public result identifies `Login | SLCM` and a Salesforce customer-account login [12] | SLCM term; separate technology surface | Evidence of a Salesforce-related SLCM environment, not proof that it replaces every legacy page |

The table shows both convergence and divergence. Convergence appears in names: `SIS`, `SLCM`, `MU SLcM`, student login, parent login, and campus-specific domains. Divergence appears in page wording, hostnames, route styles, and the presence of a Salesforce sandbox login. That divergence is exactly why a shared-code conclusion would be premature.

**Inference:** the most economical explanation is a multi-campus SLCM ecosystem with shared terminology, shared institutional processes, or both. A common codebase is only one possible implementation. Other possibilities include independently deployed applications, a common product with tenant-specific themes, a gradual replacement program, or legacy portals integrated with newer services.

**Decision insight:** use the phrase `shared SLCM product-family hypothesis`, not `shared application` or `shared database`. The former is supported by public evidence; the latter two are not.

## What `.aspx` and WebForms Actually Indicate

An `.aspx` route is a historical technology clue. It commonly appears in ASP.NET Web Forms applications, but an extension alone cannot identify the runtime, version, server, code-behind language, authentication module, or application architecture. A route can be retained during migration, proxied to a different service, generated by a compatibility layer, or served by a system whose original framework has changed.

Microsoft's ASP.NET documentation describes the page lifecycle as a sequence of processing steps, including initialization, control instantiation, restoration of state, and later processing [6]. This is the useful architectural lesson for a defensive review. A WebForms page is not just a static HTML document. It may maintain a server-side session, emit hidden state, reconstruct controls on postback, validate submitted events, and issue or consume authentication cookies.

ViewState is a client-carried state mechanism used by WebForms. Microsoft's troubleshooting material specifically discusses invalid ViewState errors [13], while specialist technical guidance describes ViewState as serving several distinct state-management jobs [14]. The operational implication is not that ViewState is inherently unsafe. The implication is that state integrity, cryptographic protection, machine-key consistency, size limits, and load-balancer behavior require deliberate configuration and testing by the application owner.

Request validation is another relevant control boundary. Microsoft describes ASP.NET request validation as a feature intended to prevent the server from accepting unencoded HTML and to reduce some script-injection scenarios [15]. OWASP describes the feature as examining request components such as query strings, cookies, and posted form values for potentially dangerous markup [16]. Request validation is defense in depth, not a substitute for output encoding, input validation, authorization, content security policy, secure design, or safe data handling. It should not be disabled casually, and any exceptions should be narrowly justified and reviewed.

The public page does not reveal whether MAHE uses ViewState MAC, encryption, event validation, anti-forgery defenses, secure cookie attributes, session rotation, or centralized rate limiting. It also does not reveal whether the CAPTCHA is server-validated, whether failed attempts are logged, or whether all identity operations occur in the same application. These are review questions, not findings.

### Table 3. WebForms-era control areas for an authorized review

| Control area | Why it matters in WebForms | Public evidence available here | Safe owner-approved review question |
|---|---|---|---|
| Page lifecycle and postback | Controls and state may be reconstructed across requests [6] | `.aspx` route and visible login page [3] | Are lifecycle-dependent controls tested after framework and infrastructure changes? |
| ViewState integrity | Invalid state can arise from tampering, stale state, key mismatch, or deployment behavior [98.0; 100.0] | No configuration is public | Are MAC/encryption, key management, size limits, and farm consistency documented? |
| Event/request validation | Validation reduces some unsafe input paths | CAPTCHA and form labels only [3] | Are validation controls enabled where appropriate and supplemented by output encoding? |
| Session and cookies | Authentication and workflow state depend on secure session handling | Not publicly disclosed | Are Secure, HttpOnly, SameSite, rotation, expiry, logout, and fixation controls verified? |
| Authentication throttling | Login endpoints face password-spraying and credential-stuffing risk | CAPTCHA label only [3] | Are rate limits, alerting, lockout design, and abuse handling tested without real-user disruption? |
| Error handling | Detailed errors can expose implementation and state information | No detailed errors observed in the public extract | Are production errors generic to users and detailed only in protected logs? |
| Deployment and patching | Framework and server support status affects remediation options | .NET Framework 4.8 is listed as active by Microsoft's policy page [17] | What exact runtime and patch baseline is installed and supported? |

Known WebForms failure patterns are often operational rather than remotely exploitable: invalid or oversized state, stale pages after deployment, lost session affinity, inconsistent cryptographic keys across servers, incompatible proxy caching, and authentication redirects that fail across domain boundaries. These are plausible classes of failure, not claims that MAHE experiences them. The student-reported password problem [8] could arise from many benign causes, including account status, synchronization delay, password policy, user error, or service degradation; public evidence cannot distinguish them.

**Decision insight:** `.aspx` should trigger a control checklist, not a vulnerability label. The high-value review is to confirm configuration, lifecycle support, and observability with the system owner.

## Identity, IIS, Akamai, and Architecture Boundaries

The input brief describes the MUJ environment as ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10 behind Akamai, with Microsoft 365 identity. Those details should be treated as supplied research context, not as independently verified public facts in this report. The public MAHE SIS evidence does not establish that those same properties apply to `sis.manipal.edu`, `slcm.manipal.edu`, MUJ, or any other portal.

The Microsoft identity platform documentation describes OAuth authorization-code flow as a mechanism by which a client obtains authorized access to protected APIs [18]. Microsoft's Entra material describes web-app and web-API authentication scenarios for ASP.NET Core [19]. Those sources establish what modern Microsoft identity integration can look like, but they do not show that the legacy-looking MAHE SIS page uses Entra ID, Microsoft 365, OpenID Connect, OAuth, or a particular federation arrangement. A WebForms front end can authenticate against a local directory, a campus identity service, a legacy database, a federation gateway, or a newer identity broker.

Similarly, a CDN or reverse proxy can change the visible edge without revealing the origin. Akamai's documentation describes edge-platform proxy behavior [20]. That supports the general architectural distinction between an edge service and an origin application, but it does not prove that any particular Manipal hostname is configured with Akamai, nor does it reveal origin addresses, cache rules, WAF policies, header handling, or bypass paths.

### Table 4. Claim-status matrix

| Claim | Status from public evidence | Reason |
|---|---|---|
| MAHE publishes a student-portal link to SIS | Confirmed | Official page links to `sis.manipal.edu/index.aspx` [5] |
| `studloginSLCM.aspx` is an MAHE SIS login surface | Confirmed | Page exposes login/CAPTCHA/date hint and MAHE Information Systems footer [3] |
| The endpoint uses ASP.NET Web Forms | Probable but not proven | `.aspx` is consistent with WebForms; no source/configuration is public |
| The endpoint runs .NET Framework 4.x | Unverified | No public runtime disclosure in the observed page |
| MUJ, MAHE, and Dubai share source code | Unverified | Similar naming and workflows do not prove code reuse |
| They share a database | Unverified | No public database or integration evidence |
| They share Microsoft 365 or Entra identity | Unverified | Microsoft documentation is generic; no MAHE-specific federation evidence observed |
| They are all behind Akamai | Unverified | Akamai documentation is generic; public page content does not prove deployment |
| A vulnerability exists in ViewState or CAPTCHA | Not established | No authorized security test or configuration evidence was performed |
| MAHE is modernizing SLCM with Salesforce-related technology | Publicly reported | Salesforce announcement describes the collaboration and API-led integration [7] |

The Salesforce announcement changes the architecture discussion. It describes a modernization effort involving an SLCM platform, existing systems, API-led integration, analytics, and AI agents [7]. **Inference:** the likely architecture is transitional or hybrid, with legacy portals potentially remaining in service while newer components are integrated around them. That inference is more defensible than claiming that all student-facing pages have already migrated or that the `.aspx` route is obsolete.

**Decision insight:** separate four boundaries in every architecture diagram: browser-to-edge, edge-to-origin, application-to-identity, and application-to-data/integration. Public hostnames can suggest the first boundary; they cannot prove the other three.

## Defensive Review Plan for a University Security Club

A student security club can contribute valuable work without touching protected accounts or conducting unapproved testing. The first deliverable should be a public-OSINT evidence register containing URL, collection date, page title, visible wording, screenshot hash if institutionally permitted, and a classification of fact, inference, or unknown. The register should avoid student names, personal data, credentials, CAPTCHA content, session tokens, and copied pages that could create privacy or copyright concerns.

The second deliverable should be a question set for the system owner. The club can ask which team owns SIS and SLCM, which domains are production versus test, which portals are being retired or modernized, which identity systems are authoritative, what the supported runtime baseline is, and where students should report login faults. It should request a sanctioned test window only if technical testing is needed. Without written authorization, ordinary browsing should stop at public content.

The third deliverable is a control map. Map the public login boundary to identity, session, state, bot mitigation, logging, monitoring, support, and recovery controls. Ask the owner to validate the controls against a non-production tenant or synthetic accounts. Do not use student credentials, test password-reset flows against real identities, submit crafted state, attempt rate-limit measurement, or compare account responses.

### Table 5. Safe review work packages

| Work package | Permitted evidence source | Output | Explicit boundary |
|---|---|---|---|
| Asset and ownership inventory | Official links and public pages [68.0-3; 114.0] | Domain-to-owner map with confidence | Do not scan or enumerate unlisted hosts |
| Public-page comparison | Normal browser access to named public pages [69.0-2; 70.0-7; 115.0] | Branding, route, and workflow comparison | Do not submit credentials or alter requests |
| Architecture hypothesis | Public announcements and page evidence [7] | Fact/inference/unknown matrix | Do not state shared code or databases as fact |
| WebForms control checklist | Microsoft and OWASP guidance [93.0; 74.0-75.0] | Owner review questionnaire | Do not attempt to validate controls against production |
| Identity-boundary review | Owner documentation and sanctioned diagrams | Entra/M365/local identity classification | Do not infer identity from branding or redirects alone |
| Incident and login-issue correlation | Help-desk records and anonymized reports | Root-cause candidates | Do not collect passwords or personal data |
| Responsible disclosure | Institutional security policy | Reproducible, minimal report | Do not publish exploit details or sensitive evidence |

For a sanctioned technical assessment, the owner should provide a written scope that names domains, dates, source IPs, test accounts, allowed methods, rate limits, stop conditions, data-handling rules, and emergency contacts. The safest environment is a non-production replica with synthetic identities. Results should distinguish an observed security control failure from an availability or usability problem. A CAPTCHA appearing on the page is not a pass/fail assessment; the owner must verify server-side enforcement and monitoring.

The club should also recommend an upgrade and dependency inventory. Microsoft's lifecycle material lists .NET Framework 4.8 as active [17], but a generic support statement does not prove that a specific application is running 4.8 or is fully patched. The owner should record exact framework, OS, IIS, third-party library, cryptographic-key, and identity-connector versions, then map each to support and patch status. Legacy does not automatically mean unsafe, but unsupported or undocumented components increase remediation uncertainty.

**Decision insight:** the club's highest-value contribution is evidence discipline: identify what the public record establishes, convert the unknowns into owner questions, and keep all validation inside a written authorization boundary.

## Case Study: MAHE and MUJ as a Shared-Platform Hypothesis

The MAHE and MUJ pages make a useful case study because they combine common vocabulary with visibly different presentation. MAHE's SIS route contains `studloginSLCM.aspx`, a CAPTCHA label, a date-format hint, and a footer naming the MAHE Information Systems Department [3]. MUJ's public page instead foregrounds `WELCOME TO MUJ PORTAL` and separates sign-in and parent-login language [1]. A straightforward explanation is campus-specific configuration over a common student-lifecycle concept. Another explanation is that independently built portals adopted institutional terminology. The public record cannot select between them.

The MAHE SLCM page adds a third observation: it uses `MU SLcM`, carries MAHE identity, and exposes a 2017 copyright statement in its search result [4]. Manipal Dubai's official site links to its own SLCM host [7], and its portal uses generic account-sign-in language [11]. This resembles a distributed institutional service family, but the differences in domains, page shells, and labels imply that campus autonomy or tenant-specific presentation may exist.

The Salesforce announcement introduces a decision inflection. It says MAHE intends to modernize SLCM, connect existing systems using API-led integration, and deploy new capabilities around the student lifecycle [7]. **Inference:** the ecosystem may be moving from a collection of legacy web applications toward a layered platform in which old pages remain as user interfaces while new services handle integration, data, analytics, or workflow. During such transitions, identity mapping, session boundaries, authorization consistency, and data ownership become more important than the visible framework label.

### Table 6. Competing architecture explanations

| Explanation | Evidence supporting it | Evidence against or missing | Confidence |
|---|---|---|---|
| Common product family with campus-specific themes | Repeated SLCM naming; MAHE, MUJ, and Dubai campus portals [69.0-2; 114.0; 115.0] | No public source-code or deployment evidence | Medium |
| One shared codebase | Similar workflow vocabulary and route conventions | Different domains and page shells; no code evidence | Low |
| Shared database | Common institutional lifecycle concept | No database, API, or tenancy evidence | Very low |
| Federated identity across portals | Modern identity patterns are technically possible [80.0; 82.0] | No MAHE-specific federation evidence | Low |
| Hybrid legacy plus modernization | `.aspx` surface plus Salesforce modernization announcement [70.0-7; 114.0] | Public announcement does not map every existing page | Medium |
| Independent campus applications | Distinct branding and hostnames | Repeated SLCM vocabulary and institutional links | Low to medium |

The contrast reveals a practical trade-off. Shared platforms can standardize enrollment, academic progress, parent access, and support workflows, reducing duplicated development. They can also magnify the blast radius of configuration errors, identity-mapping mistakes, or common dependency problems. Independent campus systems can isolate failures and tailor workflows, but they may duplicate controls and produce inconsistent student experiences. Public evidence does not show which trade-off MAHE has chosen in implementation.

**Decision insight:** architecture governance should prioritize tenant isolation, least privilege, centralized monitoring, and consistent recovery procedures even if the visible portals appear separate.

## Known Issues and Failure Modes Without Overclaiming

The public record contains one user-reported SLCM password complaint, in which a Reddit poster said the password was shown as incorrect despite being believed correct [8]. It is appropriate to call this a reported usability or availability symptom. It is not appropriate to infer credential compromise, password database failure, account enumeration, or a bypass condition. A service desk could investigate it using anonymized timestamps, campus, account state, and authentication logs.

WebForms systems can also experience invalid-state and postback errors. Microsoft documents invalid ViewState troubleshooting [13], and its page lifecycle documentation explains why state restoration and control creation are operationally important [6]. In a load-balanced deployment, inconsistent machine keys or session behavior can produce intermittent failures. In a proxy deployment, caching or cookie-domain mistakes can interfere with login. These are control-review hypotheses, not observations about the MAHE service.

Request validation is frequently misunderstood. Microsoft says the feature prevents acceptance of unencoded HTML and is designed to help prevent some script-injection attacks [15]. OWASP similarly describes examination of request elements for potentially dangerous content [16]. Neither source says request validation eliminates cross-site scripting, injection, broken authorization, or unsafe output. Therefore, a review should verify contextual output encoding, authorization on every sensitive operation, secure state handling, and logging in addition to request validation.

A CAPTCHA is also not a complete anti-abuse system. It can reduce some automated activity, but the page text alone cannot establish challenge quality, replay resistance, accessibility, rate limiting, password-spraying detection, or account-lockout behavior. A university should prefer layered controls that avoid locking out students during examinations while still detecting anomalous activity.

### Table 7. Symptom-to-control triage

| Public or plausible symptom | Alternative explanations | Owner-side evidence needed | Safe student-club contribution |
|---|---|---|---|
| Password rejected report [8] | Expired account, sync delay, policy, outage, user error | Auth logs, identity sync, help-desk ticket | Recommend anonymized correlation |
| Invalid ViewState | Stale page, key mismatch, farm inconsistency, oversized state [13] | Error logs, deployment history, key/session configuration | Explain lifecycle risk; do not craft state |
| CAPTCHA present | Bot mitigation may be partial or misconfigured | Server-side validation, rate limits, telemetry | Record visible fact only |
| Different campus login wording | Theme, tenant, independent system, migration | Architecture diagram and deployment inventory | Build fact/inference table |
| Legacy `.aspx` route | WebForms, compatibility route, proxy, retained URL | Runtime inventory and source ownership | Avoid version claims |

**Decision insight:** every symptom should be triaged through at least two benign explanations before a security hypothesis is advanced. This prevents a security club report from turning a normal support issue into an unsupported vulnerability claim.

## Synthesis

Across mechanism, scope, trade-offs, evidence base, and time horizon, the ecosystem is best understood as a layered and possibly transitional service family. Mechanistically, the MAHE SIS route looks like a WebForms-era login surface because of its `.aspx` naming and visible form-oriented text, while the Microsoft documentation describes the stateful lifecycle that makes such systems operationally distinctive [70.0-7; 93.0]. That says more about presentation and request processing than about the underlying data or identity architecture.

In scope, MAHE, MUJ, and Dubai share SLCM vocabulary and student-lifecycle context, but they use distinct domains and visibly different shells [69.0-2; 114.0-115.0]. The commonality supports a product-family or governance hypothesis. It does not support a shared database or shared source-code claim. The Salesforce announcement expands the scope further by describing integration of existing student, learning, and document systems [7]. The likely strategic direction is therefore broader than preserving one legacy login page.

In trade-offs, a common platform can improve consistency but increase correlated risk; campus-specific systems can isolate problems but duplicate identity, logging, and maintenance controls. In evidence base, direct page observations are high-confidence, framework identification is medium-to-low confidence, and claims about Microsoft 365, Entra, IIS, Akamai, origin infrastructure, and database topology remain unknown. In time horizon, the legacy-looking public surface is a current observation, whereas modernization statements describe a future-oriented transformation and cannot be used to claim that migration is complete [7].

The non-obvious tension is that a familiar legacy surface can coexist with a modern backend. Conversely, a modern cloud identity or edge service would not make the application authorization model safe automatically. The proper control model is therefore end-to-end: protect the edge, harden the application, secure state and cookies, enforce authorization, protect identity integration, isolate tenants, monitor abuse, and maintain a tested recovery path.

### Table 8. Final evidence and action ranking

| Finding | Evidence strength | Risk relevance | Recommended action |
|---|---|---|---|
| MAHE SIS is an official public student-login surface | High [68.0-3; 70.0-7] | High | Confirm owner, data classification, and incident contact |
| WebForms-era implementation is plausible | Medium [70.0; 93.0] | Medium | Review lifecycle, state, cookies, validation, and patching |
| MAHE/MUJ/Dubai form an SLCM-related ecosystem | Medium [69.0-2; 114.0-115.0] | High | Obtain an authoritative service and tenancy map |
| Shared code/database is proven | Very low | Potentially high if assumed incorrectly | Do not state it; request architecture evidence |
| Microsoft 365/Entra identity is proven for SIS | Low | High | Verify identity provider and trust boundaries with owner |
| Akamai/IIS details are proven for all portals | Low | High | Verify edge/origin design from authorized documentation |
| Login issue indicates a vulnerability | Very low [8] | Medium | Correlate with anonymized support and authentication logs |
| Modernization is occurring | Medium to high for the announcement [7] | High | Track migration, integration, and legacy-retirement controls |

The report's answer to the central question is therefore: the MAHE SIS `studloginSLCM.aspx` page publicly reveals an MAHE-owned, CAPTCHA-bearing, date-format-aware login surface consistent with an older ASP.NET WebForms presentation pattern. Alongside MAHE, MUJ, Dubai, and modernization references, it supports a shared SLCM product-family hypothesis. It does not publicly reveal enough to claim a shared implementation, identity tenant, database, origin, or exploitable weakness.

## VERDICT

**Verdict:** MAHE SIS is a publicly confirmed institutional login surface. Its `.aspx` route is a credible WebForms-era indicator, but not a standalone vulnerability indicator. MAHE, MUJ, and Manipal Dubai publicly exhibit a related SLCM naming and service pattern, yet the public record does not prove shared source code, shared databases, shared identity, or shared hosting. The public Salesforce announcement supports a broader, hybrid modernization context in which legacy and newer components may coexist [7].

**Confidence level:** **Medium overall**.

- **High confidence:** official MAHE student-portal linkage, public SIS route, visible login/CAPTCHA/date-format text, MAHE Information Systems footer, MUJ portal wording, and MAHE/Dubai SLCM references [68.0-3; 69.0-2; 70.0-7; 114.0-115.0].
- **Medium confidence:** the interpretation that `.aspx` is consistent with a WebForms-era surface and that the portals may belong to a shared SLCM product family [70.0; 93.0].
- **Low confidence or unknown:** exact .NET Framework version, MVC versus WebForms internals, IIS version, Akamai deployment, Microsoft 365/Entra integration, origin location, database topology, code reuse, tenant isolation, and any exploitable defect.

**Recommended next decision:** request an owner-approved architecture diagram and control attestation covering identity, edge, origin, session/state, tenant isolation, logging, patching, and modernization dependencies. Until that evidence exists, the responsible public-information conclusion is `legacy-compatible SLCM login surface with plausible shared product lineage; implementation and vulnerability status unverified.`

## Reasoning Summary

This report used a constrained evidence method: direct official links and page text were separated from search-result discovery; each claim was classified as confirmed, probable, inferred, or unknown; generic Microsoft and OWASP material was used to explain technology classes rather than to attribute controls to MAHE; and user-reported issues were treated as symptoms requiring owner-side correlation. This is a concise reasoning summary, not private chain-of-thought. No unauthorized access, credential testing, crafted requests, scanning, or exploit validation was performed.

## References

1. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
2. [
	SIS Portal
](https://sis.manipal.edu/)
3. [
	SIS
](https://sis.manipal.edu/studloginSLCM.aspx)
4. [
	MU SLcM
](https://slcm.manipal.edu/)
5. *Student Portal Login- MAHE (Manipal Academy Of Higher Education)*. https://www.manipal.edu/mu/academics/student-portal.html
6. *ASP.NET Page Life Cycle Overview*. https://learn.microsoft.com/en-us/previous-versions/aspnet/ms178472%28v%3Dvs.100%29
7. *About Manipal Dubai | MoHESR Licensed & CAA Accredited*. http://manipaldubai.com/about-us
8. *Slcm portal issue : r/manipaljaipur*. http://reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue
9. *Manipal University*. https://muj.slcm.jaipur.manipal.edu/
10. [
	MU SLcM
](http://slcm.manipal.edu/StudentChangePassword.aspx)
11. *Sign in to your account Manipal University Dubai https://slcm.manipaldubai.com*. https://slcm.manipaldubai.com/
12. *Login | SLCM*. http://maheslcmtech--sit.sandbox.my.site.com/login?locale=us
13. *Устранение неполадок с недопустимым viewstate - ASP. ... Microsoft Learn https://learn.microsoft.com › ... › ASP.NET*. https://learn.microsoft.com/ru-ru/troubleshoot/developer/webapps/aspnet/performance/troubleshooting-view-state-is-invalid-error
14. *TRULY Understanding ViewState - Weblogs @ ASP.NET*. https://weblogs.asp.net/infinitiesloop/truly-understanding-viewstate
15. *Request Validation - Preventing Script Attacks | Microsoft Learn*. https://learn.microsoft.com/en-us/aspnet/whitepapers/request-validation
16. *ASP.NET Request Validation - OWASP Foundation*. https://owasp.org/www-community/ASP-NET_Request_Validation
17. *.NET Framework official support policy*. https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-framework
18. *Microsoft identity platform and OAuth 2.0 authorization code flow*. https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow
19. *Microsoft Entra ID with ASP.NET Core - learn.microsoft.com*. https://learn.microsoft.com/en-us/aspnet/core/security/authentication/azure-active-directory?view=aspnetcore-10.0
20. *Proxy*. https://techdocs.akamai.com/cloudlets/docs/proxy
