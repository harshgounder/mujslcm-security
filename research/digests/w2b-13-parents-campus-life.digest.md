# Digest: w2b-13-parents-campus-life.md

## REPORT
Source file: w2b-13-parents-campus-life.md (MUJ SLCM Parent Surface: Public Evidence and Safe Review)

## ANSWER SUMMARY
- parents.php is a pre-authentication information layer: programs, student affairs, hostels, safety, anti-ragging, helplines, grievance registration, academic calendar; it contains no parent login link.
- The official Parent Portal Login Manual (hosted at /admin/photo/annoncement/49.pdf) documents OTP-based parent access: OTP goes to the registered parent mobile, and unregistered numbers are told to email admissions@jaipur.manipal.edu.
- The manual confirms only academics and examination information on the dashboard under Reports; attendance, fees, hostel, transport, notices, and messaging permissions stay unknown.
- The SLCM login form carries Parent Login and Student Login plus EmailFor, LoginFor, UserName, Password, and a request-verification token; role fields are presentation metadata, not proof of broken authorization.
- A Microsoft password-reset destination is visible in the form capture; consistent with Microsoft identity but not proof of a specific federation design.
- Hostel rules give parents a physical and operational role only: no room entry, cafeteria cash-and-carry meals, city visits need Chief Warden approval plus parent consent, night out needs a parent request on the out-pass.
- Transport evidence is route-to-campus information (distances and RSRTC buses); no dedicated transport page exists in the reviewed sitemap.
- The manual PDF sits under a crawler-disallowed /admin/ path; a documentation and discoverability inconsistency, not an access-control bypass.

## KEY FACTS
- https://jaipur.manipal.edu/parents.php - parent landing page; public info layer before login
- https://jaipur.manipal.edu/admin/photo/annoncement/49.pdf - Parent Portal Login Manual; OTP workflow authority
- https://mujslcm.jaipur.manipal.edu/ - SLCM landing with Parent Login and Student Login
- https://mujslcm.jaipur.manipal.edu/Home/Index - login form structure and @muj.manipal.edu identity label
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - student FAQ; username format, Outlook ID password, admissions-only record changes; do not project onto parents
- https://jaipur.manipal.edu/chiefwardensmessage.php - Chief Warden message and public contacts
- https://jaipur.manipal.edu/faqs-regarding-hostel.php - parent room access ban, cafeteria rule, night-out and medical notification rules
- https://jaipur.manipal.edu/hostel-fees.php - 2026-27 fee table and the no-individual-intimation rule for rule changes
- https://jaipur.manipal.edu/contact-university.php - bus stand, railway, and airport distances; arrival planning only
- https://www.jaipur.manipal.edu/announcement.php - general notice board that hosts the parent manual link
- https://jaipur.manipal.edu/events.php - public events with dates and venues
- https://jaipur.manipal.edu/academics-calender.php - public academic calendar entries
- https://jaipur.manipal.edu/robots.txt - disallows /admin/ while allowing PDF indexing; context for the manual location oddity

## ACTIONABLE LEADS
- Authorized test cases for the parent flow: parent can see only the correctly associated child, role field changes do not grant student rights, OTP retry and lockout behavior, old sessions invalidated at logout.
- Request from the owner a parent role matrix separating grades, attendance, fees, hostel, out-pass, transport, circulars, and messaging per action type.
- Confirm the phone-number update and verification process; the admissions fallback is a social-engineering surface.
- Reconcile the /admin/ robots disallow with the manual hosted under /admin/photo/annoncement/ so the official manual stays reachable and indexed.
- Establish whether night-out and out-pass requests touch any digital system before assuming a portal function.
- Ask General Services or the transport owner about any student bus service; absence from the sitemap is not proof of nonexistence.

## FLAGS
- EmailFor and LoginFor are client-visible routing inputs; the report explicitly refuses any server authorization conclusion.
- Student credential formats from the SLCM FAQ must not be reused to infer parent credentials.
- Parent dashboard scope beyond academics and examination is undocumented; do not add categories.
- The manual is hosted under the crawler-disallowed /admin/ path; that is a governance observation, not a bypass opportunity.
- Alternate SLCM hostname muj.slcm.jaipur.manipal.edu appears in search results; canonical relationship unproven.

## COVERAGE
45,231 chars read (file_size bytes), read to EOF, truncated=false confirmed.

DONE w2b-13-parents-campus-life.digest.md