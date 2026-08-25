# MUJ SLCM Public Package and Source Ecosystem Report

## Executive Summary

- **Published-package finding**: The strongest registry result is `yemit`, an npm package for MIT Manipal students that explicitly describes SLCM attendance use; no published npm package directly named `mujslcm` was returned by the npm registry search [2] [15] [12]. **Action:** treat `yemit` as a relevant historical comparator for Manipal SLCM, not as a MUJ Jaipur package.
- **MUJ-specific distribution finding**: The evidence located for Manipal University Jaipur is concentrated in public GitHub repositories, raw source files, and public web demos rather than npm, PyPI, pub.dev, crates.io, RubyGems, NuGet, or Maven artifacts. **Action:** monitor source repositories and release assets separately from package registries.
- **Browser-extension finding**: `SlcmPlus` identifies itself as a Chrome extension for MUJ students and states that it provides attendance analytics and automatic marks calculation [43]. Its manifest is visibly version `1.1` and contains content-script matches for MUJ SLCM academic pages [43]. **Action:** review the extension as an externally maintained client component, with particular attention to update provenance and permissions.
- **Automation finding**: `krishgoel/slcm-feedback-automation` states that it automates semester-end feedback on the MUJ SLCM portal and links the portal and MUJ website in its README [44]. Its visible requirements file names `python-dotenv==1.0.1` and `selenium==4.20.0` [34]. **Action:** classify it as an automation client, not a published package, and assess credential-handling risk without executing it against the portal.
- **API and scraper finding**: Several public repositories describe APIs or scrapers for Manipal SLCM, including Flask/Python, Python plus Go, and JavaScript/Python variants [40] [41] [40] [23] [20]. **Action:** inventory these repositories as potential unofficial integration code and avoid treating their README claims as proof of current compatibility.
- **Flutter/mobile finding**: `DK10WS/SLCM_APP` describes a Flutter and FastAPI mobile application for MUJ SLCM, with attendance, grades, timetable, and release-oriented distribution language [10] [10]. **Action:** treat APK or web-app distribution as a separate supply-chain channel from pub.dev.
- **Negative-result finding**: PyPI searches for `mujslcm` and `slcm` showed no matching project listings, while the `manipal` search included `mit-cod`, a MIT Manipal course-outcome tool, not a MUJ SLCM wrapper [1] [17] [3]. **Action:** do not report generic lexical matches as target integrations.
- **Security posture finding**: Public code that handles student attendance, grades, timetable, feedback, or credentials creates a plausible confidentiality and account-abuse risk if copied, deployed, or modified. This is a risk inference from the stated functions, not evidence that any listed project is malicious or vulnerable. **Action:** use read-only metadata review, provenance checks, dependency review, and owner-approved testing only.

## Scope, Ethics, and Reproducible Method

This report covers public registry and source-code evidence available from the research run on **2026-08-25**. It searches for the terms `Manipal`, `MUJ`, `SLCM`, and `mujslcm` across npm, PyPI, crates.io, RubyGems, NuGet, Maven Central, pub.dev, GitHub search results, public repository pages, README files, raw manifests, and public project landing pages. The npm registry API returned an explicit zero-object response for `mujslcm` [2]. The other registry checks were interpreted conservatively: a lexical match is not accepted as a relevant package unless its description, README, repository, or metadata connects it to Manipal, MUJ, or SLCM.

The procedure was: first search registry indexes; second inspect authoritative registry metadata where available; third inspect repository README and manifest files for source-only projects; fourth separate published packages, source repositories, browser extensions, mobile applications, and deployed demonstrations; and finally look for counterevidence through unrelated-name collisions. This is a reproducible research summary, not private chain-of-thought. I cannot provide hidden chain-of-thought reasoning, but the evidence trail, decision rules, exclusions, and limitations are stated so a university security club can repeat the work safely.

No login was attempted, no credential was supplied, no CAPTCHA was tested, no endpoint was fuzzed, and no active interaction with the MUJ SLCM portal was performed. The target-domain references in the sources are recorded only as public documentation or manifest strings. The report does not claim that the target is vulnerable, that a repository is malicious, or that any author acted without authorization.

## Registry Results: Published Artifacts Versus Name Collisions

