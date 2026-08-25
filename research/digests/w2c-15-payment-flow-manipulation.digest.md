# Digest: w2c-15-payment-flow-manipulation

## REPORT
Source file: w2c-15-payment-flow-manipulation.md (316 lines, 43158 bytes). Defensive fee-payment integrity assessment for MUJ SLCM based on vendor docs, OWASP guidance, and Indian education case reports.

## ANSWER SUMMARY
- No evidence in cited public material that MUJ SLCM is vulnerable to fee manipulation, receipt IDOR, callback forgery, or refund abuse; the only supported target fact is three sign-in choices on the portal.
- Razorpay pattern: server-created order, amount in smallest currency sub-unit, mandatory HMAC-SHA256 completion signature, service only after capture; webhooks can duplicate and arrive out of order, identified by x-razorpay-event-id.
- BillDesk pattern from a WhatsApp-specific Meta guide: HMAC or JOSE client auth with JOSE preferred, unique merchant order, transaction object posted to return URL; guide is illustrative only.
- CCAvenue Integration Document v3.3 (Nov 2021): merchant working key, encrypted request, order_id uniqueness is merchant responsibility because the vendor does not check it.
- Indian cases: CBSE June 2026 official release says attacks mitigated and no data breach while Telegraph reports unauthorized payment access involving about 50 students; Sai Nath clone diverted INR 32,000; GBU FIR alleges over INR 5 crore with fake UPI entries; none prove an MUJ defect.
- IT Act Sections 43 and 66 tie testing legality to owner permission and intent; written scope and staging are mandatory.
- Verdict: staging-only assessment with synthetic identities and a gateway sandbox; production returns, receipts, orders, callbacks, and refunds are off limits.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/ : portal shows Sign In @muj.manipal.edu, Parent Login, Student Login.
- https://razorpay.com/docs/payments/server-integration/java/integration-steps/ : server order creation, sub-unit amount, mandatory signature verification, captured status before delivery.
- https://razorpay.com/docs/webhooks/validate-test/ : raw-body HMAC, duplicate events, unordered delivery.
- https://razorpay.com/docs/api/refunds/ : refunds only for captured payments; uncaptured authorizations auto-refund after three days.
- https://links.avenues.info/downloads/CCAvenue_Integration_Ver_3_3.pdf : merchant_id, order_id, currency, amount, redirect_url, cancel_url fields; vendor does not enforce order uniqueness.
- https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/upi-intent/pg-guide-billdesk : BillDesk HMAC or JOSE, unique order ID, return URL mechanics; WhatsApp-specific.
- https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html : deny by default, permission validation on every request, relationship-aware checks.
- https://cheatsheetseries.owasp.org/cheatsheets/Business_Logic_Security_Cheat_Sheet.html : idempotency key stored with result, cached result on retry.
- https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References : IDOR definition, direct object access via user-supplied identifiers.
- https://www.cbse.gov.in/cbsenew/documents/Press_Release_Complaint_PVR_05062026.pdf : CBSE June 2026 statement, mitigated attacks, no data compromise.
- https://www.telegraphindia.com/india/cbse-revaluation-portal-system-hit-by-malicious-attack-of-50-students-with-unauthorised-access/cid/2163149 : secondary report of unauthorized payment-system access by about 50 students.
- https://the420.in/sai-nath-university-fake-website-student-fraud-agra/ : cloned university site allegedly diverted INR 32,000.
- https://timesofindia.indiatimes.com/city/noida/fir-against-ex-gbu-registrar-accounts-officer-for-rs-5-crore-fee-fraud/articleshow/130197794.cms : GBU FIR, fake UPI entries in university software; allegation only.
- https://www.indiacode.nic.in/bitstream/123456789/13116/1/it_act_2000_updated.pdf : IT Act Sections 43 and 66 permission and intent conditions.
- https://www.cert-in.org.in/RVDCP.jsp : CERT-In responsible vulnerability disclosure and coordination policy.

## ACTIONABLE LEADS
- Run an architecture review first: actual gateway from contracts, role-to-object matrix, sequence diagrams, and a single agreed data-flow diagram.
- Sandbox test matrix: order creation from ledger, amount and currency mismatch, cross-account order binding, non-authoritative browser return, raw-body webhook signature, duplicate and out-of-order replay, receipt IDOR, refund limits with maker-checker, concurrency, callback outage reconciliation.
- Implement one server-side settlement service with unique internal, gateway, payment, and processed-event keys and a monotonic state machine ending in Posted or Refunded.
- Monitoring signals: amount or currency mismatch, unknown or reused order, invalid signature, repeated event ID, refund near original amount, gateway captured but ERP pending, lookalike payment domains.
- Disclose through the university-approved channel and CERT-In when applicable; do not share without university approval.

## FLAGS
- Gateway vendor for MUJ is unverified; Razorpay, BillDesk, and CCAvenue patterns are references, not findings.
- CBSE narrative conflict: official no-breach statement versus Telegraph unauthorized access reporting; do not infer a technical root cause.
- GBU FIR is an allegation, not a technical finding or adjudication.
- BillDesk guide is WhatsApp-specific and not comprehensive.
- CCAvenue document is from 2021; it does not prove MUJ's current configuration.
- No authorized dynamic testing was performed; MUJ-specific vulnerability status is not assessed.

## COVERAGE
Chars read: 43158 (full file to EOF, truncated false).