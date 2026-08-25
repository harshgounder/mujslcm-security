# Public MUJ SLCM GitHub Exposure Assessment

## Executive Summary

This assessment reviews public GitHub repositories and individual files associated with the MUJ SLCM vocabulary: `mujslcm`, `mujslcm.jaipur.manipal.edu`, `slcm.manipal.edu`, `jaipur.manipal.edu`, `muj.manipal.edu`, and MUJ portal terminology. It is a source-inventory report, not a live penetration test. I did not authenticate to the portal, validate any credential or cookie, send requests to the target, bypass a control, or test whether a public artifact is deployed.

- **Credential Exposure**: `KrishGoel/slcm-feedback-automation` has a public `.env.example` containing a populated name, registration number, and password field rather than template placeholders; the password and identifier are redacted here because their validity is unknown. Treat the value as potentially compromised and rotate it through the proper university process. [63]
- **MUJ Endpoint Mapping**: `DK10WS/SLCM_APP` hardcodes the MUJ base URL and documents attendance, parent-login, OTP, dashboard, and release-check URL constants. Its other files show cookie-bearing requests, CSRF-token parsing, and student-data extraction. This is a code-level map, not evidence that every route is live. [36] [51] [41]
- **Browser DOM Automation**: `Tejas-Narula/SlcmPlus` targets three exact MUJ academic pages and calculates attendance, internal-mark totals, and GPA from page content. The reviewed code is primarily DOM augmentation; no explicit external API client or embedded credential is visible in the cited excerpts. [71] [72]
- **Feedback Integrity**: `AddisionS/slcm-feedback-form-filler` can set feedback controls to all-Yes or all-No and can click a submit control. Its Chrome manifest declares `<all_urls>`, `*://*/*`, `scripting`, and `activeTab`, so the permission scope is broader than the MUJ-specific description. Narrowing the scope and requiring confirmation before submission are appropriate defensive actions. [27] [25]
- **Session Handling**: The Flutter app stores a session cookie in a static process variable, sends it in a `Cookie` header, and also saves username and password values through shared preferences in the login flow. The excerpts do not prove whether the platform encrypts those values or whether a production build matches the repository. [14] [67] [51]
- **Captured Cookie Artifact**: A public portal-clone directory contains an HTTrack cookie file with a populated `__RequestVerificationToken` entry for the MUJ host. The actual value is not reproduced. The file proves public disclosure of a token-like artifact, but not that it is still valid, authenticated, or usable. [64]
- **Legacy API Pattern**: Older `manipalthetalk/App-Backend`, `canaryGrapher/slcmAPI`, and `nikeplusdash/SLCM-api` projects show credential-forwarding scrapers, browser or HTTP scraping, REST wrappers, and profile/academic-data extraction for `slcm.manipal.edu`. They must not be conflated with the Jaipur host. [26] [24] [70]
- **Technology Context**: The requester supplied ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 identity as scope context. The GitHub artifacts support observations about URL paths, HTML form fields, cookies, and portal-facing logic, but they do not independently verify CDN headers, IIS version, framework version, or Microsoft 365 federation. Any stronger statement would be an inference rather than a finding.
- **Overall Verdict**: Confidence is high that public GitHub code contains MUJ-specific automation and portal-facing client logic, high that at least one populated credential-like `.env.example` was publicly visible in the reviewed corpus, medium that the captured cookie is sensitive but unknown in validity, and low that any artifact demonstrates a current compromise or a server-side vulnerability.

The most important operational distinction is between exposure and exploitability. A repository can contain a password, a cookie, an endpoint, or a form selector without proving that the value still works, that the code is deployed, or that a server accepts an unauthorized request. The responsible response is therefore credential rotation, artifact removal, secure storage review, and owner notification, not testing the exposed material against the service.

## Scope, Evidence Method, and Safe Interpretation

The evidence set was built from public GitHub repository, directory, README, manifest, source-file, and configuration pages found using the specified MUJ and SLCM terms. Each cited marker in this report maps to an exact URL in the References table. A repository page establishes that a public artifact was visible at the cited path; it does not establish ownership by the university, current deployment, current validity, or authorization to use the artifact.

The reproducible analytical basis is deliberately provided instead of private chain-of-thought. For each hit, the review recorded: repository owner and name; branch and file path; exact target host or URL string; request method when visible; credential, cookie, token, or environment-variable behavior; DOM selectors or API route names; data fields extracted; and whether the observation was direct or inferential. The review then separated four evidence classes: direct observation, code-review inference, negative observation limited to the cited file, and unknown status.

No active testing was performed. In particular, this report does not provide instructions for logging in, solving a CAPTCHA, replaying a cookie, calling an endpoint, bypassing a control, or using a disclosed password. The high-level descriptions of login fields and routes are included so defenders can identify what should be reviewed and removed, not so readers can access the service.

The user-supplied server stack is treated as a research hypothesis. Client source can reveal what developers assumed about the portal, but a hardcoded URL or a CSRF field is not a server fingerprint. For example, the Flutter client parses `__RequestVerificationToken` and posts to MVC-looking paths, while the legacy tools reference `.aspx` pages; these are useful compatibility clues, but they do not prove the exact production framework or reverse-proxy configuration. [51] [40] [26]

## Exact Tables: MUJ-Specific Artifact Inventory

The following table lists the highest-value MUJ-specific artifacts. The `Exposure` column describes only what the cited public file exposes. It does not claim that the artifact is deployed or that its behavior succeeds against the portal.

