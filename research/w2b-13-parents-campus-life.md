# MUJ SLCM Parent Surface: Public Evidence and Safe Review

## Executive Summary

This report examines the publicly visible MUJ parent-facing ecosystem as of **25 August 2026**. It covers the public parent page, the MUJ SLCM login surface, the official Parent Portal Login Manual, hostel and warden material, transport information, and public announcements. It does not attempt to authenticate, submit credentials, trigger an OTP, alter role values, enumerate accounts, or access any non-public record.

- **Public Parent Surface**: `https://jaipur.manipal.edu/parents.php` is an informational parent resource covering programs, student affairs, hostels, safety, helplines, grievance links, and the academic calendar [2] [2]. It should be treated as a public orientation layer, not as proof of a parent account or SLCM entitlement.
- **Confirmed Parent Authentication**: The official Parent Portal Login Manual links parents to `https://mujslcm.jaipur.manipal.edu/`, describes an OTP sent to the parent's registered mobile number, and states that the dashboard exposes academic and examination information through Reports [30]. The evidence supports an OTP-gated parent workflow, but it does not establish every permission available after login.
- **Provisioning Boundary**: The manual says that a parent whose mobile number is not registered with the university should email `admissions@jaipur.manipal.edu` [30]. This confirms a university-held mobile-number dependency and an official recovery or data-correction channel. It does not disclose who creates the parent record, how a parent is matched to a student, whether two parents may be registered, or how changes are verified.
- **Student Credentials Are Not Parent Credentials**: The official SLCM FAQ describes a student username formed from name and registration number and a password tied to the official Outlook ID [4]. That is student-facing evidence and must not be generalized to parents. The parent manual instead describes OTP authentication [30].
- **Role Switching Is a UI Observation, Not a Security Finding**: The public login form displays Parent Login and Student Login choices and includes `EmailFor` and `LoginFor` fields in the form structure [1] [1] [1] [1]. These are client-visible routing inputs. The public evidence does not show the server authorization decision, so the presence of role fields does not prove account switching, privilege escalation, or an access-control defect.
- **Hostel Access Is Broader Than Portal Access in One Specific Sense**: Public hostel FAQs describe parent involvement in cafeteria visits, consent for city travel, night-out requests, and critical medical notification, while also limiting access to hostel rooms [8] [8] [8]. These are operational and physical rules, not evidence that the same functions are available in SLCM.
- **Transport Evidence Is Route Information, Not a Student Transport Module**: The official contact page describes roads, Rajasthan State Road Transport Corporation buses, the bus stand, the railway station, the airport, and taxis [13]. The official sitemap does not show a dedicated transport page in the reviewed public URL set. The defensible conclusion is that public directions were found; a MUJ-operated parent or student transport service was not established.
- **Public Circulars Are Distributed Across Several Channels**: The announcement page publicly exposes the Parent Portal Login Manual along with admissions, examination, convocation, fee, and calendar items [15] [15] [15] [15] [15]. Public events and academic-calendar pages add other notice types [11] [16]. No public source reviewed establishes a single parent-only circular archive or a public index of SLCM dashboard notices.
- **Security Posture Finding**: The evidence shows a public login form with a request-verification-token field and a Microsoft password-reset destination [1] [1]. That is an implementation observation, not proof that anti-forgery validation, reset authorization, rate limiting, session protection, or object-level access control is correct. Any technical validation must be authorized by MUJ and performed against a designated test account.

The central answer is therefore precise: parents can publicly read institutional and hostel information; an official manual confirms OTP-based parent access to at least academic and examination information; the public record does not reveal the complete parent account lifecycle or the full post-login menu; transport evidence is informational; and public circulars are visible through announcement, calendar, event, and hostel communication channels rather than a demonstrated parent-specific repository.

## Scope, Evidence Model, and Safe Reasoning Summary (cot_explicit)

I cannot provide hidden private chain-of-thought. For a university security club, the useful substitute is an auditable reasoning summary: identify the public artifact, state exactly what it establishes, separate absence of evidence from evidence of absence, and mark every interpretation as an inference. The report uses only publicly accessible university pages, a publicly linked university PDF, and public indexed form metadata. It does not rely on credentials, personal data, a live test account, or unauthorized requests.

The requester supplied a technology fingerprint describing ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 identity. That fingerprint is treated as scope metadata rather than an independently verified finding. None of those version or infrastructure claims is used as a factual conclusion below unless a cited public source states it. The public evidence does support a server-rendered login form, an institutional `@muj.manipal.edu` identity label, and a Microsoft password-reset destination [3] [1] [1]. Those signals are consistent with institutional Microsoft identity, but they do not by themselves prove a specific federation architecture.

