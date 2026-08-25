# MUJ SLCM and India's University ERP Risk Landscape

## Executive Summary

- **Attribution Is Unproven**: MUJ's public pages establish an MUJ-branded portal and parent-facing sign-in surface, while MAHE documentation defines SLCM as the system for attendance, marks, results, circulars, and student-parent academic access [2][3]. None of the reviewed public sources attributes MUJ SLCM to Saral, GateWay, Hexad, Simpliance, Jeewane, MasterSoft, Serosoft, Fedena, TCS iON, or Samarth -> treat every proposed vendor relationship as unverified until MUJ or a supplier provides documentary evidence.

- **The Supplied Stack Is a Lead, Not a Finding**: The prompt identifies ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 identity, but MUJ's public landing page does not disclose a product or framework version [2]. Microsoft also supports ASP.NET components under more than one lifecycle mechanism, and an unspecified ".NET Framework 4.x" is too broad to determine support status [18][14] -> inventory exact assemblies, operating-system build, and patch level internally rather than converting a passive fingerprint into a vulnerability conclusion.

- **The Named Vendor List Mixes Different Categories**: Saral School Soft is a real ERP product developed by Saral Computers [6]. Hexad's public material presents a general software and digital-transformation firm, while Simpliance Vendor is compliance-audit SaaS rather than a student information system [8][5]. GateWay and "Jeewane" could not be resolved to unique higher-education ERP suppliers -> normalize legal names and products before doing risk comparisons.

- **A Universal ASP.NET Claim Does Not Survive Scrutiny**: The reviewed vendors include cloud platforms with undisclosed implementation stacks, Microsoft-oriented portal patterns, and the historical open-source Fedena stack, which explicitly used Ruby, Rails 2.3.5, and MySQL [9][11][32]. -> assess each deployed tenant from contracts, software bills of materials, and authenticated administration records, not from market-wide assumptions.

- **Fedena Supplies the Strongest Public Failure Case**: Researchers published seven findings in unsupported Fedena 2.3, including authentication bypass, remote code execution, SQL injection, broken access control, and three XSS issues [33]. The researchers stated that the open-source version would not receive patches and recommended migration to a supported product [33] -> any institution still running that exact legacy branch should prioritize isolation and replacement, not rely on a WAF as a complete fix.

- **Identity Strength Does Not Replace Application Authorization**: Microsoft recommends phishing-resistant methods such as passkeys, FIDO2 security keys, Windows Hello for Business, and certificate-based authentication [21]. However, IDOR arises when object-level access checks are missing even after a user has authenticated [12] -> combine strong Microsoft 365 or Entra controls with server-side authorization on every student, mark, fee, attendance, and document object.

- **Akamai Protects a Boundary, Not the Whole Application**: Akamai edge servers contact an origin under configured origin settings, negotiate the highest TLS version the origin supports, and depend on the origin being configured for the desired TLS level [16]. **Inference:** edge protection cannot by itself correct an origin's broken authorization, unsafe query construction, or flawed recovery workflow -> test edge and origin controls as separate layers.

- **The Immediate Club Mission Should Be Defensive Assurance**: The highest-value work is authorized inventory, architecture review, role-matrix testing, dependency and patch review, recovery-flow review, centralized logging, and incident exercises. OWASP calls for per-object authorization, backend CSRF validation, strong session generation, and parameterized queries [12][17][22][24] -> do not conduct unapproved probing of MUJ or supplier infrastructure.

## Scope, Safety, and Auditable Reasoning

This report uses public landing pages, vendor product pages, Microsoft and OWASP guidance, public source repositories, and a named vulnerability research report. It does not claim access to an MUJ account, origin server, source code, supplier contract, DNS history, WAF console, Microsoft 365 tenant, or internal vulnerability scan. The MUJ portal itself warns that access is for valid registered users; a comparable MasterSoft portal likewise says that invalid, stolen, or borrowed credentials and attempts to enlarge access are prohibited [7].

A request for "chain-of-thought" cannot be satisfied by exposing private internal reasoning. The substitute below is an auditable evidence-to-conclusion record: it shows the material observations, the inference rule, uncertainty, and resulting action without revealing hidden deliberation.

