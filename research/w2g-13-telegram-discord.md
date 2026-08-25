# Public MUJ SLCM Community Risk Map

## Executive Summary

This report maps the publicly visible MUJ SLCM and adjacent LMS community footprint without entering private groups, authenticating to the portal, testing credentials, probing the host, or reproducing personal data. The evidence is strongest for the existence of public MUJ-branded community pages and for isolated student reports of login friction. It is weak for any claim that MUJ SLCM credentials, screenshots, or internal messages have been leaked.

- **Community Footprint**: A public Telegram page identifies "Manipal University Jaipur" and describes a MUJ freshers group, while public Discord invite pages identify communities named "Manipal Jaipur" and "Manipal University Jaipur." The pages prove public-facing community listings, not the contents of private or authenticated discussions. [18] [6] [7] -> Use them as leads for community governance research, not as evidence of a security incident.
- **Telegram Evidence Quality**: The direct Telegram page displayed **447 members** and **7 online**, whereas a Telemetrio directory page for the same apparent handle displayed **1,572 subscribers** and said the channel was restricted by Telegram. [18] [17] -> Treat membership counts as time- and source-dependent observations, not a stable population estimate.
- **Discord Evidence Quality**: One public invite page displayed **1,142 members** and **27 online**; another displayed **1,902 members** and **32 online**. [6] [7] A separate directory describes its MUJ community as student-made and organized around study and social channels. [5] -> Community scale is visible, but no public message evidence from those invite pages establishes SLCM help, credential sharing, or leakage.
- **Portal Friction**: A deleted Reddit post describes an old and new registration number both being rejected by SLCM, while another deleted post says the SLCM portal reports a password error even though the poster believes the password is correct. [13] [3] -> These are useful user-support signals, but they are not proof of a common outage, a broken authentication design, or compromise.
- **Official Support Path**: The official SLCM FAQ points users to the MUJ portal and tells users with AMS login trouble to re-verify credentials and then contact institutional DMS or AMS support. [16] [16] It also contains a separate Outlook-account troubleshooting path. [16] -> Direct portal support is safer than crowdsourced password exchange.
- **Leak Status**: The bounded public pages reviewed here did not provide verified MUJ-specific evidence of a leaked SLCM screenshot, credential dump, or credential-sharing conversation. The Telegram preview showed welcome and general-topic entries rather than leak material. [17] The Discord invite previews showed only community identity and membership metadata. [6] -> Report this as "not located in the reviewed public corpus," never as proof that no leak exists.
- **Stack Attribution**: The requester supplied ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 identity as investigation context. The retrieved public portal and passive-scan pages do not independently establish that complete stack. The urlscan page is a scanner page and says the displayed websites and information are not managed by urlscan. [15] [15] -> Keep the supplied stack in the hypothesis column, not the verified-facts column.
- **Identity Risk**: General security research describes infostealers as capable of collecting browser credentials, session cookies, screenshots, and device information, and describes identity-risk data as combining credentials, stealer logs, and PII with provenance and freshness. [23] [24] -> This supports defensive awareness and monitoring, not an inference that MUJ was infected or that any public group contains stolen MUJ credentials.
- **Overall Verdict**: Confidence is **high** that public MUJ-branded community listings and public SLCM problem reports exist; **moderate** that those communities can act as informal student-help or coordination surfaces; and **low** that the reviewed public evidence establishes a leak, credential-sharing event, or the supplied technical stack.

## Scope, Safety, and Evidence Standard

The question combines four different evidence classes: official MUJ application and support pages, public Telegram indexes or landing pages, public Discord invite or directory pages, and public student discussions. These classes should not be treated as interchangeable. An official FAQ can establish an institutional support instruction. A Telegram or Discord landing page can establish that a public listing exists. A Reddit post can establish that a user publicly reported a problem. None of those sources, by itself, proves what happens inside a private channel or proves that a technical vulnerability exists.

The review is deliberately public-only. It did not join a server, request access to a restricted Telegram space, authenticate to MUJ SLCM, submit a login form, test a password, enumerate accounts, retrieve a token, inspect private Discord history, or search for operationally usable secrets. Public invite URLs are included only as reproducibility references. They are not instructions to join or interact with the communities.

The evidence scale used below is:

| Evidence grade | Meaning | Example in this report |
|---|---|---|
| A - Direct official | First-party MUJ or institutional material directly states the fact | The official SLCM FAQ lists the registration link and support workflow. [16] [16] |
| B - Public platform metadata | A public platform page states the name, description, or displayed count | Telegram and Discord landing pages display MUJ names and membership metadata. [18] [6] |
| C - User report | A public user-generated post describes an experience | Reddit posts describe invalid registration numbers or a password error. [13] [3] |
| D - Inference | A conclusion constructed from multiple facts rather than stated by a source | A large student community may increase the social-engineering surface. This is an inference, not an observed incident. |
| N - Not located | The bounded review did not find confirming public material | No verified MUJ-specific leak evidence was located in the reviewed previews. This is not proof of absence. |

The distinction between direct evidence and inference is central. For example, a public community that advertises study channels may plausibly be used for help, but the landing page does not prove that a particular member asked for a password or posted a screenshot. Similarly, a student reporting a failed login is evidence of that report, not evidence of a portal-wide outage.

