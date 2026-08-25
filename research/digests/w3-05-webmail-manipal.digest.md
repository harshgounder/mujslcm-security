# Digest: w3-05-webmail-manipal.md

## REPORT
Source file: /home/liebert511/mujslcm-recon/research/w3-05-webmail-manipal.md (AI deep-research output, claims UNVERIFIED). Topic: evidence-based assessment of `webmail.manipal.edu`. Public DNS, routing, archives, official MUJ documents, vendor docs; no credential testing.

## ANSWER SUMMARY
- Network identity: `webmail.manipal.edu` resolves to `218.248.47.16` (TTL 14,400); RIPEstat shows the host block `218.248.47.0/26` with netname MAHE, while the covering route `218.248.32.0/20` is AS9829 BSNL-NIB; the /26 itself is not directly announced in the cited result.
- Parent-domain mail is Microsoft 365: MX `manipal-edu.mail.protection.outlook.com`, autodiscover CNAME to `autodiscover.outlook.com`, DKIM selectors into `learnermanipal.onmicrosoft.com`, corroborated by ViewDNS.
- Historical identity is Exchange/OWA: 2006 capture names Exchange Server 2003 OWA with `Domain\user name` fields, 2012 OWA Light (CookieAuth), 2015 and 2016 Outlook Web App.
- The 2022 archive replay at `/userportal/webpages/myaccount/login.jsp` contains "Sophos" and locale strings, and the current indexed page is titled "VPN Portal" with a JavaScript fallback message; current live markup was not extractable.
- Credential acceptance is not established for any source; the parent MX and M365 DNS do not prove the webmail host redirects to or shares Microsoft identity.
- The MUJ O365 SOP makes MFA mandatory and documents Microsoft Authenticator, phone, and email verification; the SLCM FAQ ties the SLCM password to the Outlook ID but never names the webmail host as a backend.
- Verdict: High confidence for historical OWA/Exchange lineage and parent-domain Microsoft 365, Medium for a later Sophos-style portal inference, Low for current legacy OWA status, none for credential acceptance.

## KEY FACTS
- https://dns.google/resolve?name=webmail.manipal.edu&type=A - A record 218.248.47.16, TTL 14400.
- https://stat.ripe.net/data/whois/data.json?resource=218.248.47.16 - 218.248.47.0/26 netname MAHE, ASSIGNED NON-PORTABLE, country IN.
- https://stat.ripe.net/data/prefix-overview/data.json?resource=218.248.47.0/24 - aligned to 218.248.32.0/20 announced by AS9829; queried /24 not itself announced.
- https://stat.ripe.net/data/as-overview/data.json?resource=AS9829 - holder BSNL-NIB National Internet Backbone.
- https://dns.google/resolve?name=manipal.edu&type=MX - MX preference 0 to manipal-edu.mail.protection.outlook.com.
- https://dns.google/resolve?name=autodiscover.manipal.edu&type=CNAME - autodiscover.outlook.com.
- https://dns.google/resolve?name=selector1._domainkey.manipal.edu&type=CNAME - DKIM delegation into learnermanipal.onmicrosoft.com.
- https://urlscan.io/domain/webmail.manipal.edu/ - IP 218.248.47.16, AS9829/BSNL-NIB, GeoIP Bhubaneswar, not observed on urlscan.
- https://web.archive.org/web/20060903020056id_/https://webmail.manipal.edu/exchweb/bin/auth/owalogon.asp?url=https%3A%2F%2Fwebmail.manipal.edu%2FExchange%26reason=0 - 2006 OWA explicitly on Exchange Server 2003.
- https://web.archive.org/web/20120113021334id_/https://webmail.manipal.edu/CookieAuth.dll?GetLogon?curl=Z2Fexchange%26reason=0%26formdir=1 - 2012 Exchange OWA Light capture.
- https://web.archive.org/web/20150605035251id_/https://webmail.manipal.edu/owa/auth/logon.aspx - 2015 Outlook Web App login path.
- https://web.archive.org/web/20220303013019/https://webmail.manipal.edu/userportal/webpages/myaccount/login.jsp - 2022 replay with Sophos text and locale list.
- https://webmail.manipal.edu/ - current indexed page titled "VPN Portal" with JavaScript-required message.
- https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf - official MUJ SOP: Microsoft 365 sign-in, mandatory MFA, recovery options.
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - SLCM FAQ: username pattern, password as per official Outlook ID; no webmail-host link.

## ACTIONABLE LEADS
- Ask MAHE IT whether the hostname is retired, redirected, or required; obtain a purpose statement and service generation record.
- Owner-side check that legacy OWA paths (/exchweb, /owa, /CookieAuth.dll) are disabled or access-controlled.
- Confirm whether a Sophos user/VPN portal is current, which identity provider it uses, and its port/posture (Sophos default port 4443 is vendor documentation, not host evidence).
- Verify Microsoft 365 is the only sanctioned mail authentication path and that MFA enforcement covers it.
- Track the 218.248.47.0/26 announcement question internally; report routing ownership separately from address assignment.
- Do not test credentials in any form; the report explicitly forbids it and states account-lock and incident-alert risks.

## FLAGS
- The /26 block is not directly announced in the cited RIPEstat response; claiming direct /26 announcement would overstate the data.
- "Not observed on urlscan.io" is a coverage statement, not a negative security finding.
- Archive captures are historical, not live-state evidence; 2015/2016 login fields do not prove current reachability or authentication.
- Sophos attribution is an inference from one 2022 replay plus current indexed wording; no version, port, live markup, or vendor certificate observed.
- The 2022 cleaned replay lacks a complete login form; that absence is an extraction limitation.
- CertSpotter's empty issuance array is a coverage result, not proof of no certificate.
- The current "VPN Portal" claim rests on indexed text because direct extraction returned no readable markup.
- All claims come from AI research output and are unverified until rechecked against the cited sources.

## COVERAGE
25,275 chars read on disk (wc -m), 146/146 lines, single read pass, final page returned truncated=false, EOF confirmed; file_size 25281 bytes.