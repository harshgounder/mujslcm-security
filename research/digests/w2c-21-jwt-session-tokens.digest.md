# Digest: w2c-21-jwt-session-tokens.md

## REPORT
Source: /home/liebert511/mujslcm-recon/research/w2c-21-jwt-session-tokens.md

## ANSWER SUMMARY
- No public JWT finding for SLCM. Landing page shows student and parent sign-in paths only.
- Ecosystem splits into four trust zones: SLCM (session unknown), Microsoft 365 (JWT ID tokens, opaque access tokens), MUJ Connect (token design unknown), Brightspace (OAuth bearer plus LTI 1.3 signed JWTs).
- Brightspace access-token lifetime configurable 1800-72000 seconds; Microsoft access tokens randomized 60-90 minutes.
- Algorithm policy is verifier-side: RFC 8725 fixed algorithm set, one key one algorithm, no alg=none.
- Signature success is not sufficient; issuer, audience, subject, exp, nbf, type checks required.
- Stateless JWT revocation needs jti denylists; ASP.NET sessions keep central server state for immediate termination.
- Historical library failures (CVE-2015-9235, CVE-2023-48238) show the mechanism; they do not name a MUJ dependency.
- Verdict: ecosystem is not one JWT-based system; no MUJ vulnerability established.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/ : SLCM landing page, only SLCM-specific evidence.
- https://mujconnect.in/login : MUJ Connect login, email or username only.
- https://learning.onlinemanipal.com/d2l/home/14042 : MUJ-branded Brightspace login page.
- http://d2l.com/why-d2l/customer-corner/d2l-brightspace-in-india-a-success-story : D2L case study, 85,000 online learners in five years.
- https://docs.valence.desire2learn.com/basic/oauth2.html : OAuth bearer tokens, 1800-72000 second lifetime range.
- https://community.d2l.com/brightspace/kb/articles/23730-about-lti-1-3-launch-and-authentication : LTI 1.3 OIDC launch, kid-selected public key verification.
- https://datatracker.ietf.org/doc/html/rfc8725 : algorithm pinning, explicit typing, issuer-key binding, no alg=none.
- https://datatracker.ietf.org/doc/html/rfc7519 : exp and nbf enforcement with small clock skew.
- https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens : access tokens opaque to clients, 60-90 minute randomized lifetime.
- https://learn.microsoft.com/en-us/previous-versions/aspnet/ms178581%28v%3Dvs.100%29 : ASP.NET SessionID maps to server-maintained state.
- https://learn.microsoft.com/en-us/aspnet/mvc/overview/security/xsrfcsrf-prevention-in-aspnet-mvc-and-web-pages : anti-forgery pair is not an authentication token.
- https://portswigger.net/web-security/jwt/algorithm-confusion : asymmetric-to-symmetric algorithm confusion mechanism.
- https://nvd.nist.gov/vuln/detail/CVE-2015-9235 : jsonwebtoken before 4.2.2 verification bypass.
- https://nvd.nist.gov/vuln/detail/CVE-2023-48238 : json-web-token before 4.0.0 RS256/HS256 confusion.
- https://www.imsglobal.org/spec/lti/v1p3 : LTI claims contract, deployment id, target link checks.

## ACTIONABLE LEADS
- Owner questionnaire for SLCM: cookie name, Secure, HttpOnly, SameSite, idle and absolute timeout, rotation, logout invalidation, CSRF coverage.
- Brightspace admin review: OAuth lifetime setting, refresh-token rotation, LTI tool registrations, JWKS, nonce replay window.
- MUJ Connect: document auth protocol, issuer, token format, storage, lifetimes, revocation before any security claim.
- Staging verifier regression suite: alg none, wrong algorithm family, wrong issuer, wrong audience, unknown kid, expired token, replayed nonce.
- Check cross-protocol acceptance: Brightspace API tokens must never validate as LTI ID tokens or vice versa.
- Publish a coordinated disclosure channel so club reports stay inside authorization.

## FLAGS
- urlscan.io record says the host was not observed in scan corpus; it does not confirm IIS, MVC, .NET, or Akamai (report cites it only as passive observation).
- Builtwith and Wappalyzer URLs appear in references without body claims; fingerprint data unverified.
- Reference [17] is a 404 page on learn.microsoft.com; report does not rely on it.
- 85,000 learner figure is D2L marketing material, not independent.
- SLCM cookie details and MUJ Connect token internals remain Unknown by the report's own evidence classes.
- Report explicitly rejects calling MUJ Connect JWT-vulnerable without first-party evidence.

## COVERAGE
- Chars read: 37606. EOF confirmed via read_file truncated:false.