### Evidence classification

| Evidence class | What it can establish | What it cannot establish | Report treatment |
|---|---|---|---|
| Official public parent and hostel pages | Published information, contacts, rules, facilities, and links [2] [8] | A parent's authenticated permissions or current account state | High confidence for the text actually published |
| Official Parent Portal Login Manual | The documented OTP path and the dashboard categories named in the manual [30] | The undisclosed account-creation workflow, complete menu, or current implementation behavior | High confidence for stated steps; gaps remain explicit |
| Public SLCM form and indexed markup | Visible login choices, named fields, form destination, and reset destination [1] [1] [1] [1] | Whether the server honors, validates, or restricts each field correctly | Moderate confidence as an implementation observation only |
| Sitemap, announcements, events, and calendar | Public discovery paths and published notice categories [11] [16] [15] | Proof that an unpublished or authenticated page does not exist | Useful for discovery; negative conclusions are qualified |
| Inference | A reasoned interpretation of multiple artifacts | A fact directly asserted by MUJ | Clearly labelled as inference and not presented as a vulnerability |

The reasoning chain is: first, separate the parent-facing public website from the SLCM application; second, use the official manual to answer what the parent workflow actually documents; third, use the SLCM form only to describe visible routing and identity metadata; fourth, treat hostel, transport, and circular pages as separate public channels; and fifth, convert unknowns into questions for an authorized owner rather than guesses. This avoids the common error of treating a button labelled Parent Login as proof of a known credential scheme or treating a hidden role field as proof of broken authorization.

## Parent Landing Page: What Is Public Before Login

The parent page starts with a parent-specific welcome and includes sections labelled `HELLO PARENTS`, `A WALK THROUGH`, `PROGRAMS`, `CULTURAL DIVERSITY`, `STUDENT AFFAIRS`, `HOSTELS`, `SPORTS FACILITIES & OTHER SERVICES`, `ANTI-RAGGING`, `SAFETY & SECURITY`, `HELPLINE`, `ACADEMIC CALENDAR`, and `TESTIMONIALS` [2] [2] [2] [2] [2]. The page describes the parent role as extending beyond simply sending a child to university and frames parents as participants in the student's educational and welfare context [2].

That is a meaningful public surface, but it is not an account-management surface. The page links to program information, campus or service material, anti-ragging information, online grievance registration, and the academic calendar [2] [2] [2]. It gives general admissions and hostel helpline contacts, including admissions email and telephone information and separate boys' and girls' hostel numbers [2]. The evidence reviewed here does not show a Parent Login link, a parent username format, an OTP explanation, or a parent dashboard on this page. That boundary matters because a parent may reasonably start at `parents.php` and assume it is the account entry point when the actual authentication flow is on the SLCM host.

### Public capabilities visible on the parent page

| Public area | What the page exposes | Parent-facing significance | SLCM entitlement established? |
|---|---|---|---|
| Programs | Program and study-stream information with a programs-list link [2] | Helps a family understand the university's academic offering | No |
| Student affairs | Guidance, wellness, health, counselling, and student support material [2] | Explains welfare services before or during enrollment | No |
| Hostels | A parent-oriented description of accommodation and student support [2] | Sets expectations about residence and campus life | No |
| Safety and anti-ragging | Safety priority, anti-ragging measures, and related public links [2] [2] | Provides public risk and support information | No |
| Grievance and services | Online grievance registration, radio, equality, and disadvantaged-groups links [2] | Gives parents public routes to institutional support | No parent account requirement shown |
| Academic calendar | A link labelled Academic Calendar and Holiday List [2] | Provides public scheduling information | No dashboard access shown |
| Contacts | Admissions email, toll-free number, extensions, and hostel helplines [2] | Gives parents a human support path | No |

The decision-ready insight is that `parents.php` is best modelled as a **pre-authentication information layer**. Inference: it may be intentionally designed to answer family questions without exposing student records, but the page itself does not state that design rationale. A club should therefore document the page's links and contact paths separately from SLCM authorization and should not infer that every parent-facing service on the website has a corresponding portal function.

## SLCM Login Surface: Parent and Student Role Selection

The SLCM landing page visibly identifies itself as the MUJ Portal and presents `Sign In`, an `@muj.manipal.edu` label, and a Parent Login option [1] [3]. A structured public capture of the form reports a POST action at the SLCM root and identifies visible Parent Login and Student Login choices [1] [1] [1] [1]. The same capture identifies form names including `EmailFor`, `LoginFor`, `UserName`, `Password`, and a request-verification-token field [1] [1].

### Public form elements and their defensible meaning

