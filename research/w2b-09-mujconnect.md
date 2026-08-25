# MUJ Connect OSINT Assessment: Identity, Data Flows, and SLCM Separation

## Executive Summary

- **Live Product Identity**: `mujconnect.in` presents itself as "MUJ's Own Social Place" and describes itself as "MUJ Connect - Your campus companion." Its visible product is a social/community service with anonymous posting, confession/reporting, and an AI food chatbot, not an obviously institutional student-record portal [3] [3] [17]. -> Treat it as a separate community application unless an operator or technical integration is independently confirmed.
- **Builder Attribution**: The public site does not name a person, student club, company, university department, or legal entity as its builder. The footer says only "2024 MUJ Connect" and the page branding says "MUJ's Own Social Place" [3] [3]. -> Do not attribute the live site to Naman Khator, MUJ, SDC, BuildIt, or any GitHub account on name similarity alone.
- **Native App Status**: The only clearly identified historical app named MUJ Connect is Android package `naman.com.muj`, attributed to Naman Khator. It was version 1.0, last updated April 18, 2015, had 1,000+ listed downloads and an approximately 4.45/5 rating, and is no longer available on Google Play [6]. -> This is a separate historical artifact unless future evidence links it to the current domain.
- **Current Delivery Model**: The current domain exposes a web application manifest naming the app, describing it as a Manipal University Jaipur campus companion, setting `display` to `standalone`, and declaring portrait orientation [17]. The HTML also references a Vite-style JavaScript asset and service-worker registration [18]. -> The strongest public evidence supports a PWA/web application, not a currently verified Google Play or Apple App Store application.
- **Authentication**: The registration page visibly asks for Full Name, Username, Email, avatar selection or upload, and an unnamed "Or continue with" option [2]. The login page accepts Email or Username and offers "Forgot your password?" plus an unnamed continuation option [1]. -> Google, phone-number login, Microsoft 365, and institutional SSO are not confirmed by the captured public UI.
- **Data Categories**: The site visibly or directly implies account identity data, profile/avatar data, authentication and recovery data, user-generated social content, anonymous/confession content, reports, and possibly chatbot interactions [2] [3]. -> These are product-level categories, not proof of database schema, retention period, moderation logs, IP logging, or third-party sharing.
- **API Evidence**: Passive public searches, repository review, and attempted text extraction did not produce a domain-linked API base URL or endpoint list. The served JavaScript asset is application/javascript and was not readable through the available text extraction path; a source-map lookup likewise returned the application shell rather than source code [14] [19]. -> The API inventory is **unknown**, not empty. No endpoint probing or unauthorized access should be performed.
- **SLCM Relationship**: The public SLCM landing page says "WELCOME TO MUJ PORTAL" and exposes institutional sign-in, `@muj.manipal.edu`, parent login, and student login [15]. Its public DNS answer was `98.70.14.50` [20], while `mujconnect.in` resolved to `98.84.224.111` and `18.208.88.157` [21]. -> Public evidence does not demonstrate that MUJ Connect shares SLCM authentication, APIs, hosting, or databases.
- **Public Reviews**: The old Android listing contains positive and mixed reviews, including praise for college-related access and criticism of UI/UX [6]. Those reviews apply to the 2015 package, not demonstrably to the current PWA. -> Avoid using historical ratings as a current quality or security signal.
- **Confidence**: High confidence for the visible product description, PWA metadata, current login/registration labels, historical Android metadata, and the absence of a domain-linked API in the material reviewed. Low confidence for builder identity, backend technology, exact API inventory, Google or phone authentication, privacy practices, and any SLCM integration.

## Scope, Ethics, and Method

This report is a public-information assessment of the MUJ Connect ecosystem. It uses publicly indexed pages, public application metadata, public GitHub repository pages, public social-media previews, public DNS answers, certificate-transparency results, and the public SLCM landing page. It does not use credentials, attempt account creation, submit login forms, enumerate protected resources, bypass controls, download or reverse-engineer private applications, or test for vulnerabilities.

The requested "chain-of-thought" is not reproduced. Instead, this report gives an auditable research summary: identify the live domain, separate it from same-name historical and student projects, read only public UI and metadata, compare public infrastructure clues, and mark every unresolved point as unknown. That approach matters here because "MUJ Connect" is a collision-prone name. At least one old Android product, several GitHub projects, an Instagram account, and other MUJ student platforms use similar names. A name match is not an operational attribution.

The supplied research brief describes the SLCM environment as ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10 behind Akamai, and Microsoft 365 identity. Those characteristics were treated as investigation hypotheses and scope supplied by the requester, not as independently established facts in this report. The public SLCM page itself establishes only the visible portal labels cited below. This distinction prevents an unverified banner or technology fingerprint from being presented as proof of a shared system.

## 1. What the Live Domain Publicly Says

The landing page uses the phrase "M U J's Own Social Place" and calls the experience social networking [3]. Its feature copy says "Secure & Private," supports anonymous posting, and invites users to "Confess or report" [3]. It also advertises a lightning-fast experience and an "AI-Powered" chatbot for food-related needs [3]. The page further markets "100% Anonymous," "AI Enabled," "99.9% Uptime," and "24/7 Support" [3]. These are statements made by the product page. They should be recorded as marketing claims, not independently verified security, availability, anonymity, or artificial-intelligence guarantees.

The page's product positioning is important. It differs materially from the public SLCM landing page, which is a portal with institutional, parent, and student sign-in choices [15]. The available MUJ Connect copy emphasizes community expression, social interaction, anonymous content, and food discovery. Nothing in the captured landing-page text says that it is an official SLCM module, that it is operated by Manipal University Jaipur, or that it reads attendance, timetable, grades, fees, or other student lifecycle records.

The current domain's footer says " 2024 MUJ Connect. All rights reserved" [3]. That is a copyright notice, not a legal-entity disclosure. No company name, university department, named developer, support address, privacy officer, terms page, or data-protection contact was visible in the captured public material. The absence of such an attribution does not prove that no operator exists; it means that the operator is not identified by the evidence reviewed.

### Table 1: Live-site observations

| Observation | Public evidence | Security or OSINT interpretation | Confidence |
|---|---|---|---|
| Product label | "M U J's Own Social Place" [3] | Brand positioning only; not proof of university ownership | High |
| Product description | Social networking and campus companion language [3] [17] | Community-oriented web product | High |
| Anonymous content | Anonymous posting and confession/reporting [3] | User-generated content is a central feature | High |
| AI feature | Foodie chatbot claim [3] | Possible chatbot interaction data; implementation unknown | Medium for feature, low for data handling |
| Copyright | " 2024 MUJ Connect" [3] | Date and brand notice; no named operator | High |
| Privacy/legal disclosure | No policy was found in captured public pages or search results | Privacy posture cannot be assessed from public evidence | Medium |

**Decision insight:** Security-club analysis should model MUJ Connect as an independently attributed, community-facing web service until the operator publishes a verifiable ownership or integration statement.

## 2. Who Built It? Attribution Results and False Matches

The strongest answer is: **the builder of the live `mujconnect.in` service is not publicly identified in the evidence reviewed**. The public landing, login, registration, manifest, and indexed searches identify the brand but not an individual or organization [3] [2] [17]. The domain footer does not name a developer [3]. Passive WHOIS extraction was blocked by a security-check page and exposed no usable registrant attribution [22]. Therefore, there is no responsible basis for naming a builder.

A particularly tempting false match is Naman Khator. AppBrain attributes a historical Android application named MUJ Connect to Naman Khator and gives its package as `naman.com.muj` [6]. Naman Khator's public GitHub profile also lists a `MUJ-Connect` repository described as "Our own project for Manipal!" [11] and the repository page says it was created on November 14, 2015 [10]. This is meaningful evidence that Naman Khator was associated with a MUJ project in the 2015 period. It is not evidence that he built the current `mujconnect.in` service, whose visible footer is dated 2024 and whose current UI is a different social/community product.

Other same-name repositories are also non-conclusive. The `MUJ-Connect/muj-connect` repository was created in 2021, has a Node/npm-style file layout including `package.json`, `package-lock.json`, and `server.js`, and has no visible domain or API linkage in the reviewed material [13]. The `anubhavbagri/MUJConnect-frontend` search result describes a project for connecting and chatting with random MUJ users [4]. The `VisheshVarshney/MUJConnect` result describes an anonymous student social space [7]. These projects are thematically similar to the live site, but none of the available evidence says that `mujconnect.in` deploys their code.

The Instagram account `@muj_connect` is another false-attribution risk. Its public profile is named MANIPAL FRESHERS, describes MUJ community and confession content, and showed 4,307 followers, 4,417 following, and 121 posts in the captured profile result [12]. Public post previews show MUJ/confession hashtags and dates in 2025 [9] [8]. That is evidence of an MUJ-related social account, not proof that it owns, operates, or built the domain. The live site's public material does not link to that account.

### Table 2: Attribution candidates

| Candidate | What is publicly supported | Link to `mujconnect.in` | Assessment |
|---|---|---|---|
| Naman Khator | Historical Android developer; 2015 MUJ-Connect GitHub association [6] [10] | None found | Separate historical candidate; do not attribute current site |
| `MUJ-Connect/muj-connect` | 2021 public Node/npm-style repository [13] | None found | Same-name candidate only |
| `anubhavbagri/MUJConnect-frontend` | MUJ chat project [4] | None found | Same-name candidate only |
| `VisheshVarshney/MUJConnect` | Anonymous student social-space project [7] | None found | Same-name candidate only |
| `@muj_connect` Instagram | MUJ Freshers confession/social account [12] | None found | Thematic similarity only |
| MUJ institution or SDC | MUJ has public institutional and student-development web presence [23] [24] | No official attribution found | Unproven |

**Decision insight:** The correct attribution statement for a security report is "operator/builder not publicly disclosed," with the historical Naman Khator app recorded as a separate, non-linked artifact.

## 3. App Store and Installable-App Findings

The current domain exposes a web app manifest. It names the application "MUJ Connect," repeats the description "Manipal University Jaipur Connect - Your campus companion," sets the start URL to `/`, uses standalone display mode, declares portrait orientation, and points to MUJ Connect icons [17]. The public HTML references `/manifest.json`, `/manifest.webmanifest`, a module JavaScript asset, CSS, and a service-worker registration script [18]. These are consistent with an installable PWA. They do not establish that a native Android or iOS package exists.

The historical Android listing is much more concrete. AppBrain identifies the application as MUJ Connect, package `naman.com.muj`, developer Naman Khator, version 1.0, rating 4.45, 102 reviews in the listing view, and 1,000+ downloads [6]. The same source says the app was last updated April 18, 2015 and is currently unavailable on Google Play [6] [6]. Its description concerned Outlook mail, AMS updates, My Campus Days complaints, and contacts for restaurants and cabs [6] [6]. The old app is therefore an academic-access utility, while the current domain visibly emphasizes anonymous social content and a food chatbot. The product and time gap make conflation especially unsafe.

Searches also surfaced other MUJ-branded applications, including MUJstella and CampusAdda. MUJstella's Google Play page identifies a student companion with timetable, attendance, study resources, campus directory, updates, and a January 21, 2026 update [25]. It shows a 4.3 rating and 20 reviews in the captured view, declares no data shared and no data collected, and identifies Akshit Raj as developer [25]. These facts belong to MUJstella, not MUJ Connect. CampusAdda similarly appeared as a separate MUJ-branded listing, including an Apple App Store result [26] [27].

### Table 3: App and distribution inventory

| Product or artifact | Store/package evidence | Date or scale | Relation to `mujconnect.in` |
|---|---|---|---|
| Current MUJ Connect | PWA manifest; standalone, portrait, start URL `/` [17] | Manifest observed August 25, 2026 in raw capture | Strongly linked to live domain |
| Historical MUJ Connect | Android package `naman.com.muj`; Naman Khator [6] | Version 1.0; last update April 18, 2015 [6] [6] | No domain link; treat as separate |
| Historical Android availability | AppBrain says no longer on Google Play [6] | 1,000+ downloads; old listing [6] | Not current distribution evidence |
| MUJstella | Google Play package `com.yourcompany.mujstellaapp`; developer Akshit Raj [25] | Updated Jan. 21, 2026; 1K+ downloads [25] [25] | Separate student-built platform |
| CampusAdda | Google Play and Apple App Store results [26] [27] | Listing details vary by platform | Separate MUJ-branded app |
| Verified current native MUJ Connect listing | None located in searches | Not established | Unknown, not proof of nonexistence |

**Decision insight:** For mobile threat modeling, start with the current PWA origin and its browser storage/service-worker behavior as a web application. Do not use the 2015 APK metadata to infer current endpoints or controls.

## 4. Login Method and Identity Boundary

The public registration page shows Full Name, Username, and Email fields [2]. It also says that users may choose a default avatar or upload their own [2]. A continuation control is present, but the visible text only says "Or continue with" and does not name a provider [2]. No college-credential requirement is shown on the captured registration page, and no phone-number field is visible [2].

The public login page shows "Email or Username" [1], a "Forgot your password?" recovery affordance [1], and another unnamed "Or continue with" control [1]. The captured page text does not identify Google, Microsoft, phone, SMS OTP, Microsoft 365, or a university SSO provider [1]. The most defensible conclusion is that local account login and recovery are visibly supported, while the social provider and any backend federation are unknown.

The SLCM landing page is different. It publicly presents "WELCOME TO MUJ PORTAL," institutional sign-in language, `@muj.manipal.edu`, parent login, and student login [15]. That establishes a visible institutional portal boundary. It does not establish that MUJ Connect delegates to the same identity provider. A shared university email suffix could be used by an independent application without shared tokens, directories, or Microsoft 365 integration. Conversely, a hidden OAuth flow could exist behind the unnamed control. Public UI alone cannot decide between these possibilities.

### Table 4: Authentication evidence matrix

| Question | Observed public evidence | Conclusion |
|---|---|---|
| Email login? | Login accepts "Email or Username" [1] | Confirmed at UI-label level |
| Username login? | Same label [1] | Confirmed at UI-label level |
| Password recovery? | "Forgot your password?" [1] | Recovery affordance confirmed; workflow unknown |
| Phone login or OTP? | No phone field or phone wording visible [2] [1] | Not confirmed |
| Google login? | Only unnamed "Or continue with" is visible [2] [1] | Not confirmed |
| Microsoft 365/SSO? | Not named on MUJ Connect pages; SLCM separately names `@muj.manipal.edu` [15] | Not confirmed for MUJ Connect |
| College credential verification? | Not shown on current captured pages | Not confirmed |
| Anonymous posting | Landing page claims support [3] | Product feature claim; account-to-content unlinkability unknown |

**Decision insight:** The security question is not "does it use Google?" but "what exact provider is behind the unnamed social-login control, and what account identifiers are retained?" That answer is not public in the reviewed material.

## 5. Data the Product Appears to Hold

The visible registration controls support a minimum account data model containing a full name, username, email address, and avatar selection or uploaded avatar [2]. The login and recovery controls imply credentials or an external identity mapping and a recovery process [1]. The exact password representation, reset-token lifetime, email-verification state, session-cookie names, and multifactor options are not publicly documented.

The feature copy indicates user-generated content and moderation-related actions. Anonymous posting and confession/reporting imply posts or confessions, publication state, and reports or moderation decisions [3]. The phrase "100% Anonymous" is a marketing claim [3], not proof that operators cannot associate content with accounts, IP addresses, timestamps, device identifiers, or moderation records. Anonymity can mean only that a username is not displayed publicly.

The food chatbot claim suggests a possible category of chat prompts, responses, and conversation metadata [3]. It does not show whether the chatbot is first-party, whether prompts leave the domain, or whether an external AI provider receives them. A responsible report should state the possibility without naming a provider.

No privacy policy was located in the reviewed public search results. Searches instead surfaced generic Google or unrelated Manipal Hospitals policies, neither of which can be used as MUJ Connect's policy [28] [29]. The current site pages captured no clear retention, deletion, sharing, legal basis, age, moderation, breach-notification, or data-subject-rights statements. Consequently, retention and third-party sharing are unknown.

### Table 5: Data inventory with evidence strength

| Data category | Why it is indicated | What remains unknown |
|---|---|---|
| Full name | Registration field [2] | Whether required, verified, visible, or editable |
| Username | Registration and login labels [2] [1] | Uniqueness, public exposure, history, deletion |
| Email | Registration field and email-or-username login [2] [1] | Verification, provider, sharing, retention |
| Avatar/profile image | Default avatar or upload option [2] | Image storage, EXIF handling, moderation, CDN |
| Credentials/recovery data | Password-recovery affordance [1] | Hashing, reset tokens, MFA, rate limits |
| Posts/confessions | Anonymous posting and confession copy [3] | Linkability, moderation logs, deletion, indexing |
| Reports | "Confess or report" wording [3] | Reporter identity, evidence retention, workflow |
| Chatbot prompts | Foodie chatbot claim [3] | Provider, prompt retention, human access |
| Technical telemetry | Common possibility for web apps, but not evidenced here | IP, logs, cookies, analytics, device data unknown |

**Decision insight:** The most material privacy uncertainty is the gap between a public anonymity promise and the unknown operator-side metadata that may still connect content to accounts or sessions.

## 6. API and Code OSINT

The live HTML references a JavaScript module at `/assets/index-C0ndPmj2.js`, a CSS asset, a manifest, and a service-worker registration script [18]. That tells us the browser receives a compiled client application. It does not reveal the API. Direct extraction of the JavaScript asset returned no readable citation because the asset was served as `application/javascript`; a public text proxy reported that it could not interpret the content type [14]. A source-map request likewise returned the application shell rather than source-map content [19]. These are collection limitations, not proof that the code contains no routes.

Public repository searches found several projects with similar names, but no reviewed result visibly links a repository to `mujconnect.in` or exposes a domain-specific endpoint. The Node/npm-style `MUJ-Connect/muj-connect` repository lists `server.js`, but the available page evidence does not expose its route definitions, authentication, data schema, or deployment domain [13]. The student-social repositories similarly do not establish deployment identity [4] [7].

The correct API finding is therefore a negative OSINT result with a strict qualifier: **no exact API base URL or endpoint was recovered from public indexed material and readable page evidence available for this assessment**. This is different from saying the service has no API. A deployed single-page application almost certainly communicates with some server-side service for login, content, reports, profiles, or chatbot functions, but that is an inference from the product's visible behavior and not a citable endpoint discovery.

No endpoint list is included here because guessing paths such as `/api/login`, `/api/register`, or `/api/posts` would create unverified technical information and could encourage unauthorized testing. The safe research path is to request a public developer disclosure, inspect only officially published source code, or conduct a properly authorized review under written scope.

### Table 6: API evidence status

| Evidence source | Result | What can be stated safely |
|---|---|---|
| Live HTML | Public asset and manifest references [18] | Client-side application is delivered to browser |
| JavaScript asset extraction | No readable result; content-type limitation [14] | API routes not recovered; no inference about absence |
| Source-map path | Returned application shell [19] | Public source map not established |
| GitHub name searches | Same-name projects without domain linkage [4] [7] [13] | Candidate code must not be attributed to live site |
| Search-engine endpoint queries | No relevant domain-linked endpoint result | No public indexed endpoint found in this review |

