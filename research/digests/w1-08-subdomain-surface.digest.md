## REPORT (w1-08-subdomain-surface.md)
Passive public attack-surface mapping of jaipur.manipal.edu + manipal.edu subdomains, dated 2026-08-25. Sources: crt.sh CT, dns.google, Wayback, Shodan public pages, ipinfo.io, fetched public pages. No active probing, no auth, no port scans. 362 lines, 41643 chars, read to EOF.

## ANSWER SUMMARY
- Two live MUJ SLCM generations: `mujslcm.jaipur.manipal.edu` (A 98.70.14.50, IIS 10/ASP.NET MVC 5.3, `@muj.manipal.edu`, separate parent/student login) and `muj.slcm.jaipur.manipal.edu` (A 20.244.94.89, IIS 10, ASP.NET 4.0.30319, jQuery 1.10.2, `@jaipur.manipal.edu`). Both sit in Microsoft AS8075 space; report treats them as distinct production identity surfaces.
- Shared MAHE core: `slcm.manipal.edu` (A 104.211.226.160, IIS 10/ASP.NET, Microsoft AS8075) and `sis.manipal.edu` (A 218.248.47.25, IIS 10, National Internet Backbone AS9829, fee payment routed to Fee Kart).
- Hosting estate is split, not one stack: Azure DNS at parent apex, AWS EC2 ap-south-1 for `jaipur.manipal.edu` apex (3.108.105.201) and `api.manipal.edu` (43.205.223.7, nginx 1.18.0/Node.js/Express), D2L Brightspace for `lms.manipal.edu`, Microsoft 365 mail on both apexes, Google Sites for `library.jaipur.manipal.edu`.
- Jaipur CT history holds 25 unique names including non-obvious `mujerp`, `mujone`, `npfslcm`, `rms`, `lcs`, `helpdesk`, `idp`, `dms`, `pms`, `mycampus`, `testmycampus`; CT is treated strictly as historical inventory, not proof of live DNS.
- Dictionary guesses under jaipur (`lms`, `erp`, `portal`, `mail`, `api`, `dev`, `test`, `staging`) are mostly NXDOMAIN; exceptions: `exam` (59.91.192.229, NIB) and `uat` (103.139.159.141, Seans Media).
- `mycampus.jaipur.manipal.edu` and `testmycampus.jaipur.manipal.edu` keep CNAMEs to `edtech366.azurewebsites.net` whose terminal target is NXDOMAIN (dangling aliases).
- `uat.manipal.edu` is a labeled Azure Front Door route via `uat-ci-mahe-ep-bzgfhcehh0fvhafs.a01.azurefd.net` to 150.171.110.195.
- Group-wide `*.manipal.edu` CT completeness not achieved: crt.sh truncates the broad search to a random subset.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/ - primary target; A 98.70.14.50; parent/student login, Forgot Password, `@muj.manipal.edu`.
- https://muj.slcm.jaipur.manipal.edu/ - second live MUJ portal; A 20.244.94.89; MUJ Portal, Sign In, `@jaipur.manipal.edu`.
- https://slcm.manipal.edu/ - shared MAHE SLcM; A 104.211.226.160; IIS 10/ASP.NET, Microsoft AS8075; earliest Wayback capture 2020-11-18.
- https://sis.manipal.edu/studlogin.aspx - SIS for students/parents; A 218.248.47.25; AS9829; points fee payment to Fee Kart.
- https://api.manipal.edu/ - AWS EC2 43.205.223.7; nginx 1.18.0, Node.js, Express; root emits opaque JSON `data` field.
- https://lms.manipal.edu/ - D2L Brightspace via CNAME `learner-mahe.onlinemanipal.com` -> `manipalonline.brightspace.com`; A 15.134.178.12, 13.55.178.159.
- https://uat.manipal.edu/ - labeled UAT; CNAME via `uat-ci-mahe-ep-bzgfhcehh0fvhafs.a01.azurefd.net` to 150.171.110.195.
- https://uat.jaipur.manipal.edu/ - A 103.139.159.141 in Seans Media space; no claim on app state.
- https://exam.jaipur.manipal.edu/ - A 59.91.192.229 on National Internet Backbone space; exam-labeled.
- https://mycampus.jaipur.manipal.edu/ and https://testmycampus.jaipur.manipal.edu/ - CNAMEs to `edtech366.azurewebsites.net`; terminal target NXDOMAIN.
- https://dev.manipal.edu/ - A 4.247.242.9 (Microsoft space) but serves ordinary MAHE site with Apply Now, not a dev console.
- manipal.edu apex - Azure DNS NS `ns1-36.azure-dns.com/net/org/info`; A 18.160.46.89/123/45/127; MX `0 manipal-edu.mail.protection.outlook.com`.
- jaipur.manipal.edu apex - A 3.108.105.201 (AWS EC2 ap-south-1); MX `0 jaipur-manipal-edu.mail.protection.outlook.com`; no child NS delegation.
- https://webmail.jaipur.manipal.edu/ - CNAME chain into Microsoft 365/Outlook; high-confidence M365 webmail alias.
- https://webmail.manipal.edu/ - A 218.248.47.16 on NIB space; webmail-labeled endpoint, behavior untested.

## ACTIONABLE LEADS
- `mujerp.jaipur.manipal.edu` - ERP-labeled, CT starts 2025-04-11; report claims current A 20.244.0.229 but that is contradicted elsewhere (see FLAGS); verify DNS directly.
- `rms.jaipur.manipal.edu` - acronym host, claimed A 202.131.155.153 (also contradicted); `lcs`, `npfslcm`, `dms`, `dmsmuj`, `pms`, `idp` are NODATA/legacy; monitor for reactivation.
- `helpdesk.jaipur.manipal.edu` - fresh CT 2026-01-08 but NXDOMAIN today; watch for activation.
- https://hms.manipal.edu/ - A 20.44.49.205 Microsoft space; acronym meaning unstated, worth identifying.
- https://portal.manipal.edu/ - A 45.112.150.155; generic name, function unproven.
- `mujslcm.manipal.edu` (parent level, no jaipur) - A 202.131.155.151; purpose unproven, likely MUJ by label only.
- `exam.jaipur.manipal.edu` - live NIB-hosted exam endpoint; scope its content.
- `uat.manipal.edu` + `uat.jaipur.manipal.edu` - non-prod labels, both live; authorized testing only.
- `admissions.jaipur.manipal.edu` and `apply.jaipur.manipal.edu` - CT-validated names, NODATA now; old admission surfaces.
- `mycampus`/`testmycampus` dangling CNAMEs - confirm the Azure resource is gone before any action; report explicitly does not recommend claiming the target.

## FLAGS
- Internal contradiction: `mujslcm.jaipur.manipal.edu` (ref 85) and `muj.slcm.jaipur.manipal.edu` (ref 90) are listed with A records in the naming matrix and inventory, but as NOERROR/NODATA in the CT-to-DNS state table citing the same refs. Both cannot be right; re-verify with dns.google before trusting either table.
- Same pattern for `mujerp` (A 20.244.0.229 vs NODATA, both ref 96) and `rms` (A 202.131.155.153 vs NODATA, both ref 97).
- Report lists a fetched page for https://mycampus.jaipur.manipal.edu/ (ref 9, titled "Manipal University Jaipur") while also reporting its CNAME terminal target is NXDOMAIN; both cannot hold on the same day from the same resolver.
- All evidence is third-party and dated (Shodan observations 2026-08-18/22/23, DNS 2026-08-25); unverified until live re-check. Report self-assigns 0.35 confidence to acronym host purposes and 0.20 to group CT completeness.
- Wayback "earliest capture" (2020-11-18 slcm, 2025-05-27 mujslcm) is not a launch date; the report itself rejects launch-date claims.
- NOERROR/NODATA means only no A/CNAME answer; hosts may carry other record types. CT entries never prove ownership or current DNS.
- crt.sh `*.manipal.edu` search is truncated to a random subset; this report contains no exhaustive group list, so do not treat any group inventory as complete.
- Odd filler: report answers a "cot_explicit" chain-of-thought demand; template-reuse or prompt-injection residue, irrelevant to findings.
- No Censys evidence exists; report says public Censys pages yielded nothing and it did not manufacture data. Shodan banner versions may be stale or proxied.

## COVERAGE
- File read to EOF: 362 lines, 41643 chars (file_size 41643), truncated: false. Confirmed EOF at line 362 (final reference, ref 107).