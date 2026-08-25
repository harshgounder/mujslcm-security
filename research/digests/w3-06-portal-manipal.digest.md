# Digest: w3-06-portal-manipal.md

## REPORT
Source file: w3-06-portal-manipal.md (280 lines, 46,620 bytes)
Report title: MUJ SLCM and Portal Public OSINT Assessment

## ANSWER SUMMARY
- MUJ SLCM is an academic student and parent system. Official ICT inventory names it as replacement for the older Academic Management System, covering attendance, internal marks, external marks, result publication, and broadcast messages. High confidence.
- portal.manipal.edu currently exposes an EPF application with user, resigned-employee, and admin login routes; footer credits MAHE Information Systems. It is a separate employee or administrative surface, not SLCM.
- Two separate public endpoints: SLCM resolves to 98.70.14.50, portal to 45.112.150.155 (TTL 300). Portal address is announced by AS134039, label Ibus Virtual Network Services Private Limited.
- Third-party header scan of SLCM shows IIS 10.0, ASP.NET MVC 5.3, ASP.NET 4.0.30319, grade D; X-Frame-Options present, HSTS, CSP, X-Content-Type-Options, Referrer-Policy, Permissions-Policy missing.
- Portal root returned HTTP 403 in its scan but still discloses IIS 10.0 and ASP.NET; grade F. The error response limits the value of that fingerprint.
- Wayback shows the portal root served a generic IIS Windows Server landing page on 18 April 2022; no archive proof of when EPF was deployed.
- Akamai is unconfirmed: portal CNAME and HTTPS DNS queries returned no answer, no Akamai label in the header report. Absence is not proof of no CDN.
- Microsoft SSO is unconfirmed: OpenID metadata proves a jaipur.manipal.edu tenant exists, not that SLCM federates.

## KEY FACTS
1. https://mujslcm.jaipur.manipal.edu/ : primary target; MUJ Portal sign-in and parent login surface.
2. http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf : official ICT inventory; SLCM function and module list.
3. https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=A : SLCM A record, 98.70.14.50.
4. http://securityheaders.com/?followRedirects=on&q=https://mujslcm.jaipur.manipal.edu/ : IIS 10, MVC 5.3, ASP.NET 4.0.30319 fingerprint, grade D.
5. https://portal.manipal.edu/epf/userlogin.aspx : EPF user login with email and password form, MAHE ISD footer.
6. https://portal.manipal.edu/epf/rtlogin.aspx : resigned-employee login route with employee-ID label.
7. https://portal.manipal.edu/epf/admlogin.aspx : admin login route with @manipal.edu email cue.
8. https://dns.google/resolve?name=portal.manipal.edu&type=A : portal A record, 45.112.150.155, TTL 300.
9. https://bgp.he.net/ip/45.112.150.155 : AS134039 announces 45.112.150.0/24, Ibus label.
10. https://urlscan.io/domain/portal.manipal.edu : passive metadata; AS134039, Udupi GeoIP, first observed 4 January 2019.
11. https://web.archive.org/cdx/search/cdx?url=portal.manipal.edu&output=json&filter=statuscode:200&fl=timestamp,original,statuscode,digest&collapse=digest : root 200 captures on 18 April 2022.
12. https://web.archive.org/web/20220418001040/https://portal.manipal.edu/ : archived generic IIS Windows Server landing page.
13. https://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf : SLCM credentials sent to personal Gmail during admission.
14. https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf : SLCM password described as per official Outlook ID; AMS support contacts.
15. http://login.microsoftonline.com/jaipur.manipal.edu/.well-known/openid-configuration : Microsoft tenant metadata exists; SLCM integration not stated.

## ACTIONABLE LEADS
- Enumerate EPF child routes passively: /epf, /epf/Home.aspx, userlogin, rtlogin, admlogin are search-indexed; review indexing policy, not credentials.
- Compare header sets across portal / and /epf routes in an authorized review; root 403 vs reachable child routes suggests per-path policy.
- Re-query DNS A, CNAME, HTTPS records for both hosts at later dates to track edge or CDN changes.
- Check /.well-known/security.txt on mujslcm: retrieved response looked like portal content, not an RFC 9116 record with a Contact field.
- Map the identity chain from written docs only: Gmail delivery, Outlook-ID password wording, Office 365 MFA mandate; do not assert SSO.
- Use listed governance contacts (MUJ contact page, SLCM FAQ AMS and IT Infra, MAHE student portal) for ownership confirmation.
- Record related surfaces: sis.manipal.edu, hms.manipal.edu/login.aspx, libportal.manipal.edu, apply.manipal.edu, mufc.manipal.edu.

## FLAGS
- Akamai claim from the brief: unconfirmed by this report.
- Microsoft 365 SSO claim: unconfirmed; tenant metadata is not integration proof.
- security.txt response is not a structured record; do not claim absence of a reporting process.
- Time-bound observations: SecurityHeaders scans dated 25 August 2026 (12:27 UTC portal, 12:34 UTC MUJ).
- Prefix discrepancy between sources: BGP.HE reports 45.112.150.0/24, urlscan reports route 45.112.148.0/22; both list AS134039.
- urlscan shows zero direct or incoming hits for the domain; report treats the counters as telemetry limits, not proof of disuse.
- References 11 and 12 (crt.sh, Wappalyzer) appear in the reference list but are not used as evidence in the body.

## COVERAGE
- Chars read: 46,620; lines 280; truncated false; EOF confirmed.