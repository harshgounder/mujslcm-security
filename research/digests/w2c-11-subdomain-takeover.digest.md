# Digest: w2c-11-subdomain-takeover

## REPORT
Source file: w2c-11-subdomain-takeover.md (243 lines, 37007 bytes). Dangling DNS and subdomain takeover eligibility review for MUJ SLCM and admissions hosts.

## ANSWER SUMMARY
- mujslcm.jaipur.manipal.edu has a direct A record to 98.70.14.50 (TTL 3600), no CNAME answer, and serves a live MUJ portal; no dangling-CNAME pattern.
- admissions.jaipur.manipal.edu CNAMEs to jaipurmanipal.nopaperforms.com, resolving through prodvpc-web-lb4-593721465.ap-south-1.elb.amazonaws.com to three A addresses; official MUJ admissions page is live.
- NoPaperForms custom-hostname verification, quarantine, and release rules are not publicly documented; ownership must be confirmed in writing by vendor and MUJ.
- Akamai premise not established by current SLCM DNS; Akamai docs describe property hostname to edge hostname CNAME mapping, and the observed record is a direct A.
- No named Indian university takeover was substantiated from the public record; Abusix 2024 article supplies international analogues (UC San Diego, UCLA, Georgetown, UC Davis, Alicante, La Verne), all via expired external target domains.
- Provider controls differ: Azure asuid TXT and GitHub custom-domain verification reduce re-binding; Heroku frees custom domains on app destroy.
- Verdict: no present reportable takeover; residual risk is future offboarding and vendor lifecycle, plus DNS-first decommissioning gaps.

## KEY FACTS
- https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=A : direct A answer 98.70.14.50, TTL 3600.
- https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=CNAME : successful query, no CNAME answer.
- https://dns.google/resolve?name=admissions.jaipur.manipal.edu&type=CNAME : CNAME to jaipurmanipal.nopaperforms.com, TTL 2387.
- https://dns.google/resolve?name=admissions.jaipur.manipal.edu&type=A : chain terminates via AWS ELB at three addresses.
- https://admissions.jaipur.manipal.edu/ : live MUJ UG/PG/PhD admissions page for 2026-27.
- https://mujslcm.jaipur.manipal.edu/ : live portal with sign-in and parent login options.
- https://learn.microsoft.com/en-us/azure/security/fundamentals/subdomain-takeover : Azure dangling DNS definition and asuid TXT ownership control.
- https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages : disabled Pages site with DNS left in place is takeover risk.
- https://devcenter.heroku.com/articles/custom-domains : destroying an app frees its custom domains for reassignment.
- https://cheatsheetseries.owasp.org/cheatsheets/Subdomain_Takeover_Prevention_Cheat_Sheet.html : orphaned reference plus provider claimability are the two necessary conditions.
- https://abusix.com/blog/dangling-cname-attacks-and-sub-domain-takeovers : international higher-education analogues via expired target domains.
- https://hackerone.com/reports/665398 : datacafe-cert.starbucks.com Azure reclamation case, rated High 7.5, disclosed August 2019.
- https://dns.google/resolve?name=selector1._domainkey.jaipur.manipal.edu&type=CNAME : Microsoft 365 DKIM CNAME to mujcampus.onmicrosoft.com, a mail control, not a web app CNAME.
- https://cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf : covered entities report Annexure I incidents within six hours; legal category is counsel's call.
- https://techdocs.akamai.com/property-mgr/reference/modify-property-hostnames : documented property hostname to edge hostname mapping model.

## ACTIONABLE LEADS
- Ask NoPaperForms five control questions: ownership proof, competing tenant requests, tenant deletion behavior, quarantine or reservation, certificate/log/approval handling; get answers naming the MUJ tenant.
- Inventory all CNAME, NS, MX, and external registrable-domain dependencies under jaipur.manipal.edu with owners and expiry.
- Enforce DNS-first decommissioning gate: remove DNS, wait TTL, then delete the resource.
- Retain Azure asuid and GitHub verification TXT records as long as hostnames are delegated; eliminate wildcard DNS.
- Monitor CNAME chains, response codes, certificate transparency, and content hashes; keep evidence packages ready for incident response.
- Do not register expired targets, create cloud resources, or publish proof content without written authorization.

## FLAGS
- Akamai, ASP.NET MVC 5.3, .NET 4.x, IIS 10 are user-supplied context, not verified in this DNS dataset.
- NoPaperForms controls are Unknown; absence of documentation is not proof of claimability.
- Indian takeover stories cited only from unattributed posts; do not repeat them as cases.
- Active DNS chain does not prove durable tenant reservation; only vendor and owner confirmation can.
- A valid certificate on a hijacked subdomain is possible; TLS is corroboration, not a verdict.

## COVERAGE
Chars read: 37007 (full file to EOF, truncated false).