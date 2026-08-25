# webmail.manipal.edu: Evidence-Based Mail-System Assessment

## Executive summary

- **Network identity**: Public DNS maps `webmail.manipal.edu` to **218.248.47.16** with a TTL of **14,400 seconds**. [8] RIPEstat places the address in `218.248.47.0/26`, whose `netname` is **MAHE** and whose description names Manipal Academy of Higher Education. [13] The covering route data identifies the less-specific `218.248.32.0/20` as announced by AS9829, but explicitly warns that the queried `/24` was not itself announced in that result. [22] AS9829 is identified as **BSNL-NIB - National Internet Backbone**, and its WHOIS description identifies Bharat Sanchar Nigam Limited. [20] [23] This supports the supplied NIB-space characterization, while separating address assignment from routing ownership.
- **Current mail platform for the parent domain**: `manipal.edu` currently publishes one MX target, `manipal-edu.mail.protection.outlook.com`, a Microsoft Exchange Online-style protection endpoint. [4] A third-party DNS report independently shows the same MX target and the Azure DNS nameserver set. [25] `autodiscover.manipal.edu` points to `autodiscover.outlook.com`. [7] DKIM selectors point into `learnermanipal.onmicrosoft.com`. [5] [6] Together, these are strong evidence that the parent-domain mail service uses Microsoft 365/Exchange Online, not proof that the legacy webmail host is still an Exchange server.
- **Historical host identity**: Exact-host Internet Archive captures show a documented migration or succession of mail-facing technologies. A 2006 page is explicitly titled "Microsoft Outlook Web Access" and says it was provided by **Microsoft Exchange Server 2003**. [15] The same page exposes `Domain\user name` and `Password` fields. [15] A 2012 capture is titled "Microsoft Exchange - Outlook Web Access," says "Connected to Microsoft Exchange," and displays an OWA Light interface. [17] [17] Captures from 2015 and 2016 are titled "Outlook Web App" and show username and password fields. [11] [14]
- **Current publicly indexed surface**: The current indexed response is titled **"VPN Portal"** and reports "Your browser does not support JavaScript or it is disabled!" followed by "Without JavaScript support user portal will not work." [10] Direct extraction of the current root and user-portal paths returned no readable page or raw markup. That means the present login surface cannot be safely described as a visible OWA page from the available public evidence.
- **Sophos assessment**: A 2022 exact-host archive replay at `/userportal/webpages/myaccount/login.jsp` contains the text `Sophos` and a set of portal locales. [21] Sophos documentation says its user portal is accessed through a Sophos device FQDN or IP and that port 4443 is the default. [12] **Inference**: the 2022 endpoint and the current indexed wording are consistent with a Sophos user/VPN portal, but the evidence does not establish the current live Sophos version, port, configuration, identity provider, or relationship to the current Microsoft 365 tenant.
- **Credential question**: The public record does **not** establish that `webmail.manipal.edu` currently accepts Microsoft 365 credentials, legacy Exchange credentials, VPN credentials, or any credentials at all. The archived pages prove that historical login forms existed; they do not prove that those forms remained reachable or that authentication succeeded. Credential testing would be unauthorized without explicit owner permission and is outside this assessment.
- **MUJ documentation**: The official MUJ Office 365 SOP identifies Office 365/Microsoft 365, directs users to `https://login.microsoftonline.com/`, requires MFA, and documents Microsoft Authenticator, phone, and email verification options. [1] [1] [1] [1] [1] The official SLCM FAQ gives the SLCM registration link, a `name.registration number` username pattern, and says the password is "as per official outlook ID." [24] It does not identify `webmail.manipal.edu` as the SLCM login backend.
- **Bottom line**: Confidence is **high** that the host has a genuine MAHE-assigned address and a historical Exchange/OWA lineage, and **high** that the parent `manipal.edu` mail domain uses Microsoft 365. Confidence is **medium** that the later/current web-facing surface is or was a Sophos user/VPN portal. Confidence is **low** that the host is currently a legacy OWA/Exchange box or that it still accepts credentials, because no passive source proves either proposition.

