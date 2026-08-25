# MUJ Admissions and SLCM: Public Data-Flow and Integration Report

## Executive Summary

- **Tenant Relationship**: Public DNS currently resolves `admissions.jaipur.manipal.edu` as a CNAME to `jaipurmanipal.nopaperforms.com` [18]. This is strong evidence that the branded MUJ admissions hostname is delegated to a NoPaperForms tenant, not merely that MUJ uses an unrelated admissions vendor. **Action**: treat the admissions hostname and NoPaperForms tenant as one public SaaS boundary, while avoiding any assumption that the SLCM system shares that boundary.
- **Admissions Surface**: MUJ's public admissions pages expose `Apply Now`, `Track Application`, an admissions contact channel, WhatsApp enquiry fields, and a `Pay Fee Online` link [15]. **Action**: document the admissions portal as the applicant-acquisition and application-status surface, separate from the student lifecycle login.
- **Applicant Data**: The official MUJ online-program admission manual names identity, contact, demographic, address, guardian, education, employment, photograph, signature, identity-proof, and eligibility-document data [9] [9]. **Action**: classify this as high-sensitivity education and identity data, with especially strong controls around uploaded identity and academic documents.
- **Payment and Status**: The manual says payment is online through card, net banking, or UPI, and that successful payment triggers email and SMS; it also defines statuses such as `Application Downloaded`, `Under Review`, `Admission Approved`, `Provisional Admission`, `Re Submission Required`, and `Rejected` [9] [9]. **Action**: model payment confirmation and status changes as key applicant-data transitions.
- **SLCM Onboarding**: MUJ's official SLCM FAQ names the SLCM registration link, describes a username based on a student's name and registration number, and states that the password is based on the official Outlook ID [17]. **Action**: treat SLCM as an admitted-student identity and lifecycle system, but do not claim that NoPaperForms automatically provisions accounts.
- **Admissions Authority**: The SLCM FAQ says that details entered at admission can be changed only by the Admission department after verification [17]. **Action**: infer a controlled admissions-to-SLCM data dependency, not an undocumented API or synchronization mechanism.
- **Vendor Role**: Meritto, the current product identity associated with NoPaperForms, states that customer-submitted applicant data is processed as a processor while the customer is the controller or fiduciary [14]. **Action**: obtain the MUJ-specific contract, data-processing addendum, retention schedule, and subprocessor list before making a complete legal or privacy assessment.
- **Security Evidence**: The NoPaperForms Trust Center publicly lists SOC 2, ISO 27001, and GDPR compliance statements, including an ISO surveillance-audit update dated May 21, 2025 and GDPR renewal dated June 5, 2026 [5] [5] [5]. **Action**: distinguish vendor-level attestations from controls proven for this MUJ tenant.
- **Integration Gap**: No public source reviewed here identifies a NoPaperForms API call, webhook, SSO assertion, database feed, or automated account-provisioning trigger connecting the admissions tenant to MUJ SLCM. The public API documentation lists application, payment, lead, form, query, and user modules, but does not establish that MUJ uses any particular integration [10]. **Action**: report the technical hand-off as `not publicly documented`.
- **Safety Boundary**: This report uses public webpages, public PDFs, public DNS, and public documentation only. It does not test authentication, submit forms, enumerate records, inspect applicant data, or attempt access beyond public pages. **Action**: any follow-up should use written authorization and a designated test environment.

## Scope, Evidence Standard, and What Can Be Concluded

This report covers the public relationship among three layers: the branded MUJ admissions portal, the NoPaperForms/Meritto SaaS layer, and the MUJ SLCM student-facing layer. It does not treat a product name, shared branding, a DNS record, or a generic workflow description as proof of an internal data transfer. The central distinction is between an observed public fact, a vendor-wide policy statement, and an inference about the likely operational architecture.

