# MUJ SLCM Responsible Disclosure Playbook for India

## Executive Summary

- **Authorization Is The Hard Boundary**: The Information Technology Act's Section 43 includes access, copying or downloading data, disruption, denial of access, assistance, alteration, and damage-related conduct; Section 66 applies criminal punishment when a Section 43 act is done "dishonestly or fraudulently" [4]. -> The club should obtain written, asset-specific authorization before any active validation and should not assume that educational purpose, good intentions, or student status creates permission.

- **MUJ SLCM Protects High-Impact Academic Records**: Manipal's own material describes SLCM as a single-window system containing attendance, internal marks, external marks, result publication, and broadcast messages [1]. -> Confidentiality and examination integrity should outrank technical curiosity; proof should be minimal, redacted, and gathered only within approved accounts and scope.

- **The Detailed Stack Is A Premise, Not A Verified Finding**: The public MUJ portal confirms sign-in surfaces for institutional, parent, and student users [54], but this research did not independently validate the stated ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, or Microsoft 365 components. -> Treat those details as user-supplied scoping assumptions, not as findings and never as a basis for exploit selection.

- **Ninety Days Is A Coordination Norm, Not Permission**: Google Project Zero gives a vendor 90 days to make a patch available and normally discloses 30 days after a patch; if no patch exists at day 90, it discloses then [3]. -> MUJ and the club may use 90 days as a planning ceiling, but testing authority and publication permission must be negotiated separately.

- **Education-Sector Reception Varies Sharply**: IIT Roorkee publicly thanked a young researcher, said it was plugging a cloud-storage issue on priority, and disputed claims of a large-scale leak [42]. In the CBSE case, the researcher alleged nearly three months of weak follow-up before CBSE later said identified issues had been contained and thanked alert citizens and ethical hackers [47][46]. -> Acknowledgment, technical confirmation, containment, and public credit should be tracked as four separate outcomes.

- **Fast Fixes Are Achievable**: Zomato reportedly fixed Anand Prakash's 2015 report within a day and allowed publication after remediation [43]. In a 2024 IRCTC-related case, a researcher reported through CERT-In on July 23 and CERT-In confirmed a fix on July 30 [40]. -> A concise report, a competent recipient, and a coordinating body can collapse remediation from months to days.

- **CERT-In Has Two Distinct Roles**: Its responsible-disclosure process is intended to give vendors sufficient remediation time and involves researchers, academic institutions, vendors, and other CERTs [53]. Separately, CERT-In's 2022 Directions impose six-hour incident reporting on specified organizations, not expressly on independent researchers [50]. -> Do not confuse voluntary vulnerability coordination with the organization's statutory incident-reporting obligation.

- **Severity Needs Two Layers**: CVSS v4.0 scores technical severity from 0.0 to 10.0, but FIRST says regulatory, customer, financial, safety, and reputational factors sit outside CVSS [45]. -> Pair a reproducible CVSS vector with an MUJ-specific impact statement about marks, attendance, results, identity, or parent access.

- **Minimal Proof Is The Safest Proof**: CISA's model policy says researchers should avoid privacy violations, disruption, and data manipulation, use an exploit only as needed to confirm presence, and stop immediately on encountering sensitive data [48]. -> A club report should prefer screenshots of its own approved test account, redacted logs, and expected-versus-observed behavior over copied student records or broad enumeration.

**Decision-ready insight:** MUJ should establish a written vulnerability disclosure policy and named security intake before asking students to investigate anything. Until that exists, the club should limit itself to passive public-information review and seek written authorization for a segregated test environment.

## Scope, Evidence Labels, And Reasoning Boundary

This report uses only public material and the technology description supplied in the query. It does not claim that MUJ SLCM is vulnerable, does not validate the named framework versions, and does not provide payloads, bypass sequences, account-manipulation instructions, or methods for accessing another person's data.

The request asks for explicit chain-of-thought reasoning. I cannot provide private hidden chain-of-thought. Instead, this report provides an auditable substitute: cited evidence, confidence labels, a decision-rationale table, explicit inferences, and the assumptions that would change each conclusion.

| Evidence label | Meaning in this report | Example |
|---|---|---|
| Verified public fact | Directly stated by a cited public source | Manipal describes SLCM as covering attendance, marks, results, and circulars [1]. |
| Source-attributed claim | Reported by a researcher or journalist but not independently confirmed here | The CBSE researcher claimed that some issues remained unpatched after acknowledgment [47]. |
| Recipient-confirmed fact | Publicly stated by the affected institution or its representative | IIT Roorkee said the storage was read-only and the issue was being plugged on priority [42]. |
| User-supplied premise | Present in the query but not independently established by this research | ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 identity. |
| Analyst inference | A risk or recommendation derived from cited facts, explicitly labeled as inference | An authorization flaw affecting marks would have unusually high academic-integrity impact. |
| Unknown | Not supported by the reviewed public record | Whether MUJ operates a private VDP, safe harbor, bug bounty, or security mailbox. |

**Inference:** The absence of a discovered public policy is not proof that MUJ lacks an internal security process. It means a student researcher should not rely on a policy or safe harbor that cannot be produced in writing.

## MUJ SLCM Scope: Academic Integrity Before Technical Curiosity

### What is publicly established

