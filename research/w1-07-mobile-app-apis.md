# MUJ Student Apps and SLCM API Exposure Map

## Executive Summary

- **Fragmented App Estate**: The evidence does not support a single, current, first-party mobile app called simply "MUJ" or "Manipal App" for Jaipur students. Instead, students encounter the official MUJ web portal, an MUJ-branded gym app published by a software vendor, MUJStella as an independent student platform, CampusAdda as a commercial campus service, and generic or adjacent SLCM/LMS clients. Treat the publisher, not the app title, as the trust anchor.

- **Official Portal, Not Public API**: The verified first-party MUJ surface is `https://mujslcm.jaipur.manipal.edu/`, whose public page offers institutional, parent, and student sign-in choices [5]. I found no official MUJ Swagger/OpenAPI specification, no verified MUJ Postman collection, and no public evidence supporting the proposed `https://mujslcm.jaipur.manipal.edu/api/...` pattern. Do not treat that pattern as documented merely because it is plausible.

- **Legacy SLCM Is ASP.NET Web Forms**: Public community source code for the separate MAHE Manipal SLCM system references `https://slcm.manipal.edu/loginForm.aspx`, `Academics.aspx`, and `StudentProfile.aspx`. One implementation submits `txtUserid`, `txtpassword`, `txtCaptcha`, `__VIEWSTATE`, `__EVENTVALIDATION`, and `__VIEWSTATEGENERATOR` through a persistent HTTP session [20]. The evidence supports an ASP.NET form-state and cookie-session model, not a documented JWT or OAuth API.

- **Community APIs Are Credential-Handling Scrapers**: Public repositories expose wrapper routes such as `POST /api/v1/get`, `/getattendance`, `/getscores`, `/getprofile`, and `/validateuser` [2][18][17][19][15]. These projects automate or scrape the MAHE portal; they are not vendor API documentation. Historic deployment domains should be considered untrusted and potentially defunct.

- **CampusAdda Has the Clearest Native-App Surface**: The Android app `com.app.campusadda` was updated April 3, 2026 and explicitly advertises Razorpay and wallet payments [27]. Its domain publishes both Apple App Site Association and Android Digital Asset Links documents, proving configured HTTPS universal/app links for restaurant, product, order, campaign, event, carpool, cuisine, and category content [34][33].

- **Push Exists, Vendor Attribution Does Not**: MTTN advertises alerts, announcements, push notifications, and low-attendance notifications [26][22]. CampusAdda's policy also mentions push notifications, but neither its policy nor the reviewed store evidence names Firebase or OneSignal [23]. Report push capability as verified, but Firebase/OneSignal as unverified.

- **MUJ Fee Payment Is Split Across Trust Boundaries**: MUJ's official fee page sends existing students to the SLCM portal and directs hostel and mess payments to SpaceBasic [21]. CampusAdda separately names Razorpay for food and campus-commerce payments [27]. The official MUJ fee page does not name BillDesk, CCAvenue, Razorpay, or SBI ePay for tuition [21].

- **Current MUJ Authentication Remains Partly Opaque**: The public MUJ page exposes institutional, parent, and student sign-in choices, while student Reddit posts anecdotally mention Outlook password changes and Microsoft Authenticator [35][36]. That does not prove OAuth, OpenID Connect, JWT issuance, token audience, or a mobile-app callback scheme. Any such protocol claim would exceed the available evidence.

## Scope, Evidence Model, and Safety Boundary

This is an OSINT report as of August 25, 2026. It uses public app-store pages, public privacy policies, first-party university pages, public web-association files, public GitHub repositories, a public Postman workspace, and public community discussions. It does not log into any student account, submit credentials, capture private traffic, bypass CAPTCHA, enumerate authenticated resources, or test whether historic third-party services remain exploitable.

The report separates four evidence classes. **First-party** means an MUJ, MAHE, or named vendor page describing its own system. **Store-verified** means Google Play or Apple publicly exposes the publisher, update, privacy, or feature statement. **Community-documented** means source code or a student project describes observed behavior, but the university does not endorse it. **Unverified or negative** means targeted searches did not find supporting material; this is not proof that a private implementation does not exist.

I do not provide private chain-of-thought. Instead, the report makes the decision logic auditable through exact URLs, source classifications, citations, contradictions, and explicit confidence levels. In particular, an `.aspx` path in historical source is reported as a publicly referenced page, not as an invitation to access it. A store title containing "Manipal" is not classified as official unless the publisher or a first-party source establishes that relationship.

