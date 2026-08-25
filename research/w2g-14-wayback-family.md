# MUJ SLCM Archive Evidence and Codebase Evolution

## Executive Summary

This report reconstructs the publicly observable history of the Manipal SLCM ecosystem using Wayback Machine CDX records, archived replays, current public page content, an official MUJ FAQ, an official MAHE student-portal description, public certificate metadata, and a point-in-time HTTP-header observation. It separates direct observations from inferences. It does not perform authentication, active enumeration, exploitation, parameter manipulation, CAPTCHA testing, or any other action that would require authorization.

- **Two-host architecture**: `slcm.manipal.edu` has a 2017-2026 archive trail dominated by `.aspx` routes, Web Forms client assets, and legacy academic/payment names, while `mujslcm.jaipur.manipal.edu` has 2025+ captures centered on a MUJ-branded login surface. The practical action is to analyze them as related but not automatically identical applications. [19] [20] [21]
- **Legacy authentication surface**: The 2017 archive directly exposes a `loginForm.aspx` capture plus separate student and parent password-change pages. The student and parent pages both show old-password, new-password, and confirmation fields. The action is to treat these as historical interface evidence, not as permission to access or test those endpoints. [19] [7] [5]
- **Feature-route evidence**: 2017-2018 captures contain route names associated with academic dashboards, attendance, feedback, timetable, grades, results, registration, and parent or student functions, often with 302 or 303 responses. The action is to describe these as observed route vocabulary and redirect behavior, not as proof that every route was publicly usable or still exists. [22]
- **Archive status is not application truth**: `WebForm1.aspx` appears as a CDX 200 capture in 2022, but its replay body is explicitly a 404 error page. This is a decisive warning against treating a CDX status alone as proof that a feature page worked. [23] [24]
- **MUJ login modernization**: 2025 MUJ captures show `WELCOME TO MUJ PORTAL`, sign-in and parent-login labels, a Keen login stylesheet, a custom login JavaScript path, and current public form evidence including a POST action and verification-token fields. The action is to model the MUJ host as a login-centric MVC-style shell with a separate question about post-authenticated functionality. [6] [8] [25] [26] [14]
- **Technology fingerprint**: A public header observation dated 25 August 2026 reports `Microsoft-IIS/10.0`, `X-AspNetMvc-Version: 5.3`, `X-AspNet-Version: 4.0.30319`, and `X-Powered-By: ASP.NET`. This strongly supports the supplied IIS, ASP.NET MVC 5.3, and .NET Framework-family description for the observed response, but it is a point-in-time fingerprint rather than a source-code audit. [18]
- **Identity integration**: The MUJ login surface exposes `@muj.manipal.edu`, student and parent login labels, and a Microsoft password-reset URL; the official FAQ says the password follows the official Outlook ID and separately describes MUJ Outlook-account support. This supports an operational Microsoft 365 identity relationship, but the gathered public evidence does not prove that the application itself performs OpenID Connect authentication. [14] [13] [13]
- **Removed-page conclusion**: Historical 404 captures show that particular URL requests returned 404 at particular times. The same route names also appear in other captures with 302 or 303 responses, so intentional removal, renaming, authorization gating, and archive artifacts remain competing explanations. The action is to label removal as unproven unless a before-and-after replay demonstrates it. [11] [22]
- **Akamai status**: The supplied research brief identifies Akamai as a deployment context, but the evidence assembled here does not independently establish the CDN path. The action is to mark Akamai as "not independently confirmed in this corpus" rather than infer it from an IIS origin header.

## Scope, Method, and Evidence Rules

The scope is deliberately narrow: the historical host `slcm.manipal.edu` from 2017 onward, the MUJ host `mujslcm.jaipur.manipal.edu` from 2025 onward, and public documentation that explains the student portal and account workflow. The Wayback Machine help material says that archived pages can be referenced and that URL and date specification can be used to locate captures. [12] The archive is therefore treated as a source of timestamped observations, not as a complete export of the live application.

The evidence process has four layers. First, CDX queries identify captured URL keys, timestamps, MIME types, and HTTP status codes. Second, selected replays establish what the archived body actually contained. Third, public static assets and page labels provide context for interface generations. Fourth, official MUJ and MAHE documents are used to distinguish a documented student workflow from a route name or an inferred feature. This matters because a CDX record with status 200 can represent a custom error page, and a URL with a 302 or 303 does not reveal its destination or whether the redirect came from authentication, authorization, routing, or an application error.

The report uses the following evidence vocabulary:

| Evidence label | Meaning in this report | Safe interpretation |
|---|---|---|
| **Observed** | The URL, response, page text, header, or official statement is directly present in a cited source. | State the fact narrowly and preserve its timestamp. |
| **Strong inference** | Multiple independent observations point to the same implementation pattern. | State the inference explicitly and do not turn it into source-code certainty. |
| **Working inference** | A route name, asset name, or status pattern suggests a possibility but has competing explanations. | Use terms such as "suggests," "consistent with," and "not proven." |
| **Unknown** | The public corpus does not settle the issue. | Do not fill the gap with a guess. |

The report intentionally omits captured query-string values from payment-related URLs. The CDX evidence establishes that `PaymentResponse.aspx` was captured, but transaction parameters are not reproduced because they are unnecessary for the historical conclusion and could contain sensitive identifiers. [23] The same public-only rule applies to password fields, verification tokens, cookies, and any credential-like material. The current header source itself shows a verification cookie value, but this report identifies only the header class and never reproduces the value. [18]

### Analytical reasoning summary, not private chain-of-thought

The request asks for explicit chain-of-thought. I cannot provide private internal chain-of-thought. I can provide an auditable reasoning summary: (1) define the two hostnames and date windows; (2) enumerate CDX records by status, MIME type, route family, and asset family; (3) replay representative pages; (4) compare route names with the actual archived bodies; (5) cross-check the current MUJ surface against public headers and official documentation; (6) classify each conclusion as observed, inferred, or unknown; and (7) avoid treating archive gaps or guessed paths as proof of removal or vulnerability. This method produces a reproducible evidence trail without exposing private deliberation.

The central analytical rule is simple: a page body outranks a status-only row, an official document outranks a guessed route name, and a current header snapshot describes only the response that was observed. Applying that rule prevents three common errors: calling a custom 404 page a working endpoint, calling an archived route a current feature, and calling a Microsoft password-reset link proof of application-level SSO.

## exact_tables: Capture and endpoint ledger

### Table 1. Host-level timeline from 2017 through 2026

| Approximate capture date | Host and artifact | Direct observation | Interpretation and limit |
|---|---|---|---|
| 14 July 2017 | `slcm.manipal.edu/loginForm.aspx` | CDX records a text/html 200 capture for the original HTTP URL. [19] | High-confidence evidence that this login URL was captured as an HTML response. The capture alone does not establish successful authentication or current existence. |
| 20 July 2017 | `slcm.manipal.edu/StudentChangePassword.aspx` | CDX and replay evidence show a student password-change page with old, new, and confirmation password labels. [19] [7] | Strong evidence of a separate student password-management page in the archived interface. It does not show whether the page was reachable without a session. |
| 13 August 2017 | `slcm.manipal.edu/ParentChangePassword.aspx` | The archived parent page presents the same three password-change labels and a Manipal home link. [19] [5] | Strong evidence that parent and student account-management surfaces were distinct historical pages. |
| 2017-2018 | Legacy academic route family | CDX rows record route names such as `Academicdashboard.aspx`, `ClassAttendance.aspx`, `CourseFeedback.aspx`, `CreateTimeTable.aspx`, `GradeSheet.aspx`, `Pre-Registration.aspx`, and `Results.aspx`, frequently with 302 or 303 responses. [22] | Strong route-vocabulary evidence. The status codes suggest redirect behavior, but the archive excerpt does not identify each redirect destination or prove a successful feature page. |
| 24 April 2018 | Legacy CSS, JavaScript, and image assets | Captures include Bootstrap CSS and JavaScript, jQuery 2.0.3, common CSS, and MU-branded images under `/assets`. [27] | Evidence of a conventional Bootstrap/jQuery web interface at that point. Asset presence does not prove which page loaded each asset. |
| January 2019 | Legacy Web Forms assets | Captures include `MicrosoftAjax.js` and `MicrosoftAjaxWebForms.js` under `/Scripts/WebForms/MsAjax/`. [20] | Strong implementation-era signal consistent with ASP.NET Web Forms on the legacy host. It is not a complete inventory of server-side code. |
| 18 November 2020 | Legacy host root | The root has a text/html 200 CDX record, while replay text is sparse and includes a confirmation prompt with "Are You Sure?" and "No." [2] [4] | The host was archived, but the replay is incomplete or mostly dynamic. It cannot be used to reconstruct the full landing page. |
| 30 March 2022 | `slcm.manipal.edu/WebForm1.aspx` | The CDX row is status 200, but the replay title/body says `404 Error Page`. [23] [24] | A concrete example of why archive metadata and page content must be read together. The URL was captured; the body did not represent a working page. |
| 2024 | Legacy 404 and route-noise records | Several grade, result, registration, and malformed timetable variants return captured 404 responses. [11] | Evidence of failed requests at capture times. It does not prove deliberate deletion or explain whether the requests were crawlers, users, or application links. |
| 10 January 2025 | MUJ `Home/Index` | CDX records a text/html 200 capture for `mujslcm.jaipur.manipal.edu/Home/Index`. [21] | Strong evidence that the MUJ route was publicly captured during the 2025 window. |
| 27 May 2025 | MUJ root | CDX records a text/html 200 capture for the MUJ root. [21] | Confirms a second public HTML capture in the requested MUJ period. It does not show post-login pages. |
| January 2025 | MUJ Keen login assets | CSS captures include the Keen theme login stylesheet, while JavaScript captures include a custom user-login path and `scripts.bundle.js`. [25] [26] | Strong evidence of a themed, bundled login front end. Asset naming does not establish the exact server-side framework by itself. |
| 25 October 2025 | MUJ redirect records | CDX records 302 responses for generic `.well-known`, ads, feed, robots, and sitemap-style requests. [10] | These are archive-observed redirects, not evidence that those paths are MUJ application features. They illustrate background request noise. |
| December 2025 to June 2026 | Legacy print, payment, and dashboard assets | The legacy CDX corpus contains `Print.aspx`, `PaymentResponse.aspx`, and asset names including `main.js`, `financedashboard.js`, and `academic-chart.js`; query values are intentionally omitted here. [23] | Evidence that the legacy hostname continued to generate or receive captures after the early Web Forms period. It may reflect coexistence, migration residue, or third-party/payment workflows; the archive does not settle which. |
| 5 August 2026 | MUJ asset and error records | CDX records 302 responses for font assets and a 404 response for `watermark.png`. [10] [28] | Shows continued archive activity and individual asset failures. It does not establish a broad outage or application-level removal. |

**Table takeaway.** The key change is not a clean replacement date. It is a long coexistence pattern: the legacy hostname retains `.aspx` and academic/payment vocabulary, while the MUJ hostname appears in the 2025 archive mainly through a login shell and modern asset organization. The evidence supports a migration or parallel-stack hypothesis, but not a single proven cutover event.

### Table 2. Historical endpoint ledger and evidentiary strength

