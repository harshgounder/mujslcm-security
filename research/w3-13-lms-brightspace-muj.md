# MUJ SLCM and Brightspace Public-Exposure Assessment

## Executive Summary

This report records what public research supports about the MUJ SLCM and Online Manipal learning ecosystem, what remains unproven, and what a university security club can safely do with the evidence. It is limited to public pages, public DNS responses, public vendor documentation, and passive metadata. It does not recommend login testing, endpoint enumeration, credential use, exploit execution, or any other activity against MUJ or D2L systems.

The strongest finding is that MUJ's public learning login is a D2L Brightspace tenant. The login page identifies Manipal University Jaipur Centre for Distance and Online Education and exposes the label "Powered by D2L Brightspace" [3]. MUJ's public program site describes a fully online experience, an advanced learning management system, a student portal, and recorded classes [2].

Public DNS provides a more nuanced result than the initial premise. At the time of collection, `learning.onlinemanipal.com` resolves by CNAME to `muj.brightspace.com` [23]. A second hostname, `learner-mahe.onlinemanipal.com`, resolves by CNAME to `manipalonline.brightspace.com` [22]. The supplied evidence therefore supports two Brightspace-branded aliases, but not a single public CNAME chain in which the learning hostname passes through learner-mahe. The two Brightspace names resolve to the same two observed IP addresses in the collected DNS responses, but shared addresses alone do not prove tenant identity, application configuration, or data sharing [27][30][32].

A Microsoft identity footprint is publicly visible for the `muj.manipal.edu` namespace. Public Microsoft metadata identifies tenant ID `27282fdd-4c0b-4dfb-ba91-228cd83fdf71`, an issuer, WS-Federation metadata, and OAuth authorization and token endpoints [29][24]. This proves that the namespace publishes Microsoft identity metadata. It does not prove that Brightspace uses that tenant as its relying party, that a specific Brightspace application registration exists, that attribute mappings are correct, or that SSO succeeds. The public MUJ iLearn page instead shows a lead-capture and OTP flow, including "Verify OTP" and redirection to the university application portal [16].

The requested App Store callback-failure claim could not be independently verified. Searches and store-page inspection returned unrelated Manipal Hospitals applications and no confirmed Online Manipal education-app listing, package identifier, or callback-failure review [21]. It should therefore be retained as an unverified user-provided lead, not presented as an observed incident.

D2L's public API documentation demonstrates a broad, permissioned surface. It documents OAuth 2.0 authorization-code authentication, Brightspace authorization and token endpoints, bearer-token use over HTTPS, resource-specific scopes, and a fallback scope for routes without a specific scope [26]. Public route documentation covers users, grades, content, organization structure, courses, and calendar, with version and organization-unit parameters and role or scope checks [28][25][37][36][34][35]. These are documented capabilities, not evidence that MUJ has enabled every feature or that any unauthorised request succeeded.

The public Brightspace vulnerability record most directly relevant to this research is CVE-2021-43129. NVD describes an access-control issue involving the Brightspace "Disable Right Click" quiz setting; the public record gives a CVSS v3.1 score of 6.5, while its affected-version content is not shown in the collected page excerpt [14][12]. OpenCVE's Brightspace search reports one matching CVE and shows the record as updated on 2024-11-21 [14]. This does not establish that MUJ was affected, because the public evidence does not expose MUJ's Brightspace release level, feature configuration, or remediation state.

MUJ's own privacy policy is more useful for data-governance scope than for proving the exact contents of the Brightspace tenant. It says MUJ may collect personal information such as name, date of birth, citizenship, phone number, residential or mailing address, email address, and demographic information [17]. It lists sensitive categories including passwords, financial information, health information, sexual orientation, medical records, and biometric information [17]. It also describes automatic device, browser, IP, time-zone, cookie, page-view, and interaction collection [17]. D2L documentation separately shows that Brightspace can represent users, roles, local authentication, just-in-time provisioning, organizational units, content, assignments, grades, quizzes, questions, discussions, rubrics, attendance, email, LTI, virtual classrooms, portfolios, SCORM, activity feeds, calendars, and intelligent agents [9]. Capability is not confirmation of enablement.

## Scope, Evidence Standard, and Limitations

The assessment distinguishes four evidence levels:

| Evidence level | Meaning | MUJ example |
|---|---|---|
| Directly observed public fact | A public page or resolver response states the fact | The MUJ login page says Powered by D2L Brightspace [3] |
| Vendor capability | An official D2L document says the product supports a feature | D2L documents content, grades, users, sessions, and other data sets [9] |
| Correlated infrastructure evidence | Public DNS or identity metadata shows a relationship, but not application configuration | learning.onlinemanipal.com points to muj.brightspace.com [23] |
| Inference or unverified lead | A conclusion not established by the collected public evidence | The supplied Akamai/IIS/.NET fingerprint and App Store callback allegation |

The research did not attempt to bypass authentication, submit credentials, call undocumented APIs, scan ports, manipulate parameters, test access controls, or retrieve student records. That limitation is both methodological and ethical. D2L's vulnerability disclosure policy says researchers should avoid privacy violations, production disruption, and data destruction or manipulation [10]. It also says customer-instance testing requires authorization from the associated customer, excludes connected services unless expressly listed, and prohibits denial-of-service, social-engineering, and other non-technical testing [10].

A second limitation is temporal. DNS is dynamic, and vendor release documentation changes. The DNS observations in this report are snapshots from the collected public resolver responses, not a guarantee of future resolution. Likewise, a Brightspace version cannot be inferred from the public login page or the existence of a CNAME.

## MUJ SLCM Public Boundary

The public SLCM page is a login boundary rather than a data disclosure. It presents "WELCOME TO MUJ PORTAL," "Sign In," and "Sign In Parent Login" [1]. A related public result presents a student-login label [41]. No public page collected in this research exposes student records, course data, administrative screens, or authenticated content.

The supplied research brief identifies ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365. Those values should not be treated as independently confirmed by this report. The Wappalyzer corpus page returned no named technology, version, hosting/CDN, or date evidence for the target [13]. URLscan evidence showed certificate-transparency discovery of the hostname, including a recorded hostname and date, but no hosting or technology identification [15]. A passive raw-markup check found ordinary stylesheet and JavaScript references but no explicit ASP.NET, MVC, .NET, IIS, or Akamai marker in the returned excerpt [42].

| SLCM observation | Public result | Assessment |
|---|---|---|
| Portal identity | MUJ Portal and Manipal University labels [1] | Confirmed public branding |
| Authentication boundary | Sign In and Parent Login are visible [1] | Confirmed unauthenticated boundary |
| ASP.NET MVC 5.3 | Not present in collected Wappalyzer/markup evidence [13][42] | Unverified input lead |
| .NET Framework 4.x | Not present in collected evidence [13][42] | Unverified input lead |
| IIS 10 | Not present in collected evidence [13][42] | Unverified input lead |
| Akamai | Not present in collected evidence [13][42] | Unverified input lead |
| Certificate transparency | URLscan records the hostname as discovered through CT logs [15] | Confirmed passive observation |

The defensive implication is straightforward: the portal should be treated as an identity and student-service boundary, but public branding does not identify its backend stack. Security-club reporting should avoid turning a scanner label into a confirmed software inventory item unless the operator or a reproducible public source confirms it.

## Brightspace Tenant Scope and DNS Relationships

The MUJ learning login provides direct product attribution. Its extracted public content includes "Login - Manipal University Jaipur," "Username," "Forgot your password?," and "Powered by D2L Brightspace" [3]. The MUJ Online site connects the public program brand to MUJ offerings such as MBA, BBA, MCA, and BCA and describes an advanced LMS and student portal [2].

The DNS results add tenant-alias evidence:

| Hostname | Record observed | Target or address | What it supports |
|---|---|---|---|
| learning.onlinemanipal.com | CNAME, TTL 3600 [23] | muj.brightspace.com | MUJ-branded Brightspace alias |
| learner-mahe.onlinemanipal.com | CNAME, TTL 600 [22] | manipalonline.brightspace.com | MAHE-branded Brightspace alias |
| muj.brightspace.com | A records, TTL 60 [30] | 13.55.178.159; 15.134.178.12 | Current address response |
| manipalonline.brightspace.com | A records, TTL 60 [32] | 15.134.178.12; 13.55.178.159 | Current address response |

The key inference is that the aliases appear operationally related because the collected A responses contain the same two addresses. That is an inference, not proof of shared application tenancy, shared storage, or shared authentication. The data also does not prove that `learning.onlinemanipal.com` is chained through `learner-mahe.onlinemanipal.com`; the observed CNAME targets are different.

No public evidence collected here reveals the MUJ org-unit IDs, enabled tools, tenant administrator settings, enrolment rules, LTI registrations, or student population. A public page's `/d2l/home/14042` or `/d2l/home/14201` path should not be interpreted as proof that those numbers are course, tenant, or security identifiers; the public evidence only shows the login page and branding.

## Microsoft Identity and SSO Assessment

Microsoft metadata for `muj.manipal.edu` is public. The federation metadata identifies a tenant ID and issuer and describes claims including name, email, groups, roles, object identifier, and tenant information. The OpenID configuration identifies the same tenant and exposes authorization and token endpoints [24].

| Identity artifact | Publicly observed evidence | Security interpretation |
|---|---|---|
| Namespace | `muj.manipal.edu` federation and OIDC metadata URLs [29][24] | MUJ namespace publishes Microsoft identity metadata |
| Tenant | `27282fdd-4c0b-4dfb-ba91-228cd83fdf71` [24] | Tenant identifier is public metadata, not a secret |
| Issuer | `https://sts.windows.net/.../` [24] | Public issuer metadata |
| Protocol metadata | WS-Federation metadata plus OAuth/OIDC endpoints [24] | Multiple Microsoft federation/protocol descriptions exist |
| Brightspace relying party | Not shown in collected metadata | Not publicly confirmed |
| Successful Brightspace SSO | Not observed | Not publicly confirmed |
| Attribute/role mapping | Not observed | Not publicly confirmed |

The correct conclusion is therefore "Microsoft identity integration is plausible and namespace-level metadata is confirmed, but Brightspace SSO is not publicly proven." A separate public iLearn page documents OTP verification, contact consent, and redirection to a university application portal [16]. It does not name Microsoft, Entra ID, Brightspace, SAML, or OpenID Connect.

The App Store callback-failure allegation remains unresolved. The public store search returned no confirmed Online Manipal education application or review text; the returned Manipal Hospitals listings are different products [21]. Generic search results about callback errors refer to unrelated software documentation and cannot be attributed to MUJ [43][44]. The report should therefore say: no public corroboration found, rather than claim that callback failures occurred.

## Brightspace API Surface

D2L's official documentation says Brightspace APIs use OAuth 2.0 and describes the authorization-code workflow, the Brightspace authorization endpoint, the token endpoint, and bearer-token presentation over HTTPS [26]. It also explains that specific scopes authorize API actions while the calling user's role and organization-unit context determine what the user can do [26]. This separation is an important security property: possession of an application token is not equivalent to unrestricted student-data access.