The strongest direct evidence is the DNS record. Google Public DNS returns a CNAME answer whose owner is `admissions.jaipur.manipal.edu` and whose target is `jaipurmanipal.nopaperforms.com` [18]. The target then resolves through an AWS load-balancer name in the `ap-south-1` region and returns several addresses [19]. DNS proves delegation and the currently visible resolution chain; it does not prove where application records are stored, whether a separate API exists, or whether the CNAME target is the only service involved.

The second strong evidence group is first-party MUJ material. The admissions page links to application tracking, an application route, a fee page, and admission support [15]. The SLCM FAQ separately identifies the SLCM registration URL and explains the relationship between admission-time details and later SLCM correction [17] [17]. These sources support a lifecycle relationship, but they do not state that an admissions form submission creates a student record automatically.

The third evidence group is vendor documentation. Meritto's privacy policy says that the customer is the data controller or fiduciary and that Meritto processes customer-submitted applicant data as a processor under documented instructions [14]. It also says that customers may independently integrate third-party tools, scripts, or applications and that data collected through those tools is governed by the customer and third party policies [14]. This is important because a customer-configured integration may exist without being described in the public vendor documentation. The absence of a public integration description is therefore not proof that no integration exists.

### Evidence classification table

| Evidence item | Public observation | Confidence | What it proves | What it does not prove |
|---|---|---:|---|---|
| MUJ admissions CNAME | DNS returns `jaipurmanipal.nopaperforms.com` as the CNAME target [18] | High | Hostname delegation to the named tenant | Record schema, storage, API calls, or SLCM synchronization |
| Tenant resolution | Target resolves through an AWS ELB chain [19] | High | Current public DNS resolution path | Security posture, tenant isolation, or backend database location |
| MUJ application surface | MUJ publishes Apply Now and Track Application links [15] | High | A public admissions workflow exists | Exact current field set for every program |
| SLCM FAQ | Registration URL, username pattern, Outlook-password basis, and admission-controlled correction are published [17] [17] | High | Admission information is relevant to SLCM records | Automated NoPaperForms account provisioning |
| Online-program manual | Detailed fields, uploads, payment, status, and refund rules are published [9] [9] [9] | High for its stated scope | A documented MUJ online-program workflow | That every campus program uses identical fields or rules |
| Meritto privacy policy | Customer is controller/fiduciary; Meritto is processor [14] | High for vendor policy | Vendor's stated role model | MUJ's negotiated role allocation or tenant configuration |
| Trust Center | SOC 2, ISO 27001, and GDPR statements are listed [5] | High for published assertion | Vendor-level public compliance claims | MUJ-specific audit scope or control effectiveness |

The decision-ready conclusion is therefore not that the systems are disconnected. It is that the public record shows a probable lifecycle relationship and a confirmed admissions SaaS delegation, while leaving the exact technical bridge undisclosed.

## Public Admissions Portal and NoPaperForms SaaS Boundary

The public MUJ admissions hostname is not merely adjacent to NoPaperForms in search results. The DNS answer directly names `jaipurmanipal.nopaperforms.com` as the CNAME target [18]. That finding matches the portal's visible use of NoPaperForms-style public assets in its HTML, including assets served from `cdn.npfs.co` on the public UG application route. The asset observation is useful corroboration of the SaaS presentation layer, but the decisive evidence is the DNS answer rather than a framework fingerprint or an asset URL.

The portal's public HTML also exposes applicant workflow concepts such as candidate name, candidate email, candidate mobile number, one-time-password entry, discipline selection, stream selection, and specialization selection on the UG route. These observations were obtained from server-returned markup and are used only to characterize labels, not to collect any submitted values. Because the extractor did not produce a clean, stable text document for the current form, the 2022 MUJ online-program manual is the more reliable citable source for the detailed field inventory below. The current form and the manual should not be treated as identical configurations.

