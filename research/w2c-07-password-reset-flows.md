# MUJ SLCM Password Reset Security Assessment

## Executive Summary

- **Verified Public Reset Surface**: The public MUJ portal advertises `@muj.manipal.edu` sign-in, parent and student login paths, and a visible `Forgot Password?` option [1]. The supplied scope says that option delegates to `https://passwordreset.microsoftonline.com/`; this assessment treats the delegation as a supplied fact rather than proof of MUJ's tenant configuration -> document the reset boundary as an identity-critical integration and have MUJ administrators verify the actual hyperlink, tenant, and Conditional Access behavior internally.

- **Enablement Is Not Proved by a Redirect**: Microsoft states that SSPR is not enabled for ordinary end users by default, while tenant administrators can scope it to `None`, `Selected`, or `All` users [4][5]. The SSPR service checks enablement and registered methods only after the user enters an identifier and passes CAPTCHA [4] -> do not infer that every MUJ account can self-reset merely because the portal publishes a Microsoft reset link.

- **Credential Coupling Raises the Stakes**: The prompt attributes to a public MUJ FAQ the statement that the Outlook password equals the SLCM password. That exact FAQ was not independently located in the public, indexed material reviewed. **Inference, conditional on the FAQ being current**: one reset may affect both academic records and Microsoft 365 resources -> MUJ should treat password recovery as a cross-service identity event, not as a low-impact SLCM convenience.

- **Security Questions Are a Legacy Weak Point**: Microsoft says security questions are used for SSPR, not sign-in; administrator accounts cannot use them; answers may be guessable, reused, phished, or found through OSINT [9]. Microsoft strongly encourages migration to stronger methods [9] -> eliminate questions from student and staff recovery where possible and never rely on them as the sole recovery gate.

- **Transferable OTPs Remain Phishable**: NIST classifies PSTN out-of-band verification as restricted and says verifiers should consider device swaps, SIM changes, number porting, and abnormal behavior [14]. CISA says SMS or voice MFA should be a last-resort option because it is vulnerable to phishing, SS7, and SIM-swap attacks [16] -> prefer phishing-resistant authentication for sign-in and require stronger, independently bound evidence for high-impact recovery.

- **MFA Can Be Bypassed at the Session Layer**: Microsoft documented an adversary-in-the-middle campaign that stole passwords and authenticated session cookies; replaying the cookie skipped authentication even when MFA was enabled [13]. This was not an MFA software flaw, but a session theft pattern -> combine MFA with phishing-resistant methods, Conditional Access, anomaly monitoring, and explicit session revocation [13].

- **Administrative Reset Is a Separate Attack Surface**: Microsoft requires at least Password Administrator for a general user-password reset, while other roles have target-dependent limits [10]. Global Administrators can reset any user or administrator, and Helpdesk Administrator authority depends on the target's role [2] -> minimize role assignments, use just-in-time elevation, and independently verify every helpdesk recovery request.

- **A Reset Is Not Full Containment**: Microsoft warns that Entra cannot directly revoke an application's own session token; the application must enforce its authorization policy [6]. Access tokens can also remain usable until expiration, subject to application and Continuous Access Evaluation behavior [6] -> pair password reset with token revocation, MFA re-registration where appropriate, mailbox and app review, and application-session invalidation.

- **Logging Can Make Recovery Detectable**: Entra audit events distinguish blocked attempts, self-service changes, administrator resets, successful self-service resets, reset-flow progress, unlocks, and registration [8]. Microsoft also documents temporary blocking after excessive reset activity [8] -> route these events to the university SIEM and alert on anomalous reset, registration, and administrator activity.

## Scope, Evidence Classes, and Safe Method

This is a defensive, public-information assessment. It does not test student identifiers, submit recovery requests, intercept messages, enumerate accounts, probe origin infrastructure, or attempt unauthorized access. Any validation involving MUJ's live tenant should be conducted only by MUJ personnel under written authorization, using dedicated test identities and approved monitoring.

The requested architecture describes `mujslcm.jaipur.manipal.edu` as ASP.NET MVC 5.3 on .NET Framework 4.x and IIS 10, behind Akamai, with Microsoft 365 identity. Those stack labels came from the prompt. This review did not independently validate them, and they should not be converted into vulnerability claims. The only directly verified MUJ-facing fact in the indexed public material is the login page's presentation of `@muj.manipal.edu`, parent and student sign-in, and `Forgot Password?` [1].

### Evidence classification table

| Class | What is supported | What is not supported | How the report uses it |
|---|---|---|---|
| Verified public MUJ fact | The portal exposes the named sign-in choices and `Forgot Password?` [1] | Tenant SSPR scope, methods, Conditional Access, role assignments, and backend synchronization | Used as observed external surface only |
| Supplied MUJ fact | The reset link delegates to Microsoft's reset portal; the stack and Microsoft 365 identity details; the claimed FAQ sentence | Independent public confirmation in the reviewed sources | Labeled as supplied, never as verified |
| Microsoft product fact | Generic Entra SSPR behavior, configuration, roles, logs, notifications, and containment [4][5] | MUJ's actual configuration | Used to define possible states and administrator checks |
| Security standard or case evidence | NIST, CISA, OWASP, and Microsoft's AiTM case [14][12][16][13] | Proof that MUJ has suffered or is vulnerable to those patterns | Used for threat modeling and recommendations |
| Inference | Consequence logically conditional on supplied or verified facts | A demonstrated finding | Marked `Inference` every time |

The requested `cot_explicit` format cannot be satisfied as private chain-of-thought. Instead, this report provides an auditable evidence-to-conclusion method: observation, product rule, security mechanism, bounded inference, and defensive decision. This gives reviewers the basis for each conclusion without exposing hidden reasoning or turning the report into an attack guide.

**Decision-ready insight**: Treat all MUJ-specific control claims as unknown until the tenant owner exports configuration and logs. Product documentation explains what Entra can do, not what MUJ has enabled.

## MUJ's Public Reset Boundary: What the Portal and Claimed FAQ Actually Establish

The MUJ portal's public text confirms a combined entry surface for institutional-domain sign-in, parent login, student login, and password recovery [1]. This matters because several identity populations may be represented on one page even if their backing identity stores or reset mechanisms differ. A visible link alone does not establish that parent accounts, student accounts, and Microsoft 365 identities share a recovery policy.

The supplied scope states that the password-recovery destination is `https://passwordreset.microsoftonline.com/`. Microsoft identifies its SSPR portal as the place where a user can change or reset a password [4]. **Inference**: if the MUJ link has that destination, the browser crosses from an MUJ-hosted login surface to a Microsoft-hosted recovery service. That would reduce the amount of reset logic implemented by SLCM itself, but it would not remove MUJ's responsibility for tenant policy, registration, role governance, synchronization, notifications, and incident response.

The prompt also says an MUJ FAQ states that the Outlook password equals the SLCM password. Repeated searches did not locate a publicly indexed official MUJ FAQ containing that exact wording. Therefore, the correct OSINT conclusion is: **the sentence is supplied but not independently verified in this review**. It should be checked against a current official page, handbook, or service-desk article before publication as an MUJ fact.

### Conditional implications of the claimed shared password

| Conditional fact | Security mechanism | Bounded implication | Required MUJ confirmation |
|---|---|---|---|
| Outlook and SLCM use the same Entra credential | One directory credential authenticates multiple relying services | **Inference**: compromise or reset can affect both academic and collaboration data | Confirm identity provider, tenant, and relying-party configuration |
| SLCM has a separate local password synchronized with Microsoft 365 | Password writeback or custom synchronization may connect stores | **Inference**: delay or failure could create inconsistent credentials | Confirm authoritative directory and writeback health |
| The FAQ wording is historical | Portal architecture may have changed | No current coupling should be assumed | Check document date, owner, and current support policy |
| Parent login uses a separate identity | Recovery may remain local or use another provider | Student SSPR controls may not protect parent accounts | Document each account population separately |

Microsoft notes that on-premises sourced users can be reset through Entra only when password writeback is enabled and the domain is managed; federated-domain password changes are not supported through the same path [10]. This illustrates why the FAQ wording cannot reveal the backend architecture by itself.

**Decision-ready insight**: MUJ should publish one current recovery matrix naming each population, authoritative identity store, reset destination, approved support channel, and effect of a reset on SLCM, Outlook, Teams, and other services. Ambiguous "same password" language is operationally useful but security-incomplete.

## SSPR Enablement Markers: Redirects Are Weak Evidence, Tenant Checks Are Strong Evidence

Microsoft describes SSPR as allowing users to change or reset passwords without administrator or helpdesk involvement [4]. For ordinary users, however, SSPR is not enabled on a tenant by default [4]. Administrators can choose `None`, `Selected`, or `All`; in the admin center, only one group can be directly selected, although nested groups are supported [5].

