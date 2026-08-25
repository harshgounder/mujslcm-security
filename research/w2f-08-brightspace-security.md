# MUJ Brightspace Security: Evidence, Integrations, and Risk Boundaries

## Executive Summary

- **Public CVE Record Is Narrow**: The reviewed Brightspace-specific OpenCVE query returned one result, CVE-2021-43129, while NVD provides no CVSS score, CPE/version range, or named patched version [17][4]. This means the public CVE count is a weak proxy for total product risk -> MUJ should obtain D2L customer advisories and its exact hosted release history rather than treating one public CVE as proof of low risk.
- **Known CVE Has Limited Stated Impact**: CVE-2021-43129 bypasses the quiz feature's "Disable Right Click" control and permits print/copy behavior [4]. NVD does not describe remote code execution, account takeover, or data exfiltration -> classify it as an assessment-integrity and control-design issue unless additional vendor evidence shows broader impact.
- **Most Concrete Incident Is Identity-Led Abuse**: REN-ISAC reports criminals using compromised institutional accounts and permissive Brightspace email defaults for high-volume phishing; cloud-hosted email could bypass controls in an institution's own mail service [8]. This was not presented as a Brightspace code vulnerability -> strengthen identity, role, email-recipient, and anomaly controls before focusing exclusively on CVEs.
- **SAML Is Publicly Evidenced, OIDC Is Only a Supported Option**: A passive request to `student.onlinemanipal.com/s/` led to a tenant-specific Microsoft `login.microsoftonline.com/.../saml2` flow [23]. D2L documents Azure-certified SAML support and separately identifies OIDC as an option requiring Implementation Services [3] -> treat SAML as evidenced for the student portal, but do not claim that MUJ Brightspace or SLCM uses OIDC without configuration evidence.
- **Stable Identity Mapping Is Critical**: Microsoft says applications should identify users with stable `sub` or `oid` values, optionally combined with `tid`, and should not use mutable email, phone, or UPN values as durable identifiers [9]. A grade-bearing integration must therefore map an immutable institutional person key, not an email address, across Entra, Brightspace, and SLCM.
- **Grade Sync Is a High-Integrity Trust Boundary**: Brightspace APIs can create, update, and delete grade objects; replace individual grade values; recalculate final grades; and set adjusted final grades under granular scopes [15]. OneRoster 1.2 likewise defines result read/write/delete operations protected by OAuth 2.0 Client Credentials and TLS [31] -> protect integration credentials like privileged service identities and independently reconcile every posted grade.
- **Brightspace Supports SIS Grade Passback, but MUJ Use Is Unproven**: D2L documents scheduled SIS pulls, optional grade passback during daily synchronization, manual faculty sync, OAuth credentials, and audit-log review [29]. No reviewed public source connects those functions specifically to MUJ SLCM -> any proposed SLCM-to-Brightspace data flow in this report is explicitly an inference, not a finding.
- **Online Manipal Shows a Split Public Surface**: `learning.onlinemanipal.com` publicly identifies itself as powered by D2L Brightspace [6], while the student portal initiates Microsoft SAML [23]. This suggests separate learning and student-service boundaries -> review session, account-linking, and lifecycle behavior at every transition rather than assuming one shared security control plane.
- **Public Posture Is Not a Penetration Test**: The main domain publishes a permissive robots file and sitemap [26], while the parsed response for `/.well-known/security.txt` looked like normal homepage content and did not expose an RFC-style contact in the reviewed evidence [19]. These observations say little about vulnerability resistance -> obtain header, TLS, WAF, logging, and disclosure evidence from authorized owners instead of inferring weakness from missing public documentation.
- **Authorized Research Boundary Is Explicit**: D2L's policy covers specified D2L systems but says customer-instance testing requires the customer's authorization; it excludes denial of service, phishing, exfiltration, persistence, and pivoting [2]. The university club should remain in passive OSINT unless MUJ and relevant vendors provide written scope.

## 1. Scope, Evidence Classes, and Safety Boundaries

This report evaluates public evidence concerning D2L Brightspace, Microsoft 365 or Entra SSO, SIS grade exchange, and Online Manipal. It does not claim that a generic Brightspace capability is enabled in MUJ's tenant. It also does not claim that a public CVE affects MUJ without an affected-version range and a verified MUJ release.

The supplied description of `mujslcm.jaipur.manipal.edu` as ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10 behind Akamai, with Microsoft 365 identity is treated as a user-provided working assumption. This research did not independently validate those framework, server, CDN, or identity versions. In particular, a banner, indexed technology label, or CDN response must not be treated as proof of the origin server's complete software inventory.

The report does not expose private chain-of-thought. Instead, it supplies an auditable evidence-to-conclusion trail: each material finding has a sentence-level citation, every architecture conclusion not directly shown by a source is labeled **Inference**, and exact source URLs appear in the References table.

