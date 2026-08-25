# Manipal SLCM Security History: Evidence, Gaps, and Risk

## Executive Summary

- **No Confirmed SLCM Breach**: The public record reviewed through **August 25, 2026** does not establish a confirmed compromise of `slcm.manipal.edu` or `mujslcm.jaipur.manipal.edu`. The most concrete security-related publication is a single February 2026 threat-intelligence article about the separate Manipal Library Portal; it neither implicates SLCM nor reports student credentials in the alleged data [4]. -> Treat claims that "SLCM was breached" as unsubstantiated unless MAHE, MUJ, CERT-In, law enforcement, or independently verifiable technical evidence confirms them.

- **One Material but Unconfirmed Leak Claim**: Brinztech says that on **February 18, 2026**, a forum actor released a Manipal Library Portal database for free [4]. The described fields concern journals, publishers, ISSNs, full-text availability, peer-review status, countries, and internal database identifiers, while the article itself supplies no forum URL, dataset hash, record count, or MAHE confirmation [4]. -> Investigate the library system, but classify this as a published allegation rather than a verified institutional breach.

- **Credential Exposure Is Not Breach Attribution**: A LeakRadar snapshot reports **59,820 leaked credentials** associated with `manipal.edu` [3]. LeakRadar expressly says domain-associated records do not necessarily mean the organization's infrastructure was breached and may originate from information-stealer infections on users' devices; its sources include Telegram, dark-web, and underground-forum publications [3]. -> Force resets and review authentication logs for exposed identities, but do not represent the tally as 59,820 accounts stolen from SLCM.

- **HIBP and DeHashed Are Inconclusive Without Authorized Access**: Have I Been Pwned, or HIBP, requires an organization to verify control of a domain before domain-wide search; an unverified-domain request returns HTTP 403, and domain search is available on authenticated plans [21]. DeHashed's public material describes its corpus but exposed no target-specific `manipal.edu` result in the accessible page [22]. -> MAHE or MUJ should run authorized domain searches; an outside researcher cannot responsibly turn the absence of a public result into a clean bill of health.

- **No Target-Specific CVE Was Located**: Exact-name searches did not surface a CVE naming Manipal SLCM or either requested hostname. The NVD web URLs used for direct queries instead returned the unfiltered corpus and unrelated Chrome records, while Exploit-DB exposed its search interface but no target result in static extraction [26][23][25]. -> Record the finding as "no product-specific CVE found," not "the platform has no vulnerabilities."

- **Reliability Complaints Are Real but Are Not Breach Evidence**: Public users reported a payment of **INR 487,000** remaining pending despite bank deduction and a receipt, a supposedly correct password being rejected, a fee module being unavailable for one eligible student, and old and new registration numbers both being rejected [11][10][28][27]. None of these posts alleges or demonstrates hacking. -> Treat them as availability, identity-lifecycle, and transaction-integrity incidents that deserve operational investigation, not as proof of cyber intrusion.

- **No Verified SLCM Phishing Clone Surfaced**: URLScan had seen `slcm.manipal.edu` twice but displayed no malicious or phishing verdict; it had not observed `mujslcm.jaipur.manipal.edu` [16][18]. Targeted open-web, PhishTank, and OpenPhish checks did not produce a publicly verifiable SLCM impersonation record. -> Continue brand and certificate monitoring because the absence of an indexed sample only means none was found in accessible public results.

- **The Portal Has High-Integrity Functions**: MAHE's own ICT document describes SLCM as a student-and-parent system handling attendance, internal marks, external marks, result publication, and institutional broadcasts [5]. -> Authorization, audit logging, payment reconciliation, and privileged changes deserve stronger controls than an ordinary informational website.

- **Unauthorized Testing Has Legal Exposure**: Current India Code text makes unauthorized access and data extraction Section 43 acts; Section 66 applies where a Section 43 act is done dishonestly or fraudulently and carries up to three years' imprisonment, a fine up to **INR 500,000**, or both [33]. -> Obtain written authorization before testing, minimize collection, and use coordinated disclosure rather than probing production portals on personal initiative.

## Scope, Assets, and Evidence Standard

This review covers the two requested hosts, the official MAHE and MUJ web ecosystem around them, public credential-intelligence services, vulnerability catalogs, security reporting, community complaints, phishing repositories, and the Indian reporting and computer-misuse framework. It is an open-source assessment, not a penetration test. No login was attempted, no password was tested, no account enumeration was performed, and no leaked credential was reproduced.

MAHE's own documentation provides the clearest statement of SLCM's role. It calls SLCM a single-window system for students and parents and identifies attendance, internal marks, external marks, result publication, and broadcast messages or circulars as modules [5]. The MUJ page presents parent and student sign-in paths [7]. MAHE also publishes a separate Student Portal link to `sis.manipal.edu`, showing that the institutional identity and student-services surface is broader than one SLCM hostname [8].

| Asset or surface | Publicly documented function | Security significance | Evidence status |
|---|---|---|---|
| `slcm.manipal.edu` | MAHE SLCM login; the documented SLCM suite covers attendance, marks, results, and messages [5] | Confidentiality and integrity of academic records; account takeover risk | Officially verified function |
| `mujslcm.jaipur.manipal.edu` | MUJ portal with parent and student sign-in options [7] | Student and parent identity, records, and transaction exposure | Official login page verified |
| `sis.manipal.edu` | MAHE Student Portal and grievance workflow [8][29] | Additional identity and case-management surface | Official links verified |
| `libportal.manipal.edu` | Library Portal designed and maintained by MAHE's Department of Digital and Information Technology [1] | The subject of the February 2026 leak allegation | Ownership verified; breach unconfirmed |
| `payment.manipal.edu` and fee pages | MAHE payment and finance information, including Student Finance Office contact details [9] | Payment diversion, reconciliation, and impersonation risk | Official page verified |

The report uses four evidence tiers. **Tier 1, verified**, means an official source or directly readable artifact confirms the limited claim being made. **Tier 2, credible published allegation**, means a named security source reports an event, but primary artifacts or victim confirmation are missing. **Tier 3, first-person complaint**, means a user reports a problem, with no independent technical verification. **Tier 4, unsupported rumor or absence claim**, includes search-result speculation, generic CVEs, and claims that a portal was hacked merely because it malfunctioned.

This is an evidence matrix and reproducible assessment, not private chain-of-thought. The decisive rule is simple: a credential-domain match, an outage, or a scan becomes evidence of a portal breach only when a source connects it to unauthorized access, exfiltration, or manipulation of that portal.

## Exact Incident and Exposure Table

| Date or displayed age | System | Public source | What the source actually says | Potential impact | Classification |
|---|---|---|---|---|---|
| **February 18, 2026** | Manipal Library Portal | Brinztech | A forum actor allegedly released a database for free [4] | Exposure of library catalog or subscription metadata and internal identifiers | **Tier 2 - published, unconfirmed allegation** |
| No date on accessible snapshot | `manipal.edu` identities | LeakRadar | **59,820 leaked credentials** associated with the domain [3] | Credential stuffing, account takeover, password reuse, targeted phishing | **Tier 2 signal - exposure association, not breach attribution** |
| Page displayed "1y ago" | SLCM fee status | Reddit | INR 487,000 deducted and receipt held, but portal still showed pending [11] | Registration or finance hold; duplicate-payment pressure; reconciliation failure | **Tier 3 complaint** |
| Page displayed "1y ago" | MUJ SLCM login | Reddit | User said a password believed correct produced an error [10] | Temporary loss of access | **Tier 3 complaint** |
| Page displayed "2mo ago" | SLCM 1.0 fee module | Reddit | Eligible user could not see the fee portal while peers could [28] | Unequal access to time-sensitive fee workflow | **Tier 3 complaint** |
| Page displayed "3y ago" | SLCM registration login | Reddit | Old registration number became invalid after intra-sliding; the new number was also rejected [27] | Identity-lifecycle provisioning failure | **Tier 3 complaint** |
| Two scans displayed as "1mo" | `slcm.manipal.edu` | URLScan | Host seen twice; no phishing or malicious verdict displayed [16] | None established by the scan alone | **Tier 1 scan fact; not an incident** |
| Current domain page | `mujslcm.jaipur.manipal.edu` | URLScan | Host not observed in URLScan; no direct or incoming hits displayed [18] | No impact established | **Tier 1 database fact; inconclusive** |

The table's most important distinction is between **a documented report** and **a verified underlying event**. Brinztech's article is unquestionably public and specific, but that verifies publication of the allegation, not the data's authenticity or the compromise path. Reddit posts verify that users publicly complained, not that the service failed for all users or that an attacker caused the condition.

## The 2026 Library Claim Does Not Establish an SLCM Breach

### Case study: a specific dataset claim with missing primary evidence

Brinztech dates its intelligence to February 18, 2026 and says a threat actor on a prominent hacker forum released the Manipal Library Portal database for free [4]. Its field description is unusually important: publication names, publishers, ISSNs, full-text-availability periods, peer-review status, countries of origin, and internal MID database identifiers [4]. The article also says the initial leak did not appear to contain student login credentials [4].

Those details point toward cataloging and subscription metadata, not SLCM's attendance, marks, results, or fee records. SLCM is not named in the article [4]. The official library page confirms that MAHE's Department of Digital and Information Technology designed and maintains the portal [1], so the allegation is relevant to the surrounding `manipal.edu` ecosystem. It is not, however, evidence that the requested SLCM hosts shared the alleged vulnerability, database, credentials, or incident.

The article leaves major verification gaps. It provides no affected-record count, file size, forum URL, captured forum post, dataset hash, sample validation, disclosure timeline, or MAHE response. It says Brinztech does not warrant the validity of external claims and does not report confirmation by MAHE [4]. Statements in the article about possible API or content-management flaws are hypotheses, not demonstrated root cause [4].

**Decision-ready insight:** Investigators should preserve and validate any sample through authorized channels, compare alleged internal identifiers against the real library schema, review library authentication and API logs around the claimed date, and search for unusual export activity. Until that work or an official disclosure exists, the precise label is: **"unconfirmed Manipal Library Portal data-release claim, with no demonstrated SLCM nexus."**

## Credential Databases: 59,820 Matches Do Not Equal 59,820 SLCM Accounts

### LeakRadar's number and its attribution warning

LeakRadar's accessible report states that it found **59,820 leaked credentials** associated with `manipal.edu` [3]. That is a meaningful defensive signal because exposed university-domain identifiers can support credential stuffing, mailbox takeover, spear-phishing, and reset abuse. It does not identify how many credentials are unique, current, valid, student-owned, staff-owned, or linked to SLCM.

More importantly, LeakRadar's own FAQ says these records do not necessarily mean the organization's infrastructure was breached. It identifies information-stealer malware on user devices as a common source [3]. The report says it indexes information already published by third parties in Telegram channels, dark-web forums, and underground forums [3]. Its rows are domain- or brand-referencing leaked credential records, not a forensic finding about the source server [3].

The causal alternatives matter. A student's browser may have saved an SLCM password that an infostealer extracted. A reused `@manipal.edu` address and password may have come from an unrelated website breach. A combination list may merge old credentials from many events. Only a source-level breakdown, credential validation by the domain owner, and SLCM identity logs could determine which accounts were relevant and whether any succeeded.

### HIBP and DeHashed access limits

HIBP's dashboard says domain search applies to domains the user owns [17]. Its API documentation is clearer: organizations must verify control before searching a domain; attempts against an unverified domain return HTTP 403; domain search is authenticated and plan-dependent [21]. HIBP's public breach endpoint lists breached sites, not all email addresses from other-domain breaches [21]. Therefore, not seeing a named "Manipal" breach in HIBP's public breach list would not show that no individual `@manipal.edu` address appeared elsewhere.

DeHashed publicly says it collects breach and related data and supports email and API searches [22]. The accessible public page produced no target-specific Manipal result, and a domain-wide authenticated query was not available to this review. That outcome is **inconclusive**, not a negative finding.

| Source | Target-specific public result | What it supports | What it does not support |
|---|---|---|---|
| LeakRadar | 59,820 domain-associated credential records [3] | Material identity-exposure signal | A 59,820-record SLCM database theft |
| HIBP | Domain-wide result unavailable without verified control [21] | Need for MAHE-controlled query | A public conclusion that the domain is clean or breached |
| DeHashed | No target result exposed in accessible public material [22] | Service may hold relevant indexed data | A confirmed count or current compromise |
| Public breach/news searches | Brinztech library claim found; no corroborated student email dump found | One ecosystem allegation | Proof that no private, delisted, or unindexed dump exists |

**Decision-ready insight:** MAHE and MUJ should query HIBP and commercial intelligence under verified domain ownership, normalize unique identities, expire exposed credentials, check password reuse, and correlate authentication events. Public reporting should say "credentials associated with the domain were indexed," not "Manipal lost 59,820 credentials."

## No Product-Specific CVE Is Not a Clean Bill of Health

No exact-name record located in this review identified `slcm.manipal.edu`, `mujslcm.jaipur.manipal.edu`, "Manipal SLCM," or the MAHE SLCM suite as the affected product. This is a scoped search finding, not a universal negative.

The direct NVD result URLs were unreliable for proving absence: although query terms were supplied, the extracted page displayed **382,361** total records and unrelated Chrome CVEs [26][24]. Exploit-DB's extracted pages exposed the advanced-search form but no result rows or exact target match [23][25]. VulDB did not expose a target-specific result in the statically accessible content. CVE.org and open-web exact-name queries likewise produced no target-specific candidate for validation.

| Repository | Query scope | Observable result | Assessment |
|---|---|---|---|
| NVD | Manipal, SLCM, requested hostname terms | Query page fell back to the full corpus and unrelated Chrome records [26] | No candidate found; UI result cannot prove zero records |
| CVE.org | Manipal and SLCM exact-name discovery | No target-specific candidate surfaced | No published product-specific CVE located |
| Exploit-DB | Manipal and SLCM | Search interface visible, no extracted result entries [23][25] | No public exploit located; dynamic-result limitation applies |
| VulDB | Manipal and SLCM | No target-specific record exposed in accessible result | Inconclusive database-specific negative |
| Generic ERP CVEs | Broad ERP products | Numerous unrelated products exist | Not attributable without evidence SLCM uses the affected component and version |

A CVE is normally assigned to a product vulnerability, not to every deployment of that product. The official MAHE document describes SLCM's business modules but does not identify the application framework, database, third-party packages, versions, or hosting architecture [5]. Mapping a Salesforce, Microsoft, ERPNext, JavaScript-library, or web-server CVE to SLCM without that evidence would be speculation.

This produces an important tension. The lack of an indexed CVE reduces the evidence for a **publicly disclosed product flaw**, but it says little about authorization defects, configuration errors, weak password recovery, business-logic errors, or private findings. Academic marks and fee workflows especially depend on object-level authorization and transaction integrity, classes of weakness that may never receive a platform-specific CVE.

**Decision-ready insight:** Maintain a software bill of materials and version inventory, scan authenticated and unauthenticated surfaces under written authorization, and map only confirmed component versions to CVEs. Publish a security advisory when a defect is reproducible and fixed, even if no CVE is assigned.

## SLCM Reliability Complaints: Fees, Identity, and Access

### Case study 1: INR 487,000 deducted, SLCM still pending

A Reddit user reported making a full college-fee payment of **INR 487,000**, seeing the amount deducted, and holding a receipt while SLCM continued to show the fee as pending [11]. The post asked whether to contact finance or wait and provided no public resolution [11]. No hacking, unauthorized beneficiary, altered receipt, or data exposure was alleged.

The mechanism is consistent with a reconciliation or asynchronous-state failure: the payment processor, finance ledger, and portal presentation may not have synchronized. That is still security-relevant under the broader integrity and availability triad. A stale pending flag can pressure a student to pay twice, miss registration, or disclose payment evidence to an impersonator. It does not support calling the portal "hacked."

### Case study 2: registration lifecycle breaks login

Another user said an intra-sliding update produced a new registration number; the old number became invalid and the new one was also rejected [27]. A separate MUJ user said a password believed correct generated an error [10]. Neither post presented evidence of an attacker, changed email, unexpected session, password-reset message, or unauthorized record access.

The likely operational category is identity-lifecycle and provisioning failure. Registration changes must propagate consistently across identity, SLCM, finance, examination, and support systems. Where that propagation is delayed, a legitimate user can appear unauthorized even though no malicious activity occurred.

### Case study 3: fee module visible to peers, absent for one student

A more recent complaint said the fee portal was not visible in SLCM 1.0 despite the user having more than the stated 26 required credits, while peers could see it [28]. This is a useful counterexample to a blanket "site down" description: a role, eligibility, credit, or account-state decision may have failed for one user while the service remained available to others.