| Question | Public observation | Auditable conclusion | Status |
|---|---|---|---|
| What does SLCM hold? | MAHE describes attendance, internal and external marks, results, circulars, and a single window for students and parents [3]. | The system processes high-impact academic records. A confidentiality or integrity failure could affect students and institutional decisions. | Verified function set; impact statement is an inference. |
| Is the supplied MUJ stack confirmed? | The public MUJ page identifies the portal but states no product or version [2]. | ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai, and Microsoft 365 remain user-supplied working assumptions in this report. | Low-to-medium confidence until internally inventoried. |
| Do the named firms power MUJ? | No reviewed MUJ or vendor source names an MUJ implementation partner. | No vendor attribution is supportable. Similar branding or technology is insufficient. | High confidence in the negative attribution decision, not proof that no vendor exists. |
| Are these portals uniformly .NET? | Historical Fedena source identifies Ruby, Rails 2.3.5, and MySQL [32], while several current vendors publish product scope but not implementation language [9][11]. | The market is heterogeneous; ".NET portal" is an architectural class, not a vendor identity. | High confidence. |
| Is a vulnerability report a breach report? | Fedena research documents vulnerabilities in version 2.3 [33], but it does not document compromise of a named university. | Vulnerability, exploitability, exposure, and confirmed breach must remain separate labels. | High confidence. |

The evidence standard is deliberately asymmetric. Positive claims require an official page, source repository, advisory, or credible research report. A failed search cannot prove that a breach never occurred, so the vendor table uses "no credible product-specific report located" rather than "no breaches." This distinction is essential in an ecosystem where suppliers, deployments, resellers, and similarly named products can easily be conflated.

## MUJ SLCM: What the Public Surface Actually Establishes

MAHE's documentation says SLCM replaced an older Academic Management System and is a complete suite for attendance, internal marks, external marks, result publication, and broadcast messages [3]. It further calls SLCM a single window for students and parents [3]. The MUJ landing pages publicly identify a "WELCOME TO MUJ PORTAL" surface and expose parent-oriented sign-in text [2]. These facts establish business purpose and role separation, but not the application owner, source-code lineage, database engine, or hosting architecture.

| Publicly visible element | Evidence | Defensive significance |
|---|---|---|
| MUJ-branded portal | The page labels itself "WELCOME TO MUJ PORTAL" [4][2]. | Brand trust makes the page valuable to users and therefore relevant to anti-phishing controls. |
| Student and parent academic access | MAHE calls SLCM a single window for students and parents [3]. | Separate personas imply separate entitlements, recovery paths, and session risks. |
| Attendance | Listed as an SLCM module [3]. | Integrity matters because attendance can drive eligibility and intervention workflows. |
| Internal and external marks | Both are listed SLCM modules [3]. | Confidentiality and integrity are critical; authorization should be subject, course, term, and role aware. |
| Results and circulars | Result publication and broadcast messages are included [3]. | Publication workflows require approval, audit logs, and protection from premature disclosure. |
| Technology details | No visible product or version claim appears on the public MUJ page [2]. | Passive fingerprints should be recorded as hypotheses and verified through authorized inventory. |

### Architecture status table

| Claimed component | Status in this report | What can safely be concluded |
|---|---|---|
| ASP.NET MVC 5.3 | User-supplied premise; not independently confirmed on the MUJ page. | Microsoft says some ASP.NET parts ship as external packages and those packages are treated as lifecycle "Tools" [18]. The exact deployed package must be inventoried. |
| .NET Framework 4.x | User-supplied premise; version too broad. | Microsoft retired 4.5.2, 4.6, and 4.6.1 on April 26, 2022, while 4.6.2 has an end date of January 13, 2027 [14]. Different 4.x releases therefore have materially different status. |
| IIS 10 | User-supplied premise. | IIS version alone does not identify the Windows Server release, cumulative update, application-pool identity, or TLS configuration. No stronger public conclusion is made. |
| Akamai | User-supplied premise. | Akamai documentation shows an edge-to-origin relationship and makes origin TLS support an origin configuration responsibility [16]. |
| Microsoft 365 identity | User-supplied premise. | If Entra is the identity provider, Conditional Access can evaluate user, location, device, application, and risk signals after first-factor authentication [10]. It does not prove that MUJ has enabled those controls. |
| SQL Server | Ecosystem hypothesis, not verified for MUJ. | No reviewed first-party MUJ source identifies the database engine. |

