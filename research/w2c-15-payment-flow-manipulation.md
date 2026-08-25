# MUJ Fee-Payment Assurance Without Live Exploitation

## Executive Summary

This report is a public-information, defensive assessment for a university security club. It does not claim that MUJ SLCM is vulnerable. It does not authorize testing, and it does not recommend modifying a live fee, order, callback, receipt, or refund. No login, payment, authenticated page, parameter change, receipt access, refund attempt, automated scan, or other interaction with the MUJ fee module was performed.

I cannot provide private internal chain-of-thought. Instead, the report supplies an auditable evidence-to-conclusion rationale: each finding separates observed evidence, explicitly labeled inference, defensive implication, and recommended action.

- **Evidence Boundary**: The public MUJ search result exposes institutional, parent, and student sign-in choices, but it does not establish which payment gateway or fee workflow is used [6] -> treat ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, Microsoft 365 identity, and any named gateway as input assumptions until MUJ supplies architecture and data-flow documentation.

- **Server-Authoritative Amounts**: Razorpay tells merchants to create an order before payment, pass the resulting order ID to checkout, and express the amount in the currency's smallest sub-unit [23] -> derive tuition, tax, scholarship, penalty, and currency from the university ledger on the server, never from browser-submitted totals.

- **Authenticated Completion**: Razorpay requires storage of the payment ID, order ID, and signature on the server and makes signature verification mandatory [23] -> a browser redirect must be treated as a user-experience signal, not proof that a fee is paid.

- **Asynchronous Reality**: Razorpay documents duplicate webhook delivery and warns that webhook events may arrive out of order [18] -> process callbacks idempotently and advance a fee only through valid state transitions, not merely because a callback was received.

- **Object Ownership**: OWASP defines IDOR as direct access to objects through user-supplied identifiers [5], while its authorization guidance calls for deny-by-default behavior and permission validation on every request [8] -> every receipt, order, fee demand, payment attempt, and refund must be checked against the authenticated student's permitted relationship to that object.

- **Refund Segregation**: Razorpay permits refunds only for captured payments; authorized payments that remain uncaptured are automatically refunded after three days [13] -> MUJ should require an original captured transaction, cumulative-refund limits, role separation, and independent approval before any financial reversal.

- **Incident Caution**: CBSE's June 5, 2026 press release says coordinated attacks on its post-result portal were mitigated with no breach or compromise of data [20], while subsequent reporting described unauthorized payment-system access involving about 50 students [24] -> preserve apparently conflicting accounts and avoid inferring a technical root cause that the public evidence does not establish.

- **Fraud Is Broader Than Parameter Tampering**: Published Indian cases include an alleged cloned university site that diverted INR 32,000 [29] and an alleged Gautam Buddha University scheme involving more than INR 5 crore and fake UPI entries in university software [30] -> combine application controls with domain monitoring, reconciliation, finance governance, and student communications.

- **Authorization Before Testing**: Section 43 of India's Information Technology Act addresses acts performed without the owner's permission, and Section 66 adds dishonest or fraudulent intent to covered acts [2] -> the club should perform mutation tests only under written authorization, in an approved staging environment and gateway sandbox, using university-issued synthetic accounts.

**Decision-ready insight:** The most consequential design rule is not a particular checksum algorithm. It is that the university ledger, gateway record, authenticated principal, and immutable order must agree before the ERP posts payment or exposes a receipt. The safest next step is a documented architecture review followed by sandbox-only testing, not exploration of the live MUJ portal.

## 1. Scope, Evidence, and MUJ Trust Boundaries

### 1.1 What is publicly established

The public MUJ SLCM result shows three access choices: `Sign In @muj.manipal.edu`, `Parent Login`, and `Student Login` [6]. That supports only a narrow conclusion: the landing page presents multiple authentication contexts. It does not publicly prove the framework version, web-server version, CDN behavior, identity protocol, gateway vendor, callback URL, fee API, database design, authorization model, or refund process.

| Architecture statement | Status in this report | Safe treatment |
|---|---:|---|
| `mujslcm.jaipur.manipal.edu` is the MUJ portal | Public search result supports the portal identity [6] | In scope only after MUJ confirms the exact host in writing |
| ASP.NET MVC 5.3 and .NET Framework 4.x | User-supplied assumption | Do not fingerprint or probe production; confirm from deployment inventory |
| IIS 10 behind Akamai | User-supplied assumption | Ask infrastructure owners for origin/CDN diagrams and log responsibilities |
| Microsoft 365 identity | User-supplied assumption | Confirm tenant, OIDC/SAML flow, parent identity model, and claims mapping |
| BillDesk, Razorpay, or CCAvenue | Research scenarios, not observed MUJ facts | Identify the actual acquirer/gateway from contracts and approved diagrams |
| Fee, receipt, and refund functions exist behind login | Plausible functional hypothesis | Verify from product owners; do not infer endpoints from naming conventions |

**Inference:** Multiple login choices may imply different principal types and relationships, but the public page does not show whether those roles share controllers, APIs, or object namespaces. The security review should therefore begin with a role-to-object matrix, not assumptions based on the labels.

### 1.2 The fee-payment trust model

A defensible design has at least seven distinct trust domains: identity, ERP fee ledger, internal order service, gateway, browser, callback/webhook receiver, and finance/refund operations. The browser is the least authoritative participant because a student controls its requests, history, storage, navigation, and return path. The gateway can authenticate its own messages, but it cannot decide which student ledger item should be cleared unless the university binds the gateway order to an immutable internal obligation.

| Trust domain | Authoritative for | Must not be authoritative for |
|---|---|---|
| Identity provider | Authenticated principal and approved claims | Fee amount or payment success |
| ERP fee ledger | Student obligation, concessions, penalties, currency | Gateway capture status without verification |
| Internal order service | One-time order binding and state machine | Student identity without session/claim validation |
| Payment gateway | Gateway order, payment, capture, refund, and settlement state | University receipt ownership |
| Browser/return page | Display and user navigation | Amount, currency, success, receipt owner, or refund approval |
| Webhook receiver | Authenticated event intake | Unconditional state transition |
| Finance operation | Reconciliation and approved exception handling | Unlogged direct database changes |

**Decision-ready insight:** Because the public footprint is insufficient to identify the actual implementation, the club should produce a data-flow diagram from university records before creating test cases. Any statement below about a gateway is a reference integration pattern, not a finding about MUJ.

## 2. Three Gateway Patterns Converge on One Rule

### 2.1 Razorpay: server order, signed completion, captured state

Razorpay's Java server-integration guide says an order should be created for every payment and the returned `order_id` passed to checkout [23]. It defines `amount` in the smallest currency sub-unit, describes `currency` as a three-character field, and permits an optional receipt identifier up to 40 characters [23]. After checkout, the merchant stores `razorpay_payment_id`, `razorpay_order_id`, and `razorpay_signature` on the server; signature verification is mandatory and uses an HMAC-SHA256 construction over the order and payment identifiers [23]. Razorpay also says service delivery should follow captured status, which can be tracked through its API or webhooks [23].

This produces a clear control sequence: create the amount-bearing order on the server, bind it to the student's ledger item, authenticate the completion evidence, retrieve authoritative status where appropriate, and post the fee only once.

Razorpay's webhook documentation adds two reliability constraints. The signature is an HMAC-SHA256 value over the raw request body, and the receiving system should not parse or transform that body before validation [18]. Duplicate events are expected and identifiable by `x-razorpay-event-id`; event ordering is not guaranteed [18]. These are not operational footnotes. A duplicate or late event can become a duplicate receipt, repeated posting, or invalid state rollback if the ERP lacks idempotency and monotonic state transitions.

### 2.2 BillDesk: authenticated API messages and merchant order identity

The public BillDesk page describes developer guides, sandbox examples, test cards, and an API playground [12]. A more detailed public integration guide published by Meta concerns BillDesk use with WhatsApp Business; it is illustrative and must not be assumed to describe MUJ. That guide says API clients select HMAC or JOSE authentication, with JOSE preferred, and describes those methods as encrypting or decrypting API requests and responses [15]. It includes a merchant-generated unique order ID, a two-decimal transaction amount, ISO currency, and a merchant return URL [15]. BillDesk posts a transaction object to that return URL [15], and the guide identifies success, pending, and failed authorization status codes [15].

**Inference:** A return object must still be matched to the university's internal order and expected amount. Cryptographic authenticity answers "did the expected gateway generate this message?" It does not by itself answer "does this payment clear this student's exact obligation?"

### 2.3 CCAvenue: encrypted request, merchant secret, unique order responsibility

CCAvenue's public Integration Document is Version 3.3 from November 2021 [7]. It identifies request fields including `merchant_id`, `order_id`, `currency`, `amount`, `redirect_url`, and `cancel_url [7]`. It states that the merchant configures an access code and working key, and that the transaction component encrypts order data before forwarding the request to CCAvenue [7]. Crucially, the document says `order_id` must be unique per request but that CCAvenue does not check that uniqueness [7]. That moves duplicate-order prevention into the merchant's control domain.

