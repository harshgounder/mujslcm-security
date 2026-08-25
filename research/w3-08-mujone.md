# MUJ SLCM Ecosystem: Public Evidence, Identity Boundaries, and Technology Risk

## Executive Insights

- **MUJ One Is Publicly an HR System**: The target host presents "MUJ HR SYSTEM," employee-code, date-of-birth, CAPTCHA, password-change, policy-acknowledgement, and PAS Portal controls, with an ISD/CSD, MAHE attribution [4] [4] [4] [4]. **Decision:** classify mujone.jaipur.manipal.edu as an HR-facing application unless authoritative documentation proves a wider role.
- **SLCM Is the Student and Parent Portal**: The separate mujslcm host is branded "WELCOME TO MUJ PORTAL" and publicly exposes sign-in, parent-login, and the @muj.manipal.edu account label [1] [3]. **Decision:** treat SLCM, not MUJ One, as the primary publicly evidenced student lifecycle entry point.
- **Outlook Credentials Are Coupled, but Federation Is Not Proven**: MUJ's SLCM FAQ gives the SLCM registration URL and says the password is according to the official Outlook ID [36], while the SLCM page has been observed linking password recovery to Microsoft's password-reset service [3]. **Decision:** model the relationship as shared credential or identity coupling, not confirmed Entra ID SSO.
- **Microsoft 365 Is Officially Part of MUJ IT**: MUJ's IT page lists Microsoft communication and business ERP services alongside a student life-cycle web portal and LMS [24]. A separate MUJ SOP directs students and employees to login.microsoftonline.com and makes MFA mandatory [21] [21]. **Decision:** Microsoft 365 is a confirmed ecosystem dependency, but the public evidence does not demonstrate that SLCM or MUJ One is an OAuth, SAML, or OpenID Connect relying party.
- **The Stated Azure Attribution Is Partly Supported**: Public DNS resolves mujone.jaipur.manipal.edu to 52.172.36.15 [37], and IPinfo identifies that address as AS8075 Microsoft Corporation in Chennai, Tamil Nadu, India [23]. **Decision:** report Microsoft-hosted infrastructure and Chennai geolocation; do not assert Azure South India as a verified region from this evidence alone.
- **Akamai Is Not Publicly Demonstrated**: Public URLScan material for the related SLCM hostname shows Microsoft-IIS/10.0 and Microsoft-IIS/8.5 observations, but says no framework or Akamai signal is shown [32]. **Decision:** mark the claimed Akamai layer as unverified rather than treating it as fact.
- **No Official MUJ One Mobile App Was Located**: Google Play search material does not identify a MUJ One or official MUJ student portal application [33] [34], while located apps identify independent or third-party publishers [22] [22] [28] [28]. **Decision:** no public evidence currently links a mobile app backend to MUJ One.
- **Archive Evidence Shows Longevity, Not Continuous Development History**: Filtered Wayback indexes show MUJ One HTML captures from 2022-08-17 to 2024-08-28 [17], and SLCM captures from 2025-01-10 to 2026-08-05 [19]. **Decision:** use the dates as capture bounds only; do not infer deployment dates, migrations, or uninterrupted availability.

## Scope, Method, and Evidence Standard

This report is limited to public web pages, public DNS responses, certificate/archive indexes, public app-store records, and public passive scan results. It does not attempt authentication, password testing, endpoint enumeration behind login, exploitation, source-code retrieval, or any other activity that would require authorization. The report distinguishes four categories: **observed**, meaning directly exposed by a public source; **documented**, meaning stated in an official MUJ document; **inferred**, meaning a cautious interpretation of observed facts; and **unverified**, meaning a proposition for which the reviewed public evidence is insufficient.

The central analytical problem is entity separation. The user-supplied framing groups MUJ SLCM, MUJ One, Microsoft 365 identity, Azure, and Akamai into one ecosystem. Public evidence supports an ecosystem relationship, but not a single application or a single authentication plane. The two important hostnames expose materially different public surfaces: SLCM presents student and parent access, while MUJ One presents HR controls. That distinction is more reliable than the shared "MUJ" branding.

The evidence base also has important limits. Search indexing can expose pages that are not linked from official navigation, archive captures can be incomplete, and passive scanners can observe a hostname at a different time, path, or network edge. Consequently, a negative result means "not found in the reviewed public evidence," not proof that a feature does not exist.

## Exact Evidence Register

| Evidence item | Public source URL | What it establishes | Status |
|---|---|---|---|
| MUJ One HR login | https://mujone.jaipur.manipal.edu/HR/Login.aspx | HR branding, employee-oriented fields, CAPTCHA, policy controls, MAHE development attribution [4] | Observed |
| MUJ One root/HR page | https://mujone.jaipur.manipal.edu/HR/ | HR branding, PAS Portal link, reset controls, employee-code and DOB fields [6] | Observed |
| MUJ SLCM root | https://mujslcm.jaipur.manipal.edu/ | MUJ Portal branding and @muj.manipal.edu identity label [3] | Observed |
| MUJ SLCM indexed academic path | https://mujslcm.jaipur.manipal.edu/Student/Academic/AttendanceSummaryForStudent | Publicly indexed student academic route returning the portal login surface [1] | Observed, route purpose inferred from path |
| MUJ SLCM FAQ | https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf | Registration URL, username pattern, Outlook-aligned password wording, support contacts [36] | Officially documented |
| MUJ Office 365 SOP | https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf | Microsoft login URL, university mail ID, password setup, mandatory MFA, Authenticator, Microsoft 365 access [21] [21] [21] | Officially documented |
| MUJ IT page | https://www.jaipur.manipal.edu/administration-it.php | Microsoft services, business ERP, student life-cycle web portal, and LMS in MUJ IT landscape [24] | Officially documented |
| MUJ One A record | https://dns.google/resolve?name=mujone.jaipur.manipal.edu&type=A | A record of 52.172.36.15 [37] | Observed |
| IP information | https://ipinfo.io/52.172.36.15/json | Microsoft AS8075 attribution and Chennai/Tamil Nadu geolocation [23] | Observed; geolocation is not region proof |
| MUJ One Wayback CDX | https://web.archive.org/cdx/search/cdx?url=mujone.jaipur.manipal.edu/*&output=json&filter=statuscode:200&filter=mimetype:text/html&fl=timestamp,original,statuscode,mimetype&collapse=digest&limit=100 | Filtered HTML capture bounds [17] | Archive evidence |
| MUJ SLCM Wayback CDX | https://web.archive.org/cdx/search/cdx?url=mujslcm.jaipur.manipal.edu/*&output=json&filter=statuscode:200&filter=mimetype:text/html&fl=timestamp,original,statuscode,mimetype&collapse=digest&limit=100 | Filtered HTML capture bounds [19] | Archive evidence |
| URLScan SLCM search | https://urlscan.io/api/v1/search/?q=domain:mujslcm.jaipur.manipal.edu | Public scan observations including IIS versions; no framework/Akamai proof [32] | Passive scan |
| Google Play MUJ One search | https://play.google.com/store/search?q=MUJ%20One&c=apps | No MUJ One result identified in reviewed result material [34] | Negative search result |
| Apple software search | https://itunes.apple.com/search?term=MUJ%20One&entity=software&country=in | Reviewed Apple results were not identified as MUJ One or an official MUJ student portal app [35] | Negative search result |

The table should be read as an evidence map, not as a claim that every source is equally authoritative. Official MUJ pages and documents carry the strongest weight for function and policy. DNS, IPinfo, archives, and URLScan are useful for infrastructure and historical observations, but they do not prove application ownership, logical architecture, or current deployment design.

## MUJ One: Purpose and Publicly Visible Login Flow

The strongest public-purpose signal for mujone.jaipur.manipal.edu is its own page title and form content. The page is labeled "MUJ HR SYSTEM" and exposes Email, Reset Password, Employee Code, Date of Birth, and CAPTCHA-related controls [4]. It also presents policy acknowledgement language for the Code of Conduct and Prevention of Sexual Harassment before sign-in [4]. The page identifies the developer as ISD/CSD, MAHE and recommends Google Chrome [4]. A related public page links to a PAS Portal [6].

These controls describe an employee or HR workflow much more directly than they describe a student single sign-on hub. Employee Code and Date of Birth are especially strong functional indicators because they are not generic portal branding; they are fields exposed in a password or account-recovery context [4]. The PAS Portal link is another organizational clue, although the public evidence does not explain whether PAS is an adjacent HR product, a performance-management system, or a legacy application [6].

**Inference:** MUJ One may be a broader HR entry point or a named application family with additional paths, but the reviewed public surface does not establish that. The fact that a hostname contains "mujone" is not sufficient to infer that it is a university-wide SSO broker. The public page does not show a Microsoft login button, an Entra tenant identifier, an OAuth authorization endpoint, a SAML issuer, or a mobile application callback.

The safest security-club classification is therefore "HR-facing web application, possible application-family hostname, SSO role unverified." This avoids conflating a public hostname name with an architectural role. It also prevents a common OSINT error: treating a domain label such as "One" as evidence of single sign-on.

## MUJ SLCM: Student Lifecycle Function and Login Flow

The SLCM surface is different. The page is branded "WELCOME TO MUJ PORTAL" [3]. It exposes Sign In and Sign In Parent Login controls [3] [3] and shows the @muj.manipal.edu account label [3]. A related hostname variant exposes @jaipur.manipal.edu [5]. The public index also includes an academic attendance path, although unauthenticated access returns the portal login surface rather than student records [1].

MUJ's official SLCM FAQ is more useful than the page title. It names https://mujslcm.jaipur.manipal.edu/ as the registration link [36]. It describes a username using a name and registration-number pattern and says the password is according to the official Outlook ID [36]. It also refers to AMS login support and separately discusses a MUJ Outlook account not working [36]. This is direct evidence that SLCM registration, AMS support, and Outlook identity are operationally related in MUJ's student onboarding process.

The public login snapshot also shows a POST form with an anti-forgery request-verification token and username/password controls, together with jQuery 1.10.2 and validation scripts [3]. This is useful fingerprint evidence of a server-rendered form and a conventional web authentication flow. It is not proof of the backend framework version, identity protocol, or authorization design. The visible form and client-side scripts cannot establish whether a server later redirects to Microsoft, validates locally, calls an API, or performs a hybrid process.

**Inference:** SLCM appears to be the student/parent lifecycle portal, and the Outlook relationship appears to be credential or account provisioning coupling. **Unverified:** public evidence does not prove that SLCM delegates authentication to Microsoft Entra ID. A shared password convention, a password-reset link, and a Microsoft 365 account can exist without SAML, OAuth, or OpenID Connect federation.

## Microsoft 365 Integration: What Is Documented and What Is Not

MUJ's official IT page says the MUJ IT landscape includes Microsoft services for communication and business ERP, a student life-cycle web portal, and a leading learning-management system [24]. This establishes that Microsoft and student lifecycle systems are both recognized components of the institutional IT environment. It does not say they share a tenant, use the same sign-in session, or exchange tokens.

The MUJ Office 365 SOP is explicit about the Microsoft 365 flow. It directs users to https://login.microsoftonline.com/ and says to enter a University Mail ID, then a current or temporary password [21]. It states that MFA is mandatory and must be completed before Office 365 can be used [21]. The documented methods include Microsoft Authenticator, phone SMS, and an additional email method [21]. The SOP identifies students and employees as its audience and labels itself Version 1.0, effective June 2025 [21].

The SLCM FAQ independently connects the SLCM password to the official Outlook ID [36]. A public SLCM login snapshot also shows a password-reset link to Microsoft's password-reset service [3]. Taken together, these sources support a practical identity relationship: MUJ student accounts and SLCM credentials are expected to align with Outlook/Microsoft identity operations.

They still do not prove SSO. The missing evidence would be an observed redirect to login.microsoftonline.com during an authorized, ordinary login; a documented SAML/OIDC/OAuth integration; a Microsoft Entra enterprise-application record published by MUJ; or an official architecture document naming the trust relationship. None was found in the reviewed public sources. The correct conclusion is therefore "Microsoft 365 identity dependency or credential coupling: high confidence; federated SSO: low confidence/not publicly established."

## Hosting, DNS, CDN, and Technology Fingerprints

The public DNS A record for MUJ One returns 52.172.36.15 [37]. IPinfo identifies the address as AS8075, Microsoft Corporation, and places it in Chennai, Tamil Nadu, India [23]. This is consistent with Microsoft-controlled address space and an India geolocation. It does not independently prove an Azure resource type, the Azure South India region, the origin server, or the absence of an intermediary.

A DNS authority response also exposed Azure DNS nameservers in the authority material for the manipal.edu zone [38]. That supports use of Azure DNS for the zone or delegation context, but DNS hosting and application hosting are separate questions. A university can use Azure DNS while hosting a service elsewhere, and a Microsoft-owned address can front a service without exposing its logical application architecture.

Passive URLScan material for mujslcm.jaipur.manipal.edu reports observations on multiple scan dates and identifies Microsoft-IIS/10.0 and Microsoft-IIS/8.5 among the observed server indicators [32]. The same analysis states that the framework and Akamai are not shown [32]. This is the best public evidence located for an IIS-family fingerprint, but it should be treated as time- and path-specific. It cannot be safely converted into "IIS 10 everywhere" or into a framework version.

The user-supplied technology profile names ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 identity. Public evidence only partially overlaps that profile. The SLCM page exposes MVC-compatible-looking routes, server-rendered form controls, anti-forgery protection, and jQuery validation [3]. Those are consistent with an ASP.NET MVC-style application, but they do not identify MVC 5.3. No reviewed public source independently verifies .NET Framework 4.x, and no public source verifies Akamai for either target hostname. SecurityHeaders and HackerTarget attempts timed out rather than returning headers [11] [12] [13]. A timeout is a collection failure, not a security finding.

| Technology or infrastructure claim | Public evidence | Confidence | Correct wording |
|---|---|---:|---|
| Microsoft address space for MUJ One | A record and AS8075 attribution [37] [23] | High | Resolves to a Microsoft-owned ASN/address at observation time |
| Chennai/Tamil Nadu geolocation | IPinfo record [23] | Medium | Geolocated by IPinfo to Chennai, Tamil Nadu |
| Azure South India region | No region-specific public evidence located | Low | Not publicly verified |
| IIS family on SLCM observations | URLScan reports Microsoft-IIS/10.0 and 8.5 [32] | Medium | Observed in public scans; scope and currentness limited |
| ASP.NET MVC 5.3 | No direct public version evidence located | Low | Unverified |
| .NET Framework 4.x | No direct public version evidence located | Low | Unverified |
| Akamai front end | No Akamai signal in reviewed scan material [32] | Low | Unverified |
| Microsoft 365 account dependency | Official FAQ and SOP [36] [21] | High | Documented Outlook/Microsoft 365 relationship |
| Microsoft Entra federated SSO | No public redirect/protocol/architecture evidence | Low | Not publicly established |

## Mobile App and Backend Assessment

The public app evidence does not establish a MUJ One mobile client. Google Play search material reviewed for "MUJ One" and Manipal University Jaipur did not identify a MUJ One or official MUJ student-portal app [33] [34]. This is a bounded negative result: it means no such listing was visible in the reviewed public search output, not that an internal, delisted, region-restricted, or differently named app cannot exist.

Several adjacent applications were found. MUJ GO is listed by a third-party Android catalog with package identifier com.manipal.muj.go and features such as notice board, mess menu, faculty contacts, events, item sales, and cab sharing [18] [18]. The listing does not expose a publisher that can be verified as MUJ or show a MUJ One/SLCM link [18]. It is therefore a lead, not proof of an official university app.

MUJstella identifies itself as "Made for MUJ Students, by MUJ Students," lists developer Akshit Raj, and describes timetable, attendance, study resources, campus directory, and updates [22] [22] [22]. Its update notes mention an SLCM Portal Attendance and Timetable Tracker [22]. That wording suggests a student-facing integration or convenience feature, but it does not reveal an API endpoint, prove authorization design, or connect the application to MUJ One.

CampusAdda's Android listing names Campusadda Technologies Private Limited and describes food and student-lifestyle functions [27] [27]. Its iOS listing names Sujit Sonune and explicitly says the application is independent, developed by students, and not officially affiliated with MUJ [28] [28]. The MUJ Gym iOS listing names Gayatri Software Services as developer and describes a member-login gym application [26] [26] [26]. Its copyright notice does not, by itself, prove university ownership or a connection to SLCM [26].

**Conclusion:** no public evidence found in this review demonstrates that MUJ One is a mobile-app backend, that MUJ One exposes a public API for student apps, or that any located app is an official MUJ One client. Any stronger statement would be inference beyond the sources.

## Archive History and Change Interpretation

Wayback CDX material provides useful but incomplete history. The filtered MUJ One HTML index shows an earliest visible capture of 2022-08-17 for the root URL and a latest visible capture of 2024-08-28 for an HR login path [17]. A targeted record shows the 2024-08-28 login capture as a 302 response [15]. An archived login page from that period visibly contains Email, Forgot Password, Employee Code, Date of Birth, CAPTCHA, and Change Password controls [29] [29]. This indicates that the HR-facing public surface and its employee account-recovery concepts were present in the archived material.

The filtered SLCM HTML index shows an earliest visible capture of 2025-01-10 for /Home/Index and a latest visible capture of 2026-08-05 for the root URL [19]. Archived SLCM snapshots retain the "WELCOME TO MUJ PORTAL" and "Sign In" text [31] [30]. The index also shows captured assets under a keen theme path and font assets [10], which is a useful historical UI clue but not a server-framework version proof.

The archive queries were filtered to successful HTML material, collapsed by digest, and capped. Therefore, gaps between dates do not demonstrate downtime, redesign, or migration. Archive presence also does not prove that a page was reachable by every user or that its backend behavior matched the visible capture. The defensible use of this evidence is to establish public historical presence and visible continuity of branding, not to reconstruct a complete change timeline.

## Application-Security Interpretation for a University Security Club

The public evidence suggests two separate defensive review surfaces. First, SLCM is an identity-sensitive student and parent portal. Its public page reveals account-domain conventions, parent/student role distinctions, an attendance-related route, and an Outlook-aligned password model [1] [3] [36]. Second, MUJ One is an HR-facing system with employee recovery fields, CAPTCHA, policy acknowledgement, and a PAS Portal relationship [4] [6]. These surfaces likely have different data classes and role models even if they share institutional identity administration.

**Inference:** the highest-value governance question is not whether the hostname name implies SSO; it is whether account lifecycle, MFA coverage, session boundaries, and authorization are consistently enforced across student, parent, employee, and third-party application contexts. The public material does not permit testing those controls, and this report does not recommend attempting to do so without written authorization.

For a legitimate assessment, the club should request documented architecture and an approved test scope from MUJ. The request should ask the system owner to identify authoritative hostnames, data owners, identity providers, trust protocols, mobile clients, API gateways, CDN/WAF layers, logging boundaries, and test accounts. This is a governance recommendation, not an instruction to probe the systems. Public evidence alone cannot answer those questions reliably.

A second defensive priority is provenance. Third-party app listings use MUJ branding and may mention SLCM features, but at least one explicitly disclaims official affiliation [28]. The university should publish a canonical app directory and approved-developer list so students can distinguish official applications from independent services. This would reduce phishing, credential-reuse, and shadow-integration risk without requiring any technical access to the portals.

## Synthesis

Across **purpose**, MUJ One and SLCM diverge: MUJ One publicly presents HR and employee recovery functions, while SLCM presents student and parent portal functions [4] [1]. Across **identity**, both are adjacent to Outlook/Microsoft 365 operations, but SLCM has the stronger direct evidence because the official FAQ explicitly links its password to the official Outlook ID [36]. Across **architecture**, Microsoft hosting evidence is stronger than the claims of Azure South India, Akamai, or a single SSO hub [23] [37] [32].

Across **mobile scope**, the ecosystem is fragmented: MUJ GO, MUJstella, CampusAdda, and MUJ Gym occupy different functional or third-party positions, and CampusAdda explicitly disclaims official affiliation [18] [22] [28]. This is a meaningful tension. The existence of apps that mention MUJ or SLCM can create the appearance of a unified mobile ecosystem, while public evidence does not show that MUJ One is their backend or that the university operates them.

Across **time horizon**, archives establish that MUJ One had public HTML presence by 2022-08-17 and SLCM by 2025-01-10 in the reviewed filtered indexes [17] [19]. That history supports continuity of publicly visible services, but not continuity of code, identity protocol, hosting, or security posture. The most important divergence is therefore between **branding continuity** and **architectural continuity**: the former is evidenced; the latter is not.

The integrated conclusion is that MUJ has a connected identity and application ecosystem, but the public record does not justify collapsing it into one product. The defensible model is: SLCM is the student lifecycle portal; MUJ One is publicly an HR system; Microsoft 365/Outlook is an institutional identity dependency; mobile apps are mixed-provenance; Microsoft hosting is supported for the observed MUJ One address; and exact framework/CDN/SSO claims remain partly unresolved.

## Final Verdict

**Verdict: MUJ One is not publicly demonstrated to be the MUJ student single sign-on hub or a mobile-app backend.** The available public evidence more strongly identifies it as an HR-facing web application, while mujslcm.jaipur.manipal.edu is the publicly evidenced student/parent SLCM portal [4] [3].

**Confidence level: High for functional separation; high for Outlook/Microsoft 365 ecosystem coupling; medium for Microsoft-hosted IP attribution; low for federated SSO, Azure South India region, Akamai deployment, exact ASP.NET MVC/.NET versions, and mobile-backend linkage.** The confidence qualifiers follow the evidence: official MUJ pages and documents directly support the first two categories [24] [36] [21], while passive and search evidence do not establish the latter architectural claims [32].

The principal unanswered questions are: whether SLCM uses Entra federation or local validation against Outlook-aligned credentials; whether MUJ One has undocumented student-facing routes; whether any official mobile client uses either portal; what CDN/WAF sits in front of each hostname; and which exact framework/runtime versions are deployed. Those questions should remain explicitly **not publicly established** until MUJ publishes architecture evidence or an authorized assessment produces it.

## References

1. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Student/Academic/AttendanceSummaryForStudent
2. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
3. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
4. [
	MUJ HR SYSTEM
](https://mujone.jaipur.manipal.edu/HR/Login.aspx)
5. *Manipal University*. https://muj.slcm.jaipur.manipal.edu/
6. [
	MUJ HR SYSTEM
](https://mujone.jaipur.manipal.edu/HR/)
7. *Wayback Machine*. https://web.archive.org/web/*/https://mujslcm.jaipur.manipal.edu/
8. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=mujone.jaipur.manipal.edu/*&output=json&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&collapse=digest
9. *Wayback Machine*. https://web.archive.org/web/*/https://mujone.jaipur.manipal.edu/
10. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=mujslcm.jaipur.manipal.edu/*&output=json&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&collapse=digest
11. *api.hackertarget.com*. https://api.hackertarget.com/httpheaders/?q=mujone.jaipur.manipal.edu
12. *api.hackertarget.com*. https://api.hackertarget.com/httpheaders/?q=mujslcm.jaipur.manipal.edu
13. *Scan results for mujslcm.jaipur.manipal.edu*. https://securityheaders.com/?q=mujslcm.jaipur.manipal.edu&followRedirects=on
14. *Scan results for mujone.jaipur.manipal.edu*. https://securityheaders.com/?q=mujone.jaipur.manipal.edu&followRedirects=on
15. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=mujone.jaipur.manipal.edu/HR/Login.aspx&output=json&fl=timestamp,original,statuscode,mimetype
16. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=mujslcm.jaipur.manipal.edu/&output=json&fl=timestamp,original,statuscode,mimetype
17. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=mujone.jaipur.manipal.edu/*&output=json&filter=statuscode:200&filter=mimetype:text/html&fl=timestamp,original,statuscode,mimetype&collapse=digest&limit=100
18. *MUJ GO*. https://www.myandroid.org/apps/com-manipal-muj-go
19. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=mujslcm.jaipur.manipal.edu/*&output=json&filter=statuscode:200&filter=mimetype:text/html&fl=timestamp,original,statuscode,mimetype&collapse=digest&limit=100
20. *stat.ripe.net*. https://stat.ripe.net/data/whois/data.json?resource=52.172.36.15
21. *Standard Operating Procedure*. https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf
22. *Mujstella - Apps on Google Play*. https://play.google.com/store/apps/details?id=com.yourcompany.mujstellaapp&hl=en-US
23. *ipinfo.io*. https://ipinfo.io/52.172.36.15/json
24. *Head- Digital Infrastructure & Technology Services - Manipal University Jaipur*. https://www.jaipur.manipal.edu/administration-it.php
25. [
	MU SLcM
](https://slcm.manipal.edu/)
26. *‎Manipal University Jaipur Gym App - App Store*. https://apps.apple.com/in/app/manipal-university-jaipur-gym/id6757078406
27. *CampusAdda - Apps on Google Play*. https://play.google.com/store/apps/details?id=com.app.campusadda
28. [
      ‎CampusAdda - MUJ on the App Store
    ](https://apps.apple.com/us/app/campusadda-muj/id6465745096)
29. [
	MUJ HR SYSTEM
](https://web.archive.org/web/20240828092621id_/https://mujone.jaipur.manipal.edu/HR/Login.aspx?AspxAutoDetectCookieSupport=1)
30. *Manipal University*. https://web.archive.org/web/20250527044058id_/https%3A//mujslcm.jaipur.manipal.edu/
31. *Manipal University*. https://web.archive.org/web/20250110135954id_/https://mujslcm.jaipur.manipal.edu/Home/Index
32. *urlscan.io*. https://urlscan.io/api/v1/search/?q=domain:mujslcm.jaipur.manipal.edu
33. *Manipal University Jaipur - Android Apps on Google Play*. https://play.google.com/store/search?q=Manipal%20University%20Jaipur&c=apps
34. *MUJ One - Android Apps on Google Play*. https://play.google.com/store/search?q=MUJ%20One&c=apps
35. *itunes.apple.com*. https://itunes.apple.com/search?term=MUJ%20One&entity=software&country=in
36. *Frequently Asked Questions and Contacts for SLCM Registration*. https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf
37. *dns.google*. https://dns.google/resolve?name=mujone.jaipur.manipal.edu&type=A
38. *dns.google*. https://dns.google/resolve?name=mujone.jaipur.manipal.edu&type=CNAME
