# What MUJ's ERP Host Reveals About SLCM Boundaries

## Executive Summary

This investigation is now sufficiently developed for a defensible public-information report. The strongest finding is direct and narrow: the path `http://mujerp.jaipur.manipal.edu/MUJWEB/` publicly identifies itself as "Welcome to Dynamics 365 Business Central" and presents a Business Central-style username/password sign-in form. The raw page also uses the `/MUJWEB/SignIn` form action and Microsoft navigation classes. [3] [3] This is high-confidence evidence that the MUJ ERP-labeled host exposes a Microsoft Dynamics 365 Business Central web front end. It is not, by itself, evidence that the host is the MUJ student SLCM system, that it is staff-only, or that it exchanges data with SLCM.

Microsoft describes Dynamics 365 Business Central as enterprise resource planning software and says that it connects and automates core processes such as finance, procurement, manufacturing, and supply chain. [5] [5] [5] [5] [5] The MUJ IT department's own public description is consistent with an institution-wide business-systems role: it says Digital Infrastructure and Technology Services develops, maintains, supports, and optimises ERP, LMS, network and server infrastructure, backup, telecommunications, and IT security. It also states that the MUJ IT landscape includes Microsoft services for communication and Business ERP, a student life-cycle web portal, an LMS, and a research management system. [11] [11] This supports the interpretation that MUJ operates multiple adjacent platforms, rather than one public application serving every academic and administrative purpose.

The SLCM evidence points in a different direction. MUJ's official first-year guide calls the Student Life Cycle Management portal a one-stop platform for accessing academic information throughout a student's time at the university. [1] The guide documents student onboarding, admission-derived profile fields, education and address information, parent or guardian OTP verification, parent login enablement, PDF document uploads, declarations, and helpdesk or admissions support. [1] [1] [1] [1] [1] [1] [1] [1] The public SLCM landing page separately displays "WELCOME TO MUJ PORTAL," the `@muj.manipal.edu` identity label, and Parent Login. [4] The official FAQ gives the SLCM URL, a username pattern based on name and registration number, and password guidance referring to the official Outlook ID. [2]

The public record therefore supports a boundary model: `mujerp.jaipur.manipal.edu/MUJWEB/` is an ERP login surface, while `mujslcm.jaipur.manipal.edu/` is the student-life-cycle portal. MUJ's public IT description places both ERP and student life-cycle services within the broader IT landscape, but it does not publish a data-flow diagram, API contract, SSO trust relationship, synchronization schedule, or field mapping between them. [11] The safe conclusion is adjacency, not integration.

The staff-use question has a qualified answer. MUJ publicly lists IT and systems personnel and publicly describes finance functions including student fee collections, fee receipts, scholarships, refunds, vendor payments, payroll, accounting, reporting, MIS, budgets, audits, and statutory compliance. [7] [7] [7] MUJ also exposes a separate page labeled MUJ HR SYSTEM with employee-code and date-of-birth reset fields and a PAS Portal link. [6] These facts make staff-facing administrative workflows plausible. They do not prove that named staff use the Business Central host, that the host is the finance system, or that staff use it for SLCM-adjacent actions such as marks, attendance, registration approval, or parent-account administration.

- **Host Identity**: The MUJ ERP path is publicly labeled Dynamics 365 Business Central and exposes a username/password form. [3] -> Treat it as an ERP login surface, not as proof that it is SLCM.
- **System Separation**: MUJ's official guide assigns academic-information onboarding to SLCM, while the IT page separately names ERP, student life-cycle web services, LMS, and research management. [1] [11] -> Maintain separate application identities in the club's asset inventory.
- **Identity Boundary**: SLCM guidance refers to an official Outlook ID and the portal displays `@muj.manipal.edu`; Business Central can support different credential models depending on deployment. [2] [4] [14] -> Do not infer shared Microsoft 365 SSO without tenant or configuration evidence.
- **Staff Workflow**: MUJ documents finance, payroll, accounting, IT, and HR functions, but no public source names a staff member using mujerp. [7] [11] [6] -> Classify staff use of the host as plausible but unconfirmed.
- **Integration Limit**: Searches found no public API, data-flow, SSO, synchronization, or field-mapping documentation linking ERP and SLCM. -> Report "not publicly documented," not "does not exist."
- **Fingerprint Caution**: The Business Central page gives direct product evidence; the supplied ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, Azure Central India, and CT-date statements were not independently confirmed by the retrieved public evidence. -> Keep them in a separate unverified-observations table.
- **Defensive Exposure**: A public login page reveals service identity and an authentication surface, but no vulnerability follows from that fact. -> Limit club work to passive review and authorized testing.

## Scope, Method, and Evidence Rules

The research used public web pages, official MUJ pages and PDFs, publicly indexed login surfaces, Microsoft documentation, DNS-over-HTTPS output, and a read-only public people index for role context. The review did not attempt authentication, password recovery, endpoint enumeration, parameter manipulation, vulnerability exploitation, rate-limit testing, or access to non-public records. No credentials were requested or used.

The analysis separates three evidence classes:

| Evidence class | Meaning | Treatment in this report |
|---|---|---|
| Direct observation | A public page or document explicitly displays the fact | Report as verified and cite the page |
| Corroborating context | An official MUJ or Microsoft page describes a related platform or function | Use to interpret purpose, not to prove host-specific behavior |
| Inference or supplied premise | A reasoned interpretation or a fact supplied in the brief but not independently confirmed | Label explicitly and do not present as fact |

The public source base has an important limitation: login pages are intentionally sparse. A label such as Business Central identifies a product family, but does not disclose MUJ's modules, users, permissions, database, integrations, deployment mode, or internal governance. Similarly, SLCM's visible login page shows user roles and an email-domain label but does not reveal its backend configuration. [4] The absence of a public integration document is therefore evidence about public disclosure, not proof that no private integration exists.

## mujerp Host Purpose and Product Identity

The central public artifact is the MUJ ERP path `/MUJWEB/`. Its HTML title is "Welcome to Dynamics 365 Business Central." The page includes the Microsoft navigation-style `ms-nav` layout, a `Resources/desktop.css` stylesheet, a POST form to `/MUJWEB/SignIn`, and fields labeled User name and Password. [3] The indexed result also reports "Sign In" and a Microsoft copyright notice. [3]

Microsoft's product documentation supplies the meaning of the label. Business Central is described as a comprehensive business-management product and as enterprise resource planning software. Microsoft lists improvement of financial performance, sales and service, project success, and supply-chain management among its capabilities. [5] [5] Microsoft further explains that an ERP system connects and automates processes such as finance, procurement, manufacturing, and supply chain. [5]

The most supportable purpose statement is therefore: the public MUJ ERP endpoint appears to provide browser access to a Business Central deployment used or intended for institutional enterprise-resource functions. "Appears" is important because the public page does not identify the MUJ department owning the instance, the tenant, the company database, the enabled modules, or the authorized population of users.

| Question | Public finding | Confidence | Source |
|---|---|---:|---|
| Is the host publicly reachable? | Yes, the public extraction reached a login page at the MUJ ERP hostname and `/MUJWEB/` path. | High | `http://mujerp.jaipur.manipal.edu/MUJWEB/` [3] |
| What product does the page name? | Dynamics 365 Business Central. | High | Same page [3] |
| What authentication fields are visible? | User name, Password, and Sign In. | High | Same page [3] |
| Is it an ERP product? | Microsoft describes Business Central as ERP. | High | Microsoft product page [5] |
| Is it proven to be the SLCM application? | No. The public evidence identifies two separate hostnames and separate page labels. | High for separation, not proof of no integration | SLCM page [4]; ERP page [3] |
| Is it proven staff-only? | No public page retrieved states the allowed user population. | Low | ERP page [3] |

## Login, Identity, and User Roles

The ERP page exposes a local-looking username/password form. The form's public markup labels the fields User name and Password, uses an anti-double-submit behavior on the Sign In button, and posts to `/MUJWEB/SignIn`. [3] These observations describe the visible interface only. They do not establish whether the credentials are local Business Central credentials, Windows credentials, Microsoft Entra credentials, a reverse-proxy login, or a custom identity bridge.

