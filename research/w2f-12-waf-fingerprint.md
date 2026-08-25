# Distinguishing Akamai WAF From MUJ Application Responses

## Executive Summary

- **403 Is Not Attribution**: Akamai can apply deny actions, create custom error or redirect pages, and modify response status and headers at the edge [3][23][7]. Therefore, a 403 status, an "Access Denied" title, or a particular HTML layout cannot by itself establish which layer made the decision -> classify a response only after combining client evidence with Akamai and origin logs.

- **MUJ Facts And Assumptions Must Stay Separate**: The publicly visible MUJ SLCM portal identifies itself as the MUJ portal and exposes student, parent, and forgotten-password paths while displaying the `@muj.manipal.edu` identity suffix [32]. Microsoft identifies `muj.manipal.edu` as a managed Manipal University Jaipur realm [33], and its MX record routes mail to Microsoft protection infrastructure [34]. By contrast, ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, and Akamai are club-supplied scope assumptions in this report, not independently established version findings -> do not publish those versions as fresh OSINT without an owner-approved configuration record.

- **Akamai References Are Stronger Than Generic Bodies**: Akamai's official Translate Error String tool accepts an error reference code and returns a summary and log preview that can include the failure reason, response code, WAF details, URL, client IP, edge IP, origin IP, method, and user agent [31] -> preserve the complete reference string, UTC time, URL, and client network context whenever a user reports a denial.

- **Headers Prove Transit, Not Necessarily Causation**: Administrator-oriented Akamai diagnostics can return `X-Cache`, `X-Cache-Remote`, `X-Check-Cacheable`, `X-Akamai-Request-ID`, and cache-key data [13]. A cache or request identifier supports the conclusion that Akamai handled the transaction, but it does not by itself prove that a WAF rule caused the response -> use the request identifier to correlate the client observation with security and origin events.

- **Bot Challenges Are Intentionally Variable**: Akamai says Bot Manager scores requests from 0 for human to 100 for bot, allows operators to tune cautious, strict, and aggressive responses, and uses defenses that go beyond simple block-or-allow actions [17]. Akamai also describes responses intended not to tip off malicious bots [17] -> do not treat one JavaScript page, one cookie name, or one status code as a permanent Bot Manager signature.

- **OWASP CRS Is Not Established On MUJ**: OWASP CRS uses cumulative anomaly scoring, with documented default inbound and outbound thresholds of 5 and 4 [19]. Akamai's own documentation instead names Kona Rule Set, or KRS, and Adaptive Security Engine, or ASE, modes [25]. No collected first-party source equates Akamai KRS or ASE with upstream OWASP CRS -> describe observed categories as "CRS-like" only when behavior resembles CRS, and reserve "OWASP CRS" for configuration, rule-ID, or vendor confirmation.

- **IP Allowlists Need Configuration Evidence**: Akamai's Client IP criterion can match an address, range, or CIDR and can source the client identity from either the connecting address or an `X-Forwarded-For` value [21] -> determine allowlist behavior from approved configuration and log comparisons, never by spoofing forwarding headers or attempting to evade an access rule.

- **Rate-Limit Safety Comes Before Fingerprinting**: Akamai rate policies monitor and moderate request volume and can include average, burst, and penalty-box parameters [28] -> use passive incident artifacts first, establish a tiny written request budget for any owner-approved check, and stop immediately on a challenge, 429 response, rising latency, or any operator request.

- **Logs Decide**: Akamai SIEM events can carry `configId`, `policyId`, client IP, rules, rule versions, messages, tags, data, selectors, actions, request ID, method, path, status, and response headers [30]. The SIEM API supports incremental collection and replay of missed events from the previous 12 hours [24] -> the most defensible finding is a three-way correlation among the saved client response, the Akamai event, and the IIS or application log.

**Decision-ready insight:** Based on public material alone, the club can establish an evidence-preserving attribution method, but it cannot responsibly identify MUJ's exact WAF policy, OWASP CRS deployment, IP allowlist, or present deny-page template. Those conclusions require owner-authorized telemetry or configuration access.

## Scope, Ethics, and MUJ Evidence Boundary

This report is defensive and public-information-only. It does not authorize testing, provide attack strings, recommend bypassing an allowlist, or instruct readers to discover a rate threshold. Any active validation must be approved in writing by MUJ's system owner, limited to named hosts and times, coordinated with operators, and stopped on unexpected behavior. Student-club membership is not itself authorization.

I cannot provide private chain-of-thought. In its place, the report supplies an auditable reasoning framework: each conclusion is tied to an observable artifact, each inference is labeled, contradictory explanations are retained until logs resolve them, and the decision matrices show exactly what evidence changes a classification.

