# Digest: w3-09-mujerp.md

## REPORT
Source file: w3-09-mujerp.md (194 lines, 29,860 bytes)
Report title: What MUJ's ERP Host Reveals About SLCM Boundaries

## ANSWER SUMMARY
- http://mujerp.jaipur.manipal.edu/MUJWEB/ self-identifies as "Welcome to Dynamics 365 Business Central" with a User name and Password form posting to /MUJWEB/SignIn.
- Product reading: Business Central is ERP per Microsoft documentation; the host is a Business Central web front end, not proof of SLCM linkage.
- SLCM is a separate service: one-stop academic-information portal per the first-year guide, with student and parent entry points.
- MUJ IT page names ERP, student life-cycle web portal, LMS, and research management as separate landscape items; adjacency, not integration.
- DNS-over-HTTPS returns an A record of 20.244.0.229 for mujerp, TTL 3600; region and ownership unverified.
- Business Central supports many credential modes (Windows, NavUserPassword, AccessControlService via Entra); a username and password form does not reveal identity architecture.
- Staff use is plausible from public finance and IT pages, but no public source names a staff member using mujerp.
- Supplied claims: ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, Azure Central India, CT since April 2025: none independently confirmed.

## KEY FACTS
1. https://mujerp.jaipur.manipal.edu/MUJWEB/ : Business Central title, ms-nav layout, /MUJWEB/SignIn form action.
2. https://mujslcm.jaipur.manipal.edu/Home/Index : SLCM portal with parent login.
3. https://mujslcm.jaipur.manipal.edu/ : SLCM markup with Keen theme assets and @muj.manipal.edu write-in.
4. https://www.microsoft.com/en-us/dynamics-365/products/business-central : Microsoft describes Business Central as ERP software.
5. https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/administration/users-credential-types : credential types incl AccessControlService backed by Entra ID.
6. https://dns.google/resolve?name=mujerp.jaipur.manipal.edu&type=A : A record 20.244.0.229, TTL 3600.
7. http://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf : SLCM onboarding workflow, non-editable admission fields, parent OTP.
8. http://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf : SLCM URL, username pattern, Outlook ID password guidance.
9. https://www.jaipur.manipal.edu/administration-it.php : IT landscape wording places ERP and student lifecycle side by side.
10. https://jaipur.manipal.edu/administration-finance.php : fee collections, payroll, accounting, audits; does not name mujerp.
11. https://mujone.jaipur.manipal.edu/HR/ : separate MUJ HR SYSTEM surface with employee fields.
12. https://www.microsoft.com/en-us/download/details.aspx?id=56519 : Azure IP ranges file; general, cannot prove Central India for one address.
13. http://web.archive.org/cdx/search/cdx?collapse=urlkey&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&output=json&url=mujslcm.jaipur.manipal.edu/* : archived SLCM HTML and Keen theme assets.
14. https://www.manipal.edu/mu/policies/it-policy/information-security-policy.html : related MUJ policy context cited by the report.

## ACTIONABLE LEADS
- Passive re-fetch of /MUJWEB/ at intervals; any redirect to login.microsoftonline.com would change the identity assessment.
- Query CNAME and HTTPS records for mujerp to test for CDN or gateway layers.
- Re-run CT log queries for mujerp.jaipur.manipal.edu; the report got no usable result.
- Match the exact Azure IP ranges file to 20.244.0.229 before any region claim.
- Request from the owner: tenant, credential mode, MFA status, module list, user population.
- Verify whether the SignIn form enforces double-submit only client-side; do not test server behavior without authorization.

## FLAGS
- Report wording: product label proves product family, not modules, tenant, or users.
- MVC 5.3, .NET 4.x, IIS 10, Akamai, Central India, CT date: all supplied and unverified.
- CT search failure for the exact hostname is a bounded negative.
- Staff-use and finance-system claims are inference from public role and finance pages.
- The first-year guide and FAQ describe SLCM, not Business Central usage.

## COVERAGE
- Chars read: 29,860; lines 194; truncated false; EOF confirmed.