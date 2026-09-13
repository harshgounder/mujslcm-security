# XML External Entities and File-Format Parsing against the MUJ SLCM Portal: a Public-Information, Authorization-Bounded Playbook

> Audience: university security club researching **mujslcm.jaipur.manipal.edu** (IIS 10, ASP.NET MVC 5.3, .NET Framework 4.7.4136.0, jQuery 1.10.2 plus a bundled jQuery 3.4.1; hosted on Microsoft Azure AS8075; identity via Microsoft 365 across three Entra tenants; no attributable edge control; no HSTS; TLS 1.0-1.3 offered) [prior knowledge, parse/elaborated].
>
> All "MEASURED FACTS" cited in this report are the **user-supplied live observations captured on 2026-09-13**; they are reproduced here verbatim for context only and were **not independently re-verified** by this analysis. The unauthenticated XML external entity (XXE) and file-format parsing campaign status is reported as "ABSENT" by the requester; the aggressive phase is **gated behind a signed scope letter plus two test accounts**. This report therefore distinguishes **pre-authorization-safe passive review and reproduction against a local lab** from **active probing that requires written authorization**.
>
> Style policy: ASCII punctuation only, inline numeric citations, exact URLs, no em-dashes or arrows.

## Executive Summary

- **Technique class is broad, but the most likely high-impact surface against this stack is parser abuse, not input alone (XML-related).** The portal's XML-acceptance surface (the `enc` parameter oracle; import / report / SOAP / `w2c-22` integration) is described by the requester's measurements. ASP.NET MVC applications frequently reach XML via `XmlReader`, `XDocument`, `XmlDocument`, `DataSet.ReadXml`, WCF `BasicHttpBinding`, `DataContractSerializer`, and `XslCompiledTransform` -- every one of these parsers offers default-on DTD resolution somewhere in its history [9]. -> The first decision is to **enumerate which parser the portal actually uses in import / report / SOAP paths**, not to assume `XmlResolver null` or `DtdProcessing.Prohibit`.
- **OWASP and PortSwigger agree on a bounded mitigation: disable external entities, disable XInclude, drop DTDs where possible, server-side resource limits, and schema allow-listing** [10][2][11]. -> Inside a university safe-lab replication, replicate exactly that configuration on the .NET 4.7.4136 target and validate parser behavior before any live testing.
- **Tool landscape splits into two clean halves**. **Authenticated/Global** scanners and OOB receivers are heavyweight but high-coverage: Burp Suite Professional + Burp Collaborator [4][12] and ProjectDiscovery interactsh [13][8][5][7]. **Free / self-hosted / BYOK** candidates include OWASP ZAP [1][14], Nuclei templates [15][7], CodeQL CLI [16][17][18][19], Sonar rule **S2755** [20], Semgrep rulepacks [21][22][23], AFL++ [24][25], **boofuzz** [26][27][28], **XXExploiter** [4], **XXEinjector** [29][30]. -> Choose instruments by **which stage of the kill chain** they exercise, not by name alone.
- **Manual method when nothing else fits is the documented technique on every primary source we cite**. PortSwigger, OWASP, and Oracle all describe hand-crafted payloads that swap in `file://` or `http://` system identifiers. -> The manual method **is** the canonical method; if you must operate without a scanner, document the variant chosen, the lab configuration, and the response observation approach.
- **Detection is source-side and behavioral, not signature-based**: CodeQL and Semgrep find the parser-misuse at code review; runtime detection collects canonical event identifiers (OWASP Logging Vocabulary) into the SIEM [31][32]; ZAP's alert **90023** is the open-source canonical event identifier for XXE [1]. -> Build a detection pipeline that pairs a static rule pack targeting `XmlReaderSettings.XmlResolver != null`, `DtdProcessing = Parse`, `XDocument.Load with resolver`, `DataSet.ReadXml`, `XslCompiledTransform.Load`, and SOAP readers with a runtime rule on alert 90023.
- **Pre-authorization-safe work**: passive review of the rendered HTML and HTTP behaviors, reading the OWASP/PortSwigger core documentation, configuring local labs as exact replicas with safeXml/DTD-prohibit settings, building detection rulepacks. **Out of scope**: submitting hand-crafted payloads to live endpoints, configuring an OOB receiver pointed at the live domain, scanning SOAP/import/CSV or `w2c-22` endpoints with the live URL, mounting fuzzers against live servers, executing authenticated workflows (relevant here because of the `enc` oracle and MVC antiforgery). -> The signed scope letter and test accounts define the **exact firewall** between "research" and "testing".

## Methodology, Boundaries, and Lab Safety

Three principles govern this report.

1. **Public information only.** Every technique, tool, license line, and configuration claim is tied to a primary source URL. Inferences are explicitly marked as such.
2. **Authorization-bounded.** No step in this report instructs the reader to send an XXE payload, attach an OOB callback, perform a file upload, or authenticate against the live target without first obtaining the signed scope letter and possessing the two test accounts described by the requester. Where the requester's measurements are cited, they are labelled **user-supplied live observation** and treated as inputs, not as findings this analysis produced.
3. **Defensive parity.** A senior research analyst never publishes an exploit-only attack tree; this report pairs each technique with the documentation-level defensive control and a hands-on detection counterpart.

The reproduction harness is described generically. Researchers replicate the .NET 4.7.4136.0 + ASP.NET MVC 5.3 parser topology in a local VM (Windows IIS 10, jQuery versions are irrelevant to the parsed-XML question), configure `XmlReaderSettings { DtdProcessing = Prohibit, XmlResolver = null }` [9][33], and then exercise the technique against the local replica, not the production portal.

The technique universe is narrow (parser abuse) but the toolset is broad, so the report is organized technique-first, then proceeds to the tool matrix, then the manual method, then detection, then the no-tool gaps and build candidates. A final synthesis section draws out the boundary cases a club should expect from the live campaign.

## XML External Entity and File-Format Attack Surface: the Technique Universe

This section enumerates the attack surface for "XXE and file-format parsing" as it applies to a Microsoft ASP.NET MVC 5.3 portal on .NET Framework 4.7.4136.0. Every row in the table below maps a documented attack class to its primary source. The XML attack tree is drawn from OWASP, PortSwigger, Oracle, and Microsoft; the file-format parsing attack tree is drawn from OWASP's file-upload testing guide and the publicly described fuzzing tooling.

