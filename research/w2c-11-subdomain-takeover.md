# MUJ SLCM Subdomain Takeover Risk Assessment

## Executive Summary

- **Present SLCM Posture**: The public DNS response for `mujslcm.jaipur.manipal.edu` contains a direct A record for `98.70.14.50`, while a CNAME query returns no CNAME answer [6][9]. The live page presents the MUJ portal with sign-in and parent-login choices [15]. -> Treat this host as an active application endpoint, not as a dangling-CNAME candidate. Continue normal application, identity, and infrastructure review under explicit authorization, but do not label it takeover-eligible.

- **Admissions SaaS Boundary**: `admissions.jaipur.manipal.edu` currently CNAMEs to `jaipurmanipal.nopaperforms.com` [10]. Resolution continues through an AWS load-balancer name to three A records [8], and the public page advertises Manipal University Jaipur admissions for 2026-27 [23]. -> Record this as an active third-party dependency. Its existence creates lifecycle risk, but it is not evidence of a present dangling record or takeover.

- **Eligibility Is Not a DNS-Only Fact**: OWASP defines the central condition as a DNS record pointing to a deprovisioned cloud or third-party resource, followed by the ability of another customer to claim the orphaned resource [5]. -> Use DNS to identify candidates, then require authoritative confirmation from the university and provider. Never create a cloud resource, add a custom domain, register an expired target domain, or publish proof content without written authorization.

- **Provider Controls Differ Materially**: Azure App Service supports an `asuid.{subdomain}` TXT ownership record [4]; GitHub recommends custom-domain verification and says it prevents other GitHub users from using the verified domain [2]; Heroku says domain assignment is freed when the associated app is destroyed [3]. -> A provider name in a CNAME is only the beginning of the analysis. The exact product, verification state, tenant state, and reuse policy determine risk.

- **NoPaperForms Remains a Contractual Unknown**: Public evidence shows that NoPaperForms is an education-focused SaaS provider serving more than 1,000 educational organizations, according to its own publication [19]. The reviewed public material did not document how custom hostnames are verified, reserved, quarantined, or released after tenant deletion. -> MUJ should obtain those controls in writing from the vendor; researchers should not infer claimability from silence.

- **Akamai Is Not Established by Current DNS**: Akamai documentation explains that a property hostname normally maps by CNAME to an edge hostname, which then maps through Akamai DNS to edge servers [13]. The supplied assessment context says Akamai is present, but the present SLCM DNS evidence in this review is a direct A record, not that documented CNAME pattern [6]. -> Classify Akamai as user-supplied context, not an independently verified takeover fact.

- **Indian University Case Evidence Is Weak**: This review did not substantiate a named Indian-university takeover from a primary disclosure or an official incident notice. By contrast, a 2024 Abusix report names historical higher-education examples involving UC San Diego, UCLA, Georgetown, UC Davis, the University of Alicante, and the University of La Verne [18]. -> Do not repeat unattributed social-media claims as Indian cases. Use the international examples only as lifecycle analogues.

- **Decommissioning Order Is the Main Control**: OWASP recommends updating or removing DNS, waiting at least the record TTL, and only then decommissioning the cloud resource [5]. MDN similarly says to create DNS last during provisioning and remove DNS first during deprovisioning [1]. -> Make DNS removal a mandatory change-management gate and retain provider verification TXT records for as long as a custom hostname remains delegated.

## Scope, Safety, and Evidence Standard

This report addresses one narrow question: whether public information supports a dangling-DNS or subdomain-takeover concern in the MUJ SLCM ecosystem. It does not test credentials, send requests beyond ordinary public retrieval, attempt custom-domain binding, register names, alter DNS, bypass access controls, or verify exploitability. Those actions would move from passive OSINT into active security testing and require written authorization from the domain owner and, where relevant, the SaaS provider.

A subdomain takeover is not synonymous with a CNAME. MDN describes takeover as the situation in which a subdomain points through DNS to a virtual host that is missing or removed, and another party can provide a replacement virtual host [1]. OWASP expresses the same idea as two necessary conditions: an orphaned reference and a provider that permits the orphaned resource or hostname to be claimed [5]. The analysis therefore separates what DNS proves from what only the provider can prove.

The requested explicit reasoning is presented as an auditable evidence-to-decision trace, not as private chain-of-thought. Each conclusion follows the same public rule: **record observed -> target state -> provider binding control -> authorized confirmation -> verdict**. A failure at any step stops escalation.

| Evidence label | Meaning in this report | Permitted conclusion | Prohibited overstatement |
|---|---|---|---|
| **Observed** | Directly present in a public DNS response, public page, or first-party document | The record, page, or published control existed when observed | That the service is exploitable |
| **Provider-documented** | First-party provider documentation states a binding or lifecycle rule | The rule applies to the named product, subject to its qualifiers | That MUJ uses every feature of that product |
| **Inference** | A conclusion derived from multiple observations | A prioritization hypothesis, explicitly labeled | A confirmed vulnerability |
| **Unknown** | Public evidence does not reveal a required fact | Owner or vendor validation is needed | That absence of documentation means absence of a control |
| **Not demonstrated** | Necessary takeover conditions were not shown | No public basis for a vulnerability claim | Proof that future lifecycle risk is impossible |

This evidence standard matters because provider error pages and DNS failures generate false positives. OWASP lists recognizable responses such as `No such app`, `There isn't a GitHub Pages site here.`, and Azure's `404 Web Site not found`, but it treats these as indicators to investigate rather than universal proof [5]. Unexpected content, unknown certificates, unusual infrastructure, or DMARC anomalies can indicate compromise, yet each still requires validation [5].

## MUJ's Public DNS Separates SLCM From Admissions SaaS

MUJ describes SLCM as the replacement for its older Academic Management System and says it includes attendance, internal marks, external marks, result publication, and broadcast messages [21]. That functional sensitivity raises the impact of any genuine hostname compromise, but sensitivity does not change the technical eligibility test. The SLCM application and the admissions marketing/application service must be assessed as separate hosts with different DNS models.

| Host or record | Public observation | What it establishes | Takeover interpretation |
|---|---|---|---|
| `mujslcm.jaipur.manipal.edu` CNAME | DNS status is successful but contains no CNAME answer [9] | The host is not currently represented by a public CNAME in this response | Does not match the report's dangling-CNAME pattern |
| `mujslcm.jaipur.manipal.edu` A | Direct A answer `98.70.14.50`, TTL 3600 [6] | The hostname resolves directly to an IPv4 address | **Inference:** SaaS-name reclamation through an orphaned CNAME is not indicated |
| MUJ portal page | Public page shows `WELCOME TO MUJ PORTAL`, sign-in, and parent login [15] | A recognizable application page is being served | Supports active-service classification; does not prove application security |
| `admissions.jaipur.manipal.edu` CNAME | CNAME to `jaipurmanipal.nopaperforms.com`, observed TTL 2387 [10] | MUJ delegates the admissions host to a NoPaperForms-controlled name | Third-party lifecycle dependency, not a vulnerability by itself |
| Admissions resolution chain | NoPaperForms target CNAMEs to `prodvpc-web-lb4-593721465.ap-south-1.elb.amazonaws.com`, then resolves to three A addresses [8] | The DNS chain currently terminates in addresses | Strong evidence against an NXDOMAIN-style dangling target at observation time |
| Admissions page | Public page advertises MUJ UG, PG, and PhD admissions and application information [23] | The delegated service appears operational and institution-specific | No present takeover demonstrated |
| `selector1._domainkey.jaipur.manipal.edu` | CNAME to a `mujcampus.onmicrosoft.com` DKIM selector, TTL 300 [7] | Public evidence of a Microsoft 365 mail-signing relationship | A mail-control record, not a web application CNAME |

**Inference:** The highest-value distinction is not "first party versus third party" but "active mapped resource versus orphaned reusable resource." Admissions is third party, yet its DNS chain and institution-specific content appear active. SLCM is sensitive, yet its current record type is a direct A record. Neither observation satisfies both takeover conditions.

The technology labels in the assessment input also require disciplined handling.

| Supplied technology detail | Independent status in this review | Relevance to takeover analysis |
|---|---|---|
| ASP.NET MVC 5.3 | User-supplied; not independently verified | Framework age can matter to application security, but not to CNAME claimability |
| .NET Framework 4.x | User-supplied; not independently verified | Out of scope for DNS lifecycle eligibility |
| IIS 10 | User-supplied; not independently verified | Server identity does not establish dangling SaaS state |
| Akamai | User-supplied; not demonstrated by the current SLCM DNS pattern | Relevant only if a property hostname is actually mapped to an abandoned edge configuration |
| Microsoft 365 identity | Partially supported by the public DKIM CNAME [7] | Confirms a mail relationship, not the SLCM authentication implementation or takeover eligibility |

A Microsoft 365 DKIM selector should not be mixed with web takeover findings. Its target is part of email signing, and a CNAME there serves a different protocol and control plane. The appropriate defensive question is whether the Microsoft tenant and DKIM configuration remain owned, not whether a web page can be attached to that selector.

## Azure, Heroku, GitHub Pages, NoPaperForms, and Akamai Differ

Provider suffix matching is useful for triage but dangerous as a verdict. The decisive question is whether the provider accepts an untrusted customer's binding of the exact university hostname after the original tenant resource disappears. First-party documentation shows materially different answers.

| Provider pattern | Normal DNS relationship | Documented ownership or reuse control | Safe public indicator | MUJ relevance and present status |
|---|---|---|---|---|
| **Azure App Service and related Azure services** | CNAMEs can point to names such as `azurewebsites.net`, `azurefd.net`, `azureedge.net`, or `trafficmanager.net` [4] | App Service supports `asuid.{subdomain}` TXT verification; Microsoft says this prevents another subscription from validating the custom domain without ownership proof [4] | Missing resource plus lingering CNAME is a candidate; Microsoft says the stale record should be removed [4] | SLCM has a direct A record in the present evidence, so an Azure SaaS-name takeover is not shown |
| **Heroku** | Subdomains usually CNAME to a Heroku DNS target [3] | Heroku requires account verification, but its documentation says it does not explicitly verify domain ownership and prevents simultaneous domain assignment [3] | A destroyed app with lingering DNS is dangerous because assigned custom domains are freed [3] | No Heroku CNAME was observed in the scoped MUJ records |
| **GitHub Pages** | Subdomains use a CNAME to the Pages site [2] | GitHub recommends custom-domain verification; verified domains can be published only by repositories in the verified account or organization [11] | A disabled Pages site with DNS left in place is expressly described as takeover risk [2] | No GitHub Pages CNAME was observed in the scoped MUJ records |
| **NoPaperForms** | MUJ admissions CNAMEs to `jaipurmanipal.nopaperforms.com` [10] | **Unknown:** reviewed public material did not state custom-host ownership, uniqueness, quarantine, or release rules | Current target resolves through an AWS ELB and the MUJ admissions page is live [8][23] | Active dependency; no dangling condition demonstrated |
| **Akamai property hostnames** | A property hostname maps to an Akamai edge hostname, which maps onward through Akamai DNS [13] | Property Manager creates and associates the edge hostname with an Akamai property [14] | DNS reaching Akamai proves routing, not whether an outside customer can attach the university hostname | Akamai is not established by the current direct-A SLCM evidence |

### Case study: Azure makes stale DNS dangerous but offers ownership proof

Microsoft's canonical lifecycle example is direct. A customer CNAME points to an Azure resource. The resource is deleted, but the CNAME remains. Microsoft calls that a dangling DNS entry and says the subdomain can be taken over if the name is assigned to a resource in another Azure subscription [4]. A disclosed HackerOne report illustrates the mechanism: `datacafe-cert.starbucks.com` pointed to an unclaimed Azure web service, and the reporter stated that registering the named Azure service gave control of the subdomain [20]. The report was rated High at 7.5 and publicly disclosed in August 2019 [20].

The control is not simply "use Azure." Microsoft recommends an `asuid` TXT record containing the domain verification ID [4]. It also describes Azure DNS alias records that can couple DNS lifecycle to the resource lifecycle [4]. **Inference:** MUJ should treat any future `azurewebsites.net`, `azurefd.net`, or similar record as lower risk only after the TXT verification and resource ownership are confirmed, not merely because the provider is reputable.

### Case study: GitHub and Heroku expose opposite sides of verification

GitHub explicitly warns that a disabled Pages site with DNS still configured can allow someone else to host on the subdomain [2]. Its defensive model is domain verification: only repositories under the verified account or organization may publish to the domain and immediate subdomains [11]. GitHub also strongly discourages wildcard DNS because wildcard records can preserve takeover risk even after verification [11].

Heroku documents a different lifecycle. A custom domain can be assigned to only one app at a time, but destroying the app frees the custom domains so they can be assigned elsewhere [3]. **Inference:** A live Heroku CNAME and an account-verified Heroku user are not sufficient assurances. The university must prove that the app still exists and owns the hostname, while change management must remove DNS before app destruction.

### Case study: MUJ admissions is an active NoPaperForms integration, not a confirmed flaw

The admissions CNAME is real and material: the university's official admissions page links applicants to `https://admissions.jaipur.manipal.edu/` [22], and public DNS delegates that host to NoPaperForms [10]. The target resolves to an AWS load balancer and addresses [8], while the page identifies MUJ programs and application information [23]. These observations are inconsistent with a simple "target is gone" finding.

The unresolved issue is governance. No reviewed public NoPaperForms document stated whether a tenant must prove DNS ownership, whether deleted tenant hostnames are permanently reserved, or how certificates and mappings are retired. **Inference:** That uncertainty supports a vendor-control review, not a vulnerability report. The correct request is for documentary assurance from MUJ and NoPaperForms, not an attempted external claim.

## Public DNS Can Triage Eligibility, Not Prove It

The following workflow is intentionally passive. It queries public DNS and records public provider documentation. It does not create resources, register domains, add custom hostnames, upload proof files, or interact with authentication.

| Step | Passive action | Decision question | Stop condition |
|---|---|---|---|
| 1. Confirm scope | Obtain written scope from MUJ and list only approved hostnames | Is this hostname owned by the university and in scope? | No written scope -> use only public OSINT and do not actively test |
| 2. Record DNS | Query CNAME, A, AAAA, NS, MX, and TXT through a public resolver | What exact record type and TTL exist? | Direct A/AAAA -> do not call it a dangling CNAME |
| 3. Follow the chain | Resolve each CNAME target until an address or DNS error appears | Does the chain terminate in active addresses, NXDOMAIN, NODATA, or SERVFAIL? | Active chain -> no NXDOMAIN-style dangling condition |
| 4. Identify the product | Match the target suffix to official provider documentation | Which product owns the namespace? | Unknown provider/product -> status remains Unknown |
| 5. Check ownership controls | Look for documented TXT verification, account binding, or lifecycle coupling | Can another tenant bind the exact hostname without owner proof? | Strong ownership verification -> lower risk, not zero risk |
| 6. Ask the owners | Have MUJ and the SaaS provider confirm tenant/resource ownership and deletion policy | Is the resource active and reserved to MUJ? | Confirmation of active ownership -> close takeover finding |
| 7. Report safely | Submit DNS evidence, TTL, provider rule, and uncertainty to the official channel | Is there enough evidence for a candidate misconfiguration? | Never cross the boundary into claiming or publishing content |

Safe example commands for public DNS collection are:

```text
dig +noall +answer admissions.jaipur.manipal.edu CNAME
dig +noall +answer jaipurmanipal.nopaperforms.com CNAME
dig +noall +answer jaipurmanipal.nopaperforms.com A
dig +noall +answer mujslcm.jaipur.manipal.edu CNAME
dig +noall +answer mujslcm.jaipur.manipal.edu A
```

A browser-accessible DNS-over-HTTPS equivalent is the Google Public DNS endpoint already used here, for example:

```text
https://dns.google/resolve?name=admissions.jaipur.manipal.edu&type=CNAME
https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=A
```

These queries expose only public DNS. They do not test whether a provider will accept a new tenant binding. That distinction prevents the most common analytical error: interpreting an absent A record as proof of eligibility.

| Public result | Meaning | Risk classification | Required next action |
|---|---|---|---|
| CNAME chain ends in active A/AAAA | DNS destination exists | Low evidence of dangling state | Confirm service ownership and intended use |
| CNAME target returns NXDOMAIN | Target name does not exist in DNS | Candidate orphan, not confirmed takeover | Check provider product and ownership policy; notify owner |
| NOERROR with no target address | Name exists but requested data may be absent | Ambiguous | Query relevant types and authoritative DNS; do not infer claimability |
| SERVFAIL or timeout | Resolver or authoritative failure | Operational anomaly | Repeat through another resolver and report instability |
| Provider-specific missing-resource page | Routing reached provider, but application mapping may be absent | Stronger candidate indicator | Owner/provider confirmation; no resource claim |
| Verification TXT exists | Owner proof may be enforced for the product | Risk-reducing control | Confirm TXT value is current and bound to the correct tenant |
| CNAME points to an expired registrable domain | Organization may have lost control of the target domain | High-priority candidate | Urgently alert owner; do not register it |
| Unexpected content or certificate | Could indicate misrouting or prior compromise | Incident candidate | Preserve public evidence and invoke incident response |

TLS does not settle the issue. Microsoft warns that a threat actor controlling a hijacked subdomain may obtain a valid certificate, so a valid lock icon does not protect against takeover [4]. Conversely, a certificate mismatch can result from ordinary configuration failure. Use certificates as corroboration, never as the sole verdict.

## Indian University Cases: Evidence Gap, With Global Education Analogues

No named Indian-university takeover case was verified to the standard used in this report. The searches produced generic tutorials, scanner marketing, unattributed posts, and non-Indian examples, but not a primary university notice, a provider-confirmed disclosure, or a sufficiently documented responsible-disclosure report for an Indian institution. This is a limitation of the public record reviewed, not a claim that Indian universities have never experienced dangling DNS.

That negative finding is strategically important. Repeating a university name beside an unverified allegation can cause reputational harm and can encourage unsafe testing. The correct report entry is "not publicly substantiated in reviewed sources." If the club already has a candidate case, it should require the exact hostname, historical DNS, provider, dates, owner acknowledgement, and remediation outcome before calling it a takeover.

A 2024 Abusix article supplies better-documented international higher-education analogues. It reports that attackers took over portions of popular domains through CNAMEs pointing to names under expired domains [18]. The examples below are historical reports from that article, not claims about present vulnerability.

| Institution or unit | Reported historical CNAME | Mechanism reported by source | Use in this assessment |
|---|---|---|---|
| San Diego Supercomputer Center, UC San Diego | `brak.sdsc.edu` -> `www.biologicalnetworks.org` [18] | University hostname depended on another registrable domain | Demonstrates the risk of expired external domains |
| UCLA | `user2014.stat.ucla.edu` -> `ucla.user2014.org` [18] | CNAME target outside the university's parent zone | Supports inventory of all registrable target domains |
| Georgetown University | `germs.georgetown.edu` -> `www.georgetownems.com` [18] | External-domain dependency | Shows why vendor offboarding must include DNS |
| UC Davis | `ucdim.ucdavis.edu` -> `www.ucdim.com` [18] | External target domain | Illustrates that a valid university hostname can inherit target-domain loss |
| University of Alicante | `www.master-guitar-alicante.ua.es` -> `www.master-guitar-alicante.com` [18] | External target domain | Relevant to event, campaign, and microsite retirements |
| University of La Verne | `dining.laverne.edu` -> `www.lavernedining.com` [18] | Outsourced service hostname | Comparable to dining, admissions, jobs, and events SaaS integrations |

The common mechanism differs from Azure or Heroku name reuse. In the education examples, the attacker reportedly registered an expired target domain [18]. In Azure, the attacker may reuse a deprovisioned provider resource name [4]. In GitHub or Heroku, the key issue is custom-host rebinding under provider rules [2][3]. **Inference:** MUJ needs controls for both classes: SaaS tenant lifecycle and renewal of every external registrable domain appearing in a CNAME chain.

For incident handling in India, CERT-In's 2022 directions state that covered service providers, intermediaries, data centres, bodies corporate, and government organizations must report specified Annexure I cyber incidents within six hours of noticing them or being informed [16]. Whether a particular event and MUJ entity fall within a legal category is a matter for institutional counsel and incident response. The security club should preserve timestamps and route evidence promptly, not make a legal determination.

## Remediation and Continuous Assurance

MUJ's immediate task is not to remove the active admissions record. It is to establish ownership, lifecycle accountability, and evidence that NoPaperForms cannot release the hostname to another tenant without MUJ authorization. Removing an active CNAME without service-owner approval could interrupt admissions. The correct sequence begins with an asset owner and vendor confirmation.

| Priority | Control | Owner | Completion evidence | Why it matters |
|---|---|---|---|---|
| P0 | Confirm that `jaipurmanipal.nopaperforms.com` and the custom hostname are bound to MUJ's current tenant | Admissions IT plus NoPaperForms | Vendor ticket or signed control statement naming both hostnames | Resolves the current contractual Unknown |
| P0 | Establish an incident contact and escalation path for DNS anomalies | Central IT, SOC, legal | Runbook with 24x7 contacts and CERT-In decision point | Reduces delay if content or routing changes |
| P1 | Inventory all CNAME, NS, MX, and external-domain dependencies under `jaipur.manipal.edu` | DNS administrators | Version-controlled inventory with owner, provider, purpose, expiry, and last validation | Makes orphaned records visible |
| P1 | Require provider ownership verification where available | Cloud and application owners | Azure `asuid` TXT, GitHub verification TXT, or equivalent evidence | Blocks hostname attachment without domain proof [4][11] |
| P1 | Enforce DNS-first decommissioning | Change advisory board | Change template requires DNS removal, TTL wait, then resource deletion | Prevents the classic lifecycle gap [5] |
| P1 | Eliminate unnecessary wildcard DNS | DNS administrators | Approved exceptions only, with owner and expiry | GitHub warns wildcards can sustain takeover risk [11] |
| P2 | Monitor CNAME chains, response codes, certificate transparency, and content hashes | SOC or infrastructure monitoring | Alert history and quarterly review | Detects drift after vendors or campaigns change |
| P2 | Couple DNS and cloud resources through infrastructure as code or provider aliases | Platform engineering | Automated teardown that fails if DNS remains | Reduces human offboarding errors |
| P2 | Retain historical DNS and vendor tickets | Governance and audit | Searchable evidence retained to policy | Supports incident reconstruction and responsible disclosure |

For NoPaperForms, the vendor questionnaire should ask five exact control questions: how a customer proves ownership of a custom hostname; whether two tenants can request the same hostname; what happens when a tenant or campaign is deleted; whether old mappings enter a quarantine or permanent reservation; and how certificates, logs, and support approvals are handled. The answer should name the product and tenant, not merely point to general security marketing.

For Azure, retain the `asuid` verification TXT as long as the hostname is delegated and use Azure DNS alias records where the architecture supports them [4]. For GitHub Pages, retain the verification TXT and avoid wildcard records [11]. For Heroku, remove or replace DNS before app destruction because Heroku says destroyed-app domains become available for assignment [3]. For Akamai, inventory the property hostname, edge hostname, active property version, certificate enrollment, and account owner; an edge CNAME alone does not show outsider claimability.

The security club's role should be assurance, not exploitation. It can maintain a passive inventory, compare current DNS to approved baselines, flag target NXDOMAIN changes, and prepare evidence packages. Any active provider-side validation must be performed by MUJ or the vendor in an owned tenant under a written test plan.

## Synthesis

The major patterns share one root cause but differ in mechanism, scope, control, and evidence threshold.

| Dimension | Azure | Heroku | GitHub Pages | NoPaperForms at MUJ | Akamai | Expired external domain |
|---|---|---|---|---|---|---|
| Failure mechanism | Resource deleted while CNAME remains | App destroyed while custom domain remains | Pages site disabled while DNS remains | Tenant or mapping lifecycle is not publicly documented | Property or edge mapping lifecycle could drift | Registrable CNAME target expires |
| Primary guard | `asuid` TXT and resource-aware aliases | DNS removed before app destruction | Verified custom domain and retained TXT | Vendor-specific proof and reservation policy, currently Unknown | Controlled property, edge hostname, and certificate mapping | Central renewal and ownership of target domain |
| Public evidence threshold | Missing Azure target plus exact product rule | Missing app target plus domain assignment state | Disabled/missing Pages site plus verification state | Current evidence shows an active chain, so no missing target | Akamai CNAME plus property state, which DNS alone cannot reveal | NXDOMAIN or expired target plus registration history |
| Time horizon | Resource teardown | App teardown | Site or repository disablement | Admissions campaign or contract transition | Property migration or account change | Annual domain renewal and event-site retirement |
| Current MUJ relevance | No Azure CNAME shown for SLCM | No scoped Heroku record observed | No scoped GitHub record observed | Directly relevant and active | Supplied context only; not independently established | Relevant across any broader DNS inventory |
| Trade-off | Strong controls require correct TXT lifecycle | Simple platform workflow can free names after deletion | Verification helps, wildcard DNS weakens posture | Business-critical service makes careless DNS removal harmful | CDN abstraction can obscure ownership from DNS-only review | Cheap domains are easy to forget but can affect trusted hosts |

Three non-obvious tensions emerge. First, an active third-party CNAME may be safer today than a forgotten first-party campaign domain tomorrow. Admissions is outsourced but active; a stale event microsite pointing to an expired domain could be much more dangerous. Second, successful DNS resolution is necessary for service delivery but insufficient for ownership assurance. The NoPaperForms chain reaches live addresses, yet only the vendor and MUJ can confirm durable reservation of the custom hostname.

Third, provider verification can reduce takeover risk while creating its own lifecycle obligation. Azure and GitHub TXT records are valuable only when retained, correctly associated, and included in inventory [4][11]. Removing verification before removing the service CNAME can reopen the ownership gap. **Inference:** The best control is not a scanner signature. It is a transactionally enforced lifecycle in which hostname ownership, DNS, provider resource, certificate, and vendor contract change together.

The evidence also separates impact from likelihood. SLCM carries attendance, marks, results, and parent/student access functions [21], so a hostname compromise could be high impact. But present likelihood under the dangling-CNAME scenario is not demonstrated because the host uses a direct A record and serves an MUJ portal [6][15]. Admissions has an exposed SaaS boundary, yet its live chain and branded content argue against a current dangling state [8][23]. Risk management should preserve both parts of that sentence.

## VERDICT

| Question | Verdict | Confidence | Basis |
|---|---|---|---|
| Is `mujslcm.jaipur.manipal.edu` presently a dangling CNAME? | **No evidence of that pattern.** It has no CNAME answer in the observed query and has a direct A record [9][6]. | **High** for the observed DNS state | Direct public DNS responses and a live MUJ portal [15] |
| Is `admissions.jaipur.manipal.edu` CNAMEd to NoPaperForms? | **Yes.** It points to `jaipurmanipal.nopaperforms.com` [10]. | **High** | Direct public DNS response |
| Is the admissions CNAME currently dangling? | **Not demonstrated; evidence indicates an active service.** The chain resolves through an AWS ELB to addresses and serves an MUJ admissions page [8][23]. | **High** for active resolution; **medium** for end-to-end tenant ownership | DNS and public page, but no private tenant record |
| Can an outsider claim the MUJ hostname through NoPaperForms? | **Unknown.** Public materials reviewed do not disclose the necessary hostname-binding and release controls. | **Medium** that the public answer is Unknown | Absence of a public control statement is not proof of vulnerability |
| Does the current evidence verify Akamai in front of SLCM? | **No.** Akamai appears only in supplied context; the observed SLCM record is a direct A record, while Akamai documents a property-to-edge-hostname mapping model [6][13]. | **Medium-high** | Current DNS versus provider documentation |
| Are named Indian university takeover cases established here? | **No credible named case was substantiated from the reviewed public record.** | **Medium** | Search coverage was broad, but public disclosures may be incomplete |
| Is there a reportable MUJ takeover vulnerability now? | **No.** The evidence supports a third-party lifecycle review, not a confirmed takeover finding. | **High** for "not demonstrated"; **not a guarantee of future safety** | Neither scoped host satisfies both orphaned-resource and outsider-claimability conditions |

**Final confidence: High for the present DNS observations; medium for provider-side lifecycle conclusions.** The defensible conclusion is that MUJ has an active NoPaperForms admissions integration and an active SLCM endpoint, not a publicly proven dangling-CNAME takeover. The most important residual risk is future offboarding: if MUJ or a vendor deletes the backing resource before removing DNS, the risk profile can change immediately. MUJ should verify NoPaperForms hostname ownership in writing, inventory every external dependency, retain provider ownership TXT records, and enforce DNS-first decommissioning. The university security club should remain passive unless it receives explicit written authorization for any active validation.

## References

1. *Subdomain takeover - Security | MDN*. https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/Subdomain_takeover
2. *About custom domains and GitHub Pages*. https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages
3. *Custom Domain Names for Apps | Heroku Dev Center*. https://devcenter.heroku.com/articles/custom-domains
4. *Prevent dangling DNS entries and avoid subdomain takeover | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/security/fundamentals/subdomain-takeover
5. *Subdomain Takeover Prevention - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Subdomain_Takeover_Prevention_Cheat_Sheet.html
6. *dns.google*. https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=A
7. *dns.google*. https://dns.google/resolve?name=selector1._domainkey.jaipur.manipal.edu&type=CNAME
8. *dns.google*. https://dns.google/resolve?name=admissions.jaipur.manipal.edu&type=A
9. *dns.google*. https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=CNAME
10. *dns.google*. https://dns.google/resolve?name=admissions.jaipur.manipal.edu&type=CNAME
11. *Verifying your custom domain for GitHub Pages*. https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages
12. *Set Up an Existing Custom Domain Name for Your App - Azure App Service | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/app-service/app-service-web-tutorial-custom-domain
13. *Manage hostnames*. https://techdocs.akamai.com/property-mgr/reference/modify-property-hostnames
14. *Define property hostnames*. https://techdocs.akamai.com/ion/docs/define-property-hostnames
15. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
16. *Cert-In - Home Page*. https://cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf
17. *A Guide To Subdomain Takeovers 2.0 | HackerOne*. https://www.hackerone.com/blog/guide-subdomain-takeovers-20
18. *Dangling CNAME Attacks and Sub-domain Takeovers*. https://abusix.com/blog/dangling-cname-attacks-and-sub-domain-takeovers
19. *NoPaperForms Leads the Charge on Data Security and Compliance for Educational Organizations - NoPaperForms*. https://www.nopaperforms.com/press-release/nopaperforms-leads-the-charge-on-data-security-and-compliance-for-educational-organizations
20. *HackerOne*. https://hackerone.com/reports/665398
21. *http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf*. http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf
22. *http://jaipur.manipal.edu/admissions.php*. http://jaipur.manipal.edu/admissions.php
23. *Manipal University Jaipur Admission 2026-27 | Apply Now!*. https://admissions.jaipur.manipal.edu/
