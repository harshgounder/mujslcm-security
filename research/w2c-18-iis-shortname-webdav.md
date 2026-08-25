# MUJ SLCM IIS Exposure: Evidence, Limits, and Hardening

## Executive Summary

- **Evidence Boundary**: The public MUJ page confirms a portal with general, parent, and student sign-in paths [3]. The supplied labels - ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, Microsoft 365 identity, and the verb-response observations - were not independently established by the public page. -> Treat them as investigation hypotheses until MUJ's authorized administrators corroborate them from configuration, edge, origin, and identity records.

- **Short-Name Disclosure**: Microsoft states that IIS can reveal NTFS 8.3 short names through requests containing a tilde, exposing names that would not otherwise be visible [2]. -> Classify 8.3 enumeration as a plausible IIS-specific information-disclosure risk, but do not claim MUJ is vulnerable without authorized differential-response evidence and server-side confirmation.

- **Mitigation Is Two-Stage**: Disabling future 8.3-name creation does not by itself establish that old aliases are gone. Microsoft's `fsutil 8dot3name` documentation separately covers querying behavior, scanning for affected registry references, and stripping existing short names; Microsoft warns that removal can break applications whose registry entries still use them [7]. -> Inventory compatibility dependencies, stop new alias creation where safe, and remove existing aliases only after testing and backup.

- **WebDAV Remains Undetermined**: IIS WebDAV requires installation of the WebDAV module [17], while authorization is separately governed by inherited, per-URI authoring rules [17]. -> A single status code cannot prove either installation or effective write authorization.

- **PUT 411 Is Not Write Proof**: RFC 9110 defines 411 as refusal to accept a request without a defined `Content-Length`; the requester may repeat it with a valid length [14]. -> The reported PUT 411 establishes only that one request reached a component enforcing message-framing requirements. It does not establish file creation, WebDAV, writable storage, or authorization.

- **404 Is Deliberately Ambiguous**: RFC 9110 says 404 means the origin did not find a current representation or is unwilling to disclose that one exists [14]. -> Reported 404 responses to OPTIONS or DELETE cannot distinguish an absent route, deliberate concealment, MVC routing, request filtering, Akamai handling, or origin behavior.

- **Edge Attribution Matters**: Akamai Property Manager uses configurable behaviors to instruct edge servers how to manage requests [1]. -> An externally observed status must not automatically be attributed to IIS. MUJ should compare Akamai logs and property rules with IIS W3C logs before assigning a control or defect to either layer.

- **Configuration Beats Banner Guessing**: IIS exposes security-relevant behavior through `system.webServer` sections for request filtering, handlers, errors, WebDAV, HTTP headers, authentication, and related features. The `handlers` `accessPolicy` is explicitly a filtering mechanism rather than an enforceable security policy [6]. -> Administrators should validate the effective configuration hierarchy and filesystem access controls rather than assuming that a header or 404 page proves a safe configuration.

- **Education Context Raises Impact, Not Proof**: A university portal combines internet exposure, long-lived legacy integrations, numerous student accounts, and identity dependencies. **Inference:** those characteristics can amplify the effect of name disclosure or a writable endpoint, but they do not prove that any particular IIS misconfiguration exists at MUJ. -> Prioritize low-risk, owner-run verification and identity-aware remediation without publishing discovered names or testing write/delete operations against production.

## 1. Scope, Safety, and Evidence Model

This is a public-information and defensive-analysis report. It does not perform or recommend active enumeration, file creation, deletion, authentication bypass, or WebDAV modification against `mujslcm.jaipur.manipal.edu`. The report intentionally omits exploit payloads, wildcard strings, brute-force procedures, and scanner commands. Any active validation must occur only under written MUJ authorization, with a defined maintenance window, source IPs, rate limits, logging, rollback, and a non-production target wherever possible.

The portal itself publicly displays `WELCOME TO MUJ PORTAL`, a sign-in action, and a parent-login option [3]. That is the only target-specific application fact independently confirmed here. The rest of the proposed stack should be handled as supplied context, not as verified OSINT.

### Exact evidence-status table

