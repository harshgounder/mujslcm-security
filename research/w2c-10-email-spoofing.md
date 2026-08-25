# MUJ SLCM Email Spoofing Posture and Phishing Risk

## Executive Summary

- **Non-Enforcing DMARC Is The Central Gap**: Both `jaipur.manipal.edu` and `manipal.edu` publish `p=none`, so their DMARC policies request monitoring rather than quarantine or rejection of failing mail [16][3]. Under the current DMARC standard, `p=none` must not change existing mail handling [33] -> treat exact-domain and subdomain impersonation as a material residual risk until legitimate senders have been inventoried and enforcement is staged.

- **SPF Is Strong But Cannot Finish The Job**: Each domain has one valid SPF record ending in `-all`; Jaipur authorizes Microsoft 365 and Brightspace, while the parent domain additionally authorizes SendGrid, Salesforce, and one IPv4 address [17][20]. SPF validates the SMTP `MAIL FROM` identity, not necessarily the visible `From` domain [32][63] -> retain hard fail, but rely on aligned DKIM plus enforcing DMARC to protect the address users actually see.

- **Jaipur Contains Operationally Confusing TXT Fragments**: In addition to its valid `v=spf1` record, Jaipur publishes separate TXT strings resembling pieces of another SPF policy, including an IP address, SendGrid, Outlook, and Brightspace text [17]. SPF evaluators discard strings that do not start exactly with `v=spf1` [32] -> determine whether these are stale artifacts or intended authorization, then remove or correctly consolidate them.

- **Microsoft 365 Routing And DKIM Are Publicly Visible**: Both domains route MX to Microsoft protection hosts [15][49]. Jaipur's two common Microsoft selectors resolve through CNAMEs to nonempty RSA DKIM keys; for `manipal.edu`, selector2 returns a key while selector1's target returned no TXT key during collection -> verify signing and rotation inside the tenant and with representative outbound message headers rather than treating DNS publication alone as proof that every stream signs.

- **SLCM Inherits Monitoring, Not Enforcement**: `mujslcm.jaipur.manipal.edu` resolves to `98.70.14.50`, has no TXT answer, and has no direct `_dmarc` record [12][18][9]. RFC 9989's tree walk therefore selects the immediate parent policy at `_dmarc.jaipur.manipal.edu`, which is `p=none` [33] -> if SLCM never sends mail, give that host an explicit non-sender SPF record and an enforcing direct DMARC policy after validating operational dependencies.

- **The Parent Domain Has A Reporting Blind Spot**: Jaipur's DMARC record requests aggregate reports at `dmarc@jaipur.manipal.edu`, while `manipal.edu` publishes only `v=DMARC1; p=none;` and no `rua` destination [16][3]. RFC 9989 says receivers must not generate aggregate reports when `rua` is absent [33] -> establish an authorized reporting destination for the parent before attempting a controlled enforcement rollout.

- **Lookalikes Are A Separate Control Problem**: `manipal-edu.com` and `manipaledu.com` both resolved to web addresses during collection, although neither returned an MX answer. The former had no SPF TXT answer but did publish `p=quarantine`; the latter published `v=spf1 -all`, while its `_dmarc` query followed a parking-related CNAME rather than returning a DMARC policy -> do not mistake authentication of a lookalike for affiliation with Manipal, and monitor or defensively register high-risk variants under legal and brand-governance review.

- **Identity Defense Must Extend Beyond DNS**: CISA describes FIDO/WebAuthn as the widely available phishing-resistant MFA option and strongly urges organizations to prioritize migration [31] -> pair DMARC enforcement with phishing-resistant authentication, user-visible external-sender cues, and a rapid reporting workflow.

**Decision-ready conclusion:** The DNS posture is not absent or careless: SPF is hard-fail, Microsoft 365 mail routing is clear, and public DKIM material exists. The decisive weakness is that DMARC remains in observation mode at both relevant policy points. That configuration supplies telemetry at Jaipur but does not ask receivers to contain spoofed mail. The recommended path is not an abrupt flip to `p=reject`; it is a measured `none -> quarantine -> reject` migration after report-based discovery and sender-by-sender alignment validation, matching Microsoft's staged guidance [59].

## Scope, Method, And Reproducibility

This is a point-in-time, passive OSINT assessment conducted on **2026-08-25**. It uses only public DNS responses from Google Public DNS and public standards or defensive guidance. It does not send mail, test credentials, interact with the SLCM application, enumerate accounts, bypass controls, or instruct unauthorized access.

The application-stack descriptions in the prompt - ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 identity - are not all provable from DNS. This report validates the mail-routing evidence for Microsoft 365, but it does not claim that DNS establishes an IIS version, an MVC version, Akamai request-path behavior, or the identity provider used by a particular SLCM login flow. The SLCM A record observed here is only a DNS fact; it is not an attribution of the host's underlying cloud, proxy, or ownership.

| Scope element | Technique | What the evidence can establish | What it cannot establish |
|---|---|---|---|
| SPF and DMARC | TXT lookups at both policy domains | Published policy text, TTL, and public reporting destination | Whether every receiver enforces local filtering identically |
| DKIM | CNAME and TXT lookups for Microsoft `selector1` and `selector2` | Public selector wiring and whether a key was returned at collection time | Whether every message stream signs, whether signatures align, or which selector a given message uses |
| SLCM subdomain | A, TXT, and `_dmarc` TXT queries | Host resolution, direct TXT absence, and direct DMARC absence | Application behavior, authorization state, or actual phishing activity |
| Lookalikes | Bounded A, MX, SPF, and DMARC queries | Whether selected names resolve and what mail-policy records are visible | Registrant identity, malicious intent, trademark status, or exhaustive variant coverage |
| Risk analysis | Standards-based evidence-to-conclusion mapping | Defensive scenarios and control implications | Proof that any described scenario has occurred |

The report does not provide private hidden chain-of-thought. Instead, the following auditable rationale exposes the decision path without unsupported speculation:

| Evidence | Governing rule | Conclusion | Classification |
|---|---|---|---|
| Both relevant DMARC records say `p=none` [16][3] | `p=none` expresses no disposition preference and must not alter existing handling [33] | DMARC failure does not itself request quarantine or rejection | Direct conclusion |
| Both SPF records end in `-all` [17][20] | `-all` produces SPF Fail for an unauthorized SMTP client [32] | Unauthorized use of those domains in the SPF identity should fail SPF | Direct conclusion |
| SPF authenticates `MAIL FROM`, while DMARC checks alignment with visible `From` [33][63] | DMARC passes when at least one authenticated identifier aligns [33] | Hard-fail SPF alone cannot stop an attacker from using another envelope domain with a forged visible `From` | Standards-based inference |
| SLCM has no direct DMARC record [18] | RFC 9989 walks to the immediate parent [33] | The Jaipur `p=none` policy applies to SLCM under the current standard | Direct conclusion |
| Two selected lookalikes resolve [2][19] | Domain authentication proves control of a domain, not brand affiliation | A separately controlled similar-looking domain can remain visually persuasive even if it authenticates its own mail | Defensive inference |

DNS is volatile. These findings should therefore be re-queried before remediation or publication, especially records with short TTLs. A missing answer means only that the specified query returned no corresponding answer at collection time; it does not prove historical absence or future nonexistence.

## Apex Authentication: Hard-Fail SPF Meets Non-Enforcing DMARC

### Jaipur's valid policy authorizes Outlook and Brightspace

The valid Jaipur SPF policy observed was:

`v=spf1 include:spf.protection.outlook.com include:a._spf.brightspace.com -all` [17]

The same TXT response also contained strings such as `ip4:103.139.159.150/32 include:sendgrid.net include:spf.protection.outlook.com -all` and `include:a._spf.brightspace.com`, but those strings did not begin with `v=spf1` [17]. Under RFC 7208, receivers discard returned TXT strings that do not start with the exact SPF version section; zero remaining records yields `none`, while more than one valid record yields `permerror` [32]. Here, the published evidence shows one valid SPF record, so the extra fragments do not create a multiple-SPF-record error. They do create an administrative ambiguity.

**Inference:** If the IP address and SendGrid fragment was intended to authorize sending for `jaipur.manipal.edu`, it is ineffective as SPF in its current form. If it is obsolete, leaving it in DNS can confuse future audits and change control. The responsible remediation is to determine intent from mail-flow owners and DMARC reports, not blindly paste the fragment into the valid policy.

The included Outlook policy consists of IP ranges and `-all`, with no further DNS-causing SPF mechanisms [39]. Brightspace's first included policy contains IP addresses plus one nested `include:b._spf.brightspace.com` [51]; the nested record terminates without another DNS-causing mechanism [61]. Counting the two apex includes and the one Brightspace nested include gives **three** lookup-causing terms for the observed Jaipur path. This is below RFC 7208's limit of 10 such terms per SPF evaluation [32]. The count is point-in-time and should be recomputed whenever a provider changes its policy.

### The parent domain has broader delegated sending authority

The valid `manipal.edu` SPF policy was:

`v=spf1 ip4:167.89.84.13/32 include:spf.protection.outlook.com include:a._spf.brightspace.com include:sendgrid.net include:_spf.salesforce.com -all` [20]

This delegates SPF authorization to four third-party policy domains and one fixed IPv4 address. SendGrid's observed policy contains one nested `include:ab.sendgrid.net` [50], whose returned SPF record consists of IP ranges and `~all` without another DNS-causing term [52]. Salesforce's policy uses one `exists` mechanism [40]. Including the Brightspace nested include, the calculated observed path contains **seven** lookup-causing terms: four apex includes, one Brightspace nested include, one SendGrid nested include, and one Salesforce `exists`. That remains under the RFC limit of 10 [32].

| Domain | Valid SPF authorization | Terminal qualifier | Calculated lookup-causing terms | Assessment |
|---|---|---:|---:|---|
| `jaipur.manipal.edu` | Microsoft 365 and Brightspace [17] | `-all` | 3 [39][51][61] | Strong SPF boundary; clean up non-SPF TXT fragments |
| `manipal.edu` | Fixed IPv4, Microsoft 365, Brightspace, SendGrid, Salesforce [20] | `-all` | 7 | Within the limit, but with more third-party dependency and less headroom |

**Inference:** The wider parent-domain policy creates a larger operational trust surface. This does not mean another customer of a listed provider can automatically send as Manipal; providers maintain their own tenant and abuse controls. It does mean Manipal's SPF outcome depends on the provider-published ranges and correct provider-side authorization. Separating bulk or application mail onto dedicated subdomains would narrow the effect of a vendor-specific mistake. Microsoft likewise recommends using subdomains for email services outside direct organizational control [59].

### Why `-all` does not neutralize visible From spoofing

SPF checks the domain used in SMTP transmission, specifically the `MAIL FROM` identity [32][63]. DMARC adds the missing comparison between an authenticated SPF or DKIM domain and the domain in the user-visible `From` address [63]. A message passes DMARC if at least one authenticated identifier aligns; it fails if none align [33].

**Inference:** An impersonator can use an unrelated envelope domain that passes its own SPF while placing `jaipur.manipal.edu` or `manipal.edu` in the visible `From` field. That does not pass DMARC for Manipal, but both Manipal policy records currently say `p=none`. Receivers can still block the message using local anti-phishing systems, because final handling remains receiver discretion [33]. The DNS owner, however, is not requesting quarantine or rejection through DMARC.

This distinction makes the posture mixed rather than uniformly weak: unauthorized direct SPF use should fail because of `-all`, but visible-header impersonation has no owner-requested DMARC enforcement. The highest-value improvement is therefore enforcing alignment, not making SPF more aggressive than hard fail.

## DKIM And Microsoft 365: Visible Keys, Uneven Selector State

The MX records for both assessed domains point to Microsoft protection hosts: `jaipur-manipal-edu.mail.protection.outlook.com` for Jaipur and `manipal-edu.mail.protection.outlook.com` for the parent domain [15][49]. This is strong public evidence of Microsoft 365 mail routing. It does not, by itself, prove that the SLCM web application uses Microsoft as its login identity provider.

DKIM uses the signing domain from `d=` and selector from `s=` to form a DNS query such as `selector._domainkey.example.com` [35]. Selector names are controlled by the domain owner and need not be enumerable [35], so testing Microsoft's conventional selector pair is useful but not an exhaustive search for every possible third-party signer.

| Domain and selector | Public CNAME target | TXT key result | Safe interpretation |
|---|---|---|---|
| `selector1._domainkey.jaipur.manipal.edu` | `selector1-jaipur-manipal-edu._domainkey.mujcampus.onmicrosoft.com` | `v=DKIM1`, RSA, nonempty key [42] | DNS supports Microsoft DKIM verification for this selector |
| `selector2._domainkey.jaipur.manipal.edu` | `selector2-jaipur-manipal-edu._domainkey.mujcampus.onmicrosoft.com` | `v=DKIM1`, RSA, nonempty key [37] | DNS supports Microsoft DKIM verification for this selector |
| `selector1._domainkey.manipal.edu` | `selector1-manipal-edu._domainkey.learnermanipal.onmicrosoft.com` | CNAME present, but no target TXT key returned [48] | Could be inactive or transitional; tenant-side validation needed |
| `selector2._domainkey.manipal.edu` | `selector2-manipal-edu._domainkey.learnermanipal.onmicrosoft.com` | `v=DKIM1`, RSA, nonempty key [38] | DNS supports Microsoft DKIM verification for this selector |

Microsoft states that two key pairs exist for custom-domain DKIM, only one selector is active at a time, and the other supports future rotation; it also requires both selector CNAMEs [21]. That makes the parent-domain selector1 result a review item, not proof of a vulnerability. It may reflect a normal inactive or rotation state, but DNS alone cannot determine that.

More importantly, a public key proves only that a verifier can retrieve material for that selector. It does not prove that every Microsoft 365, Brightspace, SendGrid, Salesforce, or application message is signed, that the signature survives transit, or that its `d=` domain aligns with the visible `From`. Microsoft explicitly notes that DKIM alone is insufficient and must be combined with SPF and DMARC [21].

**Decision-ready insight:** Collect representative, authorized outbound messages from each known platform in a controlled administrative review. Check `Authentication-Results`, `DKIM-Signature d=`, selector, SPF identity, and DMARC alignment. This is a defensive mail-flow validation task, not an invitation to send test messages without authorization.

## SLCM And Subdomain Inheritance: No Direct Record, Same Monitoring Outcome

The public DNS observations for SLCM were narrow but significant:

| Query | Observed result | Meaning within scope |
|---|---|---|
| `mujslcm.jaipur.manipal.edu A` | `98.70.14.50` [9] | The hostname resolved at collection time |
| `mujslcm.jaipur.manipal.edu TXT` | NOERROR response with no Answer records [12] | No direct TXT answer was returned |
| `_dmarc.mujslcm.jaipur.manipal.edu TXT` | NXDOMAIN with no Answer [18] | No direct SLCM DMARC owner name existed in this response |
| `_dmarc.jaipur.manipal.edu TXT` | `v=DMARC1; p=none; rua=mailto:dmarc@jaipur.manipal.edu` [16] | The closest visible parent policy requests monitoring |
| `_dmarc.manipal.edu TXT` | `v=DMARC1; p=none;` [3] | The organizational-domain policy also requests monitoring |

The absence of a direct SLCM record does **not** mean DMARC policy discovery stops. RFC 9989, published in May 2026 and superseding RFC 7489 [33], performs a DNS tree walk. For an Author Domain with four labels, failure to find a valid record at the exact name leads to the immediate parent; in this case `_dmarc.jaipur.manipal.edu` is selected before `_dmarc.manipal.edu` [33]. Therefore, current-standard evaluation applies Jaipur's `p=none` policy to mail visibly From `mujslcm.jaipur.manipal.edu`.

This finding needs careful wording. SLCM is not "outside DMARC." It is under a monitoring policy. The practical weakness is the non-enforcing disposition, not the lack of inheritance. Because both Jaipur and the organizational domain publish `p=none`, either policy path yields the same high-level disposition preference even in environments transitioning between DMARC specification generations.

**Inference:** A forged visible address at SLCM, or at another child such as `notice.mujslcm.jaipur.manipal.edu`, should fail DMARC when neither aligned SPF nor aligned DKIM exists. However, the discovered owner policy does not request quarantine or rejection. Local Microsoft, Google, or gateway defenses may still identify it, but that protection is receiver-dependent rather than declared by the domain owner.

For a web host that never legitimately sends email, an explicit `v=spf1 -all` at the host and an explicit direct `p=reject` DMARC record can make intent unambiguous. That recommendation must first be checked against real application behavior: password resets, support tickets, fee notices, learning-platform notifications, and outsourced communications can all create legitimate sender dependencies. No DNS-only assessment can determine whether those flows exist.

The parent-domain record also lacks an aggregate-report destination [3]. RFC 9989 states that receivers must not generate aggregate reports for a domain when `rua` is absent [33]. Jaipur has a reporting address, but the parent does not [16][3]. That makes parent-wide source discovery harder and should be corrected before moving to enforcement.

## Lookalikes: Two Resolving Names Despite Missing MX

Lookalike risk is orthogonal to exact-domain spoofing. SPF, DKIM, and DMARC can prove that a sender controls `manipal-edu.com`; they cannot prove that the sender is affiliated with `manipal.edu`. Unicode Technical Standard 39 warns that incorrect use of Unicode identifiers can expose systems to security attacks and defines confusable-detection mechanisms [28]. Even plain ASCII edits - added hyphens, omitted punctuation, or a changed suffix - can produce visual similarity without using Unicode at all.

The following is a bounded sample, not an exhaustive brand survey:

| Candidate | A result | MX result | SPF result | DMARC result | Risk interpretation |
|---|---|---|---|---|---|
| `manipal-edu.com` | Resolved to two A addresses [2] | NOERROR, no MX answer [8] | No TXT answer [41] | `p=quarantine`, relaxed alignment, aggregate reporting to an `onsecureserver.net` mailbox [43] | Existing DNS footprint; affiliation and intent unknown |
| `manipaledu.com` | Resolved to two A addresses [19] | NOERROR, no MX answer [14] | `v=spf1 -all` [44] | Query followed a CNAME to `traff-https.hugedomains.com` and returned no DMARC TXT policy [45] | Existing, apparently parked-style DNS; affiliation and intent unknown |
| `manipal-edu.in` | NXDOMAIN for A [13] | NXDOMAIN for MX [23] | Not queried after NXDOMAIN | Not queried after NXDOMAIN | Unregistered or non-existent in the observed DNS view at that moment; status can change |
| `manipal-edu.org` | NXDOMAIN for A [27] | NXDOMAIN for MX [26] | Not queried after NXDOMAIN | Not queried after NXDOMAIN | Same point-in-time limitation |
| `manipal-edu.net` | NXDOMAIN for A/MX in the bounded check [25][30] | NXDOMAIN [30] | TXT query also returned NXDOMAIN [46] | Not queried after NXDOMAIN | Same point-in-time limitation |

No ownership or malicious-intent conclusion should be drawn from these records. A resolving website may be parked, defensive, abandoned, or operated for an unrelated lawful purpose. Conversely, absence of an MX record does not prove that a domain cannot participate in email. SMTP defines an implicit-MX rule when no MX exists and the host has a usable address record [29], and outbound sending can use infrastructure separate from inbound MX.

**Inference:** The most credible lookalike scenario is not necessarily a technically sophisticated domain. It is a visually plausible sender name whose mail authenticates for the lookalike itself or is delivered based on receiver-specific filtering. A recipient may notice "Manipal" and miss the hyphen or suffix. Exact-domain DMARC cannot reject mail for someone else's lookalike domain because that other domain is a different administrative identity.

Recommended treatment is layered: monitor high-value variants, use registrar and legal processes where justified, consider defensive registration for the narrowest high-risk set, maintain browser and mail-gateway protections, and train users to verify the registrable domain rather than the display name. Do not publish an unbounded list of currently available variants, since DNS state is volatile and such a list can create unnecessary exposure.

## Defensive Phishing Scenarios For SLCM Users

The scenarios below are threat models, not reports of observed attacks. They deliberately omit payloads, lure text, credential-capture instructions, infrastructure setup, and delivery procedures.

| Scenario | Evidence-based mechanism | Likely user pressure point | Existing control | Residual gap | Defensive response |
|---|---|---|---|---|---|
| Exact Jaipur visible-From impersonation | SPF checks `MAIL FROM`, while DMARC checks alignment with visible `From` [32][63] | A purported administrative, fee, support, or account notice | Jaipur has hard-fail SPF and visible DKIM keys [17] | DMARC is `p=none` [16] | Stage DMARC enforcement after source inventory; add high-confidence impersonation rules |
| Parent-domain executive or helpdesk impersonation | Same alignment mechanism; parent authorizes several third parties [20] | Trust in a broad institutional domain | Hard-fail SPF and one returned Microsoft selector key [20][38] | `p=none`, no `rua`, and heterogeneous senders [3] | Add aggregate reporting, validate each platform, then move to quarantine and reject |
| SLCM subdomain impersonation | No direct SLCM DMARC; RFC 9989 discovers Jaipur parent [18][33] | Familiarity with the SLCM hostname | Parent policy is discoverable | Parent policy remains monitoring only [16] | If SLCM is a non-sender, publish explicit non-sender SPF and direct rejecting DMARC after dependency review |
| Brightspace-themed impersonation | Both assessed SPF records include Brightspace [17][20] | Familiar learning-platform context | Legitimate provider IPs can pass SPF when correctly used | DNS cannot prove every Brightspace message uses aligned DKIM | Validate authorized Brightspace headers and alignment; use a dedicated sending subdomain if operationally possible |
| Microsoft account or MFA-themed impersonation | Both domains route mail through Microsoft protection hosts [15][49] | Urgency around session, mailbox, or identity access | Microsoft 365 filtering and MFA may exist, but their tenant configuration is outside DNS scope | Push or OTP MFA can still be phishable; DNS cannot show conditional-access posture | Prioritize FIDO/WebAuthn and train users to initiate sign-in from a trusted bookmark, not an email link [31] |
| ASCII lookalike-domain impersonation | Two bounded variants resolve [2][19] | Fast visual recognition of the brand string | Exact-domain DMARC protects only the exact administrative domain | A distinct domain can authenticate as itself and still look familiar | Domain monitoring, gateway similarity rules, external-sender labeling, and user verification of the registrable domain |
| Reply-path diversion | Authentication may validate the sending domain while social context pushes the recipient to respond elsewhere | Conversation continuation or request for personal information | Header analysis and anti-phishing systems may detect anomalies | DNS alone cannot show visible display-name or reply-path mismatches in a message | Teach users to inspect full addresses and independently verify sensitive requests |

### Case study 1: A Jaipur exact-domain forgery

**Observation:** Jaipur publishes a valid hard-fail SPF policy, Microsoft DKIM keys, and DMARC `p=none` with an aggregate-report mailbox. **Mechanism:** An unauthorized sender that directly uses Jaipur as the SPF identity should fail because of `-all`, but SPF does not authenticate the visible `From` by itself [32][63]. A message using an unrelated envelope identity and a forged Jaipur visible address should fail DMARC alignment, yet the published policy requests no handling change [33].

**Inference and implication:** The message is not guaranteed delivery: receiver-specific anti-phishing systems can still block it [33]. Nevertheless, the domain owner has not supplied the strongest machine-readable disposition signal. The recommended action is to use Jaipur's existing `rua` telemetry to identify legitimate failures, correct them, then progress to quarantine and reject with controlled monitoring.

### Case study 2: A plausible but separate `manipal-edu` identity

**Observation:** `manipal-edu.com` resolves and publishes its own DMARC quarantine policy, while `manipaledu.com` resolves and publishes `v=spf1 -all` [2]. Neither result establishes affiliation with Manipal. **Mechanism:** Email authentication answers "did this domain authorize or sign the message?" It does not answer "is this domain the institution the recipient had in mind?"

**Inference and implication:** A message can be technically authentic for a lookalike and still be socially deceptive. Raising DMARC on `manipal.edu` cannot solve that separate-domain problem. The action is brand-domain monitoring, mail-gateway similarity detection, phishing-resistant authentication, and a verification culture for sensitive requests.

## Prioritized Remediation Roadmap

| Priority | Action | Why now | Validation gate | Success measure |
|---:|---|---|---|---|
| P0 | Add a controlled `rua` destination to `_dmarc.manipal.edu` | The current parent record has no aggregate-report destination [3], and RFC 9989 suppresses aggregate reporting when `rua` is absent [33] | Confirm mailbox or reporting-service authorization, retention, privacy, and ownership | Reports arrive and all major legitimate sources are classified |
| P0 | Inventory every legitimate sender by domain and subdomain | Parent SPF delegates to Microsoft 365, Brightspace, SendGrid, Salesforce, and an IP [20] | Representatives from central IT, Jaipur IT, learning systems, admissions, communications, and application owners approve inventory | Every high-volume source has an owner, SPF result, DKIM `d=`, and DMARC alignment status |
| P0 | Validate phishing-resistant MFA for high-risk identities | CISA prioritizes FIDO/WebAuthn as phishing-resistant MFA [31] | Tenant administrators confirm actual methods and break-glass procedures | Administrators and other high-value users use phishing-resistant methods |
| P1 | Clean Jaipur's SPF-like TXT fragments | Non-versioned fragments are ignored by SPF but confuse administration [17][32] | Determine whether the IP and SendGrid were intended senders | One documented `v=spf1` policy remains; unrelated verification TXT records remain untouched |
| P1 | Validate DKIM selector health and rotation | Jaipur returned two keys; parent selector1 returned no target TXT key | Use authorized message headers and Microsoft tenant diagnostics | Every active stream has a valid aligned signature and a tested rotation path |
| P1 | Move Jaipur from `p=none` to quarantine, then reject | Jaipur already has reporting configured [16] | Sustained reporting shows legitimate aligned traffic and understood exceptions | Failing exact-domain and inherited-subdomain mail receives the intended disposition |
| P1 | Move `manipal.edu` through the same staged sequence | Parent remains `p=none` and is operationally broader | Reporting is installed first and third-party streams are aligned | Parent reaches enforcement without measurable legitimate-mail loss |
| P2 | Publish explicit policies for non-sending application hosts | SLCM has no direct TXT or DMARC response | Confirm the host and its applications never originate mail using that From domain | `v=spf1 -all` and direct rejecting DMARC exist only where non-sending intent is confirmed |
| P2 | Separate third-party and bulk streams onto named subdomains | Microsoft recommends subdomains for services outside direct control [59] | Providers support custom aligned return-path and DKIM domains | Vendor incidents affect a narrow subdomain rather than the institutional apex |
| P2 | Establish bounded lookalike monitoring | Selected variants already have DNS footprints [2][19] | Legal, privacy, and brand teams approve thresholds and response process | Newly registered high-similarity domains are reviewed quickly without assuming malicious intent |
| P2 | Run user-centered simulations only with written authorization | Technical controls do not eliminate social deception | University policy, ethics, privacy, and incident-response approvals are documented | Reporting speed and correct escalation improve without collecting unnecessary credentials |

Microsoft recommends a gradual DMARC progression: start with `p=none`, monitor, increase to `p=quarantine`, monitor again, and then increase to `p=reject`; it also recommends handling subdomains in order of complexity and leaving the parent domain until later [59]. That framework fits this environment because the parent SPF policy is broader than Jaipur's.

Do not jump directly to reject based solely on this report. Public DNS does not reveal all legitimate message flows, forwarding behavior, mailing-list transformations, or application-specific From domains. Enforcement without inventory could disrupt legitimate mail. Conversely, indefinite `p=none` preserves the current spoofing gap. The correct control is a time-bound migration with named owners and measurable exit criteria.

## Synthesis

| Dimension | `jaipur.manipal.edu` | `manipal.edu` | `mujslcm.jaipur.manipal.edu` | Lookalike variants |
|---|---|---|---|---|
| Authentication mechanism | Hard-fail SPF, Microsoft DKIM keys, direct DMARC | Hard-fail SPF, Microsoft DKIM wiring, direct DMARC | No direct TXT/DMARC observed; parent policy discovered | Each separate domain controls its own authentication |
| Sender scope | Outlook and Brightspace [17] | Outlook, Brightspace, SendGrid, Salesforce, fixed IP [20] | No sending authority visible at the exact host [12] | Unknown and cannot be attributed from DNS |
| DMARC outcome | `p=none`, with `rua` [16] | `p=none`, without `rua` [3] | Inherits Jaipur `p=none` under RFC 9989 [33] | Manipal's DMARC has no authority over other registrable domains |
| Primary trade-off | Better telemetry, but no enforcement | Larger source complexity and weaker visibility | Clear application identity, but no explicit non-sender declaration | Brand similarity can bypass user recognition rather than protocol checks |
| Evidence confidence | High for record text | High for record text | High for DNS answers and current-standard inheritance | Moderate because the sample is bounded and ownership is unknown |
| Recommended horizon | Enforce first after report review | Add reporting, align sources, enforce later | Add explicit policy only after non-sender confirmation | Continuous monitoring and user/gateway controls |

Three non-obvious tensions emerge.

First, the strongest-looking control, `-all`, is not the decisive one for visible-From abuse. It strongly constrains unauthorized SPF use, but SPF's identity is not necessarily the address displayed to a student. DMARC alignment is the bridge, and that bridge currently ends in monitoring rather than disposition.

Second, the lack of a direct SLCM DMARC record is not itself the flaw. Current DMARC policy discovery correctly reaches Jaipur. Publishing a direct record would improve explicit intent, especially for a confirmed non-sender, but changing Jaipur's `p` policy would already affect SLCM and other descendants. The strategic decision is therefore whether descendants have been inventoried well enough to tolerate enforcement.

Third, exact-domain controls and lookalike controls solve different identity problems. Raising DMARC to reject materially improves protection for `manipal.edu` and its covered subdomains. It does nothing to establish whether `manipal-edu.com` belongs to the institution. That second problem requires brand monitoring, user-interface cues, gateway similarity analytics, and independent verification of sensitive requests.

The holistic recommendation is a two-track program: protocol enforcement for domains Manipal controls, and identity-recognition defenses for domains it does not control. Both tracks should be paired with phishing-resistant MFA because even perfectly authenticated legitimate mailboxes can be abused after account compromise.

## VERDICT

**Overall verdict: Material spoofing exposure remains despite a credible authentication foundation.**

**Confidence: High for the point-in-time DNS findings; medium-high for the risk assessment; low for any claim about actual abuse, because no such claim is made.**

The evidence supports five firm conclusions:

1. Both assessed domains have one valid hard-fail SPF policy [17][20].
2. Both publish DMARC `p=none`, so neither asks receivers to quarantine or reject DMARC-failing mail [16][3][33].
3. Both route inbound mail through Microsoft protection hosts and expose Microsoft-style DKIM selector wiring [15].
4. SLCM has no direct DMARC record but inherits Jaipur's monitoring policy under current RFC 9989 discovery [18][33].
5. At least two bounded ASCII lookalike variants resolve, but DNS does not establish their ownership or intent [2][19].

The posture should not be described as "no protection": hard-fail SPF, DKIM material, Microsoft 365 routing, and a Jaipur reporting address are meaningful controls. It also should not be described as spoof-resistant: `p=none` explicitly stops short of an owner-requested failure disposition. The practical target state is aligned SPF and DKIM for every legitimate stream, aggregate reporting at both policy domains, staged DMARC enforcement, explicit non-sender policies where justified, bounded lookalike monitoring, and phishing-resistant MFA.

No part of this report authorizes active testing. Any mail simulation, tenant inspection, header collection involving real users, or configuration change requires written university authorization, change control, privacy review, and a rollback plan.

## References

