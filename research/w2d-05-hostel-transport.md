# MUJ SLCM Hostel and Transport Artifacts: Public Exposure and Privacy Risk

## Executive Summary

- **Public Surface**: The unauthenticated MUJ SLCM page exposes branding and sign-in choices, including student and parent login labels, but the research did not access authenticated functions or claim a vulnerability. [3] -> Keep all hostel and transport records behind authenticated, role-based views.
- **Hostel Allocation Rule**: MUJ's official hostel page says allotment follows fee payment on a first-come-first-served basis, while a room may be changed only in exceptional circumstances with prior Chief Warden permission. [2] -> Publish the process and appeal route without publishing resident identities.
- **Room Assignment Data**: MUJ publicly describes double-seater rooms, beds, wardrobes, study furniture and storage, while its overview describes separate boys' and girls' blocks, more than 10,000 beds and flap-barrier access control. [13] [4] -> Treat room number, block, occupant and access records as sensitive combinations even where individual fields seem harmless.
- **Public Allotment Lists**: Repeated searches located no MUJ-specific public allotment list containing student names and register numbers. Returned list results were unrelated institutions and were excluded. This is a bounded search finding, not proof that no list exists behind login, in a non-indexed location, or in a private communication channel. -> Verify internally through authorized records review, not further enumeration.
- **Room Changes**: The public material supplies the decision threshold but not a complete workflow, form, service-level target, evidence standard or appeal mechanism. [2] -> Create a documented request workflow with least-privilege case access and auditable approval.
- **Transport Evidence Gap**: The official contact page gives campus location and intercity access information, including Jaipur bus-stand, railway-station and airport distances, but the targeted public corpus contains no MUJ student shuttle route, stop, timetable or transport-allotment roster. [18] -> Give route assignments to eligible students and parents through authenticated, minimum-necessary views.
- **Privacy Exposure**: Under the DPDP Act, personal data includes information about an identifiable individual, and processing includes making data available, dissemination and disclosure. [8] -> A PDF containing a name, register number, room and route should be treated as personal-data processing, not as a neutral notice.
- **Security Baseline**: CERT-In Directions require covered entities to report listed cyber incidents within six hours and maintain ICT logs securely for a rolling 180 days in India. [10] -> Preserve access, download and publication logs and maintain an incident playbook.
- **Recommended Publication Model**: Use individual portal views, expiring links, pseudonymous reference codes and aggregated vacancy statistics. -> Avoid public combinations of full name, register number, room, block, route, stop and timing.

## Scope, Method and Evidence Discipline

This report addresses only public information retrieved from MUJ, MAHE, MeitY, CERT-In, OWASP and clearly labeled comparative sources. It does not attempt login, password recovery, directory enumeration, parameter tampering, file discovery through unauthorized means, exploitation, scraping of personal records, or access to any student account. The SLCM page was assessed only as an unauthenticated landing surface. Its visible text identifies a MUJ portal and sign-in choices, including parent login; it does not establish what authenticated users can see. [3]

The requested technology description names ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai and Microsoft 365 identity. The public material reviewed here does not independently verify those exact versions or the claimed edge architecture. Raw page markup exposes framework-style paths and student/faculty email-domain handling, but those observations are not proof of version, patch level, hosting topology, origin exposure or a security defect. This distinction matters: a technology fingerprint can be stale, deliberately altered, inherited from a theme, or produced by a reverse proxy. Any stack statement in the input should therefore be treated as an investigation lead, not as a report conclusion.

The search strategy used separate objectives for hostel lists, room-change procedures, transport routes, SLCM public content, university privacy policy, Indian data-protection law and defensive application-security guidance. The same approach returned unrelated hostel lists from other institutions. Those results were not treated as evidence about MUJ. The absence of a MUJ-specific indexed PDF is reported only as an evidence gap. It cannot establish that a document is absent from authenticated SLCM, a campus noticeboard, an unindexed URL, a messaging group, or a time-limited link.

The report uses three evidence labels. "Observed" means directly stated by an identified source. "Not located" means repeated public searches did not produce the requested MUJ artifact. "Inference" means an analytical conclusion drawn from the observed facts and is labeled as such. This is the appropriate level of certainty for a university security-club study: useful enough to guide defensive review, but not overstated as proof of exposure.

