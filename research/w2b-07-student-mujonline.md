# MUJ Online Student Portal and SLCM: Public OSINT and Security Research Report

## Executive Summary

This report compares the public-facing MUJ Online distance-education portal at `https://student.mujonline.com/` with the MUJ campus Student Life Cycle Management portal at `https://mujslcm.jaipur.manipal.edu/`. It uses only publicly accessible pages, official MUJ/Manipal material, a public D2L customer case study, and one public student discussion. It does not attempt authentication, endpoint discovery, credential testing, crawling of private areas, or any other unauthorized activity.

- **Public Portal Identity**: `student.mujonline.com` exposes a minimal page titled "Student Portal" with "Welcome!", "To student portal", an "Email" field label, and a help-desk message; the public view does not name a password, OTP, Microsoft identity provider, or federated sign-in mechanism [5]. The immediate conclusion is that the domain is an authenticated student-facing entry point, but its exact authentication protocol is not publicly established.
- **Online Learning Function**: MUJ's official Online Manipal material describes an online learning portal/LMS supporting video tutorials, live interactive classes, recordings, discussion forums, quizzes, and exams, with remote examinations [7]. The public D2L page identifies the LMS login as "Powered by D2L Brightspace" [9]. Students should therefore treat the portal and Brightspace as related parts of a learning ecosystem, not assume they are the same application.
- **Learning Workflow**: The official MUJ student-experience page describes UNext Labs as a virtual cloud programming environment integrated with Python, R, MySQL, Java, and PHP [2]. It also describes mock exams, exam-slot booking, practical examinations through virtual programming environments, and evaluation [2].
- **SLCM Function**: The official SLCM registration FAQ gives the SLCM registration URL, a username format based on a name and registration number, a password tied to the official Outlook ID, and separate support contacts for AMS/SLCM and Outlook problems [10]. The public SLCM shell exposes student and parent sign-in choices, while the Online portal exposes only a student-oriented email entry label [6][5].
- **Identity Boundary**: MUJ's official 2025 Office 365 SOP applies to students and employees and requires university mail credentials plus mandatory MFA, including Microsoft Authenticator and alternative phone/email methods [11]. This confirms a Microsoft 365 identity service in the MUJ environment, but it does not prove that `student.mujonline.com` directly delegates to Microsoft 365.
- **Technology Boundary**: Passive public markup is consistent with a modern JavaScript single-page application on `student.mujonline.com` and a legacy-style server-rendered SLCM application using jQuery assets on the SLCM page. These are observations, not proof of framework versions, backend runtime, deployment topology, or security posture. The supplied description of SLCM as ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10 behind Akamai, and Microsoft 365 identity was not independently confirmed by the public search results in this research run and is treated as an input hypothesis, not as a verified finding.
- **Complaints and Stability**: The strongest portal-specific public complaint found concerns SLCM, not MUJ Online: a public Reddit post says that the user's password showed an error even though the user believed it was correct, and asks whether others had the same issue [13]. Searches did not identify a credible, portal-specific public breach report for `student.mujonline.com`. A generic D2L login page contains a vendor warning that a user "may not be getting an optimal system experience," but the page itself does not establish an outage [4].
- **Security Interpretation**: A small public surface is not evidence of a secure application. Conversely, the absence of a public breach report is not evidence that no incident has occurred. The defensible conclusion is that public evidence supports an authentication boundary and a multi-application learning architecture, while it does not support vulnerability claims.

## Scope, Method, and Evidence Rules

The research question contains several distinct objects that must not be conflated: the campus SLCM portal, the Online Manipal student portal, the Brightspace LMS, Microsoft 365/Outlook identity, and unrelated Manipal portals. The comparison below treats a source as authoritative only for the system it actually describes. For example, the MAHE student-portal page links to `sis.manipal.edu`, but that is an MAHE destination and should not be presented as proof about MUJ Online or MUJ SLCM [14].

The analysis is based on public page text, official PDFs, passive page markup retrieved from public URLs, public search indexes, and a public Reddit page. It does not rely on authenticated access. It also does not infer an API, database, session design, authorization model, password policy, or vulnerability from a URL, a framework-looking asset name, or a browser-rendered page alone.

### Evidence confidence scale

