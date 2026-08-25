# MUJ SLCM Ecosystem: Public GitHub Intelligence and Defensive Findings

## Executive Summary

- **Strongest Direct SLCM Evidence**: `DK10WS/SLCM_APP` describes itself as an app version for MUJ SLCM, documents student and parent login, and says it fetches grades, GPA/CGPA, and attendance from SLCM; its indexed snapshot shows 71 commits and a June 18, 2025 creation date. [7] [7] [7] -> Treat it as the highest-priority public artifact for an authorized code review, while not treating it as an official university application.

- **Multiple Integration Patterns**: The corpus contains a mobile client, a browser extension, a combined SLCM and LMS dashboard, and server-side scraper projects. The aggregator explicitly describes combining MUJ SLCM and LMS data, while SlcmPlus describes improving the MUJ SLCM experience. [13] [3] -> Model the ecosystem as several independently built integration layers, not as one confirmed software supply chain.

- **CyberSpace Club Is a Verified MUJ Organization Anchor**: MUJ's official clubs page lists CYBER SPACE, and the club site identifies Cyber Space Club with Manipal University Jaipur and describes workshops, hands-on work, peer networking, and portfolio building. [9] [9] [4] [4] -> Use the club's official site and GitHub organization as the attribution anchor, but do not infer that its website touches SLCM.

- **The CyberSpace GitHub Footprint Is Primarily Club-Web Infrastructure**: The public GitHub profile identifies CyberSpace-Club and pins `cscmuj-website` as the official club website. [2] [2] The repository is described as a Next.js project with a Vercel deployment path, and no SLCM or portal reference appears in the reviewed repository evidence. [6] -> Classify it as an informational club-site codebase unless additional public evidence establishes a portal integration.

- **MUJ ACM Is an Active Technical and Educational Hub**: The MUJ ACM site describes workshops, coding competitions, projects, research, hackathons, and networking; it lists an in-house certificate-management website, a coding platform, and an AI chatbot. [5] [5] [5] Its GitHub organization page reports 19 repositories. [15] -> Prioritize ACM repositories for educational and student-service mapping, but keep those systems distinct from SLCM unless a repository says otherwise.

- **Student-Service Portals Create a Separate Layer**: MUJ Central describes resources, event registration, carpooling, a dashboard, and OTP registration using an authorized Manipal ID. [14] [14] Its profile describes the organization as the central hub for MUJ and advertises seven repositories. [11] [11] -> Treat MUJ Central as a student-services portal candidate, not as proof of an SLCM dependency or official university ownership.

- **Legacy and Credential-Sensitive Scrapers Require the Most Care**: Manipal The Talk's `App-Backend` describes a server calling a scraper for SLCM marks, attendance, and timetable data. [1] [1] A separate SLCM-is-Dumb project describes automated login and captcha solving, and its README warns contributors not to commit `.env` credentials. [17] [17] [17] -> Review these artifacts only through authorized static analysis and secret hygiene procedures; do not run them against a university service.

- **Hackathon Repository Provenance Is Not the Same as Submission Provenance**: `AwesomeSam9523/HackX3.0` is explicitly described as the official website for MUJ HackX 3.0 and its indexed snapshot shows 355 commits. [29] Separately, an International Innovation Challenge listing says a GitHub link is optional, not required. [22] [22] -> A hackathon website repository can be listed as event infrastructure, but no repository should be labeled a participant submission without an explicit public linkage.

- **The Supplied Server Stack Remains Unconfirmed by This Public Corpus**: The official MUJ landing page exposes the text "WELCOME TO MUJ PORTAL," a sign-in prompt, the `@muj.manipal.edu` domain, and a parent login option. [20] Those strings establish an identity and login surface, but they do not independently establish ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, or Microsoft 365. -> Keep those stack details marked as user-supplied scope rather than verified OSINT findings.

## Reproducible Evidence Trail and Scope

This report uses public web pages, GitHub organization profiles, GitHub repository metadata, repository descriptions, and public README text. The primary evidence classes are: an official MUJ clubs listing; official club websites; GitHub pages that expose owners, descriptions, files, and activity metadata; and public hackathon listings. The source URLs are repeated in the References section so that a university security club can reproduce the inventory without relying on an undisclosed data source.

I do not provide private chain-of-thought or hidden internal deliberation. The safe and useful substitute requested by the `cot_explicit` field is a reproducible analytical trail: identify the public entity, verify the URL and description, separate explicit portal language from inference, compare activity metadata, record negative findings as bounded observations, and assign confidence separately to attribution, portal relevance, deployment, authorization, and vulnerability. Every conclusion below is labeled as a fact, an observation, or an inference where that distinction matters.

The research was deliberately passive. It did not attempt to log in, submit credentials, defeat a captcha, enumerate protected endpoints, exploit a vulnerability, install an APK, or test whether a repository still reaches a live service. A repository description can show what an author intended to build, but it cannot prove that code is deployed, authorized, secure, or currently maintained. Likewise, a public repository associated with a student or club is not proof that the university approved the integration.

GitHub activity values should be treated as indexed snapshots rather than permanent current values. For example, one public snapshot of `cscmuj-website` shows 46 commits, one star, and two forks. [19] Another snapshot of the same repository shows 71 commits, zero stars, and three forks. [6] [6] This discrepancy is not itself evidence of suspicious behavior. It shows why this report uses activity counts as context and avoids claiming a live count or a precise current maintenance state.

| Evidence label | Meaning in this report | What it does not mean |
|---|---|---|
| Verified public fact | The linked page explicitly states the entity, activity, or portal relationship. | It does not prove deployment, authorization, or security.
| Bounded observation | The reviewed page or corpus did not show a requested string or relationship. | It is not a global claim that the string never exists.
| Inference | A reasoned interpretation of multiple public facts. | It is not an attribution or vulnerability finding.
| Unresolved | The public evidence is insufficient to decide the question. | It is not evidence of absence or wrongdoing.

