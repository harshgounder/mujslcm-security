# MUJ SLCM Quora Footprint and Safe OSINT Assessment

## Executive Summary

- **Quora evidence is narrow**: The only directly relevant Quora answer that was available in an auditable search result concerns attendance at MUJ. It says attendance was previously uploaded before end-term examinations, but was uploaded and locked within two days in the writer's stated current period. The answer is labelled "Answer (1 of 2)," but the accessible evidence does not expose the author's name, credential, or date. [6] [6] -> Treat this as an unattributed student report, not as an official control description.

- **The official MUJ portal surface is identifiable**: The public MUJ portal page says "WELCOME TO MUJ PORTAL," presents a sign-in path using a MUJ email domain, identifies both Parent Login and Student Login, and exposes a Forgot Password option. [2] A second public hostname presents the same broad portal labels while using a Jaipur Manipal email-domain label. [4] -> Use only institution-published links when documenting the service, and do not assume that two hostnames are interchangeable merely because their page labels resemble one another.

- **The onboarding workflow is more informative than Quora**: An official MUJ onboarding guide says that first-year students receive their SLCM username and password through their personal Gmail account and directs them to the MUJ SLCM URL. [19] [19] -> The security club can document the credential-delivery and recovery lifecycle without requesting or handling anybody's credentials.

- **Parent access is explicitly connected to a verified mobile number**: The official guide says a parent's mobile number is verified by OTP and that completing this step enables Parent login. [19] -> Treat parent linkage as a privacy and authorization boundary in a defensive threat model, not as a route to test or obtain another person's access.

- **Marks and CGPA pages are not presently attributable**: The marks-sharing question is discoverable by URL, but the accessible corpus exposes no question text, answer text, answerer, credential, or date. [17] The CGPA-calculation page is blocked and exposes only an error message in the accessible corpus. [16] -> Do not repeat the commonly implied answer to the marks question or assign it to an author without a retrievable source.

- **Visible Manipal affiliations are not insider proof**: A contextual Quora page displays answerers who describe themselves as MIT or Manipal-affiliated, including Prajay Vats, Harshit Anand, Supriya Prem Kumar, Rohan Krishna, and Nikita Kishore. [3] [3] [3] [3] The page does not provide SLCM login, marks, or portal implementation detail. [3] [3] -> Classify these as affiliation signals only, not as evidence that any person worked on MUJ SLCM or had privileged access.

- **"Manipal portal" is an ambiguous search term**: The official MAHE student-portal page directs users to a separate SIS portal at `sis.manipal.edu/index.aspx`. [10] A separate student-portal page says users with problems should reach their help desk. [8] -> Keep MUJ SLCM, MAHE SIS, and other student-facing portals in separate evidence buckets; otherwise a search result can be attached to the wrong system.

- **The supplied technology description remains unverified here**: The research brief names ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10 behind Akamai, and Microsoft 365 identity. The Quora material and the public page excerpts retrieved for this report do not independently establish those exact versions, deployment components, or identity-provider relationships. The official FAQ's reference to an official Outlook ID is not, by itself, proof of a particular Microsoft 365 authentication architecture. [18] -> Treat the stack description as an analyst-supplied hypothesis until confirmed by authorized, non-invasive documentation.

- **The responsible conclusion is not a vulnerability finding**: The official FAQ publishes support routes, including the university helpline and institutional contacts, while the onboarding guide directs users with technical issues to the University Helpdesk or Admissions Department. [18] [19] -> Use the public material to build a defensive data-flow and privacy checklist; do not enumerate accounts, guess credentials, bypass login, scrape private Quora profiles, or probe the live portal without written authorization.

## Evidence Method and Decision Rationale

I cannot provide private chain-of-thought or hidden internal reasoning. I can provide an auditable evidence-selection summary. I separated the corpus into four classes: official MUJ or Manipal material, directly relevant Quora material, contextual Quora material, and blocked or incomplete pages. I then gave priority to exact page text over search-result titles, treated an indexed snippet as evidence only for the wording it actually displayed, and recorded unavailable fields as unavailable rather than filling them from memory or from a likely-looking answer.

This distinction matters because the Quora pages did not have uniform visibility. The attendance page yielded an answer excerpt, including the answer count and operational wording, but not the answerer's identity. [6] The marks-sharing page yielded a URL but no accessible question or answer fields. [17] The CGPA page returned only an error message. [16] The general "How is manipal university" page likewise returned a temporary error message rather than answer content. [1] A blocked page is evidence of an access limitation in this research collection; it is not evidence that the page has no answers.

The resulting confidence model is deliberately conservative. "High" means the exact URL and visible page label or official instruction are directly supported. "Medium" means the source text is visible but is a self-reported or unattributed claim. "Low" means the requested field is blocked, absent, or requires an inference about a person's identity or technical access. This model prevents a familiar university affiliation from becoming a claim of insider status and prevents a student description of a workflow from becoming a claim about a server-side implementation.

| Evidence class | Exact source URL | What is directly observable | Reliability use in this report |
|---|---|---|---|
| Official MUJ portal | https://mujslcm.jaipur.manipal.edu/ | The page labels the service as MUJ Portal and shows student, parent, and password-recovery sign-in labels. [2] | High for public terminology and entry-point documentation; not evidence of a vulnerability. |
| Official MUJ onboarding guide | http://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf | The guide describes credential delivery, the SLCM URL, parent OTP verification, document upload, and helpdesk escalation. [19] [19] [19] [19] | High for the documented user workflow; not a reason to handle credentials or test the live service. |
| Official MUJ FAQ | http://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf | The FAQ publishes the registration link, login wording, support channels, and a helpline. [18] | High for published support information; login conventions should not be operationalized into guessing attempts. |
| Directly relevant Quora answer | https://www.quora.com/How-is-the-attendance-calculated-at-MUJ | An unattributed answer describes a change in attendance upload and locking timing. [6] | Medium for what the anonymous answer says; low for official status, date, or implementation details. |
| Blocked or incomplete Quora pages | https://www.quora.com/Are-End-Semester-marks-shared-with-parents-at-MUJ and https://www.quora.com/How-is-CGPA-calculated-at-Manipal-University | The URL or page error is visible, but requested answer metadata is not. [17] [16] | High for the limitation; no basis for repeating an inaccessible answer. |

The table's central takeaway is that the strongest evidence answers "what public pages call the service" and "what the institution's own guide tells users to do." The strongest Quora evidence answers only "what one unattributed writer claimed about an attendance process." Those are different propositions and should remain separate in any club presentation.

## MUJ SLCM Ecosystem and Terminology

The most defensible public starting point is the MUJ portal itself. The page title and visible text identify it as the MUJ Portal and show a sign-in interface with a MUJ email-domain label, Parent Login, Student Login, and Forgot Password. [2] This establishes a public user-facing entry point and two visible role categories. It does not establish how the portal implements sessions, how it stores records, or whether the page is served by a particular framework or edge provider.

A second publicly indexed hostname, `https://muj.slcm.jaipur.manipal.edu/`, uses similar page labels and shows Parent Login, Student Login, and Forgot Password. [4] The email-domain label visible in that result differs from the one on the first hostname. [2] [4] That difference is useful for terminology research because it shows why students may use several phrases when describing the same broad service. It is not enough to conclude that the two hostnames share a backend, use the same authentication route, or represent a migration. Those would be inferences and require authorized verification.

The official first-year guide adds lifecycle context. It says that the SLCM username and password are sent to a student's personal Gmail account by Admissions and directs the student to the MUJ SLCM URL. [19] [19] The guide also refers to a Student Details area and to fields pre-filled from admission information or generated by MUJ. [19] This suggests a relationship between the admissions record and the student profile, but it does not expose the database schema or prove that every displayed value is synchronized in real time.

The same guide describes a parent-linkage step. A parent mobile number and email address are entered, the number is verified by OTP, and the guide says that this enables Parent login. [19] The guide also says that mandatory documents are uploaded and that documents will be verified during physical reporting and document verification. [19] [19] These statements provide a useful defensive map: admissions identity, student profile, parent identity, OTP verification, document collection, and later human verification are connected in the published workflow.

The term "Manipal student portal" cannot safely be treated as a unique identifier. The official MAHE student-portal page says users can register and log in to the Student Portal, describes access to web services related to student life, and links to `https://sis.manipal.edu/index.aspx`. [10] A separate MUJ student-portal result says that users facing issues should contact their help desk. [8] The existence of these separate public references means that a Quora search for "Manipal portal" can retrieve content about MAHE, MUJ, SIS, or a campus-specific service rather than MUJ SLCM.

The stack named in the research brief should therefore be treated as an unverified hypothesis in this report. No retrieved Quora excerpt identifies ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, or a Microsoft 365 tenant. The official FAQ does use the phrase "official outlook ID" in its login wording, but that phrase alone does not demonstrate a specific identity-provider configuration. [18] This is an important boundary: a public page can disclose a user-facing label without disclosing the technology that produces it.

| Ecosystem item | Exact URL | Public evidence | Defensive interpretation, explicitly labelled |
|---|---|---|---|
| MUJ SLCM entry point | https://mujslcm.jaipur.manipal.edu/ | MUJ Portal, Student Login, Parent Login, and Forgot Password are visible. [2] | Observation: a role-separated public login surface exists. Inference: role separation should be included in an authorization review, but no flaw is shown. |
| Alternate MUJ-labelled host | https://muj.slcm.jaipur.manipal.edu/ | Similar MUJ portal and role labels are visible. [4] | Observation: more than one public hostname is indexed. Inference: hostname confusion is a documentation and phishing-risk topic, not proof of duplicate systems or a weakness. |
| First-year onboarding | http://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf | Credentials are sent to personal Gmail; the guide names the SLCM URL and profile workflow. [19] [19] | Observation: onboarding depends on an external mailbox. Inference: account-recovery and phishing controls deserve review in an authorized assessment. |
| Parent linkage | Same official guide | Parent mobile verification by OTP enables Parent login. [19] | Observation: parent access is tied to a verification event. Inference: consent, number-change, and revocation handling are important questions. |
| MAHE SIS reference | http://manipal.edu/mu/academics/student-portal.html | The page links to SIS at sis.manipal.edu. [10] | Observation: this is a separate named portal reference. Inference: search results must be scoped by campus and hostname. |

The key ecosystem finding is not that the public material reveals an exploitable technical path. It is that the public terminology exposes several role and lifecycle boundaries that should be documented precisely before any authorized security review begins.

## Quora Question Inventory

