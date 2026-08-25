# Digest: w2e-09-manipal-malaysia

## REPORT
Source file: w2e-09-manipal-malaysia.md (MIU SLCM Public Footprint and Shared-Codebase Verdict)

## ANSWER SUMMARY
- student.manipal.edu.my exposes student sign-in labeled "Scholar E-Mail ID", a separate parent username/password flow, forgot-password, and public account creation at /auth/registration.
- Entity attribution is ambiguous: the MQA register lists MILA University as formerly Manipal International University (Nilai), while the manipal.edu.my helpdesk brands itself MUCM. Confirmed ownership of the student subdomain is needed.
- The registration form requests username, first name, last name, email, phone, and password confirmation; consent, privacy notice, and retention deserve priority review.
- Public markup shows a client-rendered shell, hashed static assets, kt_ style identifiers, and a Microsoft-branded student control; a React-style SPA front end is plausible, back end unknown.
- Microsoft Clarity references in markup raise analytics governance and under-18 targeting questions.
- The only attributable SLCM complaint found concerns Manipal Jaipur ("Slcm portal issue", password rejected), not Malaysia; no Malaysia complaint corpus was located.
- The MUJ stack (MVC 5.3, .NET 4.x, IIS 10, Akamai, M365) is not evidenced for Malaysia; do not transfer version claims.
- Verdict: shared SLCM product family is plausible, shared codebase is not demonstrated, and back-end technology is low confidence/unknown.

## KEY FACTS
1. https://student.manipal.edu.my/ - Malaysian portal login; student and parent flows.
2. https://student.manipal.edu.my/auth/registration - public registration route collecting identity and contact data.
3. https://helpdesk.manipal.edu.my/ - MUCM Helpdesk branding with ticketing on the parent namespace.
4. https://www2.mqa.gov.my/mqr/english/eakrKPList.cfm?IDAkrIPTS=629 - regulator record: MILA University previously known as MIU.
5. https://manipal.edu.my/ - parent domain serving a generic "One moment, please..." page.
6. http://reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue - the single attributable SLCM complaint, Jaipur, password rejected.
7. https://mujslcm.jaipur.manipal.edu/ - MUJ portal with /Home/Index style entry and parent login; comparison baseline.
8. https://slcm.manipal.edu/sendtoportal - MAHE "MU SLcM" send-to-portal artifact in the same product family.
9. https://mila.edu.my/about-us/ - MILA site page not found, supporting the entity change.
10. https://www.manipal.edu/mu/important-links/world-wide-manipal/manipal-international-university.html - historical MIU business profile.
11. https://www.pdp.gov.my/ppdpv1/en/personal-data-protection-standard-2015 - Malaysian PDP standard for storage, security, deletion.
12. https://learn.microsoft.com/en-us/clarity/faq - Clarity session recordings, heatmaps, under-18 warning.
13. https://pages.nist.gov/800-63-4/sp800-63b.html - AAL2 phishing-resistant authentication guidance.
14. https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html - session controls baseline for the owner review.
15. https://techdocs.akamai.com/property-mgr/docs/web-app-firewall - Akamai WAF capability context; edge controls are not application proof.

## ACTIONABLE LEADS
- Confirm with university IT the legal operator, data controller, incident contact, and disclosure channel for student.manipal.edu.my before any report routing.
- Authorized check of registration abuse controls: eligibility, email verification, rate limits, breached-password screening, duplicate accounts.
- Verify Clarity presence, masking settings, and age suitability with the operator.
- Review parent-account lifecycle: governance, rate limiting, revocation when relationships end.
- Request aggregated helpdesk categories (login failures, recovery, registration errors) instead of probing live systems.
- Internal comparison of repositories, SBOMs, API contracts, and identity app registrations before assuming defect propagation across campuses.

## FLAGS
- React-style SPA hypothesis is moderate confidence from markup only; back end could be ASP.NET, Java, Node, PHP, or other.
- Microsoft branding does not prove an Entra tenant, protocol, or MFA posture, and no tenant metadata was collected.
- Clarity reference is in public markup; what is captured is unknown.
- MILA/MIU/MUCM attribution ambiguity can misroute disclosures and complaints.
- No Malaysia complaints found is absence of indexed evidence, not evidence of absence.
- Registration password hint (8+ mixed characters) is UI text; server-side enforcement unproven.

## COVERAGE
- Chars read: 37,184
- EOF confirmed: yes (truncated: false on final page, 256 of 256 lines)