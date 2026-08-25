# Reporting MUJ SLCM Vulnerabilities Through CERT-In

## Executive Summary

- **Use Two Reporting Tracks**: CERT-In's Responsible Vulnerability Disclosure and Coordination Policy, or RVDCP, accepts security-vulnerability reports directly from finders, while the 2022 Directions separately require covered organizations to designate their own CERT-In Point of Contact, or PoC [16][8]. **Recommendation:** a university security club should notify MUJ's authorized IT/security administration and submit directly to CERT-In at `vdisclose@cert-in.org.in`. It should not wait for a publicly listed "nodal officer" when none can be found.

- **Do Not Confuse Three Different Clocks**: CERT-In promises to acknowledge vulnerability information within **72 working hours** [16]. Its coordination policy says it will endeavor to resolve an accepted matter within **120 days from initial vendor contact**, subject to substantial exceptions [16]. By contrast, the 2022 Directions impose a **six-hour incident-reporting deadline** on specified entities after they notice, or are informed of, an Annexure I cyber incident [8]. **Inference:** the six-hour clock does not turn every unexploited weakness into an incident; it becomes important when evidence indicates unauthorized access, leakage, compromise, malicious activity, or another listed incident actually occurred.

- **The CERT-In Researcher Route Is Email-Based**: CERT-In's RFC 2350 document identifies `vdisclose@cert-in.org.in` for vulnerability reporting [18]. RVDCP accepts PGP-encrypted email and attachments, provides a helpdesk and fax number, and links to a Vulnerability Reporting Form [16]. However, the linked PDF at `https://www.cert-in.org.in/PDF/certinvulnform.pdf` returned "requested URL is not found" during this research [19]. **Recommendation:** use the published email and RVDCP field list rather than treating the unavailable PDF as a blocker.

- **No Research Safe Harbour Is Promised**: RVDCP says the reporting party must follow applicable law, does not exempt a finder from legal compliance, and leaves the finder responsible for actions taken during discovery [16]. **Recommendation:** do not scan, exploit, bypass authentication, access another person's records, test availability, or expand impact on the production SLCM system without written authorization. Report only the minimum evidence already obtained lawfully.

- **MUJ Has Public Escalation Channels, But No Public Security PoC Was Found**: MUJ publishes `it.support@jaipur.manipal.edu` for IT Infrastructure and `registrar.office@jaipur.manipal.edu` for the Registrar Office [13]. Its Registrar page identifies Dr Amit Soni, `registrar@jaipur.manipal.edu`, and telephone `+91 141-3999100`, extension 102 [22]. Neither of the reviewed MUJ pages names a vulnerability-disclosure address or CERT-In PoC [22][13]. **Inference:** address the institutional copy to IT Infrastructure and the Registrar, expressly asking them to forward it to MUJ's authorized information-security, legal, and CERT-In PoC teams.

- **The PoC Is Not a Gatekeeper for Researchers**: The Directions say covered entities must designate a PoC to interface with CERT-In and submit that person's name, designation, organization, office address, email, mobile, office telephone, and fax [8]. RVDCP independently invites vulnerability reports from researchers, cybersecurity organizations, academic institutions, vendors, and other stakeholders [16]. **Inference:** a club should use MUJ's internal PoC if MUJ identifies one, but it does not need that officer's permission to make a good-faith direct report to CERT-In.

- **Route by Technical Ownership, Not by a Banner or Header**: Microsoft investigates vulnerabilities affecting Microsoft products and services, but warns that scanner findings are often false positives and that many findings are customer configuration issues rather than software vulnerabilities [7]. Akamai publishes `security@akamai.com` for potential vulnerabilities involving its ecosystem [9]. **Inference:** an MUJ application or configuration defect belongs first with MUJ; a demonstrable Microsoft product defect goes to MSRC; and an Akamai platform defect goes to Akamai. A technology fingerprint alone is not enough to assign responsibility.

- **Use the Correct Indian Public-Safety Channel**: NCRP and helpline 1930 are for cybercrime complaints, not ordinary coordinated vulnerability disclosure [24]. Sanchar Saathi's Chakshu accepts suspected fraudulent calls, SMS, or WhatsApp communications, but expressly says it is not the facility for reporting financial fraud or cybercrime cases [25]. **Recommendation:** keep a technical SLCM weakness in the MUJ/CERT-In RVDCP lane unless there is an actual victim, loss, criminal conduct, or fraudulent communication.

**Decision-ready insight:** The defensible default is **MUJ IT and Registrar plus CERT-In RVDCP in parallel**, with vendor reporting only when the defect is demonstrably vendor-owned. An active incident needs immediate institutional escalation because MUJ's responsible team, not the student club, must assess and satisfy any statutory six-hour duty.

## Scope, Evidence Standard, and Ethical Boundary

### What is assumed, and what is verified

The target description supplied with the request identifies `mujslcm.jaipur.manipal.edu` as an ASP.NET MVC 5.3 and .NET Framework 4.x application on IIS 10, behind Akamai, with Microsoft 365 identity. Those are **user-supplied observations, not independently verified findings in this report**. They must not be treated as proof of a vulnerability, product ownership, patch level, or exploitability.

