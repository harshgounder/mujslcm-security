# MUJ SLCM and DMS: Public Surface and Operations Report

## Executive Summary

This report examines only publicly available material concerning Manipal University Jaipur's Student Life Cycle Management ecosystem and the DMS-related hostnames `dms.jaipur.manipal.edu` and `dmsmuj.jaipur.manipal.edu`. It does not attempt authentication, password testing, endpoint enumeration, exploitation, or access to non-public records. The evidence supports a cautious conclusion: MUJ publicly documents SLCM as its student-facing academic-information platform, and its official FAQ routes unresolved AMS login problems to `dms@jaipur.manipal.edu` and `ams@jaipur.manipal.edu`. That is strong evidence that the DMS mailbox participates in AMS/SLCM support. It is not, by itself, proof that DMS is a formally named department, that DMS expands to a particular phrase, or that the DMS web host is the production SLCM backend.

- **SLCM Function**: MUJ describes SLcM as a one-stop platform for academic information throughout a student's time at the university -> treat `mujslcm.jaipur.manipal.edu` as the primary documented student portal, not as evidence of the internal architecture. [8]
- **DMS Operational Link**: The official FAQ directs students with unresolved AMS login problems to `dms@jaipur.manipal.edu` or `ams@jaipur.manipal.edu` -> treat DMS as an operational support contact with high confidence, but do not rename it from an acronym without official confirmation. [10]
- **Public DMS Surface**: The current central `dms.manipal.edu` page presents a Document Management System sign-in shell, displays `@manipal.edu`, and includes a captcha -> this is a real public login surface, but its central-domain scope is not proof that it is the MUJ AMS/SLCM service. [21]
- **Historical MUJ DMS Surface**: Internet Archive records show repeated successful root-page captures for `dms.jaipur.manipal.edu` from 2018 through 2022, including a 2018 IIS Windows Server page and 2022 captcha-related records -> the hostname had public historical web presence, while its current status remains unconfirmed. [25][181.0][213.0]
- **DMSMUJ History**: `dmsmuj.jaipur.manipal.edu` has a 2022 archived root returning the text `MUJ API TESTING!` and a separate archived `loginForm.aspx` capture -> this suggests testing or transitional infrastructure, but the purpose and relationship to production SLCM are not established. [14][215.0]
- **Certificate History**: Public CT data lists DMS names together with other MUJ names, including `mujslcm.jaipur.manipal.edu` in certificate name fields -> this demonstrates certificate association, not live DNS, hosting, ownership of a service, or data flow.
- **SLCM Technology Evidence**: A public urlscan record dated 2026-06-16 reports HTTPS redirection, HTTP 200, `Microsoft-IIS/10.0`, IP `98.70.14.50`, and AS8075 Microsoft Corporation -> this supports the supplied IIS/Azure-associated observations, but does not establish ASP.NET MVC 5.3, .NET Framework 4.x, or an Akamai layer. [26]
- **Identity Boundary**: The FAQ says the SLCM password is according to the official Outlook ID, while a separate June 2025 MUJ IT SOP documents Office 365 mail and mandatory MFA; the SOP itself does not mention SLCM or AMS -> report an identity relationship as documented operational coupling, not as confirmed Microsoft 365 SSO architecture. [10][201.6][201.31]
- **Negative Finding**: Public urlscan searches returned zero records for both DMS Jaipur hostnames -> this is a statement about urlscan's public dataset, not proof that either hostname is offline or absent. [16][197.0]
- **Security Implication**: The public evidence exposes login branding, role labels, historical route names, certificate associations, and support contacts, but no authenticated content or verified vulnerability -> club work should remain passive and defensive, using disclosure channels rather than testing accounts or protected routes.

## Scope, Method, and Evidence Standard

The research question contains four distinct issues: what SLCM publicly exposes; what DMS-related surfaces are visible; what archive and CT history says about the hostnames; and what can be responsibly inferred about operational ownership. The evidence set includes official MUJ pages and PDFs, Internet Archive CDX and snapshots, Certificate Transparency search output, and public urlscan records. Search-result noise was excluded where it concerned unrelated products such as Microsoft's Azure Database Migration Service or generic university pages.

