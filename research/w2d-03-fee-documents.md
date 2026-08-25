# MUJ Fee Artifacts: Public Evidence and SLCM Exposure

## Executive Summary

This report inventories public fee-related evidence around the Manipal University Jaipur (MUJ) Student Life Cycle Management (SLCM) ecosystem, with emphasis on what an unauthenticated researcher can verify without attempting access to protected functions. The application-stack description in the brief, including ASP.NET MVC, .NET Framework, IIS, Akamai, and Microsoft 365 identity, is treated as supplied scope rather than independently verified here. No active fingerprinting, scanning, authentication testing, transaction submission, or bypass activity is part of this report.

- **Public SLCM Boundary**: The public MUJ portal extract shows a welcome page, sign-in control, and parent-login wording, but no fee balances, receipt records, or fee-module screen [3] -> treat the fee module as unverified from the public landing surface, not as absent.
- **Program Fee Model**: MUJ's official course-fee index exposes links to many program-specific pages, while representative pages provide annual tuition, one-time registration, refundable caution deposit, and admission-total fields [2] [25] [23] -> preserve program, admission-year, student category, and currency before reusing a number.
- **Hostel Fee Baseline**: The 2026-27 hostel table lists INR 167,372 accommodation, INR 15,378 housekeeping, INR 25,475 refundable security deposit, and INR 208,225 including the deposit [5] -> do not merge hostel, tuition, mess, and refundable deposit into one generic fee.
- **Mess Fee Baseline**: MUJ's 2026-27 mess page lists INR 79,000 and warns that a revision may be communicated in advance because of fuel, market, and inflationary pressures [7] -> attach an academic-year label and retain the revision qualifier.
- **Date Divergence**: The 2026-27 academic calendar marks 16 July as the last date for fee payment [17] [17], while the hostel continuation circular requires payment by 5 July 2026 [29]. A 2025-26 annual notice separately states an 18 July 2025 course-fee deadline and a 12% per annum late-fee rate on the amount due [31] [31] -> never carry the 2025 late-fee rule into 2026 without a current notice.
- **Receipt Workflow**: The official payment page sends existing students to the MUJ SLCM URL, sends hostel and mess payments to SpaceBasic, and requires transaction details including UTR number, debit-account holder, transaction date, and amount by email using a linked format [6] [6] [6] -> classify this as a public transaction-confirmation workflow, not as a verified receipt-template or receipt-UI disclosure.
- **Refund and Waiver Evidence**: MUJ publishes a withdrawal-refund table ranging from full refund to nil depending on timing [18] and a scholarship page with tuition-fee waivers for merit, region, siblings, MUJ graduates, disability, MBA, and other categories [14] [14] [14] -> keep withdrawal refunds, scholarships, deposits, hostel charges, and late fees as separate policy objects.
- **Unanswered Public Artifacts**: No authoritative public transport-fee schedule, current recurring-student late-fee rule, validated receipt-template contents, or authenticated fee-module screenshot was verified. The official portal evidence remains a login surface [3], and a public student-built app describes login, timetable, grades, and attendance rather than an official fee screen [16] -> record these as evidence gaps, not negative proof.

The highest-confidence conclusion is that MUJ publishes a substantial but fragmented fee record. The strongest artifacts are official HTML tables and official PDF notices. The weakest are third-party receipt images, student-built interfaces, and search leads whose provenance or content cannot be validated. The practical security-club lesson is to build a versioned public-artifact register rather than infer the protected SLCM design from fee pages alone.

## 1. Public SLCM Surface and Payment Trust Boundary

MUJ's own institutional ICT inventory describes SLCM as replacing the older Academic Management System and as a single-window system for students and parents, with modules including attendance, internal marks, external marks, result publication, and broadcast messages [32]. That description establishes the system's institutional role, but it does not disclose a fee-screen layout, an API contract, or an authenticated receipt view. The public MUJ portal at the reviewed landing URL exposes the text "WELCOME TO MUJ PORTAL" and sign-in functionality, including parent-login wording [3].

A separate official payment page creates the important public trust-boundary map. For existing students it names the SLCM student portal URL, while hostel and mess fees are directed to the SpaceBasic app [6]. This is a concrete public handoff between the university's student system and an accommodation or services provider. It does not prove that the SLCM itself processes every fee type, nor does it prove that SpaceBasic is the only backend involved in every hostel transaction. Those are inferences that would require authenticated or contractual evidence, which is outside this review.

| Public surface | Direct public evidence | Authority and scope | What can be concluded | What cannot be concluded |
|---|---|---|---|---|
| MUJ SLCM landing page | Welcome, sign-in, and parent-login wording [3] | Official MUJ portal | An unauthenticated login boundary is publicly visible | Fee balances, receipt history, role controls, and fee-module screens are not established |
| Official payment page | Existing-student SLCM URL and SpaceBasic route for hostel and mess [6] | Official MUJ fee communications | Public payment routing is documented | The internal integration, session behavior, or protected endpoints are not established |
| Official course-fee index | Links to many program pages, including engineering, law, management, and science programs [2] | Official MUJ admissions content | Program-specific fee pages exist as a public information pattern | A complete, current PDF archive for every program is not established |
| Official hostel and mess pages | Academic-year tables and payment instructions [5] [7] | Official MUJ pages, with hostel-service qualifications | Current-looking hostel and mess values and service rules are public | Tuition, transport, and authenticated payment UI cannot be inferred from them |

### Case study: MUJ's payment page versus the public SLCM page

The official payment page is more informative than the public SLCM landing page. It gives the student-portal URL, an external app route for hostel and mess, and a post-payment email workflow [6] [6]. The SLCM landing page, in contrast, exposes only the entry boundary [3]. The outcome is a split evidence picture: payment policy is partly public, while the operational fee interface remains unobserved.

This case reveals why an OSINT report should not treat a login page as a product screenshot. The absence of a fee control in an unauthenticated extract is an observation about that public response, not proof that the fee module is disabled, missing, or insecure. The safe recommendation is to record the public page exactly, label the protected area as unverified, and avoid any attempt to enumerate accounts or reach authenticated functions.

## 2. Program Fee Artifacts: HTML Schedules and Representative Amounts

The official course-fee index is a directory of program pages rather than a clean, centralized PDF inventory in the reviewed public material. It lists program links across faculties and levels, including LLB, multiple M.Tech options, MBA, MCA, and science programs [2]. This matters because a researcher who searches only for PDF files can miss the primary public fee table embedded in a program page. Conversely, a researcher who copies a number without checking the page's applicability note can turn an older admission-year value into a false current figure.

The following table gives representative official program records. It is intentionally not presented as an exhaustive program catalog. Amounts are copied with the source's Indian and international columns, and the applicability note is retained where the source exposes it.

| Program page | Level and duration | Annual tuition | One-time registration | Refundable caution deposit | Total at admission | Evidence qualification |
|---|---|---:|---:|---:|---:|---|
| LLB, Bachelor of Law | UG, 3 years [25] [25] | INR 108,000; USD 2,430 | INR 10,000; USD 300 | INR 10,000; international column blank | INR 128,000; USD 2,730 [25] | Public program-fee table; admission year is not stated in the cited table |
| M.Tech Structural Engineering | PG, 2 years [23] [23] | INR 181,000; USD 4,400 | INR 10,000; USD 300 | INR 15,000; international column blank | INR 206,000; USD 4,700 [23] | Page says details apply to students admitted till academic year 2025 [23] |
| M.Tech Data Science | PG, 2 years [27] [27] | INR 181,000; USD 4,400 | INR 10,000; USD 300 | INR 15,000; international column blank | INR 206,000; USD 4,700 [27] | Same fee pattern is publicly displayed on this program page; admission-year scope must still be checked |
| B.Tech Data Science | UG program page | Not visible in reviewed fee-section extract | Not visible | Not visible | Not visible | The public extract exposes a Program Fee heading but no fee rows [21] |
| B.Tech Electrical and Electronics | UG program page | Not visible in reviewed fee-section extract | Not visible | Not visible | Not visible | The public extract exposes a Program Fee heading but no amount rows [22] |

The official course-fee page warns that tuition, registration fees, and caution deposit are subject to change and approval by the Fee Fixation Committee. It also states that registration is non-refundable and that the caution deposit is refundable on completion of the program [2]. The same page says fees can be paid by demand draft in favor of Manipal University Jaipur, payable at Jaipur [2]. These clauses are policy context, not evidence that every listed program amount is current for every admission batch.

### Case study: LLB and M.Tech show the difference between a fee record and a fee policy

The LLB page exposes a complete admission-total calculation: annual tuition of INR 108,000, a one-time registration fee of INR 10,000, and a refundable INR 10,000 caution deposit, totaling INR 128,000 for the Indian column [25]. The M.Tech Structural page exposes the same categories but a different amount profile and an explicit older applicability boundary, with INR 181,000 annual tuition and INR 206,000 at admission [23] [23].

The outcome is useful for a security club's data model. A fee record needs at least program, level, duration, student category, currency, component, amount, admission-year scope, and refundability. The mechanism is that the page's total is not a single economic object: it combines a recurring tuition value with registration and deposit components. The recommendation is to store each component separately and calculate totals only as a marked arithmetic check, not as a replacement for the university's policy wording.

The 2025-26 annual payment notice reinforces this distinction. It says that annual course fee amounts are course-wise and batch-wise in Annexure 1 [31]. That is evidence that batch context matters, but the reviewed extract does not expose every Annexure 1 row cleanly. Therefore, the representative HTML values above should not be advertised as a complete 2026-27 fee schedule.

## 3. Hostel and Mess Fees for Academic Year 2026-27

The 2026-27 hostel page is the cleanest current public numeric artifact in the reviewed set. It labels the table as double occupancy and separates accommodation, housekeeping, refundable security deposit, total including deposit, and optional services [5]. The official page also says that payment modes such as UPI, internet banking, and cards become accessible after logging into the room-booking portal [5]. This is a useful boundary: the amount table is public, while at least some payment-mode details are login-gated.

| Hostel component, double occupancy | Amount in INR | Treatment and source wording |
|---|---:|---|
| Hostel accommodation | 167,372 | Listed as hostel fees [5] |
| Housekeeping charges | 15,378 | Listed separately [5] |
| Refundable security deposit | 25,475 | Explicitly labeled refundable [5] |
| Total including security deposit | 208,225 | Official displayed total [5] |
| Laundry for 30 cycles | 8,810 | Optional service [5] |
| Health Club, one selected option | 12,750 | Optional 10-month Gym, GHS, or Bluedove option [5] |

The arithmetic check 167,372 + 15,378 + 25,475 equals 208,225. This is a calculation from the displayed rows, not a new fee rule. The page says room allotment is confirmed only after successful receipt and verification of full hostel fees [5], and it advises students to retain payment receipts and transaction references [5]. It also says payment-gateway convenience charges, if any, are borne by the student and displayed at payment time [5].

The mess page separately lists INR 79,000 for the 2026-27 academic year [7]. It states that market, fuel, and inflation conditions may lead to a revision communicated in advance [7]. It also describes a two-month mess-allotment period, limited seats, and a two-month lock-in during which change requests are not accepted [7]. Those are service-allocation rules, not late-fee rules.

| Annual hostel circular item | Public value or rule | Evidence and interpretation |
|---|---|---|
| Residential dwelling, double occupancy | INR 182,750 for 2026-27 [29] | This matches the arithmetic sum of hostel accommodation and housekeeping on the hostel page; this match is an inference supported by both official artifacts [5] |
| Mess, full year | INR 79,000 on the official mess page [7] | The circular's OCR renders the mess digits poorly but shows a total of INR 261,750 [29]; the clean mess page is the better numeric transcription |
| Residential dwelling, final year | INR 127,925 [29] | The circular states this amount for a final-year student going outside for internship; the remaining OCR fields are not treated as reliable |
| Health Club | INR 12,750 [29] | Optional service in the circular and the hostel page |
| Payment channel | SpaceBasic only [29] | Scope is the hostel continuation circular, not proof about course tuition |
| Payment deadline | On or before 5 July 2026 [29] | Failure is described as voluntary vacation of the room and possible reallocation [29] |
| Refund treatment | Fees once paid are non-refundable under the circular [29] | This is a hostel circular rule and should not be silently generalized to course-fee withdrawal policy |
| Partial payment | Payment may be made in parts [29] | The circular describes administrative presentation of the consolidated proforma amount |

### Case study: Reconciling the hostel webpage with the annual circular

The hostel page presents a total of INR 208,225 because it includes the refundable security deposit. The annual circular presents residential dwelling at INR 182,750, which equals accommodation plus housekeeping, and separately pairs that figure with the INR 79,000 mess amount to produce the circular's INR 261,750 full-year total [5] [29] [7]. This is not a contradiction once the deposit is separated from the annual service charges.

The mechanism is a scope mismatch, not necessarily a pricing mismatch: one artifact is a hostel fee table including a deposit and optional services; the other is a continuation-payment circular focused on residential dwelling and mess. The decision implication is important for public reporting. A table that labels INR 208,225 as the annual hostel charge would obscure the refundable component, while a table that labels INR 261,750 as hostel-only would incorrectly absorb mess. The recommendation is to preserve the source label beside every amount and to show the arithmetic reconciliation explicitly.

The circular also creates a hard operational consequence: payment by 5 July 2026 is tied to preserving the room, and nonpayment can make the room available for allocation to another student [29]. That is a reservation rule, not evidence of a late monetary penalty. The distinction should remain visible in any security-club artifact register.

## 4. Payment Receipts, Transaction Formats, and Public UI Evidence

The strongest public receipt-related evidence is a workflow, not a receipt screenshot. The official payment page publishes an instruction to email payment details to the university finance address, including UTR number, debit-account holder name, transaction date, and amount [6]. It repeats that students or parents must email the transaction details after paying online and provides a "Download the Format" link [6]. The public evidence therefore supports the existence of a transaction-details format link, but the reviewed public extract does not validate the contents of the linked document as a receipt template.

| Artifact | What is publicly visible | Evidence strength | Safe interpretation |
|---|---|---|---|
| MUJ SLCM landing page | Welcome, sign-in, parent-login wording [3] | High for the unauthenticated surface | No fee UI is visible in this public extract; do not infer that protected fee functions do not exist |
| MUJ payment page | SLCM URL for existing students; SpaceBasic for hostel and mess [6] | High and official | Public payment routing is documented |
| Transaction-details workflow | UTR, debit-account holder, transaction date, amount, email instruction, and format link [6] [6] | High for workflow fields | This is not the same as a publicly viewable payment-receipt screen |
| Hostel fee page | Advice to retain receipts and transaction references [5] | High for advice | Receipt retention is recommended; the receipt format itself is not shown |
| SLCM SWITCH repository | Login, timetable, grades, GPA/CGPA, and attendance feature descriptions [16] | Medium for the repository's own claims, low for official UI | A student-built interface is not proof of the official fee module |
| MUJStella | Site identifies itself as an independent student platform not affiliated with MUJ [19] | Low for official fee evidence | Any fee or receipt claim from it must be treated as third-party and non-authoritative |
| Indexed receipt lead | Scribd page could not load a required part of the site in the reviewed retrieval [28] | Very low | No receipt fields, amount, or provenance should be reproduced from this lead |

### Case study: official transaction fields versus unofficial interface claims

The official payment page names the fields that the university wants after an online payment: UTR, debit-account holder, transaction date, and amount [6]. A student-built repository instead describes a mobile interface for the university SLCM website with login, timetable, grades, GPA/CGPA, and attendance features [16] [16]. Neither source supplies an authenticated fee screenshot.

The mechanism is authority separation. The official page is suitable for documenting a payment-confirmation requirement, while the repository is suitable only for documenting what its author claims to build. The independent MUJStella site's explicit non-affiliation disclaimer makes the same boundary even clearer [19]. The recommendation is to place third-party artifacts in a separate evidence tier, never copy student PII or transaction identifiers, and never use a community screenshot to establish an official receipt format.

A screenshot of the public login page can document the exposed boundary, but it should be labeled as a login screenshot rather than a fee-module screenshot. No authenticated fee-module screenshot was verified in this research. Obtaining one would require access to a student or parent account and is outside a public-only review.

## 5. Due Dates, Late Fees, Refunds, and Fee Waivers

### Due-date and late-fee matrix

| Document and scope | Date or rate | What it controls | Confidence and limitation |
|---|---|---|---|
| Academic Calendar 2026-27 | Last date for fee payment: 16 July only [17] [17] | General calendar fee-payment milestone | High for the calendar entry; it does not itself state a late-fee amount in the cited line |
| Hostel continuation circular 2026-27 | Hostel payment by 5 July 2026 [29] | Room reservation and continuation | High for hostel scope; nonpayment is tied to voluntary room vacation and reallocation [29] |
| Annual course-fee notice 2025-26 | Course-fee deadline 18 July 2025 [31] | Historical annual course fee payment | High for 2025-26, not a current 2026-27 deadline |
| Annual course-fee notice 2025-26 | Late fee fine at 12% per annum on amount due [31] | Historical late-fee rule | Medium because the extracted clause is truncated after the visible wording; trigger and calculation convention should not be invented |
| 2026 payment page | No explicit recurring-student due date, late-fee rule, receipt format, or waiver in the reviewed page content [6] | Current payment-page disclosure | High as an evidence-gap statement about that page, not proof that no separate notice exists |

The 2025 notice also says that hostel and mess fees are in Annexure 2 and that payment is through the SpaceBasic app only [31]. It specifies cashless payment and provides online, bank-transfer, and demand-draft instructions for the course-fee context [31]. These historical details are useful for comparing document versions, but they should not be silently applied to 2026-27.

### Withdrawal refunds are not late fees

MUJ's Indian-student refund page labels the policy as a refund of fee in case of withdrawal of admission [18]. It says the student is provisionally admitted on completion of fee payment and that an approved refund follows the listed guidelines [18]. The exact table is as follows.

| Withdrawal timing | Refund or deduction | Source qualification |
|---|---|---|
| Up to 30 September 2026 | Full refund [18] | Refund of aggregate fees, with caution deposit excluded by the table note |
| 1 October to 31 October 2026 | Deduction of INR 1,000 as processing fee [18] [18] | This is a processing deduction, not a late-fee rate |
| 15 days or more before the formally notified last admission date | 100% [18] | Applies when the later admission-schedule rule is triggered |
| Less than 15 days before the formally notified last admission date | 90% [18] | Timing is relative to the formally notified date |
| 15 days or less after the formally notified last admission date | 80% [18] | Timing is relative to the formally notified date |
| More than 15 and up to 30 days after the formally notified last date | 50% [18] | Timing is relative to the formally notified date |
| More than 30 days after the formally notified last date | 0%, or nil [18] | No refund in that row |

The page says the table is inclusive of course fee but exclusive of caution deposit, and defines the program's last admission date as the day before orientation [18]. It also requires the withdrawal application format, surrender of the ID card and original fee receipt, and a dues-clearance certificate [18]. Eligible refunds are stated to be paid within 45 days from receipt of the hard copy of the application [18], while application and entrance-test fees are non-refundable [18]. The policy warns that its information is indicative and may change [18].

### Fee-waiver evidence

The official scholarship page is the relevant fee-waiver artifact. It repeatedly describes waivers against annual tuition fee, so the amounts below should not be treated as automatic reductions of hostel, mess, registration, or caution-deposit charges unless a separate rule says so.

| Scholarship or concession | Publicly stated amount, quota, or threshold | Policy condition |
|---|---|---|
| Sir M Visvesvaraya Scholarship | Category A 50%, Category B 40%, Category C 30%; five, ten, and ten scholarships respectively [14] | Thresholds shown as 80%, 70% to below 80%, and 60% to below 70%; continuity requires CGPA 7.0 without backlog [14] |
| TMA Pai Merit Scholarship | Three per UG program; where N is below 1,000, categories are 100%, 50%, and 25% [14] [14] | Topper ranking and at least 80% selection criteria are stated; continuity requires CGPA 8.5 without backlog [14] |
| Rajasthan Merit Scholarship | One per program, limited to INR 1 lakh or annual tuition fee, whichever is lower [14] | Includes at least 80% aggregate and Rajasthan-school and domicile conditions [14] |
| Local-region student scholarship | Two per program and 50% of annual tuition fee [14] | Nearby-village eligibility and combined parental annual income below INR 12 lakh are stated [14] |
| Sibling financial assistance | 20% of annual tuition fee [14] | Both siblings must enroll in the same academic session; the concession is offered to the junior sibling and income conditions apply [14] |
| MUJ graduate concession | Category A 20%, B 15%, C 10% on annual tuition fee [14] | The page ties categories to prior CGPA thresholds and requires CGPA 7.5 without backlog for continuity [14] |
| PG merit, non-M.Tech programs | Category A 50% and Category B 25% of annual tuition fee [14] | The page uses 70% and 60% thresholds and topper ranking [14] |
| Differently abled students | 20% for 40% to 75% disability and 50% above 75% [14] | Applies to applicable UG and PG programs in the page table |
| MBA merit scholarships | 50%, 40%, 30%, and 20% bands for stated CAT/XAT or MAT/CMAT/ATMA criteria [14] | The page says MBA awards are first-come, first-served based on full fee payment [14] |

The scholarship rules state that students must apply through the proper channel, may apply for only one type per academic session, and receive awards only for the actual or minimum duration of the enrolled program [14]. They also state that indiscipline can terminate a scholarship and that awards are subject to competent-authority approval [14].

### Case study: a historical late-fee clause beside a current evidence gap

The 2025-26 notice is the only verified MUJ artifact in the reviewed set that exposes a late-fee rate, and it says 12% per annum on the amount due [31]. The 2026 payment page, by contrast, exposes payment routing and transaction fields but no explicit recurring-student late-fee rule in the reviewed content [6].

The mechanism is temporal policy drift or document separation: a late-fee rule may live in an annual circular, while the payment page acts only as a routing and reconciliation page. The evidence does not establish which explanation is correct. The safe decision is to label the 12% rate as historical 2025-26, preserve the truncated wording, and mark the 2026-27 recurring late-fee rule as unanswered rather than extrapolating.

## 6. Artifact Coverage, Transport Gap, and Document Quality

The requested artifact classes do not have equal public coverage. Official MUJ pages are strong for hostel, mess, payment routing, refund policy, and scholarship rules. Program-fee coverage is partial because some pages display complete tables while others expose only a fee-section heading in the reviewed extract. The 2025 annual notice points to course-wise and batch-wise Annexure 1 values [31], but that does not by itself make every amount visible or current.

| Requested artifact class | Status after public review | Best evidence | Confidence |
|---|---|---|---|
| Fee structures per program | Partially verified | Official index and representative LLB and M.Tech tables [2] [25] [23] | Medium to high for cited pages; not exhaustive |
| Hostel fee schedule | Verified for 2026-27 double occupancy | Official hostel table [5] | High |
| Mess fee schedule | Verified for 2026-27 | Official mess page [7] | High |
| Transport fee schedule | Not verified in authoritative MUJ material reviewed | Payment page names course SLCM and hostel/mess SpaceBasic routes but not a transport schedule [6] | Low; absence from reviewed pages is not proof of no schedule |
| Payment receipt format | Workflow and format link verified; file contents not validated | UTR and transaction fields plus Download the Format link [6] | Medium |
| Due-date circulars | Verified for separate course-calendar and hostel scopes | Calendar and hostel circular [17] [29] | High, with scope distinctions |
| Late-fee rule | Historical 2025-26 rate only | 12% per annum wording [31] | Medium for historical clause, low for current applicability |
| Fee-waiver documents | Verified official scholarship tables | Scholarship page [14] [14] | High for published rules, subject to approval and continuity conditions |
| Public fee-module screenshot | Not verified | Public landing page shows login only [3] | Low for any claim about the protected UI |

Transport is the clearest unresolved requested item. The absence of a transport amount in the reviewed official payment-page and fee-page extracts should be reported as a search-result gap. It should not be converted into a claim that MUJ has no transport service or that transport is free. A future public-only update should look for a separately titled official transport notice or a prospectus annexure, but should not probe the portal or provider interfaces.

Document quality also varies. The 2026 hostel and mess HTML tables yield clean numbers, while the annual PDF extraction contains OCR corruption in some mess and final-year fields [29]. The right response is not to repair the OCR by guesswork. The clean mess page should support the INR 79,000 transcription [7], while garbled PDF fields remain marked as unreadable until an authoritative visual copy can be reviewed.

The 2025 notice exposes another versioning issue: it prints the student portal as `https://mujslcm.jaipur.manipal.edu:122/` [31], whereas the 2026 payment page prints the bare HTTPS hostname [6]. This is an observable difference in published URL form. It is an inference, not proof of a service migration, port exposure, or vulnerability. No connection test should be performed merely to resolve that question.

## 7. Concise Analytic Reasoning and Safe OSINT Boundary

I cannot provide hidden private chain-of-thought. The following is a concise, reproducible evidence trail that gives the decision logic without exposing private internal deliberation.

| Observation | Mechanism or explanation, labeled as inference | Implication | Safe recommendation |
|---|---|---|---|
| Public SLCM page shows sign-in and parent-login wording [3] | **Inference:** fee functions may be protected behind authentication, but the page alone cannot establish their implementation | Public UI evidence stops at the login boundary | Capture only the public page; do not attempt account discovery, password testing, or bypass |
| Official payment page routes course payments to SLCM and hostel/mess to SpaceBasic [6] | **Inference:** different fee classes may have different providers or reconciliation paths | A fee artifact register needs a provider and scope field | Record the route as published; do not test cross-provider sessions or transaction callbacks |
| Official workflow asks for UTR, account-holder name, date, and amount [6] | **Inference:** payment reconciliation depends on transaction metadata | Public examples may expose sensitive financial identifiers | Redact UTRs, names, account numbers, and receipts from club materials |
| Hostel page publishes values but says some payment modes appear after login [5] | **Inference:** public policy and protected transaction execution are intentionally separate surfaces | Amount research does not require accessing payment functions | Use the public table only; do not log in or submit a booking/payment form |
| 2025 and 2026 documents publish different portal URL forms [31] [6] | **Inference:** the published documents may reflect different operational versions or communication templates | Stale links can cause reporting errors and phishing confusion | Store source date and exact URL string; do not infer a security defect |
| 2025 late-fee wording exists but 2026 payment page does not state a rule [31] [6] | **Inference:** a late-fee rule may be annual, separate, or changed; the evidence cannot choose among these explanations | Historical rates must not be presented as current | Request or locate a current public circular, rather than extrapolate |
| Student-built and independent sites are not official MUJ sources [16] [19] | **Inference:** their UI claims may reflect implementation attempts or convenience tools, not the university system | Third-party screenshots have low evidentiary authority | Label them non-authoritative and never reproduce student data |

For a university security club, public-only collection should mean reading official HTML and PDFs, recording exact URLs and visible publication or academic-year context, and preserving redacted screenshots of unauthenticated pages. It should not mean submitting login forms, enumerating student identifiers, replaying payment references, guessing file paths, scanning ports, bypassing access controls, or downloading another person's receipt. Those actions would move from OSINT into unauthorized access or privacy-invasive testing.

A safe evidence record should contain the source URL, retrieval date, academic-year label, artifact type, visible scope, exact quoted field, confidence, and redaction status. It should also distinguish a source statement from an analyst calculation. For example, the equality between INR 167,372 plus INR 15,378 and INR 182,750 is a useful arithmetic reconciliation, but it should be labeled as an analyst check rather than quoted as a separate university rule.

## 8. Synthesis: What the Fee Ecosystem Reveals

The major artifacts differ across authority, scope, time horizon, and operational exposure. Comparing them directly prevents the most likely reporting mistakes.

| Dimension | Official program pages | Official hostel and mess pages | Annual notices and calendar | Third-party artifacts |
|---|---|---|---|---|
| Authority | Primary MUJ admissions content [2] | Primary MUJ service-fee content [5] [7] | Primary MUJ notices, but document-specific [29] [17] | Non-authoritative or unaffiliated by their own descriptions [16] [19] |
| Scope | Program, level, component, currency, and sometimes admission-year | Double occupancy, mess year, optional services, room rules | A specific academic year, deadline, or withdrawal event | Whatever the creator claims to implement or display |
| Time horizon | Some pages carry older applicability, such as admission through academic year 2025 [23] | Explicit 2026-27 tables [5] [7] | Strong date specificity, including 5 July 2026 and 16 July in the 2026-27 calendar [29] [17] | Unknown unless repository or page metadata is independently verified |
| Transaction exposure | Mostly public policy tables | Amounts public, some payment modes login-gated [5] | Payment channels and transaction-email requirements public [6] | Potentially shows a claimed interface, but not an official receipt |
| Main trade-off | Detail can be high but stale or incomplete by program | Numeric clarity is high, but components can be confused | Best for deadlines, but rules may be historical or scope-limited | Broad discovery value, low evidentiary authority and higher privacy risk |

Three tensions matter most. First, the public payment page is more operationally specific than the public SLCM landing page: it tells students where to pay and what metadata to email, yet it does not show the fee screen. This suggests a deliberate or practical separation between public communication and authenticated transaction processing, but it does not prove a particular architecture.

Second, the hostel values are internally reconcilable across documents, while the late-fee evidence is not temporally reconciled. Hostel accommodation plus housekeeping equals the residential amount in the annual circular, and adding the clean mess value produces the circular's full-year total [5] [29] [7]. By contrast, the 2025 late-fee rate has no current 2026 counterpart in the reviewed payment page [31] [6]. The decision is therefore different for each artifact: reconcile the hostel arithmetic, but preserve the late-fee gap.

Third, refunds and waivers address different events. The refund policy governs withdrawal timing, documentation, and deductions [18]. The scholarship page governs eligibility, annual tuition concessions, continuity, and authority approval [14] [14]. Treating a scholarship as a refund, or treating a processing deduction as a late fee, would produce a materially wrong fee model.

The actionable synthesis is a layered register: (1) authoritative amount tables, (2) dated circulars, (3) workflow and provider routes, (4) protected UI claims, and (5) third-party leads. Each row should carry a validity period and a confidence level. This structure captures what is public without implying access to the protected SLCM fee module.

## VERDICT

**Overall confidence: High for the existence and wording of the cited official public artifacts; medium for a complete MUJ fee inventory; low for the unanswered transport, current late-fee, receipt-template, and authenticated-UI questions.**

As of the 2026-08-25 research date, the public record supports the following verdict:

1. MUJ publicly documents a fee ecosystem spanning program tuition pages, hostel and mess schedules, payment routes, withdrawal refunds, and scholarship waivers. The program pages expose representative component-level amounts, including LLB and M.Tech examples [25] [23].
2. For 2026-27, the most defensible current numeric records are the hostel table, mess table, annual hostel circular, and calendar entry. The hostel table distinguishes accommodation, housekeeping, refundable deposit, and optional services [5]. The mess page separately states INR 79,000 [7].
3. The official payment page publicly exposes the SLCM and SpaceBasic routing and a transaction-details email workflow, but not the contents of a validated receipt template or a fee-module screenshot [6] [6].
4. A 12% per annum late-fee rate is verified only in the 2025-26 annual notice, with the extracted clause truncated. It must be treated as historical and not applied to 2026-27 [31].
5. No authoritative transport-fee schedule, current recurring-student late-fee rule, authenticated fee-module screenshot, or fully validated public receipt format was established. These are unanswered public-artifact questions, not evidence that the items do not exist.
6. No security vulnerability is established by the public evidence. The safe conclusion is an exposure map of public fee communications and trust-boundary clues, not a finding about authentication, authorization, payment integrity, or the supplied technology stack.

For a university security club, the most valuable next deliverable is not an access attempt. It is a version-controlled, redacted artifact ledger that records each official URL, academic-year scope, amount component, provider route, policy qualifier, and evidence confidence. That ledger will make future changes, stale links, and contradictory deadlines visible while respecting the public-only boundary.

## References

1. *Course Fee - Manipal University Jaipur*. https://jaipur.manipal.edu/fee-structure.php
2. *Manipal University Jaipur - 71 years of legacy of Manipal Education*. https://jaipur.manipal.edu/indian-fee-structure.php
3. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
4. *Manipal University*. https://muj.slcm.jaipur.manipal.edu/
5. *Hostel Fee - Manipal University Jaipur*. https://jaipur.manipal.edu/hostel-fees.php
6. *Pay Fee Online - Manipal University Jaipur *. https://jaipur.manipal.edu/pay-fee-online.php
7. *MESS FEE - Manipal University Jaipur*. https://jaipur.manipal.edu/mess-fees.php
8. *Fee Refund Policy 2026 Manipal Academy of Higher Education (MAHE)*. https://www.manipal.edu/content/dam/manipal/mu/documents/Admissions/adm2026/mahe_refund_policy_v2.pdf
9. *Terms of Service*. https://www.manipal.edu/content/dam/manipal/mu/documents/Admissions/adm2021/Payment%20Terms%20%26%20Conditions.pdf
10. *Fee Refund Policy 2026 – AICTE Approved programs Manipal Academy of Higher Education (MAHE)*. https://www.manipal.edu/content/dam/manipal/mu/documents/Admissions/adm2026/mahe_refund_policy_v4_AICTE_Approved_programsotherthanMBA.pdf
11. *Scholarship - Manipal University Jaipur*. https://www.jaipur.manipal.edu/dsw-scholarship.php
12. *General CategoryStudents Kasturba Medical College, Manipal*. https://www.manipal.edu/content/dam/manipal/mu/documents/Admissions/adm2026/2026-27%20General%20Fees%20as%20on%2004-07-2026.pdf
13. *3*. https://www.manipal.edu/content/dam/manipal/mu/documents/Admissions/adm2026/2026%20Prospectus%20File%2077_Section%203%20Hostel%20Fees_20.07.2026.pdf
14. [Scholarships and Financial Support Indian student - Manipal
    University Jaipur](https://jaipur.manipal.edu/indian-scholarship.php)
15. *GitHub - Anushkakumar10/muj_slcm · GitHub*. https://github.com/Anushkakumar10/muj_slcm
16. *GitHub - DK10WS/SLCM_APP: App Version for MUJ SLCM · GitHub*. https://github.com/DK10WS/SLCM_APP
17. *AC calender -2026-27.cdr*. https://jaipur.manipal.edu/img/pdf/academicrules/AC-calender-2026-27.pdf
18. *Course Fee Refund Rules - Manipal University Jaipur*. https://jaipur.manipal.edu/indian-refund-policy.php
19. *MUJStella - Student Platform for Manipal University Jaipur*. https://mujstella.in/
20. [B.Tech Computer Science & Engineering (Data Science) | Faculty of Science, Technology and Architecture (FoSTA)
    At Manipal University
    Jaipur, MUJ](https://jaipur.manipal.edu/foe/b-tech-data-science.php)
21. [B.Tech Computer Science & Engineering (Data Science) | Faculty of Science, Technology and Architecture (FoSTA)
    At Manipal University
    Jaipur, MUJ](https://jaipur.manipal.edu/foe/b-tech-data-science.php#Program-Fee)
22. [B Tech Electrical & Electronics Engineering | Faculty of Science, Technology and Architecture (FoSTA) At Manipal University Jaipur, MUJ
  ](https://jaipur.manipal.edu/foe/b-tech-electrical-electronics.php)
23. *M.Tech Structural Engineering | Faculty of Science, Technology and Architecture (FoSTA) At  Manipal University Jaipur, MUJ*. https://jaipur.manipal.edu/foe/m-tech-structural.php#Program-Fee
24. *M.Tech Structural Engineering | Faculty of Science, Technology and Architecture (FoSTA) At  Manipal University Jaipur, MUJ*. https://jaipur.manipal.edu/foe/m-tech-structural.php
25. * LLB (Bachelor of law) | Faculty of Law(FOL) At Manipal University Jaipur, MUJ*. https://jaipur.manipal.edu/fol/bachlor-LLB.php#Program-Fee
26. [M.Tech. (Data Science) | Faculty of Science, Technology and Architecture (FoSTA) At Manipal University Jaipur,
    MUJ](https://jaipur.manipal.edu/foe/m-tech-data-science.php#Program-Fee)
27. [M.Tech. (Data Science) | Faculty of Science, Technology and Architecture (FoSTA) At Manipal University Jaipur,
    MUJ](https://jaipur.manipal.edu/foe/m-tech-data-science.php)
28. *Client Challenge*. https://www.scribd.com/document/853413558/Updated-Payment-Receipt
29. *• �r� JIV/1;�·. ·\*. https://jaipur.manipal.edu/img/pdf/Annual-Fee-Payment-for-the-AY-2026-2027.pdf
30. *• �r� JIV/1;�·. ·\*. https://jaipur.manipal.edu/img/pdf/Annual-Fee-Payment-AY-2026-2027-NRI.pdf
31. *Notification Annual Fee Payment Ay 2025 26*. https://jaipur.manipal.edu/img/pdf/Notification_Annual-Fee-Payment-AY-2025-26.pdf
32. *http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf*. http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf
