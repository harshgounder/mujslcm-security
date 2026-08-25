# MUJ SLCM Reddit OSINT: Findings, Gaps, and Safe Actions

## Executive Summary

- **Recurring Availability Complaints**: A public r/manipal post describes SLCM as crashing every other day, while another student says the MUJ site was unusable for much of a semester and made attendance difficult to verify [10]. The decision is to treat availability and attendance visibility as the leading operational risk, not as proof of a security flaw.
- **Identity Lifecycle Friction**: A r/Manipal_Academics student reported that a registration number changed after intra-sliding and that both old and new identifiers were rejected; commenters described contacting an academic office or asking at AB1 [8]. The decision is to test identity synchronization and recovery through authorized staff workflows.
- **Payment Reconciliation Risk**: Students reported that fees had been deducted and a receipt retained while SLCM still displayed pending status [34]. Another student said a stale SLCM due had to be cleared before an admit card could be obtained, requiring proof and administrative escalation [39]. The decision is to add a receipt-backed reconciliation queue and a visible escalation status.
- **Academic Data Integrity**: Public posts mention delayed or missing attendance, removed or non-working results views, grades decreasing, and elective or subject data problems [40][42] [32]. These are user reports, not proof of database corruption. The decision is to preserve audit trails and reconcile source records before changing grades or attendance.
- **Privacy Allegation Requires Containment, Not Exploitation**: A post alleged that CGPA data for students across branches had been exposed and later said the site returned 404; a commenter claimed that a vulnerability report was sent to IT and patched within a week [33]. No institutional confirmation was found in the collected corpus. The decision is to preserve evidence privately and use responsible disclosure, never to browse other accounts or redistribute records.
- **Student Automation Is a Defensive Signal**: Public GitHub repositories describe REST or scraping projects for attendance, marks, or CGPA, including one repository that advertises automated login and CAPTCHA solving [53] [54]. Their existence does not establish a current vulnerability. The decision is to review authorization, rate limits, bot detection, secrets handling, and terms of use without running code against production.
- **Portal Architecture Is Not Independently Established**: The official MUJ page visibly presents a MUJ portal sign-in and parent login [55]. The supplied ASP.NET MVC, .NET Framework, IIS, Akamai, and Microsoft 365 descriptions were not independently confirmed by the public Reddit and portal evidence collected here. The decision is to validate the inventory with the authorized owner before designing tests.
- **Exhaustiveness Is Not Achievable From Public Indexing Alone**: Search inventories revealed additional SLCM-related titles, but some pages were empty, deleted, or lacked a recoverable permalink or full date [13] [14]. The report therefore presents a high-confidence public sample and an evidence register, not a claim that every historical Reddit thread has been found.

## Scope, Method, and Evidence Rules

This report covers public material associated with r/manipal and r/Manipal_Academics. It focuses on SLCM, MUJ portal access, attendance, grades and results, fee status, registration and profile problems, and portal behavior. A small separate section records adjacent r/manipaljaipur material because it appeared during discovery, but those posts are not merged into the requested subreddit corpus.

The research method was reproducible at a high level: search public Reddit pages and Reddit JSON representations; record the exact permalink when available; preserve the post title, visible body wording, displayed age or source timestamp, and relevant public comments; classify each item as direct page evidence, indexed evidence, or an adjacent corroboration; and remove personally identifying information from the report. This is a methodology summary, not private chain-of-thought. The report does not disclose hidden reasoning, credentials, session material, private subreddit content, or operational instructions for accessing application endpoints.

The most important evidentiary distinction is between a student complaint and an independently verified incident. For example, "fees still pending" is direct evidence that a student publicly reported that display state. It is not proof that the payment processor failed, that the university lost funds, or that the portal database is inconsistent in every case. Similarly, a post titled "Cgpa data leak of all branch students" establishes that an allegation was made; it does not establish the scope, cause, or authenticity of the alleged exposure [33].

## Primary Reddit Evidence Register: r/manipal

| Topic | Thread URL | Date evidence | Public wording or issue | Public response or workaround | Evidence status |
|---|---|---|---|---|---|
| Availability | https://www.reddit.com/r/manipal/comments/17anbg2/slcm_is_literally_ass/ | Reddit source timestamp 1697624412; page displayed about 3y ago | "How does a college that makes millions and produces so many cs graduates fails to make a proper working website that doesn't crash every other day" [10] | A commenter said attendance visibility was the practical concern and another recalled an earlier portal being worse [10] | Direct post and comments; anecdotal |
| Attendance lock | https://www.reddit.com/r/manipal/comments/17usdb4/attendance_lock_for_slcm/ | Reddit source timestamp 1699930061 | Thread asks about the SLCM attendance lock | A comment says the lock is usually about one week earlier [6] | Direct title and comment; timing not institutionally verified |
| SLCM 2.0 and electives | https://www.reddit.com/r/manipal/comments/1qa5h99/slcm_20_manipal_situation_summarised/ | Reddit source timestamp 1768152974; page displayed about 8mo ago | Title says "Slcm 2.0 manipal situation summarised" [32] | Comments report missing promised functionality, preference-form problems, missing subjects, and attendance misclassification [32] | Direct post/comments; allegations |
| CGPA exposure allegation | https://www.reddit.com/r/manipal/comments/1ncl5xy/cgpa_data_leak_of_all_branch_students/ | Reddit source timestamp 1757429775; page displayed about 1y ago | "How did they get the data of all students cgpa from across departments"; an edit says the site later showed 404 [33] | A commenter claimed the issue was reported to IT and patched within a week [33] | Unverified user allegation; no institutional confirmation |
| Phone update | https://www.reddit.com/r/manipal/comments/1ivr2aa/how_to_change_phone_number_in_slcm/ | Reddit source timestamp 1740253039 | Student asks how to change the phone number in SLCM [31] | Public comments describe using the admissions profile/address area, allowing time for synchronization, and contacting the academic section with old and new details [31] | Student-reported administrative workaround; not an official procedure |
| SLCM due and admit card | https://www.reddit.com/r/manipal/comments/1m23kxi/one_of_the_worst_departments_in_the_college/ | Reddit source timestamp 1752746625 | Student says a due remained in SLCM and had to be cleared before an end-semester admit card could be obtained [39] | Student describes keeping proof of payment and obtaining an administrative letter and signatures [39] | Direct comment; administrative workaround |
| Casual-term fee | https://www.reddit.com/r/manipal/comments/1cyd4xv/what_is_casual_term_fee_on_slcm/ | Reddit source timestamp 1716416548 | Search extract records a "fee pending rs 6000 casual term" concern [35] | No verified resolution was recovered | Direct title/index evidence; unresolved |
| Revaluation results | https://www.reddit.com/r/manipal/comments/v8ax39/how_long_will_it_take_for_the_revaluation_results/ | Reddit source timestamp 1654758037 | Student asks how long revaluation results take to update in SLCM [48] | No comments or workaround were visible [48] | Direct title; no resolution |
| Delayed academic workflow | https://www.reddit.com/r/manipal/comments/1q6txrh/we_must_protest_whatever_is_going_on_with_slcm/ | Page displayed about 8mo ago | Post attributes delayed elective classes and related calendar pressure to SLCM problems [50] | A comment mentions past lab switching, but this is not an approved workaround and should not be copied into production records [50] | Direct post/comment; causal attribution unverified |
| Third-party fee financing | https://www.reddit.com/r/manipal/comments/1m0ofr4/has_anyone_used_the_emi_option/ | Page displayed about 1y ago | Student asks whether GrayQuest produced a receipt in SLCM and expresses concern that fees might not have been paid [49] | No verified finance-office response was recovered | Student concern; not proof of fraud |

The r/manipal evidence is consistent on one point: students experience SLCM as a dependency for attendance, academic planning, fees, and examinations. That is an inference from the distribution of complaints, not a claim that all failures share one technical root cause. The oldest availability complaint specifically uses crash language [10], while later posts describe functional gaps and data presentation issues rather than a single outage. A defensible remediation program should therefore measure separate service-level indicators for availability, synchronization, authorization, and data correctness.

## Primary Reddit Evidence Register: r/Manipal_Academics

