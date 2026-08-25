# MUJ One and SLCM: Public-Facing Ecosystem Assessment

**Assessment date:** 2026-08-25

## Executive Summary

- **Portal Identity**: The public MUJ One root page identifies itself as "MUJ HR SYSTEM," and its HR page credits "ISD/CSD, MAHE"; the visible surface is therefore best classified as an employee-facing HR system, not as a confirmed student super-app [8] [5] -> treat MUJ One and the student SLCM portal as separate systems unless an official source establishes otherwise.

- **Visible Feature Set**: MUJ One publicly exposes an Email entry point, password-reset controls, employee-code and date-of-birth fields, captcha, policy acknowledgements, and a PAS Portal link [5] -> document these as observed features, but do not advertise attendance, grades, fees, timetable, or other student functions as MUJ One capabilities without further official evidence.

- **SLCM Boundary**: The official SLCM surface calls itself "WELCOME TO MUJ PORTAL" and exposes student and parent sign-in labels [3]. An official SLCM FAQ separately identifies the registration URL and gives an institutional Outlook-ID password instruction [21] -> model SLCM as a distinct academic portal with a related institutional identity context, not as a proven MUJ One module.

- **Microsoft Identity Context**: MUJ's June 2025 Office 365 SOP directs students and employees to Microsoft sign-in, university mail ID, password setup, and mandatory MFA [22] [22] [22] -> Microsoft 365 is a confirmed institutional identity and mail context, but the public evidence does not prove that MUJ One itself performs Microsoft Entra ID SSO or that SLCM accepts the same token.

- **Mobile-App Evidence**: A public Google Play search did not identify a dedicated MUJ One listing, publisher, package, rating, or review record in the returned result [1]. MUJStella is a separate student-built application that identifies itself as independent, while its listing reports 4.4 stars from 21 reviews and 1K+ downloads [6] [13] -> do not conflate MUJStella, MUJ GO, or the official library-app mention with MUJ One.

- **Integration Finding**: No public official page examined explicitly links MUJ One to SLCM, documents an API, or describes a shared-login handoff. MUJguide claims that its own student service can fetch timetable, attendance, marks, grades, CGPA, and transcript data from SLCM, but it also says it is operated solely by an individual and does not mention MUJ One [14] [14] [14] [14] -> classify this as third-party SLCM integration evidence, not MUJ One integration.

- **Complaints and Sentiment**: Public Reddit results contain anecdotal SLCM posts about password errors, portal access, login trouble, and downtime language [18] [19] [19] [19] [20] [20]. These results do not establish outage duration, root cause, prevalence, or MUJ One involvement -> use them as issue signals for monitoring, not as a reliability statistic.

- **Hosting and Technology Claims**: Google Public DNS returned an A record of 52.172.36.15 for MUJ One [16], and IPinfo attributes that address to AS8075 and Microsoft Corporation with an "hosting" AS type [17] [17] [17]. The supplied ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, and Akamai assertions were not independently established by the public evidence collected -> label those stack/version claims unverified and avoid turning passive metadata into a vulnerability claim.

- **Overall Verdict**: Confidence is high that the inspected MUJ One surface is an MAHE-credited HR portal, high that SLCM is a separate student/parent-facing portal, and moderate that institutional Outlook/Microsoft identity is operationally related to SLCM. Confidence is low-to-moderate for any claim of MUJ One-SLCM integration, a MUJ One mobile app, Akamai delivery, or the precise web stack -> the defensible conclusion is "related institutional ecosystem, public integration unproven."

## Scope, Evidence Boundaries, and Auditable Reasoning Summary

This report covers only publicly visible material associated with the MUJ One hostname, the MUJ SLCM hostname, official Manipal University Jaipur pages and documents, public DNS/IP records, public app-store pages, public third-party student applications, and public discussion pages. It does not attempt authentication, submit credentials, test password-reset behavior, enumerate private endpoints, scan ports, exploit a service, or access non-public data. The login discussion below describes labels and links visible without authentication; it is not an operational login guide.

The evidence hierarchy is important because the ecosystem contains official university pages, third-party services, app-directory pages, and user-generated posts. The official MUJ One HR page is strongest for what that page publicly presents. The official SLCM FAQ is strongest for the university's stated SLCM registration and support instructions. The Microsoft SOP is strong evidence for the institution's Office 365 identity process, but not automatically for an application's federation design. Third-party application pages establish what those applications claim, not that the university endorses them. Reddit establishes that people publicly discuss a problem, not that the problem is measured or confirmed.

