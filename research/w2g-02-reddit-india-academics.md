# Reddit OSINT Findings for the MUJ SLCM Ecosystem

## Executive Summary

This report presents a public-information review of Reddit discussions relevant to a university security club studying the MUJ SLCM ecosystem. The requested communities were r/Indian_Academia and r/developersIndia. The review looked for Manipal University, Manipal University Jaipur, MUJ, SLCM, student portals, admissions portals, login failures, privacy complaints, identity misuse, CAPTCHA, OTP, authentication, and related security language. The report does not test mujslcm.jaipur.manipal.edu, does not attempt authentication, does not reproduce an exploit, and does not treat a Reddit allegation as a confirmed vulnerability.

The most important result is negative but carefully bounded: the public subreddit searches reviewed did not yield a confirmed MUJ SLCM incident in either named community. The Manipal-related results were education-choice or course discussions. In r/Indian_Academia, the Manipal search included a 2021 comparison post and multiple 2026 education discussions, including a refund complaint about Manipal Online, but no identified portal or SLCM security complaint [28]. In r/developersIndia, the exact Manipal result was an Online BCA education-choice discussion, not a portal or security report [27].

A separate MUJ SLCM login complaint was found in r/manipaljaipur, not in either requested subreddit. Its title was "Slcm portal issue" and the public extract describes a user whose password was being rejected despite believing it was correct [25]. This is relevant context for user experience and availability, but it must not be represented as evidence from r/Indian_Academia or r/developersIndia.

The strongest direct security item in the requested communities is an r/developersIndia post about the IITK B.Cyber admissions portal, Pingala. The author described client-side CAPTCHA validation and an OTP limit associated with a browser session, then stated that the issue was reported to IIT Kanpur and that the portal was patched with image-based CAPTCHA, server-side validation, and rate limits [34]. This is a user-reported observation and remediation claim, not an independently validated assessment of MUJ SLCM.

The generic Indian education-portal evidence is broader and more useful as a risk-theme set than as proof of a defect in MUJ SLCM. r/Indian_Academia contains reports of failed candidate login, repeated password rejection, broken uploads, inaccessible education records, Aadhaar account-integrity problems, and concerns about college application data being used for spam calls [35][33][53]. These reports support a defensive review of authentication recovery, identity binding, input validation, availability, privacy notices, and complaint handling. They do not establish that MUJ SLCM has any of those weaknesses.

### Decision-ready findings

- **No confirmed MUJ SLCM Reddit incident in scope**: Searches reviewed in both named communities produced no confirmed MUJ or SLCM portal-security result. Treat this as "not located in the reviewed public index," not as proof that no post exists [29][30].
- **Out-of-scope MUJ evidence exists**: r/manipaljaipur contains a public SLCM password-error complaint. It is useful for context but cannot be counted as evidence from the requested communities [25].
- **Manipal discussions are mostly education-choice discussions**: The named communities contain Manipal course, degree, and admissions discussions, including Online Manipal, but the reviewed results do not connect them to MUJ SLCM security [28][27].
- **Admissions portals are a recurring availability surface**: NATS, UGC NET, PMRC, Swayam, Vidyalaxmi, and scholarship portals appear in public complaints involving form coverage, login, upload, password, or status problems [35][33].
- **Identity integrity is a recurring concern**: One NATS post states that the author's Aadhaar had already been used to register on the portal and that this blocked an internship; another discusses concern over Aadhaar and PAN access in a college application flow [35][33].
- **The clearest security-specific case is IITK Pingala**: The post alleges client-side CAPTCHA validation and a per-browser OTP limit, and reports subsequent server-side validation and rate limiting after disclosure [34].
- **Privacy complaints are not automatically vulnerabilities**: A complaint that application data may lead to spam calls is a privacy allegation, not proof of a data sale or breach [53].
- **Operational implication**: MUJ SLCM defenders should use these public themes to review controls and user support, but only through authorized internal testing, documented permission, and responsible disclosure.

## Scope, Method, and Evidence Standard

