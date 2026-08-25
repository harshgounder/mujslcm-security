# Public Manipal SLCM Code Exposure and Defensive Priorities

## Executive Summary

- **Public Automation Ecosystem**: At least four public repositories and one npm package automate Manipal SLCM login, attendance, marks, profile, grade, or timetable workflows. The implementations range from Selenium and CasperJS browser automation to Flask and Express wrappers [5][3][25][22][59] -> Manipal should treat portal markup, form fields, and login flows as public knowledge rather than relying on obscurity.
- **Credential Handling Risk**: Historical student-built APIs accept SLCM usernames and passwords as request parameters, and the archived Express project supports GET as well as POST handlers for credential-bearing operations [27][26][29][28] -> Deprecate any analogous official pattern, prohibit credentials in URLs, and monitor logs and referrers for accidental exposure.
- **No Verified Live Credential Leak**: The reviewed default branches expose credential variable names, schemas, and persistence behavior, but no verified, usable SLCM password, private key, database connection string, or bearer token was found. The `.env.example` file contains placeholders rather than values [19], while the Flask documentation describes a credential-bearing request schema without publishing a working account [25] -> Treat this as a design and attack-surface disclosure, not evidence that a valid student account is presently compromised.
- **Configuration Secrets Need Review**: A public Flutter repository contains a Firebase client configuration, and a separate MUJ-themed Django prototype publishes a Django `SECRET_KEY` with `DEBUG=True`; sensitive values are intentionally redacted from this report [46][50] -> Determine ownership, rotate server-side secrets where applicable, restrict Firebase through security rules and application controls, and remove secret-bearing development settings from public history.
- **Session Model Is Visible**: The Flutter client obtains request-verification material and cookies, combines session cookies, supports a parent OTP flow, and persists login-related values; the older browser automations instead rely on the authenticated browser session [54][62][20] -> Review cookie flags, CSRF validation, OTP rate limits, session rotation, credential storage, and server-side authorization independently of the client.
- **Extensions Are Lower Exposure Than APIs**: `SlcmPlus` and the feedback-form filler primarily manipulate the already loaded portal DOM, unlike API wrappers that receive credentials and initiate login themselves [2][4][15] -> Prioritize credential-receiving wrappers and mobile-session code above local-only presentation extensions, while still reviewing extension permissions and distribution.
- **Historical Portal Snapshot Exposes Structure And Data**: A GitHub Pages repository preserves an authenticated-looking SLCM HTML snapshot, including ASP.NET state fields, route names, and personal or academic content that is not reproduced here [42] -> Request removal or redaction of personal data and assume historical route taxonomy is permanently public.
- **Certificate Transparency Expands The Inventory**: Public certificate-transparency data yielded **103 distinct `manipal.edu` hostnames**, including **11 Jaipur-scoped names** and seven names explicitly labeled `dev`, `uat`, or `preprod` [44][41] -> Inventory owners and lifecycle status, but do not equate a certificate-log entry with a currently reachable or vulnerable system.
- **Leak-Site Results Require Careful Interpretation**: The public LeakIX service view listed 117 indexed service records and several `dev-*` names, but the leak-scoped page did not expose a usable leak result in this review [55][48] -> Validate exposures internally; do not label an indexed host as breached without record-level evidence.

## Scope, Safety, And Evidence Standard

This report covers material that was publicly retrievable from ordinary repository pages, package metadata, public documentation, certificate-transparency records, and indexed service listings. It did not attempt to sign into SLCM, submit credentials, bypass access controls, test the listed hosts, replay tokens, enumerate student accounts, or retrieve private data. Secret values and personal records encountered in public source files are deliberately omitted or shown only as `[REDACTED]`.

The user requested explicit chain-of-thought reasoning. Private hidden reasoning is not provided. Instead, this report supplies a reproducible evidence trail: exact repository and file URLs, the public behavior visible in each artifact, clear distinctions between observation and inference, negative-result limitations, and a risk-ranked defensive synthesis.

The search distinguished four questions that are often conflated:

1. Is an artifact publicly accessible?
2. Does it disclose architecture or credential-handling behavior?
3. Does it contain a secret-looking value?
4. Is that value verified as live, privileged, and usable?

Only the first two are strongly established across many artifacts. A Firebase client key and a Django secret value are publicly present, but they are redacted here and their current operational significance was not tested [46][50]. No reviewed source established a live SLCM account credential. Likewise, certificate transparency establishes certificate issuance or logging, not current DNS resolution, service availability, or vulnerability.

## Public Artifact Inventory

