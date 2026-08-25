## REPORT (w2c-06-rate-limit-lockout.md)
Login-controls assessment for mujslcm.jaipur.manipal.edu based on a passive form capture, framework source, and vendor docs. Verdict INDETERMINATE. 313 lines, 45600 chars, read to EOF, truncated: false.

## ANSWER SUMMARY
- Verdict INDETERMINATE: deployed lockout threshold, counter key, duration, and adaptive logic are unknown. Do not report a vulnerability from framework fingerprints or the absence of a visible initial CAPTCHA.
- Classic ASP.NET Identity 2 provides no turnkey threshold: the lockout duration starts at TimeSpan.Zero and AccessFailedAsync enforces only configured values; PasswordSignInAsync counts failures only when shouldLockout is true.
- Stock EntityFramework UserStore uppercases both sides before lookup and updates failure state by resolved user ID, so ASCII case variants normally converge on one counter. A bypass becomes plausible only if custom code counts on the raw string before resolution.
- Unicode is a separate risk: no normalization in the classic store; UTS #39 confusables are not automatic equality. Unicode tests belong in staging with administrator-created accounts only.
- IP and edge controls are friction, not account protection: OWASP wants account-keyed failure counters because attackers can vary addresses. Akamai documents burst and two-minute average thresholds and a ten-minute penalty box; IIS Dynamic IP Restrictions can block by rate or concurrency.
- Entra Smart Lockout (default ten attempts, initial one-minute lockout, separate familiar and unfamiliar counters) applies only if SLCM actually submits passwords to Entra, which is unproven.
- ASVS 5.0 requires documented controls (6.1.1), implemented controls (6.3.1), and responses that do not reveal valid users (6.3.8). Framework defaults are benchmarks, not MUJ policy.
- Response-only black-box testing cannot attribute a block to any layer; the plan requires correlation IDs and log review before testing.

## KEY FACTS
- http://mujslcm.jaipur.manipal.edu/ - the captured login form: POST with username, password, hidden EmailFor and LoginFor fields, anti-forgery token, Microsoft reset link, @muj.manipal.edu suffix.
- https://github.com/aspnet/AspNetIdentity/blob/main/src/Microsoft.AspNet.Identity.Core/UserManager.cs - lockout properties, zero default duration, AccessFailedAsync logic.
- https://github.com/aspnet/AspNetIdentity/blob/main/src/Microsoft.AspNet.Identity.Owin/SignInManager.cs - shouldLockout gate on the failure path.
- https://github.com/aspnet/AspNetIdentity/blob/main/src/Microsoft.AspNet.Identity.EntityFramework/UserStore.cs - ToUpper username comparison in FindByNameAsync.
- https://learn.microsoft.com/en-us/entra/identity/authentication/howto-password-smart-lockout - Entra defaults, familiar and unfamiliar counters, last three bad password hashes do not increment the counter.
- https://learn.microsoft.com/en-us/iis/manage/configuring-security/using-dynamic-ip-restrictions - IIS Dynamic IP Restrictions and X-Forwarded-For proxy mode.
- https://techdocs.akamai.com/cloud-security/docs/set-protections - rate policy burst and two-minute average thresholds, ten-minute deny, /32 and /64 client scoping.
- https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/03-Testing_for_Weak_Lock_Out_Mechanism - WSTG 3/4/5 attempt progression and the lockable-account rule.
- https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md - ASVS 5.0 items 6.1.1, 6.3.1, and 6.3.8.
- https://github.com/OWASP/ASVS/blob/master/4.0/en/0x11-V2-Authentication.md - ASVS 4.0.3 item 2.2.1, layered controls, no more than 100 failed attempts per hour per account.
- https://pages.nist.gov/800-63-4/sp800-63b.html - 100 consecutive failure ceiling and failure-count reset after successful authentication.
- https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html - account-keyed throttling, generic responses, exponential delay alternative, CAPTCHA as defense in depth.
- http://unicode.org/reports/tr39 - Unicode confusables framework for staging tests.
- https://learn.microsoft.com/en-us/dotnet/standard/base-types/best-practices-strings - Ordinal and OrdinalIgnoreCase guidance and the Turkish i example.
- http://login.microsoftonline.com/getuserrealm.srf?login=probe@muj.manipal.edu&xml=1 - realm metadata probe tying the muj.manipal.edu namespace to Microsoft Online.

## ACTIONABLE LEADS
- Ask the owner for four artifacts before black-box work: login controller call, lockout configuration, user-store implementation, sanitized failure-event log.
- Phase B: with a documented threshold T run T-1 failures plus one valid login, then T failures plus one valid attempt. Production discovery stops at five consecutive failures with 30-second spacing.
- Phase C: after a confirmed lockout measure unlock at 5, 10, and 15 minutes with at most three valid attempts.
- Phase D: ASCII case aggregation, two exact, two uppercase, one mixed-case failure, then a valid attempt; pass requires one account-level counter.
- Phase E: Unicode NFC and NFD equivalence tests in staging only, never production confusables.
- Phase F: two pre-registered institutional egress addresses in staging to prove account-state persistence; never spoof X-Forwarded-For.
- Phase G: observe CAPTCHA trigger stage without solving it; compare responses against an administrator-reserved nonexistent identifier.

## FLAGS
- References 13 and 21 are raw.githubusercontent.com duplicates of references 10 and 2.
- Reference 12 (Akamai terraform rate policy) is listed but the body analysis cites refs 14 and 11; mapping unclear.
- Stack labels are user-supplied; the token name alone does not establish MVC, .NET, or IIS versions.
- "No visible CAPTCHA" supports only the single captured state; adaptive challenges could still exist.
- Entra Smart Lockout behavior applies only if the SLCM password check reaches Entra, which is not established.
- The 30-second spacing and failure caps are plan controls, not claimed MUJ thresholds.

## COVERAGE
- File read to EOF: 313 lines, 45600 chars (file_size 45600), truncated: false. Confirmed EOF at line 313, final reference.