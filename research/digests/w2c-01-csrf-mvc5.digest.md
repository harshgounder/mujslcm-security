## REPORT (w2c-01-csrf-mvc5.md)
Defensive CSRF assurance assessment for mujslcm.jaipur.manipal.edu, ASP.NET MVC 5 family. No active testing by the report; stack fingerprint and token observation are user-supplied. Verdict INDETERMINATE. 337 lines, 56898 chars, read to EOF, truncated: false.

## ANSWER SUMMARY
- Verdict INDETERMINATE: no MUJ CSRF vulnerability established, safety not established either. A visible `__RequestVerificationToken` cookie and field pair is consistent with correct MVC design but proves nothing by itself.
- MVC requires a correlated pair: session-form cookie token plus non-session form token, matching 128-bit security values, correct roles, username or claim UID binding, MachineKey purpose string AntiForgeryToken.v1. "Field exists" is not the security property.
- Token reuse is expected (per-session generation allowed, serialized format has no timestamp). A finding requires a failed boundary: acceptance after logout, under a second identity, or after a controlled key or deployment change.
- JSON bodies are not covered by the native Request.Form store. Documented contract for Web API style is a custom header plus AntiForgery.Validate with both halves. Test each JSON or AJAX action independently.
- Local login CSRF and Microsoft identity CSRF are separate controls. OIDC needs state, nonce, PKCE where applicable; native MVC forms need local anti-forgery. Neither substitutes for the other.
- Sibling-subdomain cookie planting is a conditional risk multiplier, not an automatic MVC bypass: a valid field token is still required unless a weaker custom handler exists.
- Akamai, SameSite, and IIS are defense in depth. Token-bearing pages should be uncacheable or cache-isolated; multi-node MachineKey consistency matters; SameSite is partial protection only.
- No rejected proposal: report supplies an authorized negative-test matrix (L1-L12 login, M1-M5 identity, P1-P10 post-login) as the decisive evidence path.

## KEY FACTS
- https://github.com/aspnet/AspNetWebStack/tree/main/src/System.Web.WebPages/Helpers/AntiXsrf - reference implementation of the MVC anti-forgery mechanism cited throughout the lifecycle analysis.
- https://github.com/aspnet/AspNetWebStack/blob/main/src/System.Web.WebPages/Helpers/AntiXsrf/TokenValidator.cs - enforces token roles, embedded value match, and identity binding; grounds tests L2-L6 and P2-P3.
- https://github.com/aspnet/AspNetWebStack/blob/main/src/System.Web.WebPages/Helpers/AntiXsrf/AntiForgeryTokenStore.cs - reads cookie and the Request.Form field, so JSON properties are invisible to native validation.
- https://github.com/aspnet/AspNetWebStack/blob/main/src/System.Web.WebPages/Helpers/AntiXsrf/MachineKey45CryptoSystem.cs - MachineKey.Protect with purpose AntiForgeryToken.v1; basis for calling the token protected data, not a bare HMAC.
- https://learn.microsoft.com/en-us/aspnet/web-api/overview/security/preventing-cross-site-request-forgery-csrf-attacks - Microsoft guidance for token pairs and the custom-header transport for Web API style requests.
- https://learn.microsoft.com/en-us/aspnet/mvc/overview/security/xsrfcsrf-prevention-in-aspnet-mvc-and-web-pages - Microsoft warning that built-in anti-XSRF routines do not by themselves prevent login XSRF; RequireSsl control.
- https://github.com/aspnet/AspNetWebStack/blob/main/src/System.Web.WebPages/Helpers/AntiXsrf/AntiForgeryTokenSerializer.cs - serialized token format has no timestamp, supporting the reuse analysis.
- https://github.com/aspnet/AspNetWebStack/blob/main/src/System.Web.WebPages/Helpers/AntiXsrf/AntiForgeryWorker.cs - cookie token reuse and generation behavior across rendered forms.
- https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html - per-session or per-request generation accepted; signed double-submit must bind to the session; caches must Vary on header-based decisions.
- https://portswigger.net/web-security/csrf/bypassing-token-validation - documented flawed patterns: global token pool and cookie-only validation, mapped into the bypass table.
- https://mujslcm.jaipur.manipal.edu/ - the target entry point every test in the matrix is designed against.
- https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow - random state plus equality verification for the authorization-code flow.
- https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html - roles of state, nonce, PKCE; open redirectors can expose authorization codes.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.security.machinekey?view=netframework-4.8.1 - Protect encrypts or signs, so "machine key HMAC" is called an incomplete description.
- https://datatracker.ietf.org/doc/html/rfc6265 - cookie Domain scope and absence of sibling-host integrity guarantees, basis for the subdomain combined-risk model.

## ACTIONABLE LEADS
- Run the login negative matrix on an authorized host: omit field only, omit cookie only, swap roles (L4), cross-profile pair (L5), one-character tamper (L6), pre-login to post-login boundary (L8), duplicate token fields (L11), and record cookie attributes (L12).
- Identity flow checks M1-M5: random state, state rejection before local login, nonce or PKCE, registered callback destinations, SameSite behavior across supported browsers.
- Post-login P1-P10: per-route omission tests, method coverage GET/POST/PUT/PATCH/DELETE, alternate content types, AJAX header transport, token after logout, cache isolation, failure atomicity.
- Inventory every JSON or AJAX endpoint and determine which component extracts the token and whether it calls two-token validation before any side effect.
- Capture wire-level cookie attributes on HTTPS responses and Akamai cache headers (Cache-Control, Age, Vary) for token-bearing pages.
- Confirm MachineKey consistency across origin nodes with the owner before diagnosing intermittent anti-forgery failures.

## FLAGS
- Stack fingerprint (MVC 5.3, Akamai, M365 identity, token pair) is user-supplied; the report performed no live validation.
- Report self-assigns High confidence to framework mechanics and Low to current MUJ status; do not cite it as a vulnerability finding.
- Reuse observations are inconclusive by design: differing ciphertext does not prove one-time semantics and identical strings do not prove insecurity.
- Referenced Akamai docs (refs 30-32) appear in the reference list but are not meaningfully analyzed in the body; RFC 9110 is listed twice (refs 33 and 37).
- The JSON-in-body conclusion is labeled Inference pending an actual handler contract; the report does not claim MUJ has one.
- No live evidence that Akamai shares tokenized responses or that cookies carry broad Domain; those remain test hypotheses.

## COVERAGE
- File read to EOF: 337 lines, 56898 chars (file_size 56898), truncated: false. Confirmed EOF at line 337, final reference.