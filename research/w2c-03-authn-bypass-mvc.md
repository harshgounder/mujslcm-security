# MUJ SLCM Authorization Risk and Hardening Report

## Executive Summary

- **No Public Bypass Is Established**: Public material confirms the MUJ SLCM login surface, but it does not expose source code, effective filter registration, route tables, handler mappings, or production IIS configuration. The login form publicly exposes `UserName`, `Password`, `__RequestVerificationToken`, `EmailFor`, and `LoginFor` fields, plus a Microsoft password-reset destination [3]. Therefore, this report treats every MUJ-specific bypass scenario as an **INFERENCE**, not a finding, and recommends source-assisted review rather than production probing.

- **Authorization Scope Is the Primary Risk**: In classic ASP.NET MVC, `[Authorize]` can restrict an action or a controller; applying it to a controller restricts all of that controller's actions, while `[AllowAnonymous]` creates an explicit exception [9]. The decisive question is not whether `/Student/` or `/Staff/` exists, but whether every route-to-action resolution reaches an effective authorization policy. The club should prioritize an action inventory and effective-policy matrix.

- **Routes Are Security-Relevant Inputs, Not Security Boundaries**: The conventional MVC route maps three segments to `{controller}/{action}/{id}`, with defaults of `Home`, `Index`, and an empty `id` [11]. Any custom authorization logic that reasons from raw URL text, rather than the selected controller, action, authenticated principal, and requested object, can disagree with routing. Route values should be treated as untrusted inputs and authorization should run after canonical route selection.

- **The `/api/` Family Requires Separate Attention**: Classic ASP.NET Web API commonly uses `api/{controller}/{id}`, matches the URI against a route table, derives a controller from `{controller}`, and selects an action partly by HTTP verb [13]. **INFERENCE:** if MUJ has a classic Web API surface, an MVC-only authorization review can miss it. Review MVC and Web API controllers, filters, and role checks as distinct inventories.

- **Normalization Risk Comes From Layer Disagreement**: IIS Request Filtering can govern denied URL sequences, extensions, hidden segments, request limits, verbs, double escaping, and high-bit characters [21]. Windows also treats backslash as a path-component separator and advises against file or directory names ending in a space or period [14]. These facts do not prove a bypass, but they justify equivalence testing across proxy, IIS, routing, authorization, and handler layers in an authorized test environment.

- **Unicode and Case Rules Must Be Explicit**: Unicode characters can have multiple equivalent binary representations; .NET supports normalization forms C, D, KC, and KD, and Microsoft says normalized strings can then be compared ordinally [10]. Microsoft further recommends ordinal comparison for filtering or access-control decisions [5]. MUJ should define one route and identifier canonicalization policy, reject ambiguous forms early, and use ordinal or ordinal-ignore-case comparison according to the identifier's documented semantics.

- **Static and Dynamic Handling Need Policy Parity**: IIS can allow or deny file extensions and hide URL segments before MVC executes [21]. **INFERENCE:** if a logical name can be served by a static handler in one form and routed to MVC in another, controller filters alone cannot guarantee parity. Sensitive data should not reside under the public web root, and static-handler authorization must be reviewed independently.

- **Deny by Default Is the Controlling Design Principle**: OWASP recommends deny-by-default access control, global application-wide configuration, permission validation on every request, and centralized handling of failed checks [8]. The recommended MUJ design is a global authenticated default, narrow and documented anonymous exceptions, role or ownership checks at the action or service layer, and automated tests generated from the route/action inventory.

## 1. Scope, Evidence Classes, and Safety Boundary

This report uses only publicly available documentation and previously collected public MUJ pages. It does not attempt authentication, submit credentials, vary live production paths, enumerate hidden actions, or send malformed requests. It also omits operational bypass payloads. Any validation procedure below is intended only for MUJ-controlled source code, a local clone, or a written-authorization staging environment.

The requested technology description - ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Microsoft Azure AS8075, and Microsoft 365 identity - is treated as a **USER-SUPPLIED PREMISE**. Public search in this research run did not independently establish the exact MVC, .NET Framework, or IIS versions, nor did it establish that the current MUJ hostname is directly originated by an AS8075 address. This distinction matters because headers, network ownership, a login-page appearance, and framework artifacts do not by themselves establish every application-layer version.

| Evidence class | What is supported | What is not supported | Decision use |
|---|---|---|---|
| **Public observation** | The MUJ SLCM URL presents a sign-in form with named username, password, hidden, and login-selection fields, and links to Microsoft's password-reset service [3]. The public page also presents Student and Parent sign-in choices [3]. | No public observation establishes a successful bypass, an unprotected business action, or a specific internal controller list. | Use to define the visible trust boundary only. |
| **Official MUJ guidance** | MUJ's FAQ identifies the SLCM registration URL, a `name.registration number` username pattern, use of the official Outlook-ID password, and the university helpline [1]. MUJ's Office 365 help material directs users to Microsoft's login service and documents security-information methods [6]. | The documents do not disclose route tables, filter registrations, role policies, or handler mappings. | Use to connect the SLCM login experience to the institutional identity workflow without claiming implementation details. |
| **Identity-realm observation** | Microsoft's public realm response for an address at `muj.manipal.edu` identifies that realm and returns Microsoft Online federation-related fields [2]. | It does not prove how every SLCM request authenticates or how application roles are assigned. | Use as evidence of a Microsoft 365 identity dependency, not of application authorization correctness. |
| **Framework fact** | Microsoft documents MVC authorization-filter scope, conventional routes, Web API routes, IIS request filtering, Windows path conventions, and .NET string comparison [9][11][13][21][14][10]. | A documented framework capability does not show that MUJ enabled, disabled, or misconfigured it. | Use to construct defensive review hypotheses. |
| **MUJ-specific inference** | `/Home/`, `/Student/`, `/Staff/`, and `/api/` are analyzed as route-family guesses supplied by the question. | Their existence, controller names, action names, and authorization state are unverified. | Never present as a vulnerability or operational target. |

### Reasoning transparency

I cannot provide private chain-of-thought or hidden deliberative notes. The auditable reasoning method used here is: (1) separate observed facts from supplied premises; (2) identify the request-processing layers that can interpret a path; (3) ask whether those layers can disagree; (4) map the disagreement to an authorization invariant; and (5) recommend a source-level or staging-only test of that invariant. A scenario is rated above Low confidence only when both a documented framework mechanism and MUJ-specific evidence support it. No scenario reached that threshold as an actual MUJ vulnerability.

**Decision-ready insight:** The club has enough evidence for a rigorous defensive review plan, but not enough evidence to report an authentication bypass.

## 2. Public MUJ SLCM Ecosystem and Trust Boundaries

The public SLCM page is a conventional credential-entry boundary. Its form exposes `UserName` and `Password`, hidden fields named `__RequestVerificationToken`, `EmailFor`, and `LoginFor`, and a `Forgot Password?` link to `passwordreset.microsoftonline.com` [3]. The public rendering also distinguishes Student and Parent login choices [3]. These observations support an application boundary with more than one login context, but they do not reveal whether the contexts share controllers, cookies, claims, or role providers.

MUJ's FAQ states that the registration link is `https://mujslcm.jaipur.manipal.edu/`, describes the username as a name plus registration number, and says the password follows the official Outlook ID [1]. A separate MUJ Office 365 guide directs student or employee users to `https://login.microsoftonline.com/` and shows security-information methods including phone, email, and Microsoft Authenticator [6]. Together, those sources support an institutional identity relationship. They do not establish that Microsoft 365 performs SLCM's final authorization decision; that decision may still occur in application roles, claims transformation, a local database, or a combination.

This distinction separates **authentication** from **authorization**. Authentication establishes who the principal is. Authorization decides whether that principal may invoke a selected action or access a selected object. The requested bypass patterns are therefore better described as authorization-dispatch or canonicalization risks. A path trick that reaches the same login page is not a bypass. A real issue would require an unauthorized principal to reach protected functionality or data because different layers interpreted the request differently.

| Trust boundary | Publicly supported role | Defensive question | MUJ-specific status |
|---|---|---|---|
| Browser to SLCM login | Collects username, password, and login-context fields [3]. | Are all anonymous endpoints explicitly inventoried and narrowly scoped? | Public surface observed; policy unknown. |
| SLCM to Microsoft identity workflow | MUJ documents Microsoft sign-in and MFA-method management [6]. | Are authenticated identity claims validated for issuer, audience, freshness, and intended user type before local authorization? | Integration relationship supported; claim-processing details unknown. |
| IIS to ASP.NET routing | IIS can filter URL sequences, extensions, hidden segments, verbs, encodings, and request size before application routing [21][15]. | Does IIS accept or transform a request differently from the router or authorization code? | Configuration unknown. |
| MVC router to controller action | The conventional route maps URL segments to controller, action, and `id` values [11]. | Is authorization attached to every selected action regardless of raw URL form? | Route table unknown. |
| Web API router to API action | The conventional API route uses `api/{controller}/{id}` and HTTP verbs help select actions [13]. | Are API authorization policies registered and tested independently of MVC? | Existence of API surface is an inference. |
| Action to object/service layer | OWASP identifies IDOR when user-supplied references retrieve objects without sufficient authorization [4]. | Is ownership or entitlement checked for the resolved object, not merely for the route? | Business-object model unknown. |

**Decision-ready insight:** Microsoft 365 identity reduces neither the need for application authorization nor the risk of route-to-action policy gaps. MUJ should document the exact handoff from identity claims to local roles and object-level permissions.

## 3. How Centralized MVC Authorization Can Succeed or Fail

Microsoft's classic MVC documentation says `AuthorizeAttribute` restricts a controller or action to users meeting the authorization requirement [9]. The attribute can be applied to classes and methods, is inherited, and permits multiple instances [9]. When applied to an action, it restricts that action; when applied to a controller, it restricts all actions in that controller [9]. An explicit `AllowAnonymousAttribute` can make a particular action available without the authorization restriction [9].