| Artifact type | Project and exact public URL | What it exposes | Credential or secret assessment | Status signal |
|---|---|---|---|---|
| Selenium and OCR scraper | `https://github.com/sankalp2004/SLCM-is-Dumb` | Automated SLCM login, CAPTCHA handling, grade extraction, and CGPA calculation [5] | Loads `SLCM_USERNAME` and `SLCM_PASSWORD` from environment variables; no values in the template [18][19] | Public repository; portal selectors may be historical |
| Scraper configuration | `https://github.com/sankalp2004/SLCM-is-Dumb/blob/master/config.py` | Exact login and grade-sheet locations: `loginForm.aspx` and `GradeSheet.aspx` [18] | Variable names only | Public source file |
| Scraper implementation | `https://github.com/sankalp2004/SLCM-is-Dumb/blob/master/scraper.py` | Browser-form login, CAPTCHA processing, navigation, and grade parsing [20] | Browser session is used; no exported JWT or hard-coded password observed | Public source file |
| Student technical note | `https://github.com/sankalp2004/SLCM-is-Dumb/blob/master/HowThiswWorks.md` | Documents `studenthomepage.aspx`, `Academics.aspx`, and `GradeSheet.aspx`, plus environment-variable setup [63] | No credential values | Public documentation |
| Express and Puppeteer API | `https://github.com/canaryGrapher/slcmAPI` | REST-style access to marks, attendance, profile, and credential validation [3] | Receives portal credentials; no separate bearer-token design found | Deprecated because of CAPTCHA and archived on October 17, 2024 [3][7] |
| Express server | `https://github.com/canaryGrapher/slcmAPI/blob/master/server.js` | Registers `/getscores`, `/getattendance`, `/getprofile`, and `/validateuser` [64] | No JWT or authentication middleware is visible in the cited server registration | Archived repository |
| Flask API wrapper | `https://github.com/tejaskash/slcm-api` | Historical `POST /api/v1/get` interface for `ATTENDANCE`, `MARKS`, or `ALL` [25] | Request schema embeds the user's SLCM credentials; no live account published | Created in 2020; deployment URL should be treated as historical |
| Older REST scraper | `https://github.com/utk3012/SLCM` | REST API scraper and link to an Android application [22] | Authentication details are under-documented | Old repository created in 2018 [22] |
| npm attendance tool | `https://www.npmjs.com/package/yemit` | CasperJS command-line tool that authenticates to SLCM, navigates the portal, and retrieves attendance [59] | No secret value found in package metadata | Version 0.1.5, published about eight years before the indexed snapshot [59] |
| Attendance browser extension | `https://github.com/Tejas-Narula/SlcmPlus` | Attendance analytics, classes missable at a 75 percent threshold, marks, and GPA presentation [2] | DOM-oriented content script; no credential store identified | Public Chrome-extension source |
| Feedback browser extension | `https://github.com/AddisionS/slcm-feedback-form-filler` | Automates responses to SLCM feedback forms and can optionally submit them [4] | No hard-coded credentials found | Public Chrome and Firefox source |
| Flutter mobile client | `https://github.com/DK10WS/SLCM_APP` | Attendance, grades, timetable, student login, parent login, OTP, and session handling [38][62] | Public Firebase client configuration and local credential/session persistence patterns; values redacted [46][54][62] | Public source; operational ownership not independently verified |
| MUJ Django prototype | `https://github.com/Anushkakumar10/muj_slcm` | Custom-user registration, login, profile, and password-change code [52][61] | Publishes a Django `SECRET_KEY` and `DEBUG=True`; value redacted [50] | Appears to be a one-commit prototype, not established as an official MUJ service |
| Static portal snapshot | `https://github.com/slcm-manipal/slcm-manipal.github.io` | Historical authenticated-looking HTML, ASP.NET state fields, route taxonomy, and personal or academic content [42] | No login password found, but the snapshot contains privacy-sensitive content | Created in 2018; historical snapshot |
| Postman workspace | `https://www.postman.com/harshalsangole/manipal-api-collection/overview` | Public title `Manipal API Collection` and owner metadata [23] | No public request bodies, variables, authorization scheme, or secrets were visible from the overview | Scope unverified |

The inventory shows a mature unofficial automation ecosystem, but not a single unified or official API. Most projects adapt the web portal by driving a browser or parsing rendered HTML. That distinction matters: such wrappers inherit the portal's authentication and authorization behavior rather than defining an independent trust boundary.

## Student APIs And Automation Reveal A Form-Based Architecture

### `SLCM-is-Dumb`: environment variables, Selenium, OCR, and grade routes

`SLCM-is-Dumb` is the clearest end-to-end student automation case. Its public configuration identifies the classic SLCM login and grade-sheet paths and reads the username and password from environment variables [18]. The accompanying `.env.example` publishes only the expected variable names, while the README cautions against committing the real `.env` file [19][5]. This is appropriate secret separation at the repository level.

The scraper then drives a browser through login, CAPTCHA handling, and grade extraction [20]. Its technical note names additional post-login paths, including the student home, academics page, and grade sheet [63]. The artifact therefore exposes page structure and workflow, but it does not establish a backend JSON API, JWT, API key, or reusable session token. The security implication is not that Selenium is itself a breach. It is that client-side route secrecy and brittle CAPTCHA assumptions cannot protect server-side student records.

### `slcmAPI`: credentials become API parameters

The archived `canaryGrapher/slcmAPI` project converts portal actions into an Express interface for scores, attendance, profile data, and credential validation [3]. `server.js` registers four corresponding routes [64]. Each handler receives a username and password and then logs into the portal using Puppeteer. The attendance route supports GET and POST and targets the SLCM login and academics pages [27]; the marks route accepts username, password, semester, and validation-related inputs [26]. Profile and validation handlers follow the same model [29][28].

The most important failure pattern is the historical support for credentials in a GET-style request. URLs can be retained by browser history, reverse proxies, analytics systems, application logs, and referrer flows. This does not prove any credential was leaked, but it demonstrates an unsafe interface pattern. The repository's deprecation because of CAPTCHA and its later archive status also show that anti-automation changes can break wrappers without repairing underlying credential-handling risks [3][7].

### `slcm-api`, `SLCM`, and `yemit`: three generations of wrappers

The Flask-based `tejaskash/slcm-api` describes a single historical POST endpoint that takes an operation type such as attendance, marks, or both, together with SLCM credentials [25]. Exact public files include:

- `https://github.com/tejaskash/slcm-api/blob/master/slcm.py`
- `https://github.com/tejaskash/slcm-api/blob/master/slcm_scrape.py`
- `https://github.com/tejaskash/slcm-api/blob/master/SLCM.ini`

The older `utk3012/SLCM` repository identifies itself as a REST API scraper and links an Android client, but its public documentation is too sparse to support conclusions about headers, tokens, or current endpoints [22]. `yemit`, meanwhile, packages the same basic behavior as a command-line attendance tool using CasperJS and a headless browser [59]. Its registry metadata lists `index.js`, `run.js`, and `run.sh`, and identifies `slcm.manipal.edu` as the target host [60][59].

Together, these artifacts demonstrate repeated community demand for attendance and marks automation. They also show a recurring architectural mechanism: the unofficial program receives the student's primary credentials, creates a portal session, and scrapes HTML. A safer official alternative would use narrowly scoped, revocable authorization, explicit rate limits, and stable response schemas so that a timetable or attendance client never needs the student's reusable portal password.

## Browser Extensions And Mobile Clients Shift The Risk Boundary

### Local DOM extensions

`SlcmPlus` adds attendance analytics, estimates how many classes can be missed while remaining at a 75 percent threshold, and presents marks and GPA-related information [2]. Its public content script recognizes the attendance page and operates on portal content already present in the browser [15]. The feedback-form filler similarly automates form responses and supports optional submission [4]. Its Chrome source tree contains a content script, manifest, popup code, and styles at `https://github.com/AddisionS/slcm-feedback-form-filler/tree/main/chrome` [9].

These extensions differ materially from hosted credential proxies. A local content script can still read or alter sensitive page content according to its permissions, but it need not receive a password on a third-party server. Defensive review should focus on manifest permissions, update provenance, outbound network calls, and whether submission actions require an explicit user confirmation. Based on the reviewed files, neither extension yielded a verified credential or API key.

### `SLCM_APP`: cookies, request-verification material, OTP, and persistence

`DK10WS/SLCM_APP`, branded in its README as `SLCM SWITCH`, is the richest mobile-client artifact. The repository advertises attendance, grade, and timetable functions and uses Flutter with a FastAPI-related architecture description [38]. Its login implementation obtains request-verification material and cookies, submits student or parent login data, handles a parent OTP path, combines returned cookies, and saves login-related values for later use [62]. `session_manager.dart` explicitly maintains a nullable session-cookie value [54].

This is evidence of a cookie and anti-forgery-token session model in that client, not evidence of JWT. No reviewed artifact showed a Manipal bearer-token format or an `Authorization: Bearer` requirement. The code's persistence of username and password under runtime storage keys deserves review even though those values are not hard-coded in the repository. Mobile platforms require secrets to be placed in protected storage, minimized, and cleared on logout; ideally, a client should retain a revocable session credential instead of a reusable institutional password.

The Android project also publishes `google-services.json` at `https://github.com/DK10WS/SLCM_APP/blob/main/android/app/google-services.json` [46]. Firebase client API keys are often identifiers rather than standalone authorization secrets, so the mere presence of this file does not prove unauthorized database access. The proper test is defensive and server-side: confirm restrictive Realtime Database, Storage, Authentication, and App Check policies; verify that possessing the public client configuration grants no data access beyond what an unauthenticated client is intended to have.

## Public Configuration, Secret-Looking Values, And Privacy Material

| Finding | Exact file URL | Public evidence | What is not established | Defensive priority |
|---|---|---|---|---|
| Firebase client configuration | `https://github.com/DK10WS/SLCM_APP/blob/main/android/app/google-services.json` | Project identifiers, service hosts, and a client API key are present [46] | No test established unauthorized read/write access | Validate rules and ownership; rotate only if policy or ownership requires it |
| Django secret and debug mode | `https://github.com/Anushkakumar10/muj_slcm/blob/main/muj_slcm/muj_slcm/settings.py` | A literal Django `SECRET_KEY` and `DEBUG=True` are public [50] | Repository is not proven to be an official or deployed MUJ system | Remove from history, rotate if deployed, disable debug, separate development settings |
| Environment template | `https://github.com/sankalp2004/SLCM-is-Dumb/blob/master/.env.example` | Names `SLCM_USERNAME` and `SLCM_PASSWORD` without values [19] | No password leak | Keep placeholders only and retain secret-scanning controls |
| Login and password-handling prototype | `https://github.com/Anushkakumar10/muj_slcm/blob/main/muj_slcm/muj_slcm_app/views.py` | Email/password handling and debug-style variable printing are visible [52] | No real user's password is published in the cited source | Remove sensitive logging and use framework authentication primitives consistently |
| Password-change logic | `https://github.com/Anushkakumar10/muj_slcm/blob/main/muj_slcm/muj_slcm_app/student_views.py` | Uses password-setting logic for a student profile [61] | No default password is identified | Review authorization, reauthentication, CSRF, and audit logging if deployed |
| Historical portal snapshot | `https://github.com/slcm-manipal/slcm-manipal.github.io/blob/master/index.html` | Routes, ASP.NET state fields, and embedded personal or academic content [42] | No working portal credential | Remove or redact privacy-sensitive history and invalidate any still-relevant identifiers |

The distinction between a client configuration and an authorization secret is crucial. The Flutter Firebase key should not be described as a confirmed master credential. Conversely, the Django `SECRET_KEY` is intended to be server-side. If that prototype was ever deployed with the published value, rotation is warranted. Since deployment was not verified, the correct verdict is "public secret-bearing development configuration with unknown operational impact," not "Manipal production compromise."

The static `slcm-manipal.github.io` snapshot is a different class of exposure. Its HTML preserves route names such as student profile, academics, fee details, grade sheet, timetable, document, event, and faculty pages, along with ASP.NET mechanisms such as `__doPostBack`, `__VIEWSTATEGENERATOR`, and `__EVENTVALIDATION` [42]. The snapshot also contains personal or academic information, which is intentionally not repeated here [42]. Even when stale, such material can facilitate targeted phishing or privacy harm. Repository-history redaction and data-subject notification should be considered according to institutional policy and applicable law.

## API And Authentication Evidence Matrix

| Public component | Routes or operation | Inputs visible in code or documentation | State and token evidence | Assessment |
|---|---|---|---|---|
| `canaryGrapher/slcmAPI` | `/getattendance` | Username, password, and validation-related flag through GET or POST [27] | Puppeteer browser-form session; no JWT or bearer header evidenced | Historical high-risk credential-proxy design |
| `canaryGrapher/slcmAPI` | `/getscores` | Username, password, semester, validation-related flag [26] | Browser login and portal navigation | Credentials in GET-compatible handler are the principal concern |
| `canaryGrapher/slcmAPI` | `/getprofile` | Username and password [29] | Browser login to the student-profile page | Profile data is exposed to whatever caller possesses the credentials |
| `canaryGrapher/slcmAPI` | `/validateuser` | Username and password [28] | Form credential validation | Creates an avoidable credential-verification oracle if hosted without controls |
| `tejaskash/slcm-api` | Historical `POST /api/v1/get` | Credentials plus `ATTENDANCE`, `MARKS`, or `ALL` [25] | No separate authorization scheme documented | Better than GET for transport placement, but still receives reusable credentials |
| `SLCM-is-Dumb` | `loginForm.aspx`, `Academics.aspx`, `GradeSheet.aspx` | Environment-provided username and password [18][63] | Selenium-managed cookies; CAPTCHA and HTML parsing [20] | Local automation, not a backend API specification |
| `SLCM_APP` | Student and parent login flows | User-entered credentials, request-verification material, parent OTP [62] | Combined cookies and stored session-cookie value [54][62] | Strongest public evidence of cookie, CSRF-like token, and OTP handling |
| Static SLCM snapshot | ASP.NET page paths | Authenticated page and postback state | `__doPostBack`, view-state generator, and event validation [42] | Historical web-form architecture, not proof of a current API |
| `SlcmPlus` | Attendance-page content script | Existing page DOM | No independent login token shown [15] | Lower risk than credential-hosting wrappers if permissions remain narrow |

No public OpenAPI or Swagger specification was verified. The Postman workspace confirms only a public collection title and owner; its overview did not expose usable request definitions, environments, authorization variables, or endpoints [23]. The most complete student-built documentation remains the READMEs and source files in the repositories above.

No reviewed code established JWT usage. The supported conclusion is narrower: browser-managed cookies appear in Selenium, Puppeteer, and CasperJS flows; the Flutter client explicitly handles request-verification material, cookies, a session-cookie value, and an OTP flow [20][54][62]. Headers or token formats not present in the cited code should remain classified as unknown.

## GitLab, npm, Postman, Gists, Paste Sites, And Leak Indexes

### Package and repository indexes

A direct npm registry search for `mujslcm` returned zero package results [45]. A broader SLCM search found `yemit`, whose package and GitHub repository are public and relevant [53][59]. The exact sources are:

- `https://www.npmjs.com/package/yemit`
- `https://registry.npmjs.org/yemit`
- `https://github.com/rsarky/yemit`

The public GitLab project API returned empty arrays for `mujslcm` and `manipal slcm` searches. These are index-level negative results, not proof that no unindexed, renamed, deleted, forked, or private GitLab project exists. A previously indexed GitHub candidate named `madhav-manchanda/SlcmAndLms-aggregator` returned HTTP 404 through the current repository API [56], so it is not counted as a presently accessible artifact.

### Paste and leak sites

No relevant, verifiable Pastebin or public Gist containing SLCM credentials was established during this review. Search-engine absence is weak evidence because pastes can be unindexed, deleted, access-limited, or too new to index. Accordingly, the finding is "no verified public hit found," not "no paste exists."

The LeakIX distinction is particularly important. The leak-scoped query for `manipal.edu` reached a login-oriented result rather than exposing a public leak record [55]. The service-scoped view reported 117 indexed service records and included names such as `dev-api.manipal.edu`, `dev-techtatva.manipal.edu`, `dev-superadmin-techtatva.manipal.edu`, `dev-register-techtatva.manipal.edu`, and `dev-judge-techtatva.manipal.edu` [48]. A service index is not a credential leak and is not evidence of vulnerability. These names are defensive inventory leads only.

No verified RaonData record, default institutional password, or tutorial containing a working account credential was found. It would be irresponsible to infer a default password from student-facing instructions, naming conventions, or screenshots. Any discovered password should be reported privately to the institution and platform, not reproduced.

## Certificate Transparency: 103 Names And Seven Environment Labels

Direct retrieval of crt.sh results did not succeed in this research environment [24][21]. The enumeration therefore uses Cert Spotter's public certificate-transparency JSON endpoint:

`https://api.certspotter.com/v1/issuances?domain=manipal.edu&include_subdomains=true&expand=dns_names`

The data yielded **103 distinct names** [44]. CT data can include expired, superseded, wildcard-covered, or no-longer-resolving hosts. The table is an inventory of logged names, not a list of live systems.

| Hostname | Hostname | Hostname | Hostname |
|---|---|---|---|
| admin-convocation.manipal.edu | admin-guesthouse.manipal.edu | admin-summer.manipal.edu | admissions.jaipur.manipal.edu |
| aiassistant.manipal.edu | alumni.manipal.edu | ams-api.manipal.edu | ams-faculty.manipal.edu |
| ams-superadmin.manipal.edu | ams-upload.manipal.edu | ams.manipal.edu | api-convocation.manipal.edu |
| api-summer.manipal.edu | apply.aua.manipal.edu | bioincubator.manipal.edu | careernext.manipal.edu |
| cetd.manipal.edu | cia.manipal.edu | click.mailer.manipal.edu | click.studentinfo.manipal.edu |
| cloud.mailer.manipal.edu | cloud.studentinfo.manipal.edu | compliance.manipal.edu | content-preprod.manipal.edu |
| content-uat.manipal.edu | convocation.manipal.edu | counseling.manipal.edu | crm.manipal.edu |
| dev-api.manipal.edu | dev-crm.manipal.edu | dev-payment.manipal.edu | dosmplalumni.manipal.edu |
| evbab.manipal.edu | guesthouse-api.manipal.edu | guesthouse.manipal.edu | helpdesk.jaipur.manipal.edu |
| ima.manipal.edu | image.mailer.manipal.edu | image.studentinfo.manipal.edu | jaipur.manipal.edu |
| kmchslibportal.manipal.edu | kmcmplalumni.manipal.edu | koha.manipal.edu | lighthouse.manipal.edu |
| lms.manipal.edu | mahealumni.manipal.edu | maheblrlibportal.manipal.edu | mahelibportal.manipal.edu |
| maheonlinealumni.manipal.edu | manam.manipal.edu | manipal.edu | manipalmatters.manipal.edu |
| mapkmc.manipal.edu | mcodsmlralumni.manipal.edu | micmplalumni.manipal.edu | mishaalumni.manipal.edu |
| mitmplalumni.manipal.edu | mitmpllibportal.manipal.edu | msonmplalumni.manipal.edu | muj.slcm.jaipur.manipal.edu |
| mujerp.jaipur.manipal.edu | mujlms.manipal.edu | mujone.jaipur.manipal.edu | mujslcm.jaipur.manipal.edu |
| nano.manipal.edu | payment.manipal.edu | preprod.manipal.edu | registration-summer.manipal.edu |
| researcher.manipal.edu | rewilding.manipal.edu | rms.jaipur.manipal.edu | rrc-admin.manipal.edu |
| servicedesk.manipal.edu | smartachievers.manipal.edu | social.manipal.edu | stsfor.manipal.edu |
| summer.manipal.edu | superadmin-convocation.manipal.edu | superadmin-guesthouse.manipal.edu | textract-api.manipal.edu |
| textract.manipal.edu | uat.manipal.edu | view.mailer.manipal.edu | view.studentinfo.manipal.edu |
| www.alumni.manipal.edu | www.dosmplalumni.manipal.edu | www.ima.manipal.edu | www.jaipur.manipal.edu |
| www.kmcmplalumni.manipal.edu | www.mahealumni.manipal.edu | www.maheonlinealumni.manipal.edu | www.manipal.edu |
| www.mcodsmlralumni.manipal.edu | www.micmplalumni.manipal.edu | www.mishaalumni.manipal.edu | www.mitmplalumni.manipal.edu |
| www.msonmplalumni.manipal.edu | www.mujone.jaipur.manipal.edu | www.rewilding.manipal.edu | www.rms.jaipur.manipal.edu |
| www.social.manipal.edu | youngachievers.manipal.edu | youngpioneers.manipal.edu |  |

### Jaipur-scoped CT names

The CT inventory contains **11 names** under `jaipur.manipal.edu` [41]:

| Category | Exact CT name | Environment label? | Defensive interpretation |
|---|---|---|---|
| Base | `jaipur.manipal.edu` | No | Jaipur web namespace |
| Admissions | `admissions.jaipur.manipal.edu` | No | Public-facing function suggested by name only |
| Help desk | `helpdesk.jaipur.manipal.edu` | No | Support function suggested by name only |
| SLCM | `muj.slcm.jaipur.manipal.edu` | No | Alternate MUJ SLCM naming pattern |
| SLCM | `mujslcm.jaipur.manipal.edu` | No | Domain named in the research question |
| ERP | `mujerp.jaipur.manipal.edu` | No | ERP-related label, not proof of content |
| MUJ One | `mujone.jaipur.manipal.edu` | No | Application label |
| RMS | `rms.jaipur.manipal.edu` | No | Application label |
| WWW alias | `www.jaipur.manipal.edu` | No | Web alias |
| WWW alias | `www.mujone.jaipur.manipal.edu` | No | Application alias |
| WWW alias | `www.rms.jaipur.manipal.edu` | No | Application alias |

### Explicit development, UAT, and preproduction labels

| Label class | CT hostname | Why flagged | What CT does not prove |
|---|---|---|---|
| Preproduction | `content-preprod.manipal.edu` | Literal `preprod` label | Current resolution, reachability, or weaker controls |
| UAT | `content-uat.manipal.edu` | Literal `uat` label | Presence of test data or public access |
| Development | `dev-api.manipal.edu` | Literal `dev` and `api` labels | An exposed or undocumented API |
| Development | `dev-crm.manipal.edu` | Literal `dev` label | Active CRM deployment |
| Development | `dev-payment.manipal.edu` | Literal `dev` and `payment` labels | Payment-system exposure |
| Preproduction | `preprod.manipal.edu` | Literal `preprod` label | Any specific hosted application |
| UAT | `uat.manipal.edu` | Literal `uat` label | Any vulnerability or live data |

No CT hostname in this 103-name result used the literal requested labels `test`, `staging`, `qa`, `old`, `backup`, or `new` [44]. Several names contain `admin`, `superadmin`, `api`, or `upload`; those role-oriented labels may justify ownership review, but their names alone do not establish an exposed administrative interface.

## Risk Prioritization And Defensive Actions