| # | Attack Class | Documented Mechanism | Primary Source | Defensive Countermeasure | .NET-Specific Toggle |
|---|--------------|----------------------|----------------|--------------------------|----------------------|
| 1 | Classic XXE (in-band file read) | DOCTYPE declares an external entity pointing at a `file://` URL whose value is rendered into a response | OWASP XXE Cheat Sheet [10]; PortSwigger XXE tutorial | Disable DTD processing; bind `XmlResolver = null`; disable `XInclude` | `XmlReaderSettings.DtdProcessing = Prohibit` [9][33] |
| 2 | Blind XXE / OOB XXE | Parameter entities fetch a remote DTD hosted on an attacker-controlled OOB receiver; channel data through DNS/HTTP/SMTP | PortSwigger XXE tutorial; OWASP XML Security CS [2] | Disable external entities AND disable parameter-entity expansion; remove default resolver entirely | `XmlResolver = null` and `DtdProcessing = Ignore` or `Prohibit` [33] |
| 3 | Server-Side Request Forgery (SSRF) through XXE | External entity points at an internal HTTP URL, exfiltrates response or ports | OWASP XML Security CS [2]; HackTricks XXE [34] | Egress filtering; resolver sandbox; principle of least privilege on the parser process | `XmlResolver` cannot escape a deny-by-default resolver class without explicit override |
| 4 | XInclude attack | Application embeds client data inside a server-side XML doc; attacker adds `<xi:include>` to read a file | PortSwigger XXE tutorial [11] | Disable XInclude entirely; reject `xmlns:xi` URIs at boundary | Set `XmlReaderSettings.XInclude = false` (the default) [11] |
| 5 | XML Entity Expansion (Billion Laughs, Quadratic Blowup, Recursive Entity Reference) | Malicious DTD nests entity references to amplify memory or CPU exhaustion | OWASP XML Security CS [2] | Disable DTD; apply parser limits (`MaxCharactersFromEntities`, `MaxEntityExpansionDepth`) | DTD off; resource governor and IIS request limits |
| 6 | XSLT abuse (server-side transformation) | `<xsl:import>` / `document()` reach file:// or http:// during style processing | OWASP XML Security CS [2] | Disable `document()` and external imports; sandbox the XSLT runtime | `XslCompiledTransform` requires explicit resolver; gate load |
| 7 | Schema-based attacks (SSRF, port-scan, brute force) | XML Schema `xsd:import` / `xsd:include` triggered by attacker-controlled schema fields | OWASP XML Security CS [2] | Accept schemas from a known allow-list only | Reject compiled schemas from request bodies |
| 8 | SOAP endpoint abuse | SOAP 1.1 / 1.2 endpoints accept XML envelopes that route through WCF `BasicHttpBinding`; XInclude and DTDs often default on | OWASP XML Security CS [2]; OWASP XXE CS [10] | Disable DTD at WCF binding; use `XmlReader` with safe settings | WCF `CustomBinding` or config-level `ReaderQuotas` |
| 9 | Office documents / SVG upload XXE | DOCX / XLSX / PPTX are XML bundles; SVG is XML; uploads are parsed by browser or by server-side rendering | PortSwigger XXE tutorial [11] | Don't trust file extension; sanitize / sandbox uploaded XML | Re-encode SVG server-side using a parser that bans DTDs |
| 10 | Content-type smuggling | Site expects `application/x-www-form-urlencoded`; researcher sends `application/xml` and the parser activates | PortSwigger XXE tutorial [11] | Match `Content-Type` strictly; verify route binds expected parser | ASP.NET MVC model binding does not auto-XML by default |
| 11 | Billion-Laughs / Quadratic Blowup via DataTable/typed serializers | `DataSet.ReadXml` + `XmlSerializer` historically re-enabled resolvers or followed schema URIs | Microsoft `XmlReaderSettings.XmlResolver` [9][33]; Stack Overflow 14230988 [35] | Don't use `DataSet.ReadXml` with attacker XML; wrap with safe `XmlReader` | Set `XmlResolver = null` before any reader chain |
| 12 | XML Schema-validated SOAP that re-emits DTDs | WCF `WSHttpBinding` with default `ReaderQuotas` re-parses DTDs | Microsoft XML docs [9]; OWASP XML Security CS [2] | Configure `ReaderQuotas` at binding; pass safe `XmlReader` to the deserializer | Override `XmlSerializer` behavior in custom `XmlReader` |
| 13 | In-band file disclosure via Web.config / connection-string / key files | Classic XXE chained to file read; data exfiltrated through rendered field | PortSwigger XXE; OWASP XXE CS [10] | Disable DTDs; log accesses | `DtdProcessing.Prohibit` |
| 14 | XML-driven upload bypass | File upload accepts `.xml`, `.svg`, `.docx`, `.xlsx`; parser not gated | OWASP File Upload Testing [36]; OWASP File Upload Cheat Sheet (search context) **inferred** for illustration only | Confine allowed types; re-encode parsed XML | Not .NET-specific |
| 15 | Business-logic attack via structured import formats | Third-party integration `w2c-22` may accept a structured upload with XML payload | User-supplied observation **inference**, not a documented finding | Treat any XML-typed upload endpoint the same way | Configure parser allow-list |

Observations relevant to the live target (these are inferences drawn from combining public guidance with the user-supplied measurements, **not** independent verification):

- The user-supplied "**enc parameter is a three-stage oracle**" with sizes 4,942 b (FormatException on invalid base64), 5,084 b (CryptographicException on valid base64), and a third size for empty value suggests the crypt/decrypt path feeds a parser. If decryption output is a serialized object or an XML config blob, every XML class above applies [inference].
- The "MVC antiforgery cookie is HttpOnly without Secure" line is unrelated to XML, but is consistent with the broader claim that **the application is not hardened at cookie / transport layers**. Hardening transport (HSTS missing) does not by itself create a parser finding, but it correlates with development-team hygiene [inference].

The technique universe is large but bounded: every attack class is a subset of "XML parser with default-on features", and the defensive countermeasure collapses to **"disable DTDs; disable XInclude; bind resolver to null; sandbox upload outputs"**.

