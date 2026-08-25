# MUJ SLCM and NoPaperForms: Evidence-Bounded Risk Map

## Executive Summary

- **Hostname Semantics**: Certificate Transparency (CT) records show `npfslcm.jaipur.manipal.edu` as the certificate name value while `mujslcm.jaipur.manipal.edu` appears as the certificate common name; MUJ's own ICT documentation expands SLCM as Student Life Cycle Management. The interpretation that `npf` means NoPaperForms is plausible, but it is not explicitly confirmed by a public MUJ or NoPaperForms source. Treat it as a medium-confidence inference, not a fact. [38] [47]
- **Admissions Delegation**: A public DNS-over-HTTPS response returns `admissions.jaipur.manipal.edu` as a CNAME to `jaipurmanipal.nopaperforms.com`, and a separate DNS lookup page reports the same target. This is strong evidence of delegated hosting or service routing, but it does not by itself prove all application data flows, contractual arrangements, or database ownership. [6] [41]
- **Hosting Chain**: The public resolver response continues from the NoPaperForms hostname to an AWS Elastic Load Balancing hostname and reports three IPv4 addresses: `65.1.79.226`, `13.206.4.210`, and `65.0.244.41`. This identifies an observed delivery path, not the physical location of applicant data or the full backend architecture. [46]
- **SLCM Function**: MUJ's public ICT list describes SLCM as replacing the older Academic Management System and covering attendance, internal marks, external marks, result publication, and broadcast messages or circulars. It calls the system a single window for students and parents. [47]
- **Identity Boundary**: The MUJ SLCM landing page publicly exposes student and parent login language and the `@muj.manipal.edu` identity domain. The collected evidence does not establish that Microsoft 365 is the federation provider, nor does it identify the protocol, tenant, conditional-access policy, or directory boundary. [12]
- **Platform Scope**: NoPaperForms, now presenting Meritto as its flagship enrollment product, publicly describes an education CRM, lead management, application processing, enrollment workflows, payment functionality, and integrations. These are vendor capability statements; they do not prove that MUJ enables every module. [3] [40]
- **Privacy Gap**: The vendor login policy says information is collected through forms, information requests, and school applications, but the collected excerpt does not specify the exact categories, purposes, retention, sharing, or MUJ-specific controller and processor roles. No MUJ-specific admissions privacy notice was located in the reviewed public pages. [13] [17]
- **Complaint Evidence**: Targeted searches did not produce a credible, first-hand public complaint that specifically attributes a MUJ admissions failure to the NoPaperForms CRM. Available review signals are mostly positive, vendor-hosted, or general software reviews. This is an evidence gap, not evidence that no complaints exist. [40] [22] [30]
- **Security Action**: The defensible club recommendation is passive asset inventory, CT and DNS change monitoring, written authorization for any testing, and a request for documented data-flow and processor information. The club should not test credentials, access another user's data, enumerate private endpoints, or attempt a takeover.

## 1. What the Public Record Establishes

### Scope and methodology

This report uses public web pages, public DNS responses, public CT data, public technology-observation pages, public vendor documentation, and public review pages. It separates direct observations from interpretations. A hostname, certificate, DNS record, product description, or review is treated as evidence of exactly what it says, not as proof of hidden infrastructure or an undocumented institutional relationship.

The requested environment description names ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 identity. Public scanning evidence supports some of the application-stack indicators, but not all of that supplied description. A point-in-time scan reports Microsoft-IIS/10.0, ASP.NET MVC 5.3, and an ASP.NET 4.0.30319 runtime indicator for `mujslcm.jaipur.manipal.edu`. It does not establish the operating system, database, cloud account, reverse-proxy arrangement, Akamai involvement, or authoritative patch levels. [39]

The analysis therefore uses four evidence grades:

| Grade | Meaning | Examples in this report |
|---|---|---|
| Direct observation | The source explicitly records the fact | DNS CNAME, CT certificate name, portal login text, HTTP technology headers |
| Vendor or institution statement | The organization publicly describes its own system or capability | MUJ SLCM modules; Meritto CRM and payment features |
| Corroborated inference | Multiple observations support an interpretation, but no source states it directly | `npf` likely referring to NoPaperForms in `npfslcm` |
| Unknown | The reviewed sources do not establish the fact | Specific fields transferred, database location, SSO protocol, contract, retention period, incident history |

**Decision insight:** The strongest findings concern naming and DNS routing. The weakest findings concern hidden data flows, legal roles, and operational security controls. A security club should not turn a strong routing observation into an unsupported breach claim.

## 2. The `npfslcm` Hostname: Direct Facts Versus Acronym Inference

### What CT actually shows

The exact CT query for `npfslcm.jaipur.manipal.edu` returns a record in which the certificate common name is `mujslcm.jaipur.manipal.edu` and the certificate `name_value` is `npfslcm.jaipur.manipal.edu`. The record was issued by SSL Corporation's Entrust OV TLS issuing CA, entered on November 16, 2025, and lists validity from March 7, 2025 through December 22, 2025. A second record for the same name has the same validity period and an entry timestamp of March 7, 2025. [38]

The broader CT results add context. They show later or adjacent certificates for `mujslcm.jaipur.manipal.edu`, including a certificate described as valid from December 22, 2025 to December 21, 2026. They also show certificates for `admissions.jaipur.manipal.edu`. CT is therefore useful for historical asset discovery and certificate-change monitoring. [45]

CT does not prove that the certificate subject operated the application, that the certificate was issued by the application owner, or that the hostname was live at every point in the validity period. The CT record proves that a publicly trusted certificate containing the hostname was logged. It does not prove backend ownership or application data transfer. [45]

### What SLCM means

MUJ's official ICT-tool document states that SLcM means Student Life Cycle Management and that it replaced the older Academic Management System. The same document describes modules for attendance, internal marks, external marks, result publication, and broadcast messages or circulars. It describes the platform as a single window for students and parents handling academic matters. [47]

The MUJ portal itself displays “WELCOME TO MUJ PORTAL,” “Sign In,” and “Sign In Parent Login,” along with the `@muj.manipal.edu` identity domain. This supports the conclusion that the portal is intended for institutional student and parent access, but the landing page does not expose its complete functional inventory. [12]

### Does `npf` mean NoPaperForms?

The inference is reasonable because the hostname contains `npf`, the MUJ admissions hostname points directly to a NoPaperForms subdomain, and NoPaperForms publicly documents an education enrollment platform that spans lead, application, enrollment, and payment workflows. [6] [40]

However, no reviewed official source says that MUJ's `npfslcm` label expands to “NoPaperForms SLCM.” The CT record does not define the acronym. The MUJ ICT document defines SLCM but not NPF. The vendor documentation describes products and APIs but does not identify this hostname. The correct conclusion is therefore: **`npfslcm` is likely a NoPaperForms-related SLCM integration or legacy alias, with medium confidence; the naming explanation is not publicly confirmed.**

| Question | Public answer | Confidence |
|---|---|---|
| Does `slcm` mean Student Life Cycle Management? | Yes, explicitly stated by MUJ documentation | High |
| Is `npfslcm` present in MUJ CT history? | Yes, as a certificate name value associated with a certificate whose common name is `mujslcm` | High |
| Does `npf` explicitly mean NoPaperForms? | No explicit public confirmation located | Medium as an inference |
| Does CT prove the hostname's backend owner? | No; CT proves certificate naming and logging | High |

**Decision insight:** Inventory `npfslcm` as a potentially important historical alias, but do not label it a confirmed vendor integration until MUJ or NoPaperForms provides direct confirmation.

## 3. The MUJ Admissions CNAME and Hosting Chain

### Direct DNS evidence

A public DNS-over-HTTPS response returns status `0` and a CNAME record for `admissions.jaipur.manipal.edu` with target `jaipurmanipal.nopaperforms.com` and a TTL of 2,387 seconds. [6]

A separate public DNS lookup page independently reports that `admissions.jaipur.manipal.edu` resolves to the same CNAME target and describes the hostname as a subdomain of `manipal.edu`. [41]

The public resolver's recursive response exposes the next hop as `prodvpc-web-lb4-593721465.ap-south-1.elb.amazonaws.com`, followed by three IPv4 addresses: `65.1.79.226`, `13.206.4.210`, and `65.0.244.41`. The response shows a 3,600-second TTL for the two CNAME records and a 60-second TTL for the A record. [46]

This is a strong, reproducible routing finding: a user resolving the MUJ admissions hostname is directed through a NoPaperForms-named hostname and then through an AWS load-balancing name. It is not proof that every browser request, uploaded document, payment, email, or administrative export follows the same path. DNS selects a service endpoint; it does not describe application-layer fields or the internal processing sequence.

### CT and urlscan context

CT results include certificates for `admissions.jaipur.manipal.edu`, including one described as valid from March 27, 2025 to April 25, 2026. This supports the presence of the MUJ admissions hostname in publicly logged TLS certificates, but, again, it does not establish the complete service architecture.

The urlscan domain page reports the hostname as first observed six years earlier, with GeoIP in Mumbai, India, and an Amazon AS16509 association. It lists the same three IPv4 addresses and cautions that urlscan provides a live snapshot and does not host or control the website. The page also reports no direct scan hits in its displayed observations. [44] [44]