**Case study - MUJ's split trust boundary.** The public facts describe a system in which institutional identity, family access, academic records, and publication workflows meet. **Inference:** this is not one authentication problem. It is at least four boundaries: external identity to application session, session to role, role to individual academic objects, and business workflow to approved publication. A control can succeed at one boundary and fail at another.

For example, phishing-resistant Microsoft identity can reduce credential theft, but it cannot prevent a logged-in parent from seeing the wrong student's record if object authorization is defective. OWASP defines IDOR as access or modification through manipulated identifiers when required access checks are missing, and it recommends a check for every object requested [12]. The club should therefore avoid a simplistic "SSO means secure" conclusion.

## Indian Education ERP Landscape: Verified Products Versus Name Noise

The market comparison must separate a verified product from a guessed vendor. Saral School Soft, MasterSoft, Academia, Fedena, TCS iON, and Samarth have identifiable education-facing products or portals. Hexad and Simpliance are real software businesses, but the reviewed pages do not establish that they are university ERPs. GateWay and "Jeewane" remain unresolved names.

| Name supplied or relevant comparator | Verified public identity and scope | Public stack evidence | MUJ relationship | Evidence confidence |
|---|---|---|---|---|
| Saral | SARAL School Soft describes itself as an ERP solution developed by Saral Computers Pvt. Ltd. and says the company has been in service since 1990 [6]. | No language, framework, database, or hosting stack is disclosed on the reviewed page [6]. | Not established. | High for product identity; low for stack. |
| GateWay | No unique Indian higher-education ERP supplier could be resolved from the supplied name. | Unknown. | Not established. | Low; legal entity or exact URL required. |
| Hexad | Hexad describes itself as a software solution provider. Its published markets and technologies include digital transformation, automotive, enterprise systems, Microsoft, SAP, cloud, IoT, and related services, but the reviewed material does not state a university ERP [8]. | Broad technology capabilities only; no product implementation stack. | Not established. | High that the reviewed Hexad page is not evidence of an education ERP. |
| Simpliance | Simpliance Vendor is a SaaS and cloud-based vendor-compliance platform for audits, evidence, dashboards, risk scores, certificates, and statutory tracking [5]. | SaaS/cloud is stated; language, database, and framework are not [5]. | Not established. | High for category mismatch. |
| Jeewane? | The spelling does not resolve to a unique official higher-education ERP supplier in the reviewed corpus. | Unknown. | Not established. | Low; likely requires corrected spelling or URL. |
| MasterSoft | MasterSoft states that its cloud Education ERP serves schools, colleges, and universities and manages administration, finance, library, HR, and other departments [11]. Its portal states that the application is developed and owned by MasterSoft ERP Solutions Pvt. Ltd. [7]. | Cloud deployment is stated; implementation language and database are not. | Not established. | High for identity and scope; low for internal stack. |
| Academia by Serosoft | Serosoft offers Academia products for education, including SIS, ERP, university, campus, training, and school use; it describes connected workflows from enquiry to marksheet [9]. | The reviewed page says cloud-native but does not name an application framework or database [9]. | Not established. | High for identity and scope; low for stack. |
| Fedena by Foradian | Fedena is provided by Foradian and covers admissions, parent collaboration, timetables, attendance, fees, examinations, gradebooks, and online classes [23]. | Historical open-source Fedena used Ruby, Rails 2.3.5, and MySQL [32]. This must not be generalized to every current commercial Fedena service. | Not established. | High for historical stack; medium for current architecture. |
| TCS iON | TCS iON presents an integrated higher-education suite spanning learning, admissions, fees, assessment, marking, examinations, and campus operations [15]. | The reviewed page does not identify its implementation framework or database. | Not established. | High for scope; low for stack. |
| Samarth eGov | Samarth's official site presents a digital-campus initiative under the Samarth eGov name [13]. Multiple institutional Samarth portals were also visible in public search results, but no implementation stack was established. | Unknown from the reviewed first-party material. | Not established. | Medium for landscape inclusion; low for stack. |

The table exposes two OSINT traps. First, "Saral" is not enough: the defensible identity is SARAL School Soft by Saral Computers, not every Indian product carrying the word Saral. Second, a company's ability to build Microsoft, cloud, or enterprise systems does not prove that it supplied a particular university. Hexad's broad technology portfolio is therefore contextual information, not attribution evidence [8].