The central research question is therefore narrower than "find a vulnerability." It is: which public GitHub organizations and repositories have a defensible relationship to MUJ, Manipal student activity, club websites, hackathons, or portal-like systems, and what explicit SLCM references do those pages contain?

## exact_tables: Organization and Repository Inventory

The following table is the core inventory. URLs are exact public URLs, and the activity column records only metadata or descriptions visible in the cited snapshot. The confidence rating is an analytical attribution rating, not a security rating.

| Organization or repository | Exact public URL | Observable activity or purpose | Explicit portal mention | Attribution confidence |
|---|---|---|---|---|
| Cyber Space Club | https://github.com/CyberSpace-Club | GitHub identifies the user as Cyber Space Club and pins the official MUJ club website. [2] | None in the reviewed profile evidence. | High for the GitHub identity; medium for university ownership because the GitHub page itself is not a university directory. |
| CyberSpace club website | https://www.cscmuj.com/ | The site identifies Cyber Space Club and describes learning, workshops, hands-on experience, peer networking, and portfolio building. [4] | No SLCM reference in the reviewed site content. | High for club-site identity. |
| MUJ ACM Student Chapter | https://github.com/orgs/MUJ-ACM-SCHAP/repositories | The public organization page describes an open source initiative and reports 19 repositories. [15] | No direct SLCM claim in the cited organization summary. | High for organization identity; medium for the current repository count because GitHub metadata changes. |
| MUJ ACM public site | https://muj.acm.org/ | The site describes workshops, competitions, projects, research, talks, hackathons, and networking. [5] [5] | It names a certificate-management website, coding platform, and AI chatbot, but not SLCM in the cited project text. [5] | High for chapter activity. |
| MUJ Central organization | https://github.com/mujcentral | The profile calls MUJ Central the central hub for everything MUJ and shows links and pinned repositories. [11] A separate snapshot advertises seven repositories. [11] | Student-service and event portal functions appear in a repository README, not as proof of official SLCM integration. [14] | Medium: explicit MUJ branding, but no university ownership claim. |
| Manipal The Talk Network | https://github.com/manipalthetalk | The profile describes a student-run media organization spread across twelve colleges in Manipal and lists multiple projects. [16] | Its App-Backend explicitly mentions scraping SLCM. [16] | High for the organization; low for MUJ-specific attribution because the profile identifies Manipal, Karnataka rather than MUJ. |
| slcm-manipal | https://github.com/slcm-manipal | The profile identifies the account and pins a website for checking grades. [24] [24] | The repository includes a `MU SLcM_files/` directory. [27] | Low to medium for MUJ relevance; the public evidence does not identify the university as MUJ. |
| Accelerate community files | https://github.com/accelerate-muj/.github | The repository describes community health files, a constitution, and an organization landing page. [26] [26] | No SLCM reference in the cited description. | Low to medium: the name is MUJ-oriented, but the cited page does not establish an official university relationship. |

The main table shows two distinct populations. CyberSpace Club and MUJ ACM have strong organization-level evidence and public club activity, while portal repositories are more often individual or project-level artifacts. That difference matters: a club identity can be well supported even when a particular portal integration is not, and a portal repository can be technically explicit even when its affiliation is not institutionally confirmed.

## CyberSpace-Club: Verified Club Activity, No Proven SLCM Link

The CyberSpace-Club GitHub profile is a strong attribution starting point. It identifies the user as Cyber Space Club and gives the profile URL `https://github.com/CyberSpace-Club`. Its pinned repository is `CyberSpace-Club/cscmuj-website`, described as the official website for the CyberSpace Club MUJ, with JavaScript as the top language. [2] The official MUJ clubs page separately lists CYBER SPACE and supplies departmental contact information. [9] [9] The club's own site names the organization as Cyber Space Club, Manipal University Jaipur. [4]

The club website describes its activity in terms of expert-led workshops, hands-on experience, networking with peers, and portfolio building. [4] It exposes sections for events, certificates, newsletter, leaderboard, and team, and links to Instagram and LinkedIn accounts. [4] [4] These are public activity indicators, not a claim that every section is backed by a production system or that the club has privileged access to MUJ infrastructure.

The GitHub website repository is described as a `csc-24 website` and a Next.js project. [6] Its indexed page shows a main branch, a 71-commit history, JavaScript and CSS language information, and a Vercel deployment reference. [6] [6] A separate snapshot of `CyberSpace-Club/csc-24` shows a 2024 creation timestamp, 46 commits, one star, two forks, a Next.js README, and a Vercel deployment instruction. [19] [19]

The two repository snapshots should not be collapsed into a claim that one is necessarily an older or newer live state. The safe observation is that the same public organization has at least two portal-adjacent-looking names, but the cited evidence describes club web infrastructure rather than SLCM. **Inference:** the public CyberSpace footprint is more consistent with communications and event presence than with an academic-record integration. That inference is bounded by the pages reviewed; it is not a code audit and does not prove that no other private or unindexed project exists.

