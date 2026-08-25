# Digest: w2g-11-npm-pypi.md

## REPORT
Source file: w2g-11-npm-pypi.md. Public package-registry and source-ecosystem assessment for the MUJ SLCM vocabulary (Manipal, MUJ, SLCM, mujslcm) across npm, PyPI, crates.io, RubyGems, NuGet, Maven Central, pub.dev, and GitHub, research date 2026-08-25. 50 references.

## ANSWER SUMMARY
- Verdict: no directly named MUJ SLCM package was found in the tested public npm, PyPI, crates.io, RubyGems, NuGet, Maven, or pub.dev searches as of 2026-08-25. The only clear published SLCM utility is npm `yemit`, which is MIT Manipal, not MUJ Jaipur.
- `yemit` (v0.1.5, author Rohit Sarkar): attendance utility for MIT Manipal SLCM, CLI binary, dependencies casperjs, cli-table, underscore; repository caveat says the utility can break if SLCM is down or the site is modified. Useful supply-chain comparator, not a MUJ artifact.
- MUJ-specific footprint sits in source and distribution channels, not registries: SlcmPlus Chrome extension (Manifest V3, version 1.1, content-script matches for MUJ SLCM attendance and marks pages; Chrome Web Store listing unconfirmed), krishgoel/slcm-feedback-automation (python-dotenv==1.0.1, selenium==4.20.0), DK10WS/SLCM_APP (Flutter frontend, FastAPI backend, APK and web-app release paths), MUJ-Central, SlcmAndLms-aggregator, plus public demos slcm-client-unoff.vercel.app and geervan.github.io/sample.
- npm registry API for `mujslcm` returned an explicit zero-object response; PyPI pages for `mujslcm` and `slcm` show no matching listings; collisions such as `muj-input`, `@mujo/plugins`, and the npm package named `manipal` ("this is my first module") were excluded as non-evidence.
- PyPI `manipal` search surfaces mit-cod, a "Course Outcome Digitizer for MIT, Manipal" course-outcome tool; relevant to MIT Manipal only, excluded from MUJ evidence.
- Feedback automation is a recurring category: vocarista/slcm_feedback_automation is a second public SLCM feedback script; automated submission changes institutional records, so authorization, user confirmation, rate limits, auditability, and rollback procedures matter.
- Unofficial API/scraper cluster (tejaskash/slcm-api Flask, canaryGrapher/slcmAPI, manipalthetalk/App-Backend Python 2.7 + Go, nikeplusdash/SLCM-api) targets the broader Manipal SLCM and would concentrate credentials if deployed as intermediaries. sankalp2004/SLCM-is-Dumb is recorded as a high-sensitivity CAPTCHA-automation artifact without operational detail.
- Confidence: High for the observed search results; moderate for the broader absence claim. No evidence proves compromise, unauthorized access, or vulnerability in the MUJ SLCM service.

## KEY FACTS
- https://registry.npmjs.org/-/v1/search?text=mujslcm&size=250 - explicit zero-object, total 0 response; the anchor negative for npm.
- https://www.npmjs.com/package/yemit - the only clear published SLCM utility; MIT Manipal, not MUJ.
- https://registry.npmjs.org/yemit - registry metadata: v0.1.5, Rohit Sarkar, casperjs/cli-table/underscore dependencies.
- https://github.com/rsarky/yemit - source repo; warning that SLCM changes or downtime break the utility.
- https://pypi.org/search/?q=mujslcm - no matching project listings.
- https://pypi.org/search/?q=slcm - no matching project listings.
- https://pypi.org/project/mit-cod/ - Course Outcome Digitizer for MIT, Manipal; retained as related-but-excluded.
- https://github.com/Tejas-Narula/SlcmPlus - MUJ-specific Chrome extension repository.
- https://raw.githubusercontent.com/Tejas-Narula/SlcmPlus/main/manifest.json - Manifest V3, version 1.1, content-script matches on MUJ SLCM academic pages.
- https://github.com/Tejas-Narula/SlcmPlus/releases - releases page found; Chrome Web Store publication not confirmed.
- https://github.com/krishgoel/slcm-feedback-automation - MUJ SLCM semester-end feedback automation; MIT license, 3 stars, 6 forks, visible .env.example.
- https://raw.githubusercontent.com/krishgoel/slcm-feedback-automation/main/requirements.txt - python-dotenv==1.0.1 and selenium==4.20.0 pinned.
- https://github.com/DK10WS/SLCM_APP - Flutter and FastAPI mobile application for MUJ SLCM; README points to Android APK and a web-app path.
- https://slcm-client-unoff.vercel.app/ - public web demo: "SLCM Mobile Client for Attendance, Timetable & Grades at Manipal University Jaipur".
- https://github.com/madhav-manchanda/SlcmAndLms-aggregator - dashboard combining MUJ SLCM and LMS data; full-stack source project.

## ACTIONABLE LEADS
- Maintain separate supply-chain inventories per channel: registry packages, GitHub source, browser extensions, APKs, and deployed demos; record exact URL, commit or release identifier, version, maintainer, license, dependencies, collection date.
- For SlcmPlus: verify whether any distributed build matches the GitHub source byte-for-byte, inspect the full manifest permissions offline, enumerate external network destinations; check the store manually without installing or signing in.
- For DK10WS/SLCM_APP: validate release provenance, APK signing, backend ownership, and whether the web-app path is still controlled by the same maintainers.
- For krishgoel and vocarista feedback scripts: in an authorized lab only, review credential handling, logging, debug output, cookies, tokens, HTTP destinations, and secret persistence using synthetic accounts and a mock service; never submit real student credentials to third-party code.
- For the API/scraper cluster: treat each as a separate data processor; require ownership, retention, and incident-contact clarity before any institutional use; prefer read-only, locally executed, source-auditable tools.
- Registry monitoring: repeat periodic exact-term searches (npm, PyPI, crates, pub.dev) and also search repository manifests and metadata, since source-only projects never surface as packages.
- Responsible disclosure: on a real vulnerability, preserve minimum evidence, redact credentials and personal identifiers, notify the owner and MUJ through official channels, follow university rules.

## FLAGS
- All negative registry results are bounded: private, deleted, unindexed, renamed, or future packages are outside the conclusion, and embedded dependencies in source-only projects are invisible to lexical searches.
- `yemit` and `mit-cod` are MIT Manipal artifacts; citing either as MUJ supply-chain evidence overclaims. Entity resolution: "Manipal" alone never identifies the Jaipur campus.
- SlcmPlus store publication, current maintenance, and safety are unconfirmed; content-script URL matches prove page targeting, nothing about distribution.
- DK10WS/SLCM_APP source may not match distributed binaries; README release claims were not independently validated.
- The report explicitly makes no maliciousness determination for any listed project; all security statements about credential handling are labeled risk inferences.
- Two GitHub reference URLs use http:// (Anushkakumar10/muj_slcm, canaryGrapher/slcmAPI); harmless but inconsistent with the https corpus.
- Findings are time-bound to 2026-08-25 registry state.

## COVERAGE
- File: w2g-11-npm-pypi.md.
- 190 lines total; 33,803 bytes on disk; 33,740 chars read.
- Method: read_file offset 1, limit 2000, single call.
- EOF confirmed: final call returned truncated: false, last content line 190 equals total_lines 190.