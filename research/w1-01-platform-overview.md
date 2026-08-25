# MUJ SLCM: Public Platform Map and Student Journey

## Executive Summary

- **Administrative Portal, Not Proven LMS**: MUJ SLCM is the university's authenticated student-administration portal. Public evidence ties it to new-student profile registration, attendance, annual academic-fee payment, and parent/student access. It should not be described as MUJ's learning-management system because no public MUJ source identifies it as a course-content or teaching platform [15][9][10][25].

- **Authentication Boundary**: The public page at `https://mujslcm.jaipur.manipal.edu/` exposes username and password entry, Student Login, Parent Login, and Forgot Password. The form posts locally to `/`, while Forgot Password leaves SLCM for Microsoft's self-service password-reset service. This is evidence of shared Microsoft-managed credentials, but not by itself evidence of SAML, OAuth, OpenID Connect, or seamless Entra ID SSO [5][16].

- **Documented Onboarding Chain**: The strongest official student journey is Office 365 activation -> mandatory multi-factor authentication -> SLCM profile completion -> generation of two signed Student Profile Form copies -> in-person document verification. MUJ's orientation page explicitly links the Office 365 SOP, SLCM FAQ, and SLCM Profile Registration Guide [9][16].

- **Feature Evidence Is Uneven**: Attendance has an indexed official route, `https://mujslcm.jaipur.manipal.edu/Student/Academic/AttendanceSummaryForStudent`, but unauthenticated visitors see only the login page. Candidate grade and timetable routes also return the login surface, which confirms access control but does not prove the post-login screens' contents [25][28][32].

- **Payments Are Split Across Services**: MUJ's current public payment page directs existing students' academic fees to SLCM and hostel/mess fees to SpaceBasic. Certificate and document requests use `https://rzp.io/l/lCB8nGo7Wj`, with UPI/Paytm named by MUJ. A separate NTT DATA Payment Services page at `https://muj-payservices.nttdatapay.com/DirectPay/MUMessFee` is labeled for mess fees. The public evidence does not name the processor behind SLCM academic-fee checkout [10][14][27].

- **Microsoft Integration Is Real but Scoped**: MUJ publishes a June 2025 Office 365 SOP for students and employees. It requires Microsoft 365 sign-in, a new password, and mandatory MFA through Microsoft Authenticator, phone, or personal email. No public SLCM page inspected exposed a SAML/OAuth authorization endpoint, so the safe conclusion is credential and recovery integration, not proven federated SSO [16].

- **Portal Ecosystem Is Fragmented**: SLCM, DigiLibrary, SpaceBasic, Online Manipal, the MUJ alumni site, and MAHE's `sis.manipal.edu`/`slcm.manipal.edu` are separate services with different audiences. Students should not reuse instructions across these systems without checking the institution and service scope [18][8][7][12].

- **Support Must Be Routed by Failure Type**: SLCM/AMS profile or login issues go to DMS/AMS; Office 365 failures go to IT Infra; fee issues go to Student Finance; exam documents go to the examination helpdesk; incorrect admission data goes to Admissions. MUJ does not publicly identify a person with the exact title "SLCM nodal officer" in the sources reviewed [15][14][10].

**Decision-ready insight:** Treat SLCM as MUJ's protected system of record for student administration. Treat Microsoft 365, SpaceBasic, DigiLibrary, NTT DATA, Razorpay, Online Manipal, and MAHE SIS as adjacent systems, not interchangeable parts of one portal.

## Scope, Method, and Evidence Grades

This report covers pages reachable without credentials, official MUJ documents linked from `https://jaipur.manipal.edu`, indexed authenticated-route names that resolve to the login surface, official app-store listings, and clearly labeled third-party student guides. It does not attempt to sign in, use a student's credentials, bypass access controls, enumerate private records, or infer private API behavior.

I cannot provide private hidden chain-of-thought. The reproducible analytical rationale is instead summarized here:

1. A feature is marked **verified** only when an MUJ page, an official PDF, or an exact MUJ route supports it.
2. A route that merely returns the login page proves that the route is protected; it does not prove what data or controls appear after login.
3. A third-party student guide can document user experience, but it is labeled secondary evidence and cannot override MUJ's official pages.
4. A processor is attributed only to the service for which it is publicly shown. Razorpay's certificate link is not silently generalized to annual tuition, and NTT DATA's mess-fee form is not generalized to all MUJ fees.
5. An absence finding is bounded to the public surfaces reviewed. "Not publicly verified" does not mean "does not exist after login."

