# MUJ Entra Exposure: Two Tenants, One Defensive Priority

## Executive Summary

- **Two-Tenant Boundary**: Public Microsoft OpenID Connect metadata maps `jaipur.manipal.edu` to tenant **7d0726e8-bf4b-4ac1-99f1-010fb11f1d3f** and `muj.manipal.edu` to a different tenant, **27282fdd-4c0b-4dfb-ba91-228cd83fdf71** [5][3] -> MUJ should treat cross-tenant policy consistency, account lifecycle, emergency access, and logging as the first governance priority.
- **Managed, Not Externally Federated**: Microsoft's public realm responses classify both domains as `Managed` and identify the organization as Manipal University Jaipur [20][21]. The two federation-metadata documents publish Microsoft STS and WS-Federation endpoints [2][4] -> do not mistake the existence of a `federationmetadata` URL for evidence of an active third-party identity provider.
- **Portal-to-Tenant Split**: The public `muj.slcm.jaipur.manipal.edu` page advertises `@jaipur.manipal.edu`, while `mujslcm.jaipur.manipal.edu` advertises `@muj.manipal.edu` [22][23] -> **inference:** the SLCM ecosystem spans a migration, segmentation, or legacy-overlap boundary; public evidence cannot determine which explanation is correct.
- **Enumeration Is Partly Confirmed**: Domain-to-tenant enumeration is conclusively possible through intended public Microsoft discovery services [5][3][1]. Security-testing literature describes `GetCredentialType` as an account-enumeration vector [24], while Microsoft characterizes it as an internal credential-discovery endpoint that is not a supported onboarding decision API [18] -> MUJ-specific per-user differentiation remains **unknown and deliberately untested**.
- **Mandatory MFA Is Documented, Strength Is Not**: MUJ's June 2025 Office 365 SOP says MFA is mandatory before Office 365 use [25] and documents Authenticator, phone, and personal-email security-information registration [25] -> this proves an enrollment requirement, but not Conditional Access coverage, administrator protection, phishing resistance, or the absence of exclusions.
- **Recovery and MFA Must Not Be Conflated**: Microsoft's method table associates email OTP primarily with SSPR and qualified sign-in scenarios, while SMS and Authenticator push can participate in both MFA and recovery [14] -> **inference:** MUJ's personal-email step is evidence of security-information enrollment, not proof that personal email satisfies strong MFA.
- **Exchange Online Discovery Is Normal but Useful to Reconnaissance**: Both mail domains use Outlook MX infrastructure [26][27], publish DKIM selectors tied to different `onmicrosoft.com` namespaces [28][29][30][31], and point Autodiscover to `autodiscover.outlook.com` [32][33] -> hiding standard metadata is not a realistic defense; strong authentication and detection must absorb the reconnaissance risk.
- **Mail Enforcement Needs Attention**: `jaipur.manipal.edu` publishes DMARC `p=none`, `muj.manipal.edu` has no child DMARC record, and the organizational parent `manipal.edu` also publishes `p=none` [34][35][8] -> **inference:** monitoring exists, but the observed policy strings do not request quarantine or rejection of failing mail.
- **Indian Education Is a High-Exposure Context, Not Proof of MUJ Weakness**: Seqrite reports **4.92M** Education and Training detections, **18.45%** of its India detections, from October 2024 through September 2025 [15] -> use this as threat-prioritization evidence, not as evidence that MUJ has any particular MFA gap.
- **Phishing-Resistant MFA Is the Target State**: Microsoft places FIDO2, Windows Hello for Business or platform credentials, and certificate-based authentication in its phishing-resistant authentication strength [11]. CISA calls FIDO/WebAuthn and PKI-based MFA phishing-resistant, while describing SMS or voice as a last-resort option [19] -> prioritize phishing-resistant methods for administrators and other high-impact users in both tenants.

## 1. Scope, Safety, and Evidence Standard

This is a passive, public-information assessment of the Microsoft 365 identity layer associated with the MUJ SLCM ecosystem. It does not attempt passwords, submit authentication requests for real people, automate account checks, access mailboxes, or test SSPR against student or staff identities. The ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, and Akamai descriptions in the prompt are treated as supplied scope assumptions, not independently verified findings. The conclusions below concern Microsoft Entra ID and Exchange Online rather than the application's server-side vulnerability posture.

The investigation uses three evidence classes. First-party Microsoft discovery documents and public DNS records are treated as direct observations. MUJ's own Office 365 SOP and login pages are treated as first-party statements about intended user experience. External threat reports and security literature provide context but cannot establish MUJ-specific settings.

Microsoft expressly describes the OpenID Provider Configuration Document as a publicly accessible document containing OIDC endpoints, supported claims, and other provider metadata [1]. Therefore, retrieving a domain's `openid-configuration` document is passive standards-based discovery, not evidence of access control bypass. The same principle applies to DNS MX, SPF, DKIM, DMARC, and Autodiscover records, which must be externally resolvable for their normal purposes.

### Auditable decision trace

I cannot provide private hidden chain-of-thought. In its place, the table below gives a reproducible evidence-to-conclusion trace showing each observation, the limited interpretation made from it, and what remains unknown.

| Observation | Direct conclusion | Labeled inference | What is not established |
|---|---|---|---|
| The two OIDC documents return different tenant GUIDs [5][3] | Two Entra tenant security boundaries are publicly associated with the two mail domains | Policy drift is a higher governance risk than it would be in one tenant | Why MUJ operates two tenants, which one is authoritative, or whether migration is underway |
| Both realm lookups say `Managed` [20][21] | Microsoft Entra performs managed-domain home-realm discovery | Password validation is likely in Microsoft's managed identity path | Password-hash sync, pass-through authentication, hybrid AD topology, or Conditional Access policy |
| MUJ says MFA is mandatory [25] | The documented onboarding process requires MFA setup | Enrollment likely has broad operational importance | Enforcement coverage, exclusions, authentication strength, guest policy, or admin policy |
| Autodiscover CNAMEs resolve to Outlook [32][33] | Exchange clients can discover Microsoft's Outlook service | Mail and identity surfaces can be correlated during reconnaissance | Whether any particular mailbox exists |
| DMARC strings are `p=none` at observed policy points [34][8] | Published policies are monitoring-oriented | Stronger staged enforcement may reduce spoofing opportunities | Alignment pass rates, legitimate sender inventory, or readiness for `quarantine` or `reject` |

**Decision-ready insight:** the important exposure is not that public metadata exists. The important issue is whether two tenants apply equally strong identity controls after that metadata lets an observer map the environment accurately.

## 2. Two OIDC GUIDs Reveal a Split Identity Boundary

The strongest finding is the existence of two distinct Entra tenant identifiers. The domain-specific OIDC discovery URL for `jaipur.manipal.edu` resolves to issuer `https://login.microsoftonline.com/7d0726e8-bf4b-4ac1-99f1-010fb11f1d3f/v2.0`, while the equivalent URL for `muj.manipal.edu` resolves to issuer `https://login.microsoftonline.com/27282fdd-4c0b-4dfb-ba91-228cd83fdf71/v2.0` [5][3]. Both documents publish tenant-specific authorization, token, and JWKS endpoints and identify the tenant region scope as `AS` [5][3].

### Exact tenant-discovery table

| Input domain | Exact public discovery URL | Exact tenant GUID | Exact issuer | Region |
|---|---|---|---|---|
| `jaipur.manipal.edu` | `https://login.microsoftonline.com/jaipur.manipal.edu/v2.0/.well-known/openid-configuration` | `7d0726e8-bf4b-4ac1-99f1-010fb11f1d3f` | `https://login.microsoftonline.com/7d0726e8-bf4b-4ac1-99f1-010fb11f1d3f/v2.0` | `AS` [5] |
| `muj.manipal.edu` | `https://login.microsoftonline.com/muj.manipal.edu/v2.0/.well-known/openid-configuration` | `27282fdd-4c0b-4dfb-ba91-228cd83fdf71` | `https://login.microsoftonline.com/27282fdd-4c0b-4dfb-ba91-228cd83fdf71/v2.0` | `AS` [3] |

This is definitive domain-to-tenant mapping because the GUID is embedded consistently in each document's issuer, token, authorization, and key endpoints [5][3]. It does not disclose credentials, policy objects, group membership, licenses, users, or secrets.

The mail-signing records independently support the split. DKIM selectors for `jaipur.manipal.edu` alias into `mujcampus.onmicrosoft.com`, while selectors for `muj.manipal.edu` alias into `mujmanipal.onmicrosoft.com` [28][29][30][31]. Those names are not the canonical tenant GUIDs, but their divergence corroborates separate Microsoft 365 namespaces.

The application pages connect this identity split directly to SLCM. `muj.slcm.jaipur.manipal.edu` displays the suffix `@jaipur.manipal.edu` [22], whereas the prompt's target, `mujslcm.jaipur.manipal.edu`, displays `@muj.manipal.edu` [23]. **Inference:** this could represent phased migration, cohort segmentation, or a legacy and current portal pair. Public evidence does not distinguish among those scenarios, so none should be reported as fact.

### Case study: one ecosystem, two control planes

Consider an administrator who secures the `muj.manipal.edu` tenant with phishing-resistant MFA but assumes the similarly branded `jaipur.manipal.edu` identities inherit the same policy. They do not: the GUIDs identify separate Entra policy boundaries. Conditional Access, authentication-method policy, emergency accounts, guest settings, SSPR scope, logging, applications, and privileged roles must be reviewed separately.

The mechanism is governance duplication. Every policy change has two opportunities for omission, and the similar university branding can hide that divergence from help-desk staff and users. The practical recommendation is a two-column control inventory keyed by the exact GUIDs above, not by informal labels such as "old" and "new" tenant.

**Decision-ready insight:** tenant ID disclosure is a low-severity standards behavior; discovering that there are two independently governed tenants is a high-value defensive finding.

## 3. Managed Realms and Federation Metadata: What It Proves

Microsoft's public user-realm responses classify test identities in both domains as `Managed` and return `Manipal University Jaipur` as the organization name [20][21]. This supports a managed Microsoft identity route for both domains. It does not reveal whether either tenant synchronizes users from on-premises Active Directory or uses password-hash synchronization, pass-through authentication, or cloud-only accounts.

The federation-metadata URLs also resolve for both domains. Their entity IDs and passive sign-in endpoints are tenant-specific Microsoft STS and WS-Federation values [2][4].

| Domain | Realm result | Federation metadata entity ID | Passive WS-Fed endpoint | Interpretation |
|---|---|---|---|---|
| `jaipur.manipal.edu` | `Managed`; organization `Manipal University Jaipur` [20] | `https://sts.windows.net/7d0726e8-bf4b-4ac1-99f1-010fb11f1d3f/` [2] | `https://login.microsoftonline.com/7d0726e8-bf4b-4ac1-99f1-010fb11f1d3f/wsfed` [2] | Microsoft STS metadata, not proof of third-party federation |
| `muj.manipal.edu` | `Managed`; organization `Manipal University Jaipur` [21] | `https://sts.windows.net/27282fdd-4c0b-4dfb-ba91-228cd83fdf71/` [4] | `https://login.microsoftonline.com/27282fdd-4c0b-4dfb-ba91-228cd83fdf71/wsfed` [4] | Microsoft STS metadata, not proof of third-party federation |

A common analytical error is to treat successful retrieval from a path named `federationmetadata` as evidence that a university federates authentication to ADFS, Shibboleth, or another external provider. That conclusion is not supported here. The observed metadata describes Microsoft's own STS endpoints, while the separate realm evidence explicitly says `Managed` [20][21][2][4].

**Inference:** a future change from `Managed` to a federated realm would materially alter the threat model because availability and authentication controls could depend on another identity provider. No such change is shown by the current evidence.

**Decision-ready insight:** record the realm status as a monitored configuration fact. Do not report external federation as a finding unless a public realm response or owner-supplied tenant configuration actually identifies it.

## 4. GetCredentialType: Platform Pattern, MUJ Status Unknown

Security-testing literature describes the Microsoft 365 `GetCredentialType` route as capable of distinguishing supplied accounts in an Azure tenancy [24]. Microsoft, however, describes it as an internal credential-discovery endpoint rather than a documented onboarding decision API, warns that its inference does not guarantee how a user will actually authenticate, and advises against dynamically deciding between guest invitations and local accounts from its result [18].

That distinction matters. An internal sign-in-routing function can still create an enumeration signal, but its output is not an authoritative directory API. Guest identities, alternate sign-in identifiers, changing home realms, consumer accounts, and invitation redemption can create ambiguous results. Accordingly, this report does not equate a response difference with proof of a mailbox, active enrollment, or current authorization.

### Exact enumeration assessment

| Enumeration layer | MUJ status | Evidence | Security meaning | Confidence |
|---|---|---|---|---|
| Domain existence | Confirmed | Public DNS and MUJ pages [26][22][23][27] | An observer can identify valid university namespaces | High |
| Tenant GUID mapping | Confirmed | Domain-specific OIDC documents [5][3] | An observer can target tenant-aware Microsoft URLs and correlate telemetry | High |
| Managed versus federated realm | Confirmed as `Managed` | Microsoft realm responses [20][21] | Home-realm routing is externally observable | High |
| Per-user `GetCredentialType` differentiation | Not tested | General platform literature only [24][18] | Potential username-enumeration signal, but no MUJ-specific result | Low for MUJ posture |
| Mailbox existence through Autodiscover | Not established | DNS only points to Outlook [32][33] | Service presence does not prove a mailbox | High confidence in the limitation |
| SSPR account existence signal | Not tested | Public SSPR documentation only [9] | No conclusion about user-specific behavior | High confidence in the limitation |

No real student, employee, or administrator identifier should be entered into `GetCredentialType` by a club member without written authorization. An owner-approved validation, if MUJ chooses to conduct one, should use institution-created synthetic canary identities, a documented rate limit, and a narrow comparison against a reserved nonexistent identity. This report intentionally omits payloads, scripts, automation, and response-parsing instructions.

The control objective is not to make the tenant GUID secret. It is to make a discovered username insufficient for compromise. Smart Lockout is designed to distinguish valid-user activity from attacker guessing and defaults in Azure Public to lockout after ten failed attempts, initially for one minute with longer periods after subsequent attempts [13]. Microsoft also notes separate counters for familiar and unfamiliar locations [13]. These controls should be reviewed in each tenant, but the public evidence does not expose MUJ's effective lockout settings.

**Decision-ready insight:** report tenant enumeration as confirmed, account enumeration as a plausible platform risk, and MUJ-specific `GetCredentialType` exposure as unknown. Anything stronger would exceed the evidence.

## 5. SSPR and MFA: Enrollment Does Not Prove Enforcement

MUJ's Office 365 setup SOP is unusually useful public evidence. It directs users to Microsoft's login portal, asks for a university mail ID and temporary or current password, and then requires a password change [25]. It states that MFA is mandatory and must be completed before Office 365 can be used [25]. A companion section tells users how to add or change security-information methods through their Microsoft account [25].

The setup process documents phone verification by SMS OTP and a personal-email verification step [25]. Those facts establish intended enrollment options. They do not expose the Entra administrator settings that determine which populations have SSPR, how many methods are required, whether administrators face stronger requirements, or whether legacy and guest accounts are covered.

### Exact public MFA and SSPR evidence

| Question | Public evidence | What can be concluded | What remains unknown |
|---|---|---|---|
| Is MFA part of MUJ onboarding? | SOP says MFA is mandatory before Office 365 use [25] | Yes, as documented procedure | Enforcement success rate and exclusions |
| Can users manage security information? | SOP directs users to `View Account` and `Security Info` [25] | Yes, as documented procedure | Whether risky changes trigger alerts or reauthentication |
| Is phone supported? | SOP documents SMS OTP phone verification [25] | Phone is an offered registration method | Whether voice is enabled or whether phone is allowed for privileged roles |
| Is personal email collected? | SOP documents personal-email verification [25] | Personal email is an offered security-information method | Whether it is enabled for SSPR, qualified sign-in, or another recovery workflow |
| Is SSPR enabled for all users? | No public tenant policy found | No conclusion | Enabled scope, exclusions, and license-dependent features |
| How many SSPR methods are required? | Not publicly disclosed | No conclusion | One versus two methods and method combinations |
| Are administrators phishing-resistant? | Not publicly disclosed | No conclusion | Authentication-strength and Conditional Access policy |

Microsoft's SSPR documentation says enabled users must register at least one authentication method [9]. It lists Authenticator push, OATH tokens, SMS, voice, and email OTP among available SSPR methods [9]. Microsoft's current method overview distinguishes capabilities: email OTP is not ordinary primary authentication and is associated with SSPR and qualified sign-in; SMS and Authenticator push can support MFA and SSPR; FIDO2 passkeys support primary authentication and MFA but are not listed there as an SSPR recovery method [14].

**Inference:** the MUJ SOP's placement of phone and personal email within an MFA setup section may simplify the user experience by grouping security-information registration under one label. It should not be interpreted as proof that every listed method independently satisfies a strong MFA policy.

### Common university MFA gaps to audit, not confirmed MUJ findings

The following are control hypotheses for owner review. They are not claims about MUJ or Indian universities as a class.

| Audit hypothesis | Why it matters | Public MUJ evidence | Recommended owner-side test | Current MUJ status |
|---|---|---|---|---|
| Enrollment without universal enforcement | A registered method provides no protection if some applications, users, or authentication paths do not require it | Mandatory enrollment is documented [25] | Compare Conditional Access coverage across all users, guests, applications, and both tenants | Unknown |
| Phishable factors remain dominant | Standard push can be vulnerable to push bombing; SMS and voice are vulnerable to phishing, SS7, and SIM-swap attacks [19] | Phone and Authenticator are offered [25] | Measure active-method distribution and migrate high-impact roles to phishing-resistant methods | Unknown |
| Privileged users use the same strength as students | Administrator compromise has a larger blast radius | No public admin policy | Require Microsoft's phishing-resistant authentication strength for privileged roles after registration testing [11][6] | Unknown |
| Two-tenant policy drift | Independent GUIDs mean independent policy objects [5][3] | Two tenants are confirmed | Export and compare Conditional Access, authentication methods, SSPR, guest, and role policies by GUID | Plausible inference, not confirmed drift |
| Weak recovery undermines strong sign-in | Recovery methods can become the easiest route back into an account | Phone and personal email registration are documented [25] | Review SSPR scope, required-method count, stale recovery contacts, and help-desk reset controls | Unknown |
| Legacy or special flows escape the intended policy | Microsoft provides report-only deployment for blocking legacy authentication and controls for device-code and authentication-transfer flows [7][12] | No public setting | Review sign-in logs, deploy report-only policy, remediate dependencies, then enforce | Unknown |
| Emergency access depends on normal federation or normal devices | A broad policy error can lock administrators out | No public evidence | Maintain at least two monitored, cloud-only emergency accounts and test them at least every 90 days [17] | Unknown |

Microsoft's built-in phishing-resistant authentication strength includes FIDO2 security keys, Windows Hello for Business or platform credentials, and multifactor certificate-based authentication [11]. CISA similarly identifies FIDO/WebAuthn and PKI-based approaches as phishing-resistant and calls this class the gold standard [19]. The transition should be staged because Microsoft warns that requiring phishing-resistant MFA before administrators register suitable methods can lock administrators out [6].

**Decision-ready insight:** MUJ has public evidence of MFA intent, which is positive. The unanswered security question is whether every important identity and flow in both tenants is actually held to an appropriate authentication strength.

## 6. Exchange Online and Autodiscover: Normal Metadata, Recon Context

The two domains' mail records consistently identify Microsoft 365. The `muj.manipal.edu` MX points to `muj-manipal-edu.mail.protection.outlook.com`, while `jaipur.manipal.edu` points to `jaipur-manipal-edu.mail.protection.outlook.com` [26][27]. `muj.manipal.edu` publishes SPF authorization through `spf.protection.outlook.com` with `-all` [36]. `jaipur.manipal.edu` also publishes an SPF record authorizing Microsoft and Brightspace senders [37].

Both Autodiscover hostnames are CNAMEs to `autodiscover.outlook.com` [32][33]. Microsoft describes Autodiscover as a service that minimizes configuration and deployment work by giving clients access to Exchange features [38]. A DNS pointer to this service confirms the platform, not any individual mailbox.

### Exact mail-discovery table

| Control | `jaipur.manipal.edu` | `muj.manipal.edu` | Defensive interpretation |
|---|---|---|---|
| MX | `0 jaipur-manipal-edu.mail.protection.outlook.com.` [27] | `0 muj-manipal-edu.mail.protection.outlook.com.` [26] | Exchange Online protection is publicly identifiable |
| SPF | Includes `spf.protection.outlook.com` and Brightspace authorization [37] | `v=spf1 include:spf.protection.outlook.com -all` [36] | Sender authorization is published; alignment and all approved senders still need owner review |
| DKIM namespace | `mujcampus.onmicrosoft.com` through selector CNAMEs [30][31] | `mujmanipal.onmicrosoft.com` through selector CNAMEs [28][29] | Corroborates distinct Microsoft 365 namespaces |
| Autodiscover | `autodiscover.outlook.com.` [32] | `autodiscover.outlook.com.` [33] | Normal client discovery; no mailbox existence conclusion |
| Child DMARC | `v=DMARC1; p=none; rua=mailto:dmarc@jaipur.manipal.edu` [34] | No child record in the observed lookup [35] | Jaipur collects reports without requesting enforcement; MUJ depends on applicable parent behavior |
| Parent DMARC | `manipal.edu` publishes `p=none` [8] | Same organizational parent [8] | Observed parent policy is monitoring-oriented |

**Inference:** because both observed DMARC policy points use `p=none`, spoofed-message handling depends heavily on recipient filtering rather than a sender-domain request for quarantine or rejection. Before changing policy, MUJ should inventory legitimate senders, analyze aggregate reports, repair SPF or DKIM alignment, then stage enforcement. Moving directly to rejection without sender inventory could disrupt university, learning-platform, admissions, and bulk-mail workflows.

Autodiscover should not be "fixed" by removing a required Exchange Online CNAME. The appropriate response is to ensure that knowledge of the mail platform and possible username format does not lead to account compromise: strong authentication, risk-aware access, secure recovery, monitored emergency accounts, and prompt incident response.

**Decision-ready insight:** Exchange Online metadata is coherent and expected. DMARC enforcement and identity strength offer more defensive value than trying to conceal Autodiscover.

## 7. Indian Higher-Education Threat Context Without Stereotyping

Seqrite's India Cyber Threat Report 2026 covers October 2024 through September 2025 and says its telemetry recorded **265.52M detections** across more than **8M endpoints** in India [15]. Within that telemetry, Education and Training recorded **4.92M detections**, or **18.45%** [15]. The report associates the sector's observed malware with credential theft, coin mining, and data exfiltration campaigns across universities and training institutions [15].

Those are vendor-telemetry detections, not a census of Indian institutions. Seqrite states that its information comes from sources it believes reliable but disclaims warranties concerning completeness and accuracy [15]. The figures therefore justify prioritizing education-sector controls, but they do not measure MUJ compromise, Entra configuration, MFA adoption, or per-tenant weakness.

CERT-In's 2023 annual report provides broader national context. It records **1,592,917** handled incidents, including **869 phishing**, **447,720 unauthorized scanning or probing**, **941,592 vulnerable-service**, **184,131 malicious-code**, **10,665 website-defacement**, and **1,045 website-intrusion or malware-propagation** incidents [16]. CERT-In's constituency covers Indian cyberspace across government, private, public, and individual users [16], so those numbers likewise cannot be narrowed to universities or Microsoft tenants.

| Context source | Exact population or period | Exact result | What it supports | What it does not support |
|---|---|---|---|---|
| Seqrite India Cyber Threat Report 2026 | Oct 2024-Sep 2025; more than 8M endpoints [15] | 265.52M total detections; Education and Training 4.92M or 18.45% [15] | Education is a meaningful threat-prioritization category in the vendor's telemetry | MUJ compromise, MFA-gap prevalence, or a count of affected universities |
| CERT-In Annual Report 2023 | Indian cyberspace and CERT-In constituency [16] | 1,592,917 handled incidents across stated categories [16] | Phishing, probing, vulnerable services, and malware are relevant national incident classes | Education-only or Entra-only risk rates |
| MUJ Office 365 SOP | MUJ student and employee onboarding workflow | MFA described as mandatory [25] | MUJ has documented MFA intent | Technical enforcement and effectiveness |

The phrase "typical MFA gaps in Indian university tenants" should therefore be interpreted as a defensive checklist, not a statistical claim. The available public evidence supports high threat exposure and identifies widely recognized MFA failure modes. It does not support stating that Indian universities commonly disable MFA, commonly use SMS, or commonly misconfigure SSPR. This report avoids those unsupported generalizations.

**Decision-ready insight:** use Indian sector telemetry to justify urgency, but derive the MUJ verdict only from MUJ and Microsoft evidence.

## 8. Prioritized Defensive Validation Plan

All activities below are intended for MUJ's tenant owners or a team operating under written authorization. Security-club members should restrict themselves to passive public evidence unless the university formally defines scope, test identities, rate limits, logging, and emergency contacts.

| Priority | Owner action | Exact scope | Success evidence | Why now |
|---|---|---|---|---|
| P0 | Establish dual-tenant ownership | GUID `7d0726e8-bf4b-4ac1-99f1-010fb11f1d3f` and GUID `27282fdd-4c0b-4dfb-ba91-228cd83fdf71` [5][3] | Named owner, security contact, billing contact, incident lead, and policy baseline for each tenant | Prevents similar branding from hiding different control planes |
| P0 | Protect privileged roles with phishing-resistant authentication | Global Administrator, Privileged Role Administrator, Security Administrator, Exchange Administrator, application owners, and emergency operators | Conditional Access authentication-strength policy plus tested registered methods | Microsoft supports a phishing-resistant strength [11] and warns to register methods before enforcement [6] |
| P0 | Create and monitor emergency access | At least two cloud-only `.onmicrosoft.com` emergency accounts per applicable design | Successful quarterly or 90-day test and alerts on every use | Microsoft recommends redundant cloud-only accounts, monitoring, and regular tests [17] |
| P0 | Compare policy coverage across tenants | Conditional Access, authentication methods, SSPR, guests, legacy flows, device code, applications, service principals, and privileged roles | Signed exception list and zero unexplained gaps | Separate tenant GUIDs imply separate policy review |
| P1 | Validate MFA and SSPR with synthetic canaries | University-created student, employee, guest, administrator, disabled, and recovery-state test accounts | Expected challenges and recovery outcomes captured in an approved test record | Converts public documentation into configuration assurance without touching real users |
| P1 | Review legacy and special authentication flows | Legacy clients, device-code flow, authentication transfer, and noninteractive sign-ins | Report-only impact assessment followed by controlled enforcement | Microsoft recommends starting legacy-auth blocking in report-only mode [7] and provides controls for special flows [12] |
| P1 | Improve factor strength | Measure SMS, voice, standard push, number-matching push, FIDO2, platform credential, and certificate usage | Declining phishable-factor share, beginning with admins and help desk | CISA identifies SMS and voice as last-resort methods [19] |
| P1 | Harden recovery | SSPR scope, required-method count, stale phone and email contacts, help-desk reset, risky security-info changes | Two-method recovery where appropriate, alerts, and documented exception process | Public evidence does not reveal MUJ's actual SSPR policy |
| P1 | Stage DMARC enforcement | `jaipur.manipal.edu`, `muj.manipal.edu`, and applicable parent policy | High SPF/DKIM alignment followed by staged `quarantine` and `reject` decisions | Current public policy strings are `p=none` or rely on a `p=none` parent |
| P2 | Tune detection and response | Failed sign-ins, password spray, unfamiliar locations, risky sign-ins, SSPR changes, privileged operations, emergency accounts | Tested alerts and incident playbooks correlated across both tenants | Smart Lockout and emergency-account monitoring address different parts of the attack chain [13][17] |
| P2 | Clarify portal and domain lifecycle | Both SLCM URLs and both mail suffixes | User-facing canonical login guidance and retirement criteria for legacy paths | The public portals currently advertise different suffixes [22][23] |

The club can contribute without active probing by maintaining the passive evidence inventory, tracking unexpected changes to OIDC issuers, realm type, MX, DKIM, Autodiscover, and DMARC, and escalating differences through a university-approved disclosure channel. It should not build lists of likely students, submit bulk identity checks, or attempt to prove mailbox existence.

**Decision-ready insight:** the shortest path to material risk reduction is not another enumeration test. It is a two-tenant policy comparison followed by phishing-resistant protection for privileged identities and verified recovery controls.

## 9. Synthesis

The evidence describes three related but different exposure classes: standards-based discovery, possible identity enumeration, and control-policy uncertainty. Treating them as one issue would produce the wrong priorities.

| Dimension | Standards discovery | Per-user enumeration | MFA and recovery posture |
|---|---|---|---|
| Mechanism | Public OIDC, realm, DNS, federation metadata, and Autodiscover | Pre-authentication routing or recovery behavior that may differ by identity | Tenant-admin policies and user registrations |
| MUJ evidence | Strong: two GUIDs, managed realms, Outlook mail, two DKIM namespaces | Limited: general `GetCredentialType` pattern, no MUJ user test [24][18] | Partial: mandatory enrollment SOP, no public enforcement configuration [25] |
| Attacker value | Maps the environment and improves targeting | May reduce the cost of building a candidate list | Determines whether a discovered account can actually be compromised |
| Defensive mechanism | Accept necessary disclosure; monitor unexpected metadata changes | Strong authentication, lockout, risk detection, and authorized canary validation | Conditional Access, authentication strength, secure SSPR, lifecycle controls, emergency access |
| Main trade-off | Interoperability requires public metadata | Aggressive testing can become unauthorized account probing | Strong policy can create lockout or support burden if rollout is poor [6] |
| Time horizon | Continuous passive monitoring | Validate only during authorized assessment | Immediate baseline, then staged improvement |

The non-obvious tension is that MUJ's positive MFA documentation coexists with unresolved strength and coverage questions. Mandatory setup reduces risk only if the requirement applies to every important application and identity. A tenant can report full registration while privileged users still rely on phishable methods, legacy flows remain, recovery contacts are stale, or a second tenant has weaker policy. None of those gaps is proven here, but the dual-tenant architecture makes each worth checking.

A second tension concerns discovery. OIDC metadata, federation metadata, MX, DKIM, and Autodiscover reveal a great deal, yet much of that disclosure is required for standards and mail interoperability [1][38]. Trying to hide it is less effective than ensuring the exposed map leads to hardened controls. The presence of two tenant GUIDs is therefore not itself a vulnerability; it is a precise key for organizing a defensive audit.

A third tension is between usability and phishing resistance. MUJ's documented phone and personal-email onboarding methods can reduce help-desk friction [25], but Microsoft and CISA distinguish method capability and strength [14][11][19]. The right design need not force every student into the same high-assurance method immediately. It should first protect administrators, help-desk personnel, finance, application owners, and other high-impact accounts, while maintaining tested recovery and emergency paths.

The holistic conclusion is that public reconnaissance is mature enough to map MUJ's identity perimeter, but not enough to judge its internal enforcement. The most responsible next step is owner-side configuration evidence, not more aggressive public probing.

## VERDICT

**Overall verdict: MODERATE identity-governance concern, with HIGH confidence in the external architecture and MEDIUM confidence in the risk rating.**

Two separate Microsoft Entra tenants are conclusively associated with the MUJ SLCM identity ecosystem: `7d0726e8-bf4b-4ac1-99f1-010fb11f1d3f` for `jaipur.manipal.edu` and `27282fdd-4c0b-4dfb-ba91-228cd83fdf71` for `muj.manipal.edu` [5][3]. Both are publicly classified as managed realms [20][21]. The target portal `mujslcm.jaipur.manipal.edu` advertises `@muj.manipal.edu`, while another public SLCM portal advertises `@jaipur.manipal.edu` [22][23]. The external Exchange Online and Autodiscover footprint is also confirmed [26][27][32][33].

The observed OIDC and federation metadata disclosures are normal Microsoft standards behavior, not vulnerabilities by themselves [2][4][1]. The security significance comes from the confirmed two-tenant boundary and the resulting possibility of inconsistent controls. That possibility is an **inference**, not a demonstrated misconfiguration.

MUJ has strong positive public evidence of intended MFA enrollment: its SOP calls MFA mandatory [25]. Public evidence does not establish Conditional Access coverage, phishing-resistant administrator authentication, SSPR scope, recovery-method count, legacy-auth state, guest controls, emergency access, or MUJ-specific `GetCredentialType` behavior. Those items remain **unknown**, not failed.

The mail posture deserves separate attention because the observed DMARC records are monitoring-oriented rather than enforcement-oriented. This does not prove successful spoofing, but it supports a controlled alignment and enforcement project.

### Confidence table

| Conclusion | Confidence | Basis |
|---|---|---|
| Two distinct Entra tenant GUIDs | **High** | Direct Microsoft OIDC metadata [5][3] |
| Both domains are managed realms | **High** | Direct Microsoft realm responses [20][21] |
| SLCM ecosystem presents both suffixes | **High** | Public portal content [22][23] |
| Exchange Online and Autodiscover are used | **High** | MX and CNAME records [26][27][32][33] |
| MUJ documents mandatory MFA enrollment | **High** | First-party MUJ SOP [25] |
| Actual MFA and SSPR strength | **Low** | No public tenant-policy evidence |
| MUJ per-user `GetCredentialType` exposure | **Low** | Deliberately untested; only general platform evidence [24][18] |
| Cross-tenant policy drift risk | **Medium** | Strong architectural basis, but drift itself is unverified |
| Overall moderate concern | **Medium** | Combines confirmed dual governance with major internal-policy unknowns |

**Final action:** MUJ should run an owner-authorized, GUID-keyed comparison of both tenants, protect privileged roles with phishing-resistant authentication, verify SSPR and special-flow controls with synthetic identities, maintain monitored cloud-only emergency access, and stage DMARC enforcement after sender-alignment analysis. The university security club should continue passive monitoring and coordinated disclosure only.

## References

1. *OpenID Connect on the Microsoft identity platform*. https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols-oidc
2. *login.microsoftonline.com*. https://login.microsoftonline.com/jaipur.manipal.edu/federationmetadata/2007-06/federationmetadata.xml
3. *Openid Configuration*. https://login.microsoftonline.com/muj.manipal.edu/v2.0/.well-known/openid-configuration
4. *login.microsoftonline.com*. https://login.microsoftonline.com/muj.manipal.edu/federationmetadata/2007-06/federationmetadata.xml
5. *Openid Configuration*. https://login.microsoftonline.com/jaipur.manipal.edu/v2.0/.well-known/openid-configuration
6. *Require phishing-resistant multifactor authentication for ...*. https://learn.microsoft.com/en-us/entra/identity/conditional-access/policy-admin-phish-resistant-mfa
7. *Block legacy authentication with Conditional Access ...*. https://learn.microsoft.com/en-us/entra/identity/conditional-access/policy-block-legacy-authentication
8. *dns.google*. https://dns.google/resolve?name=_dmarc.manipal.edu&type=TXT
9. *Self-service password reset deep dive - Microsoft Entra ID*. https://learn.microsoft.com/en-us/entra/identity/authentication/concept-sspr-howitworks
10. *Microsoft Entra Conditional Access: Zero Trust Policy Engine*. https://learn.microsoft.com/en-us/entra/identity/conditional-access/overview
11. *Overview of Conditional Access Authentication Strengths - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/authentication/concept-authentication-strengths
12. *Block authentication flows with Conditional Access policy*. https://learn.microsoft.com/en-us/entra/identity/conditional-access/policy-block-authentication-flows
13. *Prevent Attacks Using Smart Lockout - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/authentication/howto-password-smart-lockout
14. *Microsoft Entra authentication overview - Microsoft Entra ID | Microsoft Learn*. http://learn.microsoft.com/en-us/entra/identity/authentication/overview-authentication
15. *India Cyber Threat Report 2026*. https://www.seqrite.com/documents/en/threat-reports/india-cyber-threat-report-2026.pdf
16. *cert-in.org.in*. http://cert-in.org.in/Downloader?fileName=ANUAL-2024-0001.pdf&pageid=22&type=2
17. *Manage emergency access admin accounts - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/security-emergency-access
18. *AADSTS500208 Error when user tries to login, I am using Microsoft Entra ID (Azure AD) with MSAL authentication for my web application. - Microsoft Q&A*. https://learn.microsoft.com/en-us/answers/questions/5879849/aadsts500208-error-when-user-tries-to-login-i-am-u
19. *Implementing Phishing-Resistant MFA*. https://www.cisa.gov/sites/default/files/publications/fact-sheet-implementing-phishing-resistant-mfa-508c.pdf
20. *http://login.microsoftonline.com/getuserrealm.srf?login=probe@jaipur.manipal.edu&xml=1*. http://login.microsoftonline.com/getuserrealm.srf?login=probe@jaipur.manipal.edu&xml=1
21. *http://login.microsoftonline.com/getuserrealm.srf?login=probe@muj.manipal.edu&xml=1*. http://login.microsoftonline.com/getuserrealm.srf?login=probe@muj.manipal.edu&xml=1
22. *http://muj.slcm.jaipur.manipal.edu/*. http://muj.slcm.jaipur.manipal.edu/
23. *http://mujslcm.jaipur.manipal.edu/*. http://mujslcm.jaipur.manipal.edu/
24. *Username Enumeration | Jacob Larsen*. https://larsencyber.com/docs/enpt/1.-enumeration/2.-active/user-enum
25. *http://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf*. http://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf
26. *http://dns.google/resolve?name=muj.manipal.edu&type=MX*. http://dns.google/resolve?name=muj.manipal.edu&type=MX
27. *http://dns.google/resolve?name=jaipur.manipal.edu&type=MX*. http://dns.google/resolve?name=jaipur.manipal.edu&type=MX
28. *http://dns.google/resolve?name=selector1._domainkey.muj.manipal.edu&type=CNAME*. http://dns.google/resolve?name=selector1._domainkey.muj.manipal.edu&type=CNAME
29. *http://dns.google/resolve?name=selector2._domainkey.muj.manipal.edu&type=CNAME*. http://dns.google/resolve?name=selector2._domainkey.muj.manipal.edu&type=CNAME
30. *http://dns.google/resolve?name=selector1._domainkey.jaipur.manipal.edu&type=CNAME*. http://dns.google/resolve?name=selector1._domainkey.jaipur.manipal.edu&type=CNAME
31. *http://dns.google/resolve?name=selector2._domainkey.jaipur.manipal.edu&type=CNAME*. http://dns.google/resolve?name=selector2._domainkey.jaipur.manipal.edu&type=CNAME
32. *dns.google*. https://dns.google/resolve?name=autodiscover.jaipur.manipal.edu&type=CNAME
33. *dns.google*. https://dns.google/resolve?name=autodiscover.muj.manipal.edu&type=CNAME
34. *dns.google*. https://dns.google/resolve?name=_dmarc.jaipur.manipal.edu&type=TXT
35. *dns.google*. https://dns.google/resolve?name=_dmarc.muj.manipal.edu&type=TXT
36. *http://dns.google/resolve?name=muj.manipal.edu&type=TXT*. http://dns.google/resolve?name=muj.manipal.edu&type=TXT
37. *http://dns.google/resolve?name=jaipur.manipal.edu&type=TXT*. http://dns.google/resolve?name=jaipur.manipal.edu&type=TXT
38. *Autodiscover service in Exchange Server - Microsoft Learn*. https://learn.microsoft.com/en-us/exchange/architecture/client-access/autodiscover
