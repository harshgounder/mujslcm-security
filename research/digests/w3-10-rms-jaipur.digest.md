# Digest: w3-10-rms-jaipur.md

## REPORT
Source file: w3-10-rms-jaipur.md (219 lines, 31,637 bytes)
Report title: RMS Jaipur: Public Surface, Provenance, and Unknowns

## ANSWER SUMMARY
- RMS on the target page explicitly means Research Data Management System; it links to MUJ IRINS and shows research-performance notices.
- "Result Management System" is not supported by any reviewed evidence and must not be published as fact.
- Login.aspx shows User Name, Password, the @jaipur.manipal.edu suffix, a Chrome note, and a footer crediting MSIS and ISD at MAHE.
- Central RMS (rms.manipal.edu) documents research workflows and support mailboxes and says RMS uses the same login credentials as the Outlook account; that statement is about the central page, not automatically the Jaipur host.
- Network: resolves to 202.131.155.153; BGP and IPinfo agree on AS134039, Ibus Virtual Network Services Private Limited; reverse DNS 202.131.155.153.convergentindia.com; IPinfo geolocates to Delhi.
- Legacy ASP.NET Web Forms-style indicators: Login.aspx, WebResource.axd, aspnetForm; MVC 5.3, .NET 4.x, IIS 10, Akamai remain unverified for RMS.
- Archive: root captured 2024-03-22 (February 2024 notice), Error.aspx captured 2024-08-28, WebResource.axd and assets from August 2024.
- No RMS-specific public complaint found in the searched indexes; bounded negative.

## KEY FACTS
1. https://rms.jaipur.manipal.edu/ : target root, Research Data Management System title, IRINS link, notices.
2. https://rms.jaipur.manipal.edu/Login.aspx : login fields, suffix, footer, Chrome note.
3. https://rms.manipal.edu/ : central RMS, support mailboxes, Outlook credential statement.
4. https://muj.irins.org/ : MUJ research profile portal with nodal officer and faculty login links.
5. https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf : SLCM registration URL, username pattern, AMS contacts.
6. https://mujslcm.jaipur.manipal.edu/Home/Index : SLCM portal surface for comparison.
7. https://bgp.he.net/ip/202.131.155.153 : AS134039, 202.131.155.0/24, Ibus, convergentindia reverse DNS.
8. https://ipinfo.io/202.131.155.153 : AS134039, Ibus, Delhi classification.
9. http://dns.google/resolve?name=rms.jaipur.manipal.edu&type=A : A record 202.131.155.153.
10. http://web.archive.org/cdx/search/cdx?collapse=urlkey&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&output=json&url=rms.jaipur.manipal.edu/* : root, Error.aspx, WebResource.axd records.
11. https://web.archive.org/web/20240322052206/https://rms.jaipur.manipal.edu/ : archived homepage with February 2024 DBT-Chemical Engineering notice.
12. https://web.archive.org/web/20240828150521/https://rms.jaipur.manipal.edu/Error.aspx : archived generic error page.
13. https://www.jaipur.manipal.edu/online-grevience-registration.php : grievance channels, named officials.
14. http://jaipur.manipal.edu/recognition-accrediation.php : MUJ established by Act No. 21 of 2011, UGC Act section 22.
15. https://rms.manipal.edu/PublicationEntry/Reports/Login.aspx : publication route with generic error wording.

## ACTIONABLE LEADS
- Passive route inventory from archive: Error.aspx, WebResource.axd, Styles/Style.css, image assets; watch the current route tree via indexing only.
- Watch the login flow passively for any login.microsoftonline.com redirect, given the central RMS Outlook credential statement.
- Cross-check whether the Jaipur RMS and central RMS share branding and mailboxes; ownership of the Jaipur tenant is unconfirmed.
- Confirm CDN and proxy placement against SLCM in an internal inventory; no public evidence exists.
- Later archive checks can show notice continuity; the current page shows April and May 2025 notices.
- Use the grievance page contacts only as institutional escalation, not as RMS-specific evidence.

## FLAGS
- "Result Management System" hypothesis: unsupported, report warns against publishing it.
- Outlook credential wording comes from rms.manipal.edu, not the Jaipur host; protocol unknown for both.
- Ibus is network attribution only; "Ibus Jaipur ISP" is shorthand, physical location not proven.
- IPinfo Delhi geolocation is database output, not proof of server location.
- Web Forms-style assessment is mid-high confidence on family, not version.
- BGP view "hosted-domain count 0" is tool output; not evidence about virtual hosts.
- Error.aspx archive shows only that the route existed; no current behavior can be inferred.

## COVERAGE
- Chars read: 31,637; lines 219; truncated false; EOF confirmed.