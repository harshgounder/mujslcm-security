# MUJ SLCM Azure Control-Plane Research Plan

## Executive Summary

- **Campaign Status Is Correctly Absent**: The supplied measurements establish application-layer behavior, but they do not establish an App Service resource, storage account, deployment slot, Kudu site, Easy Auth configuration, managed identity, subscription, or responsible Entra tenant. App Service Kudu, when present, is a companion application with its own SCM hostname and authorization boundary [9]. -> Record the Azure control-plane campaign as **ABSENT**, not negative, until the resource owner supplies identifiers and scope.

- **Hosting Attribution Is The First Decision Gate**: The brief places the public address in Microsoft AS8075 and identifies IIS and ASP.NET, but those observations are compatible with several Azure architectures. **Inference:** they do not prove Azure App Service. -> Obtain an owner-supplied resource ID, subscription ID, resource group, hosting service, production slot name, and tenant mapping before testing App Service-specific hypotheses.

- **Kudu Is A High-Impact Separate Plane**: Kudu can expose app settings, connection strings, environment variables, diagnostic material, process controls, deployment functions, and a REST API [9]. Access through Entra requires a role containing `Microsoft.Web/sites/publish/Action` [9]. -> Do not probe or authenticate to a guessed SCM hostname before authorization; after authorization, begin with configuration and RBAC review rather than shell or file access.

- **Deployment Credentials Need Configuration-First Review**: App Service has user-scope credentials covering a user's Azure account and app-scope credentials limited to one app [21]. Basic publishing authentication is less secure and is disabled by default for new apps [21]. -> Audit whether SCM and FTP basic publishing are allowed, who can retrieve publishing profiles, and whether CI/CD uses workload identity before retrieving any credential.

- **SAS Has A Built-In Accountability Gap**: Azure supports user-delegation, service, and account SAS; Microsoft prefers user-delegation SAS because it is secured with Entra credentials [13]. Azure cannot audit SAS generation or report how many SAS tokens exist [13]. -> Treat source/configuration scanning, short expiry, least privilege, HTTPS, stored access policies where applicable, and token-use logging as one control set rather than relying on a token inventory.

- **Slots Expand The Estate**: Deployment slots are live applications with their own hostnames, and content and configuration can be swapped with production [11]. Some settings move during a swap while slot-specific settings remain in place [11]. -> Inventory every slot, its hostname, SCM policy, identity, access restrictions, secrets, logging, and sticky settings; do not assess only the production custom domain.

- **Easy Auth And Managed Identity Are Independent Trust Boundaries**: Easy Auth handles provider sign-in, session management, token validation/storage, and identity-header injection outside application code [24]. Managed identity configuration is slot-specific, and its tokens represent the application rather than an end user [20]. -> Use two approved accounts to test authorization differences, but assess managed identity through owner-provided configuration and effective-role data, not token theft or SSRF.

- **Detection Must Precede Validation**: Azure Activity Log covers control-plane operations but normally omits reads and retains events for 90 days [18]. Blob data access requires resource logs, while SCM basic-auth attempts can be sent to `AppServiceAuditLogs` [16][19]. -> Enable and verify diagnostic destinations before any active phase so a clean result is meaningful.

- **Authorization Has Two Layers**: Microsoft does not require its own pre-approval for tests against customer-controlled Azure resources, but testers must follow Microsoft's rules [1]. That policy does not grant permission from MUJ or Manipal. -> Require the signed asset-owner letter and named test accounts; require a separate change-window addendum for credential retrieval, token use, data writes, deployment, or slot swaps.

## 1. Scope, Evidence Status, And Auditable Reasoning

### 1.1 What the supplied measurements establish

The engagement brief reports that, on **2026-09-13**, only TCP 443 was reachable; the site produced verbose ASP.NET error behavior; antiforgery was enforced; the antiforgery cookie lacked `Secure`; `trace.axd` returned 403; `elmah.axd` returned 404; two error families were measured; non-GET methods were rejected; and `enc` behaved as a three-stage error oracle. It also reports clean Host, `X-Forwarded-Host`, absolute-URI, and trust-based error-bypass attempts. These are treated here as **engagement data supplied by the requester, not independently verified public facts**.

Those observations are relevant to the web application, but none demonstrates control-plane access. The `enc` oracle indicates distinguishable application error paths; it does not, by itself, show access to keys, Key Vault, Storage, Kudu, ARM, or a managed identity. The method policy observed on the custom domain does not describe a separate SCM companion site. Likewise, a clean result for host-header variants does not prove that Front Door, Application Gateway, a reverse proxy, or an App Service access restriction is absent.

### 1.2 Evidence-to-decision ledger

This table provides an auditable reasoning summary rather than private internal chain-of-thought.

| Evidence | Classification | Supported conclusion | Unsupported leap | Decision |
|---|---|---|---|---|
| AS8075, IIS 10, ASP.NET MVC/.NET | Supplied measurement | Microsoft-hosted network presence and a Windows web stack are plausible | "The application is definitely Azure App Service" | Obtain owner-side resource attribution first |
| Microsoft 365 identity and three Entra tenants | Supplied measurement | Several identity authorities may be relevant | Which tenant owns the app registration, subscription, or managed identity | Request a tenant-to-resource map |
| No authenticated session occurred | Supplied measurement | No authenticated role or tenant boundary has been tested | Any conclusion about Easy Auth, RBAC, slots, or managed identity | Preserve **ABSENT** status |
| No HSTS and TLS 1.0-1.3 reportedly offered | Supplied measurement plus platform guidance | Transport hardening needs review; App Service guidance recommends minimum TLS 1.2 or higher and separate web/SCM configuration [6] | That the setting is controlled by App Service rather than another component | Identify the terminating resource, then remediate there |
| Verbose YSOD and stable response lengths | Supplied measurement | Existing captures may contain useful architecture clues | Permission to generate additional fault conditions or seek secrets | Review existing captures offline before authorization |
| Clean host-trust tests | Supplied measurement | The tested variants produced no visible bypass | No edge, no alternate hostname, or no SCM site | Do not convert a narrow negative into an estate-wide negative |

