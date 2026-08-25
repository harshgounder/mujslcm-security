# Digest: w2f-07-entra-tenant-enum.md

## REPORT
Source file: w2f-07-entra-tenant-enum.md (44,454 bytes, 294 lines, read to EOF)

## ANSWER SUMMARY
- Two Entra tenants are confirmed via public OIDC discovery: jaipur.manipal.edu maps to tenant 7d0726e8-bf4b-4ac1-99f1-010fb11f1d3f and muj.manipal.edu maps to tenant 27282fdd-4c0b-4dfb-ba91-228cd83fdf71. Region scope AS.
- Both realm lookups classify the domains as Managed with organization Manipal University Jaipur. The federationmetadata URLs publish Microsoft STS and WS-Federation endpoints, not a third-party IdP.
- Portal split: mujslcm.jaipur.manipal.edu advertises @muj.manipal.edu while muj.slcm.jaipur.manipal.edu advertises @jaipur.manipal.edu. Migration, segmentation, or legacy overlap are possible; public data cannot decide.
- Tenant enumeration is confirmed as platform behavior. GetCredentialType is described in the literature as an account-enumeration vector; Microsoft calls it an internal endpoint. MUJ per-user behavior is deliberately untested and unknown.
- MUJ's June 2025 Office 365 SOP says MFA is mandatory before Office 365 use and documents Authenticator, SMS phone, and personal-email registration. Enrollment intent is proven; enforcement, coverage, and strength are unknown.
- Mail posture: both domains on Outlook MX and Autodiscover; DKIM selectors alias into mujcampus.onmicrosoft.com and mujmanipal.onmicrosoft.com. DMARC is monitoring-only: child p=none for jaipur, no child record for muj, parent manipal.edu p=none.
- Context not proof: Seqrite reports 4.92M Education and Training detections, 18.45% of India detections, Oct 2024 to Sep 2025; CERT-In 2023 handled 1,592,917 incidents nationally.

## KEY FACTS
1. https://login.microsoftonline.com/jaipur.manipal.edu/v2.0/.well-known/openid-configuration - issuer, token, authorization, and JWKS endpoints embed tenant GUID 7d0726e8-bf4b-4ac1-99f1-010fb11f1d3f.
2. https://login.microsoftonline.com/muj.manipal.edu/v2.0/.well-known/openid-configuration - same metadata class for tenant GUID 27282fdd-4c0b-4dfb-ba91-228cd83fdf71; separate policy boundary.
3. http://login.microsoftonline.com/getuserrealm.srf?login=probe@jaipur.manipal.edu&xml=1 - realm response Managed, organization Manipal University Jaipur.
4. http://login.microsoftonline.com/getuserrealm.srf?login=probe@muj.manipal.edu&xml=1 - realm response Managed for the muj domain.
5. https://login.microsoftonline.com/jaipur.manipal.edu/federationmetadata/2007-06/federationmetadata.xml - Microsoft STS entity ID and passive wsfed endpoint; retrieval is not proof of external federation.
6. http://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf - first-party MUJ SOP; MFA described as mandatory before Office 365 use.
7. http://dns.google/resolve?name=jaipur.manipal.edu&type=MX - MX to jaipur-manipal-edu.mail.protection.outlook.com.
8. http://dns.google/resolve?name=muj.manipal.edu&type=MX - MX to muj-manipal-edu.mail.protection.outlook.com; distinct Exchange Online namespaces.
9. http://dns.google/resolve?name=selector1._domainkey.jaipur.manipal.edu&type=CNAME - DKIM selector aliases into mujcampus.onmicrosoft.com.
10. http://dns.google/resolve?name=selector1._domainkey.muj.manipal.edu&type=CNAME - DKIM selector aliases into mujmanipal.onmicrosoft.com; corroborates the two-namespace split.
11. https://dns.google/resolve?name=_dmarc.jaipur.manipal.edu&type=TXT - v=DMARC1; p=none; rua mailto:dmarc@jaipur.manipal.edu; reporting without enforcement.
12. https://dns.google/resolve?name=_dmarc.manipal.edu&type=TXT - parent manipal.edu also publishes p=none.
13. http://dns.google/resolve?name=jaipur.manipal.edu&type=TXT - SPF includes spf.protection.outlook.com plus Brightspace sender authorization; a link to the LMS research thread.
14. http://muj.slcm.jaipur.manipal.edu/ - sibling SLCM portal advertises the @jaipur.manipal.edu suffix, in contrast to the target portal.
15. https://www.seqrite.com/documents/en/threat-reports/india-cyber-threat-report-2026.pdf - 4.92M education detections or 18.45% share; sector context only.

## ACTIONABLE LEADS
- Passive recheck: both OIDC docs, both realm probes, MX, DKIM selectors, DMARC, and Autodiscover CNAMEs; watch for issuer or realm changes.
- Owner-side: GUID-keyed comparison of Conditional Access, authentication methods, SSPR scope, guest policy, and legacy flows in both tenants; maintain monitored cloud-only emergency accounts.
- Apply phishing-resistant authentication strength to privileged roles; register methods before enforcement.
- If MUJ authorizes tests, use synthetic canary identities for GetCredentialType and SSPR validation with a documented rate limit; never test real identities.
- Stage DMARC: sender inventory, SPF/DKIM alignment review, then quarantine and reject decisions.
- Clarify portal lifecycle: canonical login suffix and retirement criteria for the legacy path.
- Disclosure: escalate policy drift findings through a university-approved channel; no active probing.

## FLAGS
- Two tenants are confirmed; cross-tenant policy drift is an inference, not a demonstrated gap.
- Realm probes used the invented identity probe@; behavior for real identities is untested.
- GetCredentialType output is ambiguous for guests, alternate sign-in identifiers, and consumer accounts; Microsoft warns it is not an onboarding decision API.
- MFA mandatory is documentation of intent; coverage, exclusions, and authentication strength remain unknown.
- p=none does not prove spoofing occurs; an absent child record for muj means parent behavior applies.
- Seqrite and CERT-In figures are vendor and national telemetry, not university-specific measures.
- All OIDC, realm, and DNS observations are point-in-time and unverified by this digest.

## COVERAGE
Chars read: 44,454 (full file, 294 lines). EOF confirmed: truncated false on the complete read.

DONE w2f-07-entra-tenant-enum.md.digest.md