## REPORT (w1-05-code-leaks)

## ANSWER SUMMARY
- 4 GitHub repos plus 1 npm package (yemit) automate SLCM login, attendance, marks, grades, profile and timetable; portal flow must be treated as public knowledge.
- No verified live credential found: no SLCM password, private key, DB connection string or bearer token in reviewed default branches; .env.example holds placeholders only.
- Credential-handling risk is real: wrappers accept username/password as request parameters, and slcmAPI routes support GET and POST, which can leak credentials via logs, history and referrers.
- Two secret-bearing configs are public: Firebase google-services.json (DK10WS/SLCM_APP) and a Django SECRET_KEY with DEBUG=True (Anushkakumar10/muj_slcm); operational impact untested.
- Flutter client (SLCM SWITCH) shows cookie + request-verification + parent OTP + session persistence; no JWT evidence exists in any reviewed artifact.
- Cert Spotter CT data yields 103 manipal.edu hostnames, 11 Jaipur-scoped (incl muj.slcm.jaipur.manipal.edu, mujerp, mujone, rms) and 7 with dev/uat/preprod labels.
- LeakIX service index lists 117 records incl dev-* names; the leak-scoped query hit a login wall, so no usable leak record was confirmed.
- Verdict: material public technical exposure exists, but no verified live SLCM credential compromise was established.

## KEY FACTS
- https://github.com/sankalp2004/SLCM-is-Dumb - end-to-end Selenium/OCR login and CGPA automation; exposes portal flow and CAPTCHA handling.
- https://github.com/sankalp2004/SLCM-is-Dumb/blob/master/config.py - names exact routes loginForm.aspx and GradeSheet.aspx.
- https://github.com/canaryGrapher/slcmAPI - archived Express/Puppeteer API that receives SLCM credentials; archived Oct 17, 2024.
- https://github.com/canaryGrapher/slcmAPI/blob/master/routes/getattendance.js - GET and POST handlers accept username/password, the core unsafe pattern.
- https://github.com/canaryGrapher/slcmAPI/blob/master/routes/getmarks.js - credentials in a GET-compatible handler with semester input.
- https://github.com/tejaskash/slcm-api - Flask wrapper; POST /api/v1/get takes credentials plus ATTENDANCE, MARKS or ALL.
- https://github.com/DK10WS/SLCM_APP - Flutter SLCM SWITCH client with student/parent login, OTP path and session handling.
- https://github.com/DK10WS/SLCM_APP/blob/main/android/app/google-services.json - public Firebase client configuration; rules, not key secrecy, decide risk.
- https://github.com/DK10WS/SLCM_APP/blob/main/lib/pages/login.dart - shows request-verification material, cookie combining and parent OTP flow.
- https://github.com/DK10WS/SLCM_APP/blob/main/lib/session_manager.dart - nullable session-cookie value persisted for later use.
- https://github.com/Anushkakumar10/muj_slcm/blob/main/muj_slcm/muj_slcm/settings.py - public Django SECRET_KEY and DEBUG=True; value redacted in report.
- https://github.com/slcm-manipal/slcm-manipal.github.io/blob/master/index.html - authenticated-looking snapshot with ASP.NET state fields and personal or academic content.
- https://www.npmjs.com/package/yemit - CasperJS attendance tool targeting slcm.manipal.edu, published about 8 years before the indexed snapshot.
- https://api.certspotter.com/v1/issuances?domain=manipal.edu&include_subdomains=true&expand=dns_names - 103 distinct CT hostnames including dev/uat/preprod labels.
- https://leakix.net/search?scope=service&q=manipal.edu - 117 indexed service records incl dev-api, dev-techtatva and dev-register-techtatva names.

## ACTIONABLE LEADS
- Search repo history and forks of the four projects for removed .env files or real secret commits (medium confidence).
- Check whether muj_slcm Django prototype was ever deployed; rotate SECRET_KEY if so, disable DEBUG, strip secrets from history.
- Contact owners of slcm-manipal.github.io to remove or redact the snapshot's personal and academic content.
- Map CT names to owners, focusing on dev-api, dev-crm, dev-payment, content-uat, content-preprod, uat, preprod.
- Re-query LeakIX leak scope via API/auth; validate any record at record level before calling it a breach.
- Test the Firebase project's Realtime Database, Storage, Auth and App Check rules internally for the google-services.json project.
- Audit cookie flags, CSRF enforcement, OTP rate limits and session rotation on mujslcm.jaipur.manipal.edu using institution-controlled accounts.
- Verify whether historical deployments slcm-api.ml and slcm-app.herokuapp.com are still live; treat them as credential-phishing vectors.
- Monitor npm registry, GitHub and paste sites for new SLCM credential material; keep the negative findings re-checkable.
- If a working credential is ever found, report it privately to MUJ IT and the platform; never reproduce it.

## FLAGS
- crt.sh direct queries returned 404 in this environment; the 103-name count rests on Cert Spotter alone (single source).
- GitHub candidate madhav-manchanda/SlcmAndLms-aggregator returned 404 and was excluded from the inventory.
- Postman workspace overview showed no requests, auth or variables; scope unverified, not tied to SLCM.
- yemit is roughly 8 years old; its selectors and host assumptions may be stale.
- LeakIX 117 service records are an index, not breach evidence; dev-* names are inventory leads only.
- Firebase client API key is an identifier; its presence proves no unauthorized database access.
- GitLab, Pastebin, gist and RaonData negatives are moderate confidence; unindexed or deleted pastes cannot be ruled out.
- Behaviors quoted from old source code may not match current portal markup or auth flow.

## COVERAGE
Source read in full: /home/liebert511/mujslcm-recon/research/w1-05-code-leaks.md. File char count as read: 47931 (330 lines). Read pagination reached line 330 of 330; EOF confirmed (truncated: false).