| Evidence class | Meaning in this report | Example | Decision rule |
|---|---|---|---|
| Direct public evidence | A first-party page, standards document, government record, or passively returned public page states the fact | NVD's CVE description; D2L's API documentation | May support a finding within the source's stated scope |
| Corroborating public evidence | An independent organization documents operational abuse or implementation behavior | REN-ISAC's Brightspace email-fraud alert | May support incident analysis, but not an unmentioned root cause |
| User-provided assumption | A fact supplied in the research prompt but not independently confirmed here | SLCM's asserted IIS, .NET, Akamai, and MVC stack | Useful for scoping only; not a verified finding |
| Inference | A reasoned model connecting separate facts | An SLCM grade-sync service would probably be a privileged middleware boundary | Must be labeled and must not be presented as deployed reality |
| Unknown | Public evidence is insufficient | Whether MUJ uses OIDC for Brightspace; whether SLCM receives grades through OneRoster | Requires owner-supplied configuration, logs, or contracts |

D2L provides a safe-harbor policy for good-faith work performed within its rules, but the policy says testing a customer instance requires authorization from that customer [2]. It prohibits DoS or DDoS, physical and social-engineering tests, exploit-driven data exfiltration, persistent access, and pivoting [2]. Reports can be sent to D2L, and D2L says it will normally acknowledge a report within three business days when contact information is supplied [2].

Accordingly, this report used only public search, public documentation, passive retrieval of public landing pages, and public standards. It provides no instructions for bypassing authentication, manipulating grades, probing hidden endpoints, decoding the observed SAML request, or testing MUJ systems without permission.

**Decision-ready insight:** The first governance task is not scanning. It is obtaining a written asset and integration inventory from MUJ, identifying system owners, and recording which party authorizes testing for SLCM, Online Manipal, D2L, Entra, and any integration middleware.

## 2. Brightspace CVEs in the 2020s: One Public Record, Many Caveats

### 2.1 Catalog result

The Brightspace product query reviewed on OpenCVE displayed **one result**, CVE-2021-43129, and "Page 1 of 1" [17]. NVD describes the issue as a bypass of Brightspace's "Disable Right Click" quiz option, allowing a quiz taker to reach print and copy functions through the browser context menu even when the option is enabled [4]. NVD lists April 19, 2022 as its publication date and June 17, 2026 as its last modification date [4].

| CVE | Product behavior | Security property implicated | Public severity/version data | MUJ applicability |
|---|---|---|---|---|
| CVE-2021-43129 | "Disable Right Click" can be bypassed during a quiz, allowing print/copy behavior [4] | Assessment integrity and reliance on a client-side deterrent | NVD has no NIST CVSS assessment; CWE is "Other"; the reviewed page supplies no usable CPE/version range [4] | **Unknown.** No affected-version range or MUJ Brightspace build was verified |

This table should not be read as a statement that Brightspace had only one security defect in the 2020s. It means that the specific public product query returned one CVE. Private vendor advisories, non-CVE bugs, tenant configuration weaknesses, dependency CVEs, and customer-side identity incidents can all exist outside that result. OpenCVE itself is an aggregation view, while NVD says no specific patched release on the reviewed record [4].

### 2.2 Impact interpretation

**Inference:** The CVE's described impact is narrower than confidentiality loss, account takeover, or server compromise. It weakens an exam-control expectation by showing that a browser-side restriction is not an effective content-protection boundary. Because NVD has not assigned a CVSS score, this report does not invent one [4].

The defensive lesson is broader than the individual UI bypass. A browser under the student's control cannot provide a strong guarantee against copying, photographing, printing, accessibility-tool use, or content capture. High-stakes assessment integrity should therefore combine question randomization, time windows, appropriately designed open-book assessments, anomaly review, and clear academic-integrity rules. Those are governance and assessment-design controls, not claims about a software patch.

### 2.3 Vendor posture does not replace tenant validation

D2L publicly states that Brightspace connections use TLS, user sessions are uniquely identified and reverified, application logs include creator, update time, timestamps, and originating IP, and customer data is logically separated [13]. D2L also describes external firewalls, intrusion detection and prevention, SIEM, continuous vulnerability scanning, external penetration testing, and disaster-recovery replication [13]. Its compliance page describes ISO/IEC 27001:2022 as independently audited alignment of the D2L ISMS and security controls [10].

These are meaningful vendor-control representations, but they are not proof that MUJ's tenant has secure SSO mappings, least-privilege roles, safe mail permissions, correct session settings, or an intact grade-sync pipeline. Certification scope and application configuration are different evidence classes.

