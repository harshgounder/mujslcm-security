# CONTEXT-SYNTHESIS

Scope: 26 digests (w2e-01..12, w2g-01..14) read in full, all EOF confirmed. Target: https://mujslcm.jaipur.manipal.edu. Every claim below cites its digest. Stack facts marked unverified stay unverified; header observation in w2g-14 is the only independent fingerprint.

## 1) PRECEDENT SUMMARY

What other Indian universities, VDPs, and disclosures say about running this engagement safely and getting credit.

- IISc is the only verified first-party campus-wide Indian university VDP: wildcard *.iisc.ac.in, public APIs, mobile apps, no cash bounty, 5-working-day acknowledgment target, ciso@iisc.ac.in (w2e-03). No surveyed university expressly names a student portal in a verified VDP; IISc portal coverage is an inference from the wildcard (w2e-03).
- CERT-In RVDCP coordinates voluntary disclosure: 72-working-hour acknowledgment, 120-day resolution window, no safe harbor, no blanket testing permission, finder stays responsible (w2e-02, w2e-03, w2e-12). The 2022 Directions impose a six-hour incident-reporting clock and 180-day India-resident log retention on covered entities; that duty does not name independent researchers (w2e-01, w2e-02, w2e-11).
- Indian reception varies sharply. IIT Roorkee publicly praised a 16-year-old who found a JEE Advanced portal flaw (w2e-02). CBSE drew an alleged months-long silence before a containment statement (w2e-02). Zomato fixed in a day and published after the fix (w2e-02). IRCTC insurance portal went via CERT-In: report July 23, fix confirmed July 30 (w2e-02).
- University breach history is marks- and identity-centric: Bengaluru North marks tampering via registrar credentials (60+ students, INR 15,000-20,000 per student, three arrests), Bangalore University OTP bypass (55 students), Gauhati cash-for-marks via outsourced data entry (50+ students, 9 arrests) (w2e-01). Payments: fake receipt forgery at Sri Venkateswara University and look-alike domain diversion at Sai Nath (w2e-01). AIIMS ransomware: 5 of 140 servers infected, theft claims reported baseless; infection does not equal exfiltration (w2e-01).
- Disclosures finish weak: 5 of 7 core cases reached police, none published a full technical postmortem; credential acquisition paths remain unknown (w2e-01).
- IITK B.Cyber Pingala case is the direct defensive lesson: client-side CAPTCHA and per-browser OTP limit were reported and allegedly patched with server-side validation and rate limits; a client-visible control must not be the sole enforcement point (w2g-02).
- 90 days is a Project Zero coordination norm, not law and not MUJ policy; publication must be negotiated separately (w2e-02). Model clocks: 3-business-day acknowledgment, 14-day triage, 45-day critical target, 90-day ceiling, separate publication decision; track acknowledgment, technical confirmation, containment, and credit as four separate outcomes (w2e-02).
- Legal boundary: IT Act Sections 43 and 66 make authorization the hard line; written, asset-specific scope is required before any active validation (w2e-02). No safe harbor exists anywhere in the Indian path (w2e-02, w2e-12).
- Practical posture consensus across all digests: policy design and passive OSINT now, no active testing until written authorization; ask MUJ for a named security intake first (w2e-02, w2e-03, w2e-06, w2e-11).

## 2) VENDOR/PRODUCT-FAMILY PICTURE

What SLCM is, who may own it, sibling instances worldwide.

