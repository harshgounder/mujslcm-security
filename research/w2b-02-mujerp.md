# MUJ SLCM and ERP: Public OSINT Assessment

## Executive Summary

This report assesses publicly visible information about the Manipal University Jaipur (MUJ) student-life-cycle environment and the related hostname `mujerp.jaipur.manipal.edu`. It is a passive OSINT review. It does not submit credentials, attempt authentication, enumerate protected content, scan infrastructure, exploit routes, or test access controls. The evidence reviewed was limited to public web pages, public MUJ documents, public product documentation, and public third-party references.

- **Business ERP Identity**: The public ERP hostname displays the title "Welcome to Dynamics 365 Business Central" and exposes only user-name and password labels in the retrieved page content [1]. MUJ's official IT page separately describes Microsoft services for "Business ERP" and a "Student life cycle via Web portal" [14]. **Action**: Treat `mujerp` as a probable business or administrative ERP surface, but do not represent that relationship as an officially published hostname-to-system mapping.
- **Student-System Separation**: MUJ's official IT description lists ERP and the student life-cycle web portal as distinct elements of its IT landscape [14]. The official first-year guide calls SLCM a one-stop platform for academic information [13]. **Action**: Analyze SLCM and `mujerp` as related institutional systems, not as one proven application or database.
- **Likely Audience**: The SLCM public interface explicitly shows student and parent login choices [4], while the `mujerp` page shows no audience, faculty label, staff label, or module list [1]. It is an **inference**, not a confirmed fact, that the ERP is more likely aimed at internal business users, potentially including staff or faculty, because MUJ calls it Business ERP and names Microsoft Business ERP separately from the student portal [14]. **Action**: Mark staff/faculty access as unconfirmed until MUJ publishes an official user guide or system notice.
- **Academic Data**: The official onboarding guide states that SLCM provides academic information and collects identity, admission, educational-qualification, address, parent-contact, and document data [13]. **Action**: Academic and admission-related data are strongly supported for SLCM, but the public evidence does not prove that those data reside in `mujerp`.
- **Attendance and Grades**: An indexed SLCM attendance-summary URL returned only the generic login page, not attendance records [15]. Independent public tools and a GitHub README claim attendance, grades, GPA/CGPA, timetable, and parent/student login functionality for SLCM [5][18]. **Action**: Treat attendance and grades as credible SLCM feature leads, not as evidence of publicly accessible records or `mujerp` functionality.
- **Payroll**: MUJ's official Finance page states that Finance provides payroll services to faculty and staff [17] and describes accounting, financial reporting, budgets, payables, and financial data [17]. The separate MUJ HR page describes compensation, benefits, leave management, and employee lifecycle activities [19]. **Action**: Payroll exists as an institutional business function, but no public source reviewed states that payroll is a module in `mujerp`.
- **Authentication**: The SLCM FAQ states that the registration link is the MUJ SLCM hostname and describes a username pattern based on name and registration number, with the password tied to the official Outlook ID [7]. The public SLCM markup also shows a POST form, username/password inputs, an `@muj.manipal.edu` suffix, student/parent controls, and a Microsoft password-reset URL [224.0-2; raw public markup]. **Action**: Describe this as an institutional account relationship and visible login flow, not proof of modern Microsoft Entra ID, OAuth, SAML, or any particular federation architecture.
- **Technology Claims**: The supplied context names ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, Microsoft 365 identity, and Azure IP `20.244.0.229`. The public pages reviewed did not independently establish all of those details. **Action**: Keep them in a hypothesis or assessment-input column, not in the confirmed technology inventory.
- **Public Exposure**: The portals expose login pages and route names to unauthenticated visitors, but the retrieved protected-looking attendance route returned a login wall [15]. **Action**: Do not equate discoverability of a URL, route, IP, or login form with data exposure or vulnerability.

## Scope, Method, and Evidence Standard

The assessment answers five practical questions: what SLCM appears to do; what `mujerp` publicly identifies as; whether `mujerp` appears to be staff/faculty-facing; what features and data types are publicly described; and which infrastructure claims remain unverified. The evidence standard is conservative: a fact is confirmed only when the page itself states it. A feature mentioned by a student-built application is reported as a third-party claim, not as an official MUJ specification.

The phrase "chain-of-thought" in the request is addressed here through an auditable research summary rather than private internal reasoning. The decision sequence was: identify first-party MUJ pages; inspect the public login surfaces without submitting anything; read the official SLCM FAQ and onboarding guide; compare the official IT architecture description with the ERP page; use Microsoft documentation only for generic product context; then test each requested data category against explicit evidence. This is a reproducible evidence trail, not hidden step-by-step reasoning.

| Evidence class | Sources used | What it can establish | What it cannot establish |
|---|---|---|---|
| Official MUJ portal | `https://mujslcm.jaipur.manipal.edu/` | Public branding and visible login choices [4] | Protected features, records, or security posture |
| Official MUJ documents | SLCM FAQ and first-year guide | Credential onboarding, profile/document fields, support and academic-information purpose [13][7] | `mujerp` ownership of those data |
| Official MUJ IT page | `https://www.jaipur.manipal.edu/administration-it.php` | MUJ's high-level distinction between Business ERP and student life-cycle web portal [14] | The hostname, vendor configuration, or module inventory |
| ERP login page | `https://mujerp.jaipur.manipal.edu/MUJWEB/` | Dynamics 365 Business Central title and basic credential fields [1] | Audience, enabled modules, data, or authorization design |
| Official MUJ Finance/HR pages | MUJ Finance and HR pages | Payroll as a Finance service and HR processes [17][19] | Payroll's technical system or `mujerp` mapping |
| Third-party public sources | GitHub, betterSLCM, MUJStella | Independent ecosystem claims and feature leads [5][3][18] | Official MUJ endorsement, safe operation, or current production configuration |

The table's key implication is that the strongest evidence supports institutional roles and SLCM data collection, while the central question - exactly what `mujerp` contains - remains underdocumented publicly.

## MUJ's Published Digital-System Context

MUJ's official Digital Infrastructure and Technology Services page says its remit includes ERP, LMS, network infrastructure, server infrastructure, backup strategies, telecommunications, and IT security [14]. It also states that the MUJ IT landscape includes Microsoft services for communication and Business ERP, a student life cycle via web portal, an LMS, and a research management system [14]. This is the most important public architectural clue because it establishes a category-level separation between business operations and student life-cycle services.

The wording does not say that `mujerp.jaipur.manipal.edu` is the Business ERP hostname. That link is plausible because the hostname includes `erp`, the page is branded Business Central, and MUJ says Microsoft provides Business ERP [1][14]. However, the link is still an inference. The official page does not publish a hostname, tenant identifier, Business Central environment name, implementation partner, or diagram showing data flows between the systems.

MUJ also says its IT services support faculty, staff, and students in a student-centric digital ecosystem [14]. That statement proves the intended institutional constituency of IT services generally, not the audience of a particular application. It therefore cannot answer whether `mujerp` is staff-only, faculty-enabled, finance-only, or shared across administrative roles.

| Published system/context statement | Direct public evidence | Assessment |
|---|---|---|
| ERP is an MUJ IT responsibility | MUJ says IT develops, maintains, supports, and optimises ERP and related infrastructure [14] | Confirmed at institutional level |
| Microsoft supports Business ERP | MUJ says its IT landscape includes Microsoft services for communication and Business ERP [14] | Confirmed at institutional level |
| Student life cycle is delivered through a web portal | MUJ names "Student life cycle via Web portal" [14] | Confirmed at category level |
| `mujerp` is that Business ERP | Hostname and page branding suggest it; MUJ does not explicitly map the hostname [1][14] | Inference |
| `mujerp` is for staff/faculty | No public `mujerp` page states this [1] | Unknown |

