# MUJ SLCM Authentication and Token Abuse Readiness

## Executive Summary

- **Current Campaign Status**: The supplied campaign record remains PARTIAL: identity design was observed, but no authentication occurred and token semantics remain untested. The public landing page identifies the service as the MUJ portal [38]. All portal-specific measurements below are labeled as requester-supplied unless a public source is cited.
- **Token Boundary**: The first decision is whether MUJ SLCM uses an ASP.NET forms-authentication or session cookie, an Entra OIDC result, an API bearer token, a custom encrypted value, or a combination. Microsoft says the resource owns an access token and must validate its audience before accepting it [7].
- **Replay Risk**: A bearer token is usable by anyone who possesses it and does not itself prove possession of a cryptographic key [12]. The practical MUJ question is whether a captured test-account cookie or token remains useful after logout, password reset, SSPR, factor enrollment, tenant change, or device change.
- **Tenant Confusion**: Microsoft Entra exposes tenant-scoped OIDC endpoints and public discovery metadata, including signing-key information [27]. With three reported tenants, issuer, tenant ID, audience, subject, scopes, roles, and local account linkage must be tested as separate controls.
- **Recovery Is Authentication**: Microsoft lists password reset, MFA enablement, explicit refresh-token revocation, and related changes among CAE events [29]. The SSPR and OTP-parent paths therefore deserve the same assurance as password login.
- **Cookie Finding Needs Precision**: The brief reports an HttpOnly antiforgery cookie without Secure. OWASP treats Secure and HttpOnly as different controls: Secure restricts transmission to a secure channel, while HttpOnly restricts script access [18]. This does not establish that the cookie is an authentication cookie or that it is exploitable.
- **Oracle Discipline**: The reported three-stage `enc` response is evidence of input-dependent processing, not evidence of decryption, padding-oracle exploitability, or authentication bypass. Any differential assessment must be rate-limited, test-account-only, and stopped on state change.
- **Detection Must Be Designed First**: Microsoft can export Entra sign-in and audit data to Sentinel [21][6]. MUJ should correlate those records with application session issuance, token validation, SSPR, OTP, logout, and authorization events before active testing begins.
- **Tooling Is Necessary but Not Sufficient**: jwt_tool and JWT Editor can inspect or mutate JWTs [10][11], while AuthMatrix compares requests across users and roles [4]. Neither can prove the correct business authorization or tenant ownership without target-specific evidence.
- **Recommended Decision**: Keep public and offline analysis open now; reserve token replay, reset, OTP, session rotation, cross-user authorization, and oracle validation for the signed scope letter and two test accounts. The defensible verdict is unknown portal token risk, with high confidence in the taxonomy and medium confidence in target-specific prioritization.

## 1. Scope, Evidence, and an Auditable Decision Log

This report is limited to authentication and token abuse beyond the login form. It covers browser sessions, ASP.NET cookies, antiforgery state, OAuth and OIDC, JWT and opaque tokens, refresh tokens, SSPR, OTP and MFA, tenant boundaries, authorization, logout, revocation, and detection. It does not provide credentials, exploit payloads, bypass recipes, rate-limit evasion, or instructions for accessing another person's account.

The request supplies a live, non-destructive campaign record dated 2026-09-13. It says that 443 is the only reachable port; IIS 10, ASP.NET MVC 5.3, .NET Framework 4.7.4136.0, jQuery 1.10.2 plus bundled jQuery 3.4.1, Azure AS8075, Microsoft 365 identity, three Entra tenants, no attributable edge control, no HSTS, and TLS 1.0 through 1.3 were observed. It also reports verbose YSOD behavior, two error-page families, GET-only method behavior, an HttpOnly antiforgery cookie without Secure, and a three-stage `enc` response oracle. These are campaign inputs, not independently reproduced public findings. The public landing page confirms the MUJ portal identity, but does not confirm those measurements [38].

| Evidence item | Status used here | What it does and does not establish | Source or authorization condition |
|---|---|---|---|
| MUJ portal landing page | Publicly observable identity | Identifies the service as the MUJ portal; it does not establish the authentication design | http://mujslcm.jaipur.manipal.edu/Home/Index [38] |
| Stack, cloud, identity, TLS, headers, ports, errors, and method policy | Supplied campaign measurements | Useful hypotheses only; not independently verified in this report | Requester-supplied live record; any retest requires owner approval |
| SSPR, OTP parent accounts, three Entra tenants, and single M365 password | Supplied design observations | Establishes recovery and tenant priorities; does not establish MFA coverage or token semantics | Requester-supplied design record; active validation requires scope letter and test accounts |
| No authentication performed | Supplied campaign boundary | There is no evidence yet of a valid MUJ session, token, authorization decision, or replay result | Requester-supplied record |
| `enc` response-size and exception differences | Supplied behavior | Indicates input-dependent processing; does not prove an encryption weakness or access-control impact | Signed scope letter and two test accounts required before active differential testing |

### Auditable reasoning record

