# What Keen Demo1 Paths Reveal About MUJ SLCM

## Executive Summary

- **Confirmed Theme Lineage**: The public MUJ login identifies itself as the "MUJ PORTAL," while archived public asset records show the explicit directory `/keen/themes/keen/theme/demo1/dist/` and files such as `login-v1.css` and `style.bundle.css` [7][5]. This is strong evidence that the login front end derives from KeenThemes' Keen product and its `demo1` layout. It is not merely a generic Bootstrap resemblance.

- **Version Remains Unknown**: Neither the visible MUJ page nor the archived URL inventory contains a Keen release number [7][5]. **Inference:** the nested `theme/demo1/dist/assets` layout and `login-v1.css` look like a legacy Keen distribution rather than the current Bootstrap 5 preview, but they cannot establish an exact major, minor, or patch version. The club should record the version as **"Keen, legacy generation, exact release unverified"**, not as a guessed v1.x number.

- **Two High-Confidence Education Comparators**: The public Netkampuss ERP page for Annai Velankanni Matriculation School identifies itself as an online school, college, and university ERP [17]. Its page source contains `kt_body`, `kt_login`, Metronic-style bundles, and a `HOST_URL` pointing to `keenthemes.com/metronic/tools/preview`. The Avenu Learning LMS India login identifies the service by name [18] and exposes the same KT naming family plus canonical `plugins.bundle`, `style.bundle`, `scripts.bundle`, and `login-4.css` paths. **Inference:** both are high-confidence Metronic-family deployments, but neither discloses an exact release.

- **No Confirmed Indian Government Deployment**: This review did not find sufficient public evidence to label a `gov.in` portal as Keen or Metronic. A generic filename such as `style.bundle.css` is not distinctive, and a page styled as a government department is not equivalent to an official Indian government domain. The defensible result is "none confirmed in this evidence set," not "none exist."

- **No Proven Theme-JavaScript XSS**: Open Bug Bounty report OBB-4445862 names `preview.keenthemes.com`, CWE-79 XSS, and an "unpatched" status when reviewed, but classifies the component as **Custom Code** rather than distributed Keen or Metronic JavaScript [4]. It is evidence of a vendor preview-host application issue, not evidence that every customer installation inherits an XSS flaw.

- **Dependency Risk Is Conditional**: Historical dashboard bundles often contain third-party libraries, but a CVE applies only after the deployed version is established. Bootstrap before 3.4.1 and Bootstrap 4.3.x before 4.3.1 are affected by CVE-2019-8331 [11]. jQuery releases before 3.5.0 are affected by CVE-2020-11022 and CVE-2020-11023 under specified unsafe DOM-manipulation conditions [13][10]. These records justify an authorized software-composition review; they do **not** prove that MUJ is vulnerable.

- **Demo1 Is a Layout Identifier, Not a Version**: KeenThemes describes Metronic demos as distinct templates designed for real-world applications [16]. Therefore, `demo1` most directly identifies a selected layout or build target. It does not, by itself, mean "version 1," a development environment, a default account, an exposed administrative panel, or an authentication bypass.

- **Best Defensive Action**: Under university authorization, identify exact JavaScript and CSS component versions from source manifests, package lockfiles, source-map metadata, vendor banners, or an internally generated software bill of materials. OWASP Dependency-Check is specifically intended to identify known vulnerable dependent libraries [15]. Remediate verified component findings, remove unused sample material, and avoid treating a directory-name fingerprint as an exploitable weakness.

## Scope, Safety, and Evidence Standard

This report uses public login pages, public static-resource references, search-index records, official KeenThemes documentation, the official Metronic changelog, Open Bug Bounty, OWASP, and NIST's National Vulnerability Database. It does not authenticate to any portal, submit test payloads, enumerate accounts, attempt password recovery, bypass access controls, or test undocumented routes. OWASP describes its Web Security Testing Guide as a resource for developers and security professionals, but live testing still requires the asset owner's authorization [19].

The technical baseline supplied by the club says that `mujslcm.jaipur.manipal.edu` uses ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10 behind Akamai, and Microsoft 365 identity. Those values are treated here as **scope inputs**, not as independently revalidated findings. The visible page shows the MUJ portal and an `@muj.manipal.edu` sign-in cue [6], but that cue alone does not prove the identity provider, tenant configuration, federation protocol, or Microsoft 365 security posture. Likewise, a `/Home/Index` route is compatible with ASP.NET MVC conventions but does not prove a framework version.