The inventory below distinguishes direct MUJ SLCM or student-record questions from broader Manipal questions. It includes exact URLs so a university security club can reproduce the public-source trail without relying on a paraphrase. Where the page was blocked, that status is recorded rather than converted into a claim about the unseen answer.

| Category | Quora question URL | Accessible public material | Answerer or technical detail status |
|---|---|---|---|
| Attendance process, direct MUJ topic | https://www.quora.com/How-is-the-attendance-calculated-at-MUJ | The answer says the attendance system became stricter, that attendance was previously uploaded before end-term exams, and that in the writer's stated current period it was uploaded and locked within two days. [6] | Answerer name, credential, and date are unavailable; the excerpt is operational but unattributed. [6] |
| Marks shared with parents, direct MUJ topic | https://www.quora.com/Are-End-Semester-marks-shared-with-parents-at-MUJ | The URL and question identity are discoverable. [17] | Question text, answer text, answerer, credential, and date are unavailable in the accessible corpus. [17] |
| CGPA calculation, Manipal topic | https://www.quora.com/How-is-CGPA-calculated-at-Manipal-University | The page is identified as a Quora CGPA question, but the accessible page returns an error. [16] | No answer or author can be assessed from the accessible evidence. [16] |
| Maintaining CGPA at MUJ, adjacent academic topic | https://www.quora.com/How-do-I-maintain-my-CGPA-at-MUJ | A search excerpt gives general study advice about interacting with teachers and students and revising subjects. [15] | No SLCM login, marks-access, or portal implementation detail is visible in the excerpt. |
| General university experience | https://www.quora.com/How-is-manipal-university | The accessible page returns "Something went wrong" and a retry message. [1] | No answerer or answer content can be assessed. |
| Administrative procedure | https://www.quora.com/What-is-the-procedure-for-getting-the-MUJ-outpass-signed | The question title is discoverable. [11] | No answer detail or author metadata is accessible in the evidence used here. |
| Choice and experience, adjacent MUJ topic | https://www.quora.com/Which-is-better-CS-at-MUJ-or-CS-at-SRM-KTR | A snippet says the writer chose CSE at MUJ and was proud of the choice after one year. [13] | This is an experience statement, not a portal or records-system answer; author metadata is not visible in the excerpt. |
| Broad institutional criticism | https://www.quora.com/Is-Manipal-University-a-fraud | The page displays multiple profiles and broad institutional opinions, including a profile labelled Prajay Vats and a claim about studying at MIT. [3] | The visible material contains no MUJ SLCM login or portal implementation detail. [3] |

The direct inventory is smaller than the topic list in the research brief. In the accessible search and extraction set, no Quora answer containing the literal hostname `mujslcm.jaipur.manipal.edu` was recovered with both question and answer text. That statement is deliberately limited to this collection and retrieval path; it is not a global claim that no such Quora post exists. Search engines may omit pages, Quora may change visibility, and deleted or login-gated material may not be recoverable.

The most important inventory distinction is between discoverability and evidentiary usability. A title can establish that a question was indexed. It cannot establish what an inaccessible answer said. A search snippet can establish the words displayed in that snippet. It cannot establish the author's true identity, employment, or technical access. This is why the attendance page is usable for a narrowly phrased claim while the marks-sharing and CGPA pages are useful mainly as documented gaps.

## Notable Answer: Attendance Publication and Locking

The attendance question is the only Quora item in this collection with directly visible operational detail tied to MUJ. The answer begins by saying that the attendance system is stricter than in previous years. It contrasts an earlier process, in which attendance was uploaded before end-term examinations and students below 75 percent could negotiate with their respective HOD, with the writer's stated current process, in which attendance was uploaded and locked within two days. [6]

The page excerpt identifies this as "Answer (1 of 2)." [6] That label indicates that at least two answers were represented in the visible result, but the accessible evidence does not provide the second answer's text. More importantly for attribution, the same extraction explicitly reports that the answerer's name, credential, and date are unavailable. [6] Any report that assigns this statement to a specific student would therefore be inventing attribution.

This answer is notable because it gives a concrete process claim rather than a general opinion. It describes an apparent change in the timing of data publication and the point at which the record becomes locked. That is relevant to a defensive control discussion: a university system that publishes a student-facing attendance result and later prevents routine changes has a publication window, a change-control boundary, and likely an escalation path. Those last three items are an analyst's abstraction from the wording, not facts disclosed by the Quora author.

**Inference label:** The phrase "uploaded and locked" may describe an administrative rule, a workflow status, or a user-facing portal behavior. It does not prove that a database record is immutable, that a particular controller or API performs the lock, or that any bypass exists. The answer does not mention a URL path, software version, request format, database, role token, or authentication mechanism. [6] The safe conclusion is therefore about perceived process timing, not implementation.

The answer also contains a time-relative phrase, "from this year," without a visible calendar year or answer date. [6] That makes it unsuitable as a current policy statement. A club presentation can quote it as an undated historical or contemporaneous student report, but should verify the current attendance policy through official university channels before using it to brief students or auditors.

**Case study: an unattributed process report.** The attendance page illustrates both the value and the danger of OSINT. Its two-day statement is useful because it reveals what a user noticed: a tighter publication and locking rhythm. It may help a club formulate authorized questions about audit logs, correction approvals, notification timing, and dispute handling. It is dangerous if treated as a technical finding, because the identity and date are unavailable and the answer does not explain whether "lock" is literal immutability or a policy status.

The appropriate security-club output is a control checklist, not a test recipe. Ask the authorized system owner whether attendance changes are logged, whether corrections require a role-separated approval, whether students receive a timestamped publication notice, whether parent-visible data follows the same release rule, and how disputes are handled. Do not attempt to alter a live attendance record, infer an endpoint from the wording, or use the answer as justification for probing the service.

| Question raised by the Quora answer | What the source supports | What remains inference or unanswered | Safe club treatment |
|---|---|---|---|
| Was attendance published earlier before end-term examinations? | The anonymous answer says it was uploaded before end-term examinations in an earlier period. [6] | The period and official policy document are not identified. | Ask the owner for historical policy and publication records; do not present the Quora statement as policy. |
| Was a 75 percent threshold relevant? | The answer refers to students falling below 75 percent. [6] | The answer does not establish the current official threshold or consequences. | Verify through current official academic rules; do not infer enforcement logic. |
| Was the record locked within two days? | The answer says it was uploaded and locked within two days in the writer's stated current period. [6] | The event, clock, timezone, role, and technical meaning of lock are unknown. | Review authorized audit and change-control documentation only. |
| Who made the statement? | The page is labelled Answer (1 of 2). [6] | Name, credential, date, and profile are unavailable. [6] | Attribute it only to an unidentified Quora answer. |

The takeaway is precise: this is a useful lead about perceived attendance operations and a poor basis for a claim about system architecture, current policy, or exploitable behavior.

## Login, Marks, CGPA, and Student-Portal Problems

The marks-sharing question is highly relevant to the requested focus because it directly asks whether end-semester marks are shared with parents at MUJ. The exact URL is recoverable, but the accessible corpus exposes no question text, answer text, answerer name, credential, or date. [17] That means the report cannot responsibly say "the answer was no," "the answer was yes," or identify who supposedly answered it. If a search preview outside this evidence set appears to show an answer, it should be preserved as a separate source capture before being quoted; it should not be reconstructed from a remembered snippet.

The CGPA-calculation page has a similar problem. The accessible extraction says that the Quora page is blocked and only an error message is available. [16] The adjacent question about maintaining CGPA at MUJ is more visible, but its excerpt is generic study advice: interact with teachers and good students, clear doubts, and revise each subject. [15] It does not describe a login failure, a marks endpoint, an SLCM screen, or a records-access procedure. It is therefore contextual academic content, not technical evidence.

The general "How is manipal university" page also cannot be used to answer the portal question. Its accessible output is only a failure message asking the visitor to wait and try again. [1] The outpass question is discoverable by title, but the available evidence contains no answer details. [11] These pages demonstrate why a broad search for "Manipal problems" is noisy: a university experience, a hostel or administrative question, an academic advice answer, and a portal problem may all be indexed under the same brand terms.

The practical research gap is therefore not merely "more answers are needed." It is specifically the absence of three fields: answer content, answerer identity, and date. Without all three, the club cannot establish whether a writer was a current MUJ student, an alumnus, a parent, a staff member, or an unrelated commentator. It also cannot tell whether a marks statement referred to end-semester marks, internal marks, a parent portal, or an informal teacher communication channel.

The official material provides a safer comparison point. The MUJ portal visibly includes separate Parent Login and Student Login labels and a Forgot Password option. [2] The onboarding guide says that parent access becomes enabled after mobile OTP verification. [19] Those are documented workflow facts. They do not answer the Quora marks question, but they do show why a marks-sharing question has a privacy dimension: a parent-facing role can exist without the public evidence here establishing which fields that role can view.

**Case study: marks question versus attendance answer.** The attendance page exposes a detailed but unattributed process description. The marks page exposes a relevant question identity but no answer content at all. The contrast shows that topic relevance is not the same as evidentiary strength. A marks question may be more directly tied to confidentiality than the attendance answer, yet it is currently less useful for factual reporting because the answer cannot be inspected.

| Research target | Exact URL | Evidence strength | What can be reported safely |
|---|---|---|---|
| Parent visibility of end-semester marks | https://www.quora.com/Are-End-Semester-marks-shared-with-parents-at-MUJ | Question URL visible; answer fields unavailable. [17] | The question was discoverable; the answer and author's position are not reportable from this corpus. |
| CGPA calculation | https://www.quora.com/How-is-CGPA-calculated-at-Manipal-University | Page blocked. [16] | The page was not readable in the accessible collection. |
| CGPA maintenance advice | https://www.quora.com/How-do-I-maintain-my-CGPA-at-MUJ | Generic study-advice snippet visible. [15] | It is adjacent academic advice, not SLCM or marks-access evidence. |
| General university experience | https://www.quora.com/How-is-manipal-university | Error message only. [1] | No answerer or substantive answer can be assessed. |
| MUJ outpass process | https://www.quora.com/What-is-the-procedure-for-getting-the-MUJ-outpass-signed | Title visible. [11] | The existence of an administrative question is visible; the procedure is not established here. |

This section's conclusion is intentionally negative: no accessible Quora answer in the collected evidence establishes how MUJ SLCM exposes marks, whether parents receive end-semester marks, how CGPA is calculated in the system, or how a student should repair a login failure. The right next step is official documentation or consent-based interviews, not speculation.

## Answerer Signals and Insider-Likelihood Assessment