| Pattern | Integrity mechanism documented publicly | Merchant-side invariant | Important limitation |
|---|---|---|---|
| Razorpay | HMAC payment signature; HMAC webhook signature over raw body [23][18] | Server-created order, expected amount/currency, captured status, idempotent posting | Signed success still needs ledger binding |
| BillDesk | HMAC or JOSE in the cited WhatsApp-specific guide [15] | Unique merchant order, amount/currency match, valid status, return-to-order correlation | The guide is not comprehensive and is not evidence of MUJ's integration [15] |
| CCAvenue | Encrypted order request using merchant credentials [7] | Merchant-enforced unique order, immutable expected values, validated response | The cited 2021 document does not prove MUJ's current configuration |

**Decision-ready insight:** Vendor mechanics differ, but the acceptance rule should be gateway-neutral: `paid = authenticated gateway evidence + exact internal-order match + exact amount/currency match + valid forward state transition + one-time ledger posting`.

## 3. Abuse Cases: Mechanism, Impact, and Control Objective

The following are defensive abuse cases, not instructions for use against MUJ. Mutation tests belong only in an approved staging environment with synthetic data.

| Abuse case | Defensive model of the failure | Potential effect | Required control | Safe verification condition |
|---|---|---|---|---|
| Amount tampering | ERP trusts a browser-returned or client-submitted total instead of the server ledger | Underpayment clears a larger obligation | Compute amount server-side; bind it to an immutable internal and gateway order; compare exact units before posting | A synthetic mismatch is rejected and creates no paid ledger entry |
| Currency tampering | ERP compares only a numeric amount or permits the browser to choose currency | Unit mismatch or incorrect settlement | Store ISO currency with the order; compare amount and currency as one tuple | Test order remains unpaid on any mismatch |
| Order-reference forgery | A valid payment is attached to another student's order or a stale order | Cross-account credit, duplicate credit, or fee bypass | High-entropy gateway ID plus internal unique key; authenticated-principal and object relationship check; one-time state transition | Cross-account synthetic reference is denied without revealing another record |
| Return/callback forgery | Browser redirect or unauthenticated callback is treated as success | False paid status or receipt issuance | Validate vendor signature/checksum; retrieve gateway state where supported; never trust query-string success alone | Invalid or missing authentication leaves order pending/failed |
| Replay/duplicate callback | Valid event is processed more than once | Duplicate receipts, duplicate credits, inconsistent settlement | Idempotency key/event ID, unique database constraint, cached prior result, monotonic state machine | Second delivery returns the original result without a new posting |
| Out-of-order event | A delayed event overwrites a terminal state | Captured becomes pending, or refunded becomes paid | Explicit allowed transition table and event-time/version handling | Older event cannot regress a terminal state |
| Receipt IDOR | Receipt lookup checks only a user-controlled ID | Disclosure of names, fee amounts, identifiers, or payment references | Per-request object authorization; ownership/relationship query; minimum receipt data | Account A cannot retrieve Account B's synthetic receipt |
| Refund abuse | Refund endpoint accepts an arbitrary amount, payment ID, beneficiary, or repeated request | Financial loss and ledger-settlement mismatch | Captured-original requirement, cumulative limit, original rail, maker-checker approval, idempotency, audit log | Over-refund, duplicate refund, and unauthorized role all fail in sandbox |
| CSRF on state changes | Authenticated browser can be induced to submit a fee/refund action | Unintended order creation or administrative action | Framework anti-forgery validation, SameSite cookies, origin checks where appropriate, no state-changing GET | Missing or invalid anti-forgery proof fails without changing state |
| Concurrency/race | Two simultaneous confirmations or refunds pass separate pre-checks | Double posting or over-refund | Transactional lock/compare-and-swap, unique constraint, atomic cumulative-refund check | Concurrent sandbox requests produce one accepted transition |

OWASP's authorization guidance supports least privilege, deny by default, and permission validation on every request [8]. It also recommends relationship- or attribute-aware authorization where appropriate, rather than assuming a role alone settles access [8]. For university systems, this matters because a parent, student, finance operator, scholarship office, and support agent can all have legitimate but different relationships to the same fee record.

OWASP's business-logic guidance recommends accepting an idempotency key, storing it with the result, and returning the cached result on retries [4]. This must be reinforced by a database uniqueness rule. An application-only cache can fail during restarts or parallel processing.

