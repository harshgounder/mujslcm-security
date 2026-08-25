## REPORT (w2b-10-sis-manipal.md)
MAHE SIS/SLCM WebForms architecture and defensive OSINT. Public observation only. Verdict: SIS login surface confirmed, WebForms-era hypothesis medium confidence, shared-code and vulnerability claims unproven. 260 lines, 39488 chars, read to EOF, truncated: false.

## ANSWER SUMMARY
- MAHE's official Student Portal page links to https://sis.manipal.edu/index.aspx; the login route studloginSLCM.aspx shows Login, a (dd/mm/yyyy) hint, Captcha, and an MAHE Information Systems Department footer.
- .aspx is consistent with ASP.NET Web Forms but does not prove runtime, version, IIS config, auth protocol, or topology. ViewState, request validation, and CAPTCHA are review questions, not findings.
- Portal family: MAHE SLCM (MU SLcM), MUJ (WELCOME TO MUJ PORTAL), and Manipal Dubai (slcm.manipaldubai.com) share SLCM vocabulary; shared code, database, or identity is unproven. Label it "shared SLCM product-family hypothesis".
- A public Salesforce sandbox login (maheslcmtech--sit.sandbox.my.site.com) plus a Salesforce announcement about SLCM modernization support a hybrid legacy-plus-modern scenario, not complete migration.
- Supplied claims of MVC 5.3, .NET 4.x, IIS 10, Akamai, and Microsoft 365 identity remain unverified for SIS; Microsoft and Akamai documentation cited is generic.
- One Reddit SLCM password complaint is a symptom for service-desk correlation, not evidence of a security defect.

## KEY FACTS
- https://sis.manipal.edu/studloginSLCM.aspx - the analyzed login surface: Login, date hint, Captcha label, MAHE Information Systems footer.
- https://www.manipal.edu/mu/academics/student-portal.html - official MAHE page linking to sis.manipal.edu/index.aspx.
- https://sis.manipal.edu/ - SIS Portal root, sparse visible text.
- https://slcm.manipal.edu/ - MU SLcM portal, MAHE identity, 2017 copyright in search result.
- http://slcm.manipal.edu/StudentChangePassword.aspx - public password-change route under the same host.
- https://slcm.manipaldubai.com/ - Manipal Dubai SLCM sign-in page.
- http://manipaldubai.com/about-us - official Dubai page linking the campus Student Portal.
- http://maheslcmtech--sit.sandbox.my.site.com/login?locale=us - public Salesforce sandbox login named "Login | SLCM".
- https://mujslcm.jaipur.manipal.edu/ - MUJ portal welcome and sign-in surface.
- https://muj.slcm.jaipur.manipal.edu/ - secondary MUJ student-login result with Forgot Password wording.
- https://learn.microsoft.com/en-us/previous-versions/aspnet/ms178472%28v%3Dvs.100%29 - WebForms page lifecycle: initialization, control instantiation, state restoration.
- https://owasp.org/www-community/ASP-NET_Request_Validation - request validation scoped as defense in depth, not a substitute for output encoding and authorization.
- https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-framework - .NET Framework 4.8 listed as active; generic support status only.
- http://reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue - user-reported SLCM password rejection.
- https://techdocs.akamai.com/cloudlets/docs/proxy - Akamai proxy concept doc; does not prove any Manipal hostname uses Akamai.

## ACTIONABLE LEADS
- Build a public-OSINT evidence register: URL, collection date, title, wording, fact or inference or unknown class.
- Ask the owner: SIS and SLCM team ownership, production versus test domains, retirement or modernization plans, authoritative identity systems, supported runtime baseline, login-fault reporting path.
- Deliver a control map over the login boundary: identity, session, state, bot mitigation, logging, monitoring, recovery.
- For authorized technical work: written scope naming domains, dates, source IPs, test accounts, allowed methods, stop conditions; use a non-production replica with synthetic identities.
- Do not test password-reset flows, craft ViewState, or measure rate limits against production.

## FLAGS
- The report's reference citations degrade into opaque bracket tokens inside tables (for example [114.0; 35.0]); verify each cited URL directly before reuse.
- Salesforce sandbox login is public but does not prove production use or API-led integration status.
- Shared product family is an inference; shared code, shared databases, and shared identity are "Very low" or "Low" confidence in the report's own table.
- CAPTCHA presence says nothing about server-side enforcement or monitoring.
- The Reddit password complaint has multiple benign explanations; do not treat it as a compromise signal.
- .NET 4.8 active status is product policy, not evidence of the deployed runtime.

## COVERAGE
- File read to EOF: 260 lines, 39488 chars (file_size 39488), truncated: false. Confirmed EOF at line 260, final reference.