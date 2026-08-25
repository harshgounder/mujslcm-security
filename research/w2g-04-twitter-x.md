# MUJ SLCM Public-Source OSINT Report: Evidence, Gaps, and Risk Signals

## Executive Summary

- **X Coverage Result**: Direct public X search pages for `mujslcm`, `slcm.manipal`, `Manipal portal`, and `MUJ portal` exposed an authentication, cookie, and navigation shell rather than tweet result cards. No qualifying tweet body, timestamp, screenshot, or tweet URL was visible in those pages [9]. Treat this as a coverage-limited negative, not evidence that no such posts exist.
- **MUJ Portal Identity**: The target host publicly brands itself `WELCOME TO MUJ PORTAL` and presents sign-in functionality, including a parent-login label [4]. An alternate hostname displays the `@jaipur.manipal.edu` identity label [3]. This supports portal attribution, but it does not independently prove the full backend or infrastructure stack.
- **Official Documentation**: An official MUJ FAQ identifies `https://mujslcm.jaipur.manipal.edu/` as the SLCM registration link and directs users with login trouble to university contacts [17]. This is stronger attribution evidence than third-party naming alone.
- **Observed Service Complaints**: Public Reddit pages contain one report of a password being rejected despite the user believing it was correct [5], and another report that a completed fee payment remained marked pending in SLCM [2]. Neither page supplies a verified incident timeline or resolution [2].
- **Public Security Signal**: The retrieved corpus contains no authoritative breach disclosure, CVE, or institutional incident notice tied specifically to the MUJ SLCM host. The official MUJ notification page contains dated notices and helpdesk information, but the extracted content contains no outage or security-incident notice [11].
- **Security-Relevant Exposure**: Search results surfaced public academic-record pages whose titles and descriptions indicate documents derived from MUJ SLCM paths, including a January-May 2025 grade sheet [18]. This is a privacy and provenance concern, not proof of a portal vulnerability or unauthorized disclosure.
- **Unofficial Ecosystem**: Public browser extensions and student-built sites interact with or describe MUJ SLCM functionality. One extension says it automates feedback-form completion and requests access to data for all websites [6]. Another says it works only on MUJ SLCM and handles website content [10]. These artifacts warrant user-safety review, but they do not prove maliciousness.
- **Current Verdict**: Confidence is high that the host is publicly presented as a MUJ portal and that public users have reported login and fee-status problems. Confidence is low that there was a documented outage, breach, or exploitable security defect, and low that X contains no relevant posts. The requester-provided technology description remains unverified by this public-source pass.

## Scope, Method, and Evidence Rules

This report covers publicly retrievable material only. The research questions were separated into four keyword searches, MUJ portal attribution, complaints, security disclosures, screenshots, and infrastructure context. The method used direct X search URLs, indexed-web discovery, official MUJ pages, public user discussion, and public extension or repository pages. It did not submit credentials, attempt authenticated access, probe application behavior, scan the target, or reproduce secrets.

The X limitation is material. The direct `Manipal portal` search page displayed cookie text, login prompts, and general navigation, but no tweet author, post body, timestamp, screenshot, or tweet URL [9]. The same retrieval pattern applied to the other target searches. Search engines also returned unrelated results for terms such as `mujslcm`, including posts about Muslims and unrelated `MuJS` software. Those results were excluded as entity-conflation errors. A search result that contains a term but does not identify the MUJ portal is not evidence about this ecosystem.

The report distinguishes four evidence classes. First, an official source is a MUJ or Manipal domain that identifies the portal or publishes a notice. Second, a user report is a public Reddit complaint that records an experience but not a verified root cause. Third, an ecosystem artifact is a public extension, repository, or third-party service describing an integration. Fourth, an inference is an analyst interpretation that is not explicitly stated by a source. Every inference below is labeled as such. The report does not present a claim of compromise merely because a page, extension, or academic document references the portal.

The requested instruction asked for explicit chain-of-thought. Private hidden reasoning is not reproduced. Instead, this section provides an auditable decision summary: direct X pages were checked; qualifying MUJ-specific tweet cards were not visible; indexed candidates were inspected; unrelated false positives were discarded; official attribution was separated from user complaints; and security claims were restricted to what the sources actually state.