### Exact evidence-status table

| Item | Publicly supported observation | Status in this report | Operational consequence |
|---|---|---|---|
| MUJ SLCM public surface | The portal displays "WELCOME TO MUJ PORTAL," uses the `@muj.manipal.edu` suffix, and presents parent, student, and forgotten-password routes [32]. | Verified public observation | Treat the login page as the stable baseline URL, but do not submit credentials merely to fingerprint infrastructure. |
| Microsoft 365 identity | Microsoft's realm endpoint labels `muj.manipal.edu` a managed Manipal University Jaipur realm [33]. MUJ's published Office 365 procedure directs users to `login.microsoftonline.com` with their university mail ID [35]. | Verified public observation | A Microsoft-branded redirect, MFA prompt, or Microsoft error can belong to the identity provider rather than the MUJ application or Akamai WAF. |
| MUJ mail routing | The `muj.manipal.edu` MX record points to `muj-manipal-edu.mail.protection.outlook.com` [34]. | Verified public observation | Supports the Microsoft 365 identity context, but says nothing about the SLCM WAF policy. |
| ASP.NET MVC 5.3 | Supplied by the club in the research brief. | Unverified scope assumption | Do not use the version in a public vulnerability claim until MUJ confirms it or an owner-approved artifact establishes it. |
| .NET Framework 4.x | Supplied by the club in the research brief. | Unverified scope assumption | Treat generic ASP.NET-looking HTML as suggestive, not conclusive. |
| IIS 10 | Supplied by the club in the research brief. | Unverified scope assumption | Do not attribute a response to IIS from `Server` text or page styling alone. |
| Akamai in front of SLCM | Supplied by the club in the research brief. Akamai's documented WAF behavior can block threatening HTTP and HTTPS requests [10]. | Working architecture premise, not independently re-fingerprinted here | Use Akamai-specific evidence conditionally: "if the supplied architecture is current." |
| Exact WAF rules, Bot Manager policy, rate policy, and allowlist | No MUJ configuration or security-event export was provided. | Unknown | Do not infer a ruleset or allowlist merely because two clients receive different outcomes. |

The distinction matters because the request path has at least three logically separate decision planes: Akamai edge controls, the MUJ application and IIS origin, and Microsoft 365 identity. **Inference:** a user-visible denial can be generated before the origin, at the origin, or after an identity handoff. A single screen capture therefore cannot identify the responsible plane.

MUJ's own Office 365 procedure says the user enters a university mail ID, enters a current or temporary password, and can be prompted to change that password [35]. A separate MUJ procedure describes Microsoft account security information and adding phone, email, or Microsoft Authenticator methods [35]. Those documents establish a Microsoft identity workflow, but they do not prove that every SLCM route uses the same authentication policy.

**Section insight:** The first analytical task is not "detect the WAF." It is to identify the transaction's current control plane. Confusing an Entra sign-in response with an SLCM or Akamai denial will corrupt every later fingerprint.

## Akamai Fingerprints: 403 Bodies, Headers, References, and Challenges

### No single 403 template is invariant

Akamai documents that an application-security policy can alert or deny based on configured actions [3]. Initial protections can also be placed in Alert mode so that requests appear in reports without being denied [3]. This means that even a true rule match does not guarantee that the client receives a block page.

Akamai further documents custom denies that let an operator create an error message or redirect page for denied requests [23]. EdgeWorkers can set a returned status to a 2xx, 3xx, 4xx, or 5xx code and can add, replace, or remove response headers [7]. **Inference:** an MUJ-branded 403 can still be edge-generated, and an Akamai-transited response can look origin-generated. Conversely, an unbranded 403 does not prove Akamai made the decision.

For this reason, classify the following as observations rather than conclusions: status code, reason phrase, page title, visible branding, HTML length, JavaScript presence, redirect target, cookies, and `Server` text. Store them because combinations can be useful, but do not promote any one to a vendor verdict.

### Exact Akamai client-artifact table

