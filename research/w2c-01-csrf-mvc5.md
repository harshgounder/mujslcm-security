# MUJ SLCM CSRF Assurance for ASP.NET MVC 5

## Executive Summary

- **Present posture is indeterminate, not proven vulnerable**: The supplied scope identifies `https://mujslcm.jaipur.manipal.edu/`, ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, Microsoft 365 identity, and an observed `__RequestVerificationToken` cookie-plus-field pair. This research did not actively test MUJ, so those implementation details remain user-supplied observations rather than independently verified facts. The existence of the two tokens is encouraging, but only server-side rejection tests can establish protection.

- **Native MVC requires a correlated pair**: Classic ASP.NET MVC sends one request-verification token in a cookie and another in a hidden field; requests lacking either should be rejected [9]. The two are not interchangeable: source code marks the cookie token as a session token, marks the form token as a non-session token, and requires their embedded 128-bit security values to match [26]. MUJ should verify this full invariant on every unsafe action, not merely check that a parameter named `__RequestVerificationToken` exists.

- **MachineKey provides more than a bare HMAC comparison**: MVC 5.3's implementation serializes the token data and calls `MachineKey.Protect` and `MachineKey.Unprotect` with the dedicated purpose `System.Web.Helpers.AntiXsrf.AntiForgeryToken.v1` [7]. Microsoft describes `MachineKey` as encrypting or hashing data, or both, and `Protect` as encrypting or signing it [8]. Therefore, describing the token as a simple machine-key HMAC is incomplete; it is an opaque, purpose-bound, authenticated protected value whose exact algorithms depend on .NET and `machineKey` configuration.

- **Reuse is expected, but theft extends replay opportunity**: OWASP permits a CSRF token to be generated once per session or once per request [17]. MVC reuses a valid cookie token and the serialized model has no timestamp or expiration field [14][39]. **Inference:** reuse within the same authenticated identity is not itself a bypass, but a stolen valid pair can remain replayable until another boundary, such as identity change, cookie replacement, logout policy, key rotation, or custom additional-data validation, makes it invalid.

- **Cookie-only acceptance would indicate a defect**: Native MVC should reject a missing form token, a missing cookie token, swapped token types, mismatched embedded security values, and a form token bound to another authenticated identity [26]. A handler that accepts only the anti-forgery cookie, duplicates a cookie value into a request parameter, or validates against an unrelated cookie has replaced the framework invariant with a weaker construction. Signed double-submit defenses should be explicitly bound to the authenticated session; naive double-submit designs are bypassable when an attacker can set a target-domain cookie [17].

- **Sibling subdomains are a conditional risk, not an automatic MVC bypass**: RFC 6265 states that a cookie's `Domain` controls the hosts to which it is sent and that cookies do not provide integrity guarantees against sibling domains [16]. Microsoft also warns that applications sharing a domain implicitly trust one another's cookie-setting ability [15]. **Inference:** a sibling host able to plant a cookie still cannot forge a valid MVC field token without the relevant MachineKey or another valid-token source, but parent-domain cookie scope, duplicate-name parsing, shared keys, or a cookie-only custom handler can turn that capability into a practical bypass.

- **JSON requires an explicit design**: The classic token store reads the request token from `Request.Form`, not from an arbitrary JSON property [3]. Microsoft recommends transporting the pair in a custom HTTP header for Web API-style requests and then calling `AntiForgery.Validate` [9]. MUJ should test every JSON or AJAX action independently and should not assume that placing `__RequestVerificationToken` inside JSON activates the MVC attribute.

- **Local login CSRF and Microsoft identity CSRF are separate controls**: Microsoft states that the built-in ASP.NET anti-XSRF routines do not by themselves prevent login XSRF [15]. For Microsoft identity authorization-code flows, the application should generate a random `state` value and verify that the returned value is identical [35]; OpenID Connect `nonce`, PKCE where applicable, or a one-time user-agent-bound `state` provides protocol-level correlation [29]. MUJ should test local credential forms with local anti-forgery controls and identity callbacks with OAuth/OIDC correlation rather than treating either mechanism as a substitute for the other.

- **Akamai and SameSite are defense-in-depth concerns**: `SameSite` is only partial CSRF protection [28], and some OIDC or WS-Federation flows use POST-based redirects that can conflict with restrictive cookie settings [36]. A response carrying a cookie can still be cached under HTTP semantics [16], while `Cache-Control: no-store` explicitly prevents storage [25]. Token-bearing and personalized pages should therefore be tested for shared-cache isolation, correct cookie attributes, and successful identity redirects.

**Decision-ready insight:** Do not classify MUJ SLCM as safe merely because the cookie and field are visible, and do not classify it as vulnerable merely because tokens are reusable. The decisive evidence is an authorized negative-test matrix showing that every state-changing endpoint rejects absent, swapped, mismatched, cross-identity, wrong-transport, and cross-site requests before any state change.

## Scope, Evidence Boundaries, and Reproducible Reasoning

This is a defensive public-information assessment for a university security club. It does not authorize testing. Any live validation should occur only under written university authorization that names the hosts, dates, accounts, permitted request classes, data-handling rules, rate limits, and rollback contacts. Testers should use institution-provided test accounts and benign, reversible actions. They should not use another student's account, attempt credential capture, defeat access control, obtain another person's token, or test payment and academic-record changes without explicit approval.

I cannot provide private hidden chain-of-thought. Instead, the report gives a reproducible evidence-to-conclusion rationale: the observed or supplied fact, the relevant framework invariant, the target-specific inference, and the exact result that would confirm or refute it. This is more useful for peer review because each conclusion has a stated evidentiary threshold.