## X/Twitter Findings: What Was Actually Visible

### Direct keyword searches

| Target query | Direct public URL | Visible result | Assessment |
|---|---|---|---|
| `mujslcm` | https://x.com/search?q=mujslcm&src=typed_query | X shell, login prompts, navigation; no visible tweet card | No qualifying tweet evidence visible [19] |
| `slcm.manipal` | https://x.com/search?q=slcm.manipal&src=typed_query | X shell and sign-in flow; no visible tweet card | No qualifying tweet evidence visible [20] |
| `Manipal portal` | https://x.com/search?q=Manipal%20portal&src=typed_query | Cookie controls, login prompts, and navigation | No visible tweet author, text, date, screenshot, or tweet URL [9] |
| `MUJ portal` | https://x.com/search?q=MUJ%20portal&src=typed_query | X shell and navigation | No qualifying tweet evidence visible [21] |

The table records an important negative finding: the retrieved public page did not expose the search results themselves. It would be methodologically unsound to convert that into "there are no posts." Search indexing can be incomplete, X can personalize or restrict results, deleted posts can disappear, and public pages can require a session for result rendering. The correct conclusion is narrower: no qualifying tweet-level evidence was available in the retrieved public rendering.

### MUJ-specific X post URLs

A later indexed search surfaced four post URLs from the `@Jaipur_Manipal` account. They are genuine MUJ-related post candidates, but none concerns the SLCM portal.

| Date shown | Tweet URL | Visible subject | SLCM, outage, or security relevance |
|---|---|---|---|
| Aug 15, 2026 | https://x.com/Jaipur_Manipal/status/2088634410635759649 | Independence Day celebrations at Manipal University Jaipur [15] | None visible [15] |
| Aug 18, 2026 | https://x.com/Jaipur_Manipal/status/2089600565877821835 | IAESTE MUJ culinary workshop [13] | None visible [13] |
| Aug 21, 2026 | https://x.com/Jaipur_Manipal/status/2090688741627285837 | AIC-MUJ Pitch Fest and Incubation Week [16] | None visible [16] |
| Aug 24, 2026 | https://x.com/Jaipur_Manipal/status/2091866801852613107 | Two-day AICTE-CTE Secure Cloud and DevOps training using Microsoft Azure [14] | Security-themed education content, not a portal incident [14] |

The Aug 24 post is the closest security-related X result, but its subject is training. It describes cloud fundamentals, Azure security, CI/CD pipelines, hands-on sessions, and certificates [14]. **Inference:** the post indicates public institutional interest in cloud-security education, but it does not establish that the MUJ SLCM platform uses Azure, that the SLCM host was discussed, or that any vulnerability was found.

The account itself is useful for future monitoring, but account-level relevance should not be confused with post-level relevance. An official university account can publish admissions, cultural, academic, and technology-training content without mentioning student services. The four identified URLs should therefore be retained as provenance and excluded from an incident chronology.

## Portal Identity and Relationship to Manipal Services

The target host's own visible content is concise. It says `WELCOME TO MUJ PORTAL` and exposes a sign-in path and parent-login label [4]. The alternate hostname also says `WELCOME TO MUJ PORTAL` and displays the `@jaipur.manipal.edu` identity [3]. These facts establish how the service presents itself publicly, but they do not establish whether all hostnames are active aliases, whether they share infrastructure, or whether the alternate path is a historical configuration.

The official MUJ FAQ is more probative. It names `https://mujslcm.jaipur.manipal.edu/` as the registration link [17]. It also instructs users who cannot log in to recheck credentials and, if the issue remains, contact `dms@jaipur.manipal.edu` or `ams@jaipur.manipal.edu` [17]. Because this material is hosted on the official MUJ domain, it supports the conclusion that the target hostname is an institutionally referenced SLCM service, rather than an unrelated imitation.

The official MUJ site identifies Manipal University Jaipur and lists it among the Manipal group universities [8]. It describes undergraduate, postgraduate, and doctoral offerings and publishes links including timetable, academic rules, degree verification, and online courses [8]. The site also lists an academic contact and the `ams@jaipur.manipal.edu` address in its contacts material. These pages provide organizational context and a route for responsible reporting.

A potential naming trap is that the official MAHE student-portal page points to `https://sis.manipal.edu/index.aspx` [12]. That destination is not the MUJ SLCM hostname. **Inference:** "Manipal student portal," "MAHE SIS," "MUJ portal," and "MUJ Online" should be treated as separate service labels until an official source explicitly maps them. Combining them into one asset would create false attribution and could misdirect incident triage.

## Complaints and Service Reliability Signals

| Evidence date shown | Source URL | Public report | What it supports | What it does not support |
|---|---|---|---|---|
| 1y ago | https://www.reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue | User says the password shows an error despite believing it is correct [5] | A public login complaint existed | No verified outage, account lockout, root cause, or resolution |
| 1y ago | https://www.reddit.com/r/Manipal_Academics/comments/1lzf0ht/paid_my_fees_but_still_showing_as_pending_on_slcm | User reports payment deducted and receipt available while SLCM remained pending [2] | A public payment-status synchronization complaint existed | No proof of payment-system failure, data loss, or institutional incident; no resolution is shown [2] |

The Reddit evidence points to two different failure modes: authentication-state disagreement and payment-state disagreement. **Inference:** if representative, the first could reflect credential entry, identity synchronization, password changes, or normal account policy; the second could reflect reconciliation delay, payment gateway callback failure, manual posting delay, or a display defect. The sources do not identify which mechanism occurred, so these possibilities must not be reported as findings.

The official FAQ independently anticipates login problems and recommends re-verifying credentials before contacting the university [17]. This corroborates that login support is a recognized operational need, but it does not prove elevated incident frequency. The official notification page provides helpdesk contacts for assignment, project, and fee-payment issues [11] and lists dated notices on Sep 18, 2025, Nov 11, 2024, Mar 19, 2024, and Mar 22, 2023 [11]. The extracted page contains no outage or security-incident notice [11].

Relative dates create a precision limitation. Both Reddit pages show `1y ago`, not a calendar date [2][5]. The exact posting dates should therefore not be invented. A future monitoring pass should capture the page's canonical timestamp if publicly rendered, archive the page lawfully, and record the retrieval date.

## Public Screenshots and Interface Artifacts

The target portal page itself is an interface artifact: its visible title is `WELCOME TO MUJ PORTAL`, and the page presents sign-in and parent-login elements [4]. The alternate host presents the `@jaipur.manipal.edu` label [3]. These are reproducible public UI observations, not screenshots of an error state.

A Chrome Web Store listing for `Detain Shield` includes an item screenshot and says the extension works only on MUJ SLCM [10]. It describes an attendance calculation function and identifies the offering as intended for MUJ students [10]. A Firefox add-on called `SLCM Feedback Auto-Fill` describes automation of the feedback form on MUJ's SLCM portal and includes a preview of the extension [6].

| Artifact | Exact URL | Publicly visible screenshot or media signal | Claimed function | Security interpretation |
|---|---|---|---|---|
| MUJ portal landing page | https://mujslcm.jaipur.manipal.edu/ | Visible portal branding and login labels [4] | Portal sign-in | Identity evidence only; no vulnerability claim |
| Detain Shield | https://chromewebstore.google.com/detail/detain-shield/mjedocjcijmphjgbfnkpceiblklpalpp | Item media 1 is identified as a screenshot [10] | Attendance calculation for MUJ SLCM [10] | Review publisher, permissions, and data practices before use |
| SLCM Feedback Auto-Fill | https://addons.mozilla.org/en-US/firefox/addon/slcm-feedback-auto-fill/ | Preview is identified [6] | Automates feedback-form filling [6] | Requests access to data for all websites [6], which is broad |

The Firefox listing states that the add-on requires access to data for all websites [6]. That is not proof of abuse; it is a permission-scope fact that should inform student safety guidance. The Chrome listing says website content is handled and reports that data is not sold to third parties outside approved use cases and is not used for unrelated purposes [10]. These are publisher disclosures, not independent audits.

A responsible security club should avoid installing unreviewed extensions on accounts used for university services. The safe conclusion is not "the extensions are malicious." The safe conclusion is that extensions with broad browser permissions create an additional trust boundary and should be assessed through publisher identity, source availability, update history, permission minimization, and institutional approval.

## Public Academic-Record and Data-Handling Signals

Search results surfaced public Scribd pages whose titles encode MUJ SLCM academic paths. One page is titled `2025 Grade Sheet for Courses` and says the grade sheet lists courses from the January-May 2025 academic session [18]. Another page is titled `BTech Computer Science Transcript 2026`, and the search description identifies it as a transcript-related artifact derived from a MUJ SLCM path.

This is a sensitive finding because academic records can contain personal data. However, the evidence does not establish how the documents became public, whether the records were intentionally uploaded, whether they were indexed from a misconfigured page, or whether the documents were synthetic or redacted. **Inference:** the safest risk label is "publicly indexed academic-record artifact requiring provenance review," not "MUJ breach." The report intentionally omits student names, grades, registration numbers, and other personal data.

The correct response for a university security club is preservation without redistribution. Record the exact public URL, retrieval date, page title, and high-level data category. Do not download, mirror, search for additional student records, attempt to enumerate URLs, or share personal data in club channels. Report the minimum necessary facts to the university through an official contact. The official MUJ contacts include `ams@jaipur.manipal.edu` and academic contacts listed on the university contact page.

The existence of a public academic document also does not demonstrate that the underlying portal is insecure. A user may have intentionally uploaded a document; a search engine may have indexed a public sharing page; a document could have been posted by an unrelated party; or an access-control failure could have occurred. Attribution requires evidence that the portal itself made the document available without authorization.

## Security Mentions, Infrastructure Claims, and What Remains Unverified

The requested brief supplied an architecture description: ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10 behind Akamai, and Microsoft 365 identity. This report did not independently confirm those technologies from a public source. The portal's visible page and official FAQ establish branding and institutional reference, not server headers, framework versions, CDN topology, or authentication protocol. Therefore, the stack should be retained as a research hypothesis or supplied input, not presented as an OSINT finding.

The retrieved security searches produced no MUJ-specific authoritative breach report, CVE record, or institutional disclosure. They returned generic security resources such as CISA's Known Exploited Vulnerabilities catalog and the CVE reference site, neither of which identified the MUJ host in the visible result [41, 42]. They also returned unrelated breach stories and unrelated `MuJS` software results. Those were excluded.

A public GitHub repository called `muj_slcm` was created on July 13, 2025 and showed zero stars, zero forks, and one commit in the retrieved page [7]. The analyzed content did not state official affiliation [7]. Another repository, `SLCM-api`, is described as making a login request to `slcm.manipal.edu` and fetching basic user data. **Inference:** these projects demonstrate community interest and possible automation around Manipal SLCM, but they do not establish a vulnerability, institutional authorization, or safe handling of credentials.

A separate public page advertises `MUJStella` and explicitly says it is an independent student platform not affiliated with Manipal University Jaipur [22]. An Arcadia page calls itself a Web3 MUJ SLCM project and includes a wallet connection [23]. These claims are important for asset attribution: a MUJ-branded or MUJ-referencing site is not automatically an official university service. Students should verify the domain and affiliation before entering any identity or academic information.

## Risk Register and Defensive Priorities

| Priority | Evidence-backed issue | Confidence | Safe defensive action |
|---|---|---|---|
| High | Public academic-record artifacts reference MUJ SLCM-derived paths [18] | Medium | Report URLs and data categories to MUJ; do not redistribute records |
| High | Broad browser permission in feedback automation extension [6] | High | Avoid deployment on university accounts unless reviewed and approved |
| Medium | Public login complaint [5] | High for the complaint, low for root cause | Track exact dates and affected function through official support |
| Medium | Fee status reported pending after payment [2] | High for the report, low for root cause | Preserve receipt privately and use official finance/helpdesk channels |
| Medium | Multiple MUJ SLCM-related unofficial projects [7][22][23] | High for existence, low for safety | Separate official from unofficial domains and review provenance |
| Low | X search coverage gap | High for the retrieval limitation | Repeat monitoring with authenticated, policy-compliant public access and lawful archives |
| Unverified | ASP.NET MVC/.NET/IIS/Akamai/Microsoft 365 stack in the brief | Low | Confirm only through authorized asset inventory or official documentation |
| Unverified | MUJ SLCM breach or exploitable vulnerability | Low | Do not claim an incident without institutional or reproducible authorized evidence |

The most actionable concern is not an alleged exploit. It is information governance: public academic artifacts and unofficial browser integrations can place sensitive student data at risk even when there is no confirmed compromise. The club should prioritize responsible disclosure, domain verification, permission review, and careful evidence minimization.

## Monitoring Plan for a University Security Club

| Monitoring objective | Public source | Collection record | Stop condition |
|---|---|---|---|
| X keyword monitoring | X search URLs for the four target terms | Query, URL, timestamp, visible author, post date, screenshot indicator | Stop at login wall or non-public content; do not bypass |
| Official incident monitoring | MUJ notices and official contact pages | Page title, publication date, incident wording, exact URL | Do not infer an incident from page unavailability |
| Complaint monitoring | Public Reddit and other student forums | Relative or absolute date, symptom, resolution status | Do not collect credentials or personal identifiers |
| Artifact monitoring | Extension stores, public repositories, document hosts | Publisher, permissions, update date, public description | Do not install or execute unreviewed code on university accounts |
| Data-exposure triage | Publicly indexed document pages | URL, category, minimal proof, retrieval date | Do not download, enumerate, mirror, or redistribute records |

For X, the club should maintain a distinction between a search-page observation and a tweet observation. A tweet record should contain the canonical post URL, handle, visible date, exact text, media indicator, and relevance classification. If the page only exposes an authentication shell, record `not visible` rather than filling fields from snippets or assumptions.

For complaints, the club should normalize relative dates only when a reliable page timestamp is available. In this pass, `1y ago` is preserved as `1y ago` [2][5]. Converting it into a month or year would be fabricated precision. The same rule applies to outage duration, number of affected users, and any claimed security impact.

For responsible disclosure, use official university contacts. The MUJ FAQ lists `dms@jaipur.manipal.edu` and `ams@jaipur.manipal.edu` for unresolved login issues [17], and the official contact page lists academic and administrative contacts. A report should contain the minimum reproducible description, exact public URL, timestamps, impact category, and a statement that no unauthorized access was attempted.

## Synthesis

The evidence separates into three layers. The first is official identity: the MUJ SLCM hostname is explicitly named in the official FAQ [17], and the portal brands itself as MUJ Portal [4]. The second is operational friction: public users report login rejection and fee-status inconsistency [5][2]. The third is ecosystem complexity: extensions, repositories, public record pages, and independent platforms reference SLCM [6][7][22].

The layers have different evidentiary strength and different risks. Official pages are strongest for attribution but weak for incident history. User complaints are strong evidence that someone experienced a symptom but weak for root cause. Third-party artifacts are strong evidence that an ecosystem exists but weak for institutional authorization or security. Treating all three as equivalent would produce either overclaiming or missed risk.

The X findings add a fourth distinction: account relevance is not incident relevance. The @Jaipur_Manipal posts include campus events and a secure-cloud training announcement [14][15][13][16], but no SLCM outage or portal-security report. Direct target searches exposed no qualifying tweet content [9]. Thus X currently provides a monitoring lead, not a verified incident record.

The largest non-obvious tension is between public usability and public exposure. The portal needs visible login and support pathways, while academic documents and browser extensions can create additional exposure outside the core service. **Inference:** the practical risk surface may be broader than the portal host itself, but the current evidence cannot rank those components without authorized telemetry, official asset ownership, and provenance analysis.

A second tension concerns security language. The Aug 24 X post uses terms such as secure cloud and Azure security [14], while the target portal's actual architecture remains unverified. **Inference:** institutional cybersecurity education should not be used as evidence of a particular production deployment. The correct action is to ask the institution for an authorized architecture map rather than infer one from marketing or training language.

A third tension concerns automation. Student tools may improve attendance calculations or reduce repetitive feedback entry [10][6], but broad permissions can increase account and data exposure [6]. The recommendation is proportional review, not blanket prohibition: verify publisher, minimize permissions, avoid sensitive accounts, and obtain institutional approval.

