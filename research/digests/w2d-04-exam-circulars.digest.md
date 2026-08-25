## REPORT (w2d-04-exam-circulars.md)
Public MUJ exam artifacts and safe SLCM risk map. Public pages and PDFs only, no portal testing. Verdict: exam process spine documented, hall-ticket format and marks-update path not publicly established. 224 lines, 41818 chars, read to EOF, truncated: false.

## ANSWER SUMMARY
- MUJ publishes an examination landing page, Student Examinations Handbook, Examination Manual with appendices, and timetable PDF families; use these as the baseline corpus.
- "Make-up" is the documented terminology: F or I in ETE allows a make-up exam in the respective course; no standalone "back paper" page or current deadline was found.
- Grade flow: answer books evaluated, marks lists submitted, marks uploaded to AMS/DMS, initial grades calculated there, Grade Moderation Committees may adjust boundaries, results declared after approvals within 15 days.
- Hall-ticket and identity requirements are documented as conduct rules, but no hall-ticket template or field spec is public; report the format as unknown.
- Timetable PDFs expose course codes, dates, slots, and discipline headings (public scheduling metadata), dated April-May 2025, May 2025, December 2024; no 2026 timetable link on the retrieved page.
- Grievance routes: online form on Microsoft Forms, UGC Samadhaan, USGRC committee; two separate 15-day clocks (USGRC report target, Ombudsperson appeal) must not be merged with result declaration timing.
- No attributable, verified MUJ marks-dispute case was found; the evidence gap is reported as a gap.

## KEY FACTS
- https://jaipur.manipal.edu/examination.php - central examination index: handbook, manual, application formats, timetable links, make-up application at Rs 1000 per course.
- https://jaipur.manipal.edu/img/pdf/exam/Student%20Examination%20Handbook%202023-24%20%2811.08.2023%29.pdf - eligibility thresholds (UG 35%, PG 40% ETE and overall), F/I/DT outcomes, make-up rules, result timing, conduct controls.
- https://jaipur.manipal.edu/img/pdf/exam/3.%20Manual%20Exam%20Process.pdf - evaluation, marks-list submission, AMS/DMS upload, grade moderation, approvals, result declaration.
- https://jaipur.manipal.edu/img/pdf/exam/4.%20Appendix%20I%20Examination%20manual%20MUJ%2003%20Apr%2019.pdf - answer-book and attendance chain of custody, fees Rs 1000 regular and Rs 700 online per subject.
- https://jaipur.manipal.edu/img/pdf/exam/B.Tech_Higher%20Sem_ETE_APRIL-MAY_2025.pdf - discipline columns, course names and codes, Slot-1 09:30-12:30, Monday 28-04-2025.
- https://jaipur.manipal.edu/img/pdf/exam/FOMC_ETE%20Timetable%20Dec%202024.pdf - faculty timetable with BBA and semester columns.
- https://jaipur.manipal.edu/img/pdf/exam/M.TECH_II%20SEM_ETE%20TT_%20APRIL-MAY%202025_.pdf - M.Tech second-semester timetable.
- https://jaipur.manipal.edu/img/pdf/academicrules/AC-calender-2026-27.pdf - 2026-27 milestone labels: MTE, ETE, re-sessional, make-up; visible July dates without complete label pairing.
- https://www.jaipur.manipal.edu/online-grevience-registration.php - grievance submission via Microsoft Forms, UGC Samadhaan, USGRC document links.
- https://www.jaipur.manipal.edu/img/pdf/Committee_USGRC.pdf - June 26 2026 notice: school-level escalation, quorum of three, two-year terms, 15-day report target, 15-day Ombudsperson appeal.
- https://mujslcm.jaipur.manipal.edu/ - portal landing: welcome, Sign In, Sign In Parent Login only.
- https://jaipur.manipal.edu/academic-rules-regulations.php - academic rules index, related context.
- http://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References - IDOR definition used for the control recommendation.
- http://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html - session IDs as untrusted input, session renewal after privilege changes.

## ACTIONABLE LEADS
- Maintain a document map: title, academic year, event type, audience, date, PDF or page; compare future revisions against it.
- Check newly published timetable PDFs for accidental student-level data and stale-file exposure.
- Ask the owner for a control description of marks-list to AMS/DMS reconciliation and grade-moderation approval records; propose a tabletop exercise, not a live manipulation.
- Route genuine complaints through the official grievance channels; keep a dispute-evidence register with three labels (verified process, student allegation needing consent, unverified hit).
- Verify current 2026 timetable and make-up notice availability through the examination page before claiming publication gaps.

## FLAGS
- Handbook is 2023-24; it is not silently treated as current 2026 rules.
- Fee wording differs across sources: landing page Rs 1000 per course, Appendix I Rs 1000 regular and Rs 700 online per subject; preserve, do not harmonize.
- "Marks uploaded to AMS/DMS" is an operational noun, not evidence of a student-editable path or public endpoint.
- Two 15-day clocks are distinct: result declaration after moderation and approvals, versus Ombudsperson appeal after USGRC decision.
- Stack labels (ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai, Microsoft 365) are supplied scope, not independently verified.
- No verified student marks-dispute case exists in the corpus; absence is not proof no dispute ever occurred.

## COVERAGE
- File read to EOF: 224 lines, 41818 chars (file_size 41818), truncated: false. Confirmed EOF at line 224, final reference.