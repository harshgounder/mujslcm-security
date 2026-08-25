# MUJ SLCM Public-Video OSINT Report

## Executive Summary

This report answers a narrow, evidence-led question: what publicly discoverable videos and portal how-to material currently describe the Manipal University Jaipur (MUJ) SLCM ecosystem, and what can safely be learned from them without accessing restricted student data or performing intrusive testing? The strongest evidence is uneven. The official MUJ SLCM landing page publicly identifies itself as the "MUJ PORTAL," displays a sign-in path, shows the `@muj.manipal.edu` identity wording, and exposes parent and student login labels [2]. MUJ's official fee page separately states that existing-student online payment uses the student portal URL `https://mujslcm.jaipur.manipal.edu/`, while hostel and mess fees can be paid through the SpaceBasic app [3].

The most directly relevant video located is not on YouTube. It is a public Facebook video titled "MUJ- SLCM - Student Portal Walkthrough," published by JS Group of Institutions, with a visible duration of 1:42, 142 views, and an October 7, 2021 date [10]. The page confirms the title and metadata, but the retrieved public page does not provide a transcript or a reliable description of every screen shown. Therefore, it is evidence that a MUJ SLCM walkthrough was publicly posted, not evidence that every claimed portal feature or technical behavior appears in the recording.

A YouTube page titled "Manipal University - Student Portal & LMS (Learning Management System) Explained | All Doubt Clear" is also relevant. Its description says it concerns Manipal University Jaipur, a BCA course, the student portal, and an LMS walkthrough covering login, usage, features, assignments, books, PDFs, and timetable access [5]. The page identifies a 10:39 duration and a September 5, 2025 publication date [5]. However, the available page evidence does not establish that it demonstrates the MUJ SLCM application specifically, and the retrieved page indicates the video was unavailable to the extractor, so actual screen content cannot be independently verified [5].

The search produced no verified MUJ-specific YouTube fee-payment walkthrough, no verified MUJ-specific YouTube timetable-navigation walkthrough, and no verified MUJ SLCM YouTube video showing browser developer tools, HTTP requests, cookies, or network traffic. Searches repeatedly returned the official portal, official documentation, unrelated university timetable material, general Manipal or Online Manipal pages, and unrelated videos. The official MUJ YouTube channel is a useful provenance control: its visible listings concern institutional, programme, orientation, journey, and convocation content, with no visible SLCM, login, fee-payment, timetable, attendance, or developer-tools tutorial in the extracted listing [11].

**Decision:** treat the Facebook walkthrough as the only clearly MUJ-SLCM-specific public video located; treat the YouTube LMS video as adjacent but not technically conclusive; treat fee and timetable pages as documentary corroboration rather than video evidence; and treat the supplied technology-stack assertions as research hypotheses, not findings, because the retrieved public evidence does not prove ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, or Microsoft 365 identity for this host. Confidence is **high** for the video-discovery conclusions and official visible-label conclusions, **moderate** for the portal-purpose conclusions, and **low** for the requested technology-stack assertions.

## Scope, Safety, and Reproducible Reasoning Summary

The scope was restricted to public search results, public page content, public video metadata, and public documentation. No login was attempted, no credentials were used, no restricted student record was accessed, and no endpoint, parameter, session, CAPTCHA, or network control was tested. That boundary matters because a portal that presents student and parent sign-in controls is an access-controlled service, even when its landing page is publicly reachable [2].

The reasoning process can be reproduced at a high level: first separate the research into login, fees, timetable, technical-video, identity, and provenance questions; next rank primary institutional pages above search-result summaries; then inspect candidate video pages for title, publisher, date, duration, description, and direct evidence of screen content; finally classify each item as confirmed, adjacent, negative result, or unresolved. This is a reproducible reasoning summary, not a disclosure of private chain-of-thought.

The principal false-positive problem was name collision. Searches for "MUJ," "Manipal," and "timetable" returned unrelated content, including a Trent University academic-timetable video. That page describes a 2023-2024 Trent University timetable walkthrough, not MUJ [130.0 and the associated page analysis]. Likewise, a generic Manipal or Online Manipal LMS page cannot automatically be treated as the same system as the MUJ SLCM host. The report therefore preserves those distinctions.