| Assertion | Evidence class | What is established | What is not established |
|---|---|---|---|
| MUJ portal exists at the named URL | Publicly verified | The root page presents MUJ portal and sign-in text [3] | Backend topology, patch level, and effective authorization |
| ASP.NET MVC 5.3 | User-supplied | A version hypothesis | Exact package version or whether `5.3` is a valid description of the deployed MVC package |
| .NET Framework 4.x | User-supplied | A framework-family hypothesis | Exact 4.x release, servicing state, CLR mode, or application-pool settings |
| IIS 10 | User-supplied | A server-family hypothesis | Windows Server build, IIS servicing state, installed modules, or origin exposure |
| Akamai in front | User-supplied, architecturally plausible | An edge layer may exist | Which component generated each observed response |
| Microsoft 365 identity | User-supplied | An identity-layer hypothesis | Protocol, tenant policy, Conditional Access coverage, MFA strength, or local-account fallback |
| PUT -> 411 | User-supplied observation | One particular request reportedly received 411 | PUT authorization, WebDAV enablement, persistence, or origin handling |
| OPTIONS/DELETE -> 404 | User-supplied observation | Those particular requests reportedly received 404 | Whether the methods are disabled, concealed, unrouted, edge-blocked, or resource-specific |
| 8.3 short-name exposure | General IIS risk, target status unknown | IIS can disclose 8.3 aliases under affected conditions [2] | Whether MUJ has aliases, response differentiation, or an exploitable route |

**Decision-ready insight:** the present evidence supports a prioritized defensive review, not a vulnerability finding. The report's target-specific conclusions therefore use `Unknown`, `Not demonstrated`, and explicit inference labels rather than converting technology fingerprints into proof.

## 2. IIS 8.3 Short-Name Enumeration: Conditional Disclosure, Not Automatic Compromise

### 2.1 Mechanism and security significance

NTFS can maintain a second 8.3-compatible directory entry when a long filename is created. Microsoft's filesystem documentation states that when 8.3 creation is enabled, NTFS creates that additional short entry for a long filename [18]. Microsoft separately describes the IIS symptom: short file and directory names that have 8.3 equivalents can be detected, and specially formed requests containing a tilde can reveal otherwise non-visible names [2].

The security effect is information disclosure. An observer can potentially distinguish between candidate prefixes because affected IIS paths produce different responses for matching and nonmatching aliases. Directory browsing can remain disabled while this side channel still exists; a defensive description notes that responses can reveal file or directory existence even without directory listing [4].

This is not equivalent to reading the underlying file. It can disclose part of a name, extension, or directory structure, which may make later authorized assessment more focused. **Inference:** names suggesting backups, administrative functions, exports, or old releases would increase triage priority because they reveal attack-surface structure. That inference does not establish that the named content is reachable or sensitive.

### 2.2 Conditions that must all be considered

| Condition | Why it matters | MUJ status |
|---|---|---|
| Long-name objects have 8.3 aliases | No alias means there is nothing for this particular side channel to reveal | Unknown |
| The relevant content resides on NTFS-backed storage visible to IIS | The weakness is tied to filesystem alias resolution | Unknown |
| A reachable IIS path passes the relevant pattern to filesystem handling | MVC routing, Akamai, rewrite rules, and request filtering may alter handling | Unknown |
| Responses differ reliably between matches and nonmatches | Enumeration depends on an observable distinction [4] | Unknown |
| Existing aliases remain after a policy change | Stopping new alias creation and removing old aliases are separate tasks [7] | Unknown |
| Edge and origin behavior are separated | Akamai may normalize or answer a request before IIS | Unknown |

The key analytic conclusion is that an IIS 10 banner alone does not prove exposure. Conversely, disabling directory browsing does not disprove it, because directory browsing and short-name alias resolution are different mechanisms.

### 2.3 Remediation and compatibility case study

Microsoft's IIS support post associates the condition with `NtfsDisable8dot3NameCreation` and explains that the value controls 8.3-name creation across NTFS volumes [2]. Microsoft also documents more controlled `fsutil 8dot3name` operations for querying settings, scanning directories for affected registry references, testing removal, and stripping aliases [7].

**Case study - legacy compatibility versus disclosure reduction:** Imagine that MUJ's authorized administrator changes the system policy so future files no longer receive 8.3 aliases. That reduces future accumulation but does not demonstrate that aliases attached to existing portal releases have disappeared. If the administrator immediately strips every old alias, a legacy installer or registered component may fail because Microsoft warns that registry references to short names can make an application unserviceable or uninstallable [7].

The safe sequence is therefore compatibility inventory -> test scan -> backup -> staged policy change -> selective alias cleanup -> application regression testing. The mechanism explains the recommendation: short-name creation is a filesystem compatibility feature, while leakage occurs when IIS exposes a response oracle over those aliases. The implication is that both filesystem state and HTTP behavior matter. The recommended action is owner-run remediation in a cloned or pre-production environment, not internet-side brute-force confirmation.

