## REPORT (w2b-08-learning-onlinemanipal.md)
Brightspace tenant and MUJ SLCM posture assessment. Passive public evidence only. Verdict: Brightspace attribution high, Microsoft 365 SSO unconfirmed, grades sync unknown, no vulnerability finding against MUJ. 314 lines, 54600 chars, read to EOF, truncated: false.

## ANSWER SUMMARY
- D2L's own case study names MUJ Online as a Brightspace customer and describes a 2020 initiative scaling to 85,000 students in five years; URLScan records CNAME muj.brightspace.com. Tenant attribution is high confidence.
- Route /d2l/home/14042 is an indexed MUJ login page with Username and Forgot your password; no Microsoft, Entra, SAML, or OIDC naming on the public page.
- D2L documents customer-managed SAML as a capability; that says SAML is possible, not that MUJ uses it. Microsoft 365 federation remains unverified.
- Brightspace release and patch level are unknown; CVE-2021-43129 is a quiz right-click bypass with no NVD CVSS, product-level and historical only.
- Grades sync is not publicly confirmed. D2L documents generic IPSIS final-grade export (IMS LIS v2.0), SLCM documentation lists attendance, marks, and results; no connector, direction, or schedule is public.
- Public complaints are SLCM fee-state issues (fee portal not visible; paid fee pending), not Brightspace incidents.
- D2L disclosure policy requires customer authorization to test instances and accepts reports at incident@d2l.com.

## KEY FACTS
- https://learning.onlinemanipal.com/d2l/home/14042 - MUJ login route, org-unit identifier 14042, no IdP named.
- https://urlscan.io/domain/learning.onlinemanipal.com - historical record: CNAME muj.brightspace.com, AS16509 AMAZON-02, Sydney GeoIP, with explicit snapshot caveats.
- https://www.d2l.com/en-in/why-d2l/customers/manipal-university-jaipur-online - vendor and customer attribution, reported outcomes (30% discussion, 15% completion, 10% performance, 30% grading, 40% admin workload).
- https://nvd.nist.gov/vuln/detail/CVE-2021-43129 - Brightspace right-click bypass record, no affected version, CVSS N/A.
- https://community.d2l.com/brightspace/kb/articles/23533-d2l-vulnerability-disclosure-policy - authorization rule and incident@d2l.com reporting contact.
- https://community.d2l.com/brightspace/kb/articles/23729-overview-of-grades-and-ipsis - generic IPSIS final-grade export to a SIS using IMS LIS v2.0.
- https://community.d2l.com/brightspace/kb/articles/4843-saml-administration-overview - customer-managed SAML and IdP registration capability.
- http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf - SLCM ICT description: attendance, internal/external marks, results, broadcasts.
- https://www.reddit.com/r/Manipal_Academics/comments/1u8476b/slcm_portal_issue - fee portal visibility complaint, SLCM named, no resolution.
- https://www.reddit.com/r/Manipal_Academics/comments/1lzf0ht/paid_my_fees_but_still_showing_as_pending_on_slcm - deducted payment still pending, receipt mentioned.
- http://mahe.onlinemanipal.com/help-center - LMS access follows enrollment and fee payment; login details emailed.
- http://manipal.edu/mu/important-links/privacy-and-cookie-policy.html - MAHE policy: data categories, sharing, retention, privacy.mahe@manipal.edu.
- https://www.d2l.com/cloud - D2L states AWS is its primary strategic cloud provider.
- https://www.d2l.com/solutions/higher-education/d2l-brightspace-and-sis-integrations-for-higher-education/ - generic SIS integration wording, not MUJ-specific.
- https://muj.onlinemanipal.com/ - Online Manipal programme page describing LMS functions.

## ACTIONABLE LEADS
- Ask MUJ or D2L for: tenant release, IPSIS enablement status, SAML and Entra settings, claims mapping, deprovisioning flow, grade source of truth, incident history.
- Reconcile enrollment, payment, provisioning, and support timestamps to check the fee-to-access dependency.
- Route SLCM fee complaints to SLCM and payment owners; correlate with Brightspace only via authorized logs.
- Preserve URLScan, case study, and Reddit excerpts with retrieval dates in the evidence register.
- For a genuine D2L issue, report through the D2L policy; do not test the MUJ instance without customer authorization.

## FLAGS
- URLScan fields are historical observations; ASN, GeoIP, and hit-count labels are not current availability or security verdicts.
- Case study outcome percentages are vendor-published claims, not audited measurements.
- CVE-2021-43129 lacks an affected version and CVSS in the retrieved NVD record; do not map it to the tenant.
- Fee complaints may be reconciliation or support issues; not renamed as security incidents.
- The vendor case study wording quoted in the source praises the LMS chosen; the report repeats vendor claims, no tenant posture claim rests on them.
- Reference 20 in the report is a malformed markdown link to https://slcm.manipal.edu/.

## COVERAGE
- File read to EOF: 314 lines, 54600 chars (file_size 54600), truncated: false. Confirmed EOF at line 314, final reference.