| Confidence | Meaning in this report | Examples |
|---|---|---|
| High | Directly stated by an official page or document, or visibly present on the public page | Brightspace branding; SLCM registration URL; MUJ Online helpdesk address |
| Medium | Supported by an official vendor or institutional description, but not a complete technical specification | Brightspace as MUJ's LMS; described online-learning features |
| Low | A public user report, search-index observation, or passive technical clue that requires caution | One Reddit SLCM password complaint; JavaScript asset observations |
| Unknown | Not established by the public material reviewed | Exact `student.mujonline.com` authentication protocol; breach status; backend framework version |

**Decision insight:** The useful security-club deliverable is an evidence map with confidence labels, not a speculative vulnerability list.

## 1. MUJ SLCM: Public Purpose, Login Surface, and Account Dependencies

The official MUJ SLCM FAQ identifies `https://mujslcm.jaipur.manipal.edu/` as the registration link [10]. It provides a username pattern described as a name plus registration number, gives an example, and says the password is according to the official Outlook ID [10]. This is materially different from the public MUJ Online shell, which only exposes an "Email" label and does not publicly show a password or OTP label [5].

The SLCM home page visibly presents "WELCOME TO MUJ PORTAL," a general sign-in option, and a parent-login option [6]. Search-indexed text for the same public domain additionally exposes student-login and forgot-password labels. The exact interaction after selecting these choices is not established without logging in, and this report does not attempt that. The official FAQ does, however, document operational support for login failure: users are told to re-verify credentials and then contact DMS or AMS support if the problem persists [10].

The FAQ also separates SLCM/AMS problems from Outlook problems. For an Outlook account that is not working, it tells the user to reset the password and contact Team IT Infra if unresolved, listing `it.support@jaipur.manipal.edu` and extension 144 [10]. The same document says that incorrect personal details in the SLCM portal can only be changed by the admissions function after verification [10]. This suggests that SLCM is not merely a course-content viewer: it is connected to institutional records and administrative ownership. That is an inference from the documented account and records support process, not a claim that every administrative feature is visible to unauthenticated visitors.

| SLCM public evidence | What it establishes | What it does not establish |
|---|---|---|
| Official registration URL | MUJ identifies the SLCM domain for registration [10] | It does not reveal private pages or APIs |
| Username format and Outlook-linked password | A documented account convention and dependency on official Outlook identity [10] | It does not prove Microsoft Entra ID, SAML, OAuth, or direct password reuse |
| Student and parent login choices | More than one user role is exposed on the public shell [6] | It does not prove the authorization rules for either role |
| DMS/AMS support contacts | Institutional support ownership for login problems [10] | It does not measure availability or response time |
| Admission-controlled personal details | Administrative correction workflow is documented [10] | It does not enumerate all SLCM modules |

**Case study - SLCM password failure:** The public Reddit report is a small but relevant operational signal. The author says the password is showing an error despite believing it is correct and asks whether others face the same issue [13]. The report does not identify root cause, duration, account lockout behavior, or institutional confirmation. Its value is therefore diagnostic rather than statistical: it shows that credential acceptance has been a user-visible pain point, while providing no basis to call the system insecure.

**Decision insight:** For a security club, SLCM should be modeled as an institutional-record and identity-dependent service with a documented Outlook relationship and a parent/student role split. The appropriate research question is account lifecycle and recovery assurance, not whether a visible login page looks modern.

## 2. MUJ Online Student Portal: What Is Publicly Visible

The public pages at `https://student.mujonline.com/` and `https://student.mujonline.com/login` are extremely sparse. The extracted public content consists of the title "Student Portal," "Welcome!", "To student portal," the label "Email," and the instruction "If you face any issues, reach out to your help desk" [5]. No public navigation menu, course list, dashboard, password-reset control, OTP prompt, Microsoft sign-in button, parent option, or LMS link is visible in the extracted unauthenticated view.

This is an important negative finding. It does not mean that those capabilities do not exist after authentication. It means only that the public shell does not disclose them to an unauthenticated observer. The distinction matters because portal screenshots, search snippets, and user descriptions can refer to authenticated routes that are not present on the landing page.

The passive HTML is consistent with an Angular-style component application: it contains Angular-looking component attributes, a router outlet, an application login layout, and a MUJ Online login-screen asset. It also references common client-side assets, including jQuery and Video.js. These are passive observations from public markup, not a complete stack identification. The public markup does not establish Angular version, API framework, database, cloud provider, authentication provider, WAF, CDN, or server-side language.

