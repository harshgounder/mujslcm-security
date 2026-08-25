## REPORT (w2d-06-orientation-docs.md)
MUJ SLCM orientation and onboarding evidence. Official PDFs, pages, one header observation, one non-official repost. No authentication attempts. Verdict: onboarding workflow well documented; provisioning actor and timing, and default SLCM password, not publicly documented. 189 lines, 32453 chars, read to EOF, truncated: false.

## ANSWER SUMMARY
- The First-Year Student Profile Registration Guide says the Department of Admissions sends the SLCM username and password to the personal Gmail address supplied during admission. Delivery office and channel are documented; the technical account creator is not.
- No reviewed official artifact publishes a default SLCM password value. The FAQ says the password is aligned with the official Outlook ID; the guide says credentials are emailed by Admissions.
- No first-login SLCM password change is stated. The Office 365 SOP (v1.0, June 2025) explicitly documents a temporary-password flow and forced change for university email, plus mandatory MFA.
- Provisioning timing is not documented: when the SLCM or email account is created or activated is unknown; orientation reporting times (9:00 AM report, 9:15 AM verification) are physical events, not activation timestamps.
- A third-party header observation records HTTP 200, IIS/10.0, ASP.NET MVC 5.3, ASP.NET 4.0.30319, X-Powered-By ASP.NET. Akamai is not present in that record.
- The 2026 orientation page ties reporting, document verification, SLCM profile registration, and Office 365/Outlook help into one support path; support ownership is split between Admissions, SLCM support, and IT for Outlook.
- A College Sidekick repost mislabeled as BITS Pilani Goa is non-official, uploaded August 4 2024, and must not be treated as current MUJ policy.

## KEY FACTS
- http://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf - primary onboarding artifact: profile workflow, credential delivery via personal Gmail, non-editable admission-seeded fields, parent-mobile OTP for parent login.
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - registration link, username convention, password per official Outlook ID, DMS/AMS and IT Infra support routing.
- https://jaipur.manipal.edu/induction-orientation-program.php - 2026 orientation: reporting 9:00 AM, verification 9:15 AM, venues (Old Food Court, Smt. Vasanti R Pai Auditorium), help documents.
- https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf - v1.0 effective June 2025: temporary password, forced change, MFA mandatory, setup password policy (13+ chars), reset minimum (16 chars).
- https://mujslcm.jaipur.manipal.edu/ - public SLCM landing surface.
- https://mujslcm.jaipur.manipal.edu/Home/Index - portal surface with student identity hint, parent login, and a Microsoft password-reset destination in the HTML.
- http://api.hackertarget.com/httpheaders?q=https://mujslcm.jaipur.manipal.edu/ - point-in-time header fingerprint: Microsoft-IIS/10.0, MVC 5.3, ASP.NET 4.0.30319.
- https://www.collegesidekick.com/study-docs/16707539 - misattributed repost (BITS Pilani Goa label), August 4 2024 upload, historical only.
- https://jaipur.manipal.edu/img/pdf/Registration-Form.pdf - UG/PG registration form, related onboarding document.

## ACTIONABLE LEADS
- Catalogue onboarding artifacts with retrieval dates, titles, version or date metadata, and confidence classes; track revisions.
- Ask MUJ through official channels: account-lifecycle owner, activation timing definition, current SLCM and Office 365 onboarding documents, whether SLCM and Microsoft credentials are synchronized.
- Preserve the header observation as secondary evidence; do not use it to claim patch level or backend topology.
- Use the FAQ's username convention only to describe the pattern; never derive or guess real student identifiers.
- No credential guessing, no password-reset flows on accounts not owned, no route enumeration, without written scope.

## FLAGS
- The SLCM FAQ is undated; guide currency should be confirmed with Admissions before operational reliance.
- Passwords: do not infer a password formula from the Outlook-ID wording; sync, separate generation, and temporary-password interpretations all remain possible.
- Physical reporting and verification times are not account-activation times.
- The header record is third-party, point-in-time, and shows no Akamai; Akamai remains unverified, not proven absent.
- The College Sidekick document is externally hosted and misattributed; it is useful only as a lead for version comparison.
- The Microsoft reset link proves recovery affordance at the interface, not federation or credential-store sharing.

## COVERAGE
- File read to EOF: 189 lines, 32453 chars (file_size 32453), truncated: false. Confirmed EOF at line 189, final reference.