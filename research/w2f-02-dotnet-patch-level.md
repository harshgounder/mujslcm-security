# MUJ SLCM .NET 4.7.4136.0 Security Assessment

## Executive Summary

- **Build Identification**: The exact value `4.7.4136.0` maps in public Windows binary metadata to `System.Web.dll` built from the `NET472REL1LAST_B` branch. This supports a **.NET Framework 4.7.2 servicing-line** identification, not a claim that the server has only the original April 2018 4.7.2 release installed [34]. -> Treat the banner as a branch clue, not a patch verdict.

- **No Unique KB Mapping**: The same `System.Web.dll` version and hashes occur in packages for Windows 10 version 1607 and Windows Server 2016 build 14393 from October 2025 through July 2026 [34]. -> It is technically unsound to translate `4.7.4136.0` into one unique KB, patch date, or "last updated" date.

- **Authoritative Local Test**: Microsoft says the installed .NET Framework 4.5-or-later version is represented by the `Release` REG_DWORD under `HKLM\SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full`; the documented minimum values are 461808 for 4.7.2, 528040 for 4.8, and 533320 for 4.8.1 [4]. -> An authorized administrator must collect that value, the Windows build, and installed cumulative KBs before declaring the host unpatched.

- **Cumulative Servicing Matters**: Microsoft describes .NET Framework updates as cumulative security and reliability improvements, recommends applying them routinely, and directs customers to Windows Update or the Microsoft Update Catalog for the latest secure version [1]. -> A genuinely unpatched 4.x installation in 2026 may be missing years of fixes even when a visible `System.Web.dll` version has not changed.

- **Serious Historical Exposure Classes**: The Framework and ASP.NET history includes remote code execution, denial of service, information disclosure, security-feature bypass, and privilege-escalation CVEs. Examples include CVE-2018-8421, rated CVSS 3.0 9.8 and explicitly associated with Framework 4.7.2, and CVE-2021-24111, a network-reachable denial of service whose NVD configurations explicitly include 4.7.2 [25][24]. -> Missing applicable updates can have high impact, but a CVE title alone does not prove that MUJ is vulnerable.

- **2026 Risk Is Still Evolving**: NVD records published in July and August 2026 describe .NET Framework issues involving local code execution, code injection, relative path traversal, and network-based privilege elevation [28][31][26][27][30]. -> Current patch compliance must be checked against 2026 servicing, not against a historical framework-name banner.

- **Edge And Identity Controls Are Not Runtime Patches**: [Inference] Under the requester-supplied architecture, Akamai may reduce exposure to some hostile requests and Microsoft 365 identity may restrict access, but neither changes the origin's Framework binaries. The CVE set also contains local and authorized-attacker scenarios that are outside a simple perimeter-filter model [28][30]. -> Preserve these controls, but do not count them as compensating evidence for missing OS or Framework updates.

- **Separate ASP.NET Dependencies**: Microsoft states that ASP.NET ships external components separately from .NET Framework [2]. -> The requester-supplied ASP.NET MVC 5.3 fingerprint and any OWIN, Katana, identity, JSON, or other application-local packages require a separate software-composition inventory.

- **Bottom Line**: The evidence supports **"4.7.2 servicing lineage" with high confidence**, but supports neither **"unpatched" nor "patched"** from the banner alone. -> The correct club finding is "patch state indeterminate; owner-side verification required," with urgent remediation if current cumulative updates are absent.

## Scope, Evidence Boundaries, And Safe-Research Rules

This assessment concerns the public MUJ SLCM host named by the requester. The publicly retrievable landing page says "WELCOME TO MUJ PORTAL" and exposes sign-in and parent-login choices [32]. The claims that the deployment uses ASP.NET MVC 5.3, IIS 10, Akamai, and Microsoft 365 identity came from the research brief. They are treated as **supplied assumptions**, not as independently proven properties of the live host.

No active scanning, error induction, authentication testing, origin discovery, header manipulation, fuzzing, exploit reproduction, or access-control testing was performed or is recommended without written authorization. All technical conclusions below come from public documentation, public vulnerability records, and public binary metadata. Owner-side checks are described only as defensive administrative validation.

The requested "chain-of-thought" cannot be provided as private hidden reasoning. Instead, this report provides a reproducible evidence-to-conclusion audit trail: observation, source meaning, permitted inference, uncertainty, and the decision that follows.

| Evidence item | What the evidence establishes | What it does not establish | Confidence |
|---|---|---|---|
| Public MUJ page | A MUJ-branded portal with sign-in and parent-login choices is publicly reachable [32] | Backend version, patch level, Akamai configuration, or Microsoft 365 authentication flow | High for visible text; low for backend conclusions |
| `4.7.4136.0` binary metadata | Exact `System.Web.dll` file version belongs to `NET472REL1LAST_B` [34] | Installed `Release` DWORD, latest cumulative KB, or vulnerable code path | High for branch mapping |
| Microsoft version guidance | Registry `Release` value is the supported 4.5+ installed-version indicator [4] | Remote patch state without administrator access | High |
| Microsoft lifecycle policy | Framework 4.5.2+ is an OS component and follows the parent Windows lifecycle [2] | Whether MUJ's parent OS is currently supported or patched | High for policy; unknown for host |
| NVD CVE records | Vulnerability classes, publication dates, and sometimes explicit affected versions | Automatic applicability to this portal | High for listed record; conditional for MUJ |
| Requester-supplied topology | Defines the architecture to analyze | Independent verification of MVC, IIS, Akamai, or Microsoft 365 details | Assumption only |

The immediate takeaway is methodological: a passive banner is useful for narrowing a product lineage, but it cannot substitute for authenticated asset inventory. This distinction prevents both false alarms and false assurance.

## What `4.7.4136.0` Actually Identifies

The strongest public match is not a marketing release named ".NET Framework 4.7.4136.0." It is the file version of `System.Web.dll`. Public Windows binary metadata associates that exact file version with the build branch `NET472REL1LAST_B`, which is a .NET Framework 4.7.2 servicing branch [34]. The defensible wording is therefore:

> `4.7.4136.0` is consistent with the `System.Web.dll` binary from the .NET Framework 4.7.2 servicing lineage.

It should not be rewritten as "the host runs an unpatched April 2018 runtime." Microsoft lists Framework 4.7.2 as released on April 30, 2018 and currently active under its component support model [2]. Release lineage and servicing freshness are separate questions.

Microsoft also distinguishes assembly identity from file metadata. `AssemblyVersion` participates in build-time and runtime assembly location and loading [33]. `AssemblyFileVersion`, by contrast, is the version assigned to the file, appears in Windows Explorer, and is not used by .NET Framework for assembly referencing [33]. A value disclosed through an ASP.NET banner or error artifact therefore needs contextual identification before it is used as a vulnerability claim.

### The repeated-file result disproves a unique patch-date inference

The binary index lists the same version and hashes in numerous later Windows build 14393 package sets [34]. The table reproduces the relevant package chronology exactly as metadata evidence, not as proof that MUJ installed any listed KB.

| Package date | Windows package | Meaning for the version inference |
|---|---|---|
| 2025-10-14 | KB5066836 | Same `System.Web.dll` version remains present |
| 2025-11-11 | KB5068864 | Same file metadata remains present |
| 2025-12-09 | KB5071543 | Same file metadata remains present |
| 2025-12-18 | KB5074974, out-of-band | Same file metadata remains present |
| 2026-01-13 | KB5073722 | Same file metadata remains present |
| 2026-02-10 | KB5075999 | Same file metadata remains present |
| 2026-03-10 | KB5078938 | Same file metadata remains present |
| 2026-04-14 | KB5082198 | Same file metadata remains present |
| 2026-04-19 | KB5091572, out-of-band | Same file metadata remains present |
| 2026-05-12 | KB5087537 | Same file metadata remains present |
| 2026-06-09 | KB5094122 | Same file metadata remains present |
| 2026-07-14 | KB5099535 | Same file metadata remains present |