**Decision-ready insight:** the first control-plane action should not be a scan. It should be an owner-assisted attribution package. Without it, an App Service campaign risks testing guessed Microsoft-hosted assets that may not belong to the portal.

## 2. Authorization And Safety Boundary

Microsoft's Azure guidance says Microsoft pre-approval is no longer required for a customer's Azure penetration test [1]. Microsoft's unified Rules of Engagement apply to Microsoft-owned or managed online assets and impose testing constraints [4]. Neither statement substitutes for authorization from the owner of `mujslcm.jaipur.manipal.edu`.

| Tier | Prerequisite | Permitted work for this project | Explicitly excluded |
|---|---|---|---|
| **A - Safe pre-authorization** | None beyond lawful public access | Read public documentation; analyze the supplied captures offline; inspect public DNS and certificate-transparency records through passive databases; search public code and documentation for already-published Azure hostnames; run secret scanners only against club-owned copies of demonstrably public repositories; develop rules against synthetic data | Guessing storage accounts or containers; requesting candidate SCM/slot hosts; SAS replay; login attempts; tenant enumeration; automated scanning of MUJ assets; accessing nonpublic data |
| **B - Letter required** | Signed letter naming domains, Azure resource types, IP/source ranges, dates, rate limits, contacts, data-handling terms, and stop conditions | Low-rate validation of approved public Azure endpoints; narrowly scoped cloud-enumeration templates; response fingerprinting; approved anonymous-access checks that do not list or download objects; telemetry verification | Password spraying; credential use; storage listing or object retrieval unless explicitly written into scope; Kudu authentication; resource changes |
| **C - Letter plus two test accounts** | Tier B plus two named accounts in documented tenants and expected roles | Differential Easy Auth testing; read-only ARM/Graph inventory; slot and identity enumeration; RBAC comparison; review of SCM/FTP policy; review of storage public-access, Shared Key, SAS-policy, network, logging, and Defender configuration | Retrieving publishing passwords; minting or replaying SAS; opening Kudu console; requesting managed-identity tokens; reading secrets or application files; changing configuration |
| **D - Explicit change-window addendum** | Tier C plus nonproduction target, rollback plan, owner on call, approved canary data, and written permission for each action | Controlled canary blob read/write/delete; publishing-profile rotation test; nonproduction deployment; slot-swap rehearsal; managed-identity access validation against a canary resource; alert simulation | Production disruption, destructive testing, persistence, access to real student data, unrestricted post-exploitation, denial of service |

The two accounts should be deliberately different, for example a normal student-like identity and an owner-created administrative test role. They must not be real users' accounts. Authentication logs, owner contact, and an emergency stop path should be active before Tier C begins.

## 3. Technique Universe: Tool, Manual Method, Detection, And Gate

The following is the defensible technique universe for the requested class. It covers public discovery, authenticated configuration assessment, controlled validation, and detection. It is not a claim that every Azure security utility ever published has been enumerated; it includes every materially relevant tool found in the reviewed public corpus and excludes generic packet tools that add no Azure-specific capability.

