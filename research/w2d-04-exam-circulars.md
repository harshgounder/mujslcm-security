# Public MUJ Exam Artifacts and a Safe SLCM Risk Map

## Executive Summary

- **Published Process Spine**: MUJ publicly publishes an examination landing page, a Student Examinations Handbook, an Examination Manual, application-format material, and multiple timetable PDFs. The practical action is to use those documents as the club's baseline corpus, not to infer undocumented portal behavior from filenames or URLs [4] [4] [4].
- **Make-Up Terminology**: The public handbook states that students receiving F or I in an ETE may take a make-up examination, and that an immediate preceding-semester make-up is conducted after the relevant results. The action is to search and communicate using MUJ's documented "make-up" terminology rather than treating "back paper" as a separately confirmed workflow [10].
- **Grade-Change Control Point**: The Examination Manual says evaluated marks are uploaded to AMS/DMS, initial grades are calculated there, and Grade Moderation Committees may modify grade boundaries before approvals and result notification. The action is to model this as a controlled results lifecycle, not as evidence that students can directly edit marks [11] [11].
- **Hall-Ticket Evidence Gap**: The handbook requires an authentic identification card or exam hall ticket, with a temporary departmental or student-welfare ID as the stated exception, but the reviewed public corpus contains no separate hall-ticket template or field specification. The action is to record the format as unknown rather than inventing fields [10] [4].
- **Timetable Exposure**: MUJ's public timetable links expose faculty or programme groupings, semester labels, exam dates, time slots, course names, and course codes. The action is to treat these as low-sensitivity public scheduling metadata while checking that PDFs do not accidentally expose student-level data [7] [9].
- **Result Timing**: The Student Examinations Handbook states that results are declared within 15 days after grade moderation and approvals, while the 2026 grievance notification gives a 15-day window to appeal a USGRC decision to the Ombudsperson. These are different clocks; the action is not to describe either as a general revaluation deadline [10] [6].
- **Grievance Route**: MUJ's public grievance page links an online submission form, the UGC Samadhaan portal, and the University Students Grievance Redressal Committee document. The action is to direct a genuine exam or result complaint through those official channels rather than attempting to discover a portal update route [2].
- **Dispute Evidence Boundary**: The public searches reviewed for marks disputes did not produce a reliable, attributable MUJ student case that can support a claim of marks tampering, a recurring update defect, or a specific backend path. The action is to report the evidence gap plainly and avoid turning generic result pages or unverified social comments into incident evidence.
- **Portal Boundary**: The SLCM landing page visibly says "WELCOME TO MUJ PORTAL," "Sign In," and "Sign In Parent Login," but the public landing page does not expose exam links or a version statement. The action is to separate the portal's visible identity from the examination website and PDF evidence [1].
- **Stack Attribution**: ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 identity are supplied as the research brief's scope labels, not independently established findings in the cited passive corpus. The action is to mark them as unverified in a public report and never present them as a confirmed vulnerability condition.

## Scope, Evidence Standard, and Auditable Reasoning

This report answers the question using public pages and documents only. It does not log in, submit forms, enumerate accounts, alter parameters, probe routes, inspect authenticated responses, test object references, or attempt to reproduce a marks update. The SLCM hostname is treated as a public landing page, not as permission to access student records. This boundary matters because the public evidence describes process and document flows, while it does not grant authorization to test the underlying application.

The requested explicit chain-of-thought is handled as an auditable reasoning summary rather than private hidden reasoning. The reproducible chain is: identify a public artifact, quote only what the artifact states, distinguish an explicit process fact from a cautious inference, identify what the artifact does not state, and recommend a safe control or official channel. This makes the conclusion reviewable without exposing private internal deliberation.

| Evidence class | Public source | What it establishes | What it does not establish |
|---|---|---|---|
| Institutional process | MUJ examination page and Student Examinations Handbook | Named examination documents, assessment stages, notice lead time, make-up language, result timing [4] [10] [10] | A live portal endpoint, API, database schema, or student permission |
| Operational control | MUJ Examination Manual and Appendix I | Marks-list handling, AMS/DMS upload, grade moderation, answer-book and attendance controls [11] [12] | That any student or unauthorised user can change those records |
| Public schedule | MUJ timetable PDFs and academic calendar | Dates, slots, programmes, courses, codes, and milestone labels [4] [3] [7] | Student-specific hall tickets, room allocations, or current 2026 timetable files |
| Complaint governance | MUJ grievance page and 26 June 2026 USGRC notification | Online route, school-level escalation, USGRC report timing, and Ombudsperson appeal timing [2] [6] | An exam-specific revaluation deadline or proof of a particular marks dispute |
| Portal surface | Public SLCM landing page | Portal name and sign-in or parent-login labels [1] | Framework version, identity implementation, authenticated functions, or security posture |

The evidence is strongest for published rules and weakest for incident claims. The 2023-24 handbook is useful for the documented student exam lifecycle, but it is not silently treated as a current 2026 rule. Conversely, the June 2026 grievance notice is current enough to describe the published grievance governance located in this review, but it does not retroactively prove that every older examination document remains unchanged. The official page's retrieved timetable links are dated April-May 2025, May 2025, or December 2024, while the separate 2026-27 calendar supplies milestone labels; that difference is reported rather than smoothed over [4] [3].

## 1. The Public Examination Process Spine

The official examination page is the central public index. It names a downloadable Student Examination Handbook for Academic Year 2023-24, an Examination Manual with a manual exam-process component and appendices, and an Application Formats area [4]. The same page records a Make Up Application at Rs 1000 per course and says that an online form is submitted after notification, but it does not display a separate make-up URL in the retrieved content [4]. This is important: the public process is announcement-gated in the material reviewed, not documented as an openly listed, permanent student endpoint.

The handbook says examination conduction and grade awarding are a decentralised process under the Controller of Examinations. It describes a common evaluation scheme involving Mid Term Examination, Class Work Sessionals, and End Term Examination for the stated programmes, and says MTE and ETE follow the Annual Academic Calendar [10]. Programme or course-wise schedules are to be informed at least one week before examinations by the relevant department or the Office of the Controller of Examinations [10]. These provisions establish a public process spine: calendar, programme or course schedule, examination, evaluation, moderation, and result.

The application-format evidence is narrower than the phrase "exam form process" might suggest. The public page visibly has an Application Formats heading and an application-form download reference, but the retrieved content does not identify a separate student-facing result form, revaluation form, correction form, or permanent make-up URL [4] [4]. The handbook does mention a malpractice case registration form, but that is an examination-integrity record, not evidence of an ordinary exam-registration form [10]. A responsible analyst should therefore distinguish three things: a named public document, a form mentioned inside a rule, and a live workflow that has not been published.

**Case study: the 2023-24 handbook as a process contract.** The decision documented by MUJ is to communicate the programme or course schedule before the exam, conduct the examination under CoE supervision, and process results after moderation and approvals. The outcome visible to a public reader is a set of rules and named records, not a set of portal routes. This reveals that the official documents are better evidence for business controls and lifecycle states than for application-layer implementation.

For a university security club, the safe research value is to build a document map: source title, academic year, event type, stated audience, date, and whether the link is a PDF or a page. The club should then compare future public revisions against that map. It should not turn an application-form label into a guessed controller name, an uploaded PDF into a guessed database object, or a public notification into permission to submit a test record.

## 2. Hall Tickets, Identity Checks, and Eligibility

The public evidence confirms that hall-ticket and identity requirements exist, but it does not reveal a complete hall-ticket format. The handbook names the non-availability of an authentic identification card or exam hall ticket as an examination violation, with an exception for a temporary ID issued by the department or the Directorate of Student Welfare [10]. It also names carrying another student's ID card to take one's own examination as prohibited conduct [10]. The same handbook prohibits books, notes, written material, phones, programmable calculators, and other listed devices or materials in the examination hall [10]. These are conduct controls, not a public template.

Eligibility is more specific. The handbook states that UG students must secure at least 35 percent in the ETE and overall for a passing grade in a theory course, while PG students must secure 40 percent in the ETE and overall [10]. A student who is eligible but does not appear in the end-semester examination receives F, while a student who cannot appear for valid reasons, including medical, non-payment of dues, or family reasons as stated, receives I [10]. A student barred by minimum-attendance requirements receives DT and must re-register for the course at the next available opportunity [10].

| Student-facing condition | Explicit public treatment | Evidence limit | Safe interpretation |
|---|---|---|---|
| Authentic ID or hall ticket unavailable | Treated as a violation, except for a prescribed temporary ID [10] | No public visual template or field list found | Hall-ticket existence is confirmed; exact format remains unknown |
| Eligible but absent from ETE | F grade [10] | The excerpt does not publish a portal state name | A result state is documented; a database value is not |
| Valid reason for missing ETE | I grade, subject to the stated conditions [10] | No public student submission endpoint is supplied | Follow the official department or CoE process |
| Attendance minimum not met | DT and course re-registration [10] | No public re-registration screen is shown | Do not infer a self-service re-registration route |
| MTE missed for medical reason | Re-MTE may be conducted if authorities were informed before the exam [10] | No public Re-MTE form URL is listed | Treat this as a rule and notification process |

**Case study: a hall-ticket decision is visible, but the document is not.** MUJ's published choice is to make identity a gate to examination entry and to permit a narrowly described temporary-ID exception. The outcome available to an OSINT researcher is a control statement, not a sample ticket. This reveals a useful negative finding: the public corpus supports testing the completeness of future publication hygiene, but it does not support reconstructing a ticket's fields.

The official examination page's retrieved application and schedule content does not show a separate hall-ticket template, and it likewise does not show a result, revaluation, or correction form [4]. That absence is not proof that no ticket exists behind authentication or that departments never circulate one. It means only that this passive public review cannot responsibly state its format. Any report that lists student name, registration number, photograph, QR code, venue, seat, or barcode as confirmed hall-ticket fields would be extrapolating beyond the evidence.

## 3. Timetables and the Public Metadata Surface

MUJ's official examination page exposes a family of timetable links. The retrieved page lists an M.Tech ETE timetable for April-May 2025, B.Tech higher-semester and second-semester files for April-May or May 2025, faculty-specific December 2024 files for Arts, Design, Engineering, Law, Management and Commerce, and Science, plus open-elective schedules [4]. This is a public publication pattern organized by faculty, programme, semester, and examination session.

The B.Tech higher-semester timetable provides a concrete example of the metadata surface. Its extracted text presents a date column, discipline headings such as Automobile, Mechanical, Mechatronics, Civil, Chemical, Biotechnology, CSE, AIML, IT, Data Science, CCE, IoT, ECE, EEE, and ELC, and course names with codes. It includes 28-04-2025 as a Monday and shows a Slot-1 time of 09:30 AM to 12:30 PM [7]. The FOMC file similarly uses programme and semester groupings, including BBA and multiple semester columns [9]. These examples are sufficient to say that public schedules carry structured academic metadata, but not student-specific records.

| Public timetable family | Public period or label | Visible metadata | Defensive relevance |
|---|---|---|---|
| M.Tech ETE | April-May 2025, second semester | Programme and session label [4] | Useful for checking whether a public file is correctly scoped |
| B.Tech higher semester | April-May 2025 | Date, day, discipline, course name, course code, time slot [4] [7] | Public scheduling data; review for accidental personal data |
| B.Tech second semester | May 2025 | Programme or semester and ETE label [4] | Shows that separate semester files are published |
| Faculty of Law and MBA | April-May 2025 | Faculty or programme and higher-semester labels [4] | Demonstrates audience segmentation |
| Arts, Design, Engineering, Law, Management and Commerce, Science | December 2024 | Faculty-specific ETE files, including a revised Law file [4] | Revision naming is a useful publication-control signal |
| Open electives | 2024 and 2025 file families | Open-elective label and time-slot wording [4] [4] | Cross-faculty schedule metadata can be checked for consistency |

**Case study: the April-May 2025 B.Tech timetable.** MUJ chose a wide matrix rather than a student roster: disciplines form columns, courses and codes populate cells, and a time slot anchors the examination session. The outcome is highly useful to students and low in direct personal-data exposure. The security implication is an inference: a future publication pipeline should preserve the schedule's utility while preventing student identifiers, authenticated document tokens, or private room or seat assignments from being merged into the public file.

