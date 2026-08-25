# Digest: w2b-11-pay-fee-online.md

## REPORT
Source file: w2b-11-pay-fee-online.md (MUJ SLCM Fee Payments: Public-Evidence Security Report)

## ANSWER SUMMARY
- Official pay-fee page routes existing students to https://mujslcm.jaipur.manipal.edu/ for online academic fee payment; hostel and mess fees are routed through the SpaceBasic app as a separate journey.
- No public MUJ page names BillDesk, Razorpay, CCAvenue, SBI ePay, or Cashfree as the academic fee provider; gateway attribution stays Unknown for all five.
- A MUJ-branded NTT DATA Pay URL exists in search evidence, but no public SLCM linkage, checkout fields, or API evidence was found; treat as an unconfirmed integration lead.
- Bank transfer path is fully documented: Canara Bank, IFSC CNRB0003563, account number built from "MUVAN" plus registration or application number, with email reconciliation of UTR, debit account holder name, date, and amount to student.finance@jaipur.manipal.edu.
- Refund policy: full refund to 30 September 2026, Rs 1,000 deduction from 1 to 31 October 2026, then 100/90/80/50/nil bands; eligible refunds paid within 45 days of hard-copy application; original receipt, ID card surrender, and dues clearance required.
- Annual fee PDF for AY 2026-27 extracts only as a garbled hostel annexure (SpaceBasics-only wording, 5 July 2026 deadline); document tells nothing reliable about course fees.
- Comparator incidents (JMI fake fee emails and QR codes, Sai Nath clone site, CYFIRMA unnamed clone, CSJMU five fake sites) argue for canonical domain lists and verification controls; none proves a MUJ incident.
- Public evidence exposes no authenticated fee screen, receipt layout, transaction template, callback design, or payment incident; those remain Unknown.

## KEY FACTS
- https://www.jaipur.manipal.edu/pay-fee-online.php - official payment route directory; source of SLCM, SpaceBasic, bank, NRI, and reconciliation wording
- https://mujslcm.jaipur.manipal.edu/ - student portal named for online fee payment; landing shows Parent Login and Student Login only
- https://muj-payservices.nttdatapay.com/DirectPay/MUFee - MUJ-branded NTT DATA Pay URL; strongest gateway lead, integration unconfirmed
- https://jaipur.manipal.edu/fee-structure.php - programme directory only, not a complete fee schedule
- https://jaipur.manipal.edu/indian-fee-structure.php - fee policy: amount changes possible, registration non-refundable, caution deposit refundable, demand draft accepted
- https://www.jaipur.manipal.edu/indian-refund-policy.php - dated refund bands and document requirements
- https://jaipur.manipal.edu/hostel-fees.php - AY 2026-27 hostel amounts, payment modes behind room-booking portal, gateway charges possible
- https://www.jaipur.manipal.edu/img/pdf/Annual-Fee-Payment-for-the-AY-2026-2027.pdf - linked annual notification; OCR-incomplete hostel annexure only
- https://jaipur.manipal.edu/img/pdf/Annual-Fee-Payment-AY-2026-2027-NRI.pdf - NRI notification; extracted content largely duplicated the hostel annexure
- https://www.ugc.gov.in/pdfnews/1857727_Fee-Refund-Policy-2025-26.pdf - UGC refund policy reference for band comparisons
- https://www.jmi.ac.in/upload/menuupload/Advisory%20Regarding%20Fee%20Payment.pdf - JMI advisory on fake fee emails, fake QR codes, and official-channel rules
- https://the420.in/sai-nath-university-fake-website-student-fraud-agra/ - lookalike university site case; media-reported allegations only
- https://www.cyfirma.com/research/weaponization-of-indian-student-data-an-ecosystem-for-phishing-social-engineering-and-financial-fraud/ - student data weaponization report; unnamed university clone
- https://the420.in/kanpur-csjmu-5-fake-websites/ - CSJMU warning against five fake sites and third-party payment portals
- http://in.nttdatapay.com/docs - NTT DATA provider documentation with PCI-DSS claims; provider level only, no MUJ specifics

## ACTIONABLE LEADS
- Re-extract the AY 2026-27 fee PDFs with a real PDF text tool to recover the course fee schedule and installment structure.
- Retrieve the linked "Required Transaction details" document (report says extraction failed) to inventory reconciliation fields; do not invent fields.
- Monitor pay-fee-online.php for unauthorized changes; archive snapshots with hashes as an integrity baseline.
- Verify whether muj-payservices.nttdatapay.com/DirectPay/MUFee is linked from any authenticated SLCM page, only in an authorized session.
- Confirm Canara Bank details and the MUVAN account-number rule through institutional channels; never validate via live transfers.
- Authorized, non-production test cases: successful payment, user cancellation, merchant timeout, duplicate callback, refund initiation and failure, reconciliation mismatch, with synthetic identities.
- Publish a canonical payment-route inventory naming provider, merchant name, receipt identifier, refund owner, and escalation contact; provide a public incident-reporting address.
- Watch for lookalike domains and fake QR or email fee requests against the MUJ brand.

## FLAGS
- NTT DATA Pay URL is a search-result lead; the report itself classifies it "public lead, not confirmed end-to-end integration."
- Annual fee PDF figures (Rs 182,750, Rs 261,750) are OCR-garbled hostel annexure values, not course fee schedules.
- Requester stack description (ASP.NET MVC 5.3, IIS 10, Akamai, M365) is user-supplied context, not verified by this report.
- Comparator incidents are not MUJ evidence; no confirmed MUJ payment incident exists in the record.
- The MUVAN account-number construction rule is published on the page; a phishing narrative could reuse it, so verification guidance matters.
- Transaction-details DOCX was unreadable; any claim about its fields would be fabrication.

## COVERAGE
32,089 chars read (file_size bytes), read to EOF, truncated=false confirmed.

DONE w2b-11-pay-fee-online.digest.md