| Registry or channel | Query or evidence | Relevant published artifact found | Interpretation | Exact evidence URL |
|---|---|---|---|---|
| npm | `mujslcm` registry search | None returned | Strong negative for an indexed exact-term npm result at search time; not proof of private, deleted, or future packages | https://registry.npmjs.org/-/v1/search?text=mujslcm&size=250 |
| npm | `manipal` registry search | `yemit` and unrelated `manipal` | `yemit` is directly relevant to MIT Manipal; the package named `manipal` is a generic first module | https://registry.npmjs.org/-/v1/search?text=manipal&size=250 |
| npm | `slcm` registry search | `yemit` | The package description connects it to MIT Manipal and SLCM, but not MUJ Jaipur | https://registry.npmjs.org/-/v1/search?text=slcm&size=250 |
| npm | `MUJ` registry search | Generic collisions, no direct MUJ SLCM package | Names such as `muj-input` or `@mujo/plugins` are not target evidence | https://registry.npmjs.org/-/v1/search?text=MUJ&size=250 |
| PyPI | `mujslcm` search | No matching project listings visible | Negative indexed-search result | https://pypi.org/search/?q=mujslcm |
| PyPI | `slcm` search | No matching project listings visible | Negative indexed-search result | https://pypi.org/search/?q=slcm |
| PyPI | `manipal` search | `mit-cod` among visible listings | MIT Manipal course-outcome utility; not a MUJ SLCM client | https://pypi.org/search/?q=manipal |
| crates.io | `mujslcm` and `manipal` API searches | No direct references in analyzed results | Generic lexical matches were eliminated | https://crates.io/api/v1/crates?search=mujslcm&per_page=100 |
| RubyGems, NuGet, Maven | exact-term checks | No relevant direct artifact in analyzed results | Empty or zero-hit responses were not converted into a universal absence claim | https://rubygems.org/api/v1/search.json?query=mujslcm; https://azuresearch-usnc.nuget.org/query?q=mujslcm&prerelease=true&take=100; https://search.maven.org/solrsearch/select?q=mujslcm&rows=100&wt=json |
| pub.dev | `mujslcm`, Manipal SLCM searches | No named package surfaced in available results | The mobile project is on GitHub/web distribution, not shown as a pub.dev package | https://pub.dev/ |

The table's central distinction is important. A package name containing `muj`, `manipal`, or `slcm` does not establish a relationship to the MUJ SLCM ecosystem. The npm registry's `manipal` result is described as “This is my first module,” while `yemit` explicitly says it is for MIT Manipal and SLCM [15]. Similarly, the PyPI page reports 28 visible or indexed projects for `manipal`, but the relevant listing is `mit-cod`, described as “Course Outcome Digitizer for MIT, Manipal” [17]. These are different institutions and functions from MUJ Jaipur SLCM.

## Case Study 1: npm `yemit` as the Only Clear Published SLCM Utility

The package `yemit` is the clearest published npm artifact found in this investigation. Its registry metadata reports the package name, latest tag `0.1.5`, description “Script for MIT Manipal peeps to check how doomed they are,” author Rohit Sarkar, a command-line binary named `yemit`, and dependencies including `casperjs`, `cli-table`, and `underscore` [26]. The package README says that repeatedly accessing SLCM to see attendance was too much work and presents `npm install -g yemit` as the installation path [21]. The public repository identifies the project as an app for MIT Manipal students to get attendance [25].

This is a meaningful supply-chain case because it connects three layers: a published npm name, a command-line entry point, and a website-facing student utility. It is not, however, direct evidence about MUJ Jaipur. The public descriptions say MIT Manipal, and the repository's own caveat says that the utility can break if SLCM is down or the website is modified [25]. That caveat is useful defensively: a client that depends on page structure is likely to be brittle, and stale code may behave unpredictably after portal changes. It does not prove a defect in the portal or in the package.

The dependency profile also illustrates why registry mining matters. `casperjs` and the command-line wrapper make this more than a static attendance calculator: it is an executable client with external dependencies. That statement is an inference from the published metadata and binary fields, not a claim about runtime behavior beyond what the package page declares. A security club should therefore record the package tarball, lockfile state, maintainer continuity, transitive dependencies, and package integrity through normal offline software-assurance processes. It should not install or run the client against a live student portal without written authorization.

## Case Study 2: `SlcmPlus` and the MUJ Browser-Extension Surface