## Scope, safety, and method

This assessment uses publicly accessible DNS responses, public routing and registry data, official MUJ documents, official Microsoft and Sophos documentation, search-indexed page text, and Internet Archive captures. It does not use account credentials, password spraying, brute force, form submission, exploit attempts, intrusive scanning, or access to private material. The correct research question is therefore not "can a login be forced or tested?" but "what can public evidence establish without crossing an authorization boundary?"

The report uses three evidence labels. **Verified** means the cited source directly states or returns the fact. **Inference** means the relationship is technically plausible but not directly established by the source. **Unknown** means the available public evidence does not answer the question. This distinction is especially important because a hostname, a parent-domain MX record, a historical archive, and a current login surface can all refer to different service generations.

Private chain-of-thought is not reproduced. Instead, the following auditable reasoning summary records the decision path: identify the host and address; resolve parent-domain mail routing; inspect exact-host archives; compare historical product labels; inspect official institutional documentation; compare current indexed wording with vendor documentation; and stop when the remaining questions would require authentication or active probing.

## Exact evidence table: network and DNS

| Evidence item | Public result | Interpretation | Status | Exact URL |
|---|---|---|---|---|
| Host A record | `webmail.manipal.edu` -> `218.248.47.16`; TTL `14400`; DNS status `0`; response not truncated | Confirms the supplied hostname-to-address mapping at the cited observation time | Verified | https://dns.google/resolve?name=webmail.manipal.edu&type=A |
| Host CNAME query | No CNAME answer is returned in the cited response; an authority section for `manipal.edu` is shown | The host is not shown as a CNAME in this response; it does not identify the application | Verified | https://dns.google/resolve?name=webmail.manipal.edu&type=CNAME |
| MAHE address allocation | `218.248.47.0/26`; `netname: MAHE`; description names Manipal Academy of Higher Education; country `IN`; status `ASSIGNED NON-PORTABLE` | Supports institutional address assignment | Verified | https://stat.ripe.net/data/whois/data.json?resource=218.248.47.16 |
| Covering route | RIPEstat aligns the query to `218.248.32.0/20`, announced by AS9829, and warns the queried resource was not announced as supplied | Supports the route/NIB association but prevents claiming a directly observed `/26` route | Verified | https://stat.ripe.net/data/prefix-overview/data.json?resource=218.248.47.0/24 |
| AS holder | Holder `BSNL-NIB - National Internet Backbone`; announced `true` | Identifies the covering AS | Verified | https://stat.ripe.net/data/as-overview/data.json?resource=AS9829 |
| AS WHOIS | `as-name: BSNL-NIB`; description names National Internet Backbone and Bharat Sanchar Nigam Limited; country `IN` | Corroborates NIB/BSNL identity | Verified | https://stat.ripe.net/data/whois/data.json?resource=AS9829 |
| Independent host observation | URLScan lists IP `218.248.47.16`, AS9829/BSNL-NIB, GeoIP Bhubaneswar, and "Not observed on urlscan.io" | Corroborates address/AS association; the no-scan statement is not a negative security finding | Verified | https://urlscan.io/domain/webmail.manipal.edu/ |

The table shows why "NIB space" should be reported carefully. The address block is assigned to MAHE, while the covering route is associated with BSNL-NIB. **Inference**: MAHE may be using connectivity or transit provided through BSNL-NIB, but the public records do not by themselves identify the physical server operator, firewall owner, or application owner.

## Exact evidence table: parent-domain mail platform