| Scope fact | Evidence status | What can be concluded | What cannot be concluded |
|---|---|---|---|
| `https://mujslcm.jaipur.manipal.edu/` | User-supplied scope and publicly reachable entry-point URL | It is the host to include in an approved inventory. | No vulnerability, route coverage, or configuration conclusion follows from the URL alone. |
| ASP.NET MVC 5.3 on .NET Framework 4.x | User-supplied fingerprint; package existence independently corroborated | NuGet lists `Microsoft.AspNet.Mvc 5.3.0` and says it targets .NET Framework 4.5 or higher [38]. | A public package listing does not prove the exact assembly loaded by MUJ. |
| IIS 10 behind Akamai | User-supplied observation | Edge caching, TLS termination, forwarding, and multi-node consistency belong in the test plan. | This report does not infer any Akamai rule, origin topology, or IIS weakness. |
| Microsoft 365 identity | User-supplied observation | OAuth/OIDC `state`, `nonce`, callback, and SameSite behavior should be assessed separately from local MVC form tokens [29][35]. | The exact protocol, tenant, client library, and callback mode are not established here. |
| `__RequestVerificationToken` in a cookie and form field | User-supplied browser observation consistent with MVC | The names and placement match Microsoft's two-token model [9]. | Presence does not prove that the action invokes validation or that the pair is correctly bound. |
| Actual CSRF status | Not tested | A safe, exact validation plan can be specified. | The current evidence cannot support “vulnerable” or “not vulnerable.” |

### Evidence-to-conclusion rationale

| Observation | Framework or standards rule | Target-specific inference | Decisive authorized test |
|---|---|---|---|
| Cookie and field share a familiar name | MVC requires both tokens, not merely a familiar name [9]. | **Inference:** MUJ may use native MVC or a custom look-alike implementation. | Independently omit each token and verify rejection before action execution. |
| Tokens can be reused | Per-session generation is an accepted pattern [17]. | **Inference:** reuse alone is not a finding; cross-session or cross-identity acceptance may be. | Reuse only across controlled boundaries and record which boundary invalidates the token. |
| A Microsoft identity option is present | Microsoft identity uses random `state` with equality validation [35]. | **Inference:** the identity callback may legitimately be cross-site and may not use MVC's form-token mechanism. | Verify protocol correlation without replaying real authorization codes or tokens. |
| An edge CDN is present | Shared caches follow cache directives, and `no-store` prevents storage [25]. | **Inference:** tokenized HTML could be mishandled if an edge rule overrides origin privacy. | Compare authorized test sessions for cache status, token isolation, and response directives. |

**Section insight:** The public evidence establishes how MVC should behave, not how MUJ currently behaves. Every MUJ-specific security conclusion below is therefore either an explicit test recommendation or labeled **Inference**.

## How MVC 5 Builds and Validates the Token Pair

ASP.NET MVC's classic anti-forgery facility implements a variant of the synchronizer-token pattern. The browser receives a session-style token in an HTTP cookie and a request token in a hidden form field. On submission, the server extracts both protected payloads and permits the action only after the pair and, when applicable, the current identity pass validation [15].

### Exact token lifecycle

| Stage | Native MVC 5 behavior | Security consequence |
|---|---|---|
| 1. Render a protected form | `Html.AntiForgeryToken()` produces a hidden input; generation may also set a response cookie [14]. | The view and the receiving action are both part of the control. Rendering a field without validating it is cosmetic. |
| 2. Reuse or create the cookie token | If a valid cookie token exists, MVC uses it; otherwise it generates and persists a new token [14]. | Multiple forms can legitimately correlate to one cookie token. Cookie-value stability is not, by itself, a defect. |
| 3. Generate entropy | `AntiForgeryToken` uses a random 128-bit security value, and `BinaryBlob` fills its data with `RNGCryptoServiceProvider` [2][24]. | Guessing a valid native token should not be feasible absent a cryptographic or key-management failure. |
| 4. Build the request token | MVC copies the cookie token's security value into a non-session form token and adds username or claim UID plus optional additional data [26]. | The request token is correlated to both the cookie token and, after authentication, the current identity. |
| 5. Serialize | Version 1 serializes the security token, the session-token flag, either claim UID or username for non-session tokens, and additional data [39]. | The payload has structure, but callers should treat its protected representation as opaque. No timestamp appears in this format. |
| 6. Protect | MVC calls `MachineKey.Protect` with the unique purpose string `System.Web.Helpers.AntiXsrf.AntiForgeryToken.v1`, URL-token-encodes the result, and reverses the process with `Unprotect` [7]. | A value protected for another subsystem or purpose cannot simply be substituted. Tampering should fail cryptographic validation. |
| 7. Store and submit | The token store reads the cookie by configured cookie name and the request token from the configured `Request.Form` field; the saved cookie is `HttpOnly`, and `Secure` is set when `RequireSSL` is enabled [3]. | JSON is not automatically covered, and production must verify actual `Secure`, `SameSite`, `Domain`, and `Path` attributes at the wire. |
| 8. Validate structure | MVC requires a session-style cookie token and a non-session request token; swapped forms are rejected [26]. | “Any two decryptable tokens” is not enough. Token roles matter. |
| 9. Validate correlation | MVC compares the two embedded security values [26]. | A valid cookie from one pair and valid field from another should fail. |
| 10. Validate identity and context | MVC compares username or claim UID to the current identity and invokes the configured additional-data validator [26]. | Cross-user acceptance should fail even when two accounts are served by the same application and keys. |

### MachineKey, HMAC, encryption, and web farms

Calling the construction “machine key HMAC” captures the integrity objective but misses important implementation details. Microsoft documents `MachineKey` as exposing ASP.NET encryption and hashing logic, while `Protect` can encrypt or sign data [8]. The `MachineKeySection.Validation` property selects the hashing algorithm used to validate ASP.NET data [21]. In MVC's anti-forgery source, however, application code does not manually concatenate fields and calculate a raw HMAC. It serializes a structured token and delegates authenticated protection to `MachineKey.Protect` under a purpose-isolation string [7][22].

That distinction affects testing. Changing one character should produce a rejection, but a black-box tester cannot infer the configured validation or encryption algorithm merely from the opaque token. Key extraction, cryptographic attacks, and attempts to mint tokens are outside this club report and should never be attempted without a separate, explicit authorization.

A multi-origin or multi-worker deployment introduces an availability and consistency requirement. `MachineKey.Unprotect` can fail when a multi-server application uses auto-generated encryption keys [20], and Microsoft instructs web-farm operators to configure a consistent validation key manually [23]. **Inference:** if MUJ's origin tier has multiple IIS workers or servers behind Akamai, valid forms must work regardless of which authorized request reaches which healthy node. Intermittent anti-forgery failures can indicate inconsistent keys, deployment slots, virtual paths, or affinity, but such failures are not evidence of a bypass.