The reset portal first asks for a user ID and CAPTCHA [4]. The service then checks whether the user is enabled for SSPR [4]. An enabled user must have at least one registered authentication method, and reset succeeds only if that user registered a method that the administrator enabled [4]. These facts create a hierarchy of markers.

### SSPR marker and evidentiary-value table

| Public or internal marker | What it proves | What it does not prove | Confidence |
|---|---|---|---|
| MUJ publishes `Forgot Password?` [1] | A recovery route is offered | Microsoft destination, tenant scope, successful reset, or account existence | Low |
| Link destination is Microsoft's SSPR portal, as supplied | Recovery is intended to reach Microsoft | That a particular user is enabled or registered | Low to moderate |
| Microsoft user-ID and CAPTCHA screen [4] | The standard service is reachable | Validity of an MUJ identifier or tenant policy | Low |
| Post-identification eligibility decision [4] | Entra evaluated the submitted identity | Global tenant enablement | Moderate, but sensitive and not for public testing |
| Entra admin export showing `None`, `Selected`, or `All` [5] | Configured scope | Successful registration for every scoped user | High |
| Authentication-method registration report | Which authorized test users have registered methods | Whether recovery is safe under every scenario | High |
| Successful reset by an authorized test account plus audit event [8] | End-to-end operation for that account | Universal operation across students, staff, parents, or admins | High for tested scope |

Administrator accounts differ. Microsoft says administrators are enabled for SSPR by default and must use two methods [5]. The administrator policy enforces two pieces of authentication data and prohibits security questions [11]. These rules should not be generalized to students.

A time-sensitive transition also matters. Microsoft announced that, starting **September 7, 2026**, SSPR will accept only explicitly registered methods; directory-sourced phone numbers and email addresses will no longer count unless registered as authentication methods. Microsoft also announced a registration campaign beginning July 6, 2026 [21]. As of this report's date, August 25, 2026, enforcement is upcoming rather than completed.

**Decision-ready insight**: The university club should report only the public redirect as OSINT. MUJ administrators should establish actual enablement with tenant exports, test accounts, and audit logs, then prepare for the September 2026 registration requirement.

## Recovery Methods: Questions, Email, SMS, Voice, Apps, and OATH Are Not Equivalent

Microsoft lists SSPR-capable methods including Authenticator push, hardware OATH tokens, software OATH tokens, SMS, voice call, and email OTP [4]. Administrators can require one or two available methods [4]. Method count helps, but independence and phishing resistance matter more than counting two channels controlled by the same compromised device or mailbox.

### Recovery-method security table

| Method | Microsoft SSPR status | Principal risk | Defensive position |
|---|---|---|---|
| Security questions | Legacy SSPR identity check; prohibited for administrators [9][11] | Guessing, reuse, OSINT discovery, and phishing [9] | Remove; do not use as sole recovery evidence |
| Email OTP | Supported for member SSPR [3] | Transferable code; recovery can become circular if the mailbox depends on the lost credential | Use only an independently secured alternate address; alert on changes |
| SMS OTP | Supported [4] | Phishing, SS7, SIM swap; PSTN is restricted [16][14] | Last resort; evaluate SIM/porting risk and provide alternatives |
| Voice call | Supported [4] | PSTN rerouting and social-engineering exposure | Treat like SMS, not as a high-assurance method |
| Authenticator push | Supported [4] | Push bombing and accidental approval without number matching [16] | Require number matching and monitor repeated prompts |
| Software OATH OTP | Supported [4] | Manually entered OTPs are not phishing-resistant [14] | Better than password only, but vulnerable to real-time relay |
| Hardware OATH token | Supported in preview [4] | Manual OTP can still be relayed; inventory and loss handling matter | Use with binding and rapid revocation procedures |
| FIDO2 or certificate-based sign-in | Recommended by Microsoft for phishing resistance [3] | Recovery may still fall back to weaker methods | Use for primary authentication and prevent weak recovery from undoing its assurance |

Security-question implementation details do not make questions strong. Microsoft stores answers privately and prevents administrators from reading or changing them [9]. Answers must contain 3 to 40 characters; users cannot reuse a question or answer [9]. These are useful hygiene controls, but Microsoft still says questions are less secure and strongly encourages migration [9].

