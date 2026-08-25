# MUJ Identity Federation: Verified Surface and Defensible Inferences

## Executive Summary

- **Two Distinct MUJ Tenants**: Microsoft OpenID metadata resolves `jaipur.manipal.edu` to tenant `7d0726e8-bf4b-4ac1-99f1-010fb11f1d3f` and `muj.manipal.edu` to `27282fdd-4c0b-4dfb-ba91-228cd83fdf71` [5][7]. The corresponding public `onmicrosoft.com` names are `mujcampus.onmicrosoft.com` and `mujmanipal.onmicrosoft.com`, respectively [44][48]. -> MUJ should treat tenant selection and exact issuer validation as material security controls, not assume all `manipal.edu` identities belong to one directory.

- **Cloud-Managed, Not Publicly AD FS-Federated**: Microsoft's public realm-discovery responses classify both MUJ namespaces as `Managed`, identify the brand as `Manipal University Jaipur`, use `microsoftonline.com`, and expose no external authentication URL [6][1]. -> The available evidence favors Microsoft cloud authentication for these domains; it does not support a current AD FS claim.

- **SLCM Federation Remains Unproven**: The two indexed SLCM surfaces show MUJ sign-in, student/parent choices, and the `@jaipur.manipal.edu` or `@muj.manipal.edu` suffixes [2][3]. Static HTML inspection finds a local form submission and a link to `https://passwordreset.microsoftonline.com/`, but no public OIDC, SAML, or WS-Fed authorization redirect. -> Describe the relationship as a verified shared Entra identity lifecycle, not verified SSO federation, until an authorized redirect trace or application configuration establishes the protocol.

- **Official MFA Evidence Exists**: MUJ's publicly accessible June 2025 Office 365 SOP says users must complete MFA setup before using Office 365 and documents Microsoft Authenticator, phone, and email security-information methods [9]. -> Confidence is high that MFA enrollment is part of MUJ's Microsoft 365 onboarding, but the document does not prove that every SLCM login is protected by Conditional Access.

- **SSPR Is More Than a Mere Link, But Scope Is Unknown**: Microsoft says the password-reset portal first checks whether a user is enabled for self-service password reset and has the required authentication methods [41]. MUJ's SOP documents two-step identity verification followed by password creation [9]. -> SSPR appears operational for the intended Office 365 population, but public evidence cannot prove universal or current enablement for every student, employee, tenant, or SLCM account.

- **Microsoft 365 Mail Is Unambiguous**: The MX records for `jaipur.manipal.edu`, `muj.manipal.edu`, and `manipal.edu` point to Microsoft Exchange Online Protection hosts [12][14][18]. Their canonical SPF records end in `-all`, and standard Microsoft DKIM selector CNAMEs are published [22][16][24]. -> Microsoft 365 mail routing and sender authorization are verified; actual DKIM signing should still be checked in authorized message headers.

- **DMARC Is Monitoring-Only**: `jaipur.manipal.edu` explicitly publishes `p=none`, while `manipal.edu` also publishes `p=none` [15][11]. `_dmarc.muj.manipal.edu` returned NXDOMAIN [10], so RFC 7489 discovery falls back to the organizational domain and applies its `p` policy when no `sp` override exists [49]. -> The effective posture is monitoring rather than receiver-requested quarantine or rejection, leaving room to improve anti-spoofing enforcement after validating legitimate senders.

- **The Safest Test Is Configuration-Led**: Microsoft treats Conditional Access as a signal-driven policy engine and provides tenant-side policy and "What If" views to authorized roles [42]. Microsoft also documents password-spray investigation as incident response, including failed sign-ins, unexpected MFA prompts, and remediation [43]. -> Use test accounts, tenant configuration, logs, staging, and written authorization; do not run live user enumeration, password spraying, or token manipulation against production on the strength of public metadata alone.

## Scope, Method, and Evidence Grades

This review uses only publicly reachable web pages, Microsoft discovery documents, Microsoft user-realm responses, DNS-over-HTTPS answers, an official MUJ Office 365 SOP, and defensive guidance from Microsoft, OWASP, the RFC Editor, and CISA/NIST-adjacent standards sources. It does not authenticate to an MUJ account, submit passwords, enumerate named users, exercise password reset for a person, or tamper with a production token.

The report provides an auditable evidence-to-conclusion rationale rather than private internal deliberation. Each important conclusion is classified as one of three levels:

| Evidence grade | Meaning in this report | Example |
|---|---|---|
| Verified public record | A first-party endpoint or authoritative DNS response directly states the value. | Tenant GUID, `NameSpaceType=Managed`, MX target, SPF text, DMARC policy. |
| Strong inference | Several verified records support the conclusion, but application configuration remains private. | Microsoft 365 is MUJ's mail and identity backbone; the password-reset workflow is integrated with the Office 365 identity lifecycle. |
| Unknown or unverified | Public evidence cannot settle the point without authorized interaction or administrator access. | Whether SLCM uses OIDC, SAML, WS-Fed, password validation through another service, or a separate synchronized credential store. |

