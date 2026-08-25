# Indian University Portal Incidents: Lessons for MUJ SLCM

## Executive Summary

- **Marks Integrity Is The Clearest Recurring Failure**: Three named university cases involved digital marks manipulation: more than 60 students at Bengaluru North University, 55 at Bangalore University, and at least 10 identified instances involving no fewer than 50 students at Gauhati University [5][11][22]. Inference: MUJ should treat marks changes as high-risk financial transactions, requiring two-person approval, step-up authentication, immutable before-and-after records, and rapid exception review.
- **Privileged Access Dominates The Core Sample**: The two Karnataka incidents involved a registrar's credentials, while Gauhati University's case reportedly occurred at an outsourced data-entry operator and Sri Venkateswara University's fee case allegedly involved people working inside the administrative process [5][11][22][20]. Inference: the strongest common pattern is weak control over trusted identities and workflows, not a publicly established prevalence of novel software exploits.
- **IDOR Is Serious But Not Proven To Dominate Universities**: IIT Roorkee data could reportedly be retrieved by entering an enrollment number, which is IDOR-like behavior, but the reporting does not name the flaw as IDOR [16]. The adjacent PhysicsWallah disclosure explicitly alleges IDOR, absent authorization, and exposure of millions of records, but it is a researcher's account about an education company rather than an independently documented university breach [1].
- **Data Exposure Can Persist Quietly**: IIT Roorkee's exposed site was believed to have operated for about 10 years and included contact, caste, financial-background, academic-year, and photographic data for more than 30,000 students and alumni [16]. Inference: periodic external exposure inventories and data-minimization reviews are as important as perimeter blocking.
- **Payment Risk Extends Beyond The Real Portal**: Sri Venkateswara University found manipulated receipts with fake seals and signatures, while a Sai Nath Educational look-alike domain allegedly diverted INR 32,000 from an applicant [20][21]. MUJ therefore needs controls for both authenticated payment processing and impersonation of its public brand.
- **Ransomware Evidence Is Stronger In Adjacent Academic Health Care**: The reviewed Indian Express report on AIIMS Delhi establishes a week-long cyber disruption, five infected servers, and approximately 3-4 crore patient records hosted on those servers, while also reporting that claims of theft had no factual basis [19]. I found no comparably detailed, well-sourced university-portal ransomware case in the reviewed corpus; that is a limitation of this survey, not proof that none occurred.
- **Disclosure Usually Becomes A Police Or Committee Matter**: Five of seven core cases reached a police complaint, case, or arrest; four produced an internal or government inquiry. Only the Bangalore University report clearly described restoration of original marks, while the core reports did not contain a full technical postmortem. Inference: Indian university disclosure is typically enforcement-led and remediation-light in public.
- **M365 Controls Must Protect Administrative Identities**: Microsoft security defaults require MFA registration, administrator MFA, and blocking of legacy authentication; Microsoft advises more complex organizations to use Conditional Access [14]. MUJ should apply stronger, role-sensitive policies to registrars, examination staff, finance staff, and emergency accounts rather than relying on ordinary student-login policy.
- **Akamai Cannot Replace Application Authorization**: OWASP states that every endpoint receiving an object ID must verify that the logged-in user may perform the requested action on that object [13]. Inference: an edge WAF can reduce malicious traffic, but only the SLCM application can reliably decide whether a student, parent, faculty member, or registrar owns or may modify a record.
- **Incident Readiness Has A Six-Hour Clock**: CERT-In's directions require covered organizations to report listed cyber incidents within six hours, keep ICT logs in India for a rolling 180 days, and synchronize time with specified or traceable NTP sources [18]. MUJ should make evidence preservation and reporting decisions part of a rehearsed playbook, not an improvised response.

## 1. Scope, Ethics, And Auditable Reasoning

This report uses only public reporting, official guidance, and the MUJ login page. The portal publicly presents student, parent, and `@muj.manipal.edu` sign-in paths [26]. The detailed architecture in the question - ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 identity - is treated as a user-supplied working assumption. It was not independently probed or verified. No active scanning, credential testing, object enumeration, or interaction with private records was performed or is recommended.

I cannot provide private hidden chain-of-thought. Instead, the report supplies an auditable evidence-to-conclusion trail: named source, observed event, confidence classification, inference, and defensive implication. This is more useful to a security club because another analyst can challenge each link without receiving operational instructions that could enable unauthorized access.

The evidence set is deliberately divided into three groups. A **core case** is a named Indian university or institute incident involving student data, marks, or fees. An **adjacent comparator** concerns a closely related education or academic-health environment and is not counted as a university-portal case. A **counterexample** is a public allegation that the institution denied. This avoids inflating prevalence by treating every headline as a confirmed breach. For example, SPPU officials publicly said that a rumored compromise had not altered the official website and that it was functioning normally [12].