A result is treated as direct evidence only when the source states the fact. An inference is marked as such when it connects separate observations. For example, the FAQ's routing of AMS problems to a DMS mailbox is direct evidence of support routing. Calling DMS the SLCM administrator, saying that it stands for Document Management System, or asserting that it owns the database would be inference. The public current page at `dms.manipal.edu` explicitly calls itself Document Management System, but that does not establish that `dms.jaipur.manipal.edu` has the same expansion or that both systems are operated identically. [21]

The report intentionally does not provide steps for bypassing login, testing credentials, discovering hidden routes, or interacting with protected systems. Archive reading, CT review, and passive scan metadata are sufficient for the research objective. A public login page should be treated as an access boundary, not as an invitation to test it.

## MUJ SLCM's Documented Role in Student Operations

MUJ's first-year registration guide gives the clearest public description of SLCM: the Student Life Cycle Management portal is a one-stop platform for accessing academic information throughout a student's time at the university. The guide directs students to `https://mujslcm.jaipur.manipal.edu`, identifies onboarding as a student-portal process, and says that credentials are sent to the personal Gmail address supplied during admission by the Department of Admissions. [8][150.18-24]

The workflow is broader than a simple login page. The same guide says students enter the Student Details section, correct inaccurate pre-filled details through Admissions, upload required documents in PDF format, and verify parent mobile numbers by OTP; successful OTP verification enables Parent login access. It also routes technical issues or queries to the University Helpdesk or Admissions. These statements establish the public-facing workflow and the division between onboarding data correction, technical support, and parent access. They do not identify the internal application services, database, middleware, or administrator roles. [8][150.80-87][150.140-143]

The current unauthenticated SLCM shell publicly displays `WELCOME TO MUJ PORTAL`, `Sign In`, a `@muj.manipal.edu` label, and `Sign In Parent Login`. A related alias displays the MUJ portal branding and a `@jaipur.manipal.edu` label in search and page evidence. This is useful for asset inventory and brand correlation, but login labels are presentation-layer evidence only. They cannot prove that the portal authenticates directly against Microsoft Entra ID, Exchange Online, an on-premises directory, or a custom identity service. [22][208.0]

| Public SLCM observation | Direct evidence | What it supports | What it does not prove |
|---|---|---|---|
| SLCM purpose | One-stop academic information platform | Student lifecycle and academic-information role | Internal modules or data stores |
| Primary URL | `mujslcm.jaipur.manipal.edu` | Official onboarding destination | Exclusive production hostname |
| Visible roles | Student sign-in and Parent login | At least two public user journeys | Authorization model or role permissions |
| Credential wording | Password according to official Outlook ID | Operational relationship to institutional mail identity | Confirmed SSO or token flow |
| Parent onboarding | OTP verification enables Parent login | Parent account activation workflow | OTP provider or backend design |

The practical insight is that SLCM should be modeled as a business-critical academic workflow, not merely as a login endpoint. The highest-confidence public risk questions concern account recovery, support routing, and separation of student, parent, admissions, and administrative roles. Those questions can be reviewed through governance and documentation without attempting unauthorized access.

## DMS-Related Public Surfaces and Their Boundaries

There are three materially different DMS references in the evidence and they must not be conflated. First, `dms.manipal.edu` is currently visible as a central-domain page titled `Document Management System`. It displays a logo, the Document Management System label, an `@manipal.edu` identity label, and captcha wording. The public page is a sign-in gate and exposes no authenticated document content in the retrieved material. [21]

Second, the MUJ-specific hostname `dms.jaipur.manipal.edu` has historical archive evidence. The earliest root records in the compact inventory begin in August 2018 and continue through repeated monthly captures, with a 2022 root capture also listed as HTTP 200 and `text/html`. Archived root snapshots from 2018 and 2022 were titled `IIS Windows Server` and showed the IIS link, rather than a documented DMS business interface. [25][181.0][182.0] The archive also contains 2022 records for `GenerateCaptcha.aspx`, including an image/jpeg response and several records represented as text/html by the archive inventory. This indicates that an authentication-related captcha route was publicly captured; it does not demonstrate a weakness or permit access. [20]

Third, `dmsmuj.jaipur.manipal.edu` has two especially informative historical records: a December 2022 root capture whose visible content was `MUJ API TESTING!`, and an August 2022 `loginForm.aspx` capture titled `MU SLcM`. The first is direct evidence of a public test string at that historical snapshot. The second shows a historical login-form route associated by the archive title with MU SLcM. Neither record proves that the host was production, that it handled documents, or that it remains online. [14][215.0]

| Host or surface | Evidence date or status | Publicly visible evidence | Confidence and limitation |
|---|---|---|---|
| `dms.manipal.edu` | Current fetch evidence | Document Management System; `@manipal.edu`; captcha; sign-in shell | High that a central DMS login page exists; low for MUJ SLCM linkage |
| `dms.jaipur.manipal.edu` | Archive records, 2018-2022 | IIS default root and captcha-related captures | High that historical public captures exist; current status unknown |
| `dmsmuj.jaipur.manipal.edu` | Archive records, 2022 | `MUJ API TESTING!`; `loginForm.aspx` titled MU SLcM | Medium for historical MUJ testing/login surface; production role unknown |
| `mujslcm.jaipur.manipal.edu` | Current and 2026 passive record | MUJ portal login shell; IIS 10 scan observation | High for public SLCM surface; internal architecture unknown |

The key analytical distinction is between a public surface and a confirmed operational dependency. A hostname can appear in certificates, archives, or a test page without currently serving the production application. Conversely, a support mailbox can be operationally important without exposing a public DMS web application. The available evidence supports both observations but does not collapse them into one architecture.

## Archive and Certificate Timeline

The archive record provides a historical timeline rather than a current asset-status report. The root of `dms.jaipur.manipal.edu` appears repeatedly from 2018 through 2022. The 2018 and 2022 snapshots show the generic IIS Windows Server page, while the 2022 captcha records show a route associated with login functionality. The archive query for `dmsmuj.jaipur.manipal.edu` shows two 2022 records: the root test page and the `loginForm.aspx` page. [25][213.0][215.0]

| Period | Host/route | Archive result | Responsible interpretation |
|---|---|---|---|
| 2018-08 to 2020-02 | `dms.jaipur.manipal.edu:80/` | Repeated HTTP 200 `text/html` root captures | Historical public web presence; no current-status conclusion |
| 2021-05 | `dms.jaipur.manipal.edu/` | HTTP 200 `text/html` root capture | Continued historical capture; content may still be default IIS |
| 2022-02 to 2022-03 | `dms.jaipur.manipal.edu/GenerateCaptcha.aspx` | Captured captcha-related responses | Historical authentication-related surface; not a vulnerability finding |
| 2022-08 | `dmsmuj.jaipur.manipal.edu/loginForm.aspx` | HTTP 200 `text/html` | Historical login-form route; production role unverified |
| 2022-12 | `dmsmuj.jaipur.manipal.edu/` | HTTP 200 `text/plain`, `MUJ API TESTING!` | Historical test or diagnostic content; not evidence of production API |
| 2022-04 | `dms.jaipur.manipal.edu/` | Wayback availability reported a 200 snapshot | Confirms an available historical capture, not present-day availability |

Certificate Transparency adds a second historical signal. The wildcard-style MUJ certificate search output includes `dms.jaipur.manipal.edu`, `www.dms.jaipur.manipal.edu`, `dmsmuj.jaipur.manipal.edu`, `muj.slcm.jaipur.manipal.edu`, and combinations that include `mujslcm.jaipur.manipal.edu`. These are certificate name fields. They show that the names were included in certificate issuance records; they do not prove that all names were simultaneously active, that they shared a server, or that they had a common application. [4][159.2][159.6]

The exact-host CT query for `dms.jaipur.manipal.edu` returned no matching names in the retrieved output, while the broader `%.jaipur.manipal.edu` query did show DMS-related names. That apparent difference is a query/output distinction, not a contradiction about history. The broader result is the stronger evidence for certificate association; the narrow result should not be used to claim certificate absence. [2][159.0][159.6]

## SLCM Hosting and Identity Evidence

The 2026-06-16 public urlscan API record for `mujslcm.jaipur.manipal.edu` reports a manual public scan of the HTTP URL that redirected to HTTPS and returned status 200. The page metadata identifies `Microsoft-IIS/10.0`, IP `98.70.14.50`, AS8075 with Microsoft Corporation naming, India as the page country, and an HTTPS URL. This is good passive evidence for the observed web edge at that time. [26]

It does not prove every technology in the supplied fingerprint. The retrieved public evidence does not directly establish ASP.NET MVC 5.3 or .NET Framework 4.x. It also does not establish Akamai: the observed IP and ASN are described in the urlscan record as Microsoft-associated, and no retrieved source provides an Akamai hostname, header, DNS chain, or edge identifier. An Akamai deployment could theoretically coexist with an origin or could have changed over time, but that is an inference and should not be presented as confirmed.

| Technology or architecture claim | Public evidence status | Confidence |
|---|---|---|
| IIS 10 at an observed SLCM scan | Explicit `Microsoft-IIS/10.0` in 2026-06-16 urlscan record | High for that observation |
| Microsoft-associated network metadata | IP `98.70.14.50` and AS8075 Microsoft naming | High for that observation |
| HTTPS enforcement | Urlscan says `redirected: https-only` | High for that observation |
| ASP.NET MVC 5.3 | Not established in the retrieved evidence | Low/unconfirmed |
| .NET Framework 4.x | Not established in the retrieved evidence | Low/unconfirmed |
| Akamai in front of SLCM | Not established in the retrieved evidence | Low/unconfirmed |
| Microsoft 365/Office 365 identity relationship | Operationally suggested by FAQ and SOP, but not an explicit SLCM SSO statement | Medium for relationship; low for SSO architecture |

The identity evidence has two parts. The official SLCM FAQ gives username guidance based on a name and registration number and says the password is according to the official Outlook ID. It separately directs unresolved Outlook-account problems to Team IT Infra at `it.support@jaipur.manipal.edu`, extension 144. [10][202.15-18] The official IT SOP is titled `How To Setup Your Office 365 Mail ID`, is version 1.0 effective June 2025, and is aimed at students and employees. It documents a Microsoft 365 welcome page and says MFA is mandatory. [18][201.10-11][201.31]

However, the SOP's extracted content explicitly does not mention SLCM or AMS. Therefore the defensible formulation is: MUJ's public documents connect SLCM credentials operationally to the official Outlook identity, and MUJ separately documents Office 365/MFA, but the evidence does not prove that SLCM uses Microsoft 365 as its direct authentication provider or that the portal is behind a particular federation flow. [18]

## DMS Role in SLCM Operations

The official FAQ is the strongest evidence for DMS's role. It asks what to do when a user cannot log in to AMS, instructs the user to re-check credentials, and then directs unresolved cases to `dms@jaipur.manipal.edu` or `ams@jaipur.manipal.edu`. It lists Rahul Kumawat, Dinesh Sain, and Rithik Chaudhary under AMS with extensions 784, 738, and 481 respectively. [10]

This supports a high-confidence operational statement: the DMS mailbox is one of the official escalation channels for AMS login problems. It also supports a medium-confidence statement that DMS is involved in the SLCM/AMS support ecosystem, because the FAQ is explicitly titled for SLCM registration and the question concerns AMS login. It does not support the stronger statement that DMS administers every SLCM component, owns the application, manages the identity directory, or controls the underlying database.

The same FAQ distinguishes other support paths. Outlook-account problems go to Team IT Infra, while missing mandatory documents go to Admissions at `admissions@jaipur.manipal.edu`, with extensions 142, 257, and 297. This separation is important: DMS, IT Infra, and Admissions are all in the operational perimeter, but they are not interchangeable. [10]

The Directorate of Academic Administration page adds organizational context but does not resolve the acronym. It says the Directorate facilitates academic programs, develops a student-centric academic environment, implements outcome-based teaching-learning practices, coordinates academic activities, and updates course curricula. The retrieved page names an AMS Office and includes `dms@jaipur.manipal.edu`, but it does not explicitly expand DMS or provide a detailed DMS service description. [6][200.92]

| Operational question | Best public answer | Confidence |
|---|---|---|
| Is DMS an AMS login escalation contact? | Yes, via `dms@jaipur.manipal.edu` | High |
| Is DMS connected to SLCM operations? | Yes, through the SLCM FAQ's AMS support route | Medium-high |
| Is DMS the entire SLCM admin team? | Not directly proven | Low-medium |
| Does DMS mean Document Management System at MUJ Jaipur? | Not officially expanded in the retrieved MUJ FAQ | Low |
| Does DMS mean Digital Media Services? | No public evidence found in the retrieved material | Very low |
| Does DMS own the SLCM application/database? | Not publicly established | Very low |

The most useful working model is therefore a support and administration graph rather than a single owner claim: Admissions supplies or corrects onboarding data; IT Infra supports Outlook and institutional access; AMS contacts handle the academic-management service; and DMS is an official escalation mailbox for AMS login failures. The graph is evidence-based at the contact-routing level and intentionally silent about backend ownership.

## Public Exposure and Defensive Priorities

The public exposure identified here is informational, not a confirmed vulnerability. It includes branded login shells, student and parent role labels, institutional email-domain labels, historical hostnames, archived login-related route names, a historical test string, certificate associations, and passive server metadata. Each item can help defenders build an inventory and review whether old names and archived records remain appropriately governed. None authorizes attempts to log in, test credentials, manipulate captcha requests, or access documents.

| Exposure category | Observed public evidence | Defensive governance question |
|---|---|---|
| Login branding | MUJ portal and central DMS sign-in shells | Are all public login pages documented and owned? |
| Role disclosure | Student and Parent login labels | Are role names and recovery processes reviewed for unnecessary disclosure? |
| Support contacts | DMS, AMS, IT Infra, and Admissions addresses | Are mailboxes monitored, protected, and covered by incident-response procedures? |
| Historical routes | `GenerateCaptcha.aspx`, `loginForm.aspx` | Are retired routes removed or formally accepted as legacy? |
| Test content | `MUJ API TESTING!` historical root | Was the test host decommissioned or isolated from production? |
| Certificate history | DMS and SLCM names in CT output | Is certificate issuance monitored for stale or unintended names? |
| Server metadata | IIS 10 and Microsoft-associated scan metadata | Is technology disclosure minimized and asset ownership current? |

The recommended club deliverable is a passive asset register with columns for hostname, evidence URL, observation date, source type, current-status confidence, owner, and approved reporting channel. A second deliverable should map public support routes to business functions and identify where official documentation is ambiguous. The club should report any suspected issue through MUJ's published security contact or helpdesk process, and should not use public metadata as a basis for intrusive validation.

## Evidence Gaps and Unanswered Questions

Several questions remain deliberately unanswered because public evidence does not support a reliable conclusion. First, the current status of `dms.jaipur.manipal.edu` is unresolved. A direct current extraction returned no citable page result, and urlscan's public API reports no records for the hostname. Those facts justify saying "not established by this research," not saying "offline." [16]

Second, the formal name of DMS is unresolved. The central host calls itself Document Management System, but the MUJ Jaipur FAQ only uses the email address and does not expand the acronym. The possibility that DMS means Digital Media Services is unsupported in the retrieved evidence and should remain a hypothesis, not a report finding. [10][203.1-4]

Third, the relationship between central `dms.manipal.edu`, Jaipur `dms.jaipur.manipal.edu`, and `dmsmuj.jaipur.manipal.edu` is unresolved. The domains share institutional naming and CT history, but public evidence does not establish common code, common tenancy, common identity, or data exchange. The historical `MUJ API TESTING!` string is especially weak evidence for production integration because test wording can represent a temporary environment. [14][159.6]

Fourth, the supplied ASP.NET MVC 5.3, .NET Framework 4.x, and Akamai assertions remain outside the confirmed evidence gathered here. IIS 10 is directly supported for the observed 2026 SLCM scan. The other stack elements should be marked "reported but not independently established from the cited public evidence" until a trustworthy public source documents them. [26]

Finally, the identity architecture remains only partly documented. The FAQ connects the password to the official Outlook ID, and the SOP documents Office 365 and mandatory MFA, but the SOP explicitly does not mention SLCM or AMS. No claim about direct Microsoft 365 federation, Entra ID token exchange, or shared session cookies should be made from these documents alone. [10][201.6][201.31]

## Synthesis

Across scope, mechanism, evidence base, and trade-offs, the ecosystem divides into four layers. SLCM is the documented student workflow layer: it presents student and parent journeys and handles academic-information onboarding. DMS is best supported as an operational escalation layer because the official FAQ routes AMS login failures to its mailbox. Central DMS is a visible document-management login surface, but its relationship to MUJ Jaipur remains unproven. Archive and CT sources are historical inventory layers, useful for continuity and decommissioning review but weak for current service claims.

The main tension is between strong operational evidence and weak architectural evidence. The FAQ gives a concrete support route, named AMS staff, and a direct relationship between an SLCM registration document and the DMS mailbox. Yet the same public record does not say that DMS owns the application, define the acronym, or identify the backend. Operational responsibility can therefore be high while technical ownership remains unknown.

A second tension is between current observation and historical association. The 2026 urlscan record gives useful SLCM metadata, including IIS 10 and a Microsoft-associated network observation. CT and Wayback records show DMS and SLCM names across historical certificates and captures. But neither archive persistence nor certificate co-listing proves that the old DMS hosts are current, that they share infrastructure, or that they are behind Akamai. The correct decision is to preserve the associations in an asset register while assigning low confidence to unverified topology.

A third tension concerns identity. The FAQ's Outlook-password language and the Office 365 SOP's mandatory MFA make institutional identity central to the user experience. However, the SOP's absence of SLCM or AMS wording means governance should treat account recovery and SLCM access as related processes until formally documented, not assume they are one technical authentication system. The defensive priority is documentation of trust boundaries, not speculative testing.

## VERDICT

**Overall confidence: Medium-high for the operational finding; medium for the historical asset finding; low for the detailed architecture.**

The best-supported verdict is: **DMS is an official MUJ support contact in the AMS/SLCM operational workflow, while DMS-related hostnames have historical public web and certificate evidence, but public research does not establish that `dms.jaipur.manipal.edu` is currently active, that `dmsmuj.jaipur.manipal.edu` is production, that DMS is formally expanded as Document Management System or Digital Media Services for MUJ Jaipur, or that it owns the SLCM backend.** The current central `dms.manipal.edu` sign-in page is a distinct public Document Management System surface, and the 2026 passive SLCM record supports IIS 10 and Microsoft-associated hosting observations. Akamai, ASP.NET MVC 5.3, and .NET Framework 4.x remain unconfirmed in the cited evidence. [21][202.3-12][212.0][215.0][171.0]

| Verdict component | Confidence | Final determination |
|---|---:|---|
| SLCM is MUJ's student academic-information platform | High | Directly stated in official guide |
| `mujslcm.jaipur.manipal.edu` is the documented registration portal | High | Directly stated in official guide and FAQ |
| DMS mailbox supports AMS login escalation | High | Directly stated in official FAQ |
| DMS participates in SLCM operations | Medium-high | Strong operational inference from the FAQ context |
| DMS is formally a department | Low-medium | Not explicitly stated in retrieved FAQ |
| DMS expands to Document Management System for MUJ Jaipur | Low | Central DMS page uses that name, but MUJ Jaipur FAQ does not expand it |
| `dms.jaipur.manipal.edu` had historical public presence | High | Wayback root and route records |
| `dms.jaipur.manipal.edu` is currently active | Low | Current status not established |
| `dmsmuj.jaipur.manipal.edu` was production SLCM | Low | Historical login/test evidence only |
| IIS 10 observed for SLCM | High | Public 2026-06-16 scan record |
| Akamai, MVC 5.3, and .NET Framework 4.x | Low | Not established by cited evidence |
| Direct Microsoft 365 SSO for SLCM | Low-medium | Outlook/password and Office 365/MFA documents are related but not explicit SSO proof |

## References: Exact URLs

| Ref | Source and exact URL |
|---|---|
| | https://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf |
|/[202] | https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf |
| | https://urlscan.io/api/v1/search?q=domain:mujslcm.jaipur.manipal.edu |
| | https://web.archive.org/web/20180806141738id_/http://dms.jaipur.manipal.edu:80/ |
| | https://web.archive.org/web/20220418023042id_/http://dms.jaipur.manipal.edu/ |
| | https://web.archive.org/web/20221210094938id_/http://dmsmuj.jaipur.manipal.edu/ |
| | https://dms.manipal.edu/ |
| | https://urlscan.io/api/v1/search/?q=domain:dms.jaipur.manipal.edu |
| | https://urlscan.io/api/v1/search/?q=domain:dmsmuj.jaipur.manipal.edu |
| | https://jaipur.manipal.edu/about-directorate-of-academic-administration.php |
| | https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf |
| | https://crt.sh/?q=%25.jaipur.manipal.edu&output=json |
| | https://crt.sh/?q=dmsmuj.jaipur.manipal.edu&output=json |
| | https://web.archive.org/cdx/search/cdx?url=dms.jaipur.manipal.edu/&output=json&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype |
| | https://web.archive.org/cdx/search/cdx?url=dms.jaipur.manipal.edu/GenerateCaptcha.aspx*&output=json&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype |
| | https://web.archive.org/cdx/search/cdx?url=dmsmuj.jaipur.manipal.edu/*&output=json&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&collapse=urlkey |

## References

1. *archive.org*. https://archive.org/wayback/available?url=dms.jaipur.manipal.edu/
2. *404 Not Found*. https://crt.sh/?q=dmsmuj.jaipur.manipal.edu&output=json
3. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=dmsmuj.jaipur.manipal.edu/*&output=json&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&collapse=urlkey
4. *crt.sh*. https://crt.sh/?q=%25.jaipur.manipal.edu&output=json
5. *muj.slcm.jaipur.manipal.edu - urlscan.io*. https://urlscan.io/domain/muj.slcm.jaipur.manipal.edu/
6. *Directorate of Academic Administration - Manipal University Jaipur *. https://jaipur.manipal.edu/about-directorate-of-academic-administration.php
7. *mujslcm.jaipur.manipal.edu - urlscan.io*. https://urlscan.io/domain/mujslcm.jaipur.manipal.edu/
8. *Manipal University Jaipur First-Year Student Profile Registration Guide*. https://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf
9. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=dms.jaipur.manipal.edu/*&output=json&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&collapse=urlkey
10. *Frequently Asked Questions and Contacts for SLCM Registration*. https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf
11. [
	MU SLcM
](https://web.archive.org/web/20220815043240id_/https://dmsmuj.jaipur.manipal.edu/loginForm.aspx)
12. *IIS Windows Server*. https://web.archive.org/web/20180806141738id_/http://dms.jaipur.manipal.edu:80/
13. *IIS Windows Server*. https://web.archive.org/web/20220418023042id_/http://dms.jaipur.manipal.edu/
14. *web.archive.org*. https://web.archive.org/web/20221210094938id_/http://dmsmuj.jaipur.manipal.edu/
15. *urlscan.io*. https://urlscan.io/api/v1/search/?q=domain:dmsmuj.jaipur.manipal.edu
16. *urlscan.io*. https://urlscan.io/api/v1/search/?q=domain:dms.jaipur.manipal.edu
17. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=dms.jaipur.manipal.edu/*&output=json&filter=statuscode:200&filter=mimetype:text/html&fl=timestamp,original,statuscode,mimetype&collapse=urlkey
18. *Standard Operating Procedure*. https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf
19. *Manipal University*. https://muj.slcm.jaipur.manipal.edu/
20. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=dms.jaipur.manipal.edu/GenerateCaptcha.aspx*&output=json&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype
21. [
	Document Management System
](https://dms.manipal.edu/)
22. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
23. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=dms.jaipur.manipal.edu/loginForm.aspx&output=json&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype
24. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
25. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=dms.jaipur.manipal.edu/&output=json&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype
26. *urlscan.io*. http://urlscan.io/api/v1/search?q=domain:mujslcm.jaipur.manipal.edu