| Evidence class | What it can establish | What it cannot establish | Representative source |
|---|---|---|---|
| Official MUJ One page | Visible labels, controls, links, and page credit | Complete product scope, backend architecture, or legal ownership | https://mujone.jaipur.manipal.edu/HR/ [5] |
| Official SLCM page and FAQ | Public portal labels, registration URL, credential guidance, support contacts | Successful authentication, token exchange, or backend integration | https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf [21] |
| Official Office 365 SOP | Institutional Microsoft sign-in, password, and MFA procedure | MUJ One or SLCM SSO implementation | https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf [22] [22] |
| DNS and IP intelligence | A-record value and network attribution snapshot | Application ownership, CDN use, framework version, or security posture | https://dns.google/resolve?name=mujone.jaipur.manipal.edu&type=A [16] |
| App stores and directories | Public listing metadata for a specific package | University endorsement or equivalence to MUJ One | https://play.google.com/store/apps/details?hl=en-US&id=com.yourcompany.mujstellaapp [13] |
| Reddit and other user posts | Anecdotal issue language and user questions | Prevalence, root cause, uptime, or representative sentiment | https://www.reddit.com/r/manipaljaipur/search/?q=SLCM&restrict_sr=1 [19] [19] |

The reasoning summary, provided instead of private chain-of-thought, is reproducible: first identify what each official surface calls itself; second separate visible facts from claims made by third parties; third compare the credential and navigation evidence without assuming that a shared university domain means shared software; and fourth treat negative findings as bounded observations rather than proof of absence. Inferences are explicitly labelled below. This approach produces a useful security-club map without crossing into unauthorized testing.

## What MUJ One Publicly Is

The strongest public identity signal is the MUJ One root page title, which says "MUJ HR SYSTEM" and displays a pre-sign-in policy notice [8]. The HR path repeats the HR identity and presents an employee-oriented set of fields: employee code, date of birth, captcha, and password-change controls [5] [5]. The page footer says "Designed and Developed by ISD/CSD, MAHE" [5]. Together, these are strong evidence about the public presentation and a stated development credit. They are not, by themselves, a full legal-entity or current operations statement.

The same HR page exposes a link labelled "Visit PAS Portal" pointing to `http://pas.muj.edu.in/` [5]. The page does not expand the PAS acronym or describe its function in the extracted public content. **Inference:** PAS is a neighbouring institutional service linked from MUJ One, but its precise business purpose should remain unknown rather than being guessed from the acronym. No SLCM link is visible in the inspected MUJ One HR page's public feature inventory [5].

This identity differs from the public SLCM surface. The SLCM page says "WELCOME TO MUJ PORTAL" and exposes "Sign In," "Parent Login," and "Student Login" labels [3]. A second official capture similarly presents the welcome page and parent-login wording [3]. The two pages may sit in the same institutional ecosystem, but their visible audience signals differ: MUJ One is HR/employee-oriented, while SLCM is student/parent-oriented.

A useful comparison is the general Manipal student portal page. That page labels itself "Student Portal" and links to `https://sis.manipal.edu/index.aspx` [9]. The official MUJ home page also presents public services such as online grievance registration, online courses, fee payment, and a student's-corner label [10] [10] [10]. Those services show that MUJ operates several digital surfaces; they do not establish that any one of them is MUJ One.

| Public surface | Exact URL | Visible identity or audience | Evidence-bounded conclusion |
|---|---|---|---|
| MUJ One root | https://mujone.jaipur.manipal.edu/ | "MUJ HR SYSTEM" and policy notice [8] | Public MUJ One surface is presented as HR-related |
| MUJ One HR path | https://mujone.jaipur.manipal.edu/HR/ | Employee code, DOB, captcha, password reset, MAHE development credit [5] | Employee-facing workflow is strongly supported |
| MUJ SLCM | https://mujslcm.jaipur.manipal.edu/ | MUJ portal, student and parent sign-in labels [3] | Separate academic portal surface is strongly supported |
| General student portal | https://www.manipal.edu/mu/academics/student-portal.html | Student Portal, link to SIS [9] | General student access is not proof of MUJ One identity |
| MUJ official home | https://jaipur.manipal.edu/ | Public services including fee payment and student's corner [10] | Institution has multiple digital services; relationship to MUJ One not established |

The decision-ready point is that "MUJ One" should not be used as a synonym for every MUJ online service. The public evidence supports a narrow description: an MAHE-credited MUJ HR system with a public HR workflow and a link to PAS. It does not support calling it the student academic portal, a mobile super-app, or the SLCM front end.

## Publicly Advertised Features and Campus Workflows

The observable MUJ One feature set is small but concrete. The HR page contains an Email label and password-reset area [5]. Its reset workflow exposes Employee Code, Date of Birth, and captcha fields [5]. It also presents a Change Password control with New Password and Confirm New Password fields [5]. Before sign-in, it asks the user to read and accept the Code of Conduct and Prevention of Sexual Harassment policies [5]. These are direct observations of the unauthenticated page, not assumptions about what happens after a successful submission.