| Priority | Evidence | Principal risk | Recommended defensive action |
|---|---|---|---|
| 1 - Immediate ownership check | Public Django secret and debug setting [50] | If deployed, server-side signing integrity and debug disclosure | Identify owner, remove from history, rotate the secret if ever deployed, disable production debug |
| 1 - Immediate privacy review | Static portal snapshot with personal or academic content [42] | Student privacy, phishing enablement, persistent repository history | Preserve evidence internally, request platform redaction, assess notification obligations |
| 1 - Session and credential review | Mobile code persists login-related values and combines cookies [54][62] | Credential theft from device storage or improper logout/session lifecycle | Use protected storage, minimize password retention, rotate sessions after login and OTP, clear on logout |
| 2 - API design | Historical wrappers accept reusable credentials, including GET-compatible handlers [27][26] | Credentials in URLs, logs, proxies, and third-party services | Offer scoped authorization; prohibit passwords in query strings; add monitoring and rate limits |
| 2 - Firebase controls | Public client configuration [46] | Misconfigured database or storage rules, not the client key by itself | Test rules internally, enforce least privilege, App Check where suitable, and alert on anomalous access |
| 2 - Portal authorization | Scrapers publicly document routes and form flows [18][63] | Endpoint discovery and object-level authorization mistakes | Enforce authorization on every request; do not rely on hidden navigation or route obscurity |
| 3 - Extension governance | Extensions alter attendance and feedback pages [2][4] | Overbroad permissions, compromised updates, unintended submission | Publish extension guidance, review permissions, use explicit confirmation for writes |
| 3 - Asset lifecycle | CT includes dev, UAT, preprod, admin, API, and upload labels [44] | Forgotten certificates, stale DNS, inconsistent controls | Map every name to owner, data classification, expiry, DNS status, and retirement decision |
| 3 - Third-party code monitoring | Multiple old wrappers and an archived API remain public [3][7][59] | Stale examples continue unsafe patterns | Maintain continuous public-code monitoring and a researcher disclosure channel |

A practical response should begin with ownership, not takedown demands. Several repositories are student projects, historical experiments, or prototypes and may not be controlled by Manipal. The institution should first map each project to affected systems, determine whether exposed configuration belongs to an operational environment, and contact maintainers with precise file-level evidence. Blanket removal requests can destroy useful evidence or alienate good-faith developers without reducing the underlying server-side risk.

Second, Manipal should assume that all routes, field names, and form behaviors in public code are known to adversaries. Server-side controls should include per-object authorization, secure and `HttpOnly` cookies where applicable, CSRF enforcement, session rotation, robust logout, OTP attempt controls, anomaly detection, and credential-stuffing defenses. CAPTCHA can slow automation but should not be treated as an authorization boundary.

Third, the institution should provide a supported integration path. The repeated appearance of attendance, grade, timetable, and profile scrapers is a signal of unmet demand. A documented, scoped, rate-limited API can reduce the incentive for users to give primary passwords to unofficial wrappers. Authorization grants should be narrow by function and time, revocable, and auditable.

## Synthesis

The artifacts differ across mechanism, scope, evidence strength, and time horizon. Selenium, Puppeteer, and CasperJS projects emulate a browser. Their strength is that they document real page flows; their weakness is brittleness and dependence on reusable credentials. The Flask and Express wrappers add a network API in front of those flows. That makes automation convenient but expands the trust boundary because the wrapper can receive the user's password and return sensitive records.

Browser extensions take the opposite approach. `SlcmPlus` and the feedback filler operate inside a browser that already has portal content [2][4]. They can still carry meaningful permission and supply-chain risk, but the reviewed design does not require a third-party hosted service to authenticate on the user's behalf. The Flutter application falls between these models: it implements login and session logic as a client, explicitly handling cookies, request-verification material, OTP, and persistence [54][62]. Its main defensive concern is therefore client storage and session lifecycle rather than an undocumented JWT.

The configuration findings also have different meanings. The `.env.example` demonstrates good separation because it publishes variable names without values [19]. The Firebase configuration is normally shipped to clients, so its security depends on backend rules rather than key secrecy [46]. The Django `SECRET_KEY`, by contrast, is intended to remain server-side, but the repository has not been shown to be an official or deployed Manipal service [50]. Treating all three as equivalent "API key leaks" would be analytically wrong.

The historical HTML snapshot and CT inventory provide broad reconnaissance value but different evidence. The snapshot directly preserves page structure, state fields, and privacy-sensitive content [42]. CT proves that names appeared in public certificate logs [44]. It does not prove that `dev-payment.manipal.edu`, `uat.manipal.edu`, or any other listed host is online or vulnerable. LeakIX's service index similarly supports asset discovery but not a breach conclusion [48].

Across all categories, the central tension is clear: no verified live SLCM credential was found, yet substantial technical intelligence is public. The ecosystem discloses portal routes, credential schemas, scraping selectors, API-shaped wrappers, session-cookie behavior, OTP branching, application configuration, and a wide certificate-derived hostname inventory. That is enough to justify remediation, but not enough to claim a production compromise.

The recommended strategic response is therefore layered. Remove or rotate genuinely secret-bearing configuration after ownership verification. Redact privacy-sensitive snapshots. Harden session, CSRF, OTP, and object-level authorization. Inventory CT-derived assets. Finally, reduce password-sharing incentives by offering supported, scoped access for attendance, timetable, and grade use cases.

## VERDICT

**Verdict: Material public technical exposure exists, but no verified live SLCM credential compromise was established.**

Public GitHub and npm artifacts document or implement Manipal SLCM login automation, attendance and marks extraction, profile access, grade calculation, timetable functions, feedback automation, and mobile session management [5][3][25][38][59]. Exact portal routes and form-based workflows are public. Historical API wrappers accept reusable usernames and passwords, sometimes through GET-compatible handlers [27][26]. Public source also contains a Firebase client configuration, a secret-bearing Django development configuration, and a historical portal snapshot containing privacy-sensitive material [46][50][42].

No reviewed public source established a currently valid student password, default password, private key, database connection string, JWT, bearer token, or production Postman secret. No public Swagger or OpenAPI specification was verified. Negative findings for GitLab, Pastebin, Gists, RaonData, and leak-scoped indexes are **moderate-confidence search results**, not exhaustive proof of absence.

**Confidence assessment:**

- **High confidence** in the existence, URLs, and described behavior of the cited GitHub, npm, Postman-overview, CT, and LeakIX-service artifacts.
- **High confidence** that the cited source files expose credential-handling patterns, routes, cookie or request-verification behavior, and secret-bearing configuration values, with values redacted here.
- **Medium confidence** that no live credential or additional public specification exists, because deleted commits, unindexed pastes, private repositories, renamed projects, and inaccessible history cannot be ruled out.
- **Low confidence** about the current operational status or vulnerability of CT and service-index hostnames, because no active probing or authentication was performed.

## References

1. *slcm-manipal · GitHub*. https://github.com/slcm-manipal
2. *GitHub - Tejas-Narula/SlcmPlus: A Chrome extension for MUJ students that enhances the SLCM experience by providing attendance analytics and automatic marks calculation directly within the portal. · GitHub*. https://github.com/Tejas-Narula/SlcmPlus
3. *GitHub - canaryGrapher/slcmAPI: The API for SLcM, Manipal. Get your marks, your attendance and your profile details · GitHub*. https://github.com/canaryGrapher/slcmAPI
4. *GitHub - AddisionS/slcm-feedback-form-filler: This is a chrome extension that can be used to automate the process of filling feedback form on MUJ's SLCM portal · GitHub*. https://github.com/AddisionS/slcm-feedback-form-filler
5. *GitHub - sankalp2004/SLCM-is-Dumb: This extracts cgpa from https://slcm.manipal.edu/ directly and passes captcha · GitHub*. https://github.com/sankalp2004/SLCM-is-Dumb
6. *slcm-feedback-form-filler/firefox at main · AddisionS/slcm-feedback-form-filler · GitHub*. https://github.com/AddisionS/slcm-feedback-form-filler/tree/main/firefox
7. *slcmAPI/README.md at master · canaryGrapher/slcmAPI · GitHub*. https://github.com/canaryGrapher/slcmAPI/blob/master/README.md
8. *slcmAPI/routes at master · canaryGrapher/slcmAPI · GitHub*. https://github.com/canaryGrapher/slcmAPI/tree/master/routes
9. *slcm-feedback-form-filler/chrome at main · AddisionS/slcm-feedback-form-filler · GitHub*. https://github.com/AddisionS/slcm-feedback-form-filler/tree/main/chrome
10. *404 Not Found*. https://crt.sh/?q=%25.jaipur.manipal.edu&output=json
11. *slcmAPI/package.json at master · canaryGrapher/slcmAPI · GitHub*. https://github.com/canaryGrapher/slcmAPI/blob/master/package.json
12. *GitHub - slcm-manipal/slcm-manipal.github.io: Website for checking grades. · GitHub*. https://github.com/slcm-manipal/slcm-manipal.github.io
13. *SlcmPlus/manifest.json at main · Tejas-Narula/SlcmPlus · GitHub*. https://github.com/Tejas-Narula/SlcmPlus/blob/main/manifest.json
14. *GitHub - Anushkakumar10/muj_slcm · GitHub*. https://github.com/Anushkakumar10/muj_slcm
15. *SlcmPlus/content.js at main · Tejas-Narula/SlcmPlus · GitHub*. https://github.com/Tejas-Narula/SlcmPlus/blob/main/content.js
16. *SLCM-is-Dumb/requirements.txt at master · sankalp2004/SLCM-is-Dumb · GitHub*. https://github.com/sankalp2004/SLCM-is-Dumb/blob/master/requirements.txt
17. *GitHub - DK10WS/SLCM_APP: App Version for MUJ SLCM · GitHub*. https://github.com/DK10WS/SLCM_APP
18. *SLCM-is-Dumb/config.py at master · sankalp2004/SLCM-is-Dumb · GitHub*. https://github.com/sankalp2004/SLCM-is-Dumb/blob/master/config.py
19. *SLCM-is-Dumb/.env.example at master · sankalp2004/SLCM-is-Dumb · GitHub*. https://github.com/sankalp2004/SLCM-is-Dumb/blob/master/.env.example
20. *SLCM-is-Dumb/scraper.py at master · sankalp2004/SLCM-is-Dumb · GitHub*. https://github.com/sankalp2004/SLCM-is-Dumb/blob/master/scraper.py
21. *404 Not Found*. http://crt.sh/?q=%25.jaipur.manipal.edu
22. *GitHub - utk3012/SLCM: Rest API to scrape data from SLCM Manipal portal · GitHub*. https://github.com/utk3012/SLCM
23. *Manipal API Collection | Postman API Network*. https://www.postman.com/harshalsangole/manipal-api-collection/overview
24. *404 Not Found*. https://crt.sh/?q=jaipur.manipal.edu
25. *GitHub - tejaskash/slcm-api: A RESTful API to get attendance and marks data from SLCM Portal at Manipal University, written in Python using Flask. · GitHub*. https://github.com/tejaskash/slcm-api
26. *slcmAPI/routes/getmarks.js at master · canaryGrapher/slcmAPI · GitHub*. https://github.com/canaryGrapher/slcmAPI/blob/master/routes/getmarks.js
27. *slcmAPI/routes/getattendance.js at master · canaryGrapher/slcmAPI · GitHub*. https://github.com/canaryGrapher/slcmAPI/blob/master/routes/getattendance.js
28. *slcmAPI/routes/validateuser.js at master · canaryGrapher/slcmAPI · GitHub*. https://github.com/canaryGrapher/slcmAPI/blob/master/routes/validateuser.js
29. *slcmAPI/routes/getprofile.js at master · canaryGrapher/slcmAPI · GitHub*. https://github.com/canaryGrapher/slcmAPI/blob/master/routes/getprofile.js
30. *SLCM_APP/android/app at main · DK10WS/SLCM_APP · GitHub*. https://github.com/DK10WS/SLCM_APP/tree/main/android/app
31. *slcm-manipal.github.io/GS_files at master · slcm-manipal/slcm-manipal.github.io · GitHub*. https://github.com/slcm-manipal/slcm-manipal.github.io/tree/master/GS_files
32. *muj_slcm/README.md at main · Anushkakumar10/muj_slcm · GitHub*. https://github.com/Anushkakumar10/muj_slcm/blob/main/README.md
33. *slcm-api/SLCM.ini at master · tejaskash/slcm-api · GitHub*. https://github.com/tejaskash/slcm-api/blob/master/SLCM.ini
34. *SLCM_APP/lib at main · DK10WS/SLCM_APP · GitHub*. https://github.com/DK10WS/SLCM_APP/tree/main/lib
35. *muj_slcm/muj_slcm at main · Anushkakumar10/muj_slcm · GitHub*. https://github.com/Anushkakumar10/muj_slcm/tree/main/muj_slcm
36. *slcm-manipal.github.io/MU SLcM_files at master · slcm-manipal/slcm-manipal.github.io · GitHub*. https://github.com/slcm-manipal/slcm-manipal.github.io/tree/master/MU%20SLcM_files
37. *slcm-manipal.github.io/GS.html at master · slcm-manipal/slcm-manipal.github.io · GitHub*. https://github.com/slcm-manipal/slcm-manipal.github.io/blob/master/GS.html
38. *SLCM_APP/README.md at main · DK10WS/SLCM_APP · GitHub*. https://github.com/DK10WS/SLCM_APP/blob/main/README.md
39. *slcm-api/slcm_scrape.py at master · tejaskash/slcm-api · GitHub*. https://github.com/tejaskash/slcm-api/blob/master/slcm_scrape.py
40. *slcm-api/slcm.py at master · tejaskash/slcm-api · GitHub*. https://github.com/tejaskash/slcm-api/blob/master/slcm.py
41. *api.certspotter.com*. https://api.certspotter.com/v1/issuances?domain=jaipur.manipal.edu&include_subdomains=true&expand=dns_names
42. *slcm-manipal.github.io/index.html at master · slcm-manipal/slcm-manipal.github.io · GitHub*. https://github.com/slcm-manipal/slcm-manipal.github.io/blob/master/index.html
43. *slcm-manipal.github.io/GradeSheet.html at master · slcm-manipal/slcm-manipal.github.io · GitHub*. https://github.com/slcm-manipal/slcm-manipal.github.io/blob/master/GradeSheet.html
44. *api.certspotter.com*. https://api.certspotter.com/v1/issuances?domain=manipal.edu&include_subdomains=true&expand=dns_names
45. *registry.npmjs.org*. https://registry.npmjs.org/-/v1/search?text=mujslcm
46. *SLCM_APP/android/app/google-services.json at main · DK10WS/SLCM_APP · GitHub*. https://github.com/DK10WS/SLCM_APP/blob/main/android/app/google-services.json
47. *Muj Slcm*. https://api.github.com/repos/Anushkakumar10/muj_slcm/git/trees/main?recursive=1
48. *Search results for manipal.edu*. https://leakix.net/search?scope=service&q=manipal.edu
49. *SLCM_APP/lib/main.dart at main · DK10WS/SLCM_APP · GitHub*. https://github.com/DK10WS/SLCM_APP/blob/main/lib/main.dart
50. *muj_slcm/muj_slcm/muj_slcm/settings.py at main · Anushkakumar10/muj_slcm · GitHub*. https://github.com/Anushkakumar10/muj_slcm/blob/main/muj_slcm/muj_slcm/settings.py
51. *Slcm App*. https://api.github.com/repos/DK10WS/SLCM_APP/git/trees/main?recursive=1
52. *muj_slcm/muj_slcm/muj_slcm_app/views.py at main · Anushkakumar10/muj_slcm · GitHub*. https://github.com/Anushkakumar10/muj_slcm/blob/main/muj_slcm/muj_slcm_app/views.py
53. *registry.npmjs.org*. https://registry.npmjs.org/-/v1/search?text=manipal%20slcm
54. *SLCM_APP/lib/session_manager.dart at main · DK10WS/SLCM_APP · GitHub*. https://github.com/DK10WS/SLCM_APP/blob/main/lib/session_manager.dart
55. *LeakIX - Login*. https://leakix.net/search?scope=leak&q=manipal.edu
56. *Slcmandlms Aggregator*. https://api.github.com/repos/madhav-manchanda/SlcmAndLms-aggregator
57. *SLCM_APP/lib/utils at main · DK10WS/SLCM_APP · GitHub*. https://github.com/DK10WS/SLCM_APP/tree/main/lib/utils
58. *muj_slcm/muj_slcm/muj_slcm/urls.py at main · Anushkakumar10/muj_slcm · GitHub*. https://github.com/Anushkakumar10/muj_slcm/blob/main/muj_slcm/muj_slcm/urls.py
59. *yemit - npm*. https://www.npmjs.com/package/yemit
60. *registry.npmjs.org*. https://registry.npmjs.org/yemit
61. *muj_slcm/muj_slcm/muj_slcm_app/student_views.py at main · Anushkakumar10/muj_slcm · GitHub*. https://github.com/Anushkakumar10/muj_slcm/blob/main/muj_slcm/muj_slcm_app/student_views.py
62. *SLCM_APP/lib/pages/login.dart at main · DK10WS/SLCM_APP · GitHub*. https://github.com/DK10WS/SLCM_APP/blob/main/lib/pages/login.dart
63. *SLCM-is-Dumb/HowThiswWorks.md at master · sankalp2004/SLCM-is-Dumb · GitHub*. https://github.com/sankalp2004/SLCM-is-Dumb/blob/master/HowThiswWorks.md
64. *slcmAPI/server.js at master · canaryGrapher/slcmAPI · GitHub*. https://github.com/canaryGrapher/slcmAPI/blob/master/server.js
