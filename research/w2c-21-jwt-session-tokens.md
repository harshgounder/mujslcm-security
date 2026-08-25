# JWT Boundaries in MUJ's Student Portal Ecosystem

## Executive Summary

- **No Public JWT Finding for SLCM**: The public MUJ SLCM page exposes student and parent sign-in choices, but its citable content does not disclose a JWT, bearer token, cookie name, cookie attributes, or timeout [2]. -> Treat SLCM as a separate, presently undocumented web-session boundary rather than assuming that its Microsoft-branded email accounts make it JWT-based.

- **Brightspace Has Two Distinct Token Planes**: D2L documents OAuth 2.0 bearer access tokens for Brightspace APIs and signed JWT messages for LTI 1.3 launches [7][8]. MUJ's Brightspace use is publicly confirmed for online education, including a D2L case study describing growth to **85,000 online learners in five years** [27]. -> Audit API bearer tokens and LTI launch JWTs as separate protocols with separate audiences, keys, claims, and lifetimes.

- **MUJ Connect Remains an Evidence Gap**: Its public site calls itself MUJ's social place and advertises anonymous posting, while its login page accepts an email or username [5][4]. Neither page discloses JWT use, token storage, signature algorithms, claims, refresh tokens, or expiration [5][4]. -> Do not describe MUJ Connect as JWT-based or vulnerable without first-party documentation or an authorized assessment.

- **Algorithm Policy Must Come From the Verifier**: RFC 8725 requires libraries to let callers specify an allowed algorithm set, forbids use of algorithms outside that set, and requires each key to be bound to exactly one algorithm [12]. -> A verifier must not let an untrusted `alg` header choose security policy.

- **Signature Success Is Necessary but Not Sufficient**: RFC 8725 requires rejection if any cryptographic operation fails, while OWASP says consumers should validate integrity plus expected issuer, audience, expiration, and not-before claims [12][16]. -> Validation should be a fixed contract, not merely a call to a generic `decode()` function.

- **Token Lifetime Is a Risk Budget**: Brightspace permits an OAuth access-token lifetime from **1,800 seconds (30 minutes) to 72,000 seconds (20 hours)** and can optionally issue refresh tokens [7]. Microsoft identity access-token lifetimes are variable and normally randomized between **60 and 90 minutes** [24]. -> Prefer the shortest usable access lifetime, then secure refresh tokens more strongly than access tokens.

- **Cookies and JWTs Fail Differently**: Classic ASP.NET session IDs map a browser to server-side state and expire when the configured inactivity window is exceeded [18]. A self-contained JWT normally needs expiration enforcement and, for immediate termination, a denylist or equivalent state keyed by `jti` [16]. -> Central logout is naturally easier with server sessions; stateless JWT deployments must deliberately restore revocation control.

- **This Is Not a Vulnerability Disclosure**: Public evidence establishes technologies and security requirements, not an exploitable flaw in SLCM, MUJ Connect, Brightspace, or Microsoft 365. Historical JWT library failures show why the controls matter, but do not prove that MUJ uses an affected library [29][30][28]. -> Any active verification must occur only under written authorization, on approved accounts and systems.

## Scope, Evidence Standard, and Safe Analytical Method

This report covers four related but non-equivalent trust boundaries: the public SLCM portal at `mujslcm.jaipur.manipal.edu`, MUJ's Microsoft 365 identity environment, MUJ Connect, and MUJ's D2L Brightspace environment. The public SLCM page confirms that a visitor can choose sign-in and parent-login paths [2]. MUJ's Office 365 setup document identifies itself as an MUJ IT Services guide for students and employees and describes first-time mail-account and MFA configuration [13]. D2L separately identifies Brightspace as central to MUJ's online education strategy [27]. These sources support an ecosystem model, but not a claim that all four applications share tokens, keys, sessions, or identity middleware.

The research brief supplied exact stack labels - ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, and Akamai - but those exact versions were not independently established in the citable public sources reviewed. A passive URLScan record associates the hostname with Microsoft Corporation's network and says the host was not observed in its scan corpus; it does not identify IIS, ASP.NET MVC, .NET, or Akamai [14]. Accordingly, this report treats the supplied stack as a hypothesis or owner-provided baseline, not as an independently verified OSINT result.

