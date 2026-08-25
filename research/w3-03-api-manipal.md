# MUJ SLCM API Exposure and Dependency Assessment

## Executive Summary

- **Verified API Stack**: Public DNS maps `api.manipal.edu` to `43.205.223.7`, while passive Shodan observations identify Amazon EC2 in `ap-south-1`, nginx 1.18.0 on Ubuntu, Node.js, and Express -> treat this stack as independently corroborated, but validate it through an authorized internal asset inventory before remediation work.[1][121.17][121.21][121.23][121.37][121.42][121.44][121.46]
- **Opaque Public Root**: The HTTPS root returns a JSON object containing a single opaque `data` string, and Shodan observed HTTP 200 with `Content-Type: application/json; charset=utf-8` -> document the purpose, data classification, and intended consumers of this response.[2][121.86]
- **Unproven SLCM Relationship**: No reviewed official source states that `api.manipal.edu` is the backend for MUJ SLCM, although both are in the broader Manipal namespace -> do not merge their threat models or identity assumptions without internal architecture evidence. This is a bounded negative finding, not proof that no relationship exists.[2][43.0][43.1]
- **No Confirmed Official Contract**: The reviewed indexed sources did not yield an official Swagger or OpenAPI document for `api.manipal.edu`; a GitHub `api.yaml` search result describes a physiotherapy project rather than SLCM -> establish an authoritative API catalog and publish documentation only to the intended audience.[3][55.11]
- **Unknown API Authentication**: Anonymous retrieval of the root proves only that `/` is publicly readable; it does not establish how undiscovered business routes authenticate -> require an internal route inventory, owner attestation, and gateway-policy review instead of attempting public path discovery.[2][121.86]
- **Separate Identity Boundaries**: Official MUJ material documents SLCM onboarding, Admissions-issued credentials, parent OTP verification, and Microsoft 365 setup with MFA; public evidence does not show that `api.manipal.edu` uses Microsoft identity -> model SLCM, parent access, Microsoft 365, and the API as separate trust boundaries until integration is proven.[4][75.20][75.24][75.82][76.4][76.5][76.9]
- **Community Wrappers Are Historical Clues**: Public student-built repositories describe older form-login and scraping workflows against `slcm.manipal.edu`, including marks, attendance, and profile data -> use them to identify legacy dependency and credential-handling risks, not as documentation for the current MUJ portal or `api.manipal.edu`.[5][98.1][98.11][98.13][99.2]
- **Payload Changed Over Time**: Wayback CDX records contain four distinct root-response digests between June 2024 and March 2025 -> maintain versioned contracts and change records because the public representation has changed, although the archive alone does not explain why.[6]
- **Broad API-Labeled Host Family**: Passive host-search data lists several API-named Manipal hosts for convocation, events, attendance-management, and time-tracking contexts, while its bounded Jaipur response contains no API-labeled hostname -> centralize ownership, certificate, DNS, and retirement tracking across the family.[7][141.0]
- **Overall Assessment**: The infrastructure facts are high confidence, but the functional relationship among the API, MUJ SLCM, mobile clients, and Microsoft 365 remains unproven -> prioritize governance and internal verification rather than external experimentation.[1][121.17][75.20]

## 1. Scope, Ethics, and Evidence Model

This report uses public information only: official MUJ pages and documents, passive DNS, public archive indexes, passive Internet-measurement records, and public GitHub repositories. It does not rely on credential use, endpoint guessing, automated directory discovery, authentication attempts, or submission of a new Internet scan. Names of historical third-party routes are included for dependency attribution, not as instructions to invoke them.

The user requested explicit chain-of-thought. Private chain-of-thought is not provided. In its place, the following reproducible evidence model states what was observed, what it supports, and where inference begins. Every inference in this report is labeled `Inference:`.

