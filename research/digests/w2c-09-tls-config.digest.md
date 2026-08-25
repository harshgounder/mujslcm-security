# Digest: w2c-09-tls-config

## REPORT
Source file: w2c-09-tls-config.md (297 lines, 37383 bytes). Public TLS posture of mujslcm.jaipur.manipal.edu from SSL Labs, CT, urlscan, Akamai docs, RFCs.

## ANSWER SUMMARY
- SSL Labs public assessment 2026-08-25: grade B with warnings, endpoint 98.70.14.50, Microsoft-IIS/10.0, TLS 1.0/1.1/1.2 enabled, TLS 1.3 not listed.
- Leaf cert: RSA-2048/SHA-256, single SAN, valid 2025-12-22 to 2026-12-21, issuer Entrust DV TLS Issuing RSA CA 2, chain through Sectigo root R46; OCSP stapling on, CAA absent.
- BEAST true, HSTS absent, compression 0, secure renegotiation on; multiple integer oracle fields (value 1) mean not vulnerable, only BEAST is a positive boolean.
- HTTP/2 via ALPN h2 http/1.1 works, but legacy TLS branches stay; 3DES and static RSA suites offered under TLS 1.0/1.1/1.2.
- Akamai attribution not corroborated: 2026 urlscan records and the SSL Labs test converge on Microsoft AS8075 at 98.70.14.50.
- Modern client simulations pick TLS 1.2 AES-GCM; older profiles pick TLS 1.0 CBC; posture defined by weakest negotiable path.
- Remediation priority: High for protocol hardening, Medium for HSTS/governance, Investigative for architecture attribution.

## KEY FACTS
- https://api.ssllabs.com/api/v3/analyze?host=mujslcm.jaipur.manipal.edu&fromCache=on&maxAge=1000000&all=done&startNew=off : primary machine evidence, grade B, protocol/suite arrays, cert fields.
- https://urlscan.io/api/v1/search/?q=domain:mujslcm.jaipur.manipal.edu : IP/ASN/server history; 2024 record on port 122 with D-Vois, 2026 records on Microsoft AS8075.
- https://api.certspotter.com/v1/issuances?domain=mujslcm.jaipur.manipal.edu&include_subdomains=false&expand=dns_names&expand=issuer&expand=cert : CT record matching SAN, validity start, fingerprints.
- https://mujslcm.jaipur.manipal.edu/Home/Index : landing page with login choices; does not name M365, MVC, or .NET versions.
- https://techdocs.akamai.com/cps/docs/cipher-profiles : Akamai profile scopes; ak-akamai-2020q1 is TLS 1.2/1.3 only, conditional target if property confirmed.
- https://www.rfc-editor.org/rfc/rfc8996.html : TLS 1.0 and 1.1 MUST NOT be negotiated.
- https://datatracker.ietf.org/doc/rfc9113 : h2 requires TLS 1.2+, required GCM suite is present at MUJ.
- https://csrc.nist.gov/pubs/sp/800/52/r2/final : NIST TLS 1.2/1.3 baseline used as modern comparison.
- https://github.com/ssllabs/research/wiki/SSL-Server-Rating-Guide : B cap for TLS 1.0/1.1 and BEAST; guide 2009r dated 2025-05-16.
- https://github.com/ssllabs/ssllabs-scan/blob/master/ssllabs-api-docs-v4.md : field enumeration semantics, vulnBeast definition, 0-RTT value -1 means not performed.
- https://www.sectigo.com/resource-library/sectigo-acquires-entrust-public-certificate-business : explains Entrust issuer naming under Sectigo ownership.
- https://certificate.transparency.dev/ : CT limits; logging is not proof of correct issuance or safety.
- https://urlscan.io/domain/mujslcm.jaipur.manipal.edu : domain-level urlscan listing used for attribution checks.
- https://cabforum.org/working-groups/server/baseline-requirements/requirements : CA/Browser Forum baseline requirements reference.
- https://www.ssllabs.com/projects/ssllabs-apis/index.html : SSL Labs API documentation for method notes.

## ACTIONABLE LEADS
- Owner-authorized retest gate: only TLS 1.2/1.3 listed, no 3DES or TLS_RSA_* suites, vulnBeast false, HSTS valid, CAA present.
- Reconcile DNS, load balancer, Azure/IIS, and any Akamai property before changing policy; attribution precedes remediation.
- If Akamai property confirmed, migrate profile to ak-akamai-2020q1; otherwise harden the Microsoft/IIS termination point.
- Verify M365 and MVC/.NET claims separately via configuration records; do not infer from the TLS dataset.
- Keep automated renewal and CT monitoring; add CAA plus CT alerting.

## FLAGS
- Akamai premise unverified; current public records point to Microsoft, not Akamai.
- Microsoft 365 identity, ASP.NET MVC 5.3, .NET 4.x not established by TLS or landing-page evidence.
- Criteria version mismatch (result 2009q vs guide 2009r) may explain the 3DES/B-grade tension.
- 2024 urlscan used nonstandard port 122 and another provider; not a like-for-like predecessor.
- "Issued 2025-12-22" is notBefore; exact CA transaction time not exposed.
- All findings point-in-time for one resolved endpoint; split-horizon DNS could yield other paths.

## COVERAGE
Chars read: 37383 (full file to EOF, truncated false).