## Evidence Inventory and Confidence Table

| Evidence item | Exact public URL | What the page establishes | What it does not establish | Confidence |
|---|---|---|---|---|
| MUJ SLCM landing page | https://mujslcm.jaipur.manipal.edu/ | Public labels: MUJ PORTAL, Sign In, `@muj.manipal.edu`, Parent Login, Student Login [2] | No authenticated feature set, backend architecture, or security posture | High |
| MUJ SLCM home route | https://mujslcm.jaipur.manipal.edu/Home/Index | Same visible portal identity and login wording [2] | No proof of framework, CDN, or internal routes | High |
| Official fee page | https://jaipur.manipal.edu/pay-fee-online.php | Existing-student payment points to the SLCM URL; hostel/mess payment points to SpaceBasic [3] | No video, no authenticated payment workflow, and no payment-security assessment | High |
| MUJ SLCM Facebook walkthrough | https://www.facebook.com/watch/?v=3067261673486711 | Title, JS Group publisher, 1:42 duration, 142 views, October 7, 2021 [10] | No reliable transcript or complete screen-by-screen proof | High for metadata; low-to-moderate for content |
| MUJ student portal/LMS YouTube video | https://www.youtube.com/watch?v=9R1mCmnhD6Y | Description-supported MUJ portal/LMS subject; login and timetable access are claimed; duration 10:39 [5] | Does not prove SLCM specifically or actual screen content | Moderate for description; low for technical content |
| Official MUJ YouTube channel | https://www.youtube.com/channel/UCFbeX4UJyd4fHTCnCVGob_Q | Channel identity and visible institutional/programme listings [11] | Absence from extracted listings is not proof no video ever existed | Moderate negative evidence |
| MUJ timetable page | https://www.jaipur.manipal.edu/time-table.php | Official page exists and was inspected | Extracted content did not expose an identifiable SLCM navigation tutorial or specific timetable document [166 analysis] | Moderate |
| Independent attendance guide | https://slcm.vercel.app/guides/check-attendance-muj | Third-party guide claims attendance navigation and identifies the MUJ portal [9] | Not university-owned; does not prove official workflow or video content | Moderate for existence of public how-to text |
| MUJStella | https://mujstella.in/ | Self-describes as an independent platform not affiliated with MUJ [6] | Not authoritative evidence about the university portal | High for its own disclaimer |
| Public GitHub SLCM API project | https://github.com/nikeplusdash/SLCM-api | Project describes itself as an API for `https://slcm.manipal.edu` [8] | It targets another Manipal SLCM domain, not proof about MUJ host; code was not used operationally | High for repository description; low for MUJ applicability |

The table's central takeaway is that the public record is stronger for metadata and institutional links than for video content or architecture. A title is not a transcript, an adjacent portal is not the same host, and a project targeting `slcm.manipal.edu` is not evidence about `mujslcm.jaipur.manipal.edu`.

## Login Walkthrough Findings

### The clearly MUJ-specific walkthrough is on Facebook, not YouTube

The strongest exact match is the JS Group of Institutions Facebook recording. Its public metadata states "MUJ- SLCM - Student Portal Walkthrough" [10]. The page identifies JS Group of Institutions as the publisher [10], gives a visible duration of 1:42 [10], reports 142 views [10], and dates the post October 7, 2021 [10]. Those are useful discovery and provenance facts because they establish a public, named, MUJ-SLCM-labelled walkthrough rather than a search-engine guess.

The limitation is equally important. The extracted page contains metadata, not a transcript or a reliable visual inventory. It does not establish whether the recording shows login, attendance, grades, fees, timetable, parent access, or developer tools. Any statement about those screens would be an inference from the title, and the title alone cannot support it. The safe research-club use is to record the URL as a candidate for manual, lawful viewing in an ordinary browser, without signing into the portal or reproducing any personal information that may appear.

### The YouTube candidate is adjacent, not conclusive

The YouTube page "Manipal University - Student Portal & LMS (Learning Management System) Explained | All Doubt Clear" is a useful adjacent result. The page identifies the video as 10:39 long [5] and describes it as a Manipal University Jaipur student portal and LMS walkthrough. Its description says the video concerns the BCA course, student portal, and LMS, and claims coverage of login, usage, features, classes, assignments, books, PDFs, and timetable access [5]. The page analysis also records a September 5, 2025 publication date [5] and the creator name dear dashu [5].