### 2.4 Exact short-name disposition table

| Question | Current answer | Confidence | Required owner evidence |
|---|---|---:|---|
| Does the general IIS/NTFS weakness exist? | Yes, under documented conditions [2] | High | Microsoft documentation already establishes the class |
| Is MUJ SLCM affected? | Unknown | Low | Authorized controlled comparison plus filesystem alias inventory |
| Would disabling new 8.3 creation fully remediate old content? | Not necessarily | High | Compare existing aliases before and after policy change [7] |
| Can aliases be removed without risk? | Not universally | High | Microsoft warns of registry and application breakage [7] |
| Should the club enumerate names on production? | No | High | Use written authorization and owner-run testing; do not collect or publish discovered names |

## 3. WebDAV and HTTP Verbs: Why 411/404 Does Not Settle Enablement

### 3.1 IIS WebDAV has multiple independent gates

WebDAV is not synonymous with PUT. Microsoft says the WebDAV module must be installed to support WebDAV publishing [17]. Once present, `<authoringRules>` can be configured per URI, inherited by child URIs, and grant Read, Write, or Source access to selected users or groups [17]. Therefore, installation, enablement, authentication, route scope, and write authorization are separate questions.

Request filtering is another gate. Microsoft's guidance says request filtering can evaluate file extensions, hidden segments, verbs, limits, and URL sequences [10]. It also documents the subtle `applyToWebDAV` behavior: file-extension, hidden-segment, and verb filtering can apply differently to ordinary HTTP and WebDAV traffic [10]. A deployment can therefore block PUT or DELETE for ordinary handling while permitting an authenticated WebDAV path, or do the reverse.

RFC 4918 adds a resource-specific discovery signal. A client can examine the `DAV` response header from OPTIONS to learn the compliance classes of that resource [33]. A class 1 resource must return at least `1` in the DAV header on OPTIONS responses, while a class 2 resource returns at least `1, 2` [33]. The RFC emphasizes resources rather than whole servers because different resources on one server can expose different feature sets [33].

That scope rule is important: a positive DAV header on one authorized test URL does not prove WebDAV across the site, and a negative result on one MVC route does not prove the module is absent everywhere.

### 3.2 Exact interpretation of the supplied observations

| Supplied observation | Standards-compatible meaning | What it proves | What it does not prove | Assessment |
|---|---|---|---|---|
| PUT returned 411 | RFC 9110 says 411 means the server refuses a request without defined `Content-Length` [14] | A component processed enough of that message to demand length framing | WebDAV, authorization, writable storage, file creation, or IIS origin handling | Inconclusive |
| OPTIONS returned 404 | RFC 9110 permits 404 when no current representation is found or the server will not disclose one [14] | Only that the tested request received 404 | Method disabled, module absent, or origin identity | Inconclusive |
| DELETE returned 404 | The same 404 ambiguity applies [14] | Only the observed status for that resource/request | Successful or authorized deletion, WebDAV absence, or verb filtering | Inconclusive |
| No reported DAV header | RFC 4918 defines what positive DAV values mean [33] | Nothing further without the full response and resource context | Site-wide absence of WebDAV | Weak negative evidence only |
| No reported 405/Allow | `Allow` can list methods available to a target resource, and that set can change dynamically [14] | No affirmative method list was recorded | That every unlisted method is impossible at another route or layer | Inconclusive |

RFC 9110 defines OPTIONS as a request for communication options at the origin or an intervening intermediary, without implying a resource action [14]. That explicit intermediary scope is another reason not to treat one external OPTIONS response as a direct dump of IIS configuration.

PUT and DELETE also have precise semantics that are stronger than a mere status-code probe. PUT asks for target-resource state to be created or replaced by the enclosed representation [14]. DELETE asks the origin to remove the association between a target resource and its current functionality [14]. Because those are state-changing operations, an unauthorized university-club test must not send real content or attempt deletion on production.

### 3.3 WebDAV confidence and safe owner-side determination

**Finding:** WebDAV enablement on MUJ SLCM is **Unknown**.

**Reasoning summary, not private chain-of-thought:**

| Premise | Evidence | Consequence |
|---|---|---|
| WebDAV requires an installed IIS module | Microsoft installation documentation [17] | Check installed roles/modules directly |
| Effective authoring depends on per-URI inherited rules | Microsoft authoring-rule schema [17] | A site-wide yes/no answer may be inaccurate |
| Verb filtering can treat WebDAV specially | Microsoft `applyToWebDAV` guidance [10] | External PUT/DELETE statuses do not map cleanly to one switch |
| DAV compliance is advertised per resource | RFC 4918 [33] | Test only an approved non-production resource and retain full headers |
| 411 concerns message framing | RFC 9110 [14] | Do not label 411 as successful write access |
| 404 can conceal existence | RFC 9110 [14] | Do not label 404 as definitive disablement |

An authorized administrator can answer the question without internet-side exploitation by reviewing installed IIS role services, effective `<system.webServer><webdav>` configuration, inherited authoring rules, handlers/modules, request-filtering rules, Akamai property logic, and the corresponding IIS logs. A controlled test should use a dedicated non-production collection and a disposable principal with the minimum intended permissions. Success criteria should be based on server-side evidence and expected authorization boundaries, not merely on whether an unusual verb produces a non-404 response.

## 4. `system.webServer` Fingerprints: Signals Versus Configuration Proof

IIS configuration is hierarchical. Effective settings can come from `ApplicationHost.config`, site-level locations, and delegated application configuration. A response exposes only the result of that chain after routing, modules, handlers, the application, and possibly Akamai have acted.

### Exact fingerprint and control table

| Observable or configuration area | Relevant IIS control | Defensive interpretation | Hardening action |
|---|---|---|---|
| `X-Powered-By: ASP.NET` | `<httpProtocol><customHeaders>` | Microsoft documents `X-Powered-By: ASP.NET` in the default IIS 7 custom-header configuration [32] | Remove unnecessary framework advertising and verify at edge and origin |
| `X-AspNet-Version` | `<httpRuntime enableVersionHeader>` | ASP.NET's version-header setting defaults to `true`, but Microsoft says it is unnecessary for production and can be disabled [25] | Set the production policy to suppress it and regression-test monitoring dependencies |
| `Server` header | Request-filtering/server-header controls plus edge policy | A visible value is a fingerprint, not proof of patch level | Normalize at the intended layer; do not treat suppression as patching |
| Verb status differences | `<requestFiltering><verbs>` and handlers | Microsoft documents blocking PUT and DELETE while allowing different WebDAV treatment [10] | Deny unnecessary methods at both edge and origin; maintain explicit exceptions |
| DAV header | `<webdav>` plus authoring rules | A positive header advertises WebDAV compliance for the tested resource [33] | Keep WebDAV uninstalled if unused; otherwise restrict scope and principals |
| 404 body style | `<httpErrors>` and application custom errors | IIS can configure custom error responses; a branded 404 does not identify which component rejected a request [8] | Return minimal remote errors while preserving detailed internal diagnostics |
| Handler-specific response | `<handlers>` | The handler list maps requests to processing components; `accessPolicy` is not a standalone security boundary [6] | Remove unused handlers and enforce authorization and ACLs separately |
| Directory listing | `<directoryBrowse>` | Directory browsing controls listing content and defaults to disabled [29] | Keep disabled unless there is an explicit business requirement |
| HTTP substatus in logs | Site `<logFile>` fields | IIS W3C logging includes Method, URI, HTTP status, Win32 status, and HTTP substatus among its default field set [28] | Retain and correlate these fields with Akamai request IDs and timestamps |
| Failed request details | Failed Request Tracing | Tracing buffers request events and writes them when the defined failure condition occurs [21] | Enable narrowly for approved diagnostics; protect trace files as sensitive telemetry |
| Shared application pool | Application-pool identity and NTFS ACLs | Microsoft recommends one pool per site and warns that shared identities can expose another pool's filesystem resources [26] | Use isolated pools, unique identities, and least-privilege content ACLs |

Header suppression is defense in depth, not a vulnerability fix. Removing `X-Powered-By` or a `Server` value reduces low-cost fingerprinting, but an attacker may still infer IIS from error semantics or technology-specific behavior. The more important controls are patching, module minimization, request filtering, application-pool isolation, content ACLs, authentication, and monitoring.

### Case study - why a 404 can be a useful fingerprint but weak proof

Suppose an authorized tester observes a generic Akamai-branded 404 for OPTIONS and an IIS-style 404 for GET. **Inference:** the difference suggests that method-specific edge logic may be present. It still does not prove the origin's OPTIONS policy because RFC 9110 allows OPTIONS to be answered by an intermediary [14].