The following confidence labels govern the analysis.

| Evidence class | Meaning in this report | Permitted conclusion |
|---|---|---|
| Verified public fact | A first-party page, standards document, vendor document, or official vulnerability record directly states the fact | Report as fact with an inline citation |
| Passive observation | A public page exposes a visible behavior or a passive service records a host | Report narrowly; do not infer hidden configuration |
| Inference | Several verified facts support a plausible architecture or risk | Prefix with **Inference:** and do not present as implementation fact |
| Unknown | Public sources do not disclose the requested detail | State the gap rather than guessing |
| Not established | A searched claim, such as a specific vulnerability, is unsupported | Do not convert absence of evidence into proof of safety |

The requested private chain-of-thought is not disclosed. Instead, the report provides an auditable decision rationale: **observation -> bounded inference -> security implication -> defensive recommendation**. This gives the club reproducible reasoning without exposing hidden internal deliberation or offering instructions for unauthorized access.

No credentials were used, no login was attempted, no token was replayed or modified, and no endpoint was fuzzed. The conclusions come from public pages, public documentation, standards, and vulnerability records. This constraint matters: a public login page can establish that authentication exists, but it cannot establish the post-login cookie name, whether token rotation occurs, whether a backend verifies signatures, or whether logout invalidates a session.

**Decision-ready insight:** Use this report to define questions for MUJ system owners and to build defensive unit tests in an authorized staging environment. Do not use it as a claim that a production weakness has been found.

## MUJ Trust Boundaries: Four Systems, Not One Token Domain

### SLCM: visible login, undocumented post-login session

The citable SLCM landing page shows a MUJ portal with sign-in and parent-login choices [2]. It does not publicly expose a bearer token, JWT header, cookie name, expiration value, signing key endpoint, OAuth authorization endpoint, or OpenID Connect discovery document [2]. That distinction is critical: the presence of an institutional email suffix or a Microsoft password-reset journey would not, by itself, prove that the SLCM application consumes Microsoft ID or access tokens.

**Inference:** Given the supplied legacy ASP.NET MVC/.NET baseline and the server-rendered login experience, SLCM is more likely to use a conventional browser authentication cookie and possibly ASP.NET session state than a browser-managed JWT. The inference is architectural, not a finding about the production response. Microsoft documents that classic ASP.NET normally stores a `SessionID` in a browser session cookie and maps it to session state maintained by the application [18]. The actual SLCM cookie names, authentication-ticket format, flags, timeout, rotation behavior, and server-side storage remain **unknown**.

### Microsoft 365: verified identity environment, unproven SLCM federation

MUJ's own IT Services document is titled "How To Setup Your Office 365 Mail ID," covers first-time account setup and MFA configuration, and identifies students and employees as its audience [13]. It directs users to Microsoft's login service for sign-in [13]. This verifies an MUJ Microsoft 365 identity boundary.

Microsoft ID tokens are JWTs intended to prove authentication to an application [19]. Microsoft access tokens instead authorize calls to a resource; client applications are told to treat them as opaque strings because their contents belong to the target API [24]. APIs, not ordinary clients, must validate access tokens, including signature and issuer checks derived from OpenID configuration [24].

**Inference:** A student may encounter JWTs while using Microsoft 365 even if SLCM itself maintains an unrelated cookie session. Public evidence does not show that a Microsoft token is accepted by SLCM, so token reuse across those boundaries must not be assumed.

### MUJ Connect: visible application, undisclosed token design

MUJ Connect publicly describes itself as MUJ's social place, presents social-networking features, and advertises anonymous posting [5]. Its public login page asks for an email or username and provides a forgotten-password path [4]. These facts establish an application and login surface, not a token format.

The reviewed public content contains no explicit JWT, bearer-token, refresh-token, cookie, expiration, API, or Microsoft identity disclosure [5][4]. **Unknown:** whether MUJ Connect uses a JWT, opaque session token, server cookie, third-party identity token, or a combination. **Not established:** algorithm confusion, missing signature validation, insecure browser storage, excessive token life, or any other vulnerability in MUJ Connect.