The strongest answerer question is not "does this person sound confident?" It is "does the public evidence establish a relevant relationship, first-hand observation, technical specificity, and a date that can be checked?" On that standard, the attendance answerer cannot be assessed because the name, credential, and date are unavailable. [6] The anonymous writer may have been a student or another participant, but that is an inference and must remain labelled as such.

A contextual Quora page does expose several profile labels. Prajay Vats is displayed with a self-described BTech in Information Technology from Manipal Institute of Technology and a 2021 graduation label. [3] The same page contains broad claims about being forced to take admission, being held hostage, and bank accounts being hacked. [3] Those statements are subjective user claims and are not independently verified here. They do not mention MUJ SLCM, a portal hostname, an authentication event, or a reproducible technical observation. The profile therefore provides an affiliation signal but not an insider signal for this assignment.

Harshit Anand is displayed as having studied at Manipal Institute of Technology. [3] Supriya Prem Kumar is displayed as living in Bengaluru and the page attributes broader comments about MAHE programs, foreign-university ties, faculty, and support staff to that answer context. [3] [3] Rohan Krishna is displayed as having studied at Manipal Institute of Technology. [3] Nikita Kishore is displayed with a BTech-from-MIT profile label. [3] These labels may indicate familiarity with some part of the Manipal ecosystem, but the accessible page does not tie those people to MUJ SLCM operations.

The page also contains a health-card and medical-facility comment, but the accessible evidence does not connect that comment to portal administration or SLCM access. [3] This is another reminder that institutional familiarity can coexist with no relevant technical knowledge. A person can be a real student or alumnus and still be unable to speak authoritatively about identity, authorization, data retention, or server configuration.

**Inference label:** The phrase "sounds like an insider" is a weak OSINT category. At most, the visible profile labels create a low-confidence possibility of student or alumni experience. They do not prove current enrollment, staff employment, privileged access, direct observation of source code, or access to administrative functions. No person in the retrieved Quora material meets all four stronger criteria: attributable identity, MUJ SLCM-specific first-hand detail, technical specificity, and independently corroborated timing.

| Person or author signal | Publicly visible affiliation or content | SLCM relevance | Insider-likelihood assessment |
|---|---|---|---|
| Unnamed attendance answerer | Describes attendance upload and locking timing. [6] | Directly relevant process detail. | Low confidence for identity and insider status because name, credential, and date are unavailable. |
| Prajay Vats | Profile label says BTech in IT at MIT, graduated 2021. [3] | The visible answer contains broad institutional allegations, not SLCM detail. [3] | Low. Alumni-style affiliation is not privileged-access evidence. |
| Harshit Anand | Profile label says studied at MIT. [3] | No accessible MUJ SLCM implementation detail. | Low. Contextual affiliation only. |
| Supriya Prem Kumar | Profile label says lives in Bengaluru; answer context discusses MAHE programs and support. [3] [3] | No direct MUJ SLCM detail. | Low. General institutional familiarity is not system ownership. |
| Rohan Krishna | Profile label says studied at MIT. [3] | No accessible SLCM detail. | Low. Affiliation signal only. |
| Nikita Kishore | Profile label says BTech from MIT. [3] | No accessible SLCM detail. | Low. No corroborated technical or operational evidence. |

The answerer finding is therefore clear. The collection contains people who may have educational or institutional connections, but it does not contain a confirmed MUJ SLCM insider. The club should not contact these individuals seeking confidential information, and it should not publish their names as suspected insiders. If future public evidence reveals a named answerer, the club should still distinguish self-described affiliation from verified role and should avoid unnecessary personal profiling.

## Security Interpretation and Responsible Handling

The public material supports a defensive threat model focused on workflow boundaries rather than exploit paths. The official FAQ publishes the SLCM registration link and a user-facing username and password convention, including a reference to an official Outlook ID. [18] The first-year guide says credentials are sent to a personal Gmail account. [19] Together, those statements show that the public documentation discusses account onboarding and credential delivery. They do not provide permission to infer a student's credentials, test a login, or attempt password recovery against a live account.

The parent workflow deserves separate treatment. The guide says a parent's mobile number is verified by OTP and that this enables Parent login. [19] **Inference:** this creates a relationship between a student record, a parent contact channel, and a role-bearing login. A defensive review should therefore ask how a changed phone number is reverified, how a mistaken parent link is revoked, whether a student can see the status of the link, and whether parent access is limited to the intended records. None of those questions implies that a weakness exists.

The document workflow is another public boundary. The guide says required documents are uploaded, that mandatory files have format and size requirements, and that uploaded documents are verified during physical reporting. [19] [19] **Inference:** this creates confidentiality, integrity, and retention questions around personally identifying documents. A club can recommend that an authorized owner document file-type validation, malware scanning, access logging, retention, and staff review. It should not upload test files or inspect other students' documents without a written test authorization and a controlled account.

The attendance answer contributes a process-integrity hypothesis. It says attendance is uploaded and locked within two days in the writer's stated current period. [6] **Inference:** if a similar rule is official, it would be relevant to release timing, correction approval, and auditability. The source does not establish the implementation. The safe activity is to request policy and sample audit records from the owner, not to try to change, replay, or bypass a lock.

