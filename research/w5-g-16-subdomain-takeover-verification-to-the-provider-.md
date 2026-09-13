# Provider-Side Proof for Azure Subdomain Takeovers

## Executive Summary

This report answers the narrow question that matters for the MUJ SLCM campaign: does a dangling DNS record pointing at Azure App Service prove that another party can obtain the provider-side resource, or does it only identify a possible condition? Microsoft defines the risk as a DNS record pointing at a deprovisioned Azure resource. It specifically warns that a dangling CNAME can allow another Azure subscription to receive the old subdomain, and that traffic can then be routed to the new resource. [1] [1]

The target measurements in the campaign brief are treated as client-supplied observations dated 2026-09-13. They have no public URL in the brief, so they are not presented as independently verified public facts. The measured IIS, ASP.NET MVC, .NET, jQuery, TLS, error-page, method-policy, antiforgery, and `enc`-oracle observations are relevant to application-security triage, but they do not establish Azure resource claimability. This report therefore does not upgrade the campaign from PARTIAL.

- **Proof Standard**: Azure's official definition connects takeover to a deprovisioned resource and possible reassignment, while a CNAME or HTTP error page alone does not show that reassignment is currently permitted. [1] -> Keep the two MUJ records at PARTIAL until a provider-side availability result is captured.
- **Azure Signal**: Azure App Service exposes an authenticated Check Name Availability operation that returns `nameAvailable`, `reason`, and `message`; `true` means the name is valid and available according to that operation, while `false` means invalid, unavailable, or both. [19] [19] -> Use this as the primary non-destructive provider-side check after authorization.
- **Reservation Nuance**: App Service normally forbids immediate cross-tenant reuse after deletion, and the original tenant can immediately reuse the name. [2] -> Do not infer cross-tenant claimability from the visible CNAME or from a fingerprint.
- **Domain Verification**: Azure recommends a domain-verification TXT record such as `asuid` because it helps prevent another App Service app from validating or taking over a custom domain. [2] [15] -> Record the TXT state when the DNS owner authorizes that read, but do not change DNS during a detection exercise.
- **Scanner Reality**: Subjack, Subzy, SubOver, dnsReaper, TakeoverSpy, SubTake, ReClaimor, and the Nuclei takeover templates are principally DNS, HTTP, TLS, or response-fingerprint detectors. Their documented interfaces do not establish an Azure resource binding. [7] [5] [8] [4] [9] [24] [21] [17] -> Treat their positive output as a candidate, not as provider proof.
- **Action-Capable Exception**: tko-subs documents optional takeover actions for GitHub Pages and Heroku, using credentials, but not Azure App Service. [6] [6] -> Never enable its takeover mode against MUJ; it is not an Azure proof method.
- **Azure Script Gap**: AzDanglingDnsFinder advertises an authenticated check that resolved Azure service names are available, but its public README reports only a potential vulnerability and does not document an external claim or successful binding. [10] -> Use it, if at all, as an auxiliary availability signal, not as the final acceptance criterion.
- **Safety Boundary**: Public passive research and offline analysis are the safest pre-authorization activities. Provider API requests, repeated active probing, DNS changes, resource creation, custom-domain validation, or use of test identities require the signed scope letter and the two test accounts described in the brief. Security research should be performed only on equipment the finder is authorized to use. [27] [27]
- **Recommended Decision**: Obtain an explicit MUJ-approved Azure subscription or tenant context, make one read-only name-availability request for each authorized CNAME target, preserve the raw JSON and timestamp, and stop there unless the letter expressly authorizes more. A claimability result is not a reason to create a resource on the live target.

## 1. Scope, Safety, and the Proof Standard

### What the campaign must prove

A subdomain takeover has two logically separate parts. First, the organization's DNS continues to point at a provider-side name or resource that it no longer controls. Second, an unauthorized or differently controlled party can obtain that provider-side name, attach it to a resource, or otherwise cause the provider to route the organization's hostname to that party. Microsoft describes the first condition as a dangling DNS entry and identifies CNAME records as especially exposed. [1] The second condition is the part that fingerprint-only campaigns do not establish: Microsoft says another Azure subscription may be able to receive the dangling subdomain, but whether that is possible depends on provider state, resource type, tenant reservation, and domain verification. [1] [2]

For this report, the evidence tiers are deliberately conservative:

| Tier | Evidence | What it establishes | What it does not establish | MUJ status | Safe handling |
|---|---|---|---|---|---|
| T0 | Public DNS shows a CNAME chain ending in an Azure hostname | A routing dependency exists | The Azure name is unowned, available, or claimable | Supplied brief says two records are at this tier or higher | Passive collection and offline analysis are preferred |
| T1 | HTTP, TLS, DNS, or provider-error fingerprint matches an unclaimed-service signature | The endpoint resembles a known takeover condition | A provider account can obtain the resource | Current campaign status is PARTIAL, fingerprint only | Low-volume active checks require owner policy; no mutations |
| T2 | An authorized provider-side availability or ownership API reports availability or an equivalent claimability state | The provider currently reports the resource name as available in the tested context | End-to-end DNS routing, custom-domain validation, or successful hostile binding | Not yet captured for MUJ | Signed scope, authorized Azure context, and test accounts required |
| T3 | A client-approved controlled binding in a sandbox or explicitly authorized disposable resource | End-to-end provider behavior under an approved test | That a live production claim should be attempted | Not permitted by the current facts | Only with a written change and rollback plan; never as an informal proof |

The campaign's phrase "provider-side claimability" should therefore be interpreted as a T2 or T3 requirement. T1 is useful evidence, but it is not the verdict. This distinction also avoids a common error: a provider may display a generic unconfigured page while retaining the name reservation, or may allow a name to be reused only inside the original tenant. That is an inference from the Azure reservation rules, not a claim that either condition currently applies to MUJ.

### Authorization boundary

The CMU guidance says vulnerability research should be performed on equipment authorized for that purpose and that researchers should use an appropriate degree of care to reduce legal and operational risk. [27] [27] CISA's policy template similarly conditions safe-harbor treatment on good-faith compliance and instructs a researcher to stop immediately if sensitive information is encountered. [28] [28] Coordinated Vulnerability Disclosure is specifically a process for gathering, coordinating, and disclosing vulnerability information with relevant stakeholders. [27]

Accordingly, this report separates passive, read-only, and state-changing activities. It does not provide a recipe for claiming a live third-party Azure hostname. The exact CNAME targets are discussed only as supplied campaign facts, and the proposed provider check is bounded by the signed scope letter and the two test accounts.

## 2. Azure App Service Mechanics and the Provider-Side Signal

### Why the `azurewebsites.net` suffix is not enough

A CNAME ending in an Azure App Service default hostname identifies a platform relationship, not its current ownership. Azure's security guidance describes a takeover scenario in which a DNS record remains after the associated Azure resource has been deprovisioned. If the CNAME is not removed, another Azure subscription may be able to assign the dangling subdomain, and a resource with the former FQDN can receive traffic. [1]

The important counterweight is App Service name reservation. Microsoft's App Service prevention page says that after an App Service app or App Service Environment is deleted, the corresponding DNS is forbidden from reuse except by subscriptions belonging to the tenant that originally owned the DNS. [2] It further says that only subscriptions in the original tenant can immediately reuse the DNS name and that other subscriptions are not allowed to claim it right after deletion. [2] Thus, a public scan can be correct that a CNAME is stale while still being unable to show cross-tenant claimability.

Azure also documents an `asuid.{subdomain}` TXT record containing the domain verification ID. The record prevents another Azure subscription from validating or taking over the custom domain unless that subscription can satisfy the relevant verification condition. [1] [2] Azure's custom-domain tutorial calls the TXT record highly recommended because it helps avoid takeovers by other App Service apps, and its examples pair the mapping record with a TXT verification record. [15] [15]

### The documented name-availability operation

Azure's current App Service REST documentation describes Check Name Availability as a `POST` operation at:

`https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Web/checknameavailability?api-version=2026-07-15`

The documentation requires a subscription UUID in the path and an API-version query parameter. It lists Azure Active Directory OAuth2 authentication, an authorization URL at `https://login.microsoftonline.com/common/oauth2/authorize`, and the `user_impersonation` scope. [19] The request has required `name` and `type` fields and optional `environmentId` and `isFqdn` fields. [19]

A successful response is documented as `Resource Name Availability` and includes `message`, `nameAvailable`, and `reason`. [19] [19] Azure defines `nameAvailable: true` as meaning the name is valid and available; `false` means invalid, unavailable, or both. It defines `Invalid` as a naming-rule failure and `AlreadyExists` as a name already in use and therefore unavailable. [19] [19]

This is the strongest publicly documented non-destructive Azure signal found in this research, but the source does not call the result an end-to-end subdomain-takeover proof. The conservative interpretation is:

| Provider response | Safe interpretation | MUJ reporting language |
|---|---|---|
| `nameAvailable: false`, `reason: AlreadyExists` | The tested Azure provider context says the name is not available at that time | "Provider-side availability not demonstrated; name was reported unavailable in the authorized test context" |
| `nameAvailable: false`, `reason: Invalid` | The tested input does not satisfy the naming rules | "The test input was invalid; no claimability conclusion" |
| `nameAvailable: true` | The provider says the name is valid and available in the tested context | "Provider-side availability observed at timestamp; no live resource was created" |
| Error, timeout, insufficient permission, or ambiguous response | The test did not establish a result | "Provider-side claimability remains unknown" |

The table's reporting language is an inference designed to preserve the API's qualifiers. It is not a statement that Azure guarantees successful custom-domain attachment after `true`; domain verification, tenant controls, DNS state, and resource-type behavior remain separate checks.

## 3. Technique Universe for This Class of Finding

The following techniques cover the complete evidence path without confusing detection with exploitation.