### Brightspace: verified MUJ deployment with documented token protocols

D2L's MUJ case study says the university used Brightspace to scale online degree programs from zero to **85,000 students in five years** and describes Brightspace as the heart of its online education strategy [27]. A public Manipal University Jaipur login page is explicitly powered by D2L Brightspace [26]. The strongest scope is therefore MUJ online education; the case study also says Brightspace features enhanced online and on-campus learning, but this does not prove that every residential SLCM user has the same tenant, integrations, or authentication path [27].

D2L recommends OAuth 2.0 for Brightspace APIs and documents use of access tokens followed by refresh tokens [6]. For LTI 1.3, Brightspace acts as an OpenID Connect provider during launch, sends signed JWT messages, and expects the receiver to select a public key by `kid` and verify the signature [8]. These are two different token systems even when they appear in the same LMS.

| Boundary | Publicly verified function | Publicly verified token/session evidence | What remains unknown |
|---|---|---|---|
| MUJ SLCM | Student and parent sign-in [2] | No JWT or cookie format disclosed | Cookie names, flags, timeout, rotation, server state, federation, exact stack versions |
| Microsoft 365 | MUJ mail account and MFA setup [13] | Microsoft ID tokens are JWTs; access tokens authorize APIs [24][19] | Whether SLCM accepts a Microsoft token |
| MUJ Connect | Campus social application and username/email login [5][4] | None disclosed | JWT presence, algorithm, storage, claims, expiry, refresh, revocation |
| MUJ Brightspace | Online learning platform used at large scale [27][26] | OAuth bearer tokens and LTI 1.3 signed JWTs [7][8] | MUJ tenant-specific lifetimes, enabled integrations, key rotation, local policy |

**Decision-ready insight:** Model these as four trust zones. A token issued in one zone should be rejected in another unless issuer, audience, token type, key source, and intended protocol all match an explicit integration contract.

## Exact Token and Session Matrix

| Artifact | Format and state model | Transport or placement | Lifetime evidence | Required validation | MUJ-specific status |
|---|---|---|---|---|---|
| SLCM authentication cookie | **Unknown.** In a classic ASP.NET design, an authentication ticket may be carried in a cookie, but the production format is not public | Browser automatically sends matching cookies | **Unknown** for SLCM | Secure transport, cookie scope, rotation after login, logout invalidation, CSRF defenses | **Inference only:** conventional cookie session is more plausible than exposed JWT |
| ASP.NET `SessionID` pattern | Opaque identifier that maps to server-side state [18] | Normally a non-persistent browser cookie [22] | Session expires after configured inactivity; an expired ID produces a new session [18] | Protect identifier confidentiality; abandon session on logout [18] | Generic framework comparison, not a measured SLCM setting |
| ASP.NET anti-forgery pair | Separate cookie token plus hidden form token; both must pass comparison [23] | Cookie and POST form value | Request-oriented, not an authentication lifetime | Validate both using the framework's anti-forgery mechanism [23] | Generic control; actual SLCM enforcement not established |
| Microsoft ID token | JWT proving authentication to the application [19] | OpenID Connect protocol | Governed by Microsoft token claims and policy | Signature, issuer, audience, and time checks; reject a wrong audience [24] | Verified in Microsoft identity generally; SLCM consumption unproven |
| Microsoft access token | Authorization token for a resource; clients should treat it as opaque and not parse it [24] | Bearer token sent to the target API | Normally randomized **60-90 minutes** [24] | Target API validates token and expected audience [24] | Relevant to Microsoft services, not proven as an SLCM token |
| Brightspace API access token | OAuth 2.0 bearer token [7] | `Authorization: Bearer` header [7] | Configurable **1,800-72,000 seconds** [7] | TLS, exact API scopes, resource-side token validation | Verified D2L capability; MUJ's selected lifetime unknown |
| Brightspace OAuth refresh token | Credential used to obtain a new access token and new refresh token [6] | Token endpoint, not normal resource calls | Longer-lived than an access token by purpose; exact MUJ setting unknown | Confidential storage, rotation handling, revocation, narrowly registered client | Optional in D2L configuration [7] |
| Brightspace LTI 1.3 launch | Signed JWT after OIDC initiation [8] | Browser-mediated launch to a registered tool | `exp`, `iat`, and replay controls apply [32] | Signature, fixed algorithm policy, issuer, audience, nonce, deployment and message claims | Verified protocol; enabled MUJ tools unknown |
| MUJ Connect session/token | **Unknown** | **Unknown** | **Unknown** | Cannot responsibly assess without first-party or authorized evidence | Public pages disclose only login fields, not token internals [4] |

Two common classification errors follow from this matrix. First, an anti-forgery token is not an authentication token: it binds a state-changing request to a browser context, while the authentication cookie identifies the logged-in principal [23]. Second, a bearer access token is not interchangeable with an ID token: Microsoft explicitly distinguishes authorization access tokens from authentication ID tokens [24].

**Decision-ready insight:** Document each artifact by issuer, consumer, protocol, storage location, audience, token type, lifetime, refresh mechanism, and revocation path. If two artifacts cannot fill the same row with identical values, they are not interchangeable.

## JWT Failure Modes: Algorithm, Signature, Claims, Keys, and Replay

### Algorithm confusion is a verifier-policy failure

PortSwigger defines algorithm confusion as forcing a server to verify a JWT with a different algorithm from the one its developers intended; mishandling can permit forged tokens [11]. The canonical asymmetric-to-symmetric variant matters because an RSA public key is public by design, while an HMAC key must remain secret [11]. If a generic verifier accepts either family and lets the header select the family, the trust model collapses.

RFC 8725 provides the controlling rule: callers must specify the supported algorithms, the library must not use others, the JOSE header must match the operation actually performed, and each key must be used with exactly one algorithm [12]. It also says JWTs using `none` should not be generated or consumed unless explicitly requested [12]. For LTI, the 1EdTech Security Framework goes further: tool JWTs must not use `none`; implementations use an approved asymmetric signing algorithm, and RSA deployments must use at least RS256 [32].

**Defensive rule:** Pin the expected algorithm in application configuration for each issuer and token type. Treat `alg` as an assertion to compare against policy, never as the source of policy.

### Missing signature validation turns claims into attacker-controlled text

JWT parsing, Base64url decoding, and signature validation are separate operations. RFC 8725 requires validation of every cryptographic operation and rejection of the entire JWT if any operation fails [12]. OWASP likewise says JWTs must be protected by a signature or MAC, unsecured `alg=none` tokens must not be allowed, and the verifier must not use the JWT header to choose its verification algorithm [16].

A valid signature only establishes integrity under a selected key. It does not prove that the key belongs to the expected issuer, that the token targets the current application, or that its time window is valid. RFC 8725 requires issuer-key binding, validation of subject context, and audience rejection when the current recipient is not named [12]. It recommends explicit token typing and mutually exclusive validation rules when one issuer produces different JWT kinds [12].

**Defensive rule:** A successful signature check should be followed by issuer, audience, subject, token type, expiration, not-before, and application-specific authorization checks. Never treat a decoded role, student identifier, or course claim as trusted before that full sequence completes.

### LTI requires a protocol-specific claim contract

The 1EdTech framework requires LTI ID tokens to carry `iss`, `aud`, `sub`, `exp`, `iat`, and `nonce`; the tool must confirm that `aud` contains its OAuth client ID and that `exp` remains in the future [32]. The nonce binds the launch to a tool session and mitigates replay; receivers should reject a nonce previously seen inside their chosen replay window [32]. Public keys are distributed as JWK sets, and `kid` must identify the selected key even if the set currently contains only one key [32].

The LTI Core specification additionally requires a deployment identifier and a target-link URI matching the value from the initiating OIDC request [31]. These claims stop a correctly signed launch from being transplanted into the wrong deployment or link context.

**Defensive rule:** Do not validate an LTI launch with a generic "JWT valid" helper alone. Enforce the LTI message type, version, deployment, target link, issuer, audience, nonce, timestamps, registered key source, and tool-specific authorization.