| Record | Value | What it supports | Exact URL |
|---|---|---|---|
| MX | Preference `0`; `manipal-edu.mail.protection.outlook.com.` | Exchange Online-style inbound mail routing for `manipal.edu` | https://dns.google/resolve?name=manipal.edu&type=MX |
| Autodiscover CNAME | `autodiscover.outlook.com.` | Microsoft-hosted Autodiscover routing | https://dns.google/resolve?name=autodiscover.manipal.edu&type=CNAME |
| DKIM selector 1 | `selector1-manipal-edu._domainkey.learnermanipal.onmicrosoft.com.` | Microsoft 365 tenant-style DKIM delegation | https://dns.google/resolve?name=selector1._domainkey.manipal.edu&type=CNAME |
| DKIM selector 2 | `selector2-manipal-edu._domainkey.learnermanipal.onmicrosoft.com.` | Corroborating Microsoft 365 tenant-style DKIM delegation | https://dns.google/resolve?name=selector2._domainkey.manipal.edu&type=CNAME |
| Third-party MX report | Same `manipal-edu.mail.protection.outlook.com.` target; Azure DNS nameservers | Independent corroboration of the MX observation | http://viewdns.info/dnsreport?domain=manipal.edu |

Microsoft explains that MX records tell other mail systems where to send mail and that Autodiscover helps clients find and configure Exchange; it also identifies MX, Autodiscover, and SPF as primary Microsoft 365 DNS records. [3] **Inference**: the combination above is substantially stronger than an isolated Outlook hyperlink, and supports Microsoft 365/Exchange Online as the parent-domain platform. It still does not prove that `webmail.manipal.edu` is an alias for Outlook on the web.

The official MUJ SOP provides operational corroboration. It calls the system Office 365/Microsoft 365, instructs users to open `https://login.microsoftonline.com/`, and says to enter a University Mail ID. [1] [1] [1] It says MFA is mandatory before Office 365 can be used. [1] The document describes Microsoft Authenticator QR-code enrollment and alternative phone or personal-email verification methods. [1] These instructions are relevant to the MUJ identity ecosystem, but do not state that the old webmail hostname redirects to Microsoft 365.

## Exact evidence table: historical webmail and OWA lineage

| Archive timestamp | Archived path | Visible product wording | Visible login evidence | Exact replay URL |
|---|---|---|---|---|
| 2006-09-03 | `/exchweb/bin/auth/owalogon.asp` | "Microsoft Office Outlook Web Access provided by Microsoft Exchange Server 2003" | `Domain\user name` and `Password` | https://web.archive.org/web/20060903020056id_/https://webmail.manipal.edu/exchweb/bin/auth/owalogon.asp?url=https%3A%2F%2Fwebmail.manipal.edu%2FExchange%26reason=0 |
| 2012-01-13 | `/CookieAuth.dll?GetLogon` | "Microsoft Exchange - Outlook Web Access"; "Connected to Microsoft Exchange"; "Outlook Web Access Light" | `Domain\user name` and `Password` | https://web.archive.org/web/20120113021334id_/https://webmail.manipal.edu/CookieAuth.dll?GetLogon?curl=Z2Fexchange%26reason=0%26formdir=1 |
| 2015-06-05 | `/owa/auth/logon.aspx` | "Outlook Web App" | `User name` and `Password` | https://web.archive.org/web/20150605035251id_/https://webmail.manipal.edu/owa/auth/logon.aspx |
| 2016-06-09 | `/owa/auth/logon.aspx?...` | "Outlook Web App" | `User name`, `Password`, and private/public computer wording | https://web.archive.org/web/20160609223215id_/https://webmail.manipal.edu/owa/auth/logon.aspx?url=https%3A%2F%2Fwebmail.manipal.edu%2Fowa%2F%26reason=0 |
| 2022-03-03 | `/userportal/webpages/myaccount/login.jsp` | "Sophos" and locale list in the cleaned replay | No complete login form in the cleaned evidence | https://web.archive.org/web/20220303013019/https://webmail.manipal.edu/userportal/webpages/myaccount/login.jsp |

The archive index also returns these exact-host records, including the 2004 root, 2014 root, the 2006 Exchange path, the 2012 CookieAuth path, the 2015 and 2016 OWA paths, a 2016 favicon path, and the 2022 user-portal path. [9] The sequence is strong evidence of historical OWA/Exchange exposure. Microsoft's own public wording explains that Outlook on the web was formerly called Outlook Web App or OWA. [18]

However, archive chronology is not live-state evidence. A capture means an archive crawler received content at a particular time; it does not prove the same path was reachable later, that a current listener uses the same software, or that a credential would authenticate. **Inference**: the historical sequence suggests a service transition from on-premises or locally presented Exchange web access toward another perimeter or access-portal function. The transition point and ownership are not publicly established.

## Current login surface and technology assessment

The current search-indexed page is labeled "VPN Portal," and its visible fallback message says the browser lacks JavaScript or that JavaScript is disabled, followed by the statement that the user portal will not work without JavaScript. [10] The current root and the historical-looking `/userportal/webpages/myaccount/login.jsp` path produced no readable extraction and no raw markup in the passive fetch results. This is an important limitation: there is no current public form action, input-name list, HTML title, server header, framework marker, or version string that can be responsibly reported from the available evidence.

The 2022 archive replay is more informative but still incomplete. Its cleaned content contains "Sophos" and a list of supported locales. [21] Official Sophos documentation says that a Sophos user portal can be reached through a Sophos device FQDN or IP and that port 4443 is the default. [12] **Inference**: a Sophos user/VPN portal is the best explanation for the 2022 content and the current "VPN Portal" label. This inference should not be upgraded to "the host is currently running Sophos Firewall version X," because no version, live markup, port observation, or host-specific vendor certificate was obtained.

The assessment also cannot validate the supplied MUJ SLCM technology description against this mail endpoint. The SLCM FAQ identifies the registration link as `https://mujslcm.jaipur.manipal.edu/`, gives a username pattern of `name.registration number`, and says the password is as per the official Outlook ID. [24] It provides AMS and IT support contacts for institutional users. [24] These statements connect the SLCM process to an official Outlook identity, but they do not say that SLCM, `webmail.manipal.edu`, and the current portal share a backend. Therefore, ASP.NET MVC, .NET Framework, IIS, Akamai, and Microsoft 365 identity should be treated as separate ecosystem observations unless each is independently evidenced for the same host.

## Does the host still accept credentials?

No. The public evidence does not answer that question, and the responsible conclusion is **not established**. The 2006, 2012, 2015, and 2016 archives show login fields, but none of the cited evidence shows a successful authenticated session. [15] [17] [11] [14] The 2022 replay does not provide a complete current credential result. [21]

There are at least four technically distinct possibilities: the old OWA service was retired; it was retained behind a new access gateway; the hostname was repurposed for a VPN/user portal; or the current portal proxies access to another service. The parent-domain MX and Autodiscover records establish the current mail platform for `manipal.edu`, but they do not distinguish among these host-level possibilities. [4] [7]

The MUJ SOP makes MFA mandatory for Office 365 use. [1] That further weakens any inference that a visible legacy username/password form, even if reachable, would accept credentials and grant mail access without additional controls. It does not prove the behavior of the webmail host, because the SOP documents the Microsoft 365 sign-in flow rather than the historical OWA endpoint.

A security club should not submit test credentials, use password guesses, or compare authentication responses against this host without written authorization and an agreed test plan. Such activity could lock accounts, generate incident alerts, disclose personal data, or violate institutional policy. Passive sources are sufficient to document the historical exposure and the present uncertainty; they are not sufficient to claim credential acceptance.

## Public documentation and archive availability

| Document or archive | Directly useful fact | Limitation | Exact URL |
|---|---|---|---|
| MUJ Office 365 SOP, June 2025 | Office 365 setup, Microsoft sign-in URL, MFA, password and reset workflow | Does not name `webmail.manipal.edu` | https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf |
| MUJ SLCM FAQ | SLCM link, username pattern, Outlook-ID password relationship, support contacts | Does not identify the mail host or backend | https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf |
| Wayback CDX index | Exact-host capture timestamps, paths, status, MIME types, and digests | Capture availability is not current reachability | https://web.archive.org/cdx/search/cdx?url=webmail.manipal.edu/*&output=json&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype,digest&collapse=digest |
| Microsoft Outlook page | OWA is the former name for Outlook on the web | Generic Microsoft context, not host-specific evidence | https://www.microsoft.com/en-us/microsoft-365/outlook/web-email-login-for-outlook |
| Sophos user-portal documentation | Generic user portal access model and default port 4443 | Does not prove this host runs Sophos today | https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/VPNAndUserPortalHelp/UserPortal |

The archive evidence is unusually valuable because the exact hostname appears in product-specific paths rather than only in a generic domain list. The CDX output includes a 2006 Exchange Server 2003 OWA record, a 2012 CookieAuth Exchange record, 2015/2016 OWA records, and a 2022 user-portal record. [9] The result establishes historical identity far more strongly than a search result that merely contains the word "webmail."

The archive also illustrates why negative conclusions need qualifiers. The 2022 cleaned page contains only a title-like Wayback line, "Sophos," and locale strings. [21] That absence of fields is a limitation of the captured or extracted representation, not proof that no form existed. Similarly, CertSpotter returned an empty issuance array for `webmail.manipal.edu`. This is a coverage result and should not be described as proof that the host has no certificate.

## Findings still unanswered

| Question | Answer from public evidence | Confidence |
|---|---|---|
| What is the parent-domain mail system? | Microsoft 365/Exchange Online is strongly supported by MX, Autodiscover, DKIM, and official MUJ documentation | High |
| Was the exact host historically OWA/Exchange? | Yes; the 2006 capture explicitly names Exchange Server 2003, and later captures name Exchange OWA/Outlook Web App | High |
| Is the exact host currently OWA? | Not established; current public wording points to a portal rather than a visible OWA page | Low |
| Is the exact host currently Sophos? | Supported inference from the 2022 Sophos replay and current portal wording; no definitive live fingerprint | Medium |
| Is the current backend Microsoft Exchange, Microsoft 365, VPN, or a proxy? | Not established | Low |
| Does the host accept current Microsoft 365 credentials? | Not established and intentionally not tested | None/unknown |
| Does it accept historical Exchange credentials? | Not established and intentionally not tested | None/unknown |
| Is the `/26` directly announced? | The cited RIPEstat result warns the query was aligned to a less-specific announced prefix; do not claim direct `/26` announcement | High for the limitation |
| Does the SLCM portal use this host? | The official FAQ links SLCM to an Outlook ID but does not link it to this hostname | Low |
| What are the live framework and server versions? | No reliable current passive evidence obtained for this host | None/unknown |

## VERDICT

**Confidence level: High for historical OWA/Exchange lineage and parent-domain Microsoft 365; medium for a later/current Sophos-style portal; low for current legacy OWA status; none for credential acceptance.**

The strongest defensible statement is: **`webmail.manipal.edu` is a MAHE-associated hostname on the `218.248.47.0/26` address block, historically served Microsoft Outlook Web Access through Exchange Server 2003 and later Outlook Web App, while the parent `manipal.edu` domain now publishes Microsoft 365/Exchange Online DNS and official MUJ documentation describes Microsoft 365 with mandatory MFA. Public evidence from 2022 and current indexing is consistent with the hostname later presenting a Sophos-style VPN/user portal, but the present backend, current OWA availability, and credential acceptance are not established.**