The requested `cot_explicit` field is handled as an auditable decision log rather than private chain-of-thought. The decision sequence is: classify the token boundary; map each identity transition to a security property; select the least invasive observation that can distinguish competing hypotheses; define expected log evidence; and stop if the result would affect a non-test identity or create durable state. This is consistent with OWASP's guidance to gather session tokens, understand how the application creates and manages them, and test uniqueness, unpredictability, disclosure, transport, and lifecycle [14].

The key inference is that identity design alone cannot answer token-abuse questions. The same visible Microsoft login may result in a local application cookie, an OIDC ID token used only for sign-in, an access token for an API, a refresh token held by a client, or several of these. That is an architectural inference from the brief, not a claim about the live portal. It is why no vulnerability conclusion should be assigned until the two test accounts produce a token inventory and an authorization matrix.

## 2. Technique Universe Beyond the Login Form

The following is the bounded technique universe for this target class. Each row is an authorized question, not an instruction to attack a real user.

| Technique family | Authorized question | Evidence to collect | Pre-authorization status |
|---|---|---|---|
| Public identity discovery | Does published OIDC metadata identify the authority, endpoints, supported claims, and signing keys? | Discovery JSON, issuer, authorize endpoint, token endpoint, JWKS URL, tenant context | Read public metadata or use a lab tenant; target interaction follows owner policy [27] |
| Cookie and session inventory | Which cookies are pre-auth, post-auth, antiforgery, preference, or session cookies? Are Secure, HttpOnly, SameSite, Domain, Path, and expiry appropriate? | Redacted Set-Cookie records and browser cookie metadata | Own browser or offline capture; target interception requires scope [18] |
| Session schema and entropy | Are identifiers unique, unpredictable, non-meaningful, and resistant to disclosure or sequencing? | Redacted samples from each test account, timing, collision and lifecycle observations | Methodology and local replica are safe; target collection needs authorization [14] |
| Session fixation and rotation | Does the identifier rotate after login, MFA, privilege elevation, password change, and recovery? | Before and after cookie sets and invalidation records | Letter and test accounts; OWASP specifically calls for pre/post-authentication comparison [1] |
| Cookie scope and tossing | Can a path or subdomain influence a cookie, or can a loose Domain or Path expose it to another application? | Domain, Path, host-only status, duplicate-name behavior, subdomain map | Public documentation is low risk; modifying target cookies is authorized-only [18] |
| CSRF and login CSRF | Does the server bind state-changing requests to authenticated identity and antiforgery state? Does login or account linking bind to the intended browser? | Request/response pairing, token binding, failure behavior, audit record | Test design and local replica are safe; state-changing target requests need the letter [9] |
| OAuth authorization-code handling | Are redirect URIs exact, codes single-use, clients bound, codes short-lived, and PKCE enforced? | Redacted redirect and token exchange, state, nonce, challenge, and verifier presence | Protocol review is safe; using target codes or clients needs scope [8][13] |
| OIDC login binding | Does the app validate issuer, nonce, signature, audience, tenant, and the relationship between OIDC subject and local account? | Redacted ID-token claims and server-side validation result | Decode lab tokens offline; target login and account linking need the letter [27] |
| JWT validation | Does the resource enforce algorithm, signature, issuer, audience, time claims, token type, and permitted key source? | Validator decision, key ID, audience, issuer, time window, and rejection reason | Tool preparation is safe; mutated target tokens are active testing [2] |
| Opaque or encrypted value handling | Does the server reject modified, truncated, stale, cross-context, or wrongly scoped values without sensitive leakage or state change? | Redacted error class, response family, correlation ID, and state result | Offline parser design is safe; oracle differentials require scope and test accounts |
| Bearer replay | Does a captured test token work from a second controlled client, after logout, or after a security event? | First use, second use, client context, revocation timestamp, and logs | Letter and test accounts only; possession alone is not proof of identity [12] |
| Refresh-token lifecycle | Are refresh tokens rotated, stored safely, expired, revoked, and rejected in the correct tenant? | Token-family behavior, redemption result, expiry, and revocation event | Letter and test accounts; no real-user refresh tokens [15] |
| SSPR and password reset | Are responses uniform, artifacts random and single-use, factors bound, and old sessions handled? | Reset state machine, factor used, expiry, redemption count, session state, audit event | Design review and lab replica are safe; live reset and account changes need approval [20][29] |
| MFA and OTP | Is every privileged path protected, is OTP single-use and time-bound, and can recovery or enrollment lower assurance? | Factor policy, challenge binding, attempt counters, recovery path, session elevation | Test accounts and letter only; do not send unsolicited OTPs or enumerate users [30][29] |
| Tenant and audience confusion | Can a token issued by tenant A be accepted by tenant B, or linked to the wrong local MUJ record? | Issuer, tid, aud, subject, home/resource tenant, local account ID, decision | Public metadata review is safe; cross-tenant token and account-link tests need scope [27][2] |
| Horizontal and vertical authorization | Can one test account use another test account's request, or can a lower role perform a higher-role action? | Request matrix, expected role, actual status/body, server-side decision | Requires two test accounts and explicit role/data boundaries [4] |
| Logout and revocation | Does local logout invalidate the browser session, and do reset, MFA enrollment, admin revocation, and CAE invalidate cloud access? | Token state before and after event, local and Entra logs, propagation time | Letter and test accounts; avoid global revocation of real users [29] |
| Detection and response | Can defenders distinguish normal login, reset, replay, tenant mismatch, and token-validation failure? | Application correlation ID plus Entra sign-in, audit, and risk records | Build in a lab or tenant-owned telemetry; production tuning needs approval [21][28] |