**Inference:** Receipt IDs do not need to be sequential to be vulnerable. Random identifiers reduce guessability, but they do not replace authorization. Conversely, a sequential identifier is not automatically exploitable if every request is constrained by the authenticated principal's permitted object relationship.

**Decision-ready insight:** The best control is a single, server-side settlement function with strict invariants, called by both browser-return and webhook paths. Duplicating payment-posting logic across controllers creates disagreement and makes testing harder.

## 4. Indian Education Cases: What They Show and Do Not Show

Published reporting is uneven. Some reports describe observed effects or allegations without enough evidence to identify a checksum failure, IDOR, framework defect, or gateway compromise. The distinctions below are essential.

| Case | Publicly reported facts | Classification | What can defensibly be learned | What cannot be claimed |
|---|---|---|---|---|
| CBSE post-result portal, June 2026 | CBSE's press release says coordinated cyber attacks were mitigated and no data was breached or compromised [20]. Telegraph reporting described unauthorized payment-system access involving about 50 students [24]. | Portal attack with conflicting public characterization | Payment availability, monitoring, incident communications, and rapid restoration are part of fee security | The public evidence does not establish amount tampering, the gateway, exact vulnerability, or data exfiltration |
| Sai Nath University clone allegation | A report says a near-identical university site allegedly intercepted a student's INR 32,000 fee and that police were investigating [29]. | External cloned-site/payment-diversion fraud | Monitor lookalike domains; publish canonical payment URLs; verify payee identity; warn applicants | This is not evidence that the genuine university ERP was compromised |
| M.J.P. Rohilkhand University clone | Reporting described a clone website and fears of illegal collection of information concerning more than 10 lakh students [31]. | Brand impersonation and possible data collection | Domain protection and student-data minimization belong in the payment threat model | The excerpt does not prove that fees were diverted or that the official portal was breached |
| Gautam Buddha University fee case | Reporting described an FIR concerning alleged diversion of more than INR 5 crore in student fees and fake UPI transactions recorded in university software [30]. | Alleged insider/process and reconciliation fraud | Separate duties, reconcile gateway/bank/ledger records, and make financial edits tamper-evident | An FIR is an allegation, not a technical root-cause finding or final adjudication |

### Case study: CBSE and the danger of premature technical attribution

The CBSE material demonstrates why incident effects and root cause must be separated. The board's official release emphasizes coordinated attacks, continuous monitoring, mitigation, and no compromise of data [20]. Secondary reporting describes unauthorized access affecting the payment process [24]. Both can potentially be true if attackers disrupted payment behavior without extracting protected data, but that is an inference, not a confirmed reconstruction.

For MUJ, the implication is operational: design logs so an incident team can correlate identity, internal order, gateway order, amount/currency, callback authentication result, gateway status query, ledger transition, receipt issuance, and refund decision. Without that chain, public communication will be forced to rely on symptoms.

### Case study: cloned portals move the boundary outside the ERP

The Sai Nath and Rohilkhand reports show that a secure payment controller cannot stop every fee fraud. Applicants may reach a counterfeit domain before touching the genuine system [29][31]. MUJ should therefore publish one canonical payment route, use consistent payee descriptors, monitor certificate transparency and lookalike registrations, and teach students never to pay through links received from unverified contacts.

**Decision-ready insight:** No cited Indian case proves that MUJ has any flaw. The cases justify controls and test hypotheses; they are not evidence for a finding against the target.

## 5. Authorization-Gated, Non-Destructive Test Plan

### 5.1 Mandatory preconditions

Testing should not begin until the university security owner signs a rules-of-engagement document. Section 43 of the Information Technology Act concerns specified actions performed without the owner's permission, while Section 66 applies when covered acts are done dishonestly or fraudulently [2]. This report is not legal advice, but those permission and intent boundaries make informal approval inadequate.

| Authorization field | Minimum written content |
|---|---|
| Assets | Exact staging hostnames, APIs, callback receiver, gateway sandbox merchant, and excluded production systems |
| Identities | University-issued synthetic student, parent, finance, approver, and support accounts |
| Data | Synthetic student IDs, fee demands, orders, receipts, and refunds; no real student records |
| Financial constraint | Sandbox instruments only; no production payment, capture, settlement, or refund |
| Time and rate | Approved window, low request ceiling, no stress/load testing, and no automation beyond named cases |
| Methods | Specific tests approved below; no endpoint discovery outside supplied documentation |
| Observability | Named log owners for identity, ERP, database, gateway, CDN, and finance records |
| Stop conditions | Any production redirect, real payment instrument, real-person data, instability, unexpected third-party system, or scope ambiguity |
| Communications | Live contact, incident escalation path, evidence encryption, retention period, and report recipient |
| Disclosure | University approval before sharing; coordinated reporting to the affected vendor when applicable |