| Topic | Thread URL | Date evidence | Public wording or issue | Public response or workaround | Evidence status |
|---|---|---|---|---|---|
| Registration number and login | https://www.reddit.com/r/Manipal_Academics/comments/1993mdc/slcm_login/ | Reddit source timestamp 1705515761; page displayed about 3y ago | Student says a new registration number appeared after intra-sliding and SLCM rejected the identifier [8] | Comments report trying the new identifier, contacting the academic section, asking at AB1, and using the normal forgotten-password route [8] [29] | Direct post/comments; ordinary support advice |
| Fee paid but pending | https://www.reddit.com/r/Manipal_Academics/comments/1lzf0ht/paid_my_fees_but_still_showing_as_pending_on_slcm/ | Reddit source timestamp 1752473910; page displayed about 1y ago | Student says the fee was paid, a receipt existed, and SLCM still showed pending [34] | A comment says to wait a day for the receipt to be generated; another suggests waiting briefly before escalation | Direct post/comments; no independent transaction confirmation |
| Fee section not visible | https://www.reddit.com/r/Manipal_Academics/comments/1u8476b/fees_not_showing_in_slcm/ | Reddit source timestamp 1781684314 | Student says the fee portal or fee section was unavailable while peers could view it [30] | Student asks whom to email; no verified resolution was visible [30] | Direct post; unresolved |
| New student portal access | https://www.reddit.com/r/Manipal_Academics/comments/1v70yng/regarding_slcm_portal/ | Page displayed about 3mo ago | Student asks whether newly admitted students can log in and later says, "I still can't" [47] | Comments point toward orientation or an on-campus support counter [47] | Direct post/comments; support advice |
| SLCM profile creation | https://www.reddit.com/r/Manipal_Academics/comments/1uspviv/i_need_help_with_what_ever_this_slcm_profile_is/ | Page displayed about 3mo ago | Student asks for help understanding the SLCM profile process [36] | The discussion references university profile creation and orientation context | Direct title/body; limited resolution |
| Parent SLCM link | https://www.reddit.com/r/Manipal_Academics/comments/1s8mhsd/can_someone_please_share_me_the_parent_slcm_link/ | Page displayed about 5mo ago | Student requests the parent SLCM link [41] | A comment discusses a user-ID format; the exact identifier details are intentionally not reproduced [41] | Direct post/comment; sensitive operational detail withheld |
| Attendance freeze | https://www.reddit.com/r/Manipal_Academics/comments/1sgm4q7/when_does_slcm_freezecan_profs_take_attendance/ | Page displayed about 5mo ago | Student asks when SLCM freezes and whether professors can take attendance later [44] | No authoritative calendar or safe technical workaround was recovered | Direct title; unresolved |
| NPTEL marks | https://www.reddit.com/r/Manipal_Academics/comments/1splp5e/how_do_i_get_my_nptel_marks_uploaded_to_slcm/ | Page displayed about 4mo ago | Student asks how to get NPTEL marks uploaded after a long delay [43] | No verified response was recovered | Direct title; unresolved |
| Results tab | https://www.reddit.com/r/Manipal_Academics/comments/1plljtw/it_appears_they_have_removed_the_results_tab_from/ | Page displayed about 8mo ago | Search extract identifies a removed results tab and a non-working academics tab [40] | No safe student-side workaround was verified | Direct/index evidence; unresolved |
| Grades decreased | https://www.reddit.com/r/Manipal_Academics/comments/1pny6zb/grades_decreased_on_slcm/ | Page displayed about 8mo ago | Thread title reports that grades decreased on SLCM [42] | Details and resolution were not visible in the recovered extract | Direct title; unresolved |
| Second-semester attendance | https://www.reddit.com/r/Manipal_Academics/comments/1i9fyc9/anyone_facing_any_issues_with_slcm/ | Reddit source timestamp 1737782566 | Comment evidence describes attendance remaining associated with the first semester, blank options, and poor mobile optimization | No verified technical workaround was recovered | Direct comments; student report |
| Unable to log in | https://www.reddit.com/r/Manipal_Academics/comments/1m354xl/i_am_not_able_to_log_in_to_my_slcm_portal_wht_to_do/ | Page displayed about 1y ago | Thread title reports inability to log in [45] | A comment advises using the registered email; this is ordinary account-recovery advice, not a bypass [45] | Direct title/comment |

The r/Manipal_Academics material adds a lifecycle dimension. Several problems occur at transitions: a new registration number after intra-sliding, a new student waiting for profile creation, a parent needing the correct portal, or a fee payment waiting to reconcile. This suggests an inference that synchronization boundaries may be more important than the login form itself. That inference must be tested through authorized logs and staging data, not through repeated login attempts or manipulation of identifiers.

## Case Study 1: Login and Identity Synchronization

The registration-number post is the clearest public example of an identity lifecycle failure. A student reported that intra-sliding changed the registration number and that SLCM then rejected the login identifier [8]. Public replies recommended normal institutional contact paths, including the academic section and an on-campus location, and one reply points to the standard forgotten-password route [8] [29]. The evidence does not establish whether the cause was delayed provisioning, stale directory data, an incorrect identifier, or a user error.