The collection scope was deliberately narrow: public Reddit pages and public Reddit search feeds for r/Indian_Academia and r/developersIndia. Search variants included Manipal, MUJ, SLCM, portal, student portal, university portal, login, password, security, vulnerability, CAPTCHA, OTP, Aadhaar, privacy, hacked, and related education terms. Search-result pages and direct Reddit pages were read where available. Exact permalinks and timestamps are reported only where the public page or feed exposed them.

This is an OSINT report, not a penetration test. The evidence hierarchy is: first, an exact Reddit permalink with a visible title and date; second, a public Reddit search feed that supplies title, timestamp, permalink, and quote; third, a search result or page extract that identifies a topic but does not provide enough metadata for a full record. A Reddit post is a statement by a user. It is not a vendor confirmation, code review, vulnerability disclosure record, or proof of impact.

The requested "chain-of-thought" is not reproduced. Instead, this report provides an auditable reasoning summary: identify candidate posts, verify the subreddit and permalink, extract only the relevant public wording, classify the item, separate direct observation from inference, exclude unrelated or operationally dangerous content, and assign confidence. This preserves reviewability without exposing private internal reasoning.

The user-supplied technology description mentions ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 identity. The Reddit evidence reviewed here does not independently establish those implementation details. They are therefore treated as research context supplied by the requester, not as findings from Reddit. No claim below maps a Reddit complaint to a specific MUJ component unless the source itself does so.

## MUJ and Manipal Results in r/Indian_Academia

The r/Indian_Academia Manipal feed contains several education-related records. A 2021 post is titled "Factors to take into account, while choosing between VIT and Manipal, and my thoughts on the same" and is dated 2021-06-12T08:02:29+00:00. Its quoted text concerns choosing a college, not a portal [28]. A separate 2026 post asks about choosing Manipal MAHE over Delhi University, and another concerns Srishti Manipal's human-centred design program [28]. These records establish that the search can retrieve Manipal content, but they do not establish MUJ SLCM content.

A post titled "Manipal Online scammed me and refused to refund my money for 3 months" is dated 2026-06-10T01:59:46+00:00. The visible quote says, "It has now been over 6 months and I still have not received my money" [28]. This is a serious consumer-service allegation, but it is not a portal-security report. It should not be transformed into a claim about authentication, data exposure, or application security.

The exact SLCM search produced no result in r/Indian_Academia. The public API/search material reports zero results for the SLCM query, while the Manipal result set consists of education discussions and the refund complaint [29][15]. The correct OSINT wording is therefore: no MUJ SLCM post was located in the reviewed public r/Indian_Academia search results. The stronger wording "there are no such posts" is unsupported.

| Community | Search theme | Strongest located result | Date shown | Exact URL | Security relevance |
|---|---|---|---|---|---|
| r/Indian_Academia | Manipal | Factors to take into account, while choosing between VIT and Manipal | 2021-06-12 | https://www.reddit.com/r/Indian_Academia/comments/ny1o91/ysk_factors_to_take_into_account_while_choosing/ | Education choice, not security [28] |
| r/Indian_Academia | Manipal | I want to Decide between DU and Manipal. Which? | 2026-07-31 | https://www.reddit.com/r/Indian_Academia/comments/1vbjy64/i_want_to_decide_between_du_and_manipal_which/ | Education choice, not security [28] |
| r/Indian_Academia | Manipal Online | Manipal Online scammed me and refused to refund my money for 3 months | 2026-06-10 | https://www.reddit.com/r/Indian_Academia/comments/1u1osy9/manipal_online_scammed_me_and_refused_to_refund/ | Consumer-service allegation, not portal security [28] |
| r/Indian_Academia | SLCM | No exact SLCM result in reviewed feed | Not applicable | https://www.reddit.com/r/Indian_Academia/search.rss?q=SLCM&restrict_sr=1&sort=relevance&t=all | No result located [15] |

The table supports a narrow conclusion: r/Indian_Academia contains Manipal discussion, but the reviewed public evidence does not contain a verified MUJ SLCM security complaint. The absence result is an index limitation, not a statement about the entire Reddit archive.

## Manipal Results in r/developersIndia