| Technique family | Core operation | Typical evidence | False-positive or limitation | MUJ authorization level |
|---|---|---|---|---|
| Passive asset discovery | Read certificate-transparency data, public DNS history, public documentation, or an owner-provided zone export | Historical or current hostname and CNAME candidates | Historical records can be stale; CT does not prove current DNS | Safe pre-authorization when no target is contacted; still respect terms |
| Authoritative DNS resolution | Follow the full CNAME chain and query authoritative servers | Current CNAME target, TTL, NXDOMAIN, SERVFAIL, or changed chain | Recursive caches, split-horizon DNS, wildcard records, and propagation can mislead | Low impact but active; use only within owner policy |
| HTTP and TLS fingerprinting | Send a bounded GET or TLS handshake and compare status, headers, body, certificate, and redirects | Provider unclaimed-page text, default page, NXDOMAIN plus service suffix, or TLS mismatch | Providers change error pages; WAFs and rate limits create lookalikes; an active app can still serve a generic page | Requires explicit permission for target probing; no mutations |
| DNS provider classification | Match suffixes such as Azure App Service, Front Door, storage, CDN, or other SaaS providers | Provider attribution and candidate resource type | A suffix is not proof of an unclaimed resource | Read-only and bounded |
| Organization inventory | Use Azure Resource Graph or an owner-controlled inventory to correlate DNS with resources in the organization's subscriptions and tenants | CNAME still associated with an organization resource, or missing association | It cannot by itself prove that an outside subscription can claim the name | Requires owner Azure read access |
| Provider name availability | Use the provider's authenticated availability API for the exact resource type and name | `nameAvailable`, `reason`, and provider message | Availability may be scoped to an API context; it does not automatically test custom-domain binding | Signed scope and authorized provider account |
| Domain ownership verification | Inspect existing `asuid` TXT or equivalent verification record; validate only with owner-controlled DNS | Verification token present or absent | Absence is not always proof of claimability; adding a record changes DNS state | Read-only inspection needs permission; changes require explicit DNS authorization |
| Controlled sandbox validation | Bind a synthetic or disposable name in a client-owned sandbox, never the live brand hostname | Reproducible provider behavior and rollback evidence | A sandbox may not reproduce reservation or tenant state of the live resource | Requires a separate written change and rollback plan |
| Continuous monitoring | Re-run passive DNS, bounded HTTP, and authorized provider checks on a schedule | Time series of state changes and alerts | A single scan is a point-in-time observation | Monitoring scope and rate limits must be documented |

The mechanism is therefore a chain: discovery identifies a hostname; DNS identifies a provider; HTTP and TLS reduce false positives; the provider API tests the provider-side name state; and ownership or tenant context explains why the result is or is not transferable. The first three links are commonly automated. The fourth is provider-specific and credentialed. The fifth is an authorization and evidence-management problem, not merely a scanner feature.

## 4. Public Tool Inventory

The inventory below covers the public repositories, official APIs, and packages located in this research. "Self-hosted" means the operator runs the code locally or in its own CI. It does not mean that the tool is risk-free or that the license grants permission to scan a third party. "BYOK" means that the operator supplies provider credentials or tokens. A tool is marked "not documented" rather than guessed when its primary material does not state a license, output, or claim behavior.

### Provider-aware and knowledge-base tools

| Tool and exact URL | License and delivery model | How it is driven | Output | Provider-side result? |
|---|---|---|---|---|
| Azure App Service Check Name Availability: https://learn.microsoft.com/en-us/rest/api/appservice/check-name-availability/check-name-availability?view=rest-appservice-2026-07-15 | Azure service API; no standalone software license stated; authenticated service, BYOK Azure identity and subscription | `POST` with subscription ID, API version, `name`, `type`, and optional `isFqdn`; OAuth2 is documented | JSON resource-name availability with `nameAvailable`, `reason`, and `message` [19] [19] | Yes, as an authorized provider availability signal; not documented as end-to-end takeover proof |
| AzDanglingDnsFinder: https://github.com/davidokeyode/AzDanglingDnsFinder | License not specified in the README evidence; self-hosted PowerShell; BYOK Azure PowerShell login and permissions | Reads `domainnames.txt`, resolves Azure service records, and checks whether resolved Azure service names are available [10] | Text indicating whether the name resolves to Azure and whether it is potentially vulnerable [10] | Closest community Azure candidate, but README does not document successful external claim or resource binding |
| Microsoft Get-DanglingDnsRecords: https://github.com/Azure/Azure-Network-Security/blob/master/Cross%20Product/DNS%20-%20Find%20Dangling%20DNS%20Records/Readme.md | License not stated in the cited article; self-hosted PowerShell; BYOK Reader access and Azure Resource Graph read access | Uses organization DNS/CNAME input and Azure subscription or tenant data; Microsoft says it lists domains whose CNAMEs are associated with existing Azure resources [1] | Dangling-domain inventory and resource correlation | No. It is an owner-side inventory and remediation aid, not an external claimability test |
| Can I Take Over XYZ: https://github.com/EdOverflow/can-i-take-over-xyz | CC-BY-4.0; public repository/knowledge base, not a hosted scanner | Read service records and their documented conditions; scanners such as Subzy use its fingerprints | Human-readable service guidance and claim-condition data | No. It is reference data, not a provider transaction or proof tool |

The Microsoft inventory tool is particularly useful when MUJ can provide tenant and subscription read access. Its purpose is to find domain chains connected to resources in the organization's own estate, which is a different question from whether an unrelated subscription can claim an orphaned name. The distinction is supported by Microsoft's own description of the tool's required Reader and Resource Graph access. [1]

### General detection tools

| Tool and exact URL | License and delivery model | How it is driven | Output | Provider-side result? |
|---|---|---|---|---|
| Subjack: https://github.com/haccer/subjack | Apache-2.0; self-hosted Go tool; no hosted fee or BYOK is documented | Single domain `-d`, wordlist `-w`, stdin, threads, timeout, optional HTTPS, and output `-o`; JSON is selected through a `.json` output filename [7] [7] | Console or file results; README identifies labels such as stale A record and zone transfer, with JSON file support [7] [7] | No. It detects names that appear available or claimable but does not document registration [7] [7] |
| Subzy: https://github.com/PentestPad/subzy | GPL-2.0; self-hosted Go tool | `subzy run --target` for one or comma-separated targets, or `--targets` for a file; optional HTTPS, verification, timeout, concurrency, and fail hiding [5] | Console findings, failed checks, and invulnerable hosts; structured output is not documented in the cited README | No. It matches response fingerprints from Can I Take Over XYZ [5] |
| tko-subs: https://github.com/anshumanbh/tko-subs | MIT; self-hosted Go tool; BYOK GitHub token and Heroku credentials only for its optional actions | Normal mode takes domains, provider data, and an output path; optional `-takeover` accepts GitHub and Heroku credentials [6] | CSV fields are `Domain,CNAME,Provider,IsVulnerable,IsTakenOver,Response` [6] | Limited action capability, but only GitHub Pages and Heroku are documented; no Azure action is documented [6] |
| dnsReaper: https://github.com/punk-security/dnsReaper | AGPL-3.0; self-hosted or Docker; no BYOK needed for basic signature checks | `single --domain`, file mode, or DNS-zone/list inputs; it also describes ProjectDiscovery input and pipeline use [4] [4] | CSV by default, local `results.csv`, optional JSON, and non-zero pipeline exit on detection [4] [4] [4] | No. It tests broken CNAMEs against more than 50 signatures and does not document a successful provider registration [4] |
| SubOver: https://github.com/Ice3man543/SubOver | BSD 2-Clause; self-hosted Go tool | `-l` supplies a subdomain list; `-a`, thread, verbose, HTTPS, and timeout options are documented [8] | Console behavior is implied, but provider fingerprint and machine-readable output details are not specified in the cited README [8] | No documented provider-side claim check |
| TakeoverSpy: https://github.com/cyber-ishita/takeoverspy | MIT; self-hosted; no BYOK for documented detection | Single domain, list, or stdin; optional concurrency, HTTP verification, JSON `-j`, or CSV `--csv` [9] [9] | Colored console, JSON, or CSV [9] | No. It analyzes full CNAME chains and matches 50-plus service fingerprints and HTTP response bodies [9] |
| Nuclei plus takeover templates: https://github.com/projectdiscovery/nuclei and https://github.com/projectdiscovery/nuclei-templates/tree/main/http/takeovers | Nuclei engine MIT; self-hosted YAML-template engine; hosted ProjectDiscovery services are separate and are not required for local execution [14] [14] | Targets are passed to the CLI and templates selected with `-t`; Nuclei supports DNS and HTTP templates and targeted requests [16] [18] | Documented formats include JSON, JSONL, Markdown, SARIF, and PDF [14] [14] | No. The Azure DNS template matches NXDOMAIN plus an Azure CNAME suffix; it does not create or bind a provider resource [17] |

These tools are valuable for breadth and repeatability. They are not interchangeable with the Azure API. In particular, Subzy's reliance on response fingerprints, TakeoverSpy's body matching, and Nuclei's Azure template conditions all operate on observations exposed by DNS or HTTP. [5] [9] [17] A scanner can therefore be correct that a record deserves escalation while still being unable to answer the provider-side question.

### Secondary and experimental detectors

| Tool and exact URL | License and delivery model | How it is driven | Output | Claimability assessment |
|---|---|---|---|---|
| SubTake: https://github.com/bowligth/subtake | MIT; self-hosted Python; no hosted fee or BYOK documented | `python subtake.py -d`, `-l` for lists, stdin, worker and timeout options, and `-o` for JSON [24] [24] | `VULNERABLE`, `POTENTIAL`, or safe; `POTENTIAL` requires manual verification [24] [24] | Explicitly detection-only; it never claims a resource [24] |
| ReClaimor: https://pypi.org/project/reclaimor/ | MIT; self-hosted Python package | `pip install reclaimor`; `--url`, `--file`, `--output`, and HTML format options [21] | JSON, CSV, HTML, and console [21] | Detection-only by default; optional verification is documented, but provider-side proof is not documented [21] [21] [21] |
| martinvw subdomain-takeover-tools: https://github.com/martinvw/subdomain-takeover-tools | MIT; self-hosted Python package; configuration can contain Azure, GitHub, and Fastly settings, so BYOK may be required for configured validators [20] [20] | Accepts hostnames, SubTake output, or Nuclei takeover output; includes `confirm_takeover`, authoritative resolution, strict mode, and enrichment scripts [20] [20] | Validator lines, filtered results, and enriched output; README is incomplete per its own documentation [20] | False-positive reduction and validation helpers, not documented as an Azure claim transaction |
| fdzdev Subdomain-Takeover-Checker: https://github.com/fdzdev/Subdomain-Takeover-Checker | License not specified in cited evidence; self-hosted Python | `python3 checker.py -d` or `-l`; dependencies from `requirements.txt` [25] | `results.log` or a new report file with CNAME, potential-vulnerability, progress, and error information [25] | CNAME-pattern and response-message detection only; provider claimability is not specified [25] |
| takeoverpossible: https://github.com/tejassroot/subdomain-takeover-scanner | MIT; self-hosted shell/Python-style framework; no hosted tier or BYOK documented | Install from the repository; `-d` for one domain, `-f` for a file, and `-o` for JSON [13] [13] | JSON export, with DNS validation, HTTP fingerprinting, SSL verification, and false-positive filtering | README says "claimability checks" but names no provider or API. Its cited repository has zero stars, zero forks, and seven commits, so it should be treated as experimental, not as independent proof [13] [13] |

