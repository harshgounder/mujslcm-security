## REPORT (w2c-02-session-management.md)
Session-security assessment for mujslcm.jaipur.manipal.edu. Public evidence limited to the landing page; architecture labels user-supplied. Verdict NOT VERIFIED, HIGH PRIORITY TO TEST. 261 lines, 44638 chars, read to EOF, truncated: false.

## ANSWER SUMMARY
- Verdict NOT VERIFIED, HIGH PRIORITY TO TEST. No public evidence of a session defect and no proof that controls are configured correctly. The public page shows only the portal title and sign-in choices.
- Architecture labels are scope assumptions. ".NET Framework 4.x" is too broad for SameSite conclusions because patched 4.7.2 and 4.8 added 2019 SameSite support in December 2019.
- HttpOnly, Secure, and SameSite solve different problems and must be inspected per cookie. Generic System.Web defaults are false for HttpOnly and RequireSSL; session timeout defaults to 20 minutes, Forms Authentication to 30 minutes sliding.
- Fixation is the highest-value lifecycle test: new binding at authentication and privilege change, rejection of unissued and URL-carried IDs. Compare the auth cookie and ASP.NET_SessionId separately because two-cookie rotation can create a false pass.
- Three lifecycles exist: local authentication, System.Web session state, and the Entra SSO session. Passing one layer does not terminate the others; Entra cannot directly revoke an application-issued session token.
- Concurrent login is a policy decision, not automatically a defect. OWASP wants documented rules, active-session visibility, alerts, and remote termination.
- Store choice changes failure mode: InProc loses state on restart, StateServer and SQLServer persist and support farms, Custom is provider-defined. Configuration review beats black-box guessing.
- Proposed plan SLCM-01 through SLCM-11 covers baseline, cookie inventory, regeneration, transport rejection, timeouts, logout replay, concurrency, revocation, store review, and logging.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/Home/Index - the only verified MUJ fact in the report: portal title and sign-in choices.
- https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html - renewal on auth and privilege change, idle and absolute timeouts, session lifecycle logging requirements.
- https://github.com/OWASP/ASVS/blob/master/4.0/en/0x12-V3-Session-management.md - ASVS session requirements used as pass or fail criteria for fixation, logout, and renewal tests.
- https://owasp.org/www-community/attacks/Session_fixation - fixation definition and the new-token-on-authentication requirement.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.sessionstate.sessionidmanager?view=netframework-4.8.1 - ASP.NET_SessionId default name, random 24-character value, and cookieless URL transport capability.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.configuration.sessionstatesection.timeout?view=netframework-4.8.1 - 20-minute session-state default, a review prompt only.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.configuration.formsauthenticationconfiguration.timeout?view=netframework-4.8.1 - 30-minute Forms Authentication default.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.configuration.formsauthenticationconfiguration.slidingexpiration?view=netframework-4.8.1 - sliding renewal after half the configured interval.
- https://learn.microsoft.com/en-us/aspnet/samesite/system-web-samesite - SameSite behavior in classic ASP.NET and the SameSite=None plus Secure pairing rule.
- https://learn.microsoft.com/en-us/entra/identity/users/users-revoke-access - Entra cannot directly revoke application-issued session tokens.
- https://learn.microsoft.com/en-us/previous-versions/aspnet/ms178586%28v%3Dvs.100%29 - four session-state modes: InProc, StateServer, SQLServer, Custom.
- https://pages.nist.gov/800-63-4/sp800-63b/session/ - idle and absolute termination, logout invalidates the binding secret.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.httpcookie.httponly?view=netframework-4.8.1 - HttpOnly semantics and its false default.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.configuration.httpcookiessection.requiressl?view=netframework-4.8.1 - RequireSSL false default.
- http://jaipur.manipal.edu/administration-registrar.php - public registrar contact identified as a reporting channel, not the security owner.

## ACTIONABLE LEADS
- Execute SLCM-01 to SLCM-11 under written authorization: HTTP versus HTTPS baseline, Set-Cookie inventory across the lifecycle, pre and post-login identifier comparison, alternate transport rejection, idle and sliding timeout measurements, absolute timeout, logout replay, concurrent sessions in two owned profiles, password change plus Entra revocation, store configuration review, logging review.
- Record for every sensitive cookie: name, issuing response, Domain, Path, HttpOnly, Secure, SameSite, Expires, Max-Age, and value change at each lifecycle event.
- Check for session identifiers in paths, query strings, hidden fields, or ad hoc headers; require cookie-only transport.
- Verify the old pre-login identifier is unusable after login and that privilege elevation rotates the binding.
- Ask the owner for Web.config sessionState mode and origin topology before inferring a provider from black-box behavior.

## FLAGS
- One citation is broken: "InProc session loss when the AppDomain or worker process is recycled [119 source]" cites reference 119, which does not exist in a reference list ending at 23.
- Row for password change cites "[185 snippet; 200.35]" inside ASVS wording, likely index residue; verify against the actual ASVS text.
- Reference 9 (CAE) uses an http:// scheme while sibling links use https; minor inconsistency.
- All SLCM-specific outcomes are labeled Observed, User-supplied, or Inference; no live testing was performed.
- Concurrency severity is explicitly conditional on MUJ's declared policy, which is unknown.
- Framework defaults (20 and 30 minutes) must not be reported as MUJ findings.

## COVERAGE
- File read to EOF: 261 lines, 44638 chars (file_size 44638), truncated: false. Confirmed EOF at line 261, final reference.