The r/developersIndia Manipal feed similarly returns education-choice material rather than portal-security reporting. One record, dated 2026-07-11T01:51:53+00:00, is titled "Need advice regarding online Manipal university, look for advice." Its quote says, "I am considering the Online BCA from Manipal University Jaipur" [27]. The direct-page extraction classifies it as an education-choice discussion and reports no text about security, privacy, authentication, CAPTCHA, rate limiting, login, availability, or a software-project data surface [36].

Other retrieved records discuss a master's degree in Bangalore, including Manipal, or compare online degrees. The presence of Manipal as a college option is not evidence that a participant used MUJ SLCM or observed a defect. This distinction matters because search engines often match an institution name while omitting the technical subject being sought.

| Community | Thread | Date shown | Exact URL | Portal/security status |
|---|---|---|---|---|
| r/developersIndia | Need advice regarding online Manipal university, look for advice | 2026-07-11 | https://www.reddit.com/r/developersIndia/comments/1ut6xh8/need_advice_regarding_online_manipal_university/ | Online BCA education question; no portal-security content [27][36] |
| r/developersIndia | Should I do my Master's in Bangalore (RV, PES, Manipal, etc.) or wait for an opportunity abroad? | 2025-02-01 | https://www.reddit.com/r/developersIndia/comments/1iey3bg/should_i_do_my_masters_in_bangalore_rv_pes/ | Higher-education choice; no MUJ SLCM finding [27] |
| r/developersIndia | SLCM exact-search result | Not applicable | https://www.reddit.com/r/developersIndia/search.json?q=SLCM&restrict_sr=1&sort=relevance&t=all&raw_json=1 | Search material reported no exact relevant result [19] |

The practical implication is that the two named communities should not be described as having a public MUJ SLCM incident based on the reviewed evidence. A future researcher should preserve the exact search date, query, Reddit sorting mode, and permalink because Reddit indexing and visibility can change.

## The Out-of-Scope MUJ SLCM Login Complaint

The strongest direct MUJ SLCM lead is outside the requested communities. The r/manipaljaipur thread is titled "Slcm portal issue" and is displayed as "1y ago" in the extracted page. The result is associated with the MUJ SLCM portal and describes a password error despite the poster believing the password was correct [25]. The search result also describes it as an issue with SLCM portal login [25].

This item is useful because it demonstrates that a public user complaint about MUJ SLCM login exists somewhere on Reddit. It does not demonstrate a vulnerability. A rejected password can result from an incorrect password, account provisioning delay, synchronization failure, an expired account, a reset workflow problem, or a genuine application defect. The source does not provide enough evidence to distinguish those possibilities.

| Subreddit | Thread title | Displayed age | Exact URL | Portal named | Classification |
|---|---|---|---|---|---|
| r/manipaljaipur | Slcm portal issue | 1y ago | https://www.reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue | MUJ SLCM | Login/availability complaint; outside requested communities [25] |

**Inference label:** It is reasonable to infer that login reliability is a student-impacting concern worth monitoring because the post describes a password rejection. It is not reasonable to infer account takeover, weak password storage, authentication bypass, or a framework-specific defect from that statement alone.

## Generic r/Indian_Academia Portal Complaints

The generic searches produced a useful set of education and student-portal complaints. The UGC NET case is a dated candidate-login complaint. The post was published 2026-01-03T04:30:56+00:00 and states, "I am not able to login to the candidate portal for UGC NET Dec 2025" and that the website kept resetting the password while reporting, "Check password/application number and try again" [33]. The source classifies this as ordinary usability or account-access failure, not a confirmed security issue.

The PMRC post, published 2026-06-20T16:14:46+00:00, states that the website was "super buggy" and that uploads under the allowed size limit still generated an error. The quoted error includes an HTML response where JSON was expected [38]. That pattern can be a valuable defensive signal for error handling and input-validation review, but the public text does not prove exploitable injection, information disclosure, or server compromise.

The NATS cases illustrate two distinct risk classes. One r/Indian_Academia post, published 2025-09-24T17:42:34+00:00, says, "my Aadhaar has already been used to register on the NATS portal by someone else" and describes reporting to UIDAI, filing a PGPortal grievance, and contacting BOAT [51]. The classification is privacy/account integrity. It is not proof that NATS caused the registration or that a breach occurred. A separate NATS post says that the state/city dropdown contains only Indian options and has no path for schooling abroad [35]. That is an inclusivity and form-coverage problem, not a security finding.

| Date | Portal/institution | Exact URL | Verbatim public quote | Classification |
|---|---|---|---|---|
| 2026-01-03 | UGC NET candidate portal | https://www.reddit.com/r/Indian_Academia/comments/1q2l1f9/unable_to_candidate_login_to_download_admit_card/ | "I am not able to login to the candidate portal for UGC NET Dec 2025"; password reset message says "Check password/application number and try again" [33] | Availability/usability |
| 2026-06-20 | PMRC portal | https://www.reddit.com/r/Indian_Academia/comments/1ub0ira/pmrc_portal_is_full_of_bugs_and_does_not_work_help/ | "I tried all the formats under the allowed size limit but it keeps throwing this error" [38] | Upload/error-handling usability |
| 2025-09-24 | NATS portal and DRDO internship | https://www.reddit.com/r/Indian_Academia/comments/1npirgk/nats_portal_aadhaar_misuse_blocking_my_drdo/ | "my Aadhaar has already been used to register on the NATS portal by someone else" [51] | Account integrity/privacy complaint |
| 2026-05-03 | Government exam portal | https://www.reddit.com/r/Indian_Academia/comments/1t2e3jg/spent_hours_just_trying_to_get_my_photo_and/ | "Signature 'too large.' Portal timed out mid-fill." [35] | Availability/usability |
| 2025-10-22 | PM Vidyalaxmi | https://www.reddit.com/r/Indian_Academia/comments/1ocym4m/vidyalaxmi_portal_doesnt_have_my_institute_listed/ | The school and diploma institute were "not available to choose from" [35] | Form coverage/availability |
| 2024-05-14 | Swayam/NTA | https://www.reddit.com/r/Indian_Academia/comments/1crm5bh/swayam_portal_nta_hall_ticket_download/ | "I am unable to navigate through the website" [35] | Availability/usability |

A separate privacy discussion about college applications says, "privacy concerns have become a huge issue," describes random spam calls after applications, and alleges, "That's your data being sold" [53]. The first two statements are user-reported concerns. The last is an allegation, not a verified finding. A security club should record the distinction and avoid repeating the allegation as fact.

## Generic r/developersIndia Security and Portal Evidence

The IITK B.Cyber case is the most technically specific item in the requested communities. The post is titled "Ironically the IITK BCyber application portal (pingala) had practically non-existent CAPTCHA" and was published 2026-06-26T11:06:57+00:00. The author wrote that a jQuery plugin generated a character matrix CAPTCHA visible in the DOM and that validation was client-side. The author also claimed that the OTP limit was tied to a browser session [34].

The author further stated, "Reported the vulnerability along with the scripts to IITK and is patched with image-based captcha with server side validation and ratelimits" [34]. This is a responsible-disclosure and remediation narrative as presented by the poster. The public page does not independently prove the before-and-after state, the exact severity, or the number of requests involved. The safe conclusion is that a developer-community user reported a weakness in an education admissions portal and reported a remediation outcome.

| Date | Portal | Exact URL | Public quote or summary | Classification |
|---|---|---|---|---|
| 2026-06-26 | IITK B.Cyber application portal, Pingala | https://www.reddit.com/r/developersIndia/comments/1ug3qpw/ironically_the_iitk_bcyber_application_portal/ | "validated, both client side"; the author says the issue was reported and patched with server-side validation and rate limits [34] | Direct user-reported security observation |
| 2026-08-14 | NATS Portal | https://www.reddit.com/r/developersIndia/comments/1vnxop3/nats_portal_no_statecity_option_for_102_schooling/ | "there's no option for schooling done abroad" [37] | Form coverage/usability |
| 2026-05-19 | Training management portal project | https://www.reddit.com/r/developersIndia/comments/1thkn7s/i_just_built_an_entire_endtoend_enterprise_level/ | The post describes building an end-to-end training management portal [6] | Context only, not an incident |
| 2024-04-25 | IPU Senpai university result portal project | https://www.reddit.com/r/developersIndia/comments/1cv6qy3/built_this_result_portal_for_my_university/ | The author describes a parser, ETL pipeline, PostgreSQL database, and REST API for raw results [22] | Contextual architecture discussion, not a vulnerability |

The result-portal project is relevant as a design-context case, not as a MUJ finding. The author describes processing 50k-plus PDF pages and 1,200-plus PDFs into a PostgreSQL database, then exposing results through an ASP.NET Core and Dapper REST API [22]. That demonstrates the kinds of data pipelines student-result systems may involve. It does not establish that MUJ SLCM uses the same architecture, and it does not establish unauthorized access or exposure.

A TCS thread discusses an employment portal and an alleged way candidates viewed status codes through inspectable page code [21]. It is excluded from the education-portal evidence set because TCS NQT is a recruitment process. It may be a useful generic lesson about client-visible status logic, but it should not be counted as a university or student SLCM incident.

## Defensive Implications for a University Security Club

The Reddit evidence suggests a review matrix, not a vulnerability list. First, authentication and recovery deserve attention because students report password resets, invalid credentials, and rejected logins across public education services [33]. An authorized review should verify that reset tokens expire, that error messages do not unnecessarily reveal account state, that rate limits apply server-side, and that support staff have a documented identity-verification process. These are defensive recommendations, not claims about MUJ SLCM.

Second, identity binding should be treated as a distinct control. The NATS Aadhaar complaint shows the user impact when a government identity is already associated with another registration [51]. The application-security question is not merely whether an identifier is unique. It is whether the system provides a safe dispute, unlink, re-verification, audit, and escalation path without exposing identity data to unauthorized parties. No one should attempt to test this on MUJ SLCM without written authorization.

Third, CAPTCHA and OTP controls should be enforced at the server and tied to an appropriate risk model. The IITK Pingala post specifically contrasts client-side validation with reported server-side validation and rate limits after disclosure [34]. The transferable lesson is defensive: a client-visible control should not be the sole enforcement point. The report does not claim that MUJ SLCM has a comparable weakness.

Fourth, error handling and upload workflows deserve review. PMRC users reported that an upload generated an HTML-as-JSON error even when the file was under the stated size limit [38]. A safe internal review would confirm consistent content types, bounded upload size, file-type validation, malware scanning, safe storage, non-sensitive error messages, and resilience under ordinary load. These are general control objectives inferred from the complaint pattern, not observations of MUJ SLCM.

Fifth, privacy communication should be tested from the student's perspective. The college-application discussion raises concern about downstream spam calls and alleged data sharing [53], while the Mithibai-related discussion raises concern about an application flow requesting access to Aadhaar and PAN cards [33]. The defensive response is to document purpose limitation, consent, retention, sharing, contact points, and withdrawal or correction paths. The Reddit posts do not prove unlawful processing or data sale.

## Limitations and Confidence

Reddit search is not a complete archive. Results may be affected by indexing, ranking, deleted posts, removed comments, private communities, rate limits, spelling variants, and pages that expose only partial text. Some feed results supplied exact timestamps and permalinks, while other search results exposed only titles or approximate ages. The report therefore distinguishes "not located" from "does not exist."

The MUJ conclusion has moderate confidence for the reviewed public search surface and low confidence as a statement about all historical Reddit content. The generic portal themes have high confidence as a record of what the cited users wrote, but low confidence as a measure of prevalence or as proof of technical root cause. The IITK case has moderate confidence as a user-reported security disclosure because the post gives a named portal, a date, technical description, and a claimed remediation, but it remains unindependently verified in this dataset.

| Finding | Evidence quality | Confidence | Reason |
|---|---|---|---|
| No MUJ/SLCM incident located in named subreddit searches | Search-feed and direct-search evidence | Moderate for reviewed index; low for universal absence | Search visibility is incomplete [29][15] |
| MUJ SLCM login complaint exists on Reddit outside requested communities | Direct r/manipaljaipur extract | Moderate | Exact title and public complaint are visible, but subreddit is out of scope [25] |
| Manipal posts in named communities are mainly education discussions | Dated RSS results and direct extraction | Moderate to high | Titles, dates, permalinks, and quotes are visible [28][27] |
| IITK Pingala CAPTCHA issue was reported and allegedly patched | Dated direct r/developersIndia post/feed | Moderate | Detailed user statement, but no independent validation [34] |
| Indian education portals show recurring access/privacy themes | Multiple dated Reddit records | High that users made these complaints; low for prevalence | Multiple examples, but self-selected anecdotal data [35][51][53] |

## Synthesis

Across the evidence, three dimensions diverge. First is scope: Manipal posts in the named communities concern choosing courses and institutions, while the only located MUJ SLCM login complaint is in a different Manipal subreddit [28][27][25]. Second is technical specificity: most r/Indian_Academia complaints describe availability, password, upload, or identity problems, whereas the IITK Pingala post discusses an alleged enforcement weakness and a claimed server-side remediation [33][38][34]. Third is evidentiary status: every item is user-generated, but some records expose exact dates and URLs while others are only search-result leads.

The non-obvious tension is that a high volume of ordinary usability complaints can coexist with very little explicit security language. A student who cannot log in may be experiencing a harmless provisioning issue, but the same failure domain can affect academic deadlines and support load. Conversely, a technically worded post about CAPTCHA may sound severe without proving exploitability or impact. The correct security-club posture is therefore to use public complaints as hypotheses for authorized review, not as proof of defects.

The strongest actionable comparison is between the out-of-scope MUJ login complaint and the in-scope IITK Pingala report. The MUJ item is a symptom report: a password was rejected. The Pingala item is a control report: the author describes where validation occurred and claims a remediation. They require different follow-up. The first suggests reviewing provisioning, reset, error handling, and support workflows. The second suggests reviewing server-side enforcement, rate limits, telemetry, and disclosure handling. Neither supports testing MUJ SLCM without permission.

The evidence also separates privacy from security. Aadhaar reuse, Aadhaar and PAN access concerns, and suspected spam calls are important account-integrity and privacy signals [51][33][53]. They are not automatically evidence of a breach. A university security club should preserve that distinction in every write-up, because overclaiming can harm students, institutions, and legitimate disclosure processes.

## VERDICT

**Verdict: No publicly confirmed MUJ SLCM security incident was located in the reviewed r/Indian_Academia or r/developersIndia material. Confidence: Moderate for the reviewed public Reddit search surface; low for a universal claim about all Reddit history.**

A relevant MUJ SLCM password/login complaint was located in r/manipaljaipur, outside the requested communities [25]. The requested communities do contain useful generic evidence: r/Indian_Academia shows login, upload, identity-integrity, and privacy complaints [33][35][51][53], while r/developersIndia contains the most technically specific education-portal security report, concerning IITK Pingala's CAPTCHA and OTP enforcement as described by the poster [34].

**Recommended disposition:** record the MUJ item as an out-of-scope user-experience lead; record the IITK item as a cross-portal defensive case study; record generic portal complaints as risk themes; and do not label MUJ SLCM vulnerable, exposed, breached, or exploitable without authorized testing and independent evidence. Any future technical assessment should be conducted only under written authorization, with minimal data access, no credential testing against real users, no bypass attempts, and responsible disclosure to the system owner.

## References

1. *Welcome to Reddit*. https://old.reddit.com/r/Indian_Academia/search?q=Manipal&restrict_sr=on&sort=relevance&t=all
2. *Reddit - The heart of the internet*. https://www.reddit.com/r/Indian_Academia/search/?q=portal&restrict_sr=1&sort=relevance&t=all
3. *Reddit - The heart of the internet*. https://www.reddit.com/r/developersIndia/search/?q=portal&restrict_sr=1&sort=relevance&t=all
4. *Reddit - The heart of the internet*. https://www.reddit.com/r/Indian_Academia/search/?q=Manipal&restrict_sr=1&sort=relevance&t=all
5. *Manipal - Reddit Search!*. https://www.reddit.com/r/developersIndia/search/?q=Manipal&restrict_sr=1&sort=relevance&t=all
6. *developersIndia: search results - portal*. https://old.reddit.com/r/developersIndia/search?q=portal&restrict_sr=on&sort=relevance&t=all
7. *Reddit - The heart of the internet*. https://www.reddit.com/r/developersIndia/search/?q=security&restrict_sr=1&sort=relevance&t=all
8. *Reddit - The heart of the internet*. https://www.reddit.com/r/Indian_Academia/search/?q=security&restrict_sr=1&sort=relevance&t=all
9. *vulnerability - Reddit Search!*. https://www.reddit.com/r/developersIndia/search/?q=vulnerability&restrict_sr=1&sort=relevance&t=all
10. *Reddit - The heart of the internet*. https://www.reddit.com/r/Indian_Academia/search/?q=login&restrict_sr=1&sort=relevance&t=all
11. *Reddit - The heart of the internet*. https://www.reddit.com/r/Indian_Academia/search/?q=college&restrict_sr=1&sort=relevance&t=all
12. *Reddit - The heart of the internet*. https://www.reddit.com/r/developersIndia/search/?q=college&restrict_sr=1&sort=relevance&t=all
13. *Reddit - The heart of the internet*. https://www.reddit.com/r/developersIndia/search/?q=student&restrict_sr=1&sort=relevance&t=all
14. *Reddit - The heart of the internet*. https://www.reddit.com/r/Indian_Academia/search/?q=student&restrict_sr=1&sort=relevance&t=all
15. *Indian Academia*. https://www.reddit.com/r/Indian_Academia/search.json?q=SLCM&restrict_sr=1&sort=relevance&t=all&raw_json=1
16. *reddit.com*. https://www.reddit.com/r/developersIndia/search.rss?q=security&restrict_sr=1&sort=relevance&t=all
17. *reddit.com*. https://www.reddit.com/r/developersIndia/search.json?q=security&restrict_sr=1&sort=relevance&t=all&raw_json=1
18. *reddit.com*. https://www.reddit.com/r/developersIndia/search.json?q=SLCM&restrict_sr=1&sort=relevance&t=all&raw_json=1
19. *Indian Academia*. https://www.reddit.com/r/Indian_Academia/search.json?q=security&restrict_sr=1&sort=relevance&t=all&raw_json=1
20. *reddit.com*. https://www.reddit.com/r/developersIndia/search.json?q=vulnerability&restrict_sr=1&sort=relevance&t=all&raw_json=1
21. *Reddit - The heart of the internet*. https://www.reddit.com/r/developersIndia/comments/1m4qbhe/is_tcs_candstatus_inspect_portal_code_trick_true/
22. *Reddit - The heart of the internet*. https://www.reddit.com/r/developersIndia/comments/1cv6qy3/built_this_result_portal_for_my_university/
23. *Reddit - The heart of the internet*. https://www.reddit.com/r/Indian_Academia/comments/jc80j0/what_happened_to_the_keam_2020_candidate_portal/
24. *Reddit - The heart of the internet*. https://www.reddit.com/r/developersIndia/comments/1ug3qpw/ironically_the_iitk_bcyber_application_portal/
25. *Reddit - The heart of the internet*. https://www.reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue
26. *reddit.com*. https://www.reddit.com/r/developersIndia/search.json?q=Manipal&restrict_sr=1&sort=relevance&t=all&raw_json=1
27. *reddit.com*. https://www.reddit.com/r/developersIndia/search.rss?q=Manipal&restrict_sr=1&sort=relevance&t=all
28. *Indian Academia*. https://www.reddit.com/r/Indian_Academia/search.rss?q=Manipal&restrict_sr=1&sort=relevance&t=all
29. *Indian Academia*. https://www.reddit.com/r/Indian_Academia/search.json?q=Manipal&restrict_sr=1&sort=relevance&t=all&raw_json=1
30. *Indian Academia*. https://www.reddit.com/r/Indian_Academia/search.json?q=login&restrict_sr=1&sort=relevance&t=all&raw_json=1
31. *Indian Academia*. https://www.reddit.com/r/Indian_Academia/search.json?q=portal&restrict_sr=1&sort=relevance&t=all&raw_json=1
32. *reddit.com*. https://www.reddit.com/r/developersIndia/search.json?q=portal&restrict_sr=1&sort=relevance&t=all&raw_json=1
33. *Indian Academia*. https://www.reddit.com/r/Indian_Academia/search.rss?q=login&restrict_sr=1&sort=relevance&t=all
34. *reddit.com*. https://www.reddit.com/r/developersIndia/search.rss?q=portal&restrict_sr=1&sort=relevance&t=all
35. *Indian Academia*. https://www.reddit.com/r/Indian_Academia/search.rss?q=portal&restrict_sr=1&sort=relevance&t=all
36. *Reddit - The heart of the internet*. https://www.reddit.com/r/developersIndia/comments/1ut6xh8/need_advice_regarding_online_manipal_university/
37. *reddit.com*. https://www.reddit.com/r/developersIndia/search.rss?q=student%20portal&restrict_sr=1&sort=relevance&t=all
38. *Reddit - The heart of the internet*. https://www.reddit.com/r/Indian_Academia/comments/1ub0ira/pmrc_portal_is_full_of_bugs_and_does_not_work_help/
39. [[deleted by user] : r/HairyAssGirls](https://www.reddit.com/r/Indian_Academia/comments/1t0q3l0/mospi_internship_what_is_the_status_of_group_a_and_group_b/)
40. *Reddit - The heart of the internet*. https://www.reddit.com/r/Indian_Academia/comments/1n9r9xf/reliance_foundation_scholarship_unable_to_login/
41. *Reddit - The heart of the internet*. https://www.reddit.com/r/Indian_Academia/comments/1q2l1f9/unable_to_candidate_login_to_download_admit_card/
42. *NATS portal Aadhaar misuse blocking my DRDO internship, how to resolve? : r/Indian_Academia*. https://www.reddit.com/r/Indian_Academia/comments/1npirgk/nats_portal_aadhaar_misuse_blocking_my_drdo/
43. *Reddit - The heart of the internet*. https://www.reddit.com/r/developersIndia/comments/1vnxop3/nats_portal_no_statecity_option_for_102_schooling/
44. *reddit.com*. https://www.reddit.com/r/developersIndia/search.rss?q=CAPTCHA&restrict_sr=1&sort=relevance&t=all
45. *Indian Academia*. https://www.reddit.com/r/Indian_Academia/search.rss?q=password&restrict_sr=1&sort=relevance&t=all
46. *Indian Academia*. https://www.reddit.com/r/Indian_Academia/search.rss?q=admission%20portal&restrict_sr=1&sort=relevance&t=all
47. *Indian Academia*. https://www.reddit.com/r/Indian_Academia/search.rss?q=CAPTCHA&restrict_sr=1&sort=relevance&t=all
48. *reddit.com*. https://www.reddit.com/r/developersIndia/search.rss?q=privacy&restrict_sr=1&sort=relevance&t=all
49. *reddit.com*. https://www.reddit.com/r/developersIndia/search.rss?q=OTP&restrict_sr=1&sort=relevance&t=all
50. *reddit.com*. https://www.reddit.com/r/developersIndia/search.rss?q=hacked&restrict_sr=1&sort=relevance&t=all
51. *Indian Academia*. https://www.reddit.com/r/Indian_Academia/search.rss?q=Aadhaar&restrict_sr=1&sort=relevance&t=all
52. *Indian Academia*. https://www.reddit.com/r/Indian_Academia/search.rss?q=OTP&restrict_sr=1&sort=relevance&t=all
53. *Indian Academia*. https://www.reddit.com/r/Indian_Academia/search.rss?q=privacy&restrict_sr=1&sort=relevance&t=all
54. *Indian Academia*. https://www.reddit.com/r/Indian_Academia/search.rss?q=hacked&restrict_sr=1&sort=relevance&t=all
55. *reddit.com*. https://www.reddit.com/r/developersIndia/search.rss?q=Aadhaar&restrict_sr=1&sort=relevance&t=all
