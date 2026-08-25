# MUJ DNS Hygiene and Spoofing Exposure Assessment

## Executive Summary

- **Authoritative DNS Is Redundant**: `manipal.edu` publishes four Azure DNS nameservers - `ns1-36.azure-dns.com`, `ns2-36.azure-dns.net`, `ns3-36.azure-dns.org`, and `ns4-36.azure-dns.info` [4]. Independent reports say all four respond authoritatively, agree on the zone data, and occupy different network ranges [35][36]. -> This reduces ordinary single-server and single-subnet failure risk; retain all four and continuously monitor delegation consistency.

- **Jaipur Is Not Separately Delegated**: Public NS and SOA queries for `jaipur.manipal.edu` return no child-zone answer and instead identify the `manipal.edu` SOA in the authority section [15][19]. -> **Inference:** Jaipur records appear to be hosted inside the parent `manipal.edu` zone, so the security boundary, DNSSEC decision, and AXFR posture are principally those of the parent zone rather than an independent Jaipur zone.

- **DNSSEC Is Absent**: Google Public DNS returned no DS, DNSKEY, or RRSIG answer for `manipal.edu` [6][18][3]. Verisign's DNSSEC Debugger independently reported on **2026-08-25** that no DS exists in `.edu`, no DNSKEY exists at `manipal.edu`, and no RRSIGs were found [44]. -> DNS answers lack cryptographic origin and integrity validation; enable DNSSEC on the Azure-hosted zone and publish the matching DS through the `.edu` delegation process.

- **Public AXFR Exposure Was Not Observed**: HackerTarget's public zone-transfer result reports `Transfer failed` for each of the four authoritative `manipal.edu` nameservers [9]. Its Jaipur query returned only `no results found` [1]. -> The parent-zone result is reassuring, but the Jaipur result is not an independent refusal because Jaipur has no publicly visible child NS set; preserve explicit transfer restrictions and monitor them rather than treating one external result as a permanent guarantee.

- **TXT Records Reveal a Detailed Vendor Map**: The parent TXT RRset exposes Microsoft, Google, Facebook, Amazon SES, OpenAI, Brightspace, SendGrid, Salesforce, and other verification or sending relationships [22]. Jaipur exposes two Cisco CI verification values, two Microsoft verification markers, Brightspace and Outlook SPF references, and additional opaque strings [21]. -> **Inference:** These are not passwords, but they lower reconnaissance cost for tailored phishing and vendor impersonation; maintain an owner-and-expiry register and remove markers that no longer support an active service.

- **Microsoft 365 Mail Controls Are Present**: Both domains point inbound mail to Microsoft protection endpoints [2][17], and both publish two Microsoft 365 DKIM-selector CNAMEs [27][29][26][28]. -> The DNS prerequisites for SPF, DKIM, and Exchange Online routing exist, but DNS presence alone does not prove that every production message is signed or aligned; validate with DMARC aggregate telemetry.

- **DMARC Remains Monitor-Only**: `manipal.edu` publishes `v=DMARC1; p=none;`, while Jaipur publishes `v=DMARC1; p=none; rua=mailto:dmarc@jaipur.manipal.edu` [14][7]. Microsoft defines `p=none` as requesting no specific action for DMARC failures and recommends a measured progression to quarantine and reject [41]. -> Exact-domain spoofing is monitored rather than policy-blocked; use report data to move safely to enforcement.

- **Certificate Transparency Shows Long-Lived Sprawl**: The focused Jaipur crt.sh result contains **27 unique certificate names** from **2014-08-17** through **2026-08-16**, of which 25 are in the Jaipur namespace and two are external wildcard SANs [23]. The names include production, identity, helpdesk, ERP, campus, SLCM, and explicit test labels. -> Reconcile certificate names with a current asset inventory and retire abandoned DNS, certificates, and virtual hosts.

- **Overall Posture Is Mixed, Not Catastrophic**: Nameserver redundancy, failed public AXFR attempts, hard-fail SPF endings, Microsoft DKIM selectors, and DMARC reporting are positive controls [9][22][7]. DNSSEC absence, monitor-only DMARC, TXT residue, CT sprawl, and inconsistent SOA metadata leave preventable exposure. -> Prioritize DNSSEC and DMARC enforcement, then consolidate TXT and certificate governance.

## Scope, Safety, and Evidence Method

This assessment covers public DNS and certificate-transparency evidence for `manipal.edu`, `jaipur.manipal.edu`, and the MUJ SLCM hostname. The application-stack description in the request - ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 identity - is treated as supplied context, not as a conclusion independently established by this DNS review. No login, account, application endpoint, or non-public system was tested.

The evidence was collected from ordinary public resolver output, public DNS-health pages, a public AXFR checker, crt.sh, standards, CISA, and Microsoft documentation. No zone-transfer command, password attempt, vulnerability exploitation, or access-control bypass is provided. The HackerTarget output is reported as an already exposed public-tool result; it is not an instruction to repeat testing without authorization.

The requested private chain-of-thought cannot be provided. Instead, the report supplies an audit-ready evidence-to-conclusion rationale:

| Question | Observable evidence | Decision rule | Conclusion | Residual uncertainty |
|---|---|---|---|---|
| Who is authoritative? | Four Azure NS answers, corroborated by parent and local NS reports [4][35] | Parent delegation and authoritative answers should agree | Azure DNS is authoritative for `manipal.edu` | Provider-account controls are not publicly visible |
| Is Jaipur a separate zone? | No Jaipur NS or SOA answer; parent SOA returned [15][19] | A separately delegated child normally has child NS at its delegation | **Inference:** Jaipur is a namespace inside the parent zone | An unpublished split-horizon internal view cannot be ruled out |
| Is DNSSEC deployed? | No parent DS, no child DNSKEY, no RRSIG; independent debugger agrees [6][18][3][44] | A complete chain needs DS and DNSKEY links | No public DNSSEC chain exists | Future DNS changes can alter the result |
| Is AXFR publicly open? | Four parent transfers failed; Jaipur checker found no zone [9][1] | A successful public AXFR would return the zone | No public parent AXFR exposure was observed | Allowlisted transfers or later changes remain possible |
| Is spoofing strongly blocked? | SPF and DKIM DNS exist, but both DMARC policies are `p=none` [22][14][7] | DMARC enforcement requires quarantine or reject policy action | Authentication prerequisites exist; owner-requested enforcement does not | Receiver-side filtering and actual message alignment are not visible in DNS |

The table distinguishes direct observations from inferences. Public DNS is a point-in-time control-plane view: it can prove that a record was returned, but it cannot prove internal ownership, account security, mail-stream alignment, application patching, or whether every CT-listed hostname is still reachable.

## Four Azure Nameservers Provide Resilience, but Metadata Needs Cleanup

### Exact authoritative topology

| DNS item | Exact public observation | Security interpretation |
|---|---|---|
| NS 1 | `ns1-36.azure-dns.com.` | Azure-managed authoritative service [4] |
| NS 2 | `ns2-36.azure-dns.net.` | Different Azure DNS namespace [4] |
| NS 3 | `ns3-36.azure-dns.org.` | Different Azure DNS namespace [4] |
| NS 4 | `ns4-36.azure-dns.info.` | Different Azure DNS namespace [4] |
| Google-observed NS TTL | `21600` seconds | Six-hour resolver TTL at observation time [4] |
| SOA primary | `ns1-36.azure-dns.com.` | Consistent with the NS provider [8] |
| SOA responsible-name field | `awsdns-hostmaster.amazon.com.` | Incongruent with the current Azure NS provider [8] |
| SOA serial and timers | `1 7200 900 1209600 86400` | Serial `1`, 2-hour refresh, 15-minute retry, 14-day expiry, 1-day negative TTL [8] |

ViewDNS and IntoDNS independently report that all nameservers respond and agree, and that the service spans different subnets [35][36]. This is materially better than a single authoritative server or several servers in one failure domain. The use of four provider names across `.com`, `.net`, `.org`, and `.info` also avoids an in-bailiwick dependency on `manipal.edu` itself.

Both reports display a `NO GLUE` note [35][36]. **Inference:** This is low priority here because the nameserver hostnames are under Azure-controlled domains, not beneath `manipal.edu`; the resolver can obtain those addresses from the Azure DNS domains. The stronger signals are that every server has a public address, responds, and answers authoritatively [35][36].

The SOA metadata deserves review. An Azure primary with an `awsdns-hostmaster.amazon.com` responsible-name field may be deliberate, but it also resembles migration residue from an earlier Route 53 configuration. **Inference:** It does not by itself expose access or cause spoofing, yet it can misdirect operational contacts and complicate incident response. Similarly, a serial of `1` is not automatically unsafe in a managed DNS platform, but third-party tools flag it as unconventional [35]. The defensive action is to document why these values exist, not to change them blindly.

### Jaipur authority boundary

| Query | Public response | Assessment |
|---|---|---|
| `NS jaipur.manipal.edu` | No answer RRset; authority is the `manipal.edu` SOA [15] | No child delegation observed |
| `SOA jaipur.manipal.edu` | No child SOA; authority is the `manipal.edu` SOA [19] | No independent child-zone apex observed |
| `DS jaipur.manipal.edu` | No answer; parent SOA returned [10] | No Jaipur delegation signer observed |
| `DNSKEY jaipur.manipal.edu` | No answer; parent SOA returned [11] | No independent Jaipur signing apex observed |

**Inference:** DNS change control for MUJ should therefore be evaluated at the `manipal.edu` zone level. A compromised parent-zone administration path could affect Jaipur, SLCM, mail, and many other subdomains simultaneously; conversely, hardening one parent-zone account and approval workflow can protect the entire namespace.

## DNSSEC Gap Leaves the Public Namespace Unsigned

DNSSEC provides DNS origin authentication, integrity protection, public-key distribution, and authenticated denial of existence; it does not encrypt DNS data or provide confidentiality [38]. The chain normally alternates DNSKEY and DS RRsets, with each link authenticating the next [38]. Azure's documentation likewise states that the parent must contain the child's DS record for end-to-end validation [39].

### Exact DNSSEC evidence

| Layer or query | Result | Meaning |
|---|---|---|
| `.edu` -> `manipal.edu` DS | No DS answer; `.edu` SOA supplied in authority [6] | No signed delegation from the parent was observed |
| `manipal.edu` DNSKEY | No DNSKEY answer; `manipal.edu` SOA supplied [18] | No zone signing key was published |
| `manipal.edu` RRSIG | No RRSIG answer; `manipal.edu` SOA supplied [3] | No DNSSEC signatures were returned |
| Google resolver AD flag | `false` on the reviewed answers [4][6][18] | The responses were not marked authenticated data |
| Verisign independent check | No DS in `.edu`, no DNSKEY, no RRSIG [44] | Independent confirmation of unsigned status |
| Jaipur child | No child DS or DNSKEY answer [10][11] | **Inference:** Jaipur inherits the unsigned parent-zone posture |

This is a clear hygiene gap, but its consequence should be stated precisely. **Inference:** An unsigned zone gives validating resolvers no cryptographic way to distinguish authentic records from forged DNS data. That increases exposure to DNS cache poisoning or local-network response manipulation. It does not mean an attacker can edit Azure DNS, does not bypass TLS by itself, and does not reveal credentials. HTTPS clients should still reject an invalid certificate, although phishing and denial-of-service scenarios can exploit user confusion or non-TLS services.

### Case study: the SLCM address

The SLCM hostname currently returns an A record of `98.70.14.50`; the associated CNAME query did not return a CNAME answer [20][12]. This point-in-time DNS evidence does not independently support the supplied assertion that the portal is behind Akamai. **Inference:** Akamai could be present through an architecture not visible as a public CNAME, the architecture could have changed, or the supplied technology fingerprint could be stale. The safe conclusion is simply that current public DNS presents a direct A record.

Without DNSSEC, that A response is not cryptographically authenticated through DNS. TLS remains a separate protection. The practical recommendation is to enable DNSSEC for the parent Azure zone, publish the exact provider-generated DS at the `.edu` delegation, and establish rollover monitoring. Azure warns that validation requires an unbroken chain and that missing or mismatched DS/DNSKEY data breaks validation [39]. A staged change with explicit rollback ownership is important because an incorrect DS can make a signed zone unreachable to validating users.

## AXFR Is Closed Publicly; Preserve Explicit Restrictions

AXFR copies an authoritative zone and can expose hostnames and addresses at once. Microsoft's defensive guidance warns that allowing transfer to any server can send zone data to a rogue DNS server and help an attacker map domain names, computer names, and IP addresses [30]. Microsoft classifies transfers restricted to specified secondary-server IPs as the stronger configuration [30].

### Public-tool results

| Scope | Public service | Exact result | Conclusion |
|---|---|---|---|
| `manipal.edu` via `ns3-36.azure-dns.org` | HackerTarget | `Transfer failed.` [9] | No public transfer observed |
| `manipal.edu` via `ns4-36.azure-dns.info` | HackerTarget | `Transfer failed.` [9] | No public transfer observed |
| `manipal.edu` via `ns1-36.azure-dns.com` | HackerTarget | `Transfer failed.` [9] | No public transfer observed |
| `manipal.edu` via `ns2-36.azure-dns.net` | HackerTarget | `Transfer failed.` [9] | No public transfer observed |
| `jaipur.manipal.edu` | HackerTarget | `no results found` [1] | No independent Jaipur zone was found to test |

The parent result is a meaningful positive control: all four publicly delegated authoritative servers refused the public check. It directly addresses the main catastrophic AXFR scenario - anonymous extraction of the entire parent zone through a public authoritative server.

The Jaipur result requires nuance. **Inference:** `no results found` is consistent with the earlier NS/SOA evidence that Jaipur is not a separate delegated zone. It must not be rewritten as "Jaipur's authoritative servers refused AXFR," because no Jaipur-specific authoritative set was identified. The relevant transfer boundary is the parent `manipal.edu` zone.

### Case study: why failure is reassuring but not conclusive

A transfer can fail publicly while authorized transfers still occur between designated secondary servers. That is normal. One public observation also cannot prove future configuration, provider-account security, hidden DNS views, or whether export APIs are tightly controlled. Therefore, the conclusion is **no observed public AXFR exposure**, not **AXFR can never succeed**.

The defensive control should be simple: keep transfers disabled if they are unnecessary; if they are necessary, allow only documented secondary endpoints, authenticate transfers where supported, and alert on policy changes. These are controls for the university's authorized administrators, not instructions for outsiders to test the zone.

## TXT Records Expose an Integration Map, Not Credentials

DNS TXT records are public by design. The risk is therefore not that an attacker has read a secret database, but that accumulated verification and mail-routing strings reveal relationships useful for social engineering and service impersonation.

### `manipal.edu` TXT inventory

| Category | Exact or redacted public observation | Count visible | Defensive meaning |
|---|---|---:|---|
| SPF | `v=spf1 ip4:167.89.84.13/32 include:spf.protection.outlook.com include:a._spf.brightspace.com include:sendgrid.net include:_spf.salesforce.com -all` [22] | 1 | Authorizes Microsoft 365, Brightspace, SendGrid, Salesforce, and one IPv4 sender |
| Microsoft verification | Four `MS=` values and one `ms-domain-verification=` value [22] | 5 | Reveals multiple Microsoft verification events or tenants |
| Google verification | Three `google-site-verification=` values [22] | 3 | Reveals Google service-verification history |
| Amazon SES | Two `amazonses:` values [22] | 2 | Indicates SES domain-verification relationships |
| Facebook | One `facebook-domain-verification=` value [22] | 1 | Indicates Meta/Facebook domain verification |
| OpenAI | One `openai-domain-verification=` value [22] | 1 | Indicates OpenAI domain verification |
| Opaque | One long base64-like string and `M0A1N83143` [22] | 2 | Purpose is not established from DNS alone |

The table intentionally does not reproduce every full verification token. They are already public and citable, but repeating them adds little defensive value. **Inference:** A token's presence normally proves that somebody with DNS authority completed a vendor workflow at some time; it does not by itself grant present access. The governance concern is stale ownership and untracked integrations.

### `jaipur.manipal.edu` TXT inventory

| Category | Exact or redacted public observation | Count visible | Defensive meaning |
|---|---|---:|---|
| Valid SPF | `v=spf1 include:spf.protection.outlook.com include:a._spf.brightspace.com -all` [21] | 1 | Authorizes Microsoft 365 and Brightspace, then hard-fails other senders |
| Cisco CI | Two distinct `cisco-ci-domain-verification=` values [21] | 2 | Reveals Cisco-related verification history |
| Microsoft | `MS=ms43985219` and `MS=ms92065525` [21] | 2 | Reveals Microsoft verification history |
| Brightspace fragment | `include:a._spf.brightspace.com` without an SPF version prefix [21] | 1 | Residual TXT string, not a complete SPF policy |
| Additional mail fragment | Starts `ip4:103.139.159.150/32 include:sendgrid.net include:spf.protection.outlook.com` and ends with `-all` plus an apparent quote [21] | 1 | Looks like an incomplete or malformed SPF fragment |
| Opaque | One base64-like string and `M0A1N83143` [21] | 2 | Purpose is not established from DNS alone |

RFC 7208 requires an SPF record to begin exactly with `v=spf1`; records that do not are discarded during SPF selection [33]. **Inference:** The Brightspace-only and `ip4:` fragments therefore should not act as SPF policies. Because only one Jaipur string begins `v=spf1`, the displayed RRset does not appear to trigger the multiple-selected-SPF-record error described by RFC 7208 [33]. They are still configuration residue and OSINT disclosure.

The parent SPF record contains four DNS-lookup-causing `include` mechanisms. RFC 7208 limits relevant SPF DNS terms to 10 across an evaluation and requires `permerror` if the limit is exceeded [33]. **Inference:** Four top-level includes do not prove a violation, but nested includes can add lookups; the complete expansion should be monitored whenever a vendor changes its SPF chain.

Both the parent and Jaipur queries returned no CAA answer and instead returned an SOA authority response [16][5]. CAA is outside the user's main focus, but adding an intentionally managed CAA policy would reduce ambiguity over which certificate authorities are approved. This is a secondary hardening measure after DNSSEC and DMARC.

## Certificate Transparency Reveals 25 Jaipur-Namespace Names

Certificate Transparency is passive evidence of certificate issuance, not proof that a hostname currently resolves, is reachable, or remains owned by the same application team. The focused crt.sh document contains 27 unique DNS names, 25 of which are within `jaipur.manipal.edu`; it spans 2014-08-17 through 2026-08-16 [23].

### Exact Jaipur CT inventory by role

| Role | CT-observed names | What to verify internally |
|---|---|---|
| Core web and admissions | `jaipur.manipal.edu`, `www.jaipur.manipal.edu`, `admissions.jaipur.manipal.edu`, `apply.jaipur.manipal.edu`, `helpdesk.jaipur.manipal.edu` [23] | Business owner, current DNS, redirect policy, certificate owner |
| Identity | `idp.jaipur.manipal.edu` [23] | Identity-team ownership, federation metadata, retirement status |
| SLCM and campus | `mujslcm.jaipur.manipal.edu`, `muj.slcm.jaipur.manipal.edu`, `npfslcm.jaipur.manipal.edu`, `mycampus.jaipur.manipal.edu`, `testmycampus.jaipur.manipal.edu` [23] | Production/test separation and user-facing canonical hostname |
| ERP and records | `mujerp.jaipur.manipal.edu`, `testerp.jaipur.manipal.edu`, `rms.jaipur.manipal.edu`, `www.rms.jaipur.manipal.edu` [23] | Test exposure, authentication boundary, decommission date |
| Department or management portals | `lcs.jaipur.manipal.edu`, `www.lcs.jaipur.manipal.edu`, `pms.jaipur.manipal.edu` [23] | Named owner and current operational need |
| Document-management variants | `dms.jaipur.manipal.edu`, `www.dms.jaipur.manipal.edu`, `dmsmuj.jaipur.manipal.edu`, `www.dmsmuj.jaipur.manipal.edu` [23] | Duplicate-service rationalization and stale virtual hosts |
| MUJ One | `mujone.jaipur.manipal.edu`, `www.mujone.jaipur.manipal.edu` [23] | Canonical hostname and certificate scope |
| Wildcard | `*.jaipur.manipal.edu` [23] | Key custody, issuance justification, blast radius |
| External SANs in the same CT result | `*.manipaldubai.com`, `*.manipalglobal.com` [23] | **Inference:** Check whether cross-brand bundling or shared certificate administration is intended |

The parent-domain crt.sh view adds historical evidence of broader service classes, including `api.manipal.edu`, `crm.manipal.edu`, `payment.manipal.edu`, `online.manipal.edu`, `lms.manipal.edu`, and `sis.manipal.edu`, as well as wildcard certificates for `*.manipal.edu`, `*.datascience.manipal.edu`, and `*.elearning.manipal.edu` [34]. That source slice spans at least 2019-06-02 through 2022-07-26, so it is useful historical evidence but not a current exhaustive inventory [34].

### Case study: production and test labels share one namespace

`mycampus` and `testmycampus`, as well as `mujerp` and `testerp`, appear in the same public certificate history [23]. **Inference:** The labels imply lifecycle environments, but CT alone cannot establish what software runs there or whether the test systems remain live. Their value to a defender is prioritization: test-labelled assets frequently have weaker ownership, patching, data handling, or retirement discipline.

The certificate history also contains both `mujslcm.jaipur.manipal.edu` and `muj.slcm.jaipur.manipal.edu` [23]. **Inference:** Multiple near-duplicate student-portal names can create user confusion and expand phishing lookalike opportunities even when both are legitimate. MUJ should designate one canonical user-facing URL, redirect or retire alternatives safely, and train users to rely on that canonical name.

A quarterly control should reconcile CT discoveries against DNS, cloud subscriptions, application ownership, certificate issuance accounts, and decommission tickets. Findings should distinguish `current production`, `current non-production`, `redirect only`, `retired but retained`, and `unknown`. Unknown assets deserve time-bound investigation rather than automatic deletion.

## SPF and DKIM Exist, but DMARC Does Not Enforce

### Exact mail-authentication posture

| Control | `manipal.edu` | `jaipur.manipal.edu` | Assessment |
|---|---|---|---|
| MX | `0 manipal-edu.mail.protection.outlook.com.` [2] | `0 jaipur-manipal-edu.mail.protection.outlook.com.` [17] | Microsoft 365 inbound routing |
| Autodiscover | `autodiscover.outlook.com.` [13] | Not assessed in this review | Parent Microsoft client-discovery marker |
| SPF | Outlook, Brightspace, SendGrid, Salesforce, IPv4, `-all` [22] | Outlook, Brightspace, `-all` [21] | Strong terminal qualifier, but vendor inventory must stay accurate |
| DKIM selector 1 | `selector1-manipal-edu._domainkey.learnermanipal.onmicrosoft.com.` [27] | `selector1-jaipur-manipal-edu._domainkey.mujcampus.onmicrosoft.com.` [26] | Microsoft-hosted selector target |
| DKIM selector 2 | `selector2-manipal-edu._domainkey.learnermanipal.onmicrosoft.com.` [29] | `selector2-jaipur-manipal-edu._domainkey.mujcampus.onmicrosoft.com.` [28] | Microsoft-hosted rotation target |
| DMARC | `v=DMARC1; p=none;` [14] | `v=DMARC1; p=none; rua=mailto:dmarc@jaipur.manipal.edu` [7] | Monitoring, not owner-requested quarantine or rejection |

Microsoft explains that the two DKIM CNAMEs point to public keys used to verify signatures and that the alternate selector supports key rotation [37]. Their presence is positive, but it proves only DNS configuration. It does not prove that signing is enabled for every domain, that every third-party sender signs with an aligned domain, or that keys rotate successfully.

The two Microsoft tenant labels are different: `learnermanipal.onmicrosoft.com` for the parent and `mujcampus.onmicrosoft.com` for Jaipur. **Inference:** This suggests distinct Microsoft 365 tenant or domain-configuration contexts. It is not proof of administrative separation. The difference should be documented because cross-tenant mail flow and incident ownership can complicate DMARC rollout.

DMARC passes when aligned SPF or aligned DKIM succeeds and fails when both fail [41]. RFC 7489 defines `p=none` as requesting no specific delivery action, `p=quarantine` as requesting suspicious treatment, and `p=reject` as requesting rejection [40]. Therefore, a forged message that fails both aligned mechanisms is currently reported but not rejected by owner policy. A receiving provider can still block it using its own anti-abuse systems; `p=none` is not a guarantee of inbox delivery.

### Case study: Jaipur reporting is better than parent reporting

Jaipur's DMARC record includes `rua=mailto:dmarc@jaipur.manipal.edu`, while the parent record contains no reporting address [14][7]. Microsoft states that `rua` identifies the destination for aggregate reports [41]. **Inference:** Jaipur has a visible telemetry path; the parent may rely on a mechanism not visible in this record, but standard aggregate reporting is not requested there.

Microsoft recommends beginning with `p=none`, then moving to `p=quarantine`, and finally to `p=reject` after monitoring, optionally using `pct` during gradual rollout [41]. CISA states that `p=reject` provides the strongest protection against spoofed email and recommends reject for second-level domains and mail-sending hosts [42]. The appropriate action is not an immediate blind switch. First inventory every legitimate sender, confirm SPF or DKIM alignment from aggregate reports, fix failures, and then stage enforcement.

## Prioritized Defensive Roadmap

| Priority | Defensive action | Evidence driving it | Acceptance criterion | Owner class |
|---:|---|---|---|---|
| 1 | Deploy DNSSEC for `manipal.edu` and publish the correct parent DS | No DS, DNSKEY, or RRSIG [44] | Independent validators show a complete, error-free chain; rollover alerts exist | DNS platform and registrar/delegation owners |
| 2 | Move both DMARC policies from monitoring to enforcement through a staged rollout | Both are `p=none` [14][7] | All approved senders align; policy reaches `quarantine`, then `reject`; reports are reviewed [41] | Messaging and security operations |
| 3 | Add aggregate reporting for the parent domain | Parent record has no visible `rua` [14] | Reports reach a monitored, retained, and triaged mailbox or platform | Messaging security |
| 4 | Build an authoritative sender register | SPF names Outlook, Brightspace, SendGrid, Salesforce, and direct IPs [22][21] | Every sender has owner, purpose, alignment method, review date, and retirement procedure | Messaging plus service owners |
| 5 | Clean Jaipur TXT residue and stale verification records | Non-version SPF-like fragments and multiple verification markers [21] | Each TXT string has an owner and active dependency; unneeded strings are removed through change control | DNS and SaaS owners |
| 6 | Reconcile CT names with asset inventory | 25 Jaipur names plus broad parent history [23][34] | Every CT name has a disposition and canonical owner; unknowns are resolved on deadline | Attack-surface management |
| 7 | Preserve explicit AXFR restrictions | All public parent attempts failed [9] | Transfers are disabled or limited to documented secondaries; configuration drift is alerted | DNS platform owner |
| 8 | Review SOA metadata | Azure primary paired with AWS hostmaster field [8] | Responsible-name field and serial strategy are documented and operationally correct | DNS platform owner |
| 9 | Establish canonical SLCM naming | CT shows `mujslcm` and `muj.slcm` variants [23] | One user-facing canonical URL; alternatives have approved redirect or retirement states | MUJ application owner |
| 10 | Adopt a managed CAA policy | No CAA answer observed at parent or Jaipur [16][5] | Approved CA list is documented, tested, and monitored | PKI and DNS owners |

The first two actions have the largest direct anti-spoofing value. DNSSEC authenticates DNS data; DMARC enforcement tells receivers to quarantine or reject unauthenticated exact-domain mail. TXT cleanup and CT reconciliation reduce reconnaissance value and unknown attack surface, but they should not displace those foundational controls.

Changes should use university change management, named rollback owners, and monitoring. In particular, an incorrect DNSSEC DS can cause resolution failures, while premature DMARC rejection can block legitimate institutional mail. The staged recommendations from Microsoft are designed to avoid that failure mode [41].

## Synthesis

| Dimension | Current strength | Current weakness | Main trade-off | Recommended end state |
|---|---|---|---|---|
| Availability | Four responsive Azure nameservers across different subnets [35] | SOA metadata is unconventional [8] | Provider resilience versus reduced local visibility | Retain managed redundancy and document metadata/account controls |
| DNS integrity | Stable authoritative answers | No DS, DNSKEY, or RRSIG [44] | DNSSEC adds rollover and delegation complexity | Complete monitored chain of trust |
| Zone confidentiality | Public AXFR failed on all four NS [9] | One public observation cannot prove permanent policy | Secondary synchronization versus disclosure risk | Disabled transfers or explicit allowlist only |
| Mail authentication | SPF hard-fail policies and DKIM selectors exist [22][21] | DMARC is `p=none` for both scopes [14][7] | Enforcement can break unaligned legitimate senders | Telemetry-driven `p=reject` |
| Third-party integrations | DNS makes dependencies discoverable and routable | Many verification and sender markers accumulate [22][21] | SaaS agility versus inventory and impersonation surface | Owner, purpose, expiry, and alignment for every record |
| Asset visibility | CT offers a valuable external inventory [23][34] | Test, wildcard, duplicate, and historical names expand uncertainty | Operational flexibility versus larger attack surface | Continuous CT reconciliation and canonical naming |
| Jaipur autonomy | Shared parent zone centralizes control | Shared parent also concentrates blast radius [15][19] | Simpler administration versus less fault isolation | Explicit role separation and approval controls within the parent zone |

The central tension is that MUJ already has several mature managed-service controls, yet the policy layer is unfinished. Azure provides resilient authority, Microsoft 365 provides SPF/DKIM building blocks, and public AXFR is closed. At the same time, the namespace is unsigned and DMARC asks receivers only to observe failures. The architecture is therefore not devoid of security; it stops short of cryptographic DNS validation and owner-requested mail rejection.

A second tension is between integration and exposure. Brightspace, Cisco, Outlook, SendGrid, Salesforce, SES, Google, Facebook, and OpenAI markers may all correspond to legitimate university services [22][21]. **Inference:** The problem is not their public existence but the lack of visible lifecycle discipline: multiple verification artifacts and non-version SPF fragments make it difficult for an outsider - and potentially an internal responder - to distinguish active configuration from residue.

Finally, the CT history shows that SLCM is one component in a much wider identity, ERP, admissions, helpdesk, campus, records, and document-management namespace [23]. DNS hardening must therefore be governed as an enterprise control. Fixing only the SLCM A record would leave the parent trust chain, mail policy, vendor footprint, and neighboring assets unchanged.

## VERDICT

**Verdict: MODERATE DNS and spoofing risk, with HIGH confidence in the observable DNS findings.**

The strongest controls are four consistent Azure authoritative nameservers, provider-level network diversity, failed public AXFR checks on every parent nameserver, explicit SPF `-all` endings, Microsoft 365 MX routing, and two DKIM selector records for each mail scope [4][9][22][21]. These findings argue against describing the environment as broadly or trivially exposed.

The most important gaps are equally concrete: `manipal.edu` is unsigned, both DMARC policies are monitor-only, the parent DMARC record lacks a visible aggregate-report destination, Jaipur contains SPF-like TXT residue, and CT exposes a long-running, multi-service hostname estate [14][7][21][23][44]. **Inference:** These conditions make DNS manipulation harder to detect cryptographically, leave exact-domain spoofing without an owner-requested reject action, and lower the cost of reconnaissance and targeted phishing.

| Finding | Confidence | Why |
|---|---|---|
| Four Azure NS servers | High | Direct resolver answer plus two independent DNS reports [4][35][36] |
| Jaipur is not separately delegated | High | NS and SOA both return parent authority [15][19] |
| DNSSEC absent | High | Direct DS/DNSKEY/RRSIG evidence plus Verisign confirmation [6][18][3][44] |
| Public parent AXFR closed | High for observation, medium for permanence | Four failures from one public service [9] |
| TXT vendor map | High | Direct TXT answers [22][21] |
| DKIM DNS prerequisites present | High | Four direct CNAME answers |
| Actual DKIM signing and alignment | Unknown | Requires authorized mail-flow telemetry, not DNS alone |
| DMARC enforcement absent | High | Both records explicitly state `p=none` [14][7] |
| CT-listed hosts are currently live | Low/unknown | CT proves certificate issuance, not present reachability [23] |
| Supplied Akamai placement | Not confirmed by DNS | Current DNS exposes a direct A answer and no CNAME answer [20][12] |

**Recommended decision:** Treat DNSSEC deployment and staged DMARC enforcement as the two strategic projects. Run TXT cleanup, CT-to-inventory reconciliation, SOA review, CAA policy, and canonical SLCM naming as the supporting hygiene program. All validation and remediation should be performed by MUJ or Manipal personnel with explicit authorization.

## References

1. *api.hackertarget.com*. https://api.hackertarget.com/zonetransfer/?q=jaipur.manipal.edu
2. *dns.google*. https://dns.google/resolve?name=manipal.edu&type=MX
3. *dns.google*. https://dns.google/resolve?name=manipal.edu&type=RRSIG
4. *dns.google*. https://dns.google/resolve?name=manipal.edu&type=NS
5. *dns.google*. https://dns.google/resolve?name=jaipur.manipal.edu&type=CAA
6. *dns.google*. https://dns.google/resolve?name=manipal.edu&type=DS
7. *dns.google*. https://dns.google/resolve?name=_dmarc.jaipur.manipal.edu&type=TXT
8. *dns.google*. https://dns.google/resolve?name=manipal.edu&type=SOA
9. *api.hackertarget.com*. https://api.hackertarget.com/zonetransfer/?q=manipal.edu
10. *dns.google*. https://dns.google/resolve?name=jaipur.manipal.edu&type=DS
11. *dns.google*. https://dns.google/resolve?name=jaipur.manipal.edu&type=DNSKEY
12. *dns.google*. https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=A
13. *dns.google*. https://dns.google/resolve?name=autodiscover.manipal.edu&type=CNAME
14. *dns.google*. https://dns.google/resolve?name=_dmarc.manipal.edu&type=TXT
15. *dns.google*. https://dns.google/resolve?name=jaipur.manipal.edu&type=NS
16. *dns.google*. https://dns.google/resolve?name=manipal.edu&type=CAA
17. *dns.google*. https://dns.google/resolve?name=jaipur.manipal.edu&type=MX
18. *dns.google*. https://dns.google/resolve?name=manipal.edu&type=DNSKEY
19. *dns.google*. https://dns.google/resolve?name=jaipur.manipal.edu&type=SOA
20. *dns.google*. https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=CNAME
21. *dns.google*. https://dns.google/resolve?name=jaipur.manipal.edu&type=TXT
22. *dns.google*. https://dns.google/resolve?name=manipal.edu&type=TXT
23. *crt.sh*. https://crt.sh/?q=%25.jaipur.manipal.edu&output=json
24. *Manage DNS zones using DNS server in Windows Server | Microsoft Learn*. https://learn.microsoft.com/en-us/windows-server/networking/dns/manage-dns-zones
25. *Guidance for troubleshooting DNS - Windows Server | Microsoft Learn*. https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/troubleshoot-dns-guidance
26. *dns.google*. https://dns.google/resolve?name=selector1._domainkey.jaipur.manipal.edu&type=CNAME
27. *dns.google*. https://dns.google/resolve?name=selector1._domainkey.manipal.edu&type=CNAME
28. *dns.google*. https://dns.google/resolve?name=selector2._domainkey.jaipur.manipal.edu&type=CNAME
29. *dns.google*. https://dns.google/resolve?name=selector2._domainkey.manipal.edu&type=CNAME
30. *Recommendation - Configure all DNS zones only to allow zone transfers to the specified IP addresses | Microsoft Learn*. https://learn.microsoft.com/en-us/services-hub/unified/health/remediation-steps-ad/configure-all-dns-zones-only-to-allow-zone-transfers-to-specified-ip-addresses
31. *DNSSEC Tools - ICANN*. https://www.icann.org/resources/pages/tools-2012-02-25-en
32. *Troubleshoot Dns Server*. https://learn.microsoft.com/en-us/windows-server/networking/dns/troubleshoot/troubleshoot-dns-server
33. [
            
                RFC 7208 - Sender Policy Framework (SPF) for Authorizing Use of Domains in Email, Version 1
            
        ](https://datatracker.ietf.org/doc/html/rfc7208)
34. *crt.sh | %.manipal.edu*. https://crt.sh/?q=%25.manipal.edu
35. *manipal.edu DNS Report - ViewDNS.info*. https://viewdns.info/dnsreport/?domain=manipal.edu
36. *intoDNS: manipal.edu - check DNS server and mail server health*. https://intodns.com/manipal.edu
37. *How to use DKIM for email in your custom domain - Microsoft Defender for Office 365 | Microsoft Learn*. https://learn.microsoft.com/en-us/defender-office-365/email-authentication-dkim-configure
38. [
            
                RFC 4033 - DNS Security Introduction and Requirements
            
        ](https://datatracker.ietf.org/doc/html/rfc4033)
39. *Overview of DNSSEC - Azure Public DNS | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/dns/dnssec
40. [
            
                RFC 7489 - Domain-based Message Authentication, Reporting, and Conformance (DMARC)
            
        ](https://datatracker.ietf.org/doc/html/rfc7489)
41. *Set up DMARC to validate email in Microsoft 365 - Microsoft Defender for Office 365 | Microsoft Learn*. https://learn.microsoft.com/en-us/defender-office-365/email-authentication-dmarc-configure
42. *CISA Insights - Cyber: Enhance Email & Web Security*. https://www.cisa.gov/sites/default/files/publications/CISAInsights-Cyber-EnhanceEmailandWebSecurity_S508C.pdf
43. *manipal.edu | DNSViz*. https://dnsviz.net/d/manipal.edu/dnssec/
44. *DNSSEC Debugger - manipal.edu*. https://dnssec-debugger.verisignlabs.com/manipal.edu
45. *DNS records for manipal.edu.*. https://www.nslookup.io/domains/manipal.edu/dns-records/