The AWS and Mumbai observations should not be read as a precise data-residency statement. IP geolocation and cloud routing do not establish where databases, backups, logs, payment records, or support exports are stored. They also do not prove that Akamai is or is not in front of the application. The reviewed evidence supports an AWS-associated delivery path, not a full edge-network conclusion.

| Observable | What it establishes | What it does not establish |
|---|---|---|
| MUJ admissions CNAME | DNS delegation to `jaipurmanipal.nopaperforms.com` | Contract, database ownership, every data transfer |
| NoPaperForms CNAME target | A vendor-branded DNS service name is in the resolution chain | That all APIs or payment systems use the same host |
| AWS ELB hostname | The resolver exposes an AWS ELB next hop | Cloud account owner, region of stored data, backend topology |
| Three IPv4 addresses | Current public resolver answer at observation time | Permanent address set or application ownership |
| CT certificate | Hostname appears in logged TLS certificate data | Live service status or backend ownership |

**Decision insight:** The admissions linkage is high-confidence at the DNS-routing layer and low-to-medium confidence at the data-governance layer. Those are different findings and should be reported separately.

## 4. What SLCM and Meritto Are Designed to Do

### MUJ SLCM

MUJ's official ICT list describes the SLCM suite as an academic single-window system. Its stated modules include attendance, internal marks, external marks, result publication, and broadcast messages or circulars. Its stated audience includes students and parents. [47]

The public portal page adds the visible login boundary: student and parent login, with `@muj.manipal.edu` shown as the identity domain. [12] The reviewed page does not show a public API catalog, data dictionary, role matrix, identity protocol, or administrative workflow. Those omissions do not imply that controls are absent; they mean the controls are not established by the landing page.

### NoPaperForms and Meritto

NoPaperForms publicly describes Meritto as a unified, AI-powered, modular platform for educational organizations. The company says it supports the student acquisition and enrollment journey, while its broader portfolio includes fee management and student engagement. [3] [3]

The product documentation describes Enrollment Cloud as covering lead management, application processing, and enrollment completion. It describes an education CRM for student engagement, an application platform for custom forms and post-application management, and a payment cloud. It also lists integrations such as lead-generation websites, cloud telephony, exam platforms, email connectors, ERP or SIS connectors, and payment-gateway plugins. [40] [40] [40] [40]

The company publicly announced the rebranding of its flagship product to Meritto on June 26, 2023. The announcement says the former NoPaperForms flagship product was rebranded as Meritto. This matters for OSINT because older DNS names, documentation, screenshots, and user reports may use NoPaperForms while newer product pages use Meritto. [48]

### API evidence

The NoPaperForms developer portal documents API calls under `https://api.nopaperforms.io/`. It says an account is required and that access and secret keys are needed. It documents standard REST-style methods including POST, GET, PUT, and DELETE, with JSON responses. The visible API areas include Lead, Opportunity, Activity, Form, Master Data, Payment, and Application. [32] [32] [32] [32] [32] [32]

The Lead API documentation specifically describes creating a lead, updating an existing lead, and fetching leads and their attributes. [32] This provides a credible model for institution-side CRM integration, but it does not show that MUJ's admissions site calls the public API directly. A web application may use server-side services, private services, webhooks, or other integration paths that are not visible in the public documentation.

### Payment workflow evidence

Meritto's public application-payment page says applicants can pay online using multiple options, that existing payment gateways can be integrated, and that multi-stage transactions can be configured around course selection and form completion. It also describes split-payment and reporting functions, including CSV export of transactional data. [10] [10] [10] [10]

These are vendor product claims, not an observation of MUJ's specific configuration. They support the possibility that an admissions deployment can combine applicant identity, form data, payment state, and institution workflow, but they do not establish which fields MUJ collects or which payment provider it uses.

**Decision insight:** Vendor documentation is sufficient to model component classes - lead, form, application, payment, and institution integration - but insufficient to assert MUJ's exact configuration. Obtain a sanctioned architecture diagram or data-processing schedule before publishing stronger claims.

## 5. Reconstructed Data-Flow Model and Unknowns

### Observed path

The only end-to-end path directly observed in the public evidence is DNS resolution:

| Stage | Evidence status | Description |
|---|---|---|
| 1. Applicant enters MUJ admissions hostname | Directly implied by the public hostname and admissions page | `admissions.jaipur.manipal.edu` is the institution-branded entry point |
| 2. DNS alias | Direct observation | CNAME to `jaipurmanipal.nopaperforms.com` [6] |
| 3. Delivery layer | Direct observation | Recursive answer continues to an AWS ELB hostname and three public IPs [46] |
| 4. Application processing | Vendor capability, not MUJ-specific observation | Meritto publicly documents forms, leads, applications, and enrollment workflows [40] |
| 5. Payment processing | Vendor capability, not MUJ-specific observation | Meritto publicly documents application payment and gateway integration [10] |
| 6. Institutional reconciliation or SIS/ERP exchange | Capability/inference | Vendor lists ERP/SIS connectors, but no MUJ-specific exchange is publicly demonstrated [40] |
| 7. Student lifecycle records | Institution documentation | MUJ says its SLCM handles academic modules and student/parent access [47] |

### Bounded inference

**Inference:** A likely admissions journey is: applicant visits the MUJ-branded admissions hostname, submits enquiry or application information, the hosted service processes or stores some of that information, optional payment services record transaction state, and selected records may be passed to institutional workflows. This inference is supported by the DNS alias and the vendor's documented product categories. [6] [40] [10]

**Inference not established:** The public evidence does not show that the admissions CRM writes directly into the academic SLCM database. It does not show that applicant records are copied into `mujslcm.jaipur.manipal.edu`, that the two systems share a database, or that Microsoft 365 identity is used for applicant authentication. The terms “admissions CRM” and “SLCM” describe different functional domains and should not be treated as evidence of a direct integration.

### Data elements and governance unknowns

The vendor privacy excerpt states that information is collected through forms, requests for information, and school applications, but the reviewed excerpt does not specify the exact information categories, purposes, sharing, retention, deletion process, rights, or NoPaperForms role. [13] The public Trust Center says the company presents itself as SOC 2, ISO 27001, and GDPR compliant, and reports a GDPR renewal assessment for 2026-2027 dated June 5, 2026 and an ISO/IEC 27001 surveillance audit dated May 21, 2025. These are vendor-published claims and assessment notices; they do not answer MUJ-specific configuration or contract questions. [28] [28] [28]

| Unknown requiring authorized confirmation | Why it matters |
|---|---|
| Exact applicant fields | Determines privacy impact and minimization requirements |
| Controller and processor roles | Determines accountability and data-subject handling |
| API or webhook endpoints actually enabled | Determines integration exposure and monitoring scope |
| Database, backup, and log locations | Prevents unsupported data-residency claims |
| Retention and deletion schedule | Determines lifecycle and offboarding risk |
| Payment provider and tokenization model | Separates application data from payment data |
| SSO or identity protocol | Determines authentication and account-linking risk |
| Whether admissions records enter academic SLCM | Determines cross-system access and authorization risk |
| Incident history and notification process | Determines operational risk assessment |
| Administrative roles and export permissions | Determines insider and excessive-data exposure risk |

**Decision insight:** The most important unanswered questions are governance questions, not technology-brand questions. A data-flow diagram with fields, roles, destinations, retention, and access paths would reduce uncertainty more effectively than additional passive fingerprinting.

## 6. Public Complaints and Reliability Signals

### What was found

The targeted public searches reviewed NoPaperForms, Meritto, MUJ admissions, payment, OTP, login, and application-failure terms. They did not produce a credible first-hand report that specifically ties a MUJ admissions defect to the NoPaperForms CRM. The search results were dominated by official product pages, vendor material, general review pages, and unrelated or insufficiently specific results. This negative result should be phrased narrowly: **the reviewed public corpus did not establish the requested complaint**, not “there are no complaints.”

The vendor-hosted Meritto testimonials are positive. They include statements about onboarding, handling higher application volumes, streamlined admissions, and improved engagement. Because the testimonials appear on the vendor's own customer-testimonial pages, they are useful as evidence of published customer messaging but not as independent reliability measurements. [40] [40] [40]

G2 lists NoPaperForms with a 4.8 out of 5 rating from 21 reviews in the reviewed page. One visible positive comment says lead leakage is very low. That is software-review evidence, not applicant evidence, and the review population is not the same as MUJ applicants. [23] [23]

A separate G2 page for Meritto reports 4.8 out of 5 from 20 reviews. The visible reviews mention purpose-built education design, ease of use, automatic lead assignment, a crowded interface for new users, limited report customization, and possible slowness with large lead volumes. [22] [22] [22]

Software Advice reports a 4.6 overall rating from 619 reviews in the search result and describes one reviewer's experience as decent, with basic requirements and lead management handled effectively. The visible excerpt does not state a specific complaint and does not establish applicant outcomes. [30]

| Source type | Signal | Proper interpretation |
|---|---|---|
| Vendor testimonials | Positive claims about onboarding and workflow | Marketing or customer-success evidence; not independent measurement |
| G2 NoPaperForms | 4.8/5 from 21 reviews | General software-review signal; not MUJ applicant evidence |
| G2 Meritto | 4.8/5 from 20 reviews; some usability and reporting criticisms | Independent review-platform signal, but not necessarily applicant experience |
| Software Advice | 4.6 from 619 reviews in the visible result | General reviewer signal; visible excerpt lacks a concrete complaint |
| Targeted complaint searches | No confirmed MUJ-specific CRM complaint in reviewed corpus | Evidence gap, not proof of absence |

**Decision insight:** The public record supports a cautious reliability profile: generally positive published reviews with some usability, reporting, and scale-related criticisms, but no substantiated MUJ-specific complaint in the collected evidence. A club should seek anonymized, consent-based student reports rather than infer failure from search-result absence.

## 7. Security Implications and Safe Club Workplan

### Certificate and DNS hygiene

The MUJ admissions CNAME is not itself a vulnerability. MDN explains that subdomain takeover risk generally arises when a subdomain has a CNAME but no host provides content, often after a virtual host is removed or deprovisioning is mishandled. MDN recommends coordinated provisioning and deprovisioning, removing DNS records first during deprovisioning, and maintaining an inventory of domains and hosting providers. [49] [49] [49]

The observed MUJ admissions CNAME currently resolves through a live-looking chain, so the reviewed evidence does not establish a dangling-record condition. The safe recommendation is monitoring: record the intended provider, service owner, renewal contact, certificate scope, and deprovisioning owner. Do not attempt to claim, modify, or test the hostname.

CT monitoring is similarly defensive. The historical presence of `npfslcm` and continuing certificates for `mujslcm` show why certificate names should be inventoried, compared against approved assets, and reviewed when new names appear. CT should be used as an early-warning and asset-discovery source, not as permission to probe an application.

### API and authorization review

NoPaperForms documents APIs involving leads, applications, forms, payments, and related data. OWASP states that object-level authorization checks should be considered in every function that accesses a data source using an ID supplied by the user. OWASP also emphasizes that compromising client or user identification can compromise API security and recommends inventorying hosts and deployed API versions to mitigate deprecated APIs and exposed debug endpoints. [50] [50]

For a university security club, the safe deliverable is a control checklist for the system owner:

| Control area | Safe question to ask the owner | No unauthorized action |
|---|---|---|
| Authorization | Are student, parent, counselor, and administrator objects isolated by role and institution? | Do not alter IDs or attempt cross-account access |
| Authentication | What identity provider, MFA, session lifetime, and recovery process are used? | Do not test credentials or recovery flows without written scope |
| API inventory | Which public and private API versions are enabled and monitored? | Do not enumerate hidden endpoints |
| Data minimization | Which fields are mandatory, optional, exported, or retained? | Do not submit real personal data for testing |
| Payment boundary | What data is handled by the gateway versus the CRM? | Do not initiate test payments without authorization |
| Logging | Are access, export, role changes, and integration failures logged? | Do not seek other users' logs or records |
| Offboarding | Are DNS records and vendor accounts removed together? | Do not claim a vendor resource |

### Identity and privacy

The visible SLCM login domain is `@muj.manipal.edu`, but public evidence does not establish Microsoft 365 federation. The owner should document whether the portal uses Microsoft Entra ID, an application-local directory, a gateway, or another identity service; whether parent accounts are separate; and how an applicant becomes a student account. [12]

The owner should also publish or provide an admissions privacy notice that identifies collection categories, purposes, recipients, retention, rights, support contacts, and the relationship between MUJ and any service provider. The vendor policy's general statement that information is collected through forms and school applications is not a substitute for an MUJ-specific notice. [13]

**Decision insight:** The club can provide real value without active testing by producing an asset register, a data-flow questionnaire, a DNS/CT monitoring design, and an authorization template. These artifacts reduce risk while respecting the boundary between public OSINT and unauthorized access.

## 8. Synthesis

The ecosystem contains at least two conceptually different systems. MUJ's SLCM is described as an academic lifecycle and student/parent portal covering attendance, marks, results, and circulars. Meritto or NoPaperForms is described as an admissions and enrollment platform covering enquiries, leads, applications, payments, and institution-facing workflows. [47] [40]

The mechanisms differ. The SLCM evidence is institutional and academic: login, student and parent audience, and academic modules. The NoPaperForms evidence is vendor and revenue-process oriented: lead capture, application forms, enrollment conversion, payment options, APIs, and integrations. The admissions CNAME creates a strong technical relationship between the MUJ-branded entry point and a NoPaperForms-named service, but the CNAME does not demonstrate that the admissions service writes directly to the academic SLCM. [6] [46]

The scope of evidence also differs. DNS and CT provide precise but narrow observations. They are strong on names and routing and weak on data semantics. Vendor documentation provides broad capability descriptions but is not proof of MUJ's enabled configuration. Institutional documents provide the clearest account of SLCM purpose but say little about the admissions vendor. Reviews provide user-experience signals but do not establish MUJ-specific reliability or security.

The principal tension is between architectural plausibility and evidentiary certainty. It is plausible that a NoPaperForms-hosted admissions front end receives enquiry, form, application, and payment information and that selected records move into institutional operations. It is not publicly demonstrated which records move, through which API or private integration, under what legal roles, or whether the academic SLCM is involved at all. That distinction should drive the club's language and recommendations.

A second tension concerns brand continuity. Older records may say NoPaperForms while newer material says Meritto because of the June 2023 rebrand. This creates an OSINT correlation opportunity, but it also creates a risk of conflating products, hostnames, and historical deployments. [48]

A third tension concerns public confidence. Published review signals are favorable, while the reviewed searches found no specific MUJ complaint. Neither result is decisive. Positive reviews may reflect institutional users rather than applicants, and absence from indexed public pages may reflect search coverage rather than absence of incidents. The appropriate conclusion is a bounded evidence assessment, not a quality certification or a failure allegation.

| Dimension | MUJ SLCM | MUJ admissions / NoPaperForms linkage | Evidence limitation |
|---|---|---|---|
| Primary function | Academic student lifecycle | Recruitment, application, enrollment, payment | Exact MUJ configuration is not public |
| Direct evidence | MUJ ICT list and portal | CNAME and resolver chain | DNS does not show application payloads |
| Identity clue | `@muj.manipal.edu`; student and parent login | Applicant forms and vendor login policy | Microsoft 365 federation not established |
| Data classes | Attendance, marks, results, circulars | Leads, forms, applications, payment state | Exact fields and retention unknown |
| Confidence | High for stated purpose | High for DNS routing; medium for integration semantics | Contract and data-flow proof absent |

**Decision insight:** Treat the systems as related but not proven to be directly integrated. The next best evidence is owner-provided documentation, not more speculative hostname interpretation.

## 9. VERDICT

### Confidence table

| Finding | Confidence | Verdict |
|---|---:|---|
| `slcm` means Student Life Cycle Management in MUJ documentation | High | Directly documented |
| `npfslcm` appeared in CT history associated with a `mujslcm` certificate | High | Direct CT observation |
| `npf` means NoPaperForms | Medium | Plausible inference; not explicitly confirmed |
| MUJ admissions hostname CNAMEs to `jaipurmanipal.nopaperforms.com` | High | Corroborated public DNS observation |
| DNS chain reaches an AWS ELB and three listed IPs | High | Public resolver observation at collection time |
| Admissions CRM directly feeds MUJ SLCM | Low to medium | Plausible but not demonstrated |
| Microsoft 365 is the SLCM identity provider | Low | Not established by reviewed public pages |
| MUJ-specific applicant data fields and retention | Low | Not publicly established |
| A credible public MUJ-specific NoPaperForms complaint was found | Low, negative finding | Not established in the reviewed corpus |
| Vendor platform supports CRM, application, payment, and integrations | High as vendor description | Publicly documented capability, not proof of MUJ configuration |

**Final verdict:** The public record supports a **high-confidence DNS and hostname relationship** between MUJ admissions and a NoPaperForms-named service, and a **high-confidence identification of MUJ SLCM as its academic student lifecycle platform**. It supports a **medium-confidence inference** that `npfslcm` means a NoPaperForms-related SLCM alias or integration. It does **not** publicly prove a direct admissions-to-academic-SLCM data pipeline, Microsoft 365 federation, Akamai deployment, database location, contractual data-processing roles, or a MUJ-specific CRM complaint.

For the university security club, the responsible conclusion is **confidence: medium overall, high for DNS facts, medium for vendor-semantic inference, and low for undocumented data-flow and complaint claims**. Publish the hostname and DNS findings with their limits, label the `npf` interpretation as inference, and direct the institution toward passive monitoring, documented ownership, privacy transparency, and authorized control review. Do not attempt unauthorized access, credential testing, endpoint enumeration, subdomain claiming, or collection of real applicant data.

## Exact URL Table

| ID | Exact URL | Evidence used |
|---|---|---|
| | http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf | MUJ SLCM name, modules, and student/parent single-window description |
| | https://crt.sh/?q=%25.jaipur.manipal.edu&output=json | Broader CT context for MUJ hostnames |
| | https://crt.sh/?q=npfslcm.jaipur.manipal.edu&output=json | Exact CT records for `npfslcm` and `mujslcm` certificate association |
| | https://mujslcm.jaipur.manipal.edu/ | MUJ portal title and visible login audience/domain |
| | http://api.ssllabs.com/api/v3/analyze?all=done&fromCache=on&host=mujslcm.jaipur.manipal.edu&maxAge=168 | Point-in-time IIS, ASP.NET MVC, and runtime observations |
| | https://dns.google/resolve?name=admissions.jaipur.manipal.edu&type=CNAME | Public CNAME response to `jaipurmanipal.nopaperforms.com` |
| | https://dns.google/resolve?name=admissions.jaipur.manipal.edu&type=A | Public recursive DNS chain and IP addresses |
| | https://www.ipaddress.com/website/admissions.jaipur.manipal.edu | Independent public DNS lookup confirmation |
| | https://urlscan.io/domain/admissions.jaipur.manipal.edu | Public hosting, age, IP, and scan-context observations |
| | https://www.nopaperforms.com/ | Official NoPaperForms product and platform scope |
| | https://www.meritto.com/ | Official CRM, enrollment, application, and integration descriptions |
| | https://www.meritto.com/application-automation/admission-form-payment-manager | Official application payment and gateway workflow claims |
| | http://developer.nopaperforms.com/ | Official API base URL, keys, methods, objects, and lead operations |
| | https://www.nopaperforms.com/press-release/nopaperforms-rebrands-its-flagship-product-to-meritto-signifying-expanding-platform-and-markets | Official June 2023 rebrand statement |
| | https://login.nopaperforms.io/privacy-policy | Vendor policy statement about collection through forms and applications |
| | http://trustcenter.nopaperforms.com/ | Vendor-published security and compliance claims |
| | https://www.meritto.com/client-testimonials | Vendor-hosted customer testimonials |
| | https://www.g2.com/sellers/nopaperforms | G2 review count and rating context |
| | https://www.g2.com/products/meritto/reviews | Meritto review ratings and visible pros/cons |
| | https://www.softwareadvice.com/admissions/comprehensive-admission-suite-profile/reviews | Software Advice rating and visible review context |
| | https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/Subdomain_takeover | Defensive CNAME lifecycle guidance |
| | https://owasp.org/API-Security/editions/2023/en/0x11-t10/ | Defensive API authorization and inventory guidance |

## Methodology and Chain-of-Thought Note

I cannot provide private chain-of-thought or hidden internal reasoning. The auditable substitute is the evidence method used here: identify atomic claims, compare direct DNS/CT observations with institutional and vendor statements, separate observations from inferences, test complaint searches for first-hand and entity-specific evidence, record unresolved questions, and assign confidence by claim rather than by overall narrative.

## References

1. *NoPaperForms is now Meritto! - YouTube*. https://www.youtube.com/watch?v=WK0bpShr54g
2. *NoPaperForms*. http://linkedin.com/company/nopaperforms
3. *NoPaperForms | Unified Technology Platform for Education*. https://www.nopaperforms.com/
4. *NoPaperForms Launches Collexo Pixi: A Smarter, Unified ...*. https://www.nopaperforms.com/press-release/nopaperforms-launches-collexo-pixi-a-smarter-unified-student-id-card-with-payments-transit-campus-access-and-more
5. *Media Kit*. https://www.nopaperforms.com/media-kit
6. *dns.google*. https://dns.google/resolve?name=admissions.jaipur.manipal.edu&type=CNAME
7. *NoPaperForms*. http://platform.tracxn.com/a/d/company/531a7746e4b0f7e1660fdb4d/nopaperforms#a:about
8. *Admissions*. https://jaipur.manipal.edu/admissions.php
9. *Meritto: The Most Trusted EdTech CRM for Student ...*. http://meritto.com/blog/meritto-the-most-trusted-edtech-crm-for-student-enrollment-admissions
10. *Admission & Semster Fee Payment Manager For Higher ...*. https://www.meritto.com/application-automation/admission-form-payment-manager
11. *Manipal University Jaipur | Manipal Academy of Higher ... Manipal Academy of Higher Education https://www.manipal.edu › important-links › manipal-uni...*. https://www.manipal.edu/mu/important-links/world-wide-manipal/manipal-university-jaipur.html
12. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
13. *Privacy Policy - Login - NoPaperForms*. https://login.nopaperforms.io/privacy-policy
14. *manipal university jaipur*. https://search.app.goo.gl/?al=googleapp%3A%2F%2Flens%3Flens_data=KAw&amv=301204913&apn=com.google.android.googlequicksearchbox&ct=4815459-oo-lens-isb-bar-lens-cam&ct=4815459-oo-lens-isb-bar-lens-cam&efr=1&ibi=com.google.GoogleMobile&ifl=https%3A%2F%2Fapps.apple.com%2Fus%2Fapp%2Fgoogle%2Fid284815942%3Fppid=1ac8cc35-d99c-4a1d-b909-321c8968cc74&isi=284815942&ius=googleapp&lens_data=KAw&link=https%3A%2F%2Fgoo.gl%2Fiosgoogleapp%2Fdefault%3Furl=googleapp%3A%2F%2Flens%3Fmin-version=180&mt=8&mt=8&ofl=https%3A%2F%2Flens.google&pt=9008&pt=9008
15. *Admissions 2026*. https://www.manipal.edu/mu/admission.html
16. *Applications Now Open for Faculty Position*. https://jaipur.manipal.edu/career-veiw.php?url=32%2Fapplications-now-open-for-faculty
17. *Manipal University Jaipur Admission 2026-27 | Apply Now!*. https://admissions.jaipur.manipal.edu/
18. *Manipal University - mujslcm.jaipur.manipal.edu*. https://mujslcm.jaipur.manipal.edu/Home/Index
19. *Online Application Form - Manipal University College Malaysia*. https://admissions.manipal.edu.my/
20. *Investor Relations - NoPaperForms*. http://nopaperforms.com/investor-relations
21. *Meritto Reviews: Customer Success Stories & Testimonials*. https://www.meritto.com/client-testimonials
22. *Meritto Reviews 2026: Details, Pricing, & Features*. https://www.g2.com/products/meritto/reviews
23. *NoPaperForms Products | Read 21 Reviews on G2*. https://www.g2.com/sellers/nopaperforms
24. *Meritto*. http://platform.tracxn.com/a/d/company/53aa3004e4b028b38bddb01f/meritto#a:about
25. *Seamless Virtual Post Application Platform*. https://www.nopaperforms.com/virtual-post-application-platform
26. *Privacy Policy - manipaldubai.com*. https://www.manipaldubai.com/privacy-policy
27. *Manipal University*. http://muj.slcm.jaipur.manipal.edu/
28. *NoPaperForms Solutions Ltd. - Trust Center - Security & Privacy*. http://trustcenter.nopaperforms.com/
29. *Manipal University Jaipur*. http://en.wikipedia.org/wiki/Manipal_University_Jaipur
30. *Meritto Reviews, Pros and Cons - 2026 Software Advice*. https://www.softwareadvice.com/admissions/comprehensive-admission-suite-profile/reviews
31. *About MUJ - Manipal University Jaipur*. http://jaipur.manipal.edu/about-muj.php
32. *API Documentation*. http://developer.nopaperforms.com/
33. *Meritto*. http://linkedin.com/company/meritto
34. *NoPaperForms: Features, Reviews & Alternatives | 2026 Cuspera Insights*. https://www.cuspera.com/products/nopaperforms-x-19367
35. *Education CRM for Enrollment Marketing Teams | Meritto (Formerly NoPaperForms)*. http://meritto.com/education-crm-for-enrollment-marketing-team
36.(http://shodan.io/host/98.70.14.50)
37. *Meritto Launches Student Admission Portal 3.0 to ...*. https://www.nopaperforms.com/press-release/meritto-launches-student-admission-portal-3-0-to-accelerate-admissions-and-reduce-cycle-time
38. *crt.sh*. https://crt.sh/?q=npfslcm.jaipur.manipal.edu&output=json
39. *api.ssllabs.com*. http://api.ssllabs.com/api/v3/analyze?all=done&fromCache=on&host=mujslcm.jaipur.manipal.edu&maxAge=168
40. *Meritto (A Product of NoPaperForms) | Purpose-built for Education*. http://meritto.com/
41. *admissions.jaipur.manipal.edu DNS Lookup & Website Information*. https://www.ipaddress.com/website/admissions.jaipur.manipal.edu
42. *NoPaperForms - 11486 Infostealer Credentials from Cybercrime ...*. https://www.hudsonrock.com/search/domain/nopaperforms.com
43.(http://shodan.io/host/20.244.94.89)
44. *admissions.jaipur.manipal.edu - urlscan.io*. https://urlscan.io/domain/admissions.jaipur.manipal.edu
45. *crt.sh*. https://crt.sh/?q=%25.jaipur.manipal.edu&output=json
46. *dns.google*. https://dns.google/resolve?name=admissions.jaipur.manipal.edu&type=A
47. *http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf*. http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf
48. *NoPaperForms rebrands its flagship product to Meritto, signifying expanding platform and markets - NoPaperForms*. https://www.nopaperforms.com/press-release/nopaperforms-rebrands-its-flagship-product-to-meritto-signifying-expanding-platform-and-markets
49. *Subdomain takeover - Security | MDN*. https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/Subdomain_takeover
50. *OWASP Top 10 API Security Risks – 2023 - OWASP API Security Top 10*. https://owasp.org/API-Security/editions/2023/en/0x11-t10/