| Form or interface element | Public evidence | Defensible interpretation | Security conclusion not supported by the evidence |
|---|---|---|---|
| Parent Login | Visible on the MUJ portal [1] [1] [1] | MUJ presents a parent login path | That any visitor can become a parent or that parent authorization is weak |
| Student Login | Visible beside Parent Login [1] [1] | The same public surface offers a student path | That the two paths share permissions |
| `EmailFor` | Named in the public form structure [1] | A client-visible input used by the login form | That an email suffix alone grants access |
| `LoginFor` | Named in the public form structure [1] [1] | A client-visible role or login-mode input | That the server trusts it without authorization checks |
| `UserName` and `Password` | Named in the public form structure [1] [1] | The form accepts credential fields in its visible structure | Any particular credential format for parents |
| Request-verification-token field | Present in the captured form structure [1] | A visible indication of an anti-forgery design element | That token validation is correctly enforced everywhere |
| Forgot Password | Visible on the portal [1] | A recovery path is advertised | Who owns recovery for parent accounts or how identity is verified |
| Microsoft reset destination | The capture identifies `https://passwordreset.microsoftonline.com/` [1] [1] | The public flow points toward Microsoft password reset for at least one path | Proof of a complete Microsoft 365 federation or parent reset policy |

The requested `EmailFor` and `LoginFor` role-switching question should therefore be answered at two levels. At the presentation level, the page exposes parent and student choices and carries role-related field names in the form. At the authorization level, the available public evidence does not reveal the server-side rule that maps an account to a role or prevents a user from claiming another role. Inference: the fields likely help the application route the selected login mode, but that is not equivalent to permission enforcement. A secure design would derive effective privileges from the authenticated account and server-side records, not from an untrusted hidden field alone. That is a design recommendation, not a finding that MUJ fails to implement it.

The institutional identity signal is similarly limited. The portal displays `@muj.manipal.edu` [3], while the student FAQ refers to the official Outlook ID for the student password [4], and the login capture points to Microsoft's password-reset domain [1] [1]. Inference: these facts are consistent with a Microsoft-managed institutional identity ecosystem. They do not establish whether parents receive Microsoft accounts, whether parents use a separate local OTP identity, or whether a federation service sits between SLCM and Microsoft 365.

For a security club, the safe conclusion is to record the fields and visible paths as attack-surface metadata while refusing to call them a vulnerability. Do not replay requests, modify role fields, submit guessed credentials, or test another person's account without written authorization. The appropriate next artifact is an owner-provided architecture diagram or a designated test environment showing how the server binds `LoginFor` and `EmailFor` to an account.

## Parent Account Provisioning: What the Official Manual Confirms

The strongest source is the official announcement's link labelled `Click Here to download Parent Portal Login Manual`, which points to `https://jaipur.manipal.edu/admin/photo/annoncement/49.pdf` [15]. The extracted manual is titled `Manual for Information Access for the Parent` and directs the parent to `https://mujslcm.jaipur.manipal.edu/` [30]. This is materially stronger than inferring parent credentials from a student FAQ or from third-party applications.

The manual documents the following sequence: a parent uses the SLCM link; the parent mobile number must be registered with the university; the system sends an OTP to the parent's registered mobile number; and the parent enters the OTP and submits it [30]. If the mobile number is not registered, the manual instructs the parent to email `admissions@jaipur.manipal.edu` [30]. After authentication, the manual says that information related to academics and examination is available on the dashboard and directs the parent to Reports [30].

### Provisioning and access matrix

| Question | Confirmed public answer | Evidence strength | What remains unknown |
|---|---|---|---|
| Which application does the parent use? | The MUJ SLCM URL is named in the official manual [30] | High | Whether alternate mobile or app routes are supported |
| What second factor is documented? | An OTP sent to the parent's registered mobile number [30] | High | OTP lifetime, retry limit, rate limit, masking, and lockout behavior |
| What if the phone is not registered? | Email admissions at `admissions@jaipur.manipal.edu` [30] | High | Verification documents, service-level process, and who updates the record |
| Is a parent username format published? | Not in the extracted manual content or the reviewed public login evidence | Low for any assumed format | Whether a hidden identifier, student mapping, or phone number is used |
| Is a parent password published? | The manual documents OTP rather than a parent password [30] | High for the documented path | Whether a password exists for another parent flow |
| What parent information is confirmed after login? | Academics and examination information under Reports [30] | High | Attendance, fees, hostel, transport, notices, and messaging permissions |
| How is the parent tied to a student? | The public manual does not state the matching rule | Not disclosed | Student ID, admission record, family record, consent, or another relationship key |
| Can more than one parent be registered? | Not stated | Not disclosed | Number of contacts, roles, and delegation policy |
| How is a phone number changed? | The manual gives an admissions contact when it is not registered [30] | Partial | Identity checks, update authority, and audit process |

The most defensible provisioning statement is: **the public manual documents an OTP-based access process that depends on a parent mobile number already registered with the university, with admissions as the published fallback for an unregistered number**. Inference: the account or relationship record likely exists in a university-controlled data store before the OTP is issued, because the manual refers to a registered mobile number rather than open self-registration. The source does not say how that record is created, so the inference must not be upgraded into a claim about admission forms, parent declarations, or automatic provisioning.

This distinction also prevents credential leakage. The student FAQ says the registration link is the same SLCM domain and gives a student username example such as `name.registration number`, with a password based on the official Outlook ID [4]. It also says admission-time details can only be changed by the admission department after verification [4]. Those statements concern student records and admission data. They do not establish that a parent should use a registration number, an Outlook password, or a student's account. A responsible club report should explicitly reject that inference.

The parent feature inventory is similarly bounded. Academic and examination information is confirmed by the manual [30]. It is not safe to add attendance, grades, fees, transport, hostel allotment, out-pass status, or circulars merely because those categories are plausible in a student lifecycle system. They remain unanswered unless an authorized parent manual, dashboard screenshot supplied by MUJ, role-permission matrix, or owner-confirmed test account documents them.

## Hostel and Warden Pages: Public Information and Parent Touchpoints

The chief warden page welcomes hostel students, their parents, and visitors and describes accommodation amenities, wardens, building executives, security, medical support, and other facilities [6] [6]. Its navigation exposes labels such as Room Description, Hostel Fee, Mess Fee, Rules and Regulations, Medical Facilities, and FAQs About Hostel Accommodation [6]. The separate hostel FAQ gives more specific operational rules, including room types, blocks, fees, meals, visitors, permissions, and medical escalation [8] [8].

The public FAQ draws a clear physical-access boundary: parents and friends are not permitted to enter hostel rooms, while parents may have breakfast and lunch in hostel cafeterias on a cash-and-carry basis [8]. A student going into the city requires prior Chief Warden approval and parent consent, and a night out requires approval from the concerned warden with a parent request on the out-pass [8]. In a critical medical case, the warden or caretaker will inform the parents after the student is referred for care [8]. These are concrete parent-facing processes, but they are not described as SLCM functions.

### Hostel and warden parent-facing matrix

| Surface or process | Publicly documented parent relationship | What a parent can infer safely | SLCM parent access proven? |
|---|---|---|---|
| General hostel information | Facilities, utilities, security, mess, recreation, and medical support are described [6] [8] | Parents can review public accommodation expectations | No |
| Room inspection or visit | Parents and friends may not enter hostel rooms under the stated rule [8] | Physical access is restricted by hostel policy | No |
| Cafeteria | Parents may have breakfast and lunch in hostel cafeterias on a cash-and-carry basis [8] | A limited on-site family visit is contemplated | No |
| City visit | Chief Warden approval and parent consent are required [8] | Parent consent is an operational control for a student's outing | No |
| Night out | Warden approval and a parent request on the out-pass are required [8] | A parent request may be part of a paper or operational workflow | No portal implementation stated |
| Medical incident | Warden or caretaker informs parents in a critical case [8] | Parent notification is an institutional duty described on the page | No |
| Hostel payment | The fee page publishes charges and says room allotment follows receipt and verification of full fees [9] | Families can understand public payment and allotment conditions | A logged-in room-booking portal is mentioned for payment modes [9], but not an SLCM parent feature |
| Rule changes | No individual intimation is promised; students and families are directed to notice board or communications from the Chief Warden or management [9] | Rule updates may be distributed through several channels | No public parent circular dashboard proven |
| Warden contact | The page publishes university and Chief Warden contact information [6] | Parents have a public human escalation path | No |

For context, the public 2026-27 double-occupancy fee table lists hostel accommodation at INR 167,372, housekeeping at INR 15,378, refundable security at INR 25,475, and a total of INR 208,225; it separately lists laundry at INR 8,810 and health club or gym options at INR 12,750 [9]. These figures are public fee information for the stated academic year, not evidence that a parent dashboard displays a fee ledger. Parents should confirm current charges directly with the university or hostel management because public fee pages can change.

The case study here is the night-out rule. It shows the difference between a parent as a human consent provider and a parent as an SLCM user: the public page says the student needs a parent request on an out-pass [8], but it does not say that the request is submitted through SLCM. Inference: any digital out-pass integration, if it exists, cannot be established from this page. The correct security question is not "can a parent edit an out-pass?" but "which authorized system, if any, records the request, and what identity proof does it use?"

