# Digest: w2c-19-machinekey-viewstate.md

## REPORT
Source: /home/liebert511/mujslcm-recon/research/w2c-19-machinekey-viewstate.md

## ANSWER SUMMARY
- No public proof of MUJ key exposure. Both mujslcm.jaipur.manipal.edu and muj.slcm.jaipur.manipal.edu show branded login pages only.
- ASP.NET default key mode is AutoGenerate,IsolateApps with random material; a public AutoGenerate literal is not a leaked secret.
- Web farms need consistent manual keys; independent auto keys cause ViewState MAC failures across nodes.
- MVC 4.5+ anti-forgery tokens use MachineKey.Protect; Katana SystemWeb data protection delegates too. Key risk is not ViewState-only.
- Microsoft Dec 2024 incident: one public static key used for code injection; 3000+ disclosed keys flagged. Hash list comparison is the safe defensive method.
- Key equality between the two MUJ hostnames is Unknown; DNS names do not prove IIS topology or AppDomain sharing.
- Framework45 crypto behavior is opt-in via targetFramework; installing 4.5 does not change legacy apps automatically.
- Verdict: unverified deployment risk, moderate overall confidence; P0 owner-authorized key fingerprint review.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/ : portal A-side, branded login only.
- https://muj.slcm.jaipur.manipal.edu/ : second portal hostname, topology unknown.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.configuration.machinekeysection.validationkey?view=netframework-4.8.1 : validationKey default AutoGenerate,IsolateApps.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.configuration.machinekeysection.decryptionkey?view=netframework-4.8.1 : decryptionKey default and role.
- https://support.microsoft.com/en-US/servicing/DotNetFramework/troubleshooting/resolving-view-state-message-authentication-code-mac-errors : ViewState MAC, farm key coordination.
- https://www.microsoft.com/en-us/security/blog/2025/02/06/code-injection-attacks-using-publicly-disclosed-asp-net-machine-keys : incident, 3000+ disclosed keys, hash comparison script, rotation advice.
- https://github.com/Microsoft/referencesource/blob/master/System.Web/Configuration/MachineKeySection.cs : IsolateApps path hash, IsolateByAppId behavior.
- https://learn.microsoft.com/en-us/aspnet/mvc/overview/security/xsrfcsrf-prevention-in-aspnet-mvc-and-web-pages : MVC anti-forgery uses MachineKey.Protect.
- https://github.com/aspnet/AspNetKatana/blob/main/src/Microsoft.Owin.Host.SystemWeb/DataProtection/MachineKeyDataProtector.cs : Katana SystemWeb delegates to MachineKey APIs.
- https://devblogs.microsoft.com/dotnet/cryptographic-improvements-in-asp-net-4-5-pt-2/ : Framework45 opt-in mode, KDF, purpose separation.
- https://github.com/Tejas-Narula/SlcmPlus/tree/main : third-party Chrome extension, not authoritative config.
- https://github.com/Anushkakumar10/muj_slcm : third-party Python project, not authoritative config.
- https://github.com/blacklanternsecurity/badsecrets : known-secrets detection library for defensive matching.
- https://docs.github.com/en/enterprise-cloud%40latest/code-security/how-tos/secure-your-secrets/customize-leak-detection/define-custom-patterns : GitHub secret scanning custom patterns for machineKey search.
- https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html : secret rotation and revocation guidance.

## ACTIONABLE LEADS
- Map both hostnames to IIS site IDs, app IDs, physical paths, pools, origins before drawing key conclusions.
- Fingerprint fixed keys and compare with Microsoft disclosed-key hash list; never publish raw values.
- Repository history scan for machineKey, validationKey, decryptionKey, compatibilityMode with non-capturing patterns.
- Inventory all MachineKey.Protect consumers: ViewState, MVC anti-forgery, forms auth tickets, OWIN/Katana, custom blobs.
- Coordinated farm-wide rotation with logout planning and incident response if a public match appears.
- Check ViewStateUserKey assignment at Page_Init during WebForms code review.

## FLAGS
- Reference [15] in the report is a 404 page (viewstate-mac-enforced link); not usable as a source.
- Third-party repos are client-side material; no authoritative server config found. Absence of finding is not proof of safety.
- Similar branding on the two hostnames is E0-class evidence only; one-app conclusion is inference.
- Report reproduces no raw candidate keys; hash-list method is the stated safe path.
- AutoGenerate,IsolateApps literals are posture, not secrets; report warns against mislabeling them.

## COVERAGE
- Chars read: 40518. EOF confirmed via read_file truncated:false.