- SLCM = Student Life Cycle Management, an ecosystem label, not one product. MAHE defines it as the single-window suite for attendance, internal and external marks, results, and circulars for students and parents; it replaced the older Academic Management System (w2e-02, w2e-05, w2e-06, w2e-08).
- The vendor behind the current MUJ backend is not publicly established (w2e-04). Model it as layers: portal, ERP core, identity, hosting, integrator (w2e-04).
- Historical packaged-core lead: SAP Student Lifecycle Management, self-reported implementation across Manipal Education entities in 2012 and configuration from 2011 (LinkedIn self-reports, no first-party contract; w2e-04).
- Modernization: Salesforce (Agentforce Education, Data 360, MuleSoft, Tableau) with Deloitte as integrator, announced for MAHE-wide SLCM in March 2026; five AI agents placed in SLCM under the MAGIC program. MAHE-wide, does not prove the MUJ host is Salesforce-based (w2e-04, w2g-08).
- Front end: MUJ login is confirmed Keen product lineage via archived asset paths /keen/themes/keen/theme/demo1/dist/ with login-v1.css and bundles; exact release unverified. demo1 is a layout/build identifier, not a version, staging flag, or default-account evidence (w2e-10). Metronic-family comparators: Netkampuss ERP (sch-avms.netkampus.in) and Avenu Learning LMS India (learn-india.avenulearning.com), versions undisclosed (w2e-10).
- Runtime fingerprint (25 Aug 2026 public header observation): Microsoft-IIS/10.0, X-AspNetMvc-Version: 5.3, X-AspNet-Version: 4.0.30319, X-Powered-By: ASP.NET, X-Frame-Options: SAMEORIGIN. Supports the supplied IIS/MVC 5.3/.NET-family stack for that one observed response only; X-AspNet-Version 4.0.30319 is a version family, not a patch-level inventory (w2g-14). The "MVC 5.3" vs NuGet Microsoft.AspNet.Mvc 5.2.9 discrepancy stands (w2e-06). ".NET Framework 4.x" spans retired releases; only 4.8.1 stays supported (w2e-05, w2e-11).
- Two implementation eras: legacy slcm.manipal.edu shows 2017-2026 Web Forms vocabulary (.aspx routes, MicrosoftAjax assets, jQuery 2.0.3); the MUJ host appears 2025+ with MVC-shaped /Home/Index and Keen assets (w2g-14). Separate hosts, separate timelines; shared backend unproven.
- Sibling instances worldwide: slcm.manipal.edu (MAHE, Web Forms), slcm.manipaldubai.com (Dubai, moderate-high confidence of a separate application generation; UNIKUL-built Android apps MAHE DUBAI-SLCM package com.unikul.manipaldubai, 1K+ downloads, and M-Campus com.unikul.mahedubai, 50+ downloads) (w2e-04, w2e-07), student.manipal.edu.my (Malaysia; entity ambiguity MILA/MUCM/MIU; React-style shell, Clarity analytics; shared family plausible, shared codebase not demonstrated) (w2e-09), muj.slcm.jaipur.manipal.edu (alternate MUJ host; alias or separate deployment unconfirmed) (w2e-04, w2e-11, w2g-03, w2g-12), maheslcmtech.manipal.edu (modernization endpoint with Microsoft tenant SAML path) (w2e-04).
- Outside MAHE but same label family: SMUERP v5 + Vidya (KEN, SMU O365) at Sikkim Manipal (w2e-08), Amizone as the MVC-family near peer (w2e-11).
- Non-attributions to drop: Comviva, Manipal Technologies, JAIN/JGI, Unikul for MUJ, Saral, MasterSoft, Serosoft, TCS iON, Samarth, Hexad, Fedena (w2e-04, w2e-05). Fedena 2.3 open source has the only strong product-level vulnerability record in the set, inapplicable to MUJ unless a tenant is ever confirmed (w2e-05).

## 3) PUBLIC FOOTPRINT

Code, credentials, app stores, communities.

