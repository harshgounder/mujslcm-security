# UAT Exposure in the MUJ SLCM Ecosystem

## Executive Summary

- **Application Identity**: The strongest public evidence identifies `uat.manipal.edu` as a user-acceptance deployment of the public MAHE institutional website, not as a student-lifecycle portal. The UAT shell displays MAHE branding, public navigation, campus and programme links, an `Apply Now` destination, and a branded error page [16]. **Inference, high confidence:** treat this host as a preproduction marketing/content frontend unless MAHE's internal asset inventory says otherwise -> assign it to the web-platform owner rather than presuming SLCM ownership.

- **Different Technology Shape**: The UAT HTML exposes `/_next/image` and `/_next/static` asset paths [16]. **Inference, high confidence:** those are Next.js deployment markers. They do not support the proposition that this UAT uses the requester's ASP.NET MVC 5.3, .NET Framework 4.x, and IIS 10 baseline for MUJ SLCM -> maintain separate threat models for the two applications.

- **Azure Front Door Confirmed**: Public DNS maps `uat.manipal.edu` to `uat-ci-mahe-ep-bzgfhcehh0fvhafs.a01.azurefd.net` [17]. A current resolver answer continued through Azure Front Door infrastructure to `150.171.109.183` [18], while the supplied observation named `150.171.110.195`. Microsoft describes Front Door as a global CDN and explicitly says it uses an anycast network [13] -> assess the hostname, Front Door profile, and origin controls, not a single changing edge address.

- **Not an Evidenced SLCM Mirror**: The actual MUJ portal publicly identifies itself as `WELCOME TO MUJ PORTAL`, offers sign-in and parent-login choices, and displays an MUJ email suffix [4]. MAHE's separate SLCM host presents `MU SLcM Sign in to your account` [12], while MAHE's public student-portal page links to `sis.manipal.edu/index.aspx` [2]. None of those identity or login cues appears in the reviewed UAT content -> reject the SLCM-mirror hypothesis unless owner-side architecture evidence reverses it.

- **Archive Presence Is Extensive**: A passive count of the returned Internet Archive CDX index found **1,811** successful-capture rows representing **1,322** unique URLs, with timestamps from **2022-12-07** through **2023-10-02** [15]. Route families such as `/mu`, medical and engineering institutions, programmes, faculty, campuses, news, and admissions describe a broad university publishing estate [15] -> assume historic UAT URLs and content remain discoverable even when current crawling is discouraged.

- **No Public Secret Leak Was Found**: The reviewed live pages show a generic MAHE-branded `Error 500`, but no stack trace, credentials, exception detail, or configuration value [9]. The archive filenames contained no exact matches for `web.config`, `appsettings*.json`, `.env`, source-map endings, SLCM, or login routes in the locally parsed index [15]. This is a bounded negative result, not proof of absence -> an authorized owner review is still required.

- **Crawler Policy Is Not Access Control**: `robots.txt` says `User-agent: * Disallow: /` [11], yet ordinary public routes and archived material remain available. The `/sitemap.xml` path returns the MAHE application/error shell rather than an XML sitemap [16] -> fix routing and indexing intentionally, but never rely on crawler instructions to protect UAT.

- **Production Data Remains Unknown**: No public page, archive filename, DNS record, or certificate entry demonstrates a production student database, shared SLCM backend, production credentials, or real student records. **Inference, high confidence about the evidence limit:** production-data use is unverified, not confirmed. **Conditional risk:** if real student or admissions data is present, the impact rises sharply because a publicly addressable UAT usually has broader engineering access and more change activity -> owner-side data lineage and access review is the decisive next step.

- **Highest-Value Control**: Microsoft says origins should block traffic that did not pass through Front Door because bypass can avoid WAF, DDoS, and other protections [7]. For public origins, Microsoft recommends both the `AzureFrontDoor.Backend` service tag and validation of the profile-specific `X-Azure-FDID` value [7]; Front Door Premium can instead use Private Link so the origin need not be publicly reachable [6] -> verify origin isolation before spending effort on cosmetic UAT labels.

**Decision-ready insight:** the public exposure is real, but the alarming interpretation is not yet evidenced. The defensible finding is a reachable MAHE web-platform UAT behind Azure Front Door, with current Next.js indicators, historic marketing-content archives, crawler/routing anomalies, and no observed secret or student-data disclosure. The correct response is an authorized configuration and data-governance review, not external testing.

## Scope, Safety, and Evidence Method

This report uses only public, passive sources observed on **2026-08-25**: DNS-over-HTTPS answers, certificate-transparency records, normal unauthenticated page retrieval, search indexing, standard `robots.txt` and `sitemap.xml` locations, the Internet Archive CDX index, and vendor or standards documentation. No login was attempted; no credentials were entered; no forms were submitted; no directory brute force, parameter fuzzing, port scan, origin discovery, bypass attempt, or vulnerability exploitation was performed.

I cannot provide private chain-of-thought. Instead, the report exposes an auditable evidence-to-conclusion rationale. Each conclusion below separates observation, inference, uncertainty, and the owner action that could resolve that uncertainty.

### Table 1. Evidence standard and research boundaries

| Evidence class | What was used | What it can establish | What it cannot establish |
|---|---|---|---|
| Direct public DNS | CNAME and A-chain responses for the exact hostname [17][18] | Current public routing through an Azure Front Door name | The private origin, resource group, subscription, WAF policy, or backend data source |
| Direct public content | MAHE UAT pages, `robots.txt`, and `sitemap.xml` [9][11][16] | Visible branding, routes, error handling, and frontend markers | Database contents, internal APIs, source code, secrets, or authorization correctness |
| Separate first-party portals | MUJ Portal, MAHE SLCM, and MAHE Student Portal pages [4][12][2] | Public names, destinations, and login presentation | Shared code, shared databases, or shared identity tenants behind the pages |
| Historical inventory | Internet Archive CDX output for `uat.manipal.edu/*` [15] | Archive presence, capture timestamps, and captured URL names | Completeness of all historical content or whether archived pages represented production data |
| Certificate transparency | Dedicated `uat.manipal.edu` certificate records [5] | Public certificate issuance and continuity of hostname use | Application ownership, data sensitivity, or security posture |
| Authoritative guidance | Microsoft Front Door and NIST publications [7][6][14] | Appropriate defensive baselines | Whether MAHE has actually implemented those controls |

The requester's MUJ SLCM technology description is treated as a supplied scope baseline, not as a finding reproduced here. That distinction matters. A statement such as "MUJ SLCM uses ASP.NET MVC" does not transfer to another hostname merely because both are under `manipal.edu`. Likewise, Microsoft 365-related DNS on the MUJ mail domain demonstrates Microsoft-hosted mail integration, not automatically the identity provider used by the UAT application: MUJ's MX points to Outlook protection [20], while DKIM selectors point into an `onmicrosoft.com` tenant [21][22]. **Inference, high confidence:** mail-tenant evidence is insufficient to attribute UAT authentication, especially when the UAT page presents no SLCM sign-in.

## Azure Front Door Exposure and Current Reachability

The DNS result is unambiguous. `uat.manipal.edu` CNAMEs to `uat-ci-mahe-ep-bzgfhcehh0fvhafs.a01.azurefd.net` [17]. In the current resolver response, that name chained through `mr-a01.tm-azurefd.net` and returned `150.171.109.183` [18]. The supplied input instead recorded `150.171.110.195`. Microsoft says Front Door distributes static and dynamic web content through a global edge network and accelerates traffic with an anycast network [13]. **Inference, high confidence:** the differing addresses are compatible with a time-, resolver-, or edge-dependent service and do not show a contradiction or migration by themselves.

### Table 2. Edge and reachability facts