| Observed MUJ One item | Public wording or field | Audience signal | Safe interpretation |
|---|---|---|---|
| Email entry point | "Email" [5] | Employee or institutional account context | A visible email-related entry point; backend behavior is unknown |
| Password reset | "Reset Password" [5] | Account lifecycle | Publicly advertised reset function |
| Recovery inputs | Employee Code, Date of Birth, captcha [5] | Employee identity | Reset form appears employee-oriented |
| Policy acknowledgement | Code of Conduct and Prevention of Sexual Harassment [5] | Staff compliance or institutional access | Pre-sign-in acknowledgement is visible |
| Password change | New Password and Confirm New Password [5] | Account maintenance | Change-password controls are visible |
| Neighbouring service | Visit PAS Portal [5] | Institutional workflow | MUJ One links to PAS, but PAS purpose is not stated |
| Browser note | Best Viewed in Google Chrome [5] | Presentation guidance | A compatibility note, not a security or framework claim |

The public page does not, in the extracted evidence, advertise attendance, course timetable, grades, transcript, fee ledger, hostel allocation, mess information, or a student dashboard. **Inference:** the absence of those labels from the inspected MUJ One HR surface makes a student-super-app interpretation weak, but it cannot prove that authenticated users never see additional modules. That distinction matters: an unauthenticated landing page is a product boundary signal, not a complete inventory.

The contrast with the student ecosystem is clear. A third-party SLCM guide tells students to visit the SLCM host, use MUJ email credentials, open the Attendance section, and view total classes, attended classes, missed classes, and attendance percentage [12]. Because that guide is not the official MUJ One page, it is useful for documenting what students publicly associate with SLCM, but it is not evidence that MUJ One provides those functions.

A second case study is the official MUJ library page, which calls a "MUJ Library App" a mobile access technology [2]. This shows that a mobile service can be mentioned by an official MUJ page without being the same thing as MUJ One. For a security club building an asset map, the practical recommendation is to record product names exactly as published and not collapse HR, library, student information, and SLCM services into one application merely because they share the `jaipur.manipal.edu` namespace.

## App-Store Presence and Mobile-App Attribution

The public Google Play search for "MUJ One" returned generic Play navigation and did not identify a dedicated MUJ One listing, package name, publisher, rating, review count, or feature page in the captured result [1]. This is a bounded negative: it means no dedicated listing was located in that public search result at assessment time, not that an unpublished, region-restricted, renamed, or unindexed application cannot exist. The equivalent public Apple search URL used for this assessment was `https://apps.apple.com/in/search?term=MUJ%20One`; no dedicated MUJ One record was located there either, but the returned evidence was not a preserved Apple listing document, so the Apple conclusion is lower confidence than the Google Play observation.

Several adjacent mobile artifacts require careful separation. MUJStella's own site says it is an "Independent student platform" and "Not affiliated with Manipal University Jaipur" [6]. Its Google Play page identifies the application as Mujstella and links to the MUJstella developer identity [13]. The listing reports 4.4 stars from 21 reviews and 1K+ downloads [13], and records an update on January 21, 2026 [13]. Those values describe MUJStella, not MUJ One.

The MUJStella listing describes Smart Timetable, Attendance Tracker, Study Resources, Campus Directory, and Updates and Announcements [13]. Its update notes specifically say "NEW: SLCM Portal Attendance & Timetable Tracker" [13]. The listing says the application is made for MUJ students by MUJ students [13] and names Akshit Raj in developer information [13]. This is valuable evidence of student demand for SLCM-adjacent mobile tooling, but the explicit independent-platform disclaimer prevents it from being treated as an official MUJ One app.

| Candidate mobile artifact | Exact URL | Publicly observed metadata | Attribution result |
|---|---|---|---|
| MUJ One Play search | https://play.google.com/store/search?q=MUJ%20One&c=apps | No dedicated MUJ One listing was identified in the returned search page [1] | No public package or publisher established |
| MUJ One Apple search | https://apps.apple.com/in/search?term=MUJ%20One | No dedicated result located in the assessment search; no preserved listing evidence | Absence is bounded and lower-confidence |
| MUJStella | https://play.google.com/store/apps/details?hl=en-US&id=com.yourcompany.mujstellaapp | 4.4 stars, 21 reviews, 1K+ downloads, updated January 21, 2026 [13] [13] | Student-built adjacent app; not MUJ One |
| MUJStella website | https://mujstella.in/ | Explicitly independent and not affiliated with MUJ [6] | Strong negative against official-equivalence inference |
| MUJ GO directory artifact | https://www.myandroid.org/apps/com-manipal-muj-go | Package shown as `com.manipal.muj.go` and app name MUJ GO [7] | Secondary directory artifact; publisher and current official status unverified |
| MUJ Library App mention | https://www.jaipur.manipal.edu/central-library.php | Official page calls it a mobile access technology [2] | Official mention, but no MUJ One equivalence or store listing established |

A practical mobile-app conclusion follows. There is evidence of a student-built SLCM companion market, and there is an official textual mention of a library app, but there is no captured public evidence of a dedicated official MUJ One package. Any future app attribution should require a matching official university link, store publisher identity, package name, and privacy/support information. A similar name alone is not sufficient.

## Publicly Observable Login and Identity Flow

