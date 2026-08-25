# Digest: w2f-06-akamai-edge.md

## REPORT
Source file: w2f-06-akamai-edge.md (41,547 bytes, 315 lines, read to EOF)

## ANSWER SUMMARY
- `mujslcm.jaipur.manipal.edu` resolves directly to 98.70.14.50; RIPE maps covering prefix 98.70.0.0/15 to Microsoft AS8075. No CNAME to an Akamai edge hostname is returned.
- The supplied "IIS 10 behind Akamai" premise is unsupported: Akamai onboarding docs describe CNAME mapping to edgesuite.net, edgekey.net, or akamaized.net; none observed.
- Headers expose Server Microsoft-IIS/10.0, X-AspNetMvc-Version 5.3, X-AspNet-Version 4.0.30319, and X-Powered-By ASP.NET. These favor a Microsoft stack, not an Akamai edge.
- WAF status is not publicly verifiable. Akamai attack groups are collections of Kona Rule Set rules with configurable actions: alert, deny, custom deny, or none.
- If 98.70.14.50 is the backend, the origin is plainly disclosed; if it is an Azure front end, the backend is unknown. No separate hidden origin was verified.
- Sibling addresses are leads, not origins: muj.slcm.jaipur.manipal.edu at 20.244.94.89, dms.jaipur.manipal.edu at 1.186.160.28, slcm.manipal.edu at 104.211.226.160.
- Browser hardening is incomplete: SecurityHeaders grade D; HSTS, CSP, X-Content-Type-Options, Referrer-Policy, and Permissions-Policy missing; X-Frame-Options SAMEORIGIN present; request-verification cookie HttpOnly without Secure or SameSite.
- Portal links to Microsoft password reset; full Microsoft 365 federation is not proven.

## KEY FACTS
1. https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=A - A record 98.70.14.50 with TTL 3600; the current public service endpoint.
2. http://stat.ripe.net/data/prefix-overview/data.json?resource=98.70.14.50 - 98.70.0.0/15 aligns to AS8075 Microsoft Corporation; the address is Microsoft evidence, not Akamai evidence.
3. https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=CNAME - no CNAME answer, only zone authority; no Akamai edge mapping visible.
4. http://api.hackertarget.com/httpheaders?q=https://mujslcm.jaipur.manipal.edu/ - observed IIS 10, ASP.NET MVC and runtime banners, X-Powered-By, XFO SAMEORIGIN, HttpOnly cookie without Secure or SameSite.
5. http://securityheaders.com/?followRedirects=on&q=https://mujslcm.jaipur.manipal.edu/ - grade D; missing HSTS, CSP, nosniff, referrer, and permissions headers.
6. http://crt.sh/?output=json&q=mujslcm.jaipur.manipal.edu - CT shows the MUJ hostname, a www variant, and a historical dms.jaipur.manipal.edu certificate relationship.
7. https://dns.google/resolve?name=muj.slcm.jaipur.manipal.edu&type=A - 20.244.94.89; sibling address with unproven backend linkage.
8. https://dns.google/resolve?name=dms.jaipur.manipal.edu&type=A - 1.186.160.28; sibling address with unproven backend linkage.
9. https://dns.google/resolve?name=slcm.manipal.edu&type=A - 104.211.226.160; central SLCM address that also exposes an IIS/ASP.NET response.
10. https://passwordreset.microsoftonline.com/ - Microsoft recovery touchpoint linked from the portal; not proof of full federation.
11. http://techdocs.akamai.com/ion/docs/define-property-hostnames - documented Akamai onboarding model: customer DNS CNAME to an Akamai edge hostname.
12. http://techdocs.akamai.com/terraform/docs/pm-rc-edge-hostname - edge hostname classes at edgesuite.net, edgekey.net, and akamaized.net; none match the MUJ DNS.
13. https://techdocs.akamai.com/edge-diagnostics/docs/pragma-headers - X-Cache, X-Cache-Remote, and X-Akamai-Request-ID are context-dependent diagnostics absent from the ordinary MUJ response.
14. https://techdocs.akamai.com/terraform/docs/as-ds-attack-groups - KRS attack-group actions are customer-configurable; a policy does not imply blocking.
15. https://techdocs.akamai.com/site-shield/docs/welcome-site-shield - Site Shield CIDR allowlisting is explicitly not a substitute for authentication.

## ACTIONABLE LEADS
- Re-run the DNS A, CNAME, and AAAA queries and the RIPE prefix call to confirm the 2026-08-25 snapshot still holds.
- Fetch crt.sh JSON for the current certificate list and owner names.
- Compare sibling posture: http headers and securityheaders checks for slcm.manipal.edu.
- Owner-side asks: Azure resource mapping for 98.70.14.50, Akamai property and edge hostname if any, Site Shield or Origin IP ACL map, KRS/ASE mode, and attack-group actions.
- Hardening steps: strip version banners, add HSTS, CSP, nosniff, referrer, and permissions headers, and review cookie attributes.
- Do not probe candidate IPs or run Host-header bypass tests without written authorization.

## FLAGS
- The supplied Akamai premise is contradicted by current DNS and BGP evidence; treat it as an unverified design claim.
- The role of 98.70.14.50 is unresolved: origin, Azure load balancer, application gateway, or other service; public data cannot decide.
- Absence of an Akamai CNAME does not rule out an Azure-layer proxy or WAF at the same address.
- Missing Akamai diagnostic headers in an ordinary request prove nothing by themselves.
- CT records reveal names, not backend IPs; sibling addresses are entity-conflation risks.
- All DNS, RIPE, header, and CT observations are time-bound and unverified by this digest.

## COVERAGE
Chars read: 41,547 (full file, 315 lines). EOF confirmed: truncated false on the complete read.

DONE w2f-06-akamai-edge.md.digest.md