| Technique | Applicable tools | Safe/manual method | Detection counterpart | Minimum gate |
|---|---|---|---|---|
| **Hosting-resource attribution** | Azure CLI, Azure PowerShell, ARI, AzGovViz; cloud_enum only after authorization | Owner exports the exact resource ID, subscription, resource group, SKU, custom-domain binding, and responsible tenant. Pre-authorization work is passive correlation only | Asset inventory drift; Resource Graph inventory; domain-binding change alerts | A for passive; C for tenant inventory |
| **Default App Service and slot hostname discovery** | cloud_enum, Nuclei, Azure CLI/PowerShell | Prefer owner-supplied hostnames. Do not guess `azurewebsites.net` names pre-authorization. Slots are live apps with distinct hostnames [11] | App Service HTTP logs per app/slot; passive DNS monitoring; certificate inventory | B for active validation; C for complete inventory |
| **Kudu/SCM presence and exposure** | Azure CLI/PowerShell, Nuclei with owner-approved templates, Prowler/Steampipe where checks exist | Inspect ARM configuration and SCM access rules first. If App Service is confirmed, its documented non-Isolated pattern is `https://<app-name>.scm.azurewebsites.net` [9]. Do not request a guessed candidate without Tier B | `AppServiceAuditLogs` for attempted and successful basic-auth logins [19]; HTTP/access logs; ARM policy changes | B for unauthenticated existence check; C for configuration; D for console/API access |
| **SCM and FTP basic-publishing policy** | Prowler, ScoutSuite, Monkey365, Steampipe, CloudSploit, Azure CLI/PowerShell, PSRule for Azure | Read the `scm` and `ftp` basic-publishing policy resources. Do not retrieve a password merely to prove that basic auth is enabled. Microsoft recommends Entra/OIDC or managed-identity deployment instead [6] | `AppServiceAuditLogs`; Activity Log alert on writes to basic-publishing policy; Azure Policy compliance | C |
| **Deployment credential scope and retrieval rights** | Azure CLI/PowerShell; MicroBurst only under specialist supervision | Review who has `Microsoft.Web/sites/publish/Action` and who can list publishing profiles. App-scope credentials are generated per app; user-scope credentials can span the user's Azure account [21] | Activity Log for control-plane actions where emitted; SCM audit logs; privileged-role and RBAC change alerts | C for rights review; D for actual retrieval or rotation |
| **CI/CD and deployment provenance** | Azure CLI/PowerShell, Prowler, ScoutSuite, AzGovViz, Gitleaks, TruffleHog | Review owner-provided pipeline definitions, federated credentials, service connections, deploy logs, and secret stores offline. Prefer OIDC or managed identity over a stored publishing profile [19] | Pipeline audit logs; Entra service-principal sign-ins; Activity Log; deployment logs | C; D for deployment execution |
| **Deployment slot inventory and drift** | Azure CLI/PowerShell, ARI, AzGovViz, CloudFox inventory | Export every slot and compare app settings, sticky settings, custom domains, access restrictions, authentication, identity, TLS, diagnostics, and basic-auth policies. Do not swap slots during assessment | Activity Log for slot creation/update/swap; per-slot App Service logs; configuration-drift alerts | C; D for swap |
| **Public blob/container posture** | BlobHunter, cloud_enum, MicroBurst, Prowler, ScoutSuite, Monkey365, Steampipe, CloudSploit | Owner-side configuration review is preferred. Active anonymous listing or object requests are not pre-authorization activity. BlobHunter is authenticated and emits a CSV of publicly exposed containers [34] | `StorageRead`, `StorageWrite`, and `StorageDelete` resource logs in `StorageBlobLogs` [16]; alerts on `Anonymous` authentication | B for narrowly approved public check; C for complete inventory |
| **Storage account and container name discovery** | cloud_enum, MicroBurst, Nuclei custom templates | Use names from owner inventory or already-published references. Avoid wordlist expansion against MUJ before the letter | DNS/HTTP edge telemetry where available; Storage resource logs once a valid account is reached; rate/anomaly alerting | B |
| **SAS discovery in code, logs, and configuration** | Gitleaks, TruffleHog, Trivy secret scanning; custom offline rules | Scan owner-provided or public repositories offline. Redact signatures immediately. Do not follow, verify, or replay a discovered URL. Gitleaks is a local secret scanner; TruffleHog supports custom regex detectors [27][40] | Repository secret-scanning alerts; DLP; storage access logs keyed to token hash where available [16] | A for public/offline material; C for private repositories |
| **SAS quality review** | No complete live-estate tool; custom parser/build candidate | Parse an owner-supplied, redacted SAS for type, service, resource, permissions, start/expiry, protocol, IP range, and stored-access-policy linkage. Never store the signature. Microsoft advises HTTPS, least privilege, and a revocation plan [13] | Storage logs by authentication type/token hash; alerts for expired, long-lived, broad, or anomalous SAS use | C for metadata; D for any live use |
| **Shared Key and public-access controls** | Prowler, ScoutSuite, Monkey365, Steampipe, CloudSploit, PSRule, Checkov, Trivy | Read whether Shared Key and anonymous blob access are allowed, and whether SAS expiration policy is configured. Prefer Entra authorization where supported [10] | Azure Policy; Activity Log on storage configuration changes; Defender for Storage | C |
| **Easy Auth discovery and tenant binding** | Azure CLI/PowerShell; Prowler/ScoutSuite for configuration; browser or Burp/ZAP for approved account flows | Read `authsettingsV2`, provider registration, allowed tenant/audience, unauthenticated action, token-store state, and redirect URIs. Provider login paths use `/.auth/login/<provider>` when the feature is configured [24] | App Service authentication/HTTP logs; Entra interactive and noninteractive sign-ins; redirect and failure-rate alerts | C |
| **Easy Auth account-differential validation** | Browser developer tools, Burp Suite, OWASP ZAP; a purpose-built harness is preferable | With two test accounts, compare login, logout, session renewal, application roles, tenant rejection, and downstream authorization. Do not retain access or refresh tokens. Easy Auth can cache ID, access, and refresh tokens if its token store is enabled [24] | Entra sign-ins; App Service auth logs; application authorization events | C |
| **Managed identity presence and effective access** | Azure CLI/PowerShell, AzureHound, Stormspotter, CloudFox RBAC, Prowler, ScoutSuite, Monkey365 | Export identity IDs and role assignments, then model access to Storage, Key Vault, SQL, and ARM. System-assigned identities die with the app; user-assigned identities are reusable resources [20] | Managed-identity sign-in logs; target-service resource logs; Key Vault/Storage diagnostics; RBAC-change alerts | C |
| **Managed identity runtime validation** | No safe general-purpose scanner; native SDK/client in a canary app | Use a nonproduction slot and a canary resource. Validate only an owner-approved permission. Do not attempt SSRF, metadata-service coercion, or token extraction from production | Managed-identity sign-ins plus target data-plane logs; canary alerts | D |
| **RBAC and graph attack-path analysis** | AzureHound, Stormspotter, CloudFox, ROADtools; GraphRunner/AADInternals only for a separately authorized identity assessment | Begin with owner-exported read-only data. Review `publish/Action`, slot writes, identity assignment, role-assignment writes, storage key/list actions, and Key Vault access | Activity Log for role-assignment changes; Entra audit and sign-in logs; privileged-access reviews | C; post-exploitation modules excluded without separate scope |
| **IaC and policy validation** | PSRule for Azure, Checkov, Trivy, Steampipe, Prowler | Scan owner-provided ARM, Bicep, Terraform, or pipeline artifacts offline; compare desired state with live read-only export | CI policy gates; Azure Policy; deployment-denial and exemption alerts | A for public IaC; C for private/live state |
| **Telemetry coverage test** | Azure Monitor/Log Analytics, Defender for Cloud, native clients | Verify that each approved canary event yields a timestamped event in the expected table before testing begins. Activity Log normally omits reads [18], so absence there cannot disprove enumeration | Alert health, diagnostic-setting drift, ingestion-latency checks, table-retention monitoring | C for read-only verification; D for canaries |

**Takeaway:** no single product covers public discovery, management-plane configuration, data-plane use, identity graphing, and logging. The minimum credible campaign combines owner-side native inventory, one posture framework, offline secret scanning, manual Easy Auth testing with two accounts, and detection verification.

## 4. Tool Catalog

Output entries marked "module-specific" mean that the project's reviewed top-level documentation did not promise a stable universal report schema. This is important for reproducibility: the club should wrap such tools rather than assume machine-readable output.

