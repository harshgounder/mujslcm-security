## REPORT (w2c-05-register-number-enum.md)
Register-number predictability assessment for MUJ SLCM based on public PDFs, GitHub projects, and open metadata. Verdict: MATERIAL DEFENSIVE EXPOSURE, NO VERIFIED ENUMERATION OR IDOR. 241 lines, 35582 chars, read to EOF, truncated: false.

## ANSWER SUMMARY
- Username derivation confirmed: official SLCM FAQ publishes `Username: name.registration number` with example garv.2506040062 and ties the password to the official Outlook ID. A register number is part of a predictable login name, not an authentication secret.
- Digit semantics are NOT verified: no legend explains 25, 06, 04, or 0062. Predictability is high at the syntax and username layers, low at the enrollment-allocation layer. Do not publish a decoder.
- Public exposure is narrow but material: one full example sits in an official PDF; the onboarding guide documents the registration-number field and its profile context (name, branch, DOB, phone, email, addresses, parent details, uploaded documents, OTP via parent mobile).
- No bulk register-number lists were verified in circulars, result PDFs, placement pages, or LinkedIn. That negative result is not proof of absence; those channels should be monitored.
- SlcmPlus does local DOM math on attendance, marks, and grades pages without external transmission; it proves sensitive page categories exist, not an IDOR.
- The threat is compositional: public name plus number completes the username; consequences depend on response behavior, MFA, rate limits, and object authorization.
- Account discovery and credential stuffing are more direct consequences than IDOR because the username grammar is public.
- Safe validation uses only synthetic accounts and preapproved identities; no neighboring-number tests, no guessed usernames against production.

## KEY FACTS
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - official FAQ with the username formula, example garv.2506040062, and Outlook password guidance.
- https://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf - registration number is MUJ-generated and non-editable; profile data model with parent mobile OTP.
- https://github.com/Tejas-Narula/SlcmPlus/blob/main/manifest.json - manifest naming three MUJ SLCM page categories: attendance summary, internal marks, grades.
- https://github.com/Tejas-Narula/SlcmPlus/blob/main/content.js - reads attendance counts, marks, credits, letter grades from rendered tables; no external transmission call.
- https://github.com/DK10WS/SLCM_APP - third-party Flutter and FastAPI mobile project advertising schedules, grades, GPA, attendance, custom authentication.
- http://github.com/AddisionS/slcm-feedback-form-filler - automation of the MUJ SLCM feedback form.
- http://github.com/sankalp2004/SLCM-is-Dumb/blob/master/config.py - targets slcm.manipal.edu, not the MUJ Jaipur host; use only as ecosystem context.
- http://github.com/canaryGrapher/slcmAPI/blob/master/package.json - separate Manipal SLcM scraping API, same attribution caveat.
- http://login.microsoftonline.com/muj.manipal.edu/.well-known/openid-configuration - public OpenID metadata linking the muj.manipal.edu namespace to Microsoft login infrastructure.
- https://owasp.org/www-community/attacks/Credential_stuffing - stuffing uses breached username and password pairs; MFA recommended.
- https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html - login, reset, and recovery must not disclose whether an account exists; throttling controls.
- https://pages.nist.gov/800-63-4/sp800-63b.html - controls against online guessing: attempt limits, progressive delays, bot detection, adaptive signals.
- https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html - IDOR definition and per-object access check requirement.
- https://learn.microsoft.com/en-us/entra/identity/authentication/concept-mfa-howitworks - MFA overview used as the primary compensating control argument.
- https://learn.microsoft.com/en-us/entra/identity/authentication/howto-password-smart-lockout - Entra smart lockout as a candidate hardening reference.

## ACTIONABLE LEADS
- Re-verify the FAQ PDF and the example; request replacement of realistic examples with synthetic placeholders and removal of cached copies.
- Run offline scans of jaipur.manipal.edu PDFs, text layers, spreadsheets, public shares, and repository history for name-number pairs.
- Compare login, reset, and recovery responses for preapproved existing versus nonexistent synthetic accounts for message, status, and timing equivalence.
- Authorized review of attendance, marks, grades, profile, document, and parent-facing routes for object-level authorization with synthetic students.
- Ask MUJ for a redacted registration-number legend under authorization; do not infer digit meanings from one example.
- Evaluate MFA coverage, throttling, and breach-based password protection with owner-observed test accounts only.

## FLAGS
- The example number 2506040062 came from the user plus the FAQ; the phrase "password as per official outlook ID" is FAQ-attributed but the report did not re-fetch the PDF. Re-verify before citing.
- All digit-field meanings are Inference or Unknown; the report explicitly forbids presenting a decoder as fact.
- Bulk exposure channels are Not verified; absence in this review is not proof of absence.
- Third-party repos may be stale; anything targeting slcm.manipal.edu must not be attributed to mujslcm.jaipur.manipal.edu.
- Reference 13 is a garbled Devanagari text layer of a MeitY PDF cited for the DPDP Act; the report disclaims legal advice.
- SlcmPlus claims are based on public manifest and content.js only; extension behavior on real pages was not executed by this report.

## COVERAGE
- File read to EOF: 241 lines, 35582 chars (file_size 35582), truncated: false. Confirmed EOF at line 241, final reference.