The warden page also publishes a Chief Warden contact number and the admission contact path [6] [6]. The SLCM FAQ separately lists `chief.warden@jaipur.manipal.edu` and phone `0141 3999 108` for hostel-related help [4]. These contacts are useful for legitimate support, but they should not be used to request or disclose another person's records.

## Transport: Campus Directions Versus a Parent Transport Service

The official contact page says Jaipur is linked by road transport and describes Rajasthan State Road Transport Corporation buses between Jaipur and Delhi, with buses approximately every half hour and typical journeys of six hours by Volvo or six to seven hours by other deluxe buses [13]. It states that the Jaipur bus stand is about 25 km from MUJ, the railway station is about 24 km away, and the airport is about 27 km away; it also mentions prepaid taxi or cab service [13].

### Transport evidence table

| Transport topic | Public evidence | What it supports | What it does not support |
|---|---|---|---|
| Road access | General road and road-transport connectivity is described [13] | Directions and arrival planning | A university-operated shuttle |
| RSRTC buses | Jaipur-Delhi service and approximate frequency are described [13] | Public intercity travel information | A MUJ parent or student bus pass |
| Bus stand | Jaipur bus stand is stated to be about 25 km from MUJ [13] | Last-mile planning | A university pickup route |
| Railway | Jaipur Railway Station is stated to be about 24 km away [13] | Rail arrival planning | A station transfer service |
| Airport | Airport distance is stated as about 27 km [13] | Air arrival planning | A scheduled airport shuttle |
| Taxi | Prepaid taxi or cab service is mentioned [13] | General arrival option | A university transport booking module |
| Dedicated transport page | No dedicated transport URL is visible in the reviewed official sitemap | No public transport page was located in that URL inventory | Proof that no private or unpublished transport service exists |

The decision is to classify transport as **public route-to-campus information**. Inference: parents may use this information to plan a visit, but the reviewed evidence cannot answer whether MUJ operates buses for students, whether a vendor manages routes, or whether SLCM displays transport details. The absence of a sitemap entry is a discovery limitation, not proof of nonexistence. An authorized information request to General Services or the university transport owner would be the appropriate next step.

## Public Circulars, Announcements, Events, and Calendars

The announcement page is the most important public notice source because it explicitly publishes the Parent Portal Login Manual link [15] [15]. The same page includes public items such as CUET admission notices [15], a PhD interview result [15], a convocation notification [15], an annual course fee item [15], and an academic calendar item [15]. These examples show that the announcement page is a general university notice board rather than a parent-only circular stream.

The events page provides a second public channel. It lists an upcoming MUJ Alumni Meet dated 24 October 2026 at MUJ and also displays past events with dates, venues, and read-more links [11]. The academic-calendar page lists public calendar entries for 2026-27, 2025-26, and 2024-25 variants [16]. The sitemap identifies announcement and news pages as well as event and calendar paths.

### Public notice channel matrix

| Channel | Exact URL | Public material confirmed | Parent-specific or SLCM-specific? |
|---|---|---|---|
| Parent landing page | `https://jaipur.manipal.edu/parents.php` | Parent information, helplines, grievance and calendar links [2] [2] | Parent-oriented, but not a circular archive |
| Announcement page | `https://www.jaipur.manipal.edu/announcement.php` | General notices plus the Parent Portal Login Manual link [15] | Parent-specific manual exists; general feed otherwise |
| Parent manual PDF | `https://jaipur.manipal.edu/admin/photo/annoncement/49.pdf` | OTP and academic/examination dashboard instructions [30] | Parent-specific, but static and public |
| Events page | `https://jaipur.manipal.edu/events.php` | Upcoming and past events with dates and venues [11] | General public events, not parent circulars |
| Academic calendar | `https://jaipur.manipal.edu/academics-calender.php` | Public academic calendar entries [16] | General academic information |
| News page | `https://jaipur.manipal.edu/news.php` | Sitemap-discovered news path | The reviewed evidence does not establish a parent-only feed |
| Hostel fee and rules communications | `https://jaipur.manipal.edu/hostel-fees.php` | Fee and rule-change communication instructions [9] | Parent-relevant, but not shown as SLCM notices |

The hostel fee page is especially useful for understanding distribution risk. It says that no individual intimation of rule or policy changes will be given to students, parents, or guardians, and directs readers to the notice board or communications sent by the Chief Warden or management [9]. This means that a parent may need to monitor several official channels. It also means that a public `announcement.php` page should not automatically be treated as the authoritative location for every operational hostel circular.