| Publicly observable student-portal item | Evidence status | Security interpretation |
|---|---|---|
| Page title | Directly visible as "Student Portal" [5] | Confirms product labeling only |
| Welcome message | Directly visible [5] | Cosmetic/user-experience evidence |
| Email label | Directly visible [5] | Indicates an email-oriented login input, not the complete auth protocol |
| Password field | Not visible in extracted public text | Do not infer absence after client-side rendering or after a prior step |
| OTP or MFA | Not named in public shell | Do not claim passwordless, OTP, or MFA behavior |
| Microsoft 365 button | Not named in public shell | Do not equate MUJ Microsoft 365 with portal SSO |
| Help path | Generic help-desk message [5] | Support exists as a stated fallback, but no SLA is stated |
| Authenticated features | Not public | Must be documented by official user guides or authorized users |

The official Online Manipal help center supplies a more concrete support boundary for enrolled students: `helpdesk@mujonline.edu.in` and telephone `+91 7996 600 444` [1]. It separately lists admissions contact information, showing that prospective-student and enrolled-student support are treated as different channels [1].

**Case study - minimal public shell:** A minimal login shell reduces accidental disclosure of internal navigation and may reduce passive information leakage, but it also makes independent verification difficult. An analyst can confirm the product name and email-oriented entry point, yet cannot confirm the post-login dashboard, account recovery, or authorization model. The correct output is therefore an evidence boundary: public shell confirmed; authenticated behavior unknown.

**Decision insight:** The club should not publish a feature inventory for `student.mujonline.com` as if it were directly observed. It should publish a two-layer inventory: public-shell facts, and official Online Manipal learning capabilities that are likely to be delivered through the broader LMS ecosystem but are not proven to be implemented inside this particular domain.

## 3. MUJ Online Learning Architecture and LMS Links

Online Manipal's official MUJ material describes online degree and certification delivery through a learning portal, explicitly calling it an LMS [7]. The page says that learners can use laptops, smartphones, or tablets and access video tutorials, live interactive classes, recorded sessions, discussion forums, quizzes, and exams through the LMS [7]. It also says examinations are conducted remotely [7].

The official D2L customer page names the product as D2L Brightspace. It describes MUJ's challenge as implementing a robust LMS and identifies Brightspace as the selected solution [8]. The public login route at `https://learning.onlinemanipal.com/d2l/home/14042` displays "Username," "Forgot your password?", and "Powered by D2L Brightspace" [9]. This is stronger evidence than a generic search result: it directly ties the MUJ learning route to Brightspace branding.

D2L's case study describes real-time progress tracking, assignment submissions, multimedia content, discussion forums, notifications, quizzes, tests, peer evaluations, assignments, and feedback [8]. It also says that students needed reliable access from urban and rural locations and that the platform was selected to support scale and regulatory requirements [8]. These are statements from D2L's customer story and should be treated as vendor-published case-study claims, not as an independent availability audit.

The D2L login page contains generic system-experience language stating that a user may not be getting an optimal system experience and offering a learn-more option [4]. That wording should not be reported as proof of a MUJ outage. It may be a standard vendor/browser compatibility message. The page itself does not identify a service incident, affected users, start time, or end time.

| Learning-system route | Public URL | Publicly supported role |
|---|---|---|
| MUJ Online student portal | `https://student.mujonline.com/` | Student-facing entry shell; email label and help message visible [5] |
| MUJ Online student portal login | `https://student.mujonline.com/login` | Login route; same sparse public shell in extracted view [15] |
| MUJ Brightspace login | `https://learning.onlinemanipal.com/d2l/home/14042` | Course/e-learning login; Brightspace branding visible [9] |
| MUJ Online programme site | `https://muj.onlinemanipal.com/` | Public programme, delivery, and service information [7] |
| MUJ Online student experience | `https://muj.onlinemanipal.com/student-experience` | Learning, lab, examination, and evaluation descriptions [2] |
| Enrolled-student help | `https://muj.onlinemanipal.com/help-center` | Helpdesk email and phone contact [1] |
| MUJ SLCM | `https://mujslcm.jaipur.manipal.edu/` | Institutional SLCM registration and sign-in route [10] |

