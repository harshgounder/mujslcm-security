# Digest: w2g-13-telegram-discord.md

## REPORT
Source file: w2g-13-telegram-discord.md. Public community risk map for MUJ SLCM and adjacent LMS: Telegram, Discord, Reddit, official MUJ pages, and general threat-intelligence context. Public-only review; no joining groups, no portal authentication, no credential testing. 25 references.

## ANSWER SUMMARY
- Verdict: Moderate confidence for the public ecosystem map; High that public MUJ-branded community listings and isolated public SLCM problem reports exist; Low for any leak, credential-sharing, compromise, or stack-attribution conclusion.
- Telegram: direct page for @manipaljaipurfresher shows "Manipal University Jaipur", a "MUJ Freshers group", 447 members and 7 online; a Telemetrio page for the apparent same handle shows 1,572 subscribers and a restricted-by-Telegram status. Counts are treated as time- and source-dependent; the report refuses to average or reconcile them.
- Discord: invite 7a5D7KKNFf shows "Manipal Jaipur" with 1,142 members and 27 online; invite manipal-university-jaipur-1008377907057545269 shows "Manipal University Jaipur" with 1,902 members and 32 online and an official-sounding listing title; discord.do describes a student-made community with department-wise study channels, voice channels, a cafeteria, fun zone, and peer discussion. No university endorsement is confirmed for any server.
- Portal friction: two deleted-author Reddit posts: r/Manipal_Academics "Slcm login" (old and new registration numbers both rejected after an intra-sliding update) and r/manipaljaipur "Slcm portal issue" (password error despite the poster believing it correct). Archived posts, no verified resolution.
- Official support path: the SLCM FAQ directs AMS login trouble to re-verify credentials then contact institutional DMS or AMS support, with a separate Outlook-account troubleshooting path. The FAQ's credential-format example is deliberately omitted by the report.
- Leak status: "not located in the reviewed public corpus" for leaked SLCM screenshots, credential dumps, or credential-sharing conversations. The urlscan "Live Screenshot" is a scanner interface feature, not leak evidence; urlscan states it does not manage the displayed sites.
- Stack claims (ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai, M365) remain unverified requester-supplied hypotheses; the FAQ's Outlook references provide context only.
- General infostealer and identity-risk sources (flare.io, Constella, Have I Been Pwned) explain threat mechanisms but attribute nothing to MUJ.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/ - public portal page; sign-in and parent-login options with an @muj.manipal.edu label.
- https://muj.slcm.jaipur.manipal.edu/ - alternate public rendering with an @jaipur.manipal.edu identity label.
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - official FAQ: registration link, AMS login re-verify step, DMS or AMS support, separate Outlook troubleshooting path.
- https://t.me/manipaljaipurfresher - direct Telegram landing page; MUJ Freshers group, 447 members, 7 online.
- https://telemetr.io/en/channels/1394408318-manipaljaipurfresher - Telemetrio directory for the same apparent handle; 1,572 subscribers, channel restricted by Telegram; visible rows are welcome/general topics.
- https://discord.com/invite/7a5D7KKNFf - public invite page; "Manipal Jaipur", 1,142 members, 27 online.
- https://discord.com/invite/manipal-university-jaipur-1008377907057545269 - public invite page; "Manipal University Jaipur", 1,902 members, 32 online.
- https://discord.do/manipal-university-jaipur/ - directory description: student-made community, study and voice channels, peer discussion.
- https://www.reddit.com/r/Manipal_Academics/comments/1993mdc/slcm_login - archived post, deleted author; old and new registration numbers rejected after an intra-sliding update.
- https://www.reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue - deleted-author report of a password error despite believed-correct password.
- https://urlscan.io/domain/mujslcm.jaipur.manipal.edu - passive scan page; scanner metadata only, disclaims management of displayed sites.
- https://muj.onlinemanipal.com/ - Online Manipal LMS description (e-tutorials, virtual labs, e-libraries); adjacent service context, not proof of shared backend.
- https://www.d2l.com/en-in/why-d2l/customers/manipal-university-jaipur-online - D2L customer page naming MUJ Online as an LMS context.
- http://flare.io/flare-data-explorer/stealer-logs - general infostealer capability (credentials, session cookies, screenshots); threat model, not MUJ evidence.
- http://haveibeenpwned.com/API/v3 - general breach/stealer-log context; no MUJ-specific record cited.

## ACTIONABLE LEADS
- Governance confirmation: ask community administrators for public moderation and reporting statements; publish an official recognized-channel directory and a policy that all other groups are independent unless confirmed.
- Anti-phishing messaging: state across SLCM, Outlook onboarding, LMS pages, and official social accounts that staff never need passwords, OTPs, cookies, or private screenshots; provide a report address and push official password-reset flows.
- Registration-change messaging: give students a controlled status message naming the active identifier, expected synchronization timing, and the owning official unit (triggered by the reg-number rejection report).
- Incident-validation protocol for future leak claims: preserve public URL, timestamp, channel name, redacted description; escalate to university security and legal contacts; ask platforms to preserve or remove material; publish only confirmed facts.
- Evidence ledger discipline: record source type, timestamp, confidence, redaction status; do not merge divergent Telegram counts or the two Discord invite counts.
- Passive surface check: the urlscan domain page can be reviewed for scan history and subdomain results as an authorized passive step only.
- Direct support routing: point students to FAQ DMS/AMS escalation instead of crowdsourced password exchange.

## FLAGS
- Membership counts diverge across sources (447 direct vs 1,572 directory; a nearGroups entry shows 3,903 members and 55 online without a matching handle). The report explicitly forbids averaging or assuming identity; the nearGroups entry is not used as a third count.
- The two Discord invite pages may be different servers or overlapping communities; nothing proves they are the same object, so counts are not added.
- Reddit posts are deleted-author, archived user reports; they prove reports, not systemic outage, password validity, or compromise.
- "Official Public Listed Community of MUJ Students" is a self-description; no MUJ institutional page confirms sponsorship or operation.
- The urlscan screenshot feature is scanner UI; the page itself says displayed websites are not managed by urlscan. Treating it as a leaked screenshot would be a category error.
- The FAQ's credential-related example and Outlook identity reference are omitted from the report; do not reconstruct or reproduce them.
- Infostealer, Constella, and HIBP material is general context with no MUJ attribution; a public leak claim would still need provenance, date, affected service, and institutional validation.
- The supplied technical stack remains requester-supplied hypothesis; no verified version, CDN, or identity architecture appears in the reviewed evidence.

## COVERAGE
- File: w2g-13-telegram-discord.md.
- 334 lines total; 52,591 bytes on disk; 52,583 chars read.
- Method: read_file offset 1, limit 2000, single call.
- EOF confirmed: final call returned truncated: false, last content line 334 equals total_lines 334.