**Section insight:** Native MVC's security property is not “field exists.” It is `valid protected cookie token + valid protected request token + matching embedded random value + correct token roles + correct authenticated identity + valid optional context`.

## Known Bypass Patterns and Their Actual Relevance

The word “bypass” needs discipline. Several commonly reported patterns attack incomplete custom validation, not the native MVC invariant. The table separates a genuine framework expectation from the failure condition that creates risk.

| Pattern | Native MVC expectation | Failure condition to look for | MUJ-specific assessment |
|---|---|---|---|
| Reuse within one session | Tokens may be generated per session or per request [17]. MVC's serialized fields contain no timestamp [39]. | Treating a reusable token as proof of a vulnerability, or conversely allowing it after an identity/session boundary that policy says should invalidate it. | **Inference:** ordinary same-session reuse is likely expected. Test logout, account switch, authentication, and controlled key/deployment boundaries. |
| Token not tied to session | Cookie and request tokens must share the same embedded security value [26]. | The server accepts any token from a global pool. PortSwigger documents this flawed pattern [13]. | Reject unless the token is paired with the test browser's current cookie token and identity. |
| Cookie-only validation | Missing either native token must be rejected [9][26]. | A handler accepts the anti-forgery cookie by itself or accepts the same attacker-controlled value in cookie and parameter. | A successful state change after removing the form/header token would be a high-severity implementation defect. |
| Token tied to an unrelated cookie | Native MVC correlates its own cookie and form payloads [26]. | The application validates a token against a non-session cookie that can be planted independently. This pattern is documented in practical CSRF research [13]. | Inventory every cookie read by custom handlers; do not assume a cookie name implies authentication binding. |
| Parent-domain or sibling-subdomain cookie injection | Host scope is governed by `Domain`; sibling domains do not have cookie-integrity isolation [16]. | A sibling can plant a suitably scoped cookie and the target uses naive double-submit, ambiguous duplicate-cookie parsing, shared MachineKeys, or another valid-token oracle [17][13]. | **Inference:** cookie-setting power alone should not defeat native MVC because a valid field token is still required. Combined weaknesses change the conclusion. |
| Cookie and field swapped | Cookie token must be session-form and request token must be non-session-form [26]. | A custom validator deserializes values but does not enforce roles. | Swap only in an approved test account; any state change is a strong finding. |
| Cross-user pair | The request token carries username or claim UID and must match the current identity [26]. | Validation suppresses identity heuristics incorrectly, relies on an empty/non-unique claim, or bypasses native validation. | Use two institution-provided test identities only. Never collect another person's token. |
| Login CSRF | Microsoft's classic anti-XSRF documentation warns that the built-in routines do not themselves defend against login XSRF [15]. | A cross-site party can force the browser into an attacker-chosen account or bind the wrong external identity because login initiation/callback lacks correlation. | Test local login and Microsoft identity flows separately; do not assume a hidden MVC token proves login-CSRF resistance. |
| JSON in-body token | Native storage reads `Request.Form` [3]. | A JSON property is ignored, loosely compared, parsed inconsistently, or accepted without its cookie counterpart. | **Inference:** a JSON body named `__RequestVerificationToken` has no effect unless MUJ added a handler. Establish the handler contract from code or authorized tests. |
| Custom header | Microsoft suggests carrying the pair in a custom header and invoking `AntiForgery.Validate` [9]. | The handler checks only header presence, validates one half, trusts an arbitrary origin, or is omitted on some routes. | Verify extraction, pair splitting, native validation, failure behavior, CORS, and route coverage. |
| Unsafe GET or method gap | HTTP GET is supposed to be safe; POST alone does not solve CSRF [34]. Microsoft recommends anti-forgery tokens for nonsafe POST, PUT, and DELETE methods [9]. | A state change is reachable by GET, an alternate verb, a form-compatible content type, or a second route without validation. | Inventory behavior, not just HTML forms. Any state-mutating GET is a design finding even if `SameSite=Lax` blocks some demonstrations. |
| SameSite-only defense | SameSite restricts some cross-site cookie transmission but is only partial CSRF protection [28]. | Developers omit server-side tokens because a browser presently defaults to Lax, or they test in only one browser [34]. | Record actual attributes and test supported identity/browser scenarios; retain server-side validation. |

### Reuse: what should count as a finding

The cookie token is designed for reuse while valid. A newly rendered field token can also remain logically equivalent for validation because it contains the same shared security value and no timestamp. **Inference:** different ciphertext strings across renders do not necessarily mean one-time semantics because cryptographic protection can add variability around equivalent plaintext; conversely, identical strings do not establish insecurity.

A useful finding requires a failed boundary. Examples include acceptance after the tester logs out and establishes a genuinely new authenticated context, acceptance under a second controlled identity despite identity binding, or acceptance with a cookie from another controlled browser profile. The expected result must be defined before testing because some applications deliberately preserve an anonymous anti-forgery cookie across authentication while relying on the request token's identity binding.

### Subdomains: combined-risk model

RFC cookie scoping creates ambient trust, but MVC's cryptographic pair adds a second barrier. **Inference:** practical exploitation generally requires a combination, such as a sibling-domain cookie-setting primitive plus naive double-submit validation; two applications that share parent-domain cookies and MachineKeys; an endpoint that discloses or mints a pair; or ambiguous duplicate-cookie handling. PortSwigger notes that another application in the same overall DNS domain can sometimes set a cookie with suitable scope [13], while OWASP recommends a signed double-submit token explicitly tied to the authenticated session [17].

Therefore, the club should not report “subdomain takeover equals MVC CSRF bypass.” It should report the exact chain only if each link is authorized and demonstrated in a controlled environment. The defensive action is narrower cookie scope, unique keys and names per application, deterministic duplicate-cookie rejection, and elimination of weaker custom validators.

**Section insight:** Token reuse, subdomain scope, and JSON transport are risk multipliers only when a validation invariant is absent or crossed. The test report should identify the failed invariant rather than use a generic “CSRF bypass” label.

## Exact Authorized Test Matrix for SLCM Login

The following matrix is suitable for a staging system or a production test window explicitly approved by MUJ. Use only a tester-controlled browser, tester-controlled origin, and institution-issued test identities. Choose a login result that is easy to observe and undo. Do not automate password guessing, submit another person's credentials, or replay live Microsoft authorization codes.

| ID | Test on each local login form | Exact controlled mutation | Secure expected result | Finding if state changes or login succeeds |
|---|---|---|---|---|
| L1 | Establish baseline | Load the form normally and submit it once with the issued cookie-field pair and approved test credentials. | Login succeeds; the team records action URL, method, content type, redirects, cookie attributes, and token names. | No finding; this calibrates the workflow. |
| L2 | Missing request token | Remove only the hidden `__RequestVerificationToken` field while retaining the cookie. | Rejection before authentication state changes; MVC requires both tokens [9]. | High-confidence missing validation or route mismatch. |
| L3 | Missing cookie token | Retain the field but remove only the anti-forgery cookie in a disposable browser profile. | Rejection before authentication state changes [26]. | High-confidence incomplete validation. |
| L4 | Swapped roles | Place the field token in the cookie position and the cookie token in the field position. | Rejection because token roles differ [26]. | Custom handler may deserialize without enforcing token type. |
| L5 | Mismatched valid pair | In two isolated, tester-controlled profiles, combine cookie A with field B. | Rejection because embedded security values differ [26]. | Token pool, cookie-only, or otherwise unbound validation. |
| L6 | Tamper resistance | Change one character in one token without attempting to construct a replacement. | Rejection during unprotection or validation [7][20]. | Severe integrity-validation failure or token not actually checked. |
| L7 | Same anonymous-session reuse | Re-submit an unchanged issued pair in the same anonymous browser context. | Policy-dependent; reuse may be accepted because per-session tokens are allowed [17]. | Do not file solely because this succeeds. Record observed lifetime. |
| L8 | Pre-login to post-login boundary | After an approved test login, submit a benign protected action with a request token issued before authentication, then repeat with a freshly rendered authenticated token. | Result depends on when identity was embedded. The fresh authenticated pair must work; a pair bound to the wrong identity should fail [26]. | Cross-identity acceptance is significant; anonymous-cookie persistence by itself is not. |
| L9 | Controlled login-CSRF simulation | From a tester-owned origin, attempt only the approved benign sign-in initiation using tester-owned credentials and browser. | The application should require anti-forgery and/or robust Origin/flow correlation and should not silently establish an attacker-selected account. Native MVC alone is not guaranteed to prevent login XSRF [15]. | A forced tester-account session shows login-CSRF exposure; stop without involving any real user. |
| L10 | Origin and Fetch Metadata | Compare same-origin and tester-controlled cross-site submissions while recording `Origin` and `Sec-Fetch-Site`. | Token validation remains primary; defense-in-depth may reject inappropriate `cross-site` requests. `Sec-Fetch-Site` identifies same-origin, same-site, cross-site, or user-initiated contexts [19]. | Missing headers are not alone a finding. Acceptance plus missing/invalid tokens is. |
| L11 | Duplicate input handling | In staging, add a second same-name token field with a benign invalid value in each ordering. | Deterministic rejection or one documented, consistently validated value. | Parser disagreement or “first at edge, last at app” ambiguity requires engineering review. |
| L12 | Cookie attributes | Record anti-forgery and authentication cookies exactly as received. | HTTPS cookies should be `Secure`; non-JavaScript cookies should be `HttpOnly`; `Domain` should be as narrow as functionality permits [28]. | A broad Domain, missing Secure, or unexpected JavaScript access increases risk but does not alone prove CSRF. |

### Microsoft 365 sign-in matrix

Microsoft identity is not simply another local HTML POST. The authorization-code flow returns a response to the application's registered `redirect_uri`, and the application should compare response `state` to the value issued in the request [35]. The flow should use Microsoft-supported authentication libraries rather than handwritten token processing [35].

| ID | Identity-flow check | Secure expected result | Important distinction |
|---|---|---|---|
| M1 | Initiation state | Each clean flow receives a random, session-correlated `state` value [35]. | Do not demand an MVC form token on a redirect initiation if the supported identity library uses protocol correlation. |
| M2 | Returned state | A missing, altered, stale, or wrong-session `state` is rejected before establishing the local login [35]. | Test with synthetic/staging callbacks or library tests; do not replay a live authorization code. |
| M3 | OIDC correlation | Where OpenID Connect applies, verify the library's `nonce`; where appropriate, verify PKCE or one-time user-agent-bound `state` [29]. | `nonce`, PKCE, and `state` have protocol-specific roles; document which library control is relied upon. |
| M4 | Callback destination | Only registered callback locations are accepted, and user-controlled return targets cannot become open redirectors. OWASP warns that open redirectors can expose authorization codes or access tokens [29]. | This is an identity-flow review, not a request to test arbitrary redirect payloads on production. |
| M5 | SameSite compatibility | Complete each supported browser and callback mode while recording correlation-cookie attributes. Some OIDC and WS-Federation configurations use POST redirects [36]. | A cookie setting that blocks the legitimate callback is an availability defect; weakening all cookies to fix it can create a security defect. |

**Section insight:** A local form should fail closed when either MVC token is absent or invalid. A Microsoft identity callback should fail closed when protocol correlation is absent or wrong. Applying the wrong mechanism to the wrong boundary can either leave a gap or break legitimate login.

## Exact Post-Login and JSON Test Matrices

Begin with an authenticated route inventory generated from approved navigation, source review, or application documentation. Do not spider outside the authorized path set. The functional categories below are conditional: they are not claims that MUJ exposes each feature.

| Conditional feature category | Examples of state to protect if present | Required CSRF coverage | Safe test choice |
|---|---|---|---|
| Profile and preferences | Display name, contact preference, notification setting | Every unsafe action and alternate route | Toggle a tester-only preference and restore it. |
| Academic workflow | Registration choices, elective preferences, submissions | Token plus authorization and workflow checks | Use a sandbox record or designated test term only. |
| Fees and finance | Payment initiation, saved details, refunds, receipt delivery | Token, reauthentication for sensitive actions, and transaction integrity | Do not create monetary movement without explicit finance-team approval. |
| Files and forms | Upload, delete, replace, submit, approve | Multipart requests need the same anti-forgery enforcement | Upload and remove a harmless designated test file. |
| Messaging and notifications | Send, subscribe, mark, delete | Protect every state-mutating action, including bulk endpoints | Use a private test recipient or disabled delivery channel. |
| Account security | Password, email, recovery, MFA, linked identity | Anti-forgery plus reauthentication and audit logging | Use dedicated test identities and prearranged recovery. |
| Parent or delegate access | Link, unlink, consent, permission changes | Strong anti-forgery, authorization, and explicit confirmation | Use university-created paired test identities only. |
| Session controls | Logout-all, revoke device, remember-browser | Anti-forgery where state change has security impact | Use only the tester's sessions. |

### Post-login negative tests

| ID | Test | Exact controlled mutation | Secure expected result |
|---|---|---|---|
| P1 | Route coverage | For each unsafe endpoint, compare valid baseline with field omitted and cookie omitted. | Both negative requests fail before controller state change [26]. |
| P2 | Pair binding | Combine two valid pairs from isolated profiles. | Mismatched security values fail [26]. |
| P3 | Identity binding | Use only two authorized test accounts and present account A's field token in account B's authenticated context. | Username or claim UID mismatch fails [26]. |
| P4 | Method coverage | Check approved GET, POST, PUT, PATCH, and DELETE mappings without attempting destructive actions. | GET remains safe; every unsafe mapping enforces an appropriate CSRF control. POST alone is not sufficient [34]. |
| P5 | Alternate content type | For one benign action, compare the documented form encoding with JSON or other accepted encodings. | Unsupported encodings fail; supported unsafe encodings invoke equivalent validation. |
| P6 | AJAX/header route | Remove the custom header, remove its cookie half, alter one half, and use a pair from another profile. | Each invalid case fails; valid header transport calls native validation [9]. |
| P7 | Token after logout | Log out a tester, start a new context, and present the old pair only to a benign endpoint. | The result should match documented session policy; authenticated state must not be resurrected. |
| P8 | Duplicate names | In staging, supply two token fields or two same-name cookies in opposite orders. | Deterministic, documented rejection is preferred. Edge and origin must agree on the selected value. |
| P9 | Cache isolation | Load the same token-bearing page in two authorized profiles and inspect cache directives, edge indicators, and token/cookie separation. | No user receives another test user's personalized token or content; `no-store` prevents cache storage [25]. |
| P10 | Failure atomicity | Trigger a benign invalid-token request and inspect the test record afterward. | No partial write, queued job, email, audit-side action, or session change occurs before rejection. |

### JSON and custom anti-forgery handlers

A property named `__RequestVerificationToken` inside JSON is not equivalent to an MVC form field. The native store reads `Request.Form[_config.FormFieldName]` [3]. **Inference:** unless middleware or an action filter parses JSON and forwards the extracted value to native validation, `ValidateAntiForgeryTokenAttribute` will not discover that property through the normal form-token store.

Microsoft's Web API guidance demonstrates a different contract: carry token material in a custom header and call `AntiForgery.Validate` [9]. A robust custom handler should still validate both protected values. It should not downgrade to “header exists,” “cookie exists,” or “header equals an unrelated cookie.”

| JSON/custom-handler control | What to inspect in code review | Authorized black-box check | Failure interpretation |
|---|---|---|---|
| Extraction source | Exact header or JSON property name and allowed content types | Send a valid request through only the documented transport. | Undocumented fallback transports expand attack surface. |
| Pair completeness | Cookie token plus request token both reach `AntiForgery.Validate` | Remove each half independently. | Acceptance of either negative case is a strong defect [9]. |
| Native validation | Handler calls the two-token validation API, not a string-presence check | Tamper one character and mismatch controlled pairs. | Acceptance suggests custom validation bypasses MachineKey or pair binding. |
| Route coverage | Filter or middleware applies to every unsafe JSON action | Inventory approved routes and perform omission tests. | One uncovered action is independently vulnerable even if others are correct. |
| Duplicate properties | Parser has deterministic duplicate-property behavior | Staging only: submit duplicate token properties in opposite order. | Different edge, binder, and handler interpretations create request ambiguity. |
| CORS and custom header | Only approved origins can cause credentialed custom-header requests | Review preflight and credential policy from a tester-owned origin. | CORS is defense in depth; a permissive policy must not replace token validation. |
| Error handling | Invalid token is rejected before body processing or side effects | Compare database/audit state after a benign invalid request. | Parsing or side effects before validation can make rejection too late. |
| Logging | Token values are redacted while reason, route, user, and correlation ID remain visible | Review approved logs, not production secrets. | Full token logging creates a replay source; no telemetry impedes detection. |

**Section insight:** The decisive JSON question is not “is the token in the body?” It is “which component extracts which value, and does that component invoke the complete cookie-plus-request-token validation before any side effect?”

## Akamai, IIS, Cookies, and Microsoft Identity Interactions

The supplied Akamai and IIS details create test hypotheses, not findings. HTTP allows a response containing `Set-Cookie` to be stored and reused by a cache unless cache behavior prevents it [16]. `Cache-Control` controls browser and shared-cache behavior, and `no-store` explicitly directs caches not to store the response [25]. **Inference:** a tokenized login or personalized post-login page should normally be uncacheable by shared edges, or its cache key and private handling must guarantee per-user isolation.

| Interaction | Why it matters | Exact evidence to collect | Secure outcome |
|---|---|---|---|
| Akamai cacheability | A shared tokenized response could expose another session's field token or content. | Response `Cache-Control`, `Age`, `Vary`, edge cache-status headers, repeated authorized-profile loads. | Personalized and token-bearing responses are not shared across users. |
| Header-based CSRF defenses and caches | OWASP says caches must vary when responses differ based on headers such as `Origin` or `Sec-Fetch-Site` [17]. | Compare same-origin and cross-site decisions plus `Vary` behavior. | A cached allow response cannot override a later deny context. |
| TLS termination | MVC can require SSL for generation and validation, and the saved cookie becomes `Secure` when `RequireSSL` is enabled [3][14]. | Browser-visible scheme, redirects, cookie attributes, and approved origin configuration review. | HTTPS is canonical; no insecure request mints or accepts tokens. |
| Multiple IIS nodes | `Unprotect` can fail with auto-generated keys in a multi-server app [20]. | Repeated valid submissions correlated to approved node/deployment telemetry. | All healthy nodes accept valid tokens and reject invalid ones consistently. |
| Cookie scope | A broad Domain exposes a cookie to more hosts, and sibling domains lack cookie-integrity isolation [16]. | Exact `Domain`, `Path`, name, Secure, HttpOnly, and SameSite values. | Host-only or narrowly scoped cookies unless a documented function requires broader scope. |
| SameSite and identity callbacks | SameSite provides some CSRF protection, but POST-based identity redirects can require special handling [36]. | Supported browser tests for local login, external initiation, callback, logout, and silent renewal if used. | Restrictive settings protect local cookies without breaking protocol correlation. |
| Alternate hostnames | Multiple application hostnames can create separate cookie jars or unintended parent-domain sharing. | Approved DNS and application inventory, not opportunistic subdomain probing. | One documented canonical host or explicitly isolated applications and cookie names. |

Fetch Metadata can supplement, but not replace, token validation. `Sec-Fetch-Site` tells the server whether a request is same-origin, same-site, cross-site, or user initiated, allowing policy decisions [19]. Roll such policies out in report-only mode first; OWASP recommends logging requests that would be blocked and reviewing false positives before enforcement [17]. Identity callbacks, webhooks, and legitimate cross-site integrations need explicit policy exceptions based on route and protocol, not a global bypass.

**Section insight:** The edge should preserve the application's security decision, never manufacture it. Tokens belong to MVC or an explicitly designed API handler; Akamai caching, SameSite, Origin checks, and Fetch Metadata reduce exposure but do not validate the token pair.

## Prioritized Remediation Blueprint

The following actions are recommendations, not assertions that MUJ is currently misconfigured.

| Priority | Engineering action | Acceptance criterion | Risk addressed |
|---|---|---|---|
| P0 | Inventory every state-changing MVC, Web API, AJAX, upload, and identity endpoint. | Every unsafe route has an owner, authentication model, CSRF mechanism, and negative test. | Hidden method and route gaps. |
| P0 | Apply `ValidateAntiForgeryTokenAttribute` to every applicable classic MVC unsafe action or controller. The attribute is an authorization filter applicable to classes and methods [10]. | Omission of either token rejects before action execution. | Missing per-action validation. |
| P0 | For JSON, define one custom-header contract and call `AntiForgery.Validate` with both tokens [9]. | Missing, malformed, mismatched, and cross-profile pairs all fail. | JSON/form transport gap and cookie-only validation. |
| P0 | Protect local login initiation and verify Microsoft identity `state`/`nonce` through a supported library [35]. | Forced-login and wrong-state tests fail in controlled accounts. | Login CSRF and identity mix-up. |
| P0 | Ensure GET, HEAD, OPTIONS, and TRACE do not mutate state; cover all unsafe verb aliases. | Route inventory and application tests show no state-changing safe method [34]. | Method-based bypass. |
| P1 | Set `AntiForgeryConfig.RequireSsl = true` in HTTPS production and verify actual cookie attributes. `RequireSsl` controls whether anti-forgery tokens require an SSL channel [15]. | HTTP redirects before token issuance; cookies arrive with appropriate Secure, HttpOnly, SameSite, Path, and Domain. | Transport and cookie exposure. |
| P1 | Keep anti-forgery and authentication cookies host-only or as narrowly scoped as functionality allows. Use unique names and keys per application. | No unnecessary parent-domain Domain attribute; duplicate-cookie behavior is deterministic. | Sibling-subdomain injection and application confusion. |
| P1 | Configure consistent, securely managed MachineKeys across intended web-farm nodes and isolate unrelated applications. | Every healthy node accepts the same valid controlled token and rejects tampering; key access is restricted [23]. | Random failures, accidental cross-app trust, key compromise blast radius. |
| P1 | Mark personalized and tokenized responses against shared storage, normally with `Cache-Control: no-store`, and review Akamai property rules. | Two authorized sessions never receive each other's token or personalized response [25]. | CDN disclosure and stale-token delivery. |
| P1 | Bind claims correctly. MVC can use a configured unique claim type, while the default claim extractor uses name-identifier and identity-provider claims [40]. | Two authorized identities never share the same anti-forgery identity binding. | Cross-user token acceptance. |
| P2 | Use optional `AdditionalDataProvider` only for a clearly defined, testable context such as a sensitive workflow version. MVC validates configured additional data [26]. | Context changes invalidate only the intended actions without widespread false failures. | Replay across sensitive workflow boundaries. |
| P2 | Add Origin and Fetch Metadata checks as defense in depth with explicit exceptions and report-only rollout [17][19]. | Legitimate identity/integration traffic works; inappropriate cross-site unsafe requests are rejected and logged. | Residual cross-site request risk. |
| P2 | Redact token and session values from logs while retaining route, user ID, reason code, correlation ID, and edge/origin decision. | Security telemetry supports incident review without becoming a token repository. | Replay from logs and weak detection. |
| P2 | Maintain regression tests for every negative matrix row. | CI or staging tests fail when an unsafe action loses protection. | Future coverage regressions. |

A cookie name beginning with `__RequestVerificationToken` has no browser-enforced prefix semantics. If engineering adopts a browser-enforced `__Host-` name, all prefix requirements must be met; MDN recommends `__Host-` for cookies restricted to one host and a `/` path [28]. This should be treated as hardening, not a substitute for the field/header half or identity binding.

**Section insight:** The fastest high-value work is route coverage plus negative tests. Cryptographic redesign is unnecessary when native MVC is used correctly; custom code should be minimized to the JSON transport adapter and identity-library integration.

## Synthesis: Four Mechanisms, Four Different Trust Boundaries

| Dimension | Native MVC HTML forms | Custom JSON/AJAX | Microsoft 365 OAuth/OIDC | Akamai/IIS deployment |
|---|---|---|---|---|
| Primary mechanism | Protected cookie token plus protected hidden form token [9]. | Explicit extraction plus both-token validation, commonly through a custom header [9]. | Random `state`, equality check, and protocol controls such as `nonce` or PKCE where applicable [29][35]. | Correct cache, TLS, forwarding, and shared-key behavior; not a CSRF-token validator. |
| Binding | Shared 128-bit security value plus current username/claim UID and optional data [26]. | Whatever the adapter preserves; strongest when it calls native validation unchanged. | Browser authorization transaction and registered callback. | Cache key, origin pool, application identity, and MachineKey scope. |
| Reuse model | Session reuse can be legitimate [17]; no token timestamp appears in the native format [39]. | Must be documented; should not silently weaken native semantics. | State should be unique and correlated to the flow [35]. | Cached objects and keys have operational lifetimes unrelated to CSRF token lifetime. |
| Main failure mode | Attribute omitted, unsafe GET, missing identity binding, or accepting only one token. | Token left inside JSON without extraction, header presence-only checks, or uncovered routes. | Missing/wrong-state acceptance, open redirect, callback mix-up, or broken SameSite correlation. | Shared caching of personalized HTML, inconsistent keys, broad cookies, or proxy-origin policy disagreement. |
| Availability tension | Per-request invalidation can break back-button or multi-tab workflows. | Strict header/CORS rules can break legitimate clients. | Restrictive SameSite can break POST-based callbacks [36]. | Per-node keys break valid tokens; shared keys increase the importance of key isolation. |
| Best verification | Pairwise negative matrix and identity-bound tests. | Transport-contract, route-coverage, and side-effect-order tests. | Library configuration and controlled state/nonce tests. | Multi-session cache isolation and multi-node consistency tests. |

Three non-obvious tensions drive the final strategy.

First, **freshness versus usability**: one-time tokens narrow replay but can create false failures in tabs and navigation, while MVC's session-oriented reuse is operationally stable. The correct recommendation is not mandatory per-request rotation; it is strong pair and identity binding plus explicit invalidation boundaries.

Second, **cookie isolation versus federated login**: host-only, Secure, restrictive SameSite cookies reduce ambient authority, but federated identity may require a cross-site return. The solution is purpose-specific cookies and protocol correlation, not globally loosening every cookie or exempting the entire login surface.

Third, **edge performance versus personalized security state**: Akamai can improve delivery, but a tokenized page is part of an individual browser-server security conversation. **Inference:** shared caching should be disabled for those pages unless a reviewed design proves isolation. Header-based Origin or Fetch Metadata decisions also require correct cache variation [17].

The unified model is therefore defense in depth with clear ownership: MVC validates HTML token pairs; a narrow adapter validates JSON pairs; the Microsoft identity library validates authorization-flow correlation; and the edge preserves confidentiality, routing consistency, and application decisions.

## VERDICT

**Verdict: INDETERMINATE - no current MUJ SLCM CSRF vulnerability is established, and safety is not established either.**

The observed `__RequestVerificationToken` cookie-plus-field pair is consistent with the correct classic ASP.NET MVC design. Native MVC 5 provides substantial protection when both protected tokens are required, their embedded 128-bit values match, their roles are correct, the request token matches the authenticated username or claim UID, and any configured additional data validates [26]. MachineKey purpose-bound protection should reject tampering [7][22].

However, public observation cannot show whether every login and post-login action invokes that validator, whether JSON handlers preserve both halves, whether login CSRF has separate protection, whether cookies are narrowly scoped, whether Akamai shares tokenized responses, or whether Microsoft identity callbacks validate `state`. Those are decisive unknowns.

| Confidence dimension | Level | Basis |
|---|---|---|
| ASP.NET MVC 5 mechanism | **High** | Microsoft documentation and .NET Foundation source agree on token structure, protection, and validation. |
| Relevance of listed bypass families | **High** | Each family maps to a documented failed invariant or standards-level cookie behavior. |
| Suitability of the authorized test plan | **High** | Tests directly exercise native validation branches using benign, controlled mutations. |
| Exact MUJ stack fingerprint | **Medium-Low** | Supplied by the requester and not independently verified in this report. |
| Current MUJ vulnerability status | **Low / Indeterminate** | No active validation, configuration review, or authorized source review was performed. |

**Promotion to “protected” requires:** complete unsafe-route inventory; rejection of missing, swapped, mismatched, cross-profile, and cross-identity tokens; correct JSON-header validation; explicit login/OAuth correlation; narrow secure cookies; cache isolation; and consistent results across supported browsers and origin nodes.

**Promotion to “vulnerable” requires:** an authorized, reproducible demonstration that a specific unsafe action changes state without the required user intent, with the exact failed invariant documented and all testing limited to institution-provided accounts and benign data.

**Overall confidence in this verdict: High.** The confidence is high precisely because the verdict does not extrapolate from token presence or public fingerprints to an unsupported vulnerability claim.

## References

