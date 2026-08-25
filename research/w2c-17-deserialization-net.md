# MUJ SLCM .NET Deserialization Risk Assessment

## Executive Summary

- **No Confirmed MUJ Deserialization Vulnerability**: The public MUJ portal exposes a landing page with sign-in and parent-login choices [22], but public evidence does not show that the application calls `BinaryFormatter.Deserialize`, accepts attacker-controlled serialized objects, serves a vulnerable WebForms page, or uses a disclosed `machineKey` -> treat this report as a risk-surface assessment and request an owner-authorized code and configuration review, not an external exploitation exercise.

- **MVC Does Not Prove BinaryFormatter Use**: Microsoft.AspNet.Mvc **5.3.0** is a real package that targets .NET Framework 4.5 or higher [15], but neither the MVC version nor a .NET response banner establishes that application code invokes an unsafe formatter -> locate actual deserialization call sites and trace their input sources before assigning a vulnerability.

- **BinaryFormatter Is Unsafe by Design**: Microsoft says `BinaryFormatter` is dangerous, applications should stop using it, and it cannot be made secure [7]. Its unsafe deserialization can cause denial of service, information disclosure, or remote code execution in the application process [7] -> remove it rather than relying on a binder, edge firewall, or authentication requirement.

- **ViewState Applies to WebForms Remnants, Not MVC by Association**: Microsoft describes ViewState as information round-tripped by WebForms `.aspx` pages [9], while `LosFormatter` serializes WebForms ViewState [3]. Therefore, an MVC application is relevant to ViewState only if it contains, routes to, embeds, or shares configuration with WebForms pages -> inventory `.aspx`, master-page, and `PageStatePersister` artifacts in the authorized source tree and deployment manifest.

- **MAC Integrity Is the Primary ViewState Gate**: ASP.NET attaches a message authentication code to `__VIEWSTATE`, validates it on postback, and rejects a request without a valid MAC [9]. Microsoft subsequently made ViewState MAC enforcement non-disableable through the security update described in advisory 2905247 [17] -> confirm the update and compatibility configuration rather than attempting to submit test payloads to a university system.

- **machineKey Disclosure Can Be Critical**: Microsoft observed limited activity in December 2024 in which a publicly available static ASP.NET machine key was used to inject malicious code [10]; the resulting code executed in the IIS worker process and provided remote-code-execution capability [10] -> search authorized repositories and secret-management records for copied or reused keys, rotate exposed values, and protect the configuration at rest.

- **ysoserial.net Is Capability Evidence, Not Target Evidence**: The project supports `BinaryFormatter` and `LosFormatter` [4] and includes `ObjectStateFormatter` support in its formatter mappings [4], but its own documentation says the vulnerability lies in the application performing unsafe deserialization, not merely in the presence of gadget-capable libraries [4] -> do not interpret tool support as proof that MUJ SLCM is exploitable.

- **The Observed 4.7.4136.0 String Is Not a Patch Inventory**: Microsoft directs administrators to determine .NET Framework 4.5 and later through the registry `Release` value under `HKLM\SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full` [13], and warns against using the executing runtime version as a substitute [13] -> classify `4.7.4136.0` as an unverified fingerprint until the system owner correlates it with the OS, registry release, installed cumulative updates, and relevant file versions.

- **Akamai Is Compensating Control, Not a Serializer Fix**: Akamai describes App and API Protector as a WAF with Layer 7 DDoS, API, sensitive-data, and bot controls [20]. **Inference:** a WAF can reduce or detect suspicious traffic, but it cannot make an origin call to an unsafe deserializer safe -> fix the application and key-management root causes even if Akamai is confirmed in the request path.

## Scope, Evidence Standard, and Safety Boundary

This assessment uses only public documentation, the publicly visible MUJ portal landing page, and the technology observations supplied in the commissioning brief. It did not log in, submit crafted state, enumerate hidden routes, attempt key recovery, generate a deserialization payload, or interact with any student, parent, staff, or Microsoft 365 account. Nothing in this report authorizes testing of `mujslcm.jaipur.manipal.edu`, `sis.manipal.edu`, or any related Manipal system.

The commissioning brief supplies the following working observations: ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10 behind Akamai, Microsoft 365 identity, and an observed ASP.NET value of `4.7.4136.0`. Except for the existence of the MVC 5.3.0 package and the public portal content, those observations were not independently verified here. They remain hypotheses for the system owner to validate.

