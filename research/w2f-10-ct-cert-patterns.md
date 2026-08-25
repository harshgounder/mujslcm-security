# MUJ SLCM Certificate Transparency Exposure and Defensive Priorities

## Executive Summary

- **Two Live Naming Conventions**: Public CT records and publicly indexed portal pages contain both `mujslcm.jaipur.manipal.edu` and `muj.slcm.jaipur.manipal.edu`; these are distinct DNS names, not interchangeable spellings [7][6][11][17]. -> Maintain both names in the authorized certificate inventory until service owners document whether they are parallel services, aliases, or migration artifacts.
- **Current Certificates For Both Names**: As of **2026-08-25**, CT shows an exact-name certificate for `mujslcm` valid through **2026-12-21** and one for `muj.slcm` valid through **2026-12-22** [7][6]. -> Treat the name split as current certificate-management scope, not merely historical residue.
- **Dense 2024 Issuance Cluster**: Six deduplicated MUJ SLCM-related certificates were associated with a late-December 2024 issuance cluster, including several overlapping exact-name certificates [7][6]. -> Review CA order history and deployment records internally; **inference:** the cluster may reflect retries, reissues, validation changes, or planned rollover, but CT alone cannot establish the cause.
- **Test-Labeled Certificates Are Historical But Material**: The Jaipur CT snapshot contains five certificates for `testmycampus.jaipur.manipal.edu`, one for `testerp.jaipur.manipal.edu`, and one MUJ SLCM certificate that included `npfslcm.jaipur.manipal.edu` [6]. All had expired by the report date. -> Confirm retirement and ownership in approved internal systems rather than testing the names from the Internet.
- **Wildcard Use Was Repeated**: The snapshot contains nine deduplicated certificates covering `*.jaipur.manipal.edu`, with validity periods from **2020-05-07** through **2023-12-16** [6]. -> Verify whether the wildcard and its private keys have been retired, where they were deployed, and whether narrowly scoped replacements now exist.
- **Cross-Family SAN Grouping Is The Most Surprising Pattern**: CT records paired the Jaipur wildcard SAN with CNs such as `*.manipalglobal.com` and `*.manipaldubai.com`; other certificates paired `jaipur.manipal.edu` with CN `manipal.edu` and `apply.jaipur.manipal.edu` with CN `apply.manipal.edu` [6]. -> Interpret these as certificate grouping or issuance architecture, not proof of compromise, while assigning explicit ownership across the domain family.
- **CT Reveals Names, Not Reachability**: CT is a public record of certificate issuance, and CT logs are append-only and publicly auditable [3][4][2]. -> A logged name should become an inventory lead, but it does not by itself prove current DNS, a listening service, application ownership, or vulnerability.
- **CT Monitoring Has Important Blind Spots**: Cloudflare states that CT monitoring triggers when a certificate covering a monitored domain is issued and logged, but it does not detect lookalike domains such as character substitutions or added hyphens [21]. -> Combine CT alerts with approved brand-domain monitoring and internal certificate records.
- **Central Lifecycle Management Is The Main Control**: NIST recommends formal certificate-management programs with policies, inventories, continuous monitoring, and automation; it warns that poor certificate management can cause outages and security breaches [19][22]. -> Assign owners, reconcile CT with the authoritative inventory, automate renewal, and create a documented response path for unknown issuance.

## Scope, Safety Boundary, and Evidence Status

This report is limited to **passive public information**: publicly indexed CT data, public documentation, and publicly rendered portal text. It does not perform login attempts, DNS brute forcing, port scanning, vulnerability probing, directory enumeration, credential testing, or interaction with non-public application functions. No finding should be used as authorization to access a system.

The supplied target context describes `mujslcm.jaipur.manipal.edu` as ASP.NET MVC 5.3 on .NET Framework 4.x and IIS 10, behind Akamai, with Microsoft 365 identity. Those details are treated here as **user-supplied scope assumptions**, not findings. CT records describe certificates and names; they do not establish an application framework, web-server version, CDN path, or identity provider. The public exact-name portal does visibly display `WELCOME TO MUJ PORTAL`, sign-in options, and `@muj.manipal.edu` [11], but that text alone does not prove Microsoft 365 implementation.

A reasoning-transparency note is necessary: private chain-of-thought is not reproduced. Instead, the report provides a reproducible evidence trail in the form **observation -> bounded interpretation -> limitation -> defensive decision**. Every interpretation that goes beyond the literal CT record is labeled **Inference**.

### Exact evidence model

| Evidence type | What it directly establishes | What it does not establish | Treatment in this report |
|---|---|---|---|
| CT certificate row | A certificate or precertificate record containing the recorded CN/SAN names, issuer, serial, timestamps, and validity period was publicly logged [7][8][6] | DNS resolution, current deployment, service ownership, private-key location, or vulnerability | Direct observation |
| Repeated serial in CT | The same certificate serial appears in more than one returned log entry [7][8][6] | Multiple independently issued certificates | Deduplicate by serial |
| Expired `not_after` | The certificate's recorded validity ended before 2026-08-25 [7][8][6] | Whether a server still incorrectly presents it | Direct observation only |
| Lexical label such as `test` | The public certificate name contains that literal label [6] | That the host is truly non-production, reachable, or weakly protected | `Test-labeled`, not `confirmed test environment` |
| Public portal rendering | A public page displays the cited words and sign-in labels [11][17] | Backend technology, tenancy, authentication flow, or trust boundary | UI context only |
| Analyst relationship finding | Two names, dates, or certificate fields form a notable pattern | Causation or organizational intent | Explicitly labeled inference |

**Decision-ready insight:** CT data is reliable for discovering certificate names and issuance history, but only authorized internal configuration and ownership records can convert those leads into confirmed assets.

## What Certificate Transparency Proves

Certificate Transparency is designed around public visibility of TLS certificate issuance. DigiCert describes CT logs as a publicly auditable record of TLS/SSL certificate issuance and says that this visibility holds CAs accountable [3]. Google's CT documentation describes certificate logs as append-only ledgers [4]. Let's Encrypt similarly defines CT as a system for logging and monitoring the issuance of TLS certificates and states that it submits all certificates it issues to CT logs [2].

This architecture creates a useful asymmetry for defenders. A university does not need to know which team requested a certificate before noticing that the certificate exists in a public log. A monitor can alert on new names, unfamiliar issuers, unexpected SAN groupings, or parallel naming schemes. Cloudflare describes its CT-monitoring feature as alerting when a certificate covering the monitored domain is issued by a CA and added to a public CT log [21].

The same visibility has a disclosure cost. A certificate name can reveal a meaningful label even when the service is obscure, retired, private in intent, or no longer deployed. The Jaipur data exposes labels including `testmycampus`, `testerp`, `mujerp`, `dmsmuj`, `npfslcm`, `idp`, `pms`, and `lcs` [6]. **Inference:** those labels give an external observer a partial vocabulary of system roles and project names. They do not provide credentials, application data, IP addresses, or proof that any host remains online.

A certificate's validity window is also not a service-availability timeline. `not_before` and `not_after` answer when the certificate was intended to be valid, while the CT entry timestamp answers when the record entered a log. None of those fields says that a server used the certificate continuously or at all. For this reason, this report uses `current certificate record` rather than `live host`.

CT monitoring also has two documented limitations relevant to a university program. First, a shared certificate can generate an alert because the monitored domain appears beside names that do not belong to the subscriber [21]. Second, CT monitoring does not detect typo or lookalike domains outside the monitored namespace; Cloudflare gives substitutions and hyphenation as examples [21]. Thus, CT should complement, not replace, authoritative certificate inventory, DNS governance, and brand protection.

**Decision-ready insight:** use CT as an early-warning and reconciliation source. Never promote a CT name directly to a confirmed asset, incident, or vulnerability without internal evidence.

## The `mujslcm` Certificate History: 10 Unique Serials, 9 Expired

The exact `mujslcm.jaipur.manipal.edu` query returned **10 unique certificate serials** after duplicate CT rows were collapsed. The records contain three distinct names across CN and SAN fields: `mujslcm.jaipur.manipal.edu`, `www.mujslcm.jaipur.manipal.edu`, and `dms.jaipur.manipal.edu` [7].

### Exact certificate table for `mujslcm.jaipur.manipal.edu`

| # | CN | SAN/name values | Issuer shorthand | Not before | Not after | Serial | Status on 2026-08-25 |
|---:|---|---|---|---|---|---|---|
| 1 | `mujslcm.jaipur.manipal.edu` | `mujslcm.jaipur.manipal.edu` | Entrust DV TLS Issuing RSA CA 2 | 2025-12-22 00:00:00 | 2026-12-21 23:59:59 | `00a8fe91aaac91730fe90d034dee36f7c7` | Current [7] |
| 2 | `mujslcm.jaipur.manipal.edu` | Exact name | Entrust OV TLS Issuing RSA CA 1 | 2025-03-07 12:04:28 | 2025-12-22 16:25:10 | `540dddb8fc45abd142751ef840ba2878` | Expired [7] |
| 3 | `mujslcm.jaipur.manipal.edu` | Exact name | Entrust OV TLS Issuing RSA CA 1 | 2024-12-23 04:45:00 | 2025-12-22 16:25:10 | `66b7a29b97c486de45aa5d16d51a176c` | Expired [7] |
| 4 | `mujslcm.jaipur.manipal.edu` | Exact name | Entrust OV TLS Issuing RSA CA 1 | 2024-12-22 11:54:26 | 2025-12-22 11:03:13 | `7f04f626614ef2dff9c2eec83f9a3575` | Expired [7] |
| 5 | `mujslcm.jaipur.manipal.edu` | Exact name | Entrust OV TLS Issuing RSA CA 1 | 2024-12-22 11:21:36 | 2025-12-21 13:42:48 | `43805d9dce1c7ab0166d02f9496b7ef7` | Expired [7] |
| 6 | `mujslcm.jaipur.manipal.edu` | Exact name | Entrust OV TLS Issuing RSA CA 1 | 2024-12-22 10:53:52 | 2025-12-22 11:03:13 | `3b50dfd98967c76d487067a86d8d77c5` | Expired [7] |
| 7 | `mujslcm.jaipur.manipal.edu` | Exact name | Entrust OV TLS Issuing RSA CA 1 | 2024-12-22 09:54:33 | 2025-12-21 13:42:48 | `4e428f98ea2bbbc9cbee94de12af1ea1` | Expired [7] |
| 8 | `mujslcm.jaipur.manipal.edu` | Exact name; `www.mujslcm.jaipur.manipal.edu` | Entrust Certification Authority - L1K | 2024-01-02 05:23:09 | 2025-01-02 05:23:08 | `129a61ca7c5adb29a112c84e44ad3100` | Expired [7] |
| 9 | `mujslcm.jaipur.manipal.edu` | Exact name | Entrust Certification Authority - L1K | 2022-11-21 09:03:22 | 2023-11-21 09:03:22 | `127b4db235082feb98d72c49d260ab97` | Expired [7] |
| 10 | `dms.jaipur.manipal.edu` | `mujslcm.jaipur.manipal.edu` | Entrust Certification Authority - L1K | 2022-05-11 06:04:05 | 2022-11-20 06:04:05 | `71cac8c7107780b18cff77ab2f88a5c4` | Expired [7] |

The most important lifecycle signal is not merely that old certificates expired. Expiration is normal. The stronger signal is the **concentration of overlapping serials** around December 22-23, 2024. At least six related certificates were recorded in the family analysis, with multiple serials sharing the exact subject but slightly different issue and expiry times [7][6].

**Inference:** this pattern is consistent with repeated requests, reissues, validation retries, or a managed rollover process. It is not evidence of malicious issuance. The appropriate defensive response is to compare the serials with Entrust order history and internal deployment records. Unknown serials should trigger the approved incident and CA-contact process; known but unused serials should be documented and, where appropriate, revoked by authorized owners.

The 2022 CN/SAN relationship is also notable. One certificate used CN `dms.jaipur.manipal.edu` while its returned name value was `mujslcm.jaipur.manipal.edu` [7]. **Inference:** this suggests that two service labels were grouped in one certificate or that the CA display/search result reflects a SAN-based relationship. It does not prove that the applications shared a server or trust boundary.

**Decision-ready insight:** the exact `mujslcm` name should have one documented owner, one approved certificate profile, and a reconciled explanation for each of the ten serials.

## `muj.slcm` Versus `mujslcm`: A Current Naming Collision, Not A Typo Finding

Both spellings appear in CT and both resolve to publicly indexed portal content. The exact `mujslcm` page displays `WELCOME TO MUJ PORTAL`, while the `muj.slcm` page also displays `WELCOME TO MUJ PORTAL` and a sign-in control [11][17]. This establishes that both names are publicly represented. It does not establish whether they route to the same origin or application.

### Exact `muj.slcm.jaipur.manipal.edu` certificate table

| # | CN | SAN/name values | Issuer shorthand | Not before | Not after | Serial | Status on 2026-08-25 |
|---:|---|---|---|---|---|---|---|
| 1 | `muj.slcm.jaipur.manipal.edu` | Exact name | Entrust DV TLS Issuing RSA CA 2 | 2025-12-22 00:00:00 | 2026-12-22 23:59:59 | `09c867ca587b8eaa30e0c30af2eb1f2d` | Current [6] |
| 2 | `muj.slcm.jaipur.manipal.edu` | Exact name; `www.muj.slcm.jaipur.manipal.edu` | Entrust Certification Authority - L1K | 2024-06-13 06:14:11 | 2025-06-13 06:14:10 | `71e4d600aecc3e306fa7d884c1e688b2` | Expired [6] |
| 3 | `muj.slcm.jaipur.manipal.edu` | Exact name | Entrust Certification Authority - L1K | 2023-06-13 04:43:37 | 2024-06-13 04:43:37 | `02fb2d9945f461e05b3937d921967fb3` | Expired [6] |
| 4 | `dmsmuj.jaipur.manipal.edu` | `dmsmuj`; `muj.slcm`; `www.dmsmuj` | Entrust Certification Authority - L1K | 2022-08-16 10:47:49 | 2023-06-10 10:47:49 | `51c255f7c2685cb52ac70e026a8115fb` | Expired [6] |

