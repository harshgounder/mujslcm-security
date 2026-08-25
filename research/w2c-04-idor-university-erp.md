# Defensive IDOR Assurance Map for MUJ SLCM

## Executive Summary

- **Public Boundary, Not a Vulnerability Finding**: The public page establishes only that `mujslcm.jaipur.manipal.edu` presents a "WELCOME TO MUJ PORTAL" page with sign-in and parent-login options [13]. It does not establish the private route inventory, identifier format, or any IDOR. -> Treat this report as a defensive assessment plan, not an allegation about MUJ.

- **Authorization, Not Identifier Shape**: OWASP says object identifiers may be sequential integers, UUIDs, or generic strings, and every endpoint that accepts an object ID and acts on the object needs an object-level authorization check [3]. -> Make the decision from the authenticated subject, requested object, attempted action, and relevant relationship or context.

- **GUIDs Are Defense in Depth**: OWASP describes GUIDs and random identifiers as ways to make valid values difficult to guess, while separately requiring access checks for each object and every access attempt [1]. -> Replace enumerable IDs where practical, but never accept a GUID as proof of authority.

- **Parameterized Queries Do Not Solve IDOR**: CWE-639 gives an invoice example in which a parameterized SQL statement prevents injection but still returns another user's invoice because ownership is not checked [6]. -> Distinguish query safety from authorization safety in design reviews.

- **Six High-Value Object Families**: Marks, fee receipts, notifications, document downloads, timetables, and profile updates create different subject-object relationships. [Inference] Marks and profile changes emphasize integrity; receipts and documents emphasize confidentiality; notifications and timetables may mix individual, cohort, and public scope. -> Test each operation and relationship separately rather than applying one generic "logged-in user" rule.

- **Identity Is Only the First Gate**: Microsoft defines authorization as deciding what data an authenticated party may access and what it may do, while its identity platform uses OpenID Connect for authentication and OAuth 2.0 for authorization flows [4]. -> Even if Microsoft 365 identity is used, SLCM must still enforce local record ownership, delegation, course assignment, and administrative scope.

- **India-Linked Evidence Is Limited**: One public writeup reports that changing a numeric `userid` exposed another student's document or record [7], and its author publicly identifies as a Jamal Mohamed College cybersecurity student [14]. The target institution is not named. A second writeup reports exposed financial records in the author's college portal but omits the institution, country, identifier behavior, and remediation status [2]. -> Use these as mechanism case studies, not proof against MUJ or proof of a named Indian university breach.

- **Safe Validation Requires Synthetic Cross-Account Objects**: OWASP recommends at least two users with different owned objects, and additional privilege levels when relevant [10]. -> Execute the map only under written authorization, with institution-created test accounts and seeded non-production records; never enumerate live identifiers or inspect another real student's data.

- **Verdict in One Line**: IDOR/BOLA is a high-priority assurance theme for an SLCM-class portal, but the public evidence reviewed here does not prove that MUJ uses sequential IDs or has an object-authorization vulnerability.

## Scope, Evidence, and Safety Boundary

This report covers a defensive test design for an SLCM-class university portal. The public MUJ page proves the portal name and a parent-login option, but no more [13]. The six record families in the brief are therefore treated as **requested test hypotheses**, not as observed MUJ endpoints. No target-specific route names, payloads, credentials, private responses, or student records are included.

The technology description also requires separation between evidence and assumptions. Microsoft publishes a `Microsoft.AspNet.Mvc 5.3.0` package targeting .NET Framework 4.5 and compatible with that framework or higher [11]. That proves the package/version combination is technically real; it does not prove this portal deploys it. The assertions that MUJ uses MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 identity came from the research brief and were not independently established by the public material retrieved here.

| Scope element | Evidence status | What may safely be concluded | What must not be concluded |
|---|---|---|---|
| `mujslcm.jaipur.manipal.edu` | Publicly verified | It serves an MUJ-branded sign-in page [13]. | That any private function is vulnerable. |
| Parent role | Publicly verified at UI level | A parent-login choice is displayed [13]. | The underlying delegation model, permissions, or effectiveness of enforcement. |
| ASP.NET MVC 5.3 and .NET Framework 4.x | User-supplied target claim; package existence independently verified | MVC 5.3.0 is a real Microsoft package for .NET Framework 4.5 or higher [11]. | That the package is present on this host or reveals its patch state. |
| IIS 10, Akamai, Microsoft 365 | User-supplied target claims | They are useful architectural assumptions for planning defense reviews. | That passive search proved their deployment or configuration. |
| Marks, fees, notices, documents, timetable, profile routes | Requested test families | They define the minimum coverage of an authorized assessment. | That these functions exist at particular paths or use client-controlled IDs. |
| Public IDOR evidence against MUJ | Not found | No responsible conclusion of vulnerability can be made. | That absence of a public report proves the portal secure. |

