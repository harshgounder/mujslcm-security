# Testing MUJ SLCM Login Controls Without Causing Harm

## Executive Summary

- **Runtime Policy Is Unknown**: The public MUJ page proves that the login is a self-posting username/password form with an anti-forgery token and a Microsoft password-reset link, but it does not disclose the deployed lockout threshold, counter key, rate limit, or adaptive challenge logic [19]. -> Treat MUJ's lockout status as **unverified**, not vulnerable or secure, until an authorized test and server-log review are completed.
- **Classic Identity Has No Safe Turnkey Threshold**: Classic ASP.NET Identity 2 source exposes configurable lockout properties, initializes the lockout duration to zero, and locks only when `AccessFailedAsync` reaches the configured maximum [2]. `PasswordSignInAsync` invokes that failure path only when the application passes `shouldLockout=true` [10]. -> Do not infer a five-attempt/five-minute policy from the claimed MVC stack; inspect MUJ configuration and controller code.
- **Stock Case Handling Usually Converges**: The classic Entity Framework `UserStore.FindByNameAsync` implementation uppercases both the stored and supplied username before lookup [17]. After lookup, failed-access state is updated using the resolved user's ID [21]. -> Under that exact stock path, ASCII case changes should normally reach one account counter; a bypass becomes plausible only if custom MUJ code keys throttling on the raw submitted string or resolves users differently.
- **Unicode Remains A Separate Risk**: Classic `UserStore` shows uppercase conversion but no Unicode normalization [17]. .NET normalization can produce forms C, D, KC, or KD, while Unicode UTS #39 separately addresses single-script, mixed-script, and whole-script confusables [7][4]. -> Test Unicode equivalence in staging with administrator-created accounts, never by submitting look-alike identifiers that might belong to real users.
- **IP Rotation Tests The Wrong Layer If Used Alone**: OWASP recommends associating failed-login counters with the account rather than the source IP specifically because an attacker can use many IP addresses [22]. Akamai can enforce IP-based rate controls and a ten-minute penalty box, while IIS can temporarily block clients by request rate or concurrency [14][6]. -> Retain IP and edge controls, but make the decisive password-failure counter account-based and persistent across network changes.
- **Microsoft 365 Does Not Prove Portal Lockout**: MUJ publishes Microsoft 365 sign-in and MFA instructions, and its realm metadata identifies the `muj.manipal.edu` namespace with the Manipal University Jaipur brand and Microsoft Online [18][20]. Entra Smart Lockout has its own defaults and heuristics [3]. -> Confirm whether the SLCM POST validates locally, delegates to Entra, or uses a hybrid flow before attributing any observed block.
- **No Visible CAPTCHA Is A Narrow Observation**: The captured form contains no visible CAPTCHA control, but that single state cannot exclude an adaptive or dynamically injected challenge [19]. OWASP treats CAPTCHA as defense in depth rather than a complete brute-force control [22]. -> Record challenge behavior after a few approved failures, but never attempt to bypass or automate a CAPTCHA.
- **ASVS Requires Documented And Implemented Controls**: ASVS 5.0 requires documentation describing rate limiting, anti-automation, adaptive response, and protection against malicious account lockout; it separately requires those controls to be implemented and failed responses not to reveal valid users [5]. -> MUJ should maintain a written authentication-control specification and test each layer against it.
- **Production Testing Must Be Small And Reversible**: OWASP's lockout test requires an account that the tester can afford to lock and recommends leaving the test until late if only one account exists [8]. -> Use an administrator-created throwaway account, a written rules-of-engagement document, a monitored maintenance window, strict request caps, and immediate stop conditions.

## Scope, Evidence Labels, And Safety Boundary

This report addresses only the public login surface at `https://mujslcm.jaipur.manipal.edu/`, public vendor documentation, published source code, and a proposed test plan. It does **not** perform login attempts, send crafted authentication traffic, enumerate users, rotate IP addresses, solve challenges, or access non-public data.

The prompt supplies the architecture labels "ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10 behind Akamai." Those labels are treated as **scope assumptions supplied by the requester**, not independently proven facts. The public form's `__RequestVerificationToken` is consistent with an ASP.NET anti-forgery mechanism, but a token name alone does not establish the precise MVC, .NET, or IIS version [19]. Likewise, Akamai product documentation shows what Akamai can do, not which policy MUJ has enabled [11].

The public page displays the `@muj.manipal.edu` suffix, Parent Login and Student Login choices, and a Forgot Password option [19]. Its HTML capture shows a POST form with username and password inputs, hidden `EmailFor` and `LoginFor` fields, an anti-forgery token, and a link to Microsoft's password-reset service [19]. Separately, MUJ's own Office 365 guide instructs students and employees to sign in through Microsoft Online and describes phone, email, and Microsoft Authenticator as MFA methods [18]. These observations establish an ecosystem relationship, but not the password-validation path used by the custom SLCM form.

I cannot provide private chain-of-thought. Instead, the report provides an audit-ready reasoning ledger: each conclusion is labeled as an observation, code fact, standard requirement, inference, unknown, or recommendation. That format exposes the evidence and decision rule without presenting hidden internal deliberation.

| Evidence label | Meaning in this report | Example |
|---|---|---|
| Observation | Directly present in public MUJ material | The form POSTs to the portal and includes username, password, and anti-forgery fields [19]. |
| Code fact | Direct behavior in published framework source | `PasswordSignInAsync` calls `AccessFailedAsync` only when `shouldLockout` is true [10]. |
| Standard requirement | A requirement or recommendation from OWASP or NIST | ASVS 5.0 requires implemented credential-stuffing and brute-force controls [5]. |
| Inference | A bounded conclusion derived from facts, explicitly identified | **Inference:** If MUJ keys a custom counter on the raw username, spelling variants may fragment it. |
| Unknown | Not disclosed by public evidence | MUJ's threshold, observation window, duration, CAPTCHA trigger, and counter key. |
| Recommendation | A proposed defensive action, not a claim about current MUJ behavior | Resolve an account once, then key failure state on its immutable internal ID. |

**Decision-ready insight:** Public OSINT is sufficient to identify what must be tested, but not sufficient to assign MUJ a pass or fail on lockout or rate limiting.

## Five Enforcement Layers Create Attribution Risk

Authentication protection can occur at several layers. A failure at one layer can be hidden by another, and the response alone may not identify which component acted.

| Layer | Publicly supported capability or observation | What remains unknown for MUJ | Diagnostic implication |
|---|---|---|---|
| Browser and form | MUJ exposes a self-posting credential form with an anti-forgery token and Microsoft reset link [19]. | Client-side validation, adaptive JavaScript, and post-failure challenge state. | A static page capture cannot prove the absence of CAPTCHA or throttling. |
| Custom MVC application | Classic Identity offers account failure counts and lockout dates, but applications configure and invoke them [2][10]. | Whether MUJ uses Identity 2, a custom membership store, LDAP, Entra, or a hybrid adapter. | A normal-looking MVC form does not prove that Identity lockout is active. |
| IIS | Dynamic IP Restrictions can block excessive concurrent requests or requests over a time interval [6]. It can use `X-Forwarded-For` in proxy mode [6]. | Whether the module is installed, enabled, logging-only, or correctly configured behind Akamai. | A 403, 401, 404, or connection reset may be IIS enforcement rather than application lockout [6]. |
| Akamai edge | Rate policies support burst and two-minute average thresholds and can scope criteria to login submissions [14]. | Match criteria, client identifier, thresholds, action, bot controls, and exceptions used by MUJ. | An edge deny does not establish an account lockout, and an origin response does not establish that edge controls are absent. |
| Microsoft Entra | Smart Lockout is always on for Entra customers and has separate familiar and unfamiliar location counters [3]. | Whether the SLCM password is submitted to Entra and which tenant-specific settings apply. | Entra behavior should be claimed only when Entra sign-in logs correlate with the test. |

### Case study: the same "blocked" result can have five causes

Suppose the throwaway account receives a denial after several bad passwords. The application may have set a lockout end date, Akamai may have put the source IP into a penalty box, IIS may have temporarily blocked the client, Entra may have applied Smart Lockout, or a custom controller may simply have introduced a delay. Akamai documents a ten-minute deny period for a rate-violating client [14], while Entra's public-cloud default begins with a one-minute lockout after ten failed attempts [3]. Similar elapsed-time behavior therefore does not identify the layer.

The mechanism matters because remediation differs. An Akamai block protects request capacity but may disappear when traffic comes from another client identifier. An account lockout follows the account but creates denial-of-service risk if an outsider can trigger it. A useful test must correlate WAF, IIS, application, and Entra timestamps. **Inference:** response-only black-box testing can establish that some control acted, but generally cannot prove which control owned the state.

**Decision-ready insight:** Define a shared correlation ID and log review plan before testing; otherwise the club may mislabel an edge rate limit as an account lockout or vice versa.

## ASP.NET Identity Defaults Do Not Prove Effective Lockout

The most important framework finding is that classic ASP.NET Identity 2 does not, by source code alone, give MUJ a known, effective threshold. `UserManager` declares `UserLockoutEnabledByDefault`, `MaxFailedAccessAttemptsBeforeLockout`, and `DefaultAccountLockoutTimeSpan`; the backing lockout duration starts at `TimeSpan.Zero`, and the constructor shown in source does not initialize a usable policy [2]. When called, `AccessFailedAsync` increments the user's count, compares it with `MaxFailedAccessAttemptsBeforeLockout`, sets the lockout end date, and resets the failure count [2].

A second switch exists at sign-in time. `PasswordSignInAsync` finds the user, checks existing lockout state, and checks the password. On an incorrect password, it calls `AccessFailedAsync` only if `shouldLockout` is true [10]. A controller can therefore have configured lockout properties but still fail to count password failures because it passes false.

