# Digest: w2c-13-open-redirect-mvc

## REPORT
Source file: w2c-13-open-redirect-mvc.md (292 lines, 41318 bytes). Analysis of the reported ReturnUrl to enc to /Home/Index login flow in an ASP.NET MVC context.

## ANSWER SUMMARY
- No publicly demonstrated open redirect; the ReturnUrl to enc flow is a brief-supplied observation with no raw samples or server source, so implementation status is UNKNOWN.
- enc token syntax cannot reveal semantics: Base64, base64url, and ASP.NET UrlTokenEncode look alike; candidates include plaintext, MachineKey.Protect output, HMAC, forms ticket, opaque server-side handle.
- Url.IsLocalUrl rejects null, empty, absolute URLs, //host, and /\host forms; accepts / and ~/; it does no host comparison, so a route allowlist must follow it.
- Microsoft's classic MVC case: Redirect(returnUrl) without validation is the vulnerable pattern; the repair is Url.IsLocalUrl plus a fixed Home/Index fallback.
- Cryptographic protection proves tamper evidence, not destination safety; validation must happen after the final decode, before the redirect sink.
- Entra redirect_uri must match a registered value; callback handoff and post-callback continuation are two separate boundaries, and RFC 9700 bars open redirectors in OAuth clients.
- Escalation requires owner-authorized source or staging proof of an external redirect; otherwise report as a review item only.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/Home/Index : public landing showing "WELCOME TO MUJ PORTAL" and sign-in options.
- https://github.com/Tejas-Narula/SlcmPlus/blob/main/manifest.json : third-party extension manifest naming attendance, internal marks, and grades routes; client-side only.
- https://learn.microsoft.com/en-us/aspnet/mvc/overview/security/preventing-open-redirection-attacks : vulnerable and repaired MVC redirect patterns.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.security.machinekey.protect?view=netframework-4.8.1 : purpose-bound byte protection; unprotect requires matching purpose.
- https://github.com/aspnet/AspNetWebStack/blob/main/src/System.Web.WebPages/RequestExtensions.cs : IsUrlLocalToHost string-prefix logic, the core of Url.IsLocalUrl.
- https://github.com/aspnet/AspNetWebStack/blob/main/src/System.Web.Mvc/RedirectResult.cs : constructor only rejects null or empty; no safety wrapper.
- https://github.com/aspnet/AspNetWebStack/blob/main/src/System.Web.Mvc/UrlHelper.cs : delegation of IsLocalUrl to RequestExtensions.
- https://learn.microsoft.com/en-us/entra/identity-platform/reply-url : responses go only to registered reply URIs.
- https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow : state should be a random unique value, not URLs or sensitive data.
- https://www.rfc-editor.org/rfc/rfc9700.html : OAuth clients must not expose open redirectors; code or token exfiltration risk in relevant flows.
- https://www.rfc-editor.org/rfc/rfc4648.html : Base64 encodes arbitrary octets; base64url uses - and _.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.httpserverutility.urltokenencode?view=netframework-4.8.1 : URL-token encoding for arbitrary bytes.
- https://url.spec.whatwg.org/ : backslash treated specially for HTTP(S)-style URLs, the parser differential behind the /\ rule.
- https://owasp.org/www-community/attacks/open_redirect : open redirect defined as redirection to a user-supplied unvalidated destination.
- https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html : route ID or token mapped server-side with warning page.

## ACTIONABLE LEADS
- Owner-authorized server code review: find the enc assignment (serializer, Protect call, purpose strings) and the consumption path (decode, unprotect, expiry, IsLocalUrl, redirect sink).
- Offline classification of already-held samples: length, alphabet, padding, URL escaping; local decode only.
- Local or staging unit tests across the full separator matrix (null, /, ~/, //host, /\host, absolute, encoded forms).
- Verify farm-wide MachineKey protection state without leaking configuration values.
- Preferred design: protected route ID to server mapping to RedirectToAction with fixed fallback; log reason codes, never raw tokens.
- Without authorization, publish a framework-level risk assessment, not a vulnerability claim.

## FLAGS
- MachineKey, Base64, and HMAC hypotheses all rated Low for evidence; framework analysis is High, MUJ implementation is Low.
- Third-party extension is client-side and carries no server redirect logic.
- No raw samples supplied; the reported flow was not reproduced.
- Public client repositories are not substitutes for server code.
- Same-host absolute URL exceptions add parser risk; the classic helper rejects absolute form deliberately.

## COVERAGE
Chars read: 41318 (full file to EOF, truncated false).