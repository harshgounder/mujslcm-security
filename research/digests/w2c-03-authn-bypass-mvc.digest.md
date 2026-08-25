# Digest: w2c-03-authn-bypass-mvc.md

## REPORT
Source file: w2c-03-authn-bypass-mvc.md. Authorization and authentication-bypass risk analysis for the MUJ SLCM ecosystem. Framework-reasoning report built from Microsoft and OWASP documentation plus public MUJ pages. Treats all MUJ-specific bypass scenarios as INFERENCE, not findings.

## ANSWER SUMMARY
- Verdict: no publicly substantiated MUJ SLCM authentication bypass identified. Confidence High that public evidence is insufficient to claim a vulnerability; Low to Very Low that any individual pattern is exploitable on MUJ.
- Tech stack (ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Azure AS8075, M365 identity) is a user-supplied premise; the research run did not independently establish versions or AS8075 origin.
- Public login form exposes UserName, Password, hidden __RequestVerificationToken, EmailFor, LoginFor, plus a Forgot Password link to passwordreset.microsoftonline.com; page distinguishes Student and Parent login choices.
- MUJ FAQ confirms SLCM registration URL, name.registration-number username pattern, official Outlook-ID password, and university helpline. Office 365 SOP directs users to Microsoft login with phone, email, and Authenticator security methods.
- Microsoft realm response for probe@muj.manipal.edu returns Microsoft Online federation fields; evidence of M365 identity dependency only, not proof of where final authorization happens.
- Core framework facts: [Authorize] restricts action or controller with [AllowAnonymous] exceptions, conventional MVC route is {controller}/{action}/{id}, Web API uses api/{controller}/{id}, IIS Request Filtering can govern sequences, extensions, hidden segments, verbs, double escaping, and high-bit characters before MVC runs.
- Eight requested bypass patterns (route-parameter tricks, trailing slash, trailing dot/space, backslash, Unicode normalization, case gap, extensionless conflict, static-handler shadow, direct action without [Authorize]) map to /Home/, /Student/, /Staff/, /api/ route guesses, each with a safe verification invariant.
- Recommended next decision: obtain written authorization and source/config access, then build a machine-readable inventory of every MVC action, Web API action, anonymous exception, static handler, and effective policy. No operational payloads appear in the report by design.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/ - the login surface; form field names and Student/Parent choices define the visible trust boundary.
- http://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - FAQ confirming registration URL, name.registration-number username pattern, Outlook-ID password, helpline.
- http://login.microsoftonline.com/getuserrealm.srf?login=probe@muj.manipal.edu&xml=1 - realm probe showing Microsoft Online federation fields for the domain.
- http://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf - Office 365 SOP: Microsoft login service and MFA/security-info methods.
- https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html - deny-by-default, application-wide access control, per-request validation; basis for P0 remediation priorities.
- http://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References - IDOR definition driving the /Student/ ownership analysis.
- https://learn.microsoft.com/en-us/previous-versions/aspnet/dd460317%28v%3Dvs.118%29 - AuthorizeAttribute scope: controller-level, action-level, inheritance, AllowAnonymous.
- https://learn.microsoft.com/en-us/aspnet/mvc/overview/older-versions-1/controllers-and-routing/asp-net-mvc-routing-overview-cs - conventional route with defaults; basis for trailing-separator and extensionless analysis.
- https://learn.microsoft.com/en-us/aspnet/web-api/overview/web-api-routing-and-actions/routing-in-aspnet-web-api - Web API route model; justifies a separate API endpoint inventory.
- https://learn.microsoft.com/en-us/iis/configuration/system.webserver/security/requestfiltering - IIS Request Filtering layers; high-bit character setting documented default true.
- https://learn.microsoft.com/en-us/iis/manage/configuring-security/configure-request-filtering-in-iis - substatus codes 404.5, 404.6, 404.7, 404.8, 404.11, 404.12, 404.14, 404.15 for denial telemetry.
- https://learn.microsoft.com/en-us/dotnet/standard/base-types/best-practices-strings - ordinal comparison recommended for access-control filtering.
- http://learn.microsoft.com/en-us/dotnet/api/system.string.normalize?view=netframework-4.8.1 - Unicode normalization forms C, D, KC, KD.
- https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file - Windows path semantics: backslash separator, terminal space/period warnings.
- https://learn.microsoft.com/en-us/iis/configuration/system.webserver/security/requestfiltering/denyurlsequences - denyUrlSequences configuration for rejected URL sequences.

## ACTIONABLE LEADS
- Request from application owner: effective web.config, URL Rewrite rules, request-filtering configuration, route registrations, reverse-proxy rules; then compute effective policy per action including inheritance and anonymous behavior.
- Follow the 8-phase authorized validation plan: architecture inventory, effective-policy analysis, canonicalization specification, generated route tests, object-authorization tests with synthetic principals and disjoint fixtures, static/dynamic parity review, logging with IIS substatus, CI regression gate that fails unclassified actions.
- Test equivalence classes (trailing slash, trailing dot/space, backslash, Unicode forms, case variants, extensionless routes) only in local or staging environments; capture endpoint, handler, policy, principal, and status before redirect rewriting.
- Keep MVC and Web API inventories separate and make them consume the same service-layer authorization so policy parity is testable.
- Validate M365 claims (issuer, audience, freshness, intended user type) before any local role or object authorization; document the identity-to-role handoff.
- Disclosure trigger: report findings only if source review shows path-prefix authorization, unclassified actions, API filter gaps, or protected files under public roots.

## FLAGS
- Every MUJ-specific mapping (/Home/, /Student/, /Staff/, /api/) is an INFERENCE; the report repeats this label and never claims an observed vulnerability. Do not cite any route family as confirmed.
- Stack premise (MVC 5.3, .NET 4.x, IIS 10, AS8075) is unverified by this report; headers and login-page appearance do not establish application versions.
- References 17-20 cite ASP.NET Core and Kestrel host-filtering docs inside a classic MVC report; refs 18 and 19 are the same Kestrel page in English and Arabic variants, a weak fit and a possible source-list artifact.
- No source code, route table, filter registration, rewrite rules, handler map, or test results were available; framework capability facts do not show MUJ enabled or misconfigured anything.
- Text contains zero operational bypass payloads by design; the report explicitly forbids testing malformed variants against production.

## COVERAGE
- File: w2c-03-authn-bypass-mvc.md.
- 263 lines total; 49,031 bytes on disk; 49,029 chars read.
- Method: read_file offset 1, limit 2000, single call.
- EOF confirmed: final call returned truncated: false, last content line 263 equals total_lines 263.