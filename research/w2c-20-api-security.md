# Securing the MUJ SLCM API Surface

## Executive Summary

- **Evidence Boundary**: The public MUJ landing page confirms an institutional sign-in choice plus separate parent and student login choices, but it does not publish an API specification or identify its authentication protocol [12]. Public student code supplies the strongest route evidence, so the club should treat those routes as leads for an authorized inventory, not as proof of an official or currently deployed API.

- **Concrete Route Exposure**: A public, third-party Flutter project defines routes for attendance, grades, internal marks, calendar events, directory information, CGPA/GPA, OTP, and the dashboard on `https://mujslcm.jaipur.manipal.edu` [56]. Because route names disclose business functions and expected data domains, MUJ should inventory, authenticate, authorize, log, and retire these endpoints as a single governed API surface.

- **Cookie Session Dominates Public Code**: The code performs a login-page GET, extracts `__RequestVerificationToken` and cookies, submits credentials by POST, and then sends the resulting cookie to academic-data requests [40]. No bearer-token use appears in the examined route clients, so the evidence supports a cookie-authenticated MVC/JSON model more strongly than an OAuth bearer API model.

- **BOLA Is The Priority Authorization Risk**: The exposed function names operate on student records, attendance, marks, and calendar events. OWASP describes broken object-level authorization as manipulation of an object identifier and requires a check that the logged-in user may perform the requested action on the requested object [5]. The defensive priority is server-side ownership and role enforcement on every request, even when the client sends an empty enrollment or student-code field.

- **CORS Is Unmeasured, Not Cleared**: No collected public source proves MUJ's live CORS policy. In classic Web API 2, origins, methods, headers, and credentials are separate policy dimensions, and wildcard origin is invalid when credential support is enabled [46]. MUJ should therefore test exact allowlists with university-owned origins under written authorization rather than assume Akamai or same-origin browser behavior prevents cross-origin exposure.

- **CSRF And Token Taxonomy Must Stay Separate**: Cookie authentication is susceptible to CSRF because browsers automatically send destination cookies; ASP.NET's classic mitigation is the anti-forgery or request-verification token [37]. The `__RequestVerificationToken` visible in third-party code is consequently evidence of a form anti-CSRF mechanism, not evidence of a Microsoft identity access token.

- **Legacy Services Remain An Inventory Question**: The passive searches found no indexed MUJ-specific `.asmx` or `.svc` service. That is not proof of absence because WCF metadata publishing is disabled by default, while enabled metadata can reveal a detailed and potentially sensitive service description [6]. Authorized source, IIS, and deployment-configuration review is more reliable than public URL guessing.

- **Edge Security Must Reach The Origin**: If the requester-supplied Akamai architecture is accurate, Site Shield only prevents direct-origin bypass after its subnet ranges are allowlisted at the origin perimeter [32]. MUJ should combine origin allowlisting, verified edge-to-origin TLS, controlled forwarded-header trust, IIS request filtering, and application-layer authorization rather than treat the CDN as the authorization boundary.

- **Verdict**: Public evidence establishes a meaningful, cookie-oriented MVC/JSON surface and discloses multiple sensitive business routes. It does not establish a live exploitable CORS, authorization, token-validation, verbose-error, ASMX, or WCF vulnerability. The correct action is an authorized validation program focused first on object authorization, cookie and anti-forgery handling, route inventory, and origin controls.

## 1. Scope, Evidence Classes, And Safety Boundary

This is a passive OSINT and defensive architecture assessment. It uses the public portal page, public GitHub repositories and source files, and primary documentation from Microsoft, OWASP, IETF, Akamai, and MDN. It does not report the results of probing undocumented paths, sending malformed requests, attempting authentication, changing object identifiers, enumerating students, testing stolen credentials, or bypassing Akamai.

The requester supplied the following stack description: ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10 behind Akamai, with Microsoft 365 identity. The open-web search performed for this report did not independently establish those exact versions or components. They are therefore a **scope assumption**, not an OSINT finding. The recommendations are applicable if that assumption is accurate, but the university should confirm versions from its software bill of materials, IIS configuration, application packages, and identity registration records.

The evidence must be separated into four classes:

| Evidence class | What is established | What is not established | Decision use |
|---|---|---|---|
| Direct first-party public evidence | The MUJ portal presents institutional, parent, and student sign-in choices [12]. | Authentication protocol, API list, live CORS policy, cookie attributes, and authorization decisions are not shown. | Establishes the public entry point only. |
| Direct third-party code evidence | A public Flutter project names MUJ routes and models cookies, anti-forgery tokens, OTP, and academic-data calls [56][40]. | The code is not an official specification and may be incomplete, inaccurate, or stale. | Supplies candidates for an authorized internal inventory. |
| Authoritative platform guidance | Microsoft documents Web API routing, CORS, CSRF, IIS errors, WCF metadata, and identity-token responsibilities [18][46][37][6][45]. | It does not reveal MUJ's current configuration. | Defines expected controls and test assertions. |
| Explicit inference | Route semantics suggest sensitive academic records and a cookie-oriented MVC/JSON design. | It cannot establish exploitability, data access, or the deployed server implementation. | Prioritizes review without declaring a vulnerability. |

A note on reasoning: this report provides an auditable evidence-to-inference-to-action trail rather than private chain-of-thought. Every inference is labeled, and every proposed test is limited to a university-approved environment, university-issued test accounts, and written rules of engagement. The OWASP Web Security Testing Guide describes itself as a comprehensive guide for testing web applications and web services [2]; using that kind of methodology still requires explicit authorization from the asset owner.

**Decision-ready insight:** The club has enough evidence to propose a scoped assessment, but not enough to announce a breach, vulnerability, or unsupported technology fingerprint.

## 2. Public MUJ Evidence Reveals A Functional MVC/JSON Surface

The first-party landing page is modest: it says "WELCOME TO MUJ PORTAL" and offers institutional, parent, and student login paths [12]. It does not expose an OpenAPI document, developer portal, route list, token description, or service contract in the collected page content. This makes public client code unusually important, but also requires careful qualification.

A public repository describes itself as an app version of MUJ SLCM and says it can display attendance, grades, GPA/CGPA, subject-wise attendance, and a timetable; it identifies Flutter/Dart as the front end, FastAPI as its own back end, and custom email/password logic as its authentication layer [11]. Those are claims about the third-party project, not proof that MUJ officially operates FastAPI or endorses the app.

The strongest endpoint evidence comes from `lib/pages/redirects.dart`, which defines the following URL constants [56]:

| Public code constant | Exact route in third-party source | Apparent business function | Evidence status |
|---|---|---|---|
| `loginURL` | `https://mujslcm.jaipur.manipal.edu` | Login entry point | Exact third-party string; not an official API declaration [56]. |
| `Attendance` | `/Student/Academic/GetAttendanceSummaryList` | Attendance summary | Exact third-party string [56]. |
| `GradesURL` | `/Student/Academic/GetGradesForFaculty` | Grades | Exact third-party string [56]. |
| `MarksURL` | `/Student/Academic/GetInternalMarkForFaculty` | Internal marks | Exact third-party string [56]. |
| `TimeTableWeek` | `/Student/Academic/GetStudentCalenderEventList` | Weekly calendar events | Exact third-party string, including the source's spelling of `Calender` [56]. |
| `TimeTableEvent` | `/Student/Academic/GetEventDetailStudent` | Event detail | Exact third-party string [56]. |
| `InformationURL` | `/Employee/EmployeeDirectory/IndexStudent` | Student-facing directory | Exact third-party string [56]. |
| `CGPAURL` | `/Student/Academic/GetCGPAGPAForFaculty` | CGPA/GPA | Exact third-party string [56]. |
| `otpValidateURL` | `/Home/OnValidate` | OTP validation | Exact third-party string [56]. |
| `otpIndexURL` | `/Home/IndexOTP` | OTP page or workflow | Exact third-party string [56]. |
| `HomeURL` | `/Home/Dashboard` | Dashboard | Exact third-party string [56]. |
| `OnExpireURL` | `/Home/OnExpire` | OTP or session expiration | Exact third-party string [56]. |
| `ResendOTPUrl` | `/Home/ResendOTP` | OTP resend | Exact third-party string [56]. |

These paths look like MVC controller/action routes rather than a canonical `/api/v1/...` design. **Inference:** verbs such as `GetAttendanceSummaryList` and `GetInternalMarkForFaculty` suggest JSON-returning action methods behind MVC or Web API routing, but names alone cannot identify the controller base class, serializer, response content type, or server framework.

Classic Web API 2 supports both convention-based routing and attribute routing. Microsoft gives `[Route("customers/{customerId}/orders")]` as an attribute-route template and notes that attribute and convention routing can coexist [18]. Therefore, absence of `/api` is not evidence that a route is not an API, while an API-looking path is not evidence that it is anonymously accessible.

**Decision-ready insight:** Import every route above into the authorized asset inventory, assign an owner and data classification, then verify it against server-side route registration. Do not equate public naming with public authorization.

## 3. Request Semantics Show Sensitive Data And Object Boundaries

Separate source files provide method, parameter, session, and response evidence. This is more informative than route names because it shows how an unofficial client expects the portal to behave.

| Function | HTTP behavior in public code | Submitted fields | Authentication context | Response fields consumed |
|---|---|---|---|---|
| Login | GET login page, then POST credentials [40] | `__RequestVerificationToken`, `EmailFor`, `LoginFor`, `UserName`, `Password` [40] | Cookies from `Set-Cookie` are returned in a later `Cookie` header [40]. | A 302 response is treated as successful and combined cookies are returned [40]. |
| Attendance | POST [55] | `StudentCode`, supplied as an empty string [55] | `SessionManager.sessionCookie` in `Cookie` [55] | `AttendanceSummaryList`, including `CourseID`, `Percentage`, `Total`, and `Present` [55]. |
| Grades | POST [27] | `Enrollment`, supplied empty, and selected `Semester` [27] | Session cookie [27] | `InternalMarksList`, `CourseID`, `Grade`, and `Credits` [27]. |
| Internal marks | POST [30] | Empty `Enrollment` and selected `Semester` [30] | Session cookie [30] | `MTE1`, `MTE2`, `CWS`, `ETE`, `PRS`, `Total`, and `RESESSION` [30]. |
| Weekly timetable | POST [53] | `Year`, `Month`, `Type`, `Dated`, and `PreNext` [53] | Session cookie [53] | Event data grouped by `StartDate` [53]. |
| Timetable event | POST [53] | `EventID` [53] | Session cookie [53] | `AttendanceType` and `SlotScheme`-derived time [53]. |