| Evidence class | Examples used | What it can establish | Important limitation |
|---|---|---|---|
| First-party official | MUJ portal and onboarding documents | Published portal URLs, login labels, onboarding process, Microsoft 365 and MFA instructions | Does not document the internals of `api.manipal.edu` unless it names that host.[8][43.2][75.20][76.4][76.5] |
| Direct public representation | HTTPS root of `api.manipal.edu` | The root returned JSON containing an opaque `data` value at collection time | Does not reveal the meaning, consumers, cryptography, or other routes.[2] |
| Passive infrastructure observation | Google DNS, urlscan domain metadata, Shodan | IP address, reverse DNS, AWS attribution, observed server and framework headers | A passive observation can age, and fingerprinting can be incomplete or deliberately altered.[1][103.11][103.14][121.42][121.48] |
| Public archive index | Wayback CDX | Capture dates, MIME type, status, digest, and record length | Different digests show different archived representations, not semantic API versions.[6] |
| Public source code | GitHub repositories and raw files | What third-party authors documented or implemented historically | It is not proof of university authorization, current operation, or applicability to MUJ.[9][116.0][128.0] |
| Bounded negative search | No official specification or mobile dependency located | No confirming artifact was found in the reviewed corpus | It cannot prove universal absence and should not be converted into a categorical claim.[3][102.0] |

Confidence labels are applied per issue. `High` means multiple direct or authoritative sources converge. `Moderate` means evidence is direct but limited in time, scope, or provenance. `Low` means only indirect community evidence exists. `Unresolved` means the reviewed public record is insufficient.

A critical scoping distinction is required. `mujslcm.jaipur.manipal.edu`, `muj.slcm.jaipur.manipal.edu`, `slcm.manipal.edu`, and `api.manipal.edu` are different hosts. The official MUJ pages expose different sign-in labels: one shows `@muj.manipal.edu` and a parent login, while another shows `@jaipur.manipal.edu`.[8][43.2][43.3][41.0][41.2] The older community code targets `slcm.manipal.edu`, not either MUJ hostname or `api.manipal.edu`.[5][98.1] Therefore, technology or authentication findings must not be transferred between them without evidence.

The user-supplied characterization of the MUJ portal as ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, and Akamai was not independently corroborated by the sources collected for this report. The community repositories do show older ASP.NET Web Forms artifacts such as `__VIEWSTATE`, `__EVENTVALIDATION`, `StudentProfile.aspx`, and `Academics.aspx`, but those artifacts concern the legacy `slcm.manipal.edu` workflow.[10][98.1][98.11][98.13] They do not validate the supplied MVC/IIS/Akamai fingerprint for the current MUJ portal.

## 2. Public Surface, Hosting, and Stack

The strongest independently verified finding is the infrastructure chain for `api.manipal.edu`. Google Public DNS returned an A record of `43.205.223.7` with a 300-second TTL.[1] The CNAME query did not return a CNAME answer; instead, it returned the `manipal.edu` authority information.[11][78.1] urlscan's domain page associates the address with AS16509, identifies the PTR as `ec2-43-205-223-7.ap-south-1.compute.amazonaws.com`, and places the address in Mumbai, India.[12][103.11][103.14][103.15]

Shodan provides more specific passive fingerprinting. Its host record lists the AWS EC2 hostname, `api.manipal.edu`, Amazon as cloud provider, `ap-south-1` as region, EC2 as service, AS16509, Ubuntu, Node.js, nginx 1.18.0, and Express.[13][121.21][121.23][121.25][121.35][121.37][121.42][121.44][121.46] The observation is time-bounded: Shodan labels the host last seen on August 23, 2026, with the HTTPS observation dated August 22, 2026.[13][121.74]

| Layer | Public observation | Confidence | Interpretation |
|---|---|---|---|
| DNS | `api.manipal.edu` -> `43.205.223.7` | High | Direct DNS evidence.[1] |
| Cloud network | AS16509, Amazon, EC2, `ap-south-1` | High | DNS, PTR, urlscan, and Shodan converge.[12][103.14][121.21][121.23][121.25] |
| Operating system | Ubuntu | Moderate | Passive fingerprinting, not an authenticated host inventory.[13][121.40] |
| Reverse proxy | nginx 1.18.0 | High for the observed date | Version appeared in the HTTP banner and technology classification.[13][121.65][121.67] |
| Application runtime | Node.js | Moderate | Shodan technology classification.[13] |
| Web framework | Express | High for the observed response | Shodan classified Express and recorded `X-Powered-By: Express`.[13][121.86] |
| HTTPS content | HTTP 200, JSON, 199-byte observed body | High for the observed date | Direct passive response metadata.[13] |
| TLS identity | Certificate subject and SAN `api.manipal.edu` | High for the observed certificate | Shodan recorded a Let's Encrypt certificate valid from July 14 to October 12, 2026.[13][121.89] |