For a security club, the lesson is to model identity as a state machine: admitted, registered, intra-slid, provisioned, password-reset eligible, parent-linked, and active. The application owner should verify that each state has a defined source of truth, a correlation identifier, an expiry rule, and an auditable reconciliation result. Testing should use synthetic accounts and written authorization. It should verify that a user cannot see another person's profile when identifiers change, while avoiding any attempt to discover real student records.

The phone-number post provides a second lifecycle signal. A student asks how to change a phone number, and public responses describe an admissions-profile update, time for synchronization, and contacting the academic section with old and new information [31]. Because this is student-generated advice, it should be treated as a lead rather than an official procedure. The safe operational recommendation is to require verified support requests, show the effective date of a profile change, and notify the account owner through an already trusted channel.

## Case Study 2: Fees, Receipts, and Administrative Consequences

The strongest payment case involves a student who says the fee was paid, a receipt was available, but SLCM continued to show the fees as pending [34]. A comment says that waiting a day may allow receipt generation. This is a classic reconciliation ambiguity: the student sees a successful payment artifact, while the academic system displays a pending state. It could arise from settlement delay, callback failure, queue processing, account mapping, or a display cache. Reddit does not identify the mechanism.

A separate r/manipal comment describes a stale SLCM due blocking an admit card until the student produced payment proof and obtained administrative signatures [39]. This turns a display problem into an academic access problem. The recommended control is not a student-side workaround. It is a finance-to-SLCM reconciliation service with immutable transaction identifiers, idempotent updates, a receipt download, a clear pending reason, and a human escalation path that cannot silently alter the record.

The casual-term fee thread and GrayQuest discussion show that students also seek explanations for unfamiliar fee labels and third-party payment status [35] [49]. Those posts do not prove incorrect charges or fraud. They do show that unclear labels and delayed receipt visibility can create distrust. A secure design should make the payee, amount, academic period, settlement state, and support owner visible without exposing other students' payment information.

## Case Study 3: Academic Data, Attendance, and Portal Functionality

The availability complaint says the site crashed frequently and that students needed a working website [10]. Another comment says a MUJ site was effectively unusable for much of a semester and that attendance could not be checked reliably. Later material describes attendance remaining associated with the wrong semester, blank options, and mobile usability problems. These reports support a reliability and correctness workstream, but not a common root cause.

SLCM 2.0 reports add functional regression concerns. Public comments describe promised functionality not working, the old site being preferable, preference data being lost, subjects missing for part of a batch, and attendance being misclassified [32]. The results-tab and grades-decreased titles indicate further student concern, although the recovered evidence does not provide enough detail to determine what changed or why [40][42]. The safe recommendation is to introduce versioned academic records, change histories, pre-release migration tests, and a user-visible correction workflow.

Attendance freeze questions and delayed NPTEL-mark uploads reveal process ambiguity as well as software problems [44] [43]. The university should publish authoritative cutoffs and responsible offices, while the application should distinguish "not yet uploaded," "pending validation," "frozen," and "corrected." Students should not be advised to alter requests, replay forms, or manipulate client-side state. Any discrepancy should be reported with a screenshot, timestamp, course identifier, and no password or session token.

## Case Study 4: Privacy Allegation and Responsible Handling

The CGPA post is a high-risk but low-certainty item. The title asks how data for all students across departments was obtained, and the edit says the website later showed 404 [33]. A commenter claims the issue was reported to IT and patched within a week [33]. These are public statements, not an independent breach investigation. The report therefore classifies the item as an unverified allegation, not a confirmed incident.

The correct security-club exercise is evidence preservation and responsible disclosure. Preserve the public URL, timestamp, screenshots that contain no personal data, and a minimal description of what was visible. Do not enumerate records, access another account, test guessed identifiers, use a leaked link, or circulate samples. Ask the authorized university security or IT contact to confirm scope, affected data categories, containment, and notification obligations. If the university cannot confirm, the report should retain the uncertainty.

This case also demonstrates why a 404 is not a complete security conclusion. It may indicate removal, routing change, access control, or an unrelated error page. Conversely, a page returning normally does not prove that authorization is correct. Only an authorized test with synthetic records and server-side logs can establish whether object-level access controls work.

## Public GitHub Inventory and Safe Interpretation

