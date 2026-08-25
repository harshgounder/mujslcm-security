# Digest: w2g-01-reddit-r-manipal.md

## REPORT
Source file: w2g-01-reddit-r-manipal.md (MUJ SLCM Reddit OSINT: Findings, Gaps, and Safe Actions)

## ANSWER SUMMARY
- Recurring availability complaints: SLCM described as crashing every other day and a MUJ site unusable for much of a semester.
- Identity lifecycle friction: a registration number changed after intra-sliding and both old and new identifiers were rejected.
- Payment reconciliation failures: fee paid with receipt while SLCM showed pending; a stale due blocked an admit card until proof and escalation.
- Academic data reports: missing or wrong-term attendance, removed results tab, grades decreased, SLCM 2.0 preference and subject regressions.
- CGPA exposure allegation is unverified: site later returned 404, a commenter claimed IT patched within a week, no institutional confirmation found.
- Public GitHub projects document ongoing automation interest, one advertising CAPTCHA solving; existence is not evidence of a current vulnerability.
- The supplied stack remains an unverified inventory hypothesis; Reddit evidence does not confirm it.
- Coverage is a high-confidence sample, not exhaustive; some threads lacked recoverable permalinks or dates.

## KEY FACTS
1. https://www.reddit.com/r/manipal/comments/17anbg2/slcm_is_literally_ass/ - leading availability complaint from 2023.
2. https://www.reddit.com/r/manipal/comments/17usdb4/attendance_lock_for_slcm/ - attendance lock thread; comment claims the lock is about one week earlier.
3. https://www.reddit.com/r/manipal/comments/1qa5h99/slcm_20_manipal_situation_summarised/ - SLCM 2.0 regression reports.
4. https://www.reddit.com/r/manipal/comments/1ncl5xy/cgpa_data_leak_of_all_branch_students/ - CGPA exposure allegation with 404 edit and patch claim.
5. https://www.reddit.com/r/Manipal_Academics/comments/1993mdc/slcm_login/ - intra-sliding registration number rejection.
6. https://www.reddit.com/r/Manipal_Academics/comments/1lzf0ht/paid_my_fees_but_still_showing_as_pending_on_slcm/ - fee paid but pending with receipt available.
7. https://www.reddit.com/r/manipal/comments/1m23kxi/one_of_the_worst_departments_in_the_college/ - stale SLCM due blocking an admit card.
8. https://www.reddit.com/r/manipal/comments/1cyd4xv/what_is_casual_term_fee_on_slcm/ - casual term fee concern, fee pending Rs 6,000.
9. https://www.reddit.com/r/manipal/comments/1m0ofr4/has_anyone_used_the_emi_option/ - GrayQuest EMI receipt concern in SLCM.
10. https://www.reddit.com/r/Manipal_Academics/comments/1plljtw/it_appears_they_have_removed_the_results_tab_from/ - removed results tab and non-working academics tab report.
11. https://www.reddit.com/r/Manipal_Academics/comments/1pny6zb/grades_decreased_on_slcm/ - grades decreased report, details unrecovered.
12. https://www.reddit.com/r/Manipal_Academics/comments/1s8mhsd/can_someone_please_share_me_the_parent_slcm_link/ - parent link request; user-ID format intentionally withheld in the report.
13. https://github.com/tejaskash/slcm-api - Flask REST API for attendance and marks from SLCM.
14. https://github.com/sankalp2004/SLCM-is-Dumb - CGPA extraction with CAPTCHA automation and credential warnings.
15. https://mujslcm.jaipur.manipal.edu/ - public portal surface: "WELCOME TO MUJ PORTAL", Sign In, Parent Login, @muj.manipal.edu.

## ACTIONABLE LEADS
- Build a measurement plan for availability, login success by lifecycle state, payment reconciliation age, and attendance freshness.
- Create a finance-to-SLCM reconciliation queue with immutable transaction IDs, idempotent updates, and visible escalation status.
- Preserve evidence of the CGPA allegation privately and ask the owner to confirm scope, containment, and fix status.
- Model identity as a state machine (admitted, intra-slid, provisioned, parent-linked, active) and test sync with synthetic accounts.
- Scan public SLCM repositories for exposed secrets and rotate any compromised credentials.
- Publish status labels for attendance and marks ("not yet uploaded", "pending validation", "frozen", "corrected") and correction tickets.

## FLAGS
- The CGPA allegation is unverified; the patch claim is a single commenter with no institutional confirmation.
- Dates are partial: some threads have Unix timestamps, others only relative ages.
- Reddit indexing is incomplete; deleted and unindexed threads mean the corpus is a sample.
- Student workarounds (lab switching, credential advice) are not official procedures.
- A 404 is not a security conclusion; only authorized tests with synthetic records can prove object-level controls.

## COVERAGE
Chars read: 38929. EOF confirmed: yes (truncation flag false on full read).