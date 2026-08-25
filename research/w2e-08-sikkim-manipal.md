# SMU Student Systems OSINT: Exposure, Evidence, and MUJ Similarity

## Executive Summary

- **Three Distinct Current Surfaces**: SMU publicly exposes a regular-campus **SMUERP v5**, a separate **Vidya** student-learning login, and an admissions application portal. SMUERP offers student, employee, and email logins, while Vidya requests a student email and offers **SMU O365** sign-in [19][6]. -> Treat these as separate applications with separate owners, data flows, authentication policies, and incident playbooks rather than as one SLCM host.

- **Microsoft Identity Is The Strongest MUJ Similarity**: Vidya explicitly displays "Login with SMU O365" [6]. The supplied MUJ baseline also identifies Microsoft 365 identity, although the publicly extracted MUJ page independently verifies only a generic sign-in and a parent-login choice [1]. -> Coordinate conditional access, MFA, session revocation, and identity logging across both institutions, but do not infer a shared application codebase from a shared identity provider.

- **SMUERP Is Not Evidenced As A MUJ MVC Clone**: The regular-campus system identifies itself as **SMUERP v5**, describes a common real-time database and modular software design, and publishes `.aspx` student-login and payment routes [19][15]. -> The evidence is more consistent with a legacy ASP.NET Web Forms-style ERP than with the supplied MUJ ASP.NET MVC 5.3 baseline. This is an inference from public artifacts, not a server-side version confirmation.

- **Vidya Uses A Different Product Layer**: Vidya says it is powered by **KEN**, while KEN describes its product as a university operating platform spanning admissions, academics, assessments, finance, and engagement [6][16]. -> Assess Vidya as a vendor-backed platform and review vendor access, tenant configuration, SSO claims, APIs, and support boundaries independently from SMUERP and MUJ SLCM.

- **Examination Data Is Operationally Sensitive**: SMU's official examination manual assigns staff responsibility for system-based marks entry, password-protected scanned scripts, backups, online result publication, and student access through an online portal [11]. -> Give examination identities, marks workflows, document stores, and publication jobs a higher control tier than ordinary content pages.

- **Legacy SMU-DE Had A Distributed Portal Family**: Public historical pages link EduNxt for existing students, an Azure-hosted Online Examination Booking System, a separate results domain, a re-registration service, and an SMUDE app [7]. -> Inventory retired DNS names, cloud resources, certificates, redirects, and vendor accounts; historical endpoints can remain useful for phishing even after academic use ends.

- **No Confirmed Public SMU Cyber Incident Was Found**: This review found no credible public report tying SMU's identified portals to a confirmed breach, exploit, ransomware event, or defacement. CERT-In describes itself as India's national cyber-incident response agency, but its general role does not establish an SMU incident [22]. -> Record the conclusion as "no confirmed public incident located," not "no incident occurred."

- **The Public Complaint Evidence Is Operational, Not A Vulnerability Disclosure**: A 2020 Change.org petition with **236 supporters** alleged long examination delays for SMU-DE students and requested online exams or alternate relief, but did not allege a portal exploit or technical malfunction [20]. -> Do not relabel student-service dissatisfaction as a security incident; route availability and exam-continuity concerns into service-management and resilience reviews.

- **Overall Similarity Is Layer-Dependent**: SMU and MUJ are similar in purpose and Microsoft-centered identity, but public evidence points to different application families: MUJ MVC according to the supplied baseline, SMUERP v5 with `.aspx` routes, and KEN-powered Vidya. -> Reuse governance and identity controls, not vulnerability assumptions or exploit hypotheses.

## 1. Scope, Safety Boundary, and Evidence Method

This is a passive, public-information OSINT report with a research cutoff of **2026-08-25**. It uses public university pages, publicly accessible login pages, official manuals, vendor pages, indexed historical material, a student petition, and national incident-response information. It does not include credential use, login attempts, account enumeration, parameter manipulation, port scanning, vulnerability scanning, or attempts to access non-public records.

