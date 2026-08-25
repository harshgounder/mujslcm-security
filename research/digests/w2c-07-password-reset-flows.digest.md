## REPORT (w2c-07-password-reset-flows.md)
Password-reset security assessment for the MUJ SLCM portal with Microsoft Entra SSPR delegation. Verdict: recovery entry point verified, delegate and tenant state not established. Overall confidence Moderate. 275 lines, 37774 chars, read to EOF, truncated: false.

## ANSWER SUMMARY
- Verdict: public evidence supports a recovery entry point and a supplied design delegating recovery to Microsoft Entra SSPR. It does not establish an exploitable weakness, nor SSPR scope, methods, role assignments, Conditional Access, writeback, or session revocation.
- SSPR is not enabled for ordinary users by default; scope can be None, Selected, or All. Eligibility and registered methods are checked only after the user enters an identifier and passes CAPTCHA.
- The claimed FAQ sentence (Outlook password equals SLCM password) was not independently located in reviewed public material and must be treated as supplied. If current, one reset spans academic and collaboration services; this drives the highest-severity inference.
- Security questions are a legacy weak point: SSPR-only, prohibited for administrators, guessable, reusable, and OSINT-able. Remove where possible; never the sole recovery gate.
- SMS and voice are restricted by NIST and last-resort per CISA. Method independence and phishing resistance matter more than counting channels on one device.
- AiTM case: stolen session cookies replay past MFA. Reset handling must cover session state, factor binding, and post-reset containment, not just the password.
- Admin reset planes: Password Administrator is the baseline, Global Administrator carries maximum blast radius, temporary passwords never expire until first sign-in. Separate requester proof, password reset, and factor replacement.
- Entra cannot directly revoke application-issued session tokens; containment requires application session invalidation. A Sept 7, 2026 SSPR explicit-registration enforcement is upcoming as of the report date.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/ - portal with @muj.manipal.edu, parent and student login, and a visible Forgot Password option, the only verified MUJ-facing fact.
- https://passwordreset.microsoftonline.com/ - supplied reset destination; the report says the page extraction did not expose the link destination.
- https://learn.microsoft.com/en-us/entra/identity/authentication/concept-sspr-howitworks - SSPR deep dive: enablement defaults, ID plus CAPTCHA first, method registration checks.
- https://learn.microsoft.com/en-us/entra/identity/authentication/tutorial-enable-sspr - None, Selected, All scoping and the admin two-method default.
- https://learn.microsoft.com/en-us/entra/identity/authentication/concept-sspr-policy - administrator policy: two authentication data pieces, security questions prohibited for admins.
- https://learn.microsoft.com/en-us/entra/identity/authentication/concept-authentication-security-questions - question risks, 3 to 40 character answers, no question or answer reuse, migration encouragement.
- https://learn.microsoft.com/en-us/entra/fundamentals/users-reset-password-azure-portal - administrator reset roles and the temporary password that never expires until first sign-in.
- https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/permissions-reference - Helpdesk, User, and Authentication Administrator capabilities and target-dependent limits.
- https://learn.microsoft.com/en-us/entra/identity/users/users-revoke-access - Entra cannot directly revoke an application-issued session token.
- https://www.microsoft.com/en-us/security/blog/2022/07/12/from-cookie-theft-to-bec-attackers-use-aitm-phishing-sites-as-entry-point-to-further-financial-fraud/ - AiTM campaign: password and session cookie theft, MFA bypassed by replay.
- https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html - uniform responses, side channels, rate limits, high-entropy single-use tokens, no auto-login after reset.
- https://pages.nist.gov/800-63-4/sp800-63b/authenticators - PSTN restricted status, one-time out-of-band secrets, authenticator binding on phone replacement.
- https://www.cisa.gov/sites/default/files/publications/fact-sheet-implementing-phishing-resistant-mfa-508c.pdf - CISA guidance: SMS and voice as last resort, push fatigue with number matching.
- https://learn.microsoft.com/en-us/entra/identity/authentication/howto-sspr-reporting - audit event categories and the temporary block after five reset attempts in 24 hours.
- https://techcommunity.microsoft.com/blog/microsoft-entra-blog/whats-new-in-microsoft-entra-june-2026/4517885 - September 7, 2026 explicit-method enforcement and the July 6, 2026 registration campaign.

## ACTIONABLE LEADS
- MUJ-owned configuration review: verify each portal hyperlink, tenant, and Conditional Access; export SSPR scope and administrator policy; inventory Password, Helpdesk, User, Authentication, Privileged Authentication, and Global Administrator assignments.
- Validate the claimed FAQ wording against a current official page and publish a recovery matrix naming each population, identity store, destination, and reset effect.
- Remove security questions; minimize email, SMS, and voice; require number matching on push; prepare for September 2026 explicit method registration.
- Route SSPR and role events to the SIEM with alerts on policy changes, method registration and replacement, blocked attempts, and admin resets.
- Build a compromise playbook: reset, MFA re-registration, token revocation, application session invalidation, mailbox rule and app registration review.
- Review temporary-password delivery: independent identity proofing, never an untrusted or circular channel, and monitoring that the password is replaced at first sign-in.

## FLAGS
- Shared Outlook and SLCM password claim: supplied in the prompt, not independently located in reviewed public material; the report rates it Low to Moderate confidence.
- Reset link delegation: supplied fact; the text extraction did not expose the destination, so the redirect target is not verified from the page itself.
- AiTM, OTP interception, SIM swap, and push-bombing are generic threat patterns, not findings against MUJ.
- Reference 19 duplicates reference 1 under /Home/Index and reference 9 uses an http scheme; minor consistency issues.
- The September 2026 date is forward-dated from the report date of August 25, 2026; re-verify Microsoft guidance before citing.
- All tenant-level conclusions require MUJ administrator confirmation; nothing was tested by the report.

## COVERAGE
- File read to EOF: 275 lines, 37774 chars (file_size 37774), truncated: false. Confirmed EOF at line 275, final reference.