| Artifact and exact file URL | Directly observed function | Sensitive material observed | Assessment |
|---|---|---|---|
| `https://github.com/Tejas-Narula/SlcmPlus/blob/main/manifest.json` | Chrome Manifest V3 content script matches exact MUJ attendance, internal-mark, and grades pages. [71] | No credential or secret shown in the cited manifest. | High-confidence MUJ target mapping; no server-side API proof. |
| `https://github.com/Tejas-Narula/SlcmPlus/blob/main/content.js` | Reads table cells, calculates attendance and marks, maps grades to points, computes weighted GPA, and uses a mutation observer. [72] | No explicit credential, cookie, or external network call shown in the cited excerpt. | Browser-side analytics and DOM augmentation; inference that it is lower exposure than a scraper because the cited code operates on loaded page content. |
| `https://github.com/AddisionS/slcm-feedback-form-filler/blob/main/chrome/manifest.json` | Declares content-script and extension permissions including `<all_urls>`, `*://*/*`, `scripting`, and `activeTab`. [27] | No credential or `.env` value shown. | Broad browser permission scope; target restriction should be reviewed. |
| `https://github.com/AddisionS/slcm-feedback-form-filler/blob/main/chrome/content.js` | Selects radio inputs, sets Yes or No dropdown values, dispatches change events, and can click `btnSubmit`. [25] | No cookie or token handling shown. | Integrity-impacting feedback automation; no evidence of authentication bypass. |
| `https://github.com/KrishGoel/slcm-feedback-automation/blob/main/script.py` | Opens the MUJ portal, fills `UserName` and `Password`, filters pending feedback, selects controls, enters a fixed comment, and submits. [69] | Reads `NAME`, `REGISTRATION_NUMBER`, and `PASSWORD` from environment variables. [69] | Direct MUJ browser automation; credential exposure is in the separate `.env.example`, not this source file. |
| `https://github.com/KrishGoel/slcm-feedback-automation/blob/main/.env.example` | Contains three environment entries for name, registration number, and password. [63] | A populated name, registration number, and password-like value were visible; all sensitive values are redacted in this report. [63] | Highest-priority public secret finding; validity is unknown. |
| `https://github.com/DK10WS/SLCM_APP/blob/main/lib/pages/redirects.dart` | Defines the MUJ base URL, an attendance route, parent OTP routes, a dashboard route, and a GitHub release-check URL. [36] | No embedded credential in the cited constants. | Strongest direct MUJ route inventory in the reviewed corpus. |
| `https://github.com/DK10WS/SLCM_APP/blob/main/lib/pages/login.dart` | Fetches a login page, parses a verification token, posts student or parent login fields, follows a redirect, and processes OTP-related flows. [51] [51] | Student and parent payload field names are visible; no populated credential is shown. [51] [51] | Important authentication-flow documentation; production behavior remains unknown. |
| `https://github.com/DK10WS/SLCM_APP/blob/main/lib/session_manager.dart` | Holds a session cookie in a static string, clears it on logout, and uses its presence as the login state. [14] | Cookie value is not embedded. | In-memory session design; secure persistence and lifecycle need review. |
| `https://github.com/vikrant500/college_portal_web_and_dbms/blob/main/mujslcm.jaipur.manipal.edu_122/cookies.txt` | Public HTTrack cookie file associated with the portal-clone directory. [64] | A populated verification-token cookie entry is visible in the source preview; the token is not reproduced. [64] | Treat as sensitive historical material; validity and authentication status are unknown. |

The MUJ-specific pattern is consistent across the table: student projects generally interact with the already rendered portal through selectors, while the Flutter project goes further and recreates requests with cookies, form fields, CSRF tokens, and JSON responses. That difference matters for defensive review because a DOM helper mainly depends on the user already being logged in, whereas a request-replay client creates a more detailed map of application behavior. This is a code-review inference based on the cited mechanisms, not a claim of exploitability. [72] [43] [51]

## Credential, Cookie, and Personal-Data Exposure

The clearest exposure is `KrishGoel/slcm-feedback-automation/.env.example`. Unlike a safe template containing values such as `your_username` and `your_password`, the cited file displays populated fields. The source preview contains a name, a registration number, and a password-like value; this report intentionally does not repeat any of them. The repository README also instructs users to create a `.env` file with those fields, and the script loads them with `python-dotenv`. [63] [42] [69]

The correct conclusion is not that the password is currently valid. The direct conclusion is that a credential-like value was publicly present in a file named `.env.example` at the time of review. Validity, ownership, reuse, and account scope are unknown. The account owner or repository maintainer should rotate the password, invalidate active sessions, remove the value from current files and Git history, and notify the university security or identity team through an established channel. This recommendation does not require anyone to test the value.

The portal-clone cookie file is a separate but important exposure. The file identifies itself as an HTTrack cookie file and includes a `__RequestVerificationToken` entry associated with the MUJ host. A request-verification token is not automatically a login session, and the excerpt does not establish whether it is expired, bound to a session, or accepted by the server. The safe classification is `sensitive token-like artifact, validity unknown`, not `working account access`. [64]

The Flutter code creates a different class of risk. `SessionManager` keeps a cookie in a static string and considers the user logged in when the string is present. Its utility code adds a `Cookie` header to requests and can read saved username and password values from shared preferences after a redirect. The login screen explicitly saves credentials through shared preferences. The cited code does not establish whether the platform encrypts the preferences, whether the device is rooted, or whether this repository build is distributed to users. [14] [67] [51]

The same app parses personal academic information. The information page sends the session cookie and extracts name, registration number, section, program, and related fields into a user-information map. Attendance, grades, marks, timetable, and change-password pages similarly use authenticated requests. This is not evidence of a breach; it is evidence that a third-party client is designed to handle sensitive student records and therefore deserves a privacy and secure-storage review. [41] [43] [52] [45] [44] [50]