The two public hostnames create a documentation issue. The main public result uses `mujslcm.jaipur.manipal.edu` and labels a MUJ portal with parent and student sign-in. [2] Another result uses `muj.slcm.jaipur.manipal.edu` with similar labels. [4] **Inference:** multiple public-looking entry points can increase the risk of user confusion or impersonation, especially if students receive links through informal channels. This is not evidence that either hostname is malicious or misconfigured. The defensive response is to publish a canonical-link policy and to direct students to institution-controlled support.

The official sources give a responsible reporting route. The FAQ lists a university helpline and institutional contacts, including Admissions, DMS, Academic Section, and IT support. [18] The onboarding guide tells users with technical issues or queries to contact the University Helpdesk or Admissions Department. [19] The portal page itself exposes Forgot Password. [2] A university security club should use these channels for suspected account or privacy issues and should preserve only the minimum public evidence needed to describe the problem.

| Publicly visible surface | Evidence | Defensive question, labelled as a question rather than a finding | Prohibited or unsafe interpretation |
|---|---|---|---|
| Credential delivery | The guide says credentials are sent to personal Gmail. [19] | Are delivery, recovery, expiry, and phishing protections documented? | Do not obtain, guess, or test another person's credentials. |
| Parent OTP link | Parent mobile verification enables Parent login. [19] | How are consent, number changes, revocation, and role scope handled? | Do not attempt to trigger or intercept OTPs. |
| Document upload | Mandatory documents are uploaded and later verified. [19] [19] | Are validation, access logs, retention, and staff review controlled? | Do not upload unapproved test material or access other records. |
| Attendance lock report | An anonymous answer says attendance is locked within two days. [6] | Is there an official policy, audit trail, and correction workflow? | Do not probe or attempt to alter live attendance data. |
| Role-separated login | Portal page shows Parent Login, Student Login, and Forgot Password. [2] | Are role boundaries and recovery processes tested in an authorized environment? | Do not enumerate users or use recovery as an access experiment. |
| Hostname choice | Two MUJ-labelled public hostnames are indexed. [2] [4] | Which link is canonical and how are redirects and user communications governed? | Do not infer that one host is a test or bypass endpoint. |

This approach preserves the value of OSINT while preventing the report from becoming an access guide. It also keeps the distinction between a design question and a confirmed security defect, which is essential when the public evidence comes from an anonymous social-media answer.

## Gaps, Corroboration, and Limitations

The largest gap is Quora page visibility. The marks-sharing page has no accessible answer fields. [17] The CGPA-calculation page is blocked. [16] The general university page returns an error and retry message. [1] These outcomes limit attribution and prevent a reliable comparison of competing answers. They do not prove that Quora has no answer, that the answer was deleted, or that the topic was never discussed.

The second gap is temporal context. The attendance answer says "from this year" but the accessible material gives no calendar year or author date. [6] A time-relative statement cannot safely be used as the current MUJ attendance policy. It may describe a past academic year, a particular program, or the writer's own interpretation of a portal event. Official current documentation is required before publication as policy.

The third gap is independent corroboration. The retrieved Quora answer is not corroborated by an official MUJ attendance-policy excerpt in the evidence set used for this report. The official onboarding and FAQ sources corroborate portal naming, support channels, account onboarding, parent OTP, and document verification, but they do not corroborate the two-day attendance-lock claim. [18] [19] [19] This difference should be stated plainly rather than hidden under a general citation to the university website.

The fourth gap is technical attribution. None of the relevant Quora excerpts identifies ASP.NET MVC, .NET Framework, IIS, Akamai, a Microsoft 365 tenant, a controller, an API, or a database. The public portal labels show a user interface, not a stack fingerprint. The official Outlook wording in the FAQ is a user-facing instruction and does not independently verify the identity architecture. [18]

The fifth gap is answerer identity. The attendance answerer is explicitly unavailable. [6] The contextual profiles show Manipal-related labels, but no SLCM-specific expertise. [3] [3] [3] This prevents an insider-likelihood conclusion stronger than low confidence.

| Limitation | Direct evidence | Effect on the report | Required handling |
|---|---|---|---|
| Quora anti-bot or access failure | Error and retry output on multiple pages. [1] [16] | Full answers and metadata cannot be audited. | Say "not accessible in this collection," not "no answer exists." |
| Unattributed attendance answer | Name, credential, and date unavailable. [6] | Cannot assess current student status or authority. | Attribute only to an unnamed Quora answer. |
| Undated relative claim | "From this year" appears without a visible calendar date. [6] | Currentness cannot be established. | Verify with current official policy. |
| Marks answer unavailable | All requested fields unavailable. [17] | No conclusion about parent visibility of marks. | Do not reproduce a remembered or third-party paraphrase. |
| Architecture not disclosed | Public excerpts show portal labels and workflow, not stack components. [2] [19] | Supplied version and provider claims remain unverified. | Treat them as hypotheses pending authorized confirmation. |

The limitation analysis is itself decision-relevant. It identifies exactly what the club can repeat, what it can use as a lead, and what it must leave unresolved. That is more useful than inflating a thin public footprint into an unsupported narrative.

## Synthesis

The evidence separates into five strategies with different mechanisms, scope, trade-offs, and time horizons. Official portal pages are best for naming the public surface. Official onboarding and FAQ documents are best for declared workflow and support. Quora is useful for user perception and process anecdotes. Contextual profiles can suggest affiliation but cannot establish access. Blocked pages show research uncertainty rather than substantive answers.