**Case study - MasterSoft versus Academia.** Both companies describe broad, cloud-oriented education systems. MasterSoft emphasizes cross-department campus administration [11], while Serosoft presents a family of education products and end-to-end student workflows [9]. Yet neither reviewed product page reveals the language, framework, database version, tenant isolation model, or patch cadence. **Inference:** procurement claims answer "what it does," not "how safely this tenant is built." Security assurance has to come from architecture documents, a current software bill of materials, penetration-test summaries, subprocessor records, and contractual remediation commitments.

## What Previous-Generation ASP.NET Portals Typically Do

A previous-generation Microsoft portal often combines server-rendered pages or MVC routes, IIS hosting, .NET Framework packages, state or session cookies, an identity integration, and a relational database. This is a reference architecture, not a confirmed MUJ diagram. Microsoft says that ASP.NET includes both components within .NET Framework and external packages, so package and operating-system lifecycles must both be considered [18].

| Layer | Common behavior in this portal class | Security implication | Defensive evidence to request |
|---|---|---|---|
| Edge/CDN | The edge contacts an origin under configured origin settings [16]. | **Inference:** origin exposure, TLS, caching, and header trust must be reviewed separately from application logic. | Akamai property export, origin allow-list, authenticated origin pull configuration, cache rules, and TLS policy. |
| IIS and .NET | IIS hosts the application pool; ASP.NET components can be framework components or external packages [18]. | A banner such as ".NET 4.x" is not enough to establish support. | Exact Windows build, IIS role configuration, CLR version, assembly inventory, NuGet lock data, and patch evidence. |
| Web Forms state | In a farm, servers require consistent machine-key configuration or a ViewState generated on one server may fail validation on another [26]. ViewStateUserKey mismatches cause rejection [26]. | Poor key management can cause availability faults and, in vulnerable legacy designs, undermine trust in client-carried state. | Unique generated keys, protected secret storage, rotation process, and confirmation that unsafe legacy settings are disabled. |
| MVC or controller routes | Requests map to controller actions and business objects. | **Inference:** authorization must be enforced in controllers/services, not just by hiding menu items. | Role matrix, controller authorization conventions, negative authorization tests, and code-review evidence. |
| Identity | Entra Conditional Access can apply device, location, application, user, and risk signals and require MFA or compliant devices [10]. | Strong identity reduces account takeover but does not supply object-level authorization. | Conditional Access export, emergency-account controls, risky-sign-in response, and phishing-resistant MFA coverage. |
| Session | A session token binds authentication to HTTP traffic and the application's access controls [22]. | Theft, fixation, excessive lifetime, or failure to rotate after privilege change can extend an attacker's access. | Secure, HttpOnly, and SameSite cookies; idle and absolute timeouts; rotation after privilege changes [22]. |
| Database | Dynamic SQL that concatenates user input can produce SQL injection [24]. | A compromised application account can expose every record available to that account. | Parameterized queries, separate least-privilege accounts, query logging, and encrypted backups [24]. |

Microsoft's lifecycle data shows why exact versions matter. .NET Framework 4.5.2, 4.6, and 4.6.1 retired in 2022, while 4.6.2 reaches its listed end date in January 2027 [14]. Calling all of these ".NET Framework 4.x" collapses supported and unsupported states into one label. The same caution applies to "MVC 5.3": even if that package identification is correct, the assessment still needs package version, dependencies, Windows support, configuration, and deployed security updates.

**Case study - the load-balanced ViewState failure mode.** Microsoft documents that independently generated machine keys in a web farm cause servers to disagree about ViewState authenticity [26]. The immediate symptom can be intermittent MAC-validation errors rather than a clean security alert. The broader lesson is operational: legacy portal security depends on configuration consistency across every node, not just application source. A CDN or load balancer can make this inconsistency harder to diagnose because users move across layers before reaching an origin.

## Vulnerabilities and Breach Evidence by Vendor

Only one product in the reviewed set produced a strong, product-specific public vulnerability record: unsupported open-source Fedena 2.3. That finding should not be projected onto current commercial Fedena without version evidence, and it should not be projected onto MUJ. Conversely, the absence of a located advisory for another vendor does not establish safety.