There is a small discoverability inconsistency: `robots.txt` disallows `/admin/` for crawlers while allowing images and PDFs to be indexed [10], and the announcement page publicly links the manual under `/admin/photo/annoncement/49.pdf` [15]. This is not evidence of an access-control defect. Inference: it is a content-management and discoverability issue that the site owner may wish to reconcile so that an official manual remains reliably reachable and consistently indexed. A security club should report this as a documentation and operational-consistency observation, not as a bypass opportunity.

The unanswered circular question is therefore narrow: the public evidence confirms several general notice channels and one parent-specific login manual, but it does not demonstrate whether a logged-in parent sees circulars, hostel notices, transport alerts, attendance warnings, or messages in SLCM. That requires an owner-supplied parent role matrix or an authorized test session.

## Security Interpretation and Authorized Club Recommendations

The public artifacts support a threat model with five layers: public information, login routing, identity recovery, parent data, and operational communications. The key security principle is to avoid confusing visibility with authorization. A form can expose a field without trusting it; a public manual can document a process without revealing an account; and a hostel page can require a parent request without implementing that request in SLCM.

### Observation to mechanism to implication to recommendation

| Observation | Mechanism or explanation | Implication | Safe recommendation for MUJ or an authorized club |
|---|---|---|---|
| Parent and student choices share a visible login surface [1] [1] | The interface presents role selection before authentication | Role metadata may be user-controlled at the browser boundary | Verify server-side role binding with a designated test account and written scope; do not test live users |
| `EmailFor` and `LoginFor` are visible form fields [1] [1] | The client submits role-related data in a form structure | Hidden or client-side values must not be treated as the authorization boundary | Review controller and authorization logic, or obtain a permission matrix from the owner |
| Request-verification-token field is present [1] | The form includes an anti-forgery design element | Presence alone does not prove validation on every state-changing action | Review framework configuration and authorized negative tests without exposing tokens |
| Parent authentication uses a registered mobile and OTP [30] | The identity proof depends on a university-held contact channel | Phone ownership, change control, retry limits, and stale records become important | Confirm phone update verification, OTP expiry, retry throttling, audit logs, and account deprovisioning |
| Unregistered numbers are directed to admissions [30] | A human support channel handles missing identity data | Social engineering and misrouting are possible operational risks | Use an official support workflow with identity verification, ticketing, least privilege, and audit trails |
| Academic and examination data are named on the dashboard [30] | Parent access includes at least those categories | Student data confidentiality and object-level authorization matter | Verify that a parent can see only the correctly associated student and only the intended fields |
| Public manual and contact data are available [15] [2] | Legitimate users can self-help without logging in | Documentation can also help impersonation attempts if process details are excessive | Keep instructions current, avoid publishing secrets, and monitor support abuse without blocking legitimate parents |
| Hostel rules depend on parent consent and requests [8] | Physical or administrative workflows involve parents | The real source of truth may be an out-pass or warden process rather than SLCM | Map ownership of each record and ensure changes are auditable across systems |
| Transport pages are not established [13] | Public evidence covers arrival directions only | A club could mislabel a third-party or unrelated system as MUJ transport | Confirm the service owner before including any transport endpoint in scope |

The most important authorized test cases are conceptual rather than exploit instructions. The owner should verify that a parent account cannot select a different child, that a student account cannot be treated as a parent merely by changing a role field, that a reset or OTP request does not disclose whether arbitrary numbers are registered, and that logout and account changes invalidate old sessions. These are acceptance criteria for a controlled assessment, not directions for probing the live application.

A second recommendation is data minimization. The manual confirms academics and examinations, but it does not enumerate the fields. MUJ should publish or provide to authorized reviewers a parent role matrix that distinguishes grades, attendance, fees, hostel records, out-passes, transport, circulars, and messaging. Each row should state view, download, submit, approve, and administrative actions. This avoids the ambiguity created when a public label says Parent Login but the public documentation names only Reports.

A third recommendation is documentation governance. The parent manual should carry a visible revision date and owner, link from the parent page or a stable document library, and remain consistent with the announcement index and crawler policy. The public site currently links the manual from an announcement while the robots policy disallows the `/admin/` path [10] [15]. This is an operational quality issue and a continuity risk for legitimate parents, not a reason for a club to attempt restricted retrieval.

## Synthesis: Five Surfaces, Five Different Trust Boundaries

The evidence does not describe one unified "parent portal" in which every parent-facing activity occurs. It describes a set of surfaces with different mechanisms, audiences, and levels of certainty.