The central distinction is token format versus token meaning. A JWT can be correctly signed yet accepted for the wrong audience. An opaque cookie can be unreadable yet replayable. A correct antiforgery pair can protect a state-changing MVC action while having no bearing on the authentication cookie. OWASP treats Secure, HttpOnly, SameSite, Domain, Path, and expiry as separate properties [18].

## 3. MUJ-Specific Test Design for ASP.NET MVC and Entra

### 3.1 Establish the local session model without guessing

ASP.NET MVC antiforgery uses a synchronizer-token pattern: a cookie token and a form token are submitted together, and the runtime compares them; the token values are generated unpredictably [31]. The field token can include the authenticated username, while token payloads are encrypted and signed [31]. The framework's cryptographic services use MachineKey protection for the relevant ASP.NET versions [31]. Therefore, the reported antiforgery cookie should be treated as a CSRF control artifact until the application proves otherwise.

The scoped test should record all Set-Cookie values before login, after password authentication, after MFA or OTP completion, after an elevated action, after logout, and after a password or SSPR event. Compare names, values, flags, Domain, Path, SameSite, and expiry. Do not infer that the lack of Secure on the reported antiforgery cookie transfers to the authentication cookie. Conversely, do not dismiss it: Secure prevents transmission over an insecure channel, and HttpOnly limits script access; one flag cannot substitute for the other [18].

The immediate hypothesis is session renewal, not session theft. OWASP says to verify whether the same session-cookie value survives authentication and whether a new value is issued after authentication [1]. With two test accounts, the safe matrix is anonymous browser to account A, anonymous browser to account B, account A to account B's explicitly non-sensitive test object, logout, reset, factor change, and re-login. A positive finding requires a server-side authorization consequence and a reproducible audit trail, not merely a different response length.

### 3.2 Treat the `enc` behavior as an evidence gate

The brief reports invalid base64 producing a FormatException-sized response, valid base64 producing a CryptographicException-sized response, and an empty value producing a third response size. That pattern may arise from input parsing, decryption failure, exception formatting, or a custom parameter contract. It does not establish that plaintext is revealed, that a padding oracle exists, or that a valid authenticated value can be manufactured.

The responsible next step is a tightly controlled differential assessment using only synthetic values tied to the two test accounts. Record request hash, redacted parameter class, status, response family, byte count, timing bucket, correlation ID, and server-side event. Stop on any successful authorization, state change, abnormal error rate, or non-test identity. Do not send a public exploit corpus, attempt key recovery, or treat a response-size difference as a finding by itself. This is a safety recommendation based on the supplied observation and OWASP's requirement to analyze disclosure and token structure without equating representation with impact [14].

### 3.3 Validate Entra tokens at the resource boundary

Microsoft says APIs must accept only an access token whose audience matches the API, and that the resource server, rather than the client, should validate the access token [7]. Microsoft also identifies tenant ID, subject, scopes, roles, groups, and related claims as authorization inputs [2]. For MUJ, the minimum redacted claim record is issuer, tid, aud, sub or oid, scp, roles, groups if present, iat, nbf, exp, nonce where relevant, client ID, home tenant, and local MUJ account ID.

The three-tenant observation creates four test hypotheses: the wrong issuer is accepted; the right issuer but wrong tid is accepted; the right tenant and issuer but wrong audience is accepted; or a legitimate guest identity is linked to the wrong local account. These are inferences from the reported architecture, not findings. A two-account, two-tenant matrix can distinguish them without touching a third party, provided the scope letter explicitly names each test tenant and both account owners approve the flow.

### 3.4 Recovery and CAE are part of the same session

Microsoft documents account disablement, password reset, MFA enablement, explicit refresh-token revocation, and high user risk as CAE events [29]. It also states that CAE can cause a resource to reject a token before expiry and use a claim challenge to obtain a new token [29]. This is the relevant model for SSPR and OTP parent accounts: a reset that leaves a previously issued local session valid may be a design choice or a defect, but the owner must define the expected result.

Refresh-token behavior is not identical to local cookie behavior. Microsoft says refresh tokens are replaced on use, should be securely deleted by the client, have longer lifetimes than access tokens, and may be revoked before expiry by user or administrator action [15]. Microsoft also notes that a B2B refresh token may need revocation in the home tenant rather than the resource tenant [15]. That makes the reported dual-tenant split a concrete test priority, not a reason to assume compromise.

## 4. Tool Catalog and Tool-Supported Case Study

There is no literal finite list of every program capable of sending HTTP or decoding a JWT. The catalog below defines the relevant tool universe by function and lists the named tools that directly perform the required operations. It is conservative about hosted services and licensing where the cited material does not state a free tier.

| Tool or component | Exact URL | License and deployment | How it is driven | Output and MUJ use |
|---|---|---|---|---|
| Browser DevTools and cookie jar | https://developer.chrome.com/docs/devtools/ | Built into the browser; no separate tester license; local-only observation | Network and Application/Storage panels; save only redacted HAR or screenshots | Headers, cookies, redirects, timing, and browser-visible token placement. Safest first observation |
| Burp Suite Community and Professional | https://portswigger.net/burp/eula | PortSwigger proprietary. Community is licensed royalty-free for internal business use; Professional and DAST are separately licensed products [23]. Desktop/self-hosted; no BYOK requirement | Configure an authorized test browser for the local proxy; use Proxy, Repeater, Comparer, Logger, and extensions | HTTP messages, comparisons, project files, issue records, and request history. Professional is advertised as a web-security testing product with a free trial [32] |
| JWT Editor | https://github.com/PortSwigger/jwt-editor | Apache-2.0; free self-hosted Burp extension [11] | Install from the BApp Store or load the built JAR into Burp Extensions [11] | Parsed and edited JWS/JWE header, payload, signature, encryption state, and modified HTTP messages. It can use a supplied test key; it cannot obtain a legitimate MUJ signing key [11] |
| AuthMatrix | https://github.com/SecurityInnovation/AuthMatrix | MIT; free self-hosted Burp extension [4] | Define roles, users, session tokens, expected requests, and failure regex; send requests to AuthMatrix and run the matrix [4] | Color-coded green, red, and blue results and saved configurations for regression testing [4] |
| OWASP ZAP plus Authentication Helper | https://www.zaproxy.org/docs/desktop/addons/authentication-helper/ | Free, open-source, self-hosted OWASP project; confirm the current license at https://www.zaproxy.org/license/ | GUI, local API, or Automation Framework YAML. The framework is controlled by one YAML file [36] | Sites, requests, alerts, session/authentication configuration, and generated reports. Use passive collection first; active scanning is not authorized by default |
| mitmproxy, mitmdump, and mitmweb | https://github.com/mitmproxy/mitmproxy | MIT; free self-hosted [24]. It provides an interactive TLS-capable proxy, command-line mitmdump, and web UI mitmweb [24] | Local proxy with explicit test-browser/device trust; scripts can normalize or correlate flows | Interactive flows and script-generated records. Preserve a redacted flow export and hash manifest because the cited project page does not fix one report format |
| jwt_tool | https://github.com/ticarpi/jwt_tool | GPL-3.0; free self-hosted [10] | CLI with a supplied JWT, header or cookie source, test key/JWKS, and explicitly rate-limited authorized options | Decoded header/payload, validation and scan findings, key/secret checks, tamper/forge results, and stdout logs. It supports scanning, fuzzing, key testing, forging, timestamp changes, and rate limiting [10] |
| Postman OAuth 2.0 | https://learning.postman.com/v11/docs/use/send-requests/authorization/oauth-20 | Proprietary hosted/desktop API platform; plan-dependent; no self-hosting or BYOK claim is made here. Official pricing is plan based [39] | Configure authorization-code, PKCE, implicit, password-credential, or client-credential details in the Authorization tab [37] | Token retrieval, request/response bodies, console history, collections, and environment variables. Use synthetic or test-account secrets only |
| Fiddler Everywhere | https://www.telerik.com/fiddler/fiddler-everywhere/documentation/collaboration/exporting-and-importing | Commercial cross-platform local debugging proxy; purchase plans are published by Telerik [40]; not self-hosted as a service and no BYOK requirement | Local HTTPS-decryption proxy with explicit test-browser trust and capture filters | Captured traffic can be exported and imported in multiple formats [41]. Use only redacted test-account traffic |
| Microsoft Entra and Sentinel | https://learn.microsoft.com/en-us/azure/sentinel/connect-azure-active-directory | Tenant-owned Microsoft service, permission and licensing dependent; not a general token-forging tool and not self-hosted | Export Entra logs through the connector and query them in Sentinel; use admin-approved revocation and risk controls | Sign-in, audit, provisioning, non-interactive, risk, and related records. The connector streams Entra data to Sentinel [21] |

The useful case study is the contrast between JWT Editor and AuthMatrix. JWT Editor answers a representation question: can a controlled token be parsed, verified, edited, encrypted, or re-signed with a key that the tester already owns [11]. AuthMatrix answers a policy question: do two identities receive the expected result when the same request is presented under different role and user contexts [4]. Neither answers the other question. A green AuthMatrix result does not show that a JWT is well validated, and a valid JWT signature does not show that the requested MUJ action is authorized.