The proper response is correlation. IIS W3C logs can retain method, URI, status, substatus, Win32 status, and timing [28]. If no matching IIS event exists while Akamai logged the request, the edge probably terminated it. If both layers recorded it, the origin's `sc-status`, `sc-substatus`, handler, and failed-request trace can identify the decision point. This is stronger than visual comparison of public error pages.

## 5. Akamai, ASP.NET MVC, and Microsoft Identity: Separate Control Planes

Akamai, IIS, ASP.NET MVC, and Microsoft identity do not form one indivisible security control. Each can accept, normalize, reject, redirect, or authorize a request at a different stage.

### Exact layered-responsibility table

| Layer | Likely responsibility | Evidence available here | Target conclusion |
|---|---|---|---|
| Akamai edge | CDN/WAF behavior, request normalization, caching, and possibly immediate responses | Property Manager behaviors instruct Akamai edge servers how to manage requests [1] | Exact MUJ rules unknown |
| IIS 10 hypothesis | TLS termination if not at edge, request filtering, modules, handlers, errors, logging | General IIS controls are documented; target version is supplied | Not independently verified |
| ASP.NET MVC hypothesis | Route matching, controller actions, application-generated 404s, authentication integration | Public root only shows sign-in presentation [3] | Exact MVC version unknown |
| NTFS/content store | Short-name aliases and filesystem ACLs | Microsoft documents 8.3 behavior and application-pool isolation [7][26] | Target filesystem state unknown |
| Microsoft identity hypothesis | User authentication, token issuance, account policy, and conditional access | Identity placement is supplied, not proven by the root page | Tenant policy unknown |

The supplied `ASP.NET MVC 5.3` label deserves special caution. The official public release page located during this review is titled `What's New in ASP.NET MVC 5.2` [22]. That does not prove that a package described as 5.3 cannot exist in any component or private build, but it means the exact `5.3` label should not be promoted to a verified fact without package inventory or deployment records.

**Inference:** if Microsoft 365 or Entra ID handles student authentication, the identity control plane can reduce account risk through strong authentication policies, but it does not disable WebDAV, remove NTFS aliases, or correct IIS request filtering. Conversely, hardening IIS verbs does not guarantee that legacy local accounts, token validation, or sign-out behavior are safe. MUJ should therefore assign owners separately for edge configuration, Windows/IIS, application code, and identity policy.

## 6. IIS 10 Misconfiguration Patterns Relevant to Education Deployments

No source collected here measures the prevalence of these configurations across Indian universities or proves them at MUJ. The term `known patterns` below means configurations repeatedly addressed by Microsoft's IIS security documentation and applicable to education environments, not a claim that universities commonly run each one.

### Exact pattern-risk-remediation table

| Pattern | Mechanism | Education-specific impact | MUJ status | Priority |
|---|---|---|---|---:|
| Residual 8.3 aliases | IIS response differences expose short aliases [2] | Legacy student systems may retain old deployment names and integrations | Unknown | High to verify |
| WebDAV installed but unused | Optional publishing module expands methods and configuration | Publishing features may outlive a retired content workflow | Unknown | High to verify |
| Broad inherited authoring rules | Child URIs inherit parent permissions [17] | A rule intended for staff content could cover a student-facing subtree | Unknown | Critical if present |
| Request filtering bypass for WebDAV | `applyToWebDAV` can make filters treat WebDAV differently [10] | Administrators may believe a verb or extension is blocked when publishing bypasses it | Unknown | High |
| Unnecessary response headers | Framework headers disclose implementation details [32][25] | Lowers the cost of targeting a long-lived portal | Unknown | Medium |
| Remote detailed errors | Error configuration can expose component and path details | Student-generated malformed requests can become an information source | Unknown | High |
| Directory browsing enabled | IIS can expose directory listings; the default is disabled [29] | Reports, exports, or class material could be indexed unintentionally | Unknown | High |
| Shared pools or permissive ACLs | Shared identity can allow cross-site resource access [26] | One legacy departmental app could affect another application on the host | Unknown | Critical |
| Incomplete method logging | Missing method/substatus correlation hides control decisions | Large user populations make edge/origin diagnosis harder | Unknown | High |
| Banner hiding without patching | Cosmetic suppression leaves modules and software unchanged | Creates false assurance during annual audit | Unknown | Medium |
| Mixed edge/origin policies | Akamai and IIS can make different decisions | A method blocked at one hostname may reach an alternate origin path | Unknown | Critical to architecture review |
| Legacy framework ambiguity | An unspecified `.NET Framework 4.x` label does not state servicing level | Academic systems often require long compatibility windows | Unknown | High to inventory |

### Case study - an unused WebDAV feature

Consider a portal migrated from direct faculty publishing to a modern content workflow. The IIS WebDAV module remains installed, but the team believes PUT is blocked because a public request returned 411 and DELETE returned 404. That belief is unsound: 411 addresses missing content length [14], 404 can conceal existence [14], and request filtering can treat WebDAV differently [10].

The mechanism is configuration drift across layers. The implication is that a retired business process can leave a write-capable module or broad authoring rule behind even when the normal UI no longer uses it. The recommendation is to remove the module if there is no documented owner and requirement. If WebDAV is required, limit it to a dedicated path, authenticated principals, approved content types, explicit verbs, and least-privilege storage.

### Case study - shared application pools

A Windows host may serve more than one university application. Microsoft recommends one application pool per site and explains that applications sharing an identity can access another pool's filesystem resources unless isolation and ACLs are correct [26].

The mechanism is not an HTTP verb; it is process and filesystem trust. The implication is that even a modest application weakness can have broader impact if sites share identities or content permissions. The recommendation is unique application pools, virtual or dedicated identities, minimal NTFS grants, no write permission to executable or configuration directories, and separate storage for uploads.

## 7. Authorized Defensive Validation and Remediation Plan

The following plan is for MUJ's system owners or assessors operating under written authorization. It does not require the student club to probe production.

### Exact phased plan

| Phase | Owner action | Evidence retained | Pass criterion |
|---|---|---|---|
| 1. Confirm architecture | Document DNS/CDN, Akamai property, origin host, IIS site, application pool, storage volume, and identity flow | Approved data-flow diagram and owner list | Every request-processing layer has an accountable owner |
| 2. Preserve baseline | Export effective IIS and Akamai configurations and record versions and checksums | Configuration snapshots in restricted storage | Rollback is possible and secrets are redacted |
| 3. Inventory modules | Review installed IIS role services, global modules, site modules, handlers, and WebDAV | Installed-feature and effective-handler inventory | Unused publishing and sample features are absent |
| 4. Review verbs | Compare edge method policy, IIS request filtering, handlers, MVC routes, and WebDAV exceptions | Method-policy matrix per path | Only business-required methods reach each resource |
| 5. Review 8.3 state | Query volume policy, inventory existing aliases, and use Microsoft's compatibility scan/test process | Owner-side alias and dependency report | New aliases are disabled where safe; existing aliases are addressed without breaking dependencies |
| 6. Review WebDAV | Inspect `<webdav>`, authoring rules, inheritance, authentication, and `applyToWebDAV` | Effective per-URI WebDAV matrix | Module absent if unused; otherwise least privilege is demonstrated |
| 7. Correlate telemetry | Match approved test IDs across Akamai and IIS W3C logs | Edge event, IIS status/substatus, handler/trace evidence | The component producing each result is known |
| 8. Harden disclosure | Remove unnecessary framework headers and minimize remote error detail | Before/after headers and error samples | No unnecessary version disclosure; diagnostics remain available internally |
| 9. Enforce isolation | Verify one pool per site where feasible, unique identity, and least-privilege NTFS ACLs | Pool/identity/ACL review | Application content and upload paths have no unnecessary cross-access |
| 10. Regression test | Exercise login, student, parent, staff, upload, download, and administrative workflows in staging | Signed functional and security results | Hardening does not break required academic workflows |
| 11. Deploy and monitor | Apply through change control, monitor failures, and maintain rollback | Change record, dashboards, alert rules | No unexplained rise in 4xx/5xx, authentication failure, or support incidents |

### Detection and monitoring priorities

IIS W3C logs include method, URI, query, status, Win32 status, substatus, user agent, and timing among the default fields [28]. MUJ should preserve those fields and add a cross-layer request identifier where its Akamai design permits. Alerts should focus on bursts of unusual methods, repeated tilde-bearing path variations, repeated request-filtering substatus codes, and method/path combinations that are not part of normal portal workflows.

Such detection must avoid storing unnecessary credentials, tokens, or personal information. Access to edge, IIS, failed-request, and identity logs should follow role-based access and retention policy. Failed Request Tracing is powerful because it buffers request events and writes them when a defined failure occurs [21], but that detail also makes trace files sensitive operational records.

### Remediation order

| Order | Action | Rationale |
|---:|---|---|
| 1 | Remove unintended write/delete capability or broad WebDAV authoring | Highest direct integrity risk |
| 2 | Eliminate alternate-origin bypass and align Akamai/IIS policies | Prevents a correct edge rule from being bypassed |
| 3 | Correct application-pool and NTFS permissions | Limits cross-application and post-compromise impact |
| 4 | Address existing 8.3 aliases with compatibility testing | Removes the disclosure root cause without breaking legacy software |
| 5 | Minimize modules, handlers, detailed errors, and directory browsing | Shrinks exposure and diagnostic leakage |
| 6 | Suppress unnecessary headers | Reduces easy fingerprinting but does not replace the higher-value controls |
| 7 | Improve telemetry and recurring drift review | Makes the hardening durable |

## 8. Synthesis

### Cross-cutting comparison

| Dimension | 8.3 disclosure | WebDAV/verbs | `system.webServer` fingerprints | Akamai edge | Microsoft identity |
|---|---|---|---|---|---|
| Primary mechanism | NTFS alias plus IIS response distinction | Module, authoring, handler, and verb policy | Headers, errors, handlers, modules, and logging | Configurable intermediary behavior | Authentication and access policy |
| Main security property | Confidentiality of names | Integrity and authorization | Information disclosure and control correctness | Exposure reduction and request mediation | Account and session access |
| Best evidence | Filesystem inventory plus authorized differential test | Installed module, effective rules, and controlled resource test | Effective configuration and correlated logs | Property configuration and edge logs | Tenant and application registration records |
| Why public status codes mislead | A route may suppress the distinction | 411 and 404 do not prove enablement | Custom errors and handlers collapse different causes | Edge may answer before origin | Sign-in UI does not reveal policy strength |
| Highest-value remediation | Stop new aliases and safely remove old ones | Remove unused WebDAV or tightly scope it | Minimize features and enforce isolation | Align edge and origin policy | Strong, centrally governed authentication |
| Residual risk | Names may remain in backups or old volumes | Another route may have different rules | Headers can be inferred despite suppression | Alternate origin paths | Legacy/local authentication may bypass central policy |

Three tensions define the MUJ assessment.

First, security hardening and compatibility can conflict. Removing 8.3 aliases is attractive, but Microsoft warns that applications can depend on them [7]. The correct response is staged compatibility testing, not leaving the disclosure indefinitely or stripping aliases blindly.

Second, concealment and diagnosability can conflict. Minimal public errors and headers reduce reconnaissance, but operations still need detailed internal telemetry. IIS supports rich W3C fields [28] and failure-triggered tracing [21], allowing MUJ to keep public responses sparse while preserving restricted diagnostic evidence.

Third, edge controls and origin controls can diverge. An Akamai rule can reduce exposure, but it does not remediate an unsafe origin configuration. **Inference:** if an alternate path reaches IIS directly, edge-only blocking may fail. Conversely, origin-only hardening does not prevent noisy probing or resource consumption at the edge. The durable design is defense in depth with matching method policy, no publicly reachable origin bypass, and cross-layer correlation.

The holistic conclusion is therefore narrower but more reliable than a scanner-style verdict: the reported responses are useful triage signals, yet none establishes short-name exposure, WebDAV enablement, or write/delete authorization at MUJ. The server owners can resolve every major uncertainty through configuration inspection and controlled non-production tests without publishing sensitive names or performing unauthorized operations.

## VERDICT

**Overall verdict: No confirmed IIS vulnerability from the supplied public evidence. A focused owner-authorized IIS hardening review is warranted.**

| Question | Verdict | Confidence |
|---|---|---:|
| Is IIS 8.3 short-name enumeration a real applicable risk class? | Yes, conditionally [2] | High |
| Is MUJ SLCM demonstrably vulnerable to it? | Unknown; not demonstrated | Low |
| Does PUT 411 prove PUT or WebDAV is enabled? | No [14] | High |
| Do OPTIONS/DELETE 404 prove those verbs or WebDAV are disabled? | No; 404 is ambiguous [14] | High |
| Is WebDAV enabled on MUJ SLCM? | Unknown | Low |
| Are the exact MVC, .NET, IIS, Akamai, and identity versions independently verified here? | No; treat as supplied hypotheses | High |
| Is there enough evidence for remediation planning? | Yes, at the control-family level | High |
| Is there enough evidence for public vulnerability disclosure? | No | High |

