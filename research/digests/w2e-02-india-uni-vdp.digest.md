# Digest: w2e-02-india-uni-vdp.md

## REPORT
Source file: w2e-02-india-uni-vdp.md (MUJ SLCM Responsible Disclosure Playbook for India)

## ANSWER SUMMARY
- IT Act Sections 43 and 66 make authorization the hard boundary; written, asset-specific scope is required before any active validation.
- SLCM is documented as a single-window system for attendance, marks, results, and circulars, so confidentiality and exam integrity outrank technical curiosity.
- The detailed stack (ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai, M365) is a user-supplied premise, unverified by the report.
- 90 days is a coordination norm from Project Zero, not testing permission; publication must be negotiated separately.
- Indian reception varies: IIT Roorkee praised a 16-year-old finder, CBSE drew an alleged months-long silence, Zomato fixed in a day, IRCTC via CERT-In in seven days.
- CERT-In has two distinct roles: voluntary coordinated disclosure and the 2022 six-hour statutory incident duty, which does not name independent researchers.
- Severity needs two layers: a reproducible CVSS v4.0 vector plus an MUJ-specific impact statement.
- Recommended posture: policy design and passive OSINT now, no active testing until written authorization exists.

## KEY FACTS
1. http://indiacode.nic.in/bitstream/123456789/13116/1/it_act_2000_updated.pdf - IT Act text; Sections 43 and 66 define access, copying, alteration, and dishonest or fraudulent conduct.
2. https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf - six-hour incident reporting duty for specified organizations, not researchers.
3. https://www.cert-in.org.in/VulnerIncident.jsp - CERT-In voluntary coordination channel for researchers and academic institutions.
4. http://cert-in.org.in/RVDCP.jsp - CERT-In responsible disclosure and coordination policy.
5. https://projectzero.google/vulnerability-disclosure-policy.html - 90-day vendor window, 30-day post-patch disclosure, seven-day for active exploitation.
6. https://www.firstpost.com/tech/meet-the-16-year-old-who-spotted-and-fixed-a-jee-advanced-portal-flaw-before-cybercriminals-could-ws-e-14019184.html - IIT Roorkee JEE Advanced case: public praise plus disagreement over exposure scale.
7. https://www.ndtv.com/education/cbse-osm-portal-had-critical-vulnerabilities-ethical-hacker-told-ndtv-he-alerted-board-months-earlier-11550090 - CBSE researcher account of weak follow-up.
8. https://www.ndtv.com/education/cbse-admits-vulnerabilities-after-ethical-hacker-flags-alleged-exposure-11571388 - CBSE containment statement and thanks to ethical hackers.
9. https://www.thenewsminute.com/atom/zomato-hack-security-breach-its-system-not-first-time-user-information-was-compromised-62317 - Zomato reported one-day fix with post-fix publication.
10. https://certpro.com/irctc-data-breach - IRCTC insurance portal case: CERT-In report July 23, fix confirmed July 30.
11. https://www.cisa.gov/vulnerability-disclosure-policy-template - CISA model policy: 3-business-day acknowledgment, stop-on-sensitive-data rule, safe harbor for compliant work.
12. https://www.first.org/cvss/v4.0/specification-document - CVSS v4.0 bands and Base, Threat, Environmental, Supplemental metric groups.
13. https://whitehat.olacabs.com/ - Ola VDP as a first-party scope example excluding staging and sandbox.
14. http://mujslcm.jaipur.manipal.edu/ - target hostname; no public VDP or security.txt verified.
15. http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf - MAHE ICT document describing SLCM functions and high-impact records.

## ACTIONABLE LEADS
- Ask MUJ IT for a named security intake and written scope before any testing; escalate to CERT-In only for lawful coordination.
- Use the report template fields with a CVSS v4.0 vector plus an SLCM-specific impact statement.
- Propose a coordination clock: 3-business-day acknowledgment, 14-day triage, 45-day critical target, 90-day ceiling, separate publication decision.
- Track acknowledgment, technical confirmation, containment, and credit as four separate outcomes.
- Build stop conditions into club rules: stop at first sensitive record, unexpected privilege, or instability.

## FLAGS
- CBSE chronology is the researcher's claim; the board statement came later and no independent audit exists.
- Zomato and IRCTC accounts are secondary commercial or journalistic sources.
- Stack details remain unverified; do not base exploit selection on them.
- IT Act analysis is general risk guidance, not legal advice.
- The 90-day norm is a private research-team policy, not Indian law or MUJ policy.
- Reference list is noisy (Amity, Ricoh, Nokia, WHO, EFF, Red Hat entries), a possible deep-research artifact; treat body citations as the evidence core.

## COVERAGE
Chars read: 48255. EOF confirmed: yes (truncation flag false on full read).