| Vendor or product | Public vulnerability evidence located | Public breach evidence located in this review | Assessment |
|---|---|---|---|
| MUJ SLCM | No verified MUJ-specific advisory was located. | No verified public breach report was located. | Unknown, not "secure." The supplied stack remains an assessment lead. |
| SARAL School Soft | No credible product-specific advisory was located. | No credible product-specific breach report was located. | Evidence gap; obtain version and assurance records from Saral Computers. |
| GateWay | Entity unresolved. | Entity unresolved. | No meaningful search conclusion is possible until identity is corrected. |
| Hexad | No education ERP was established on the reviewed page [8]. | No MUJ-related breach report was located. | Exclude from the ERP risk table unless a contract or exact product is supplied. |
| Simpliance Vendor | Reviewed product is vendor-compliance SaaS, not a student ERP [5]. | No MUJ-related breach report was located. | Relevant only if MUJ separately uses it for compliance operations. |
| Jeewane? | Entity unresolved. | Entity unresolved. | Correct the spelling or provide a domain before further attribution. |
| MasterSoft | No credible product-specific advisory was located. | No credible confirmed breach report was located. | Public silence is not an assurance artifact. |
| Academia by Serosoft | No credible product-specific advisory was located. | No credible confirmed breach report was located. | Request private assurance documents and disclosure policy. |
| Fedena 2.3 open-source branch | Seven public findings: authentication bypass, RCE, SQL injection, broken access control, and three XSS issues [33]. | The reviewed research did not document compromise of a named institution. | Confirmed severe legacy vulnerabilities, but not a confirmed university breach. |
| TCS iON higher education | No credible product-specific advisory was located in this review. | No confirmed TCS iON Digital Campus breach was located. | Do not conflate unrelated TCS incidents with TCS iON. |
| Samarth eGov | No credible product-specific advisory was located. | No credible confirmed breach report was located. | Government sponsorship or broad deployment would not substitute for tenant-level assurance. |

### Fedena 2.3 case study: why version qualifiers control the verdict

Pentest Ltd reported seven findings specifically in Fedena School Management Software version 2.3. The reported classes were CVE-2021-27980 authentication bypass, CVE-2021-27974 remote code execution, CVE-2021-27979 SQL injection, CVE-2021-27976 broken access control, and CVE-2021-27975, CVE-2021-27977, and CVE-2021-27978 for XSS [33]. This is unusually strong public evidence because it names the product, version, vulnerability classes, and individual CVEs.

The authentication-bypass advisory says default Fedena 2.3 stored sessions client-side and used a statically set secret in the public repository; the researcher reported obtaining administrator-level access in the tested default configuration [30]. A companion report describes unauthenticated remote code execution and states that the publicly available secret could be used against instances retaining that value [34]. These are historical research findings, not instructions to reproduce them.

The remediation picture is more important than the exploit narrative. Pentest stated that the open-source version was unsupported, that no patches would be produced for the reported issues, and that migration to a supported product was its primary recommendation [33]. It also said WAF-based mitigation would be incomplete [33]. **Inference:** for an exact Fedena 2.3 match, replacement is the defensible strategy; for a modern Fedena tenant, the correct action is version confirmation and vendor evidence, not guilt by product name.

This case also disproves a purely Microsoft-centered market model. The historical Fedena repository explicitly identifies Ruby, Rails 2.3.5, and MySQL [32]. The common risk is therefore not ".NET" itself. It is long-lived business software with exposed identity, old dependencies, high-value data, weak defaults, and unclear maintenance ownership.

## How This Portal Class Behaves in Practice

The practical security model is a chain of state transitions: identify a user, create a session, select a role, request an academic object, change or publish state, and record the event. Each transition requires a different control.

| Workflow | Normal behavior | Representative failure class | Defensive requirement |
|---|---|---|---|
| Sign-in | Institutional, student, parent, faculty, or administrative identity starts a session. | Credential stuffing, phishing, enumeration, weak MFA. | Generic authentication responses and MFA; OWASP calls MFA the best defense against most password attacks [20]. Microsoft recommends phishing-resistant authentication for the strongest sign-in experience [21]. |
| Recovery | A user who forgot credentials restores access. | Helpdesk social engineering, weak identity proofing, recovery-token leakage. | Reauthentication after recovery or password reset and high-assurance recovery controls [20]. |
| Session continuity | The browser carries a session across portal actions. | Guessable, stolen, overlong, or unrotated session identifiers. | CSPRNG-generated meaningless identifiers with at least 64 bits of entropy, protected cookies, timeouts, and rotation after privilege changes [22]. |
| Record lookup | The user requests a student, course, marksheet, invoice, attendance record, or document. | IDOR or cross-tenant exposure. | Enforce server-side permission for every requested object [12]. |
| State-changing form | A user submits marks, fees, profile data, approvals, or preferences. | CSRF or missing business authorization. | Attach and validate backend CSRF tokens for POST, PUT, PATCH, and DELETE operations; use SameSite cookies [17]. |
| Search and reporting | Filters and identifiers become database queries. | SQL injection or over-broad export. | Prepared statements with variable binding and least-privilege database accounts [24]. |
| Publication | Approved results or circulars become visible to a wider audience. | Premature release, unauthorized change, stale cache, missing audit trail. | **Inference:** dual approval for high-impact publication, immutable audit events, cache review, and rollback capability. |
| Integration | ERP exchanges data with identity, payment, email, LMS, document, or analytics systems. | Excessive API scope, long-lived secrets, replay, or inconsistent revocation. | **Inference:** per-integration identities, narrow scopes, key rotation, signed requests where applicable, and correlated logs. |

This behavior explains why banner-based vulnerability hunting is inadequate. A fully patched framework can still implement broken object authorization. Conversely, a legacy-looking portal can be defensibly operated if its exact dependencies remain supported, configurations are hardened, identity is strong, database privileges are narrow, and business rules are continuously tested. The verdict must follow evidence at every layer.

## Defensive Research and Assurance Plan

The club should work only under written university authorization, with named systems, permitted test cases, time windows, data-handling rules, and a stop condition. Public OSINT can map ownership and documentation, but active testing should occur in a university-provided test tenant or isolated replica. No student record should be used as test data.

| Priority | Authorized action | Evidence produced | Decision enabled |
|---|---|---|---|
| 1 | Ask MUJ IT to export an exact inventory of Windows, IIS, CLR, MVC, NuGet packages, database version, Akamai configuration, and identity integration. | Versioned architecture and software bill of materials. | Determines whether any component is unsupported and replaces passive guesses. |
| 2 | Obtain contracts and data-flow diagrams naming the application owner, host, support provider, identity provider, payment processor, backup location, and subprocessors. | Legal entity and responsibility matrix. | Resolves the unsupported Saral, GateWay, Hexad, Simpliance, and Jeewane attribution hypotheses. |
| 3 | Review Entra configuration, including phishing-resistant MFA coverage, privileged-role policies, legacy-authentication blocking, device requirements, and risky-sign-in response. | Conditional Access export and control exceptions. | Measures account-takeover resistance against Microsoft's documented signal and grant model [10][21]. |
| 4 | Build a role-object-action matrix for student, parent, faculty, examiner, finance, helpdesk, and administrator personas. Test it only in an approved environment. | Negative and positive authorization test results. | Detects IDOR and horizontal or vertical privilege errors [12]. |
| 5 | Review session and recovery design. | Cookie settings, timeout values, session-rotation events, recovery audit logs. | Tests controls recommended by OWASP for secure sessions and reauthentication [22][20]. |
| 6 | Review state-changing requests and database access patterns in source or approved test tooling. | CSRF coverage, parameterization evidence, database account grants. | Detects missing CSRF validation and unsafe dynamic SQL [17][24]. |
| 7 | Verify edge-to-origin controls. | Origin allow-list, TLS configuration, direct-origin exposure assessment, cache and header rules. | Confirms whether Akamai is a controlled security boundary rather than an assumed one [16]. |
| 8 | Demand supplier assurance. | Current penetration-test executive summary, remediation SLA, vulnerability-disclosure policy, backup-restore evidence, incident contacts, and secure-development lifecycle summary. | Converts "no public CVE found" into a meaningful assurance decision. |
| 9 | Exercise incident response using synthetic records. | Detection timeline, containment actions, identity revocation, evidence preservation, communications draft, and restore results. | Shows whether MUJ can respond to account takeover, record tampering, ransomware, or supplier outage without touching production data. |

