# Digest: w2g-03-quora-manipal.md

## REPORT
Source file: w2g-03-quora-manipal.md (MUJ SLCM Quora Footprint and Safe OSINT Assessment)

## ANSWER SUMMARY
- The Quora footprint is thin: one accessible anonymous answer on MUJ attendance publication and a two-day lock.
- Official sources carry more weight: the onboarding guide says credentials go to a personal Gmail account, parent mobile OTP enables Parent login, and documents are verified at physical reporting.
- The marks-sharing question is discoverable but its answer fields are unavailable; the CGPA page is blocked; neither supports any conclusion.
- No confirmed MUJ SLCM insider was found; visible Quora profile labels are affiliation signals only.
- Two MUJ-labelled hostnames are indexed (mujslcm.jaipur.manipal.edu and muj.slcm.jaipur.manipal.edu); hostname confusion is a documentation and phishing topic.
- The supplied stack (ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai, M365) remains unverified by Quora evidence; "official outlook ID" wording proves nothing.
- The right output is a defensive data-flow and privacy checklist plus authorized questions, not a test recipe.

## KEY FACTS
1. https://mujslcm.jaipur.manipal.edu/ - official portal: Student Login, Parent Login, Forgot Password.
2. https://muj.slcm.jaipur.manipal.edu/ - alternate MUJ-labelled hostname with similar page labels.
3. http://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf - guide: credential delivery via personal Gmail, parent OTP, document upload and verification.
4. http://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - FAQ: registration link, login wording, support channels, helpline.
5. https://www.quora.com/How-is-the-attendance-calculated-at-MUJ - the only accessible relevant answer; unattributed, undated.
6. https://www.quora.com/Are-End-Semester-marks-shared-with-parents-at-MUJ - relevant question URL; answer fields unavailable.
7. https://www.quora.com/How-is-CGPA-calculated-at-Manipal-University - blocked page, error only.
8. https://www.quora.com/How-do-I-maintain-my-CGPA-at-MUJ - generic study advice snippet only.
9. https://www.quora.com/Is-Manipal-University-a-fraud - contextual page with visible profile labels and broad claims.
10. https://www.quora.com/profile/Prajay-Vats - profile label, BTech in IT at MIT, 2021; affiliation signal only.
11. http://manipal.edu/mu/academics/student-portal.html - MAHE student portal page linking to SIS at sis.manipal.edu.
12. https://student.mujonline.com/login - MUJ student portal result with helpdesk wording.
13. https://srmuniversity.quora.com/Which-is-better-CS-at-MUJ-or-CS-at-SRM-KTR - experience snippet only.
14. https://www.quora.com/What-is-the-procedure-for-getting-the-MUJ-outpass-signed - title only, no answer content.
15. https://www.quora.com/How-is-manipal-university - error-only output ("Something went wrong").

## ACTIONABLE LEADS
- Verify current attendance publication and lock policy through official MUJ channels before quoting the anonymous claim.
- Ask the owner how parent number changes are reverified, how mistaken parent links are revoked, and whether students see link status.
- Publish one canonical MUJ SLCM link and a clear support route to reduce hostname confusion and impersonation risk.
- Document onboarding data flows: Gmail delivery, OTP, document upload, physical verification.
- Request policy and sample audit records for attendance change control; do not attempt to replay or bypass locks.
- Keep MAHE SIS, MUJ SLCM, and student.mujonline.com in separate evidence buckets.

## FLAGS
- The attendance answer is anonymous, undated ("from this year"), and uncorroborated; it is not current policy.
- Marks and CGPA pages are inaccessible; do not reconstruct remembered or implied answers.
- Named profiles (Prajay Vats, Harshit Anand, Supriya Prem Kumar, Rohan Krishna, Nikita Kishore) are affiliation signals, not insider evidence; do not contact or profile them.
- "Official outlook ID" does not establish a Microsoft 365 authentication architecture.
- No Quora result with the literal hostname and both question and answer text was recovered; this is a collection limitation.

## COVERAGE
Chars read: 52298. EOF confirmed: yes (truncation flag false on full read).