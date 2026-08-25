# Digest: w2f-02-dotnet-patch-level

## REPORT
Source file: w2f-02-dotnet-patch-level.md (MUJ SLCM .NET 4.7.4136.0 Security Assessment)

## ANSWER SUMMARY
- 4.7.4136.0 maps with high confidence to the System.Web.dll file version from branch NET472REL1LAST_B, a .NET Framework 4.7.2 servicing lineage. It is not a unique KB, patch date, or install date.
- The same file version and hashes appear in Windows Server 2016 build 14393 packages from October 2025 through July 2026. A serviced host can still expose this value, so "eight years unpatched" claims are false positives.
- Authoritative installed-version check is local: HKLM\SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full Release DWORD. Minimums: 461808 (4.7.2), 528040 (4.8), 533320 (4.8.1).
- Framework 4.5.2+ is a Windows component that follows the parent OS lifecycle; 4.8.1 is the latest release. An active-support label does not prove updates were deployed.
- Serious history includes CVE-2018-8421 (CVSS 9.8 RCE, NVD names 4.7.2) and CVE-2021-24111 (network DoS, 4.7.2 in NVD config). 2026 NVD records add local code execution, code injection, relative path traversal, and network-based privilege elevation.
- Verdict: patch state indeterminate from public evidence. Conditional high remediation priority only if the owner confirms missing applicable cumulative updates.
- CVE-2024-29187 was excluded because it concerns the WiX installer toolset, not the Framework; keyword-only CVE aggregation overstates exposure.
- ASP.NET ships external components separately from the Framework; MVC, OWIN/Katana, JSON, and identity packages need a separate composition inventory.

## KEY FACTS
- https://winbindex.m417z.com/ - third-party binary index mapping 4.7.4136.0 to NET472REL1LAST_B and to build 14393 packages through July 2026.
- https://learn.microsoft.com/en-us/dotnet/framework/install/how-to-determine-which-versions-are-installed - Release DWORD method and documented minimum values.
- https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-framework - 4.5.2+ follows parent Windows lifecycle; 4.8.1 latest; ASP.NET external components note.
- https://learn.microsoft.com/en-us/dotnet/framework/release-notes/release-notes - Framework updates are cumulative security and reliability improvements.
- https://nvd.nist.gov/vuln/detail/CVE-2018-8421 - CVSS 9.8 RCE; NVD explicitly names Framework 4.7.2.
- https://nvd.nist.gov/vuln/detail/CVE-2021-24111 - network-reachable DoS CVSS 7.5; NVD configuration explicitly includes 4.7.2.
- https://nvd.nist.gov/vuln/detail/CVE-2026-62872 - incorrect authorization lets an authorized attacker elevate privileges over a network.
- https://nvd.nist.gov/vuln/detail/CVE-2026-50646 - protection-mechanism failure permits unauthorized local code execution.
- https://nvd.nist.gov/vuln/detail/CVE-2026-65810 - relative path traversal permits local privilege elevation.
- https://nvd.nist.gov/vuln/detail/CVE-2024-21409 - RCE family advisory with CWE-416 use-after-free; exact version not shown in captured text.
- https://nvd.nist.gov/vuln/detail/CVE-2024-29187 - WiX toolset CVE, excluded; example of keyword-only aggregation error.
- https://nvd.nist.gov/vuln/detail/CVE-2025-21176 - January 2025 RCE in .NET, .NET Framework, and Visual Studio family.
- https://mujslcm.jaipur.manipal.edu/ - the only independently verified host fact: public portal with sign-in and parent-login choices.
- https://learn.microsoft.com/en-us/troubleshoot/developer/dotnet/framework/general/assembly-version-assembly-file-version - AssemblyVersion versus AssemblyFileVersion distinction; file metadata is not used for referencing.
- https://nvd.nist.gov/vuln/detail/CVE-2020-1147 - XML source markup RCE across .NET Framework, SharePoint, and Visual Studio.

## ACTIONABLE LEADS
- Owner-side evidence: Release DWORD, Windows edition/build/support state, installed KB list with pending reboot, signed binary metadata as corroboration only, and an application-local assembly inventory.
- Map every candidate CVE through the MSRC applicability matrix (exact OS, Framework release, KB supersedence, architecture, enabled feature) into a dated worksheet.
- Patch in staging first: sign-in, parent access, sessions, uploads, reports, integrations. Upgrade to 4.8 or 4.8.1 only where the parent OS supports it.
- Review version disclosure (headers, error pages) only after servicing; hiding a banner is not patching.
- Club-safe work: public source map, CVE applicability worksheet, owner checklist. No error induction, origin hunting, header manipulation, account enumeration, or role-boundary tests.

## FLAGS
- The repeated-file result contradicts any unique-KB inference; the report explicitly warns against calling all 4.7-era hosts unpatched.
- Most 2021-2026 CVE rows lack exact affected Framework releases in captured NVD text; they are family-level records, applicability unresolved.
- 2026-dated NVD CVEs (CVE-2026-50646, CVE-2026-62872, CVE-2026-65810) are future-dated claims from the source; unverified, treat as record citations only.
- winbindex is third-party; Microsoft publishes no such mapping. Confirm against owner inventory before any claim.
- Verdict split: high confidence on branch mapping, low/unsupported on MUJ being unpatched or affected; do not cite as exposure proof.

## COVERAGE
Chars read: 35,282 (file size), 271 lines. EOF confirmed: true (truncated false).

DONE w2f-02-dotnet-patch-level.digest.md