| Question | Public observation | Assessment | Confidence |
|---|---|---|---|
| Does the hostname exist? | The CNAME answer is present and successful [17] | Yes | High |
| Is Azure Front Door in the path? | The canonical name ends in `a01.azurefd.net` [17] | Yes | High |
| Is one IP a stable asset identifier? | The supplied IP and current resolver IP differ; Front Door uses anycast [18][13] | No | High |
| Is HTTPS naming intentional? | CT shows certificates specifically for `uat.manipal.edu`, including May 2026 certificates valid to November 2026 [5] and December 2025 certificates valid to June 2026 [5] | Yes, the hostname is operationally maintained | High |
| Is the application healthy? | Reviewed public UAT routes returned a branded `Error 500` shell [9] | At least some paths are failing or deliberately falling back; root/origin health cannot be inferred | Moderate |
| Is the origin exposed directly? | No origin hostname or address is present in the reviewed public evidence | Unknown | Low |

**Case study - why the edge is not the origin.** The CNAME discloses the Front Door endpoint, not the private application server. That distinction is protective only if requests cannot bypass Front Door. Microsoft explicitly warns that bypassed traffic might avoid Front Door's WAF, DDoS protection, and other controls [7]. Therefore, merely seeing an Azure Front Door hostname is not evidence that the backend is isolated.

For a public-IP origin, Microsoft recommends two controls together: accept only the `AzureFrontDoor.Backend` service tag and validate that `X-Azure-FDID` matches the organization's Front Door profile [7]. The documentation warns that IP filtering alone is insufficient because other Azure customers share Front Door backend address space [7]. **Inference, high confidence:** owner verification of those two conditions is more security-relevant than tracking the edge IP shown by DNS.

## What Application Does UAT Front?

The public content answers this more strongly than the hostname label. The `/sitemap.xml` request does not return a list of URLs. It returns a MAHE-branded application shell with the title "Top Higher Education Institution in India | Manipal University (MAHE)," an MAHE logo, `Apply Now`, navigation for institutional content, campuses, programmes, and footer policies [16]. It also contains the branded failure language `Oops`, `Error 500`, and "This page has taken a study break" [16]. A separately reviewed UAT marketing route has the same MAHE identity, the same `Apply Now` link, and the same generic error treatment [9].

### Table 3. Application-identity evidence

| Signal | Observed value | Interpretation |
|---|---|---|
| Brand | MAHE/Manipal University [16] | First-party institutional web property |
| Main content model | About, programmes, campuses, research, admissions, and policy/navigation links [16] | Public marketing and publishing frontend |
| Primary conversion | `Apply Now` points to `apply.manipal.edu` [9] | Admissions journey, not student lifecycle management |
| Error treatment | Branded generic `Error 500` shell [9] | Application-level or routing fallback; not a verbose developer exception |
| Authentication cues | No SLCM, student-login, parent-login, or account prompt in the reviewed UAT shell [16] | No public evidence of an authenticated SLCM surface |
| Frontend asset pattern | `/_next/image` and `/_next/static/media/...` [16] | **Inference, high confidence:** Next.js frontend |
| Media delivery | The logo is loaded through a separate `a01.azurefd.net` media-route host [16] | **Inference, moderate confidence:** decoupled media delivery; CMS product and origin remain unknown |

**Case study - the misleading sitemap.** A valid sitemap path normally returns sitemap data, but this UAT path returns the normal application/error shell [16]. The page also exposes Next.js-style assets [16]. **Inference, high confidence:** a catch-all frontend route or error handler is serving an HTML application where XML was expected. That is a quality and observability issue, but it is not a secret leak.

The historical footprint reinforces the application classification. Captured route families include MAHE-level pages and named institutions such as medical, engineering, pharmacy, nursing, architecture, and information-science properties, along with programmes, faculty, campuses, and news [15]. **Inference, high confidence:** the UAT host historically staged a broad university content estate. Nothing in those route families resembles grade entry, attendance, fee ledgers, course registration, parent access, or another core SLCM workflow.

The exact backend remains unknown. The public evidence does not identify a database engine, headless CMS product, source repository, API-management layer, server runtime behind Next.js, or whether rendering is static, server-side, or hybrid. The safe conclusion is narrower: **the public frontend is consistent with a MAHE institutional-web UAT and has current Next.js markers.** Attributing ASP.NET MVC, IIS, Adobe Experience Manager, Strapi, or any other origin technology would exceed the evidence.

## UAT Versus MAHE and MUJ SLCM

Three separately named student-facing destinations are publicly visible. The MUJ portal at `mujslcm.jaipur.manipal.edu/Home/Index` says `WELCOME TO MUJ PORTAL`, displays a sign-in flow and a parent-login choice, and shows an MUJ email suffix [4]. The MAHE SLCM host at `slcm.manipal.edu` says `MU SLcM Sign in to your account` [12]. Separately, MAHE's public Student Portal page sends users to `https://sis.manipal.edu/index.aspx` [2]. These are not minor route variants under `uat.manipal.edu`; they are distinct hostnames and publicly distinct experiences.

### Table 4. Exact public comparison

| Dimension | `uat.manipal.edu` | MUJ portal | MAHE SLCM | MAHE Student Portal |
|---|---|---|---|---|
| Public purpose | MAHE institutional content, programmes, campuses, admissions [16] | MUJ account and parent sign-in [4] | SLCM account sign-in [12] | Directory page linking to SIS [2] |
| Login visible | No in reviewed shell | Yes | Yes | Link-out rather than embedded login |
| Brand text | MAHE/Manipal University [16] | MUJ Portal [4] | MU SLcM [12] | Student Portal [2] |
| Frontend clue | `/_next/` assets [16] | Requester-supplied ASP.NET MVC baseline was not revalidated | Backend not inferred from visible text | Destination path ends in `index.aspx` [2] |
| Edge evidence | Azure Front Door CNAME [17] | Not assessed here | Not assessed here | Not assessed here |
| Evidence of shared data | None | None from public page | None from public page | None from directory page |

**Inference, high confidence:** `uat.manipal.edu` does not publicly mirror MUJ SLCM or MAHE SLCM. This is not a proof that no internal API, identity tenant, or database is shared. It means the mirror hypothesis lacks positive public evidence and conflicts with the visible application roles.

Microsoft-related DNS must also be interpreted narrowly. The MUJ domain has an Outlook-protection MX record [20] and DKIM aliases into a named `onmicrosoft.com` tenant [21][22]. That is strong evidence for Microsoft 365 mail service. It does not prove that the MAHE marketing UAT accepts Microsoft identities, that it uses the same tenant, or that SLCM tokens are valid there. **Inference, high confidence:** identity federation, app registrations, redirect URIs, token audiences, and conditional-access policy remain owner-only facts.

The operational implication is separation. The club should maintain at least two models: one for a public Next.js/institutional-content UAT behind Front Door, and one for authenticated student-lifecycle systems under their own hostnames. Combining them would create false positives, such as treating an admissions link as SLCM integration, and false negatives, such as applying only IIS hardening to a Next.js deployment.

## Public Artifacts, Archives, and Configuration-Leak Review

The review found public operational metadata, but not a credential or configuration disclosure. DNS reveals the Azure Front Door endpoint [17]. CT reveals that the organization has repeatedly obtained certificates for the labeled UAT hostname [5]. The HTML exposes normal public asset and route names, including `/_next/` paths [16]. `robots.txt` disallows all crawling [11]. The sitemap location returns branded HTML rather than XML [16]. These facts enlarge the public footprint, but none is a secret by itself.

### Table 5. Artifact and leak assessment

| Artifact class | Result | Security meaning | Confidence and limit |
|---|---|---|---|
| Verbose exception or stack trace | Not observed; only generic `Error 500` branding [9] | No direct framework path, source file, query, or credential disclosure in reviewed content | Moderate; only sampled public pages |
| Configuration files | No exact archive-name match for `web.config`, `appsettings*.json`, `.env`, or common config-file forms in the locally parsed CDX inventory [15] | No public configuration leak found | Moderate; filename and index review is not exhaustive content inspection |
| Source maps | No filename ending in `.map` in the locally parsed CDX inventory [15] | No archived source-map filename found | Moderate; current asset manifests were not probed |
| API documentation | Search results did not identify UAT-specific Swagger or API documentation; reviewed pages show marketing content | No public API-doc evidence | Low to moderate; negative search result is weak evidence |
| Secrets or personal records | No credentials, tokens, keys, connection strings, student records, or admissions records observed [9][16] | No confirmed confidentiality incident | Moderate for reviewed pages only |
| Crawler policy | `User-agent: * Disallow: /` [11] | Requests voluntary crawler exclusion | High; it does not provide authorization |
| Sitemap behavior | HTML error/application shell instead of XML [16] | Routing or deployment-quality anomaly; not a secret leak | High for observed response |
| Certificate history | Dedicated UAT certificates logged in 2025 and 2026 [5] | Persistent, intentionally TLS-enabled hostname | High |
| Archive presence | 1,811 successful rows, 1,322 unique URLs, 2022-12-07 to 2023-10-02 in the returned CDX data [15] | Historic content and routes remain discoverable | High for this CDX response; no independent count source |

**Archive calculation note:** the counts above were computed locally from the public CDX JSON by counting returned capture tuples and then de-duplicating the original-URL field. The query already filtered for HTTP 200 and collapsed identical digests. This is reproducible from the exact CDX URL in References, but it is still one archive provider's inventory rather than an independent census.

**Case study - branded 500 versus verbose failure.** The UAT response identifies MAHE and reports a server-style failure, but it does not expose exception class names, stack frames, filesystem paths, SQL text, environment variables, or configuration values [9]. That is materially safer than a developer exception page. However, repeated generic 500 responses can still create availability, monitoring, search-index, and deployment-confidence concerns. **Inference, moderate confidence:** the error is a reliability signal, not evidence of exploitable information disclosure.

The correct wording is therefore "no public config or secret leak found in the bounded review," not "the UAT has no leaks." An exhaustive conclusion would require authorization, a defined asset inventory, authenticated roles, source and pipeline review, and owner-side cloud configuration. This report deliberately does not provide instructions for external enumeration or access.

## Production-Data Risk Model

Public OSINT cannot see a private database connection. No reviewed artifact establishes that UAT contains production student data, copies a production SLCM database, uses production API credentials, or shares production storage. Conversely, absence of a public leak cannot establish clean data separation. The question is therefore a governance and architecture uncertainty, not a discovered breach.

NIST Cybersecurity Framework Version 1.1 states in PR.DS-7 that development and testing environments are separate from production [14]. NIST also frames privacy management as an enterprise-risk activity intended to protect individuals [3]. Those principles fit this case because student, parent, applicant, staff, academic, and financial records can create privacy and operational consequences if copied into a lower environment. **Inference:** the categories in the next table are risk scenarios, not claims about MAHE's actual data.

### Table 6. Conditional production-data scenarios

| Scenario | Public evidence for it | Likelihood assessment | Impact if true | Owner-side decision test |
|---|---|---|---|---|
| Public marketing content only | Strong: MAHE navigation, programmes, campuses, and `Apply Now` [16] | Most consistent with evidence | Low to medium | Inventory databases and APIs attached to the UAT deployment |
| Copy of production CMS content | Historic breadth and current branded content make this plausible [15][16] | Plausible, unverified | Medium if content includes drafts, contacts, unpublished research, or internal metadata | Review CMS space, export jobs, media metadata, and publication workflow |
| Production applicant or lead data | `Apply Now` links to a separate host rather than showing data locally [9] | No supporting evidence | High if forms or integrations return real applicant records | Trace UAT form destinations, queues, CRM connectors, and test accounts |
| Production SLCM/student database clone | UAT lacks SLCM login cues, while SLCM uses separate hosts [4][12][2] | Unsupported by public evidence | Critical if grades, attendance, fees, identity data, or parent records are present | Compare connection inventories and data classifications; inspect record provenance under authorization |
| Shared production identity app | MUJ has Microsoft 365 mail DNS, but UAT shows no identity flow | Unknown | High if redirect URIs, secrets, or token audiences cross environments | Review Entra app registrations, service principals, redirect URIs, credentials, and conditional access |
| Shared production secrets or storage | No public config values or keys observed [9] | Unknown | High to critical | Review Key Vault references, managed identities, environment variables, storage accounts, and rotation history |
| Publicly reachable origin behind Front Door | Edge use is confirmed, but origin identity is not [17][18] | Unknown | High if origin bypasses WAF or access policy | Verify Private Link or combined service-tag and `X-Azure-FDID` controls [7] |

