# Digest: w2e-03-disclosure-case-studies.md

## REPORT
Source file: w2e-03-disclosure-case-studies.md (India's Thin University VDP Landscape: Lessons for MUJ)

## ANSWER SUMMARY
- IISc is the only verified first-party campus-wide Indian university VDP: wildcard *.iisc.ac.in, public APIs, mobile apps, no cash bounty.
- No surveyed university expressly names a student portal in a verified VDP; IISc portal coverage is an inference from the wildcard.
- IIT Kanpur C3i research is outbound disclosure to industrial OEMs, not an inbound campus program.
- SRM Sonepat's bug bounty is an offline educational competition with no named production target and no stated prize.
- HackerOne pages for Amrita and IIT Madras are external, community-moderated directory entries that deny affiliation and validation.
- CERT-In RVDCP coordinates and may credit finders but gives no safe harbor and no blanket testing permission.
- MUJ publishes no conforming security.txt at the standard location (portal sign-in returned) and no labeled security channel; it.support@jaipur.manipal.edu is IT Infrastructure only.
- Recommended first move: governance request for written scope, then a proposed MUJ VDP modeled on IISc.

## KEY FACTS
1. https://iso.iisc.ac.in/wp-content/uploads/2025/08/RVDP.pdf - IISc VDP policy: scope, exclusions, ciso@iisc.ac.in, 5-working-day acknowledgment, no cash reward.
2. https://www.cert-in.org.in/RVDCP.jsp - CERT-In RVDCP: 72-hour acknowledgment target, 120-day resolution window, no safe harbor.
3. https://mujslcm.jaipur.manipal.edu/.well-known/security.txt - checked RFC 9116 location returns the portal sign-in page, not a security file.
4. https://jaipur.manipal.edu/contact-university.php - MUJ contact table listing it.support@jaipur.manipal.edu, extensions 778 and 300.
5. https://www.rfc-editor.org/rfc/rfc9116.html - security.txt standard; Contact and Expires are required fields.
6. https://security.cse.iitk.ac.in/responsible-disclosure - C3i page tabling Rockwell and Schneider advisories; not a campus VDP.
7. https://unstop.com/competitions/bug-bounty-srm-university-delhi-ncr-sonepat-1647952 - SRM competition listing with no target, no prize amount, and a registration fee.
8. https://hackerone.com/amrita_university - Amrita directory page: no guidelines, community-moderated, unaffiliated.
9. https://hackerone.com/indian_institute_of_techn - IIT Madras directory page with the same explicit caveats.
10. https://hackerone.com/hacktivity/overview - Hacktivity feed: searchable report metadata, evidence only, not scope.
11. https://www.bugcrowd.com/products/vulnerability-disclosure/ - Bugcrowd VDP model and safe-harbor discussion for disclosure.
12. https://www.openbugbounty.org/faq/ - hosted programs versus generic non-intrusive reporting; platform pays no bounties.
13. http://yeswehack.com/programs - YesWeHack directory checked; no Indian university program verified in the snapshot.
14. https://hackerone.com/directory/programs - Directory context: presence is not authorization.
15. https://www.hackerone.com/bug-bounty-programs - HackerOne bounty program background page.

## ACTIONABLE LEADS
- Email MUJ IT Infrastructure asking whether a private VDP exists and who owns SLCM security intake; do not test while waiting.
- Draft a MUJ VDP on the IISc model: policy URL, valid security.txt, named assets, explicit portal status, prohibited techniques, response targets, safe-harbor wording.
- Have MUJ classify Akamai, M365 identity, payment services, parent login, APIs, and vendor backends before any scoped test.
- Use CERT-In only for post-discovery coordination, never as pre-authorization.
- Treat Hacktivity and Open Bug Bounty records for academic domains as disclosure history, not scope.

## FLAGS
- IISc portal coverage is a labeled inference; the policy excludes third-party services and automated-tool findings.
- SRM listing shows no target or prize; its registration fee is not a bounty.
- Amrita and IITM pages explicitly deny affiliation and validation.
- "Not found" for other universities is a survey result, not proof of absence; no authoritative national registry exists.
- The security.txt check is a single observed URL state; content may change.

## COVERAGE
Chars read: 35627. EOF confirmed: yes (truncation flag false on full read).