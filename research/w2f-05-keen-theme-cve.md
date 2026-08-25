# MUJ SLCM Keen Theme Security Exposure Assessment

## Executive Summary

- **Keen Lineage Is Strongly Verified**: The public MUJ login page and the Internet Archive record show `login-v1.css`, `style.bundle.css`, `plugins.bundle.js`, `scripts.bundle.js`, and `login.js` beneath `/keen/themes/keen/theme/demo1/dist/` [3]. This is strong evidence of the legacy Keen `demo1` asset family. It is not, by itself, a version number -> use the path as a product-family fingerprint, then use embedded component banners and file hashes for version analysis.

- **Exact Keen Release Remains Unknown**: The archived MUJ stylesheet identifies **Bootstrap 4.4.1** [8], while the archived plugin bundle identifies **jQuery 3.4.1** [10]. The current Keen demo1 identifies itself as a Bootstrap 5 dashboard [4]. Inference: MUJ uses an older Keen generation than the current preview, but those dependency versions do not uniquely identify one Keen release -> record the package as `Keen legacy demo1, exact release unverified`, not as a guessed release number.

- **Dependency XSS Exposure Is Real but Exploitability Is Unproved**: jQuery 3.4.1 falls inside the affected ranges for CVE-2020-11022 and CVE-2020-11023, both fixed in jQuery 3.5.0 [15][16]. The CVEs require untrusted HTML to reach specific DOM-manipulation methods. Public assets do not establish that condition on MUJ -> prioritize dependency replacement and authorized source review, but do not report a confirmed MUJ XSS vulnerability.

- **Keen JavaScript Contains Security-Relevant Sinks**: The archived `scripts.bundle.js` uses `innerHTML`, `.html()`, and related insertion methods in datatable, error, file-name, message, and quick-search paths; it also conditionally applies DOMPurify to a datatable template [9]. These are review targets, not proof of a flaw -> trace data provenance in the university's authorized source tree before making an XSS finding.

- **The Login Script Is Not a Demonstrated XSS Case**: `login.js` validates username and password fields, uses `ajaxSubmit`, and inserts a fixed error message; the archived code does not demonstrate attacker-controlled data reaching its alert insertion [7]. This distinguishes a dangerous API from a vulnerable data flow -> do not turn a sink inventory into an exploit claim.

- **IIS 10 Is Corroborated; Several Supplied Stack Labels Are Not**: Public urlscan records show three MUJ observations, with the two 2026 observations reporting `Microsoft-IIS/10.0`, Microsoft AS8075, and `98.70.14.50`; the 2024 observation reported IIS 8.5 on a different network [14]. The reviewed evidence does not independently establish `ASP.NET MVC 5.3`, `.NET Framework 4.x`, Akamai, or Microsoft 365 federation -> retain those as supplied hypotheses until configuration, headers, DNS, or identity metadata is reviewed under authorization.

- **Commercial License Compliance Cannot Be Read From CSS**: The MUJ stylesheet contains Bootstrap's MIT copyright and license banner [8], but that is a third-party dependency notice, not a Keen purchase artifact. KeenThemes' terms say Keen sales were handled through getbootstrap and define project and redistribution limits [1][13] -> verify procurement records, invoices, account statements, and the license that applied when MUJ acquired the theme; do not infer infringement from public assets.

- **No Defensible Global Site Count Exists From the Public Evidence**: A urlscan query requiring four legacy filenames returns **2,684 scan results**, not 2,684 unique sites or exact template matches [21]. A single-filename query reaches 10,000 results and still has more, demonstrating severe overbreadth. The latest Common Crawl exact-path query returned no capture [22] -> report the exact global reuse count as `unknown`; treat 2,684 as a bounded candidate-scan count only.

- **Recommended Response Is Defensive Modernization**: Replace or isolate old front-end dependencies, inventory every template bundle with software-composition analysis, review KTDatatable and KTQuickSearch source-to-sink paths, deploy a restrictive Content Security Policy in report-only mode first, and retain evidence of the historical Keen license. Perform testing only in an expressly authorized environment and route any credible finding through MUJ's security process or CERT-In's vulnerability-reporting channel [23].

## Scope, Safety Boundary, and Reproducible Decision Rationale

This report examines only public information: the public login page, Internet Archive CDX and replay records, public urlscan records, current KeenThemes documentation, license terms, and NVD records. It does not use credentials, submit payloads, enumerate accounts, bypass access controls, or direct readers to test a live university service. The MUJ portal itself publicly presents a welcome page with sign-in and parent-login choices [24]. A Manipal compliance document describes SLCM as the Student Life Cycle Management suite for attendance, marks, results, and broadcast messages, making conservative handling appropriate because the system supports student academic records [25].

The requested `cot_explicit` field is addressed with a reproducible evidence rationale rather than private hidden chain-of-thought. The following table exposes the decision rules, evidence gates, and conclusions needed to audit the assessment.

| Table 1 - Decision gate | Evidence accepted | Evidence rejected as insufficient | Result |
|---|---|---|---|
| Product fingerprint | Exact path family, filenames, CSS classes, and KT component names | One generic filename such as `style.bundle.css` | Keen legacy `demo1` lineage: high confidence |
| Exact version | Vendor version banner, package manifest, release-specific hash, or authoritative changelog match | `/demo1/dist/` path alone or current vendor preview | Exact Keen release: unknown |
| XSS applicability | Affected component version plus untrusted source-to-dangerous-sink flow | CVE version match alone or presence of `.html()` alone | Dependency exposure: verified; MUJ exploitability: unproved |
| License compliance | Purchase record, invoice, account statement, purchase code if historically issued, and applicable license text | CSS path, copyright comment, or absence of a public license file | Public compliance status: indeterminate |
| Template reuse count | Deduplicated domains matching multiple exact resource hashes and DOM structure in a defined dataset | Search-engine hit count or filename-only scan count | Global exact count: unknown; urlscan candidate scans: 2,684 |
| Infrastructure claim | Repeated passive observation or first-party configuration | Product-looking URL, IP ownership alone, or user-supplied label | IIS 10 and Microsoft hosting corroborated; other labels unverified |

The method is deliberately asymmetric. Positive evidence can establish that a file, banner, or scan observation existed. Its absence from a search index cannot establish that no other deployment exists. Likewise, finding a vulnerable library version establishes an affected dependency, but not a remotely reachable application vulnerability. This distinction prevents both false reassurance and exaggerated vulnerability claims.

## MUJ Ecosystem Fact Check: What Is Observed Versus Supplied

Public archive data records the MUJ home page and numerous assets with HTTP 200 status on January 10, 2025. The relevant records include `login-v1.css`, `style.bundle.css`, `scripts.bundle.js`, `plugins.bundle.js`, a page-level `login.js`, a standalone `jquery-1.10.2.min.js`, and jQuery validation files [3]. This is a stronger provenance chain than merely recognizing a visual layout because it ties the host to named resources in an independent archive.

The public urlscan dataset contains three scans. The June 2026 and January 2026 observations show `Microsoft-IIS/10.0`, Microsoft AS8075, and IP `98.70.14.50`; a November 2024 scan shows IIS 8.5 and IP `202.131.155.150` on AS45769 [14]. Inference: the service's hosting or delivery path changed between the 2024 and 2026 observations. The data does not show whether the Microsoft address is an origin, reverse proxy, platform service, or another delivery layer.

| Table 2 - Supplied stack claim | Public evidence reviewed | Assessment | Confidence |
|---|---|---|---|
| Keen `demo1` theme | Exact MUJ archive paths under `/keen/themes/keen/theme/demo1/dist/` [3] | Verified product-family fingerprint | High |
| ASP.NET MVC | `/Home/Index`, jQuery validation files, and MVC-like resource organization [3] | Inference: consistent with classic ASP.NET MVC, but not proof | Medium-low |
| ASP.NET MVC 5.3 | No reviewed public artifact states this exact product version | Unverified supplied label; do not publish as fact | Low |
| .NET Framework 4.x | No reviewed artifact exposes an authoritative CLR or framework version | Unverified supplied label | Low |
| IIS 10 | Two 2026 urlscan records report `Microsoft-IIS/10.0` [14] | Corroborated passive observation | High |
| Behind Akamai | Reviewed urlscan records identify Microsoft AS8075, not an Akamai field [14] | Not established; this does not prove Akamai is absent | Low |
| Microsoft-hosted infrastructure | Two 2026 observations map the page IP to Microsoft AS8075 [14] | Corroborated at the observed network layer | High |
| Microsoft 365 identity | Public login branding alone does not prove the identity provider | Unverified; require tenant-authority or redirect metadata | Low |