The MUJ admissions page presents the public workflow as a university-branded service. It includes `Track Application` and `Apply Now` links [15]. It also publishes a WhatsApp enquiry template asking for Name, Phone, Email ID, Course, City, and State [15]. This is not proof that every field enters NoPaperForms, but it is direct evidence of applicant or prospective-student data expected by the admissions operation. The same page links `Pay Fee Online` [15], although the generic fee page does not by itself establish that the link is the same transaction flow as an application fee.

The vendor's public API documentation lists `Lead`, `Opportunity`, `Activity`, `Form`, `Payment`, `User, Role & Permission`, `Query`, and `Application` as public modules [10]. This list fits an education-enrollment platform capable of supporting lead capture, forms, applications, payment records, and role-based access. It does not prove that the MUJ tenant uses all modules, that a particular endpoint is enabled, or that any module communicates with SLCM.

### Architecture observations and limits

| Layer | Publicly observed name or function | Public evidence | Safe interpretation |
|---|---|---|---|
| Branded entry point | `admissions.jaipur.manipal.edu` | MUJ admissions page and DNS answer [18] | MUJ-branded admissions hostname |
| SaaS tenant | `jaipurmanipal.nopaperforms.com` | CNAME target [18] | NoPaperForms tenant or routing target |
| SaaS assets | `cdn.npfs.co` assets on current form markup | Public server HTML observation | SaaS presentation assets are used; backend flow remains unproven |
| Applicant acquisition | Enquiry template with Name, Phone, Email, Course, City, State | Official MUJ page [15] | Prospective-student contact data is solicited |
| Application tracking | `Track Application` | Official MUJ page [15] | Applicant status/tracking surface exists |
| Vendor modules | Lead, Form, Payment, Application, and other modules | Official API documentation [10] | Vendor supports these integration concepts |
| Student lifecycle | MUJ SLCM | Official FAQ [17] | Separate student-facing lifecycle portal |

**Decision insight:** the public record supports a SaaS-hosted admissions front end with a branded MUJ alias. It does not support publishing a claim that NoPaperForms directly owns, administers, or can log into MUJ SLCM.

## Applicant Data Categories and Likely Flow

The official MUJ online-program admission manual provides the most concrete public checklist. It instructs an applicant to select a programme and enter a name matching eligibility documents, a valid email address, and a valid phone number [9]. It also identifies date of birth, gender, marital status, blood group, nationality, category, and benefit category [9]. The communication address includes house number, street, city, district, state, PIN code, contact number, and alternative email address; a permanent address may be entered separately [9]. Guardian relationship and guardian name are included [9].

Academic data includes 10th and 12th or equivalent qualifications, a three-year bachelor's degree for applicable MBA/MCA candidates, work experience, qualifying examination, passing year, specialization, institution or board, and final percentage or an `Awaited` result state [9]. The manual says that an application number becomes visible after the applicant verifies details and submits the form [9]. These categories create a direct identity-to-application link and a direct relationship between applicant contact data and a status identifier.

The document-upload checklist is materially more sensitive. It calls for identity proof and eligibility documents, including academic marks cards, a degree certificate where applicable, a specimen signature, a passport-size photograph, and identity documents such as Aadhaar, Voter ID, PAN, or passport depending on the applicant category [9]. It specifies image and document formats, size limits, scan resolution, and readability requirements [9] [9]. It also requires an electronic signature on the declaration before submission [9]. The university may physically verify originals, and the manual says forms and documents are verified within five working days after online submission [9] [9].

Meritto's policy provides a useful vendor-side category map, but it is not a MUJ-specific form specification. It names identity and contact data such as name, mobile or phone, email, organization, designation, and country or region when an enquiry is submitted [14]. It also names technical and usage data including IP address, approximate location, browser and device information, operating system, pages viewed, time spent, clickstream paths, cookies, beacons, and pixels [14]. It identifies communications metadata such as SMS, call, and email metadata [14], and third-party data shared by systems integrated with Meritto [14].

### Applicant-data matrix

| Category | Publicly documented examples | Likely lifecycle purpose | Evidence status |
|---|---|---|---|
| Identity | Name, DOB, nationality, gender, identity proof [9] [9] | Match applicant to credentials and later records | Directly documented in manual |
| Contact | Email, mobile, address, alternative email [9] [9] | Notifications, SMS, correspondence, support | Directly documented in manual |
| Academic | 10th/12th results, degree, institution, passing year, specialization, percentage [9] | Eligibility and admission decision | Directly documented in manual |
| Demographic or benefit | Marital status, blood group, category, benefit category [9] | Eligibility, benefits, student records | Directly documented in manual |
| Guardian | Relationship and guardian name [9] | Applicant support and identity context | Directly documented in manual |
| Employment | Employment data and work experience [9] | Programme eligibility or profile | Directly documented, conditional in part |
| Uploaded documents | Marks cards, degree, photo, signature, identity proof [9] | Verification and record creation | Directly documented in manual |
| Application metadata | Application number, status, submission event [9] [9] | Tracking and workflow control | Directly documented in manual |
| Payment data | Online card, net banking, UPI payment; receipt access [9] [9] | Application or admission fee processing | Directly documented for online programmes |
| Technical data | IP, device, browser, usage, cookies, pixels [14] | Security, analytics, service operation | Vendor-wide policy, not MUJ-specific |
| Integrated-system data | Data shared by third-party systems [14] | Connected services and enrichment | Vendor-wide policy; exact MUJ sources unknown |

The table supports a bounded flow model: registration or enquiry creates contact and programme data; application completion adds demographic, academic, guardian, and employment data; document upload adds identity and eligibility material; payment adds transaction status and receipt information; review changes the application status; admission then provides data that is relevant to SLCM registration or correction. The last step is an inference from the manual and SLCM FAQ, not a published system diagram.

## Application Checklist, Verification, and Payment Flow

The manual's contents explicitly cover form filling, fee payment, personal data, educational qualification, document verification, photograph and specimen signature, declaration, application status, and withdrawal or refund [9]. Its general instructions tell applicants to read the prospectus, upload original supporting documents, keep information accurate, use the application portal for status and notifications, and expect correspondence through the registered email address [9]. The manual therefore describes an application lifecycle rather than a simple lead form.

After submission, the form enters `Under Review`, and university officials verify the form and documents within five working days [9]. The named status sequence includes `Application Downloaded`, `Under Review`, `Admission Approved`, `Provisional Admission`, `Re Submission Required`, and `Rejected` [9]. The manual says `Admission Approved` applies to candidates meeting eligibility criteria after receipt of the requisite fee, while provisional admission can address minor eligibility-document deficiencies at the university's discretion [9]. A resubmission state covers documentation deficiencies or fee shortages [9].

Payment is described as online only, using a valid credit or debit card through an online payment gateway or net banking/UPI [9] [9]. Successful payment triggers email and SMS, and the student portal provides access to the fee receipt [9] [9]. The manual does not state the payment processor name, merchant-of-record arrangement, card-data storage model, tokenization design, or whether NoPaperForms or another service hosts the payment page. Those are important unanswered questions, particularly because vendor documentation separately lists Payment as a module [10].

Refund rules are also explicit for the online-program document. The manual gives a withdrawal schedule of 100 percent at least 15 days before the notified admission deadline, 90 percent less than 15 days before it, 80 percent within 15 days after it, 50 percent more than 15 but within 30 days after it, and zero percent more than 30 days after it; it also specifies a Rs. 500 processing deduction [9]. If an application is rejected, the manual says the fee is refunded within 30 days after rejection less the Rs. 500 processing charge [9]. These rules should not be generalized automatically to every campus programme or current admissions cycle because the source is an online-program manual and is dated in the document archive.

### Status and payment table