Authorization filters execute before action filters in the MVC filter sequence [7]. That is a strong framework hook, but the hook only helps if the correct filter is effective for the selected action. A controller may be protected while a second controller offering equivalent functionality is not. A custom authorization attribute may make a decision from a route string that was normalized differently earlier. An anonymous exception may be broader than intended. A static handler may serve a resource without entering MVC at all. These are design-review possibilities, not observations about MUJ.

If an MVC authorization failure returns HTTP 401, forms authentication can redirect the browser to a login page [9]. A reviewer must therefore distinguish the underlying authorization result from the browser's final page. Redirect equivalence is not sufficient evidence that two request forms followed the same filter and handler path. In authorized automated tests, capture the selected endpoint, handler, policy, principal, response status before redirect rewriting, and any final redirect separately.

OWASP's guidance supplies the proper invariant: deny by default, prefer application-wide access-control configuration, check permissions on every request, and centralize failed-check handling [8]. A centralized `[Authorize]` gate is valuable when it is a true default policy. It is fragile when "centralized" means a custom prefix check, one base controller that not all controllers inherit, or a manually maintained list of protected routes.

| Gate design | Expected strength | Characteristic failure mode | Required evidence |
|---|---|---|---|
| Global authenticated default plus narrow anonymous exceptions | Strongest starting point because new endpoints inherit denial; aligned with OWASP's application-wide and deny-by-default guidance [8]. | An exception is too broad, a second framework pipeline is omitted, or object-level permission checks are absent. | Global filter registration, anonymous-action inventory, MVC/API parity, and object-policy tests. |
| Controller-level `[Authorize]` | Protects all actions selected on that controller [9]. | A parallel controller, inherited override, or non-MVC handler exposes equivalent functionality. | Complete controller/action/handler inventory. |
| Action-level `[Authorize]` | Precise per action [9]. | A newly added or rarely used action omits the attribute. | Build-time rule requiring an explicit protected or anonymous classification for every action. |
| Custom raw-path gate | Potentially brittle. | The gate and router canonicalize route text differently. | Canonicalization specification and equivalence tests at each pipeline layer. |
| Menu-only or client-side hiding | Not a server authorization boundary. OWASP requires enforcement on a trusted service layer and validation on every request [22][8]. | Direct navigation reaches the server action despite an absent link. | Server-side policy trace for every endpoint. |

**Decision-ready insight:** The best audit question is, "What effective policy protects each resolved endpoint and object?" It is not, "Does this URL look protected?"

## 4. Authentication-Bypass Pattern Matrix

The following table maps every requested pattern to the four supplied route-family guesses. Each MUJ mapping is explicitly an **INFERENCE**. The table intentionally avoids concrete malformed production URLs.

