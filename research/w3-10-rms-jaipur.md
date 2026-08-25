# RMS Jaipur: Public Surface, Provenance, and Unknowns

## Executive Summary

This report examines the publicly observable research-management service at `rms.jaipur.manipal.edu`, its relationship to the Manipal University Jaipur (MUJ) SLCM ecosystem, and the limits of what can responsibly be concluded without authenticated access or intrusive testing. The assessment uses only public webpages, publicly indexed search results, official institutional documents, public DNS information, public routing/ASN information, and Internet Archive records. It does not attempt authentication, password testing, vulnerability exploitation, port scanning, enumeration beyond public indexing, or access to non-public records.

The most important finding is terminological. The target page explicitly calls itself **Research Data Management System**. That is the only expansion of RMS identified in the reviewed public material. The evidence does not support calling it a Result Management System, although the word “result” may be a reasonable hypothesis in a student-services context. That hypothesis should not be published as fact. The target also links to the MUJ IRINS research profile system and displays research-performance notices, which strongly supports a research-management interpretation. [6] [9]

The target presents a public login screen with `User Name`, `Password`, and the institutional suffix `@jaipur.manipal.edu`. It also displays a Chrome compatibility note and credits “MSIS and ISD, Manipal Academy of Higher Education” for design and development. [11] [11] [11] Those statements provide stronger evidence for institutional technical stewardship than for legal ownership of the host or the underlying application.

RMS appears related to, but not publicly proven to be technically identical with, MUJ’s SLCM and AMS ecosystem. The official SLCM FAQ identifies `https://mujslcm.jaipur.manipal.edu/` as the registration link, documents a username format based on a name and registration number, refers to the official Outlook identity, and directs AMS login problems to `dms@jaipur.manipal.edu` or `ams@jaipur.manipal.edu`. [2] The SLCM portal itself says “WELCOME TO MUJ PORTAL,” offers a sign-in surface, shows `@muj.manipal.edu`, and includes a parent-login option. [1] These are meaningful institutional connections, but no reviewed public source proves that RMS and SLCM share a database, authentication service, codebase, hosting stack, or trust boundary.

The technology evidence supports a **legacy ASP.NET Web Forms-style** assessment for at least some RMS pages. Public and archived material contains `.aspx` routes and `WebResource.axd` assets, while the public central RMS page exposes a form/postback-oriented implementation in raw markup. [5] [7] However, the reviewed evidence does not prove ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai use, a database platform, or a specific Microsoft 365 authentication protocol for the RMS host. Those values may describe another MUJ service, a historical scan, or an adjacent SLCM component; they should remain unverified for RMS.

The supplied network attribution is consistent with the target resolving to `202.131.155.153`. Public BGP and IP intelligence identify the announced `/24` as originated by AS134039 and associate that ASN with Ibus Virtual Network Services Private Limited. The reverse DNS name is `202.131.155.153.convergentindia.com`. [16] [7] [10] This identifies a network provider and routing context, not necessarily the application owner, campus, physical server, or security operator.

The public evidence shows no indexed RMS-specific complaint, breach report, or outage report in the searches conducted. That is a bounded negative finding, not proof that no complaints exist. MUJ does publish formal grievance mechanisms and named contacts, but those pages do not establish an RMS complaint. [12]

**Overall confidence:** high that RMS publicly means Research Data Management System; high that the target is institutionally associated with Manipal and MUJ; medium-high that MSIS/ISD are involved in technical development or maintenance; medium-high that the exposed pages use a legacy ASP.NET Web Forms-style architecture; medium for network attribution; low for the exact framework/runtime, IIS/Akamai deployment, database, authentication implementation, and legal hosting entity.

## Scope, Ethics, and Evidence Method

The objective was to characterize public exposure and provenance, not to test the security of the application. The evidence set consists of official MUJ and Manipal pages, public login pages, public support/documentation pages, search-indexed results, public DNS output, public routing data, and Wayback Machine records. A page was treated as primary evidence when it was hosted on an institutional domain or when it was an archive record of the target itself.

The report distinguishes three evidence categories. **Verified observation** means that the page or record explicitly states the fact. **Corroborated attribution** means that two or more public sources point in the same direction, such as the target’s footer and the central RMS page. **Inference** means a reasoned interpretation of technical or organizational clues that is not directly stated. Inferences are labelled explicitly and should not be converted into confirmed asset facts.

