# Digest: w2f-10-ct-cert-patterns.md

## REPORT
Source file: w2f-10-ct-cert-patterns.md (MUJ SLCM Certificate Transparency Exposure and Defensive Priorities)

## ANSWER SUMMARY
- Two live naming conventions exist in CT and public pages: `mujslcm.jaipur.manipal.edu` and `muj.slcm.jaipur.manipal.edu`. Distinct DNS names, both active as of 2026-08-25 with current Entrust certificates.
- `mujslcm` exact-name query returns 10 unique serials, 9 expired, one current (Entrust DV, valid to 2026-12-21). Six certs cluster around December 22-23, 2024, likely reissues or managed rollover, not malicious issuance.
- `muj.slcm` has 4 serials, one current (valid to 2026-12-22), issued same day as the mujslcm cert by the same Entrust DV CA, suggesting coordinated renewal.
- Nine expired wildcards `*.jaipur.manipal.edu` span 2020-05-07 to 2023-12-16, issued by Amazon CAs. Wildcard retirement needs internal verification.
- Test-labeled names seen: five `testmycampus`, one `testerp`, plus `npfslcm` as an SAN beside `mujslcm` on serial 540dddb8fc45abd142751ef840ba2878. Labels prove issuance, not environment status.
- Cross-family SAN grouping pairs Jaipur wildcard SANs with CNs `*.manipalglobal.com`, `*.manipaldubai.com`, `manipal.edu`, `apply.manipal.edu`. Grouping is an inference, not proof of compromise.
- Verdict: High confidence in CT facts, Medium-Low for cluster explanations. CT shows governance sprawl, not a demonstrated vulnerability.

## KEY FACTS
- https://crt.sh/?q=%25.jaipur.manipal.edu&output=json - Family snapshot with 27 name strings, wildcard history, cross-domain SANs. Core evidence source.
- https://crt.sh/?q=mujslcm.jaipur.manipal.edu&output=json - Exact-name query, 10 serials including the December 2024 cluster and current 2026 cert.
- https://crt.sh/?q=slcm.manipal.edu&output=json - Legacy `slcm.manipal.edu` history, 9 serials, 5 with CN `sis.manipal.edu`.
- https://mujslcm.jaipur.manipal.edu/Home/Index - Portal page showing WELCOME TO MUJ PORTAL branding.
- https://muj.slcm.jaipur.manipal.edu/ - Dotted-name portal, also shows MUJ PORTAL branding, public identity of the parallel name.
- https://slcm.manipal.edu/ - Legacy MU SLcM page, lineage link to the current names.
- https://letsencrypt.org/docs/ct-logs/ - CT definition and append-only submission requirement from a CA.
- https://certificate.transparency.dev/logs/ - Official CT log directory, grounds the monitoring approach.
- https://www.digicert.com/faq/public-trust-and-certificates/what-are-ct-logs - DigiCert explanation of CT as public auditable issuance record.
- https://developers.cloudflare.com/ssl/edge-certificates/additional-options/certificate-transparency-monitoring/ - Documented CT monitoring limits: shared-cert alerts, no lookalike detection.
- https://www.nccoe.nist.gov/tls-server-certificate-management - NIST TLS cert management guidance, basis for the 8-stage workflow.
- https://www.nccoe.nist.gov/publication/1800-16/VolA/index.html - NIST SP 1800-16 volume on certificate management, inventory and monitoring emphasis.
- https://letsencrypt.org/docs/challenge-types/ - DNS-01 wildcard issuance and API credential risk guidance.
- https://crt.sh/?q=testmycampus.jaipur.manipal.edu&output=json - Returns 404 Not Found title in references, yet data is used in the testmycampus table.
- https://crt.sh/?q=npfslcm.jaipur.manipal.edu&output=json - Also titled 404 Not Found in references while npfslcm appears as an SAN elsewhere.
- https://crt.sh/?q=testerp.jaipur.manipal.edu&output=json - Titled 404 Not Found while the testerp serial is presented as evidence.
- https://www.rfc-editor.org/rfc/rfc9162 - RFC 9162 CT v2, standards anchor for log behavior.

## ACTIONABLE LEADS
- Reconcile all 10 mujslcm serials against Entrust order history and internal deployment records; unknown serials become certificate-governance incidents.
- Decide the canonical relationship between `mujslcm` and `muj.slcm`; both are current, same-day issued, one-day-differing expiry.
- Verify retirement of the nine wildcards and the `testmycampus`, `testerp`, `npfslcm` names through CA accounts, CMDB, DNS, load balancers, and repos.
- Check whether the 2022 `dms.jaipur.manipal.edu` CN with mujslcm SAN implies shared infra; confirm from deployment records.
- Assign ownership to all 27 observed name strings: current, retired, alias, third-party, unknown.
- Set up continuous CT monitoring with a normalization and serial-dedup step; alert on unknown issuer, new label, or unusual SAN grouping. Report anomalies to MUJ's security contact, never attempt revocation.
- Disclosure step: submit findings through MUJ's approved security-reporting channel only.

## FLAGS
- Contradiction: several crt.sh reference URLs are titled "404 Not Found" while the report still cites their data; results may have been collected earlier and links re-fetched later. Data provenance is weakened.
- Unverified: all cluster and grouping explanations are labeled inference; CT cannot show cause.
- Suspicious claim: same-day issuance of both current certs implies coordination, but this is inference pending CA orders.
- Hallucination risk: serials and dates are specific and internally consistent across tables, but the report is AI deep-research output; treat every serial as needing independent crt.sh re-query before use.
- The claim "five testmycampus serials" depends on the family snapshot; collection date and dedup method are stated but not reproducible inline.
- Cross-domain SAN pairs (manipalglobal, manipaldubai) are presented as fact of grouping; intent remains unknown.
- Verdict label "no demonstrated vulnerability" should keep scope: CT alone cannot prove reachability of any listed name.

## COVERAGE
- Chars read: 38419
- EOF confirmed: true (read_file truncated=false, 318 lines)