| API family | Public route examples | Data/security significance |
|---|---|---|
| Users | `PUT /d2l/api/lp/(*version*)/users/(*userId*)/names`; user and session resources [28] | Identity attributes, sessions, roles, and user operations; scope and user context apply |
| Grades | Grade-object access and grade-value routes under `/d2l/api/le/(*version*)/(*orgUnitId*)/grades/` [25] | Grade objects, access, and final/current-user grade values |
| Content | Content root, due items, topics, completions, captions, and ordering routes [37] | Course materials, due work, progress, and content metadata |
| Organization structure | Organization info, primary URL, org structure, children, and org types [36] | Tenant/course hierarchy and org-unit metadata; permissions can produce 403 [36] |
| Courses | Source-course and course-offering routes [34] | Course templates, offerings, deployment, and source-course data |
| Calendar | Events, user events, org-unit events, create/delete, and access routes [35] | Scheduling and event data, subject to role permissions |
| Integrations and identity | Role mapping, global user mapping, LTI and related data-set families [28][9] | Potential federation and external-tool linkage, configuration dependent |

The route documentation repeatedly uses an API version and often an organization-unit ID. It also identifies OAuth scopes such as `users:userdata:update`, `grades:gradeobjects:read`, `grades:gradeobjects:write`, and `organizations:organization:read` [28][25][36]. These examples are useful for architecture review, but they are not permission bypasses and should not be used against MUJ without written authorization.

D2L's December 2025 release notes also mention new server-to-server authentication for Brightspace APIs [40]. That item establishes a documented product direction, not proof that MUJ has enabled server-to-server access. A responsible club exercise is to build a local mock Brightspace integration or review D2L documentation, not to request tokens or probe the MUJ tenant.

## Security Advisories and Deployment Relevance

The public Brightspace CVE inventory found one matching record: CVE-2021-43129. OpenCVE shows the identifier, Brightspace/D2L product association, a 6.5 Medium CVSS v3.1 score, and an update date of 2024-11-21 [14]. NVD describes the issue as a bypass of the Brightspace quiz "Disable Right Click" feature that permits print and copy functionality through the browser context menu [12].

| Advisory or control | Public evidence | Relevance to MUJ |
|---|---|---|
| CVE-2021-43129 | Quiz right-click control bypass; CVSS 6.5 Medium [14][12] | Conditional; MUJ version and feature use unknown |
| Affected-version detail | Not present in collected NVD excerpt [12] | Cannot map to MUJ release |
| D2L cloud updates | D2L says customers do not buy, install, or update the LMS; D2L handles updates [38] | Patch responsibility likely differs from self-hosted software, but contract/configuration must be confirmed |
| D2L infrastructure | D2L says AWS is its primary strategic cloud infrastructure provider [38] | Vendor-level context, not proof of MUJ data location |
| D2L safeguards | D2L describes secure connections, session controls, logging, configurable access settings, logical separation, testing, and third-party audits [8] | Vendor assurance, not an instance-specific audit |
| Release process | D2L release notes say functionality and configuration can change before release [18] | Configuration and feature availability must be tracked over time |

The CVE is not evidence of an active MUJ vulnerability. A meaningful mapping would require an authorized source such as MUJ's vendor-support record, a contractual D2L security bulletin, a confirmed tenant release version, or a sanctioned assessment. The safe recommendation is to ask the service owner whether the relevant quiz setting is used and whether D2L's remediation was inherited through the managed service.

## Student Data: Confirmed Policy Scope Versus Brightspace Capability

MUJ's privacy policy says it describes how MUJ collects, uses, shares, and processes personal information [17]. It says the exact kind of information depends on the products or services used [17]. Its examples include identity, contact, address, demographic, and citizenship information [17], while its SPDI examples include password, financial, health, medical, sexual-orientation, and biometric information [17]. The presence of a category in the policy does not prove that every category is stored in Brightspace.