**Decision-ready insight:** Ask D2L or the institutional contract owner for the tenant's release history, security advisory record, penetration-test executive summary, SOC report, subprocessor list, recovery objectives, and incident-notification process. Then compare those materials with the actual tenant configuration. Do not use the public CVE count as the risk rating.

## 3. Public Incidents: Configuration and Identity Can Dominate Product CVEs

### 3.1 Brightspace email fraud

REN-ISAC reports that criminals used compromised institutional accounts and Brightspace's default behavior to send high-volume phishing. The alert says default configurations did not throttle outgoing email and cloud-hosted instances could use D2L email infrastructure in a way that bypassed an institution's own email-service controls [8]. It does not identify a Brightspace code vulnerability or name affected institutions, although it acknowledges Minnesota State Colleges and Universities for helping with the issue [8].

| Event or evidence | What is directly supported | What is not supported | Defensive implication |
|---|---|---|---|
| CVE-2021-43129 | Quiz right-click restriction bypass [4] | Server compromise, credential theft, or data breach | Avoid treating client-side deterrents as security boundaries |
| REN-ISAC Brightspace email fraud | Compromised institutional accounts plus permissive mail behavior enabled bulk phishing [8] | A D2L code flaw or a confirmed MUJ incident | Apply MFA, role-based mail permissions, recipient limits, and alerting |
| D2L global status observation | The page reported all services operational and no reported organization outages over the preceding 90 days [22] | Historical proof of perfect uptime or MUJ-specific availability | Use tenant-specific monitoring and contractual incident records |

REN-ISAC recommends limiting contacts to active courses, restricting recipient counts, configuring BCC and role-based permissions, and reducing email capabilities in very large courses [8]. The mechanism is important: one compromised account becomes more damaging when the application grants it broad messaging reach and when the resulting messages avoid familiar institutional mail controls.

### 3.2 Availability evidence has a narrow scope

At the time of retrieval, D2L's status page displayed "All Services Operational" and separately monitored Authentication, APIs, Grades Tool, Quizzing, and Integrations [22]. The same page warns that it is not a direct uptime monitor, that status updates may be delayed, and that the global view represents clients generally unless a specific Brightspace URL is supplied [22].

This point-in-time evidence cannot establish MUJ's historical availability or exclude tenant-specific incidents. It is useful primarily because it shows which service categories D2L distinguishes operationally.

**Decision-ready insight:** MUJ should correlate Entra sign-in risk, Brightspace authentication and email logs, D2L status notifications, and institutional mail telemetry. A product-CVE-only monitoring program would miss the clearest public abuse pattern.

## 4. Microsoft 365 SSO: SAML Is Evidenced, OIDC Remains a Design Option

### 4.1 What the public pages prove

The public learning page at `learning.onlinemanipal.com` contains a username field, password-recovery link, and "Powered by D2L Brightspace" attribution [6]. A passive retrieval of `student.onlinemanipal.com/s/` led to a tenant-specific Microsoft `login.microsoftonline.com` SAML endpoint containing a signed SAML request flow [23]. This supports the conclusion that the student portal uses Microsoft Entra SAML for that observed login path.

It does **not** prove that the Brightspace learning page uses the same SAML application, that SLCM uses that tenant, that OIDC is enabled anywhere, that authentication succeeded, or that account claims are mapped correctly. The observed request was not decoded or replayed.

D2L describes SAML as its most commonly requested Brightspace SSO method and says the workflow is customer managed through an administration front end [3]. D2L lists Azure among the identity providers against which its implementation is certified [3]. D2L also lists OIDC, LDAP, GUID SSO, and CAS as other options, but says those lack the SAML self-service capability and require Implementation Services [3].

### 4.2 OIDC and SAML comparison

| Dimension | OIDC with Microsoft Entra | SAML with Microsoft Entra | MUJ/Online Manipal evidence |
|---|---|---|---|
| Core artifact | Signed JWT ID token; OIDC extends OAuth 2.0 for authentication [14] | Signed SAML token sent to the service provider | SAML request observed at the student portal [23] |
| Typical flow | Authorization code is redeemed at the token endpoint; `state` and `nonce` protect the flow [14] | Browser carries an assertion from Entra to the application's assertion consumer endpoint | Exact Brightspace SAML topology is not public |
| Validation | Validate signature and applicable claims with a standard library [14] | Validate signature against current federation metadata and signing keys [21] | Configuration unknown |
| Identity key | Prefer stable `sub` or `oid`, with `tid` where cross-service tenant context is needed [9] | NameID or mapped claim must be selected deliberately | Public claim mapping unknown |
| Brightspace administration | D2L says OIDC requires Implementation Services [3] | D2L provides a self-service SAML administration tool with logging and default-login controls [3] | SAML is the better-supported public hypothesis, but only for the observed student portal |
| Certificate/key lifecycle | Discovery and key rollover should be handled programmatically | Federation metadata and certificate rollover must be monitored | No public evidence of MUJ's rollover process |