The key mechanism is access asymmetry. UAT often changes more frequently and may be accessible to developers, vendors, content authors, testers, and automation. **Inference:** if production data is copied into that environment, the number of people and components able to reach the data can increase even when the production application remains well controlled. The response should be data minimization and separation: synthetic data by default; irreversible de-identification or carefully governed masking only when realistic records are necessary; separate encryption boundaries and credentials; and expiration of test datasets.

A second mechanism is integration drift. A marketing frontend can call admissions, CRM, analytics, media, search, or identity services without being an SLCM clone. **Inference:** the highest realistic data risk may be a shared integration credential or lead-data pipeline rather than a full student database. This is why owner-side data-flow mapping is more useful than guessing from the public framework.

A third mechanism is cache persistence. Front Door and downstream caches can retain responses according to configured behavior. No reviewed source shows sensitive UAT caching, so this is only a conditional concern. The owner should verify that authenticated or personal-data responses are never publicly cached and that cache keys do not mix users or environments.

## Defensive Control Plan for Authorized Owners

The following plan is for MAHE/MUJ asset owners or an explicitly authorized security team. It does not instruct the club to test controls from outside. Microsoft says origins should reject traffic that did not come through Front Door [7]. It recommends Private Link for supported Front Door Premium deployments [7][6], or combined backend service-tag filtering and profile-specific `X-Azure-FDID` verification for public origins [7].

### Table 7. Prioritized owner actions

| Priority | Owner action | Evidence or mechanism | Completion evidence |
|---|---|---|---|
| P0 | Identify the authoritative owner, subscription, Front Door profile, routes, origin groups, WAF policy, and deployment pipeline for `uat.manipal.edu` | DNS proves the Front Door endpoint but not the origin [17] | Signed asset record and architecture diagram |
| P0 | Prove origin isolation | Direct-origin traffic can bypass Front Door controls [7] | Private Link approval and public-origin closure, or service-tag filtering plus exact `X-Azure-FDID` validation [7] |
| P0 | Classify every UAT datastore and integration | Production-data status is publicly unknowable | Data-flow map with owner, classification, source, retention, and legal basis |
| P0 | Remove production personal data unless formally justified | NIST calls for test/production separation [14] and privacy-risk management [3] | Synthetic-data proof or approved de-identification record; no untracked production extracts |
| P1 | Separate UAT identities and secrets from production | Cross-environment credentials turn a UAT compromise into a production path | Distinct managed identities, app registrations, vault entries, keys, scopes, and rotation records |
| P1 | Gate UAT according to business need | Public reachability is confirmed [17][16] | Approved exposure decision; preauthentication, network restriction, or documented public-content exception |
| P1 | Repair error and fallback routing | Branded 500 pages and HTML at `/sitemap.xml` reduce quality and obscure fault origin [9][16] | Correct status codes, valid sitemap or deliberate 404, and monitored error budget |
| P1 | Treat `robots.txt` only as crawler guidance | It currently disallows all crawling [11] | Real authorization at edge/app; indexing policy documented separately |
| P1 | Review cache and response-header policy | Front Door is a CDN for static and dynamic content [13] | Tests performed by the owner showing no caching of authenticated or personal responses |
| P2 | Review public artifact publication in CI/CD | Next.js assets and historical routes are readily discoverable [16][15] | Build checks for secrets, source maps, debug flags, manifests, and unintended files |
| P2 | Monitor CT, DNS, WAF, origin, and application errors | CT demonstrates continuing certificate issuance [5] | Alerting tied to named owners and incident runbooks |
| P2 | Set a retirement or promotion policy | A long-lived labeled UAT has certificates and archive history [5][15] | Time-bound exception, promotion date, or decommission record |