| Client-visible artifact | What the source supports | Attribution value | Safe handling on MUJ |
|---|---|---|---|
| HTTP 403 | Akamai policies can apply a deny action [3], while edge code can emit any 4xx status [7]. | Weak alone | Record it; do not trigger more denials to test consistency. |
| Custom "Access Denied" or branded body | Akamai custom denies can produce an operator-crafted error message or redirect page [23]. | Weak to medium | Hash and preserve the body from an actual incident. Body design is not an invariant fingerprint. |
| Akamai-style reference string | The official translator consumes an error reference code and can return failure, WAF, network, request, and origin details [31]. | Strong evidence of an Akamai-handled error when the reference is successfully translated | Save the complete string exactly, including case, punctuation, UTC time, URL, and client public IP. Ask an authorized Akamai administrator to translate it. |
| `X-Akamai-Request-ID` | Akamai's documented diagnostic mapping returns the request ID used to identify a request in logs [13]. | Strong edge-correlation key, but not proof of WAF causation | Obtain through owner-approved diagnostics or existing logs. Do not assume the header is exposed on normal public responses. |
| `X-Cache` | Akamai maps its diagnostic request to `X-Cache`, with values describing hits, misses, refreshes, negative caching, and failover use of stale content [13]. | Medium evidence of edge handling; low evidence of a WAF decision | Use only to distinguish cache/origin handling, not to label a rule match. |
| `X-Cache-Remote` | Describes how the parent response was served [13]. | Medium for delivery-path analysis | Treat it as delivery metadata, not a security verdict. |
| `X-Check-Cacheable` | Reports whether a response is cacheable [13]. | Low for WAF attribution | Useful when asking whether a repeated body came from cache; it does not identify the denying layer. |
| `X-True-Cache-Key` or `X-Cache-Key` | Akamai diagnostics can return the effective cache key and related delivery data [13]. | Medium for cache investigation; potentially sensitive | Restrict to authorized operators and redact internal identifiers from a club report. |
| JavaScript or interstitial challenge | Bot Manager can challenge suspected bots and tune responses by score [17]. | Medium only when correlated with Bot Manager telemetry | Do not automate or solve the challenge. Preserve a screenshot and stop. |
| Cookie change | The first-party material collected here does not establish a fixed Bot Manager cookie signature for MUJ. | Insufficient | Do not claim Bot Manager from a cookie name copied from a third-party fingerprint list. |
| Microsoft sign-in page or MFA screen | MUJ directs users to Microsoft's login portal for Office 365 [35] and documents account security methods [35]. | Strong evidence of identity-provider context, not WAF causation | Record the redirect chain without entering credentials unless the approved test requires an owned test account. |

### Why challenge fingerprints age badly

Akamai describes Bot Manager as observing traffic at the edge, using behavior analysis and browser fingerprinting, and assigning a Bot Score [17]. Its response segments can be watched, challenged, or mitigated, and the customer can adjust the action and score boundary [17]. Akamai also describes stealthy and nuanced defenses intended not to reveal decisions to malicious automation [17].

**Inference:** two requests that appear semantically identical to a human can receive different outcomes because their network reputation, browser state, request history, or policy context differs. That does not automatically demonstrate an IP allowlist or an application bug. It can also reflect bot scoring, a penalty mechanism, policy rollout, or different edge state.

The responsible club response to a challenge is observation, not adaptation. Do not rotate user agents, replay challenge tokens, clear and regenerate cookies repeatedly, switch through proxies, or attempt to mimic another client. Those actions stop being passive fingerprinting and can resemble evasion.

**Section insight:** The most valuable Akamai fingerprint is not a logo or header. It is a correlation handle that an authorized operator can resolve in Akamai telemetry.

## OWASP CRS Versus Akamai KRS and ASE

OWASP Core Rule Set and Akamai managed protections may cover similar attack categories, but similar coverage does not establish shared implementation. CRS applies numeric anomaly scores to transactions and uses a threshold to make blocking decisions [19]. The documented defaults are an inbound threshold of 5 and an outbound threshold of 4 [19]. CRS paranoia level controls aggressiveness, with PL1 intended to produce very few false alarms [15].

Akamai's first-party terminology is different. Its documentation names Kona Rule Set rules and ASE modes, and explains that KRS or manual ASE policies do not automatically receive rule upgrades, while automatic modes do [25]. It also documents an evaluation mode in which rules trigger as they would in production but only record how they would have responded [25]. ASE is described as combining threat scoring, behavior signals, anomaly detection, and automatic response adjustment [27].

### Exact ruleset-comparison table

| Dimension | OWASP CRS | Akamai KRS or ASE | What can be concluded for MUJ |
|---|---|---|---|
| Decision model | Cumulative anomaly score with blocking at a configured threshold [19]. | KRS rules and ASE modes are managed through Akamai security policies [25]. ASE uses contextual scoring and anomaly signals [27]. | Similar scoring behavior is not enough to identify CRS. |
| Default threshold | Inbound 5 and outbound 4 in the documented CRS defaults [19]. | No MUJ threshold is publicly established. | Do not infer a threshold by sending progressively suspicious requests. |
| Aggressiveness control | CRS paranoia level controls how aggressive the enabled rule set is; PL1 is intended to have few false alarms [15]. | ASE can operate in automatic or manual modes; KRS is separately named [25]. | A false positive does not reveal a CRS paranoia level. |
| Rule identity | A CRS deployment can expose rule metadata in authorized audit logs. | Akamai SIEM events can include rules, versions, messages, tags, selectors, data, and actions [30]. | Rule metadata is the correct evidence source. A client body is not. |
| Safe evaluation | CRS can be tuned using logs and exclusions; exact local settings are deployment-specific. | Akamai documents an evaluation mode that records what rules would have done without changing production behavior [25]. | If MUJ wants a positive-control test, use staging or evaluation mode under owner control. |
| Vendor conclusion | CRS is an open ruleset architecture with documented anomaly scoring. | The collected Akamai sources say KRS and ASE; they do not state that these are upstream CRS [27][25]. | Current verdict: OWASP CRS on MUJ is unproven. |

### What counts as a defensible "ruleset fingerprint"

A high-confidence ruleset finding needs one of three forms of evidence. First, a configuration export can explicitly name the policy mode and rule set. Second, an authorized Akamai event can show `policyId`, rule identifiers, rule versions, messages, tags, data, and `ruleActions` [30]. Third, the system owner or vendor can confirm the deployment.

Behavioral resemblance is lower-grade evidence. For example, several benign false positives that accumulate into one block might look like anomaly scoring. **Inference:** that pattern is compatible with CRS, ASE, a custom score, or multiple independent controls. It should be written as "score-like behavior observed" rather than "OWASP CRS detected."

Do not derive rule identity by probing many payload families. Besides the authorization problem, that method changes browser reputation, may activate Bot Manager or a penalty box, and confounds the experiment. It also risks triggering the rate controls the club is specifically trying to avoid.

**Section insight:** For MUJ, the ruleset question is a telemetry question, not a payload-crafting exercise.

## IP Allowlists and Trust-Boundary Failure Modes

Akamai's Client IP criterion can match an individual address, a range, or a CIDR block, and the documented condition can be used to deny selected end users [21]. The Property Manager documentation allows up to 300 addresses, ranges, or CIDRs in one match and up to three separate Client IP matches in a property or include-rule tree [21]. It also allows the configuration to use the connecting IP or a value from `X-Forwarded-For` [21]. These are product capabilities, not evidence that MUJ uses any particular one.

### Exact allowlist-pattern table

| Observed pattern | Plausible explanation | Evidence needed | Prohibited conclusion or action |
|---|---|---|---|
| Campus succeeds; residential network gets 403 | **Inference:** campus egress CIDR may be allowed, residential IP reputation may differ, or the application may require a campus context. | Approved config review plus one normal transaction from each preapproved context and correlated logs. | Do not claim an allowlist from the two statuses alone. Do not rotate residential proxies. |
| One residential ISP fails while another succeeds | **Inference:** reputation, geolocation, IPv4/IPv6 treatment, carrier NAT, or a narrow CIDR condition may differ. | Akamai event fields, client IP as seen by the edge, and policy action. | Do not enumerate the boundary by scanning neighboring addresses. |
| Same user changes outcome after moving networks | **Inference:** network identity may be part of the decision, but browser state and bot score may have changed too. | Preserve browser/session state and compare existing logs. | Do not replay session material from another network to test bypass. |
| A supplied `X-Forwarded-For` value appears to alter behavior | Akamai can be configured to use connecting IP or XFF [21], but trust behavior is configuration-specific. | Property configuration and trusted-proxy design review. | Never test by spoofing forwarding headers against production. |
| Origin accepts only Akamai edge traffic | **Inference:** this is an origin-access control, not an end-user campus allowlist. | Owner firewall and origin-access configuration. | Never seek or directly access an origin address to bypass Akamai. |
| Denials begin after a burst | Akamai rate policies can use average, burst, and penalty-box settings [28]; Bot Manager scores can also change with request history [17]. | Rate-policy and bot telemetry. | Do not repeat requests to estimate the threshold. |

A key trust-boundary distinction is often missed: "which source addresses may reach the origin" and "which end-user addresses may use the application" are different controls. **Inference:** even if MUJ's origin firewall accepts only Akamai infrastructure, that says nothing about whether campus users are allowlisted at the edge. Conflating them can lead to unsafe recommendations such as attempting direct-origin validation, which this report expressly rejects.

**Section insight:** Infer an IP policy only when the edge's observed client identity and the matched policy are available. Network-to-network status comparison is a lead, not proof.

## Low-Rate WAF-vs-Application Identification Runbook

The safest plan is passive-first, correlation-led, and explicitly bounded. It should be operated by, or alongside, MUJ personnel who can view Akamai and origin telemetry.

### Exact low-rate workflow

| Phase | Owner-approved action | Request budget | Evidence recorded | Stop condition |
|---|---|---:|---|---|
| 0. Authorization | Obtain written scope naming `mujslcm.jaipur.manipal.edu`, approved source networks, test account if needed, UTC window, contacts, and prohibited actions. | 0 | Approval record and escalation contact. | No written approval. |
| 1. Configuration inventory | Ask the Akamai administrator for security mode, custom-deny definitions, Bot Manager status, rate policies, Client IP criteria, and evaluation-mode availability. | 0 | Redacted configuration facts. | Administrator declines or information is outside scope. |
| 2. Passive incident collection | Collect a real user's saved response, complete headers, body, screenshot, redirect chain, UTC time, URL, public client IP, browser version, and whether the user was already authenticated. | 0 additional | Immutable incident bundle and body hash. | Credentials, tokens, or personal data cannot be safely redacted. |
| 3. Identity-plane check | Determine whether the final responding host is MUJ, Akamai-handled MUJ, or Microsoft login. MUJ's documented Office 365 flow uses Microsoft's login portal [35]. | 0 additional when using the saved trace | Host sequence and redirect sequence. | The trace crosses into an unapproved third-party identity transaction. |
| 4. Reference translation | If an error reference exists, have an authorized operator enter it into Akamai Edge Diagnostics. The tool can return WAF, network, request, client, edge, and origin details [31]. | 0 public requests | Translation result, redacted as necessary. | Reference cannot be resolved or access is unavailable. |
| 5. SIEM correlation | Search by request ID or a narrow UTC/client/host/path tuple. Akamai events can expose policy, rule, action, HTTP status, and response headers [30]. | 0 public requests | Matching event or documented no-match. | The time window is too broad or data access is not authorized. |
| 6. Origin correlation | Ask the IIS/application owner whether the same request reached the origin and what status or application event it produced. | 0 public requests | Origin presence, application trace ID, route, status, and timing. | Logs contain sensitive student data that cannot be minimized. |
| 7. One baseline navigation | Only if passive artifacts are insufficient, perform one ordinary browser navigation to the already public login page from one approved source. Do not add unusual methods, headers, paths, or input. | 1 | Normal headers, body hash, redirects, timing. | Any challenge, 429, unexpected redirect, or operator concern. |
| 8. Preapproved cohort check | Only when the explicit question is an allowlist, repeat the same ordinary navigation once from one other preapproved institutional context. Keep method, URL, browser, and timing policy constant. | 1 per approved context | Edge-observed IP and correlated events. | Outcomes begin changing, latency rises, or no logging is available. |
| 9. Staging positive control | If rule validation is necessary, the owner should use Akamai evaluation mode or a non-production environment. Evaluation mode records how rules would respond without production enforcement [25]. | Set by owner, outside this public runbook | Rule ID, policy, expected action, observed action. | No isolated environment or operator supervision. |
| 10. Closeout | Revoke temporary access, purge tokens, retain redacted evidence, and record unresolved alternatives. | 0 | Final evidence matrix and owner acknowledgment. | None. |

The recommended production request budget is intentionally tiny: one ordinary baseline navigation per approved context, not a sequence of synthetic "tests." This number is a conservative recommendation, not an Akamai product limit. The club should not attempt to find the rate threshold. Akamai documents that rate policies can moderate traffic using average, burst, and penalty-box parameters [28], but the example settings in the documentation are not evidence of MUJ's configuration.

### Exact correlation keys

| Key | Client source | Akamai source | Origin source | Use |
|---|---|---|---|---|
| UTC timestamp | Browser trace or saved incident | Event `start` and retrieval interval [30] | IIS/application timestamp | Bound the search to seconds, accounting for clock skew. |
| Host and path | Requested URL | Event `host` and `path` [30] | Site binding and application route | Prevent mixing the login page, API, and Microsoft redirect. |
| Request ID | Response or approved diagnostics | `requestId` in SIEM event data [30] | Forwarded correlation field if configured | Strongest shared key when available. |
| Client IP | User's observed public egress | `clientIP` [30] | Edge-forwarded client identity if trusted and logged | Evaluate allowlist or reputation explanations. |
| Status | Browser response | Event `status` [30] | Origin status | Determine whether the edge generated, replaced, or forwarded the result. |
| Rule evidence | Usually absent | Rules, versions, messages, tags, selectors, data, and actions [30] | Application authorization or validation event | Separate WAF detection from application denial. |
| Response headers | Browser trace | `responseHeaders` can appear in SIEM event details [30] | Origin header record | Detect edge additions or replacements without guessing from style. |

### Classification logic

1. **Confirmed edge security response:** The client artifact correlates to an Akamai security event with a deny, challenge, or other mitigating action, and the origin has no matching application request. This is the highest-confidence WAF or bot-control classification.

2. **Confirmed origin or application response:** The request appears in the origin log, the application records the relevant authorization or validation decision, and Akamai shows no mitigating rule action. Akamai may still have delivered the response, but it did not originate the denial.

3. **Edge-transformed origin response:** Origin logs show a response, while client and Akamai records show that edge logic changed the status, headers, body, or redirect. Akamai EdgeWorkers can change status and headers, so this is technically plausible [7].

4. **Identity-provider response:** The redirect chain terminates at Microsoft and the observed page belongs to that identity transaction. MUJ's official procedure uses `login.microsoftonline.com` [35]. Classify it separately rather than forcing it into WAF versus application.

5. **Indeterminate:** A 403 or challenge exists but no resolvable reference, request ID, security event, or origin correlation is available. "Indeterminate" is preferable to a confident but unsupported vendor claim.

**Section insight:** A low-rate workflow succeeds by reducing requests and increasing telemetry, not by making test inputs more exotic.

## Decision Matrix and Case Studies

### Exact confidence matrix

| Evidence combination | Classification | Confidence | Main caveat |
|---|---|---:|---|
| 403 only | Unknown denying layer | Very low | Any edge or application component can return a 4xx response [7]. |
| 403 plus generic deny body | Possible edge or application denial | Low | Akamai custom denies can be branded or redirected [23]. |
| Challenge plus changing browser behavior | Possible bot control | Medium-low | Bot Manager responses are tunable and deliberately nuanced [17]. |
| Resolvable Akamai reference with WAF details | Akamai-handled security response | High | Still verify that the translated event matches the user's transaction [31]. |
| `X-Akamai-Request-ID` plus matching SIEM deny action | Akamai security response | Very high | Requires authorized diagnostics and SIEM access [13][30]. |
| Origin log and application authorization event, no Akamai mitigating action | Application-layer denial | High | Ensure clocks and request IDs are aligned. |
| Origin status differs from client status and edge transformation is logged | Edge-transformed origin response | High | Identify whether the change came from security policy, delivery logic, or EdgeWorkers. |
| Campus/off-campus difference without logs | Possible IP policy or reputation difference | Low | Network, browser, identity, bot score, and cache state can all differ. |
| Rule IDs and versions from policy/SIEM | Specific Akamai rule evidence | High | Does not establish OWASP CRS unless metadata explicitly says so. |

### Case study 1: Akamai reference beats page appearance

**Scenario, explicitly hypothetical:** An MUJ user reports a 403 with an unfamiliar denial page and a complete reference string. The club's unsafe instinct would be to reproduce the response repeatedly from different networks. The better decision is to freeze the artifact and ask an authorized Akamai operator to translate the reference.

Akamai's translator can return the reason for failure, WAF details, applied property, URL, response code, date, client and connecting IPs, edge and origin IPs, user agent, and method [31]. If that record identifies a security action and the timestamp matches, the outcome is a high-confidence edge classification without generating another public request. What this reveals is the central mechanism of reliable fingerprinting: correlation creates certainty; visual resemblance does not.

### Case study 2: Microsoft identity is a third response plane

The MUJ portal publicly uses the `@muj.manipal.edu` identity suffix [32], Microsoft labels that suffix a managed MUJ realm [33], and MUJ's Office 365 procedure sends users to Microsoft's login portal [35]. A student who reports a blocked sign-in may therefore be describing an SLCM page, an Akamai response on the MUJ host, or a Microsoft identity response after redirection.

The decision is to save the redirect chain and final host before classifying the screen. If the response belongs to Microsoft, the outcome should be recorded as an identity-plane event unless a preceding MUJ or Akamai response supplies contrary evidence. The lesson is that vendor fingerprinting must follow transaction boundaries; otherwise a club may wrongly report an Akamai false positive or an ASP.NET authorization defect.

### Case study 3: Campus-only success does not prove an allowlist

**Scenario, explicitly hypothetical:** The portal loads from a campus network but produces a denial from a residential connection. Akamai supports Client IP conditions over addresses, ranges, and CIDRs [21], so a campus allowlist is plausible. Bot Manager also changes its response strategy based on scoring and request history [17], and rate policies can impose burst and penalty behavior [28].