| Pattern | Documented mechanism | `/Home/` inference | `/Student/` inference | `/Staff/` inference | `/api/` inference | Safe verification invariant | Primary control |
|---|---|---|---|---|---|---|---|
| Route-parameter tricks | Conventional MVC routing maps segments to controller, action, and `id`, with defaults for omitted values [11]. Web API maps route placeholders to controller and action parameters [13]. | A default or optional value could select an action different from one assumed by custom path logic. | An identifier could be mistaken for proof of student ownership. | An action or identifier could be trusted without checking the staff role. | `{id}` or another route value could select an object without ownership authorization. | Every equivalent route resolution has the same effective policy; every object lookup checks entitlement. | Authorize the selected endpoint and resolved object, never the textual prefix. |
| Trailing slash variation | MVC route defaults mean different textual paths can resolve through the same route logic [11]. | The root, `Home`, and `Home/Index` representations may be functionally related. | A trailing separator must not change the effective student policy. | A trailing separator must not change the effective staff policy. | API route matching must preserve authorization regardless of terminal separator handling. | Canonically equivalent requests select the same handler and policy, or noncanonical forms are rejected. | One canonical form, early rejection or redirect, and post-routing authorization. |
| Trailing dot or space | Windows advises not ending file or directory names with a space or period [14]. IIS can deny selected URL sequences [12]. | A dynamic route and filesystem interpretation could diverge. | Same risk if a logical path approaches a physical directory or file boundary. | Higher impact if staff-only content is stored below a public path. | Relevant only if API paths can encounter file or handler resolution. | No accepted representation changes handler class, resource identity, or policy. | Reject ambiguous terminal characters before dispatch and log the rejection. |
| Backslash variation | Windows uses backslash to separate path components, and both slash and backslash are reserved in file names [14]. | IIS, routing, rewrite, and filesystem layers must agree on segment boundaries. | A prefix policy must not see one segment while the handler sees two. | Same, with role separation treated as high impact. | Verify API routing and upstream proxy interpretation agree. | All layers produce one canonical segment sequence, or the request is rejected. | Reject alternate separators at the edge; never normalize after an authorization decision. |
| Unicode normalization | Equivalent Unicode characters can have different binary representations; normalization produces a canonical representation for comparison [10]. IIS Request Filtering's high-bit-character setting controls whether non-ASCII URL characters are accepted; the documented default is `true` [21]. | A custom comparison against `Home` could disagree with later normalization. | Usernames, identifiers, or action labels could compare inconsistently. | Role or username comparisons are especially sensitive. | JSON, route, query, and path canonicalization may differ. | Normalize once at the trust boundary and compare the canonical identifier consistently. | Defined normalization form, restricted identifier alphabet where practical, and ordinal comparison. |
| Case-sensitivity gap | Microsoft warns that culture-sensitive handling of user names, file paths, and system names can create security issues [5] and recommends ordinal comparison for access-control filtering [5]. | `Home` variants must not change policy attachment. | Student identifiers and route labels need documented case semantics. | Staff role names and account identifiers need fixed semantics. | Controller/action and object-key comparisons must use explicit rules. | Every supported case variant has identical resource identity and policy; unsupported variants are rejected. | `Ordinal` or `OrdinalIgnoreCase` according to a written identifier contract. |
| Extensionless-routing conflict | Conventional MVC routes are extensionless, while IIS can independently allow or deny file extensions [11][21]. | A logical action name and a physical resource name could enter different handlers. | A download or report endpoint deserves handler-parity review. | Administrative exports have high consequence if handled statically. | API-like names should not collide with physical resources or alternate handlers. | No sensitive logical resource has both static and dynamic resolution paths with different policies. | Remove sensitive files from web root; explicit handler mappings and extension allowlists. |
| Static-file handler shadow | IIS hidden-segment and extension rules can act before MVC controller filters [21]. | A public asset must remain public and contain no protected data. | Student documents must not be directly web-addressable static files. | Staff-only files must be outside public static roots. | API response snapshots or exports must not exist as public files. | Static-handler inventory contains no protected resource; static and dynamic access policies cannot diverge. | Store protected content outside web root and serve it through an authorized action/service. |
| Direct action lacking `[Authorize]` | MVC protects an action or controller only where the attribute or an effective global policy applies [9]. OWASP describes direct access risk when user input reaches resources without sufficient authorization [4]. | Public login/help actions may be deliberately anonymous; all others need explicit classification. | Every student action requires authenticated and object-level policy unless deliberately public. | Every staff action requires authenticated role/policy enforcement. | Every API operation needs its own effective policy and object check. | Every routable action is classified as protected or intentionally anonymous, with a test proving the expected result. | Global deny-by-default plus an allowlisted anonymous-action manifest. |

**Decision-ready insight:** Direct-action coverage and API-policy separation are the highest-priority review areas. Canonicalization scenarios matter primarily when authorization is based on raw path text or when requests can leave the MVC pipeline.

## 5. Deeper Analysis of the Normalization Patterns

### 5.1 Route parameters and direct object access

The conventional MVC route is `{controller}/{action}/{id}` [11]. The conventional Web API route is `api/{controller}/{id}`, and route placeholders can become action parameters [13]. These are dispatch mechanisms, not authorization decisions. An `id` can identify a record, but possession of an identifier does not establish ownership or entitlement.

OWASP defines IDOR as direct access to an object through user-supplied input without sufficient authorization [4]. **INFERENCE:** for `/Student/`, the important case is not merely whether a user is authenticated as some student; it is whether the service verifies that the requested academic, financial, attendance, or profile object belongs to that student or is otherwise permitted. **INFERENCE:** for `/Staff/`, a staff role may still be too broad if departmental or functional boundaries apply. **INFERENCE:** for `/api/`, object authorization must be identical whether an identifier arrives in a route, query parameter, body, or composite key.

The remedy is policy binding after route selection and again at the object or service boundary. Route constraints can improve input quality, but they cannot replace an entitlement check. Automated tests should use two synthetic accounts with deliberately disjoint fixture objects in a nonproduction environment, because the property being tested is cross-principal isolation rather than the secrecy of identifiers.

### 5.2 Trailing separators, dots, and backslashes

A trailing slash can be a benign canonicalization issue, while a trailing dot, space, or backslash can cross from URI interpretation into Windows and IIS semantics. Windows documents backslash as a component separator and warns against terminal periods or spaces in names [14]. IIS supplies configurable request filtering, including denied sequences and identifiable 404 substatus codes [12]. None of those facts proves that a specific MUJ request is transformed in a dangerous way.

The defensive concern is a time-of-check/time-of-use disagreement: a custom gate examines one string, while URL Rewrite, IIS, ASP.NET routing, or a file handler later interprets another logical path. The safe architecture either rejects ambiguous forms before any authorization decision or canonicalizes once and passes the canonical representation through every later layer. Repeated decode-normalize-authorize cycles are dangerous because each transformation creates another opportunity for disagreement.

For MUJ, the club should not test malformed variants against production. It should ask the application owner for the effective `web.config`, rewrite rules, request-filtering configuration, route registrations, and reverse-proxy rules. A local pipeline test can then assert that each equivalence class either produces one endpoint and one policy or is rejected consistently.

