# SLCM Session Security: Safe Tests and Defensive Decisions

## Executive Summary

- **Live Posture Remains Unknown**: The public MUJ page proves that a portal and sign-in choices exist, but it exposes no authenticated cookie, timeout, concurrency, or server-side store behavior [2] -> do not call SLCM vulnerable or secure until MUJ authorizes an authenticated assessment.
- **Architecture Is A Scope Assumption**: ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 identity were supplied in the brief, not independently established by the cited public content -> revalidate versions and request flow with the service owner before selecting framework-specific remediation.
- **Three Cookie Flags Solve Different Problems**: `HttpOnly` blocks compliant client-side script from reading a cookie, while `Secure` restricts return of the cookie to TLS and SameSite constrains cross-site sending [12][18][14] -> inspect each attribute separately on every session and authentication cookie.
- **Framework Defaults Are Not Evidence Of SLCM Configuration**: The documented generic `HttpCookie.HttpOnly` and `HttpCookiesSection.HttpOnlyCookies` defaults are false, `HttpCookiesSection.RequireSSL` defaults to false, the session-state timeout default is 20 minutes, and Forms Authentication defaults to a 30-minute timeout with sliding expiration enabled [12][17][18][15][13][16] -> use these only as configuration-review prompts, never as findings about SLCM.
- **Fixation Is The Highest-Value Lifecycle Test**: OWASP requires a new session token on authentication and rejects URL exposure; its session guidance also requires renewal after a privilege change and rejection of IDs the application did not generate [21][8] -> compare pre-login and post-login identifiers using one authorized account, then verify the old identifier is unusable.
- **Authentication And Session State Can Expire Differently**: Classic ASP.NET documents separate session-state and Forms Authentication timeout controls, and Forms Authentication can renew after half its configured interval [15][13][16] -> test local authorization, session data, and identity-provider state independently rather than treating one redirect as proof that all sessions ended.
- **Concurrent Login Is A Policy Decision, Not Automatically A Vulnerability**: OWASP says the application decides whether simultaneous logons are allowed, but recommends active-session visibility, concurrent-login alerts, and remote termination [8] -> obtain MUJ's intended policy before assigning severity, then test it in two owned browser profiles.
- **Microsoft Revocation Does Not Guarantee Local Session Revocation**: Microsoft states that Entra ID cannot directly revoke a session token issued by an application and that the application must enforce its own authorization policy [4] -> test portal logout, Entra revocation, password change, and local cookie replay as separate events under administrator supervision.
- **Store Choice Changes Failure Mode**: InProc loses sessions on application restart and is unsuitable for a web farm without an architecture compensating control; StateServer and SQLServer survive application restarts and support multiple web servers, while Custom behavior depends on its provider [7] -> verify `Web.config` and deployment topology instead of guessing the provider from black-box behavior.
- **Decision**: No public evidence reviewed here establishes an exploitable SLCM session-management defect. The justified conclusion is **Not Verified, High Priority To Test**, with high confidence in the assessment method and low confidence in the live configuration.

## Scope, Evidence, And Safety Boundaries

This report assesses the session-management questions in the brief for `mujslcm.jaipur.manipal.edu`. A public extraction identifies the page as "WELCOME TO MUJ PORTAL" and exposes sign-in and parent-login labels [2]. That evidence verifies the existence of the public entry point only. It does not reveal post-authentication `Set-Cookie` headers, the relationship between an identity-provider cookie and local application state, expiration behavior, a concurrent-session rule, or the configured state provider.

The claimed stack is therefore recorded as **user-supplied scope information**: ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10 behind Akamai, and Microsoft 365 identity. It is not presented as a fresh OSINT finding. In particular, a broad label such as ".NET Framework 4.x" is not precise enough to establish SameSite behavior because Microsoft added support for the 2019 SameSite draft to patched .NET Framework 4.7.2 and 4.8 in December 2019 [14]. The exact target framework, operating-system patch level, OWIN or other authentication middleware, and effective configuration all matter.

No login, cookie replay, fixation attempt, timeout wait, password change, account revocation, or server restart was performed for this report. Every SLCM-specific outcome below is either **Observed**, **User-supplied**, **Inference**, **Proposed authorized test**, or **Unknown**.

| Evidence class | Exact status in this report | What it can support | What it cannot support |
|---|---|---|---|
| Observed public content | MUJ portal title and public sign-in choices [2] | Entry-point identification and test planning | Authenticated security conclusions |
| User-supplied architecture | MVC 5.3, .NET 4.x, IIS 10, Akamai, Microsoft 365 | Scope hypotheses | Current versions or effective controls |
| Authoritative framework documentation | Microsoft System.Web, Entra, OWIN, and NIST sources | Expected mechanisms and configuration-review questions | SLCM's live settings |
| Authoritative security guidance | OWASP Cheat Sheet, WSTG, and ASVS | Control objectives and pass/fail logic | Proof of an SLCM defect |
| Inference | Explicitly prefixed **Inference** | Prioritization and likely failure mechanisms | A vulnerability finding |
| Proposed authorized test | Not executed | Reproducible verification plan | A reported test result |

Active work must occur only under written MUJ authorization that names the exact hosts, dates, accounts, request limits, data-handling rules, and emergency contacts. Use club-controlled accounts and browser profiles. Do not enumerate users, guess credentials, access another person's records, induce state changes for other users, test XSS as a way to evaluate `HttpOnly`, brute-force session IDs, or recycle production workers. The official MUJ registrar page lists `registrar@jaipur.manipal.edu` and says the Registrar has authority to receive complaints and suggestions for appropriate action [23]. That is a public institutional contact, although MUJ should identify the correct security owner before testing begins.

The request asks for explicit chain-of-thought. I cannot provide private hidden reasoning. Instead, the report provides an auditable decision record: evidence -> mechanism -> bounded test -> pass/fail criterion. This offers reproducibility without exposing private internal deliberation.

## ASP.NET Session Architecture And The Microsoft Identity Boundary

Microsoft describes `SessionIDManager` as the System.Web component that manages identifiers for ASP.NET session state. By default, the identifier travels in a cookie named `ASP.NET_SessionId`; the documented default value is a randomly generated 24-character string [20]. This cookie is an index into server-side state. It should not automatically be equated with the cookie or token that proves the user is authenticated.

Classic ASP.NET exposes separate controls for session state and Forms Authentication. The session-state timeout defaults to 20 minutes [15], while Forms Authentication has a documented 30-minute default and can use sliding expiration [13][16]. **Inference:** if an application uses both mechanisms without coordinating them, the user can remain authenticated after session data disappears, or retain session state after an authentication cookie is rejected. Such mismatch can cause confusing redirects, regenerated carts or workflows, stale privilege context, or incomplete logout. These are hypotheses to test, not observed SLCM behavior.

Microsoft also documents a modern OWIN integration for ASP.NET MVC and Web API applications on .NET Framework 4.7.2 or later, with Entra authentication and automatic token refresh [22]. The brief does not establish that SLCM uses this package, so it is a review branch rather than a finding. If SLCM uses OWIN, Katana, Microsoft.Identity.Web.OWIN, or another OpenID Connect component, its authentication cookie, nonce and correlation cookies, token cache, and System.Web session cookie require separate review.

The identity-provider boundary is especially important. Microsoft documents Entra browser cookies used to facilitate single sign-on [19]. It separately warns that Entra ID cannot directly revoke an application-issued session token [4]. Microsoft further limits the initial Continuous Access Evaluation focus to Exchange, Teams, and SharePoint Online and says not all client and resource combinations are supported [9]. **Inference:** an Entra account disable, refresh-token revocation, or Microsoft 365 sign-out must not be assumed to terminate an already issued local SLCM session.

| Layer | Possible artifact | Security decision it represents | Authorized SLCM verification |
|---|---|---|---|
| Microsoft Entra | Entra SSO cookies or tokens | Identity-provider session and ability to obtain tokens [19] | Observe the approved sign-in and sign-out flow; do not collect tenant-wide data |
| OIDC or OWIN middleware, if present | Local authentication cookie, nonce, correlation cookie, token cache | Local authenticated principal and protocol transaction | Inventory cookie names and flags before, during, and after the callback |
| System.Web session state | `ASP.NET_SessionId` by default [20] | Lookup key for server-side application state | Compare identifier and state lifecycle across login, privilege change, timeout, and logout |
| Application authorization | Server-side role and ownership checks | Whether a request is permitted | Use only the tester's own records and approved roles; never infer authorization from UI visibility |
| Akamai and IIS, if the supplied architecture is accurate | Edge and origin request handling | TLS termination, routing, caching, and process lifetime | Configuration review with owners; do not infer origin topology from the public page |

**Decision-ready insight:** the minimum complete test tracks at least two lifecycles: the application authentication session and `ASP.NET_SessionId`. A third lifecycle, the Entra SSO session, matters for logout and emergency revocation. Passing a test at one layer does not prove the others terminate.

## Cookie Controls: Three Flags, Three Failure Modes