The MUJ portal publicly presents institutional, parent, and student sign-in choices [54]. An official Manipal ICT document says SLCM replaced an older academic-management system and acts as a single window for attendance, internal and external marks, result publication, and circulars for students and parents [1]. These are enough facts to identify the system as high impact without probing it.

| Surface or capability | Public status | Security significance | Permitted conclusion |
|---|---|---|---|
| MUJ SLCM hostname | Publicly visible [54] | Identifies the application owner and disclosure target | It may be named in a report, but visibility does not grant testing permission. |
| Student login | Publicly visible [54] | Likely gates student-specific functions | No conclusion about authentication strength is justified. |
| Parent login | Publicly visible [54] | Creates a distinct role and authorization boundary | **Inference:** role separation deserves authorized testing. |
| Institutional sign-in | Publicly visible [54] | May involve institutional identity services | The exact identity architecture remains unverified. |
| Attendance and marks | Officially documented [1] | Confidentiality and integrity affect students directly | **Inference:** unauthorized viewing and alteration would be high-impact outcomes. |
| Results and circulars | Officially documented [1] | Results are sensitive; circulars may affect many users | **Inference:** integrity and availability tests require strict change controls. |
| ASP.NET MVC 5.3 and .NET 4.x | User-supplied premise | Version-specific assumptions may be stale or wrong | Do not select tests or claim exposure from the version label alone. |
| IIS 10, Akamai, Microsoft 365 | User-supplied premise | Edge and identity layers may have different owners | Confirm ownership and scope in writing before any active work. |

### The practical risk model

**Inference:** SLCM's most consequential risks are not generic web scores alone. They include unauthorized viewing of marks or attendance, unauthorized modification of academic records, impersonation across student/parent roles, disclosure of identity or contact data, and loss of availability during registration or result periods. Each is an impact hypothesis, not an allegation about MUJ.

The club should therefore use a data-flow and role model before a technical checklist. The relevant subjects are students, parents, faculty, examination staff, administrators, identity providers, application operators, and third-party service providers. The protected objects include marks, attendance, results, circulars, credentials, audit trails, and account-recovery data. This is an analyst model based on SLCM's documented functions [1], not a map of MUJ's private architecture.

**Decision-ready insight:** The first club deliverable should be a one-page scope and authorization agreement, not a scanner output. It should name test accounts, environment, dates, allowed methods, prohibited methods, data-retention rules, emergency contacts, and publication approval.

## Indian Disclosure Case Studies: Reception, Timelines, And Failure Modes

### Comparative case table

| Case | Private report or trigger | Reception | Remediation or outcome | Evidence limitation |
|---|---|---|---|---|
| JEE Advanced 2026 / IIT Roorkee | A 16-year-old researcher flagged a cloud-storage configuration issue; the article was published June 5, 2026 [42] | IIT Roorkee thanked the researcher and applauded responsible behavior [42] | The institution said the issue was being plugged on priority and described storage as read-only [42] | Large exposure figures were allegations; the institution called leak claims misleading [42]. |
| CBSE On-Screen Marking | Researcher said issues were found February 25, 2026 and sent to CERT-In, with evidence supplied on request [47] | CERT-In allegedly acknowledged registration; researcher alleged little substantive follow-up [47] | CBSE later said identified vulnerabilities had been contained and thanked alert citizens and ethical hackers [46] | CBSE is an education board, not a university; early chronology is the researcher's account. |
| Zomato 2015 | Anand Prakash approached Zomato in June 2015 [43] | Zomato treated it as ethical disclosure and permitted later publication [43] | Reportedly fixed within one day [43] | The report does not establish exploitation, actual access, or a bounty [43]. |
| IRCTC insurance portal 2024 | Nilabh Rajpoot reported through CERT-In on July 23, 2024 [40] | CERT-In communicated with the relevant organization [40] | CERT-In reportedly confirmed a fix on July 30 [40] | The detailed account is a secondary commercial source; the affected component was a third-party insurance portal [40]. |
| Ola current program | First-party policy defines asset scope and excludes staging and sandbox environments [49] | Provides a formal route and rules for researchers | Demonstrates governance rather than one completed case | A policy cannot prove how every future report will be handled. |

### Case study 1: IIT Roorkee shows how public credit can coexist with factual disagreement

The JEE Advanced case is the closest documented university-level analogue found. Firstpost reported that IIT Roorkee, which conducted that year's JEE Advanced, acknowledged and fixed a cloud-storage configuration issue after it was flagged by 16-year-old Rylen Anil [42]. The institution publicly thanked the named researcher, said it was plugging the issue on priority, described the stored material as read-only, and applauded his responsible and ethical behavior [42].

Reception was therefore positive in one important sense: the finder received public acknowledgment instead of a public threat. Yet the parties did not agree on impact. The researcher alleged that large numbers of result records and admit-card files could be accessed; IIT Roorkee called claims of a large-scale leak misleading and factually incorrect [42]. The researcher also said he had downloaded only a small number of files for verification and deleted them [42].

**Inference:** This case shows why a good report separates "vulnerability confirmed," "records potentially reachable," and "records actually acquired." A recipient can accept the configuration problem while disputing the exposure count. For MUJ, the club should never estimate affected students by broad collection. It should provide a bounded hypothesis and ask the authorized owner to calculate exposure from server-side logs.