The date boundary is also material. The retrieved official page does not show a separately linked 2026 timetable URL; the displayed files are dated April-May 2025, May 2025, or December 2024 [4]. Separately, the 2026-27 academic calendar names MTE, showing MTE answer scripts, ETE, showing ETE answer scripts, re-sessional examination, and make-up examination milestones [3] [3] [3]. The calendar includes visible July dates, including 16, 24, 25, 26, and 27 July, but the extracted text does not make every date-to-label pairing clear [3]. Therefore the calendar is evidence of planned milestone categories, not a substitute for a 2026 course timetable.

## 4. Make-Up, Repeat, and the Meaning of "Back Paper"

The most important terminology finding is that MUJ's public handbook and manual use "make-up" rather than presenting a separately named back-paper page. The handbook says students who obtain F or I in ETE may take a make-up examination in the respective courses [10]. It says make-up examinations are conducted along with the regular ETE of a semester and only for courses running in that semester [10]. It also states that immediate preceding-semester make-up examinations are held after the relevant results and that no special make-up is scheduled for a student who misses that opportunity [10].

The handbook adds a grade consequence: students appearing in the described examinations, except those with I in ETE, are awarded one grade lower than the grade secured under the stated rule, while an E grade is retained [10]. The manual independently places make-up or repeat treatment in the exam-process sequence and gives the results-declaration process after moderation and approval [11] [11]. Appendix I lists a make-up examination fee of Rs 1000 for regular programmes and Rs 700 per subject for online programmes [12] [12]. The landing page separately gives Rs 1000 per course for its Make Up Application notice [4]. The differing wording and programme categories should be preserved, not silently harmonized.

| Trigger or category | Publicly stated action | Timing or qualification | What remains unknown |
|---|---|---|---|
| F or I in ETE | Make-up examination in the respective course [10] | Course and semester rules apply [10] | No public live form URL or portal state |
| Immediate preceding semester | Make-up after relevant semester results [10] | No special make-up if the opportunity is missed [10] | No current session-specific notice located |
| Re-MTE | Re-MTE for genuine medical grounds [10] | Prior notice before the examination; missing both can produce zero for MTE [10] | No public Re-MTE application template |
| Regular programme fee | Rs 1000 per course or, in Appendix I wording, Rs 1000 for regular programmes [4] [12] | Online form after notification on the landing-page wording [4] | No permanent public submission URL |
| Online programme fee | Rs 700 per subject in Appendix I [12] | Stated in the fee table | No explanation of how this maps to a particular current notice |
| Grade consequence | Generally one grade lower, with E retained in the cited rule [10] | Applies to the described make-up cases and excludes I as stated | No public student-specific outcome record |

**Case study: a missed ETE and the F/I split.** MUJ distinguishes an eligible absence from an absence with a valid reason: the former is F and the latter is I under the handbook's wording [10]. That decision feeds the later make-up rule, because F and I are both named as make-up triggers but the grade consequence separately excludes I in the one-grade-lower statement [10] [10]. The outcome is a process with several state transitions, not a generic "back paper" button. This is an inference about lifecycle structure, not a claim about database implementation.

The safe conclusion is therefore precise: MUJ publicly documents make-up examinations that cover some failed or incomplete ETE outcomes, re-MTE for a limited medical circumstance, and attendance-based DT re-registration. It does not, in the retrieved public material, publish a standalone page called "back paper procedure" with a current session deadline. The club should use the official notification and department or CoE channel for a real student case, and should not infer that any public PDF filename or form label identifies an editable record.

## 5. Results, Marks Flow, and the Carefully Bounded Update-Path Inference

The strongest public clue about an internal results lifecycle is in the Examination Manual. It says answer booklets are issued and evaluated, marks are placed on the top sheet, answer books are shown to students individually, and marks lists and associated materials are submitted to the Exam Section. It then states that marks are uploaded to AMS/DMS and that initial grades are calculated there [11]. The manual further says departmental Grade Moderation Committees may modify grade boundaries before final result notification, and that results are declared by the Office of the Controller of Examinations after moderation and approvals [11] [11].

The Student Examinations Handbook adds a result clock: results are declared within 15 days after grade moderation and approvals from the concerned Faculty Dean and Apex Committee [10]. It also says results may be held for unpaid fee or library dues or pending disciplinary action [10]. These are published business rules. They do not show a student-facing mark-edit function, an API, a controller route, an object identifier, a database table, or an authenticated role.