The priority order follows exposure and uncertainty. Inventory comes first because ".NET 4.x" spans retired and still-supported releases [14]. Identity comes next because a portal can expose multiple high-trust personas, but authorization review must follow immediately because strong MFA cannot prevent authenticated cross-record access [21][12]. Supplier assurance closes the largest public-information gap: current commercial products often advertise scope and scale while withholding implementation and patch details.

## Synthesis: The Vendor Name Matters Less Than the Control Boundary

| Dimension | MUJ SLCM | Previous-generation .NET portal class | Cloud education suites | Unsupported Fedena 2.3 |
|---|---|---|---|---|
| Evidence base | Public roles and functions are verified; stack and supplier are not [3][2]. | Microsoft documents component and package lifecycle rules [18]. | Vendors verify broad scope but disclose limited implementation detail [9][15][11]. | Product, version, seven CVEs, and unsupported status are publicly documented [33]. |
| Main security mechanism | Identity, role, object authorization, and academic workflow. | IIS/.NET patching, secure state and session configuration, controller authorization, database least privilege. | Tenant isolation, supplier operations, cloud IAM, API governance, and contractual assurance. | Migration away from the affected unsupported branch. |
| Main blind spot | Passive fingerprints may be mistaken for verified architecture. | Framework age may distract from business-logic and identity failures. | "Cloud" and scale claims may be mistaken for technical assurance. | WAF mitigation may be mistaken for a complete fix [33]. |
| Time horizon | Immediate inventory and control validation. | Continuous patch and configuration lifecycle. | Continuous supplier governance and tenant testing. | Urgent isolation and replacement if the exact affected version is present. |
| Confidence | High on function, low-to-medium on stack. | High as a reference model, not as MUJ attribution. | High on vendor-stated functionality, low on undisclosed internals. | High for the reported legacy findings. |

Three non-obvious conclusions follow. First, the vendor-identification problem is not clerical. If "Hexad" or "Simpliance" is incorrectly treated as the SLCM developer, risk owners may contact the wrong company, request the wrong evidence, and miss the real processor. Legal-entity normalization is therefore a security control.

Second, "behind Akamai" and "uses Microsoft 365" describe two strong control opportunities, not a security verdict. Akamai still depends on configured origin behavior [16], while Entra Conditional Access acts after first-factor authentication and can impose MFA, device, and risk requirements [10]. Neither layer can infer whether a parent should see student A or student B. That decision remains inside the ERP.

Third, Fedena shows that the sector's common denominator is not ASP.NET. The common denominator is long-lived, role-heavy software connected to valuable records and external systems. One historical product used Rails and MySQL [32]; other vendors disclose cloud delivery without a concrete stack [9][11]. A sound assessment therefore organizes evidence around identity, sessions, object authorization, workflow integrity, database privilege, origin security, supplier maintenance, and incident readiness.

## VERDICT

**Overall verdict: The public evidence supports an MUJ-branded, high-impact student lifecycle portal, but it does not support attributing that portal to any of the proposed vendors or independently confirming the complete supplied technology stack.** MAHE documentation verifies that SLCM handles attendance, marks, results, circulars, and student-parent academic access [3]. MUJ's landing page verifies the portal identity and role-facing surface but not a product or framework version [2].

**Risk verdict: Medium-High inherent risk, Unknown residual risk.** The inherent rating follows the sensitivity and integrity importance of academic records and the number of likely trust boundaries. Residual risk cannot be scored responsibly without exact inventory, identity-policy exports, authorization tests, origin configuration, logging evidence, and supplier assurance.

**Vendor verdict:**

| Finding | Confidence |
|---|---|
| Saral School Soft is a real education ERP from Saral Computers. | High [6] |
| MasterSoft, Academia, Fedena, TCS iON, and Samarth belong in the broader Indian education-system landscape. | High for the first four products [9][23][15][11]; medium for Samarth based on the reviewed material [13]. |
| Hexad and Simpliance are not demonstrated as university ERP products by the reviewed pages. | High [8][5] |
| GateWay and "Jeewane" identify unique ERP suppliers. | Low; unresolved. |
| Any named vendor powers MUJ SLCM. | Low; no public attribution evidence located. |
| The exact MUJ deployment is ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, Microsoft 365, and SQL Server. | Low-to-medium as a user-supplied hypothesis; not independently verified as a complete stack. |
| Unsupported Fedena 2.3 has seven documented serious vulnerability findings. | High [33] |
| Those Fedena findings apply to MUJ or every current Fedena tenant. | Very low; no such attribution or version match exists. |