The table corrects a common OSINT error: a plausible technology label should not become a fact merely because several neighboring clues fit it. `Home/Index` and unobtrusive validation are useful hypotheses for authorized code review, but they do not expose an assembly version. Similarly, an address announced by Microsoft does not prove Microsoft 365 authentication, and failure to see Akamai in three scans does not prove that Akamai is never in the path.

Decision-ready insight: treat the stack description as two layers. The externally supported layer is Keen legacy assets plus IIS 10 on Microsoft-observed infrastructure. The unverified layer is the exact MVC/.NET version, Akamai role, and Microsoft 365 federation. Defensive planning can proceed without overstating the second layer.

## Version Fingerprinting: The Path Identifies a Family, Not a Release

### Case study: MUJ's path says Keen, its banners say legacy generation

The path `/keen/themes/keen/theme/demo1/dist/assets/css/pages/login/login-v1.css` is unusually descriptive. It contains the vendor-family name, theme name, demo number, distribution directory, asset type, page category, and login variant. The archive also records the matching `style.bundle.css`, `plugins.bundle.js`, `scripts.bundle.js`, and `login.js` files [3]. Together, these provide a high-quality family fingerprint and make accidental filename collision unlikely.

The path still lacks an explicit release identifier. `demo1` is a layout designation, while `dist` indicates built output. Neither token is a semantic version. The archived global stylesheet carries a **Bootstrap v4.4.1** banner and MIT notice [8], and the archived plugin bundle carries a **jQuery v3.4.1** banner dated May 1, 2019 [10]. By contrast, the current vendor preview calls Keen demo1 a **Bootstrap 5** admin dashboard [4].

Inference: MUJ's public bundle belongs to a pre-Bootstrap-5 Keen generation. This is an era classification, not an exact Keen release. Different Keen releases, local rebuilds, backported dependencies, and copied assets can share the same directory layout. A deployment can also retain an old directory name after replacing selected files.

| Table 3 - Fingerprint signal | What it establishes | What it does not establish | Evidentiary weight |
|---|---|---|---|
| Full `/keen/themes/keen/theme/demo1/dist/` path | Keen legacy demo1 package lineage | Release number, acquisition date, license validity | High for family |
| `login-v1.css` | Login variant and legacy naming convention | That HTML is byte-identical to the vendor demo | Medium-high |
| `Bootstrap v4.4.1` banner | Bundled stylesheet dependency version [8] | Keen product version | High for dependency |
| `jQuery v3.4.1` banner | Plugin-bundle dependency version [10] | Which jQuery object is active at every execution point | High for dependency |
| Standalone `jquery-1.10.2.min.js` archive URL | A file with that versioned name was archived [3] | The file's integrity or runtime precedence | Medium |
| Current Bootstrap 5 preview | Current vendor generation differs from MUJ's archived Bootstrap 4 assets [4] | Exact date MUJ's package was released | Medium |
| KT component names | Shared Keen/Metronic JavaScript lineage [9] | Commercial edition, release, or patch level | Medium |

A rigorous next step for the university, performed only in its own repository or authorized staging environment, is deterministic package identification. Compare SHA-256 hashes of local vendor files against retained installation media, inspect package manifests and source maps, and map dependency banners to the corresponding Keen changelog. If no exact match exists, document the deployment as a locally modified fork. Do not infer a version by changing live URLs or requesting guessed files.

Decision-ready insight: the defensible label is **`Keen legacy demo1 using Bootstrap 4.4.1-era assets; exact Keen version unknown`**. Any more precise public claim would exceed the evidence.