| Evidence grade | Meaning | Example |
|---|---|---|
| A - First-party explicit | Official MUJ page or PDF directly states the fact | SLCM annual-fee route; Office 365 MFA; SLCM registration FAQ |
| B - First-party route | Exact MUJ URL exists but unauthenticated content is hidden | Attendance, candidate grades, and candidate timetable routes |
| C - Official adjacent service | Store, processor, or Manipal-group page confirms a scoped integration | SpaceBasic app; NTT DATA mess-fee form; MAHE SIS |
| D - Independent secondary | Student-built or third-party source, clearly disclosed | betterSLCM attendance guide; MUJStella |
| Not verified | No public evidence sufficient to make the requested claim | Separate core-campus LMS; SLCM transport module; public staff dashboard |

The practical limitation is important: the public root page contains only the authentication boundary. No ethical public-web review can inventory "every" post-login button without an authorized account. Accordingly, the feature table below separates directly evidenced functions from plausible but unverified dashboard claims.

**Decision-ready insight:** The most reliable report is a boundary map, not a simulated authenticated tour. It shows exactly where public evidence ends.

## The Public Login Surface and Authentication Boundary

### Canonical and alternate entry points

The canonical URL is `https://mujslcm.jaipur.manipal.edu/`. Its public title is "Manipal University," and its visible page says "WELCOME TO MUJ PORTAL," "Sign In," and "Parent Login" [5]. The indexed `https://mujslcm.jaipur.manipal.edu/Home/Index` route presents the same login surface rather than a public dashboard [3]. It is therefore accurate to call `/Home/Index` a public login-page route, but the capture does not prove that every successful login redirects there.

A second hostname, `https://muj.slcm.jaipur.manipal.edu/`, also resolves to an MUJ-branded sign-in page. Public search results associate the canonical host with `@muj.manipal.edu` and the alternate host with `@jaipur.manipal.edu`. MUJ's separate DigiLibrary explicitly accepts both domains, confirming that both are institutional email patterns [18]. The official SLCM FAQ, however, gives the username pattern as `name.registration number`, for example `garv.2506040062`, and says the password is the one used for the official Outlook ID [15]. Users should follow the prompt on the particular login page rather than assuming that the full email address is always required.

### Form behavior visible in public source

Public HTML inspection shows:

- a local HTML form with `method="post"` and `action="/"`;
- `UserName` and `Password` fields;
- an anti-forgery request token;
- a password reveal/hide control;
- a username validation rule of 2 to 50 characters;
- Student and Parent mode buttons; and
- hidden `LoginFor` state, with the client script setting student and parent modes separately.

These are implementation observations from the unauthenticated page, while the citable visible labels remain the welcome, sign-in, and parent-login text [5]. A parent can therefore choose a dedicated mode, but no public source describes how a parent account is issued or what a parent can view.

The Forgot Password anchor points to `https://passwordreset.microsoftonline.com/`. MUJ's official recovery SOP also takes users through Microsoft sign-in, "Forgot my password," CAPTCHA, two-step verification, and creation of a new password [16]. This explains why changing the Outlook password can restore SLCM access: MUJ's FAQ tells students that the SLCM password follows the official Outlook ID [15].

### What the public login does not establish

No unauthenticated SLCM source inspected exposed a SAML request, OAuth authorization endpoint, OpenID Connect metadata link, or visible "Sign in with Microsoft" control. The login form accepts credentials locally and sends password recovery to Microsoft. That pattern is compatible with synchronized credentials, backend directory validation, or federation hidden after submission, but public evidence cannot distinguish among them.

The public root and `/Home/Index` pages also expose no dashboard announcements, alert feed, examination notice list, or timetable. Those items may appear after authentication; they are simply not on the captured public page [5][3]. Online Manipal has a separate notices page, but that belongs to the online-program ecosystem and must not be represented as the core SLCM notice board.

**Case study - password failure:** A new student whose SLCM password fails should first verify the documented username format and Outlook password. If the Outlook account also fails, MUJ directs the student to reset the Microsoft password and then contact IT Infra if unresolved [15]. This workflow reveals the integration mechanism more reliably than assuming a particular SSO protocol.

**Decision-ready insight:** Publicly, SLCM is a local login boundary with Microsoft-backed password lifecycle. Calling it "Microsoft SSO" would exceed the evidence.

## Student Journey: Outlook Activation to Verified Profile

MUJ's Orientation Program page provides the clearest official onboarding sequence. It links three separate resources: the Office 365 and Outlook setup SOP, "FAQs for SLCM Registration," and the "SLCM Profile Registration Guide" [9]. The exact profile-guide URL is `https://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf`. Although that PDF did not return extractable text during this review, its title and link are present on the official orientation page, so its existence is verified.

