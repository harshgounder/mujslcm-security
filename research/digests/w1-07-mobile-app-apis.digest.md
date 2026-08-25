## REPORT (w1-07-mobile-app-apis)

## ANSWER SUMMARY
- No verified first-party "MUJ" or "Manipal App" store listing exists; treat publisher, package ID and privacy policy as the trust anchor, not the app title.
- The only verified first-party surface is the web portal mujslcm.jaipur.manipal.edu with institutional, parent and student login choices.
- No official Swagger/OpenAPI spec, no verified MUJ Postman collection, and no evidence for a mujslcm /api/... pattern; that pattern is not documented.
- Legacy MAHE SLCM is ASP.NET Web Forms: txtUserid, txtpassword, txtCaptcha, __VIEWSTATE, __EVENTVALIDATION and session cookies; not JWT or OAuth.
- Community wrappers (slcm-api.ml, slcm-app.herokuapp.com, canaryGrapher, tejaskash) are credential-handling scrapers, not API documentation; historic deployments should be treated as untrusted.
- CampusAdda (com.app.campusadda, App ID 6465745096) is the clearest native surface: Razorpay/wallet payments, OTP delivery, and valid AASA and assetlinks files.
- Push capability is verified for MTTN and mentioned by CampusAdda, but Firebase and OneSignal attribution is unverified.
- MUJ fees: SLCM portal for existing students, SpaceBasic for hostel/mess; BillDesk, CCAvenue, Razorpay and SBI ePay are not attributable to MUJ tuition.

## KEY FACTS
- https://play.google.com/store/apps/details?id=com.app.campusadda&hl=en_US - CampusAdda Android, updated Apr 3 2026, 10K+ downloads, Razorpay and wallet advertised.
- https://campus-adda.com/.well-known/apple-app-site-association - verified AASA binding U7WSBR3A3J.com.app.campusadda to restaurant, product, order, campaign, event and carpool paths.
- https://campus-adda.com/.well-known/assetlinks.json - Android App Links delegation to com.app.campusadda with two signing-certificate SHA-256 fingerprints.
- https://apps.apple.com/us/app/campusadda/id6465745096 - CampusAdda iOS v3.2.2; purchases, location, contacts, identifiers and diagnostics linked to user.
- https://mujslcm.jaipur.manipal.edu/ - only verified first-party MUJ surface; public login choices for institutional, parent and student roles.
- https://play.google.com/store/apps/details?id=com.yourcompany.mujstellaapp&hl=en_US - MUJStella Android, independent, 1K+ downloads, timetable, attendance and SLCM tracker.
- https://mujstella.in/mujslcm - installable PWA, explicitly not affiliated with MUJ, sign-in required.
- https://apps.apple.com/in/app/manipal-university-jaipur-gym/id6757078406 - MUJ-branded gym app published by Gayatri Software Services; gym credentials, plans, measurements, diet data.
- https://play.google.com/store/apps/details?id=com.mttn.android&hl=en_IN - MTTN Android, 10K+ downloads, SLCM attendance and grade features, push and low-attendance alerts.
- https://slcm.manipal.edu/loginForm.aspx - legacy MAHE login page referenced by community code; not an MUJ Jaipur surface.
- https://raw.githubusercontent.com/nikeplusdash/SLCM-api/master/SLCM.py - shows form fields txtUserid, txtpassword, txtCaptcha and ASP.NET hidden state in a persistent session.
- https://raw.githubusercontent.com/canaryGrapher/slcmAPI/master/routes/validateuser.js - credential-validation routine returning credentialsValid true/false; an avoidable oracle pattern.
- https://www.postman.com/harshalsangole/manipal-api-collection/overview - public workspace with no visible requests, auth or SLCM relationship.
- https://jaipur.manipal.edu/pay-fee-online.php - official fee page: existing students to SLCM portal, hostel/mess to SpaceBasic; no gateway named for tuition.
- https://apkpure.com/slcm-manipal/com.wSLcMManipal_10192522 - archived 2020 third-party wrapper APK; a tier-3 block target for credential safety.

## ACTIONABLE LEADS
- Build a three-tier allow-list: verified MUJ domains; vendor/community apps with verified IDs, publishers and policies; archived APKs and credential wrappers to block.
- Test CampusAdda deep links (carpool share token, order, campaign, event) for open redirects or payment-state tampering before trusting links.
- Enumerate campus-adda.com routes surfaced by the app-link files for any public API or misconfigured endpoints.
- Confirm the current status of slcm-api.ml and slcm-app.herokuapp.com; treat as defunct until proven otherwise and warn students off them.
- Ask CampusAdda, MUJStella and MTTN vendors for attestation or SBOM on Firebase/OneSignal, analytics and payment SDKs.
- Review the SpaceBasic redirect boundary on the MUJ fee page; check for link-injection or lookalike domains.
- Ask MUJ Online/D2L about the Brightspace API surface and the Microsoft-account auth callback failure described in App Store reviews.
- Check alternate stores (Huawei AppGallery, Galaxy Store) for MUJ-branded apps under vendor publishers.
- Report credential-forwarding wrappers to MUJ IT as phishing vectors; consider takedown requests where they solicit portal credentials.
- Never submit credentials to archived APKs such as com.wSLcMManipal_10192522 or any historic wrapper.

## FLAGS
- CampusAdda iOS publisher (Sujit Sonune) differs from Android publisher (Campusadda Technologies Private Limited); resolve before trusting the pair.
- MUJStella package id com.yourcompany.mujstellaapp is a template-style namespace suggesting low maturity; verify developer and build provenance.
- Play "no data collected" claims for MUJStella and MTTN sit uneasily beside SLCM-linked attendance and grade features; unresolved.
- CampusAdda Play listing says data is not encrypted while its policy claims reasonable safeguards; the store declaration should dominate risk assessment.
- Reddit posts about Outlook password changes and Microsoft Authenticator are anecdotes, not proof of Entra OAuth, OIDC or token issuance.
- The Brightspace App Store review is user feedback, not vendor documentation.
- MAHE Dubai-SLCM (UNIKUL) and D2L Brightspace are separate ecosystems; do not conflate them with MUJ Jaipur.
- No .asmx/.svc endpoint and no verified /api/ base was found; both absences are search-based and moderate confidence only.

## COVERAGE
Source read in full: /home/liebert511/mujslcm-recon/research/w1-07-mobile-app-apis.md. File char count as read: 37483 (244 lines). Read pagination reached line 244 of 244; EOF confirmed (truncated: false).