| Tool and exact URL | Licence and delivery | Driven by | Documented output | Best use here and gate |
|---|---|---|---|---|
| **cloud_enum** - https://github.com/initstring/cloud_enum | MIT; free, self-hosted [33] | CLI, keyword-based public-resource enumeration | Text, JSON, CSV [33] | Azure storage, blob, database, VM, and web-app discovery [33]. Tier B only against target-derived names; maintainer notes limited active use [33] |
| **MicroBurst** - https://github.com/NetSPI/MicroBurst | BSD 3-Clause; free PowerShell module [43] | PowerShell functions | Module-specific PowerShell/console output; no universal format documented | Azure discovery, weak-configuration audit, and sensitive post-exploitation modules [43]. Use only selected discovery/audit functions at Tier C; exclude credential-dumping functions |
| **BlobHunter** - https://github.com/cyberark/blobhunter | MIT; free, self-hosted [34] | Python CLI with Azure CLI authentication | CSV [34] | Authenticated subscription-wide public-container review. Tier C |
| **CloudFox** - https://github.com/BishopFox/cloudfox | MIT; free, self-hosted [37] | CLI with an Azure principal | Terminal/module output; stable aggregate format not documented in the reviewed page | `whoami`, inventory, RBAC, storage, and VM situational awareness [37]. Designed for Viewer-like access [37]. Tier C |
| **Nuclei** - https://github.com/projectdiscovery/nuclei | MIT CLI; free self-hosted plus optional hosted tiers [35] | CLI, templates, optional cloud/API | JSON, JSONL, Markdown, SARIF, PDF [35] | Only owner-reviewed Azure/HTTP templates with strict target list and rate limits. Tier B or C; never broad autonomous scanning |
| **ROADtools / ROADrecon** - https://github.com/dirkjanm/ROADtools | MIT; free, self-hosted [49] | CLI plus Angular analysis UI | SQLAlchemy-backed local database; plugin-dependent exports [49] | Entra tenant exploration and app/service-principal relationships. Tier C; token-exchange features excluded from baseline |
| **AzureHound** - https://github.com/SpecterOps/AzureHound | GPL-3.0; free collector for BloodHound [32] | CLI with approved tenant credentials or token | Stdout or JSON file [32] | Entra and ARM relationship collection for attack-path analysis. Tier C |
| **Stormspotter** - https://github.com/Azure/Stormspotter | MIT; free, locally hosted graph UI [31] | CLI collector, FastAPI backend, web UI | Collector SQLite; conversion to JSON exists, but the application parses SQLite [31] | Azure subscription/ARM/Entra attack graph [31]. Tier C; beta and incomplete resource coverage [31] |
| **AADInternals** - https://github.com/Gerenios/AADInternals | MIT; free, self-hosted PowerShell module [26] | PowerShell | PowerShell objects and command-specific files; no universal report documented | Specialist Entra administration/security research. Exclude offensive/token functions from the base club campaign; separately scoped Tier C/D only |
| **GraphRunner** - https://github.com/dafthack/GraphRunner | MIT; free, self-hosted [46] | PowerShell, HTML GUI, Microsoft Graph | Command-specific console and exports; no universal schema documented | Its stated focus is post-exploitation with authenticated tokens [46]. Not recommended for the initial MUJ App Service assessment |
| **Prowler** - https://github.com/prowler-cloud/prowler | Apache-2.0; free self-hosted with optional hosted platform [38] | CLI, container, CI, optional SaaS | CSV, JSON, JSON-OCSF, HTML and integrations as supported by current release [38] | Broad Azure posture and compliance checks. Tier C; pin version and preserve raw output |
| **Scout Suite** - https://github.com/nccgroup/ScoutSuite | GPL-2.0; free, self-hosted [36] | Python CLI | Local HTML report with account configuration and findings [36] | Independent Azure configuration review. Tier C |
| **Monkey365** - https://github.com/silverhack/monkey365 | GPL-3.0; free, self-hosted [42] | PowerShell | HTML plus command/report data supported by the framework; verify current module schema before automation | Microsoft 365, Azure, and Entra posture review [42]. Useful where three tenants must be kept distinct. Tier C |
| **Azure Compliance Mod for Powerpipe** - https://github.com/turbot/steampipe-mod-azure-compliance | Apache-2.0; free, self-hosted [41] | Powerpipe/Steampipe CLI and dashboard | Interactive dashboards, snapshots and benchmark reports; export depends on engine | Repeatable CIS/NIST and custom SQL-style Azure controls [41]. Tier C |
| **CloudSploit** - https://github.com/aquasecurity/cloudsploit | GPL-3.0; free, self-hosted [30] | Node.js CLI/API-style plugins | Console, CSV, JSON where configured; confirm release-specific flags | Independent cloud-configuration checks. Tier C |
| **Azure CLI** - https://github.com/Azure/azure-cli and https://learn.microsoft.com/en-us/cli/azure | MIT; free, self-hosted client [28] | CLI, scripts, `az rest` for approved ARM calls | JSON by default; JSONC, YAML, YAMLC, table, TSV, and none are documented output modes [51] | Primary read-only inventory and exact resource queries. Tier C; avoid commands that list secrets, credentials, or keys without Tier D |
| **Azure PowerShell** - https://github.com/Azure/azure-powershell | MIT; free, self-hosted [45] | PowerShell cmdlets | PowerShell objects, with normal PowerShell conversion to approved formats | Native inventory and repeatable owner-side evidence collection. Tier C |
| **PSRule for Azure** - https://github.com/Azure/PSRule.Rules.Azure | MIT; free, self-hosted [47] | PowerShell/CLI/CI against IaC or exported resources | YAML, JSON, Markdown, NUnit3 XML, CSV, SARIF [52] | Preventive IaC and exported-state rules. Tier A for public IaC; Tier C for private/live exports |
| **Azure Resource Inventory (ARI)** - https://github.com/microsoft/ARI | MIT; free, self-hosted [29] | PowerShell with Azure authentication | Excel inventory and supported diagrams/reports [29] | Owner-readable estate baseline and evidence package. Tier C |
| **Azure Governance Visualizer (AzGovViz)** - https://github.com/Azure/Azure-Governance-Visualizer | MIT; free, self-hosted [48] | PowerShell polling ARM, Storage, and Graph | CSV, HTML, Markdown, JSON [53] | Tenant/subscription hierarchy, policy, RBAC, and governance context. Tier C |
| **Gitleaks** - https://github.com/gitleaks/gitleaks | MIT; free, self-hosted [27] | CLI, pre-commit, CI | JSON, CSV, JUnit, SARIF, and template-supported reports in current releases | Offline search for publishing profiles, connection strings, and SAS-like material. Use custom validated rules and never verify found tokens |
| **TruffleHog** - https://github.com/trufflesecurity/trufflehog | AGPL-3.0; free, self-hosted with commercial options [40] | CLI, container, CI, source connectors | Human-readable and JSON-family output; release-dependent | Secret discovery across approved repositories and history; supports custom regex detectors [40]. Tier A/C depending on repository ownership |
| **Checkov** - https://github.com/bridgecrewio/checkov | Apache-2.0; free, self-hosted with optional platform [44] | CLI, CI, API/platform integrations | CLI, JSON, JUnit XML, SARIF, GitLab SAST and other documented framework outputs | IaC checks for App Service, Storage, identity, logging, and policy. Tier A/C |
| **Trivy** - https://github.com/aquasecurity/trivy | Apache-2.0; free, self-hosted [39] | CLI, server, container, CI | Table, JSON, template, SARIF, CycloneDX/SPDX as supported [39] | IaC misconfiguration and secret scanning. Tier A/C |
| **AzCopy v10** - https://github.com/Azure/azure-storage-azcopy | MIT; free, self-hosted [50] | CLI | Transfer status, logs, and job-plan artifacts [50] | Not a discovery scanner. Use only for an owner-approved canary transfer at Tier D; never use it to explore real student data |