| Endpoint or route family | Archive observation | What it supports | What it does not prove |
|---|---|---|---|
| `/loginForm.aspx` | 2017 text/html 200 capture. [19] | A historical legacy login URL existed in the archive corpus. | That credentials were accepted, that it was unauthenticated, or that it remains live. |
| `/StudentChangePassword.aspx` | 2017 page labels include old, new, and confirmation password fields. [7] | A student-facing password-change workflow was rendered in the archived page. | Password policy, backend validation, or current reachability. |
| `/ParentChangePassword.aspx` | 2017 page labels include the same password-change fields. [5] | A separate parent-facing password workflow was rendered. | That parent and student accounts used separate databases or roles. |
| `/Academicdashboard.aspx` | 2017 route captured with status 302. [22] | The URL was requested and the response redirected. | The dashboard contents or the redirect target. |
| `/ClassAttendance.aspx` and related attendance routes | 2017 route family captured with 302 responses. [22] | Attendance was part of the historical route vocabulary. | Whether every route was a user-facing production feature or a protected route. |
| `/CourseFeedback.aspx` | 2017 302 record; a later `CourseFeedbackForHSkmc.aspx` 302 record also appears. [22] | Feedback-related routing existed in the observed archive requests. | The applicable school, workflow, or permission model. |
| `/CreateTimeTable.aspx` and timetable variants | 2017 `CreateTimeTable.aspx` 302 and a later reschedule-timetable record are present. [22] | Timetable administration or display was represented in route names. | That students could access the administrative-sounding create route. |
| `/GradeSheet.aspx`, `/Grade.Sheet.aspx`, and `/Results.aspx` | The routes appear with 302 or 303 records in some captures and with 404 records in other captures. [22] [11] | Route handling changed across time or request context. | A simple conclusion that the pages were permanently removed. |
| `/Pre-Registration.aspx`, `/Re_Registration.aspx`, and fee-related variants | Registration and re-registration paths appear in 302 records, while a later re-registration request appears as 404 in the 404 corpus. [22] [11] | Registration was a meaningful historical route family. | Whether the later 404 was a removal, a bad request, an authorization result, or an archive artifact. |
| `/WebForm1.aspx` | 2022 CDX 200 row, but replay is an explicit 404 page. [23] [24] | The archive captured a named endpoint and its error body. | That `WebForm1.aspx` was a working feature endpoint in 2022. |
| `/Print.aspx` and `/PaymentResponse.aspx` | Both appear in later legacy-host CDX data. [23] | Print/payment response functionality remained visible in the archive corpus. | Payment success, transaction validity, or safe handling of archived query parameters. |

**Table takeaway.** The route ledger is most useful as a map of historical application vocabulary. It is not a current attack surface list. The repeated mixture of 200, 302, 303, and 404 responses is exactly why each path must remain tied to its timestamp and response body.

## Legacy Login Pages and the Web Forms Era

The strongest historical evidence is the 2017 authentication and password-management surface. The CDX login filter returns `loginForm.aspx`, `ParentChangePassword.aspx`, and `StudentChangePassword.aspx` as text/html 200 captures in July and August 2017. [19] The student replay exposes the labels `Change Password`, `Enter Old Password:`, `Enter New Password:`, and `Enter Confirm Password:`. [7] The parent replay exposes the same workflow. [5] This is more informative than a filename alone because the archived body confirms that the password-management interface actually rendered those labels.

The 2017 login replay itself is less complete. The available cleaned replay contains a Manipal home link and a fragmentary closing parenthesis, and the extraction result explicitly says that replay completeness is not established. [3] A search result for the same historical page identifies it as `MU SLcM Sign in to your account` and associates it with Manipal Academy of Higher Education. [17] The defensible conclusion is therefore that a branded login page existed in the archive corpus, not that every form field or authentication mechanism can be reconstructed from the replay.

The endpoint grammar and assets reinforce the historical generation. The host uses `.aspx` page names across login, password, results, registration, attendance, timetable, and payment-related paths. [19] [22] The 2019 archive contains files explicitly named `MicrosoftAjax.js` and `MicrosoftAjaxWebForms.js`. [20] Together, these observations strongly support a Web Forms-era interface on the legacy host. This is a strong inference about the application surface and client framework family, not proof that every server component was implemented in one project or that no MVC modules existed behind the same hostname.

### Case study: `WebForm1.aspx` and the danger of a status-only conclusion

`WebForm1.aspx` is the clearest case study because it exposes a direct contradiction between archive metadata and page content. The filtered CDX row says that the URL was captured with status 200 and text/html. [23] If that row were read without opening the replay, an analyst might incorrectly report a working endpoint. The replay instead identifies `404 Error Page` and references an error image. [24]

The mechanism is straightforward: applications often return a custom error document with a nominal HTTP status that is not a reliable semantic description, and archive tooling records what it received. The implication is that route inventories must combine status, body title, visible labels, and timestamp. The recommendation for a security club is to maintain two separate fields in every worksheet: `archive_status` and `body_interpretation`. This prevents a historical 200 from being promoted to a verified feature.

### Case study: grade and result routes that change status

The grade and result route family demonstrates a second tension. `GradeSheet.aspx`, `Grade.Sheet.aspx`, and `Results.aspx` appear in redirect records at some times, while similar or identical variants appear in captured 404 records at other times. [22] [11] A malformed spelling such as `gardesheet.aspx` also appears among the 404 requests. [11]

Several mechanisms can produce this pattern: a route can be renamed, moved behind an authentication redirect, handled differently by a virtual directory, requested with a typo, or recorded as a custom error by the archive. The evidence does not select one explanation. The insight is therefore not "the university removed grades" but rather "the legacy route surface was not stable enough to infer feature lifecycle from one response." The safe research action is to create a before-and-after table per exact URL, preserve date and status, and keep body-based conclusions separate from route-name hypotheses.

## What the 2017-2024 Timeline Says About Feature Evolution

The historical route names describe a broad student-information-system vocabulary. The observed set includes academic dashboards, attendance views and reports, course feedback, timetables, examination attendance, grades, results, pre-registration, re-registration, and password management. [22] The older asset set includes Bootstrap, jQuery 2.0.3, common CSS, and MU-branded imagery. [27] The 2019 MicrosoftAjax Web Forms files add a more specific implementation signal. [20]

The official public documentation gives a separate, current-facing view of the portal's purpose. The MAHE student portal page says it provides access to web services and information related to everyday life as a student at MAHE. [16] The official MUJ FAQ gives more concrete account and administrative workflows: it lists the MUJ SLCM registration link, specifies a username made from a name and registration number, says the password follows the official Outlook ID, and gives AMS contact routes for login trouble. [13]

The FAQ also describes operational boundaries around the portal. Personal details entered at admission can be changed by the admission department after verification, qualifying-examination-result issues go to admission, and orientation-date issues go to an assigned coordinator. [13] These statements do not prove that each historical route remains present, but they show that the portal sits inside a larger administrative process rather than operating as a standalone login page.

### Table 3. Feature evolution: documented workflow versus route inference

| Capability or domain | Historical archive evidence | Official or current corroboration | Confidence and correct wording |
|---|---|---|---|
| Authentication and password change | `loginForm.aspx` plus separate student and parent password-change pages are captured in 2017. [19] [7] [5] | MUJ current page exposes sign-in, parent login, and student login labels. [8] | **High** for historical and current login surfaces. Do not claim identical authentication code. |
| Student and parent role separation | Separate historical student and parent password pages; current MUJ page has parent and student labels. [7] [5] [14] | The role labels are directly visible. | **High** for separate interface roles; **unknown** for database or authorization design. |
| Academic results and grades | `GradeSheet.aspx`, `Grade.Sheet.aspx`, and `Results.aspx` route names appear in redirect and 404 corpora. [22] [11] | The public FAQ discusses a qualifying-examination result issue handled by admission. [13] | **Medium** for historical result-related functionality; no proof of a current public results page. |
| Attendance | Multiple `ClassAttendance` route names are captured with 302 responses. [22] | No cited current FAQ statement confirms a current attendance page. | **Medium-low**: route vocabulary only, not current feature confirmation. |
| Timetable | `CreateTimeTable.aspx`, `DefaultAttendance.aspx`, and rescheduling-related routes appear in the redirect corpus. [22] | No cited current page confirms current timetable implementation. | **Medium-low**: historical route evidence, not a current feature claim. |
| Course feedback | `CourseFeedback.aspx` and a later specialized feedback route appear with 302 responses. [22] | No cited current public documentation confirms the current implementation. | **Medium-low**: route-family evidence only. |
| Registration and onboarding | Pre-registration and re-registration paths appear in the legacy archive. [22] | The official FAQ provides the current registration link and username/password onboarding model. [13] | **High** for documented onboarding; **medium** for continuity of the legacy route names. |
| Personal-details correction | No route body is needed to establish the workflow. | The FAQ says admission controls changes after verification. [13] | **High** for the documented administrative process. |
| Orientation support | Not established by the route corpus. | The FAQ directs students to an assigned coordinator and says to meet the coordinator after arrival. [13] | **High** for the public workflow; not evidence of a particular endpoint. |
| Printing and payment response | `Print.aspx` and `PaymentResponse.aspx` appear in later legacy-host captures. [23] | The supplied official FAQ does not establish their current implementation. | **Medium** for historical endpoint presence; low for current behavior. |

**Table takeaway.** The system's historical surface appears functionally broad, but the public evidence is asymmetric: route names reveal breadth, while the official FAQ confirms only selected administrative workflows. The responsible conclusion is feature continuity in purpose, not proven continuity in code or URL.

A plausible evolution model is therefore a layered one. The old host seems to have accumulated many Web Forms pages and static assets over time. The later records show specialized financial and academic assets as well as print and payment paths. The MUJ host, by contrast, is publicly visible first as a branded entry shell. That pattern is consistent with a migration in which the front door was modernized or relocated while some legacy services remained archived under the older hostname. It remains an inference because the captures do not provide a deployment diagram, source repository, database migration, or authenticated post-login replay.

## MUJ SLCM from 2025: Login Shell, Assets, and Current Public Surface

The MUJ archive begins with a small but coherent public surface. The January 2025 `Home/Index` record and May 2025 root record are both text/html 200 captures in the filtered CDX output. [21] The January replay says `WELCOME TO MUJ PORTAL` and `Sign In`. [6] A current extraction adds `@muj.manipal.edu`, `Sign In Parent Login`, and separate student and parent labels. [8]

The static asset evidence is particularly useful because it is more specific than a visual label. The CSS corpus includes a Keen theme login stylesheet at a path ending in `pages/login/login-v1.css`. [25] The JavaScript corpus includes `pages/custom/user/login.js` and a bundled script. [26] These are consistent with a deliberately themed login application rather than a raw default error page. They do not, by themselves, prove that Keen authored the server-side application or that the current backend is a particular MVC version.

The current public page evidence supplies a more detailed interface snapshot. The visible surface includes a root POST form, student and parent login choices, username and password inputs represented by names such as `txtUserName` and `txtPassword`, hidden login-context fields, and a verification-token field. [14] The same extraction reports a Forgot Password link to `https://passwordreset.microsoftonline.com/`. [14] Those details are enough to describe the public login contract at a high level without reproducing tokens or attempting a submission.

### Table 4. MUJ 2025+ archive evidence