This distinction matters because Microsoft publishes several kinds of metadata independently of any particular application. An Entra OpenID document proves that a domain is registered in a tenant and provides tenant-specific protocol endpoints. A WS-Federation metadata document proves that Microsoft's security token service publishes WS-Fed metadata for that tenant. Neither one proves that the SLCM application is configured as a relying party for the relevant protocol [5][8].

Likewise, a `passwordreset.microsoftonline.com` link proves that the page sends users to Microsoft's SSPR service. It does not, by itself, prove that the portal delegates its primary login to Entra. Microsoft's own documentation says the reset service evaluates enablement and registered methods only after the user enters the workflow [41]. MUJ's separate onboarding SOP is the stronger evidence that Office 365 identities and reset methods are operational for at least the document's intended student and employee audience [9].

## Three Entra Tenants Exposed by Public Metadata

### Exact tenant-discovery table

| Public namespace queried | OpenID tenant ID and issuer | Matching public tenant alias | Realm type and brand | Evidence-bounded conclusion |
|---|---|---|---|---|
| `jaipur.manipal.edu` | `7d0726e8-bf4b-4ac1-99f1-010fb11f1d3f`; issuer `https://sts.windows.net/7d0726e8-bf4b-4ac1-99f1-010fb11f1d3f/` [5] | `mujcampus.onmicrosoft.com` returns the same GUID [44] | `Managed`; `Manipal University Jaipur`; `microsoftonline.com`; no external `AuthURL` [6] | Verified separate MUJ cloud tenant. No public indication that this namespace redirects to AD FS. |
| `muj.manipal.edu` | `27282fdd-4c0b-4dfb-ba91-228cd83fdf71`; issuer `https://sts.windows.net/27282fdd-4c0b-4dfb-ba91-228cd83fdf71/` [7] | `mujmanipal.onmicrosoft.com` returns the same GUID [48] | `Managed`; `Manipal University Jaipur`; `microsoftonline.com`; no external `AuthURL` [1] | Verified second MUJ cloud tenant, distinct from `jaipur.manipal.edu`. |
| `manipal.edu` | `29bebd42-f1ff-4c3d-9688-067e3460dc1f`; issuer `https://sts.windows.net/29bebd42-f1ff-4c3d-9688-067e3460dc1f/` [46] | `learnermanipal.onmicrosoft.com` returns the same GUID [47] | `Managed`; `Manipal Academy of Higher Education`; `microsoftonline.com`; no external `AuthURL` [45] | Verified root-domain tenant, distinct from both MUJ tenant GUIDs. |

The non-obvious finding is not merely that MUJ uses Entra ID. It is that the public namespace structure maps to at least three directories: two branded for Manipal University Jaipur and one for the broader Manipal Academy of Higher Education. That separation may reflect history, populations, licensing, organizational boundaries, or migration. Public records do not establish the reason.

The security implication is concrete. A relying party that is meant for one directory should validate the exact issuer and tenant, rather than accept any token whose email ends in a broadly related domain. Microsoft instructs resource servers to validate `aud`, validate `iss` against the appropriate OpenID document, ensure `tid` is a GUID, and use the tenant value when associating data with a subject [40]. Accepting a token for the wrong resource creates a confused-deputy risk [40]. In a multi-tenant Manipal environment, loose suffix-based authorization would be especially dangerous because the visible domains do not all identify the same tenant.

### Federation metadata does not mean AD FS

The public `FederationMetadata.xml` for `jaipur.manipal.edu` identifies tenant `7d0726e8-bf4b-4ac1-99f1-010fb11f1d3f`, issuer `https://sts.windows.net/7d0726e8-bf4b-4ac1-99f1-010fb11f1d3f/`, and Microsoft's tenant WS-Fed endpoint [8]. The equivalent document for `muj.manipal.edu` identifies tenant `27282fdd-4c0b-4dfb-ba91-228cd83fdf71` and its Microsoft WS-Fed endpoint [4]. These are Microsoft Entra security-token-service documents, not evidence of an MUJ-operated AD FS farm.

The decisive public discriminator is the realm result. Both domains return `Managed`, not `Federated`, and neither publishes an external authentication URL in that response [6][1]. The root `manipal.edu` namespace behaves the same way [45]. Therefore:

1. **Verified**: Microsoft Entra hosts identity metadata and cloud sign-in endpoints for all three namespaces.
2. **Strong inference**: Primary authentication for those namespaces is cloud-managed at the time of observation.
3. **Not supported**: A claim that MUJ currently sends these domain users to on-premises AD FS.
4. **Still possible but unproven**: Password hash synchronization, pass-through authentication behind the cloud experience, directory synchronization, or application-specific federation. The public realm response does not disclose every back-end identity component.

The operational recommendation is to inventory all three tenant GUIDs in the institution's application catalog, verify intended cross-tenant access, and monitor accidental use of a root-domain authority where an MUJ-specific authority was intended.

## Microsoft 365 Mail: Strong SPF, Monitoring-Only DMARC

### Exact DNS record table

| Domain and record | Exact public answer | Security interpretation |
|---|---|---|
| `jaipur.manipal.edu` MX | `0 jaipur-manipal-edu.mail.protection.outlook.com.` [12] | Verified Exchange Online Protection inbound routing. |
| `jaipur.manipal.edu` SPF | `v=spf1 include:spf.protection.outlook.com include:a._spf.brightspace.com -all` [22] | Microsoft 365 and Brightspace are named in the canonical SPF policy; `-all` is a hard-fail qualifier. Additional TXT fragments exist, but strings without `v=spf1` are not treated here as independent canonical SPF policies. |
| `_dmarc.jaipur.manipal.edu` TXT | `v=DMARC1; p=none; rua=mailto:dmarc@jaipur.manipal.edu` [15] | Aggregate reporting is requested, but the published policy asks for monitoring, not quarantine or rejection. |
| `selector1._domainkey.jaipur.manipal.edu` CNAME | `selector1-jaipur-manipal-edu._domainkey.mujcampus.onmicrosoft.com.` [23] | Microsoft 365 DKIM selector is provisioned. |
| `selector2._domainkey.jaipur.manipal.edu` CNAME | `selector2-jaipur-manipal-edu._domainkey.mujcampus.onmicrosoft.com.` [19] | Second Microsoft 365 rollover selector is provisioned. |
| `muj.manipal.edu` MX | `0 muj-manipal-edu.mail.protection.outlook.com.` [14] | Verified Exchange Online Protection inbound routing for the second MUJ namespace. |
| `muj.manipal.edu` SPF | `v=spf1 include:spf.protection.outlook.com -all` [16] | Only Microsoft's SPF include is named in the returned canonical policy; unauthorized sources receive hard-fail treatment at the SPF layer. |
| `_dmarc.muj.manipal.edu` TXT | NXDOMAIN, status 3 [10] | No subdomain-specific override was found. RFC policy discovery therefore falls back to the organizational domain. |
| `selector1._domainkey.muj.manipal.edu` CNAME | `selector1-muj-manipal-edu._domainkey.mujmanipal.onmicrosoft.com.` [13] | Microsoft 365 DKIM selector is provisioned for the second MUJ tenant. |
| `selector2._domainkey.muj.manipal.edu` CNAME | `selector2-muj-manipal-edu._domainkey.mujmanipal.onmicrosoft.com.` [17] | Second Microsoft 365 selector is provisioned. |
| `manipal.edu` MX | `0 manipal-edu.mail.protection.outlook.com.` [18] | Verified Exchange Online Protection inbound routing for the root domain. |
| `manipal.edu` SPF | `v=spf1 ip4:167.89.84.13/32 include:spf.protection.outlook.com include:a._spf.brightspace.com include:sendgrid.net include:_spf.salesforce.com -all` [24] | The root domain authorizes a dedicated IP plus Microsoft 365, Brightspace, SendGrid, and Salesforce, ending in hard fail. |
| `_dmarc.manipal.edu` TXT | `v=DMARC1; p=none;` [11] | Monitoring-only organizational policy. No `sp` override appears in the returned value. |
| `selector1._domainkey.manipal.edu` CNAME | `selector1-manipal-edu._domainkey.learnermanipal.onmicrosoft.com.` [21] | Microsoft 365 DKIM selector maps to the root-domain tenant alias. |
| `selector2._domainkey.manipal.edu` CNAME | `selector2-manipal-edu._domainkey.learnermanipal.onmicrosoft.com.` [20] | Second Microsoft 365 selector is provisioned. |

Three conclusions follow from the table.

First, Microsoft 365 mail use is not an inference based only on a portal logo. Each domain's MX target is in `mail.protection.outlook.com`, and each domain publishes the standard two Microsoft DKIM selector aliases. The selector targets also independently corroborate the tenant-alias mapping: `mujcampus`, `mujmanipal`, and `learnermanipal`.

Second, SPF is comparatively strict because each canonical policy ends in `-all`. That is valuable but not equivalent to complete spoofing protection. SPF evaluates authorized sending infrastructure, while DMARC determines how receivers should handle alignment failures. The published DMARC policies for `jaipur.manipal.edu` and `manipal.edu` are both `p=none` [15][11].

Third, the lack of a local `_dmarc.muj.manipal.edu` record does not mean the subdomain is outside DMARC. RFC 7489 says a receiver that finds no policy at the subdomain must query the organizational domain; if that record lacks `sp`, the `p` policy applies [49]. Consequently, `muj.manipal.edu` inherits the root's `p=none` posture. All three reviewed namespaces therefore have monitoring-only DMARC disposition, either explicitly or by inheritance.

### Spoofing posture

The posture is mixed rather than simply secure or insecure:

- **Positive controls**: Microsoft 365 MX routing, hard-fail SPF, Microsoft DKIM selector publication, and a DMARC aggregate-report mailbox for the Jaipur namespace are all visible.
- **Residual weakness**: `p=none` asks receivers to observe rather than enforce a quarantine or reject outcome. A determined impersonation attempt may still be delivered depending on receiver behavior, alignment, reputation, and other filtering.
- **Unknown**: CNAME publication does not prove every legitimate stream currently carries a valid DKIM signature. That requires controlled message-header inspection.
- **Migration risk**: The root SPF policy names several third-party senders [24]. Moving directly to enforcement without classifying and aligning each sender could disrupt legitimate mail.