The requested explicit chain-of-thought is replaced with an auditable evidence-to-verdict method. This gives the club the relevant decision criteria without presenting hidden internal reasoning or operational attack steps:

| Decision stage | Question | Evidence needed | Present result |
|---|---|---|---|
| Technology | Is the component present? | Package manifest, deployed assemblies, registry release, IIS configuration | MVC 5.3 and `4.7.4136.0` are supplied observations; public portal alone does not prove the full stack |
| Reachability | Can untrusted data reach a deserializer? | Authorized data-flow review from HTTP, cookies, files, queues, caches, or databases to a sink | Not publicly established |
| Integrity gate | Does cryptographic validation occur before ViewState deserialization? | Effective WebForms and `machineKey` configuration, update state, and code path | Not publicly established; modern ASP.NET is designed to validate the MAC [9] |
| Gadget compatibility | Are dangerous types available to the relevant formatter? | Authorized dependency and runtime inventory | Not publicly established; ysoserial.net support alone is not target evidence [4] |
| Impact | What privilege would a successful path obtain? | Application-pool identity, network access, secrets, database rights, and isolation controls | Not publicly established |
| Verdict | Is exploitation demonstrated? | Reproducible owner-authorized evidence in an isolated environment | No |

**Decision-ready insight:** The principal unknown is not whether dangerous .NET formatter classes exist. They do. The unknown is whether MUJ SLCM exposes a reachable, attacker-influenced deserialization sink whose integrity controls or secrets fail. Public fingerprints cannot answer that question.

## Public MUJ Architecture: Facts, Inputs, and Inferences

The MUJ portal's extracted public content says "WELCOME TO MUJ PORTAL," presents a sign-in action, and shows a parent-login choice [22]. That establishes an externally reachable portal and multiple user journeys, but it does not establish how authentication is implemented behind the page or whether the same application handles every journey.

| Architecture item | Status in this report | What the evidence supports | Deserialization relevance |
|---|---|---|---|
| Public MUJ portal | Publicly verified | Landing page and sign-in/parent-login presentation [22] | Establishes exposure of a web entry point only |
| ASP.NET MVC 5.3 | Brief-supplied; package existence verified | Microsoft.AspNet.Mvc 5.3.0 exists and targets .NET Framework 4.5 or higher [15] | MVC does not itself demonstrate `BinaryFormatter` or ViewState use |
| .NET Framework 4.x | Brief-supplied | Compatible with the cited MVC package [15] | Retains legacy formatter APIs; actual use must be found in code |
| IIS 10 | Brief-supplied, not independently verified | No target-specific public proof obtained | Relevant to process identity, logging, application pools, and patching if confirmed |
| Akamai | Brief-supplied, not independently verified | Akamai's product category includes WAF and Layer 7 protections [20] | Compensating edge control; not proof that origin code is safe |
| Microsoft 365 identity | Brief-supplied, not independently verified | No target-specific federation metadata was used in this assessment | Authentication can narrow reachability but does not remove risk from authenticated or background processing paths |
| `4.7.4136.0` | Brief-supplied observation | No authoritative public mapping to MUJ's installed patch state was found | Useful as a lead, insufficient as a vulnerability or support finding |
| WebForms remnants | Scenario only | ViewState is a WebForms `.aspx` mechanism [9] | Relevant only if such pages are actually deployed or share keys/configuration |

**Inference:** If Akamai terminates the public connection while IIS hosts the origin, response characteristics can represent different layers. A header may describe an origin framework, an edge may add or suppress other headers, and authentication may redirect before application code runs. This layered design increases the importance of owner-side evidence: deployed binaries, effective configuration, registry release values, and request tracing.

**Inference:** Microsoft 365 sign-in, if confirmed, would reduce some anonymous application paths but would not protect a deserializer reached after authentication, through a parent flow, from a queued message, from a poisoned stored object, or through an internal service. Authentication and safe object deserialization are separate controls.

## BinaryFormatter Risk in an MVC 5.3 Application

### Why the formatter is dangerous

Microsoft's position is categorical: `BinaryFormatter` is dangerous, should not be used for data processing, and cannot be made secure [7]. `BinaryFormatter.Deserialize` is never safe with untrusted input [7]. Microsoft identifies possible consequences including denial of service, information disclosure, remote code execution, and code execution in the context of the target process [7].