| MUJ artifact | Timestamp or period | Evidence | Meaning and limit |
|---|---|---|---|
| `Home/Index` HTML | 10 January 2025 | CDX text/html 200 row. [21] | A public MUJ landing route was archived. It does not expose authenticated features. |
| Root HTML | 27 May 2025 | CDX text/html 200 row. [21] | A second public entry-page capture exists. It does not prove that the root and `Home/Index` were separate applications. |
| Archived landing labels | January 2025 replay | `WELCOME TO MUJ PORTAL` and `Sign In`. [6] | Direct evidence of the MUJ-branded login presentation. |
| Current role labels | Current public extraction | Student login, parent login, and `@muj.manipal.edu` are visible. [8] | Direct evidence of the public role-oriented login surface. |
| Login CSS | January 2025 | Keen login-v1 stylesheet path. [25] | Evidence of the front-end theme and login asset family. |
| Login JavaScript | January 2025 | Custom user-login script and scripts bundle. [26] | Evidence of a custom client-side login asset family. |
| Generic redirect requests | 25 October 2025 | `.well-known`, ads, feed, robots, and sitemap-style requests return 302 in the CDX result. [10] | Archive request noise and redirects, not proof of application features. |
| Font assets | 5 August 2026 | Font paths return 302 in a later CDX query. [10] | Indicates captured redirect behavior for assets, not a functional conclusion. |
| `watermark.png` | 5 August 2026 | A 404 text/html record is present. [28] | One missing asset at one capture time, not evidence of a broad failure. |

**Table takeaway.** The MUJ record is capture-sparse compared with the legacy route corpus. Its strongest public evidence is the entry surface and asset family, not a feature-by-feature post-login history. The absence of additional public HTML captures should be treated as archive coverage uncertainty rather than proof that MUJ had no other functions.

The contrast with the legacy host is important. The old host gives us many names but incomplete bodies. The MUJ host gives us a clearer public shell but few post-login artifacts. This is a classic OSINT asymmetry: the older system is more verbose in URL vocabulary, while the newer system is more legible at the front door. A migration analysis that uses only route counts will overstate knowledge of the old system; one that uses only the current login page will understate the historical breadth of the student-information workflow.

## Technology Signals and What They Say About the Codebase

The most direct current technology evidence is a public header observation for the MUJ host. It reports HTTP 200, `Server: Microsoft-IIS/10.0`, `X-AspNetMvc-Version: 5.3`, `X-AspNet-Version: 4.0.30319`, `X-Powered-By: ASP.NET`, and an `X-Frame-Options: SAMEORIGIN` header. [18] This is strong evidence for the supplied technology fingerprint at the time of observation. `4.0.30319` should be described precisely as the ASP.NET version-family value returned in the header; it is not, by itself, a complete .NET Framework patch-level inventory.

The public page and header evidence also show different layers. The current page extraction exposes a verification-token field and jQuery 1.10.2, while the header observation exposes a server-side MVC version and ASP.NET version-family string. [14] [18] The first set describes page construction and client-side behavior; the second describes response metadata. Neither provides source code, controller names, route registration, database schema, or build configuration.

### Table 5. Technology evidence matrix

| Technology or architectural claim | Direct evidence | Confidence | Correct conclusion |
|---|---|---|---|
| IIS 10 on the observed MUJ response | `Server: Microsoft-IIS/10.0`. [18] | High for the observation | The public response identifies Microsoft IIS 10.0. Do not generalize to every backend host or every historical date. |
| ASP.NET MVC 5.3 | `X-AspNetMvc-Version: 5.3`. [18] | High for the observation | The observed response advertises ASP.NET MVC 5.3. It does not prove every MUJ endpoint uses MVC. |
| .NET Framework 4.x family | `X-AspNet-Version: 4.0.30319`. [18] | High for the returned header, medium for broad platform wording | The response exposes the ASP.NET version-family value 4.0.30319. It does not reveal patch level or application configuration. |
| ASP.NET server stack | `X-Powered-By: ASP.NET` and ASP.NET-related version headers. [18] | High | The response identifies ASP.NET at the web layer. |
| Request-verification mechanism | Current extraction reports hidden verification-token fields; header observation reports a `__RequestVerificationToken` cookie class. [14] [18] | Medium-high | A request-verification pattern is publicly visible. Its correctness or security strength was not tested. |
| MVC/Web Forms historical divergence | MUJ advertises MVC 5.3, while the old host has `.aspx` pages and MicrosoftAjax WebForms assets. [18] [19] [20] | High as a cross-host difference; medium as a migration claim | The public surfaces belong to visibly different implementation eras or stacks. A shared backend cannot be ruled out without deeper evidence. |
| Keen/jQuery login front end | MUJ Keen CSS and custom login JS captures; current extraction reports jQuery 1.10.2. [25] [26] [14] | High for asset presence | The entry page uses a themed and bundled front-end family. Asset presence is not proof of vendor ownership of the whole application. |
| Akamai reverse proxy or CDN | No gathered citation independently identifies Akamai. | Low | Keep the supplied Akamai description as an external research premise, not a verified conclusion of this report. |

**Table takeaway.** The evidence supports a meaningful stack transition: legacy Web Forms-era artifacts on `slcm.manipal.edu` and an observed MVC 5.3/IIS 10 response on `mujslcm.jaipur.manipal.edu`. It does not support a stronger claim such as "the entire old application was rewritten in MVC" because no source shows a complete deployment boundary.

### Case study: the old Web Forms surface versus the MUJ MVC response

The old host is represented by page grammar and assets: `.aspx` route names, separate password pages, Bootstrap and jQuery assets, and explicit MicrosoftAjax Web Forms files. [7] [27] [20] The MUJ host is represented by an MVC version header, a root login shell, a verification-token pattern, Keen assets, and a current form-oriented page. [14] [18]

The mechanism suggested by this contrast is not necessarily a single rewrite. It could be a new MUJ front end, a parallel deployment, a staged migration, or a separate application serving a similar institutional function. The implication is that codebase lineage should be described as "evidence of distinct public implementation eras" rather than "proven code replacement." The safe recommendation is to keep host-level timelines separate until a public artifact links a legacy endpoint to a MUJ controller, redirect, official migration notice, or shared asset pipeline.

## Microsoft 365 Identity and Account-Recovery Evidence

The identity evidence is substantial but bounded. The current MUJ page displays `@muj.manipal.edu`, student and parent login labels, and a Forgot Password link. [14] The focused extraction identifies that link as `https://passwordreset.microsoftonline.com/`. [14] This is direct evidence that the public recovery journey delegates or points users toward Microsoft's password-reset service.

