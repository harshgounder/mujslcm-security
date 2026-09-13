# Human-Vector Assessment for MUJ SLCM

## Executive Insights

- **Campaign Status**: The supplied assessment record marks the social-engineering campaign as ABSENT, and no human-vector evidence was collected because the campaign never authenticated. That is an assessment gap, not evidence that users, mailboxes, or Entra identities are resistant. -> Record the class as Not Assessed, not Pass, until a bounded simulation produces delivery, reporting, click, and escalation evidence.

- **Most Relevant Technique Family**: MITRE ATT&CK separates phishing delivery into attachment, link, third-party service, and voice variants under T1566.001 through T1566.004. [10] -> Start with a control matrix covering email, personal webmail, collaboration services, SMS, and voice rather than testing only the MUJ SLCM web page.

- **Credential Objective**: T1598 describes phishing for information as an attempt to trick a target into disclosing credentials or other actionable information, and distinguishes that objective from phishing intended to execute code. [11] -> The safe first test should measure whether a user reports a suspicious request or enters a dummy value, never whether a real password or MFA token can be captured.

- **Personal-Gmail Exposure**: The supplied record says that credentials are delivered to personal Gmail. MITRE explicitly places personal webmail and other non-enterprise services in the spearphishing-via-service family. [31] **Inference**: a Microsoft 365-only mail-control view may miss part of the user journey. -> Add a test-account and endpoint/browser telemetry path for approved personal-mail scenarios, without contacting real personal accounts.

- **DMARC Limitation**: RFC 7489 defines `p=none` as a request that no specific delivery action be taken for DMARC failures. [26] **Inference**: the supplied `p=none` posture on three domains should be treated as a monitoring and impersonation-risk issue, not as a blocking control. -> Verify reporting, SPF, DKIM alignment, Microsoft anti-phishing policy, lookalike-domain protection, and user reporting before any authorized simulation.

- **Identity Pivot**: Microsoft documents consent phishing as tricking users into granting permissions to malicious cloud applications, which can expose legitimate cloud services and data. [3] **Inference**: the presence of Microsoft 365 identity and three Entra tenants makes OAuth-consent behavior a separate test objective from password phishing. -> Validate consent policy and audit visibility with a harmless, preapproved test application or a vendor simulation; do not request real data permissions.

- **Preferred Simulation Tools**: Gophish is an open-source toolkit for phishing engagements and awareness training. [22] Microsoft Attack Simulation Training provides managed scenarios and reports when the tenant has Defender for Office 365 Plan 2 or Microsoft 365 E5. [4] -> Prefer Microsoft AST when licensed and Gophish when a university-controlled, self-hosted lab is required; avoid credential-capture frameworks.

- **Detection Evidence**: Microsoft Safe Links can scan and rewrite URLs, check them at click time, and store click data; wrapped mail clicks appear in `UrlClickEvents` with `AppName` set to `Mail`. [30] Entra audit logs capture application, service-principal, user, and permission changes. [35] -> Define the expected evidence chain before launch: message trace, URL click, endpoint/browser event, user report, and Entra audit event where applicable.

- **Authorization Boundary**: NIST says Rules of Engagement are established before a test and give the team authority for defined activities without additional permissions. [45] SET and King Phisher also warn that explicit permission is required. [12] [20] -> Passive public research can proceed now; any message, call, SMS, lookalike page, test login, OAuth prompt, or interaction with a target account requires the signed scope letter and the two test accounts.

- **Build Priority**: The largest gap is not another phishing framework. It is a safe evidence pipeline that joins campaign IDs, delivery status, user report, click, endpoint signal, and Entra audit data without collecting secrets. -> Build that read-only measurement layer before expanding channel coverage.

## Scope, Evidence, and Safety Boundary

This report addresses social-engineering and human-vector classes around the MUJ SLCM portal. It does not claim that the portal is exploitable, that any account was compromised, or that any message reached a real user. The target facts in the brief are treated as supplied assessment inputs dated 2026-09-13: IIS 10, ASP.NET MVC 5.3, .NET Framework 4.7.4136.0, jQuery 1.10.2 plus bundled jQuery 3.4.1, Microsoft Azure AS8075, Microsoft 365 identity, three Entra tenants, no attributable edge control, no HSTS, TLS 1.0 through 1.3 offered, port 443 as the only reachable port, the stated error behavior, and the stated campaign gate. They do not have a public URL in the supplied material, so they are not presented as independently re-verified web findings.

The supplied record also says that the campaign never authenticated and that the aggressive phase is gated behind a signed scope letter plus two test accounts. Those constraints are binding. The report therefore describes tools and control objectives at a defensive, non-operational level. It does not provide lure copy, target-selection advice, credential-capture setup, proxy configuration, token replay, persistence, or instructions to contact users.

The requested `cot_explicit` output cannot be supplied as private chain-of-thought. Instead, this is an auditable reasoning summary that shows the evidence, the inference, and the resulting decision. This preserves the useful decision trail without exposing hidden internal deliberation.

| Evidence or supplied input | Classification | Decision consequence |
|---|---|---|
| Campaign status is ABSENT and no human-vector class was assessed | Supplied assessment input | Mark the class Not Assessed. Do not convert absence of campaign evidence into a security pass. |
| DMARC is `p=none` on three domains | Supplied input interpreted using RFC 7489 | Treat DMARC as non-enforcing by itself and prioritize monitoring, anti-phishing, and reporting. [26] |
| Credentials are delivered to personal Gmail | Supplied input mapped to ATT&CK | Include third-party-service and endpoint detection; personal webmail is within T1566.003's documented scope. [31] |
| Microsoft 365 identity and three Entra tenants | Supplied input mapped to Microsoft guidance | Separate password, MFA, OAuth-consent, and cross-tenant audit questions. [3] |
| YSOD, method behavior, `enc` oracle, cookies, TLS, and HSTS observations | Supplied web-layer inputs | Track them as web application findings. Do not infer a human-vector result from them. |
| Signed scope letter and two test accounts required for aggressive testing | Supplied authorization condition, consistent with NIST ROE | No target-directed delivery or authentication test before the letter and accounts are available. [45] |

