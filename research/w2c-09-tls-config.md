# MUJ SLCM TLS Posture: Evidence, Gaps, and Priorities

## Executive Summary

- **Current Public Result**: A public SSL Labs assessment completed at the epoch corresponding to **2026-08-25 08:07:20.653 UTC** returned **grade B with warnings** for `mujslcm.jaipur.manipal.edu`, identified one endpoint at `98.70.14.50`, and reported `Microsoft-IIS/10.0`. It found TLS 1.0, TLS 1.1, and TLS 1.2, but did not list TLS 1.3 as supported [9][15]. -> Treat removal of TLS 1.0/1.1 and deployment of a modern TLS 1.2/1.3-only policy as the first transport-security change.

- **Legacy Protocol Debt**: TLS 1.0 and TLS 1.1 support is not merely unfashionable. RFC 8996 says implementations **MUST NOT** negotiate either version [3]. SSL Labs' rating guide caps a server that supports TLS 1.0 or TLS 1.1 at B [10]. -> Unless an authorized compatibility inventory identifies an indispensable legacy client, retire both versions.

- **HTTP/2 Is Real but Narrow**: The test reported ALPN `h2 http/1.1`, which is direct evidence that HTTP/2 can be negotiated [9]. RFC 9113 requires HTTP/2 over TLS to use TLS 1.2 or later and the `h2` ALPN identifier [4]. -> Do not mistake HTTP/2 support for proof that the endpoint is modern-only; old HTTP/1.1 clients can still reach the same service through TLS 1.0/1.1.

- **Certificate Is Healthy but Modest in Meaning**: The leaf is RSA-2048/SHA-256, has exactly one SAN, and is valid from **2025-12-22 00:00:00 UTC** through **2026-12-21 23:59:59 UTC**. Its issuer DN is `Entrust DV TLS Issuing RSA CA 2` [9]. -> Preserve automated renewal and CT monitoring, but do not treat a DV certificate as evidence that the application, organization, or login workflow is trustworthy.

- **Cipher Breadth Creates Avoidable Exposure**: TLS 1.2 offers strong ECDHE/DHE plus AES-GCM choices, and modern simulated clients selected those choices. The same endpoint also offers CBC suites, static RSA key exchange, and `TLS_RSA_WITH_3DES_EDE_CBC_SHA` under TLS 1.0, TLS 1.1, and TLS 1.2 [9]. -> Keep ECDHE or DHE with AEAD, and remove 3DES, static RSA key exchange, and legacy CBC-only compatibility where operationally possible.

- **BEAST and HSTS Findings Matter**: SSL Labs set `vulnBeast=true` and reported HSTS absent [9]. Its API documentation defines `vulnBeast=true` as vulnerable, while the rating guide caps BEAST-vulnerable configurations at B and warns on absent or invalid HSTS [15][10]. -> Eliminate the protocol/cipher combinations that create the BEAST condition, then deploy HSTS through controlled, authorized change management.

- **Akamai Attribution Is Not Corroborated**: Two 2026 urlscan observations identify `98.70.14.50` as Microsoft AS8075 and `Microsoft-IIS/10.0`; the August SSL Labs result tested that same address and exposed the same IIS signature [7][9]. No cited current record places an Akamai address or Akamai response signature in the tested path. -> Treat "behind Akamai" as an unverified or stale premise, not as the explanation for MUJ's observed suites.

- **Akamai Still Offers a Useful Conditional Comparison**: Akamai documents customer-selectable modern profiles limited to TLS 1.2/1.3 and compatibility profiles that retain all TLS versions, CBC, or legacy-client behavior [2]. -> If MUJ administrators independently confirm an Akamai property, move that property to `ak-akamai-2020q1` or an equivalent modern policy; otherwise harden the actual Microsoft/IIS termination point.

- **Evidence Boundary Is Critical**: The landing page visibly offers institutional, parent, and student login choices, but the cleaned public page does not name Microsoft 365, ASP.NET MVC 5.3, or .NET Framework 4.x [12][8]. -> Keep identity-provider and framework claims outside the TLS verdict until separately verified through authorized configuration records or stronger public artifacts.

## Scope, Evidence Quality, and Safe Method

This report evaluates the public TLS posture of one hostname. It does not attempt to authenticate, enumerate accounts, bypass controls, test credentials, discover an origin by evading a CDN, or provide exploitation instructions. The analysis uses public certificate-transparency data, public urlscan records, the public SSL Labs result, official standards, and vendor documentation. That scope is appropriate for a university security club studying defensive posture, but it is not a substitute for an owner-authorized internal review.