The decision is not to add more networks. It is to compare one preapproved normal transaction per context and obtain the edge-observed client IP, matched policy action, and origin presence. If a Client IP rule matches, the result supports an allowlist conclusion. If a bot or rate action matches, the same external symptom has a different cause. This case shows why controlled variables without internal telemetry remain inadequate in a multi-layer edge architecture.

**Section insight:** Every strong case replaces repeated production requests with a better correlation key.

## Synthesis

The MUJ SLCM problem contains four mechanisms that can produce superficially similar outcomes but require different remedies.

| Mechanism | Scope | Typical evidence | Trade-off | Correct remedy |
|---|---|---|---|---|
| Akamai WAF policy | Request content and security policy at the edge | Translated reference, SIEM rule/action, request ID [30][31] | Blocks attacks but can produce false positives | Tune the specific rule or exception under owner control; validate in evaluation mode. |
| Akamai Bot Manager | Client behavior, browser signals, history, and bot score | Bot telemetry and tuned response segment [17] | Reduces automation abuse but visible challenges may vary | Adjust bot policy or support legitimate clients; do not teach clients to evade challenges. |
| Akamai rate policy | Request volume over configured windows | Rate-policy event and penalty context [28] | Absorbs surges but can affect shared campus or carrier-NAT addresses | Tune thresholds and exclusions from traffic data; never discover limits by stress. |
| MUJ IIS/application | Routing, authentication, authorization, validation, and application state | Origin request, application event, route, status, and trace ID | Enforces business rules but can be mistaken for edge denial | Correct application authorization, error handling, or account state. |
| Microsoft identity | Managed-domain sign-in and account security workflow | Redirect to Microsoft, tenant/realm context, identity logs [33][35] | Centralizes identity but adds another response plane | Investigate the identity transaction rather than changing WAF rules. |

The most important tension is that Akamai's strongest security features intentionally weaken stable external fingerprints. Custom denies change bodies and redirects [23]; EdgeWorkers change statuses and headers [7]; Bot Manager changes actions according to score and uses responses designed not to reveal too much [17]. Therefore, the absence of a famous Akamai header or page cannot disprove Akamai, while the presence of an Akamai delivery header cannot prove a WAF block.

A second tension is between OWASP familiarity and evidentiary precision. CRS offers a useful conceptual model because it documents anomaly scoring and thresholds [19]. Yet Akamai's documented production vocabulary is KRS and ASE [25]. Calling any score-like WAF "OWASP CRS" may sound technically informed but is less accurate than saying "the available evidence does not identify the managed ruleset."

A third tension is between experimental control and operational safety. Changing networks, headers, methods, paths, cookies, and request sequences can appear to isolate variables, but each change also alters bot, reputation, cache, application, or rate-policy state. The production-safe strategy is the opposite: make fewer requests, hold normal client behavior constant, and increase server-side observability.

The integrated recommendation is a shared incident record containing the client artifact, UTC time, URL, redirect chain, public egress IP, request or reference ID, Akamai event, and origin event. That record supports WAF tuning, application debugging, identity escalation, or allowlist review without encouraging unauthorized probing.

## VERDICT

**Overall verdict: Medium confidence in the architecture-specific assessment; very high confidence in the attribution methodology.**

1. **MUJ public and identity surface - High confidence.** The public portal and its `@muj.manipal.edu` sign-in context are directly visible [32]. Microsoft identifies the domain as a managed MUJ realm [33], and MUJ publishes a Microsoft 365 sign-in procedure [35].

2. **Akamai as the current MUJ edge - Medium confidence in this report.** It is a supplied scope premise, not a conclusion independently established from a saved MUJ response or owner configuration. Akamai product behavior is well supported, but applying it to a particular MUJ incident remains conditional.

3. **Any particular MUJ 403 is WAF-generated - Low confidence without artifacts; high confidence if correlated.** A 403 body or header is insufficient because Akamai permits custom denies and edge response modification [23][7]. A translated error reference or matching SIEM deny action raises confidence to high or very high [30][31].

4. **OWASP CRS is deployed - Low confidence and currently unproven.** The public evidence establishes CRS behavior generally and Akamai KRS/ASE terminology separately [19][25]. It does not establish equivalence or MUJ deployment.

5. **A campus or other IP allowlist exists - Low confidence and currently unproven.** Akamai supports such matching [21], but only configuration or matched-event evidence can establish MUJ's policy.

