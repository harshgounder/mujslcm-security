# MUJ SLCM Akamai Exposure and Origin-Leak Assessment

## Executive Summary

- **Architecture Premise Fails Current Public Tests**: `mujslcm.jaipur.manipal.edu` currently has a direct A record to **98.70.14.50** [2], while RIPE maps the covering `98.70.0.0/15` route to **Microsoft Corporation, AS8075** [38]. No CNAME to an Akamai edge hostname appears in the tested public DNS response [39]. -> Treat "IIS 10 behind Akamai" as an unverified design description, not an observed fact.

- **98.70.x.x Is Microsoft Evidence, Not Akamai Evidence**: The `98.70.x.x` observation supports Microsoft-hosted infrastructure. Akamai documentation says normal property onboarding maps the public hostname by CNAME to an Akamai edge hostname [24], with documented suffixes including `edgesuite.net`, `edgekey.net`, and `akamaized.net` [23]. -> Correct the asset inventory before making WAF or origin-masking assumptions.

- **Headers Look Like Direct IIS/ASP.NET**: The observed response exposes `Server: Microsoft-IIS/10.0`, `X-AspNetMvc-Version: 5.3`, `X-AspNet-Version: 4.0.30319`, and `X-Powered-By: ASP.NET` [40]. Akamai cache/debug fields such as `X-Cache`, `X-Cache-Remote`, and `X-Akamai-Request-ID` are documented as diagnostics returned in response to particular Akamai Pragma requests [9]. -> The ordinary response does not positively fingerprint Akamai; DNS and BGP evidence point away from it.

- **No WAF Policy Can Be Inferred Externally**: Akamai WAF attack groups are collections of Kona Rule Set rules, but each group can be set to `alert`, `deny`, a custom deny action, or `none` [15]. KRS and `ASE_MANUAL` deployments require rule upgrades, while `AAG` and `ASE_AUTO` can update automatically [10]. -> Do not equate product purchase, a "default rule," or an Akamai-looking header with effective blocking.

- **Origin Masking Requires Access Control, Not Secrecy Alone**: Akamai recommends concealing an origin behind a randomly named A record [6], but Site Shield documentation explicitly says CIDR allowlisting is not a substitute for authentication [19]. -> Use origin firewall restrictions plus authenticated edge-to-origin traffic; hostname obscurity is only a supplementary measure.

- **Current Public Endpoint Is Already Disclosed**: Public DNS directly publishes `98.70.14.50` [2]. That address may be the IIS origin or an Azure-hosted front end; public evidence does not distinguish those roles. -> If the address is the intended origin, there is no effective Akamai origin masking at present. If it is an Azure proxy, the actual backend remains undisclosed in the reviewed evidence.

- **No Separate Hidden Origin Was Verified**: Certificate Transparency records disclose the MUJ hostname and historical certificate relationships [41], but CT logs are certificate ledgers, not authoritative mappings from names to origin IPs [26]. Other ecosystem addresses exist, including `muj.slcm.jaipur.manipal.edu` at `20.244.94.89` [29], `dms.jaipur.manipal.edu` at `1.186.160.28` [34], and `slcm.manipal.edu` at `104.211.226.160` [30]. None is proven to be the backend of `mujslcm.jaipur.manipal.edu`. -> Keep these as separately owned leads, not origin findings.

- **Microsoft 365 Identity Is Only Partially Evidenced**: The public portal links to Microsoft's online password-reset service [12], whose page accepts an email or username for account recovery [18]. This supports a Microsoft-managed recovery dependency, but it does not prove that every SLCM login is federated through Microsoft Entra ID. -> Verify the identity flow from internal configuration rather than from branding or a reset link.

- **Basic Browser Hardening Is Incomplete**: The observed response includes `X-Frame-Options: SAMEORIGIN` but lacks HSTS, CSP, `X-Content-Type-Options`, `Referrer-Policy`, and `Permissions-Policy`; the resulting SecurityHeaders grade was D [42][40]. -> Fix browser-side controls independently of any CDN decision.

- **Verdict**: There is **high confidence** that the current public endpoint is Microsoft-routed and that the supplied Akamai premise is unsupported for this hostname. There is **moderate confidence** that no distinct origin is publicly exposed beyond the current A record, because passive public searches cannot prove universal absence.

## Scope, Ethics, and Evidence Model

This report uses public, passive evidence: public DNS answers, Certificate Transparency entries, indexed pages, vendor documentation, externally visible response headers, and public routing data. It does not include login attempts, vulnerability payloads, WAF probing, direct-IP Host-header comparison, port scanning, credential testing, or attempts to bypass an intermediary. Those activities require written authorization, agreed source addresses, logging coordination, and a university-approved test window.

I cannot provide private hidden chain-of-thought. Instead, the report supplies a reproducible analytical trace: observation, source, inference label, competing explanation, and decision. This is more useful for peer review because another club member can check each public fact without relying on undisclosed reasoning.

| Evidence class | Meaning in this report | Example | Permitted conclusion |
|---|---|---|---|
| Confirmed observation | Directly present in a public response or first-party document | DNS A record is `98.70.14.50` [2] | State as fact for the observation time |
| Vendor behavior | Akamai or Microsoft documentation describes a platform feature | Akamai edge onboarding normally uses a CNAME to an edge hostname [24] | Compare the target with the documented model |
| Analyst inference | Several observations support, but do not prove, a conclusion | Direct Microsoft A record plus IIS headers suggests no Akamai edge | Label explicitly as inference |
| Negative finding | A bounded review did not locate evidence | No separate origin was found in the reviewed CT, DNS, and indexed sources | Never restate as "no leak exists anywhere" |
| Unresolved alternative | Public evidence supports more than one architecture | `98.70.14.50` could be an origin or Azure front end | Require owner-side configuration review |

The time boundary matters. DNS, certificates, WAF policies, and cloud front ends can change. The DNS and HTTP observations in this assessment represent the current public state reviewed on **2026-08-25**, not a guarantee about earlier or later states.

**Decision-ready insight:** The club can confidently challenge the Akamai attribution, but it should not claim to have disproved every possible private intermediary or backend arrangement.

## 98.70.14.50 Is Microsoft AS8075, Not an Akamai Netblock

### Case study: a misleading architecture label

The strongest attribution evidence is the current DNS answer. Google Public DNS returns one A record for `mujslcm.jaipur.manipal.edu`: **98.70.14.50**, with TTL 3600 [2]. The CNAME query returns no CNAME answer and instead shows only the zone's authority information [39]. Public routing evidence aligns the covering `98.70.0.0/15` prefix with **AS8075, Microsoft Corporation** [38].

That pattern conflicts with the supplied phrase "IIS 10 behind Akamai." Akamai's own onboarding documentation describes an edge hostname that maps requests to Akamai edge servers, followed by a customer DNS CNAME to that edge hostname [24]. Akamai documents three common edge-hostname classes: Standard TLS at `edgesuite.net`, Enhanced TLS at `edgekey.net`, and Shared Cert at `akamaized.net` [23]. None appears in the current CNAME result.

**Inference:** The public request path is most consistent with a Microsoft-hosted endpoint, not an Akamai edge. This does not prove that `98.70.14.50` is the final application VM. Microsoft could place an Azure load balancer, application gateway, reverse proxy, or other managed service at that address. It does show that the client-facing address is routed by Microsoft rather than by a visible Akamai edge mapping.

| Attribution signal | Current MUJ observation | Normal Akamai comparison | Assessment |
|---|---|---|---|
| Public A record | `98.70.14.50` [2] | Edge address reached through Akamai mapping [24] | Microsoft-routed endpoint |
| Public CNAME | No CNAME answer [39] | Customer hostname commonly CNAMEs to an edge hostname [24] | Akamai mapping not observed |
| BGP owner | Microsoft AS8075 [38] | Akamai documentation describes Akamai-owned/service CIDRs [7] | `98.70.x.x` is not evidence of Akamai ownership |
| HTTP server family | IIS 10 and ASP.NET headers [40] | Not independently decisive, because proxies may pass or rewrite origin headers | Supports Microsoft stack, not Akamai attribution |
| Certificate name | MUJ hostname appears in CT history [41] | A certificate name identifies a TLS identity, not necessarily the network operator | Neutral on CDN ownership |

Akamai does not present one timeless public netblock that should be copied into every origin firewall. Its CIDR application provides current and proposed lists [1], and its firewall documentation says the blocks belong to edge servers for a particular service and carry activation status [7]. Site Shield Stable CIDRs deliberately use larger Akamai-owned ranges and still require firewall maintenance [11]. Therefore, comparing `98.70.14.50` against an arbitrary third-party "Akamai range list" would be weaker than the observed DNS and BGP route.

**Decision-ready insight:** Reclassify `98.70.14.50` as a Microsoft-routed public endpoint. Require the service owner to produce the Akamai property hostname, contract property, and active DNS mapping before documenting Akamai as part of the current path.

## Akamai Edge Fingerprints: What Headers Can and Cannot Prove

### Case study: ordinary MUJ headers versus authorized diagnostics

The ordinary MUJ response is strongly application-specific. It reports `Microsoft-IIS/10.0`, `X-AspNetMvc-Version: 5.3`, `X-AspNet-Version: 4.0.30319`, and `X-Powered-By: ASP.NET`; it also sets an ASP.NET request-verification cookie and returns `X-Frame-Options: SAMEORIGIN` [40]. These fields reveal the origin technology family, but an edge proxy could technically preserve them. They are therefore positive IIS/ASP.NET fingerprints, not absolute proof of a direct origin connection.

Akamai's better fingerprints are contextual. Its Edge Diagnostics documentation maps request-side Pragma controls to response fields. `akamai-x-cache-on` returns `X-Cache`; `akamai-x-cache-remote-on` returns `X-Cache-Remote`; `akamai-x-check-cacheable` returns `X-Check-Cacheable`; and other controls expose cache keys, serial values, and `X-Akamai-Request-ID` [9]. Because those values are diagnostic responses, their absence from a normal browser request is not independently conclusive.

| Signal | What it establishes | What it does not establish | MUJ status |
|---|---|---|---|
| `X-Cache` | Akamai documents it as edge-response information [9] | Its absence from an ordinary request does not disprove Akamai | Not present in the captured ordinary response [40] |
| `X-Cache-Remote` | Describes how an Akamai parent response was served [9] | It does not identify the protected origin by itself | Not observed [40] |
| `X-Akamai-Request-ID` | Provides an Akamai request identifier for logs [9] | A disclosed identifier is not proof that WAF blocking is enabled | Not observed [40] |
| `edgesuite.net`, `edgekey.net`, `akamaized.net` | Documented Akamai edge-hostname suffixes [23] | Private/custom DNS designs may require additional owner evidence | No CNAME to these suffixes observed [39] |
| `Server: Microsoft-IIS/10.0` | IIS is exposed in the response [40] | It cannot alone distinguish an origin from a proxy preserving the header | Observed |
| ASP.NET version headers | The response identifies MVC/ASP.NET runtime families [40] | They do not prove whether assemblies contain all available security updates | Observed |

The combined evidence is stronger than any one header. An Akamai CNAME, Akamai-routed address, and Akamai diagnostics together would be persuasive. MUJ instead presents a direct Microsoft address, no Akamai CNAME, and an IIS-focused header set. **Inference:** Akamai is unlikely to be on the currently observed client-facing path.

The version disclosures are still a security-hygiene problem. SecurityHeaders specifically identifies `X-AspNetMvc-Version` and `X-AspNet-Version` as information that should be removed [42][43]. Suppression will not patch an old component, but it reduces unnecessary reconnaissance value. Patch status must be checked from the deployed assemblies, operating-system inventory, and software-bill-of-materials records; a banner is not enough.

**Decision-ready insight:** Use DNS plus routing plus authorized edge diagnostics for attribution. Do not declare Akamai present or absent from `Server` alone, and do not turn a version banner into an unsupported vulnerability claim.

## Akamai WAF Baselines: Managed Rules Still Require Policy Decisions

Akamai describes its Web Application Firewall behavior as a suite that blocks threatening HTTP and HTTPS requests and says only one instance is implemented per property, typically in the default rule [33]. "Default rule" here means placement in a Property Manager rule tree; it does not mean every customer receives an identical, immutable enforcement policy.

Akamai attack groups are collections of Kona Rule Set rules [15]. The action is configuration-dependent: `alert` records the event, `deny` blocks it, a custom deny can take a customer-defined action, and `none` takes no action [15]. Evaluation mode runs alongside existing rules and records what new rules would have done; its default evaluation action is `alert` [32]. Thus, seeing a policy or even an evaluation event does not prove that the request would be blocked.

| WAF layer | Documented behavior | Operational failure mode | Defensive requirement |
|---|---|---|---|
| Property WAF behavior | Blocks threatening HTTP/HTTPS requests when configured [33] | Behavior absent from the active property or wrong hostname scope | Verify active property and hostname coverage |
| KRS attack groups | Group related managed rules [15] | Group action set to `alert` or `none` rather than `deny` [15] | Review effective actions per policy |
| KRS update mode | `KRS` is manual; `AAG` is automatic [36] | Rules age while administrators assume automatic maintenance | Record mode and update owner |
| Adaptive Security Engine | `ASE_AUTO` updates automatically; `ASE_MANUAL` does not [36] | Manual recommendations remain unapplied | Set change-control SLA or use approved auto mode |
| Evaluation mode | Measures how candidate rules would respond to live traffic [32] | Evaluation is mistaken for enforcement | Complete evaluation and activate intended actions |
| Custom rules | Add application-specific controls beyond managed detections [8] | Generic signatures miss business-logic abuse | Model sensitive SLCM workflows separately |
| Edge DDoS and rate controls | Product includes network and Layer 7 DDoS defenses and granular rate controls [8] | Controls are licensed but not applied to login or transcript endpoints | Validate per-host and per-path policy scope |

Akamai's product brief says App & API Protector combines WAF, bot mitigation, API protection, and DDoS protection [8]. It names SQL injection, cross-site scripting, local file inclusion, server-side request forgery, and related attack classes among its application defenses [8]. These are product capabilities, not findings about MUJ.

For the MUJ case, there is no public evidence of an active Akamai property, much less the policy ID, ruleset version, mode, exceptions, action state, rate policy, or bot controls. Attempting to infer those details through hostile payloads would exceed this report's passive scope. The safe answer to "which default Akamai rules protect MUJ?" is **not publicly verifiable**.

**Decision-ready insight:** Ask the owner for an exported effective policy showing hostname scope, KRS/ASE mode, ruleset version, attack-group actions, exceptions, and last activation. Until then, record Akamai WAF protection as unverified.

## Origin Masking That Survives Public-IP Discovery

### Case study: secrecy fails unless the origin rejects bypass traffic

Akamai recommends creating a new origin hostname and using a random string in the origin A record to conceal it [6]. That reduces casual discovery, but it is not a security boundary. Certificate issuance, historical DNS, other subdomains, configuration mistakes, and provider inventories can eventually disclose an address.

Akamai Site Shield addresses the enforcement problem by routing edge-to-origin traffic through defined CDN CIDR ranges; customers allowlist those ranges at the perimeter firewall [19]. Origin IP ACL similarly ensures that origin requests come from a small, stable list of Akamai-controlled address prefixes [14]. However, Akamai explicitly warns that Site Shield and stable CIDRs are not substitutes for authentication [11][19]. Shared ranges may serve multiple platform products, so source-IP permission alone is weaker than a credential unique to the intended delivery path.

| Control | Security mechanism | Residual risk | Recommended use |
|---|---|---|---|
| Random origin hostname | Reduces obvious DNS discovery [6] | Historical DNS and CT can preserve clues | Supplementary concealment only |
| Site Shield | Restricts origin access to defined Akamai ranges [19] | CIDRs change and may be shared | Firewall allowlist with maintenance owner |
| Stable CIDRs | Uses larger, mostly stable Akamai-owned ranges [11] | Larger shared ranges expand trust | Pair with origin authentication [11] |
| Origin IP ACL | Uses a small stable list of Akamai-controlled prefixes [14] | Source address is not application identity | Prefer when supported, plus authentication |
| Origin TLS verification | Authenticates the origin certificate and fails an invalid connection [6] | Protects edge-to-origin server identity, not necessarily who may call the origin | Always use strict HTTPS verification |
| Edge-to-origin authentication | Authenticates permitted intermediary traffic [11] | Key or certificate lifecycle must be managed | Use mTLS or a securely validated signed secret |
| Public-IP rotation | Invalidates previously recorded origin addresses | Fails if new address is again published directly | Perform after DNS and firewall controls are ready |

Cross-vendor guidance reaches the same architectural conclusion. Cloudflare advises auditing DNS-only records for origin information, rotating origins because historical DNS records persist, and blocking traffic not originating from trusted proxy ranges [28]. Its authenticated-origin documentation also notes that a network-wide certificate proves only that a request came from that provider's network; a customer-specific certificate is stronger [27]. This is not evidence that MUJ uses Cloudflare. It is corroboration of the general principle that network membership and tenant authentication solve different problems.

For MUJ, publishing `98.70.14.50` as the service A record means that address is not masked [2]. **Inference:** If this is the backend IIS endpoint, an attacker who knows it would not need an origin-discovery technique. If it is an Azure reverse proxy with a private backend, the actual origin may still be protected, but that cannot be established externally.

**Decision-ready insight:** Protect the backend so disclosure of its address is harmless. The origin should accept application traffic only through approved edge paths and authenticated health/administration channels.

## Passive Origin Discovery: DNS, CT/SANs, and Error Clues

Public origin research is best framed as a defender's exposure audit, not as a bypass recipe. Certificate Transparency is explicitly public and append-only, allowing observers to see certificates issued by CAs [26]. DNS records are public by design, and vendor guidance warns that historical records can retain pre-CDN IP addresses [28]. Error responses and headers can then provide correlation clues, but clues must not be promoted to proof without owner-side validation.

| Public-data method | Defensive question | Evidence value | False-positive risk | MUJ result |
|---|---|---|---|---|
| Current A/AAAA/CNAME | Does the public name map to a CDN edge or directly to a provider address? | High for current routing | Split-horizon and geolocation can produce different answers | A record is `98.70.14.50`; no CNAME observed [2][39] |
| Historical/passive DNS | Did the hostname previously point somewhere else? | High when timestamped by a reputable dataset | Shared hosting and reassigned cloud IPs | No distinct historical MUJ origin was verified in the reviewed public results |
| CT and SAN review | Which hostnames have appeared in public certificates? | High for name discovery | A certificate name need not resolve to the same application | MUJ and historical related names appear in CT [41] |
| Related-subdomain DNS | Do sibling names expose separate infrastructure? | Medium | Siblings may be unrelated services | Several separate addresses exist; linkage to MUJ origin is unproven [30][29][34] |
| Response headers | Does a candidate expose the same unusual stack or application metadata? | Medium as corroboration | Default IIS headers are common | MUJ exposes IIS/ASP.NET fields [40] |
| Error-page comparison | Do distinctive templates, request IDs, or backend hostnames appear? | Low to medium | Generic CDN and framework error pages are widely reused | No public error-page origin hostname was verified |
| Indexed static assets | Do indexed URLs contain internal hostnames or absolute backend URLs? | Medium | Old code and third-party mirrors can be stale | Public scripts are indexed, but no separate backend was established [12] |
| Public routing/RDAP | Who originates the candidate IP prefix? | High for network attribution | Network owner is not necessarily application owner | `98.70.0.0/15` aligns to Microsoft AS8075 [38] |

The certificate record deserves careful handling. The reviewed CT output contains multiple certificates for `mujslcm.jaipur.manipal.edu`, including a current Entrust certificate, older records containing `www.mujslcm.jaipur.manipal.edu`, and an older record associated with `dms.jaipur.manipal.edu` [41]. Current DNS puts `dms.jaipur.manipal.edu` at `1.186.160.28` [34]. **Inference:** This is a useful historical relationship, but it does not prove that `1.186.160.28` is or was the MUJ SLCM origin. Certificates can be reissued, names can migrate, and the current DNS state can differ from the certificate period.

Similarly, `muj.slcm.jaipur.manipal.edu` resolves to `20.244.94.89` [29], while the central `slcm.manipal.edu` resolves to `104.211.226.160` [30] and exposes its own IIS/ASP.NET response [44]. These are separate assets until ownership records or application configuration prove backend equivalence. Treating every sibling as an "origin" would be entity conflation.

**Decision-ready insight:** Maintain a timestamped exposure ledger. Promote an address from "lead" to "origin" only with owner-side architecture evidence or an explicitly authorized correlation test.

## MUJ SLCM Public-Origin Leak Assessment

### Finding 1: the public service IP is disclosed

The current hostname directly publishes **98.70.14.50** [2]. That is a confirmed disclosure of the public service endpoint. It is not, by itself, proof of a hidden-origin leak because the architecture may intentionally expose an Azure front end. The word "origin" must be reserved for the server or service from which a CDN retrieves content.

### Finding 2: no Akamai-facing address is visible

No CNAME answer points to a documented Akamai edge-hostname suffix [39][23]. The routed network is Microsoft AS8075 [38], and the observed response is IIS/ASP.NET-focused [40]. **Inference:** The simplest architecture consistent with the evidence is a Microsoft-hosted web endpoint serving the portal without a visible Akamai edge in front.

### Finding 3: the exact Azure role is unresolved

The evidence cannot distinguish a directly exposed IIS VM from an Azure service forwarding to another backend. The HTTP response passes application-server headers, but proxies can preserve such headers. Consequently, the defensible formulation is: **the client-facing Microsoft endpoint is public; the final backend topology is unknown**.

### Finding 4: CT reveals names, not a distinct backend

The certificate history exposes the MUJ hostname and historical related names [41]. CT is designed as a public ledger of issued certificates [26]. No reviewed CT record directly supplies a second origin IP. The current `dms` and `muj.slcm` addresses are leads, not verified backends [29][34].

### Finding 5: the application leaks stack and control information

The response discloses IIS, ASP.NET MVC, ASP.NET runtime, and `X-Powered-By` values [40]. The public page includes a request-verification token, username and password fields, and a Microsoft password-reset link [12]. The anti-forgery token is a positive design signal, but its presence does not establish the security of all state-changing routes.

The observed request-verification cookie was `HttpOnly` but did not show `Secure` or `SameSite` attributes in the captured header [40]. Because it is an anti-forgery cookie rather than demonstrated session authentication, the impact should not be overstated. The correct owner action is to inventory every cookie and apply attributes according to its purpose.

### Finding 6: browser security headers are incomplete

SecurityHeaders assigned a D grade and reported missing HSTS, CSP, `X-Content-Type-Options`, `Referrer-Policy`, and `Permissions-Policy [42]. The response did include `X-Frame-Options: SAMEORIGIN` [40]. Missing HSTS is especially relevant because the hostname accepts an HTTP URL that redirects to HTTPS; without HSTS, the browser has no long-lived instruction from this site to require HTTPS on future visits.

### Finding 7: Microsoft identity is not fully demonstrated

The site links to `passwordreset.microsoftonline.com` [12], and that Microsoft page provides account recovery using an email or username [18]. This confirms a Microsoft recovery touchpoint. It does not show an OAuth/OIDC authorization endpoint, SAML metadata, tenant ID, token validation flow, MFA policy, or Conditional Access configuration. Calling the entire portal "Microsoft 365 identity" would therefore overstate the public evidence.

| Question | Answer | Confidence | Reason |
|---|---|---|---|
| Is `98.70.14.50` public? | Yes | High | Direct DNS answer [2] |
| Is `98.70.14.50` Akamai space? | Evidence says no | High | Microsoft AS8075 routing [38] |
| Is a visible Akamai edge in front? | Not supported | High | No Akamai CNAME, Microsoft-routed A record [2][39] |
| Is `98.70.14.50` the final IIS origin? | Unknown | Moderate uncertainty | Could be a Microsoft front end; public data cannot distinguish it |
| Is another hidden origin publicly verified? | No verified distinct origin found | Moderate | Bounded CT, DNS, and indexed-source review |
| Are sibling addresses origins? | Unproven | High | They resolve separately but lack backend linkage [30][29][34] |
| Is Akamai WAF protecting MUJ? | Not publicly verifiable | High | No property or policy evidence; WAF actions are configurable [15] |
| Is Microsoft account recovery used? | Yes | High | Portal link and Microsoft reset page [12][18] |
| Is all authentication federated to Microsoft 365? | Unknown | High | Public evidence is insufficient |

**Decision-ready insight:** The report should not say "we found the hidden Akamai origin." It should say "the hostname currently exposes a Microsoft-routed service address, while the claimed Akamai layer is not visible and no separate backend address has been verified."

## Remediation and Authorized Validation Roadmap

| Priority | Action | Owner evidence required | Completion criterion |
|---|---|---|---|
| P0 | Correct the architecture inventory | DNS zone, Azure resource mapping, Akamai property hostname, active property version | One approved diagram identifies client edge, WAF, proxy, and backend roles |
| P0 | Determine what `98.70.14.50` actually is | Azure subscription/resource ID and traffic flow | Address classified as VM, load balancer, application gateway, or other service |
| P1 | If Akamai is intended, activate a documented edge mapping | Akamai property and edge hostname | Public DNS follows the approved Akamai edge-hostname design [24] |
| P1 | Restrict origin ingress | Site Shield or Origin IP ACL data, firewall policy, health-check sources | Backend rejects unapproved network paths [19][14] |
| P1 | Authenticate edge-to-origin traffic | Certificate or signed-request design and rotation owner | Origin validates a tenant-specific edge credential [11] |
| P1 | Enable strict origin TLS verification | Certificate trust and hostname-validation settings | Invalid origin certificates cause connection failure [6] |
| P1 | Remove version disclosure | IIS and ASP.NET response configuration | IIS/MVC/runtime banners absent from ordinary responses [42][43] |
| P1 | Add browser security policy | Application-tested header baseline | HSTS, CSP, `nosniff`, referrer, and permissions controls present [42] |
| P1 | Review every cookie | Cookie inventory by authentication function | Session cookies use Secure, HttpOnly, and appropriate SameSite values |
| P2 | Prove effective WAF enforcement | Active security config and policy export | Sensitive hosts and paths have reviewed actions, exceptions, and versions [15] |
| P2 | Use evaluation before rule promotion | Evaluation report and false-positive disposition | Candidate rules measured, approved, then activated [32] |
| P2 | Establish managed-rule maintenance | KRS/ASE mode and named owner | Manual modes have an SLA; automatic modes are monitored [36] |
| P2 | Verify identity architecture internally | Entra enterprise app, protocol metadata, MFA and Conditional Access policy | Recovery, authentication, and authorization flows separately documented |
| P3 | Monitor CT and DNS continuously | Approved domain inventory and alert routing | New certificates and DNS changes generate owner-reviewed alerts [26] |
| P3 | Rotate a backend IP after controls are ready | Firewall and DNS change plan | Historical address no longer reaches the backend [28] |

Any active validation should be performed by an authorized university team. A suitable engagement would define the exact hostnames, source addresses, permitted request classes, test accounts, payload exclusions, data-handling rules, emergency contacts, and stop conditions. The security club should not independently test candidate IPs, bypass paths, login behavior, or WAF signatures.

For an Akamai deployment, the most useful evidence is administrative rather than adversarial: active property hostnames, edge hostname, production activation timestamp, Site Shield or Origin IP ACL map, origin authentication behavior, AppSec configuration ID, policy ID, KRS/ASE mode, effective attack-group actions, exception list, and SIEM delivery status. Those records answer the open questions without touching student data.

**Decision-ready insight:** Fix attribution first. Otherwise the university may spend effort tuning an Akamai policy that is not on the observed request path while leaving a Microsoft-hosted endpoint directly exposed.

## Synthesis

The central tension is between **visibility** and **enforcement**. DNS, BGP, CT, and headers reveal what the public can observe. They do not reveal every private hop or effective WAF action. Conversely, a well-designed origin remains secure even when its address becomes known because the firewall and authentication layer reject unapproved traffic.

| Dimension | Current observed MUJ posture | Documented Akamai delivery posture | Resilient target posture |
|---|---|---|---|
| Client routing | Direct Microsoft-routed A record [2][38] | Customer CNAME maps to Akamai edge hostname [24] | Approved edge mapping, monitored continuously |
| Attribution | IIS/ASP.NET plus Microsoft BGP | Akamai DNS suffix, routing, and controlled diagnostics [9][23] | Multiple independent signals and owner configuration agree |
| WAF | Not publicly established | Managed rules and attack groups with configurable actions [15] | Explicit deny posture after evaluation, with documented exceptions |
| Rule maintenance | Unknown | Manual or automatic modes [36] | Named owner, version SLA, evaluation and rollback process |
| Origin secrecy | Public endpoint disclosed [2] | Randomized origin name reduces casual discovery [6] | Discovery assumed; access still denied without trusted edge identity |
| Network restriction | Unknown | Site Shield or Origin IP ACL allowlisting [19][14] | Stable least-privilege ingress with lifecycle monitoring |
| Origin authentication | Unknown | Akamai says allowlisting is not a substitute for authentication [11] | Tenant-specific mTLS or equivalent authenticated request path |
| Identity | Microsoft recovery link observed [12][18] | Independent of CDN/WAF | Federation, MFA, recovery, and app authorization separately verified |
| Browser hardening | Multiple missing headers [42] | Edge can add headers, but application compatibility still matters | Tested CSP, HSTS, MIME, referrer, and feature controls |
| Evidence limitation | Passive review cannot identify every backend | Administrative data can show actual property and policy | Public monitoring plus owner-side validation |

The non-obvious finding is that an Akamai deployment would not automatically resolve the most concrete issues observed. A CDN could obscure or rewrite some headers, but it would not establish secure cookie semantics, correct authorization, an effective CSP, or safe business logic. Likewise, a managed WAF can detect broad attack classes, but an attack group left in `alert` or `none` does not enforce a block [15].

The opposite divergence also matters: the absence of an Akamai CNAME does not mean the application has no front-end protection at all. Microsoft could provide an Azure-layer proxy or WAF at `98.70.14.50`. That alternative remains unverified because the public evidence identifies the network owner and application headers, not the Azure resource type. The correct next step is owner-side Azure inventory, not speculative public probing.

Finally, CT and related-subdomain evidence demonstrate why "security by unknown hostname" is fragile. Public certificate logs deliberately reveal issued names [26], and historical DNS can preserve old mappings [28]. The stronger architecture is one in which an exposed IP cannot be used to bypass the intended control plane.

**Decision-ready insight:** Separate four questions in every future assessment: Who routes the public endpoint? Which edge or WAF actually processes the hostname? What system serves as the origin? What mechanism prevents direct origin access? MUJ's public evidence answers the first, leaves the second and third partly unresolved, and supplies no proof for the fourth.

## VERDICT

**Verdict on Akamai:** **Not supported by current public evidence. High confidence.** The hostname resolves directly to `98.70.14.50` [2], the covering route is associated with Microsoft AS8075 [38], and no Akamai edge-hostname CNAME is returned [39]. Akamai's documented onboarding model normally uses an edge hostname and CNAME [24].

**Verdict on the 98.70.x.x claim:** **It is Microsoft/Azure evidence, not Akamai-range evidence. High confidence.** It should not be entered into an "Akamai IP allowlist" without an Akamai-provided, property-specific CIDR source. Akamai's own tooling distinguishes current, proposed, active, future, and deleted service CIDRs [1][7].

**Verdict on origin leakage:** **The public service address is disclosed; a separate hidden origin is not verified. Moderate confidence.** If `98.70.14.50` is the backend, the origin is plainly exposed. If it is an Azure front end, the actual backend may remain private. The public data reviewed cannot decide between those architectures.

**Verdict on sibling IPs:** **Do not classify them as origins. High confidence.** `20.244.94.89`, `1.186.160.28`, and `104.211.226.160` are associated with related hostnames [29][34][30], but no reviewed evidence links them as the backend of the target hostname.

**Verdict on WAF protection:** **Unknown. High confidence in the uncertainty.** Akamai policy actions and upgrade modes are customer-configurable [10][15]. No active MUJ AppSec configuration was publicly established.

**Overall confidence:** **High** for DNS, routing, exposed headers, and the conclusion that the stated Akamai premise is unsupported. **Moderate** for the bounded negative finding that no separate origin leak was found. **Low** for any claim about private Azure topology, effective WAF rules, or full Microsoft 365 federation, because those require owner-side records.

## References

1. *Access the CIDR Lists application*. https://techdocs.akamai.com/client-access-control/docs/access-cidr-lists-app
2. *dns.google*. https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=A
3. *Upgrade KRS ruleset*. https://techdocs.akamai.com/application-security/reference/put-policy-rules
4. *Create a custom rule*. https://techdocs.akamai.com/application-security/reference/post-config-custom-rules
5. *dns.google*. https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=AAAA
6. *Origin Server*. https://techdocs.akamai.com/property-mgr/docs/origin-server
7. *About CIDR blocks*. https://techdocs.akamai.com/firewall-rules/docs/about-cidr-blocks
8. *App & API Protector*. http://akamai.com/site/en/documents/brief/akamai-app-and-api-protector-product-brief.pdf
9. *Pragma headers*. https://techdocs.akamai.com/edge-diagnostics/docs/pragma-headers
10. *Rule upgrade*. https://techdocs.akamai.com/terraform/docs/as-rc-rule-upgrade
11. *Site Shield Stable CIDRs overview*. https://techdocs.akamai.com/site-shield/docs/site-shield-stable-cidrs-overview
12. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
13. *Origin IP Access Control List*. https://techdocs.akamai.com/property-mgr/docs/origin-ip-access-control
14. *Welcome to Origin IP ACL*. https://techdocs.akamai.com/origin-ip-acl/docs/welcome
15. *Attack groups*. https://techdocs.akamai.com/terraform/docs/as-ds-attack-groups
16. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
17. *Site Shield*. https://techdocs.akamai.com/property-mgr/docs/siteshield-beh
18. [
	Microsoft Online Password Reset
](https://passwordreset.microsoftonline.com/)
19. *Welcome to Site Shield*. https://techdocs.akamai.com/site-shield/docs/welcome-site-shield
20. *WAF policy rule action*. https://techdocs.akamai.com/powershell/docs/set-appsecpolicyrule
21. *Policy attack group action*. https://techdocs.akamai.com/powershell/docs/set-appsecpolicyattackgroup
22. *Set protections*. https://techdocs.akamai.com/cloud-security/docs/set-protections
23. *Edge hostname*. http://techdocs.akamai.com/terraform/docs/pm-rc-edge-hostname
24. *Define property hostnames*. http://techdocs.akamai.com/ion/docs/define-property-hostnames
25. [
    Logs : Certificate Transparency
  ](https://certificate.transparency.dev/logs)
26. *Certificate Transparency in Chrome | CertificateTransparency*. https://googlechrome.github.io/CertificateTransparency
27. *Authenticated Origin Pulls (mTLS) · Cloudflare SSL/TLS docs*. http://developers.cloudflare.com/ssl/origin-configuration/authenticated-origin-pull
28. *Protect your origin server*. https://developers.cloudflare.com/fundamentals/security/protect-your-origin-server
29. *dns.google*. https://dns.google/resolve?name=muj.slcm.jaipur.manipal.edu&type=A
30. *dns.google*. https://dns.google/resolve?name=slcm.manipal.edu&type=A
31. *dns.google*. https://dns.google/resolve?name=muj.slcm.jaipur.manipal.edu&type=CNAME
32. *Policy evaluation mode*. https://techdocs.akamai.com/powershell/docs/set-appsecpolicyevaluationmode
33. *Web Application Firewall*. https://techdocs.akamai.com/property-mgr/docs/web-app-firewall
34. *dns.google*. https://dns.google/resolve?name=dms.jaipur.manipal.edu&type=A
35. *dns.google*. https://dns.google/resolve?name=dms.jaipur.manipal.edu&type=CNAME
36. *WAF mode*. https://techdocs.akamai.com/terraform/docs/as-ds-waf-mode
37. *dns.google*. https://dns.google/resolve?name=slcm.manipal.edu&type=CNAME
38. *http://stat.ripe.net/data/prefix-overview/data.json?resource=98.70.14.50*. http://stat.ripe.net/data/prefix-overview/data.json?resource=98.70.14.50
39. *dns.google*. https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=CNAME
40. *http://api.hackertarget.com/httpheaders?q=https://mujslcm.jaipur.manipal.edu/*. http://api.hackertarget.com/httpheaders?q=https://mujslcm.jaipur.manipal.edu/
41. *http://crt.sh/?output=json&q=mujslcm.jaipur.manipal.edu*. http://crt.sh/?output=json&q=mujslcm.jaipur.manipal.edu
42. *http://securityheaders.com/?followRedirects=on&q=https://mujslcm.jaipur.manipal.edu/*. http://securityheaders.com/?followRedirects=on&q=https://mujslcm.jaipur.manipal.edu/
43. *http://securityheaders.com/?followRedirects=on&q=https://slcm.manipal.edu/*. http://securityheaders.com/?followRedirects=on&q=https://slcm.manipal.edu/
44. *http://api.hackertarget.com/httpheaders?q=https://slcm.manipal.edu/*. http://api.hackertarget.com/httpheaders?q=https://slcm.manipal.edu/