### Stage 1: Activate the university identity

The Office 365 SOP is titled "How To Setup Your Office 365 Mail ID," version 1.0, effective June 2025, for students and employees [16]. It instructs the user to open `https://login.microsoftonline.com/`, enter the University Mail ID and temporary/current password, set a new password, and continue to the additional-security-information screen [16].

MFA is mandatory. The documented methods include Microsoft Authenticator, phone/SMS, and personal email. Authenticator setup uses a work or school account and QR-code scan; successful completion sends the user to the Microsoft 365 home page and Office applications [16]. The same SOP documents how to add or change security methods through View Account -> Security Info -> Add Method [16].

### Stage 2: Enter SLCM

The official SLCM FAQ gives `https://mujslcm.jaipur.manipal.edu/` as the registration link. It says the username follows a `name.registration number` pattern and uses the official Outlook password [15]. On the public page, the student selects Student Login; a parent has a separate Parent Login mode [5].

### Stage 3: Complete the student profile

The orientation instructions require students to complete the Student Profile in SLCM, generate the Student Profile Form, print two copies, and self-sign them [9]. This is the most defensible public evidence for SLCM's registration/profile function. The FAQ also says that personal details originally supplied during admission can be changed only after Admissions verifies them, which implies that SLCM profile data is tied to the admission record rather than freely editable by the student [15].

The FAQ addresses missing mandatory documents by sending the student to Admissions, at `admissions@jaipur.manipal.edu` and extensions 142, 257, or 297 [15]. That proves document handling is part of the onboarding process, but it does not prove that every document is uploaded inside SLCM. The public evidence supports profile generation and document verification, not a generalized "document upload module."

### Stage 4: Report and verify

For Orientation 2026, MUJ instructed students to report by 9:00 AM, with document verification beginning at 9:15 AM. The page listed weekday assistance hours of 9:00 AM to 6:00 PM [9]. SLCM profile help used extensions 738/784 and 481/263, while Outlook/IT issues used IT Helpdesk extension 144 and mobile `9358009341` [9].

**Case study - incorrect personal data:** A student's name or other personal detail is wrong in SLCM. The student should not repeatedly edit or recreate the profile. MUJ says the admission-time data can be changed only by Admissions after verification [15]. The mechanism is controlled correction of the system-of-record data; the implication is that Admissions, not IT, owns this failure.

**Decision-ready insight:** MUJ's documented journey is identity first, profile second, physical verification third. Directing all onboarding problems to one generic helpdesk would ignore the published ownership model.

## Exact Feature Verification Matrix

| Requested feature | Public status | Exact public URL or surface | What can be stated safely |
|---|---|---|---|
| Student login | Verified | `https://mujslcm.jaipur.manipal.edu/` | Username/password login with a Student Login mode [5] |
| Parent login | Verified | Same root URL | Dedicated Parent Login mode is publicly visible; account provisioning and permissions are not public [5] |
| New-student registration/profile | Verified | Root URL plus `https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf` | Complete profile, generate two copies, self-sign, and submit for verification [15][9] |
| Attendance | Route verified; data gated | `https://mujslcm.jaipur.manipal.edu/Student/Academic/AttendanceSummaryForStudent` | Exact route exists and returns login when unauthenticated; no public student data is exposed [25] |
| Timetable | Not publicly verified as a post-login feature | Candidate `https://mujslcm.jaipur.manipal.edu/Student/Academic/TimeTableForStudent` | Candidate route returns only login. Official examination timetables are separately published on the examination page [28][14] |
| Marks and grades | Secondary claim; official route content gated | Candidate `https://mujslcm.jaipur.manipal.edu/Student/Academic/GradesForStudent` | Candidate route returns login. Independent betterSLCM material claims grades, CGPA, and internal marks, but it is not MUJ authority [32][33] |
| Grade cards/GPA/CGPA | Verified as MUJ exam outputs, not specifically as SLCM screens | `https://www.jaipur.manipal.edu/img/pdf/exam/Student%20Examination%20Handbook%202023-24%20(11.08.2023).pdf` | Official handbook defines grade cards, GPA, and CGPA; it does not state they are delivered through SLCM [29] |
| Annual academic-fee payment | Verified | Root URL, linked by `https://jaipur.manipal.edu/pay-fee-online.php` | Existing students are directed to SLCM; checkout processor is not publicly named [10] |
| Fee receipts | Not first-party verified as a dashboard feature | Authentication-gated | Third-party material claims fee receipts, but no official public dashboard documentation was found |
| Exam form or exam registration | Not verified as SLCM | `https://jaipur.manipal.edu/examination.php` | MUJ publishes application formats and some online forms after notifications; no public source ties general exam registration to SLCM [14] |
| Course registration | Not publicly verified | Authentication-gated | The SLCM FAQ documents first-year profile registration, not semester course registration [15] |
| Hostel and mess | Verified as adjacent service | SpaceBasic app; `https://muj-payservices.nttdatapay.com/DirectPay/MUMessFee` | Current MUJ page directs hostel/mess fees to SpaceBasic; NTT DATA also exposes a scoped mess-fee form [10][27] |
| Transport | Not publicly verified | None found | No official public SLCM transport page or current MUJ transport portal was verified |
| Library | Verified as a separate portal | `https://mujlibrary.live/` | DigiLibrary tracks books, renewals, and catalog access using either institutional email domain; no SLCM linkage is stated [18] |
| Document upload | Partially evidenced | SLCM profile and orientation documents | Profile form generation and mandatory-document verification are official; a generalized upload center is not publicly shown [9][15] |
| Notifications | Not exposed on public SLCM login | Root URL | No public SLCM announcement feed was captured. Online Manipal's notices are separate |
| Staff/faculty workflows | Not publicly documented | Root and alternate hosts | Office 365 SOP includes employees, but visible SLCM staff functions, attendance entry, and mark entry were not verified [16] |

