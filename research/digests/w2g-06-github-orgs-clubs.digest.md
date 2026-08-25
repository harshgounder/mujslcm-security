# Digest: w2g-06-github-orgs-clubs

## REPORT
Source file: w2g-06-github-orgs-clubs.md (MUJ SLCM Ecosystem: Public GitHub Intelligence and Defensive Findings)

## ANSWER SUMMARY
- Strongest direct SLCM artifact: DK10WS/SLCM_APP (SLCM SWITCH), a Flutter/Dart + FastAPI/Python app with student and parent login and retrieval of grades, GPA/CGPA, and attendance; 71 commits in snapshot, created Jun 18 2025. Authorization and deployment unresolved.
- Integration patterns are diverse: a mobile client, a Chrome extension (SlcmPlus with a MUJ SLCM host match), a SLCM+LMS aggregator (SlcmAndLms-aggregator), and server-side scrapers (Manipal The Talk App-Backend, SLCM-is-Dumb).
- CyberSpace Club and MUJ ACM are verified MUJ anchors via the official clubs page; their GitHub footprints are club web and education projects with no cited SLCM link.
- MUJ Central is a student-services portal candidate: OTP to an authorized Manipal ID, dashboard with attendance and timetable, resources, event registration; no explicit SLCM integration in the cited README.
- SLCM-is-Dumb documents automated login and captcha/OCR and warns contributors not to commit .env files; treat as credential-sensitive, review offline only.
- HackX3.0 is event infrastructure (official event website repo, 355 commits), not a participant submission; the IIC listing says GitHub links are optional.
- The supplied stack (ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai, M365) is not confirmed by this corpus; @muj.manipal.edu on the landing page proves a domain, not an identity provider.
- No vulnerability findings; the pass was passive and no repository was executed or tested.

## KEY FACTS
1. https://github.com/DK10WS/SLCM_APP - SLCM SWITCH app; direct MUJ SLCM client with login and academic retrieval.
2. https://github.com/DK10WS/SLCM_APP/blob/main/README.md - README documenting Flutter, FastAPI, custom email/password auth.
3. https://github.com/madhav-manchanda/SlcmAndLms-aggregator/tree/main - aggregator combining MUJ SLCM and LMS data.
4. https://github.com/Tejas-Narula/SlcmPlus/tree/main - Chrome extension enhancing the MUJ SLCM experience.
5. https://github.com/Tejas-Narula/SlcmPlus/blob/main/manifest.json - manifest with MUJ SLCM host match and attendance handling.
6. https://github.com/manipalthetalk/App-Backend - scraper backend for marks, attendance, timetable; Manipal Karnataka, not MUJ.
7. https://github.com/sankalp2004/SLCM-is-Dumb - CGPA scraper with Selenium/OCR, automated login language, .env warning.
8. https://github.com/raghavkapoor-prog/MUJ-Central - student-services portal; OTP login, attendance and timetable dashboard.
9. https://github.com/mujcentral - MUJ Central organization profile, seven repositories in snapshot.
10. https://github.com/CyberSpace-Club - club profile pinning the official club website.
11. https://github.com/CyberSpace-Club/cscmuj-website - Next.js club site with Vercel deployment reference.
12. https://github.com/orgs/MUJ-ACM-SCHAP/repositories - MUJ ACM Student Chapter organization, 19 repositories in snapshot.
13. https://muj.acm.org/ - ACM chapter site; GMC certificate manager, coding platform, AI chatbot.
14. https://github.com/AwesomeSam9523/HackX3.0 - official MUJ HackX 3.0 website repo; 355 commits in snapshot.
15. https://github.com/slcm-manipal/slcm-manipal.github.io - grades website with MU SLcM_files directory; MUJ link unresolved.

## ACTIONABLE LEADS
- Authorized static review of SLCM_APP and SlcmPlus: credential handling, token storage, API endpoint references.
- Scan SLCM-is-Dumb history for committed .env secrets offline; rotate confirmed secrets through owners; never try credentials.
- Ask each repository owner and MUJ which projects are approved, deployed, and current.
- Request a data-flow diagram from MUJ Central maintainers: where dashboard attendance and timetable data originate.
- Under written scope, compare SlcmPlus-referenced routes and page handling against live portal structure.
- Keep hackathon submission provenance separate: no repo is a submission without an explicit public link.
- Route any likely issue found in static review through responsible disclosure; no live testing.

## FLAGS
- Snapshot discrepancy: cscmuj-website shows 71 commits in one snapshot and 46 commits in another; activity counts are context, not live values.
- csc-24 and cscmuj-website are two similarly named repos; identity must be reconciled before ownership assumptions.
- manipalthetalk is Manipal, Karnataka, not MUJ; do not merge into the MUJ set.
- slcm-manipal organization does not identify MUJ; string "MU" alone is not attribution.
- Repository descriptions are intent, not proof of deployment, authorization, or security.
- The IIC listing appears with two URLs in the report (1702074 and 1702624); listing URLs are volatile.
- SLCM-is-Dumb targets slcm.manipal.edu per its own description; captcha language plus credentials make it high-sensitivity.

## COVERAGE
- Chars read: 51,994
- EOF confirmed: yes (truncated: false on final page, 273 of 273 lines)