| Exposure class | Public artifact | Direct observation | Validity or impact status | Defensive priority |
|---|---|---|---|---|
| Populated credential-like environment file | KrishGoel `.env.example` | Name, registration number, and password-like value are visible; redacted here. [63] | Current validity and account ownership unknown. | Immediate rotation and history cleanup. |
| Verification-token cookie | Vikrant portal-clone `cookies.txt` | Populated token entry associated with the MUJ host. [64] | Session binding and expiry unknown. | Revoke related sessions and remove the file. |
| Client-side saved credentials | DK10WS login and utility code | Username and password values are saved/read through shared preferences. [67] [51] | Encryption and production deployment unknown. | Replace with platform secure storage and minimize retention. |
| In-memory authenticated session | DK10WS session manager | Static cookie storage and boolean login state. [14] | Runtime lifetime and logout completeness unknown. | Centralize session expiry and clear all request state. |
| Student-record extraction | DK10WS information, attendance, grades, marks, timetable | Name, registration data, academic data, and timetable are parsed after authenticated requests. [41] [43] [52] [45] [44] | Intended functionality, not proof of unauthorized access. | Minimize fields, document consent, and audit logs. |

## API and Browser-Automation Patterns

The most detailed MUJ request pattern appears in `DK10WS/SLCM_APP`. The redirect file sets `https://mujslcm.jaipur.manipal.edu` as the base and includes `Student/Academic/GetAttendanceSummaryList`, parent OTP paths, a dashboard path, and a GitHub release endpoint. The attendance screen posts to the attendance constant with a cookie and expects an `AttendanceSummaryList` response. The grades and marks screens similarly post with a cookie, a semester field, and an empty enrollment field, then parse returned data. [36] [43] [52] [45]

The client also reveals an application-level data model. Attendance records contain fields such as course identifier, percentage, total classes, and attended classes, after which the client calculates whether additional classes are needed to reach a 75 percent threshold. Marks include course data and component totals. The information page parses registration number, name, section, program, and related fields. These details are useful for defenders preparing data-minimization and authorization tests, but they should not be treated as a license to query the service. [43] [45] [41]

The login flow parses a hidden `__RequestVerificationToken`, constructs a student payload with `EmailFor`, `LoginFor`, `UserName`, and `Password`, and handles redirects. A separate parent payload uses a MUJ email suffix and a different login mode. The change-password flow similarly retrieves a verification token and posts new-password and confirmation fields. These are direct source observations. It is an inference, not a verified fingerprint, that the token and route design reflect an MVC-style server implementation. [51] [51] [50]

The feedback projects use a different mechanism. `SlcmPlus` matches exact academic page URLs and manipulates the DOM. `AddisionS` selects generic radio controls, specific dropdown IDs, and a submit button, while its popup stores the auto-submit setting in browser local storage and injects the content script into the active tab. Neither cited extension excerpt shows a credential store or API client. The AddisionS manifest nevertheless uses broad host permissions, creating a least-privilege concern if the extension is installed in a browser containing other authenticated sites. [71] [25] [23] [27]

`KrishGoel/slcm-feedback-automation` uses Selenium rather than a direct API. It opens the MUJ root, locates `UserName` and `Password`, visits the feedback list, filters pending items, changes controls, enters a fixed comment, submits, and records a local completed state. The code therefore exposes selectors and workflow assumptions but not a REST route list. The README says to run `main.py`, while the repository tree and cited source file identify `script.py`; that documentation mismatch is a maintenance issue and is not itself a security vulnerability. [69] [29] [42]

| Client pattern | Example | Observed inputs and outputs | What it exposes to defenders |
|---|---|---|---|
| DOM analytics | SlcmPlus | Attendance table cells, marks cells, grades, credits, and GPA calculations. [72] | Page structure and client-side data fields; no visible API route in cited code. |
| Generic extension automation | AddisionS | Radio inputs, dropdown IDs, message actions, and submit button. [25] [23] | Feedback form selectors and broad browser permission scope. |
| Selenium credential automation | KrishGoel | Environment-sourced credentials, login field names, feedback list, pending-state logic, and submit control. [69] | Workflow and selectors; exposed credential-like value is in `.env.example`. |
| Cookie-bearing JSON client | DK10WS attendance and grades | Cookie header, POST requests, semester/enrollment fields, JSON keys. [43] [52] | Route names, request shape, response schema, and session dependency. |
| CSRF-aware form client | DK10WS login and password change | Hidden token parsing, login payloads, redirect handling, and password fields. [51] [50] | Authentication and account-management assumptions. |

## Legacy SLCM Wrappers: Useful Comparison, Separate Scope

The older `manipalthetalk/App-Backend` project directly identifies its target template as `http://slcm.manipal.edu/{}` and opens `loginform.aspx`, `Academics.aspx`, and a grade-sheet page. It submits `txtUserid` and `txtpassword`, extracts timetable, attendance, internal marks, end-semester grades, and GPA, and writes JSON output. The README describes the scraper as Python 2.7 with a Go server wrapper. [26] [18]

Its `server.go` accepts `regno` and `password` form values, sets wildcard CORS, caches JSON by registration number, and constructs a shell command containing the user-supplied registration number and password before invoking the scraper. The code excerpt is enough for a defensive code-review warning: interpolating untrusted form data into a shell command could create command-injection risk if escaping is incomplete. That is an inference from the code, not evidence that the old service is online, reachable, or exploitable. The cache design also deserves review because the key is registration number while the request includes a password, although the excerpt alone cannot establish cross-user disclosure. [28]

`canaryGrapher/slcmAPI` is a Node and Puppeteer REST wrapper. Its server registers routes named `/getscores`, `/getattendance`, `/getprofile`, and `/validateuser`, and the routes directory contains corresponding JavaScript files. Its README describes an API for marks, attendance, profile details, and credential validation, but also says the repository is deprecated because the login portal introduced CAPTCHA. GitHub marks the repository as archived and read-only. [24] [21] [7] [15]

`nikeplusdash/SLCM-api` uses `requests`, BeautifulSoup, local `user.txt` credentials, and OCR-related logic in Python, with a JavaScript counterpart. It references the base host, profile and academics pages, and fields for registration number, application number, name, year, branch, joining date, birthday, gender, phone, emergency contact, email, attendance, and marks. The README says the project makes a login request and exposes a hosted API, but the repository itself is an older artifact and the report makes no claim about current deployment. [70] [38] [30]

These projects matter as historical design patterns: they demonstrate that student developers have repeatedly attempted to turn a browser-only academic portal into a scraper or API. They do not prove that the Jaipur MUJ host shares the same routes, controls, or vulnerabilities. The safe use of this comparison is to build a defensive review checklist: credential handling, cache keys, CORS, subprocess invocation, data minimization, CAPTCHA-related control boundaries, and session expiry.

## Low-Signal, Adjacent, and Negative Findings

`sankalp2004/SLCM-is-Dumb` is a Selenium and OCR project for the non-Jaipur `slcm.manipal.edu` host. Its README describes automatic login, grade-sheet navigation, and CGPA extraction, while its configuration file names the login and grade-sheet URLs and loads `SLCM_USERNAME` and `SLCM_PASSWORD` from the environment. The public `.env.example` contains placeholders such as `your_username_here` and `your_password_here`, not populated credentials. [49] [49] [34] [40]

Its source shows browser selectors for username and password fields, CAPTCHA-related processing, grade-sheet navigation, and multiple CGPA extraction fallbacks. This report intentionally does not describe a way to defeat or automate a CAPTCHA. The relevant security conclusion is that the project handles credentials and academic results in a local browser process, so secrets, screenshots, logs, and debug artifacts should be reviewed and excluded from version control. [47] [47] [47]

`Prashastiiii/mujslcm` is a small college project repository whose README says only that it is being made as a college project. Its visible tree includes HTML, CSS, image, placement, and project directories; the cited `project/index.php` is an empty PHP block. The reviewed pages do not establish a MUJ portal URL, authentication flow, API, environment secret, or SLCM integration. [8] [3] [1]

`Anushkakumar10/muj_slcm` contains a minimal Django-shaped project tree and a requirements file containing Django. The cited repository evidence does not establish a MUJ host, authentication, API call, cookie, or populated secret. This should be classified as a low-signal project-name match, not a portal scraper. [2] [73] [74]

`justin212407/web3-muj-slcm` is adjacent rather than a confirmed authentication client. Its README describes a Web3 domain and document concept for MUJ students and references the MUJ SLCM URL as a portal concept. Its backend tree contains Hardhat and contract material plus an `.env.example`, while its frontend README describes Next.js, TypeScript, TailwindCSS, blockchain, and wallet integration. The cited material does not establish that it logs into SLCM, reads portal records, or contains populated portal credentials. [37] [68] [61]

The portal-clone directory is also not equivalent to a live portal copy. Its tree contains `Home`, `Scripts`, assets, `cookies.txt`, `hts-log.txt`, and other downloaded files; the script directory contains jQuery and validation libraries, and the Home directory contains `Index.html`. The directory name and downloaded cookie file show collection artifacts, not deployment or authorization. [39] [62] [39]

## Defensive Risk Register and Recommended Actions

The following register translates public observations into defensive priorities. Ratings describe review priority, not proof of exploitation.

| Priority | Issue | Evidence and confidence | Safe action |
|---|---|---|---|
| P0 | Populated credential-like value in a public `.env.example` | Direct observation in the KrishGoel file; high confidence for disclosure, unknown validity. [63] | Notify the owner through a trusted channel, rotate the account password, revoke sessions, remove the value from current history, and run repository secret scanning. Do not test the value. |
| P0 | Verification-token cookie in a public clone | Direct observation of a populated token entry; high confidence for disclosure, unknown session binding. [64] | Revoke relevant sessions if the university can identify them, remove the file and history, and treat all downloaded browser-state artifacts as sensitive. |
| P1 | Credentials retained by the Flutter client | Direct observation that shared preferences are read and written in the login flow; encryption and deployment unknown. [67] [51] | Use platform secure storage, avoid storing passwords, prefer short-lived refreshable sessions, and clear state on logout. |
| P1 | Cookie lifecycle is process-static | Direct observation of static cookie state and cookie headers; server-side expiry unknown. [14] [43] | Centralize expiry, clear all cached headers on logout, handle invalid sessions, and avoid logging request headers. |
| P1 | Broad extension permissions | Direct observation of `<all_urls>`, `*://*/*`, `scripting`, and `activeTab`. [27] | Restrict host matches to the intended portal, remove unused permissions, and publish a clear data-use statement. |
| P1 | Automatic feedback submission | Direct observation of a submit click after bulk control changes. [25] [69] | Require explicit confirmation, show the affected course or survey, and preserve an audit trail where policy permits. |
| P1 | Legacy shell interpolation | Code-review inference from `sh -c` command construction with form values. [28] | Replace shell strings with an argument-array process API, validate lengths and characters, isolate the worker, and retire unneeded service code. |
| P1 | Wildcard CORS in legacy wrapper | Direct observation of `Access-Control-Allow-Origin: *`; security impact is deployment-dependent. [28] | Restrict origins, methods, and headers to approved clients, and require authentication at the wrapper boundary. |
| P2 | Excessive academic-data extraction | Direct observation of profile, attendance, grades, marks, and timetable parsing. [41] [43] [45] | Minimize fields, define retention, obtain user consent, and prevent debug screenshots or logs from containing records. |
| P2 | Documentation and implementation drift | README says `main.py`, while the cited repository tree and source identify `script.py`. [42] [29] [69] | Correct documentation, pin releases, and make security review target a named commit. |

The first response should be containment, not curiosity. A university security club can responsibly notify the repository owner and university security team, preserve only the minimum public evidence needed for remediation, and avoid downloading or circulating secrets. If the value is real, rotation matters more than proving that it works. If the value is stale, removal still matters because reuse and historical leakage cannot be assumed away.

For the application team, the principal engineering work is to reduce credential material in third-party clients. A client should not need a long-lived password after login, and a browser extension that only edits a page should not request access to every web origin. A feedback tool should also make the user see and confirm the exact intended action, because integrity loss can occur even without account takeover.

For the GitHub governance team, enable secret scanning where available, use push protection, review forks and historical commits, and create a disclosure playbook covering passwords, session cookies, CSRF tokens, screenshots, logs, and downloaded HTML. This report does not claim that GitHub or MUJ controls are absent; it identifies controls that would reduce recurrence.

## Technology-Context Assessment

The visible code contains several features that are compatible with server-rendered web applications: hidden verification-token fields, named form inputs, HTTP redirects, `.aspx` paths in legacy projects, and route-like paths under `Home` and `Student/Academic`. Those observations help defenders understand client assumptions. They do not independently prove `ASP.NET MVC 5.3`, `.NET Framework 4.x`, or any specific IIS version. [51] [40] [26]

The Flutter login payload includes an `EmailFor` value using `@muj.manipal.edu`, as well as student and parent login modes. That supports the narrower statement that the client expects MUJ-branded email-domain and role fields. It does not establish that Microsoft 365 is the identity provider, that the domain is federated, or that the portal delegates authentication to Microsoft. [51] [51]

Nothing in the cited GitHub artifacts establishes Akamai involvement, response headers, TLS behavior, origin exposure, or the current server software banner. Those questions require passive, authorized asset-management evidence from the university or an approved scanner, not assumptions from repository code. The same limitation applies to whether the target is presently reachable, whether routes still exist, and whether a disclosed token or password is valid.

## Synthesis: What the Corpus Reveals Across Strategies

The artifacts fall into five strategies: DOM augmentation, generic browser extensions, Selenium workflow automation, cookie-bearing native clients, and server-side scraping wrappers. Their mechanisms and trade-offs differ materially, as shown below.

| Strategy | Representative artifact | Mechanism | Scope of data or action | Main trade-off |
|---|---|---|---|---|
| DOM augmentation | SlcmPlus | Reads rendered attendance, marks, and grades tables and adds calculations. [72] | Academic display data already present in the page. [71] | Lower route exposure in the cited code, but dependent on brittle page selectors. |
| Generic extension | AddisionS feedback filler | Injects a content script, changes controls, and optionally submits. [25] | Any page matching broad permission scope, with feedback selectors intended for SLCM. [27] | Convenient automation versus excessive browser authority and accidental submission. |
| Selenium feedback automation | KrishGoel | Opens a browser, loads env credentials, fills fields, edits feedback, and submits. [69] | Account login and survey workflow. [42] | Simple to build, but exposes credential-handling and automation-state risks. |
| Native request client | DK10WS SLCM_APP | Posts cookies and form data, parses JSON or HTML, follows redirects, and manages sessions. [43] [51] | Profile, attendance, grades, marks, timetable, and password-change functions. [41] [50] | Richer user experience and route visibility, but greater credential, cookie, and PII exposure. |
| Server-side scraper/API | App-Backend or canaryGrapher | Accepts credentials and scrapes the legacy SLCM host through Python, Puppeteer, or HTTP. [26] [24] | Academic records and validation endpoints. [7] | Centralized service increases convenience but concentrates passwords, cache, CORS, and subprocess risk. |
| Clone/download artifact | Vikrant portal directory | Stores downloaded HTML, scripts, logs, assets, and a cookie file. [39] [64] | Potentially copied portal content and browser state. | Useful for historical analysis, but token disclosure and stale data must be treated as sensitive. |

The non-obvious tension is that the most technically detailed artifact is not necessarily the most dangerous. `SlcmPlus` exposes exact page paths but appears to calculate from the rendered DOM, while `DK10WS/SLCM_APP` exposes a more complete request and session model. Conversely, the highest-priority immediate issue is not a route list at all: it is the populated `.env.example` value. This separates architectural intelligence from credential incident response. [71] [36] [63]

A second tension is between user convenience and data minimization. The native client offers profile, attendance, grades, marks, timetable, and password-change screens, but that breadth means it handles more sensitive data and session material than a page-only GPA helper. The correct design response is not to prohibit all student tooling; it is to constrain permissions, avoid password retention, use secure session storage, minimize returned fields, and make consent visible. [41] [43] [14]

A third tension concerns historical evidence. The older wrappers show that the broader Manipal SLCM ecosystem has attracted scraping and API projects, but they target `slcm.manipal.edu`, use older page conventions, and include an archived or deprecated project. Reusing their route assumptions against the Jaipur host would be an unsupported inference. Their value is comparative: they identify categories for defensive review, not a shortcut to testing the current MUJ service. [26] [7] [15] [70]

## VERDICT

**Overall confidence: High for public-artifact identification; medium for exposure severity; low for live compromise or exploitability.**

| Verdict question | Conclusion | Confidence | Basis |
|---|---|---|---|
| Are there public MUJ-specific scripts and clients? | Yes. SlcmPlus, AddisionS, KrishGoel, and DK10WS contain direct MUJ portal references or workflows. [75] [6] [42] [76] | High | Multiple independent repositories and exact file paths. |
| Is a populated credential-like value publicly visible? | Yes, in the reviewed KrishGoel `.env.example`; the value is redacted and validity is unknown. [63] | High for disclosure | Direct source observation; no validation performed. |
| Is a token-like cookie artifact publicly visible? | Yes, in the portal-clone `cookies.txt`; session status is unknown. [64] | High for disclosure; medium for sensitivity | Direct source observation and token name; no replay or validation. |
| Are exact MUJ request patterns visible? | Yes, including base URL, attendance route, cookie headers, CSRF parsing, form fields, and academic response parsing. [36] [43] [51] | High | Direct source code. |
| Does the corpus prove a current server vulnerability? | No. The reviewed evidence does not establish deployment, current route behavior, or exploitability. | High | No active testing and no source that proves those conditions. |
| Does the corpus independently verify ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai, or Microsoft 365 identity? | No. These remain requester-supplied context or hypotheses; client code alone is insufficient. | High for limitation | No cited GitHub artifact provides a reliable server fingerprint or identity-provider proof. |
| Is the legacy `slcm.manipal.edu` code MUJ-host evidence? | No. It is comparison evidence for a different host and older ecosystem. [26] [70] | High | Exact host strings are different. |

The actionable conclusion is narrow and defensible: notify and remediate the populated `.env.example`, remove the token-bearing cookie artifact, review Git history, audit the Flutter client for secure storage and session expiry, narrow extension permissions, and review legacy wrappers for shell, CORS, caching, and credential-handling defects. Do not attempt to use any exposed value. The evidence supports responsible incident response and secure design review, not unauthorized access.

## References

1. *mujslcm/project/index.php at main · Prashastiiii/mujslcm · GitHub*. https://github.com/Prashastiiii/mujslcm/blob/main/project/index.php
2. *GitHub - Anushkakumar10/muj_slcm · GitHub*. https://github.com/Anushkakumar10/muj_slcm
3. *mujslcm/README.md at main · Prashastiiii/mujslcm · GitHub*. https://github.com/Prashastiiii/mujslcm/blob/main/README.md
4. *GitHub - Tejas-Narula/SlcmPlus: A Chrome extension for MUJ students that enhances the SLCM experience by providing attendance analytics and automatic marks calculation directly within the portal. · GitHub*. https://github.com/Tejas-Narula/SlcmPlus/tree/main
5. *GitHub - manipalthetalk/App-Backend: Scrapes the SLCM for ...*. https://github.com/manipalthetalk/App-Backend
6. *GitHub - AddisionS/slcm-feedback-form-filler: This is a chrome extension that can be used to automate the process of filling feedback form on MUJ's SLCM portal · GitHub*. http://github.com/AddisionS/slcm-feedback-form-filler
7. *GitHub - canaryGrapher/slcmAPI: The API for SLcM, Manipal. Get your marks, your attendance and your profile details · GitHub*. http://github.com/canaryGrapher/slcmAPI
8. *GitHub - Prashastiiii/mujslcm · GitHub*. https://github.com/Prashastiiii/mujslcm
9. *GitHub - DK10WS/SLCM_APP: App Version for MUJ SLCM · GitHub*. https://github.com/DK10WS/SLCM_APP
10. *GitHub - sankalp2004/SLCM-is-Dumb: This extracts cgpa from https://slcm.manipal.edu/ directly and passes captcha · GitHub*. https://github.com/sankalp2004/SLCM-is-Dumb
11. *slcm-feedback-form-filler/chrome/popup.html at main · AddisionS/slcm-feedback-form-filler · GitHub*. https://github.com/AddisionS/slcm-feedback-form-filler/blob/main/chrome/popup.html
12. *App-Backend/scraper/requirements.txt at master · manipalthetalk/App-Backend · GitHub*. https://github.com/manipalthetalk/App-Backend/blob/master/scraper/requirements.txt
13. *SLCM_APP/lib/pages at main · DK10WS/SLCM_APP · GitHub*. https://github.com/DK10WS/SLCM_APP/tree/main/lib/pages
14. *SLCM_APP/lib/session_manager.dart at main · DK10WS/SLCM_APP · GitHub*. https://github.com/DK10WS/SLCM_APP/blob/main/lib/session_manager.dart
15. *slcmAPI/README.md at master · canaryGrapher/slcmAPI · GitHub*. https://github.com/canaryGrapher/slcmAPI/blob/master/README.md
16. *slcmAPI/package.json at master · canaryGrapher/slcmAPI · GitHub*. https://github.com/canaryGrapher/slcmAPI/blob/master/package.json
17. *SLCM_APP/lib/utils at main · DK10WS/SLCM_APP · GitHub*. https://github.com/DK10WS/SLCM_APP/tree/main/lib/utils
18. *App-Backend/README.md at master · manipalthetalk/App-Backend · GitHub*. https://github.com/manipalthetalk/App-Backend/blob/master/README.md
19. *slcm-feedback-form-filler/firefox/content.js at main · AddisionS/slcm-feedback-form-filler · GitHub*. https://github.com/AddisionS/slcm-feedback-form-filler/blob/main/firefox/content.js
20. *SLCM_APP/lib/main.dart at main · DK10WS/SLCM_APP · GitHub*. https://github.com/DK10WS/SLCM_APP/blob/main/lib/main.dart
21. *slcmAPI/routes at master · canaryGrapher/slcmAPI · GitHub*. https://github.com/canaryGrapher/slcmAPI/tree/master/routes
22. *SLCM_APP/pubspec.yaml at main · DK10WS/SLCM_APP · GitHub*. https://github.com/DK10WS/SLCM_APP/blob/main/pubspec.yaml
23. *slcm-feedback-form-filler/chrome/popup.js at main · AddisionS/slcm-feedback-form-filler · GitHub*. https://github.com/AddisionS/slcm-feedback-form-filler/blob/main/chrome/popup.js
24. *slcmAPI/server.js at master · canaryGrapher/slcmAPI · GitHub*. https://github.com/canaryGrapher/slcmAPI/blob/master/server.js
25. *slcm-feedback-form-filler/chrome/content.js at main · AddisionS/slcm-feedback-form-filler · GitHub*. https://github.com/AddisionS/slcm-feedback-form-filler/blob/main/chrome/content.js
26. *App-Backend/scraper/scraper.py at master · manipalthetalk/App-Backend · GitHub*. https://github.com/manipalthetalk/App-Backend/blob/master/scraper/scraper.py
27. *slcm-feedback-form-filler/chrome/manifest.json at main · AddisionS/slcm-feedback-form-filler · GitHub*. https://github.com/AddisionS/slcm-feedback-form-filler/blob/main/chrome/manifest.json
28. *App-Backend/server.go at master · manipalthetalk/App-Backend · GitHub*. https://github.com/manipalthetalk/App-Backend/blob/master/server.go
29. *GitHub - krishgoel/slcm-feedback-automation: An automation script for filling out semester-end feedback on the college portal (SLCM Manipal, Jaipur) · GitHub*. https://github.com/KrishGoel/slcm-feedback-automation/tree/main
30. *GitHub - nikeplusdash/SLCM-api: An api for https://slcm.manipal.edu · GitHub*. https://github.com/nikeplusdash/SLCM-api/tree/master
31. *GitHub - nikeplusdash/SLCM-api: An api for https://slcm.manipal.edu · GitHub*. https://github.com/nikeplusdash/SLCM-api
32. *GitHub - justin212407/web3-muj-slcm: Web3 Domain Name Service (DNS) for Manipal University Jaipur (MUJ) students. This innovative platform will equip students with Web3-compatible domains under the university’s domain name, empowering them to securely receive, manage, and verify their NFT credentials. · GitHub*. https://github.com/justin212407/web3-muj-slcm/tree/main
33. *GitHub - sankalp2004/SLCM-is-Dumb: This extracts cgpa from https://slcm.manipal.edu/ directly and passes captcha · GitHub*. https://github.com/sankalp2004/SLCM-is-Dumb/tree/master
34. *SLCM-is-Dumb/.env.example at master · sankalp2004/SLCM-is-Dumb · GitHub*. https://github.com/sankalp2004/SLCM-is-Dumb/blob/master/.env.example
35. *SLCM_APP/lib/pages/settings.dart at main · DK10WS/SLCM_APP · GitHub*. https://github.com/DK10WS/SLCM_APP/blob/main/lib/pages/settings.dart
36. *SLCM_APP/lib/pages/redirects.dart at main · DK10WS/SLCM_APP · GitHub*. https://github.com/DK10WS/SLCM_APP/blob/main/lib/pages/redirects.dart
37. *web3-muj-slcm/README.md at main · justin212407/web3-muj-slcm · GitHub*. https://github.com/justin212407/web3-muj-slcm/blob/main/README.md
38. *SLCM-api/README.md at master · nikeplusdash/SLCM-api · GitHub*. https://github.com/nikeplusdash/SLCM-api/blob/master/README.md
39. *college_portal_web_and_dbms/mujslcm.jaipur.manipal.edu_122 at main · vikrant500/college_portal_web_and_dbms · GitHub*. https://github.com/vikrant500/college_portal_web_and_dbms/tree/main/mujslcm.jaipur.manipal.edu_122
40. *SLCM-is-Dumb/config.py at master · sankalp2004/SLCM-is-Dumb · GitHub*. https://github.com/sankalp2004/SLCM-is-Dumb/blob/master/config.py
41. *SLCM_APP/lib/pages/information.dart at main · DK10WS/SLCM_APP · GitHub*. https://github.com/DK10WS/SLCM_APP/blob/main/lib/pages/information.dart
42. *slcm-feedback-automation/README.md at main · krishgoel/slcm-feedback-automation · GitHub*. https://github.com/KrishGoel/slcm-feedback-automation/blob/main/README.md
43. *SLCM_APP/lib/pages/Attendance.dart at main · DK10WS/SLCM_APP · GitHub*. https://github.com/DK10WS/SLCM_APP/blob/main/lib/pages/Attendance.dart
44. *SLCM_APP/lib/pages/timetable.dart at main · DK10WS/SLCM_APP · GitHub*. https://github.com/DK10WS/SLCM_APP/blob/main/lib/pages/timetable.dart
45. *SLCM_APP/lib/pages/marks.dart at main · DK10WS/SLCM_APP · GitHub*. https://github.com/DK10WS/SLCM_APP/blob/main/lib/pages/marks.dart
46. *GitHub - krishgoel/slcm-feedback-automation: An automation script for filling out semester-end feedback on the college portal (SLCM Manipal, Jaipur) · GitHub*. https://github.com/KrishGoel/slcm-feedback-automation
47. *SLCM-is-Dumb/scraper.py at master · sankalp2004/SLCM-is-Dumb · GitHub*. https://github.com/sankalp2004/SLCM-is-Dumb/blob/master/scraper.py
48. *GitHub - justin212407/web3-muj-slcm: Web3 Domain Name Service (DNS) for Manipal University Jaipur (MUJ) students. This innovative platform will equip students with Web3-compatible domains under the university’s domain name, empowering them to securely receive, manage, and verify their NFT credentials. · GitHub*. https://github.com/justin212407/web3-muj-slcm
49. *SLCM-is-Dumb/README.md at master · sankalp2004/SLCM-is-Dumb · GitHub*. https://github.com/sankalp2004/SLCM-is-Dumb/blob/master/README.md
50. *SLCM_APP/lib/pages/change_password.dart at main · DK10WS/SLCM_APP · GitHub*. https://github.com/DK10WS/SLCM_APP/blob/main/lib/pages/change_password.dart
51. *SLCM_APP/lib/pages/login.dart at main · DK10WS/SLCM_APP · GitHub*. https://github.com/DK10WS/SLCM_APP/blob/main/lib/pages/login.dart
52. *SLCM_APP/lib/pages/grades.dart at main · DK10WS/SLCM_APP · GitHub*. https://github.com/DK10WS/SLCM_APP/blob/main/lib/pages/grades.dart
53. *slcm-feedback-form-filler/firefox/background.js at main · AddisionS/slcm-feedback-form-filler · GitHub*. https://github.com/AddisionS/slcm-feedback-form-filler/blob/main/firefox/background.js
54. *slcm-feedback-automation/requirements.txt at main · krishgoel/slcm-feedback-automation · GitHub*. https://github.com/KrishGoel/slcm-feedback-automation/blob/main/requirements.txt
55. *SLCM-api/SLCMv2 at master · nikeplusdash/SLCM-api · GitHub*. https://github.com/nikeplusdash/SLCM-api/tree/master/SLCMv2
56. *SLCM-api/SLCMv1 at master · nikeplusdash/SLCM-api · GitHub*. https://github.com/nikeplusdash/SLCM-api/tree/master/SLCMv1
57. *slcm-feedback-form-filler/firefox/style.css at main · AddisionS/slcm-feedback-form-filler · GitHub*. https://github.com/AddisionS/slcm-feedback-form-filler/blob/main/firefox/style.css
58. *slcm-feedback-form-filler/firefox/manifest.json at main · AddisionS/slcm-feedback-form-filler · GitHub*. https://github.com/AddisionS/slcm-feedback-form-filler/blob/main/firefox/manifest.json
59. *slcm-feedback-form-filler/firefox/popup.html at main · AddisionS/slcm-feedback-form-filler · GitHub*. https://github.com/AddisionS/slcm-feedback-form-filler/blob/main/firefox/popup.html
60. *college_portal_web_and_dbms/mujslcm.jaipur.manipal.edu_122/Home at main · vikrant500/college_portal_web_and_dbms · GitHub*. https://github.com/vikrant500/college_portal_web_and_dbms/tree/main/mujslcm.jaipur.manipal.edu_122/Home
61. *web3-muj-slcm/frontend at main · justin212407/web3-muj-slcm · GitHub*. https://github.com/justin212407/web3-muj-slcm/tree/main/frontend
62. *college_portal_web_and_dbms/mujslcm.jaipur.manipal.edu_122/Scripts at main · vikrant500/college_portal_web_and_dbms · GitHub*. https://github.com/vikrant500/college_portal_web_and_dbms/tree/main/mujslcm.jaipur.manipal.edu_122/Scripts
63. *slcm-feedback-automation/.env.example at main · krishgoel/slcm-feedback-automation · GitHub*. https://github.com/KrishGoel/slcm-feedback-automation/blob/main/.env.example
64. *college_portal_web_and_dbms/mujslcm.jaipur.manipal.edu_122/cookies.txt at main · vikrant500/college_portal_web_and_dbms · GitHub*. https://github.com/vikrant500/college_portal_web_and_dbms/blob/main/mujslcm.jaipur.manipal.edu_122/cookies.txt
65. *SLCM-api/SLCM.js at master · nikeplusdash/SLCM-api · GitHub*. https://github.com/nikeplusdash/SLCM-api/blob/master/SLCM.js
66. *slcm-feedback-form-filler/firefox/popup.js at main · AddisionS/slcm-feedback-form-filler · GitHub*. https://github.com/AddisionS/slcm-feedback-form-filler/blob/main/firefox/popup.js
67. *SLCM_APP/lib/utils/util.dart at main · DK10WS/SLCM_APP · GitHub*. https://github.com/DK10WS/SLCM_APP/blob/main/lib/utils/util.dart
68. *web3-muj-slcm/backend at main · justin212407/web3-muj-slcm · GitHub*. https://github.com/justin212407/web3-muj-slcm/tree/main/backend
69. *slcm-feedback-automation/script.py at main · krishgoel/slcm-feedback-automation · GitHub*. https://github.com/KrishGoel/slcm-feedback-automation/blob/main/script.py
70. *SLCM-api/SLCM.py at master · nikeplusdash/SLCM-api · GitHub*. https://github.com/nikeplusdash/SLCM-api/blob/master/SLCM.py
71. *SlcmPlus/manifest.json at main · Tejas-Narula/SlcmPlus · GitHub*. https://github.com/Tejas-Narula/SlcmPlus/blob/main/manifest.json
72. *SlcmPlus/content.js at main · Tejas-Narula/SlcmPlus · GitHub*. https://github.com/Tejas-Narula/SlcmPlus/blob/main/content.js
73. *muj_slcm/requirements.txt at main · Anushkakumar10/muj_slcm · GitHub*. https://github.com/Anushkakumar10/muj_slcm/blob/main/requirements.txt
74. *muj_slcm/muj_slcm at main · Anushkakumar10/muj_slcm · GitHub*. https://github.com/Anushkakumar10/muj_slcm/tree/main/muj_slcm
75. *SlcmPlus/README.md at main · Tejas-Narula/SlcmPlus · GitHub*. https://github.com/Tejas-Narula/SlcmPlus/blob/main/README.md
76. *SLCM_APP/README.md at main · DK10WS/SLCM_APP · GitHub*. https://github.com/DK10WS/SLCM_APP/blob/main/README.md