I cannot provide private chain-of-thought. Instead, the following table gives an auditable evidence-to-conclusion rationale without exposing hidden deliberation.

| Observable evidence | Defensible interpretation | Decision for the club |
|---|---|---|
| OWASP defines IDOR as direct object access based on user-supplied input that permits authorization bypass [10]. | An ID in a request is a review trigger, not proof of a defect. | Inventory references first; test the server's authorization decision second. |
| OWASP requires checks on every object action [3]. | Authentication at login is insufficient. | Build tests around subject-object-action-context tuples. |
| GUIDs reduce guessing but remain object IDs [1][3]. | Entropy and authority are separate properties. | Require both opaque references and authorization where feasible. |
| The public MUJ page exposes no private record behavior [13]. | No live IDOR claim is supportable. | Keep all target testing inside a written authorization and synthetic-data plan. |

## Why Every Identifier Is an Authorization Decision

OWASP defines IDOR as an application providing direct access to objects based on user-supplied input; the resulting failure can expose database records or files [10]. CWE-639 describes the underlying weakness more precisely: a user-controlled key selects a record, but the authorization process does not verify that the authenticated user has sufficient entitlement to that data operation [6]. The result can be horizontal escalation between peer users or vertical escalation into more privileged functions [6].

The governing model should be written as **subject + object + action + context -> allow or deny**. The subject is not merely "authenticated"; it includes the institutional identity, role, active enrollment or employment, and delegated relationships. The object is not merely an integer; it includes ownership, student, cohort, course, semester, document classification, and workflow state. The action distinguishes list, read, download, create, edit, publish, acknowledge, and delete. Context can include an active parent delegation, assigned course, current term, or approved finance function.

OWASP recommends relationship-based access control and attribute-based access control for application development. ABAC decides from subject attributes, object attributes, environmental conditions, and policy; ReBAC decides from relationships between resources [12]. These models fit a university better than a flat role check. A faculty member may be allowed to read marks only for an assigned course and term; a parent may be allowed to view only records covered by an active student-parent link; a finance operator may view receipts but not marks.

The canonical failure is not "an ID was sequential." The failure is that the server accepted an object reference without proving the subject's relationship to the requested object and authority for the action. OWASP therefore says to use datasets the current user can access when looking up primary keys, and to verify permission every time access is attempted [1]. This is stronger than retrieving an unrestricted record and hiding fields in the browser.

| Failure class | Authorization question | Typical control error | Defensive requirement |
|---|---|---|---|
| Horizontal read | May Student A read Student B's object? | Controller checks login but not ownership. | Scope the data query to the authenticated student's permitted dataset. |
| Horizontal write | May one peer change another peer's object? | Update accepts a client-supplied owner or record key. | Resolve ownership server-side and allowlist editable fields. |
| Vertical access | May a student invoke a faculty, finance, or registrar operation? | Role is checked only in the menu or client. | Enforce role and object scope on the server for every request [12]. |
| Relationship bypass | May Parent A view Student B? | "Parent" role is accepted without validating the parent-student link. | Validate the active relationship for the exact student object. |
| Function/property mismatch | May an allowed reader access sensitive properties or perform an update? | Read permission is reused for export or edit. | Authorize each operation and each sensitive property; OWASP specifically requires validation of access to object properties [16]. |
| Static-file bypass | May a direct file URL bypass application policy? | Application protects the list page but storage serves the file directly. | Authorize before streaming or issuing a short-lived, subject-bound retrieval grant. |

**Decision-ready insight:** identifier discovery, role checking, and ownership checking are three separate layers. An assessment passes only when the application enforces all applicable layers server-side.

## India-Linked Education Portal Case Studies and Their Limits

### Case study 1: Numeric `userid` exposed another student's record

A public educational-portal writeup states that accessing one user's document and incrementing or decrementing a `{userid}` value revealed another student's record, confirming missing access control [7]. This is a direct illustration of the CWE-639 mechanism: a controllable key selected the record, while an ownership decision was absent. It is relevant to document downloads, profile records, receipts, or marks whenever a numeric student or record identifier reaches a data lookup.