The mechanism matters. A normal data parser maps data into a schema selected by the application. A polymorphic object deserializer can instead let serialized metadata influence the types created and the behavior triggered while reconstructing an object graph. Microsoft's code-analysis guidance describes the risk as unexpected types with malicious side effects and lists possible operating-system command execution, network communication, or file deletion [21].

A `SerializationBinder` is not a complete answer. Microsoft says the attack category cannot be mitigated by a `SerializationBinder` or another `BinaryFormatter` switch [7]. Its CA2300 guidance likewise says limiting types may mitigate known remote-code-execution attacks while leaving denial-of-service risk, and repeats that `BinaryFormatter` cannot be made secure [21].

### What would make MVC code reachable

| Potential application pattern | Required precondition | Risk if the precondition is met | MUJ status |
|---|---|---|---|
| Request body, form value, cookie, or header decoded and passed to `BinaryFormatter.Deserialize` | External user controls all or part of the byte stream | Potential process-context compromise, disclosure, or denial of service [7] | Unknown |
| Uploaded or imported file later deserialized | A user or upstream system can replace or poison the serialized object | Delayed execution when the application processes the object; Microsoft illustrates poisoned stored data as a trust-boundary problem [7] | Unknown |
| Session, cache, database, queue, or message-bus object deserialized | An attacker can write to or influence the backing store | Risk may move from the HTTP boundary to an internal or post-authentication boundary | Unknown; inference |
| Signed serialized data | Verification occurs before deserialization and signing key remains secret | Integrity may reduce tampering, but migration remains preferred because `BinaryFormatter` is not secure [21] | Unknown |
| Binder-constrained BinaryFormatter | Binder is correct and exhaustive | Known type abuse may be reduced, but denial of service and future bypass risk remain [7][21] | Still unacceptable as a long-term design |
| MVC package installed with no formatter call | No reachable sink | Package presence alone creates no demonstrated deserialization vulnerability | This is the current public-evidence position |

The authorized review should search source, compiled dependency inventories, and configuration for `BinaryFormatter`, `IFormatter`, `Deserialize`, `ISerializable`, `SerializationBinder`, `SoapFormatter`, `NetDataContractSerializer`, `LosFormatter`, and `ObjectStateFormatter`. This is a defensive source-review checklist, not a request to test the public portal.

Microsoft provides code-analysis rule CA2300, titled "Do not use insecure deserializer BinaryFormatter" [21], and recommends a secure serializer that does not let an attacker specify an arbitrary type [21]. The migration guide identifies `System.Text.Json`, `DataContractSerializer`, MessagePack, and protobuf-net as migration choices, depending on the required format and compatibility constraints [8].

| Migration need | Preferred direction | Security design condition |
|---|---|---|
| New JSON contracts | `System.Text.Json` [8] | Define explicit DTOs; do not deserialize arbitrary runtime types |
| XML interoperability | `DataContractSerializer` [8] | Use declared contracts and bounded object graphs |
| Compact binary format | MessagePack or protobuf-net [8] | Use explicit schemas/contracts and safe resolver configuration |
| Legacy data conversion | Isolated one-time migration process | Remove network access and production credentials; Microsoft advises separating potential gadget code from internet-connected code [16] |

**Decision-ready insight:** For MUJ, the first BinaryFormatter question is a repository and data-flow question, not a network-scanning question. If no sink exists, the risk is theoretical. If a sink exists but only processes strongly controlled local data, it still creates technical debt. If any untrusted party can influence the stream, Microsoft guidance supports treating removal as urgent.

## WebForms ViewState, MAC, and machineKey Failure Modes

### MVC and WebForms must not be conflated

ViewState is state round-tripped between WebForms `.aspx` pages [9]. `LosFormatter` is specifically documented as serializing the ViewState for a WebForms page [3]. Therefore, a page built only with the MVC pipeline is not proven to have a ViewState surface merely because it runs on `System.Web`.

**Inference:** The "sis.manipal.edu-style remnants" scenario becomes material if the authorized deployment inventory finds `.aspx` pages, WebForms controls, master pages, `PageStatePersister` subclasses, or older applications sharing a parent IIS site or common `machineKey`. Without that evidence, describing MUJ SLCM as ViewState-vulnerable would be speculation.

### What MAC validation does

On a WebForms page, the `__VIEWSTATE` field carries serialized page state. ASP.NET protects it with a MAC, validates the MAC on postback, and rejects a request that lacks a valid MAC [9]. The key used for that calculation comes from the application's `<machineKey>` configuration [9]. This is an integrity control: it decides whether the application should trust the returned state.

Microsoft advisory 2905247 addressed the condition in which ViewState MAC validation could be disabled. The update caused MAC validation to be enabled at all times and removed the server's ability to disable it [17]. Microsoft's later guidance says ASP.NET 4.5.2 behavior protects requests with encryption and a MAC, and that KB2905247 applied the updated behavior to earlier ASP.NET versions [14].

There is an important configuration nuance. The `ViewStateEncryptionMode` API documents `Auto`, `Always`, and `Never`; `Auto` encrypts when a control requests it, `Always` always encrypts, and `Never` does not encrypt even when requested [12]. The security blog's statement about ASP.NET 4.5.2 reflects the hardened compatibility behavior [14]. **Inference:** an owner should inspect effective `targetFramework`, `httpRuntime`, `machineKey compatibilityMode`, and installed updates rather than assuming behavior from an API default or banner alone.

### machineKey operations and failure modes

Microsoft explains that ViewState uses `ValidationKey` for the MAC and `DecryptionKey` for optional ViewState encryption [10]. In a web farm, all servers that generate and consume a page's state must use the same validation key and algorithm [9]. If servers generate local automatic keys independently, a postback reaching another node can fail validation [9]. That availability problem is not itself evidence that the MAC is bypassable; it shows that correct key management is necessary.

| Configuration state | Integrity outcome | Security or operational consequence | Priority |
|---|---|---|---|
| Unique secret key, modern MAC enforcement, controlled deployment | Forged state should fail validation [9] | Desired baseline | Maintain and monitor |
| Different automatic keys across farm nodes | Legitimate state from one node may fail on another [9] | Availability and troubleshooting problem | Fix farm configuration |
| Copied key from public documentation or repository | An outside party may know a trusted signing key | Potential malicious state acceptance; real abuse has been observed [10] | Critical rotation and incident review |
| Same key reused across unrelated applications | Compromise of one configuration may affect another application that trusts the same value | Larger blast radius | High; inference |
| Key stored in cleartext configuration with broad read access | Host or repository disclosure can expose signing material | Integrity boundary collapses if the key is stolen | High |
| ViewStateUserKey set per authenticated user | State is associated with an individual identifier and is harder to reuse across users [11] | Useful additional binding, not a substitute for MAC or secret keys | Defense in depth |

`ViewStateUserKey` must be assigned during `Page_Init`; setting it during `Page_Load` throws an exception [11]. That detail belongs in code review because a control configured too late may not provide the intended binding.

Microsoft advises never using a `machineKey` obtained from a key-generation website and says applications should use keys they generated themselves [9]. It also documents protected configuration as a way to encrypt the `<machineKey>` section if configuration files are disclosed [9]. Microsoft now recommends not copying public keys and regularly rotating keys [10].

### Case study: Microsoft's December 2024 machineKey incident

Microsoft Threat Intelligence observed limited activity in December 2024 involving one publicly disclosed static ASP.NET machine key [10]. Microsoft also identified more than **3,000** publicly disclosed keys that could potentially support this class of ViewState code-injection attack [10]. The qualifier matters: Microsoft described the observed activity as limited and one key as used in that activity, not 3,000 confirmed compromises.

The accepted malicious state caused code to be loaded and executed in the IIS worker process, providing remote-code-execution capability on the target server [10]. The lesson for MUJ is conditional but direct: if an application trusts a public or stolen key and exposes a compatible ViewState processing path, the cryptographic trust gate may accept attacker-created state. Conversely, finding a WebForms page without finding a key failure is not enough to assert this outcome.

**Decision-ready insight:** The most valuable defensive action is a secret-provenance review. A randomly generated, protected, application-unique key with modern MAC enforcement changes the analysis materially. A copied, leaked, or cross-application key demands urgent rotation and incident investigation.

## ObjectStateFormatter, LosFormatter, and ysoserial.net

Microsoft includes `LosFormatter` and `ObjectStateFormatter` in its BinaryFormatter-related security guidance [7]. `LosFormatter` serializes WebForms ViewState in a compact ASCII form [3], and Microsoft explicitly says it is insecure and cannot be made secure [3].

