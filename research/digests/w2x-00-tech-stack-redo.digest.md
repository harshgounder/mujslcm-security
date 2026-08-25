# Digest: w2x-00-tech-stack-redo

## REPORT
Source file: w2x-00-tech-stack-redo.md (MUJ SLCM Stack, Exposure, and Infrastructure Assessment)

## ANSWER SUMMARY
- Stack confirmed from public evidence: IIS 10.0, X-AspNet-Version 4.0.30319, X-AspNetMvc-Version 5.3 on MUJ; the parent slcm.manipal.edu independently reports IIS 10.0 and ASP.NET 4.0.30319.
- The YSOD value 4.7.4136.0 is an ASP.NET/System.Web assembly servicing version, not an installed-runtime or Windows patch inventory. Exact patch state is not publicly determinable.
- jQuery 1.10.2 with jquery.validate and jquery.validate.unobtrusive sits in the archived Keen demo1 asset tree used by the login page. This report counts 1.10.2 inside all four requested CVE ranges.
- CVE-2020-11023 has a concrete real-world signal: CISA added it to the KEV catalog on 2025-01-23. Exploitability at MUJ still depends on data flow.
- The "Akamai edge" label is contradicted: MUJ resolves to 98.70.14.50, AS8075 Microsoft (Pune), inside 98.70.0.0/15, with no PTR. Sibling muj.slcm.jaipur.manipal.edu is 20.244.94.89, also AS8075. A historical Akamai layer is possible but not established.
- TLS: both hosts grade B on SSL Labs. Both offer TLS 1.0, 1.1, 1.2, 3DES, static-RSA and CBC suites, negotiate HTTP/2 via ALPN, and lack HSTS. MUJ cert is an Entrust DV RSA cert for a single name (issued 2025-12-22, expiry 2026-12-21); parent uses a *.manipal.edu Sectigo OV wildcard.
- Missing anti-forgery token produces an HTTP 500 YSOD with a full stack trace. The exception is consistent with token enforcement, not a CSRF bypass; the defect is detailed remote error disclosure.
- Verdict: legacy ASP.NET MVC/IIS deployment with material hardening gaps, one obsolete client library, and an unproven runtime patch level. No server-side RCE, CSRF bypass, session fixation, ViewState exploit, path traversal, or MUJ-specific XSS demonstrated.

## KEY FACTS
- https://api.ssllabs.com/api/v3/analyze?host=mujslcm.jaipur.manipal.edu&publish=off&all=done&fromCache=on - MUJ grade B, TLS 1.0/1.1/1.2, h2 ALPN, MVC/IIS headers, no HSTS.
- https://api.ssllabs.com/api/v3/analyze?host=slcm.manipal.edu&publish=off&all=done&fromCache=on - parent grade B, classic ASP.NET session cookie (HttpOnly, SameSite=Lax), no XFO in capture.
- https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=A - current A record 98.70.14.50.
- https://ipinfo.io/98.70.14.50 - AS8075 Microsoft, Pune, marked hosting.
- https://bgp.he.net/ip/98.70.14.50 - route 98.70.0.0/15 owned by Microsoft.
- https://dns.google/resolve?name=muj.slcm.jaipur.manipal.edu&type=A - sibling hostname resolves to 20.244.94.89 (AS8075).
- http://web.archive.org/cdx/search/cdx?collapse=urlkey&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&output=json&url=mujslcm.jaipur.manipal.edu/* - archived asset inventory with Keen demo1 tree and jquery-1.10.2.min.js.
- https://crt.sh/?q=mujslcm.jaipur.manipal.edu&output=json - Entrust DV RSA certificate, single DNS name, 2025-12-22 to 2026-12-21.
- https://nvd.nist.gov/vuln/detail/CVE-2020-11023 - option-element HTML XSS; 1.10.2 in range; KEV-listed.
- https://www.cisa.gov/news-events/alerts/2025/01/23/cisa-adds-one-known-exploited-vulnerability-catalog - CVE-2020-11023 added to KEV on 2025-01-23.
- https://learn.microsoft.com/en-us/aspnet/mvc/overview/security/xsrfcsrf-prevention-in-aspnet-mvc-and-web-pages - two-token antiforgery model; missing, unreadable, or swapped tokens throw, which explains the YSOD.
- https://learn.microsoft.com/en-us/iis/get-started/whats-new-in-iis-10/http2-on-iis - IIS 10 HTTP/2 over TLS with HTTP/1.1 fallback, matching ALPN h2 http/1.1.
- https://learn.microsoft.com/en-us/iis/manage/configuring-security/use-request-filtering - IIS filter rejection codes 404.6/404.7/404.8/404.11/404.14/404.15 for verb, extension, hidden segment, double-encoding, and size rules.
- https://urlscan.io/api/v1/search/?q=filename%3A%22keen%2Fthemes%2Fkeen%2Ftheme%2Fdemo1%2Fdist%2Fassets%2Fcss%2Fpages%2Flogin%2Flogin-v1.css%22 - exact-path query returned MUJ scans only; no unrelated deployment asserted.
- https://dns.google/resolve?name=manipal.edu&type=TXT - SPF references Microsoft 365 protection, Brightspace, SendGrid, Salesforce; DMARC published at p=none via https://dns.google/resolve?name=_dmarc.manipal.edu&type=TXT.

## ACTIONABLE LEADS
- Authorized test order: DOM XSS and prototype pollution sinks; error handling (generic pages plus correlation IDs); antiforgery semantics (omission, swap, replay, identity change); session fixation and rotation; IIS path normalization parity; header and framing policy; TLS hardening; conditional ViewState/machineKey only where __VIEWSTATE appears; alternate-host parity for 20.244.94.89.
- Do not frame testing as an Akamai bypass. Establish the actual Azure service, load balancer, WAF, or direct-IIS topology from owner records first, then test front-door and origin parity.
- TLS remediation order: disable TLS 1.0/1.1 and 3DES/static-RSA, keep TLS 1.2 with modern suites, add TLS 1.3 where the platform allows, then staged HSTS starting with a short max-age.
- Suppress Server, X-Powered-By, X-AspNet-Version, and X-AspNetMvc-Version headers where operationally possible; this is recon reduction, not a patch.
- Confirm Secure and SameSite flags on the antiforgery cookie and session cookie; verify token pair binding and rotation on login.
- No YSOD corpus hunting or index probing; report privately to the university owner via coordinated disclosure.

## FLAGS
- Contradicts the "behind Akamai" premise used by w2f-01/w2f-02/w2f-03/w2f-04: AS8075 ownership and absent PTR contradict current Akamai edge attribution. Historical Akamai involvement is not ruled out.
- Cross-report CVE-2020-11022 conflict: this report counts 1.10.2 in range (>=1.2, <3.5.0 per NVD), while w2f-03 excludes it using the current CVE.org range (>=1.12.0). Both range sources are cited; canonical-record conflict must be resolved before the final count.
- 52.172.36.15 and 202.131.155.153 have no established portal relationship; naming them as origins would be speculation (the report says so explicitly).
- The YSOD observation is supplied hands-on evidence for 2026-08-25, not independently reproduced in this repo; treat as user-supplied.
- Keen demo1 fingerprint is high confidence for product, low for release; no exact Keen/Metronic version claim is supported.
- NVD keyword searches for Keenthemes and Keen theme returned zero; the single Metronic NVD hit was a name collision and was not assigned.
- SSL Labs grades and profiles are point-in-time cached scans; they can drift.

## COVERAGE
Chars read: 45,130 (file size), 373 lines. EOF confirmed: true (truncated false).

DONE w2x-00-tech-stack-redo.digest.md