All rows derive from the exact-version metadata record [34]. They show why file-level version stagnation does not equal machine-level servicing stagnation: cumulative packages can update other Framework or Windows components while leaving an unchanged `System.Web.dll` in the package inventory.

[Inference] If the MUJ value came from that file, the most precise conclusion is branch identity. If it came from a different artifact, the observer must first identify that artifact. In neither case does the number alone establish an exploitable condition.

## Microsoft's 4.x Servicing Model Changes The Interpretation

All .NET Framework versions since 4 are in-place updates, so only one 4.x version can be present on a system [3]. A later 4.x release replaces the earlier 4.x installation, and Microsoft says an administrator does not have to uninstall the earlier release first [3]. This explains why application compatibility labels, CLR identifiers, assembly metadata, and the installed Framework product level can appear related without being interchangeable.

For Framework 4.5 and later, Microsoft's authoritative installed-version method is the local registry. The path is `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full`, and the `Release` REG_DWORD represents the installed version [4]. Microsoft directs checks for a minimum supported level to use a greater-than-or-equal comparison [4].

| Product level | Minimum `Release` value | Proper interpretation |
|---|---:|---|
| .NET Framework 4.7.2 | 461808 | 461808 or greater means at least 4.7.2 |
| .NET Framework 4.8 | 528040 | 528040 or greater means at least 4.8 |
| .NET Framework 4.8.1 | 533320 | 533320 or greater means at least 4.8.1 |

These thresholds are Microsoft's documented minimums [4]. They identify the product release, but a complete patch audit still needs the parent OS build and installed cumulative updates.

Framework 4.5.2 and later is defined as a Windows component and follows the lifecycle of the underlying Windows product [2]. Microsoft lists 4.7.2, 4.8, and 4.8.1 as active; it identifies 4.8.1 as the latest Framework version [2]. This does **not** mean every machine carrying one of those product levels is secure. Active support means updates are available under the applicable parent-product policy; it does not prove they were deployed.

Microsoft says Framework updates contain cumulative security and reliability improvements, recommends regular application of updates, and identifies Windows Update and the Update Catalog as acquisition channels [1]. Consequently, "Framework 4.7.2" can describe both a serviced supported system and a neglected system. The difference is administrative evidence, not the branch label.

## CVE Timeline Through 2020: The 4.7.2 Line Inherited Serious Fixes

Because no authoritative source maps `4.7.4136.0` to one unique release date, an exact "before this binary versus after this binary" split would be false precision. The responsible substitute is a dated servicing-line chronology. The first table covers the pre-4.7.2 lineage and the early 4.7.2 era. "Applicability" records only what the cited NVD text establishes.

| CVE | Published | Vulnerability class | Scope stated by source | MUJ relevance and limit |
|---|---|---|---|---|
| CVE-2017-8759 | 2017-09-12 | Remote code execution | Framework 2.0 through 4.7 are named [17] | Pre-4.7.2 lineage example; not evidence of present exposure |
| CVE-2018-8421 | 2018-09-12 | Remote code execution from untrusted input | NVD names Framework versions through 4.7.2 and reports CVSS 3.0 9.8 [25] | Directly demonstrates that 4.7.2 required security servicing |
| CVE-2019-0545 | 2019-01-08 | Information disclosure through CORS bypass | NVD names .NET Framework and .NET Core [18] | Web-relevant class; exact MUJ configuration is unknown |
| CVE-2019-0820 | 2019-05-16 | Denial of service from improper RegEx processing | NVD names .NET Framework and .NET Core [9] | Availability concern only if an affected path is reachable |
| CVE-2020-1108 | 2020-05-21 | Denial of service from improper web-request handling | NVD names .NET Framework and .NET Core [13] | Potentially web-facing class; exact affected build is not shown in the captured record |
| CVE-2020-1147 | 2020-07-14 | Remote code execution involving source markup in XML input | NVD names .NET Framework, SharePoint, and Visual Studio [20] | Serious class, but workload and affected-component applicability must be established |

The table is a curated, representative list rather than a claim that every entry affects every Framework 4.7.2 host. CVE-2018-8421 provides the clearest early anchor because NVD explicitly includes 4.7.2 and supplies a critical network vector [25]. The others demonstrate why inventory must include enabled components and application behavior, not merely a product-family name.