| Repository | Public description or signal | What it means defensively | What this report withholds |
|---|---|---|---|
| https://github.com/tejaskash/slcm-api | Described as a Flask REST API for attendance and marks from SLCM; files include slcm.py and slcm_scrape.py [53] | Indicates historical interest in programmatic access and a need for rate limits, secrets scanning, and authorization review | Code, endpoints, request construction, credentials, and deployment steps |
| https://github.com/nikeplusdash/SLCM-api/tree/master/SLCMv1 | Repository and SLCMv1 path are publicly indexed with application files [51] | Supports a historical automation inventory | No operational API details or instructions |
| https://github.com/utk3012/SLCM | Described as a REST API to scrape the SLCM Manipal portal [52] | Suggests the owner should monitor automated traffic and review old integrations | No scraping instructions or target procedures |
| https://github.com/sankalp2004/SLCM-is-Dumb | Public description mentions CGPA extraction, CAPTCHA automation, Selenium, and credential-security warnings [54] [54] [54] | Signals the need for bot controls, CAPTCHA governance, secret detection, and review of legacy public code | No CAPTCHA-solving method, login automation, endpoint, script, or execution advice |

The repository inventory is not evidence that these projects still work, are authorized, or affected the current MUJ deployment. It is a defensive indicator. Owners should scan public repositories for exposed secrets, rotate any compromised credentials, and contact maintainers through responsible channels where appropriate. Security-club members should not run the projects against the live portal.

## Portal Surface and Architecture Uncertainty

The official MUJ portal page visibly identifies itself as "WELCOME TO MUJ PORTAL," presents "Sign In," shows the @muj.manipal.edu domain text, and includes "Sign In Parent Login" [55]. That establishes a public login surface and a parent-login concept. It does not establish the framework version, server platform, CDN behavior, authentication protocol, tenant configuration, or whether the current page is backed by the same legacy SLCM components discussed in Reddit.

The ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 identity labels in the research brief should therefore be treated as supplied inventory hypotheses until confirmed by the authorized asset owner. An inference from public complaints would be unsafe. A portal that feels slow does not prove an IIS issue; a Microsoft-branded email domain does not prove that portal authentication uses Microsoft 365; and a visible parent login does not prove that parent and student authorization are correctly separated.

A safe assessment plan would use a staging environment or explicitly approved test accounts. It should cover authentication mapping, session invalidation, password recovery, role separation, object-level authorization, payment-state reconciliation, migration rollbacks, audit logging, cache invalidation, rate limits, and error-message minimization. Results should be reported with test-account identifiers only. No live endpoint discovery, request replay, identifier guessing, or bypass attempts are necessary to produce useful defensive findings.

## Safe Student Workarounds and Escalation Matrix

| Observed problem | Safe public advice reported in the corpus | Security-safe improvement |
|---|---|---|
| Registration number rejected after intra-sliding | Contact the academic section or on-campus support; use the normal password-recovery flow [8] [29] | Provide a verified identity-sync status and a one-time support ticket |
| Fee paid but still pending | Retain the receipt and allow the documented settlement window; escalate to finance if the state remains pending [34] | Show transaction ID, settlement state, last synchronization time, and escalation owner |
| SLCM due blocks an admit card | Keep proof of payment and use the formal administrative escalation described by the student [39] | Add a controlled exception process with approvals and immutable audit records |
| Phone number needs updating | Use the normal profile-management route and contact the academic section with verified details [31] | Require re-authentication, notify the old trusted channel, and log the change |
| New student cannot log in | Ask orientation or the official on-campus support counter [47] | Publish provisioning milestones and a support SLA |
| Attendance or marks missing | Report the course, term, timestamp, and screenshot through official support; do not edit requests or replay traffic | Provide correction tickets and visible status transitions |

## What Remains Unanswered