## What the Public MUJ Material Establishes

MUJ's official hostel page states that separate hostels for boys and girls are available on campus, with separate entry and adequate security, and that twin-sharing AC rooms are provided. [2] The same official page describes hostel allotment as occurring after fees are deposited on a first-come-first-served basis. It says a room can be changed only under exceptional circumstances and with prior permission of the Chief Warden. [2] These are operational rules, not evidence that the corresponding records are publicly downloadable.

The official room page identifies double-seater rooms and lists beds, wardrobes, common wardrobes, study tables with chairs, overhead shelves and universal sockets near study tables and beds. [13] This description is useful for understanding what an allotment artifact might contain, but it does not publish a resident roster. It also creates an important privacy consideration: a room number is not merely a furniture label once connected to a named student or a small group of occupants.

The official hostel overview states that MUJ has separate boys' and girls' hostel blocks and more than 10,000 student beds. [4] It also mentions lifts, staircases and corridors in boys' blocks and flap-barrier-enabled access control. [4] The Chief Warden page describes 24-hour security, 24-hour medical facility, Wi-Fi, power, water, rooms, mess and gym facilities. [17] These statements show that accommodation records sit within a broader safety and access-control environment. They do not show whether access-control data is integrated with SLCM, nor whether any particular API or database is exposed.

MUJ's official hostel fee page provides an additional allocation lifecycle. For academic year 2026-27, it lists double-occupancy hostel accommodation at INR 167,372, housekeeping at INR 15,378, a refundable security deposit of INR 25,475 and a total including that deposit of INR 208,225. [14] It says room allotment is confirmed only after successful receipt and verification of full hostel fees. [14] It also states that non-payment by specified dates results in immediate forfeiture of the room and fees already paid. [14]

The page lists optional laundry and health-club charges, payment by UPI, internet banking and card, and possible payment-gateway convenience charges borne by the student. [14] It says hostel fees are strictly non-refundable after the academic year commences, while an eligible pre-commencement refund is reduced by a INR 5,000 administrative processing fee. [14] These details are not needed in a public allotment list. A privacy-preserving notice should publish only what a student needs to complete payment and should not disclose who paid, who did not pay, or who lost an allocation.

The mess page lists 2026-27 mess charges of INR 79,000 and says the fee may be revised during the academic session because of operational and cost factors, with advance communication through an official notice. [15] It states that a selected mess is allotted for a fixed two-month period after which residents may switch. [15] A mess assignment can become sensitive when combined with a room, route or attendance pattern. That is an inference from the linkage of records, not a claim that MUJ publicly exposes such a combination.

## Allotment Lists and PDF Exposure: Findings and Safe Interpretation

The requested artifact is a list that may include a student's full name, register number, room number, hostel block, course or batch, and sometimes a route or stop. In a typical operational document, each field has a legitimate administrative purpose. The problem is the join: a full name plus register number identifies a student; a room and block reveal residence; a route and stop can reveal recurring movement. A public PDF can also be copied, indexed, cached, forwarded and retained after the assignment changes.

| Artifact or field | Public MUJ evidence found | Privacy significance | Recommended defensive treatment |
|---|---|---|---|
| Hostel allotment rule | Official MUJ page states fee payment and first-come-first-served allotment. [2] | Reveals process, but not individual identity. | Safe for public policy documentation. |
| Full student name | No MUJ-specific public allotment list was located in the returned corpus. | Directly identifies a resident. | Do not publish in a bulk roster. |
| Register number | No MUJ-specific public allotment list was located in the returned corpus. | Persistent identifier that can enable cross-linking. | Show only to the authenticated student, or use a short-lived reference. |
| Room or block | MUJ publicly describes room types and hostel blocks, not resident assignments. [13] [4] | Reveals residence when joined to a person. | Individual portal view; aggregate vacancies publicly. |
| Route, stop and time | No MUJ student route roster was located. | Can reveal routine location and movement. | Authenticated student/parent view; avoid public bulk files. |
| Fees and payment status | MUJ publishes fee categories and payment conditions. [14] | Payment status can reveal financial circumstances. | Publish fee policy, never payer or defaulter lists. |
| Versioned PDF URL | No MUJ-specific public allotment PDF was located. | URLs can be forwarded and indexed. | Expiring, access-controlled documents with revocation. |

