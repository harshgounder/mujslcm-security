# Manipal Student Portal Attack Surface: Passive Public Mapping

## Executive Summary

- **Two MUJ SLCM Generations**: `mujslcm.jaipur.manipal.edu` and `muj.slcm.jaipur.manipal.edu` both resolve publicly and expose branded MUJ login experiences. The first uses `@muj.manipal.edu` and separate parent/student controls, while the second presents the MUJ Portal with `@jaipur.manipal.edu` [39][12][36]. -> Treat them as distinct production identity surfaces until their owners prove one is only a redirect or retirement candidate.
- **Shared MAHE Core**: `slcm.manipal.edu` is the shared MAHE SLcM endpoint, while `sis.manipal.edu` explicitly serves students and parents and directs users to Fee Kart for academic-fee payment [11][14]. -> Put SLCM, SIS, payment, and identity changes under one cross-campus change-control process.
- **Mixed Hosting Estate**: The student surface spans Microsoft/Azure addresses, an AWS-hosted API, National Internet Backbone/on-premises-looking addresses, Microsoft 365 mail, D2L Brightspace, and Google Sites. Shodan attributes the SLCM and both MUJ portals to IIS 10, but `api.manipal.edu` to nginx/Node.js on Amazon [2][3][5][4]. -> Assign an accountable service owner per platform rather than treating `manipal.edu` as one homogeneous stack.
- **Certificate History Is Richer Than Naming Guesses**: Jaipur CT data contains 25 unique DNS names or wildcard entries, including non-obvious `mujerp`, `mujone`, `npfslcm`, `rms`, `lcs`, `mycampus`, `testmycampus`, `dms`, `pms`, and `idp` names [1]. -> Use CT history as an asset-discovery input, but never as proof that a name still resolves.
- **Dictionary Guesses Produce Many Negatives**: Under Jaipur, the requested `lms`, `erp`, `portal`, `mail`, `wifi`, `alumni`, `fee`, `admission`, `student`, `staff`, `api`, `dev`, `test`, and `staging` labels return NXDOMAIN; several corresponding parent-domain names also do not exist [48]. -> Keep negative answers in the inventory so future monitoring can detect unexpected activation.
- **Mail Is Microsoft 365**: Both apexes publish Exchange Online Protection MX hosts, and `webmail.jaipur.manipal.edu` follows a Microsoft 365/Outlook CNAME chain [17][21][86]. -> Mail identity, SPF, and tenant-domain governance belong in the same attack-surface program as student portals.
- **Dangling Historical Aliases Need Ownership Review**: `mycampus.jaipur.manipal.edu` and `testmycampus.jaipur.manipal.edu` still return CNAMEs to `edtech366.azurewebsites.net`, but the terminal target returns NXDOMAIN in the public resolver response [68][69]. -> Validate the Azure resource relationship and remove obsolete aliases; this report does not attempt or recommend claiming the target.
- **Archive Evidence Is Uneven**: The earliest snapshots returned by the Wayback availability API are **2020-11-18** for `slcm.manipal.edu` and **2025-05-27** for `mujslcm.jaipur.manipal.edu` [23][24]. -> Treat these as earliest available responses from that API, not as proof of each application's launch date.
- **Group-Wide CT Completeness Is Not Obtainable From The Public Result Page**: crt.sh warns that the broad `manipal.edu` search is truncated to a random subset and recommends excluding expired certificates [38]. -> Do not label any broad-group list exhaustive without a successful bulk export or authorized internal certificate inventory.

## Scope, Safety, and Evidence Semantics

This is a **passive, public-source inventory dated 2026-08-25**. It uses certificate-transparency output, Google Public DNS HTTPS responses, Wayback availability and snapshots, publicly indexed Shodan host pages, and unauthenticated public web pages. It does not log in, submit credentials, bypass controls, test vulnerabilities, enumerate users, scan ports, or attempt to claim cloud resources. The useful result is therefore an externally observable control-plane map, not a penetration test.

The evidence rules matter. A CT row means a certificate containing a DNS name was logged; it does **not** prove current DNS, current ownership, or a live application. A DNS `Status: 3` is reported as NXDOMAIN. `Status: 0` without an Answer section is reported as NOERROR/NODATA, which is materially different: the name can exist in the zone while lacking the queried A/CNAME record. A CNAME ending in NXDOMAIN is called a retained or dangling alias, not a confirmed exploitable takeover. A Shodan banner is a dated third-party observation, not a new active probe by this report.

The requested `cot_explicit` cannot be satisfied as disclosure of private chain-of-thought. Instead, this report provides an auditable reasoning trace: source, observation, classification rule, uncertainty, and conclusion are visible in each table. That is enough for a reviewer to reproduce the findings without exposing hidden internal reasoning.

## Certificate Transparency: 25 Jaipur Names, With A Group-Wide Limitation

The Jaipur wildcard JSON response can be normalized into **25 unique name values**, counting the wildcard itself and `www` variants. "First seen" and "last seen" below are the minimum and maximum crt.sh `entry_timestamp` values in the retrieved result, not certificate validity bounds [1].

| CT name | First seen UTC | Last seen UTC |
|---|---:|---:|
| `jaipur.manipal.edu` | 2017-02-23 13:20:49.186 | 2026-08-16 13:06:55.341 |
| `www.jaipur.manipal.edu` | 2017-02-23 13:20:49.186 | 2026-08-16 13:06:55.341 |
| `admissions.jaipur.manipal.edu` | 2021-07-26 06:36:22.690 | 2026-07-13 00:18:48.086 |
| `mujone.jaipur.manipal.edu` | 2021-06-23 05:46:26.878 | 2026-06-24 07:35:18.804 |
| `www.mujone.jaipur.manipal.edu` | 2021-06-23 05:46:26.878 | 2026-06-24 07:35:18.804 |
| `mujerp.jaipur.manipal.edu` | 2025-04-11 07:58:55.931 | 2026-04-11 08:52:20.326 |
| `rms.jaipur.manipal.edu` | 2022-04-01 11:33:40.355 | 2026-03-27 06:08:13.628 |
| `www.rms.jaipur.manipal.edu` | 2022-04-01 11:33:40.355 | 2026-03-27 06:08:13.628 |
| `helpdesk.jaipur.manipal.edu` | 2026-01-08 09:35:53.449 | 2026-01-08 09:35:54.597 |
| `mujslcm.jaipur.manipal.edu` | 2022-11-21 09:03:23.138 | 2025-12-22 10:42:09.681 |
| `muj.slcm.jaipur.manipal.edu` | 2023-06-13 04:43:37.584 | 2025-12-22 10:41:24.012 |
| `www.muj.slcm.jaipur.manipal.edu` | 2023-06-13 04:43:37.584 | 2025-12-22 10:41:24.012 |
| `npfslcm.jaipur.manipal.edu` | 2025-03-07 12:14:29.564 | 2025-11-16 15:12:06.545 |
| `lcs.jaipur.manipal.edu` | 2024-07-22 07:30:50.858 | 2025-07-20 04:31:58.107 |
| `www.lcs.jaipur.manipal.edu` | 2024-07-22 07:30:50.858 | 2025-07-20 04:31:58.107 |
| `testmycampus.jaipur.manipal.edu` | 2023-07-07 09:31:35.375 | 2025-05-31 11:08:23.888 |
| `mycampus.jaipur.manipal.edu` | 2023-07-24 06:10:45.767 | 2025-01-29 04:20:43.391 |
| `apply.jaipur.manipal.edu` | 2017-10-23 21:49:58.872 | 2024-07-03 06:32:39.630 |
| `*.jaipur.manipal.edu` | 2021-07-03 00:03:25.808 | 2023-11-02 21:43:42.994 |
| `dmsmuj.jaipur.manipal.edu` | 2020-06-05 13:04:28.839 | 2022-08-16 10:47:49.515 |
| `www.dmsmuj.jaipur.manipal.edu` | 2022-08-16 10:47:49.515 | 2022-08-16 10:47:49.515 |
| `dms.jaipur.manipal.edu` | 2018-09-25 10:09:45.623 | 2021-10-21 05:18:55.505 |
| `www.dms.jaipur.manipal.edu` | 2018-09-25 10:09:45.623 | 2020-09-30 02:23:06.828 |
| `pms.jaipur.manipal.edu` | 2022-01-26 08:17:49.825 | 2022-01-26 08:17:50.013 |
| `idp.jaipur.manipal.edu` | 2018-10-22 09:56:30.103 | 2019-04-11 10:07:54.717 |

The key insight is lifecycle, not just count. `idp`, `dms`, `dmsmuj`, and `pms` have old or one-day CT histories; `mujerp`, `helpdesk`, `mujone`, and the apex have recent entries. The two SLCM hostnames overlap in certificate history, supporting the conclusion that MUJ has operated parallel or successive public portal names rather than a single stable label.

For `*.manipal.edu`, the public crt.sh result page explicitly says the result is truncated and that only a random subset is displayed; it recommends retrying with expired certificates excluded [38]. Because the complete set was not returned, publishing an "all group names" table would be false precision. The parent-domain analysis below therefore has two defensible parts: direct verification of every required naming convention, and confirmed student systems discovered through public pages and DNS. **Group CT completeness remains unresolved by design, not silently assumed.**

## Live DNS Control Plane: Apexes And Provider Signals

| Domain | A | AAAA | MX | TXT highlights | NS |
|---|---|---|---|---|---|
| `manipal.edu` | `18.160.46.89`, `18.160.46.123`, `18.160.46.45`, `18.160.46.127` [16] | No direct AAAA answer [105] | `0 manipal-edu.mail.protection.outlook.com` [17] | SPF authorizes Microsoft 365, Brightspace, SendGrid, Salesforce, and `167.89.84.13/32`; other strings include Microsoft, Google, and Amazon SES verification tokens [18] | `ns1-36.azure-dns.com`, `ns2-36.azure-dns.net`, `ns3-36.azure-dns.org`, `ns4-36.azure-dns.info` [19] |
| `jaipur.manipal.edu` | `3.108.105.201` [20] | No direct AAAA answer [106] | `0 jaipur-manipal-edu.mail.protection.outlook.com` [21] | SPF includes Microsoft 365, Brightspace, and SendGrid; additional strings include Microsoft and Cisco verification [22] | No child-zone NS answer; it is not separately delegated in the queried response and inherits the parent DNS control plane [107] |

The apex records reveal a split architecture. The parent uses Azure DNS for authoritative service but resolves its web apex to a multi-address edge set, while the Jaipur apex is an AWS EC2 address in `ap-south-1` [19][20][32]. Both mail routes are Microsoft 365 Exchange Online Protection [17][21]. This is why provider attribution must be record-specific: Azure NS does not mean every website is hosted in Azure, and a Microsoft MX does not mean the student application itself is Microsoft-hosted.

### Required naming-convention matrix: `manipal.edu`

| Candidate | Public resolution on 2026-08-25 | Purpose and evidence classification |
|---|---|---|
| `slcm.manipal.edu` | A `104.211.226.160` [72] | High-confidence shared MAHE SLCM; page identifies MAHE MU SLcM [11]. |
| `mujslcm.manipal.edu` | A `202.131.155.151` [73] | Resolves, but purpose is not proven by the public page evidence; likely MUJ-related by label only. |
| `lms.manipal.edu` | CNAME `learner-mahe.onlinemanipal.com` -> `manipalonline.brightspace.com`; A targets `15.134.178.12`, `13.55.178.159` [74] | High-confidence hosted LMS/D2L affinity; the public page exposes "My Home" and browser-support messaging [13]. |
| `erp.manipal.edu` | NXDOMAIN [41] | No public host at this exact label. |
| `portal.manipal.edu` | A `45.112.150.155` [75] | Generic portal name; function not established from DNS alone. |
| `mail.manipal.edu` | NOERROR/NODATA [76] | Name exists without an A/CNAME answer; apex MX, not this host, carries mail routing. |
| `webmail.manipal.edu` | A `218.248.47.16` [77] | Public webmail-labelled endpoint; application behavior was not authenticated or tested. |
| `wifi.manipal.edu` | NXDOMAIN [42] | No public host at this exact label. |
| `library.manipal.edu` | A `45.112.150.128` [78] | High-confidence Web-OPAC; page provides library selection including MIT Library and says it is maintained by Total IT [10]. |
| `alumni.manipal.edu` | A `52.74.41.140` [79] | High-confidence MAHE Alumni Association site [8]. |
| `exam.manipal.edu` | NXDOMAIN [43] | No public host at this exact label. |
| `fee.manipal.edu` | NXDOMAIN [44] | No standalone label; SIS says fee payment is reached through Fee Kart after portal login [14]. |
| `admission.manipal.edu` | NXDOMAIN [45] | Singular label absent; other admission/apply names exist. |
| `student.manipal.edu` | NXDOMAIN [46] | No public host at this exact label. |
| `staff.manipal.edu` | NXDOMAIN [47] | No public host at this exact label. |
| `api.manipal.edu` | A `43.205.223.7` [80] | Public API root returns an opaque JSON `data` field [7]; Shodan sees AWS, nginx, Node.js, and Express [4]. |
| `dev.manipal.edu` | A `4.247.242.9` [81] | Publicly resolves to Microsoft space [30], but the fetched page presents ordinary MAHE public-site navigation and Apply Now rather than a developer console [15]. |
| `test.manipal.edu` | NOERROR/NODATA [82] | Name exists but no A/CNAME answer in the query. |
| `uat.manipal.edu` | CNAME through `uat-ci-mahe-ep-bzgfhcehh0fvhafs.a01.azurefd.net` and `mr-a01.tm-azurefd.net` to `150.171.110.195` [83] | Public UAT-labelled Azure Front Door route; existence is confirmed, application purpose beyond the label is not. |
| `staging.manipal.edu` | NXDOMAIN [48] | No public host at this exact label. |

### Required naming-convention matrix: `jaipur.manipal.edu`

| Candidate | Public resolution on 2026-08-25 | Purpose and evidence classification |
|---|---|---|
| `slcm.jaipur.manipal.edu` | NOERROR/NODATA [84] | Exact guessed host has no A/CNAME; MUJ uses other SLCM names. |
| `mujslcm.jaipur.manipal.edu` | A `98.70.14.50` [85] | Confirmed MUJ portal with parent/student login and forgot-password control [36]. |
| `lms.jaipur.manipal.edu` | NXDOMAIN [49] | No exact host; MUJ Online public material describes a D2L LMS instead [35]. |
| `erp.jaipur.manipal.edu` | NXDOMAIN [50] | No exact host; CT instead reveals `mujerp`. |
| `portal.jaipur.manipal.edu` | NXDOMAIN [51] | No exact host; portal function is on SLCM-labelled hosts. |
| `mail.jaipur.manipal.edu` | NXDOMAIN [52] | No exact host. |
| `webmail.jaipur.manipal.edu` | CNAME chain through `mail.office365.com`, `outlook.office365.com`, and Microsoft cloud names to Outlook addresses [86] | High-confidence Microsoft 365 webmail alias. |
| `wifi.jaipur.manipal.edu` | NXDOMAIN [53] | No public host at this exact label. |
| `library.jaipur.manipal.edu` | CNAME `sites.google.com` with Google A answers [87] | Public Google Sites affinity; content purpose is inferred from the label, not authenticated. |
| `alumni.jaipur.manipal.edu` | NXDOMAIN [54] | No exact campus-specific alumni host. |
| `exam.jaipur.manipal.edu` | A `59.91.192.229` [88] | Public exam-labelled host on National Internet Backbone address space [33]; application purpose not probed. |
| `fee.jaipur.manipal.edu` | NXDOMAIN [55] | No public host at this exact label. |
| `admission.jaipur.manipal.edu` | NXDOMAIN [56] | Singular label absent; CT contains plural `admissions`. |
| `student.jaipur.manipal.edu` | NXDOMAIN [57] | No public host at this exact label. |
| `staff.jaipur.manipal.edu` | NXDOMAIN [58] | No public host at this exact label. |
| `api.jaipur.manipal.edu` | NXDOMAIN [59] | No campus API at this exact label. |
| `dev.jaipur.manipal.edu` | NXDOMAIN [60] | No public host at this exact label. |
| `test.jaipur.manipal.edu` | NXDOMAIN [61] | No public host at this exact label. |
| `uat.jaipur.manipal.edu` | A `103.139.159.141` [89] | Public UAT-labelled host in Seans Media address space [34]; no claim is made about application state. |
| `staging.jaipur.manipal.edu` | NXDOMAIN [62] | No public host at this exact label. |

The two matrices show why dictionary enumeration is only one layer. Exact `erp.jaipur...` and `portal.jaipur...` guesses fail, yet CT exposes `mujerp` and two SLCM portal names. Conversely, a DNS answer for `dev` or `uat` proves reachability but not sensitive content. The appropriate governance action is ownership validation, not an automatic vulnerability label.

## Current DNS State Of Every Jaipur CT Name

The table below closes the loop between historical certificate evidence and current public resolution. The wildcard certificate name is omitted because `*.jaipur.manipal.edu` is a certificate pattern, not a literal DNS hostname.

| CT-derived name | Current A/CNAME result |
|---|---|
| `jaipur.manipal.edu` | NOERROR/NODATA (name exists but no A/CNAME answer) [20] |
| `www.jaipur.manipal.edu` | NOERROR/NODATA (name exists but no A/CNAME answer) [93] |
| `admissions.jaipur.manipal.edu` | NOERROR/NODATA (name exists but no A/CNAME answer) [94] |
| `mujone.jaipur.manipal.edu` | NOERROR/NODATA (name exists but no A/CNAME answer) [95] |
| `www.mujone.jaipur.manipal.edu` | NOERROR/NODATA (name exists but no A/CNAME answer) [63] |
| `mujerp.jaipur.manipal.edu` | NOERROR/NODATA (name exists but no A/CNAME answer) [96] |
| `rms.jaipur.manipal.edu` | NOERROR/NODATA (name exists but no A/CNAME answer) [97] |
| `www.rms.jaipur.manipal.edu` | NOERROR/NODATA (name exists but no A/CNAME answer) [64] |
| `helpdesk.jaipur.manipal.edu` | NOERROR/NODATA (name exists but no A/CNAME answer) [65] |
| `mujslcm.jaipur.manipal.edu` | NOERROR/NODATA (name exists but no A/CNAME answer) [85] |
| `muj.slcm.jaipur.manipal.edu` | NOERROR/NODATA (name exists but no A/CNAME answer) [90] |
| `www.muj.slcm.jaipur.manipal.edu` | NOERROR/NODATA (name exists but no A/CNAME answer) [66] |
| `npfslcm.jaipur.manipal.edu` | NOERROR/NODATA (name exists but no A/CNAME answer) [98] |
| `lcs.jaipur.manipal.edu` | NOERROR/NODATA (name exists but no A/CNAME answer) [99] |
| `www.lcs.jaipur.manipal.edu` | NOERROR/NODATA (name exists but no A/CNAME answer) [67] |
| `testmycampus.jaipur.manipal.edu` | NOERROR/NODATA (name exists but no A/CNAME answer) [68] |
| `mycampus.jaipur.manipal.edu` | NOERROR/NODATA (name exists but no A/CNAME answer) [69] |
| `apply.jaipur.manipal.edu` | NOERROR/NODATA (name exists but no A/CNAME answer) [100] |
| `dmsmuj.jaipur.manipal.edu` | NOERROR/NODATA (name exists but no A/CNAME answer) [101] |
| `www.dmsmuj.jaipur.manipal.edu` | NOERROR/NODATA (name exists but no A/CNAME answer) [70] |
| `dms.jaipur.manipal.edu` | NOERROR/NODATA (name exists but no A/CNAME answer) [102] |
| `www.dms.jaipur.manipal.edu` | NOERROR/NODATA (name exists but no A/CNAME answer) [71] |
| `pms.jaipur.manipal.edu` | NOERROR/NODATA (name exists but no A/CNAME answer) [103] |
| `idp.jaipur.manipal.edu` | NOERROR/NODATA (name exists but no A/CNAME answer) [104] |

The most important lifecycle signal is the pair of Azure Website aliases: both `mycampus` and `testmycampus` retain CNAME data even though the terminal target is NXDOMAIN [68][69]. Several `www` variants and the newly logged `helpdesk` name are NXDOMAIN despite their CT history [63][64][65][66][67]. This demonstrates the central rule: **CT is historical inventory; DNS is current routing state.**

## Student Portal Inventory: Purpose, Technology, And Footprint

| System | Student-facing purpose | Public technology or routing evidence | Confidence and exposure |
|---|---|---|---|
| `slcm.manipal.edu` | Shared MAHE student lifecycle management portal | A `104.211.226.160`; Shodan ties the hostname to Microsoft AS8075, ports 80/443, IIS 10, and ASP.NET headers [72][2] | **High**. Public login surface; no authenticated functions tested. |
| `sis.manipal.edu` | Student/parent information and academic fee workflow | A `218.248.47.25` [91]; page explicitly limits service to bona fide MAHE students/parents and points to Fee Kart [14] | **High**. Public landing/login workflow with payment linkage. |
| `mujslcm.jaipur.manipal.edu` | MUJ parent and student sign-in | A `98.70.14.50`; visible `@muj.manipal.edu`, parent/student login, and Forgot Password [85][36] | **High**. Azure/Microsoft address; IIS 10 and ASP.NET MVC banners [27][3]. |
| `muj.slcm.jaipur.manipal.edu` | Alternate MUJ Portal sign-in | A `20.244.94.89`; visible MUJ Portal, Sign In, `@jaipur.manipal.edu` [90][12] | **High**. Microsoft address; IIS 10, Windows Server, jQuery 1.10.2, ASP.NET 4.0.30319 [28][5]. |
| `lms.manipal.edu` | Hosted learning-management entry point | Brightspace CNAME chain [74]; public page presents "My Home" and browser requirements [13] | **High** for LMS affinity, **medium** for exact campus population. |
| `hms.manipal.edu` | Publicly named MAHE system endpoint | A `20.44.49.205` [92] | **Medium**. Microsoft-hosted routing is confirmed [31], but the acronym's business meaning is not asserted without stronger first-party text. |
| `webmail.jaipur.manipal.edu` | Campus webmail redirect/alias | Multi-hop Microsoft 365/Outlook CNAME chain [86] | **High** provider affinity. No mailbox or tenant tests performed. |
| `library.manipal.edu` | Cross-campus Web-OPAC and library selection | A `45.112.150.128` [78]; page lists MIT and other libraries and Total IT maintenance [10] | **High**. Public catalog/login surface. |
| `library.jaipur.manipal.edu` | Jaipur-labelled library page | Google Sites CNAME/A chain [87] | **Medium**. Routing is certain, business purpose is label-based. |
| `alumni.manipal.edu` | MAHE alumni association | A `52.74.41.140` [79]; page title confirms association [8] | **High**. Student-adjacent rather than active-student core. |
| `exam.jaipur.manipal.edu` | Exam-labelled campus endpoint | A `59.91.192.229` [88], National Internet Backbone [33] | **Medium**. Name and reachability confirmed; functions not tested. |
| `mujerp.jaipur.manipal.edu` | ERP-labelled MUJ service | CT history begins 2025; current A `20.244.0.229` [1][96] | **Medium**. Purpose is a strong naming inference, not page-confirmed. |
| `mujone.jaipur.manipal.edu` | Branded MUJ service | CT history and current DNS are confirmed [1][95] | **Low to medium** for purpose. Do not expand "One" into an unstated product function. |
| `rms.jaipur.manipal.edu` | Acronym-labelled service | Current A `202.131.155.153` [97] | **Low** for purpose, **high** for public DNS. |
| `api.manipal.edu` | Public application API endpoint | AWS EC2 `ap-south-1`, nginx, Node.js, Express; root emits opaque JSON [7][29][4] | **High** technology affinity, **medium** application-scope attribution. |
| `uat.manipal.edu` / `uat.jaipur.manipal.edu` | Non-production-labelled routes | Azure Front Door CNAME for group UAT; direct A in Seans Media space for Jaipur [83][89][34] | **High** reachability, **low** business-content certainty. |

A particularly useful contrast is SLCM versus SIS. SIS self-describes its audience and fee workflow, so its purpose is direct evidence [14]. SLCM's purpose is supported by its MAHE branding and repeated student-login naming, but technical banners reveal its stack, not its authorization boundaries. This distinction prevents a common analytical error: inferring data exposure merely because an authentication page and technology banner are public.

## Archive Evolution: What Can And Cannot Be Established

| Host | Earliest snapshot returned by availability API | Historical structure observed | Defensible change conclusion |
|---|---:|---|---|
| `slcm.manipal.edu` | 2020-11-18 06:05:11 UTC [23] | Archived page material retains MAHE copyright/identity; sampled markup contained ASP.NET state/event fields and login-related controls. Current public evidence still identifies MAHE MU SLcM [11]. | A long-lived MAHE-branded SLCM login is supported. No specific removed feature can be proven from the sampled public extracts. |
| `mujslcm.jaipur.manipal.edu` | 2025-05-27 04:40:58 UTC [24] | Archived/current indexed structures show "WELCOME TO MUJ PORTAL," `@muj.manipal.edu`, Parent Login, Student Login, and Forgot Password [39][36]. | The separate parent/student model is visible. The evidence does not support claiming that a feature was removed; extraction differences are not product-change evidence. |

These dates are deliberately phrased as "earliest returned by the availability API." A failed or incomplete CDX enumeration can miss older captures, and an archive's first capture is not a launch date. Likewise, HTML extraction can omit script-generated or image-only controls. The report therefore rejects two tempting but unsupported claims: that SLCM launched in 2020, and that MUJ removed a login feature between snapshots.

The historical value lies instead in continuity. The parent SLCM carries a 2017 MAHE copyright identity in current indexed content [11], while the MUJ host carries explicit campus identity and separate user classes [36]. This suggests distinct application families or branded deployments, a conclusion reinforced by the different DNS addresses and Shodan hostname observations.

## IIS, ASP.NET, Cloud, And On-Premises Affinity

| Observed endpoint | Network/provider evidence | Public banner evidence | Interpretation |
|---|---|---|---|
| `slcm.manipal.edu` / `104.211.226.160` | Microsoft Corporation, AS8075; observed 2026-08-23 [2] | Ports 80/443; Microsoft HTTPAPI 2.0 and IIS 10; response includes IIS 10 and ASP.NET version headers [2] | Azure-addressed legacy Microsoft web stack. |
| `mujslcm.jaipur.manipal.edu` / `98.70.14.50` | Microsoft AS8075; observed 2026-08-22 [3] | Port 443, IIS 10, ASP.NET MVC 5.3 and ASP.NET headers [3] | Azure-hosted MUJ portal, Microsoft application stack. |
| `muj.slcm.jaipur.manipal.edu` / `20.244.94.89` | Microsoft AS8075; observed 2026-08-18 [5] | Port 443, IIS 10, Windows Server, ASP.NET 4.0.30319, jQuery 1.10.2 [5] | Separate Azure-addressed MUJ portal with similar but independently exposed stack. |
| `sis.manipal.edu` / `218.248.47.25` | MAHE organization on AS9829/National Internet Backbone; observed 2026-08-25 [6] | Ports 80, 443, 4444, 8443; IIS 10 and ASP.NET 4.0.30319 on observed services [6] | Institution-linked or on-premises/leased-line-looking Microsoft estate. Public banners do not prove physical location. |
| `api.manipal.edu` / `43.205.223.7` | Amazon AS16509, EC2 hostname in `ap-south-1`; observed 2026-08-23 [4] | Ports 80/443; Ubuntu, Node.js, Express, nginx 1.18.0 [4] | Modern Linux/API stack, technically distinct from SLCM/SIS. |

The technology affinity is strong because DNS, provider data, hostname observations, and banners converge. It is not a vulnerability assessment. Version strings can be stale, proxied, or deliberately altered. The actionable finding is architectural heterogeneity: IIS/ASP.NET applications, a Linux/Node API, Microsoft 365, D2L, Google Sites, Azure Front Door, and AWS all require different patching, logging, identity, and decommissioning owners.

Public Censys target pages did not yield comparable host details without an authenticated interface, so this report does not manufacture Censys evidence. Shodan's publicly indexed pages are used with their "Last Seen" dates to make the observation window explicit.

## Sister-Campus Parallels: Dubai, Sikkim, And MIT Manipal

| Campus/entity | Confirmed public system | Relationship to the scoped domains | What the parallel reveals |
|---|---|---|---|
| Manipal Dubai | Official campus page identifies it as a MAHE branch and links `https://slcm.manipaldubai.com/` as "Student Portal" [40] | Outside `manipal.edu`, under `manipaldubai.com` | The SLCM naming pattern is group-wide conceptually, but campus DNS can be separately branded and delegated. |
| Sikkim Manipal University | Official Online Manipal page identifies Sikkim Manipal University and online BA/MA offerings [37] | Public student functions appear under separate SMU/Online Manipal domains; no Sikkim-specific `*.manipal.edu` student host was verified in this pass | Do not force sister campuses into the parent suffix. Brand affiliation is not DNS inheritance. |
| MIT Manipal | `slcm.manipal.edu` identifies MAHE MU SLcM [11]; `library.manipal.edu` explicitly offers "Manipal Institute of Technology Library" among its choices [10] | Shared `manipal.edu` systems rather than a proven `mit.*` portal in this evidence set | MIT's public footprint is consistent with shared MAHE services; an MIT-specific SLCM hostname should not be invented without evidence. |
| MUJ | Two campus SLCM hosts plus MUJ ERP/One/other CT names [1][85][90] | Nested under `jaipur.manipal.edu` | MUJ exposes a more campus-specific naming layer than the shared MAHE/MIT pattern. |

The comparison shows three operating models. Dubai uses a campus-branded external domain and still calls the service SLCM. MIT appears in shared MAHE service catalogs and uses the group SLcM identity. MUJ uses nested campus DNS and multiple branded portals. Sikkim's visible online presence uses distinct domains rather than an evidenced `manipal.edu` subdomain. Therefore, sister-campus discovery must combine brand research with DNS suffix research; a single wildcard query cannot represent the whole organization.

## Synthesis: Identity, Hosting, Lifecycle, And Evidence Trade-Offs

Across **mechanism**, the portals divide into four families. First, MAHE/MUJ transactional systems use IIS/ASP.NET on Microsoft or institution-linked networks. Second, learning uses a managed D2L/Brightspace CNAME chain. Third, communications use Microsoft 365. Fourth, newer web/API functions use AWS, nginx, Node.js, Azure Front Door, or Google Sites. This mixture explains why no one provider signal can stand in for the whole attack surface.

Across **scope**, `slcm.manipal.edu` and SIS are shared group services, while `mujslcm` and `muj.slcm` are campus-specific. Dubai demonstrates an external campus domain, Sikkim demonstrates separate brand domains, and MIT appears in shared service content rather than a verified dedicated hostname. The scope implication is practical: a certificate inventory limited to `*.manipal.edu` will miss externally branded sister-campus portals, while a Jaipur-only inventory will miss shared SLCM, SIS, LMS, mail, and library dependencies.

Across **lifecycle**, CT and DNS tell different stories. Recent certificates for `mujerp` and `helpdesk` suggest recent naming activity, but `helpdesk` is currently NXDOMAIN. Old CT names such as `idp` and `dms` can still resolve, while some `www` aliases do not. `mycampus` and `testmycampus` retain CNAMEs whose terminal Azure target is NXDOMAIN [68][69]. The operational recommendation is a three-way state model: **historical-only**, **DNS-live**, and **application-confirmed**. Collapsing those into a binary "exists/does not exist" field loses the most important lifecycle information.

Across **trade-offs**, public naming helps students discover services but enlarges observable identity and platform metadata. Generic labels such as `api`, `dev`, and `uat` are easy to enumerate; non-obvious names such as `mujerp` are exposed by CT. Hiding names is not a security boundary, so the better controls are consistent authentication, minimal banners, hardened recovery flows, strict owner records, centralized certificate issuance, and prompt DNS retirement. None of those recommendations depends on attempting access.

Across the **evidence base**, DNS has the highest confidence for current routing, first-party page text has the highest confidence for purpose, CT has the highest value for historical discovery, Wayback has value for continuity but weak launch-date inference, and Shodan has value for dated technology affinity but cannot establish vulnerability. The strongest findings in this report are those where at least two layers converge: MUJ portal page plus DNS plus IIS banner; SIS page plus DNS plus institution-linked network; API DNS plus AWS hostname plus nginx/Node banner.

A prioritized defensive sequence follows from that synthesis:

1. Reconcile `slcm`, `sis`, `mujslcm`, `muj.slcm`, `mujerp`, `mujone`, and `npfslcm` to named business and technical owners.
2. Validate and remove obsolete DNS, starting with terminal-NXDOMAIN Azure aliases and historical `www` names.
3. Decide whether both MUJ login generations remain required; if so, document their user populations and recovery ownership.
4. Reduce unnecessary platform/version headers across IIS and nginx estates without treating suppression as a substitute for patching.
5. Bring Microsoft 365 aliases, SPF sources, LMS vendor routing, and payment links into the same third-party dependency register.
6. Monitor CT and DNS state transitions separately so that certificate issuance, host activation, and retirement each generate distinct review events.

## VERDICT

**Verdict: The publicly visible Manipal student-system surface is real, diverse, and only partly centralized.** The high-confidence core is shared MAHE SLCM/SIS/LMS/mail/library plus two live MUJ SLCM portals. The technology estate spans Azure/Microsoft IIS and ASP.NET, MAHE/National Internet Backbone addresses, AWS nginx/Node, Microsoft 365, D2L Brightspace, Azure Front Door, and Google Sites. The highest-priority hygiene issue visible from passive data is lifecycle governance: parallel portal names, old CT entries, current NXDOMAINs, and two CNAMEs ending at an NXDOMAIN Azure target.

**Confidence by claim class:**

| Claim class | Confidence | Reason |
|---|---:|---|
| Current A/CNAME existence and requested-name negatives | **High, 0.95** | Direct public DNS responses, with NXDOMAIN separated from NODATA. |
| Jaipur CT names and first/last timestamps | **High, 0.95** | Complete normalized response returned for the scoped Jaipur wildcard query [1]. |
| Portal purpose for SIS, MUJ SLCM, LMS, library, alumni | **High, 0.90** | First-party or public landing-page text aligns with DNS. |
| IIS/AWS/provider affinity | **High, 0.90** | DNS, provider attribution, and dated Shodan banners converge. |
| Wayback "first capture" | **Medium, 0.70** | It is the earliest snapshot returned by the availability API, not a guaranteed corpus-wide first or launch date. |
| Purpose of acronym-only names (`rms`, `lcs`, `pms`, `idp`) | **Low, 0.35** | Names and routing exist, but expansions were not verified; the report intentionally does not guess. |
| Exhaustive `*.manipal.edu` CT inventory | **Not achieved, 0.20** | crt.sh publicly truncates the broad result to a random subset [38]. |
| Overall live student-surface map | **High, 0.88** | Required naming candidates, major confirmed portals, DNS control plane, archives, and technology evidence are covered; group-wide historical CT completeness remains the explicit exception. |

## References

1. *crt.sh*. https://crt.sh/?q=%25.jaipur.manipal.edu&output=json
2.(https://www.shodan.io/host/104.211.226.160)
3.(https://www.shodan.io/host/98.70.14.50)
4.(https://www.shodan.io/host/43.205.223.7)
5.(https://www.shodan.io/host/20.244.94.89)
6.(https://www.shodan.io/host/218.248.47.25)
7. *api.manipal.edu*. https://api.manipal.edu/
8. *MAHE ALUMNI ASSOCIATION*. https://alumni.manipal.edu/
9. *Manipal University Jaipur*. https://mycampus.jaipur.manipal.edu/
10. *MAHE WEB - OPAC*. https://library.manipal.edu/
11. [
	MU SLcM
](https://slcm.manipal.edu/)
12. *Manipal University*. https://muj.slcm.jaipur.manipal.edu/
13. *Unsupported Browser*. https://lms.manipal.edu/
14. [
	SIS
](https://sis.manipal.edu/studlogin.aspx)
15. *Top Higher Education Institution in India |Manipal University (MAHE)*. https://dev.manipal.edu/
16. *dns.google*. https://dns.google/resolve?name=manipal.edu&type=A
17. *dns.google*. https://dns.google/resolve?name=manipal.edu&type=MX
18. *dns.google*. https://dns.google/resolve?name=manipal.edu&type=TXT
19. *dns.google*. https://dns.google/resolve?name=manipal.edu&type=NS
20. *dns.google*. https://dns.google/resolve?name=jaipur.manipal.edu&type=A
21. *dns.google*. https://dns.google/resolve?name=jaipur.manipal.edu&type=MX
22. *dns.google*. https://dns.google/resolve?name=jaipur.manipal.edu&type=TXT
23. *archive.org*. https://archive.org/wayback/available?url=slcm.manipal.edu&timestamp=20201118000000
24. *archive.org*. https://archive.org/wayback/available?url=mujslcm.jaipur.manipal.edu&timestamp=20250528000000
25. *ipinfo.io*. https://ipinfo.io/104.211.226.160/json
26. *ipinfo.io*. https://ipinfo.io/218.248.47.25/json
27. *ipinfo.io*. https://ipinfo.io/98.70.14.50/json
28. *ipinfo.io*. https://ipinfo.io/20.244.94.89/json
29. *ipinfo.io*. https://ipinfo.io/43.205.223.7/json
30. *ipinfo.io*. https://ipinfo.io/4.247.242.9/json
31. *ipinfo.io*. https://ipinfo.io/20.44.49.205/json
32. *ipinfo.io*. https://ipinfo.io/3.108.105.201/json
33. *ipinfo.io*. https://ipinfo.io/59.91.192.229/json
34. *ipinfo.io*. https://ipinfo.io/103.139.159.141/json
35. *Manipal University Jaipur (Online) - D2L*. http://d2l.com/en-in/why-d2l/customers/manipal-university-jaipur-online
36. *muj portal - Manipal University*. https://mujslcm.jaipur.manipal.edu/
37. *Sikkim Manipal University | Online Manipal: Online Degree ...*. https://smu.onlinemanipal.com/
38. *crt.sh | %.manipal.edu*. https://crt.sh/?q=%25.manipal.edu
39. *Manipal University - mujslcm.jaipur.manipal.edu*. https://mujslcm.jaipur.manipal.edu/Home/Index
40. *About Manipal Dubai | MoHESR Licensed & CAA Accredited*. http://manipaldubai.com/about-us
41. *dns.google*. https://dns.google/resolve?name=erp.manipal.edu&type=A
42. *dns.google*. https://dns.google/resolve?name=wifi.manipal.edu&type=A
43. *dns.google*. https://dns.google/resolve?name=exam.manipal.edu&type=A
44. *dns.google*. https://dns.google/resolve?name=fee.manipal.edu&type=A
45. *dns.google*. https://dns.google/resolve?name=admission.manipal.edu&type=A
46. *dns.google*. https://dns.google/resolve?name=student.manipal.edu&type=A
47. *dns.google*. https://dns.google/resolve?name=staff.manipal.edu&type=A
48. *dns.google*. https://dns.google/resolve?name=staging.manipal.edu&type=A
49. *dns.google*. https://dns.google/resolve?name=lms.jaipur.manipal.edu&type=A
50. *dns.google*. https://dns.google/resolve?name=erp.jaipur.manipal.edu&type=A
51. *dns.google*. https://dns.google/resolve?name=portal.jaipur.manipal.edu&type=A
52. *dns.google*. https://dns.google/resolve?name=mail.jaipur.manipal.edu&type=A
53. *dns.google*. https://dns.google/resolve?name=wifi.jaipur.manipal.edu&type=A
54. *dns.google*. https://dns.google/resolve?name=alumni.jaipur.manipal.edu&type=A
55. *dns.google*. https://dns.google/resolve?name=fee.jaipur.manipal.edu&type=A
56. *dns.google*. https://dns.google/resolve?name=admission.jaipur.manipal.edu&type=A
57. *dns.google*. https://dns.google/resolve?name=student.jaipur.manipal.edu&type=A
58. *dns.google*. https://dns.google/resolve?name=staff.jaipur.manipal.edu&type=A
59. *dns.google*. https://dns.google/resolve?name=api.jaipur.manipal.edu&type=A
60. *dns.google*. https://dns.google/resolve?name=dev.jaipur.manipal.edu&type=A
61. *dns.google*. https://dns.google/resolve?name=test.jaipur.manipal.edu&type=A
62. *dns.google*. https://dns.google/resolve?name=staging.jaipur.manipal.edu&type=A
63. *dns.google*. https://dns.google/resolve?name=www.mujone.jaipur.manipal.edu&type=A
64. *dns.google*. https://dns.google/resolve?name=www.rms.jaipur.manipal.edu&type=A
65. *dns.google*. https://dns.google/resolve?name=helpdesk.jaipur.manipal.edu&type=A
66. *dns.google*. https://dns.google/resolve?name=www.muj.slcm.jaipur.manipal.edu&type=A
67. *dns.google*. https://dns.google/resolve?name=www.lcs.jaipur.manipal.edu&type=A
68. *dns.google*. https://dns.google/resolve?name=testmycampus.jaipur.manipal.edu&type=A
69. *dns.google*. https://dns.google/resolve?name=mycampus.jaipur.manipal.edu&type=A
70. *dns.google*. https://dns.google/resolve?name=www.dmsmuj.jaipur.manipal.edu&type=A
71. *dns.google*. https://dns.google/resolve?name=www.dms.jaipur.manipal.edu&type=A
72. *dns.google*. https://dns.google/resolve?name=slcm.manipal.edu&type=A
73. *dns.google*. https://dns.google/resolve?name=mujslcm.manipal.edu&type=A
74. *dns.google*. https://dns.google/resolve?name=lms.manipal.edu&type=A
75. *dns.google*. https://dns.google/resolve?name=portal.manipal.edu&type=A
76. *dns.google*. https://dns.google/resolve?name=mail.manipal.edu&type=A
77. *dns.google*. https://dns.google/resolve?name=webmail.manipal.edu&type=A
78. *dns.google*. https://dns.google/resolve?name=library.manipal.edu&type=A
79. *dns.google*. https://dns.google/resolve?name=alumni.manipal.edu&type=A
80. *dns.google*. https://dns.google/resolve?name=api.manipal.edu&type=A
81. *dns.google*. https://dns.google/resolve?name=dev.manipal.edu&type=A
82. *dns.google*. https://dns.google/resolve?name=test.manipal.edu&type=A
83. *dns.google*. https://dns.google/resolve?name=uat.manipal.edu&type=A
84. *dns.google*. https://dns.google/resolve?name=slcm.jaipur.manipal.edu&type=A
85. *dns.google*. https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=A
86. *dns.google*. https://dns.google/resolve?name=webmail.jaipur.manipal.edu&type=A
87. *dns.google*. https://dns.google/resolve?name=library.jaipur.manipal.edu&type=A
88. *dns.google*. https://dns.google/resolve?name=exam.jaipur.manipal.edu&type=A
89. *dns.google*. https://dns.google/resolve?name=uat.jaipur.manipal.edu&type=A
90. *dns.google*. https://dns.google/resolve?name=muj.slcm.jaipur.manipal.edu&type=A
91. *dns.google*. https://dns.google/resolve?name=sis.manipal.edu&type=A
92. *dns.google*. https://dns.google/resolve?name=hms.manipal.edu&type=A
93. *dns.google*. https://dns.google/resolve?name=www.jaipur.manipal.edu&type=A
94. *dns.google*. https://dns.google/resolve?name=admissions.jaipur.manipal.edu&type=A
95. *dns.google*. https://dns.google/resolve?name=mujone.jaipur.manipal.edu&type=A
96. *dns.google*. https://dns.google/resolve?name=mujerp.jaipur.manipal.edu&type=A
97. *dns.google*. https://dns.google/resolve?name=rms.jaipur.manipal.edu&type=A
98. *dns.google*. https://dns.google/resolve?name=npfslcm.jaipur.manipal.edu&type=A
99. *dns.google*. https://dns.google/resolve?name=lcs.jaipur.manipal.edu&type=A
100. *dns.google*. https://dns.google/resolve?name=apply.jaipur.manipal.edu&type=A
101. *dns.google*. https://dns.google/resolve?name=dmsmuj.jaipur.manipal.edu&type=A
102. *dns.google*. https://dns.google/resolve?name=dms.jaipur.manipal.edu&type=A
103. *dns.google*. https://dns.google/resolve?name=pms.jaipur.manipal.edu&type=A
104. *dns.google*. https://dns.google/resolve?name=idp.jaipur.manipal.edu&type=A
105. *dns.google*. https://dns.google/resolve?name=manipal.edu&type=AAAA
106. *dns.google*. https://dns.google/resolve?name=jaipur.manipal.edu&type=AAAA
107. *dns.google*. https://dns.google/resolve?name=jaipur.manipal.edu&type=NS
