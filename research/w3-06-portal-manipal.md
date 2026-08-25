# MUJ SLCM and Portal Public OSINT Assessment

## Executive Summary

- **Academic Function**: Official Manipal University Jaipur material identifies SLcM as the replacement for the older Academic Management System and lists attendance, internal marks, external marks, result publication, and broadcast messages as its modules [17] -> treat `mujslcm.jaipur.manipal.edu` as an academic student and parent system, not merely a generic login page.
- **Portal Function**: The public `portal.manipal.edu` application surface is an EPF system with user, resigned-employee, and administrator login labels, and its footer attributes development to the Information Systems Department at MAHE Manipal [7] -> inventory it as a separate employee or administrative application from MUJ SLCM.
- **Network Attribution**: A public Google DNS response returns `45.112.150.155` for `portal.manipal.edu` with a 300-second TTL [5]. BGP data places that address in AS134039, announced as `45.112.150.0/24`, with the operator label Ibus Virtual Network Services Private Limited [6] -> report Ibus as the network origin or announcing operator, not as proven application owner or tenant.
- **Historical Baseline**: Wayback CDX records successful root captures on 18 April 2022, and the archived page is an IIS Windows Server default landing page [8] [13] -> the hostname has a documented generic-IIS phase, but the archive does not prove when the EPF application was deployed.
- **Technology Evidence**: A current third-party header report for MUJ SLCM records Microsoft-IIS/10.0, ASP.NET MVC 5.3, ASP.NET version identifier 4.0.30319, and `X-Powered-By: ASP.NET` [21]. A separate report for the portal root records Microsoft-IIS/10.0 and ASP.NET, but the response was HTTP 403 [22] -> keep the supplied MUJ stack attribution separate from the weaker portal-root observation.
- **Identity Boundary**: The MUJ first-year guide says SLCM credentials are sent to a student's personal Gmail account and separately instructs students to activate an official email ID [23]. The Office 365 guide says MFA is mandatory before Office 365 use [25] -> document the onboarding chain as distinct credential and identity stages unless an authorized internal source proves federation.
- **Microsoft Tenant Evidence**: Public OpenID metadata establishes a Microsoft identity tenant associated with `jaipur.manipal.edu`, but the metadata itself does not establish that SLCM is integrated with it or supports Microsoft SSO [24] -> classify active SSO as unconfirmed, not as a finding.
- **Akamai Status**: The target DNS lookups returned no CNAME or HTTPS answer in the captured resolver responses [15] [16], and the public header report does not explicitly identify Akamai [22] -> the brief's Akamai description remains unverified from public evidence; absence of those indicators does not rule out a CDN, proxy, or conditional routing.
- **Defensive Priority**: Public material exposes role-specific login labels, stack headers, and an administrator route in search results [7] [26] -> the university's authorized owners should reconcile DNS, application ownership, indexing, error handling, version disclosure, headers, and identity relationships in an internal inventory before any security testing.

## Analytical Basis, Scope, and Evidence Rules

I cannot provide private chain-of-thought or hidden reasoning. Instead, this report gives a concise, reproducible analytical basis: each conclusion is separated into direct observation, source-backed interpretation, and explicitly labelled inference. The evidence set is limited to public pages, public DNS resolver responses, public BGP and passive-telemetry pages, public archive metadata, search-index observations, and official Manipal documents. No authentication, password testing, brute force, intrusive enumeration, exploit validation, or access to protected functions is used or recommended.

The most important distinction is between an endpoint, a network announcement, and an institution. DNS shows what address a resolver returned. BGP shows which autonomous system announced a prefix. A web page shows what a responding application disclosed. None of those layers alone proves legal ownership, physical hosting, tenancy, or authorization. For that reason, the report uses "observed," "reported," and "consistent with" for technical data, and uses "inference" when connecting separate observations.

The observations are also time-bound. The portal SecurityHeaders report identifies a report time of 25 August 2026 12:27:58 UTC [22], while the MUJ report identifies 25 August 2026 12:34:32 UTC [21]. Archive captures represent their capture dates, not a continuous history. Search indexing is dynamic and is not an exhaustive route inventory. These limitations reduce overclaiming while still making the public attack-surface picture useful for defensive governance.

## Exact Tables: Evidence Inventory

| Research question | Direct public finding | Confidence | Exact source URL |
|---|---|---:|---|
| What does MUJ SLCM do? | It replaced the older AMS and covers attendance, marks, results, and broadcast messages for students and parents [17]. | High | http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf |
| What is the portal's current public application? | EPF pages expose user, resigned-employee, and admin login labels and identify MAHE Information Systems as developer [7]. | High | https://portal.manipal.edu/epf/userlogin.aspx |
| What address did DNS return? | `portal.manipal.edu` returned `45.112.150.155` with TTL 300 in the captured Google Public DNS response [5]. | High for that response | https://dns.google/resolve?name=portal.manipal.edu&type=A |
| Who announces the address? | AS134039 announces `45.112.150.0/24` and is labelled Ibus Virtual Network Services Private Limited [6]. | High for network attribution | https://bgp.he.net/ip/45.112.150.155 |
| Is the historical root documented? | Wayback recorded 200 responses for the root on 18 April 2022, and the archived page was an IIS Windows Server landing page [8] [13]. | High for captures | https://web.archive.org/cdx/search/cdx?url=portal.manipal.edu&output=json&filter=statuscode:200&fl=timestamp,original,statuscode,digest&collapse=digest |
| Is MUJ's supplied stack publicly visible? | A third-party report lists IIS 10, ASP.NET MVC 5.3, ASP.NET 4.0.30319, and ASP.NET [21]. | Medium-high | http://securityheaders.com/?followRedirects=on&q=https://mujslcm.jaipur.manipal.edu/ |
| Is Akamai proven? | The captured portal CNAME and HTTPS DNS responses contain no answer, and the public header result does not name Akamai [15] [16] [22]. | Low; unconfirmed | https://dns.google/resolve?name=portal.manipal.edu&type=CNAME |

The table distinguishes high-confidence facts from lower-confidence infrastructure inferences. In particular, the AS row answers "who announces the IP" more reliably than it answers "who operates the application." That distinction is central to a responsible university security report.

## 1. MUJ SLCM Function and the Student Onboarding Case

The public MUJ portal itself identifies the service as a MUJ portal and presents sign-in and parent-login choices [2]. The official ICT inventory is more informative than the landing page: it says Student Life Cycle Management replaced the older Academic Management System, provides attendance, internal marks, external marks, result publication, and broadcast-message functions, and serves as a single window for students and parents handling academic matters [17]. This is direct evidence of business function, not a guess based on the hostname.

The official first-year guide reinforces that interpretation. It calls SLcM a one-stop platform for accessing academic information throughout a student's time at the university and gives `https://mujslcm.jaipur.manipal.edu` as the access link [23] [23]. The official FAQ uses the older AMS term while giving the same SLCM registration URL and AMS contacts [20] [20]. The mixed terminology is important: it suggests a transition in institutional naming, but it does not by itself prove that the backend was replaced, rewritten, or migrated.

### Case study: student onboarding is not the same as SSO

A new-student workflow illustrates the identity boundary. The first-year guide says the SLCM username and password are sent to the personal Gmail address supplied during admission [23]. The same guide separately presents an instruction to activate the official email ID and says the official email password reset procedure is included in the email sent to personal Gmail [23]. The FAQ also describes the SLCM password as being based on the official Outlook ID [20]. Taken together, these documents show an operational relationship among admissions, personal Gmail, official email, and SLCM credentials.

They do not establish that SLCM delegates authentication to Microsoft. That is a key analytical point: a university may use an official Outlook identity as a credential source, a password policy reference, a separate directory record, or an actual federated login. The public documents establish the first three possibilities as relevant to onboarding, but do not prove the fourth. The defensible action is to map the identity lifecycle internally, not to infer SSO from the presence of Microsoft terminology.

| Identity or support surface | Publicly documented behavior | Interpretation | Exact source URL |
|---|---|---|---|
| MUJ SLCM | Credentials are sent to a personal Gmail account used during admission [23]. | Admission communications are part of onboarding; this is not proof of the login provider. | https://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf |
| Official MUJ email | Students are told to activate an official email ID and use a documented reset process [23]. | Official email is a separate lifecycle step in the public guide. | https://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf |
| Outlook wording | The FAQ says the SLCM password is as per the official Outlook ID [20]. | Shows credential or password-policy linkage; the exact authentication architecture is not stated. | https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf |
| Microsoft 365 | MFA is mandatory before Office 365 can be used [25]. | Confirms an institutional Microsoft 365 control for Office 365, not automatically for SLCM. | https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf |
| Entra metadata | The public configuration names a `jaipur.manipal.edu` Microsoft tenant and Microsoft endpoints [24]. | Tenant existence is established; SLCM federation remains unconfirmed. | http://login.microsoftonline.com/jaipur.manipal.edu/.well-known/openid-configuration |

## 2. portal.manipal.edu Function and Current Public Surface

The current public application evidence points to EPF rather than SLCM. The indexed EPF page presents "Home," "User login," "Resigned Employee login," and "admin login," followed by an email-ID and password form [7]. Its footer says it was designed and developed by the Information Systems Department at MAHE Manipal [7]. A second EPF login route exposes an employee-ID form, while the indexed administrator route is labelled "Admin Login" and includes an `@manipal.edu` email cue [27] [26]. These are descriptions of publicly visible labels only; they are not instructions to attempt authentication.

The portal root behaves differently from the EPF subapplication in the available passive evidence. A current third-party report for `https://portal.manipal.edu/` records a 403 response and warns that not all security headers may be set on an error response [22]. The same report still identifies the target as `45.112.150.155` and records Microsoft-IIS/10.0 and ASP.NET in the raw response [22] [22]. Thus, "generic but live" should be stated carefully: DNS resolves, an HTTP service responds to a passive report, and a public EPF application page is available in indexing, but the root response captured by the report is an access-denied page rather than a normal landing page.

### Case study: root behavior versus subapplication behavior

The root and EPF routes are a useful example of why hostname-level conclusions are dangerous. The root's 403 response may reflect an access policy, a default-site rule, a WAF decision, or an application configuration. The EPF page, by contrast, exposes a functional login interface and institutional attribution [7]. The evidence therefore supports two separate observations: root-level access is restricted in the captured response, and a child application is publicly discoverable.

The inference is that the host may be serving multiple site bindings or application paths with different policies. That inference is plausible but not proven by the public pages. A defensive owner should reconcile the IIS site, virtual-directory, DNS, and reverse-proxy inventories internally. A security club should not attempt to bypass the 403 or probe alternate functions; the public report is already sufficient to raise an ownership and exposure question.

| Indexed or publicly observed path | Visible function or label | Evidence status | Exact source URL |
|---|---|---|---|
| `/epf` | EPF application entry point [7]. | Publicly indexed and observed. | https://portal.manipal.edu/epf |
| `/epf/Home.aspx` | EPF home route. | Search-index observation; live behavior should not be assumed from indexing. | https://portal.manipal.edu/epf/Home.aspx |
| `/epf/userlogin.aspx` | User login with email ID and password [7]. | Publicly observed. | https://portal.manipal.edu/epf/userlogin.aspx |
| `/epf/rtlogin.aspx` | Resigned-employee or related employee login route with an employee-ID label [27]. | Publicly observed. | https://portal.manipal.edu/epf/rtlogin.aspx |
| `/epf/admlogin.aspx` | Administrator login route with an `@manipal.edu` email cue [26]. | Search-index observation; authorization behavior is not tested. | https://portal.manipal.edu/epf/admlogin.aspx |
| `/` | Root target returned HTTP 403 in the cited passive report [22]. | Current report observation, not a complete route inventory. | https://portal.manipal.edu/ |

The table is an exposure inventory, not a test plan. Search indexing can lag behind deployment and can contain stale URLs. The safe conclusion is that these paths have been publicly discoverable at some point, so owners should verify whether each is intentional, protected, and appropriately indexed.

## 3. Network Attribution for 45.112.150.155

The captured Google Public DNS A response answers the narrow DNS question: `portal.manipal.edu` resolved to `45.112.150.155`, with an answer TTL of 300 seconds [5]. The response is evidence from that resolver at that time, not a universal statement about every recursive resolver or every point in time. A CNAME query returned no answer and included the parent-domain SOA authority [15]. An HTTPS-record query likewise returned no answer [16]. These results are useful indicators, but negative DNS answers do not eliminate conditional records, proxying, or a CDN layer that is not represented in those record types.

The network attribution is stronger. BGP.HE reports AS134039, the announced prefix `45.112.150.0/24`, and the operator description Ibus Virtual Network Services Private Limited [6]. Urlscan separately lists the IP as `45.112.150.155`, the route as `45.112.148.0/22`, the AS as AS134039, and GeoIP as Udupi, India [9] [9] [9]. The two public sources agree at the high-level AS and address level, while their prefix views differ because one is the more specific announced `/24` and the other is the route associated with the AS metadata.

| Layer | Observation | What it proves | What it does not prove | Exact source URL |
|---|---|---|---|---|
| DNS A | `portal.manipal.edu` -> `45.112.150.155`, TTL 300 [5]. | A resolver returned this address. | Global permanence, ownership, or application tenancy. | https://dns.google/resolve?name=portal.manipal.edu&type=A |
| DNS CNAME | No answer in the captured response [15]. | No CNAME was returned by that query. | That no proxy or CDN exists under all conditions. | https://dns.google/resolve?name=portal.manipal.edu&type=CNAME |
| BGP origin | AS134039 and `45.112.150.0/24` [6]. | The public route was associated with this announcing AS. | That Ibus owns the Manipal application or data. | https://bgp.he.net/ip/45.112.150.155 |
| Passive metadata | AS134039, Udupi GeoIP, `45.112.148.0/22`, and the IP [9] [9] [9]. | Independent metadata is consistent with the network attribution. | Physical location of the server or institutional control. | https://urlscan.io/domain/portal.manipal.edu |
| Domain relationship | Urlscan identifies `manipal.edu` as the registered domain [9]. | The hostname is under that registered-domain label. | The registered-domain holder's hosting contract or infrastructure design. | https://urlscan.io/domain/portal.manipal.edu |

### Who hosts it?

The most supportable answer is: the IP is publicly announced through AS134039, labelled Ibus Virtual Network Services Private Limited, and geolocated by urlscan to Udupi. That is a network-origin answer. It is not enough to say that Ibus owns or operates the EPF application, that a specific campus hosts it, or that the server is physically in Udupi. Those stronger claims would require a first-party infrastructure statement, contract record, or authorized internal evidence, none of which is present in the cited public material.

Urlscan's page also reports no direct hits, no incoming hits, and nothing talked to the domain in its available view [9], while separately displaying passive metadata and a live-screenshot notice [9]. This apparent tension is why those fields should be treated as telemetry limitations rather than as proof that the service is unused. The AS and DNS findings are the reliable core; the urlscan activity counters are context only.

## 4. Technology and Security Header Observations

The MUJ SLCM technology lead in the research brief is substantially corroborated by a current third-party header report. The report gives the site as `https://mujslcm.jaipur.manipal.edu/`, IP `98.70.14.50`, and grade D [21]. Its exposed response metadata includes Microsoft-IIS/10.0, `x-aspnetmvc-version: 5.3`, `x-aspnet-version: 4.0.30319`, and `x-powered-by: ASP.NET` [21]. The exact runtime identifier is safer to report than a broader claim about every installed .NET component. It is consistent with an ASP.NET and .NET Framework 4.x-era deployment, but the public report does not enumerate the full framework inventory.

The portal root has weaker but still useful technology evidence. Its separate report gives grade F, target IP `45.112.150.155`, and an HTTP 403 response [22] [22]. Microsoft-IIS/10.0 and ASP.NET are present in the raw response [22]. Because the report warns that the response was an error and that not all headers may be set on an error response [22], this should not be treated as a complete characterization of the EPF application's normal responses. Most importantly, the public evidence does not justify transferring the MUJ SLCM MVC 5.3 label to `portal.manipal.edu`.

| Host | Public technology indicators | Header or status observation | Confidence and caveat | Exact source URL |
|---|---|---|---|---|
| `mujslcm.jaipur.manipal.edu` | IIS 10.0, ASP.NET MVC 5.3, ASP.NET version identifier 4.0.30319, ASP.NET powered-by header [21]. | SecurityHeaders grade D and several missing headers are reported [21] [21]. | Medium-high for the captured response; third-party report, time-bound. | http://securityheaders.com/?followRedirects=on&q=https://mujslcm.jaipur.manipal.edu/ |
| `portal.manipal.edu` root | IIS 10.0 and ASP.NET [22]. | SecurityHeaders grade F; raw status HTTP 403 [22] [22]. | Medium for the captured error response; not a full normal-page fingerprint. | https://securityheaders.com/?q=https%3A%2F%2Fportal.manipal.edu%2F&followRedirects=on |
| `portal.manipal.edu/epf` | Public `.aspx` EPF routes and institutional footer [7]. | Normal login page content is visible in the cited page. | High for page function; no claim that all EPF components share one framework version. | https://portal.manipal.edu/epf/userlogin.aspx |
| Akamai layer | No explicit Akamai label in the cited public header result [22]. | Portal CNAME and HTTPS queries returned no answer [15] [16]. | Low; Akamai use is unconfirmed, not disproved. | https://dns.google/resolve?name=portal.manipal.edu&type=HTTPS |

The reported MUJ header posture includes X-Frame-Options, HSTS, CSP, X-Content-Type-Options, Referrer-Policy, and Permissions-Policy in the header checklist, with HSTS, CSP, X-Content-Type-Options, Referrer-Policy, and Permissions-Policy reported missing while X-Frame-Options is present [21]. The portal report lists the same class of security headers and reports them missing, but again warns that the 403 response may distort the result [22]. These are configuration-review signals, not proof of exploitability.

### Case study: two hosts, two disclosure profiles

The MUJ report returns a functional-looking page and exposes the exact MVC and ASP.NET version indicators [21]. The portal root returns 403 but still exposes IIS and ASP.NET in the error response [22]. The inference is that the two hosts, or at least the two observed response policies, have different exposure profiles: MUJ is more informative at the application layer, while the portal root is more restrictive at the status layer but still discloses server technology.

The recommended decision is therefore not "fix one header everywhere" in isolation. Owners should compare normal, denied, redirect, and error responses under authorized internal review; verify which layer terminates TLS; confirm whether a proxy modifies headers; and remove unnecessary version disclosure where operationally safe. No public testing beyond the cited passive observations is needed to justify that review.

## 5. Archive History and the Evolution Question

Wayback CDX shows two successful root captures for `portal.manipal.edu` on 18 April 2022: an HTTP root and an HTTPS root, each with status 200 [8]. A wildcard query adds a successful capture of `/iis-85.png` [4]. The archived HTTPS snapshot is titled "IIS Windows Server" and contains the standard IIS link [13]. This is strong evidence that the root served a generic IIS landing page at that capture time.

The available archive does not establish a continuous timeline from the default page to the current EPF application. The target's urlscan metadata lists the hostname as first observed on 4 January 2019 [9] and gives an age label of eight years [9], but those fields are passive-observation metadata, not proof of application content in 2019. The correct historical statement is therefore narrow: the hostname was observed by urlscan by the listed date, and the root was a default IIS page in April 2022.

MUJ SLCM has a different archive pattern. The wildcard CDX result includes 200 captures for the root, `/Home/Index`, favicon, CSS and JavaScript, logos, and other theme assets on 10 January 2025, with a later root capture on 27 May 2025 and asset rows in August 2026. The archived paths include a Keen theme asset tree and application-specific login and navigation resources. This provides public evidence of a structured MVC-style application surface, but archive paths alone do not prove all current routes or current deployment settings.

| Host | Archive observation | Date represented | Safe conclusion | Exact source URL |
|---|---|---|---|---|
| portal root | HTTP and HTTPS root status 200 [8]. | 18 April 2022. | The root was captured successfully at that time. | https://web.archive.org/cdx/search/cdx?url=portal.manipal.edu&output=json&filter=statuscode:200&fl=timestamp,original,statuscode,digest&collapse=digest |
| portal root | `/iis-85.png` status 200 [4]. | 18 April 2022. | The root-associated IIS asset was archived. | https://web.archive.org/cdx/search/cdx?url=portal.manipal.edu/*&output=json&filter=statuscode:200&fl=timestamp,original,statuscode,digest&collapse=urlkey |
| portal snapshot | Title "IIS Windows Server" and standard IIS link [13]. | 18 April 2022. | The archived root was a generic IIS landing page. | https://web.archive.org/web/20220418001040/https://portal.manipal.edu/ |
| MUJ SLCM | Root, `/Home/Index`, scripts, styles, favicon, and assets returned status 200 in CDX output. | 10 January 2025 and later captures. | MUJ had a structured archived application surface. | https://web.archive.org/cdx/search/cdx?url=mujslcm.jaipur.manipal.edu/*&output=json&filter=statuscode:200&fl=timestamp,original,statuscode,digest&collapse=urlkey |

### Case study: historical root versus current EPF

The 2022 archived root is generic IIS, while the currently indexed child route is a branded EPF login page with MAHE attribution [13] [7]. A reasonable inference is that the hostname's root configuration, application mapping, or deployment purpose changed over time. It is not safe to say that the EPF system itself existed in 2022, because the archived root does not show it and the available CDX records do not provide an application deployment date.

This distinction matters for incident response and asset ownership. A team reviewing only the current EPF page might miss the fact that the hostname had a generic root history. A team reviewing only the archive might incorrectly conclude that no current application exists. The decision-ready action is to preserve the archive as historical evidence and separately confirm current application mappings through internal change records.

## 6. Links to Other Manipal Systems and Institutional Context

The official MAHE student portal page links to the SIS student portal at `https://sis.manipal.edu/index.aspx` [10]. The SIS site describes itself as a Student Information System conceived for students and parents of the Manipal Academy of Higher Education, limits use to bona fide students and parents, provides student or parent and administrator or faculty login choices, and directs users to Fee Kart for academic-fee payment [3]. This is a direct institutional relationship in the public navigation and site descriptions, unlike the unproven relationship between SLCM and Microsoft SSO.

The same official MAHE page exposes other institutional links, including application status and admissions through `apply.manipal.edu`, a research portal, and related navigation [10]. Publicly indexed or extracted login surfaces also include a Manipal FC page with a `@manipal.edu` username cue and MAHE Information Systems footer, a hospital-management login page [28], and a library portal [29]. Their existence is useful for asset discovery, but the public evidence does not establish that these systems share infrastructure, identity, or authorization with MUJ SLCM.

| System or domain | Publicly visible function | Relationship to MUJ SLCM | Exact source URL |
|---|---|---|---|
| MUJ SLCM | Academic information, student and parent portal [17] [2]. | Primary subject of this report. | https://mujslcm.jaipur.manipal.edu/ |
| SIS | Student Information System for MAHE students and parents; includes administrator or faculty login and Fee Kart [3]. | Directly linked from the official MAHE student portal; shared SLCM identity is not established. | https://sis.manipal.edu/ |
| MAHE Student Portal | Official navigation links to SIS and application status or admissions [10] [10]. | Institutional navigation context, not proof of shared backend. | https://www.manipal.edu/mu/academics/student-portal.html |
| Admissions | Application status and admissions workflow are linked by the official MAHE page [10]. | Upstream onboarding context; first-year SLCM guide says credentials are sent after admission [23]. | https://apply.manipal.edu/ |
| MUFC | Login page uses a `@manipal.edu` username cue and MAHE Information Systems attribution. | Similar institutional branding; shared authentication is unconfirmed. | https://mufc.manipal.edu/ |
| Hospital Management | Public login page exists at the listed URL [28]. | Related institutional surface; functional or ownership linkage to SLCM is not established. | https://hms.manipal.edu/login.aspx |
| Library Portal | Public library portal title is present [29]. | Related institutional surface; shared authentication is unconfirmed. | https://libportal.manipal.edu/ |

### Case study: SIS is a confirmed navigation link, not a confirmed shared identity

The SIS relationship is stronger than a hostname similarity because the official MAHE student portal explicitly links to SIS [10]. SIS also describes its intended users and functions [3]. That combination supports a high-confidence statement that SIS is part of the broader Manipal student-services ecosystem.

The public evidence still stops short of proving that SLCM and SIS share a database, session, identity provider, or authorization model. This is an important contrast with the official page's visible navigation: a link proves institutional discoverability, not technical integration. The defensive inventory should record SIS as a related system and separately record whether the same account, MFA policy, and lifecycle events are actually shared.

The official MUJ contact page supplies practical ownership paths for this inventory. It lists academic contacts, IT Infra, the Registrar Office, Student Welfare, and Webmaster contacts [1] [1] [1] [1]. The SLCM FAQ also gives AMS and DMS contacts for login issues and an IT Infra email for Outlook problems [20]. These are appropriate public governance channels for confirming ownership; they are not evidence that any individual listed is the technical operator of a particular server.

## 7. Public Indexing, Metadata Exposure, and Defensive Interpretation

The indexed EPF route set is operationally meaningful because it distinguishes user, resigned-employee, and administrator audiences [7]. The administrator route is separately discoverable and includes a branded email cue [26]. Public labels do not demonstrate an access-control flaw, and the report should not imply that they do. They do, however, provide enough information for a defender to ask whether role-specific pages are intentionally public, whether they should appear in search results, and whether denial behavior is consistent across the routes.

The same principle applies to technology headers. The MUJ report discloses exact server and ASP.NET version indicators [21]. The portal error response discloses IIS and ASP.NET even while returning 403 [22]. Version disclosure by itself is not proof of vulnerability. It is a useful hardening and asset-correlation signal, particularly when an institution has multiple legacy `.aspx` applications and several branded login pages.

The public MUJ security.txt path is also worth recording cautiously. The retrieved response at `/.well-known/security.txt` appeared to contain portal sign-in content and an `@muj.manipal.edu` reference rather than a clearly structured security.txt contact record [30]. RFC 9116 says the Contact field must be present in a security.txt file [31]. This does not prove that the university lacks a vulnerability-reporting process; it indicates that the particular public response retrieved at that path was not a clear, usable security.txt document. Researchers should use official university contacts and responsible disclosure channels rather than attempting to validate the path through intrusive methods.

| Exposure category | Public evidence | Safe interpretation | Defensive owner action |
|---|---|---|---|
| Role labels | EPF page names user, resigned-employee, and admin login [7]. | Audience segmentation is publicly disclosed; no access-control conclusion follows. | Confirm intended public discoverability and consistent authorization for each role. |
| Admin route | `/epf/admlogin.aspx` appears in public indexing with an admin label [26]. | Route existence is an exposure fact, not evidence of bypass. | Review indexing, route naming, authentication, monitoring, and ownership through authorized channels. |
| Server versions | MUJ report exposes IIS 10, MVC 5.3, and ASP.NET 4.0.30319 [21]. | Technology fingerprinting is possible from the public response. | Review version-support status and whether unnecessary headers can be removed. |
| Error response | Portal root returns 403 but exposes IIS and ASP.NET [22]. | Error behavior discloses server technology; the report may not represent normal responses. | Compare normal and error response policies in an authorized internal review. |
| Security.txt | Retrieved path is not clearly a structured security.txt response [31]. | Public reporting instructions may be unclear at that path. | Publish or verify a current responsible-disclosure contact using official governance. |

## 8. Defensive Priorities for the University Security Club

The first priority is asset ownership reconciliation. The public evidence shows at least two named application hosts, two different IP addresses, and different response profiles: MUJ SLCM is reported at `98.70.14.50` [21], while the portal target is at `45.112.150.155` [22]. The target address is announced by AS134039 [6], while the MUJ DNS A response returns `98.70.14.50` [14]. The inference is that these are distinct public endpoints, not a single interchangeable SLCM host. Owners should validate this against the authoritative DNS, IIS, certificate, reverse-proxy, and service-owner inventories.

The second priority is an identity map. Public documents mention personal Gmail delivery, official Outlook identity, Office 365, mandatory MFA, and SLCM credentials [23] [20] [25]. The public Microsoft OpenID configuration confirms a tenant but explicitly does not prove SLCM integration [24]. The action is to document which system creates an account, which system resets a password, where MFA is enforced, and whether SLCM is local-authenticated, directory-backed, or federated. This should be done from internal architecture records, not by attempting alternate login flows.

The third priority is response and header consistency. The MUJ report reports missing HSTS, CSP, X-Content-Type-Options, Referrer-Policy, and Permissions-Policy while showing X-Frame-Options [21]. The portal report reports missing headers on a 403 response but warns that an error response can omit normal headers [22]. Owners should test these controls in a controlled staging or authorized production review, including successful, denied, redirect, and error responses. The report does not recommend probing or bypassing any public control.

The fourth priority is indexing and lifecycle hygiene. The public route list includes a role-specific administrator path and multiple employee login paths [7] [26]. Search exclusion alone would not replace authentication, but a deliberate indexing policy can reduce unnecessary operational metadata. The owner should also verify that retired routes, old AMS naming, and legacy EPF pages are either intentionally maintained, redirected, or removed under change control.

The fifth priority is CDN and hosting confirmation. The brief says the system is behind Akamai, but the cited public evidence does not independently confirm that statement. The captured portal DNS responses have no CNAME or HTTPS answer [15] [16], and the header report names IIS and ASP.NET without naming Akamai [22]. This is not proof that Akamai is absent. The safe action is to confirm the edge provider from internal DNS management, TLS termination records, CDN configuration, and authorized logs, then document which headers and source IPs are expected at each layer.

| Priority | Evidence basis | Decision or action | Constraint |
|---|---|---|---|
| Ownership inventory | Separate MUJ and portal IPs and response reports [21] [22]. | Assign a named owner and service purpose to every hostname, path, IP, and ASN relationship. | Use internal records; do not infer ownership from the AS alone. |
| Identity architecture | Gmail onboarding, Outlook wording, Office 365 MFA, and Entra metadata [23] [20] [25] [24]. | Document account creation, reset, MFA, federation, and deprovisioning paths. | Do not claim SSO without an architecture or first-party confirmation. |
| Header and error policy | MUJ missing-header report and portal 403 warning [21] [22]. | Review normal and error responses and reduce version disclosure where appropriate. | Passive reports are signals, not exploitability findings. |
| Indexing hygiene | Public EPF role routes and administrator route [7] [26]. | Verify intentional indexing, route lifecycle, and role separation. | Do not test credentials or access controls without authorization. |
| CDN confirmation | No captured CNAME or HTTPS answer; no explicit Akamai label [15] [16] [22]. | Reconcile public evidence with internal edge-provider records. | Absence of public indicators is inconclusive. |

## Synthesis

The ecosystem is best understood as several related but not yet technically conflated services. MUJ SLCM is an academic workflow system: its documented scope is attendance, marks, results, broadcasts, and student or parent access [17]. `portal.manipal.edu` is presently represented by EPF employee and administrator login routes [7]. SIS is a separate student-information and fee-related service that is directly linked from the official MAHE student portal [10] [3]. The evidence base is strongest for function and navigation, weaker for shared infrastructure, and weakest for shared authentication.

| Dimension | MUJ SLCM | portal.manipal.edu EPF | SIS | Decision-ready contrast |
|---|---|---|---|---|
| Primary audience | Students and parents for academic matters [17] [2]. | Employees, resigned employees, and administrators based on visible role labels [7]. | Students, parents, administrators, and faculty [3]. | Audience overlap exists, but role and business functions differ. |
| Public technology evidence | IIS 10, MVC 5.3, ASP.NET 4.0.30319 [21]. | IIS 10 and ASP.NET seen on a 403 root response [22]; EPF pages are `.aspx` routes [7]. | The cited page establishes function, not a complete stack fingerprint [3]. | Do not transfer MUJ's MVC version to portal or SIS. |
| Public network evidence | A response is reported at `98.70.14.50` [21], and MUJ A DNS returns that address [14]. | `45.112.150.155` and AS134039 are publicly reported [5] [6]. | The cited evidence identifies the domain but does not establish shared hosting. | Treat addresses as separate assets pending internal confirmation. |
| Identity evidence | SLCM credentials and official email are discussed in onboarding [23] [20]. | EPF form uses email or employee identity labels [7] [27]. | SIS exposes student or parent and administrator or faculty roles [3]. | Shared institutional branding does not prove shared authentication. |
| Archive evidence | Structured root, Home/Index, and assets appear in 2025-2026 CDX captures. | Root was a generic IIS page in April 2022 [8] [13]. | No archive claim is made here from the cited evidence. | Archive continuity is stronger for MUJ than for the portal application. |
| Main trade-off | Rich academic functionality requires a clear student identity lifecycle. | Multiple role paths create operational segmentation and indexing risk. | Broad student and finance functions need clear audience separation. | Governance should manage the ecosystem as a portfolio, not one hostname. |

Three tensions deserve emphasis. First, institutional identity is converging operationally while technical integration remains unknown: the same public documents mention SLCM, official Outlook, Office 365 MFA, and a Microsoft tenant, but none proves SLCM SSO [23] [25] [24]. Second, public accessibility and defensive restriction diverge: EPF child routes are discoverable, while the target root returned 403 [7] [22]. This may be intentional segmentation, but it also creates an asset-management problem if the owner of the root differs from the owner of the child application.

Third, the network layer is more observable than the tenancy layer. AS134039 and the `/24` route are public facts [6], while application ownership, physical hosting, and CDN use are not proven. This is the non-obvious risk: a security report that calls the ASN the "host" or calls Microsoft OpenID metadata an "SSO integration" would be more confident than the evidence permits. The correct strategy is layered attribution with explicit uncertainty.

## VERDICT

**Overall confidence: Medium-high for the core inventory; medium for current technology posture; low for Akamai and SSO claims.**

| Claim | Verdict | Confidence | Reason |
|---|---|---:|---|
| MUJ SLCM is an academic student and parent system | Verified | High | Official ICT inventory, official MUJ page, FAQ, and first-year guide agree [17] [2] [20] [23]. |
| `portal.manipal.edu` currently exposes an EPF application surface | Verified | High | Public EPF page shows the function, roles, form, and MAHE Information Systems footer [7]. |
| `portal.manipal.edu` resolves to `45.112.150.155` in the captured lookup | Verified for the captured response | High | Google Public DNS A response states the address and TTL [5]. |
| The address is announced by Ibus-labelled AS134039 | Verified at the network layer | High | BGP.HE identifies AS134039 and `45.112.150.0/24` [6]. |
| The exact application tenant or physical host is Ibus | Not established | Low | An announcing AS does not prove application ownership or physical tenancy. |
| MUJ SLCM exposes IIS 10, MVC 5.3, ASP.NET 4.0.30319 | Reported by current passive header evidence | Medium-high | The SecurityHeaders report lists these values [21]. |
| Portal root uses the same MVC 5.3 stack | Not established | Low | The portal report shows IIS and ASP.NET on a 403 but does not report MVC 5.3 [22]. |
| The portal is behind Akamai | Unconfirmed | Low | No captured CNAME or HTTPS answer and no explicit Akamai label appear in the cited evidence [15] [16] [22]. |
| MUJ SLCM uses Microsoft 365 or Entra SSO | Unconfirmed | Low | Tenant metadata exists, but the OpenID document expressly does not establish SLCM integration [24]. |
| Portal root had a generic IIS phase | Verified for April 2022 captures | High | Wayback recorded root 200 captures and an IIS Windows Server page [8] [13]. |

The final decision is to treat `mujslcm.jaipur.manipal.edu`, `portal.manipal.edu`, and `sis.manipal.edu` as related Manipal ecosystem assets with separate functions and currently separate public evidence. The security club can responsibly report the network attribution, EPF route inventory, archive baseline, MUJ technology indicators, identity-document relationships, and unresolved Akamai or SSO questions. It should not publish the stronger claims that Ibus owns the application, that the root and SLCM share a backend, or that Microsoft SSO is active.

The recommended next step is an authorized owner-confirmation and configuration review using internal DNS, IIS, certificate, CDN, identity, and change-management records. Public evidence already supports that review. No unauthorized login attempt, bypass attempt, brute force, exploit validation, or protected-function enumeration is necessary or appropriate.

## References

1. *Contact Us - Manipal University Jaipur *. https://jaipur.manipal.edu/contact-university.php
2. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
3. [
	SIS Portal
](https://sis.manipal.edu/)
4. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=portal.manipal.edu/*&output=json&filter=statuscode:200&fl=timestamp,original,statuscode,digest&collapse=urlkey
5. *dns.google*. https://dns.google/resolve?name=portal.manipal.edu&type=A
6. *45.112.150.155 - bgp.he.net*. https://bgp.he.net/ip/45.112.150.155
7. [

](https://portal.manipal.edu/epf/userlogin.aspx)
8. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=portal.manipal.edu&output=json&filter=statuscode:200&fl=timestamp,original,statuscode,digest&collapse=digest
9. *portal.manipal.edu - urlscan.io*. https://urlscan.io/domain/portal.manipal.edu
10. *Student Portal Login- MAHE (Manipal Academy Of Higher Education)*. https://www.manipal.edu/mu/academics/student-portal.html
11. *http://crt.sh/?output=json&q=mujslcm.jaipur.manipal.edu*. http://crt.sh/?output=json&q=mujslcm.jaipur.manipal.edu
12. *Technologies used on portal.manipal.edu - Wappalyzer*. https://www.wappalyzer.com/lookup/portal.manipal.edu/
13. *IIS Windows Server*. https://web.archive.org/web/20220418000717/http://portal.manipal.edu/
14. *dns.google*. https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=A
15. *dns.google*. https://dns.google/resolve?name=portal.manipal.edu&type=CNAME
16. *dns.google*. https://dns.google/resolve?name=portal.manipal.edu&type=HTTPS
17. *Contents*. https://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf
18. *dns.google*. https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=CNAME
19. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=mujslcm.jaipur.manipal.edu/*&output=json&filter=statuscode:200&fl=timestamp,original,statuscode,digest&collapse=urlkey
20. *Frequently Asked Questions and Contacts for SLCM Registration*. https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf
21. *Scan results for https://mujslcm.jaipur.manipal.edu/*. http://securityheaders.com/?followRedirects=on&q=https://mujslcm.jaipur.manipal.edu/
22. *Scan results for https://portal.manipal.edu/*. https://securityheaders.com/?q=https%3A%2F%2Fportal.manipal.edu%2F&followRedirects=on
23. *Manipal University Jaipur First-Year Student Profile Registration Guide*. https://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf
24. *Openid Configuration*. http://login.microsoftonline.com/jaipur.manipal.edu/.well-known/openid-configuration
25. *Standard Operating Procedure*. https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf
26. *Manipal Academy of Higher Education*. https://portal.manipal.edu/epf/admlogin.aspx
27. [

](https://portal.manipal.edu/epf/rtlogin.aspx)
28. *Login*. https://hms.manipal.edu/login.aspx
29. [
	Library Portal
](https://libportal.manipal.edu/)
30. *http://mujslcm.jaipur.manipal.edu/.well-known/security.txt*. http://mujslcm.jaipur.manipal.edu/.well-known/security.txt
31. *http://rfc-editor.org/rfc/rfc9116.html*. http://rfc-editor.org/rfc/rfc9116.html
