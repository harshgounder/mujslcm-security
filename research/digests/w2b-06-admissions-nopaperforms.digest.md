## REPORT (w2b-06-admissions-nopaperforms.md)
MUJ admissions and NoPaperForms/Meritto SaaS link to SLCM. Public DNS and document analysis only, no testing. Verdict: hostname delegation confirmed, technical hand-off to SLCM not publicly documented. 228 lines, 37678 chars, read to EOF, truncated: false.

## ANSWER SUMMARY
- DNS resolves admissions.jaipur.manipal.edu as CNAME to jaipurmanipal.nopaperforms.com, then through an AWS ELB chain in ap-south-1. Delegation is confirmed; record storage, schema, and SLCM sync are not.
- The 2022 online-program manual documents identity, contact, academic, guardian, employment, uploaded document, payment, and status data, plus refund rules. It is an archived example, not the current schema for every program.
- Payment is online only (card, net banking, UPI), success triggers email and SMS, fee receipt via student portal. Processor name and tokenization are not stated.
- Statuses named: Application Downloaded, Under Review, Admission Approved, Provisional Admission, Re Submission Required, Rejected.
- SLCM FAQ: registration URL, username from name plus registration number, password based on the official Outlook ID, and Admission-only correction of admission-time details.
- No public source names an API, webhook, SSO assertion, database feed, or provisioning trigger between NoPaperForms and SLCM. The bridge is undisclosed.
- Meritto says the customer is controller or fiduciary and Meritto is processor; Trust Center lists SOC 2, ISO 27001, GDPR claims. These are vendor-wide, not MUJ-tenant evidence.

## KEY FACTS
- https://dns.google/resolve?name=admissions.jaipur.manipal.edu&type=CNAME - the core delegation proof: owner admissions.jaipur.manipal.edu, target jaipurmanipal.nopaperforms.com.
- https://dns.google/resolve?name=jaipurmanipal.nopaperforms.com&type=A - resolution chain through an AWS ELB name in ap-south-1, several addresses.
- https://admissions.jaipur.manipal.edu/ - current 2026-27 branded admissions landing page.
- https://muj.onlinemanipal.com/wp-content/uploads/2022/01/MUJ-Admission-Manual-Online-Programmes-V5.pdf - the detailed field, status, payment, and refund spec.
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - SLCM registration URL, username convention, Outlook-based password, Admission-controlled correction.
- https://www.meritto.com/privacy-policy/ - controller/processor split, subprocessors, contacts data@meritto.com, ticket@meritto.com, grievance@meritto.com.
- http://trustcenter.nopaperforms.com/ - SOC 2, ISO 27001 (surveillance audit May 21 2025), GDPR renewal (June 5 2026) claims.
- http://developer.nopaperforms.com/ - vendor module list: Lead, Opportunity, Activity, Form, Payment, User Role Permission, Query, Application.
- https://mujslcm.jaipur.manipal.edu/Home/Index - SLCM login surface with student and parent sign-in choices.
- https://jaipur.manipal.edu/admissions.php?p=UG - Apply Now and Track Application links, WhatsApp enquiry fields (Name, Phone, Email ID, Course, City, State).
- https://www.jaipur.manipal.edu/pay-fee-online.php - Pay Fee Online link, separate from the application flow in the report's view.
- http://manipal.edu/mu/important-links/privacy-and-cookie-policy.html - MAHE-wide privacy policy, not a MUJ-specific DPA.
- https://www.jaipur.manipal.edu/admission-contact.php - admission contact channel.
- https://apply.manipal.edu/ - separate application login surface, distinct from admissions.jaipur.manipal.edu.
- http://jaipur.manipal.edu/admissions.php - admissions index page.

## ACTIONABLE LEADS
- Re-run the two dns.google queries fresh; record answers and dates as point-in-time evidence.
- Check cdn.npfs.co asset references on the current UG route as SaaS presentation corroboration.
- Map the public admissions workflow: Apply Now, Track Application, Pay Fee Online, WhatsApp enquiry, admission contact.
- Treat the SLCM FAQ account convention as the onboarding boundary spec: name plus registration number, Outlook-based password, Admission-only corrections.
- Ask MUJ for a sanitized admissions-to-SLCM data-flow diagram, field-mapping document, tenant DPA, payment architecture summary, upload-deletion policy, and a non-production test account.
- Do not submit fake applications, enumerate applicants, or probe IIS, ASP.NET, Akamai, or M365 behavior without written scope.

## FLAGS
- The detailed field inventory comes from a 2022 archived online-program manual; the current form schema is not proven identical.
- The extractor failed to produce a stable text document of the current form; form labels seen in server HTML are not values.
- Application number is not equated with SLCM registration number anywhere in the reviewed sources; do not conflate them.
- No public integration mechanism exists in the record; absence of documentation is not proof of absence of an integration.
- Trust Center dates are vendor-level attestation only, no tenant-specific audit evidence.
- DNS observations are time-sensitive; E.g. style citations in the report mix sources but all listed references were preserved.

## COVERAGE
- File read to EOF: 228 lines, 37678 chars (file_size 37678), truncated: false. Confirmed EOF at line 228, final reference.