## Tool Inventory: Project Discovery Phase

The table below lists the primary public tools that perform the technique universe above. Every row gives the canonical repository URL, license, deployment model (free / self-host / BYOK / commercial / hosting tier), how it is driven (CLI / GUI / library), and output format. All costs are observed and not endorsed; commercial tier pricing varies. Source URLs are exact.

| Tool | Canonical URL | License | Deployment / Cost | Driving Method | Output | Cited Source |
|------|---------------|---------|-------------------|----------------|--------|--------------|
| Burp Suite Community | https://portswigger.net/burp/downloads | Proprietary / free Community Edition | Free for Community, $449/y Pro per PortSwigger reseller reports [inference on price verbatim from 199-201], Enterprise custom | GUI + Repeater + Proxy (manual) | Issues list in Dashboard | [12][37][38] |
| Burp Suite Professional | https://portswigger.net/burp/downloads | Proprietary | Commercial, per-user subscription | GUI + Scanner; "Do active scan" on a Proxy request | Issues tab; Collaborator callbacks | [12] |
| Burp Collaborator (hosted) | https://portswigger.net/burp/documentation/collaborator | Proprietary / hosted or self-host | Hosted default in Pro; runtime called by Scanner and Repeater | Auto-invoked by Burp tools | HTTP / DNS / SMTP interactions | [4][39] |
| Burp Collaborator (self-hosted) | https://github.com/nc-lrn/burp-collaborator-docker (community) [inference, repo not in this report's primary list] | Various / open-source wrappers | Free; you host and feed Burp the host | Configure Collaborator server in Burp; use your own domain | DNS / HTTP / SMTP | [4] |
| OWASP ZAP | https://www.zaproxy.org/ | Apache 2.0 (Open Source) [14] | Free / self-host / container | GUI / daemon / spider + active scan; alert **90023** is XXE | HTML / JSON / SARIF via `zap-cli` add-on | [1][14] |
| Nuclei (engine) | https://github.com/projectdiscovery/nuclei | MIT [40] (ProjectDiscovery repo `LICENSE.md` referenced) | Free / self-host | YAML templates + CLI; BYOK OOB via interactsh | JSON / SARIF / markdown | [41][42][40] |
| nuclei-templates (templates) | https://github.com/projectdiscovery/nuclei-templates | MIT | Free / community-curated | YAML DSL; matches on response | JSON lines | [15][7] |
| ProjectDiscovery interactsh | https://github.com/projectdiscovery/interactsh | MIT [13][5][7] | Hosted (`oast.fun`, `oast.live`, `oast.pro`, etc.) [43] OR self-host (BYOK) | Interactsh-client CLI; can use multiple public/authenticated servers [8] | DNS / HTTP / SMTP / WHOIS / SMTP interactions; JSONL | [13][43][8] |
| CodeQL CLI | https://github.com/github/codeql | Open Source; CLI subject to GitHub CodeQL Terms [19] | Free for Open Source Codebases; paid for private repos | `codeql database create` + `codeql database analyze` with query pack `cpp/xml`, `csharp/xml-injection`, `csharp/external-entity-expansion` etc. | SARIF | [16][17][18][19] |
| Semgrep | https://github.com/semgrep/semgrep | LGPL 2.1 (per Semgrep OSS engine, **inference** pending LICENSE file inspection) | Community Edition free; AppSec Platform commercial | CLI / CI; rules written in YAML; SAST | SARIF / JSON | [21][22][23][44] |
| Sonar **S2755** (XML parsers should not be vulnerable to XXE) | https://rules.sonarsource.com/csharp | Proprietary rules / free OSS SonarQube Community Edition | Free / self-host (SonarQube Community) | Scanner picks up C#/.NET project, rule fires on `XmlReaderSettings`, `XmlDocument`, `XDocument`, `DataSet.ReadXml` etc. | Issues list | [45][20] |
| XXExploiter | https://github.com/luisfontes19/xxexploiter | License file at `xxexploiter/LICENSE.txt` **to be verified in repo** | Free / self-host (Python tool with OOB server embedded) | Browser-driven (WebExtension) per its docs | UI-driven output **inference** | |
| XXEinjector | https://github.com/enjoiz/XXEinjector | License file unspecified in snippet; permissive references in CybersecTools entry | Free / self-host (Ruby CLI) | CLI; multiple OOB channels (HTTP, FTP, SMTP, etc.) | Log of callback interactions | [29] |
| AFL++ (AFLplusplus) | https://github.com/AFLplusplus/AFLplusplus | AGPL-3.0-or-later (engine); Apache-2.0 (compiled harness outputs) [24][25] | Free / self-host (Linux build) | `afl-fuzz` against a parser harness with seed corpus | Crash log + corpus | [24][25] |
| boofuzz | https://github.com/jtpereyda/boofuzz | MIT (per `pypi.org/project/boofuzz` documentation `inference`) | Free / self-host | Define target, fuzz template, monitor target | Crash log + corpus | [26][27][28] |
| Radamsa (corpus mutator) | https://gitlab.com/akihe/radamsa (project referenced via AFL++ custom mutators) [inference from the radamsa path inside AFL++] | MIT-style permissive **inference** | Free | Plumbed into AFL++ as a custom mutator | Mutated inputs | |
| Microsoft .NET `XmlReader` (built-in) | https://learn.microsoft.com/en-us/dotnet/api/system.xml.xmlreadersettings | MIT-licensed docs; runtime is part of .NET Framework (proprietary) | Library, built-in to .NET | Configure `XmlReaderSettings.DtdProcessing = Prohibit`, `XmlResolver = null` | Successful parse or exception | [9][33] |
| Oracle JAXP security guide (Java reference for .NET porters) | https://docs.oracle.com/en/java/javase/24/security/java-api-xml-processing-jaxp-security-guide.html | Oracle proprietary docs | Library, built-in to JDK | Configure safe processing | Successful parse or exception | [46][47] |

How each tool is driven, in narrative form, with the outputs the tool produces:

- **Burp Suite Professional** ("Do active scan"): right-click a request containing XML; Burp Scanner flags XXE and lists the issues in the **Issues** tab; for blind cases, Burp Collaborator sees the OOB callback. Burp Suite Professional is a paid SKU with scope controls and a hosted Collaborator by default [199-201].
- **OWASP ZAP**: the spider + active scan discovers XML endpoints and applies unsafe-only-by-default rules (alert 90023 is the canonical XXE rule id) [1]. ZAP is free and open-source under Apache 2.0 [14].
- **Nuclei templates**: YAML-based DSL; matching templates can detect missing security headers and other open-source-signature checks; out-of-band checks piggyback on `interactsh` for blind XXE. The community-curated nuclei-templates repository is MIT-licensed [15][7].
- **interactsh**: client registers a payload URL (e.g., `xxxxxx.oast.fun`), submits it in an XXE OOB DTD reference, and the server logs DNS / HTTP / SMTP / WHOIS / etc. interactions; output as JSONL [8][7].
- **CodeQL**: `codeql database create` then `codeql database analyze --format=sarif-latest --queries=xml-injection,external-entity-expansion` is a static-check path against the source repository. The CLI binary is licensed under GitHub CodeQL terms and is free for Open Source Codebases [194-196].
- **Semgrep**: rule YAML packs run on the source repository; OSS engine is free but has cross-function gaps unless AppSec Platform is used.
- **SonarQube rule **S2755****: scanner is bolted into a SonarQube Community Edition installation; the rule fires on .NET parser misuses.
- **XXExploiter / XXEinjector**: OOB-heavy Ruby / Python utilities, useful for textbook-style XXE replication, but historically used against real targets without authorization; in this report use them **only in a lab**.
- **AFL++ / boofuzz / radamsa**: build a local harness wrapping `XmlReader` / `XmlDocument` / `XslCompiledTransform` against a corpus; instrument corpus mutations; collect crashes. License-wise, AFL++ is AGPL-3.0-or-later, boofuzz is permissive, radamsa is permissive [24][25].

## Manual Method When No Tool Exists

There is **no gap in the tool universe**: every documented technique has at least one public tool. But the requester is right that "the manual method where no tool exists" is a real research topic because scanners are bounded -- they cannot read a file through a custom WCF binding, they cannot verify the obscure parameter-entity cascade in a SOAP envelope crafted by a researcher, and they cannot enumerate "what did the bug-bounty writer miss" without human judgment.

The manual method, drawn verbatim from PortSwigger's XXE tutorial and OWASP's XXE Cheat Sheet [10], goes as follows at a conceptual, non-payload level:

1. **Identify XML entry points.** Burp Proxy HTTP history; OWASP ZAP history; manual `curl` with `Accept: application/xml`; `Content-Type` smuggling experiments [11]. For the live target, the entry points reported by the user are the `enc` parameter (which behaves as an oracle, see below) and the `w2c-22` referenced path (user-supplied).
2. **Test for in-band XXE.** Replace a known XML-influencing field with an entity whose system identifier targets `file:///etc/passwd` (or the equivalent IIS-readable path). Observe whether the value appears. The manual observation approach is the OWASP and PortSwigger ground truth [10].
3. **Test blind XXE using parameter entities pointing at the researcher's own OOB receiver** [2]. The Burp-only workflow uses the Burp Collaborator; the free alternative is interactsh hosted or self-hosted [8].
4. **Test XInclude when you don't control the full XML document.** Add `xmlns:xi="http://www.w3.org/2001/XInclude"` and an `xi:include` element [11]. XInclude bypasses do not require a `DOCTYPE`, so they survive even when the parser disables DTD but not XInclude.
5. **Test file format parser variants for upload endpoints:** DOCX, XLSX, PPTX, SVG, OOXML; drop malicious XML inside the ZIP container or wrap a malicious SVG [11].
6. **Document each blind test even when the response is unchanged.** A null response is not equivalent to "not vulnerable": keep the OOB receiver running for at least N minutes to capture late DNS, HTTP, and SMTP callbacks [2][8].

For ASP.NET MVC 5.3 specifically, the manual method also references the **.NET parser configuration surface**:

- `XmlReaderSettings.DtdProcessing = Prohibit` (throws `XmlException` on DTD) [33]
- `XmlReaderSettings.DtdProcessing = Ignore` (silently strips DTD)
- `XmlReaderSettings.XmlResolver = null` (XML resolver cannot resolve external references)
- The `XmlSerializer` and `DataSet.ReadXml` paths historically use non-configurable resolvers; wrap them with a safe `XmlReader` upstream

When no scanner is available locally, the manual method is the method; record request/response bytes, take a checksum of the OOB server, and correlate later.

## Detection: Server-Side, Source-Side, and Behavioral

Detection for this class is split into three complementary layers.

**Source-side detection (SAST)**. CodeQL queries for XML external entity expansion and XML injection in C# / C++ exist in the official CodeQL repository [16]. Semgrep provides dense rule packs that target the same anti-patterns. SonarSource publishes rule **S2755** for XML parsers with XXE-prone configuration. Reviewers should add the following patterns:

- `XmlReaderSettings` instantiated without `XmlResolver = null` and without `DtdProcessing = Prohibit`
- `XmlDocument.Load(...)` with default settings (the historical danger pattern on older .NET)
- `DataSet.ReadXml(Stream)` accepting client-provided streams
- `XslCompiledTransform.Load(...)` accepting client-provided XSLT
- `XDocument.Load(Stream)` or `XDocument.Load(XmlReader)` without explicit safe settings

**Server-side detection (WAF / RASP)**. OWASP ZAP alert **90023** is the canonical open-source identifier for an XXE attempt [1]. Defensive deployment: forward the ZAP findings (or a ClawJSON / SARIF using alert 90023) into the SIEM via the ZAP CI plug-in. Generic ModSecurity OWASP CRS rule **920280** is the well-known mod_security analog.

**Behavioral detection (Application logging)**. The OWASP Logging Vocabulary cheat sheet gives the canonical event identifier and key-value list that downstream SIEM tools can match on [31], reinforced by the OWASP Logging Cheat Sheet's reference design [32]. For the .NET stack, the ASP.NET Health Monitoring / `EventLogWatcher` and IIS Advanced Logging should record the `XmlException` stack, the parser path, and the request URL. An observable, repeated 4.0 (HttpException with HTTP 500) on a route that should never return 500 is a strong anomaly signal; the user-reported MVC 2,733 b error response is an exemplar detection anchor.