A second case study is the contrast between mitmproxy and Sentinel. mitmproxy observes client-side transport and can normalize flows, while Sentinel joins tenant-side sign-in and audit records [24][21]. The mechanism, vantage point, and output are different. A proxy can show that a browser reused a cookie; only application and identity logs can show whether the server accepted that reuse, associated it with the right subject, and generated a security event. This is why the project should retain both redacted flow evidence and server-side correlation IDs.

## 5. Manual Methods and Detection Counterparts

Manual work remains essential because tools do not know the MUJ account model, the expected parent-child relationship, or which actions are intentionally cross-tenant. The safe method is to write the expected state transition first and then observe only the two approved accounts.

| Test objective | Manual method, without exploit instructions | Detection counterpart and expected record |
|---|---|---|
| Token inventory | In a test browser, list response cookies, authorization headers, redirects, hidden fields, and token-bearing JSON. Redact values before storage | Application records token type, issuance event, account ID, tenant, client ID, and correlation ID; Entra records sign-in and token-related activity where available [21][28] |
| Cookie flags | Compare Set-Cookie attributes across anonymous, authenticated, MFA-complete, logout, and reset states | Log cookie issuance class, rotation reason, session ID hash, and old-session invalidation; OWASP provides the attribute expectations [18] |
| Session rotation | Capture only hashes of identifiers before and after login and privilege changes; compare whether the server issues a new identifier | Log session-created, session-rotated, session-invalidated, actor, reason, and correlation ID; OWASP calls for pre/post comparison [1] |
| CSRF and login binding | Confirm that a normal form or state-changing request carries the expected antiforgery pairing and that an altered or missing pair is rejected in the test account | Log antiforgery validation success/failure without logging the token; the MVC pattern uses paired cookie and field values [31] |
| OAuth/OIDC flow | Record redacted authorize and token exchanges, checking exact redirect, state, nonce, PKCE challenge/verifier, issuer, audience, and one-time-code behavior | Log client ID, redirect URI, state/nonce correlation, code redemption, failure reason, and token issuance. OWASP identifies code and PKCE material as credentials when leaked [5] |
| JWT or opaque validation | Submit only controlled values from the two test accounts and compare server decisions, not just response size | Log validation result, issuer, audience, tenant, subject, scope/role, key ID, time result, and rejection category; Microsoft requires resource-side audience validation [7][2] |
| Replay and logout | Use a single test token or cookie in two controlled clients, then repeat after local logout and an approved security event | Alert on the same token hash across divergent device, network, or user-agent context; CAE is intended to enforce critical-event revocation near real time [29] |
| SSPR and OTP | Walk only the owner-approved test-account reset and factor paths. Record challenge type, expiry, completion, session state, and whether a second redemption is accepted | Log reset initiation/completion, factor method, attempt count, actor, tenant, session revocation, and administrative changes; reset and MFA changes are CAE events [29] |
| Tenant and authorization matrix | Send the same non-sensitive test request under account A and account B, and where approved under each named tenant, then compare the expected role decision | Alert on tenant mismatch, audience mismatch, local-account mismatch, and cross-user access; AuthMatrix can preserve the role/request matrix [4] |
| `enc` differential | Use a small, preapproved set of synthetic categories and stop at the first unexpected state transition; never attempt key recovery | Log parameter class, response family, correlation ID, exception category, and state result. A difference without a state change is not a vulnerability verdict |
| Revocation | Coordinate a single approved logout, password reset, factor change, or admin revocation and measure local and cloud behavior | Record revocation request, issuer response, token rejection, propagation time, and CAE claim challenge where applicable [29][15] |

### Detection design

At the application layer, the recommended fields are an event ID, UTC timestamp, correlation ID, request ID, redacted session hash, token class, issuer, tenant ID, audience, subject or local account ID, client ID, role or scope, outcome, reason, source network category, user-agent category, and whether the event rotated or invalidated a session. This is a design recommendation and should be adapted to MUJ's privacy and retention policy; it is not a claim that these fields currently exist.

At the Entra layer, the detection team should enable the relevant sign-in and audit streams, understand their schema, and preserve the tenant context. Microsoft describes Entra activity logs as a source for monitoring and threat hunting [6], and Sentinel's connector supports streaming Entra log types [21]. Useful analytic joins include: reset completion followed by use of an old session; MFA enrollment followed by a new device sign-in; the same account appearing in divergent tenant or network contexts; a token validation failure followed by repeated requests; and a local authorization decision that disagrees with `tid`, `aud`, `scp`, or `roles`.

A detection counterpart must be tested in both directions. A test that is correctly blocked but generates no useful record is operationally incomplete. A test that generates a noisy record but does not identify the account, tenant, session hash, and correlation ID is difficult to investigate. The acceptance criterion should be a replayable evidence bundle: redacted client flow, server event, Entra event, expected decision, actual decision, and a timeline.

## 6. NO-TOOL GAPS and BUILD CANDIDATES

Commercial and open-source tools can proxy traffic, parse tokens, mutate controlled messages, and compare responses. They do not know which MUJ tenant owns a record, whether a parent OTP account is intended to authorize a child account, whether a local session should survive SSPR, or whether a successful HTTP response represents a permitted business action. Those are no-tool gaps inferred from the scopes of the tools above.

| Gap | Why existing tools do not close it | Build candidate | Minimum safe output |
|---|---|---|---|
| Token-boundary classifier | Proxies see artifacts but do not reliably classify local MVC cookies versus OIDC ID tokens, access tokens, refresh tokens, antiforgery values, and custom encrypted parameters | A local redaction-first parser that labels token source, transport, cookie flags, JWT claims, and lifecycle transition | JSON inventory with hashes only, no secret values, plus evidence pointers |
| Consent-aware two-account harness | AuthMatrix compares requests but does not manage owner-approved account scope, tenant ownership, or destructive-state gates | A session/authorization matrix runner with an explicit allowlist, role map, request IDs, and stop conditions | CSV/JSON matrix showing expected versus actual decisions and an immutable run manifest |
| Tenant and issuer correlator | JWT tools can read claims, but they do not know MUJ's approved mapping of issuer, tid, aud, home tenant, resource tenant, and local account | A policy file plus validator that rejects undeclared tenant combinations before sending any request | Pass/fail decision, reason, claim hash, and policy version |
| SSPR/OTP state machine | Generic proxies do not understand factor enrollment, recovery assurance, OTP reuse, or session invalidation expectations | A lab-first state machine driven by approved test-account fixtures and owner-defined expected transitions | State transition graph, factor method, expiry, reuse result, and revocation evidence |
| Revocation monitor | A client proxy cannot reliably observe server-side token rejection or CAE propagation | Correlator for application events, Entra sign-in/audit events, and token/session hashes | Timeline showing issuance, event, rejection, propagation, and residual access |
| Safe oracle harness | Response comparers can flag byte differences but cannot decide whether a difference is parser noise, cryptographic failure, or authorization impact | A bounded differential runner with synthetic categories, rate budget, anomaly threshold, and immediate stop on state change | Redacted response family, timing bucket, correlation ID, and no recovered secret |
| Detection replay simulator | JWT tools generate test artifacts but do not generate the exact operational evidence defenders need | An offline event generator and Sentinel test-data pack using synthetic identities and token hashes | Queries, expected alerts, false-positive notes, and cleanup record |
| Evidence and privacy pack | General tools often save full tokens and credentials in project files | A redaction, hashing, encryption-at-rest, retention, and destruction wrapper | Redacted report, hash manifest, owner approval ID, and deletion confirmation |

The highest-value build is the consent-aware two-account harness. It turns a vague token-abuse campaign into a controlled experiment: each request has an owner, an account, a tenant, a role, an expected result, an allowed rate, a cleanup action, and a detection query. The second priority is the tenant and issuer correlator because the reported dual-tenant design can produce a serious authorization error even when every JWT signature is valid. The third is the revocation monitor because a token that is valid at issuance may still be unacceptable after password reset, MFA change, or explicit administrative revocation.

## 7. Synthesis: Mechanism, Scope, Trade-Offs, and Time Horizon

| Boundary or strategy | Mechanism | Scope | Main trade-off | Evidence needed |
|---|---|---|---|---|
| ASP.NET MVC antiforgery | Paired cookie and field token, protected by framework cryptography [31] | State-changing browser requests | Helps CSRF resistance but is not an authentication or tenant-control proof | Token pairing, identity binding, cookie flags, and server validation |
| Local application session | Opaque or protected cookie with server-side interpretation | MUJ web session | Simple integration can make replay and lifecycle behavior opaque | Rotation, expiry, logout, reset invalidation, and authorization decisions |
| Entra OIDC ID token | Signed identity assertion with issuer, nonce, audience, and tenant context [27] | Sign-in and account linking | Strong federation semantics require correct validation and local mapping | Redacted claims and server-side validation result |
| Entra access token | Resource-scoped token whose `aud` must match the API [7] | API authorization | A valid token for another resource is not automatically valid here | Audience, issuer, tenant, scope, role, and resource decision |
| Bearer token | Possession-based use without key proof [12] | Any resource that accepts it | Easy interoperability but high replay impact if leaked | Controlled second-client use, revocation, sender context, and logs |
| Refresh token | Longer-lived mechanism for obtaining new access tokens; replacement and revocation are documented by Microsoft [15] | Client-to-identity-provider lifecycle | Better usability increases the value of storage and revocation controls | Rotation behavior, storage, expiry, home/resource tenant, and revocation |
| CAE and Token Protection | Near-real-time critical-event response, or device binding for supported scenarios [29][25] | Selected Microsoft resources and supported clients | Coverage is resource- and client-dependent; it is not proof of protection for every MUJ web path | Resource support, claim challenge, device context, and actual rejection |
| JWT testing tool | Parse, validate, mutate, sign with supplied keys, and compare | Token representation and protocol behavior | Cannot prove business authorization or acquire a legitimate signing key [10][11] | Server acceptance and authorization result under scope |
| Authorization matrix tool | Replay approved requests under defined users and roles [4] | Business authorization | Requires correct expected matrix and safe test objects | Status, body, side effect, server decision, and cleanup |

Several non-obvious tensions follow. First, stronger federation does not automatically mean stronger local authorization: Microsoft requires the resource to validate audience and tenant-related claims, so an identity provider can be correct while the portal's mapping is wrong [7][2]. Second, token revocation is not a single switch. CAE can provide near-real-time behavior for supported resources, while local MVC cookies and unsupported web paths still require application-level invalidation [29]. Third, a response oracle may be high quality evidence of an implementation distinction but low quality evidence of account impact. The campaign should rank evidence by security consequence, not by how dramatic an exception looks.

The strongest case study is Microsoft CAE. It changes the security mechanism from fixed expiry alone to critical-event evaluation, but Microsoft explicitly describes an initial focus on Exchange, Teams, and SharePoint Online and requires client understanding of claim challenge [29]. The lesson for MUJ is not to claim CAE coverage; it is to verify whether the particular MUJ resource participates and whether the local session honors the same event. A second case study is ASP.NET antiforgery: framework signing and encryption protect the token pair, but OWASP still requires separate cookie and lifecycle checks [31][18]. The lesson is to avoid collapsing CSRF protection, authentication, and session revocation into one label.

## 8. Safe Pre-Authorization Work Versus Letter-Gated Work

| Activity | Safe before the signed scope letter | Requires the letter and two test accounts |
|---|---|---|
| Read public MUJ landing pages and public vendor documentation | Yes, at normal human rate and subject to owner policy [38] | No |
| Study OWASP, RFC, Microsoft, and tool documentation | Yes | No |
| Build parsers and dashboards against synthetic tokens and a local MVC/OIDC lab | Yes | No |
| Inspect the browser and cookies of a personally controlled lab or test environment | Yes | No |
| Download, install, and configure Burp, ZAP, mitmproxy, JWT Editor, AuthMatrix, jwt_tool, or Postman | Yes, without connecting to MUJ | No |
| Read publicly published OIDC discovery or JWKS metadata | Generally low risk, but obtain owner permission if the target's policy forbids automated requests | No for a lab; target automation should be named in scope |
| Proxy an authenticated MUJ browser session | No | Yes |
| Capture, decode, mutate, replay, or compare MUJ cookies, JWTs, authorization codes, refresh tokens, or `enc` values | No | Yes |
| Test session rotation, logout, SSPR, OTP, MFA enrollment, password reset, or revocation | No | Yes |
| Test cross-user, cross-role, cross-tenant, or parent-child authorization | No | Yes, with named test objects and explicit tenant boundaries |
| Exercise rate limits, lockout, error differentials, or active scanning | No | Yes, with written rates, stop conditions, and cleanup |
| Query or tune production Entra/Sentinel telemetry | Read-only defensive review may be allowed by the owner; do not assume permission | Yes for test correlation, alert changes, or admin revocation |

The safe pre-authorization boundary is therefore mostly offline and observational. Even a benign-looking proxy request can transmit a cookie, generate an identity event, trigger an OTP, or change a server-side session. The signed letter should name the hostnames, tenants, accounts, roles, time window, source addresses, permitted tools, rate limits, prohibited actions, escalation contact, data handling rules, and cleanup procedure.

## VERDICT

**Confidence: High for the technique universe and tool capability mapping; medium for prioritization against the reported MUJ architecture; low for any claim that MUJ is currently vulnerable.**

The evidence supports a readiness conclusion, not a vulnerability conclusion. The campaign has a strong identity-design lead: Microsoft 365 single-password behavior, SSPR, OTP-gated parent accounts, and a dual-tenant split make recovery, tenant mapping, session lifecycle, and token replay the right next areas. The campaign does not yet support a claim that MFA is absent, that a JWT is accepted, that the `enc` value is forgeable, that the antiforgery cookie is the authentication cookie, or that an old session survives reset. Those remain unknowns.

The immediate go/no-go decision is straightforward. Before authorization, proceed with public-document review, local lab construction, synthetic-token parsing, tool installation, detection-query design, and a written two-account matrix. After the signed scope letter and account provisioning, begin with passive authenticated capture, token inventory, session rotation, logout, and server-side logging. Only then perform tightly bounded reset, OTP, tenant, authorization, replay, and `enc` differential tests. A stop condition is any action affecting a non-test identity, any durable account change not explicitly approved, any unexpected authorization success, any uncontrolled OTP or notification, or any inability to correlate the action in logs.

The recommended campaign deliverable is not a list of mutated tokens. It is a defensible evidence bundle for each hypothesis: scope ID, test account and tenant, redacted request and response, token class and hash, expected decision, actual decision, application correlation ID, Entra event, cleanup result, and a clear statement of whether the result is a vulnerability, a hardening observation, an inconclusive implementation difference, or an untested condition.