| CyberSpace artifact | Exact URL | Evidence-backed activity | SLCM or portal result | Defensive interpretation |
|---|---|---|---|---|
| Organization profile | https://github.com/CyberSpace-Club | Club identity and pinned official site. [2] | No explicit SLCM string in the cited profile. | Attribution anchor; review organization access and repository permissions if authorized. |
| `cscmuj-website` | https://github.com/CyberSpace-Club/cscmuj-website | Next.js club website, main branch, indexed 71 commits, Vercel reference. [6] | No portal or SLCM mention in the reviewed repository evidence. | Treat as public club web code, not as a university portal client. |
| `csc-24` | https://github.com/CyberSpace-Club/csc-24 | Next.js repository with an indexed 2024 creation timestamp and 46 commits. [19] [19] | No portal or SLCM mention in the reviewed evidence. | Reconcile repository identity before using activity counts or ownership assumptions. |
| Official club site | https://www.cscmuj.com/ | Workshops, events, certificates, newsletter, leaderboard, and team sections. [4] [4] | No SLCM mention in the reviewed site content. | Use for public activity corroboration, not technical attribution of portal code. |

## MUJ ACM: Educational Repositories and Student-Service Projects

The official MUJ ACM site identifies the group as the MUJ ACM Student Chapter and describes a community that explores computing, nurtures talent, promotes learning, and fosters innovation through collaborative projects and industry engagement. [5] Its mission emphasizes learning, knowledge sharing, computing projects, mentorship, hands-on learning, and collaboration. [5] The activity model includes workshops and seminars on web development and machine learning, coding competitions, hackathons, projects, research, talks, and networking events. [5] [5]

The public project inventory is especially useful for separating portal-like functions from SLCM-specific functions. MUJ ACM describes GMC as an in-house website for certificate management for events, a coding platform for problem solving and contests, and an AI chatbot for common questions and ACM event information. [5] None of those cited descriptions says that the service reads MUJ SLCM. The ACM GitHub organization page calls itself an open source initiative and reports 19 repositories. [15]

The repository `https://github.com/MUJ-ACM-SCHAP/Python` is described as an online collection of notes, slides, assignments, and related material for the Bronze-level Python class of ACM MUJ SCHAP. [25] This is an educational repository rather than a portal integration based on the available description. **Inference:** ACM is a useful source of student-built software and learning artifacts, but its public evidence supports a broader technical-community role rather than a direct SLCM dependency.

This distinction reduces false positives. A certificate portal, coding platform, chatbot, club website, and SLCM client may all be student-built web systems, but their data domains and trust boundaries differ. A certificate system may process names and event participation; a coding platform may process code submissions; an AI chatbot may process questions; an SLCM client may process grades, attendance, timetables, and identity data. The source evidence supports the existence of the first three ACM project categories, but not a claim that they share credentials, databases, or deployment infrastructure.

| MUJ ACM artifact | Exact URL | Stated activity | Portal relevance | Confidence and caution |
|---|---|---|---|---|
| ACM chapter site | https://muj.acm.org/ | Workshops, competitions, projects, research, talks, hackathons, and networking. [5] [5] | Broad student technology activity; no cited SLCM statement. | High for activity; no deployment claim. |
| ACM GitHub organization | https://github.com/orgs/MUJ-ACM-SCHAP/repositories | Open source initiative with 19 reported repositories. [15] | Repository inventory may include student services, but the count page alone does not identify SLCM. | Medium to high; counts are snapshot-sensitive. |
| Python learning repository | https://github.com/MUJ-ACM-SCHAP/Python | Bronze-level Python notes, slides, assignments, and related material. [25] | No portal function in the cited description. | High for educational purpose. |
| GMC project | https://muj.acm.org/ | In-house certificate management website for ACM events. [5] | Event certificate portal, not SLCM on current evidence. | High for stated project category; implementation details unresolved. |
| Coding platform | https://muj.acm.org/ | Online coding problems, contests, and skills practice. [5] | Student coding service, not academic-record access on current evidence. | High for stated purpose. |

## MUJ Central and the Student-Service Portal Layer

The individual repository `https://github.com/raghavkapoor-prog/MUJ-Central` describes MUJ Central as a one-stop destination for Manipal University Jaipur students. [8] The README says it is developed by a team of MUJ students and that anyone can join and contribute. [8] Its stated features include past-year papers, presentations, books, doubt support, event registration for hackathons, workshops, and seminars, and a carpooling portal. [8] The README further describes authentication using an OTP sent to an authorized Manipal ID and a dashboard containing profile, attendance, timetable, and related information. [8] [14]

The same README gives the project a broader student-services scope: resources include library material, e-books, question papers, syllabus, clubs, and societies. [8] That makes MUJ Central relevant to portal mapping, but the cited text does not say that it authenticates against MUJ SLCM or imports records from the official SLCM service. The word "portal" appears in connection with event registration and carpooling. [8] **Inference:** MUJ Central should be classified as a student-services portal candidate, not as a verified SLCM wrapper.

The organization profile identifies `MUJ Central`, links a bit.ly site, and shows Python and HTML among top languages. [11] Its pinned repositories include `mujcentral/mujcentral.github.io`. [11] A separate public snapshot says that `mujcentral` has seven repositories. [11] The individual MUJ-Central repository snapshot shows zero stars, one fork, a 2023-07-20 creation timestamp, and 373 commits. [8] These values are historical indexed metadata and should not be presented as a current live count.

A security club should pay attention to the combination of academic-looking fields and community authentication without calling it a vulnerability. The README says the system can expose attendance and timetable information after login, but the public text does not reveal whether those values come from SLCM, a separate database, user uploads, or a manually maintained service. A legitimate review would need owner authorization, a data-flow diagram, test accounts, and a non-production environment. Public GitHub text alone cannot supply those facts.