**Case study - Private Link versus public origin.** With Front Door Premium, Private Link connects Front Door to supported origins over a private endpoint and removes the need for the origin to be publicly accessible [6]. It does not make the client-to-Front-Door path private, and Microsoft documents limitations, including unsupported origin types and no client or mutual TLS support at Front Door [6]. The architectural choice therefore depends on origin type and tier, but the security objective is constant: the origin should not accept arbitrary Internet traffic.

**Recommendation:** do not make "UAT" in the hostname the control boundary. Labels inform humans; they do not authenticate users, segregate data, or isolate origins. The enforceable boundaries are Front Door/WAF routing, origin network policy, application authorization, environment-specific identity and secrets, and controlled data movement.

## Synthesis

### Table 8. Cross-cutting comparison

| Dimension | MAHE marketing UAT | MUJ/MAHE SLCM surfaces | Azure Front Door control plane | Archive/OSINT layer |
|---|---|---|---|---|
| Primary mechanism | Public content delivery and admissions navigation [16] | Authenticated student or parent access [4][12] | Global edge routing/CDN [13] | Historical URL and content discovery [15] |
| Public technology signal | Next.js-style assets [16] | Distinct login presentations; requester baseline not transferred | Anycast edge and profile-specific origin headers [13][7] | Captured route names, not backend architecture |
| Main risk | Deployment errors, overexposure, shared integrations, accidental publication | Account, academic, financial, parent, and identity impact if compromised | Origin bypass if backend accepts non-Front-Door traffic [7] | Persistence of old paths and content |
| Evidence base | Direct UAT pages | Direct first-party portal pages | Microsoft documentation plus DNS | Internet Archive CDX |
| Major unknown | Backend/CMS, origins, data stores, auth, integrations | Shared backend or identity relationships | Actual WAF, Private Link, service-tag, and FDID configuration | Completeness and deleted/non-200 content |
| Time horizon | Current deployment plus staged redesigns | Ongoing operational systems | Continuous configuration | 2022-2023 captures in reviewed index |
| Decision | Treat as its own web platform | Do not conflate with UAT without architecture proof | Verify origin isolation first | Assume historical discoverability |

The non-obvious tension is that the hostname is more alarming than the content. `uat.manipal.edu` is clearly labeled and publicly routable, but its visible application is an institutional marketing shell, not SLCM. Conversely, a marketing UAT can still create production impact through shared identity, CRM, media, search, analytics, secrets, or origin infrastructure even without displaying a student login. **Inference:** application identity lowers the likelihood of a full SLCM database mirror but does not eliminate cross-environment integration risk.

A second tension is between crawler exclusion and durable discoverability. The current `robots.txt` asks all compliant crawlers to stay out [11], yet the archive holds a large historical URL inventory [15], and CT permanently records certificate issuance [5]. The mechanism is simple: crawler policy is prospective, voluntary, and not retroactive. **Implication:** security must not depend on search invisibility, and decommissioning should include data, routes, certificates, caches, and archive-aware disclosure review.

A third tension is between a managed edge and an unknown origin. Azure Front Door can improve availability and protection [13], but Microsoft warns that an unrestricted origin can bypass those benefits [7]. **Recommendation:** owner-side proof of origin isolation, data separation, and credential separation should determine the final risk rating.

## VERDICT

**VERDICT: Publicly reachable MAHE institutional-web UAT behind Azure Front Door; not publicly evidenced as an MAHE or MUJ SLCM mirror. Overall confidence: High for edge and application identity, Moderate for the bounded no-leak assessment, and Low for any conclusion about private production data.**

### Table 9. Final confidence and risk judgment

