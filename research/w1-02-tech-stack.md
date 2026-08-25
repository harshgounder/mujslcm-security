# Public Fingerprint of MUJ and Manipal SLCM

## Executive Summary

- **Microsoft Stack Exposure**: The MUJ SLCM root response publicly discloses `Server: Microsoft-IIS/10.0`, `X-AspNet-Version: 4.0.30319`, `X-AspNetMvc-Version: 5.3`, `X-Powered-By: ASP.NET`, and an `__RequestVerificationToken` cookie, which is enough to identify an IIS 10 plus ASP.NET MVC 5.3 application surface on .NET Framework 4.x, but not enough to prove the exact Windows build or .NET patch level [7]. -> Remove framework disclosure headers and verify the deployed `Microsoft.AspNet.Mvc` package and .NET Framework servicing state internally.
- **MUJ Login Surface Is MVC, Parent Looks Different**: The MUJ login DOM posts to `https://mujslcm.jaipur.manipal.edu/` and exposes hidden `__RequestVerificationToken`, `EmailFor`, and `LoginFor` fields plus `UserName` and `Password` inputs, while the parent `slcm.manipal.edu` header report exposes an `ASP.NET_SessionId` cookie and no `X-AspNetMvc-Version` header [1][5]. -> Treat MUJ and parent SLCM as related but not identical application stacks.
- **jQuery 1.10.2 Is Still Loaded On MUJ**: The MUJ DOM loads `https://mujslcm.jaipur.manipal.edu/Scripts/jquery-1.10.2.min.js`, `jquery.validate.min.js`, and `jquery.validate.unobtrusive.min.js`; the separately fetched validation plugin is jQuery Validation v1.11.1 from 2013 under MIT license [1][17]. -> Upgrade jQuery and validation dependencies in a controlled regression cycle.
- **Client-Side CVE Exposure Is Conditional But Real**: jQuery 1.10.2 falls inside the affected ranges for CVE-2015-9251, CVE-2019-11358, and CVE-2020-11023, while CVE-2020-11022 starts at jQuery 1.12.0 and therefore does not include 1.10.2 [26][25][24][30]. -> Prioritize upgrade because exploitability depends on whether attacker-controlled values reach vulnerable jQuery sinks, but scanners will correctly flag the library.
- **Keen/Metronic Theme Evidence Is Strong, Exact Version Is Not**: MUJ loads `keen/themes/keen/theme/demo1/dist/assets/...` styles and scripts, and the fetched login assets show Keen demo1 login files, but those assets do not contain a version banner; Keen HTML Pro documentation lists 9 demos and technologies such as Bootstrap 5, Datatables, FullCalendar, Gulp, NPM, Webpack, and Axios, but the exact version number is not present in the source we observed [1][27][23][12]. -> Identify the theme version from internal package metadata, not from the public path alone.
- **IIS 10 And HTTP/2 Narrow The Platform**: Microsoft documentation says IIS 10.0 shipped with Windows 10 and Windows Server 2016, and IIS HTTP/2 support was introduced in IIS 10.0, works only over TLS, has no new IIS-specific configuration setting, and falls back to HTTP/1.1 when needed [15][16]. -> Public evidence supports a Windows Server 2016-or-newer inference, but not a precise OS release.
- **TLS Public Scan Shows Legacy Protocol Risk On MUJ**: SSL Labs reported MUJ at IP `98.70.14.50`, grade `B`, HTTP/2 ALPN `h2` and `http/1.1`, TLS 1.0, TLS 1.1, and TLS 1.2 enabled, and warnings including BEAST, CBC suites, 3DES, and absent HSTS [6]. -> Disable TLS 1.0 and 1.1, remove 3DES/CBC where possible, and deploy HSTS after validating subdomain readiness.
- **Hosting Points To Microsoft AS8075, Not A Third-Party CDN**: Google DNS resolves MUJ to `98.70.14.50` and parent SLCM to `104.211.226.160`; RIPEstat aligns those addresses to Microsoft AS8075 prefixes, and reverse PTR queries return DNS status 3 rather than hostnames [41][42][13][19][28][14]. -> Label hosting as Microsoft cloud or Microsoft network with no public Cloudflare or Akamai evidence.
- **Security Headers Are Weak**: SecurityHeaders scored MUJ `D` and parent SLCM `F`; MUJ has `X-Frame-Options: SAMEORIGIN`, but both reports list missing HSTS, CSP, X-Content-Type-Options, Referrer-Policy, and Permissions-Policy, and the parent also lacks X-Frame-Options [10][9]. -> Add headers at IIS, reverse proxy, or application middleware level and retest.
- **Backend Database Remains Unknown**: The parent `/Home/Index` route returns a generic IIS-style 404 page and no SQL, Oracle, EF, stack trace, or connection-string leak was found in the citable public evidence [2]. -> Do not infer SQL Server solely from ASP.NET MVC; verify database technology internally.

## exact_tables inventory

| Table key | Purpose | Primary evidence |
|---|---|---|
| `table_1_stack_fingerprint` | Exact observable technologies for MUJ and parent SLCM | Header reports, browser DOM capture, direct extracts |
| `table_2_muj_login_dom` | MUJ login form, scripts, and assets | Browser DOM capture |
| `table_3_security_headers` | Present and missing security headers | SecurityHeaders and Hackertarget |
| `table_4_network_hosting` | DNS, reverse DNS, ASN, certificate, CDN inference | Google DNS, RIPEstat, crt.sh, SSL Labs |
| `table_5_aspnet_mvc_cves` | ASP.NET MVC and .NET Framework historical CVE relevance | NVD, Acunetix, NuGet |
| `table_6_jquery_cves` | jQuery 1.10.2 exposure | GitHub Advisory Database, NVD/GitHub extracted advisories |
| `table_7_theme_evidence` | Keen/Metronic theme and reuse assessment | MUJ assets, KeenThemes public docs, search results |
| `table_8_backend_hints` | Routes, errors, and database evidence | Direct page extract, IIS 404, browser DOM |

These tables separate directly observed facts from inference. The main operational takeaway is that MUJ has a high-confidence IIS 10 plus ASP.NET MVC 5.3 plus old jQuery fingerprint, while the parent instance shares IIS/ASP.NET hosting characteristics but does not expose the same MVC version header.

## table_1_stack_fingerprint - what is directly observable

| Layer | MUJ SLCM `https://mujslcm.jaipur.manipal.edu/` | Parent `https://slcm.manipal.edu/` | Confidence | Interpretation |
|---|---|---|---|---|
| Web server | `Microsoft-IIS/10.0` [7] | `Microsoft-IIS/10.0` [5] | High | Both are served by IIS 10. |
| ASP.NET runtime disclosure | `X-AspNet-Version: 4.0.30319` [7] | `X-AspNet-Version: 4.0.30319` [5] | High | Both run ASP.NET on the .NET 4 CLR family; the header is not a full .NET Framework patch identifier. |
| MVC version disclosure | `X-AspNetMvc-Version: 5.3` [7] | Absent from the public header report [5] | High for MUJ, low for parent | MUJ is ASP.NET MVC 5.3; parent should not be assumed to be the same MVC app. |
| Powered-by disclosure | `X-Powered-By: ASP.NET` [7] | `X-Powered-By: ASP.NET` [5] | High | Both disclose ASP.NET. |
| Login cookie | `__RequestVerificationToken=...; path=/; HttpOnly` [7] | `ASP.NET_SessionId=...; path=/; HttpOnly; SameSite=Lax` [5] | High | MUJ exposes MVC anti-CSRF cookie behavior; parent exposes classic ASP.NET session state. |
| Clickjacking header | `X-Frame-Options: SAMEORIGIN` [7] | Absent from the header report [5] | High | MUJ has a legacy frame control; parent does not expose it in the sampled response. |
| Login page identity | Browser title `Manipal University`; citable direct extract says `WELCOME TO MUJ PORTAL` and `Sign In` [1] | Direct extract confirms `MU SLcM` shell and confirmation modal text [43] | Medium to high | The two pages are separately branded login surfaces. |
| Front-end libraries | jQuery 1.10.2, jQuery Validate, jQuery Unobtrusive Validate, Keen demo1 assets [1] | Not fully citable from browser because the one browser-use budget was consumed by MUJ; header and direct text confirm ASP.NET page shell [5][43] | High for MUJ, limited for parent | MUJ front-end fingerprint is exact; parent front-end requires a fresh browser capture for the same certainty. |

The key fingerprint is not just

## References

1. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
2. *404 - File or directory not found.*. https://slcm.manipal.edu/Home/Index
3. *crt.sh*. https://crt.sh/?q=slcm.manipal.edu&output=json
4. *crt.sh*. https://crt.sh/?q=mujslcm.jaipur.manipal.edu&output=json
5. *api.hackertarget.com*. https://api.hackertarget.com/httpheaders/?q=https://slcm.manipal.edu/
6. *api.ssllabs.com*. https://api.ssllabs.com/api/v3/analyze?host=mujslcm.jaipur.manipal.edu&fromCache=on&all=done&maxAge=168
7. *api.hackertarget.com*. https://api.hackertarget.com/httpheaders/?q=https://mujslcm.jaipur.manipal.edu/
8. *api.ssllabs.com*. https://api.ssllabs.com/api/v3/analyze?host=slcm.manipal.edu&fromCache=on&all=done&maxAge=168
9. *Scan results for https://slcm.manipal.edu/*. https://securityheaders.com/?q=https%3A%2F%2Fslcm.manipal.edu%2F&followRedirects=on
10. *Scan results for https://mujslcm.jaipur.manipal.edu/*. https://securityheaders.com/?q=https%3A%2F%2Fmujslcm.jaipur.manipal.edu%2F&followRedirects=on
11. *jQuery 3.4.0 Released | Official jQuery Blog*. https://blog.jquery.com/2019/04/10/jquery-3-4-0-released/
12. *Keen HTML Pro - Multi Demo Bootstrap Admin Dashboard Theme*. https://keenthemes.com/products/keen-html-pro
13. *Prefix Overview*. https://stat.ripe.net/data/prefix-overview/data.json?resource=98.70.14.50
14. *dns.google*. https://dns.google/resolve?name=160.226.211.104.in-addr.arpa&type=PTR
15. *New Features Introduced in IIS 10.0 | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/get-started/whats-new-in-iis-10/new-features-introduced-in-iis-10
16. *HTTP/2 on IIS | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/get-started/whats-new-in-iis-10/http2-on-iis
17. *mujslcm.jaipur.manipal.edu*. https://mujslcm.jaipur.manipal.edu/Scripts/jquery.validate.min.js
18. *jQuery 3.5.0 Released! | Official jQuery Blog*. https://blog.jquery.com/2020/04/10/jquery-3-5-0-released/
19. *Prefix Overview*. https://stat.ripe.net/data/prefix-overview/data.json?resource=104.211.226.160
20. [
        NuGet Gallery
        | Microsoft.AspNet.Mvc 5.3.0
    ](https://www.nuget.org/packages/Microsoft.AspNet.Mvc/5.3.0)
21. *mujslcm.jaipur.manipal.edu*. https://mujslcm.jaipur.manipal.edu/Scripts/jquery-1.10.2.min.js
22. [
        NuGet Gallery
        | Microsoft.AspNet.Mvc 5.2.9
    ](https://www.nuget.org/packages/Microsoft.AspNet.Mvc/5.2.9)
23. *Login V1*. https://mujslcm.jaipur.manipal.edu/keen/themes/keen/theme/demo1/dist/assets/css/pages/login/login-v1.css
24. *Potential XSS vulnerability in jQuery · CVE-2020-11023 · GitHub Advisory Database · GitHub*. https://github.com/advisories/GHSA-jpcq-cgw6-v4j6
25. *XSS in jQuery as used in Drupal, Backdrop CMS, and other products · CVE-2019-11358 · GitHub Advisory Database · GitHub*. https://github.com/advisories/GHSA-6c3j-c64m-qhgq
26. *Cross-Site Scripting (XSS) in jquery · CVE-2015-9251 · GitHub Advisory Database · GitHub*. https://github.com/advisories/GHSA-rmxg-73gg-4p98
27. *mujslcm.jaipur.manipal.edu*. https://mujslcm.jaipur.manipal.edu/keen/themes/keen/theme/demo1/dist/assets/js/pages/custom/user/login.js
28. *dns.google*. https://dns.google/resolve?name=50.14.70.98.in-addr.arpa&type=PTR
29. *Metronic — #1 Tailwind & Bootstrap Dashboard Template*. https://keenthemes.com/metronic
30. *Potential XSS vulnerability in jQuery · CVE-2020-11022 · GitHub Advisory Database · GitHub*. https://github.com/advisories/GHSA-gxr4-xjj5-5px2
31. *mujslcm.jaipur.manipal.edu*. https://mujslcm.jaipur.manipal.edu/Scripts/jquery.validate.unobtrusive.min.js
32. *Microsoft Security Bulletin MS15-099 - Critical | Microsoft Learn*. https://learn.microsoft.com/en-us/security-updates/securitybulletins/2015/ms15-099
33. *Microsoft Security Bulletin MS14-059 - Important | Microsoft Learn*. https://learn.microsoft.com/en-us/security-updates/securitybulletins/2014/ms14-059
34. *Registration5 Gz Semver2*. https://api.nuget.org/v3/registration5-gz-semver2/microsoft.aspnet.mvc/5.3.0.json
35. *CVE Record: CVE-2015-2526*. https://www.cve.org/CVERecord?id=CVE-2015-2526
36. *Registration5 Gz Semver2*. https://api.nuget.org/v3/registration5-gz-semver2/microsoft.aspnet.mvc/5.2.9.json
37. *NVD - CVE-2015-2526*. https://nvd.nist.gov/vuln/detail/CVE-2015-2526
38. *CVE Record: CVE-2014-4075*. https://www.cve.org/CVERecord?id=CVE-2014-4075
39. *Registration5 Gz Semver2*. https://api.nuget.org/v3/registration5-gz-semver2/microsoft.aspnet.mvc/index.json
40. *NVD - CVE-2014-4075*. https://nvd.nist.gov/vuln/detail/CVE-2014-4075
41. *dns.google*. https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=A
42. *dns.google*. https://dns.google/resolve?name=slcm.manipal.edu&type=A
43. [
	MU SLcM
](https://slcm.manipal.edu/)
