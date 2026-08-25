# HMS Manipal OSINT Report: Identity, Exposure, and MUJ Separation

## Executive Summary

- **Service Identity**: Public pages and the administrative host explicitly identify HMS as the "Hostel Management System" and describe room and seat booking based on block selection, capacity, and availability. The evidence supports Hostel Management System, not Hospital Management System. [1]

- **Institutional Scope**: The public hms.manipal.edu landing page identifies Manipal, Health Science, Mangalore, and Bangalore campus hostel contacts and repeatedly references MAHE. It does not identify Manipal University Jaipur. [4]

- **MUJ Relationship**: MUJ SLCM is a different host and presents itself as the "MUJ Portal" with student and parent login options. The reviewed public material does not establish that hms.manipal.edu is part of MUJ SLCM or that the two applications share a database or authentication flow. [2]

- **Hosting**: A current public DNS response maps hms.manipal.edu to **20.44.49.205**, while IP metadata identifies that address as **AS8075 Microsoft Corporation**. [25][26] A public Shodan snapshot identifies the hostname and reports Microsoft Azure Application Gateway v2, with last-seen information dated 23 August 2026. [23]

- **Technology Attribution**: The exact IIS 10.0, ASP.NET MVC 5.3, and ASP.NET 4.0.30319 fingerprint is directly evidenced for MUJ SLCM, not for hms.manipal.edu. [11] The hms response exposes no server or framework version in the public header snapshot, so assigning MVC 5.3 to HMS would be an inference not supported by the collected evidence. [8]

- **Akamai Claim**: The collected evidence does not support the proposition that hms.manipal.edu is behind Akamai. The observed address is in Microsoft space, and the public host snapshot identifies Microsoft Azure Application Gateway v2. This does not prove that Akamai is never used elsewhere in the delivery path, but no public evidence located in this review demonstrates it. [26][23]

- **Identity Integration**: HMS publicly presents learner email, mobile OTP, employee authentication, application number, roll/registration number, and guest login labels. [3] A Microsoft tenant and federation metadata record exists for the muj.manipal.edu namespace, but the metadata itself does not state that hms.manipal.edu or MUJ SLCM uses a particular application registration.

- **Security Posture Snapshot**: An external SecurityHeaders snapshot dated 25 August 2026 reports grade A for hms.manipal.edu, IP 20.44.49.205, and the presence of X-Frame-Options, HSTS, CSP, X-Content-Type-Options, X-XSS-Protection, and X-Download-Options. It reports Referrer-Policy and Permissions-Policy as missing. This is a point-in-time third-party observation, not a penetration test or a guarantee of application security. [10]

- **Public Security Mentions**: The reviewed reports do not establish an HMS hostel compromise. An Open Bug Bounty record concerns manipal.edu.np and XSS, not hms.manipal.edu. A Brinztech report concerns the Manipal Library Portal, and LeakRadar expressly warns that its domain-level leak records do not mean the organisation's infrastructure was breached. [295.38, 295.41, 295.56, 295.85; 288.0-8; 293.13-18, 293.21-25, 293.52-58]

- **Decision**: Treat hms.manipal.edu as a MAHE hostel-management application hosted through Microsoft infrastructure. Treat MUJ SLCM as a related-brand but separately evidenced Jaipur student portal. Confidence is **high** for the HMS name and Microsoft hosting, **high** that hms is not proven to be the MUJ SLCM host, **medium** for the exact HMS backend technology, and **low** for any claim that HMS is behind Akamai or has a publicly documented security incident.

## Scope, Method, and Evidence Rules

This report uses public web pages, public DNS responses, public HTTP-header snapshots, public certificate/archive indexes, public search indexes, and public security-report pages. It does not attempt authentication, credential testing, parameter manipulation, directory brute forcing, vulnerability exploitation, source-code retrieval, or state-changing requests. The report therefore describes observable public evidence rather than asserting that an application is secure or insecure.