The independent attendance guide at `https://slcm.vercel.app/guides/check-attendance-muj` claims course-level totals, attendance percentage, warning thresholds, grades, internal marks, CGPA, and timetable functions [33]. It is useful as a lead, not authoritative confirmation. Similarly, `https://mujstella.in/` explicitly calls itself an independent student platform not affiliated with MUJ [30].

**Decision-ready insight:** The public record strongly verifies authentication, profile registration, attendance-route naming, academic-fee entry, and parent access. It is weak for timetable, marks, course/exam registration, transport, notifications, and staff screens because those functions are either authentication-gated or documented only by independent student sites.

## Fees, Examinations, and Payment Integrations

### Payment routing table

| Scope | Official route | Named platform or processor | Publicly documented methods | Important boundary |
|---|---|---|---|---|
| Existing-student annual academic fee | `https://mujslcm.jaipur.manipal.edu/` from `https://jaipur.manipal.edu/pay-fee-online.php` | Processor not disclosed | SLCM online mode; alternative Canara Bank transfer | Do not attribute Razorpay or NTT DATA to this checkout without transaction-stage evidence [10] |
| Hostel and mess | SpaceBasic app | SpaceBasic | App payment | Current public MUJ page explicitly separates this from SLCM [10] |
| Mess fee for new/existing students | `https://muj-payservices.nttdatapay.com/DirectPay/MUMessFee` | NTT DATA Payment Services domain | Public form requests registration number and total fee | Page existence is verified, but its relationship to the current SpaceBasic instruction is not dated [27] |
| Certificates and examination documents | `https://rzp.io/l/lCB8nGo7Wj` | Razorpay short-link/domain | MUJ names UPI/Paytm | This is certificate/document payment, not proof of the annual tuition processor [14] |
| Electronic transfer | Canara Bank account using `MUVAN` plus registration/application number | Canara Bank | Bank transfer; NRI wire transfer also listed | Students must email transaction details to Student Finance [10] |

SpaceBasic's official App Store listing names SBasic Private Limited as developer and describes the product as campus and hostel management software for iPhone and iPad [23]. Exact store URLs are `https://apps.apple.com/us/app/spacebasic/id1217386342` and `https://play.google.com/store/apps/details?id=com.app.spacebasic`.

MUJ's annual-fee page also links current annual-fee notices and tells students to email UTR, account-holder, transaction date, and amount to `student.finance@jaipur.manipal.edu`. Student Finance extensions are 236, 252, and 741; Accounts extensions are 294, 439, and 782 [10].

### Examination resources and registration boundary

The official examination hub is `https://jaipur.manipal.edu/examination.php`. It links a Student Examinations Handbook, Examination Manual, appendices, application formats, examination schedules, and time-table PDFs [14]. The Student Examinations Handbook states that its evaluation scheme is effective from academic year 2023-24 [29]. It defines a 10-point grade system, GPA, CGPA, semester grade cards, and the consequence of a DT grade for insufficient attendance [29].

For certificates, the student downloads an application, pays online, and emails the form and receipt to `exam.store@jaipur.manipal.edu` or `exam.helpdesk@jaipur.manipal.edu`. MUJ says updates are communicated within 48 working hours after receipt [14]. The page also lists a make-up application at Rs. 1,000 per course through online form submission after notification [14].

No reviewed MUJ source states that general semester exam registration happens inside SLCM. The correct report therefore distinguishes:

- official SLCM profile registration;
- official examination applications and notified forms;
- official examination schedules and handbooks; and
- an unverified claim that a general "exam form" is an SLCM dashboard feature.

**Case study - payment misrouting:** A student paying annual course fees should begin at MUJ's Pay Fee Online page and follow its SLCM link. A hostel resident should use SpaceBasic. An alumnus requesting a certificate should use the `rzp.io` certificate form. The mechanism is service-specific routing; the risk is paying through a genuine MUJ-related processor for the wrong purpose.

**Decision-ready insight:** Processor names are meaningful only with service scope. Public evidence supports SpaceBasic for hostel/mess, NTT DATA for a mess-fee form, and Razorpay for certificates, while the SLCM academic-fee processor remains undisclosed.

## Official Documentation and Support Surfaces

### Official documentation inventory

| Page or document | Exact URL | What it contributes |
|---|---|---|
| MUJ main website | `https://jaipur.manipal.edu/` | Authoritative university website and navigation base |
| Orientation Program 2026 | `https://jaipur.manipal.edu/induction-orientation-program.php` | Reporting workflow, help numbers, required documents, and links to SLCM/Office guides [9] |
| FAQs for SLCM Registration | `https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf` | Username/password pattern, AMS/DMS and IT escalation, admission-data corrections [15] |
| SLCM Profile Registration Guide | `https://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf` | Officially linked profile guide; text was not publicly extractable in this review [9] |
| Office 365 and Outlook SOP | `https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf` | Microsoft identity setup, password policy, MFA, recovery [16] |
| Pay Fee Online | `https://jaipur.manipal.edu/pay-fee-online.php` | SLCM, SpaceBasic, bank-transfer, and finance-contact routes [10] |
| Course Fee | `https://jaipur.manipal.edu/fee-structure.php` | Program fee-information landing page |
| Annual Fee Payment 2026-27 | `https://jaipur.manipal.edu/img/pdf/Annual-Fee-Payment-for-the-AY-2026-2027.pdf` | Current fee notice linked from MUJ's fee page |
| Examination hub | `https://jaipur.manipal.edu/examination.php` | Handbooks, manuals, forms, schedules, certificates, NAD/ABC links [14] |
| Student Examinations Handbook | `https://www.jaipur.manipal.edu/img/pdf/exam/Student%20Examination%20Handbook%202023-24%20(11.08.2023).pdf` | Evaluation, grades, GPA/CGPA, attendance consequences [29] |
| Examination Manual | `https://www.jaipur.manipal.edu/img/pdf/exam/3.%20Manual%20Exam%20Process.pdf` | Examination administration and grading process [31] |
| Academic Calendar | `https://jaipur.manipal.edu/academics-calender.php` | Orientation and academic-calendar document index |
| Contact Us | `https://jaipur.manipal.edu/contact-university.php` | University-wide office, extension, and email directory [11] |

A current general-purpose "student handbook" distinct from the Student Examinations Handbook was not verified. Department handbooks exist, but they should not be represented as one university-wide SLCM manual.

### Support routing matrix

| Problem | Official first contact | Details |
|---|---|---|
| SLCM/AMS login after credential recheck | DMS/AMS | `dms@jaipur.manipal.edu`, `ams@jaipur.manipal.edu`; Rahul Kumawat ext. 784, Dinesh Sain ext. 738, Rithik Chaudhary ext. 481 [15] |
| Outlook, Office 365, password, or MFA | IT Infra | `it.support@jaipur.manipal.edu`; orientation help ext. 144 and mobile `9358009341` [15][9] |
| Missing documents or incorrect admission data | Admissions | `admissions@jaipur.manipal.edu`; extensions 142, 257, 297 [15] |
| Academic/profile-registration issue | Academic/AMS | `academic@jaipur.manipal.edu`, `ams@jaipur.manipal.edu`; main number `0141-3999100`, academic ext. 263 [11] |
| Annual fee payment or transfer posting | Student Finance | `student.finance@jaipur.manipal.edu`; extensions 236, 252, 741 [10] |
| Exam certificate/application | Examination helpdesk | `exam.store@jaipur.manipal.edu`, `exam.helpdesk@jaipur.manipal.edu`; Controller of Examinations contact also appears in MUJ's directory [14][11] |
| Hostel matter | Chief Warden | `chief.warden@jaipur.manipal.edu`; `0141-3999108` in the SLCM FAQ [15] |
| Library | Library office | `library@jaipur.manipal.edu`; extension 179 [11] |