The official MUJ FAQ independently says that the SLCM password is "as per official outlook ID" and provides a registration link at the MUJ host. [13] A separate FAQ entry addresses a non-working MUJ Outlook account, instructs users to reset the password, and directs unresolved issues to Team IT Infra. [13] The two sources converge on an operational identity model in which the institutional Outlook account matters to SLCM access and support.

A public OpenID configuration endpoint for `muj.manipal.edu` also returns Microsoft identity metadata, including an issuer, authorization endpoint, token endpoint, and Microsoft Graph-related hosts. [29] This proves that public Microsoft identity configuration exists for the domain or tenant context. It does not prove that the SLCM application uses that configuration, because the gathered evidence does not show an application client identifier, redirect URI, callback route, authorization request, or token exchange tied to SLCM.

### Table 6. Identity claims and confidence

| Claim | Evidence | Confidence | Boundary |
|---|---|---|---|
| MUJ uses institutional-domain login labels | `@muj.manipal.edu`, student login, and parent login are visible. [8] | High | Labels do not reveal the authentication protocol. |
| Password recovery points to Microsoft | Current extraction identifies `passwordreset.microsoftonline.com`. [14] | High | A recovery link is not proof that the login form itself is an OAuth or OIDC client. |
| Official Outlook credentials are relevant operationally | The FAQ says the password follows the official Outlook ID and separately discusses MUJ Outlook-account support. [13] [13] | High | This supports account relationship and support workflow, not a complete identity architecture diagram. |
| Microsoft OpenID metadata exists | The public Microsoft OpenID configuration endpoint returns tenant identity metadata. [29] | High | It does not tie SLCM to a particular client registration or callback. |
| SLCM directly performs OIDC SSO | No captured public artifact in this corpus shows a SLCM authorization redirect, callback, client ID, or token exchange. [14] [29] | Low to medium | Report as unproven, not false. |

**Table takeaway.** The safest description is "Microsoft-linked identity and recovery workflow," not "proven Microsoft SSO." That wording preserves what the official FAQ and public page establish while avoiding an architectural claim that would require authenticated or configuration-level evidence.

For a university security club, this distinction is operationally important. Password reset, Outlook support, and an OpenID discovery document are adjacent signals. They may belong to one integrated identity design, but they may also be connected through institutional process rather than direct application federation. Treating them as equivalent would produce a false-positive architecture diagram and could lead to unsafe assumptions about session handling.

## Removed Pages, 404s, Redirects, and Archive Noise

The archive contains many failed or ambiguous requests. The legacy 404 corpus includes spelling variants such as `gardesheet.aspx`, `Grade.Sheet.aspx`, `GradeSheet.aspx`, `Gradsheet.aspx`, and `marksheet.aspx`, along with `Result.aspx`, `Results.aspx`, `Re_Registration.aspx`, and a malformed timetable path. [11] The same general route families also occur in redirect records. [22] That divergence is a central finding, not a nuisance to be smoothed away.

### Table 7. What can and cannot be said about apparent removal

| Observation | What can be stated | What remains unanswered |
|---|---|---|
| A named route has a captured 404 | The request returned or was recorded as a 404 at the cited timestamp. [11] | Whether the route was intentionally removed, mistyped, protected, moved, or represented by a custom error page. |
| The same route has a 302 or 303 elsewhere | The route produced a redirect response in another capture. [22] | The destination, user state, and reason for redirect. |
| `WebForm1.aspx` has CDX 200 but replay 404 | The archive metadata and page body disagree semantically; the replay body is the stronger page-level evidence. [23] [24] | Why the application or archive recorded the nominal 200. |
| `.well-known` and common-file paths have redirect records | Those paths were present in archive requests and yielded 302 records. [10] | Whether a human, crawler, scanner, or automated service generated the requests. |
| A single image has a 404 | The image was missing or unavailable in that capture response. [28] | Whether the page was broken, whether a fallback existed, or whether the asset was nonessential. |

**Table takeaway.** "Removed page" is too strong for the available evidence. The archive supports the narrower statement "a URL returned 404 in a particular capture." A removal claim requires a documented before-and-after sequence, a current official link change, or a body-level comparison that rules out request errors and authorization behavior.

The route-noise pattern is also relevant to OSINT interpretation. Generic `.well-known`, ads, feed, robots, sitemap, and asset paths appear in redirect or error queries on both hosts. [11] [10] These records may reflect crawler behavior or broad URL collection rather than intentional application design. They should not be turned into a list of alleged hidden features. Likewise, an old route name is not a vulnerability, and a public 404 is not evidence that the server is misconfigured.

A safer timeline language is therefore: "the archive observed route X with response Y at time T." Only after that should an analyst add a clearly marked inference such as "this may indicate a route transition." This discipline is particularly important for a student research project because it preserves the difference between historical documentation and active security testing.

## Comparative Analysis: Legacy Host versus MUJ Host

### Table 8. Cross-host comparison across mechanism, scope, trade-offs, and evidence

| Dimension | `slcm.manipal.edu` legacy corpus | `mujslcm.jaipur.manipal.edu` MUJ corpus | Analytical consequence |
|---|---|---|---|
| Main evidence period | 2017 onward, with dense old route and asset evidence. [19] [22] | 2025 onward, with a small number of public HTML captures and login assets. [21] [25] [26] | The two corpora have unequal coverage; raw capture counts cannot be compared as application size. |
| URL grammar | `.aspx` pages for login, password, grades, results, attendance, timetable, registration, print, and payment. [7] [22] [23] | Root and `Home/Index` entry routes with Keen login asset paths. [21] [25] | The grammar supports different public implementation eras. |
| Technology evidence | MicrosoftAjax Web Forms assets and Bootstrap/jQuery assets. [27] [20] | Current header advertises IIS 10, MVC 5.3, ASP.NET 4.0.30319, and ASP.NET. [18] | Strong stack divergence, but not proof of a full rewrite or shared database. |
| Feature visibility | Broad route vocabulary but limited body-level replay. [22] [11] | Clear public login shell but little public post-login content. [8] [14] | Legacy gives breadth; MUJ gives front-door clarity. |
| Authentication model evidence | Separate student and parent password pages; login replay incomplete. [7] [5] [3] | Student/parent labels, Microsoft recovery link, and verification-token pattern. [14] | Role continuity is plausible; protocol continuity is unproven. |
| Failure semantics | Mixed 200, 302, 303, and 404 records, including a 200 CDX row with a 404 body. [23] [11] [22] | Redirects for some generic paths and one asset 404 in later captures. [10] [28] | Archive status requires body and timestamp context on both hosts. |
| Functional trade-off | Historical breadth makes feature mapping possible but invites overinterpretation. | Modern login evidence is easier to describe but gives little public feature history. | Use separate evidence models rather than force a single unified inventory. |
| Identity evidence | Legacy public pages do not establish Microsoft identity integration. [3] | MUJ page and FAQ connect login operations to `@muj.manipal.edu`, Outlook, and Microsoft reset. [14] [13] | Identity continuity is better supported for MUJ than for the archived legacy login. |
| CDN or edge conclusion | No independent Akamai evidence in the gathered citations. | IIS header is visible in a point-in-time public observation. [18] | Do not use either host's surface alone to infer the full network path. |

**Table takeaway.** The non-obvious tension is that the newer MUJ host is technically clearer but historically less transparent, while the older host is historically richer but semantically noisier. The best report therefore joins the two timelines cautiously: it identifies continuity of institutional purpose and role vocabulary, while keeping implementation lineage and migration timing as open questions.

The principal divergence is between feature breadth and evidence quality. A route list can make the old system look fully understood, but its 302 and 404 behavior shows that the list is not a functional inventory. Conversely, the MUJ root page and current header can make the new system look simple, but the official FAQ and identity links show that the login shell is part of a wider administrative ecosystem. The appropriate synthesis is layered rather than linear.

## Research Gaps and Safe Next Questions

The following questions remain unanswered by public evidence gathered here. They are deliberately framed as documentation questions, not instructions for probing the system.

| Open question | Why it remains open | Safe evidence that could answer it |
|---|---|---|
| Was there a formal migration from the legacy host to MUJ? | The timelines overlap, but no public migration notice or definitive redirect chain was found in the cited corpus. | An official university announcement, archived help page, or public documentation naming the transition. |
| Does MUJ expose authenticated academic modules after login? | The public captures focus on the entry page, and no authenticated replay is used. [8] [14] | Official user documentation or publicly accessible, non-authenticated feature descriptions. |
| Is the current login directly federated with Microsoft OIDC? | The recovery link, Outlook wording, and OpenID metadata are adjacent but no callback or client configuration is shown. [13] [29] [14] | Official identity architecture documentation or a public vendor/institutional integration notice. |
| Are old `.aspx` routes still deployed? | Historical CDX captures are not current reachability tests, and current MUJ evidence is a different hostname. [23] [18] | A current official link, current public archive capture, or authorized assessment. |
| Why do identical-looking routes alternate between redirect and 404? | Archive captures lack consistent destination, headers, session state, and application logs. [11] [22] | Additional timestamped public replays with complete headers and bodies, or authorized server-side documentation. |
| Is Akamai in front of the MUJ host? | The supplied brief says so, but the gathered evidence does not independently identify an Akamai edge. | An official DNS/CDN architecture statement or authorized infrastructure documentation. |
| Which later assets belong to which authenticated module? | Asset path names such as `financedashboard.js` and `academic-chart.js` are suggestive but not enough to map a runtime page. | Public release documentation, archive replays of the referring HTML, or authorized application documentation. |

The safe next research phase is archival rather than active. A club can preserve exact CDX query URLs, replay URLs, capture timestamps, response status, visible page text, and the distinction between HTML and asset records. It can compare official FAQ revisions and university portal descriptions. It should not submit credentials, replay captured tokens, bypass login, guess passwords, scan for hidden paths, or attempt to validate whether a historical endpoint is currently reachable without written authorization.

## VERDICT

### Confidence-ranked findings

| Finding | Confidence | Verdict |
|---|---|---|
| The historical `slcm.manipal.edu` public surface includes Web Forms-era `.aspx` pages and MicrosoftAjax Web Forms assets. | **High** | Supported by captured password pages, route grammar, and explicit WebForms asset names. [7] [5] [20] |
| The legacy host had a broad route vocabulary covering authentication, attendance, feedback, timetable, grades, results, registration, print, and payment-related paths. | **High for route vocabulary; medium for feature availability** | The names and response records are directly captured, but route names do not prove user-facing success. [22] [23] |
| The 2022 `WebForm1.aspx` record is not evidence of a working page. | **High** | The CDX row is 200 but the replay body is an explicit 404 error page. [23] [24] |
| The MUJ host has a 2025+ public login shell with student and parent role labels and a Keen/jQuery-style asset family. | **High** | Supported by archived labels, current labels, and captured CSS/JavaScript paths. [6] [8] [25] [26] |
| The observed MUJ response advertises IIS 10, ASP.NET MVC 5.3, ASP.NET 4.0.30319, and ASP.NET. | **High for the dated response** | Directly present in a point-in-time public header observation on 25 August 2026. [18] |
| The MUJ public identity workflow is linked operationally to institutional Outlook and Microsoft password recovery. | **High** | The page and official FAQ independently support this narrow claim. [14] [13] [13] |
| The MUJ application itself uses direct Microsoft OIDC or OAuth SSO. | **Low to medium, unproven** | Microsoft OpenID metadata exists and the recovery link is Microsoft-based, but no public callback, client identifier, or token exchange is cited. [29] [14] |
| The MUJ host is behind Akamai. | **Low in this report** | It is supplied as research context but not independently established by the gathered public evidence. Do not present it as verified. |
| Specific historical pages were intentionally removed. | **Low to medium, route-specific only** | 404 captures establish responses at timestamps, while other captures show redirects for related routes. Intentional removal is not proven. [11] [22] |
| The MUJ host is a complete replacement for the legacy host. | **Low to medium, migration hypothesis** | The stack and URL patterns differ, but no public artifact proves a complete replacement, cutover date, or shared data layer. [20] [18] |

### Overall verdict

**Overall confidence: Medium-high for the historical surface and current public technology fingerprint; medium for the migration narrative; low-to-medium for claims about removed pages, direct Microsoft SSO, and Akamai.** The most defensible narrative is that Manipal's public SLCM ecosystem shows at least two implementation eras. The older `slcm.manipal.edu` corpus exposes a Web Forms-style academic portal vocabulary with separate student and parent password pages, route redirects, static Bootstrap/jQuery assets, and later print/payment-related captures. The MUJ host presents a newer login-focused public surface whose observed response advertises ASP.NET MVC 5.3 on IIS 10 and whose account workflow is operationally tied to the `@muj.manipal.edu` and Outlook identity context. [7] [20] [23] [14] [18] [13]

The codebase conclusion must remain carefully worded. **Observed:** the two public surfaces differ in URL grammar, assets, and the current MUJ response headers. **Strong inference:** the hosts represent distinct public implementation eras, and a staged migration, parallel deployment, or modernization is plausible. **Not established:** that the old code was fully rewritten, that every old feature moved to MUJ, that old pages were deliberately removed, that Microsoft OIDC is the direct login protocol, or that Akamai is proven from this evidence.

For the university security club, the practical conclusion is to preserve this as an archival change-history study, not an active target inventory. The highest-value future artifact would be an official migration or architecture document that connects the two hostnames and explains identity integration. Until such a document appears, the report should cite exact timestamps and replay bodies, keep 404 and redirect observations separate, and label every architectural bridge as an inference.

## References

1. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=mujslcm.jaipur.manipal.edu/*&from=2025&output=json&filter=statuscode:200&collapse=urlkey
2. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=slcm.manipal.edu/*&from=2017&output=json&filter=statuscode:200&collapse=urlkey
3. [
	MU SLcM
](https://web.archive.org/web/20170714034235id_/http://slcm.manipal.edu:80/loginForm.aspx)
4. [
	MU SLcM
](https://web.archive.org/web/20201118060511id_/https%3A//slcm.manipal.edu/)
5. [
	MU SLcM
](https://web.archive.org/web/20170813123113id_/http://slcm.manipal.edu:80/ParentChangePassword.aspx)
6. *Manipal University*. https://web.archive.org/web/20250527044058id_/https%3A//mujslcm.jaipur.manipal.edu/
7. [
	MU SLcM
](https://web.archive.org/web/20170720030733id_/http://slcm.manipal.edu:80/StudentChangePassword.aspx)
8. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
9. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=slcm.manipal.edu/*&from=2017&output=json&filter=statuscode:3..&collapse=urlkey
10. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=mujslcm.jaipur.manipal.edu/*&from=2025&output=json&filter=statuscode:3..&collapse=urlkey
11. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=slcm.manipal.edu/*&from=2017&output=json&filter=statuscode:404&filter=mimetype:text/html&collapse=urlkey
12. *Using the Wayback Machine – Internet Archive Help Center*. http://help.archive.org/help/using-the-wayback-machine
13. *Frequently Asked Questions and Contacts for SLCM Registration*. https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf
14. *http://mujslcm.jaipur.manipal.edu/*. http://mujslcm.jaipur.manipal.edu/
15. *crt.sh*. http://crt.sh/?output=json&q=mujslcm.jaipur.manipal.edu
16. *Student Portal Login- MAHE (Manipal Academy Of Higher ...*. https://www.manipal.edu/mu/academics/student-portal.html
17. *MU SLcM*. https://slcm.manipal.edu/
18. *http://api.hackertarget.com/httpheaders?q=https://mujslcm.jaipur.manipal.edu/*. http://api.hackertarget.com/httpheaders?q=https://mujslcm.jaipur.manipal.edu/
19. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=slcm.manipal.edu/*&from=2017&output=json&filter=statuscode:200&filter=urlkey:.*(login|password).*&collapse=urlkey
20. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=slcm.manipal.edu/Scripts/*&from=2017&output=json&filter=statuscode:200&collapse=urlkey
21. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=mujslcm.jaipur.manipal.edu/*&from=2025&output=json&filter=statuscode:200&filter=mimetype:text/html&collapse=urlkey
22. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=slcm.manipal.edu/*&from=2017&output=json&filter=statuscode:3..&filter=urlkey:.*(academic|dashboard|attendance|timetable|result|grade|registration|course|login|parent|student).*&collapse=urlkey
23. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=slcm.manipal.edu/*&from=2017&output=json&filter=statuscode:200&filter=mimetype:text/html&collapse=urlkey
24. * 404 Error Page*. https://web.archive.org/web/20220330054426id_/https://slcm.manipal.edu/WebForm1.aspx
25. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=mujslcm.jaipur.manipal.edu/*&from=2025&output=json&filter=statuscode:200&filter=mimetype:text/css&collapse=urlkey
26. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=mujslcm.jaipur.manipal.edu/*&from=2025&output=json&filter=statuscode:200&filter=mimetype:application/javascript&collapse=urlkey
27. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=slcm.manipal.edu/assets/*&from=2017&output=json&filter=statuscode:200&collapse=urlkey
28. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=mujslcm.jaipur.manipal.edu/*&from=2025&output=json&filter=statuscode:404&filter=mimetype:text/html&collapse=urlkey
29. *Openid Configuration*. http://login.microsoftonline.com/muj.manipal.edu/.well-known/openid-configuration