The requested "cot_explicit" field cannot be supplied as private chain-of-thought. Instead, this section gives an auditable summary of the analysis: first separate the hostname from the MUJ SLCM hostname; second prefer official pages for service identity and institutional scope; third use passive DNS and public telemetry for hosting; fourth distinguish directly observed headers from technology inference; and fifth test security claims for exact hostname and service matching. Each material conclusion below is labeled as either **Observed** or **Inference**.

There is also an important source-quality distinction. Official Manipal pages are strongest for naming, institutional purpose, hostel policy, and public contacts. DNS and IP metadata are strongest for current resolution and network attribution. Shodan and SecurityHeaders are useful passive observations but are snapshots collected by third parties. Search results and community posts can indicate how users experience a service but do not establish architecture or security defects.

## 1. What Does HMS Stand For?

### Direct public identity

The strongest direct evidence comes from the separate administrative hostname hms-admin.manipal.edu. Its public page uses the title "HMS" and explicitly expands the service as **HOSTEL MANAGEMENT SYSTEM**. It says that the web application enables room and seat booking according to block selection, room capacity, and availability. [1] That is a direct naming and function statement, not a technology guess.

The main hms.manipal.edu login page is titled Login and labels the service "Hostel Booking" in its public content. It provides an instruction for NEET-based programmes to use the MAHE registration number as the user ID. It also exposes labels for application number, roll/registration number, guest login, learner email login authentication, mobile OTP authentication, and employee login authentication. [3] These labels are consistent with a student-residence workflow and inconsistent with the hypothesis that HMS primarily means Hospital Management System.

The hms landing page describes the experience as "Your Home Away From Home" and includes a contact section directing users to hostel administration. [4] It lists campus-specific chief warden or hostel contacts for Manipal, Health Science, Mangalore, and Bangalore. [4] The visible public content is therefore residential and administrative, not clinical.

### Name assessment table

| Candidate expansion | Public evidence | Assessment | Confidence |
|---|---|---|---|
| Hostel Management System | Explicit expansion on hms-admin; room and seat booking description | Supported directly | High |
| Hostel Booking System | Login page labels the service "Hostel Booking" | Supported as a functional description | High |
| Hospital Management System | No reviewed HMS page describes patients, clinicians, appointments, wards, or hospital workflows | Unsupported by reviewed evidence | High |
| A shared MUJ hostel application | MUJ official hostel page and SLCM page do not name hms.manipal.edu | Not established | Medium-high |

**Takeaway:** The correct working expansion for this investigation is **Hostel Management System**. "Hospital Management System" should not be used in a security-club report except as a rejected alternative.

## 2. Publicly Visible Pages and Functions

The public surface is limited but informative. The main root and Home.aspx pages expose a landing page, campus information, and hostel-administration contact information. The login.aspx page exposes login-method labels. The administrative hostname exposes a separate sign-in page and a concise statement of booking functionality. A legacy host, hostel.manipal.edu/indexICAS.aspx, is also indexed as "Hostel Management System" and shows a login and CAPTCHA presentation. [121.0-32; 125.0-9; 124.1-9; 207.0-10]

A public Wayback CDX listing provides historical evidence of additional URL paths. The listed paths include the root, Authorization.aspx, Error1.aspx, Home.aspx, HostelPages/Atom_PayResponse.aspx, HostelPages/HDFCResponse.aspx, login.aspx, a session-expiry variant, CSS and JavaScript assets, and ScriptResource.axd/WebResource.axd. [15] These are historical or indexed paths, not a recommendation to request them. The presence of a payment-response path suggests that payment processing has existed in the application surface, but the record alone does not establish the payment provider, current availability, authorization behavior, or whether the route accepts state-changing input.

### Public page inventory

