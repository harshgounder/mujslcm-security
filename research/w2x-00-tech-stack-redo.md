# MUJ SLCM Stack, Exposure, and Infrastructure Assessment

## Executive Summary

- **Legacy Stack Confirmed**: The MUJ login surface is a classic ASP.NET MVC application on Microsoft IIS 10.0. Public response data reports `X-AspNetMvc-Version: 5.3`, `X-AspNet-Version: 4.0.30319`, and `X-Powered-By: ASP.NET`; the parent instance independently reports IIS 10.0 and ASP.NET 4.0.30319 [28][29]. The practical action is to manage it as an in-place-serviced .NET Framework application, not as modern ASP.NET Core.

- **Patch Level Remains Unproven**: The disclosed YSOD value `ASP.NET Version: 4.7.4136.0` is best treated as a System.Web/ASP.NET assembly servicing version, not a complete installed-runtime or Windows patch inventory. Microsoft identifies the .NET Framework 4.5+ installation through the registry `Release` DWORD, while CLR and framework assemblies are versioned separately [18]. Therefore, no exact KB, CVE remediation state, or Windows Server release can responsibly be inferred from `4.7.4136.0` alone.

- **jQuery Is The Clearest Client-Side Risk**: The archived asset inventory exposes jQuery 1.10.2 and its validation plug-ins in the same Keen `demo1` tree used by the login page [11]. Version 1.10.2 falls inside the affected ranges for CVE-2015-9251, CVE-2019-11358, CVE-2020-11022, and CVE-2020-11023 [16][13][8][59]. Exploitability still depends on application data flow, but CVE-2020-11023 has a concrete real-world exploitation signal because CISA added it to the Known Exploited Vulnerabilities catalog [20][58].

- **Keen Fingerprint Is Strong, Exact Release Is Not**: The path `/keen/themes/keen/theme/demo1/dist/assets/...` and associated bundled CSS/JavaScript establish a high-confidence Keenthemes Keen `demo1` template fingerprint [11]. They do not expose a package manifest or release number, so mapping the site to a precise Keen or Metronic version would be speculation. An exact-path URLScan query found MUJ scans rather than a defensible list of unrelated deployments [53].

- **TLS Modernization Is Overdue**: SSL Labs graded both public hosts **B**. Both offered TLS 1.0, 1.1, and 1.2, negotiated HTTP/2 through ALPN, and exposed CBC, static-RSA, and 3DES compatibility suites; HSTS was absent [28][29]. The remediation order is to disable TLS 1.0/1.1 and 3DES/static-RSA suites, validate TLS 1.2 interoperability, add TLS 1.3 where the Windows/IIS platform permits it, and then deploy HSTS safely.

- **Current Evidence Does Not Support Akamai Attribution**: MUJ currently resolves to `98.70.14.50` [1], but both IPInfo and BGP data map that address to Microsoft Corporation, AS8075, inside `98.70.0.0/15` [42][44]. Its reverse lookup has no PTR answer [9]. The supplied label "Akamai edge IP" is therefore not corroborated and is contradicted by current routing ownership. A historical Akamai layer remains possible, but it is not established by the collected public evidence.

- **Header Posture Is Uneven And Incomplete**: MUJ sends `X-Frame-Options: SAMEORIGIN`; the parent capture does not. Neither captured response includes CSP, HSTS, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`, or COOP [28][29]. These omissions remove browser-side defense in depth. They do not by themselves prove XSS, clickjacking, or data leakage.

- **Detailed Error Disclosure Is A Confirmed Operational Defect**: The supplied public observation found that omitting the anti-forgery token triggered an HTTP 500 YSOD with a full stack trace and `ASP.NET Version: 4.7.4136.0`. ASP.NET's documented anti-forgery behavior is to throw when either token is absent, unreadable, swapped, or mismatched [21]. The exception is therefore consistent with enforcement, not evidence of a CSRF bypass; the security defect is returning diagnostic detail to a remote, unauthenticated client.

- **Testing Should Follow Evidence, Not Product Folklore**: The first authorized tests should trace untrusted data into jQuery DOM sinks, validate anti-forgery and session transitions, verify production error handling, and examine IIS path normalization. ViewState and machineKey testing is conditional: the sampled MUJ MVC login did not establish a WebForms `__VIEWSTATE` surface. Test it only on endpoints that actually emit ViewState or other machineKey-protected artifacts.

## Scope, Evidence Standard, and Reproducible Reasoning

This assessment covers only public behavior of `https://mujslcm.jaipur.manipal.edu`, `https://slcm.manipal.edu`, and the related hostname `https://muj.slcm.jaipur.manipal.edu`. It combines current DNS, CT, SSL Labs, IP/ASN, direct-page, search-index, and web-archive evidence with the hands-on observations supplied for 2026-08-25. The visible MUJ page identifies itself as "WELCOME TO MUJ PORTAL," offers ordinary and parent sign-in, and displays the `@muj.manipal.edu` identity context [4]. The parent host exposes a distinct, sparse public page [3].

No intrusive requests, credential attacks, origin bypass attempts, or exploitation were used. "Present" means that a public response, asset, DNS record, or archive disclosed the feature. "Absent" means absent from the specifically captured public response, not necessarily absent from every route. "Inference" means the conclusion fits the evidence but is not directly stated by the host. "Unknown" is used where public data cannot decide the issue.