The SLCM login surface exposes a welcome page, student and parent sign-in labels, and a forgot-password label [3]. A structured public capture reports that the form action is `https://mujslcm.jaipur.manipal.edu/`, uses POST, and includes `UserName` and `Password` fields [3]. The same capture reports a forgot-password link to `https://passwordreset.microsoftonline.com/` [3]. These are observations about public markup and links. They do not establish the result of authentication, the identity provider's token flow, MFA enforcement for SLCM, or the presence of a secure session after login.

The official SLCM FAQ provides a different kind of evidence. It names the registration link as `https://mujslcm.jaipur.manipal.edu/` [21]. It says the username is a name plus registration number, giving `garv.2506040062` as an example, and says the password is as per the official Outlook ID [21]. It also gives the university helpline and AMS support contacts [21] [21]. This is a university-published instruction and should outrank an unofficial guide when the two differ.

| Stage or artifact | Public observation | What it supports | What remains unknown |
|---|---|---|---|
| MUJ One HR page | Email, reset-password, employee-code, DOB, captcha, policy acknowledgement, change-password controls [5] | Employee-oriented account workflow | Actual authentication provider, redirect, session, and post-login modules |
| SLCM page | Student and parent sign-in labels [3] | Student/parent audience | Successful login behavior and identity federation |
| SLCM form capture | POST action to SLCM host; UserName and Password fields [3] | Public form structure | Backend validation, storage, token issuance, and authorization |
| SLCM recovery link | Microsoft password-reset URL [3] | A public link to Microsoft's reset service | Whether the application uses Microsoft Entra ID SSO or only directs users to password recovery |
| Official SLCM FAQ | Registration URL, registration-number username example, Outlook-ID password instruction [21] | Stated university credential guidance | Whether the same credential is accepted by MUJ One |
| Office 365 SOP | Microsoft portal, university mail ID, password setup, MFA [22] [22] [22] | Institutional Microsoft 365 identity process | Application-specific federation and conditional-access behavior |

There is an important credential discrepancy. The official FAQ gives a username in the form `name.registration number` [21], while an unofficial SLCM guide says the username is the full MUJ email address ending in `@muj.manipal.edu` [12]. The sources should not be silently reconciled. **Inference:** the difference may reflect different cohorts, a changed convention, or an unofficial simplification, but the public evidence cannot decide which explanation is correct. A university security club should cite the official FAQ for the documented format and direct real users to official support rather than publish a guessed normalization rule.

The Office 365 SOP is explicit about the separate Microsoft identity process. It is document IT-SOP-O365-001, version 1.0, effective June 2025, for students and employees [22]. It directs users to `https://login.microsoftonline.com/`, enter a university mail ID, enter a current or temporary password, and set a new password [22]. It then says MFA is mandatory for the university account and must be completed before Office 365 use [22]. The SOP describes Authenticator, phone, and email verification options [22]. **Inference:** this confirms an institutional Microsoft identity environment, but not an MUJ One SSO implementation. A password-reset URL and an Outlook-based password instruction are identity-context clues, not proof of an OAuth, OpenID Connect, or SAML handoff.

## MUJ One and SLCM Integration Assessment

The central integration question has four possible meanings: a visible hyperlink, a shared identity provider, a data/API integration, or a mobile wrapper. Public evidence supports only some neighbouring relationships, not an official MUJ One-SLCM connection.

| Integration type | Public evidence | Assessment |
|---|---|---|
| MUJ One navigation to SLCM | MUJ One HR page exposes a PAS Portal link, but no SLCM link in the observed feature set [5] | No explicit official navigation link found |
| SLCM navigation to MUJ One | SLCM page exposes sign-in and parent/student labels, with no MUJ One reference in the captured content [3] | No explicit reverse link found |
| Shared institutional identity context | SLCM FAQ refers to official Outlook ID [21]; Office 365 SOP documents Microsoft sign-in and MFA [22] [22] | Related identity context is supported; shared application SSO is unproven |
| Microsoft password recovery | SLCM capture links to Microsoft password reset [3] | Recovery relationship is visible; token-based federation is unproven |
| Official SLCM data API in MUJ One | No public API, data contract, or MUJ One feature description was found | No public evidence |
| Third-party SLCM data use | MUJguide says its timetable, attendance, marks, grades, CGPA, and transcript features connect to SLCM [14] [14] [14] | Third-party claim, not MUJ One integration |
| Student mobile SLCM tracking | MUJStella release notes claim SLCM attendance and timetable tracking [13] | Separate third-party app claim |

MUJguide is the clearest public case study of a claimed SLCM integration, but it also illustrates why attribution matters. The site describes itself as a free campus super-app built and operated solely by Bharath G [14]. It advertises a timetable connection that fetches a real timetable from the MUJ portal [14], an attendance connection that fetches attendance [14], and marks, grades, CGPA, and transcript information from SLCM [14]. It says SLCM credentials used for attendance are stored on the device and never transmitted to MUJguide servers [14]. These statements describe MUJguide's own architecture and claims; they do not prove a university-approved API, nor do they connect MUJguide to MUJ One.

