# Safe SSRF Research for the MUJ SLCM Ecosystem

## Executive Summary

- **Evidence Boundary**: The public MUJ portal confirms a portal landing page, institutional sign-in context, and parent-login option. The extracted page shows `@muj.manipal.edu`, but it does not name Microsoft 365 or expose an identity-provider URL [15]. The brief's claims of ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 must therefore be treated as requester-supplied architecture assumptions, not independently verified findings.

- **No Vulnerability Finding**: Public evidence does not establish that MUJ SLCM offers image-by-URL import, user-configurable webhooks, URL-to-PDF conversion, or XML document processing. It also does not establish SSRF. The report evaluates what would be risky **if** an authorized architecture or code review confirms one of these features.

- **Primary SSRF Boundary**: OWASP defines SSRF as attacker influence over a URL that server-side code reads or submits to, potentially letting the application reach internal resources that the external user cannot reach directly [2]. The important trust boundary is consequently the application's outbound network path, not merely the browser-to-Akamai-to-IIS ingress path.

- **Four Candidate Sink Classes**: OWASP expressly identifies externally hosted images and custom webhook or callback URLs as SSRF-prone patterns [3]. A URL-to-PDF renderer adds a second network-capable parser: WeasyPrint's own security documentation says it can retrieve HTTPS resources and local `file://` resources, and recommends a custom URL fetcher and strict resource isolation for untrusted input [16]. XML external entity behavior is a fourth sink because an XML resolver may retrieve an external resource.

- **Dot Net Redirect Hazard**: On the .NET Framework versions listed by Microsoft, `HttpWebRequest.AllowAutoRedirect` defaults to `true`; disabling it returns 300-399 responses to application code instead of following them [6]. A check applied only to the first URL can therefore be invalidated by a later redirect unless redirects are disabled or every hop is resolved and revalidated.

- **Dot Net XML Nuance**: Microsoft documents that `XmlReaderSettings.XmlResolver` defaults to `null` beginning with .NET Framework 4.5.2, while older behavior used an `XmlUrlResolver`; a null resolver causes an exception when external access is attempted [9]. That safer default is not a substitute for explicit configuration because parser type and framework version matter. Microsoft also documents vulnerable-by-default `XmlTextReader` behavior for .NET Framework 4.0 through 4.5.2 when DTD processing is left at `Parse` [8].

- **Akamai and IIS Are Not Egress Controls**: Microsoft describes IIS ARR reverse proxying as receiving Internet requests and forwarding them to back-end applications [21]. Akamai describes SSRF as using a web or cloud server as a pivot to access resources behind a firewall [13]. **Inference:** an ingress reverse proxy or WAF may detect a malicious input, but it does not by itself constrain a request later created by application code; application validation and deny-by-default egress remain necessary.

- **Authorization-First Testing**: NIST SP 800-115 says every assessment should have a plan that identifies scope, authorized testers, logistics, data handling, incident handling, and explicitly prohibited activities [20]. For this university-club project, the safe path is static review and isolated testing first, followed only by owner-authorized staging callbacks to infrastructure controlled by MUJ or the assessor. No internal address, cloud metadata service, third-party host, or production endpoint should be used as a test destination.

## 1. Public Evidence, Assumptions, and Analytical Transparency

The independently observable page at `https://mujslcm.jaipur.manipal.edu/Home/Index` displays the MUJ portal, an institutional sign-in associated with `@muj.manipal.edu`, and a parent-login option [15]. The root URL similarly presents the MUJ portal and sign-in choices [17]. This supports the hostname and login-context claims, but nothing in the extracted public content identifies the application framework, IIS version, Akamai deployment, or Microsoft 365 identity provider.

I cannot provide private chain-of-thought or hidden internal reasoning. Instead, this report provides a reproducible analytical record: source observations, requester-supplied assumptions, explicitly labeled inferences, decision criteria, test gates, and confidence levels. That is more suitable for a security-club report because another reviewer can challenge each premise without needing unverifiable private reasoning.

| Architecture statement | Evidence status | What may safely be concluded | What must not be claimed |
|---|---|---|---|
| `mujslcm.jaipur.manipal.edu` is an MUJ portal | Publicly verified | The public page identifies itself as the MUJ portal [17] | It does not prove any SSRF-prone feature exists |
| Institutional and parent sign-in choices exist | Publicly verified | The page shows institutional and parent-login choices [15] | It does not prove that either path uses Microsoft 365 |
| Microsoft 365 identity | Requester-supplied assumption | It may be used as a review hypothesis | The page does not explicitly name Microsoft 365 or expose an identity-provider URL [15] |
| ASP.NET MVC 5.3 and .NET Framework 4.x | Requester-supplied assumption | These versions can guide an authorized code-review checklist | They are not independently verified by the public page |
| IIS 10 behind Akamai | Requester-supplied assumption | This is a plausible ingress model for threat modeling | It is not evidence that egress is filtered, nor that a bypass exists |
| Image import, webhooks, URL-to-PDF, or XML processing | Candidate feature classes | Review them if source, configuration, or product documentation confirms them | Their presence cannot be inferred from the login page |
| SSRF in MUJ SLCM | Not established | No vulnerability verdict can be made from public evidence | Do not describe MUJ SLCM as vulnerable |

The central conclusion is deliberately narrow: the technology assumptions make SSRF review relevant, but relevance is not vulnerability evidence. Passive public research can define a safe review plan; it cannot establish server-side network behavior.

## 2. Four SSRF Sink Patterns and Distinct Failure Modes

OWASP describes SSRF as functionality that imports from, publishes to, or reads from a user-influenced URL [2]. Its prevention guidance names an externally hosted user image and a user-supplied webhook or callback URL as concrete examples [3]. These are useful models for reviewing a student lifecycle platform, but they remain generic patterns until an authorized inventory confirms corresponding MUJ features.

| Candidate sink | Server-side action | Principal failure mode | Safe evidence to seek | Primary control |
|---|---|---|---|---|
| Image URL import | Application downloads an image supplied by URL | The downloader can be redirected or resolved to a non-public destination; the response may not actually be an image | Source call graph, approved staging log, and a callback to an assessor-controlled public image | Prefer direct upload; otherwise allowlist destinations, disable redirects, validate resolved addresses, enforce size and media limits |
| Webhook or callback | Application sends an outbound notification to a registered URL | A user can choose a destination inside a more trusted network or exploit redirect and DNS changes | Configuration model, ownership-verification design, and one inert staging callback | Approved-domain or tenant-specific allowlist, destination verification, no automatic credentials, signed minimal payload |
| URL-to-PDF | Renderer loads a page and its images, fonts, styles, or embeds | The primary URL or a nested resource can create an unintended network or local-file request | Renderer identity and version, URL-fetch policy, sandbox settings, and isolated integration tests | Custom fetcher, no local-file access, deny-by-default egress, same-origin or explicit asset allowlist, time and memory limits |
| XML document processor | Parser resolves a DTD, entity, schema, or other external resource | A resolver performs an outbound request or accesses a local file during parsing | Parser type, framework version, `DtdProcessing`, and `XmlResolver` configuration | Prohibit DTDs when unnecessary, set the resolver to null, and use trusted local schemas only |

### Case study: OWASP's image and webhook models

An image importer often appears benign because its business result is a file, not an HTTP response. The mechanism still requires server-side code to accept a location and retrieve content. OWASP uses exactly this example: a user provides an avatar URL for the application to download [3]. If the application validates only the textual hostname, a redirect, alternate address representation, or DNS change can separate the checked destination from the connected destination. OWASP consequently recommends not accepting complete URLs when a narrower identifier can work, disabling redirect following, and restricting routes at the network layer [3].