`HttpOnly`, `Secure`, and SameSite are complementary, not interchangeable. Microsoft defines `HttpOnly` as making a cookie inaccessible to client-side script in a compliant browser [12]. It also cautions that `HttpOnly` does not protect the cookie from an attacker who can access the network channel, which is why transport protection remains necessary [12]. The `Secure` configuration causes compliant browsers to return the cookie only over SSL or TLS [18]. Microsoft describes SameSite as providing some CSRF protection; cookies without an attribute are commonly treated as Lax by modern browsers, while `SameSite=None` permits cross-site use and must be paired with `Secure` [14].

The generic System.Web API defaults are dangerous to treat as live evidence. `HttpCookie.HttpOnly`, the global `httpOnlyCookies` switch, and `RequireSSL` are documented with false defaults [12][17][18]. Framework components can override generic defaults, patches can change behavior, and application code or middleware can issue cookies independently. The only reliable SLCM result comes from an effective response capture plus configuration review.

| Control | Threat reduced | What a pass looks like | Exact authorized test | Important limitation |
|---|---|---|---|---|
| `HttpOnly` | Script reading and exfiltration of the cookie | Every sensitive session or authentication cookie has `HttpOnly` unless a documented protocol requirement forbids it | In browser developer tools or an approved intercepting proxy, record each `Set-Cookie` attribute on landing, login initiation, callback, authenticated navigation, and renewal | Do not attempt XSS. `HttpOnly` does not stop a script from causing authenticated requests and does not replace XSS prevention [12] |
| `Secure` | Browser transmission of the cookie over cleartext HTTP | Sensitive cookies include `Secure`; HTTP redirects to HTTPS before any sensitive cookie is set or sent | Start a fresh owned profile, request the public HTTP entry once, and inspect the redirect chain and cookie transmission | A redirect alone is insufficient if a cookie was emitted or sent before the redirect |
| `SameSite` | Some cross-site request and leakage scenarios | Explicit value chosen per cookie and flow; `None` is paired with `Secure` [14] | Inspect attributes first. If functional validation is approved, use only a benign, non-state-changing callback or test-environment flow | Strict can break federated callbacks; Lax or None may be necessary for particular OIDC response modes. SameSite is not a complete CSRF defense |
| `Domain` | Cross-subdomain cookie exposure | Narrow host scope unless sharing is documented | Record whether the cookie is host-only or has a `Domain` attribute; compare all cookies with the same name | **Inference:** a broad parent-domain cookie can increase sibling-subdomain influence |
| `Path` | Unnecessary route exposure | Narrowest functional path, or a documented reason for `/` | Record `Path` and check for duplicate names on different paths | Narrow Path is containment, not an authorization boundary |
| Prefix and lifetime | Cookie-origin hardening and unintended persistence | Session identifiers are non-persistent unless persistence is explicitly required; optional host-prefix use is valid | Record `Expires`, `Max-Age`, prefix, and creation or renewal time | Client persistence does not prove server-side validity |

### Case study: SameSite and federated login

**Proposed case study, not performed:** capture cookies in an authorized SLCM login using one clean browser profile. Separate the pre-login `ASP.NET_SessionId`, the local authentication cookie, and any short-lived OIDC nonce or correlation cookies. Microsoft notes that SameSite behavior in classic ASP.NET depends on patched framework support and that `SameSite=None` must be Secure [14].

The failure pattern to avoid is a blanket change of every cookie to Strict. **Inference:** that can improve apparent scanner results while breaking an identity-provider callback that legitimately starts cross-site. The correct decision is per-cookie: Strict or Lax where the flow permits, and None plus Secure only where cross-site protocol behavior requires it. Validate both security attributes and successful sign-in after the change.

**Decision-ready insight:** a report that says only "the session cookie is Secure" is incomplete. The evidence record must contain cookie name, issuing response, Domain, Path, HttpOnly, Secure, SameSite, persistence, and whether its value changed at each lifecycle event.

## Session Fixation And Post-Login Regeneration

Session fixation differs from random session guessing. The dangerous condition is that a preselected or attacker-influenced identifier survives authentication and becomes associated with the victim's authenticated state. OWASP requires a new token on authentication and says session tokens must not appear in URL parameters [21]. Its session guidance also requires renewal after a privilege-level change, recommends cookie-only exchange, and says an application should not accept a session ID it never generated [8].

System.Web can be configured for cookieless sessions, in which the session identifier is placed in the URL [20]. That capability is not evidence that SLCM uses it. It establishes a concrete configuration-review question: require cookies and reject alternate transports. A URL-carried identifier can leak into history, copied links, referrers, logs, screenshots, and support tickets. The safe result is therefore no session token in paths, query strings, hidden fields, or ad hoc headers unless a separately reviewed protocol requires it.

