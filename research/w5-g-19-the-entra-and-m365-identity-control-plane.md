# Closing MUJ SLCM’s Three-Tenant Identity Blind Spot

## Executive Summary

- **Coverage Gap**: The supplied campaign record says the Entra/Microsoft 365 control plane received **no authenticated testing**, despite identifying **three tenants** and a portal credential tied to Microsoft 365 -> classify identity assurance as **ABSENT**, not “passed,” and prioritize a separately authorized identity campaign.

- **Six Directional Trust Reviews**: Three tenants create **six ordered tenant-to-tenant relationships**—`3 × (3 − 1) = 6`—because inbound and outbound cross-tenant policies can differ -> document and test all six directions rather than treating “the three tenants” as one boundary. Microsoft describes cross-tenant access settings as separately governing inbound and outbound B2B collaboration, B2B direct connect, and trust settings.

- **Credential Blast Radius**: “The portal password is the M365 password” is security-critical but does not establish how authentication works -> determine whether SLCM redirects to Entra using OIDC/SAML, validates credentials through a legacy flow, or maintains synchronized credentials. Microsoft explicitly discourages the OAuth Resource Owner Password Credentials flow because it is incompatible with several modern controls, including MFA.

- **Consent And Workload Risk**: Guest invitation, user/admin consent, app registration, service-principal ownership, credentials, workload identities, and tenant-wide grants remain untested -> start with read-only policy and grant enumeration, then use canary apps and guests only after written authorization. Entra distinguishes application objects from tenant-local service principals, while delegated and application permissions create materially different risk.

- **Device-Code And PRT Exposure**: Device-code phishing and Primary Refresh Token paths were untouched -> initially assess Conditional Access, device registration, token protection, and sign-in telemetry without extracting tokens; conduct any token exercise only on an issued test device. Device-code flow and PRT behavior are documented parts of Microsoft’s identity platform, while Conditional Access can target authentication flows such as device code.

- **Telemetry Must Precede Testing**: Consent grants, invitations, app credentials, service-principal sign-ins, role changes, and device registrations can otherwise disappear into short native retention windows -> export Entra sign-in and audit logs to Log Analytics, Sentinel, or another approved SIEM before executing canaries.

- **Web Findings Are Context, Not Identity Proof**: The supplied **2026-09-13** measurements—four verbose YSOD triggers, a three-state `enc` oracle, no HSTS, TLS **1.0–1.3**, and an antiforgery cookie lacking `Secure`—justify remediation but do not prove an Entra compromise path -> keep the web and identity workstreams correlated but separately evidenced.

- **Authorization Boundary**: Pre-authorization work should stop at documentation review, evidence preservation, and narrowly passive public-source analysis -> guest invitations, consent prompts, app registrations, device-code authentication, PRT handling, password validation, authenticated Graph access, and tenant mutations require the signed scope letter and controlled test accounts.

- **Bottom-Line Decision**: There is **high confidence that identity campaign coverage is absent**, but **low confidence about actual exploitability** because no authenticated identity evidence was collected -> authorize a telemetry-first, least-privilege campaign rather than describing the target as either secure or vulnerable.

---

## 1. Evidence Boundaries Prevent a False “Secure” Conclusion

The target endpoint is `https://mujslcm.jaipur.manipal.edu/`.All target-specific response sizes, headers, technologies, and campaign-status statements below come from the supplied **2026-09-13** measurement record. They have not been independently revalidated, and no public URL can substantiate the exact byte counts or the claim that three tenants were enumerated.

This report uses public Microsoft, CISA, MITRE, OWASP, NIST, and tool-project documentation for architectural and defensive claims. It does not provide private deliberative reasoning, token-theft instructions, phishing templates, credential-capture procedures, or commands for operating offensive tools. Instead, it provides an auditable evidence-to-decision rationale.

### Supplied measurements and their bounded implications