| Host or URL | Publicly observed purpose or label | Institution/campus signal | Evidence status |
|---|---|---|---|
| https://hms.manipal.edu/ | Hostel landing page; "Your Home Away From Home"; contact information | MAHE and multiple campuses | Direct observation |
| https://hms.manipal.edu/Home.aspx | Hostel landing/home content and campus contacts | Manipal, Health Science, Mangalore, Bangalore | Direct observation |
| https://hms.manipal.edu/Login.aspx | Hostel booking login; MAHE registration-number instruction; multiple login labels | MAHE registration reference | Direct observation |
| https://hms-admin.manipal.edu/ | HMS administration sign-in; room and seat booking description | manipal.edu identity label | Direct observation |
| https://hostel.manipal.edu/indexICAS.aspx | Legacy Hostel Management System login and CAPTCHA | MAHE copyright in indexed result | Direct observation from public page |
| https://hms.manipal.edu/Authorization.aspx | Historical authorization path | hms.manipal.edu | Historical archive record |
| https://hms.manipal.edu/HostelPages/Atom_PayResponse.aspx | Historical payment-response path | hms.manipal.edu | Historical archive record |
| https://hms.manipal.edu/HostelPages/HDFCResponse.aspx | Historical payment-response path | hms.manipal.edu | Historical archive record |
| https://mujslcm.jaipur.manipal.edu/Home/Index | MUJ Portal; student and parent login labels | @muj.manipal.edu | Separate application |

The table distinguishes current-looking public pages from historical archive records. A path appearing in an archive does not mean it is currently reachable, safe to access, or authorized for testing. The responsible conclusion is only that the path was publicly captured by the archive at the cited time.

## 3. MAHE Versus MUJ: The Central Attribution Question

The most important analytical issue is entity conflation. Manipal is a group with multiple institutions. The hms landing page names MAHE and gives campus contacts in Karnataka, including Manipal, Mangalore, and Bangalore. [4] The MAHE accommodation page describes student hostels and directs users to hostel-finance, notices, instructions, contact, and rules information by campus. [18]

MUJ is separately identified by its official Jaipur site as Manipal University Jaipur. The reviewed institutional material distinguishes MUJ in Jaipur from MAHE in Karnataka, while describing both as separate universities in the Manipal Education and Medical Group. [14] MUJ's own hostel page describes "MUJ Hostel" and world-class hostels on the Manipal University Jaipur campus. [16]

The MUJ SLCM portal is also separately branded. Its public page says "WELCOME TO MUJ PORTAL," presents sign-in and parent-login options, and uses the @muj.manipal.edu identity namespace. [2] Nothing on that public page names hms.manipal.edu. Conversely, the hms landing page does not name Jaipur or MUJ in its reviewed campus and contact content. [4]

### Institutional comparison

| Attribute | hms.manipal.edu | mujslcm.jaipur.manipal.edu | Conclusion |
|---|---|---|---|
| Public service label | Hostel / Hostel Booking | MUJ Portal | Distinct labels |
| Explicit institution | MAHE | MUJ / @muj.manipal.edu | Distinct public identity signals |
| Visible role | Hostel administration and booking | Student and parent portal sign-in | Different primary functions |
| Geographic signal | Manipal, Mangalore, Bangalore campuses | Jaipur namespace and MUJ branding | No public evidence of same campus service |
| Publicly evidenced shared login | Learner email, mobile OTP, employee authentication labels | Student and parent login labels | Shared identity not proven |
| Publicly evidenced shared backend | None | None | Unknown |

**Inference:** The two applications may belong to the same broader institutional technology ecosystem, but the reviewed public evidence does not justify calling hms.manipal.edu a MUJ SLCM component. The safe attribution is "Manipal-group-related, MAHE-oriented HMS" and "separate MUJ SLCM portal."

## 4. Hosting, DNS, Microsoft Space, and the Akamai Question

A public Google DNS response gives an A record for hms.manipal.edu with data value 20.44.49.205 and a 3,600-second TTL. [25] IPinfo identifies the same address as Chennai, Tamil Nadu, India, with organization AS8075 Microsoft Corporation. [26] The geographic field is geolocation metadata, not proof that the application or its operators are physically located in Chennai.

The public Shodan page for 20.44.49.205 identifies hms.manipal.edu as a hostname under manipal.edu and identifies Microsoft Corporation as the cloud provider or organization. Its public snapshot reports Microsoft Azure Application Gateway v2 and last-seen information of 23 August 2026. [23] The same snapshot records port 80 redirect behavior and an HTTPS response served by Microsoft-Azure-Application-Gateway/v2. [23]

This is consistent with the supplied "Microsoft space" characterization. It also changes how a researcher should interpret headers: a gateway can terminate TLS, redirect HTTP, add affinity cookies, and conceal the backend server banner. The public hms header snapshot includes ApplicationGatewayAffinityCORS and ApplicationGatewayAffinity cookies and does not expose values for Server, X-AspNet-Version, X-AspNetMvc-Version, or X-Powered-By. [8]

### Hosting evidence table

| Signal | Result | What it proves | What it does not prove |
|---|---|---|---|
| A record | 20.44.49.205 | Current observed hostname-to-address mapping | That the address is a dedicated origin server |
| IP organization | AS8075 Microsoft Corporation | Network metadata associates the address with Microsoft | That Microsoft operates the application or owns Manipal data |
| Shodan product | Microsoft Azure Application Gateway v2 | A public snapshot observed an Azure gateway response | The complete delivery path or backend architecture |
| PTR lookup | No PTR records found | No reverse hostname was returned by the cited lookup | That no other DNS or historical hostname exists |
| CNAME query | No CNAME answer; authoritative data references Azure DNS nameservers | The queried response did not provide a CNAME | That Azure DNS is the application host or origin |
| Akamai search | No hms-specific Akamai record located in this review | No positive evidence obtained | That Akamai is impossible somewhere upstream |

The Akamai conclusion must be carefully qualified. The evidence collected directly points to Microsoft Azure Application Gateway and Microsoft network space. The review did not locate a hostname, DNS alias, header, certificate, or passive record tying hms.manipal.edu to Akamai. Therefore, "behind Akamai" is **not publicly substantiated here**. It is not appropriate to state that Akamai is definitely absent from every possible upstream arrangement.

## 5. Technology Fingerprints: What Is Proven and What Is Not

The supplied MUJ SLCM fingerprint is directly reproduced by a public HTTP-header snapshot. The response is HTTP 200 and includes Server: Microsoft-IIS/10.0, X-AspNetMvc-Version: 5.3, X-AspNet-Version: 4.0.30319, X-Powered-By: ASP.NET, X-Frame-Options: SAMEORIGIN, a private cache directive, and an HttpOnly request-verification cookie. [11]

A second public snapshot reports the same stack for the MUJ SLCM address and identifies the MUJ host under Microsoft Corporation and AS8075. [27] A SecurityHeaders snapshot for MUJ reports grade D, IP 98.70.14.50, X-Frame-Options present, and HSTS, CSP, X-Content-Type-Options, Referrer-Policy, and Permissions-Policy missing at its report time. [9]

HMS is different. The current hms public header result shows HTTP 200, private cache behavior, Azure Application Gateway affinity cookies, ASP.NET_SessionId, SAMEORIGIN, HSTS, CSP, X-XSS-Protection, X-Content-Type-Options, and X-Download-Options. [8] It does not reveal the backend's version headers. The public hms HTML contains .aspx routes and a __VIEWSTATEGENERATOR field on Home.aspx. [121.0-32; 277.0] Those are compatible with ASP.NET Web Forms-style deployment, but they do not justify claiming a particular .NET Framework version or MVC version.

### Technology attribution table

| Technology claim | hms.manipal.edu evidence | MUJ SLCM evidence | Confidence |
|---|---|---|---|
| Microsoft network/cloud space | A record and IP metadata; Azure gateway snapshot | Microsoft organization and AS8075 snapshot | High |
| IIS 10.0 | Backend banner not exposed in hms header snapshot | Server: Microsoft-IIS/10.0 | High for MUJ; low for HMS |
| ASP.NET | .aspx pages, session cookie, ViewState-compatible field | X-Powered-By: ASP.NET | High for general HMS ASP.NET family; direct header proof stronger for MUJ |
| ASP.NET MVC 5.3 | Not exposed by hms snapshot | X-AspNetMvc-Version: 5.3 | High for MUJ only |
| .NET Framework 4.x | Exact HMS version not exposed | X-AspNet-Version: 4.0.30319 | High for MUJ only |
| Azure Application Gateway | Affinity cookies and Shodan product snapshot | Shodan/header snapshot for related MUJ host | Medium-high for hms edge |
| Akamai | No positive record located | No positive record relevant to hms | Low / unsubstantiated |

**Inference:** The hms edge likely masks or normalizes origin headers. That is a reason to avoid transplanting the MUJ SLCM fingerprint onto HMS, not a reason to assume the applications use different or identical frameworks.

## 6. Integrations and Authentication Signals

HMS exposes several authentication paths in its public login content: MAHE registration number for NEET-based programmes, application number, roll/registration number, guest login, learner email login authentication, mobile OTP authentication, and employee login authentication. [3] These labels show that the service is designed to accommodate multiple user populations and authentication mechanisms. They do not reveal whether those mechanisms are local, federated, or backed by Microsoft Entra ID.

The official MUJ SLCM page uses @muj.manipal.edu and offers student and parent login labels. [2] Public Microsoft OpenID metadata exists for the muj.manipal.edu namespace. It identifies tenant ID 27282fdd-4c0b-4dfb-ba91-228cd83fdf71, Microsoft authorization and token endpoints, an issuer under sts.windows.net, Microsoft Graph-related hosts, and supported user claims. [13] The federation metadata also describes tenant and user claims and WS-Federation endpoints associated with that namespace.

That metadata establishes the existence of a Microsoft identity namespace and its published protocol metadata. It does **not** establish that hms.manipal.edu uses a specific client ID, a specific redirect URI, MSAL, SAML, WS-Federation, or the same sign-in flow as MUJ SLCM. The metadata-reading result explicitly notes that it does not state that an SLCM application uses those identifiers or endpoints.

A separate official MAHE Research Data Management System page says RMS uses the same login credentials as the Outlook account. [17] However, that page does not say the statement applies to hms.manipal.edu. It would therefore be an attribution error to use RMS wording as proof of HMS Microsoft 365 integration.

### Integration evidence matrix

| Integration or linkage | Evidence | Status |
|---|---|---|
| HMS uses learner email as a login option | HMS public login labels | Directly observed |
| HMS uses mobile OTP as a login option | HMS public login labels | Directly observed |
| HMS supports employee authentication | HMS public login labels | Directly observed |
| MUJ has a Microsoft tenant namespace | OpenID/federation metadata | Directly observed |
| HMS uses the MUJ Microsoft tenant | No hms redirect, issuer, or client evidence located | Not established |
| HMS uses Outlook credentials | Only an unrelated/ separate RMS page makes that statement | Not established |
| HMS and MUJ SLCM share a backend | No public evidence located | Not established |
| HMS integrates payment services | Historical Atom/HDFC response paths and MUJ fee page evidence payment portals generally | Historical HMS path only; provider/current flow unknown |

## 7. Public Security Mentions and Defensive Observations

The strongest positive security observation for HMS is the third-party SecurityHeaders snapshot. It reports an A grade, capped at A, for hms.manipal.edu at 20.44.49.205 on 25 August 2026. [10] It lists X-Frame-Options: SAMEORIGIN, X-Content-Type-Options: nosniff, Strict-Transport-Security, Content-Security-Policy, X-XSS-Protection, and X-Download-Options as present. [10] It lists Referrer-Policy and Permissions-Policy as missing. [10]

The header content also matters. The hms snapshot exposes a CSP containing broad HTTPS source expressions and permits unsafe-inline and unsafe-eval for scripts, alongside SAMEORIGIN and HSTS. [8] These facts are observations, not a vulnerability finding. A header grade cannot assess authorization, business logic, session invalidation, payment integrity, account recovery, or data access controls.

The comparison with MUJ is useful but must not be overread. MUJ's snapshot receives D and lacks several modern response headers at that snapshot time. [9] The difference may reflect separate applications, separate edge configurations, or different scan conditions. It does not prove that HMS is secure or that MUJ is exploitable.

### Security-report triage table

| Public source | Exact affected target | Claim | Relevance to hms.manipal.edu |
|---|---|---|---|
| Open Bug Bounty | manipal.edu.np | XSS/CWE-79; patched; reported 11 October 2021 | Not an HMS report |
| Brinztech | Manipal Library Portal | Database exposure claim dated 18 February 2026 | Does not name HMS or hostel system |
| LeakRadar | General manipal.edu domain view | Published third-party leak records; warns they do not prove infrastructure breach | No specific HMS finding in reviewed text |
| SecurityHeaders | hms.manipal.edu | Grade A snapshot; missing Referrer-Policy and Permissions-Policy | Relevant passive posture snapshot, not a penetration test |
| URLScan search | hms.manipal.edu | Public search returned zero records | Absence of indexed scans, not evidence of safety |
| Wayback CDX | hms.manipal.edu | Historical public paths and assets | Reconnaissance context only; not a vulnerability finding |

The Open Bug Bounty record names manipal.edu.np, classifies the issue as XSS/CWE-79, and marks it patched, with a report date of 11 October 2021. [19] It does not name hms.manipal.edu. [19]

The Brinztech item names the Manipal Library Portal and describes a claimed database release on 18 February 2026. [20] The reviewed text does not name the HMS hostname or hostel system. [20] LeakRadar similarly warns that its domain-view material does not mean the organisation's infrastructure was breached, and says it indexes leaks already published by third parties, including possible info-stealer logs. [24] It is therefore unsuitable as proof of an HMS compromise.

## 8. MUJ Hostel Operations Versus HMS

MUJ's official hostel facility page describes hostels on the MUJ campus, including separate boys' and girls' hostels, security, room arrangements, medical support, mess, housekeeping, wardens, and maintenance. [16] It says hostel allotment follows fee deposit on a first-come-first-served basis and directs students to SpaceBasic for maintenance-related issues. [16] The official page also exposes a "Pay Fee Online" link. [16]

The official MUJ fee page states academic year 2026-27 figures for double occupancy: hostel accommodation Rs 167,372, housekeeping Rs 15,378, refundable security deposit Rs 25,475, and total including security deposit Rs 208,225. [22] It says payment modes are available through the room booking portal after login and that room allotment is confirmed after receipt and verification of full hostel fees. [22] Its explicit online-fee destination is https://jaipur.manipal.edu/pay-fee-online.php. [22]

Neither the reviewed MUJ hostel facility page nor fee page explicitly names hms.manipal.edu or the MUJ SLCM host. [255.78-79, 255.115; 290.90-97, 290.130] This does not prove that no internal integration exists. It means the public institutional pages do not document one. The contrast reinforces the attribution rule: MUJ hostel operations and MAHE HMS should be reported separately unless an official source explicitly links them.

## 9. Unanswered Questions and Safe Research Boundaries

Several questions remain unanswered because public evidence does not expose them. The exact HMS origin server framework and patch level are unknown. The observed gateway removes or leaves blank the usual server and ASP.NET version fields. [8] The historical presence of .aspx, ViewState-compatible content, and ASP.NET session behavior supports a broad ASP.NET inference, but not a precise version claim. [121.0-32; 277.0]

The current HMS payment provider is unknown. Historical archive paths include Atom_PayResponse.aspx and HDFCResponse.aspx, but path names alone do not prove a current integration, merchant configuration, or payment security posture. [15] The MUJ official fee page independently documents a room-booking portal and a Pay Fee Online destination, but does not connect those destinations to hms.manipal.edu. [22]

The relationship between HMS and Microsoft 365 is also unknown. HMS exposes learner-email and employee-authentication labels, while MUJ has a Microsoft identity namespace. [125.7-9; 208.0] No public evidence reviewed here shows an HMS redirect to login.microsoftonline.com, a client identifier, a tenant issuer in HMS configuration, or a Microsoft 365 credential statement specifically for HMS. The correct conclusion is "possible identity integration, not publicly verified."

Finally, no hms-specific vulnerability report was located in the reviewed public sources. That negative result is bounded: it means no matching report was found in the searched public indexes and pages, not that no private report, undisclosed incident, or vulnerability exists.

## Final VERDICT

**Overall confidence: High for service identity and broad institutional attribution; medium-high for Microsoft edge hosting; medium for the separation from MUJ SLCM; low for exact HMS backend technology and Akamai attribution.**

The most defensible final identification is:

> **hms.manipal.edu is a MAHE-oriented Hostel Management System / Hostel Booking application, publicly fronted by Microsoft-associated infrastructure at 20.44.49.205. It is not publicly demonstrated to be a hospital-management system, a MUJ SLCM component, or an Akamai-fronted service.**

The strongest facts are the explicit Hostel Management System label and room/seat booking description on hms-admin, the MAHE registration-number instruction and hostel login labels on hms, the DNS A record, Microsoft network attribution, and Azure Application Gateway observation. [124.1, 124.9; 125.2-9; 209.0; 222.0; 294.10-13, 294.24-25, 294.46]

The MUJ SLCM stack should be retained as a separate comparison dataset: its public headers directly expose IIS 10.0, ASP.NET MVC 5.3, ASP.NET 4.0.30319, ASP.NET, and SAMEORIGIN. [11] Those values should not be copied into an HMS technology claim. The Microsoft tenant metadata for muj.manipal.edu establishes a public identity namespace, but not HMS integration. [208.0; 291.0-2]

The security conclusion is deliberately limited. HMS presents a favorable third-party header snapshot with grade A and several standard defensive headers, but missing Referrer-Policy and Permissions-Policy. [10] There is no public, hostname-specific vulnerability or breach finding in the reviewed material. Unrelated reports involving manipal.edu.np, the Manipal Library Portal, or general domain-leak aggregation must not be relabeled as HMS incidents. [295.38-41, 295.56, 295.85; 288.0-8; 293.13-18, 293.52-58]

For a university security club, the decision-ready message is therefore: document HMS as a public MAHE hostel service; document MUJ SLCM as a distinct Jaipur student portal; record Microsoft hosting as observed; mark Akamai and shared Microsoft 365 authentication as unverified; and treat all security conclusions as passive-snapshot observations rather than authorization to probe the service.

## Exact-URL References

| Citation IDs used | Exact URL |
|---|---|
|,,,,,,, | https://hms.manipal.edu/ |
|,,,,,, | https://hms.manipal.edu/Login.aspx |
|,,,,, | https://hms.manipal.edu/Home.aspx |
|,,, | https://hms-admin.manipal.edu/ |
|,,,, | https://mujslcm.jaipur.manipal.edu/Home/Index |
|,,, | https://login.microsoftonline.com/muj.manipal.edu/.well-known/openid-configuration and http://login.microsoftonline.com/muj.manipal.edu/federationmetadata/2007-06/federationmetadata.xml |
| | https://dns.google/resolve?name=hms.manipal.edu&type=A |
| | https://dns.google/resolve?name=hms.manipal.edu&type=CNAME |
|, | https://api.hackertarget.com/reversedns/?q=20.44.49.205 |
| | https://ipinfo.io/20.44.49.205/json |
| | https://www.shodan.io/host/20.44.49.205 |
| | http://securityheaders.com/?followRedirects=on&q=https://hms.manipal.edu/ |
| | http://securityheaders.com/?followRedirects=on&q=https://mujslcm.jaipur.manipal.edu/ |
| | http://api.hackertarget.com/httpheaders?q=https://mujslcm.jaipur.manipal.edu/ |
| | http://api.hackertarget.com/httpheaders?q=https://hms.manipal.edu/ |
| | https://web.archive.org/cdx/search/cdx?collapse=urlkey&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&output=json&url=hms.manipal.edu/* |
| | https://jaipur.manipal.edu/hostel-facility.php |
| | https://jaipur.manipal.edu/hostel-fees.php |
| | https://www.manipal.edu/mu/campus-life/accommodation.html |
| | https://rms.manipal.edu/ |
| | https://www.openbugbounty.org/reports/2160625/ |
| | https://www.brinztech.com/breach-alerts/brinztech-alert-database-of-manipal-library-portal-leaked/ |
| | http://leakradar.io/en/report/manipal.edu |
| | https://hostel.manipal.edu/indexICAS.aspx |
| | https://jaipur.manipal.edu/ |

