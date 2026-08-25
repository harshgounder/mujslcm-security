## REPORT (w1-02-tech-stack.md)
## ANSWER SUMMARY
- MUJ root discloses Microsoft-IIS/10.0, X-AspNet-Version 4.0.30319, X-AspNetMvc-Version 5.3, X-Powered-By ASP.NET: IIS 10 plus ASP.NET MVC 5.3 on .NET Framework 4.x; exact Windows build and patch level not proven.
- MUJ login DOM has a local form posting to / with hidden __RequestVerificationToken, EmailFor, LoginFor, UserName, Password. Parent slcm.manipal.edu exposes ASP.NET_SessionId and no MVC version header: related but not identical stacks.
- jQuery 1.10.2 plus validate and unobtrusive scripts still loaded; validation plugin v1.11.1 from 2013. In CVE-2015-9251, CVE-2019-11358, CVE-2020-11023 ranges; CVE-2020-11022 does not apply (starts at 1.12.0).
- Keen/Metronic theme evidence strong from asset paths (keen/themes/keen/theme/demo1/dist/assets/...); exact version absent from public source.
- SSL Labs: IP 98.70.14.50, grade B, h2 and http/1.1 ALPN, TLS 1.0/1.1/1.2 enabled, BEAST/CBC/3DES warnings, no HSTS.
- SecurityHeaders: MUJ D, parent F. MUJ has X-Frame-Options SAMEORIGIN; both miss HSTS, CSP, X-Content-Type-Options, Referrer-Policy, Permissions-Policy.
- DNS via dns.google resolves MUJ to 98.70.14.50, parent to 104.211.226.160; RIPEstat maps both to Microsoft AS8075; PTR queries return status 3, no hostnames. No Cloudflare or Akamai evidence in this report.
- Backend DB unknown; parent /Home/Index returns a generic IIS 404 with no leak. Do not assume SQL Server.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/ | source of the full header fingerprint (IIS 10.0, ASP.NET 4.0.30319, MVC 5.3).
- https://api.hackertarget.com/httpheaders/?q=https://mujslcm.jaipur.manipal.edu/ | instrument behind the MUJ header claim.
- https://api.hackertarget.com/httpheaders/?q=https://slcm.manipal.edu/ | parent header report; ASP.NET_SessionId, no MVC version header.
- https://api.ssllabs.com/api/v3/analyze?host=mujslcm.jaipur.manipal.edu&fromCache=on&all=done&maxAge=168 | grade B scan; TLS 1.0/1.1/1.2 live, BEAST/CBC/3DES, no HSTS.
- https://securityheaders.com/?q=https%3A%2F%2Fmujslcm.jaipur.manipal.edu%2F&followRedirects=on | D grade; missing HSTS, CSP, nosniff, referrer, permissions.
- https://securityheaders.com/?q=https%3A%2F%2Fslcm.manipal.edu%2F&followRedirects=on | F grade; parent also lacks X-Frame-Options.
- https://mujslcm.jaipur.manipal.edu/Scripts/jquery-1.10.2.min.js | exact old jQuery asset served by the portal.
- https://mujslcm.jaipur.manipal.edu/Scripts/jquery.validate.min.js | jQuery Validation v1.11.1 (2013).
- https://mujslcm.jaipur.manipal.edu/Scripts/jquery.validate.unobtrusive.min.js | unobtrusive validation script.
- https://mujslcm.jaipur.manipal.edu/keen/themes/keen/theme/demo1/dist/assets/css/pages/login/login-v1.css | Keen demo1 login stylesheet; theme evidence.
- https://mujslcm.jaipur.manipal.edu/keen/themes/keen/theme/demo1/dist/assets/js/pages/custom/user/login.js | Keen demo1 login script; theme evidence.
- https://github.com/advisories/GHSA-rmxg-73gg-4p98 | CVE-2015-9251 advisory; jQuery before 3.0.0 cross-domain Ajax condition.
- https://github.com/advisories/GHSA-6c3j-c64m-qhgq | CVE-2019-11358 advisory; jQuery before 3.4.0 deep extension.
- https://github.com/advisories/GHSA-jpcq-cgw6-v4j6 | CVE-2020-11023 advisory; jQuery 1.x and 2.x range.
- https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=A | resolves 98.70.14.50; input to the AS8075 mapping.

## ACTIONABLE LEADS
- Enumerate sibling static assets under /Scripts/, /Content/, /keen/ for versioned bundles; look for a manifest or source map naming the Keen version.
- Recheck headers after a fix cycle: X-Powered-By, X-AspNet-Version, X-AspNetMvc-Version removal; HSTS, CSP, nosniff, Referrer-Policy, Permissions-Policy addition.
- Retest TLS after disabling 1.0/1.1 and 3DES/CBC via SSL Labs; confirm h2 ALPN behavior.
- Treat parent slcm.manipal.edu as a separate test surface: classic ASP.NET session cookie, possible .aspx/WebForms/ViewState endpoints, no MVC header.
- Use the two crt.sh queries referenced (slcm.manipal.edu, mujslcm.jaipur.manipal.edu) for certificate transparency subdomain discovery.
- Review MS15-099, MS14-059, CVE-2015-2526, CVE-2014-4075 references for .NET Framework patch relevance to the disclosed 4.0.30319 runtime.
- Confirm whether any CDN or Akamai layer sits in front (report found none); compare Server header and connection behavior directly.
- Check /elmah.axd, /trace.axd, and error behavior given the verbose header disclosure profile.
- Verify HTTP/2 with a direct curl --http2 test; IIS 10 HTTP/2 works only over TLS.

## FLAGS
- Report says no Cloudflare or Akamai evidence, but the parent task context states the target is Akamai-fronted. Direct contradiction; verify live before trusting either.
- Parent-stack front-end details are not fully citable because only one browser capture was allowed (MUJ only).
- The sentence "The key fingerprint is not just" ends abruptly before References; the report body is truncated mid-thought (generation artifact).
- Exact Keen/Metronic version unverified; ref 29 title says Metronic while body evidence is Keen, a naming mismatch.
- CVE mapping for older .NET bulletins (MS15-099, MS14-059) is listed but never explained in the body.
- Windows build and .NET patch level not proven by headers; IIS 10 only implies Server 2016 or newer.
- SSL Labs result used fromCache=on; single snapshot, grade can drift.
- All CVE claims are range membership only; no sink or reachability proof.

## COVERAGE
- 12321 chars read; verified to EOF (98/98 lines, read_file truncated: false).