## Expiry, Storage, Revocation, and Browser Threats

RFC 7519 says the current time must be before `exp` and after or equal to `nbf`; only a small clock-skew allowance, usually no more than a few minutes, is appropriate [15]. Expiration therefore needs active enforcement by the consumer. Merely including an `exp` claim does nothing if a library is called in a mode that parses claims without validating them.

Brightspace illustrates the operational trade-off. D2L allows an administrator to set an access-token lifetime between **30 minutes and 20 hours**; after it expires, the token becomes invalid and the user is prompted to sign in again unless refresh-token behavior is enabled [7]. A 20-hour bearer token reduces reauthentication friction but gives a stolen token a much larger reuse window. A 30-minute token narrows that window but makes secure refresh behavior and session continuity more important.

Microsoft uses a different default: access-token lifetimes are variable and normally randomized from **60 to 90 minutes** [24]. Microsoft also warns clients to treat access tokens as opaque because the resource API owns the token format and validation rules [24]. **Inference:** A portal that decodes a Microsoft access token in browser code and builds authorization decisions from its visible claims would be violating that trust division, even if the token happens to look like a JWT.

Classic ASP.NET sessions have a different revocation model. The browser carries an opaque ID while the application retains session values in-process, in a state service, in SQL Server, or in another configured store [18]. Once the inactivity timeout is exceeded, the session is expired, and ASP.NET can abandon the session during logout [18]. This central state gives operators an immediate control point that a wholly self-contained JWT lacks.

OWASP's JWT guidance recommends placing a unique `jti` on a denylist after explicit session termination and keeping that denial until the token expires [16]. This is a deliberate return of server state to a nominally stateless design. Other revocation patterns include short access-token lifetimes, refresh-token rotation, per-user security-version checks, signing-key rotation for broad emergencies, and resource-server introspection when the protocol supports it.

Browser cookies introduce CSRF concerns because the browser automatically attaches them to matching requests. Microsoft's ASP.NET guidance describes a synchronizer-token design with one anti-forgery value in a cookie and another in a hidden form field; the server accepts the POST only when both validate [23]. Secure and HttpOnly attributes reduce transport and script-access risks, but do not by themselves prevent a browser from sending an unexpired cookie on a cross-site request [23].

| Lifetime choice | Benefit | Principal risk | Recommended control |
|---|---|---|---|
| Short access token | Narrows replay window | More refresh activity and failure modes | Rotate refresh tokens and detect reuse |
| Long access token | Fewer interruptions | Longer value after theft | Reserve for low-risk, constrained clients; prefer narrower scopes |
| Browser session cookie | Central invalidation and small client artifact | CSRF and session fixation if poorly handled | Rotate after login, use Secure/HttpOnly/SameSite, anti-CSRF tokens, server logout |
| Self-contained JWT | Scales verification across services | Difficult immediate revocation and claim-confusion risk | Short `exp`, strict audience/type rules, `jti` denial, separate keys and validators |
| Refresh token | Preserves user experience with short access tokens | High-value long-lived credential | Confidential storage, one-time rotation, family revocation, anomaly monitoring |

**Decision-ready insight:** Lifetime cannot compensate for broken verification, and perfect verification cannot compensate for a 20-hour stolen bearer token. Verification, storage, scope, rotation, and revocation must be designed together.

## Case Studies and Defensive Validation Blueprint

### Case study 1: SLCM's safest conclusion is "session unknown"

The SLCM public page supports a narrow finding: it offers student and parent authentication paths [2]. It does not support a claim that the application emits JWTs or that its cookies have any particular name or attributes. The supplied ASP.NET baseline makes an opaque cookie session plausible, and Microsoft's legacy documentation shows how such a session normally maps a browser `SessionID` to server-maintained state [18].

The important lesson is methodological. Technology fingerprinting can generate a test hypothesis, but it cannot establish a post-authentication control. For SLCM, an owner-authorized review should ask for configuration or controlled evidence covering cookie name, `Secure`, `HttpOnly`, `SameSite`, domain and path scope, idle and absolute timeout, identifier rotation after login, logout invalidation, concurrent sessions, and CSRF validation. Until then, each field stays **unknown**, not "secure" or "vulnerable."