Port 80 was observed returning `301 Moved Permanently` to `https://api.manipal.edu/`, while HTTPS returned `200 OK` with JSON.[13][121.86] The HTTPS headers included `Access-Control-Allow-Origin: *` and `X-Powered-By: Express`.[13] A wildcard CORS header is not, by itself, a vulnerability. Whether it creates risk depends on the sensitivity of responses, credential mode, and authorization enforcement.

`Inference:` The direct A record, EC2 reverse name, and matching Shodan service record make it likely that the public API is served directly from an EC2 instance or an EC2-hosted reverse-proxy tier. This inference does not prove whether additional private load balancers, WAFs, or service tiers exist behind nginx.[1][103.14][121.17]

The root response is an object with one `data` member whose value is an opaque string.[2] The string should not be labeled encrypted, signed, compressed, or Base64 merely from appearance. The public evidence does not disclose its algorithm, schema, freshness, or sensitivity. `Inference:` Such opacity may represent application-level encoding or an intentionally non-self-describing contract, but internal source code or documentation is required to determine its purpose.

The user-supplied claim that the MUJ portal sits behind Akamai must not be transferred to `api.manipal.edu`. The API evidence instead points to a direct AWS address and nginx/Express. This is a topology distinction, not proof that Akamai is absent from every MUJ service.[1][121.17][121.44][121.46]

## 3. Endpoints, OpenAPI, and Authentication

Only one official-host path is directly documented by the reviewed public evidence: the root `/` of `https://api.manipal.edu/`. It returned JSON without a visible login challenge.[2] The HTTP service redirected the same root to HTTPS.[13] No additional business endpoint on this host is asserted here because no official contract or indexed first-party documentation was located, and this research did not guess paths.

| Host or project | Publicly documented path or category | Status in this report | Security interpretation |
|---|---|---|---|
| `api.manipal.edu` | `/` | Confirmed public root | Anonymous readability applies only to this representation.[2][121.86] |
| `api.manipal.edu` | HTTP root -> HTTPS root | Confirmed redirect | Supports transport upgrade for the root.[13] |
| nikeplusdash historical deployment | `/login`, `/docs` | Third-party wrapper only | README says login established access to other wrapper routes and warns users to end sessions.[5][96.6][96.7][96.8] |
| canaryGrapher wrapper | `/getscores`, `/getattendance`, `/getprofile`, `/validateuser` | Third-party implementation only | These Express routes describe a scraper API, not the official API host.[14][132.4][132.5][132.6] |
| Legacy MAHE SLCM upstream | `StudentProfile.aspx`, `Academics.aspx` | Historical portal pages | Community code used authenticated sessions to retrieve profile, attendance, and marks.[15][98.13][98.14] |
| ManipalTheTalk backend | Marks, attendance, timetable | Category-level documentation only | README says a server called a separate scraper; no relationship to `api.manipal.edu` is documented.[16][100.3][100.4] |

The canaryGrapher project provides the clearest third-party route inventory. Its repository contains route files for attendance, marks, profile, and user validation.[17] Its `package.json` identifies version 1.4.2 and dependencies including Express 4.17.1, Axios, body-parser, nodemon, and Puppeteer.[18] Its server registers the four named paths with Express.[14][132.2][132.3][132.6] These facts show how a community wrapper modeled SLCM data. They do not establish routes on `api.manipal.edu`.

Swagger/OpenAPI status is `not publicly confirmed`. A discovered GitHub file named `api.yaml` declares Swagger 2.0, but its title is `Node Js API Project for physiotherapy`, and the visible tags concern user-related endpoints.[3][55.10][55.11] It makes no visible claim to be the contract for `api.manipal.edu` or SLCM. Treating that file as an official API specification would be a false-positive attribution.