The report uses four evidence levels:

| Evidence level | Meaning | Appropriate wording |
|---|---|---|
| Confirmed | Explicit product/path statement in a first-party page, public markup, archive, or official documentation | "Uses Keen demo1 assets" |
| High-confidence inference | Several distinctive, mutually reinforcing fingerprints, but no version banner | "Metronic-family implementation; exact release unknown" |
| Conditional risk | A CVE exists, but the target's affected component/version is not established | "Potentially relevant if the bundled version falls in the affected range" |
| Unconfirmed or excluded | Only a generic filename, visual resemblance, or organization label is present | "Insufficient evidence" |

This evidence ladder is the report's substitute for the requested private chain-of-thought. It gives the reproducible basis for each conclusion without exposing hidden internal reasoning or encouraging unauthorized testing. Every inference is labeled as such.

## MUJ SLCM Baseline: Confirmed Keen Lineage, Unknown Release

MAHE's own ICT documentation describes Student Life Cycle Management, or SLCM, as the replacement for an older Academic Management System. It says SLCM includes attendance, internal marks, external marks, result publication, and broadcast-message modules, and serves as a single window for student and parent academic matters [20]. The public MUJ endpoint presents "WELCOME TO MUJ PORTAL" and separate sign-in and parent-login text [7]. These sources establish that the page is an academic lifecycle portal, not merely a generic theme demonstration.

The strongest theme evidence is the literal public resource hierarchy recorded for MUJ. The archive lists the login endpoint and resources under:

`/keen/themes/keen/theme/demo1/dist/assets/`

The indexed files include `css/pages/login/login-v1.css`, `css/style.bundle.css`, global plugin bundles, layout skins, and fonts [5]. The product name occurs twice in the path, while `demo1` occupies the same semantic position used for a selected demo/build in KeenThemes products. This is much stronger attribution than a color palette, Poppins font, `style.bundle.css`, or a KT-prefixed DOM identifier in isolation.

| MUJ observation | Direct implication | What it does not prove |
|---|---|---|
| `/keen/themes/keen/theme/` | Strong Keen product-line attribution | Exact Keen release |
| `/demo1/dist/` | Assets were built from the demo1 layout target | "Version 1" or development status |
| `login-v1.css` | A packaged login-page variant is used | A first product release |
| `plugins.bundle.css` and `style.bundle.css` | The deployment uses compiled global/vendor and theme bundles | Which libraries and versions are inside them |
| Layout skin files | The application retains vendor-style skin separation | That unused demo pages remain reachable |

The **version finding is intentionally negative**: no exact version is publicly established. The current official Keen preview describes Keen as a multi-demo Bootstrap 5 admin template [3]. MUJ's deeper legacy-looking hierarchy differs from current flat distribution conventions, but directory evolution is not a reliable version oracle. Developers may copy folders forward, rename roots, preserve old paths after upgrades, or selectively replace bundle contents.

**Inference, moderate confidence:** MUJ probably integrated a legacy Keen distribution and retained much of its original output structure. The evidence does not justify publishing "Keen v1.4.x," "Bootstrap 4," or any patch number. A precise answer requires an authorized view of a source manifest, package lockfile, build metadata, source-map comment, or vendor banner. Guessing the release would create false CVE matches and potentially waste remediation effort.

The supplied server-side and identity technologies should be assessed separately from the theme. A front-end theme does not determine whether MVC anti-forgery controls, session cookies, Microsoft identity flows, IIS headers, or Akamai edge rules are secure. Theme attribution narrows front-end inventory work; it does not answer server-side security questions.

## Keen and Metronic Lineage: Similar Conventions, Different Products

Keen and Metronic are separate KeenThemes products. The official Keen preview names the product "Keen" and presents a `demo1` preview [3]. The official Metronic site likewise presents its own documentation and demo collection [2]. Shared naming such as `demo1`, `plugins.bundle`, `style.bundle`, `scripts.bundle`, `KTAppSettings`, and `kt_login` reflects a common vendor engineering vocabulary. It does not make the products interchangeable.