### Case study 2: CBSE illustrates acknowledgment without confidence-building communication

Nisarga Adhikary told NDTV that he discovered weaknesses in CBSE's On-Screen Marking environment on February 25, 2026 and informed CERT-In, later supplying screen recordings and further details when requested [47]. He said CERT-In acknowledged registration and coordination but that substantive follow-up did not arrive, and he alleged that several issues remained for an extended period [47]. Those claims are attributable to the researcher, not independently proven here.

A later NDTV report recorded CBSE saying that vulnerabilities in its service provider's OnMark portal had been contained, that government and IIT cybersecurity specialists had been engaged, and that CBSE thanked alert citizens and ethical hackers while requesting official-channel reporting [46]. That later response is important counterevidence to a simple "ignored report" narrative.

**Inference:** The process failure was at least partly communicative. Even if internal work had begun, a generic acknowledgment followed by silence allowed the finder to conclude that little was happening. MUJ should issue a ticket number, owner, next-update date, and status labels such as "received," "triaged," "confirmed," "mitigating," "fixed," and "retest complete." It should not reveal sensitive remediation detail, but it should not leave a good-faith reporter guessing for months.

### Case study 3: Zomato demonstrates the value of rapid validation and controlled publication

The News Minute reported that Anand Prakash approached Zomato in June 2015 after identifying a weakness that could expose user information [43]. Zomato reportedly fixed it within a day, treated the event as ethical disclosure, and allowed Prakash to publish his account after the fix [43]. The source does not prove that data was actually taken or that Zomato paid a bounty [43].

The central lesson is not "pay every finder." It is that rapid reproduction, remediation, and permission to publish can align the firm's interests with the researcher's desire for recognition. **Inference:** MUJ can reproduce this incentive structure without a cash bounty by offering a hall of fame, signed acknowledgment, certificate, or supervised research credit after remediation and privacy review.

### Case study 4: IRCTC shows the value and limits of CERT-In coordination

A published account says Nilabh Rajpoot reported an IRCTC-linked insurance-portal issue to CERT-In on July 23, 2024; CERT-In relayed it to the relevant organization and confirmed remediation by July 30 [40]. The report described unauthorized access to passenger travel details and potential nominee changes, but the relevant component was a third-party insurance portal [40].

The seven-day interval is a useful positive case for neutral coordination. It also highlights ownership complexity: a university may depend on identity, payment, CDN, cloud, or software vendors, but students see one service. **Inference:** MUJ's intake process should accept the report first, identify the technical owner internally, and avoid making the student guess which vendor contract governs the component.

**Decision-ready insight:** Reception quality is measurable. Track acknowledgment time, time to confirmation, time to interim mitigation, time to fix, retest completion, reporter satisfaction, and whether publication occurred by agreement.

## The 90-Day Norm: Coordination Clock, Not Testing Permission

Project Zero's standard policy gives the vendor 90 days after notification to make a patch available. If a patch appears within that period, vulnerability details are normally released 30 days after the patch; if no patch appears, disclosure occurs at day 90 [3]. A vendor expecting to patch within another 14 days may request a grace period, while evidence of active exploitation invokes a seven-day rather than 90-day deadline [3].

This is a disclosure policy operated by one research team. It is not an Indian statute, a universal safe harbor, or permission to test MUJ. CISA's model policy instead uses the more contextual phrase "reasonable amount of time" before public disclosure [48].

### Proposed MUJ coordination clock

The following is an **analyst recommendation**, not a statement of existing MUJ policy or Indian law.

| Time from report | MUJ action | Researcher action | Publication status |
|---|---|---|---|
| 0-3 business days | Acknowledge, issue case ID, preserve logs, name coordinator | Stop testing; preserve minimal encrypted evidence | No publication |
| By day 7 | Validate scope, request only necessary clarification, assign provisional severity | Answer questions without expanding testing | No publication |
| By day 14 | Confirm, reject with reasons, or mark duplicate; deploy emergency mitigation if needed | Correct factual errors and agree on communication cadence | No publication |
| Every 14 days | Provide status and next milestone | Maintain confidentiality | No publication |
| By day 45 for critical/high | Target remediation or documented compensating control | Retest only when expressly invited | Joint advisory planning may begin |
| By day 90 | Complete remediation or agree to a justified extension | Do not publish automatically if disclosure would expose students | Coordinated decision, preferably written |
| Active exploitation | Escalate immediately to leadership, CERT-In, vendor, and incident response | Do not collect more evidence or alert attackers | Disclosure timing controlled by incident safety |

CISA's template suggests acknowledgment within three business days [48], so the proposed first milestone is realistic. **Inference:** Academic calendars matter. A vulnerability involving live results or examinations may require an immediate containment target measured in hours, while a low-impact header issue could safely take longer.

**Decision-ready insight:** Set the clock in the first acknowledgment. A deadline should motivate remediation, not become a threat. Publication requires a separate risk decision covering student privacy, exploitability after the fix, vendor dependencies, and legal review.

## IT Act Sections 43 And 66: Why Consent And Intent Both Matter

This section is risk guidance, not legal advice. The club and MUJ should obtain advice from an Indian cyber-law professional before active testing or contentious publication.

### Statutory risk matrix

