# Reconstructing the MUJ Helpdesk Host from Public Signals

## Executive Summary

This investigation now has enough public evidence to answer the main questions with an important limitation: the hostname's certificate and naming history are observable, but the helpdesk application's page content, backend, vendor, DNS target, and exact operational lifetime are not publicly recoverable from the sources tested.

- **Current status**: Google Public DNS returns status `3` for both A and CNAME queries for `helpdesk.jaipur.manipal.edu`, with no A answer and no CNAME target. That is an NXDOMAIN response at the queried resolver, not merely an HTTP outage. [9] [5]
- **Strongest activation signal**: crt.sh records two certificates for the exact hostname, both issued by Entrust DV TLS Issuing RSA CA 2, entered into CT on 2026-01-08 at approximately 09:35:53-09:35:54 UTC, and valid from 2026-01-08 through 2027-01-08. [6] This proves certificate transparency logging and TLS provisioning activity, but not that the web application served users.
- **Archive result**: Internet Archive CDX queries for the exact hostname, HTTP and HTTPS variants, wildcard paths, and non-200 responses returned empty arrays. The Wayback availability API also returned no archived snapshot for 2026-01-08. [30] Common Crawl queries for the available 2026 collections reported no captures, and URLScan returned zero results for the exact hostname. [15] [16] [17] [31]
- **Platform attribution**: There is no public evidence tying the target hostname to Freshdesk, Zendesk, osTicket, or a custom product. The separate `helpdesk.manipal.edu.my` site is explicitly powered by osTicket, but it is a different host and different institutional namespace. [8] The correct conclusion for the target is **unknown**, not Freshdesk, Zendesk, or osTicket.
- **SLCM relationship**: Official MUJ material confirms that `mujslcm.jaipur.manipal.edu` is the MUJ SLCM registration portal, that users use an official Outlook identity, and that AMS/SLCM login problems are routed to named MUJ AMS/DMS and IT Infra contacts. [18] The official ICT document describes SLCM as replacing AMS and providing attendance, internal marks, external marks, result publication, and circular broadcasts. [19] None of those documents names the target helpdesk hostname or a ticketing integration.
- **Email and SOP integration**: Public documents show an email-and-telephone support workflow, not a documented helpdesk-ticket workflow for the target. The SLCM FAQ gives `dms@jaipur.manipal.edu`, `ams@jaipur.manipal.edu`, and `it.support@jaipur.manipal.edu`, plus extensions and a university helpline. [18] The Online Manipal channel separately publishes `helpdesk@mujonline.edu.in` and a MUJ Online help center. [3] [29]

**Bottom line:** confidence is **high** that the hostname had a certificate-provisioning event on 2026-01-08 and is currently NXDOMAIN at the tested resolver; **moderate to high** that the host was intended to be MUJ-related because it sits under `jaipur.manipal.edu` and appeared in the exact-host CT record; and **low** for any claim about the application vendor, application framework, SSO integration, email ingestion, ticket workflow, or actual production activation.

## Scope, Evidence Rules, and Entity Separation

The evidence base was limited to public DNS responses, certificate-transparency records, public archive APIs, public scan indexes, public university pages and PDFs, and publicly readable support pages. No authentication was attempted, no ticket was submitted, no endpoint was fuzzed, and no attempt was made to access non-public content. This is appropriate for a university security-club OSINT study because the question can be answered as an evidence and attribution problem without interacting with protected application functions.

Three namespaces must be kept separate. First, the campus SLCM service is hosted at `mujslcm.jaipur.manipal.edu`; its public page says `WELCOME TO MUJ PORTAL`, identifies `@muj.manipal.edu`, and distinguishes parent and student login. [7] Second, the investigated hostname is `helpdesk.jaipur.manipal.edu`; its current DNS response is NXDOMAIN and no page was retrieved. [9] Third, `helpdesk.manipal.edu.my` is the public MUCM helpdesk, with a different country-code namespace and a visible osTicket footer. [8]

The Online Manipal help center is a fourth context, not automatically the same system as campus SLCM. Its page lists Manipal University Jaipur among several institutions, describes one helpdesk, and gives MUJ-related contacts. [3] [3] It also names the Epic.U platform for MUJ online learners. [3] That is useful evidence about a support channel for online learners, but it does not identify the backend of `helpdesk.jaipur.manipal.edu`.

**Interpretive rule:** a hostname, certificate, email address, or shared brand is an association signal, not proof of shared software, identity tenancy, database, ownership, or deployment. All conclusions below use the labels **observed**, **supported inference**, or **unresolved**.

## 2026-01-08 Certificate and DNS Timeline

The clearest timeline signal is the CT record. crt.sh reports certificate ID `23628924661`, issued by `C=CA, O=Entrust Limited, CN=Entrust DV TLS Issuing RSA CA 2`, with common name and name value `helpdesk.jaipur.manipal.edu`. Its CT entry timestamp is `2026-01-08T09:35:54.597`, its not-before value is `2026-01-08T00:00:00`, and its not-after value is `2027-01-08T23:59:59`. [6] A second record, certificate ID `23628923708`, has the same hostname, issuer, and validity window, with entry timestamp `2026-01-08T09:35:53.449`. [6]

| Timeline point | Public observation | What it supports | What it does not prove |
|---|---|---|---|
| 2026-01-08 00:00 UTC | Certificate not-before begins | A certificate was created with this validity start | The site was live at midnight |
| 2026-01-08 09:35:53-54 UTC | Two CT entries for the exact hostname | TLS certificate issuance/logging activity | Successful DNS publication or HTTP service |
| 2026-01-08 through 2027-01-08 | Certificate validity window | Intended certificate lifetime | Continuous deployment or continuous DNS |
| Current query date | A and CNAME status 3, no answer | Current queried DNS state is NXDOMAIN | Exact deletion date or historical IP |

The timing is consistent with a deployment or pre-deployment sequence, but that is an inference. A certificate may be obtained before DNS cutover, during a test, for a service that was never made public, or for a hostname that was subsequently withdrawn. CT logging records certificate issuance; it does not prove that a listener accepted requests. The CT page itself supplies no deployment confirmation. [6]

The current A lookup reports `Status: 3`, no `Answer` section, and an SOA authority response for `manipal.edu.`. [9] The current CNAME query likewise reports `Status: 3`, with no CNAME target. [5] The most defensible timeline is therefore: certificate activity on 2026-01-08, followed by an unknown period of possible DNS publication or testing, followed by a state that is NXDOMAIN at the time of measurement. The exact activation and removal dates remain unanswered.

No historical A record, CNAME target, IP address, Akamai edge hostname, load balancer name, or origin hostname was recovered. Mnemonic's public passive-DNS response returned count zero and an empty data array for this hostname. [24] That is a negative result from that source, not proof that no passive-DNS provider has ever observed the record.

## Archive Capture Results

The archive search produced a strong negative result. Internet Archive CDX queries for the hostname and wildcard path returned `[]` for exact, HTTP, HTTPS, and non-200 variants. The Wayback availability endpoint, queried for the host around 2026-01-08, returned `archived_snapshots: {}`. [30]

| Source | Query target | Result | Evidentiary meaning |
|---|---|---|---|
| Internet Archive CDX | Exact host and wildcard | Empty array | No returned Wayback captures in the queried views |
| Internet Archive availability | Host at 2026-01-08 | No archived snapshots | No snapshot returned for that date query |
| Common Crawl | 2026 collections | No captures found | No returned Common Crawl record in tested collections |
| URLScan | Exact hostname | `results: []`, `total: 0` | No public URLScan result returned |
| Mnemonic | Passive DNS | `count: 0`, `data: []` | No record returned by that API |

Common Crawl's early 2026 queries reported no captures for the target, and later queries reported the same. [15] [16] [17] One requested collection was unavailable, so that collection cannot be treated as evidence either way. [14] URLScan returned an empty result set with total zero. [31]

This means the club cannot responsibly reconstruct the target's page title, ticket form, footer, login provider, JavaScript bundle, response headers, or redirect destination from the tested public archives. The absence may reflect a short-lived host, robots restrictions, lack of crawling, no public HTTP service, or a certificate-only/pre-production configuration. Those are competing explanations, not established facts.

A useful contrast is the SLCM host. Wayback has public HTML captures for `mujslcm.jaipur.manipal.edu/Home/Index` at `20250110135954` and for the root at `20250527044058`, both status 200 and `text/html`. [26] The archived SLCM page visibly says `WELCOME TO MUJ PORTAL`, `@muj.manipal.edu`, and `Sign In Parent Login`. [27] The contrast shows that archive infrastructure did capture a related MUJ host, while returning no target helpdesk capture. It does not prove that the helpdesk never existed.

## Platform Attribution: Freshdesk, Zendesk, osTicket, or Custom

The target cannot currently be attributed to Freshdesk, Zendesk, osTicket, or a custom application with confidence. There is no target HTML, vendor footer, vendor-specific route, DNS CNAME, screenshot, URLScan result, or archived response from which to make that determination.

Freshdesk and Zendesk both support custom domains. Freshdesk's documentation says that a custom portal URL requires DNS verification and that an SSL certificate is generated for a custom-domain portal after DNS verification. [32] Zendesk's host-mapping documentation likewise describes changing a help-center URL to a subdomain of the customer's own domain using a CNAME and configuration. [33] These facts make Freshdesk and Zendesk technically plausible candidates, but they are generic vendor capabilities. They are not target-specific evidence.

The strongest software fingerprint found in the broader Manipal environment belongs to a different host. `helpdesk.manipal.edu.my` is titled MUCM Helpdesk, exposes Support Center Home and Open a New Ticket, and has the explicit footer `Helpdesk software - powered by osTicket`. [8] Its login page says users may sign in with Microsoft Work or School credentials, including `manipal.edu.my` staff and `scholar.manipal.edu.my` student credentials. [8]

| Candidate | Target-specific evidence | Evidence from other Manipal pages | Assessment |
|---|---|---|---|
| Freshdesk | None recovered | Freshdesk supports custom URLs and SSL after DNS verification | Possible in the abstract; unsubstantiated |
| Zendesk | None recovered | Zendesk supports custom host mapping | Possible in the abstract; unsubstantiated |
| osTicket | None recovered | Explicit footer on `helpdesk.manipal.edu.my` | Proven for separate MUCM host only |
| Custom MUJ application | No target page or headers | MUJ operates web portals and IT services | Possible but unsubstantiated |

The separate osTicket instance is a useful comparator because it demonstrates that a Manipal-branded helpdesk can use an open-source ticket system and Microsoft SSO. However, the `.edu.my` suffix, MUCM branding, and separate credential domains prevent transferring that attribution to the `.jaipur.manipal.edu` hostname. The correct platform verdict is **unresolved**.

## Email, SOP, and Support-Process Integration

The official MUJ SLCM FAQ gives the best evidence for the campus support process. It identifies `https://mujslcm.jaipur.manipal.edu/` as the registration link, says the password is based on the official Outlook ID, and gives the university helpline `0141 - 3999100`. [18] For AMS login problems, it instructs users to re-verify credentials and, if unresolved, contact `dms@jaipur.manipal.edu` or `ams@jaipur.manipal.edu`. [18]

The FAQ names AMS personnel and extensions: Rahul Kumawat at 784, Dinesh Sain at 738, and Rithik Chaudhary at 481. [18] For a non-working MUJ Outlook account, it directs users to reset the password and then contact Team IT Infra at `it.support@jaipur.manipal.edu`, extension 144. [18] The official contact page separately lists Academics with `academic@jaipur.manipal.edu` and `ams@jaipur.manipal.edu`, and IT Infra with `it.support@jaipur.manipal.edu`. [1]

| Support domain | Public channel | Exact evidence | Link to target helpdesk host |
|---|---|---|---|
| SLCM/AMS login | Email and telephone | DMS/AMS addresses, helpline, named extensions | No direct link found |
| MUJ Outlook account | Team IT Infra email and extension | `it.support@jaipur.manipal.edu`, ext 144 | No direct link found |
| Academic administration | Academic email and campus phone | `academic@jaipur.manipal.edu`, `ams@jaipur.manipal.edu` | No direct link found |
| MUJ Online learner support | Helpdesk email and phone | `helpdesk@mujonline.edu.in`, `+91-7996 600 444` | Separate online-learning context |
| Target helpdesk | Unknown | No public page or workflow recovered | Unresolved |

The official ICT list defines SLcM as Student Life Cycle Management and says it replaced the older Academic Management System. [19] It describes attendance, internal marks, external marks, result publication, and broadcast messages, and calls it a single-window system for students and parents. [19] It does not name a service-desk product, ticketing vendor, email parser, or helpdesk hostname.

Online Manipal's help center says it provides one helpdesk and support from admission to enrollment and beyond. [3] For MUJ, it lists `helpdesk@mujonline.edu.in`, `+91-7996 600 444`, and a grievance contact at `director.dodlmuj@jaipur.manipal.edu`. [3] Its notices say university email communication for that online context happens with `helpdesk@mujonline.edu.in` and direct users with issues to that address or phone number. [29]

**Supported inference:** MUJ has documented support channels that include email, telephone, AMS/DMS contacts, and Team IT Infra. **Not supported:** that any of these channels fed the target hostname, that the target converted email into tickets, or that the target was part of the Online Manipal Epic.U platform.

## Relationship to MUJ SLCM, IIS/Akamai, and Microsoft 365 Identity

The SLCM relationship is strong at the institutional and operational level but weak at the target-host level. The SLCM login page is publicly identified as the MUJ portal and shows parent and student login choices. [7] Its archived captures show the same visible identity wording. [27] The official FAQ links directly to the SLCM hostname and refers to the official Outlook ID. [18] These facts establish that SLCM and MUJ Outlook identities are part of the same documented user workflow.

The official MUJ IT page describes an IT landscape including Microsoft services for communication and Business ERP, a student life-cycle web portal, learning-management services, research-management services, and IT security. [2] It also says IT services are based on in-house and outsourced support through MaGE, DVoiS, Dimension Data, and Velocis. [2] This supports a mixed technology environment, not a single shared platform.

Public URLScan records for the SLCM host show scans at `2024-11-20T10:26:41.940Z`, `2026-01-15T05:39:23.899Z`, and `2026-06-16T11:37:37.041Z`; the recorded requests returned status 200, with Microsoft IIS 10.0 on the first two observations. [21] The URLScan domain page identifies Microsoft Corporation's AS8075, Pune GeoIP, and Azure DNS nameservers, while also marking the host as not observed on that page's current view. [20] [20] [20]

These SLCM observations are consistent with the user-provided description of an ASP.NET/IIS/Akamai/Microsoft 365 ecosystem, but the public records reviewed here do not independently establish every part of that stack for the helpdesk target. In particular, no target response header, Akamai edge hostname, ASP.NET route, MVC version, .NET version, Microsoft login redirect, or Microsoft 365 tenant identifier was recovered.

## Activation Signals, Competing Explanations, and Safe Follow-up

The evidence supports four possible scenarios:

| Scenario | Supporting observations | Contradicting or missing evidence | Confidence |
|---|---|---|---|
| Pre-production or reserved host | Exact-host certificate on 2026-01-08; no archives or scans | No direct deployment record | Moderate |
| Short-lived production service | Certificate plus helpdesk naming under MUJ domain | No page capture, DNS history, or traffic evidence | Possible |
| Certificate-only configuration | CT record with current NXDOMAIN and no target content | Does not explain intended operational purpose | Possible |
| Misconfigured or withdrawn deployment | Certificate followed by present NXDOMAIN | Exact withdrawal date and cause unknown | Possible |

The most economical interpretation is that the hostname was provisioned or prepared around 2026-01-08 and later removed or never publicly activated. That is a **supported inference**, not a proven event timeline. Certificate issuance alone cannot distinguish an active production cutover from a staging or abandoned setup. Current NXDOMAIN also does not show whether the DNS record was deliberately removed, expired, replaced, or never published to the public zone.

A public-only follow-up program should remain passive: preserve the CT record IDs, periodically query public CT logs for renewed certificates, monitor public DNS resolution, check public archive APIs, and review newly published official MUJ documents for a direct support URL. The club should not attempt login, ticket creation, password-reset flows, endpoint enumeration, origin discovery, or any test that changes state. MUJ's broader IT policy states that its IT policies govern information assets, systems, networks, and digital assets across its institutions and provides an information-security contact. [22]

## exact_tables

The following table is the compact evidence ledger requested for reproducibility.

| Claim | Status | Public URL |
|---|---|---|
| Target A query is NXDOMAIN | Observed | https://dns.google/resolve?name=helpdesk.jaipur.manipal.edu&type=A |
| Target CNAME query is NXDOMAIN | Observed | https://dns.google/resolve?name=helpdesk.jaipur.manipal.edu&type=CNAME |
| Target CT records logged 2026-01-08 | Observed | https://crt.sh/?q=%25.helpdesk.jaipur.manipal.edu&output=json |
| Wayback exact/protocol queries empty | Observed | https://web.archive.org/cdx/search/cdx?url=helpdesk.jaipur.manipal.edu%2F*&output=json&fl=timestamp%2Coriginal%2Cstatuscode%2Cmimetype%2Cdigest%2Clength |
| Wayback date availability empty | Observed | https://archive.org/wayback/available?url=helpdesk.jaipur.manipal.edu%2F&timestamp=20260108 |
| Common Crawl no target captures | Observed | https://index.commoncrawl.org/CC-MAIN-2026-30-index?url=helpdesk.jaipur.manipal.edu%2F*&output=json |
| URLScan target result count zero | Observed | https://urlscan.io/api/v1/search/?q=domain%3Ahelpdesk.jaipur.manipal.edu |
| SLCM FAQ links registration host | Observed | https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf |
| SLCM replaces AMS and lists academic modules | Observed | https://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf |
| MUCM comparator is powered by osTicket | Observed, separate host | https://helpdesk.manipal.edu.my/login.php |
| MUJ IT page describes Microsoft and student-life-cycle services | Observed, contextual | https://www.jaipur.manipal.edu/administration-it.php |

## Synthesis

Across mechanism, scope, and evidence strength, the target and the known comparator diverge. The target has a certificate and a DNS disappearance but no page artifact. The MUCM comparator has visible pages, ticket routes, a named osTicket footer, and Microsoft SSO wording. The SLCM host has archived pages, official FAQ references, and public IIS observations. Those are three different evidence profiles and should not be collapsed into one system.

The key tension is between a strong provisioning signal and a weak service signal. The exact-host CT record is unusually specific: it names the hostname, issuer, entry timestamp, and validity period. Yet every tested public content source is empty for the target. This could indicate a short deployment window, a pre-production certificate, a withdrawn project, or a DNS publication problem. It cannot justify a vendor attribution.

The support-process evidence creates a second tension. MUJ's official SLCM materials document a mature operational escalation path through AMS, DMS, Team IT Infra, Outlook identity, email addresses, telephone extensions, and a helpline. The existence of that process makes a helpdesk hostname plausible, but plausibility is not integration evidence. No source reviewed links `helpdesk.jaipur.manipal.edu` to the FAQ, SLCM page, official contact page, Online Manipal help center, or the osTicket MUCM instance.

The practical lesson for the security club is to retain the target as an unresolved historical asset, not to label it as a confirmed vulnerability or confirmed ticketing platform. The useful, reproducible result is the narrow one: certificate provisioning was publicly logged on 2026-01-08; the hostname is currently NXDOMAIN at the tested resolver; public archives and scan indexes contain no recoverable target page; and official MUJ documents establish related SLCM and support channels without proving target integration.

## Final Verdict

**Verdict: likely MUJ-related hostname prepared for TLS around 2026-01-08, but application identity and operational activation are unproven.**

| Verdict component | Conclusion | Confidence |
|---|---|---|
| Current DNS state | NXDOMAIN for A and CNAME queries | High |
| 2026-01-08 TLS event | Two CT records for exact hostname, Entrust issuer, 2026-01-08 validity start | High |
| Actual production activation | Not established | High confidence in the uncertainty |
| Exact removal/deactivation date | Unknown | High confidence in the uncertainty |
| Freshdesk attribution | Unsupported | High confidence |
| Zendesk attribution | Unsupported | High confidence |
| osTicket attribution | Proven only for separate `helpdesk.manipal.edu.my` | High |
| Custom MUJ application | Possible, not demonstrated | Low |
| SLCM integration | Institutional context is documented; direct host integration is not | Moderate for context, low for direct integration |
| Email/SOP integration | MUJ support emails and procedures are documented; target linkage is not | Moderate for general support, low for target linkage |

The final confidence level for the overall reconstruction is **moderate**: high-confidence facts explain the certificate and current DNS state, while the central application-identification question remains unresolved because the public target artifacts are absent.

## References

1. *Contact Us - Manipal University Jaipur*. https://jaipur.manipal.edu/contact-university.php
2. *Head- Digital Infrastructure & Technology Services - Manipal ...*. https://www.jaipur.manipal.edu/administration-it.php
3. *Help Center - Get Answers to All Your Queries*. https://www.onlinemanipal.com/help-center
4. *Manipal University - muj.slcm.jaipur.manipal.edu*. https://muj.slcm.jaipur.manipal.edu/Home/
5. *dns.google*. https://dns.google/resolve?name=helpdesk.jaipur.manipal.edu&type=CNAME
6. *crt.sh*. https://crt.sh/?q=%25.helpdesk.jaipur.manipal.edu&output=json
7. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
8. *MUCM Helpdesk - Manipal*. https://helpdesk.manipal.edu.my/login.php
9. *dns.google*. https://dns.google/resolve?name=helpdesk.jaipur.manipal.edu&type=A
10. *index.commoncrawl.org*. https://index.commoncrawl.org/CC-MAIN-2026-04-index?url=helpdesk.jaipur.manipal.edu%2F*&output=json
11. *index.commoncrawl.org*. https://index.commoncrawl.org/CC-MAIN-2026-21-index?url=helpdesk.jaipur.manipal.edu%2F*&output=json
12. *index.commoncrawl.org*. https://index.commoncrawl.org/CC-MAIN-2026-08-index?url=helpdesk.jaipur.manipal.edu%2F*&output=json
13. *index.commoncrawl.org*. https://index.commoncrawl.org/CC-MAIN-2026-12-index?url=helpdesk.jaipur.manipal.edu%2F*&output=json
14. *index.commoncrawl.org*. https://index.commoncrawl.org/CC-MAIN-2026-18-index?url=helpdesk.jaipur.manipal.edu%2F*&output=json
15. *index.commoncrawl.org*. https://index.commoncrawl.org/CC-MAIN-2026-25-index?url=helpdesk.jaipur.manipal.edu%2F*&output=json
16. *index.commoncrawl.org*. https://index.commoncrawl.org/CC-MAIN-2026-30-index?url=helpdesk.jaipur.manipal.edu%2F*&output=json
17. *index.commoncrawl.org*. https://index.commoncrawl.org/CC-MAIN-2026-34-index?url=helpdesk.jaipur.manipal.edu%2F*&output=json
18. *Frequently Asked Questions and Contacts for SLCM Registration*. https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf
19. *Contents*. https://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf
20. *mujslcm.jaipur.manipal.edu - urlscan.io*. https://urlscan.io/domain/mujslcm.jaipur.manipal.edu
21. *urlscan.io*. https://urlscan.io/api/v1/search/?q=domain%3Amujslcm.jaipur.manipal.edu
22. *IT Policies*. http://manipal.edu/mu/policies/it-policy.html
23. *404 Not Found*. https://crt.sh/?output=json&q=mujslcm.jaipur.manipal.edu
24. *api.mnemonic.no*. https://api.mnemonic.no/pdns/v3/helpdesk.jaipur.manipal.edu
25. *Manipal University*. https://web.archive.org/web/20250527044058/https://mujslcm.jaipur.manipal.edu/
26. *web.archive.org*. http://web.archive.org/cdx/search/cdx?collapse=urlkey&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&output=json&url=mujslcm.jaipur.manipal.edu/*
27. *Manipal University*. https://web.archive.org/web/20250110135954/https://mujslcm.jaipur.manipal.edu/Home/Index
28. *Student Portal*. https://student.mujonline.com/
29. *Notices - MUJ*. https://muj.onlinemanipal.com/notifications
30. *archive.org*. https://archive.org/wayback/available?url=helpdesk.jaipur.manipal.edu%2F&timestamp=20260108
31. *urlscan.io*. https://urlscan.io/api/v1/search/?q=domain%3Ahelpdesk.jaipur.manipal.edu
32. *Use a custom portal URL and verify DNS : Freshdesk Support*. https://support.freshdesk.com/support/solutions/articles/37590-set-up-a-custom-portal-url-and-verify-dns
33. *Host mapping - Changing the URL of your help center - Zendesk help*. https://support.zendesk.com/hc/en-us/articles/4408838571930-Host-mapping-Changing-the-URL-of-your-help-center