NIST adds two important mechanisms. First, an out-of-band secret must be accepted only once during its validity period, providing replay resistance [14]. Second, changing a preregistered phone number constitutes binding a new authenticator and must follow authenticator-binding rules [14]. The recovery flow must therefore protect changes to the recovery channel at least as carefully as use of the channel.

**Decision-ready insight**: MUJ should rank methods by resistance to remote phishing and channel takeover, not merely by availability. Two weak, co-resident channels should not be treated as equivalent to two independent strong signals.

## Administrator Reset Paths: Role Scope, Temporary Passwords, and Helpdesk Risk

Microsoft permits administrators to reset a user's forgotten, locked, or initially unavailable password [10]. At least Password Administrator is required for a general reset, while other roles have narrower target-dependent rights [10]. The role model creates a separate recovery plane that must be assessed independently from SSPR.

### Administrative role and reset table

| Role | Documented capability | Important limit or risk | Recommended governance |
|---|---|---|---|
| Password Administrator | Baseline role for user-password reset [10] | Can become a social-engineering target | Just-in-time activation, ticket linkage, independent identity proofing |
| Helpdesk Administrator | Can change passwords and invalidate refresh tokens, depending on the target's role [2] | Authority varies with target; frontline support is highly exposed | Scope narrowly and deny privileged-target resets |
| User Administrator | Can reset passwords and invalidate refresh tokens [2] | Cannot manage MFA [2] | Separate password administration from factor administration |
| Authentication Administrator | Can view, set, and reset authentication methods for non-admin users [2] | Factor replacement can enable takeover even without changing the password | Alert on method deletion, addition, and re-registration |
| Privileged Authentication Administrator | Needed for certain administrator-account containment actions [6] | Highly consequential role | Use privileged access workflows and dual control |
| Global Administrator | Can reset any user and every other administrator [2] | Maximum blast radius | Reserve for emergency use; avoid routine helpdesk work |

In the Entra administrative reset workflow, Microsoft generates a temporary password that the administrator copies and gives to the user. The user must change it at next sign-in [10]. Microsoft also states that this temporary password never expires and remains usable until that first sign-in [10]. That property creates an operational requirement: deliver it through an authenticated, short-lived support process and monitor whether it is promptly replaced. The platform behavior should not be mistaken for a recommended ticketing practice.

Microsoft's SSPR contact link also has governance implications. In its default state, a help request emails eligible administrators. Notification priority runs through Helpdesk or Password Administrators, then User Administrators, then Global Administrators, with at most 100 recipients [17]. Microsoft recommends least-privileged roles and says Global Administrator should be limited to emergency scenarios [17].

**Inference**: if the claimed shared Outlook/SLCM credential is current, a helpdesk reset could affect more than one service. The ticket should therefore trigger a cross-service risk review, not merely confirmation that SLCM login now works.

**Decision-ready insight**: Separate three authorities: proving the requester's identity, resetting the password, and replacing authentication methods. No single routine helpdesk role should silently control all three for privileged or high-impact accounts.

## Reset-Flow Attack Patterns: From Enumeration to Session Replay

The following patterns are generic threat models, not findings against MUJ. They are included so authorized defenders can verify controls without reproducing an attack.

### Attack-pattern and mitigation table

| Pattern | Mechanism | Potential impact | Safe defensive control |
|---|---|---|---|
| Account enumeration | Different messages or timing reveal whether an identifier exists | Target list for phishing or credential attacks | Return consistent messages and timing [12] |
| Reset flooding | Automated requests trigger repeated email, SMS, or push traffic | Harassment, cost, and user conditioning | Per-account rate limits, CAPTCHA, and anomaly detection [12] |
| Email OTP capture | A phisher or compromised mailbox obtains a transferable code | Password reset and possible cross-service takeover | Independent recovery mailbox, short validity, single use, risk alerts |
| SIM swap or number porting | Attacker redirects the victim's telephone number | SMS or voice OTP interception | Evaluate swap/porting signals and offer non-PSTN alternatives [14] |
| Security-question OSINT | Public biographical data or phishing reveals answers | Recovery bypass | Remove questions; require stronger methods [9] |
| Push fatigue | Repeated prompts induce accidental approval | Unauthorized authentication or factor confirmation | Number matching, throttling, and user reporting [16] |
| AiTM phishing | Reverse proxy captures password, MFA interaction, and session cookie | Authenticated session replay and mailbox access | FIDO2 or certificates, Conditional Access, anti-phishing, and monitoring [13] |
| Recovery-channel replacement | Attacker substitutes a phone or other recovery method | Durable control of future resets | Treat replacement as new-authenticator binding [14] |
| Residual application session | Password changes but an app session remains valid | Continued access after apparent recovery | Revoke Entra tokens and application-owned sessions [6] |
| Unsafe reset token | Predictable, reusable, long-lived, or exposed reset artifact | Direct password takeover | Random, securely stored, user-bound, expiring, single-use tokens [12] |