The sample is purposive, not statistically representative. News coverage favors visible arrests, large numbers, and dramatic outcomes; universities may resolve lesser incidents without publication. Counts below therefore describe the reviewed cases only. They must not be generalized into a national breach rate.

### Evidence classification

| Label | Meaning in this report | Publication standard |
|---|---|---|
| Confirmed public event | An institution, police source, court-related action, or multiple concrete facts establish that an incident occurred | State what the source establishes and preserve its qualifiers |
| Reported or alleged mechanism | A journalist, police source, institution, or researcher attributes a method, but no full technical postmortem is public | Use "reported," "alleged," or "the source says" |
| Analyst inference | A control class appears consistent with the reported behavior, but the source does not name it | Label explicitly as "Inference" |
| Adjacent comparator | Relevant to defensive planning but not an Indian university student-portal case | Exclude from core prevalence counts |
| Counterexample | A compromise claim was publicly denied or remained unverified | Do not count as an incident |

The key methodological decision is to count only what the evidence supports. A public record retrievable by enrollment number may be BOLA-like, but without technical evidence it is not labeled a confirmed IDOR. A stolen registrar password is a credential-control failure, but it does not establish whether phishing, password reuse, malware, insider disclosure, or another cause obtained that password.

## 2. Exact Incident Matrix: Nine Cases And One Counterexample

| Case and public date | Category | Publicly reported facts | Vulnerability or fraud class | Public outcome | Confidence and scope |
|---|---|---|---|---|---|
| Gujarat Technological University, July 2020 | Student-data leak | Personal data of about 1,200 BE students reportedly leaked, including photographs, PAN, Aadhaar, and voter-ID details [10] | Technical cause undisclosed; reporting described a hacked system | Police reporting linked publication of the data to an affiliated-college student while seeking another alleged hacker [2] | High confidence that exposure occurred; low confidence on technical root cause |
| IIT Roorkee, reported August 2025 | Long-lived public exposure | More than 30,000 student and alumni records were reportedly accessible; entering an enrollment number displayed personal details and photographs [16] | **Inference:** BOLA/IDOR-like object access, but not source-confirmed IDOR | Institute ordered an inquiry after being alerted; operator and purpose were unknown [16] | High on public exposure; medium on mechanism |
| Bengaluru North University UUCMS, October 2024 | Marks tampering | Registrar credentials were reportedly misused to alter marks of more than 60 failed students; alleged payments were INR 15,000-20,000 per student [5] | Compromised privileged credentials and fraudulent workflow | Three arrests, frozen accounts, high-level probe, security-tightening announcement, and action to identify beneficiaries [5] | High on incident and enforcement; acquisition path for credentials unknown |
| Bangalore University UUCMS, June 2025 report | Marks tampering | Marks of 55 students were altered with the registrar-evaluation login; five students passed because of changes [11] | Privileged credential compromise plus reported OTP bypass | Internal committee, planned police complaint, and restoration of original marks [11] | High on effect; medium on how OTP was bypassed |
| Gauhati University, June 2024 | Cash-for-marks | Police reported digital marksheet tampering; at least 10 inflation instances and no fewer than 50 students who apparently paid [22] | Outsourced privileged/data-entry process abuse | Nine arrests, internal investigation, and widened police inquiry [22] | High on case; attribution to contractor end comes from CID sources |
| Sri Venkateswara University, May 2026 report | Fee-payment fraud | Manipulated fee receipts allegedly used fake seals and forged employee signatures; reported misappropriation was INR 65,686 [20] | Insider-enabled receipt and reconciliation fraud | Registrar complaint and campus-police case under cited BNS provisions [20] | High that a case was registered; allegations not a final adjudication |
| Sai Nath Educational, reported August 2026 | Look-alike portal/payment fraud | A near-identical unofficial domain allegedly diverted INR 32,000 from a prospective student [21] | Domain impersonation, phishing, and payment diversion | Police traced creation to a Bihar designer, examined the recipient account, and continued investigating; one complaint was registered [21] | Medium because the principal source is a specialist news site and the case remained open |
| PhysicsWallah, June 2025, adjacent | Exposed education API/web object | CyberX9 alleged that IDOR, no authorization, and no rate limiting exposed millions of student and parent records [1] | Explicitly alleged IDOR/BOLA and exposed object access | Researcher reported disclosure on April 22, fix confirmation on May 1, and escalation to CERT-In/NCIIPC on May 31 [1] | Medium; detailed first-party researcher account, not an independent university case |
| AIIMS Delhi, November 2022, adjacent | Ransomware/cyber disruption | Online services were disrupted for a week; five of 140 physical and virtual servers were infected and hosted data for about 3-4 crore patients [19] | Ransomware/cyberattack comparator; entry vector not established in cited report | Source rejected claims of stolen patient data as having no factual basis [19] | High on disruption and infected servers; low on vector and exfiltration |
| Savitribai Phule Pune University, 2025, counterexample | Rumored website breach | Officials said the official site's content was unaltered and the site was functioning normally [12] | Not established | Public denial | Excluded from incident counts |

The table shows why precise language matters. Only the adjacent PhysicsWallah account explicitly names IDOR. The IIT Roorkee behavior resembles broken object-level authorization, but the article leaves open whether the exposed website was official, copied data from elsewhere, or used another design. Conversely, the UUCMS and Gauhati cases provide strong evidence of privilege misuse without identifying a classic web vulnerability such as SQL injection or remote code execution.

## 3. Student Data Exposure: GTU, IIT Roorkee, And PhysicsWallah

### GTU: Large impact, missing root cause

Gujarat Technological University's 2020 incident exposed a highly usable identity package: photographs and government-ID information associated with approximately 1,200 engineering students [10]. Police-related reporting said an engineering student from an affiliated college uploaded data and that another alleged hacker remained sought [2]. That establishes harm and a human role but not the server-side weakness.

The absence of a technical postmortem is analytically important. It would be unsound to relabel this as IDOR, SQL injection, an exposed backup, or credential theft. **Inference:** for MUJ, the correct lesson is not to optimize for one imagined exploit. It is to inventory where Aadhaar, PAN, photographs, and identity documents exist; minimize copies; encrypt or tokenize sensitive fields; constrain bulk export; and alert on unusual download volume.

### IIT Roorkee: An object-authorization warning

The IIT Roorkee report is the closest core example to an IDOR/BOLA pattern. A public site allegedly exposed data for more than 30,000 current and former students, including student and parent mobile numbers, caste, financial background, email, admission and graduation years, and photographs [16]. A person could retrieve a record by entering an enrollment number, and the site was believed to have existed for roughly 10 years [16]. The institute ordered an inquiry after the newspaper's alert [16].

**Inference:** predictable enrollment numbers appear to have functioned as object locators without an adequate entitlement gate. That is BOLA-like, not confirmed BOLA. OWASP defines object-level authorization as the code-level check that a user may access the requested object and says every endpoint accepting an object ID should verify the logged-in user's permission for the requested action [13]. Random identifiers can add friction, but OWASP separately requires authorization and tests [13].

For MUJ, a record request should be authorized from authenticated identity, role, relationship, and permitted purpose. A student should not obtain another student's record merely by changing an identifier; a parent role should be bound to a verified relationship; faculty access should be limited to assigned courses or duties; and administrator bulk access should be exceptional and monitored. These are defensive requirements, not an invitation to test the live portal.

### PhysicsWallah: Useful adjacent evidence with source limitations

CyberX9's June 2025 publication alleged that PhysicsWallah exposed millions of student and parent records through IDOR, missing authorization, and absent rate limits [1]. It listed names, contact information, addresses, government IDs, academic data, photographs, parent details, and course or center information [1]. The researcher said it notified company founders on April 22, received fix confirmation on May 1, and escalated to CERT-In and NCIIPC on May 31 [1].

This is valuable because it gives an explicit class and disclosure timeline. It is not equivalent to an independent regulator's finding, and PhysicsWallah is not a university. **Inference:** it supports testing object authorization in education software, but it must not be used to claim that exposed APIs dominate Indian university incidents.

## 4. Marks Tampering: Identity And Workflow Failures Dominate

### Karnataka's repeated UUCMS pattern

The Bengaluru North University case is the clearest cash-for-marks example. Investigators reportedly found that accused persons misused the registrar's login credentials and changed marks for more than 60 students; the accused allegedly received INR 15,000-20,000 from each student [5]. Police arrested three people, froze their accounts, and continued investigating a wider group [5]. Government and UUCMS officials announced a high-level probe and tighter security, while the institution sought beneficiary details before issuing degrees [5].

A later Bangalore University incident affected 55 students in two private colleges and the Jnanabharati campus; five passed due to the alterations [11]. The registrar said the attackers used his login ID and password, changed marks at night, and bypassed the OTP normally sent during a password change. He discovered the changed password the next morning [11]. The university formed an internal committee, planned a police complaint, and said original marks would remain [11].

The repeated system name does not prove the same root cause. One case involved alleged bribery and arrests; the other report left motive partly uncertain and said UUCMS officials had not answered queries [11]. **Inference:** the shared control weakness is excessive reliance on one privileged session or credential. MFA helps, but MFA alone is insufficient if recovery, OTP, session, help-desk, or application workflows can bypass it.

### Gauhati University: Third-party privilege is first-party risk

Gauhati University's cash-for-marks case arose after a discrepancy in one college marksheet triggered investigation [22]. Police reported nine arrests, at least 10 inflated-mark instances, and no fewer than 50 students who apparently paid [22]. CID sources said the Integrated University Management System covered admissions, examinations, re-evaluation, finance, records, grievance functions, and student and alumni databases; the university had outsourced it, ITI Limited handled data entry, and tampering occurred at that end [22].

