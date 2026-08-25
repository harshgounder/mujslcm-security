# MUJ SLCM Orientation and Onboarding Evidence Report

## Executive Summary

This report reviews only publicly accessible material relevant to the Manipal University Jaipur (MUJ) Student Life Cycle Management (SLCM) onboarding ecosystem. It does not attempt authentication, password testing, endpoint enumeration, exploitation, or access to non-public records. The evidence base consists primarily of MUJ-hosted PDFs and pages, supplemented by one public header-observation record and one clearly non-official document-hosting page used only to identify historical or conflicting language.

- **Primary Onboarding Artifact**: MUJ publishes a First-Year Student Profile Registration Guide that describes SLCM as the platform for academic information and gives an ordered profile-completion workflow -> use it as the principal orientation/onboarding reference, but confirm its currency with Admissions before operational reliance [3].
- **Credential Delivery**: The official guide states that the Department of Admissions sends the SLCM username and password to the personal Gmail address supplied during admission -> the public record identifies the sending office and delivery channel, not the underlying technical account creator [3].
- **Default Password Finding**: No reviewed official MUJ artifact publishes a default SLCM password value. The official FAQ describes the SLCM password as being aligned with the official Outlook ID, while the profile guide says credentials are sent by Admissions -> treat the relationship as documented but do not infer a password formula [226.1-2; 168.22-28].
- **First-Time Login**: The SLCM guide describes first access at a high level and identifies the portal URL, but it does not require a first-login password change. The separate Office 365 SOP does explicitly describe a temporary-password flow and a forced password change for Microsoft 365 email [168.18-28; 224.4-16].
- **Provisioning Timing**: The reviewed material does not state when the SLCM or official email account is technically created, activated, or made usable. It describes when a student receives credentials, which is not the same as proving backend provisioning time [168.22-28; 224.6; 224.90-91].
- **Orientation Integration**: The 2026 orientation page connects physical reporting, document verification, SLCM academic-profile registration, Office 365/Outlook help, SLCM FAQs, and the profile-registration guide into one support path [141.110-126; 141.149-154].
- **Identity and Recovery**: The live portal exposes student and parent sign-in modes and a password-reset link to Microsoft, while the official FAQ routes SLCM failures to DMS/AMS and Outlook failures to IT Infra [273.0-3; 226.3-18].
- **Application-Stack Evidence**: A third-party header-observation page records IIS 10, ASP.NET MVC 5.3, ASP.NET 4.0.30319, and ASP.NET as the power-by value at a point in time. It does not establish source-code composition, patch level, backend topology, or Akamai usage; Akamai is not present in that observation [9].
- **Security Interpretation**: The strongest defensible conclusion is that MUJ publicly documents credential delivery and onboarding actions, but intentionally leaves the sensitive operational details of account creation and exact provisioning timing undocumented in the reviewed corpus -> a club should catalogue the artifacts and gaps, not attempt to fill them by testing the service.

## Scope, Method, and Evidence Handling

The research question concerns orientation handbooks, SLCM step-by-step login material, first-time login instructions, default-password language, and account provisioning. The research therefore separates five evidence classes: official MUJ web pages, official MUJ PDFs, public interface text, third-party observations, and non-official document reposts. This separation matters because a search result can expose a historical document or a similarly named SLCM product without proving that the material is current MUJ policy.

The principal source is the MUJ-hosted First-Year Student Profile Registration Guide. Its title and pre-instruction heading identify it as a student portal onboarding artifact, and it describes SLCM as the one-stop platform for academic information during a student's university tenure [3]. The second principal source is the MUJ-hosted SLCM FAQ, which supplies a registration link, a username convention, a relationship to the official Outlook identity, and support routing [6]. The third is the MUJ-hosted Office 365 SOP, marked version 1.0 and effective June 2025, which documents first-time email setup, password replacement, MFA, and recovery [224.0-6; 224.90-91].

The 2026 orientation page is treated as an integration and support source, rather than as a credential specification. It names the orientation schedule, reporting and document-verification process, help documents, SLCM contacts, and Office 365/Outlook support [141.67-74; 141.110-126; 141.149-156]. The live SLCM page is treated as interface evidence only. Its public text exposes a welcome message, sign-in, student identity hint, and parent-login option; it does not disclose a default password or provisioning workflow [10].