| Data category | Public MUJ policy evidence | Brightspace capability evidence | Status for MUJ Brightspace |
|---|---|---|---|
| Identity/contact | Name, date of birth, citizenship, phone, address, email, demographics [17] | Users and role-related data sets [9] | Policy-supported; tenant storage not individually confirmed |
| Credentials/authentication | Password listed as SPDI [17] | Local Authentication and JIT Provisioning data-set families [9] | Capability/policy-supported; implementation unknown |
| Financial/payment | Financial information listed as SPDI [17] | No collected evidence proves Brightspace payment storage | Do not assume Brightspace holds payment-card data |
| Health/biometric/sensitive | Health, medical, sexual-orientation, biometric examples [17] | No collected evidence maps these fields to Brightspace | Policy category only |
| Course materials and progress | MUJ site describes LMS, portal, and recorded classes [2] | Content, assignments, grades, quizzes, questions, discussions, rubrics, attendance [9] | Product capability and public service description; enablement not proven |
| Sessions and access logs | MUJ policy describes browser, IP, time zone, cookies, pages, interactions [17] | Session History includes session ID, org ID, user ID, UTC start/end, last access, timeout, and history ID [9] | Brightspace capability; MUJ retention/configuration unknown |
| Device/app access | MUJ policy describes device and browser data [17] | System Access includes source, app version, device, offline mode, and IP address [9] | Brightspace capability; actual collection depends on use/configuration |
| Communications/integrations | MUJ policy permits legitimate-business sharing with vendors [17] | Email, LTI, virtual classroom, portfolio, SCORM, activity feed, calendar, intelligent-agent families [9] | Potential integrations; no MUJ enablement proof |

Brightspace's Session History data set is particularly concrete. It contains login-session histories for all users in an organization, does not include app usage, and includes identifiers and UTC timestamps [9]. The System Access Log captures access from a browser, Pulse, or Brightspace Parent and Guardian, and may include source, app version, device, offline mode, and IP address [9]. These are product-level data definitions, not a claim that MUJ has enabled every source or retained every field.

MUJ says it may share PI and SPDI with service providers and other parties for legitimate business purposes [17]. It says sites are hosted on AWS servers in India and Singapore and that hard copies are held in India [17]. It also states that internet transmission and electronic storage are not 100% secure [17]. The policy provides user choices to review or correct information, decline requested information, withdraw consent in writing, and opt out of promotional communications [17].

## Defensive Priorities for a University Security Club

| Priority | Safe activity | Expected output |
|---|---|---|
| 1. Asset and ownership validation | Maintain a passive inventory of public hostnames, official login pages, vendor pages, and resolver snapshots | Evidence-backed asset register, with observation dates |
| 2. SSO assurance | Ask the service owner for the sanctioned Brightspace relying-party configuration, redirect URI inventory, claims mapping, MFA policy, and deprovisioning process | Configuration review without touching student accounts |
| 3. API governance | Review registered applications, scopes, token lifetime, service-account ownership, rotation, logging, and least privilege using administrative evidence | Permission matrix and token-governance checklist |
| 4. Data minimization | Map each MUJ policy category to the actual system of record and retention schedule | Data-flow and retention register |
| 5. Vendor assurance | Request D2L release, incident, vulnerability, and shared-responsibility documentation through MUJ procurement or IT | Deployment-specific risk decision |
| 6. Responsible disclosure | Use D2L's disclosure process only with the required customer authorization for customer-instance testing [10] | Coordinated report, no data collection |
| 7. Student privacy | Avoid collecting real student data in demonstrations; use synthetic identities and local mocks | Reproducible training material without privacy exposure |

The most valuable club project is not probing the portals. It is producing a control map: which identity provider provisions which account, which service owns the authoritative student record, what Brightspace scopes are approved, how grades and submissions are retained, and how a student is deprovisioned across SLCM, Microsoft identity, and Brightspace.

## What Is Still Unanswered

| Question | Current answer | Why it remains unanswered |
|---|---|---|
| Is the supplied SLCM stack fingerprint accurate? | Not independently confirmed | Public Wappalyzer, URLscan, and raw-markup evidence did not show the named versions or CDN [13][15][42] |
| Does learning.onlinemanipal.com chain through learner-mahe? | No; different CNAME targets were observed | DNS showed learning -> muj.brightspace.com and learner-mahe -> manipalonline.brightspace.com |
| Does Brightspace use the MUJ Microsoft tenant? | Not publicly proven | Tenant metadata exists, but no Brightspace relying-party configuration or successful SSO trace was collected [24] |
| Did an Online Manipal app have callback failures? | Unverified | Public store searches returned no confirmed education-app review; unrelated Manipal Hospitals results must be excluded [21] |
| Which Brightspace release runs for MUJ? | Unknown | Public login and DNS evidence do not expose tenant release information |
| Which tools are enabled for MUJ? | Unknown | D2L documentation lists capabilities, not tenant configuration [9] |
| What exact student records are in Brightspace? | Policy and product categories provide a bounded possibility set | No authenticated or administrative MUJ data inventory was public, and accessing one would require authorization |
| Where is MUJ Brightspace data stored? | MUJ policy says its sites are hosted on AWS in India and Singapore; D2L says AWS is its primary strategic provider [17][38] | These statements do not prove the specific Brightspace tenant's storage region or contractual arrangement |
| Is CVE-2021-43129 remediated for MUJ? | Unknown | MUJ release/configuration and remediation records were not public [14][12] |

## VERDICT

**Confidence level: Moderate for the public architecture map; low-to-moderate for deployment-specific security conclusions.**

High-confidence conclusions are that MUJ publicly exposes a SLCM login boundary, MUJ Online publicly identifies an advanced LMS, the MUJ learning page is powered by D2L Brightspace, `learning.onlinemanipal.com` currently aliases to `muj.brightspace.com`, and the separate MAHE-branded hostname aliases to `manipalonline.brightspace.com` [1][2][3][23][22]. High-confidence vendor findings include D2L OAuth/API patterns, permissioned resource families, Brightspace data-set capabilities, D2L disclosure restrictions, and the public CVE description [26][28][37][9][10][12].

Moderate-confidence conclusions are that the two Brightspace aliases may be operationally related because their collected A responses overlap, and that the public MUJ Microsoft tenant could be relevant to institutional identity. Both are inferences unless MUJ or D2L confirms the application configuration [27][24].

Low-confidence or unsupported conclusions are that the SLCM definitely runs the supplied ASP.NET MVC/.NET/IIS/Akamai stack, that Brightspace SSO definitely uses Microsoft accounts, that App Store callback failures occurred in an Online Manipal education app, that MUJ is affected by CVE-2021-43129, or that every D2L data category is enabled in this tenant. Those claims should remain explicitly unverified.

The decision for the security club is therefore: use the report as a passive architecture and data-governance baseline, and seek written authorization and operator-supplied configuration evidence before making any deployment-specific vulnerability claim.

## References