**Inference:** Empty `StudentCode` or `Enrollment` values may mean the server derives the current student from the authenticated session. If so, that is generally safer than trusting a client-selected student identifier. It is not proof of safety: every endpoint still needs a server-side rule binding the session principal, requested semester or event, and returned record.

The most important test category is object-level authorization. OWASP describes BOLA as a violation at the object level, commonly involving manipulation of an identifier, and says the server must check whether the logged-in user may perform the requested action on the requested object [5]. For SLCM, the relevant objects include student records, course registrations, grade rows, attendance summaries, calendar events, and directory entries.

The authorized assessment should not simply ask whether an endpoint returns HTTP 200. It should ask whether each object is within the authenticated user's permitted scope, whether role changes affect scope immediately, and whether parent, student, faculty, and administrative roles are separated. Test objects must be synthetic or belong to consenting test accounts. Real student identifiers should not be enumerated.

OWASP also requires access control at every non-public REST endpoint [47]. That control belongs on the server. Hidden menu items, empty client fields, JavaScript checks, Akamai rules, or an unguessable route name are not substitutes.

**Decision-ready insight:** The route inventory and object-authorization matrix should be reviewed together. The academic endpoints carry the greatest potential impact because they combine sensitive records with identifiers, semesters, events, and role semantics.

## 4. Session Cookies, Anti-Forgery Tokens, And Microsoft Identity Are Distinct Layers

The public client code strongly supports a session-cookie flow. It fetches the login page, extracts cookies and an HTML input named `__RequestVerificationToken`, posts credentials, collects response cookies, and reuses the cookie string [40]. A separate `SessionManager` holds the session cookie in a static variable and clears it on logout [28]. This is evidence about the third-party client's behavior, not the exact name, attributes, encryption, or server lifetime of the real cookie.

The larger login page also saves a username and password in Flutter `SharedPreferences` and can use saved credentials for automatic login [35]. **Inference:** That is a third-party client-side credential-storage concern. It should not be attributed to the MUJ server, but the university should assess whether unofficial clients are encouraged by missing official mobile support and whether policy, user education, or an approved API can reduce password handling by third parties.

The code links to `https://passwordreset.microsoftonline.com/` [35], and the public portal presents a university-domain sign-in choice [12]. Neither fact proves that the examined academic endpoints accept Microsoft Entra bearer tokens. The requester-supplied "Microsoft 365 identity" should therefore be decomposed into at least three possible layers:

| Layer | Purpose | Evidence in this review | Required control |
|---|---|---|---|
| Microsoft identity or institutional SSO | Authenticate the human and possibly issue identity tokens | Scope assumption plus a Microsoft password-reset link in third-party code [35]. | Validate the actual OIDC/SAML/OAuth registration and redirect URIs internally. |
| MVC session cookie | Maintain the browser's application session | Strongly represented in third-party code [40][28]. | Secure attributes, rotation, expiration, logout invalidation, and CSRF defenses. |
| OAuth access token | Authorize a client to a resource API | No bearer use found in the examined MUJ client files. | If present elsewhere, validate it at the resource API and keep it separate from ID tokens. |

Microsoft states that access tokens differ from ID tokens, which serve as proof of authentication, and that the resource server validates an access token before accepting it as authorization evidence [45]. Its claim-validation guidance identifies audience, tenant, subject, and actor where applicable as API validation concerns [50]. A portal must not accept an ID token merely because it is signed, nor accept an access token issued for a different audience.

RFC 6750 requires TLS for bearer-token use, recommends the `Authorization: Bearer` header, and warns against tokens in page URLs because histories, logs, and other locations can leak them [49]. If MUJ has bearer APIs not visible in the public code, those properties become mandatory review items.

**Decision-ready insight:** First document the real boundary: Entra authentication, MVC session creation, and API authorization. Treating all three artifacts as interchangeable "tokens" creates validation and incident-response gaps.

## 5. Cookie Hardening And CSRF Must Be Tested Together

Cookie security has two independent questions: can an attacker obtain or misuse the cookie, and can another site cause the browser to send it? `Secure`, `HttpOnly`, and `SameSite` address different parts of that problem. MDN states that `Secure` limits transmission to HTTPS, `HttpOnly` prevents JavaScript access through `Document.cookie`, and `SameSite` controls cross-site sending and provides some CSRF protection [8].

OWASP recommends not storing authentication tokens, session IDs, JWTs, refresh tokens, or credentials in `localStorage` or `sessionStorage`, and instead recommends hardened cookies. It also says session cookies should explicitly use `SameSite=Strict` where possible or `Lax`, and that `SameSite=None` must not be used without `Secure` [17]. Exact `SameSite` selection remains a product decision: cross-domain identity redirects can require carefully scoped exceptions.

