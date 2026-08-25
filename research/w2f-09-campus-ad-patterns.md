# MUJ SLCM Identity Risk: Evidence, Inference, and Controls

## Executive Summary

- **Shared Credential Is A Risk Premise, Not An Architecture Finding**: The research brief reports an MUJ FAQ statement that the Outlook password equals the SLCM password, but no citable public copy of that FAQ was recovered. The public portal does show the `@muj.manipal.edu` suffix, Parent Login, Student Login, and Forgot Password text [10]. -> Treat credential equivalence as a high-priority claim for administrative confirmation, not as proof of Password Hash Synchronization (PHS), federation, or a common password database.

- **One Password Does Not Necessarily Mean Password Reuse**: Microsoft PHS can let a user employ the same on-premises password for Microsoft 365 without storing a clear-text or reversibly encrypted password in Entra ID [12]. Pass-through Authentication (PTA) instead validates cloud sign-ins directly against on-premises Active Directory [13]. -> Determine where each sign-in is validated before describing MUJ's design or risk.

- **SSO And Password Parity Are Different**: Microsoft documents SAML enterprise-application SSO in which users authenticate with Entra credentials [2], while PHS merely makes an on-premises password usable for Entra sign-in [5]. -> Ask whether SLCM consumes an Entra-issued token or separately receives a password. This distinction controls the security conclusion.

- **MFA Coverage, Not Microsoft 365 Presence, Is Decisive**: Every Microsoft 365 tenant is an Entra tenant [27], but that fact does not prove which MFA policy is active. Security Defaults requires all users to register, requires administrators to perform MFA at every sign-in, applies MFA to privileged Azure resources, and prompts ordinary users when Microsoft deems it necessary [4]. -> Obtain tenant-side policy and sign-in evidence rather than testing public accounts.

- **Legacy Paths Can Defeat A Cloud-Only Control Strategy**: Microsoft states that legacy authentication does not support MFA and recommends blocking it; its documentation says more than 97% of credential-stuffing attacks and more than 99% of password-spray attacks use legacy authentication protocols [14]. -> Verify that Exchange legacy protocols, SLCM local login paths, service identities, and recovery paths are either blocked, separately protected, or deliberately risk-accepted.

- **A Shared Credential Expands Conditional Blast Radius**: CISA explains that MFA limits compromise because a stolen first credential alone cannot satisfy the second requirement [19]. **Inference:** if the same password is accepted independently by Outlook and SLCM, theft of that password can expose both mail and ERP unless both authentication paths enforce equivalent controls. -> Require MFA at the identity provider and remove or compensate for any password-only application path.

- **The Exact MUJ Stack Remains A Scope Assumption**: The brief labels the portal as ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10 behind Akamai. The citable first-party page establishes the portal and its login audiences but does not identify those implementation versions [9]. -> Use the versions as internal asset-inventory leads only; obtain server, deployment, and edge configuration records before making patch or exposure claims.

- **Administrator Evidence Can Resolve The Key Questions Safely**: Entra Connect configuration, domain federation status, enterprise-application records, Conditional Access policies, authentication-method reports, and aggregated sign-in logs can distinguish PHS, PTA, federation, and MFA coverage. -> The club should submit a defensive evidence request to authorized administrators, not probe accounts, credentials, reset flows, or origin infrastructure.

- **Incident Readiness Must Span Both Systems**: CISA recommends resetting affected credentials across enterprise services, updating passwords reused elsewhere, reviewing authentication logs, and enforcing phishing-resistant MFA [21]. CERT-In directions require covered entities to report specified incidents within six hours and retain ICT logs securely in India for 180 days [22]. -> Build one identity incident playbook covering Microsoft 365, SLCM, parent access, and any on-premises directory.

## 1. Scope, Safety, and Evidence Standard

This report uses public information only and does not provide instructions for unauthorized testing. It does not attempt login, password reset, account enumeration, origin discovery, rate-limit testing, vulnerability scanning, or bypass validation. Any future technical validation must have written authorization, named test accounts, approved times, a stop condition, and an incident contact.

The requested explicit chain-of-thought cannot be supplied as private internal reasoning. Instead, the report provides an auditable analytical trace in the form **observation -> mechanism -> implication -> defensive action**. This exposes the basis of each conclusion without presenting hidden deliberation or operational intrusion guidance.

### Table 1. Evidence grading used throughout

| Grade | Meaning | Acceptable conclusion | MUJ example |
|---|---|---|---|
| A - Direct | First-party public evidence states or displays the fact | Report as observed, with scope limited to the page | The MUJ portal displays `@muj.manipal.edu`, Parent Login, Student Login, and Forgot Password [10] |
| B - Corroborated capability | Primary vendor or government documentation proves a mechanism generally | Explain what the mechanism can do, but not that MUJ uses it | Microsoft documents PHS, PTA, SAML SSO, Security Defaults, and Conditional Access [5][2][13][3] |
| C - Supplied premise | The research brief asserts the fact, but public evidence was not recovered | Analyze conditionally and request confirmation | `Outlook password = SLCM password`; ASP.NET MVC 5.3; IIS 10; Akamai |
| D - Inference | A conclusion logically follows only if stated conditions hold | Label every use as **Inference** | If Outlook and SLCM independently accept one password, compromise can cross application boundaries |
| Unknown | Public evidence cannot determine the fact | State unknown; do not guess | MUJ's PHS, PTA, federation, Conditional Access, and MFA status |

The central evidentiary rule is that a Microsoft-supported architecture is not evidence that MUJ deployed it. Likewise, a shared password is not evidence of SSO, PHS, or insecure duplication. This distinction prevents the most consequential OSINT error in this case: turning product capability into an institution-specific finding.

## 2. What The Public MUJ Surface Actually Establishes

The first-party portal publicly identifies itself as the MUJ portal and displays the institutional suffix `@muj.manipal.edu` [9]. Indexed public text also exposes Parent Login, Student Login, and Forgot Password choices [10]. Those observations support a narrow conclusion: the application presents more than one login audience and associates at least one user flow with an MUJ email-style identifier.

They do not reveal where a password is validated. Three buttons can route to three controllers in one application, three identity providers, or merely three user-interface modes. **Inference:** the parent option may have a different identity lifecycle because parents may not possess institutional Microsoft 365 identities, but the public labels do not establish that it uses a local password store. It would therefore be inaccurate to call Parent Login an MFA bypass without authorized configuration evidence.

The portal's public text also does not prove that SLCM redirects to Microsoft, consumes a SAML or OpenID Connect token, queries Active Directory, uses PTA, or validates a local database password. The Forgot Password destination is not included in the citable page text [10]. No public sign-in result can establish whether MFA would be required after a valid first factor because Conditional Access is evaluated after first-factor authentication [3]. Attempting to discover that behavior with an account would exceed passive OSINT unless expressly authorized.

### Table 2. MUJ-specific claims and present status

| Claim | Public evidence | Status | Safe conclusion |
|---|---|---|---|
| The portal exists at the named MUJ host | First-party portal page [9] | Verified | The host is a public MUJ login surface |
| Student identifiers use `@muj.manipal.edu` | The suffix is displayed [9][10] | Verified | At least one displayed login flow uses the MUJ suffix |
| Parent and student choices exist | Both labels are indexed [10] | Verified | Multiple login audiences are presented |
| Outlook password equals SLCM password | Stated in the research brief; citable FAQ copy not recovered | Supplied premise | Analyze conditionally and ask MUJ to produce the current FAQ or policy |
| Microsoft 365 identity is used | Stated in the brief; Microsoft confirms that Microsoft 365 subscriptions use Entra tenants generally [27] | Premise plus generic corroboration | Do not infer the SLCM integration method |
| Azure AD Connect PHS is deployed | No MUJ-specific public configuration evidence | Unknown | One of several plausible architectures |
| SLCM is federated to Entra | No MUJ-specific public federation evidence | Unknown | Plausible, not demonstrated |
| MFA is absent or present | No tenant policy or sign-in-log evidence | Unknown | Neither a vulnerability nor a control can be claimed |
| ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai | Supplied by the brief; not identified in citable first-party page text [9] | Unverified scope assumption | Confirm from authorized inventory and edge records |

### MUJ case study: why restraint changes the conclusion

Suppose the FAQ statement is current and users really enter one password into both Outlook and SLCM. A superficial assessment might call this "password reuse." That conclusion could be wrong. Microsoft PHS exists specifically to let a cloud user use the same password as on-premises Active Directory [5], while PTA validates the cloud sign-in directly against that directory [13]. Federation can instead remove the second password transaction entirely by letting an application accept an identity-provider token [2].

The correct finding is therefore conditional: **MUJ appears to promote credential parity, but the authority and protocol are unknown.** The security question is not simply whether the strings match. It is whether SLCM receives a reusable password, accepts a signed token, delegates validation to Active Directory, and enforces the same MFA and session policies as Microsoft 365.

## 3. Stack Claims Matter Less Than The Identity Boundary

The supplied ASP.NET MVC, .NET Framework, IIS, and Akamai labels may be useful to an authorized asset owner, but they should not drive a public vulnerability conclusion. The first-party text extracted from the login page does not state a framework, runtime, server, or edge version [9]. Banner-derived version precision can also be operationally misleading when an edge service normalizes responses or when libraries survive after a platform upgrade. **Inference:** an Akamai edge, if confirmed, would describe traffic delivery and protection, not the origin's authentication authority.

A federated ASP.NET application can still maintain its own authorization roles and session cookie after Entra authentication. Conversely, a locally authenticated application can sit behind a major edge provider without gaining Entra MFA. **Inference:** the security boundary is therefore the complete chain from first-factor authority through token validation, application authorization, session management, and recovery, rather than the product names visible at the HTTP layer.

### Table 3. Internal evidence needed to validate supplied stack labels

| Supplied label | Authorized evidence to request | Why it matters | Public-report treatment now |
|---|---|---|---|
| ASP.NET MVC 5.3 | Dependency manifest, deployment package inventory, software-composition report | Determines the actual supported library and patch state | Unverified premise |
| .NET Framework 4.x | Server feature inventory and application target framework | `4.x` is too broad for a patch conclusion | Unverified premise |
| IIS 10 | CMDB record, server build, patch compliance, and origin ownership | Separates web-server version from operating-system support state | Unverified premise |
| Akamai | DNS/CDN ownership record, property configuration, origin-access policy | Establishes edge coverage and whether origin access is constrained | Unverified premise |
| Microsoft 365 identity | Entra tenant record, verified domains, enterprise applications | Confirms the identity tenant and SLCM relationship | Generic Microsoft capability is known; MUJ design is unknown |

The security club should not attempt to validate versions by inducing errors or reaching an origin. The asset owner can resolve every row from inventory and configuration evidence without touching production user accounts.

## 4. Six Architectures Can Produce One Password Experience

Microsoft now calls the relevant synchronization product Microsoft Entra Connect, although "Azure AD Connect" remains common terminology. PHS synchronizes a hash of an on-premises Active Directory password to Entra ID and lets the user sign in to Microsoft 365 using the same password [5]. Microsoft states that passwords are not stored in clear text or with reversible encryption in Entra ID [12]. PHS typically needs the changed hash to synchronize before the new password works in the cloud; Microsoft documents a typical two-minute synchronization interval [12].

PTA produces a similar user experience through a different trust boundary. It validates the password directly against on-premises Active Directory, keeps the password out of cloud storage, and works with Conditional Access and MFA [13]. Password writeback addresses the opposite direction: Entra self-service password reset can synchronize a changed password back to on-premises Active Directory [15].

Federation changes the question from "where is the same password copied?" to "which identity provider issues the token?" Microsoft documents SAML SSO for an Entra enterprise application, after which users sign in with Entra credentials [2]. Microsoft also documents Application Proxy and partner integrations that can put SSO, MFA, and per-application Conditional Access in front of legacy on-premises applications [8].

### Table 4. Architecture alternatives behind the reported shared password

| Pattern | Password validation point | Why Outlook and SLCM can appear to share credentials | MFA control point | Availability or security trade-off | MUJ status |
|---|---|---|---|---|---|
| PHS plus SLCM using on-premises AD | Outlook at Entra; SLCM at AD | A derived password hash is synchronized to Entra, while SLCM uses the source directory [5] | Entra for Outlook; separate enforcement needed at SLCM unless federated | Cloud sign-in is highly available, but on-premises account-state changes are not immediate in the cloud [12] | Unknown |
| PTA plus SLCM using AD | Both ultimately validated against on-premises AD | PTA lets on-premises and cloud applications use the same password [13] | Entra Conditional Access can protect cloud sign-in [13]; SLCM still needs integration | Depends on on-premises authentication agents; additional agents provide availability [13] | Unknown |
| Entra SAML federation to SLCM | Entra authenticates; SLCM validates a signed assertion | User signs in with Entra credentials and SLCM need not receive a local password [2] | Entra Conditional Access before token issuance | Better centralized policy, but application authorization and sessions remain separate concerns | Unknown |
| Application Proxy or legacy-app partner integration | Entra fronts an on-premises application | SSO and MFA can protect a legacy application without a public direct login [8] | Entra per-application Conditional Access [8] | Connector and application compatibility must be managed | Unknown |
| Entra password writeback plus AD-backed SLCM | Reset occurs in Entra and writes to AD | One reset can update the directory used by SLCM [15] | Reset assurance and sign-in MFA are distinct policy questions | Requires licensing, permissions, and Entra Connect configuration [15] | Unknown |
| Independent local SLCM store with coordinated password | SLCM database and Entra separately | A custom process could set equivalent passwords in two systems | Each application must protect its own login | Highest risk of policy drift and inconsistent incident response | **Inference only; no MUJ evidence** |

Two non-obvious points follow. First, PHS is not itself SLCM SSO. It only explains how an on-premises credential can become usable in Entra. SLCM would still need AD authentication, federation, or another integration. Second, seeing the same password after a cloud reset may suggest writeback, but it cannot prove it because help-desk synchronization or another directory process could create the same result.

The decision-ready question is: **Does SLCM receive a password or a token?** A token-based answer supports centralized MFA. A password-based answer requires a second question: **Which directory validates it and what compensating MFA protects that path?**

## 5. One Credential Across Mail And ERP Changes The Blast Radius

