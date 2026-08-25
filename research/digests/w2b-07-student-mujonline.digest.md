## REPORT (w2b-07-student-mujonline.md)
Public OSINT comparison: MUJ Online student portal versus MUJ SLCM, plus Brightspace, M365 identity, and stack claims. No authentication attempted. Verdict: multi-application ecosystem, portal auth protocol unknown, no vulnerability claims. 242 lines, 36739 chars, read to EOF, truncated: false.

## ANSWER SUMMARY
- student.mujonline.com exposes a sparse shell: "Student Portal", "Welcome!", "To student portal", an Email label, and a help-desk message. Password, OTP, and provider are not shown.
- SLCM is separately documented as an institutional portal: registration URL, name-plus-registration-number username, Outlook-linked password, DMS/AMS and IT Infra support split, Admission-only corrections.
- D2L Brightspace is publicly identified as the LMS: "Powered by D2L Brightspace" on the login route plus a D2L customer case study. The student portal itself is not proven to be Brightspace.
- MUJ Office 365 SOP documents university mail IDs and mandatory MFA (Authenticator, phone SMS OTP, personal email). It does not prove federation for student.mujonline.com.
- One public Reddit report of an SLCM password error exists; no credible portal-specific breach report was found for MUJ Online.
- Supplied stack (ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai, M365 identity) is treated as an input hypothesis; public evidence confirms only fragments (jQuery 1.10.2 assets on SLCM, Angular-style assets on the portal).
- iLearn page looks like an enquiry or enrolment flow with four-digit OTP, not an enrolled-student login.

## KEY FACTS
- https://student.mujonline.com/ - public portal shell; Email label and help-desk text only.
- https://student.mujonline.com/login - same sparse shell on the login route.
- https://learning.onlinemanipal.com/d2l/home/14042 - Brightspace login route with visible product branding.
- https://muj.onlinemanipal.com/student-experience - UNext Labs (Python, R, MySQL, Java, PHP), mock exams, slot booking, practical exams, evaluation.
- https://muj.onlinemanipal.com/help-center - enrolled-student support: helpdesk@mujonline.edu.in, +91 7996 600 444.
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - SLCM registration URL, username format, Outlook-based password, support contacts.
- https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf - first-time setup, temporary password, mandatory MFA, verification methods.
- https://mujslcm.jaipur.manipal.edu/Home/Index - SLCM surface with student and parent choices.
- https://www.d2l.com/en-in/why-d2l/customers/manipal-university-jaipur-online - D2L case study naming Brightspace, scale, and learning capabilities.
- https://muj.onlinemanipal.com/ilearn-login - enrolment-style page with consent checks and OTP, not confirmed as student login.
- https://muj.onlinemanipal.com/ - programme delivery page describing LMS features and remote exams.
- https://www.reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue - the single public credential complaint, SLCM-specific.
- https://www.manipal.edu/mu/academics/student-portal.html - MAHE portal page linking sis.manipal.edu; not evidence about MUJ Online.
- http://muj.onlinemanipal.com/notifications - official notices describing the LMS learning workflow.
- https://learning.onlinemanipal.com/d2l/home/14201 - second D2L route with generic system-experience wording.

## ACTIONABLE LEADS
- Passive collection only: capture response headers, certificates, and DNS for student.mujonline.com, learning.onlinemanipal.com, and mujslcm.jaipur.manipal.edu.
- Research backlog: official user guide for the portal, explicit SSO documentation, recovery and lockout procedures, disclosure instructions (none found yet).
- Build a portal ownership matrix: who owns identity, records, course content, labs, exams, and support per domain.
- Model SLCM and portal as separate incident categories; do not merge failures into one "MUJ login problem".
- Authorized follow-up only: verify headers, certs, and deployment relationships under written permission.

## FLAGS
- Brightspace "may not be getting an optimal system experience" wording is generic, not an outage.
- Angular-style and jQuery observations are passive markup clues, not confirmed frameworks.
- The Office 365 SOP proves M365 identity exists university-wide, not that the portal delegates to it.
- iLearn classification is based on visible controls only.
- No breach evidence is absence of incident reports, not proof of security.
- Akamai was not independently confirmed in this pass.

## COVERAGE
- File read to EOF: 242 lines, 36739 chars (file_size 36739), truncated: false. Confirmed EOF at line 242, final reference.