I cannot provide private chain-of-thought. In its place, the report supplies an auditable evidence-to-conclusion record: every important conclusion identifies its observation, source quality, inference boundary, and confidence. That is more useful to a security club because another analyst can reproduce the source review without receiving instructions that could facilitate unauthorized access.

### Evidence hierarchy

| Evidence class | Examples in this report | Permitted conclusion | Key limitation |
|---|---|---|---|
| First-party live page | Vidya, SMUERP, SMU students page, MUJ portal | Current public branding, visible fields, published links | Does not prove back-end versions or internal topology |
| First-party official document | SMU examination manual | Documented roles, workflows, handling requirements | May describe policy rather than actual implementation |
| First-party historical page | SMU-DE existing-student page | Historical portal names and URLs | Does not establish that a service remains active |
| Vendor page | KEN website | Vendor's stated product scope | Marketing claims are not an independent security assessment |
| User-generated document or petition | Scribd FAQ/manual, Change.org petition | What the artifact or complainant says | Provenance, completeness, and independent verification are limited |
| Search-negative finding | Incident, vulnerability, and complaint searches | No matching credible report was located in the bounded review | Cannot prove that an event never happened |

The label **Inference** is used wherever public artifacts support a reasoned conclusion without directly stating it. Runtime versions, origin servers, CDN topology, patch status, open ports, and vulnerability status cannot be established merely from a login page. The supplied MUJ facts - ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 - are treated as the comparison baseline requested by the user, not as facts fully revalidated in this SMU-focused review.

**Decision-ready insight:** The safe output of OSINT is an asset and hypothesis map. It is not authorization to test any mapped host.

## 2. Exact Public System Map: Current, Adjacent, and Historical

The strongest result is that "the SMU portal" is not one application. The official students page links an ERP, more than one item labeled Student Login, fee-payment services, and grievance services [9]. The current learning login and admissions site are separate again.

| Status | System and exact public URL | Publicly evidenced purpose and behavior | Attribution confidence |
|---|---|---|---|
| Current | `https://erp.smu.edu.in/` | Identifies itself as **SMUERP v5** and Sikkim Manipal University ERP; offers student, employee, and email login choices [19] | High |
| Current | `https://erp.smu.edu.in/common/loginstd.aspx` | Student path using registration number with password-recovery link [19] | High |
| Current | `http://erp.smu.edu.in/GenPay/QuickPay.aspx` | SMU Quick Pay collects user type, phone, email, amount, description, and remarks [15] | High |
| Current | `https://vidya.smu.edu.in/` | "Student Login," student email, Remember Me, Forgot Password, SMU O365 login, powered by KEN [6] | High |
| Current, admissions | `https://apply.smu.edu.in/` | Public page advertises an admissions session; it should not be confused with the continuing-student ERP [10] | High |
| Current marketing umbrella | `https://smu.onlinemanipal.com/` | Markets SMU online degree programs; the page lists BBA, MBA, MCA, BA, MA, and M.Com/B.Com offerings [4] | High for marketing role; low for LMS internals |
| Current but ambiguously linked | `https://ecm.org.in/` | One item labeled Student Login on the official students page points to this external domain [9] | Low for ownership and purpose; no inference made |
| Historical | `https://edunxt.smude.edu.in/?q=MULNLogin/edunxtlogin` | Existing-student EduNxt link on the SMU-DE page [7] | High for historical publication |
| Historical | `http://smu-oebs-lb.centralindia.cloudapp.azure.com/SMUOEBS/Default.aspx` | SMU-DE Examination Booking System [7] | High for historical publication; current status not claimed |
| Historical | `http://results.smude.edu.in/` | SMU-DE results link [7] | High for historical publication; current status not claimed |
| Historical | `http://myzone.smude.edu.in/` | FAQ describes re-registration or re-sit workflow [18] | Medium because evidence is a republished FAQ |
| Unresolved shared LMS route | `https://learning.onlinemanipal.com/d2l/home/12169` | Public response exposes a D2L-style `/d2l/` route and an unsupported-browser page, but no extracted SMU branding [13] | Low for SMU attribution; excluded from the confirmed SMU map |