## VERDICT

**Overall confidence: Moderate for portal attribution and public service-friction signals; low for any claim of X-based outage evidence, breach, or exploitable vulnerability.**

1. **MUJ SLCM attribution: High confidence.** The official FAQ names the target URL as the SLCM registration link [17], and the host brands itself `WELCOME TO MUJ PORTAL` [4].
2. **Public login and fee-status complaints: High confidence that the reports exist; low confidence regarding cause or scale.** The Reddit pages state the symptoms, but both use a relative date and neither supplies an independently verified resolution [2][5].
3. **X outage/security evidence: Low confidence and currently unsubstantiated.** Direct search pages did not expose qualifying tweet-level content [9], and the four MUJ-specific post URLs located by indexing concern unrelated university activities [14][15][13][16].
4. **Public academic-record exposure signal: Medium confidence as an indexing/provenance concern, not as a breach.** A public grade-sheet page describes January-May 2025 records [18], but the available evidence does not establish how the document became public or whether the portal caused the exposure.
5. **Technology stack: Low confidence from this research.** ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 identity were supplied as input but were not independently established by the retrieved public sources. They must not be reported as verified findings.
6. **Recommended posture: Responsible disclosure and evidence minimization.** Preserve exact URLs and timestamps, avoid credentials and personal data, do not install or execute unreviewed integrations on university accounts, and route suspected exposure to official MUJ contacts [17].

### References with exact URLs

| Reference | Exact URL | Evidence used |
|---|---|---|
| MUJ SLCM portal | https://mujslcm.jaipur.manipal.edu/ | Portal branding and login labels [4] |
| Alternate MUJ SLCM hostname | https://muj.slcm.jaipur.manipal.edu/ | MUJ branding and `@jaipur.manipal.edu` label [3] |
| Official SLCM FAQ | https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf | Registration link and support contacts [17] |
| Official MUJ site | https://jaipur.manipal.edu/ | University identity and service links [8] |
| Official MUJ contact page | http://jaipur.manipal.edu/contact-university.php | Academic and administrative contacts |
| Official MUJ notices | https://muj.onlinemanipal.com/notifications | Dated notices and helpdesk information [11] |
| MAHE student portal page | https://www.manipal.edu/mu/academics/student-portal.html | Separate SIS destination [12] |
| X search: mujslcm | https://x.com/search?q=mujslcm&src=typed_query | Search-page limitation [19] |
| X search: slcm.manipal | https://x.com/search?q=slcm.manipal&src=typed_query | Search-page limitation [20] |
| X search: Manipal portal | https://x.com/search?q=Manipal%20portal&src=typed_query | Search-page limitation [9] |
| X search: MUJ portal | https://x.com/search?q=MUJ%20portal&src=typed_query | Search-page limitation [21] |
| MUJ X post, Aug 15, 2026 | https://x.com/Jaipur_Manipal/status/2088634410635759649 | Campus celebration [15] |
| MUJ X post, Aug 18, 2026 | https://x.com/Jaipur_Manipal/status/2089600565877821835 | Culinary workshop [13] |
| MUJ X post, Aug 21, 2026 | https://x.com/Jaipur_Manipal/status/2090688741627285837 | Pitch Fest [16] |
| MUJ X post, Aug 24, 2026 | https://x.com/Jaipur_Manipal/status/2091866801852613107 | Secure-cloud training [14] |
| Reddit login complaint | https://www.reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue | Password error report [5] |
| Reddit fee complaint | https://www.reddit.com/r/Manipal_Academics/comments/1lzf0ht/paid_my_fees_but_still_showing_as_pending_on_slcm | Pending fee status report [2] |
| Firefox extension | https://addons.mozilla.org/en-US/firefox/addon/slcm-feedback-auto-fill/ | SLCM automation and broad permission [6] |
| Chrome extension | https://chromewebstore.google.com/detail/detain-shield/mjedocjcijmphjgbfnkpceiblklpalpp | MUJ SLCM scope and screenshot marker [10] |
| GitHub repository | https://github.com/Anushkakumar10/muj_slcm | Creation date and low activity [7] |
| MUJStella | https://mujstella.in/ | Independent, non-affiliated platform claim [22] |
| Public grade-sheet page | https://www.scribd.com/document/983177245/Https-Mujslcm-jaipur-manipal-edustudentAcademicGradesForStudent | January-May 2025 academic-record description [18] |

## References

1. *Jaipur Manipal*. https://x.com/Jaipur_Manipal
2. *Reddit - The heart of the internet*. https://www.reddit.com/r/Manipal_Academics/comments/1lzf0ht/paid_my_fees_but_still_showing_as_pending_on_slcm
3. *Manipal University*. https://muj.slcm.jaipur.manipal.edu/
4. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
5. *Reddit - The heart of the internet*. https://www.reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue
6. *SLCM Feedback Auto-Fill – Get this Extension for 🦊 Firefox (en-US)*. https://addons.mozilla.org/en-US/firefox/addon/slcm-feedback-auto-fill/
7. *GitHub - Anushkakumar10/muj_slcm · GitHub*. https://github.com/Anushkakumar10/muj_slcm
8. *Manipal University Jaipur - 71 years of legacy of Manipal Education*. https://jaipur.manipal.edu/
9. *x.com*. https://x.com/search?q=Manipal%20portal&src=typed_query
10. *Detain Shield - Chrome Web Store*. https://chromewebstore.google.com/detail/detain-shield/mjedocjcijmphjgbfnkpceiblklpalpp
11. *Notices - MUJ*. https://muj.onlinemanipal.com/notifications
12. *Student Portal Login- MAHE (Manipal Academy Of Higher Education)*. https://www.manipal.edu/mu/academics/student-portal.html
13. [Manipal Jaipur on X: "Interns from Oman, Austria, Iran, Palestine &amp; Jordan cooked up their culinary heritage at IAESTE MUJ's Culinary Workshop, with MUJ Leadership joining in to taste the flavours!
The best way to understand a culture? Taste it.
#IAESTEMUJ #ManipalUniversityJaipur #CulinaryWork… / X](https://x.com/Jaipur_Manipal/status/2089600565877821835)
14. [Manipal Jaipur on X: "TECHNOVATE Hub wrapped up!  
2-day AICTE-CTE training on Secure Cloud &amp; DevOps using Microsoft Azure, covering Cloud fundamentals, Azure security, CI/CD pipelines &amp; more, with hands-on sessions + certificates for participants. 
#MUJ #TECHNOVATEHub #MicrosoftAzure #Clou… / X](https://x.com/Jaipur_Manipal/status/2091866801852613107)
15. [Manipal Jaipur on X: "Glimpses of the 80th Independence Day celebrations at Manipal University Jaipur! 🇮🇳✨

A day filled with pride, patriotism and the spirit of togetherness as the MUJ community came together to celebrate the journey of our nation and the promise of a brighter tomorrow.

#MUJ" / X](https://x.com/Jaipur_Manipal/status/2088634410635759649)
16. [Manipal Jaipur on X: "Pitch Fest: Incubation Week 6.0 wraps up at AIC-MUJ!
70+ startup registrations | 25+ selected for Pre-Incubation
Congratulations to all selected startups, here's to turning ideas into innovation, and innovation into impact! 💡
#AICMUJ #IncubationWeek6 #ManipalUniversityJaipur" / X](https://x.com/Jaipur_Manipal/status/2090688741627285837)
17. *Frequently Asked Questions and Contacts for SLCM Registration*. https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf
18. *2025 Grade Sheet for Courses | PDF*. https://www.scribd.com/document/983177245/Https-Mujslcm-jaipur-manipal-edustudentAcademicGradesForStudent
19. *X. It’s what’s happening / X*. https://x.com/search?q=mujslcm&src=typed_query
20. *x.com*. https://x.com/search?q=slcm.manipal&src=typed_query
21. *x.com*. https://x.com/search?q=MUJ%20portal&src=typed_query
22. *MUJStella - Student Platform for Manipal University Jaipur*. https://mujstella.in/
23. *MUJ SLCM*. https://arcadiaslcm.vercel.app/