| Complaint | Confidentiality impact shown? | Integrity impact shown? | Availability impact shown? | Cyberattack evidence? |
|---|---:|---:|---:|---:|
| Paid fee still pending | No | **Possible transaction-state mismatch** | Possible workflow block | No [11] |
| Correct password rejected | No | Not demonstrated | **Login unavailable to reporter** | No [10] |
| Fee module absent | No | Possible eligibility-state mismatch | **Feature unavailable to reporter** | No [28] |
| Old and new registration IDs rejected | No | Possible identity-state mismatch | **Login unavailable to reporter** | No [27] |

Targeted searches did not locate a verifiable public report of unauthorized mark modification, mass unauthorized SLCM access, or a ransomware outage attributed to Manipal. No official outage chronology or historical Downdetector-style incident record was found for the named portals. Those are bounded research results, not proof such events never occurred.

MAHE publishes a student-grievance route and says its Grievance Redressal Committee includes an Ombudsman [29]. That gives affected students a canonical escalation path. The public page, however, did not expose a dedicated security-incident contact or breach-notification process in the extracted content [29].

**Decision-ready insight:** SLCM should publish transaction IDs, synchronization status, expected posting times, and a no-duplicate-payment warning. Identity changes should be monitored end to end. Support should distinguish account takeover indicators from ordinary authentication and provisioning failures.

## Phishing and Fake-Payment Surface

URLScan's domain page says `slcm.manipal.edu` had been seen twice. It associated the host with Microsoft ASN AS8075 and IPv4 address `104.211.226.160`, but displayed no malicious or phishing verdict [16]. The two visible scan ages were only "1mo," not exact dates [16]. That is ordinary observational data, not a finding that the host is malicious.

For `mujslcm.jaipur.manipal.edu`, URLScan displayed "Not observed" and no direct or incoming hits [18]. It also warned that its live snapshot is not hosted or controlled by URLScan [18]. A not-observed result means only that the service had no indexed observation under that hostname; it is neither an uptime test nor a security rating.

| Source or surface | Result for requested hosts | Phishing conclusion | Limitation |
|---|---|---|---|
| URLScan - `slcm.manipal.edu` | Seen twice [16] | No malicious or phishing verdict displayed [16] | A scan is not an abuse report |
| URLScan - `mujslcm.jaipur.manipal.edu` | Not observed [18] | No phishing record established | Lack of observation is not evidence of safety |
| PhishTank | No target-specific item surfaced in accessible public searches | **No verified listing found** | URL-by-URL API or authenticated dataset access may find records not indexed by search engines |
| OpenPhish | No target-specific item surfaced in accessible public searches | **No verified listing found** | Public landing content is not a complete historical brand search |
| Open-web/news searches | No reproducible SLCM clone or Manipal fake-fee incident located | **No public case verified** | Unreported, removed, or private-message campaigns remain possible |

The official ecosystem itself is broad enough to create user confusion. MAHE publishes a dedicated fee page with program, hostel, and refund links [31]. The payment portal lists the Student Finance Office and institutional contact details [9]. MUJ separately publishes application tracking and admissions routes [30]. The extracted fee and grievance pages exposed privacy, public-advisory, and terms links, but no specific anti-phishing or fake-fee warning text [31].

The absence of a documented clone does not remove phishing risk. Attackers do not need to compromise SLCM: they can copy branding, use a lookalike host, send a fake "fee pending" message, or exploit a real portal delay to make their request plausible. The INR 487,000 pending-status complaint illustrates the social-engineering opportunity without proving that anyone exploited it.

**Decision-ready insight:** Publish one canonical login-and-payment directory, digitally sign high-value payment mail, deploy DMARC enforcement, monitor certificate transparency and brand lookalikes, and teach students never to pay from an unsolicited message. A suspected clone should be preserved as a URL, screenshot, headers, timestamp, and transaction destination before takedown.

## CERT-In Duties and Indian Testing Boundaries

CERT-In's April 28, 2022 Directions apply mandatory reporting to service providers, intermediaries, data centres, bodies corporate, and government organizations. Covered entities must report listed cyber incidents within **six hours** of noticing them or being informed of them [20]. The listed categories include unauthorized access, compromise of systems or information, malicious-code attacks, identity theft, spoofing, phishing, denial-of-service attacks, data breach, data leak, attacks on digital-payment systems, and unauthorized access to social-media accounts [20].

The Directions also require covered entities to enable logs for ICT systems, retain them securely for a rolling **180 days** within India, and provide them to CERT-In with incident reports or when directed [20]. They require a designated point of contact for CERT-In [20]. These are directly relevant if a credential exposure is validated, an SLCM account is taken over, marks are altered without authorization, a fee system is attacked, or a library dataset is confirmed leaked.

No CERT-In advisory specifically naming Manipal SLCM was located in the reviewed material. Generic ERP vulnerabilities cannot be assumed to affect SLCM without product and version evidence. CERT-In does provide a Responsible Vulnerability Disclosure and Coordination Policy page [12], but the accessible text reviewed here did not grant a Manipal-specific safe harbor or authorization to test.

Current consolidated India Code text draws the critical permission line. Section 43 covers access without the permission of the owner or person in charge and separately covers downloading, copying, or extracting data [33]. Section 66 applies when a person dishonestly or fraudulently performs a Section 43 act and permits imprisonment up to three years, a fine up to INR 500,000, or both [33].

| Activity | Legal and operational assessment | Safer course |
|---|---|---|
| Viewing a public login page and public documentation | Ordinary passive research | Keep requests normal and do not enumerate accounts |
| Trying guessed, reused, or leaked credentials | Unauthorized account access risk under Section 43; Section 66 may apply with dishonest or fraudulent conduct [33] | Do not test; notify the institution of exposure indicators |
| Changing identifiers to access another student's records | Unauthorized access and possible data extraction | Test only in an institution-provided environment with written scope |
| Downloading a sample database to "verify" a leak | May involve unauthorized copying or extraction [33] | Send the location and hash to authorized responders; do not redistribute data |
| Running automated scans against production | May disrupt service and can create reportable scanning or incident noise | Obtain written authorization, rate limits, time window, and contacts |
| Reporting a suspected vulnerability without exploitation | Consistent with coordinated disclosure | Give reproducible, minimal-impact evidence to MAHE and, where appropriate, CERT-In |

This is not individual legal advice. The practical standard is stricter than "I meant well": obtain written authorization that names the hosts, test methods, accounts, data-handling rules, time period, and emergency contact. Stop if real student data appears. Do not alter marks, attendance, payments, or identity records even as a demonstration.

**Decision-ready insight:** MAHE and MUJ should publish a vulnerability-disclosure policy with explicit scope, safe research methods, prohibited actions, response targets, and a `security.txt` contact. Researchers should use that process or CERT-In coordination, not self-authorize production testing.

## Defensive Priorities for MAHE, MUJ, and Students

### For MAHE and MUJ

1. **Validate the library claim without contaminating evidence.** Preserve application, API, database, identity-provider, and export logs around the February 2026 claim. Obtain any sample through counsel or CERT-In, hash it, and compare only authorized records. Do not infer that SLCM is involved merely because both use `manipal.edu`.

2. **Turn the 59,820-domain signal into an identity investigation.** Under verified ownership, obtain record-level source metadata from HIBP, LeakRadar, DeHashed, and other providers. Deduplicate identities, distinguish stealer logs from third-party breaches, expire affected passwords, revoke sessions, and hunt for successful reuse. LeakRadar's own warning makes source attribution essential [3].

3. **Protect high-integrity academic actions.** Require step-up authentication and dual control for mark changes, result publication, fee adjustments, and identity merges. Log before-and-after values, actor, source address, approval chain, and transaction ID. MAHE's documented module list shows why academic integrity must be treated as a privileged workflow [5].

4. **Fix transaction observability.** Expose payment-processor reference, ledger-posting state, expected settlement time, and support escalation in SLCM. Alert when money is captured but the student ledger remains pending beyond policy. The public INR 487,000 complaint demonstrates the user harm a synchronization gap can create [11].

5. **Harden identity lifecycle.** Test registration-number changes, intra-sliding, course migration, parent linkage, and account recovery across all connected systems. A user whose old and new identifiers both failed illustrates a control-plane reliability gap [27].

6. **Meet and exceed CERT-In readiness.** Maintain searchable logs for at least the mandated 180-day period in India, designate the required contact, and rehearse six-hour reporting [20]. Preserve payment and privileged-change logs longer where academic or financial policy requires it.

7. **Publish security communications.** Provide a status page, incident archive, canonical login directory, anti-fraud page, security contact, and disclosure policy. This reduces rumor, helps students distinguish outage from takeover, and gives researchers a lawful path.

### For students and parents

Use only links reached through the official MAHE or MUJ sites, not links in unexpected fee messages. Use a unique password and a password manager; do not reuse the SLCM password on other sites. If a payment remains pending, retain the bank reference and official receipt, contact the published finance or grievance route, and do not pay again solely because an unsolicited caller or message demands it. MAHE's grievance page provides a student escalation link and Ombudsman-backed process [29].

If login fails, check for password-reset or profile-change notices, but do not assume compromise from an error alone. Report genuine takeover indicators such as an unknown recovery address, unrecognized session, changed marks, altered payment destination, or reset message not initiated by the user. Never test another student's identifier or account.

## Synthesis: Incident, Exposure, Reliability, and Rumor

The evidence falls into four mechanisms that must not be collapsed into one story.

| Dimension | Library leak allegation | Credential exposure | SLCM complaints | CVE and phishing searches |
|---|---|---|---|---|
| Mechanism | Alleged database release by a forum actor [4] | Stealer logs, combination lists, or third-party dumps may associate credentials with the domain [3] | Payment reconciliation, provisioning, eligibility, or login failures [11][10][28][27] | Public cataloging and scanning visibility |
| Scope | Separate library portal | Identities using or referencing `manipal.edu` | Individual student workflows | Publicly indexed disclosures and observations |
| Evidence base | One detailed secondary article; no victim confirmation [4] | One numerical domain report plus provider caveats [3] | First-person posts without technical validation | No exact product-specific CVE or phishing verdict located [16][23] |
| Main risk | Data exposure and possible repeat access | Account takeover and phishing | Availability, integrity, missed deadlines, duplicate-payment pressure | False reassurance from database silence |
| Time horizon | Historical incident investigation | Immediate identity hygiene and continuing monitoring | Operational remediation and trend analysis | Continuous inventory and brand monitoring |

The non-obvious tension is that the **strongest numerical signal**, 59,820 credentials, is also the weakest for breach attribution. Conversely, the smaller library allegation is specific about the dataset but lacks independent proof and does not concern SLCM. The student complaints are concrete descriptions of harm but offer no attacker evidence. The vulnerability and phishing searches are useful chiefly because they constrain what can responsibly be claimed, not because they prove safety.

A second tension concerns confidentiality versus integrity. Public discussion tends to focus on leaked data, but SLCM's documented responsibilities make unauthorized changes to marks, results, attendance, or payment state potentially more consequential than exposure of library catalog metadata. Yet no public evidence reviewed here demonstrates mark tampering. That gap should motivate stronger audit controls, not an unsupported assertion that tampering occurred.

A third tension is visibility. MAHE has public grievance, fee, and privacy links [29][31], but the extracted pages did not expose a clear security-incident contact, anti-fraud warning, or public SLCM incident archive [29][31]. Poor security communication can make routine failures look like breaches and can leave real incidents underreported.

The holistic conclusion is therefore not "nothing happened" and not "SLCM was hacked." It is that the public record contains one unconfirmed ecosystem leak claim, one material credential-exposure signal with major attribution limits, several genuine service complaints, and no publicly verified compromise of the named SLCM portals.

## VERDICT

**Verdict:** As of the research cutoff, there is **no publicly verified evidence that `slcm.manipal.edu` or `mujslcm.jaipur.manipal.edu` suffered a confirmed breach, ransomware incident, unauthorized mark-tampering event, published product-specific CVE, or documented phishing clone.** This is a bounded open-source conclusion, not proof that no private or undisclosed incident occurred.

The most important security findings are:

1. **Published but unconfirmed:** the February 18, 2026 Manipal Library Portal database-release claim, involving catalog or subscription metadata and internal identifiers, with no demonstrated SLCM connection and no MAHE confirmation [4].
2. **Material exposure signal, not breach proof:** LeakRadar's 59,820 domain-associated credential records, subject to its explicit warning that user-device stealers and third-party publications may be the source [3].
3. **Verified public complaints, not verified cyber incidents:** fee-status, fee-module, password, and registration-ID failures [11][10][28][27].
4. **No exact public vulnerability or phishing match found:** database and scan results did not produce a target-specific CVE, exploit, or malicious verdict [16][23][25].

**Overall confidence: Moderate-high.** Confidence is high in what the cited pages state and in the classification of the Reddit posts as complaints. Confidence is moderate in negative findings because HIBP domain search requires verified control, DeHashed and some vulnerability/phishing databases restrict or dynamically render results, and undisclosed incidents are inherently invisible to open-source research.

**Priority:** MAHE and MUJ should investigate identity exposure and the library allegation, improve payment and identity-state reconciliation, deploy stronger privileged-action auditing, and publish a clear security-reporting channel. Those actions address the evidence without amplifying rumors.

## References

1. [
	Library Portal
](https://libportal.manipal.edu/)
2. *LeakRadar · GitHub*. https://github.com/LeakRadar
3. *manipal.edu Data Breach Report | LeakRadar*. https://leakradar.io/en/report/manipal.edu
4. *Brinztech Alert: Database of Manipal Library Portal Leaked*. https://www.brinztech.com/breach-alerts/brinztech-alert-database-of-manipal-library-portal-leaked/
5. *Contents*. http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf
6. [
	MU SLcM
](https://slcm.manipal.edu/)
7. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
8. *Student Portal Login- MAHE (Manipal Academy Of Higher Education)*. https://www.manipal.edu/mu/academics/student-portal.html
9. *MAHE Payment Portal*. http://payment.manipal.edu/
10. *Reddit - The heart of the internet*. https://www.reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue
11. *Reddit - The heart of the internet*. https://www.reddit.com/r/Manipal_Academics/comments/1lzf0ht/paid_my_fees_but_still_showing_as_pending_on_slcm
12. *RVDCP*. https://www.cert-in.org.in/RVDCP.jsp
13. *Indian - Computer Emergency Response Team*. https://www.cert-in.org.in/
14. *MINISTRY OF LAW, JUSTICE AND COMPANY AFFAIRS (Legislative Department)*. https://www.meity.gov.in/static/uploads/2024/03/ITbill_2000.pdf
15. *OpenPhish - Phishing Intelligence*. https://openphish.com/
16. *slcm.manipal.edu - urlscan.io*. https://urlscan.io/domain/slcm.manipal.edu
17. *Have I Been Pwned: Sign In to Your Dashboard*. https://haveibeenpwned.com/DomainSearch
18. *mujslcm.jaipur.manipal.edu - urlscan.io*. https://urlscan.io/domain/mujslcm.jaipur.manipal.edu
19. *PhishTank | Join the fight against phishing*. https://www.phishtank.net/
20. *No. 20(3)/2022-CERT-In Government of India Ministry of Electronics and Information Technology (MeitY) Indian Computer Emergency Response Team (CERT-In) Electronics Niketan,*. https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf
21. *Have I Been Pwned: API Documentation*. https://haveibeenpwned.com/API/v3
22. *DeHashed — #FreeThePassword*. https://dehashed.com/
23. *Exploit Database Search*. https://www.exploit-db.com/search?q=Manipal
24. *NVD - Search and Statistics*. https://nvd.nist.gov/vuln/search/results?form_type=Basic&results_type=overview&query=SLCM&search_type=all&isCpeNameSearch=false
25. *Exploit Database Search*. https://www.exploit-db.com/search?q=SLCM
26. *NVD - Search and Statistics*. https://nvd.nist.gov/vuln/search/results?form_type=Basic&results_type=overview&query=Manipal&search_type=all&isCpeNameSearch=false
27. *Reddit - The heart of the internet*. https://www.reddit.com/r/Manipal_Academics/comments/1993mdc/slcm_login/
28. *Fees not showing in slcm : r/Manipal_Academics*. https://www.reddit.com/r/Manipal_Academics/comments/1u8476b/fees_not_showing_in_slcm
29. *Grievances | MAHE - Manipal Academy of Higher Education *. https://www.manipal.edu/mu/about-us/grievances.html
30. *ADMISSIONS - Manipal University Jaipur*. https://jaipur.manipal.edu/admissions.php
31. *Fee & Refunds 2026*. https://www.manipal.edu/mu/admission/fees.html
32. *India Code: Information Technology Act, 2000 (Central Act 21 of 2000)*. https://www.indiacode.nic.in/handle/123456789/13116?sam_handle=123456789%2F1362
33. *THE INFORMATION TECHNOLOGY ACT, 2000 ––––––––– ARRANGEMENT OF SECTIONS –––––––––*. https://www.indiacode.nic.in/bitstream/123456789/13116/1/it_act_2000_updated.pdf
