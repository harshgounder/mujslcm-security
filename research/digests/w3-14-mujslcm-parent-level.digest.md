# Digest: w3-14-mujslcm-parent-level.md

## REPORT
Source file: w3-14-mujslcm-parent-level.md (MUJ SLCM hostname attribution and exposure report)

## ANSWER SUMMARY
- Parent mujslcm.manipal.edu resolves to 202.131.155.151 (A only, TTL 300). No AAAA, CNAME, HTTPS, TXT, MX, or NS answers appear in queried responses.
- The Jaipur child mujslcm.jaipur.manipal.edu is the officially documented SLCM registration link in the MUJ FAQ.
- Child scans across Nov 2024, Jan 2026, Jun 2026 return HTTP 200 with x-aspnetmvc-version 5.3, x-aspnet-version 4.0.30319, Microsoft-IIS/10.0 (IIS 8.5 in 2024), IP 98.70.14.50 (202.131.155.150 in 2024).
- Akamai is not demonstrated in any public scan. Observed network is Microsoft IIS and AS8075.
- A passwordreset.microsoftonline.com link titled "Forgot Password?" exists on the child; that is Microsoft-linked recovery, not proof of Microsoft 365 federation.
- Parent has zero URLScan results, zero Wayback captures, empty Certificate Spotter result. Child has Wayback 200 captures from 2025-01-10 and 2025-05-27.
- Verdict: parent is an unattributed DNS-present asset, best working hypothesis orphaned or legacy infrastructure; not proven to be old SLCM, backup, alias, or squat.

## KEY FACTS
- https://dns.google/resolve?name=mujslcm.manipal.edu&type=A - parent A record 202.131.155.151.
- https://dns.google/resolve?name=mujslcm.manipal.edu&type=AAAA - no AAAA answer, only SOA authority for manipal.edu.
- https://urlscan.io/api/v1/search/?q=domain:mujslcm.manipal.edu&size=100 - parent URLScan results: [], total 0.
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - first-party source naming mujslcm.jaipur.manipal.edu as the SLCM registration link.
- https://urlscan.io/result/019ed038-c4af-765c-9499-2da69a77e30a/ - Jun 2026 scan: MVC 5.3, ASP.NET 4.0.30319, IIS 10.0, 98.70.14.50.
- https://urlscan.io/result/019bc028-d1ec-72f5-b0df-647554467edb/ - Jan 2026 scan: IIS 10, AS8075, Forgot Password link to Microsoft.
- https://urlscan.io/result/17a4443c-7b48-46f7-9b83-c207114b958f/ - Nov 2024 scan: port 122, HTTP 200, IIS 8.5, 202.131.155.150.
- https://web.archive.org/cdx/search/cdx?collapse=urlkey&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&output=json&url=mujslcm.jaipur.manipal.edu/* - child 200 captures 20250527044058 and 20250110135954.
- https://api.hackertarget.com/reversedns/?q=202.131.155.151 - parent reverse DNS maps to convergentindia.com naming.
- https://api.hackertarget.com/reversedns/?q=202.131.155.150 - sibling historical address maps to the same Convergent India pattern.
- https://slcm.manipal.edu/ - separate MAHE-branded portal, not usable as MUJ parent evidence.
- https://crt.sh/?q=mujslcm.manipal.edu&output=json - returned 404; treat as unavailable query, not proof of certificate absence.
- https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-framework - .NET Framework 4.0 end of support 2016-01-12; header alone does not prove runtime.
- http://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf - NIST CSF 2.0 inventory requirements behind the governance recommendation.
- https://www.cisa.gov/resources-tools/resources/secure-by-design - owner accountability guidance for reducing exposure.

## ACTIONABLE LEADS
- Owner-side: reconcile DNS zone records, certificates, load balancer and CDN configs, and CMDB entries for both hostnames.
- Classify the parent as "unattributed - DNS present - application and ownership unconfirmed" in the asset register.
- Passive follow-up: re-check parent HTTP/HTTPS reachability and certificate issuance over time; do not fuzz or probe.
- If the parent is retired, remove stale DNS and certificates after dependency review; if required, publish an owner-approved canonical URL.
- Do not copy the child's MVC/IIS fingerprint onto the parent; the parent has no recovered application fingerprint.

## FLAGS
- Child moved from 202.131.155.150/IIS 8.5 (2024) to 98.70.14.50/IIS 10 (2026); observed change, not proof of migration.
- .150/.151 adjacency and shared reverse-DNS naming are suggestive only; not proof of common ownership.
- The Akamai assertion from the supplied research brief is unverified by every cited public source.
- Header 4.0.30319 is not proof of exact .NET Framework release; Microsoft lists 4.0 as EOL 2016-01-12.
- Reference 24 (learn.microsoft.com ASP.NET MVC overview) returned 404; dead reference in the report.
- Report is AI deep-research output; all claims need independent verification.

## COVERAGE
Read 34,839 chars (201 lines), single pagination pass, EOF confirmed (truncated false).