# Digest: w3-13-lms-brightspace-muj.md

## REPORT
Source file: w3-13-lms-brightspace-muj.md (MUJ SLCM and Brightspace public-exposure assessment)

## ANSWER SUMMARY
- MUJ learning login is a D2L Brightspace tenant. learning.onlinemanipal.com CNAMEs to muj.brightspace.com; learner-mahe.onlinemanipal.com CNAMEs to manipalonline.brightspace.com; both A responses share IPs 13.55.178.159 and 15.134.178.12.
- The login page shows "Powered by D2L Brightspace" for Manipal University Jaipur Centre for Distance and Online Education.
- Microsoft metadata for muj.manipal.edu is public: tenant 27282fdd-4c0b-4dfb-ba91-228cd83fdf71 with WS-Fed and OIDC endpoints. No proof Brightspace uses that tenant as relying party.
- The App Store callback-failure claim is unverified. Play store search returned only Manipal Hospitals apps, no Online Manipal education app.
- The MUJ iLearn page shows an OTP flow; it names no Microsoft, Entra ID, Brightspace, SAML, or OIDC.
- The supplied SLCM stack fingerprint (ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai) is not confirmed by Wappalyzer, urlscan, or raw markup checks.
- Only one Brightspace CVE found: CVE-2021-43129, quiz right-click control bypass, CVSS 6.5, medium. MUJ exposure unknown.
- D2L documents a broad permissioned API surface (users, grades, content, org units, courses, calendar) with OAuth scopes.

## KEY FACTS
- https://learning.onlinemanipal.com/d2l/home/14042 - public login page, "Powered by D2L Brightspace" label.
- https://dns.google/resolve?name=learning.onlinemanipal.com&type=CNAME - CNAME to muj.brightspace.com, TTL 3600.
- https://dns.google/resolve?name=learner-mahe.onlinemanipal.com&type=CNAME - CNAME to manipalonline.brightspace.com, TTL 600.
- https://dns.google/resolve?name=muj.brightspace.com&type=A - A records 13.55.178.159 and 15.134.178.12.
- http://login.microsoftonline.com/muj.manipal.edu/.well-known/openid-configuration - public tenant metadata and OIDC endpoints.
- http://login.microsoftonline.com/muj.manipal.edu/federationmetadata/2007-06/federationmetadata.xml - public WS-Federation metadata for the namespace.
- https://muj.onlinemanipal.com/ilearn-login - lead-capture and OTP flow page; no SSO vendor named.
- https://muj.onlinemanipal.com/privacy-policy - MUJ policy: AWS hosting in India and Singapore; SPDI categories; sharing with vendors.
- https://nvd.nist.gov/vuln/detail/CVE-2021-43129 - the relevant Brightspace CVE, CVSS 6.5.
- https://app.opencve.io/cve/?product=brightspace&vendor=d2l - OpenCVE shows one matching CVE, updated 2024-11-21.
- https://docs.valence.desire2learn.com/basic/oauth2.html - OAuth 2.0 authorization-code flow and scope model.
- https://community.d2l.com/brightspace/kb/articles/23533-d2l-vulnerability-disclosure-policy - customer-instance testing needs customer authorization.
- https://community.d2l.com/brightspace/kb/articles/4537-sessions-and-system-access-data-sets - Session History and System Access data set definitions.
- https://www.d2l.com/cloud - D2L says AWS is primary cloud provider and D2L handles LMS updates.
- https://play.google.com/store/search?q=Online%20Manipal&c=apps&hl=en_IN - store search found no Online Manipal education app.

## ACTIONABLE LEADS
- Ask the service owner for the sanctioned Brightspace relying-party configuration, redirect URI inventory, claims mapping, MFA policy, deprovisioning process.
- Ask whether the quiz "Disable Right Click" setting is used so CVE-2021-43129 remediation can be confirmed through the managed service.
- Run a club exercise on a local mock Brightspace integration; no token requests against the MUJ tenant.
- Re-capture DNS snapshots for both aliases over time; do not infer tenant identity from shared IPs.
- Keep the App Store callback allegation labeled unverified until a real listing or review is found.

## FLAGS
- Supplied Akamai/IIS/.NET fingerprint is unverified; collected Wappalyzer and markup evidence showed none of it.
- /d2l/home/14042 and /d2l/home/14201 paths are not proof those numbers are course or tenant IDs.
- Reference 42 is a Manipal Hospitals YouTube video mislabeled as a passive raw-markup check; discard as evidence.
- References 43 and 44 (Supabase callback docs) are unrelated to MUJ; ignore.
- Shared Brightspace IPs and public tenant metadata support inference only, not confirmed SSO or shared tenancy.
- Report is AI deep-research output; all claims need independent verification.

## COVERAGE
Read 30,487 chars (226 lines), single pagination pass, EOF confirmed (truncated false).