### cot_explicit: Transparent evidence trail, not private chain of thought

I cannot provide hidden private chain-of-thought. I can provide an auditable reasoning summary that a university security club can reproduce safely. First, I anchored the ecosystem on official MUJ portal, FAQ, and LMS pages. Second, I matched public community pages by explicit MUJ names and handles rather than treating every "Manipal University" result as MUJ. Third, I separated landing-page metadata from visible message content. Fourth, I used public student reports only as reports of user experience and checked them against the official support workflow. Fifth, I searched for leak, screenshot, and credential-sharing indicators but retained a bounded negative conclusion because private, deleted, restricted, or unindexed content cannot be evaluated from public previews.

This approach also rejects several tempting but unsafe shortcuts. A displayed membership count is not a count of active students. A self-described "official" server is not automatically institutionally endorsed. A password-error post is not proof that the password system is vulnerable. A technology label supplied in the research brief is not a verified fingerprint. These decisions are evidence controls, not conclusions that the underlying systems are safe.

## MUJ SLCM and LMS Ecosystem

The public MUJ portal is clearly presented as a sign-in service. One retrieved page says "WELCOME TO MUJ PORTAL" and exposes sign-in and parent-login options. [9] Another public rendering shows the MUJ portal with an `@jaipur.manipal.edu` identity label. [11] A further rendering shows an `@muj.manipal.edu` label alongside parent login. [9] The visible variations establish that more than one public label or rendering exists, but they do not establish separate authentication tenants, separate databases, or an error in identity configuration.

The official SLCM FAQ provides a stronger institutional anchor. It gives the MUJ SLCM registration link and includes a question about being unable to log in to AMS. Its stated first step is to re-verify login credentials, followed by contacting named institutional DMS or AMS support if the issue remains unresolved. [16] [16] The same FAQ contains guidance for a non-working MUJ Outlook account and directs unresolved cases toward IT infrastructure support. [16] This is the most reliable public evidence found for the intended support path.

The FAQ also documents a username convention and says that the password is associated with the official Outlook identity, but this report intentionally omits the example format and does not reproduce any credential-like value. [16] The wording establishes an operational relationship between SLCM or AMS support and an official Outlook account. **[Inference]** It does not, on its own, prove that every portal component uses Microsoft 365 authentication, that single sign-on is enabled, or that the supplied identity architecture is current.

The LMS label belongs to an adjacent but not necessarily identical service. Online Manipal describes an advanced Learning Management System that provides e-tutorials, virtual programming labs, case studies, and e-libraries. [10] Its public material describes a fully online experience involving classes, projects, examinations, and placement activities. [10] A D2L customer page identifies Manipal University Jaipur Online and describes the university's need for a robust learning-management system. [22] **[Inference]** The public evidence supports a connected MUJ digital-learning ecosystem, but it does not prove that the Online Manipal LMS, campus SLCM portal, and any student discussion group share credentials or backend services.

The wider student environment also includes official-facing clubs and chapters. The MUJ student-welfare page lists many clubs and chapters, including technology and student-development organizations. [8] [8] This matters to the threat model because student communities naturally have multiple legitimate communication surfaces. **[Inference]** A broad communication ecosystem can make it easier to route genuine support questions, but it can also make impersonation and misinformation harder for students to detect. That is a governance observation, not evidence of malicious activity.

### exact_tables: Ecosystem anchors

| Entity or surface | What the public evidence states | What it does not establish | Evidence |
|---|---|---|---|
| MUJ portal | Public page presents a MUJ portal with sign-in and parent-login functions | Does not prove a vulnerability, outage, or backend technology | [9] |
| SLCM FAQ | Official document provides the registration link and login-support workflow | Does not authorize anyone to test credentials or access another account | [16] [16] |
| Outlook support | FAQ includes a separate path for a non-working MUJ Outlook account | Does not prove full Microsoft 365 tenant architecture or SSO | [16] |
| Online Manipal LMS | Public site describes an advanced LMS and online learning resources | Does not prove that it is the same application as campus SLCM | [10] |
| D2L MUJ Online case study | D2L identifies MUJ Online as an LMS customer context | Does not prove the current production stack of the campus portal | [22] |
| Student clubs | MUJ's student-welfare page lists clubs and chapters | Does not prove that any club operates a portal-help or security channel | [8] [8] |

The table's key takeaway is that the official sources support an ecosystem map and a support route, not a compromise narrative. The safest operational conclusion is to direct account problems to institutional channels and to treat community discussion as supplementary context.

## Public Telegram Footprint

The clearest MUJ-specific Telegram result is the public page for `@manipaljaipurfresher`. The direct Telegram landing page displays the name "Manipal University Jaipur," describes a "MUJ Freshers group," and says that users can view and join it in Telegram. It displayed **447 members** and **7 online** at retrieval. [18] This is direct platform metadata and is sufficient to establish a public-facing MUJ-branded group page.

A Telemetrio page for the apparent same handle provides a different view. It identifies "Manipal University Jaipur," exposes the handle in its page link, says the channel was restricted by Telegram, and displayed **1,572 subscribers**. [17] The directory also showed "About the channel" with no data in the captured description area. [17] [17] The directory's visible historical entries include welcome messages and general topics such as an online MBA question and a statement about placement data. [17]

