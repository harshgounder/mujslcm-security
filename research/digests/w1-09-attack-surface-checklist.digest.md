## REPORT (w1-09-attack-surface-checklist.md)
## ANSWER SUMMARY
- Verdict: GO only with signed university authorization and synthetic test identities; otherwise NO-GO. Sections 43 and 66 of India's IT Act make permission the controlling gate.
- Priority order: horizontal/vertical authorization and IDOR first, payment and record business logic second, session/CSRF and identity controls third, diagnostics and config review fourth, headers/TLS baseline last.
- IDOR method: two accounts, two owned objects, one changed variable, one request, stop on first proof; never guess production IDs.
- Session: ASP.NET_SessionId must renew after login and role change; __RequestVerificationToken variants (missing, mutated, cross-session, expired) go only against a no-op action.
- Legacy ASP.NET review over exploitation: customErrors, compilation debug=false, elmah.axd, trace.axd, WebDAV, 8.3 short names, .aspx/.asmx/.svc inventory, machineKey provenance, ViewState MAC; never forge cookies or deserialization payloads.
- Role confusion: EmailFor/LoginFor are attacker-controlled hints; the server must re-derive role from the identity store.
- Disclosure: registrar@jaipur.manipal.edu (Dr Amit Soni) first, CERT-In RVDCP for coordination, 90-day window as practice only. No dedicated MUJ PSIRT found (confidence 0.74 on that route).
- jQuery 1.10.2 falls in CVE-2015-9251 and CVE-2019-11358 ranges; range membership is a finding, reachability must be proven separately.

## KEY FACTS
- https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References | IDOR definition and two-user method basis.
- https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/03-Identity_Management_Testing/04-Testing_for_Account_Enumeration_and_Guessable_User_Account | enumeration needs material response difference, not client markup.
- https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html | session renewal after privilege change; cookie flag requirements.
- https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html | header removal and hardening baselines.
- https://www.indiacode.nic.in/bitstream/123456789/13116/1/it_act_2000_updated.pdf | IT Act sections 43, 66, 66C, 66D quoted for the authorization gate.
- https://www.jaipur.manipal.edu/administration-registrar.php | Dr Amit Soni, Registrar; registrar@jaipur.manipal.edu; +91 141-3999100 ext 102; disclosure first contact.
- https://www.cert-in.org.in/RVDCP.jsp | CERT-In responsible vulnerability disclosure and coordination policy.
- https://projectzero.google/vulnerability-disclosure-policy.html | Project Zero 90-day policy cited; see FLAGS, URL looks malformed.
- https://nvd.nist.gov/vuln/detail/CVE-2015-9251 | jQuery XSS before 3.0.0, cross-domain Ajax condition.
- https://nvd.nist.gov/vuln/detail/CVE-2019-11358 | jQuery deep-extension XSS before 3.4.0.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.configuration.customerrorsmode?view=netframework-4.8.1 | Off/On/RemoteOnly error mode semantics.
- https://elmah.github.io/a/securing-error-log-pages/ | ELMAH remote access default-disabled; secure via authorization when enabled.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.security.machinekey?view=netframework-4.8.1 | machineKey algorithms shared with Forms Auth and ViewState.
- https://www.microsoft.com/en-us/security/blog/2025/02/06/code-injection-attacks-using-publicly-disclosed-asp-net-machine-keys | real-world leaked machineKey code injection campaign.
- https://owasp.org/www-project-top-10-for-business-logic-abuse | business logic abuse framing for fee and record tests.

## ACTIONABLE LEADS
- Route matrix on approved assets: /Home/Index, /Student/*, /Staff/*, /Account/*; one GET each as logged out, Student A, Student B, Staff A; record status, size, protected-data presence.
- IDOR replay on document paths with synthetic canaries (TA-001 / TB-001 pattern); HEAD first, small Range GET if needed; stop on first cross-user hit.
- Hidden field test: same credentials with LoginFor=Student vs Staff; check navigation and API authorization results, not just login success.
- Fee flow: capture pre-redirect request, change one field (amount, order id, student id), send only to the pre-authorization step; never complete 3DS or replay callbacks.
- Reset flow: verify target host, tenant branding, generic responses, token lifetime and single-use, rate controls; one test account only.
- Diagnostic probes: one GET each to /elmah.axd and /trace.axd; one malformed param on an approved field; one OPTIONS for WebDAV; config review for customErrors, debug, machineKey provenance.
- Lockout: sacrificial account only, at exercise end, known threshold, stop at first throttle; never spread attempts across usernames.
- Disclosure sequence: encrypted report to registrar@jaipur.manipal.edu with engagement ID; CERT-In RVDCP only for coordination or a real incident; 90-day timeline with day-2 ack target; joint publication timing.

## FLAGS
- Ref 7 URL https://projectzero.google/vulnerability-disclosure-policy.html uses a domain that likely does not exist; the real Project Zero policy is hosted elsewhere. Treat as unverified, possibly fabricated link.
- The report states no live requests were made; route names, hidden fields, jQuery version, reset destination, and stack are hypotheses from the brief, not verified observations.
- Ref 6 uses http://cert-in.org.in/SecurityIncident.jsp while the body cites https://www.cert-in.org.in/; two different CERT-In URLs, content unverified.
- Refs 29 and 31 both point at NIST SP 800-115 via different URLs; duplicate oddity, content unverified.
- IT Act quotes are a research summary, not legal advice; verify language against the PDF before relying on it.
- "5 to 10 attempts typical lockout threshold" is a generic OWASP note, not a portal measurement.
- Confidence splits (0.89 methodology, 0.74 route) are model outputs.
- The report leans on the brief's claim that the portal is ASP.NET MVC 5.3 / .NET 4.x / IIS 10; w1-02 headers corroborate that stack.

## COVERAGE
- 46547 chars read; verified to EOF (295/295 lines, read_file truncated: false).