Two cautions follow. First, the official students page publishes both HTTPS and HTTP destinations, including an HTTP Quick Pay URL and HTTP student-login link [9]. This records what the page links; it does not establish whether transport is downgraded, redirected, or insecure in practice. An authorized owner should canonicalize HTTPS and validate HSTS and redirect behavior internally.

Second, the external `ecm.org.in` destination is anomalous only in the literal sense that it leaves the `smu.edu.in` namespace. There is not enough evidence to call it malicious, misconfigured, or obsolete. The appropriate action is administrative ownership verification, not probing.

**Decision-ready insight:** Build the asset register around business ownership and data handled, not around the word "SLCM." The same university publishes ERP, learning, admissions, payment, grievance, examination, and legacy distance-learning surfaces.

## 3. SMUERP v5: Regular-Campus ERP and SLCM-Family Evidence

SMUERP is the clearest regular-campus student-information system. Its public page calls it "SMUERP - Sikkim Manipal University Enterprise Resource Planning" [19]. It describes version 5 as a modular system using a common database so departments can store and retrieve information in real time [19]. The page also says the ERP handles patient-care registration and scanned hospital documents, as well as inventory functions [19]. This means the exposed brand is broader than a student-only portal.

| Observable dimension | Direct public evidence | Security relevance |
|---|---|---|
| User populations | Student, employee, and email login choices [19] | Multiple identity populations increase role-separation and lifecycle complexity |
| Student identifier | Registration number appears as the student-login field [19] | Student identifiers should never substitute for authorization checks |
| Recovery | A student password-recovery route is publicly linked [19] | Recovery responses should resist account enumeration and abuse |
| Architecture description | Common database and modular software design [19] | A shared data layer can increase blast radius if module authorization is inconsistent |
| Payment | Quick Pay accepts user type, phone, email, amount, and narrative fields [15] | Payment reconciliation, input validation, fraud monitoring, and privacy controls are material |
| Support visibility | Software, hardware, and hospital support extensions are displayed [15] | Useful for legitimate support, but also for social-engineering pretexting |
| Application-family clue | Student and payment paths end in `.aspx` [15] | **Inference:** consistent with ASP.NET Web Forms-style implementation, not proof of exact runtime/version |

A historical, user-uploaded manual is labeled as a guide to the Sikkim Manipal University "Student Life Cycle Management system portal," but the visible evidence does not expose enough of that manual to prove source-code lineage [12]. Therefore, it is fair to describe SMUERP as part of SMU's student-lifecycle ecosystem, but not to claim that it is the same product or codebase as MUJ SLCM.

Microsoft describes Web Forms as one of the ASP.NET application programming models, and ASP.NET ViewState as a mechanism for preserving page state. Those references make `.aspx` and stateful page artifacts useful architectural indicators, but they still do not identify an exact .NET or IIS version. The precise versions requested for MUJ should not be copied onto SMUERP without first-party documentation or an authorized configuration review.

**Inference:** SMUERP's visible naming, modular ERP description, `.aspx` routes, and registration-number login make it a business-function peer of MUJ SLCM, not an evidenced deployment clone. Confidence is **high** on the business-function relationship and **medium** on the Web Forms-style implementation inference.

## 4. Vidya, KEN, and SMU O365: A Separate Learning Surface

Vidya's public page is unusually clear. It says "Your Learning, Simplified," labels the form "Student Login," requests "Student Email," offers Remember Me and Forgot Password, provides "Login with SMU O365," and credits KEN [6]. That establishes purpose, identity input, federation choice, and vendor branding without logging in.

KEN describes its platform as an AI-native university operating system unifying admissions, academics, administration, and engagement [16]. Its published workflow claims span application processing and enrollment, learning management and assessments, student-success tracking, billing and reconciliation, finance and procurement, HR, inventory, and analytics [16]. These are vendor claims, not proof that SMU licenses every module.

### Vidya evidence-to-risk table

| Observation | Direct fact or inference | Defensive implication |
|---|---|---|
| Student-email field [6] | Direct fact | Protect against email-based account discovery and phishing |
| Remember Me [6] | Direct fact | Review persistent-token duration, revocation, and shared-device warnings |
| Forgot Password [6] | Direct fact | Use uniform recovery responses, rate limits, and event logging |
| SMU O365 [6] | Direct fact | Enforce MFA and conditional access at the identity provider; correlate IdP and application logs |
| Powered by KEN [6] | Direct fact | Maintain vendor ownership, data-processing, support-access, breach-notification, and exit provisions |
| Full KEN module set at SMU | Not established | Do not assume vendor marketing equals enabled tenant functionality |
| Same code as MUJ SLCM | Contradicted by visible product branding, but not forensically disproved | Test and patch each application independently under authorization |

The identity similarity to the supplied MUJ baseline is significant. Both environments appear to rely on Microsoft-centered institutional identity. Yet identity federation is a shared control plane, not evidence of a shared web stack. A modern vendor portal and a legacy MVC application can both redirect to Microsoft 365 while retaining entirely different session handling, authorization logic, APIs, databases, and release cycles.

The most useful club exercise is therefore a non-invasive trust-boundary diagram. It should identify the browser, SMU O365 tenant, Vidya/KEN tenant, student records, support administration, and any approved downstream LMS or assessment systems. The exercise should use documentation and owner interviews, not live experimentation.

**Decision-ready insight:** Vidya is closer to MUJ at the identity layer than at the application layer. Centralize identity assurance while preserving separate application risk registers.

## 5. Examinations, Results, and Legacy SMU-DE Workflows

SMU's official examination manual shows why student-system security cannot be reduced to login-page technology. The manual assigns a Programmer responsibility for entering evaluator marks, preparing draft and final results, publishing results online, transmitting scanned answer books, and backing up data to a virtual server and external drive [11]. It also says scanned answer books sent for external evaluation are watermarked and password protected [11].

The publication chain is equally specific. Marks entered in the system are to be verified by examination leadership [11]. Result sheets go to IT for website publication, and results become available to students on the online portal [11]. Hall tickets and admit cards bind identity, registration number, photograph, and signature to examination access [11].

| Workflow | Publicly documented handling | Primary defensive objective |
|---|---|---|
| Candidate identity | Admit card with photograph, registration number, and signature [11] | Prevent impersonation while minimizing exposed identity data |
| Hall-ticket preparation | Assigned to Programmer and Junior Assistant roles [11] | Segregation of duties and issuance audit trail |
| Marks entry | System entry followed by verification [11] | Dual control, immutable logs, anomaly detection |
| Scanned scripts | Watermark and password protection for external evaluation [11] | Controlled sharing, key handling, expiry, recipient authentication |
| Results | IT publication and student online-portal access [11] | Release authorization, cache control, privacy, rollback plan |
| Backup | Virtual-server and external-drive backups [11] | Encryption, offline copies, restoration testing, custody logging |

Legacy SMU-DE used a more distributed model. SMU-DE was established in **2001** for professional distance programs in management and IT [8]. Historical public pages connected EduNxt, an examination-booking system on Microsoft Azure, a results domain, an app, and re-registration [7]. The EduNxt FAQ describes a virtual classroom, recorded WebEx sessions, downloadable study resources, mobile applications, and an incident-based helpdesk [18].

The same FAQ documents a historical first-login credential convention derived from the student's university identity and then instructs students to change the password [18]. This is historical evidence, not a claim about any current endpoint. It is still a useful lesson: predictable bootstrap credentials and delayed password changes create avoidable account-takeover risk. The defensive replacement is a time-limited activation link, verified recovery channel, forced enrollment in MFA, and invalidation after first use.

**Decision-ready insight:** Examination security depends on end-to-end workflow integrity. Protect marks, scripts, hall tickets, publication jobs, and backups, not only the portal front door.

## 6. How Closely SMU Resembles MUJ SLCM

The comparison must distinguish application runtime, identity, business purpose, infrastructure, and evidence quality. Similarity in one dimension does not transfer to another.