### Case study: Microsoft's AiTM campaign

Microsoft observed a large-scale campaign in which AiTM phishing sites stole passwords, hijacked authenticated sessions, and bypassed the need to repeat MFA [13]. The attacker positioned a proxy between the user and the legitimate site, capturing both the password and the session cookie [13]. Stolen credentials and cookies were then used to access mailboxes and conduct follow-on business email compromise [13].

The mechanism is important: Microsoft explicitly says this is not a vulnerability in MFA. The attacker steals the proof of an already authenticated session; replaying that cookie skips the authentication ceremony regardless of the original sign-in method [13]. In a reset context, the same lesson applies to a successfully phished OTP or an already stolen browser session: changing the password alone may not remove the attacker.

OWASP therefore recommends that, after a reset, the user either be asked to invalidate all existing sessions or that sessions be invalidated automatically. It also advises against automatic login after the new password is set [12]. The application should regenerate its session identifier after a password change [15].

**Decision-ready insight**: The dominant failure mode is not always "MFA was absent." It can be "recovery or session state was weaker than MFA." MUJ's controls should preserve authentication assurance through the entire reset, factor-binding, and post-reset session lifecycle.

## Detection and Incident Response: Reset, Re-register, Revoke, and Review

Entra provides specific audit categories for SSPR policy changes, blocked attempts, self-service password changes, administrator resets, successful self-service resets, reset-flow progress, unlocks, and registration [8]. Audit logs can be filtered to the Self-service Password Management service [8]. These events allow a university SOC to distinguish user recovery from helpdesk intervention and from repeated failure.

Microsoft documents a temporary abuse control: after more than five total attempts in 24 hours, the user is blocked from additional reset operations, authentication attempts, or phone validation for the next 24 hours [8]. This is a platform control, not a substitute for university monitoring. An attacker may distribute attempts across accounts, while a legitimate student under pressure may repeatedly fail.

### Detection and response table

| Signal | Why it matters | Recommended response |
|---|---|---|
| SSPR policy changed | Alters who can reset and how | Require change record; compare old and new values; review administrator |
| User registered or replaced a method | Can create durable recovery control | Alert on risky location, new device, or proximity to password reset |
| Blocked reset attempts | May show abuse or confused user | Correlate across IP, account, device, and helpdesk contacts |
| Successful self-service reset | Confirms recovery event | Notify user; review concurrent sessions and sign-ins |
| Administrator reset | Represents privileged intervention | Link to ticket, requester verification, and role activation |
| MFA re-registration required | Removes possibly compromised factors | Verify that new binding occurs on a trusted device and channel |
| Session revocation | Contains token reuse | Confirm application-owned sessions are also terminated |
| Mailbox rule or app-registration change | Possible post-compromise persistence | Investigate and remove unauthorized changes [20] |

For risky or compromised identities, Microsoft lists administrator actions including password reset, MFA re-registration, blocking the user, and revoking sessions [20]. For active unauthorized access, it recommends blocking the user, resetting the password, and revoking refresh tokens, followed by review for privilege escalation, application registrations, mailbox rules, and sensitive-resource access [20]. Microsoft cautions that contacting a user through email or Teams may be unsafe because those channels could themselves be compromised [20].

Containment has technical limits. Entra cannot directly revoke a session token issued by an application; that application must enforce revocation [6]. Continuous Access Evaluation can accelerate revocation for capable applications, but locally stored data or nonintegrated applications may persist [6].

**Decision-ready insight**: Define a university recovery incident as complete only when identity, factors, Entra tokens, application sessions, suspicious persistence, and user communications have all been addressed.

## MUJ Control Roadmap: Authorized Checks With No Student-Account Probing

The roadmap below is deliberately administrative and nonexploitative. It assumes MUJ's identity and security teams perform the work with test accounts and approved access.

### Prioritized control table

| Priority | Authorized action | Evidence produced | Success condition |
|---|---|---|---|
| P0 | Confirm each portal hyperlink, tenant, and identity population | Signed architecture and recovery-flow map | Student, staff, parent, alumni, and admin flows are distinct and owned |
| P0 | Export SSPR scope and administrator policy | Entra configuration snapshot | Scope matches policy; admins retain strong two-gate controls [11] |
| P0 | Inventory Password, Helpdesk, User, Authentication, Privileged Authentication, and Global Administrator assignments | Role review | Routine support uses the least privilege documented by Microsoft [17] |
| P0 | Validate the claimed FAQ and replace ambiguous wording | Current official support article | Users know which services change and which support channel is legitimate |
| P1 | Remove security questions and minimize email, SMS, and voice recovery | Authentication-method policy | Weak methods are unavailable except documented exceptions |
| P1 | Require strong primary authentication and number matching where push remains | Conditional Access and method configuration | Remote phishing and push-fatigue exposure is reduced [16] |
| P1 | Prepare for September 7, 2026 explicit-method enforcement | Registration campaign report | In-scope users have at least one explicitly registered method [21] |
| P1 | Protect method replacement as authenticator binding | Registration policy and alerts | New phone or method requires strong recent authentication and risk checks |
| P2 | Integrate SSPR and role events with the SIEM | Alert rules and test evidence | Reset, registration, policy change, and admin reset generate actionable alerts |
| P2 | Create compromise playbook covering reset, factor re-registration, token revocation, and app sessions | Exercised runbook | A test incident closes every containment layer |
| P2 | Review temporary-password delivery | Helpdesk procedure | Identity is independently verified; password is never sent through an untrusted or circular channel |
| P3 | Exercise recovery with dedicated test identities | Approved test report | Each expected flow works without account disclosure, weak fallback, or residual sessions |

OWASP's baseline can be used as acceptance criteria. Recovery should return uniform messages and timing, use a side channel, rate-limit automated submissions, generate high-entropy artifacts, bind them to one user, store them securely, expire them, and make them single-use [12]. After reset, the service should notify the user without sending the password, avoid automatic login, and invalidate existing sessions [12].

For the club, safe public research stops at documenting pages, policies, certificates, published support material, and vendor documentation. It should not submit real MUJ identifiers, compare responses for account existence, trigger OTPs, call the helpdesk under false pretenses, or inspect nonpublic origin infrastructure.

**Decision-ready insight**: The most useful student-club deliverable is a gap register for MUJ administrators, not a live proof of bypass. Configuration evidence and controlled test-account results can answer the important questions without exposing students.

## Synthesis: The Recovery Chain Is Only as Strong as Its Weakest State Change

The evidence supports four distinct layers: public routing, Entra eligibility, identity proofing, and post-reset containment. Conflating them produces false confidence. A Microsoft-hosted page may be genuine while the tenant scope is wrong; two methods may be enabled while both are phishable; a password may be changed while a session remains active.

### Cross-cutting comparison table

| Dimension | Public MUJ portal | Entra SSPR | Administrative reset | Post-reset containment |
|---|---|---|---|---|
| Primary mechanism | Routes users to sign-in or recovery | Evaluates scope, registration, and proof methods | Privileged operator changes password or methods | Revokes access and removes persistence |
| Evidence available publicly | Page text and links [1] | Generic Microsoft behavior only | Generic Microsoft role model only | Generic Microsoft response guidance only |
| Evidence requiring tenant access | Exact hyperlink, tenant, populations | `None`/`Selected`/`All`, methods, policies, reports | Role assignments, tickets, approvals | Tokens, app sessions, mailbox rules, device state |
| Main trade-off | Simplicity versus ambiguity | User autonomy versus recovery assurance | Fast support versus social-engineering and privilege risk | Rapid containment versus application limitations |
| Typical weak point | Outdated FAQ or misleading shared-password wording | Weak fallback or stale recovery channel | Excess privilege or poor requester verification | Residual session or persistence |
| Best control | Current recovery matrix | Strong registered methods and risk-aware policy | Least privilege and independent proofing | Reset plus re-register, revoke, and review |

Three tensions deserve emphasis. First, self-service reduces helpdesk involvement [4], but it transfers trust to preregistered channels. If those channels are old, shared, or easy to intercept, automation scales the wrong trust decision. Second, MFA improves sign-in, but AiTM demonstrates that an authenticated session can be stolen after MFA [13]. Recovery design must therefore include session state, not merely factor count. Third, administrative recovery helps users who cannot satisfy SSPR, but it introduces human identity-proofing and privileged-role risk.