| Fixation vector | SLCM-specific hypothesis | Bounded authorized test | Pass criterion | Severity condition |
|---|---|---|---|---|
| Pre-login cookie retained after login | Anonymous `ASP.NET_SessionId` becomes privileged | Record the pre-login value, authenticate the owned account normally, then record all post-login cookies | Privileged session uses a newly issued binding secret; old value cannot recover authenticated state [21][10] | High if another party can set or learn the old value and it becomes authenticated |
| Application accepts an unissued ID | Server adopts a syntactically valid value it did not create | In staging, or once in production only if explicitly approved, submit one non-sensitive request with a clearly synthetic valid-format value | Server rejects it or issues its own new identifier [8] | High if the supplied value is retained through login |
| URL or form transport | Session ID appears outside cookies | Inspect redirects, callback URLs, form fields, browser history, and approved proxy history; do not publish live tokens | No session token outside cookies [21][8] | High because URLs and forms have broader leakage paths |
| Broad-domain overwrite | A sibling subdomain can influence a parent-scoped cookie | Configuration review first; any cross-subdomain validation must be in a test environment | Host-only scope or documented trusted sharing; deterministic duplicate-cookie handling | Depends on sibling-domain trust and parser behavior |
| Duplicate cookie names | Edge, IIS, and application select different values | In staging, create two same-name cookies with different approved Path or Domain scopes | Request is rejected or every layer selects the same intended cookie | High if security layers disagree |
| Login rotates auth cookie but not state ID | Authentication changes while pre-auth state binding survives | Compare both cookie families, not only the auth cookie | Every security-relevant pre-auth binding is replaced or safely migrated | Context-dependent; lower if the retained ID cannot influence or expose authenticated state |
| Privilege elevation without rotation | Role or administrative function reuses a lower-privilege ID | Using an approved role-changing test account, compare identifiers immediately before and after elevation | New binding after privilege change [8] | High if the old token retains elevated access |
| Logout leaves old ID valid | Browser deletes a cookie but server record remains | Log out, then replay one previously captured owned-account request in the approved harness | Server denies it and creates no authenticated state [8][21] | High if old token still authorizes access |

### Case study: two-cookie rotation can create a false pass

**Proposed case study, not performed:** suppose the Microsoft identity callback issues a new local authentication cookie while `ASP.NET_SessionId` remains unchanged. A scanner that watches only the authentication cookie reports rotation. That is not enough to decide fixation safety because pre-login data could still be keyed by the unchanged state identifier.

**Inference:** unchanged `ASP.NET_SessionId` is not automatically exploitable. If authentication and authorization rely on a separate protected cookie, the state ID was never attacker-influenceable, and no sensitive state is attached to it, impact may be limited. The assessor must establish the complete chain: influence or disclosure of the old ID -> survival across authentication -> attachment of privileged or sensitive state -> successful reuse. Report each link separately and stop if any link would require another user's session.

Remediation should regenerate the security binding at login and privilege changes, copy only allowlisted pre-authentication state into the new session, abandon the old server-side state, and invalidate both authentication and state artifacts at logout. Log lifecycle events using a one-way correlation value rather than raw session secrets; OWASP recommends recording creation, renewal, destruction, login, logout, privilege changes, timeout expiration, and invalid-session activity [8].

## Idle, Sliding, Absolute, Logout, And Concurrent Sessions

Timeout testing must distinguish at least four clocks: System.Web session inactivity, local authentication inactivity, absolute session age, and the identity-provider or token lifetime. Microsoft documents a 20-minute default for `SessionStateSection.Timeout`, a 30-minute Forms Authentication default, and renewal of a sliding Forms Authentication cookie when a user browses after half the interval [15][16][13]. These are framework defaults, not SLCM findings.

OWASP states that all sessions should have idle and absolute timeouts and that expiration must be enforced server-side [8]. NIST similarly requires termination when either inactivity or overall timeout expires, says activity resets inactivity, and says successful reauthentication resets both [10]. NIST also says users should have an accessible logout mechanism and that logout invalidates the session-binding secret [10].

