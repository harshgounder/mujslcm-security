# EXEC-SUMMARY: MUJ SLCM security research (club deliverable)

Date: 2026-09-13 (campaign 2026-08-25, layer pass and gap register 2026-09-13).
Repo: github.com/harshgounder/mujslcm-security (private).
Scope: one target, https://mujslcm.jaipur.manipal.edu. Recon-grade throughout, no destructive testing,
no authentication attempts, no sibling host touched.

## What this package produced

- 135 research launches in this repo: 10 + 84 + 15 + 1 in the campaign, 25 in wave 5
- 140 report and synthesis files, 5,585,870 chars, every one read to EOF
- 109 per-run digests plus 3 domain syntheses plus a deterministic wave-5 digest
- 10 verified hands-on findings, 1 documented error caught by a reaudit, and 4 corrections logged
  in the layer pass
- the full layer stack of the portal, L0 to L13, each row with its raw capture
- a graded gap register against the WSTG spine: 25 gaps, 450 attached tool rows, 84 no-tool gaps,
  47 build candidates
- a target test plan, an aggressive-phase playbook, a gated auth-phase suite, and a disclosure letter
  template

## The picture of the target

IIS 10 with ASP.NET MVC 5.3 and .NET Framework 4.7.4136.0, served from a single Azure address
(98.70.14.50, AS8075) with only port 443 reachable, no reverse proxy in front, no attributable WAF, TLS
1.0 through 1.3 all accepted with 3DES and CBC suites, no HSTS, no downgrade protection, and a
two-generation jQuery load (1.10.2 with 3.4.1 inside a 4.2 MB bundle). Identity is Microsoft 365: the
portal password is the campus M365 password and usernames follow a public format. The estate around it
spans Azure, AWS ap-south-1 and on-prem Jaipur ranges, with two live test instances and an identity
provider host.

## Verified findings

F1. Verbose .NET error pages, four reproducible triggers, customErrors off, exact runtime leaked.
F2. trace.axd returns 403, so ASP.NET tracing is enabled and restricted; ELMAH is absent.
F3. Version banners: IIS 10, ASP.NET 4.0.30319, MVC 5.3, x-powered-by ASP.NET.
F4. Legacy client stack: jQuery 1.10.2 (2013), confirmed live alongside a bundled 3.4.1.
F5. Credential design: M365 password, public username format, reset delegated to Entra SSPR.
F6. Password echo on failed login with a response-size oracle.
F7. Request validation rejects hostile input by producing a YSOD, which is also what a WAF
    fingerprinter mistakes for an edge control.
F8. The `enc` parameter is a machineKey-protected blob. Live work refined this into a three-stage
    oracle: not base64 gives FormatException at 4,942 bytes, valid base64 that fails decryption gives
    CryptographicException at 5,084 bytes, and an empty value gives a third family.
F9. The antiforgery cookie is HttpOnly without Secure, and no SameSite attribute is observed.
F10. Edge posture at campaign time. Amended: WAF status is UNKNOWN from outside, not absent.
E1. A route-oracle error the reaudit caught and corrected.

## What the layer pass added (2026-09-13)

- DNS: two SPF records on the parent domain (an SPF permerror), DMARC split across the family
  (none, not published, reject), three DKIM tenants, senders that include SendGrid and Amazon SES
- TLS measured properly: 1.3 offered (a common scanner misses this), 1.0 and 1.1 also accepted
- the estate: 30 certificate names, 18 resolving, across Azure, AWS and on-prem, with `idp`, `pms`,
  `testerp` and `testmycampus` newly identified
- clean results, now closed rather than assumed: host-header injection, X-Forwarded-Host,
  absolute-URI targets, trust-based error-detail bypass, verb tampering, server-side validation
- two error-page families, MVC and IIS, which tells you which stack answers an unmapped path

## What is NOT covered, in one line

Post-auth is unwritten, and the campaign holds no brief for XSS, SQLi, CORS, XXE, SSTI, smuggling,
cache poisoning, race conditions, the Azure or Entra control planes, detection engineering, DPDP
obligations, supply chain, mobile static analysis, social engineering, or the retest loop. Wave 5 exists
to answer each of those, one report per gap.

## Honest limits

- Nothing here is an exploit. Every finding is information disclosure, transport hardening or design
  observation, verified with single requests and raw captures.
- No scanner, fuzzer or authentication attempt has run against the target or any sibling host.
- The authorized phase needs a signed registrar letter plus two test accounts.
- Every claim is re-probed before it is restated; corrections are logged, not quietly edited.

## Assets

| asset | where |
|---|---|
| layer map | `findings/LAYER-MAP.md` |
| findings and playbooks | `findings/` |
| raw hand evidence | `recon/`, `recon/layers-2026-09-13/` |
| reports, syntheses, digests | `research/` |
| briefs and run ledgers | `briefs/`, `ledger/`, `wave*-runs.json` |
| pipeline | `scripts/` |
| disclosure template | `disclosures/DISCLOSURE-LETTER.md` |
