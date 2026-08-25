# Digest: w2c-16-ssrf-mvc.md

## REPORT
Source: /home/liebert511/mujslcm-recon/research/w2c-16-ssrf-mvc.md

## ANSWER SUMMARY
- No public evidence that MUJ SLCM offers image-by-URL import, webhooks, URL-to-PDF, or XML processing. SSRF not established.
- Four candidate sink classes: image URL import, webhook/callback, URL-to-PDF renderer, XML external resource. Each has a different failure mode.
- .NET Framework 4.x details decide risk: AllowAutoRedirect defaults true, XmlResolver null default since 4.5.2, XmlTextReader 4.0-4.5.2 defaults DtdProcessing.Parse.
- IIS ARR and Akamai are ingress controls; neither constrains application-originated egress. Deny-by-default routing required.
- Redirect validation gap: first-URL-only checks fail when HttpWebRequest follows redirects by default.
- Test policy is authorization-first: written scope, passive inventory, static review, isolated unit tests, one owner-controlled staging callback per sink.
- Hard-deny destination classes: loopback, RFC 1918, link-local, IPv6 ULA/link-local, cloud metadata, third-party hosts.
- Verdict: SSRF review justified as defensive design exercise; no vulnerability claim against MUJ.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/Home/Index : only target-specific evidence, portal with institutional and parent sign-in.
- https://mujslcm.jaipur.manipal.edu/ : root page, same evidence boundary.
- https://owasp.org/Top10/2021/A10_2021-Server-Side_Request_Forgery_%28SSRF%29 : SSRF definition, positive allowlist and deny-by-default guidance.
- https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html : image and webhook sink patterns, IPAddress.TryParse and DNS rebinding caveats.
- https://learn.microsoft.com/en-us/dotnet/api/system.net.httpwebrequest.allowautoredirect?view=netframework-4.8.1 : redirects on by default, MaximumAutomaticRedirections.
- https://learn.microsoft.com/en-us/dotnet/api/system.net.httpwebrequest.proxy?view=netframework-4.8.1 : proxy inheritance, local bypass, direct connection paths.
- https://learn.microsoft.com/en-us/dotnet/api/system.xml.xmlreadersettings.xmlresolver?view=netframework-4.8.1 : null resolver default since 4.5.2.
- https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html : XXE prevention, parser defaults by framework version.
- https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#security : renderer retrieves HTTPS and file:// resources, custom fetcher advice.
- https://www.iana.org/assignments/iana-ipv4-special-registry/iana-ipv4-special-registry.xhtml : IPv4 loopback, private, link-local classification for deny policy.
- https://www.iana.org/assignments/iana-ipv6-special-registry/iana-ipv6-special-registry.xhtml : IPv6 loopback, ULA, link-local classification.
- https://learn.microsoft.com/en-us/iis/extensions/url-rewrite-module/reverse-proxy-with-url-rewrite-v2-and-application-request-routing : IIS ARR is inbound reverse proxying only.
- https://www.akamai.com/glossary/what-is-server-side-request-forgery : Akamai describes SSRF as server-side pivot.
- https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf : NIST SP 800-115 plan requirements.
- https://csrc.nist.gov/pubs/sp/800/115/final : assessment plan, scope, prohibited activities, incident handling.

## ACTIONABLE LEADS
- Under authorization only: trace MVC action params, model-bound fields, webhook settings, queue messages into outbound request and XML APIs.
- Source review for WebRequest.Create, HttpWebRequest, WebClient, HttpClient, renderer and XML resolver sinks.
- Staging policy tests with mocks: redirects, schemes, IPv4/IPv6 answers, DNS changes.
- Owner-run benign callback once per sink with ROE limits: image, webhook, PDF render, XML mock.
- Inspect proxy and egress config; verify AllowAutoRedirect and XmlResolver settings in deployed config.
- Akamai/WAF rules for detection only; never the sole SSRF control.

## FLAGS
- All four sink features unverified at target; report says no public evidence any exists.
- Stack labels (MVC 5.3, .NET 4.x, IIS 10, Akamai, M365) requester-supplied, not independently verified.
- WeasyPrint and wkhtmltopdf cited as generic renderer examples; no evidence MUJ uses either.
- Report explicitly rejects converting technology fingerprint into vulnerability claim; treat all target conclusions Low confidence.
- Reference [18] wkhtmltopdf URL present but not used in body claims.

## COVERAGE
- Chars read: 37745. EOF confirmed via read_file truncated:false.