### 4.3 OIDC validation requirements

Microsoft's OIDC documentation says the authorization request should contain `openid`, a registered redirect URI, a random `state`, and a `nonce`; the returned `state` and token `nonce` must match their original values [14]. The application must validate the ID token's signature and claims and should use a token-validation library rather than implementing validation manually [14].

Microsoft identifies `aud` as the intended token recipient and says a token should be rejected if it does not match the application's ID. It also identifies `iss`, `exp`, `nbf`, and `nonce` as security-relevant claims [9]. Microsoft warns that email, phone, and UPN values can change or be reused and recommends stable `sub` or `oid` identifiers [9].

**Inference:** If MUJ ever uses OIDC between Entra and Brightspace, SLCM, or integration middleware, using email as the cross-system primary key could misassociate a recycled or changed address with the wrong academic record. The durable mapping should bind an immutable institutional person identifier to the appropriate Entra `oid` and tenant context, with controlled reconciliation when records merge or change.

### 4.4 SAML certificate and session lifecycle

Microsoft says token signatures must be validated with public keys in the tenant's OIDC discovery or SAML/WS-Fed federation metadata [21]. Applications should handle rollover programmatically, be prepared for multiple simultaneously valid keys, and refresh metadata when an unknown key identifier is encountered [21]. A stale, manually pinned certificate can therefore become an availability failure even when there is no attack.

Conditional Access creates another boundary. Microsoft defines sign-in frequency as how long a user can use a resource before signing in again, and its documented default is a rolling 90-day window when the session's security posture has not changed [12]. Password changes, noncompliant devices, and disabled accounts can revoke sessions [12]. Microsoft also warns that frequent prompts can cause MFA fatigue and phishing risk, while persistent browser cookies and excessive token caching can outlive the session behavior an administrator intended [12].

| SSO failure case | Mechanism | Consequence | Defensive control |
|---|---|---|---|
| Mutable claim used as primary key | Email or UPN changes or is reused | Wrong account may link to an academic identity | Use immutable `oid`/`sub` plus institutional person ID |
| Audience or issuer not constrained | Token for another recipient or tenant is accepted | Cross-application or cross-tenant confusion | Validate signature, audience, issuer, nonce, time claims, and tenant |
| Stale SAML certificate | Service provider trusts only an expired key | Login outage during rollover | Consume and monitor federation metadata; retain tested break-glass access |
| Long-lived local LMS cookie | Application does not return to Entra for reevaluation | Disabled or risky user may retain a local session longer than expected | Align local session timeouts with Entra policy and test revocation |
| Excessive reauthentication | Users receive repeated MFA prompts | MFA fatigue and increased phishing susceptibility | Apply risk-based policy to sensitive roles and actions |
| Orphaned privileged account | SIS/HR lifecycle does not remove LMS role | Former or transferred user retains access | Automate deprovisioning and run periodic entitlement reconciliation |

**Decision-ready insight:** The security club should ask identity administrators for a redacted SAML/OIDC configuration review, not attempt the login flow. The review should cover tenant restriction, immutable identifier mapping, assertion/token lifetime, signing-key rollover, local-session invalidation, MFA and Conditional Access, break-glass access, and deprovisioning latency.

## 5. Grade Sync With SIS/SLCM: The Highest-Integrity Integration Boundary

### 5.1 What OneRoster and Brightspace support

1EdTech states that OneRoster exchanges people, courses, enrollments, organizations, and grades through CSV or REST patterns [5]. Its gradebook model includes categories, line items, results, score scales, assessment line items, and assessment results [5].

The OneRoster 1.2 Gradebook REST binding requires OAuth 2.0 Client Credentials, bearer-token authorization, scopes, and TLS; TLS 1.2 or 1.3 is required and SSL must not be used [31]. The binding includes operations to read all results, read class results, post results for a line item, update a result, and delete a result [31].

D2L's Brightspace OneRoster preparation guide says scheduled pulls can populate schools, classes, users, and enrollments. It maps OneRoster grade categories to Brightspace grade categories, line items to grade items, and results to scores [29]. Where the SIS supports grade passback, administrators can return grades during daily synchronization or permit faculty to initiate a manual sync [29]. D2L tells administrators to generate a OneRoster consumer, record OAuth credentials and the SIS endpoint, configure IPSIS Administration, and inspect the IPSIS Audit Log after processing [29].

### 5.2 Supported integration patterns and MUJ status

