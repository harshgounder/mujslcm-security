# Digest: w2e-01-india-uni-breach-history.md

## REPORT
Source file: w2e-01-india-uni-breach-history.md (Indian University Portal Incidents: Lessons for MUJ SLCM)

## ANSWER SUMMARY
- Dominant risk class in 7 core Indian university incidents is privileged identity and trusted workflow abuse (4 of 7 cases), not confirmed IDOR or exposed APIs.
- Marks tampering recurred: Bengaluru North (60+ students, registrar credentials, INR 15,000-20,000 per student), Bangalore University (55 students, reported OTP bypass), Gauhati (50+ students, outsourced data entry).
- IIT Roorkee exposure of 30,000+ records via enrollment number is BOLA-like by inference, not source-confirmed IDOR.
- Payment fraud spans fake receipt forgery (Sri Venkateswara University, INR 65,686) and look-alike domain diversion (Sai Nath Educational, INR 32,000).
- Disclosure outcomes are enforcement-led: 5 of 7 core cases reached police, none published a full technical postmortem.
- AIIMS Delhi is the strongest ransomware comparator: 5 of 140 servers infected, 3-4 crore patient records hosted, theft claims reported as baseless.
- CERT-In Directions 2022 impose a six-hour incident reporting clock and 180-day in-India log retention on covered entities.

## KEY FACTS
1. https://www.thehindu.com/news/national/karnataka/uucms-portal-of-bengaluru-north-university-hacked-and-marks-of-students-tampered-with/article68740901.ece - Bengaluru North marks tampering, registrar credentials, three arrests.
2. https://m.economictimes.com/news/new-updates/how-marks-of-55-bangalore-university-students-were-illegally-changed-inside-uucms-breach-thats-shaking-karnatakas-education-system/articleshow/122039174.cms - Bangalore University OTP bypass detail, restoration of original marks.
3. https://www.ndtv.com/india-news/gauhati-university-marsheet-scam-marksheet-tampering-scam-detected-at-assams-gauhati-university-6003115 - Gauhati cash-for-marks, 9 arrests, ITI Limited data entry end.
4. https://timesofindia.indiatimes.com/city/dehradun/iit-roorkee-data-breach-exposes-personal-details-of-30k-alumni/articleshow/123220043.cms - IIT Roorkee 30k+ records, enrollment-number retrieval, ~10 year exposure.
5. https://www.cyberx9.com/physicswallah-millions-students-defense-data-exposed-blog - explicit IDOR researcher account with disclosure timeline, adjacent comparator only.
6. https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization - OWASP BOLA definition; every object ID endpoint needs an entitlement check.
7. https://www.thehindu.com/news/national/andhra-pradesh/fake-fee-receipt-scam-unearthed-in-sv-university/article71041791.ece - SVU fake receipts with forged seals and signatures.
8. https://the420.in/sai-nath-university-fake-website-student-fraud-agra/ - look-alike domain payment diversion of INR 32,000.
9. https://indianexpress.com/article/cities/delhi/aiims-cyber-attack-at-least-five-servers-infected-have-data-of-3-4-crore-patients-8297028 - AIIMS ransomware comparator; infection without proven exfiltration.
10. https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf - six-hour reporting and 180-day log retention obligations.
11. https://www.csk.gov.in/documents/IndiaRansomwareReport2022.pdf - 53% year-over-year ransomware rise, offline backup and 3-2-1 guidance.
12. https://learn.microsoft.com/en-us/entra/fundamentals/security-defaults - Microsoft security defaults: MFA registration, admin MFA, legacy auth blocking.
13. https://www.deccanherald.com/india/gujarat-technological-university-system-hacked-1200-students-personal-data-leaked-867789.html - GTU 1,200 student identity data leak, root cause undisclosed.
14. https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf - DPDP Act text; penalty maxima of INR 250 crore and INR 200 crore.
15. http://mujslcm.jaipur.manipal.edu/ - target portal, public sign-in surfaces for institutional, parent, student users.

## ACTIONABLE LEADS
- Treat marks changes as financial-grade transactions for MUJ: dual approval, step-up auth, append-only audit, after-hours and bulk-change alerts.
- Use the UUCMS precedent to argue for registrar and exam-staff identity hardening, separate admin accounts, Controlled Access review.
- Test object authorization only with authorized synthetic accounts; never change identifiers against live data.
- Prebuild a canonical payment domain list, DMARC/SPF/DKIM posture, and domain monitoring for admission season.
- Rehearse the six-hour CERT-In reporting decision and 180-day log retention for SLCM identity, app, and payment logs.
- Run a tabletop ransomware scenario covering identity, SLCM, exams, payment reconciliation, and backups.

## FLAGS
- IIT Roorkee IDOR is analyst inference; the article does not name the flaw class.
- PhysicsWallah is a researcher's account about an education company, not an independently verified university case.
- AIIMS theft claims were reported as having no factual basis; infection does not equal exfiltration.
- SVU and Sai Nath outcomes are open cases and allegations, not adjudicated facts.
- Sample is purposive and media-selected; counts do not generalize to a national rate.
- No full technical postmortem exists for any core case; credential acquisition paths are unknown.
- Reference list contains uncited entries (femtosec.io, undercoverist.org items), a possible research-noise artifact.

## COVERAGE
Chars read: 46413. EOF confirmed: yes (truncation flag false on full read).