The central inference is therefore narrow: the target's stated identity and mail posture make human-vector testing relevant, but they do not establish that phishing succeeds. The right deliverable is a controlled measurement plan and a tool decision, not an attack campaign.

## Technique Universe for the Human-Vector Class

MITRE ATT&CK's T1566 family is the primary delivery universe. Its four sub-techniques cover malicious attachments, malicious links, third-party services, and voice. [10] MITRE describes these as electronically delivered social engineering, often relying on the user to click, open, call, download, or provide access. [27] CAPEC-98 independently describes phishing as masquerading as a legitimate entity to induce confidential information disclosure, commonly credentials. [7]

| Family or technique | What it covers | MUJ SLCM relevance | Safe evidence to collect |
|---|---|---|---|
| T1566.001 Spearphishing Attachment | An attachment-based lure; MITRE notes that the user normally must open the attachment and that the message supplies a plausible reason. [29] | Benign attachment simulation may test whether users report or open an inert document. It must not contain malware, macros, exploit code, or active content. | Delivery, report, open event, file classification, and endpoint alert. |
| T1566.002 Spearphishing Link | A message containing a link that asks the user to click or copy a URL. [32] | The natural first controlled test for a portal-adjacent identity journey, but the destination should be a static training page and should never request a real password. | Delivery, Safe Links verdict, click, browser event, report, and training completion. |
| T1566.003 Spearphishing via Service | Delivery through personal webmail, social media, or another third-party service rather than enterprise email. [31] | Directly relevant to the supplied personal-Gmail fact. It requires an approved test mailbox and endpoint, not real student or staff accounts. | Test-mail receipt, endpoint/browser event, report, and any permitted downstream identity signal. |
| T1566.004 Spearphishing Voice | A phone-based variant that manipulates a user into providing access or taking a follow-on action. [27] | Relevant to vishing and MFA-prompt social engineering, but only with test numbers and an approved script. | Call completion, report, callback decision, browser or RMM event, and MFA/consent signal. |
| T1598.001-.004 Phishing for Information | The same four delivery surfaces when the objective is gathering data rather than code execution. [11] | The core credential and information-disclosure class for this brief. | Dummy-value submission, report, or safe abandonment; never a real secret. |
| T1204 User Execution | The human action that follows delivery, such as opening a file or link. [16] It has five current sub-technique IDs. [16] | Measures human action separately from message delivery and from server-side web behavior. | Click/open timestamp, browser or file event, child process if benign test instrumentation is used, and report. |
| Consent phishing | A cloud-identity variant in which a user grants permissions to an application. Microsoft describes the permission and data-access risk. [3] | Relevant to Entra tenants, but it should be tested with a harmless application and explicit scope. | Consent prompt display, refusal or approval, app/service-principal audit record, and removal verification. |
| Impersonation and lookalike identity | A supporting social mechanism, not a replacement for the ATT&CK delivery IDs. Microsoft notes that lookalike domains can pass SPF, DKIM, and DMARC while still impersonating a trusted identity. [34] | Relevant to the supplied DMARC posture, but no lookalike-domain delivery should occur before written authorization. | Anti-phishing verdict, user report, and message trace; no real-user targeting. |

A key distinction prevents measurement errors. T1566 answers how the message or call arrives; T1598 answers whether the objective is information disclosure; T1204 answers what the person does next. A campaign can therefore deliver a link, ask for information, and measure a click without ever executing code. That is why a portal's YSOD, antiforgery, HTTP method, and `enc` behavior cannot substitute for a human-vector result.

Consent phishing and QR phishing deserve explicit treatment. ATT&CK documents malicious links used for OAuth access tokens and device-code phishing. [32] Microsoft AST supports OAuth Consent Grant and QR-code payloads, with click and permission-related report fields. [46] These are not reasons to run a live consent or QR campaign against users. They are reasons to include the corresponding control points in the test matrix.

## Target-Specific Risk Interpretation

The MUJ SLCM application findings supplied in the brief are mostly web-layer observations. Verbose YSOD behavior can disclose implementation details; an antiforgery cookie lacking `Secure` is a transport-control concern; TLS and HSTS posture affect transport hardening; method and parameter behavior are application-layer observations. None of those facts proves that a human can be persuaded to disclose a password. The campaign status should remain ABSENT until a human-vector exercise produces evidence.

The email and identity inputs change prioritization. RFC 7489 says `p=none` requests no specific action on a failing message, whereas `quarantine` asks receivers to treat it as suspicious and `reject` asks them to reject it. [26] **Inference**: if all three domains really remain at `p=none`, DMARC alone does not give the receiving system an instruction to quarantine or reject. That does not prove spoofed messages will be delivered, because local mail policy, SPF, DKIM, Microsoft anti-phishing, reputation, and lookalike detection can still act. It does mean that DMARC aggregate reporting and other controls carry more weight.

Microsoft anti-phishing policies provide spoof intelligence, first-contact safety indicators, impersonation protection, thresholds, and additional reporting. [34] Microsoft also warns that a lookalike domain can pass email authentication while still deceiving a recipient. [34] **Inference**: a safe assessment should test not just exact-domain spoofing, but whether the defensive program recognizes a visually similar sender, a new external sender, and a third-party-service message. It should do so with approved simulation identities, not by registering a deceptive domain and mailing real users.

The personal-Gmail fact maps directly to T1566.003. MITRE describes fake social accounts, personal webmail, rapport-building, and delivery outside enterprise mail controls. [31] **Inference**: the scope must include the browser and endpoint used for the approved test account, because the Microsoft 365 mail tenant may not see the original message or click path. This is especially important when the same browser later reaches a Microsoft identity page. The test should still avoid real personal accounts and should not ask a test user to submit an actual secret.

The three Entra tenants create a second boundary. Microsoft documents that consent phishing can grant an application access to data and recommends control over consent, publisher verification, auditing, and least privilege. [3] [3] **Inference**: the assessment should name the tenant, test account, application, and expected audit event for every authorized identity scenario. A result from one tenant must not be generalized to the other two.