| Pattern | Publicly documented mechanism | Advantages | Main risks | MUJ status |
|---|---|---|---|---|
| IPSIS plus OneRoster REST | Scheduled SIS pull, optional grade passback, OAuth credentials, audit log [29] | Standardized objects, scheduled and manual modes, vendor-supported mapping | Broad client credentials, mapping errors, stale or duplicated writes | **Unknown** |
| OneRoster CSV batch | OneRoster supports CSV exchange [5]; D2L documents ZIP-based CSV processing [29] | Simple and inspectable for batch transfer | File exposure, stale data, partial processing, weaker immediacy | **Unknown** |
| Brightspace native Grades API | Granular operations and scopes for grade objects and grade values [15] | Fine-grained application control and near-real-time workflows | Custom code, token storage, overwrite semantics, object authorization | **Unknown** |
| Manual institutional export/import | Institutionally controlled administrative process | Strong human approval for low volume | Delay, transcription error, weak scalability | **Unknown** |

**Inference:** Any of these could connect Brightspace to SLCM, but no reviewed public source proves that MUJ uses one. The presence of Brightspace and SLCM in the same educational ecosystem is not evidence of a direct API connection. There may be middleware, a data warehouse, a manual process, a different SIS product, or no automated grade flow.

### 5.3 Native Grades API has powerful write semantics

Brightspace's documented API can create, update, read, and delete grade objects under separate scopes [15]. It can read grade values, replace a user's value, recalculate final grades, and set an adjusted final grade [15]. D2L notes that updates replace all associated object or value data and that a grade-value type must match the grade-object type [15].

Brightspace recommends OAuth 2.0 over its proprietary ID Key authentication. Its guide describes creating an OAuth application, obtaining initial access and refresh tokens for a user, sending the access token in API request headers, and using refresh-token rotation as access tokens expire [20].

| Grade-data control objective | Why it matters | Minimum defensive evidence |
|---|---|---|
| Least privilege | A token capable of setting final grades has high integrity impact | Exact client scopes, owner, permitted courses, and prohibited operations |
| Immutable subject mapping | Email-based mapping can change or collide | Institutional person ID tied to stable Entra and SIS identifiers |
| Idempotency and replay control | Retry logic can duplicate or overwrite results | Correlation ID, source timestamp, version check, and replay-safe design |
| Directionality | A two-way sync can create loops or stale overwrites | Authoritative source defined separately for roster, line item, raw score, and final grade |
| Reconciliation | API success does not prove semantic correctness | Counts, totals, exception reports, and sampled source-to-target comparison |
| Approval separation | One compromised integration identity should not silently finalize grades | Separate service identity, change approval, and privileged-action alerting |
| Secret lifecycle | Client secret or refresh token compromise enables automated access | Managed secret storage, rotation, revocation drill, and no human sharing |
| Audit retention | Grade disputes require a defensible record | Before/after value, actor/client ID, source system, timestamp, course, learner, and reason |
| Failure containment | Partial batches can leave systems inconsistent | Quarantine queue, retry limits, rollback process, and visible error ownership |

### 5.4 Case study: scheduled grade passback

D2L's documented OneRoster implementation provides the concrete case. An administrator records an SIS endpoint and OAuth credentials, schedules a daily pull, optionally enables grades to return during that synchronization, and reviews IPSIS Audit Log processing [29]. The decision is operationally efficient because roster and grade exchanges use a shared, standardized model.

The same efficiency creates concentration risk. A single client credential and mapping configuration can affect many classes. If a user identifier is mapped incorrectly, a stale result is accepted as current, or a full-object update overwrites fields unexpectedly, the integration can produce valid-looking but academically incorrect records. That is an **inference from the documented write and mapping capabilities**, not evidence that such an event occurred at MUJ.

The recommended control is a two-stage integrity design: the integration writes to a staging or review state where feasible, and an independent reconciliation checks course, learner, line-item, score, grading period, and source timestamp before academic finalization. High-impact exceptions should require human approval, while routine successful records still retain machine-readable provenance.

**Decision-ready insight:** Before asking "Is the API secure?", define the authoritative system for each data element. Roster ownership may belong to SLCM, formative scores to Brightspace, and official final grades to SLCM. Security depends on enforcing those directional rules, not merely encrypting the connection.

## 6. Public Security Posture of OnlineManiapal.com

### 6.1 Direct observations

| Public surface | Direct evidence | Security meaning | Important limitation |
|---|---|---|---|
| `learning.onlinemanipal.com` | Public page says "Powered by D2L Brightspace" [6] | Confirms a D2L-hosted learning surface | Does not reveal tenant settings, release, or SSO configuration |
| `student.onlinemanipal.com/s/` | Passive fetch initiated a tenant-specific Microsoft SAML flow [23] | Confirms an Entra SAML authentication path for that portal | Does not prove successful login, claim mapping, MFA, or linkage to Brightspace |
| `www.onlinemanipal.com/robots.txt` | Allows general crawlers and publishes a sitemap URL [26] | Supports ordinary public discovery | Robots directives are not access control and reveal no vulnerability |
| `learning.onlinemanipal.com/robots.txt` | Disallows `/content/` and `/shared/` to crawlers [24] | Expresses crawler preferences for learning content paths | Does not restrict authenticated users or attackers |
| `www.onlinemanipal.com/.well-known/security.txt` | Parsed response contained normal homepage-style material rather than visible RFC-style security contact fields [19] | Public disclosure contact was not demonstrated by this response | Could be routing or parsing fallback; absence is not proven |
| D2L global status | Operational when checked; global view is not a direct uptime monitor [22] | Provides vendor-wide operational context | Not Online Manipal or MUJ tenant-specific assurance |

These findings establish platform attribution and identity-routing clues, not vulnerability resistance. No claim is made here about HTTP security headers, cookie flags, TLS cipher quality, DNSSEC, SPF, DKIM, DMARC, WAF efficacy, Akamai configuration, origin exposure, or software patch status because this research did not obtain reliable public evidence for those points.

### 6.2 Posture strengths visible in public documentation

The learning platform benefits from D2L's publicly represented baseline controls, including TLS, transaction-level session reverification, logging, logical tenant separation, continuous vulnerability scanning, and external penetration testing [13]. D2L also publishes a detailed vulnerability-disclosure policy and identifies a reporting channel [2]. The student portal's use of Microsoft SAML creates an opportunity to apply centralized identity policy, although the public flow does not reveal which Conditional Access or MFA rules are active.

### 6.3 Evidence gaps

The most important gaps are configuration and ownership records:

| Gap | Why it blocks a stronger conclusion | Owner-supplied evidence to request |
|---|---|---|
| No public Brightspace tenant release/build | Prevents CVE applicability analysis | D2L release history and security-advisory mapping |
| No public SAML/OIDC claim map | Prevents assessment of account-binding safety | Redacted enterprise-app claims and unique-user mapping |
| No public local-session configuration | Prevents evaluation of Entra revocation propagation | Brightspace session timeout and logout design |
| No public SLCM integration diagram | Prevents confirmation of automated grade sync | Data-flow diagram, API inventory, middleware owner, and data dictionary |
| No demonstrated security.txt contact on the reviewed main-domain response | Makes public responsible disclosure less discoverable | Official security contact and coordinated-disclosure page |
| No tenant-specific status history | Prevents historical availability or incident conclusions | D2L tenant notices, help-desk records, and contractual incident reports |

**Inference:** The split between a D2L learning host and an Entra-backed student portal increases the importance of secure handoffs. It does not inherently indicate weakness. The key questions are whether both surfaces map the same person consistently, whether logout and deprovisioning propagate, and whether privileged grade actions require stronger controls than ordinary course viewing.

**Decision-ready insight:** Public OSINT supports a moderate-confidence architectural picture, but not a security grade. A responsible public posture assessment should say "not publicly evidenced" rather than translate missing documentation into a negative scanner score.

## 7. Defensive Roadmap for the University Security Club

All activities below are governance, documentation review, or owner-authorized validation. None requires testing production endpoints without permission.

| Priority | Defensive action | Deliverable | Success criterion |
|---|---|---|---|
| P0 | Establish written authorization and system ownership | Scope signed by MUJ, D2L relationship owner, and relevant platform owners | Every asset and data flow has an accountable owner and permitted test class |
| P0 | Produce an authoritative architecture diagram | SLCM, Entra, student portal, Brightspace, middleware, mail, and logging flows | Every trust boundary, protocol, credential type, and authoritative data source is shown |
| P0 | Inventory privileged identities and secrets | Human admins, service principals, OAuth clients, refresh tokens, and break-glass accounts | No unknown owner; all secrets have rotation and revocation dates |
| P1 | Review SAML/OIDC mappings | Redacted issuer, audience, redirect/ACS, NameID/claim, and tenant settings | Immutable identity key; no email-only account binding |
| P1 | Test lifecycle behavior in an authorized non-production tenant | Joiner, transfer, withdrawal, disablement, password reset, and role-removal cases | Access and grade privileges disappear within the approved service level |
| P1 | Review grade-sync integrity | Data dictionary, directionality matrix, reconciliation report, and rollback runbook | Every official grade has source, time, actor/client, and before/after provenance |
| P1 | Restrict Brightspace email capabilities | Role and recipient policy aligned to REN-ISAC recommendations | Compromised low-privilege accounts cannot send institution-wide mail |
| P2 | Correlate monitoring | Entra, Brightspace, IPSIS/API, mail, and SLCM event use cases | Alerts cover anomalous login, mass mail, token use, bulk grade change, and sync failure |
| P2 | Formalize vendor evidence review | Annual D2L SOC/certification/advisory and recovery review | Findings map to tenant controls and tracked remediation owners |
| P2 | Publish a disclosure route | RFC 9116-style security contact or clearly linked policy | Researchers can find an authorized reporting channel without probing |
| P3 | Run incident exercises | Tabletop for compromised faculty account, stale SAML key, and incorrect grade batch | Owners can revoke, contain, reconcile, communicate, and recover within targets |

The club can contribute safely by preparing threat models, reviewing public standards, building checklists, and analyzing sanitized configuration exports supplied by administrators. It should not attempt credential testing, SAML replay, API calls, grade changes, fuzzing, content bypass, subdomain takeover checks, or origin discovery without explicit written authorization and a non-production plan.

## 8. Synthesis

The ecosystem has four distinct security mechanisms that should not be collapsed into one "LMS security" score.

| Dimension | D2L product security | Microsoft identity | SIS/grade integration | Public web posture |
|---|---|---|---|---|
| Primary mechanism | Hosted application controls, tenant roles, sessions, logs, and release management | SAML/OIDC assertions, MFA, Conditional Access, and lifecycle | OAuth client credentials, mappings, write scopes, schedules, and reconciliation | TLS-facing pages, public routes, disclosure material, and service attribution |
| Main evidence | NVD, D2L security and API documentation | Microsoft protocol guidance and observed SAML redirect | OneRoster 1.2 and D2L IPSIS/Grades API documentation | Online Manipal landing pages, robots responses, and D2L status |
| Dominant risk | Configuration or non-CVE defect hidden by a small public CVE count | Account compromise, claim confusion, stale session, or rollover failure | Silent integrity loss through wrong identity, direction, or overwrite | Overinterpretation of sparse public signals |
| Blast radius | Course, tenant, or shared service | Potentially every federated application for an identity | Many learners and official academic records | Primarily discovery and reputation unless linked to a real weakness |
| Best control | Exact release and tenant configuration evidence | Immutable identifiers and tested session/key lifecycle | Least privilege plus independent reconciliation | Clear disclosure route and owner-authorized assurance |
| Evidence confidence | Medium | High for student-portal SAML, low for Brightspace OIDC | High for product capability, low for MUJ deployment | Medium for direct observations, low for unobserved controls |

The non-obvious tension is that the only cataloged Brightspace CVE found is narrow, while the most operationally consequential public scenario involves compromised accounts and email permissions. The mechanism shifts the priority from patch counting to identity and authorization design. A perfectly patched LMS can still amplify a stolen account if the role can reach too many recipients [8].

A second tension is between centralized identity and local application sessions. Entra can revoke or challenge a session, but Microsoft warns that local cookies and token caching affect whether the application returns for reevaluation [12]. Centralized MFA therefore does not automatically prove immediate Brightspace or portal revocation.

The third tension is between integration efficiency and academic integrity. OneRoster and Brightspace APIs standardize high-volume grade movement, but the same automation increases blast radius. OAuth 2.0 and TLS protect the channel and client authentication [31]; they do not prove that the right learner, course, line item, grading period, or authoritative source was selected. Semantic reconciliation is as important as cryptography.

Finally, the public Online Manipal surface provides enough evidence to identify D2L and Entra components, but not enough to score implementation quality. The correct analytical outcome is a bounded model with explicit unknowns, not a speculative vulnerability list.

## VERDICT

**Overall verdict: No public evidence reviewed here establishes a presently exploitable MUJ Brightspace, SLCM, or Online Manipal vulnerability. Overall confidence: MODERATE.**

The strongest findings are:

1. The reviewed public Brightspace catalog returned one CVE, CVE-2021-43129, whose stated effect is a quiz right-click control bypass; NVD supplies no CVSS score, affected-version range, or named fixed release [17][4].
2. A documented Brightspace abuse pattern combines compromised institutional identities with permissive email behavior, showing that configuration and account security can matter more than the small public CVE count [8].
3. Online Manipal's learning surface is publicly attributable to D2L Brightspace [6], and the observed student-portal path initiates Microsoft Entra SAML [23].
4. Brightspace and OneRoster provide powerful grade-write and passback capabilities [15][29], but no public source reviewed proves that MUJ SLCM uses any specific one.