CSRF remains relevant because browsers automatically send cookies to the destination site. Microsoft identifies cookie-authenticated sites as typical CSRF targets and names ASP.NET anti-forgery tokens, also called request-verification tokens, as the mitigation [37]. The public login code's `__RequestVerificationToken` handling is consistent with that pattern [40]. It does not show whether every state-changing action validates a token, whether JSON actions use a custom header, or whether token and cookie values are bound correctly.

An authorized review should establish the following assertions:

| Assertion | Pass condition | Failure significance |
|---|---|---|
| Cookie transport | Every authentication cookie is `Secure`; edge-to-origin transport is also protected. | Network or proxy-path exposure. |
| Script access | Session cookies are `HttpOnly` unless there is a documented exception. | XSS can more easily extract session material. |
| Cross-site policy | `SameSite` is explicit and compatible with the documented identity flow. | Cross-site session use may be broader than intended. |
| Session rotation | The application rotates session identifiers after authentication and privilege changes. | Session fixation or stale privilege risk. |
| Logout and expiry | Server-side session invalidation works; the client clears local state. | Reuse after logout or role change. |
| Anti-forgery | Every state-changing cookie-authenticated action validates an unpredictable token or approved equivalent. | Cross-site actions may execute in a victim's session. |
| Sensitive caching | Authenticated academic responses are not stored in shared caches. | Grades or attendance may leak between users. |

These checks should be made with university-issued test accounts and browser developer tools or an approved intercepting proxy. They should not be performed with captured real-user sessions.

**Decision-ready insight:** The visible anti-forgery token is encouraging but not a clean bill of health. Coverage across JSON POST actions matters more than the presence of a token on the login page.

## 6. CORS Is A Policy Matrix, Not A Single Header

No public evidence collected here demonstrates MUJ's current `Access-Control-Allow-Origin`, `Access-Control-Allow-Credentials`, preflight, or cache behavior. The report therefore makes no finding that CORS is vulnerable or secure.

Classic Web API 2 exposes several independent CORS dimensions. Microsoft documents an `origins` list, allowed `methods`, and allowed request `headers`; each can use `*` in appropriate contexts [46]. Credentials are disabled by default at the browser-policy level unless the client requests them and the server supports them. Critically, `*` is invalid as the allowed origin when credential support is enabled [46].

For a cookie-oriented portal, an overbroad credentialed allowlist is higher risk than a permissive policy on a genuinely public, non-sensitive endpoint. The assessment should therefore evaluate CORS per endpoint and data class.

| CORS case | Defensive expectation | Rationale |
|---|---|---|
| Login and OTP routes | Only documented university origins, or no cross-origin access if not required | These routes influence authentication state. |
| Attendance, grades, marks, CGPA | No cross-origin credentials unless an approved client architecture requires them | These routes return sensitive academic records. |
| Timetable and directory | Explicit origins and minimum response fields | Even lower-sensitivity data can support profiling. |
| Public static content | A broader origin policy may be acceptable if it never returns user-specific data | Public content and authenticated APIs should not inherit one global policy blindly. |
| Preflight caching | `Vary: Origin` and carefully bounded cache behavior where origins vary | Prevent one origin's response policy from being reused incorrectly. |

**Inference:** Because the third-party app sends a raw `Cookie` header in a non-browser Flutter client [55], it is not subject to browser CORS enforcement in the same way as browser JavaScript. That demonstrates why CORS is not an authentication or authorization control. A native client, server-side process, or compromised browser context can reach the network without relying on CORS permission; the server must still authenticate and authorize every request.

The authorized test should use only pre-approved university origins and a controlled test API response. Review expected and unexpected origins, credentialed and non-credentialed requests, simple and preflighted methods, allowed headers, `null` origin handling, redirects, and cache variation. It should not host deceptive pages or target real students.

**Decision-ready insight:** Treat CORS as defense in depth. Exact allowlists reduce browser data exposure, but only server-side authorization protects the underlying student objects.

## 7. ASMX, WCF/SVC, JSON Actions, And Error Responses

The passive search did not return an indexed MUJ-specific `.asmx` or `.svc` endpoint. This is a limited negative finding, not a proof of absence. WCF does not publish metadata by default, while published metadata can contain a detailed service description and potentially sensitive information [6]. An unindexed service, internal-only binding, disabled metadata endpoint, or route behind authentication could therefore remain invisible to search engines.

The right method is an internal inventory of IIS applications, deployed assemblies, `web.config`, service activation entries, route registration, source controllers, and API gateway rules. The inventory should include MVC JSON actions, Web API controllers, ASMX files, WCF `.svc` services, scheduled integrations, mobile back ends, and deprecated versions. OWASP warns that inadequate inventory and retirement can leave unpatched or deprecated endpoints exposed, and recommends recording environment, access, version, role, data flow, sensitivity, authentication, errors, redirects, rate limits, CORS, endpoints, parameters, requests, and responses [16].

Verbose errors require controls at several layers:

| Layer | Relevant control | Defensive objective |
|---|---|---|
| ASP.NET Web API | Global exception logger and handler | Return a stable generic error contract while retaining correlation details in protected logs. Web API cannot always replace a response after streaming has begun [42]. |
| MVC application | Production custom errors and centralized exception handling | Prevent stack traces, source paths, SQL details, controller names, and secrets from reaching users. |
| WCF | Keep `includeExceptionDetailInFaults` disabled in production | Microsoft says enabling it returns otherwise undeclared application exceptions and is not secure in production [34]. |
| IIS | `<httpErrors>` with external custom errors | `DetailedLocalOnly` returns detail locally and custom errors to external clients, avoiding external disclosure [43]. |
| Akamai/CDN | Consistent edge error mapping and cache rules | Prevent caching of authenticated errors and avoid exposing origin-specific diagnostics. |

Errors should carry a correlation identifier, generic client message, and appropriate status code. Protected server logs can retain the exception, route, principal, request identifier, and deployment version. Sensitive values such as passwords, cookies, bearer tokens, OTPs, anti-forgery tokens, student identifiers, and full response bodies should be redacted.

For WCF metadata that is genuinely required, Microsoft notes that HTTP GET metadata endpoints can use SSL [6]. The safer production posture is to publish only what an integration needs, authenticate where appropriate, protect transport, and prevent metadata from becoming an undocumented external discovery mechanism.

**Decision-ready insight:** Do not spend the assessment guessing `.asmx` and `.svc` URLs on production. A configuration-backed inventory is both safer and more complete.

## 8. IIS And Akamai Must Enforce A Continuous Trust Boundary

This section is conditional on the requester-supplied IIS 10 and Akamai architecture being accurate. A CDN can reduce exposure, but it does not decide whether one student may read another student's marks.

Akamai Site Shield routes traffic to the origin through defined IP ranges. Akamai says those ranges must be allowlisted at the perimeter to help prevent direct attacks that bypass cloud defenses [32]. If an origin remains publicly reachable from arbitrary addresses, an attacker may avoid edge rate limits, WAF policy, bot controls, or edge logging. **Inference:** Origin closure is therefore a prerequisite for treating Akamai controls as consistently applied.

Akamai also allows client identity to be derived from the connecting address or `X-Forwarded-For`; when a proxy or load balancer is used, that header represents the original client address [10]. The origin should accept forwarded identity only from trusted Akamai paths, normalize duplicate or malformed chains, and never let an untrusted direct client self-assert a privileged source IP.

For edge-to-origin encryption, Akamai recommends secure HTTPS delivery. Its documented Platform Settings trust certificates from the Akamai certificate store and require the certificate CN or SAN to match the forwarded host header [7]. MUJ should confirm hostname verification, certificate lifecycle, modern TLS, and no HTTP downgrade between edge and origin.

IIS Request Filtering can restrict URL sequences, extensions, hidden segments, request and query lengths, verbs, query sequences, custom patterns, and header lengths [51]. These controls can reject malformed or unexpectedly large input before application processing, but they must not replace application validation.

| Boundary | Required control | Evidence to retain |
|---|---|---|
| Internet to Akamai | TLS, WAF/bot/rate policy, request identifiers | Edge configuration version and security-event logs. |
| Akamai to origin | Origin allowlist, authenticated or verified TLS, host-header validation | Firewall rules, certificate checks, origin connection logs. |
| Proxy identity | Trust forwarded headers only from approved edge ranges | Normalization rules and a known-good client-IP log sample. |
| IIS | Request Filtering, external custom errors, least enabled modules | Exported IIS configuration and change history. |
| Application | Authentication, per-object authorization, CSRF, input validation | Automated tests and authorization decision logs. |
| Data tier | Parameterized access and least-privilege service account | Database role review and audit records. |

**Decision-ready insight:** Validate the full request path. A correct edge policy with a reachable origin, spoofable forwarded header, or missing application authorization is not a complete control.

## 9. Public Student Scripts Are Both Evidence And Supply-Chain Risk

The public repositories illuminate the portal, but their behavior must not be confused with official design. The Flutter client manually parses `Set-Cookie`, sends a concatenated `Cookie` header, and reauthenticates after some 302 responses [54][40]. The login page code stores credentials in `SharedPreferences` and supports automatic login [35]. These behaviors increase the importance of university guidance about unofficial clients and credential handling.

A separate feedback-form extension manipulates radio controls and dropdowns, dispatches change events, and can click `btnSubmit` automatically [25]. Its manifest requests `scripting`, `activeTab`, `<all_urls>`, and a content-script match of `*://*/*` [21]. **Inference:** That breadth is an extension supply-chain and least-privilege concern; it is not evidence of a MUJ server vulnerability.

The university security response should be measured. Public code should not be treated as malicious merely because it automates a portal. Instead, MUJ can:

1. Publish an acceptable-use and responsible-disclosure policy.
2. Offer a documented, scoped integration mechanism if student demand is legitimate.
3. Warn users not to provide university passwords to unofficial applications.
4. Encourage browser extensions to limit host permissions to the minimum required origin.
5. Detect anomalous automation through rate and behavior controls without collecting unnecessary student data.
6. Rotate or redesign routes only when needed; route secrecy is not an access-control strategy.

