# Digest: w2e-04-slcm-vendor-id.md

## REPORT
Source file: w2e-04-slcm-vendor-id.md (Identifying the Vendor Behind Manipal's SLCM)

## ANSWER SUMMARY
- The vendor behind the current MUJ SLCM backend is not publicly established; SLCM is best modeled as an ecosystem label with separate layers (portal, ERP core, identity, hosting, integrator).
- MAHE SIS pages carry direct in-house credits: "Information Systems Department, Manipal Academy of Higher Education" and "Department of Digital and Information Technology".
- SAP Student Lifecycle Management is the strongest historical packaged-core lead: self-reported implementation across Manipal Education entities in 2012 and configuration from 2011.
- Salesforce (Agentforce Education, Data 360, MuleSoft, Tableau) and Deloitte (implementation) are confirmed 2026 modernization roles for MAHE.
- Comviva, Manipal Technologies, JAIN/JGI, and Unikul are unsupported for MUJ; an Unikul Dubai customer story remains unconfirmed.
- Passive clues (RequestVerificationToken, jQuery validation, Microsoft password reset) show framework conventions, not ERP authorship.
- Recommended safe wording separates the SIS layer, historical SAP core, current MUJ backend (unconfirmed), and Salesforce modernization.

## KEY FACTS
1. https://mujslcm.jaipur.manipal.edu/ - MUJ portal, no vendor credit, form fields and Microsoft password-reset link observed.
2. https://sis.manipal.edu/ - current MAHE SIS, footer credits Department of Digital and Information Technology.
3. https://sis.manipal.edu/studloginSLCM.aspx - SIS login route with the older Information Systems Department attribution.
4. https://slcm.manipal.edu/ - classic MAHE SLCM endpoint, no vendor credit in reviewed content.
5. https://slcm.manipaldubai.com/ - Dubai student portal host linked from the official campus page.
6. https://student.manipal.edu.my/ - Malaysia portal using Scholar E-Mail ID language.
7. https://maheslcmtech.manipal.edu/ - modernization endpoint exposing a Microsoft tenant SAML path.
8. https://www.salesforce.com/in/news/press-releases/2026/03/26/manipal-university-ai-transformation/ - Salesforce MAHE announcement naming products and Deloitte as integrator.
9. https://www.manipal.edu/mu/news-events/mahe-introduces--magic--to-power-ai-driven-academic-and-administ.html - MAGIC program, five AI agents placed in SLCM.
10. http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf - MAHE ICT inventory defining SLCM as the single-window academic suite.
11. https://linkedin.com/in/adrija-sen-91631110 - profile reporting SAP SLcM implementation across Manipal Education entities in 2012.
12. https://linkedin.com/in/poornima-vishwaradhya-a0b95b22 - profile reporting SAP SLcM configuration at Manipal Global from March 2011.
13. http://sap.com/products/erp/student-lifecycle-management-for-sap-s4hana-cloud-private-edition.html - SAP SLCM product scope across the student journey.
14. https://unikul.com/overview - Unikul Dynamics 365-based SLCM product page with no Manipal reference.
15. https://campusdynamix.com/slcm-for-universities - unnamed Dubai Academic City customer that replaced SAP; possible MAHE Dubai link, unconfirmed.

## ACTIONABLE LEADS
- Request an approved architecture summary and software bill of materials from MUJ's authorized IT or data-protection contact.
- Ask for procurement records, contracts, and privacy notices to settle attribution without touching protected functions.
- Keep MUJ, MAHE SIS, Dubai, Malaysia, and maheslcmtech in separate evidence buckets.
- Verify LinkedIn-derived leads against first-party documents before any claim.
- Confirm whether the alternate host muj.slcm.jaipur.manipal.edu (seen in other reports) is a live alias or a stale entry.

## FLAGS
- LinkedIn profiles are self-reported; no first-party MUJ-to-SAP contract or architecture document exists.
- The Unikul customer story names no customer; geographic fit with Dubai Academic City is a low-confidence inference.
- In-house footers appear on MAHE SIS pages, not on the MUJ page; extension to MUJ is inference.
- "MVC 5.3" and the rest of the stack are user-supplied; the page capture does not establish package versions.
- Reference 16 is titled "login.microsoftonline.com" while its URL is maheslcmtech.manipal.edu, a labeling oddity worth rechecking.

## COVERAGE
Chars read: 34493. EOF confirmed: yes (truncation flag false on full read).