Burp Suite and OWASP ZAP remain useful supporting HTTP clients for the two-account Easy Auth matrix. Burp supports community or custom extensions [54], while ZAP provides JSON, XML, and SARIF reporting options [55]. They are not substitutes for ARM-side configuration evidence.

## 5. Control-Surface Case Studies

### 5.1 SAS: usage can be observed, creation cannot

A useful Azure Storage case is the difference between **governance visibility** and **data-plane visibility**. Microsoft documents three SAS types. User-delegation SAS uses Entra credentials; service and account SAS rely on the storage account key [13]. Microsoft recommends user-delegation SAS where possible and warns that anyone obtaining a leaked SAS can use it [13].

The failure case is assuming that an owner can enumerate all outstanding tokens. Azure does not track how many SAS tokens were generated, and SAS creation itself cannot be audited [13]. Storage logging can identify access type and retain a hash associated with SAS or OAuth authentication [16], but that observes use, not issuance.

For MUJ SLCM, the implication is procedural. The club should first search approved source, deployment artifacts, documentation, and configuration offline. A found token should be redacted and reported, not opened. After Tier C begins, defenders should inspect storage-account policy and `StorageBlobLogs`. Only a Tier D canary token with synthetic data should be used to prove expiry, permission, revocation, and alert behavior.

### 5.2 Kudu: a separate administrative application, not another URL path

Kudu is not merely an MVC route beneath the measured custom domain. App Service creates it as a companion application, normally using an SCM hostname [9]. Its documented capabilities include settings, connection strings, environment and server variables, command execution, diagnostics, process management, ZIP deployment, deployment scripts, and a REST API [9].

This explains why the supplied GET-only method behavior and clean host-header tests do not settle the Kudu question. **Inference:** if the target is App Service, the SCM plane may have different authentication, access restrictions, TLS settings, and logs. Conversely, probing guessed SCM names before resource attribution could touch unrelated tenants.

The safe decision is configuration-first. At Tier C, inspect the exact SCM policy, access rules, role assignments, and audit destination. Access to Kudu through Entra should be limited to a role containing the necessary publish action rather than broad administrative roles [9]. Console, file, environment, process, or REST access belongs only in Tier D and should target a nonproduction slot.

### 5.3 Slots: deployment safety creates additional attack surface

Deployment slots reduce deployment risk because they are live apps that can be warmed and swapped without dropping requests [11]. The security tension is that every slot is also an addressable application. A staging slot can drift from production in authentication, logging, network restrictions, secrets, or basic publishing settings.

A swap also has non-obvious semantics: some configuration follows the content while slot-specific settings remain with the slot [11]. Managed identity adds another dimension because its configuration is slot-specific [20]. A posture tool may report two individually valid resources while missing that their swap behavior creates an unsafe combination.

For this target, owner-side export should compare production and every slot as a matrix. The assessment should model a swap without performing one. A real swap rehearsal requires Tier D, a rollback plan, and synthetic data because a successful security test that alters production routing is still an operational incident.

### 5.4 Easy Auth and application authorization are not the same control

Easy Auth can authenticate clients, validate and refresh provider tokens, manage sessions, and inject identity information into request headers [24]. When the token store is enabled, ID, access, and refresh tokens can be cached for the authenticated session [24]. This platform service does not automatically prove that the MVC application enforces the correct student, faculty, administrative, or tenant authorization after identity is established.

The failure case is testing only whether one account can log in. Three observed Entra tenants make tenant binding, audience, redirect URI, claims, app roles, guest handling, and logout/session invalidation material. **Inference:** the two test accounts should differ in expected authorization, not merely username.

The Tier C method is a small state matrix: unauthenticated, account A, account B, expired session, logout, and rejected tenant. Record status, redirect chain, cookies, user-visible authorization, and server-side events without retaining tokens. This validates both platform authentication and application authorization while avoiding password spraying or access to real student records.

## 6. Detection Engineering Counterpart