| Test | Controlled sequence | Evidence to capture | Pass condition | Failure interpretation |
|---|---|---|---|---|
| Idle timeout | Authenticate an owned account, make no requests, then request a harmless page just before and just after the owner-declared limit | Last server activity, response status, redirect chain, new cookies, and whether old cookie replay works | Server rejects old authentication/state after the limit | Client cookie deletion alone is not proof of invalidation |
| Sliding renewal | Make one harmless request after more than half the declared local-auth interval, then observe renewal | `Set-Cookie` time and value before and after the midpoint | Behavior matches documented policy; renewal does not bypass absolute age | Silent indefinite renewal indicates missing or ineffective absolute limit |
| Absolute timeout | In staging, send one low-frequency harmless request below the idle threshold until the declared maximum age | Original authentication time and final rejection time | Session ends at the absolute cap despite activity [8] | Continued authorization indicates no effective absolute bound |
| Logout | Log out through the UI and make one replay of an owned-account request | Server response, cookie deletion, state invalidation, back-button behavior | Both local authentication and state are invalid; back navigation cannot resume the session [21] | UI redirect with server-valid old token is a failure |
| Browser close | Close all profile windows and reopen | Persistence attributes and restored state | Outcome matches documented policy | This does not replace server timeout testing |
| Entra revocation | MUJ administrator revokes the test user while local sessions exist | Revocation time, token refresh result, local portal result | Result matches MUJ incident policy; local session is terminated within its declared bound | Entra cannot directly revoke application-issued session tokens [4] |
| Password change or reset | Change the test password under administrator supervision | Both browsers' post-change state and session inventory | Other sessions terminate if that is MUJ's chosen control; ASVS expects effective cross-application and federated termination [185 snippet; 200.35] | Record IdP and local outcomes separately |

The exact timeout values should be policy-driven. Do not claim that NIST mandates a particular SLCM duration from the session overview alone; the retrieved NIST page points to assurance-level sections for exact durations [10]. A reasonable assessment records MUJ's data classification, device-sharing risk, user friction, and reauthentication support, then checks implementation against the approved policy.

### Concurrent session policy

OWASP explicitly treats simultaneous logon as an application design decision. If concurrency is forbidden, the application should terminate the old session or ask the user which session remains active. Even when concurrency is allowed, OWASP recommends active-session details, concurrent-login alerts, and remote termination [8]. Therefore, two working sessions are not, by themselves, a vulnerability.

| Intended policy | Browser A and Browser B test | Expected deterministic result | Security follow-up |
|---|---|---|---|
| Single active session | Log in to the same owned account in A, then B | A is invalidated, or the user selects which session remains | Confirm invalidation is server-side and survives replay |
| Limited concurrency | Repeat only up to the approved limit | Oldest or selected session ends according to policy | Verify race-free enforcement and clear notification |
| Unlimited concurrency with visibility | Log in from two owned profiles | Both remain active and appear in an inventory | Verify user can identify and terminate either session |
| Risk-triggered concurrency | Use only owner-approved network and device variations | Step-up, warning, or termination follows documented risk rules | Do not spoof unrelated users or evade controls |
| Emergency revocation | Administrator revokes the test account | All local and IdP-related sessions terminate within declared bounds | Record any residual local session as a separate finding |

**Decision-ready insight:** the strongest SLCM design is not necessarily "one browser only." It is a documented rule with deterministic enforcement, user-visible active sessions, remote termination, alerts for meaningful anomalies, and reliable global revocation after account recovery.

## Server-Side Session Store Risks Across Four Modes

Microsoft documents four relevant System.Web choices. InProc keeps state inside the local worker process and loses it on application restart; StateServer stores serializable objects in a separate ASP.NET state service; SQLServer stores serializable state in a database; and Custom delegates behavior to a provider [7]. Microsoft separately documents InProc session loss when the AppDomain or worker process is recycled [119 source].

| Mode | Documented behavior | Primary security or resilience risk | Best verification | SLCM inference |
|---|---|---|---|---|
| InProc | Local worker memory; default mode; no restart persistence; unsuitable for a web farm as documented [7] | Forced logout and workflow loss on recycle; inconsistent state if requests reach different nodes | `Web.config`, IIS topology, recycle policy, and a staging-only recycle test | **Inference:** if the supplied Akamai architecture fronts multiple origin nodes, affinity or a shared store would be required; Akamai presence alone does not prove a multi-node origin |
| StateServer | Separate ASP.NET state service; survives app restart; supports web farms; objects must be serializable [7] | Network-service availability, endpoint exposure, serialization boundaries, and stale data | Inspect `stateConnectionString`, firewall rules, service identity, encryption controls, retention, and failover | **Inference:** black-box persistence across a restart suggests but does not prove StateServer |
| SQLServer | SQL database; survives restart; supports web farms; serializable objects required [7] | Database compromise can expose concentrated session state; availability and cleanup affect all sessions | Inspect database permissions, encrypted transport, protected secrets, cleanup jobs, monitoring, and recovery | **Inference:** avoid storing complete student records when a minimal identifier will do |
| Custom | Provider-defined [7] | Unknown cryptography, serialization, expiry, atomicity, and failover | Code review, provider threat model, integration tests, and operational runbook | Treat as unverified until provider behavior is documented |
| Off or stateless application | No System.Web state provider | Authentication token lifecycle becomes the dominant control | Verify no code assumes Session values for authorization | `ASP.NET_SessionId` might still appear only if a component creates state; confirm empirically |