The absence finding deserves special care. Searches returned a non-MUJ hostel allotment document with student names and roll numbers, but the institution was not MUJ, so it was excluded from the evidence base. The search also returned MUJ hostel facility, overview and fee pages, not a resident list. This supports the narrow conclusion that no MUJ-specific list was located through the public search corpus used here. It does not support the stronger conclusion that MUJ has never published one.

**Inference:** If MUJ were to publish a list containing names, register numbers and rooms, the combined record would carry materially greater privacy risk than an aggregate notice such as "Block B has 120 vacant beds." The inference follows from the Act's definition of personal data and processing, which includes collection, storage, sharing, disclosure, dissemination and making data available. [8] It is not a legal finding about a particular MUJ document, because no such document was located.

A security club should not collect examples containing real student PII for a presentation. Use a synthetic table with fake identifiers, blur screenshots, preserve only URL metadata and publication dates, and report the data schema rather than the values. If an actual public document is discovered by an authorized reviewer, notify the institution through its security or privacy contact and do not redistribute it.

## Room Changes: What Is Known and What Is Missing

The official MUJ rule has two parts. First, allotment is tied to fee payment and a first-come-first-served process. Second, post-allotment change is restricted to exceptional circumstances and requires prior Chief Warden permission. [2] The hostel FAQ adds that rooms are vacated annually for maintenance, that existing students may sometimes receive the same room, and that room outcomes depend on availability. [16] It also says luggage help may be available on hostel allocation day on request. [16]

The public pages do not state what counts as exceptional, whether a medical or accessibility reason is handled differently, which office receives the request, what evidence is required, how long a decision takes, whether both roommates must consent, how a room inventory is updated, or whether a refused request can be appealed. Those are unanswered process questions, not defects. The correct research conclusion is that the public procedure is incomplete, not that the institution has no procedure.

| Room-change control point | Publicly stated MUJ position | Unanswered operational question | Defensive design recommendation |
|---|---|---|---|
| Initial allocation | First-cum-first basis after fee payment. [16] | How is ordering recorded and audited? | Immutable allocation event and staff audit trail. |
| Eligibility to change | Exceptional circumstances and Chief Warden permission. [2] | What is the definition and evidence standard? | Published criteria and privacy-limited evidence access. |
| Availability | FAQ answers indicate availability-based outcomes. [16] | Who sees live inventory and when? | Role-based inventory; no public resident map. |
| Annual turnover | Rooms are vacated annually for maintenance. [16] | When are old assignments retired? | Retention schedule and automatic closure of stale links. |
| Appeal | Not located in public material. | Is there an independent review route? | Documented appeal owner, deadline and audit record. |
| Notification | Allocation-day luggage support is mentioned. [16] | How are approvals and denials delivered? | Authenticated notification, no sensitive email subject lines. |

**Recommendation:** The minimum viable room-change workflow should accept a request, classify it, restrict attachments to authorized housing staff, obtain Chief Warden approval, update the authoritative room record, notify affected occupants privately, and retain an audit event without exposing the underlying medical or personal narrative. This recommendation is based on least privilege and data minimization principles; it is not a claim about MUJ's current implementation.

## Transport Routes and Allotment Artifacts

The public transport evidence is narrower than the hostel evidence. MUJ's official contact page identifies the campus at Dehmi Kalan, off the Jaipur-Ajmer Expressway, Jaipur, Rajasthan 303007. [18] It describes Rajasthan State Road Transport Corporation bus services between Jaipur and Delhi at approximately half-hour intervals in both directions. [18] It says a bus journey typically takes six hours by Volvo or six to seven hours by other deluxe buses, and places the Jaipur bus stand 25 km from MUJ. [18] It also places Jaipur Railway Station 24 km away and Jaipur Airport 27 km away. [18]

These are campus-access facts, not a MUJ student shuttle schedule. The targeted searches did not locate a MUJ route list, stop roster, timetable, transport registration form or transport allotment PDF. The MUJ hostel FAQ likewise returned no transport-specific answer. Therefore, no route names, stops or schedules should be invented or borrowed from unrelated Jaipur transport pages. The absence of a public route roster may mean the information is delivered privately, may be maintained elsewhere, or may not be indexed. It does not show that MUJ has no transport service.