A responsible improvement path is to review aggregate reports, inventory every legitimate source, confirm SPF or DKIM alignment, test lower-risk subdomains, then phase DMARC from `none` toward `quarantine` and finally `reject`. This should be an administrator-led mail-governance project, not an external test.

## SLCM Sign-In: Shared Identity Lifecycle, Protocol Unproven

### What the public portal actually establishes

Two SLCM hostnames are publicly indexed:

| Portal | Publicly visible behavior | What it proves | What it does not prove |
|---|---|---|---|
| `https://muj.slcm.jaipur.manipal.edu/` | MUJ sign-in page, `@jaipur.manipal.edu`, student and parent login choices, and "Forgot Password" [2] | The portal recognizes a Jaipur institutional namespace and separate user modes. | No public response identifies OIDC, SAML, WS-Fed, a client ID, or an Entra reply URL. |
| `https://mujslcm.jaipur.manipal.edu/` | MUJ sign-in page, `@muj.manipal.edu`, parent/student choices, and "Forgot Password" [3] | The portal also recognizes the second MUJ namespace. | No public response establishes a Microsoft authorization redirect or token type. |
| Both static pages | Direct HTML inspection shows a local form action and a link to `https://passwordreset.microsoftonline.com/`. | Password recovery is connected to Microsoft's work/school account lifecycle. | A reset link is not proof that primary SLCM authentication is delegated to Entra. |

This distinction changes the central verdict. The observed page looks like an application collecting a local identifier/password form, not like a landing page that immediately issues a 302 redirect to `login.microsoftonline.com/{tenant}/oauth2/...`. There may still be an Entra-backed validation process behind the form, but public static content cannot identify it. Possibilities include an undisclosed SAML or WS-Fed flow after submission, API-based credential validation, synchronized credentials, or a separate application account. Stating which one is in use would be speculation.

The publicly indexed suffixes also explain why tenant separation matters. A faculty or employee path could be associated with `jaipur.manipal.edu`, while a student path could use `muj.manipal.edu`; the HTML and search results expose both modes, but no public policy document authoritatively maps every population. Application authorization should therefore rely on immutable tenant and object identifiers rather than only the typed suffix.

### How ASP.NET MVC commonly integrates with Entra

The `/Home/Index` style route, jQuery validation, and anti-forgery markup observed in the static page are consistent with a Microsoft web stack, but they are not enough to identify a framework version or federation protocol. Microsoft documents modern Entra integration for ASP.NET MVC and Web API applications through `Microsoft.Identity.Web.OWIN` on .NET Framework 4.7.2 or later [33]. Its OIDC pattern is identifiable in application configuration by `UseOpenIdConnectAuthentication`, an authority, client ID, redirect URI, response type, and token-validation parameters [33]. None of those private configuration artifacts is publicly available for SLCM.

| Pattern | Typical browser/application behavior | Security controls | MUJ-specific status |
|---|---|---|---|
| OpenID Connect with OAuth 2.0 authorization code | Browser is sent to Entra `/authorize`; the app receives a response at a registered redirect URI and redeems a code at `/token` [31]. | Validate `state`, `nonce`, signature, issuer, audience, tenant, redirect URI, and authorization code handling [31]. | OpenID metadata exists, but no public SLCM redirect proves use. |
| WS-Federation | Relying party redirects to a WS-Fed sign-in endpoint and consumes a signed security token. Tenant WS-Fed endpoints appear in Microsoft's federation metadata [8][4]. | Pin trusted issuer/signing metadata, validate audience and reply URL, enforce time and replay controls. | Metadata exists, but no SLCM request proves it is the selected protocol. |
| SAML 2.0 | Service provider sends an authentication request to an IdP and receives a signed response at its assertion consumer service. | Validate schema, signature, `Destination`, `Audience`, `Recipient`, `InResponseTo`, time bounds, and replay [50]. | No public SLCM SAML request, entity ID, or ACS URL was found. |
| Local form plus back-end identity integration | Portal collects credentials or an application identifier and calls an undisclosed back-end service. | Never expose credentials to unnecessary components; protect sessions, rate-limit failures, and avoid account-disclosing errors. | Most consistent with the unauthenticated static presentation, but back-end behavior remains unknown. |

For OIDC, Microsoft says `state` should be a random unique value and must match between request and response to resist CSRF; `nonce` should be verified to mitigate token replay [31]. Microsoft also recommends using a validation library instead of implementing ID-token validation manually [31]. For SAML, OWASP requires secure signature handling and exact validation of `Destination`, `Audience`, recipient, `InResponseTo`, and validity intervals [50]. These are the controls an authorized SLCM review should examine once the actual protocol is known.

## MFA and Password Recovery: Official 2025 Evidence

MUJ's official document is titled "How To Setup Your Office 365 Mail ID," identifies IT Services, carries document number `IT-SOP-O365-001`, version 1.0, and says it is effective June 2025 for students and employees [9]. Although the PDF says "For Internal Use Only," it is publicly reachable on an official MUJ web domain. That makes it meaningful public evidence, while not turning it into proof of the present configuration of every account.

The onboarding sequence is explicit. Users navigate to Microsoft's sign-in service, enter their university mail ID and temporary/current password, change the password, and then receive a "More information required" prompt [9]. The SOP then says: "You must complete the MFA setup process before you can use Office 365" [9]. It lists Microsoft Authenticator, phone, and email among security-information methods [9].

