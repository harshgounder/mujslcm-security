# Digest: w2f-08-brightspace-security.md

## REPORT
Source file: w2f-08-brightspace-security.md (43,853 bytes, 315 lines, read to EOF)

## ANSWER SUMMARY
- The public Brightspace CVE record is narrow: one result, CVE-2021-43129, a bypass of the "Disable Right Click" quiz control. NVD has no CVSS score, CPE range, or named patched version. MUJ applicability is unknown.
- The most concrete public incident is identity-led: REN-ISAC reports criminals using compromised institutional accounts and permissive Brightspace email defaults for bulk phishing. Not a D2L code vulnerability.
- SAML is evidenced at the student portal: a passive fetch of student.onlinemanipal.com/s/ produced a tenant-specific login.microsoftonline.com saml2 flow. OIDC is a D2L-supported option that requires Implementation Services; no MUJ evidence of OIDC use.
- Grade sync is the highest-integrity boundary. Brightspace APIs can create, update, replace, recalculate, and set adjusted final grades under scopes. OneRoster 1.2 gradebook uses OAuth 2.0 Client Credentials and TLS 1.2 or 1.3. No public source proves MUJ uses any of these flows with SLCM.
- Identity mapping guidance: use stable sub or oid values, not mutable email, phone, or UPN. A grade-bearing integration needs an immutable institutional person key.
- learning.onlinemanipal.com publicly says powered by D2L Brightspace. www robots.txt is permissive with a sitemap; the security.txt response looked like homepage content with no RFC-style contact shown.
- D2L's disclosure policy covers specified D2L systems; customer-instance testing requires customer authorization and excludes DoS, phishing, exfiltration, persistence, and pivoting.
- Overall verdict: no public evidence reviewed establishes a presently exploitable MUJ Brightspace, SLCM, or Online Manipal vulnerability. Confidence moderate.

## KEY FACTS
1. https://nvd.nist.gov/vuln/detail/CVE-2021-43129 - the only Brightspace CVE found; quiz right-click bypass, no severity or version range on the record.
2. https://app.opencve.io/cve/?product=brightspace&vendor=d2l - catalog query returned one result, Page 1 of 1.
3. https://www.ren-isac.net/services/publications/alerts/Brightspace_Email_Fraud.html - documented abuse pattern: compromised accounts plus permissive email defaults, cloud email bypassing institutional mail controls.
4. https://learning.onlinemanipal.com/d2l/home/14042 - public learning page with username field and "Powered by D2L Brightspace" attribution.
5. https://student.onlinemanipal.com/s/ - passive fetch redirected into a tenant-specific Microsoft SAML flow.
6. https://community.d2l.com/brightspace/kb/articles/4843-saml-administration-overview - SAML self-service with Azure certification; OIDC, LDAP, GUID SSO, and CAS lack self-service and require Implementation Services.
7. https://community.d2l.com/brightspace/kb/articles/23832-getting-ready-for-oneroster-integration - IPSIS scheduled pulls, optional grade passback during daily sync, manual faculty sync, OAuth credentials, and IPSIS Audit Log review.
8. https://docs.valence.desire2learn.com/res/grade.html - grade object and grade value write scopes, recalculation, and adjusted final grade operations.
9. https://www.imsglobal.org/spec/oneroster/v1p2/gradebook/bind/rest - OneRoster 1.2 gradebook REST binding: OAuth 2.0 Client Credentials, scopes, TLS 1.2 or 1.3, read and write operations.
10. https://learn.microsoft.com/en-us/entra/identity-platform/id-token-claims-reference - rejects mutability of email, phone, and UPN; recommends stable sub or oid with tid context.
11. https://community.d2l.com/brightspace/kb/articles/23533-d2l-vulnerability-disclosure-policy - safe harbor scope and the customer-authorization boundary for instance testing.
12. https://status.d2l.com/ - global status page; all services operational when checked, with warnings that it is not a direct uptime monitor.
13. https://www.onlinemanipal.com/robots.txt - permissive crawl directives plus sitemap URL; ordinary public discovery, no access-control value.
14. https://www.onlinemanipal.com/.well-known/security.txt - parsed response resembled homepage material; RFC-style security contact not demonstrated.
15. https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-session-lifetime - sign-in frequency default of a rolling 90 days; local cookies and token caching can outlive intended session behavior.

## ACTIONABLE LEADS
- Passive: re-fetch learning.onlinemanipal.com, both robots files, and www security.txt; monitor D2L status categories Authentication, APIs, Grades Tool, Quizzing, Integrations.
- Owner-side: D2L tenant release history and advisory mapping, redacted SAML claims configuration, SOC report, subprocessor list, session and logout design.
- Grade integrity: data dictionary, directionality matrix, reconciliation runbook, and before/after provenance for every official grade.
- Email controls per REN-ISAC: active-course-only contacts, recipient limits, BCC and role-based permissions.
- Disclosure: use D2L's reporting channel for vendor issues; the university should publish an RFC 9116-style security contact.
- No credential testing, SAML replay, API calls, fuzzing, or content bypass without written authorization and a non-production plan.

## FLAGS
- One public CVE is a weak risk proxy; private advisories, non-CVE defects, and tenant misconfigurations can exist outside the catalog.
- Any SLCM-to-Brightspace grade flow is an inference in this report, not a finding; no public source ties OneRoster, IPSIS, or Grades API use to MUJ.
- The security.txt observation may be routing or parsing fallback; missing RFC fields do not prove the absence of a contact.
- The SAML redirect was observed once and not decoded; it does not prove login success, claim mapping, MFA, or Brightspace linkage.
- D2L ISO 27001 and control claims describe vendor posture, not the MUJ tenant configuration.
- All page fetches and status checks are point-in-time and unverified by this digest.

## COVERAGE
Chars read: 43,853 (full file, 315 lines). EOF confirmed: truncated false on the complete read.

DONE w2f-08-brightspace-security.md.digest.md