### Case study: InProc restart versus a shared store

Microsoft's InProc model is fast because values remain in the local worker process, but it does not preserve state when the application restarts [7]. **Proposed staging case study, not performed:** authenticate a test account, place a harmless marker in an approved workflow, recycle the staging application pool, and request the page again. The expected InProc outcome is loss of server-side session data; the expected shared-store outcome is persistence, subject to policy.

The result is mostly an availability and consistency finding, not automatically account compromise. **Inference:** the security issue becomes more serious if authorization decisions are cached only in Session, if a failover reconstructs incomplete privilege context, or if stale shared-state records outlive authentication. The remediation is not simply "use SQLServer." It is to make authorization authoritative on every request, minimize session contents, align expiry with authentication, protect the store, and test failure behavior.

Configuration review is superior to black-box inference. StateServer uses a `stateConnectionString`, SQLServer uses a `sqlConnectionString` and installed session database, and Custom names a provider in `Web.config` [7]. Review service accounts, least privilege, network reachability, transport encryption, secret protection, data classification, serialization types, cleanup, monitoring, backups, and failover. Never trigger production recycling or database failure from a university-club test.

## Authorized SLCM Test Plan And Exact Evidence Schema

The plan below is intentionally bounded. It avoids destructive actions and other users' data. "Production allowed" still means written authorization.

| ID | Focus item | Environment | Exact action | Exact pass criterion | Stop condition |
|---|---|---|---|---|---|
| SLCM-01 | Public baseline | Production, passive | One fresh-profile request to HTTP and HTTPS public landing pages | HTTPS is canonical; no sensitive cookie crosses HTTP | Unexpected state change, instability, or scope redirect |
| SLCM-02 | Cookie inventory | Production with owned account | Capture `Set-Cookie` on landing, login initiation, callback, first authenticated page, renewal, and logout | Every sensitive cookie has justified HttpOnly, Secure, SameSite, Domain, Path, and lifetime | Any token or personal data appears in a shareable log |
| SLCM-03 | Post-login regeneration | Production if explicitly approved | Compare all pre-login and post-login cookie values | New security binding; old values cannot restore authenticated state [21] | Test would require another user's browser or token |
| SLCM-04 | Alternate transport rejection | Staging preferred | Check approved benign request handling for URL, form, or unissued session IDs | Cookie-only; unissued and alternate-transport IDs are rejected [8] | Any request reaches sensitive function |
| SLCM-05 | Idle and sliding timeout | Production with owned account | Wait around declared limits and make one harmless midpoint request | Server behavior matches policy; old token rejected after expiry [8] | Repeated unexpected errors or account lockout |
| SLCM-06 | Absolute timeout | Staging | Maintain low-frequency activity below idle limit until declared absolute cap | Server terminates at cap [8] | Load, maintenance conflict, or no approved duration |
| SLCM-07 | Logout replay | Production if approved | Log out, then replay one previously captured owned-account request | Server denies; both local auth and state are invalid [8][21] | Replay would alter data |
| SLCM-08 | Concurrent sessions | Production with owned account | Use two clean browser profiles according to approved policy | Deterministic allow, limit, warn, inventory, or terminate result [8] | Anomaly controls affect unrelated systems |
| SLCM-09 | Password and Entra revocation | Staging or administrator-supervised window | Change password or revoke test user, then check both owned sessions once | Result matches incident policy; no undeclared residual local session | No identity administrator or rollback plan |
| SLCM-10 | Store and recycle | Configuration review plus staging | Inspect provider and perform controlled staging restart | Documented persistence, expiry, failover, and no authorization inconsistency | Never recycle production |
| SLCM-11 | Logging | Configuration review | Review lifecycle events without reading raw session secrets | Creation, renewal, destruction, login, logout, privilege change, timeout, and invalid activity are correlatable [8] | Logs expose reusable credentials |

For every executed case, preserve the following exact fields. Hash or redact reusable secrets before they leave the controlled evidence system.

| Evidence field | Required value |
|---|---|
| Authorization | Approver, ticket, exact host, account, date, and permitted actions |
| Request | UTC timestamp, method, path without secret query data, and response status |
| Cookie | Redacted name or approved name, salted one-way correlation value, Domain, Path, HttpOnly, Secure, SameSite, Expires, Max-Age |
| Lifecycle event | Anonymous start, login initiation, callback, authenticated use, renewal, privilege change, timeout, logout, or revocation |
| Identity state | Entra sign-in state, local authentication state, and System.Web session state recorded separately |
| Expected result | Policy or cited control objective |
| Actual result | Exact observed behavior without interpretation |
| Decision | Pass, fail, inconclusive, or not tested |
| Safety | Request count, data touched, stop condition, cleanup completed |

### Prioritized remediation decisions

| Priority | Decision | Why now | Verification after change |
|---|---|---|---|
| P0 | Rotate at authentication and privilege change; invalidate at logout | Fixation and residual sessions directly affect account boundaries [8][21] | Repeat SLCM-03 and SLCM-07 |
| P0 | Explicitly secure every authentication and state cookie | Generic defaults cannot be trusted, and each attribute covers a different threat [12][18][14] | Repeat SLCM-02 across the entire login flow |
| P1 | Align idle, sliding, absolute, and identity-token lifetimes | Separate clocks can create residual authorization or user confusion [15][13][10] | Repeat SLCM-05 and SLCM-06 |
| P1 | Implement active-session visibility and revocation | Concurrency is safest when users can see and terminate sessions [8] | Repeat SLCM-08 and SLCM-09 |
| P1 | Review store topology and minimize stored data | Each provider has different restart, farm, and concentration risks [7] | Configuration review and SLCM-10 |
| P2 | Correlate lifecycle logs without raw tokens | Detection requires creation, renewal, destruction, and anomaly events [8] | SLCM-11 plus an alert exercise |

## Synthesis

The controls fall into four different mechanisms. Cookie attributes constrain browser handling. Rotation prevents continuity across a privilege boundary. Timeouts and logout limit continuity over time. Concurrent-session and store controls manage continuity across devices and infrastructure. None substitutes for another.

| Dimension | Cookie attributes | Rotation and fixation defense | Timeout and logout | Concurrency controls | Store controls |
|---|---|---|---|---|---|
| Mechanism | Browser-enforced transport, script-access, and cross-site rules | Replaces the binding secret at authentication or privilege change | Ends validity after inactivity, age, logout, or revocation | Governs multiple bindings for one account | Protects and expires state behind the identifier |
| Primary scope | Each cookie | Security transitions | Time and user action | Account-wide session inventory | IIS process, service, database, or custom provider |
| Main failure | Missing flag or wrong SameSite value | Pre-auth or old token becomes privileged | Client appears logged out while server token remains valid | Undocumented residual sessions | Loss, inconsistency, over-retention, or concentrated compromise |
| Evidence | `Set-Cookie` and browser behavior | Before/after identifier correlation and old-token denial | Timed server responses and replay denial | Two owned profiles and administrator events | `Web.config`, topology, code, logs, and staging failure tests |
| Trade-off | Strict settings can break federation | State migration must preserve only safe pre-auth data | Short limits increase friction; long sliding sessions increase exposure | Single-session rules can disrupt legitimate multi-device use | Shared stores improve continuity but add dependencies and sensitive concentration |
| Time horizon | Per response and request | At login, elevation, recovery, and logout | Minutes to overall session lifetime | Entire account lifetime | Deployment and operations lifecycle |

Three non-obvious tensions matter most.

First, federated login can conflict with an indiscriminate SameSite policy. Microsoft supports explicit SameSite control in patched classic ASP.NET and requires Secure when SameSite is None [14]. The correct design is not the strictest label everywhere; it is the narrowest value that preserves the authorized OIDC flow for each cookie.

Second, a successful Entra revocation does not prove local termination. Microsoft says application-issued session tokens require application enforcement [4]. Therefore, emergency account response must join identity administration with local session inventory and revocation. CAE should not be credited to SLCM unless its exact client and resource combination supports it [9].

Third, infrastructure resilience and confidentiality can pull in opposite directions. InProc limits state to a worker's memory but loses it on restart and does not naturally support a farm [7]. StateServer and SQLServer improve continuity across restarts and servers [7], but **Inference:** they concentrate reachable serialized state and require stronger network, identity, expiry, and monitoring controls. The recommendation is architecture-specific, not a universal migration to a database.

The holistic sequence is therefore: establish written policy -> inventory every token -> verify cookie controls -> verify rotation and rejection of old or unissued IDs -> measure all timeout clocks -> test logout and concurrent-session revocation -> review state-store configuration and failure behavior -> confirm lifecycle logging. A defect should be reported only when the authorized observation, security consequence, and reproducible evidence all exist.