| Provision or concept | Relevant statutory content | Research implication | Confidence |
|---|---|---|---|
| Section 43 access | The Act enumerates accessing or securing access to a computer resource [4]. | **Legal-risk inference:** accessing functionality outside an authorized account or scope can create exposure even when no damage is intended. | High on text; medium on application |
| Section 43 data acquisition | The Act enumerates downloading, copying, or extracting data or information [4]. | **Legal-risk inference:** copying another student's record as "proof" is materially riskier than stopping at the first indication. | High on text; medium on application |
| Section 43 operational harm | Enumerated conduct includes damage, disruption, denial of access, assisting access, account manipulation, deletion or alteration, and source-code interference [4]. | Do not run load tests, modify records, plant files, establish persistence, or help another person gain access. | High |
| Section 43 remedy | The cited text makes the responsible person liable to pay damages by way of compensation to the affected person [4]. | A good motive does not erase potential compensation exposure. | High on text |
| Section 66 mental element | A person who dishonestly or fraudulently does an act referred to in Section 43 may face up to three years' imprisonment, a fine up to five lakh rupees, or both [4]. | Intent, communications, data handling, and conduct may become critical evidence. | High on text; case-specific in application |
| Written authorization | CISA's model expressly treats compliant research as authorized and promises not to recommend legal action [48]. | An MUJ-specific signed authorization is stronger risk control than relying on an overseas template. | High as process advice |
| Sensitive-data stop rule | CISA says to stop when a vulnerability is established or sensitive data is encountered [48]. | Build this stop condition into the club's rules and report template. | High as best practice |

### Scenarios for the club

Every row below is an **analyst legal-risk inference**, not a determination that conduct is lawful or unlawful.

| Proposed activity | Risk assessment | Safe alternative |
|---|---|---|
| Reading the public login page and official documentation | Lower risk, but public visibility is not permission for intrusive testing | Record only URLs, visible labels, and official documents. |
| Checking published headers or public metadata once | Potentially low impact, but still obtain club and faculty rules | Use already published passive sources where possible. |
| Testing normal functions in one's own production student account | Medium to high risk because the account terms may not authorize security testing | Ask MUJ for named test accounts and a segregated environment. |
| Changing identifiers to seek another student's record | High legal and privacy risk | Describe the hypothesis; let MUJ validate server-side or provide two dummy accounts. |
| Password spraying, OTP guessing, credential stuffing, or social engineering | Unacceptable without explicit authorization; CISA's model excludes social engineering [48] | Review policy and identity configuration documentation with administrators. |
| Automated enumeration or load testing | High disruption, privacy, and denial-of-service risk | Use rate-limited tests in staging under an approved plan. |
| Altering marks, attendance, results, circulars, or account roles | Extremely high integrity risk | Use synthetic records in staging and verify audit logs. |
| Downloading a dataset to estimate affected users | High risk under the data-acquisition language of Section 43 [4] | Stop at the first indication and ask the owner to quantify from logs. |
| Publicly posting a live endpoint, token, payload, or student screenshot | High risk to students and remediation | Publish only after fix, retest, redaction, and written coordination. |

### CERT-In's role and the six-hour distinction

CERT-In says responsible coordination exists to give affected vendors or OEMs sufficient remediation time and that it collaborates with researchers, academic institutions, vendors, and other CERTs [53]. Its separate April 28, 2022 Directions require service providers, intermediaries, data centres, bodies corporate, and government organizations to report listed cyber incidents within six hours of noticing them or being informed; reports may go to `incident@cert-in.org.in`, the listed phone number, or fax [50]. Independent researchers are not named in that duty-holder list [50].

**Inference:** A vulnerability report is not automatically a reportable cyber incident, and the six-hour rule should not be misquoted as a universal researcher deadline. If evidence suggests exploitation, MUJ's responsible officers should determine their reporting obligation immediately. A student should use CERT-In's current official vulnerability-coordination page rather than assuming that an incident mailbox is the correct channel.

**Decision-ready insight:** Written authorization, minimal evidence, immediate stopping, and disciplined communications are not cosmetic ethics. They are the artifacts most likely to distinguish a bounded good-faith review from conduct that appears intrusive or dishonest.

## Zero-Unauthorized-Access Workflow For The Club

| Stage | Required action | Mandatory stop or gate | Deliverable |
|---|---|---|---|
| 1. Governance | Appoint faculty sponsor, club lead, legal/privacy contact, and MUJ technical owner | No active work without named owner | Project charter |
| 2. Passive scoping | Inventory only public domains, documentation, published contacts, and supplied architecture assumptions | Do not authenticate, enumerate, or scan | Passive surface register |
| 3. Authorization | Obtain signed scope naming hosts, environment, accounts, dates, tools, rate limits, data rules, and publication rules | Ambiguity means out of scope | Authorization letter |
| 4. Test design | Translate risks into test cases using synthetic data | No production mark, result, or identity changes | Approved test plan |
| 5. Minimal validation | Validate only the smallest fact needed in the authorized environment | Stop on first sensitive record, unexpected privilege, instability, or third-party system | Redacted evidence package |
| 6. Immediate notice | Send concise initial alert for credible high-impact findings | No additional proof unless requested in writing | Case ID and acknowledgment |
| 7. Triage | Agree on severity, affected owner, containment, and next update | Escalate internally if active exploitation is suspected | Triage record |
| 8. Remediation | Apply code, configuration, identity, logging, and process fixes | Retest only under renewed written permission | Fix record and regression tests |
| 9. Closure | Confirm scope of fix and securely delete unnecessary evidence | Retain only what policy or law requires | Closure statement |
| 10. Publication | Agree on wording, credit, date, and redactions | No live secrets, personal data, or reusable exploit instructions | Coordinated advisory |

The workflow adapts CISA's model boundaries: avoid privacy violations and disruption; use validation only as necessary; do not exfiltrate data, establish persistence, or pivot; and stop on sensitive data [48].

### Escalation ladder

1. Use a published MUJ security or VDP channel if one exists.
2. If none is published, ask MUJ's IT administration for the designated security contact without sending sensitive details to a broad mailbox.
3. Send a minimal encrypted or access-controlled report to the designated owner.
4. If a credible high-impact issue receives no acknowledgment, send a short follow-up referencing the original case ID and a proposed coordination date.
5. For unresolved serious risk, use CERT-In's official Responsible Vulnerability Disclosure and Coordination channel, which expressly works with researchers and academic institutions [53].
6. If exploitation or an incident is suspected, alert MUJ leadership and incident response immediately; the institution should assess the CERT-In six-hour obligation [50].
7. Seek legal advice before public disclosure where authorization, data access, or the recipient's position is disputed.

**Inference:** Admissions, finance, grievance, and general support addresses are poor places for sensitive vulnerability detail because distribution and retention may be broad. A short request for the correct security contact is safer than attaching evidence to a general mailbox.

## Professional Disclosure Report Template

### Required fields

| Field | What to include | What to exclude |
|---|---|---|
| Report ID and title | Neutral identifier and outcome-focused title | Sensational language such as "total takeover" without proof |
| Reporter | Name or pseudonym, secure contact, faculty sponsor | Unnecessary identity documents |
| Authorization | Approver, signed scope, environment, account IDs, test dates | Assumptions that student status equals permission |
| Affected asset | Exact host/application and owner | Unverified adjacent domains |
| Executive summary | One paragraph: condition, affected role/object, likely impact | Payloads or personal records |
| Discovery timeline | Discovery, stop, report, acknowledgment, update dates | Altered timestamps |
| Preconditions | Required role, approved account, environment | Stolen credentials or third-party access |
| Expected behavior | The security control that should have applied | Unsupported design claims |
| Observed behavior | Minimal, factual observation from authorized testing | Broad exploitation or user enumeration |
| Reproduction | Numbered steps already performed within scope | Instructions to access real users or persistence |
| Evidence | Redacted screenshot, request ID, server log correlation, hashes | Tokens, passwords, full response bodies, student PII |
| Technical severity | CVSS v4.0 vector, score, metric rationale | A score without a vector or assumptions |
| Business impact | Marks, attendance, results, identity, parent access, availability | Claiming a breach from mere possibility |
| Affected population | Known minimum and owner-calculated estimate | Researcher-side bulk collection |
| Interim mitigation | Disable path, restrict role, feature flag, monitoring | Destructive changes |
| Root-cause hypothesis | Clearly labeled hypothesis | Presenting guesswork as confirmed code behavior |
| Remediation | Server-side control, configuration, identity, logging, tests | Generic "sanitize everything" advice |
| Retest plan | Test accounts, environment, expected pass condition | Unapproved production retest |
| Disclosure plan | Embargo, credit, advisory owner, proposed publication date | Threats or unilateral release of live details |
| Evidence disposal | Deletion date, retained artifacts, custodian | Indefinite personal-data retention |

CISA recommends that a report identify the vulnerability's location, potential impact, and detailed reproduction steps; it also suggests that proof material can help [48]. In the MUJ context, "detailed" must still mean bounded and authorized. FIRST defines CVSS as a framework for communicating technical characteristics and severity, with Base, Threat, Environmental, and Supplemental metric groups [45].

### Copy-ready safe template

```text
CONFIDENTIAL SECURITY REPORT

1. Report metadata
Report ID:
Title:
Date and time zone:
Reporter and secure contact:
Faculty sponsor:

2. Authorization
Authorizing official:
Written authorization reference:
In-scope asset and environment:
Approved test accounts:
Approved dates and methods:

3. Executive summary
In one paragraph, state the observed security-control failure and the
potential effect. Do not include secrets or personal data.

4. Affected asset
Hostname/application:
Component or feature:
Owner or vendor, if known:
First observed version/date:

5. Preconditions
Required role:
Required approved account:
Required configuration:

6. Expected versus observed behavior
Expected:
Observed:

7. Minimal reproduction within authorized scope
Step 1:
Step 2:
Step 3:
Stop condition reached:
No other accounts or records accessed: Yes/No/Unknown

8. Evidence
Redacted screenshot identifiers:
Request or trace IDs:
Relevant timestamps:
Sensitive fields removed:
Evidence custodian and deletion date:

9. Severity
CVSS version and vector:
CVSS score and qualitative band:
Metric rationale:
MUJ-specific confidentiality impact:
MUJ-specific integrity impact:
MUJ-specific availability impact:
Academic-calendar urgency:

10. Scope of impact
Confirmed minimum:
Potential maximum, to be calculated by MUJ from logs:
Evidence of exploitation: Yes/No/Unknown

11. Remediation
Immediate containment:
Long-term code/configuration fix:
Logging and detection improvement:
Regression tests:

12. Coordination
Initial report date:
Acknowledgment date:
Next update date:
Proposed retest date:
Proposed disclosure date, subject to agreement:
Credit preference:
```