| Question | Current status | Why it remains unanswered | Appropriate next step |
|---|---|---|---|
| Did every historical SLCM thread get found? | No | Reddit search and indexing miss deleted, private, unindexed, or empty pages; inventories contain titles without complete URLs [13] [14] | Repeat authorized public searches periodically and preserve a dated query log |
| What are the exact dates for every thread? | Partial | Some extracts expose Unix timestamps or relative ages, while others expose only titles | Read each live page manually or through an authorized archive and record UTC timestamps |
| What caused login failures? | Unknown | Reports are compatible with provisioning, identifier changes, password state, or service failure [8] | Correlate support tickets, directory sync logs, and synthetic-account tests |
| Were fees actually lost or merely delayed? | Unknown | Reddit confirms reported display states, not processor or ledger records [34] | Reconcile payment gateway, finance ledger, and SLCM event logs |
| Was the CGPA allegation a confirmed breach? | Unknown | The post and comment are user claims; no institutional confirmation appears in the collected evidence [33] | Seek owner confirmation; do not reproduce or test alleged access |
| Was the alleged issue fixed? | Partially claimed | A commenter says IT patched it, but scope and fix are not independently verified [33] | Request a responsible-disclosure closure summary from the owner |
| Is the supplied technology stack current? | Not established | The official page exposes a login surface but not reliable stack proof [55] | Validate the asset inventory with the authorized owner |
| Are GitHub projects authorized or still operational? | Unknown | Public descriptions establish existence, not permission or current compatibility [53] [54] | Review repositories defensively; do not run against production |

## Synthesis

Across three dimensions, the evidence separates operational reliability from security certainty. On scope, r/manipal contains broad complaints about crashes, attendance, fees, academic scheduling, and a privacy allegation [10] [33]. r/Manipal_Academics contributes more transition-specific cases involving registration, onboarding, fee visibility, results, and marks [8] [34] [40]. The adjacent r/manipaljaipur posts are useful corroborative signals but fall outside the requested primary corpus: one reports paid installments still appearing in SLCM [1], and another reports a password error [2]. The divergence suggests different user populations and lifecycle stages, not necessarily different systems.

On mechanism, the complaints divide into four plausible classes: service availability, identity synchronization, financial reconciliation, and academic data presentation. The same portal can be involved in each, but the evidence does not justify collapsing them into one root cause. The most consequential tension is between the student experience and the system of record: a student may possess a receipt while SLCM says pending [34], or may know that attendance was taken while the portal displays the wrong term. That tension requires auditability and reconciliation, not client-side workarounds.

On trade-offs, rapid student automation can improve convenience but creates credential, authorization, rate-limit, and data-minimization risks. Public repositories show that automation interest exists [53] [54], while the CGPA allegation shows why unauthorized experimentation would be harmful [33]. The defensible balance is to permit documented integrations in controlled environments, prohibit live scraping without authorization, and make official APIs or exports safer than unofficial automation.

On time horizon, Reddit complaints range from an older crash report and revaluation question to newer SLCM 2.0, fee, login, and results concerns [10] [48] [32] [34]. This persistence suggests that the university should treat SLCM as a critical academic service rather than a convenience site. It does not prove that every release fails. The immediate priority is measurement: availability, login success by lifecycle state, payment reconciliation age, attendance freshness, marks correction time, and unauthorized-access test results from synthetic accounts.

## VERDICT

**Overall confidence: Moderate for the existence and categories of public student complaints; low for root causes, breach confirmation, current remediation status, and exhaustive coverage.**

The strongest conclusion is that public Reddit material documents recurring student friction around SLCM availability, login and registration transitions, fees, attendance, results, marks, and portal functionality [10] [8] [34]. The evidence is sufficient for a university security club to build a defensive threat model and a responsible-disclosure checklist. It is not sufficient to claim a confirmed breach, a working exploit, a particular framework vulnerability, or a universal failure pattern.

The recommended club deliverable is a redacted evidence register plus a safe test plan: synthetic accounts, written authorization, no live data enumeration, no credential reuse, no CAPTCHA bypassing, no request tricks, no endpoint abuse, and no publication of student data. The university should be asked to validate the technology inventory, reconcile payment and academic records, document identity transitions, and provide a formal channel for privacy reports. Until those steps occur, the public record supports a **defensive risk signal**, not an offensive finding.

## References

1. *Reddit - The heart of the internet*. https://www.reddit.com/r/manipaljaipur/comments/1utflne/slcm_fee_problem/
2. *Reddit - The heart of the internet*. https://www.reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue
3. *Reddit - The heart of the internet*. https://www.reddit.com/r/Manipal_Academics/comments/1993mdc/slcm_login/
4. *Reddit - The heart of the internet*. https://www.reddit.com/r/Manipal_Academics/comments/1daywdf/muj/
5. *Reddit - The heart of the internet*. https://www.reddit.com/r/manipal/comments/17anbg2/slcm_is_literally_ass/
6. *Attendance Lock For Slcm*. https://www.reddit.com/r/manipal/comments/17usdb4/attendance_lock_for_slcm/.json?raw_json=1
7. *Fees Not Showing In Slcm*. https://www.reddit.com/r/Manipal_Academics/comments/1u8476b/fees_not_showing_in_slcm/.json?raw_json=1
8. *Slcm Login*. https://www.reddit.com/r/Manipal_Academics/comments/1993mdc/slcm_login/.json?raw_json=1
9. *Paid My Fees But Still Showing As Pending On Slcm*. https://www.reddit.com/r/Manipal_Academics/comments/1lzf0ht/paid_my_fees_but_still_showing_as_pending_on_slcm/.json?raw_json=1
10. *Slcm Is Literally Ass*. https://www.reddit.com/r/manipal/comments/17anbg2/slcm_is_literally_ass/.json?raw_json=1
11. *Reddit - The heart of the internet*. https://www.reddit.com/r/manipal/search/?q=SLCM&restrict_sr=1&sort=relevance&t=all
12. *Reddit - The heart of the internet*. https://www.reddit.com/r/Manipal_Academics/search/?q=fees&restrict_sr=1&sort=relevance&t=all
13. *Reddit - The heart of the internet*. https://www.reddit.com/r/Manipal_Academics/search/?q=SLCM&restrict_sr=1&sort=relevance&t=all
14. *Reddit - The heart of the internet*. https://www.reddit.com/r/Manipal_Academics/search/?q=portal&restrict_sr=1&sort=relevance&t=all
15. *Reddit - The heart of the internet*. https://www.reddit.com/r/manipal/search/?q=portal&restrict_sr=1&sort=relevance&t=all
16. *Welcome to Reddit*. https://old.reddit.com/r/manipal/comments/17usdb4/attendance_lock_for_slcm/
17. *Welcome to Reddit*. https://old.reddit.com/r/Manipal_Academics/comments/1lzf0ht/paid_my_fees_but_still_showing_as_pending_on_slcm/
18. *Welcome to Reddit*. https://old.reddit.com/r/manipal/comments/17anbg2/slcm_is_literally_ass/
19. *Welcome to Reddit*. https://old.reddit.com/r/Manipal_Academics/comments/1u8476b/fees_not_showing_in_slcm/
20. *Welcome to Reddit*. https://old.reddit.com/r/Manipal_Academics/comments/1993mdc/slcm_login/
21. *Reddit - The heart of the internet*. https://www.reddit.com/r/manipal/comments/1ncl5xy/cgpa_data_leak_of_all_branch_students/
22. *Reddit - The heart of the internet*. https://www.reddit.com/r/manipal/comments/1qa5h99/slcm_20_manipal_situation_summarised/
23. *Manipal Academics*. https://www.reddit.com/r/Manipal_Academics/search.json?q=SLCM&restrict_sr=1&sort=relevance&t=all&raw_json=1
24. *reddit.com*. https://www.reddit.com/r/manipal/search.json?q=SLCM&restrict_sr=1&sort=relevance&t=all&raw_json=1
25. *Attendance Lock For Slcm*. https://www.reddit.com/r/manipal/comments/17usdb4/attendance_lock_for_slcm.json?raw_json=1
26. *How\ Long\ Will\ It\ Take\ For\ The\ Revaluation\ Results*. https://www.reddit.com/r/manipal/comments/v8ax39/how\_long\_will\_it\_take\_for\_the\_revaluation\_results.json?raw_json=1
27. *What\ Is\ Casual\ Term\ Fee\ On\ Slcm*. https://www.reddit.com/r/manipal/comments/1cyd4xv/what\_is\_casual\_term\_fee\_on\_slcm.json?raw_json=1
28. *Slcm Is Literally Ass*. https://www.reddit.com/r/manipal/comments/17anbg2/slcm_is_literally_ass.json?raw_json=1
29. *Slcm Login*. https://www.reddit.com/r/Manipal_Academics/comments/1993mdc/slcm_login.json?raw_json=1
30. *Fees Not Showing In Slcm*. https://www.reddit.com/r/Manipal_Academics/comments/1u8476b/fees_not_showing_in_slcm.json?raw_json=1
31. *How To Change Phone Number In Slcm*. https://www.reddit.com/r/manipal/comments/1ivr2aa/how_to_change_phone_number_in_slcm.json?raw_json=1
32. *Slcm 20 Manipal Situation Summarised*. https://www.reddit.com/r/manipal/comments/1qa5h99/slcm_20_manipal_situation_summarised.json?raw_json=1
33. *Cgpa Data Leak Of All Branch Students*. https://www.reddit.com/r/manipal/comments/1ncl5xy/cgpa_data_leak_of_all_branch_students.json?raw_json=1
34. *Paid My Fees But Still Showing As Pending On Slcm*. https://www.reddit.com/r/Manipal_Academics/comments/1lzf0ht/paid_my_fees_but_still_showing_as_pending_on_slcm.json?raw_json=1
35. *What Is Casual Term Fee On Slcm*. https://www.reddit.com/r/manipal/comments/1cyd4xv/what_is_casual_term_fee_on_slcm.json?raw_json=1
36. *I Need Help With What Ever This Slcm Profile Is*. https://www.reddit.com/r/Manipal_Academics/comments/1uspviv/i_need_help_with_what_ever_this_slcm_profile_is.json?raw_json=1
37. *http://constella.ai/*. http://constella.ai/
38. *We Must Protest Whatever Is Going On With Slcm*. https://www.reddit.com/r/manipal/comments/1q6txrh/we_must_protest_whatever_is_going_on_with_slcm.json?raw_json=1
39. *One Of The Worst Departments In The College*. https://www.reddit.com/r/manipal/comments/1m23kxi/one_of_the_worst_departments_in_the_college.json?raw_json=1
40. *It Appears They Have Removed The Results Tab From*. https://www.reddit.com/r/Manipal_Academics/comments/1plljtw/it_appears_they_have_removed_the_results_tab_from.json?raw_json=1
41. *Can Someone Please Share Me The Parent Slcm Link*. https://www.reddit.com/r/Manipal_Academics/comments/1s8mhsd/can_someone_please_share_me_the_parent_slcm_link.json?raw_json=1
42. *Grades Decreased On Slcm*. https://www.reddit.com/r/Manipal_Academics/comments/1pny6zb/grades_decreased_on_slcm.json?raw_json=1
43. *How Do I Get My Nptel Marks Uploaded To Slcm*. https://www.reddit.com/r/Manipal_Academics/comments/1splp5e/how_do_i_get_my_nptel_marks_uploaded_to_slcm.json?raw_json=1
44. *When Does Slcm Freezecan Profs Take Attendance*. https://www.reddit.com/r/Manipal_Academics/comments/1sgm4q7/when_does_slcm_freezecan_profs_take_attendance.json?raw_json=1
45. *I Am Not Able To Log In To My Slcm Portal Wht To Do*. https://www.reddit.com/r/Manipal_Academics/comments/1m354xl/i_am_not_able_to_log_in_to_my_slcm_portal_wht_to_do.json?raw_json=1
46. *Anyone Facing Any Issues With Slcm*. https://www.reddit.com/r/Manipal_Academics/comments/1i9fyc9/anyone_facing_any_issues_with_slcm.json?raw_json=1
47. *Regarding Slcm Portal*. https://www.reddit.com/r/Manipal_Academics/comments/1v70yng/regarding_slcm_portal.json?raw_json=1
48. *How long will it take for the revaluation results to get updated in the SLCM? : r/manipal*. https://www.reddit.com/r/manipal/comments/v8ax39/how_long_will_it_take_for_the_revaluation_results_to_get_updated_in_the_slcm/
49. *Reddit - The heart of the internet*. https://www.reddit.com/r/manipal/comments/1m0ofr4/has_anyone_used_the_emi_option/
50. *Reddit - The heart of the internet*. https://www.reddit.com/r/manipal/comments/1q6txrh/we_must_protest_whatever_is_going_on_with_slcm/
51. *SLCM-api/SLCMv1 at master · nikeplusdash/SLCM-api · GitHub*. https://github.com/nikeplusdash/SLCM-api/tree/master/SLCMv1
52. *GitHub - utk3012/SLCM: Rest API to scrape data from SLCM Manipal portal · GitHub*. https://github.com/utk3012/SLCM
53. *GitHub - tejaskash/slcm-api: A RESTful API to get attendance and marks data from SLCM Portal at Manipal University, written in Python using Flask. · GitHub*. https://github.com/tejaskash/slcm-api
54. *GitHub - sankalp2004/SLCM-is-Dumb: This extracts cgpa from https://slcm.manipal.edu/ directly and passes captcha · GitHub*. https://github.com/sankalp2004/SLCM-is-Dumb
55. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