| Evidence type | Mechanism of knowledge | Scope | Main trade-off | Time horizon and confidence |
|---|---|---|---|---|
| Official portal page | Institution-published user interface labels. [2] | Public entry point and role names. | Strong terminology, little implementation detail. | Current-looking surface, high confidence for labels. |
| Official FAQ and guide | Institution-published instructions and contacts. [18] [19] | Onboarding, parent OTP, documents, support. | Describes intended process, not necessarily every production behavior. | Policy or onboarding context, high confidence for what is written. |
| Anonymous attendance answer | User-reported observation. [6] | One process claim about upload and locking. | Specific detail but no identity, date, or official corroboration. | Historical or time-relative, medium confidence as a reported statement. |
| Contextual Quora profiles | Self-described education or institutional familiarity. [3] [3] | Broad university discussion. | Human context without SLCM specificity. | Unknown, low confidence for insider status. |
| Blocked Quora pages | URL or error response. [17] [16] [1] | Establishes discoverability or access limitation. | Cannot inspect answer or attribution. | No substantive confidence about unseen content. |

The first non-obvious tension is between operational specificity and attribution. The attendance answer is more technically useful than a generic university opinion, yet it is less attributable than the contextual profiles. The second tension is between official completeness and implementation uncertainty. The guide gives a detailed onboarding sequence, including parent OTP and document verification, but it does not reveal whether the live system always behaves exactly as documented. The third tension is between brand unity and system identity. "Manipal portal" covers more than one public reference, including the MAHE SIS link, so search relevance does not guarantee system identity. [10]

The comparative implication is that no single source class answers the entire research question. A defensible club briefing should combine the official portal and guide for the intended data flow, the attendance answer for a clearly labelled user-reported concern, and the blocked-page record for uncertainty. It should not use profile labels to infer insider access or use an inaccessible marks answer to fill a privacy conclusion.

**Case study contrast: attendance versus parent marks.** Attendance gives a visible claim about timing and locking but no named speaker. Parent marks gives a highly relevant question but no visible answer. The former is a lead for integrity and auditability review; the latter is a lead for privacy and role-scope review. Neither is a vulnerability report. The correct synthesis is to ask the system owner for current policy, role matrix, audit evidence, and correction workflows, then to test only in a written-authorized environment.

For decision-makers, the public record supports three actions. First, publish one canonical MUJ SLCM link and a clear support route. Second, document student, parent, admissions, academic, and helpdesk data flows, including OTP and recovery. Third, preserve the Quora attendance statement as an anonymous lead and verify it through current official policy rather than through live experimentation. The supplied stack description can inform a future authorized scope document, but it should not be presented as independently verified by this OSINT collection.

## VERDICT

**Overall confidence: medium for the public portal and workflow description; low for Quora attribution, marks/CGPA answers, insider identification, and the supplied technical stack.**

The public Quora footprint recovered here is thin but not empty. One directly relevant question has an accessible answer with a concrete, student-facing claim about attendance publication and locking. [6] [6] That claim is useful as an OSINT lead, but its author, date, authority, and technical meaning are unavailable. The marks-sharing question is discoverable but substantively inaccessible. [17] The CGPA and general university pages are blocked or error-only. [16] [1]

No retrieved Quora answerer can be confirmed as a MUJ SLCM insider. The contextual profiles show Manipal-related self-descriptions, but the corresponding visible material does not provide portal-specific technical detail. [3] [3] [3] The correct label is **no confirmed insider evidence**, not "no insiders exist."

The official sources establish a more reliable baseline: MUJ Portal terminology, Student and Parent Login labels, password recovery, credential delivery through the documented onboarding process, parent OTP linkage, document verification, and institutional support channels. [2] [18] [19] [19] [19] They do not independently verify the exact ASP.NET MVC, .NET Framework, IIS, Akamai, or Microsoft 365 claims supplied in the brief.

| Finding | Confidence | Reason |
|---|---|---|
| MUJ SLCM public URL and portal labels | High | Direct official page text is accessible. [2] |
| Parent and student role labels | High | Both roles are visibly named on the official portal page. [2] |
| Onboarding, personal-Gmail delivery, parent OTP, and document workflow | High for the written guide | These are stated in the official guide; live implementation is not independently tested. [19] [19] [19] |
| Attendance upload and two-day lock statement | Medium | The answer text is visible, but it is anonymous, undated, and uncorroborated. [6] [6] |
| Parent visibility of end-semester marks | Low or unresolved | The question URL is visible but all requested answer fields are unavailable. [17] |
| CGPA calculation answer | Low or unresolved | The page is blocked in the accessible corpus. [16] |
| Confirmed MUJ SLCM insider | Low and unsupported | No relevant answerer identity and no portal-specific profile evidence were recovered. [6] [3] |
| Exact stack and edge-provider description | Low and unverified in this collection | User-supplied description is not independently established by the retrieved excerpts. |

**Final decision:** Use the report as a public-source evidence register and a defensive scoping document, not as an exploitation guide. The most credible next step is authorized corroboration with MUJ's published support or security contacts and, if approved, a controlled review of role separation, credential lifecycle, parent-link authorization, document handling, attendance change control, and audit logging. Do not attempt unauthorized access, credential guessing, OTP manipulation, endpoint discovery, or private-profile investigation.

## References and Exact URLs