A useful comparative control is visible in Hilliard City Schools' official bus-stop page. It describes primary student transportation information and provides an in-district student login, with student ID and birth date fields, rather than exposing every student's assignment as a public roster. [19] This is not a MUJ policy and not a legal requirement for MUJ. It is a comparative design pattern showing how route data can be individualized while general transport information remains public.

| Transport information class | MUJ public evidence | Exposure risk | Safer publication pattern |
|---|---|---|---|
| Campus address | Official contact page. [18] | Low; intended for visitors. | Public. |
| Intercity bus availability | Jaipur-Delhi service description. [18] | Low to moderate; not an individual's routine. | Public, with freshness date. |
| Distance to bus stand, rail and airport | Official access information. [18] | Low; general location information. | Public. |
| Student route assignment | Not located. | High when joined to name or register number. | Authenticated student/parent view. |
| Stop and pickup time | Not located. | High; recurring movement pattern. | Authenticated, minimum necessary display. |
| Transport payment/allotment status | Not located. | Financial and behavioral information. | Private account or authorized staff view. |

**Inference:** A public route map may be acceptable when it shows only general service corridors, but a public route-assignment list is riskier because it links people to predictable locations and times. The distinction is analytical and should be validated against MUJ's actual service model before any operational change.

## Privacy and Regulatory Analysis

The MAHE privacy policy says it applies to students, parents, visitors and other individuals who provide personal data to the Institute. [6] It lists data categories that may include name, contact details, address, email, gender, age, date of birth, username and password. [6] It also discusses health information, financial information in connection with purchases or online payment, IP address, browser and operating-system information. [6] A hostel or transport record may not contain every category, but the policy demonstrates that the institutional environment processes identity, contact, payment and technical data.

The policy says information may be used for enrolment and service provision, and that personal details may be used for statements, payment reminders, newsletters and similar communications. [6] It says data is not sold or traded, while allowing sharing with third parties assisting with business operations, website operation or services, subject to confidentiality. [6] It also identifies sharing with college affiliates and third-party service providers such as website hosting and webinars. [6]

The policy states that data is retained as long as necessary for the collected purposes, including legal, accounting or reporting requirements, and that it will be securely destroyed after the retention period according to an internal retention and destruction policy. [6] It describes reasonable physical and technical measures against unauthorized access, alteration, disclosure or destruction, while acknowledging that no website, transmission, computer system or wireless connection is completely secure. [6] It provides a privacy grievance email and says grievances will be addressed within 30 days. [6]

The DPDP Act defines personal data as data about an individual who is identifiable by or in relation to that data. [8] It defines processing broadly to include collection, recording, organization, storage, retrieval, use, sharing, disclosure, dissemination, making available, erasure and destruction. [8] It defines a personal-data breach to include unauthorized processing or accidental disclosure, acquisition, sharing, use, alteration, destruction or loss of access that compromises confidentiality, integrity or availability. [8]

The Act says a person may process personal data only in accordance with the Act and for a lawful purpose, including where the Data Principal has given consent. [8] Its notice provision requires information about the personal data and purpose, how rights may be exercised and how a complaint may be made. [8] The Act requires appropriate technical and organizational measures and reasonable security safeguards, and requires breach intimation to the Board and affected Data Principals. [8]

For student records, the Act's rights provisions are directly relevant. Section 11 concerns obtaining information about personal data and its processing. [8] Section 12 provides correction, completion, updating and erasure, subject to retention necessary for the specified purpose or legal compliance. [8] Section 13 provides grievance-redressal means, and consent may be withdrawn at any time under the cited provision. [8] The exact legal application and commencement of provisions should be confirmed by MUJ counsel and current government notifications; this report does not give legal advice.

The PIB source confirms that the Government notified the DPDP Rules, 2025 on 14 November 2025. [9] The extracted source does not itself provide a complete commencement timeline, so this report does not claim that every Act provision is currently enforceable in the same way. This qualifier is important because a compliance recommendation can be sound even where legal commencement details differ.

## Application-Security Controls for SLCM Artifacts

OWASP describes ASVS as a basis for testing web-application technical security controls and a list of secure-development requirements. [12] For the requested use case, the relevant control questions are authorization, object-level access to PDFs and records, authentication assurance, secure document delivery, logging, retention and error handling. These are control categories, not evidence that MUJ fails any of them.

OWASP's Authorization Cheat Sheet recommends least privilege, deny-by-default, permission validation on every request, server-side checks and tests that verify the permission mapping. [11] [11] Applied to hostel and transport artifacts, that means a student should receive only their own room and route record; a parent should receive only the linked student records authorized by the institution; a warden should see the block or cases needed for the job; and a transport administrator should not automatically see medical or payment details.

| Control | Question for an authorized MUJ review | Evidence to collect without exposing PII |
|---|---|---|
| Authentication | Are student, parent, staff and administrator roles distinct? | Role matrix and test-account results. |
| Authorization | Does every document request enforce server-side ownership and role checks? | Redacted authorization test cases and logs. |
| Object-level access | Can one authorized test account retrieve another test account's artifact? | Synthetic records only; no real student identifiers. |
| Document delivery | Are URLs expiring, revocable and non-guessable? | Configuration evidence and synthetic URL tests. |
| Search indexing | Are private PDFs excluded from indexing and cacheable public paths? | Headers, robots policy and deployment design review. |
| Logging | Are view, download, approval and publication events recorded? | Redacted audit samples. |
| Retention | Are obsolete room and route lists removed or access-revoked? | Retention schedule and deletion evidence. |
| Incident response | Can a mistaken publication be revoked and affected people notified? | Tabletop exercise record. |

CERT-In Directions state that covered service providers, intermediaries, data centres, body corporates and government organizations must report listed cyber incidents within six hours of noticing or being informed. [10] They also require ICT-system logs to be enabled and securely maintained for a rolling 180 days within Indian jurisdiction. [10] The directions additionally require time synchronization to approved or accurate sources. [10] The university and its vendors should determine coverage with counsel, but these are strong operational reasons to preserve reliable publication and access logs.

## Action Plan for the University Security Club

The club should first build a synthetic artifact inventory. Create fake names, fake register numbers, fake rooms and fake routes, then map each field to a legitimate audience and retention period. This demonstrates the privacy problem without acquiring or redistributing real student information.

Second, request an authorized, non-production review from MUJ's IT, hostel and privacy contacts. Ask for a role matrix, publication workflow, room-change workflow, transport assignment workflow, retention schedule and incident escalation contacts. Ask whether public notices are approved, whether PDFs are indexed, and whether old versions are revoked. Do not ask for credentials or private student records.

Third, recommend a two-tier publication model. The public tier should contain hostel rules, fee policies, general block descriptions, general transport information and contact channels. The private tier should contain an individual student's allotment, route, stop, timing, payment state and room-change status. A staff dashboard can provide aggregate occupancy and operational views without displaying unnecessary personal fields.

Fourth, recommend a privacy review before each publication. The reviewer should ask: Does the document identify a person? Does it reveal residence or routine movement? Is every field necessary? Is there a less identifying alternative? Is the audience limited? Does the link expire? Is the document searchable or cacheable? Will the link remain valid after reassignment? These questions operationalize the Act and OWASP principles without assuming a breach.

## Unanswered Questions and Evidence Gaps

| Question | Current answer | Confidence | Safe next step |
|---|---|---|---|
| Does public MUJ SLCM expose allotment PDFs? | Not located in the public search corpus. | Medium for search result; low for universal absence. | Authorized portal-owner review. |
| Does MUJ publish names and register numbers in lists? | Not verified for MUJ. | High that this research did not verify it. | Do not repeat or redistribute alleged examples. |
| What are MUJ student transport routes and stops? | Not located publicly. | High for the searched public corpus. | Ask transport office for current, authorized documentation. |
| What is the room-change form and SLA? | Not located; only policy threshold is public. | High. | Obtain approved workflow from hostel administration. |
| Are SLCM versions exactly ASP.NET MVC 5.3, .NET 4.x and IIS 10? | Not independently verified here. | High. | Use authorized asset inventory or vendor documentation. |
| Is Akamai the current reverse proxy? | Not independently verified here. | High. | Confirm through authorized architecture documentation. |
| Is Microsoft 365 the complete identity path? | Email-domain labels and public identity references do not prove the full path. | High. | Confirm with identity owners, not active probing. |
| Are MAHE policy statements MUJ-specific in every operational detail? | The retrieved policy is an MAHE policy and references students and parents. | Medium. | Confirm MUJ applicability and local notice text. |