### Case Study: Microsoft Attack Simulation Training

Microsoft AST is a useful case because it demonstrates what a human-vector assessment should measure without requiring an actual compromise. The service supports credential-harvest, malware-attachment, link, drive-by URL, and OAuth-consent scenarios, and Microsoft says it is available with Defender for Office 365 Plan 2 or Microsoft 365 E5. [46] [46] [4] The platform reports delivery, user actions, training, and activity details; its report fields include user, compromise state, timestamps, browser, IP, device, and actions such as clicking, forwarding, replying, deleting, and granting permissions. [46]

The important design lesson is separation of simulation from compromise. Microsoft supports a credential-harvest simulation, but a university can configure the exercise so that the test stops at a safe training boundary. It can measure who received a message, who reported it, who clicked, and who completed training without storing a real password. The service also exposes predicted versus actual compromise rates, which gives the university a way to compare difficulty and outcomes rather than merely count clicks. [4]

### Case Study: Gophish and King Phisher

Gophish illustrates the self-hosted measurement model. Its project describes an open-source toolkit for phishing engagements and awareness training, supports binary releases, and exposes a local web interface. [22] The campaign documentation records opening, link clicks, attempted landing-page submission, and device information. [9] Raw logs can be exported to CSV, and GoReport can produce CSV or DOCX reports. [25] Its MIT license is permissive but does not remove the need for authorization. [41]

King Phisher illustrates the broader channel and content model, but also the legal boundary. Its repository describes awareness campaigns, flexible email and server content, multiple campaigns, landing-page credential harvesting, page cloning, geolocation, plugins, and SMS campaign alerts. [20] It is BSD 3-clause licensed, yet the project explicitly says it is for legal applications with explicit permission. [20] [20] For MUJ SLCM, only the awareness and measurement subset is appropriate; credential harvesting and cloning are not needed to answer the research question.

### Case Study: High-Risk Credential and Session Tools

Evilginx, Modlishka, and CredSniper demonstrate why tool enumeration must distinguish awareness simulation from adversary-grade credential capture. Evilginx describes itself as a man-in-the-middle framework for phishing credentials and session cookies and for bypassing two-factor authentication; it also implements its own HTTP and DNS server. [14] [14] Modlishka describes a transparent reverse proxy, ethical phishing testing, and 2FA bypass support. [19] CredSniper explicitly advertises credential and 2FA-token capture and an API for captured credentials. [28]

These tools may be relevant to threat modeling, but they are not appropriate first-line MUJ test tools. Using them would create exactly the secrets and session artifacts that the university should avoid collecting. Their presence in this inventory is a warning and a gap classification, not a recommendation to deploy them. A signed scope letter does not automatically make real credential or token collection proportionate; the proposed assessment can answer the human-vector question with dummy inputs and safe landing pages.

## Tool Inventory and Operational Boundaries

The table below covers the publicly documented tools identified for this bounded review. "Every tool" is interpreted as every tool located in the reviewed public sources for the listed technique families, not every commercial product or private fork on the Internet. Public availability, license, and documentation do not grant permission to use a tool against MUJ SLCM.

| Tool and exact URL | License and delivery model | How it is driven at a safe level | Documented output or limitation | MUJ decision |
|---|---|---|---|---|
| Gophish - https://github.com/gophish/gophish | MIT license; free/open source and self-hosted. [41] | Local web interface and campaign configuration; the README documents binary releases and a local browser interface. [22] External mail or hosting is **BYOK by inference** because the operator supplies infrastructure; the cited project does not promise a hosted relay. | Campaign dashboard; open, click, landing submission attempt, device and browser data; CSV raw logs; GoReport CSV or DOCX. [9] [25] | Preferred self-hosted option for a safe email simulation using static pages and dummy data. |
| King Phisher - https://github.com/CrimsonForge-io/king-phisher | BSD 3-clause; free/open source and self-hosted. [20] [20] | Client/server architecture, message and server templates, and plugins; no attack steps are provided here. [20] [20] | Campaign events, landing-page interactions, geolocation, SMS campaign alerts, and flexible content are documented; a canonical export format is not stated in the cited page. [20] | Use only for authorized awareness work if its server and content are isolated and credential collection is disabled.
| Phishing Frenzy - https://github.com/pentestgeek/phishing-frenzy | GPLv3, free copyleft software. [39] | A Ruby on Rails phishing framework; the cited README provides the project identity but not a safe operating procedure. [42] | The cited public material does not specify a canonical report format or complete event schema. | Candidate for lab review only; require a source audit, isolation, and a written output contract before use. |
| Social-Engineer Toolkit (SET) - https://github.com/trustedsec/social-engineer-toolkit | BSD-derived license text; free/open source. The project says to review its license before use. [43] | Interactive console; the project describes guided vectors for authorized social-engineering assessments. [12] [12] | Public README evidence in this review does not establish a normalized awareness-report format. | Not a first choice for MUJ. It is broad and high-risk; use only in a contained lab or for expressly scoped, non-credential demonstrations. |
| Microsoft Attack Simulation Training - https://learn.microsoft.com/en-us/defender-office-365/attack-simulation-training-get-started | Commercial Microsoft 365 capability requiring Defender for Office 365 Plan 2 or Microsoft 365 E5; this is a tenant entitlement, not an open-source license. [4] | Microsoft Defender portal, role-based permissions, and scheduled or launched simulations. Microsoft documents Attack Simulation Administrator, Attack Payload Author, Security Operator, and Security Reader roles. [4] | Managed reports, CSV export, delivery, training, compromise, browser, IP, device, click, reply, delete, forward, and permissions-granted fields. [46] [46] [46] | Best fit if already licensed. Prefer safe payloads, no real secrets, and tenant-by-tenant approval. |
| Evilginx - https://github.com/kgretzky/evilginx2 | BSD-3-Clause; free/open source but self-hosted and high-risk. [14] [14] | Standalone man-in-the-middle framework with its own HTTP and DNS server. [14] No setup or lure instructions are included. | Repository includes a `log` directory, but the cited material does not define a safe awareness output schema. [14] | Threat-model reference only. Do not deploy against MUJ, do not collect credentials, cookies, or MFA tokens. |
| Modlishka - https://github.com/drk1wi/Modlishka | GPLv3; self-hosted; commercial use is described as permitted under the license, with a separate contact note for commercial applications. [19] [19] | Transparent reverse-proxy model and point-and-click proxying are described publicly. [19] | Credential-management/session-impersonation functionality is documented, but a safe report format is not. [19] | Threat-model reference only; not needed for a human-awareness result. |
| CredSniper - https://github.com/ustayready/CredSniper | Apache 2.0; free/open source and self-hosted. [28] [40] | Flask/Jinja phishing framework; high-level documentation only. [28] | Explicitly captures credentials and 2FA tokens and exposes captured data through an API. [28] | Exclude from the proposed engagement. It creates real-secret risk and exceeds the measurement need. |
| Muraena - https://github.com/muraenateam/muraena | License and commercial terms were not established in the cited source set. | Public description indicates a custom reverse-proxy approach. [13] | Output and logging contract were not established. | Do not select until license, provenance, output handling, and safe-mode behavior are independently verified. |
| Proofpoint phishing simulations - https://www.proofpoint.com/us/products/security-awareness-training/phishing-simulations | Vendor-hosted commercial service; the cited product page does not state an open-source license or public price. | Hosted awareness platform with simulated phishing and additional channel templates described by the vendor. [47] | Product reporting is vendor-specific; obtain retention, export, and secret-handling terms contractually. | Possible SaaS option, subject to university procurement, privacy review, and no real-credential configuration. |
| Cofense PhishMe SAT - https://cofense.com/phishme-security-awareness-training-(sat)-platform | Vendor-hosted commercial service; public page does not state an open-source license or public price. | Vendor describes realistic simulations delivered through active email and awareness workflows. [48] | Board-ready reporting and analytics are described publicly; exact export schema should be confirmed before purchase. [48] | Possible option for managed training, subject to data-processing and tenant-scope review. |
| Hoxhunt - https://hoxhunt.com/ | Vendor-hosted commercial service; public page does not state an open-source license or public price. | Vendor describes simulations across email, SMS, phone calls, and Teams with personalized training. [49] | Dashboard and microtraining outputs are vendor-specific; verify retention and export. | Useful for multi-channel coverage if procurement and test-account controls are acceptable. |
| SoSafe phishing simulations - http://sosafe-awareness.com/products/phishing-simulations | Vendor-hosted commercial service; public page does not state an open-source license or public price. | Vendor describes email, smishing, and vishing simulation capabilities. [50] | Dashboard metrics are described; exact event schema and retention need contractual confirmation. [50] | Candidate for channel coverage, not a substitute for Entra and endpoint evidence. |
| Arsen vishing and smishing - https://arsen.co/en/solutions/vishing-smishing | Vendor-hosted commercial service; public licensing and price were not stated in the cited page. | Vendor describes vishing and smishing solutions. [51] | Output schema was not established in the cited source. | Candidate only after lawful telecom, privacy, and test-number review. |
| KnowBe4 security awareness training - https://www.knowbe4.com/products/security-awareness-training | Vendor-hosted commercial service; public page describes training and testing but not an open-source license. | Vendor platform for training, testing, and reinforcement. [52] | Confirm exact exports, channel coverage, and data retention with the vendor. | Possible email-awareness option; still requires independent Entra and endpoint correlation. |

The table shows an important procurement distinction. Open-source does not mean safe, and hosted does not mean complete. A tool can report a click while missing personal-Gmail delivery, endpoint behavior, or Entra consent. Conversely, a managed platform can simplify campaign reporting while leaving the university dependent on vendor retention and export terms.

## Manual Method Where Tool Coverage Is Missing

A manual method is necessary for local workflows, service channels, and voice when a platform does not support the exact university process. The method below is intentionally a control-validation method, not a phishing recipe.

| Surface | Manual control-validation method | Safe output | Authorization |
|---|---|---|---|
| Email link | Send one preapproved message only to the two test accounts, using a neutral training destination that collects no password and no token. | Message trace ID, delivery result, report action, click time, Safe Links result, and training-page visit. | Signed scope letter and test accounts required for sending. |
| Email attachment | Use an inert, non-macro document with a unique test marker. Do not use executable content, exploit content, macros, or active scripts. | Delivery, report, open event if available, endpoint alert, and removal confirmation. | Signed scope letter and test accounts required. |
| Personal Gmail or other service | Use only an institution-controlled test mailbox or the supplied test account. Do not contact a real personal address. Place a static marker page behind the test link and record only the approved event token. | Mail receipt, browser click, report, and endpoint event. | Signed scope letter and explicit third-party-service permission required. |
| SMS or Teams | Use a test number or test channel and an approved message that points to a static training page. Do not impersonate a real person or request a login. | Delivery, click, report, and channel metadata. | Signed scope letter plus channel owner approval. |
| Voice | Use a test number, a preapproved short script, and a stop condition. The script must not request a secret, MFA approval, or production action. | Call completion, report or refusal, and any approved follow-on event. | Signed scope letter, test number, and explicit voice approval. |
| OAuth consent | Prefer a screenshot or mock consent screen. If a real test is necessary, use a harmless application, minimum permissions, test account, immediate revocation, and a written tenant-by-tenant rule. | Consent display, refusal or approval, Entra audit record, and revocation evidence. | Signed scope letter, named tenant, named app, and test accounts. |
| User reporting | Give test users a documented reporting route and measure reporting latency, not just clicks. CISA recommends built-in email reporting and prompt response. [8] | Report timestamp, channel, triage result, and feedback completion. | Training owner approval; target-directed exercise still needs the letter. |

The manual method has no need to imitate the real MUJ login page. It can use a university-branded training page that states it is an authorized exercise after the event, or it can use a neutral page that immediately explains the test. A unique, non-secret token can correlate a test account to a page visit. That token must not be reusable as a credential, session cookie, or authorization artifact.

