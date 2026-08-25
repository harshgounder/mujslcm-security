# Digest: w3-02-uat-manipal.md

## REPORT
Source file: /home/liebert511/mujslcm-recon/research/w3-02-uat-manipal.md (AI deep-research output, claims UNVERIFIED). Topic: exposure of `uat.manipal.edu` in the MUJ SLCM ecosystem. Passive sources observed 2026-08-25.

## ANSWER SUMMARY
- Application identity: the UAT shell is a MAHE institutional/marketing frontend (MAHE logo, programmes, campuses, Apply Now) with a branded Error 500 fallback; it does not publicly mirror MUJ SLCM or MAHE SLCM.
- Frontend markers `/_next/image` and `/_next/static` indicate a Next.js deployment, not the supplied ASP.NET MVC/IIS baseline; threat models must stay separate.
- Azure Front Door is confirmed: CNAME to `uat-ci-mahe-ep-bzgfhcehh0fvhafs.a01.azurefd.net`; anycast makes the supplied 150.171.110.195 versus current resolver 150.171.109.183 compatible, not contradictory.
- Archive presence is extensive: 1,811 successful CDX rows, 1,322 unique URLs, 2022-12-07 to 2023-10-02; historic content stays discoverable.
- No public secret leak found: generic Error 500 only, no stack traces, config files, or source-map names in the reviewed CDX inventory; bounded negative result.
- `robots.txt` disallows all crawlers while `sitemap.xml` returns the HTML app shell instead of XML; crawler policy is not access control.
- Microsoft guidance drives the main risk question: origins should reject non-Front-Door traffic (service tag `AzureFrontDoor.Backend` plus `X-Azure-FDID` check, or Private Link on Premium); origin isolation is unknown and owner-side.
- Verdict: High confidence in edge and app identity, Moderate in the bounded no-leak claim, Low for production-data status; risk rated Medium, escalating conditionally.

## KEY FACTS
- https://dns.google/resolve?name=uat.manipal.edu&type=CNAME - CNAME to `uat-ci-mahe-ep-bzgfhcehh0fvhafs.a01.azurefd.net`.
- https://dns.google/resolve?name=uat.manipal.edu&type=A - resolver chain through Front Door to 150.171.109.183.
- https://uat.manipal.edu/ - MAHE-branded shell, title "Top Higher Education Institution in India | Manipal University (MAHE)".
- https://uat.manipal.edu/sitemap.xml - returns branded HTML/error shell rather than an XML sitemap.
- https://uat.manipal.edu/mu.html - branded Error 500 body, `Apply Now` pointing to apply.manipal.edu.
- https://uat.manipal.edu/robots.txt - `User-agent: * Disallow: /`.
- https://crt.sh/?q=uat.manipal.edu - dedicated UAT certificates logged for 2025 and 2026, hostname actively maintained.
- https://web.archive.org/cdx/search/cdx?url=uat.manipal.edu%2F*&output=json&filter=statuscode%3A200&fl=timestamp%2Coriginal%2Cstatuscode%2Cmimetype%2Cdigest&collapse=digest - 1,811 rows / 1,322 unique URLs, Dec 2022 to Oct 2023.
- https://learn.microsoft.com/en-us/azure/frontdoor/origin-security - requires service-tag filtering plus profile-specific X-Azure-FDID validation for public origins.
- https://learn.microsoft.com/en-us/azure/frontdoor/private-link - Front Door Premium alternative so origins need no public address.
- https://learn.microsoft.com/en-us/azure/frontdoor/front-door-overview - Microsoft states Front Door is a global anycast CDN.
- https://mujslcm.jaipur.manipal.edu/Home/Index - MUJ portal "WELCOME TO MUJ PORTAL", sign-in and parent login.
- https://slcm.manipal.edu/ - MAHE SLCM "MU SLcM Sign in to your account".
- https://manipal.edu/mu/academics/student-portal.html - MAHE public student portal page linking to sis.manipal.edu/index.aspx.
- http://uat.manipal.edu/muj/admission/international-students/how-to-apply.html - historical UAT admissions route, supports the marketing-staging read.

## ACTIONABLE LEADS
- Owner-side proof of origin isolation: Private Link approval or combined service-tag plus X-Azure-FDID verification; treat origin bypass as the top control question.
- Classify UAT datastores and integrations; map data lineage for CMS content, forms, CRM connectors, and test accounts before any data claim.
- Fix routing anomalies: correct status codes at /sitemap.xml, monitor the branded 500 fallback, document robots.txt as crawler guidance only.
- Track CT and DNS for uat.manipal.edu; plan promotion or decommission with cache, certificate, and archive-aware review.
- Keep two models in club work: Next.js institutional UAT behind Front Door versus authenticated student-lifecycle hosts; do not merge.

## FLAGS
- Supplied IP 150.171.110.195 versus observed 150.171.109.183: report treats as anycast variance; no migration proven either way.
- CDX counts were computed locally from one provider response; no independent census.
- Origin hostname and address not present in public evidence; bypassability is unknown.
- No public evidence of production student data; absence of a leak is not proof of clean data separation.
- Next.js classification is an inference from asset paths, high confidence but not owner-confirmed.
- robots.txt disallow is voluntary crawler policy, not authorization.
- No-leak, no-source-map, no-config findings are bounded reviews, not exhaustive.
- All claims rest on AI deep-research output; treat every citation as unverified until rechecked.

## COVERAGE
36,195 chars read on disk (wc -m), 243/243 lines, single read pass, final page returned truncated=false, EOF confirmed; file_size 36195 bytes.