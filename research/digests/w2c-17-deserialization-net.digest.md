# Digest: w2c-17-deserialization-net.md

## REPORT
Source: /home/liebert511/mujslcm-recon/research/w2c-17-deserialization-net.md

## ANSWER SUMMARY
- No confirmed MUJ deserialization vulnerability. Public evidence is a portal landing page with sign-in and parent login.
- BinaryFormatter is unsafe by design per Microsoft, cannot be made secure, causes DoS, disclosure, or RCE in process context.
- MVC 5.3 does not prove BinaryFormatter or ViewState use; package existence verified, deployment not.
- ViewState is a WebForms .aspx mechanism; relevant only if .aspx remnants exist or share machineKey config.
- ViewState MAC enforcement is non-disableable since advisory 2905247; machineKey integrity is the gate.
- Microsoft Dec 2024 incident: one public static key used for code injection in IIS worker process; 3000+ disclosed keys flagged.
- Observed value 4.7.4136.0 is not a patch inventory; registry Release DWORD is the supported method.
- ysoserial.net formatter support is capability evidence, not target evidence.
- Verdict: plausible conditional risk, no confirmed MUJ deserialization vulnerability.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/ : only target-specific evidence.
- https://learn.microsoft.com/en-us/dotnet/standard/serialization/binaryformatter-security-guide : BinaryFormatter danger, removal guidance.
- https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca2300 : CA2300 insecure deserializer rule.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.ui.losformatter?view=netframework-4.8.1 : LosFormatter serializes WebForms ViewState, insecure.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.ui.objectstateformatter?view=netframework-4.8.1 : can fall back to BinaryFormatter for ISerializable types.
- https://github.com/pwntester/ysoserial.net : formatter and gadget capability evidence only.
- https://support.microsoft.com/en-US/servicing/DotNetFramework/troubleshooting/resolving-view-state-message-authentication-code-mac-errors : ViewState MAC behavior, farm key consistency.
- https://www.microsoft.com/en-us/security/blog/2025/02/06/code-injection-attacks-using-publicly-disclosed-asp-net-machine-keys : Dec 2024 incident, 3000+ disclosed keys, rotation advice.
- https://learn.microsoft.com/en-us/security-updates/securityadvisories/2013/2905247 : MAC validation made non-disableable.
- https://learn.microsoft.com/en-us/dotnet/framework/install/how-to-determine-which-versions-are-installed : registry Release method, Environment.Version warning.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.ui.page.viewstateuserkey?view=netframework-4.8.1 : ViewStateUserKey binding, Page_Init requirement.
- https://www.nuget.org/packages/Microsoft.AspNet.Mvc : MVC 5.3.0 package exists, targets .NET 4.5+.
- https://learn.microsoft.com/en-us/dotnet/standard/serialization/binaryformatter-migration-guide : migration to System.Text.Json, DataContractSerializer, MessagePack, protobuf-net.
- https://learn.microsoft.com/en-us/iis/configuration/system.applicationhost/sites/site/tracefailedrequestslogging : failed request tracing requires role service and enablement.
- https://www.akamai.com/products/app-and-api-protector : WAF is compensating control, not a serializer fix.

## ACTIONABLE LEADS
- Owner-authorized SAST inventory for BinaryFormatter, IFormatter, Deserialize, ISerializable, SerializationBinder, SoapFormatter, NetDataContractSerializer, LosFormatter, ObjectStateFormatter.
- Data-flow trace from HTTP, cookies, files, queues, caches, databases into each sink.
- WebForms remnant inventory: .aspx list, master pages, PageStatePersister subclasses, effective ViewState config.
- machineKey provenance review: repository history, secret scans, compare fingerprints with Microsoft hash list, rotate exposed keys.
- Verify framework via registry Release, OS build, cumulative updates; banner is correlation only.
- IIS failed-request tracing as detection with privacy and retention policy.

## FLAGS
- 4.7.4136.0 is a supplied observation with no authoritative mapping; report refuses CVE or patch verdicts from it.
- MVC 5.3 verified only as NuGet package existence; IIS 10, Akamai, M365 requester-supplied.
- No public WebForms remnant identified; all ViewState claims conditional.
- Reference [15] NuGet link has malformed markdown (line break in label) but URL itself valid.
- Report states no exploit attempt was made and no payload details were included.

## COVERAGE
- Chars read: 40390. EOF confirmed via read_file truncated:false.