| MUJ Central artifact | Exact URL | Publicly stated function | Explicit SLCM relation | Safe conclusion |
|---|---|---|---|---|
| MUJ Central repository | https://github.com/raghavkapoor-prog/MUJ-Central | MUJ student destination with resources, event registration, carpooling, dashboard, profile, attendance, and timetable features. [14] [8] | No explicit SLCM integration in the cited README passages. | Student-services portal candidate; not an official SLCM client on this evidence. |
| MUJ Central organization | https://github.com/mujcentral | Organization identity, site link, Python and HTML, pinned repositories. [11] | No direct SLCM statement in the profile excerpt. | Useful discovery anchor; repository count is snapshot-sensitive. |
| MUJ Central website repository | https://github.com/mujcentral/mujcentral.github.io | Pinned MUJ Central HTML repository. [11] | No SLCM statement in the cited profile excerpt. | Website artifact; deployment and data source unresolved. |

## SLCM-Related Code: Direct, Indirect, Legacy, and Ambiguous References

The strongest direct repository evidence is `DK10WS/SLCM_APP`. Its description says "App Version for MUJ SLCM." [7] The README calls the project SLCM SWITCH and describes a mobile application that provides an interface for the university SLCM website. [12] The documented stack is Flutter and Dart on the frontend, FastAPI and Python on the backend, custom email and password authentication, and Docker as an optional deployment component. [7] The feature text describes student and parent login, timetable and calendar viewing, and automatic retrieval of grades, GPA/CGPA, and subject-wise attendance. [7] This is a clear public reference to MUJ SLCM, but it remains an author-described project. It does not prove permission to automate the service or prove that the application is deployed.

`SlcmAndLms-aggregator` is another direct text match. Its repository description says it is a full-stack application combining data from the MUJ SLCM and LMS portals into one dashboard. [13] A backend README describes the same purpose as combining both MUJ SLCM and LMS portals. [10] The available evidence does not establish whether the project is complete, deployed, authorized, or still maintained. It does establish the intended data-domain relationship.

`Tejas-Narula/SlcmPlus` is a browser-extension pattern. A GitHub topic result describes it as a Chrome extension for MUJ students that enhances the SLCM experience. [3] The repository contains `content.js`, `manifest.json`, styles, and images. [21] The manifest evidence says the extension improves workflow for MUJ students and includes a match pattern beginning with the MUJ SLCM host. [30] The content script evidence shows table-oriented page handling and a URL containing an attendance-summary route. These are direct code-reference indicators, not evidence that the extension bypasses access controls or that the route is currently reachable.

The legacy scraper pattern is different. Manipal The Talk's `App-Backend` describes scraping SLCM for marks, attendance, and timetable data. [1] Its README says the scraper is called by the server to extract data from SLCM and identifies Python 2.7 and Golang. [1] The indexed repository snapshot shows four stars, one fork, a 2017-12-02 creation timestamp, and 25 commits. [1] The organization profile identifies Manipal The Talk Network as a student-run media organization in Manipal, Karnataka. [16] That is a real portal reference, but it is not enough to assign MUJ affiliation.

`SLCM-is-Dumb` is especially sensitive because the README describes a Python scraper for extracting CGPA using Selenium and OCR, including automated login and captcha-solving language. [17] It documents username and password environment variables and explicitly says not to commit `.env` files or credentials. [17] [17] The correct defensive interpretation is not that the repository proves a vulnerability. It is that any authorized review should examine secret handling, consent, terms of use, data minimization, and whether test fixtures can replace live academic accounts. This report intentionally does not reproduce operational steps.

The `slcm-manipal` organization is a useful but ambiguous candidate. Its profile pins a JavaScript website described as a website for checking grades. [24] [24] The repository snapshot includes a `MU SLcM_files/` directory and shows an indexed 2018 creation timestamp with 17 commits. [27] The public evidence does not identify Manipal University Jaipur, so it should not be merged into the MUJ-specific set merely because it contains the string "MU".

`CTMUJ-Student-Portal` is MUJ-specific by its own description. It is described as a full-stack PBL project for Manipal University Jaipur students and as a web-based platform intended to simplify academic life. [28] Its page reports five commits, no issues, no pull requests, zero stars, zero forks, and no releases in the indexed snapshot. [28] [28] [28] [28] The cited page lists a frontend of HTML, CSS, and vanilla JavaScript, with Node.js, Express.js, and MongoDB in the technology stack. [28] It does not mention SLCM in the available evidence, so it belongs in the MUJ portal candidate set but not the direct SLCM set.

| Repository or organization | Exact URL | Portal evidence | Activity evidence | Classification |
|---|---|---|---|---|
| SLCM SWITCH | https://github.com/DK10WS/SLCM_APP | Explicit MUJ SLCM app; student and parent login; grades, GPA/CGPA, timetable, and attendance. [7] [7] | 3 stars, zero forks, 71 commits in the indexed snapshot. [7] | Direct MUJ SLCM reference; authorization and deployment unresolved. |
| SLCM plus LMS aggregator | https://github.com/madhav-manchanda/SlcmAndLms-aggregator | Explicitly combines MUJ SLCM and LMS data. [13] [10] | Activity details not established in the cited excerpt. | Direct intended integration; completeness and deployment unresolved. |
| SlcmPlus | https://github.com/Tejas-Narula/SlcmPlus | MUJ SLCM enhancement, host match, and attendance-summary page handling. [3] [30] | Repository contains extension files including content.js and manifest.json. [21] | Direct browser-extension reference; no claim of bypass or live use. |
| Manipal The Talk App-Backend | https://github.com/manipalthetalk/App-Backend | Scraper and server for SLCM marks, attendance, and timetable. [1] [1] | 4 stars, 1 fork, 25 commits, created 2017-12-02 in snapshot. [1] | Direct SLCM reference; MUJ attribution not established. |
| SLCM-is-Dumb | https://github.com/sankalp2004/SLCM-is-Dumb | CGPA scraper, automated login and captcha/OCR language. [17] | Indexed snapshot shows 17 commits and a 2025-06-17 creation timestamp. [17] | Credential-sensitive research artifact; do not run against live systems. |
| slcm-manipal grade site | https://github.com/slcm-manipal/slcm-manipal.github.io | Website for checking grades and `MU SLcM_files/`. [24] [27] | 17 commits in indexed snapshot. [27] | Generic Manipal SLCM candidate; MUJ link unresolved. |
| CTMUJ Student Portal | https://github.com/aayra101/CTMUJ-Student-Portal | MUJ student portal and long-term PBL project, but no SLCM reference in available evidence. [28] | Five commits and no published releases in snapshot. [28] [28] | MUJ portal candidate; SLCM relationship unresolved. |

## Hackathon Repositories, Club Websites, and Discovery Candidates

The public GitHub topic page for Manipal University Jaipur surfaced several useful discovery candidates. It lists `vverma022/mujcentral2.0` as a MUJ student-help website, `Tejas-Narula/SlcmPlus` as a MUJ SLCM enhancement, `CrystalFire1o8/themusicclubmuj` as the official Music Club MUJ website, and `adityasinha-1988/CSE-Exam-sitting-finder` as an exam seating arrangement portal. [3] It also lists `accelerate-muj/.github` as community health and organization material. [3] A topic result is a discovery mechanism, not institutional verification. Each candidate still needs its own owner, README, and deployment evidence.

The HackX evidence is stronger for event-site attribution. `https://github.com/AwesomeSam9523/HackX3.0` describes itself as the official website for MUJ HackX 3.0. [29] Its indexed snapshot shows four stars, four forks, a main branch, a June 19, 2025 creation timestamp, and 355 commits. [29] The repository has backend, docker, frontend, and public partner directories in the visible file list. [29] The public evidence does not show an SLCM reference, so this is event infrastructure rather than a portal artifact.

An International Innovation Challenge listing adds an important provenance constraint. It identifies International Innovation Challenge 3.0, says shortlisted teams would participate at Manipal University Jaipur, and says a prototype may include code with a GitHub link that is optional. [22] [22] The listing requires a project presentation of up to nine slides. [22] Therefore, an event can accept GitHub links without publishing a complete participant-repository index. **Inference:** failure to find a submission repository is not evidence that no submission exists, and the presence of a MUJ hackathon website repository is not evidence that it is a submission.

The Music Club and exam-seating candidates are relevant because they show how broad the portal vocabulary is. The topic page calls the Music Club repository an official MUJ club website and calls the exam-seating project a portal. [3] Neither cited topic entry establishes an SLCM integration. The same caution applies to Accelerate: its repository describes organization governance and community health files, including a SECURITY.md and CONTRIBUTING.md, but the cited text does not establish university ownership or a portal relationship. [26] [26]

| Candidate | Exact URL | Observable activity | Portal or SLCM mention | Status |
|---|---|---|---|---|
| MUJ HackX 3.0 website | https://github.com/AwesomeSam9523/HackX3.0 | Official-event website description; backend, frontend, Docker, and public directories; 355 commits in snapshot. [29] | No SLCM mention in reviewed evidence. | Verified event-site candidate, not a participant submission. |
| HackX public event site | https://www.hackxmuj.com/ | Associated public event URL used for HackX discovery. | No portal claim used in this report. | Event context only; repository linkage is based on the repository description. |
| International Innovation Challenge listing | https://unstop.com/hackathons/crp-iic-3-0-manipal-university-jaipur-1702074 | Hackathon listing; project submission in a presentation; shortlisted teams at MUJ. [22] [22] | GitHub code link is optional. [22] | Submission provenance unresolved. |
| Music Club MUJ website | https://github.com/CrystalFire1o8/themusicclubmuj | Topic description calls it the official website of The Music Club, Manipal University Jaipur. [3] | No SLCM mention in the cited topic entry. | Club-site candidate. |
| CSE exam seating finder | https://github.com/adityasinha-1988/CSE-Exam-sitting-finder | Topic description calls it a web-based exam seating arrangement portal. [3] | No SLCM mention in the cited topic entry. | Portal candidate; ownership and deployment unresolved. |
| Accelerate organization files | https://github.com/accelerate-muj/.github | Community health files, constitution, governance, and organization landing page. [26] [26] | No SLCM mention in cited evidence. | Low-confidence MUJ-related discovery candidate. |

## Portal References and Passive Stack Analysis

The official MUJ landing page is the correct public anchor for the university portal identity. It displays "WELCOME TO MUJ PORTAL," a sign-in prompt, the `@muj.manipal.edu` domain, and both parent and student login labels. [20] Those strings support a statement that a public MUJ-branded login landing page exists. They do not support a statement about how the back end is implemented.

The direct code references form a useful passive map. `SLCM_APP` explicitly names MUJ SLCM and documents academic fields. [7] [7] The aggregator explicitly names both MUJ SLCM and LMS. [13] SlcmPlus contains a MUJ SLCM host match and attendance-related page handling in the reviewed evidence. [30] The App-Backend description names marks, attendance, and timetable scraping, while the SLCM-is-Dumb README names CGPA extraction and login automation. [1] [17] These references are sufficient to identify high-level data flows for an authorized threat model: identity input, academic record retrieval, client-side display, and possible server-side mediation.

The public evidence does not independently confirm the technology stack supplied in the task input: ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, or Microsoft 365 identity. The landing page's `@muj.manipal.edu` string is an email or identity-domain indicator, not proof of Microsoft 365. [20] Similarly, a page that displays a sign-in form does not establish the framework, web server, reverse proxy, or hosting provider. The responsible wording is: those details are **in-scope user-provided assertions, not independently verified findings in this report**.

