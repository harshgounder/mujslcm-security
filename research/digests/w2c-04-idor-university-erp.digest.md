## REPORT (w2c-04-idor-university-erp.md)
Defensive IDOR and BOLA assurance map for an SLCM-class university portal. No public evidence of a MUJ IDOR; no vulnerability finding. Six synthetic test families proposed. 287 lines, 43462 chars, read to EOF, truncated: false.

## ANSWER SUMMARY
- Verdict: IDOR and BOLA is a high-priority defensive assurance area for the described portal class, but public evidence does not prove MUJ uses sequential IDs or has an authorization flaw. The report must not be presented as a penetration-test result.
- Authorization, not identifier shape, is the decision: every endpoint accepting an object reference needs a per-object check. GUIDs are defense in depth, never proof of authority. A sequential ID with a scoped query can be safe.
- Parameterized queries do not solve IDOR (CWE-639 invoice example stays vulnerable without an ownership check). Query safety and authorization safety are separate properties.
- Six object families matter: marks, fee receipts, notifications, documents, timetable, profile. Each has a different subject-object relationship; one generic "logged-in user" rule is insufficient.
- India-linked writeups are mechanism case studies only: the numeric userid increment case (author is a Jamal Mohamed College student, target institution unnamed) and the anonymized financial-records case. Neither establishes proof against MUJ or a named Indian university.
- Microsoft 365 identity authenticates the subject; it does not know local record ownership, parent delegation, course assignment, or finance scope. Authorization must be enforced by the application.
- Validation is safe only with synthetic data: seed records, cross-object negative substitution, no enumeration of live identifiers.
- Regression gates: response confidentiality, state integrity, operation isolation, relationship expiry, property control, alternate representation, error consistency, cache isolation, auditability, CI enforcement.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/Home/Index - public page with separate sign-in and parent-login options, the only verified MUJ fact.
- https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html - per-object access checks, dataset-scoped lookups, avoid identifiers in URLs and POST bodies.
- https://cwe.mitre.org/data/definitions/639.html - user-controlled key selects a record without verifying entitlement; horizontal and vertical escalation.
- https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization - API1 requirement for object-level checks on every object action.
- https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization - API3 property-level authorization, used for the profile-field control.
- https://medium.com/@itcsafsar/idor-vulnerability-exposing-sensitive-student-information-responsible-disclosure-b49694354c6e - numeric userid increment case study for document and record exposure.
- https://in.linkedin.com/in/itcsafsar - author page establishing the Jamal Mohamed College affiliation for attribution limits.
- https://medium.com/@vickyrohith70/how-i-found-an-idor-vulnerability-a-responsible-disclosure-story-def2885bbe0c - anonymized financial-records portal case, no institution or fix status.
- https://hackerone.com/indian_institute_of_techn - IIT response-policy page; proves a disclosure channel exists, not any IDOR case.
- https://www.nuget.org/packages/Microsoft.AspNet.Mvc/5.3.0 - package existence verified; deployment on MUJ not verified.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.mvc.authorizeattribute?view=aspnet-mvc-5.2 - AuthorizeAttribute is a coarse user or role gate; it does not promise record ownership.
- https://learn.microsoft.com/en-us/aspnet/core/security/authorization/resource-based?view=aspnetcore-10.0 - resource-based authorization principle; page documents ASP.NET Core, not MVC 5, so APIs must not be copied.
- http://learn.microsoft.com/en-us/entra/identity-platform/authentication-vs-authorization - authentication versus authorization distinction.
- https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References - two-user and privilege-level testing method.
- https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html - log authorization failures with correlation references, not record contents.

## ACTIONABLE LEADS
- Build AUTHZ-MARK-01 through AUTHZ-PROFILE-01 with synthetic Students A and B, parent A, assigned and unassigned faculty, finance operator, registrar. Substitute only pre-seeded non-owned references; never guess IDs.
- Test operation isolation: read permission must not grant export, update, approve, publish, or delete. Test property-level control on profile fields and mark fields.
- Check file delivery paths: direct storage URLs, pre-signed retrieval links, preview versus download authorization, and cache privacy for personalized responses.
- Test 403 versus 404 consistency to avoid an existence oracle.
- Encode one positive and one negative test per policy row in CI as a release-blocking gate.
- Inventory where object references appear: path, query, form field, JSON body, hidden field, filename, workflow state.

## FLAGS
- Case study 1: target institution unnamed, no independently corroborated remediation; author affiliation is the only India link. Do not cite as a proven Indian university case.
- Case study 2: institution, country, identifier format, and fix status all absent from the cited material.
- Case study 3: IIT HackerOne page establishes policy existence only; no published IDOR case was established.
- MVC 5.3, IIS 10, Akamai, and Microsoft 365 deployment claims are user-supplied; only the NuGet package existence is verified.
- Role matrix and CDN cache claims are explicitly labeled Inference; they are a recommended baseline, not MUJ policy.
- Report intentionally contains no MUJ route names or live identifiers, so all actionable leads are hypothetical object families pending authorization.

## COVERAGE
- File read to EOF: 287 lines, 43462 chars (file_size 43462), truncated: false. Confirmed EOF at line 287, final reference.