`ObjectStateFormatter` serializes and deserializes object graphs used for ViewState and control state; `PageStatePersister` and `LosFormatter` use it inside ASP.NET infrastructure [5]. A particularly important implementation detail is that it can fall back to `BinaryFormatter` for otherwise serializable types implementing `ISerializable` or carrying `SerializableAttribute` [5]. This is why reviewing only explicit `new BinaryFormatter()` statements can miss adjacent risk.

| Class or tool | Documented role | Security interpretation | What it proves about MUJ |
|---|---|---|---|
| `BinaryFormatter` | General .NET object graph serializer/deserializer | Unsafe with untrusted input and cannot be made secure [7] | Nothing without a reachable call site |
| `LosFormatter` | Compact WebForms ViewState serialization [3] | Microsoft says it cannot be made secure [3] | Relevant only if deployed code calls it or WebForms state reaches it |
| `ObjectStateFormatter` | ViewState/control-state graph formatting used by ASP.NET infrastructure [5] | May use `BinaryFormatter` for additional serializable types [5] | Relevant to actual WebForms/state-processing paths |
| `ysoserial.net` | Proof-of-concept collection for unsafe .NET object deserialization [4] | Demonstrates known formatter/gadget capabilities | Does not prove target reachability or key failure |
| MVC model binding | Application input mapping in MVC | Not equivalent to arbitrary object-graph deserialization | Must not be reported as BinaryFormatter risk without a sink |

The ysoserial.net repository lists `BinaryFormatter` and `LosFormatter` among supported formatters [4] and includes `ObjectStateFormatter` in formatter mappings [4]. Its own caveat is decisive: a chain requires an application with the relevant classes to unsafely deserialize the data, and the vulnerability is in unsafe deserialization rather than merely having gadget-capable classes installed [4].

For a university club, ysoserial.net should be treated as taxonomy and defensive-awareness material. This report intentionally omits command syntax, payload creation, gadget selection, signing parameters, and delivery procedures. Any practical validation belongs in a purpose-built local lab or a system-owner-approved clone using synthetic data and non-production keys.

**Decision-ready insight:** Formatter support establishes possibility, not exploitability. A defensible MUJ finding requires a complete chain: deployed WebForms or custom formatter path -> attacker-influenced data -> failed or compromised integrity gate -> compatible types -> meaningful process privileges.

## What ASP.NET 4.7.4136.0 Can and Cannot Prove

The supplied value `4.7.4136.0` is an observation, but no authoritative source obtained in this research maps it to MUJ's effective .NET release, Windows support state, or cumulative security-update level. Microsoft says the supported method for .NET Framework 4.5 and later is the registry `Release` value under `HKLM\SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full` [13]. Microsoft also says not to use `Environment.Version` for this determination because it describes the executing runtime rather than installed assembly or framework versions [13].

| Question | Can `4.7.4136.0` answer it? | Required owner evidence |
|---|---|---|
| Is some ASP.NET/.NET 4.x code executing? | It may support that hypothesis, depending on where the string came from | Capture source and header/assembly provenance |
| Is .NET Framework 4.7 or 4.7.2 installed? | No authoritative conclusion from this string alone | Registry `Release` DWORD [13] |
| Are current security updates installed? | No | OS build, installed cumulative updates, servicing records, and relevant file versions |
| Is the Windows version supported? | No | OS edition, release, and lifecycle status |
| Is BinaryFormatter reachable? | No | Source and data-flow review |
| Is ViewState MAC enforced? | No | Effective ASP.NET configuration and patch state |
| Is a `machineKey` exposed? | No | Secret-provenance, repository, deployment, and access-control review |
| Is MUJ exploitable? | No | Owner-authorized evidence for every precondition |

The lifecycle context reinforces this limitation. Microsoft defines .NET Framework 4.5.2 and later as a Windows component, so its support follows the underlying Windows lifecycle [2]. Microsoft lists .NET Framework **4.8.1** as the latest version and supports it while installed on a supported Windows release [2].

**Inference:** If `4.7.4136.0` accurately reflects an older runtime family, modernization deserves attention, but age is not equivalent to missing patches. Conversely, an old-looking banner must not be accepted as evidence that all applicable security updates are installed. Version family, OS lifecycle, cumulative servicing, and application configuration are distinct checks.

Information disclosure still has defensive significance. **Inference:** suppressing unnecessary framework-version headers reduces free reconnaissance value, but doing so neither upgrades the framework nor fixes unsafe deserialization. Header hardening is a low-cost hygiene item, not the core remediation.

**Decision-ready insight:** Record `4.7.4136.0` as a lead with high uncertainty. Do not assign a CVE, unsupported status, or deserialization severity from it. The next step is an authenticated administrator inventory, not more public probing.

## Owner-Authorized Assessment and Remediation Roadmap

| Priority | Owner-authorized action | Evidence or deliverable | Why it matters |
|---|---|---|---|
| P0 | Establish written scope and preserve production safety | Named systems, test window, contacts, prohibited actions, backup and rollback plan | Prevents student research from becoming unauthorized testing |
| P0 | Inventory deserialization sinks | Source/SAST report for `BinaryFormatter`, `LosFormatter`, `ObjectStateFormatter`, related interfaces, and indirect library use | Finds the actual risk surface; CA2300 identifies BinaryFormatter as insecure [21] |
| P0 | Trace trust boundaries into each sink | Data-flow map from HTTP, files, cookies, queues, caches, databases, and admin imports | Determines whether input is untrusted or can be poisoned |
| P0 | Review all `machineKey` values and provenance | Per-application key inventory without exposing values in tickets; repository-history and secret-scan results | Public or reused keys can collapse ViewState integrity [10] |
| P0 | Rotate exposed or copied keys | Coordinated deployment record and incident-review decision | Microsoft recommends avoiding public keys and rotating them [10] |
| P1 | Inventory WebForms remnants | Deployed `.aspx` list, master pages, `PageStatePersister` subclasses, and effective ViewState configuration | Separates the real ViewState surface from the MVC surface [9][5] |
| P1 | Verify installed framework and updates | Registry `Release`, OS version, cumulative-update inventory, file versions | A banner is not a patch inventory [13] |
| P1 | Replace BinaryFormatter-family sinks | Migration design using explicit contracts and safe serializers | Microsoft recommends removal and migration [7][8] |
| P1 | Validate farm configuration | Same intended algorithm and secret across nodes, application-unique key scope | Prevents validation failures while preserving integrity [9] |
| P1 | Protect configuration secrets | Least-privilege ACLs, protected configuration, secret scanning, rotation process | Microsoft documents protected configuration for `<machineKey>` secrecy [9] |
| P2 | Add focused detection | Alerts for repeated ViewState validation failures, abnormal state sizes, deserialization exceptions, and key-access events | Supports incident detection; inference-based monitoring recommendation |
| P2 | Enable appropriate IIS tracing in a controlled manner | Retention-limited trace policy with privacy review | IIS requires the tracing role service and site/application/directory enablement [19] |
| P2 | Tune Akamai as compensating control | Reviewed WAF policy and origin-only network restrictions | WAF can mitigate web threats but does not repair a deserializer [20] |
| P3 | Reduce fingerprint leakage | Remove unnecessary framework and server version disclosure after testing | Lowers passive reconnaissance value; inference |
| P3 | Modernize supported platform | Tested plan toward current supported Framework or application redesign | Reduces dependence on legacy APIs and configuration behavior |

### Safe validation sequence

1. **Code first.** Run approved static analysis and manual review on a controlled copy. Microsoft CA2300 says to use a secure serializer and prevent attackers from choosing arbitrary types [21]. Do not begin with crafted requests against the public site.

2. **Configuration second.** Export effective configuration through approved administration channels. Confirm MAC enforcement, `targetFramework`, compatibility mode, ViewState encryption policy, per-user binding, farm consistency, and secret storage. Never paste real keys into club notes, chat systems, screenshots, or public issue trackers.

3. **Patch and lifecycle third.** Collect the registry `Release` value, OS build, installed servicing updates, and relevant assembly versions. Compare them with Microsoft support records. Treat the response banner only as a correlation point.

4. **Isolated test fourth.** If a risky call site exists, reproduce it in an owner-controlled lab with synthetic data and non-production secrets. The success criterion should be safe evidence such as a rejected malformed object, a unit-test failure before migration, or confirmation that an unexpected type cannot be instantiated. No production payload delivery is needed.

5. **Production assurance last.** Deploy fixes through change control, rotate secrets where required, monitor errors, and verify that legitimate sign-in, parent, student, and administrative workflows remain available. **Inference:** key rotation can invalidate state generated with the previous key, so operational planning and communication are necessary.

### Detection without exploitation

IIS failed-request tracing is not enabled merely by installing IIS: Microsoft says the tracing role service must be installed and tracing then enabled at the relevant scope [19]. The configuration controls whether tracing is enabled, where logs are stored, and how many trace files are retained [19]. Use this only with a privacy and retention policy because portal traffic may contain student-related metadata.

At the application layer, log formatter type, call-site identifier, input source category, validation outcome, and exception class, but never log serialized blobs, authentication tokens, ViewState contents, or secret key material. At the edge, alert on repeated rejected state submissions and unusual request-size patterns. These are recommendations, not evidence of current malicious activity at MUJ.

**Decision-ready insight:** The roadmap prioritizes proof of reachability and key integrity before network testing. That produces a more accurate result, protects university users, and directly supports remediation.

## Synthesis

The principal technologies differ in mechanism, scope, and proof requirements. Treating them as one generic ".NET deserialization" issue would produce false positives.

| Dimension | BinaryFormatter in MVC code | WebForms ViewState | machineKey management | ysoserial.net | Framework/patch state | Akamai edge |
|---|---|---|---|---|---|---|
| Mechanism | Application reconstructs an object graph | ASP.NET round-trips page/control state | Keys authenticate and may encrypt state | Models known formatter/gadget capabilities | Determines available hardening and support baseline | Filters or observes HTTP traffic |
| Necessary proof | Reachable deserialization call and attacker influence | Deployed `.aspx`/state path | Leaked, copied, reused, weakly protected, or inconsistent key | Compatible target sink and classes | Registry release, OS, and servicing inventory | Confirmed routing and effective policy |
| Primary failure | Unsafe object creation | Untrusted state accepted or unsafe formatter reached | Forged state can pass trust gate | Tool capability mistaken for target vulnerability | Banner mistaken for patch status | Compensating control mistaken for a code fix |
| Evidence base here | Strong generic evidence, no MUJ call site | Strong generic evidence, no confirmed MUJ WebForms page | Strong generic and real incident evidence, no MUJ key evidence | Repository capability evidence only | Official inventory method, unresolved MUJ state | Product capability evidence, unverified MUJ deployment |
| Time horizon | Immediate removal if reachable | Immediate hardening if remnants exist | Immediate rotation if exposure is found | Lab and defensive taxonomy | Near-term inventory and modernization | Continuous tuning after origin fixes |
| Main trade-off | Compatibility versus eliminating unsafe design | Legacy page compatibility versus secure state handling | Farm availability versus key uniqueness and rotation | Research value versus misuse risk | Upgrade effort versus legacy support burden | Coverage versus false positives and bypass risk |

Three non-obvious tensions emerge.

First, older applications may have received the MAC-enforcement update while still retaining dangerous formatter APIs. Patch compliance therefore does not prove safe application design. Microsoft can enforce the ViewState MAC [17], yet custom `BinaryFormatter.Deserialize` calls remain unsafe [7].

Second, a correctly shared farm key improves availability but can increase blast radius if it is reused too broadly. The same key must be consistent across nodes serving one application [9], but **inference:** unrelated applications should not share it. Availability requires controlled sharing; containment requires narrow scope.

Third, an edge WAF and Microsoft 365 authentication can reduce exposure while leaving the root cause intact. **Inference:** they change who can reach a path and what traffic is detected, but they do not change the semantics of `BinaryFormatter`, `LosFormatter`, or `ObjectStateFormatter`. Origin code, keys, patch state, and process privileges remain decisive.

The holistic conclusion is therefore conditional: MUJ's supplied technology profile justifies a high-priority internal review, but the public record does not justify a public vulnerability claim. The correct analytical move is to convert hypotheses into owner-side evidence, starting with sink inventory and key provenance.

## VERDICT

**Verdict: PLAUSIBLE CONDITIONAL RISK, NO CONFIRMED MUJ DESERIALIZATION VULNERABILITY.**

| Verdict component | Assessment | Confidence |
|---|---|---|
| BinaryFormatter-family classes are dangerous with untrusted data | Confirmed by Microsoft [7] | High |
| ViewState is relevant to WebForms remnants and depends on MAC/key integrity | Confirmed generically [9] | High |
| Public/static machine keys can enable severe ViewState abuse | Confirmed by Microsoft's December 2024 case [10] | High |
| ysoserial.net supports the named formatter classes | Confirmed [4] | High |
| MVC 5.3 proves unsafe deserialization | Rejected; no such evidence | High |
| MUJ deploys a reachable WebForms remnant | Unknown | Low |
| MUJ uses BinaryFormatter on attacker-influenced data | Unknown | Low |
| MUJ's `machineKey` is exposed, copied, or reused | Unknown | Low |
| `4.7.4136.0` proves a missing patch | Rejected; registry and OS inventory are required [13] | High |
| Overall target-specific exploitability | Not established | Moderate confidence in the negative finding, because public evidence is necessarily limited |

**Overall confidence: MODERATE.** Confidence is high in the platform-level security conclusions and low in target-specific exploitability because the decisive artifacts are private: source code, effective Web.config, key provenance, deployed page inventory, registry release, OS updates, dependencies, and application-pool privileges.

The university security club should report this as a **responsible hardening hypothesis**: "The supplied legacy .NET profile warrants an owner-authorized audit for unsafe deserialization and ViewState key hygiene." It should not report "MUJ SLCM is vulnerable to ysoserial.net," "ViewState RCE is confirmed," or "4.7.4136.0 is unpatched." Those stronger statements are not supported by the public evidence.

## References

1. *MachineKey Class (System.Web.Security) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.security.machinekey?view=netframework-4.8.1
2. *.NET Framework official support policy | .NET*. https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-framework
3. *LosFormatter Class (System.Web.UI) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.ui.losformatter?view=netframework-4.8.1
4. *GitHub - pwntester/ysoserial.net: Deserialization payload generator for a variety of .NET formatters · GitHub*. https://github.com/pwntester/ysoserial.net
5. *ObjectStateFormatter Class (System.Web.UI) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.ui.objectstateformatter?view=netframework-4.8.1
6. *Insecure Deserialization | OWASP Foundation*. https://owasp.org/www-community/vulnerabilities/Insecure_Deserialization
7. *Deserialization risks in use of BinaryFormatter and related types - .NET | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/standard/serialization/binaryformatter-security-guide
8. *BinaryFormatter migration guide - .NET | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/standard/serialization/binaryformatter-migration-guide
9. *Resolving view state message authentication code (MAC) errors | Microsoft Support*. https://support.microsoft.com/en-US/servicing/DotNetFramework/troubleshooting/resolving-view-state-message-authentication-code-mac-errors
10. *Code injection attacks using publicly disclosed ASP.NET machine keys | Microsoft Security Blog*. https://www.microsoft.com/en-us/security/blog/2025/02/06/code-injection-attacks-using-publicly-disclosed-asp-net-machine-keys
11. *Page.ViewStateUserKey Property (System.Web.UI) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.ui.page.viewstateuserkey?view=netframework-4.8.1
12. *ViewStateEncryptionMode Enum (System.Web.UI) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.ui.viewstateencryptionmode?view=netframework-4.8.1
13. *Determine which .NET Framework versions are installed - .NET Framework | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/framework/install/how-to-determine-which-versions-are-installed
14. *Secure ASP.NET ViewState - .NET Blog*. https://devblogs.microsoft.com/dotnet/secure-asp-net-viewstate/
15. [
        NuGet Gallery
        | Microsoft.AspNet.Mvc 5.3.0
    ](https://www.nuget.org/packages/Microsoft.AspNet.Mvc)
16. *Deserialization - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html
17. *Microsoft Security Advisory 2905247 | Microsoft Learn*. https://learn.microsoft.com/en-us/security-updates/securityadvisories/2013/2905247
18. *.NET Framework & Windows OS versions - .NET Framework | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/framework/install/versions-and-dependencies
19. *Trace Failed Requests Logging for a Site &lt;traceFailedRequestsLogging&gt; | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/configuration/system.applicationhost/sites/site/tracefailedrequestslogging
20. *App & API Protector — Website Application Protection | Akamai*. https://www.akamai.com/products/app-and-api-protector
21. *CA2300: Do not use insecure deserializer BinaryFormatter (code analysis) - .NET | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca2300
22. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
