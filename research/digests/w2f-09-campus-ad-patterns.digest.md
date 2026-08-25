# Digest: w2f-09-campus-ad-patterns.md

## REPORT
Source file: w2f-09-campus-ad-patterns.md (MUJ SLCM Identity Risk: Evidence, Inference, and Controls)

## ANSWER SUMMARY
- Report analyzes the claim "Outlook password equals SLCM password" and finds it is a supplied premise, not a recovered fact. No citable public FAQ copy was found. Treat as unverified, needs MUJ confirmation.
- Public portal evidence is narrow: shows `@muj.manipal.edu` suffix, Parent Login, Student Login, Forgot Password text. This proves login audiences exist, not where passwords validate or whether MFA runs.
- Six architectures can produce one-password UX: PHS, PTA, SAML federation, Application Proxy, password writeback, or independent local store with coordinated passwords. MUJ status for all six is Unknown.
- Key decision question: does SLCM receive a password or an identity-provider token? Token input supports centralized MFA; password input needs a second question about validating directory and compensating MFA.
- Stack labels (ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai) are unverified scope assumptions, not findings from first-party text.
- No public basis to declare MFA absent or passwords duplicated. Recommended next step is an authorized administrator evidence review, not external testing.
- Incident duties: CERT-In 2022 directions require six-hour incident reporting and 180-day in-India log retention for covered entities. Shared credential makes mail and ERP one blast radius.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/Home/Index - First-party portal page, the only verified MUJ surface in the report.
- http://mujslcm.jaipur.manipal.edu/ - Indexed portal entry showing Parent Login, Student Login, Forgot Password labels.
- https://muj.slcm.jaipur.manipal.edu/ - Alternate dotted hostname cited alongside the main portal, naming ambiguity.
- https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/whatis-phs - Microsoft PHS mechanism, explains same-password UX without password storage in Entra.
- https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-pta - PTA validates cloud sign-in against on-premises AD, alternative trust boundary.
- https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/add-application-portal-setup-sso - SAML SSO lets SLCM accept Entra tokens instead of passwords.
- https://learn.microsoft.com/en-us/entra/fundamentals/security-defaults - Free baseline MFA policy, contextual prompting for ordinary users.
- https://learn.microsoft.com/en-us/entra/identity/conditional-access/overview - Conditional Access engine, evaluated after first factor, needs P1/P2 tiers.
- https://learn.microsoft.com/en-us/entra/identity/authentication/tutorial-enable-sspr-writeback - Password writeback, explains same-password-after-reset patterns.
- https://learn.microsoft.com/en-us/entra/identity/conditional-access/policy-block-legacy-authentication - Legacy protocols do not support MFA, blocking recommended in Report-only mode.
- https://www.cisa.gov/topics/cybersecurity-best-practices/multifactor-authentication - CISA MFA definition and 99% account-takeover reduction claim.
- https://www.cisa.gov/news-events/alerts/2025/04/16/cisa-releases-guidance-credential-risks-associated-potential-legacy-oracle-cloud-compromise - CISA reset and review guidance for credential incidents.
- https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf - CERT-In 70B directions, six-hour reporting and 180-day log retention.
- https://studentclearinghouse.org/about/trust/security - Higher-ed comparison showing published MFA, zero-trust, and SOC 2 claims.
- http://support.msjc.edu/support/solutions/articles/20000040321 - MSJC MFA enrollment guidance, transparency benchmark for universities.
- https://msjc.edu/mymsjc/pg.html - MSJC SSO moved to Microsoft 365 My Apps, shows what MUJ could publish.

## ACTIONABLE LEADS
- Ask MUJ for the current FAQ or policy text that states Outlook password equals SLCM password; this resolves the key premise.
- Submit an authorized evidence request covering: Entra Connect config (PHS/PTA/federation), verified-domain status, enterprise-application record for SLCM, Security Defaults and Conditional Access assignments, legacy auth policy, parent identity lifecycle, deprovisioning workflow, log retention and time sync.
- Determine whether SLCM receives a password or a token; this drives the whole conclusion.
- Check whether Parent Login is a local credential store or covered by Entra policy; do not label it an MFA bypass without config evidence.
- Verify stack labels (MVC 5.3, .NET 4.x, IIS 10, Akamai) from dependency manifests, CMDB, and edge config, not banners.
- Build one identity incident playbook spanning M365, SLCM, parent access, and on-premises directory, mapped to CERT-In reporting duties.
- Follow-up test surface: Exchange legacy protocol status and mailbox-recovery pivots, only with written authorization.

## FLAGS
- Contradiction risk: report says portal display proves `@muj.manipal.edu` usage, but the shared-password FAQ was never recovered; the two claims have different evidence strength.
- Suspicious claim: "MFA makes accounts 99% less likely to be hacked" is vendor/government stat, cited as conditional, not a guarantee.
- Unverified URLs: the FAQ with the shared-password statement is absent from references; the report admits no citable copy was found.
- Hallucination risk: reference [24] MSJC My Apps and the NSC security page are repeated across many source numbers (5, 9, 13, 30, 31, 47 all map to studentclearinghouse.org/about/trust/security), suggesting noisy citation indexing rather than distinct sources.
- Reference 1 in the full list is a "404 - Content not found" page; that source is dead.
- All MUJ architecture rows in Table 4 and Table 6 are Unknown; any reader inference that MUJ uses a specific pattern would be fabrication.
- Overall verdict calls confidence MODERATE for the risk model but LOW for backend configuration claims.

## COVERAGE
- Chars read: 47231
- EOF confirmed: true (read_file truncated=false, 323 lines)