This is not evidence that the host is vulnerable, abandoned, or usable with old credentials. It is evidence of historical technology exposure and a service-identity transition that merits owner-side validation. The appropriate authorized follow-up is administrative: ask MAHE IT to confirm whether the hostname is retired, redirected, or still required; inventory any legacy Exchange dependencies; verify that old OWA paths are disabled or access-controlled; confirm that Microsoft 365 is the only intended mail authentication path; and ensure the portal does not accept inappropriate credential types. Those checks should be performed by the system owner or under written authorization, not by submitting credentials to the public endpoint.

## References

1. *Standard Operating Procedure - Manipal University Jaipur*. https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf
2. *Outlook on the Web*. https://learn.microsoft.com/en-us/exchange/clients-and-mobile-in-exchange-online/outlook-on-the-web/outlook-on-the-web
3. *External Domain Name System records for Microsoft 365*. http://learn.microsoft.com/en-us/microsoft-365/enterprise/external-domain-name-system-records?view=o365-worldwide
4. *dns.google*. https://dns.google/resolve?name=manipal.edu&type=MX
5. *dns.google*. http://dns.google/resolve?name=selector2._domainkey.manipal.edu&type=CNAME
6. *dns.google*. http://dns.google/resolve?name=selector1._domainkey.manipal.edu&type=CNAME
7. *dns.google*. https://dns.google/resolve?name=autodiscover.manipal.edu&type=CNAME
8. *dns.google*. https://dns.google/resolve?name=webmail.manipal.edu&type=A
9. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=webmail.manipal.edu/*&output=json&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype,digest&collapse=digest
10. *VPN Portal*. https://webmail.manipal.edu/
11. *Outlook Web App*. https://web.archive.org/web/20150605035251id_/https://webmail.manipal.edu/owa/auth/logon.aspx
12. *User portal - Sophos Firewall*. https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/VPNAndUserPortalHelp/UserPortal
13. *stat.ripe.net*. https://stat.ripe.net/data/whois/data.json?resource=218.248.47.16
14. *Outlook Web App*. https://web.archive.org/web/20160609223215id_/https://webmail.manipal.edu/owa/auth/logon.aspx?url=https%3A%2F%2Fwebmail.manipal.edu%2Fowa%2F%26reason=0
15. *Microsoft Outlook Web Access*. https://web.archive.org/web/20060903020056id_/https://webmail.manipal.edu/exchweb/bin/auth/owalogon.asp?url=https%3A%2F%2Fwebmail.manipal.edu%2FExchange%26reason=0
16. *Sophos*. https://web.archive.org/web/20220303013019id_/https://webmail.manipal.edu/userportal/webpages/myaccount/login.jsp
17. *Microsoft Exchange - Outlook Web Access*. https://web.archive.org/web/20120113021334id_/https://webmail.manipal.edu/CookieAuth.dll?GetLogon?curl=Z2Fexchange%26reason=0%26formdir=1
18. *Microsoft 365 Outlook Login*. https://www.microsoft.com/en-us/microsoft-365/outlook/web-email-login-for-outlook
19. *User Portal Sophos https://docs.sophos.com › en-us › utm › utmAdminGuide*. https://docs.sophos.com/nsg/sophos-utm/utm/9.7/help/en-us/Content/utm/utmAdminGuide/UserPortal.htm
20. *As Overview*. https://stat.ripe.net/data/as-overview/data.json?resource=AS9829
21. *web.archive.org*. https://web.archive.org/web/20220303013019/https://webmail.manipal.edu/userportal/webpages/myaccount/login.jsp
22. *Prefix Overview*. https://stat.ripe.net/data/prefix-overview/data.json?resource=218.248.47.0/24
23. *stat.ripe.net*. https://stat.ripe.net/data/whois/data.json?resource=AS9829
24. *Frequently Asked Questions and Contacts for SLCM Registration*. https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf
25. *manipal.edu DNS Report - ViewDNS.info*. http://viewdns.info/dnsreport?domain=manipal.edu
26. *webmail.manipal.edu - urlscan.io*. https://urlscan.io/domain/webmail.manipal.edu/
