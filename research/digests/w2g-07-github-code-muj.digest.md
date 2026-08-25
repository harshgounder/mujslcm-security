# Digest: w2g-07-github-code-muj.md

## REPORT
Source file: w2g-07-github-code-muj.md. Public GitHub exposure assessment for the MUJ SLCM vocabulary (mujslcm, mujslcm.jaipur.manipal.edu, slcm.manipal.edu, jaipur.manipal.edu, muj.manipal.edu). Source-inventory report with a full 76-entry reference table; no live testing performed.

## ANSWER SUMMARY
- Overall confidence: High for public artifact identification, medium for exposure severity, low for live compromise or exploitability. A repo page proves a public artifact was visible, not deployment or current validity.
- Top finding: KrishGoel/slcm-feedback-automation .env.example shows populated name, registration number, and password-like value instead of placeholders. Values redacted in the report; treat as potentially compromised, rotate through the university process, clean git history, do not test the value.
- Secondary finding: vikrant500/college_portal_web_and_dbms portal-clone dir holds an HTTrack cookies.txt with a populated __RequestVerificationToken entry for the MUJ host. Classified as sensitive token-like artifact, validity unknown.
- DK10WS/SLCM_APP (Flutter) is the richest route map: MUJ base URL, Student/Academic/GetAttendanceSummaryList, parent OTP paths, dashboard, GitHub release-check; cookie-bearing POSTs, CSRF token parsing, JSON response parsing, change-password flow. Session cookie held in a static string; username and password saved through shared preferences.
- Tejas-Narula/SlcmPlus is DOM-only Chrome MV3 augmentation on exact MUJ attendance, marks, and grades pages; computes attendance, internal marks, GPA. No credential or external API client visible in cited excerpts.
- AddisionS/slcm-feedback-form-filler sets feedback controls to all-Yes or all-No and clicks submit; manifest declares <all_urls>, *://*/*, scripting, activeTab, broader than the MUJ-specific description.
- Legacy wrappers manipalthetalk/App-Backend, canaryGrapher/slcmAPI, nikeplusdash/SLCM-api target slcm.manipal.edu, not Jaipur. App-Backend server.go interpolates regno and password into a shell command (inferred command-injection risk) and sets wildcard CORS with a regno-keyed cache.
- GitHub artifacts do not independently verify ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai, or Microsoft 365 federation; those stay requester-supplied context. Client code is not a server fingerprint.

## KEY FACTS
- https://github.com/KrishGoel/slcm-feedback-automation/blob/main/.env.example - populated credential-like values; highest-priority public secret finding.
- https://github.com/vikrant500/college_portal_web_and_dbms/blob/main/mujslcm.jaipur.manipal.edu_122/cookies.txt - public HTTrack cookie file with verification-token entry for the MUJ host.
- https://github.com/DK10WS/SLCM_APP/blob/main/lib/pages/redirects.dart - MUJ base URL plus attendance, parent-OTP, dashboard, and release-check route constants.
- https://github.com/DK10WS/SLCM_APP/blob/main/lib/pages/login.dart - parses hidden __RequestVerificationToken, posts EmailFor, LoginFor, UserName, Password for student and parent modes, handles redirects and OTP.
- https://github.com/DK10WS/SLCM_APP/blob/main/lib/session_manager.dart - session cookie in a static string; presence of the string equals login state.
- https://github.com/DK10WS/SLCM_APP/blob/main/lib/utils/util.dart - adds Cookie headers and reads saved username/password from shared preferences.
- https://github.com/DK10WS/SLCM_APP/blob/main/lib/pages/Attendance.dart - cookie-bearing POST to the attendance constant; parses AttendanceSummaryList with course id, percentage, total and attended classes.
- https://github.com/Tejas-Narula/SlcmPlus/blob/main/manifest.json - MV3 content script matching exact MUJ academic page URLs.
- https://github.com/Tejas-Narula/SlcmPlus/blob/main/content.js - table-cell reads, marks and GPA calculations, mutation observer; no network call or credential visible.
- https://github.com/AddisionS/slcm-feedback-form-filler/blob/main/chrome/manifest.json - broad host permissions incl. <all_urls> and *://*/*.
- https://github.com/AddisionS/slcm-feedback-form-filler/blob/main/chrome/content.js - sets radio/dropdown values, dispatches change events, can click btnSubmit.
- https://github.com/manipalthetalk/App-Backend/blob/master/server.go - forms a shell command from user-supplied regno and password; wildcard CORS; cache keyed by regno.
- https://github.com/canaryGrapher/slcmAPI/blob/master/server.js - archived Puppeteer REST wrapper with /getscores, /getattendance, /getprofile, /validateuser; deprecated after portal CAPTCHA.
- https://github.com/sankalp2004/SLCM-is-Dumb/blob/master/.env.example - placeholder-only credentials (low signal); targets non-Jaipur slcm.manipal.edu.
- https://github.com/KrishGoel/slcm-feedback-automation/blob/main/script.py - Selenium flow: opens MUJ root, fills UserName and Password, filters pending feedback, enters fixed comment, submits.

## ACTIONABLE LEADS
- Disclosure steps: notify the KrishGoel and vikrant500 repository owners plus the university security or identity team through an established channel; rotate the account password, revoke active sessions, remove values from current files and git history, run repository secret scanning. Never use any exposed value against the service.
- GitHub governance: enable secret scanning and push protection, review forks and historical commits, and create a disclosure playbook covering passwords, session cookies, CSRF tokens, screenshots, logs, and downloaded HTML.
- Use DK10WS route names (Student/Academic/GetAttendanceSummaryList, dashboard, parent OTP, change-password) as an endpoint inventory to reconcile against the live portal during authorized review; treat the route existence as code-level map only.
- Review the vikrant500 clone tree (cookies.txt, hts-log.txt, Scripts, Home/Index.html) for additional downloaded browser state; treat all of it as sensitive historical material.
- Code-review targets from legacy wrappers: shell interpolation, CORS, regno-keyed cache isolation, CAPTCHA control boundaries, session expiry, logging of headers.
- Engineering actions for the Flutter client: platform secure storage, no long-lived password retention, short-lived refreshable sessions, centralized expiry, clear all cached headers on logout.

## FLAGS
- Credential and token values are redacted in the report; validity, account ownership, session binding, and expiry are unknown. Exposure is proven, exploitability is not.
- Repos are student projects, not university-owned; deployment and production build matching are unverified (explicitly unknown for the Flutter app).
- slcm.manipal.edu artifacts (App-Backend, slcmAPI, SLCM-api, SLCM-is-Dumb) are a different host and older ecosystem; reusing their routes against the Jaipur host would be an unsupported inference. SLCM-is-Dumb README even mentions CAPTCHA, and slcmAPI is archived/deprecated.
- Documentation drift: KrishGoel README says run main.py while the tree and cited source identify script.py; report flags it as maintenance, not a vulnerability.
- Several reference URLs use http:// (AddisionS, canaryGrapher, nikeplusdash) instead of https://; verify redirects before relying on the link form.
- The broader Manipal ecosystem (AttendanceSummaryList-style routes, .aspx paths in legacy code) is used only as comparison evidence; the report says it cannot verify the MUJ server stack.

## COVERAGE
- File: w2g-07-github-code-muj.md.
- 257 lines total; 48,461 bytes on disk; 48,321 chars read.
- Method: read_file offset 1, limit 2000, single call.
- EOF confirmed: final call returned truncated: false, last content line 257 equals total_lines 257.