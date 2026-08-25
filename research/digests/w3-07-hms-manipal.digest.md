# Digest: w3-07-hms-manipal.md

## REPORT
Source file: w3-07-hms-manipal.md (280 lines, 33,341 bytes)
Report title: HMS Manipal OSINT Report: Identity, Exposure, and MUJ Separation

## ANSWER SUMMARY
- HMS means Hostel Management System. hms-admin.manipal.edu explicitly expands HMS and describes room and seat booking by block, capacity, and availability.
- Scope is MAHE: landing page lists Manipal, Health Science, Mangalore, and Bangalore hostel contacts. No Jaipur or MUJ references.
- hms.manipal.edu resolves to 20.44.49.205, AS8075 Microsoft Corporation; Shodan snapshot reports Microsoft Azure Application Gateway v2, last seen 23 August 2026.
- Edge masks the origin: header snapshot shows gateway affinity cookies and no Server, X-AspNet-Version, X-AspNetMvc-Version, or X-Powered-By values.
- SecurityHeaders snapshot dated 25 August 2026: grade A for hms; X-Frame-Options, HSTS, CSP, X-Content-Type-Options, X-XSS-Protection, X-Download-Options present; Referrer-Policy and Permissions-Policy missing.
- IIS 10.0, MVC 5.3, ASP.NET 4.0.30319 fingerprint is evidenced for MUJ SLCM only, not for HMS.
- Akamai is not substantiated for hms.manipal.edu; no DNS alias, header, certificate, or passive record located.
- No hostname-specific incident: Open Bug Bounty record is manipal.edu.np XSS, Brinztech is the library portal, LeakRadar is a domain-level aggregator.

## KEY FACTS
1. https://hms.manipal.edu/ : hostel landing page, "Your Home Away From Home", campus contacts.
2. https://hms-admin.manipal.edu/ : explicit HOSTEL MANAGEMENT SYSTEM label and booking description.
3. https://hms.manipal.edu/Login.aspx : login labels: learner email, mobile OTP, employee auth, guest, application and roll numbers.
4. https://dns.google/resolve?name=hms.manipal.edu&type=A : A record 20.44.49.205, TTL 3600.
5. https://ipinfo.io/20.44.49.205/json : AS8075 Microsoft, Chennai geolocation.
6. https://www.shodan.io/host/20.44.49.205 : Azure Application Gateway v2 product snapshot.
7. http://securityheaders.com/?followRedirects=on&q=https://hms.manipal.edu/ : grade A snapshot, two headers missing.
8. http://api.hackertarget.com/httpheaders?q=https://mujslcm.jaipur.manipal.edu/ : MUJ stack fingerprint (IIS 10, MVC 5.3, ASP.NET 4.0.30319).
9. http://web.archive.org/cdx/search/cdx?collapse=urlkey&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&output=json&url=hms.manipal.edu/* : historical paths including Authorization.aspx, Atom_PayResponse.aspx, HDFCResponse.aspx.
10. https://login.microsoftonline.com/muj.manipal.edu/.well-known/openid-configuration : tenant ID 27282fdd-4c0b-4dfb-ba91-228cd83fdf71; no HMS client evidence.
11. https://jaipur.manipal.edu/hostel-facility.php : MUJ hostels, first-come-first-served allotment, SpaceBasic maintenance link.
12. https://jaipur.manipal.edu/hostel-fees.php : 2026-27 double occupancy fees, room booking portal, pay-fee-online destination.
13. https://www.openbugbounty.org/reports/2160625/ : manipal.edu.np XSS, patched; not HMS.
14. https://www.brinztech.com/breach-alerts/brinztech-alert-database-of-manipal-library-portal-leaked/ : library portal claim, not HMS.
15. https://hostel.manipal.edu/indexICAS.aspx : legacy indexed "Hostel Management System" login with CAPTCHA.

## ACTIONABLE LEADS
- Passive recheck of the login page over time to see if a login.microsoftonline.com redirect or client ID ever appears; none observed so far.
- Verify the payment surface: archive paths Atom_PayResponse.aspx and HDFCResponse.aspx exist; current provider unknown.
- Compare header behavior across hms root, Home.aspx, and Login.aspx under authorized review; gateway may add affinity cookie markers.
- Treat hms.manipal.edu, hms-admin.manipal.edu, and legacy hostel.manipal.edu/indexICAS.aspx as three surfaces of one service.
- Confirm whether the MUJ room-booking portal (fee page) is the same service; MUJ pages do not name hms.
- Treat missing Referrer-Policy and Permissions-Policy as hardening signals only; grade A snapshot is not a security verdict.

## FLAGS
- Citation markers like [295.38] and [288.0-8] appear to be extract line ranges; the mapping cannot be verified from the report text alone.
- Shodan and SecurityHeaders are third-party snapshots, time-bound to August 2026.
- CSP in the hms snapshot permits unsafe-inline and unsafe-eval for scripts; noted as observation, not a finding.
- PTR and CNAME queries returned nothing: bounded negative results.
- RMS page statement "RMS uses Outlook credentials" must not be reused as HMS evidence.
- MUJ fee figures (Rs 167,372, Rs 15,378, Rs 25,475) are for 2026-27 and apply to MUJ hostels, not HMS.

## COVERAGE
- Chars read: 33,341; lines 280; truncated false; EOF confirmed.