The report does not expose private chain-of-thought. Instead, each conclusion uses a reproducible four-step structure: **observation -> documented mechanism -> bounded inference -> authorized verification**. That provides an auditable basis without pretending that a banner proves configuration that only a server administrator can inspect.

### Exact evidence-to-conclusion matrix

| Observation | Direct evidence | Bounded conclusion | Confidence |
|---|---|---|---|
| IIS and ASP.NET banners | IIS 10.0, MVC 5.3, ASP.NET 4.0.30319 headers [28] | Classic ASP.NET MVC on .NET Framework/System.Web | High |
| `ASP.NET Version: 4.7.4136.0` in YSOD | Supplied public error capture | A 4.7 servicing-branch ASP.NET assembly is plausible; exact installed Framework/KB is unknown | Medium for branch, low for exact patch |
| jQuery 1.10.2 path | Archived asset inventory [11] | Login front end ships a vulnerable-version-range jQuery release | High |
| Keen `demo1` path | Archived CSS and bundle paths [11] | Keenthemes Keen demo1 product/template | High for product, low for release |
| MUJ A record `98.70.14.50` | Google DNS [1] | Current public endpoint address | High |
| AS8075 Microsoft route | IPInfo and BGP [42][44] | Current address attribution is Microsoft/Azure, not demonstrated Akamai | High |
| Missing browser headers | SSL Labs response header capture [28][29] | Browser defense-in-depth gaps on sampled routes | High for sampled responses |
| Missing anti-forgery token produces exception | Supplied capture plus documented failure behavior [21] | Validation appears active; detailed error handling is unsafe | High |

This distinction matters. A version header identifies a technology, but it does not establish whether Windows cumulative updates are current. A cookie identifies a session mechanism, but it does not prove fixation. A missing CSP increases the impact of an injection flaw, but it does not create the injection flaw.

## Exact Application Stack and Request Flow

The most defensible stack model is:

| Layer | MUJ evidence | Parent evidence | Assessment |
|---|---|---|---|
| Transport | HTTPS, ALPN `h2 http/1.1`, HTTP/2 [28] | HTTPS, ALPN `h2 http/1.1`, HTTP/2 [29] | IIS 10 HTTP/2 over TLS |
| Web server | `Microsoft-IIS/10.0` [28] | `Microsoft-IIS/10.0` [29] | Confirmed |
| Application framework | MVC 5.3, ASP.NET 4.0.30319 [28] | ASP.NET 4.0.30319 [29] | MUJ is MVC; parent is classic ASP.NET, exact UI framework not fully proven |
| Runtime family | Supplied YSOD says ASP.NET 4.7.4136.0 | No comparable YSOD cited | .NET Framework 4.x/System.Web; exact installed release unknown |
| UI template | Keen `theme/demo1/dist/assets` [11] | Not established | Keenthemes Keen demo1, release unknown |
| JavaScript | jQuery 1.10.2, jquery.validate, jquery.validate.unobtrusive [11] | Not established | Legacy jQuery validation stack |
| CSRF control | `__RequestVerificationToken` cookie and form token; cookie is HttpOnly [28] | Not established in captured headers | ASP.NET MVC synchronizer-token variant |
| Session | No `ASP.NET_SessionId` in cited MUJ response | `ASP.NET_SessionId`, HttpOnly, SameSite=Lax [29] | Parent uses classic ASP.NET session state on sampled route |
| Post-login route | Supplied redirect target `/Home/Index` | Unknown | Conventional MVC controller/action shape, not proof of default route configuration |
| Identity recovery | Supplied link to `passwordreset.microsoftonline.com` | Unknown | Entra password-reset dependency for that workflow, not proof all authentication is federated |

### Case study: the missing-token YSOD

The login form submits `UserName`, `Password`, the hidden `EmailFor` and `LoginFor` values, and an anti-forgery field to `/`, according to the supplied direct markup capture. Removing the anti-forgery token produced an HTTP 500 with a detailed YSOD. ASP.NET MVC's anti-XSRF implementation uses two tokens, one normally in a cookie and one in the form, and signs/encrypts their payloads [21]. `Html.AntiForgeryToken` generates them and `ValidateAntiForgeryToken` performs validation [21].

The outcome reveals two separate controls. First, token validation likely ran, because missing-token failure is a documented exception condition [21]. Second, production exception handling exposed internal diagnostics. It would be incorrect to call this an anti-forgery bypass. The actionable finding is to return a generic 4xx/5xx page remotely, retain full detail only in protected logs, and ensure monitoring records repeated validation failures.

## ASP.NET 4.7.4136.0 and Patch-Level Analysis

### What the number can and cannot mean

`X-AspNet-Version: 4.0.30319` is the CLR/System.Web compatibility lineage used by .NET Framework 4.x; it is not the marketing release number for 4.7, 4.7.2, 4.8, or 4.8.1. Microsoft explains that .NET Framework contains assemblies and a CLR that are versioned separately [18]. For Framework 4.5 and later, the supported way to identify the installed product is the registry's `Release` DWORD [18].

The YSOD footer's `4.7.4136.0` is therefore best classified as an **ASP.NET/System.Web assembly file or product version**. Its `4.7` prefix is consistent with the in-place .NET Framework 4.7 servicing family, but it does not uniquely establish "Framework 4.7.2 with KB X." Servicing can vary with Windows SKU, cumulative update branch, and assembly. A remote analyst lacks the registry Release value, `System.Web.dll` file metadata, OS build, and installed-KB inventory needed for exact mapping.

Microsoft also treats .NET Framework 4.5.2 and later as Windows components whose support follows the underlying OS [17]. Framework 4.8.1 is the latest Framework release, while 4.8, 4.7.2, 4.7.1, and 4.7 remain listed as active only when installed on supported Windows versions [17]. This creates an important distinction: an old-looking ASP.NET assembly string is a patch-management warning, not conclusive evidence of an unpatched machine.

### Representative .NET 4.x CVE chronology

| CVE | Published | Documented mechanism and affected line | Relation to `4.7.4136.0` | What can be concluded remotely |
|---|---:|---|---|---|
| CVE-2017-8759 | 2017-09-13 | .NET Framework 2.0 through 4.7 could permit remote code execution through a malicious document or application [33] | Predates later 4.7 servicing builds | Historical exposure existed in the product line; current patch status unknown |
| CVE-2019-0820 | 2019-05-16 | .NET Framework and .NET Core denial of service caused by improper processing of regular-expression strings; records include Framework 4.7.2 [32] | Later than the original 4.7.2 release | Cannot infer whether its Windows update is installed from a YSOD footer |
| CVE-2023-36560 | 2023-11-14 | ASP.NET security-feature bypass, CVSS 8.8 High; affected records include Framework 4.7.x/4.7.2 branches [34] | Much later security servicing event | Exact remediation requires OS/KB verification; banner alone is insufficient |

For CVE-2023-36560, the CVE record includes a 4.7 branch boundary of versions before `4.7.4076.0` for several product combinations [34]. It is tempting to compare `4.7.4136.0` numerically and declare the portal fixed. That would be unsafe: the YSOD number and CVE configuration boundaries may describe different package/OS combinations. Numeric comparison across servicing branches is not a substitute for Microsoft's applicable update record.

### Patch verification requirement

The owner should collect four items from the server: Windows edition and build, .NET `Release` DWORD, `System.Web.dll` file/product version and signature, and installed cumulative/security KBs. Compare those with the Microsoft Security Response Center entries applicable to that OS. If the application remains on a 4.7-era runtime, plan an upgrade to 4.8 or 4.8.1 where supported, but do not treat an in-place runtime upgrade as a replacement for application regression tests.

The conclusion is deliberately narrower than the requested "exact patch." **Exact patch status is not publicly determinable.** Claiming otherwise would turn a useful fingerprint into an unsupported vulnerability assertion.

## jQuery 1.10.2: Four CVEs, Mechanics, and Actual Exposure

The archived MUJ tree names `jquery-1.10.2.min.js`, `jquery.validate`, and `jquery.validate.unobtrusive` [11]. This is direct version evidence, stronger than guessing from API behavior. However, a vulnerable library version is only the first half of exploitability. The application must also pass attacker-influenced data through the affected function or sink.

### Exact CVE matrix

| CVE | Affected versions | Mechanism | Does 1.10.2 fall in range? | MUJ-specific exploit status |
|---|---|---|---|---|
| CVE-2015-9251 | jQuery before 3.0.0 [16] | A cross-domain Ajax request without an explicit `dataType` can execute a `text/javascript` response, producing XSS [16] | Yes | No affected Ajax call was publicly demonstrated |
| CVE-2019-11358 | jQuery before 3.4.0 [13] | Deep `jQuery.extend(true, {}, source)` can let an enumerable `__proto__` property modify `Object.prototype` [13] | Yes | No untrusted deep-merge data flow was demonstrated |
| CVE-2020-11022 | jQuery >=1.2 and <3.5.0 [8] | Untrusted HTML passed to `.html()`, `.append()`, or related DOM manipulation can execute code, even after some sanitization [8] | Yes | No attacker-controlled DOM sink was demonstrated |
| CVE-2020-11023 | jQuery >=1.0.3 and <3.5.0 [59] | Untrusted HTML containing `option` elements passed to manipulation methods may execute code [20] | Yes | No MUJ exploit was demonstrated; CISA KEV establishes exploitation in the wider ecosystem [20] |

CVE-2019-11358 is a prototype-pollution primitive, not automatically XSS. The jQuery project described the flaw as unintended `Object.prototype` extension and fixed it in 3.4.0 [26]. A practical exploit requires an attacker-controlled object, a vulnerable deep merge, and a later security-sensitive use of the polluted property. The login page's mere inclusion of jQuery does not prove those conditions.

CVE-2020-11022 and CVE-2020-11023 concern HTML parsing and DOM insertion. jQuery 3.5.0 changed `htmlPrefilter`; the project explicitly described the release's main change as a security fix [24]. CVE-2020-11023 deserves priority because CISA's catalog shows known exploitation outside MUJ [20]. That catalog status raises urgency but does not establish that this portal is exploitable.

### Case study: why a login page can still expose DOM risk

A common dismissal is that a login page has only static HTML. That conclusion should be tested, not assumed. Validation messages, server-returned errors, query-string banners, password-reset status, and role-specific labels can all become attacker-influenced strings. If code inserts those strings using `.html()` or `.append()`, the 2020 jQuery flaws become relevant. If code uses `textContent`, `.text()`, or fixed templates, the same vulnerable library may be unreachable through that route.

The authorized test should inventory every call to `.html()`, `.append()`, `.before()`, `.after()`, `htmlPrefilter`, `parseHTML`, `globalEval`, cross-domain `$.ajax`, and deep `$.extend`. Trace each input backward. Report a vulnerability only when an untrusted source reaches the affected operation without effective contextual handling.

### Mitigation sequence

1. Upgrade to at least jQuery 3.5.0, and preferably to the organization's currently supported jQuery release, in a staged environment.
2. Use jQuery Migrate temporarily to identify compatibility problems. The official upgrade guide warns that restoring the legacy HTML prefilter also restores the lost security fix [19].
3. Replace HTML-string insertion with safe text or DOM construction wherever possible.
4. If rich HTML is genuinely required, use a maintained sanitizer under a policy designed for the actual sink. jQuery's release guidance referenced DOMPurify while warning about the legacy prefilter behavior [24].
5. Add CSP only after the application is made compatible. CSP is an additional barrier, not a substitute for removing unsafe sinks; its primary role is restricting resources, especially scripts, to reduce XSS impact [35].

## Keenthemes Keen `demo1`: Fingerprint, Version Limits, and Theme Risk

The archived URL inventory contains `/keen/themes/keen/theme/demo1/dist/assets/css/pages/login/login-v1.css`, `style.bundle.css`, skin files, and JavaScript bundles alongside jQuery 1.10.2 [11]. This repeated namespace is a strong product fingerprint: vendor family `keen`, theme `keen`, demo layout `demo1`, compiled distribution `dist/assets`.

It is not an exact release fingerprint. Keenthemes has reused demo names and generated bundle names across releases, and the collected URLs expose no `package.json`, source map banner, changelog, build hash, or semantic version. The appropriate result is:

| Fingerprint question | Result | Confidence |
|---|---|---:|
| Is this a Keenthemes-style Keen asset tree? | Yes | High |
| Is the layout `demo1`? | Yes | High |
| Is it definitely Metronic rather than Keen? | No | Low |
| Can a precise Keen release be assigned? | No public version marker found | Low |
| Does NVD list a CVE for keyword `Keenthemes` or `Keen theme`? | The queried NVD API returned zero results for each keyword [36][43] | High for query result only |
| Does zero NVD result mean the theme is safe? | No; bundled dependencies and application code remain separate attack surfaces | High |

A keyword search for `Metronic` returned one NVD result, but the name collision was not established as the Keenthemes web template [39]. It should not be assigned to MUJ. This illustrates why theme-name CVE searches require vendor and product validation.

### Other sites using the same path

An exact URLScan filename query returned MUJ scan records for the Keen path [53]. The broader public search and Common Crawl work did not produce a defensible independent domain that could be named without conflating copied snippets, archived MUJ assets, or generic Keen demos. Accordingly, **no unrelated deployment is asserted**. That is a negative research result, not proof that MUJ is unique.

### Theme-level case study

The theme itself may be visually static, but its compiled bundles create dependency opacity. A scanner may label "Keen vulnerable" when the actual vulnerable component is jQuery, a validation plug-in, Bootstrap, or custom code inside `scripts.bundle.js`. Conversely, the absence of a theme CVE does not clear those embedded packages.

The corrective control is a software bill of materials generated from the deployed files. Record hashes and versions for jQuery, validation libraries, Bootstrap, icon packs, date/time widgets, and all theme plug-ins. Compare source maps or package lock files where available. Replace entire vendor bundles when upstream upgrades are provided rather than manually patching one minified function and losing provenance.

## IIS 10, HTTP/2, and TLS Profile

Microsoft documents that HTTP/2 support was introduced in IIS 10.0 [22]. IIS supports it over TLS and falls back to HTTP/1.1 when negotiation or features prevent HTTP/2 [22]. That matches SSL Labs' observation of ALPN `h2 http/1.1` on both hosts [28][29]. HTTP/2 is therefore a confirmed transport feature, not evidence of a separate reverse proxy.

### TLS comparison

| Control | MUJ | Parent | Assessment |
|---|---|---|---|
| SSL Labs grade | B [28] | B [29] | Material configuration debt |
| TLS 1.0 | Enabled [28] | Enabled [29] | Disable after dependency validation |
| TLS 1.1 | Enabled [28] | Enabled [29] | Disable |
| TLS 1.2 | Enabled [28] | Enabled [29] | Retain with modern suites |
| TLS 1.3 | Not reported | Not reported | Treat as unavailable in captured profile |
| HTTP/2 | ALPN `h2` [28] | ALPN `h2` [29] | Confirmed |
| 3DES | Offered [28] | Offered [29] | Remove |
| Static RSA suites | Offered [28] | Offered [29] | Prefer ECDHE with AEAD |
| CBC/BEAST flag | Present [28] | Present [29] | Legacy protocol/suite compatibility issue |
| HSTS | Absent [28] | Absent [29] | Add after HTTPS-only readiness |

The MUJ certificate is an Entrust DV RSA certificate for `mujslcm.jaipur.manipal.edu`; CT records show issuance on 2025-12-22 and expiry on 2026-12-21 with that single DNS name [25]. The parent SSL Labs profile instead presented a `*.manipal.edu` Sectigo OV wildcard certificate [29]. These are distinct certificate-management paths, supporting the conclusion that the two public instances are related applications but not a single identical TLS endpoint.

HSTS tells browsers to use HTTPS for future connections and prevents users from bypassing later certificate errors [52]. It does not protect the first insecure visit unless preloading or prior state exists [52]. Roll it out in stages: remove mixed content, verify every relevant subdomain, begin with a short `max-age`, increase it after monitoring, and consider `includeSubDomains` or preload only after ownership review.

IIS 10 is capable of secure operation, but its banner does not identify Windows Server edition, request-filtering customizations, application-pool identity, or installed updates. Suppress `Server`, `X-Powered-By`, `X-AspNet-Version`, and MVC version headers where operationally possible. This reduces reconnaissance value but is secondary to patching and configuration.

## Hosting, DNS, ASN, PTR, and Certificate Transparency

### Current hostname and address evidence

| Host or address | Public observation | ASN/PTR result | Defensible attribution |
|---|---|---|---|
| `mujslcm.jaipur.manipal.edu` | A = `98.70.14.50` [1] | AS8075 Microsoft; prefix `98.70.0.0/15`; no PTR [42][44][9] | Microsoft/Azure-hosted address space |
| `slcm.manipal.edu` | A = `104.211.226.160` [6] | No separate ASN lookup cited here | Public parent endpoint; SSL Labs identifies IIS 10 [29] |
| `muj.slcm.jaipur.manipal.edu` | A = `20.244.94.89` [10] | AS8075 Microsoft; `20.192.0.0/10`; no PTR [40][37] | Azure sibling endpoint |
| `52.172.36.15` | No current portal DNS relationship established | AS8075 Microsoft; `52.160.0.0/11`; no PTR [41][38] | Azure/Microsoft address, portal role unknown |
| `202.131.155.153` | No current portal DNS relationship established | AS134039 Ibus; PTR `202.131.155.153.convergentindia.com` [48][46] | Ibus/Convergent India address, portal role unknown |

### Case study: correcting the Akamai label

The supplied baseline called `98.70.14.50` an Akamai edge. Current public routing says otherwise. IPInfo identifies AS8075 Microsoft Corporation in Pune and marks the address as hosting [42]. BGP data independently places it in Microsoft's `98.70.0.0/15` route [44]. The reverse-DNS query returns NXDOMAIN under Azure-managed reverse authority rather than an Akamai hostname [9].

The bounded conclusion is not "Akamai has never been involved." CT, DNS history, an upstream WAF, or a prior CNAME could reveal a past layer. The conclusion is that **the current public IP is not demonstrated to be an Akamai-advertised edge**. Security testing and allowlisting should use current DNS and ASN evidence, not the uncorroborated label.

The sibling `20.244.94.89` is a clearer Azure signal: both the A record and AS8075 mapping agree [10][40]. CT reportedly exposed that alternate hostname, while live DNS now confirms it. Its existence should trigger an authorized control-parity review: same authentication policy, same headers, same patching, and no weaker route to the same backend.

The other two supplied IPs must remain unassigned. `52.172.36.15` is Microsoft/Azure space, but no collected DNS or certificate record tied it to these portals. `202.131.155.153` belongs to AS134039 and has a Convergent India PTR, but again no current portal relationship was established [48]. Treating either as an origin would be speculation.

### DNS ecosystem evidence

The `manipal.edu` TXT set includes SPF references to Microsoft 365 protection, Brightspace, SendGrid, and Salesforce [23]. The `jaipur.manipal.edu` TXT set includes Microsoft and Brightspace-related mail controls plus Cisco verification strings [15]. DMARC is published with `p=none` [5]. These records reveal institutional SaaS dependencies, but they do not prove that SLCM itself sends through each provider or that Cisco Webex/Brightspace code runs in the portal.

## Full Security Header Audit

The table concerns the sampled login/root responses in SSL Labs, supplemented by the supplied direct comparison. It must not be generalized to every authenticated route.

| Header/control | MUJ | Parent | Security role | Consequence of omission |
|---|---|---|---|---|
| `X-Frame-Options` | `SAMEORIGIN` [28] | Not present in captured list [29] | Blocks framing by other origins | Parent lacks this clickjacking defense on sampled response |
| `Content-Security-Policy` | Missing | Missing | Restricts scripts/resources and can block framing [35] | No application-defined browser allowlist; greater impact if injection exists |
| `X-Content-Type-Options: nosniff` | Missing | Missing | Forces declared MIME handling and prevents sniffing [49] | Browser receives no explicit anti-sniffing instruction |
| `Strict-Transport-Security` | Missing [28] | Missing [29] | Forces future HTTPS and blocks certificate-error bypass [52] | No HSTS protection against downgrade on an initial/non-HSTS visit |
| `Referrer-Policy` | Missing | Missing | Controls how much referrer data accompanies requests [50] | Browser default `strict-origin-when-cross-origin` applies rather than an explicit portal policy [50] |
| `Permissions-Policy` | Missing | Missing | Allows/denies browser features in documents and iframes [51] | No portal-specific feature restriction; directive defaults apply [51] |
| `Cross-Origin-Opener-Policy` | Missing | Missing | Can isolate top-level browsing-context groups and sever opener references [45] | No explicit opener/process isolation |
| Anti-forgery cookie flags | HttpOnly; `Secure` not shown [28] | N/A in cited response | Protects token cookie from script access and transport misuse | Confirm `Secure` and appropriate SameSite behavior directly |
| Session cookie flags | N/A in cited MUJ response | HttpOnly, SameSite=Lax; `Secure` not shown [29] | Limits script access and some cross-site sending | Confirm `Secure`, scope, expiry, and rotation |

### Case study: same family, different frame defense

MUJ's `SAMEORIGIN` header is consistent with Microsoft's recommendation for protecting the anti-forgery-enabled page from clickjacking [21]. The parent response lacks it. This divergence matters because anti-CSRF tokens do not prevent a user from being visually tricked into interacting with a framed page.

The preferred modernization is a CSP `frame-ancestors` directive, optionally retaining X-Frame-Options for older clients. Begin in report-only mode for script/style directives because legacy Keen bundles and inline code may otherwise break. The objective is not merely a scanner-green header set; it is a policy that the application can enforce without unsafe wildcards or broad `unsafe-inline` exceptions.

## Backend Evidence, Error Pages, Routes, and Cookies

Public and archived material supports a coherent MVC model. The MUJ root and `/Home/Index` both expose the same welcome/sign-in surface [2][4]. The archive captured both routes and their common Keen assets [11]. A redirect to `/Home/Index` after authentication follows the familiar controller/action URL shape, although route tables can be customized and the path alone does not prove the default route.

The anti-forgery evidence is particularly specific. ASP.NET's implementation uses unpredictable token material, binds authenticated identity information where available, and protects token payloads cryptographically [21]. Missing, unreadable, swapped, security-token-mismatched, or username-mismatched pairs cause failure [21]. Thus, the observed YSOD confirms an exception path around anti-forgery validation but does not demonstrate bypass.

The parent sets `ASP.NET_SessionId` with HttpOnly and SameSite=Lax in the sampled SSL Labs response [29]. This proves the classic session-state module issued a cookie. It does not show whether that identifier survives authentication, whether an independent forms-authentication cookie is used, or whether session state contains authorization data.

No indexed YSOD corpus or cached stack trace was found that could be safely attributed beyond the supplied reproducible error observation. That negative result does not negate the direct finding. It means the report should not invent controller names, filesystem paths, database providers, or source-code line numbers that were not captured.

## Authorized Defensive Test Plan

The following priorities are based on the observed stack. They are not claims that each vulnerability exists.

| Priority | Test class | Why it fits this stack | Safe acceptance criterion |
|---:|---|---|---|
| 1 | DOM XSS and prototype pollution | jQuery 1.10.2 falls in all four requested affected ranges | No untrusted source reaches affected Ajax, deep-merge, or HTML sinks |
| 2 | Error handling | Missing anti-forgery token produced detailed YSOD | Remote failures return generic pages and correlation IDs only |
| 3 | Anti-forgery semantics | Cookie plus hidden token and MVC validator are present | Tokens are required, pair-bound, identity-bound where applicable, and unusable cross-session |
| 4 | Session fixation and transition | Parent issues `ASP.NET_SessionId` | Session/auth identifiers rotate on login and privilege changes |
| 5 | IIS path normalization and traversal resistance | IIS 10 origin with legacy application routes | Front end and origin reject equivalent malformed/canonicalized paths consistently |
| 6 | Header and framing controls | Parent lacks XFO; both lack CSP/HSTS | CSP/frame policy blocks unauthorized framing; HTTPS policy is consistent |
| 7 | TLS hardening | TLS 1.0/1.1, 3DES, CBC/static RSA remain | Only approved protocol versions and forward-secret AEAD suites remain |
| 8 | ViewState/machineKey, conditional | Classic ASP.NET may coexist with WebForms remnants | Test only endpoints that emit `__VIEWSTATE`, forms-auth, or other machineKey-protected artifacts |
| 9 | Alternate-host parity | Sibling Azure hostname is live | All public names enforce the same authentication, headers, routing, and patch policy |

### Anti-forgery and authentication

Test token omission, cookie/form swapping, cross-session replay, pre-login versus post-login use, duplicate fields, content-type changes, and authenticated identity changes. Do not equate a 500 response with bypass; success means an unauthorized state change. ASP.NET documents the two-token pattern and mismatch conditions [21]. Correct the error handler even if every bypass test fails.

Review the supplied hidden `EmailFor` and `LoginFor` fields as client-controlled selectors. Verify that changing them cannot select a privileged authentication flow, redirect target, tenant, role, or password-reset context without server-side authorization. Their presence alone is not a vulnerability.

### Session fixation

OWASP defines fixation/capture of a session identifier as a route to session hijacking and requires regeneration after authentication or any privilege change [57]. Capture an anonymous session, authenticate using the same browser, and verify that both session and authentication identifiers change as designed. Repeat across parent-login and ordinary-login paths. Cookie presence before login is normal; failure to rotate at the trust transition is the meaningful finding.

Also verify `Secure`, HttpOnly, SameSite, domain/path scope, expiry, logout invalidation, idle timeout, absolute timeout, parallel-session policy, and cache controls. The parent already shows HttpOnly and SameSite=Lax [29], but `Secure` was not visible in that captured header.

### ViewState and machineKey

Do not launch a generic ViewState finding against an MVC page that emits no `__VIEWSTATE`. If WebForms endpoints are discovered, determine whether they emit ViewState and event-validation fields. Microsoft states that beginning with ASP.NET 4.5.2, ViewState is protected with encryption and a MAC, with earlier versions brought under the stronger behavior through KB2905247 [56].

MachineKey becomes relevant because it supplies cryptographic protection for ViewState and forms authentication. Microsoft notes that `DecryptionKey` is used for forms authentication and for ViewState under AES/3DES configurations, and that a web farm needs consistent manually configured keys [54]. The authorized review should look for weak, disclosed, reused, or inconsistent keys in configuration management, not attempt to infer a key from a banner.

### IIS path traversal and front-door consistency

IIS request filtering can reject double-encoded requests with 404.11, hidden segments with 404.8, blocked extensions with 404.7, disallowed verbs with 404.6, and oversized URLs/query strings with 404.14/404.15 [55]. Verify that the public endpoint and any authorized origin test path normalize URLs identically. Focus on canonicalization, encoded separators, dot segments, alternate data representations, verb handling, and static-file boundaries without attempting destructive file access.

Because current evidence points to Microsoft/Azure rather than Akamai, describe this as a **front-door/origin parity test**, not an "Akamai bypass" test. First establish the actual Azure service, load balancer, WAF, or direct-IIS topology from owner records.

## Synthesis

The two portals share an IIS/System.Web foundation but diverge in application and security details. MUJ exposes an MVC 5.3 banner, anti-forgery token, Keen demo1 assets, and `SAMEORIGIN`. The parent exposes a classic ASP.NET session cookie and lacks the captured framing header. Both negotiate HTTP/2, retain legacy TLS protocols and suites, omit HSTS, and receive B grades [28][29]. This is not one uniform endpoint; it is a family that needs per-host control validation.

Across the evidence, the strongest vulnerability lead is not the .NET build string. It is the exact jQuery 1.10.2 asset. The four CVE ranges clearly include that release, and one is in CISA's KEV catalog. Yet even here, the application must expose the relevant sink. The correct mechanism-driven conclusion is "high-priority reachable-code review," not "confirmed XSS."

The inverse applies to the YSOD. Detailed remote disclosure is already demonstrated, but the trigger also indicates that anti-forgery validation rejected a missing token. One control worked while another failed. That tension is strategically important: remediation should preserve token enforcement while replacing remote diagnostic output with a generic error and protected telemetry.

Infrastructure attribution produced the largest correction to the supplied baseline. `98.70.14.50`, `20.244.94.89`, and `52.172.36.15` are currently in AS8075 Microsoft routes, while `202.131.155.153` belongs to AS134039 Ibus [44][37][38][46]. Only the first two have an established current hostname relationship in the collected data. Calling the MUJ IP an Akamai edge or the other addresses portal origins would exceed the evidence.

The broader pattern is legacy compatibility debt: jQuery 1.10.2, MVC 5.3, detailed System.Web errors, TLS 1.0/1.1, 3DES/static RSA, and absent browser policies. None alone proves compromise. Together they justify a modernization program ordered by reachable risk: eliminate detailed errors, upgrade jQuery and its bundles, close unsafe DOM flows, establish exact Windows/.NET patch state, rotate session identifiers correctly, normalize header policy across every hostname, and then harden TLS.

## VERDICT

**Overall verdict: A well-supported legacy ASP.NET MVC/IIS deployment with material hardening gaps, one clearly obsolete client library, and an unproven runtime patch level. No server-side remote-code-execution, CSRF bypass, session fixation, ViewState exploit, path traversal, or successful MUJ-specific XSS was demonstrated by the public evidence.**

| Finding | Verdict | Confidence |
|---|---|---:|
| IIS 10.0, ASP.NET MVC 5.3, .NET Framework/System.Web 4.x | Confirmed | **High** |
| Exact .NET KB or vulnerability patch state from `4.7.4136.0` | Not publicly determinable | **High** confidence in limitation |
| jQuery 1.10.2 present and within four requested CVE ranges | Confirmed | **High** |
| MUJ-specific exploitability of those jQuery CVEs | Not demonstrated; requires sink analysis | **High** |
| Keenthemes Keen demo1 product fingerprint | Confirmed | **High** |
| Exact Keen/Metronic release | Unknown | **High** confidence in limitation |
| HTTP/2 and B-grade legacy TLS configuration | Confirmed | **High** |
| Current MUJ address is Microsoft/Azure AS8075 | Confirmed | **High** |
| Current MUJ address is an Akamai edge | Not supported and contradicted by current ASN evidence | **High** |
| Header omissions on sampled public responses | Confirmed | **High** |
| Detailed remote error disclosure | Confirmed by supplied hands-on observation | **High** |
| Anti-forgery bypass | Not demonstrated; observed failure is consistent with enforcement | **High** |
| Parent session fixation | Not demonstrated | **High** |
| WebForms/ViewState remnants | Unknown; conditional testing only | **Medium** |

**Final confidence: High for stack, asset, TLS, DNS, ASN, certificate, and sampled-header findings; medium for architecture inferences; low for any exact patch, hidden origin, or exploitability claim that requires authenticated or server-side access.**

## References

1. *dns.google*. https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=A
2. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
3. [
	MU SLcM
](https://slcm.manipal.edu/)
4. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
5. *dns.google*. https://dns.google/resolve?name=_dmarc.manipal.edu&type=TXT
6. *dns.google*. https://dns.google/resolve?name=slcm.manipal.edu&type=A
7. *dns.google*. https://dns.google/resolve?name=153.155.131.202.in-addr.arpa&type=PTR
8. *NVD - CVE-2020-11022*. https://nvd.nist.gov/vuln/detail/CVE-2020-11022
9. *dns.google*. https://dns.google/resolve?name=50.14.70.98.in-addr.arpa&type=PTR
10. *dns.google*. https://dns.google/resolve?name=muj.slcm.jaipur.manipal.edu&type=A
11. *web.archive.org*. http://web.archive.org/cdx/search/cdx?collapse=urlkey&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&output=json&url=mujslcm.jaipur.manipal.edu/*
12. *dns.google*. https://dns.google/resolve?name=89.94.244.20.in-addr.arpa&type=PTR
13. *NVD - CVE-2019-11358*. https://nvd.nist.gov/vuln/detail/CVE-2019-11358
14. *Manipal University*. https://muj.slcm.jaipur.manipal.edu/
15. *dns.google*. https://dns.google/resolve?name=jaipur.manipal.edu&type=TXT
16. *NVD - CVE-2015-9251*. https://nvd.nist.gov/vuln/detail/CVE-2015-9251
17. *.NET Framework official support policy | .NET*. https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-framework
18. *Determine which .NET Framework versions are installed - .NET Framework | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/framework/migration-guide/how-to-determine-which-versions-are-installed
19. *jQuery Core 3.5 Upgrade Guide | jQuery*. https://jquery.com/upgrade-guide/3.5/
20. *NVD - CVE-2020-11023*. https://nvd.nist.gov/vuln/detail/CVE-2020-11023
21. *XSRF/CSRF Prevention in ASP.NET MVC and Web Pages | Microsoft Learn*. https://learn.microsoft.com/en-us/aspnet/mvc/overview/security/xsrfcsrf-prevention-in-aspnet-mvc-and-web-pages
22. *HTTP/2 on IIS | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/get-started/whats-new-in-iis-10/http2-on-iis
23. *dns.google*. https://dns.google/resolve?name=manipal.edu&type=TXT
24. *jQuery 3.5.0 Released! | Official jQuery Blog*. https://blog.jquery.com/2020/04/10/jquery-3-5-0-released/
25. *crt.sh*. https://crt.sh/?q=mujslcm.jaipur.manipal.edu&output=json
26. *jQuery 3.4.0 Released | Official jQuery Blog*. https://blog.jquery.com/2019/04/10/jquery-3-4-0-released/
27. *crt.sh*. https://crt.sh/?q=slcm.manipal.edu&output=json
28. *api.ssllabs.com*. https://api.ssllabs.com/api/v3/analyze?host=mujslcm.jaipur.manipal.edu&publish=off&all=done&fromCache=on
29. *api.ssllabs.com*. https://api.ssllabs.com/api/v3/analyze?host=slcm.manipal.edu&publish=off&all=done&fromCache=on
30. *CVE Record: CVE-2021-26701*. https://www.cve.org/CVERecord?id=CVE-2021-26701
31. *CVE Record: CVE-2020-1147*. https://www.cve.org/CVERecord?id=CVE-2020-1147
32. *CVE Record: CVE-2019-0820*. https://www.cve.org/CVERecord?id=CVE-2019-0820
33. *CVE Record: CVE-2017-8759*. https://www.cve.org/CVERecord?id=CVE-2017-8759
34. *CVE Record: CVE-2023-36560*. https://www.cve.org/CVERecord?id=CVE-2023-36560
35. *Content Security Policy (CSP) - HTTP | MDN*. https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP
36. *services.nvd.nist.gov*. https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=Keenthemes
37. *20.244.94.89 - bgp.he.net*. https://bgp.he.net/ip/20.244.94.89
38. *52.172.36.15 - bgp.he.net*. https://bgp.he.net/ip/52.172.36.15
39. *services.nvd.nist.gov*. https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=Metronic
40. *20.244.94.89 | Pune, AS8075, VPN Not Detected | IPinfo*. https://ipinfo.io/20.244.94.89
41. *52.172.36.15 | Chennai, AS8075, VPN Not Detected | IPinfo*. https://ipinfo.io/52.172.36.15
42. *98.70.14.50 | Pune, AS8075, VPN Not Detected | IPinfo*. https://ipinfo.io/98.70.14.50
43. *services.nvd.nist.gov*. https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=Keen%20theme
44. *98.70.14.50 - bgp.he.net*. https://bgp.he.net/ip/98.70.14.50
45. *Cross-Origin-Opener-Policy (COOP) header - HTTP | MDN*. https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Opener-Policy
46. *202.131.155.153 - bgp.he.net*. https://bgp.he.net/ip/202.131.155.153
47. *HTTP Headers - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html
48. *202.131.155.153 | Delhi, AS134039, VPN Not Detected | IPinfo*. https://ipinfo.io/202.131.155.153
49. *X-Content-Type-Options header - HTTP | MDN*. https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Content-Type-Options
50. *Referrer-Policy header - HTTP | MDN*. https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Referrer-Policy
51. *Permissions-Policy header - HTTP | MDN*. https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Permissions-Policy
52. *Strict-Transport-Security header - HTTP | MDN*. https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security
53. *urlscan.io*. https://urlscan.io/api/v1/search/?q=filename%3A%22keen%2Fthemes%2Fkeen%2Ftheme%2Fdemo1%2Fdist%2Fassets%2Fcss%2Fpages%2Flogin%2Flogin-v1.css%22
54. *MachineKeySection.DecryptionKey Property (System.Web.Configuration) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.configuration.machinekeysection.decryptionkey?view=netframework-4.8.1
55. *Use Request Filtering | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/manage/configuring-security/use-request-filtering
56. *Secure ASP.NET ViewState - .NET Blog*. https://devblogs.microsoft.com/dotnet/secure-asp-net-viewstate
57. *Session Management - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
58. *CISA Adds One Known Exploited Vulnerability to Catalog | CISA*. https://www.cisa.gov/news-events/alerts/2025/01/23/cisa-adds-one-known-exploited-vulnerability-catalog
59. *CVE-2020-11023 Detail - NVD*. https://nvd.nist.gov/vuln/detail/cve-2020-11023