Appendix I supplies a second layer of control detail. Answer and attendance records include name, registration number, date, month, year, subject, and answer-booklet number [12] [12]. Invigilators reconcile booklets and question papers with attendance, arrange answer books by attendance-sheet sequence, and deposit them with the coordinator [12]. The Chief Superintendent and related officials oversee identity-card checks, malpractice investigation, answer-book transmission, and reports [12]. The manual says sealed question-paper envelopes identify course name, course code, examination date and time, and number of copies [11].

| Explicit public fact | Bounded inference | Prohibited conclusion |
|---|---|---|
| Marks lists are submitted and marks are uploaded to AMS/DMS [11] | The results lifecycle has a source-record-to-processing transition that deserves reconciliation and audit logging | A student can edit AMS/DMS or that a public endpoint exists |
| Grade Moderation Committees may modify grade boundaries [11] | Result publication should preserve who approved a change and when | A grade-boundary change is evidence of tampering |
| Results follow moderation and approvals [10] [11] | Publication should be treated as a controlled release point | The portal's result view is the authoritative write path |
| Answer books and attendance are reconciled [12] [12] | Reconciliation between physical or source records and digital marks is a useful defensive control | Any mismatch proves a cyber incident |
| Student-facing result, revaluation, and correction forms were not shown in retrieved examination content [4] | The public publication surface is incomplete for those workflows | No such process exists anywhere inside authenticated or departmental systems |

**Case study: AMS/DMS as a control boundary.** The documented decision is to upload marks, calculate initial grades, allow moderation, and require approvals before result declaration [11] [11]. The outcome visible to the public is a multi-role process. The mechanism is therefore best described as controlled data movement and approval, not as a direct student update path. That distinction prevents a common OSINT error: converting a legitimate operational noun such as "upload" into a speculative exploit route.

A defensive club can turn this evidence into a non-invasive control checklist for MUJ or for a lab replica: mark-list reconciliation, dual approval for moderation, immutable audit records for grade changes, separation of source marks from published results, and clear retention of answer-book and attendance references. These are recommendations based on the published lifecycle. They are not assertions that MUJ lacks those controls.

## 6. Results Grievances, Appeal Windows, and the Missing Dispute Case

The public grievance page provides three distinct routes. It links "SUBMIT YOUR GRIEVANCE ONLINE" to a Microsoft Forms URL, links the UGC Samadhaan portal, and links a University Students Grievance Redressal Committee document [2]. The page also publishes institutional grievance contacts, but this report omits personal phone numbers and email addresses because they are unnecessary to the technical conclusion [2]. The route is sufficient for a student with a real examination or result complaint; it is not evidence of a hidden SLCM update mechanism.

The USGRC notification is dated June 26, 2026 and says the committee is constituted in compliance with the UGC Redress of Grievance of Students Regulations, 2019 and AICTE Grievance Redressal Regulations 2019 [6]. It states that the USGRC addresses grievances unresolved by the School-level Students Grievance Redressal Committee within its assigned jurisdiction [6]. It says the committee follows natural justice, has a quorum of three including the Chairperson, and that members serve for two years [6]. It also says the USGRC sends its report and recommendations within 15 days of receiving a grievance, and that a student may appeal to the Ombudsperson within 15 days of receiving the USGRC decision [6].

| Window or route | What the source says | What it should not be called |
|---|---|---|
| Online submission | MUJ links a Microsoft Forms submission route [2] | A confirmed SLCM-integrated result editor |
| UGC route | MUJ links Samadhaan [2] | Proof that a dispute is cyber-related |
| School escalation | Unresolved grievances proceed from school level to USGRC [6] | A result-specific revaluation workflow |
| USGRC report | Report and recommendations within 15 days of receiving the grievance [6] | A promise that marks will change within 15 days |
| Ombudsperson appeal | Appeal within 15 days of receiving the USGRC decision [6] | A general deadline to request revaluation |
| Examination result declaration | Results within 15 days after moderation and approvals [10] | The same clock as a grievance or appeal |

The key unanswered point is a result-specific grievance or revaluation window. The committee notification's remit is general and does not state an exam-mark-specific deadline [6] [6]. The handbook's result section states declaration timing and conditions for holding results, but the focused extracted text contains no separate revaluation, grievance, or correction procedure [10]. The official examination page's retrieved content likewise shows no result, revaluation, or correction form [4].

**Case study: the 2026 USGRC notice.** MUJ made a governance decision to use school-level escalation, a university committee, natural-justice principles, a 15-day report target, and a 15-day Ombudsperson appeal [6]. The outcome is a documented complaint path, not a published case. The public corpus reviewed here contains no reliable, attributable student account that establishes a marks dispute, a recurring correction failure, or a backend update path. That is a low-confidence area by design: absence of a verified public case is not proof that no student has ever complained.

For the security club, the responsible output is a dispute-evidence register with three labels: verified institutional process, student-reported allegation requiring consent and corroboration, and unverified search hit. Only the first category is supported here. A generic result page, a third-party marks calculator, or an unattributed social comment must not be upgraded into an incident report.

## 7. SLCM Surface, Identity Claims, and What the Public Host Does Not Prove

The public SLCM landing page is small. Its extracted text says "WELCOME TO MUJ PORTAL," "Sign In," and "Sign In Parent Login" [1]. It does not expose an exam timetable, a hall-ticket document, a result page, or an authenticated role description in the public landing-page text. This is enough to identify the hostname's public presentation, but not enough to characterize its application security.

The examination artifacts sit on the university's main website and are linked as PDFs below an examination directory, while the SLCM landing page is on a separate hostname [1] [4]. That separation creates an important analytical boundary. A timetable PDF is evidence of a public publication repository. It is not evidence that the same file is generated by SLCM. Similarly, a grievance Microsoft Forms link proves that the public grievance page uses a Microsoft Forms destination [2], but it does not prove that SLCM uses Microsoft 365 as its identity provider or that the form shares a session with SLCM.

| Surface | Publicly confirmed | Not confirmed by this review |
|---|---|---|
| MUJ SLCM hostname | Portal welcome text, sign-in and parent-login labels [1] | MVC version, .NET version, IIS version, Akamai policy, identity flow, exam modules |
| MUJ examination page | Process documents, application-format area, timetable links [4] [4] | Whether the PDFs are generated by SLCM or a separate publishing workflow |
| Timetable PDFs | Faculty, programme, course, date, and time metadata in public files [7] [9] | Student-specific data, ticket renderer, or result update logic |
| Grievance page | Office Forms, UGC Samadhaan, and USGRC destinations [2] | Shared authentication, shared database, or SLCM write permissions |
| Research brief stack labels | Supplied scope assumptions | Independent public confirmation of each product and version |

**Case study: two public surfaces, one assumed ecosystem.** The public evidence shows a document surface and a portal surface, but it does not connect them technically. The safe inference is that students may experience them as one university ecosystem, while the evidence base does not establish a shared application, shared database, or shared identity session. The outcome is a more conservative risk map: process relationships can be analyzed; implementation relationships remain unknown.

The supplied labels ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 identity are retained as scope assumptions for future authorized work. They should appear in a report as "provided but not independently verified" unless an owner-approved, passive source publishes them. A public sign-in page alone cannot establish software version or a protection boundary. An analyst should not claim that a version is vulnerable, that Akamai is correctly configured, or that Microsoft 365 is the identity authority without direct, authorized evidence.

## 8. Defensive Research Plan Without Unauthorized Access

The published artifacts support a useful, non-invasive research plan. First, preserve official URLs and retrieval dates for the examination landing page, handbook, manual, committee notice, academic calendar, and timetable files. Second, compare only public revisions: a new timetable file, changed wording, changed fee, or changed grievance link can be logged as a publication change without touching the portal. Third, ask MUJ for written permission before any technical assessment, provide a scope that excludes student data and production writes, and use a test tenant or lab replica if the university wants application-security validation.

| Observation | Mechanism indicated by public text | Defensive implication | Safe next action |
|---|---|---|---|
| Marks lists and AMS/DMS upload are documented [11] | Marks move through an operational processing stage | Audit source-to-result reconciliation and role separation | Ask the owner for a control description; do not test production |
| Grade moderation and approvals precede results [11] [11] | Publication is a controlled release point | Preserve approval history and change logs | Review a redacted sample or policy, with consent |
| Answer books and attendance are reconciled [12] [12] | Physical or source records provide an integrity reference | Reconcile counts and identifiers before upload | Design a tabletop exercise, not a live manipulation |
| Public timetable PDFs expose course metadata [7] | Schedule publication is a public information flow | Check for accidental personal data and stale files | Perform document review only |
| Grievances use official routes [2] [6] | Complaints have a governance channel | Preserve case IDs and response deadlines under policy | Direct students to the official channel |
| Portal landing page is sign-in only in public text [1] | Authenticated functions are not public artifacts | Do not treat the sign-in surface as permission | Stop at the landing page without written scope |

The OWASP material in the research context provides useful defensive vocabulary. It defines IDOR as direct access to objects based on user-supplied input [13], describes insufficient authorization checks as the cause in the example [13], and says session IDs must be treated as untrusted input [14]. Those principles support a high-level control recommendation: MUJ should authorize every student-record operation against the authenticated subject and server-side role, renew session identifiers after privilege changes, and log the full session lifecycle [14] [14] [14]. This report does not claim that MUJ has or lacks those controls, and it gives no route, parameter, payload, or test sequence.

A safe tabletop scenario can remain abstract: "A legitimate marks list differs from a published result after moderation." Participants identify the owner, source record, approval record, grievance route, and evidence-retention requirement. They do not create accounts, submit fabricated forms, replay requests, inspect another student's record, or attempt to change a grade. The exercise tests governance and detection logic rather than production security.

The same rule applies to public dispute research. A student who voluntarily supplies a redacted notice can help establish dates, official channels, and resolution status. The club should remove registration numbers, names, email addresses, QR codes, barcodes, screenshots of authenticated pages, and session tokens before publication. No alleged dispute should be used to guess an update endpoint. The ethical value of the report is to identify documented controls and evidence gaps, not to convert a complaint into an attack recipe.

## Synthesis

The main entities and strategies in this review differ in mechanism, scope, trade-off, evidence strength, and time horizon. The handbook is a student-facing rule set; the manual is an operational-control description; the timetable is a public schedule artifact; the grievance notice is a governance instrument; and SLCM is only a public sign-in surface in the evidence collected. Treating them as interchangeable would create the very overclaim that a security report should avoid.

| Evidence object | Mechanism | Scope | Trade-off | Evidence strength and horizon |
|---|---|---|---|---|
| Student Examinations Handbook | Eligibility, grades, missed exams, make-up, result timing [10] [10] | Student rules | Clear outcomes but incomplete implementation detail | High for its 2023-24 text; historical unless updated |
| Examination Manual | Evaluation, AMS/DMS, grade moderation, approvals [11] [11] | Institutional exam operations | Shows control points but not live interfaces | High for stated process; implementation unknown |
| Appendix I | Chain of custody, identifiers, attendance, fees [12] [12] | Exam administration | Strong integrity context but older references appear in the document | High for listed controls; current applicability needs owner confirmation |
| Timetable PDFs | Public dates, slots, courses, codes [4] [7] | Schedule publication | Useful transparency with metadata exposure | High for the individual files; current 2026 link gap |
| USGRC notice | School escalation, committee, report and appeal clocks [6] | Student grievance governance | Accountable route but no exam-specific revaluation rule | High for the June 2026 notice |
| SLCM landing page | Portal sign-in and parent-login presentation [1] | Public application surface | Identifies the surface but reveals almost no function | High for visible wording; low for architecture |

Three non-obvious tensions emerge. First, the examination process is described as decentralised under the CoE, while AMS/DMS and approval stages imply structured institutional processing [10] [11]. The reasonable interpretation is not contradiction but layered governance: departments and committees can participate while result publication remains controlled. The exact division of permissions is not public.

Second, the public surface is transparent about schedules and governance but opaque about student-specific artifacts. Timetable PDFs expose course metadata, while the hall-ticket format and result or revaluation forms are not publicly exposed in the retrieved corpus [7] [4]. This is a defensible privacy boundary, but it also means an OSINT researcher cannot use public evidence to reconstruct the student workflow.

Third, two separate 15-day periods can be mistaken for one: result declaration after moderation and approvals, and Ombudsperson appeal after a USGRC decision [10] [6]. They have different triggers and should be recorded as separate clocks. Likewise, "make-up" is documented, while "back paper" is a user-facing synonym or hypothesis rather than a separately verified MUJ page [10] [4].

The integrated conclusion is that the highest-value public finding is not a suspected update route. It is a control map: source marks and answer-book records move through evaluation, AMS/DMS, grade moderation, approvals, publication, and grievance governance. A responsible club can study that map, compare future public artifacts, and recommend auditability without accessing student data or testing production.

## VERDICT

**Overall confidence: High for published examination and grievance process facts; medium for the abstract results-lifecycle model; low for any claim about public marks-dispute prevalence or a live SLCM update path.**

The public record supports the following final answer. MUJ publishes exam-process documents and timetable artifacts; the handbook documents eligibility, F/I/DT outcomes, Re-MTE and make-up treatment; the manual documents marks-list submission, AMS/DMS upload, grade moderation, approvals, and result declaration; and the 2026 grievance notice documents school escalation, a 15-day USGRC reporting target, and a 15-day Ombudsperson appeal [4] [10] [11] [6].

The public record does not support a confirmed hall-ticket template, a current public result or revaluation form, a standalone back-paper page, a result-specific grievance deadline, a verified student marks-dispute case, or a technical claim that the cited SLCM host uses the stack labels supplied in the brief [4] [1]. The safest update-path statement is an explicitly labelled inference: MUJ's published process contains controlled transitions from answer-book and marks-list records through AMS/DMS, grade moderation, approvals, and result publication. That inference must not be expanded into a route, parameter, object identifier, or exploit hypothesis.

**Decision for the university security club:** classify the examination artifacts as a public-process and publication-hygiene research topic, not as permission to test the SLCM application. Maintain a source ledger, label 2023-24 and 2026 documents by their actual dates, route genuine student complaints through MUJ's official grievance channels, and seek written authorization plus a non-production environment before any application-security assessment.

## References

1. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
2. *Online Grievance Registration - Manipal University Jaipur *. https://www.jaipur.manipal.edu/online-grevience-registration.php
3. *AC calender -2026-27.cdr*. https://jaipur.manipal.edu/img/pdf/academicrules/AC-calender-2026-27.pdf
4. *Examination - Manipal University Jaipur *. https://jaipur.manipal.edu/examination.php
5. *MANIPAL UNIVERSITY JAIPUR END TERM EXAMINATION, APRIL-MAY 2025 TIME-TABLE Program Name: M.Tech (AIML DEPARTMENT) Second Sem DATE Slot-1 (09:30 AM*. https://jaipur.manipal.edu/img/pdf/exam/M.TECH_II%20SEM_ETE%20TT_%20APRIL-MAY%202025_.pdf
6. *Committee Usgrc*. https://www.jaipur.manipal.edu/img/pdf/Committee_USGRC.pdf
7. *Slot-1 (09:30 AM - 12:30 PM)*. https://jaipur.manipal.edu/img/pdf/exam/B.Tech_Higher%20Sem_ETE_APRIL-MAY_2025.pdf
8. *Academics rules & regulation - Manipal University Jaipur *. http://jaipur.manipal.edu/academic-rules-regulations.php
9. *ENVIRONMENTAL ENVIRONMENTAL SCIENCE (CHY1003/ SCIENCE (CHY1003/ 09-12- MICROECONOMICS BUSINESS OPERATIONS HA4101(cid:9) HT3101(cid:9) LOGISTICS HA2101 COST ACCOUNTING – II HA4101(cid:9) MBA*. https://jaipur.manipal.edu/img/pdf/exam/FOMC_ETE%20Timetable%20Dec%202024.pdf
10. *Student Examinations Handbook*. https://jaipur.manipal.edu/img/pdf/exam/Student%20Examination%20Handbook%202023-24%20%2811.08.2023%29.pdf
11. *EXAMINATION MANUAL*. https://jaipur.manipal.edu/img/pdf/exam/3.%20Manual%20Exam%20Process.pdf
12. *APPENDIX - I*. https://jaipur.manipal.edu/img/pdf/exam/4.%20Appendix%20I%20Examination%20manual%20MUJ%2003%20Apr%2019.pdf
13. *http://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References*. http://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References
14. *http://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html*. http://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