The defensible statement is therefore: no official Swagger/OpenAPI artifact for `api.manipal.edu` was found in the reviewed indexed sources. It would be incorrect to state that no specification exists internally or at an unindexed location. It would also be inappropriate to try conventional documentation paths without authorization merely to convert a negative search into a stronger claim.

Authentication must be separated into four layers:

| Boundary | Public evidence | Finding |
|---|---|---|
| API root | Root returns HTTP 200 JSON | Public root; broader API auth unresolved.[2][121.86] |
| Legacy `slcm.manipal.edu` | Community clients used form fields, server-generated state, CAPTCHA, and a persistent HTTP session | Historical form/session model, not confirmed current MUJ or API behavior.[10][98.1][98.8] |
| MUJ SLCM | Admissions sends SLCM credentials to the student's recorded personal Gmail account; parent mobile OTP enables parent login | Official onboarding workflow, but not a full protocol specification.[4][75.24][75.82] |
| Microsoft 365 | Official MUJ SOP directs users to `login.microsoftonline.com`, requires a password change, and describes MFA setup | Confirms a Microsoft 365 identity process; does not prove API federation.[19][76.5][76.8][76.9][76.14] |

`Inference:` Because the API root is public while SLCM and Microsoft 365 have explicit sign-in workflows, the safest architecture assumption is that they are separate trust zones until internal diagrams prove otherwise. The public record does not support claims that the opaque JSON is protected by Microsoft Entra ID, that it contains SLCM data, or that it is consumed by an official mobile application.

## 4. Mobile Dependencies and GitHub Case Studies

No official App Store, Play Store, package manifest, or first-party source repository was found that explicitly names `api.manipal.edu` as a mobile backend. This is an unresolved dependency question, not evidence that no mobile dependency exists. The public GitHub material instead documents community-built intermediaries aimed at the older `slcm.manipal.edu` portal.

| Project | Public purpose | Technology and dates | API-host relevance |
|---|---|---|---|
| `nikeplusdash/SLCM-api` | API for `slcm.manipal.edu` that logs in and fetches basic user data | Python is the repository's primary language; created May 31, 2020; pushed December 8, 2022; archived | No documented `api.manipal.edu` dependency.[9][96.1] |
| `canaryGrapher/slcmAPI` | Open-source REST API for Manipal SLCM marks, attendance, and profile data | JavaScript; created May 22, 2020; pushed February 29, 2024; archived | Community scraper, not official API documentation.[20][116.1][99.2] |
| `manipalthetalk/App-Backend` | Scrapes SLCM for marks, attendance, timetable, and related data | Python 2.7 and Go documented; created December 2, 2017; last pushed January 27, 2018 | App-oriented backend clue, but no documented link to `api.manipal.edu`.[16][100.5][128.0] |
| Vedic Technologies `manipal-server/api.yaml` | Swagger 2.0 physiotherapy project | 1,135-line YAML in a separate repository | False positive for SLCM/API attribution.[3][55.4][55.6][55.8] |

### Case Study 1: nikeplusdash/SLCM-api

The README states that the wrapper sent a login request to `https://slcm.manipal.edu`, fetched basic user data, claimed not to store user data, and was deployed historically on Heroku with documentation under `/docs`.[5][96.3][96.4][96.8] It also says users should use `/login` before other routes and should log out their session.[5][96.7] The repository tree includes separate `SLCMv1` and `SLCMv2` directories alongside JavaScript and Python implementations.[21]

The Python implementation shows the older auth mechanics more clearly: it used a `requests.Session`, retrieved server-generated ASP.NET fields, handled a CAPTCHA, submitted form credentials, and then requested profile and academics pages.[15][98.1][98.8][98.11][98.13] The code labels resulting categories as basic details, attendance, and marks.[15][98.12][98.14]

Security significance: the repository demonstrates historical demand for programmatic access and illustrates why users might give credentials to unofficial intermediaries. It should not be treated as proof of a current flaw. The repository's README says no user data was stored, but that is an author claim, not an independently audited privacy guarantee.[5]