1. *Manipal University*. http://mujslcm.jaipur.manipal.edu/
2. *Online Bachelor and Master Programmes | Online Degree Programs in India | Online Manipal*. https://muj.onlinemanipal.com/
3. *Login - Manipal University Jaipur*. https://learning.onlinemanipal.com/d2l/home/14042
4. *Online Manipal | UGC Entitled Online UG & PG Degree Courses*. https://www.onlinemanipal.com/
5. *Privacy & Cookie Policy | MAHE*. http://manipal.edu/mu/important-links/privacy-and-cookie-policy.html
6. *Brightspace Data Sets and the Data Purge tool - Brightspace*. https://community.d2l.com/brightspace/kb/articles/4291-brightspace-data-sets-and-the-data-purge-tool
7. *Brightspace API Reference — Developer Platform (January 2026)*. https://docs.valence.desire2learn.com/reference.html
8. *LMS Security, Monitoring & Protection | D2L*. https://www.d2l.com/security/
9. *Sessions and System Access data sets - Brightspace*. https://community.d2l.com/brightspace/kb/articles/4537-sessions-and-system-access-data-sets
10. *D2L Vulnerability Disclosure Policy - Brightspace*. https://community.d2l.com/brightspace/kb/articles/23533-d2l-vulnerability-disclosure-policy
11. *Privacy Notice - D2L*. https://www.d2l.com/legal/privacy-notice
12. *NVD - CVE-2021-43129*. https://nvd.nist.gov/vuln/detail/CVE-2021-43129
13. *http://wappalyzer.com/lookup/mujslcm.jaipur.manipal.edu*. http://wappalyzer.com/lookup/mujslcm.jaipur.manipal.edu
14. *Brightspace CVEs and Security Vulnerabilities - OpenCVE*. https://app.opencve.io/cve/?product=brightspace&vendor=d2l
15. *http://urlscan.io/domain/mujslcm.jaipur.manipal.edu*. http://urlscan.io/domain/mujslcm.jaipur.manipal.edu
16. *iLearn Login - MUJ*. https://muj.onlinemanipal.com/ilearn-login
17. *Privacy Policy - MUJ*. https://muj.onlinemanipal.com/privacy-policy
18. *Release Notes Overview - Brightspace*. https://community.d2l.com/brightspace/kb/articles/5588-release-notes-overview
19. *Welcome — Developer Platform (January 2026)*. https://docs.valence.desire2learn.com/index.html
20. *Release Notes — Brightspace*. https://community.d2l.com/brightspace/categories/release-notes-en
21. *Online Manipal – Android Apps on Google Play*. https://play.google.com/store/search?q=Online%20Manipal&c=apps&hl=en_IN
22. *dns.google*. https://dns.google/resolve?name=learner-mahe.onlinemanipal.com&type=CNAME
23. *dns.google*. https://dns.google/resolve?name=learning.onlinemanipal.com&type=CNAME
24. *Openid Configuration*. http://login.microsoftonline.com/muj.manipal.edu/.well-known/openid-configuration
25. *docs.valence.desire2learn.com*. https://docs.valence.desire2learn.com/res/grade.html
26. *OAuth 2.0 authentication — Developer Platform (January 2026)*. https://docs.valence.desire2learn.com/basic/oauth2.html
27. *dns.google*. https://dns.google/resolve?name=learning.onlinemanipal.com&type=A
28. *docs.valence.desire2learn.com*. https://docs.valence.desire2learn.com/res/user.html
29. *login.microsoftonline.com*. http://login.microsoftonline.com/muj.manipal.edu/federationmetadata/2007-06/federationmetadata.xml
30. *dns.google*. https://dns.google/resolve?name=muj.brightspace.com&type=A
31. *dns.google*. https://dns.google/resolve?name=muj.brightspace.com&type=CNAME
32. *dns.google*. https://dns.google/resolve?name=manipalonline.brightspace.com&type=A
33. *dns.google*. https://dns.google/resolve?name=manipalonline.brightspace.com&type=CNAME
34. *Courses (course offerings, templates, schemas) — Developer Platform (August 2026)*. https://docs.valence.desire2learn.com/res/course.html
35. *Calendar (Events and scheduling) — Developer Platform (August 2026)*. https://docs.valence.desire2learn.com/res/calendar.html
36. *docs.valence.desire2learn.com*. https://docs.valence.desire2learn.com/res/orgunit.html
37. *docs.valence.desire2learn.com*. https://docs.valence.desire2learn.com/res/content.html
38. *LMS Cloud | Brightspace Cloud Based Learning Platform | D2L*. https://www.d2l.com/cloud
39. *NVD - Search and Statistics*. https://nvd.nist.gov/vuln/search/results?form_type=Basic&results_type=overview&query=D2L%20Brightspace
40. *December 2025/20.25.12 - Brightspace*. https://community.d2l.com/brightspace/kb/articles/33363-december-2025-20-25-12
41. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
42. *App Features | Book Appointment Online | Manipal Hospitals India*. https://www.youtube.com/watch?v=TiOeNFG_9tQ
43. *How to Catch/ Handle Error on the Supabase callback URL (OAuth)*. https://stackoverflow.com/questions/76861476/how-to-catch-handle-error-on-the-supabase-callback-url-oauth
44. *Error Codes | Supabase Docs*. https://supabase.com/docs/guides/auth/debugging/error-codes