This case expands the threat model from stolen credentials to authorized operators abusing legitimate capabilities. **Inference:** MUJ should treat vendors, temporary staff, and data-entry personnel as privileged actors. Contracts, background processes, and NDAs do not replace technical separation of duties.

### Marks-control design for MUJ

| Control | Required behavior | Evidence it is working |
|---|---|---|
| Two-person authorization | One person proposes a post-publication marks change; a separately authenticated authorized person approves it | No single account can complete the transaction; approver and initiator differ |
| Step-up identity | Re-authenticate privileged users for marks publication, reopening, or bulk correction | M365 and application logs show strong authentication tied to the transaction |
| Append-only audit | Store actor, time, student, course, old value, new value, reason, approver, and source session | Daily reconciliation can reproduce every final mark from approved changes |
| Temporal and volume alerts | Flag after-hours changes, many students, repeated failures, or unusual campuses | Alert is triaged within a defined service-level objective |
| Independent reconciliation | Compare SLCM results with signed departmental source records before publication | Exceptions are reviewed before transcripts or degrees issue |
| Vendor least privilege | Restrict operators to assigned functions, cohorts, and time windows | Quarterly access review shows no dormant or excessive privilege |

The decision-ready lesson is that examination integrity needs accounting-style controls. Credential hardening prevents some entry, while dual control and reconciliation limit damage even when a valid account is compromised.

## 5. Payment Fraud: Secure The Workflow And The University's Name

Sri Venkateswara University's case was not described as payment-gateway hacking. It involved manipulated receipts with fake official seals and forged employee signatures for examination-related certificate fees [20]. The Hindu reported INR 65,686 in alleged misappropriation and alleged involvement by an enquiry-counter employee and an academic consultant [20]. The registrar complained and campus police registered a case [20].

The mechanism is therefore reconciliation failure plus possible insider collusion. **Inference:** a receipt should never be treated as independent proof of settlement. MUJ should verify payment from a server-to-server gateway event or bank reconciliation record, bind that event to student and fee liability, and make later reversal visible. Manual adjustments should require reason codes and dual approval.

Sai Nath Educational illustrates the external half of payment risk. A student allegedly paid INR 32,000 through a near-identical unofficial website and discovered that the university had not received it [21]. The institution asked police to take down the site; investigators traced its creation to a Bihar-based designer, examined who commissioned it, and followed the recipient bank account [21]. The case remained open, so criminal responsibility was not finally established in the cited source.

**Inference:** MUJ cannot prevent every domain registration, but it can reduce successful impersonation. It should publish a short canonical list of payment domains, place the list on admission letters and verified social channels, digitally sign or centrally validate receipts, monitor confusing domains, and give applicants a well-advertised verification channel. Takedown, registrar, hosting, search-engine, payment-provider, and bank contacts should be preassembled.

| Payment threat | Preventive control | Detective control | Response control |
|---|---|---|---|
| Insider or fake receipt | Gateway-originated transaction ID; signed receipt; no screenshot-based acceptance | Daily liability-to-bank reconciliation; duplicate and gap detection | Freeze manual adjustment privilege; preserve logs; contact bank and police |
| Payee or bank-detail change | Two-person approval and out-of-band confirmation | Alert on beneficiary, merchant, callback, or settlement-account changes | Disable changed route and reconcile all affected transactions |
| Look-alike admissions site | Canonical domain list, verified communications, DMARC/SPF/DKIM for mail | Domain monitoring and reports from students | Rapid takedown and bank/payment-provider notification |
| Refund diversion | Refund only to validated original method except controlled exceptions | Compare refunds with original payer and approved case | Hold anomalous refund and invoke fraud review |

These controls reduce both cyber and administrative fraud. They also avoid the mistaken assumption that every payment incident begins inside the web application.

## 6. Ransomware: Sparse University Evidence, Strong Defensive Relevance

The reviewed public corpus did not yield a detailed Indian university-portal ransomware case with a documented initial-access vector, affected university systems, recovery timeline, and final outcome. This is an evidence gap. It should not be converted into the claim that Indian universities have not experienced ransomware.

AIIMS Delhi is the closest high-quality adjacent comparator. The cited Indian Express report described online services disabled for a week, five infected servers among 40 physical and 100 virtual servers, and approximately 3-4 crore patient records hosted on the five systems [19]. It also said reports of patient data theft had no factual basis [19]. That distinction is essential: system infection and operational disruption do not by themselves prove exfiltration.

CERT-In's India Ransomware Report 2022 found a 53% year-over-year increase in reported ransomware incidents and said ransomware groups broadened attacks across critical sectors [25]. The report says actors try to infect or destroy online backups and recommends current offline backups plus regular recovery testing and the 3-2-1 rule [25]. It also recommends segmentation, prioritizing patches for public-facing systems, MFA for critical assets, least privilege, log monitoring, and tested ransomware response plans [25].

**Inference:** MUJ's highest-consequence ransomware scenario is not only loss of the public portal. It is simultaneous loss of identity, SLCM, examinations, payment reconciliation, shared storage, and online backups during admissions or results. Recovery objectives should therefore be set per business process.

| Recovery asset | Minimum defensive objective | Safe validation |
|---|---|---|
| Student and marks database | Offline or immutable copies plus point-in-time recovery | Restore into an isolated environment and reconcile record counts and audit chains |
| M365 identity configuration | Exported configuration, documented emergency identities, and privileged-role inventory | Tabletop loss of ordinary admin access without using production credentials |
| IIS/.NET deployment | Reproducible build, signed release artifact, secrets outside source and package | Rebuild a clean non-production instance from approved artifacts |
| Payment records | Independent bank/gateway settlement record | Reconcile recovered SLCM liabilities to external settlement data |
| Incident evidence | Time-synchronized, centralized logs protected from application administrators | Confirm retention, searchability, and chain of custody during exercises |

No live ransomware simulation should target production without written authorization, approved scope, rollback, and institutional oversight. A tabletop exercise and isolated restore test produce useful assurance without endangering student services.

## 7. Which Vulnerability Classes Actually Dominated?

The answer depends on honest classification. The seven-case core sample comprises GTU, IIT Roorkee, Bengaluru North University, Bangalore University, Gauhati University, Sri Venkateswara University, and Sai Nath Educational. Categories are assigned from the public account, not from speculation.

| Primary class | Core cases | Count out of 7 | Interpretation |
|---|---|---:|---|
| Privileged credential or trusted workflow abuse | Bengaluru North, Bangalore University, Gauhati University, Sri Venkateswara University | 4 | Dominant observed class; includes stolen/misused credentials, contractor privilege, and alleged insider process abuse |
| BOLA/IDOR-like public object access | IIT Roorkee | 1 | Analyst inference from enrollment-number retrieval; not source-confirmed IDOR |
| Look-alike domain/social engineering | Sai Nath Educational | 1 | External impersonation rather than compromise of the genuine portal |
| Unknown technical compromise | Gujarat Technological University | 1 | Exposure established, root cause not publicly established |
| Explicitly named exposed API/IDOR | None in core sample | 0 | PhysicsWallah supplies adjacent, researcher-reported evidence only |
| Ransomware | None in core sample | 0 | AIIMS supplies an adjacent operational comparator |

Thus, **weak identity, excessive privilege, and inadequate process integrity dominate this corpus**. Four of seven core cases fall directly into that family. If external trust abuse at Sai Nath is included in a broader identity-and-authenticity family, the figure becomes five of seven, but that broader grouping should not be confused with login authentication.

IDOR does not dominate the core university sample. It appears once as an inference at IIT Roorkee and once explicitly in the adjacent PhysicsWallah report. Exposed APIs likewise do not dominate the university evidence; the reviewed reports often lack enough architecture detail even to determine whether an API was involved.

This finding has a practical implication. A security program focused only on CVEs, WAF rules, and penetration tests could miss the most repeated failure mode: a legitimate-looking high-privilege action with an illegitimate purpose. MUJ needs both application security and transactional integrity.

## 8. Typical Disclosure Outcomes: Enforcement First, Detail Later Or Never

| Outcome in seven core cases | Cases | Count | What the public record shows |
|---|---|---:|---|
| Police complaint, registered case, or arrest | GTU, Bengaluru North, Gauhati, Sri Venkateswara, Sai Nath | 5 | Law-enforcement action is the most frequent visible outcome [2][5][22][20][21] |
| Internal or government inquiry | IIT Roorkee, Bengaluru North, Bangalore University, Gauhati | 4 | Institutions often announce investigation before publishing technical conclusions [16][5][11][22] |
| Arrests publicly reported | GTU, Bengaluru North, Gauhati | 3 | Enforcement can be concrete even when technical disclosure is sparse [2][5][22] |
| Explicit integrity restoration | Bangalore University | 1 | Source says original marks would remain and altered ones would not be reflected [11] |
| Announced security tightening | Bengaluru North/UUCMS | 1 | Announcement did not include a detailed public control list [5] |
| Confirmed technical fix in a core case | None documented in reviewed articles | 0 | This means "not documented here," not necessarily "not performed" |
| Full public root-cause postmortem | None documented in reviewed articles | 0 | Mechanisms were described, but no end-to-end technical report was found |

The adjacent PhysicsWallah account shows a different disclosure path: researcher contact, a reported nine-day interval to fix confirmation, and later regulator escalation [1]. The SPPU denial shows another possible outcome: rapid rejection of a rumor [12].