MUJStella provides a second adjacent case. Its listing claims an SLCM attendance and timetable tracker [13], while its website explicitly disclaims affiliation with MUJ [6]. Two independent student-facing products therefore publicly point to demand for SLCM-derived convenience features, but neither is evidence of MUJ One ownership or integration.

**Inference:** the most defensible ecosystem model is a set of institutionally related but publicly distinct surfaces: MUJ One HR, MUJ SLCM academic access, Microsoft 365 identity, and independent student tools. A shared domain and a common university credential may make integration plausible, but they do not establish a shared backend, API, or SSO. The report should therefore use the phrase "public integration unproven" rather than "not integrated," because public documentation can be incomplete.

## Public Reviews, Complaints, and Reliability Signals

No dedicated MUJ One app listing was identified in the public Google Play search result, so there is no captured MUJ One star rating, review count, or store complaint record to analyze [1]. The absence of a listing also means that reviews of MUJStella cannot be transferred to MUJ One. MUJStella's 4.4-star, 21-review record is a separate product signal [13].

The public discussion evidence is concentrated on SLCM rather than MUJ One. One Reddit post is titled "Slcm portal issue" and says the user's password is showing an error despite being believed correct, then asks whether others face the issue [18]. A public SLCM search page includes titles such as "SLCM working ??," "What's SLCM username," "Slcm down!," "FINALLY SLCM WORKING!!!," and "How tf is slcm still down" [19] [19] [19] [19] [19]. These titles show recurring public discussion themes, but they do not provide a validated incident timeline.

A public portal search also contains "My Portal isn't opening," an urgent SLCM help post, and questions about allotted sections [20] [20] [20]. It includes posts saying users could not log in to Microsoft 365 and SLCM even after trying Microsoft Authenticator [20]. The page presents titles and engagement metadata, not an authoritative diagnosis or resolution; the extracted evidence explicitly shows no demonstrated resolutions for the listed entries [20].

| Public signal | Exact URL | What is directly supported | What must not be inferred |
|---|---|---|---|
| Password error report | https://www.reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue | A user publicly reported a password error and asked if others saw it [18] | That credentials, SLCM, or Microsoft identity was actually down for all users |
| SLCM search results | https://www.reddit.com/r/manipaljaipur/search/?q=SLCM&restrict_sr=1 | Public titles mention working status, username, downtime, and recovery language [19] [19] [19] [19] [19] | Uptime percentage, incident cause, or population-level sentiment |
| Portal search results | https://www.reddit.com/r/manipaljaipur/search/?q=portal&restrict_sr=1 | Titles mention opening, urgent help, login, Microsoft 365, and SLCM [20] [20] [20] | That every report concerns MUJ One or the same incident |
| MUJ One app search | https://play.google.com/store/search?q=MUJ%20One&c=apps | No dedicated MUJ One result was captured [1] | That no mobile client exists anywhere |

The sentiment conclusion is therefore qualitative and narrow: SLCM access and credential problems are visible topics in public student discussions, while MUJ One-specific user sentiment is not publicly established in the captured sources. **Inference:** a club can use these posts as leads for an official support and status-page review, but should not publish a claim such as "SLCM is unreliable" without time-bounded measurements or university incident data. The official FAQ's AMS and IT Infra contacts provide an appropriate public support path for users who have a real account problem [21].

## Hosting, DNS, and Technology Claims

The MUJ One hostname resolves publicly in Google Public DNS to 52.172.36.15 in the captured A-record response [16]. IPinfo identifies the address as 52.172.36.15, AS8075, Microsoft Corporation, and an AS type of hosting [17] [17] [17]. This is consistent with Microsoft-hosted infrastructure and with the supplied Azure observation. It is not proof that Microsoft owns the application, that MUJ owns the address, or that the application is hosted directly on a particular Azure service.

A separate CNAME query returned no CNAME answer in the captured response [23]. **Inference:** the observed DNS evidence does not expose an Akamai CNAME at that moment, but the absence of a CNAME answer does not prove that Akamai, another reverse proxy, or an upstream service is absent. CDNs can be represented through A records, provider-specific routing, or configurations not visible from one public DNS query. The safe statement is simply that Akamai delivery was not independently confirmed by the evidence cited here.