That is strong evidence of mandatory MFA registration in the Office 365 onboarding journey. It is not the same as proof that every authentication event requires a second factor. Entra Conditional Access evaluates user, group, location, device, application, risk, and other signals, and enforcement occurs after first-factor authentication [42]. A policy can require MFA, authentication strength, compliant devices, approved applications, or other controls [42]. The actual tenant policies are visible to authorized roles in the Entra admin center, not in public metadata [42].

The careful conclusion is therefore:

- **Verified**: MFA enrollment is part of the documented 2025 Office 365 setup for the SOP's student and employee audience.
- **Likely**: At least some Microsoft 365 access is gated on registration or an MFA-related requirement.
- **Unknown**: Whether every user is in scope, whether legacy protocols are blocked, which authentication strengths are accepted, whether number matching or phishing-resistant methods are required, and whether SLCM itself is a Conditional Access-protected enterprise application.

### SSPR interpretation

Microsoft defines SSPR as allowing a user to change or reset a password without administrator or help-desk involvement [41]. The public portal checks whether the user is enabled and whether the authentication methods required by policy are registered [41]. Microsoft also notes that SSPR is not simply enabled for every tenant by default [41].

MUJ's SOP instructs a user to select "Forgot my password," choose a verification method, complete two-step identity verification, and then create a new password [9]. This is stronger than the SLCM link alone: it documents MUJ's intended operational reset process. Even so, group scoping and current account eligibility remain private. A user outside the enabled scope could still reach the same Microsoft portal and be told to contact an administrator [41].

The recovery surface deserves the same rigor as primary sign-in. MUJ should require strong registered methods, prevent weak recovery methods from bypassing stronger sign-in controls, protect help-desk overrides, and alert on method changes and unusual reset attempts.

## Associated Identity Surfaces

The public identity estate includes more than the SLCM page:

1. **Microsoft Office 365 sign-in**: MUJ's SOP sends students and employees to `https://login.microsoftonline.com/`, uses the university mail ID, and documents password change, MFA registration, security information, and reset [9].
2. **Microsoft password reset**: Both SLCM pages link to `https://passwordreset.microsoftonline.com/`, the Microsoft SSPR service described in Microsoft's documentation [41].
3. **Two MUJ mail namespaces**: The SLCM surfaces expose `@jaipur.manipal.edu` and `@muj.manipal.edu` [2][3]. Each maps to a different Entra tenant [5][7].
4. **Root Manipal identity**: `manipal.edu` maps to tenant `29bebd42-f1ff-4c3d-9688-067e3460dc1f`, brand `Manipal Academy of Higher Education`, and alias `learnermanipal.onmicrosoft.com` [45].
5. **Microsoft mail protection and DKIM aliases**: Exchange Online Protection MX records and `onmicrosoft.com` DKIM targets expose which cloud mail systems correspond to the public namespaces [12][14][18].
6. **Parent/student application modes**: Public SLCM pages identify distinct parent and student login paths [2][3]. That is an application authorization boundary that deserves separate role and session testing.

The attack surface is therefore a federation and lifecycle graph, not one login form. Identity proofing at enrollment, temporary passwords, MFA registration, password recovery, tenant routing, SLCM session creation, parent access, Microsoft 365 tokens, and email recovery messages all participate in the security outcome.

## Identity Attack Surface and Authorized Test Plan

### Risk register

| Surface | Publicly supported risk hypothesis | Consequence if mishandled | Responsible validation |
|---|---|---|---|
| Tenant and realm discovery | Domain queries reveal tenant GUIDs, brand names, managed status, and aliases [5][7]. | Better-targeted phishing, tenant confusion, and overbroad trust configuration. | Passively inventory domains and compare them with the authorized tenant/application catalog. Do not treat tenant IDs as secrets. |
| Account enumeration | Different login, reset, or parent/student responses may disclose whether an identifier exists. OWASP recommends equivalent behavior for failed authentication outcomes [37]. | Enables targeted social engineering and credential attacks. | With written authorization, use only named synthetic existing and nonexistent accounts; compare status, text, size, and timing at very low volume. Stop if real identities or notifications are involved. |
| Password spraying | Microsoft associates large failed-sign-in volumes, unusual activity, and unexpected MFA prompts with investigation indicators [43]. | Password compromise, lockouts, MFA fatigue, incident-response cost, and possible account compromise. | Do not spray production. Review Entra sign-in logs, Identity Protection, smart lockout, banned-password policy, legacy authentication, and Conditional Access. Use a lab or formally approved synthetic-account exercise only. |
| Cross-tenant token acceptance | MUJ-related suffixes map to different tenant IDs [5][7][46]. | A valid token from the wrong Manipal tenant could be accepted if authorization uses email suffix alone. | In staging, present valid test tokens from each authorized tenant and verify exact issuer, `tid`, audience, object identity, and role mapping. |
| OIDC implementation | Incorrect `state`, `nonce`, issuer, signature, or audience validation permits CSRF, replay, or token substitution [40][31]. | Session takeover or confused-deputy authorization. | Review library configuration and execute negative tests in staging using expired, wrong-audience, wrong-issuer, and replayed synthetic tokens. Do not tamper with live users' tokens. |
| SAML or WS-Fed implementation | Weak signature or destination checks, XML wrapping, long validity, or missing replay controls can make assertions portable or forgeable. | Unauthorized SLCM sessions. | If the protocol is confirmed, validate schema, signature, trusted certificate, audience, destination, recipient, `InResponseTo`, time bounds, and replay detection [50]. |
| SSPR and recovery | The portal exposes a recovery entry point, and MUJ documents two-step verification [9]. | Recovery could become a weaker path than primary authentication; notification abuse can affect users. | Use two dedicated test accounts in each tenant; verify method registration, reset audit events, notifications, help-desk override, and post-reset session revocation. |
| Parent/student boundary | SLCM exposes separate parent and student modes [2][3]. | Role confusion, insecure direct object reference, or session crossover. | Use paired authorized test identities; verify role claims, object-level authorization, logout, session rotation, and prohibition on changing role by client-side parameters. |
| Email spoofing | DMARC is `p=none` explicitly or by inheritance [15][10][11][49]. | Lookalike or direct-domain impersonation may be more deliverable than under enforcement. | Analyze aggregate reports and controlled messages. Verify SPF/DKIM alignment before phased enforcement. |

### Why user enumeration must remain bounded

Public Entra metadata discovery is domain-level and does not require testing whether a named person has an account. Moving from tenant discovery to identity enumeration is a meaningful boundary. Error text, reset behavior, response timing, MFA prompts, and notifications can affect real users even when no password is attempted.

A defensible assessment uses two or three institution-created synthetic identities, one deliberately nonexistent identifier, a documented maximum request count, source IPs known to the security team, and a pre-agreed stop condition. The desired result is uniform external behavior and rich internal telemetry. The assessor should not build a student directory, infer enrollment status, or probe names gathered from public sources.

### Why password spraying is not a public-information test

Tenant IDs, MX records, and a public login page do not authorize credential testing. Password spraying changes system state, can trigger lockouts or alerts, creates privacy issues in sign-in logs, and can compromise an account if a password is valid. Microsoft's incident-response guidance recommends investigating successful sign-ins, failed MFA after a correct password, attacker IPs, data access, and possible exfiltration [43]. Its remediation includes password change, blocking compromised users and attacker IPs, blocking legacy authentication, enabling MFA and Identity Protection, and using banned-password lists [43].

For MUJ, the safer control assessment is to inspect smart-lockout settings, sign-in logs, risk detections, authentication methods, legacy protocol use, named locations, and Conditional Access. If management still requires a live resistance test, it needs explicit written scope, synthetic accounts, an agreed rate, monitoring, rollback, and incident contacts. It should never use real students' or employees' identities.

### Protocol-specific validation plan

An authorized browser trace with one test account should answer the currently unknown SLCM question without broad probing:

1. Record the first-party SLCM URL and every HTTP 302 location without storing credentials or tokens in the report.
2. Determine whether the browser reaches a Microsoft `/authorize` or `/wsfed` endpoint, a SAML IdP endpoint, or remains on a local form.
3. Record only non-secret identifiers needed for validation: tenant authority, client or entity ID, registered reply/ACS URL, protocol, and expected issuer.
4. Compare those values with the Entra enterprise application or app registration owned by MUJ.
5. In staging, test wrong issuer, wrong audience, expired token/assertion, replay, missing nonce or `InResponseTo`, and tenant mismatch.
6. Confirm that application authorization uses stable object and tenant identifiers, not mutable mail aliases alone.
7. Verify session rotation after login, secure cookie settings, logout behavior, idle/absolute timeout, and revocation after password reset.

This approach maximizes evidence while minimizing impact. It also avoids the key analytical error in the original premise: equating a reset link with a proven SSO protocol.

## Synthesis

The identity environment has three layers that are related but not interchangeable.

| Dimension | Microsoft 365 and Entra tenants | SLCM application | Email authentication |
|---|---|---|---|
| Verified mechanism | Three managed Entra tenants expose OpenID/WS-Fed metadata; MUJ documents Office 365 setup, MFA, and SSPR [9]. | Public pages expose institutional suffixes, student/parent modes, local forms, and a Microsoft reset link [2][3]. | Exchange Online Protection MX, strict SPF, Microsoft DKIM CNAMEs, and DMARC `p=none`. |
| Scope | Cloud identity and Microsoft 365 lifecycle for documented students/employees. | Academic lifecycle and role access; exact identity-provider binding is private. | Mail receipt, sending authorization, signatures, alignment, and receiver disposition. |
| Main trade-off | Multiple tenants can preserve organizational boundaries but increase trust and routing complexity. | A local presentation can simplify user experience but obscures where and how credentials are validated. | Broad sender support preserves deliverability, while `p=none` avoids disruption but does not request enforcement. |
| Evidence gap | Conditional Access policy details, synchronization architecture, method strengths, and cross-tenant settings. | Actual protocol, client/entity ID, reply URL, token/assertion validation, and password-handling design. | Whether all live streams sign and align; readiness for quarantine/reject. |
| Security priority | Exact tenant/issuer authorization and consistent MFA/recovery governance. | Authorized protocol trace, configuration review, and role/session testing. | Sender inventory, alignment validation, and staged DMARC enforcement. |

The most important tension is that the strongest evidence of Microsoft integration sits outside the SLCM authentication transaction. DNS proves Microsoft 365 mail. Entra metadata proves tenant registration. The MUJ SOP proves an Office 365 onboarding, MFA-registration, and reset process. None of those artifacts exposes an SLCM OIDC request, SAML response, or WS-Fed redirect. The institution clearly has a Microsoft identity backbone, but the public record does not show exactly how SLCM consumes it.

A second tension is between strong enrollment language and unknown enforcement. MUJ says MFA setup must be completed before Office 365 use [9], while Microsoft explains that Conditional Access can vary by user, device, application, risk, and location [42]. Registration is verified; universal challenge behavior is not. This is why an administrator-side Conditional Access review is more probative than screenshots or student anecdotes.

A third tension is between mature Microsoft mail plumbing and weak DMARC disposition. The MX, SPF, and DKIM records are coherent and tenant-specific, but both explicit DMARC policies are `none`. That combination commonly reflects a legitimate migration stage: the institution has authentication mechanisms but has not yet asked receivers to reject failures. The appropriate action is evidence-led enforcement after sender cleanup, not an abrupt DNS change.

Finally, the separate tenant GUIDs create a non-obvious authorization risk. `jaipur.manipal.edu`, `muj.manipal.edu`, and `manipal.edu` look related to humans, but Entra treats them as different directory issuers [5][7][46]. Any SLCM design that trusts a suffix without binding it to the intended `tid`, `iss`, `aud`, and application role could collapse boundaries that the tenant architecture otherwise preserves. Exact issuer validation is therefore the highest-value technical control to verify once authorized access is available.

## VERDICT

**Overall verdict: MUJ has a clearly verified Microsoft 365 and Microsoft Entra identity estate, including at least two distinct MUJ Entra tenants, cloud-managed domain authentication, Exchange Online Protection, public Microsoft DKIM aliases, an official Office 365 onboarding process, mandatory MFA registration language, and a documented SSPR workflow. However, the public record does not prove that the SLCM application's primary login is federated to Entra through OIDC, SAML, or WS-Federation.**

The original proposition should therefore be rewritten as follows:

> MUJ SLCM is visibly connected to MUJ's Microsoft identity lifecycle because it recognizes MUJ Microsoft mail namespaces and links to Microsoft's password-reset service. Public Entra and DNS records independently verify Microsoft 365 tenants and managed cloud authentication. The exact SLCM sign-on protocol and token flow remain unverified.

### Confidence by finding

| Finding | Confidence | Basis |
|---|---|---|
| `jaipur.manipal.edu` tenant ID and `mujcampus` alias | **High** | Direct Microsoft OpenID metadata [5][44]. |
| `muj.manipal.edu` tenant ID and `mujmanipal` alias | **High** | Direct Microsoft OpenID metadata [7][48]. |
| `manipal.edu` root tenant and `learnermanipal` alias | **High** | Direct Microsoft metadata [45]. |
| Managed cloud authentication rather than current AD FS redirect | **High for public realm state** | Both MUJ realms say `Managed` and expose no external AuthURL. |
| Microsoft 365 mail routing and published SPF/DKIM records | **High** | Direct DNS answers. |
| Monitoring-only DMARC posture | **High** | Explicit `p=none`, NXDOMAIN at the subdomain, and RFC inheritance [15][10][11][49]. |
| MFA enrollment in MUJ Office 365 onboarding | **High as of the June 2025 SOP** | Official MUJ instructions [9]. |
| Universal MFA/Conditional Access coverage | **Low to moderate** | No public tenant policy; enforcement is private and signal-dependent [42]. |
| SSPR availability for intended Office 365 users | **Moderate to high** | MUJ documents the reset journey, but public evidence cannot verify every account's group scope [9][41]. |
| SLCM use of OIDC, SAML, or WS-Fed | **Low / unverified** | No public authorization redirect, ACS/reply URL, client/entity ID, or protocol message was found [2][3]. |

**Priority actions**: perform an authorized SLCM redirect/configuration review; enforce exact tenant, issuer, and audience validation; verify Conditional Access coverage for both MUJ tenants; test SSPR and role boundaries with synthetic accounts; review DKIM alignment from controlled mail samples; and stage DMARC enforcement after legitimate-sender remediation.

## References

1. *login.microsoftonline.com*. https://login.microsoftonline.com/getuserrealm.srf?login=probe@muj.manipal.edu&xml=1
2. *Manipal University*. https://muj.slcm.jaipur.manipal.edu/
3. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
4. *login.microsoftonline.com*. https://login.microsoftonline.com/muj.manipal.edu/federationmetadata/2007-06/federationmetadata.xml
5. *Openid Configuration*. https://login.microsoftonline.com/jaipur.manipal.edu/.well-known/openid-configuration
6. *login.microsoftonline.com*. https://login.microsoftonline.com/getuserrealm.srf?login=probe@jaipur.manipal.edu&xml=1
7. *Openid Configuration*. https://login.microsoftonline.com/muj.manipal.edu/.well-known/openid-configuration
8. *login.microsoftonline.com*. https://login.microsoftonline.com/jaipur.manipal.edu/federationmetadata/2007-06/federationmetadata.xml
9. *Help Document Sop Office 365 And Outlook Email Id*. https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf
10. *dns.google*. https://dns.google/resolve?name=_dmarc.muj.manipal.edu&type=TXT
11. *dns.google*. https://dns.google/resolve?name=_dmarc.manipal.edu&type=TXT
12. *dns.google*. https://dns.google/resolve?name=jaipur.manipal.edu&type=MX
13. *dns.google*. https://dns.google/resolve?name=selector1._domainkey.muj.manipal.edu&type=CNAME
14. *dns.google*. https://dns.google/resolve?name=muj.manipal.edu&type=MX
15. *dns.google*. https://dns.google/resolve?name=_dmarc.jaipur.manipal.edu&type=TXT
16. *dns.google*. https://dns.google/resolve?name=muj.manipal.edu&type=TXT
17. *dns.google*. https://dns.google/resolve?name=selector2._domainkey.muj.manipal.edu&type=CNAME
18. *dns.google*. https://dns.google/resolve?name=manipal.edu&type=MX
19. *dns.google*. https://dns.google/resolve?name=selector2._domainkey.jaipur.manipal.edu&type=CNAME
20. *dns.google*. https://dns.google/resolve?name=selector2._domainkey.manipal.edu&type=CNAME
21. *dns.google*. https://dns.google/resolve?name=selector1._domainkey.manipal.edu&type=CNAME
22. *dns.google*. https://dns.google/resolve?name=jaipur.manipal.edu&type=TXT
23. *dns.google*. https://dns.google/resolve?name=selector1._domainkey.jaipur.manipal.edu&type=CNAME
24. *dns.google*. https://dns.google/resolve?name=manipal.edu&type=TXT
25. *Microsoft identity platform and OAuth 2.0 authorization ... Microsoft Learn https://learn.microsoft.com › entra*. https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow
26. *Microsoft Entra authentication & authorization error codes*. https://learn.microsoft.com/en-us/entra/identity-platform/reference-error-codes
27. *Microsoft Identity Platform – Zugriffstoken Microsoft Learn https://learn.microsoft.com › de-de › entra › access-tokens*. https://learn.microsoft.com/de-de/entra/identity-platform/access-tokens
28. *Microsoft identity platform UserInfo endpoint*. https://learn.microsoft.com/en-us/entra/identity-platform/userinfo
29. *Microsoft Entra Connect - AD FS management and customization ...*. https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-fed-management
30. *Testing for User Enumeration and Guessable User Account*. https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/03-Identity_Management_Testing/04-Testing_for_Account_Enumeration_and_Guessable_User_Account
31. *OpenID Connect (OIDC) on the Microsoft identity platform*. https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols-oidc
32. *ID tokens in the Microsoft identity platform*. https://learn.microsoft.com/en-us/entra/identity-platform/id-tokens
33. *OWIN Integration with Microsoft.Identity.Web | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/msidweb/frameworks/owin
34. *Configure OpenID Connect Web (UI) authentication in ASP.NET ...*. https://learn.microsoft.com/en-us/aspnet/core/security/authentication/configure-oidc-web-authentication?view=aspnetcore-10.0
35. *Microsoft Entra ID with ASP.NET Core - learn.microsoft.com*. https://learn.microsoft.com/en-us/aspnet/core/security/authentication/azure-active-directory?view=aspnetcore-10.0
36. *ID tokens in the Microsoft identity platform*. https://learn.microsoft.com/th-th/entra/identity-platform/id-tokens
37. *Testing for Account Enumeration and Guessable User*. https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/03-Identity_Management_Testing/04-Testing_for_Account_Enumeration_and_Guessable_User_Account
38. *Microsoft Entra Connect and federation - Microsoft Entra ID*. https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-fed-whatis
39. *Authentication - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
40. *Access tokens in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens
41. *Self-service password reset deep dive - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/authentication/concept-sspr-howitworks
42. *Microsoft Entra Conditional Access: Zero Trust Policy Engine - Microsoft Entra ID | Microsoft Learn*. https://learn.microsoft.com/en-us/entra/identity/conditional-access/overview
43. *Password spray investigation | Microsoft Learn*. https://learn.microsoft.com/en-us/security/operations/incident-response-playbook-password-spray
44. *Openid Configuration*. https://login.microsoftonline.com/mujcampus.onmicrosoft.com/.well-known/openid-configuration
45. *login.microsoftonline.com*. https://login.microsoftonline.com/getuserrealm.srf?login=probe@manipal.edu&xml=1
46. *Openid Configuration*. https://login.microsoftonline.com/manipal.edu/.well-known/openid-configuration
47. *Openid Configuration*. https://login.microsoftonline.com/learnermanipal.onmicrosoft.com/.well-known/openid-configuration
48. *Openid Configuration*. https://login.microsoftonline.com/mujmanipal.onmicrosoft.com/.well-known/openid-configuration
49. *rfc-editor.org*. https://www.rfc-editor.org/rfc/rfc7489.html
50. *SAML Security - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html
