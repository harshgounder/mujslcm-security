# Digest: w2b-02-mujerp.md

## REPORT
Source: w2b-02-mujerp.md (MUJ SLCM and ERP public OSINT assessment)

## ANSWER SUMMARY
- mujerp.jaipur.manipal.edu/MUJWEB/ publicly presents a Dynamics 365 Business Central sign-in surface; username/password fields and /MUJWEB/SignIn POST form observed.
- MUJ's official IT page describes Microsoft "Business ERP" and a "Student life cycle via Web portal" as separate landscape items; it never maps the mujerp hostname.
- ERP audience (staff, faculty, finance), enabled modules, and data are unknown; no public module list, role matrix, or owner statement.
- SLCM is better documented: official FAQ names the registration link and username pattern; first-year guide describes one-stop academic platform handling identity, admission, contact, education, document data.
- Attendance route /Student/Academic/AttendanceSummaryForStudent is publicly indexed but a GET returned the generic login wall, no records.
- Payroll exists as an MUJ Finance service for faculty and staff; no source places payroll inside mujerp.
- Separate MUJ HR login surface exists at mujone.jaipur.manipal.edu/HR/Login.aspx with email, employee code, DOB, captcha fields.
- Supplied technology claims (ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, Azure 20.244.0.229) remain unconfirmed by public evidence.

## KEY FACTS
- https://mujerp.jaipur.manipal.edu/MUJWEB/ - ERP landing; "Welcome to Dynamics 365 Business Central" title, user-name and password labels.
- https://mujerp.jaipur.manipal.edu/MUJWEB/SignIn - public markup shows form POST to this endpoint; no SSO button or role selector observed.
- https://mujslcm.jaipur.manipal.edu/ - SLCM landing; WELCOME TO MUJ PORTAL, Sign In and Parent Login controls, @muj.manipal.edu suffix.
- https://mujslcm.jaipur.manipal.edu/Student/Academic/AttendanceSummaryForStudent - indexed attendance route; retrieval returned login wall only.
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - official FAQ; registration link, name-plus-registration-number username, Outlook ID password, AMS support.
- http://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf - official onboarding guide; SLCM academic purpose, identity/admission fields, parent OTP, document uploads.
- https://www.jaipur.manipal.edu/administration-it.php - official IT page; Microsoft Business ERP vs student life cycle portal, IT security remit.
- https://www.jaipur.manipal.edu/administration-finance.php - Finance page; payroll services to faculty and staff, accounting and reporting duties.
- https://jaipur.manipal.edu/human-resource.php - HR page; employee lifecycle, compensation, benefits, leave management.
- https://mujone.jaipur.manipal.edu/HR/Login.aspx - separate MUJ HR login surface; employee-oriented fields.
- https://slcm.vercel.app/guides/check-attendance-muj - betterSLCM guide; claims attendance display and prediction, third-party.
- http://github.com/DK10WS/SLCM_APP - third-party app README; claims attendance, grades, GPA/CGPA, timetable; not official.
- https://mujstella.in/ - independent student platform; explicit non-affiliation with MUJ.
- https://learn.microsoft.com/en-us/dynamics365/business-central/finance - generic product docs; finance capabilities and payroll transaction imports, not MUJ configuration.
- https://www.microsoft.com/en-us/dynamics-365/products/business-central - generic product context for Business Central.

## ACTIONABLE LEADS
- Verify the 20.244.0.229 mapping claim by resolving mujerp DNS and checking attribution; report currently holds it unconfirmed.
- In an authorized environment only, test whether /MUJWEB/SignIn failure responses distinguish valid users; note the surface in inventory.
- Inventory SLCM routes named by third-party tools (attendance, grades paths) and check which are publicly indexed.
- Keep ERP and SLCM as separate boxes in club diagrams with an unverified relationship label.
- Disclosure step: ask MUJ IT for an official hostname-to-system mapping and Business Central tenant documentation.

## FLAGS
- "mujerp is staff/faculty-facing" is an inference; page states no audience.
- Payroll inside mujerp is unproven; generic Business Central docs do not prove enabled modules.
- Azure IP 20.244.0.229, ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai, M365 identity are unconfirmed inputs.
- Attendance/grades claims come from third-party sources, not official MUJ specs.
- Route discoverability does not equal data exposure; retrieval hit the login boundary.

## COVERAGE
Chars read: 36,398. EOF confirmed: true.