| Verdict component | Confidence | Reason |
|---|---|---|
| Description of CVE-2021-43129 | High | Direct NVD and catalog evidence |
| Completeness of the public CVE count | Medium-low | Catalog result is observable, but private and non-CVE issues may exist |
| Student portal uses a Microsoft SAML path | High | Direct passive redirect evidence |
| Brightspace supports Azure SAML and OIDC | High | First-party D2L documentation |
| MUJ Brightspace uses OIDC | Low | No direct public configuration evidence |
| MUJ SLCM receives automated grades from Brightspace | Low | Capability is documented; deployment is not |
| Online Manipal's overall vulnerability resistance | Low to moderate | Platform clues are public, but headers, configurations, patch state, and assurance reports are not |
| Recommended priority on identity and grade integrity | High | Supported by incident mechanism and documented write capabilities |

The responsible next step is a jointly authorized configuration and architecture review, followed by controlled non-production validation. Until that occurs, CVE applicability, SLCM grade-sync topology, Brightspace SSO mode, claim mapping, session revocation, and tenant-specific incident history should remain labeled **Unknown**, not secure and not vulnerable.

## References

1. *Brightspace API Reference — Developer Platform (January 2026)*. https://docs.valence.desire2learn.com/reference.html
2. *D2L Vulnerability Disclosure Policy - Brightspace*. https://community.d2l.com/brightspace/kb/articles/23533-d2l-vulnerability-disclosure-policy
3. *SAML Administration Overview - Brightspace*. https://community.d2l.com/brightspace/kb/articles/4843-saml-administration-overview
4. *NVD - CVE-2021-43129*. https://nvd.nist.gov/vuln/detail/CVE-2021-43129
5. *OneRoster® | 1EdTech*. https://www.1edtech.org/standards/oneroster
6. *Login - Manipal University Jaipur*. https://learning.onlinemanipal.com/d2l/home/14042
7. *LMS Security, Monitoring & Protection | D2L*. https://www.d2l.com/security/
8. *Brightspace Email Fraud: Alerts: publications: Services: REN-ISAC: Research Education Networking Information Sharing & Analysis Center*. https://www.ren-isac.net/services/publications/alerts/Brightspace_Email_Fraud.html
9. *ID token claims reference - Microsoft identity platform | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity-platform/id-token-claims-reference
10. *Security & Privacy Compliance | D2L*. https://www.d2l.com/security/compliance/
11. *Online Manipal | UGC Entitled Online UG & PG Degree Courses*. https://www.onlinemanipal.com/
12. *Conditional Access adaptive session lifetime policies - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-session-lifetime
13. *Security Policies and Protection | D2L*. https://www.d2l.com/security/protection
14. *OpenID Connect (OIDC) on the Microsoft identity platform - Microsoft identity platform | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols-oidc
15. *docs.valence.desire2learn.com*. https://docs.valence.desire2learn.com/res/grade.html
16. [[PDF] Brightspace Security Incident Final Report - DigitalCommons@UMaine](https://digitalcommons.library.umaine.edu/cgi/viewcontent.cgi?article=3851&context=univ_publications)
17. *Brightspace CVEs and Security Vulnerabilities - OpenCVE*. https://app.opencve.io/cve/?product=brightspace&vendor=d2l
18. *OneRoster Version 1.2 | IMS Global Learning Consortium*. https://www.imsglobal.org/spec/oneroster/v1p2
19. *Online Manipal | UGC Entitled Online UG & PG Degree Courses*. https://www.onlinemanipal.com/.well-known/security.txt
20. *Brightspace API Authentication Guide - OAuth 2.0 - Brightspace*. https://community.d2l.com/brightspace/kb/articles/1134-brightspace-api-authentication-guide-oauth-2-0
21. *Signing Key Rollover in Microsoft identity platform - Microsoft identity platform | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity-platform/signing-key-rollover
22. *D2L Service and Brightspace real-time status*. https://status.d2l.com/
23. *login.microsoftonline.com*. https://student.onlinemanipal.com/s/
24. *learning.onlinemanipal.com*. https://learning.onlinemanipal.com/robots.txt
25. *Configure a OneRoster integration - Brightspace*. https://community.d2l.com/brightspace/kb/articles/32187-configure-a-oneroster-integration
26. *onlinemanipal.com*. https://www.onlinemanipal.com/robots.txt
27. *Unsupported Browser*. https://learning.onlinemanipal.com/.well-known/security.txt
28. *Customize SAML token claims - Microsoft identity platform | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity-platform/saml-claims-customization
29. *Getting ready for OneRoster integration - Brightspace*. https://community.d2l.com/brightspace/kb/articles/23832-getting-ready-for-oneroster-integration
30. *OneRoster Rostering Service REST/JSON Binding*. https://www.imsglobal.org/spec/oneroster/v1p2/rostering/bind/rest
31. *OneRoster Gradebook REST/JSON Binding*. https://www.imsglobal.org/spec/oneroster/v1p2/gradebook/bind/rest
32. *Microsoft Entra federation metadata - Microsoft identity platform | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity-platform/federation-metadata