### Case study 2: Brightspace separates API authorization from LTI launches

D2L's API flow uses an OAuth bearer token in the authorization header and lets deployments configure a 30-minute to 20-hour lifetime [7]. LTI 1.3 instead begins with OpenID Connect and sends a signed JWT whose receiver verifies a `kid`-selected public key [8]. Both involve tokens, but they differ in issuer, consumer, claims, transport, replay defenses, and lifecycle.

The failure mode is cross-protocol acceptance. If an API accepts an LTI ID token because both are signed by a familiar issuer, or an LTI tool accepts an API access token because it contains a student identity, signature validity would not repair the audience and token-type error. RFC 8725's explicit typing and mutually exclusive validation rules directly address that confusion [12]. The defensive design is one validator per protocol and issuer, with no shared "accept any university JWT" function.

### Case study 3: Historical libraries prove algorithm confusion is not theoretical

Auth0 documented two families of JWT library failure: some libraries accepted `alg=none` as verified, while others could confuse an expected RSA signature with HMAC verification and thereby misuse a public key as a symmetric secret [29]. NVD records that Node's `jsonwebtoken` before **4.2.2** allowed asymmetric-to-symmetric verification bypass [30]. A later NVD record states that `joaquimserafim/json-web-token` before **4.0.0** selected the verification algorithm from an unverified token and was vulnerable to RS256/HS256 confusion; version 4.0.0 fixed it [28].

These cases do not identify a MUJ dependency. They show the mechanism and explain why a current package version alone is not enough: application configuration must constrain algorithms and keys. A secure regression suite, operated only by the system owner or under written authorization, should verify in an isolated environment that unsigned tokens, wrong-family algorithms, wrong issuer, wrong audience, wrong type, expired or premature tokens, unknown `kid`, and replayed nonce values are all rejected without exposing sensitive error detail.

### Case study 4: MUJ Connect demonstrates the danger of filling OSINT gaps with assumptions

MUJ Connect's public pages establish a social application and a username/email login [5][4]. They do not establish JWT use or any named weakness [5][4]. Calling it "JWT vulnerable" would conflate a research focus with evidence and could cause reputational harm.

The correct owner-facing request is documentary: identify the authentication protocol, issuer, token format, verification library, allowed algorithms, key source, claims contract, browser storage method, access and refresh lifetimes, logout behavior, and incident revocation procedure. If MUJ Connect uses opaque sessions, much of the JWT checklist is inapplicable; if it uses JWTs, the checklist becomes testable in an authorized staging environment.

| Owner control | SLCM cookie session | Microsoft token consumer | Brightspace API | Brightspace LTI tool | MUJ Connect |
|---|---|---|---|---|---|
| Fixed issuer and audience | If federated | Required [24] | Required at resource server | Required [32] | Unknown |
| Algorithm allowlist | If JWT federation exists | Required for local JWT validation | Depends on token validation role | Required; no `none` [32] | Unknown |
| Key source and rotation | If signed external tokens exist | OpenID discovery/JWKS [24] | Vendor/resource configuration | Registered JWKS and `kid` [32] | Unknown |
| Idle and absolute timeout | Required | Token-policy dependent | Access-token lifetime **30 min-20 h** [7] | `exp`, `iat`, nonce window [32] | Unknown |
| Immediate termination | Server session abandonment | Account/token revocation controls | Refresh-family revocation and access expiry | Tool session plus replay cache | Unknown |
| CSRF or replay defense | Anti-forgery pair [23] | OIDC state/nonce as applicable | Bearer secrecy and TLS [7] | Nonce and one-time authorization code [32] | Unknown |

## Synthesis

The four systems differ along at least four dimensions: **state model, protocol role, time horizon, and revocation mechanism**. SLCM's likely cookie model keeps identity state near the application and lets the server end a session, but browser-automatic cookie attachment creates CSRF obligations. Microsoft identity issues tokens for specific applications and resources; an ID token proves authentication, while an access token belongs to the API and should appear opaque to the client [24][19]. Brightspace combines short- or long-lived OAuth bearer access with separately signed LTI launch JWTs [7][8]. MUJ Connect cannot yet be placed in any token category.