| Stage | Publicly stated event | Data likely involved | Boundary or uncertainty |
|---|---|---|---|
| Application Downloaded | Form remains in this state until filled and submitted [9] | Draft form and contact/application context | Storage location not stated |
| Under Review | Submission triggers review and document verification [9] | Form, uploads, identity and academic data | Reviewer system not named |
| Payment | Online card, net banking, or UPI [9] [9] | Payment result, application reference, receipt | Processor and tokenization not stated |
| Payment confirmation | Email and SMS are triggered after successful fee payment [9] | Contact details, payment status | Message provider not named |
| Admission Approved | Eligibility and requisite fee conditions satisfied [9] | Eligibility, fee, decision, application number | SLCM hand-off not stated |
| Provisional Admission | Minor document deficiency may be accepted [9] | Deficiency and provisional decision | Authority and automation not stated |
| Re Submission Required | Documentation deficiency or fee shortage [9] | Missing document or fee status | No public API or webhook stated |
| Rejected | Conditions not fulfilled or withdrawal before admission [9] | Decision, reason, refund context | Retention after rejection not stated |

**Decision insight:** the admissions platform clearly handles a multi-stage workflow with documents and payments. The exact payment processor, document store, and notification providers remain out of scope for public proof.

## The Public Link to SLCM Account Creation

The SLCM evidence is stronger than a generic portal login. MUJ's official FAQ calls itself `Frequently Asked Questions and Contacts for SLCM Registration` and provides the registration link `https://mujslcm.jaipur.manipal.edu/` [17]. It describes a username based on a student's name and registration number and says the password is based on the official Outlook ID [17]. This is a public account-credential instruction, not merely a brand reference.

The same FAQ states that if personal details are not correct in the SLCM portal, the details filled at the time of admission can only be changed by Admission; the applicant or student is instructed to meet the Admission department, after which Admission verifies and changes the details [17]. It also routes missing mandatory documents to Admission [17]. These statements establish an operational dependency: admission-time data and verification affect SLCM records, and the Admission department is the authority for corrections.

The public SLCM login page separately shows `WELCOME TO MUJ PORTAL`, `Sign In`, `@muj.manipal.edu`, and `Sign In Parent Login` [20]. Its public surface does not explain how an account is provisioned, when it is created, whether the registration number originates in NoPaperForms, whether Microsoft 365 creates the Outlook identity, or whether a student record is manually entered into SLCM. Public HTML shows distinct student and faculty domain handling in the login presentation, but that does not prove an identity-provider protocol or a Microsoft 365 federation flow.

### SLCM linkage assessment

| Question | Public answer | Confidence |
|---|---|---:|
| Is there an official MUJ SLCM registration URL? | Yes, named in the official FAQ [17] | High |
| Does SLCM use an identity tied to a registration number? | The FAQ gives a name-plus-registration-number username pattern [17] | High |
| Is an Outlook identity involved? | The FAQ states the password is as per the official Outlook ID [17] | High |
| Does Admission control correction of SLCM personal details? | Yes, after admission verification [17] | High |
| Does the public FAQ say NoPaperForms provisions SLCM accounts? | No | High negative for the reviewed public source |
| Does it identify an API, webhook, SSO assertion, or batch feed? | No | High negative for the reviewed public source |
| Does it state when provisioning occurs? | No | High negative for the reviewed public source |
| Can the systems still be integrated privately? | Yes, this remains possible but is an inference, not a documented fact | Medium as an architectural possibility |

The responsible conclusion is `documented admissions-to-SLCM operational relationship; undocumented technical hand-off`. It would be unsafe to claim that the admissions application number is the SLCM registration number, because the public manual and FAQ use different terms and do not explicitly equate them. It would also be unsafe to claim automatic provisioning, Microsoft 365 SSO, or a shared database.

## Privacy, Processor Role, and Security Posture

The MAHE privacy policy is relevant context but is not a MUJ-specific data-processing agreement. It identifies name, contact details, postal address, email address, gender, age, date of birth, username and password, and states that health and financial information may be sensitive personal data in relevant contexts [8]. It says data may be collected automatically and from third-party social networking or commercial sources [8]. It describes purposes including enrolment, service delivery, customized content, recommendations based on website activity, payment reminders, newsletters, and brochures [8]. It also says personal data is not sold or traded but may be shared with third parties assisting business operations, website operation, or servicing, subject to confidentiality [8].

Meritto's policy is more specific about its own role. It says applicants, leads, and students provide personal data to customers, that the customer is the data controller or fiduciary, and that Meritto acts as processor under documented customer instructions [14]. It names vetted subprocessors for hosting, email, SMS, payments, security, and support and says they process data under documented instructions and contractual protections [14]. It also says customers may independently integrate tools, scripts, or applications and that those tools are governed by their own policies [14]. This is precisely why the MUJ tenant's individual configuration cannot be inferred from the generic vendor policy.

The policy states that data may be transferred to jurisdictions with different data-protection laws, with safeguards such as standard contractual clauses, PDPL mechanisms, and contractual safeguards aligned with India's DPDP requirements [14]. It says personal information is retained only as long as necessary for the collection purpose, legal or contractual obligations, or legitimate business needs, after which it is securely deleted or anonymized where possible [14]. The policy lists rights including access, correction, erasure, withdrawal of consent, grievance redressal, and nomination under India's DPDP framework [14]. It gives general privacy, grievance, and data-rights contacts, including `data@meritto.com`, `ticket@meritto.com`, and `grievance@meritto.com` [14]. These are vendor-wide statements, not proof of the notice shown to an MUJ applicant.

The Trust Center lists SOC 2, ISO 27001, and GDPR as compliance claims [5]. It records an ISO/IEC 27001 surveillance-audit completion on May 21, 2025 and a GDPR renewal completion on June 5, 2026 [5] [5]. The public page also lists policy and ISMS-related documents such as access control, business continuity, an ISMS manual, scope, and system description [5]. It does not publicly detail, in the reviewed text, the MUJ tenant's encryption configuration, retention schedule, subprocessor identities, backup design, incident history, penetration-test scope, or tenant-specific access controls. Absence from the reviewed public page is not evidence that those controls do not exist.

### Privacy and assurance table

| Topic | Public statement | Assessment for MUJ |
|---|---|---|
| Controller/processor | Customer is controller/fiduciary; Meritto is processor [14] | General model; MUJ contract not public |
| Applicant sources | Customer-hosted or Meritto-managed forms and integrated systems [14] [14] | Supports possible form ingestion; exact MUJ configuration unknown |
| Subprocessors | Hosting, email, SMS, payments, security, and support providers are mentioned [14] | Provider names and MUJ scope not established |
| Retention | Necessary-purpose/legal/business-needs standard; deletion or anonymization afterward [14] | No MUJ-specific duration |
| Rights | Access, correction, erasure, consent withdrawal, grievance redressal, and related rights [14] | Vendor policy; applicant notice and process should be confirmed with MUJ |
| Transfers | Global infrastructure may cause cross-border transfers with safeguards [14] | No MUJ-specific transfer map |
| Compliance | SOC 2, ISO 27001, GDPR claims and dated updates [5] [5] | Vendor-level assertion, not tenant audit evidence |

## Threat Modeling Without Unauthorized Testing

For a university security club, the most useful security analysis is a boundary model rather than an exploitation plan. The admissions portal handles identity, contact, academic, document, and payment-related information. The SLCM portal handles an identity associated with a registration number and an official Outlook identity [17]. The transition between these systems is therefore a high-value trust boundary even though its implementation is not public.

The principal risks are conceptual. First, duplicate or inconsistent identity records could arise if an applicant's name, email, mobile number, application number, registration number, or Outlook identity are mapped differently. The FAQ's instruction that Admission alone corrects SLCM details after verification [17] suggests a controlled reconciliation process, but it does not reveal whether reconciliation is manual or automated. Second, uploaded marks cards, identity proofs, photographs, and signatures are sensitive artifacts [9]. Their exposure would be more serious than exposure of a generic enquiry record. Third, payment status and admission status can affect access, refund, and enrolment decisions [9]. The public materials do not reveal authorization rules, webhook signing, replay protection, or reconciliation controls.