**Inference:** Indian education-sector disclosure appears reactive and fragmented. Police activity, committees, and press statements are visible; affected-person communication, vulnerability detail, control validation, and lessons learned are less visible. MUJ can improve trust by publishing a bounded post-incident notice that states systems affected, data or records involved, containment, user action, and validated corrective themes without exposing exploitable detail.

CERT-In's directions add a time constraint. Covered bodies must report Annexure I incidents within six hours of noticing them or being informed; the listed categories include application attacks, data breach, and data leak [18]. Covered organizations must also retain ICT logs securely in India for 180 days and synchronize time to specified or traceable NTP services [18]. Applicability to a specific MUJ incident should be confirmed by counsel and the incident commander, but operational readiness cannot wait for that discussion.

The Digital Personal Data Protection Act text requires a Data Fiduciary to take reasonable security safeguards and to notify the Board and affected Data Principals in the prescribed manner after a personal-data breach [24]. Its schedule states maxima of INR 250 crore for failure to take reasonable safeguards and INR 200 crore for failure to provide the specified notice [24]. The act itself says provisions commence on dates appointed by government notification, potentially on different dates [24]; current applicability and subordinate rules should therefore be checked rather than assumed.

## 9. Priority Defensive Plan For The MUJ SLCM Stack

### Priority matrix

| Priority | Defensive action | Incident evidence addressed | MUJ-specific acceptance criterion |
|---:|---|---|---|
| 1 | Protect registrar, examination, finance, and tenant-admin identities with phishing-resistant MFA where feasible, Conditional Access, separate admin accounts, and controlled recovery | Both Karnataka cases used registrar credentials and one reported OTP bypass [5][11] | No privileged role uses shared credentials; legacy authentication blocked; every recovery event logged and reviewed |
| 2 | Enforce server-side object authorization on every student, parent, marks, document, and payment object | IIT Roorkee behavior and adjacent PhysicsWallah IDOR [16][1] | Automated negative tests prove one role cannot access another role's object merely by changing an identifier |
| 3 | Add dual approval, append-only history, and daily reconciliation for marks | Bengaluru North, Bangalore University, and Gauhati [5][11][22] | Every post-publication change has distinct initiator and approver plus before/after values |
| 4 | Bind receipts to gateway or bank settlement and monitor look-alike domains | Sri Venkateswara and Sai Nath [20][21] | A receipt cannot create entitlement without independent settlement; canonical payment domains are published |
| 5 | Centralize Akamai, IIS, application, M365, database-audit, and payment logs | CERT-In requires reporting and 180-day logs for covered entities [18] | One incident timeline can correlate edge request, session, identity, transaction, and database change using synchronized time |
| 6 | Patch the supported stack and reduce legacy exposure | CERT-In says ransomware groups exploit known vulnerabilities with available patches [25] | Complete asset/SBOM inventory, defined patch SLA, no unsupported internet-facing component without an approved compensating control |
| 7 | Build immutable/offline backups and test isolated restoration | CERT-In emphasizes offline backups, testing, and 3-2-1 retention [25] | Quarterly exercise restores marks, identity dependencies, and payment reconciliation within approved objectives |
| 8 | Operate a vulnerability disclosure channel | PhysicsWallah's account shows researcher-to-company-to-regulator escalation [1] | Published `security.txt` or equivalent, monitored mailbox, acknowledgment SLA, safe evidence-handling procedure |

### Identity and M365

Microsoft's security defaults include MFA registration for all users, administrator MFA, MFA when necessary, and blocking legacy authentication [14]. Microsoft says complex organizations should consider Conditional Access instead [14]. For MUJ, the policy should distinguish high-volume student access from high-impact administrative authority. Registrar and finance identities warrant stronger factors, compliant devices or managed workstations, location and risk evaluation where appropriate, short privileged sessions, and re-authentication before consequential actions.

Emergency accounts need documented, tightly monitored treatment. They should not become a routine bypass. Privileged-role assignment, authentication-method change, password reset, new OAuth consent, and Conditional Access policy change should generate high-severity review.

### ASP.NET MVC, .NET Framework, IIS, And Akamai

Under the supplied architecture assumption, MUJ should maintain an exact component inventory rather than rely on broad labels such as ".NET 4.x." Patch status, third-party packages, authentication middleware, session configuration, and deployment artifacts matter more than the framework name alone.

For every state-changing action, require anti-forgery protection appropriate to MVC 5, authorization independent of UI visibility, strict input validation, secure cookie attributes, safe error handling, and least-privilege application-pool identities. Secrets should not be stored in source repositories, web roots, backups, or deployment packages. IIS should expose only required handlers and methods, with diagnostic detail restricted from public responses.

Akamai can provide valuable edge filtering, rate controls, and telemetry. **Inference:** it cannot determine academic ownership or approve a marks change. The origin should accept intended traffic paths, while the application must make entitlement decisions. Any direct-origin exposure should be treated as an architecture risk and reviewed defensively by authorized staff.

### Safe assurance for a student security club

The club should work only under written authorization and use isolated replicas, synthetic identities, and non-production data. Appropriate activities include threat modeling, reviewing source or configuration supplied by the university, writing unit and integration tests for authorization, tabletop incident exercises, and checking public brand impersonation through passive sources. It should not enumerate student IDs, attempt credential reuse, bypass access controls, alter records, send phishing messages, or test production availability.

## 10. Synthesis: Mechanism, Scope, Trade-Offs, And Evidence

| Dimension | Data-exposure cases | Marks-integrity cases | Payment-fraud cases | Ransomware comparator |
|---|---|---|---|---|
| Primary mechanism | Public object access, unknown compromise, or alleged IDOR | Compromised registrar credentials, OTP bypass, or privileged operator abuse | Fake receipts, insider process abuse, or look-alike domain | Malware-driven service disruption; cited entry vector unknown |
| Primary harmed property | Confidentiality and privacy | Integrity, fairness, and credential legitimacy | Financial integrity and institutional authenticity | Availability, recovery integrity, and possibly confidentiality |
| Best early detector | External exposure inventory, access anomaly, bulk-read alert | Before/after audit, after-hours and bulk-change alert, reconciliation | Bank/gateway reconciliation and domain monitoring | EDR, lateral-movement telemetry, backup monitoring, service-health alerts |
| Strongest preventive control | Per-object authorization and data minimization | Dual control plus strong privileged identity | Independent settlement verification and verified domains | Segmentation, patching, MFA, least privilege, offline backups |
| Evidence limitation | Technical root cause often unnamed | Initial credential-acquisition method usually unknown | Open cases and alleged insider roles | No detailed university case in reviewed corpus |
| Time horizon | Exposure may persist for years | Damage may occur in one privileged session | Fraud peaks around admission, examination, or certificate deadlines | Disruption can affect many services at once |

Three non-obvious tensions emerge.

First, stronger login authentication does not guarantee transaction integrity. The Bangalore University report describes an OTP bypass, while Gauhati involves people operating a trusted data-entry process [11][22]. MFA is necessary, but dual approval and reconciliation are what make a fraudulent transaction difficult to complete silently.

Second, privacy and integrity failures require different telemetry. An IDOR-like leak may consist of many individually valid-looking reads; marks fraud may be one valid-looking write. Rate limiting helps the former, while context-rich audit and independent approval help the latter. A single generic "security log" is unlikely to serve both well.

Third, edge security and application security are complementary, not interchangeable. OWASP requires authorization at every object-using function [13]. **Inference:** Akamai may stop known malicious patterns and excessive traffic, but an authenticated request using a legitimate identifier can still be unauthorized in the university's business context.

The holistic strategy is therefore layered: protect identity, authorize every object, make high-impact changes dual-controlled, reconcile money and marks independently, minimize exposed data, preserve correlated evidence, and rehearse restoration. This approach addresses the observed incidents without pretending that one vulnerability class explains them all.

## VERDICT

**Verdict: The dominant publicly supported risk in the reviewed Indian university cases is abuse of privileged identity and administrative workflow, not confirmed IDOR or exposed APIs.** Four of seven core cases directly involve privileged credentials, contractors, or insiders. One case is BOLA/IDOR-like by inference, one is a look-alike-domain fraud, and one has an undisclosed technical cause. Explicit IDOR appears in the adjacent PhysicsWallah researcher report, not in a core university case.

For MUJ SLCM, the highest priorities should be: (1) protect registrar, examination, finance, and M365 privileged identities; (2) require server-side object authorization; (3) dual-control and reconcile marks and payments; (4) centralize time-synchronized evidence for the six-hour CERT-In decision window; and (5) maintain tested offline or immutable recovery. Akamai and routine patching remain important, but they cannot compensate for weak business authorization or unreviewed privileged actions.

**Overall confidence: Moderate-high.** Confidence is high for the existence, scale, and public outcomes of the strongest named cases. Confidence is moderate for cross-case dominance because the sample is small, media-selected, and technically incomplete. Confidence is low for any claim that a specific unreported exploit caused GTU or IIT Roorkee, or that ransomware is rare in universities. Those claims are not made.

**Residual unknowns:** no full public technical postmortem was found for the seven core cases; acquisition paths for registrar credentials were not established; the IIT Roorkee exposure was not independently classified as IDOR; current remediation status was often unreported; and the reviewed corpus did not establish a detailed Indian university ransomware case. These gaps justify defensive testing in authorized, non-production environments, not probing of the live MUJ portal.

## References