### 5.2 Phased test matrix

| Phase | Test objective | Approved method | Expected secure result | Evidence to retain |
|---|---|---|---|---|
| 0. Architecture review | Establish actual flow | Review source/configuration, contracts, sequence diagrams, controller routes, and gateway settings supplied by MUJ | One agreed diagram identifies every authoritative field and trust transition | Versioned diagram and owner sign-off |
| 1. Order creation | Prove server authority | In staging, create synthetic fee demands with known concession, tax, late-fee, and currency values | Server creates one immutable order from ledger values; browser values cannot redefine it | Internal order row, gateway sandbox order, correlation ID |
| 2. Amount mismatch | Test exact comparison | Alter only an approved synthetic staging request so its displayed/submitted amount differs from the ledger | Request is rejected or ignored; no payment posting or receipt occurs | Sanitized request/response, mismatch log, unchanged ledger |
| 3. Currency mismatch | Test tuple binding | Use a sandbox test case where order currency and returned currency deliberately differ | No ledger clearance; event is flagged for investigation | Expected/received tuple and state history |
| 4. Order binding | Test principal-object relation | With two university-issued synthetic accounts, attempt to associate Account A's sandbox payment with Account B's synthetic order | Denied without disclosing B's fee or receipt data | Authorization decision and audit event |
| 5. Browser return | Prove return is non-authoritative | Exercise the documented sandbox return path with missing, invalid, or stale authentication evidence | UI may show an error/pending state; ledger never becomes paid | Signature result, gateway query result, transition log |
| 6. Webhook authenticity | Validate raw-body signature handling | Use gateway sandbox tooling or a university-owned callback fixture to send valid and invalid signed fixtures | Invalid event is rejected; valid event is accepted only once | Raw-body hash, key version, event ID, response code |
| 7. Duplicate and ordering | Test idempotency/state machine | Replay only university-created sandbox fixtures and submit an approved out-of-order sequence | Duplicate returns prior result; older event cannot regress terminal state | Event IDs, database constraint result, before/after states |
| 8. Receipt authorization | Test IDOR safely | Request only the two synthetic receipts supplied for the exercise, once from each account and role | Owner/authorized relation succeeds; unrelated account receives a generic denial | Access-decision logs; no real receipt content |
| 9. Refund limits | Test finance controls | On a captured sandbox payment, submit approved zero-risk cases for unauthorized role, duplicate refund, and cumulative amount above the original | All invalid cases fail atomically; valid case requires designated approval | Approver identities, original/cumulative amounts, idempotency key |
| 10. Concurrency | Test atomicity | Run a small, pre-agreed pair of simultaneous sandbox confirmations or refunds | Exactly one financial state change and one receipt/refund record | Transaction IDs, lock/constraint behavior |
| 11. Recovery | Verify reconciliation | Simulate an approved callback outage while the sandbox gateway reaches a terminal state | Scheduled reconciliation finds the discrepancy without double posting | Reconciliation report and corrective transition |
| 12. Negative-data review | Minimize exposure | Inspect authorized logs and receipts using synthetic data | No secret, full payment credential, unnecessary identity claim, or sensitive callback body is retained | Redacted sample logs and retention configuration |

### 5.3 Test oracles and severity

A test passes only when all relevant stores agree: internal order, gateway order/payment, ledger, receipt, and refund ledger. A correct HTTP status alone is insufficient. For example, an invalid callback that receives an error but has already inserted a paid row is a failure.

| Finding condition | Suggested severity | Immediate response |
|---|---:|---|
| Synthetic underpayment clears a larger fee | Critical | Stop testing, preserve evidence, disable affected posting path in staging, review production logs under incident authority |
| Unauthenticated callback creates paid state | Critical | Block callback processing until authentication and reconciliation controls are fixed |
| Cross-account synthetic receipt access | High, or Critical if payment/identity data is extensive | Correct object-level authorization and review access logs |
| Duplicate callback creates duplicate financial posting | High | Add atomic idempotency and reconcile all affected records |
| Unauthorized refund role or over-refund succeeds in sandbox | Critical | Disable refund function for that role and require maker-checker controls |
| UI-only price difference with server rejection | Informational | Correct misleading display, but do not report a payment-integrity failure |
| Verbose generic denial reveals a receipt exists | Low to Medium | Normalize errors and reduce metadata exposure |

**Decision-ready insight:** The plan never needs a real student's identifier, a production transaction, broad enumeration, or a live refund. If a control cannot be evaluated with synthetic accounts and sandbox events, redesign the test with the system owner rather than expanding access.

## 6. Remediation, Monitoring, and Coordinated Disclosure

### 6.1 Reference settlement state machine

| Current state | Permitted next states | Required evidence |
|---|---|---|
| `Demanded` | `OrderCreated`, `Cancelled` | Authenticated principal and server ledger calculation |
| `OrderCreated` | `Pending`, `Authorized`, `Failed`, `Expired` | Matching immutable internal/gateway order |
| `Pending` | `Authorized`, `Captured`, `Failed`, `Expired` | Authenticated gateway event or authoritative status retrieval |
| `Authorized` | `Captured`, `AutoRefunded`, `Failed` | Exact amount/currency and gateway state |
| `Captured` | `Posted`, `RefundPending`, `Disputed` | One-time posting transaction and reconciliation data |
| `Posted` | `RefundPending`, `Disputed` | Approved finance workflow; never a browser request alone |
| `RefundPending` | `PartRefunded`, `Refunded`, `RefundFailed` | Maker-checker approval, cumulative limit, gateway refund record |
| Terminal states | No backward transition without documented exception | Privileged, audited correction workflow |

Razorpay's own guidance distinguishes authorization from capture and recommends delivering service only after captured status [23]. Its refund API accepts refunds only for captured payments [13]. Those vendor states should map to separate ERP states rather than a single Boolean `Paid` flag.

### 6.2 Engineering controls

Use one server-side settlement service for return, webhook, reconciliation, and administrative retry paths. Require a unique internal order key, unique gateway order key, unique gateway payment key, and unique processed-event key. Make posting and receipt issuance part of one database transaction or an outbox-based workflow so one cannot succeed invisibly without the other.

For object authorization, enforce the authenticated relationship in the data query itself. OWASP recommends permission checks on every request and deny-by-default behavior [8]. A controller-level role check such as `Student` is insufficient when the real question is whether this student, parent, sponsor, or employee may access this particular receipt.

For callbacks, validate the vendor's cryptographic evidence before parsing business fields where the protocol requires raw-body validation. Razorpay explicitly says to validate the HMAC using the raw body and warns not to parse or cast it first [18]. Keep secrets in a managed vault, record key versions rather than secrets, rotate under a dual-secret transition procedure, and never place merchant keys in browser code.

### 6.3 Monitoring and reconciliation

| Signal | Detection objective | Response owner |
|---|---|---|
| Amount/currency mismatch | Attempted tampering or integration defect | Application security plus finance |
| Unknown or already-used order | Forgery, replay, or reconciliation fault | Payment engineering |
| Invalid callback signature | Spoofing, stale key, proxy/body transformation | Security operations |
| Repeated event ID | Expected retry versus application idempotency failure | Payment engineering |
| Cross-account receipt denial spike | Enumeration or broken client workflow | Security operations |
| Refund near or above original amount | Abuse or accounting defect | Finance controller |
| Manual database fee adjustment | Insider risk and control bypass | Internal audit |
| Gateway captured but ERP pending | Lost callback or processing failure | Reconciliation operations |
| ERP paid but no gateway capture/settlement | False posting or data corruption | Incident response plus finance |
| Lookalike MUJ payment domain | Phishing and fee diversion | Brand protection plus student affairs |

OWASP recommends security logging and testing authorization logic with unit and integration tests [8]. Logs should use correlation IDs and pseudonymous student keys, retain before/after states, and avoid full receipts or sensitive payment data. Alerts should be actionable: one invalid signature may be an integration error, while a distributed surge combined with unknown orders is materially different.

For disclosure, the university should acknowledge reports, preserve confidentiality, provide a secure evidence channel, coordinate with the gateway, and establish remediation timelines. CERT-In publishes a Responsible Vulnerability Disclosure and Coordination Policy describing its vulnerability-reporting process and handling of submitted information [10]. That policy does not grant permission to test a third-party system; authorization must come first.

**Decision-ready insight:** Application security and finance reconciliation are one control system. Neither can compensate for the absence of the other.

## 7. Synthesis: One Invariant Across Different Gateways

| Dimension | Razorpay reference | BillDesk reference | CCAvenue reference | MUJ control implication |
|---|---|---|---|---|
| Order origin | Server creates an order for each payment [23] | Merchant generates a unique order ID in the cited integration [15] | Merchant supplies `order_id` and must ensure uniqueness [7] | ERP must create and own the order before redirect |
| Amount representation | Smallest currency sub-unit [23] | Two-decimal amount in cited guide [15] | `amount` plus `currency` request fields [7] | Use vendor-specific formatting only at the adapter boundary; store a canonical internal money type |
| Message protection | HMAC payment and webhook signatures [23][18] | HMAC or JOSE in cited guide [15] | Merchant working key and encrypted request [7] | Adapter validates vendor evidence; core service receives a normalized verified event |
| Completion state | Capture is distinct from authorization [23] | Guide exposes success, pending, and failed statuses [15] | Public document defines transaction request and return parameters but does not prove MUJ handling | ERP needs an explicit state machine, not a Boolean |
| Duplicate responsibility | Duplicate and out-of-order webhooks are documented [18] | Not specified in the cited page | Merchant order uniqueness is expressly merchant-controlled [7] | Idempotency belongs in MUJ regardless of vendor behavior |
| Receipt authorization | Outside gateway scope | Outside gateway scope | Outside gateway scope | University alone must enforce receipt ownership and data minimization |
| Refund governance | Refund only captured payment [13] | Not specified in cited public guide | Not relied upon here | University must add role separation, cumulative limits, and reconciliation |

The non-obvious tension is that stronger cryptography does not automatically create stronger business integrity. A perfectly authenticated callback can still be applied to the wrong student's ledger item. Conversely, a correct object-authorization check cannot establish that funds were captured. The fee module needs both cryptographic message authenticity and relational business authorization.

A second tension is between availability and correctness. Automatically trusting the browser return can make payments appear immediate, but it creates a false-posting risk. Waiting indefinitely for one webhook avoids that mistake but can strand valid payments when callbacks fail. The balanced design records a pending state, authenticates asynchronous events, queries authoritative gateway state when appropriate, and runs reconciliation.

A third tension concerns identifiers. High-entropy receipt and order IDs reduce accidental discovery, yet only ownership checks prevent IDOR. Strict authorization without unique order constraints still permits duplicate financial processing. Identifier unpredictability, authorization, uniqueness, and idempotency solve different problems and must not be treated as substitutes.

### Evidence-to-conclusion rationale

| Observation | Mechanism | Implication | Recommendation |
|---|---|---|---|
| Vendor flows carry client-visible order and return data | Browser is outside the server trust boundary | Client values can be altered or replayed | Reconstruct expectations from the internal order and authenticate gateway evidence |
| Webhooks can duplicate and arrive out of order [18] | Delivery is at-least-once and asynchronous | Naive handlers can double-post or regress state | Use event uniqueness plus a monotonic state machine |
| IDOR arises from direct object access based on user input [5] | Identifier possession is mistaken for authorization | Receipts and payments can cross account boundaries | Enforce the principal-object relationship on every query |
| Indian reports include both portal incidents and cloned sites [20][29] | Threats operate inside and outside the ERP | Controller hardening alone is incomplete | Combine AppSec, monitoring, reconciliation, domain defense, and student education |
| Refunds move real funds after original payment | A privileged second transaction extends the attack surface | Weak role or amount controls can create direct loss | Use original-transaction binding, maker-checker approval, cumulative limits, and audit |

**Decision-ready insight:** MUJ should commission an architecture-and-code review before any dynamic assessment. Once the actual gateway and flow are confirmed, the club can instantiate the sandbox matrix without touching live students or funds.

## VERDICT

**Verdict:** There is **no evidence in the cited public material that MUJ SLCM is vulnerable to fee manipulation, receipt IDOR, callback forgery, or refund abuse**. The named stack and infrastructure are user-supplied assumptions; the only publicly supported target fact used here is the existence of institutional, parent, and student sign-in choices [6].

**Risk verdict:** Fee-payment integrity is inherently high impact. The highest-priority hypotheses are server-side amount/currency authority, authenticated and reconciled completion, one-time order posting, per-object receipt authorization, and tightly governed refunds. Published Indian cases justify those hypotheses but do not prove an MUJ defect.

**Recommended decision:** Approve only a written-scope, staging-only assessment with synthetic identities and a gateway sandbox. Do not test production returns, receipts, orders, callbacks, or refunds. Stop immediately if a test encounters real data, a production gateway, or an unlisted system.

**Confidence:**

| Conclusion | Confidence | Basis |
|---|---:|---|
| General gateway/control model | High | Primary vendor documentation plus OWASP guidance |
| Indian incident descriptions | Medium | Official CBSE statement plus qualified secondary reports; technical root causes remain incomplete |
| MUJ-specific architecture | Low | Most architecture details came from the prompt and were not independently established |
| MUJ-specific vulnerability status | Not assessed | No authorized dynamic testing, authenticated access, source review, or configuration review was performed |

## References

1. *Transaction Authorization - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html
2. [[PDF] Information Technology Act, 2000 - India Code](https://www.indiacode.nic.in/bitstream/123456789/13116/1/it_act_2000_updated.pdf)
3. *Bs Viewcontent*. https://www.rbi.org.in/Scripts/bs_viewcontent.aspx?Id=4236
4. *Business Logic Security Cheat Sheet*. https://cheatsheetseries.owasp.org/cheatsheets/Business_Logic_Security_Cheat_Sheet.html
5. *Testing for Insecure Direct Object References (IDOR)*. https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References
6. *muj portal - Manipal University*. https://mujslcm.jaipur.manipal.edu/
7. *CCAvenue Integration Document*. https://links.avenues.info/downloads/CCAvenue_Integration_Ver_3_3.pdf
8. *Authorization - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
9. *Indian - Computer Emergency Response Team*. http://cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf
10. *RVDCP*. https://www.cert-in.org.in/RVDCP.jsp
11. *India Code: Section Details*. https://www.indiacode.nic.in/show-data?actid=AC_CEN_45_76_00001_200021_1517807324077&orderno=48
12. *BillDesk*. https://docs.billdesk.io/
13. *Razorpay Docs*. https://razorpay.com/docs/api/refunds/
14. *ValidateAntiForgeryTokenAttribute Class (System.Web.Mvc) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.mvc.validateantiforgerytokenattribute?view=aspnet-mvc-5.2
15. *BillDesk Payment Gateway Integration Guide*. https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/upi-intent/pg-guide-billdesk
16. *AuthorizeAttribute Class (System.Web.Mvc) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.mvc.authorizeattribute?view=aspnet-mvc-5.2
17. *Razorpay Docs*. https://razorpay.com/docs/api/orders/create/
18. *Validate and Test Webhooks | Razorpay Curlec Docs*. https://razorpay.com/docs/webhooks/validate-test/
19. *Microsoft identity platform and OAuth 2.0 authorization code flow - Microsoft identity platform | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow
20. *5 0 .06.2026 PRESS RELEASE CBSE Lodges Complaint with Delhi Police over Coordinated Cyber Attacks on Post-Result Services Portal; 24X7*. https://www.cbse.gov.in/cbsenew/documents/Press_Release_Complaint_PVR_05062026.pdf
21. *Webhooks | Best Practices | Razorpay Docs*. https://razorpay.com/docs/webhooks/best-practices/
22. *OpenID Connect (OIDC) on the Microsoft identity platform - Microsoft identity platform | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols-oidc
23. *Integration Steps | Java SDK | Razorpay Docs*. https://razorpay.com/docs/payments/server-integration/java/integration-steps/
24. *CBSE payment portal hacked by students | CBSE revaluation portal system hit by 'malicious attack of 50 students with unauthorised access' - Telegraph India*. https://www.telegraphindia.com/india/cbse-revaluation-portal-system-hit-by-malicious-attack-of-50-students-with-unauthorised-access/cid/2163149
25. *Cross-Site Request Forgery Prevention - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
26. *Inside the CBSE OSM Cyberattack │A Technical Breakdown of the June 2026 Incident*. https://cyberpeace.org/resources/blogs/inside-the-cbse-osm-cyberattack-a-technical-breakdown-of-the-june-2026-incident
27. *Notifications | Official Website of Reserve Bank of India *. https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=11822
28. *Reserve Bank of India*. https://www.rbi.org.in/commonperson/english/scripts/FAQs.aspx?Id=420
29. *How a Cloned University Portal Cheated a Student Out of Her Fees*. https://the420.in/sai-nath-university-fake-website-student-fraud-agra/
30. *FIR against ex-GBU registrar, accounts officer for Rs 5-crore ...*. https://timesofindia.indiatimes.com/city/noida/fir-against-ex-gbu-registrar-accounts-officer-for-rs-5-crore-fee-fraud/articleshow/130197794.cms
31. *Clone website of Rohilkhand Univ raises data theft fears for ...*. https://timesofindia.indiatimes.com/city/meerut/clone-website-of-rohilkhand-univ-raises-data-theft-fears-for-10l-students/articleshow/126207394.cms