| Supplied observation | What it supports | What it does **not** support | Recommended action |
|---|---|---|---|
| Only **TCP/443** was reachable; TLS **1.0–1.3** was offered; HSTS was absent | Legacy TLS remains enabled, and browsers receive no persistent HSTS policy | It does not prove a practical downgrade, especially while port 80 is unreachable | Disable TLS 1.0/1.1 after dependency review; deploy HSTS with a staged rollout. NIST’s TLS guidance centers on TLS 1.2 and 1.3, while OWASP documents the purpose and deployment risks of HSTS.|
| IIS **10**, ASP.NET MVC **5.3**, .NET Framework **4.7.4136.0**, jQuery **1.10.2** plus bundled jQuery **3.4.1** | A legacy application stack and two jQuery generations warrant dependency and support review | Version banners alone do not demonstrate a vulnerability | Confirm exact loaded files, patch levels, and runtime support under authorization; do not infer exploitability from banners |
| Verbose YSOD appeared on **four triggers** with `customErrors` off | Detailed exceptions can disclose internals and create response oracles | It does not prove code execution or data access | Enable production-safe error handling, preserve correlation IDs server-side, and test regression. OWASP treats verbose error handling as an information-disclosure risk.|
| MVC antiforgery was enforced; antiforgery cookie was `HttpOnly` without `Secure` | CSRF control is present, but the cookie is not explicitly restricted to HTTPS | This was the antiforgery cookie, not necessarily an authentication cookie; current exploitability is reduced if HTTP is genuinely unreachable | Set `Secure`, review `SameSite`, and separately inventory every authentication/session cookie. OWASP explains that the `Secure` attribute prevents transmission over unencrypted channels.|
| `trace.axd` returned **403** and `elmah.axd` returned **404** | One diagnostic endpoint appeared access-controlled and another absent on tested paths | It does not prove that alternate routes, virtual directories, or management endpoints are absent | Retain the restrictive configuration and verify through authenticated configuration review rather than route guessing |
| Two error families were observed: MVC **2,733 bytes** and IIS **1,216 bytes** | Requests appear to reach different handling layers | It does not identify a bypass by itself | Normalize external error responses and correlate internal logs by request ID |
| On the measured route, GET was accepted; POST and PUT returned **411**; other methods returned **404** | Route/server handling differs by method and content-length expectations | It does not establish a site-wide method policy | Verify per route from configuration and automated regression tests |
| `enc` produced **4,942-byte** `FormatException` output for invalid Base64, **5,084-byte** `CryptographicException` output for valid Base64, and a third size for an empty value | The parameter exposes at least three distinguishable processing states | It does not prove plaintext recovery, chosen-ciphertext exploitation, or authentication bypass | Remove exception detail, equalize failure handling, and perform cryptographic design review only under the application scope letter |
| Host, `X-Forwarded-Host`, absolute-URI, and trust-based error-bypass probes were clean | The tested variants produced no finding | It does not prove that every proxy, cache, or alternate hostname path is safe | Record as a negative test with exact request evidence; do not overgeneralize |
| The campaign never authenticated; guest, consent, app/SP, device-code, and PRT paths were untouched | Identity-control coverage is **ABSENT** | It says nothing reliable about the target’s actual Entra security posture | Launch a new, explicitly scoped identity campaign |

The crucial distinction is between a **coverage finding** and a **security finding**. The evidence strongly supports “not assessed”; it does not support either “compromisable” or “secure.”

---

## 2. Three Tenants Expand the Review to Six Trust Directions

Microsoft’s cross-tenant controls distinguish inbound from outbound access and can separately address B2B collaboration, B2B direct connect, tenant restrictions, and trust of MFA or device claims.Therefore, **three confirmed tenant IDs imply six ordered policy relationships**:

| Direction | Required questions |
|---|---|
| Tenant A → Tenant B | Can A users enter B? Does B trust A’s MFA, compliant-device, or hybrid-join claims? |
| Tenant B → Tenant A | Are outbound restrictions from B and inbound restrictions at A equivalent or materially different? |
| Tenant A → Tenant C | Are collaboration and application access explicitly allowed or inherited from defaults? |
| Tenant C → Tenant A | Can C guests access A resources, and how are those guests governed? |
| Tenant B → Tenant C | Is direct connect, cross-tenant synchronization, or B2B collaboration configured? |
| Tenant C → Tenant B | Are tenant restrictions and trust claims aligned with the reverse direction? |

This six-direction count is an **inference based on the reported three distinct tenants**. It should be confirmed from authoritative tenant IDs, verified domains, and portal application ownership after authorization.

The assessment should also identify which tenant owns the portal’s enterprise application, which tenant contains student accounts, whether staff or administrators reside elsewhere, and whether any of the three is merely a resource tenant. A login domain, verified domain, and tenant-local service principal are not interchangeable concepts; an application object has one home tenant while service principals are instantiated in consuming tenants.

### Recommended three-tenant deliverable

Create one signed matrix containing:

1. Authoritative tenant ID and verified domains.
2. Business owner and security owner.
3. Portal application object ID and tenant-local service-principal object ID.
4. Inbound and outbound defaults.
5. Per-organization overrides.
6. MFA, compliant-device, and hybrid-join trust settings.
7. B2B collaboration and direct-connect status.
8. Cross-tenant synchronization configuration.
9. Guest invitation and redemption restrictions.
10. Log destination, retention, and incident-response owner.

Do not infer this matrix from login-page branding. Obtain it through read-only administrative exports after the letter is signed.

---

## 3. The Entra/M365 Technique Universe to Cover

The table below describes the major technique families relevant to this target. MITRE maps cloud-account use, additional cloud credentials, cloud roles, device registration, token theft, and token reuse to separate ATT&CK techniques, reinforcing that “identity testing” is not a single test case.

