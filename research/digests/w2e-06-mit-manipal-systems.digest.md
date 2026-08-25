# Digest: w2e-06-mit-manipal-systems.md

## REPORT
Source file: w2e-06-mit-manipal-systems.md (MIT Manipal Signals for Defending MUJ SLCM)

## ANSWER SUMMARY
- MIT/MAHE public evidence transfers as workflow test cases, not as confirmed MUJ vulnerabilities; overall confidence rated 0.78, medium-high.
- MAHE ICT report defines SLCM: attendance, internal and external marks, results, circulars, single window for students and parents.
- Front doors differ: sis.manipal.edu, slcm.manipal.edu, and the MUJ portal; reviews must inventory redirects, identity handoffs, and role boundaries.
- Unofficial automation demand is documented: slcmAPI (2020, deprecated after CAPTCHA), SLCM-is-Dumb (2025, digit CAPTCHA automation), SLCM_APP (2025, Flutter/FastAPI with custom credential logic).
- No public Manipal SLCM vulnerability disclosure was located; that is a bounded OSINT result, not proof of absence.
- "ASP.NET MVC 5.3" is unverified; public NuGet evidence points to Microsoft.AspNet.Mvc 5.2.9, and 4.5.2/4.6/4.6.1 retired in April 2022.
- Office 365 is MAHE-wide; identity lifecycle crosses the Microsoft and SLCM boundary, making recovery and session revocation key controls.
- Priority is control validation (MFA coverage, role isolation, session revocation, origin restriction) in owner-run environments, not exploitation.

## KEY FACTS
1. https://mujslcm.jaipur.manipal.edu/ - target portal with student and parent entry choices.
2. https://slcm.manipal.edu/ - MAHE-branded SLCM endpoint, family relevance.
3. https://sis.manipal.edu/ - SIS limited to bona fide MAHE members.
4. http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf - ICT report: SLCM functions plus O365, Teams, Brightspace, Impartus, Moodle, EduNxt.
5. https://github.com/sankalp2004/SLCM-is-Dumb - 2025 CGPA scraper advertising digit-CAPTCHA automation.
6. http://github.com/canaryGrapher/slcmAPI - 2020 API, deprecated after CAPTCHA was introduced.
7. http://github.com/DK10WS/SLCM_APP - 2025 MUJ mobile app with custom email/password logic and no stated credential-storage rule.
8. https://github.com/nikeplusdash/SLCM-api - API for slcm.manipal.edu that advises session logout.
9. https://mujstella.in/ - independent student platform with an explicit non-affiliation disclaimer.
10. https://www.manipal.edu/mit.html - MIT official presence inside the MAHE domain.
11. https://www.nuget.org/packages/Microsoft.AspNet.Mvc/5.2.9 - public MVC package evidence that contradicts the "5.3" label.
12. https://learn.microsoft.com/en-us/entra/identity/conditional-access/policy-block-legacy-authentication - legacy auth linked to 97%+ of credential stuffing and 99%+ of password spraying; Report-only staging guidance.
13. https://techdocs.akamai.com/origin-ip-acl/docs/welcome - Origin IP ACL guidance for restricting direct-origin traffic.
14. https://libportal.manipal.edu/ - library portal maintained by Digital and Information Technology.
15. https://admin.mit659.examly.io/login - publicly indexed MIT-branded Examly admin login; ownership and current use unverified.

## ACTIONABLE LEADS
- Produce an exact SBOM for OS, IIS, .NET Framework, MVC packages, jQuery, and authentication middleware.
- Run Conditional Access changes in Report-only mode first; keep emergency accounts outside blocking policies.
- Test student/parent authorization boundaries with synthetic accounts in an approved environment.
- Verify anti-forgery coverage on every state-changing route and session renewal, logout, and revocation behavior.
- Restrict origin acceptance to Akamai paths and monitor for direct-origin traffic.
- Decide between a sanctioned read-only API and an explicit no-integration policy; warn students against giving passwords to third-party tools.
- Keep CAPTCHA but layer rate, risk, session, and anomaly controls on top.

## FLAGS
- Repository maintainers' MIT Manipal student status is unverified (report assigns 0.15 confidence).
- MVC 5.2.9 versus 5.3 discrepancy; IIS 10 and Akamai are requester-supplied premises.
- Repository claims are self-descriptions; nothing was executed or verified.
- No attributable Manipal vulnerability disclosure exists; do not claim one.
- MUJStella is independent and not affiliated with MUJ.
- Examly admin login ownership is medium-low confidence; do not treat as an official MIT system without confirmation.

## COVERAGE
Chars read: 36693. EOF confirmed: yes (truncation flag false on full read).