**Final confidence: Medium.** Confidence is high on SLCM's documented functions, the categorization of the verified vendors, Microsoft and OWASP defensive guidance, and the Fedena 2.3 case. Confidence is low on MUJ's exact versions, database, origin architecture, implementation partner, and residual vulnerability state. The decisive next step is not broader unauthenticated probing; it is an authorized evidence request and controlled assessment using synthetic data.

## References

1. [
	MU SLcM
](https://slcm.manipal.edu/)
2. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
3. *Contents*. http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf
4. *Manipal University*. https://muj.slcm.jaipur.manipal.edu/
5. *Vendor Audit Software | Vendor Compliance Tool | Simpliance Vendor*. https://www.aparajitha.com/products/vendor-audit
6. *Welcome to SARAL School Soft...an ERP Solution...Developed by Saral Computers Pvt. Ltd...in service since 1990*. http://erp.saral.in/sch
7. *Mastersoft ERP Solutions Pvt.Ltd - Student Portal*. https://cimsstudentnewui.mastersofterp.in/
8. *Hexad*. https://www.hexad.in/
9. *Education ERP Solutions & Modules | Academia by Serosoft*. https://serosoft.com/solutions
10. *Microsoft Entra Conditional Access: Zero Trust Policy Engine - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/conditional-access/overview
11. [
	Education ERP Campus Software for Schools & Higher Ed | MasterSoft ERP Solution
](http://iitms.co.in/)
12. *Insecure Direct Object Reference Prevention - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html
13. *Samarth eGov*. https://samarth.edu.in/
14. *Microsoft .NET Framework - Microsoft Lifecycle | Microsoft Learn*. https://learn.microsoft.com/en-us/lifecycle/products/microsoft-net-framework
15. [
    TCS iON: Achieving Excellence in Higher Education Institutions
  ](https://www.tcsion.com/institutions/higher-education)
16. *Origin Server*. https://techdocs.akamai.com/property-mgr/docs/origin-server
17. *Cross-Site Request Forgery Prevention - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
18. *ASP.NET official support policy | .NET*. https://dotnet.microsoft.com/en-us/platform/support/policy/aspnet
19. *ASP.NET Web Forms | Microsoft Learn*. https://learn.microsoft.com/en-us/aspnet/web-forms
20. *Authentication - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
21. *Microsoft Entra authentication overview - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/authentication/overview-authentication
22. *Session Management - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
23. *School Management Software & School Management System - Fedena*. https://fedena.com/
24. *SQL Injection Prevention - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
25. *Leading Educational ERP Software & Student Information System | Serosoft*. https://serosoft.com/
26. *Resolving view state message authentication code (MAC) errors | Microsoft Support*. https://support.microsoft.com/en-US/servicing/DotNetFramework/troubleshooting/resolving-view-state-message-authentication-code-mac-errors
27. *fedena/doc/README_FOR_APP at master · projectfedena/fedena · GitHub*. https://github.com/projectfedena/fedena/blob/master/doc/README_FOR_APP
28. *GitHub - mazhar266/fedena: Fedena, Open Source School Management System · GitHub*. https://github.com/mazhar266/fedena
29. *GitHub - projectfedena/fedena_v2.1 · GitHub*. https://github.com/projectfedena/fedena_v2.1
30. *Authentication Bypass - Fedena School Management | Pentest*. https://pentest.co.uk/labs/fedena-authentication-bypass-cve-2021-27980/
31. *NVD - Search and Statistics*. https://nvd.nist.gov/vuln/search
32. *GitHub - projectfedena/projectfedena_v2.0: Source Code for Fedena version 2.0 · GitHub*. https://github.com/projectfedena/projectfedena_v2.0
33. *Vulnerabilities - Fedena School Management | Pentest*. https://pentest.co.uk/labs/research/fedena-school-management-software/
34. *CVE's*. https://chris-young.net/cves/