The official student-experience page adds a practical layer. It describes UNext Labs as a virtual cloud environment for programming skills and lists Python, R, MySQL, Java, and PHP integration [2]. It also describes mock exams, slot booking, virtual programming environments for practical exams, and evaluation [2]. These capabilities demonstrate that the online ecosystem is broader than a basic content portal, but they do not prove that every function is hosted under `student.mujonline.com` rather than Brightspace or another linked service.

**Decision insight:** The safest architecture diagram has separate nodes for the student portal, Brightspace LMS, virtual lab/examination tooling, support, and SLCM. Draw relationships as "publicly associated" unless an official link or authenticated user documentation proves a direct integration.

## 4. Identity, Microsoft 365, and Login Behavior

The official MUJ Office 365 SOP is a strong source for the university identity environment. It is titled "How To Setup Your Office 365 Mail ID," describes first-time account setup and MFA, and states that its audience is students and employees [11]. It instructs users to open Microsoft's Office portal, enter a university mail ID, sign in with a current or temporary password, and set a new password [11].

The same document states that MFA is mandatory for the university account and requires completion before Office 365 can be used [11]. It describes Microsoft Authenticator, QR-code enrollment, phone verification by SMS OTP, and personal-email verification as available methods [11]. These facts establish a Microsoft-managed account and MFA process for MUJ's Office 365 environment.

The SLCM FAQ links the SLCM password to the official Outlook ID [10]. Taken together, the two official documents support this limited statement: MUJ SLCM account operations are documented in relation to official Outlook identity, and MUJ maintains a Microsoft 365/MFA process for students and employees. They do not support the stronger statement that `student.mujonline.com` uses Microsoft 365 SSO. The student portal's public shell names only "Email" and does not name Microsoft, Outlook, Azure, Authenticator, SAML, or OAuth [5].

The public iLearn page must also be kept separate. It is titled "iLearn Login," but the extracted content presents an "Enroll Now" flow, contact details, programme selection, consent to contact by email/SMS/WhatsApp/voice, and four-digit OTP verification [3]. It therefore appears, based on explicit public content, to be an enquiry or enrolment flow rather than a clearly established enrolled-student authentication page. That is a classification based on the page's visible controls, not a claim about hidden routes.

| Identity or login claim | Status | Basis |
|---|---|---|
| SLCM uses an official Outlook-linked password convention | Verified as documented | MUJ SLCM FAQ [10] |
| MUJ Office 365 accounts use university mail IDs | Verified as documented | MUJ IT SOP [11] |
| MFA is mandatory for the university Office 365 account | Verified as documented | MUJ IT SOP [11] |
| Microsoft Authenticator, phone, and email methods are described | Verified as documented | MUJ IT SOP [11] |
| `student.mujonline.com` directly uses Microsoft 365 SSO | Unknown | The public shell does not name a provider [5] |
| `student.mujonline.com` uses OTP | Unknown | No OTP is named in the public shell [5] |
| iLearn page is the enrolled-student login | Not established | Visible content emphasizes enrolment and OTP verification [3] |

**Security implication:** Identity correlation is the highest-risk area for overclaiming. A shared email vocabulary does not prove shared authentication, and a university-wide MFA policy does not prove that every application enforces MFA. The security club should describe these as separate trust-boundary questions.

## 5. Technology Stack: Verified Signals Versus Supplied Hypotheses

The original brief supplies a technical characterization of the SLCM environment: ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 identity. The public evidence gathered here confirms only parts of the surrounding picture. The SLCM page's passive markup references jQuery 1.10.2, jQuery validation assets, and a `/keen/` theme path. That is consistent with a server-rendered application using older client-side dependencies, but it does not prove ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, or Akamai. The visible SLCM page itself only states the portal branding and sign-in choices [6].

The Online portal's passive markup contains Angular-style component attributes, a router outlet, a login-layout component, and an asset named for a MUJ Online login screen. This supports a cautious description of a client-rendered JavaScript application. It does not establish the Angular version, backend technology, hosting platform, CDN, WAF, authentication provider, or API design. The extracted visible page still contains only the sparse shell [5].

Brightspace is the one technology product directly identified by an official public login page: the page says "Powered by D2L Brightspace" [9]. The D2L customer story further identifies Brightspace Core as the platform used in the case study [8]. This is sufficient to name Brightspace as the LMS product associated with MUJ Online, but not to say that the student portal itself is built on Brightspace.