| Technique family | Authorized assessment objective | Principal control | Detection counterpart | Gate |
|---|---|---|---|---|
| Tenant and federation topology | Confirm tenant IDs, verified domains, application home tenant, resource tenants, federation, and cross-tenant relationships | Maintained ownership inventory; restricted domain/federation administration | Audit changes to domains, federation, and cross-tenant policies | Public metadata review may be low risk; authenticated enumeration requires letter |
| Guest invitation policy | Determine who can invite guests, allowed/blocked domains, guest visibility, and default guest restrictions | Restrict inviters; use explicit collaboration policy and sponsor ownership | Audit external-user invitations and additions | Letter plus controlled guest mailbox |
| Guest redemption and lifecycle | Validate redemption, account matching, invitation expiry, guest-to-member changes, orphan handling, and removal | Access reviews, entitlement lifecycle, sponsor recertification | Sign-in logs plus guest-object and access-review evidence | Letter plus member and guest test accounts |
| Cross-tenant claim trust | Verify whether MFA, compliant-device, or hybrid-join claims from each external tenant are trusted | Explicit per-tenant inbound/outbound rules | Cross-tenant sign-in fields and Conditional Access results | Read-only review first; controlled sign-in later |
| User consent | Determine whether ordinary users can grant delegated permissions and under what publisher/permission conditions | Restrict consent to verified publishers and selected low-impact permissions where appropriate | Audit OAuth delegated grants and new service principals | Letter plus benign canary app |
| Admin consent workflow | Test whether denied user consent enters a governed, time-limited review process | Admin consent workflow with accountable reviewers | Workflow request, decision, grant, and reviewer audit trail | Letter; sponsor-operated reviewer |
| Illicit consent resistance | Validate that branding, incremental consent, multi-tenant apps, and `offline_access` do not bypass governance | Permission classification, verified publisher policy, app governance | New grant, unusual scope, first-seen publisher, and anomalous API use | No live phishing; controlled canary only |
| App registration | Test whether standard users can register applications and create tenant-local service principals | Disable broad registration if unnecessary; delegate through controlled roles/processes | “Add application,” “Add service principal,” owner changes | Letter plus standard member account |
| App and SP ownership | Identify excessive owners and whether owners can add credentials or redirect URIs without independent approval | Minimal owners, separation of duties, monitored change process | Owner additions and application updates | Read-only first; controlled mutation later |
| Credential addition | Assess secrets, certificates, federated credentials, lifetime, expiry, and unmonitored credential injection | Prefer certificates or federated credentials; enforce credential policies | Audit added passwords, keys, or federated credentials | Controlled canary app only |
| Application permissions | Enumerate app-only Graph, Exchange, SharePoint, Teams, and directory permissions | Least privilege; admin consent governance; periodic review | App-role assignments and service-principal sign-ins | Read-only grant enumeration |
| Workload identity abuse | Identify overprivileged service principals, unattended credentials, and weak Conditional Access coverage | Workload-identity Conditional Access where supported; credentialless federation | Service-principal sign-in logs and workload risk detections | Letter; no production-secret use |
| Device-code flow | Determine which apps and policies permit device-code authentication and whether users recognize the official flow | Block device code where not required; scope Conditional Access by authentication flow | Sign-in protocol, app ID, IP, user agent, CA result | Letter, test account, approved app; no deceptive phishing |
| Device registration abuse | Test whether users can register or join uncontrolled devices and gain policy advantages | Restrict join/registration; require compliant managed devices | Device addition, owner change, join type, subsequent sign-ins | Letter plus disposable managed test device |
| PRT issuance and trust | Validate join state, TPM protection, MFA claim, session controls, and browser SSO assumptions | Managed devices, phishing-resistant MFA, token protection where supported | Device-bound sign-in details and token-protection status | Posture review first; token handling requires enhanced red-team scope |
| Token theft and replay | Evaluate revocation, Continuous Access Evaluation, sign-in risk, and session binding | CAE, token protection, session controls, rapid response | Impossible travel, unfamiliar token/app use, revocation response | No live theft; canary tokens only in isolated lab |
| Password and legacy authentication | Determine whether SLCM sees a password directly, redirects to Entra, or uses a legacy grant | Standards-based federation; disable legacy/ROPC paths; MFA/passwordless | Sign-in protocol and application correlation | Letter plus test accounts; never use real student credentials |
| Privileged roles and PIM | Enumerate standing roles, role-assignable groups, activation requirements, and emergency accounts | PIM, approval, MFA, time-bound activation, monitored emergency accounts | Role assignment, activation, denial, and emergency-account use | Read-only role review; no privilege activation unless explicit |
| Logging and response | Confirm collection of interactive, noninteractive, service-principal, managed-identity, audit, and M365 workload logs | Central export, retention, alerting, immutable case evidence | SIEM analytics and incident workflow | Configure before any active exercise |

Microsoft documents guest controls, user-consent options, admin consent workflow, workload-identity Conditional Access, access reviews, PIM, and emergency-access account design.These controls should be assessed as one system: a restrictive consent setting can still be undermined by excessive app owners, while strong MFA can still leave risky device-code or token-replay paths.

---

## 4. The Password Claim Requires Architecture Verification

The statement that “the portal password is the M365 password” has at least three possible explanations:

| Possible architecture | Security meaning | How to distinguish safely |
|---|---|---|
| Standards-based Entra SSO | The user authenticates at Microsoft, and the portal receives tokens rather than the password | Record the authorized browser redirect chain, issuer, client ID, tenant ID, and resulting Entra sign-in entry |
| Legacy direct authentication against Entra | The portal or backend receives the password and exchanges or validates it through a legacy mechanism | Examine application configuration and sign-in protocol with the owner; do not capture a production password |
| Separate credential store synchronized by policy or user behavior | The same password exists in two systems, creating independent compromise and reset problems | Review design documentation and perform password-reset behavior testing only with the two test accounts |

This is an **inference tree**, not a claim that any one implementation exists. Microsoft warns that ROPC requires an application to handle the user’s password and does not support several modern authentication scenarios.Consequently, the highest-value test is not a password spray; it is proving which architecture is in use.

A standards-based redirect should produce a traceable Entra sign-in for the portal application. A direct HTML form that submits the password to the SLCM origin would justify immediate architecture review, but even that visual observation should be confirmed server-side before assigning severity.

---

## 5. Tools: Defensive Assessors, Graph Clients, and Restricted Red-Team Utilities

No defensible report can guarantee a list of literally **every** public tool: forks, private commercial products, and short-lived scripts change continuously. The following is a broad inventory of publicly documented tools materially relevant to the requested techniques. Repository licenses can change, so the current `LICENSE` file must be checked before institutional redistribution.

“BYOK” is generally not the relevant model here. These tools normally use an authorized tenant identity, service principal, certificate, or delegated OAuth session. Tenant credentials and tokens must never be uploaded to an unapproved hosted service.

### Configuration, graph, and posture tools

| Tool and exact URL | Licence / availability | How it is driven | Relevant coverage | Typical output |
|---|---|---|---|---|
| Microsoft Entra admin center and Graph Explorer[34] | Microsoft-hosted; Graph Explorer is free to use with granted tenant permissions | Browser UI and REST requests | Guests, grants, apps, SPs, roles, policies, logs | UI tables, downloadable CSV where offered, REST JSON |
| Microsoft Graph PowerShell SDK[35] | MIT; free and self-hosted | PowerShell with delegated or application authentication | Broad read/write Graph coverage, including invitations, apps, grants, and logs | PowerShell objects; JSON/CSV when exported |
| Azure CLI[36] | MIT; free and self-hosted | Command line using authorized Azure/Entra authentication | App registrations, service principals, role and tenant metadata | JSON, JSONC, table, TSV, YAML |
| Maester[37] | MIT; free and self-hosted | PowerShell/Pester and CI workflows | Entra and Microsoft 365 control tests, drift, evidence | Console/Pester results, HTML reporting, CI-compatible test results |
| ScubaGear[38] | CC0/public-domain dedication; free and self-hosted | PowerShell modules against M365 services | CISA Secure Cloud Business Applications baseline checks | HTML and machine-readable assessment artifacts documented by the project |
| Monkey365[39] | GPL-3.0; free and self-hosted | PowerShell with tenant scopes | Entra, Azure, and M365 configuration review | HTML, JSON, CSV |
| Prowler[40] | Apache-2.0; free/self-hosted, with optional commercial service | Python CLI or container | Azure/M365 posture checks and compliance mappings | CSV, JSON/OCSF, HTML |
| Microsoft365DSC[41] | MIT; free and self-hosted | PowerShell Desired State Configuration | Export, compare, and govern tenant configuration | PowerShell configuration files and comparison/report artifacts |
| EntraExporter[42] | MIT; free and self-hosted | PowerShell | Entra configuration snapshot and version-controlled drift review | Structured JSON exports |
| AzureHound[43] | GPL-3.0; free and self-hosted | Compiled CLI collector using authorized tenant access | Graph relationships involving users, groups, roles, apps, and service principals | BloodHound-compatible JSON |
| ORCA[51] | MIT; free and self-hosted | PowerShell module | Microsoft security configuration analysis, especially Exchange Online protection | HTML report |

**Takeaway:** Maester, ScubaGear, Monkey365, Prowler, Microsoft365DSC, and EntraExporter overlap but are not interchangeable. Use at least one baseline assessor plus a raw Graph export so that a failed or incomplete check does not become a blind spot.

### Exercise, investigation, and high-risk tools

| Tool and exact URL | Licence / availability | How it is driven | Relevant capability | Output and restriction |
|---|---|---|---|---|
| ROADtools[44] | MIT; free and self-hosted | Python CLI and local web interface | Tenant reconnaissance, object/grant analysis, and advanced token/device research | Local SQLite database and interactive views; token functions require explicit red-team scope |
| AADInternals[45] | MIT; free and self-hosted | PowerShell module | Entra reconnaissance, federation, device, token, guest, and application research | PowerShell objects and console output; high-risk functions restricted to lab/test identities |
| GraphRunner[46] | Public source; verify repository licence before reuse | PowerShell | Graph-based enumeration and post-authentication identity testing | Console and module-dependent file output; authorized red-team use only |
| TokenTactics[47] | Public source; verify repository licence before reuse | PowerShell | Device-code and token-oriented research | Token/console objects rather than an audit report; never operate against real users |
| Sparrow[48] | CC0; free and self-hosted | PowerShell | CISA incident-response collection for Azure/M365 | CSV and supporting evidence files |
| Untitled Goose Tool[49] | CC0; free and self-hosted | Python CLI | Collection and analysis of Azure, Entra, and M365 investigation data | Structured local investigation output, including CSV/JSON-style artifacts |
| Hawk[50] | Open-source PowerShell project; verify current repository licence | PowerShell module | M365/Entra compromise investigation | CSV and text-based forensic collections |
| Microsoft Purview Audit[28] | Commercial Microsoft cloud service; licence-dependent | Portal, PowerShell, or API search | Unified M365 audit evidence | Search tables, CSV export, API results |
| Defender for Cloud Apps/App Governance[29] | Commercial; licence-dependent | Microsoft portal, APIs, and policies | Risky OAuth apps, app behavior, grant investigation | Alerts, app inventory, investigation records |
| Microsoft Defender XDR Advanced Hunting[30] | Commercial; licence-dependent | KQL in portal or API | Cross-workload identity and endpoint correlation | KQL result tables, CSV/JSON through export/API |
| Microsoft Sentinel[31] | Azure service; ingestion and retention charges may apply | Data connectors, KQL, analytics rules, playbooks | Entra audit/sign-in detection and incident response | Log Analytics tables, incidents, JSON/CSV exports |

**Takeaway:** ROADtools, AADInternals, GraphRunner, and TokenTactics are not pre-authorization assessment utilities. Their inclusion identifies the relevant public tooling universe; it is not authorization to operate them against MUJ, its users, devices, or tenants.

### Native Graph operations that cover gaps

Microsoft Graph exposes a dedicated invitation resource and represents delegated consent through `oauth2PermissionGrant` objects.Native Graph is often preferable to a specialized tool because it provides an auditable, read-only query path and predictable JSON evidence.

Use a purpose-created read-only assessment service principal where possible. Do not grant broad Graph permissions merely to make a scanner convenient; the assessment identity itself would become a new high-value workload credential.

---

## 6. Manual Methods Where Automation Is Insufficient

Some identity questions require business context, user observation, or a controlled state transition. A scanner can enumerate a grant but cannot decide whether that grant is justified.

| Gap | Authorized manual method | Success criterion | Cleanup and evidence |
|---|---|---|---|
| Portal authentication architecture | With a test account, capture a sanitized browser flow and correlate it to the Entra sign-in log; have the owner confirm server-side protocol/configuration | Clear determination of OIDC/SAML redirect, legacy credential flow, or separate store | Remove passwords and tokens from HAR files; retain client ID, issuer, timestamps, correlation ID, and screenshots |
| Six-direction tenant trust | Export inbound/outbound settings from each tenant and conduct one controlled sign-in per approved direction | Policy and observed result agree in all six directions | Record tenant IDs, CA result, trusted claims, and denied/allowed outcome |
| Guest invitation lifecycle | Invite only the approved external mailbox, redeem it, assign a harmless test resource, review it, and remove it | Invitation, redemption, review, and deletion are all logged and governed | Delete guest, invitation, group assignment, and access package; preserve audit IDs |
| Consent governance | Use a benign canary app requesting only approved low-impact delegated permissions; test denial, workflow, approval, revocation, and re-consent | Policy behaves as documented, with accountable reviewer and complete audit trail | Remove grant, service principal, and canary app; revoke test-account sessions |
| App registration policy | Ask the standard member test account to attempt creation of a clearly named canary app without adding sensitive permissions | Result matches policy; owner/credential actions are independently governed | Delete object and SP; search for residual grants, credentials, owners, and sign-ins |
| Device-code controls | Use an approved test application and have the test user intentionally complete the legitimate Microsoft-hosted flow—without deception | Conditional Access result and telemetry match policy | Revoke sessions, remove app grant, retain sign-in record; never retain the token |
| PRT/device posture | Enroll or join a disposable organization-issued test device, verify PRT-related posture and device-bound controls through supported diagnostics and logs | Unmanaged or untrusted devices cannot obtain privileged access; token-protection status is visible where supported | Remove device registration, retire the test device, revoke sessions |
| Incident-response readiness | Generate the above benign canaries while the SOC observes | SOC detects, triages, identifies owner, and executes cleanup within agreed objectives | Preserve case IDs, alert timestamps, source logs, and lessons learned |

The consent test must not imitate a university login page or solicit a real user. The device-code test must not use deceptive messaging. PRT extraction or replay is unnecessary for the initial control assessment and should be treated as a separate endpoint-red-team exercise.

---

## 7. Detection Counterparts for Every Tested Technique

Entra provides separate sign-in views for interactive users, noninteractive users, service principals, and managed identities; its audit logs record directory and policy changes.Because native retention varies by report and licence, Microsoft recommends routing logs through diagnostic settings when longer retention or external analysis is required.

| Technique or event | Primary evidence | Detection logic | Required response |
|---|---|---|---|
| External invitation | Entra audit log | First-seen inviter, unusual invitation volume, unapproved domain, or invitation outside business process | Validate sponsor; disable or remove unauthorized guest; review assigned resources |
| Guest redemption and sign-in | User sign-in log plus guest object | New home tenant, unusual IP/device, failed CA, or resource access immediately after redemption | Suspend access, revoke sessions, inspect invitation and assignments |
| Cross-tenant access | Sign-in properties including home/resource tenant and cross-tenant type | Previously unseen tenant pair, unexpected trust claim, or policy mismatch | Block pair if unauthorized; correct inbound/outbound policy |
| User consent | Audit log and delegated permission grant | New app, first-seen publisher, risky scope combination, `offline_access`, or grant outside approved catalogue | Revoke grant, disable SP, investigate user and app |
| Admin consent | Audit log, app-role assignments, consent workflow | Tenant-wide grant, high-impact Graph/M365 permission, unexpected approver | Revoke grant; remove credentials; assess data accessed |
| App registration | Audit log | Standard user creates app despite policy, suspicious naming, multitenant setting, or unexpected redirect URI | Disable/delete app and SP; investigate owner and associated grants |
| Owner addition | Audit log | New owner outside app team, guest owner, or owner added shortly before credential creation | Remove owner; rotate credentials; review all app changes |
| Secret/certificate/federated credential addition | Audit log | Credential added outside deployment pipeline, long validity, unknown issuer/subject | Remove credential, disable SP, examine sign-ins |
| Application permission assignment | Audit log plus SP inventory | High-impact app role granted to unapproved SP | Revoke role; search service-principal sign-ins and affected workloads |
| Service-principal sign-in | Service-principal sign-in log | New IP, geography, resource, credential key, or unusual volume | Disable SP or credential; rotate; assess API access |
| Device-code authentication | User sign-in log and CA details | Device-code protocol for an app/user with no business need, unfamiliar IP/user agent, or CA bypass | Revoke session, disable app, investigate user communications |
| Device registration/join | Audit log and device inventory | Unmanaged device, unusual owner, excessive registrations, or join followed by privileged access | Disable/delete device; revoke user sessions; inspect CA |
| PRT or token anomalies | Sign-in logs, endpoint telemetry, token-protection details where available | Token use inconsistent with device, location, session, or risk; protected resource accessed without expected binding | Revoke sessions, disable device/account, isolate endpoint |
| Privileged-role change | Audit log and PIM | Standing assignment, role-assignable group change, approval bypass, unusual activation | Remove assignment; investigate initiator; review subsequent actions |
| Portal/Entra seam | IIS/application logs plus Entra sign-ins | Successful portal session without corresponding expected Entra event, mismatched user/tenant, or repeated failure oracle | Disable affected path/session; correlate app and identity incident |

The exact friendly operation labels can vary by portal and API version. Detection engineering should preserve the raw operation name, activity ID, correlation ID, initiator, target resource, modified properties, tenant IDs, app ID, service-principal ID, IP, user agent, Conditional Access result, and timestamp. The Microsoft Graph `signIn` resource documents many of the fields needed for cross-tenant and application correlation.

Purview Audit adds M365 workload activity, App Governance helps investigate risky OAuth applications, Defender XDR enables cross-domain hunting, and Sentinel can centralize Entra data.None should be assumed enabled merely because the institution licenses Microsoft 365.

---

## 8. Recommended Control Baseline for This Target

### Guest and cross-tenant controls

Restrict guest invitation to an accountable set of users or the Guest Inviter role rather than allowing uncontrolled invitation. Configure guest directory visibility, collaboration restrictions, and domain rules according to university partnerships.

For each of the **six directions**, set explicit inbound and outbound rules. Trust external MFA or device claims only from partner tenants with documented governance; do not treat the three enumerated tenants as automatically trusted merely because they are associated with the same university.

Use access reviews or equivalent sponsor recertification to remove abandoned guests.Guest cleanup should include direct assignments, group membership, Teams, SharePoint sites, enterprise apps, and access packages.

### Consent, apps, and service principals

Configure user consent around approved low-impact permissions and publisher conditions rather than unrestricted consent. Use the admin consent workflow for requests requiring review.

Review whether ordinary users can register applications. Microsoft documents default user permissions that can include application registration, but institutions can restrict them and delegate controlled application-development roles.Monitor app owners because ownership can confer significant management power even without a directory role.

For every application and service principal, record:

- Business and technical owner.
- Publisher and verification state.
- Single-tenant or multitenant status.
- Redirect URIs.
- Delegated grants and app-role assignments.
- Owners.
- Secrets, certificates, and federated credentials.
- Last user and service-principal sign-in.
- Data owner approval.
- Expiry and review date.

Prefer certificate-based or workload identity federation over long-lived shared secrets where the platform supports it.Conditional Access for workload identities can cover service principals in supported scenarios, but it is not a universal substitute for permission reduction and does not protect every workload identity type.

### Device code, PRT, and session controls

Block device-code authentication where there is no business requirement; otherwise, limit it through Conditional Access authentication-flow controls.An approved exception should identify the application, user population, device scenario, owner, and expiration date.

A PRT is part of Entra device SSO and is associated with device registration/join and a session key.Assessment should therefore cover device-join permissions, TPM-backed protection, endpoint privilege, compliance, browser SSO, and device removal—not just MFA.

Token protection can bind supported sign-in tokens to devices, but Microsoft documents platform, resource, client, and licensing limitations.Continuous Access Evaluation can improve response to selected critical events but is likewise not a universal instant-revocation mechanism.

### Privilege and emergency access

Move eligible administrative roles to PIM with time-limited activation, approval where appropriate, MFA, and notification.Maintain emergency-access accounts according to Microsoft’s guidance and monitor every use.

If each of the three tenants independently follows Microsoft’s recommendation for at least two emergency accounts, that implies **at least six emergency accounts across the three tenants**. This is a planning inference, not evidence that six accounts currently exist.

---

## 9. Authorization Matrix: What Is Safe Before and After the Letter

“Safe” does not mean legally authorized in every jurisdiction or under every university policy. The institution’s rules and owner approval remain controlling.

| Activity | Pre-authorization status | Requirements after authorization |
|---|---|---|
| Review supplied screenshots, headers, reports, and public Microsoft documentation | **Safe** | None beyond normal data handling |
| Build test cases, detection queries, cleanup scripts, and evidence templates offline | **Safe** | Validate in an owned lab tenant |
| Review public certificate-transparency and ordinary public DNS information at low volume | **Generally low risk**, subject to institutional policy | Do not extend into account or tenant-user enumeration |
| Make ordinary browser GET requests to the public portal | Only if university policy permits; avoid repeated oracle probing | Scope must specify rate, routes, source IPs, dates, and contacts |
| Query tenant metadata, federation, or user-existence endpoints for reconnaissance | **Do not continue pre-authorization** | Scope exact domains, endpoints, rate, and data retention |
| Authenticate to SLCM or any Entra tenant | **Prohibited pre-authorization** | Signed letter and named test accounts |
| Send a guest invitation | **Prohibited** | Controlled mailbox, sponsor, cleanup plan |
| Present or approve a consent prompt | **Prohibited** | Canary app, approved permissions, sponsor-operated reviewer |
| Create an application or service principal | **Prohibited** | Naming convention, owner, expiry, deletion procedure |
| Add a secret, certificate, federated credential, owner, or permission | **Prohibited** | Canary object only; no production app mutation |
| Execute device-code authentication | **Prohibited** | Test user, approved test app, no deception |
| Register/join a device | **Prohibited** | Disposable managed device and documented removal |
| Extract, replay, or retain PRT/access/refresh tokens | **Prohibited** | Separate enhanced red-team authorization, isolated device, canary identity, secure evidence controls |
| Test passwords, MFA fatigue, spraying, or phishing | **Prohibited** | Not part of the proposed initial campaign; requires exceptional separate authorization |
| Read Entra/M365 logs through Graph or portals | **Prohibited without tenant authorization** | Least-privilege read-only identity and approved evidence storage |

The two test accounts should ideally be:

1. A standard, nonprivileged member in the portal’s home tenant.
2. A controlled external account in one of the other scoped tenants or an approved test tenant.

Admin-consent and policy-review actions should be performed by a sponsor-operated administrative account, not by converting either research account into a standing administrator.

---

## 10. NO-TOOL GAPS and BUILD CANDIDATES

Current products enumerate objects and test generic baselines well, but they do not completely solve the target-specific questions below.

| Gap | Why existing tools fall short | Build candidate | Safety properties | Output |
|---|---|---|---|---|
| Three-tenant directional trust diff | Most reports assess one tenant at a time and obscure asymmetric inbound/outbound rules | **Three-Tenant Trust Mapper** | Read-only Graph access; no sign-ins or policy writes | JSON source snapshot, six-direction HTML matrix, SARIF findings |
| Consent semantics | Tools list scopes but rarely combine publisher status, grant type, owner, credential age, usage, and data sensitivity | **Consent Surface Linter** | Read-only; local permission catalogue; no consent generation | JSON/CSV inventory and risk-ranked SARIF |
| Canary lifecycle | Manual guest/app tests often leave residual objects, grants, or credentials | **Identity Canary Orchestrator** | Allowlisted object prefix; dry run; expiry; transaction log; mandatory cleanup verification | Signed JSON manifest, evidence bundle, cleanup attestation |
| Device-code detection validation | A successful or blocked login does not prove the SOC correlated the protocol, app, user, IP, and CA result | **Device-Code Telemetry Validator** | Approved app/account only; no deceptive content; token discarded immediately | Timeline JSON and detection pass/fail report |
| PRT posture without token theft | Offensive tools focus on obtaining or using tokens, while defenders need a safer control assessment | **PRT Posture Assessor** | Collects policy, device, and log metadata only; never reads token material | Device/control matrix, JSON evidence, remediation report |
| Portal-to-Entra architecture proof | Browser capture can leak secrets and scanners cannot reliably distinguish redirect from backend credential handling | **Sanitized Auth-Flow Recorder** | Automatic password, cookie, code, and token redaction; allowlisted hosts | Redacted HAR, redirect diagram, issuer/client/tenant summary |
| App/SP ownership drift | Generic tools flag permissions but may not identify owner-to-credential-to-role attack paths | **Workload Identity Drift Graph** | Read-only snapshot comparison; no graph mutation | Versioned JSON and owner/credential/role change alerts |
| Evidence normalization | Maester, ScubaGear, Graph, Sentinel, and manual tests emit different formats | **Identity Evidence Packager** | Local processing; provenance hashes; secret scanning | SARIF, JSON, HTML executive report, evidence manifest |

SARIF is an OASIS-standardized machine-readable format suitable for normalizing findings into development and security workflows.The build candidates should also emit raw JSON so findings remain independently verifiable.

The most valuable candidate is the **Three-Tenant Trust Mapper** because the target’s unusual feature is not simply “uses Entra”; it is the reported presence of **three tenants** with no completed cross-tenant assessment. The safest initial product is the **PRT Posture Assessor**, because it answers many defensive questions without handling a PRT.

---

## 11. Recommended Campaign Sequence

### Phase 0 — Before authorization

1. Freeze the supplied **2026-09-13** evidence.
2. Obtain application, identity, SOC, and legal owners.
3. Draft exact tenant IDs, domains, source IPs, dates, test windows, stop conditions, and emergency contacts.
4. Prepare canary naming and guaranteed cleanup conventions.
5. Build detections before generating events.
6. Validate all tooling in an owned lab tenant.

No authentication, invitation, consent, registration, device-code, or token activity should occur in this phase.

### Phase 1 — Signed letter, read-only access

1. Confirm all three tenant IDs and application ownership.
2. Export guest, cross-tenant, consent, app-registration, Conditional Access, device, role, and logging policies.
3. Inventory apps, service principals, grants, owners, credentials, and sign-in recency.
4. Export interactive, noninteractive, service-principal, managed-identity, audit, and Purview coverage.
5. Run Maester plus either ScubaGear or another approved baseline, then reconcile against raw Graph data.

A scanner failure should be reported as an evidence limitation, not silently converted into a pass.

### Phase 2 — Controlled state transitions

1. Invite and remove one controlled guest.
2. Exercise one low-impact delegated consent request.
3. Test the admin consent workflow without granting high-impact data access.
4. Attempt standard-user canary app registration.
5. Add and remove only a canary credential if explicitly allowed.
6. Validate service-principal and app-role alerts.
7. Test all approved tenant directions.

Every mutation needs an object ID, owner, creation timestamp, expiry, cleanup action, and post-cleanup verification.

### Phase 3 — Device and session controls

1. Conduct an intentional, nondeceptive device-code sign-in.
2. Register or join a disposable managed test device if in scope.
3. Confirm PRT-related posture through supported diagnostics and sign-in evidence.
4. Validate token-protection and CAE behavior where supported.
5. Exercise session revocation.
6. Conduct a SOC tabletop around suspected consent or token compromise.

Token extraction or replay should remain outside this phase unless the scope letter separately and explicitly authorizes it.

---

## VERDICT

### Campaign status: **ABSENT**

The available record shows that the campaign never authenticated and did not examine guest invitation, illicit consent, application or service-principal abuse, device-code flow, device registration, PRT handling, cross-tenant trust, or identity detection. Therefore, the Entra/M365 control plane has **no meaningful campaign coverage**.

### Security posture: **INDETERMINATE**

The report cannot responsibly conclude that MUJ SLCM is vulnerable to any of these techniques. Three tenants and a shared M365 authentication context increase the number and potential impact of failure paths, but actual exploitability depends on policies, grants, application ownership, device management, and telemetry that were never observed.

### Priority: **HIGH**

The identity workstream deserves priority because:

- There are reportedly **three tenants**, producing **six directional trust relationships**.
- The portal credential is reportedly the Microsoft 365 credential, creating a potentially broad blast radius.
- Consent grants and service principals can provide durable API access independent of the portal.
- Device-code and PRT paths can bypass assumptions based solely on password-form or web-application testing.
- The current web findings expose information and response distinctions but do not answer the larger identity questions.

### Confidence

| Conclusion | Confidence | Basis |
|---|---:|---|
| Identity campaign coverage is absent | **High** | Explicit campaign record: no authentication and named technique families untouched |
| Three tenants require six directional policy reviews | **High**, conditional on the three-tenant fact | Mathematical consequence of asymmetric inbound/outbound policy |
| Portal/M365 credential linkage materially raises potential impact | **Medium-High** | Reported shared credential context; authentication architecture remains unknown |
| Any particular consent, guest, app, device-code, or PRT exploit is currently possible | **Low** | No authenticated policy or behavioral evidence |
| A telemetry-first authorized campaign will substantially improve assurance | **High** | It directly closes the documented evidence gaps and creates detection validation |

**Final decision:** Do not treat the previous campaign as evidence that the Entra/M365 layer is secure. Obtain the signed letter, provision the two controlled accounts and a disposable test device, enable/export telemetry, and execute the staged plan. Until then, the accurate status remains **ABSENT / NOT ASSESSED**, not vulnerable and not cleared.

---