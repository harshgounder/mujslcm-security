# Digest: w2g-14-wayback-family.md

## REPORT
Source file: w2g-14-wayback-family.md. Archive evidence and codebase evolution study for the Manipal SLCM ecosystem: Wayback CDX queries, archived replays, current public pages, official FAQ, MAHE student-portal page, a public header observation, and Microsoft OpenID metadata. Evidence labels: Observed, Strong inference, Working inference, Unknown. 29 references.

## ANSWER SUMMARY
- Verdict: Medium-high confidence for the historical surface and the current public technology fingerprint; medium for the migration narrative; low-to-medium for removed pages, direct Microsoft SSO, and Akamai. The public ecosystem shows at least two implementation eras.
- Legacy host slcm.manipal.edu (2017-2026 corpus): .aspx route vocabulary including loginForm.aspx, StudentChangePassword.aspx, ParentChangePassword.aspx, Academicdashboard.aspx, ClassAttendance.aspx, CourseFeedback.aspx, CreateTimeTable.aspx, GradeSheet.aspx, Pre-Registration.aspx, Results.aspx, mostly with 302/303 records; MicrosoftAjax Web Forms assets (Jan 2019); Bootstrap and jQuery 2.0.3 assets (Apr 2018); later Print.aspx and PaymentResponse.aspx captures (query values omitted).
- MUJ host mujslcm.jaipur.manipal.edu (2025+): public login shell only. Home/Index captured 10 Jan 2025, root captured 27 May 2025 with "WELCOME TO MUJ PORTAL" and Sign In; Keen login-v1.css, pages/custom/user/login.js, scripts.bundle.js; current form exposes txtUserName, txtPassword, hidden login-context fields, a verification-token field, and Forgot Password linking to passwordreset.microsoftonline.com.
- WebForm1.aspx lesson: the CDX row shows status 200 (30 Mar 2022) but the replay body is an explicit 404 Error Page; archive metadata must always be read with body and timestamp.
- Header fingerprint (25 August 2026, public API observation): HTTP 200, Microsoft-IIS/10.0, X-AspNetMvc-Version: 5.3, X-AspNet-Version: 4.0.30319, X-Powered-By: ASP.NET, X-Frame-Options: SAMEORIGIN. Supports the supplied IIS/MVC 5.3/.NET-family stack for the observed response only.
- Identity: the FAQ says the SLCM password follows the official Outlook ID and documents AMS and Outlook support routes; the public OpenID configuration endpoint for muj.manipal.edu returns Microsoft tenant metadata. Direct SLCM OIDC use is unproven: no client identifier, redirect URI, callback, or token exchange is cited.
- 404 and 302 patterns coexist for the same route families (including misspellings like gardesheet.aspx), so intentional removal is unproven; "removed page" claims require a before-and-after body comparison.
- Akamai is not independently confirmed in this corpus; it stays an external research premise.

## KEY FACTS
- https://web.archive.org/cdx/search/cdx?url=mujslcm.jaipur.manipal.edu/*&from=2025&output=json&filter=statuscode:200&collapse=urlkey - MUJ 200 corpus; Home/Index (10 Jan 2025) and root (27 May 2025) HTML captures.
- https://web.archive.org/web/20170714034235id_/http://slcm.manipal.edu:80/loginForm.aspx - 2017 legacy login replay; branded page with incomplete replay body.
- https://web.archive.org/web/20170720030733id_/http://slcm.manipal.edu:80/StudentChangePassword.aspx - student password-change page; old, new, and confirmation labels.
- https://web.archive.org/web/20170813123113id_/http://slcm.manipal.edu:80/ParentChangePassword.aspx - separate parent password-change page with the same labels.
- https://web.archive.org/cdx/search/cdx?url=slcm.manipal.edu/*&from=2017&output=json&filter=statuscode:3..&filter=urlkey:.*(academic|dashboard|attendance|timetable|result|grade|registration|course|login|parent|student).*&collapse=urlkey - 302/303 route-vocabulary corpus for the legacy academic route family.
- https://web.archive.org/cdx/search/cdx?url=slcm.manipal.edu/*&from=2017&output=json&filter=statuscode:404&filter=mimetype:text/html&collapse=urlkey - legacy 404 corpus including GradeSheet, Grade.Sheet, Gradsheet, gardesheet, marksheet, Result, Results, Re_Registration variants.
- https://web.archive.org/web/20220330054426id_/https://slcm.manipal.edu/WebForm1.aspx - CDX 200 row whose body is a 404 Error Page; the report's central status-versus-body case study.
- https://web.archive.org/cdx/search/cdx?url=slcm.manipal.edu/Scripts/*&from=2017&output=json&filter=statuscode:200&collapse=urlkey - MicrosoftAjax.js and MicrosoftAjaxWebForms.js captures, a Web Forms-era signal (Jan 2019).
- https://web.archive.org/cdx/search/cdx?url=slcm.manipal.edu/assets/*&from=2017&output=json&filter=statuscode:200&collapse=urlkey - Bootstrap CSS/JS, jQuery 2.0.3, and MU-branded image assets (24 Apr 2018).
- https://web.archive.org/web/20250527044058id_/https%3A//mujslcm.jaipur.manipal.edu/ - 27 May 2025 MUJ root replay; "WELCOME TO MUJ PORTAL" and Sign In.
- https://mujslcm.jaipur.manipal.edu/Home/Index - current MUJ surface; student and parent login labels, @muj.manipal.edu.
- http://api.hackertarget.com/httpheaders?q=https://mujslcm.jaipur.manipal.edu/ - 25 Aug 2026 header observation: IIS 10.0, MVC 5.3, ASP.NET 4.0.30319, SAMEORIGIN.
- http://login.microsoftonline.com/muj.manipal.edu/.well-known/openid-configuration - Microsoft identity metadata (issuer, auth/token endpoints, Graph hosts) for the domain; tenant-level, not SLCM-level.
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - official FAQ: registration link, Outlook-ID password wording, AMS contact routes, Outlook troubleshooting via Team IT Infra.
- https://web.archive.org/cdx/search/cdx?url=slcm.manipal.edu/*&from=2017&output=json&filter=statuscode:200&filter=mimetype:text/html&collapse=urlkey - legacy HTML 200 corpus; contains Print.aspx and PaymentResponse.aspx in later captures.

## ACTIONABLE LEADS
- Archival next phase (recommended): preserve exact CDX query URLs, replay URLs, capture timestamps, response status, and visible page text; keep two fields per row: archive_status and body_interpretation.
- Build before-and-after tables per exact URL before claiming removal; a removal claim needs a documented body-level comparison, not a status row.
- Use the legacy route vocabulary as historical ecosystem context only; the report is explicit that route names are not an attack-surface list.
- High-value future artifact: an official migration or architecture document connecting the two hostnames and explaining identity integration; ask MUJ for it through authorized channels.
- Authorized-only verification items: current reachability of historical endpoints, whether the MUJ response headers hold across endpoints, OIDC client registration and callback config, Akamai path via DNS/CDN records.
- Track archived 2025+ MUJ assets (Keen login CSS, custom login JS, scripts.bundle.js) for drift against the live page during authorized review.
- Report hygiene: separate host timelines, label every architectural bridge as inference, never replay tokens or reproduce query values from PaymentResponse.aspx.

## FLAGS
- The header fingerprint is one point-in-time public observation via a third-party API (hackertarget); banners can be altered by proxies or spoofing and are not a source-code audit. X-AspNet-Version 4.0.30319 is the version-family value, not a patch-level inventory.
- CDX status alone is not truth: WebForm1.aspx (200 row, 404 body) is the report's own worked example; a nominal 200 can be a custom error document.
- PaymentResponse.aspx query strings and verification-cookie values are deliberately omitted; do not reconstruct or replay captured tokens.
- Redirect records (302/303) do not reveal destinations or whether the cause was authentication, authorization, routing, or an error.
- Microsoft OpenID metadata proves tenant configuration only; "Microsoft-linked identity and recovery workflow" is the safe wording, not "proven Microsoft SSO."
- Removal, full-rewrite, and shared-backend conclusions are explicitly unproven; the report says a route name is not a vulnerability and a public 404 is not misconfiguration.
- The crt.sh certificate-metadata URL appears in the scope description but receives no body-level analysis in the report.
- Corpus asymmetry: legacy data is route-rich but body-poor; MUJ data is front-door-only. Raw capture counts must not be compared as application size.

## COVERAGE
- File: w2g-14-wayback-family.md.
- 323 lines total; 55,156 bytes on disk; 55,154 chars read.
- Method: read_file offset 1, limit 2000, single call.
- EOF confirmed: final call returned truncated: false, last content line 323 equals total_lines 323.