## References

1. *HMS*. https://hms-admin.manipal.edu/
2. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
3. *Login*. https://hms.manipal.edu/Login.aspx
4. *Hostel*. https://hms.manipal.edu/
5. *Hostel*. https://hms.manipal.edu/Home.aspx
6. *api.hackertarget.com*. https://api.hackertarget.com/reversedns/?q=20.44.49.205
7. *urlscan.io*. https://urlscan.io/api/v1/search/?q=domain:hms.manipal.edu
8. *api.hackertarget.com*. http://api.hackertarget.com/httpheaders?q=https://hms.manipal.edu/
9. *Scan results for https://mujslcm.jaipur.manipal.edu/*. http://securityheaders.com/?followRedirects=on&q=https://mujslcm.jaipur.manipal.edu/
10. *Scan results for https://hms.manipal.edu/*. http://securityheaders.com/?followRedirects=on&q=https://hms.manipal.edu/
11. *api.hackertarget.com*. http://api.hackertarget.com/httpheaders?q=https://mujslcm.jaipur.manipal.edu/
12. *2026 Prospectus Section 3 Hostel Fees.pdf*. https://www.manipal.edu/content/dam/manipal/mu/documents/Admissions/adm2026/2026%20Prospectus%20Section%203%20Hostel%20Fees.pdf
13. *Openid Configuration*. https://login.microsoftonline.com/muj.manipal.edu/.well-known/openid-configuration
14. *Manipal University Jaipur - 71 years of legacy of Manipal Education*. https://jaipur.manipal.edu/
15. *web.archive.org*. https://web.archive.org/cdx/search/cdx?collapse=urlkey&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&output=json&url=hms.manipal.edu/*
16. *MUJ Hostel - Manipal University Jaipur *. https://jaipur.manipal.edu/hostel-facility.php
17. [

](https://rms.manipal.edu/)
18. *Student hostels and accommodation | Manipal Academy of Higher Education*. https://www.manipal.edu/mu/campus-life/accommodation.html
19. *manipal.edu.np Cross Site Scripting vulnerability OBB-2160625 | Open Bug Bounty*. https://www.openbugbounty.org/reports/2160625/
20. *Brinztech Alert: Database of Manipal Library Portal Leaked*. https://www.brinztech.com/breach-alerts/brinztech-alert-database-of-manipal-library-portal-leaked/
21. *login.microsoftonline.com*. http://login.microsoftonline.com/muj.manipal.edu/federationmetadata/2007-06/federationmetadata.xml
22. *Hostel Fee - Manipal University Jaipur*. https://jaipur.manipal.edu/hostel-fees.php
23.(https://www.shodan.io/host/20.44.49.205)
24. *manipal.edu Data Breach Report | LeakRadar*. http://leakradar.io/en/report/manipal.edu
25. *dns.google*. https://dns.google/resolve?name=hms.manipal.edu&type=A
26. *ipinfo.io*. https://ipinfo.io/20.44.49.205/json
27.(http://shodan.io/host/98.70.14.50)