### 5.3 Unicode and case sensitivity

Microsoft documents that equivalent Unicode text may have more than one binary representation and that normalization permits subsequent ordinal comparison [10]. Microsoft also warns that culturally interpreted user names and file paths can lead to security issues [5]. For access-control filtering, Microsoft's guidance is to use ordinal comparison [5].

**INFERENCE:** risk exists if a MUJ customization compares a route, username, role, department code, or resource key before normalization, while another component compares it afterward. Case folding introduces a related issue: culture-sensitive lowercasing can produce results that differ by locale, while route and identity identifiers are normally non-linguistic tokens.

A safe policy must be field-specific. Route names can usually be restricted to a narrow ASCII grammar. Human display names should not be authorization identifiers. Usernames and role names need a documented normalization and case contract shared by account provisioning, sign-in, claims transformation, database lookup, and authorization. Compatibility normalization should not be selected casually because it can intentionally collapse characters that Unicode treats as compatibility equivalents. The owner should choose the policy, migrate existing identifiers safely, and reject collisions.

### 5.4 Extensionless routes and static-handler shadows

MVC's conventional route is extensionless [11], while IIS can make independent decisions about file extensions and hidden segments [21]. **INFERENCE:** a risk arises if a protected logical resource can also be resolved as a physical file, a default document, an alternate extension, or another handler whose access policy differs from MVC's. The issue is not that static files are inherently unsafe; it is that `[Authorize]` cannot protect a request that never reaches the MVC authorization filter.

For `/Home/`, this most often concerns public assets and default documents. For `/Student/` and `/Staff/`, the high-consequence examples are generated reports, exports, uploaded documents, temporary files, or cached responses placed under a public directory. For `/api/`, snapshots, debug artifacts, or serialized output should not be web-addressable files. These are scenario classes, not claims that MUJ stores such files.

The robust control is architectural: keep protected content outside the web root, retrieve it through a service that performs authorization, and configure a restrictive static-extension allowlist. Inventory every IIS handler and module that can serve content. Test response origin by handler identity, not merely by comparing status codes or page appearance.

**Decision-ready insight:** Normalization defenses should reduce ambiguity, but the stronger invariant is handler-independent authorization. If a resource is sensitive, no alternate handler should be able to serve it.

## 6. Route-Family Defensive Case Studies

These are **INFERENCE-BASED DESIGN-REVIEW CASE STUDIES**, not reports of observed MUJ behavior.

| Route family | Intended role assumption | Main review question | Highest-value control | Confidence that the risk class is relevant | Confidence that MUJ is vulnerable |
|---|---|---|---|---|---|
| `/Home/` | Mixed public and authenticated entry points | Are anonymous exceptions limited to login, help, and other explicitly public actions? | Controller/global authenticated default with an anonymous-action allowlist. | High for any MVC login application. | Low. |
| `/Student/` | Authenticated student self-service | Does every action verify both student authentication and ownership of the resolved record? | Service-layer ownership policy plus cross-account fixture tests. | High as a general self-service risk. | Low. |
| `/Staff/` | Authenticated staff functions | Are staff permissions differentiated by function, department, and operation rather than one broad role? | Least-privilege policy and action-by-role matrix. | Medium to high as a general administrative risk. | Low. |
| `/api/` | Programmatic MVC-adjacent or Web API access | Is the API pipeline separately inventoried and protected for every verb and object? | API-specific deny-by-default filters and contract tests. | Medium because the route's existence is unverified. | Very low. |

### Case study A: `/Home/` and the anonymous exception problem

A login application necessarily needs at least one anonymous entry point. MVC supports this model by letting a controller-level `[Authorize]` restriction coexist with an explicit anonymous action [9]. **INFERENCE:** if MUJ uses a `Home` controller for sign-in and post-login landing functions, a narrow exception for the sign-in action is normal. The failure case would be an exception attached too broadly, or a second action that was assumed protected because it was not linked from the page.

The decision is to make anonymous access a positive manifest, not the absence of an attribute. A build should fail when a new routable action lacks an explicit classification. The expected outcome is that adding a new action cannot silently make it public. This also makes security review easier because the anonymous surface is a short, reviewable table.

### Case study B: `/Student/` and object ownership

Suppose an authenticated student action receives a record identifier. Conventional MVC routing can place the third segment into `id` [11], while OWASP warns that a user-supplied reference becomes IDOR when the application retrieves an object without sufficient authorization [4]. **INFERENCE:** checking only `User.Identity.IsAuthenticated` would establish that the caller is a student, not that the caller owns the requested record.

The design decision is to move ownership enforcement into the service or repository policy used by every controller and API path. In a synthetic staging fixture, Student A's principal must never obtain Student B's object through any route, query, body, export, or alternate handler. The expected outcome is consistent denial independent of how the identifier reaches the service.

### Case study C: `/Staff/` and least privilege