## XSS Assessment: Dependency Exposure Is Not a Confirmed MUJ Vulnerability

### Case study: jQuery 3.4.1 passes the version gate but not the exploitability gate

The archived plugin bundle explicitly identifies jQuery 3.4.1 [10]. NVD describes CVE-2020-11022 as affecting jQuery from 1.12.0 through versions before 3.5.0 when untrusted HTML is passed to methods such as `.html()` or `.append()`; jQuery 3.5.0 contains the fix [15]. NVD describes CVE-2020-11023 as affecting jQuery from 1.0.3 through versions before 3.5.0 when untrusted HTML containing `option` elements reaches DOM-manipulation methods [16]. Therefore, jQuery 3.4.1 is in both affected ranges. The separately named jQuery 1.10.2 asset is in the CVE-2020-11023 range, but it is below CVE-2020-11022's stated lower boundary [15][16].

That establishes dependency exposure, not a working MUJ attack. Both records require an untrusted-data condition. The archived login script uses validation and `ajaxSubmit`, then constructs an alert using a fixed incorrect-password message [7]. No attacker-controlled response is shown entering that message. Accordingly, the public login script does not satisfy the source-to-sink gate for a confirmed XSS finding.

### Case study: Keen's general bundle contains sinks worth reviewing

The general `scripts.bundle.js` presents a more meaningful review surface. Its archived code inserts file names, messages, dropdown data, datatable cells, errors, and quick-search responses through `.html()` or related APIs; it also uses `innerHTML` in several components [9]. The datatable path conditionally sanitizes a template with DOMPurify when that library is available [9].

Inference: server-returned KTDatatable and KTQuickSearch content are the highest-value authorized review targets because remote data and HTML-producing templates can create a source-to-sink chain. The same evidence also prevents overstatement: conditional DOMPurify use shows that at least one path anticipates HTML-safety concerns, and the public bundle does not reveal MUJ's server-side encoding, response schemas, Content Security Policy, or runtime component usage.

| Table 4 - XSS item | Affected evidence | MUJ relevance | Conclusion |
|---|---|---|---|
| CVE-2020-11022 | jQuery >=1.12.0 and <3.5.0; fixed in 3.5.0 [15] | Bundled jQuery 3.4.1 is in range [10] | Dependency affected; exploitability unproved |
| CVE-2020-11023 | jQuery >=1.0.3 and <3.5.0; fixed in 3.5.0 [16] | jQuery 3.4.1 is in range; version-named 1.10.2 asset is also in range | Dependency affected; exploitability unproved |
| CVE-2019-8331 | Bootstrap before 3.4.1 and Bootstrap 4.3.x before 4.3.1 [19] | MUJ stylesheet says Bootstrap 4.4.1 [8] | Stated affected range does not cover 4.4.1 |
| CVE-2024-6484 | NVD record says the issue was not a Bootstrap security issue and was rescinded [20] | No valid basis for mapping to MUJ | Do not use as evidence |
| CVE-2024-6531 | NVD record likewise says the associated claim was not a Bootstrap security issue [17] | No valid basis for mapping to MUJ | Do not use as evidence |
| CVE-2024-6485 | NVD describes a `data-loading-text` XSS scenario but supplies no affected version range [18] | Cannot map responsibly to Bootstrap 4.4.1 | Applicability unknown |
| KTDatatable/QuickSearch sinks | `.html()`, `innerHTML`, AJAX-response, and template paths [9] | Relevant only if MUJ uses these components with untrusted data | Authorized data-flow review required |
| MUJ `login.js` | Fixed alert text after validation and AJAX submit [7] | No demonstrated untrusted source | No confirmed XSS from this file |

The most important contradiction is that an old library can be genuinely affected while the application remains unexploitable along a particular route. Conversely, absence of proof on the public login page does not show that authenticated datatables or search widgets are safe. The proper classification is therefore **potential dependency-based XSS exposure, no confirmed MUJ XSS**.

## Licensing Artifacts: What Public Files Can and Cannot Prove

### Case study: an MIT banner is not a Keen purchase receipt

The archived MUJ `style.bundle.css` identifies Bootstrap 4.4.1, names the Bootstrap and Twitter copyright holders, and states that Bootstrap is MIT licensed [8]. That notice concerns the open-source dependency. It neither grants nor disproves a commercial Keen license.

KeenThemes' terms state that Keen sales were handled through getbootstrap [1]. The current license explanation describes Bootstrap Market's historical categories: Standard for one end product without source redistribution, Multisite for up to five end products without source redistribution, and Extended for unlimited end products with restricted source redistribution [13]. Current direct Keen plans separately allow unlimited projects for a solo developer or a team of up to 15 developers, while prohibiting redistribution and public sharing; a custom license can grant special redistribution permission [13]. These current terms should not automatically be applied retroactively to a historical purchase.

| Table 5 - Potential artifact | Publicly visible? | What it can prove | What it cannot prove |
|---|---|---|---|
| Keen directory and filenames | Yes [3] | Use or copying of a Keen-family build | Whether the copy was licensed |
| Bootstrap MIT banner | Yes [8] | Dependency attribution and license notice | Commercial Keen entitlement |
| KeenThemes account statement | Not public; terms say transactions are logged [1] | Purchase history associated with the account | Deployment scope without the license text |
| Invoice or procurement record | Not public | Acquisition date, seller, purchaser, and SKU | Continued compliance after transfer or reuse |
| Applicable historical license | Not public for MUJ | Project, developer, client-transfer, and redistribution rights | Whether deployed files stayed within those rights |
| Current Keen license page | Public [13] | Current plan structure | Terms of an earlier purchase unless incorporated |
| Public purchase code or license key | Not found in the current license text [13] | Nothing from current public evidence | Absence does not imply an unlicensed copy |

Inference: the asset layout is useful for internal software inventory, but licensing compliance requires nonpublic records. The university should retain the invoice, account statement, original download archive, version-specific license text, and any client-transfer documentation. If MUJ received the theme through a contractor, the contract should identify which party owned the entitlement and whether transfer was permitted.

Decision-ready insight: public OSINT supports a **license-verification task**, not an infringement allegation. The safe conclusion is `commercial license status indeterminate from public artifacts`.

## Reuse Measurement: 2,684 Candidate Scans Are Not 2,684 Sites

The requested count must first define identity. An exact demo1 login-template match could mean a shared path string, identical CSS bytes, identical JavaScript bytes, matching DOM structure, or visual similarity. Each definition produces a different number. A defensible strict definition would require at least the complete legacy path, the same login-v1 stylesheet hash, the same page-level script hash or DOM signature, and domain deduplication within a named time window.

urlscan documents that its Search API finds archived scans and is subject to individual quotas and visibility controls [2]. A search for `filename:login-v1.css` reports 10,000 results and `has_more: true`, but visible records do not establish the Keen path. This demonstrates why a single basename is too generic.

A stronger public query requiring all four filenames - `login-v1.css`, `style.bundle.css`, `scripts.bundle.js`, and `plugins.bundle.js` - returns **2,684 results** with `has_more: false` [21]. However, those are scan documents. The response includes repeated domains and many subdomains, and the API result does not prove that every matching filename belongs to the exact Keen path or that the page uses the same login DOM. Therefore, **2,684 is a candidate-scan count, not a site count**.

| Table 6 - Reuse measurement | Observed result | Unit actually counted | Fitness for exact-site claim |
|---|---:|---|---|
| urlscan single filename | 10,000 with more results available | Archived scan results matching `login-v1.css` | Very poor; severely overbroad |
| urlscan four-filename conjunction | 2,684, no more indicated [21] | Scan results matching four basenames | Useful candidate set, still not exact |
| Common Crawl August 2026 exact path | No capture found [22] | Captures in one bounded crawl index | A zero for this index only, not the web |
| Common Crawl collection metadata | August 7-20, 2026 for CC-MAIN-2026-34 [12] | One finite crawl period | Establishes denominator limits |
| PublicWWW static result page | No usable count exposed in the extracted public page [26] | Unknown | Cannot support a number |
| Defensible global exact count | Unknown | Deduplicated internet sites | Not measurable from reviewed public evidence |

### Case study: why the zero and 2,684 do not conflict

The Common Crawl query asks for one full asset path in one August 2026 crawl and returns no capture [22]. The urlscan query asks whether four basenames appear in archived scan documents and returns 2,684 results [21]. The datasets, time coverage, crawling behavior, visibility, and match predicates differ. There is no contradiction: a page may be in urlscan but absent from that Common Crawl index, and a urlscan filename match may belong to a different directory or template.

Inference: a research club could publish a reproducible **bounded prevalence study** if it fixes the dataset, date, signature, and deduplication rule. It should not publish an internet-wide exact count. For the present question, the direct answer is: **the exact number of sites reusing the exact MUJ demo1 login template is unknown; 2,684 is the broadest defensible public candidate-scan figure found, not the answer to the exact-site question.**

## Defensive Action Plan for an Authorized University Environment

The highest-value work is dependency and data-flow remediation, not visual rebranding. Renaming `/keen/` or moving files may reduce casual fingerprinting but does not repair vulnerable code. The archive already preserves the historical paths [3], so obscurity has limited security value.

| Table 7 - Priority | Authorized defensive action | Evidence trigger | Completion criterion |
|---:|---|---|---|
| 1 | Inventory all front-end files and produce an SBOM | jQuery 3.4.1 and Bootstrap 4.4.1 banners [8][10] | Every JS/CSS dependency has version, owner, source, and support status |
| 2 | Replace jQuery with a supported release and regression-test | CVE-2020-11022/11023 fixed in 3.5.0 [15][16] | No affected jQuery copy remains in built output or runtime |
| 3 | Trace KTDatatable and KTQuickSearch data flows | Remote/template content enters HTML insertion APIs [9] | Untrusted content is encoded or sanitized at a documented boundary |
| 4 | Review duplicate jQuery loading and execution order | Archive records both a 1.10.2-named file and bundled 3.4.1 [3][10] | One approved jQuery version loads exactly once |
| 5 | Introduce CSP in report-only mode, then enforce | Legacy bundles contain numerous insertion paths [9] | Policy telemetry is clean; unsafe inline allowances are minimized |
| 6 | Rebuild from trusted source rather than editing minified bundles | Exact Keen release is unknown | Reproducible build, locked dependencies, retained source maps, signed artifact hashes |
| 7 | Preserve license evidence | Public assets cannot prove entitlement | Invoice, license text, download archive, and transfer records are retained |
| 8 | Validate supplied architecture labels internally | Public evidence only corroborates part of the claimed stack [14] | CMDB and deployment records state exact framework, CDN, and identity versions |
| 9 | Establish responsible disclosure handling | CERT-In publishes a vulnerability-reporting channel [23] | Security contact, triage SLA, evidence-retention process, and legal authorization are documented |

For XSS review, the authorized team should use source-code analysis and unit tests around encoding boundaries. Test fixtures should remain in a local development or designated staging environment. The review should focus on whether API responses, profile fields, filenames, datatable templates, or search results can carry markup into the sinks already identified. There is no need to test the public portal to answer those questions.

For the theme migration, the team should assume that jumping directly from a legacy Bootstrap 4 Keen build to the current Bootstrap 5 preview may involve markup, plugin, and layout incompatibilities because the current vendor page identifies Bootstrap 5 [4]. A controlled rebuild with regression tests is safer than replacing isolated minified files.

## Synthesis: Separate Provenance, Vulnerability, License, and Prevalence

Four distinct questions are easy to collapse into one: what product is present, which release it is, whether it is exploitable, and how widely the same template is reused. The evidence supports different confidence levels for each.