The decision-ready conclusion is to use the official IT page as a system-context source, not as a detailed application inventory. Any security-club diagram should show the Business ERP and SLCM as separate boxes with a dotted, explicitly unverified relationship.

## What the `mujerp` Portal Publicly Reveals

The public page title is "Welcome to Dynamics 365 Business Central" [1]. The visible extracted interface contains "User name:" and "Password:" [1]. Public server-rendered markup also shows a form posting to `/MUJWEB/SignIn`, a return URL for `/MUJWEB/`, and required user-name and password fields. These observations describe the public sign-in surface only; they do not involve submitting the form or testing any credentials.

The page does not publicly state that it is a staff portal, faculty portal, finance portal, payroll portal, procurement portal, or academic portal [1]. It does not expose a module menu, user guide, public privacy notice describing data categories, role matrix, organization name in the visible login content, or a public system owner. The page title is strong evidence of the product family, but product identity is not equivalent to deployment configuration.

Microsoft's own generic Business Central page describes the product as AI-powered ERP for small and midsize businesses and lists comprehensive business management [9]. It describes finance, sales, service, operations, dashboards, reports, and role-based KPIs [9]. Microsoft's finance documentation additionally describes accounting, budgeting, receivables, payables, bank reconciliation, financial reporting, and payroll transaction imports [16].

Those generic capabilities help explain why MUJ may use Business Central for administrative operations, but they do not prove which capabilities MUJ enabled. In particular, "payroll transaction imports" is not the same as a payroll engine, and generic product documentation cannot prove that MUJ uses Business Central for payroll, attendance, student records, or faculty workflows.

| Question about `mujerp` | Public observation | Confidence |
|---|---|---|
| Product identity | Page title identifies Dynamics 365 Business Central [1] | High |
| Basic login flow | User-name and password fields are visible [1] | High |
| Form endpoint | Public markup shows POST to `/MUJWEB/SignIn` | High for observed markup; not a security conclusion |
| Staff audience | Not stated | Low/unknown |
| Faculty audience | Not stated | Low/unknown |
| Finance/accounting modules | Generic Business Central docs describe them, but MUJ configuration is not published [16] | Low for MUJ-specific claim |
| Payroll module | Not stated by the MUJ ERP page; MUJ Finance separately states payroll as a service [17] | Low for `mujerp` mapping |
| Attendance module | Not stated | Low/unknown |
| Academic-record module | Not stated | Low/unknown |

The practical conclusion is narrow but useful: the portal is publicly identifiable as a Business Central sign-in surface, while its tenant-specific purpose and data remain non-public.

## SLCM Purpose, Login Flow, and Academic Data

The official MUJ SLCM landing page says "WELCOME TO MUJ PORTAL" and displays Sign In and Parent Login controls [4]. Public markup further exposes student and parent login controls, a username input, a password input, an `@muj.manipal.edu` suffix, and a Microsoft password-reset destination. These are observations about the page presentation and form structure, not a claim that Microsoft 365 performs the actual authentication through a particular protocol.

The official SLCM FAQ identifies the registration link as `https://mujslcm.jaipur.manipal.edu/` and gives a username pattern described as name plus registration number; it says the password is according to the official Outlook ID [7]. The same FAQ includes AMS support, IT support, an academic-section contact, and a workflow for correcting personal details through Admissions [7]. These details support the conclusion that SLCM is part of MUJ's student-administration process.

The official first-year guide is more explicit. It says SLCM serves as a one-stop platform for accessing academic information throughout a student's time at the university [13]. It says credentials are sent to a personal Gmail address supplied during admission, and that an official-email password-reset procedure is included in the email [13]. The guide directs students to a Student Details section and lists registration number, name, academic year, program/branch, date of joining, date of birth, gender, mobile number, program duration, disability status, email, and year of admission [13].

The same guide describes educational qualifications, permanent and present addresses, parent contact details, OTP verification, parent-login enablement, and uploaded admission documents [13]. This is direct evidence that SLCM onboarding handles personal, admission, identity, contact, educational, and document data. It is not evidence that the same data is stored in the Business Central portal.

| SLCM data or function | Official public evidence | Status |
|---|---|---|
| Academic-information purpose | SLCM is described as a one-stop platform for academic information [13] | Confirmed |
| Student login | Public portal has Sign In and student-oriented onboarding [4][13] | Confirmed |
| Parent login | Public interface shows Parent Login; OTP verification enables parent login [4][13] | Confirmed |
| Identity/admission profile | Guide lists identity and admission fields [13] | Confirmed |
| Educational qualifications | Guide requests qualifications chronologically [13] | Confirmed |
| Contact/address data | Guide requests addresses and parent contact details [13] | Confirmed |
| Uploaded documents | Guide requires admission and identity documents and describes a List of Documents tab [13] | Confirmed |
| Attendance | Official public page does not display records; independent sources claim an SLCM attendance feature [15][5] | Likely SLCM lead, not official module proof |
| Grades/results | Third-party sources claim grades or GPA/CGPA; the public portal response shows no records [18][15] | Third-party lead |
| Payroll | No SLCM onboarding evidence states payroll | Not supported |

This distinction matters to the security club: the official material demonstrates data sensitivity without demonstrating public exposure. The portal's login page is a boundary, and the retrieved attendance route returned that boundary rather than a record.

## Attendance, Grades, and Academic Records: What Can Be Said Safely

The URL `https://mujslcm.jaipur.manipal.edu/Student/Academic/AttendanceSummaryForStudent` is publicly indexed, but a GET retrieval returned the generic MUJ portal with Sign In, the MUJ email suffix, and Parent Login controls [15]. No attendance number, course row, student identity, grade, or academic record appeared. The correct OSINT conclusion is therefore that an attendance-summary route name is publicly discoverable, not that attendance data is publicly accessible.

A public betterSLCM guide claims that SLCM displays attendance per course, total classes, attended classes, missed classes, and an attendance percentage [5]. It also claims that betterSLCM presents the same attendance data with visual indicators, prediction, and history [5]. This is useful ecosystem evidence, but it is not an official MUJ specification. The page's claims should be labeled third-party and time-sensitive.

A public GitHub repository describes itself as an app version for MUJ SLCM and says it is designed to provide a modern interface for the university's SLCM website [18]. Its README claims student attendance, grades, timetable, student/parent authentication, and automatic display of grades, GPA/CGPA, and subject-wise attendance [18]. The README does not identify the app as an official MUJ system [18].

MUJStella is even more explicit about its status: its public page labels it an independent student platform and says it is not affiliated with Manipal University Jaipur [3]. It should not be cited as institutional confirmation. Taken together, these sources make attendance and academic-record functionality plausible for SLCM, but they do not establish that `mujerp` contains those records, that the data is publicly readable, or that any third-party tool is authorized.

| Claim | Best available source | Safe wording |
|---|---|---|
| Attendance route exists in public indexing | MUJ route returned generic login [15] | A route is discoverable; records were not observed |
| SLCM has attendance capability | betterSLCM and GitHub claims [5][18] | Third-party sources claim it |
| SLCM has grades/GPA | GitHub README claim [18] | Third-party claim, not official proof |
| SLCM has timetable | GitHub README claim [18] | Third-party claim |
| `mujerp` stores attendance or grades | No source reviewed says this [1][14] | Unknown |
| Academic data is sensitive | Official guide lists identity, education, contact, and documents [13] | Supported by the fields described |

The security implication is that a login wall protects a potentially sensitive student-information environment, but public OSINT alone cannot assess the effectiveness of that protection.

## Payroll, Staff, Faculty, and HR Separation

MUJ's official Finance page states that the Finance Department handles financial accounts and activities for MUJ and constituent institutions [17]. It specifically states that Finance provides payroll services to all faculty and staff [17]. It also lists financial accounting and reporting, books of account, monthly closure, financial statements, annual budgets, vendor payments, accounts payable, audits, taxes, and financial data for ranking and accreditation [17].

MUJ's official HR page says HR manages recruitment, onboarding, performance appraisal, promotions, compensation, policy, and employee welfare across academic, research, and administrative functions [19]. It also lists employee lifecycle, performance management, compensation and benefits, pay structures, benefits, and leave management [19]. These sources establish that faculty/staff administration and payroll-related institutional functions exist.

The separate public MUJ HR System page displays Email, Employee Code, Date of Birth, captcha, password-reset, password-change, and policy-acknowledgement controls [6]. It is therefore reasonable to distinguish the HR login surface from SLCM. However, the HR page does not state payroll, attendance, or specific HR modules [6]. It also does not state that it is backed by Business Central.

The strongest inference is that `mujerp` may support internal business operations, while the HR system and SLCM are separate surfaces. The inference rests on three facts: MUJ calls Microsoft functionality Business ERP; the ERP page identifies Business Central; and MUJ publishes separate SLCM and HR login experiences [14][1][6]. The inference does not identify the actual user population or data flows.

| Requested question | Official evidence | Verdict |
|---|---|---|
| Does MUJ have staff/faculty payroll? | Finance says payroll services are provided to faculty and staff [17] | Yes, institutional function confirmed |
| Is payroll in `mujerp`? | No MUJ `mujerp` page or official mapping states this [1] | Unknown |
| Is `mujerp` for staff? | No public audience label [1] | Unknown; plausible inference |
| Is `mujerp` for faculty? | No public audience label [1] | Unknown |
| Is there a separate HR system? | Public page titled MUJ HR SYSTEM with employee-oriented fields [6] | Yes, public login surface confirmed |
| Is the HR system Business Central? | No source reviewed says this | Unknown |

A report for the club should therefore avoid the shortcut "ERP equals payroll." An ERP product can support finance and payroll integrations, while payroll may be operated by a separate HR or finance service.

## Login and Identity Observations Without Authentication Testing

The SLCM public interface has two visible user paths: student and parent [4]. The official onboarding guide says parent login becomes available after parent mobile and email details are submitted and verified by OTP [13]. The FAQ describes official Outlook identity and an official-email password-reset process [7][13].

Public markup for SLCM shows a username input, password input, a displayed `@muj.manipal.edu` suffix, student and parent submit controls, a hidden request-verification token, and a Microsoft password-reset link. These are page-level observations. They do not prove that the portal delegates authentication to Microsoft 365, uses Entra ID, uses OAuth, uses SAML, or applies conditional access. A Microsoft password-reset destination may indicate account integration, but the exact trust relationship is not publicly documented in the reviewed pages.

The ERP page's public markup shows a conventional form POST to `/MUJWEB/SignIn` with required user-name and password fields. The retrieved page also identifies Business Central [1]. No SSO button, Microsoft login redirect, staff/faculty selector, password-reset control, or public role description appeared in the extracted ERP content [1].

| Surface | Publicly visible flow | Not established |
|---|---|---|
| SLCM | Student/parent controls, username/password presentation, MUJ email suffix, password-reset relationship [4][7] | Protocol, token lifecycle, MFA, federation, authorization rules |
| SLCM attendance route | Returns generic login page [15] | Whether protected content is reachable after authorization |
| `mujerp` | User name, password, and Business Central branding [1] | SSO, roles, MFA, tenant, modules, data |
| MUJ HR System | Email, employee code, date of birth, captcha, policy acknowledgement [6] | Payroll implementation, SSO, role model, backend |

The safe conclusion is that public login behavior provides useful inventory information but does not justify application-security findings. A security club should not attempt to validate the unknowns against live production systems without written authorization.

## Technology and Infrastructure Claims: Confirmed, Unconfirmed, and Inference

The public evidence confirms the `mujerp` page's Business Central branding [1] and MUJ's institutional use of Microsoft services for communication and Business ERP [14]. It does not independently confirm the supplied Azure address `20.244.0.229`, ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, or Microsoft 365 identity for the specific systems.

The SLCM page's markup visibly references jQuery, validation scripts, a login theme, and an MVC-style request-verification token. Those clues may be consistent with a Microsoft web stack, but they are not a reliable version fingerprint. A visible script path or form token cannot establish the exact framework version, server version, patch level, reverse proxy, CDN, or hosting provider. The report therefore does not convert the supplied technology inventory into a confirmed finding.

The ERP page's `/MUJWEB/` path and Business Central title are stronger product clues than a guessed server-stack fingerprint [1]. Even so, Business Central can be deployed in different environments and customized. Microsoft product documentation describes capabilities at the product level, not the MUJ tenant level [9][16].

| Technology/infrastructure item | Public evidence reviewed | Status |
|---|---|---|
| Dynamics 365 Business Central on `mujerp` | Page title [1] | Confirmed public branding |
| Microsoft Business ERP in MUJ IT landscape | Official MUJ IT page [14] | Confirmed institutional statement |
| Microsoft 365/Outlook relationship for SLCM accounts | FAQ and reset wording [7][13] | Account relationship supported; exact identity protocol unknown |
| ASP.NET MVC 5.3 | No public source reviewed states the version | Unconfirmed |
| .NET Framework 4.x | No public source reviewed states the version | Unconfirmed |
| IIS 10 | No public source reviewed states the version | Unconfirmed |
| Akamai edge/CDN | No public source reviewed states it | Unconfirmed |
| Azure IP `20.244.0.229` for `mujerp` | No public source reviewed maps the IP to the hostname | Unconfirmed |

This table should be carried into any future authorized assessment as an evidence-status register. It prevents a passive OSINT report from accidentally publishing a speculative fingerprint as fact.

## Public Mentions and Source Reliability

The most authoritative public mention of SLCM is MUJ's own FAQ, which names the registration link, credential convention, AMS support, academic contact, and personal-detail correction process [7]. The first-year guide is also official and describes academic-information access, onboarding data, parent-login enablement, and document uploads [13].

The most authoritative public mention of `mujerp` is the page itself, which identifies Dynamics 365 Business Central and shows a basic sign-in form [1]. MUJ's IT page adds institutional context by naming Business ERP and student life cycle via web portal [14]. No public official deployment guide, procurement notice, faculty handbook, ERP module catalog, payroll manual, or data dictionary was found that maps `mujerp` to specific business processes.

The third-party ecosystem is more descriptive but less authoritative. betterSLCM claims attendance details and enhancements [5]. A GitHub project claims to fetch grades, GPA/CGPA, timetable, and attendance from SLCM [18]. MUJStella explicitly disclaims affiliation with MUJ [3]. These sources are valuable for understanding what students believe or build around the portal, but they do not certify production behavior, authorization, security, or institutional approval.

| Source | Public claim | Reliability for MUJ system scope |
|---|---|---|
| MUJ SLCM FAQ | Credentials, registration, support, personal-detail workflow [7] | High |
| MUJ first-year guide | Academic purpose and onboarding data [13] | High |
| MUJ IT page | Business ERP and student portal categories [14] | High for institutional context |
| `mujerp` page | Business Central branding and login [1] | High for observed page identity |
| MUJ Finance page | Payroll and finance responsibilities [17] | High for institutional function |
| betterSLCM | Attendance feature claims [5] | Medium/low for current production scope |
| GitHub SLCM app | Attendance, grades, GPA/CGPA, timetable claims [18] | Medium/low; not official |
| MUJStella | Student platform, explicit non-affiliation [3] | Useful for source-status context, not official confirmation |

The decision is to use primary MUJ material for conclusions and third-party material only as corroborative leads.

## Risk-Relevant Interpretation for a University Security Club

The publicly documented SLCM onboarding data includes identity, date of birth, contact details, academic program, educational qualifications, parent information, government or identity documents, photographs, and admission records [13]. That is a sensitive-data profile even though no protected record was observed. The public ERP page does not reveal its data categories, but Business Central is a business-management product with finance and operations capabilities at the generic product level [9][16].

The main OSINT risk is not that the login pages prove a vulnerability. It is that public naming and ecosystem references can encourage conflation: students may assume SLCM, HR, and Business Central are one system; analysts may assume a route name means a readable endpoint; and generic Microsoft documentation may be mistaken for MUJ's enabled modules. The evidence supports none of those shortcuts.

A defensible club briefing should present three boundaries. First, the public SLCM surface identifies student and parent access but shows no records without authentication [4][15]. Second, the official guide demonstrates that SLCM is important to academic onboarding and handles sensitive information [13]. Third, `mujerp` is visibly Business Central but has no public module or audience documentation [1].

Recommended club outputs should be non-invasive: a source register, a system-relationship diagram with confidence labels, a data-category matrix, and a responsible-disclosure checklist. The club should not collect credentials, install unknown third-party clients, attempt password resets, replay requests, bypass login, test authorization boundaries, or use public references to access data. Any technical validation should be performed only in a written, authorized test environment.

## exact_tables

| Exact URL | Public role in this report | Key evidence |
|---|---|---|
| `https://mujerp.jaipur.manipal.edu/MUJWEB/` | MUJ ERP public landing page | Dynamics 365 Business Central title; user-name and password fields [1] |
| `https://mujerp.jaipur.manipal.edu/MUJWEB/SignIn` | Publicly indexed ERP sign-in route | Search result identifies Business Central sign-in page |
| `https://mujslcm.jaipur.manipal.edu/` | MUJ SLCM public landing page | MUJ portal branding; Sign In and Parent Login [4] |
| `https://mujslcm.jaipur.manipal.edu/Student/Academic/AttendanceSummaryForStudent` | Publicly indexed attendance route | Retrieved response was a generic login wall, not attendance data [15] |
| `https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf` | Official SLCM FAQ | Registration link, credential convention, support, academic and personal-detail workflows [7] |
| `http://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf` | Official onboarding guide | Academic purpose, identity/admission fields, parent OTP, document uploads [13] |
| `https://www.jaipur.manipal.edu/administration-it.php` | Official MUJ IT context | ERP, Microsoft Business ERP, student life-cycle web portal, IT security responsibility [14] |
| `https://www.jaipur.manipal.edu/administration-finance.php` | Official Finance context | Payroll services for faculty and staff; finance responsibilities [17] |
| `https://jaipur.manipal.edu/human-resource.php` | Official HR context | Employee lifecycle, compensation, benefits, and leave management [19] |
| `https://mujone.jaipur.manipal.edu/HR/Login.aspx` | Separate MUJ HR login | Email, employee code, date of birth, captcha, policy controls [6] |
| `https://www.microsoft.com/en-us/dynamics-365/products/business-central` | Generic product context | Business Central ERP, finance, operations, dashboards, reports [9] |
| `https://learn.microsoft.com/en-us/dynamics365/business-central/finance` | Generic finance product context | Accounting, reporting, payables, receivables, payroll transaction imports [16] |
| `https://slcm.vercel.app/guides/check-attendance-muj` | Third-party SLCM lead | Attendance display and betterSLCM claims [5] |
| `https://github.com/DK10WS/SLCM_APP` | Third-party public project | Claims attendance, grades, GPA/CGPA, timetable; not identified as official [18] |
| `https://mujstella.in/` | Independent student platform | Explicitly says not affiliated with MUJ [3] |

The table is the report's exact URL index. It deliberately separates official evidence from third-party claims and generic product documentation.

## VERDICT

**Confidence level: Moderate to high for the public-facing identity and SLCM purpose; low to moderate for the specific `mujerp` audience, modules, data stores, and infrastructure mapping.**

The strongest supported conclusion is that `mujerp.jaipur.manipal.edu` publicly presents a Microsoft Dynamics 365 Business Central sign-in surface [1], and MUJ officially describes Microsoft Business ERP as part of its IT landscape while describing the student life cycle through a web portal [14]. It is therefore reasonable to classify `mujerp` as a probable institutional business-ERP surface. It is not reasonable to state as fact that it is staff/faculty-only, that it contains payroll, or that it stores attendance or academic records.

SLCM is better documented. MUJ publicly identifies it as an academic-information platform and official onboarding material describes identity, admission, educational, parent, contact, and document data [13]. Public third-party sources additionally claim attendance, grades, GPA/CGPA, and timetable features [5][18]. The attendance route retrieved only a login wall [15], so no public record exposure was observed.

Payroll is confirmed as an MUJ institutional function because Finance states that it provides payroll services to faculty and staff [17]. The technical placement of payroll is unknown. The separate HR login and official HR pages reinforce system separation but do not map payroll to `mujerp` [6][19].

Finally, the supplied claims about Azure `20.244.0.229`, ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 identity should remain **unconfirmed OSINT inputs**. The reviewed public sources support only narrower statements: Business Central branding on `mujerp`, Microsoft Business ERP in MUJ's IT description, and an Outlook-related account workflow for SLCM [1][14][7]. Any stronger technology or hosting assertion would exceed the evidence.

## References

1. *Welcome to Dynamics 365 Business Central.*. https://mujerp.jaipur.manipal.edu/MUJWEB/
2. *Manipal University Jaipur - 71 years of legacy of Manipal Education*. http://jaipur.manipal.edu/
3. *MUJStella - Student Platform for Manipal University Jaipur*. https://mujstella.in/
4. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
5. *How to Check Your Attendance at MUJ | mujslcm Guide*. https://slcm.vercel.app/guides/check-attendance-muj
6. [
	MUJ HR SYSTEM
](https://mujone.jaipur.manipal.edu/HR/Login.aspx)
7. *Frequently Asked Questions and Contacts for SLCM Registration*. https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf
8. *Academics rules & regulation - Manipal University Jaipur *. https://www.jaipur.manipal.edu/academic-rules-regulations.php
9. *Business Central | Microsoft Dynamics 365*. https://www.microsoft.com/en-us/dynamics-365/products/business-central
10. *Head, Human Resources - Manipal University Jaipur*. https://www.jaipur.manipal.edu/administration-hr.php
11. *Examination - Manipal University Jaipur *. https://www.jaipur.manipal.edu/examination.php
12. *SLCM Mobile*. https://slcm-client-unoff.vercel.app/
13. *Manipal University Jaipur First-Year Student Profile Registration Guide*. http://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf
14. *Head- Digital Infrastructure & Technology Services - Manipal University Jaipur*. https://www.jaipur.manipal.edu/administration-it.php
15. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Student/Academic/AttendanceSummaryForStudent
16. *Financial management (contains video) - Business Central | Microsoft Learn*. https://learn.microsoft.com/en-us/dynamics365/business-central/finance
17. *Finance Manipal University Jaipur*. https://www.jaipur.manipal.edu/administration-finance.php
18. *GitHub - DK10WS/SLCM_APP: App Version for MUJ SLCM · GitHub*. http://github.com/DK10WS/SLCM_APP
19. *Human Resource - Manipal University Jaipur*. https://jaipur.manipal.edu/human-resource.php