| Surface | Minimum telemetry | Detection logic | Known blind spot |
|---|---|---|---|
| ARM/App Service configuration | Activity Log exported to Log Analytics or Event Hub | Alert on writes to auth settings, identity, slot, hostname, TLS, access restrictions, diagnostic settings, and basic-publishing policies | Activity Log normally does not capture reads [18] |
| SCM/FTP authentication | `AppServiceAuditLogs` and SCM access telemetry | Failed/successful publishing login, new source IP, legacy basic auth, repeated failures | No signal if diagnostic routing is absent or the resource is not App Service |
| Main app and slots | Per-slot HTTP, application, authentication, and platform logs | New hostname access, unexpected slot traffic, auth failures, anomalous user agent, status spikes | Production-only logging leaves staging blind |
| Blob data plane | `StorageRead`, `StorageWrite`, `StorageDelete` into `StorageBlobLogs` [16] | Group by authentication type, token hash, requester identity, object path, source IP, operation, and status | SAS issuance is not auditable; unused leaked SAS has no access event [13] |
| Entra users and service principals | Sign-in and audit logs in each responsible tenant | New app/service-principal use, cross-tenant failures, impossible role for test account, unusual token audience | Sign-in proves authentication activity, not every downstream resource read |
| Managed identity | Managed-identity sign-in logs plus target-service resource logs | New destination resource, denied access, unusual volume, identity/role change followed by access | Role/group changes can be delayed by managed-identity caching for about 24 hours [20] |
| CI/CD | Azure DevOps or GitHub audit logs, workload-identity sign-ins, deployment logs | New federated credential, secret fallback, unapproved branch/environment, unexpected deployment principal | External build systems may require separate retention and export |
| Posture | Azure Policy, Prowler/Steampipe/PSRule baselines, Resource Graph snapshots | Drift in minimum TLS, HTTPS-only, public blob access, Shared Key, SCM auth, diagnostics, identity, and network rules | Compliance pass does not validate application authorization or effective data-plane access |

Azure retains Activity Log events for 90 days unless they are exported [18]. Diagnostic settings can send them to Log Analytics, Event Hubs, or Storage for longer retention and correlation [18]. The testing letter should therefore require a named log destination and retention period rather than the vague statement "logging enabled."

## 7. NO-TOOL GAPS

| Gap | Why existing tools do not settle it | Required manual control |
|---|---|---|
| **Custom domain to exact Azure resource** | DNS, ASN, IIS, and certificates may support a hypothesis but do not prove the subscription/resource owner | Owner supplies resource ID and domain-binding evidence; independently compare read-only ARM output |
| **SAS issuance inventory** | Azure cannot audit SAS generation or report token count [13] | Preventive policy, source scanning, short expiry, least privilege, stored access policies where supported, and use telemetry |
| **Unused leaked SAS** | No access means no Storage log event | Offline secret scanning and rapid key/policy response; never wait for an alert |
| **Main-site versus SCM equivalence** | A clean custom-domain result says nothing definitive about companion SCM policy | Compare explicit ARM configuration for both sites; then perform one approved low-rate validation |
| **Slot swap effective security** | Inventory tools list resources but rarely compute which settings move, stay, or combine after a swap | Build an effective-state diff and owner-reviewed swap model |
| **Easy Auth plus MVC authorization** | Configuration scanners can see provider settings but cannot prove page- and role-level outcomes | Two-account browser matrix with server-side event correlation |
| **Managed identity effective data-plane reach** | ARM RBAC graphs may miss service-specific policies, cached permissions, and application behavior | Combine identity graph, target-service policy, and a synthetic Tier D canary |
| **Three-tenant attribution** | Public tenant hints do not prove which tenant owns the app registration, subscription, guests, or managed identity | Owner-provided tenant map and test-account matrix |
| **Read-only enumeration detection** | Activity Log usually omits reads [18] | Entra sign-in correlation, API diagnostics where available, short-lived assessment principal, and pre/post inventory |
| **Meaning of supplied application errors** | Error size and exception type do not establish Azure secrets or control-plane linkage | Offline content review; owner code review; no additional fault generation without scope |

## 8. BUILD CANDIDATES

| Candidate | Input and operation | Output | Safety design | Priority |
|---|---|---|---|---|
| **SLCM Azure Lineage Packager** | Owner-entered resource IDs plus passive DNS/certificate/public-code evidence; correlates rather than brute-forces | JSON and Markdown evidence graph with confidence labels | No target requests; refuses guessed-host validation | **P0** because App Service is not yet proven |
| **App Service Estate Diff** | Read-only ARM exports for app and every slot; compares TLS, HTTPS-only, SCM/FTP policy, auth, identity, access rules, diagnostics, sticky settings, domains | JSON, CSV, SARIF, human diff | Secret values are never requested; values are hashed or presence-only | **P0** |
| **SAS Governance Linter** | Redacted URLs, source files, or deployment artifacts; parses SAS metadata without network use | SARIF/JSON finding with type, permissions, expiry, protocol, IP, policy linkage | Signature removed at ingestion; no verification request capability | **P0** |
| **Easy Auth Two-Account Matrix** | Approved app URL, two test accounts, expected roles/tenants, owner-defined routes | HAR with tokens/cookies redacted, JSON state matrix, pass/fail report | Allowlisted routes, no spraying, no token export, hard request cap | **P1** |
| **Slot Swap Risk Modeler** | Production/slot configuration snapshots and documented swap rules | Pre-swap and post-swap effective-state table | Simulation only; cannot invoke swap | **P1** |
| **Managed Identity Reach Analyzer** | Resource graph, role assignments, service-specific access policies, slot identity map | Graph plus least-privilege findings | No token acquisition; flags uncertainty rather than testing access | **P1** |
| **SCM Exposure And Telemetry Correlator** | Approved SCM configuration, `AppServiceAuditLogs`, access restrictions, basic-auth policy | Timeline and control/detection mismatch report | No authentication or Kudu API client included | **P1** |
| **Azure Canary Telemetry Harness** | Owner-created nonproduction slot, canary blob/resource, expected KQL event map | Timestamped evidence bundle showing generated event and observed alert | Tier D lock, synthetic data only, automatic stop, no production IDs accepted | **P2** |