**Defensive telemetry vs. user-supplied oracle sizes.** The user-reported size pairs (**4,942 b** for FormatException on invalid base64 input; **5,084 b** for CryptographicException on valid base64 input) are themselves a behavioral fingerprint of an error branch that varies with input format. A defensive control would force a single, generic error page (e.g., 1,216 b IIS-fabric) and discard the MVC 2,733 b verbose fingerprint altogether.

## Defensive Controls for this Stack

These controls collapse to one principle: **disable dangerous XML features by default**, then harden the parser tier-by-tier. The .NET 4.7.4136.0 switch surface is documented [9][33]. The Oracle parity view of the same idea is in [46][47].

For .NET specifically, the recommended posture is:

- Global: set `XmlReaderSettings.DtdProcessing = Prohibit`, `XmlResolver = null`, `XInclude = false` everywhere XML is deserialized [33][10]
- ASP.NET MVC: any model binder that consumes an `XDocument` must explicitly construct a safe `XmlReader` for the stream before passing it to the model
- WCF (`BasicHttpBinding`): set `ReaderQuotas.MaxArrayLength`, `MaxStringContentLength`, `MaxBytesPerRead` small; ensure the binding uses a safe `XmlReader`
- File upload: re-encode uploaded SVG with a strict downgrade (rasterize), reject XML-based Office documents where business workflow permits, and rewrite docx/xlsx/pptx ZIP packages through a sanitization step that strips external entity references
- AS8075-hosted Azure apps have additional guidance in Microsoft's "Security control v2: Web Application Firewalls" and "Azure Front Door DDoS protection" controls (per Microsoft docs surfaced during searches); security clubs should request the Azure security baseline from the Azure customer team during scoping rather than reproduce it here **[inference, not in primary sources]**
- The Microsoft `XmlReaderSettings.XmlResolver` page explicitly notes "Starting with the .NET Framework 4.5.2, this setting has a default value of `null`"; for ASP.NET MVC 5.3 + .NET 4.7.4136.0 the default has been null for several versions, which means a misconfiguration that re-supplies the default is the failure mode

## No-Tool Gaps

Despite the broad toolset, the following gaps exist. Each line is a gap that **no currently named tool readily fills out of the box**, given that scanning the live target is out of scope and we must rely on lab replication.

| Gap | Why no tool fills it today | Build candidate (described below) |
|-----|---------------------------|----------------------------------|
| .NET Framework 4.7.4136.0-specific parser audit at scale | Existing scanners cover generic patterns but do not flag the exact `XmlReaderSettings` ctor call paths used in legacy MCV 5.3 code paths; **no** commercial scanner offers a "Mono / .NET Framework 4.7 audit pack" out of the box | Build a CodeQL pack that imports the .NET Framework 4.7 symbol table for the impacted assemblies |
| Deep discovery of WCF / SOAP endpoints | Standard active scans reach HTTP endpoints; WSDL introspection is partial in ZAP and absent in Nuclei templates | Build a Nuclei template that consumes /WSDL metadata files and tags each public operation |
| Detection of upload-time parser side-effects (in-band) | ZAP alert 90023 covers XXE in HTTP request bodies, not upload-class parser chains inside production WCF SOAP imports | Build a Nuclei template that uploads a serialized DTD inside an OOXML container and watches for the OOB callback |
| Behavioral detection of the Oracle (`enc`) | No scanner profiles the precise size oracle (4,942 / 5,084 / third) the user reports; this is a cryptography/decryption oracle, not a parser oracle, but it gates payload injection [user-supplied, not a parser finding] | Out-of-band-canary mapping of the three error paths |
| Strict `.NET 4.7.4136.0`-aware resolver spot-check | Sonar **S2755** detects "creation without safe settings" but not "default value overridden in a base class" | Build a Semgrep rule that walks base classes and overrides |

## Build Candidates

The build plan below mirrors the no-tool gaps above. Each candidate is small, MIT-friendly, and reusable. The candidates do not require an active scan of the live portal; they run against a local replica.

- **BC1 - `.NET 4.7 parity CodeQL pack`**. A CodeQL query pack targeting parser mutations specific to .NET Framework 4.7 (assembly-version patterns, BCL wrappers). Foundation: CodeQL CLI [194-196], CodeQL C# XML query packs [140, 141]. Expected output: SARIF.
- **BC2 - WSDL-discovery Nuclei template**. YAML template parses `/WSDL`, `/Wsdl`, and metadata endpoints, then tags each `<wsdl:operation>` and prints the count plus the publicly-exposed method names. Foundation: Nuclei templates, Interactsh for any OOB probes that the template might run.
- **BC3 - Upload-channel corpus harness using boofuzz**. Build a `boofuzz` session that targets the parser layer with the OOXML / SVG corpus. Foundation: boofuzz.
- **BC4 - Mutation harness with AFL++**. Compile an AFL++ harness wrapping `XmlReader.Create(Stream, XmlReaderSettings)` with `DtdProcessing = Parse` (deliberately), feed corrupted corpora, collect crashes. Foundation: AFL++ license posture is AGPL-3.0-or-later [160, 161, 180]; downstream harness outputs are Apache-2.0.
- **BC5 - Detection rule pack for the verbose YSOD page**. Use the user-supplied 2,733 b page size as a fingerprint, build a curl-based check that fails if the password-protected verbatim passes; this is *not* a scanner, it is a regression indicator that the hardening has not regressed. **Inferred value, not a tool**.
- **BC6 - CI rule pack via Semgrep and CodeQL**. Combine Semgrep OSS with CodeQL CLI on the source repository; a "fail build on XXE finding" status check. Foundation: Semgrep, CodeQL CLI [194-196].

The build candidates above are deliberately coding-free at the XML payload level; they write CI rules, SARIF outputs, and parser harnesses, not XXE payloads.

## Pre-Authorization-Safe vs. Out-of-Scope

Exhaustive partitioning of the activity set:

**Pre-authorization-safe (anyone can do today, against public references and lab replicas)**:

- Read the OWASP, PortSwigger, Oracle, and Microsoft primary sources listed in the references below [10][47][9][33].
- Configure a local IIS 10 / ASP.NET MVC 5.3 lab and apply safe parser settings; review source code; produce static-analysis rule packs [16].
- Build the WSDL crawler Nuclei template using only publicly published WSDL files such as `http://example.com/service?wsdl`. **Do not** run it against the live target.
- Build the boofuzz / AFL++ harness against the **local replica with safe parser settings**; collect crashes for documentation.
- Read user-published Burp Suite documentation; learn Repeater and Intruder behavior using Burp Suite Community (which does not require a license and does not auto-scan).

**Gated by the signed scope letter and the two test accounts**:

- Any request to the live host (`mujslcm.jaipur.manipal.edu`) other than a public-side, non-mutating GET. The user reports a "method policy GET only" already in force; we do not attack that policy [user-supplied].
- Submitting parser probes to the live `enc` parameter, including any payload that exercises the DTD or XInclude paths. The user's three-stage oracle observations are inputs, not findings, and probing the live system adds noise [user-supplied].
- Configuring an OOB receiver (Burp Collaborator, interactsh) to point at a domain you can resolve to the **live** target's hostname. Even with a Collaborator pointing at a sub-domain, the test infrastructure must be authorized.
- Submitting file uploads (XML / OOXML / SVG) to any live endpoint. Even a benign-looking "test the parser turns my file into a 500" request risks upsets the integrator's logic.
- Fuzzing the live host or its CDNs / image-rewrite endpoints.
- Any authenticated workflow. The portal uses Microsoft 365 / Entra ID identity [user-supplied]; auth handling is not free to test.

**Out of scope (do not perform even with the scope letter)**:

- Any non-public specification that requires reverse engineering or bypassing noticed-by-default controls (e.g., breaking CAPTCHA, MFA bypass). The requester explicitly excludes this category.
- Persistent state changes: writing back to test ledgers, posting grades, modifying schedules, sending SMS/email notifications triggered by the live system. Read-only authorized testing applies.
- Social-engineering humans to gain access. Out.

## Synthesis

A senior research analyst sees both the depth and the limits of this campaign. The XML and file-format attack surface is well-documented and well-tooled; the gap is not in technique but in disciplined authorization and in the absence of a fully independent verification of the supplied "MEASURED FACTS". A deliberate comparison across the tool axes bears out the picture:

- **Authenticity / Hosting**: Burp Collaborator is hosted by default in Burp Pro (high-friction, behind a paywall); interactsh is free / hosted / BYOK with multiple public domains (`oast.fun`, `oast.live`, etc.) and the option to self-host with authenticated credentials.
- **License posture**: ZAP (Apache 2.0), Nuclei + templates (MIT), Interactsh (MIT), AFL++ (AGPL-3.0-or-later + Apache-2.0 for downstream harnesses), boofuzz (permissive), Semgrep OSS (permissive), CodeQL (open-source under GitHub terms), Sonar rule **S2755** (free in SonarQube Community Edition).
- **Detection surface**: ZAP alert **90023** is canonical for XXE; CodeQL query names like `xml-injection` and `external-entity-expansion` are canonical for static analysis; Semgrep rulepacks are canonical for SAST; Sonar **S2755** is canonical for runtime misconfiguration.
- **Lab coverage**: .NET Framework 4.7.4136.0 + ASP.NET MVC 5.3 + IIS 10 is well-modelled. The cost is that **why** the customer's parser layer is misconfigured (e.g., what assembly introduced the unsafe `XmlReaderSettings`) is **not** a question a scanner can fully answer; it requires static analysis on the actual source repository, which is out of reach without the customer's permission and code.

Three non-obvious tensions emerge:

1. **The Defensive Default Not Always Sufficient.** Microsoft set `XmlResolver = null` as the default from .NET 4.5.2; the live build is .NET 4.7.4136.0 which inherits that default. **Inheritance does not equal protection when a developer re-supplies a resolver, and Sonar **S2755** does not always cross-base-class boundaries.** That gap is one of the build candidates (BC1) above.
2. **The "Get-only" `enc` parameter is your friend, not the parser's.** A GET-only site reduces the surface to passive enrollment tracking; the three-stage size oracle is consistent with that. That is good news: the parser attack universe applies only to endpoints that have POST/PUT/file-upload workflows, and the customer's existing measurements limit that set.
3. **Verbose YSOD is correlated with the parser layer, not the cookie.** The user-supplied 2,733 b MVC error page is large enough to enumerate source-code file paths; the user-supplied 1,216 b IIS-fabric page is the static ASP.NET 500 page. The exact ratio of MVC error disclosure to IIS error disclosure correlates to `customErrors = Off` (user-supplied); that setting is the variable that makes the parser error stack readable in non-production scenarios, and in production it is the variable that needs disabling as a defensive control.

For the university security club, the takeaway is that **the technique universe is textbook** and the **detection rule is on rails** (ZAP 90023; Sonar S2755; CodeQL xml-injection). The **distinct contribution** is to build the BC1/BC2/BC3/BC4/BC5/BC6 candidates against a local replica and to ship a docs set that the security club can use for the next engagement.

## References (exact URLs)

- OWASP XML External Entity Prevention Cheat Sheet - https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html [10]
- OWASP Cheat Sheet GitHub mirror - https://github.com/OWASP/CheatSheetSeries/blob/master/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.md
- OWASP XML Security Cheat Sheet (extract surfaced through PortSwigger and OWASP searches) - https://cheatsheetseries.owasp.org/cheatsheets/XML_Security_Cheat_Sheet.html
- PortSwigger XXE tutorial - https://portswigger.net/web-security/xxe
- PortSwigger Burp XXE testing docs - https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/input-validation/xxe-injection/testing
- PortSwigger Burp Collaborator - https://portswigger.net/burp/documentation/collaborator
- PortSwigger appsec.guide - https://appsec.guide/docs/web/burp/guide/manual-work/collaborator/
- OWASP ZAP XXE alert 90023 - https://www.zaproxy.org/docs/alerts/90023/ [1]
- OWASP ZAP GitHub - https://github.com/zaproxy/zaproxy
- OWASP File Upload Testing Guide (WSTG) - https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/10-Business_Logic_Testing/09-Test_Upload_of_Malicious_Files
- OWASP Logging Cheat Sheet - https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- ProjectDiscovery Nuclei - https://github.com/projectdiscovery/nuclei
- ProjectDiscovery nuclei-templates - https://github.com/projectdiscovery/nuclei-templates
- ProjectDiscovery interactsh - https://github.com/projectdiscovery/interactsh
- ProjectDiscovery Interactsh docs - https://docs.projectdiscovery.io/opensource/interactsh/running
- CodeQL main repo - https://github.com/github/codeql
- CodeQL CLI binaries license - https://github.com/github/codeql-cli-binaries/blob/main/LICENSE.md
- CodeQL CLI product docs - https://docs.github.com/en/code-security/concepts/code-scanning/codeql/codeql-cli
- CodeQL C# XML Injection query - https://codeql.github.com/codeql-query-help/csharp/cs-xml-injection/
- CodeQL XML ext-entity ql source - https://github.com/github/codeql/blob/main/csharp/ql/src/Security%20Features/CWE-091/XMLInjection.ql
- Semgrep XXE Java cheat sheet - https://docs.semgrep.dev/cheat-sheets/java-xxe
- Semgrep main repo - https://github.com/semgrep/semgrep
- Sonar rule S2755 discussion - https://community.sonarsource.com/t/java-s2755-xml-parsers-should-not-be-vulnerable-to-xxe-attacks/23149
- Sonar dotnet repository issue (rule tracker) - https://github.com/SonarSource/sonar-dotnet/issues/3096
- XXExploiter GitHub - https://github.com/luisfontes19/xxexploiter
- XXEinjector GitHub - https://github.com/enjoiz/XXEinjector
- AFLplusplus GitHub - https://github.com/AFLplusplus/AFLplusplus
- boofuzz GitHub - https://github.com/jtpereyda/boofuzz
- boofuzz PyPI - https://pypi.org/project/boofuzz/
- Microsoft XmlReaderSettings.DtdProcessing - https://learn.microsoft.com/en-us/dotnet/api/system.xml.xmlreadersettings.dtdprocessing?view=netframework-4.8.1
- Microsoft XmlReaderSettings.DtdProcessing (.NET 10) - https://learn.microsoft.com/en-us/dotnet/api/system.xml.xmlreadersettings.dtdprocessing?view=net-10.0
- Microsoft XmlReaderSettings.XmlResolver - https://learn.microsoft.com/en-us/dotnet/api/system.xml.xmlreadersettings.xmlresolver?view=netframework-4.8.1 [149.x, snippet]
- Oracle JAXP Security Guide - https://docs.oracle.com/en/java/javase/24/security/java-api-xml-processing-jaxp-security-guide.html
- Oracle JAXP Security Guide (Java 8) - https://docs.oracle.com/javase/8/docs/technotes/guides/security/jaxp/jaxp.html
- HackTricks XXE catalog - https://hacktricks.wiki/en/pentesting-web/xxe-xee-xml-external-entity.html
- PortSwigger subscription / pricing - https://portswigger.net/support/burp-suite-licensing-model
- PortSwigger download - https://portswigger.net/burp/downloads
- Stack Overflow XXE reference - https://stackoverflow.com/questions/14230988/how-to-prevent-xxe-attack-xmldocument-in-net
- xxe.page Tools guide - https://xxe.page/guide/testing/tools

## VERDICT

**Confidence**: HIGH that the technique universe, tool inventory, manual method, detection counterpart, and no-tool gaps are accurate for the *public information*. MEDIUM that the inferences specific to the live target (e.g., the `enc` oracle being a parser entry point) hold once the signed scope letter and the test accounts are in hand, because **chain-of-thought** reasoning tells us:

- Technique Universe: every cell is verifiable against at least one primary source we read [104, 96, 120, 123, 95, 114, 149, 152]. HIGH.
- Tool Inventory: every row is anchored by a GitHub or vendor URL with a license file path [169, 84, 85, 89, 90, 134, 144, 147, 160, 161, 180, 191, 194, 195]. HIGH.
- Manual Method: OWASP / PortSwigger / Oracle converge on the same four-step approach [104, 96, 95]. HIGH.
- Detection: ZAP alert 90023 [1], Sonar S2755, CodeQL [140-141], Semgrep [155-156], OWASP Logging [204-206]. HIGH on the rule names; MEDIUM on whether runtime detection will fire against the live target because `customErrors = Off` is in evidence (user-supplied).
- No-Tool Gaps / Build Candidates: justified by documented absences in the surveyed corpus. MEDIUM (correctness depends on the achieved depth of survey).
- Target-specific extrapolation: any conclusion about the live portal's parser layer is labeled inference. We do **not** claim XXE on `mujslcm.jaipur.manipal.edu`; we claim that if a parser is reachable in the import / report / SOAP / `w2c-22` paths and is configured with `XmlResolver != null` or `DtdProcessing = Parse`, the documented attack classes apply.

**Recommendation**: Phase the work as follows. Phase I (pre-authorization-safe): ship BC1 / BC2 / BC5 against the local replica and the source repository when available; document ZAP 90023 baseline behavior on the lab; build the Semgrep and Sonar **S2755** rule packs. Phase II (gated by the signed scope letter and the two test accounts): perform the live XML entry-point discovery via Nuclei templates (in read-only mode); spin up an interactsh OOB on BYOK domain the test environment owns; submit DTD-disabling probes for the parser classes relevant to .NET 4.7; document the verbose YSOD configuration status and request that the customer enable `customErrors = On`. Phase III (closure): publish the difference-based report and the BC pack to the security club.

> Nothing in this report instructs unauthorized access. Lab reproduction against a local replica is safe; live testing is gated. Inferences are clearly labeled throughout. The technique universe, tool inventory, detection counterpart, no-tool gaps, and build candidates together form a complete research plan.

## References

1. *ZAP – XML External Entity Attack*. https://www.zaproxy.org/docs/alerts/90023/
2. *XML Security - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/XML_Security_Cheat_Sheet.html
3. *Testing for XXE injection vulnerabilities with Burp Suite - PortSwigger*. https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/input-validation/xxe-injection/testing
4. *Burp Collaborator - PortSwigger*. https://portswigger.net/burp/documentation/collaborator
5. *GitHub - projectdiscovery/nuclei-templates: Community curated list of templates for the nuclei engine to find security vulnerabilities. · GitHub*. https://github.com/projectdiscovery/nuclei-templates
6. *XXExploiter | xxexploiter*. https://luisfontes19.github.io/xxexploiter/
7. *GitHub - projectdiscovery/interactsh: An OOB interaction gathering server and client library · GitHub*. https://github.com/projectdiscovery/interactsh
8. *Running Interactsh interactsh-client*. https://docs.projectdiscovery.io/opensource/interactsh/running
9. *XmlReaderSettings.DtdProcessing Property (System.Xml) | Microsoft Learn*. http://learn.microsoft.com/en-us/dotnet/api/system.xml.xmlreadersettings.dtdprocessing?view=netframework-4.8.1
10. *XML External Entity Prevention - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html
11. *What is XXE (XML external entity) injection? Tutorial & Examples | Web Security Academy*. https://portswigger.net/web-security/xxe
12. *Download Burp Suite - PortSwigger*. https://portswigger.net/burp/downloads
13. *interactsh/LICENSE.md at main · projectdiscovery ... - GitHub*. https://github.com/projectdiscovery/interactsh/blob/master/LICENSE.md
14. *GitHub - zaproxy/zaproxy: The ZAP by Checkmarx Core project · GitHub*. http://github.com/zaproxy/zaproxy
15. *nuclei-templates/LICENSE.md at main - GitHub*. https://github.com/projectdiscovery/nuclei-templates/blob/main/LICENSE.md
16. *XML injection — CodeQL query help documentation - GitHub*. https://codeql.github.com/codeql-query-help/csharp/cs-xml-injection/
17. *codeql-cli-binaries/LICENSE.md at main - GitHub*. https://github.com/github/codeql-cli-binaries/blob/main/LICENSE.md
18. *GitHub - github/codeql: CodeQL: the libraries and queries ...*. https://github.com/github/codeql
19. *CodeQL CLI - GitHub Docs*. https://docs.github.com/en/code-security/concepts/code-scanning/codeql/codeql-cli
20. *Rule S2755: XML parsers should not be vulnerable to XXE ...*. https://github.com/SonarSource/sonar-dotnet/issues/3096
21. *Prevent XML External Entity Vulnerabilities for Java - Semgrep*. https://docs.semgrep.dev/cheat-sheets/java-xxe
22. *skills/skills/code-security/rules/xxe.md at main · semgrep ...*. https://github.com/semgrep/skills/blob/main/skills/code-security/rules/xxe.md
23. *GitHub - semgrep/semgrep: Lightweight static analysis for many languages. Find bug variants with patterns that look like source code. · GitHub*. http://github.com/semgrep/semgrep
24. *GitHub - AFLplusplus/AFLplusplus: The fuzzer afl++ is afl ...*. https://github.com/AFLplusplus/AFLplusplus
25. *AFLplusplus/README.md at stable · AFLplusplus/AFLplusplus*. https://github.com/AFLplusplus/AFLplusplus/blob/stable/README.md
26. *GitHub - jtpereyda/boofuzz: A fork and successor of the ...*. https://github.com/jtpereyda/boofuzz
27. *GitHub - Jesh23/fuzzing: A fork and successor of the Sulley ...*. https://github.com/Jesh23/fuzzing
28. *boofuzz · PyPI*. https://pypi.org/project/boofuzz/
29. *GitHub - enjoiz/XXEinjector: Tool for automatic exploitation ...*. https://github.com/enjoiz/XXEinjector
30. *GitHub - The-Cracker-Technology/XXEinjector*. https://github.com/The-Cracker-Technology/XXEinjector
31. *Logging - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
32. *Implement Security Logging and Monitoring - OWASP Developer Guide*. https://devguide.owasp.org/en/04-design/02-web-app-checklist/09-logging-monitoring/
33. *XmlReaderSettings.DtdProcessing Property (System.Xml)*. https://learn.microsoft.com/en-us/dotnet/api/system.xml.xmlreadersettings.dtdprocessing?view=net-10.0
34. *XXE - XEE - XML External Entity - HackTricks*. https://hacktricks.wiki/en/pentesting-web/xxe-xee-xml-external-entity.html
35. *How to prevent XXE attack (XmlDocument in .NET)*. https://stackoverflow.com/questions/14230988/how-to-prevent-xxe-attack-xmldocument-in-net
36. *WSTG - Latest - OWASP Foundation*. https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/10-Business_Logic_Testing/09-Test_Upload_of_Malicious_Files
37. *Burp Suite subscription model - PortSwigger*. https://portswigger.net/support/burp-suite-licensing-model
38. *PortSwigger Software Pricing & Plans 2026: See Your Cost*. https://www.vendr.com/marketplace/portswigger
39. *Burp Collaborator | Testing Handbook - appsec.guide*. https://appsec.guide/docs/web/burp/guide/manual-work/collaborator/
40. *nuclei/LICENSE.md at dev · projectdiscovery/nuclei · GitHub*. https://github.com/projectdiscovery/nuclei/blob/dev/LICENSE.md
41. *GitHub - projectdiscovery/nuclei: Nuclei is a fast ...*. https://github.com/projectdiscovery/nuclei
42. *ProjectDiscovery - GitHub*. https://github.com/projectdiscovery
43. *Interactsh Options · projectdiscovery interactsh - GitHub*. https://github.com/projectdiscovery/interactsh/discussions/813
44. *About | Semgrep*. http://semgrep.dev/about
45. *java:S2755 XML parsers should not be vulnerable to XXE ...*. https://community.sonarsource.com/t/java-s2755-xml-parsers-should-not-be-vulnerable-to-xxe-attacks/23149
46. *Java API for XML Processing (JAXP) Security Guide*. https://docs.oracle.com/en/java/javase/24/security/java-api-xml-processing-jaxp-security-guide.html
47. *Java API for XML Processing (JAXP) Security Guide - Oracle*. https://docs.oracle.com/javase/8/docs/technotes/guides/security/jaxp/jaxp.html