[Inference] For a university portal, denial of service can disrupt academic workflows even without data theft, while remote code execution or information disclosure can threaten confidentiality and integrity. That impact assessment is conditional: reachability, patch state, and vulnerable code paths remain unverified.

## CVE Timeline From 2021 To August 2026: Servicing Did Not Stop

The later chronology shows continued security work across Framework and ASP.NET. Some NVD records name Framework 4.7.2 explicitly; others name only the broad product family. Broad-family entries should drive an administrator's applicability review, not a public accusation.

| CVE | Published | NVD description | Scope precision | Defensive interpretation |
|---|---|---|---|---|
| CVE-2021-24111 | 2021-02-25 | .NET Framework denial of service, CVSS 3.1 7.5, network reachable without privileges or interaction [24] | NVD configuration explicitly includes 4.7.2 [24] | High-value patch-compliance checkpoint |
| CVE-2022-21911 | 2022-01-11 | .NET Framework denial of service [14] | Exact affected release not shown in captured text | Check MSRC applicability against OS and installed KBs |
| CVE-2022-41089 | 2022-12-13 | .NET Framework remote code execution [12] | Exact release not shown | Potentially high impact; no MUJ exposure claim |
| CVE-2023-36899 | 2023-08-08 | ASP.NET elevation of privilege [15] | ASP.NET family only in captured description | Inventory ASP.NET component and patch applicability |
| CVE-2023-36049 | 2023-11-14 | .NET, .NET Framework, and Visual Studio elevation of privilege [8] | Framework family; exact release not shown | Relevant to host hardening and post-compromise risk |
| CVE-2023-36560 | 2023-11-14 | ASP.NET security-feature bypass [19] | ASP.NET family; exact release not shown | Review only through owner-side component inventory |
| CVE-2024-21409 | 2024-04-09 | .NET, .NET Framework, and Visual Studio remote code execution; CWE-416 use-after-free [22] | Exact Framework version not shown | High-impact family advisory requiring applicability review |
| CVE-2024-38081 | 2024-07-09 | .NET, .NET Framework, and Visual Studio elevation of privilege [16] | Exact version not shown | Primarily a host and post-compromise concern until scope is confirmed |
| CVE-2025-21176 | 2025-01-14 | .NET, .NET Framework, and Visual Studio remote code execution [7] | Exact version not shown in captured NVD configuration | Confirm against MSRC and installed cumulative update |
| CVE-2025-55248 | 2025-10-14 | Inadequate encryption strength permits an authorized network attacker to disclose information [10] | Names .NET and .NET Framework broadly | Identity alone may not eliminate an authorized-attacker case |
| CVE-2026-50646 | 2026-07-14 | Protection-mechanism failure permits unauthorized local code execution in Framework [28] | Framework family | Post-compromise defense-in-depth issue, not a direct anonymous-web claim |
| CVE-2026-50650 | 2026-07-14 | Code injection permits unauthorized local privilege elevation in Framework [31] | Framework family | Requires local threat modeling and patch review |
| CVE-2026-62872 | 2026-08-11 | Incorrect authorization permits an authorized attacker to elevate privileges over a network [30] | Framework family | Particularly relevant to authenticated multi-user services if applicable |
| CVE-2026-62897 | 2026-08-11 | Integer overflow permits unauthorized local code execution [26] | Framework family | Local/post-compromise exposure, not necessarily edge-reachable |
| CVE-2026-65810 | 2026-08-11 | Relative path traversal permits unauthorized local privilege elevation [27] | Framework family | Local hardening and cumulative servicing issue |

This timeline does not mean 15 exploitable flaws exist on MUJ SLCM. It means a 2026 assessment cannot stop at a 4.7.2 lineage label. The same family continued receiving fixes through the month of this assessment, while the captured NVD records often omit the exact Framework release and fixed KB. Applicability therefore depends on MSRC's product matrix, parent Windows version, installed rollups, architecture, and enabled component.

A useful negative finding emerged during curation: CVE-2024-29187 was excluded because its NVD record concerns the WiX installer toolset and fixes in WiX 3.14.1 and 4.0.5, not the Framework runtime [23]. This illustrates why keyword-only CVE aggregation overstates exposure.

## What A Truly Unpatched 4.x Runtime Would Mean In 2026

"Unpatched" should mean an owner-verified absence of applicable cumulative security updates, not merely observation of `4.7.4136.0`. If that absence is confirmed, the operational concern is substantial because Microsoft characterizes Framework updates as cumulative security and reliability improvements [1]. Missing recent servicing can leave multiple vulnerability classes unresolved at once.

| Risk dimension | Relevant evidence | 2026 implication if applicable updates are absent | Important qualifier |
|---|---|---|---|
| Remote code execution | CVE-2018-8421, CVE-2020-1147, CVE-2022-41089, CVE-2024-21409, CVE-2025-21176 [25][20][12][22][7] | Possible compromise of the worker process or host through an affected reachable component | Each CVE has distinct prerequisites; no live applicability was tested |
| Denial of service | CVE-2019-0820, CVE-2020-1108, CVE-2021-24111, CVE-2022-21911 [9][13][24][14] | Application-pool or service disruption may affect portal availability | Edge filtering may reduce some inputs but does not prove safety |
| Information disclosure | CVE-2019-0545 and CVE-2025-55248 [18][10] | Security boundaries or protected information may be exposed under affected conditions | Authentication and exact cryptographic use matter |
| Security/authorization bypass | CVE-2023-36560 and CVE-2026-62872 [19][30] | Authenticated users may cross an intended security boundary if the affected path exists | A Microsoft 365 sign-in front end does not itself establish Framework authorization behavior |
| Local privilege and execution | 2026 local Framework CVEs [28][31][26][27] | A lesser foothold may become a stronger host compromise | These are not automatically anonymous Internet attacks |
| Unsupported parent platform | Framework 4.5.2+ follows the parent Windows lifecycle [2] | Even a nominally active Framework line can become operationally unsafe on an unsupported OS | MUJ's exact origin OS and lifecycle state are unknown |
| Application-local dependency lag | ASP.NET external components can ship separately [2] | OS servicing may leave vulnerable MVC or other NuGet assemblies untouched | Requires software-composition analysis of the deployed application |

[Inference] The highest defensible risk statement is conditional: **if** the owner confirms missing applicable security rollups on an Internet-facing authenticated portal, remediation priority should be high. The evidence does not support claiming a current breach, an exploitable endpoint, or a specific unpatched CVE.

The reverse is also important. Because the same `System.Web.dll` version appears in package inventories through July 2026 [34], a fully serviced Windows Server 2016 installation may still expose that file version. Calling every such host "eight years unpatched" would create a false positive and undermine responsible disclosure.

## MUJ SLCM Case Study: Edge, Identity, IIS, Runtime, And Application

The requester-supplied architecture contains at least five security layers: Akamai at the edge, IIS 10 as the web server, ASP.NET and Framework at runtime, MVC and other application libraries, and Microsoft 365 identity. The public evidence independently confirms only a MUJ portal with sign-in and parent-login choices [32]. The following analysis is therefore explicitly architectural inference.

**Case study, decision and mechanism.** [Inference] Suppose Akamai blocks a known malicious request pattern before it reaches IIS. That can reduce exploitability for that pattern, but it does not alter `System.Web.dll`, the Framework registry release, or Windows servicing state. It also cannot directly resolve local-only weaknesses such as CVE-2026-50646, CVE-2026-50650, CVE-2026-62897, or CVE-2026-65810, all of which NVD describes as local Framework issues [28][31][26][27]. The decision implication is to retain edge controls while treating them as defense in depth, not as a patch substitute.

**Case study, identity boundary.** [Inference] Microsoft 365 identity can determine who authenticates, while the portal still decides what an authenticated account may do. CVE-2026-62872 is described as incorrect authorization allowing an authorized attacker to elevate privileges over a network [30]. That record does not prove MUJ is affected, but it demonstrates the mechanism by which a strong identity provider and a vulnerable downstream authorization component can coexist. The decision implication is to validate runtime and application authorization independently of sign-in strength.

**Case study, dependency split.** Microsoft explicitly notes that ASP.NET ships external components separately from Framework [2]. [Inference] Consequently, installing current Windows and Framework rollups may not update an application-local MVC, OWIN, JSON serializer, or identity middleware DLL. Conversely, updating an MVC package does not establish that the underlying Framework and OS are current. The decision implication is to maintain two linked inventories: platform servicing and application software composition.

| Layer | Supplied or observed status | What it can contribute | What it cannot prove |
|---|---|---|---|
| Akamai | Supplied by requester | [Inference] Request filtering, rate control, and edge isolation | Origin Framework patch state |
| IIS 10 | Supplied by requester | [Inference] Web-server controls, TLS termination options, request pipeline | Framework cumulative-update status |
| .NET Framework/System.Web | Branch evidenced by `4.7.4136.0` metadata [34] | Managed web runtime and ASP.NET platform | Unique KB or current vulnerability status |
| ASP.NET MVC 5.3 | Supplied by requester | Application routing and MVC behavior | OS/runtime servicing or package currency |
| Microsoft 365 identity | Supplied by requester | [Inference] Authentication and account policy | Correct downstream authorization or safe app logic |
| MUJ application | Public sign-in page observed [32] | Business workflows | Internal data flows, roles, code paths, or security controls |

The case-study result is not that the architecture is insecure. It is that no single layer can answer the patch question for all the others.

## Authorized Validation And Remediation Plan

The security club should not attempt to settle the uncertainty from outside the system. The following workflow is for MUJ's authorized administrators or an assessor operating under written scope.

| Priority | Owner-authorized action | Evidence to record | Decision criterion |
|---:|---|---|---|
| 1 | Read the local Framework `Release` REG_DWORD | Value at `HKLM\SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full` | Compare with Microsoft minimums: 461808, 528040, or 533320 [4] |
| 2 | Record Windows edition, version, build, architecture, and support state | Configuration-management export | Framework 4.5.2+ follows the parent OS lifecycle [2] |
| 3 | Export installed quality and security updates | Update history, servicing-stack state, pending reboot, latest successful cumulative KB | Match against the applicable Microsoft servicing baseline, not a web banner |
| 4 | Inventory Framework binaries as corroboration | Signed file paths, versions, hashes, and package ownership | Use file metadata to investigate inconsistency, never as the sole release test [33] |
| 5 | Inventory application-local assemblies | MVC, OWIN/Katana, identity libraries, serializers, database providers, and other deployed packages | Handle separately because ASP.NET has externally shipped components [2] |
| 6 | Map relevant CVEs through MSRC applicability | Exact OS, Framework release, KB supersedence, architecture, and enabled feature | Mark each CVE applicable, not applicable, superseded, or unresolved |
| 7 | Patch in a staging environment | Regression results for sign-in, parent access, sessions, uploads, reports, and integrations | Deploy current supported cumulative servicing after successful testing |
| 8 | Upgrade where supported | Compatibility test for Framework 4.8 or 4.8.1 | Microsoft identifies 4.8.1 as latest, but parent-OS compatibility must govern [2] |
| 9 | Review version disclosure | Response-header and error-page configuration under authorized testing | Reduce unnecessary disclosure only after fixing servicing; hiding a banner is not patching |
| 10 | Preserve edge and identity defenses | Akamai and identity-policy configuration review | Treat as layered controls, not evidence that runtime fixes are unnecessary |

A sound evidence package should contain the registry value, OS build, latest cumulative update, pending-reboot state, relevant signed-binary metadata, application dependency manifest, and a dated CVE applicability worksheet. This creates a repeatable result that can be audited after every maintenance cycle.

Do not attempt to obtain those artifacts through unauthorized access. Do not deliberately trigger verbose errors, search for an origin that bypasses Akamai, alter forwarding headers, enumerate accounts, test parent/student role boundaries, or reproduce any CVE against the public service without written permission. A university club can still add value by producing the public-source map, maintaining the CVE worksheet, and offering the owner a safe checklist.

## Synthesis: Branch Confidence Is High, Patch Confidence Is Unknown

Three distinctions resolve the apparent contradiction in the evidence.

First, **file identity is not product servicing state**. `4.7.4136.0` identifies a `System.Web.dll` file in the `NET472REL1LAST_B` branch [34]. Microsoft separately defines `AssemblyFileVersion` as file metadata that the Framework does not use for referencing [33], and defines the registry `Release` value as the installed Framework product indicator [4]. The mechanism is separate versioning domains; the implication is that passive fingerprints are necessarily incomplete.

Second, **product release is not cumulative patch freshness**. Framework 4.7.2 is an active release line under Microsoft's Windows-component policy [2]. Microsoft also says Framework updates are cumulative and should be applied regularly [1]. The mechanism is in-place, OS-linked servicing; the implication is that the same release lineage can represent materially different security states.

Third, **perimeter and identity controls are not component remediation**. [Inference] Akamai can affect which requests arrive, Microsoft 365 identity can affect who signs in, IIS can enforce web-server policy, Framework provides runtime services, and MVC plus application libraries implement business behavior. The scope and trade-off of each layer differ. Local 2026 Framework CVEs show why edge controls cannot cover every threat [28][31][26][27], while CVE-2026-62872 shows why an authorized network user can remain relevant after authentication [30].

| Dimension | Passive banner approach | Owner-side servicing audit | Layered security review |
|---|---|---|---|
| Mechanism | Maps visible metadata to a binary lineage | Reads authoritative local state and installed updates | Tests how edge, identity, server, runtime, and application controls combine |
| Scope | Narrow and non-invasive | Exact host patch and lifecycle state | End-to-end attack paths and compensating controls |
| Strength | Fast, safe, useful for triage | Best evidence for patch compliance | Best evidence for residual risk |
| Weakness | Cannot prove a unique KB or CVE | Requires authorization and administrative access | Can become complex and must remain tightly scoped |
| Time horizon | Snapshot of exposed metadata | Repeatable each patch cycle | Continuous architecture and application assurance |
| Recommended role | Generate a question | Answer the patch question | Answer the broader security question |

The non-obvious conclusion is that an apparently old-looking version can exist on a recently serviced platform, while an apparently supported product can still be unsafe if cumulative updates are missing. Both false-positive and false-negative errors are possible unless the registry, OS, KB, and dependency evidence are combined.

## VERDICT

**Verdict:** `ASP.NET runtime 4.7.4136.0` is best identified as the `System.Web.dll` file version from the **.NET Framework 4.7.2 servicing branch `NET472REL1LAST_B`** [34]. It does **not** correspond to one uniquely identifiable security rollup, KB, or installation date. The same file metadata appears across Windows build 14393 packages from October 2025 through July 2026 [34].

**Patch-status verdict:** **Indeterminate from public evidence.** Neither "unpatched" nor "fully patched" is justified by the banner. The decisive evidence is the local `Release` REG_DWORD, parent Windows lifecycle/build, installed cumulative updates, and application-local package inventory [4][2].

**Conditional risk verdict:** **High remediation priority if missing applicable cumulative updates is confirmed.** The Framework/ASP.NET history includes critical remote code execution, denial of service, information disclosure, authorization bypass, and local privilege-escalation classes [25][24][12][22][30]. This is a conditional risk determination, not a claim that MUJ is currently exploitable.

**Confidence:**

| Conclusion | Confidence | Basis |
|---|---|---|
| 4.7.4136.0 maps to `System.Web.dll` and `NET472REL1LAST_B` | High | Exact-version public binary metadata [34] |
| Branch corresponds to Framework 4.7.2 servicing lineage | High | Branch label plus Microsoft's 4.7.2 release taxonomy [34][2] |
| No unique KB/date can be inferred | High | Same version and hashes occur across numerous later packages [34] |
| MUJ is unpatched | Low/unsupported | Required owner-side registry and KB evidence is absent |
| MUJ is affected by any particular CVE | Low/unknown | Applicability, installed updates, and reachable code paths are unverified |
| A confirmed unpatched 4.x portal warrants urgent remediation | High | Cumulative servicing policy and documented high-impact vulnerability classes [1][25][12][22] |

## References

1. *.NET Framework release information - .NET Framework | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/framework/release-notes/release-notes
2. *.NET Framework official support policy | .NET*. https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-framework
3. *.NET Framework system requirements - .NET Framework | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/framework/get-started/system-requirements
4. *Determine which .NET Framework versions are installed - .NET Framework | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/framework/install/how-to-determine-which-versions-are-installed
5. *.NET Framework & Windows OS versions - .NET Framework | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/framework/install/versions-and-dependencies
6. *.net Framework CVEs and Security Vulnerabilities - OpenCVE*. https://app.opencve.io/cve?product=.net_framework&vendor=microsoft
7. *NVD - CVE-2025-21176*. https://nvd.nist.gov/vuln/detail/CVE-2025-21176
8. *NVD - CVE-2023-36049*. https://nvd.nist.gov/vuln/detail/CVE-2023-36049
9. *NVD - CVE-2019-0820*. https://nvd.nist.gov/vuln/detail/CVE-2019-0820
10. *NVD - CVE-2025-55248*. https://nvd.nist.gov/vuln/detail/CVE-2025-55248
11. *NVD - CVE-2019-1301*. https://nvd.nist.gov/vuln/detail/CVE-2019-1301
12. *NVD - CVE-2022-41089*. https://nvd.nist.gov/vuln/detail/CVE-2022-41089
13. *NVD - CVE-2020-1108*. https://nvd.nist.gov/vuln/detail/CVE-2020-1108
14. *NVD - CVE-2022-21911*. https://nvd.nist.gov/vuln/detail/CVE-2022-21911
15. *NVD - CVE-2023-36899*. https://nvd.nist.gov/vuln/detail/CVE-2023-36899
16. *NVD - CVE-2024-38081*. https://nvd.nist.gov/vuln/detail/CVE-2024-38081
17. *NVD - CVE-2017-8759*. https://nvd.nist.gov/vuln/detail/CVE-2017-8759
18. *NVD - CVE-2019-0545*. https://nvd.nist.gov/vuln/detail/CVE-2019-0545
19. *NVD - CVE-2023-36560*. https://nvd.nist.gov/vuln/detail/CVE-2023-36560
20. *NVD - CVE-2020-1147*. https://nvd.nist.gov/vuln/detail/CVE-2020-1147
21. *NVD - CVE-2021-26413*. https://nvd.nist.gov/vuln/detail/CVE-2021-26413
22. *NVD - CVE-2024-21409*. https://nvd.nist.gov/vuln/detail/CVE-2024-21409
23. *NVD - CVE-2024-29187*. https://nvd.nist.gov/vuln/detail/CVE-2024-29187
24. *NVD - CVE-2021-24111*. https://nvd.nist.gov/vuln/detail/CVE-2021-24111
25. *NVD - CVE-2018-8421*. https://nvd.nist.gov/vuln/detail/CVE-2018-8421
26. *NVD - CVE-2026-62897*. https://nvd.nist.gov/vuln/detail/CVE-2026-62897
27. *NVD - CVE-2026-65810*. https://nvd.nist.gov/vuln/detail/CVE-2026-65810
28. *NVD - CVE-2026-50646*. https://nvd.nist.gov/vuln/detail/CVE-2026-50646
29. *NVD - CVE-2026-50649*. https://nvd.nist.gov/vuln/detail/CVE-2026-50649
30. *NVD - CVE-2026-62872*. https://nvd.nist.gov/vuln/detail/CVE-2026-62872
31. *NVD - CVE-2026-50650*. https://nvd.nist.gov/vuln/detail/CVE-2026-50650
32. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
33. *Use AssemblyVersion and AssemblyFileVersion - .NET Framework | Microsoft Learn*. https://learn.microsoft.com/en-us/troubleshoot/developer/dotnet/framework/general/assembly-version-assembly-file-version
34. *winbindex.m417z.com*. https://winbindex.m417z.com/