The author publicly describes himself as a final-year B.Sc cybersecurity student at Jamal Mohamed College [14]. That makes the writeup **India-linked through the author**, but the retrieved article evidence does not name the affected institution or establish that Jamal Mohamed College was the target. It also does not provide independently corroborated remediation evidence in the retrievable material. Calling it a proven MUJ, Manipal, or named Indian-university vulnerability would exceed the evidence.

The defensive lesson is still concrete. A team should not "test neighboring numbers" on real data. It should seed Student A and Student B records in an approved environment, then confirm that Student A cannot retrieve Student B's known synthetic object reference. This reproduces the authorization question without enumeration, privacy harm, or ambiguity over consent.

### Case study 2: College portal exposed sensitive financial records

A second public writeup says the researcher encountered an IDOR in his college's internal portal that exposed sensitive financial records [2]. Fee receipts are a plausible SLCM-class analogue because they can combine student identity, amounts, payment references, dates, and institutional account information. The cited material, however, does not state the institution, country, identifier format, scope, or fix status [2].

This is therefore **an anonymized college-portal claim, not a proven Indian-university case**. Its value is as a failure pattern: finance data can be behind an authenticated page yet still lack per-receipt ownership checks. Its evidentiary limitations matter just as much as its mechanism. A security club should not fill those gaps by guessing the institution or searching live receipt identifiers.

### Case study 3: Disclosure infrastructure is not vulnerability evidence

The Indian Institute of Technology HackerOne page establishes that an IIT has a response policy for vulnerability disclosure [15]. The retrieved material does not establish a public IIT IDOR report [15]. This distinction is useful: a disclosure program is an appropriate reporting channel, but it is not evidence that a particular vulnerability exists.

| Case | Publicly supported fact | Institution attribution | Corroboration/remediation | Evidence grade | Appropriate use |
|---|---|---|---|---|---|
| Mohamed Afsar educational-portal writeup | Numeric `userid` change exposed another student's document/record [7]. | Target unnamed; author is affiliated with Jamal Mohamed College [14]. | No independently verified fix in retrieved evidence. | Medium for mechanism; low for target attribution. | Model synthetic cross-student document tests. |
| Vicky Rohith college-portal writeup | College portal exposed sensitive financial records [2]. | Institution and country unnamed. | Identifier and fix status not established [2]. | Low-to-medium for mechanism; low for attribution. | Prioritize receipt ownership and download controls. |
| IIT HackerOne page | A vulnerability-response policy exists [15]. | Named IIT program page. | No published IDOR case established [15]. | High for policy existence; none for IDOR. | Identify a legitimate reporting route, not a defect. |

**Decision-ready insight:** the public writeups support the risk model but do not satisfy a strict threshold for a named, corroborated Indian university IDOR case. The report preserves that negative result rather than fabricating one.

## Six-Object SLCM Authorization Test Map

The map below is for a staging or dedicated assessment tenant containing synthetic records. OWASP recommends identifying every place where user input references database rows, files, pages, or other objects [10], and comparing at least two users with distinct objects and privileges [10]. The map intentionally uses no MUJ route names or live identifiers.