The claimed Outlook/SLCM password equality sharpens all three tensions. **Inference, conditional on current shared identity**: the reset's blast radius spans at least academic and collaboration services. That increases the value of self-service availability, but it also increases the consequence of weak recovery and incomplete containment.

The strongest architecture is therefore not "SSPR enabled" in isolation. It is a coherent chain: clearly published official route; correct tenant and population mapping; explicitly registered, independent methods; phishing-resistant primary authentication; protected authenticator replacement; least-privileged helpdesk fallback; comprehensive audit; and application-aware revocation.

## VERDICT

**Verdict: The public evidence supports that MUJ presents a password-recovery entry point and that the supplied design delegates recovery to Microsoft Entra SSPR. It does not establish a publicly exploitable weakness, nor does it prove MUJ's SSPR scope, enabled methods, administrator assignments, Conditional Access, password writeback, or session-revocation configuration.**

**Overall confidence: Moderate.**

| Finding | Confidence | Reason |
|---|---|---|
| Public MUJ portal exposes institutional sign-in and `Forgot Password?` | High | Direct public page evidence [1] |
| Microsoft Entra SSPR has the documented generic behaviors described | High | Microsoft primary documentation [4][5] |
| SMS, voice, security questions, and manual OTPs have the stated generic risks | High | Microsoft, NIST, and CISA guidance [9][14][16] |
| MUJ's link currently delegates to the named Microsoft portal | Moderate | Supplied fact and passive observation, but the citable text extraction did not expose the destination |
| Outlook and SLCM currently share one password | Low to moderate | Attributed to an MUJ FAQ in the prompt, but the exact public document was not independently located |
| MUJ is vulnerable to OTP interception, MFA bypass, or admin-reset abuse | Not established | No authorized tenant test, configuration export, or incident evidence |

The most important next step is an MUJ-owned configuration review using test identities. The university should verify the reset link and FAQ, export SSPR scope and methods, remove weak fallback, review roles, prepare for September 2026 explicit registration, and exercise full containment. Until that occurs, responsible reporting should describe **risk conditions**, not claim a vulnerability.

## References

1. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
2. *Microsoft Entra Built-in Roles - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/permissions-reference
3. *Microsoft Entra authentication overview - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/authentication/overview-authentication
4. *Self-service password reset deep dive - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/authentication/concept-sspr-howitworks
5. *Enable Microsoft Entra self-service password reset - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/authentication/tutorial-enable-sspr
6. *Revoke user access in an emergency in Microsoft Entra ID - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/users/users-revoke-access
7. *Choosing and Using Security Questions - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Choosing_and_Using_Security_Questions_Cheat_Sheet.html
8. *Self-service password reset reports - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/authentication/howto-sspr-reporting
9. *Security questions authentication method - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/authentication/concept-authentication-security-questions
10. *Reset a user's password - Microsoft Entra | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/fundamentals/users-reset-password-azure-portal
11. *Self-service password reset policies - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/authentication/concept-sspr-policy
12. *Forgot Password - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html
13. *From cookie theft to BEC: Attackers use AiTM phishing sites as entry point to further financial fraud | Microsoft Security Blog*. https://www.microsoft.com/en-us/security/blog/2022/07/12/from-cookie-theft-to-bec-attackers-use-aitm-phishing-sites-as-entry-point-to-further-financial-fraud/
14. *Authenticators*. https://pages.nist.gov/800-63-4/sp800-63b/authenticators
15. *Session Management - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
16. *Implementing Phishing-Resistant MFA*. https://www.cisa.gov/sites/default/files/publications/fact-sheet-implementing-phishing-resistant-mfa-508c.pdf
17. *Customize Self-Service Password Reset - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/authentication/howto-sspr-customization
18. *More than a Password | CISA*. https://www.cisa.gov/MFA
19. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
20. *Investigate risk with Microsoft Entra ID Protection - Microsoft Entra ID Protection | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/id-protection/howto-identity-protection-investigate-risk
21. *What's New in Microsoft Entra: June 2026 | Microsoft Community Hub*. https://techcommunity.microsoft.com/blog/microsoft-entra-blog/whats-new-in-microsoft-entra-june-2026/4517885