## VERDICT

**Verdict: NOT VERIFIED - HIGH PRIORITY FOR AUTHORIZED TESTING.**

No cited public evidence proves that the MUJ SLCM portal lacks `HttpOnly`, `Secure`, or an appropriate SameSite value. No public evidence proves session fixation, missing post-login regeneration, an excessive or sliding-only lifetime, an unsafe concurrency rule, ineffective logout, or an exposed server-side store. Conversely, the public landing page cannot prove that any of those controls are correctly implemented [2].

**Confidence in live SLCM security posture: Low.** Authenticated responses and internal configuration were not available, and the supplied product versions were not independently verified.

**Confidence in the test and review methodology: High.** The control objectives and mechanisms are grounded in Microsoft System.Web and Entra documentation, NIST session requirements, and OWASP WSTG, Cheat Sheet, and ASVS guidance [10][8][7][14][21].

**Overall confidence in the verdict: Moderate.** The negative conclusion is narrow: there is insufficient public evidence to claim a vulnerability. The prioritization is stronger: post-login rotation, complete cookie flags, server-side timeout and logout, concurrent-session revocation, and store review are the correct first checks.

The club should submit the proposed plan to MUJ, obtain a named owner and written authorization, execute SLCM-01 through SLCM-11 with only controlled accounts, and report actual results as Pass, Fail, Inconclusive, or Not Tested. Until that occurs, scanner-derived framework names and generic defaults must remain hypotheses rather than findings.

## References

1. *Session data is lost if you use InProc - ASP.NET | Microsoft Learn*. https://learn.microsoft.com/en-us/troubleshoot/developer/webapps/aspnet/development/session-data-lost-inproc-mode
2. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
3. *SessionStateSection.CookieSameSite Property (System.Web.Configuration) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.configuration.sessionstatesection.cookiesamesite?view=netframework-4.8.1
4. *Revoke user access in an emergency in Microsoft Entra ID - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/users/users-revoke-access
5. *WSTG - Stable | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/06-Session_Management_Testing/07-Testing_Session_Timeout
6. *Session fixation | OWASP Foundation*. https://owasp.org/www-community/attacks/Session_fixation
7. *Session-State Modes | Microsoft Learn*. https://learn.microsoft.com/en-us/previous-versions/aspnet/ms178586%28v%3Dvs.100%29
8. *Session Management - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
9. *Continuous access evaluation in Microsoft Entra - Microsoft Entra ID | Microsoft Learn*. http://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-continuous-access-evaluation
10. *Session Management*. https://pages.nist.gov/800-63-4/sp800-63b/session/
11. *WSTG - Latest | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/06-Session_Management_Testing/02-Testing_for_Cookies_Attributes
12. *HttpCookie.HttpOnly Property (System.Web) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.httpcookie.httponly?view=netframework-4.8.1
13. *FormsAuthenticationConfiguration.SlidingExpiration Property (System.Web.Configuration) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.configuration.formsauthenticationconfiguration.slidingexpiration?view=netframework-4.8.1
14. *Work with SameSite cookies in ASP.NET | Microsoft Learn*. https://learn.microsoft.com/en-us/aspnet/samesite/system-web-samesite
15. *SessionStateSection.Timeout Property (System.Web.Configuration) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.configuration.sessionstatesection.timeout?view=netframework-4.8.1
16. *FormsAuthenticationConfiguration.Timeout Property (System.Web.Configuration) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.configuration.formsauthenticationconfiguration.timeout?view=netframework-4.8.1
17. *HttpCookiesSection.HttpOnlyCookies Property (System.Web.Configuration) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.configuration.httpcookiessection.httponlycookies?view=netframework-4.8.1
18. *HttpCookiesSection.RequireSSL Property (System.Web.Configuration) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.configuration.httpcookiessection.requiressl?view=netframework-4.8.1
19. *Web browser cookies used in Microsoft Entra authentication - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/authentication/concept-authentication-web-browser-cookies
20. *SessionIDManager Class (System.Web.SessionState) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.sessionstate.sessionidmanager?view=netframework-4.8.1
21. *ASVS/4.0/en/0x12-V3-Session-management.md at master · OWASP/ASVS · GitHub*. https://github.com/OWASP/ASVS/blob/master/4.0/en/0x12-V3-Session-management.md
22. *OWIN Integration with Microsoft.Identity.Web | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/msidweb/frameworks/owin
23. *http://jaipur.manipal.edu/administration-registrar.php*. http://jaipur.manipal.edu/administration-registrar.php