The requested “chain-of-thought” cannot be provided as private internal reasoning. The safe substitute is this reproducible methodology summary: identify the hostname; read its public root and login routes; compare official neighboring services; inspect only publicly returned markup and archive metadata; compare the target’s labels, links, footer, and dates; check public DNS and routing records; search exact and variant complaint phrases; and record both positive evidence and unresolved gaps.

The following source ledger provides exact URLs for the principal claims.

| Evidence ID | Source type | Exact URL | Main use |
|---|---|---|---|
| 41 | Current RMS homepage extraction | `https://rms.jaipur.manipal.edu/` | Public name, research purpose, MUJ IRINS link, notices |
| 44 | Current RMS login extraction | `https://rms.jaipur.manipal.edu/Login.aspx` | Login fields, suffix, footer, Chrome note |
| 38 | Official MUJ SLCM FAQ PDF | `https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf` | SLCM URL, identity and support guidance |
| 39 | Public SLCM portal | `https://mujslcm.jaipur.manipal.edu/Home/Index` | Public sign-in and parent-login surface |
| 88 | Central RMS page | `https://rms.manipal.edu/` | RMS workflow, support mailboxes, Outlook credential guidance |
| 43 | MUJ IRINS portal | `https://muj.irins.org/` | Research-profile function and public role-based logins |
| 36, 146 | Official MUJ pages | `https://www.jaipur.manipal.edu/` and `http://jaipur.manipal.edu/about-muj.php` | Institutional context |
| 90, 147 | Official recognition page | `http://jaipur.manipal.edu/recognition-accrediation.php` | Legal status and Act reference |
| 40 | Wayback CDX metadata | `http://web.archive.org/cdx/search/cdx?collapse=urlkey&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&output=json&url=rms.jaipur.manipal.edu/*` | Archived target URLs and timestamps |
| 87 | Archived RMS homepage | `https://web.archive.org/web/20240322052206/https://rms.jaipur.manipal.edu/` | Historical page and February 2024 notice |
| 174 | Archived RMS error page | `https://web.archive.org/web/20240828150521/https://rms.jaipur.manipal.edu/Error.aspx` | Historical error-page wording |
| 85 | Public BGP data | `https://bgp.he.net/ip/202.131.155.153` | ASN, prefix, provider and reverse DNS |
| 86 | Public IP intelligence | `https://ipinfo.io/202.131.155.153` | Range, ASN, hostname and broad geolocation |
| 42 | Official MUJ grievance page | `https://www.jaipur.manipal.edu/online-grevience-registration.php` | Complaint channels and named officials |

## What RMS Is and Who It Serves

The target’s own visible title is “Research Data Management System.” [6] Its homepage links to the MUJ IRINS portal and displays department-level research-performance notices. [6] The public evidence therefore supports a research administration or research information role, not a student examination-result portal. The alternative expansion “Result Management System” was not found in the target page, central RMS page, MUJ SLCM FAQ, or reviewed search results. The correct reportable position is: **RMS is explicitly branded as Research Data Management System; Result Management System is unverified.**

The central RMS page helps explain the functional scope. It provides separate contact routes for new RMS access, publication and article-processing-charge queries, grants and seed-money entries, open-access publication questions, funds received under grant projects, and intellectual-property queries. [15] It also says that a Useful Link folder is available under the Search tab. [15] Those functions are consistent with a research-management platform handling publication, funding, intellectual property, and research records.

The target is connected to the same research-information environment through its MUJ IRINS link. [6] The IRINS page identifies MUJ and provides public links for “Login as Nodal Officer” and “Login as Faculty.” [9] It also exposes research-oriented categories such as expert names, organizations, designations, expertise, scholarly resources, and department-wise citation impact metrics. [9] The link proves a public relationship between the RMS landing page and the MUJ research-profile service. It does not prove that IRINS is built by the same vendor or that RMS directly imports or exports IRINS records.

MUJ’s institutional context is also public. The official About page says that the Manipal Education and Medical Group includes Manipal Academy of Higher Education, Sikkim Manipal University, American University of Antigua, Manipal International University, and Manipal University Jaipur. [17] The same page says MUJ was launched in 2011 as a self-financed State Private University. [17] The official recognition page states that MUJ was established by Act No. 21 of 2011 of the State Legislature of Rajasthan as a State Private University under section 22 of the UGC Act. [14]

The operator question needs careful wording. The strongest direct evidence is not a corporate registry entry but the target footer: “Designed and Developed by MSIS and ISD, Manipal Academy of Higher Education.” [11] The central RMS page gives the same general design/development attribution, although its visible wording uses “CSD and ISD” on that page. [15] **Inference:** MSIS/ISD and related Manipal information-services personnel likely have technical stewardship or development responsibility. The evidence does not establish whether MAHE owns the software, whether MUJ operates a tenant of a centrally administered system, whether an external contractor maintains the code, or which legal entity controls the server account.

## Public Pages, Login Surface, and Documentation

The target has a publicly reachable root page and a publicly indexed `Login.aspx` route. The root and login page expose a title, a username field, a password field, and the institutional suffix `@jaipur.manipal.edu`. [6] [6] [6] This is a login screen, not evidence of authenticated access or of a successful login. No credentials were used or tested.

The page also contains a public Chrome compatibility note. [11] That is a usability statement, not a security control. The reviewed visible material does not state that multi-factor authentication, conditional access, CAPTCHA, rate limiting, account lockout, device trust, or federated authentication is enabled. The absence of a statement is not evidence that the control is absent; it only means that it was not documented on the public page.

The central RMS page is more informative than the Jaipur landing page about operational support. It directs new-access, publication, APC, and conference-entry questions to `help.rms@manipal.edu`; grants and seed-money questions to `grants.mu@manipal.edu`; open-access publication questions to `ioap.mahe@manipal.edu`; grant-funds questions to `uss.research@manipal.edu`; and IPR queries to `techtransfer.mu@manipal.edu`. [15] It says existing users with login problems should check whether their password has expired, reset it if necessary, and retry. [15] It also states that RMS uses the same login credentials as the Outlook account. [15]

That Outlook statement is important but limited. It indicates credential reuse or an identity relationship for the central RMS page. It does not prove that the Jaipur RMS hostname uses Microsoft Entra ID, Active Directory Federation Services, OAuth, SAML, OpenID Connect, or a particular Microsoft 365 tenant. The target’s Jaipur suffix and the SLCM FAQ’s Outlook wording show institutional identity conventions, but they do not reveal the protocol.

The public SLCM portal is a separate visible surface. It says “WELCOME TO MUJ PORTAL,” displays “Sign In,” shows `@muj.manipal.edu`, and includes “Sign In Parent Login.” [1] The official SLCM FAQ identifies the registration link as `https://mujslcm.jaipur.manipal.edu/`, gives an example username made from a name and registration number, says the password is as per the official Outlook ID, and provides the University Helpline `0141 - 3999100`. [2] For AMS login problems it lists `dms@jaipur.manipal.edu` and `ams@jaipur.manipal.edu`, together with named AMS extensions. [2]

| Public surface | Publicly visible function or clue | What it does not prove |
|---|---|---|
| `rms.jaipur.manipal.edu/` | Research Data Management System title, MUJ IRINS link, research notices | That RMS means Result Management System |
| `rms.jaipur.manipal.edu/Login.aspx` | Username/password screen and Jaipur identity suffix | Successful authentication or control effectiveness |
| `rms.manipal.edu/` | Research, publication, grants, IPR support and Outlook login guidance | That Jaipur RMS is technically identical to central RMS |
| `muj.irins.org/` | Faculty and nodal-officer research-profile functions | Shared codebase or direct integration |
| `mujslcm.jaipur.manipal.edu/Home/Index` | MUJ portal, sign-in and parent-login options | Shared RMS/SLCM database or authentication protocol |
| MUJ SLCM FAQ PDF | Registration URL, username/password guidance and AMS contacts | A complete RMS user manual or architecture document |

The documentation gap is therefore material. Public support instructions exist, but no reviewed source provides a complete end-user manual, data-flow diagram, role matrix, retention policy, API specification, security architecture, or incident-reporting procedure specifically for RMS.

## Technology and Network Attribution

The strongest technology evidence comes from target URLs and archived assets. The Wayback CDX record includes the target root, `Error.aspx`, a CSS file, image files, and two `WebResource.axd` JavaScript resources, all returned as successful public records in the archive metadata. [5] The public login route is `Login.aspx`, and the raw markup contains an `aspnetForm` form and ASP.NET-style controls. [11] These are classic indicators of ASP.NET Web Forms-era implementation.

**Inference:** the public RMS surface is likely an ASP.NET Web Forms application, or at least includes Web Forms pages. Confidence is medium-high because the route naming, WebResource handler, form naming, and archived assets are mutually consistent. This is not the same as proving a precise version. The evidence does not establish ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, SQL Server, Windows Server, or any current patch level.

The supplied MUJ ecosystem description mentions ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 identity for `mujslcm.jaipur.manipal.edu`. Those attributes should not automatically be transferred to `rms.jaipur.manipal.edu`. The target’s visible evidence points toward Web Forms-style pages, while MVC is a different application pattern. It is possible that the ecosystem contains multiple applications, legacy and modern components, or a front end and back end with different technologies. No public source reviewed here resolves that ambiguity.

The central RMS page’s public raw markup includes form-postback behavior and hidden state fields, but the extracted analysis did not find a direct framework version, IIS banner, proxy declaration, or database identifier. [15] [15] This reinforces the correct defensive conclusion: identify observable framework family, avoid asserting exact versions without a trustworthy fingerprint, and treat headers or scans from unrelated hosts as non-transferable.

The network record is similarly bounded. Public DNS output resolves `rms.jaipur.manipal.edu` to `202.131.155.153`. [16] Public BGP information shows `202.131.155.0/24`, origin AS134039, and the description “Ibus Virtual Network Services Private Limited.” [7] The page also gives the reverse-DNS name `202.131.155.153.convergentindia.com`. [7] IPinfo likewise associates the address with the `/24`, AS134039, Ibus Virtual Network Services Private Limited, and a Delhi, India location classification. [10]

| Network field | Public value | Interpretation |
|---|---|---|
| Target IPv4 | `202.131.155.153` | DNS answer for the target hostname |
| Announced prefix | `202.131.155.0/24` | Public routing range |
| Origin ASN | `AS134039` | Routing origin shown by BGP data |
| Network organization | Ibus Virtual Network Services Private Limited | Provider/ASN attribution, not application ownership |
| Reverse DNS | `202.131.155.153.convergentindia.com` | PTR-style hostname shown publicly |
| Broad location | Delhi, India | Database geolocation; not proof of physical server location |
| Hosted-domain count in BGP view | 0 | Tool output; not proof that no virtual hosts exist |

The user-supplied phrase “Ibus Jaipur ISP” should consequently be treated as a shorthand description, not as a fully verified legal or geographic conclusion. The public BGP evidence identifies Ibus Virtual Network Services Private Limited and the route; the reviewed data does not prove that the server is physically in Jaipur or that Ibus is the application operator.

## Archive Captures and Historical Change

The Wayback CDX record is valuable because it preserves target-specific historical metadata rather than merely a search-engine cache. It lists a root-page capture at timestamp `20240322052206`, an `Error.aspx` capture at `20240828150521`, CSS and image assets from August 2024, and two `WebResource.axd` JavaScript records from August 2024. [5]

The archived root page calls the service “Research Data Management System,” links to MUJ IRINS, and shows the same Jaipur username suffix and password field. [8] It also contains a February 2024 notice recognizing the Department of Biotechnology and Chemical Engineering for top research performance. [8] The current page contains later April and May 2025 departmental notices. [6] **Inference:** the service was publicly reachable and visibly maintained across at least the archived February 2024 and current 2025 notice periods. That does not prove uninterrupted availability.

The archived `Error.aspx` page shows “Research Data Management System,” “Logout,” “An Error Occurred!!!...Please contact the Admin for more details...” and “Go Back.” [18] This demonstrates that a generic error route was publicly archived. It does not reveal the triggering condition, indicate a vulnerability, or establish that an error remained present in the current application.

| Archive record | Timestamp | Publicly recorded item | Evidentiary value |
|---|---:|---|---|
| Root | 20240322052206 | RMS homepage | Historical name and research link |
| Error route | 20240828150521 | `Error.aspx` | Generic error-page continuity |
| Stylesheet | 20240820022205 | `Styles/Style.css` | Historical presentation asset |
| Images | 20240820022945, 20240820030139 | Two image paths | Historical page assets |
| Script resources | 20240820032243, 20240820042036 | `WebResource.axd` | Legacy Web Forms-style indicator |

The archive should not be mistaken for a complete change log. A capture records what the archive received, not every deployment, configuration change, or security state. It also does not prove that the current server uses the same binaries as the 2024 pages.

## Complaints, Grievance Channels, and Negative Findings

Exact-domain and variant searches for complaints, login problems, incidents, outages, and security reports returned the target pages, central RMS support pages, MUJ grievance pages, and unrelated or general portal results, but no indexed RMS-specific complaint or incident report. **Bounded negative finding:** no RMS-specific public complaint was located in the reviewed indexed material. This is not evidence that users have never complained, because complaints may be private, removed, unindexed, written under a different service name, or handled through internal support.

MUJ’s official grievance page provides a formal route to submit a grievance online and a route through the UGC Samadhaan portal. [12] It names Dr Pankaj Vyas as chair of the grievance committee and lists a contact number and email address; it also identifies Dr Kshama Agarwal as ombudsperson. [12] Those are escalation resources for the institution generally. The page does not state that any complaint concerns RMS. [12]

The distinction matters operationally. A support mailbox such as `help.rms@manipal.edu` is evidence of a support process, not evidence of a security incident. A generic error page is evidence of an error-handling route, not evidence of a breach. A public login screen is evidence of exposure of an authentication interface, not evidence of weak authentication.

## Risk Interpretation and Safe Defensive Recommendations

The public surface creates ordinary defensive priorities, but the evidence does not justify declaring a vulnerability. First, the institution should maintain an authoritative inventory linking each hostname to a service owner, legal entity, data classification, identity provider, hosting provider, and lifecycle status. This is especially important because RMS, SLCM, AMS, IRINS, DMS, and central Manipal portals use related branding but visibly different hostnames and identity suffixes.

Second, the owner should confirm whether the legacy Web Forms-style pages remain supported and patched. The public evidence shows `Login.aspx` and `WebResource.axd` indicators, but no version. A safe internal review should therefore verify framework and IIS versions from configuration management, not infer them from public routes. It should also confirm whether legacy pages are behind the same reverse proxy or CDN as SLCM. No external probing is necessary for this conclusion.

Third, the institution should document authentication boundaries. The central RMS page says RMS uses Outlook credentials. [15] Administrators should confirm whether that means direct directory validation, federation, or a separate synchronized credential store; whether MFA and conditional access apply; whether service accounts are excluded; and how password-expiry errors are handled. These are internal control questions, not assumptions about the implementation.

Fourth, public error handling should be reviewed for information disclosure. The archived error page is generic and does not itself expose stack traces. [18] The current public RMS publication route likewise returns a generic “Sorry,” “An error occurred,” and “Please re-try your action with proper data,” with a support email. [19] That is preferable to publishing exception details, but internal logs should still preserve diagnostic context while public responses remain generic.

Fifth, documentation should be improved. The public pages provide contacts and basic login guidance, but no visible data-flow or security documentation. A minimum internal package should include service owner, data types, user roles, authentication protocol, recovery process, logging owner, incident route, retention period, dependencies, and retirement plan. Public documentation should avoid publishing sensitive implementation details.

| Defensive priority | Evidence basis | Safe action |
|---|---|---|
| Asset ownership | Multiple related Manipal/MUJ hostnames and separate suffixes | Maintain a signed service inventory and owner map |
| Legacy lifecycle | `Login.aspx`, `WebResource.axd`, archived Web Forms-style assets | Verify versions internally and plan modernization or retirement |
| Identity boundary | Central RMS says Outlook credentials are used | Confirm federation, MFA, expiry, and recovery controls internally |
| Error handling | Public generic error pages | Preserve internal diagnostics while minimizing public detail |
| Documentation | Support guidance but no full public manual | Create internal architecture and operations documentation |
| Complaint handling | Official MUJ grievance routes | Map RMS support escalation to institutional incident response |

## Synthesis

Across five dimensions, RMS and SLCM should be treated as related institutional services rather than one confirmed application. **Scope** differs: RMS is explicitly research-management oriented, with publication, grants, APC, IPR, and research-profile links; SLCM is presented as a MUJ portal with student/parent sign-in and AMS registration guidance. [15] [1] **Mechanism** is unresolved: both expose institutional login patterns, but only the central RMS page explicitly says Outlook credentials are used, and no reviewed source proves that the Jaipur RMS and SLCM share an identity protocol. [15] **Technology** also diverges in evidence: RMS has strong legacy Web Forms-style indicators, while the supplied MVC/IIS/Akamai description for SLCM cannot be transferred to RMS without direct evidence. [5] [11]

**Ownership evidence** is stronger for technical stewardship than for hosting control. The RMS footer credits MSIS and ISD at MAHE, while MUJ’s official pages establish MUJ’s institutional status and relationship within the Manipal group. [11] [17] [14] The network records point to Ibus Virtual Network Services for the route, but a provider does not become the application owner merely because its ASN announces the address. [7] This is the central attribution tension: institutional branding and development credits identify the service context, while routing data identifies connectivity infrastructure.

**Evidence maturity** is uneven. Naming, public login exposure, support contacts, institutional context, and archive continuity are high-confidence findings. Framework version, reverse-proxy placement, Microsoft 365 protocol, database, legal hosting entity, and current security controls are low-confidence or unknown. **Trade-off:** a report that states the unknowns clearly is more useful to defenders than one that fills gaps with familiar technology labels.

The non-obvious finding is that the public surface is not primarily a student-results interface. The target’s own expansion, research notices, IRINS link, and central RMS workflow all point toward research administration. The strongest responsible conclusion is therefore that RMS is a Manipal research data-management service serving a Jaipur/MUJ context, with technical stewardship credited to MAHE information-services groups and network connectivity attributed publicly to Ibus Virtual Network Services. Direct integration with SLCM remains unproven.

## FINAL VERDICT

**Verdict:** `rms.jaipur.manipal.edu` is publicly identifiable as a **Research Data Management System** associated with Manipal’s research-information environment and MUJ’s Jaipur institutional context. It is not publicly established as a Result Management System. [6] [15]

**Confidence table:**

| Finding | Confidence | Reason |
|---|---|---|
| RMS expands to Research Data Management System | High | Explicit title on current and archived pages |
| RMS is research/publication-oriented | High | Central workflow notices and IRINS link |
| Public login screen exists | High | Current login route exposes username/password fields |
| MSIS/ISD have development or stewardship involvement | Medium-high | Explicit footer attribution |
| MUJ is a state private university established under Act No. 21 of 2011 | High | Official recognition page |
| IP is routed through AS134039/Ibus Virtual Network Services | Medium-high | Public BGP and IP intelligence agree |
| Legacy ASP.NET Web Forms-style surface | Medium-high | `.aspx`, `WebResource.axd`, and form markers |
| ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10 | Low/unverified | Not stated by reviewed target evidence |
| Akamai is in front of RMS | Low/unverified | Not established by reviewed evidence |
| Microsoft 365 protocol is used by RMS | Low-medium | Outlook credential wording exists, protocol is unstated |
| RMS and SLCM share a backend or identity service | Low/unverified | Institutional relationship exists, technical link absent |
| Public RMS-specific complaint found | None located | Search non-finding; not proof of absence |

The recommended security-club conclusion is to publish the confirmed identity, public login exposure, archive record, support/documentation gap, and bounded network attribution while explicitly labelling framework, CDN, authentication-protocol, database, and ownership claims as unresolved. Any further verification should be performed by the institution or with written authorization and should rely first on internal asset inventories, configuration records, logs, and vendor documentation rather than unauthorized testing.

## References

1. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
2. *Frequently Asked Questions and Contacts for SLCM Registration*. https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf
3. *Manipal University Jaipur - 71 years of legacy of Manipal Education*. https://www.jaipur.manipal.edu/
4. *Contact Us - Manipal University Jaipur *. https://www.jaipur.manipal.edu/contact-university.php
5. *web.archive.org*. http://web.archive.org/cdx/search/cdx?collapse=urlkey&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&output=json&url=rms.jaipur.manipal.edu/*
6. [
	RMS
](https://rms.jaipur.manipal.edu/)
7. *202.131.155.153 - bgp.he.net*. https://bgp.he.net/ip/202.131.155.153
8. [
	RMS
](https://web.archive.org/web/20240322052206/https://rms.jaipur.manipal.edu/)
9. *Manipal University Jaipur*. https://muj.irins.org/
10. *202.131.155.153 | Delhi, AS134039, VPN Not Detected | IPinfo*. https://ipinfo.io/202.131.155.153
11. [
	RMS
](https://rms.jaipur.manipal.edu/Login.aspx)
12. *Online Grievance Registration - Manipal University Jaipur *. https://www.jaipur.manipal.edu/online-grevience-registration.php
13. *Head- Digital Infrastructure & Technology Services - Manipal University Jaipur*. https://www.jaipur.manipal.edu/administration-it.php
14. *Recognition & Accreditations - Manipal University Jaipur *. http://jaipur.manipal.edu/recognition-accrediation.php
15. [

](https://rms.manipal.edu/)
16. *dns.google*. http://dns.google/resolve?name=rms.jaipur.manipal.edu&type=A
17. *About MUJ - Manipal University Jaipur*. http://jaipur.manipal.edu/about-muj.php
18. [
	RMS
](https://web.archive.org/web/20240828150521/https://rms.jaipur.manipal.edu/Error.aspx)
19. [
	RMS
](https://rms.manipal.edu/PublicationEntry/Reports/Login.aspx)