## References

1. *WSTG - v4.2 | OWASP Web Security Testing Guide*. https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/06-Session_Management_Testing/03-Testing_for_Session_Fixation/
2. *Secure applications and APIs by validating claims - Microsoft identity platform | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity-platform/claims-validation
3. *ZAP – Authentication Helper*. https://www.zaproxy.org/docs/desktop/addons/authentication-helper/
4. *GitHub - SecurityInnovation/AuthMatrix: AuthMatrix is a Burp Suite extension that provides a simple way to test authorization in web applications and web services. · GitHub*. https://github.com/SecurityInnovation/AuthMatrix
5. *WSTG - Latest | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/05-Testing_for_OAuth_Weaknesses
6. *Access activity logs in Microsoft Entra ID - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/monitoring-health/howto-access-activity-logs
7. *Access tokens in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens
8. *rfc-editor.org*. https://www.rfc-editor.org/rfc/rfc7636.html
9. *WSTG - v4.2 | OWASP Web Security Testing Guide*. https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/06-Session_Management_Testing/05-Testing_for_Cross_Site_Request_Forgery/
10. *GitHub - ticarpi/jwt_tool: :snake: A toolkit for testing, tweaking and cracking JSON Web Tokens · GitHub*. https://github.com/ticarpi/jwt_tool
11. *GitHub - PortSwigger/jwt-editor: A Burp Suite extension for creating and editing JSON Web Tokens. This tool supports signing and verification of JWS, encryption and decryption of JWE and automation of several well-known attacks against applications that consume JWT. · GitHub*. https://github.com/PortSwigger/jwt-editor
12. *rfc-editor.org*. https://www.rfc-editor.org/rfc/rfc6750.html
13. *WSTG - Latest | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/05.1-Testing_for_OAuth_Authorization_Server_Weaknesses
14. *WSTG - v4.2 | OWASP Web Security Testing Guide*. https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/06-Session_Management_Testing/01-Testing_for_Session_Management_Schema/
15. *Refresh tokens in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity-platform/refresh-tokens
16. *rfc-editor.org*. https://www.rfc-editor.org/rfc/rfc6749.html
17. *Working with JWTs in Burp Suite - PortSwigger*. https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/session-management/jwts
18. *WSTG - v4.2 | OWASP Web Security Testing Guide*. https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/06-Session_Management_Testing/02-Testing_for_Cookies_Attributes/
19. *Concept Sspr Howitworks*. https://learn.microsoft.com/en-us/entra/identity/authentication/concept-sspr-howitworks
20. *Forgot Password - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html
21. *Send Microsoft Entra ID data to Microsoft Sentinel | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/sentinel/connect-azure-active-directory
22. *Revoke user access in an emergency in Microsoft Entra ID - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/users/users-revoke-access
23. *Burp Suite Terms & Conditions of Supply - PortSwigger*. https://portswigger.net/burp/eula
24. *GitHub - mitmproxy/mitmproxy: An interactive TLS-capable intercepting HTTP proxy for penetration testers and software developers. · GitHub*. https://github.com/mitmproxy/mitmproxy
25. *How Token Protection Enhances Conditional Access Policies - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-token-protection
26. *WSTG - Latest | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/09-Testing_for_Weak_Password_Change_or_Reset_Functionalities
27. *OpenID Connect (OIDC) on the Microsoft identity platform - Microsoft identity platform | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols-oidc
28. *Learn about the monitoring and health activity log schemas - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-activity-log-schemas
29. *Continuous access evaluation in Microsoft Entra - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-continuous-access-evaluation
30. *WSTG - Latest | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/11-Testing_Multi-Factor_Authentication
31. *XSRF/CSRF Prevention in ASP.NET MVC and Web Pages | Microsoft Learn*. http://learn.microsoft.com/en-us/aspnet/mvc/overview/security/xsrfcsrf-prevention-in-aspnet-mvc-and-web-pages
32. *Burp Suite Professional - PortSwigger*. https://portswigger.net/burp/pro
33. *Authentication - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
34. *ZAP – Report Generation*. https://www.zaproxy.org/docs/desktop/addons/report-generation/
35. *Session Management - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
36. *Automation Framework - ZAP*. https://www.zaproxy.org/docs/automate/automation-framework/
37. *Authenticate with OAuth 2.0 authentication in Postman*. https://learning.postman.com/v11/docs/use/send-requests/authorization/oauth-20
38. *http://mujslcm.jaipur.manipal.edu/Home/Index*. http://mujslcm.jaipur.manipal.edu/Home/Index
39. *Plans & Pricing | Postman API Platform*. https://www.postman.com/pricing/
40. *Buy Fiddler Everywhere | Telerik*. https://www.telerik.com/purchase/fiddler
41. *Fiddler Everywhere Exporting and Importing HTTPS Traffic ...*. https://www.telerik.com/fiddler/fiddler-everywhere/documentation/collaboration/exporting-and-importing