### Case Study 2: canaryGrapher/slcmAPI

The README calls the project an open-source REST API intended to spare app or website developers from writing their own SLCM scrapers.[22][99.3][99.4] Its version history records 1.0.x for theory marks, 1.1.x for attendance, 1.2.x for admission-profile details, 1.3.x for credential validation, and 1.4.x for request-response exception handling.[22][99.6][99.7][99.8][99.9][99.10] The same README marks the project deprecated after CAPTCHA was introduced.[22]

Security significance: CAPTCHA disrupted automation but did not create a documented official API. `Inference:` The sequence from marks to attendance to profile and credential validation shows progressive expansion of sensitive-data scope in community tooling. That history argues for an official client strategy, clear acceptable-use terms, and user education against entering university credentials into unapproved services.

### Case Study 3: ManipalTheTalk App-Backend

The README says the scraper and server were independent and that the system extracted marks, attendance, and timetable data.[16][100.3][100.4] This is the best public clue of an app-oriented dependency, but it is an old community project and does not name `api.manipal.edu`. `Inference:` It demonstrates historical mobile or app demand for SLCM-derived data, not a current production dependency.

The resulting mobile verdict is `unconfirmed`. Internally, defenders should obtain mobile build manifests, domain allowlists, certificate-pinning configuration, analytics inventories, and API gateway logs. Those authorized internal artifacts can answer the dependency question without public probing.

## 5. Historical Versions and Related API Hosts

The archive record supports change over time but not semantic version numbering. Wayback CDX lists four successful JSON captures of the API root with distinct digests: June 21, 2024; December 27, 2024; and two captures one second apart on March 19, 2025. Their archived record lengths are 607, 717, 720, and 718 bytes.[6] Distinct digests establish that the archived representations differed. They do not show which fields changed or whether each difference was a planned release, rotating value, timestamp, encryption nonce, or operational artifact.

| Date | Public event | What it establishes |
|---|---|---|
| 2017-12-02 | ManipalTheTalk App-Backend created | Community app/backend interest in SLCM existed by 2017.[23] |
| 2018-01-27 | App-Backend last pushed | The visible implementation is historical rather than recent.[23] |
| 2020-05-22 | canaryGrapher/slcmAPI created | A community REST wrapper existed by May 2020.[20] |
| 2020-05-31 | nikeplusdash/SLCM-api created | A second community wrapper appeared nine days later.[9] |
| 2022-04-05 | urlscan domain page says `api.manipal.edu` was observed through CT | Public certificate evidence for the hostname existed by that date.[12][103.26][103.27] |
| 2024-06-21 | First returned Wayback 200/JSON digest | Public archival evidence of the root response.[6] |
| 2024-12-27 | Second distinct digest | Archived representation changed.[6] |
| 2025-03-19 | Two additional distinct digests | The root could vary even across adjacent captures.[6] |
| 2026-08-22 to 2026-08-23 | Shodan HTTPS and HTTP observations | Recent passive evidence of JSON/Express on HTTPS and nginx redirect on HTTP.[13][121.74][121.86] |

The related-host inventory comes from HackerTarget's passive host-search output and must be treated as discovery evidence, not an authoritative CMDB. The response directly lists the following names and addresses.[7]

| API-labeled hostname | Listed address | Name-based likely context | Status |
|---|---:|---|---|
| `ams-api.manipal.edu` | `18.60.15.4` | `Inference:` Attendance-management or similarly named service | Passive listing only.[7] |
| `api.manipal.edu` | `43.205.223.7` | General API host | Independently DNS-confirmed.[7][77.0] |
| `api-convocation.manipal.edu` | `13.234.80.43` | `Inference:` Convocation service | Passive listing only.[7] |
| `api-invictus.manipal.edu` | `35.154.131.148` | `Inference:` Named event or application | Passive listing only.[7] |
| `api-mangaloreconvocation.manipal.edu` | `65.0.191.62` | `Inference:` Mangalore convocation service | Passive listing only.[7] |
| `api-mlrconv.manipal.edu` | `13.127.223.171` | `Inference:` Abbreviated convocation service | Passive listing only.[7] |
| `api-summer.manipal.edu` | `65.1.193.164` | `Inference:` Summer-program service | Passive listing only.[7] |
| `api-techtatva.manipal.edu` | `13.234.173.30` | `Inference:` TechTatva event service | Passive listing only.[7] |
| `api-timetracker.manipal.edu` | `43.204.223.55` | `Inference:` Time-tracking service | Passive listing only.[7] |

The bounded `jaipur.manipal.edu` host-search response lists SLCM, ERP, identity-provider, admissions, DMS, and other names, but no hostname whose leftmost label is `api`.[24] This means only that no such name appeared in that response. It does not prove that MUJ has no API hosts, because passive datasets have collection and freshness limits.

`Inference:` The number and naming diversity of API-labeled hosts indicates decentralized application ownership or event-specific deployment patterns across the Manipal family. The inference should be tested internally against DNS administration records, cloud accounts, certificate inventories, data owners, and decommissioning tickets.

## 6. Defensive Priorities

The evidence supports governance and exposure-reduction work, not an assumption of compromise. Recommendations below are for authorized university owners and avoid external testing instructions.

| Priority | Owner | Defensive action | Evidence driver | Success measure |
|---|---|---|---|---|
| P0 | Central IT and API owner | Assign a named business owner, technical owner, data classification, and lifecycle state to `api.manipal.edu` | Public root and direct AWS exposure.[2][77.0] | CMDB record approved and reviewed quarterly |
| P0 | API engineering | Produce an internal route and method inventory, including auth policy and data schema; compare deployed routes with source and gateway configuration | Only the root is publicly documented; broader auth is unresolved.[2][121.86] | Every deployed route mapped to owner, auth, and data class |
| P0 | Identity and SLCM teams | Document whether SLCM, parent login, Microsoft 365, and the API share identities, tokens, or synchronization | Public sources show separate login processes but no API federation evidence.[4][75.82][76.9] | Signed trust-boundary diagram and token-flow review |
| P1 | Platform engineering | Remove unnecessary version disclosure and evaluate whether `X-Powered-By` is needed; maintain supported nginx, Node.js, and Express versions | Passive banners disclose nginx and Express.[13][121.86] | External headers disclose only approved metadata |
| P1 | API security | Review wildcard CORS against actual browser clients, credential mode, and response sensitivity | Shodan observed `Access-Control-Allow-Origin: *`.[13] | CORS policy matches an approved client-origin inventory |
| P1 | Product and mobile teams | Inventory mobile and web consumers from build artifacts, DNS logs, API telemetry, and application registrations | No public official mobile dependency was confirmed | Every consumer has owner, version, and retirement date |
| P1 | DNS and cloud governance | Reconcile all API-labeled Manipal hosts with cloud accounts, certificates, and owners; retire stale event systems | Passive data lists nine API-labeled hosts.[7] | Zero unowned hosts; retirement evidence for inactive assets |
| P1 | SLCM team | Publish an approved integration pattern so students do not need unofficial credential-forwarding scrapers | Community projects requested credentials and scraped sensitive academic data.[5][98.8][99.3] | Approved client guidance and reduced unofficial integrations |
| P2 | Change management | Keep versioned API contracts, response-change records, and compatibility tests | Four distinct archived root digests exist.[6] | Every production response change tied to a release record |
| P2 | Security awareness | Warn users not to enter SLCM credentials into unapproved apps and provide a reporting channel | Historical wrappers implemented credential-based sessions.[15][98.8][99.9] | Awareness notice, intake workflow, and takedown process |

A software-version finding should be handled carefully. Shodan labels nginx 1.18.0 as an end-of-life product, but its page also warns that vulnerability associations can be inferred from product/version detection and may not apply.[13][121.92][121.93] Version evidence should trigger an authenticated internal package and patch review, not a public claim that the server is exploitable.

Similarly, opaque JSON is not itself a control. If the `data` value contains sensitive information, confidentiality must come from authorization, transport security, and sound cryptography rather than obscurity. If it is public configuration or a bootstrap manifest, the owner should document that classification. The observed root provides insufficient evidence to choose between those cases.[2]

For Microsoft 365, the official SOP demonstrates password and MFA onboarding.[19][76.14] The appropriate control question is whether API authentication, if any, uses a managed application registration with audience, issuer, scope, and token-lifetime validation. Public evidence cannot answer that. The answer should come from authorized tenant and source-code review.

## 7. Synthesis

The ecosystem separates into four evidence-backed components.

| Component | Strongest evidence | What is known | What remains unknown |
|---|---|---|---|
| MUJ SLCM portals | Official portal pages and onboarding guide | Official portal URL, student-facing sign-in labels, parent login, onboarding credentials, parent OTP | Exact current application stack, API calls, session controls, and relationship to `api.manipal.edu`.[8][43.2][43.3][75.20][75.24][75.82] |
| Microsoft 365 identity | Official MUJ IT SOP | Microsoft sign-in, password-change process, and MFA setup are part of MUJ identity operations | Whether API or SLCM tokens are federated with Microsoft identity.[19][76.5][76.9][76.14] |
| `api.manipal.edu` | DNS, root response, Shodan, archives | AWS EC2 address, nginx/Node.js/Express, HTTPS JSON root, public root changes over time | Business purpose, complete routes, clients, data semantics, auth model, owner, and SLCM linkage.[1][121.42][121.44][121.46][44.0][101.0] |
| Community integrations | Public GitHub repositories | Historical credential/session scraping for profile, marks, attendance, and timetable; multiple wrapper versions | Authorization status, current operation, official mobile adoption, and applicability to MUJ.[5][98.11][98.13][99.5][100.1] |

The most important contrast is between `verified infrastructure` and `unverified function`. The API stack and address are well supported by independent sources. The claim that this API serves MUJ SLCM or an official mobile application is not. A shared parent domain is insufficient evidence of a direct application relationship.

A second contrast is between `identity presence` and `identity integration`. Microsoft 365 and MFA are officially documented for MUJ users.[19][76.5] SLCM onboarding and parent OTP are also officially documented.[4][75.82] Yet no reviewed source shows OAuth/OIDC metadata, an Entra application registration, token claims, or a Microsoft login redirect for `api.manipal.edu`. Therefore, any statement that the API uses Microsoft 365 authentication would be speculation.

A third contrast is between `historical community endpoints` and `official API endpoints`. The GitHub route names are useful for understanding demanded data categories and old automation patterns.[17][132.3][132.6] They must not be copied into an asset inventory for `api.manipal.edu` without internal confirmation. The public root is the only confirmed official-host endpoint in this report.[2]

`Inference:` The most plausible risk is not a demonstrated remote vulnerability but an API-governance gap: public service exposure, opaque response semantics, no located public contract, multiple legacy scrapers, uncertain client ownership, and a broad family of API-labeled hosts. The correct response is internal ownership and contract validation, followed by targeted, authorized security testing under a written scope.

## VERDICT

**Overall confidence: Moderate.**

| Finding | Confidence | Verdict |
|---|---|---|
| `api.manipal.edu` resolves to `43.205.223.7` on Amazon infrastructure | High | Verified by direct DNS plus urlscan and Shodan metadata.[1][103.14][121.17][121.21] |
| nginx 1.18.0, Ubuntu, Node.js, and Express were exposed | High for the passive observation dates | Shodan recorded both technology labels and matching HTTP headers.[13][121.42][121.44][121.46][121.65][121.86] |
| Root serves opaque JSON | High | Direct root extraction and passive HTTP metadata agree.[2][121.86] |
| Root representation changed historically | High | Four distinct Wayback digests were recorded.[6] |
| Official Swagger/OpenAPI documentation is publicly available | Unresolved | No valid official artifact was found; the located Swagger file was a physiotherapy-project false positive.[3] |
| API uses Microsoft 365 authentication | Low or unsupported | Microsoft 365 and MFA are official MUJ services, but API federation was not documented.[19][76.5] |
| API is the backend for MUJ SLCM or an official mobile app | Low or unsupported | No reviewed official or source artifact established the dependency.[2][75.20] |
| Historical community wrappers accessed SLCM data | High | Multiple public repositories document login/session scraping for marks, attendance, profile, and timetable.[5][98.11][98.13][99.6][100.1] |
| Related API-labeled Manipal hosts exist | Moderate | Passive host-search data lists nine names, but ownership and current activity require internal confirmation.[7] |

**Final determination:** `api.manipal.edu` is a real, Internet-facing JSON service on AWS EC2 whose observed stack is nginx 1.18.0, Node.js, and Express. Its root is public and opaque, and archived representations have changed. Public evidence does not establish its business purpose, complete endpoint set, authentication model, official mobile consumers, Swagger/OpenAPI contract, or direct relationship to MUJ SLCM. The MUJ identity ecosystem demonstrably includes SLCM credentials, parent OTP, Microsoft 365, and MFA, but those facts must not be projected onto the API without internal proof.[2][77.0][121.42][121.44][121.46][75.24][75.82][76.5]

The university security club should therefore describe the case as a `moderate-confidence governance and exposure concern`, not as a confirmed vulnerability. Any deeper validation should occur only through an authorized engagement with named owners, written scope, approved test accounts, and institutional rules of engagement.

## References

1. *dns.google*. https://dns.google/resolve?name=api.manipal.edu&type=A
2. *api.manipal.edu*. https://api.manipal.edu/
3. *manipal-server/api.yaml at main · Vedic-Technologies/manipal-server · GitHub*. https://github.com/Vedic-Technologies/manipal-server/blob/main/api.yaml
4. *Manipal University Jaipur First-Year Student Profile Registration Guide*. http://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf
5. *Slcm Api*. https://raw.githubusercontent.com/nikeplusdash/SLCM-api/master/README.md
6. *web.archive.org*. https://web.archive.org/cdx/search/cdx?url=api.manipal.edu%2F*&output=json&fl=timestamp,original,mimetype,statuscode,digest,length&filter=statuscode%3A200&collapse=digest
7. *api.hackertarget.com*. https://api.hackertarget.com/hostsearch/?q=manipal.edu
8. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
9. *Slcm Api*. https://api.github.com/repos/nikeplusdash/SLCM-api
10. *Slcm Api*. https://raw.githubusercontent.com/nikeplusdash/SLCM-api/master/SLCM.js
11. *dns.google*. https://dns.google/resolve?name=api.manipal.edu&type=CNAME
12. *api.manipal.edu - urlscan.io*. https://urlscan.io/domain/api.manipal.edu
13.(https://www.shodan.io/host/43.205.223.7)
14. *raw.githubusercontent.com*. https://raw.githubusercontent.com/canaryGrapher/slcmAPI/master/server.js
15. *Slcm Api*. https://raw.githubusercontent.com/nikeplusdash/SLCM-api/master/SLCM.py
16. *App Backend*. https://raw.githubusercontent.com/manipalthetalk/App-Backend/master/README.md
17. *api.github.com*. https://api.github.com/repos/canaryGrapher/slcmAPI/contents/routes
18. *raw.githubusercontent.com*. https://raw.githubusercontent.com/canaryGrapher/slcmAPI/master/package.json
19. *Standard Operating Procedure*. https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf
20. *api.github.com*. https://api.github.com/repos/canaryGrapher/slcmAPI
21. *Slcm Api*. https://api.github.com/repos/nikeplusdash/SLCM-api/contents
22. *raw.githubusercontent.com*. https://raw.githubusercontent.com/canaryGrapher/slcmAPI/master/README.md
23. *api.github.com*. https://api.github.com/users/manipalthetalk/repos?per_page=100
24. *api.hackertarget.com*. https://api.hackertarget.com/hostsearch/?q=jaipur.manipal.edu
25. *urlscan.io*. https://urlscan.io/api/v1/search/?q=domain%3Aapi.manipal.edu
26. *Manipal University*. https://muj.slcm.jaipur.manipal.edu/