| Dimension | MUJ baseline | SMUERP v5 | SMU Vidya | Assessment |
|---|---|---|---|---|
| Business purpose | Student lifecycle and parent/student access | Student plus enterprise, payment, inventory, and hospital ERP [19] | Learning-focused student login backed by a broader campus vendor [6][16] | Moderate functional overlap |
| Public route style | `/Home/Index` in the public MUJ URL | `.aspx` login and payment routes [15] | Product-branded learning login | Low route/application similarity |
| Application family | ASP.NET MVC 5.3 and .NET Framework 4.x, supplied baseline | **Inference:** ASP.NET Web Forms-style ERP; exact versions unknown | KEN-powered; exact tenant stack not established | Low evidenced codebase similarity |
| Identity | Microsoft 365, supplied baseline | Registration-number login plus employee/email choices [19] | Explicit SMU O365 option [6] | Moderate to high identity-layer similarity for Vidya |
| Edge and server | IIS 10 behind Akamai, supplied baseline | Not publicly established in reliable first-party evidence | Not publicly established in reliable first-party evidence | Unknown; do not transfer MUJ assumptions |
| User segmentation | Public MUJ page shows sign-in and parent-login choices [1] | Student, employee, email, and Quick Pay populations [19][15] | Student email and O365 [6] | Similar multi-population concern, different implementation |
| Vendor/product evidence | No vendor identified on extracted MUJ landing text [1] | SMU-IS and SMUERP branding [15][19] | KEN attribution [6] | Different named ownership layers |
| Shared vulnerability assumptions | None justified | None justified | None justified | Do not generalize findings across hosts |

### Evidence-to-conclusion rationale

1. **Observation:** MUJ and Vidya both expose institutional sign-in concepts, and Vidya explicitly names O365 [6]. **Conclusion:** identity-control patterns may be reusable. **Confidence:** high for Vidya, medium for the cross-institution comparison because the detailed MUJ identity fact comes from the supplied baseline.

2. **Observation:** SMUERP calls itself an ERP, describes a modular common database, and uses `.aspx` routes [19][15]. **Conclusion:** it resembles MUJ in student-lifecycle purpose but not clearly in application architecture. **Confidence:** high on purpose, medium on framework family.

3. **Observation:** Vidya credits KEN, whose stated scope includes academic and administrative workflows [6][16]. **Conclusion:** Vidya should be managed as a vendor platform, not assumed to be a MUJ SLCM instance. **Confidence:** high on branding, medium on the exact enabled module set.

4. **Observation:** no first-party SMU source states ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, or Akamai for the identified SMU systems. **Conclusion:** those MUJ properties must remain MUJ-specific. **Confidence:** high as an evidence-gap finding.

**Decision-ready insight:** Overall resemblance is **moderate at the business layer, moderate at the identity layer, and low at the evidenced application-stack layer**.

## 7. Public Incidents, Vulnerability Claims, Portal Complaints, and Ports

The incident search covered combinations of SMU and Sikkim Manipal with breach, cyberattack, ransomware, vulnerability, exploit, defacement, CERT-In, OpenBugBounty, Zone-H, and public exposure indexes. No credible result was found that tied the identified SMU systems to a confirmed compromise. CERT-In's general mandate includes cyber-incident information, alerts, emergency measures, and coordination, but that mandate is not evidence about SMU [22].

| Category | Result | Evidentiary meaning |
|---|---|---|
| Confirmed SMU breach or ransomware event | None located | Absence of public evidence only |
| Public vulnerability disclosure for Vidya or SMUERP | None located | Does not establish that the systems are vulnerability-free |
| Public defacement record | None credibly tied to the scoped systems | Does not establish complete historical absence |
| Technical portal-failure complaint | No well-supported first-person report located | Search engines may not index closed support tickets or social posts |
| Official support demand | Historical EduNxt FAQ provides an incident-helpdesk process and email/phone channels [18] | Confirms support need, not a failure rate |
| Student-service complaint | 2020 examination-delay petition with 236 supporters [20] | Operational grievance; not a technical or security incident |
| Network-port exposure | Not assessed actively; no reliable passive inventory established | No port claim should be made |

The Change.org petition needs careful wording. It alleged that SMU-DE examinations had not been held after March 2019, said students received late information, and requested home-based online exams or alternate academic and fee relief during the COVID-19 disruption [20]. The page says it was created on **7 June 2020** and had **236 supporters** [20]. It does not independently verify the allegations and does not claim hacking, data exposure, or portal malfunction.

If the user's phrase "port complaints" literally means complaints about exposed network ports, this review deliberately did not scan. No verified passive port inventory was found, so the correct entry is **Not established**. If the intended phrase was "portal complaints," the petition and historical support material are the only relevant public artifacts found, and neither proves a security defect.

**Decision-ready insight:** Keep four registers separate: confirmed incidents, responsible disclosures, availability/support tickets, and student grievances. Combining them produces misleading risk reporting.

## 8. Defensive Priorities for an Authorized University Team

These recommendations are defensive and require system-owner authorization. They do not require students or club members to test production systems.

| Priority | Authorized defensive action | Why it follows from the evidence |
|---|---|---|
| 1 | Establish named owners for SMUERP, Vidya/KEN, admissions, Online Manipal, payment, exams, grievance services, and every legacy SMU-DE domain | The public ecosystem spans multiple applications, vendors, and generations |
| 2 | Enforce MFA and conditional access for SMU O365; correlate O365, Vidya, ERP, and helpdesk events | Vidya explicitly offers O365 login [6] |
| 3 | Make login and recovery responses uniform; rate-limit and alert on recovery abuse | OWASP explains that different responses for valid and invalid users enable account enumeration [23] |
| 4 | Review registration-number and object-level authorization server-side | OWASP defines IDOR as user-controlled object access without sufficient authorization checks [24] |
| 5 | Centralize session lifecycle logging, revoke persistent sessions, and reject session IDs supplied through unintended mechanisms | OWASP recommends logging the full session lifecycle and avoiding alternate session-ID mechanisms [25] |
| 6 | Protect result publication with dual authorization, immutable logs, signed release manifests, rollback, and cache purging | The official manual documents marks entry, verification, and online publication [11] |
| 7 | Encrypt examination backups and test restoration; maintain offline or logically isolated copies | The manual identifies virtual-server and external-drive backups [11] |
| 8 | Canonicalize HTTPS for every published ERP and payment link; validate HSTS and remove stale HTTP references | The official students page publishes HTTP student and Quick Pay destinations [9] |
| 9 | Remove unnecessary technology-disclosure headers and keep frameworks and TLS libraries patched | OWASP recommends removing `X-Powered-By` and maintaining current TLS-library patches [26][27] |
| 10 | Retire or explicitly archive legacy DNS, Azure resources, certificates, email channels, and branding | Historical SMU-DE pages expose several recognizable service names [7] |
| 11 | Verify third-party links such as `ecm.org.in`, document contractual ownership, and monitor for domain or certificate changes | The external destination is linked as Student Login on an official page [9] |
| 12 | Publish a vulnerability-disclosure policy with scope, safe harbor, prohibited actions, reporting channel, and response targets | No SMU-specific public VDP was located in this review |

For disclosure, the university should designate a security contact rather than direct researchers to guess. MUJ's public registrar page identifies the registrar as a recipient of complaints and suggestions and publishes `registrar@jaipur.manipal.edu` [28]. That is an administrative contact, not proof of a formal vulnerability-disclosure program. The better long-term solution is a dedicated security address and policy.

Students must not try credentials, alter identifiers, enumerate accounts, inspect another person's records, or test payment and examination workflows without written authorization. India's Information Technology Act addresses unauthorized access to computer resources, and separately criminalizes fraudulent or dishonest use of another person's password or unique identification feature [29].

**Decision-ready insight:** The club's highest-value contribution is governance: asset inventory, evidence preservation, threat modeling, tabletop exercises, and a disclosure-policy proposal.

## 9. Synthesis: Shared Identity, Different Application Generations

The ecosystem resolves into three architectural generations rather than one SLCM clone.

First, **SMUERP v5** is the regular-campus operational core. Its scope spans student access, payments, enterprise functions, inventory, and hospital workflows [19]. Its route style and public ERP description differ from the supplied MUJ MVC baseline. Its principal trade-off is integration: a common database and modular system can streamline operations, but authorization mistakes or privileged-account compromise may affect several modules.

Second, **Vidya/KEN** is a vendor-backed learning and engagement layer with O365 federation [6]. Its advantage is a clearer modern identity handoff and a vendor product model. Its trade-off is shared responsibility: SMU controls identity policy and tenant governance, while the vendor may control application code, hosting, support tooling, and parts of incident response.

Third, **legacy SMU-DE** was a distributed collection of EduNxt, myzone, examination booking, results, apps, and support processes [7][18]. Its advantage was specialized distance-learning functionality. Its long-term risk is residue: old domains, recognizable brands, obsolete instructions, cloud resources, and support identities can outlive the service and strengthen phishing narratives.

| Comparison dimension | MUJ SLCM | SMUERP v5 | Vidya/KEN | Legacy SMU-DE |
|---|---|---|---|---|
| Primary mechanism | MVC student portal, per supplied baseline | Integrated modular ERP [19] | Vendor learning/campus platform [6][16] | Federated specialist portals [7] |
| Scope | Student and parent access [1] | Students, staff, payments, inventory, health operations [19] | Learning plus potentially broad vendor modules [16] | Distance learning, exams, results, re-registration |
| Identity | Microsoft 365, supplied baseline | Registration number plus employee/email paths [19] | SMU O365 [6] | Historical portal credentials and helpdesk [18] |
| Time horizon | Current comparison target | Current | Current | Historical/transitioning |
| Main trade-off | Legacy framework maintenance versus institutional integration | Broad blast radius versus integrated operations | Vendor dependency versus platform modernization | Specialized services versus residual attack surface |
| Evidence strength | Mixed: user-supplied stack plus public landing page | Strong first-party public evidence | Strong branding, limited tenant internals | Strong historical linkage, weak current-status evidence |

The non-obvious tension is that the **closest apparent similarity is also the least useful for predicting application vulnerabilities**. Microsoft identity can unify phishing defenses, MFA, and session response across MUJ and Vidya, but it says little about authorization logic inside an MVC portal, a Web Forms-style ERP, or a KEN tenant. Conversely, SMUERP may be the closest functional peer to MUJ SLCM while being the least similar visible application architecture.

A second tension is modernization versus fragmentation. Vidya may reduce some legacy burden, but it adds a vendor trust boundary while SMUERP, admissions, payments, and historical systems remain visible. Migration does not automatically reduce attack surface unless old systems, domains, accounts, documentation, and integrations are retired.

The holistic recommendation is therefore: **centralize identity, logging, disclosure, and incident governance; decentralize application assumptions.** Each portal needs its own owner, data classification, architecture record, authorized assessment scope, recovery plan, and retirement criteria.

## VERDICT

**Verdict:** SMU operates an identifiable student-system ecosystem, but public evidence does **not** support calling its current systems replicas of MUJ SLCM.

- **SMUERP v5** is the strongest regular-campus SLCM analogue by business purpose. Its public `.aspx` routes and ERP description suggest a different ASP.NET application style from the supplied MUJ MVC 5.3 baseline [19][15].
- **Vidya** is a distinct KEN-powered learning portal with explicit SMU O365 sign-in [6]. It resembles MUJ most strongly at the institutional identity layer, not at the evidenced application layer.
- **Online Manipal** is confirmed as SMU's current online-program marketing umbrella, but its public page does not identify an SMU-specific LMS login or technical stack [4]. The D2L route reviewed is therefore left unattributed rather than guessed [13].
- **Legacy SMU-DE** demonstrably used EduNxt, Azure-hosted exam booking, a results domain, myzone, apps, and helpdesk processes [7][18]. These are relevant to historical exposure and decommissioning, not proof of current operation.
- **Security incidents:** no confirmed public SMU-specific compromise was located. Confidence in this negative finding is necessarily limited because private incidents and support cases may never be published.
- **Portal complaints:** one material public petition concerns examination delay and continuity, not exploitation or portal malfunction [20].
- **Ports:** not tested and not established.

**Overall confidence: Moderate-High.**

Confidence is **high** for the identities, links, visible fields, and workflows stated on first-party pages; **medium** for the inference that SMUERP is Web Forms-style and architecturally unlike MUJ MVC; **low** for unverified current status of historical SMU-DE endpoints; and **low-to-moderate** for the absence-of-public-incident conclusion.

The actionable conclusion for the security club is not "test SMU because it looks like MUJ." It is: document the separate trust boundaries, propose centralized identity and disclosure controls, and seek written authorization before any technical validation.

## References

1. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
2. *Sikkim Manipal Institute of Technology*. https://www.smu.edu.in/smit
3. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
4. *Online Degree Programs in India | Sikkim Manipal University | Online Manipal*. https://smu.onlinemanipal.com/
5. *Sikkim Manipal University*. https://www.smu.edu.in/
6. *Login*. https://vidya.smu.edu.in/
7. *Distance Education MBA, MCA, BBA, BCA, M.Sc. (IT), B.Sc. (IT) Programs | SMUDE*. https://smude.edu.in/smude.html/1000
8. *Sikkim Manipal University-Distance Education*. https://www.manipal.edu/mu/important-links/world-wide-manipal/sikkim-manipal-university-distance-education.html
9. *About Sikkim Manipal University*. https://www.smu.edu.in/students.php
10. *Login*. https://apply.smu.edu.in/
11. *Examination Manual Of Smu Tadong Campus*. https://www.smu.edu.in/img/content/dam/manipal/smu/IQAC/Examination-Manual-of-SMU-Tadong-Campus.pdf
12. *Sikkim Manipal University Student Portal Guide*. https://www.scribd.com/doc/104502831/SMUDE-Student-Portal-Manual
13. *Unsupported Browser*. https://learning.onlinemanipal.com/d2l/home/12169
14. *About Ken42 | Unified Education & Campus Management Platform*. https://ken42.com/about-us
15. [
	

](http://erp.smu.edu.in/GenPay/QuickPay.aspx)
16. *Ken42 | Unified Campus Management & Student Success Platform*. https://ken42.com/
17. *Student Helpdesk*. https://smude.edu.in/smude/studentservices/student-helpdesk.html/1000
18. *EduNxt FAQs: Access, Support & Features | PDF | Password | Mobile App*. https://www.scribd.com/document/336548041/SMUDE-FAQs
19. [
	
    SMUERP v5||HOME

](https://erp.smu.edu.in/)
20. *Petition · Online Exam should be Conduct/Cancelled for SMU DE as already declared for Reg. SMU stud. - India · Change.org*. https://www.change.org/p/dr-ramesh-pokhriyal-nishank-online-exams-should-also-be-conducted-cancelled-for-smu-de-as-already-declared-for-regular-smu-students
21. *Cert-In - Home Page*. https://www.cert-in.org.in/SecurityIncident.jsp
22. *cert-in.org.in*. https://www.cert-in.org.in/s2cMainServlet?pageid=PUBWEL01
23. *http://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/03-Identity_Management_Testing/04-Testing_for_Account_Enumeration_and_Guessable_User_Account*. http://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/03-Identity_Management_Testing/04-Testing_for_Account_Enumeration_and_Guessable_User_Account
24. *http://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References*. http://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References
25. *http://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html*. http://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
26. *http://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html*. http://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html
27. *http://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html*. http://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html
28. *http://jaipur.manipal.edu/administration-registrar.php*. http://jaipur.manipal.edu/administration-registrar.php
29. *http://indiacode.nic.in/bitstream/123456789/13116/1/it_act_2000_updated.pdf*. http://indiacode.nic.in/bitstream/123456789/13116/1/it_act_2000_updated.pdf