Those claims are description-supported, not independently observed screen facts. The page was unavailable to the extractor and supplied no transcript, so the actual login flow, portal hostname, page paths, request sequence, identity provider, and timetable interface remain unverified [5]. It should therefore be catalogued as "MUJ student portal/LMS explainer, SLCM not confirmed," not as a verified SLCM technical demonstration.

### Official portal labels provide limited corroboration

The official MUJ SLCM page visibly says "WELCOME TO MUJ PORTAL," presents "Sign In," displays `@muj.manipal.edu`, and exposes parent and student login labels [2]. This corroborates that the host is publicly presented as a MUJ portal and that the interface distinguishes student and parent entry points. It does not show what happens after authentication, whether Microsoft 365 is involved, or which backend framework serves the page.

The official MAHE student-portal page should not be conflated with MUJ SLCM. It links to a Student Portal and directs users to `https://sis.manipal.edu/index.aspx` [12]. That is evidence of a separate MAHE SIS portal link, not evidence that SIS, MUJ SLCM, Online Manipal, and the MUJ host are one application. This distinction prevents a common OSINT error: merging portals because they share a parent brand.

## Fee-Payment Research

### What is officially documented

The official MUJ payment page is the strongest fee-related source. It labels the section "PAY FEE ONLINE (Existing Students)" and explicitly gives the Student Portal URL as `https://mujslcm.jaipur.manipal.edu/` [3]. It separately states, "Hostel & Mess fee can be paid via SpaceBasic App" [3]. This supports a system-boundary model in which existing-student academic fee payment is associated with the SLCM portal while hostel and mess payments use a separate application.

The official page also includes annual course-fee notices and transfer-related material [3]. Because those details can change, the page itself should be treated as the authoritative public starting point for current payment instructions, rather than a student video or old social-media post. No bank-account details are reproduced here because they are unnecessary to answer the video-discovery question and could become stale.

### What was not found on YouTube

Repeated searches for MUJ SLCM fee-payment videos returned the official fee page, the SLCM landing page, general fee pages, Reddit discussions, and unrelated refund material. The retrieved video result titled "Manipal Refund Policy 2026" is about refund rules and UGC/AICTE explanations, not a verified MUJ SLCM payment walkthrough [13]. It should not be counted as evidence of the portal's payment screens.

No discovered YouTube page supplied all of the following together: MUJ identity, SLCM hostname, a fee-payment task, and visible or transcript-confirmed portal steps. The correct status is therefore **no verified MUJ SLCM fee-payment video located in this research pass**. This is a bounded negative finding, not proof that no such video exists. YouTube indexing, privacy settings, deletion, regional visibility, title variation, and search-engine ranking can all hide a video.

The security-club implication is to use the official fee page only for awareness and to avoid payment testing. Do not submit payment forms, probe transaction identifiers, attempt to alter amounts, or replay requests. Any authorized assessment would require written permission, a test account, a defined test window, and a payment-provider-approved procedure.

## Timetable and Academic-Calendar Research

The official MUJ timetable page was searched and extracted, but the available content did not expose a clearly identifiable timetable document name, academic period, or SLCM navigation instruction in the relevant extracted portion [166 analysis]. The MUJ homepage does label a "Time Table" area among its public navigation and student-service content [269 analysis], which confirms the existence of an institutional timetable area but not a particular SLCM screen.

Searches also surfaced "How to Navigate the 2023-2024 Academic Timetable," but the page explicitly describes a Trent University timetable walkthrough [1]. It is a false positive and is excluded from the MUJ corpus. This is a valuable example for analysts: a video title containing "academic timetable" does not establish university identity.

The YouTube Manipal student-portal/LMS video claims timetable access in its description [5]. That makes it relevant as a lead, but the page does not prove whether the timetable is the MUJ SLCM timetable, an LMS calendar, a course schedule, or a separate academic-calendar page. It is therefore classified as **description-supported timetable relevance, not verified SLCM timetable footage**.

No MUJ-specific YouTube timetable tutorial with a stable, independently verifiable video URL was located. The research gap is not merely a missing link; it is a missing combination of identity and content evidence. A future analyst should search by department, course, academic year, Hindi transliteration, and phrases students may use instead of "timetable," while maintaining the same false-positive controls.

## Developer Tools, Network Traffic, and Technology Claims

### No verified public video showing developer tools or network traffic

The searches for MUJ SLCM developer tools, Network-panel captures, HTTP requests, cookies, and browser traffic did not return a verified MUJ-specific video. Results included the public portal, unrelated developer-tools discussions, a Chrome extension, third-party guides, and code repositories. The absence of a qualifying video means the report cannot responsibly claim that a public recording exposes API paths, request parameters, response formats, authentication tokens, cookies, or internal service names.

The research boundary is deliberate. Even if a video displayed network traffic, reproducing requests against a live student system could cross from passive OSINT into unauthorized access. A university club can study a publicly posted recording, document visible redacted concepts, and recommend defensive review, but should not replay requests or use captured identifiers.

### Technology-stack assertions remain unverified here

The research brief supplied the hypothesis that the host uses ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 identity. The retrieved public page excerpts do not establish those facts. The MUJ landing page exposes a title, login labels, email-domain wording, and standard page metadata, but the extracted evidence does not show an ASP.NET MVC string, a .NET Framework version, an IIS banner, an Akamai header, or a Microsoft identity-provider redirect [2]. A search for the exact framework version returned the generic Microsoft.AspNet.Mvc NuGet page, which describes the package, not MUJ's deployment [14]. That is not host-specific evidence.

The Microsoft 365 hypothesis also needs separation from ordinary email-domain use. The portal page displays `@muj.manipal.edu` [2], and an indexed Microsoft realm lookup showed a federation-related response for a MUJ email address [15]. That may suggest an enterprise identity relationship, but it does not prove that the SLCM login flow uses Microsoft 365, nor does it establish current configuration, tenant controls, conditional access, or identity federation for this host. This is an **inference**, and it must remain labelled as such.

A public repository titled `SLCM-api` describes an API for `https://slcm.manipal.edu` and lists files such as `SLCM.py` and `SLCM.js` [8]. It is not evidence about the MUJ host because the target domain differs. The repository is useful as ecosystem context only, and it should not be treated as authorization or as a basis for using code against any live portal.

### Defensive interpretation

From a defensive perspective, the public evidence supports a modest asset-inventory conclusion: the MUJ SLCM host has a publicly reachable branded login page and is publicly linked by the university's fee page for existing-student payments [3][2]. It does not support a vulnerability conclusion. A safe club project could create a passive evidence register, compare public page changes over time, verify that videos do not expose personal data, and send responsible disclosure if a public recording reveals credentials or student records. It should not scan, fuzz, authenticate, scrape, or manipulate the live portal without written authorization.

## Adjacent Public How-To Ecosystem and Provenance Controls

The independent betterSLCM guide claims to explain how to check attendance on the MUJ SLCM portal and describes attendance percentages and real-time tracking with predictive analytics [9]. Because the page is on `slcm.vercel.app`, not the university domain, it is third-party documentation. It can help analysts understand the vocabulary students use, but it cannot establish an official workflow, current interface, or university endorsement.

MUJStella is an even clearer provenance case. Its page explicitly says "Independent student platform" and "Not affiliated with Manipal University Jaipur" [6]. Its self-description therefore provides a strong warning against treating student-built tools as official. The presence of a page that claims to access or represent SLCM-related information is not proof of authorization, safety, or official integration.

The official MUJ YouTube channel provides a useful counterweight. It identifies itself as Manipal University Jaipur and describes MUJ as launched in 2011 [11]. Its visible titles concern programmes, campus experiences, orientation, convocation, and institutional storytelling [11]. No SLCM or portal how-to listing was visible in the extracted page. This does not prove that the channel never published one, but it reduces the confidence that the located third-party videos are official university productions.

## Research Gaps and Recommended Next Steps

| Gap | Current status | Safe next step | Do not do |
|---|---|---|---|
| MUJ SLCM YouTube login walkthrough | No exact MUJ-specific YouTube walkthrough verified; adjacent LMS video found | Search title variants, channel pages, playlists, Hindi/English phrasing, and archived public metadata | Do not sign in to validate a video |
| MUJ SLCM fee-payment video | No verified qualifying video | Monitor official MUJ communications and search old public uploads by academic year | Do not submit or alter payment transactions |
| MUJ timetable tutorial | No verified qualifying video; unrelated Trent result excluded | Search course/department and academic-year variants; inspect official timetable documents | Do not access restricted schedules or student records |
| Developer-tools/network video | No verified MUJ-specific result | Review only publicly posted, redacted recordings; ask the publisher for permission if needed | Do not replay captured requests or tokens |
| ASP.NET MVC/.NET/IIS/Akamai attribution | Unproven by retrieved evidence | Obtain an authorized architecture document or passive, consented assessment result | Do not banner-grab or probe the host |
| Microsoft 365 identity | Possible but not established; email-domain and realm evidence are insufficient | Use official IT documentation or written confirmation | Do not test federation, password reset, or tenant behavior |
| Current page and video availability | Time-sensitive and may change | Record access date and preserve URLs, titles, and hashes where lawful | Do not redistribute personal data |

The most valuable next research action is not more generic searching. It is a provenance-focused pass over public MUJ-affiliated channels, student clubs, orientation materials, and dated academic-year posts, using terms such as "SLCM," "student portal," "attendance," "fee payment," "course registration," "class timetable," and local-language variants. Every candidate should be classified by host, publisher, date, and whether actual screen content is independently visible.

## Synthesis

The evidence divides the ecosystem into three layers. First is the official access layer: the MUJ SLCM page visibly identifies the portal and login roles, while the official fee page links existing-student payment to that host [2][3]. Second is the public-explainer layer: the Facebook recording is explicitly MUJ SLCM-labelled, while the YouTube recording is a broader MUJ student-portal/LMS explanation [10][5]. Third is the unofficial-support layer: independent guides and student-built platforms discuss or wrap SLCM-related functionality but expressly lack university affiliation [9][6].

Across **identity**, the official host is strongest because it carries the MUJ portal wording and the `@muj.manipal.edu` label [2]. Across **content specificity**, the Facebook title is stronger than the YouTube description because it names "MUJ- SLCM" directly [10]. Across **screen-level verifiability**, neither is sufficient in the extracted corpus: the Facebook page lacks transcript-level details, and the YouTube page was unavailable to the extractor [10][5]. Across **institutional provenance**, the official MUJ channel is stronger than third-party publishers, but its visible listing did not contain the requested tutorials [11].

The main tension is between discoverability and authority. The most specific walkthrough is third-party, while the official channel is authoritative but not visibly instructional. The official fee page is authoritative for payment-channel association, but it is not a video and does not reveal authenticated workflow details. The independent attendance guide is more operationally descriptive than the official landing page, but its non-affiliation means it cannot be used as a definitive security or product specification.

The same tension applies to technology attribution. A branded login page can support asset identification, but it cannot prove the server framework, reverse proxy, CDN, or identity architecture. A generic package page, a separate Manipal SLCM repository, or a Microsoft realm response may provide context, but none establishes the supplied stack for the MUJ host. The responsible conclusion is therefore conservative: public material confirms an access-controlled MUJ portal and related student-service ecosystem, but does not confirm the requested implementation stack or expose a qualifying technical video.

## VERDICT

**Overall confidence: Moderate to high for the public-video inventory; high for official visible portal and fee-link facts; low for implementation-stack attribution.**

1. **Confirmed:** The public MUJ SLCM page presents itself as the MUJ Portal and exposes student and parent sign-in labels with MUJ email-domain wording [2].
2. **Confirmed:** The official MUJ fee page associates existing-student online payment with the SLCM URL and separately directs hostel and mess payment to SpaceBasic [3].
3. **Confirmed:** A public Facebook recording titled "MUJ- SLCM - Student Portal Walkthrough" was posted by JS Group of Institutions on October 7, 2021; its page shows 1:42 and 142 views [10].
4. **Partially confirmed:** A YouTube video describes a MUJ student portal/LMS walkthrough, including claimed login and timetable access, but SLCM identity and actual screen content are not independently verified [5].
5. **Not found in this pass:** A verified MUJ-specific YouTube fee-payment tutorial, a verified MUJ-specific YouTube timetable tutorial, or a verified MUJ SLCM video showing developer tools or network traffic.
6. **Unresolved:** The supplied claims about ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 identity are not established by the retrieved public evidence. The Microsoft 365 link is only an inference from domain/federation context and must not be reported as confirmed [15][2].

For a university security club, the actionable conclusion is to preserve the exact URLs and provenance, use the videos only as public awareness material, redact any personal information in notes or screenshots, and pursue any deeper technical assessment only under written authorization. The current evidence supports OSINT documentation, not vulnerability claims or live-system testing.

## Exact URL Reference Table

| Reference | Exact URL |
|---|---|
| Official MUJ SLCM portal | https://mujslcm.jaipur.manipal.edu/ |
| Official MUJ SLCM home route | https://mujslcm.jaipur.manipal.edu/Home/Index |
| MUJ official fee page | https://jaipur.manipal.edu/pay-fee-online.php |
| MUJ official timetable page | https://www.jaipur.manipal.edu/time-table.php |
| MUJ SLCM Facebook walkthrough | https://www.facebook.com/watch/?v=3067261673486711 |
| MUJ student portal/LMS YouTube video | https://www.youtube.com/watch?v=9R1mCmnhD6Y |
| Official MUJ YouTube channel | https://www.youtube.com/channel/UCFbeX4UJyd4fHTCnCVGob_Q |
| Independent attendance guide | https://slcm.vercel.app/guides/check-attendance-muj |
| Independent MUJStella platform | https://mujstella.in/ |
| Separate Manipal SLCM API repository | https://github.com/nikeplusdash/SLCM-api |
| Official MAHE student portal page | https://www.manipal.edu/mu/academics/student-portal.html |
| Generic MVC package page, not MUJ evidence | https://www.nuget.org/packages/Microsoft.AspNet.Mvc |
| Microsoft realm lookup indexed during research | http://login.microsoftonline.com/getuserrealm.srf?login=probe@muj.manipal.edu&xml=1 |

The URLs are included for research traceability. Access should remain within ordinary public browsing and institutional authorization boundaries.

## References

1. *How to Navigate the 2023-2024 Academic Timetable*. https://www.youtube.com/watch?v=1v0QXkIpkGo
2. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
3. *Pay Fee Online - Manipal University Jaipur *. https://jaipur.manipal.edu/pay-fee-online.php
4. *Time Table - Manipal University Jaipur *. https://www.jaipur.manipal.edu/time-table.php
5. *Manipal University - Student Portal & LMS (Learning ...*. https://www.youtube.com/watch?v=9R1mCmnhD6Y
6. *MUJStella - Student Platform for Manipal University Jaipur*. https://mujstella.in/
7. *Manipal University Jaipur - 71 years of legacy of Manipal Education*. https://jaipur.manipal.edu/
8. *GitHub - nikeplusdash/SLCM-api: An api for https://slcm.manipal.edu · GitHub*. https://github.com/nikeplusdash/SLCM-api
9. *How to Check Your Attendance at MUJ | mujslcm Guide | betterSLCM*. https://slcm.vercel.app/guides/check-attendance-muj
10. *MUJ- SLCM - Student Portal Walkthrough | JS Group of Institutions | Facebook*. https://www.facebook.com/watch/?v=3067261673486711
11. *Ucfbex4Ujyd4Fhtcncvgob Q*. https://www.youtube.com/channel/UCFbeX4UJyd4fHTCnCVGob_Q
12. *Student Portal Login- MAHE (Manipal Academy Of Higher Education)*. https://www.manipal.edu/mu/academics/student-portal.html
13. *MUJ fee deadline ??? : r/manipaljaipur*. https://www.reddit.com/r/manipaljaipur/comments/1uaqh0g/muj_fee_deadline
14. *NuGet Gallery | Microsoft.AspNet.Mvc 5.3.0*. https://www.nuget.org/packages/Microsoft.AspNet.Mvc
15. *login.microsoftonline.com*. http://login.microsoftonline.com/getuserrealm.srf?login=probe@muj.manipal.edu&xml=1