| System | Public technology evidence | Safe wording | Unsafe wording |
|---|---|---|---|
| SLCM | Legacy-looking jQuery validation and theme assets in passive markup; public sign-in shell [6] | "Public markup is consistent with a server-rendered legacy-style application" | "Confirmed ASP.NET MVC 5.3 on IIS 10" without a source |
| Student portal | Angular-looking components/router and MUJ login assets in passive markup; sparse visible shell [5] | "Public markup is consistent with a JavaScript component application" | "Confirmed Angular version and API stack" |
| Brightspace LMS | Explicit product branding on public login [9] and D2L case study [8] | "MUJ's public LMS route is powered by D2L Brightspace" | "The student portal is Brightspace" |
| Microsoft identity | Official Office 365 setup and MFA SOP [11] | "MUJ documents Microsoft 365 identity and MFA for students and employees" | "The Online portal delegates directly to Microsoft 365" |
| Akamai | Not independently confirmed in the retrieved public sources | "Akamai status not established in this pass" | "Behind Akamai" as a verified fact |

**Decision insight:** Technology fingerprinting should be treated as asset inventory, not vulnerability proof. A future authorized assessment could validate headers, certificates, and deployment relationships under written permission, but public OSINT alone cannot safely turn those clues into version or exposure claims.

## 6. Public Complaints, Security Reports, and Stability Signals

The public evidence is asymmetric. For SLCM, the Reddit report specifically describes a password error despite the user's belief that the password was correct [13]. The official FAQ independently anticipates SLCM/AMS login problems and instructs users to re-verify credentials before contacting DMS or AMS [10]. These two sources align on the existence of a login-support scenario, but they do not prove a systemic outage, broken password validation, or security defect.

For MUJ Online, searches returned the portal itself, official programme material, the Brightspace login, and general reviews, but no credible portal-specific breach advisory or reproducible public incident report. The portal itself says users should contact their help desk if they face issues [5]. The official help center lists the enrolled-student email and telephone channel [1]. These are support signals, not complaints and not service-level measurements.

The D2L page's generic "may not be getting an optimal system experience" message is another weak stability signal [4]. It lacks the details needed to attribute an incident to MUJ, so it should not be counted as an outage. Similarly, positive marketing statements about a user-friendly portal or insightful live classes are testimonials or promotional content, not independent reliability evidence.

| Signal | System | Strength | What can be concluded |
|---|---|---|---|
| Password rejected despite user believing it correct | SLCM | Low, user-generated | At least one public user reported a credential-acceptance problem [13] |
| Official login troubleshooting instructions | SLCM/AMS | High, official | MUJ documents credential re-check and DMS/AMS escalation [10] |
| Generic help-desk instruction | MUJ Online portal | High for page content | The page directs users to helpdesk support [5] |
| Enrolled-student contact channel | MUJ Online | High, official | Helpdesk email and phone are publicly listed [1] |
| Generic optimal-experience warning | Brightspace route | Low/ambiguous | It does not establish a MUJ outage [4] |
| Portal-specific breach disclosure | MUJ Online | Not found in reviewed public sources | No positive breach claim should be made |
| Vulnerability disclosure programme | MUJ Online/SLCM | Not established | Do not invent a reporting channel |

A security-club report should also distinguish complaints about admission, counselling, or service quality from application-security incidents. A complaint about a promised discount, delayed support, or an exam experience may be relevant to operational resilience, but it is not automatically evidence of unauthorized access, data exposure, injection, or account takeover.

**Decision insight:** The evidence supports a cautious operational-risk statement: SLCM has a public credential complaint and an official login-support workflow; MUJ Online has a visible help path but no verified public incident record in the reviewed corpus. Neither system should be labeled vulnerable on this basis.

## 7. SLCM Versus MUJ Online: Functional and Security Comparison

SLCM and MUJ Online appear to serve different stages and modes of the student relationship. SLCM is linked by official MUJ documentation to registration, Outlook-based credentials, AMS/DMS support, admissions-controlled personal details, and student/parent sign-in choices [10][6]. MUJ Online is presented as an online degree delivery environment whose public materials emphasize LMS content, live and recorded classes, discussions, quizzes, remote exams, virtual programming labs, and learner support [7][2].

The distinction is not simply "old portal versus new portal." The systems have different information roles. SLCM is an institutional lifecycle and administrative access point. MUJ Online is a distance-education experience with a separate Brightspace LMS and associated examination/lab workflows. The public evidence does not prove that they share a database or identity provider, so a diagram should show possible integration as an unverified relationship.

| Dimension | MUJ SLCM | MUJ Online student portal and LMS ecosystem |
|---|---|---|
| Primary audience | Students and parents are visible as role choices [6] | Online students; public portal is student-labelled [5] |
| Public entry | `https://mujslcm.jaipur.manipal.edu/` [10] | `https://student.mujonline.com/` and `/login` [5] |
| Identity evidence | Username format and Outlook-linked password documented [10] | Email label visible; provider and password behavior unknown [5] |
| Administrative role | Registration, personal-detail correction, AMS/DMS support documented [10] | Public material emphasizes delivery, learning, assessment, and support [7] |
| Learning role | No course-content features visible publicly | Brightspace login and LMS capabilities publicly documented [9][8] |
| Assessments | Not established from public SLCM shell | Quizzes, exams, assignments, mock exams, practical exams, and evaluation described [7][2] |
| Parent access | Explicitly visible [6] | No parent option visible in public shell [5] |
| Recovery/support | DMS/AMS and IT Infra contacts documented [10] | Helpdesk email and telephone documented [1] |
| Public technical signal | jQuery/theme assets and legacy-style shell, cautiously interpreted | JavaScript component shell; Brightspace is separately identified [9] |
| Public incident signal | One password-error report [13] | No verified portal-specific breach or outage found in reviewed sources |

The case-study contrast is useful. A student who cannot log into SLCM may need DMS, AMS, or IT Infra because the problem may involve institutional records or Outlook credentials [10]. A student who cannot access coursework may be dealing with the student portal, Brightspace, a virtual lab, or examination tooling, each with a different support boundary [7][2]. Treating all failures as one "MUJ login problem" would obscure the actual trust boundary and delay appropriate escalation.

**Decision insight:** The club should maintain separate incident categories for SLCM identity/records, Online portal access, Brightspace course access, virtual labs, and remote examinations. This is more actionable than a single MUJ portal severity label.

## 8. Recommended Public-Information Research Backlog

The following backlog stays within safe public-information practice. It does not instruct researchers to bypass controls, submit test credentials, enumerate hidden routes, or probe production systems.

| Priority | Safe research question | Desired public evidence | Current status |
|---|---|---|---|
| 1 | Is there an official user guide for `student.mujonline.com`? | Official PDF, help article, or student handbook | Unanswered |
| 2 | Does MUJ explicitly document SSO between the student portal and Microsoft 365? | Official identity or onboarding documentation | Unanswered; Office 365 SOP covers Microsoft account MFA but not this portal [11] |
| 3 | Is the student portal a front door to Brightspace or a separate service hub? | Official link map or authenticated-user documentation published by MUJ | Partially answered; both are publicly associated with Online Manipal, but direct integration is not proven [9][7] |
| 4 | What are the official recovery and lockout procedures? | Help-center article or student handbook | SLCM partially documented; Online portal not detailed [10][5] |
| 5 | Are there official security advisories or responsible-disclosure instructions? | MUJ security page, policy, or advisory archive | Not found in reviewed sources |
| 6 | Are there independent stability reports for MUJ Online? | Dated, attributable student reports with symptoms and duration | Not established; avoid counting generic vendor warnings [4] |
| 7 | Can the supplied SLCM stack be corroborated passively? | Public vendor documentation, archived official materials, or non-invasive technology record | Not independently confirmed in this pass |
| 8 | Which support channel owns each failure type? | Official escalation matrix | Partially documented for SLCM and enrolled students [10][1] |

A university security club can add value by publishing a responsible-disclosure template, a portal ownership matrix, and a user education page explaining how to recognize the official domains. It should not publish credentials, session tokens, private screenshots, student records, or exploit demonstrations. Public research should also record collection dates because portals, vendor platforms, and support addresses change.

**Decision insight:** The next high-value artefact is not a scanner output. It is an official-source relationship map showing which domain owns identity, course content, records, support, labs, and examinations.

## Synthesis

The main divergence is architectural. SLCM exposes a role-oriented institutional portal with student and parent login choices, a documented Outlook-linked password convention, and administrative support ownership [6][10]. MUJ Online exposes a student-labelled email entry shell with little public detail [5], while its broader public programme material describes a rich distance-learning experience delivered through an LMS [7]. Brightspace is explicitly identified as the LMS product [9].

The second divergence is evidence quality. SLCM has stronger public documentation for account setup and troubleshooting: the official FAQ supplies a registration URL, username convention, support contacts, Outlook escalation, and admissions workflow [10]. MUJ Online has stronger public documentation for learning capabilities: Brightspace, discussions, assignments, assessments, remote exams, virtual labs, and evaluation are described across official and vendor pages [8][2]. Neither source set fully documents the student's authenticated journey through `student.mujonline.com`.

The third divergence is operational risk. The one concrete public complaint concerns SLCM password rejection [13], and the official FAQ anticipates login failures [10]. MUJ Online's public evidence is mostly positive or descriptive, plus a generic Brightspace system-experience message that does not prove an outage [4]. This difference may reflect actual service experience, differences in public discussion, search visibility, or the fact that the Online portal reveals less unauthenticated functionality. It should not be interpreted as a reliability ranking.

The fourth divergence is identity confidence. MUJ's Office 365 SOP establishes university mail IDs and mandatory MFA for students and employees [11]. The SLCM FAQ connects SLCM passwords to the official Outlook ID [10]. But the public MUJ Online shell does not name Microsoft 365, Outlook, Authenticator, SAML, OAuth, or OTP [5]. The correct security posture is therefore "identity relationship partially documented, portal federation unknown."

Finally, the supplied SLCM technology description should remain a hypothesis unless supported by a public, attributable source. Passive markup can suggest application age or client-side architecture, but it cannot safely prove precise framework versions, patch levels, IIS configuration, Akamai origin relationships, or authorization quality. The report's strongest defensible conclusion is that MUJ operates a multi-application student ecosystem with distinct administrative, identity, learning, lab, examination, and support surfaces.

## VERDICT

**Verdict: MUJ Online is publicly identifiable as a student-facing entry point within a broader Online Manipal distance-learning ecosystem, with D2L Brightspace publicly identified as the LMS. It is not publicly possible from the reviewed unauthenticated material to enumerate the portal's authenticated features or prove its login protocol. SLCM is better documented publicly as an institutional, Outlook-linked student/parent portal with official login-support workflows.**

**Confidence: Medium-high for the system distinction and Brightspace association; high for the cited public shell text, official contacts, SLCM FAQ, and Office 365 SOP; low for exact student-portal authentication behavior, direct SSO relationships, deployment topology, and vulnerability status.**

**Security conclusion:** No verified public evidence reviewed here establishes that `student.mujonline.com` or MUJ SLCM is breached or vulnerable. The absence of such evidence is not a security assurance. The responsible next step is authorized documentation review and coordinated disclosure through official channels, not intrusive testing.

## References

1. *Help Center - MUJ*. https://muj.onlinemanipal.com/help-center
2. *Student Experience - MUJ - Online Manipal*. https://muj.onlinemanipal.com/student-experience
3. *iLearn Login - MUJ*. https://muj.onlinemanipal.com/ilearn-login
4. *Login - Manipal University Jaipur*. https://learning.onlinemanipal.com/d2l/home/14201
5. *Student Portal*. https://student.mujonline.com/
6. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
7. *Online Manipal | UGC Entitled Online UG & PG Degree Courses*. http://muj.onlinemanipal.com/notifications
8. *Manipal University Jaipur (Online) | D2L*. https://www.d2l.com/en-in/why-d2l/customers/manipal-university-jaipur-online
9. *Login - Manipal University Jaipur*. https://learning.onlinemanipal.com/d2l/home/14042
10. *Frequently Asked Questions and Contacts for SLCM Registration*. https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf
11. *Standard Operating Procedure*. https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf
12. *Privacy & Cookie Policy | MAHE*. https://www.manipal.edu/mu/important-links/privacy-and-cookie-policy.html
13. *Reddit - The heart of the internet*. https://www.reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue
14. *Student Portal Login- MAHE (Manipal Academy Of Higher Education)*. https://www.manipal.edu/mu/academics/student-portal.html
15. *Student Portal*. https://student.mujonline.com/login