The phrase "every tool" needs one qualification. The public ecosystem contains forks, one-off scripts, commercial scanners, and repositories that are not maintained or whose licenses are absent. No responsible analyst can prove that an unindexed private tool does not exist. The table is therefore exhaustive for the public primary repositories and official material located for this report, while explicitly identifying incomplete or experimental entries instead of inflating them into authoritative evidence.

## 5. Detection Counterpart and the Manual Provider-Side Method

### Detection counterpart

The detection counterpart is the safe, repeatable pipeline that precedes provider proof:

1. Normalize the hostname and preserve the exact input.
2. Resolve the full CNAME chain with authoritative context and a timestamp.
3. Attribute the terminal provider from the chain, not from the HTTP body alone.
4. Perform at most a bounded, authorized GET or TLS handshake and retain status, selected headers, redirect chain, certificate summary, body hash, and response length.
5. Compare the result against a maintained fingerprint set.
6. Mark the result as `candidate`, `not_candidate`, or `unknown`, never as `takeover_confirmed`, unless the provider-side step is present.
7. If authorized, add provider API output and tenant/domain-verification context.

This pipeline explains why the open-source tools are still useful. Subjack supports concurrent list scanning and JSON file output. [7] Subzy makes the fingerprint dependency explicit. [5] dnsReaper returns CSV or JSON and can fail a CI pipeline when a signature is detected. [4] [4] Nuclei makes the detection logic inspectable as YAML and can emit structured formats. [17] [14] These are good detection properties, but they do not change the evidence tier.

A recommended evidence record is:

| Field | Required content | Reason |
|---|---|---|
| `observed_at` | UTC timestamp and time source | Claimability changes over time |
| `hostname` | Exact owner hostname | Prevents confusion between two records |
| `cname_chain` | Every CNAME hop and terminal answer | Shows provider attribution and aliases |
| `dns_context` | Resolver, authoritative result, TTL, and response code | Detects cache and split-horizon issues |
| `http_context` | Method, status, redirect, selected headers, body hash, and length | Makes fingerprints reproducible without storing sensitive content |
| `provider` | Azure App Service or other provider | Selects the correct adapter |
| `provider_check` | API operation, subscription context, response, and reason | Separates T1 from T2 |
| `domain_verification` | Existing TXT record state if authorized | Captures the `asuid` control relevant to App Service |
| `verdict` | `fingerprint_only`, `provider_available`, `provider_unavailable`, or `unknown` | Prevents a scanner from overstating its result |
| `authorization_ref` | Scope-letter identifier and approved operator | Makes the activity auditable |

### Manual method when a tool is not enough

**Pre-authorization, safe by default:** public documentation review, offline analysis of the supplied two CNAMEs, passive certificate-transparency review, and review of owner-provided DNS exports. No target is contacted and no account is used. This is the only category I would describe as unambiguously safe before authorization.

**Pre-authorization, low impact but not automatically permitted:** a public DNS lookup or single HTTP GET may be technically non-destructive, but it still contacts infrastructure and may fall outside a university club's authorization. The signed letter should define the hostnames, rate, method, time window, source IP, and data-handling rules before these are repeated. The fact that the brief records earlier non-destructive measurements does not expand the club's authorization.

**After the signed scope letter and with the two test accounts:** obtain client-provided Azure tenant and subscription context; authenticate with the least privilege that the API permits; call the documented Check Name Availability operation for each explicitly authorized target label and resource type; save the raw JSON, HTTP status, API version, subscription identifier in redacted form, tenant identifier in redacted form, and UTC timestamp; evaluate `nameAvailable` and `reason`; then stop. The API requires an authenticated context and a subscription ID, so a random unaffiliated account is not a valid substitute for the client-approved context. [19]

Do not create an App Service, add a custom domain, change the CNAME, add an `asuid` record, publish content, or attempt to demonstrate control by serving a page on the live hostname. Those are state-changing operations. If MUJ wants an end-to-end demonstration, the safe design is a synthetic label or sandbox resource owned by MUJ, with an explicit change ticket, rollback, and monitoring plan. A live CNAME can be used only for the read-only provider check if the letter expressly includes it.

## 6. Application to the MUJ SLCM Campaign

The following table distinguishes facts supplied in the brief from conclusions that follow from public Azure documentation.

| Campaign item | Status in the brief | Takeover relevance | Correct interpretation |
|---|---|---|---|
| Two dangling CNAMEs to `edtech366.azurewebsites.net` | Supplied live measurement, report-only | High: identifies the Azure App Service provider path | T0/T1 candidate; not provider proof |
| Provider-side claimability | Not verified | Decisive | The campaign must remain PARTIAL |
| 443 only reachable | Supplied measurement | Low to takeover proof | Limits the observed web surface; it does not say whether the Azure name is available |
| Verbose YSOD and `customErrors` off | Supplied measurement | Low to takeover proof; relevant to application disclosure | Separate web-application finding; do not combine it with DNS ownership |
| MVC antiforgery and cookie attributes | Supplied measurement | Low to takeover proof | Separate session and cookie-hardening issue; no evidence that it affects App Service name reservation |
| `trace.axd` and `elmah.axd` results | Supplied measurement | Low | Application paths, not provider-resource evidence |
| GET-only method behavior | Supplied measurement | Low | HTTP method policy does not answer provider claimability |
| Three-stage `enc` oracle | Supplied measurement | Low to takeover proof | Application input-processing issue; keep out of the takeover verdict |
| Clean host-header and proxy-header tests | Supplied measurement | Indirectly useful | Reduces one class of routing confusion, but does not test Azure ownership |
| No authentication and aggressive phase gated by letter and accounts | Supplied constraint | High for safety | Do not cross the gate; provider API work belongs after authorization |

The supplied target stack, Azure AS8075 attribution, Microsoft 365 identity, Entra-tenant count, HSTS state, TLS range, and edge-control observations should remain in the broader application report. They do not substitute for an App Service provider response. This is an inference from the evidence model: the Azure takeover criterion concerns the DNS-to-resource relationship, while the YSOD, MVC, cookie, method, and parameter observations concern application behavior.

The correct MUJ decision tree is short:

1. Preserve the existing T1 evidence without further probing.
2. Ask MUJ to confirm that the two CNAME records are within scope and to identify the subscription or tenant that historically owned the App Service resource, if known.
3. Use the Microsoft inventory tool or an equivalent client-side resource inventory to determine whether the organization still owns a corresponding resource. Microsoft's tool requires Azure subscription and Resource Graph read access for that owner-side correlation. [1]
4. With the signed letter and test accounts, perform the read-only provider availability check for the exact resource label and type.
5. If the provider says unavailable, report a stale or suspicious CNAME with no demonstrated cross-tenant claimability. If it says available, report a provider-side availability observation at the captured timestamp, without creating a resource or claiming the hostname.
6. If the API errors or the scope does not provide the necessary tenant/subscription context, report `unknown`, not `vulnerable`.

The two CNAMEs should not be called "taken over," "exploitable," or "confirmed vulnerable" on the present evidence. The strongest defensible language is: "Two DNS records point to an Azure App Service hostname associated with a suspected dangling-resource condition. Public and fingerprint evidence identify a candidate. Provider-side claimability was not tested; status remains PARTIAL." That wording is an inference from the supplied facts and the Azure evidence tiers, not a claim that the records are safe.

## 7. NO-TOOL GAPS and BUILD CANDIDATES

### NO-TOOL GAPS

**1. No general Azure end-to-end proof mode.** The mainstream detectors reviewed here compare DNS and HTTP evidence. Even the Azure-specific Nuclei template matches NXDOMAIN and Azure suffixes rather than calling a provider API. [17] The only public material located that explicitly checks Azure service-name availability is AzDanglingDnsFinder, whose README stops at "potentially vulnerable" and does not document a successful external binding. [10]

**2. Tenant and reservation state are invisible to public scanners.** App Service's cross-tenant reservation behavior is provider-side. A public scanner cannot infer the original tenant from a CNAME, and the presence or absence of a generic page does not expose that reservation state. Microsoft's documentation makes the tenant restriction explicit. [2]

**3. Custom-domain validation is a different state machine.** The default hostname's availability, the custom domain's `asuid` verification, and the DNS mapping are related but not identical. Azure recommends the TXT verification record to prevent another app from validating the domain. [2] A tool that reports only `nameAvailable` should not claim that an attacker can complete custom-domain validation.

**4. Evidence is not normalized.** Existing tools emit console text, CSV, JSON, logs, or template findings. [4] [6] [9] [14] There is no shared evidence schema that forces a scanner to record resolver context, API context, tenant, reason code, timestamp, and authorization reference together.

**5. Destructive actions are not consistently separated.** tko-subs documents optional takeover actions for GitHub Pages and Heroku and accepts credentials. [6] Most other tools are detection-only, but a user could still combine their output with a manual claim. A safe research tool should make live resource creation impossible by default and require an explicit, auditable sandbox mode.

**6. Provider coverage is asymmetric.** CNAME fingerprints are easy to add; authoritative provider checks require an adapter, authentication model, rate limits, naming rules, and rollback semantics. A single universal "takeover confirmed" label is therefore misleading across Azure, GitHub, Heroku, storage, CDN, and SaaS providers.

### BUILD CANDIDATES

| Candidate | Proposed function | Guardrails | Proposed output |
|---|---|---|---|
| `azure-claimability-readonly` | Call the documented App Service Check Name Availability API for a normalized label and resource type | Default deny; require scope-letter ID, allowlisted hostname, client tenant and subscription, read-only mode, no resource-creation permissions | JSON with target, normalized name, API version, `nameAvailable`, `reason`, `message`, UTC timestamp, redacted tenant/subscription, and authorization reference |
| `takeover-evidence-correlator` | Join authoritative DNS, bounded HTTP/TLS, fingerprint, and provider result | Preserve `unknown`; never convert a fingerprint into `confirmed`; hash bodies instead of retaining content | JSONL plus SARIF with one evidence object per observation and explicit evidence tier |
| `azure-owner-inventory` | Wrap the Microsoft dangling-DNS inventory and Resource Graph correlation for client-owned tenants | Reader-only role; no DNS write, App Service write, or custom-domain write permission | CSV and JSON mapping hostname, CNAME chain, owning subscription, resource type, and owner-side status |
| `provider-adapter-contract` | Define a common interface for name availability, resource existence, and domain verification | Each adapter must state whether its result is public, authenticated, tenant-scoped, or destructive | Versioned schema with `provider_signal_type` and `proof_limit` fields |
| `sandbox-proof-runner` | Test synthetic names in a MUJ-owned Azure sandbox rather than live brand names | Separate tenant or subscription, explicit change ticket, automatic teardown, no user traffic, and manual approval | Full run manifest, provider response, resource IDs, teardown evidence, and rollback status |
| `continuous-dangling-monitor` | Re-check approved DNS records and provider availability on a schedule | Rate limit, alert deduplication, credential rotation, retention limit, and owner notification | Time-series alert with first-seen, last-seen, and provider-response history |

The first candidate is the highest-value build for this campaign. It is small enough to review, maps directly to an official API, and can be made non-destructive. The second candidate prevents the exact reporting error that produced the PARTIAL state: it preserves the difference between a fingerprint and provider proof. The sandbox runner is useful for education, but it must never be repurposed to test the two live MUJ records without a new written authorization.

## 8. Synthesis and Comparative Analysis

| Strategy | Mechanism | Scope | Trade-off | Evidence strength for MUJ |
|---|---|---|---|---|
| Fingerprint scanner | DNS suffix, HTTP body, TLS, or NXDOMAIN matching | Broad, low credential burden | Fast and scalable, but provider state is inferred | T1 only; current PARTIAL |
| Microsoft owner inventory | Resource Graph and tenant/subscription correlation | Organization's own Azure estate | Strong owner-side context, but cannot prove outside claimability | Useful prerequisite, not final proof |
| Azure availability API | Authenticated provider name check | Exact provider name and resource type | Strongest non-destructive signal found, but still context- and type-dependent | T2 target; not yet run |
| Controlled sandbox binding | Approved resource creation and binding in client-owned environment | Narrow and high assurance | State-changing, requires rollback and change control | T3 only in a synthetic MUJ sandbox |
| Informal live claim attempt | Create or attach a resource to the target name | Live production target | Unsafe, potentially disruptive, and outside the current gate | Prohibited by this report |

The central tension is between breadth and proof. Fingerprint tools cover many services and can be run locally, but they are necessarily based on observable symptoms. The Azure API has narrower coverage and requires an authorized subscription context, but it tests the provider's own availability state. The Microsoft inventory tool has an opposite strength: it can show that MUJ still owns or no longer owns a related resource, yet it is not designed to show whether a stranger could claim the name. These strategies are complementary, not substitutes.

A second tension is between `nameAvailable` and custom-domain control. A positive name-availability response would be meaningful provider evidence, but it should not be overstated as proof that an external actor can immediately complete every step of custom-domain attachment. Azure's `asuid` guidance and tenant reservation rules show why. Conversely, a negative response would not prove that the DNS record is correctly managed; it would only show that the tested provider name was unavailable or invalid in that context.

### Auditable reasoning summary

I cannot provide private hidden chain-of-thought. The auditable reasoning chain used for this report is:

1. Start with the provider's definition of the threat: dangling DNS can route traffic to a resource in another subscription. [1]
2. Identify the missing proposition in the campaign: the brief has a CNAME and fingerprint evidence but no provider response.
3. Test the proposition against Azure's own reservation and TXT-verification controls, which show that CNAME appearance is not enough. [2] [15]
4. Review tool documentation and classify each tool by its actual mechanism. The reviewed scanners use fingerprints, while tko-subs documents limited GitHub/Heroku action capability, not Azure. [5] [6] [9] [17]
5. Select the documented Azure name-availability API as the least invasive provider-side check, while preserving its stated semantics and limitations. [19]
6. Apply the authorization boundary: passive evidence before approval, provider API only with the signed scope and test identities, and no live resource creation. [27] [27] [28]
7. Conclude that the existing status is PARTIAL, with high confidence in the status classification and deliberately low confidence about the underlying claimability until the provider check is run.

## VERDICT

**Verdict: PARTIAL - fingerprint/dangling-CNAME evidence only.**

**Confidence in this verdict: High.** The supplied campaign facts explicitly say that two CNAMEs point to `edtech366.azurewebsites.net` and that provider-side claimability was not verified. Public Azure documentation confirms that dangling CNAMEs can create takeover risk, but also documents tenant-based name reservation and domain-verification controls. [1] [2] The public tools reviewed do not fill that gap: the dominant behavior is DNS, HTTP, TLS, or fingerprint matching, and the one documented action-capable tool is limited to GitHub Pages and Heroku rather than Azure. [5] [6] [9] [17]

**Confidence about actual exploitability: Unknown, not high or low.** Nothing in the supplied measurements or public fingerprints establishes that another Azure subscription can obtain the name. A future authorized response of `nameAvailable: true` would be a strong T2 provider-side observation; an unavailable or ambiguous response would keep the result at unknown or suspicious rather than safe. The API's exact semantics and required OAuth/subscription context are documented by Microsoft. [19] [19]

**Safe pre-authorization:** passive public research, offline analysis, owner-provided DNS exports, and review of public tool and Azure documentation. A single DNS query or HTTP GET is low impact but still requires the owner's policy to permit active contact. Do not treat the club's possession of a hostname as authorization.

**Requires the signed scope letter and two test accounts:** active target probing beyond the already approved measurements, authenticated Azure API use, use of client tenant or subscription identifiers, `asuid` or custom-domain validation work, any DNS change, any App Service creation or deletion, any content hosting, and any attempt to demonstrate a live binding. The current report recommends only the authenticated, read-only provider availability request, followed by preservation of raw evidence and immediate stop.

**Required next evidence:** for each of the two CNAMEs, collect the full CNAME chain, authoritative DNS result, timestamp, authorized Azure subscription/tenant context, raw Check Name Availability response, and any existing `asuid` TXT state that MUJ authorizes the club to read. If any item is unavailable, report the result as `unknown` rather than upgrading the finding. Do not create or attach a live Azure resource merely to obtain a stronger screenshot.

## References

1. *Subdomain Takeover*. https://learn.microsoft.com/en-us/azure/security/fundamentals/subdomain-takeover
2. *Prevent Subdomain Takeovers - Azure App Service | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/app-service/reference-dangling-subdomain-prevention
3. *404 - Content not found*. https://learn.microsoft.com/en-us/rest/api/appservice/resource-provider/check-name-availability
4. *GitHub - punk-security/dnsReaper: dnsReaper - subdomain takeover tool for attackers, bug bounty hunters and the blue team! · GitHub*. https://github.com/punk-security/dnsReaper
5. *GitHub - PentestPad/subzy: Subdomain takeover vulnerability checker · GitHub*. https://github.com/PentestPad/subzy
6. *GitHub - anshumanbh/tko-subs: A tool that can help detect and takeover subdomains with dead DNS records · GitHub*. https://github.com/anshumanbh/tko-subs
7. *GitHub - haccer/subjack: DNS Takeover tool written in Go · GitHub*. https://github.com/haccer/subjack
8. *GitHub - Ice3man543/SubOver: A Powerful Subdomain Takeover Tool · GitHub*. https://github.com/Ice3man543/SubOver
9. *GitHub - cyber-ishita/takeoverspy: Subdomain Takeover Detection Tool - 50+ service fingerprints, CNAME chain analysis, and HTTP verification · GitHub*. https://github.com/cyber-ishita/takeoverspy
10. *GitHub - davidokeyode/AzDanglingDnsFinder: AzDanglingDnsFinder is a PowerShell script designed to identify DNS names that may be vulnerable to sub-domain takeover by checking if they point to Azure services that no longer exist or are not currently in use. The tool checks for dangling DNS records associated with Azure services like ApiManagement, WebApp, FrontDoor, and TrafficManager. · GitHub*. https://github.com/davidokeyode/AzDanglingDnsFinder
11. *nuclei-templates/http/takeovers at main · projectdiscovery/nuclei-templates · GitHub*. https://github.com/projectdiscovery/nuclei-templates/tree/main/http/takeovers
12. *Check Name Availability - REST API (Azure App Service) | Microsoft Learn*. https://learn.microsoft.com/en-us/rest/api/appservice/check-name-availability?view=rest-appservice-2025-03-01
13. *GitHub - tejassroot/subdomain-takeover-scanner: Python-based strict subdomain takeover detection framework focused on minimizing false positives through DNS validation, HTTP fingerprinting, SSL verification, and claimability checks. · GitHub*. https://github.com/tejassroot/subdomain-takeover-scanner
14. *GitHub - projectdiscovery/nuclei: Nuclei is a fast, customizable vulnerability scanner powered by the global security community and built on a simple YAML-based DSL, enabling collaboration to tackle trending vulnerabilities on the internet. It helps you find vulnerabilities in your applications, APIs, networks, DNS, and cloud configurations. · GitHub*. https://github.com/projectdiscovery/nuclei
15. *Set Up an Existing Custom Domain Name for Your App - Azure App Service | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/app-service/app-service-web-tutorial-custom-domain
16. *Introduction to Nuclei Templates*. https://docs.projectdiscovery.io/templates/introduction
17. *nuclei-templates/dns/azure-takeover-detection.yaml at main · projectdiscovery/nuclei-templates · GitHub*. https://github.com/projectdiscovery/nuclei-templates/blob/main/dns/azure-takeover-detection.yaml
18. *Running Nuclei*. https://docs.projectdiscovery.io/opensource/nuclei/running
19. *Check Name Availability - Check Name Availability - REST API (Azure App Service) | Microsoft Learn*. https://learn.microsoft.com/en-us/rest/api/appservice/check-name-availability/check-name-availability?view=rest-appservice-2026-07-15
20. *GitHub - martinvw/subdomain-takeover-tools: Some helper tools to validate subdomain takeovers · GitHub*. https://github.com/martinvw/subdomain-takeover-tools
21. *reclaimor · PyPI*. https://pypi.org/project/reclaimor/
22. *Azure-Network-Security/Cross Product/DNS - Find Dangling DNS Records/Readme.md at master · Azure/Azure-Network-Security · GitHub*. https://github.com/Azure/Azure-Network-Security/blob/master/Cross%20Product/DNS%20-%20Find%20Dangling%20DNS%20Records/Readme.md
23. *GitHub - AndyRace/DanglingDns · GitHub*. https://github.com/AndyRace/DanglingDns
24. *GitHub - bowligth/subtake: SubTake - subdomain takeover scanner (detection only) with a 44-service fingerprint database. by pdietzel · GitHub*. https://github.com/bowligth/subtake
25. *GitHub - fdzdev/Subdomain-Takeover-Checker: Python tool for detecting subdomain takeover vulnerabilities by resolving CNAME records and checking for known error messages. It supports bulk domain scanning and logs detailed results for analysis. · GitHub*. https://github.com/fdzdev/Subdomain-Takeover-Checker
26. *GitHub - EdOverflow/can-i-take-over-xyz: "Can I take over XYZ?" — a list of services and how to claim (sub)domains with dangling DNS records. · GitHub*. https://github.com/EdOverflow/can-i-take-over-xyz
27. *http://sei.cmu.edu/documents/1945/2017_003_001_503340.pdf*. http://sei.cmu.edu/documents/1945/2017_003_001_503340.pdf
28. *http://cisa.gov/vulnerability-disclosure-policy-template*. http://cisa.gov/vulnerability-disclosure-policy-template
