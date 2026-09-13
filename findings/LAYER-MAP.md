# LAYER-MAP: every layer that makes up mujslcm.jaipur.manipal.edu

Built 2026-09-13 by hands-on probing plus the campaign's verified findings. Every row names the
raw evidence file it comes from, under `recon/layers-2026-09-13/`, `recon/`, or `findings/`.
Confidence labels: VERIFIED-LIVE (measured today), VERIFIED-REPO (measured 2026-08-25 and
re-confirmed where stated), INFERRED (stated as such), UNKNOWN (not observable from outside).

Target: https://mujslcm.jaipur.manipal.edu (MUJ Student Life Cycle Management portal).
Main target only. Nothing was run against the sibling hosts.

## 1. The layer stack

### L0 People and process
| what | value | evidence | confidence |
|---|---|---|---|
| owner | MUJ academic management services, IT infrastructure | FaQs-SLCM.txt, F5 | VERIFIED-REPO |
| disclosure path | club lead, nodal officer, AMS, IT Infra, then CERT-In at 90 days | TEST-PLAN.md | VERIFIED-REPO |
| security.txt | absent (`/security.txt`, `/.well-known/security.txt` both 302 to the gate) | BATTERY-SUMMARY.json | VERIFIED-LIVE |
| bug bounty or VDP | none found for the portal | w2e-02, w2e-12 | VERIFIED-REPO |

Implication: no channel exists for a stranger to report a bug, which is the usual reason low-severity
findings on portals like this stay unpatched for years.

### L1 Domain and DNS
| what | value | evidence | confidence |
|---|---|---|---|
| target host | single A record, 98.70.14.50, no AAAA, no CNAME | dns.json, dns-doh.json | VERIFIED-LIVE |
| parent zones | jaipur.manipal.edu, muj.manipal.edu, manipal.edu all on Microsoft 365 mail | dns-parents.json | VERIFIED-LIVE |
| SPF, jaipur | two v=spf1 records: outlook + Brightspace, and a second with a /32 ip4 + SendGrid + outlook | dns-parents.json | VERIFIED-LIVE |
| SPF, muj | `v=spf1 include:spf.protection.outlook.com -all` | dns-parents.json | VERIFIED-LIVE |
| SPF, manipal.edu | outlook only, `-all` | dns-parents.json | VERIFIED-LIVE |
| DMARC, jaipur | `p=none` with rua | dns-parents.json | VERIFIED-LIVE |
| DMARC, muj | not published | dns-parents.json | VERIFIED-LIVE |
| DMARC, manipal.edu | `p=reject; pct=100` | dns-parents.json | VERIFIED-LIVE |
| DKIM tenancy | jaipur to mujcampus.onmicrosoft.com, muj to mujmanipal.onmicrosoft.com, manipal.edu to learnermanipal.onmicrosoft.com | dns-parents.json | VERIFIED-LIVE |
| nameservers | manipal.edu on Azure DNS (ns1-36.azure-dns.com and siblings), SOA hostmaster contact is awsdns-hostmaster.amazon.com | dns-parents.json | VERIFIED-LIVE |
| tenant verification | two MS= records on jaipur, four on manipal.edu, plus amazonses and an MS=DD record | dns-parents.json | VERIFIED-LIVE |

Two v=spf1 records on one domain is an SPF permerror under RFC 7208, so the jaipur domain effectively
has no enforced SPF at receivers that follow the spec. The zone was built by one provider and hosted
by another, which usually means nobody owns it end to end.

### L2 Edge and ingress
| what | value | evidence | confidence |
|---|---|---|---|
| public IP | 98.70.14.50, AS8075 Microsoft Azure, central India (Pune) | nmap.txt, probes | VERIFIED-LIVE |
| open ports | 443 only. 80 filtered, 8080 filtered | nmap.txt | VERIFIED-LIVE |
| HTTP versions | HTTP/2 and HTTP/1.1 via ALPN | http2-check.txt, testssl.txt | VERIFIED-LIVE |
| reverse proxy or CDN | no reverse-proxy banner, no CDN headers, IP is a plain Azure address | testssl.txt | VERIFIED-LIVE |
| WAF | none attributable. wafw00f's positive verdict is a false positive, see 3.4 | wafw00f.txt | VERIFIED-LIVE |
| edge cache | `cache-control: private` on the login page | home-headers.txt | VERIFIED-LIVE |

### L3 TLS and PKI
| what | value | evidence | confidence |
|---|---|---|---|
| certificate | Entrust DV TLS Issuing RSA CA 2, RSA 2048, single SAN `mujslcm.jaipur.manipal.edu` | tls-cert.txt, testssl.txt | VERIFIED-LIVE |
| chain | Entrust intermediate, Sectigo Public Server Authentication Root R46, USERTrust | tls-chain.txt | VERIFIED-LIVE |
| validity | 2025-12-22 to 2026-12-21, 99 days remaining at probe time | testssl.txt | VERIFIED-LIVE |
| protocols | TLS 1.0, 1.1, 1.2, 1.3 all complete a handshake | tls-protocols.txt, tls-v2.txt | VERIFIED-LIVE |
| suites | 3DES and CBC suites offered, AEAD with forward secrecy offered, no RC4, no export, no NULL | testssl.txt | VERIFIED-LIVE |
| OCSP | stapling offered, not revoked | testssl.txt | VERIFIED-LIVE |
| HSTS | not offered | testssl.txt | VERIFIED-LIVE |
| fallback protection | TLS_FALLBACK_SCSV NOT supported | testssl.txt | VERIFIED-LIVE |
| grading side effects | SWEET32 reported vulnerable (64-bit block ciphers), LUCKY13 potentially vulnerable | testssl.txt | VERIFIED-LIVE |

Legacy protocol support plus 3DES plus no downgrade protection plus no HSTS is the classic
legacy-friendly configuration of an IIS box that has never had a TLS review.

### L4 Host and operating system
| what | value | evidence | confidence |
|---|---|---|---|
| server banner | `Microsoft-IIS/10.0` | home-headers.txt | VERIFIED-LIVE |
| OS | Windows Server with IIS 10 (Windows Server 2016 or later family) | INFERRED from banner | INFERRED |
| patch state | not observable. The verbose error page leaks the ASP.NET patch level, not the OS level | enc-trigger.txt | UNKNOWN |
| response behaviour | no reverse proxy, no ARR headers, direct responder | testssl.txt, home-headers.txt | VERIFIED-LIVE |

### L5 Web server configuration
| what | value | evidence | confidence |
|---|---|---|---|
| error handling | customErrors off. Four reproducible verbose-error triggers | F1, enc-oracle.txt | VERIFIED-LIVE |
| tracing | `trace.axd` returns 403, so ASP.NET tracing is enabled and access restricted. `elmah.axd` 404 | trace-axd.txt, elmah-axd.txt | VERIFIED-LIVE |
| static tree | `/Scripts/jquery-1.10.2.min.js` served (94,140 b). `/Scripts/` returns 403 so the directory exists and listing is denied | BATTERY-SUMMARY.json | VERIFIED-LIVE |
| protected paths | `/web.config`, `/Global.asax`, `/bin/`, `/App_Data/`, `/packages.config` all 404 | BATTERY-SUMMARY.json | VERIFIED-LIVE |
| error pages | two families. MVC error view (2,733 b) for `/Views/`, IIS error page (1,216 b) for unmapped deep paths | body-404-views.html, body-404-app.html | VERIFIED-LIVE |
| method policy | GET 200. HEAD 404. POST and PUT 411. OPTIONS, TRACE, DELETE, PATCH, PROPFIND, SEARCH all 404 | BATTERY-SUMMARY.json, ROUND3.json | VERIFIED-LIVE |
| directory browsing | denied | BATTERY-SUMMARY.json | VERIFIED-LIVE |

### L6 Application framework
| what | value | evidence | confidence |
|---|---|---|---|
| framework | ASP.NET MVC 5.3 on .NET Framework 4.7.4136.0 (patch level leaked in the YSOD) | enc-trigger.txt | VERIFIED-LIVE |
| antiforgery | MVC antiforgery enforced server-side. Empty POST without a token returns 500 HttpAntiForgeryException. Empty POST with a token returns 200 with validation messages | POST_empty_no_token.body, ROUND3.json | VERIFIED-LIVE |
| session cookie | `__RequestVerificationToken`, HttpOnly present, Secure absent, no SameSite attribute seen | home-headers.txt, testssl.txt | VERIFIED-LIVE |
| route gate | every path up to three segments 302s to `/Home/Index`. Deeper paths and handlers diverge | ATTACK-SURFACE-MAP, ROUND3.json | VERIFIED-LIVE |
| enc parameter | a machineKey-protected blob. Three failure stages, two exception classes, two distinct response sizes. See 3.5 | ENC-ORACLE.json | VERIFIED-LIVE |
| post-login routes | 13 route names derived from the public Flutter client, not from probing | w2c-20 | VERIFIED-REPO |
| auth surface | never exercised. Six test scripts exist and are dry-run only | TRACKER.md | VERIFIED-REPO |

### L7 Client layer
| what | value | evidence | confidence |
|---|---|---|---|
| theme | Keenthemes Keen, demo1 tree, served from `/keen/themes/keen/theme/demo1/dist/` | asset-list.txt | VERIFIED-LIVE |
| jQuery | 1.10.2 loaded as its own file (94,140 b) AND 3.4.1 inside `plugins.bundle.js` (4,239,112 b). Two generations on one page | asset-versions.json | VERIFIED-LIVE |
| plugins with versions | Idle Timer 1.0, Waypoints 4.0.1, autosize 4.0.2, bootstrap-timepicker 0.5.2, nouislider 13.1.5 | bundle-components.txt | VERIFIED-LIVE |
| validation plugins | jquery.validate plus jquery.validate.unobtrusive | asset-list.txt | VERIFIED-LIVE |
| source maps | `jquery-1.10.2.min.js.map` 302 (gate), `plugins.bundle.js.map` 404 | sourcemaps.txt | VERIFIED-LIVE |
| client security headers | absent: CSP, HSTS, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, COOP | home-headers.txt, testssl.txt | VERIFIED-LIVE |
| framing | `x-frame-options: SAMEORIGIN` present | home-headers.txt | VERIFIED-LIVE |

### L8 Identity and federation
| what | value | evidence | confidence |
|---|---|---|---|
| portal accounts | username is `name.registrationNumber`, published in the official FAQ PDF | F5, FaQs-SLCM.txt | VERIFIED-REPO |
| password | the user's Microsoft 365 password. Reset delegates to Entra SSPR | F5 | VERIFIED-REPO |
| tenants | jaipur.manipal.edu, muj.manipal.edu, manipal.edu, all federated none, all Managed | oidc-*.json, getuserrealm.xml | VERIFIED-LIVE |
| SSO into the portal | not proven. The login is a local form, the reset link is Microsoft | ATTACK-SURFACE-MAP | VERIFIED-REPO |
| MFA | claimed enforced since June 2025 in the student SOP, not independently verified | w2f-09 | VERIFIED-REPO |
| mail | M365 for all three domains, DKIM per tenant, SPF and DMARC as in L1 | dns-parents.json | VERIFIED-LIVE |

### L9 Data layer
| what | value | evidence | confidence |
|---|---|---|---|
| engine | not observable from outside. MSSQL is the default for this stack | INFERRED | UNKNOWN |
| data classes | marks, results, fee receipts and documents, exam circulars, hostel and transport, library, placement, staff directory, onboarding documents | w2d-01 to w2d-09 | VERIFIED-REPO |
| PII character | student identity plus academic records plus fee records, which is regulated personal data under the DPDP Act 2023 | INFERRED from data classes | INFERRED |
| storage of documents | served through the app, path shape unknown. Downloads are a named post-auth target | TEST-PLAN.md | VERIFIED-REPO |

### L10 Integrations
| what | value | evidence | confidence |
|---|---|---|---|
| admissions CRM | NoPaperForms, `jaipurmanipal.nopaperforms.com`, behind an AWS ELB in ap-south-1 | ct-liveness.json | VERIFIED-LIVE |
| LMS | Brightspace D2L at learning.onlinemanipal.com, plus an SPF authorisation for `a._spf.brightspace.com` | dns-parents.json | VERIFIED-LIVE |
| lecture capture | Impartus, `a.impartus.com` behind an AWS ECS load balancer | ct-liveness.json | VERIFIED-LIVE |
| mail senders | Microsoft 365 plus SendGrid plus Amazon SES | dns-parents.json | VERIFIED-LIVE |
| conferencing | Webex domain verification TXT present | F5 | VERIFIED-REPO |
| mobile app | MUJ Connect (mujconnect.in), a Flutter client whose route names leak the post-auth surface | w1-07, w2c-20 | VERIFIED-REPO |

### L11 Observability and monitoring
| what | value | evidence | confidence |
|---|---|---|---|
| app tracing | ASP.NET tracing enabled and restricted (trace.axd 403) | trace-axd.txt | VERIFIED-LIVE |
| error logging | ELMAH not deployed (404) | elmah-axd.txt | VERIFIED-LIVE |
| SIEM or WAF telemetry | unknown. No sign of an edge control in front of the host | INFERRED | UNKNOWN |
| uptime and change monitoring | the certificate is the only change signal we can watch from outside | tls-cert.txt | INFERRED |

### L12 Estate around the target
| what | value | evidence | confidence |
|---|---|---|---|
| certificate names | 30 names on the jaipur wildcard and host certificates | ct-names.txt | VERIFIED-LIVE |
| names that resolve | 18 of 30 | ct-liveness.json | VERIFIED-LIVE |
| Azure plane | mujslcm 98.70.14.50, muj.slcm and npfslcm 20.244.94.89, mujerp 20.244.0.229, mujone 52.172.36.15, mycampus and testmycampus on edtech366.azurewebsites.net | ct-liveness.json | VERIFIED-LIVE |
| AWS plane | jaipur.manipal.edu and www 3.108.105.201, admissions on a NoPaperForms ELB, lcs on an Impartus ECS ELB, all ap-south-1 | ct-liveness.json | VERIFIED-LIVE |
| on-prem plane | rms 202.131.155.153, testerp 202.131.155.152, dms 1.186.160.28, dmsmuj 1.186.160.19, idp and pms 1.186.160.23 | ct-liveness.json | VERIFIED-LIVE |
| test instances | testerp and testmycampus both resolve and both were left untouched | ct-liveness.json | VERIFIED-LIVE |

### L13 Legal and regulatory
| what | value | evidence | confidence |
|---|---|---|---|
| reporting duty | CERT-In Directions 70B, six-hour reporting for specified incidents | cert-in-directions-70B.pdf | VERIFIED-REPO |
| personal data law | DPDP Act 2023, student records are personal data with a breach notification duty | dpdp_act_2023_b.pdf | VERIFIED-REPO |
| authorization position | recon only. Nothing state-changing ran. The aggressive phase needs a signed letter and two test accounts | standing orders | VERIFIED-REPO |

## 2. Evidence index

| file | proves |
|---|---|
| home-headers.txt | server and app banners, cookie flags, cache control, no HSTS or CSP |
| home.html, asset-list.txt, asset-versions.json, bundle-components.txt, plugins.bundle.js | client layer, theme, dual jQuery, plugin versions |
| tls-cert.txt, tls-chain.txt, tls-protocols.txt, tls-v2.txt, testssl.txt | TLS and PKI layer |
| nmap.txt, ports.txt | port posture |
| wafw00f.txt | the edge verdict and its false positive |
| enc-oracle.txt, ENC-ORACLE.json, enc-*.body | the enc parameter oracle, three stages |
| BATTERY-SUMMARY.json, ROUND3.json | method matrix, path classes, host header handling, validation recheck |
| body-404-views.html, body-404-app.html | the two error-page families |
| dns.json, dns-doh.json, dns-parents.json, ct-names.txt, ct-liveness.json | DNS layer and the estate |
| nuclei-lab.txt | the scanner toolchain exercised against a local lab only |

## 3. Round 3, live, 2026-09-13

All rows below come from the scripts in `scripts/` and the captures listed above. Single requests,
1.6 s apart, target only.

### 3.1 The estate has three hosting planes, not one
| host | resolves to | plane | note |
|---|---|---|---|
| mujslcm.jaipur.manipal.edu | 98.70.14.50 | Azure AS8075 | the target, central India |
| muj.slcm.jaipur.manipal.edu | 20.244.94.89 | Azure | alternate SLCM host |
| npfslcm.jaipur.manipal.edu | 20.244.94.89 | Azure | NoPaperForms SLCM naming |
| mujerp.jaipur.manipal.edu | 20.244.0.229 | Azure | ERP |
| mujone.jaipur.manipal.edu | 52.172.36.15 | Azure south India | MUJ One |
| mycampus.jaipur.manipal.edu | edtech366.azurewebsites.net | Azure App Service | direct azurewebsites host, no Front Door |
| testmycampus.jaipur.manipal.edu | edtech366.azurewebsites.net | Azure App Service | test instance shares the app service |
| jaipur.manipal.edu and www | 3.108.105.201 | AWS | CloudFront range, not Azure |
| admissions.jaipur.manipal.edu | NoPaperForms, then a prodvpc web LB in ap-south-1 | AWS ELB plus vendor | third party CRM |
| lcs.jaipur.manipal.edu | Impartus, then a prod ECS LB in ap-south-1 | AWS ECS plus vendor | lecture capture vendor |
| rms.jaipur.manipal.edu | 202.131.155.153 | on-prem, Jaipur ISP | not cloud |
| testerp.jaipur.manipal.edu | 202.131.155.152 | on-prem, Jaipur ISP | test ERP, adjacent IP to RMS |
| dms.jaipur.manipal.edu, dmsmuj.jaipur.manipal.edu | 1.186.160.28, 1.186.160.19 | on-prem | document management |
| idp.jaipur.manipal.edu | 1.186.160.23 | on-prem | an identity provider host, role not established |
| pms.jaipur.manipal.edu | 1.186.160.23 | on-prem | shares the IP with idp, role not established |

The portal is not a standalone box. It lives in an estate that spans Azure, AWS and on-prem ranges,
with two separate test-instance hosts and an identity provider host whose role is still open. Anything
learned about the SLCM host has to be re-checked wherever the same code runs, and the test instances
are the likeliest place a same-codebase instance is reachable.

### 3.2 DNS layer, parents done properly
The first pass queried the host label for MX and TXT records, which is empty by design. Corrected
against the parent domains, in the table in L1.

Two v=spf1 records on one domain is an SPF permerror, which means the domain effectively has no
working SPF policy at receivers that follow RFC 7208.

### 3.3 Edge and protocol posture, measured
- 443 open, 80 filtered, 8080 filtered (dockerised nmap 7.98)
- TLS 1.0, 1.1, 1.2 and 1.3 all complete a handshake
- 3DES and CBC suites offered, which produces the SWEET32 verdict. LUCKY13 reported as potentially vulnerable. TLS_FALLBACK_SCSV not supported, so downgrade prevention is absent
- OCSP stapling offered, not revoked. Certificate is Entrust DV, RSA 2048, single SAN, valid to 2026-12-21
- No HSTS, no public key pinning, no reverse-proxy banner
- No WAF is attributable, see 3.4

### 3.4 The wafw00f result is a false positive, explained
wafw00f 2.4.2 reports the site "seems to be behind a WAF or some sort of security solution", with the
reason that a normal request returns 200 and an XSS string returns 500. That 500 is ASP.NET request
validation, already recorded as F7. The same run then failed with an exceeded-redirect loop caused by
the app's catch-all gate. Four requests total. The honest reading is no attributable WAF, and a
fingerprinting tool scoring the app's own error handling as an edge control. This agrees with F10 and
adds the mechanism.

### 3.5 The enc parameter is a three-stage oracle
Refines F8 from a two-case observation into a graded oracle. All live, all reproducible.

| enc value | status | body | exception | stage |
|---|---|---|---|---|
| absent | 200 | 20,045 b | none | normal login page |
| empty string | 500 | 5,509 b | CryptographicException | base64 ok, decrypt fails |
| 1, 2 or 3 chars | 500 | 4,942 b | FormatException | base64 decode rejects the input |
| length not a multiple of 4 | 500 | 4,942 b | FormatException | base64 decode rejects the input |
| url-safe characters or whitespace | 500 | 5,532 b | FormatException | base64 decode rejects the input |
| `AAA=` or `AAAA` | 500 | 5,084 b | CryptographicException | base64 ok, decrypt fails |
| 32 characters, no padding | 500 | 5,084 b | CryptographicException | base64 ok, decrypt fails |
| 24 characters plus two equals signs | 500 | 4,942 b | FormatException | padding invalid for that length, decode rejects it |

Two response sizes and two exception classes separate "not base64" from "base64 but not a valid
protected blob". The second class is the machineKey-adjacent surface recorded as F8. The oracle is
useful for confirming what kind of data the parameter carries without ever attempting to forge it.

### 3.6 Probes that came back clean, now closed
| probe | result | reading |
|---|---|---|
| Host: evil.example | 200, same page, no reflection, no redirect | no host-header impact at the login page |
| X-Forwarded-Host: evil.example | 200, same page | not consumed |
| absolute-URI request target | 200, same page | proxy-style injection ignored |
| X-Forwarded-For 127.0.0.1 and Host localhost on the enc trigger | 500 FormatException, unchanged | no trust-based error-detail bypass |
| X-Original-URL: /trace.axd | 200 login page | header not honoured by IIS here |
| POST with a valid antiforgery token and empty credentials | 200, 20,167 b, validation messages | server-side validation active, no enumeration signal |
| static file /Scripts/jquery-1.10.2.min.js | 200, 94,140 b | static handler serves the tree |
| /Scripts/ directory | 403 | directory exists, listing denied |
| /Views/ | 404, 2,733 b, MVC error view | a second error-page family |
| /Home/NoSuchAction/extra/seg | 404, 1,216 b, IIS error page | IIS answers, not the MVC pipeline |

Two error-page families means two handlers answer an unmapped path, which is a routing detail worth
knowing before any post-auth work.

### 3.7 Tool log for this pass
| tool | version | where it ran | outcome |
|---|---|---|---|
| curl battery | 8.x | target | 46 targeted requests, all saved |
| wafw00f | 2.4.2 | target | generic verdict, false positive, 4 requests |
| testssl.sh | 3.3dev | target | protocols, suites, vulnerabilities, headers |
| nmap | 7.98 in docker | target | 443 open, 80 and 8080 filtered |
| openssl s_client | 3.x | target | handshake per protocol, chain, ALPN |
| Cloudflare DoH, crt.sh | API | passive | parent DNS and 30 certificate names |
| nuclei | 3.11.1 in docker, 1,654 templates | local lab only | 12 findings on a plain local server, 2,114 requests, 3 min |

The scanner class (nuclei, ffuf, sqlmap, nikto) stays off the target under standing order 3.1. The lab
run is the same toolchain exercised end to end, so the templates and the invocation are proven ready
for the authorized phase. That satisfies the instruction to use the tools without breaking the order
that protects the target.

## 4. Corrections register, this pass

| id | what was wrong | how it was caught | corrected statement |
|---|---|---|---|
| E2 | my first F8 re-check used 24 base64 characters plus two equals signs, an invalid length, so it produced FormatException | the enc oracle ladder separated decode failure from decrypt failure | padding must make the length a multiple of 4, or the decode rejects it before any crypto runs |
| E3 | testssl reports TLS 1.3 as not offered | its bundled client is OpenSSL 1.0.2, which cannot speak TLS 1.3 | TLS 1.3 is offered. System OpenSSL 3.x completes a 1.3 handshake |
| E4 | wafw00f scores a WAF from the app's own 500 | request validation F7 explains the 500, the redirect loop comes from the auth gate | no attributable WAF |

## 5. Unknowns, and how each one gets resolved

| unknown | why it matters | how to resolve it |
|---|---|---|
| Windows and IIS patch level | decides which IIS or .NET CVEs apply | auth phase, or a banner-safe authenticated probe |
| whether any WAF or IPS sits in front at the provider level | changes what a scan would trip | measured negative from outside; ask the university, or check inside the letter |
| the identity provider host `idp.jaipur.manipal.edu` | could be the SSO component of the same stack | ask, then test inside scope |
| whether the portal federates to Entra or keeps local forms auth | decides whether Entra attacks apply to the portal path | post-auth token inspection on a test account |
| database engine and version | decides SQL injection impact | auth phase |
| what `enc` packs (machineKey protect vs DPAPI vs a wrapper) | decides whether a key compromise is a real path | post-auth code review or the vendor's docs |
| deployment pipeline and whether Kudu or SCM is reachable | App Service style deployment creds are a classic full-takeover path | ask, then test in scope |
| logging and detection coverage | decides whether testing is visible | cooperative: ask the university |
| the sibling and test hosts | same code elsewhere is the usual soft entry | out of scope now. intel only |

## 6. What we are facing

A single-host, legacy-friendly, verbose ASP.NET application on Azure with no edge control in front of
it, no security.txt, no VDP, and three separate families of test and sibling hosts around it. The
identity design means the portal password is the campus Microsoft 365 password, and usernames are
derivable from public documents, so account-level controls (lockout, rate limiting, MFA) carry the
weight. Inside the app the observable weak spots are the verbose error path, the machineKey-adjacent
`enc` parameter, the missing transport hardening and the missing client-side policy headers. None of
that is an exploit, and none of it was pushed further.

This document is research and preparation. Nothing here authorizes testing of the portal or any
sibling host. The aggressive phase stays behind the signed letter and the two test accounts.
