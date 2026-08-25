# Digest: w2d-03-fee-documents.md

## REPORT
Source: w2d-03-fee-documents.md (MUJ fee artifacts: public evidence and SLCM exposure)

## ANSWER SUMMARY
- MUJ publishes a large but fragmented public fee record: program pages, hostel and mess tables, annual circulars, refund policy, scholarship waivers; the SLCM landing page itself exposes only a login boundary and no fee UI.
- 2026-27 hostel double occupancy: INR 167,372 accommodation, INR 15,378 housekeeping, INR 25,475 refundable security deposit, INR 208,225 total including deposit; optional laundry INR 8,810 and health club INR 12,750.
- Hostel continuation circular reconciles with the hostel page: residential dwelling INR 182,750 (accommodation + housekeeping), mess INR 79,000, full-year total INR 261,750, deadline 5 July 2026, SpaceBasic-only payment, non-refundable once paid.
- Payment page routes existing students to the SLCM portal for course fees and to SpaceBasic for hostel and mess; post-payment email must include UTR number, debit-account holder, transaction date, amount, using a linked format.
- 12% per annum late-fee rate appears only in the 2025-26 annual notice (deadline 18 July 2025) and must be treated as historical, not applied to 2026-27; the 2026-27 academic calendar gives 16 July as the fee-payment date.
- Refund table runs from full refund to nil based on withdrawal timing; scholarships grant tuition-fee waivers (Visvesvaraya, TMA Pai, Rajasthan merit, local-region, sibling, MUJ graduate, disability, MBA bands).
- Unanswered: transport fee schedule, current recurring-student late-fee rule, validated receipt-template contents, authenticated fee-module screenshot.
- Notable: the 2025-26 notice prints the portal as https://mujslcm.jaipur.manipal.edu:122/ while the 2026 payment page prints the bare hostname; the report flags this as an observable URL-form difference, inference only.

## KEY FACTS
- https://jaipur.manipal.edu/hostel-fees.php - 2026-27 hostel table with component amounts, login-gated payment modes, receipt retention advice.
- https://jaipur.manipal.edu/mess-fees.php - mess fee INR 79,000 with revision warning for fuel/market/inflation pressure.
- https://jaipur.manipal.edu/pay-fee-online.php - payment routing (SLCM vs SpaceBasic) and UTR/account-holder/date/amount email workflow with Download the Format link.
- https://jaipur.manipal.edu/indian-fee-structure.php - official course-fee index across programs; registration non-refundable, caution deposit refundable.
- https://jaipur.manipal.edu/fol/bachlor-LLB.php#Program-Fee - LLB fees: INR 108,000 tuition, INR 10,000 registration, INR 10,000 deposit, INR 128,000 at admission (USD columns shown).
- https://jaipur.manipal.edu/foe/m-tech-structural.php#Program-Fee - M.Tech Structural: INR 181,000 tuition, INR 206,000 at admission; applies to students admitted till academic year 2025.
- https://jaipur.manipal.edu/img/pdf/Annual-Fee-Payment-for-the-AY-2026-2027.pdf - hostel continuation circular; 5 July 2026 deadline, SpaceBasic only, OCR-garbled fields in mess and final-year rows.
- https://jaipur.manipal.edu/img/pdf/academicrules/AC-calender-2026-27.pdf - academic calendar; 16 July as last fee-payment date.
- https://jaipur.manipal.edu/img/pdf/Notification_Annual-Fee-Payment-AY-2025-26.pdf - 18 July 2025 deadline, 12% per annum late fee, Annexure 1 course-wise and batch-wise amounts, portal URL with :122 port.
- https://jaipur.manipal.edu/indian-refund-policy.php - withdrawal refund table (full to nil), 45-day refund window, dues-clearance certificate requirement.
- https://jaipur.manipal.edu/indian-scholarship.php - waiver categories and CGPA continuity conditions for scholarships.
- https://mujslcm.jaipur.manipal.edu/Home/Index - SLCM login boundary; no fee balances or module UI in public extract.
- http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf - MUJ ICT inventory; SLCM described as replacing AMS with attendance, internal/external marks, result publication, broadcast modules.
- https://github.com/DK10WS/SLCM_APP - student-built app describing login, timetable, grades, attendance; not official fee evidence.
- https://mujstella.in/ - independent platform explicitly not affiliated with MUJ.

## ACTIONABLE LEADS
- Build a versioned artifact register: source URL, retrieval date, academic-year label, component, amount, currency, provider route, confidence, redaction status.
- Locate a current 2026-27 recurring-student late-fee circular and any separately titled transport fee notice.
- Investigate the :122 URL form found only in the 2025 notice; treat any port-based inference as unverified.
- Track reconciliation checks (hostel components vs circular totals) as analyst calculations, labeled as such.
- Do not submit payment forms, probe the portal, or replay transaction references; public-only boundary.

## FLAGS
- OCR corruption in the annual circular (mess and final-year fields) must not be repaired by guesswork; the clean mess page supports INR 79,000.
- 12% late fee is historical 2025-26 only; clause extraction was truncated.
- 5 July (hostel circular) vs 16 July (calendar) is a scope difference, not a contradiction.
- Scribd "Updated Payment Receipt" failed to load in review; very low reliance.
- Garbled PDF titles in references (mojibake) indicate extraction artifacts.
- The :122 portal URL form may indicate a legacy document or old deployment; inference only, no connection tests performed.

## COVERAGE
Chars read: 43,755. EOF confirmed: true.