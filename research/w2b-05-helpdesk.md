# MUJ SLCM Helpdesk OSINT Assessment: What Is Publicly Verifiable

## Executive Summary

- **Target-host attribution**: The ticketing vendor behind `helpdesk.jaipur.manipal.edu` cannot be identified from the public evidence reviewed. Freshworks is directly visible on `servicedesk.manipal.edu`, while osTicket is directly visible on `helpdesk.manipal.edu.my`; neither is the MUJ Jaipur hostname. [14] [15] [15] -> Do not label the target as Freshdesk, Zendesk, osTicket, or native without first-party confirmation.
- **Current public reachability signal**: Google Public DNS returned `Status: 3` and no Answer section for A, AAAA, and CNAME queries for the exact helpdesk hostname. [25] [26] [27] The result is a resolver observation, not proof that the service was permanently decommissioned. -> Treat the hostname as currently unresolved from this vantage point, while retaining the possibility of split DNS, a temporary record change, or an alternate access path.
- **Historical and passive visibility**: urlscan reports the exact hostname as not observed, with no direct hits, nothing hosted, no incoming hits, and nothing talking to the domain. [2] [2] A Wayback CDX request for the target returned an empty array. -> The public discovery footprint is very small.
- **Certificate contradiction**: Certificate-transparency data contains exact certificates for `helpdesk.jaipur.manipal.edu`, issued by Entrust DV TLS Issuing RSA CA 2 and valid from **2026-01-08** through **2027-01-08**. [21] -> A certificate proves that the name was included in a publicly logged certificate; it does not prove that DNS currently resolves or that an application is presently serving traffic.
- **SLCM is a separate, better-observed host**: The official MUJ onboarding guide identifies `https://mujslcm.jaipur.manipal.edu` as the Student Lifecycle Management portal and describes it as the one-stop platform for academic information. [13] [13] -> Keep SLCM observations separate from helpdesk observations.
- **Visible SLCM identity surface**: The public SLCM page exposes `Sign In`, `Parent Login`, `Student Login`, `Forgot Password?`, and an `@muj.manipal.edu` label. [4] -> These are visible UI labels only; they do not establish the complete authentication architecture.
- **Microsoft identity evidence**: A public urlscan result for the SLCM host records ASP.NET, Microsoft-IIS/10.0, and a link to `https://passwordreset.microsoftonline.com` titled `Forgot Password?`. [23] [23] -> This supports a Microsoft-associated password-reset integration, but it does not independently prove that all SLCM authentication is Microsoft 365 identity.
- **Official login and support workflow**: The onboarding guide says SLCM credentials are sent to the personal Gmail address supplied during admission, and directs technical issues or queries to the University Helpdesk or Admissions Department. [13] [13] -> The guide is the strongest public source for the intended support path, although it does not name the helpdesk hostname or vendor.
- **Knowledge-base result**: No MUJ helpdesk article about SLCM login problems was found. Public user discussions instead report an invalid-registration-number problem after intra-sliding and a password-error symptom. [6] [3] -> These are user reports, not official incident records or confirmed root causes.
- **API and attachment result**: No target-host API or attachment route was evidenced. Zendesk API routes found during research are official vendor documentation only, including article and attachment routes, and must not be treated as routes exposed by MUJ. [20] [19] -> Do not test or enumerate those paths on the target.

## Scope, Method, and Evidence Rules

This assessment uses public web search, public page extraction, public passive records, certificate-transparency material, public DNS-over-HTTPS responses, and publicly visible portal or forum text. It does not use credentials, password testing, active endpoint enumeration, vulnerability exploitation, directory brute forcing, unauthorized requests, or attempts to access private tickets or attachments. The phrase "not found" means "not found in the reviewed public evidence" unless a source expressly establishes a stronger condition.

The analysis distinguishes four evidence levels. **Direct evidence** is text or metadata returned by the named public source. **Corroborated evidence** is a finding supported by more than one independent public source. **Inference** is an analyst conclusion drawn from observations, and is labeled as such. **Unknown** means that the reviewed evidence does not support a conclusion. This distinction matters because a support platform may be configured behind a custom hostname, temporarily removed from DNS, restricted to authenticated users, or omitted from search indexes.

The central separation is between the target helpdesk hostname and the SLCM application hostname. The SLCM portal has direct public page and urlscan evidence. The helpdesk hostname does not. The presence of Microsoft IIS or a Microsoft password-reset link on SLCM cannot be transferred to the helpdesk, and a Freshworks page on another Manipal hostname cannot be transferred to MUJ Jaipur.

### Evidence inventory

| Evidence item | Exact public URL | Direct observation | Assessment value |
|---|---|---|---|
| Target helpdesk passive page | https://urlscan.io/domain/helpdesk.jaipur.manipal.edu | Not observed; no direct hits; nothing hosted; no incoming hits; nothing talked to the domain | Bounded negative for public urlscan visibility [2] [2] |
| Target helpdesk DNS A query | https://dns.google/resolve?name=helpdesk.jaipur.manipal.edu&type=A | Status 3; no Answer section shown | Current resolver observation [25] |
| Target helpdesk DNS AAAA query | https://dns.google/resolve?name=helpdesk.jaipur.manipal.edu&type=AAAA | Status 3; no Answer section shown | Current resolver observation [26] |
| Target helpdesk DNS CNAME query | https://dns.google/resolve?name=helpdesk.jaipur.manipal.edu&type=CNAME | Status 3; no Answer section shown | Current resolver observation [27] |
| Target helpdesk CT records | https://crt.sh/?q=%25.jaipur.manipal.edu&output=json | Exact helpdesk name in certificates, Entrust issuer, 2026-01-08 to 2027-01-08 validity | Historical/current certificate evidence [21] |
| Target helpdesk archive query | https://web.archive.org/cdx/search/cdx?url=helpdesk.jaipur.manipal.edu/*&output=json&filter=statuscode:200 | Empty array | No matching 200 captures in that query response |
| MUJ SLCM portal | https://mujslcm.jaipur.manipal.edu/ | Public MUJ portal sign-in surface | Direct application evidence [4] |
| MUJ SLCM onboarding guide | https://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf | Official SLCM URL, credentials workflow, support direction | Primary workflow evidence [13] [13] [13] |

The table shows the principal tension: the helpdesk name has certificate evidence but weak current DNS and archive visibility. That combination is consistent with a hostname that was provisioned, renewed, migrated, or temporarily withdrawn, but the public evidence does not identify which explanation is correct.

## Finding 1: The MUJ Helpdesk Vendor Is Not Publicly Attributable

The question posed three main possibilities: Freshdesk, Zendesk, or a native system. The reviewed evidence does not establish any of them for `helpdesk.jaipur.manipal.edu`. Direct extraction of the target hostname returned no page content, and searches using the exact hostname with Freshdesk, Zendesk, osTicket, Jira, ServiceNow, API, attachment, and ticket terms did not produce a target-host result. The absence of a search hit is not proof that no vendor exists; it only means that no public attribution was recovered.

Freshworks is directly visible at `https://servicedesk.manipal.edu/support/tickets/new`, where the extracted page title is `Freshworks`. [14] That is useful context because it demonstrates that a Manipal-branded service hostname uses Freshworks, but the hostname is different. The correct conclusion is therefore "Freshworks is confirmed for another Manipal service desk," not "MUJ helpdesk uses Freshworks."

Similarly, the public `https://helpdesk.manipal.edu.my/` page identifies itself as `MUCM Helpdesk`, offers `Open a New Ticket`, says a valid email address is required, and states that the helpdesk software is powered by osTicket. [15] [15] [15] Again, this is a separate domain and should not be merged with MUJ Jaipur infrastructure. The domain difference is material because branding, deployment ownership, ticket data, authentication, and attachment storage can all differ between campuses or business units.

Zendesk remains a hypothesis only. Zendesk documentation describes public and authenticated Help Center API behavior, but no target-host response or Zendesk-specific branding was recovered. Freshdesk remains a hypothesis only for the same reason. A native ASP.NET application is also a hypothesis, not a finding: the SLCM host has ASP.NET and IIS evidence, but that evidence belongs to `mujslcm.jaipur.manipal.edu`, not the helpdesk hostname.

### Vendor attribution matrix

| Candidate | Direct evidence on `helpdesk.jaipur.manipal.edu` | Evidence on another Manipal URL | Status for target |
|---|---|---|---|
| Freshdesk/Freshworks | None recovered | `servicedesk.manipal.edu/support/tickets/new` visibly returns `Freshworks` [14] | Not attributable |
| Zendesk | None recovered | Zendesk public documentation exists, but no MUJ target response [20] | Not attributable |
| osTicket | None recovered | `helpdesk.manipal.edu.my` says powered by osTicket [15] | Not attributable |
| Jira Service Management | None recovered | No target-specific Jira branding or route | Unverified |
| ServiceNow | None recovered | No target-specific ServiceNow branding or route | Unverified |
| Native MUJ application | None recovered for helpdesk | SLCM separately exposes ASP.NET/IIS evidence [23] | Unverified |

**Decision-ready insight:** the correct vendor label for the target is **Unknown**, with high confidence that the available evidence does not justify a named product. The most useful next step for an authorized owner is internal asset inventory or a first-party support confirmation, not public speculation.

## Finding 2: Public Ticket, Search, and Authentication Behavior Is Unknown

No public target-host landing page was extracted. No target-host `support`, `ticket`, `search`, `solutions`, `requests`, `hc`, or comparable route was returned by the reviewed searches or page extraction. The urlscan page for the exact hostname says it was not observed and has no direct hits or hosted content. [2] [2] The Wayback query also returned an empty array. These observations explain why public ticket behavior could not be characterized.

There is no defensible evidence that the target permits anonymous ticket submission, ticket-number lookup, public ticket search, article search, guest tracking, or public registration. There is also no defensible evidence that the target requires Microsoft 365, local accounts, email verification, or a vendor-specific customer portal. Those are all unresolved behaviors.

The official MUJ contact page supplies an IT support contact, `it.support@jaipur.manipal.edu`, and IT extension numbers **778** and **300**. [9] It does not link the target helpdesk hostname in the evidence reviewed. The separate Online Manipal help-center page says technical issues can be raised through the Help Center or student portal and lists `helpdesk@mujonline.edu.in` with **+91-7996 600 444** for an enrolled-learner context. [12] [12] These are official support channels, but they should not be assumed to be aliases for the target helpdesk.

The target's certificate history complicates the picture. Certificate-transparency data contains exact `helpdesk.jaipur.manipal.edu` certificates with Entrust DV TLS Issuing RSA CA 2 as issuer and validity from January 8, 2026 to January 8, 2027. [21] A certificate-transparency record is evidence of certificate issuance and logging, not evidence of application content, ticket access, or current DNS. Google DoH returned Status 3 with no Answer in three record-type queries, but the Google documentation excerpt reviewed defines the Status field and gives examples for Status 0 and Status 2 without explicitly defining value 3. [22] Accordingly, this report does not overstate the result as a proven permanent deletion or a formally confirmed NXDOMAIN condition.

**Decision-ready insight:** treat public ticket behavior as **not observable**, not as open or closed. The lack of a public page is itself useful risk information for OSINT, but it does not reveal the access-control model.

## Finding 3: SLCM Login Support Exists, but No Target Helpdesk KB Article Was Found

The strongest primary source is the official MUJ First-Year Student Profile Registration Guide. It says the Student Life Cycle Management portal is the one-stop platform for accessing academic information throughout the student's time at the university. [13] It directs students to `https://mujslcm.jaipur.manipal.edu` for the SLCM onboarding step. [13]

The guide states that the SLCM username and password are sent to the student's personal Gmail account supplied during admission. [13] It also tells students to activate the official email ID and says that a standard operating procedure for resetting the official email password is included in the email sent to the personal Gmail account. [13] The distinction matters: the guide directly documents an admission-delivered SLCM credential workflow and a separate official-email password-reset instruction, but it does not say that the SLCM account itself is administered through Microsoft 365.

The public portal text exposes `Sign In`, `Parent Login`, `Student Login`, `Forgot Password?`, and `@muj.manipal.edu`. [4] A public urlscan result for the SLCM page records HTTP 200, Microsoft-IIS/10.0, ASP.NET, and a link to `https://passwordreset.microsoftonline.com` titled `Forgot Password?`. [23] [23] This is meaningful corroboration for a Microsoft-associated password-reset link and the IIS/ASP.NET technology signal. It still does not establish the full identity flow, token protocol, tenant, conditional-access policy, or whether the password-reset page handles SLCM credentials versus official email credentials.

No official MUJ helpdesk article specifically about SLCM login failure was found. The public user evidence is narrower. One Reddit post says that after an intra-sliding update, an old registration number became invalid and a new registration number also produced an invalid result, followed by requests for help and a contact route. [6] Another public post reports that a password was showing an error even though the user believed it was correct. [3] These reports establish that users publicly discussed registration-number and password symptoms. They do not establish a root cause, outage duration, affected population, or official resolution.

### SLCM support evidence matrix

| Source | Publicly stated item | What it supports | What it does not support |
|---|---|---|---|
| Official MUJ guide | SLCM is the one-stop academic-information portal [13] | Intended business role | Current uptime or vendor |
| Official MUJ guide | SLCM URL is `mujslcm.jaipur.manipal.edu` [13] | Official portal address | Helpdesk URL ownership |
| Official MUJ guide | Credentials sent to personal Gmail [13] | Credential delivery workflow | Full identity-provider architecture |
| Official MUJ guide | Technical issues go to University Helpdesk or Admissions [13] | Intended escalation path | Which ticketing product is used |
| Public SLCM page | Sign In, Parent Login, Student Login, Forgot Password, MUJ email label [4] | Visible UI surface | Hidden routes or backend APIs |
| urlscan SLCM result | IIS/10.0, ASP.NET, Microsoft password-reset link [23] [23] | Passive technology and link evidence | Microsoft 365 as the sole identity system |
| Reddit discussion | Invalid registration number after intra-sliding [6] | User-reported symptom | Confirmed cause or official resolution |
| Reddit discussion | Password error despite user believing password was correct [3] | User-reported symptom | Account compromise or outage |

**Decision-ready insight:** the public SLCM support story is actionable at the workflow level - use the official University Helpdesk or Admissions channel - but not at the platform or incident-diagnosis level.

## Finding 4: API and Attachment Exposure Is Not Demonstrated

No target-host API or attachment endpoint was recovered. This includes no direct evidence of Freshdesk API routes, Zendesk API routes, osTicket endpoints, ASP.NET MVC controller routes, attachment download URLs, public ticket identifiers, or knowledge-base JSON responses on `helpdesk.jaipur.manipal.edu`.

The research did find official Zendesk documentation, but it must remain a comparator. Zendesk documents article routes such as `GET /api/v2/help_center/{locale}/articles` and states that the response lists only articles the requesting agent, end user, or anonymous user can view. [20] It also documents a ticket-upload route, `POST /api/v2/uploads?filename={filename}`, and explains that the upload does not itself attach the file to a comment. [19] Zendesk further states that an upload token is valid for 60 minutes and describes visibility conditions for uploaded files before and after association. [19]

Those routes answer what a Zendesk deployment might expose in its documented API, not what MUJ exposes. They cannot be converted into target-host URLs without evidence of a Zendesk tenant, and attempting them against an unconfirmed target would exceed the OSINT boundary used here. The Freshdesk documentation result similarly describes portal customization, including a custom portal URL and DNS verification, but it does not identify the MUJ target or establish its route structure. [17]

The absence of an observed API route is not a security guarantee. An API may be private, authenticated, undiscoverable, client-side-only, or hosted on a different origin. An attachment may be stored by a SaaS provider under a vendor URL rather than the helpdesk hostname. Conversely, the lack of public ticket data is a positive privacy signal within this dataset: no public ticket content or attachment was observed, and there is no basis to claim that such data is exposed.

### API and attachment status table

| Target question | Public evidence found | Result | Safe interpretation |
|---|---|---|---|
| Public ticket-list API | None | Unknown | No public route was evidenced |
| Public ticket-search API | None | Unknown | No public search behavior was evidenced |
| Knowledge-base article API | None on target | Unknown | Vendor documentation is not target evidence |
| Ticket attachment upload | None on target | Unknown | Do not infer upload exposure |
| Attachment download | None on target | Unknown | No public attachment URL was recovered |
| Zendesk comparator | Documented vendor routes [20] [19] | Comparator only | Not a MUJ finding |
| Freshdesk comparator | Custom portal URL documentation [17] | Comparator only | Not a MUJ finding |

**Decision-ready insight:** report API and attachment exposure as **not publicly demonstrated**, with confidence higher than a simple search negative because direct extraction, exact-host searches, passive records, and archives produced no target route. Do not convert that into a claim that private APIs do not exist.

## Technology and Identity Context: Keep Confirmed and Claimed Signals Separate

The input description associates SLCM with ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10 behind Akamai, and Microsoft 365 identity. The public evidence supports only part of that description. A urlscan record for the SLCM host shows Microsoft-IIS/10.0 and ASP.NET. [23] It also records an earlier scan with Microsoft-IIS/8.5 and a different IP and ASN, indicating that passive observations can change over time. [24]

The same urlscan result identifies the main SLCM IP as `98.70.14.50`, AS8075, and Microsoft Corporation, and records HTTP 200. [23] [23] These are scan-time observations. They do not prove that the host is directly exposed, that the IP is a dedicated origin, or that a named CDN such as Akamai is absent from all traffic paths. The result itself did not explicitly identify a CDN or proxy. [23]

The result's ASP.NET detection does not prove ASP.NET MVC version 5.3 or .NET Framework 4.x. No extracted evidence here states those versions. Likewise, the Microsoft password-reset link supports a Microsoft-associated integration, but the public page does not state the Microsoft 365 tenant, authentication protocol, account synchronization model, or whether the SLCM portal delegates all authentication to Microsoft.

### Technology claim audit

| Input or candidate claim | Public evidence | Status |
|---|---|---|
| ASP.NET on SLCM | urlscan explicitly reports ASP.NET [23] | Supported |
| IIS 10 on SLCM | urlscan explicitly reports Microsoft-IIS/10.0 [23] | Supported for scan observation |
| ASP.NET MVC 5.3 | No source excerpt states this version | Unverified |
| .NET Framework 4.x | No source excerpt states this version | Unverified |
| Akamai in front of SLCM | No explicit Akamai indicator in reviewed result [23] | Unverified |
| Microsoft-associated password reset | Link to passwordreset.microsoftonline.com [23] | Supported as link evidence |
| Microsoft 365 is the complete SLCM identity provider | Not explicitly stated | Unverified |
| Helpdesk shares SLCM technology stack | No target-host page or fingerprint | Unsupported inference |

**Decision-ready insight:** the SLCM technology profile should be written as "ASP.NET and IIS/10.0 observed; Microsoft password-reset link observed; MVC version, .NET Framework version, Akamai, and complete identity architecture not publicly verified." 

## High-Level Reasoning Summary

The reasoning chain is intentionally summarized at a high level rather than exposing private chain-of-thought. First, the target was separated from similarly named Manipal services. This eliminated the risk of treating Freshworks on `servicedesk.manipal.edu` or osTicket on `helpdesk.manipal.edu.my` as evidence about the MUJ Jaipur hostname. Second, direct target-host extraction and exact-name searches were compared with passive sources. The result was consistent: no public target page, route, ticket content, or vendor fingerprint was recovered.

Third, the apparent contradiction between no current DNS Answer and an exact 2026 certificate was preserved rather than resolved by speculation. The certificate proves public certificate issuance for the name; the DNS query records a resolver result at the research time. Neither alone proves service status. Fourth, SLCM was analyzed using primary official onboarding material, the public portal labels, passive urlscan metadata, and user discussions. That produced a supported workflow narrative without claiming that user reports were official findings.

Finally, vendor API documentation was retained only as a comparison framework. It demonstrates what public article and attachment APIs can look like in a known product, but no target-host evidence maps MUJ to Zendesk or Freshdesk. This is the central analytical safeguard: a route documented by a vendor is not an exposed route on the university system.

## Unanswered Questions and Evidence Gaps

| Unanswered question | Why it remains unanswered | Confidence in current gap |
|---|---|---|
| Which ticketing vendor operates the target? | No target page, banner, script, canonical URL, or vendor response was recovered | High |
| Does the target currently resolve publicly? | Google DoH returned Status 3 with no Answer, but resolver results can be contextual and are not permanent-service proof | Moderate to high |
| Is the target retired, migrated, or split-DNS? | Certificate evidence conflicts with weak current public visibility; no authoritative lifecycle notice found | High |
| Can anonymous users open tickets? | No target landing page or form was available | High |
| Can users search tickets by number or email? | No target ticket page or documentation was available | High |
| Is there a public knowledge base? | No target KB article or KB route was found | Moderate to high |
| Are attachments publicly downloadable? | No target attachment URL or behavior was found | High for no observed exposure; low for nonexistence |
| Does SLCM use Microsoft 365 for all authentication? | A Microsoft password-reset link is observed, but full identity architecture is not stated | High |
| Is Akamai in the SLCM path? | No explicit Akamai indicator appears in the reviewed passive evidence | High |
| What caused reported login problems? | User discussions provide symptoms but no confirmed root cause or official resolution | High |

## VERDICT

**Overall confidence: Moderate-to-high for the bounded negative findings; low-to-moderate for any claim about the hidden or current implementation.**

The most defensible verdict is that **the public record does not identify the ticketing system used by `helpdesk.jaipur.manipal.edu`, does not expose a verifiable public ticket/search workflow, does not reveal a MUJ helpdesk knowledge-base article about SLCM login problems, and does not demonstrate public API or attachment exposure**. This verdict is supported by direct extraction failures, exact-host searches, urlscan's no-observation page, an empty Wayback query, and the absence of target-specific vendor evidence. [2] [2]

The target hostname nevertheless has exact certificate-transparency records valid from **2026-01-08** through **2027-01-08**, so it should not be described as conclusively nonexistent or permanently decommissioned. [21] The current Google DoH observations show Status 3 with no Answer for A, AAAA, and CNAME, but the reviewed Google documentation does not itself define value 3 in the excerpt, so the safest wording is "unresolved by that public resolver at the observation point." [25] [26] [27] [22]

For SLCM, the public record is materially stronger: the official guide names the portal, describes its academic purpose, documents admission-delivered credentials, and directs technical issues to the University Helpdesk or Admissions. [13] [13] [13] The portal visibly exposes sign-in, parent login, student login, forgot-password, and a MUJ email-domain label. [4] Passive urlscan evidence records ASP.NET, Microsoft-IIS/10.0, and a Microsoft password-reset link. [23] [23] These findings support a Microsoft-associated identity integration, but not the full input claim about MVC 5.3, .NET Framework 4.x, Akamai, or complete Microsoft 365 identity.

For a university security club, the operational conclusion is simple: document the target helpdesk as **unattributed and not publicly observable**, document SLCM separately as **publicly identifiable with limited passive technology evidence**, and preserve all vendor API material as **non-target comparison data**. Any further confirmation of vendor, route behavior, or attachment handling should come from an authorized owner, first-party architecture documentation, or an approved test environment - not from attempts to access or enumerate the production service.

## References

1. *404 Not Found*. https://crt.sh/?q=helpdesk.jaipur.manipal.edu
2. *helpdesk.jaipur.manipal.edu - urlscan.io*. https://urlscan.io/domain/helpdesk.jaipur.manipal.edu
3. *Reddit - The heart of the internet*. https://www.reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue
4. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
5. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
6. *Reddit - The heart of the internet*. https://www.reddit.com/r/Manipal_Academics/comments/1993mdc/slcm_login
7. *SLcM Portal Login and Registration Guide | PDF | Password | Test (Assessment)*. https://www.scribd.com/document/364114260/Slcm-Mit-Usermanual
8. *Manipal University Jaipur - 71 years of legacy of Manipal Education*. https://www.jaipur.manipal.edu/
9. *Contact Us - Manipal University Jaipur *. https://www.jaipur.manipal.edu/contact-university.php
10. *Head- Digital Infrastructure & Technology Services - Manipal University Jaipur*. https://www.jaipur.manipal.edu/administration-it.php
11. *Online Manipal | UGC Entitled Online UG & PG Degree Courses*. http://muj.onlinemanipal.com/notifications
12. *Help Center - Get Answers to All Your Queries | Online Manipal*. https://www.onlinemanipal.com/help-center
13. *Manipal University Jaipur First-Year Student Profile Registration Guide*. https://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf
14. *Freshworks*. https://servicedesk.manipal.edu/support/tickets/new
15. *MUCM Helpdesk*. https://helpdesk.manipal.edu.my/
16. *404: Not found | Zendesk Developer Docs*. https://developer.zendesk.com/api-reference/ticketing/tickets/requests
17. * Portal Setup and Customization : Freshdesk Support*. https://support.freshdesk.com/support/solutions/45926
18. *301 Moved Permanently*. http://developers.freshdesk.com/api
19. *Attachments | Zendesk Developer Docs*. https://developer.zendesk.com/api-reference/ticketing/tickets/ticket-attachments
20. *Articles | Zendesk Developer Docs*. https://developer.zendesk.com/api-reference/help_center/help-center-api/articles
21. *crt.sh*. https://crt.sh/?q=%25.jaipur.manipal.edu&output=json
22. *JSON API for DNS over HTTPS (DoH)  |  Public DNS  |  Google for Developers*. https://developers.google.com/speed/public-dns/docs/doh/json
23. *mujslcm.jaipur.manipal.edu - urlscan.io*. https://urlscan.io/result/019ed038-c4af-765c-9499-2da69a77e30a/
24. *urlscan.io*. http://urlscan.io/api/v1/search?q=domain:mujslcm.jaipur.manipal.edu&size=100
25. *dns.google*. https://dns.google/resolve?name=helpdesk.jaipur.manipal.edu&type=A
26. *dns.google*. https://dns.google/resolve?name=helpdesk.jaipur.manipal.edu&type=AAAA
27. *dns.google*. https://dns.google/resolve?name=helpdesk.jaipur.manipal.edu&type=CNAME
