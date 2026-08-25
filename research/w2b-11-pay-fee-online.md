# MUJ SLCM Fee Payments: Public-Evidence Security Report

## Executive Summary

This report examines the publicly visible fee-payment surface associated with Manipal University Jaipur (MUJ), especially the official "Pay Fee Online" page and the MUJ SLcM login domain. It is an OSINT report, not a penetration test. It uses only public pages and documents, and it does not attempt authentication, submit payment forms, enumerate authenticated routes, or test security controls.

- **Primary Student Route**: MUJ's official page directs existing students to the MUJ SLcM portal at https://mujslcm.jaipur.manipal.edu/ [3] -> treat this as the authoritative starting point, but do not assume that the public login page proves what authenticated fee modules contain.
- **Separated Hostel Route**: The same official page states that hostel and mess fees can be paid through the SpaceBasic app [3] -> keep academic-fee, hostel-fee, and mess-fee investigations as separate payment journeys.
- **Bank Reconciliation**: MUJ publishes a Canara Bank account-name, account-number construction, IFSC, branch, and an email-reconciliation requirement containing UTR, debit-account-holder name, transaction date, and amount [3] -> reconciliation data is a material security and privacy asset even when the payment itself occurs outside SLcM.
- **Gateway Attribution**: No public MUJ page reviewed here names BillDesk, Razorpay, CCAvenue, SBI ePay, or Cashfree as the academic-fee provider [3]. A separate public search result identifies an MUJ-branded NTT DATA Pay URL [9], and NTT DATA describes its own service as a payment-gateway platform [15], but public evidence does not prove that the URL is linked from authenticated SLcM or that it is the only or current MUJ gateway.
- **Public Fee Data**: MUJ's fee-structure HTML page is a programme directory rather than a complete fee schedule, while the Indian-fee page states that tuition, registration, and caution-deposit amounts can change and that registration is non-refundable while the caution deposit is refundable on programme completion [5] [4] -> researchers should archive the exact programme page and academic-year document used for any payment decision.
- **Refund Process**: MUJ's Indian-student refund policy gives dated refund bands, requires an application, original fee receipt, surrendered ID card, and dues-clearance certificate, and says eligible refunds are paid within 45 days of receiving the hard-copy application [1] -> receipt retention and a documented offline workflow are central controls.
- **Hostel Exception**: The public hostel page publishes Academic Year 2026-27 double-occupancy figures and optional-service figures, says payment modes are shown inside the room-booking portal, and says gateway convenience charges may apply [6] -> the hostel flow is not evidence of the academic SLcM flow.
- **Threat Model**: Jamia's official advisory describes fake fee requests, impersonation email accounts, and fake QR codes, while cases reported by The420 and CYFIRMA describe cloned university websites used or suspected for fee and data collection [12] [10] [13] -> brand and domain verification should be treated as a payment control, not merely an awareness message.
- **Evidence Boundary**: The public record reviewed does not expose an authenticated fee screen, a MUJ receipt layout, a complete readable course-fee PDF, a transaction-template document, a confirmed gateway callback design, or a confirmed MUJ payment incident -> those items remain Unknown rather than being inferred.

## 1. Scope, Method, and Evidence Rules

The target is the public MUJ fee ecosystem, not a live security assessment. The official payment page is https://www.jaipur.manipal.edu/pay-fee-online.php, the student portal advertised there is https://mujslcm.jaipur.manipal.edu/, and the separately discovered branded payment URL is https://muj-payservices.nttdatapay.com/DirectPay/MUFee. The public SLcM landing page visibly identifies itself as "WELCOME TO MUJ PORTAL" and presents Parent Login and Student Login options [2]. The public login evidence does not show a fee function, payment amount, receipt, or gateway name [2].

The report uses a confidence taxonomy. "Observed" means the wording or link is present in a public source. "Corroborated" means a second source supports the same proposition. "Inference" means an analytical conclusion constructed from observed facts; it is not presented as a fact about MUJ. "Unknown" means the public evidence does not establish the proposition. This distinction matters because a payment URL discovered in search results is not automatically proof of an active integration, and a login form is not proof of a vulnerable or secure backend.

The requested application-stack description in the research brief - ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 identity - is treated here as user-supplied context, not independently verified evidence. The public login page does show a Microsoft password-reset destination and MUJ email-domain handling in its markup, but that is insufficient to make a complete identity-architecture claim. No exploit or unauthorized-access instruction is included.

## 2. What the Official MUJ Payment Page Actually Publishes

The clearest public workflow is a set of parallel routes, not one fully documented checkout. For existing students, MUJ labels the online route as the Student Portal and links to https://mujslcm.jaipur.manipal.edu/ [3]. The public login page then shows Parent Login and Student Login [2]. The page does not expose a fee amount, fee category selector, payment-method list, transaction-status screen, receipt format, or named gateway in the publicly readable content [3].

The official page separately says that hostel and mess fees can be paid through SpaceBasic [3]. This is a meaningful architectural distinction. It indicates that at least one residential-fee journey is not documented as the same public route as ordinary existing-student fee payment. It does not prove whether SpaceBasic is a gateway, a room-management application, a merchant front end, or an orchestration layer.

MUJ also publishes an electronic-transfer path. The page names Canara Bank, the account name MANIPAL UNIVERSITY JAIPUR, the IFSC CNRB0003563, a current-account type, and a branch address at Pushpraj Tower, Near RIICO, Narayan Nagar, Chirota Road, Bagru - 303007 [3]. It says the account number is formed from MUVAN followed by the student's registration or application number, and gives MUVAN123456789 as an example [3]. Because this is an account-number construction rule, students should independently verify the official page and registration/application identifier before transferring funds. That recommendation is a safety practice, not a claim that the published rule is fraudulent.

The page requires students or parents to email payment details after paying online. The visible required fields are UTR number, debit-account-holder name, date of transaction, and amount [3]. It also publishes Student Finance and Accounts Office telephone extensions and the address student.finance@jaipur.manipal.edu [3]. The public evidence therefore supports an explicit reconciliation workflow, but not an automated payment-status API or an electronic receipt-generation design.

| Public route | Evidence | What is established | What remains unknown |
|---|---|---|---|
| Existing-student online payment | MUJ Pay Fee page, https://www.jaipur.manipal.edu/pay-fee-online.php [3] | Portal advertised as https://mujslcm.jaipur.manipal.edu/ | Authenticated fee screens, gateway, callback, receipt |
| Hostel and mess | MUJ Pay Fee page [3] | SpaceBasic is named | Exact provider role and transaction lifecycle |
| Domestic transfer | MUJ Pay Fee page [3] | Canara Bank details and post-payment email reconciliation | Automated matching, alerting, and exception handling |
| NRI wire | MUJ Pay Fee page [3] | USD, Canara Bank, SWIFT CNRBINBBBFD, beneficiary account 120030244406 | Currentness of correspondent-bank handling and receipt design |
| Public branded payment lead | https://muj-payservices.nttdatapay.com/DirectPay/MUFee [9] | MUJ name/address and NTT DATA Pay title appear in search evidence | Whether it is current, linked from SLcM, and used for which fee |

**Decision insight:** The public route map is sufficiently reliable for safe user-facing documentation, but insufficient for a technical data-flow diagram. The safe diagram should show SLcM, SpaceBasic, bank transfer, and the NTT DATA URL as separate evidence nodes with the latter explicitly marked "unconfirmed integration."

## 3. Gateway Attribution and the NTT DATA Pay Lead

The named-gateway question cannot be answered affirmatively for BillDesk, Razorpay, CCAvenue, SBI ePay, or Cashfree from the public evidence reviewed. Searches for those names returned generic gateway pages and the MUJ payment page, but no official MUJ statement associating one of those providers with MUJ. The official page's visible payment routes name the Student Portal, SpaceBasic, electronic transfer, and NRI wire transfer; it does not name one of the five requested gateways [3] [3].

A separate search result identifies https://muj-payservices.nttdatapay.com/DirectPay/MUFee with the title "Manipal University Jaipur | MUJ - NTT DATA Pay" and the MUJ campus address [9]. This is stronger than a generic provider mention because the URL is MUJ-branded and the page title associates MUJ with NTT DATA Pay. However, direct page extraction produced no readable checkout fields or payment instructions, and no public evidence reviewed here links the URL from the authenticated SLcM account. The appropriate classification is "public lead, not confirmed end-to-end integration."

NTT DATA's own public documentation describes its service as a payment gateway integration platform, references transaction API documentation, and claims PCI-DSS compliance and enterprise-grade security [15]. Those are provider-level statements. They do not establish that the MUJ URL currently uses a particular API version, merchant configuration, return URL, webhook, receipt template, or refund process. Nor do they establish that the provider is one of the requested five; NTT DATA is a separate provider name.

| Candidate gateway/provider | Public MUJ attribution found? | Evidence status | Safe conclusion |
|---|---:|---|---|
| BillDesk | No | Generic gateway search result only | Unknown for MUJ |
| Razorpay | No | Generic comparison/search results only | Unknown for MUJ |
| CCAvenue | No | Generic provider result only | Unknown for MUJ |
| SBI ePay | No | No MUJ attribution found | Unknown for MUJ |
| Cashfree | No | No MUJ attribution found | Unknown for MUJ |
| NTT DATA Pay | Yes, as a public branded URL | URL/title/address observed, integration unconfirmed [9] | Plausible lead, not proof of active SLcM linkage |

**Inference:** The presence of a provider-hosted MUJ URL suggests that at least one payment service may exist outside the visible SLcM landing page. It does not show whether this is admissions, annual fees, hostel fees, a legacy route, or a test/unused page. The research club should not label NTT DATA the confirmed MUJ academic-fee gateway without an official public link or an authorized institutional confirmation.

## 4. Fee Structures and Public Documents

The page at https://jaipur.manipal.edu/fee-structure.php is not, on the evidence extracted, a single fee table. It is a directory listing schools, departments, programmes, and academic categories, including engineering, computer applications, design, arts, business, and postgraduate programmes [5]. It does not itself provide a complete current-year amount table, payment mode, refund rule, or downloadable fee schedule in the readable sections [5] [5]. This is important for OSINT accuracy: a directory page should not be cited as if it were a programme fee invoice.

The Indian-fee page gives a policy-level caveat: tuition fee, registration fee, and caution deposit are subject to change and approval by the Fee Fixation Committee. It states that registration fee is non-refundable and caution deposit is refundable on completion of the programme [4]. It also states that fees can be paid by demand draft in favour of Manipal University Jaipur, payable at Jaipur [4]. This is an official payment mode, but it does not prove that demand draft is the only or current mode for every programme.

The official Pay Fee page links an annual course-fee notification for Academic Year 2026-27 and an NRI notification [3] [3]. The downloaded course-fee PDF evidence was materially incomplete: the readable portion was Annexure-2 concerning hostel accommodation, and course-fee amounts and installment schedules were not readable [14]. The same document exposes a hostel deadline of 5 July 2026 and says the hostel fee should be deposited through SpaceBasics only [14]. Its OCR contains garbled numbers, including a readable residential-dwelling figure of Rs 182,750 and a full-year total of Rs 261,750, but the surrounding text is incomplete [14]. Those figures should not be used as an academic course-fee schedule.

| Document/page | Public purpose | Readable evidence | Reliability limitation |
|---|---|---|---|
| Pay Fee Online | Payment-route directory | SLcM, SpaceBasic, bank, NRI, contacts, notifications [3] | Does not reveal authenticated checkout |
| Course Fee directory | Programme navigation | Programme/school listings [5] | Not a complete amount schedule |
| Indian fee page | Fee-policy/payment statement | Change caveat, non-refundable registration, refundable caution deposit, demand draft [4] | Amounts not generally visible in extracted content |
| AY 2026-27 notification | Annual notification | Hostel annexure, SpaceBasics-only wording, deadline [14] | OCR/incomplete document; course-fee section unreadable |
| NRI notification | NRI/annual notification link | Extracted content substantially duplicated hostel annexure [11] | NRI course-fee route and amounts not readable |

**Decision insight:** For a university security club, the fee-document risk is not only falsification. It is also version ambiguity. A payment instruction should carry the exact source URL, academic year, programme, category, publication/update date if available, and a hash or archived copy maintained by the university under an authorized process.

## 5. Receipt, Reconciliation, and Refund Flow

The public record supports a reconciliation workflow more clearly than a receipt format. After online payment, MUJ asks students or parents to email UTR number, debit-account-holder name, transaction date, and amount to student.finance@jaipur.manipal.edu [3]. The page links a "Required Transaction details" document [3], but the document could not be read by the public extraction tool. Therefore, no additional fields should be invented, and no claim should be made about receipt number, merchant order ID, bank reference, GST fields, QR code, or PDF layout.

The Indian-student refund page states that a refund claim by a provisionally admitted student may be considered on merit, and that refund bands follow the stated UGC-related guidelines [1]. It identifies aggregate fees as inclusive of course fee but exclusive of caution deposit [1] [1]. The readable policy bands are: full refund up to 30 September 2026; a Rs 1,000 processing-fee deduction from 1 October through 31 October 2026; and, for schedules extending beyond 31 October, 100%, 90%, 80%, 50%, or nil refund depending on withdrawal timing relative to the formally notified last admission date [1].

The process is document-heavy. MUJ says withdrawal requests must use the application format available at the Office of Admissions [1]. It requires surrender of the ID card and original fee receipt plus a dues-clearance certificate [1]. Eligible refunds are paid within 45 days of receipt of the hard-copy application [1]. For a request made less than 15 days before the formally notified last admission date or the day before orientation, physical reporting by the candidate, parent, or guardian is mandatory [1]. Application and entrance-test fees, where applicable, are not refundable [1]. The page also says the information is indicative and may change in response to statutory or regulatory notifications [1].

| Refund or reconciliation element | Officially visible rule | Security/operations implication |
|---|---|---|
| Post-payment reconciliation | Email UTR, debit-account-holder name, date, amount [3] | Protect email intake and prevent misattribution |
| Refund scope | Aggregate fees include course fee and exclude caution deposit [1] [1] | Keep fee components separately ledgered |
| Early withdrawal | Full refund up to 30 September 2026 [1] | Preserve policy version and admission-date evidence |
| October withdrawal | Rs 1,000 processing deduction [1] | Explain deduction before payment/withdrawal |
| Later withdrawal | 100%, 90%, 80%, 50%, or nil bands [1] | Enforce date calculations consistently |
| Required documents | Application, original receipt, ID card surrender, dues clearance [1] | Receipt availability is a control dependency |
| Refund timing | Within 45 days of hard-copy application if eligible [1] | Track intake date and status audibly |
| Non-refundable items | Application and entrance-test fees where applicable [1] | Display exceptions distinctly |

**Inference:** Requiring an original receipt and hard-copy application reduces some casual duplicate claims, but it also creates a continuity risk if the student loses the receipt or the institution cannot map the emailed UTR to the ledger. A secure design should support a student-visible transaction history and a controlled reissue process, but the public sources do not show whether MUJ has those capabilities.

## 6. Hostel and Residential Payment Flow

MUJ's public hostel page is more detailed than the public course-fee directory. It says the table is for Academic Year 2026-27 and publishes double-occupancy figures: hostel accommodation Rs 167,372, housekeeping charges Rs 15,378, refundable security deposit Rs 25,475, and total including security deposit Rs 208,225 [6]. It lists laundry for 30 cycles at Rs 8,810 and a health-club option at Rs 12,750 [6].

The page says payment modes such as UPI, internet banking, and credit/debit card are accessible after logging into the room-booking portal [6]. It says room allotment is confirmed only after successful receipt and verification of full hostel fees [6]. It also says payment-gateway convenience charges, if any, are borne by the student and displayed at payment time [6]. These are the strongest public indications of card/UPI capability in the MUJ material reviewed, but they concern the hostel room-booking flow, not necessarily academic fees in SLcM.

The page states that hostel fees are strictly non-refundable after commencement of the academic year and that, where pre-commencement refund eligibility exists, an administrative processing fee of Rs 5,000 is deducted [6]. It gives info.jaipur@elevatecampuses.com for payment queries [6]. The separate annual notification says hostel payment should be completed by 5 July 2026 and through SpaceBasics only [14]. The coexistence of "room-booking portal" language, SpaceBasics references, and a possible provider-hosted payment URL means the public evidence shows a multi-component residential workflow, not a single easily attributable gateway.

## 7. Indian University Payment-Portal Incidents and Lessons

The best official comparator found is Jamia Millia Islamia's advisory dated 16 July 2026. JMI says scammers sent fake fee-payment requests using fraudulent email IDs such as jmi.feescontroller@proton.me and jmi.feescontroller@pm.me, together with fake QR codes, to candidates for specified JMI programmes [12]. JMI says it never requests fee payments through email, WhatsApp, SMS, messages, or phone calls, does not share fee QR codes over email or WhatsApp, and tells users not to scan QR codes or transfer money to an unverified account [12]. It directs new students to pay online by visiting the concerned Faculty, Department, or Centre, and old students to use the JMI student portal; it says official communications use official JMI domains or named portals [12]. Reports of messages or lost money should go to cybercrime.gov.in and ciso@jmi.ac.in [12]. JMI's advisory does not say its university system was breached [12].

A reported Sai Nath University case illustrates lookalike-domain risk. The420 reports that a student seeking admission to a private university in Jharkhand was allegedly cheated of Rs 32,000, that the institution's official presence was said to be sainathuniversity.com and sainathuniversity.net, and that an unauthorised third website, sainathuniversityresult.com, closely mimicked the university's identity [10]. The report says the money did not reach university accounts, the case was under police investigation, and police were examining the alleged role of a Bihar-based designer [10] [10]. These are media-reported allegations and investigation statements, not a judicial finding.

CYFIRMA reports that on 27 December 2025 a cloned website imitating an unnamed prominent Indian university was identified and reported after concerns that it was collecting fees and sensitive information [13]. CYFIRMA says the site resembled the official portal and displayed academic content, but does not name the university, domain, IP, hosting, or specific fields collected in that case [13]. The report's broader discussion identifies student-data categories such as names, mobile numbers, email addresses, residential details, academic information, government identifiers, and banking or payment data [13]. Those general categories must not be presented as proof that the unnamed clone collected every field.

A further reported CSJMU case says Chhatrapati Shahu Ji Maharaj University identified five fake websites using its name and offering services from admissions to result processing [16]. The sites allegedly used the same logo, photographs, and interface layout and may have been used to collect personal data, fees, or forged documents [16]. The report says CSJMU directed users to csjmu.ac.in, warned against lookalike domains and third-party payment portals, and advised against sharing credentials, Aadhaar details, or payment information [16] [16]. It does not establish a confirmed payment loss or name the five domains.

| Case | Confirmed public fact | Payment relevance | Limitation |
|---|---|---|---|
| JMI advisory | Fake emails and QR codes; official-channel rules [12] | Direct impersonation and QR-payment risk | No claim of JMI system breach |
| Sai Nath report | Lookalike university site; alleged Rs 32,000 loss; police investigation [10] | Clone can divert admission fees | Media report; allegations remain qualified |
| CYFIRMA report | Unnamed cloned university site reportedly collecting fees/data [13] | Brand trust can enable credential/data/payment harvesting | University and technical indicators undisclosed |
| CSJMU report | Five fake sites offering admissions/results; warning against payments [16] | Lookalike portals can imitate academic workflows | No confirmed loss or domain list in report |

**Decision insight:** The comparator incidents point to the same control family: publish a canonical domain list, prohibit payment requests through informal channels, train users to validate the URL and beneficiary, and provide a rapid reporting route. None of these cases proves that MUJ suffered the same incident.

## 8. Risk Register for the Publicly Observable MUJ Flow

The following register separates evidence from inference. The risk statements are analytical judgments, not claims of compromise.

| Risk area | Public observation | Inference and impact | Priority |
|---|---|---|---|
| Gateway ambiguity | Requested gateways are not named on the public MUJ payment page [3] | Students may be unable to distinguish an official redirect from a clone; provider attribution is difficult | High |
| Multi-route confusion | SLcM, SpaceBasic, bank transfer, NRI wire, and a public NTT DATA URL appear in separate evidence [3] [9] | Different routes can create inconsistent support, receipts, and refund expectations | High |
| Reconciliation email | UTR and payer details are sent to a finance email address [3] | Email is a valuable personal/financial-data intake point and a possible impersonation target | High |
| Receipt dependency | Refund requires original fee receipt [1] | Loss or alteration of a receipt can delay legitimate refunds | Medium |
| Document integrity | Annual PDF extraction is incomplete/OCR-corrupted [14] | Users may misread amounts or rely on stale/garbled copies | Medium |
| Informal-channel fraud | JMI documented fake email and QR requests [12] | Similar social engineering could target any university brand; this is a general threat inference, not MUJ evidence | High |
| Authenticated surface unknown | Public SLcM page shows only login roles and no fee module [2] | External researchers cannot responsibly assert module behavior from the landing page | High for evidence quality, not a confirmed vulnerability |

Recommended defensive work for an authorised university team is limited to governance and verification: maintain an official payment-route inventory; place the canonical links on the official domain; publish the exact provider name per route; bind each receipt to a server-side transaction identifier; monitor lookalike domains and fake QR/email reports; protect the finance mailbox with strong authentication and anti-spoofing controls; and provide a public incident-reporting address. These recommendations do not require or imply testing the live system.

## 9. What Remains Unanswered

| Question | Status | Why it remains unanswered |
|---|---|---|
| Which of BillDesk, Razorpay, CCAvenue, SBI ePay, or Cashfree handles MUJ academic fees? | Unknown | No official public attribution found |
| Is NTT DATA Pay the current academic-fee gateway? | Unconfirmed lead | MUJ-branded search result exists, but no public SLcM linkage or readable checkout evidence [9] |
| What does the authenticated SLcM fee module contain? | Unknown | Public page only shows login and roles [2] |
| What is the MUJ receipt layout? | Unknown | Public template link was not readable; no receipt sample found |
| What fields are in the transaction-details template? | Unknown | The DOCX did not yield readable content |
| Are payment callbacks signed and idempotent? | Unknown | No public technical documentation or authorised test evidence |
| What is the complete current course-fee PDF schedule? | Partially answered | Linked PDF extraction exposed an incomplete hostel annexure, not readable course-fee schedules [14] |
| What is the exact hostel gateway and refund API/process? | Partially answered | Public page gives payment modes and refund policy but not provider/API details [6] |
| Has MUJ suffered a public payment-portal incident? | No confirmed public incident found in this review | Search results produced comparator cases, not a verified MUJ incident |
| What are the applicable failed-transaction timelines for each rail? | Not established here | The retrieved RBI corpus exposed only that a framework was finalised, not the operative table [7] |

## 10. Safe Research Plan for an Authorised University Team

The next steps should be conducted by MUJ or an explicitly authorised assessor, not by attempting to bypass login or probe production endpoints. First, obtain a written route inventory from the Finance and IT owners covering academic fees, hostel/mess fees, NRI transfers, admissions, and refunds. Second, reconcile each route with an official link on the MUJ domain and record the provider, merchant name, allowed payment methods, receipt identifier, refund owner, and escalation contact. Third, obtain a redacted sample receipt and a redacted transaction-details template through institutional channels rather than scraping private student data.

For controlled testing, use a non-production environment and synthetic identities. Test only normal business cases approved in scope: successful payment, user cancellation, bank debit with merchant timeout, duplicate callback, refund initiation, refund failure, and reconciliation mismatch. The objective should be to verify transaction integrity and supportability, not to discover or exploit weaknesses. Evidence should exclude real card data, passwords, UTRs, Aadhaar numbers, and student identifiers.

## VERDICT

**Overall confidence: Moderate for the public route map; low-to-moderate for gateway attribution; low for authenticated-module and receipt-format conclusions.**

The public evidence supports a bounded conclusion: MUJ officially directs existing students to the MUJ SLcM portal, separates hostel/mess payment through SpaceBasic, publishes domestic and NRI bank-transfer instructions, and requires finance-email reconciliation fields [3]. MUJ also publishes a dated refund policy with receipt and hard-copy requirements [1], and a hostel page with 2026-27 amounts, portal payment modes, gateway-charge language, and refund conditions [6].

The evidence does **not** support naming BillDesk, Razorpay, CCAvenue, SBI ePay, or Cashfree as the MUJ academic-fee gateway. It does support recording the MUJ-branded NTT DATA Pay URL as a lead, while preserving the qualification that its current purpose and authenticated SLcM linkage are unconfirmed [9]. The evidence also does not support publishing a receipt schema, callback design, authenticated fee-module map, or claim that MUJ experienced a payment breach.

The practical security verdict is therefore **route ambiguity and impersonation exposure are credible risks, but compromise is not demonstrated**. The strongest public defensive lesson from the JMI, Sai Nath, CYFIRMA, and CSJMU material is to make official domains, payment channels, beneficiary details, receipts, and reporting contacts explicit and easy to verify [12] [10] [13] [16].

## References

1. *Course Fee Refund Rules - Manipal University Jaipur*. https://www.jaipur.manipal.edu/indian-refund-policy.php
2. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
3. *Pay Fee Online - Manipal University Jaipur *. https://www.jaipur.manipal.edu/pay-fee-online.php
4. *Manipal University Jaipur - 71 years of legacy of Manipal Education*. https://jaipur.manipal.edu/indian-fee-structure.php
5. *Course Fee - Manipal University Jaipur*. https://jaipur.manipal.edu/fee-structure.php
6. *Hostel Fee - Manipal University Jaipur*. https://jaipur.manipal.edu/hostel-fees.php
7. *Reserve Bank of India*. https://www.rbi.org.in/commonman/Upload/English/Notification/PDFs/NT6720092019.pdf
8. [[PDF] UGC Fee Refund Policy for Academic Session 2025-26.](https://www.ugc.gov.in/pdfnews/1857727_Fee-Refund-Policy-2025-26.pdf)
9. *Manipal University Jaipur | MUJ - NTT DATA Pay*. https://muj-payservices.nttdatapay.com/DirectPay/MUFee
10. *How a Cloned University Portal Cheated a Student Out of Her Fees - The420.in*. https://the420.in/sai-nath-university-fake-website-student-fraud-agra/
11. *• �r� JIV/1;�·. ·\*. https://jaipur.manipal.edu/img/pdf/Annual-Fee-Payment-AY-2026-2027-NRI.pdf
12. *Advisory Regarding Fee Payment*. https://www.jmi.ac.in/upload/menuupload/Advisory%20Regarding%20Fee%20Payment.pdf
13. *Weaponization of Indian Student Data – An Ecosystem for Phishing, Social Engineering, and Financial Fraud - CYFIRMA*. https://www.cyfirma.com/research/weaponization-of-indian-student-data-an-ecosystem-for-phishing-social-engineering-and-financial-fraud/
14. *• �r� JIV/1;�·. ·\*. https://www.jaipur.manipal.edu/img/pdf/Annual-Fee-Payment-for-the-AY-2026-2027.pdf
15. *NTT DATA Payment Services India Documentation*. http://in.nttdatapay.com/docs
16. *CSJMU Alert: Five Fake Websites Using Varsity Name Offer Admissions and Results - The420.in*. https://the420.in/kanpur-csjmu-5-fake-websites/