`SlcmPlus` is explicitly MUJ-specific. Its README describes it as a Chrome extension for MUJ students that adds attendance analytics and automatic marks calculation directly within the portal [43]. The README lists features including calculations related to the required 75% attendance threshold, automatic total-mark calculation from tables, and semester-wise GPA display [43]. The repository's raw manifest identifies Manifest V3, the extension name `SlcmPlus`, version `1.1`, and a description about providing insights for MUJ students [43].

The manifest also contains content-script URL matches for MUJ SLCM academic paths, including attendance and internal-mark pages [43]. This is stronger than a repository title alone because it is a concrete distribution configuration tied to specific pages. It still does not demonstrate that the extension is currently published in the Chrome Web Store, that it is maintained, or that it is safe. The search located the GitHub repository and a GitHub releases page, but no confirmed Chrome Web Store listing for this project [45] [48].

The risk mechanism is straightforward. A browser extension that modifies or reads authenticated academic pages may have access to sensitive page content, and a content script tied to portal URLs can be affected by updates to those URLs or page markup. These are general security implications inferred from the manifest's content-script design and the README's stated analytics functions; they are not findings that the extension exfiltrates data. A defensible review should inspect permissions, content-script scope, update provenance, release assets, build reproducibility, and whether the extension sends data to external origins. Those checks should be performed on downloaded source and manifests offline or in an isolated test environment, not by entering student credentials into an unverified extension.

## Case Study 3: MUJ Feedback Automation and Credential-Handling Risk

The repository `krishgoel/slcm-feedback-automation` states that it automates semester-end feedback on the SLCM portal for Manipal University Jaipur and links directly to the MUJ SLCM and university pages [44]. The repository metadata reports an MIT license, three stars, six forks, a main branch, and a visible `.env.example` file [24]. Its `requirements.txt` names `python-dotenv==1.0.1` and `selenium==4.20.0` [34].

These facts establish a public automation project, not a PyPI package. The `.env.example` filename and `python-dotenv` dependency indicate that environment-based configuration is part of the repository's stated setup, but the available evidence does not establish whether credentials are stored safely, transmitted securely, logged, or retained. Any conclusion beyond that is an inference and must be labelled as such. The project's purpose also creates a business-logic concern: automatically submitting feedback is different from merely displaying attendance. Automated submission can affect institutional records, so authorization, user confirmation, rate limits, auditability, and rollback procedures matter.

A second repository, `vocarista/slcm_feedback_automation`, is also publicly described as a script to automate SLCM feedback [13]. Its existence provides corroboration that feedback automation is a recurring project category, but it does not prove that the two repositories share code, operators, infrastructure, or vulnerabilities. The safe review question is not “how can this be run against the portal?” but “what data and actions would this code handle if an authorized student or administrator ran it in a controlled test environment?”

## Case Study 4: APIs, Scrapers, and Unofficial Client Backends

The older public repository `tejaskash/slcm-api` describes a RESTful API for attendance and marks from the SLCM portal at Manipal University, written in Python with Flask [40]. Its repository metadata shows a MIT license, a master branch, and files including `static/`, `templates/`, and the application source [40]. The README describes attendance and marks response objects and identifies the Manipal SLCM site as the upstream system [40].

`canaryGrapher/slcmAPI` describes an API for Manipal SLCM that exposes marks, attendance, and profile details. Its visible history distinguishes support for marks, attendance, user details, and credential checks [23]. `manipalthetalk/App-Backend` describes a design in which a scraper extracts SLCM data and a server uses it; the repository identifies Python 2.7 and Go [20]. `nikeplusdash/SLCM-api` describes an API for `slcm.manipal.edu` and contains separate SLCM versions and Python/JavaScript source files [41].

These repositories are not MUJ Jaipur-specific on the evidence shown unless their own text says so. They are included because the query asks for the wider Manipal and SLCM ecosystem, and because they demonstrate a repeated architectural pattern: an unofficial client or scraper obtains academic data and presents it through another API or application. The mechanism creates a plausible concentration risk. If a student gives credentials to an intermediary service, the intermediary may become a high-value holder of credentials and academic data. That is an inference from the architecture, not evidence that any listed repository stores credentials improperly.

The source set also includes `sankalp2004/SLCM-is-Dumb`, whose description claims a Python Selenium and OCR scraper for CGPA extraction and references digit-based CAPTCHA handling [20]. Because CAPTCHA bypass or automated authentication can cross legal and institutional boundaries, this report does not reproduce operational instructions or recommend testing it. The appropriate university-club treatment is to record its existence as a high-sensitivity artifact, preserve the public metadata, and refer any authorized assessment to the institution's written rules and responsible-disclosure process.

## MUJ-Specific Source and Application Inventory

| Project | Channel | Publicly stated purpose or README snippet | Stack or source evidence | Distribution status in the evidence | Exact URL |
|---|---|---|---|---|---|
| `SlcmPlus` | GitHub source and extension manifest | “A Chrome extension for MUJ students” providing attendance analytics and automatic marks calculation [43] | Manifest V3; version `1.1`; content-script matches include MUJ SLCM academic pages [43] | GitHub repository and releases page found; Chrome Web Store publication not confirmed [45] [48] | https://github.com/Tejas-Narula/SlcmPlus |
| `krishgoel/slcm-feedback-automation` | GitHub source | Automates semester-end feedback on the MUJ SLCM portal [44] | Python 3; `python-dotenv==1.0.1`; `selenium==4.20.0` [34] | Source repository; not shown as PyPI package | https://github.com/krishgoel/slcm-feedback-automation |
| `vocarista/slcm_feedback_automation` | GitHub source | “Script to automate SLCM feedback” [13] | Detailed dependency evidence not confirmed in the available excerpt | Source repository; not shown as registry package | https://github.com/vocarista/slcm_feedback_automation |
| `DK10WS/SLCM_APP` | GitHub source, mobile/web-app distribution | Mobile application for the university SLCM website, with attendance, grades, and timetable [10] | Flutter frontend, FastAPI backend, Python 3.9+, Docker listed in README evidence [10] | README points to GitHub releases for Android APK and a web-app path for iOS [10] | https://github.com/DK10WS/SLCM_APP |
| `Prashastiiii/mujslcm` | GitHub source | README says “we are making this college project” [33] | Exact stack not established from the short README excerpt | Source repository; no registry artifact established | https://github.com/Prashastiiii/mujslcm |
| `Anushkakumar10/muj_slcm` | GitHub source | Public repository named `muj_slcm` [28] | `requirements.txt` visibly contains Django [27] | Source repository; one search result reports a small repository with one commit and a requirements file [22] | https://github.com/Anushkakumar10/muj_slcm |
| `SLCM Mobile` | Public web demo | “SLCM Mobile Client for Attendance, Timetable & Grades at Manipal University Jaipur” [9] | Web demo; underlying source stack not established from the landing-page excerpt | Public demo; registry publication not shown | https://slcm-client-unoff.vercel.app/ |
| `MUJ Central` | GitHub source | One-stop destination for Manipal University Jaipur students [11] | Full-stack project; exact SLCM integration details not established in the excerpt | Source repository; registry publication not shown | https://github.com/raghavkapoor-prog/MUJ-Central |
| `SlcmAndLms-aggregator` | GitHub source | Combines data from MUJ SLCM and LMS portals in one dashboard [49] | Full-stack application; exact dependency set not established here | Source repository; registry publication not shown | https://github.com/madhav-manchanda/SlcmAndLms-aggregator |
| `SLCM Mobile - MUJ` | Public web demo | Search result describes “The MUJSLCM portal, but actually fast” [50] | Static/demo details not fully established | Public web project; registry publication not shown | https://geervan.github.io/sample/ |

The key takeaway is that MUJ-specific software exists as a small but varied ecosystem: extension, automation script, Django project, Flutter/FastAPI application, dashboard, aggregator, and demos. The available evidence does not establish that these projects are operated by MUJ, endorsed by MUJ, or connected to one another. It also does not establish that any is malicious. Their commonality is functional: they present alternative ways to view, transform, or automate student-portal data.

## What the Registry Results Do and Do Not Prove

The negative registry results are useful but bounded. An exact npm API query for `mujslcm` returned `objects: []` and `total: 0` [2]. PyPI search pages for `mujslcm` and `slcm` showed no matching project listings in the captured pages [1] [3]. Other queried registry endpoints returned empty or zero-hit responses, and crates.io results were explicitly assessed as generic or unrelated [16] [5] [8].

These results support the conclusion that no directly named, publicly indexed package was found in the tested registry searches at the research time. They do not prove that no wrapper exists. A package could use an unrelated name, be private, be deleted, be unindexed by the search endpoint, be distributed only as a GitHub release or APK, or be embedded inside a larger application. The source repositories demonstrate exactly why registry-only searching is insufficient: relevant applications can exist without being published as packages.

The PyPI `mit-cod` result should be retained as a related but excluded artifact. It is described as a “Course Outcome Digitizer for MIT, Manipal” [31], and the search listing identifies it as directly about MIT Manipal but not MUJ, SLCM, or `mujslcm` [17]. This is a useful example of entity resolution: “Manipal” alone does not identify the Jaipur campus or the SLCM portal.

## Defensive Implications for a University Security Club

**Supply-chain provenance.** Maintain separate inventories for registry packages, GitHub source, browser extensions, APKs, and deployed demos. A GitHub repository is not automatically a package, and an APK release is not validated merely because its source is public. Record the exact URL, commit or release identifier, package version, maintainer, license, dependencies, and collection date.

**Credential exposure.** Any unofficial client that accepts student credentials should be presumed sensitive until reviewed, but not presumed malicious. In an authorized lab, inspect configuration handling, logs, debug output, cookies, tokens, HTTP destinations, error reporting, and secret persistence using synthetic accounts and a controlled mock service. Do not submit real student credentials to third-party code.

**Academic-data confidentiality.** Attendance, marks, GPA, timetable, profile, and feedback are student records. The stated features of `SlcmPlus`, `SLCM_APP`, and the API repositories show why these projects can handle sensitive data [43] [10] [23]. A security review should test least privilege, local storage, server-side retention, transport protection, authorization boundaries, and deletion behavior, but only with written permission.

**Update and breakage risk.** The `yemit` repository explicitly warns that changes to SLCM can break the utility [25]. Similar page-dependent clients may fail open, display stale data, submit to the wrong field, or expose debugging information after a portal change. The appropriate control is version pinning, regression testing against a mock portal, explicit user confirmation before submissions, and a rapid disable mechanism.

**Extension and release risk.** For `SlcmPlus`, verify whether the GitHub source corresponds byte-for-byte to any distributed extension, inspect manifest permissions, and review all external network destinations. For `SLCM_APP`, verify release provenance, APK signing, backend ownership, and whether the documented web-app path is still controlled by the same maintainers [10]. These are recommendations based on the distribution models, not allegations about either project.

**Responsible disclosure.** If a source review reveals an actual vulnerability, do not exploit it against the portal or student accounts. Preserve the minimum public evidence, avoid collecting personal data, notify the repository owner and MUJ through an appropriate official channel, and follow the university's rules. The club's public report should redact credentials, cookies, personal identifiers, live tokens, and actionable exploit details.

## Unanswered Questions and Research Gaps

| Question | Current status | Why it remains unanswered | Safe next step |
|---|---|---|---|
| Is there a published npm package specifically for MUJ SLCM? | Not found in the exact-term search | Unrelated package names and private/deleted packages are outside the conclusion | Repeat periodic registry searches and inspect package metadata offline |
| Is there a published PyPI package specifically for MUJ SLCM? | Not found in captured `mujslcm` or `slcm` searches | A project could use an unrelated name or Git-only distribution | Search repository manifests and package metadata, not only names |
| Is `SlcmPlus` published in an extension store? | Not confirmed | Search found GitHub and releases but no confirmed store listing [48] | Check the store manually without installing or signing in; record only public listing data |
| What exact permissions and network destinations does `SlcmPlus` use? | Partially answered | The captured manifest excerpt shows URL matches but not the complete manifest | Review the raw manifest and source offline; do not load it with a real account |
| Does `SLCM_APP` currently distribute an APK or web app? | README describes release and web-app paths [10] | Current asset availability and provenance were not independently validated | Review public release metadata and signing information without installing on a personal device |
| Do the repositories share code or infrastructure? | Not established | Similar functionality does not prove common authorship or reuse | Compare public commit history and licenses offline; avoid credential or portal testing |
| Are any listed artifacts malicious or vulnerable? | No determination | Public descriptions alone cannot support that conclusion | Conduct authorized static and dependency analysis in an isolated lab |
| Does any artifact target the exact MUJ hostname today? | Manifest and README references exist for some MUJ projects [43] [44] | Current runtime behavior was not tested | Use a mock target or owner-provided test environment |

## Synthesis

Across the ecosystem, four dimensions separate the artifacts. First is **distribution**: `yemit` is a published npm package, `mit-cod` is a published PyPI package for MIT Manipal but not SLCM, while most MUJ projects are GitHub repositories, extension source, APK-oriented releases, or demos. Second is **function**: `SlcmPlus` is an in-browser analytics enhancement, feedback repositories automate a state-changing workflow, API projects create intermediary data services, and `SLCM_APP` presents a mobile client. Third is **data sensitivity**: analytics may read academic pages, APIs and mobile apps may centralize attendance and grades, and feedback automation may submit institutional records. Fourth is **maintenance risk**: page-dependent code can break when upstream markup changes, a risk explicitly acknowledged by `yemit` [25].

The non-obvious tension is that the registry footprint is small while the application footprint is broader. A registry search may suggest little activity, but public source discovery reveals multiple client patterns. This means package-name monitoring alone is not an adequate defensive control. Conversely, the existence of many repositories does not establish a coordinated ecosystem, current operation, or malicious intent. The evidence supports a targeted inventory and provenance program, not an accusation.

The second tension is between convenience and control. Attendance dashboards, mobile clients, and automated forms can reduce repetitive work, but they also move access and decision-making outside the official portal. The safer strategic boundary is to prefer read-only, locally executed, source-auditable tools; require explicit confirmation for submissions; use synthetic test identities; and prohibit unapproved credential forwarding. Where a third-party backend is involved, the club should treat it as a separate data processor and demand clear ownership, retention, and incident-contact information before any institutional use.

## VERDICT

**Verdict: No directly named MUJ SLCM package was found in the tested public npm, PyPI, crates.io, RubyGems, NuGet, Maven, or pub.dev searches as of 2026-08-25.** The strongest published registry finding is `yemit`, an npm utility explicitly associated with MIT Manipal SLCM, not MUJ Jaipur [2] [26] [21]. The strongest MUJ-specific findings are public source and application artifacts: `SlcmPlus`, feedback automation repositories, `SLCM_APP`, Django and dashboard projects, and public demos [43] [44] [10] [9].

**Confidence: High for the observed search results; moderate for the broader absence claim.** Confidence is high because authoritative registry endpoints and public project pages were queried and the key negative results were explicit. Confidence is moderate, rather than absolute, because lexical searches cannot detect private, deleted, unindexed, renamed, or future artifacts, and source-only projects may embed dependencies without publishing a package. No evidence in this research proves compromise, unauthorized access, or vulnerability in the MUJ SLCM service.

## References

1. *Search results · PyPI*. https://pypi.org/search/?q=mujslcm
2. *registry.npmjs.org*. https://registry.npmjs.org/-/v1/search?text=mujslcm&size=250
3. *Search results · PyPI*. https://pypi.org/search/?q=slcm
4. *GitHub - Prashastiiii/mujslcm*. https://github.com/Prashastiiii/mujslcm
5. *azuresearch-usnc.nuget.org*. https://azuresearch-usnc.nuget.org/query?q=mujslcm&prerelease=true&take=100
6. *GitHub - akjha992/MU-SLCM-APP*. https://github.com/akjha992/MU-SLCM-APP
7. *GitHub - krishgoel/slcm-feedback-automation: An automation ...*. https://github.com/KrishGoel/slcm-feedback-automation
8. *search.maven.org*. https://search.maven.org/solrsearch/select?q=mujslcm&rows=100&wt=json
9. *SLCM Mobile - MUJ*. https://slcm-client-unoff.vercel.app/
10. *GitHub - DK10WS/SLCM_APP: App Version for MUJ SLCM*. https://github.com/DK10WS/SLCM_APP
11. *GitHub - raghavkapoor-prog/MUJ-Central: MUJ Central is a ...*. https://github.com/raghavkapoor-prog/MUJ-Central
12. *registry.npmjs.org*. https://registry.npmjs.org/-/v1/search?text=slcm&size=250
13. *GitHub - vocarista/slcm_feedback_automation: Script to ...*. https://github.com/vocarista/slcm_feedback_automation
14. *Search results · PyPI*. https://pypi.org/search/?q=MUJ
15. *registry.npmjs.org*. https://registry.npmjs.org/-/v1/search?text=manipal&size=250
16. *crates.io*. https://crates.io/api/v1/crates?search=manipal&per_page=100
17. *Search results · PyPI*. https://pypi.org/search/?q=manipal
18. *registry.npmjs.org*. https://registry.npmjs.org/-/v1/search?text=MUJ&size=250
19. *crates.io*. https://crates.io/api/v1/crates?search=mujslcm&per_page=100
20. *GitHub - manipalthetalk/App-Backend: Scrapes the SLCM for ...*. https://github.com/manipalthetalk/App-Backend
21. *yemit - npm*. https://www.npmjs.com/package/yemit
22. *GitHub - Anushkakumar10/muj_slcm · GitHub*. http://github.com/Anushkakumar10/muj_slcm
23. *GitHub - canaryGrapher/slcmAPI: The API for SLcM, Manipal. Get your marks, your attendance and your profile details · GitHub*. http://github.com/canaryGrapher/slcmAPI
24. *GitHub - krishgoel/slcm-feedback-automation: An automation script for filling out semester-end feedback on the college portal (SLCM Manipal, Jaipur) · GitHub*. https://github.com/krishgoel/slcm-feedback-automation
25. *GitHub - rsarky/yemit: :tada: An app for MIT Manipal students to get their attendance.*. https://github.com/rsarky/yemit
26. *registry.npmjs.org*. https://registry.npmjs.org/yemit
27. *Muj Slcm*. https://raw.githubusercontent.com/Anushkakumar10/muj_slcm/main/requirements.txt
28. *Muj Slcm*. https://raw.githubusercontent.com/Anushkakumar10/muj_slcm/main/README.md
29. *Slcm Feedback Automation*. https://raw.githubusercontent.com/krishgoel/slcm-feedback-automation/main/.env.example
30. *pub.dev*. https://pub.dev/api/search?q=mujslcm
31. *Client Challenge*. https://pypi.org/project/mit-cod/
32. *pub.dev*. https://pub.dev/api/search?q=manipal%20slcm
33. *raw.githubusercontent.com*. https://raw.githubusercontent.com/Prashastiiii/mujslcm/main/README.md
34. *Slcm Feedback Automation*. https://raw.githubusercontent.com/krishgoel/slcm-feedback-automation/main/requirements.txt
35. *GitHub - DK10WS/SLCM_APP: App Version for MUJ SLCM · GitHub*. https://github.com/DK10WS/SLCM_APP/tree/main
36. *registry.npmjs.org*. https://registry.npmjs.org/manipal
37. *Tejas Narula*. https://raw.githubusercontent.com/Tejas-Narula/SlcmPlus/main/manifest.json
38. *Mit Cod*. https://pypi.org/pypi/mit-cod/json
39. *GitHub - Tejas-Narula/SlcmPlus: A Chrome extension for MUJ students that enhances the SLCM experience by providing attendance analytics and automatic marks calculation directly within the portal. · GitHub*. https://github.com/Tejas-Narula/SlcmPlus/tree/main
40. *GitHub - tejaskash/slcm-api: A RESTful API to get attendance and marks data from SLCM Portal at Manipal University, written in Python using Flask. · GitHub*. https://github.com/tejaskash/slcm-api
41. *GitHub - nikeplusdash/SLCM-api: An api for https://slcm.manipal.edu · GitHub*. https://github.com/nikeplusdash/SLCM-api
42. *GitHub - sankalp2004/SLCM-is-Dumb: This extracts cgpa from https://slcm.manipal.edu/ directly and passes captcha · GitHub*. https://github.com/sankalp2004/SLCM-is-Dumb
43. *Tejas Narula*. https://raw.githubusercontent.com/Tejas-Narula/SlcmPlus/main/README.md
44. *Slcm Feedback Automation*. https://raw.githubusercontent.com/krishgoel/slcm-feedback-automation/main/README.md
45. *GitHub - Tejas-Narula/SlcmPlus: A Chrome extension for MUJ students that enhances the SLCM experience by providing attendance analytics and automatic marks calculation directly within the portal. · GitHub*. https://github.com/Tejas-Narula/SlcmPlus
46. *Slcm Feedback Automation*. https://raw.githubusercontent.com/vocarista/slcm_feedback_automation/main/README.md
47. *Slcm App*. https://raw.githubusercontent.com/DK10WS/SLCM_APP/main/README.md
48. *Releases · Tejas-Narula/SlcmPlus · GitHub*. https://github.com/Tejas-Narula/SlcmPlus/releases
49. *madhav-manchanda/SlcmAndLms-aggregator - GitHub*. https://github.com/madhav-manchanda/SlcmAndLms-aggregator/tree/main
50. *SLCM Mobile | For MUJ - geervan.github.io*. https://geervan.github.io/sample/