| Candidate "default" | What the source actually establishes | Applicability to MUJ |
|---|---|---|
| Classic Identity 2 library | Lockout properties are configurable; the duration field begins at zero; `AccessFailedAsync` enforces the configured maximum [2]. | Relevant if MUJ really uses classic Identity 2, but it does not reveal MUJ's values. |
| MVC login invocation | Failed passwords affect lockout only when `shouldLockout=true` [10]. | Requires controller or runtime verification. |
| OWASP WSTG typical practice | Accounts are often locked after three to five failures; another WSTG passage describes five to ten as a typical threshold and five to thirty minutes as a possible compromise [8]. | Benchmark, not a framework default or mandatory MUJ value. |
| Entra Smart Lockout | Azure Public and 21Vianet tenants default to ten attempts and an initial sixty-second duration; Azure US Government defaults to three attempts [3]. | Relevant only if the tested authentication reaches Entra. |
| NIST SP 800-63B-4 | Unless otherwise specified, a verifier shall cap consecutive failures for one authenticator on one subscriber account at no more than 100 [1]. | A maximum safety bound, not a recommended everyday portal threshold. |

### Case study: configured properties with an inactive failure path

Consider an MVC application whose startup code sets a threshold and duration, but whose login controller passes `shouldLockout=false`. The policy appears correct during a configuration review, yet failed passwords never invoke `AccessFailedAsync`. The published `SignInManager` control flow demonstrates exactly why such a split review can miss the defect [10].

The reverse problem is also possible. If `shouldLockout=true` but `MaxFailedAccessAttemptsBeforeLockout` and duration are not intentionally configured, relying on the library's property declarations does not produce a defensible policy [2]. **Inference:** the club must test the complete route from controller call, through user resolution, to atomic failure-count update and unlock, rather than checking one settings file.

**Decision-ready insight:** Ask MUJ's application owner for four artifacts before black-box work: the login controller call, lockout configuration, user-store implementation, and a sanitized failure-event log. That white-box evidence can reduce production attempts substantially.

## Case And Unicode Variants Can Fragment Counters

Classic Entity Framework `UserStore.FindByNameAsync` uses `u.UserName.ToUpper() == userName.ToUpper()` [17]. `SignInManager` resolves that user before invoking `AccessFailedAsync`, and `AccessFailedAsync` updates the resolved user by ID [10][21]. Under this exact stock path, ordinary ASCII case changes such as `student1`, `STUDENT1`, and `Student1` should normally resolve to the same user and therefore the same failure state.

That conclusion is intentionally narrow. Microsoft recommends `StringComparison.Ordinal` or `OrdinalIgnoreCase` for culture-agnostic, security-relevant identifiers because culture-sensitive behavior varies by locale [9]. The Turkish `i`, `I`, `İ`, and `ı` illustrate why generic uppercase/lowercase assumptions are unsafe; Microsoft documents a security example where a culture-sensitive `FILE:` check differs under Turkish culture [9]. The classic store's `ToUpper()` expression also delegates comparison to the database provider, so the exact collation and translation remain implementation-dependent [16].

Unicode normalization addresses a different issue. `.Normalize()` can place equivalent text into forms C, D, KC, or KD [7]. UTS #39's confusable data addresses visual similarity and distinguishes single-script, mixed-script, and whole-script confusables [4]. Normalization does not automatically decide that a Latin `a` and a visually similar Cyrillic character represent the same account.

| Variant class | Example concept | Expected stock-Identity result | Bypass risk in custom auth | Production test rule |
|---|---|---|---|---|
| Exact spelling | The issued username exactly as displayed | Resolves normally. | Low unless counters are otherwise broken. | Allowed only for the throwaway account. |
| ASCII case | Lower, upper, and mixed case of the same ASCII identifier | Uppercase lookup is intended to converge [17]. | **Inference:** high if the counter is keyed on raw input before resolution. | First prove each spelling authenticates to the same owned account. |
| Canonically equivalent Unicode | Precomposed character versus base character plus combining mark | No normalization appears in classic `UserStore` [17]. | **Inference:** depends on application normalization and database collation. | Staging only, using an administrator-created Unicode test account. |
| Compatibility variant | Full-width or compatibility character | KC/KD may transform compatibility forms, but the app must choose that policy [7]. | **Inference:** inconsistent normalization can split lookup and throttling. | Staging or unit test only. |
| Cross-script confusable | Visually similar characters from different scripts | UTS #39 treats these as confusable-detection concerns, not automatic equality [4]. | May become a different account rather than a bypass of the same account. | Never submit against production unless administrators created and own both identifiers. |

### Case study: the counter-before-lookup anti-pattern

Imagine custom code that increments `failures[submittedUsername]` and only later calls a case-insensitive directory lookup. `Student1` and `STUDENT1` authenticate to one account but accumulate separate counters. **Inference:** alternating spellings would remain below each raw-string threshold even though one account receives all attempts.

The stock flow avoids that particular split by resolving the user first and updating by ID [21][17]. The defensive pattern is therefore: validate input syntax, apply a documented canonicalization policy, resolve exactly one account, and update an atomic counter keyed by immutable account ID. Preserve the raw spelling only as telemetry.

**Decision-ready insight:** An ASCII case test is appropriate on an owned production account after mapping is verified; a Unicode confusable test is not. Unicode should be covered by unit, integration, and staging tests where ownership and account mapping are controlled.

## IP Rotation Limits: Edge Friction Is Not Account Protection

OWASP explicitly says the failed-login counter should be associated with the account rather than the source IP because an attacker can use multiple IP addresses [22]. That does not make IP controls useless. IP, prefix, network reputation, device, global endpoint, and account signals solve different problems.

Akamai rate policies can use burst thresholds measured over one to five seconds and average thresholds measured over a two-minute window [14]. They can scope matching to login submissions and other request attributes [14]. Akamai's documentation identifies IPv4 clients with `/32` and IPv6 clients with `/64`, and describes a ten-minute penalty-box deny [14]. Its broader product also analyzes dimensions such as country, network fingerprint, and HTTPS request attributes [11]. None of that proves MUJ enabled those features.

IIS Dynamic IP Restrictions can temporarily block a client after excessive concurrency or request rate [6]. Behind a proxy it can use `X-Forwarded-For` [6]. A configuration error here creates two opposite risks: all users can appear to come from an Akamai edge address, or an origin can trust an attacker-controlled forwarding header. This sentence is a **configuration-risk inference**, not a finding about MUJ.

| Control key | Survives source-IP change? | Main benefit | Main weakness | Recommended role |
|---|---:|---|---|---|
| Raw source IP or prefix | No | Stops bursts from one network and protects capacity. | Distributed traffic can move to another bucket; shared NAT can create false positives. | Edge friction and anomaly signal. |
| Account ID | Yes | Directly limits guesses against one account. | A hard threshold can be abused to lock out a victim [22]. | Primary password-failure control with progressive response. |
| Account plus IP | Partly | Distinguishes concentrated from distributed activity. | Must not replace a global per-account ceiling. | Secondary risk feature. |
| Device or behavioral signal | Often | Adds context beyond address. | Privacy, spoofing, and model-quality trade-offs. | Adaptive response, not sole enforcement. |
| Global login-endpoint rate | Yes | Protects service capacity. | Cannot protect a targeted account by itself. | Availability backstop. |
| Entra familiar/unfamiliar counters | Partly | Separates location contexts; Entra tracks separate counters [3]. | Applies only to authentication that reaches Entra. | Identity-provider layer where applicable. |

Entra also tracks the last three bad password hashes and does not increment its lockout counter when the same bad password is submitted repeatedly [3]. That means a repeated-identical-password test may undercount Entra behavior. It does not imply an MUJ bypass because the portal may not delegate that request to Entra and other controls may still act.

**Decision-ready insight:** Do not conduct real "IP rotation" against production. If authorized, use no more than two pre-registered institutional egress addresses in staging and verify from logs that account state persists. Never switch addresses to evade an active deny.

## CAPTCHA And OWASP ASVS Requirements

The MUJ capture has no visible CAPTCHA field or widget in the observed form state [19]. That supports only the statement "no CAPTCHA was visible in this capture." It does not support "MUJ has no CAPTCHA," because a challenge may appear after failures, be injected dynamically, or be replaced by an invisible bot signal.

OWASP says CAPTCHA can impede automated login attempts but should be defense in depth, not a complete preventative control; it may be more usable to require it after a small number of failures [22]. OWASP also recommends a generic response whether the account is missing, the password is wrong, or the account is locked, and warns that response time and HTTP status can leak account validity [22].

| Standard item | Requirement or guidance | MUJ verification question |
|---|---|---|
| ASVS 5.0 6.1.1 | Documentation must define rate limiting, anti-automation, adaptive response, protection from credential stuffing and brute force, and prevention of malicious lockout [5]. | Is there an approved authentication-control specification with thresholds, windows, and ownership? |
| ASVS 5.0 6.3.1 | Credential-stuffing and brute-force controls must be implemented according to that documentation [5]. | Do test results and logs match the specification at every layer? |
| ASVS 5.0 6.3.8 | Failed authentication, registration, and forgot-password behavior must not reveal valid users through message, status, or timing [5]. | Are responses materially equivalent for the owned account and an administrator-reserved nonexistent ID? |
| ASVS 4.0.3 2.2.1 | Effective controls can include soft lockout, rate limiting, CAPTCHA, increasing delays, IP restrictions, and risk-based controls; the requirement also states no more than 100 failed attempts per hour on one account [15]. | Does MUJ use a layered control rather than one brittle hard lock? |
| NIST SP 800-63B-4 3.2.10 | The verifier shall generally allow no more than 100 consecutive failures for one authenticator on one subscriber account [1]. | Is there a firm account-level ceiling even if edge addresses vary? |

**Decision-ready insight:** CAPTCHA is optional within a layered design; effective account-centered throttling, generic responses, logging, and denial-of-service resistance are not optional outcomes.

## Non-Destructive MUJ SLCM Test Plan

### Authorization gates and test assets

No active step below is permitted merely because the tester owns a normal student account. Written approval must identify the hostname, account, date, source addresses, request cap, support contact, and allowed observations. The throwaway account should be created or explicitly designated by MUJ's administrator and contain no academic, financial, attendance, or personal records.

OWASP states that lockout testing requires an account the tester can afford to lock [8]. If only one account is available, OWASP recommends conducting this test at the end of the plan to avoid losing access [8].

| Gate | Exact requirement before testing | Stop if absent |
|---|---|---|
| Written authorization | Named approver, exact hostname, test dates, techniques, and data-handling terms. | Yes. |
| Owned account | Administrator-created throwaway account with confirmed recovery path and no production records. | Yes. |
| Monitoring | Application owner watching Akamai, IIS, application, database, and Entra logs where applicable. | Yes. |
| Recovery | Named operator able to unlock or reset only the throwaway account. | Yes. |
| Source control | One approved egress address for production; a second address only for a separately approved staging test. | Yes. |
| Request budget | Maximum submissions and minimum spacing recorded in the rules of engagement. | Yes. |
| Data minimization | No real usernames, leaked passwords, credential lists, or unrelated account identifiers. | Yes. |
| Emergency contact | Real-time channel for unexpected errors, alerts, or user impact. | Yes. |

### Phase A: passive baseline and one known-good control

1. Save the public login page once and record the UTC time, final URL, visible fields, cookies, security headers, and any challenge. Do not infer a missing control from a single state.
2. Perform one normal login and logout with the throwaway account. Record only status class, response category, redirects, response size, elapsed time, and correlation identifiers. Never place the real password in notes or packet exports.
3. Ask the owner to confirm which log layers received the event. If no application or identity event can be correlated, stop. Attribution is not reliable.
4. Confirm that the account can be reset by the designated operator. Do not trigger the public reset process unless that action is separately approved.

### Phase B: discover or verify the threshold with the fewest failures

White-box confirmation is preferred. If the owner supplies a documented threshold `T`, observation window `W`, and duration `D`, run one below-threshold sequence of `T-1` invalid passwords followed by one valid login. After the approved cooldown, run exactly `T` invalid passwords followed by one valid attempt. Stop immediately if lockout appears earlier than expected.

Use distinct, offline-generated invalid strings that cannot equal the actual password. This is not password guessing; the purpose is to exercise failure accounting. Submit manually or through an owner-approved harness at no faster than one authentication request every 30 seconds. The 30-second spacing is a conservative test control chosen for this plan, not a claimed MUJ threshold.

If the owner refuses configuration access but authorizes black-box discovery, use the WSTG progression only in staging: three invalid attempts then a valid attempt; after recovery, four invalid attempts then a valid attempt; after recovery, five invalid attempts then a valid attempt [8]. Production discovery should stop at five failures. If no control acts, record "threshold not established within approved cap" rather than continuing toward ten, one hundred, or an unlimited sequence.

| Phase B sequence | Maximum authentication submissions | Expected interpretation | Mandatory stop |
|---|---:|---|---|
| Known `T`, below threshold | `T-1` invalid plus 1 valid | Valid succeeds; prior failures may reset after success in the classic flow [13]. | Any lockout, 5xx response, support alert, or unexplained account change. |
| Known `T`, at threshold | `T` invalid plus 1 valid | Valid attempt should be denied or delayed according to documented policy. | First lockout or edge deny. |
| Unknown threshold, staging | WSTG 3/4/5 progression | Finds a common low threshold without open-ended traffic [8]. | First lockout or completion of five-failure stage. |
| Unknown threshold, production | No more than 5 consecutive invalid submissions | A bounded observation only. | Five failures even if no lockout occurs. |

### Phase C: measure unlock without hammering

After the first confirmed lockout, send no more invalid passwords. If `D` is documented, make one valid attempt just before expiry only when approved and one just after expiry. If duration is unknown, WSTG illustrates checks at five, ten, and fifteen minutes [8]. Use at most those three valid attempts and stop after the first success.

Record whether the state is a hard lock, soft delay, CAPTCHA, generic failure, edge deny, or administrative lock. A generic user-facing message is desirable for anti-enumeration, so operators must use logs rather than demand an explicit "locked" message [22].

### Phase D: ASCII case aggregation

First, use the correct password once with the exact username and once with an ASCII case variant. Continue only if both events resolve in logs to the same throwaway account ID. Then, in a fresh approved window, distribute no more than the known threshold across exact, uppercase, and mixed-case spellings. For a threshold of five, a safe allocation is two exact, two uppercase, and one mixed-case invalid submission, followed by one valid exact-case attempt.

Pass means every failure increments one account-level state and the threshold acts at the same cumulative total. Fail means logs show separate counters or the cumulative policy can be avoided by spelling changes. Do not include culture-sensitive or Unicode characters in this production phase.

### Phase E: Unicode in staging only

Create controlled staging accounts whose intended equivalence classes are documented. Test NFC versus NFD only if administrators intentionally expect them to represent one account. Test compatibility and cross-script characters as rejection or collision cases, not as production login attempts. The expected result must be defined in advance: either both forms map to one immutable account and counter, or one form is consistently rejected before authentication.

Do not submit visual confusables against production. A look-alike identifier may be a different valid person's account, and testing it would violate the owned-account boundary.

### Phase F: network-key behavior without evasion

Do not rotate through VPNs, proxies, Tor, cloud hosts, mobile networks, or third-party infrastructure. In production, inspect logs to verify that the account counter is independent of address. If an active edge or IIS deny occurs, do not switch addresses to continue.

In staging only, and with two pre-registered institutional egress addresses, split a below-threshold sequence between address A and address B. The cumulative account count should persist even though IP-specific telemetry has two buckets. A second staging check can confirm that an IP-specific burst control does not erase or replace the account counter. Never spoof `X-Forwarded-For`; test forwarding-header trust through configuration review or an isolated origin test.

### Phase G: CAPTCHA and response equivalence

Observe whether a challenge appears initially or after the approved failures. If it appears, record its trigger stage and stop automated activity. Do not solve it through a service, replay tokens, suppress scripts, or attempt accessibility-path bypasses.

For response equivalence, compare only the throwaway account with an administrator-reserved identifier guaranteed not to be assigned. Compare HTTP status, redirect chain, response category, length range, and broad timing distribution. Do not optimize for microsecond timing or run large samples. ASVS requires that valid users not be deducible from messages, status codes, or response time [5].

### Evidence record and stop rules

| Evidence field | Why it is needed |
|---|---|
| UTC timestamp and test-case ID | Correlates all layers without storing secrets. |
| Submitted username class | Exact, ASCII case variant, or controlled staging Unicode class. Do not store unrelated usernames. |
| Source label | Approved address A or staging address B, not a rotating address list. |
| Attempt ordinal | Establishes cumulative threshold and observation window. |
| HTTP outcome | Status, redirect category, response-size band, and generic message class. |
| Challenge state | None visible, CAPTCHA shown, progressive delay, or other adaptive response. |
| Edge/IIS/application/Entra event IDs | Attributes enforcement to the correct layer. |
| Resolved internal account ID | Proves variants reached one throwaway account; redact after analysis. |
| Failure count and lockout end | Confirms account-key behavior and duration. |
| Recovery event | Confirms safe closure and restored account access. |

Stop immediately on any 5xx response, unexpected latency or resource degradation, effect on a non-test account, security-operations escalation, inability to correlate logs, unplanned password reset, account data change, CAPTCHA appearance during automated work, edge denial, or instruction from the owner. Restore the throwaway account, revoke its credentials, and archive only sanitized findings.

**Decision-ready insight:** The plan tests one hypothesis at a time, never uses real accounts, and treats an inconclusive result as inconclusive rather than raising traffic until something breaks.

## Findings Matrix And Remediation Priorities

| Test area | Pass condition | Failure indicator | Priority remediation |
|---|---|---|---|
| Failure invocation | Every invalid password reaches an audited failure-count path. | Wrong passwords never increment state because lockout is disabled or `shouldLockout=false`. | P0: enable and unit-test failure accounting [10]. |
| Counter key | State is keyed to immutable account ID after canonical lookup. | Raw spelling, email alias, or login mode creates separate buckets. | P0: canonicalize once, resolve once, increment atomically by account ID. |
| ASCII case | Exact, upper, and mixed case aggregate to one counter when they map to one account. | Variant switching keeps each counter below threshold. | P0: align lookup and throttling identity semantics. |
| Unicode | Staging behavior matches a documented normalization and confusable policy. | Equivalent forms resolve inconsistently or collide silently. | P1: normalize with an explicit form, restrict identifier scripts, and add UTS #39 checks where appropriate [7][4]. |
| Source-IP change | Account state persists across approved staging addresses. | Moving address resets the only effective control. | P0: add account-level throttling; retain IP controls as secondary signals [22]. |
| Lockout denial of service | Progressive delay, soft lock, or safe recovery prevents malicious permanent lockout. | Anyone can indefinitely lock a victim with a few requests. | P0: use graduated response, secure recovery, and monitoring [22]. |
| CAPTCHA | Challenge is adaptive and supplemental. | CAPTCHA is the only brute-force control, or testers can continue automatically after it appears. | P1: combine with account and endpoint limits [22]. |
| Response equivalence | Missing, wrong-password, and locked states are materially generic. | Message, status, redirect, or timing reveals validity. | P1: unify external responses and preserve detail only in logs [22]. |
| Proxy attribution | Only trusted Akamai/IIS paths determine client address. | Arbitrary forwarding headers alter enforcement identity. | P0: restrict origin access and trust forwarding metadata only from controlled proxies. |
| Documentation | ASVS 5.0 control design and implementation match. | No owner can state threshold, window, duration, key, reset, or monitoring rule. | P1: create the ASVS 6.1.1 specification and verify under 6.3.1 [5]. |

The application should not select a threshold by copying a framework sample. It should document the threat model, user population, MFA coverage, help-desk capacity, and denial-of-service tolerance. OWASP recommends considering the threshold, observation window, and duration together, and describes exponential delay as an alternative to a fixed duration [22].

A strong implementation updates counters atomically so parallel failures cannot race. It keeps account, IP-prefix, device, and global endpoint signals as separate dimensions. The response to a user remains generic, while internal logs retain the exact reason and enforcing layer. Successful authentication should reset the relevant retry count; NIST says the verifier should disregard previous failures and reset the authenticator retry count after successful authentication [1].

**Decision-ready insight:** The highest-value fix is not "add CAPTCHA." It is to ensure that all aliases and accepted spellings resolve to one account before atomic failure accounting, then combine progressive account response with edge protection and safe recovery.

## Synthesis

| Mechanism | Scope | Variant behavior | IP-change behavior | Denial-of-service trade-off | Evidence base | Best use |
|---|---|---|---|---|---|---|
| Classic Identity account lockout | One resolved application account | Stock store uppercases names; custom behavior may differ [17]. | Should persist because failure state is updated by user ID [21]. | Hard thresholds can be weaponized. | Published source, not MUJ configuration. | Primary account-centered control if correctly invoked. |
| Raw-string custom counter | One submitted spelling | **Inference:** fragments across case, normalization, or aliases. | May persist by spelling but still be bypassable by variants. | Can lock one spelling while another remains usable. | Hypothetical anti-pattern to test. | Avoid. |
| IIS Dynamic IP Restrictions | Client IP or forwarded client address | Does not understand account identity. | A new client bucket may avoid the old temporary block. | Shared networks can be overblocked. | Microsoft IIS documentation [6]. | Origin availability and burst protection. |
| Akamai rate policy | Matching requests and configured client identifier | Does not inherently establish application account equivalence. | IP-based examples use `/32` and `/64`; other product signals may add context [14][11]. | Edge false positives can affect a network, but protect origin capacity. | Akamai product documentation, not site configuration. | Edge burst, bot, and DDoS friction. |
| Entra Smart Lockout | Entra tenant identity | Uses Entra's own identity resolution and bad-password-hash logic. | Familiar and unfamiliar locations have separate counters [3]. | Designed to distinguish attacker and genuine user, but still needs tenant policy review. | Microsoft Entra documentation. | Identity-provider protection when SLCM delegates to Entra. |
| CAPTCHA | Human-interaction challenge | Independent of account canonicalization. | Can follow the session or challenge implementation rather than the account. | Accessibility and usability costs; not complete prevention. | OWASP guidance [22]. | Adaptive defense in depth after risk rises. |

Three non-obvious tensions emerge.

First, case-insensitive lookup can coexist with case-sensitive throttling. The stock Entity Framework store tries to converge case variants [17], but custom code can still count before lookup. The security property depends on ordering, not merely on whether login "accepts uppercase."

Second, stronger hard lockout can reduce password guessing while increasing malicious lockout. OWASP expressly warns about attackers locking other users and recommends considering alternatives such as exponential delay and recovery access [22]. The right design therefore combines an account ceiling with progressive friction, notification, MFA, and safe recovery rather than treating permanent lock as the only success state.

Third, edge controls and account controls optimize different outcomes. Akamai and IIS protect availability and suppress bursts. Account-centered counters protect a target even when traffic is distributed. Entra may add identity intelligence, but only if the SLCM flow reaches it. No one layer substitutes for the others.

The integrated strategy is: normalize and validate identifiers under one documented policy; resolve to an immutable ID; record failures atomically; apply progressive account response; add IP, prefix, device, endpoint, and behavioral controls; keep external errors generic; correlate logs across Akamai, IIS, application, and Entra; and maintain a safe recovery route. That strategy implements ASVS's documentation-plus-verification model [5] while respecting OWASP's warning that anti-automation must not become an easy account-lockout attack [15].

## VERDICT

**Verdict: MUJ SLCM's deployed lockout and rate-limiting effectiveness is INDETERMINATE from public information. Do not report a vulnerability based on framework fingerprints or the absence of a visible initial CAPTCHA.**

| Conclusion | Confidence | Basis |
|---|---|---|
| The public portal exposes a custom username/password POST form, anti-forgery token, Microsoft reset link, and `@muj.manipal.edu` login suffix. | High | Direct public capture [19]. |
| MUJ uses Microsoft 365 identity services somewhere in its ecosystem. | High | MUJ's own sign-in/MFA guide and Microsoft realm metadata [18][20]. |
| The SLCM form delegates each password check to Entra. | Low | No public evidence establishes the credential-validation route. |
| Classic ASP.NET Identity 2 requires explicit policy configuration and `shouldLockout=true` for the shown sign-in failure path. | High | Published framework source [2][10]. |
| Stock classic Entity Framework lookup intends case-insensitive username resolution. | High | Published `ToUpper()` lookup source [17]. |
| MUJ's custom implementation preserves one counter across case and Unicode variants. | Low | Requires authorized runtime and code verification. |
| MUJ has no CAPTCHA or bot defense. | Low | Only one state with no visible CAPTCHA was observed [19]. |
| The proposed plan can verify the major unknowns without brute force or unauthorized access if MUJ approves and monitors it. | High | It uses an owned lockable account, bounded WSTG sequences, strict caps, and immediate stop conditions [8]. |

**Overall confidence: High in the framework analysis, standards mapping, public-surface observations, and safety plan; low in any site-specific conclusion about MUJ's active threshold, counter key, duration, Akamai/IIS policy, or CAPTCHA trigger.**

The club should present the current result as a set of testable hypotheses, not as an exploit claim. Proceed only with written authorization from MUJ, an administrator-created throwaway account, real-time owner monitoring, and the bounded plan above. If authorization is not granted, stop at this OSINT report.

## References

1. *NIST Special Publication 800-63B*. https://pages.nist.gov/800-63-4/sp800-63b.html
2. *AspNetIdentity/src/Microsoft.AspNet.Identity.Core ... - GitHub*. https://github.com/aspnet/AspNetIdentity/blob/main/src/Microsoft.AspNet.Identity.Core/UserManager.cs
3. *Prevent Attacks Using Smart Lockout - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/authentication/howto-password-smart-lockout
4. *UTS #39: Unicode Security Mechanisms*. http://unicode.org/reports/tr39
5. *ASVS/5.0/en/0x15-V6-Authentication.md at master · OWASP/ASVS · GitHub*. https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md
6. *Using Dynamic IP Restrictions | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/manage/configuring-security/using-dynamic-ip-restrictions
7. *String.Normalize Method (System) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.string.normalize?view=netframework-4.8.1
8. *WSTG - Latest | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/03-Testing_for_Weak_Lock_Out_Mechanism
9. *Best Practices for Comparing Strings in .NET - .NET | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/standard/base-types/best-practices-strings
10. *AspNetIdentity/src/Microsoft.AspNet.Identity.Owin/SignInManager.cs at main · aspnet/AspNetIdentity · GitHub*. https://github.com/aspnet/AspNetIdentity/blob/main/src/Microsoft.AspNet.Identity.Owin/SignInManager.cs
11. *App & API Protector*. http://akamai.com/site/en/documents/brief/akamai-app-and-api-protector-product-brief.pdf
12. *Rate policy*. https://techdocs.akamai.com/terraform/docs/as-rc-rate-policy
13. *raw.githubusercontent.com*. https://raw.githubusercontent.com/aspnet/AspNetIdentity/main/src/Microsoft.AspNet.Identity.Owin/SignInManager.cs
14. *Set protections*. https://techdocs.akamai.com/cloud-security/docs/set-protections
15. *ASVS/4.0/en/0x11-V2-Authentication.md at master · OWASP/ASVS · GitHub*. https://github.com/OWASP/ASVS/blob/master/4.0/en/0x11-V2-Authentication.md
16. *raw.githubusercontent.com*. https://raw.githubusercontent.com/aspnet/AspNetIdentity/main/src/Microsoft.AspNet.Identity.EntityFramework/UserStore.cs
17. *AspNetIdentity/src/Microsoft.AspNet.Identity.EntityFramework/UserStore.cs at main · aspnet/AspNetIdentity · GitHub*. https://github.com/aspnet/AspNetIdentity/blob/main/src/Microsoft.AspNet.Identity.EntityFramework/UserStore.cs
18. *http://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf*. http://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf
19. *http://mujslcm.jaipur.manipal.edu/*. http://mujslcm.jaipur.manipal.edu/
20. *http://login.microsoftonline.com/getuserrealm.srf?login=probe@muj.manipal.edu&xml=1*. http://login.microsoftonline.com/getuserrealm.srf?login=probe@muj.manipal.edu&xml=1
21. *raw.githubusercontent.com*. https://raw.githubusercontent.com/aspnet/AspNetIdentity/main/src/Microsoft.AspNet.Identity.Core/UserManager.cs
22. *Authentication - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