| Test ID | Hypothesized object family | Actions to cover | Required authorization relationship | Safe synthetic test | Passing result | Provisional impact if absent |
|---|---|---|---|---|---|---|
| AUTHZ-MARK-01 | Marks or grade records | List, view detail, export, submit, edit, approve, publish | Student -> own published marks; parent -> explicitly linked student and permitted view; faculty -> assigned course/term; registrar -> delegated academic scope | Seed marks for Students A/B and assigned/unassigned Faculty F1/F2. Exercise each action with the exact pre-seeded non-owned record, never a guessed ID. | Non-owner receives the institution's uniform deny/not-found result; no grade data or metadata leaks; no state changes; decision is logged. | Confidentiality loss for reads; severe integrity impact for edit, approval, or publication. |
| AUTHZ-FEE-01 | Fee invoice or receipt | List, view, download, print, email copy, administrative correction | Student -> own finance object; parent -> active linked-student grant; finance -> assigned institutional scope | Seed two receipts with harmless values. Student A attempts only the known Student B synthetic reference under written authorization. | No receipt body, amount, payer detail, filename, or download URL is returned; no shared cache stores the personalized response. | Financial privacy exposure; integrity risk if correction or status actions are reachable. |
| AUTHZ-NOTICE-01 | Notification and attachment | List, read, acknowledge, dismiss, download attachment, create/publish | Recipient -> individual or eligible cohort; publisher -> authorized unit and audience | Seed one individual notice, one cohort notice, and one public notice. Test eligible and ineligible subjects against each classification. | Individual notices remain recipient-bound; cohort notices enforce cohort membership; public notices behave according to documented policy; write actions remain publisher-only. | Private-message exposure, unauthorized acknowledgement, or audience manipulation. |
| AUTHZ-DOC-01 | Student document | List, preview, download, upload replacement, verify, delete | Student -> own document where policy allows; verifier -> assigned workflow; parent -> only explicitly delegated classes | Seed harmless PDFs or text files for Students A/B and workflow states such as draft, submitted, verified, and expired. | Policy is enforced before content streaming; direct storage references do not bypass the application; unauthorized updates/deletes have no effect. | High confidentiality risk and potentially severe integrity or fraud risk. |
| AUTHZ-TIME-01 | Timetable or schedule | View personal, view cohort, export calendar, edit room/session | Student/faculty -> own or eligible cohort schedule; scheduler -> assigned department/campus | Seed schedules for two cohorts, departments, and terms. Define in advance which schedules are public, cohort-wide, or private. | Access matches the documented classification; an allowed view does not imply edit authority; stale-term or other-campus references are denied where policy requires. | Usually lower confidentiality impact than marks, but potentially important operational or safety impact for unauthorized edits. |
| AUTHZ-PROFILE-01 | Student profile | View, edit contact fields, upload photo, change sensitive identifiers, administrative update | Student -> own allowlisted fields; parent -> policy-defined read or delegated fields; staff -> role and purpose-limited scope | Seed profiles A/B. Test reads and each editable property separately, including fields that must remain registrar-controlled. | Non-owned profile is inaccessible; server ignores or rejects unauthorized properties; immutable identifiers and verification states cannot be changed by a student. | PII exposure, impersonation, account recovery abuse, or record-integrity damage. |

The matrix must be expanded across input locations because an object reference can appear in a path, query, form field, JSON body, hidden field, filename, or workflow state. OWASP advises avoiding identifiers in URLs and POST bodies where possible, deriving the current user from session information, and keeping multi-step identifiers in the session to reduce tampering [1]. These measures reduce exposure but do not replace authorization.

### Role and relationship matrix

| Synthetic subject | Marks | Fee receipts | Notifications | Documents | Timetable | Profile |
|---|---|---|---|---|---|---|
| Student A | Own published records only | Own objects only | Own, eligible cohort, public | Own policy-permitted documents | Own/eligible cohort | Own allowlisted fields |
| Student B | Same rules for B, never A by default | Same rules for B | Same rules for B | Same rules for B | Same rules for B/cohort | Same rules for B |
| Parent A | Linked Student A scope only | Linked Student A if policy grants it | Linked or family-directed notices only | Only delegated document classes | Policy-defined linked schedule | Policy-defined view/update only |
| Assigned faculty | Assigned course and term | None unless separately granted | Course or unit audience | Assigned workflow only | Assigned teaching schedule | Minimum necessary academic fields |
| Unassigned faculty | No access based solely on faculty status | None | Public or broad staff notices only | No unrelated workflow access | Policy-defined public/staff schedule | No unrelated student profile |
| Finance operator | No marks | Assigned finance scope | Finance notices if eligible | Finance-supporting documents only | None by default | Minimum billing identity fields |
| Registrar/administrator | Explicit delegated academic scope | Only if role includes finance | Authorized publishing scope | Defined verification scope | Defined scheduling scope | Defined administrative fields |
| Unauthenticated subject | Public resources only | None | Public notices only | None | Only schedules explicitly classified public | None |

[Inference] This is a recommended baseline, not MUJ's published policy. University owners must replace every cell with an approved rule and resolve ambiguous cases such as parental consent, adult-student privacy, cross-listed courses, alumni access, and staff acting in multiple roles.

**Decision-ready insight:** the same ID can be allowed for one operation and forbidden for another. A successful read test does not authorize update, export, publication, acknowledgement, or deletion.

## Sequential IDs, GUIDs, Signed References, and Parameterization

A sequential integer increases discoverability, but it is not itself an IDOR. OWASP explicitly includes sequential integers, UUIDs, and generic strings as possible object identifiers [3]. The vulnerability appears when the endpoint acts without checking that the logged-in user may perform that action on that object [3].

Likewise, "parameterized ID" is not the opposite of GUID. Parameterization describes how a value is transported or safely bound into a database statement; GUID describes an identifier's format and entropy. CWE's invoice example uses a parameterized SQL statement and still displays any requested invoice because it omits the authorization check [6].

| Reference design | Enumeration resistance | Authorization value | Advantages | Residual risk and rule |
|---|---|---|---|---|
| Sequential integer | Low | None by itself | Compact, efficient, easy to index and debug. | High discoverability; always scope lookup to the authorized dataset. |
| Random GUID/UUID | Usually high when generated correctly | None by itself | OWASP recommends random, unpredictable record IDs and describes GUIDs as difficult to guess [1][3]. | Leakage through logs, links, browser history, or another endpoint still enables replay; enforce object authorization. |
| Generic opaque string | Depends on generator | None by itself | Can avoid exposing database keys. | Predictable or reused strings may remain enumerable; validate authority every time. |
| Signed reference | High tamper detection when designed and managed correctly | Proves server issuance and integrity, not necessarily current authority | CWE notes a digital signature can help detect key tampering [6]. | Revocation, role changes, forwarding, expiry, and cross-user reuse still require policy checks. |
| Session-bound handle | High outside the session | Can reduce client control when correctly bound | OWASP recommends deriving the current user from session data and using session-held identifiers in multi-step flows [1]. | Session fixation, confused workflows, or server-side mapping errors remain possible. |
| Encrypted identifier | Variable | None by itself | Conceals the underlying value. | OWASP warns that encrypting identifiers can be challenging to do securely [1]; do not use it as the primary authorization control. |
| Composite business key | Often low | None by itself | May map naturally to term, student, or course. | Each component may create an authorization or mass-assignment surface; validate the resolved object and action. |

**Recommended design:** retain internal keys as needed, expose high-entropy references where practical, and make the decisive lookup equivalent to "find this object within the authenticated subject's permitted dataset." If the object is absent from that scoped dataset, do not fall back to an unrestricted lookup.

## ASP.NET MVC, Microsoft Identity, IIS, and Akamai Control Placement

### MVC and the application service

The official MVC documentation says `System.Web.Mvc.AuthorizeAttribute` restricts controller or action access to users meeting authorization requirements and can be configured with authorized users or roles [18]. It also provides an override point for custom authorization checks [18]. The documentation does not claim that the attribute automatically verifies ownership of a particular receipt, mark, profile, or document [18].

Microsoft's newer ASP.NET Core resource-authorization guidance illustrates the architectural reason: declarative authorization can run before the application loads the resource, so the application invokes authorization after obtaining the resource and evaluates a policy such as whether the document author matches the current user [8]. That page documents ASP.NET Core, not MVC 5, so its APIs should not be copied as though they were MVC 5 APIs. [Inference] The transferable principle is to centralize an explicit resource-authorization service and call it for every operation after securely resolving the relevant object or, preferably, to incorporate the scope directly into the repository query.

### Microsoft 365 identity

If the user-supplied Microsoft 365 assumption is correct, the identity provider establishes who authenticated and may supply roles or claims. Microsoft distinguishes that authentication function from authorization, which decides what data the party may access and what it may do [4]. The portal must still resolve institutional relationships that the identity provider may not know, including record ownership, parent delegation, assigned course, finance function, and active term.

### CSRF is complementary, not equivalent

ASP.NET MVC anti-forgery tokens address requests induced by a malicious site while a user is logged in. MVC sends a cookie token and form token, and the server rejects requests that do not return both [5]. The same guidance explains that the threat arises because the browser automatically includes the user's authentication cookie [5]. Anti-forgery checks protect state-changing requests from CSRF; they do not establish that the authenticated user owns the referenced object [5].

### IIS and Akamai assumptions

[Inference] If IIS 10 and Akamai are in the request path, they can contribute TLS termination, request filtering, rate limiting, coarse route controls, and telemetry. They generally cannot decide whether Parent A is linked to Student A or whether Faculty F1 is assigned to Course C without application-supplied policy context. OWASP's requirement remains that every endpoint receiving an object ID and acting on the object perform an object-level check [3].

[Inference] Personalized marks, receipts, profiles, and documents should not enter a shared edge cache unless the cache policy is explicitly private and keyed on the complete authorization context. A CDN cache hit must never bypass the application's object decision. This is a design requirement to validate with synthetic data, not a statement about MUJ's current Akamai configuration.

| Layer | Primary responsibility | Must enforce | Must not be mistaken for |
|---|---|---|---|
| Microsoft identity | Authenticate subject; provide validated identity/claims | Token validation, issuer/audience rules, session security | Record ownership or current university relationship |
| MVC controller/filter | Coarse authentication, role, and route policy | Deny unauthenticated or clearly unauthorized functions | Complete object-level authorization |
| Authorization service | Evaluate subject-object-action-context | Ownership, delegation, assignment, workflow state, field permission | Identifier entropy alone |
| Repository/data layer | Return only policy-permitted records | User/role/relationship-scoped query | An unrestricted lookup followed by UI hiding |
| File service | Authorize before preview/download | Object and storage-key binding, expiry for issued links | Secrecy of a filename |
| IIS/Akamai edge | Transport and perimeter controls | Valid requests, rate/abuse controls, safe caching, telemetry | Knowledge of private database relationships |
| Client/UI | Explain available actions | User experience only | A security boundary; OWASP says client-side checks must not decide access [12]. |

### Logging without creating a second data leak

OWASP recommends logging authorization failures, user privilege changes, and administrative actions [9]. It says application logs should capture enough "when, where, who and what" information for monitoring, including identity, event type, action, object, result, and reason [9]. The authorization event should use an internal correlation or pseudonymous object reference, not copy the sensitive record body.

OWASP also says session identifiers, access tokens, passwords, encryption keys, and payment-card or bank data should normally be removed, masked, hashed, sanitized, or encrypted rather than recorded directly [9]. Event data should be sanitized against log injection [9]. For this assessment, a pass requires both correct denial and a useful, privacy-preserving audit record.

## Authorized Test Protocol and Regression Gates

The following protocol is intentionally bounded. It is not permission to test the public MUJ service. The university must provide written scope, accounts, test windows, contacts, approved tools, data-handling rules, and a stop condition before any active validation.

| Phase | Authorized activity | Required evidence | Stop condition |
|---|---|---|---|
| 1. Policy definition | University owners define the role/relationship matrix and classify each object. | Approved policy table and named owner for every row. | Any ambiguous permission remains unresolved. |
| 2. Synthetic setup | Create Student A/B, Parent A/B, assigned/unassigned faculty, finance, and registrar accounts with harmless records. | Seed manifest listing synthetic object ownership and expected decisions. | Any account or record belongs to a real person. |
| 3. Reference inventory | Record object-reference locations from normal use of synthetic accounts. | Route/action/reference inventory without live identifiers. | A route is outside written scope. |
| 4. Positive baseline | Confirm each subject can perform only its expected action on its own seeded object. | Minimal request/response metadata and audit correlation ID. | Unexpected sensitive data appears. |
| 5. Negative cross-object test | Substitute only a pre-seeded synthetic non-owned reference; do not enumerate. | Denial response, no side effect, and application log. | First unexpected authorization success; preserve minimal evidence and stop that family. |
| 6. Vertical and relationship test | Exercise pre-approved role and delegation combinations. | Decision matrix across action and relationship state. | A real record, unapproved role, or out-of-scope function is encountered. |
| 7. Regression automation | Encode positive and negative tests in CI against a dedicated environment. | Repeatable results tied to policy requirements. | A deployment makes any authorization test fail. |
| 8. Disclosure and retest | Report through the institution's approved channel, then retest only the agreed fix. | Minimal redacted report, owner acknowledgment, closure evidence. | Scope changes or consent is withdrawn. |

OWASP recommends deny-by-default behavior and permission validation on every request, not merely most requests [12]. It also says automated unit and integration testing can reduce authorization flaws entering production [12]. OWASP API1 specifically recommends tests for the authorization mechanism and says not to deploy changes that make those tests fail [3].

| Regression gate | Required pass condition |
|---|---|
| Response confidentiality | Denied response contains no protected body, title, amount, student name, grade, filename, attachment metadata, or pre-signed retrieval link. |
| State integrity | Database row, workflow state, acknowledgement flag, file, or profile property remains unchanged after denial. |
| Operation isolation | Read permission does not silently grant export, update, approve, publish, delete, or administrative correction. |
| Relationship expiry | Revoked parent links, ended course assignments, expired terms, and removed staff duties take effect without stale authorization. |
| Property control | Profile and mark updates accept only server-approved fields; property access is validated [16]. |
| Alternate representation | HTML, JSON, export, print, attachment, mobile/API, and asynchronous variants enforce the same policy. |
| Error consistency | The selected 403/404 policy does not reveal protected object content or create a practical existence oracle. |
| Cache isolation | Personalized responses are not served across synthetic identities. |
| Auditability | Denial captures subject, action, protected-object correlation, result, reason, time, and request correlation without secrets or record contents [9]. |
| CI enforcement | Every policy row has at least one positive and one negative automated test, and a failed gate blocks release [3]. |

The evidence package should be deliberately small: test-case ID, synthetic subject, synthetic object label, expected rule, observed status, whether any state changed, and a correlation ID. Do not attach another person's record, retain live PII, publish route details before remediation, or continue after the first unambiguous synthetic proof.

**Decision-ready insight:** the safest convincing proof is one institution-seeded object crossing one institution-seeded authorization boundary. Enumeration adds harm, not evidentiary quality.

## Synthesis

The main controls differ across mechanism, scope, trade-off, evidence base, and time horizon. Identifier design reduces discovery probability. Identity establishes the subject. Application authorization decides the relationship and action. Repository scoping limits what data can be selected. Edge controls reduce abuse and improve visibility. Regression tests preserve those decisions across releases.

| Control strategy | Mechanism | Scope | Primary benefit | Principal trade-off or failure mode | Evidence basis | Time horizon |
|---|---|---|---|---|---|---|
| Sequential IDs plus scoped query | Easy identifier; strong server-side policy | Every object operation | Can be secure despite predictable IDs | A single unscoped lookup creates exposure | OWASP requires per-object checks [1]. | Immediate and continuous |
| GUIDs plus scoped query | High-entropy reference and policy | Every object operation | Reduces enumeration and preserves authorization | Teams may mistake entropy for authority | OWASP calls GUIDs defense in depth and still requires checks [1]. | Design and migration |
| Signed/session-bound references | Tamper detection or reduced client control | Selected workflows and downloads | Useful additional containment | Forwarding, stale authority, expiry, and key management | CWE and OWASP describe signatures/session mapping as supplementary measures [6][1]. | Workflow-specific |
| Microsoft identity | Authentication and claims | Session and coarse role | Strong subject identity when correctly configured | Does not know every local ownership/delegation fact | Microsoft distinguishes authentication and authorization [4]. | Session lifetime |
| MVC `AuthorizeAttribute` | Controller/action user or role restriction | Coarse function access | Central familiar gate | Documentation does not promise record ownership enforcement [18]. | Every request plus custom policy |
| Resource authorization | Subject-object-action evaluation | Exact record and operation | Directly addresses BOLA | Requires consistent invocation and policy data | Microsoft's document-author example illustrates resource checks [8]. | Every object action |
| IIS/Akamai controls | Perimeter filtering, rate control, telemetry, caching | Network/HTTP edge | Reduces abuse and supports monitoring | Cannot independently infer private institutional relationships [Inference] | OWASP still assigns the check to every object endpoint [3]. | Every request and incident |
| Automated policy tests | Positive and negative regression | Entire authorization matrix | Prevents reintroduction | Incomplete matrices create blind spots | OWASP recommends authorization unit/integration tests and release blocking [12][3]. | Every build and release |

Three non-obvious tensions follow.

First, the most visible property, identifier predictability, is not the decisive property. A sequential ID with a correctly scoped query can be safe, while a leaked GUID accepted without authorization can be unsafe. Therefore the club should report "missing object-level authorization," not merely "sequential IDs."

Second, stronger authentication can coexist with weak record authorization. Microsoft 365 may give high confidence in who the user is, while the application can still confuse which student's receipt, document, or marks that identity may access. Identity assurance raises the quality of the subject signal; it does not complete the policy decision.

Third, a generic role model is too coarse for a university. "Parent," "faculty," and "administrator" do not identify the linked student, assigned course, responsible department, active term, or permitted operation. ReBAC and ABAC fit these changing relationships better than menu visibility or a single role flag [12].

The holistic recommendation is therefore a layered design: authenticated identity; deny-by-default policy; relationship-aware object authorization; scoped repository queries; high-entropy external references as defense in depth; protected file delivery; non-shared caching for personalized data; privacy-preserving audit logs; and a synthetic positive/negative matrix enforced in CI.

## VERDICT

**Verdict:** IDOR/BOLA should be treated as a **high-priority defensive assurance area** for the described SLCM-class ecosystem. The public MUJ page shows separate sign-in and parent-login presentation [13], which makes cross-subject and delegated-relationship testing relevant. OWASP and CWE establish that any endpoint accepting an object reference can fail when it does not authorize the exact action on the exact object [6][3].

**No vulnerability finding:** This research found no public evidence proving that MUJ's marks, receipts, notifications, documents, timetable, or profile functions use sequential IDs, accept foreign object references, or omit authorization. It also did not independently verify the supplied IIS, Akamai, Microsoft 365, or exact application-version deployment claims. The report must not be represented as a MUJ penetration-test result.

**Confidence levels:**

| Conclusion | Confidence | Basis |
|---|---|---|
| The IDOR/BOLA model and recommended server-side controls are correct. | High | OWASP, CWE, and Microsoft primary guidance [6][1][3][8]. |
| The six-object test map is appropriate for an SLCM-class student portal if those functions exist. | High for methodology; medium for MUJ applicability | The object families came from the brief, while WSTG supports mapping rows, files, and functions across two or more synthetic users [10]. |
| The public portal exposes a parent-login option. | High | Direct public-page evidence [13]. |
| The described backend stack is deployed exactly as stated. | Low from this research | MVC 5.3.0 package existence is verified [11], but target deployment is not. |
| MUJ currently has an IDOR vulnerability. | Unsupported | No public proof was found; no authorized live test was conducted. |
| Public writeups prove a named Indian university IDOR case. | Low/unsupported under a strict standard | The mechanisms are reported, but affected institutions are anonymized or country attribution is absent [7][2]. |

**Go-forward decision:** obtain written university authorization, convert the role and relationship tables into approved policy, provision synthetic accounts and objects, and execute one bounded positive/negative test per object-action relationship. If any synthetic cross-object request succeeds, stop that test family, preserve minimal evidence, notify the authorized contact, fix the centralized policy or scoped query, and add a release-blocking regression test. Never enumerate live identifiers or access a real student's data.

## References

1. *Insecure Direct Object Reference Prevention Cheat Sheet*. https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html
2. *How I Found an IDOR Vulnerability – A Responsible ... - Medium*. https://medium.com/%40vickyrohith70/how-i-found-an-idor-vulnerability-a-responsible-disclosure-story-def2885bbe0c
3. *API1:2023 Broken Object Level Authorization - OWASP API ...*. https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization
4. *Authentication vs. authorization - Microsoft identity platform | Microsoft Learn*. http://learn.microsoft.com/en-us/entra/identity-platform/authentication-vs-authorization
5. *Preventing Cross-Site Request Forgery (CSRF) Attacks in ASP.NET MVC | Microsoft Learn*. https://learn.microsoft.com/en-us/aspnet/web-api/overview/security/preventing-cross-site-request-forgery-csrf-attacks
6. [CWE -

    CWE-639: Authorization Bypass Through User-Controlled Key (4.20)
    ](https://cwe.mitre.org/data/definitions/639.html)
7. *IDOR Vulnerability Exposing Sensitive Student Information ...*. https://medium.com/%40itcsafsar/idor-vulnerability-exposing-sensitive-student-information-responsible-disclosure-b49694354c6e
8. *Resource-based authorization in ASP.NET Core | Microsoft Learn*. https://learn.microsoft.com/en-us/aspnet/core/security/authorization/resource-based?view=aspnetcore-10.0
9. *Logging - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
10. *WSTG - Latest | OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References
11. [
        NuGet Gallery
        | Microsoft.AspNet.Mvc 5.3.0
    ](https://www.nuget.org/packages/Microsoft.AspNet.Mvc/5.3.0)
12. *Authorization - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
13. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
14. *Mohamed Afsar J - Penetration Tester | SOC Analyst | IAM ...*. https://in.linkedin.com/in/itcsafsar
15. *Indian Institute of Technology | Response Policy*. https://hackerone.com/indian_institute_of_techn
16. *API3:2023 Broken Object Property Level Authorization*. https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization
17. *4 Access Control¶*. https://owasp-aasvs4.readthedocs.io/en/latest/V4.html
18. *AuthorizeAttribute Class (System.Web.Mvc) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.mvc.authorizeattribute?view=aspnet-mvc-5.2
