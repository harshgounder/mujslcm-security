# MUJ SLCM Hostname Attribution and Exposure Report

## Executive Summary

- **Parent Host Resolves**: `mujslcm.manipal.edu` currently has an A record of **202.131.155.151**, but the public DNS response contains no AAAA answer and no answer for the queried CNAME, HTTPS, TXT, MX, or NS types. [2] [3] [8] [11] [9] [7] [10] -> Treat the hostname as an asset requiring owner confirmation, not as a confirmed live application.
- **Child Host Is the Evidenced MUJ Portal**: The official MUJ FAQ identifies `https://mujslcm.jaipur.manipal.edu/` as the SLCM registration link. [17] -> Make the Jaipur hostname the primary application record in the university asset inventory.
- **Child Application Is Publicly Reachable**: Public scans recorded HTTP 200 responses for `mujslcm.jaipur.manipal.edu` in November 2024, January 2026, and June 2026. [14] [16] [15] -> Verify the service is still institutionally required and maintain it as a production identity-bearing application.
- **Child Technology Is Strongly Fingerprinted**: The June 2026 scan reports `x-aspnetmvc-version: 5.3`, `x-aspnet-version: 4.0.30319`, `Microsoft-IIS/10.0`, and named client-side technologies including Font Awesome and jQuery. [15] [15] -> Track the application as legacy ASP.NET MVC technology, but do not claim that the parent hostname has the same stack.
- **Akamai Is Not Demonstrated**: The public child scans identify Microsoft IIS and Microsoft ASN 8075, and do not explicitly identify Akamai. [15] [16] [16] -> Reconcile the supplied Akamai assertion against authoritative DNS, CDN configuration, and internal architecture records before treating it as fact.
- **Microsoft Identity Evidence Is Limited**: The child scan records a `passwordreset.microsoftonline.com` destination titled "Forgot Password?" but does not establish that the login itself is Microsoft 365 federation. [16] [16] [15] [15] -> Document this as Microsoft-linked password recovery, not as proof of OIDC, SAML, Azure AD, or Microsoft 365 authentication.
- **Parent Has No Observed Archive or Scan Footprint**: Wayback CDX returned `[]` for both the parent hostname and its wildcard path scope, URLScan returned zero results, and Certificate Spotter returned `[]`. [1] -> The absence supports an orphaned or minimally used public asset hypothesis, but does not prove non-use or malicious registration.
- **Child Has Historical Continuity**: Wayback recorded successful 200 captures of the child root on **2025-05-27** and `/Home/Index` on **2025-01-10**, along with CSS, JavaScript, image, and favicon assets. [19] -> The child is not merely a newly created lookalike in the public record.
- **Classification Remains Unresolved**: The evidence supports an official MUJ relationship for the Jaipur child, while no public evidence connects the parent `.151` address to that application. [17] [2] [12] -> Classify the parent as **unattributed / ownership confirmation required**, not as a confirmed backup, old host, or squat.

This report uses public DNS responses, public web pages, public certificate-transparency queries, public URLScan records, and public web archives. It does not attempt authentication, bypass controls, enumerate private application functions, submit forms, exploit endpoints, or infer confidential university architecture. The requested chain-of-thought is not reproduced; instead, the report provides an auditable evidence trail, confidence labels, and concise analytical reasoning.

## Scope, Definitions, and Evidence Model

The target set contains three materially different names: `mujslcm.manipal.edu`, `mujslcm.jaipur.manipal.edu`, and `muj.slcm.jaipur.manipal.edu`. The first is the parent-level hostname under review. The second is the hostname explicitly named by the MUJ FAQ. [17] The third is a closely related sibling spelling that presents the same broad MUJ portal branding in search results and public page extraction. [5] [6]

The analysis distinguishes four evidence states. **Observed** means the exact public source states the fact. **Not observed** means the searched source returned no relevant record, such as an empty URLScan or CDX result. **Not established** means a source contains a related clue but not enough to prove the stronger claim. **Inference** means an analyst interpretation built from observed facts; it is labeled as such and is not presented as institutional confirmation.

A negative result is narrower than it may appear. A zero-result URLScan query does not prove that a hostname never existed, was never scanned privately, or cannot answer from another network path. An empty Internet Archive CDX response does not prove that the hostname was never online. Similarly, no certificate result from a public CT service does not prove that no certificate was ever issued, because certificates may be absent from a queried service, outside its indexing window, or issued under another name. These limitations are why the report does not call the parent a squat solely because its public footprint is sparse.

The report also treats IP addresses as observations rather than ownership proof. The parent hostname resolves to `202.131.155.151`. [2] Passive reverse DNS maps that address to `202.131.155.151.convergentindia.com`; the sibling historical address `202.131.155.150` maps similarly. [12] [13] Reverse DNS is an operator or hosting clue, not proof that the university owns the address or that both addresses served the same software.

## exact_tables

### Table 1. Target host comparison

| Hostname | Public role evidence | DNS or scan evidence | Archive / certificate evidence | Assessment |
|---|---|---|---|---|
| `mujslcm.manipal.edu` | No public page, title, or portal function was recovered from the passive checks in this research. | A record `202.131.155.151`; no public AAAA answer. [2] [3] No CNAME, HTTPS, TXT, MX, or NS answer appeared in the queried responses. [8] [11] [9] [7] [10] | Wayback exact-host and wildcard CDX queries returned `[]`. URLScan returned zero results. [1] Certificate Spotter returned `[]`. | Unattributed parent-level asset; live application status unconfirmed. |
| `mujslcm.jaipur.manipal.edu` | MUJ's public FAQ names it as the SLCM registration link. [17] The page is branded `WELCOME TO MUJ PORTAL` and exposes student/parent sign-in choices. [4] | Public scans report HTTP 200, Microsoft IIS/10.0, ASP.NET MVC 5.3, ASP.NET version 4.0.30319, and IP `98.70.14.50`. [15] [15] | Wayback has 2025 captures of the root and `/Home/Index`. [19] CT material and public URLScan records exist for the child. [26] [18] | Strongly evidenced official MUJ SLCM application. |
| `muj.slcm.jaipur.manipal.edu` | Public extraction shows `WELCOME TO MUJ PORTAL`, `Sign In`, and `Parent Login`. [5] [6] | No independent parent-level linkage was established in this research. | No separate archive conclusion is drawn here. | Related sibling hostname; relationship to the main child requires owner confirmation. |
| `slcm.manipal.edu` | Public search identifies it as `Manipal Academy of Higher Education - MU SLcM`. [20] | The page identifies MAHE rather than MUJ. [20] | Not used as evidence about the parent hostname. | Separate MAHE-branded portal, not evidence that the parent `.151` host is MUJ. |

**Table takeaway:** The public evidence is asymmetric. The Jaipur child has institutional, functional, technical, and archive evidence; the parent has DNS evidence but no corresponding application evidence. That asymmetry is the central attribution fact.

### Table 2. Publicly observed technical indicators

| Indicator | Child observation | Parent observation | Interpretation |
|---|---|---|---|
| HTTP response | HTTP 200 in public scans. [16] [15] | No extracted HTTP page or scan result. | Parent availability is unknown, not proven down. |
| Web server | `Microsoft-IIS/10.0 / ASP.NET`. [15] | Not observed. | Do not transfer the child server fingerprint to the parent. |
| Framework header | `x-aspnetmvc-version: 5.3`; `x-aspnet-version: 4.0.30319`. [15] | Not observed. | The supplied MVC claim is supported for the child scan, not for `.151`. |
| IP and network | `98.70.14.50`, AS8075, Microsoft Corporation, US. [15] [15] [15] | `202.131.155.151`; reverse DNS `202.131.155.151.convergentindia.com`. [2] [12] | Different observed network endpoints; this does not by itself prove different ownership or a backup relationship. |
| TLS | Entrust DV TLS Issuing RSA CA 2 in 2026 scans. [16] [15] [15] | No Certificate Spotter issuance returned for exact parent query. | Child has observed TLS continuity; parent TLS is not evidenced by this query. |
| CDN / proxy | Akamai not explicitly identified in the public scan pages. [16] [16] | Not observed. | Akamai remains an unverified supplied assertion. |
| Identity clue | `passwordreset.microsoftonline.com` link titled `Forgot Password?`. [16] [16] [15] [15] | Not observed. | Microsoft-linked recovery exists; federation protocol and tenant configuration are not proven. |
| Client-side assets | Font Awesome, Google Font API, jQuery; the page markup also references jQuery 1.10.2, validation libraries, and a Keen theme. [16] [6] | Not observed. | Publicly observed child dependencies should be inventoried and maintained; no parent inference is justified. |

**Table takeaway:** The child fingerprint is specific enough for asset inventory and defensive review, but it should not be used as a proxy fingerprint for the parent. The absence of parent indicators is itself a finding about observability, not a software-version determination.

## Purpose and Institutional Relationship

The strongest purpose evidence is first-party. The PDF is titled **Frequently Asked Questions and Contacts for SLCM Registration**, and its registration link is `https://mujslcm.jaipur.manipal.edu/`. [17] The same material discusses AMS login problems and instructs users to re-verify credentials. [17] This establishes that the Jaipur hostname was publicly presented by a MUJ source as part of SLCM registration and access support.

The child page's visible interface is consistent with that purpose. It says `WELCOME TO MUJ PORTAL` and offers `Sign In`; the extracted page also exposes `Parent Login` and a student-login path. [4] A public HTML readout shows a POST form directed to the child root, username and password fields, and client-side validation references. [6] These observations support the description "identity-bearing student/parent portal login" without claiming anything about post-authentication functions or data.

The term SLCM ordinarily denotes a student lifecycle management system. SAP's official documentation describes Student Lifecycle Management as accounting for university resources and academic work completed by students. [27] A separate public MUJ student-platform result describes the MUJ SLCM portal as providing registration details, grades, fee receipts, and official functions, but that result is not used to assert the internal design of the target application. [28] The conservative conclusion is that the child is an academic administration and registration portal, while the exact feature set should be confirmed by the university or by authorized documentation.

The related `slcm.manipal.edu` portal should not be collapsed into the MUJ child. Its public title is `Manipal Academy of Higher Education - MU SLcM`, and it identifies MAHE with a 2017 copyright notice. [20] That is evidence of a separate MAHE-branded portal page, not evidence that it is the parent-level host or that the parent is a shared backend. The name similarity is expected within a university ecosystem and is not, by itself, proof of common hosting.

**Inference:** The Jaipur child is very likely the official MUJ SLCM access point because a MUJ-owned FAQ names it as the registration link and the page carries MUJ portal branding. [17] [4] The parent `mujslcm.manipal.edu` is not shown in the same first-party material. Therefore, public evidence does not establish that the parent is the old MUJ portal, a backup, or a current alias.

## Technology Findings and the Akamai / Microsoft Claims

The child technology claim is unusually well supported by passive evidence. A June 16, 2026 public scan reports `x-aspnetmvc-version: 5.3`, `x-aspnet-version: 4.0.30319`, and `Microsoft-IIS/10.0`. [15] The same scan reports HTTP 200 and the child endpoint at `98.70.14.50`. [15] A January 15, 2026 scan independently reports the same ASP.NET/IIS family, the same effective IP, and the same Microsoft ASN. [16] [16] [16]

The version string must be handled precisely. `4.0.30319` is an observed ASP.NET version header value; it is not, by itself, proof that the application runs exactly on .NET Framework 4.0. Microsoft's support policy says .NET Framework 4.0 is inactive and reached end of support on January 12, 2016, while later .NET Framework versions have different support treatment. [25] [25] The public scan does not disclose the installed Windows version, actual runtime patch level, application dependencies, or whether an intermediary rewrote headers. Accordingly, the report records the header, does not equate it with a full platform bill of materials, and recommends owner-side validation.

The supplied Akamai assertion is not corroborated by the public child scans used here. The June 2026 result names Microsoft IIS, Microsoft ASN 8075, and Microsoft Corporation, while the explicit technology list names Font Awesome and jQuery. [15] [15] The January result likewise reports Microsoft IIS, Microsoft ASN 8075, and the same effective IP. [16] Neither result explicitly names Akamai. This does not prove that Akamai is absent: a CDN or upstream service may be invisible to a particular scan, may apply only to another hostname, or may have changed. It does mean that "behind Akamai" is **not established by the cited public evidence**.

The Microsoft 365 identity assertion is also narrower than the public clue. The child page has a password-reset destination on `passwordreset.microsoftonline.com`, and URLScan labels it as a Forgot Password link. [16] [16] That supports a Microsoft-linked account recovery workflow. It does not demonstrate that the portal uses Microsoft 365 as its primary identity provider, nor does it establish SAML, OAuth, OIDC, Azure AD, Entra ID, conditional access, or tenant ownership. An application can direct users to a Microsoft password-reset service while still implementing its own application login or a separate integration.

**Defensive implication:** The application inventory should record two separate fields: `observed technology headers` and `owner-confirmed runtime architecture`. The former can contain ASP.NET MVC 5.3, ASP.NET 4.0.30319, IIS 10, jQuery, and the observed TLS provider. [15] [15] The latter should remain pending until the university confirms framework patching, reverse-proxy/CDN topology, identity protocol, and supported operating system.

## Current State and Historical Presence

The parent currently resolves in Google Public DNS to `202.131.155.151` with a 300-second TTL in the captured response. [2] Its AAAA query returned no AAAA answer and only an SOA authority response for `manipal.edu`. [3] The CNAME, HTTPS, TXT, MX, and NS queries likewise showed no answer section in the captured responses. [8] [11] [9] [7] [10] A DNS name can therefore be delegated or configured to return an A record while exposing no additional records in these queries; that pattern does not identify the application behind the address.

The parent has no recovered public web page in this research. Direct extraction of HTTP and HTTPS URLs produced no citations, and URLScan's exact-domain API response contained `results: []`, `total: 0`, and `has_more: false`. [1] Certificate Spotter's exact-host query returned an empty list. A direct CT query through crt.sh returned a 404 response rather than certificate data, so it should be treated as an unavailable query result, not as proof of absence. [29] The stronger parent CT statement in this report is limited to the Certificate Spotter empty result.

The parent also has no Internet Archive CDX captures in the tested scopes. The exact-host query returned `[]`, and the wildcard path query returned `[]`. This is a meaningful lack of public historical visibility, especially when contrasted with the child. The child archive includes a root capture at `20250527044058`, an `/Home/Index` capture at `20250110135954`, and multiple successful static assets. [19] The child therefore has a documented historical web presence; the parent does not in the checked archive scopes.

The child was also live in public scans at multiple points. A November 20, 2024 scan reached `https://mujslcm.jaipur.manipal.edu:122/` and returned 200 OK from `202.131.155.150`, with Microsoft IIS 8.5 and an Entrust certificate authority. [14] [14] [14] A January 15, 2026 scan reached the standard HTTPS child URL, returned 200, and reported Microsoft IIS 10.0 at `98.70.14.50`. [16] [16] A June 16, 2026 scan again returned 200 with the same child IP and IIS 10. [15] [15]

The change from `202.131.155.150` and IIS 8.5 in 2024 to `98.70.14.50` and IIS 10 in 2026 is an observed infrastructure difference. [14] [15] **Inference:** it may reflect migration, proxying, hosting change, or scan-path differences, but it does not prove that the parent `.151` address is the old child server. The numerical adjacency of `.150` and `.151` is not sufficient evidence of common ownership or a backup relationship.

## Relationship Analysis: Old Host, Backup, Alias, or Squat?

### Table 3. Hypothesis matrix

| Hypothesis | Evidence supporting it | Evidence against or missing | Confidence |
|---|---|---|---|
| Parent is the old MUJ SLCM | The parent name is semantically similar to the child and resolves within the same `manipal.edu` DNS namespace. [2] | No archive capture, URLScan result, CT issuance, page, or first-party document ties `.151` to an earlier service. [1] | Low |
| Parent is a backup or failover | Parent has an A record and the child has had multiple observed endpoints over time. [2] [14] [15] | No DNS failover record, certificate, scan, application content, or official architecture statement connects them. [2] | Low |
| Parent is a current alias | The name could be intended as a shorter parent-level alias. | No CNAME or HTTPS answer appeared in the queried responses, and no parent page was recovered. [8] [11] | Low |
| Parent is a squat or unauthorized lookalike | Sparse parent evidence and no demonstrated application identity could warrant review. | It is under the institution's `manipal.edu` namespace and has a DNS A record; no phishing page, content, certificate, or malicious behavior was observed. [2] [1] | Low to medium as a risk hypothesis, not a finding |
| Parent is an orphaned or misconfigured legacy DNS/web asset | DNS exists, while web, archive, scan, and certificate evidence is sparse or absent. [2] | No authoritative owner statement, zone history, or server-side record was available publicly. | Medium as a working hypothesis |

**Table takeaway:** The evidence favors an operational review category, not a definitive historical label. The parent should be placed in an `unattributed / verify ownership` queue until the university can map it to an approved service, retired service, redirect, or decommissioned record.

The strongest linkage is one-way: MUJ's official FAQ points to the Jaipur child. [17] There is no equivalent first-party source recovered here pointing to `mujslcm.manipal.edu`. The child and parent also have different observed endpoint evidence: the parent resolves to `202.131.155.151`, while current child scans resolve through `98.70.14.50`; the older child scan used `202.131.155.150`. [2] [12] [14] [15] Different addresses do not disprove a relationship, because migrations and proxies are common, but they remove the simplest direct-hosting explanation.

The parent name is not enough to call it a squat. A squat normally requires evidence that an actor registered or operates a deceptive name without authorization. Here, the name is a subdomain under `manipal.edu`, and the public evidence does not show an unauthorized registrant, deceptive content, credential collection, malicious redirect, or certificate mismatch. The prudent security conclusion is not "squat"; it is "unattributed asset with potential impersonation and stale-record risk."

Likewise, the parent is not proven to be a backup. A backup relationship requires at least one corroborator such as a DNS failover configuration, matching certificate SAN, historical page content, shared owner statement, matching application fingerprint, or documented disaster-recovery architecture. None of those was recovered for `.151`. A numerical relationship between `202.131.155.150` and `202.131.155.151` would be suggestive at most, and reverse DNS shows both addresses under a Convergent India naming pattern without proving that they belong to one application. [12] [13]

## Application Security and Governance Actions

The recommendations below are owner-side governance actions, not instructions for probing the target. CISA describes cyber asset attack surface management as helping organizations identify potential vulnerabilities and weaknesses in digital assets and reduce exposure points. [22] NIST CSF 2.0 specifically calls for inventories of software, services, and systems, inventories of external network data flows, lifecycle management, and recording validated vulnerabilities. [30] Those principles fit the parent-versus-child ambiguity directly.

**First, establish authoritative ownership.** The university should reconcile DNS zone records, registrar or DNS-provider change history, service catalogs, certificates, load-balancer configurations, CDN property names, and application CMDB records for both hostnames. This is the only reliable way to determine whether `.151` is a redirect, retired service, standby endpoint, development artifact, or current production dependency. Public evidence alone cannot answer that question.

**Second, classify the parent deliberately.** Use a temporary record such as `unattributed - DNS present - web service unconfirmed`, with owner, business purpose, data classification, authentication dependency, approved exposure, and retirement decision fields. Do not classify it as a squat solely because URLScan and Wayback are empty. Do not classify it as a backup solely because the label resembles the child.

**Third, validate the child stack through authorized internal records.** The public child fingerprint includes MVC 5.3, ASP.NET 4.0.30319, and IIS 10. [15] The university should confirm the actual .NET Framework release, Windows Server support status, patch cadence, dependency inventory, and whether headers are generated by the origin or intermediary. Microsoft's current policy lists .NET Framework 4.0 as inactive and end-of-support on January 12, 2016. [25] The header therefore deserves lifecycle review, but it is not enough to infer the exact installed runtime.

**Fourth, document identity boundaries.** Record the password-reset link as a Microsoft-linked recovery dependency, not as proof of Microsoft 365 federation. [16] [16] Confirm the actual authentication protocol, tenant, redirect URIs, logout behavior, account lifecycle, MFA policy, parent/student role separation, and incident contacts through authorized configuration review. The public report intentionally omits credentials, anti-forgery values, cookies, and contact details from the FAQ.

**Fifth, reduce unnecessary exposure without destructive action.** If the parent is retired, the owner should first identify dependencies, redirect or retire it according to change control, remove stale DNS records, revoke unused certificates, and update official documentation. If it is required, publish an owner-approved canonical URL and monitor certificate issuance, DNS changes, and external asset discovery. CISA's Secure by Design guidance emphasizes taking ownership of customer security outcomes and accountability. [21]

**Sixth, use versioned defensive testing guidance.** OWASP describes its Web Security Testing Guide as a comprehensive guide and framework of best practices for security professionals and organizations. [23] Any future testing should be authorized, scoped, rate-limited, logged, and coordinated with the university owner. A university security club should not submit login forms, guess credentials, enumerate protected paths, test injection, or attempt bypasses against these systems without explicit written authorization.

### Table 4. Safe evidence-to-action workflow

| Evidence state | Safe owner action | Success condition |
|---|---|---|
| Parent A record exists but no application evidence | Confirm DNS owner and business owner; correlate with approved service inventory. | Named owner and documented purpose, or approved retirement. |
| Parent has no archive or URLScan footprint | Treat as an evidence gap, not as proof of maliciousness or non-use. | Decision supported by internal records and change history. |
| Child exposes legacy-looking headers | Confirm exact runtime and support status internally; patch or migrate under change control. | Supported platform baseline and documented exception if needed. |
| Password reset points to Microsoft | Verify identity protocol and tenant ownership; review MFA and account lifecycle. | Auth flow documented and monitored. |
| Parent and child differ in IP/provider evidence | Check CDN, DNS, load balancer, and DR architecture records. | Relationship classified as alias, backup, migration, separate service, or unknown. |
| Service is retired | Remove stale DNS/certificates and update official links after dependency review. | No approved dependency remains and retirement is recorded. |

**Table takeaway:** The highest-value control is asset attribution, not additional public probing. A correct ownership decision will determine whether the parent should be hardened, redirected, monitored, or removed.

## Limitations and Unanswered Questions

The parent application's purpose remains unanswered. No public page, title, form, server banner, certificate, archive capture, or URLScan result was recovered for `mujslcm.manipal.edu` in the checks documented here. [1] DNS resolution alone does not reveal whether the endpoint is an application, redirector, reserved address, stale record, or controlled service.

The parent technology also remains unanswered. The child has a public MVC/IIS fingerprint, but there is no parent response from which to extract an ASP.NET header or framework signal. [15] The child fingerprint must not be copied onto the parent. In particular, the parent cannot be reported as ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, or Akamai-backed based only on the supplied scope description.

The parent relationship remains unanswered. No public evidence demonstrates that `.151` is the old child endpoint, a backup, a failover, a canonical alias, or an unauthorized squat. The official MUJ relationship is established for the Jaipur child, not the parent. [17] This distinction is important because a semantically plausible hostname can be both institutionally controlled and operationally stale, or institutionally controlled but allocated to a different service.

The current-state conclusion is also bounded. The child was observed returning HTTP 200 in June 2026, while the parent had no public scan result in the checked URLScan API. [15] [1] These are observations from public services, not a guarantee of present availability from every network, nor a substitute for internal uptime and service-monitoring data.

The archive conclusion is similarly bounded. The child has public Wayback records, while the tested parent scopes returned empty arrays. [19] Absence from an archive is not evidence that an asset never existed. It only means that no capture was returned for the requested scopes and filters.

## Synthesis

Across **purpose**, the child has first-party confirmation while the parent does not. The MUJ FAQ explicitly names the Jaipur child as the SLCM registration link. [17] The parent has only a semantically suggestive name and an A record. Across **technology**, the child has multiple passive fingerprints - MVC 5.3, ASP.NET 4.0.30319, IIS 10, Microsoft ASN, Entrust TLS, jQuery, and Font Awesome - while the parent has no recovered application fingerprint. [15] [15] [2] Across **history**, the child has successful Wayback captures and repeated public scans; the parent has no captures, zero URLScan results, and an empty Certificate Spotter result. [19]

Across **network placement**, the evidence shows divergence rather than identity. The parent resolves to `202.131.155.151`; an older child scan used `202.131.155.150`; later child scans used `98.70.14.50`. [2] [14] [15] That divergence could reflect migration, proxying, or unrelated services. It is compatible with an old-host or backup theory, but it does not prove one. The key tension is that naming similarity suggests a relationship while the observable infrastructure and public records fail to corroborate it.

Across **identity**, a Microsoft password-reset destination is visible on the child, but a password-reset link is weaker evidence than a documented federation flow. [16] [16] This creates a second tension: the portal visibly intersects with Microsoft identity services, yet the authentication architecture is not public. The correct security posture is to treat Microsoft-linked recovery as a dependency to verify, not to infer the whole identity design.

Across **risk**, the most plausible operational concern is stale or misattributed exposure, not proven maliciousness. A DNS-present but application-unobserved hostname can create ownership confusion, certificate-management gaps, and impersonation risk if official users are directed to it later. That is a governance problem that should be resolved through internal asset records and controlled change management. It should not be escalated into a squat finding without evidence of unauthorized control or deception.

## FINAL VERDICT

**Verdict: `mujslcm.manipal.edu` is a DNS-present, publicly unattributed parent-level asset. It is not publicly demonstrated to be the old MUJ SLCM, a backup, a current alias, or a squat.** The best working hypothesis is **orphaned, legacy, misconfigured, or separately provisioned institutional DNS/web infrastructure**, because the hostname resolves to `202.131.155.151` while yielding no recovered page, no URLScan records, no Wayback captures, and no Certificate Spotter issuances. [2]

**Confidence: Medium for the factual evidence; Low to medium for the classification.** Confidence is high that the Jaipur child is the publicly evidenced MUJ SLCM registration portal because the official FAQ names it and the page carries MUJ portal branding. [17] [4] Confidence is high that the child publicly exposed the reported MVC/IIS/ASP.NET indicators in the cited scans. [16] [15] Confidence is lower for the parent classification because public passive evidence cannot reveal internal DNS history, CDN configuration, disaster-recovery mapping, or authorization records.

**Operational decision:** Do not label the parent a squat or backup in a security register. Label it `unattributed - DNS A record present - application and ownership unconfirmed`, assign it to the university DNS/security owner for authoritative correlation, and resolve it through approved inventory and change-control processes. If ownership cannot be established and no dependency exists, retire the record safely; if it is required, document its purpose, canonical relationship, TLS coverage, identity dependency, monitoring, and support lifecycle.

## References

1. *urlscan.io*. https://urlscan.io/api/v1/search/?q=domain:mujslcm.manipal.edu&size=100
2. *dns.google*. https://dns.google/resolve?name=mujslcm.manipal.edu&type=A
3. *dns.google*. https://dns.google/resolve?name=mujslcm.manipal.edu&type=AAAA
4. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
5. *Manipal University*. https://muj.slcm.jaipur.manipal.edu/
6. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
7. *dns.google*. https://dns.google/resolve?name=mujslcm.manipal.edu&type=MX
8. *dns.google*. https://dns.google/resolve?name=mujslcm.manipal.edu&type=CNAME
9. *dns.google*. https://dns.google/resolve?name=mujslcm.manipal.edu&type=TXT
10. *dns.google*. https://dns.google/resolve?name=mujslcm.manipal.edu&type=NS
11. *dns.google*. https://dns.google/resolve?name=mujslcm.manipal.edu&type=HTTPS
12. *api.hackertarget.com*. https://api.hackertarget.com/reversedns/?q=202.131.155.151
13. *api.hackertarget.com*. https://api.hackertarget.com/reversedns/?q=202.131.155.150
14. *mujslcm.jaipur.manipal.edu - urlscan.io*. https://urlscan.io/result/17a4443c-7b48-46f7-9b83-c207114b958f/
15. *mujslcm.jaipur.manipal.edu - urlscan.io*. https://urlscan.io/result/019ed038-c4af-765c-9499-2da69a77e30a/
16. *mujslcm.jaipur.manipal.edu - urlscan.io*. https://urlscan.io/result/019bc028-d1ec-72f5-b0df-647554467edb/
17. *Frequently Asked Questions and Contacts for SLCM Registration*. https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf
18. *mujslcm.jaipur.manipal.edu - urlscan.io*. https://urlscan.io/domain/mujslcm.jaipur.manipal.edu
19. *web.archive.org*. https://web.archive.org/cdx/search/cdx?collapse=urlkey&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&output=json&url=mujslcm.jaipur.manipal.edu/*
20. *Manipal Academy of Higher Education - MU SLcM*. https://slcm.manipal.edu/
21. *Secure-by-Design | CISA*. https://www.cisa.gov/resources-tools/resources/secure-by-design
22. *Cyber Asset Attack Surface Management (CAASM) | CISA*. https://www.cisa.gov/resources-tools/services/cyber-asset-attack-surface-management-caasm
23. *OWASP Web Security Testing Guide | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/
24. *404 - Content not found*. https://learn.microsoft.com/en-us/aspnet/mvc/overview/getting-started/introduction/aspnet-mvc-overview
25. *.NET Framework official support policy | .NET*. https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-framework
26. *http://crt.sh/?output=json&q=mujslcm.jaipur.manipal.edu*. http://crt.sh/?output=json&q=mujslcm.jaipur.manipal.edu
27. *Student Lifecycle Management (IS-HER-CM) | SAP Help Portal*. https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/0dd6552bb884415f93aaa24c788ae644/7984cf535b804808e10000000a174cb4.html
28. *MUJStella - Student Platform for Manipal University Jaipur*. https://mujstella.in/
29. *404 Not Found*. https://crt.sh/?q=mujslcm.manipal.edu&output=json
30. *The NIST Cybersecurity Framework (CSF) 2.0*. http://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf
