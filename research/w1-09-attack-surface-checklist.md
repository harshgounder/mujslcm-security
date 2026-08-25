# Authorized ASP.NET MVC Portal Security Testing in India

## Executive Summary

- **Authorization First**: The highest-value tests are horizontal and vertical authorization, insecure direct object references (IDOR), protected-document access, and role confusion. IDOR occurs when user-controlled identifiers reach objects without sufficient authorization checks [1]. Use two university-issued test accounts and only objects owned by those accounts; compare the same request across sessions and never inspect a real third party's record.

- **Business Logic Before Cosmetic Findings**: Fee payment integrity, marks, timetables, notifications, profile lookup, and Student/Staff/Admin boundaries can expose financial or personal data even when every header is correct. OWASP distinguishes these design-level flaws from traditional injection and configuration weaknesses because they manipulate application workflows, state transitions, and decisions [13]. Test them with synthetic records or in staging, stopping before payment, record modification, message dispatch, or another irreversible transition.

- **Identity Controls Need Small, Controlled Comparisons**: User enumeration is demonstrated by materially different server responses for an existing test user and a definitely nonexistent user, not by the mere presence of an HTML `data-val-required` attribute. OWASP expects failed authentication responses to be consistent [2]. Lockout testing must use a sacrificial account at the end of the exercise because the test can deny access to that account [24].

- **Session and CSRF Tests Are High Value but Safe When Self-Contained**: Confirm that `ASP.NET_SessionId` changes after authentication or privilege change, because OWASP requires session renewal after a privilege transition [3]. For `__RequestVerificationToken`, send missing, modified, cross-session, and expired tokens only against a no-op action or dedicated test account. Include the login POST in scope, but never conduct login CSRF against another person.

- **ASP.NET Legacy Surfaces Need Configuration Review, Not Exploitation**: Check `customErrors`, compilation debug settings, `elmah.axd`, `trace.axd`, WebDAV, 8.3 short names, legacy `.aspx`/`.asmx`/`.svc` endpoints, `machineKey`, and WebForms ViewState. Microsoft defines `customErrors="Off"` as disabling custom errors and allowing standard errors, while `RemoteOnly` presents custom pages to remote clients [30]. Do not test leaked machine keys by forging authentication or deserialization payloads.

- **Dependency Presence Is Not Exploitability**: jQuery 1.10.2 falls within the version ranges for CVE-2015-9251, which affects jQuery before 3.0.0 under a particular cross-domain Ajax condition [17], and CVE-2019-11358, which affects versions before 3.4.0 when unsafe deep extension processes an enumerable `__proto__` property [10]. Report the old version as a component-risk finding, then separately prove whether the affected code path exists using inert input.

- **Written Permission Is a Hard Gate**: Section 43 of India's Information Technology Act addresses specified acts done without permission, including securing access and extracting data [11]. A signed Rules of Engagement should therefore name the exact host, accounts, source IPs, dates, permitted methods, prohibited actions, data-handling rules, emergency contacts, and stop conditions. A public-facing login page is not implied permission.

- **Disclosure Runs Owner First, CERT-In When Coordination Is Needed**: Send a private, encrypted report to the university's authorized security/IT contact and copy its formally designated nodal recipient. MUJ's official page lists Dr Amit Soni, Registrar, at `registrar@jaipur.manipal.edu` and states that the Registrar may receive administrative complaints and suggestions [16]. CERT-In maintains an official Responsible Vulnerability Disclosure and Coordination Policy page [25]; use it for national coordination, not as a substitute for university authorization.

- **A 90-Day Window Is Practice, Not Permission or Indian Statute**: Google's Project Zero uses a 90-day remediation period followed, when a patch arrives within that period, by a 30-day disclosure window [7]. Treat 90 days as a coordination benchmark, not an automatic publication trigger. For a live student portal, postpone technical publication if it could expose students while remediation remains active.

**Decision-ready insight:** Proceed only after written authorization. Within that scope, prioritize read-only authorization and business-logic tests over broad endpoint fuzzing, version disclosure, or aggressive IIS probing.

## Scope and Authorization: Written Permission Is the First Security Control

This report is a playbook for an authorized exercise. It does not assert that `mujslcm.jaipur.manipal.edu` is vulnerable, that the named routes are reachable, or that the stated component versions have been independently verified. The route names, hidden fields, jQuery version, password-reset destination, and technology stack are hypotheses supplied in the exercise brief. No live requests to the portal were required to prepare this report.

NIST SP 800-115 is intended to help organizations plan and conduct technical security tests, analyze findings, and develop mitigation strategies [31]. Apply that planning discipline through a signed Rules of Engagement before sending even a malformed request. The authorization should come from an officer who can bind the university or from an explicitly delegated system owner, not merely from a lecturer, student, help-desk employee, or portal user.

### Minimum written Rules of Engagement

| Field | Exact requirement | Why it matters |
|---|---|---|
| Assets | `mujslcm.jaipur.manipal.edu`, resolved IPs if appropriate, and any separately approved API, identity, payment, or staging hosts | Permission for one hostname does not automatically cover Microsoft Entra, a payment gateway, CDN, or vendor API. |
| Accounts and data | Named Student, Staff, and optional Admin test identities; synthetic records; ownership of test documents | Supports A/B authorization comparisons without touching real users. |
| Time and source | Start/end dates, time zone, approved tester IPs, and rate ceilings | Lets defenders distinguish testing from an attack and stop it safely. |
| Allowed methods | GET/HEAD, narrowly specified POSTs, proxy replay, token mutation, approved route checks, and configuration review | Prevents scope creep from passive review into exploitation. |
| Prohibited methods | DoS, password spraying, credential stuffing, unrestricted brute force, malware, persistence, shell upload, destructive SQL, social engineering, real payment, bulk scraping, or third-party testing | These create operational, legal, privacy, and financial risks disproportionate to validation value. |
| Data handling | No downloading of real student files; redact cookies, passwords, IDs, marks, and payment data; encrypt evidence; define retention and deletion date | A finding should not become a second data exposure. |
| Stop conditions | Unexpected personal data, service instability, lockout of a non-test account, payment authorization, email/SMS flood, evidence of active compromise, or request from the incident lead | Turns safety from an intention into an executable rule. |
| Contacts | Test lead, university incident lead, application owner, identity owner, payment owner, legal/privacy contact, and 24x7 emergency number | Ensures a sensitive finding reaches someone able to contain it. |

The legal reason for this formality is direct. Section 43 begins with acts performed "without permission" and includes obtaining access, copying or extracting data, introducing contaminants, disrupting resources, denying authorized access, facilitating unauthorized access, and altering or destroying information [11]. Section 66 adds criminal exposure when a Section 43 act is done dishonestly or fraudulently, with punishment that may extend to three years, a fine up to five lakh rupees, or both [11]. Section 66C covers dishonest or fraudulent use of another person's password or unique identification feature [11], while Section 66D covers cheating by personation through a computer resource [11].

These provisions do not turn this report into legal advice, and a technically "good faith" motive does not replace permission. Do not use borrowed credentials, impersonate a real student or employee, obtain another person's one-time code, or represent yourself as university staff. Authorization should be specific enough that a reviewer can distinguish every planned request from an act outside permission.

**Section insight:** The safest technical control is organizational: written scope converts an ambiguous interaction with a public portal into a bounded university-directed assessment.

## Priority Matrix: Authorization and Business Logic Lead

Priority combines plausible impact, reachability, value of the evidence, and the chance that testing itself causes harm. "Expected evidence" means the minimum defensible proof, not permission to escalate.

| Priority | Vulnerability class | Risk | Non-destructive test method | Expected evidence |
|---:|---|---|---|---|
| 1 | Horizontal/vertical authorization, forced browsing, IDOR, document downloads | Critical/High | Use two synthetic accounts; replay a GET or no-op request under the other session; check logged-out and lower-role access to approved MVC routes | Unauthorized 200 response or private object content where 401/403/not-found is expected; no real third-party data retained |
| 2 | Fee payment and other business-logic integrity | Critical/High | In staging, intercept amount/currency/order references, modify one field, and stop before external authorization or settlement | Server rejects mismatch or recomputes canonical amount; vulnerable evidence is acceptance into the next state without a valid server-side check |
| 3 | Marks, timetable, notifications, profiles, role confusion | High | Compare A/B accounts and Student/Staff roles; alter only synthetic IDs or `EmailFor`/`LoginFor`; use one known canary record | Cross-user data, expanded role, or protected action obtained solely by changing a client-controlled value |
| 4 | Password reset and identity handoff | High | Confirm the destination, generic responses, token properties, rate controls, and local session invalidation using one test account | Reset cannot be enumerated or replayed; token is short-lived and single-use; no untrusted host controls reset URL |
| 5 | Session fixation and cookie controls | High | Record pre-login and post-login cookie values in the same test browser; verify renewal and logout invalidation | `ASP.NET_SessionId` or auth token changes after login; old token no longer authorizes; Secure/HttpOnly/SameSite are appropriate |
| 6 | CSRF, including login POST | High/Medium | Omit, alter, expire, and cross-session replay `__RequestVerificationToken` on a no-op test action | Invalid requests are rejected server-side; login/session-changing POST has an intentional defense |
| 7 | Login enumeration, password policy, lockout/rate limiting | Medium/High | Use one valid test username and one impossible username; tiny request count; sacrificial account for lockout | Uniform status/body/timing; server-enforced password policy; predictable throttling without broad account denial |
| 8 | Verbose errors, debug, ELMAH, Trace, legacy endpoints | Medium/High | One benign malformed input per approved parameter; single GET/HEAD to known diagnostic paths; configuration review | No remote stack trace, source path, secrets, request log, or unrestricted diagnostic console |
| 9 | `machineKey` and WebForms ViewState integrity | Critical if misconfigured, otherwise configuration risk | Review secrets/configuration; if WebForms exists, change one byte in an owned page's ViewState and expect rejection | Unique protected keys; no public/default key; MAC enforced; no forged payload execution attempted |
| 10 | WebDAV and unsafe HTTP methods | High if write-enabled | Configuration review plus one OPTIONS request; do not issue PUT/DELETE/MOVE/COPY against production | Write-capable methods absent or strongly authorized; WebDAV disabled unless required |
| 11 | Reflected HTML/XSS and open redirect | Medium/High | Use a unique inert marker and `https://example.com/`; do not use credential-stealing or persistent payloads | Correct context encoding; no arbitrary HTML interpretation; redirect destination constrained to approved origins |
| 12 | TLS and response headers | Medium | One TLS configuration scan and representative GETs for public, login, authenticated, and download responses | TLS 1.2/1.3; valid certificate; CSP/HSTS/nosniff/referrer policy; no unnecessary `X-Powered-By` |
| 13 | jQuery 1.10.2 affected code paths | Medium, context dependent | Confirm inventory/SBOM, then test only the specific Ajax or deep-merge sink with inert data | Component version plus reachable vulnerable operation; version string alone remains insufficient |
| 14 | IIS 8.3 short names and endpoint inventory | Low/Medium alone | Prefer filesystem/config review; if black-box is explicitly allowed, use a tiny paired-control request set, not a full alphabet scan | Stable response difference suggesting short-name handling, or an unexpected legacy endpoint requiring separate authorization review |

Authorization receives top priority because OWASP defines IDOR around direct, user-controlled object access without sufficient authorization [1] and recommends at least two users with different owned objects for testing [1]. Headers remain important, but OWASP describes them as controls that help reduce XSS, clickjacking, and information-disclosure risks [5], not substitutes for object-level access checks.

**Section insight:** A single proven read-only cross-user access failure is more decision-relevant than dozens of low-impact version banners. Stop after the minimum evidence needed to reproduce and fix it.

## Identity, Session, CSRF, and MVC Authorization

### Login enumeration, password policy, and rate controls

Treat `data-val-required` as a client-side usability marker. It can reveal field names and browser validation rules, but it does not establish user enumeration or server-side enforcement. Disable browser-side validation in an intercepting proxy and send four tightly controlled cases: empty identifier, impossible identifier plus wrong password, valid test identifier plus wrong password, and valid test credentials. Record status, redirect location, body length, normalized message, response time band, cookies, and whether a CAPTCHA or throttle appears. OWASP's procedure likewise compares a valid user with wrong password against an invalid user with wrong password and investigates any material response difference [2].

Do not statistically time hundreds of attempts. Two or three repetitions per case at approximately one request every several seconds are enough to identify obvious divergence without turning the test into credential guessing. A vulnerability exists when the server response lets a reasonable observer distinguish account existence. A generic browser-side "required" message generated before submission is not server-side evidence.

Test password policy through configuration/unit review first. On production, use only a dedicated test account and a change/reset request designed to be rejected, then stop before committing a new credential. Validate minimum length, breached/common-password rejection, maximum-length handling, Unicode acceptance if supported, and consistency between browser and server. Do not attempt lists of common passwords or reuse a real password. If full enforcement requires changing the account, perform it in staging or obtain explicit permission for a disposable account and restore it through the approved owner.

For lockout, OWASP says the tester needs an account that can safely be locked and recommends leaving the test until the end if only one account exists [24]. Establish the approved threshold in advance, send incorrect passwords to the sacrificial account only, and stop at the first visible throttle or lock. OWASP notes that 5 to 10 unsuccessful attempts is a typical threshold, but the correct portal setting is risk-based rather than a universal requirement [24]. Never distribute attempts across many usernames.

### Session fixation and CSRF

Capture the anonymous `ASP.NET_SessionId`, authenticate as the test user, and compare the post-login session and authentication cookies. Also compare after any authorized role elevation. OWASP requires renewal after a privilege-level change [3], recommends Secure cookies for TLS-only transport [3], HttpOnly to block DOM access [3], and Strict or Lax SameSite protection according to the application's needs [3]. Log out, then replay one harmless GET with the old cookies; expected evidence is rejection or a new anonymous session. Do not transplant a token into another person's browser.

For `__RequestVerificationToken`, first confirm both the form token and corresponding cookie/session relationship. On an approved no-op POST, test four variants: missing token, one-character mutation, a token from the second test session, and an expired token after logout. ASP.NET anti-CSRF guidance calls for tokens tied to the authenticated user's session and validation of the submitted form value [21]. Each invalid variant should fail before business logic runs.

The login POST deserves an explicit decision. Login changes browser identity and can be abused for login CSRF even though the victim starts unauthenticated. Use two researcher-controlled accounts and browsers: attempt to submit account A's login request from browser B without a valid token, then confirm that no unintended session is created. Do not send a login form to a real user.

### Forced browsing, routes, IDOR, and downloads

Build a small approved route matrix for `/Home/Index`, `/Student/*`, `/Staff/*`, and `/Account/*`. For each exact route, issue at most one GET while logged out, as Student A, Student B, and Staff A. Do not recursively fuzz controllers or invoke POST/DELETE actions. Record 200/302/401/403/404, response size, and whether the body contains protected data. A 302 to login or indistinguishable not-found response can be appropriate; a 200 shell is not necessarily vulnerable unless protected capability or data appears.

For IDOR, OWASP recommends mapping every location where user input references an object, changing that reference, and using at least two users to cover different owned objects [1]. Create record A under account A and record B under account B. Replay only A and B's identifiers across the sessions. Test route segments, query strings, form fields, JSON IDs, composite keys, and document identifiers. For downloads, prefer HEAD if authorization executes identically; otherwise use a small Range GET for the test document. Do not guess neighboring production IDs. Expected secure behavior is 403, 404, or a sanitized response with no cross-user content.

**Case study:** Student A can open `/Student/Document/Download/TA-001`, while Student B owns `/Student/Document/Download/TB-001`. Replaying `TB-001` under A is sufficient. If B's synthetic document is returned, preserve only headers and a hash or a prearranged canary phrase, then stop. OWASP's two-session method treats identical private data or success on the other user's resource as evidence of lateral authorization failure [26].

**Section insight:** The governing pattern is two accounts, two owned objects, one changed variable, one request, and an immediate stop after proof.

## ASP.NET MVC 5, IIS 10, and Legacy Endpoint Misconfiguration

### Error, debug, and diagnostic exposure

Use one benign malformed value on an existing, approved parameter, such as a non-numeric string where a numeric test ID is expected. Do not send traversal, template, SQL, or deserialization payloads merely to provoke an exception. A secure production response contains a generic error and correlation ID while detailed diagnostics remain in protected logs. Microsoft defines `customErrors="Off"` as disabling custom errors, `On` as enabling them, and `RemoteOnly` as presenting custom errors remotely while retaining detailed ASP.NET errors locally [30]. Review IIS `httpErrors` as well as ASP.NET `customErrors`, because either layer can determine the visible response.

Review deployment configuration for `<compilation debug="false">`. Do not infer `debug=true` from a slow response alone. Confirm it through authorized configuration review, build artifacts, or a clear debug-specific response. Report source paths, framework versions, stack frames, SQL details, secrets, or configuration fragments as sensitive evidence, but redact them from broad distribution.

Send one GET or HEAD to `/elmah.axd` and `/trace.axd`. If either returns a protected 401/403/404, stop. ELMAH disables remote access by default, but it can be enabled with `allowRemoteAccess`; when enabled, its own guidance says to secure the handler through ASP.NET authorization for specific users or roles [28]. If a diagnostic page is exposed, capture its title and access-control result, not every logged exception. Do not browse request bodies, cookies, or student identifiers.

### WebDAV, short names, and legacy handlers

Start with configuration review. Microsoft states that IIS WebDAV publishing requires the WebDAV module and authoring rules before users or groups can publish content [22]. In black-box testing, send one OPTIONS request to the site root and one approved application path. The presence of DAV headers or verbs is a lead, not proof of unauthorized write access. Do not issue PUT, DELETE, MOVE, COPY, LOCK, UNLOCK, or a body-bearing PROPPATCH against production. If read-only PROPFIND is needed, it must be separately authorized and limited to a synthetic directory.

For IIS 8.3 short-name behavior, avoid automated character-by-character enumeration. Prefer checking whether short-name creation is disabled on the volume and whether the request filtering configuration rejects tilde patterns. If a black-box check is expressly authorized, use a very small paired-control set against a known synthetic filename and an impossible control, with no more than 10 to 20 requests at about one request per second. A stable status or timing difference is enough to open a configuration finding; do not continue reconstructing names.

For `.aspx`, `.asmx`, and `.svc`, inventory source, deployment manifests, IIS handler mappings, application routes, JavaScript references, documentation, and logs before network discovery. Then send HEAD or GET only to exact approved candidates. If limited discovery is authorized, use a curated list of perhaps 20 organization-provided paths at low rate, not a generic internet-scale wordlist. An endpoint's existence is not automatically a vulnerability; test its authentication, authorization, methods, and data exposure separately.

### `machineKey` and ViewState

The .NET Framework `MachineKey` class uses the same algorithms and key material as ASP.NET Forms Authentication and ViewState and exposes protect/unprotect operations [19]. Review configuration for public examples, copied keys, repository exposure, weak algorithms, and unsafe sharing across unrelated applications. Never prove a bad key by forging an admin cookie or creating a deserialization payload. The safe evidence is the configuration value's provenance and a hash/redacted fingerprint, followed by rotation.

ViewState applies only if WebForms pages exist; MVC pages do not acquire ViewState merely because the application uses .NET Framework. Detect a WebForms page through an approved GET and the presence of `__VIEWSTATE` or related fields. Check configuration and change one byte in the test page's ViewState, expecting server-side MAC validation failure without state change. Microsoft's documentation says `EnableViewStateMac` should never be false in production, even where a page does not use ViewState, because the MAC protects other ASP.NET functions as well (exact URL in References). Do not use gadget chains or payload generators.

**Section insight:** Configuration inspection produces stronger and safer evidence than exploit demonstration for diagnostics, WebDAV, `machineKey`, and ViewState.

## Web Layer: Headers, TLS, Redirects, Encoding, Reset, and jQuery

Collect headers from four representative responses: public landing page, login page, authenticated page, and document download. Remove `X-Powered-By` and unnecessary `Server` detail; OWASP specifically recommends removing `X-Powered-By` headers [5]. Evaluate CSP by actual page needs, not by mere presence. Check HSTS only over HTTPS, `X-Content-Type-Options: nosniff`, an appropriate `Referrer-Policy`, frame protection through CSP `frame-ancestors`, and `Cache-Control: no-store` for sensitive records. OWASP provides `nosniff` and `strict-origin-when-cross-origin` as recommended examples [5] and gives a strong HSTS example with `includeSubDomains` and `preload` [5]. Do not recommend preload until every subdomain is confirmed HTTPS-ready.

TLS validation should confirm a valid certificate chain and hostname, TLS 1.2 and preferably TLS 1.3, rejection of obsolete protocols, secure renegotiation, and appropriate cipher suites. TLS provides confidentiality, integrity, and server authentication when correctly implemented [4]. Use one authorized configuration scan, avoiding stress or repeated handshake testing.

For open redirects, test approved parameters such as `returnUrl`, `redirect`, `next`, or `continue` with `https://example.com/`, a reserved harmless destination. OWASP's method is to identify URL-handling injection points and determine possible destinations [14]. The secure result rejects the value or resolves it to a local allowlisted path. Do not use a lookalike university domain.

For reflected HTML injection, send a unique inert marker such as `MUJTEST-7F3C` and harmless metacharacters, then inspect raw HTML and the parsed DOM. Start without executable script. If the marker is reflected, determine its context and whether characters are encoded. Only in staging, and only if explicitly approved, may a harmless execution proof such as setting a local DOM attribute be used. Reflected XSS is non-persistent and affects users who open a crafted request [32]; never send such a URL to another person.

The brief states that password reset links go to `passwordreset.microsoftonline.com`, Microsoft's work/school password-reset portal. Treat that as an identity-boundary observation, not proof that every portal account is fully managed by Entra ID. Verify the exact HTTPS destination, tenant branding, generic local response, and absence of an open redirect. Use one test account. OWASP says reset tokens should be CSPRNG-generated and sufficiently long, with at least 128 bits offered as a practical minimum [23], short-lived [23], single-use [23], and protected against automated requests [23]. Do not trigger reset messages for unconsenting users.

Finally, jQuery 1.10.2 is old enough to fall within two relevant affected ranges. CVE-2015-9251 affects versions before 3.0.0 when a cross-domain Ajax request without `dataType` executes a `text/javascript` response [17]. CVE-2019-11358 affects versions before 3.4.0 when unsafe deep extension processes an enumerable `__proto__` property [10]. Upgrade to a supported 3.x release after compatibility testing, but do not label the portal exploitable unless the corresponding sink and attacker influence are demonstrated.

**Section insight:** Separate baseline hardening from exploitability. A missing header or old library raises risk; a reachable unsafe sink establishes a vulnerability.

## Business Logic: Fees, Marks, Notifications, Profiles, and Roles

OWASP models business-logic abuse around workflows, state transitions, and decisions rather than only malformed syntax [13]. Build a state diagram for each flow: prerequisites, actor, server-side object, allowed transition, external side effect, and rollback. Then test only transitions that cannot charge money, alter academic records, send bulk messages, or expose a non-test person's data.

### Fee payment integrity

Use a payment sandbox or university-approved test merchant. Capture the request before gateway redirection and identify client-visible fields such as amount, currency, fee head, order ID, student ID, return URL, and signature. Change exactly one field, send it only to the pre-authorization validation step, and stop. Never complete 3-D Secure, authorize a card, forge a gateway callback, replay a settled order, or test a live merchant without the payment provider's separate permission.

The expected secure design derives amount and currency from a server-side fee record, binds the order to the authenticated student, signs or otherwise protects gateway parameters, reconciles the callback against the original order, and enforces idempotency. Evidence of risk is the application accepting a changed value into the next server-side state, not merely displaying an editable hidden field. If production cannot provide a safe pre-commit boundary, verify the behavior through unit/integration tests and code review instead.

### Marks, timetables, notifications, and profiles

For marks and timetables, create records for Student A and Student B. Replay B's synthetic course, term, or student identifier under A. Do the same across Staff and Student roles using read-only requests. Stop on the first cross-user result. IDOR exists when user input retrieves another object without sufficient authorization [1]; sequential or GUID identifiers are neither secure nor insecure by themselves.

For notifications, use two synthetic notifications with known IDs. Request only A and B's IDs across the paired accounts. Do not iterate a numerical range. A 404 that is indistinguishable from a nonexistent record may be safer than revealing whether another user's notification exists.

For profile autocomplete or APIs, insert a unique canary profile into staging. Query only its exact prefix plus one impossible control. Record whether unauthenticated, Student, and Staff sessions receive different approved fields. Do not enumerate alphabetic prefixes, paginate the directory, or retain returned personal data. Secure output should minimize fields and enforce purpose-based authorization on every request.

### Student/Staff/Admin role confusion

Treat `EmailFor` and `LoginFor` as attacker-controlled hints. With one test identity, alter Student to Staff or Admin in the hidden field while keeping credentials unchanged. The server should derive role and tenant from an authoritative identity/authorization store, reject the mismatch, and never issue stronger claims because of a client field. Also test whether the visible login tabs call different server endpoints or only restyle the same request.

**Case study:** A Student test account submits its valid username/password while `LoginFor=Staff`. If authentication succeeds only as Student, the hidden field is cosmetic or safely constrained. If the same identity receives Staff navigation but every Staff API returns 403, the defect is UI confusion rather than a complete privilege escalation. If a protected Staff GET returns synthetic Staff data, preserve that single response and stop. This staged interpretation prevents overstating a cosmetic issue while still detecting a real vertical bypass.

**Section insight:** Client-controlled prices, identifiers, and role labels are test inputs, never trust anchors. The server must re-derive every consequential value.

## India Disclosure Path: MUJ First, CERT-In Coordination Second

### Step 1: Contain and document

Stop testing after minimum proof. Preserve UTC timestamp, approved source IP, affected route, role, request/response pair, business impact, reproduction prerequisites, and a redacted evidence hash. Remove passwords, full cookies, student names, marks, document contents, and payment data. Do not upload evidence to a public paste service or issue tracker.

Score severity from demonstrated impact and exploit preconditions, not scanner labels. Distinguish "old component detected" from "affected code path reachable," and "route returns 200" from "protected data disclosed." Include a safe remediation test and request an encrypted transfer channel for sensitive attachments.

### Step 2: Notify the university privately

Send the report to the security/IT contact named in the authorization. If no dedicated PSIRT or security address is provided, use a formally accountable university route and request internal forwarding. MUJ's official page lists Dr Amit Soni, Registrar, phone `+91 141-3999100`, extension `102`, and `registrar@jaipur.manipal.edu`; it also states that the Registrar can receive complaints and suggestions concerning administration [16]. Do not infer that this is a dedicated security mailbox. The authorization owner should ideally name a technical incident contact before testing begins.

The initial message should include:

1. "Confidential security report" in the subject.
2. The written authorization or engagement identifier.
3. A one-paragraph impact summary.
4. Exact affected asset and test account roles.
5. Minimal reproduction steps.
6. Redacted request/response evidence.
7. Confirmation that testing stopped and no persistence or real data was retained.
8. Suggested containment and durable remediation.
9. Proposed acknowledgment, triage, fix, and retest dates.
10. Researcher contact and encryption preference.

Ask for acknowledgment within two business days for critical issues and five business days otherwise. Those are operational recommendations, not statutory deadlines.

### Step 3: Use CERT-In for coordination or a real incident

CERT-In's official site is `https://www.cert-in.org.in/`, and its Responsible Vulnerability Disclosure and Coordination Policy is at `https://www.cert-in.org.in/RVDCP.jsp`. The page identifies an official policy for responsible vulnerability disclosure and coordination [25]. Use that route when the university cannot be reached, multiple Indian organizations or vendors are affected, coordinated publication is required, or the finding has national/sector significance.

A vulnerability report is not automatically a cyber incident. If testing reveals evidence of ongoing compromise, data exfiltration, malware, or an active attack, stop and notify the university incident lead immediately so the legally responsible organization can make any required CERT-In incident report. Do not investigate the attacker, access suspected stolen data, or expand scope on your own.

### Step 4: Coordinate a 90-day remediation window

A practical schedule is day 0 private report, day 2 acknowledgment target, day 7 triage, day 30 remediation plan, day 60 status/retest preparation, and day 90 resolution or an agreed extension. Project Zero's published policy gives vendors 90 days to patch and, if patched within that period, discloses details 30 days after the patch [7]. It also permits a requested 14-day grace period in defined circumstances [7] and shortens the timetable for vulnerabilities exploited in the wild [7].

That is a prominent industry policy, not a rule that compels a university researcher to publish exploit details. Public disclosure should be jointly timed, minimize weaponizable detail, confirm that students can update or are protected, and account for examinations, admissions, and payment periods. If remediation is delayed but users remain at risk, escalate privately through university leadership, the authorized nodal path, and CERT-In rather than dropping a live exploit.

### Platforms and training environments

Do not conflate adjacent services:

- **CERT-In** is India's national incident-response and vulnerability-coordination body, not blanket authorization to test an arbitrary Indian website.
- **HackerOne Hacktivity** is a public/community feed of disclosed program activity, not a scope grant for MUJ. Only a named HackerOne program policy could authorize testing.
- **TryHackMe-style labs and academic cyber ranges** authorize activity only inside their stated lab assets. TryHackMe's own vulnerability-disclosure or bounty rules do not cover a university portal.
- **Indian bug-bounty aggregators or private platforms** can help discover programs, but authorization comes from the asset owner's current program scope and terms, not from directory inclusion.

**Section insight:** The defensible path is authorization -> minimum proof -> confidential owner report -> CERT-In coordination where appropriate -> controlled retest -> carefully timed disclosure.

## Synthesis: Three Test Modes, Different Evidence and Risk

| Dimension | Black-box production test | Gray-box test with synthetic accounts | Configuration/code review |
|---|---|---|---|
| Best use | Headers, TLS, generic errors, route access result | IDOR, role boundaries, sessions, CSRF, marks, notifications, profile APIs | `machineKey`, ViewState, debug, WebDAV, payment calculations, authorization filters |
| Evidence strength | Shows externally observable behavior | Shows actor/object relationship and reproducible authorization failure | Shows root cause and systemic extent |
| Operational risk | Medium if fuzzing or lockout is uncontrolled | Low when records are synthetic and rate is bounded | Lowest for dangerous cryptographic and write-capable controls |
| Main limitation | A 200 or banner may be ambiguous | Requires carefully provisioned identities and data | May miss deployment drift or proxy/IIS behavior |
| Stop rule | Stop at sensitive output or instability | Stop at first cross-account proof | Do not export secrets; record redacted fingerprints |

The major tension is between realism and safety. A live payment completion would be realistic but creates financial and record-integrity risk; a staging transition or code-level invariant provides safer evidence. Likewise, forging a cookie with a leaked `machineKey` could demonstrate catastrophic impact, but the configuration exposure already proves the control failure and permits immediate rotation. More exploitation would add harm, not decision value.

A second tension is between defense-in-depth and root controls. CSP, HSTS, `nosniff`, and dependency upgrades matter, but they cannot repair an endpoint that returns Student B's marks to Student A. Conversely, strong object authorization does not make verbose stack traces or an exposed ELMAH log acceptable. The correct program sequences work by expected loss: authorization and payment integrity first, identity/session second, diagnostics and platform configuration third, and baseline headers/inventory throughout.

A third tension is between disclosure speed and student protection. A fixed 90-day benchmark creates accountability, while automatic publication can expose an unpatched academic system. The solution is a documented timeline with escalation, retesting, and explicit publication criteria. The 90-day model should motivate progress, not replace judgment.

### Transparent decision rationale

The prioritization uses four explicit factors: potential harm, likelihood of reachability, confidence produced by a small test, and risk created by the test itself. That is why two-account IDOR and role checks rank above 8.3 enumeration, and why configuration review outranks exploitation for `machineKey` and ViewState. This is a concise decision rationale, not private chain-of-thought.

**Synthesis insight:** Use black-box requests to confirm externally visible boundaries, gray-box accounts to prove actor/object authorization, and configuration review for controls whose exploitation would be dangerous. No single method is sufficient by itself.

## VERDICT

**Verdict: GO only with signed university authorization and synthetic test identities; otherwise NO-GO.**

For an authorized ASP.NET MVC 5 / .NET Framework 4.x / IIS 10 portal, the first testing wave should cover: (1) horizontal/vertical authorization and downloads, (2) fee and academic-record business logic, (3) session renewal and CSRF, and (4) identity/reset controls. The second wave should cover error/debug/diagnostic exposure, WebDAV and legacy handlers, cryptographic configuration, ViewState if WebForms exists, and old client dependencies. Headers, TLS, redirects, and reflected injection should run as a representative-response baseline, not as a substitute for authorization testing.

The exercise is not authorized merely because the portal is public, the researcher is a student, CERT-In has a disclosure policy, or a bounty platform lists similar programs. Written scope from MUJ or a legally empowered delegate is the controlling prerequisite. Under the IT Act, permission is central to Section 43, while dishonest or fraudulent Section 43 conduct can engage Section 66 [11].

**Confidence: High (0.89)** for the prioritization, non-destructive methodology, ASP.NET/IIS control model, and statutory quotations. **Confidence: Moderate (0.74)** for the institution-specific disclosure route because the official Registrar contact is verified, but no dedicated MUJ PSIRT or public vulnerability-disclosure policy was established in the reviewed material. The engagement owner should obtain a named technical security contact before testing.

## References

1. *WSTG - Latest | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References
2. *WSTG - Latest | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/03-Identity_Management_Testing/04-Testing_for_Account_Enumeration_and_Guessable_User_Account
3. *Session Management - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
4. *Transport Layer Security - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html
5. *HTTP Headers - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html
6. *Cert-In - Home Page*. http://cert-in.org.in/SecurityIncident.jsp
7. [
    
      Vulnerability Disclosure Policy - Project Zero
    
  ](https://projectzero.google/vulnerability-disclosure-policy.html)
8. *Code injection attacks using publicly disclosed ASP.NET machine keys | Microsoft Security Blog*. https://www.microsoft.com/en-us/security/blog/2025/02/06/code-injection-attacks-using-publicly-disclosed-asp-net-machine-keys
9. * Security Bulletin: API Connect is vulnerable to JQuery Cross-Site Scripting (XSS) and other vulnerabilities (CVE-2012-6708, CVE-2015-9251, CVE-2019-11358, CVE-2020-11022, CVE-2020-11023)*. https://www.ibm.com/support/pages/security-bulletin-api-connect-vulnerable-jquery-cross-site-scripting-xss-and-other-vulnerabilities-cve-2012-6708-cve-2015-9251-cve-2019-11358-cve-2020-11022-cve-2020-11023
10. *NVD - CVE-2019-11358*. https://nvd.nist.gov/vuln/detail/CVE-2019-11358
11. *THE INFORMATION TECHNOLOGY ACT, 2000 ––––––––– ARRANGEMENT OF SECTIONS –––––––––*. https://www.indiacode.nic.in/bitstream/123456789/13116/1/it_act_2000_updated.pdf
12. *Business logic vulnerability | OWASP Foundation*. https://owasp.org/www-community/vulnerabilities/Business_logic_vulnerability
13. *OWASP Top 10 for Business Logic Abuse | OWASP Foundation*. https://owasp.org/www-project-top-10-for-business-logic-abuse
14. *WSTG - v4.2 | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/11-Client-side_Testing/04-Testing_for_Client-side_URL_Redirect
15. *OWASP Payment Security Testing Guide | OWASP Foundation*. https://owasp.org/www-project-payment-security-testing-guide
16. *Registrar - Manipal University Jaipur*. https://www.jaipur.manipal.edu/administration-registrar.php
17. *NVD - CVE-2015-9251*. https://nvd.nist.gov/vuln/detail/CVE-2015-9251
18. *Authorization - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
19. *MachineKey Class (System.Web.Security) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.security.machinekey?view=netframework-4.8.1
20. *WSTG - v4.1 | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/v41/4-Web_Application_Security_Testing/08-Testing_for_Error_Handling/02-Testing_for_Stack_Traces
21. *Anti CSRF Tokens ASP.NET | OWASP Foundation*. https://owasp.org/www-community/Anti_CRSF_Tokens_ASP-NET
22. *WebDAV &lt;webdav&gt; | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/configuration/system.webserver/webdav
23. *WSTG - Latest | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/09-Testing_for_Weak_Password_Change_or_Reset_Functionalities
24. *WSTG - v4.1 | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/v41/4-Web_Application_Security_Testing/04-Authentication_Testing/03-Testing_for_Weak_Lock_Out_Mechanism
25. *RVDCP*. https://www.cert-in.org.in/RVDCP.jsp
26. *WSTG - Latest | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/02-Testing_for_Bypassing_Authorization_Schema
27. [
      ScottGu's Blog - Don’t run production ASP.NET Applications with
      debug=”true” enabled
    ](https://weblogs.asp.net/scottgu/442448)
28. *ELMAH—Securing Error Log Pages*. https://elmah.github.io/a/securing-error-log-pages/
29. *NIST SP 800-115, Technical Guide to Information Security Testing and Assessment*. https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=152164
30. *CustomErrorsMode Enum (System.Web.Configuration) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.configuration.customerrorsmode?view=netframework-4.8.1
31. *http://csrc.nist.gov/pubs/sp/800/115/final*. http://csrc.nist.gov/pubs/sp/800/115/final
32. *WSTG - v4.1 | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/v41/4-Web_Application_Security_Testing/07-Input_Validation_Testing/01-Testing_for_Reflected_Cross_Site_Scripting