OWASP defines least privilege as assigning only the minimum privileges necessary and applying it horizontally and vertically [8]. **INFERENCE:** a broad `Staff` role could be insufficient if finance, examinations, admissions, and academic administration have different authorities. A centralized gate can still be too coarse even when it works exactly as coded.

The design decision is an action-by-permission matrix rather than one staff-wide authorization branch. Each high-impact operation should state its required permission and scope. The expected outcome is that a legitimate staff login cannot cross functional boundaries merely by reaching an unlinked controller action.

### Case study D: `/api/` and pipeline divergence

Classic Web API routing conventionally uses `api/{controller}/{id}` and selects actions partly by HTTP verb [13]. **INFERENCE:** if MUJ exposes this route family, reviewing only `System.Web.Mvc` controllers and filters would be incomplete. API actions can also expose the same object model as browser actions through a different route and serialization path.

The decision is to maintain separate MVC and API endpoint inventories that converge on the same service-layer policies. The expected outcome is policy parity: the same principal and object produce the same authorization decision whether invoked by a browser-facing controller or an authorized API client.

**Decision-ready insight:** `/Home/` is primarily an exception-management problem, `/Student/` an ownership problem, `/Staff/` a least-privilege problem, and `/api/` a pipeline-parity problem.

## 7. Authorized Validation Plan

This plan is deliberately non-operational against the public service. It assumes written authorization and preferably access to source code and a staging clone.

| Phase | Inputs | Defensive work | Pass criterion | Evidence retained |
|---|---|---|---|---|
| 1. Architecture inventory | Solution files, route registration, `FilterConfig`, Web API configuration, `web.config`, rewrite rules, handler mappings. | Enumerate all MVC controllers/actions, API controllers/actions, static roots, modules, handlers, and anonymous exceptions. | Every reachable endpoint has an owner and explicit access classification. | Versioned endpoint-policy manifest. |
| 2. Effective-policy analysis | Controller inheritance, attributes, global filters, custom authorization code, claims transformation. | Compute the effective policy for each action, including inherited and anonymous behavior. MVC authorization filters run before action filters [7]. | No endpoint relies only on menu visibility, naming convention, or raw-path prefix. | Machine-readable action-to-policy matrix. |
| 3. Canonicalization specification | Proxy rules, IIS Request Filtering, URL Rewrite, ASP.NET routes, filesystem rules. | Define accepted character set, decoding count, separator policy, Unicode form, case semantics, and canonical redirects. IIS can separately govern high-bit characters and double escaping [21]. | Every request is canonicalized once before dispatch, or rejected; no authorization decision precedes a later identity-changing normalization. | Canonicalization decision record and configuration snapshot. |
| 4. Generated route tests | Endpoint manifest and a safe equivalence-class generator. | In a local or staging environment, test approved representations and rejected ambiguity classes without using production accounts or data. | Equivalent requests select the same handler, endpoint, policy, principal, and resource; invalid forms fail uniformly. | Test logs with endpoint and handler telemetry. |
| 5. Object-authorization tests | Synthetic principals and disjoint synthetic records. | Verify horizontal and vertical isolation for every object-bearing action and API operation. OWASP requires validation on every request [8]. | No principal can access an object outside the fixture's explicit entitlement graph. | Automated policy-test report. |
| 6. Static/dynamic parity review | Web root, deployment package, upload paths, export jobs, temporary directories. | Confirm protected data is outside static roots and cannot be served by an alternate handler. | Static inventory contains only intentionally public content. | Deployment artifact scan and handler map. |
| 7. Logging and response review | IIS logs, application authorization events, identity logs. | Correlate selected endpoint, policy outcome, principal identifier, request ID, and IIS substatus without logging secrets. IIS documents distinct request-filtering substatus codes such as 404.5, 404.6, 404.7, 404.8, 404.11, 404.12, 404.14, and 404.15 [15]. | Security staff can distinguish routing misses, filter rejections, authentication failures, and authorization denials. | Redacted event examples and alert rules. |
| 8. Regression gate | CI pipeline and deployment review. | Fail builds for unclassified actions, policy drift, protected files under web root, or canonicalization-test failures. OWASP recommends automated unit and integration testing of access-control logic [8]. | A new route cannot ship without policy and tests. | CI attestation linked to release. |

The plan should start with source and configuration, not black-box production traffic. That produces higher confidence with less risk to student accounts, lockout controls, privacy, and service availability. If black-box validation is required, MUJ should define the exact scope, test window, synthetic accounts, source addresses, stop conditions, data-handling rules, and incident contact in writing.

**Decision-ready insight:** A generated endpoint-policy manifest turns an open-ended bypass hunt into a finite assurance problem that can be repeated on every release.

## 8. Remediation Priorities and Ownership

| Priority | Action | Owner | Why now | Acceptance measure |
|---|---|---|---|---|
| P0 | Establish global deny-by-default authorization for every dynamic pipeline; allow anonymous access only through an explicit manifest. | Application security and platform engineering | OWASP recommends deny by default and application-wide configuration [8]. | 100% of endpoints have explicit effective-policy classification. |
| P0 | Enforce object ownership and functional permission in a shared service layer. | Application engineering | Route identifiers are untrusted; IDOR results from insufficient authorization on user-supplied references [4]. | Cross-principal synthetic tests pass for every object type. |
| P0 | Remove protected documents, exports, caches, and uploads from public static roots. | Platform and application engineering | IIS static handling can occur outside MVC authorization; extensions and hidden segments have independent rules [21]. | Deployment scan finds no protected artifact in a public directory. |
| P1 | Publish and implement one canonicalization contract for URL paths and security identifiers. | Architecture and identity engineering | .NET normalization and ordinal comparison must be explicit for non-linguistic security tokens [10][5]. | Shared canonicalization library and equivalence tests cover every route family. |
| P1 | Review IIS Request Filtering, URL Rewrite, proxy rules, and handler mappings as one pipeline. | Infrastructure engineering | IIS can reject sequences, verbs, extensions, encodings, and high-bit characters before MVC [21][15]. | Version-controlled baseline with approved deviations. |
| P1 | Separate MVC and API endpoint inventories and make them consume the same authorization services. | Application engineering | MVC and Web API use different conventional dispatch models [11][13]. | Policy-parity tests pass across browser and API operations. |
| P2 | Improve denial telemetry and alerting using IIS substatus plus application policy events. | Security operations | Request Filtering exposes reason-specific substatus codes useful for analysis [12][15]. | Dashboards distinguish malformed traffic from authorization denials without user enumeration. |
| P2 | Add Unicode-confusable and identifier-collision review to account provisioning. | Identity engineering | Unicode equivalence and culture-sensitive comparisons can create inconsistent identity handling [10][5]. | Provisioning rejects canonical collisions and uses the documented case policy. |

**Decision-ready insight:** P0 work removes entire classes of bypass regardless of path syntax. P1 reduces parser disagreement, and P2 makes remaining anomalies detectable.

## 9. Synthesis

The eight requested patterns divide into three mechanisms. First, **coverage failures** occur when an action, API operation, or static handler lacks the intended policy. Direct action access, API-pipeline omission, and static-handler shadowing belong here. Second, **identity failures** occur when a route or object identifier is accepted as proof of entitlement. Route-parameter manipulation and IDOR belong here. Third, **representation failures** occur when layers disagree about dots, slashes, backslashes, case, Unicode, encoding, or extensions.

| Dimension | Coverage failures | Identity failures | Representation failures |
|---|---|---|---|
| Security question | Did the request reach an effective policy? | Did the policy authorize this principal for this object and operation? | Did every layer interpret the same canonical request and resource? |
| Typical scope | Controller/action, API filter, static handler. | Route value, query, body field, object key, role scope. | Proxy, IIS, rewrite module, ASP.NET router, custom gate, filesystem. |
| Strongest control | Global deny-by-default plus explicit anonymous exceptions [8]. | Service-layer entitlement checks on every request [8][4]. | Early single canonicalization, restricted grammar, ordinal comparison [10][5]. |
| Main trade-off | Strict defaults can expose undocumented dependencies during rollout. | Fine-grained policies require a maintained entitlement model. | Aggressive normalization can create collisions; rejection is often safer. |
| MUJ route emphasis | `/Home/` exceptions, `/api/` filter parity, all static roots. | `/Student/` ownership and `/Staff/` functional scope. | All four supplied route families. |
| Evidence base | Strong framework and OWASP evidence; MUJ configuration absent. | Strong OWASP mechanism; MUJ object model absent. | Strong platform evidence; MUJ normalization behavior absent. |

The non-obvious tension is that a "centralized" gate can improve coverage while increasing representation risk if it centralizes the wrong abstraction. A global framework authorization filter makes new actions deny by default. A global custom routine that decides from the raw path may instead create one high-leverage parser mismatch. Centralization is therefore beneficial only when the policy binds to the resolved endpoint, authenticated principal, requested operation, and resolved object.

A second tension concerns normalization versus rejection. Normalizing every unusual representation may seem user-friendly, but each transformation can merge originally distinct inputs. Unicode compatibility normalization can collapse characters by design, and Windows path rules differ from generic URI text rules [10][14]. For security-sensitive paths, the safer choice is often to accept a narrow canonical grammar and reject alternate separators, terminal ambiguity, repeated encoding, or unexpected character classes before routing.

A third tension is between identity centralization and authorization decentralization. Microsoft 365 can centralize credential and MFA handling, as reflected in MUJ's Office 365 guidance [6], while SLCM still needs local decisions about student ownership, parent relationships, staff function, and object scope. Strong upstream authentication makes those local decisions more trustworthy; it does not replace them.

The resulting strategy is layered but not redundant. IIS Request Filtering rejects malformed or disallowed request classes. ASP.NET routing selects one endpoint. A global policy establishes an authenticated default. Endpoint policy enforces role or operation permission. The service layer enforces object entitlement. Static resources remain intentionally public or stay outside the web root. Telemetry records which layer rejected the request. If each layer has a clear invariant, parser diversity becomes manageable rather than mysterious.

**Decision-ready insight:** The club should frame the project as an authorization-invariant audit, not a hunt for clever path strings. That approach finds missing policies, object-level gaps, API divergence, and handler shadows while remaining safe and reproducible.

## 10. VERDICT

**Verdict: No publicly substantiated MUJ SLCM authentication bypass was identified.**

**Overall confidence: High** that the public evidence is insufficient to claim a vulnerability.

**Confidence in the defensive risk model: High.** Microsoft and OWASP documentation directly support the relevant mechanisms: controller/action authorization scope [9], route-driven dispatch [11][13], IIS request filtering [21], Windows path semantics [14], Unicode normalization and ordinal comparison [10][5], and per-request object authorization [4][8].

**Confidence that any individual pattern is exploitable on MUJ: Low to Very Low.** The report has no source code, route table, global-filter registration, custom authorization logic, rewrite rules, handler map, request-filtering configuration, or authorized test results. The `/Home/`, `/Student/`, `/Staff/`, and `/api/` mappings are therefore **INFERENCES ONLY**.

**Most important next decision:** obtain written authorization and source/configuration access, then produce a machine-readable inventory of every MVC action, Web API action, anonymous exception, static handler, and effective authorization policy. If that inventory shows global deny-by-default coverage, service-layer object authorization, canonicalization before policy evaluation, and no protected static resources, the requested path variants should not create an authorization bypass. If it shows path-prefix authorization, unclassified actions, API-filter gaps, or protected files under public roots, remediate those structural defects before any production-facing validation.

## References

1. *http://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf*. http://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf
2. *http://login.microsoftonline.com/getuserrealm.srf?login=probe@muj.manipal.edu&xml=1*. http://login.microsoftonline.com/getuserrealm.srf?login=probe@muj.manipal.edu&xml=1
3. *http://mujslcm.jaipur.manipal.edu/*. http://mujslcm.jaipur.manipal.edu/
4. *WSTG - Latest | OWASP Foundation*. http://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References
5. *Best Practices for Comparing Strings in .NET - .NET ...*. https://learn.microsoft.com/en-us/dotnet/standard/base-types/best-practices-strings
6. *http://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf*. http://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf
7. *Understanding Action Filters (C#) | Microsoft Learn*. https://learn.microsoft.com/en-us/aspnet/mvc/overview/older-versions-1/controllers-and-routing/understanding-action-filters-cs
8. *Authorization - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
9. *AuthorizeAttribute Class (System.Web.Mvc) | Microsoft Learn*. https://learn.microsoft.com/en-us/previous-versions/aspnet/dd460317%28v%3Dvs.118%29
10. *http://learn.microsoft.com/en-us/dotnet/api/system.string.normalize?view=netframework-4.8.1*. http://learn.microsoft.com/en-us/dotnet/api/system.string.normalize?view=netframework-4.8.1
11. *ASP.NET MVC Routing Overview (C#) | Microsoft Learn*. https://learn.microsoft.com/en-us/aspnet/mvc/overview/older-versions-1/controllers-and-routing/asp-net-mvc-routing-overview-cs
12. *Deny URL Sequences &lt;denyUrlSequences&gt; | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/configuration/system.webserver/security/requestfiltering/denyurlsequences
13. *Routing in ASP.NET Web API | Microsoft Learn*. https://learn.microsoft.com/en-us/aspnet/web-api/overview/web-api-routing-and-actions/routing-in-aspnet-web-api
14. *Naming Files, Paths, and Namespaces - Win32 apps | Microsoft Learn*. https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file
15. *Configure Request Filtering in IIS | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/manage/configuring-security/configure-request-filtering-in-iis
16. *AuthorizeAttribute Class (System.Web.Mvc) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.mvc.authorizeattribute?view=aspnet-mvc-5.2
17. *Simple authorization in ASP.NET Core MVC | Microsoft Learn*. https://learn.microsoft.com/en-us/aspnet/core/mvc/security/authorization/simple?view=aspnetcore-10.0
18. *Host filtering with ASP.NET Core Kestrel web server | Microsoft Learn*. https://learn.microsoft.com/en-us/aspnet/core/fundamentals/servers/kestrel/host-filtering?view=aspnetcore-10.0
19. *Host filtering with ASP.NET Core Kestrel web server | Microsoft Learn*. https://learn.microsoft.com/ar-sa/aspnet/core/fundamentals/servers/kestrel/host-filtering?preserve-view=true&view=aspnetcore-10.0
20. *Policy-based authorization in ASP.NET Core | Microsoft Learn*. https://learn.microsoft.com/en-us/aspnet/core/security/authorization/policies?view=aspnetcore-10.0
21. *Request Filtering <requestFiltering> | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/configuration/system.webserver/security/requestfiltering
22. *ASVS/4.0/en/0x12-V4-Access-Control.md at master · OWASP/ASVS*. https://github.com/OWASP/ASVS/blob/master/4.0/en/0x12-V4-Access-Control.md
