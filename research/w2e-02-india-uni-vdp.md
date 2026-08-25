# India's Thin University VDP Landscape: Lessons for MUJ

## Executive Summary

- **Verified University Program**: This survey found one clear, first-party, campus-wide Indian academic vulnerability disclosure program: the Indian Institute of Science Responsible Vulnerability Disclosure Policy. It covers `*.iisc.ac.in`, public-facing APIs, and IISc mobile applications, but it excludes third-party services and several intrusive testing categories [3]. -> MUJ should use this as the most relevant Indian university benchmark.

- **Student Portal Coverage**: IISc does not expressly name an ERP, learning-management system, or student portal. A first-party portal below `iisc.ac.in` appears covered at the domain level, but that is an **inference**, not explicit portal authorization [3]. -> Researchers should obtain written confirmation before testing any authenticated student system, even where a wildcard appears broad.

- **No Cash Bounty At IISc**: IISc expressly says that it does not currently offer monetary rewards. It may provide website acknowledgment or credit, at its discretion, for a valid report [3]. -> A university club should separate the goal of safe disclosure from any expectation of payment.

- **Directory Is Not Authorization**: HackerOne pages for Amrita University and IIT Madras are marked as external, community-moderated entries. Both say that there are no known reporting guidelines, that HackerOne has not validated the information, and that the pages are not affiliated with the universities [15][16]. -> Never interpret a HackerOne Directory result as permission to test.

- **Competition Is Not Production Scope**: SRM University Delhi-NCR, Sonepat listed an offline "Bug Bounty" competition in which teams submit reports and proofs of concept. The listing does not identify an authorized target or say that any SRM production domain, ERP, or student portal is in scope [7]. -> Authorization for a controlled event cannot be transferred to ordinary university systems.

- **CERT-In Coordinates; It Does Not Pre-Authorize**: CERT-In accepts reports about newly identified vulnerabilities, validates them, coordinates with vendors and stakeholders, and may publish a note or advisory. Its policy gives no safe harbor and says reporters remain responsible for compliance with applicable law [1]. -> CERT-In is an escalation and coordination route after a vulnerability is encountered lawfully, not blanket permission to investigate a campus.

- **MUJ Has A Public Disclosure Gap**: The public request to `https://mujslcm.jaipur.manipal.edu/.well-known/security.txt` returned the MUJ Portal sign-in page rather than an RFC 9116 file [10]. MUJ's public contact page lists `it.support@jaipur.manipal.edu` for IT Infrastructure, but it does not label that address as a VDP, CISO, SOC, or bug-bounty channel [13]. -> The club should request a written scope and reporting process from IT Infrastructure before undertaking any security testing.

- **Hacktivity Is Evidence, Not Scope**: HackerOne describes Hacktivity as a dynamic repository of security vulnerabilities, with searchable report and reward metadata [6]. -> Use it to study disclosure outcomes, but obtain authorization only from the relevant owner's current program policy.

- **Best Immediate MUJ Action**: The safest deliverable is not an unsolicited test plan. It is a proposed MUJ VDP modeled on IISc: an official policy URL, `security.txt`, named first-party assets, explicit portal status, prohibited techniques, a secure channel, response targets, coordinated-disclosure rules, and a good-faith assurance.

## 1. Scope, Safety Boundary, and Auditable Decision Rationale

This report surveys public evidence available as of **August 25, 2026**. It covers first-party university policies, platform pages, CERT-In material, and clearly labeled adjacent initiatives. It does not authorize access to any system and does not recommend scanning, exploitation, account attacks, bypassing access controls, accessing another person's record, testing Microsoft 365, or attempting to evade Akamai.

The stack description in the question - ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10 behind Akamai, and Microsoft 365 identity - is treated as **user-supplied context, not independently verified fact**. Even a correct technology identification would not create authorization. Version banners, framework names, public DNS records, or a platform directory entry are not substitutes for an asset owner's written scope.

The request asked for explicit chain-of-thought. I cannot provide private hidden reasoning or a token-by-token internal deliberation. I can provide the following auditable decision logic, which exposes the evidence standard and conclusions without revealing hidden chain-of-thought.

| Decision question | Evidence required | Classification rule | Safety consequence |
|---|---|---|---|
| Is this a university VDP? | First-party policy inviting inbound reports about university-owned assets | Count as verified only if owner, scope, channel, and rules are identifiable | A VDP permits reporting under its terms; it does not necessarily permit every testing method |
| Is this a bug bounty? | First-party or owner-authorized platform page promising rewards for qualifying reports | Do not call recognition, a competition prize, or possible vendor payment a bounty | Never promise a researcher money unless the program does |
| Is a student portal covered? | The portal is named, or a first-party wildcard clearly includes its host and no exclusion conflicts | Label wildcard coverage as inference unless the portal is explicit | Obtain written confirmation before authenticated testing |
| Does a platform listing authorize research? | Current owner-affiliated program policy and in-scope asset list | Directory, Hacktivity, and historical-report pages are discovery evidence only | Follow the current owner policy, not the search result |
| Does CERT-In authorize testing? | An express CERT-In statement granting permission for the target activity | No such blanket permission appears in the RVDCP | Use CERT-In for lawful reporting and coordination only |
| Is a negative finding conclusive? | Exhaustive authoritative registry, which does not exist here | "Not found" means no public program was verified in this survey | Contact the owner; do not infer that no private process exists |

This method deliberately distinguishes four things that search results often collapse: an inbound campus VDP, a paid production bounty, a controlled educational competition, and a university security group publishing vulnerabilities it found in somebody else's products. The distinction is central to both accuracy and safety.

## 2. Survey Results: One Verified Campus VDP, Several False Positives

### Exact comparison table

| Institution or initiative | Program name and classification | Published scope | Reward structure | Submission channel | Student portal coverage | Survey judgment |
|---|---|---|---|---|---|---|
| Indian Institute of Science | Responsible Vulnerability Disclosure Policy; verified first-party inbound VDP | `*.iisc.ac.in`, public-facing APIs, and IISc mobile applications; third-party services, personal devices, physical security, social engineering, DoS, and automated-tool findings are excluded [3] | No monetary reward; possible discretionary acknowledgment or credit [3] | Email `ciso@iisc.ac.in` with subject `Responsible Vulnerability Disclosure Report`; policy requests description, reproduction steps, evidence, impact, remediation suggestions, and reporter details [3] | Not named. **Inference:** a first-party student portal below `iisc.ac.in` appears within the wildcard, subject to all exclusions and any third-party dependency | **Verified VDP; no cash bounty** |
| IIT Kanpur C3i security page | `Responsible Disclosure`; researcher-side advisory catalogue, not an inbound campus VDP | Listed entries concern Rockwell Automation and Schneider Electric industrial products, not IIT Kanpur campus assets [2] | No campus reward terms shown | No campus reporting channel shown | No | **Not a university-system VDP** |
| SRM University Delhi-NCR, Sonepat | `Bug Bounty`; offline educational competition | Participants identify, analyze, document, and submit findings under organizer-defined ethical boundaries, but the listing names no target environment [7] | No prize amount is stated in the captured listing; a registration fee is shown, which is not a bounty [7] | Reports submitted through the official competition platform [7] | No production domain, ERP, or portal is named | **Controlled event, not verified production bounty** |
| Amrita University on HackerOne | External HackerOne Directory security page | Shows `amrita.edu` and `amrita.ac.in`, but says no reporting guidelines are known [15] | None published on the page | `Request Disclosure Assistance`, not an owner-affiliated program submission route [15] | No | **Community directory entry; no authorization** |
| IIT Madras on HackerOne | External HackerOne Directory security page | Shows `iitm.ac.in`, but says no reporting guidelines are known [16] | None published on the page | Directory/disclosure-assistance context, not a verified owner program | No. A portal is not placed in scope | **Community directory entry; no authorization** |
| IIT Kanpur C3i disclosures | University researchers coordinating findings with product vendors | OEM industrial-control products and CVEs shown in the table [2] | Not stated | The page is a publication list, not an intake policy [2] | No | **Important academic CVD work, but wrong direction for this survey** |
| Manipal University Jaipur | No public production VDP or bounty verified | No public asset scope found. The attempted standard `security.txt` location returns the portal sign-in content [10] | None published | Public IT Infrastructure contact is `it.support@jaipur.manipal.edu`, extensions 778 and 300; this is not labeled as a vulnerability channel [13] | No public authorization found for SLCM | **Disclosure gap; request written scope** |

The most important survey result is the scarcity itself. Searches across IITs, NITs, BITS Pilani, VIT, SRM, IIITs, Ashoka, Shiv Nadar, Jindal, Amrita, and Manipal surfaced many cybersecurity pages, courses, historical reports, and directory records, but only IISc supplied a first-party policy with the basic elements of an inbound campus VDP. This is a survey result, not proof that those institutions lack private reporting arrangements.

### Portal answer in one sentence

**No surveyed Indian university explicitly names its student portal in a verified public VDP or bounty.** IISc provides the only plausible wildcard case, but portal coverage is an **inference** from `*.iisc.ac.in`, not an express statement [3]. That distinction matters because an apparently first-party portal may use a third-party identity provider, payment system, cloud service, or managed application that the policy excludes.

## 3. IISc Case Study: A Strong Baseline With One Portal Ambiguity

IISc's policy is the closest Indian academic analogue for MUJ. Its value is not that it pays researchers; it does not. Its value is that it defines the institutional bargain: what assets are covered, what actions are unacceptable, how a report should be sent, how quickly it will be acknowledged, and how good-faith activity will be treated.

The scope is comparatively clear. It includes IISc domains and subdomains under `*.iisc.ac.in`, public-facing APIs, and institute mobile applications [3]. It excludes third-party services and applications, personal devices of students and staff, physical-security testing, social engineering, denial-of-service attacks, and vulnerabilities identified through automated tools [3]. The automated-tool exclusion is unusually restrictive and should be read literally: even a low-impact automated finding is not covered merely because the target domain matches the wildcard.

The conduct rules are similarly important. Testing must be non-intrusive and must avoid compromising security, privacy, availability, or data. If access is obtained, the researcher must stop and report rather than explore further [3]. Public disclosure requires IISc's prior consent, and researchers must allow time for investigation and mitigation [3]. The policy also requires compliance with applicable laws [3].

IISc asks for reports at `ciso@iisc.ac.in` with the specified subject line. Requested content includes a detailed description, reproduction steps, proof of concept if available, impact, suggested remediation, and contact details [3]. IISc commits to acknowledge receipt within five working days, keep the researcher informed, address validated issues, and notify the reporter after remediation [3]. It also says that it will not pursue legal action for good-faith research that complies with the policy [3].

The reward arrangement is accurately described as recognition, not bounty. IISc offers no current monetary reward, although it may provide public acknowledgment or credit at its discretion [3]. This creates a useful governance model for universities with limited bounty budgets: a VDP can still reduce ambiguity and create a trusted channel without promising cash.

The unresolved point is portal scope. **Inference:** an IISc-operated student portal hosted on a subdomain of `iisc.ac.in` would appear to satisfy the wildcard. The policy nevertheless does not identify any ERP or student portal by name, and third-party services are excluded. A careful researcher should therefore ask the IISc CISO to confirm the exact hostname, ownership, identity provider, test account, permitted techniques, and data-handling limits before doing anything beyond ordinary authorized use.

For MUJ, the lesson is direct: copying only IISc's wildcard would be insufficient. A MUJ policy should explicitly classify SLCM as in scope, out of scope, or report-only/no-testing. It should separately classify Microsoft 365 identity, Akamai-managed edge services, payment processors, parent-login functions, and any vendor-operated backend.

## 4. False Positives: Why Search Results Overstate University Bounties

### IIT Kanpur: disclosure research is not an inbound campus program

The IIT Kanpur C3i page is titled `Responsible Disclosure`, but its table records research advisories involving industrial OEMs and products. Examples include Rockwell Automation PLCs, Schneider Electric devices, Modicon M340 CPUs, and RTUs, with CVEs and vulnerability descriptions [2]. The page shows no invitation to test IIT Kanpur systems, campus asset scope, submission channel, reward policy, or safe-harbor language [2].

This is valuable coordinated-vulnerability-disclosure work by an academic security organization, but it runs from university researchers to outside vendors. Calling it an IIT Kanpur campus VDP would reverse the direction of the program and could mislead students into assuming that institute systems are open for research.

### SRM: a named bug-bounty competition without production scope

The SRM University Delhi-NCR, Sonepat listing is a real university-associated `Bug Bounty` event. It is offline, permits teams of one or two, and asks participants to identify vulnerabilities, assess impact and exploitability, prepare a report, and include a proof of concept [7]. Submissions are judged on severity, exploitability, report quality, proof validity, clarity, and ethical conduct [7].

The missing detail is decisive: the public listing does not name a target, lab, domain, production service, ERP, or student portal [7]. It also does not publish a prize amount in the captured content [7]. Therefore, the event demonstrates a controlled security exercise, not open permission to test SRM infrastructure. Only instructions delivered by the organizers inside the event can define its authorized environment.

### HackerOne Directory: Amrita and IIT Madras are explicit non-programs

The Amrita entry lists `amrita.edu` and `amrita.ac.in`, but immediately says there are no known reporting guidelines. It is marked `External Program`; its information is community-moderated, its accuracy is not validated by HackerOne, and the page is not affiliated with Amrita University [15]. The IIT Madras entry makes the same points for `iitm.ac.in` [16].

These caveats are stronger than mere absence. They directly negate owner affiliation and validation. The entries may help someone seek disclosure assistance after lawfully encountering a problem, but they cannot create scope, safe harbor, a reward promise, or permission to test.

### Historical Open Bug Bounty reports

Open Bug Bounty distinguishes hosted programs governed by a specific program page from generic reports for certain web vulnerabilities detected non-intrusively [8]. It expressly says that the platform itself does not pay bounties; owners of hosted programs pay qualifying rewards directly [8]. Therefore, a historical report involving an academic domain, including the public reports found for Amrita-related domains, shows that a report existed. It does **not** by itself prove that the university operated a bounty or authorized general testing.

## 5. CERT-In RVDCP: National Coordination, Not A Campus Bounty

CERT-In's program is formally named the **Responsible Vulnerability Disclosure and Coordination Policy**, or RVDCP. It defines a process for collecting, analyzing, coordinating mitigation, and ultimately disclosing newly identified cybersecurity vulnerabilities [1]. CERT-In collaborates with researchers, cybersecurity organizations, academic institutions, vendors, OEMs, and other CERTs [1].

### Exact CERT-In comparison table

| Required item | CERT-In position | MUJ relevance |
|---|---|---|
| Scope | Newly identified vulnerabilities in products; the issue should be reproducible on the latest available or supported version and not previously known [1] | A campus web application may require coordination, but the policy does not specifically place university portals in scope |
| Report contents | Affected product and version/model, vendor, description, concise reproduction steps, evidence, and impact; additional discovery and disclosure details are preferred [1] | Use these fields for a minimal, privacy-preserving MUJ report |
| Submission channel | Official Vulnerability Reporting Form: `https://cert-in.org.in/PDF/certinvulnform.pdf` [1] | Use if direct owner coordination fails or national coordination is warranted |
| Initial response | Acknowledgment targeted within 72 working hours [1] | This is a CERT-In target, not an MUJ response SLA |
| Coordination | CERT-In validates, decides whether to coordinate, and works with vendors, the reporter, and stakeholders [1] | Helpful where ownership or vendor responsibility crosses organizations |
| Resolution window | CERT-In endeavors to resolve within 120 days from initial vendor contact, with exceptions for exploitation, severity, duplicate reporting, or party agreement [1] | Do not treat 120 days as permission for unilateral publication |
| Credit | CERT-In may credit the finder in a note or advisory [1] | Recognition may be available |
| Money | CERT-In does not promise a bounty; if a vendor wants to reward a finder, CERT-In only connects the parties and does not join reward discussions [1] | No payment expectation |
| Legal protection | No safe harbor. The reporting party must follow applicable law and remains responsible for discovery activity [1] | CERT-In reporting cannot cure unauthorized testing |

CERT-In makes efforts to restrict disclosure to the minimum needed, although it may share information with trusted third parties when coordination requires it [1]. After remediation, or at an appropriate time agreed with stakeholders, it may publish a vulnerability note or advisory [1]. If an issue remains unresolved after the coordination period, CERT-In may close it or disclose it and end coordination [1].

The practical order for a university club should be: first preserve evidence obtained during normal authorized use; stop activity; notify the university through its designated channel; and use CERT-In where coordination is needed. CERT-In should not be the opening justification for exploring a target.

A further precision point is necessary. The extracted CERT-In web page rendered the email field only as `vulnerability`, not a complete address [1]. This report therefore does not guess an email address. The official PDF form URL above is the exact, verified public channel.

## 6. Hacktivity-Style Platforms: What Each Page Actually Establishes

### Platform comparison table

| Platform or feature | What it is | Scope and reward model | Submission meaning | Authorization warning |
|---|---|---|---|---|
| HackerOne Hacktivity | Searchable repository of disclosed and undisclosed vulnerability reports [6] | Report records can display program, asset, weakness, severity, state, disclosure date, and reward; examples on the page include specific resolved reports and rewards [6] | A research and transparency feed | A report's visibility does not expand the associated program's scope |
| HackerOne Directory external page | Community-maintained record for an organization not necessarily enrolled in a hosted program | Amrita and IITM pages publish no guidelines or reward promise [15][16] | Can offer disclosure-assistance context | Explicitly unaffiliated and unvalidated in these examples |
| Bugcrowd VDP | Managed disclosure channel with multiple submission methods, triage, integrations, and reporting [5] | The cited VDP page does not promise that every VDP pays rewards | Researchers report through a secure channel; Bugcrowd validates, triages, and prioritizes before customer review [5] | The owner's individual engagement brief must govern testing |
| YesWeHack public programs | Program directory checked as an additional hosted-platform source | Listings are program-specific; no Indian university program was verified in the reviewed survey snapshot | Submit only through a current, owner-affiliated program | Directory presence must be paired with the program's exact scope and rules |
| Open Bug Bounty hosted program | Owner-created program with its own guidelines [8] | Owner, not Open Bug Bounty, pays any qualifying bounty [8] | Use the program page and owner-defined process | Rules do not extend beyond listed assets |
| Open Bug Bounty generic reporting | Channel for XSS and some other web vulnerabilities found through prescribed non-intrusive means [8] | No platform-paid bounty [8] | Dangerous classes such as SQL injection or RCE must go directly to the owner's listed email and are not processed in the generic workflow [8] | A generic report is not proof of an owner-run program |

Hacktivity is especially easy to misunderstand. HackerOne calls it a dynamic vulnerability repository and gives users filters for reporter, program, asset type, weakness, CVE, bounty, severity, state, and disclosure date [6]. Those features make it useful for studying how real organizations classify and resolve reports. They do not make every organization appearing in the feed an open target.

Bugcrowd's VDP description highlights the institutional side of the model. Researchers report through a secure disclosure channel; Bugcrowd validates, triages, and prioritizes submissions; the customer then reviews and confirms the triaged finding [5]. Its page also frames a VDP as a trusted reporting method under responsible-disclosure terms and explicitly discusses creating safe harbor for disclosure [5]. Whether a particular researcher receives a bounty, however, depends on the specific engagement, not the generic platform product page.

Open Bug Bounty draws a useful boundary between an owner-hosted program and generic non-intrusive reporting. It accepts generic XSS and some other classes only when found by prescribed non-intrusive means, while a hosted program follows its own page [8]. It does not pay rewards itself [8]. That means its name contains `Bounty`, but not every report is part of a paid bounty.

The operational rule across all platforms is simple: the authoritative artifact is the current, owner-affiliated program policy. Check the exact hostname, asset type, eligibility, allowed techniques, prohibited techniques, test-account requirements, data rules, disclosure timing, and reward table before any action. If one of those is absent, ask first.

## 7. MUJ SLCM: A Disclosure-Safe Plan Without Unauthorized Testing

### Current public posture

The standard RFC 9116 location for a web service is `/.well-known/security.txt` [11]. A conforming file is plain text, UTF-8, and follows the defined grammar; it must contain `Contact` and `Expires`, while `Policy` is optional [11]. At the checked MUJ SLCM URL, the returned content is the ordinary portal sign-in page with `Sign In` and `Parent Login`, not a security contact file [10]. **Inference:** MUJ SLCM does not currently publish a conforming `security.txt` at that location.

MUJ does publish an IT Infrastructure contact: `it.support@jaipur.manipal.edu`, extensions 778 and 300. The same official contact table lists the Registrar Office and Webmaster separately [13]. The IT address is the most relevant public starting point, but it is not described as a security-reporting channel and does not itself grant authorization.

### Safe action table for the university club

| Phase | Allowed, low-risk action | Prohibited or approval-dependent action | Deliverable |
|---|---|---|---|
| 1. Governance request | Email IT Infrastructure asking whether MUJ has a private VDP and who owns SLCM security intake | Do not start testing while waiting | Written owner, channel, and escalation path |
| 2. Scope negotiation | Request exact hostnames, test accounts, dates, source IPs if relevant, data limits, and emergency stop contacts | Do not assume `*.manipal.edu` or the SLCM hostname implies wildcard authorization | Signed or otherwise attributable authorization |
| 3. Third-party classification | Ask MUJ to classify Akamai, Microsoft 365, payment services, parent login, APIs, and vendor-operated components | Do not test a third party under MUJ permission unless that third party is expressly covered | Asset and dependency matrix |
| 4. Rules of engagement | Obtain allowed methods, rate limits, prohibited classes, logging requirements, and handling instructions | No password attacks, MFA testing, social engineering, DoS, bulk automation, persistence, or access to another user's data without explicit approval | Rules-of-engagement document |
| 5. Minimal validation | If authorized, demonstrate only the minimum needed and stop on unexpected access | Do not pivot, enumerate records, download datasets, alter grades, impersonate users, or retain personal data | Redacted evidence and timestamps |
| 6. Reporting | Send a concise encrypted or otherwise approved report through the named channel | Do not send sensitive proof to broad mailing lists or public trackers | Reproducible, privacy-preserving report |
| 7. Coordination | Agree on acknowledgment, severity, remediation, retest, credit, and disclosure timing | Do not publish before written coordination | Closure record and lessons learned |

### Recommended report fields

| Field | Safe content |
|---|---|
| Asset | Exact URL or application component authorized by MUJ |
| Discovery context | State whether it arose during normal portal use, code review, or an approved assessment |
| Preconditions | Authorized role and test-account type, without real credentials |
| Description | Clear security boundary that appears to fail |
| Minimal reproduction | Only the few steps necessary for MUJ's team to reproduce; redact tokens and personal data |
| Impact | Plausible confidentiality, integrity, or availability effect, labeled as demonstrated or inferred |
| Evidence | Sanitized request IDs, timestamps, screenshots, or logs; no third-party data |
| Containment | Confirm that testing stopped and no persistence or data alteration occurred |
| Remediation | Practical fix suggestion, clearly separated from verified facts |
| Disclosure preference | Private coordination, credit preference, and no assumption of a reward |

The club can also propose a MUJ VDP before seeking technical scope. A strong policy should name SLCM explicitly; identify whether parent login and Microsoft identity are covered; distinguish first-party code from Akamai and vendor services; define non-intrusive testing; prohibit social engineering, DoS, credential attacks, and student-data access; state a response target; provide safe harbor for compliant good-faith activity; and publish a valid `security.txt`. IISc's five-working-day acknowledgment and no-cash/possible-credit model offers a practical starting point [3].

## 8. Synthesis: Mechanism, Scope, Trade-Offs, and Evidence

The surveyed mechanisms solve different problems. IISc's VDP solves intake ambiguity: it tells researchers which institute assets are covered, how to behave, where to report, and what response to expect. CERT-In solves multi-party coordination: it validates and works with finders, vendors, and stakeholders, potentially through a 120-day process [1]. HackerOne Hacktivity solves transparency and learning by exposing report metadata [6]. Bugcrowd and similar hosted services solve intake, triage, and workflow at scale [5]. Open Bug Bounty provides both owner-hosted programs and a constrained generic-report path [8]. SRM's event solves education and competition objectives, not continuing production intake [7].

| Dimension | IISc VDP | CERT-In RVDCP | Hosted platforms | SRM event | MUJ current public posture |
|---|---|---|---|---|---|
| Primary mechanism | Direct institutional policy | National coordination | Managed intake, triage, and program pages | Time-bounded controlled challenge | Generic IT contact |
| Scope | Named wildcard, APIs, apps, and exclusions [3] | Newly identified product vulnerabilities [1] | Per-program asset list | Unspecified in public listing [7] | No published security scope |
| Payment | None; possible credit [3] | None from CERT-In; vendor may independently reward [1] | Program-dependent | No prize amount stated in captured page [7] | None published |
| Safe harbor | Good-faith assurance for policy-compliant work [3] | None; reporter remains legally responsible [1] | Program-dependent | Ethical boundaries mentioned, but no public production authorization [7] | None published |
| Student portal | Not explicit; wildcard inference only | Not specifically addressed | Only if a program lists it | Not listed | SLCM not publicly authorized |
| Evidence strength | First-party policy | First-party government policy | Strong only for owner-affiliated program pages | First-party-associated event listing | First-party contact page plus missing conforming `security.txt` |

The non-obvious tension is that the most security-focused institutions do not necessarily publish the clearest campus-testing invitation. IIT Kanpur's C3i page shows sophisticated coordinated disclosure to industrial vendors, yet it offers no campus VDP [2]. SRM uses the phrase `Bug Bounty`, yet its public listing does not identify production targets [7]. Amrita and IIT Madras appear in HackerOne search results, yet the pages expressly deny affiliation and known guidelines [15][16]. These divergences explain why a name or platform badge must never substitute for owner-authenticated scope.

For MUJ, the strategic recommendation is governance-first. A public VDP would convert today's ambiguous contact path into an explicit security control. It would reduce risky improvisation by students, improve report quality, give IT a triage workflow, and clarify third-party boundaries. The policy need not begin with money. IISc demonstrates that clear scope, response commitments, credit, and a good-faith assurance can establish a credible program without a bounty budget [3].

## VERDICT

**Verdict:** In the public evidence reviewed, the **Indian Institute of Science is the only verified Indian university with a first-party, campus-wide inbound vulnerability disclosure policy that clearly states scope, exclusions, submission channel, response expectations, recognition, and good-faith treatment** [3]. It is a VDP, not a monetary bug bounty.

No verified program in this survey expressly places a student portal in scope. IISc's `*.iisc.ac.in` wildcard creates the strongest domain-level case, but portal coverage remains an **inference** and may be narrowed by the third-party exclusion [3]. SRM's event is a controlled competition rather than a published production bounty [7]. IIT Kanpur's page documents outbound research disclosures to OEMs rather than inbound campus reports [2]. HackerOne's Amrita and IIT Madras pages are unaffiliated, unvalidated external-directory records with no known guidelines [15][16].

For **MUJ SLCM**, no public VDP, bounty, portal authorization, or conforming `security.txt` was verified. The correct immediate route is to contact MUJ IT Infrastructure at `it.support@jaipur.manipal.edu`, ask for the designated security owner, and obtain a written scope before any testing [13]. If a vulnerability is encountered during normal authorized use, stop, preserve minimal sanitized evidence, report privately, and consider CERT-In coordination where appropriate. CERT-In is not pre-authorization and provides no legal safe harbor [1].

**Confidence: High for the classifications of IISc, CERT-In, IIT Kanpur, SRM, the two HackerOne Directory pages, Open Bug Bounty, and MUJ's published contact/security.txt posture. Moderate for the nationwide negative conclusion.** The survey used broad and institution-specific public searches, but no authoritative national registry of university VDPs exists, private programs may not be indexed, and policies can change. Therefore, `not publicly verified` is the defensible conclusion for the other universities searched; `does not exist` would be too strong.

## References

1. *RVDCP - Indian Computer Emergency Response Team*. https://www.cert-in.org.in/RVDCP.jsp
2. *Responsible Disclosure | security cse*. https://security.cse.iitk.ac.in/responsible-disclosure
3. *Wp Content*. https://iso.iisc.ac.in/wp-content/uploads/2025/08/RVDP.pdf
4. *Bug Bounty Programs - HackerOne*. https://www.hackerone.com/bug-bounty-programs
5. *Vulnerability Disclosure Programs | Bugcrowd*. https://www.bugcrowd.com/products/vulnerability-disclosure/
6. *Hacktivity | HackerOne*. https://hackerone.com/hacktivity/overview
7. *Bug Bounty - 2026 | 1647952*. https://unstop.com/competitions/bug-bounty-srm-university-delhi-ncr-sonepat-1647952
8. *Open Bug Bounty FAQ - Frequently Asked Questions - OpenBugBounty.org*. https://www.openbugbounty.org/faq/
9. *Free Bug Bounty Program and Coordinated Vulnerability Disclosure | Open Bug Bounty*. https://www.openbugbounty.org/
10. *Manipal University*. https://mujslcm.jaipur.manipal.edu/.well-known/security.txt
11. *RFC 9116: A File Format to Aid in Security Vulnerability Disclosure*. https://www.rfc-editor.org/rfc/rfc9116.html
12. *Directory: Report Vulnerabilities to Companies' Security ...*. https://hackerone.com/directory/programs
13. *Contact Us - Manipal University Jaipur*. https://jaipur.manipal.edu/contact-university.php
14. *Bug Bounty Programs - YesWeHack*. http://yeswehack.com/programs
15. *Amrita University | Response Policy | HackerOne*. https://hackerone.com/amrita_university
16. *HackerOne*. https://hackerone.com/indian_institute_of_techn