| Surface | Mechanism | Confirmed parent scope | Evidence horizon | Main trade-off |
|---|---|---|---|---|
| `parents.php` | Public informational website [2] | Programs, welfare, hostels, safety, contacts, grievance and calendar links [2] | Pre-authentication | Broad discoverability, no student-specific data shown |
| SLCM login page | Public form with Parent and Student choices and role-related fields [1] [1] [1] [1] | A parent login path is presented | Interface-level | Convenient role selection, but server authorization is not visible |
| Parent Login Manual | OTP sent to registered parent mobile; Reports includes academics and examination [30] | At least academic and examination information after parent authentication | Documented operational flow | Useful self-service, but provisioning and full permissions remain opaque |
| Hostel and warden pages | Public rules, consent, approval, contacts, and medical notification [6] [8] | Family participation in defined physical and administrative processes | Public operational policy | Clear boundaries, but no demonstrated SLCM integration |
| Announcements, events, calendars, and transport | Public notices and directions [13] [11] [16] [15] | General notices and campus-arrival planning | Public communication | High reach, but distributed channels can create version and ownership ambiguity |

Three tensions are decision-relevant. First, the parent page presents parents as active participants in education and welfare, while it does not explain the SLCM path [2] [2]. The public website and authenticated portal are therefore complementary but weakly joined from a user's perspective. Second, the login page visibly offers role selection, while the public evidence does not expose the server-side authorization model [1]. The interface makes the distinction visible but cannot establish whether the security boundary is sound.

Third, the manual documents a concrete parent workflow, but only for OTP and academic or examination Reports [30]. Hostel pages, by contrast, describe parent consent and warden notification in operational terms [8] [8]. This divergence suggests that the term "parent access" covers different mechanisms: portal viewing, human consent, and institutional notification. Inference: treating them as one permission set would create an inaccurate threat model.

The practical synthesis is to build an owner-confirmed data-flow map with separate nodes for the public website, SLCM parent identity, student identity, admissions support, hostel or warden processes, and public notice channels. The first priority is not live testing. It is confirming which system owns the parent-student relationship, which system owns OTP and reset events, and whether hostel, transport, and circular data ever cross into the parent dashboard.

## VERDICT

**Overall confidence: High for the public surface inventory and the documented OTP workflow; medium for the interpretation of the SLCM form; low for the complete parent account lifecycle and full post-login feature set.**

| Verdict question | Conclusion | Confidence | Reason |
|---|---|---|---|
| What can any parent read without logging in? | Public program, welfare, hostel, safety, grievance, calendar, contact, event, announcement, and route information is available across the cited pages [2] [13] [11] [15] | High | Directly stated on official public pages |
| Is there an official parent login? | Yes. The SLCM page presents Parent Login and the official manual directs parents to the SLCM URL [1] [30] | High | Two official artifacts agree |
| How are parents authenticated? | The manual documents an OTP sent to the registered parent mobile, with admissions as the fallback for an unregistered number [30] | High | Direct manual statement |
| What can parents access after login? | Academics and examination information through Reports are confirmed [30] | High for those categories | Direct manual statement |
| Are attendance, fees, hostel, transport, out-pass, circular, or messaging permissions confirmed? | No, not by the public sources reviewed | Low or unresolved | The manual does not enumerate them |
| Is the `EmailFor` or `LoginFor` presentation evidence a vulnerability? | No conclusion of vulnerability is justified | High confidence in restraint | Public form metadata does not reveal server authorization [1] [1] |
| Is a MUJ student transport portal confirmed? | No. Public route information is confirmed, but a dedicated parent or student transport service is not | Medium | Contact page and sitemap evidence are informative, not exhaustive [13] |
| Is there one public parent circular repository? | Not demonstrated. Notices are distributed across announcements, events, calendars, hostel communications, and possibly authenticated systems | Medium-high | Several public channels are confirmed; a unified repository is not [9] [11] [16] [15] |
| Is the supplied version and infrastructure fingerprint independently verified here? | No. It remains requester-provided scope metadata | High | No cited source in this report establishes those versions |

The final risk judgment is **informational exposure and documentation ambiguity, not a demonstrated exploit**. The manual's OTP procedure is useful and appropriate to legitimate parents, but the public record does not reveal enough to assess the strength of phone-number registration, support verification, role binding, or object-level authorization. The university security club should request written authorization, a non-production test account, an owner-approved permission matrix, and a contact for responsible disclosure. It should not attempt to bypass the login, alter hidden fields, guess credentials, trigger OTPs for real users, or inspect another student's data.

## References: Exact URLs

| Source ID used in inline citations | Exact URL | Use in this report |
|---|---|---|
| 46 | https://jaipur.manipal.edu/parents.php | Parent landing page |
| 47 | https://mujslcm.jaipur.manipal.edu/ | SLCM landing page |
| 103 | https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf | Official SLCM FAQ and student provisioning |
| 104 | https://mujslcm.jaipur.manipal.edu/Home/Index | SLCM login page and institutional identity label |
| 131 | https://jaipur.manipal.edu/chiefwardensmessage.php | Chief Warden message and contacts |
| 132 | https://jaipur.manipal.edu/faqs-regarding-hostel.php | Hostel FAQ and parent-related rules |
| 133 | https://jaipur.manipal.edu/hostel-fees.php | Public hostel fees and communications policy |
| 134 | https://jaipur.manipal.edu/hostel-facility.php | Public hostel facility information |
| 165 | https://jaipur.manipal.edu/contact-university.php | Campus directions and university contacts |
| 167 | https://jaipur.manipal.edu/events.php | Public event listings |
| 185 | https://www.jaipur.manipal.edu/announcement.php | Public announcement page |
| 194 | https://jaipur.manipal.edu/academics-calender.php | Public academic-calendar listing |
| 199 | https://mujslcm.jaipur.manipal.edu/ | Public SLCM form structure and login metadata |
| 204 | https://jaipur.manipal.edu/robots.txt | Public crawler policy |
| 205 | https://jaipur.manipal.edu/sitemap.xml | Public URL inventory |
| 221 | https://www.jaipur.manipal.edu/announcement.php | Announcement entry linking the parent manual |
| 299 | http://jaipur.manipal.edu/admin/photo/annoncement/49.pdf | Extracted official Parent Portal Login Manual; the announcement links the HTTPS form of the same PDF |

This report intentionally treats the manual's published content as the authority for the documented parent flow and treats all unlisted permissions as unresolved rather than assumed.

## References

1. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
2. *Welcome Parents | Manipal University Jaipur*. https://jaipur.manipal.edu/parents.php
3. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
4. *Frequently Asked Questions and Contacts for SLCM Registration*. https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf
5. *Hostel Helpline - Manipal University Jaipur*. https://jaipur.manipal.edu/hostel-helpline.php
6. *Chief Warden's Message - Manipal University Jaipur*. https://jaipur.manipal.edu/chiefwardensmessage.php
7. *MUJ Hostel - Manipal University Jaipur *. https://jaipur.manipal.edu/hostel-facility.php
8. *FAQs - Manipal University Jaipur *. https://jaipur.manipal.edu/faqs-regarding-hostel.php
9. *Hostel Fee - Manipal University Jaipur*. https://jaipur.manipal.edu/hostel-fees.php
10. *jaipur.manipal.edu*. https://jaipur.manipal.edu/robots.txt
11. *Events - Manipal University Jaipur *. https://jaipur.manipal.edu/events.php
12. *jaipur.manipal.edu*. https://jaipur.manipal.edu/sitemap.xml
13. *Contact Us - Manipal University Jaipur *. https://jaipur.manipal.edu/contact-university.php
14. *Manipal University Jaipur - 71 years of legacy of Manipal Education*. https://jaipur.manipal.edu/
15. *Announcement - Manipal University Jaipur Announcement*. https://www.jaipur.manipal.edu/announcement.php
16. *Academic Calendar*. https://jaipur.manipal.edu/academics-calender.php
17. *News - Manipal University Jaipur *. https://jaipur.manipal.edu/news.php
18. *Student Portal*. https://student.mujonline.com/
19. *MU SLcM*. https://slcm.manipal.edu/
20. *Manipal Slcm Jaipur*. https://www.instagram.com/popular/manipal-slcm-jaipur?hl=en
21. *Change Password*. https://slcm.manipal.edu/StudentChangePassword.aspx
22. *Manipal University*. https://muj.slcm.jaipur.manipal.edu/
23. *SLCM Mobile - MUJ*. https://slcm-client-unoff.vercel.app/
24. *Manipal University - mujslcm.jaipur.manipal.edu*. https://mujslcm.jaipur.manipal.edu/Student/Academic/AttendanceSummaryForStudent
25. *Parents | Manipal Academy of Higher Education (formerly ...*. https://www.manipal.edu/mu/parents.html
26. *MUJStella - Student Platform for Manipal University Jaipur*. https://mujstella.in/
27. *Login | Register | RemotLog | MUJ LIBRARIES (Offline Students ...*. http://jaipur-manipal-edu.muj.remotlog.com/login
28. *Manipal University Jaipur - Online Manipal*. https://muj.onlinemanipal.com/
29. *Library Portal | Student Portal*. https://www.mujlibrary.live/
30. *PowerPoint Presentation*. http://jaipur.manipal.edu/admin/photo/annoncement/49.pdf
