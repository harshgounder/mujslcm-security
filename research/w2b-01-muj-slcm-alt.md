# MUJ SLCM Alternate Host OSINT Assessment

## Executive Summary

- **Alternate Host Identity**: `muj.slcm.jaipur.manipal.edu` publicly presents a MUJ-branded sign-in page with the heading "WELCOME TO MUJ PORTAL" and a sign-in control. This establishes that the hostname serves a MUJ portal presentation, but it does not by itself establish whether the host is production, development, staging, or a reverse proxy [1]. -> Treat it as a live-looking institutional portal hostname, not as a confirmed development system.
- **Azure Address**: A current Google Public DNS snapshot resolves the alternate hostname to `20.244.94.89`, with a 3,600-second TTL; the response identifies the queried record as an A record [11]. -> Record the address as an observed DNS mapping, not as proof that the address is dedicated to MUJ.
- **Cloud Attribution**: RIPEstat maps `20.244.94.89` to AS8075 and the prefix `20.192.0.0/10` [12]. IPinfo labels the address `AS8075 Microsoft Corporation` and geolocates it to Pune, Maharashtra, India [13]. ARIN identifies the larger range as `20.192.0.0 - 20.255.255.255`, CIDR `20.192.0.0/10`, name `MSFT` [10]. -> The defensible conclusion is Microsoft-operated address space, not a confirmed Azure App Service, VM, or tenant.
- **Same Application Family**: Passive captures of the alternate and primary pages show the same page title, generic description, MUJ portal heading, login design, Keen asset paths, ASP.NET-style form fields, and Microsoft password-reset destination. The primary capture includes the same login flow concepts and the `@muj.manipal.edu` student domain [2] [1]. -> The evidence strongly supports a shared application template or release family.
- **Official SLCM Reference**: MUJ's publicly indexed SLCM FAQ identifies `https://mujslcm.jaipur.manipal.edu/` as the registration link and discusses AMS login support [3]. The FAQ does not name the alternate hostname in the visible extract [3]. -> The primary hostname is the only one publicly confirmed by the official FAQ as the SLCM registration endpoint.
- **Primary Host Address**: The primary hostname resolves in the observed DNS snapshot to `98.70.14.50` [14]. RIPEstat maps that address to AS8075 and `98.70.0.0/15` [15]. IPinfo likewise labels it `AS8075 Microsoft Corporation` [16]. -> Both hostnames currently appear in Microsoft-associated address space, but they use different address ranges.
- **Akamai Status**: The collected public evidence does not independently establish that the primary hostname is currently behind Akamai. Search results found general Akamai documentation, but no target-specific Akamai header, DNS alias, or authoritative MUJ statement [2]. -> Treat "Akamai-fronted" as an assessment input or prior observation, not as independently proven by this OSINT pass.
- **Public Exposure Difference**: URLScan's public API search for the alternate returns zero results [17], while the primary has a public scan record showing `98.70.14.50` and a public scan page [18]. -> This is a difference in public observation coverage, not evidence that the alternate is private, unused, or a development instance.
- **Security Significance**: The alternate's direct Microsoft-associated address increases the importance of asset inventory and ownership confirmation, because it may represent a separate origin, migration endpoint, alternate binding, or independent deployment. Nothing collected proves origin exposure, shared data, authentication equivalence, or a vulnerability. -> The appropriate club output is a responsible disclosure-oriented asset relationship report, not an access attempt.

## Scope, Ethics, and Evidence Standard

This report is limited to publicly available material returned by search, passive DNS and registry records, public certificate or scan indexes, public web-page captures, and publicly accessible MUJ documents. It does not attempt authentication, password testing, endpoint enumeration, port scanning, origin discovery, header manipulation, bypasses, exploitation, or access to student, parent, faculty, or administrative data. A login page is treated as a public presentation artifact only. The presence of a form, anti-forgery token, or password-reset link is not treated as authorization to submit data.

The evidence standard separates three levels. First, an **observation** is something directly stated in a public record, such as an A record, visible page title, or official document URL. Second, a **corroborated observation** is supported by more than one independent public source, such as Microsoft attribution from RIPEstat, ARIN, and IPinfo. Third, an **inference** is a reasoned interpretation of multiple observations. Inferences in this report are explicitly labelled and do not replace confirmation by MUJ or its hosting provider.

The report also avoids a common OSINT error: treating infrastructure ownership as application ownership. Microsoft may operate an address range without being the application owner, and a university may use Microsoft infrastructure without owning the cloud account. Similarly, identical HTML may result from a shared codebase, copied template, common deployment package, or a deliberate replica. It does not prove that both names reach the same server process or database.

## Hostname and Public Page Identity

The alternate page is publicly titled "Manipal University" and visibly states "WELCOME TO MUJ PORTAL" followed by "Sign In" [1]. Search indexing independently returns the same alternate hostname with the MUJ portal wording and `@jaipur.manipal.edu` text [1]. These are direct indications that the hostname is not merely an unrelated Microsoft landing page. They establish branding and intended audience, but not operational ownership or environment tier.

The primary page likewise carries the title "Manipal University" and the visible MUJ portal heading [2]. Search indexing shows the primary page with parent and student sign-in labels [2]. The official MUJ FAQ gives the primary hostname as the SLCM registration link, which is stronger institutional evidence than a search result or a page title [3].

The two public pages differ in visible email-domain context. The alternate page capture shows `@jaipur.manipal.edu` [1], while the primary page capture includes `@muj.manipal.edu` [2]. The server-returned HTML comparison also shows login logic that sets `EmailFor` to `@jaipur.manipal.edu` for one login path and `@muj.manipal.edu` for another [1]. This difference should not be overinterpreted. It may reflect a faculty-versus-student routing choice, a configuration difference, a version difference, or a page-state difference. It does not establish separate applications.

| Publicly observed property | Alternate: muj.slcm.jaipur.manipal.edu | Primary: mujslcm.jaipur.manipal.edu | Assessment |
|---|---|---|---|
| Page title | Manipal University [1] | Manipal University [2] | Same visible title |
| Main branding | WELCOME TO MUJ PORTAL [1] | WELCOME TO MUJ PORTAL [2] | Same visible branding |
| Login presentation | Sign In [1] | Sign In and parent login [2] | Same family of login UI |
| Email-domain text | @jaipur.manipal.edu [1] | @muj.manipal.edu [2] | Configuration or role difference possible |
| Password reset | Microsoft password-reset destination visible in the captured form [1] | Same destination visible in the primary form capture [19] | Same identity ecosystem signal |
| Official SLCM designation | Not found in the official FAQ extract | Official FAQ registration link [3] | Primary has stronger official confirmation |

The table supports a **same-family** conclusion, not a **same-backend** conclusion. A responsible analyst should preserve that distinction in any ticket or report.

## DNS, IP, and Cloud Attribution

Google Public DNS returned an A record for the alternate hostname with the exact value `20.244.94.89` and a TTL of 3,600 seconds [11]. The same query's authority information references Azure DNS nameservers in the `manipal.edu` zone [20]. The queried CNAME response returned no CNAME answer and instead showed the zone authority [21]. The queried AAAA response similarly showed no IPv6 answer in the returned data [22]. These observations describe the resolver response at the collection time; they are not a guarantee that DNS will remain unchanged.

RIPEstat independently maps `20.244.94.89` to AS8075 and prefix `20.192.0.0/10` [12]. ARIN's record describes that range as `20.192.0.0 - 20.255.255.255`, CIDR `20.192.0.0/10`, name `MSFT`, and handle `NET-20-192-0-0-1` [10]. IPinfo labels the individual address `AS8075 Microsoft Corporation`, with a Pune, Maharashtra, India geolocation [13]. The location should be understood as a geolocation database result, not proof of the physical server location.

| DNS or registry item | Alternate value | Primary value | What it supports |
|---|---:|---:|---|
| A record | 20.244.94.89 [11] | 98.70.14.50 [14] | Distinct observed IPv4 mappings |
| Observed TTL | 3,600 seconds [11] | 3,600 seconds [14] | Snapshot cache lifetime, not deployment age |
| RIPEstat ASN | 8075 [12] | 8075 [15] | Same Microsoft-associated ASN |
| RIPEstat prefix | 20.192.0.0/10 [12] | 98.70.0.0/15 [15] | Different Microsoft-associated prefixes |
| IPinfo organization | AS8075 Microsoft Corporation [13] | AS8075 Microsoft Corporation [16] | Independent cloud/network attribution |
| CNAME response | No CNAME answer shown [21] | No CNAME answer shown [23] | No public alias in the queried response |
| AAAA response | No AAAA answer shown [22] | No AAAA answer shown [24] | No IPv6 answer in those snapshots |

**Inference:** the alternate and primary are both hosted or fronted by infrastructure in Microsoft-associated address space, but their distinct prefixes could reflect different services, regions, resource allocations, or ordinary address management. They do not prove two application stacks, and they do not prove that either address is a dedicated origin.

## What the HTML Similarity Shows

The passive server-returned HTML comparison is the strongest evidence linking the two endpoints at the application-family level. Both captures include the same `Manipal University` title and `User login example` description, and both reference the Keen login theme and common asset paths [2] [1]. Both contain the same broad form vocabulary, including username and password controls, and both expose the Microsoft password-reset destination [1] [19].

The primary page's capture includes an ASP.NET-style request-verification field and form inputs named `EmailFor`, `LoginFor`, `UserName`, and `Password` [19]. The alternate page's server-returned HTML includes the same general login structure and the same script and theme conventions [1]. These details are compatible with a common MVC application package or common institutional portal product. They are not proof that requests are handled by one backend, because two independently deployed applications can share all static assets and view templates.

| Similarity indicator | Public observation | Strength of inference |
|---|---|---|
| Title and description | Same `Manipal University` title and `User login example` description [2] [1] | Strong same-template signal |
| MUJ branding | Same `WELCOME TO MUJ PORTAL` heading [2] [1] | Strong same-purpose signal |
| Theme assets | Same Keen login asset family and path pattern [1] | Strong code or deployment-family signal |
| Form vocabulary | Username, password, login-role fields visible in captures [1] [19] | Moderate-to-strong same-flow signal |
| Microsoft identity | Password reset points to `passwordreset.microsoftonline.com` [1] [19] | Shared identity ecosystem signal |
| Backend destination | Not established by the public captures | No conclusion permitted |
| Database or tenant | Not established by the public captures | No conclusion permitted |

**Inference:** the most economical explanation is that the alternate is another binding or deployment of the MUJ SLCM portal family. However, "same app" should be used only with the qualifier "same visible application family or template." The evidence cannot distinguish a production alias, an old deployment, a staging deployment, a migration target, or a parallel role-specific service.

## Official Documents and Public Mentions

The official MUJ SLCM FAQ is the most important public document located. It is titled "Frequently Asked Questions and Contacts for SLCM Registration" and states `Registration Link: https://mujslcm.jaipur.manipal.edu/` [3]. It discusses AMS login problems and directs users to re-check credentials [3]. The same extract provides MUJ contact channels, including `dms@jaipur.manipal.edu` and `ams@jaipur.manipal.edu` [3].

The FAQ therefore confirms an operational relationship between the primary hostname and MUJ's SLCM/AMS workflow. It does not name `muj.slcm.jaipur.manipal.edu` in the visible extract [3]. That absence should be reported narrowly: no alternate-host reference was found in this document, not that MUJ has never documented the alternate anywhere.

The official Microsoft 365 setup document is relevant to identity context but does not establish the alternate host's application role. It is a MUJ IT Services standard operating procedure for setting up Office 365 mail, identified as version 1.0 and effective June 2025, for students and employees [5]. It states that MFA is mandatory before Office 365 use [5] and describes Microsoft sign-in, password reset, and alternative MFA methods [5] [5]. This supports the observation that Microsoft identity is part of MUJ's public account ecosystem. It does not prove that the SLCM login itself is implemented as Microsoft federated authentication.

Search results also surfaced public GitHub material. One directory is named `mujslcm.jaipur.manipal.edu_122` and visibly contains paths such as `Home/`, `Scripts/`, and Keen theme assets [4]. This is useful as a public mention and as corroboration that the same asset naming is circulating publicly. It is not an official MUJ repository, and the public directory does not prove that the author owned the application, that the content was obtained lawfully, or that it represents the current production deployment. A separate repository named `muj_slcm` is indexed with a single commit and top-level files including `README.md`, `requirements.txt`, and a project directory [25]. It should likewise be treated as an unverified third-party reference.

| Source category | Exact public item | Finding | Reliability for deployment-role claims |
|---|---|---|---|
| Official MUJ PDF | SLCM FAQ [3] | Names primary registration link and AMS support | High for primary URL; silent on alternate |
| Official MUJ PDF | Office 365 SOP [5] | Documents Microsoft identity, password, and MFA procedures | High for M365 process; not SLCM topology |
| Public portal page | Alternate login [1] | Shows MUJ portal branding and sign-in | High for visible presentation; low for backend role |
| Public portal page | Primary login [2] | Shows same MUJ portal family | High for visible presentation; low for backend role |
| Third-party GitHub | Saved directory [4] | Contains host-named path and portal-like assets | Low for ownership or production status |
| URLScan | Alternate domain page [8] | Public observation summary but no public scan result | Low for current operational conclusions |

## Relationship to the Primary Host and Akamai Question

The primary hostname has several public indicators of institutional use. The live-looking page is MUJ-branded [2], and the official FAQ publishes it as the SLCM registration link [3]. Its A record is `98.70.14.50` [14], and both RIPEstat and IPinfo associate the address with AS8075 and Microsoft Corporation [15] [16]. A public URLScan result page also identifies `98.70.14.50` for the primary host [18].

The alternate has a parallel but weaker public record. Its page is MUJ-branded [1], its A record is `20.244.94.89` [11], and its address is independently attributed to Microsoft's AS8075 [12] [13]. Yet the official FAQ does not list it [3], and URLScan's public API search returns zero results for the exact alternate domain [17]. The difference is best described as an evidence asymmetry.

The supplied research scope describes the primary as Akamai-fronted, but this pass did not retrieve target-specific evidence sufficient to independently verify that claim. The search results for Akamai were generic vendor documentation and an unrelated Akamai technical page, not a MUJ-specific DNS alias or response record [2]. A public scan page for the primary identifies the IP and scan metadata, but the visible extract does not itself state Akamai [18]. Therefore, this report does not assert that the primary is currently behind Akamai, nor does it assert that the alternate bypasses Akamai. Both remain open topology questions.

Several architectures are consistent with the observations:

1. **Two hostnames, one application family, separate Microsoft front ends.** Each name could be bound to a different cloud resource or address while sharing code and identity configuration.
2. **A primary CDN path plus a separate alternate binding.** The primary could be CDN-fronted while the alternate points directly to a Microsoft service. This is plausible but unproven because the target-specific Akamai evidence was not recovered.
3. **Migration or legacy coexistence.** One host could be newer, older, or role-specific. The similar HTML would remain expected if both deployments came from the same release package.
4. **Shared reverse proxy or load-balancer architecture.** Different public A records could still feed a common logical service, but no public evidence proves that relationship.
5. **Non-production deployment.** The alternate could be development or staging, but the public page and address alone do not establish that label.

| Hypothesis | Supporting observations | Contradicting or missing evidence | Status |
|---|---|---|---|
| Same visible application family | Identical branding, title, description, assets, and login concepts [2] [1] | No source-code or deployment declaration | Strong inference |
| Same backend/database | Similar form and identity behavior | No public backend, connection, tenant, or database evidence | Unknown |
| Alternate is dev/staging | Separate hostname and IP | No official dev/staging label; page is fully branded | Unproven |
| Alternate is a backend/origin | Microsoft A record and distinct prefix | No origin declaration; cloud IP may be proxy or shared service | Unproven |
| Primary is Akamai-fronted | User-provided scope; generic Akamai context | No target-specific Akamai DNS/header evidence retrieved | Not independently verified |
| Alternate bypasses Akamai | Direct Microsoft-associated A record | A record alone cannot establish request path or CDN policy | Unproven |

## Risk Interpretation for a University Security Club

The main defensible security finding is **asset relationship uncertainty**, not a vulnerability. An institution may have multiple public hostnames presenting nearly identical login interfaces. If their lifecycle, ownership, authentication policy, logging, patching, and data boundary differ, users and defenders may not know which endpoint is authoritative. The official FAQ currently gives the primary URL, while the alternate is publicly discoverable and branded similarly [3] [1]. That mismatch warrants an owner-confirmed inventory review.

The second issue is **cloud-boundary ambiguity**. Both observed A records are in Microsoft-associated space, but in different prefixes [11] [14] [12] [15]. This may be normal multi-resource hosting. It may also reflect a migration, independent application service, or direct cloud binding. The data cannot distinguish these cases. The correct defensive action is therefore confirmation of resource ownership and intended traffic flow, not an attempt to compare responses aggressively.

The third issue is **identity presentation consistency**. The pages reference Microsoft password reset and show MUJ email-domain logic [1] [19]. The official M365 SOP confirms that MUJ uses Microsoft sign-in, password reset, and MFA procedures for university accounts [5] [5]. This makes it important for the owner to verify whether both hostnames enforce the same identity policies, but it does not authorize anyone to test credentials or MFA behavior.

Recommended responsible next steps for an authorized owner are administrative and passive: confirm which hostname is canonical; document the business purpose of every DNS record; confirm whether `20.244.94.89` is an intended Microsoft resource; verify whether the alternate is production, migration, staging, or retired; document CDN-to-origin routing; and remove or redirect obsolete public bindings after change approval. If a security club submits a report, it should include the exact public URLs and timestamps of observations, avoid credentials and personal data, and request an official contact for validation.

## Evidence Gaps and What Cannot Be Claimed

The evidence does not prove that the alternate is a development instance. A development label requires an official configuration record, a public institutional statement, or a clearly attributable deployment artifact. None was found in the collected public material. The evidence does not prove that the alternate is a backend. DNS points to an address, not to a role in an application architecture. The evidence does not prove a shared database, session store, identity tenant, or code repository.

The evidence also does not prove that the alternate is an Akamai bypass. A CDN can coexist with direct-looking DNS records, and a Microsoft-associated address can represent a proxy, application gateway, hosted service, or origin. Conversely, the absence of a public CNAME in the resolver result does not rule out CDN behavior implemented through other DNS or provider arrangements. The queried data shows no CNAME answer in those snapshots [21] [23], but that is not a complete topology map.

Finally, public URLScan coverage is not a liveness or ownership test. The alternate domain search returns zero public results [17], while the primary has a public result. This difference may reflect submission history, indexing, policy, or scan timing. It cannot be used to classify the alternate as hidden or non-production.

## VERDICT

**Overall confidence: Moderate for the narrow conclusion that `muj.slcm.jaipur.manipal.edu` is a MUJ-branded SLCM-family login endpoint; low-to-moderate for any deeper infrastructure relationship.**

The strongest supported conclusion is: **the alternate hostname publicly presents the same visible MUJ portal family as `mujslcm.jaipur.manipal.edu`, resolves to `20.244.94.89` in Microsoft-associated AS8075 address space, and is likely a separate hostname or binding belonging to the same application family.** The word "likely" is important. Identical public HTML, branding, assets, form vocabulary, and Microsoft password-reset linkage provide strong same-template evidence [2] [1] [19], but they do not prove shared backend, database, deployment tier, or production status.

The primary hostname has stronger institutional confirmation because MUJ's official SLCM FAQ publishes it as the registration link [3]. The alternate is not named in that visible official document [3]. Its observed Microsoft address is corroborated by RIPEstat, ARIN, and IPinfo [12] [10] [13], but those sources establish network allocation, not MUJ tenant ownership.

**Final disposition:** classify the alternate as **Public MUJ SLCM-family endpoint, operational role unconfirmed**. Do not classify it as "dev," "staging," "backend," "origin," or "Akamai bypass" without owner confirmation. The Akamai-fronting claim remains **not independently verified in this collection**. No vulnerability is established by the public evidence reviewed.

## References

1. *Manipal University*. https://muj.slcm.jaipur.manipal.edu/
2. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
3. *Frequently Asked Questions and Contacts for SLCM Registration*. https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf
4. *college_portal_web_and_dbms/mujslcm.jaipur.manipal.edu_122 at main · vikrant500/college_portal_web_and_dbms · GitHub*. https://github.com/vikrant500/college_portal_web_and_dbms/tree/main/mujslcm.jaipur.manipal.edu_122
5. *Standard Operating Procedure*. https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf
6. *mujslcm.jaipur.manipal.edu - urlscan.io*. https://urlscan.io/domain/mujslcm.jaipur.manipal.edu
7. *stat.ripe.net*. https://stat.ripe.net/data/whois/data.json?resource=20.244.94.89
8. *muj.slcm.jaipur.manipal.edu - urlscan.io*. https://urlscan.io/domain/muj.slcm.jaipur.manipal.edu
9. *urlscan.io*. https://urlscan.io/api/v1/search/?q=domain:mujslcm.jaipur.manipal.edu
10. *Whois-RWS*. https://whois.arin.net/rest/ip/20.244.94.89
11. *dns.google*. https://dns.google/resolve?name=muj.slcm.jaipur.manipal.edu&type=A
12. *Network Info*. https://stat.ripe.net/data/network-info/data.json?resource=20.244.94.89
13. *ipinfo.io*. https://ipinfo.io/20.244.94.89/json
14. *dns.google*. https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=A
15. *Network Info*. https://stat.ripe.net/data/network-info/data.json?resource=98.70.14.50
16. *ipinfo.io*. https://ipinfo.io/98.70.14.50/json
17. *urlscan.io*. https://urlscan.io/api/v1/search/?q=domain:muj.slcm.jaipur.manipal.edu
18. *mujslcm.jaipur.manipal.edu - urlscan.io*. https://urlscan.io/result/019ed038-c4af-765c-9499-2da69a77e30a/
19. *Manipal University*. http://mujslcm.jaipur.manipal.edu/
20. *dns.google*. https://dns.google/resolve?name=muj.slcm.jaipur.manipal.edu&type=NS
21. *dns.google*. https://dns.google/resolve?name=muj.slcm.jaipur.manipal.edu&type=CNAME
22. *dns.google*. https://dns.google/resolve?name=muj.slcm.jaipur.manipal.edu&type=AAAA
23. *dns.google*. https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=CNAME
24. *dns.google*. https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=AAAA
25. *GitHub - Anushkakumar10/muj_slcm*. http://github.com/Anushkakumar10/muj_slcm