Fourth, the vendor policy names integrated systems, subprocessors, and technical usage data [14] [14] [14]. That creates a governance need to inventory what is enabled for this tenant, especially analytics, messaging, payment, document storage, and any CRM or student-system connector. Fifth, the public SLCM login presentation includes student and parent roles [20]. Role separation is visible at the interface, but no public material reviewed here establishes the authorization model behind those roles.

A safe assessment plan should be documentary. The club can request written permission from MUJ and ask for a sanitized architecture diagram, data-flow inventory, retention schedule, subprocessor list, incident-response contact, and a test account in a non-production environment. It should not submit fake applications to production, attempt password guessing, enumerate identifiers, request password resets for other users, inspect hidden application endpoints, or probe IIS, ASP.NET, Akamai, Microsoft 365, or SLCM behavior without explicit authorization. The public presence of a framework or CDN is not authorization to test it.

### Safe evidence-request table

| Requested artifact | Why it matters | Production access needed? |
|---|---|---:|
| Sanitized admissions-to-SLCM data-flow diagram | Confirms whether the bridge is API, batch, manual, or SSO | No |
| Field-mapping document | Establishes whether application and registration identifiers are equivalent | No |
| MUJ-specific privacy notice and DPA | Identifies controller, processor, retention, rights, and sharing | No |
| Payment architecture summary | Identifies processor, tokenization, receipts, and reconciliation | No |
| Upload-storage and deletion policy | Establishes document retention and access controls | No |
| Tenant-specific assurance report | Connects vendor controls to the MUJ service scope | No |
| Non-production test account | Allows authorized validation without applicant data | Only approved test environment |
| Incident and vulnerability-reporting process | Gives the club a safe escalation route | No |

## Synthesis: What the Evidence Means Together

Across three dimensions - ownership, data scope, and lifecycle integration - the evidence is asymmetric. Ownership of the admissions hostname is strongly evidenced by DNS: MUJ's branded host points to the NoPaperForms tenant [18]. The data scope is strongly evidenced for the online-program workflow: the manual describes identity, academic, demographic, document, payment, status, and refund data [9] [9] [9]. The lifecycle relationship is also evidenced, but at the business-process level: SLCM uses a registration-number-based identity and Admission controls corrections to details entered at admission [17] [17].

The weak dimension is the technical bridge. The vendor API documentation lists the kinds of objects one might expect in an enrollment platform [10], but it does not say that MUJ uses a particular API or that SLCM consumes a NoPaperForms record. The online-program manual describes an application portal and statuses but does not name SLCM, student-account creation, or an integration trigger [9]. The SLCM FAQ describes credentials and admission authority but does not name NoPaperForms. Therefore, the public record supports a likely hand-off in the operational sense, while the protocol, direction, timing, and automation remain unknown.

There is also a scope tension. MUJ's admissions page is a current public 2026-27 landing page [2], while the detailed admission manual is an archived online-program document. The current form visibly contains programme and verification controls, but the public extractor did not yield a stable clean field inventory for it. It would be an error to claim that the archived manual is the exact schema for every current UG, PG, PhD, or campus application. The correct use is as a documented MUJ workflow example and a strong indicator of the categories the institution may process.

A second tension concerns privacy. Meritto's policy assigns the customer the controller or fiduciary role and Meritto the processor role [14], while the MAHE-wide policy describes university purposes and operational third-party sharing [8] [8]. These statements are compatible, but they do not substitute for a tenant-specific notice. A security or privacy review should therefore ask who determines the purposes of the admissions processing, which legal entity receives the application, which vendors receive documents or payment metadata, and when records move to SLCM.

A third tension concerns security assurance. Vendor compliance claims are meaningful evidence of an assurance programme, especially where the Trust Center lists SOC 2, ISO 27001, and GDPR [5]. They are not equivalent to evidence that MUJ has configured least privilege, tenant isolation, secure document deletion, signed integration messages, or strong SLCM provisioning controls. The right recommendation is not to dismiss the certifications or to treat them as conclusive, but to request scope and applicability for the MUJ service.

## VERDICT

**Verdict: The public evidence supports a high-confidence conclusion that MUJ's branded admissions hostname is currently delegated to a NoPaperForms tenant, and a high-confidence conclusion that MUJ's admissions process handles substantial identity, academic, document, contact, payment, and workflow data. It supports a high-confidence business-process link between admission verification and SLCM records and credentials.**

**The public evidence does not support a high-confidence claim that NoPaperForms automatically creates SLCM accounts, that the application number equals the SLCM registration number, that Microsoft 365 performs the provisioning, or that a particular API, webhook, SSO assertion, or database feed exists. Those claims are `not publicly documented` in the sources reviewed.**

**Confidence level: High for DNS delegation and publicly documented data categories; high for the admissions-department relationship to SLCM correction; medium for the broader inference that admission outcomes feed or enable SLCM onboarding; low for the exact technical integration mechanism.**

The defensible architecture statement for a university security club is: `MUJ admissions.jaipur.manipal.edu -> public CNAME to jaipurmanipal.nopaperforms.com -> SaaS-hosted admissions and application workflow; admission verification and registration-number/Outlook-based identity are publicly tied to MUJ SLCM, but the system-to-system hand-off is undisclosed.` This statement preserves the observed facts, labels the inference, and avoids exposing applicant information or encouraging unauthorized access.

## References

1. *NoPaperForms | Unified Technology Platform for Education*. https://www.nopaperforms.com/
2. *Manipal University Jaipur Admission 2026-27 | Apply Now! Manipal Academy of Higher Education https://admissions.jaipur.manipal.edu*. https://admissions.jaipur.manipal.edu/
3. *Course Fee*. https://jaipur.manipal.edu/fee-structure.php
4. *ADMISSIONS - Manipal University Jaipur*. http://jaipur.manipal.edu/admissions.php
5. *NoPaperForms Solutions Ltd. - Trust Center - Security & Privacy*. http://trustcenter.nopaperforms.com/
6. *Manipal University*. https://mujslcm.jaipur.manipal.edu
7. *Manipal University Jaipur - 71 years of legacy of Manipal ...*. http://jaipur.manipal.edu/
8. *Privacy & Cookie Policy | MAHE*. http://manipal.edu/mu/important-links/privacy-and-cookie-policy.html
9. *Guidelines on Eligibility Document Verification February - MUJ*. https://muj.onlinemanipal.com/wp-content/uploads/2022/01/MUJ-Admission-Manual-Online-Programmes-V5.pdf
10. *API Documentation*. http://developer.nopaperforms.com/
11. *Login*. https://apply.manipal.edu/
12. *Pay Fee Online - Manipal University Jaipur *. https://www.jaipur.manipal.edu/pay-fee-online.php
13. *Admission Contact - Manipal University Jaipur*. https://www.jaipur.manipal.edu/admission-contact.php
14. *Privacy Policy » Meritto*. https://www.meritto.com/privacy-policy/
15. *ADMISSIONS - Manipal University Jaipur*. https://jaipur.manipal.edu/admissions.php?p=UG
16. *Terms and Conditions | Meritto (Formerly NoPaperForms)*. http://meritto.com/terms-and-conditions
17. *Frequently Asked Questions and Contacts for SLCM Registration*. https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf
18. *dns.google*. https://dns.google/resolve?name=admissions.jaipur.manipal.edu&type=CNAME
19. *dns.google*. https://dns.google/resolve?name=jaipurmanipal.nopaperforms.com&type=A
20. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
