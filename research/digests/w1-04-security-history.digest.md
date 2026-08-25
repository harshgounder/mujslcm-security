## REPORT (w1-04-security-history.md: Manipal SLCM Security History: Evidence, Gaps, and Risk)

## ANSWER SUMMARY
- No confirmed breach of slcm.manipal.edu or mujslcm.jaipur.manipal.edu in the public record reviewed through August 25, 2026; claims that "SLCM was breached" are unsubstantiated.
- The only concrete leak allegation is Brinztech's February 18, 2026 claim of a Manipal Library Portal database release; it names no SLCM system, supplies no forum URL, dataset hash, record count, or MAHE confirmation, and says no student credentials appeared in the data.
- LeakRadar reports 59,820 leaked credentials associated with manipal.edu; the provider's own FAQ says domain-associated records do not mean the organization's infrastructure was breached (stealer logs, Telegram, dark-web, forum sources are common).
- HIBP domain search requires verified domain ownership (unverified returns HTTP 403); DeHashed exposed no target-specific result; both are inconclusive without authorized queries.
- No product-specific CVE for SLCM or the named hosts was found in NVD, CVE.org, Exploit-DB, or VulDB; NVD query URLs fell back to the full corpus (382,361 records) and unrelated Chrome CVEs, so the absence evidence is weak.
- Four Reddit reliability complaints (INR 487,000 fee pending after deduction, correct password rejected, fee module absent for one eligible user, old and new registration numbers rejected) are Tier 3 complaints with no attacker evidence.
- URLScan has seen slcm.manipal.edu twice with no malicious or phishing verdict; mujslcm.jaipur.manipal.edu was "not observed"; no verifiable phishing clone surfaced in PhishTank or OpenPhish.
- Testing boundaries are real: CERT-In Directions 70B require 6-hour incident reporting and 180-day in-India log retention for covered entities; IT Act Sections 43/66 make unauthorized access and extraction criminal (up to 3 years and INR 500,000 fine).

## KEY FACTS
- https://leakradar.io/en/report/manipal.edu - 59,820 domain-associated credential records; provider caveat blocks breach attribution.
- https://www.brinztech.com/breach-alerts/brinztech-alert-database-of-manipal-library-portal-leaked/ - the February 2026 library leak allegation; single unconfirmed secondary source.
- https://libportal.manipal.edu/ - library portal in the alleged leak; designed and maintained by MAHE Department of Digital and Information Technology.
- https://slcm.manipal.edu/ - MAHE SLCM target; URLScan seen twice, no malicious verdict.
- https://mujslcm.jaipur.manipal.edu/ - MUJ target host; not observed in URLScan.
- https://urlscan.io/domain/slcm.manipal.edu - host associated with Microsoft ASN AS8075 and IPv4 104.211.226.160; no phishing verdict.
- https://urlscan.io/domain/mujslcm.jaipur.manipal.edu - "Not observed"; no direct or incoming hits; inconclusive, not a safety rating.
- http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf - official document showing SLCM handles attendance, marks, result publication, broadcasts (high-integrity functions).
- https://haveibeenpwned.com/API/v3 - HIBP domain search is authenticated and plan-dependent; unverified domains get HTTP 403.
- https://dehashed.com/ - no target-specific Manipal result in accessible public material; inconclusive.
- https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf - mandatory 6-hour incident reporting and 180-day log retention for covered entities.
- https://www.indiacode.nic.in/bitstream/123456789/13116/1/it_act_2000_updated.pdf - IT Act Section 43/66 text defining unauthorized access and extraction penalties.
- https://www.cert-in.org.in/RVDCP.jsp - CERT-In responsible disclosure coordination policy; no Manipal-specific safe harbor.
- https://www.manipal.edu/mu/about-us/grievances.html - official grievance route with Ombudsman; no security-incident contact exposed.
- https://nvd.nist.gov/vuln/search/results?form_type=Basic&results_type=overview&query=Manipal&search_type=all&isCpeNameSearch=false - NVD query fell back to the unfiltered corpus; do not cite NVD absence as proof.

## ACTIONABLE LEADS
- Authorized identity investigation: MAHE/MUJ should run HIBP, DeHashed, and LeakRadar source-level queries under verified ownership, deduplicate identities, expire exposed passwords, revoke sessions, and correlate with SLCM sign-in logs.
- Library leak validation: preserve application, API, database, identity-provider, and export logs around February 18, 2026; obtain any sample through counsel or CERT-In, hash it, and compare against libportal schema; search for unusual export activity on that date.
- Origin-exposure check: slcm.manipal.edu sits on Azure IP 104.211.226.160; the target is Akamai-fronted, so test whether the origin answers directly on that IP with a Host header, bypassing WAF.
- Review libportal.manipal.edu for CMS/API endpoints and keys in public JavaScript; it is the only host with a concrete (alleged) incident.
- Set up brand monitoring: certificate transparency, lookalike domains, and fake "fee pending" campaigns; the INR 487,000 complaint shows the social-engineering hook. Preserve any clone as URL, screenshot, headers, timestamp, transaction destination before takedown.
- Disclosure path: use CERT-In RVDCP coordination plus MAHE's grievance route; push MAHE to publish a security.txt and a named security contact.
- Operational fixes implied by complaints: expose transaction IDs and expected posting times in fee workflows; end-to-end identity-lifecycle monitoring for registration changes; step-up auth and dual control for mark, result, and fee changes.
- Reddit threads identify affected populations for outreach; do not use them as test accounts.

## FLAGS
- Brinztech article is Tier 2: publication is verified, event is not. No hash, count, forum URL, or victim confirmation.
- 59,820 is domain-associated, not 59,820 stolen SLCM accounts; the report itself warns against the stronger claim.
- All four Reddit complaints are Tier 3 first-person reports; none demonstrates cyberattack.
- "No CVE found" is a bounded search result; NVD UI failures and dynamic Exploit-DB pages make the negative weak. Do not repeat as "platform has no vulnerabilities".
- URLScan "not observed" for the MUJ host is an absence in one index, not a security rating.
- HIBP absence claims are invalid without verified domain access; an outside researcher cannot certify the domain as clean.
- Display ages ("1y ago", "2mo ago", "3y ago") are approximate; do not quote as exact incident dates.
- PhishTank/OpenPhish checks were search-index based; authenticated or per-URL API lookups may find records the static search missed.

## COVERAGE (40265 chars as read, read verified to EOF, 284 lines)