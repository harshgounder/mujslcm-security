# Digest: w2e-10-keentheme-portals

## REPORT
Source file: w2e-10-keentheme-portals.md (What Keen Demo1 Paths Reveal About MUJ SLCM)

## ANSWER SUMMARY
- MUJ's login front end is confirmed as Keen product lineage via archived asset paths /keen/themes/keen/theme/demo1/dist/ with login-v1.css, style.bundle.css and plugin bundles.
- Exact Keen release is unknown; no version banner or manifest. Defensible label: "Keen, legacy generation, exact release unverified".
- demo1 is a layout/build identifier, not a version number, not a staging flag, and not evidence of default accounts or an exposed admin panel.
- Two high-confidence Metronic-family comparators: Netkampuss ERP (sch-avms.netkampus.in, HOST_URL to the Metronic preview tool) and Avenu Learning LMS India (learn-india.avenulearning.com); neither discloses a version.
- No gov.in portal is confirmed as Keen/Metronic in this evidence set; Assam University and LFMEAB pages are excluded as false positives.
- OBB-4445862 (XSS on preview.keenthemes.com, reported Jan 12 2026, unpatched at review) is labeled Custom Code, not distributed theme JavaScript; it does not prove a MUJ theme XSS.
- Bootstrap and jQuery CVEs (2019-8331, 2020-11022, 2020-11023, 2019-11358) are conditional on exact deployed versions and data flows; not MUJ findings.
- Recommended next step is an owner-approved source and SBOM review, not Internet-side testing.

## KEY FACTS
1. https://mujslcm.jaipur.manipal.edu/ - visible MUJ PORTAL login, the theme target page.
2. http://web.archive.org/cdx/search/cdx?collapse=urlkey&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&output=json&url=mujslcm.jaipur.manipal.edu/* - archive inventory proving the /keen/.../demo1/dist/ asset paths.
3. https://mujslcm.jaipur.manipal.edu/Home/Index - /Home/Index route, MVC-convention compatible.
4. https://keenthemes.com/metronic/changelog - Metronic changelog showing dependency security fixes; no version bridge to MUJ.
5. https://preview.keenthemes.com/keen/demo1 - official Keen demo1 preview; product naming source.
6. https://www.openbugbounty.org/reports/4445862/ - preview.keenthemes.com XSS, component labeled Custom Code.
7. https://sch-avms.netkampus.in/ - Netkampuss ERP page with KT globals and Metronic preview HOST_URL.
8. https://learn-india.avenulearning.com/ - Avenu Learning LMS India login with canonical KT bundle paths.
9. https://ausexamination.ac.in/ - Assam University exam page; excluded, generic bundle filename only.
10. https://demo-compliance.smart-office365.com/ - LFMEAB styled page; excluded, not an official gov.in domain.
11. https://nvd.nist.gov/vuln/detail/CVE-2019-8331 - Bootstrap tooltip/popover XSS; conditional check only.
12. https://nvd.nist.gov/vuln/detail/CVE-2020-11022 - jQuery DOM-manipulation XSS; conditional check only.
13. https://nvd.nist.gov/vuln/detail/CVE-2020-11023 - jQuery option-element XSS; conditional check only.
14. https://nvd.nist.gov/vuln/detail/CVE-2019-11358 - jQuery Object.prototype pollution; conditional check only.
15. https://owasp.org/www-project-dependency-check - tool for automated component inventory in the authorized review.

## ACTIONABLE LEADS
- Ask the MUJ owner for the licensed Keen package version, source repo tag, build job, package.json, and lockfile.
- Generate an internal SBOM for the deployed front-end build; map only version-applicable CVEs.
- Compare deployed static-file hashes against approved builds to find drift and stale bundles.
- Inventory deployed sample pages and source maps; remove unnecessary vendor material.
- Review custom JavaScript DOM sinks (URL, message, profile, server data) before claiming XSS conditions.
- Verify CSP, cookies, anti-forgery, login throttling, and identity config under written authorization.
- Assign ownership and update cadence for the theme to prevent orphaned vendor assets.

## FLAGS
- Any Keen v1.x, Bootstrap 4, or patch-level claim in the wild would be unsupported; the report explicitly avoids guessing versions.
- OBB-4445862 concerns preview-host custom code; do not generalize to the distributed theme or to MUJ.
- urlscan.io API query (reference 9) is cited as supporting evidence but no results are shown in the report; treat as weak secondary support.
- devs.keenthemes.com forum answer (reference 8) is unverified community content.
- demo1 must not be treated as a routable application route, dev environment, or authentication bypass.
- Generic filenames like style.bundle.css alone are not distinctive (Assam case demonstrates the false-positive boundary).

## COVERAGE
- Chars read: 33,727
- EOF confirmed: yes (truncated: false on final page, 251 of 251 lines)