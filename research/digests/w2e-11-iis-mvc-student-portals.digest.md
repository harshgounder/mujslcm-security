# Digest: w2e-11-iis-mvc-student-portals

## REPORT
Source file: w2e-11-iis-mvc-student-portals.md (Benchmarking MUJ SLCM Against Indian ASP.NET Portals)

## ANSWER SUMMARY
- Amizone is the strongest MVC-family near peer; LPU UMS, Chandigarh CUIMS, and MAHE SLCM show classic Web Forms markers; Sharda eSharda and Manav Rachna remain stack-unverified functional candidates.
- Identity is MUJ's clearest positive signal: realm discovery marks muj.manipal.edu and jaipur.manipal.edu as managed Microsoft tenants, and the June 2025 MUJ SOP documents mandatory Office 365 MFA.
- MVC 5.3.0 is a real NuGet package (.NET 4.5+, last update Oct 23 2023); the real lifecycle risk is the vague ".NET Framework 4.x" label, since only 4.8.1 remains supported on supported Windows.
- Three incident cases frame the benchmark: Kashmir 2022 alleged data sale, Surya Shakti Infotech admissions ransomware (June 2025), and the JEE Advanced cloud misconfiguration (June 2026); none ties to MUJ SLCM.
- The LPU plaintext-credential claim is uncorroborated first-person reporting with no institutional confirmation or remediation record.
- Eight defensive classes frame the checklist: runtime ambiguity, split identity and weak recovery, authorization, session and CSRF, upload/export, errors and headers, CDN-to-origin trust, logging and disclosure.
- CERT-In 2022 Directions impose six-hour incident reporting for listed incidents and 180-day India-resident log retention; rehearse the clock in a tabletop.
- A 90-day roadmap starts with asset and identity inventory and ends with an authorized assessment; the report authorizes no testing.

## KEY FACTS
1. https://mujslcm.jaipur.manipal.edu/ - target portal with student and parent login paths.
2. https://muj.slcm.jaipur.manipal.edu/ - alternate MUJ front door ("WELCOME TO MUJ PORTAL").
3. https://student.amizone.net/ - Amizone; MVC-family near peer with parent visibility.
4. https://ums.lpu.in/lpuums - LPU legacy UMS; home-grown ERP with Web Forms state markers.
5. https://studentums.lpu.in/login - separate modern LPU login, coexistence case.
6. https://uims.cuchd.in/ - Chandigarh CUIMS student and parent ERP; Web Forms markers, old jQuery filename.
7. https://slcm.manipal.edu/ - MAHE SLCM; Web Forms markers and jQuery 2.0.3 asset path, closest organizational comparator.
8. https://www.nuget.org/packages/Microsoft.AspNet.Mvc - MVC 5.3.0 package facts, .NET 4.5+ target.
9. https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-framework - .NET Framework support policy; 4.8.1 supported, earlier 4.x retired.
10. http://login.microsoftonline.com/getuserrealm.srf?login=probe@muj.manipal.edu&xml=1 - realm discovery result: managed tenant for muj.manipal.edu.
11. http://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf - MUJ SOP; MFA mandatory before Office 365 use.
12. https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf - six-hour reporting, 180-day logs, clock sync duties.
13. https://kashmirobserver.net/2022/08/10/kashmir-university-hacking-data-of-1-million-students-found-on-dark-web/ - Kashmir 2022 alleged sale case, unconfirmed database.
14. https://timesofindia.indiatimes.com/city/kolkata/ransomware-targets-it-firm-handling-college-admissions/articleshow/122119513.cms - admissions-provider ransomware case, June 2025.
15. https://www.rfc-editor.org/rfc/rfc9116.html - security.txt standard for the disclosure route.

## ACTIONABLE LEADS
- Resolve exact .NET and Windows builds, then grade lifecycle support; do not accept ".NET 4.x" as sufficient.
- Confirm MFA coverage for every SLCM role including parent and any local fallback paths.
- Build a role-object authorization matrix with staging denial tests for cross-user and cross-role access.
- Audit session cookies, CSRF coverage on every state-changing form, uploads, exports, and bulk downloads.
- Verify Akamai-to-origin TLS, origin ACL, trusted client-IP headers, and cache behavior with the infra owner.
- Publish and monitor /.well-known/security.txt with valid Contact and Expires.
- Run a tabletop covering account takeover, record exposure, vendor ransomware, and Akamai-origin anomaly inside the six-hour window.

## FLAGS
- MUJ stack remains brief-supplied; MVC-family signals are passive observations, not vulnerability findings.
- Realm probe uses a constructed probe@muj.manipal.edu address; result supports a managed-tenant claim only.
- Kashmir figures (1M+ records, $250) come from one news report; the university never confirmed legitimacy.
- Surya Shakti facts partly rest on "reportedly" and "believed" wording.
- LPU plaintext claim is uncorroborated; keep as a claim, not a finding.
- IIT Roorkee denied mass extraction on the record; report preserves the denial.
- The stated confidence "Moderate-high, 0.78" is a presented number with no derivation shown; treat as presentation.

## COVERAGE
- Chars read: 42,854
- EOF confirmed: yes (truncated: false on final page, 238 of 238 lines)