A webhook has the same primitive but a different business requirement. The remote destination is intentionally user-configurable, so a fixed global allowlist may be impractical. The design should instead bind each destination to a verified tenant or institutional domain, send no ambient credentials, minimize the payload, and enforce a deny-by-default egress policy. The observation is that both features create outbound requests; the mechanism differs because images pull data while webhooks push data. The implication is that a single generic URL regular expression is not an adequate control for both.

### Case study: WeasyPrint demonstrates URL-to-PDF risk

WeasyPrint's own documentation warns that untrusted HTML or CSS requires extra configuration to prevent high resource use, endless rendering, and local-file leaks [16]. It states that the renderer can retrieve network files through HTTPS and that its default timeout covers HTTP, HTTPS, and FTP but not other protocols such as `file://` [16]. It recommends a custom URL fetcher and process-level limits [16].

This does not show that MUJ uses WeasyPrint. It demonstrates why a renderer must be treated as a network client and file parser, not merely as a formatting library. **Inference:** an ASP.NET application may invoke a different renderer, but the review questions remain the same: which schemes are supported, whether nested resources are fetched, which redirect policy applies, whether local files are reachable, and what network namespace the process can access.

### Case study: .NET XML defaults are version-dependent

Microsoft documents that an `XmlReaderSettings` resolver set to null throws when the reader attempts to access an external resource, and that null became the default beginning with .NET Framework 4.5.2 [9]. However, Microsoft also documents `XmlTextReader` in .NET Framework 4.0 through 4.5.2 as defaulting to `DtdProcessing.Parse` in the cited security guidance [8]. `Prohibit` rejects a document containing a DOCTYPE, `Ignore` skips it, and `Parse` processes inline DTDs [8].

The apparent tension is the key lesson: saying ".NET Framework 4.x" is too broad for an XXE verdict. Parser class, construction path, configuration, and exact framework behavior all matter. The safe decision is to configure both controls explicitly rather than relying on inherited defaults.

## 3. ASP.NET and .NET Framework Mechanics That Change Risk

`WebRequest` is the abstract .NET request/response model, and registered descendants can handle protocols such as HTTP or FTP [4]. Microsoft now recommends `HttpClient` for new development and marks `WebRequest`, `HttpWebRequest`, `ServicePoint`, and `WebClient` obsolete in modern development guidance [4]. That recommendation does not mean these APIs are absent from a .NET Framework 4.x application; Microsoft lists `HttpWebRequest.AllowAutoRedirect` as applicable through .NET Framework 4.8.1 [6].

| .NET behavior | Documented fact | Security consequence | Review or remediation decision |
|---|---|---|---|
| Protocol dispatch | `WebRequest` descendants may be registered for particular protocols or server paths [4] | A generic URI sink may support more than the reviewer expects | Inventory permitted schemes at the application boundary; normally allow only HTTPS for public callbacks |
| Automatic redirects | `HttpWebRequest.AllowAutoRedirect` defaults to `true` [6] | A safe initial URL can lead to a different destination | Set it to false, or validate and authorize every hop before connecting |
| Redirect count | `MaximumAutomaticRedirections` controls the maximum followed redirects [6] | Limiting count reduces loops but does not validate destinations | Treat count as resource protection, not SSRF authorization |
| Authorization behavior | `HttpWebRequest` clears `Authorization` on automatic redirect and attempts re-authentication at the new location [6] | Built-in behavior reduces one credential-forwarding path but does not make the redirected destination safe | Do not attach ambient credentials to generic fetchers; separately authorize each destination |
| Proxy selection | An explicit request proxy overrides application or machine settings; absent those settings, Internet options may be inherited, or the request may connect directly [7] | Staging and production can take different network paths | Make proxy and egress policy explicit and test the deployed configuration |
| Local proxy bypass | `HttpWebRequest` supports local proxy bypass [7] | A centralized outbound proxy can be bypassed for destinations considered local if configured that way | Do not rely solely on proxy inspection; enforce host-level or subnet egress policy too |
| IP parsing | OWASP notes that .NET `IPAddress.TryParse` accepts several alternate encodings and says to compare the parsed output with the allowlist [3] | Comparing only the raw string can produce inconsistent decisions | Parse once, normalize, classify the resulting address, and use that canonical value |
| Domain validation | OWASP identifies `Uri.CheckHostName` for format checks and separately requires allowlist membership [3] | Syntactic validity does not establish authorization | Keep format validation and destination authorization as distinct checks |
| DNS timing | OWASP warns that a later business-code resolution can leave an application exposed to DNS pinning behavior [3] | A hostname may resolve differently between validation and connection | Re-resolve at the controlled connection boundary and backstop with egress filtering |