| Item | Status in this report | What may safely be concluded | What must not be concluded |
|---|---|---|---|
| MUJ SLCM hostname | User-supplied scope identifier | It identifies the portal the club is discussing | It does not establish authorization to test |
| ASP.NET MVC, .NET Framework, IIS | User-supplied fingerprint | They suggest a Microsoft-origin software stack | They do not prove that a finding is a Microsoft product defect |
| Akamai | User-supplied fingerprint | Akamai may provide edge, delivery, or protection services | It does not prove that Akamai owns the origin application's behavior |
| Microsoft 365 identity | User-supplied architecture claim | Identity behavior may involve Microsoft and MUJ configuration | A tenant policy or integration mistake is not automatically an MSRC vulnerability |
| MUJ organizational status | Publicly verified at a limited level | MUJ describes itself as a self-financed State Private University launched in 2011 [21] | This report does not make a definitive legal finding that MUJ falls within every use of "body corporate" in the Directions |
| Public MUJ reporting contacts | Verified from MUJ pages | IT Infrastructure, Registrar Office, Registrar, and administrative contacts are published [22][13] | Their publication does not prove which employee is MUJ's confidential CERT-In PoC |

The distinction matters because a report can cause unnecessary risk if it assigns a custom application defect to Microsoft or Akamai, sends personal student records to unnecessary recipients, or asks a public-facing academic office to validate an exploit. CERT-In's own policy asks for an affected product, exact version or model, vendor, concise reproduction steps, supporting evidence, and impact [16]. That structure favors careful attribution over speculative fingerprinting.

### Ethical and legal boundary

RVDCP does not provide a broad safe harbour. It says the reporting party must comply with applicable laws and remains responsible for actions taken while discovering a vulnerability [16]. The club should therefore preserve only evidence already obtained through authorized use or an explicitly approved assessment. It should not access another student's account, retrieve records belonging to others, alter data, defeat access controls, conduct password attacks, test denial of service, upload active payloads, or continue after confirming a minimal issue.

A defensible evidence package can identify the affected URL or feature, the account role lawfully used, the observation time with time zone, the expected and observed behavior, the security impact stated conservatively, and redacted screenshots. It should omit cookies, bearer tokens, passwords, student identifiers, grades, financial information, or other personal data. If sensitive evidence is indispensable, RVDCP permits PGP-encrypted email and attachments [16].

### Auditable decision rationale

This report does not expose private chain-of-thought. Instead, the following table supplies a concise, reviewable evidence-to-decision rationale.

| Evidence | Governing distinction | Decision |
|---|---|---|
| A reproducible weakness exists but there is no evidence it was exploited | Vulnerability coordination under RVDCP [16] | Notify MUJ and `vdisclose@cert-in.org.in` |
| Unauthorized access, data leakage, malicious code, or another Annexure I event may have occurred | Cyber incident under the 2022 Directions [8] | Alert MUJ urgently; do not wait for routine vulnerability triage |
| The behavior is in custom SLCM code or MUJ tenant configuration | Operator-owned application or configuration issue; Microsoft says many scanner findings are configuration-related [7] | MUJ is the primary technical recipient |
| The defect reproduces in a Microsoft product or service independent of MUJ's tenant configuration | Vendor product vulnerability [7] | Submit a separate MSRC report and notify MUJ |
| The defect is in Akamai's platform rather than MUJ's origin | Akamai ecosystem issue [9] | Report to Akamai and notify MUJ |
| A person suffered fraud, loss, stalking, extortion, or another cybercrime | Victim/law-enforcement matter [24] | Use NCRP or 1930 in addition to institutional reporting |

**Decision-ready insight:** The architecture determines who may need a copy, but authorization and observed behavior determine what may be reported. Do not convert an OSINT fingerprint into an invitation to test.

## CERT-In's Three CONTACT Lanes

CERT-In's RFC 2350 description is the clearest public source for its operational contact categories. It describes CERT-In's constituency as Indian cyberspace and the Indian cyber community, including government, public-sector and private-sector organizations, individuals, and home users [18]. That breadth supports direct reporting by a student researcher, although an institutional club should still use formal university governance.

| CONTACT category | Published channel | Published purpose | Appropriate MUJ use | Do not use it for |
|---|---|---|---|---|
| Incident Response Help Desk | `incident@cert-in.org.in`; `+91-11-24368572`; toll-free `+91-1800-11-4949`; fax `+91-11-24368546` or `+91-1800-11-6969` [18] | Cybersecurity incident reports; the help desk operates 24x7 [18] | Evidence that compromise, unauthorized access, leakage, malicious activity, or another reportable event has occurred | A merely theoretical or unexploited weakness with no incident evidence |
| Vulnerability Reporting | `vdisclose@cert-in.org.in` [18] | Responsible disclosure and coordination of product security vulnerabilities under RVDCP [16] | A reproducible SLCM vulnerability needing MUJ/vendor coordination | General IT support, account recovery, or ordinary service complaints |
| Information Desk | `info@cert-in.org.in`, `advisory@cert-in.org.in`, and `subscribe@cert-in.org.in` [18] | Security alerts, technical questions, feedback, advisories, and subscriptions [18] | Clarification or non-case-specific questions | The primary submission of a time-sensitive incident or vulnerability |