- Top credential finding: KrishGoel/slcm-feedback-automation .env.example carries a populated name, registration number, and password-like value instead of placeholders; treat as potentially compromised, rotate through the university process, clean git history, never test the value (w2g-07, w2g-11).
- Secondary: vikrant500/college_portal_web_and_dbms holds an HTTrack cookies.txt with a populated __RequestVerificationToken entry for the MUJ host; validity unknown (w2g-07).
- Route map: DK10WS/SLCM_APP (SLCM SWITCH, Flutter/FastAPI, 71 commits, created Jun 18 2025) discloses MUJ base URL, Student/Academic/GetAttendanceSummaryList, parent OTP paths, dashboard, change-password flow; session cookie held in a static string, username/password saved via shared preferences (w2g-06, w2g-07).
- Extension cluster: Tejas-Narula/SlcmPlus is DOM-only MV3 augmentation on exact MUJ attendance/marks/grades pages, no credential or network call visible; Chrome Web Store listing unconfirmed (w2g-06, w2g-07, w2g-11). AddisionS/slcm-feedback-form-filler declares <all_urls> and *://*/*, broader than its MUJ description (w2g-07). Firefox SLCM Feedback Auto-Fill requests all-websites access; Detain Shield claims MUJ-only attendance use; both are publisher disclosures, not audits (w2g-04).
- Legacy wrappers target slcm.manipal.edu, not Jaipur: manipalthetalk/App-Backend interpolates regno and password into a shell command (inferred command-injection risk) with wildcard CORS; canaryGrapher/slcmAPI is archived/deprecated; nikeplusdash/SLCM-api advises session logout; sankalp2004/SLCM-is-Dumb runs Selenium/OCR CAPTCHA automation with an .env warning, high sensitivity (w2g-06, w2g-07, w2g-11).
- Registries: zero-object response for mujslcm on npm; no PyPI listings; the only clear published SLCM utility is npm yemit (MIT Manipal, not MUJ). MUJ footprint lives in source channels (GitHub, extensions, APKs, demos), not registries (w2g-11).
- Decoys and non-affiliated: MUJStella, betterSLCM (slcm.vercel.app), slcm-client-unoff.vercel.app, muj.onlinemanipal.com, student.mujonline.com, MUJ-Central, SlcmAndLms-aggregator, Geervan demo (w2g-03, w2g-05, w2g-06, w2g-11).
- App stores: UNIKUL Dubai apps above; SpaceBasic is the official hostel/mess fee channel per the MUJ fee page (w2e-07, w2g-05).
- Communities: Telegram @manipaljaipurfresher (447 direct vs 1,572 directory, counts diverge, do not merge), Discord servers at 1,142 and 1,902 members with no confirmed university endorsement (w2g-13). Reddit: availability complaints (SLCM "crashing every other day"), registration-number rejection after intra-sliding, fee-paid-but-pending, removed results tab, grades decreased; the CGPA leak allegation is unverified with a single commentator's patch claim (w2g-01, w2g-02, w2g-04). Quora footprint is thin, one anonymous attendance answer (w2g-03). X: @Jaipur_Manipal posts are routine campus content; direct X search returned no tweet cards (w2g-04).
- Documents: Scribd hosts a 2025 grade sheet with an SLCM-derived path in the title and a third-party "Eligible Students MUJ-1" claim of registration data; provenance unknown, report privately, never redistribute (w2g-04, w2g-12). Stack Overflow: zero literal mujslcm hits; two Manipal SMTP samples expose a BOPSERVER/Project connection string and a 584-vs-587 port discrepancy, no MUJ-host evidence (w2g-10). Dorks found no confirmed first-party student-record exposure; XLSX-titled results resolving to PDF URLs are a recurring trap (w2g-12).
- Closest security-adjacent official items: FAQ names dms@jaipur.manipal.edu and ams@jaipur.manipal.edu for login trouble and the SLCM registration link (w2g-04); Office 365 SOP v1.0 June 2025 documents mandatory MFA (w2e-11, w2g-08).

## 4) DISCLOSURE PATH

Best practice for MUJ.

- Two parallel tracks for a real finding: confidential notice to MUJ IT and Registrar, plus a direct RVDCP report to vdisclose@cert-in.org.in. Do not wait for a publicly listed nodal officer; none was found (w2e-12).
- MUJ contacts: it.support@jaipur.manipal.edu (IT Infrastructure, extensions 778/300), registrar@jaipur.manipal.edu (Dr Amit Soni, ext 102), registrar.office@jaipur.manipal.edu, admin.office@jaipur.manipal.edu, plus dms@ and ams@ for login-trouble routing (w2e-03, w2e-12, w2g-04). No public security mailbox, VDP, or conforming security.txt exists; the RFC 9116 location returns the portal sign-in page (w2e-03).
- CERT-In lanes: vdisclose@ (RVDCP voluntary coordination, 72-hour ack, 120-day resolution), incident@ for suspected Annexure I incidents (six-hour clock), info@ for general contact; the linked certinvulnform.pdf returned not found at research time, email is the reliable mechanism (w2e-12). Route by ownership: MSRC only for demonstrable Microsoft product flaws, security@akamai.com only for Akamai platform defects; MAHE information-security policy must not be presented as MUJ policy without confirmation (w2e-12).
- 90-day norm: cite Project Zero policy (90-day vendor window, 30-day post-patch disclosure, seven-day for active exploitation) as the coordination model, not as permission; publication is a separate negotiated decision (w2e-02).
- What to document: a report envelope with subject, classification, timing, prior disclosure, researcher preference; a reproducible CVSS v4.0 vector plus an MUJ-specific impact statement; redacted evidence only (no cookies, tokens, credentials, grades, or student identifiers); a timeline tracking acknowledgment, technical confirmation, containment, and credit separately (w2e-02, w2e-12).
- First move: governance request for written scope from MUJ IT, then a proposed MUJ VDP modeled on IISc (policy URL, valid security.txt, named assets, explicit portal status, prohibited techniques, response targets, safe-harbor wording) (w2e-03). No active testing until written authorization exists (w2e-02).
- Stop conditions in club rules: stop at first sensitive record, unexpected privilege, or instability (w2e-02).

## 5) TOP GAPS IN KNOWLEDGE

- Vendor identity of the MUJ SLCM backend: unconfirmed. SAP historical, Salesforce future, current Jaipur backend unknown (w2e-04, w2g-08).
- Is muj.slcm.jaipur.manipal.edu a live alias or a separate deployment? Every digest flags it; owner confirmation required (w2e-04, w2e-05, w2g-03, w2g-04, w2g-12).
- Exact software bill of materials: MVC 5.3 header observed once; .NET patch level, IIS build, NuGet packages, jQuery/Bootstrap versions, Akamai presence all unverified (w2e-05, w2e-06, w2e-10, w2g-14).
- Whether the CERT-In 2022 Directions apply to MUJ as a covered entity: not legally resolved; MUJ counsel should confirm (w2e-12).
- Identity and tenant equivalence across Manipal campuses: Dubai (Microsoft not named on login), Malaysia (MUCM/MILA ambiguity), MUJ (managed Microsoft tenant, MFA SOP). Do not assume one tenant, one flow, or shared codebase (w2e-07, w2e-09, w2e-11).
- Validity and ownership of the KrishGoel credential-like values and the vikrant500 token file: exposure proven, exploitability unknown (w2g-07).
- Provenance of Scribd artifacts (grade sheet, "Eligible Students" list): user upload, misconfiguration, or unrelated posting; unknown (w2g-04, w2g-12).
- Personnel who own or maintain the Jaipur host: four direct SLCM leads (Upadhyay, Vishwaradhya, Khalandar, Muthamadhu) and MUJ-local candidates, none publicly tied to the Jaipur host (w2g-08).
- Salesforce migration timing and effect on the current portal: MAHE-wide announcement only; no MUJ-host evidence (w2e-04, w2g-08).
- No public security intake, no nodal officer, no security.txt: the disclosure routing itself is unconfirmed beyond registrar and IT Infrastructure forwarding points (w2e-03, w2e-12).

## 6) COVERAGE TABLE

All files read via read_file to EOF (truncated: false on every final read). Chars = bytes on disk.

| Digest | Chars read | EOF |
|---|---|---|
| w2e-01-india-uni-breach-history | 5,477 | yes |
| w2e-02-india-uni-vdp | 4,852 | yes |
| w2e-03-disclosure-case-studies | 4,301 | yes |
| w2e-04-slcm-vendor-id | 4,438 | yes |
| w2e-05-india-erp-vendors | 4,392 | yes |
| w2e-06-mit-manipal-systems | 4,468 | yes |
| w2e-07-manipal-dubai | 4,988 | yes |
| w2e-08-sikkim-manipal | 4,759 | yes |
| w2e-09-manipal-malaysia | 4,708 | yes |
| w2e-10-keentheme-portals | 4,658 | yes |
| w2e-11-iis-mvc-student-portals | 4,988 | yes |
| w2e-12-certin-bugbounty | 5,042 | yes |
| w2g-01-reddit-r-manipal | 4,665 | yes |
| w2g-02-reddit-india-academics | 4,958 | yes |
| w2g-03-quora-manipal | 4,247 | yes |
| w2g-04-twitter-x | 4,906 | yes |
| w2g-05-youtube-tutorials | 4,635 | yes |
| w2g-06-github-orgs-clubs | 5,031 | yes |
| w2g-07-github-code-muj | 7,656 | yes |
| w2g-08-linkedin-sicm-devs | 7,700 | yes |
| w2g-09-job-postings | 7,009 | yes |
| w2g-10-stackoverflow | 8,125 | yes |
| w2g-11-npm-pypi | 7,309 | yes |
| w2g-12-google-dorks | 6,604 | yes |
| w2g-13-telegram-discord | 7,707 | yes |
| w2g-14-wayback-family | 8,490 | yes |
| TOTAL | 146,113 | 26/26 EOF |