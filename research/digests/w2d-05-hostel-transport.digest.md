## REPORT (w2d-05-hostel-transport.md)
MUJ SLCM hostel and transport artifacts: public exposure and privacy risk. Public pages, regulations, and defensive guidance only. Verdict: no MUJ allotment or transport rosters located publicly; privacy-risk review supported. 181 lines, 31510 chars, read to EOF, truncated: false.

## ANSWER SUMMARY
- Repeated searches located no MUJ-specific public allotment list with student names and register numbers, and no student transport route roster. This is a bounded negative finding, not proof of absence behind login or in unindexed channels.
- Hostel rules are public: allotment after fee payment on a first-come-first-served basis; room changes only in exceptional circumstances with prior Chief Warden permission.
- Public facility and fee data: twin-sharing rooms, 10,000+ beds, flap-barrier access control; 2026-27 double-occupancy fee INR 167,372 plus housekeeping INR 15,378 and refundable deposit INR 25,475; forfeiture on late non-payment.
- Transport public data is campus access only: Dehmi Kalan address, Jaipur bus stand 25 km, railway station 24 km, airport 27 km. No shuttle routes, stops, or timetables were located.
- Under DPDP Act definitions, a PDF joining name, register number, room, and route would be personal-data processing, not a neutral notice.
- CERT-In Directions require covered entities to report listed incidents within six hours and keep ICT logs for a rolling 180 days in India.
- Recommended publication model: individual portal views, expiring links, pseudonymous references, aggregate vacancy statistics; no public name plus register number plus room or route combinations.

## KEY FACTS
- https://jaipur.manipal.edu/hostel-facility.php - allotment rule: fee payment, first-come-first-served, Chief Warden permission for changes.
- https://jaipur.manipal.edu/room-description.php - double-seater rooms, beds, wardrobes, study furniture, universal sockets.
- https://jaipur.manipal.edu/hostel-overview.php - separate boys' and girls' blocks, 10,000+ beds, flap-barrier access control.
- https://jaipur.manipal.edu/hostel-fees.php - 2026-27 fee breakdown, confirmation after full fee receipt, forfeiture terms, refund rules with INR 5,000 processing deduction.
- https://jaipur.manipal.edu/mess-fees.php - mess charge INR 79,000, two-month allotment windows, revision notice language.
- https://jaipur.manipal.edu/faqs-regarding-hostel.php - annual vacancy for maintenance, possible same-room continuity, allocation-day luggage help.
- https://jaipur.manipal.edu/chiefwardensmessage.php - 24-hour security and medical facility, Wi-Fi, mess, gym.
- https://www.jaipur.manipal.edu/contact-university.php - campus location and intercity distances; no shuttle data.
- http://manipal.edu/mu/important-links/privacy-and-cookie-policy.html - MAHE policy: data categories, sharing, retention, 30-day grievance window.
- https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf - DPDP Act text: personal data, processing definition, breach definition, rights (sections 11-13).
- http://pib.gov.in/PressReleasePage.aspx?PRID=2190655 - DPDP Rules 2025 notified November 14 2025.
- https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf - six-hour incident reporting, 180-day log retention, time synchronization.
- https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html - least privilege, deny-by-default, server-side permission validation.
- https://owasp.org/www-project-application-security-verification-standard - ASVS as the control baseline reference.
- https://www.hilliardschools.org/departments/transportation/busstop - comparative design: individualized route login instead of public roster (not MUJ policy).

## ACTIONABLE LEADS
- Build a synthetic artifact inventory with fake names, register numbers, rooms, and routes; never collect or redistribute real student PII.
- Request an authorized non-production review: role matrix, publication workflow, room-change and transport assignment workflows, retention schedule, incident contacts.
- Propose a two-tier publication model: public policy tier, private individual-view tier with staff aggregate dashboards.
- Run a pre-publication privacy review checklist: identifiability, residence or movement disclosure, field necessity, less identifying alternatives, audience limits, link expiry, cacheability.
- If a real public document is found, notify MUJ through its privacy or security contact and do not redistribute it.

## FLAGS
- Negative search findings are medium confidence for the corpus, low confidence for universal absence.
- Stack labels (ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai, Microsoft 365) are not independently verified in this report.
- The MAHE privacy policy is institutional, not MUJ-specific in every operational detail.
- DPDP Rules were notified November 14 2025; the report does not claim uniform commencement or enforcement status.
- Reference 8 is a Gazette PDF with garbled title text; legal claims are cited from it and need counsel confirmation.
- The Hilliard City Schools example is comparative only.

## COVERAGE
- File read to EOF: 181 lines, 31510 chars (file_size 31510), truncated: false. Confirmed EOF at line 181, final reference.