| Corpus citation used in report | Exact URL | Source role |
|---|---|---|
| [2] | https://mujslcm.jaipur.manipal.edu/ | Official MUJ portal landing page and public sign-in labels. |
| [4] | https://muj.slcm.jaipur.manipal.edu/ | Alternate MUJ-labelled portal hostname visible in public indexing. |
| [18] | http://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf | Official MUJ SLCM FAQ and support information. |
| [19], [19], [19], [19], [19] | http://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf | Official first-year SLCM onboarding and profile guide. |
| [10] | http://manipal.edu/mu/academics/student-portal.html | Official MAHE student-portal page and SIS link. |
| [8] | https://student.mujonline.com/ | MUJ student-portal result with helpdesk wording. |
| [6], [6] | https://www.quora.com/How-is-the-attendance-calculated-at-MUJ | Directly relevant Quora attendance question and accessible answer excerpt. |
| [17] | https://www.quora.com/Are-End-Semester-marks-shared-with-parents-at-MUJ | Directly relevant marks-sharing question; answer fields unavailable. |
| [16] | https://www.quora.com/How-is-CGPA-calculated-at-Manipal-University | CGPA question; page blocked in the accessible corpus. |
| [15] | https://www.quora.com/How-do-I-maintain-my-CGPA-at-MUJ | Adjacent academic-advice question and generic study snippet. |
| [1] | https://www.quora.com/How-is-manipal-university | General university page; error-only accessible output. |
| [11] | https://www.quora.com/What-is-the-procedure-for-getting-the-MUJ-outpass-signed | Administrative question title. |
| [13] | https://www.quora.com/Which-is-better-CS-at-MUJ-or-CS-at-SRM-KTR | Adjacent MUJ experience snippet. |
| [3], [3] | https://www.quora.com/Is-Manipal-University-a-fraud | Contextual Quora page with broad opinions and visible profile labels. |
| [3] | https://www.quora.com/profile/Prajay-Vats | Profile URL visible from the contextual Quora page. |
| [3] | https://www.quora.com/profile/Harshit-Anand-7 | Profile URL visible from the contextual Quora page. |
| [3] | https://www.quora.com/profile/Supriya-Prem-Kumar | Profile URL visible from the contextual Quora page. |
| [3] | https://www.quora.com/profile/Rohan-Krishna-9 | Profile URL visible from the contextual Quora page. |
| [3] | https://www.quora.com/profile/Nikita-Kishore-1 | Profile URL visible from the contextual Quora page. |

All conclusions above are limited to publicly visible material and explicitly identified inferences. The report does not claim that blocked pages contain no answers, that a profile affiliation grants privileged access, or that any public workflow description demonstrates a vulnerability.

## References

1. *Quora - A place to share knowledge and better understand the ...*. https://www.quora.com/How-is-manipal-university
2. *muj portal - Manipal University*. https://mujslcm.jaipur.manipal.edu/
3. *Is Manipal University a fraud? - Quora*. https://www.quora.com/Is-Manipal-University-a-fraud
4. *Manipal University*. https://muj.slcm.jaipur.manipal.edu/
5. *Why is Manipal, a university town based in Karnataka ... Quora 30+ answers · 13 years ago*. https://www.quora.com/Common-Misconceptions-Why-is-Manipal-a-university-town-based-in-Karnataka-widely-believed-to-exist-somewhere-in-the-North-Eastern-frontiers-of-India
6. *How is the attendance calculated at MUJ?*. https://www.quora.com/How-is-the-attendance-calculated-at-MUJ
7. *Quora*. https://www.quora.com/I-got-MUJ-IT-with-my-boards-marks-this-year-But-I-want-to-take-a-drop-year-Should-I-take-a-drop-Will-I-get-the-same-branch-next-year-in-MUJ-with-my-board-marks
8. *Student Portal*. https://student.mujonline.com/login
9. *Examination - Manipal University Jaipur*. https://www.jaipur.manipal.edu/examination.php
10. *Student Portal Login- MAHE (Manipal Academy Of Higher ...*. http://manipal.edu/mu/academics/student-portal.html
11. *What is the procedure for getting the MUJ outpass signed?*. https://www.quora.com/What-is-the-procedure-for-getting-the-MUJ-outpass-signed
12. *I got a 90/200 in the Manipal Entrance Exam. What rank ... Quora 6 answers · 11 years ago*. https://www.quora.com/I-got-a-90-200-in-the-Manipal-Entrance-Exam-What-rank-can-I-expect-and-what-stream-will-I-get
13. *Which is better, CS at MUJ or CS at SRM KTR?*. https://srmuniversity.quora.com/Which-is-better-CS-at-MUJ-or-CS-at-SRM-KTR
14. *Quora*. https://www.quora.com/How-was-your-experience-with-online-Manipal-University-for-an-MBA
15. *How to maintain my CGPA at MUJ - Quora*. https://www.quora.com/How-do-I-maintain-my-CGPA-at-MUJ
16. *How is CGPA calculated at Manipal University? - Quora*. https://www.quora.com/How-is-CGPA-calculated-at-Manipal-University
17. *Are End- Semester marks shared with parents at MUJ? - Quora*. https://www.quora.com/Are-End-Semester-marks-shared-with-parents-at-MUJ
18. *Frequently Asked Questions and Contacts for SLCM Registration*. http://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf
19. *Manipal University Jaipur First-Year Student Profile Registration Guide*. http://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf
