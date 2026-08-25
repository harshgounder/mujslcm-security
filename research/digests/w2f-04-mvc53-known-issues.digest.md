# Digest: w2f-04-mvc53-known-issues

## REPORT
Source file: w2f-04-mvc53-known-issues.md (MVC 5.3 Risk Map for MUJ SLCM)

## ANSWER SUMMARY
- MVC 5.3.0 is a real release: NuGet published on 2023-10-23, Web Stack v3.3.0 on 2023-10-24. Microsoft lists MVC 5.x as supported under its external ASP.NET tool policy with no end date. Not EOL, but legacy System.Web.
- WebGrease is NOT a direct MVC 5.3 dependency. It enters through the separate Microsoft.AspNet.Web.Optimization 1.1.3 package (deprecated, no longer maintained), which requires WebGrease >=1.5.2.
- The only confirmed historical MVC advisory, MS14-059 / CVE-2014-4075 (input-encoding XSS), enumerates affected releases through MVC 5.1. MVC 5.3 is not in the bulletin.
- CVE-2018-8171 is a package-level advisory (CVSS 7.5, login-attempt validation) whose consulted record gives no affected range or fixed version. Applicability to 5.3 is unresolved, not assumed.
- The "unsafe reflection" issue #428 is an open, version-unspecified Veracode CWE-470 report on System.Net.Http.Formatting.dll, unconfirmed by maintainers. It is not a UrlHelper advisory.
- Core JsonResult defaults to DenyGet; no core JsonpResult was found. Any JSONP behavior on MUJ is custom or third-party until its assembly is identified.
- Antiforgery community issues (#48, #157, #162, #328) are closed operational failures (IIS classic pipeline, load-balanced token decryption, MachineKey coupling, Google Web Light), not CVEs.
- Verdict: no public evidence proves an MVC 5.3 flaw on MUJ. Evidence justifies an owner-authorized review of deployment inventory, legacy optimization chain, build imports, redirects, JSON behavior, antiforgery topology, sessions, and controller authorization.

## KEY FACTS
- https://www.nuget.org/packages/Microsoft.AspNet.Mvc/5.3.0 - package record; direct deps Razor >=3.3.0 and WebPages >=3.3.0; no WebGrease in the direct list.
- https://dotnet.microsoft.com/en-us/platform/support/policy/aspnet - MVC 5.x supported, classified as a Tool, no end date.
- https://learn.microsoft.com/en-us/security-updates/SecurityBulletins/2014/ms14-059 - MS14-059; affected MVC 2.0 through 5.1, so 5.3 is not enumerated.
- https://www.nuget.org/packages/Microsoft.AspNet.Web.Optimization/1.1.3 - legacy, no longer maintained; requires WebGrease >=1.5.2.
- https://www.nuget.org/packages/WebGrease/1.6.0 - last updated 2014-01-23; floors on Antlr 3.4.1.9004 and Newtonsoft.Json 5.0.4 (declared minimums, not deployed versions).
- https://advisories.gitlab.com/pkg/nuget/microsoft.aspnet.mvc/ - CVE-2018-8171 CVSS 7.5 advisory; no version range in the consulted record.
- https://api.github.com/repos/aspnet/AspNetWebStack/issues/428 - open Veracode reflection finding on System.Net.Http.Formatting.dll; label Needs: Author Feedback; no maintainer confirmation.
- https://github.com/aspnet/AspNetWebStack/blob/main/src/System.Web.Mvc/UrlHelper.cs - ObjectToDictionary route-value conversion; no request-controlled class instantiation shown.
- https://github.com/aspnet/AspNetWebStack/blob/main/src/System.Web.Mvc/JsonResult.cs - DenyGet default; JavaScriptSerializer for non-null data.
- https://learn.microsoft.com/en-us/aspnet/mvc/overview/security/preventing-open-redirection-attacks - open-redirect pattern and IsLocalUrl mitigation.
- https://api.github.com/repos/aspnet/AspNetWebStack/issues/162 - classic pipeline PlatformNotSupportedException after 5.2.3 to 5.2.6 upgrade.
- https://api.github.com/repos/aspnet/AspNetWebStack/issues/328 - token decryption failure across two Windows Server 2019 IIS nodes behind a load balancer; root cause unresolved.
- https://api.github.com/repos/aspnet/AspNetWebStack/issues/157 - antiforgery serializer used MachineKey only; no OWIN data-protector integration point.
- https://api.github.com/repos/aspnet/AspNetWebStack/issues/48 - Google Web Light removed the token field; intermediary transformation failure case.
- https://learn.microsoft.com/en-us/nuget/consume-packages/package-references-in-project-files - PackageReference asset controls (IncludeAssets, ExcludeAssets, PrivateAssets) and packages.lock.json locked restore.

## ACTIONABLE LEADS
- Export the resolved package graph (project files, packages.config, project.assets.json, lock files, DLL hashes); confirm whether Web Optimization is installed and used; plan retirement of the legacy optimization branch.
- Review imported .props and .targets, constrain NuGet sources, lock restores in CI, and generate an SBOM.
- Static review targets: returnUrl handling with IsLocalUrl, JsonResult AllowGet opt-ins, JSONP callbacks, antiforgery coverage on every state-changing route, object-level authorization on student and parent records.
- Test CSRF across the real topology: multi-node farm consistency, proxy/CDN behavior, cookie flags, identity transitions. A 500 on token omission means enforcement, not bypass.
- Track issue #428 and reproduce only in an isolated test project using the exact deployed binary.
- Release gates: version provenance, build provenance, redirects, JSON exposure, CSRF, authorization, session policy, authentication errors, monitoring.

## FLAGS
- CVE-2018-8171 has no affected range in the consulted advisory; a package-name match alone must not be called a 5.3 vulnerability.
- Issue #428 is a reporter-submitted scanner finding without maintainer confirmation; high hallucination risk if cited as a confirmed flaw.
- Many references are raw API endpoints (api.github.com, api.nuget.org); valid evidence but not human-readable pages.
- MVC 5.3, .NET 4.x, IIS 10, Akamai, and Microsoft 365 are user-supplied premises; host-specific conclusions are conditional.
- Open-issue searches returned zero results; bounded negative results, not proof of no defects.
- MS14-059 is historical provenance only; citing it as current MUJ exposure would be an error the report explicitly warns against.

## COVERAGE
Chars read: 50,421 (report text extracted from JSON-persisted tool output), 388 lines. EOF confirmed: true (truncated false).

DONE w2f-04-mvc53-known-issues.digest.md