# Digest: w2c-10-email-spoofing

## REPORT
Source file: w2c-10-email-spoofing.md (297 lines, 41616 bytes). Point-in-time 2026-08-25 passive DNS review of SPF, DKIM, DMARC for jaipur.manipal.edu, manipal.edu, and SLCM.

## ANSWER SUMMARY
- Both domains publish DMARC p=none, so neither requests quarantine or rejection; RFC 9989 tree walk applies Jaipur p=none to mail visible From mujslcm.jaipur.manipal.edu.
- SPF hard fail (-all) on both domains; Jaipur authorizes Outlook plus Brightspace (3 lookup terms), parent adds SendGrid, Salesforce, fixed IPv4 (7 terms).
- Jaipur TXT carries non-versioned SPF-like fragments (ip4:103.139.159.150/32, SendGrid, Outlook, Brightspace text); SPF evaluators discard them, leaving administrative ambiguity.
- MX for both domains points to Microsoft protection hosts; Jaipur selector1 and selector2 return nonempty RSA DKIM keys; manipal.edu selector2 returns a key, selector1 has CNAME but no target TXT key at collection.
- SLCM host: A 98.70.14.50, no TXT answer, no direct _dmarc record; parent DMARC also lacks rua, and RFC 9989 suppresses aggregate reports when rua is absent.
- Lookalikes: manipal-edu.com resolves with p=quarantine and no SPF; manipaledu.com resolves with v=spf1 -all and parked CNAME; .in/.org/.net variants NXDOMAIN.
- Recommended path: measured none to quarantine to reject after reporting and sender inventory, per Microsoft staged guidance.

## KEY FACTS
- https://dns.google/resolve?name=jaipur.manipal.edu&type=TXT : hard-fail SPF plus confusing non-versioned fragments.
- https://dns.google/resolve?name=_dmarc.jaipur.manipal.edu&type=TXT : p=none with rua mailbox, monitoring only.
- https://dns.google/resolve?name=manipal.edu&type=TXT : parent SPF with four third-party includes.
- https://dns.google/resolve?name=_dmarc.manipal.edu&type=TXT : p=none, no rua destination.
- https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=A : SLCM resolves to 98.70.14.50.
- https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=TXT : NOERROR with no answers, no direct policy.
- https://dns.google/resolve?name=_dmarc.mujslcm.jaipur.manipal.edu&type=TXT : NXDOMAIN, no direct DMARC owner name.
- https://dns.google/resolve?name=jaipur.manipal.edu&type=MX : jaipur-manipal-edu.mail.protection.outlook.com.
- https://dns.google/resolve?name=selector1._domainkey.jaipur.manipal.edu&type=TXT : nonempty RSA DKIM key returned.
- https://dns.google/resolve?name=selector2._domainkey.manipal.edu&type=TXT : parent selector2 key returned.
- https://dns.google/resolve?name=selector1._domainkey.manipal.edu&type=TXT : CNAME present, no key returned; rotation review item.
- https://dns.google/resolve?name=manipal-edu.com&type=A : lookalike resolves to two addresses.
- https://dns.google/resolve?name=_dmarc.manipal-edu.com&type=TXT : lookalike publishes p=quarantine with onsecureserver.net reporting.
- https://www.rfc-editor.org/rfc/rfc9989.html : parent policy discovery and rua suppression rules.
- https://learn.microsoft.com/en-us/defender-office-365/email-authentication-dmarc-configure : staged none to quarantine to reject migration framework.

## ACTIONABLE LEADS
- Add an authorized rua destination to _dmarc.manipal.edu before any enforcement step.
- Inventory every legitimate sender under the parent SPF; validate SPF result, DKIM d=, and DMARC alignment on real outbound headers.
- Resolve intent of Jaipur TXT fragments with mail-flow owners, then remove or consolidate.
- For confirmed non-sending hosts such as SLCM, publish explicit v=spf1 -all and a direct enforcing DMARC record after dependency checks.
- Stage Jaipur to quarantine then reject using existing rua telemetry; revisit parent later due to broader scope.
- Bounded lookalike monitoring plus FIDO/WebAuthn for high-risk identities per CISA.

## FLAGS
- Parent selector1 missing TXT key may be a normal inactive/rotation state; DNS alone cannot decide.
- SPF lookup-term counts are point-in-time; provider policy changes shift them.
- Lookalike ownership and intent unknown; NXDOMAIN results are volatile.
- No claim of observed abuse; this is posture analysis only.
- DNS is volatile; records should be re-queried before remediation or publication.

## COVERAGE
Chars read: 41616 (full file to EOF, truncated false).