The discrepancy is important. It may reflect different capture dates, a channel-versus-group classification difference, platform-side changes, or stale directory data. **[Inference]** It should not be resolved by averaging the numbers or by assuming that the larger number is current. The defensible statement is that public pages have displayed materially different counts for an apparent MUJ fresher community.

A separate generic Jaipur Telegram directory displayed a MUJ entry with **3,903 members** and **55 online**, but the excerpt does not provide enough matching handle information to prove that it is the same object as `@manipaljaipurfresher`. [19] [19] This is a useful example of why search-index results must be de-duplicated before counting communities. It is not used here as a third confirmed count for the same group.

The Telegram evidence does not show SLCM help, a leaked screenshot, or credential-sharing language in the visible excerpts. The rows exposed by the directory are welcome messages and general student topics, not a public credential exchange. [17] The direct landing page likewise provides a welcome and socialization description rather than a security or support description. [18] This does not tell us what may exist in unindexed history or private discussions. It only describes what was publicly visible in the reviewed pages.

A similarly named Telegram result for "Manipal University" was labeled "School of Law" and displayed 104 members. [20] It is not treated as MUJ evidence. This false-positive control is important because the word "Manipal" alone does not identify the Jaipur campus or its SLCM ecosystem.

### exact_tables: Telegram inventory

| Public surface | Visible identity or description | Displayed scale or status | Relevance to the question | Assessment |
|---|---|---|---|---|
| Direct Telegram page | Manipal University Jaipur; MUJ Freshers group; socialization wording | 447 members; 7 online | Public MUJ student-community lead | B - direct public metadata, no visible SLCM or leak content [18] |
| Telemetrio page | Manipal University Jaipur; apparent handle `manipaljaipurfresher` | 1,572 subscribers; channel restricted by Telegram | Historical or indexed community lead | B - directory metadata; count is not reconciled with direct page [17] |
| Telemetrio visible rows | Welcome messages, online MBA question, placement-data comment, general message | Historical entries visible in the directory | Indicates general student topics only | B - no visible credential or screenshot evidence [17] |
| Generic Jaipur directory | MUJ entry in a Jaipur university list | 3,903 members; 55 online in the excerpt | Discovery lead, but no matching handle in the excerpt | C - do not merge with the confirmed handle [19] [19] |
| School of Law result | Manipal University, School of Law | 104 members; 2 online | Name collision control | Eliminated as MUJ SLCM evidence [20] |

The Telegram takeaway is narrow but useful: a public MUJ fresher community is discoverable, and its public metadata has changed or diverged across sources. No reviewed Telegram preview substantiates a leak or password-sharing event. A security club should preserve the distinction between a public landing page, a directory snapshot, and actual message content.

## Public Discord Footprint

The first public Discord invite page identifies a server named "Manipal Jaipur." It displays **27 online** and **1,142 members**. [6] The page is a join or account interface and does not expose a searchable channel list, message history, screenshot, or SLCM support conversation in the captured material. The server's existence is therefore supported, but its internal purpose and moderation quality are not independently established by this page.

A second public invite page identifies "Manipal University Jaipur" and displays **32 online** and **1,902 members**. [7] A related listing uses an official-sounding title for an "Official Public Listed Community of MUJ Students." [7] That wording is a self-description or listing label, not proof of university sponsorship. No retrieved MUJ institutional page in this research confirms that the server is operated or endorsed by the university.

A Discord directory gives a more detailed description of a MUJ community. It says the community server is made by students of Manipal University Jaipur, says that people interested in studying or exploring MUJ can join, and describes department-wise study channels, voice channels, a cafeteria, a fun zone, and peer discussion. [5] This supports a plausible student-help and coordination function. It still does not expose the specific content of those channels or demonstrate that members exchange SLCM credentials.

The two Discord counts should also be handled carefully. They may represent separate servers, different capture times, or different invite pages for overlapping communities. The public evidence does not prove that they are the same server, so the report lists them separately rather than adding them together. **[Inference]** The existence of multiple MUJ-branded public Discord surfaces may increase the number of places where support questions arise, but the evidence cannot rank them by reliability or determine whether any is moderated by authorized staff.

Historical Reddit material also points to student-created Discord discovery, but deleted posts and old invite references are weak evidence for current availability. The public Reddit page for the SLCM login discussion is explicitly marked as an archived post with a deleted author. [13] [13] Similar deleted or archived community references should be preserved as historical leads only, not treated as current access or current membership evidence.

### exact_tables: Discord inventory

| Public surface | Publicly visible identity | Displayed scale | Visible purpose evidence | Security interpretation |
|---|---|---:|---|---|
| Discord invite `7a5D7KKNFf` | Manipal Jaipur | 1,142 members; 27 online | Invite page exposes name and counts only | Public community lead; no visible SLCM, leak, or credential evidence [6] |
| Discord invite with MUJ slug | Manipal University Jaipur | 1,902 members; 32 online | Invite page exposes name and counts only | Separate public community lead; no proof of institutional operation [7] |
| Discord directory listing | Student-made Manipal University Jaipur community | No count used here | Study channels, voice channels, peer discussion, social areas | Supports a help/coordination interpretation, not a security finding [5] |
| Official-sounding listing title | Official Public Listed Community of MUJ Students | 1,902 members in the captured title | Official-sounding label only | Treat as self-description until MUJ confirms ownership [7] |

The Discord takeaway is that public community scale and study-oriented descriptions are visible, but message-level evidence is not. The correct next step for an authorized university team would be governance confirmation and a reporting channel, not covert collection from private spaces.

## Student Portal-Problem Case Studies

### Case study 1: registration-number transition and SLCM rejection

A public post in `r/Manipal_Academics` is titled "Slcm login." The page labels the author as deleted and the post as archived. [13] The visible text says that after an intra-sliding update the student received a new registration number, the old number was rejected, and the new number was also rejected. [13] The post asks what to do and where to contact, making it a direct example of a student seeking a support route rather than an attempt to publish credentials.

The most defensible reading is that this student experienced an identity or registration-state mismatch at the time of posting. It is not possible from the public page to determine whether the cause was delayed data synchronization, a user mistake, an account-state transition, a transient portal issue, or an unrelated problem. The deleted author and archived status also prevent a reliable assessment of any follow-up or resolution. [13] [13]

The official FAQ provides a relevant institutional response pattern: re-verify the login details and contact DMS or AMS support when the issue persists. [16] **[Inference]** The match between the user's request for a contact route and the FAQ's support workflow suggests that official escalation is the appropriate remedy for this class of problem. It does not show that the FAQ was written in response to this Reddit post or that the two events are connected.

### Case study 2: password-error report in r/manipaljaipur

A separate public post in `r/manipaljaipur` is titled "Slcm portal issue." The visible text says, "My password is showing error even though ik that is correct" and asks whether someone else faces the same issue. [3] The page marks the author as deleted and identifies the community as public. [3] [3]

This is evidence of a reported authentication symptom, not evidence that the password was actually correct, that another user saw the same symptom, or that the portal had a systemic outage. There is no visible public resolution in the captured material. The post's wording also does not expose the password itself, and this report does not attempt to infer or reconstruct it.

The official FAQ again gives a safer comparison point. It instructs users with AMS login trouble to re-verify credentials and then use institutional DMS or AMS support. [16] It separately handles Outlook-account failures through password reset and IT infrastructure support. [16] **[Inference]** The combination suggests that students may experience SLCM, AMS, and Outlook issues as related from a user perspective, while the public evidence does not establish whether the systems share a backend or identity provider.

### Case study 3: public community help versus unverified institutional authority

The Telegram page invites MUJ freshers to socialize and meet fellow freshers. [18] The Discord directory describes study channels, voice channels, peer discussion, and project-team discovery. [5] These descriptions show why students may naturally use public communities to ask about administrative portals, course logistics, or access problems.

The same mechanism creates a trust boundary. A student-help group can be useful without being an official support channel. A person offering to "fix" an account in a public chat may be a helpful peer, an impersonator, or simply mistaken. **[Inference]** The public evidence supports a need for clear official-channel labeling and anti-phishing guidance, but it does not show that any MUJ community member has abused that trust.

### exact_tables: Portal-problem evidence

| Public report or official source | Observed wording or function | Status of the evidence | Safe conclusion |
|---|---|---|---|
| Reddit `Slcm login` | Old and new registration numbers were reportedly rejected after an intra-sliding update | User report; author deleted; post archived | One reported registration or login problem; no proof of systemic outage [13] |
| Reddit `Slcm portal issue` | Poster reports a password error despite believing the password is correct | User report; author deleted | One reported authentication symptom; no proof of password validity or compromise [3] |
| Official SLCM FAQ | Re-verify credentials, then contact DMS or AMS support | Direct official guidance | Use institutional escalation instead of sharing passwords [16] |
| Official Outlook troubleshooting | Separate support path for a non-working MUJ Outlook account | Direct official guidance | Keep Outlook recovery within authorized support processes [16] |
| Telegram fresher page | Welcome and socialization description | Public group metadata | Potential peer-help surface, not official support evidence [18] |
| Discord directory | Study, voice, peer, and project-team descriptions | Public directory description | Potential coordination surface, not proof of SLCM support or endorsement [5] |

The case-study takeaway is that the public record supports ordinary support friction and a need for better routing. It does not support upgrading isolated user reports into a claim of a security incident.

## Leaks, Screenshots, and Credential-Sharing Status

### What was and was not found

The public Telegram material reviewed in this run exposes group identity, membership metadata, a restriction notice in a directory, and a small set of visible historical topics. [17] [17] None of the cited visible entries provides a verified SLCM credential, password, session token, private screenshot, or claim of unauthorized access. The direct Telegram page similarly exposes a welcome message and socialization wording rather than a leak report. [18]

The public Discord invite material exposes server names, online counts, member counts, and account-creation interface text. [6] [7] The directory material describes student study and social functions. [5] The retrieved public previews do not expose message history or a verified screenshot-sharing event. This limitation is important: a landing page cannot be used to certify what may have occurred inside a channel that the page does not display.