**Evidence-based reasoning summary, not private chain-of-thought:** the conclusion follows by comparing what each official artifact explicitly says with what it omits. Where the documents name a sender, channel, action, or contact, the report states that fact. Where they do not name a backend actor or time, the report records an explicit unknown. Where a conclusion combines two facts, it is labelled an inference. This approach avoids treating a portal label, a password-reset link, or a web-server header as proof of a broader architecture or policy.

## Artifact Inventory and Provenance

| Artifact | Host and exact URL | Format or surface | Publicly documented purpose | Evidentiary status |
|---|---|---|---|---|
| First-Year Student Profile Registration Guide | http://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf | PDF | Student profile and SLCM onboarding | Primary official MUJ artifact [3] |
| Frequently Asked Questions and Contacts for SLCM Registration | https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf | PDF | SLCM registration, credential relationship, troubleshooting, contacts | Primary official MUJ artifact [6] |
| Orientation Program 2026 | https://jaipur.manipal.edu/induction-orientation-program.php | Web page | Orientation schedule, reporting, documents, help documents and contacts | Primary official MUJ page [141.67-74; 141.110-126] |
| Office 365 and Outlook setup SOP | https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf | PDF | First-time university email setup, password change and MFA | Primary official MUJ IT artifact, version 1.0, effective June 2025 [8] |
| SLCM landing route | https://mujslcm.jaipur.manipal.edu/ | Public portal page | Sign-in and parent-login surface | Primary public MUJ interface evidence [2] |
| SLCM Home Index route | https://mujslcm.jaipur.manipal.edu/Home/Index | Public portal page | Sign-in identity hint and parent-login surface | Primary public MUJ interface evidence [10] |
| Header observation | http://api.hackertarget.com/httpheaders?q=https://mujslcm.jaipur.manipal.edu/ | Third-party observation | Point-in-time response-header record | Secondary technical observation [9] |
| Historical repost | https://www.collegesidekick.com/study-docs/16707539 | Third-party document page | Reposted document labelled Frequently Asked Questions (2023) | Non-official, non-endorsed, not current-policy evidence [7] |

The table shows why the PDF guide and MUJ FAQ carry more weight than the third-party repost. The College Sidekick page attributes the uploaded material to BITS Pilani Goa, states that it is not endorsed by that school, identifies a user uploader, and records an August 4, 2024 upload date [7]. It can preserve historical text, but it cannot establish that the content is a current MUJ instruction. The technical header record is similarly useful only for what it observed, not for claims beyond the response headers.

## Orientation Program and Onboarding Context

The official 2026 orientation page is not merely an event announcement. It connects orientation attendance to document verification and publishes a support structure for the student onboarding lifecycle. The page states that students must report by 9:00 AM and that document verification begins at 9:15 AM in designated rooms [4]. It also lists orientation venues, including the Old Food Court and the Smt. Vasanti R Pai Auditorium in Academic Block 3 [141.74; 141.84-85]. These facts establish a physical verification checkpoint, not an online account-provisioning timestamp.

The page lists an Orientation Programme Schedule 2026, an Orientation Process Flow, Important Helpline Numbers, a list of documents to be submitted during reporting, and help documents [4]. The help-document set includes Office 365/Outlook/password-reset material, Hostel FAQs, SLCM FAQs, and the SLCM Profile Registration Guide [4]. This is the clearest public evidence that MUJ expects SLCM onboarding and institutional email setup to be handled as related onboarding tasks.

The page separately lists support for Academic Profile Registration and SLCM, as well as IT Helpdesk support for Outlook registration [4]. It also gives Team Admissions contact information for admission queries [141.115-118; 141.155-156]. The division is analytically important: Admissions is associated with admission and profile corrections, SLCM support is associated with academic-profile registration, and IT support is associated with Outlook. **Inference:** this routing suggests functional ownership boundaries, but it does not prove which team creates records in an identity directory or in the SLCM database.

The orientation material therefore answers the question "where should a new student look for help?" more clearly than it answers "which system creates the account?" It also establishes that physical reporting and document verification are part of the onboarding sequence. The profile guide says uploaded documents are verified during physical reporting and document verification at the university [3]. That wording supports an operational distinction between online submission and later institutional verification.

## The Official SLCM Profile-Registration Workflow

The guide begins with preparation. Students are told to gather scanned required documents, a recent passport-size photograph, a signed and notarized anti-ragging affidavit containing student and parent or guardian declarations, and a parent mobile number for OTP verification [3]. It also tells students to rename files according to document names [3]. These are onboarding prerequisites, not credentials and not evidence of account provisioning.

The guide then identifies the SLCM portal URL and says that the Department of Admissions sends the username and password to the personal Gmail address supplied during admission [3]. It additionally tells students to activate the official email ID and says that a standard operating procedure for resetting the official email password is included in the email sent to the personal Gmail account [3]. This is the most direct public description of credential delivery found in the reviewed official corpus.

After login, the guide directs the student to the Student Details section. It says that several fields are non-editable and are pre-filled from admission information or generated by MUJ, including the registration number, student name, academic year, programme or branch, date of joining, date of birth, gender, mobile number, maximum programme duration, specially abled status, email ID, and year of admission [3]. If these details are wrong, the student is directed to Admissions for correction after classes commence [3]. The FAQ corroborates the governance point by saying admission-entered personal details can be changed by Admissions after verification [6].

The remaining workflow covers ABC or APAAR ID, hostel status, educational qualifications, address details, parent and guardian information, document uploads, profile picture requirements, policy declarations, and parent-mobile OTP completion [168.64-84; 168.85-117; 168.118-143]. Parent-mobile verification enables parent login, according to the guide [3]. The document upload section identifies mandatory records and file constraints, while the final section requires declarations and OTP verification before completion [168.85-87; 168.135-143].

| Workflow stage | Explicit public statement | Security-relevant interpretation |
|---|---|---|
| Preparation | Required documents, photograph, affidavit and parent mobile OTP readiness [3] | Prepares identity and evidence inputs; does not disclose account creation |
| SLCM entry | Portal URL is published [3] | Identifies the intended public service; does not authorize testing |
| Credential delivery | Admissions sends SLCM username and password to the personal Gmail used in admission [3] | Documents delivery office and channel, not backend creator |
| Official email | Student is told to activate official email; password-reset SoP is in the email [3] | Email setup is linked to onboarding, but activation timing is absent |
| Student Details | Admission-seeded and MUJ-generated fields are non-editable [3] | Indicates authoritative data fields and correction workflow |
| Parent details | Parent mobile is verified by OTP and enables parent login [3] | Shows a second user relationship and verification dependency |
| Documents | Mandatory uploads and later physical verification are described [168.85-117; 168.140-143] | Online profile completion is not the same as final document acceptance |
| Completion | Declarations and parent-mobile OTP complete the process [3] | Defines workflow completion, not account provisioning time |

The actionable insight is that the guide is a profile-registration manual, not a complete identity-management specification. It tells a student what to prepare and submit, while leaving directory synchronization, account creation, initial credential generation, and activation events outside the public narrative.

## Login, First-Time Access, and Password Language

The official SLCM FAQ gives the most specific public credential language. It publishes the registration link, describes the username as a name-plus-registration-number convention, and says the password is "as per official outlook ID" [6]. This report intentionally does not reproduce the FAQ's sample identifier or treat it as a live credential. The phrase is useful as evidence of the documented relationship, not as a basis for guessing any student's username or password.

The profile guide uses different wording: it says the username and password are sent to the personal Gmail account by the Department of Admissions [3]. The two statements are not necessarily contradictory. One describes the delivery event; the other describes a relationship between the SLCM password and the official Outlook identity. However, the public material does not say whether the same password is synchronized, whether it is separately generated from an Outlook record, whether the phrase is shorthand for a temporary password, or whether the relationship applies to every student cohort. **Inference:** these are plausible implementation possibilities, but none is established by the reviewed documents and none should be presented as fact.

The search corpus also contains generic or third-party SLCM manuals that mention changing a default password. Those materials are not MUJ primary evidence. The official MUJ guide itself does not state a default SLCM password and does not state that the first SLCM login forces a password change [3]. Therefore the correct answer to the default-password question is: **no default SLCM password value is publicly stated in the reviewed official MUJ artifacts**.

The live public portal exposes sign-in, a student identity hint, parent login, and a forgot-password path that points to Microsoft's password-reset service in the public HTML [10]. This establishes recovery affordance and identity integration at the interface level. It does not reveal whether the SLCM application validates locally, delegates to Microsoft, or uses a synchronized credential store. **Inference:** the Microsoft reset link and the FAQ's Outlook relationship suggest integration between SLCM onboarding and Microsoft identity, but they do not prove the exact authentication protocol or directory architecture.

Microsoft 365 email is documented more fully in the official June 2025 SOP. It calls itself a step-by-step guide for first-time email setup and MFA configuration [8]. It tells the user to enter a current or temporary password and says a new password will then be required [8]. It defines a setup password policy requiring no name or personal information, a combination of character classes, and at least 13 characters for the setup flow [8]. The recovery section states a 16-character minimum for a reset password [8]. Because these are Microsoft 365 email instructions, they must not be silently re-labelled as SLCM password rules.

| Password or access question | Official MUJ evidence | Answer status |
|---|---|---|
| Is an SLCM username convention published? | Official FAQ states a name-plus-registration-number pattern [6] | Yes, convention published; do not infer individual identifiers |
| Is an SLCM password value published? | Official FAQ refers to the official Outlook identity; profile guide says credentials are emailed [226.1-2; 168.22-24] | No value published |
| Is a default SLCM password published? | No reviewed official guide or FAQ states one [168.22-28; 226.0-45] | Unknown, not publicly documented |
| Is first SLCM login described? | Portal entry and profile workflow are described [3] | High-level only |
| Is an SLCM first-login password change required? | No explicit requirement in reviewed official SLCM material [3] | Unknown / not stated |
| Is first-time email password change described? | Temporary-password entry followed by a prompt to set a new password [8] | Yes, for Office 365 email |
| Is MFA mandatory for Office 365? | SOP says MFA is mandatory before Office 365 use [8] | Yes, for Office 365 per the SOP |

## Account Provisioning: Who, When, and What Is Actually Proven

The strongest explicit statement about who is involved is that the Department of Admissions sends SLCM credentials to the personal Gmail account supplied during admission [3]. The profile guide also says that admission-provided values may be pre-filled and that incorrect values should be corrected through Admissions [3]. The FAQ similarly says Admissions changes admission-entered details after verification [6]. These statements support a role for Admissions in credential delivery and correction of admission-originated data.

They do not prove that Admissions creates the SLCM account in the application database. Sending credentials may be performed by a staff workflow, an automated process initiated by Admissions, an identity-management system, or a separate IT service. The reviewed documents do not name the database administrator, directory administrator, application service, registrar, or automated job responsible for technical provisioning. The Office 365 SOP also does not state who creates or provisions the university email account [224.0-6; 224.90-91].

Timing is similarly limited. The guide says credentials have been sent to the personal Gmail account and then presents the portal onboarding sequence [3]. It does not say whether delivery occurs immediately after admission confirmation, after fee payment, after document verification, before orientation, on a cohort date, or after another institutional event. The orientation page gives reporting and verification times, but those are physical event times rather than account-activation times [4].

The evidence supports a three-part distinction:

1. **Admission data capture:** fields may be pre-filled from information supplied during admission [3].
2. **Credential delivery:** Admissions sends SLCM credentials to the personal Gmail address used in admission [3].
3. **Technical provisioning and activation:** the public documents do not identify the system actor or timestamp [168.22-28; 224.0-6].

**Inference:** the public workflow probably depends on an upstream admission record because the guide says fields are based on admission information and because Admissions handles corrections. That is a reasonable data-lineage hypothesis, not proof of the internal implementation. A security club should record it as an architecture question for authorized clarification, not as a finding about a hidden endpoint or database.

## Identity, Support, and Recovery Boundaries

The SLCM FAQ routes login failures to verification of credentials and then to DMS or AMS contacts [6]. It routes Outlook failures to password reset and then to Team IT Infra [6]. The orientation page independently lists SLCM and Academic Profile Registration contacts and an IT Helpdesk number for Outlook registration [4]. This is consistent with a support model in which SLCM academic-profile issues and Microsoft 365 identity issues are handled by different operational teams.

The official email SOP documents Microsoft sign-in at the Microsoft portal, a temporary-password flow, forced password replacement, MFA setup, recovery through a forgot-password workflow, and additional verification methods [224.8-16; 224.25-32; 224.90-107]. It states that Microsoft Authenticator, phone, and personal email methods can be configured as verification methods [8]. These details are relevant to identity governance, but they are not evidence that SLCM itself uses Microsoft federation or that SLCM passwords are identical to Microsoft passwords.

The live SLCM page contains a student email-domain hint and a separate parent-login mode in its public interface [10]. The public HTML also exposes a Microsoft password-reset destination [10]. These facts indicate that the interface has been designed around student and parent roles and a Microsoft-linked recovery path. They do not authorize attempts to submit credentials, probe validation behavior, or inspect other users' records.

| Function | Publicly named route or owner | What remains unknown |
|---|---|---|
| SLCM credential delivery | Department of Admissions via personal Gmail [3] | Automated versus manual delivery and technical creator |
| SLCM login support | DMS/AMS contacts in the FAQ [6] | Internal escalation workflow and identity-system ownership |
| Outlook access support | Team IT Infra and orientation IT Helpdesk [226.14-18; 141.119-120] | Account-creation trigger and mailbox provisioning timestamp |
| Admission-seeded corrections | Admissions after verification [168.59; 226.35-38] | Exact approval system and audit-log process |
| Parent access | Parent mobile OTP enables parent login [3] | Parent-account creation trigger and lifecycle |
| Password recovery | Microsoft reset path and Office 365 recovery SOP [273.0-3; 224.90-107] | Whether recovery is federated, synchronized, or merely linked |

The decision-ready insight is to keep ownership, delivery, authentication, and recovery as separate questions. Public material answers each only partially, and collapsing them would create an unsupported architecture claim.

## Application and Edge-Technology Context

A public header-observation record for the SLCM URL reports HTTP 200, Microsoft-IIS/10.0, ASP.NET MVC version 5.3, ASP.NET version 4.0.30319, and X-Powered-By ASP.NET at the observation time [9]. This aligns with the technology context supplied in the research brief, but it should be described narrowly as an observed response-header fingerprint.

The observation does not prove that every route uses the same framework, that the deployed application is unpatched, that the application source code uses a particular MVC pattern, or that the backend is directly exposed. Response headers can be altered, removed, cached, or generated by an intermediary. The record is also hosted by a third-party header-observation service rather than by MUJ [9].

The same observation does not explicitly show Akamai [9]. Therefore the safe statement is not "MUJ is behind Akamai" based on this corpus. The safe statement is: **Akamai was not independently established in the reviewed public artifact set; the supplied Akamai context remains unverified here.** This is an evidence boundary, not a claim that Akamai is absent.

The portal's public HTML contains framework-related client-side assets and login-form behavior, but those details do not establish a vulnerability. A university security club should not convert passive fingerprints into exploit hypotheses without authorization. The appropriate research output is a technology inventory with confidence and source limitations, not a test plan against the live portal.

## Historical and Conflicting Artifacts

The College Sidekick page is important precisely because it demonstrates how false confidence can arise. It hosts a document titled Frequently Asked Questions (2023), identifies BITS Pilani Goa as the school, says the site is not endorsed by that school, and records an August 4, 2024 upload by a user account [7]. The uploaded text contains a MUJ-looking SLCM registration URL and login troubleshooting language [7].

This material should not be treated as current MUJ policy. Its provenance is external, its school attribution is inconsistent with MUJ, and its document date is historical. It may be a repost, a misattributed course document, or a copy of an older MUJ artifact, but the reviewed page cannot establish which. **Inference:** it is useful as a lead for version comparison, not as a source for current password or provisioning conclusions.

The official MUJ FAQ is materially stronger because it is hosted on the MUJ domain and its title directly concerns SLCM registration [6]. Even so, the FAQ itself has no visible date or audience metadata in the reviewed text [6]. The June 2025 Office 365 SOP has clearer version metadata, making it stronger for current email setup guidance than for SLCM policy [8]. The 2026 orientation page is the strongest source for current orientation scheduling and support routing [141.67-74; 141.110-126].

| Claim type | Best source | Confidence | Reason |
|---|---|---:|---|
| Orientation reporting and verification | MUJ Orientation Program 2026 page | High | Current official page with explicit schedule and reporting text [4] |
| SLCM profile workflow | MUJ First-Year Student Profile Registration Guide | High | Official student-facing PDF with ordered steps [168.0-4; 168.18-143] |
| SLCM credential delivery office and channel | MUJ profile guide | High | Explicit Admissions and personal Gmail wording [3] |
| SLCM password relationship to Outlook | MUJ SLCM FAQ | Medium-high | Explicit but terse and undated wording [6] |
| Default SLCM password value | None found in official reviewed sources | High confidence in non-finding | No official reviewed artifact publishes one [168.22-28; 226.0-45] |
| Office 365 forced first-time password change | MUJ IT SOP | High | Versioned SOP explicitly says temporary password and new password prompt [8] |
| Account creator and activation time | None found | High confidence in non-finding | Official sources describe sending and support, not technical provisioning [168.22-28; 224.0-6] |
| IIS/MVC/.NET header fingerprint | Third-party header observation | Medium | Exact headers reported, but point-in-time and secondary [9] |
| Akamai deployment | None independently established | Low/unknown | Not present in reviewed header observation [9] |

## Safe Research Boundaries for a University Security Club

This report is limited to public information. Acceptable follow-up work includes preserving the public PDFs and pages with retrieval dates, comparing future official versions, checking whether MUJ publishes revised orientation material, and asking the university through its published support channels for authorized clarification about account lifecycle documentation. The club can also build a source register that records URL, document title, visible version/date, evidence type, and confidence.

The club should not submit guessed credentials, use the public username convention to derive real student identifiers, attempt password-reset flows for accounts it does not own, inspect parent or student records, bypass controls, enumerate hidden routes, or probe the live application for security weaknesses without written authorization. The public presence of a login form, a password-reset link, or a response header does not grant permission to interact with the service beyond ordinary authorized use.

A responsible research question for MUJ would be: "Can the university provide the current student-facing SLCM and Office 365 onboarding documents, the documented account-lifecycle owner, and the official timing definition for credential delivery and activation?" That question seeks clarification without testing the system. It also directly addresses the gaps identified by the evidence.

## Verdict

**Verdict: The public MUJ corpus supports a high-confidence conclusion that MUJ publishes a student-facing SLCM onboarding workflow, an official SLCM FAQ, an orientation support page, and a versioned Office 365 first-time setup SOP.** The profile guide explicitly says that the Department of Admissions sends SLCM credentials to the personal Gmail address supplied during admission [3]. The SLCM FAQ publishes a username convention and says the password is aligned with the official Outlook identity [6]. The orientation page ties SLCM registration and Office 365 help to the orientation and reporting process [141.119-126; 141.149-154].

**Confidence: High for the existence and content of the official onboarding artifacts; medium-high for the documented credential-delivery relationship; high confidence that no default SLCM password value, technical account-creation actor, or exact provisioning timestamp was found in the reviewed official material; medium for the point-in-time IIS/MVC/.NET fingerprint; unknown for Akamai.** The last two classifications are deliberately conservative. The reviewed public evidence does not justify converting delivery by Admissions into proof that Admissions technically creates the account, and it does not justify converting a Microsoft password-reset link into proof of a particular federation or synchronization design.

The most useful security-club deliverable is therefore an evidence-backed artifact catalogue and gap register, not an access experiment. The central gap is not a discovered credential or vulnerability. It is the absence of public documentation explaining the technical account-lifecycle event between admission data capture, credential delivery, and successful activation. That gap should remain labelled **not publicly documented** unless MUJ provides an authorized, current statement.

## References

1. *ADMISSIONS - Manipal University Jaipur*. http://jaipur.manipal.edu/admissions.php
2. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
3. *Manipal University Jaipur First-Year Student Profile Registration Guide*. http://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf
4. *Orientation Program 2026 - Manipal University Jaipur - Manipal University Jaipur*. https://jaipur.manipal.edu/induction-orientation-program.php
5. *REGISTRATION FORM (UG/PG)*. https://jaipur.manipal.edu/img/pdf/Registration-Form.pdf
6. *Frequently Asked Questions and Contacts for SLCM Registration*. https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf
7. *Frequently Asked Questions (2023).pdf - Frequently Asked Questions and Contacts Registration Link: https:/mujslcm.jaipur.manipal.edu:122/ Q1. I am unable - College Sidekick*. https://www.collegesidekick.com/study-docs/16707539
8. *Standard Operating Procedure*. https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf
9. *http://api.hackertarget.com/httpheaders?q=https://mujslcm.jaipur.manipal.edu/*. http://api.hackertarget.com/httpheaders?q=https://mujslcm.jaipur.manipal.edu/
10. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