This distinction matters because the ecosystem spans at least three institutional contexts. MUJ Jaipur uses `mujslcm.jaipur.manipal.edu`; MAHE Manipal uses `slcm.manipal.edu`; and MAHE Dubai has a separately published SLCM app from UNIKUL. Community projects aimed at MAHE's older portal cannot automatically be applied to MUJ Jaipur. Likewise, Online Manipal's D2L Brightspace LMS is not evidence that on-campus MUJ SLCM exposes D2L APIs.

The practical recommendation is to maintain an allow-list containing the verified university domain, the app-store package or App ID, and the actual publisher. Students should not enter university credentials into historic wrapper deployments such as `slcm-api.ml` or `slcm-app.herokuapp.com`. Their public READMEs demonstrate why: the wrappers solicit portal credentials and then retrieve academic records [2][1].

## App Inventory: Official, Vendor, and Community Clients

### Exact inventory

| App or surface | Platform and identifier | Publisher or status | Last update/version visible | Public permissions or privacy statement | MUJ/SLCM role and exact URL |
|---|---|---|---|---|---|
| MUJ SLCM portal | Mobile web; no store package | First-party MUJ portal | Not stated | Public page exposes sign-in choices, not app permissions | Official student portal: `https://mujslcm.jaipur.manipal.edu/` [5] |
| CampusAdda | Android, `com.app.campusadda` | Campusadda Technologies Private Limited | Updated Apr 3, 2026; 10K+ downloads | Play says no third-party sharing, possible personal-information collection, deletion available, and data not encrypted | MUJ-focused food, events, wallet, and campus service app: `https://play.google.com/store/apps/details?id=com.app.campusadda&hl=en_US` [27] |
| CampusAdda | iOS/iPadOS, App ID `6465745096` | Sujit Sonune | Version 3.2.2; page shows Apr 4 without a year | Data linked to the user may include purchases, location, contact information, contacts, user content, identifiers, usage, and diagnostics | `https://apps.apple.com/us/app/campusadda/id6465745096` [8] |
| Mujstella | Android, `com.yourcompany.mujstellaapp` | MUJstella; developer contact Akshit Raj | Updated Jan 21, 2026; 1K+ downloads | Play says no third-party sharing and no data collected | Timetable, attendance, resources, directory, and SLCM portal tracker: `https://play.google.com/store/apps/details?id=com.yourcompany.mujstellaapp&hl=en_US` [24] |
| MUJStella web/PWA | Installable web app | Explicitly independent and not affiliated with MUJ | Not stated | Privacy link present; public page says sign-in required | `https://mujstella.in/mujslcm`; home-screen installation and offline behavior are advertised [28] |
| Manipal University Jaipur Gym | iOS/iPadOS, App ID `6757078406` | Gayatri Software Services Private Limited | Version/update date not displayed | Apple says the developer does not collect data | Gym credentials, plan details, measurements, diet, and exercise plans: `https://apps.apple.com/in/app/manipal-university-jaipur-gym/id6757078406` [6] |
| SLcM Manipal | Archived Android package `com.wSLcMManipal_10192522` | Pramath N R; no official MAHE/MUJ status established | Version 1.0; updated Jan 30, 2020 | Permissions not stated on the archive page | Third-party portal wrapper for the wider Manipal SLCM ecosystem: `https://apkpure.com/slcm-manipal/com.wSLcMManipal_10192522` [13] |
| Manipal The Talk Network | Android, `com.mttn.android` | MTTN; developer contact Advaith Gurunath | Updated Sep 26, 2025; 10K+ downloads | Play says no data shared and no data collected | Community media app with SLCM attendance and grade features: `https://play.google.com/store/apps/details?id=com.mttn.android&hl=en_IN` [26] |
| MTTN iOS link | iOS, App ID `1386295566` | Linked by MTTN's own app page | Current store metadata not retrievable in this review | Not established | Public landing page links `https://apps.apple.com/us/app/mttn/id1386295566` [22] |
| Brightspace Pulse | iOS/iPadOS, App ID `1001688546` | D2L Corporation | Version 2.2511.0; update date not displayed in the extracted listing | Apple lists contact info, user content, identifiers, and diagnostics as linked; location, usage, and diagnostics may be unlinked | Generic D2L mobile LMS client: `https://apps.apple.com/in/app/brightspace-pulse/id1001688546` [30] |
| MAHE DUBAI-SLCM | Android, `com.unikul.manipaldubai` | UNIKUL Dev Team / UNIKUL Solutions | Updated Aug 29, 2025; 1K+ downloads | Play says no data shared or collected | Adjacent SLCM ecosystem, not MUJ Jaipur: `https://play.google.com/store/apps/details?id=com.unikul.manipaldubai&hl=en_US` [25] |
| MAHE DUBAI-SLCM | iOS/iPadOS, App ID `1627570076` | UNIKUL Solutions Private Limited | Version 1.1.6, Nov 8, 2024 as displayed in the US locale | Apple says the developer does not collect data | Adjacent ecosystem: `https://apps.apple.com/us/app/mahe-dubai-slcm/id1627570076` [29] |

The inventory's main surprise is the absence of a verified current store app published directly by Manipal University Jaipur and titled simply "MUJ," "Manipal University Jaipur," or "Manipal App." Searches for those names repeatedly returned the web portal, Manipal Hospitals, MIT.ai Student for Manipal Institute of Technology, or MAHE Dubai. Those are false positives for an MUJ Jaipur inventory.

There is also no independently verified, standalone MUJ attendance app. Attendance is instead a feature inside MUJStella, MTTN, the official SLCM web portal, and community API wrappers. That is an important distinction: a student searching for an "attendance app" is more likely to encounter an unofficial client that asks for portal credentials.

### Case study: MUJStella versus the MUJ Gym app

MUJStella is transparent about being an independent student platform [28]. Its Android listing offers timetable, attendance, resources, directory, and SLCM tracking, while the associated website can be installed as a PWA [24][28]. The breadth is useful, but the university is not the publisher and the public materials do not document an API or login handoff.

The gym app is narrower: gym-issued credentials expose plans, measurements, diet, and exercise data [6]. Its MUJ name suggests an operational relationship, but the publisher is Gayatri Software Services, not MUJ [6]. The lesson is that branding and operational use do not equal institutional publication. Trust decisions should bind the app ID, publisher, privacy policy, and support channel together.

## Public SLCM API and Legacy Service Surface

### Exact public surface table

| Surface | Exact base or endpoint | Method or interface | Authentication evidence | Status and interpretation |
|---|---|---|---|---|
| MUJ portal | `https://mujslcm.jaipur.manipal.edu/` | Public login page | Institutional, parent, and student sign-in choices | Verified first-party web surface; no public API specification [5] |
| MAHE legacy SLCM | `https://slcm.manipal.edu/loginForm.aspx` | Browser GET/login form; community code then submits login | User ID, password, CAPTCHA, ASP.NET form state, session cookies | Community-observed upstream page, not MUJ Jaipur [20] |
| MAHE academics | `https://slcm.manipal.edu/Academics.aspx` | Community code uses authenticated navigation or POST | Existing authenticated session | Attendance and marks source [20][18][17] |
| MAHE profile | `https://slcm.manipal.edu/StudentProfile.aspx` | Community code uses authenticated navigation or POST | Existing authenticated session | Student-profile source [20][19] |
| tejaskash wrapper | Historic base `https://slcm-api.ml`; route `POST /api/v1/get` | JSON request | `request.credentials.username`, `request.credentials.password`, plus `request.type` | Community Flask wrapper; request types `ATTENDANCE`, `MARKS`, `ALL` [2] |
| nikeplusdash wrapper | Historic `https://slcm-app.herokuapp.com/`; `/login`; docs at `/docs` | README does not specify all methods | Wrapper logs in to `slcm.manipal.edu`; user data claimed not stored | Community project, created in 2020; not an official API [1] |
| canaryGrapher attendance | `/getattendance` | GET and POST | `username`, `password`, optional `novalidate`; validation through local `/validateuser` | Community Express/Puppeteer route [18] |
| canaryGrapher marks | `/getscores` | GET and POST | `username`, `password`, `semester`, optional `novalidate` | Community scraper route [17] |
| canaryGrapher profile | `/getprofile` | GET and POST | `username`, `password`, optional `novalidate` | Community scraper route [19] |
| canaryGrapher validation | `/validateuser` | GET and POST | `username`, `password`; success checked through a post-login selector | Returns `credentialsValid: true/false` [15] |
| Public Postman workspace | `https://www.postman.com/harshalsangole/manipal-api-collection/overview` | No visible requests | No visible auth settings or environment | Not tied to SLCM, MUJ, or `manipal.edu`; user-published, no description [10] |

The key finding is that the public documentation is almost entirely **community reverse-engineered wrappers**, not an official API product. The tejaskash repository explicitly accepts university credentials and returns attendance or marks. CanaryGrapher launches browser automation against form selectors. Nikeplusdash uses direct HTTP requests and an HTTP session. These are three implementations of screen-scraping or form automation, not three confirmations of a stable REST contract.

The public source does establish exact `.aspx` pages. It does **not** establish any SLCM `.asmx` or `.svc` service, and targeted searches for those suffixes produced no relevant result. It also does not verify a MUJ Jaipur `/api/` base. The safest conclusion is therefore narrow: public code references legacy MAHE `.aspx` pages; the current MUJ portal exposes a login UI; no official Swagger/OpenAPI schema or current MUJ API catalog was found.

### Case study: CanaryGrapher's scraper reveals the contract boundary

The attendance route first validates credentials through its own local `/validateuser`, then automates the upstream login page, opens `Academics.aspx`, selects an attendance tab, and parses the `#tblAttendancePercentage` table into subject, subject code, total classes, present, absent, and percentage fields [18]. The marks route follows a similar path but selects a different tab and parses accordion content [17].

This reveals a crucial mechanism: the apparent REST endpoints are wrappers around HTML behavior. If MUJ or MAHE changes a selector, CAPTCHA flow, page layout, or session policy, the wrapper may fail even if the portal remains available. The operational recommendation is not to build production student services on these historic routes. Institutions should publish a scoped, consented API if third-party access is desired; students should avoid forwarding credentials to unofficial middleware.

## Authentication and Public Traffic-Analysis Evidence

The strongest authentication evidence comes from public source code, not from a packet-capture article. The Python implementation in `nikeplusdash/SLCM-api` creates a `requests.Session()`, fetches the SLCM login page and CAPTCHA image, extracts ASP.NET hidden values, and posts `txtUserid`, `txtpassword`, `txtCaptcha`, `__EVENTVALIDATION`, `__VIEWSTATEGENERATOR`, and `__VIEWSTATE` [20]. It then reuses the session to request profile and academic pages [20].

That is consistent with an ASP.NET Web Forms authentication workflow: hidden form-state fields preserve page state, CAPTCHA challenges automation, and the session carries cookies. The hidden fields are **not bearer tokens** and should not be described as JWTs. The reviewed code does not expose an `Authorization: Bearer` header, OAuth authorization endpoint, OpenID discovery document, access token, refresh token, or JWT claims.

The JavaScript and Puppeteer implementation reaches the same portal through browser automation. It fills `#txtUserid` and `#txtpassword`, clicks `#btnLogin`, waits for navigation, and uses a post-login selector to infer success [15]. In other words, the public projects either preserve an HTTP session or preserve a browser context. Neither provides evidence of a stable mobile API authentication contract.

| Authentication context | Publicly supported mechanism | What is not supported by evidence | Confidence |
|---|---|---|---|
| MAHE legacy SLCM | Form login, CAPTCHA, ASP.NET state fields, cookie-bearing session | JWT, OAuth, OpenID Connect, API key | High |
| CanaryGrapher wrapper | Credentials supplied to wrapper; browser automation logs into upstream portal | Wrapper-issued token standard | High |
| tejaskash wrapper | Credentials inside JSON request to a historic third-party deployment | Official endorsement or safe current operation | High |
| Current MUJ portal | Separate institutional, parent, and student sign-in choices | Exact redirect URI, token format, mobile callback | Medium |
| MTTN SLCM feature | Public page says users log in once and CAPTCHA is solved automatically | Endpoint, credential storage, token, encryption model | Medium [22] |

Targeted searches did not locate a Medium or dev.to article documenting students intercepting MUJ app traffic. Reddit results discuss login problems rather than packet capture. One MUJ thread recommends Outlook and Microsoft Authenticator, while another says an Outlook-triggered password change allowed subsequent SLCM login [35][36]. These are useful current-context hints, but they are anecdotes. They do not prove that the MUJ portal uses Microsoft Entra OAuth/OIDC, nor do they reveal token format or mobile redirect behavior.

The security implication is straightforward. A service asking for raw SLCM credentials is operating at a much higher trust level than a standards-based delegated authorization client. None of the community wrappers demonstrates delegated consent. Even if a repository claims not to store data, students cannot verify the behavior of a historic hosted deployment from the README alone. Use the university portal directly.

## Push, Analytics, and Backend Signals

No reviewed MUJ-related store listing or privacy policy explicitly names Firebase Cloud Messaging, Firebase Analytics, or OneSignal. Searches for those combinations returned generic vendor documentation and unrelated student projects, not evidence tied to the listed MUJ apps. Therefore, assigning Firebase or OneSignal to MUJ, MUJStella, CampusAdda, or MTTN would be speculation.

Push capability itself is better supported. MTTN's Android listing advertises alerts, announcements, and push notifications [26]. Its public landing page says a linked SLCM profile can trigger low-attendance notifications [22]. CampusAdda's privacy policy refers generally to push notifications and internal analytics/reporting but does not identify an SDK provider [23]. MAHE Dubai-SLCM advertises notifications and alerts without naming the transport [25].

| App | Push or analytics capability | Named SDK/vendor | Backend signal that can safely be reported |
|---|---|---|---|
| CampusAdda | Push notifications and internal analytics mentioned in policy | None; Firebase and OneSignal not named | Native Android/iOS service with OTP, wallet, payments, maps, and verified HTTPS app links [27][23] |
| MTTN | Push, announcements, and low-attendance notifications | None | Community app links to SLCM-derived attendance and grades [22] |
| MUJStella | Updates/announcements and SLCM tracker | None | Android app plus installable PWA; public API not documented [24][28] |
| MAHE Dubai-SLCM | Notifications and alerts | None | Institution-specific SLCM product from UNIKUL, separate from MUJ [25] |
| MUJ Gym | No push/analytics statement found | None | Vendor app with member credentials and plan data [6] |

CampusAdda provides a useful data-quality contradiction. Google Play says the Android app's data is not encrypted [27], while the privacy policy says reasonable technical and organizational safeguards are used but cannot guarantee perfect security [23]. These statements are not necessarily logically incompatible, but the store declaration should dominate a student's practical risk assessment because it is the platform's structured disclosure.

The recommendation is to avoid inferring architecture from features. Push notifications do not prove Firebase; social login does not prove a particular identity broker; maps do not prove Google Maps unless named. If an institutional risk register needs SDK-level certainty, it should use a university-authorized software bill of materials or vendor attestation rather than public speculation.

## Payment Integrations and Redirect Boundaries

There are two separate payment contexts. CampusAdda handles campus-commerce transactions. Its Android and iOS listings explicitly advertise secure payment through Razorpay or an in-app wallet [27][8]. The app also uses OTP-tracked delivery, coupons, points, wallet balances, and order history. This supports a native commerce backend with a payment-processor boundary, but the listings do not document Razorpay order-creation endpoints, callback URLs, webhook signatures, or key handling.

MUJ's first-party fee page is different. Existing students are directed to `https://mujslcm.jaipur.manipal.edu/`, while hostel and mess fees are routed through the SpaceBasic app [21]. The same page documents bank-transfer routes for other cases, but it does not name BillDesk, CCAvenue, Razorpay, or SBI ePay for tuition [21]. Generic BillDesk documentation exists publicly, but generic gateway documentation is not evidence of an MUJ integration.

| Payment use case | Verified route or provider | Public integration detail | Assessment |
|---|---|---|---|
| MUJ existing-student fees | MUJ SLCM portal, `https://mujslcm.jaipur.manipal.edu/` | Portal entry point only | First-party and high confidence [21] |
| MUJ hostel and mess | SpaceBasic app | Provider named; API/callback not documented | First-party and high confidence [21] |
| CampusAdda orders | Razorpay or CampusAdda wallet | Provider named in both store descriptions; no merchant API detail | Store-verified [27][8] |
| BillDesk | No MUJ-specific tie found | Generic documentation only | Do not attribute to MUJ |
| CCAvenue | No MUJ-specific tie found | None | Do not attribute to MUJ |
| SBI ePay | No MUJ-specific tie found | None | Do not attribute to MUJ |

### Case study: CampusAdda's payment and link boundary

CampusAdda is the only reviewed app where payments and verified app links coexist in public documentation. A web link can open a restaurant, product, order, campaign, event, or carpool route in the app, and the user may then enter a commerce flow using Razorpay or the wallet [34][27]. That is convenient, but it also creates a phishing-sensitive boundary: users should verify the `campus-adda.com` host before following payment or order links.

No source publishes the private gateway credentials or server callbacks, and this report does not attempt to discover them. The correct operational control is domain verification, signed mobile builds, server-side amount validation, and payment-status confirmation from the processor. Public deep-link metadata should never be mistaken for authorization to change payment state.

## Deep Links, Universal Links, and Web-to-App Bridges

CampusAdda provides conclusive, first-party web-association evidence. Its Apple file at `https://campus-adda.com/.well-known/apple-app-site-association` binds `U7WSBR3A3J.com.app.campusadda` to these HTTPS path families: `/restaurant/*`, `/product/*`, `/order/*`, `/campaign/*`, `/event/*`, `/events/detail?slug=...`, `/carpool/ride/*`, `/carpool/share?token=...`, `/cuisine-restaurant`, and `/category-product` [34].

Its Android file at `https://campus-adda.com/.well-known/assetlinks.json` delegates `common.handle_all_urls` to `com.app.campusadda` and publishes two signing-certificate SHA-256 fingerprints [33]. Together, these files prove configured universal links and Android App Links. They do not prove that every route works in every installed version, but they are much stronger evidence than a marketing page.

| Bridge | Public evidence | Exact URL | Conclusion |
|---|---|---|---|
| CampusAdda Apple universal links | Valid AASA app identifier and path components | `https://campus-adda.com/.well-known/apple-app-site-association` | Verified [34] |
| CampusAdda Android App Links | Valid Digital Asset Links package and fingerprints | `https://campus-adda.com/.well-known/assetlinks.json` | Verified [33] |
| MUJStella PWA install | Page offers home-screen installation, offline use, and sign-in | `https://mujstella.in/mujslcm` | Verified PWA bridge, not verified native universal links [28] |
| MTTN stores | Landing page links Google Play and Apple App Store | `https://app.manipalthetalk.org/` | Verified store handoff; no URI scheme documented [22] |
| MTTN to SLCM | Landing page says SLCM attendance/grades can be linked and users log in once | `https://app.manipalthetalk.org/` | Verified feature claim; endpoint/token details absent [22] |
| Brightspace browser handoff | App listing says it can log into D2L Brightspace through a browser | `https://apps.apple.com/in/app/brightspace-pulse/id1001688546` | Verified browser handoff; no MUJ-specific callback published [30] |
| MUJ portal sign-in | Portal exposes institutional, parent, and student login choices | `https://mujslcm.jaipur.manipal.edu/` | Verified web login choices; redirect targets not publicly documented [5] |

The reviewed MUJStella and MTTN well-known paths did not yield valid association documents, so this report does not claim native universal links for them. MUJStella is still a web-to-home-screen bridge because its page explicitly offers installation and offline behavior [28]. That is a PWA capability, not evidence of Android App Links or Apple Universal Links.

Brightspace Pulse presents another instructive boundary. The vendor listing says additional tasks can be completed by logging into Brightspace through a browser [30]. An App Store review describes a Microsoft-account authentication flow failing to return from an in-app WebKit view [30]. A review is not vendor documentation, but it illustrates why callback handling, cookie policy, and identity-provider compatibility matter in LMS apps.

## Synthesis: Documented, Inferred, and Unknown

| Dimension | Official MUJ portal | Legacy MAHE SLCM | CampusAdda | MUJStella | MTTN | D2L/MAHE Dubai |
|---|---|---|---|---|---|---|
| Primary role | Student lifecycle web portal | Older lifecycle portal | Campus commerce and lifestyle | Independent student companion | Community media plus SLCM convenience | LMS or separate institutional SLCM |
| Trust anchor | `jaipur.manipal.edu` / `mujslcm.jaipur.manipal.edu` | `slcm.manipal.edu` | Store package plus `campus-adda.com` | Store developer plus explicit non-affiliation | MTTN publisher and landing page | D2L or UNIKUL publisher |
| Public API evidence | None found | HTML pages and community scrapers | No public business API found | No public API found | No endpoint documentation | No MUJ-specific public API found |
| Authentication mechanism | Public login choices; exact protocol unknown | ASP.NET form state, CAPTCHA, cookie session | OTP/social-login language; provider details limited | Sign-in stated; mechanism unknown | Login-once/CAPTCHA automation claim | Browser handoff or institution-specific login |
| Payment role | Tuition entry point | None documented | Razorpay and wallet | None documented | None documented | None documented |
| App-link evidence | None publicly verified | Not applicable | Strong AASA and assetlinks evidence | PWA install only | Store links only | Browser handoff only |
| Main risk | Users may confuse unofficial clients with the portal | Credentials exposed to brittle wrappers | Commerce, location, wallet, and deep-link phishing | Non-affiliated app handling student workflows | Automated SLCM access without public protocol detail | Identity callback and institution-mismatch risk |

Three non-obvious tensions emerge.

First, **the richest public endpoint documentation belongs to the least authoritative sources**. GitHub repositories reveal exact routes and form fields, but they describe 2020-era community wrappers and the MAHE host. The first-party MUJ portal reveals almost no technical contract. This means technical specificity must not be confused with current applicability.

Second, **app-store privacy statements and functional scope do not always align intuitively**. MUJStella and MTTN declare no data collection on Google Play while offering attendance, grades, directories, or SLCM-linked features [24][26]. Those declarations may reflect local processing, browser handoff, a narrow interpretation of collection, or current implementation, but public evidence does not resolve which. A university assessment should ask for a data-flow diagram rather than infer one.

Third, **deep-link maturity is strongest in a commercial campus app, not the academic portal ecosystem**. CampusAdda publishes standards-compliant association files, while the official MUJ page remains a web login surface and community academic apps publish little callback detail. This suggests that commerce-oriented mobile engineering is more publicly observable than lifecycle-management integration.

The strategic recommendation is a three-tier allow-list. Tier 1 contains first-party university portals and institution-contracted LMS surfaces. Tier 2 contains vendor or community apps with verified package IDs, publishers, policies, and narrowly scoped use. Tier 3 contains archived APKs and credential-forwarding wrappers; these should be blocked or strongly discouraged. If MUJ wants a third-party ecosystem, it should replace password-sharing scrapers with a documented, scoped OAuth/OIDC API, publish mobile association files, and identify approved clients.

## VERDICT

**Overall confidence: High for the app inventory and historical MAHE SLCM mechanics; medium for current MUJ authentication; high for the negative conclusion that no public official MUJ API documentation was located.**

1. **Which apps serve MUJ students?** Verified current or relevant surfaces include the MUJ web portal, CampusAdda Android/iOS, MUJStella Android/PWA, and the vendor-published MUJ Gym iOS app. Brightspace Pulse is the generic mobile client for the D2L ecosystem used by MUJ Online, while MTTN, archived SLcM Manipal, and MAHE Dubai-SLCM belong to the wider Manipal/SLCM ecosystem rather than constituting official MUJ Jaipur apps.

2. **What public API documentation exists?** No official MUJ Swagger/OpenAPI or verified SLCM Postman collection was found. Public technical detail comes from community GitHub projects. One public Postman workspace titled "Manipal API Collection" exposes no visible requests, URLs, authentication, description, or SLCM relationship [10].

3. **What endpoints are publicly documented?** The strongest exact references are the MAHE pages `loginForm.aspx`, `Academics.aspx`, and `StudentProfile.aspx`; historic wrapper routes `POST /api/v1/get`, `/login`, `/getattendance`, `/getscores`, `/getprofile`, and `/validateuser`; and the official MUJ portal root. No relevant `.asmx` or `.svc` endpoint and no verified MUJ `/api/...` base was found.

4. **What authentication flow is supported?** Historical MAHE source supports ASP.NET Web Forms state, CAPTCHA, and cookie sessions. Current MUJ evidence supports multiple login choices and anecdotal Outlook/Microsoft Authenticator involvement, but not a documented JWT, OAuth, or OIDC contract.

5. **What SDK, payment, and bridge evidence exists?** Push behavior is documented, but Firebase and OneSignal attribution is not. CampusAdda names Razorpay and publishes valid iOS/Android association files. MUJ names its SLCM portal for existing-student fees and SpaceBasic for hostel/mess fees; BillDesk, CCAvenue, and SBI ePay are not established for MUJ by the reviewed first-party material.

**Decision-ready conclusion:** Use `https://mujslcm.jaipur.manipal.edu/` directly for official MUJ lifecycle and fee access. Treat MUJStella, CampusAdda, and MTTN according to their actual publishers and disclosed scopes. Do not submit university credentials to archived APKs or historic wrapper APIs. For institutional integration, require written vendor approval, current API documentation, delegated authorization, data-flow disclosure, and signed-app/domain verification.

## References

1. *GitHub - nikeplusdash/SLCM-api: An api for https://slcm.manipal.edu · GitHub*. https://github.com/nikeplusdash/SLCM-api
2. *GitHub - tejaskash/slcm-api: A RESTful API to get attendance and marks data from SLCM Portal at Manipal University, written in Python using Flask. · GitHub*. https://github.com/tejaskash/slcm-api
3. *GitHub - canaryGrapher/slcmAPI: The API for SLcM, Manipal. Get your marks, your attendance and your profile details · GitHub*. https://github.com/canaryGrapher/slcmAPI
4. *Mujstella - MUJ Student App | Manipal University Jaipur*. https://mujstella.vercel.app/
5. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
6. *‎Manipal University Jaipur Gym App - App Store*. https://apps.apple.com/in/app/manipal-university-jaipur-gym/id6757078406
7. *Online Bachelor and Master Programmes | Online Degree Programs in India | Online Manipal*. https://muj.onlinemanipal.com/
8. *‎CampusAdda App - App Store*. https://apps.apple.com/us/app/campusadda/id6465745096
9. *Student Portal Login- MAHE (Manipal Academy Of Higher Education)*. https://www.manipal.edu/mu/academics/student-portal.html
10. *Manipal API Collection | Postman API Network*. https://www.postman.com/harshalsangole/manipal-api-collection/overview
11. *Manipal University Jaipur (Online) | D2L*. https://www.d2l.com/en-in/why-d2l/customers/manipal-university-jaipur-online
12. *MAHE Payment Portal*. http://payment.manipal.edu/
13. *SLcM Manipal APK for Android Download*. https://apkpure.com/slcm-manipal/com.wSLcMManipal_10192522
14. *slcmAPI/routes at master · canaryGrapher/slcmAPI · GitHub*. https://github.com/canaryGrapher/slcmAPI/tree/master/routes/
15. *raw.githubusercontent.com*. https://raw.githubusercontent.com/canaryGrapher/slcmAPI/master/routes/validateuser.js
16. *raw.githubusercontent.com*. https://raw.githubusercontent.com/canaryGrapher/slcmAPI/master/server.js
17. *raw.githubusercontent.com*. https://raw.githubusercontent.com/canaryGrapher/slcmAPI/master/routes/getmarks.js
18. *raw.githubusercontent.com*. https://raw.githubusercontent.com/canaryGrapher/slcmAPI/master/routes/getattendance.js
19. *raw.githubusercontent.com*. https://raw.githubusercontent.com/canaryGrapher/slcmAPI/master/routes/getprofile.js
20. *Slcm Api*. https://raw.githubusercontent.com/nikeplusdash/SLCM-api/master/SLCM.py
21. *Pay Fee Online - Manipal University Jaipur *. https://jaipur.manipal.edu/pay-fee-online.php
22. *MTTN App*. https://app.manipalthetalk.org/
23. *Privacy Policy*. https://campus-adda.com/privacy-policy.html
24. *Mujstella - Apps on Google Play*. https://play.google.com/store/apps/details?hl=en_US&id=com.yourcompany.mujstellaapp
25. *MAHE DUBAI-SLCM - Apps on Google Play*. https://play.google.com/store/apps/details?hl=en_US&id=com.unikul.manipaldubai
26. *Manipal The Talk Network – Apps on Google Play*. https://play.google.com/store/apps/details?id=com.mttn.android&hl=en_IN
27. *CampusAdda - Apps on Google Play*. https://play.google.com/store/apps/details?id=com.app.campusadda&hl=en_US
28. *MUJStella - Student Platform for Manipal University Jaipur*. https://mujstella.in/mujslcm
29. *‎MAHE DUBAI - SLCM App - App Store*. https://apps.apple.com/us/app/mahe-dubai-slcm/id1627570076
30. *‎Brightspace Pulse App - App Store*. https://apps.apple.com/in/app/brightspace-pulse/id1001688546
31. *MUJStella - Student Platform for Manipal University Jaipur*. https://mujstella.in/.well-known/assetlinks.json
32. *MUJStella - Student Platform for Manipal University Jaipur*. https://mujstella.in/.well-known/apple-app-site-association
33. *.Well Known*. https://campus-adda.com/.well-known/assetlinks.json
34. *Apple App Site Association*. https://campus-adda.com/.well-known/apple-app-site-association
35. *r/manipaljaipur on Reddit: ANY ONE FACING ISSUE WITH SLCM PORTAL?*. https://www.reddit.com/r/manipaljaipur/comments/1m2bgru/any_one_facing_issue_with_slcm_portal/
36. *r/manipaljaipur on Reddit: Slcm portal issue*. https://www.reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue/