| Requested technical or identity element | Public evidence found | What can safely be concluded | Confidence |
|---|---|---|---|
| MUJ portal identity | WELCOME TO MUJ PORTAL and sign-in labels. [20] | A MUJ-branded public login landing page is evidenced. | High |
| MUJ SLCM host relationship | SLCM_APP, aggregator, and SlcmPlus explicitly reference MUJ SLCM or the MUJ SLCM host. [7] [13] [30] | Several public projects intend to interact with MUJ SLCM. | High for stated intent; low for authorization or deployment. |
| Academic data domains | Grades, GPA/CGPA, attendance, timetable, and calendar are described by SLCM_APP; marks, attendance, and timetable by App-Backend. [7] [1] | These projects describe handling academic data categories. | High for README claims. |
| ASP.NET MVC 5.3 | Not established by the cited public pages. | Retain as user input only. | Unknown |
| .NET Framework 4.x | Not established by the cited public pages. | Retain as user input only. | Unknown |
| IIS 10 | Not established by the cited public pages. | Retain as user input only. | Unknown |
| Akamai | Not established by the cited public pages. | Retain as user input only. | Unknown |
| Microsoft 365 identity | `@muj.manipal.edu` appears on the landing page. [20] | The domain is evidenced; the identity provider is not. | Unknown |

**Inference:** the most defensible architecture hypothesis is a set of external student-built clients and portals that may interact with an official academic login or data surface. That hypothesis is useful for threat modeling, but it must not be promoted to a confirmed topology. The public evidence does not show whether credentials are sent directly to the official service, whether an intermediary backend stores data, whether a browser extension only reads already-rendered pages, or whether any project is authorized.

## Defensive Review Priorities Without Unauthorized Access

The first priority is ownership and authorization. Ask MUJ and each repository owner to identify which projects are approved, who owns the code, whether the project is active, and which environment is permitted for testing. A public URL is not a testing authorization. This is particularly important where the README describes student or parent login and academic data. [7] No live account, password, captcha, or session should be used for research unless the owner supplies written permission and a test account.

The second priority is credential and secret hygiene. The SLCM-is-Dumb README itself tells contributors not to commit `.env` files and to keep credentials secure. [17] That warning should become a review checklist: inspect repository history for accidental secrets using approved offline tooling, rotate any confirmed exposed secret through the owner, remove sensitive values from issue comments and build logs, and verify that sample configuration uses placeholders. Do not attempt any discovered credential, and do not include credentials in a club report.

The third priority is data-flow minimization. SLCM_APP describes student and parent login and academic-data retrieval. [7] MUJ Central describes OTP registration and dashboard data such as attendance and timetable. [8] The review should therefore ask whether the application needs every field, whether parent and student roles are separated, whether logs redact grades and identifiers, whether tokens are short-lived, and whether cached data is deleted. These are review questions, not claims that a weakness exists.

The fourth priority is boundary analysis across integration styles. A mobile app, browser extension, aggregator, and scraper have different exposure points. A mobile app may package API endpoints or retain tokens; a browser extension may have broad host permissions; an aggregator may centralize records; a scraper may break when login or page structure changes. The public descriptions support the existence of these patterns. [7] [21] [13] [1] The report does not infer that any one pattern is vulnerable.

The fifth priority is provenance and build security. CyberSpace's website evidence references Next.js and Vercel, while HackX3.0 exposes backend, frontend, and Docker directories. [6] [29] An authorized review can check branch protection, dependency pinning, CI secret scope, deployment ownership, and whether preview deployments contain production data. Those checks should be performed in repositories or environments where the reviewers have permission.

The sixth priority is responsible disclosure. If static review reveals a likely issue, preserve only the minimum evidence, avoid accessing other users' records, notify the repository owner and the university security contact, and give a reasonable remediation window. Do not publish a working exploit, a bypass recipe, credentials, or personal academic data. For a student security club, the learning objective is to document the trust boundary and remediation path, not to demonstrate access to a real account.

| Review priority | Evidence motivating the priority | Safe authorized action | Do not do |
|---|---|---|---|
| Ownership and authorization | Public projects describe MUJ SLCM, student login, or academic data. [7] [7] | Obtain written scope, owner contacts, test accounts, and approved environments. | Do not infer permission from public code. |
| Secret hygiene | README uses SLCM username/password environment variables and warns against committing `.env`. [17] [17] | Scan authorized history offline, rotate confirmed secrets, redact reports. | Do not try any credential or token. |
| Identity and role separation | SLCM_APP documents student and parent login; MUJ Central documents OTP to an authorized Manipal ID. [7] [14] | Test only with owner-provided accounts and verify role/data minimization. | Do not access another person's academic record. |
| Client and extension boundary | SLCM_APP uses Flutter/FastAPI; SlcmPlus contains extension files and a MUJ host match. [7] [21] [30] | Review permissions, token storage, and dependency configuration in an approved environment. | Do not install or execute untrusted artifacts against production. |
| Provenance | HackX3.0 is an event website repository; IIC says GitHub links are optional. [29] [22] | Label event infrastructure and participant submissions separately. | Do not attribute an unlinked repository to a participant. |

## Comparative Analysis and Synthesis

The evidence becomes clearer when the major entities and strategies are compared across purpose, mechanism, scope, trade-offs, and time horizon. CyberSpace and ACM are organization-centered communities. MUJ Central and CTMUJ are student-service or PBL portals. SLCM_APP and SlcmPlus are direct client-side integration candidates. App-Backend and SLCM-is-Dumb represent scraping or automation patterns. HackX3.0 is event infrastructure. These are not interchangeable categories.