MUJ's administration page publicly names Mr. Anshuman Mohanty as Head of Digital Infrastructure and Technology Services [21]. It does not call him the SLCM nodal officer. The evidence therefore supports identifying the responsible IT leadership function, not inventing a nodal designation or personal contact.

**Decision-ready insight:** "SLCM support" is not one queue. The escalation path follows data ownership: IT for identity, AMS/DMS for SLCM operation, Admissions for source data, Student Finance for payment posting, and COE for examination documents.

## Related Portals, LMS, Apps, and Manipal Sister Systems

| System | Exact URL | Institution/audience | Publicly visible function | Relationship to MUJ SLCM |
|---|---|---|---|---|
| MUJ SLCM canonical | `https://mujslcm.jaipur.manipal.edu/` | MUJ students and parents | Login boundary [5] | Core subject of this report |
| MUJ SLCM alternate | `https://muj.slcm.jaipur.manipal.edu/` | MUJ | Alternate branded login | Related hostname, not a separate proven product |
| MUJ `/Home/Index` | `https://mujslcm.jaipur.manipal.edu/Home/Index` | MUJ | Same public login surface [3] | Route, not public dashboard |
| MUJ DigiLibrary | `https://mujlibrary.live/` | MUJ students | Book tracking, renewals, catalog, OTP email login [18] | Adjacent library portal; no stated SLCM integration |
| MUJ Alumni Network | `https://mujalumni.in/` | Alumni | MUJ-branded community, news, and events [13] | Separate post-study community |
| Online Manipal MUJ | `https://muj.onlinemanipal.com/` | Online-degree learners | Online MBA, BBA, MCA, BCA, and related programs [12] | Separate online-program ecosystem, not core-campus SLCM |
| Online Manipal student login | `https://student.onlinemanipal.com/login` | Online learners | Online student-portal login | Do not substitute for MUJ SLCM |
| Online Manipal notices | `https://muj.onlinemanipal.com/notifications` | Online learners | Separate notices page | Not evidence of public SLCM announcements |
| SpaceBasic iOS | `https://apps.apple.com/us/app/spacebasic/id1217386342` | Campus/hostel users | Campus and hostel-management app [23] | MUJ directs hostel/mess fees here |
| SpaceBasic Android | `https://play.google.com/store/apps/details?id=com.app.spacebasic` | Campus/hostel users | Android app by SBASIC Private Limited | Same adjacent hostel service |
| MAHE official Student Portal page | `https://www.manipal.edu/mu/academics/student-portal.html` | MAHE, not MUJ | Links to `https://sis.manipal.edu/index.aspx` [8] | Sister institution, not MUJ credentials by default |
| MAHE legacy/group SLcM | `https://slcm.manipal.edu/` | MAHE ecosystem | Separate SLcM host | Not the MUJ portal |
| MAHE SLcM Change Password | `https://slcm.manipal.edu/StudentChangePassword.aspx` | MAHE users | Old, new, and confirm-password fields [7] | Demonstrates a separate password surface |
| MUJ admissions | `https://admissions.jaipur.manipal.edu/` | Applicants | Application and admissions tracking | Pre-SLCM applicant journey |

### MIT Manipal and sister-system distinction

The official MAHE Student Portal page links to `https://sis.manipal.edu/index.aspx`, while the older `https://slcm.manipal.edu/` remains publicly reachable [8][2]. No separate official MIT Manipal SLCM hostname was verified. MIT students may use MAHE-level services, but that does not make `slcm.manipal.edu` an MUJ mirror.

### LMS and ERP conclusion

No extractable public content was found at the user-suggested `https://lms.jaipur.manipal.edu/`, and no official MUJ page reviewed identified a separate core-campus LMS URL. Online Manipal advertises an LMS for online degrees, but its scope is online programs, not necessarily on-campus MUJ [12]. Therefore:

- **Core-campus LMS URL:** not publicly verified.
- **Online-program LMS:** publicly represented by Online Manipal.
- **ERP:** no separately branded public MUJ ERP portal was verified. SLCM performs ERP-like student-administration functions, but no public source identifies its vendor or formally labels it "ERP."
- **Mobile SLCM app:** no official MUJ-branded SLCM mobile app was verified.
- **Official adjacent apps:** SpaceBasic for hostel/mess and Microsoft Authenticator for mandatory Office 365 MFA [10][16].

**Case study - portal-name collision:** A search for "Manipal student portal" can return MUJ SLCM, MAHE SIS, MAHE SLcM, or Online Manipal. The mechanism is group-wide brand reuse across different institutions and delivery modes. The safe selection rule is to confirm both hostname and audience before entering credentials.

**Decision-ready insight:** The Manipal ecosystem is federated organizationally, not one universal portal. MUJ, MAHE/MIT, and Online Manipal must be treated as distinct identity and service scopes.

## Synthesis: One Lifecycle, Multiple Systems

The evidence reveals a distributed service architecture rather than a monolithic student super-app.

| Dimension | MUJ SLCM | Microsoft 365 | SpaceBasic/NTT DATA | DigiLibrary | Online Manipal | MAHE SIS/SLcM |
|---|---|---|---|---|---|---|
| Primary scope | Student administration | Identity, email, Office apps, MFA | Hostel/mess and scoped payments | Library circulation/catalog | Online-degree teaching and services | MAHE student administration |
| Audience | MUJ students and parents; staff role not public | MUJ students and employees | Residents and fee payers | MUJ students | Online learners | MAHE/MIT ecosystem |
| Public entry | MUJ-branded local form | Microsoft sign-in and reset | App/store or processor form | OTP email portal | Separate branded portal | MAHE SIS or legacy SLcM |
| Strongest evidence | FAQ, orientation, fee page, attendance route | Official Office 365 SOP | MUJ fee page plus processor/app pages | Public portal text | Program landing page | Official MAHE portal link |
| Main risk | Assuming hidden features | Calling credential linkage SSO | Paying through wrong scoped service | Assuming SLCM integration | Confusing online with campus | Using sister-university credentials |
| Evidence horizon | Current login and 2026 onboarding/fee pages | SOP effective June 2025 | Current fee instruction plus undated NTT form | Current public portal | Current public program page | Current portal link plus legacy host |

Three non-obvious tensions matter.

First, the password model is integrated without publicly proven SSO. SLCM tells users to use the Outlook password, and its reset link goes to Microsoft, yet the SLCM page still presents a local username/password form [15][16]. The practical implication is that password synchronization or directory-backed authentication may exist, but users should not expect a Microsoft consent or seamless-login experience unless the live post-submit flow shows it.

Second, payment integration is deliberately fragmented by purpose. This is not necessarily poor design: different merchants may own tuition, accommodation, mess, or certificate revenue. The operational risk comes from collapsing those categories in user guidance. MUJ's own pages prevent that by sending academic fees to SLCM, hostel/mess to SpaceBasic, and certificates to the `rzp.io` payment form [10][14].

Third, feature breadth and public verifiability diverge. Independent student tools claim a rich dashboard covering attendance, grades, CGPA, internal marks, and timetable [33], while MUJ's public evidence confirms only selected routes and processes. This does not disprove the richer dashboard. It means an OSINT report must label those details secondary until MUJ publishes a manual or an authorized user supplies a lawful screenshot.

The resulting lifecycle is:

`Applicant portal -> Microsoft identity activation -> MUJ SLCM profile -> physical verification -> authenticated academic administration -> service-specific library/hostel/payment systems -> examination documents -> alumni community.`

Each transition has a different data owner and support contact. That architecture explains why a single "SLCM helpdesk" answer is inadequate.

**Decision-ready insight:** MUJ has a coherent lifecycle but not a single interface. The correct user strategy is to start from the official MUJ page for the task, preserve the exact hostname, and escalate according to the office that owns the underlying record.

## VERDICT

**What MUJ SLCM is:** An authenticated Manipal University Jaipur student lifecycle and administrative portal at `https://mujslcm.jaipur.manipal.edu/`. Public evidence verifies student/parent login, Outlook-linked credentials, first-year profile registration, an attendance route, and academic-fee entry [5][15][9][25][10].

**What it is not publicly proven to be:** A learning-management system, a universal Manipal-group portal, a publicly browsable notice board, or a confirmed SAML/OAuth/Entra SSO application. A separate core-campus LMS, SLCM transport function, public staff dashboard, general document-upload center, and SLCM exam-registration screen were not verified.

**Payment verdict:**

- Annual academic fees: enter through SLCM; processor not publicly disclosed.
- Hostel/mess: SpaceBasic according to MUJ's current public page.
- Mess-fee direct form: NTT DATA Payment Services surface exists.
- Certificates/documents: Razorpay `rzp.io` form, with UPI/Paytm named by MUJ.
- Bank alternative: Canara Bank transfer with Student Finance notification.

**Confidence:**

- **High, 0.93**, for public login controls, official onboarding documents, Microsoft 365/MFA instructions, helpdesk contacts, payment routing, and examination-document procedures.
- **Medium-high, 0.82**, for attendance-route existence and the relationship among adjacent portals.
- **Medium-low, 0.45**, for the full authenticated feature inventory because the dashboard is credential-protected and several requested capabilities appear only in secondary student guides.
- **Overall confidence: 0.86.**

The central OSINT conclusion is conservative but strong: MUJ SLCM is the university's protected administrative system of record, surrounded by purpose-specific Microsoft, finance, hostel, library, online-learning, examination, and alumni services. Any richer claim about post-login modules should be labeled authentication-gated until MUJ publishes a current user manual or authorized access confirms it.

## References

1. *Academic Calendar - Manipal University Jaipur*. https://jaipur.manipal.edu/academics-calender.php
2. [
	MU SLcM
](https://slcm.manipal.edu/)
3. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
4. *Manipal University*. https://muj.slcm.jaipur.manipal.edu/
5. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
6. *Notices - MUJ*. https://muj.onlinemanipal.com/notifications
7. [
	MU SLcM
](https://slcm.manipal.edu/StudentChangePassword.aspx)
8. *Student Portal Login- MAHE (Manipal Academy Of Higher Education)*. https://www.manipal.edu/mu/academics/student-portal.html
9. *Orientation Program 2026 - Manipal University Jaipur - Manipal University Jaipur*. https://jaipur.manipal.edu/induction-orientation-program.php
10. *Pay Fee Online - Manipal University Jaipur *. https://jaipur.manipal.edu/pay-fee-online.php
11. *Contact Us - Manipal University Jaipur *. https://www.jaipur.manipal.edu/contact-university.php
12. *Online Bachelor and Master Programmes | Online Degree Programs in India | Online Manipal*. https://muj.onlinemanipal.com/
13. *Official Community of Manipal University Jaipur*. https://mujalumni.in/
14. *Examination - Manipal University Jaipur *. https://www.jaipur.manipal.edu/examination.php
15. *Faqs Slcm*. https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf
16. *Help Document Sop Office 365 And Outlook Email Id*. https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf
17. *Course Fee - Manipal University Jaipur*. https://jaipur.manipal.edu/fee-structure.php
18. *Library Portal | Student Portal*. https://mujlibrary.live/
19. *CERTIFICATE FEES*. https://rzp.io/l/lCB8nGo7Wj
20. *• �r� JIV/1;�·. ·\*. https://jaipur.manipal.edu/img/pdf/Annual-Fee-Payment-AY-2026-2027-NRI.pdf
21. *Head- Digital Infrastructure & Technology Services - Manipal University Jaipur*. https://www.jaipur.manipal.edu/administration-it.php
22. *SpaceBasic - Apps on Google Play*. http://play.google.com/store/apps/details?hl=en_US&id=com.app.spacebasic
23. *‎SpaceBasic App - App Store*. http://apps.apple.com/us/app/spacebasic/id1217386342
24. *• �r� JIV/1;�·. ·\*. https://jaipur.manipal.edu/img/pdf/Annual-Fee-Payment-for-the-AY-2026-2027.pdf
25. *Manipal University - mujslcm.jaipur.manipal.edu*. https://mujslcm.jaipur.manipal.edu/Student/Academic/AttendanceSummaryForStudent
26. *2025 Grade Sheet for Courses | PDF - Scribd*. https://www.scribd.com/document/983177245/Https-Mujslcm-jaipur-manipal-edustudentAcademicGradesForStudent
27. *Manipal University Jaipur | MUJ*. https://muj-payservices.nttdatapay.com/DirectPay/MUMessFee
28. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Student/Academic/TimeTableForStudent
29. *Student Examinations Handbook*. https://www.jaipur.manipal.edu/img/pdf/exam/Student%20Examination%20Handbook%202023-24%20(11.08.2023).pdf
30. *MUJStella - Student Platform for Manipal University Jaipur*. https://mujstella.in/
31. *EXAMINATION MANUAL*. https://www.jaipur.manipal.edu/img/pdf/exam/3.%20Manual%20Exam%20Process.pdf
32. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Student/Academic/GradesForStudent
33. *How to Check Your Attendance at MUJ | mujslcm Guide | betterSLCM*. https://slcm.vercel.app/guides/check-attendance-muj
34. *APPENDIX - I*. https://www.jaipur.manipal.edu/img/pdf/exam/4.%20Appendix%20I%20Examination%20manual%20MUJ%2003%20Apr%2019.pdf
35. *MUJStella - Student Platform for Manipal University Jaipur*. https://mujstella.in/mujslcm