| Technical assertion or clue | Public evidence | Assessment |
|---|---|---|
| MUJ One address 52.172.36.15 | Google DNS A record [16] | Confirmed as the captured DNS answer at assessment time |
| Microsoft network attribution | IPinfo shows AS8075 and Microsoft Corporation [17] [17] | Confirmed attribution of the IP record; application ownership not established |
| Hosting classification | IPinfo reports AS Type hosting [17] | Network classification only |
| Akamai reverse proxy | CNAME query did not return a CNAME answer [23] | Not independently confirmed; negative is inconclusive |
| ASP.NET MVC 5.3 | SLCM public markup exposes a form and common JavaScript/theme clues [3] | Exact MVC version not established |
| .NET Framework 4.x | No version string in the cited public evidence | Unverified |
| IIS 10 | No server banner or official technology statement in the cited evidence | Unverified |
| jQuery and Keen theme assets | Public SLCM capture reports jQuery 1.10.2, jQuery Validate, unobtrusive validation, and Keen assets [3] | Static asset clues only; not proof of server framework or patch state |
| Microsoft 365 identity | Official SOP documents Microsoft sign-in, university mail ID, password setup, and MFA [22] [22] | Institutional identity environment confirmed; app SSO not proven |
| Microsoft-hosted email DNS | MUJ domain TXT response includes `spf.protection.outlook.com` and Microsoft verification material [15] | Supports Microsoft-hosted mail context; not application SSO proof |

The supplied stack statement should thus be split into verified and unverified parts. The public SLCM markup has a conventional form action and JavaScript validation assets [3], and a public JavaScript URL contains a login-page script [4]. Those clues are compatible with many web architectures. They do not independently prove ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, or a particular security patch level. Passive fingerprinting should be treated as a hypothesis generator, not as a finding of vulnerability.

For the university security club, the key risk-control lesson is attribution discipline. A Microsoft IP does not mean an application is secure because it is in Azure. A missing CNAME does not mean there is no CDN. A JavaScript theme does not identify a server framework. These are useful OSINT clues, but not authorization to probe the service.

## Case Studies and Safe Security-Club Implications

**Case study 1: official boundary versus assumed super-app.** MUJ One's public HR page exposes employee controls and a PAS link [5], while the SLCM page exposes student and parent sign-in [3]. A researcher who treats the common MUJ branding as one application could incorrectly attribute student features to an HR portal. The mechanism behind the confusion is naming and institutional namespace reuse: users see "MUJ" in multiple service names, while the pages reveal different audiences. The implication is an asset inventory error, which can lead to incorrect threat modeling. The recommendation is to keep separate records for hostname, path, audience, owner/developer credit, authentication evidence, and data function.

**Case study 2: third-party convenience versus official attribution.** MUJguide publicly advertises SLCM-derived timetable, attendance, and academic data [14] [14] [14]. MUJStella separately advertises an SLCM tracker [13], but its own site says it is not affiliated with MUJ [6]. The mechanism is a student demand for a more convenient interface around an academic portal. The implication is that a feature appearing in a third-party app is evidence of demand and a claimed integration path, not evidence that MUJ One supplies or authorizes the feature. The recommendation is to label third-party claims as claims and record their privacy, developer, and credential-handling statements separately.

**Case study 3: identity correlation without SSO proof.** The SLCM FAQ ties its password instruction to the official Outlook ID [21]. The SLCM markup points password recovery to Microsoft's reset service [3]. The Office 365 SOP describes Microsoft sign-in and mandatory MFA for university accounts [22]. The mechanism is a shared institutional identity environment, which makes operational coupling plausible. The implication is that a researcher could overstate the evidence and call this proven federation. The recommendation is to say "Microsoft identity context is documented; MUJ One/SLCM token federation is not publicly documented" unless an official architecture or user-facing redirect explicitly proves it.

| Security-club question | Evidence-led answer | Safe next action using public information only |
|---|---|---|
| Is MUJ One the student SLCM portal? | No; public labels and audiences differ [5] [3] | Keep separate asset records |
| Is Microsoft 365 part of the institutional identity environment? | Yes, for Office 365; SLCM also references Outlook credentials [22] [21] | Cite the distinction between identity context and application SSO |
| Is MUJ One-SLCM data integration public? | No explicit official integration found; third-party integrations are documented as third-party claims [14] [14] | Monitor official documentation and preserve dated public evidence |
| Is a MUJ One mobile app proven? | No dedicated store listing was captured; adjacent apps are separate [1] [6] | Require publisher/package confirmation before attribution |
| Are SLCM outages proven? | Public posts contain downtime and login language, but no validated timeline [19] [20] | Treat posts as leads, not reliability metrics |
| Are the supplied stack versions proven? | No; only generic markup and asset clues are visible [3] [4] | Record as unverified hypotheses and do not scan without authorization |

These cases reveal a consistent pattern: the ecosystem is easy to associate and difficult to prove as one technical system. The safe research product is therefore a relationship graph with confidence labels, not a single architecture diagram presented as fact.

## Synthesis: What the Evidence Says Across the Ecosystem

The most important comparison is not between brand names but between scope, mechanism, and evidence quality.

| Entity or surface | Primary scope | Visible mechanism | Evidence strength | Main trade-off or risk |
|---|---|---|---|---|
| MUJ One | HR and employee account workflow | Employee code, DOB, captcha, policy acknowledgement, reset/change-password controls [5] | High for visible page identity and fields | Narrow public surface may hide additional authenticated functions |
| MUJ SLCM | Student and parent academic portal | Student/parent sign-in, UserName/Password form, Microsoft password-reset link [3] | High for public login surface; moderate for credential guidance | Credential conventions appear inconsistent between official and unofficial sources [21] [12] |
| Microsoft 365 identity | Institutional mail and account security | Microsoft login, university mail ID, password setup, mandatory MFA [22] | High for Office 365 procedure | Institutional identity evidence does not prove app federation |
| MUJguide | Student convenience layer over claimed SLCM data | Timetable, attendance, marks, grades, CGPA, transcript claims [14] [14] | Moderate for what the site claims | Third-party status and credential-handling trust must be evaluated separately [14] [14] |
| MUJStella | Student mobile companion | Timetable, attendance, campus directory, announcements, SLCM tracker [13] [13] | High for store metadata; low for official endorsement | Explicitly independent from MUJ [6] |
| MUJ Library App | Library access | Official page calls it mobile access technology [2] | Moderate for official mention | No public evidence equates it with MUJ One |

Three tensions stand out. First, the official surfaces are narrower than the student-created tools: MUJ One visibly emphasizes HR compliance and account maintenance, while MUJguide and MUJStella emphasize attendance, timetable, and academic convenience [5] [14] [13]. This divergence suggests different product scopes, not necessarily a hidden MUJ One feature set.

Second, identity evidence is stronger than integration evidence. The official FAQ references Outlook credentials, the SLCM page points to Microsoft password reset, and the Office 365 SOP mandates Microsoft account MFA [21] [3] [22]. Yet no cited source says that MUJ One or SLCM accepts a Microsoft-issued application token, redirects to an institutional tenant, or exchanges a SAML/OIDC assertion. The mechanism that can explain shared passwords or recovery is not necessarily the mechanism that proves SSO.

Third, public user demand is stronger than official mobile attribution. Student applications publicly claim SLCM tracking and have store metadata, including reviews and downloads for MUJStella [13] [13]. The MUJ One Play search, by contrast, does not expose a dedicated official listing [1]. This may reflect a web-first HR design, an unlisted mobile experience, or a different product name; public evidence cannot choose among those possibilities.

The combined conclusion is an evidence-bounded graph: MUJ One, SLCM, and Microsoft 365 are institutionally adjacent; student tools publicly consume or claim to consume SLCM-related data; and the public record does not establish a direct MUJ One-SLCM data or authentication integration. The recommendation is to preserve this distinction in every club presentation, threat model, and future research note.

## VERDICT

**Overall verdict: MUJ One is publicly evidenced as an MAHE-credited, HR-oriented web portal at `mujone.jaipur.manipal.edu`; MUJ SLCM is a separate student/parent-facing academic portal; and a direct MUJ One-SLCM integration is not publicly proven.** The Microsoft 365 relationship is credible as an institutional identity context because the official Office 365 SOP documents Microsoft sign-in, university mail IDs, password setup, and mandatory MFA, while the official SLCM FAQ references the Outlook ID [22] [22] [21]. It remains unproven that either application uses Microsoft Entra ID SSO or a shared token flow.

| Finding | Confidence | Reason |
|---|---|---|
| MUJ One public surface is HR-oriented | High | Root title and HR page fields/credits are explicit [8] [5] |
| MUJ SLCM is a distinct student/parent portal | High | Official page labels student and parent sign-in [3] |
| SLCM has an Outlook/Microsoft identity context | Moderate to high | Official FAQ and Microsoft reset link support the relationship [21] [3] |
| Office 365 uses Microsoft sign-in and mandatory MFA | High | Official June 2025 SOP states the process [22] [22] |
| MUJ One uses the same SSO as SLCM | Low | No public token, redirect, or official architecture evidence |
| MUJ One directly integrates SLCM data | Low | No official link/API/module found; third-party tools are separate [14] |
| Dedicated official MUJ One Android/iOS app | Low | No dedicated Google Play result captured; Apple result not preserved as a listing [1] |
| MUJ One is hosted on Microsoft-attributed infrastructure | Moderate to high | DNS and IPinfo support the address/network attribution [16] [17] [17] |
| Akamai is confirmed in front of MUJ One/SLCM | Low | Captured CNAME response did not expose Akamai and no independent source confirmed it [23] |
| ASP.NET MVC 5.3, .NET 4.x, IIS 10 are confirmed | Low | Public evidence shows generic form and assets, not exact versions [3] [4] |
| SLCM has public access/credential complaints | Moderate as an anecdotal signal | Reddit titles and one password-error post support discussion, not prevalence [18] [19] [20] |

**Confidence statement:** high for page labels, visible controls, official document wording, and captured DNS/IP observations; moderate for the institutional identity relationship; low-to-moderate for mobile absence, third-party integration implications, CDN attribution, and exact technology versions. The principal unanswered questions are the authenticated MUJ One feature set, the actual SSO/token architecture, any official API between systems, the purpose of PAS, current app publication status outside the captured searches, and validated reliability metrics.

For an OSINT-only university security club, the defensible publication language is: **"MUJ One and MUJ SLCM are publicly distinct MUJ-branded surfaces with a documented Microsoft 365 identity context, but public evidence does not prove that MUJ One integrates with SLCM or that the supplied stack/CDN claims are accurate."** Any deeper answer would require official documentation or explicit authorization for testing, neither of which is assumed here.

## References: Exact URLs

| Citation IDs used | Exact source URL |
|---|---|
| [8] | https://mujone.jaipur.manipal.edu/ |
| [5] | https://mujone.jaipur.manipal.edu/HR/ |
| [3], [3], [3] | https://mujslcm.jaipur.manipal.edu/ |
| [4] | http://mujslcm.jaipur.manipal.edu/keen/themes/keen/theme/demo1/dist/assets/js/pages/custom/user/login.js |
| [21] | https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf |
| [22] | https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf |
| [15] | https://dns.google/resolve?name=muj.manipal.edu&type=TXT |
| [16] | https://dns.google/resolve?name=mujone.jaipur.manipal.edu&type=A |
| [23] | https://dns.google/resolve?name=mujone.jaipur.manipal.edu&type=CNAME |
| [17], [17], [17] | https://ipinfo.io/52.172.36.15 |
| [12] | https://slcm.vercel.app/guides/check-attendance-muj |
| [14], [14], [14] | https://www.mujguide.in/ |
| [6] | https://mujstella.in/ |
| [13] | https://play.google.com/store/apps/details?hl=en-US&id=com.yourcompany.mujstellaapp |
| [1] | https://play.google.com/store/search?q=MUJ%20One&c=apps |
| [7] | https://www.myandroid.org/apps/com-manipal-muj-go |
| [2] | https://www.jaipur.manipal.edu/central-library.php |
| [9] | https://www.manipal.edu/mu/academics/student-portal.html |
| [10], [10], [10] | https://jaipur.manipal.edu/ |
| [18] | https://www.reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue |
| [19] | https://www.reddit.com/r/manipaljaipur/search/?q=SLCM&restrict_sr=1 |
| [20] | https://www.reddit.com/r/manipaljaipur/search/?q=portal&restrict_sr=1 |
| Apple search checked for bounded app-presence review | https://apps.apple.com/in/search?term=MUJ%20One |

## References

1. *MUJ One - Android Apps on Google Play*. https://play.google.com/store/search?q=MUJ%20One&c=apps
2. *Library - Manipal University Jaipur *. https://www.jaipur.manipal.edu/central-library.php
3. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
4. *mujslcm.jaipur.manipal.edu*. http://mujslcm.jaipur.manipal.edu/keen/themes/keen/theme/demo1/dist/assets/js/pages/custom/user/login.js
5. *MUJ HR SYSTEM - Manipal Academy of Higher Education*. https://mujone.jaipur.manipal.edu/HR
6. *MUJStella - Student Platform for Manipal University Jaipur*. https://mujstella.in/
7. *MUJ GO*. https://www.myandroid.org/apps/com-manipal-muj-go
8. *MUJ HR SYSTEM*. https://mujone.jaipur.manipal.edu/
9. *Student Portal Login- MAHE (Manipal Academy Of Higher Education)*. https://www.manipal.edu/mu/academics/student-portal.html
10. *Manipal University Jaipur - 71 years of legacy of Manipal Education*. https://jaipur.manipal.edu/
11. *http://internshala.com/competitions/hackx-3-0*. http://internshala.com/competitions/hackx-3-0
12. *How to Check Your Attendance at MUJ | mujslcm Guide | betterSLCM*. https://slcm.vercel.app/guides/check-attendance-muj
13. *Mujstella - Apps on Google Play*. https://play.google.com/store/apps/details?hl=en-US&id=com.yourcompany.mujstellaapp
14. *MUJguide — Student Platform for Manipal University Jaipur*. https://www.mujguide.in/
15. *dns.google*. https://dns.google/resolve?name=muj.manipal.edu&type=TXT
16. *dns.google*. https://dns.google/resolve?name=mujone.jaipur.manipal.edu&type=A
17. *52.172.36.15 | Chennai, AS8075, VPN Not Detected | IPinfo*. https://ipinfo.io/52.172.36.15
18. *Reddit - The heart of the internet*. https://www.reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue
19. *Reddit - The heart of the internet*. https://www.reddit.com/r/manipaljaipur/search/?q=SLCM&restrict_sr=1
20. *Reddit - The heart of the internet*. https://www.reddit.com/r/manipaljaipur/search/?q=portal&restrict_sr=1
21. *Frequently Asked Questions and Contacts for SLCM Registration*. https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf
22. *Standard Operating Procedure*. https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf
23. *dns.google*. https://dns.google/resolve?name=mujone.jaipur.manipal.edu&type=CNAME