### Severity model for SLCM

CVSS v4.0 qualitative bands are None 0.0, Low 0.1-3.9, Medium 4.0-6.9, High 7.0-8.9, and Critical 9.0-10.0; use of the labels is optional [45]. CVSS also instructs consumers to enrich Base metrics with Threat and Environmental context [45].

| Dimension | Questions for MUJ | Report treatment |
|---|---|---|
| Technical exploitability | Is authentication required? Is user interaction required? Does impact cross an authorization boundary? | Encode only observed, authorized facts in the CVSS vector. |
| Confidentiality | Could marks, attendance, results, contact data, or identity records be viewed? | State confirmed minimum; do not collect more records. |
| Integrity | Could records, roles, circulars, or recovery details be changed? | Validate only in staging with synthetic data. |
| Availability | Could a single request or ordinary workflow impair service? | Do not perform load or denial testing in production. |
| Academic impact | Does timing overlap examinations, registration, or result publication? | Add urgency outside the CVSS score. |
| Population | How many roles and records are reachable? | Ask MUJ to calculate from architecture and logs. |
| Exploitation evidence | Do logs show abuse? | Escalate to incident response; do not investigate independently. |
| Regulatory/reputation | Are personal data, contractual vendors, or public trust affected? | Record as organizational risk outside CVSS [45]. |

### Sanitized hypothetical example

**Hypothetical only - not a finding about MUJ:** Suppose two institution-provided dummy student accounts in an authorized staging environment reveal that one test account can receive another dummy account's academic object because an ownership check is missing.

The report title should be "Missing server-side ownership check may expose another student's academic record." Reproduction should say only that two named dummy accounts and a synthetic record were used under authorization. It should not include a production endpoint, a reusable identifier-manipulation sequence, or any real student response.

The remediation would require a deny-by-default server-side authorization check on every object access, role and tenant validation, consistent enforcement across HTML and API paths, audit logging for denied and successful access, and regression tests using synthetic accounts. **Inference:** Because SLCM carries marks, attendance, and results [1], MUJ-specific impact could exceed the generic technical score, particularly near examination or result dates.

**Decision-ready insight:** A professional report gives the recipient enough information to reproduce safely, not enough information for an untrusted reader to exploit production.

## Synthesis: Process Quality Beats Technical Aggression

| Entity or strategy | Coordination mechanism | Scope | Main strength | Main trade-off | Evidence base | Time horizon |
|---|---|---|---|---|---|---|
| IIT Roorkee / JEE | Direct acknowledgment and public thanks | Education portal configuration | Positive researcher recognition and rapid priority fix [42] | Public disagreement over exposure scale [42] | Recipient statements plus journalism | Immediate |
| CBSE / CERT-In | Researcher-to-CERT-In-to-authority path | Examination-marking ecosystem | Eventual containment statement and request for official reports [46] | Researcher alleged long silence and incomplete follow-up [47] | Reporter account plus later recipient statement | Weeks to months |
| Zomato | Direct ethical disclosure | Consumer platform | Reported one-day fix and post-fix publication [43] | No evidence here of bounty or actual exploitation | Secondary journalism quoting company response | One day plus publication coordination |
| IRCTC / CERT-In | Neutral government coordinator | Third-party insurance portal linked to rail bookings | Report-to-fix confirmation in seven days [40] | Component ownership and source quality are less direct | Secondary case account | Seven days |
| Ola VDP | Pre-published first-party rules and scope | Named domains and mobile apps [49] | Reduces uncertainty before testing | Policy quality does not guarantee case handling | First-party program | Continuous |
| Project Zero | Fixed 90+30 deadline | Vendor vulnerabilities | Predictable and transparent timing [3] | Too rigid if copied without student-privacy and incident context | First-party policy | 90-120 days |
| Proposed MUJ model | Written authorization, named intake, staged testing, status cadence | SLCM and expressly named dependencies | Balances research value, legal safety, and student protection | Requires staff ownership and legal review | Analyst synthesis from cited models | Continuous with case-specific clocks |

Three non-obvious tensions emerge.

First, public praise is not safe harbor. IIT Roorkee applauded the researcher's conduct [42], but a future researcher still needs written authorization before testing. Positive reception after the fact should not be mistaken for permission before the fact.

Second, rapid remediation does not prove that no one else accessed data. Zomato's one-day fix [43] and the IRCTC case's seven-day confirmation [40] are operational successes, but only logs and incident investigation can address prior exploitation. **Inference:** The disclosure process and incident-response process must connect without forcing the student to become an investigator.

Third, a 90-day deadline can be both too long and too short. It is too long for active exploitation or live examination-integrity risk, where Project Zero itself substitutes seven days [3]. It may be too short for a complex replacement involving identity, CDN, vendor, and legacy application layers. The resolution is not to abandon deadlines, but to combine risk-based containment with transparent milestones.

The cases also expose an incentives divergence. Zomato's controlled post-fix publication gave recognition [43]; IIT Roorkee gave public praise [42]; CBSE's early generic acknowledgment allegedly failed to reassure the reporter [47]. **Inference:** Timely status communication and credit may produce more defensive value than a bounty alone.

**Holistic conclusion:** MUJ's best protection is not inviting uncontrolled student testing. It is converting curiosity into a governed pipeline: passive observation, written authorization, synthetic accounts, minimal validation, rapid acknowledgment, risk-based containment, coordinated retesting, evidence deletion, and agreed publication.

## VERDICT

**Verdict:** The university security club should proceed with a responsible-disclosure program design and passive OSINT study, but should **not** conduct active testing against `mujslcm.jaipur.manipal.edu` until MUJ issues written, asset-specific authorization and a safe test plan.

The public evidence establishes that SLCM handles attendance, marks, results, and student/parent academic functions [1], making privacy and integrity consequences potentially serious. Indian education-sector cases show both constructive acknowledgment and prolonged communication uncertainty [42][47]. Indian firm cases show that high-quality routing can produce remediation in one to seven days [43][40]. Sections 43 and 66 create meaningful compensation and criminal-risk considerations around access, copying, disruption, damage, and dishonest or fraudulent conduct [4].

**Confidence: High (0.88) on the recommended disclosure process, legal-risk boundaries at a general level, and the cited case timelines. Medium (0.65) on the MUJ-specific architecture because the detailed stack is user-supplied and was not independently verified. Low on whether MUJ currently has a private VDP or internal safe harbor, because no reliable public evidence was found.**

**Final action:** Ask MUJ for a signed authorization, a segregated environment, synthetic student and parent accounts, an emergency contact, and a written disclosure timeline. If MUJ cannot supply those controls, restrict the club project to policy design, public-document analysis, threat modeling, and secure report-writing exercises.

## References

1. *http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf*. http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf
2. *RVDCP*. http://cert-in.org.in/RVDCP.jsp
3. *Vulnerability Disclosure Policy - Project Zero*. https://projectzero.google/vulnerability-disclosure-policy.html
4. *http://indiacode.nic.in/bitstream/123456789/13116/1/it_act_2000_updated.pdf*. http://indiacode.nic.in/bitstream/123456789/13116/1/it_act_2000_updated.pdf
5. *is Amity Government or Private? - Rebellion Research*. https://www.rebellionresearch.com/is-amity-government-or-private
6. *Developer Go-to-market Signals Guide | Reo.Dev*. http://reo.dev/signals?domain=nitt.edu
7. *write-up/API Fuzzing for Bug Bounty The Complete ... - GitHub*. https://github.com/SecurityTalent/write-up/blob/main/API%20Fuzzing%20for%20Bug%20Bounty%20The%20Complete%20Attack%20Focused%20Methodology.md
8. *disclose/research-threats: Collection of legal ...*. https://github.com/disclose/research-threats
9. *responsible-disclosure*. https://github.com/topics/responsible-disclosure
10. *IDOR in the Wild: A Comprehensive Analysis of 250 Real-World ...*. https://www.thebughunter.blog/case-studies/idor-analysis
11. *Zomato*. http://eternal.com/our-businesses/zomato
12. *MSRC Researcher Portal*. https://msrc.microsoft.com/create-report
13. *Privacy Policy – Agent Studio & Slash | Razorpay*. http://razorpay.com/privacy-policy/agent-studio-slash
14. *What kind of exposure do students get at Amity University Bengaluru?*. https://www.quora.com/What-kind-of-exposure-do-students-get-at-Amity-University-Bengaluru-1
15. *IRCTC down: Thousands of users report issues while ... The Economic Times https://m.economictimes.com › News › Trending*. https://m.economictimes.com/news/new-updates/irctc-down-thousands-of-users-report-issues-while-booking-tickets-ahead-of-diwali/articleshow/124621455.cms
16. *Amity University – Leading Private University in India ...*. https://www.amity.edu/
17. *Vulnerability Hall of Fame - World Health Organization (WHO)*. https://www.who.int/about/cybersecurity/vulnerability-hall-of-fame
18. *Vulnerability Notes Database - CERT*. https://www.kb.cert.org/vuls
19. *Boeing crash due to design flaw leads to $ 150,000 redress ...*. http://www.uniindia.com/~/boeing-crash-due-to-design-flaw-leads-to-150-000-redress-demand-per-passenger-expert/States/news/3516787.html
20. *bug-bounty-writeup/src/idor.md at main · x1337loser ... - GitHub*. https://github.com/x1337loser/bug-bounty-writeup/blob/main/src/idor.md
21. *IDOR → Account Takeover — A Real Bug Chain ... - Medium*. https://medium.com/%40ghostyjoe/idor-account-takeover-a-real-bug-chain-walkthrough-7512a41d5a32
22. *Log4j Timeline of Events | Latest Log4j Vulnerabilities - Automox*. https://www.automox.com/blog/log4j-vulnerability-timeline
23. *Security bug in India's income tax portal exposed taxpayers ... Yahoo https://www.yahoo.com › news › articles › security-bug...*. https://www.yahoo.com/news/articles/security-bug-india-income-tax-143002294.html
24. *AI Security for Startups: Risks, Challenges & Best Practices in 2026*. http://rizevault.razorpay.com/p/ai-security-for-startups-risks-challenges
25. *Razorpay Agent Studio: Principles, Guardrails, and Merchant Control*. http://razorpay.com/blog/razorpay-agent-studio-principles-guardrails-and-merchant-control
26. [FortiBleed: 86,644 Fortinet Firewalls Exposed [2026]](https://shattered.io/fortibleed-fortinet-86644-firewalls-2026/)
27. *Alerts & Security Vulnerability Announcements - Ricoh USA*. https://www.ricoh-usa.com/en/support-and-download/alerts/alerts-security-vulnerability-announcements
28. *Hall of fame - Nokia.com*. https://www.nokia.com/we-are-nokia/security/products/cvd/hall-of-fame/
29. *Meet Rylen Anil: 16-Year-Old Cybersecurity Researcher Who ...*. https://www.newsx.com/education/meet-rylen-anil-16-year-old-cybersecurity-researcher-who-exposed-a-security-flaw-in-jee-advanced-2026-portal-230299/
30. *A path way to Global Studies|Global Exposure Amity University https://amity.edu › global-exposure*. https://amity.edu/global-exposure.aspx
31. *RHSA-2026:38750 - Security Advisory - Red Hat Customer Portal*. https://access.redhat.com/errata/RHSA-2026%3A38750
32. *Responsible Disclosure Hall of Fame - Schuberg Philis*. https://schubergphilis.com/security-hall-of-fame
33. *About Razorpay Security | Razorpay Docs*. http://razorpay.com/docs/security?preferred-country=US
34. *Security Vulnerability Disclosure Program Hall of Fame*. https://www.eff.org/security/hall-of-fame
35. *“Bug Bounty Bootcamp #34: IDOR Beyond GET — Modifying ...*. https://infosecwriteups.com/bug-bounty-bootcamp-34-idor-beyond-get-modifying-deleting-and-method-switching-for-maximum-159554377462
36. *Zomato hacked: Hackers steal data of 17 million users*. https://economictimes.indiatimes.com/small-biz/startups/zomato-hacked-hackers-steal-data-of-17-million-users/articleshow/58742044.cms
37. *Razorpay Agent Studio | AI Agents for Payments & Revenue Operations*. http://razorpay.com/agent-studio
38. *Amity University*. https://www.amity.edu/auup
39. *Zomato hacked! Are Indian online startups taking security for ...*. https://www.techinasia.com/zomato-hacked-indian-online-startups-security-granted
40. *IRCTC Fixes Critical Data Breach on Insurance Portal - CertPro*. https://certpro.com/irctc-data-breach
41. *Zomato hacked by white hat, who was nice enough to let them ...*. https://siliconangle.com/2015/06/10/zomato-hacked-by-white-hat-who-was-nice-enough-to-let-them-know/
42. *Meet the 16-year-old who spotted a JEE Advanced portal flaw ...*. https://www.firstpost.com/tech/meet-the-16-year-old-who-spotted-and-fixed-a-jee-advanced-portal-flaw-before-cybercriminals-could-ws-e-14019184.html
43. *Zomato hack: Security breach in its system not the first time ...*. https://www.thenewsminute.com/atom/zomato-hack-security-breach-its-system-not-first-time-user-information-was-compromised-62317
44. *Who Is Rylen Anil? 16-Year-Old Cybersecurity Researcher Who ...*. https://thelogicalindian.com/who-is-rylen-anil-16-year-old-cybersecurity-researcher-who-flagged-security-flaws-in-jee-advanced-portal/
45. *CVSS v4.0 Specification Document*. https://www.first.org/cvss/v4.0/specification-document
46. *CBSE Admits Flaws In OSM Portal After Hacker Flags Alleged Exposure*. https://www.ndtv.com/education/cbse-admits-vulnerabilities-after-ethical-hacker-flags-alleged-exposure-11571388
47. *CBSE OSM Portal Had Critical Vulnerabilities, Ethical Hacker Told NDTV He Alerted Board Months Earlier*. https://www.ndtv.com/education/cbse-osm-portal-had-critical-vulnerabilities-ethical-hacker-told-ndtv-he-alerted-board-months-earlier-11550090
48. *Vulnerability Disclosure Policy Template | CISA*. https://www.cisa.gov/vulnerability-disclosure-policy-template
49. *Ola Responsible Disclosure Program*. https://whitehat.olacabs.com/
50. *No. 20(3)/2022-CERT-In Government of India Ministry of Electronics and Information Technology (MeitY) Indian Computer Emergency Response Team (CERT-In) Electronics Niketan,*. https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf
51. *India Code: Section Details*. https://www.indiacode.nic.in/show-data?actid=AC_CEN_45_76_00001_200021_1517807324077&orderno=48&sectionId=13057&sectionno=43
52. *Recommendations for Federal Vulnerability Disclosure ...*. https://www.nist.gov/publications/recommendations-federal-vulnerability-disclosure-guidelines
53. *VulnerIncident - Indian Computer Emergency Response Team*. https://www.cert-in.org.in/VulnerIncident.jsp
54. *http://mujslcm.jaipur.manipal.edu/*. http://mujslcm.jaipur.manipal.edu/