1. *AspNetWebStack/src/System.Web.WebPages/Helpers/AntiXsrf at main · aspnet/AspNetWebStack · GitHub*. https://github.com/aspnet/AspNetWebStack/tree/main/src/System.Web.WebPages/Helpers/AntiXsrf
2. *AspNetWebStack/src/System.Web.WebPages/Helpers/AntiXsrf/AntiForgeryToken.cs at main · aspnet/AspNetWebStack · GitHub*. https://github.com/aspnet/AspNetWebStack/blob/main/src/System.Web.WebPages/Helpers/AntiXsrf/AntiForgeryToken.cs
3. *AspNetWebStack/src/System.Web.WebPages/Helpers/AntiXsrf/AntiForgeryTokenStore.cs at main · aspnet/AspNetWebStack · GitHub*. https://github.com/aspnet/AspNetWebStack/blob/main/src/System.Web.WebPages/Helpers/AntiXsrf/AntiForgeryTokenStore.cs
4. *AntiForgeryConfig.UniqueClaimTypeIdentifier Property (System.Web.Helpers) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.helpers.antiforgeryconfig.uniqueclaimtypeidentifier?view=aspnet-webpages-3.2
5. *AntiForgeryConfig Class (System.Web.Helpers) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.helpers.antiforgeryconfig?view=aspnet-webpages-3.2
6. *AntiForgeryConfig.CookieName Property (System.Web.Helpers) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.helpers.antiforgeryconfig.cookiename?view=aspnet-webpages-3.2
7. *AspNetWebStack/src/System.Web.WebPages/Helpers/AntiXsrf/MachineKey45CryptoSystem.cs at main · aspnet/AspNetWebStack · GitHub*. https://github.com/aspnet/AspNetWebStack/blob/main/src/System.Web.WebPages/Helpers/AntiXsrf/MachineKey45CryptoSystem.cs
8. *MachineKey Class (System.Web.Security) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.security.machinekey?view=netframework-4.8.1
9. *Preventing Cross-Site Request Forgery (CSRF) Attacks in ASP.NET MVC | Microsoft Learn*. https://learn.microsoft.com/en-us/aspnet/web-api/overview/security/preventing-cross-site-request-forgery-csrf-attacks
10. *ValidateAntiForgeryTokenAttribute Class (System.Web.Mvc) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.mvc.validateantiforgerytokenattribute?view=aspnet-mvc-5.2
11. *AntiForgeryConfig.RequireSsl Property (System.Web.Helpers) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.helpers.antiforgeryconfig.requiressl?view=aspnet-webpages-3.2
12. *AntiForgeryConfig.AdditionalDataProvider Property (System.Web.Helpers) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.helpers.antiforgeryconfig.additionaldataprovider?view=aspnet-webpages-3.2
13. *Bypassing CSRF token validation | Web Security Academy*. https://portswigger.net/web-security/csrf/bypassing-token-validation
14. *AspNetWebStack/src/System.Web.WebPages/Helpers/AntiXsrf/AntiForgeryWorker.cs at main · aspnet/AspNetWebStack · GitHub*. https://github.com/aspnet/AspNetWebStack/blob/main/src/System.Web.WebPages/Helpers/AntiXsrf/AntiForgeryWorker.cs
15. *XSRF/CSRF Prevention in ASP.NET MVC and Web Pages | Microsoft Learn*. https://learn.microsoft.com/en-us/aspnet/mvc/overview/security/xsrfcsrf-prevention-in-aspnet-mvc-and-web-pages
16. [
            
                RFC 6265 - HTTP State Management Mechanism
            
        ](https://datatracker.ietf.org/doc/html/rfc6265)
17. *Cross-Site Request Forgery Prevention - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
18. *muj portal - Manipal University*. https://mujslcm.jaipur.manipal.edu/
19. *Sec-Fetch-Site header - HTTP | MDN*. https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Sec-Fetch-Site
20. [MachineKey.Unprotect(Byte[], String[]) Method (System.Web.Security) | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/api/system.web.security.machinekey.unprotect?view=netframework-4.8.1)
21. *MachineKeySection.Validation Property (System.Web.Configuration) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.configuration.machinekeysection.validation?view=netframework-4.8.1
22. [MachineKey.Protect(Byte[], String[]) Method (System.Web.Security) | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/api/system.web.security.machinekey.protect?view=netframework-4.8.1)
23. *MachineKeySection.ValidationKey Property (System.Web.Configuration) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.configuration.machinekeysection.validationkey?view=netframework-4.8.1
24. *AspNetWebStack/src/System.Web.WebPages/Helpers/AntiXsrf/BinaryBlob.cs at main · aspnet/AspNetWebStack · GitHub*. https://github.com/aspnet/AspNetWebStack/blob/main/src/System.Web.WebPages/Helpers/AntiXsrf/BinaryBlob.cs
25. *Cache-Control header - HTTP | MDN*. https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control
26. *AspNetWebStack/src/System.Web.WebPages/Helpers/AntiXsrf/TokenValidator.cs at main · aspnet/AspNetWebStack · GitHub*. https://github.com/aspnet/AspNetWebStack/blob/main/src/System.Web.WebPages/Helpers/AntiXsrf/TokenValidator.cs
27. *Origin header - HTTP | MDN*. https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Origin
28. *Secure cookie configuration - Security | MDN*. https://developer.mozilla.org/en-US/docs/Web/Security/Practical_implementation_guides/Cookies
29. *OAuth2 - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html
30. *Quick start*. https://techdocs.akamai.com/purge-cache/docs/quick-start
31. *Prefetch Objects*. https://techdocs.akamai.com/property-mgr/docs/prefetching
32. *Learn about Akamai's caching*. http://techdocs.akamai.com/property-mgr/docs/know-caching
33. [
            
                RFC 9110 - HTTP Semantics
            
        ](https://datatracker.ietf.org/doc/html/rfc9110)
34. *WSTG - Latest | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/06-Session_Management_Testing/05-Testing_for_Cross_Site_Request_Forgery
35. *Microsoft identity platform and OAuth 2.0 authorization code flow - Microsoft identity platform | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow
36. *Work with SameSite cookies in ASP.NET | Microsoft Learn*. https://learn.microsoft.com/en-us/aspnet/samesite/system-web-samesite
37. [
            
                RFC 9110 - HTTP Semantics
            
        ](https://datatracker.ietf.org/doc/html/rfc9110#section-9.2.1)
38. [
        NuGet Gallery
        | Microsoft.AspNet.Mvc 5.3.0
    ](https://www.nuget.org/packages/Microsoft.AspNet.Mvc/)
39. *AspNetWebStack/src/System.Web.WebPages/Helpers/AntiXsrf/AntiForgeryTokenSerializer.cs at main · aspnet/AspNetWebStack · GitHub*. https://github.com/aspnet/AspNetWebStack/blob/main/src/System.Web.WebPages/Helpers/AntiXsrf/AntiForgeryTokenSerializer.cs
40. *AspNetWebStack/src/System.Web.WebPages/Helpers/AntiXsrf/ClaimUidExtractor.cs at main · aspnet/AspNetWebStack · GitHub*. https://github.com/aspnet/AspNetWebStack/blob/main/src/System.Web.WebPages/Helpers/AntiXsrf/ClaimUidExtractor.cs