The most valuable build is not another endpoint brute-forcer. It is the **App Service Estate Diff**, because present tools split the evidence across app, slot, identity, storage, auth, and logging views. A presence-only secret model also lets a university club produce evidence without collecting credentials.

## 9. Synthesis

The estate must be analyzed across four different mechanisms. **Public discovery** asks whether an Azure-shaped endpoint exists; cloud_enum and tightly restricted Nuclei templates address that question, but they cannot prove ownership. **Management-plane review** asks how the resource is configured; native Azure clients, Prowler, Scout Suite, Steampipe, Monkey365, ARI, and AzGovViz are stronger here. **Identity-path analysis** asks what users, service principals, and managed identities can reach; AzureHound, Stormspotter, ROADtools, and CloudFox provide graph context. **Data-plane validation** asks what actually happens when a permitted identity accesses Storage, Kudu, or the application; that phase requires specific authorization, canary data, and resource logs.

The most important tension is between evidence quality and operational risk. A public SCM response or functioning SAS would be strong evidence, but obtaining it by guessing or replay before authorization would be unacceptable. Conversely, an owner-side configuration export is safer and broader but may not prove runtime behavior. The correct sequence is therefore configuration -> detection verification -> narrow runtime canary, not scan -> credential use -> retrospective logging.

A second tension is visibility. Activity Log gives strong evidence for configuration changes but normally not reads [18]. Storage logs can show token use but not token creation [13][16]. Easy Auth can authenticate a user but does not prove correct MVC authorization. Slots improve deployment reliability yet multiply live hostnames and create swap semantics. These are not isolated findings; together they show why a single "Azure scan" would underperform.

For MUJ SLCM, the measured web findings should remain in a separate application track. The verbose errors, non-Secure antiforgery cookie, no HSTS, and legacy TLS support deserve remediation, but none should be represented as control-plane compromise. The Azure track begins only when ownership and architecture are established. If the owner confirms App Service, the first priorities are SCM/basic-auth policy, complete slot inventory, storage/SAS governance, Easy Auth tenant binding, managed-identity effective access, and diagnostic coverage.

## VERDICT

**Verdict: The Azure control-plane campaign is ABSENT, not clean and not compromised.**

**Confidence: High (0.92) that the supplied testing does not cover the requested Azure control-plane surfaces.** The brief explicitly states that the campaign never authenticated and lists no Blob Storage, SAS, Kudu/SCM, publishing-profile, slot, Easy Auth, managed-identity, ARM, or Azure logging work.

**Confidence: Medium-low (0.35) that the public portal is specifically Azure App Service.** Microsoft network presence, IIS, ASP.NET, and Microsoft identity are consistent with App Service, but the supplied evidence does not exclude a VM, reverse proxy, Application Gateway, Front Door, or another hosting arrangement. This is explicitly an inference, not an attribution.

**Authorization decision:** Tier A passive and offline work is safe before the letter. Any active discovery of guessed Azure assets requires the signed letter. Authenticated configuration and two-user authorization testing require both the letter and the two dedicated accounts. Publishing-profile retrieval, SAS use, Kudu access, managed-identity token validation, blob writes, deployment, or slot swaps require an additional explicit nonproduction change window.

**Recommended next action:** ask the owner for the resource-attribution package and telemetry evidence, then run a read-only App Service Estate Diff. Do not attempt to beat "ABSENT" by touching guessed Azure endpoints; beat it by producing owner-attributed, logged, reproducible evidence.

## References

1. *Penetration testing | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/security/fundamentals/pen-testing
2. *Sign-in logs in Microsoft Entra ID - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-sign-ins
3. *Azure Monitor Logs reference - StorageBlobLogs - Azure Monitor | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/storagebloblogs
4. *Microsoft Security Testing Rules of Engagement*. https://www.microsoft.com/en-us/msrc/pentest-rules-of-engagement
5. *Enable Diagnostic Logs - Azure App Service | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/app-service/troubleshoot-diagnostic-logs
6. *Overview Security*. https://learn.microsoft.com/en-us/azure/app-service/overview-security
7. *Overview Access Restrictions*. https://learn.microsoft.com/en-us/azure/app-service/overview-access-restrictions
8. *Tutorial: Access Azure databases with managed identity - Azure App Service | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/app-service/tutorial-connect-msi-azure-database
9. *Kudu service overview - Azure App Service | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/app-service/resources-kudu
10. *Prevent authorization with Shared Key - Azure Storage | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/storage/common/shared-key-authorization-prevent
11. *Deploy Staging Slots*. https://learn.microsoft.com/en-us/azure/app-service/deploy-staging-slots
12. *Secure Your Domain with TLS/SSL - Azure App Service | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/app-service/configure-ssl-bindings
13. *Grant limited access to data with shared access signatures (SAS) - Azure Storage | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/storage/common/storage-sas-overview
14. *Remediate anonymous read access to blob data (Azure Resource Manager deployments) - Azure Storage | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/storage/blobs/anonymous-read-access-prevent
15. *List of built-in policy definitions - Azure Policy | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/governance/policy/samples/built-in-policies
16. *Azure Blob Storage Monitoring Metrics and Logs Reference | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/storage/blobs/monitor-blob-storage-reference
17. *Configure an expiration policy for shared access signatures (SAS) - Azure Storage | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/storage/common/sas-expiration-policy
18. *Activity Log in Azure Monitor - Azure Monitor | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/activity-log
19. *Configure Basic Auth Disable*. https://learn.microsoft.com/en-us/azure/app-service/configure-basic-auth-disable
20. *Managed Identities - Azure App Service | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/app-service/overview-managed-identity
21. *Manage Deployment Credentials - Azure App Service | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/app-service/deploy-configure-credentials
22. *Security Recommendations for Blob Storage - Azure Storage | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/storage/blobs/security-recommendations
23. *Configure Microsoft Entra Authentication - Azure App Service | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/app-service/configure-authentication-provider-aad
24. *Authentication and Authorization - Azure App Service | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/app-service/overview-authentication-authorization
25. *Environment Variables and App Settings Reference - Azure App Service | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/app-service/reference-app-settings
26. *GitHub - Gerenios/AADInternals: AADInternals PowerShell module for administering Azure AD and Office 365 · GitHub*. https://github.com/Gerenios/AADInternals
27. *GitHub - gitleaks/gitleaks: Find secrets with Gitleaks 🔑 · GitHub*. https://github.com/gitleaks/gitleaks
28. *GitHub - Azure/azure-cli: Azure Command-Line Interface · GitHub*. https://github.com/Azure/azure-cli
29. *GitHub - microsoft/ARI: Azure Resource Inventory - It's a Powerful tool to create EXCEL inventory from Azure Resources with low effort · GitHub*. https://github.com/microsoft/ARI
30. *GitHub - aquasecurity/cloudsploit: Cloud Security Posture Management (CSPM) · GitHub*. https://github.com/aquasecurity/cloudsploit
31. *GitHub - Azure/Stormspotter: Azure Red Team tool for graphing Azure and Azure Active Directory objects · GitHub*. https://github.com/Azure/Stormspotter
32. *GitHub - SpecterOps/AzureHound: Azure Data Exporter for BloodHound · GitHub*. https://github.com/SpecterOps/AzureHound
33. *GitHub - initstring/cloud_enum: Multi-cloud OSINT tool. Enumerate public resources in AWS, Azure, and Google Cloud. · GitHub*. https://github.com/initstring/cloud_enum
34. *GitHub - cyberark/BlobHunter: Find exposed data in Azure with this public blob scanner · GitHub*. https://github.com/cyberark/blobhunter
35. *GitHub - projectdiscovery/nuclei: Nuclei is a fast, customizable vulnerability scanner powered by the global security community and built on a simple YAML-based DSL, enabling collaboration to tackle trending vulnerabilities on the internet. It helps you find vulnerabilities in your applications, APIs, networks, DNS, and cloud configurations. · GitHub*. https://github.com/projectdiscovery/nuclei
36. *GitHub - nccgroup/ScoutSuite: Multi-Cloud Security Auditing Tool · GitHub*. https://github.com/nccgroup/ScoutSuite
37. *GitHub - BishopFox/cloudfox: Automating situational awareness for cloud penetration tests. · GitHub*. https://github.com/BishopFox/cloudfox
38. *GitHub - prowler-cloud/prowler: Prowler is the world’s most widely used open-source cloud security platform that automates security and compliance across any cloud environment. · GitHub*. https://github.com/prowler-cloud/prowler
39. *GitHub - aquasecurity/trivy: Find vulnerabilities, misconfigurations, secrets, SBOM in containers, Kubernetes, code repositories, clouds and more · GitHub*. https://github.com/aquasecurity/trivy
40. *GitHub - trufflesecurity/trufflehog: Find, verify, and analyze leaked credentials · GitHub*. https://github.com/trufflesecurity/trufflehog
41. *GitHub - turbot/steampipe-mod-azure-compliance: Run individual configuration, compliance and security controls or full compliance benchmarks for CIS, HIPAA HITRUST, NIST, and more across all of your Azure subscriptions using Powerpipe and Steampipe. · GitHub*. https://github.com/turbot/steampipe-mod-azure-compliance
42. *GitHub - silverhack/monkey365: Monkey365 is an open-source security assessment tool for Microsoft 365, Azure, and Microsoft Entra ID. It helps security professionals identify misconfigurations, review cloud security posture, and evaluate environments against industry security best practices and compliance standards. · GitHub*. https://github.com/silverhack/monkey365
43. *GitHub - NetSPI/MicroBurst: A collection of scripts for assessing Microsoft Azure security · GitHub*. https://github.com/NetSPI/MicroBurst
44. *GitHub - bridgecrewio/checkov: Prevent cloud misconfigurations and find vulnerabilities during build-time in infrastructure as code, container images and open source packages with Checkov by Bridgecrew. · GitHub*. https://github.com/bridgecrewio/checkov
45. *GitHub - Azure/azure-powershell: Microsoft Azure PowerShell · GitHub*. https://github.com/Azure/azure-powershell
46. *GitHub - dafthack/GraphRunner: A Post-exploitation Toolset for Interacting with the Microsoft Graph API · GitHub*. https://github.com/dafthack/GraphRunner
47. *GitHub - Azure/PSRule.Rules.Azure: Rules to validate Azure resources and infrastructure as code (IaC) using PSRule. · GitHub*. https://github.com/Azure/PSRule.Rules.Azure
48. *GitHub - JulianHayward/Azure-MG-Sub-Governance-Reporting: Azure Governance Visualizer aka AzGovViz is a PowerShell script that captures Azure Governance related information such as Azure Policy, RBAC (a lot more) by polling Azure ARM, Storage and Microsoft Graph APIs. · GitHub*. https://github.com/JulianHayward/Azure-MG-Sub-Governance-Reporting
49. *GitHub - dirkjanm/ROADtools: A collection of Azure AD/Entra tools for offensive and defensive security purposes · GitHub*. https://github.com/dirkjanm/ROADtools
50. *GitHub - Azure/azure-storage-azcopy: The new Azure Storage data transfer utility - AzCopy v10 · GitHub*. https://github.com/Azure/azure-storage-azcopy
51. *https://learn.microsoft.com/en-us/cli/azure*. https://learn.microsoft.com/en-us/cli/azure
52. *Analysis output - PSRule*. https://microsoft.github.io/PSRule/v2/analysis-output/
53. *Azure Governance Visualizer aka AzGovViz - GitHub*. https://github.com/Azure/Azure-Governance-Visualizer
54. *https://portswigger.net/burp/documentation/desktop/extensions*. https://portswigger.net/burp/documentation/desktop/extensions
55. *https://www.zaproxy.org/docs/desktop/addons*. https://www.zaproxy.org/docs/desktop/addons