The two current records were issued on the same date by the same Entrust DV issuing CA but have separate serials and one-day-different expiry dates [7][6]. **Inference:** coordinated renewal is more plausible than an accidental spelling error, although only the service owner can confirm whether the two names support compatibility, migration, or separate routes.

The security concern is not that one spelling is inherently dangerous. The concern is governance ambiguity. Users, help-desk staff, documentation writers, identity administrators, certificate operators, and CDN administrators may refer to different names. Ambiguity can cause incorrect links, missed monitoring rules, incomplete allowlists, or failure to retire a legacy endpoint.

### Naming-governance decision table

| Question for authorized owners | Why CT raises it | Required evidence | Safe decision |
|---|---|---|---|
| Are both names intended to remain public? | Both have current certificates [7][6] | Application and DNS owner records | Keep and monitor, or retire one through change control |
| Do they represent one service? | Both pages display the MUJ portal label [11][17] | Approved architecture and routing configuration | Document canonical name and aliases |
| Why does each have a separate certificate? | Separate current serials exist [7][6] | CA orders and certificate-deployment inventory | Preserve only justified profiles |
| Should `www` variants remain? | Historical certificates included both `www` forms [7][6] | DNS and product requirements | Remove unnecessary SANs at next approved issuance |
| Is either a legacy transition name? | Records span 2022-2026 [7][6] | Change history and user communications | Set an owner-approved retirement date if legacy |

**Decision-ready insight:** treat `muj.slcm` and `mujslcm` as a live namespace-governance issue, not a typo to be tested externally.

## Test-Labeled Names and Expired SANs

The Jaipur-family snapshot exposes two names with an explicit `test` prefix and one SLCM-related `npf` label. Calling all of them `development systems` would exceed the evidence. The defensible description is **test-labeled or environment-looking certificate names**.

### Exact test-labeled and adjacent SLCM certificate table

| Name | CN/SAN relationship | Validity | Serial | Status | Evidence-safe interpretation |
|---|---|---|---|---|---|
| `testmycampus.jaipur.manipal.edu` | CN and SAN exact | 2025-05-31 to 2025-11-30 | `05e1f5b42617acd5f11f184e599ebf5c` | Expired | Fifth observed test-labeled certificate [6] |
| `testmycampus.jaipur.manipal.edu` | CN and SAN exact | 2025-01-14 to 2025-07-14 | `0e514f118ec2584a157e85267f318f5d` | Expired | Repeated issuance [6] |
| `testmycampus.jaipur.manipal.edu` | CN and SAN exact | 2024-08-27 to 2025-02-27 | `0b17c64c3ea2dc20f72032e9c907e8c1` | Expired | Repeated issuance [6] |
| `testmycampus.jaipur.manipal.edu` | CN and SAN exact | 2024-04-10 to 2024-10-10 | `0da3a30e81ef60fe1fb474d6e8064cf1` | Expired | Repeated issuance [6] |
| `testmycampus.jaipur.manipal.edu` | CN and SAN exact | 2023-07-07 to 2024-01-07 | `0956c13dee80f4985c19d697a4accc28` | Expired | Earliest record in extracted sequence [6] |
| `testerp.jaipur.manipal.edu` | CN and SAN exact | 2023-06-29 to 2024-06-29 | `0dec749327a5812f292aadf01e04bee3` | Expired | Explicitly test-labeled ERP-related string [6] |
| `npfslcm.jaipur.manipal.edu` | SAN beside CN `mujslcm.jaipur.manipal.edu` | 2025-03-07 to 2025-12-22 | `540dddb8fc45abd142751ef840ba2878` | Expired | SLCM-adjacent SAN; `npf` meaning unconfirmed [6] |

### Case study: the `testmycampus` renewal train

Five serials cover `testmycampus` over overlapping six-month windows between 2023 and late 2025 [6]. That is stronger evidence of repeated certificate issuance than a single forgotten certificate would provide. It remains insufficient to show that a test service was continuously reachable.

**Inference:** the repeated sequence suggests the name was intentionally maintained for some period rather than appearing in one accidental request. A defensive owner should therefore search approved CA-account, CMDB, DNS, load-balancer, and repository records for the exact string. If no owner or business purpose exists, the correct response is controlled retirement, not external probing.

The `npfslcm` record demonstrates why SAN review matters. It appeared beside `mujslcm` on serial `540dd...`, meaning a query focused only on CNs could miss it [6]. Certificate inventory should parse every SAN, normalize case, and retain the relationship between names sharing a serial.

**Decision-ready insight:** prioritize repeated test-labeled names over one-off labels, but confirm them through internal ownership data rather than assuming exposure from CT alone.

## Wildcards and Cross-Domain Certificate Grouping

The Jaipur-family snapshot contains nine deduplicated wildcard certificates for `*.jaipur.manipal.edu`. All nine were expired by 2026-08-25 [6]. Wildcards reduce the number of certificates needed across sibling names, but they can broaden key reuse and obscure per-service ownership if not tightly managed.

### Exact wildcard history

| # | Wildcard SAN | Issuer | Not before | Not after | Serial | Status |
|---:|---|---|---|---|---|---|
| 1 | `*.jaipur.manipal.edu` | Amazon RSA 2048 M01 | 2022-11-17 | 2023-12-16 | `09d3ebbe0b10aadf7a3c7f092c4ff06a` | Expired [6] |
| 2 | `*.jaipur.manipal.edu` | Amazon Server CA 1B | 2021-10-18 | 2022-11-16 | `07d6ca07d8d7aafc305d19fc65db2253` | Expired [6] |
| 3 | `*.jaipur.manipal.edu` | Amazon Server CA 1B | 2021-09-02 | 2022-10-01 | `035b3b16aec208363da03031a7345a32` | Expired [6] |
| 4 | `*.jaipur.manipal.edu` | Amazon Server CA 1B | 2021-07-03 | 2022-08-01 | `08e10a21fb7afdce6b07fc2588b3681b` | Expired [6] |
| 5 | `*.jaipur.manipal.edu` | Amazon Server CA 1B | 2020-08-01 | 2021-08-31 | `0754421e9c3402ece9ee25c70f5f0d2c` | Expired [6] |
| 6 | `*.jaipur.manipal.edu` | Amazon Server CA 1B | 2020-07-01 | 2021-07-31 | `0e4be35b3b11f96394197ca188623755` | Expired [6] |
| 7 | `*.jaipur.manipal.edu` | Amazon Server CA 1B | 2020-05-29 | 2021-06-28 | `0e00764432d9c9b027a75e259b6a90c3` | Expired [6] |
| 8 | `*.jaipur.manipal.edu` | Amazon Server CA 1B | 2020-05-21 | 2021-06-20 | `0e88cd33100b271423ebbadcfb878fad` | Expired [6] |
| 9 | `*.jaipur.manipal.edu` | Amazon Server CA 1B | 2020-05-07 | 2021-06-06 | `0721dfa021cd224455eb5f92b11cb790` | Expired [6] |

The wildcard sequence contains several overlapping periods in 2020-2022 [6]. **Inference:** overlap may reflect certificate replacement, separate cloud resources, or parallel deployment. It does not prove that one private key was shared among all hosts.

Let's Encrypt documents that DNS-01 validation can issue wildcard certificates and warns that placing full DNS API credentials on a web server significantly increases impact if that server is compromised; it recommends narrowly scoped credentials or separate validation infrastructure [20]. That is general control guidance, not evidence that MUJ used Let's Encrypt or exposed DNS credentials.

### Cross-domain CN/SAN groupings

| CN family | Jaipur SAN relationship | Observed period or count | Analyst assessment |
|---|---|---|---|
| `*.manipalglobal.com` | SAN `*.jaipur.manipal.edu` | Eight wildcard serials from 2020-2022 [6] | **Inference:** shared certificate-management or cloud issuance context; ownership should be explicit |
| `*.manipaldubai.com` | SAN `*.jaipur.manipal.edu` | One serial valid 2022-11-17 to 2023-12-16 [6] | Same caution; not proof of cross-domain routing |
| `manipal.edu` | SANs `jaipur.manipal.edu`, `www.jaipur.manipal.edu` | Eight listed serials from 2018-2026 [6] | Likely domain-family grouping, subject to owner confirmation |
| `apply.manipal.edu` | SAN `apply.jaipur.manipal.edu` | Seven listed serials from 2018-2025 [6] | Likely shared admissions naming, subject to confirmation |
| `MUJONE.JAIPUR.MANIPAL.EDU` | Lowercase-equivalent SAN | One serial valid 2025-06-26 to 2026-06-26 [6] | Case-only presentation difference; DNS names are conventionally compared case-insensitively |

The broadest concern is not the wildcard's public visibility. The control concern is whether one compromised deployment or credential could affect many names. That depends on private-key distribution, validation credentials, and certificate termination architecture, none of which CT reveals.

**Decision-ready insight:** confirm that the historical wildcard is retired, identify every authorized deployment that held its key, and prefer service-specific certificates where operationally feasible.

## How CT Reveals Manipal's Service Vocabulary

The extracted Jaipur snapshot contained **27 distinct name strings** across CN and SAN values [6]. The following classification is intentionally conservative.

### Exact observed-name inventory

| Category | Exact CT-observed names | Status of classification |
|---|---|---|
| Base and public web | `jaipur.manipal.edu`, `www.jaipur.manipal.edu`, `admissions.jaipur.manipal.edu`, `apply.jaipur.manipal.edu`, `helpdesk.jaipur.manipal.edu` | Function suggested by ordinary words; purpose not independently verified [6] |
| MUJ portal and SLCM | `mujslcm.jaipur.manipal.edu`, `www.mujslcm.jaipur.manipal.edu`, `muj.slcm.jaipur.manipal.edu`, `www.muj.slcm.jaipur.manipal.edu`, `npfslcm.jaipur.manipal.edu` | CT-observed names; exact and dotted portals also have public page evidence [6][11][17] |
| Explicit test labels | `testmycampus.jaipur.manipal.edu`, `testerp.jaipur.manipal.edu` | Test-labeled strings only [6] |
| Campus and ERP labels | `mycampus.jaipur.manipal.edu`, `mujerp.jaipur.manipal.edu`, `mujone.jaipur.manipal.edu`, `www.mujone.jaipur.manipal.edu` | **Inference:** likely product or project vocabulary [6] |
| DMS-related | `dms.jaipur.manipal.edu`, `www.dms.jaipur.manipal.edu`, `dmsmuj.jaipur.manipal.edu`, `www.dmsmuj.jaipur.manipal.edu` | Acronym meaning and architecture unconfirmed [6] |
| Other role-like acronyms | `rms.jaipur.manipal.edu`, `www.rms.jaipur.manipal.edu`, `lcs.jaipur.manipal.edu`, `www.lcs.jaipur.manipal.edu`, `pms.jaipur.manipal.edu`, `idp.jaipur.manipal.edu` | Role-like names; `idp` is identity-looking, but actual function is unconfirmed [6] |
| Wildcard | `*.jaipur.manipal.edu` | Direct wildcard observation [6] |

This is the central OSINT lesson. CT does not reveal an internal network map, but it can reveal **internal-looking naming vocabulary** used in publicly trusted certificates. Acronyms and project names can help a defender discover assets missing from the CMDB. They can also help an outsider construct guesses, which is why certificate-name minimization matters.

**Inference:** the coexistence of `mujslcm`, `muj.slcm`, `dms`, `dmsmuj`, `mujerp`, `mycampus`, and `mujone` suggests multiple generations or functional groupings of student and campus systems. The evidence does not establish which are production, legacy, externally reachable, or operated by the same team.

**Decision-ready insight:** reconcile all 27 strings against authoritative ownership records and mark each as current, retired, alias, third-party managed, or unknown.

## Defensive Case Study: Turning CT Into An Authorized Control Loop

NIST states that many organizations lack centralized TLS-certificate monitoring and management [19]. Its example architecture uses policies, certificate inventories, continuous monitoring of operational and security status, and automated certificate management [19]. NIST also warns that poor management can result in outages, breaches, reputational harm, and exposure of confidential data [22].

For MUJ, the practical case is the late-2024 exact-name cluster. CT contributes serials and dates. The CA account contributes requestor, validation method, order status, and revocation state. The certificate manager or load balancer contributes deployment status. DNS governance contributes name ownership. The application owner contributes business purpose. Only the combined record can explain whether the six certificates were expected.

### Authorized defensive workflow

| Stage | Passive or internal action | Output | Escalation rule |
|---:|---|---|---|
| 1 | Monitor CT for `manipal.edu` and delegated families | New serial, names, issuer, validity | Alert on unknown issuer, new label, or unusual SAN grouping |
| 2 | Normalize names and deduplicate by serial | One certificate object with all CN/SAN relationships | Do not count duplicate log rows as separate certificates |
| 3 | Match against approved CA and inventory records | Owner, request, deployment, renewal policy | Unknown serial becomes a certificate-governance incident |
| 4 | Classify names | Current, legacy, alias, test, third-party, retired, unknown | `Unknown` requires owner assignment, not Internet probing |
| 5 | Review wildcard and multi-family certificates | Key custody and blast-radius record | Replace unjustified broad scope through change control |
| 6 | Validate retirement internally | CA revocation state, DNS record, deployment inventory | Do not test public endpoints without written authorization |
| 7 | Automate renewal and expiry alerts | Renewal evidence and exception queue | Escalate before expiry according to institutional SLA |
| 8 | Preserve evidence | Serial, CT timestamp, owner decision, ticket | Audit unexplained issuance and repeated reissue clusters |

NIST specifically recommends comprehensive inventories, ownership tracking, continuous monitoring, and automation [22]. It identifies application outages caused by expired certificates as a concrete risk [22]. This supports a formal program rather than an ad hoc spreadsheet.

Cloudflare's documentation adds an operational caution: only a CA can revoke a malicious certificate [21]. Therefore, the response plan should include verified CA contacts and authorized domain-control personnel. Club members should report anomalous public records to the university security contact; they should not attempt revocation, validation, or service access themselves.

**Decision-ready insight:** CT becomes valuable when connected to ownership, CA order history, deployment evidence, and a ticketed exception process.

## Limitations, False Positives, and Counterevidence

### Exact limitation table

| Potential overclaim | Why it is unsafe | Correct statement |
|---|---|---|
| `The host is live` | CT records issuance, not present reachability [3][2] | `The name appeared in a logged certificate` |
| `This is a development server` | Only the lexical labels `testmycampus` and `testerp` are known [6] | `This is a test-labeled certificate name` |
| `Multiple CT rows mean multiple certificates` | Identical serials appeared more than once in returned data [7][8][6] | Deduplicate by serial before counting |
| `An expired certificate is still served` | `not_after` does not show deployment | `The logged certificate is expired` |
| `CN/SAN mismatch means misissuance` | Multi-name and cross-family certificates can be legitimate [6][21] | `The grouping needs ownership confirmation` |
| `Both SLCM names are the same application` | Similar public pages do not prove common origin [11][17] | `Both names display MUJ portal branding` |
| `CT monitoring catches phishing` | Lookalike domains outside the monitored name can evade alerts [21] | Combine CT with separate brand monitoring |
| `CT confirms Microsoft 365, Akamai, IIS, or ASP.NET` | Certificate names do not identify those layers | Treat them as unverified scope assumptions here |

The family-wide snapshot is also time-dependent. crt.sh may aggregate multiple logs and duplicate a certificate across entries. New certificates may appear after collection. This report therefore states the collection date and serial-deduplication method rather than presenting the data as a permanent complete inventory.

Absence is weak evidence. Failure to find a name in a query does not prove that no certificate ever existed, because query syntax, log coverage, ingestion, name normalization, and collection timing can affect results. Conversely, presence is strong evidence only for the certificate record itself.

**Decision-ready insight:** preserve uncertainty labels in tickets and dashboards. A cautious `unknown` is more useful than an unsupported `internal server` or `vulnerability` label.

## Synthesis

The MUJ SLCM evidence contains four distinct patterns that require different controls. Treating them as one generic `subdomain exposure` problem would lose the important distinctions.

### Comparative analysis

| Pattern | Direct evidence | Likely mechanism | Main trade-off | Evidence strength | Correct control |
|---|---|---|---|---|---|
| `mujslcm` exact-name history | 10 unique serials; one current; nine expired [7] | **Inference:** routine renewal plus a reissue cluster | Availability and migration flexibility versus inventory complexity | High for issuance, low for cause | Reconcile serials and standardize issuance |
| `muj.slcm` parallel name | Four serials including a current 2026 certificate; public portal branding [6][17] | **Inference:** alias, migration, or separate route | Compatibility versus naming ambiguity | High for existence, medium for relationship | Define canonical name and retirement policy |
| Test-labeled certificates | Five `testmycampus`, one `testerp`, and one `npfslcm` SAN relationship [6] | **Inference:** maintained non-production or pre-production naming | Operational convenience versus public vocabulary disclosure | High for labels, low for environment status | Confirm owners and retire unused names internally |
| Jaipur wildcard | Nine expired wildcard serials spanning 2020-2023 [6] | **Inference:** shared cloud or certificate deployment | Fewer certificates versus broader key scope | High for wildcard history, low for key distribution | Verify retirement and minimize wildcard use |
| Cross-domain CN/SAN groups | Jaipur SANs paired with Manipal Global, Dubai, base-domain, and apply-domain CNs [6] | **Inference:** centralized or cloud-managed issuance | Consolidation versus blurred ownership | High for grouping, low for organizational intent | Assign joint ownership and review SAN necessity |
| Legacy `slcm.manipal.edu` | Nine unique serials, all expired, including five with CN `sis.manipal.edu` [8] | **Inference:** historical SIS/SLCM relationship | Backward compatibility versus legacy debt | High for history, low for current architecture | Document lineage and close monitoring gaps |

Three non-obvious tensions emerge.

First, narrower exact-name certificates now coexist with historical wildcard use. **Inference:** this may indicate movement toward more service-specific issuance, but the evidence does not show a formal policy change. If that interpretation is correct, MUJ should codify it so future teams do not reintroduce broad wildcards without review.

Second, the same-day current issuance for `mujslcm` and `muj.slcm` implies coordinated management, while historical records tie those names to `dms`, `dmsmuj`, `npfslcm`, and `www` variants [7][6]. This creates a governance problem larger than certificate expiry: service identity is spread across several labels and SAN relationships.

Third, CT both helps and hurts visibility. It allows MUJ defenders to discover unmanaged names without touching hosts, but it also exposes system vocabulary to everyone. The rational response is not to avoid CT, which is core Web PKI infrastructure [2]. It is to avoid unnecessary public names, use narrowly scoped certificates and validation credentials, and continuously monitor what is logged.

The strongest strategic conclusion is therefore organizational: certificate issuance should be treated as a governed asset-lifecycle event. NIST's model of policy, inventory, continuous monitoring, ownership, and automation directly addresses the observed pattern [19][22].

## VERDICT

**Verdict: MUJ's public CT history shows a meaningful certificate-governance and naming-exposure issue, but it does not by itself demonstrate a vulnerability, unauthorized service, or compromise.**

**Confidence: High** for the certificate names, serials, validity dates, wildcard history, and current-versus-expired classifications, because those conclusions come directly from public CT records [7][8][6].

**Confidence: High** that `mujslcm.jaipur.manipal.edu` and `muj.slcm.jaipur.manipal.edu` are both current certificate-management concerns as of 2026-08-25, because each has a current CT certificate and each has publicly indexed portal content [7][6][11][17].

**Confidence: Medium** that the repeated test-labeled and SLCM-adjacent names reflect maintained systems or environments. Repeated issuance supports intentional use, but CT cannot establish deployment or operational purpose [6].

**Confidence: Medium-Low** for any explanation of the December 2024 issuance cluster, cross-domain wildcard grouping, or name migrations. Those explanations are explicitly inferences pending internal CA, DNS, CDN, and application-owner evidence.

**Priority order:**

| Priority | Defensive action | Reason |
|---:|---|---|
| 1 | Reconcile every current and historical SLCM serial with an owner and CA order | Resolves the six-certificate cluster and unknown-issuance risk |
| 2 | Decide the canonical relationship between `mujslcm` and `muj.slcm` | Both remain current and publicly represented |
| 3 | Verify retirement of wildcard, `testmycampus`, `testerp`, and `npfslcm` certificates through internal records | Reduces legacy and vocabulary exposure without unauthorized testing |
| 4 | Monitor CT continuously for the Manipal domain family | Detects new labels, issuers, and SAN groupings [21] |
| 5 | Implement NIST-style inventory, ownership, monitoring, and automation | Reduces expiry outages, unmanaged certificates, and slow incident response [22] |

Nothing in this report authorizes access to any named system. The safe club contribution is to document the public records, preserve uncertainty, and submit findings through MUJ's approved security-reporting channel.

## References

1. [
    Logs : Certificate Transparency
  ](https://certificate.transparency.dev/logs/)
2. [
Certificate Transparency (CT) Logs -  Let's Encrypt
](https://letsencrypt.org/docs/ct-logs/)
3. *What are CT Logs? | DigiCert FAQ*. https://www.digicert.com/faq/public-trust-and-certificates/what-are-ct-logs
4. [
    How CT Works : Certificate Transparency
  ](https://certificate.transparency.dev/howctworks/)
5. *RFC 9162: Certificate Transparency Version 2.0 | RFC Editor*. https://www.rfc-editor.org/rfc/rfc9162
6. *crt.sh*. https://crt.sh/?q=%25.jaipur.manipal.edu&output=json
7. *crt.sh*. https://crt.sh/?q=mujslcm.jaipur.manipal.edu&output=json
8. *crt.sh*. https://crt.sh/?q=slcm.manipal.edu&output=json
9. *Certificate Transparency search — find TLS certificates by ...*. https://ctlogs.dev/
10. *404 Not Found*. https://crt.sh/?q=testmycampus.jaipur.manipal.edu&output=json
11. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
12. *404 Not Found*. https://crt.sh/?q=npfslcm.jaipur.manipal.edu&output=json
13. *404 Not Found*. https://crt.sh/?q=muj.slcm.jaipur.manipal.edu&output=json
14. *404 Not Found*. https://crt.sh/?q=testerp.jaipur.manipal.edu&output=json
15. *Certificate Transparency Log API - Edgewatch*. https://edgewatch.com/kb/certificate-transparency-log-api
16. *RFC 6962: Certificate Transparency | RFC Editor*. http://rfc-editor.org/info/rfc6962
17. *Manipal University*. https://muj.slcm.jaipur.manipal.edu/
18. [
	MU SLcM
](https://slcm.manipal.edu/)
19. *TLS Server Certificate Management | NCCoE*. https://www.nccoe.nist.gov/tls-server-certificate-management
20. [
Challenge Types -  Let's Encrypt
](https://letsencrypt.org/docs/challenge-types/)
21. *Certificate Transparency Monitoring*. https://developers.cloudflare.com/ssl/edge-certificates/additional-options/certificate-transparency-monitoring/
22. *Executive Summary — NIST SP 1800-16  documentation*. https://www.nccoe.nist.gov/publication/1800-16/VolA/index.html