1. *dns.google*. https://dns.google/resolve?name=selector1._domainkey.manipal.edu&type=CNAME
2. *dns.google*. https://dns.google/resolve?name=manipal-edu.com&type=A
3. *dns.google*. https://dns.google/resolve?name=_dmarc.manipal.edu&type=TXT
4. *dns.google*. https://dns.google/resolve?name=selector2._domainkey.jaipur.manipal.edu&type=CNAME
5. *dns.google*. https://dns.google/resolve?name=_dmarc.mujlearn.jaipur.manipal.edu&type=TXT
6. *dns.google*. https://dns.google/resolve?name=mujlearn.jaipur.manipal.edu&type=TXT
7. *dns.google*. https://dns.google/resolve?name=selector2._domainkey.manipal.edu&type=CNAME
8. *dns.google*. https://dns.google/resolve?name=manipal-edu.com&type=MX
9. *dns.google*. https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=A
10. *dns.google*. https://dns.google/resolve?name=autodiscover.jaipur.manipal.edu&type=CNAME
11. *dns.google*. https://dns.google/resolve?name=selector1._domainkey.jaipur.manipal.edu&type=CNAME
12. *dns.google*. https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=TXT
13. *dns.google*. https://dns.google/resolve?name=manipal-edu.in&type=A
14. *dns.google*. https://dns.google/resolve?name=manipaledu.com&type=MX
15. *dns.google*. https://dns.google/resolve?name=jaipur.manipal.edu&type=MX
16. *dns.google*. https://dns.google/resolve?name=_dmarc.jaipur.manipal.edu&type=TXT
17. *dns.google*. https://dns.google/resolve?name=jaipur.manipal.edu&type=TXT
18. *dns.google*. https://dns.google/resolve?name=_dmarc.mujslcm.jaipur.manipal.edu&type=TXT
19. *dns.google*. https://dns.google/resolve?name=manipaledu.com&type=A
20. *dns.google*. https://dns.google/resolve?name=manipal.edu&type=TXT
21. *How to use DKIM for email in your custom domain - Microsoft ...*. https://learn.microsoft.com/en-us/defender-office-365/email-authentication-dkim-configure
22. *CISA Releases Guidance on Phishing-Resistant and Numbers Matching Multifactor Authentication | CISA*. http://cisa.gov/news-events/alerts/2022/10/31/cisa-releases-guidance-phishing-resistant-and-numbers-matching-multifactor-authentication
23. *dns.google*. https://dns.google/resolve?name=manipal-edu.in&type=MX
24. *Avoiding Source Code Spoofing - The Unicode Blog*. http://blog.unicode.org/2022/03/avoiding-source-code-spoofing.html
25. *dns.google*. https://dns.google/resolve?name=manipal-edu.net&type=A
26. *dns.google*. https://dns.google/resolve?name=manipal-edu.org&type=MX
27. *dns.google*. https://dns.google/resolve?name=manipal-edu.org&type=A
28. *UTS #39: Unicode Security Mechanisms*. http://unicode.org/reports/tr39
29. *rfc-editor.org*. https://www.rfc-editor.org/rfc/rfc5321.html
30. *dns.google*. https://dns.google/resolve?name=manipal-edu.net&type=MX
31. *Implementing Phishing-Resistant MFA*. http://cisa.gov/sites/default/files/publications/fact-sheet-implementing-phishing-resistant-mfa-508c.pdf
32. *rfc-editor.org*. https://www.rfc-editor.org/rfc/rfc7208.html
33. *RFC 9989: Domain-Based Message Authentication, Reporting, and Conformance (DMARC)*. https://www.rfc-editor.org/rfc/rfc9989.html
34. *More than a Password CISA (.gov) https://www.cisa.gov › MFA*. https://www.cisa.gov/MFA
35. *rfc-editor.org*. https://www.rfc-editor.org/rfc/rfc6376.html
36. *http://rfc-editor.org/rfc/rfc5322.txt*. http://rfc-editor.org/rfc/rfc5322.txt
37. *dns.google*. https://dns.google/resolve?name=selector2._domainkey.jaipur.manipal.edu&type=TXT
38. *dns.google*. https://dns.google/resolve?name=selector2._domainkey.manipal.edu&type=TXT
39. *dns.google*. https://dns.google/resolve?name=spf.protection.outlook.com&type=TXT
40. *dns.google*. https://dns.google/resolve?name=_spf.salesforce.com&type=TXT
41. *dns.google*. https://dns.google/resolve?name=manipal-edu.com&type=TXT
42. *dns.google*. https://dns.google/resolve?name=selector1._domainkey.jaipur.manipal.edu&type=TXT
43. *dns.google*. https://dns.google/resolve?name=_dmarc.manipal-edu.com&type=TXT
44. *dns.google*. https://dns.google/resolve?name=manipaledu.com&type=TXT
45. *dns.google*. https://dns.google/resolve?name=_dmarc.manipaledu.com&type=TXT
46. *dns.google*. https://dns.google/resolve?name=manipal-edu.net&type=TXT
47. *dns.google*. https://dns.google/resolve?name=autodiscover.manipal.edu&type=CNAME
48. *dns.google*. https://dns.google/resolve?name=selector1._domainkey.manipal.edu&type=TXT
49. *dns.google*. https://dns.google/resolve?name=manipal.edu&type=MX
50. *dns.google*. https://dns.google/resolve?name=sendgrid.net&type=TXT
51. *dns.google*. https://dns.google/resolve?name=a._spf.brightspace.com&type=TXT
52. *dns.google*. https://dns.google/resolve?name=ab.sendgrid.net&type=TXT
53. *dns.google*. https://dns.google/resolve?name=manipal-edu.co.in&type=A
54. *dns.google*. https://dns.google/resolve?name=manipal-edu.co&type=MX
55. *Enhanced Email and Web Security | CISA*. https://www.cisa.gov/resources-tools/resources/enhanced-email-and-web-security
56. *dns.google*. https://dns.google/resolve?name=manipal-education.com&type=A
57. *dns.google*. https://dns.google/resolve?name=manipal-edu.co.in&type=MX
58. *dns.google*. https://dns.google/resolve?name=manipal-edu.co&type=A
59. *Set up DMARC to validate email in Microsoft 365 - Microsoft Defender for Office 365 | Microsoft Learn*. https://learn.microsoft.com/en-us/defender-office-365/email-authentication-dmarc-configure
60. *Enhance Email & Web Security | CISA*. https://www.cisa.gov/resources-tools/resources/enhance-email-web-security
61. *dns.google*. https://dns.google/resolve?name=b._spf.brightspace.com&type=TXT
62. *Set up SPF to identify valid email sources for your Microsoft 365 domain - Microsoft Defender for Office 365 | Microsoft Learn*. https://learn.microsoft.com/en-us/defender-office-365/email-authentication-spf-configure
63. *How email authentication works in Microsoft 365 - Microsoft Defender for Office 365 | Microsoft Learn*. https://learn.microsoft.com/en-us/defender-office-365/email-authentication-about
64. *rfc-editor.org*. https://www.rfc-editor.org/rfc/rfc7489.html