The URLScan domain page contains a "Live Screenshot" feature, but that is a scanner interface feature and not evidence of a student or attacker screenshot. [15] The same page cautions that the websites and information displayed are not managed by urlscan. [15] **[Inference]** Treating a scanner screenshot as a leaked application screenshot would be a category error.

The bounded search also returned name collisions and general security material, but no verified MUJ-specific public evidence that ties a screenshot, credential list, or credential-sharing discussion to MUJ SLCM. The proper status is therefore **not located in the reviewed public corpus**. This is not a claim that no such material exists. Private groups, deleted posts, restricted channels, ephemeral messages, and unindexed content are outside the evidence available here.

### Why credential claims require special handling

General infostealer research explains that infostealers can steal credentials saved in browsers, session cookies, screenshots, and basic infected-device information, after which the data may be packaged and exfiltrated to attacker infrastructure. [23] Have I Been Pwned describes stealer logs as combinations of website addresses, email addresses, and passwords, while treating passwords as a separate search service. [25] Constella describes identity-risk data as a curated combination of exfiltrated credentials, infostealer logs such as stolen session cookies, and PII with context and freshness. [24]

These sources are general threat-intelligence context, not MUJ evidence. **[Inference]** If a public chat claimed that MUJ credentials had been exposed, the claim would still need provenance, date, affected service, validation by the institution, and careful redaction before it could be treated as an incident indicator. A screenshot with a portal logo would not by itself prove authenticity, currentness, or unauthorized acquisition.

This report does not reproduce example usernames, password formats, email addresses, phone numbers, tokens, invite secrets beyond the already public reference URLs, or any alleged stolen material. The official FAQ contains a credential-related example and an Outlook identity reference, but the example is omitted here because repeating it would add exposure without advancing the public-interest finding. [16] The correct club practice is to preserve only the minimum redacted evidence needed for institutional reporting.

### exact_tables: Evidence status for sensitive claims

| Claim category | Positive public evidence located | Evidence status | What may safely be said |
|---|---|---|---|
| SLCM login problems | Two deleted Reddit posts describe registration-number rejection or a password-error symptom | Verified as user reports, not verified as systemic defects [13] [3] | Publicly reported portal friction exists in the reviewed record |
| Public MUJ help or coordination surfaces | Telegram welcomes freshers; Discord directory describes study and peer channels | Verified as descriptions, not as message-level behavior [18] [5] | Communities may function as informal help surfaces |
| Leaked SLCM screenshot | No verified MUJ-specific leak was visible in the reviewed public pages; urlscan screenshot is a scanner feature | Not located; do not treat scanner UI as leak evidence [15] [15] | No verified public screenshot leak found in the bounded review |
| Credential-sharing talk | No visible cited preview shows a MUJ SLCM password or credential exchange | Not located; private or deleted content remains unknown [17] [6] | Do not claim that credential sharing occurred |
| Infostealer exposure | General sources describe the capability of infostealers | General threat model only [23] [24] | Educate and monitor; do not attribute infection to MUJ |
| Public data breach | No MUJ-specific breach announcement or verified dataset record was located in this review | Not located | Do not label MUJ compromised based on generic breach material |

The table's key takeaway is evidentiary restraint. A negative public search result is useful for prioritization but cannot close an incident investigation. A positive incident conclusion would require an authoritative institutional confirmation or a carefully validated, lawfully obtained artifact, neither of which is present in the reviewed public evidence.

## Application-Security Interpretation of the Supplied Stack

The research brief supplies a host and a proposed architecture: ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai in front, and Microsoft 365 identity. Those values are retained here as **scope metadata supplied by the requester**, not as findings independently established by the public pages reviewed. The public portal pages show sign-in branding and identity labels. [9] [11] The passive URLScan page identifies the domain and exposes scanner metadata, but the captured evidence does not establish the full framework, server, CDN, or identity stack. [15] [15] [15]

This distinction matters because technology labels can be misleading when inferred from a login page. A framework version may be inherited from a component, a server may be behind a reverse proxy, a CDN may mask the origin, and an identity label may be a user-interface convention. **[Inference]** Without an authorized assessment or an authoritative architecture document, it is not safe to convert those hypotheses into vulnerability claims.

The public evidence does support several defensive questions for an authorized owner. First, are the portal, AMS, Outlook, and Online Manipal LMS intentionally separate services or parts of one identity journey? The FAQ mentions SLCM registration, AMS login, and Outlook support in one document, while Online Manipal separately describes its LMS. [16] [16] [10] Second, are students given one unambiguous support route for registration changes and password errors? The two Reddit reports show that students publicly ask where to contact when access fails. [13] [3] Third, are official and unofficial communities visibly differentiated? The Discord directory describes a student-made community, while another listing uses official-sounding wording. [5] [7]

**[Inference]** The principal application-security risk suggested by the public record is not a demonstrated exploit. It is a trust and support-routing risk: students facing login friction may seek help in large public communities, where impersonation, oversharing, or unsafe advice could occur. The inference is grounded in the coexistence of reported portal problems, public student communities, and official support instructions. [13] [18] [16]

A second inference concerns identity exposure. The FAQ's reference to the official Outlook identity creates a reason for the university to review account-recovery messaging and to warn students never to disclose passwords or session information to peers. [16] [16] General infostealer literature explains why browser-stored credentials and session cookies are high-value targets, but that literature does not establish any MUJ-specific infection. [23] [24] The suitable response is preventative hardening and awareness, not public accusation.

### exact_tables: Stack and identity claim audit

| Claim in the research brief | Status after public review | Evidence boundary | Safe wording |
|---|---|---|---|
| ASP.NET MVC 5.3 | Not independently verified in the retrieved public evidence | Public pages show portal sign-in branding, not a verified framework version [9] [15] | "Requester-supplied technology hypothesis" |
| .NET Framework 4.x | Not independently verified | No cited public page establishes the runtime version | Do not publish as a measured fact |
| IIS 10 | Not independently verified | Passive page metadata does not establish origin server software [15] [15] | Treat as an owner-confirmation item |
| Akamai front end | Not independently verified | A reverse-proxy or CDN attribution requires authoritative or authorized confirmation | Treat as an architecture hypothesis |
| Microsoft 365 identity | Partially contextualized only | Official FAQ refers to Outlook identity and Outlook support, but not a complete tenant or SSO design [16] [16] | Say "official Outlook identity is referenced in the FAQ" |
| SLCM and LMS are one system | Not established | Official pages describe portal, AMS support, and an LMS in related but distinct contexts [16] [10] | Keep services separate unless MUJ confirms integration |

The stack-audit takeaway is that public OSINT can identify naming, support, and trust-boundary questions but should not be used to assert a version-specific vulnerability. Any technical verification should be performed only by the owner or by a formally authorized assessment team.

## Risk Analysis and Defensive Recommendations

### Risk 1: students may confuse peer help with official support

The Telegram group presents itself as a fresher social space, and the Discord directory presents a student-made community with study and peer channels. [18] [5] The official FAQ, by contrast, gives institutional routes for login trouble. [16] **[Inference]** This creates a predictable support-routing gap: students may first ask peers because peer communities are visible and fast, while the official route may be less discoverable during an outage or registration transition.

Recommended owner action: publish a short, prominent support notice on the official portal and student onboarding material. The notice should identify the official SLCM, AMS, and Outlook support routes, state that staff will never request a password or session cookie, and explain how to report a suspicious message. This is a defensive communication recommendation, not a suggestion to monitor private student conversations.

### Risk 2: registration changes can create identity confusion

The public SLCM login report describes both an old and a new registration number being rejected after an intra-sliding update. [13] The FAQ separately instructs users to re-verify details and contact support when login fails. [16] **[Inference]** When an account identifier changes, a user may not know whether to retry, reset a password, contact admissions, or contact technical support. Ambiguous ownership can push the user toward crowdsourced advice.

Recommended owner action: provide a controlled registration-change status message that tells a student which identifier is active, when synchronization is expected, and which official unit owns the case. The message should avoid exposing student records. A redacted FAQ update or status banner can address the support need without disclosing backend details.

### Risk 3: password and Outlook support may be perceived as one credential system

The official FAQ references the official Outlook identity when describing password context and includes a separate Outlook-account support path. [16] [16] **[Inference]** Students may therefore assume that a password request from a peer, group administrator, or unofficial helper is legitimate if it is framed as an Outlook or SLCM fix. General infostealer research shows why credentials and session cookies should be treated as sensitive. [23]

Recommended owner action: use consistent anti-phishing language across the SLCM portal, Outlook onboarding, LMS pages, and official social accounts. The language should say that support staff do not need a student's password, one-time code, browser cookie, or screenshot containing personal data. It should provide a report address and encourage password reset through the official recovery flow when a student has already disclosed a secret.

### Risk 4: public community labels may overstate authority

A Discord directory describes a student-made server, while another listing has an official-sounding title. [5] [7] The evidence does not show a university confirmation of ownership. **[Inference]** The visual or textual use of "official" may cause students to assign more authority to an unofficial community than is warranted.

Recommended owner action: publish an official list of recognized channels and a statement that all other groups are independent unless explicitly confirmed. Ask recognized student communities to place a visible disclaimer in their descriptions. This is a transparency measure, not a request to suppress independent speech.

### Risk 5: public leak claims may be amplified without validation

The reviewed material does not verify a MUJ-specific leak, while general threat intelligence shows that stolen identity data can include credentials, session cookies, screenshots, and PII. [23] [24] **[Inference]** A sensational claim in a student channel could be copied across Telegram, Discord, and Reddit before the institution can assess provenance. Repeating an alleged secret in a report can increase harm even when the allegation is false.

Recommended owner action: establish a small incident-validation protocol. Preserve the public URL, timestamp, channel name, and a redacted description. Do not download or redistribute credentials. Escalate through the university's security and legal contacts, and ask the platform to preserve or remove material when appropriate. Publish only confirmed facts and a safe user action such as password reset through official tools.

### exact_tables: Defensive action plan

| Priority | Owner | Action | Evidence or trigger | Safety boundary |
|---|---|---|---|---|
| High | MUJ IT and student services | Make SLCM, AMS, Outlook, and LMS support routes explicit | Students publicly ask where to contact after login failure [13] [16] | Publish contact paths, not account data |
| High | MUJ identity team | State that support never needs passwords, OTPs, cookies, or private screenshots | FAQ links SLCM access with official Outlook identity [16] | Never collect secrets in a club or public channel |
| High | Incident response | Create a redacted intake process for alleged leaks | No verified leak was located, so future claims need provenance | Do not download, test, or redistribute alleged credentials |
| Medium | Community managers | Mark student-made communities as independent unless institutionally confirmed | Discord directory calls its community student-made [5] | Do not treat a public invite as endorsement |
| Medium | Portal owner | Review registration-change messaging and escalation ownership | Reddit report describes old and new identifiers being rejected [13] | Use synthetic test accounts only in authorized testing |
| Medium | Security club | Maintain an evidence ledger with source type, timestamp, confidence, and redaction status | Counts differ across Telegram sources [18] [17] | Preserve public URLs; avoid personal identifiers |
| Low | Communications team | Issue anti-phishing reminders through official channels | Public communities provide informal help surfaces [18] [5] | Educate without monitoring private groups |

The action plan's central recommendation is to reduce the incentive for students to exchange secrets in public communities by making official support faster, clearer, and easier to verify. The public record does not justify intrusive collection or a claim of compromise.

## Comparative Analysis and Synthesis

The major entities and strategies differ along mechanism, scope, authority, and evidentiary strength. The official MUJ FAQ is authoritative but narrow: it explains support and escalation. Telegram and Discord pages are broad community surfaces but expose little message-level evidence. Reddit gives concrete user narratives but has lower reliability and, in these cases, deleted authors and archived posts. General infostealer sources explain a threat mechanism but do not attribute it to MUJ.

| Surface or strategy | Mechanism | Scope | Authority | Main trade-off | Evidence strength |
|---|---|---|---|---|---|
| Official SLCM FAQ | Institutional troubleshooting and escalation | Account and registration support | First-party | Reliable routing but may be less conversational than peer groups | High for stated support workflow [16] [16] |
| Telegram fresher group | Rapid peer socialization and general discussion | Freshers and student topics | Community-level, not established as institutional | Fast help can coexist with misinformation risk | Moderate for existence; low for security claims [18] [17] |
| Discord communities | Study, peer, voice, and project coordination | Larger student community surfaces | One directory explicitly says student-made; institutional endorsement unverified | Richer coordination may increase trust ambiguity | Moderate for descriptions; low for message claims [5] [6] |
| Reddit reports | Individual problem narration and request for help | Public, searchable user discussions | User-generated | Concrete symptoms lack verification and follow-up | Moderate for report existence; low for root cause [13] [3] |
| General identity-risk intelligence | Explains credential, cookie, screenshot, and PII exposure mechanisms | Cross-organization threat model | Industry or service-provider context | Relevant for prevention but cannot prove a MUJ incident | High for general mechanism; none for MUJ attribution [23] [24] |
| Requester-supplied stack | Hypothesized technical architecture | Host and identity scope | Not independently sourced in this review | Useful for authorized scoping but dangerous if stated as fact | Low until owner-confirmed [15] [15] |

Three tensions emerge. First, the largest apparent communities are not the most authoritative sources. Discord pages display 1,142 and 1,902 members, yet the public evidence does not show that either server is university-run. [6] [7] The official FAQ has far less social reach but stronger authority for account support. [16] The implication is that MUJ should improve the discoverability of official help rather than try to replace independent communities.

Second, public visibility and evidentiary visibility diverge. Telegram and Discord pages make community names and counts visible, but not the messages that would be needed to verify credential-sharing or screenshot allegations. [18] [6] A community can be highly visible as an entity while remaining opaque as an information source. The implication is that OSINT reports should not convert size into risk severity without message-level evidence.

Third, support friction and security risk are related but not equivalent. Reddit reports show that students ask for help when registration numbers or passwords appear to fail. [13] [3] General infostealer sources show why credentials and cookies are valuable targets. [23] **[Inference]** Together these facts justify anti-phishing controls and a clear escalation path, but they do not justify claiming that a failed login was caused by stolen credentials or that MUJ suffered a breach.

The overall synthesis is therefore a two-track conclusion. Track one is an ordinary service-quality finding: public students have described access friction, and MUJ publishes a support process. Track two is a security-governance finding: public peer communities may become de facto support channels, so institutional communications should make authority, privacy, and reporting boundaries explicit. Neither track supplies verified evidence of an SLCM exploit, leak, or credential-sharing event.

## Limitations and Unanswered Questions

The following questions remain unanswered by public evidence:

| Unanswered question | Why the current evidence cannot answer it | Safe next step for an authorized owner |
|---|---|---|
| Are the public Telegram and Discord communities currently active in their internal channels? | Landing pages expose metadata, not full message history; one directory says the Telegram channel was restricted [17] | Ask community administrators for a public moderation and reporting statement; do not enter private areas for covert collection |
| Are the two Discord invite pages the same server or different servers? | Names and counts differ, and the pages do not expose stable ownership evidence [6] [7] | Confirm ownership through published official contacts |
| Did the Reddit login reports indicate a common outage? | Posts are individual, deleted, and lack verified resolution [13] [3] | Review authorized support tickets and incident records, not public speculation |
| Did a MUJ SLCM screenshot or credential dump circulate privately? | Private, deleted, restricted, and unindexed material is outside this public review | Use lawful incident-response channels and request platform preservation if a specific public URL is reported |
| What is the actual production stack? | Public portal branding and passive pages do not verify all supplied versions or vendors [9] [15] | Obtain an owner-approved architecture record or conduct an authorized assessment |
| Are SLCM, AMS, Outlook, and the LMS federated? | The FAQ and LMS pages show related services but not the integration design [16] [10] | Confirm the identity architecture with MUJ IT; do not infer it from labels |
| Is any community officially endorsed? | One listing is official-sounding and another says student-made, but public institutional confirmation was not found [7] [5] | Publish a recognized-channel directory and independent-community policy |

These are not gaps to fill through unauthorized access. They are questions for the institution, its contracted assessors, platform administrators, or formally authorized incident responders. The public OSINT finding should remain bounded until such confirmation exists.

## VERDICT

**Overall confidence: Moderate for the public ecosystem map; high for the existence of public MUJ-branded listings and isolated public SLCM problem reports; low for any leak, credential-sharing, compromise, or stack-attribution conclusion.**

The public record supports the following final findings:

1. MUJ has a publicly visible SLCM portal and an official FAQ with a defined support path for login problems. [9] [16] [16]
2. A public Telegram page identifies a MUJ fresher group, and public Discord pages identify MUJ-branded communities. [18] [6] [7]
3. Public directory and community descriptions support a student social, study, and coordination role, but do not prove university ownership or expose message-level behavior. [5] [7]
4. Two public, deleted Reddit reports describe SLCM access friction involving registration-number rejection and a reported password error. [13] [3]
5. No verified MUJ-specific public evidence of a leaked SLCM screenshot, credential dump, or credential-sharing event was located in the bounded pages and previews reviewed. The correct qualification is "not located," not "did not happen." [17] [6] [15]
6. The supplied ASP.NET MVC, .NET Framework, IIS, Akamai, and Microsoft 365 descriptions remain unverified scope hypotheses. The official FAQ's Outlook references provide context but not a complete architecture confirmation. [16] [16] [15] [15]

The recommended disposition is **monitor and clarify, not escalate publicly as a breach**. MUJ or an authorized assessor should validate the architecture, improve official support messaging, publish recognized channels, and establish a redacted process for future public leak claims. The security club should preserve public URLs and timestamps, avoid joining or probing communities, never collect credentials, and label every conclusion as direct evidence or inference.

## References

1. [[deleted by user] : r/Manipal_Uni_Jaipur](https://www.reddit.com/r/Manipal_Uni_Jaipur/comments/13u7kvt/muj_freshers_discord)
2. [[deleted by user] : r/manipaluniversityjaip](https://www.reddit.com/r/manipaluniversityjaip/comments/1d5mj8a/manipal_university_jaipur_freshers_discord)
3. *Reddit - The heart of the internet*. https://www.reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue
4. *MUJStella - Student Platform for Manipal University Jaipur*. https://mujstella.in/
5. *Manipal University Jaipur – Discord.Do*. https://discord.do/manipal-university-jaipur/
6. *Discord*. https://discord.com/invite/7a5D7KKNFf
7. *Discord*. https://discord.com/invite/manipal-university-jaipur-1008377907057545269
8. *Clubs and Chapters - Manipal University Jaipur *. http://jaipur.manipal.edu/dsw-student-clubs.php
9. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
10. *Online Bachelor and Master Programmes | Online Degree Programs in India | Online Manipal*. https://muj.onlinemanipal.com/
11. *Manipal University*. https://muj.slcm.jaipur.manipal.edu/
12. *Online Manipal | UGC Entitled Online UG & PG Degree Courses*. http://muj.onlinemanipal.com/notifications
13. *Reddit - The heart of the internet*. https://www.reddit.com/r/Manipal_Academics/comments/1993mdc/slcm_login
14. [[deleted by user] : r/manipaljaipur](https://www.reddit.com/r/manipaljaipur/comments/1d5synl/a_discord_server_for_freshers_joining_muj/)
15. *mujslcm.jaipur.manipal.edu - urlscan.io*. https://urlscan.io/domain/mujslcm.jaipur.manipal.edu
16. *Frequently Asked Questions and Contacts for SLCM Registration*. https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf
17. *Manipal University Jaipur 📚🖥 - Statistics & analytics of Telegram channel @manipaljaipurfresher*. https://telemetr.io/en/channels/1394408318-manipaljaipurfresher
18. *Telegram: View @manipaljaipurfresher*. https://t.me/manipaljaipurfresher
19. *Jaipur Telegram groups in  universities, List of Telegram groups in  2026*. https://www.neargroups.com/telegram/jaipur/universities
20. *Telegram: View @manipal_university*. https://telegram.me/manipal_university
21. *Telegram: View @manipal_university*. https://t.me/manipal_university
22. *Manipal University Jaipur (Online) | D2L*. https://www.d2l.com/en-in/why-d2l/customers/manipal-university-jaipur-online
23. *http://flare.io/flare-data-explorer/stealer-logs*. http://flare.io/flare-data-explorer/stealer-logs
24. *http://constella.ai/*. http://constella.ai/
25. *http://haveibeenpwned.com/API/v3*. http://haveibeenpwned.com/API/v3