NIST's Phish Scale is a suitable measurement framework for the message itself. NIST describes it as a method for awareness-training implementers to rate an email's human phishing-detection difficulty. [23] It should be used before launch to document why a message is easy, moderate, or difficult, and after launch to compare difficulty with reporting and click outcomes. The scale does not authorize a campaign and does not replace an ROE.

## Detection Counterpart

Detection must be designed before the exercise. A click-only result is weak: it may reflect an automated scanner, a Safe Links prefetch, a forwarded message, or a user opening a message without believing it. The strongest evidence is a correlated chain with a message identifier, event timestamp, user report, browser or endpoint signal, and identity audit record when relevant.

| Technique or behavior | Detection counterpart | Relevant source and MUJ action |
|---|---|---|
| T1566.001 attachment | Audit inbound attachments, scan them, correlate mail metadata to file creation, process start, and outbound activity. MITRE lists these controls and correlation points. [29] | Validate Defender or endpoint telemetry on the two test accounts; retain only benign markers. |
| T1566.002 link | Correlate inbound mail, embedded URLs, Safe Links verdicts, browser navigation, and any subsequent identity event. MITRE describes this correlation chain. [32] | Enable or verify Safe Links click tracking. Microsoft documents URL rewriting, time-of-click checks, and click storage. [30] [30] |
| T1566.003 service | Monitor approved third-party-service interactions, browser downloads, and subsequent endpoint behavior. MITRE specifically calls out personal webmail, Gmail, and social-media paths. [31] | Use an institution-controlled test mailbox and endpoint. Do not assume Microsoft mail logs contain the originating service event. |
| T1566.004 voice | Review corporate call logs, VoIP/SIP records, messaging-client activity, browser/RMM follow-on, and MFA or consent events. [27] | Test only with a number and script named in the ROE. |
| T1598 information disclosure | Measure report, refusal, safe dummy-value entry, and training completion. Do not store real credentials. MITRE distinguishes information gathering from code execution. [11] | Define a zero-secret data contract before launch. |
| T1204 user execution | Look for open/click, file creation or decompression, child process, and outbound behavior when the test is allowed to create a benign event. [16] | Use inert content and endpoint instrumentation. A click alone is not proof of compromise. |
| Spoofing and impersonation | Use anti-phishing policies, spoof intelligence, impersonation protection, thresholds, first-contact signals, and message trace. [34] [34] | Compare exact-domain spoof handling with lookalike-domain warning behavior in a lab or vendor simulation, not with real recipients. |
| URL protection | Safe Links scans incoming mail, can rewrite URLs, checks at click time, warns on malicious links, and can store click data. [30] [30] | Confirm the target policy and `UrlClickEvents` visibility before the exercise. |
| OAuth consent | Audit application and service-principal creation or changes, requested permissions, user consent, and sign-in activity. Microsoft recommends auditing consented permissions. [3] | Correlate with Entra audit logs. Microsoft says application, group, user, and license changes are captured. [35] |
| Mail delivery | Use Message trace to determine whether messages were received, rejected, deferred, or delivered and what actions occurred before final status. [36] | Capture trace identifiers for test messages and retain them with the campaign evidence. |
| User reporting | Provide the built-in reporting route and test triage. Microsoft exposes a Defender Submissions page for suspected phishing or fraud. [38] | Measure report latency and analyst disposition, not just employee behavior. |
| Strong authentication | Prefer phishing-resistant MFA, such as passkeys or FIDO/PKI-based methods. Microsoft describes passkeys as phishing-resistant credentials. [1] CISA describes FIDO or PKI-based MFA as phishing resistant. [8] | Treat this as a control recommendation, not permission to test bypasses. |

### Detection Case Study: Safe Links and Entra Logs

Safe Links and Entra audit logs answer different questions. Safe Links can show that a protected user clicked a wrapped mail URL and can block or warn on a malicious verdict. [30] Entra audit logs can show application, service-principal, permission, and actor details. [35] **Inference**: a successful human-vector defense requires both planes when an exercise includes identity. A mail click without an Entra event may be a safe abandonment; an Entra consent event without the expected campaign token may indicate a separate application path or an attribution problem.

Message trace adds delivery truth. Microsoft says it follows messages through the cloud organization and shows whether they were received, rejected, deferred, or delivered, as well as actions before final status. [36] The report should not label a user as vulnerable if the message was not delivered, nor label a user as safe if the message was never presented. This is a measurement rule, not an assumption about MUJ's current configuration.

## NO-TOOL GAPS

| Gap | Why existing tools do not close it | Consequence for MUJ SLCM | Priority |
|---|---|---|---|
| No human-vector baseline | The supplied campaign is ABSENT; tools can generate events but cannot create historical user behavior. | No defensible reportable rate for reporting, clicking, or safe abandonment. | High |
| No personal-Gmail evidence path | Microsoft mail controls focus on controlled mailboxes, while ATT&CK treats personal webmail as a third-party service. [31] | The most relevant supplied path may be invisible to tenant-only dashboards. | High |
| No voice and SMS evidence | Email tools do not automatically prove behavior on phone or SMS channels. | Vishing and smishing remain unassessed even if email controls pass. | High |
| No cross-tenant correlation contract | Microsoft audit logs are tenant-specific records; the supplied environment has three Entra tenants. | A result from one tenant could be incorrectly generalized. | High |
| No zero-secret credential measurement | Several open-source tools can capture real credentials or tokens, but that is unnecessary and unsafe. [28] [14] | The club lacks a safe default for measuring information-disclosure behavior. | High |
| No normalized event schema | Gophish exports CSV and optional DOCX, AST exports CSV, and other tools have vendor-specific dashboards. [25] [46] | Cross-tool comparison and independent audit are difficult. | Medium |
| No difficulty calibration | A click rate without message difficulty can mislead. NIST Phish Scale exists for this purpose. [23] | A hard or easy message can dominate the apparent result. | Medium |
| No documented tool assurance | Some projects do not document a canonical output format, safe mode, or retention behavior. [42] | Procurement and evidence handling may be weaker than the campaign UI suggests. | Medium |
| No post-event recovery measure | A simulation may record a click but not whether the user reports, changes a password, revokes consent, or follows response guidance. | The university cannot measure resilience after the initial mistake. | Medium |

The most important gap is the absence of an evidence contract. Before selecting a platform, define the minimum record: campaign ID, target test-account identifier, channel, message trace ID if applicable, delivery state, report timestamp, click timestamp, Safe Links verdict, endpoint marker, Entra tenant, application ID if applicable, consent or refusal, training status, and retention deadline. Explicitly exclude passwords, MFA codes, session cookies, refresh tokens, and production personal data.

## BUILD CANDIDATES

| Candidate | Safe design | Output | Guardrail |
|---|---|---|---|
| Zero-secret simulation orchestrator | Submit static training URLs and inert attachments only to the two test accounts. Generate one-time random correlation tokens that cannot authenticate. | Normalized JSON or CSV event records with delivery, report, click, and training states; no secrets. | Reject any form field named or behaving like a password, token, or MFA input. |
| Three-tenant identity evidence adapter | Read approved audit events from each Entra tenant and normalize tenant ID, application, actor, timestamp, permission change, and correlation ID. Entra logs expose timestamps, service, activity, status, correlation ID, and actor or target details. [35] | Tenant-separated audit extract and a cross-tenant comparison table. | Read-only permissions, named test app, immediate revocation, and no real data scopes. |
| Mail and URL evidence joiner | Join Message trace, Safe Links or `UrlClickEvents`, campaign token, and report timestamp. | One timeline per test message and a false-positive review queue. | Do not treat a Safe Links scan or prefetch as human intent without corroboration. |
| Personal-service test harness | Use an institution-owned test Gmail mailbox or approved equivalent, a controlled browser profile, and a static training page. | Receipt, click, report, browser, and endpoint events. | Never use a student's or employee's personal mailbox; obtain explicit third-party-service approval. |
| Voice and SMS safe harness | Use test numbers, preapproved scripts, an immediate stop phrase, and a static page. | Call or message delivery, report, refusal, and training events. | No impersonation of real staff, no MFA approval request, no secret collection. |
| NIST difficulty annotator | Store Phish Scale rationale for each message before launch. | Difficulty label, rationale, and comparison with report and click outcome. | Do not interpret difficulty as a license to increase deception beyond the ROE. |
| Recovery and training tracker | Record report, password-reset advice delivered, consent revocation, and training completion after the exercise. | Time-to-report, time-to-remediate, and completion metrics. | Use dummy accounts and do not force production password changes. |
| DMARC observability dashboard | Consume authorized aggregate DMARC reports and compare aligned sources over time. RFC 7489 describes aggregate reporting feedback. [26] | Domain, source, alignment, disposition, and trend records. | Treat reports as sensitive metadata; restrict access and define retention. |

The first build should be the evidence joiner plus zero-secret simulation orchestrator. It provides more security value than adding another landing-page clone. The second build should cover the personal-service path, because that is the supplied fact most likely to evade a tenant-only campaign report. Voice and SMS can follow after legal, privacy, and telecom approvals.

## Pre-Authorization Versus Authorized Activities

| Activity | Safe before the signed scope letter? | Requires the signed scope letter and two test accounts? |
|---|---|---|
| Read public MITRE, NIST, CISA, Microsoft, and project documentation | Yes | No |
| Passive review of public DNS, DMARC, SPF, DKIM, certificates, and public mail metadata | Yes, if limited to public information and ordinary rate limits | No |
| Review the supplied web findings and map them to human-vector hypotheses | Yes | No |
| Build a local lab using synthetic users, domains, and dummy data | Yes | No |
| Review tool licenses and inspect source code without executing against MUJ | Yes | No |
| Configure AST, Gophish, or another platform in a disconnected lab | Yes | No |
| Send a simulated email to a MUJ address or test mailbox | No | Yes, with exact sender, recipient, schedule, content, and stop conditions in scope |
| Send SMS, Teams, or personal-webmail test content | No | Yes, with channel owner approval and test endpoint |
| Place a voice call or test MFA-prompt workflow | No | Yes, with named test number and explicit voice or identity scope |
| Host a lookalike or portal-themed landing page for a target user | No | Yes only if expressly written, but this report recommends a neutral static page instead |
| Ask a user to log in or enter a password, MFA code, session value, or OAuth permission | No | The proposed plan does not require real secrets even with authorization; use dummy values or a mock page |
| Capture, store, replay, or export real credentials, cookies, refresh tokens, or MFA tokens | No | Not proposed and not necessary for this assessment |
| Use Evilginx, Modlishka, CredSniper, or similar AiTM tools against the portal or users | No | Not proposed; keep them as threat-model references only |
| Query tenant audit logs or message trace for the approved exercise | No target access before scope; after approval, yes with least privilege and named tenant/account | Yes |

NIST's ROE principle is the governing standard for authorization: authority should exist for defined activities before testing begins. [45] The tool warnings reinforce that principle. SET says not to use it against systems, accounts, networks, or people without consent. [12] King Phisher requires explicit permission from the targeted organization. [20]

## Synthesis and Comparative Analysis

The tools and techniques divide into three materially different strategies. First, managed awareness platforms such as Microsoft AST, Proofpoint, Cofense, Hoxhunt, SoSafe, Arsen, and KnowBe4 reduce operational burden and may cover multiple channels. Their trade-off is dependency on licensing, vendor retention, export formats, and privacy terms. AST has the strongest documented alignment with this target's Microsoft identity context because it reports delivery, user activity, and OAuth-consent simulation fields. [46] [46]

Second, self-hosted awareness frameworks such as Gophish, King Phisher, Phishing Frenzy, and SET give the university greater control over data and customization. Gophish has the clearest documented reporting path in this review: dashboard events, CSV logs, and optional CSV or DOCX reporting. [25] King Phisher has broader content and campaign features but also documents credential harvesting and page cloning, which increases the need for isolation and configuration review. [20] Phishing Frenzy's cited README establishes its framework identity but not a complete output contract. [42] The trade-off is that the club must supply safe infrastructure, protect logs, and build its own evidence joins.

Third, AiTM and credential-capture frameworks such as Evilginx, Modlishka, CredSniper, and Muraena model the adversary's high-risk path rather than a proportionate awareness test. Evilginx explicitly targets credentials and session cookies; Modlishka describes transparent proxying and 2FA-bypass use cases; CredSniper describes capturing credentials and 2FA tokens. [14] [19] [28] Their mechanism is technically closer to the threat, but their trade-off is secret exposure, session risk, legal risk, and unnecessary contact with production identity. For MUJ SLCM, using them would reduce safety without improving the answer to whether users recognize and report a lure.

The technique universe also reveals a non-obvious divergence. Email delivery is visible to Microsoft mail controls, but personal Gmail, social platforms, voice, and SMS move the event outside a single mail tenant. Conversely, Entra consent can create a strong identity audit trail even when the initial message was external. The correct architecture is therefore not a single phishing dashboard. It is a controlled multi-surface exercise with a normalized evidence layer that joins mail, browser, endpoint, user report, and Entra records.

The target's web findings create another tension. The portal has application-layer observations that deserve remediation, but those findings should not be used to justify social engineering or to infer that phishing will work. Human-vector risk is about trust, delivery, user action, identity controls, and detection. The portal can be technically hardened while the organization remains vulnerable to a convincing request sent through personal webmail; the reverse can also be true. That is why this class should be independently assessed and reported as Not Assessed until evidence exists.

## Recommended Decision Sequence

1. **Before authorization**, document the supplied facts, perform only passive public checks, review DMARC reporting and public anti-phishing posture, map the three tenants, and build a synthetic lab. Do not send messages or interact with real users.
2. **After the signed letter and test accounts**, select Microsoft AST if the required license exists. Otherwise use Gophish in a university-controlled environment with a static, zero-secret training destination. Keep the exercise to the two test accounts first.
3. **Measure the email-link path**, then the inert attachment path if expressly required. Capture Message trace, Safe Links, report, click, endpoint, and training evidence. Stop if any real secret is requested or entered.
4. **Measure personal-service behavior** only with the approved test mailbox and browser profile. Treat this as a separate T1566.003 campaign, not as an extension of the Microsoft 365 mail test.
5. **Measure consent behavior** with a mock screen or harmless test application and minimum permissions. Verify the expected Entra audit event and revoke immediately.
6. **Defer voice and SMS** until telecom, privacy, and channel-owner approvals are written into the ROE. Use test numbers, neutral scripts, and no MFA or secret request.
7. **Do not deploy AiTM or credential-capture tools.** Their documented purpose is disproportionate to the research question and creates avoidable secret-handling risk.

## VERDICT

**Overall confidence: High for the technique taxonomy, safety boundary, and detection architecture; Medium for tool inventory completeness and current commercial licensing details.** The public sources clearly establish the T1566, T1598, and T1204 universe, the distinction between delivery, information disclosure, and user execution, the relevance of third-party services and consent phishing, and the available Microsoft and open-source reporting mechanisms. [10] [11] [16] [31]

**Campaign verdict: ABSENT / NOT ASSESSED.** Based on the supplied record, no human-vector campaign authenticated and no human-vector class was assessed. That is not a Pass. The evidence supports a controlled, zero-secret simulation plan, not a conclusion that MUJ SLCM users would resist phishing.

**Priority verdict: High.** The supplied combination of `p=none`, personal-Gmail credential delivery, Microsoft 365 identity, and three Entra tenants creates a plausible human-vector research priority. The inference is not that compromise is occurring; it is that a tenant-only mail posture may not measure the full path. RFC 7489's semantics support treating `p=none` as non-enforcing by itself. [26] MITRE's third-party-service technique supports expanding the detection boundary. [31]

**Tool verdict: Use Microsoft AST if licensed; otherwise use Gophish in a lab or tightly scoped two-account exercise. Use hosted multi-channel services only after procurement, privacy, export, and retention review. Keep Evilginx, Modlishka, CredSniper, and Muraena out of the proposed engagement.** The defensible success criterion is not credential capture. It is whether the approved test accounts receive, recognize, report, safely abandon, and recover from a simulated request, with the expected mail, browser, endpoint, and Entra evidence.

## References

1. *Passkeys (FIDO2) authentication method in Microsoft Entra ID ...*. https://learn.microsoft.com/en-us/entra/identity/authentication/concept-authentication-passkeys-fido2
2. *NIST Phish Scale User Guide*. https://www.nist.gov/publications/nist-phish-scale-user-guide
3. *Protect against consent phishing - Microsoft Entra ID*. https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/protect-against-consent-phishing
4. *Get started using Attack simulation training - Microsoft ...*. https://learn.microsoft.com/en-us/defender-office-365/attack-simulation-training-get-started
5. *License | Gophish User Guide*. https://docs.getgophish.com/user-guide/license
6. *Anti-phishing protection - Microsoft Defender for Office 365*. https://learn.microsoft.com/en-us/defender-office-365/anti-phishing-protection-about
7. *CAPEC - CAPEC-98: Phishing (Version 3.9) - Mitre Corporation*. https://capec.mitre.org/data/definitions/98.html
8. *Phishing Guidance: Stopping the Attack Cycle at Phase One - CISA*. https://www.cisa.gov/sites/default/files/2025-03/Phishing%20Guidance%20-%20Stopping%20the%20Attack%20Cycle%20at%20Phase%20One%20508.pdf
9. *Campaigns | Gophish User Guide*. https://docs.getgophish.com/user-guide/documentation/campaigns
10. *Phishing, Technique T1566 - Enterprise | MITRE ATT&CK®*. https://attack.mitre.org/techniques/T1566/
11. *Phishing for Information, Technique T1598 - MITRE ATT&CK®*. https://attack.mitre.org/techniques/T1598/
12. *GitHub - trustedsec/social-engineer-toolkit: The Social ...*. https://github.com/trustedsec/social-engineer-toolkit
13. *GitHub - muraenateam/muraena: Muraena is an almost ...*. https://github.com/muraenateam/muraena
14. *GitHub - kgretzky/evilginx2: Standalone man-in-the-middle ...*. https://github.com/kgretzky/evilginx2
15. *SP 800-115, Technical Guide to Information Security Testing ...*. https://csrc.nist.gov/pubs/sp/800/115/final
16. *User Execution, Technique T1204 - Enterprise | MITRE ATT&CK®*. https://attack.mitre.org/techniques/T1204/
17. *UrlClickEvents table in the advanced hunting schema ...*. https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-urlclickevents-table
18. *RFC 7489: Domain-based Message Authentication, Reporting, and ...*. https://www.rfc-editor.org/info/rfc7489/
19. *GitHub - drk1wi/Modlishka: Modlishka. Reverse Proxy. · GitHub*. http://github.com/drk1wi/Modlishka
20. *GitHub - CrimsonForge-io/king-phisher: Phishing Campaign ...*. https://github.com/CrimsonForge-io/king-phisher
21. *CredSniper/README.md at master · ustayready/CredSniper · GitHub*. https://github.com/ustayready/CredSniper/blob/master/README.md?plain=1
22. *Gophish: Open-Source Phishing Toolkit - GitHub*. https://github.com/gophish/gophish
23. *TN 2276, NIST Phish Scale User Guide | CSRC*. https://csrc.nist.gov/pubs/tn/2276/final
24. *Phishing Guidance: Stopping the Attack Cycle at Phase One | CISA*. https://www.cisa.gov/resources-tools/resources/phishing-guidance-stopping-attack-cycle-phase-one
25. *Generating Reports*. https://docs.getgophish.com/user-guide/documentation/generating-reports
26. *RFC 7489: Domain-based Message Authentication, Reporting, and Conformance (DMARC) | RFC Editor*. https://www.rfc-editor.org/rfc/rfc7489
27. *Phishing: Spearphishing Voice, Sub-technique T1566.004 - Enterprise | MITRE ATT&CK®*. https://attack.mitre.org/techniques/T1566/004/
28. *GitHub - ustayready/CredSniper: CredSniper is a phishing framework written with the Python micro-framework Flask and Jinja2 templating which supports capturing 2FA tokens. · GitHub*. https://github.com/ustayready/CredSniper
29. *Phishing: Spearphishing Attachment, Sub-technique T1566.001 - Enterprise | MITRE ATT&CK®*. https://attack.mitre.org/techniques/T1566/001/
30. *Complete Safe Links overview for Microsoft Defender for Office 365 - Microsoft Defender for Office 365 | Microsoft Learn*. https://learn.microsoft.com/en-us/defender-office-365/safe-links-about
31. *Phishing: Spearphishing via Service, Sub-technique T1566.003 - Enterprise | MITRE ATT&CK®*. https://attack.mitre.org/techniques/T1566/003/
32. *Phishing: Spearphishing Link, Sub-technique T1566.002 - Enterprise | MITRE ATT&CK®*. https://attack.mitre.org/techniques/T1566/002/
33. *Simulate a phishing attack with Attack simulation training - Microsoft Defender for Office 365 | Microsoft Learn*. https://learn.microsoft.com/en-us/defender-office-365/attack-simulation-training-simulations
34. *Anti Phishing Policies About*. https://learn.microsoft.com/en-us/defender-office-365/anti-phishing-policies-about
35. *Learn about the audit logs in Microsoft Entra ID - Microsoft ...*. https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-audit-logs
36. *Message trace in the Microsoft Defender portal*. https://learn.microsoft.com/en-us/defender-office-365/message-trace-defender-portal
37. *King Phisher Documentation¶*. https://king-phisher.readthedocs.io/en/latest/
38. *Report spam, non-spam, phishing, suspicious emails, Teams ...*. https://learn.microsoft.com/en-us/defender-office-365/submissions-report-messages-files-to-microsoft
39. *phishing-frenzy/LICENSE at master · pentestgeek/phishing-frenzy · GitHub*. https://github.com/pentestgeek/phishing-frenzy/blob/master/LICENSE
40. *CredSniper/LICENSE at master · ustayready/CredSniper · GitHub*. https://github.com/ustayready/CredSniper/blob/master/LICENSE
41. *gophish/LICENSE at master · gophish/gophish · GitHub*. https://github.com/gophish/gophish/blob/master/LICENSE
42. *phishing-frenzy/README.md at master · pentestgeek/phishing-frenzy · GitHub*. https://github.com/pentestgeek/phishing-frenzy/blob/master/README.md
43. *social-engineer-toolkit/readme/LICENSE at master · trustedsec/social-engineer-toolkit · GitHub*. https://github.com/trustedsec/social-engineer-toolkit/blob/master/readme/LICENSE
44. *Modlishka/LICENSE at master · drk1wi/Modlishka · GitHub*. https://github.com/drk1wi/Modlishka/blob/master/LICENSE
45. *Rules of Engagement (ROE) - Glossary | CSRC*. https://csrc.nist.gov/glossary/term/Rules_of_Engagement
46. *Reports for Attack simulation training - Microsoft Defender for Office 365 | Microsoft Learn*. https://learn.microsoft.com/en-us/defender-office-365/attack-simulation-training-insights
47. *Assess - Phishing Simulations, Assessments & Tests ...*. https://www.proofpoint.com/us/products/security-awareness-training/phishing-simulations
48. *PhishMe Security Awareness Training (SAT) Platform | Cofense*. https://cofense.com/phishme-security-awareness-training-(sat)-platform
49. *The Hoxhunt Human Risk Management Platform*. http://hoxhunt.com/
50. *Personalised Phishing Simulations | SoSafe*. http://sosafe-awareness.com/products/phishing-simulations
51. *Vishing & Smishing Attack Simulation*. https://arsen.co/en/solutions/vishing-smishing
52. *Phishing Simulation Reporting: Key Metrics, Dashboards, and ...*. https://www.accountablehq.com/post/phishing-simulation-reporting-key-metrics-dashboards-and-templates