**Confidence level: Moderate overall.** Confidence is high in the standards and Microsoft configuration analysis, but low for target-specific conclusions because no authorized origin-side configuration, complete response transcript, edge log, IIS log, filesystem inventory, or identity record was available. The highest-priority next step is not broader internet probing. It is an owner-run comparison of Akamai and IIS method policy, WebDAV installation and authoring rules, NTFS 8.3 state, application-pool isolation, and correlated logs.

## References

1. *Behaviors*. https://techdocs.akamai.com/property-mgr/docs/behs
2. *IIS Short name Enumeration*. https://techcommunity.microsoft.com/blog/iis-support-blog/iis-short-name-enumeration/3951320
3. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
4. *IIS Short File Name Enumeration – Brackish Security*. https://brackish.io/2023/11/17/iis-short-file-name-enumeration
5. *Microsoft Entra Conditional Access: Zero Trust Policy Engine - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/conditional-access/overview
6. *learn.microsoft.com*. https://learn.microsoft.com/en-us/iis/configuration/system.webserver/handlers
7. *fsutil 8dot3name | Microsoft Learn*. https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/fsutil-8dot3name
8. *HTTP Errors &lt;httpErrors&gt; | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/configuration/system.webserver/httperrors
9. *login.microsoftonline.com*. http://login.microsoftonline.com/muj.manipal.edu/federationmetadata/2007-06/federationmetadata.xml
10. *How to Configure WebDAV with Request Filtering | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/publish/using-webdav/how-to-configure-webdav-with-request-filtering
11. *CISA and NSA Release New Guidance on Identity and Access Management | CISA*. https://www.cisa.gov/news-events/alerts/2023/10/04/cisa-and-nsa-release-new-guidance-identity-and-access-management
12. *Verbs &lt;verbs&gt; | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/configuration/system.webserver/security/requestfiltering/verbs
13. *Http Status Code*. https://learn.microsoft.com/en-us/troubleshoot/developer/webapps/iis/health-diagnostic-performance/http-status-code
14. *RFC 9110: HTTP Semantics*. https://www.rfc-editor.org/rfc/rfc9110.html
15. *WebDAV &lt;webdav&gt; | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/configuration/system.webserver/webdav
16. *Request Filtering <requestFiltering> | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/configuration/system.webserver/security/requestfiltering
17. *WebDAV Authoring Rules &lt;authoringRules&gt; | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/configuration/system.webserver/webdav/authoringrules
18. *fsutil behavior | Microsoft Learn*. https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/fsutil-behavior
19. *Configure Request Filtering in IIS | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/manage/configuring-security/configure-request-filtering-in-iis
20. *Windows Authentication &lt;windowsAuthentication&gt; | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/configuration/system.webserver/security/authentication/windowsauthentication
21. *Troubleshoot failed requests using tracing in IIS 7 - Internet Information Services | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/troubleshoot/using-failed-request-tracing/troubleshooting-failed-requests-using-tracing-in-iis
22. *What’s New in ASP.NET MVC 5.2 | Microsoft Learn*. https://learn.microsoft.com/en-us/aspnet/mvc/overview/releases/whats-new-in-aspnet-mvc-52
23. *ASP.NET official support policy | .NET*. https://dotnet.microsoft.com/en-us/platform/support/policy/aspnet
24. *Application Pool Identities | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/manage/configuring-security/application-pool-identities
25. *HttpRuntimeSection.EnableVersionHeader Property (System.Web.Configuration) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.configuration.httpruntimesection.enableversionheader?view=netframework-4.8.1
26. *Ensure Security Isolation for Web Sites | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/manage/configuring-security/ensure-security-isolation-for-web-sites
27. *Internet Information Services (IIS) - Microsoft Lifecycle | Microsoft Learn*. https://learn.microsoft.com/en-us/lifecycle/products/internet-information-services-iis
28. *Log Files for a Web Site &lt;logFile&gt; | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/configuration/system.applicationhost/sites/site/logfile/
29. *Directory Browse &lt;directoryBrowse&gt; | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/configuration/system.webServer/directoryBrowse/
30. *HSTS settings for a Web Site &lt;hsts&gt; | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/configuration/system.applicationhost/sites/site/hsts
31. *Microsoft .NET Framework - Microsoft Lifecycle | Microsoft Learn*. https://learn.microsoft.com/en-us/lifecycle/products/microsoft-net-framework
32. *Custom Headers &lt;customHeaders&gt; | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/configuration/system.webserver/httpprotocol/customheaders/
33. *rfc-editor.org*. https://www.rfc-editor.org/rfc/rfc4918.html