The 2022 Directions independently publish `incident@cert-in.org.in`, telephone `1800-11-4949`, and fax `1800-11-6969` for mandatory Annexure I incident reports [8]. These channels overlap with the RFC 2350 incident lane, which reinforces that `incident@` and `vdisclose@` are not interchangeable labels.

**Inference:** If the club cannot determine whether observed facts indicate only a weakness or an actual compromise, it should notify MUJ immediately, describe the uncertainty explicitly, and avoid making an unsupported declaration that a breach occurred. CERT-In can receive the vulnerability at `vdisclose@`; MUJ's authorized incident team can decide whether the six-hour organizational duty has been triggered. If there is strong evidence of an ongoing incident, the report can also be sent to the 24x7 Incident Response Help Desk without delaying MUJ.

**Decision-ready insight:** Use `vdisclose@` for the weakness, `incident@` for an actual or strongly suspected incident, and the Information Desk for general questions. A report should state which lane it is invoking.

## RVDCP Mechanics: 72 Hours, 120 Days, and a Broken PDF

### What CERT-In asks the researcher to submit

RVDCP applies to security vulnerabilities in products and accepts encrypted email and attachments [16]. It also makes an important eligibility request: the vulnerability should reproduce on the latest available or supported version and should not already be known [16]. A club should preserve those qualifiers rather than claiming that an old, unsupported component automatically qualifies for coordination.

| RVDCP information element | Status in the policy | MUJ-safe implementation |
|---|---|---|
| Affected product or products | Requested [16] | Identify "MUJ SLCM" and the precise feature, without scanning unrelated hosts |
| Exact software version or model | Requested [16] | State only versions actually confirmed; label passive fingerprints as unverified |
| Vendor details | Requested [16] | Identify MUJ as operator; name Microsoft or Akamai only where ownership is supported |
| Vulnerability description | Requested [16] | Use a short neutral description, not promotional severity language |
| Concise reproduction steps | Requested [16] | Describe only an already authorized, minimum-impact observation; do not include secrets |
| Supporting evidence | Requested [16] | Use redacted screenshots, a sanitized request/response excerpt, or a non-sensitive demonstration |
| Security impact | Requested [16] | Distinguish demonstrated impact from hypothetical worst case |
| Other possibly affected products or versions | Preferred additional information [16] | Include only evidence-based scope; do not speculate broadly |
| Discovery method and tools | Preferred additional information [16] | State whether the observation arose during normal use, review, or an authorized exercise |
| Known exploitation | Preferred additional information [16] | Say "not observed" if that is all the evidence supports |
| Disclosure constraints | Preferred additional information [16] | State that the club will avoid publication while coordination is active |
| Prior or planned reports | Preferred additional information [16] | List MUJ, CERT-In, MSRC, or Akamai copies accurately |
| Anonymity and credit preference | Explicitly supported [16] | Decide in advance whether the student, club, or university may be named |

CERT-In says it will acknowledge receipt within **72 working hours** [16]. It then examines and validates the report and tells the discloser whether it will coordinate the case [16]. After validation, CERT-In may coordinate with the relevant vendor, the discloser, and other stakeholders for remediation and closure [16].

### Confidentiality and sharing

CERT-In says it will make all possible efforts to limit disclosure to the bare minimum, but it may share some or all information with trusted third parties when their assistance is needed [16]. That is a controlled-sharing commitment, not a promise that the report will remain exclusively between the finder and CERT-In. A reporter should therefore minimize personal data and state any handling constraints in the initial message.

RVDCP says CERT-In may publish a vulnerability note or advisory after remediation or at another appropriate time determined with stakeholders [16]. It may credit a researcher in the published note or advisory, and it can connect a vendor that wants to offer a reward with the discloser, but CERT-In does not participate in reward discussions [16]. The process should be approached as risk reduction and coordination, not as an assumed bounty program.

### Timeline expectations

| Stage | Published expectation | Important qualifier |
|---|---|---|
| Receipt | Acknowledgement within 72 working hours [16] | "Working hours" is not the same as 72 elapsed hours |
| Validation | CERT-In examines the report and states whether it will coordinate [16] | No separate fixed validation deadline is published in the extracted policy |
| Vendor coordination | CERT-In coordinates with relevant parties after successful validation [16] | The initial vendor-contact date may be later than the researcher's submission date |
| Target resolution | Endeavor to resolve within 120 days from initial vendor contact [16] | This is a target, not an unconditional deadline |
| Accelerated or changed timing | Timeline may change for active exploitation, multiple reports, exceptional seriousness, or stakeholder agreement [16] | Urgency is case-specific |
| Delay or non-cooperation | Coordination may exceed 120 days for disagreement, vendor non-response, or other circumstances [16] | No guaranteed maximum is stated |
| Closure or disclosure | CERT-In may close with notice to the discloser, or make the issue public and stop vendor coordination [16] | Public disclosure should not be unilaterally pre-empted by the club |

### The form-link problem

The RVDCP page links `/PDF/certinvulnform.pdf`, but the extracted URL returned CERT-In's "requested URL is not found" page [19]. This is a website-availability observation, not evidence that CERT-In has stopped accepting reports. The RVDCP page itself remains available, and RFC 2350 supplies `vdisclose@cert-in.org.in` [18].

**Recommendation:** send a structured email that follows the RVDCP fields. If the report contains sensitive material, use the PGP option described by RVDCP [16]. Ask for acknowledgement and a case reference. Do not send live credentials, reusable tokens, complete databases, or unnecessary personal information.

**Decision-ready insight:** The practical CERT-In "portal" for a researcher is the RVDCP page plus the vulnerability mailbox. The unavailable PDF is a documentation defect, not a reason to delay a responsible report.

## The 2022 Directions: Six Hours, PoC, and 180-Day Logs

CERT-In issued the Directions on 28 April 2022 under section 70B. The text applies its principal duties to service providers, intermediaries, data centres, bodies corporate, and government organizations [8]. It says non-compliance or failure to furnish information may invite punitive action under section 70B(7) and other applicable laws, and that the Directions become effective 60 days after issuance [8]. This report does not provide a definitive legal opinion on MUJ's classification; MUJ should have counsel or its compliance team confirm the precise basis of applicability.

### Core duties relevant to a university portal

| Duty | Exact operational rule | Relevance to MUJ SLCM | Club's role |
|---|---|---|---|
| Clock synchronization | Covered entities must synchronize ICT system clocks to specified or traceable time sources [8] | Reliable timestamps support incident reconstruction | Record the observation time and time zone; do not change systems |
| Incident notification | Annexure I incidents must be reported within six hours of noticing them or being informed of them [8] | A student report can put an organization on notice | Notify MUJ promptly and preserve the delivery record |
| Reporting channel | `incident@cert-in.org.in`, `1800-11-4949`, and `1800-11-6969` [8] | Gives MUJ's response team multiple urgent channels | Do not impersonate MUJ's authorized officer |
| Assistance to CERT-In | CERT-In may direct covered entities to act, supply information, or assist, including near-real-time information within a specified period [8] | MUJ may need logs and technical personnel available | Preserve original evidence and identify a club contact |
| Designated PoC | Covered entities must designate and update a PoC to interface with CERT-In [8] | MUJ's private PoC may not be published publicly | Ask the Registrar and IT Infrastructure to forward the report internally |
| PoC fields | Name, designation, organization, address, email, mobile, office phone, and fax [8] | Shows this is a formal organizational liaison record | Do not guess or publicly identify an employee as the PoC |
| Log retention | Covered entities must enable ICT logs, keep them securely for a rolling 180 days within Indian jurisdiction, and provide them with a report or when directed [8] | SLCM, identity, origin, edge, database, and administrative logs may be relevant | Do not ask the club to collect production logs; request that MUJ preserve them |

The six-hour requirement belongs to the covered organization. A student or club can supply the facts that bring an event to MUJ's attention, but the club is not automatically authorized to classify the event, represent MUJ to the Government, or disclose institutional logs. The report should make timing easy to determine by stating when the issue was first observed and when MUJ was informed.

### Annexure I categories most relevant to SLCM

| Incident category in the Directions | Example of the distinction, without testing guidance | Routing consequence |
|---|---|---|
| Compromise of critical systems or information | Evidence that an attacker obtained control or sensitive information, not merely that a control seems weak [8] | Urgent MUJ incident escalation |
| Unauthorized access to IT systems or data | Observed access outside the user's authorized role [8] | Stop immediately; preserve minimal evidence; alert MUJ |
| Website defacement or intrusion | Unauthorized changes, malicious code, or external links [8] | Incident lane, not ordinary web support |
| Malicious-code attack | Virus, worm, Trojan, bot, spyware, ransomware, or cryptomining activity [8] | Immediate containment by MUJ's authorized team |
| Server or network-device attack | Attack involving database, mail, DNS, routers, or similar infrastructure [8] | MUJ incident team plus relevant service provider |
| Identity theft, spoofing, or phishing | Misuse of identities or deceptive login communications [8] | MUJ identity team; possibly NCRP for victims |
| DoS or DDoS | Availability attack [8] | Incident reporting and provider coordination; never test availability |
| Application attack | Attack against an application such as an e-governance or e-commerce service [8] | Relevant analogy for an institutional portal |
| Data breach or data leak | Exposure or unauthorized release of protected data [8] | Urgent incident and privacy/legal review |
| Cloud malicious activity | Malicious or suspicious activity affecting cloud systems, servers, software, or applications [8] | MUJ plus the affected cloud provider |

**Inference:** a vulnerability is a weakness; an incident is an event. A missing authorization check reported without accessing another person's record can remain a vulnerability report. Evidence that another person's records were actually accessed, exposed, altered, or exfiltrated raises the incident question. The finder should not generate more exposure merely to prove that distinction.

### Does the club have to go through the nodal officer?

No public language reviewed here says that an external finder must route RVDCP submissions through the affected entity's PoC. The Directions place the PoC duty on the organization [8], while RVDCP directly welcomes collaboration with researchers and academic institutions [16].

**Inference:** the best governance path is not "nodal officer or CERT-In." It is **both institutional notice and direct CERT-In vulnerability reporting**, unless MUJ gives the club a documented internal procedure that achieves the same prompt escalation. If MUJ identifies its authorized security or CERT-In PoC, that person should replace the Registrar as the institutional recipient. Until then, the public IT and Registrar channels are defensible forwarding points.

**Decision-ready insight:** The PoC provision strengthens MUJ's internal responsibility; it does not remove the researcher's direct RVDCP route.

## MUJ Reporting Playbook: Operator First, CERT-In Direct, Vendors Conditionally

### Recipient order

| Priority | Recipient | Published channel | When to include | Why |
|---|---|---|---|---|
| 1 | MUJ IT Infrastructure | `it.support@jaipur.manipal.edu`; extensions 778 and 300 through the main number [13] | Every SLCM application, identity-integration, or configuration report | It is the published technical escalation point |
| 2 | MUJ Registrar | `registrar@jaipur.manipal.edu`; `+91 141-3999100`, extension 102 [22] | Every material report where no security address is public | The Registrar is a documented senior institutional office |
| 3 | MUJ Registrar Office | `registrar.office@jaipur.manipal.edu`; extensions 134 and 225 [13] | Administrative tracking or when the named Registrar address does not acknowledge | It creates an office-level delivery record |
| 4 | MUJ administration | `admin.office@jaipur.manipal.edu`; extensions 119 and 105 [13] | Operationally serious or unacknowledged matters | It is a published administrative fallback |
| 5 | CERT-In Vulnerability Reporting | `vdisclose@cert-in.org.in` [18] | Reproducible security vulnerabilities suitable for coordination | It invokes RVDCP directly |
| 6 | CERT-In Incident Help Desk | `incident@cert-in.org.in`, telephone and fax channels [8] | Actual or strongly suspected Annexure I incidents | It is the 24x7 incident lane |
| 7 | Microsoft MSRC | `https://msrc.microsoft.com/create-report` [7] | A demonstrable Microsoft product/service vulnerability | MSRC investigates Microsoft products and services [7] |
| 8 | Akamai security | `security@akamai.com` [9] | A demonstrable Akamai ecosystem vulnerability | Akamai publishes this as its security channel |

The reviewed MUJ pages do not name a vulnerability-disclosure mailbox or CERT-In PoC [22][13]. That is a bounded finding about those public pages, not proof that MUJ lacks an internal security team. The first message should ask IT and the Registrar to assign an authorized security owner and provide a secure follow-up channel.

### Formal workflow

| Step | Club action | Safety and governance control | Expected output |
|---|---|---|---|
| 1. Stop | End any interaction once the minimum authorized observation is established | Do not broaden scope, access other accounts, alter records, or test availability | No additional user or system impact |
| 2. Classify provisionally | Mark the matter "potential vulnerability," "suspected incident," or "uncertain" | Label inference; do not claim a breach without evidence | A conservative routing decision |
| 3. Sanitize evidence | Remove cookies, tokens, credentials, personal data, grades, payment details, and unrelated records | Keep an unmodified private original only where lawful and necessary | A shareable evidence set |
| 4. Record provenance | Note date, time zone, authorized account role, feature, expected behavior, and observed behavior | State that the architecture fingerprint is user-supplied or passively observed | An auditable chronology |
| 5. Notify MUJ | Send to IT Infrastructure and the Registrar; request forwarding to information security, legal, privacy, and MUJ's CERT-In PoC | Use a neutral subject; do not include exploit code in the first unencrypted email | Institutional notice and delivery timestamp |
| 6. Notify CERT-In | Send the structured report to `vdisclose@cert-in.org.in` [18] | Follow RVDCP fields; use PGP where sensitive [16] | CERT-In case intake |
| 7. Escalate an incident | If facts indicate an Annexure I event, alert MUJ urgently and use the CERT-In incident lane as appropriate [8] | Do not speak on MUJ's behalf unless authorized | Rapid incident assessment |
| 8. Notify a vendor conditionally | Submit separately to MSRC or Akamai only when evidence supports vendor ownership [7][9] | Avoid sending MUJ-specific secrets to a vendor unnecessarily | Parallel product-level triage |
| 9. Track | Request acknowledgement, case identifier, owner, and secure follow-up route | CERT-In's published acknowledgement target is 72 working hours [16] | Documented chain of custody |
| 10. Coordinate | Answer narrowly scoped questions and let authorized teams perform production validation | Do not resume testing without written authorization | Remediation without expanded risk |
| 11. Close | Ask for confirmation of remediation and permission before any retest or publication | CERT-In coordinates disclosure timing with stakeholders [16] | Controlled closure |

### Suggested report envelope

The following is a reporting template, not an instruction to conduct testing.

| Field | Suggested content |
|---|---|
| Subject | `Responsible disclosure: potential vulnerability in MUJ SLCM - confidential` |
| To | `it.support@jaipur.manipal.edu`; `registrar@jaipur.manipal.edu`; `vdisclose@cert-in.org.in` |
| Administrative fallback | `registrar.office@jaipur.manipal.edu` |
| Classification | `Potential vulnerability`, `Suspected incident`, or `Uncertain - please assess urgently` |
| Affected asset | `mujslcm.jaipur.manipal.edu`, plus only the relevant feature |
| Discovery context | Normal authorized use, code review, or a specifically authorized exercise |
| Observation | Expected behavior versus observed behavior, stated without unnecessary exploit detail |
| Impact | Demonstrated impact first; hypothetical impact separately labeled as inference |
| Evidence | Redacted screenshots or sanitized excerpts; no reusable secrets or unrelated personal data |
| Timing | First observation time, time zone, cessation time, and institutional-notification time |
| Prior disclosure | Identify every recipient and case number |
| Request | Acknowledge receipt, assign an authorized owner, preserve relevant logs, provide a secure channel, and coordinate remediation |
| Researcher preference | Name/club attribution, anonymity, or no public credit, as RVDCP permits [16] |

A sample opening paragraph could read:

> We are reporting a potential security vulnerability observed during authorized use of MUJ SLCM. We stopped after the minimum observation and did not access other users' records, alter data, or test service availability. The attached evidence is redacted. Please forward this report to MUJ's authorized information-security, legal/privacy, and CERT-In Point of Contact teams, acknowledge receipt, preserve relevant logs, and provide a secure channel for follow-up. Any impact not directly demonstrated is labeled as inference.

This wording does not claim legal immunity, authorization beyond what exists, or a confirmed breach. It also gives MUJ the timestamps needed to assess whether the six-hour incident clock applies.

### Follow-up and publication

CERT-In's acknowledgement target is 72 working hours [16], but no comparable MUJ public acknowledgement SLA was found on the reviewed pages. **Recommendation:** if MUJ does not acknowledge promptly, resend through the Registrar Office and administration while maintaining the CERT-In case. For urgent incident evidence, use telephone escalation rather than waiting for ordinary email.

Do not publish the vulnerability, proof of concept, affected records, or identifying screenshots while coordination is active. RVDCP gives CERT-In flexibility to coordinate publication after remediation or at another appropriate time and recognizes that the 120-day target can change [16]. The club should seek written agreement before retesting or presenting the case publicly.

**Decision-ready insight:** The report should create two traceable records: one proving that MUJ was informed, and one placing the vulnerability into CERT-In's RVDCP process.

## Four SLCM Decision Cases

These are **hypothetical routing cases, not allegations that any MUJ vulnerability exists**.

### Case 1: A custom SLCM authorization weakness

A student notices during normal authorized use that an SLCM feature appears to return information beyond the student's own role. The student stops without changing identifiers, opening another person's record, or expanding the observation. The club documents only the authorized context and the non-sensitive indication that a boundary may be missing.

**Mechanism:** the behavior appears in MUJ's application authorization logic, even though the site uses Microsoft technologies and Akamai. Microsoft cautions that many findings are configuration-related rather than software vulnerabilities [7]. **Inference:** MUJ is the primary owner. The club should notify MUJ IT and the Registrar and send the sanitized report to CERT-In's vulnerability channel. It should not file with MSRC or Akamai merely because their technology appears in the architecture.

### Case 2: A reproducible Microsoft product defect

During a university-authorized assessment, the same security behavior reproduces in a supported Microsoft product independent of MUJ's custom code or tenant policy. The report can identify the product, version, updates, configuration, minimal reproduction, and impact without exposing student data. MSRC asks for those categories of information and requires individual vulnerability reports to be submitted separately [7].

**Mechanism:** the defect follows the vendor product rather than MUJ's implementation. **Inference:** submit to the MSRC Researcher Portal and notify MUJ because its deployment may be affected. MSRC generally confirms receipt within one business day [7]. CERT-In RVDCP can remain involved where Indian coordination is useful. This is a three-party coordination case, not a reason to exclude the operator.

### Case 3: An Akamai platform issue

A university-authorized review finds that the issue belongs to Akamai's platform or service behavior, rather than MUJ's origin application. Akamai publishes `security@akamai.com`, supports encrypted communication, and subjects participating research to its Security Research Agreement [9].

**Mechanism:** edge and origin ownership are separate. **Inference:** report the Akamai-specific defect to Akamai, notify MUJ of exposure to its service, and avoid giving Akamai unrelated SLCM records or credentials. If the behavior exists only because MUJ configured an edge rule incorrectly, MUJ remains the primary owner.

### Case 4: Evidence of active compromise or data leakage

A club member receives credible evidence that SLCM data has already been accessed or disclosed without authorization. The member does not download more records to prove scope. Unauthorized access, data breach, data leak, application attacks, and malicious cloud activity are listed incident categories [8].

**Mechanism:** the situation is no longer only about a latent weakness; it may be an event requiring containment, log preservation, legal review, and regulatory reporting. **Inference:** call MUJ's published main number and contact IT/Registrar urgently, send the factual chronology, and use CERT-In's incident channel where appropriate. The organization must determine its six-hour duty from when it noticed or was informed of the incident [8]. If an individual is a victim of cybercrime or financial loss, NCRP or 1930 is an additional route [24].

**Decision-ready insight:** Ownership follows the defect; urgency follows the observed event. Neither should be inferred solely from a server header.

## Synthesis: Vulnerability, Incident, Vendor, Crime, and Spam Routes

| Route | Trigger | Primary actor | Time expectation | Evidence scope | Main trade-off |
|---|---|---|---|---|---|
| MUJ internal disclosure | Any credible SLCM weakness or suspected incident | MUJ IT/security, Registrar, legal/privacy | No public MUJ SLA found on reviewed pages | Minimal, redacted, institution-specific | Fast operator awareness, but no public VDP process was found |
| CERT-In RVDCP | Reproducible product security vulnerability | Finder, CERT-In, vendor/operator | 72 working-hour acknowledgement; 120-day target from vendor contact with exceptions [16] | Product, version, vendor, reproduction, evidence, impact [16] | National coordination, but no legal safe harbour [16] |
| CERT-In incident response | Actual or strongly suspected Annexure I incident | Covered entity and CERT-In | Six hours from notice for covered entities [8] | Incident facts and later requested information | Urgent legal clock; should not be used to overstate a bare weakness |
| MUJ CERT-In PoC | Organizational liaison required by the Directions | MUJ's designated representative | Must be maintained and updated [8] | Formal identity and contact fields [8] | Efficient official communication, but the identity may be non-public |
| Microsoft MSRC | Microsoft product/service vulnerability | Researcher and Microsoft | Generally one business day for receipt confirmation [7] | One vulnerability per report with product-specific details [7] | Strong vendor expertise, but configuration issues may be out of the product-vulnerability lane [7] |
| Akamai security | Akamai ecosystem vulnerability | Researcher and Akamai | No response SLA was found in the extracted page | Akamai-specific information, optionally encrypted [9] | Correct for edge-platform defects, not MUJ origin defects |
| NCRP or 1930 | Actual cybercrime, victimization, or financial fraud | Victim and law enforcement | Emergency-driven, not a vulnerability-remediation SLA | Complaint and loss details | Law-enforcement route, not coordinated technical disclosure [24] |
| Chakshu | Suspected fraudulent communication through call, SMS, or WhatsApp | Telecom user and DoT ecosystem | Not a vulnerability SLA | Communication details | Expressly not the facility for financial fraud or cybercrime cases [25] |
| TRAI UCC complaint | Unsolicited commercial communication or spam | Subscriber and telecom service provider | A complaint within three days; later submissions are treated as reports [26] | Sender and communication details | Telecom-spam enforcement, unrelated to an SLCM software flaw |

Three non-obvious tensions emerge.

First, **direct reporting and institutional governance are complementary rather than competing**. RVDCP invites researchers and academic institutions [16], while the Directions require the organization to maintain a PoC [8]. The researcher can initiate coordination directly; MUJ must still own operational remediation and any incident duty.

Second, **the six-hour and 120-day numbers govern different objects**. Six hours concerns organizational notice of specified incidents [8]. The 120-day target concerns coordinated resolution after CERT-In contacts the vendor [16]. Applying six hours to every vulnerability creates false urgency; applying 120 days to active compromise creates dangerous delay.

Third, **vendor presence is not vendor ownership**. Microsoft explicitly distinguishes product vulnerabilities from configuration-related findings [7]. Akamai's channel concerns its security ecosystem [9]. A layered architecture therefore requires layered attribution: MUJ owns its application and tenant decisions, while vendors own defects intrinsic to their products or platforms.

A further institutional boundary is important. A separate information-security policy found on `manipal.edu` expressly concerns MAHE information assets and MAHE's security program [5]. MUJ publicly describes itself separately as a self-financed State Private University [21]. **Inference:** the MAHE policy must not be presented as MUJ's disclosure policy unless MUJ confirms that it applies. Doing so would create false assurance about authorization, scope, or reporting channels.

**Decision-ready insight:** The most resilient strategy uses parallel but bounded lanes: MUJ for ownership, CERT-In for national coordination, the vendor only for a vendor defect, and law-enforcement or telecom channels only for the harms they were designed to address.

## VERDICT

**Verdict:** A university security club should **not wait exclusively for a MUJ nodal officer**, and it should **not bypass MUJ by reporting only to CERT-In**. The recommended formal path is:

1. Stop at the minimum lawfully obtained evidence.
2. Send a confidential institutional notice to `it.support@jaipur.manipal.edu` and `registrar@jaipur.manipal.edu`, with `registrar.office@jaipur.manipal.edu` as an administrative fallback [22][13].
3. Ask MUJ to assign its authorized information-security owner and forward the case to its legal/privacy and CERT-In PoC functions.
4. Submit the same sanitized vulnerability report directly to `vdisclose@cert-in.org.in` under RVDCP [18][16].
5. If evidence indicates an actual Annexure I incident, alert MUJ urgently and use CERT-In's 24x7 incident lane as appropriate; the covered organization's deadline is six hours from notice [8][18].
6. Add MSRC or Akamai only when evidence shows that the flaw belongs to their product or platform [7][9].
7. Do not retest, publish, or seek additional affected data without written authorization and coordinated approval.

The 2022 PoC is best understood as MUJ's official interface with CERT-In, not as a prerequisite that blocks direct researcher access to RVDCP. That conclusion is an **inference from the coexistence of the organizational PoC duty and CERT-In's open researcher-reporting policy** [8][16].

**Confidence: High, with two bounded caveats.** Confidence is high on CERT-In channels, RVDCP fields, the 72-working-hour acknowledgement, the qualified 120-day target, the six-hour incident rule, PoC duty, and 180-day log rule because they come from CERT-In primary sources [16][8]. Confidence is moderate on the precise internal MUJ routing because no public MUJ vulnerability-disclosure policy or CERT-In PoC was found on the reviewed official pages; the Registrar and IT Infrastructure are therefore documented escalation points, not confirmed members of MUJ's security team [22][13]. The linked CERT-In form PDF was unavailable, so email under RVDCP is the reliable public submission mechanism found in this research [19][18].

## References

1. *Cert-In - Home Page*. https://www.cert-in.org.in/SecurityIncident.jsp
2. *Indian - Computer Emergency Response Team*. https://www.cert-in.org.in/
3. *Cert-In - Directions70B*. https://www.cert-in.org.in/Directions70B.jsp
4. *Mandatory Disclosures & Reports - Manipal University Jaipur *. https://www.jaipur.manipal.edu/mandatory-disclosure.php
5. *Information Security Policy*. https://www.manipal.edu/mu/policies/it-policy/information-security-policy.html
6. *MSRC Researcher Portal*. https://msrc.microsoft.com/report/vulnerability
7. *FAQs - Report an issue and submission guidelines*. https://www.microsoft.com/en-us/msrc/faqs-report-an-issue
8. *No. 20(3)/2022-CERT-In Government of India Ministry of Electronics and Information Technology (MeitY) Indian Computer Emergency Response Team (CERT-In) Electronics Niketan,*. https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf
9. *Akamai Vulnerability Reporting | Akamai*. https://www.akamai.com/global-services/support/vulnerability-reporting
10. *Cert-In - Home Page*. http://cert-in.org.in/s2cMainServlet?pageid=WHATWELIST
11. *Indian - Computer Emergency Response Team*. http://cert-in.org.in/PDF/FAQs_on_CyberSecurityDirections_May2022.pdf
12. *Indian - Computer Emergency Response Team*. http://cert-in.org.in/s2cMainServlet?pageid=CONTACTUS
13. *Contact Us - Manipal University Jaipur *. http://jaipur.manipal.edu/contact-university.php
14. *Manipal University Jaipur - 71 years of legacy of Manipal Education*. https://jaipur.manipal.edu/
15. *cert-in.org.in*. https://www.cert-in.org.in/s2cMainServlet?pageid=PUBWEL01
16. *RVDCP*. https://cert-in.org.in/RVDCP.jsp
17. *Cert-In - Home Page*. https://www.cert-in.org.in/PDF/CERT-In_RVDCP_Poster.pdf
18. *The Indian Computer Emergency Response Team (CERT-In) Ministry of Electronics and Information Technology Government of India RFC 2350 v1.0 1.*. https://www.cert-in.org.in/PDF/RFC2350.pdf
19. *Cert-In - Home Page*. https://www.cert-in.org.in/PDF/certinvulnform.pdf
20. *Recognition & Accreditations - Manipal University Jaipur *. http://jaipur.manipal.edu/recognition-accrediation.php
21. *About MUJ - Manipal University Jaipur*. http://jaipur.manipal.edu/about-muj.php
22. *Registrar - Manipal University Jaipur*. https://www.jaipur.manipal.edu/administration-registrar.php
23. *India Code: Section Details*. https://www.indiacode.nic.in/show-data?actid=AC_CEN_45_76_00001_200021_1517807324077&sectionId=13102&sectionno=70B&orderno=93
24. *http://i4c.mha.gov.in/ncrp.aspx*. http://i4c.mha.gov.in/ncrp.aspx
25. *http://sancharsaathi.gov.in/*. http://sancharsaathi.gov.in/
26. *http://trai.gov.in/complain-or-report-against-ucc*. http://trai.gov.in/complain-or-report-against-ucc
