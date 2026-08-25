## REPORT (w1-10-sso-entra.md: MUJ Identity Federation: Verified Surface and Defensible Inferences)

## ANSWER SUMMARY
- Microsoft OpenID metadata resolves three separate Entra tenants: jaipur.manipal.edu (7d0726e8-bf4b-4ac1-99f1-010fb11f1d3f, alias mujcampus.onmicrosoft.com), muj.manipal.edu (27282fdd-4c0b-4dfb-ba91-228cd83fdf71, alias mujmanipal.onmicrosoft.com), and the manipal.edu root (29bebd42-f1ff-4c3d-9688-067e3460dc1f, alias learnermanipal.onmicrosoft.com).
- Both MUJ namespaces return NameSpaceType=Managed with brand "Manipal University Jaipur" and no external AuthURL; evidence favors Microsoft cloud authentication and does not support a current AD FS claim.
- SLCM federation is unproven: both indexed SLCM pages show a local form submission plus a passwordreset.microsoftonline.com link, with no public OIDC, SAML, or WS-Fed authorization redirect.
- MUJ's publicly reachable June 2025 Office 365 SOP (IT-SOP-O365-001, version 1.0) documents mandatory MFA setup before Office 365 use and a two-step SSPR flow; it is a strong enrollment signal, not proof of Conditional Access enforcement on every login.
- Mail is verified Microsoft 365: Exchange Online Protection MX for all three domains, SPF ending in -all, Microsoft DKIM selector CNAMEs published; DMARC is monitoring-only (p=none explicit for jaipur and manipal.edu; muj.manipal.edu NXDOMAIN inherits the root p=none per RFC 7489).
- The three domains map to different tenant GUIDs, so email-suffix-based authorization is unsafe; exact issuer, tid, and audience validation is the highest-value control.
- Enumeration, password spraying, and token tampering are not authorized by public metadata; the report's safe path is synthetic accounts, staging, and admin-side log and policy review.

## KEY FACTS
- https://login.microsoftonline.com/jaipur.manipal.edu/.well-known/openid-configuration - resolves tenant 7d0726e8-bf4b-4ac1-99f1-010fb11f1d3f with sts.windows.net issuer.
- https://login.microsoftonline.com/muj.manipal.edu/.well-known/openid-configuration - resolves second MUJ tenant 27282fdd-4c0b-4dfb-ba91-228cd83fdf71, distinct from the first.
- https://login.microsoftonline.com/manipal.edu/.well-known/openid-configuration - root domain tenant 29bebd42-f1ff-4c3d-9688-067e3460dc1f, brand Manipal Academy of Higher Education.
- https://login.microsoftonline.com/mujcampus.onmicrosoft.com/.well-known/openid-configuration - alias returns the same GUID as jaipur.manipal.edu, confirming the tenant mapping.
- https://login.microsoftonline.com/mujmanipal.onmicrosoft.com/.well-known/openid-configuration - alias returns the same GUID as muj.manipal.edu.
- https://login.microsoftonline.com/getuserrealm.srf?login=probe@jaipur.manipal.edu&xml=1 - realm response: Managed, brand Manipal University Jaipur, no external AuthURL.
- https://login.microsoftonline.com/getuserrealm.srf?login=probe@muj.manipal.edu&xml=1 - same Managed classification for the second namespace.
- https://login.microsoftonline.com/jaipur.manipal.edu/federationmetadata/2007-06/federationmetadata.xml - WS-Fed metadata is Microsoft Entra STS output, not proof of an MUJ AD FS farm.
- https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf - MUJ Office 365 SOP; documents mandatory MFA registration and two-step SSPR; marked "For Internal Use Only" yet public.
- https://dns.google/resolve?name=jaipur.manipal.edu&type=MX - MX target jaipur-manipal-edu.mail.protection.outlook.com, verifying Exchange Online Protection.
- https://dns.google/resolve?name=jaipur.manipal.edu&type=TXT - SPF includes spf.protection.outlook.com and a._spf.brightspace.com, hard-fail -all.
- https://dns.google/resolve?name=_dmarc.jaipur.manipal.edu&type=TXT - DMARC p=none with aggregate report mailbox dmarc@jaipur.manipal.edu.
- https://dns.google/resolve?name=_dmarc.muj.manipal.edu&type=TXT - NXDOMAIN, so RFC 7489 discovery falls back to the organizational domain policy.
- https://mujslcm.jaipur.manipal.edu/ - target portal exposing @muj.manipal.edu suffix, student/parent modes, local form, and the Microsoft reset link.
- https://www.rfc-editor.org/rfc/rfc7489.html - the DMARC subdomain fallback rule that makes muj.manipal.edu inherit p=none.

## ACTIONABLE LEADS
- Authorized browser trace with one synthetic test account on both SLCM hostnames: record the full HTTP 302 chain to see whether it hits login.microsoftonline.com /authorize or /wsfed, a SAML IdP, or stays on the local form.
- Once the protocol is known, staging tests: wrong issuer, wrong audience, expired or replayed tokens, missing nonce or InResponseTo, and cross-tenant token acceptance (a token minted for the other MUJ tenant presented to SLCM).
- Check whether SLCM authorization binds tenant/object identifiers or mutable mail aliases; the two-tenant finding makes suffix-only trust the main confused-deputy risk.
- Entra admin-side review: Conditional Access coverage for both MUJ tenants, smart lockout, banned password list, legacy authentication blocking, Identity Protection, and sign-in logs around reset events; no live spraying.
- SSPR tests with dedicated synthetic accounts per tenant: method registration, reset audit events, notification behavior, help-desk override paths, and post-reset session revocation.
- Parent/student role boundary tests with paired authorized accounts: role claims, object-level authorization, session rotation, and client-side role parameter tampering.
- Email follow-up: collect DMARC aggregate reports (rua dmarc@jaipur.manipal.edu), inventory all legitimate senders, verify SPF/DKIM alignment with controlled messages, then phase DMARC from p=none toward quarantine and reject.
- Re-check the SOP PDF: it is an internal-use document on a public URL, which is an information-disclosure observation, and its content may drift from live configuration.

## FLAGS
- SLCM federated login (OIDC, SAML, or WS-Fed) is unverified; the reset link alone is not proof of SSO. Any parent-level claim that SLCM "uses Entra SSO" would be overreach.
- AD FS absence is inferred from Managed realm responses; password hash sync or pass-through authentication behind the cloud UI cannot be excluded from public data.
- MFA evidence is enrollment language from a single June 2025 SOP; universal Conditional Access enforcement is Low to moderate confidence.
- The SOP PDF is marked "For Internal Use Only" but is public; flag as a real finding, but it does not prove current production settings.
- muj.manipal.edu DMARC inheritance depends on RFC 7489 logic and the root record having no sp override; re-verify DNS before citing.
- Tenant GUIDs, aliases, MX, and SPF are point-in-time public answers; they can change and are not secrets.
- Two reference URLs are German and Thai locale variants of Microsoft ID-token docs (learn.microsoft.com/de-de, /th-th); content equivalence with the English pages is unverified and they look like search artifacts.
- No live probing was performed by the report; any enumeration, spraying, or token manipulation done downstream would require separate written authorization.

## COVERAGE (44955 chars as read, read verified to EOF, 307 lines)