6. **Recommended action - Proceed only through owner-approved passive capture and log correlation.** Do not generate suspicious payloads, spoof client-IP headers, rotate proxies, automate challenges, discover rate thresholds, or attempt direct-origin access. If positive-control testing is required, MUJ should conduct it in Akamai evaluation mode or a non-production environment [25].

The defensible final statement for the club is: **"The supplied architecture is consistent with an Akamai-fronted MUJ SLCM application using Microsoft-managed identity, but public client artifacts alone cannot identify the current WAF ruleset, prove an IP allowlist, or distinguish every edge denial from an application response. Correlated Akamai and origin telemetry is required."**

## References

1. *JavaScript injection*. https://techdocs.akamai.com/terraform/docs/bmgr-rc-javascript-injection
2. *Akamai TechDocs*. https://techdocs.akamai.com/home
3. *Mitigate threats against your web applications*. https://techdocs.akamai.com/cloud-security/docs/app-api-protector
4. *Request Object*. https://techdocs.akamai.com/edgeworkers/docs/request-object
5. *Bot Manager | Product Brief | Akamai*. https://www.akamai.com/resources/product-brief/bot-manager
6. *Welcome to Origin IP ACL*. https://techdocs.akamai.com/origin-ip-acl/docs/welcome
7. *Response Object*. https://techdocs.akamai.com/edgeworkers/docs/response-object
8. *Custom deny action*. https://techdocs.akamai.com/terraform/docs/bmgr-rc-custom-deny-action
9. *RFC 9110: HTTP Semantics*. https://www.rfc-editor.org/rfc/rfc9110.html
10. *Web Application Firewall*. https://techdocs.akamai.com/property-mgr/docs/web-app-firewall
11. *About CIDR blocks*. https://techdocs.akamai.com/client-access-control/docs/about-cidr-blocks
12. *HTTP Errors &lt;httpErrors&gt; | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/configuration/system.webserver/httperrors/
13. *Pragma headers*. https://techdocs.akamai.com/edge-diagnostics/docs/pragma-headers
14. *Request Content (CURL)*. https://techdocs.akamai.com/edge-diagnostics/docs/request-content-curl
15. *Paranoia Levels :: CRS Documentation*. https://coreruleset.org/docs/2-how-crs-works/2-2-paranoia_levels/
16. *False Positives and Tuning :: CRS Documentation*. https://coreruleset.org/docs/2-how-crs-works/2-3-false-positives-and-tuning/
17. *Bot Manager | Bot Detection, Protection, and Management | Akamai*. http://akamai.com/products/bot-manager
18. *API client allow lists*. https://techdocs.akamai.com/identity-cloud/docs/api-client-allow-lists-1
19. *Anomaly Scoring :: CRS Documentation*. https://coreruleset.org/docs/2-how-crs-works/2-1-anomaly_scoring/
20. *CRS Documentation*. https://coreruleset.org/docs/index.print
21. *Client IP*. https://techdocs.akamai.com/property-mgr/docs/client-ip
22. *Rules*. https://techdocs.akamai.com/terraform/docs/as-ds-rules
23. *Custom deny*. https://techdocs.akamai.com/terraform/docs/as-rc-custom-deny
24. *SIEM Integration API*. https://techdocs.akamai.com/siem-integration/reference/api
25. *Rule upgrade*. https://techdocs.akamai.com/terraform/docs/as-rc-rule-upgrade
26. *Upgrade KRS ruleset*. https://techdocs.akamai.com/application-security/reference/put-policy-rules
27. *Adaptive Security Engine | Akamai *. https://www.akamai.com/resources/solution-brief/adaptive-security-engine
28. *Rate policy*. https://techdocs.akamai.com/terraform/docs/as-rc-rate-policy
29. *Akamai Blog | The Adaptive Security Engine – A Quantum Leap Forward for Application and API Protection*. https://www.akamai.com/blog/security/the-adaptive-security-engine-a-quantum-leap-forward-for-application
30. *Manage security events*. https://techdocs.akamai.com/powershell/docs/siem
31. *Translate Error String*. https://techdocs.akamai.com/edge-diagnostics/docs/translate-error-string
32. *http://mujslcm.jaipur.manipal.edu/*. http://mujslcm.jaipur.manipal.edu/
33. *http://login.microsoftonline.com/getuserrealm.srf?login=probe@muj.manipal.edu&xml=1*. http://login.microsoftonline.com/getuserrealm.srf?login=probe@muj.manipal.edu&xml=1
34. *http://dns.google/resolve?name=muj.manipal.edu&type=MX*. http://dns.google/resolve?name=muj.manipal.edu&type=MX
35. *http://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf*. http://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf
