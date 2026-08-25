# Digest: w2f-05-keen-theme-cve.md

## REPORT
Source file: w2f-05-keen-theme-cve.md (35,154 bytes, 248 lines, read to EOF)

## ANSWER SUMMARY
- MUJ login page and Internet Archive records show the Keen demo1 asset family under `/keen/themes/keen/theme/demo1/dist/`. Exact Keen release is unknown.
- Archived bundles identify Bootstrap 4.4.1 and jQuery 3.4.1. jQuery 3.4.1 sits in the affected ranges of CVE-2020-11022 and CVE-2020-11023. Dependency exposure is verified; MUJ exploitability is unproved.
- `scripts.bundle.js` holds `innerHTML` and `.html()` sinks in datatable, error, filename, message, and quick-search paths, with conditional DOMPurify use. `login.js` shows no demonstrated attacker-controlled flow.
- IIS 10 is corroborated by two 2026 urlscan observations (98.70.14.50, Microsoft AS8075). ASP.NET MVC 5.3, .NET Framework 4.x, Akamai, and Microsoft 365 federation remain unverified supplied labels.
- A urlscan four-filename query returns 2,684 candidate scan results, not 2,684 sites. A Common Crawl August 2026 exact-path query returned no capture. Exact global reuse count is unknown.
- Commercial license status is indeterminate from public artifacts. The MIT banner in `style.bundle.css` covers the Bootstrap dependency, not a Keen purchase.
- Recommended response is defensive modernization: SBOM, jQuery replacement, source-to-sink review of KTDatatable and KTQuickSearch, report-only CSP, retained license evidence, CERT-In disclosure route.

## KEY FACTS
1. http://web.archive.org/cdx/search/cdx?collapse=urlkey&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&output=json&url=mujslcm.jaipur.manipal.edu/* - CDX provenance proving the Keen demo1 assets were archived with HTTP 200.
2. https://web.archive.org/web/20250110135955id_/https://mujslcm.jaipur.manipal.edu/keen/themes/keen/theme/demo1/dist/assets/css/style.bundle.css - archived stylesheet carries the Bootstrap 4.4.1 MIT banner.
3. https://web.archive.org/web/20250110135958id_/https://mujslcm.jaipur.manipal.edu/keen/themes/keen/theme/demo1/dist/assets/plugins/global/plugins.bundle.js - archived plugin bundle identifies jQuery 3.4.1, dated May 1 2019.
4. https://web.archive.org/web/20250110135958id_/https://mujslcm.jaipur.manipal.edu/keen/themes/keen/theme/demo1/dist/assets/js/scripts.bundle.js - archived general bundle with HTML insertion sinks and conditional DOMPurify.
5. https://web.archive.org/web/20250110135959id_/https://mujslcm.jaipur.manipal.edu/keen/themes/keen/theme/demo1/dist/assets/js/pages/custom/user/login.js - archived login script uses validation, ajaxSubmit, and a fixed error message with no untrusted flow shown.
6. https://web.archive.org/web/20250110135958id_/https://mujslcm.jaipur.manipal.edu/Scripts/jquery-1.10.2.min.js - second version-named jQuery asset; raises a duplicate-load and execution-order question.
7. https://nvd.nist.gov/vuln/detail/CVE-2020-11022 - jQuery 1.12.0 to before 3.5.0 XSS range that covers the bundled 3.4.1.
8. https://nvd.nist.gov/vuln/detail/CVE-2020-11023 - jQuery 1.0.3 to before 3.5.0 option-element range that also covers the 1.10.2 asset.
9. https://urlscan.io/api/v1/search/?q=domain%3Amujslcm.jaipur.manipal.edu&size=100 - three scans; the 2026 pair reports Microsoft-IIS/10.0 on AS8075 at 98.70.14.50, the 2024 scan reports IIS 8.5 on AS45769.
10. https://urlscan.io/api/v1/search/?q=filename%3Alogin-v1.css%20AND%20filename%3Astyle.bundle.css%20AND%20filename%3Ascripts.bundle.js%20AND%20filename%3Aplugins.bundle.js&size=10000 - 2,684 candidate scan results with no more indicated; scan documents, not unique sites.
11. https://urlscan.io/api/v1/search/?q=filename%3Alogin-v1.css&size=10000 - 10,000 hits with more available; shows a single basename is severely overbroad.
12. https://index.commoncrawl.org/CC-MAIN-2026-34-index?url=%2A%2Fkeen%2Fthemes%2Fkeen%2Ftheme%2Fdemo1%2Fdist%2Fassets%2Fcss%2Fpages%2Flogin%2Flogin-v1.css&output=json&filter=status%3A200&collapse=urlkey - no capture in the August 2026 crawl; a bounded zero for that index only.
13. https://preview.keenthemes.com/keen/demo1 - current vendor demo1 is a Bootstrap 5 dashboard, distinct from MUJ's archived Bootstrap 4 era assets.
14. https://mujslcm.jaipur.manipal.edu/Home/Index - public welcome page with sign-in and parent-login choices.
15. http://cert-in.org.in/RVDCP.jsp - CERT-In vulnerability-reporting channel for routing any confirmed finding.

## ACTIONABLE LEADS
- Review the archived URLs above for exact byte evidence; compare SHA-256 hashes against retained Keen installation media in the university repo.
- Owner-side review targets: KTDatatable and KTQuickSearch source-to-sink flows in `scripts.bundle.js`.
- Verify current live asset paths and headers before treating the January 2025 archive as current state.
- Request an SBOM, single jQuery load, and report-only CSP rollout.
- License step: retain invoice, account statement, download archive, version-specific license text, and transfer records.
- Disclosure step: route any confirmed finding via CERT-In RVDCP; nothing confirmed to report yet.

## FLAGS
- No contradiction between 0 Common Crawl captures and 2,684 urlscan results; the datasets, predicates, and time windows differ.
- Supplied labels MVC 5.3, .NET 4.x, Akamai, M365 federation are not verified by this report; do not publish as fact.
- 2,684 is a bounded candidate-scan count; repeated domains and subdomains are present in the result set.
- CVE-2024-6485 has no affected version range; CVE-2024-6531 and CVE-2024-6484 were marked not Bootstrap security issues; do not use as evidence.
- CVE-2019-8331 does not cover Bootstrap 4.4.1.
- No public purchase record exists; absence of a license file is not proof of infringement.
- All archive, scan, and vendor URLs are point-in-time and unverified by this digest.

## COVERAGE
Chars read: 35,154 (full file, 248 lines). EOF confirmed: truncated false on the complete read.

DONE w2f-05-keen-theme-cve.md.digest.md