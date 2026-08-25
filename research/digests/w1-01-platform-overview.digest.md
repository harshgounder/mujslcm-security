## REPORT (w1-01-platform-overview.md)
## ANSWER SUMMARY
- SLCM is an authenticated student administration portal, not a proven LMS. No public MUJ source calls it a course-content or teaching platform.
- Public root shows username/password login, Student Login, Parent Login, Forgot Password. The form posts to /; Forgot Password exits to passwordreset.microsoftonline.com. This proves Microsoft credential linkage, not SAML/OAuth/Entra SSO.
- Documented onboarding chain: Office 365 activation, mandatory MFA, SLCM profile completion, two signed Student Profile Form copies, in-person document verification.
- Public feature evidence is uneven: attendance route exists and is login-gated; timetable and grades candidate routes return only the login page. Post-login screens are unproven.
- Payments split by purpose: academic fees enter via SLCM with processor undisclosed; hostel/mess goes to SpaceBasic; a mess-fee form exists on NTT DATA Payment Services; certificates use a Razorpay rzp.io link. Canara Bank transfer is the alternative.
- Escalation follows data ownership: DMS/AMS for SLCM/AMS login, IT Infra for Office 365, Admissions for source data, Student Finance for fees, examination helpdesk for exam documents.
- Ecosystem is fragmented: DigiLibrary, SpaceBasic, Online Manipal, MAHE SIS and slcm.manipal.edu are separate services with separate audiences. No core-campus LMS or SLCM mobile app verified.
- Overall confidence 0.86; full authenticated feature inventory only 0.45.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/ | canonical login surface; welcome, sign-in, parent login labels.
- https://mujslcm.jaipur.manipal.edu/Home/Index | indexed route serving the same login surface; no public dashboard proven.
- https://muj.slcm.jaipur.manipal.edu/ | alternate MUJ-branded sign-in hostname; different email domain association.
- https://mujslcm.jaipur.manipal.edu/Student/Academic/AttendanceSummaryForStudent | exact attendance route; login-gated, strongest feature route evidence.
- https://mujslcm.jaipur.manipal.edu/Student/Academic/TimeTableForStudent | candidate timetable route; returns login only.
- https://mujslcm.jaipur.manipal.edu/Student/Academic/GradesForStudent | candidate grades route; returns login only.
- https://passwordreset.microsoftonline.com/ | Forgot Password destination; Microsoft recovery boundary.
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf | username pattern name.registration number, Outlook password, escalation contacts.
- https://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf | officially linked profile guide; text not extractable, existence link-verified only.
- https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf | Office 365 SOP, mandatory MFA, effective June 2025.
- https://jaipur.manipal.edu/pay-fee-online.php | splits academic fees to SLCM and hostel/mess to SpaceBasic.
- https://muj-payservices.nttdatapay.com/DirectPay/MUMessFee | NTT DATA mess-fee form; relationship to current instruction undated.
- https://rzp.io/l/lCB8nGo7Wj | Razorpay certificate/document payment; UPI/Paytm named.
- https://jaipur.manipal.edu/examination.php | exam hub; handbooks, application formats, schedules.
- https://mujlibrary.live/ | DigiLibrary; separate portal accepting both MUJ email domains.

## ACTIONABLE LEADS
- Probe the three named /Student/Academic/* routes for differential auth behavior (redirect, status, body size) across logged-out states before any authenticated test.
- Pull a behavior diff between canonical host and muj.slcm.jaipur.manipal.edu; also /Home/Index vs root.
- Inspect LoginFor/EmailFor hidden fields on the login form: test whether Student vs Parent mode changes the POST target or server behavior.
- Verify the Forgot Password redirect target, tenant branding, generic responses, and any open redirect behavior on recovery.
- Intercept the SLCM academic-fee checkout pre-gateway for amount, order id, student id, return URL fields (authorized testing only); processor is undisclosed so payment endpoint discovery is open.
- Re-fetch and OCR the SLCM Profile Registration Guide PDF; text was not extractable and it may carry endpoint details.
- Fetch the two Annual Fee PDFs (AY 2026-27 main and NRI) from the fee page; check bank instruction detail and form fields.
- Use independent guides (slcm.vercel.app, mujstella.in) as leads for real post-login functions; verify later under authorization.
- Disclosure contacts: registrar@jaipur.manipal.edu, dms@ and ams@ for SLCM ops, it.support@ for identity, student.finance@ for fees, exam.store@ and exam.helpdesk@ for exam documents; help extensions 738/784/481/263.

## FLAGS
- All post-login feature claims are unverified; only the unauthenticated login boundary was observed.
- Reference 26 is a Scribd copy of the grades route claiming 2025 grade sheet content; third-party, unverified, do not trust.
- References 20 and 24 (Annual Fee PDFs) carry garbled mojibake titles ("• �r� JIV/1;�·. ·\*"); URL content unverified.
- Profile-guide PDF existence rests on a link alone; no extractable text found.
- NTT DATA form undated; relation to the current SpaceBasic mess instruction is unclear.
- Alternative hostname email-domain association comes from search results, not first-party pages.
- Absence findings (no LMS, no transport, no staff dashboard) are bounded to public surfaces only.
- Confidence numbers (0.93/0.82/0.45/0.86) are model outputs, not measurements.
- Report labels SLCM administrative, not LMS; do not carry an LMS label forward without first-party proof.

## COVERAGE
- 39357 chars read; verified to EOF (336/336 lines, read_file truncated: false).