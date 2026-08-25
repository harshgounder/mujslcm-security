# Digest: w2c-20-api-security.md

## REPORT
Source: /home/liebert511/mujslcm-recon/research/w2c-20-api-security.md

## ANSWER SUMMARY
- Public third-party Flutter code names 13 MUJ routes on mujslcm.jaipur.manipal.edu: attendance, grades, marks, CGPA/GPA, calendar, directory, OTP, dashboard.
- Client model is cookie-session with __RequestVerificationToken; no bearer token use found in examined files.
- BOLA is the top authorization risk per OWASP API1:2023; server-side ownership and role checks required on every object.
- CORS is unmeasured, not cleared. Wildcard origin is invalid with credentials; per-endpoint allowed-origin policy needed.
- __RequestVerificationToken is anti-CSRF evidence, not a Microsoft identity access token.
- No indexed .asmx or .svc service found. WCF metadata is off by default; configuration-backed inventory beats URL guessing.
- Akamai Site Shield works only if origin allowlists Akamai ranges; forwarded-header trust must be bounded.
- Verdict: substantial and sensitive API-like surface publicly inferable, no live exploitable vulnerability established.

## KEY FACTS
- https://raw.githubusercontent.com/DK10WS/SLCM_APP/main/lib/pages/redirects.dart : 13 route constants, strongest route evidence.
- https://raw.githubusercontent.com/DK10WS/SLCM_APP/main/lib/utils/login.dart : login GET/POST flow, token and cookie extraction.
- https://raw.githubusercontent.com/DK10WS/SLCM_APP/main/lib/pages/Attendance.dart : POST attendance with empty StudentCode field.
- https://raw.githubusercontent.com/DK10WS/SLCM_APP/main/lib/pages/grades.dart : grades POST with empty Enrollment field.
- https://raw.githubusercontent.com/DK10WS/SLCM_APP/main/lib/pages/marks.dart : marks response fields MTE1, MTE2, CWS, ETE, PRS, Total.
- https://raw.githubusercontent.com/DK10WS/SLCM_APP/main/lib/pages/timetable.dart : timetable POST fields Year, Month, Type, Dated, PreNext.
- https://raw.githubusercontent.com/DK10WS/SLCM_APP/main/lib/pages/login.dart : third-party client stores credentials in SharedPreferences.
- https://raw.githubusercontent.com/DK10WS/SLCM_APP/main/lib/session_manager.dart : session cookie manager, clears on logout.
- https://github.com/AddisionS/slcm-feedback-form-filler : feedback extension, supply-chain concern.
- https://raw.githubusercontent.com/AddisionS/slcm-feedback-form-filler/main/chrome/manifest.json : scripting, activeTab, all_urls permissions.
- https://mujslcm.jaipur.manipal.edu/Home/Index : first-party landing page, only direct evidence.
- https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization : BOLA definition, server-side object checks.
- https://learn.microsoft.com/en-us/aspnet/web-api/overview/security/enabling-cross-origin-requests-in-web-api : CORS dimensions, wildcard plus credentials invalid.
- https://learn.microsoft.com/en-us/aspnet/web-api/overview/security/preventing-cross-site-request-forgery-csrf-attacks : cookie-auth CSRF and anti-forgery mitigation.
- https://techdocs.akamai.com/site-shield/docs/welcome-site-shield : Site Shield ranges must be allowlisted at origin perimeter.

## ACTIONABLE LEADS
- Reconcile the 13 public routes with internal route registration and assign owners and data classifications.
- Synthetic-account BOLA matrix: endpoint by role by object, semester and event scope changes, immediate role-change effect.
- Cookie review: Secure, HttpOnly, SameSite, rotation after login, logout invalidation, anti-forgery coverage on state-changing POSTs.
- CORS review with approved university origins only, including preflight, headers, redirects, cache variation.
- Error contract review across MVC, Web API, WCF, IIS layers with correlation IDs and redaction.
- Origin closure check: Akamai ranges, direct-origin reachability, X-Forwarded-For trust boundaries.
- If official mobile support is added, use authorization-code flow with PKCE and scoped tokens.

## FLAGS
- All routes come from third-party code and may be stale, incomplete, or wrong; not official API declarations.
- No bearer use found, but absence in examined client files is not proof of server behavior.
- Report names token taxonomy confusion as a trap: anti-forgery token is not an access token.
- Akamai, MVC 5.3, .NET 4.x, M365 identity are requester-supplied assumptions, not OSINT findings.
- SharedPreferences credential storage is a third-party client issue, not a MUJ server finding.
- Report states no active testing was performed and real student identifiers were not enumerated.

## COVERAGE
- Chars read: 46857. EOF confirmed via read_file truncated:false.