1. *PhysicsWallah recklessly exposed highly sensitive personal ...*. https://www.cyberx9.com/physicswallah-millions-students-defense-data-exposed-blog
2. *23-yr-old uploaded data to force GTU to put off exams*. https://www.ahmedabadmirror.com/23-yr-old-uploaded-data-to-force-gtu-to-put-off-exams/77360275.html
3. *Exposed Git Directory Leak Compromises 1.5M Records*. https://femtosec.io/threat-intelligence/exposed-git-repository-student-database-breach
4. *Assam Cash-for-Marks Scam: Nine Arrested in Digital Tampering ...*. https://undercoverist.org/assam-cash-for-marks-scam-nine-arrested-in-digital-tampering-case/
5. *UUCMS portal of Bengaluru North University hacked and marks of students tampered with - The Hindu*. https://www.thehindu.com/news/national/karnataka/uucms-portal-of-bengaluru-north-university-hacked-and-marks-of-students-tampered-with/article68740901.ece
6. *‘Access denied’: Mumbai University can’t see its digital ...*. https://timesofindia.indiatimes.com/city/mumbai/access-denied-mumbai-university-cant-see-its-digital-infra-as-five-staffers-protect-passwords-cyber-audit-hits-a-wall/articleshow/122805956.cms
7. *GTU website hacking: Cops nab engg student - Ahmedabad Mirror*. https://www.ahmedabadmirror.com/gtu-website-hacking-cops-nab-engg-student/77641315.html
8. *Gauhati University marks ‘scam’: Panel to examine software used to store student scores*. https://www.telegraphindia.com/north-east/gauhati-university-marks-scam-panel-to-examine-software-used-to-store-student-scores/cid/2030902
9. *IIT-Roorkee data breach: Over 30,000 student's, personal ...*. https://government.economictimes.indiatimes.com/news/secure-india/iit-roorkee-data-breach-exposes-personal-information-of-over-30000-students/123233870
10. *Gujarat Technological University system hacked, 1,200 ...*. https://www.deccanherald.com/india/gujarat-technological-university-system-hacked-1200-students-personal-data-leaked-867789.html
11. *How marks of 55 Bangalore University students were illegally changed: Inside UUCMS breach that’s shaking K*. https://m.economictimes.com/news/new-updates/how-marks-of-55-bangalore-university-students-were-illegally-changed-inside-uucms-breach-thats-shaking-karnatakas-education-system/articleshow/122039174.cms
12. *University website safe, says SPPU, after hack rumours*. https://www.hindustantimes.com/cities/pune-news/university-website-safe-says-sppu-after-hack-rumours-101756668455364.html
13. *API1:2023 Broken Object Level Authorization - OWASP API Security Top 10*. https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization
14. *Configure Security Defaults for Microsoft Entra ID - Microsoft Entra | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/fundamentals/security-defaults
15. *WSTG - Latest | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/12-API_Testing/02-API_Broken_Object_Level_Authorization
16. *IIT-Roorkee data breach exposes personal details of 30k+ alumni | Dehradun News - Times of India*. https://timesofindia.indiatimes.com/city/dehradun/iit-roorkee-data-breach-exposes-personal-details-of-30k-alumni/articleshow/123220043.cms
17. *Block legacy authentication with Conditional Access - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/conditional-access/policy-block-legacy-authentication
18. *No. 20(3)/2022-CERT-In Government of India Ministry of Electronics and Information Technology (MeitY) Indian Computer Emergency Response Team (CERT-In) Electronics Niketan,*. https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf
19. *AIIMS cyber attack: At least five servers infected, have data  of 3-4 crore patients | Delhi News - The Indian Express*. https://indianexpress.com/article/cities/delhi/aiims-cyber-attack-at-least-five-servers-infected-have-data-of-3-4-crore-patients-8297028
20. [
	Fake fee receipt scam unearthed in SV University - The Hindu
](https://www.thehindu.com/news/national/andhra-pradesh/fake-fee-receipt-scam-unearthed-in-sv-university/article71041791.ece)
21. *How a Cloned University Portal Cheated a Student Out of Her Fees - The420.in*. https://the420.in/sai-nath-university-fake-website-student-fraud-agra/
22. *Gauhati University Marsheet scam: "Cash-For-Marks" Scam In Assam's Gauhati University, 9 Arrested*. https://www.ndtv.com/india-news/gauhati-university-marsheet-scam-marksheet-tampering-scam-detected-at-assams-gauhati-university-6003115
23. *UP Police Thwart Cyber Fraud of Rs. 120 Crore, Seven Arrested*. https://undercoverist.org/up-police-thwart-cyber-fraud-of-rs-120-crore-seven-arrested/
24. [xxxGIDHxxx xxxGIDExxx vlk/kkj.k Hkkx [k.M izkf/kdkj ls izdkf'kr PUBLISHED BY AUTHORITY lañ ubZ fnYyh] 'kqØokj] vxLr 11] 2023@Jko.k 20] 1945](https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf)
25. *Ransomware Report*. https://www.csk.gov.in/documents/IndiaRansomwareReport2022.pdf
26. *http://mujslcm.jaipur.manipal.edu/*. http://mujslcm.jaipur.manipal.edu/