The strongest lesson is architectural. Unofficial clients will reproduce whichever login and session behavior the web portal exposes. If an approved mobile API is needed, an authorization-code flow with PKCE, short-lived audience-restricted access tokens, platform-protected storage, and server-side scopes is preferable to distributing logic that handles raw passwords. This is a recommendation, not a claim about MUJ's current capabilities.

**Decision-ready insight:** Treat public student code as a source of attack-surface intelligence and user-demand evidence. Fix server controls first, then reduce risky unofficial credential handling through supported alternatives and clear policy.

## 10. Authorized Validation Plan

No step below should occur until MUJ names the assets, approves the time window, supplies test accounts and synthetic records, identifies emergency contacts, defines prohibited actions, and agrees on evidence retention. Production testing should be minimized; a representative staging environment is preferable.

| Phase | Authorized activity | Expected artifact | Stop condition |
|---|---|---|---|
| 1. Governance | Written scope for hosts, routes, roles, rate limits, data, and test times | Signed rules of engagement | No signed approval or unclear ownership. |
| 2. Internal inventory | Compare source routes, IIS applications, assemblies, MVC/Web API registration, ASMX/SVC activation, Akamai properties, and identity registrations | Authoritative API register | Discovery of an unmanaged production integration. |
| 3. Baseline capture | Use university-issued test accounts to record normal login, anti-forgery, cookie, redirect, and logout behavior | Sanitized request-flow diagram | Any real-user credential or record appears. |
| 4. Authorization matrix | With synthetic accounts, verify role and object ownership for every endpoint | Endpoint-by-role-by-object table | Response contains data outside the synthetic tenant or account set. |
| 5. CSRF review | Confirm every state-changing cookie-authenticated action validates an approved anti-forgery mechanism | Automated positive and negative tests | Test might affect a real account or send an OTP to a real user. |
| 6. CORS review | Evaluate exact approved and unapproved origins, credentials, preflights, headers, redirects, and cache variation | CORS policy matrix | Any test requires an uncontrolled external domain. |
| 7. Error review | Trigger safe, designed validation failures in staging and compare application, IIS, WCF, and edge responses | Error-contract and log-redaction report | Stack trace or secret appears in production. |
| 8. Session review | Check cookie flags, rotation, expiry, logout, concurrent sessions, and role changes | Session-lifecycle test record | Session material would need to leave the approved test workstation. |
| 9. Edge/origin review | Confirm Site Shield ranges, firewall rules, origin TLS, forwarded-header trust, and direct-origin closure | Network-path assurance record | Test could disrupt edge or origin availability. |
| 10. Remediation regression | Convert each confirmed issue into a repeatable automated test | CI/CD security gate | Test uses production personal data. |

Severity should reflect demonstrated impact, not route appearance. A confirmed cross-student marks disclosure would be critical or high depending on scale and controls; a verbose framework banner without sensitive data would normally rank much lower. Evidence should contain only the minimum request and response fragments needed to reproduce a finding, with credentials and personal data redacted.

## 11. Synthesis: Routes, Identity, Browser Policy, And Edge Controls

The major control families address different mechanisms and cannot substitute for one another.

| Dimension | MVC session and CSRF | Bearer API | CORS | IIS/WCF errors | Akamai/origin |
|---|---|---|---|---|---|
| Primary mechanism | Cookie establishes application session; anti-forgery proves request intent | Access token authorizes a client to an API audience | Browser decides whether one origin may read another origin's response | Server controls diagnostic disclosure | Edge filters and proxies traffic before origin |
| Evidence for MUJ | Strong third-party code evidence [40][55] | No bearer use found in examined MUJ files | Live policy unknown | Live configuration unknown | Stack presence is requester-supplied; controls are platform guidance |
| Key failure | Session theft, fixation, missing CSRF, stale logout | Wrong audience or token type, URL leakage | Overbroad credentialed origin | Stack traces, service details, sensitive logs | Direct-origin bypass or spoofed forwarded identity |
| Correct control | Harden cookies, rotate sessions, validate anti-forgery | TLS, authorization header, resource-server validation [49][45] | Exact policy per route and data class [46] | Generic external errors, protected detailed logs [43][34] | Origin allowlist, verified TLS, trusted proxy boundary [32][7] |
| Residual limitation | Does not stop an authorized user from requesting another user's object if BOLA exists | Does not protect against incorrect object authorization by itself | Does not protect native clients or direct HTTP callers | Does not enforce authorization | Does not understand student-record ownership |

Three non-obvious tensions follow.

First, the visible anti-forgery token is both a positive control signal and a warning against taxonomy confusion. It indicates awareness of cookie-request forgery in at least part of the workflow [40], but it is not a Microsoft access token and cannot authorize academic objects.

Second, a CDN can make direct attack traffic harder while simultaneously complicating attribution if forwarded headers are trusted incorrectly. Akamai supports both connecting-IP and forwarded-IP models [10]; the origin must know which proxy hops it trusts. Authorization should never depend only on a client IP.

Third, public route disclosure is less important than server enforcement. Renaming `/GetInternalMarkForFaculty` might reduce casual discovery, but the route is already present in public code [56]. Durable security comes from authenticated principals, role checks, per-object checks, minimum response fields, logging, and tests.

The holistic conclusion is therefore not "hide the endpoints" and not "Akamai protects them." It is: maintain one authoritative inventory from edge to code, establish the real identity-to-session boundary, enforce authorization for every object, constrain browser cross-origin behavior, suppress external diagnostics, and continuously regression-test those assertions.

## VERDICT

**Verdict: A substantial and sensitive API-like surface is publicly inferable, but no live exploitable vulnerability is established.**

Public third-party source code names at least thirteen MUJ-hosted routes or route constants covering authentication, OTP, dashboard, attendance, grades, marks, CGPA/GPA, directory information, and timetable functions [56]. Separate files show POST requests, session-cookie reuse, anti-forgery-token handling, and structured academic response fields [40][55][27][30][53]. This is sufficient to justify a high-priority authorized review.

It is not sufficient to claim that MUJ currently has BOLA, CORS misconfiguration, bearer-token confusion, verbose errors, exposed ASMX/WCF metadata, origin bypass, or insecure cookie attributes. No active validation was performed, and the exact MVC, .NET, IIS, Akamai, and Microsoft 365 stack remains a requester-supplied assumption rather than an independently confirmed finding.

**Confidence:**

| Conclusion | Confidence | Basis |
|---|---|---|
| Public code discloses the listed route strings | High | Exact strings in a public source file [56]. |
| Unofficial client expects cookie sessions and an anti-forgery token | High for the code; medium for the current server | Direct client logic [40], but third-party code can drift. |
| Academic endpoints process sensitive object types | High for client expectations | Exact consumed fields in attendance, grades, marks, and timetable code [55][27][30][53]. |
| MUJ uses bearer tokens on these routes | Low / not established | No bearer use found in the examined client files. |
| MUJ exposes ASMX or WCF/SVC services | Low / not established | No indexed target-specific evidence; WCF metadata can be disabled by default [6]. |
| A live exploitable API vulnerability exists | Low / not established | No authorized active test evidence. |
| Authorized BOLA, session, CSRF, CORS, error, and origin review is warranted | High | Sensitive route semantics plus authoritative control requirements [5][37][46][32]. |

The university security club should present this as an **attack-surface and assurance proposal**, not a vulnerability disclosure. The first three work items should be: (1) reconcile the public route list with an internal authoritative inventory, (2) run a synthetic-account object-authorization matrix, and (3) document the Entra-to-MVC-session boundary, cookie attributes, anti-forgery coverage, and logout behavior.

## References

1. *OpenID Connect (OIDC) on the Microsoft identity platform*. https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols-oidc
2. *OWASP Web Security Testing Guide*. https://owasp.org/www-project-web-security-testing-guide
3. *GitHub - Anushkakumar10/muj_slcm · GitHub*. http://github.com/Anushkakumar10/muj_slcm
4. *Access token claims reference - Microsoft identity platform*. https://learn.microsoft.com/en-us/entra/identity-platform/access-token-claims-reference
5. *API1:2023 Broken Object Level Authorization*. https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization
6. *Security Considerations with Metadata - WCF | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/framework/wcf/feature-details/security-considerations-with-metadata
7. *Origin Server - Property Manager*. https://techdocs.akamai.com/property-mgr/docs/origin-server
8. *Set-Cookie header - HTTP - MDN Web Docs*. https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie
9. *RFC 6265 - HTTP State Management Mechanism - Datatracker*. https://datatracker.ietf.org/doc/html/rfc6265
10. *Client IP - Property Manager*. https://techdocs.akamai.com/property-mgr/docs/client-ip
11. *GitHub - DK10WS/SLCM_APP: App Version for MUJ SLCM · GitHub*. http://github.com/DK10WS/SLCM_APP
12. *Manipal University - mujslcm.jaipur.manipal.edu*. https://mujslcm.jaipur.manipal.edu/Home/Index
13. *.NET Framework official support policy*. https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-framework
14. *OWASP Top 10 API Security Risks – 2023*. https://owasp.org/API-Security/editions/2023/en/0x11-t10
15. *Prevent Cross-Site Request Forgery (XSRF/CSRF) attacks in ASP.NET ...*. https://docs.asp.net/en/latest/security/anti-request-forgery.html
16. *API9:2023 Improper Inventory Management*. https://owasp.org/API-Security/editions/2023/en/0xa9-improper-inventory-management
17. *Session Management Cheat Sheet*. https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
18. *Attribute Routing in ASP.NET Web API 2 - Microsoft Learn*. https://learn.microsoft.com/en-us/aspnet/web-api/overview/web-api-routing-and-actions/attribute-routing-in-web-api-2
19. *GitHub - AddisionS/slcm-feedback-form-filler: This is a chrome extension that can be used to automate the process of filling feedback form on MUJ's SLCM portal · GitHub*. https://github.com/AddisionS/slcm-feedback-form-filler
20. *Muj Slcm*. https://api.github.com/repos/Anushkakumar10/muj_slcm/git/trees/main?recursive=1
21. *Slcm Feedback Form Filler*. https://raw.githubusercontent.com/AddisionS/slcm-feedback-form-filler/main/chrome/manifest.json
22. *Slcm Feedback Form Filler*. https://raw.githubusercontent.com/AddisionS/slcm-feedback-form-filler/main/firefox/popup.js
23. *Slcm Feedback Form Filler*. https://raw.githubusercontent.com/AddisionS/slcm-feedback-form-filler/main/chrome/popup.js
24. *Slcm Feedback Form Filler*. https://raw.githubusercontent.com/AddisionS/slcm-feedback-form-filler/main/firefox/content.js
25. *Slcm Feedback Form Filler*. https://raw.githubusercontent.com/AddisionS/slcm-feedback-form-filler/main/chrome/content.js
26. *Routing in ASP.NET Web API | Microsoft Learn*. https://learn.microsoft.com/en-us/aspnet/web-api/overview/web-api-routing-and-actions/routing-in-aspnet-web-api
27. *Slcm App*. https://raw.githubusercontent.com/DK10WS/SLCM_APP/main/lib/pages/grades.dart
28. *Session Manager*. https://raw.githubusercontent.com/DK10WS/SLCM_APP/main/lib/session_manager.dart
29. *Muj Slcm App*. https://raw.githubusercontent.com/Anushkakumar10/muj_slcm/main/muj_slcm/muj_slcm_app/models.py
30. *Slcm App*. https://raw.githubusercontent.com/DK10WS/SLCM_APP/main/lib/pages/marks.dart
31. *Muj Slcm*. https://raw.githubusercontent.com/Anushkakumar10/muj_slcm/main/muj_slcm/manage.py
32. *Welcome to Site Shield*. https://techdocs.akamai.com/site-shield/docs/welcome-site-shield
33. *Student Views*. https://raw.githubusercontent.com/Anushkakumar10/muj_slcm/main/muj_slcm/muj_slcm_app/student_views.py
34. *Service Debug Behavior - WCF | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/framework/wcf/samples/service-debug-behavior
35. *Slcm App*. https://raw.githubusercontent.com/DK10WS/SLCM_APP/main/lib/pages/login.dart
36. *XSRF/CSRF Prevention in ASP.NET MVC and Web Pages | Microsoft Learn*. https://learn.microsoft.com/en-us/aspnet/mvc/overview/security/xsrfcsrf-prevention-in-aspnet-mvc-and-web-pages
37. *Preventing Cross-Site Request Forgery (CSRF) Attacks in ASP.NET MVC | Microsoft Learn*. https://learn.microsoft.com/en-us/aspnet/web-api/overview/security/preventing-cross-site-request-forgery-csrf-attacks
38. *Verify scopes and app roles protected web API - Microsoft identity platform | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity-platform/scenario-protected-web-api-verification-scope-app-roles
39. *Muj Slcm*. https://raw.githubusercontent.com/Anushkakumar10/muj_slcm/main/muj_slcm/muj_slcm/settings.py
40. *Slcm App*. https://raw.githubusercontent.com/DK10WS/SLCM_APP/main/lib/utils/login.dart
41. *Cross-Site Request Forgery Prevention - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
42. *Global Error Handling in ASP.NET Web API 2 - ASP.NET 4.x | Microsoft Learn*. https://learn.microsoft.com/en-us/aspnet/web-api/overview/error-handling/web-api-global-error-handling
43. *HTTP Errors &lt;httpErrors&gt; | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/configuration/system.webserver/httperrors/
44. *Muj Slcm*. https://raw.githubusercontent.com/Anushkakumar10/muj_slcm/main/muj_slcm/muj_slcm/urls.py
45. *Access tokens in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens
46. *Enabling Cross-Origin Requests in ASP.NET Web API 2 | Microsoft Learn*. https://learn.microsoft.com/en-us/aspnet/web-api/overview/security/enabling-cross-origin-requests-in-web-api
47. *REST Security - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html
48. *WSTG - Latest | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/11-Client-side_Testing/07-Testing_Cross_Origin_Resource_Sharing
49. [
            
                RFC 6750 - The OAuth 2.0 Authorization Framework: Bearer Token Usage
            
        ](https://datatracker.ietf.org/doc/html/rfc6750)
50. *Secure applications and APIs by validating claims - Microsoft identity platform | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity-platform/claims-validation
51. *Request Filtering &lt;requestFiltering&gt; | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/configuration/system.webserver/security/requestfiltering/
52. *Slcm App*. https://api.github.com/repos/DK10WS/SLCM_APP/git/trees/main?recursive=1
53. *Slcm App*. https://raw.githubusercontent.com/DK10WS/SLCM_APP/main/lib/pages/timetable.dart
54. *Slcm App*. https://raw.githubusercontent.com/DK10WS/SLCM_APP/main/lib/utils/util.dart
55. *Slcm App*. https://raw.githubusercontent.com/DK10WS/SLCM_APP/main/lib/pages/Attendance.dart
56. *Slcm App*. https://raw.githubusercontent.com/DK10WS/SLCM_APP/main/lib/pages/redirects.dart