Microsoft's Business Central documentation explains why that distinction matters. For Business Central online, users are added through the Microsoft 365 admin center and can then be imported into Business Central. [14] For on-premises deployments, Microsoft documents several credential types, including Windows, username/password, NavUserPassword, and AccessControlService. [14] [14] The AccessControlService option relies on Microsoft Entra ID, while the username/password option prompts users for credentials that are validated against Windows authentication. [14] Consequently, a username/password form alone cannot identify the underlying identity architecture.

SLCM presents a separate public identity model. The SLCM page displays `@muj.manipal.edu`, Parent Login, and the MUJ Portal label. [4] The official FAQ gives the SLCM registration link and says the password is "as per official outlook ID." [2] The first-year guide says that SLCM credentials are sent to the personal Gmail address supplied during admission by the Department of Admissions. [1] These statements concern student onboarding and do not prove that the ERP uses the same credentials or tenant.

| Platform | Visible public login evidence | Publicly documented user categories | What remains unknown |
|---|---|---|---|
| MUJ ERP / MUJWEB | User name, Password, Sign In; Business Central title. [3] | None stated on the page. | Staff scope, modules, tenant, SSO, MFA, role model, and authorization boundaries. |
| MUJ SLCM | MUJ Portal, `@muj.manipal.edu`, Parent Login, Student Login. [4] | Student and parent entry points are visible. [4] | Staff role implementation, Microsoft tenant linkage, MFA, backend framework, and ERP integration. |
| MUJ HR System | Employee Code, Date of Birth, captcha, password reset, policy acknowledgement, PAS Portal link. [6] | Employee-oriented reset fields are visible. [6] | Relationship to ERP, SLCM, Microsoft 365, and PAS implementation. |

## Technology, Hosting, and Passive Fingerprints

The direct ERP fingerprint is stronger than the direct SLCM fingerprint. The ERP page title, `ms-nav` CSS naming, `/MUJWEB/` route, and Microsoft copyright are all consistent with Business Central. [3] This is product-level evidence, not a complete server-stack fingerprint.

The extracted SLCM markup visibly includes a page title of Manipal University, a Keen theme login stylesheet, and JavaScript that writes `@muj.manipal.edu` into the page. [15] [15] An archived public index also shows SLCM HTML and Keen theme assets at historical URLs. [16] These observations support a conventional web portal and show that static assets were publicly retrievable. They do not independently prove ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, or any particular server patch level.

The research also queried public searches for Akamai, framework, IP ownership, and CT evidence. The searches did not return an authoritative page that independently confirmed Akamai in front of either relevant host, did not produce a usable CT result for the exact ERP hostname, and did not yield an authoritative ownership record for the supplied IP. DNS-over-HTTPS did return an A record mapping `mujerp.jaipur.manipal.edu` to `20.244.0.229`, with status 0 and a TTL of 3600 at retrieval. [10] That confirms the observed DNS answer, but not the cloud region, subscription owner, workload, or geographic location.

Microsoft's public Azure IP-ranges page says its file contains ranges for Public Azure as a whole, Azure regions, and several Azure services. [13] That general description cannot, without matching the exact published range data and allocation context, establish that one particular address is in Central India or that MUJ controls it. The brief's Azure Central India and CT-since-April-2025 statements should therefore be retained as supplied leads, not as independently verified report findings.

| Technical or infrastructure claim | Status after public review | Safe wording |
|---|---|---|
| ERP product is Business Central | Verified | The public `/MUJWEB/` page identifies itself as Dynamics 365 Business Central. [3] |
| ERP form uses username and password | Verified | The public page displays User name and Password fields. [3] |
| SLCM uses a Keen theme asset | Directly observed in public markup | The retrieved SLCM markup references Keen login assets. [15] |
| SLCM is ASP.NET MVC 5.3 on .NET Framework 4.x and IIS 10 | Not independently verified in retrieved sources | Treat as an unverified supplied fingerprint. |
| Akamai fronts SLCM or ERP | Not independently verified | Do not state as fact. |
| ERP resolves to 20.244.0.229 | Verified for the retrieved DNS response | DNS-over-HTTPS returned that A record. [10] |
| 20.244.0.229 is Azure Central India | Not established by the retrieved sources | Treat as an unverified supplied attribution. |
| ERP certificate transparency began in April 2025 | Not established by the retrieved CT result | Treat as an unverified supplied date. |

## Public MUJ Documentation and Adjacent Workflows

MUJ's official IT page provides the most useful institutional context. It names the Head of Digital Infrastructure and Technology Services and says the function supports teaching, research, administration, faculty, staff, and students. [11] It specifically names ERP, LMS, network infrastructure, server infrastructure, data communications, backup strategies, telecommunications, and IT security. [11] It also says the MUJ IT landscape includes Microsoft services for communication and Business ERP, a student life-cycle web portal, an LMS, and a research management system. [11]

This is a significant corroborating source because it connects the words ERP and student life cycle to the same institutional IT landscape while keeping them as distinct service descriptions. It does not say that Business Central is the database of SLCM or that SLCM is a Business Central module. The correct interpretation is an institutional platform inventory, not an integration specification.

The SLCM guide provides direct evidence of academic and student-administration workflows. It calls SLCM the one-stop academic-information portal. [1] It says admission supplies non-editable fields such as registration number, student name, academic year, program or branch, date of joining, date of birth, gender, mobile number, program duration, email, and year of admission. [1] It requires chronological educational qualifications, permanent and present addresses, and parent or guardian contact information. [1] [1] Parent access is enabled after OTP verification of the parent's mobile number. [1] Mandatory red-marked documents must be uploaded as PDF files of no more than 1 MB. [1] Declarations are opened through linked policy pages and must be completed before submission. [1]

The FAQ adds operational support boundaries. It gives the SLCM URL, username pattern, Outlook-ID password guidance, and university helpline. [2] It routes AMS login issues to DMS or AMS contacts and Outlook-account problems to Team IT Infra. [2] It separately lists admissions, DMS, academic, and chief-warden contacts. [2] It says admission-originated details can only be changed by the admissions department after verification. [2]

MUJ's Finance page documents functions that are strongly ERP-adjacent: student fee collections, fee receipts, scholarships, refunds, vendor payments, payroll for faculty and staff, financial accounting and reporting, periodical MIS, annual budgets, audits, tax matters, and account consolidation. [7] [7] [7] However, it does not name mujerp or Business Central as the application implementing those functions. The public MUJ HR page is also separate, labeled MUJ HR SYSTEM, with employee-code and date-of-birth fields, password reset, policy acknowledgement, and a PAS Portal link. [6]

| Workflow domain | Publicly documented MUJ function | Directly tied to mujerp? | Directly tied to SLCM? |
|---|---|---:|---:|
| Student onboarding | Profile, education, address, parent OTP, documents, declarations. [1] [1] [1] | No | Yes |
| Student identity support | SLCM URL, username pattern, Outlook-ID password guidance. [2] | No | Yes |
| Academic-information access | SLCM is described as a one-stop academic-information portal. [1] | No | Yes |
| Student finance | Fee collections, fee receipts, scholarships, refunds. [7] | No | Not established by the cited guide/FAQ |
| Institutional finance | Vendor payments, payroll, accounting, MIS, budgets, audits. [7] | No | No |
| HR | Employee-code/date-of-birth reset, policy acknowledgement, PAS Portal link. [6] | No | No |
| IT governance | ERP, LMS, infrastructure, backup, telecommunications, IT security. [11] | Context only | Context only |

## Integrations and Staff Use Assessment

The positive integration evidence is organizational rather than technical. MUJ's IT page says the IT landscape includes Microsoft communication services, Business ERP, a student-life-cycle web portal, LMS, and research management system. [11] The Finance page describes student financial services and institutional accounting. [7] The SLCM guide describes student academic-information and onboarding workflows. [1] [1] Together, these sources make it reasonable to model MUJ as a multi-system environment in which identity, student records, finance, HR, and academic operations may be related at the business-process level.

That reasoning is an inference, not a public integration finding. The sources do not disclose whether SLCM sends fee status to Business Central, whether Business Central sends student identifiers to SLCM, whether finance staff approve SLCM records, or whether the two applications share an identity provider. No retrieved public source exposes an API endpoint, webhook, integration guide, data dictionary, SSO metadata, Microsoft Entra application registration, or synchronization schedule for the pair.

The staff-use question is similarly bounded. MUJ publicly describes a technology function that works with faculty, staff, and students and maintains ERP and other systems. [11] Public role data also included people associated with MUJ whose titles include Information Technology Specialist, Systems Executive, System Executive, Junior System Engineer, and IT Administration and Network support. Those records establish public role context, but the result itself explicitly provided no proof that any named person uses the specific ERP host. The Finance page establishes that staff-facing finance and payroll functions exist. [7] The HR page establishes a separate employee-oriented system. [6]

| Staff-use proposition | Assessment | Reason |
|---|---|---|
| MUJ has staff responsible for technology and systems | Supported | Official IT page names the function and responsibilities. [11] |
| MUJ has staff-facing finance and payroll workflows | Supported | Official Finance page explicitly names payroll, vendor payments, accounting, reporting, and audits. [7] |
| mujerp is used by staff | Plausible, not proven | It is labeled ERP, but the login page states no user population. [3] |
| mujerp is the finance system | Not publicly proven | Finance functions are documented, but no cited Finance page names mujerp or Business Central. [7] |
| Staff use mujerp for SLCM-adjacent functions | Unconfirmed | No public workflow, user guide, role page, API, or named-user evidence ties the host to SLCM operations. |
| ERP and SLCM exchange data | Not publicly documented | Institutional co-existence is documented; technical linkage is not. [11] |
| ERP and SLCM share Microsoft 365 identity | Not publicly proven | SLCM references Outlook ID, while Business Central supports multiple credential modes. [2] [14] |

## Security-Club Research Boundaries and Defensive Actions

The public evidence reveals login surfaces and product names, but it does not establish a vulnerability. A security club should not submit credentials, test password-reset behavior, enumerate hidden routes, inspect authenticated responses, or attempt to bypass controls without written authorization from MUJ and the system owner.

A safe next phase is a governance-oriented evidence request. Ask the authorized owner to confirm the canonical asset list, business owner, data classification, identity provider, MFA status, retention requirements, logging coverage, vendor support boundary, and approved testing window. Request architecture documentation through proper channels rather than attempting to infer it from public behavior.

For a defensive review, the owner can validate whether public login pages disclose unnecessary product details, whether authentication errors are generic, whether MFA is enforced for staff, whether legacy credential modes are disabled, whether administrative roles are separated, whether logs capture sign-ins and privileged changes, whether service accounts are inventoried, and whether ERP-to-SLCM transfers are authenticated, minimized, monitored, and reconciled. These are recommendations, not claims about MUJ's current controls.

| Safe activity | Permitted basis | Stop condition |
|---|---|---|
| Passive documentation review | Public pages and official documents | Stop when evidence would require authentication or probing |
| Asset and ownership inventory | Written institutional authorization | Do not infer ownership from hostname alone |
| Architecture review | Owner-provided diagrams and configuration summaries | Do not request secrets or tokens |
| Authenticated testing | Explicit scope, test accounts, dates, rate limits, and contacts | Stop outside scope or on production impact |
| Integration review | Owner-provided API and data-flow documentation | Do not discover endpoints by unauthorized enumeration |

## Synthesis

The public evidence distinguishes four layers. First, the public MUJ website is an institutional information surface containing academic, admissions, and service labels, but the retrieved home-page evidence does not explicitly name ERP, SLCM, HR, or a staff portal. [8] [8] Second, SLCM is a student-life-cycle service with student and parent entry points and detailed onboarding documentation. [4] [1] Third, the MUJ HR page is an employee-oriented service with reset and policy fields. [6] Fourth, mujerp is a Business Central ERP login surface with no public role labels. [3]

| Dimension | MUJ ERP / MUJWEB | MUJ SLCM | MUJ HR System | MUJ public website |
|---|---|---|---|---|
| Primary public label | Dynamics 365 Business Central. [3] | MUJ Portal / Student Life Cycle Management. [4] [1] | MUJ HR SYSTEM. [6] | Manipal University Jaipur institutional site. [8] |
| Visible audience | Not stated. [3] | Student and parent entry points. [4] | Employee-oriented reset fields. [6] | Public visitors and applicants. [8] |
| Main documented purpose | ERP/business management context. [5] | Academic-information access and onboarding. [1] | HR account and policy workflow. [6] | Public university information and services. [8] |
| Identity evidence | Username/password form; underlying mode unknown. [3] [14] | `@muj.manipal.edu`; Outlook-ID guidance; parent login. [4] [2] | Employee Code, Date of Birth, captcha. [6] | No ERP/SLCM/HR identity label in retrieved home-page evidence. [8] |
| Integration evidence | No public SLCM data flow found. | No public ERP data flow found. | No public ERP/SLCM link found. | Links and labels do not establish backend integration. |
| Confidence on purpose | High | High | High on page identity, lower on backend role | High as public site, low for internal systems |

The key tension is that MUJ publicly groups ERP and student-life-cycle services within one IT landscape while exposing them through different product surfaces and hostnames. [11] That is exactly what a mature institutional environment might look like, but it is not a substitute for a technical integration record. A second tension is identity: SLCM documentation references Outlook credentials, whereas Business Central can be configured for Microsoft 365, Windows, or Business Central-managed credentials depending on deployment. [2] [14] Similar-looking Microsoft identity language therefore cannot prove a shared trust relationship.

## VERDICT

**Overall confidence: High for the ERP product identification and SLCM purpose; Moderate for the institutional adjacency model; Low for the exact integration and staff-use claims.**

1. **Purpose:** High confidence that the public MUJ ERP-labeled endpoint exposes a Dynamics 365 Business Central login. [3]
2. **Technology:** High confidence in the Business Central product fingerprint; low-to-moderate confidence in any deeper server-stack claim not directly shown in the retrieved public material. The supplied ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, and Akamai assertions remain unverified here.
3. **Login:** High confidence that the ERP page visibly requests a username and password. [3] Low confidence about the underlying identity provider or SSO configuration. Microsoft documents multiple possible Business Central credential models. [14]
4. **Public documentation:** High confidence that official MUJ materials document SLCM onboarding, academic-information access, parent login, Outlook-related support, finance functions, IT responsibilities, and a separate HR system. [1] [1] [1] [2] [7] [11] [6]
5. **Integrations:** No public evidence retrieved proves ERP-SLCM APIs, data exchange, field mappings, synchronization, or shared SSO. This should be reported as **not publicly documented**, not as evidence that integration is absent.
6. **Staff use:** It is reasonable to infer that MUJ staff and administrative teams operate institutional systems because MUJ documents staff-facing IT, finance, payroll, and HR functions. [11] [7] [6] However, it is **not publicly proven** that staff use `mujerp.jaipur.manipal.edu` for SLCM-adjacent functions.

The decision-ready conclusion is: **treat mujerp as a distinct Business Central ERP asset that is institutionally adjacent to, but not publicly demonstrated to be integrated with, MUJ SLCM. Treat staff use for SLCM-adjacent workflows as plausible but unconfirmed. Any stronger conclusion requires authorized owner-provided documentation or an explicitly approved assessment.**

## References

1. *http://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf*. http://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf
2. *http://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf*. http://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf
3. *Welcome to Dynamics 365 Business Central.*. https://mujerp.jaipur.manipal.edu/MUJWEB/
4. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
5. *Business Central | Microsoft Dynamics 365*. https://www.microsoft.com/en-us/dynamics-365/products/business-central
6. [
	MUJ HR SYSTEM
](https://mujone.jaipur.manipal.edu/HR/)
7. *Finance Manipal University Jaipur*. https://jaipur.manipal.edu/administration-finance.php
8. *Manipal University Jaipur - 71 years of legacy of Manipal Education*. https://jaipur.manipal.edu/
9. [
	MUJ HR SYSTEM
](https://mujone.jaipur.manipal.edu/HR/Login.aspx)
10. *dns.google*. https://dns.google/resolve?name=mujerp.jaipur.manipal.edu&type=A
11. *Head- Digital Infrastructure & Technology Services - Manipal University Jaipur*. https://www.jaipur.manipal.edu/administration-it.php
12. *Information Security Policy*. https://www.manipal.edu/mu/policies/it-policy/information-security-policy.html
13. *Download Azure IP Ranges and Service Tags – Public Cloud from Official Microsoft Download Center*. https://www.microsoft.com/en-us/download/details.aspx?id=56519
14. *Authentication and credential types - Business Central | Microsoft Learn*. https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/administration/users-credential-types
15. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
16. *web.archive.org*. http://web.archive.org/cdx/search/cdx?collapse=urlkey&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&output=json&url=mujslcm.jaipur.manipal.edu/*