| Table 8 - Dimension | Provenance strategy | Vulnerability strategy | License strategy | Prevalence strategy |
|---|---|---|---|---|
| Primary mechanism | Path and bundle correlation | Version plus source-to-sink flow | Procurement record plus applicable terms | Exact signature plus dataset-bounded deduplication |
| Strongest MUJ evidence | Full Keen demo1 path family [3] | jQuery 3.4.1 and KT insertion sinks [9][10] | Vendor licensing categories [13] | 2,684 four-filename scan results [21] |
| Main limitation | No Keen version banner | No demonstrated attacker-controlled flow | No public MUJ purchase record | Scan results are not exact unique sites |
| Time horizon | Historical archive and current deployment inventory | Immediate dependency upgrade, then ongoing SCA | Acquisition-time terms plus current deployment scope | Snapshot-specific measurement only |
| False-positive risk | Calling a family path an exact version | Calling an affected dependency a working exploit | Calling absent public evidence infringement | Calling scans, hosts, or subdomains unique sites |
| Recommended conclusion | Legacy Keen demo1, exact release unknown | Potential XSS exposure, not confirmed MUJ XSS | Compliance indeterminate publicly | Exact global count unknown |

The non-obvious tension is that the best fingerprint is also the least useful remediation target. The long Keen path makes vendor attribution easy, yet moving it does not remove the affected jQuery version or dangerous insertion patterns. Conversely, dependency banners are excellent for patch triage but poor for identifying the exact Keen commercial release.

A second tension concerns openness. Public archives improve accountability and let defenders identify obsolete assets, but they also preserve paths after migration. That means a historical fingerprint should not be treated automatically as a current vulnerability. The January 2025 archive proves that those URLs were captured then [3]; a current internal inventory must decide what remains deployed.

A third tension concerns counting. The urlscan candidate query is broad enough to find reuse at scale but too broad to answer the exact-template question. Tightening the signature improves precision while reducing coverage because public crawlers may never fetch every resource. This is a standard precision-recall trade-off. The correct response is not to choose the more dramatic number, but to publish the match rule and label its unit.

Holistic conclusion: MUJ has a well-supported legacy Keen demo1 footprint with old front-end dependencies. This justifies internal modernization and focused source review. It does not justify claims of a known Keen release, confirmed exploitable XSS, license infringement, Akamai or Microsoft 365 architecture, or an exact global clone count.

## VERDICT

| Table 9 - Final finding | Verdict | Confidence |
|---|---|---|
| MUJ uses Keen legacy `demo1` assets | **Confirmed by public path and archive evidence** [3] | High |
| Exact Keen version | **Not established** | Low |
| Bootstrap generation | **Archived bundle identifies Bootstrap 4.4.1** [8] | High |
| jQuery generation | **Archived plugin bundle identifies jQuery 3.4.1** [10] | High |
| Publicly reported XSS applicable to bundled dependency | **CVE-2020-11022 and CVE-2020-11023 version ranges include jQuery 3.4.1** [15][16] | High |
| Confirmed exploitable XSS in MUJ SLCM | **Not proved by public evidence** | Low |
| Confirmed first-party Keen/Metronic CVE in reviewed assets | **Not found; bundle contains review-worthy sinks, not a demonstrated advisory** [9] | Medium |
| IIS 10 | **Corroborated in two 2026 passive observations** [14] | High |
| ASP.NET MVC 5.3 and .NET Framework 4.x | **Supplied but not independently verified** | Low |
| Akamai role | **Not independently verified** | Low |
| Microsoft 365 identity federation | **Not independently verified** | Low |
| Keen commercial license status | **Indeterminate from public artifacts** | Low |
| Exact number of sites reusing the template | **Unknown** | High confidence in non-measurability from reviewed evidence |
| Bounded reuse indicator | **2,684 urlscan candidate scan results, not sites** [21] | High for the query result; low for exact-template prevalence |

**Overall confidence: High for the Keen family fingerprint, embedded dependency versions, IIS 10 observation, and CVE version mapping; medium for the inferred legacy generation and security-review priorities; low for exact Keen release, target exploitability, commercial-license status, uncorroborated architecture labels, and global reuse prevalence.**

The defensible final statement is: **MUJ SLCM publicly exposes a legacy Keen demo1 asset structure whose archived bundles identify Bootstrap 4.4.1 and jQuery 3.4.1. The jQuery version is covered by two public XSS records, and Keen's general bundle contains security-relevant DOM sinks, but public evidence does not prove a working MUJ XSS. The exact Keen release and exact number of sites using the same login template are unknown. A urlscan four-filename query yields 2,684 candidate scans, which must not be represented as 2,684 unique or exact-match sites.**

## References

1. *Terms | Keenthemes*. https://keenthemes.com/terms
2. *Search API Reference - urlscan.io*. https://urlscan.io/docs/search/
3. *web.archive.org*. http://web.archive.org/cdx/search/cdx?collapse=urlkey&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&output=json&url=mujslcm.jaipur.manipal.edu/*
4. *Keen - Multi-demo Bootstrap 5 HTML Admin Dashboard Template by KeenThemes*. https://preview.keenthemes.com/keen/demo1
5. *Login V1*. https://web.archive.org/web/20250110135955id_/https://mujslcm.jaipur.manipal.edu/keen/themes/keen/theme/demo1/dist/assets/css/pages/login/login-v1.css
6. *web.archive.org*. https://web.archive.org/web/20250110135958id_/https://mujslcm.jaipur.manipal.edu/Scripts/jquery-1.10.2.min.js
7. *web.archive.org*. https://web.archive.org/web/20250110135959id_/https://mujslcm.jaipur.manipal.edu/keen/themes/keen/theme/demo1/dist/assets/js/pages/custom/user/login.js
8. *web.archive.org*. https://web.archive.org/web/20250110135955id_/https://mujslcm.jaipur.manipal.edu/keen/themes/keen/theme/demo1/dist/assets/css/style.bundle.css
9. *web.archive.org*. https://web.archive.org/web/20250110135958id_/https://mujslcm.jaipur.manipal.edu/keen/themes/keen/theme/demo1/dist/assets/js/scripts.bundle.js
10. *web.archive.org*. https://web.archive.org/web/20250110135958id_/https://mujslcm.jaipur.manipal.edu/keen/themes/keen/theme/demo1/dist/assets/plugins/global/plugins.bundle.js
11. *urlscan.io*. https://urlscan.io/api/v1/search/?q=filename%3Alogin-v1.css&size=10000
12. *index.commoncrawl.org*. https://index.commoncrawl.org/collinfo.json
13. *Licenses | Keenthemes*. https://keenthemes.com/licensing
14. *urlscan.io*. https://urlscan.io/api/v1/search/?q=domain%3Amujslcm.jaipur.manipal.edu&size=100
15. *NVD - CVE-2020-11022*. https://nvd.nist.gov/vuln/detail/CVE-2020-11022
16. *NVD - CVE-2020-11023*. https://nvd.nist.gov/vuln/detail/CVE-2020-11023
17. *NVD - CVE-2024-6531*. https://nvd.nist.gov/vuln/detail/CVE-2024-6531
18. *NVD - CVE-2024-6485*. https://nvd.nist.gov/vuln/detail/CVE-2024-6485
19. *NVD - CVE-2019-8331*. https://nvd.nist.gov/vuln/detail/CVE-2019-8331
20. *NVD - CVE-2024-6484*. https://nvd.nist.gov/vuln/detail/CVE-2024-6484
21. *urlscan.io*. https://urlscan.io/api/v1/search/?q=filename%3Alogin-v1.css%20AND%20filename%3Astyle.bundle.css%20AND%20filename%3Ascripts.bundle.js%20AND%20filename%3Aplugins.bundle.js&size=10000
22. *index.commoncrawl.org*. https://index.commoncrawl.org/CC-MAIN-2026-34-index?url=%2A%2Fkeen%2Fthemes%2Fkeen%2Ftheme%2Fdemo1%2Fdist%2Fassets%2Fcss%2Fpages%2Flogin%2Flogin-v1.css&output=json&filter=status%3A200&collapse=urlkey
23. *http://cert-in.org.in/RVDCP.jsp*. http://cert-in.org.in/RVDCP.jsp
24. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
25. *http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf*. http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf
26. *" - Web pages - PublicWWW.com*. https://publicwww.com/websites/%22%2Fkeen%2Fthemes%2Fkeen%2Ftheme%2Fdemo1%2Fdist%2Fassets%2Fcss%2Fpages%2Flogin%2Flogin-v1.css%22/