The non-obvious tension is that "stateless" does not mean "simpler security." A JWT can reduce shared session-store dependency, but it moves complexity into algorithm policy, key rotation, issuer and audience binding, explicit typing, expiration, replay control, and revocation. OWASP's recommendation to denylist `jti` values after termination demonstrates that strong logout often reintroduces state [16]. Conversely, a stateful cookie does not automatically provide safety: transport flags, rotation, timeout, logout, and CSRF controls remain necessary [23].

A second tension is institutional identity versus application authorization. MUJ's Microsoft 365 environment is verified [13], but that does not make every MUJ-branded token valid everywhere. The safest architecture is explicit trust minimization: SLCM accepts only its configured session or explicitly registered identity flow; Microsoft APIs accept only tokens whose audience names that API; a Brightspace API validates its OAuth access token; and each LTI tool validates only its registered platform, client ID, deployment, message type, nonce, and key [12][32].

A third tension concerns expiry. Brightspace's supported range from 30 minutes to 20 hours is operational flexibility, not a recommendation that every deployment choose 20 hours [7]. Short life reduces exposure after theft but increases dependence on secure refresh handling. Long life reduces interruption but increases incident-response pressure. The correct setting follows data sensitivity, client type, scope, device trust, revocation capability, and user experience rather than a universal number.

The practical program for MUJ should therefore be evidence-driven and boundary-specific. First, inventory every token and session artifact without assuming that all dotted strings are JWTs. Second, write a validation contract per issuer and use case. Third, test negative cases in owner-controlled staging. Fourth, log validation failures in a privacy-preserving manner and alert on replay, refresh reuse, unknown keys, and repeated cross-audience attempts. Finally, publish a coordinated disclosure channel so the security club can report observations safely without testing beyond authorization.

## VERDICT

| Question | Verdict | Confidence |
|---|---|---|
| Does public evidence prove that SLCM itself uses JWTs? | **No.** Public evidence shows login paths but no JWT format or token endpoint [2] | **High** for the public-evidence conclusion; **low** for hidden implementation details |
| Is a conventional SLCM cookie session plausible? | **Yes, as an inference** from the supplied ASP.NET baseline and the standard ASP.NET state model [18] | **Moderate**, not verified production behavior |
| Are JWTs present in the wider MUJ ecosystem? | **Yes.** Microsoft identity uses JWT ID tokens, and Brightspace LTI 1.3 uses signed JWT messages [8][19] | **High** |
| Are bearer tokens present? | **Yes in documented Brightspace OAuth and Microsoft API flows** [7][24] | **High** |
| Is MUJ Connect publicly proven to use JWTs? | **No. Its token design is unknown** [5][4] | **High** that public evidence is insufficient; **low** about internals |
| Is algorithm confusion a relevant design risk? | **Yes as a general JWT risk**, controlled by fixed algorithm and key policy [12] | **High** |
| Is algorithm confusion established in any MUJ application? | **No public evidence found** | **High** that this report establishes no such finding |
| Are exact SLCM MVC/.NET/IIS/Akamai versions independently verified here? | **No.** Passive public sources reviewed did not expose them [14] | **Moderate-high** |

**Overall verdict:** The MUJ ecosystem should not be described as one JWT-based authentication system. It is a set of distinct trust boundaries: a publicly undocumented SLCM web session, a verified Microsoft 365 identity environment, a MUJ Connect implementation whose token format is unknown, and a verified Brightspace deployment whose vendor protocols use OAuth bearer tokens and signed LTI JWTs. The strongest actionable risks are cross-token confusion, verifier-selected algorithms, incomplete claim validation, excessive bearer lifetimes, refresh-token compromise, and weak revocation design. None is established as an MUJ vulnerability by the public evidence in this report.

**Overall confidence: Moderate-high.** Confidence is high for standards, Brightspace protocol behavior, MUJ's use of Brightspace for online education, and the Microsoft 365 identity boundary. Confidence is moderate for the inferred SLCM session model. Confidence is intentionally low for undocumented SLCM cookie settings, MUJ Connect token internals, tenant-specific Brightspace configuration, and the exact server/CDN versions supplied in the research brief.

## References

1. *How to obtain an OAuth 2.0 Refresh Token - Brightspace*. https://community.d2l.com/brightspace/kb/articles/1196-how-to-obtain-an-oauth-2-0-refresh-token
2. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
3. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
4. *MUJ Connect*. https://mujconnect.in/login
5. *MUJ Connect*. https://mujconnect.in/
6. *Brightspace API Authentication Guide - OAuth 2.0 - Brightspace*. https://community.d2l.com/brightspace/kb/articles/1134-brightspace-api-authentication-guide-oauth-2-0
7. *OAuth 2.0 authentication — Developer Platform (January 2026)*. https://docs.valence.desire2learn.com/basic/oauth2.html
8. *About LTI 1.3 launch and authentication - Brightspace*. https://community.d2l.com/brightspace/kb/articles/23730-about-lti-1-3-launch-and-authentication
9. [
        MUJSLCM.JAIPUR.MANIPAL.EDU
    ](https://builtwith.com/mujslcm.jaipur.manipal.edu)
10. *Technologies used on mujslcm.jaipur.manipal.edu - Wappalyzer*. https://www.wappalyzer.com/lookup/mujslcm.jaipur.manipal.edu/
11. *Algorithm confusion attacks | Web Security Academy*. https://portswigger.net/web-security/jwt/algorithm-confusion
12. [
            
                RFC 8725 - JSON Web Token Best Current Practices
            
        ](https://datatracker.ietf.org/doc/html/rfc8725)
13. *Standard Operating Procedure*. http://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf
14. *mujslcm.jaipur.manipal.edu - urlscan.io*. https://urlscan.io/domain/mujslcm.jaipur.manipal.edu
15. [
            
                RFC 7519 - JSON Web Token (JWT)
            
        ](https://datatracker.ietf.org/doc/html/rfc7519)
16. *REST Security - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html
17. *404 - Content not found*. https://learn.microsoft.com/en-us/previous-versions/aspnet/ff647070%28v%3Dmsdn.10%29
18. *ASP.NET Session State Overview | Microsoft Learn*. https://learn.microsoft.com/en-us/previous-versions/aspnet/ms178581%28v%3Dvs.100%29
19. *ID token claims reference - Microsoft identity platform | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity-platform/id-token-claims-reference
20. *Access token claims reference - Microsoft identity platform | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity-platform/access-token-claims-reference
21. *Session Management - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
22. *ASP.NET Cookies Overview | Microsoft Learn*. https://learn.microsoft.com/en-us/previous-versions/aspnet/ms178194%28v%3Dvs.100%29
23. *XSRF/CSRF Prevention in ASP.NET MVC and Web Pages | Microsoft Learn*. https://learn.microsoft.com/en-us/aspnet/mvc/overview/security/xsrfcsrf-prevention-in-aspnet-mvc-and-web-pages
24. *Access tokens in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens
25. *Cross-Site Request Forgery Prevention - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
26. *Login - Manipal University Jaipur*. https://learning.onlinemanipal.com/d2l/home/14042
27. *D2L Brightspace in India: A Success Story | D2L*. http://d2l.com/why-d2l/customer-corner/d2l-brightspace-in-india-a-success-story
28. *NVD - CVE-2023-48238*. https://nvd.nist.gov/vuln/detail/CVE-2023-48238
29. *Critical vulnerabilities in JSON Web Token libraries*. https://auth0.com/blog/critical-vulnerabilities-in-json-web-token-libraries/
30. *NVD - CVE-2015-9235*. https://nvd.nist.gov/vuln/detail/CVE-2015-9235
31. *Learning Tools Interoperability Core Specification 1.3 | IMS Global Learning Consortium*. https://www.imsglobal.org/spec/lti/v1p3
32. *1EdTech Security Framework v1.1 | IMS Global Learning Consortium*. https://www.imsglobal.org/spec/security/v1p1