### Redirect validation gap

Consider an authorized staging image importer that checks the first hostname and then calls `HttpWebRequest.GetResponse()`. Microsoft documents that automatic redirect following is on by default [6]. **Inference:** if the first server returns a redirect and application code does not inspect it, the effective destination can differ from the destination that passed validation. The correct security property is therefore not "the submitted URL was safe" but "every network connection created for this job was authorized."

Replacing `HttpWebRequest` with `HttpClient` can improve maintainability, but API migration alone does not create that property. The handler's redirect, proxy, DNS, and credential behavior must still be configured. The recommendation is a dedicated outbound-fetch service or wrapper with one narrow policy, rather than scattered calls to `WebRequest.Create`, `WebClient`, `HttpWebRequest`, or `HttpClient` throughout MVC controllers and background jobs.

## 4. Why IIS and Akamai Do Not Automatically Solve Loopback Risk

Microsoft's IIS ARR example defines a reverse proxy as an Internet-accessible server that receives web requests and forwards them to intranet applications [21]. Akamai defines SSRF as manipulation of an API's requests so that a web or cloud server acts as a pivot into resources protected behind a firewall [13]. These sources describe different traffic directions: ingress proxying brings a client request toward the application, while SSRF causes application code to originate another request.

**Architectural inference:** if Akamai is in front of MUJ SLCM, it can inspect the incoming action that asks the application to fetch something. It does not automatically become the enforcement point for the later connection created by an IIS worker process, background service, webhook dispatcher, XML resolver, or renderer. That outbound request may use a configured proxy, inherited Windows settings, local proxy bypass, or a direct connection, as Microsoft documents for `HttpWebRequest` [7]. This is why the word "behind" must not be mistaken for "unable to initiate egress."

| Incomplete protection | Why it fails | Source-grounded issue | Required replacement or backstop |
|---|---|---|---|
| Block only the word `localhost` | Loopback is an address class, not one spelling | IANA identifies IPv4 `127.0.0.0/8` and IPv6 `::1/128` as loopback and not globally reachable [12][14] | Resolve and classify canonical IPv4 and IPv6 addresses |
| Block only RFC 1918 IPv4 | IPv6 unique-local and link-local destinations remain | IANA identifies `fc00::/7` as unique-local and `fe80::/10` as link-local, neither globally reachable [12] | Apply one policy across every A and AAAA result |
| Validate only before a redirect | The client can connect to a later location | .NET Framework `HttpWebRequest` follows redirects by default [6] | Disable redirects or re-authorize every hop |
| Validate a hostname only once | DNS answers can change before use | OWASP specifically warns about DNS pinning and a later business-code resolution [3] | Couple resolution with connection and enforce network egress restrictions |
| Depend only on an outbound proxy | Local-bypass or direct-connect configuration can change the path | Microsoft documents local proxy bypass and direct connection when no proxy is configured [7] | Add host firewall, subnet ACL, or equivalent deny-by-default routing |
| Depend only on Akamai or another WAF | The dangerous operation is an application-originated request | OWASP states SSRF can coerce an application to reach destinations despite firewalls, VPNs, or ACLs [1] | Combine ingress detection with application authorization and egress enforcement |
| Maintain a regex denylist | Alternate representations and parser differences create gaps | OWASP says not to mitigate SSRF with a denylist or regular expression [1] | Use a positive allowlist where possible and canonical address classification everywhere else |

The correct design objective is not "recognize known bad host strings." It is "prove that each actual connection is to an approved public or partner destination." OWASP recommends enforcing scheme, port, and destination with a positive allowlist, disabling redirects, accounting for DNS rebinding and TOCTOU, and applying deny-by-default network policy [1].

## 5. Authorization-First, No-Damage Test Plan

NIST states that an assessment plan provides structure and accountability and should exist regardless of scope or tester [20]. It should identify authorized and excluded systems, permitted testing levels, prohibited activities, contacts, sensitive-data handling, and incident procedures [20]. NIST further recommends ceasing activity when an incident occurs until the organization authorizes resumption [20].

These requirements are especially important for SSRF because an uncontrolled test can make the university's server contact an internal or third-party system. The club should not test the live portal merely because a feature appears reachable. Written authorization must identify the precise hostname, account, feature, environment, source IPs, time window, request cap, data to be retained, prohibited destinations, and named stop authority.

| Gate | Activity | Evidence produced | Safety boundary | Exit criterion |
|---|---|---|---|---|
| 0. Written authorization | Obtain approval from the system owner and security or IT operations | Signed assessment plan or ROE | No technical testing before approval | Scope, exclusions, contacts, and halt criteria are unambiguous |
| 1. Passive inventory | Review public documentation and owner-provided architecture | Feature and trust-boundary map | No login, scanning, or crafted requests | Candidate URL and XML sinks are identified or ruled out |
| 2. Static review | Inspect authorized source and configuration for outbound APIs and parser settings | Source-to-sink map and configuration findings | No network traffic | Every input path to `WebRequest`, `HttpWebRequest`, `WebClient`, `HttpClient`, renderer, or XML resolver is classified |
| 3. Isolated unit tests | Replace network clients with mocks or a test handler | Proof that redirects, schemes, and non-public addresses are rejected | No route to campus, Internet, or cloud metadata services | Policy tests pass for IPv4, IPv6, redirects, and DNS changes |
| 4. Owner-controlled staging | Use one inert HTTPS callback endpoint controlled by MUJ or the authorized assessor | Correlation ID, request count, resolved address, headers approved for capture | No third parties, no internal destinations, no sensitive payload | Expected callback occurs once and contains no credentials or student data |
| 5. Constrained production confirmation | Only if separately authorized and operationally necessary, repeat the minimum benign callback | Confirmation of deployed behavior | Maintenance window, one approved feature, immediate stop authority | One conclusive result, then stop |
| 6. Remediation verification | Re-run the same benign approved case after fixes | Before-and-after control evidence | Same destination and limits as the approved test | Block or allow decision matches the written security policy |

### Destination classes that testing must never contact

The following table is a defensive deny policy, not a payload list. An authorized test harness should verify rejection with mocked destinations or an isolated laboratory network. It should not send traffic from MUJ infrastructure to these ranges.

| Address class | Prefixes | IANA reachability status | Test policy |
|---|---|---|---|
| IPv4 loopback | `127.0.0.0/8` | Not globally reachable [14] | Hard deny; validate only in a disconnected unit-test harness |
| IPv4 private use | `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` | Not globally reachable [14] | Hard deny unless a fixed internal integration is separately designed and allowlisted by address and service |
| IPv4 link-local | `169.254.0.0/16` | Not globally reachable [14] | Hard deny; never use as an SSRF proof target |
| IPv6 loopback | `::1/128` | Not globally reachable [12] | Hard deny |
| IPv6 unique-local | `fc00::/7` | Not globally reachable [12] | Hard deny unless a specific internal integration is formally approved |
| IPv6 link-local | `fe80::/10` | Not globally reachable [12] | Hard deny |
| Other special-purpose or non-global space | Current IANA special-purpose registries | Status varies by registered prefix | Default deny unless the security architecture explicitly authorizes the exact use |

### Benign per-sink confirmation designs

| Sink | Authorized benign test | Expected secure result | Stop condition |
|---|---|---|---|
| Image import | A tiny, valid image on a university-controlled HTTPS host with no redirects | One request, accepted media type, bounded body, no cookies or authorization headers | More than the ROE-approved request count, unexpected headers, or any request to another host |
| Webhook | Register an empty event against an assessor-controlled HTTPS endpoint using a test tenant | Destination ownership is verified; payload contains only a random correlation value | Any student data, session material, repeated delivery beyond policy, or unapproved redirect |
| URL-to-PDF | Render a static controlled page containing one approved same-origin asset | Renderer reaches only the allowlisted host; local files and all other origins remain unavailable | Any unexpected origin, local-file attempt, resource spike, or renderer instability |
| XML processor | Use mocks to confirm that a DOCTYPE is rejected and external resolution never invokes a network client | `DtdProcessing` is prohibited and resolver is null where external resources are unnecessary | Any real network resolution or filesystem access |

The callback receiver should store only the minimum evidence approved by the ROE: timestamp, random case identifier, source network information if permitted, HTTP method, and a small allowlisted header set. It should return an empty success response, issue no redirect, load no subresources, set no cookies, and collect no credentials. OWASP recommends logging accepted and blocked network flows, while NIST requires explicit data storage, transmission, retention, and destruction rules [1][20].

## 6. Defensive Architecture and Acceptance Criteria

A robust design layers feature constraints, canonical parsing, redirect control, network isolation, parser hardening, renderer sandboxing, and telemetry. OWASP recommends positive allowlists, no raw user-controlled complete URLs when a narrower value is possible, disabled redirects, and network routes limited to legitimate flows [3].

| Layer | Recommended control | Acceptance criterion |
|---|---|---|
| Feature design | Replace arbitrary URLs with uploaded files, stored object identifiers, or administrator-defined integration IDs where possible | Ordinary users cannot introduce a new network destination |
| Scheme and port | Permit only the exact schemes and ports required by the feature, normally HTTPS for external callbacks | Unsupported schemes and ports are rejected before DNS resolution |
| Host authorization | Use exact host allowlists or tenant-bound verified domains; avoid suffix checks that blur label boundaries | Every accepted host maps to a named business integration owner |
| Address resolution | Resolve all IPv4 and IPv6 answers, normalize them, and reject any non-global or prohibited result | A hostname is rejected if any usable answer violates policy |
| Redirects | Set `AllowAutoRedirect` to false for `HttpWebRequest`, or implement an explicitly bounded, revalidated redirect loop | No redirect causes a connection before the next destination is authorized [6] |
| Proxy and route | Configure the outbound proxy explicitly and back it with host or network deny-by-default egress | A local-bypass or missing-proxy condition still cannot reach prohibited networks [7] |
| Credentials | Use a dedicated unprivileged outbound client with no inbound cookies, user tokens, or ambient machine credentials | Callback captures contain no authentication material |
| Response handling | Cap response bytes, content type, decompression, duration, and concurrency; never return raw remote bodies to the user | Large, slow, malformed, or mismatched responses terminate safely; OWASP advises against returning raw responses [1] |
| XML | Set DTD processing to `Prohibit` and the resolver to null unless a narrowly trusted resolver is required | External resolution produces no network or local-file access [9][8] |
| PDF renderer | Use a custom URL fetcher, restrict network and filesystem access, and enforce process time and memory limits | The renderer can retrieve only explicitly approved assets and cannot read local files [16] |
| Segmentation | Run generic fetchers and renderers in a network segment with no route to administrative, identity, database, or management services | Compromise of the fetch worker does not create an internal pivot; OWASP recommends network segregation [3] |
| Telemetry | Log normalized destination, resolved addresses, port, redirect count, decision reason, sink name, tenant, and correlation ID | Security operations can distinguish approved integration traffic from blocked probes without logging secrets |
| Edge control | Keep Akamai or WAF rules for attack detection and rate limiting, but do not treat them as the sole SSRF control | Disabling the edge in a lab does not change the egress policy decision |

### Detection priorities

The highest-value alert is a blocked outbound request from a web or rendering worker to a non-global address. Other useful signals include repeated rejected destinations, mixed IPv4 and IPv6 answers, redirect attempts to a different registrable domain, URL inputs containing user information, unexpected ports, a sudden increase in renderer fetch counts, and DNS answers that change between policy checks. These are recommended detection hypotheses derived from the validated failure modes, not evidence of activity at MUJ.

Source review should follow data flow from MVC action parameters, model-bound fields, database-stored webhook settings, uploaded documents, and queue messages into outbound request and XML APIs. The key question is not whether a controller contains the word `Url`; it is whether untrusted data can influence scheme, authority, port, path to a privileged service, redirect target, DNS result, proxy choice, or renderer subresource. Microsoft describes `WebRequest` as URI-driven protocol dispatch, which is why source-to-sink tracing is more reliable than a simple string search [4].

## 7. Synthesis: One Primitive, Four Different Control Problems

All four patterns share one primitive: lower-trust input influences a higher-trust process that can access a URL or external resource. They differ in direction, protocol surface, nested processing, expected destination diversity, and failure cost.

| Dimension | Image import | Webhook | URL-to-PDF | XML external resource |
|---|---|---|---|---|
| Network direction | Pull | Push | Pull, often with nested pulls | Pull during parsing |
| Typical destination scope | Public media hosts or one storage service | Many customer or partner endpoints | Page origin plus assets unless constrained | Usually none; sometimes trusted schemas |
| Best design move | Prefer direct upload | Verify and bind destinations to integration owners | Isolate the renderer and custom-fetch every asset | Disable DTD and external resolution |
| Redirect tolerance | Usually unnecessary | Usually unnecessary | Sometimes expected, but each hop must be revalidated | Not an HTTP feature requirement; resolver should normally be off |
| Parser complexity | Image decoder after download | Usually minimal response processing | HTML, CSS, font, image, and URI processing | XML, DTD, entity, and schema processing |
| Main resource risk | Oversized or deceptive file | Delivery loops and data disclosure | CPU, memory, local files, and multiple network requests | Entity expansion, file access, and outbound resolution |
| Strongest containment | Allowlisted downloader with media limits | Dedicated dispatcher with minimal signed payload | Sandboxed worker with deny-by-default egress | Explicit parser settings and no resolver |
| Public evidence for MUJ feature | None located | None located | None located | None located |

The first non-obvious tension is that the most flexible business feature is the hardest to allowlist. Image import can often be replaced with upload, and XML external resolution can often be eliminated. Webhooks are valuable precisely because destinations vary. Their safer architecture therefore depends more heavily on destination ownership verification, isolated dispatchers, minimal payloads, and network policy.

The second tension is between framework defaults and explicit intent. The documented null `XmlResolver` default beginning with .NET Framework 4.5.2 is helpful [9], while `HttpWebRequest` automatic redirects default to enabled [6]. A team that relies on defaults gets inconsistent protection across APIs and versions. Explicit configuration makes the security property reviewable and testable.

The third tension is between perimeter visibility and connection authority. Akamai or another edge can provide valuable ingress detection, while IIS ARR can deliberately route inbound traffic to back-end applications [21]. Neither fact proves control over every application-originated connection. The holistic architecture assigns the final allow or deny decision to a dedicated fetch policy and then independently prevents prohibited routes at the network layer.

The fourth tension is evidentiary. The brief supplies a detailed stack, but the public portal exposes only login context. A strong university report should resist converting a plausible technology fingerprint into a vulnerability claim. The immediate actionable result is a prioritized, owner-authorized review plan, not an exploit attempt.

## VERDICT

**Verdict: SSRF review is justified as a defensive design exercise, but there is no public evidence in this research that MUJ SLCM contains an SSRF vulnerability.**

| Conclusion | Confidence | Basis |
|---|---|---|
| Generic image URL, webhook, URL-to-PDF, and XML features can create SSRF-capable sinks | High | OWASP directly identifies image and webhook patterns; Microsoft and WeasyPrint document resolver and renderer network behavior [3][9][16] |
| Legacy .NET behavior can undermine first-URL-only validation | High | Microsoft documents enabled-by-default `HttpWebRequest` redirects and environment-dependent proxy behavior [6][7] |
| An ingress WAF or reverse proxy is insufficient as the only SSRF defense | High for the general architecture; moderate for the unverified MUJ deployment | OWASP and Akamai describe SSRF as a server-side pivot; IIS documentation describes inbound reverse proxying [1][13][21] |
| MUJ SLCM uses all technologies stated in the brief | Low to moderate | The public portal verifies the portal and institutional sign-in context, but not the named framework, IIS, Akamai, or Microsoft 365 versions [15] |
| MUJ SLCM exposes one of the four candidate sinks | Low | No public evidence located |
| MUJ SLCM is vulnerable to SSRF | No evidentiary basis | No authorized dynamic test, source review, configuration review, or confirmed sink was available |

**Overall confidence: High** in the general SSRF and .NET defensive analysis; **low** in any target-specific exposure claim. The university security club should present this as a threat model and safe assessment plan. It should not test the live portal, authenticate, scan, target internal addresses, contact cloud metadata services, or send callbacks until MUJ's authorized owner supplies written scope and rules of engagement.

## References

1. *A10 Server Side Request Forgery (SSRF) - OWASP Top 10:2021*. https://owasp.org/Top10/2021/A10_2021-Server-Side_Request_Forgery_%28SSRF%29
2. *Server Side Request Forgery | OWASP Foundation*. https://owasp.org/www-community/attacks/Server_Side_Request_Forgery
3. *Server Side Request Forgery Prevention - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html
4. *WebRequest Class (System.Net) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.net.webrequest?view=netframework-4.8.1
5. *Breaking change: WebRequest, WebClient, and ServicePoint are obsolete - .NET | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/core/compatibility/networking/6.0/webrequest-deprecated
6. *HttpWebRequest.AllowAutoRedirect Property (System.Net) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.net.httpwebrequest.allowautoredirect?view=netframework-4.8.1
7. *HttpWebRequest.Proxy Property (System.Net) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.net.httpwebrequest.proxy?view=netframework-4.8.1
8. *XML External Entity Prevention - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html
9. *XmlReaderSettings.XmlResolver Property (System.Xml) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.xml.xmlreadersettings.xmlresolver?view=netframework-4.8.1
10. *XmlReaderSettings.DtdProcessing Property (System.Xml) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.xml.xmlreadersettings.dtdprocessing?view=netframework-4.8.1
11. *SP 800-115, Technical Guide to Information Security Testing and Assessment | CSRC*. https://csrc.nist.gov/pubs/sp/800/115/final
12. *IPv6 Special-Purpose Address Space*. https://www.iana.org/assignments/iana-ipv6-special-registry/iana-ipv6-special-registry.xhtml
13. *What Is Server-Side Request Forgery? | Akamai*. https://www.akamai.com/glossary/what-is-server-side-request-forgery
14. *IPv4 Special-Purpose Address Space*. https://www.iana.org/assignments/iana-ipv4-special-registry/iana-ipv4-special-registry.xhtml
15. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
16. *First Steps - WeasyPrint 69.0 documentation*. https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#security
17. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
18. *wkhtmltopdf.org*. https://wkhtmltopdf.org/usage/wkhtmltopdf.txt
19. *First Steps - WeasyPrint 69.0 documentation*. https://doc.courtbouillon.org/weasyprint/stable/first_steps.html
20. *Technical guide to information security testing and assessment*. https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf
21. *Reverse Proxy with URL Rewrite v2 and Application Request Routing | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/extensions/url-rewrite-module/reverse-proxy-with-url-rewrite-v2-and-application-request-routing