**Decision insight:** API attribution is the highest-value unanswered technical question, but it must be answered through public disclosure or authorized testing, not speculative endpoint enumeration.

## 7. Passive Infrastructure and SLCM Relationship

Public DNS resolution for `mujconnect.in` returned two A records: `98.84.224.111` and `18.208.88.157`, with a 120-second TTL in the captured response [21]. This is a time-sensitive observation and should not be treated as permanent hosting identity. DNS addresses can belong to cloud infrastructure, load balancing, migration, or reverse proxies. The certificate-transparency result showed a Let's Encrypt certificate for `mujconnect.in` and a wildcard name, with a validity window beginning July 30, 2026 in the captured record [30]. That supports current HTTPS certificate issuance, not operator identity or application architecture.

The SLCM host resolved separately to `98.70.14.50` [20]. The public SLCM page exposes institutional login labels and the `@muj.manipal.edu` identity wording [15]. The different observed DNS answers are consistent with separate network placement, but they do not prove separate ownership, separate databases, or absence of a shared CDN. Similarly, the requester-supplied Akamai and IIS/.NET characterization was not treated as independently confirmed here. A reverse proxy can obscure origin details, and a page's visible markup cannot by itself establish the complete backend stack.

The public evidence supports a conservative architecture model: MUJ SLCM is an institutional portal on one host; MUJ Connect is a separately branded PWA on another domain; the two have no publicly documented integration in the reviewed pages. The model should remain provisional until an official integration document, shared OAuth metadata, or public source code establishes a connection.

### Table 7: Passive comparison

| Attribute | MUJ Connect | MUJ SLCM | Interpretation |
|---|---|---|---|
| Domain | `mujconnect.in` | `mujslcm.jaipur.manipal.edu` | Separate hostnames [17] [15] |
| Public product text | Social place, anonymous posts, chatbot [3] | MUJ Portal; institutional, parent, student sign-in [15] | Different visible roles |
| DNS A answer | `98.84.224.111`, `18.208.88.157` [21] | `98.70.14.50` [20] | Different observed answers; not ownership proof |
| Public identity | Brand only; builder not named | Manipal University branding in portal title/content [15] | Different attribution visibility |
| Shared authentication | Not publicly shown | `@muj.manipal.edu` wording visible [15] | No public proof of sharing |

**Decision insight:** Treat SLCM and MUJ Connect as separate trust zones in a threat model. Do not assume that a user who can access one can access the other, or that a compromise of one would automatically expose the other.

## 8. Public Reviews and User Sentiment

The only detailed public reviews found for an app actually named MUJ Connect are attached to the historical Android listing. Reviews praise it as a perfect MUJ app, call it helpful for college-related material, and say it contains almost everything an MUJ student requires [6] [6]. One reviewer says the concept is good but that UI/UX needs substantial work [6]. Another says it was helpful and found no bugs [6]. The listing's 4.45 rating and 100-102 review figures are historical aggregator metadata and are internally presented in slightly different contexts [6] [6].

These reviews should not be mapped onto the current PWA. The old listing described Outlook, AMS updates, My Campus Days complaints, restaurants, and cabs [6] [6], while the current site advertises social networking, anonymous posting, reporting, and an AI food chatbot [3]. The change in feature set is enough to treat them as separate products absent a direct migration or ownership statement.

The Instagram evidence is public but not equivalent to independent product reviews. The account profile shows MUJ Freshers confession/community positioning [12], and post previews show engagement counts and MUJ/confession hashtags [9] [8]. Nothing in those previews links the account to `mujconnect.in`, and social engagement cannot validate security, privacy, uptime, or identity controls.

**Decision insight:** Historical reviews are useful for understanding an older MUJ student utility, but there is no verified current review corpus for the `mujconnect.in` PWA in the evidence gathered.

## 9. Risks, Unknowns, and Safe Follow-up Questions

The principal risk is attribution uncertainty. Users may interpret MUJ branding as institutional endorsement, while the public pages do not identify a university unit or legal operator [3] [3]. A security club should record this as governance and trust-boundary uncertainty, not as evidence of maliciousness.

The second risk is anonymity ambiguity. The site advertises anonymous posting [3] and "100% Anonymous" [3], but the registration process collects identifiable account attributes including full name and email [2]. The public evidence does not explain whether anonymous means anonymous to other users, moderators, database administrators, infrastructure providers, or third-party services. Those are different threat models.

The third risk is undocumented data handling. No verified MUJ Connect privacy policy was found. Retention, deletion, content moderation, account suspension, third-party AI processing, analytics, and incident response are therefore unknown. Security conclusions should not be drawn from the marketing phrases "Secure & Private" or "99.9% Uptime" [3] [3].

The fourth risk is endpoint and identity-provider opacity. The compiled client is publicly referenced but not readable through the available extraction route [18] [14]. The social-login provider is unnamed [2] [1]. It is consequently impossible from current public evidence to determine whether the service uses Google OAuth, another provider, local credentials, phone verification, or a combination.

Safe follow-up questions for the operator are preferable to active discovery: Who is the legal or institutional operator? Is the service affiliated with MUJ? Which identity providers are supported? What fields are collected, retained, shared, and deleted? Does anonymous content remain linkable to accounts or technical logs? Is the chatbot operated by a third party? What is the public vulnerability-reporting contact? Are there official Android or iOS builds, and what are their package identifiers? These questions can be sent through a public support channel if one is published, without testing the application.

## Synthesis

Across four dimensions, the evidence points to separation rather than integration. **Product scope** differs: MUJ Connect advertises social interaction, anonymous posts, confession/reporting, and a food chatbot [3], while SLCM exposes institutional, parent, and student portal sign-in [15]. **Distribution** differs: MUJ Connect is clearly represented as a standalone-display PWA [17], whereas the only clearly identified MUJ Connect native package is a discontinued 2015 Android artifact [6]. **Identity** differs: MUJ Connect exposes an unnamed social continuation and email/username login [2] [1], while SLCM visibly uses `@muj.manipal.edu` wording [15]. **Infrastructure evidence** differs: the observed DNS answers are separate [21] [20], though DNS alone cannot prove organizational separation.

The main tension is between branding and attribution. "M U J's Own Social Place" sounds institutionally connected [3], but the public evidence does not name MUJ, a department, or an operator. The correct interpretation is not that the site is unofficial, nor that it is official. It is that official status is unverified. The same discipline applies to anonymity: the product promises anonymous posting while collecting full name, username, email, and avatar information during registration [3] [2]. The promise may concern public display rather than operator-side unlinkability, but that is an inference and must remain qualified.

The evidence base is strongest for user-visible behavior and weakest for backend implementation. Public pages establish labels and marketing claims. App aggregators establish historical metadata. GitHub and Instagram establish same-name or same-theme candidates. DNS and certificates establish transient public infrastructure signals. None establishes the live API, database, provider configuration, or legal operator. Therefore, an application-security research plan should prioritize documentation and authorized disclosure over guessing endpoints or correlating unrelated student projects.

## VERDICT

**Overall confidence: Moderate for the high-level separation assessment; high for page-level observations; low for builder, API, privacy, and identity-provider attribution.**

1. `mujconnect.in` is a current MUJ-branded, installable PWA with a social/community feature set. **High confidence.**
2. The live site's builder/operator is not publicly identified in the reviewed evidence. **High confidence.**
3. Naman Khator is associated with a separate historical 2015 Android MUJ Connect artifact, but current-site attribution is unsupported. **High confidence.**
4. The current public UI visibly supports email/username login, password recovery, profile fields, avatar handling, and an unnamed social-login continuation. **High confidence.**
5. Google login, phone login, Microsoft 365 identity, and shared SLCM SSO are not confirmed. **Moderate-to-high confidence as an OSINT non-finding; not proof of absence.**
6. The product likely stores account and user-generated-content categories indicated by its UI, but retention, sharing, technical logs, and anonymity guarantees are unknown. **Moderate confidence for indicated categories; low confidence for handling.**
7. No domain-linked API endpoint inventory was recovered. **High confidence as a research limitation; low confidence if interpreted as proof that no API exists.**
8. Public evidence does not demonstrate technical integration with MUJ SLCM. **Moderate confidence.**

**Recommended club position:** classify MUJ Connect as an unattributed public-facing community PWA adjacent to, but not proven to be part of, the MUJ SLCM trust domain. Do not perform active endpoint discovery, credential testing, APK reverse engineering, or account probing without written authorization. Record the API, operator, provider, privacy, and integration questions as open items.

## References

1. *MUJ Connect*. https://mujconnect.in/login
2. *MUJ Connect*. https://mujconnect.in/register
3. *MUJ Connect*. https://mujconnect.in/
4. *GitHub - anubhavbagri/MUJConnect-frontend: Connect and chat ...*. https://github.com/anubhavbagri/MUJConnect-frontend
5. *GitHub - SUHANIC123/muj-connect*. https://github.com/SUHANIC123/muj-connect
6. *MUJ Connect - Free APK Download for Android*. https://www.appbrain.com/app/muj-connect/naman.com.muj
7. *GitHub - VisheshVarshney/MUJConnect: A social media ...*. https://github.com/VisheshVarshney/MUJConnect
8. *Instagram*. https://www.instagram.com/p/DNupMJrwNCs/
9. *Instagram photo by MUJ CONNECT • Apr 15, 2025 at 11:02 AM*. https://www.instagram.com/p/DIef7XKh-kn/
10. *GitHub - princenaman/MUJ-Connect: Our own project for Manipal! · GitHub*. https://github.com/princenaman/MUJ-Connect
11. *princenaman (Naman Khator) · GitHub*. https://github.com/princenaman
12. *MANIPAL FRESHERS (@muj_connect) • Instagram photos and videos*. https://www.instagram.com/muj_connect/
13. *GitHub - MUJ-Connect/muj-connect · GitHub*. https://github.com/MUJ-Connect/muj-connect
14. *Index C0Ndpmj2*. https://r.jina.ai/http://mujconnect.in/assets/index-C0ndPmj2.js
15. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
16. *api.ssllabs.com*. http://api.ssllabs.com/api/v3/analyze?all=done&fromCache=on&host=mujslcm.jaipur.manipal.edu&maxAge=168
17. *mujconnect.in*. https://mujconnect.in/manifest.json
18. *MUJ Connect*. https://mujconnect.in/robots.txt
19. *MUJ Connect*. https://mujconnect.in/assets/index-C0ndPmj2.js.map
20. *dns.google*. https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=A
21. *dns.google*. https://dns.google/resolve?name=mujconnect.in&type=A
22. *Whois mujconnect.in*. https://www.whois.com/whois/mujconnect.in
23. *Manipal University Jaipur - 71 years of legacy of Manipal...*. https://www.jaipur.manipal.edu/
24. *SDC MUJ TEAM - Software Development Centre at Manipal ...*. https://in.linkedin.com/in/sdc-muj-team-419007326
25. *Mujstella - Apps on Google Play*. https://play.google.com/store/apps/details?id=com.yourcompany.mujstellaapp
26. *CampusAdda App - App Store*. http://apps.apple.com/us/app/campusadda/id6465745096
27. *CampusAdda - MUJ on the App Store*. https://apps.apple.com/in/app/campusadda-muj/id6465745096?platform=iphone
28. *Privacy Policy*. https://www.manipalhospitals.com/privacy-policy
29. *Privacy & Terms – Google*. https://policies.google.com/
30. *crt.sh*. https://crt.sh/?q=mujconnect.in&output=json