KeenThemes explains that Metronic offers a collection of unique demos, each representing a distinct template for real-world applications [16]. The correct interpretation is therefore:

| Token or path element | Most defensible meaning | Confidence |
|---|---|---|
| `keen` in a vendor directory | Keen product attribution | High |
| `metronic` in a vendor URL or banner | Metronic product attribution | High |
| `demo1` | Selected demo/layout/build target | High |
| `dist` | Compiled distribution output | High |
| `assets/css/style.bundle.css` | Compiled theme stylesheet | Medium; not product-specific alone |
| `assets/plugins/global/plugins.bundle.js` | Aggregated third-party/global JavaScript | Medium; contents and versions unknown |
| `kt_` DOM IDs or KT globals | KeenThemes-family convention | Medium to high when combined with other signals |
| `login-v1.css` or `login-4.css` | Packaged page-layout variant | Medium; not a product version number |

Version attribution is harder because theme customers frequently customize builds. A path associated with one vendor release can survive several application upgrades, while the bundle contents may be replaced independently. Conversely, a modern-looking bundle name can wrap an old dependency. The official Metronic changelog illustrates continued change across product generations: it lists Metronic v8.3.2 with Bootstrap 5.3.8 and v8.3.3 with Gulp, Axios, and npm security-related updates [1]. That chronology cannot be back-applied to MUJ without a version bridge.

The practical framework is **product fingerprint -> generation estimate -> exact component inventory**. Product fingerprinting uses explicit vendor directories and URLs. A generation estimate uses several independent layout and component conventions and must be labeled as inference. Exact component inventory requires manifests or direct version evidence. Skipping the last step and matching every CVE associated with Bootstrap or jQuery is an example of the base-rate fallacy: common libraries appear in many products, but only specific affected releases and code paths are vulnerable.

## Other Public Portal Case Studies

### Netkampuss ERP: Strong Metronic Attribution, Version Not Disclosed

The public `sch-avms.netkampus.in` page describes Netkampuss as an online school, college, and university ERP and names Annai Velankanni Matriculation School [17]. Its public page source contains the mutually reinforcing signals `kt_body`, `kt_login`, `KTAppSettings`, `plugins.bundle`, `scripts.bundle`, `login-1.css`, and a `HOST_URL` that points to `https://keenthemes.com/metronic/tools/preview`.

**Inference, high confidence:** this is a customized Metronic-family front end. The explicit vendor preview URL distinguishes it from applications that merely use Bootstrap or a generic `style.bundle.css`. However, no public release banner or package manifest establishes the exact Metronic version. The safest version field is **"unknown; legacy Bootstrap-generation Metronic family"**. Even the phrase "legacy Bootstrap-generation" is an inference from its component and layout conventions, not a patch-level claim.

The case shows why a portal inventory should preserve evidence granularity. Netkampuss is useful as a peer architecture example because it combines an education ERP purpose with a KeenThemes-family interface. It is not evidence that Netkampuss and MUJ share backend code, authentication, hosting, ownership, or vulnerabilities. One uses a Metronic fingerprint while MUJ has an explicit Keen directory.

### Avenu Learning LMS India: Strong KT/Metronic Family, Ambiguous Generation

The second comparator is `learn-india.avenulearning.com`, whose public page calls itself "Avenu Learning LMS India" [18]. The organization's public site describes Avenu Learning as an education partner connecting universities with learners and expanding access to online education [21]. Its login source contains `/assets/css/pages/login/login-4.css`, `/assets/plugins/global/plugins.bundle.css`, `/assets/css/style.bundle.css`, `/assets/js/scripts.bundle.js`, `KTAppSettings`, and `kt_login`.

**Inference, high confidence:** the combined KT globals, packaged login variant, and canonical KeenThemes bundle layout indicate a Metronic-family implementation. **Version:** not publicly disclosed. The path is consistent with historical Bootstrap-based Metronic builds, but it is unsafe to assign v7 or v8 without a manifest or banner because these conventions span releases and are often copied into custom applications.

The Avenu case is a useful contrast with MUJ. MUJ contains an explicit `keen/themes/keen/theme/demo1` namespace, making the product attribution direct. Avenu lacks a literal `metronic` directory in the observed asset paths, so its conclusion depends on a cluster of vendor-specific conventions. The confidence remains high at the family level but lower at the exact product/version level.

### Assam University and Government-Styled Pages: Why False Positives Matter

The public Assam University examination page identifies itself as "Assam University, Silchar" [22]. Its markup contains `assets/css/style.bundle.css`, but that filename is generic and is used by many build systems. No explicit Keen, Metronic, `demo1`, or KT product signal was established in the reviewed evidence. It is therefore **excluded from the confirmed list**.

Likewise, a public page titled "LFMEAB :: Login" contains Department of Environment text [23], but its host is not a `gov.in` domain and the observed bundles do not establish Keen or Metronic. Organization wording, a government-looking logo, or a bundle filename cannot substitute for an official-domain and product-fingerprint chain.

| Portal | Sector | Public evidence | Product assessment | Version assessment |
|---|---|---|---|---|
| MUJ SLCM | Indian higher education | Explicit `/keen/themes/keen/theme/demo1/dist/` paths [5] | **Confirmed Keen** | Exact release unknown |
| Netkampuss school ERP | Indian education ERP | KT globals, Metronic preview URL, canonical bundle layout; page identity [17] | **High-confidence Metronic-family inference** | Unknown |
| Avenu Learning LMS India | Education LMS | KT globals and canonical login/bundle paths; page identity [18] | **High-confidence Metronic-family inference** | Unknown |
| Assam University examination | Indian higher education | Generic `style.bundle.css`; page identity [22] | **Unconfirmed; excluded** | Not applicable |
| LFMEAB login | Government-styled portal, jurisdiction not established here | Department text and generic bundles [23] | **Unconfirmed; excluded** | Not applicable |
| Indian `gov.in` portals | Indian government | No sufficiently distinctive public result in this review | **None confirmed** | Not applicable |

The decision-ready result is a short, evidence-tiered list rather than a long but unreliable catalog. Additional portals may exist, but public attribution should require an explicit vendor path/banner or a distinctive cluster of KT components plus canonical bundles.

## Public Vulnerabilities: Separate Theme Code, Demo-Host Code, and Dependencies

### Case Study: OBB-4445862 Is Not a Universal Theme XSS

Open Bug Bounty report OBB-4445862 names `preview.keenthemes.com` and records CWE-79 cross-site scripting [4]. It gives a reported time of January 12, 2026, and the page showed an "unpatched" status when reviewed [4]. This is directly relevant because the affected host belongs to the same vendor's preview ecosystem.

The limiting fact is equally important: the report labels the component **Custom Code** and does not attribute the defect to a distributed Keen or Metronic JavaScript file [4]. No public parameter or reusable theme component is identified in the cited report [4]. Therefore, the report supports "a public XSS report affected the vendor preview host," not "Keen demo1 contains an inherited XSS" and not "MUJ is vulnerable."

This distinction is the core application-security lesson. A demonstration site combines theme assets, preview routing, server code, sample data, and vendor-specific custom logic. A defect in any one layer can affect the preview host without being shipped to customers. Before treating a vendor-site report as a supply-chain vulnerability, an analyst needs the vulnerable file/function, affected release range, and evidence that the code is included in customer distributions.

### Conditional Dependency CVEs

The following records are authoritative vulnerability examples for common historical front-end dependencies. They are included as **conditional checks**, not MUJ findings.

| Record | Affected versions and mechanism | Relevance to MUJ or peers | Status in this report |
|---|---|---|---|
| CVE-2019-8331 | Bootstrap before 3.4.1 and Bootstrap 4.3.x before 4.3.1; XSS through tooltip or popover `data-template` [11] | Relevant only if an affected Bootstrap version and feature are actually bundled | Conditional, unverified |
| CVE-2020-11022 | jQuery 1.12.0 through versions before 3.5.0; unsafe DOM manipulation of untrusted HTML may execute code; patched in 3.5.0 [10] | Relevant only if affected jQuery is present and application data reaches the unsafe sink | Conditional, unverified |
| CVE-2020-11023 | jQuery 1.0.3 through versions before 3.5.0; untrusted HTML containing `option` elements may execute through DOM-manipulation methods; patched in 3.5.0 [13] | Same version-and-data-flow requirement | Conditional, unverified |
| CVE-2019-11358 | jQuery before 3.4.0; deep `extend` operations can lead to `Object.prototype` pollution when given an unsanitized object [12] | Relevant only if the affected release and unsafe object flow exist | Conditional, unverified |
| OBB-4445862 | XSS on `preview.keenthemes.com`, classified as Custom Code [4] | Vendor preview-host issue; no proven theme-package inheritance | Public report, not a target finding |

The Metronic changelog reinforces the dependency distinction. Metronic v9.4.12 says it resolved npm security vulnerabilities by updating `minimatch` and `flatted` [1]. Metronic v9.4.5 records security vulnerability fixes and dependency overrides [1]. Metronic v8.3.3 says npm security vulnerabilities were addressed with dependency cleanup [1]. The changelog does not identify a distributed Keen/Metronic theme XSS or a CVE that can be mapped to MUJ from its `demo1` path alone.

A vulnerable library also does not automatically mean an exploitable application. Exploitability depends on the exact release, whether the vulnerable module is included in the production bundle, whether the vulnerable feature is invoked, whether untrusted data reaches the relevant sink, and what browser-side controls constrain impact. Conversely, minification or bundling does not remove a vulnerable code path. That is why version inventory and data-flow review must precede a finding.

## What `demo1` Asset Paths Actually Imply

The most defensible semantic interpretation comes from KeenThemes' own description: demos are distinct templates or layouts [16]. In a build-oriented theme, the developer selects a demo, compiles its Sass/JavaScript and vendor packages, and deploys the output under a distribution directory. A retained `demo1` segment records that lineage.

| Possible inference from `demo1` | Assessment | Reason |
|---|---|---|
| The front end derives from a KeenThemes demo/layout | Supported when combined with explicit `keen` or `metronic` evidence | Vendor documentation treats demos as distinct templates [16] |
| The selected layout was demo 1 | Supported | `demo1` is the build/layout selector in the path |
| The application uses product version 1 | **Not supported** | Demo numbers and release numbers are separate concepts |
| The host is a development or staging environment | **Not supported** | Production deployments often retain vendor directory names |
| A `/demo1` application route exists | **Not supported** | An asset directory does not imply a routable controller/page |
| Default credentials exist | **Not supported** | No relationship follows from the directory name |
| Authentication can be bypassed | **Not supported** | Static path disclosure says nothing about server authorization |
| Other sample pages may have been copied | Plausible but unverified inference | Theme packages include multiple components, but deployment contents vary |
| The path aids passive fingerprinting | Supported | It exposes vendor and layout taxonomy in a public URL |
| The theme is vulnerable | **Not supported without version and affected code** | CVEs have explicit product/version/mechanism requirements |

An exposed demo path is therefore primarily an **information-disclosure and asset-governance clue**, not a vulnerability by itself. Its defensive value is that it helps an authorized team find the owning build, compare deployed files with the licensed source package, and identify unnecessary sample assets. The security impact rises only if deployed sample material introduces real behavior, sensitive data, unsafe server endpoints, source maps containing proprietary source, or outdated executable dependencies.

MUJ's path is particularly informative because it includes the product name, selected demo, distribution directory, and asset class in one URL. That allows high-confidence lineage attribution. It still does not establish which optional pages exist. This report deliberately did not request guessed demo pages or test whether unlinked routes were reachable.

The path also reveals a maintenance risk: copied vendor trees can become "orphaned assets" whose original package manager and update process are lost. **Inference:** if MUJ's theme was integrated as a static folder rather than maintained through a repeatable build, dependency ownership may be unclear. That is an asset-management concern to verify internally, not evidence of negligence or compromise.

## Defensive Validation Plan for the University Club

The appropriate next step is an authorized inventory exercise, not Internet-side exploitation. OWASP Dependency-Check was created to identify known vulnerable application dependencies [15]. OWASP ASVS provides a basis for testing technical security controls and secure-development requirements [14]. These frameworks support a controlled process that separates component discovery from vulnerability confirmation.

| Priority | Authorized action | Expected evidence | Decision produced |
|---|---|---|---|
| 1 | Ask the application owner for the licensed Keen package version, source repository tag, build job, `package.json`, and lockfile | Exact theme and dependency versions | Resolves the largest uncertainty |
| 2 | Generate an internal SBOM or software-composition report for the deployed front-end build | Component names, versions, hashes, dependency paths | Maps only applicable CVEs |
| 3 | Compare deployed static-file hashes with the organization's approved build artifacts | Drift, local modifications, stale bundles | Distinguishes vendor code from custom code |
| 4 | Inventory intentionally deployed sample pages and source maps | Approved route and file list | Removes unnecessary material without speculative scanning |
| 5 | Review custom code that writes URL, message, profile, or server data into the DOM | Sources, transforms, and HTML/DOM sinks | Determines whether XSS conditions exist |
| 6 | Validate CSP, cookie, anti-forgery, login throttling, and identity configuration under written authorization | Control-specific test results | Covers risks the theme fingerprint cannot answer |
| 7 | Establish ownership and update cadence | Named owner, support entitlement, patch SLA | Prevents orphaned vendor assets |

The team should not claim a CVE match from a minified filename or visual design. If an authorized source review finds jQuery before 3.5.0, the next question is whether untrusted HTML reaches the DOM methods described in CVE-2020-11022 or CVE-2020-11023 [13][10]. If Bootstrap falls in the CVE-2019-8331 range, the next question is whether affected tooltip/popover templates are used with attacker-influenced data [11]. This observation -> mechanism -> validation sequence prevents both false alarms and missed custom-code risks.

Because the OBB report concerns custom code on a preview host, the club should pay equal attention to MUJ-specific JavaScript. Vendor upgrades alone cannot fix a custom DOM sink, while custom patches cannot repair an outdated bundled dependency. Both layers require separate ownership.

## Synthesis: Product Lineage Is Stronger Than Vulnerability Attribution

The evidence converges on three different levels of certainty. MUJ has the strongest product attribution because its path literally names Keen and `demo1`. Netkampuss has the strongest Metronic comparator because its source points to the Metronic preview tool and uses the associated KT/bundle conventions. Avenu has a similarly strong family fingerprint but no literal product directory. Assam University demonstrates the false-positive boundary: `style.bundle.css` alone is insufficient.

| Dimension | MUJ SLCM | Netkampuss ERP | Avenu Learning LMS India | Assam University candidate | Keenthemes preview XSS report |
|---|---|---|---|---|---|
| Primary evidence | Explicit Keen/demo1 directory [5] | KT conventions plus Metronic preview reference; education ERP identity [17] | KT conventions plus canonical bundles; LMS identity [18] | Generic bundle filename; university identity [22] | OBB report on preview host [4] |
| Product confidence | High: Keen | High inference: Metronic family | High inference: Metronic family | Low; unconfirmed | Host is KeenThemes, but vulnerable component is Custom Code |
| Exact version | Unknown | Unknown | Unknown | Unknown/not applicable | No distributed theme release identified |
| Security conclusion | Inventory needed | Inventory needed | Inventory needed | Do not attribute | Vendor-host XSS only; inheritance unproven |
| Main trade-off | Strong fingerprint, weak version evidence | Strong family evidence, customized paths | Strong conventions, no literal product label | Avoid false positive | Avoid supply-chain overgeneralization |
| Time horizon | Immediate SBOM and ownership check | Same for operator | Same for operator | Revisit only with better evidence | Monitor report and vendor advisories |

The non-obvious tension is that the most visible evidence is not the evidence needed for a vulnerability decision. A directory path is excellent for product lineage but poor for exact versioning. A CVE record is excellent for defining affected versions and mechanisms but says nothing about whether MUJ has that code. A public XSS report is useful for awareness but can concern custom preview logic rather than the sold theme. Good analysis must join these evidence types only when a verified bridge exists.

The comparison also shows that "Keen or Metronic" should not become a single undifferentiated target class. Shared vendor conventions explain why pages look alike, but each application may contain different bundles, local modifications, authentication systems, and update histories. MUJ's server-side MVC and Microsoft identity assumptions cannot be inferred for Netkampuss or Avenu, and their theme fingerprints cannot establish MUJ's dependencies.

For the university club, the highest-value output is therefore not a list of speculative vulnerable portals. It is a reproducible attribution and triage model:

1. Confirm the product with explicit vendor evidence.
2. Treat `demo1` as a layout/build clue.
3. Establish the exact release and dependency graph internally.
4. Map only version-applicable CVEs.
5. Validate the vulnerable data flow under authorization.
6. Separate vendor code, preview-site custom code, and institution-specific code.

That model is useful beyond MUJ because it turns passive OSINT into defensible asset management without crossing into unauthorized testing.

## VERDICT

**Overall confidence: High for MUJ's Keen/demo1 lineage; medium for the two Metronic-family comparator attributions; low for exact versions; high that no cited evidence proves MUJ has a theme-level XSS.**

1. **MUJ theme:** **Confirmed Keen, demo1 layout/build lineage.** The explicit `/keen/themes/keen/theme/demo1/dist/` path is decisive [5].
2. **MUJ exact theme version:** **Unknown.** No public version banner or manifest was found. Any precise v1.x, v2.x, Bootstrap, or patch assertion would be an unsupported guess.
3. **Other education portals:** **Netkampuss ERP and Avenu Learning LMS India are high-confidence Metronic-family implementations**, based on clusters of KT and canonical bundle markers; exact releases remain unknown [17][18].
4. **Indian government portals:** **None confirmed in the reviewed evidence.** This is a bounded research result, not proof of absence.
5. **Theme-level XSS:** **Not established.** OBB-4445862 affects the KeenThemes preview host but is labeled Custom Code and does not identify distributed theme JavaScript [4].
6. **Dependency vulnerabilities:** **Plausible but unverified.** Bootstrap and jQuery CVEs should be checked only after exact deployed versions and relevant code paths are established [11][13][10].
7. **Meaning of `demo1`:** **A layout/build identifier and passive fingerprint, not a version or exploit.** It becomes a material security issue only if actual sample functionality, sensitive artifacts, or vulnerable dependencies are deployed.

The club's recommended next decision is to request an owner-approved source and SBOM review. Until that review exists, the correct risk statement is: **"Legacy Keen demo1 assets create a component-inventory and maintenance question, but public evidence alone does not demonstrate an exploitable MUJ vulnerability."**

## References

1. *Metronic - The World's #1 Tailwind & Bootstrap Dashboard Since 2013*. https://keenthemes.com/metronic/changelog
2. *Metronic - The World's #1 Dashboard Since 2013*. https://keenthemes.com/metronic/docs
3. *Keen - Multi-demo Bootstrap 5 HTML Admin Dashboard Template ...*. https://preview.keenthemes.com/keen/demo1
4. *preview.keenthemes.com Cross Site Scripting Vulnerability ...*. https://www.openbugbounty.org/reports/4445862/
5. *web.archive.org*. http://web.archive.org/cdx/search/cdx?collapse=urlkey&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&output=json&url=mujslcm.jaipur.manipal.edu/*
6. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
7. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
8. *Keen Latest Version Keenthemes https://devs.keenthemes.com › ...*. https://devs.keenthemes.com/question/keen-latest-version
9. *urlscan.io*. https://urlscan.io/api/v1/search/?q=page.country%3AIN%20AND%20filename%3Astyle.bundle.css&size=100
10. *NVD - CVE-2020-11022*. https://nvd.nist.gov/vuln/detail/CVE-2020-11022
11. *NVD - CVE-2019-8331*. https://nvd.nist.gov/vuln/detail/CVE-2019-8331
12. *NVD - CVE-2019-11358*. https://nvd.nist.gov/vuln/detail/CVE-2019-11358
13. *NVD - CVE-2020-11023*. https://nvd.nist.gov/vuln/detail/CVE-2020-11023
14. *OWASP Application Security Verification Standard (ASVS)*. https://owasp.org/www-project-application-security-verification-standard
15. *OWASP Dependency-Check*. https://owasp.org/www-project-dependency-check
16. *Metronic - Tailwind CSS - @keenthemes*. https://keenthemes.com/metronic/tailwind/docs
17. *Netkampuss | ERP*. https://sch-avms.netkampus.in/
18. *Avenu Learning LMS India | Login*. https://learn-india.avenulearning.com/
19. *OWASP Web Security Testing Guide*. https://owasp.org/www-project-web-security-testing-guide
20. *http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf*. http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf
21. *Home | Avenu Learning*. https://www.avenulearning.com/
22. *Assam University, Silchar*. https://ausexamination.ac.in/
23. *LFMEAB :: Login*. https://demo-compliance.smart-office365.com/
