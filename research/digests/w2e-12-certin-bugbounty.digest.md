# Digest: w2e-12-certin-bugbounty

## REPORT
Source file: w2e-12-certin-bugbounty.md (Reporting MUJ SLCM Vulnerabilities Through CERT-In)

## ANSWER SUMMARY
- Use two parallel tracks: a confidential notice to MUJ IT and Registrar, plus a direct RVDCP report to vdisclose@cert-in.org.in. Do not wait for a publicly listed nodal officer; none was found.
- Three clocks differ: 72 working hours for acknowledgement, 120 days from initial vendor contact as a resolution target, and six hours for covered entities to report Annexure I incidents. Do not conflate them.
- The researcher route is email-based; the linked certinvulnform.pdf returned "requested URL is not found", so submit the RVDCP field list by email, PGP-encrypted when sensitive.
- RVDCP offers no safe harbor; it requires lawful conduct and leaves the finder responsible. Stop at minimum lawful evidence; no scanning or exploitation without written authorization.
- MUJ public channels: it.support@jaipur.manipal.edu, registrar@jaipur.manipal.edu (Dr Amit Soni, +91 141-3999100, extension 102), registrar.office@jaipur.manipal.edu, admin.office@jaipur.manipal.edu. No public security mailbox or CERT-In PoC found.
- Route by ownership: MUJ for application and configuration defects, MSRC only for demonstrable Microsoft product flaws, security@akamai.com only for Akamai platform defects.
- NCRP and helpline 1930 are cybercrime lanes, Chakshu handles fraudulent communications, TRAI handles spam; none is a vulnerability lane.
- The MAHE information-security policy must not be presented as MUJ's disclosure policy without MUJ confirmation.

## KEY FACTS
1. https://cert-in.org.in/RVDCP.jsp - RVDCP policy page; fields, 72-hour acknowledgement, 120-day target.
2. https://www.cert-in.org.in/PDF/RFC2350.pdf - CERT-In RFC 2350 contact lanes: vdisclose@, incident@, info@.
3. https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf - 2022 Directions; six-hour reporting, PoC duty, 180-day logs.
4. https://www.cert-in.org.in/PDF/certinvulnform.pdf - linked vulnerability form PDF, observed not found at research time.
5. http://jaipur.manipal.edu/contact-university.php - MUJ contact page with IT Infrastructure and Registrar Office channels.
6. https://www.jaipur.manipal.edu/administration-registrar.php - Registrar page; Dr Amit Soni, registrar@, phone extension 102.
7. https://msrc.microsoft.com/report/vulnerability - MSRC Researcher Portal for Microsoft product defects.
8. https://www.microsoft.com/en-us/msrc/faqs-report-an-issue - MSRC guidance; one-business-day receipt, configuration findings often excluded.
9. https://www.akamai.com/global-services/support/vulnerability-reporting - Akamai reporting channel, security@akamai.com.
10. http://jaipur.manipal.edu/about-muj.php - MUJ self-description as a self-financed State Private University.
11. https://www.manipal.edu/mu/policies/it-policy/information-security-policy.html - MAHE information security policy; separate from MUJ unless confirmed.
12. http://i4c.mha.gov.in/ncrp.aspx - NCRP cybercrime complaint lane.
13. http://sancharsaathi.gov.in/ - Chakshu lane for fraudulent calls, SMS, WhatsApp; not for cybercrime.
14. http://trai.gov.in/complain-or-report-against-ucc - TRAI unsolicited communication complaint lane.
15. https://www.jaipur.manipal.edu/mandatory-disclosure.php - mandatory disclosures page, context for MUJ statutory claims.

## ACTIONABLE LEADS
- Send the sanitized report to it.support@ and registrar@ with registrar.office@ as fallback; ask for forwarding to security, legal/privacy, and the CERT-In PoC.
- Submit the same report to vdisclose@cert-in.org.in following RVDCP fields; ask for acknowledgement and a case reference.
- For suspected Annexure I events, alert MUJ by phone and use the incident@ lane; do not impersonate MUJ's authorized officer.
- Preserve only redacted evidence: no cookies, tokens, credentials, grades, or student identifiers.
- Use the provided report envelope template (subject, classification, timing, prior disclosure, researcher preference).
- Ask MUJ to name an authorized security owner and a secure follow-up channel; treat IT/Registrar as forwarding points only.
- Do not retest, publish, or expand scope without written agreement and coordinated approval.

## FLAGS
- Whether the 2022 Directions apply to MUJ is not legally resolved in the report; MUJ counsel should confirm applicability.
- certinvulnform.pdf failure is a transient availability observation; email remains the reliable mechanism.
- Registrar and IT Infrastructure are documented escalation points, not confirmed members of MUJ's security team.
- The MAHE information security policy applies to MAHE assets; presenting it as MUJ policy would create false assurance.
- No safe harbor exists; all steps assume lawful minimal observation already performed.
- High confidence applies to CERT-In primary-source facts; moderate confidence applies to internal MUJ routing.

## COVERAGE
- Chars read: 45,129
- EOF confirmed: yes (truncated: false on final page, 336 of 336 lines)