| Finding | Verdict | Confidence |
|---|---|---|
| Azure Front Door routing | Confirmed by CNAME and current A-chain [17][18] | High |
| Application fronted | MAHE public institutional/marketing and admissions frontend [16] | High |
| Current frontend family | **Inference:** Next.js, based on `/_next/` assets [16] | High |
| Exact origin stack and CMS | Not publicly determined | Low |
| Mirrors MUJ or MAHE SLCM | No supporting public evidence; visible purpose and hosts differ [4][12][2] | Moderate-high |
| Public configuration or secret leak | None found in bounded live, search, and archive review [9][15] | Moderate, not exhaustive |
| Archive presence | Confirmed and extensive [15] | High |
| Uses production student data | Unknown; no public evidence either way | Low |
| Current risk rating | **Analyst inference: Medium**, driven by public UAT exposure, persistent archive footprint, and unknown origin/data controls | Moderate |
| Escalation condition | **Analyst inference: High to Critical** if owner review confirms production personal data, shared production secrets/identity, or a bypassable origin | Conditional |

No discovered fact justifies claims of a breach, exposed student records, or an exploitable vulnerability. The most responsible next step is a confidential, authorized owner review using the P0 controls in Table 7. The club should report the evidence and uncertainty exactly as stated, avoid accessing anything beyond normal public content, and allow MAHE/MUJ administrators to validate private architecture and data lineage.

## References

1. *SP 800-53 Rev. 5, Security and Privacy Controls for Information Systems and Organizations | CSRC*. https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
2. *Student Portal Login- MAHE (Manipal Academy Of Higher Education)*. http://manipal.edu/mu/academics/student-portal.html
3. *Privacy Framework | NIST*. https://www.nist.gov/privacy-framework
4. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
5. *crt.sh | uat.manipal.edu*. https://crt.sh/?q=uat.manipal.edu
6. *Secure your Origin with Private Link in Azure Front Door Premium | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/frontdoor/private-link
7. *Secure traffic to origins - Azure Front Door | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/frontdoor/origin-security
8. *How To Apply*. http://uat.manipal.edu/muj/admission/international-students/how-to-apply.html
9. *uat.manipal.edu*. http://uat.manipal.edu/mu.html
10. *MAHE - Manipal Academy of Higher Education, Admissions open for 2026 (Formerly Manipal University)*. https://www.manipal.edu/mu.html
11. *uat.manipal.edu*. https://uat.manipal.edu/robots.txt
12. *MU SLcM*. https://slcm.manipal.edu/
13. *http://learn.microsoft.com/en-us/azure/frontdoor/front-door-overview*. http://learn.microsoft.com/en-us/azure/frontdoor/front-door-overview
14. *Framework for Improving Critical Infrastructure Cybersecurity, Version 1.1*. https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.04162018.pdf
15. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=uat.manipal.edu%2F*&output=json&filter=statuscode%3A200&fl=timestamp%2Coriginal%2Cstatuscode%2Cmimetype%2Cdigest&collapse=digest
16. *uat.manipal.edu*. https://uat.manipal.edu/sitemap.xml
17. *dns.google*. http://dns.google/resolve?name=uat.manipal.edu&type=CNAME
18. *dns.google*. http://dns.google/resolve?name=uat.manipal.edu&type=A
19. *Top Higher Education Institution in India |Manipal University (MAHE)*. https://uat.manipal.edu/
20. *http://dns.google/resolve?name=jaipur.manipal.edu&type=MX*. http://dns.google/resolve?name=jaipur.manipal.edu&type=MX
21. *http://dns.google/resolve?name=selector2._domainkey.jaipur.manipal.edu&type=CNAME*. http://dns.google/resolve?name=selector2._domainkey.jaipur.manipal.edu&type=CNAME
22. *http://dns.google/resolve?name=selector1._domainkey.jaipur.manipal.edu&type=CNAME*. http://dns.google/resolve?name=selector1._domainkey.jaipur.manipal.edu&type=CNAME