The SSL Labs API response deserves a precise methodological note. Its documentation says `fromCache` returns cached assessments when available, but also says a request with `fromCache=on` and `all=done` can start a new assessment if no cached report exists [15]. Thus, this report calls the output a **public SSL Labs assessment**, not purely passive historical data. The response is marked `isPublic=true`, `status=READY`, and includes millisecond epoch fields for start and completion [9][15]. No custom socket probing or unauthorized application interaction is described or recommended here.

### Evidence classification

| Evidence class | Source used | What it can establish | Important limit |
|---|---|---|---|
| A: machine-readable endpoint observation | SSL Labs API result [9] | Offered protocols, suites, certificate, HTTP/2/ALPN, selected feature and vulnerability results at test time | A point-in-time result for one resolved endpoint and one test service |
| A: official technical standard | RFC 8996 and RFC 9113 [3][4] | Normative protocol requirements | Does not identify MUJ's operational business constraints |
| A: vendor configuration documentation | Akamai cipher-profile documentation [2] | Profiles that Akamai customers can select | Does not reveal which profile any particular hostname uses |
| B: public passive observation | urlscan API [7] | Historical IP, ASN, server signature, page status, and certificate dates | Scanner vantage and time may differ from another user's path |
| B: transparency record | Cert Spotter and CT documentation [5][14] | Logged certificate identity and validity data | Logging does not prove present deployment or application safety |
| C: supplied ecosystem premise | "Akamai," "Microsoft 365," "ASP.NET MVC 5.3," and ".NET Framework 4.x" | Research hypotheses | Not independently established by the cited TLS and landing-page evidence |

### Claim audit

| Claim in the research brief | Assessment | Basis |
|---|---|---|
| HTTP/2 observed | **Verified** | SSL Labs reports ALPN `h2 http/1.1` [9] |
| Entrust DV leaf | **Verified, with transition nuance** | Issuer DN is Entrust-branded; its chain terminates through Sectigo material [9] |
| "Issued 2025-12-22" | **Partly verified** | `notBefore` is 2025-12-22; that is the validity start, not necessarily the exact issuance transaction time [5][9] |
| Single SAN | **Verified** | Only `mujslcm.jaipur.manipal.edu` appears in SAN [5][9] |
| TLS 1.1 exposure | **Verified** | SSL Labs lists TLS 1.1 and its accepted suites [9] |
| Akamai edge in the current path | **Not corroborated; current evidence points elsewhere** | 2026 observations identify Microsoft AS8075 at the same tested IP [7][9] |
| Microsoft 365 identity | **Not established in this TLS dataset** | The public page shows `@muj.manipal.edu` and login roles, but does not name the identity provider in cleaned content [12][8] |
| MVC 5.3 and .NET Framework 4.x | **Not established in this TLS dataset** | The cited public landing-page text does not state those versions [12] |

The decision-ready implication is that the strong findings are the endpoint's actual TLS behaviors. The stack and CDN labels should remain hypotheses until stronger evidence closes the attribution gap.

## Endpoint History: The Public Record Points to Microsoft, Not Akamai

Public observations form a useful chronology. The historical record does not prove continuous ownership or a single architecture, but it shows that the current address has been stable across multiple 2026 observations.

| Observation time | URL/port | IP and network | Server/result | Certificate observation |
|---|---|---|---|---|
| 2024-11-20 | `https://mujslcm.jaipur.manipal.edu:122/` | `202.131.155.150`, AS45769 D-Vois | HTTP 200, `Microsoft-IIS/8.5` | Valid from 2024-01-02; Entrust Certification Authority L1K [7] |
| 2026-01-15 | `https://mujslcm.jaipur.manipal.edu/` | `98.70.14.50`, AS8075 Microsoft | HTTP 200, `Microsoft-IIS/10.0` | Valid from 2025-12-22; Entrust DV TLS Issuing RSA CA 2 [7] |
| 2026-06-16 | `https://mujslcm.jaipur.manipal.edu/` | `98.70.14.50`, AS8075 Microsoft | HTTP 200, HTTPS-only, `Microsoft-IIS/10.0` | Same 2025-12-22 validity start and Entrust DV issuer [7] |
| 2026-08-25 | Port 443 SSL Labs assessment | `98.70.14.50` | Grade B, warnings, `Microsoft-IIS/10.0` | Same single-SAN leaf and chain [9] |

The 2024 record used a nonstandard port and a different provider, so it should not be treated as a like-for-like predecessor of today's port 443 service. The three 2026 data points are more probative: January and June urlscan results attach the address to Microsoft AS8075, and the August TLS test resolves and tests that same address [7][9].

**Inference, medium-high confidence:** from the cited public vantage points, TLS appears to terminate at a Microsoft-hosted IIS 10 endpoint rather than an Akamai edge. This remains an inference because split-horizon DNS, geographic steering, temporary bypasses, or an unobserved upstream service could produce another path. Still, "behind Akamai" should not be promoted to fact when the available IP, ASN, and server observations consistently point to Microsoft.

This is an important OSINT case study in attribution discipline. A server header alone could be passed through a proxy and would be weak evidence. Here, however, the same Microsoft ASN address recurs over months and is the endpoint SSL Labs tested. The combined evidence is stronger than the IIS header alone, yet it still does not reveal the private origin topology or owner-side configuration.

## Certificate Record: One SAN, Entrust Name, Sectigo Chain

The leaf certificate is conventional and substantially stronger than the surrounding legacy protocol policy. SSL Labs reports an RSA 2048-bit public key, SHA-256-with-RSA signature, no certificate issues, one DNS SAN, and validity from 2025-12-22 through 2026-12-21 [9]. Cert Spotter independently records the same SAN, validity start, issuer DN, certificate SHA-256 fingerprint, and public-key fingerprint [5].

| Certificate field | Public value | Assessment |
|---|---|---|
| Subject CN | `mujslcm.jaipur.manipal.edu` [9] | Matches the evaluated host |
| SAN | `mujslcm.jaipur.manipal.edu` only [5][9] | Exactly one SAN; no wildcard or additional host shown |
| Validity | 2025-12-22 00:00:00 UTC to 2026-12-21 23:59:59 UTC [9] | Approximately one year; currently valid at assessment time |
| Issuer DN | `C=CA, O=Entrust Limited, CN=Entrust DV TLS Issuing RSA CA 2` [9] | Domain-validated issuing hierarchy |
| Leaf key/signature | RSA 2048, SHA256withRSA [9] | Conventional publicly trusted configuration |
| Serial | `00a8fe91aaac91730fe90d034dee36f7c7` [9] | Exact leaf identifier |
| SHA-256 | `ac5809c880358f9cfbf5c89ad49289ff197858e026895540c903f244a6540924` [5][9] | Matches CT-derived and SSL Labs records |
| OCSP/SCT | OCSP stapling enabled; SCT present [9] | Positive deployment features, without implying application safety |
| DNS CAA | SSL Labs reports CAA absent [9] | Governance improvement opportunity, not proof of compromise |

Calling December 22 the "issuance date" is slightly stronger than the public fields warrant. The records establish `notBefore`, meaning the certificate became valid at that instant. They do not expose the exact CA transaction timestamp. The accurate formulation is **"validity began on 2025-12-22"** [5][9].

The apparently mixed Entrust/Sectigo naming is explainable without assuming an invalid chain. The leaf issuer is Entrust-branded, but SSL Labs shows the intermediate chaining to `Sectigo Public Server Authentication Root R46` [9]. Sectigo announced its purchase of Entrust's public certificate business on January 29, 2025 and said customers would receive a seamless transition [13]. That transaction explains why public metadata may label the issuer family "Sectigo" while the issuing-CA distinguished name remains Entrust-branded. The source does not explicitly promise indefinite continuation of Entrust naming, so the report does not go further.

Certificate Transparency adds accountability, not a security warranty. CT logs are publicly verifiable, append-only ledgers that let observers see which CAs issued certificates, when, and for which domains [14]. CT documentation also cautions that logging does not itself prove correct issuance or CA trustworthiness [14]. **Inference:** a single SAN narrows this certificate's advertised identity scope to one hostname, but it does not reduce risks from a compromised server, stolen private key, insecure application, or weak TLS policy.

## TLS Handshake and Cipher Inventory

The public result reports three enabled protocol versions. SSL and TLS 1.3 are not listed in the result's supported-protocol array, so the careful claim is "TLS 1.3 was not reported as supported," not that every possible network vantage can never negotiate it [9].

| Protocol | Public result | Main security implication |
|---|---|---|
| TLS 1.0 | Enabled [9] | Formally deprecated; enables legacy CBC and 3DES choices |
| TLS 1.1 | Enabled [9] | Formally deprecated even though it improves on some TLS 1.0 behavior |
| TLS 1.2 | Enabled [9] | Strong ECDHE/DHE plus AES-GCM available, but legacy suites remain |
| TLS 1.3 | Not listed as supported [9] | Modern protocol benefits are not evidenced by this result |
| HTTP/2 | ALPN `h2 http/1.1` [9] | Modern application protocol is available over TLS 1.2 or later |

RFC 8996 states that TLS 1.0 and TLS 1.1 MUST NOT be used or negotiated [3]. NIST SP 800-52 Revision 2 requires government TLS servers and clients to support TLS 1.2 with FIPS-based suites and required TLS 1.3 support by January 1, 2024 [1]. MUJ is not asserted to be subject to the US federal profile, but the comparison shows how far a current conservative baseline has moved beyond TLS 1.1.

### Exact offered suites reported by SSL Labs

| Protocol | Cipher suite | Class | Security note |
|---|---|---|---|
| TLS 1.0 | `TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA` | ECDHE, AES-CBC | Forward-secret key exchange, legacy record protection |
| TLS 1.0 | `TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA` | ECDHE, AES-CBC | Forward-secret key exchange, legacy record protection |
| TLS 1.0 | `TLS_RSA_WITH_AES_256_CBC_SHA` | Static RSA, AES-CBC | No Forward Secrecy |
| TLS 1.0 | `TLS_RSA_WITH_AES_128_CBC_SHA` | Static RSA, AES-CBC | No Forward Secrecy |
| TLS 1.0 | `TLS_RSA_WITH_3DES_EDE_CBC_SHA` | Static RSA, 3DES | 112-bit reported strength; obsolete 64-bit block cipher |
| TLS 1.1 | `TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA` | ECDHE, AES-CBC | Better key exchange, deprecated protocol |
| TLS 1.1 | `TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA` | ECDHE, AES-CBC | Better key exchange, deprecated protocol |
| TLS 1.1 | `TLS_RSA_WITH_AES_256_CBC_SHA` | Static RSA, AES-CBC | No Forward Secrecy |
| TLS 1.1 | `TLS_RSA_WITH_AES_128_CBC_SHA` | Static RSA, AES-CBC | No Forward Secrecy |
| TLS 1.1 | `TLS_RSA_WITH_3DES_EDE_CBC_SHA` | Static RSA, 3DES | Deprecated protocol plus obsolete cipher |
| TLS 1.2 | `TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384` | ECDHE, AEAD | Strong modern choice |
| TLS 1.2 | `TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256` | ECDHE, AEAD | Strong modern choice |
| TLS 1.2 | `TLS_DHE_RSA_WITH_AES_256_GCM_SHA384` | DHE, AEAD | Strong, with 2048-bit DH reported |
| TLS 1.2 | `TLS_DHE_RSA_WITH_AES_128_GCM_SHA256` | DHE, AEAD | Strong, with 2048-bit DH reported |
| TLS 1.2 | `TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384` | ECDHE, AES-CBC | Forward-secret but non-AEAD |
| TLS 1.2 | `TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256` | ECDHE, AES-CBC | Forward-secret but non-AEAD |
| TLS 1.2 | `TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA` | ECDHE, AES-CBC | Legacy hash/CBC construction |
| TLS 1.2 | `TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA` | ECDHE, AES-CBC | Legacy hash/CBC construction |
| TLS 1.2 | `TLS_RSA_WITH_AES_256_GCM_SHA384` | Static RSA, AEAD | AEAD without Forward Secrecy |
| TLS 1.2 | `TLS_RSA_WITH_AES_128_GCM_SHA256` | Static RSA, AEAD | AEAD without Forward Secrecy |
| TLS 1.2 | `TLS_RSA_WITH_AES_256_CBC_SHA256` | Static RSA, AES-CBC | No Forward Secrecy |
| TLS 1.2 | `TLS_RSA_WITH_AES_128_CBC_SHA256` | Static RSA, AES-CBC | No Forward Secrecy |
| TLS 1.2 | `TLS_RSA_WITH_AES_256_CBC_SHA` | Static RSA, AES-CBC | Legacy construction |
| TLS 1.2 | `TLS_RSA_WITH_AES_128_CBC_SHA` | Static RSA, AES-CBC | Legacy construction |
| TLS 1.2 | `TLS_RSA_WITH_3DES_EDE_CBC_SHA` | Static RSA, 3DES | Obsolete cipher retained under TLS 1.2 |

All suite names and strength/protocol groupings above come from the exact-host response [9]. The table's labels such as "strong modern choice" and "legacy construction" are analyst classifications based on whether the suite uses ephemeral key exchange and AEAD; they are not claims that every session is exploitable.

The client simulations make the practical split clear. Modern Chrome, Firefox, Edge, Safari, Opera, OpenSSL, and Java profiles selected TLS 1.2 with AES-GCM, commonly through ECDHE. Older Android, Internet Explorer, Windows Phone, Java, OpenSSL, and Safari profiles selected TLS 1.0 with CBC; IE 6 on XP failed [9]. **Inference:** normal current users probably receive the stronger branch, but the server still preserves a weaker branch for clients capable of asking for it. A secure default for modern users does not erase the attack surface exposed to legacy negotiation.

## HTTP/2 Does Not Cancel Legacy TLS

The handshake evidence for HTTP/2 is straightforward: SSL Labs reports ALPN protocols `h2 http/1.1` [9]. RFC 9113 defines `h2` as HTTP/2 over TLS and says an HTTPS client uses ALPN to select the application protocol [4]. This is stronger evidence than a page-load speed impression or generic technology fingerprint.

The security interpretation is narrower. RFC 9113 requires HTTP/2-over-TLS implementations to use TLS 1.2 or higher [4]. For TLS 1.2 deployments it requires compression to be disabled, restricts renegotiation, discourages prohibited suites, and requires support for `TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256` with P-256 [4]. MUJ offers that required GCM suite and reports no TLS compression, so the observed h2 branch has relevant modern ingredients [9].

**Inference:** an h2-capable browser cannot use TLS 1.0 for its h2 connection, but that does not force the entire virtual host to reject TLS 1.0/1.1. The same endpoint advertises HTTP/1.1 in ALPN and accepts legacy protocols and ciphers [9]. Therefore, "HTTP/2 works" and "legacy TLS remains enabled" are compatible observations, not contradictory ones.

This distinction matters for risk communication. HTTP/2 is a performance and application-framing capability with TLS constraints; it is not a blanket certification of certificate governance, HSTS, cipher hygiene, or origin architecture. The club should report the positive observation and the remaining protocol debt separately.

## Akamai Settings: Useful Comparison, Unproven Attribution

Akamai's documentation shows that edge TLS behavior is policy-driven. Through Certificate Provisioning System, a customer selects a cipher profile, which determines suites offered in the handshake; Akamai says existing profiles are not routinely changed except in security incidents [2]. That mechanism can produce long-lived compatibility exposure when an old enrollment is not deliberately migrated.

| Akamai profile | Documented protocol scope | Relevant suite pattern | Meaning for this case |
|---|---|---|---|
| `ak-akamai-2020q1` | TLS 1.2 and TLS 1.3 only; default/recommended for new certificates since 2020-09-16 [2] | AEAD-focused; no CBC or 3DES listed [2] | Conditional target if an Akamai property is confirmed |
| `ak-akamai-2020q1-without-chachapoly` | TLS 1.2 and TLS 1.3 only [2] | Excludes ChaChaPoly; no CBC or 3DES listed [2] | Modern compatibility variant |
| `ak-akamai-2018q3` | All TLS versions, including TLS 1.3 [2] | Includes CBC and RSA suites; no 3DES listed [2] | Can preserve TLS 1.0/1.1 despite TLS 1.3 capability |
| `ak-akamai-default-2017q3` | All TLS versions, including TLS 1.3 [2] | Intended for clients requiring TLS 1.0/1.1 or lacking Forward Secrecy [2] | Direct example of the legacy-client pattern |
| Deprecated 2016-era profiles | No longer selectable, but existing enrollments may continue [2] | Some include `DES-CBC3-SHA` for old Windows/IE compatibility [2] | Explains how inherited profiles can retain 3DES |
| End-of-life profiles | Existing enrollments may remain and renew [2] | Include CBC-era, RSA, and 3DES suites [2] | Renewal alone does not modernize TLS policy |

This vendor evidence supports a **mechanism**, not a site-specific attribution. It shows how an Akamai-fronted educational service could expose TLS 1.1: an administrator might retain `ak-akamai-2018q3`, `ak-akamai-default-2017q3`, or an inherited profile for legacy clients. It does not show that MUJ selected any such profile, and it does not establish how prevalent the pattern is across education sites [2].

No defensible public cohort dataset was found in the reviewed sources for the prevalence of TLS 1.1 among Akamai-fronted university sites. Accordingly, this report does **not** claim that educational Akamai customers usually have weak TLS. Any explanation involving old campus devices, embedded clients, or compatibility pressure would be plausible but unsupported here, so it remains omitted rather than presented as fact.

The observed MUJ list also does not cleanly match Akamai's documented active profiles: it includes 3DES under all enabled protocol versions, while Akamai's listed 2017q3 and 2018q3 active profiles do not list 3DES [2][9]. That divergence reinforces the attribution warning. **Inference:** the observed policy is more consistent with a locally managed Windows/IIS cipher configuration or another unverified termination layer than with the documented current Akamai active profiles. This is not proof of the specific control plane.

## What the Public SSL Test Actually Says

The exact-host result is `READY`, `isPublic=true`, engine version `2.4.3`, criteria version `2009q`, endpoint grade B, and `hasWarnings=true` [9]. SSL Labs' public rating guide currently visible in the research corpus is version `2009r`, dated 2025-05-16 [10]. Because the result and guide carry different criteria labels, the current guide is useful for interpretation but should not be treated as a perfect reconstruction of the test engine's arithmetic.

SSL Labs first validates the certificate, scores protocol support, key exchange, and cipher support, combines the category scores, and maps the resulting number to a letter grade [10]. The guide caps TLS 1.0/1.1 support at B and BEAST vulnerability at B [10]. It also describes a C penalty for 3DES or another 64-bit block cipher with TLS 1.1 or later [10]. Yet the machine result is B [9]. The honest conclusion is that the legacy protocol and BEAST rules are fully consistent with the observed B, while the apparent 3DES/rating tension may reflect criteria-version or rule-application differences that this public artifact does not resolve.

### Feature and vulnerability interpretation

| Public field | Exact result | Correct interpretation |
|---|---|---|
| `vulnBeast` | `true` [9] | API definition says endpoint is vulnerable to BEAST [15] |
| `poodle` | `false` [9] | SSLv3 POODLE boolean was not raised |
| `poodleTls` | `1` [9] | API enumeration says value 1 means not vulnerable [15] |
| `openSslCcs` | `1` [9] | Not vulnerable [15] |
| `openSSLLuckyMinus20` | `1` [9] | Not vulnerable [15] |
| `ticketbleed` | `1` [9] | Not vulnerable [15] |
| `bleichenbacher` | `1` [9] | Not vulnerable [15] |
| `zombiePoodle` | `1` [9] | Not vulnerable [15] |
| `goldenDoodle` | `1` [9] | Not vulnerable [15] |
| `zeroLengthPaddingOracle` | `1` [9] | Not vulnerable [15] |
| `sleepingPoodle` | `1` [9] | Not vulnerable [15] |
| `freak`, `logjam`, `heartbleed` | `false` [9] | Those booleans were not raised in this result |
| HSTS | absent [9] | Browser upgrade enforcement is not advertised by the tested response |
| OCSP stapling | enabled [9] | Endpoint staples revocation information |
| Compression | `0` [9] | No TLS compression method reported |
| Secure renegotiation | `renegSupport=2` [9] | Bit 1 means secure renegotiation supported [15] |
| Session IDs | `sessionResumption=1` [9] | IDs returned, but sessions were not resumed [15] |
| Session tickets | `0` [9] | No ticket-support bit set [15] |
| 0-RTT | `-1` [9] | Test not performed, not "disabled" [15] |

This correction is important: many SSL Labs fields are enumerations, so value `1` does not mean "vulnerable" for the oracle tests. The only clearly positive vulnerability boolean in the cited result is BEAST. The broader concern remains policy breadth: deprecated protocols, 3DES, CBC, static RSA, absent HSTS, and no reported TLS 1.3 [9].

## Risk Priorities and Defensive Remediation

The risk is not "TLS is broken." Modern simulated clients negotiated TLS 1.2 with AES-GCM, the certificate is valid and trusted along major paths, HTTP/2 works, and multiple severe historical test flags were negative [9]. The risk is that the server preserves unnecessary weaker options alongside the strong ones.

| Priority | Finding | Mechanism and consequence | Defensive action for the authorized owner | Validation criterion |
|---|---|---|---|---|
| P0 | TLS 1.0 and TLS 1.1 enabled | Clients can negotiate formally deprecated protocols [3][9] | Set the actual termination layer to TLS 1.2 minimum after an owner-approved client inventory | Public result lists only TLS 1.2/1.3 |
| P0 | 3DES and static RSA offered | 3DES has a 64-bit block design; static RSA lacks Forward Secrecy [9][10] | Remove `TLS_RSA_WITH_3DES_EDE_CBC_SHA` and static-RSA suites | No 3DES or `TLS_RSA_*` in suite inventory |
| P0 | BEAST positive | Legacy CBC behavior creates the test condition [9][15] | Remove TLS 1.0 and associated legacy CBC paths rather than relying on client mitigations | `vulnBeast=false` in an owner-authorized retest |
| P1 | TLS 1.3 not reported | Endpoint misses the modern protocol branch shown in current Akamai and NIST baselines [2][1] | Enable TLS 1.3 where supported without weakening TLS 1.2 | TLS 1.3 appears; modern client simulations succeed |
| P1 | HSTS absent | Users can lack browser-enforced HTTPS-only policy after first secure contact [9][10] | Add HSTS only after confirming every covered hostname and redirect path is HTTPS-ready | Valid HSTS shown; no dependent host outage |
| P1 | Edge owner uncertain | Changes applied to the wrong platform will not alter the public handshake [7][9] | Reconcile DNS, load balancer, Azure/IIS, and any Akamai property in internal configuration records | Named control owner matches the public termination point |
| P2 | CAA absent | DNS does not express a CA authorization policy in the observed test [9] | Consider CAA plus CT alerting under domain-governance policy | Expected CAA record and renewal path verified |
| P2 | Identity boundary unverified | TLS findings do not establish Microsoft 365 or token/session policy [12] | Review SSO separately with the identity team; do not infer it from the web certificate | Documented IdP, redirect URIs, MFA, and session controls |

The safest rollout is staged and owner-authorized. First identify actual negotiating client populations from server-side telemetry, then remove the oldest protocol branch in a controlled window, monitor failures, and retire remaining legacy suites. This is a governance recommendation, not an instruction to probe the service. If an Akamai property is confirmed, Akamai recommends profiles such as `ak-akamai-2020q1` for PFS, HTTP/2, TLS 1.3, and PCI-oriented support [2]. If no Akamai property is in the path, those settings are irrelevant and the Microsoft/IIS or load-balancer owner must make the change.

Certificate operations should remain separate from cipher policy. Renewal of the same certificate can succeed while a legacy cipher profile persists; Akamai explicitly notes that some end-of-life profiles may continue on existing enrollments and automated renewals [2]. Conversely, replacing the leaf certificate will not by itself disable TLS 1.0, remove 3DES, or enable HSTS. These controls live at different layers.

## Evidence-to-Conclusion Reasoning Summary

The following table supplies an auditable rationale without exposing private scratch work. Each conclusion shows what the evidence supports and what it does not.

| Observation | Supported conclusion | Unsupported leap avoided |
|---|---|---|
| Same Microsoft AS8075 IP in January and June urlscan, and same IP in August SSL Labs [7][9] | Current public evidence points to a Microsoft-hosted TLS endpoint | "Akamai is definitely absent everywhere" |
| ALPN lists `h2 http/1.1` [9] | HTTP/2 negotiation is available | "All connections use HTTP/2" or "legacy TLS is disabled" |
| TLS 1.0/1.1/1.2 suite arrays exist [9] | Endpoint accepts deprecated protocol branches | "Every user receives weak encryption" |
| Modern simulations select TLS 1.2 AES-GCM [9] | Strong options are available and preferred for those profiles | "The configuration is fully secure" |
| `vulnBeast=true`, while multiple integer oracle fields equal 1 [9][15] | BEAST is positive; the listed value-1 oracle tests mean not vulnerable | Treating every nonzero integer as a vulnerability |
| Leaf has one SAN and DV issuer [5][9] | Certificate authenticates control for the named DNS identity under public-PKI rules | Organizational vetting, application integrity, or secure identity flows |
| Akamai documents legacy and modern profiles [2] | Profile inheritance is a credible mechanism for weak Akamai TLS exposure | Claiming MUJ uses a particular Akamai profile |
| Landing page shows institutional, parent, and student sign-ins [12][8] | Several login journeys exist | Proving Microsoft 365, MFA posture, MVC version, or .NET version |

The non-obvious tension is that several positive features coexist with a B-grade legacy policy. A valid certificate, OCSP stapling, HTTP/2, TLS 1.2 GCM, and negative results for many named vulnerabilities do not compensate for continued acceptance of deprecated protocol and cipher branches. Security posture is determined by the weakest negotiable path, not only the path a current browser chooses.

## Synthesis: Edge, Origin, Certificate, and Identity Are Different Boundaries

| Boundary | What is publicly evidenced | Security control in scope | Main trade-off | Confidence |
|---|---|---|---|---|
| Public TLS termination | `98.70.14.50`, IIS 10, TLS 1.0/1.1/1.2, h2, grade B [9] | Protocols, suites, HSTS, certificate presentation | Legacy compatibility versus reduced attack surface | High for test time |
| Microsoft-hosted endpoint | AS8075 in two 2026 urlscan records [7] | Hosting/load-balancer/IIS ownership | Operational simplicity versus attribution ambiguity | Medium-high |
| Claimed Akamai layer | Vendor profiles are documented, but site-specific selection is absent [2] | CDN edge policy if property exists | Global edge management versus inherited compatibility profiles | Low for MUJ attribution |
| Public certificate hierarchy | One-SAN Entrust DV leaf chaining through Sectigo material [5][9] | DNS identity, renewal, CT, revocation | Narrow identity scope versus limited organizational assurance | High |
| Login/identity layer | Multiple visible login choices and `@muj.manipal.edu` label [12][8] | SSO, MFA, tokens, sessions | Central identity convenience versus separate redirect/session risks | Low for Microsoft 365 premise |
| Application framework | IIS 10 only is evidenced by the TLS and scan records [7][9] | MVC/.NET patching and app controls | Legacy framework compatibility versus maintenance risk | Low for stated MVC/.NET versions |

Three cross-cutting conclusions follow. First, **attribution precedes remediation**: an administrator cannot fix a handshake by changing an Akamai profile if users actually terminate on a Microsoft-hosted IIS or load balancer. Second, **certificate health and TLS policy are orthogonal**: the leaf can be valid, logged, and correctly named while the endpoint still accepts obsolete protocols. Third, **transport and identity reviews are related but distinct**: the certificate protects the browser-to-host channel; it does not prove how Microsoft 365, MFA, parent credentials, or application sessions are implemented.

The Akamai comparison remains valuable as a failure-pattern model. Vendor platforms often preserve old profiles for customers with compatibility requirements, and those profiles can survive certificate renewals [2]. Yet the MUJ evidence warns against converting a generic mechanism into a site-specific accusation. The correct sequence is evidence, attribution, owner identification, controlled change, and authorized verification.

## VERDICT

**Overall verdict: B-grade public TLS with a valid certificate and working HTTP/2, but material legacy-protocol and cipher debt. Remediation priority: High for protocol hardening, Medium for HSTS and governance, and Investigative for architecture attribution.**

The strongest positive findings are the valid single-SAN certificate, major-platform trust paths, RSA-2048/SHA-256 leaf, OCSP stapling, TLS 1.2 AES-GCM options, ephemeral key-exchange options, and HTTP/2 negotiation [9]. The strongest negatives are accepted TLS 1.0/1.1, BEAST positive, 3DES, extensive CBC and static-RSA choices, absent HSTS, and no TLS 1.3 support reported by the public assessment [9]. RFC 8996 makes the protocol conclusion unambiguous: TLS 1.0 and TLS 1.1 must not be negotiated [3].

**Confidence levels:**

| Finding | Confidence | Reason |
|---|---|---|
| Certificate identity, SAN, and validity | **High** | SSL Labs and Cert Spotter agree [5][9] |
| Protocol, cipher, HTTP/2, HSTS, and BEAST result at assessment time | **High** | Exact-host machine-readable SSL Labs output [9] |
| Current endpoint is Microsoft-hosted | **Medium-high** | Same address across independent 2026 observations, with AS8075 attribution [7][9] |
| MUJ is currently behind Akamai | **Low / not corroborated** | No cited site-specific Akamai edge evidence; current records point to Microsoft |
| Weak Akamai profile mechanism in general | **High** | Akamai's own profile documentation [2] |
| Prevalence among Akamai-fronted education sites | **Insufficient evidence** | No defensible cohort dataset was found in the reviewed public sources |
| Microsoft 365 identity and MVC/.NET versions | **Low in this report** | Landing-page and TLS artifacts do not independently establish those premises [12][8] |

The university security club should present this as a defensive finding to the authorized service owner: **modern clients get a reasonably strong TLS 1.2 path, but the endpoint still exposes weaker negotiable paths that should be retired.** It should not present Akamai as the cause without fresh DNS, property, or owner-side proof, and it should not extend a TLS result into claims about account security or application vulnerabilities.

## References

1. *SP 800-52 Rev. 2, Guidelines for the Selection, Configuration ...*. https://csrc.nist.gov/pubs/sp/800/52/r2/final
2. *Update SSL/TLS cipher profiles*. https://techdocs.akamai.com/cps/docs/cipher-profiles
3. *RFC 8996: Deprecating TLS 1.0 and TLS 1.1*. https://www.rfc-editor.org/rfc/rfc8996.html
4. [
            
        RFC 9113 - HTTP/2

        ](https://datatracker.ietf.org/doc/rfc9113)
5. *api.certspotter.com*. https://api.certspotter.com/v1/issuances?domain=mujslcm.jaipur.manipal.edu&include_subdomains=false&expand=dns_names&expand=issuer&expand=cert
6. *mujslcm.jaipur.manipal.edu - urlscan.io*. https://urlscan.io/domain/mujslcm.jaipur.manipal.edu
7. *urlscan.io*. https://urlscan.io/api/v1/search/?q=domain:mujslcm.jaipur.manipal.edu
8. *Manipal University - mujslcm.jaipur.manipal.edu*. https://mujslcm.jaipur.manipal.edu/Home/Index
9. *api.ssllabs.com*. https://api.ssllabs.com/api/v3/analyze?host=mujslcm.jaipur.manipal.edu&fromCache=on&maxAge=1000000&all=done&startNew=off
10. *SSL Server Rating Guide · ssllabs/research Wiki · GitHub*. https://github.com/ssllabs/research/wiki/SSL-Server-Rating-Guide
11. *Qualys SSL Labs - Projects / SSL Labs APIs*. https://www.ssllabs.com/projects/ssllabs-apis/index.html
12. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
13. *Sectigo acquires Entrust public certificate business, doubling the size of its enterprise operations | Sectigo® Official*. https://www.sectigo.com/resource-library/sectigo-acquires-entrust-public-certificate-business
14. [
    Certificate Transparency : Certificate Transparency
  ](https://certificate.transparency.dev/)
15. *ssllabs-scan/ssllabs-api-docs-v4.md at master · ssllabs/ssllabs-scan · GitHub*. https://github.com/ssllabs/ssllabs-scan/blob/master/ssllabs-api-docs-v4.md
16. *Latest Baseline Requirements | CA/Browser Forum*. https://cabforum.org/working-groups/server/baseline-requirements/requirements
