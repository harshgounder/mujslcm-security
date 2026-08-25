# Digest: w2f-12-waf-fingerprint.md

## REPORT
Source file: w2f-12-waf-fingerprint.md (Distinguishing Akamai WAF From MUJ Application Responses)

## ANSWER SUMMARY
- A 403 status or Access Denied body is not attribution. Akamai can deny, craft custom error pages, and rewrite status and headers at the edge. Response appearance alone cannot name the deciding layer.
- Three decision planes exist on the MUJ path: Akamai edge, IIS/application origin, Microsoft 365 identity. A user-visible denial can come from any of them; one screenshot cannot identify the plane.
- Strongest Akamai fingerprint is a correlation handle, not a logo: the error reference string (Translate Error String tool can return WAF, origin, client, edge details), X-Akamai-Request-ID, and SIEM events with policyId, rule IDs, actions.
- OWASP CRS on MUJ is unproven. CRS uses anomaly scoring (default inbound 5, outbound 4), but Akamai's own vocabulary is Kona Rule Set and Adaptive Security Engine; no source equates them.
- IP allowlist is unproven. Akamai Client IP criteria exist (address, range, CIDR, connecting IP or X-Forwarded-For), but only config or matched-event evidence establishes MUJ policy. Campus-vs-residential difference has many explanations.
- Microsoft identity is verified context: realm check labels muj.manipal.edu a managed MUJ realm, MX routes to Microsoft, and MUJ's published Office 365 SOP uses login.microsoftonline.com.
- Recommended path is passive capture plus log correlation, budget of one ordinary baseline navigation per approved context, stop on challenge or 429.
- Verdict: Medium confidence in architecture assessment, very high confidence in attribution methodology.

## KEY FACTS
- http://mujslcm.jaipur.manipal.edu/ - Public portal surface, WELCOME TO MUJ PORTAL, parent/student/forgot-password routes.
- http://login.microsoftonline.com/getuserrealm.srf?login=probe@muj.manipal.edu&xml=1 - Realm probe evidence that muj.manipal.edu is a managed MUJ realm.
- http://dns.google/resolve?name=muj.manipal.edu&type=MX - MX to muj-manipal-edu.mail.protection.outlook.com, Microsoft 365 mail routing.
- http://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf - MUJ Office 365 SOP, documents Microsoft login flow and account security steps.
- https://techdocs.akamai.com/edge-diagnostics/docs/translate-error-string - Official translator for Akamai error reference codes, returns WAF and origin details.
- https://techdocs.akamai.com/edge-diagnostics/docs/pragma-headers - X-Cache, X-Cache-Remote, X-Check-Cacheable, X-Akamai-Request-ID diagnostic headers.
- https://techdocs.akamai.com/cloud-security/docs/app-api-protector - Akamai WAF can alert or deny based on configured actions.
- https://techdocs.akamai.com/terraform/docs/as-rc-custom-deny - Custom deny pages and redirects, why bodies are not invariant fingerprints.
- https://techdocs.akamai.com/edgeworkers/docs/response-object - EdgeWorkers can set status codes and modify headers, edge-transformed responses.
- https://techdocs.akamai.com/property-mgr/docs/client-ip - Client IP criterion, 300 addresses/ranges/CIDRs, connecting IP or X-Forwarded-For option.
- https://techdocs.akamai.com/terraform/docs/as-rc-rate-policy - Rate policies with average, burst, penalty-box parameters.
- https://coreruleset.org/docs/2-how-crs-works/2-1-anomaly_scoring/ - CRS cumulative anomaly scoring with documented thresholds.
- https://coreruleset.org/docs/2-how-crs-works/2-2-paranoia_levels/ - CRS paranoia levels, PL1 low false alarms.
- https://techdocs.akamai.com/terraform/docs/as-rc-rule-upgrade - KRS and ASE modes, automatic vs manual rule upgrades.
- https://www.akamai.com/resources/solution-brief/adaptive-security-engine - ASE combines threat scoring, behavior, anomaly detection.
- http://akamai.com/products/bot-manager - Bot Manager scores 0 to 100, tuned responses, intentionally opaque.
- https://techdocs.akamai.com/powershell/docs/siem - SIEM events carry configId, policyId, rule IDs, actions, requestId, status.
- https://www.rfc-editor.org/rfc/rfc9110.html - HTTP semantics reference for status code attribution limits.
- https://learn.microsoft.com/en-us/iis/configuration/system.webserver/httperrors/ - IIS httpErrors, origin-side custom error possibility.

## ACTIONABLE LEADS
- Preserve full incident bundles from any reported denial: complete reference string, headers, body hash, screenshot, redirect chain, UTC time, URL, public client IP, browser version, auth state.
- Have an authorized Akamai operator translate error reference strings and search SIEM by requestId or narrow UTC/client/host/path tuple.
- Ask the Akamai admin for security mode, custom-deny definitions, Bot Manager status, rate policies, Client IP criteria, evaluation-mode availability.
- Correlate three ways before classifying: client artifact, Akamai event, IIS/application log. Classify outcomes as edge security, origin response, edge-transformed, identity-provider, or indeterminate.
- One baseline navigation per approved context maximum; stop on challenge, 429, latency rise, or operator request.
- Confirm the Microsoft identity plane via realm check and MX before blaming WAF.
- Refer any positive-control rule testing to evaluation mode or staging under owner control.

## FLAGS
- Contradiction: Akamai presence is a club-supplied premise, while the report itself says no collected first-party source confirms it; all Akamai statements are conditional.
- Suspicious claim: intensity of "Akamai-style reference string" as strong evidence assumes the translator is real and accessible; verify before treating it as a finding.
- Unverified URLs: realm probe uses a probe@muj.manipal.edu address; the report claims it labels the domain as managed, but the raw XML output is not reproduced.
- Hallucination risk: Bot Manager, allowlist, and rate policy statements are product capability citations, not MUJ observations; do not convert them into MUJ findings.
- The exact MUJ deny page template, ruleset, thresholds, and allowlist are unknown; any concrete claim about them would be fabricated.
- Two competing explanations for every observed pattern (WAF, bot score, rate policy, app logic) are retained deliberately; readers must not pick one without telemetry.
- The report contains no actual MUJ 403 capture; every 403 claim in it is hypothetical scenario language.

## COVERAGE
- Chars read: 41800
- EOF confirmed: true (read_file truncated=false, 290 lines)