CISA defines MFA as requiring two or more credentials and explains that a compromised first credential alone should not satisfy the second requirement [19]. CISA also states that MFA makes accounts 99% less likely to be hacked [19]. Microsoft makes a related but differently qualified claim: MFA combined with blocking legacy authentication stops more than 99.9% of common identity-related attacks [4]. These figures should not be treated as guarantees, but both sources support prioritizing MFA over password-only access.

**Inference:** if Outlook and SLCM independently accept the same reusable password, one successful credential phish can create two initial-access opportunities. Mail access can expose communications, contacts, and trusted sender identity; ERP access can expose records and workflows available to that account. The exact data and privileges depend on role, so this report does not claim access to any specific MUJ record.

**Inference:** mail can also become a recovery pivot if an application sends reset messages or approvals to the institutional mailbox. That scenario must be verified from approved application configuration, not tested against real users. Similarly, an ERP account can become a social-engineering pivot if its directory exposes classmates, faculty, or administrative context.

### Table 5. Conditional threat paths and defensive controls

| Conditional path | Required condition | Potential effect | Preventive control | Detection and response |
|---|---|---|---|---|
| Password phishing -> Outlook and SLCM | Both paths accept the same password; neither requires an independent second factor | Cross-application account takeover | Phishing-resistant MFA on both paths; federate SLCM where feasible | Correlate Entra and SLCM sign-ins; revoke sessions and reset affected credentials |
| Outlook compromise -> SLCM recovery | SLCM recovery relies on the compromised mailbox | Attacker attempts a reset or intercepts notification | Strong reset assurance; out-of-band verification for sensitive recovery | Alert on reset followed by new device or anomalous sign-in |
| Compromised campus account -> trusted phishing | Mailbox can send internally and recipients trust the sender | Lateral credential theft | Phishing-resistant MFA, user reporting, outbound anomaly controls | Search mail and sign-in telemetry; notify recipients under the incident plan |
| Legacy mail protocol -> password-only access | A legacy protocol remains enabled | MFA policy is not invoked | Block legacy authentication; Microsoft says these protocols do not support MFA [14] | Begin in Report-only mode before enforcement [14] |
| Entra MFA -> local SLCM password path | SLCM is not federated or otherwise covered | Outlook is protected while ERP remains password-only | Add application-level MFA or place SLCM behind a supported Entra integration | Compare application coverage, not just MFA enrollment totals |
| Parent account -> alternate local identity | Parent Login uses a separate lifecycle | Weaker enrollment, reset, or deprovisioning may exist | Separate parent policy, verified contact lifecycle, risk-based monitoring | Review inactive and anomalous parent accounts |
| User policy -> service identity blind spot | Automation uses service principals, shared accounts, or API keys | Human MFA policy does not cover workload access | Managed identities, workload controls, key rotation, least privilege | CISA recommends reviewing API keys and shared accounts associated with affected identities [21] |

The mechanism is concentration of trust. A single credential can simplify user support, but its safety depends on centralized policy and complete coverage. Centralization without MFA concentrates failure; centralization with strong MFA, device and risk signals, prompt deprovisioning, and unified logging can reduce duplicated controls.

## 6. MFA Gaps Are About Coverage, Not A Product Logo

Security Defaults is available with the free Entra tier and supplies a baseline against identity attacks [4]. It requires all users to register for MFA, requires specified administrators to perform MFA every time they sign in, blocks legacy authentication, and requires MFA for Azure management resources [4]. Ordinary users are prompted when Microsoft deems it necessary based on factors such as location, device, role, and task [4]. Thus, MFA registration is not equivalent to a challenge on every ordinary sign-in.

Conditional Access is Microsoft's Zero Trust policy engine. It evaluates user, group, location, device, application, risk, and other signals after first-factor authentication, then can block access or require MFA, a specified authentication strength, a compliant device, an approved application, or other controls [3]. Conditional Access requires Entra ID P1, while risk-based policies require the P2 Identity Protection capability [3]. No public evidence establishes MUJ's license tier.

Security Defaults and Conditional Access also differ in flexibility. Microsoft describes Security Defaults as on or off, while Conditional Access is fully customizable [4]. When an organization replaces Security Defaults with Conditional Access, Microsoft says it must disable Security Defaults and should immediately enable replacement policies [4]. **Inference:** a migration gap, an exclusion, or an uncovered application can leave users registered for MFA without uniformly enforced protection.

### Table 6. MFA coverage gaps to validate administratively