| Entity or strategy | Primary purpose | Mechanism stated by public evidence | Data or scope | Main trade-off | Evidence horizon |
|---|---|---|---|---|---|
| CyberSpace Club | Cybersecurity community and club activity | Workshops, hands-on work, events, certificates, newsletter, leaderboard, and team sections. [4] [4] | Club participation and public communications | Strong attribution, but no cited SLCM relationship | Current public site and indexed repositories; exact live counts vary. [6] [19] |
| MUJ ACM | Computing education and technical projects | Workshops, competitions, research, certificate management, coding platform, chatbot. [5] [5] | Learning, events, certificates, coding, questions | Broad project surface can create false portal associations | Organization reports 19 repositories in snapshot. [15] |
| MUJ Central | Student services and community resources | OTP account, dashboard, resources, event registration, carpooling. [14] [14] | Student resources and dashboard-style data | Useful centralization versus unclear data provenance | Repository snapshot reports 373 commits; organization count reports seven repositories. [8] [11] |
| SLCM_APP | Mobile SLCM interface | Flutter/FastAPI, custom authentication, student and parent login, academic retrieval. [7] | Grades, GPA/CGPA, attendance, timetable | Convenience versus credential and academic-data exposure | Created 2025-06-18 with 71 commits in indexed snapshot. [7] |
| SlcmPlus | Browser workflow enhancement | Chrome extension files, MUJ host match, table and attendance-page handling. [21] [30] | Rendered portal pages and attendance workflow | Convenience versus extension permissions and page-change fragility | Snapshot does not prove live deployment or authorization. |
| App-Backend scraper | Server-mediated academic extraction | Server calls a scraper; Python 2.7 and Golang. [1] | Marks, attendance, timetable. [1] | Centralized extraction versus legacy and consent risk | Indexed repository created 2017-12-02. [1] |
| SLCM-is-Dumb | CGPA extraction | Selenium, OCR, captcha-solving language, environment credentials. [17] [17] | CGPA and grade-sheet workflow | High sensitivity around credentials and anti-automation controls | Indexed snapshot created 2025-06-17. [17] |
| HackX3.0 website | Hackathon event infrastructure | Public repository has backend, frontend, Docker, and partner directories. [29] | Event information and participation | Event-site identity does not prove submission identity | Indexed snapshot shows 355 commits. [29] |

Three non-obvious tensions emerge. First, the ecosystem is simultaneously community-led and identity-sensitive. Clubs openly publish websites and learning projects, while portal projects describe login and academic records. Public collaboration is beneficial for student learning, but the same openness can expose configuration, dependencies, or assumptions about a protected data service. That is a risk-management tension, not evidence of misconduct.

Second, centralization has opposite effects depending on the layer. MUJ Central presents one destination for resources and event services. [14] The SLCM and LMS aggregator similarly presents a single dashboard for two data sources. [13] Centralization can improve usability, but it also increases the consequence of a credential, token, authorization, or logging error. **Inference:** the aggregator deserves a higher data-flow review priority than a static club website, even though the public description does not prove a vulnerability.

Third, freshness and provenance diverge. SLCM_APP has a 2025 creation timestamp and 71 commits in the indexed snapshot. [7] App-Backend has a 2017 creation timestamp and 25 commits. [1] CTMUJ is a PBL portal with five commits and no releases in the snapshot. [28] [28] These dates indicate different project stages, but they do not prove which project is active, which one is deployed, or which one is authorized. The right action is to request owner confirmation rather than rank projects by age alone.

The synthesis is therefore a layered model: official MUJ portal identity at the center; student-built direct clients and scrapers around the academic data surface; separate club, certificate, coding, event, and resource portals; and a public GitHub discovery layer that mixes verified organizations with ambiguous name matches. The model is useful for defensive scoping precisely because it preserves uncertainty instead of turning every repository mention into an attribution or vulnerability claim.

## Unanswered Questions and Confidence Boundaries

| Question still unanswered | Current status | Why it remains unanswered |
|---|---|---|
| Is every MUJ-named GitHub organization officially recognized by MUJ? | Unresolved | The official MUJ clubs page lists several clubs, but GitHub profile branding alone does not prove institutional ownership. [9] [9] |
| Is `DK10WS/SLCM_APP` authorized to access MUJ SLCM? | Unresolved | Its README states intended functionality, but public repository text does not show approval or a deployment authorization. [7] [7] |
| Is the aggregator deployed and currently used by students? | Unresolved | The description states intended combination of SLCM and LMS, not operational status. [13] |
| Does MUJ ACM's GMC, coding platform, or chatbot share infrastructure with SLCM? | Unresolved | The ACM site describes the projects but does not state a shared identity, database, or deployment. [5] |
| Is `slcm-manipal` MUJ-specific? | Unresolved | The page says website for checking grades and includes `MU SLcM_files/`, but the cited evidence does not identify MUJ. [24] [27] |
| Is HackX3.0 a participant submission? | No evidence found | The repository calls itself the event's official website, while a separate event listing says GitHub links are optional. [29] [22] |
| Is the supplied ASP.NET, .NET, IIS, Akamai, and Microsoft 365 stack publicly confirmed? | Unresolved | The public portal landing page shows identity and login text, not server or identity-provider technology. [20] |
| Is any listed project vulnerable? | No vulnerability finding | This research was passive and did not perform authorized testing or exploit validation. |

## VERDICT

**Verdict: The public GitHub corpus supports a real, multi-project MUJ and Manipal student-technology ecosystem, with high confidence for the existence of CyberSpace Club, MUJ ACM activity, MUJ Central branding, and several repositories that explicitly describe SLCM or MUJ portal interactions.** The most direct MUJ SLCM references are `DK10WS/SLCM_APP`, `SlcmAndLms-aggregator`, and `SlcmPlus`. [7] [13] [3] The strongest non-MUJ-specific SLCM reference is Manipal The Talk's App-Backend, which explicitly describes server-side scraping for marks, attendance, and timetable data. [1] [1]

**Confidence is high for repository descriptions and public activity claims, medium for organization-to-MUJ attribution outside the official club listing, and low or unknown for authorization, production deployment, current maintenance, and vulnerability status.** The official MUJ clubs page corroborates Cyber Space and ACM as listed clubs or chapters. [9] [9] The club and chapter websites corroborate their public missions and activities. [4] [5] But no cited page establishes that the university owns every individual repository, approves every SLCM integration, or operates every portal candidate.

The final defensive conclusion is deliberately narrow: public code and descriptions expose a map of intended integrations and data categories, not proof of compromise. The security club should use the map to obtain written authorization, build a source-to-destination data-flow diagram, review secrets and role separation offline, and coordinate responsible disclosure. It should not log into the live portal, use credentials, solve captchas, install untrusted builds, or probe endpoints based only on public GitHub evidence.

## References

1. *GitHub - manipalthetalk/App-Backend: Scrapes the SLCM for : Marks, Attendance, Timetable, etc. · GitHub*. https://github.com/manipalthetalk/App-Backend
2. *CyberSpace-Club (Cyber Space Club) · GitHub*. https://github.com/CyberSpace-Club
3. *manipal-university-jaipur · GitHub Topics · GitHub*. https://github.com/topics/manipal-university-jaipur
4. *CSC MUJ*. https://www.cscmuj.com/
5. *MUJ ACM*. https://muj.acm.org/
6. *GitHub - CyberSpace-Club/cscmuj-website*. https://github.com/CyberSpace-Club/cscmuj-website
7. *GitHub - DK10WS/SLCM_APP: App Version for MUJ SLCM · GitHub*. https://github.com/DK10WS/SLCM_APP
8. *GitHub - raghavkapoor-prog/MUJ-Central: MUJ Central is a website that aims to provide a one-stop destination for students of Manipal University Jaipur. It offers various features and resources to help students succeed in their academic and non-academic pursuits. Some of the features and resources are: · GitHub*. https://github.com/raghavkapoor-prog/MUJ-Central
9. *Clubs and Chapters - Manipal University Jaipur *. https://www.jaipur.manipal.edu/dsw-student-clubs.php
10. *SlcmAndLms-aggregator/backend/README.md at main - GitHub*. https://github.com/madhav-manchanda/SlcmAndLms-aggregator/blob/main/backend/README.md
11. *mujcentral (MUJ Central) · GitHub*. https://github.com/mujcentral
12. *SLCM_APP/README.md at main · DK10WS/SLCM_APP · GitHub*. https://github.com/DK10WS/SLCM_APP/blob/main/README.md
13. *madhav-manchanda/SlcmAndLms-aggregator - GitHub*. https://github.com/madhav-manchanda/SlcmAndLms-aggregator/tree/main
14. *MUJ-Central/README.md at main · raghavkapoor-prog/MUJ-Central · GitHub*. https://github.com/raghavkapoor-prog/MUJ-Central/blob/main/README.md
15. *MUJ ACM Student Chapter - GitHub*. https://github.com/orgs/MUJ-ACM-SCHAP/repositories
16. *Manipal The Talk Network · GitHub*. https://github.com/manipalthetalk
17. *GitHub - sankalp2004/SLCM-is-Dumb: This extracts cgpa from https://slcm.manipal.edu/ directly and passes captcha · GitHub*. https://github.com/sankalp2004/SLCM-is-Dumb
18. *SlcmAndLms-aggregator/README.md at main - GitHub*. https://github.com/madhav-manchanda/SlcmAndLms-aggregator/blob/main/README.md
19. *GitHub - CyberSpace-Club/csc-24 · GitHub*. https://github.com/CyberSpace-Club/csc-24
20. *Manipal University*. http://mujslcm.jaipur.manipal.edu/Home/Index
21. *GitHub - Tejas-Narula/SlcmPlus: A Chrome extension for MUJ students that enhances the SLCM experience by providing attendance analytics and automatic marks calculation directly within the portal. · GitHub*. https://github.com/Tejas-Narula/SlcmPlus/tree/main
22. *International Innovation Challenge 3.0 - 2026*. http://unstop.com/hackathons/international-innovation-challenge-30-manipal-university-mu-jaipur-1702624
23. *MUJ HackX 3.0 | 36-Hour National Hackathon at Manipal University Jaipur*. http://internshala.com/competitions/hackx-3-0
24. *slcm-manipal · GitHub*. https://github.com/slcm-manipal
25. *GitHub - MUJ-ACM-SCHAP/Python: An online collection of notes ...*. https://github.com/MUJ-ACM-SCHAP/Python
26. *GitHub - accelerate-muj/.github: Community health files, constitution, and org landing page for Accelerate. · GitHub*. https://github.com/accelerate-muj/.github
27. *GitHub - slcm-manipal/slcm-manipal.github.io: Website for checking grades. · GitHub*. https://github.com/slcm-manipal/slcm-manipal.github.io
28. *GitHub - aayra101/CTMUJ-Student-Portal: Full Stack PBL Project  A fully functional college student portal for Manipal University Jaipur (MUJ) students, built as a long-term Project Based Learning (PBL) initiative. · GitHub*. https://github.com/aayra101/CTMUJ-Student-Portal
29. *GitHub - AwesomeSam9523/HackX3.0: Official website for MUJ HackX 3.0 🚀 · GitHub*. https://github.com/AwesomeSam9523/HackX3.0
30. *SlcmPlus/manifest.json at main · Tejas-Narula/SlcmPlus · GitHub*. https://github.com/Tejas-Narula/SlcmPlus/blob/main/manifest.json