## VERDICT

**Overall verdict: the public evidence supports a meaningful privacy-risk review, but does not establish that MUJ has publicly exposed hostel allotment lists, transport rosters or an exploitable SLCM weakness. Confidence: Medium-High for the verified official hostel, fee, FAQ, SLCM landing-page, MAHE policy, DPDP, CERT-In and OWASP statements; Medium for the negative search findings; Low for any claim about authenticated or unindexed content.**

The strongest verified finding is process asymmetry. MUJ publicly documents hostel facilities, fees, allocation conditions and a restrictive room-change rule, while the public search corpus does not provide a comparable route roster or MUJ resident-allotment list. [2] [14] [18] The safest conclusion is not that the system is exposed or secure. It is that the university should ensure the private operational artifacts are deliberately separated from public informational pages, protected by server-side authorization, logged, retained only as needed and published only in the minimum necessary form.

A university security club can make a valuable contribution by documenting this design distinction, testing only with written authorization and synthetic data, and presenting a redacted control matrix rather than real names, register numbers, rooms, stops or credentials. That approach is consistent with the DPDP concepts of personal data and processing, with the MAHE policy's stated safeguards and retention principles, with CERT-In logging and incident-response expectations, and with OWASP least-privilege authorization guidance. [8] [6] [10] [11]

## References

1. *Announcement - Manipal University Jaipur Announcement*. https://www.jaipur.manipal.edu/announcement.php
2. *MUJ Hostel - Manipal University Jaipur *. https://jaipur.manipal.edu/hostel-facility.php
3. *Manipal University*. http://mujslcm.jaipur.manipal.edu/
4. *MUJ Hostel | Overview - Manipal University Jaipur*. https://jaipur.manipal.edu/hostel-overview.php
5. *FAQ's - Manipal University Jaipur *. https://jaipur.manipal.edu/faq%27s.php
6. *Privacy & Cookie Policy | MAHE*. http://manipal.edu/mu/important-links/privacy-and-cookie-policy.html
7. *Digital Personal Data Protection Rules 2025 | Ministry of Electronics and Information Technology*. https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa?pageTitle=Digital-Personal-Data-Protection-Rules-2025
8. [xxxGIDHxxx xxxGIDExxx vlk/kkj.k Hkkx [k.M izkf/kdkj ls izdkf'kr PUBLISHED BY AUTHORITY lañ ubZ fnYyh] 'kqØokj] vxLr 11] 2023@Jko.k 20] 1945](https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf)
9. *Digital Personal Data Protection (DPDP) Rules, 2025*. http://pib.gov.in/PressReleasePage.aspx?PRID=2190655
10. *No. 20(3)/2022-CERT-In Government of India Ministry of Electronics and Information Technology (MeitY) Indian Computer Emergency Response Team (CERT-In) Electronics Niketan,*. https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf
11. *Authorization - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
12. *OWASP Application Security Verification Standard (ASVS) | OWASP Foundation*. https://owasp.org/www-project-application-security-verification-standard
13. *Room Decription - Manipal University Jaipur*. https://jaipur.manipal.edu/room-description.php
14. *Hostel Fee - Manipal University Jaipur*. https://jaipur.manipal.edu/hostel-fees.php
15. *MESS FEE - Manipal University Jaipur*. https://jaipur.manipal.edu/mess-fees.php
16. *FAQs - Manipal University Jaipur *. https://jaipur.manipal.edu/faqs-regarding-hostel.php
17. *Chief Warden's Message - Manipal University Jaipur*. https://jaipur.manipal.edu/chiefwardensmessage.php
18. *Contact Us - Manipal University Jaipur *. https://www.jaipur.manipal.edu/contact-university.php
19. *Bus Stop information - Hilliard City Schools*. https://www.hilliardschools.org/departments/transportation/busstop