| Gap scenario | Why the Microsoft 365 logo does not resolve it | Evidence to request | MUJ finding now |
|---|---|---|---|
| Security Defaults disabled | Tenant administrators can replace it with Conditional Access [4] | Current tenant properties and policy inventory | Unknown |
| Students excluded from a Conditional Access policy | Conditional Access evaluates users and groups [3] | Policy assignments, exclusions, and coverage report | Unknown |
| SLCM uses local authentication | A non-federated application does not automatically inherit Entra policy | Enterprise-app record and SLCM authentication design | Unknown |
| Ordinary user registered but not challenged every time | Security Defaults uses contextual prompting for ordinary users [4] | Aggregated sign-in results showing MFA requirement and satisfaction | Unknown |
| Legacy authentication enabled | Legacy protocols do not support MFA [14] | Exchange authentication policy and legacy sign-in summary | Unknown |
| Service principals or API identities uncovered | User-scoped Conditional Access does not block service-principal calls [14] | Workload identity and credential inventory | Unknown |
| Parent identities outside Entra | Public portal presents Parent Login [10], but its authority is unknown | Parent identity source, reset, MFA, and deprovisioning documentation | Unknown |
| Weak fallback or recovery | Sign-in MFA and password reset are separate control planes | SSPR methods, help-desk procedure, recovery audit logs | Unknown |
| Licensing limits granular policy | P1 is needed for Conditional Access and P2 for risk-based policy [3] | Purchased licenses and assigned coverage | Unknown |

### Higher-education case study: MSJC publishes what MUJ's public evidence lacks

Mt. San Jacinto College publicly documents Microsoft 365 MFA enrollment. Its guidance defines MFA as two or more verification factors, says the extra factor decreases the likelihood of a successful cyberattack, and lists SMS, voice, or Microsoft Authenticator as enrollment options [26]. MSJC also publicly states that it moved its SSO portal to Microsoft 365 My Apps [24].

This does not prove that MSJC's implementation is perfect or that MUJ lacks MFA. It demonstrates a transparency benchmark: a university can publish the identity portal, MFA enrollment expectations, supported methods, and help path without exposing sensitive configuration. MUJ could reduce ambiguity by publishing equivalent user-facing statements while keeping tenant internals private.

### Education-data case study: documented defense in depth

The National Student Clearinghouse, a nonprofit higher-education partner, states that all access is controlled by passwordless or multifactor authentication [25]. It also publicly describes zero-trust vetting [25], least-privilege role-based access [25], encryption at rest and in transit [25], and two 24/7 managed security services [25]. Its program is measured against SOC 2 Type 2, the NIST Cybersecurity Framework, the Cyber Kill Chain, and MITRE ATT&CK [25].

The comparison reveals the key mechanism: MFA is strongest as one layer in an identity system that also limits privilege, protects data, monitors continuously, and measures controls against frameworks. MUJ's public page cannot show whether those layers exist. The appropriate result is an evidence request, not an adverse finding.

## 7. Defensive Validation Plan: Administrator Evidence, Not Probing

The validation plan should follow a Zero Trust assumption: never infer that a request is trusted merely because it comes from a campus network or an institutional account. Conditional Access is explicitly described by Microsoft as a Zero Trust policy engine [3]. The plan should also map to the NIST Cybersecurity Framework functions: Govern, Identify, Protect, Detect, Respond, and Recover. This is a governance structure, not an invitation to test production controls.

### Table 7. Authorized evidence request

| Question | Evidence the owner can provide | Decision it resolves | Sensitive detail to exclude from club copies |
|---|---|---|---|
| What is the cloud sign-in method? | Entra Connect configuration summary showing PHS, PTA, or federation | Distinguishes the password authority | Connector secrets, agent keys, service-account credentials |
| Is the MUJ domain managed or federated? | Verified-domain and federation-status summary | Determines whether Entra or an external IdP handles the domain | Signing private keys and internal endpoints |
| How does SLCM trust identity? | Enterprise-application record, protocol name, issuer/audience summary, or approved architecture diagram | Distinguishes SAML/OIDC token use from local password validation | Certificates' private material and production secrets |
| Does SLCM receive passwords? | Application authentication design statement | Determines password exposure and MFA inheritance | Password samples, hashes, and database contents |
| Who receives MFA? | Security Defaults status; Conditional Access assignments, exclusions, and authentication-strength requirements | Measures student, staff, admin, parent, and guest coverage | User-level sign-in details not needed for analysis |
| Are legacy protocols blocked? | Exchange authentication-policy summary and aggregated legacy sign-in report | Identifies password-only mail paths | Individual message content |
| Are parent users covered? | Parent identity lifecycle, reset, MFA, and inactivity policy | Resolves alternate-path risk | Parent personal data |
| What happens on termination? | Joiner-mover-leaver workflow and deprovisioning service levels | Measures residual access | Individual HR or student records |
| Can incidents be correlated? | Log-source inventory, retention periods, time synchronization, and incident ownership | Determines detection and CERT-In readiness | Raw logs unless incident handling requires them |

### Table 8. Phased remediation roadmap

| Phase | Defensive actions | Success measure |
|---|---|---|
| 0-14 days: establish truth | Name an identity owner; approve an architecture diagram; inventory every interactive, parent, service, and recovery path; document license tier; preserve current policy exports | Every route has an owner, authority, protocol, MFA state, and log source |
| 15-30 days: close obvious gaps | Place legacy-auth blocking in Report-only mode; identify exclusions; require phishing-resistant MFA for administrators; maintain protected emergency access accounts | No unexplained password-only path; emergency access is controlled and monitored |
| 31-60 days: unify coverage | Federate SLCM where supported or add equivalent application-level MFA; align student, staff, parent, guest, and service identity policies; harden recovery | Every high-value interactive path requires an approved second factor |
| 61-90 days: detect and exercise | Correlate Entra and SLCM events; test the incident playbook administratively; conduct a tabletop for shared-credential compromise; publish user guidance | Tabletop demonstrates containment across mail, ERP, sessions, resets, and support |
| Ongoing: govern | Quarterly review of exclusions and inactive accounts; annual architecture attestation; patch and dependency review for the supplied web stack; metrics to the security committee | Declining exceptions, complete logging, current dependencies, documented risk acceptance |

Microsoft recommends beginning legacy-auth blocking in Report-only mode so administrators can measure impact before switching the policy on [14]. CISA recommends phishing-resistant MFA wherever technically feasible, strong unique passwords, review of anomalous authentication, and resets across affected enterprise services [21]. These actions should be executed by authorized owners with rollback plans, not by the club.

## 8. Incident Response And Indian Operational Context

CERT-In's 2022 directions apply specified duties to service providers, intermediaries, data centers, body corporates, and government organizations. They require reporting listed cyber incidents within six hours of noticing them or being informed, secure retention of ICT logs for a rolling 180 days within India, and clock synchronization with specified or traceable time sources [22]. Whether each provision applies to MUJ in a particular incident is a legal and regulatory question for university counsel; this report is not legal advice.

A shared-credential incident should not be handled as an email-only or SLCM-only event. CISA recommends resetting known affected users across enterprise services, especially where local credentials may not be federated; immediately changing passwords reused elsewhere; reviewing privileged, service, and federated identities; and assessing API keys and shared accounts [21].

### Table 9. Shared-credential incident playbook outcomes

| Function | Required outcome | Rationale |
|---|---|---|
| Govern | Incident commander, identity owner, application owner, privacy contact, and CERT-In point of contact are named | Prevents delay during a six-hour regulatory window where applicable [22] |
| Identify | Determine affected human accounts, parent identities, service accounts, sessions, tokens, API keys, and applications | Password reset alone may not cover every associated credential [21] |
| Protect | Reset affected passwords, revoke active sessions, require phishing-resistant MFA, and remove unsafe legacy access | CISA explicitly recommends resets and phishing-resistant MFA [21] |
| Detect | Review Entra, mail, SLCM, directory, recovery, and administrative events on a synchronized timeline | CERT-In requires time synchronization and retained logs for covered entities [22] |
| Respond | Contain both mail and ERP, preserve evidence, notify stakeholders through approved channels | Cross-application trust can create multiple effects from one credential |
| Recover | Restore access through verified recovery, monitor recurrence, and close the policy gap that allowed the incident | Avoids returning the user to the same vulnerable authentication path |

**Inference:** the most damaging response failure would be resetting only the Microsoft 365 password while leaving an independently stored SLCM credential active, or resetting only SLCM while active Microsoft sessions remain valid. The architecture inventory must tell responders whether one reset propagates through PHS, PTA, writeback, federation, or no shared control at all.

## 9. Synthesis: Four Tensions Determine The Real Risk

### Table 10. Cross-cutting comparison

| Dimension | PHS | PTA | Federation or Application Proxy | Independent SLCM credential |
|---|---|---|---|---|
| Mechanism | Derived on-premises hash is synchronized to Entra [5] | Entra sign-in is validated against on-premises AD [13] | Entra issues or mediates identity for the application [2][8] | Application validates its own reusable secret |
| Password exposure to SLCM | Depends on whether SLCM separately uses AD | Depends on whether SLCM separately uses AD | Usually unnecessary for SAML token consumption | Required by the local application |
| MFA scope | Entra MFA protects cloud sign-in; SLCM requires its own integration | Entra MFA works with PTA [13]; SLCM coverage remains a separate question | Central policy can cover the application | Separate MFA is required |
| Availability | Cloud authentication has strong availability; state changes can lag [12] | Depends on available authentication agents [13] | Depends on Entra, connectors, and application trust | Depends on SLCM and its credential store |
| Operational trade-off | Simple cloud sign-in and possible delayed account-state propagation | Immediate AD policy at sign-in but on-premises dependency | Strong central policy with integration complexity | Simpler legacy design but policy drift and larger password blast radius |
| Public MUJ evidence | None | None | None | None |

**Tension 1: shared password versus SSO.** Password parity is a user-experience statement. SSO is a protocol and session statement. PHS can create parity without federating SLCM, while SAML can create SSO without giving SLCM the password [5][2]. The university should stop using the two terms interchangeably in documentation.

**Tension 2: centralization versus concentration.** One authoritative identity can improve deprovisioning and policy consistency. The same design raises the consequence of a stolen first factor if any connected application omits MFA. The right recommendation is not "use separate passwords everywhere"; it is "centralize authority where practical, enforce phishing-resistant MFA, and eliminate uncontrolled local paths."

**Tension 3: free baseline versus granular enforcement.** Security Defaults provides broad, free protection and blocks legacy authentication [4]. Conditional Access provides application, group, device, location, and risk-sensitive control but requires P1 or P2 licensing for key capabilities [3]. **Inference:** an education tenant may face cost and support trade-offs, but those pressures do not establish MUJ's policy or justify leaving high-value ERP access password-only.

**Tension 4: strong generic evidence versus weak institution-specific evidence.** Microsoft and CISA documentation supports the mechanisms and controls with high confidence. The MUJ public page supports only a narrow surface description. The responsible OSINT verdict must therefore be strong on architectural possibilities and defensive priorities, but restrained on MUJ's actual implementation.

The non-obvious conclusion is that the FAQ phrase, if authentic, is neither automatically good nor automatically bad. It can describe a well-controlled single identity with federation and phishing-resistant MFA, or a fragile pair of password stores joined only by policy. The difference is invisible from the login page.

## VERDICT

### Table 11. Confidence-weighted findings

| Finding | Verdict | Confidence |
|---|---|---|
| MUJ operates the cited public portal and presents institutional, parent, student, and recovery-oriented choices | Supported by first-party/indexed portal text [9][10] | **High** |
| The public user experience is associated with `@muj.manipal.edu` | Directly displayed [9][10] | **High** |
| The Outlook and SLCM passwords are currently identical for all relevant users | Present in the research brief, but the cited FAQ was not independently recovered | **Low to moderate** |
| MUJ uses Entra Connect PHS | Plausible Microsoft pattern, no MUJ-specific proof | **Low** |
| MUJ uses PTA | Plausible alternative, no MUJ-specific proof | **Low** |
| SLCM is federated to Entra using SAML, OIDC, Application Proxy, or another method | Plausible and defensively preferable where supported, but not demonstrated | **Low** |
| MUJ lacks MFA | Not established; public pages cannot resolve post-first-factor policy | **Very low** |
| A password shared independently by mail and ERP would increase blast radius | Strong conditional inference supported by MFA and compromised-credential guidance [19][21] | **High, conditional on independent password acceptance** |
| Exact ASP.NET MVC, .NET, IIS, and Akamai labels are correct | Supplied in the brief but not verified in citable first-party text | **Low** |
| Priority action is an authorized identity-path and MFA-coverage review | Supported by the unresolved architecture and documented control gaps | **High** |

**Overall verdict: MODERATE CONFIDENCE in the risk model, LOW CONFIDENCE in any claim about MUJ's exact backend configuration.**

There is no public basis to declare MUJ vulnerable, to declare MFA absent, or to assert that a password database is duplicated. There is sufficient basis to identify a material governance question: the portal presents several identity audiences, the brief reports one Outlook/SLCM password, and Microsoft supports multiple architectures that would produce that experience with very different security properties.

The decisive next step is not external testing. It is a written, administrator-approved evidence review answering five questions:

1. Which authority validates each student, staff, parent, guest, and service sign-in?
2. Does SLCM receive a password or an identity-provider token?
3. Which users and applications are covered by MFA, authentication strength, device, and risk policies?
4. Which legacy, recovery, and nonhuman paths remain outside those policies?
5. Can logs and incident actions correlate and contain Microsoft 365 and SLCM within the required response window?

If the reported FAQ is current and both systems independently accept the same password, the highest-priority control is phishing-resistant MFA on both paths, followed by elimination of legacy authentication, unified session revocation, and a cross-application incident playbook. If SLCM is already federated and fully covered by Conditional Access, the risk is materially lower, and the main task becomes documenting that control and confirming parent, recovery, and workload identities are not exceptions.

## References: Exact URLs

- Source 1, MSJC Microsoft 365 MFA enrollment: http://support.msjc.edu/support/solutions/articles/20000040321
- Source 2, What is Microsoft Entra: https://learn.microsoft.com/en-us/entra/fundamentals/what-is-entra
- Source 4, MSJC Microsoft 365 My Apps SSO transition: https://msjc.edu/mymsjc/pg.html
- Source 5, National Student Clearinghouse security: https://studentclearinghouse.org/about/trust/security
- Source 9, National Student Clearinghouse zero-trust statement: https://studentclearinghouse.org/about/trust/security
- Source 13, National Student Clearinghouse least-privilege statement: https://studentclearinghouse.org/about/trust/security
- Source 30, National Student Clearinghouse managed security services: https://studentclearinghouse.org/about/trust/security
- Source 31, National Student Clearinghouse encryption statement: https://studentclearinghouse.org/about/trust/security
- Source 47, National Student Clearinghouse security frameworks: https://studentclearinghouse.org/about/trust/security
- Source 100, Microsoft PHS overview: https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/whatis-phs
- Source 130, Microsoft SAML SSO for enterprise applications: https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/add-application-portal-setup-sso
- Source 131, Microsoft secure hybrid access for legacy applications: https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/secure-hybrid-access
- Source 165, Microsoft Entra password writeback: https://learn.microsoft.com/en-us/entra/identity/authentication/tutorial-enable-sspr-writeback
- Source 166, Microsoft legacy-authentication blocking: https://learn.microsoft.com/en-us/entra/identity/conditional-access/policy-block-legacy-authentication
- Source 167, Microsoft hybrid authentication method comparison: https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/choose-ad-authn
- Source 169, Microsoft Entra Pass-through Authentication: https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-pta
- Source 170, MUJ portal: https://mujslcm.jaipur.manipal.edu/Home/Index
- Source 187, Microsoft Entra Security Defaults: https://learn.microsoft.com/en-us/entra/fundamentals/security-defaults
- Source 189, Microsoft Entra Conditional Access overview: https://learn.microsoft.com/en-us/entra/identity/conditional-access/overview
- Source 204, indexed MUJ portal entry: http://mujslcm.jaipur.manipal.edu/
- Source 210, CISA Multifactor Authentication: https://www.cisa.gov/topics/cybersecurity-best-practices/multifactor-authentication
- Source 212, CISA credential-risk guidance: https://www.cisa.gov/news-events/alerts/2025/04/16/cisa-releases-guidance-credential-risks-associated-potential-legacy-oracle-cloud-compromise
- Source 215, CERT-In Directions under section 70B: https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf

## References

1. *404 - Content not found*. https://learn.microsoft.com/en-us/entra/identity/app-proxy/application-proxy-config-sso-how-to
2. *Enable SAML single sign-on for an enterprise application - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/add-application-portal-setup-sso
3. *Microsoft Entra Conditional Access: Zero Trust Policy Engine - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/conditional-access/overview
4. *Configure Security Defaults for Microsoft Entra ID - Microsoft Entra | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/fundamentals/security-defaults
5. *What is password hash synchronization with Microsoft Entra ID? - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/whatis-phs
6. *Self-service password reset policies - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/authentication/concept-sspr-policy
7. *Implement password hash synchronization with Microsoft Entra Connect Sync - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-password-hash-synchronization
8. *Secure hybrid access, protect legacy apps with Microsoft Entra ID - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/secure-hybrid-access
9. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
10. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
11. *Manipal University*. https://muj.slcm.jaipur.manipal.edu/
12. *Authentication for Microsoft Entra hybrid identity solutions - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/choose-ad-authn
13. *Microsoft Entra Connect: Pass-through Authentication - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-pta
14. *Block legacy authentication with Conditional Access - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/conditional-access/policy-block-legacy-authentication
15. *Enable Microsoft Entra Password Writeback - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/authentication/tutorial-enable-sspr-writeback
16. *Microsoft Entra Connect - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-pta-faq
17. *Indian - Computer Emergency Response Team*. https://www.cert-in.org.in/
18. *Indian - Computer Emergency Response Team*. http://cert-in.org.in/s2cMainServlet?pageid=GUIDLNVIEW02&refcode=CISG-2026-02
19. *Multifactor Authentication | Cybersecurity and Infrastructure Security Agency CISA*. https://www.cisa.gov/topics/cybersecurity-best-practices/multifactor-authentication
20. *Microsoft 365 guidance for security & compliance - Service Descriptions | Microsoft Learn*. https://learn.microsoft.com/en-us/office365/servicedescriptions/microsoft-365-service-descriptions/microsoft-365-tenantlevel-services-licensing-guidance/microsoft-365-security-compliance-licensing-guidance
21. *CISA Releases Guidance on Credential Risks Associated with Potential Legacy Oracle Cloud Compromise | CISA*. https://www.cisa.gov/news-events/alerts/2025/04/16/cisa-releases-guidance-credential-risks-associated-potential-legacy-oracle-cloud-compromise
22. *No. 20(3)/2022-CERT-In Government of India Ministry of Electronics and Information Technology (MeitY) Indian Computer Emergency Response Team (CERT-In) Electronics Niketan,*. https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf
23. *Nonfederal Entity Sharing Guidance Nov 2025 Update*. https://www.cisa.gov/sites/default/files/2025-11/NonFederal-Entity-Sharing-Guidance-Nov-2025-Update.pdf
24. *http://msjc.edu/mymsjc/pg.html*. http://msjc.edu/mymsjc/pg.html
25. *http://studentclearinghouse.org/about/trust/security*. http://studentclearinghouse.org/about/trust/security
26. *http://support.msjc.edu/support/solutions/articles/20000040321*. http://support.msjc.edu/support/solutions/articles/20000040321
27. *http://learn.microsoft.com/en-us/entra/fundamentals/what-is-entra*. http://learn.microsoft.com/en-us/entra/fundamentals/what-is-entra
