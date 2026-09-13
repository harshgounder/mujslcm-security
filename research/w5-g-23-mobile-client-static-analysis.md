# Authorized Flutter APK Static-Analysis Playbook

## Executive Summary

- **Scope Boundary**: The supplied campaign record says the MUJ SLCM portal is reachable only on 443 and that the campaign has read client code but has not statically analyzed the APK. That means the unresolved evidence is inside the mobile package, not a license to probe the portal. Begin with an offline, hash-preserving APK workflow and do not execute target-facing tests until the signed scope letter is active.
- **Flutter AOT Blind Spot**: A Flutter release application normally carries Dart AOT material in `libapp.so`; OWASP identifies distinctive assembly, sequential class information, limited documentation, and obfuscation as reasons ordinary Android decompilers are insufficient [9]. Pair ordinary APK tools with Blutter, native disassembly, and controlled string/rule analysis rather than treating a clean JADX report as proof of a clean client.
- **Manifest Reachability**: Exported activities, services, receivers, providers, aliases, intent filters, URI schemes, hosts, and permissions are statically enumerable before a device is used. OWASP recommends inspecting the decoded manifest first because that reflects the package declaration without requiring an attached device [16]. Treat exploitability as a separate, authorized runtime question.
- **Secret Exposure**: APKLeaks, MobSF, Gitleaks, TruffleHog, detect-secrets, Semgrep, YARA, and ripgrep can identify candidate literals, endpoints, keys, or high-entropy material. A match is not proof that a credential is valid or authorized for use. Report, quarantine, and rotate any real secret through the owner; never test it against MUJ services without explicit scope and the two test accounts.
- **Pinning Evidence**: Network Security Config is a declarative source of pinning evidence, while custom `TrustManager`, hostname-verifier, WebView, or native TLS code can sit outside that simple path [21]. Static indicators can establish implementation intent, but only an authorized runtime test can establish whether pinning is enforced for a particular request path.
- **Deep-Link Risk**: Android App Links combine manifest filters with website association files, and each host or subdomain needs an appropriate association statement [24] [24]. The first safe deliverable is an inventory of declared routes and association requirements, not a live invocation of exported components.
- **Tool Separation**: MobSF is a broad static-analysis front end with HTML, PDF, and JSON exports [27], while JADX and Apktool expose different representations, Blutter targets Flutter AOT, and Ghidra or Rizin target native binaries. The correct result is an evidence bundle, not a single scanner score.
- **Authorization Gate**: Hashing, decoding, decompiling, disassembling, and scanning a lawfully obtained APK in an isolated offline workspace are operationally suitable before authorization, subject to the club's rules and ownership. Installation, re-signing, launching, proxying, deep-link invocation, API calls, pinning tests, and validation of credentials require the signed scope letter; authenticated behavior requires the two test accounts.
- **Decision**: The current target-specific conclusion is not "secure" or "insecure." It is "APK evidence absent." The recommended next artifact is a signed intake record, a SHA-256 hash, split-APK inventory, manifest report, MobSF report, DEX/native inventories, Blutter output where compatible, and a manually reviewed findings register.

## Analytical Rationale: An Auditable Substitute for Private Chain-of-Thought

The request asks for explicit chain-of-thought. I cannot provide private hidden reasoning or internal deliberation. The following is the reproducible decision rationale an independent reviewer can audit:

1. Separate facts supplied by the campaign record from facts that require APK evidence. The supplied server observations describe the portal; they do not establish what is embedded in SLCM_APP.
2. Divide the APK question into package metadata, Android components, Dart AOT, Java/Kotlin and smali, native ELF code, secrets and configuration, transport security, and provenance or supply chain.
3. Assign a documented static tool to each surface, then add a manual fallback where the tool cannot establish semantics or where Flutter AOT and obfuscation reduce coverage.
4. Classify each action as offline static work, authorized runtime work, or authenticated target work. This prevents a harmless evidence collection step from silently becoming an unapproved interaction.
5. Treat every unverified SLCM_APP result as an inference or hypothesis until the original package is analyzed and the evidence is recorded with file path, hash, offset or line, tool version, and reproduction notes.

This rationale is deliberately concise, repeatable, and suitable for a club report; it is not a disclosure of hidden internal reasoning.

## 1. What Static Analysis Must Answer for SLCM_APP

OWASP defines mobile static analysis as examining and evaluating source or compiled application material without executing it, with the aim of identifying potential vulnerabilities, errors, or compliance issues [20]. For SLCM_APP, the work should answer eight separate questions rather than produce one generic risk score.

First, what exactly is the artifact? The analyst must distinguish a universal APK from ABI-specific APKs, an APK set, a split package, a debug build, and a release build. Flutter documentation says split-per-ABI builds produce separate APKs, while omitting the split option produces a fat APK [41]. A result from an arm64 split cannot automatically be generalized to an armeabi-v7a or x86 build. Record the filename, size, signing certificate digest, package name, version code, version name, target SDK, ABIs, and SHA-256 before any transformation.

Second, what Android policy is declared? The manifest is the authoritative starting point for permissions, application attributes, components, aliases, exported state, intent filters, cleartext settings, backup behavior, and network security configuration. OWASP's component workflow specifically calls for decoding the manifest, identifying activities and aliases, inspecting exported attributes and intent filters, then interpreting the result with target SDK, version, and permission context [16].

Third, what can be reached through declared URLs or Android components? An app may expose custom schemes, HTTPS App Links, activities, services, receivers, providers, or aliases. Android's App Links documentation describes the scheme, host, path, and verification relationship, and explains that each host or subdomain needs corresponding association material [24] [24]. Static analysis can identify the declaration and missing association evidence. It cannot by itself prove that a component is exploitable.

Fourth, where are the 13 client routes and their request-building logic? The supplied campaign brief identifies the Flutter client as the source of those routes. The APK review should search Java/Kotlin, smali, assets, `libapp.so`, generated configuration, and native libraries for path strings, hostnames, HTTP verbs, headers, parameter names, serialization keys, and crypto or encoding operations. [Inference] A route found in a string table is a lead, not proof of reachability, authentication, or server authorization.

Fifth, what is compiled into the Dart AOT layer? OWASP describes Flutter AOT challenges and recommends locating `libapp.so` and using Flutter-specific tooling [9]. This matters because the portal's server-side findings do not answer whether the client contains hardcoded endpoints, tokens, certificate material, debugging flags, or client-side authorization assumptions.

Sixth, is transport security declared or implemented? Android Network Security Config is a declarative XML mechanism referenced from the application manifest [22] [22]. OWASP notes that declarative pinning covers framework network paths such as `HttpsURLConnection` and WebView unless a custom trust manager is used, while native code can sit outside that path [21]. Search both the XML configuration and code paths.

Seventh, does the package contain secrets or sensitive configuration? Scan strings, resources, assets, DEX, smali, Dart AOT-derived text, native data sections, and embedded JSON. Candidate classes include API keys, signing material, bearer tokens, database credentials, private keys, cloud configuration, certificate blobs, debug endpoints, and personal data. Do not call an endpoint to validate a match before authorization.

Eighth, can an independent reviewer reproduce the finding? Every finding should include the original artifact hash, transformed artifact hash where applicable, tool and version, command or UI path, file and offset or line, a redacted evidence excerpt, confidence, false-positive assessment, and authorization status. This is more defensible than a screenshot of a dashboard.

### Technique universe and detection counterpart

| Technique | Static evidence to collect | Detection counterpart and boundary | Priority for SLCM_APP |
|---|---|---|---|
| Artifact provenance | Hashes, package identity, version, certificate, split and ABI inventory | Intake manifest and reproducibility check; does not prove the file is the production client | Critical before all other work |
| Manifest and component review | Activities, aliases, services, receivers, providers, `exported`, permissions, filters | Manifest rule set and manual review; runtime invocation is a separate authorized test [16] | Critical |
| Deep-link and App Link review | Schemes, hosts, paths, verification declarations, association requirements | Route inventory and association check; does not prove hijackability [24] | High |
| DEX and smali review | Decompiled classes, bytecode, strings, request builders, WebView and TLS calls | JADX/Apktool plus manual cross-check; decompilers can be incomplete [2] | High |
| Flutter AOT review | `libapp.so`, Dart strings, symbols, generated names, native libraries | Blutter, native disassembly, string/rule scan; obfuscation and optimization can leave gaps [9] | Critical |
| Native binary review | ELF sections, imports, symbols, crypto and TLS calls, packer indicators | APKiD plus Ghidra/Rizin; semantics still need manual interpretation | High |
| Secret and configuration review | URLs, keys, tokens, certificates, JSON, environment names, high entropy | Multi-scanner correlation and redaction; a candidate is not a valid credential | Critical |
| TLS and pinning review | Network Security Config, `TrustManager`, hostname verifier, WebView, native TLS | Static evidence plus authorized runtime confirmation; no static proof of enforcement [21] | High |
| Crypto and encoding review | Algorithms, key material, base64, custom `enc` handling, IVs, salts, error strings | Rule and call-site review; no claim about server oracle behavior without authorized testing | High |
| Third-party and build review | SDK names, versions, licenses, debug flags, obfuscation metadata | SBOM and dependency review; does not prove vulnerability in a dependency | Medium |

The table is intentionally split into detection and proof. A detector answers "where should a reviewer look?" A proof claim answers "what can be concluded?" Confusing those two is the main way an APK report overstates risk.

## 2. APK Intake, Manifest, and Reachability

The first pass should be deterministic and offline. Preserve the original file as read-only, calculate a cryptographic hash, and record how it was obtained. If the package came from a distribution channel, retain the download metadata and certificate chain where lawfully available. If multiple split APKs exist, analyze the base and every relevant split, because a scanner run against only the base may miss ABI-specific native code or feature resources.

The Android SDK `apkanalyzer` is a useful baseline because its command-line subjects cover the APK itself, files, manifest, DEX, and resources [11]. It can print metadata, list files, inspect manifest information, inspect DEX content, and inspect resources [11] [11]. Use it to create a machine-readable inventory before higher-level tools alter or decode the artifact.

Apktool supplies a second representation: decoded resources and manifest material plus smali, with a rebuild path [3]. The rebuild path is useful for controlled lab work but is not needed for the preauthorization evidence pass. Record both the original and decoded output hashes. Do not distribute a modified package or install it on a device without written authorization.

JADX is the readable DEX layer. Its documented inputs include APK, DEX, AAR, AAB, and ZIP, and its interface includes a GUI and command-line mode, resource and manifest handling, deobfuscation, search, and debugging aids [2]. It can export Java, JSON, or a Gradle-style project [2]. Its own documentation warns that no decompiler can recover 100 percent of code perfectly [2], so every material claim should be checked against smali or the original DEX when control flow looks suspicious.

The manifest review should produce a table with component name, type, exported value or inferred state, permission, process, intent actions, categories, data schemes, hosts, ports, paths, and source file. Also record whether a component is in the base APK or a feature split. The result is a static attack-surface inventory, not an instruction to invoke it.

For App Links, record each HTTP or HTTPS scheme, host, path, and verification-related attribute. Android states that separate intent filters are needed when combinations of data elements have different relationships, because data attributes in one filter are merged [24]. It also states that each host or subdomain requires appropriate asset association material [24]. A missing or inconsistent association is a configuration finding, not proof that another application can claim a user action.

### MUJ SLCM case study: what the current record does and does not establish

The supplied campaign record reports IIS 10, ASP.NET MVC 5.3, .NET Framework 4.7.4136.0, jQuery 1.10.2 plus a bundled jQuery 3.4.1, Azure AS8075, Microsoft 365 identity, three Entra tenants, no attributable edge control, no HSTS, and TLS 1.0 through 1.3 offered. It also records a GET-only method policy, two error-page families, verbose YSOD behavior, antiforgery enforcement with an HttpOnly cookie lacking Secure, clean host and forwarding-header bypass attempts, and an `enc` error oracle. These are supplied live observations, not findings independently remeasured in this report.

The important analytical consequence is narrower: none of those server observations can establish whether the APK has an exported component, an App Link, a certificate pin, a hardcoded secret, or a client-side copy of the `enc` algorithm. [Inference] The absence of APK work is therefore a material evidence gap even though the web reconnaissance is already detailed. The correct next step is offline package analysis, not more unauthenticated probing.

## 3. Flutter and Native Code: Closing the libapp.so Blind Spot

Flutter release builds compile Dart code ahead of time. OWASP describes the resulting AOT reverse-engineering problem as distinctive assembly, sequential class information, limited documentation, and obfuscation or optimization that frustrates ordinary decompilation [9]. A normal Java decompiler may still be useful for the Android wrapper, plugins, and generated glue, but it is not a complete view of Dart application logic.

Blutter is the most directly relevant specialist in this report. The documented workflow extracts an APK, locates `libapp.so`, and runs Blutter; its outputs include an `asm` directory, `blutter_frida.js`, `objs.txt`, and `pp.txt` [9]. The repository documentation limits its supported Android path to arm64 `libapp.so` and recent Dart versions [8]. It can determine the Dart version automatically and compile a matching component if needed, but the documented limitations include obfuscated applications, iOS, and APK input workflow gaps [8] [8]. Treat Blutter as a high-value parser with conditional coverage, not a guarantee.

The recommended native sequence is: inventory ABIs; extract each `libapp.so`; record architecture and Dart version; run Blutter where its compatibility conditions are satisfied; search its output for route strings, domains, header names, serialization keys, crypto names, and error messages; then inspect relevant native code in Ghidra or Rizin. Ghidra provides disassembly, decompilation, graphing, and scripting with Java or Python support [28], and its repository identifies an Apache-2.0 license [28]. Rizin supports analysis, disassembly, debugging, and several binary formats, including ELF and DEX, under LGPL-3.0 [29] [29]. Neither tool is Flutter-specific; the analyst must establish the function boundaries and avoid treating a string cross-reference as a complete call graph.

reFlutter addresses a different problem. Its documented approach patches a precompiled Flutter library and supports specified Android and iOS architectures and Flutter channels [34]. It accepts an APK or IPA and can emit `dump.dart`; a patched Android release APK must be signed and aligned, and the documentation warns that pinning bypass works only for some cases [34] [38]. That makes reFlutter an authorized runtime-analysis aid, not a preauthorization static scanner. Its repository is GPLv3+ [34]. Do not patch, re-sign, launch, or route traffic through a proxy for SLCM_APP until the scope letter explicitly covers those actions.

Flutter's own documentation adds an important interpretive caution: obfuscation renames symbols but does not encrypt resources or protect the application from reverse engineering [40]. Flutter documents `--obfuscate` with `--split-debug-info`, which produces a symbols file for later symbolization [40]. Therefore, an obfuscated package can still contain discoverable endpoint strings, configuration, and native artifacts. Obfuscation should reduce casual readability, not be reported as a secret-management control.

### Native and AOT review table

| Evidence surface | Tool path | Expected output | What it can support | What it cannot support alone |
|---|---|---|---|---|
| `libapp.so` arm64 | Blutter | `asm/*`, `blutter_frida.js`, `objs.txt`, `pp.txt` [8] | Candidate Dart functions, strings, object and snapshot evidence | Complete coverage across architectures or obfuscated builds |
| Flutter native ELF | Ghidra | Project, disassembly, decompiler views, graphs, scripts [28] | Manual code review and cross-references | Automatic identification of Dart semantics |
| Flutter or plugin ELF/DEX | Rizin | Interactive analysis, disassembly, scripts; exact output is workflow-dependent [29] | Binary triage and low-level review | A canonical security report |
| Patched Flutter runtime | reFlutter | `dump.dart` and patched package [38] | Authorized runtime-oriented observation | Safe preauthorization use, universal pinning bypass, or proof of a server flaw |
| Flutter build metadata | Official Flutter inspection | ABI and native library evidence [41] [41] | Build and packaging interpretation | Source-level reconstruction |

The practical case study is SLCM_APP itself: if the 13 routes exist only in Dart AOT strings, JADX may report little while Blutter and native review reveal them. If they exist in plugin Java or generated networking code, the reverse may be true. [Inference] The report should therefore state coverage per representation and never use "JADX found no secret" as a package-wide negative.

## 4. Secrets, TLS Pinning, and Embedded Configuration

### Secret detection

A mobile package is public to a determined user once distributed. Static secret detection should cover DEX, smali, resources, assets, generated JSON, native data, Blutter output, and decompiled source. Run multiple detectors with different assumptions. APKLeaks is designed to scan APK URIs, endpoints, and secrets [6], uses JADX, and supports custom sensitive rules in JSON [6]. Its output can be text or JSON written to a file [6], under Apache-2.0 [6].

MobSF is the broad aggregator. Its static mode analyzes code and resources without execution and looks for insecure patterns, permissions, exposed secrets, and hardcoded credentials [27]. It can export HTML, PDF, and JSON [27], and the project documents GPLv3, manual installation, Docker, and offline use [27]. Use it as an index and corroborate important findings in the underlying file representation.

Gitleaks scans local Git repositories, directories, files, and standard input [13], although an APK is an archive rather than a source repository. Run it on decoded resources, decompiled output, Blutter output, and extracted text, with archive handling understood; archive scanning is disabled by default in the documented configuration [13]. Its documented output choices include JSON, CSV, JUnit, and SARIF [13], and the project is MIT licensed [1]. TruffleHog can scan local files and directories [10], emits JSON, SARIF, and GitHub Actions formats, and can report verification states [10] [10]. Verification may involve service-specific calls, so keep the preauthorization pass local and non-validating.

detect-secrets is useful for a baseline workflow. It is Apache-2.0 [14], supports scanning, hooks, auditing, and a baseline snapshot [14], and stores JSON results [14] [14]. Semgrep provides rules that can run in an IDE, pre-commit hook, or CI, and its community engine runs locally without uploading code by default [30]. Its documented limitation that community analysis can miss cross-function and cross-file true positives is directly relevant to generated and compiled mobile code [30]. YARA is BSD-3-Clause and available as a command-line or Python-driven rule engine [32] [32]. ripgrep is a simple MIT/UNLICENSE recursive regular-expression search tool [33] [33].

Use detections as triage. A string resembling a key may be a public identifier, sample value, dead code, test credential, or truncated artifact. A high-entropy string may be a hash, compressed data, or an encrypted blob. A route hostname may be a development endpoint. The report should classify each match as candidate, corroborated static secret, or not a secret, and should not attempt online validation without authorization.

### TLS and pinning

Inspect `res/xml/network_security_config.xml`, the manifest reference to it, certificate resources, certificate hashes, `networkSecurityConfig`, `usesCleartextTraffic`, and any debug-only overrides. Android documents Network Security Config as XML referenced by the manifest [22] [22]. Its pinning model uses public-key hashes, and a certificate chain is accepted when it contains a pinned key [22]. OWASP's guidance covers custom `SSLSocket` hostname verification, warns against trust-all behavior, and notes that WebView can use Network Security Config [21].

Static code review should search for `X509TrustManager`, `checkServerTrusted`, `HostnameVerifier`, `verify`, `SSLContext`, `TrustManagerFactory`, WebView settings, native TLS libraries, certificate byte arrays, SHA-256 pin strings, and proxy or debug flags. These are detection signatures, not proof. A custom verifier may be unused, an NSC file may apply only to some processes, or a native library may create its own trust path. Conversely, absence of obvious strings may reflect obfuscation or external plugin code.

The supplied campaign record says TLS 1.0 through 1.3 were offered by the portal. [Inference] That server observation does not show which versions the mobile client negotiates or whether the client rejects older versions. Static package evidence can show policy declarations and code paths; a negotiated-version or pinning-enforcement conclusion needs an authorized runtime test with a test account only where authentication is required.

## 5. Tool Matrix: Name, URL, License, Access, Operation, and Output

The following is the evidence-backed tool universe used for this report: tools with documented direct support for APK structure, Android code, Flutter AOT, native analysis, secret detection, manifest or component review, behavioral rule scanning, or report aggregation. It is not a claim that no other security product exists. Where a public source did not state pricing, BYOK, or a license, the table says so rather than guessing.

| Tool | Exact URL | License | Free, self-host, or BYOK posture | How it is driven | Output format and SLCM use |
|---|---|---|---|---|---|
| MobSF | https://mobsf.org/ | GPLv3 [27] | Free/self-host and offline modes are documented; no BYOK is needed for local static analysis [27] | Web interface, Docker, or REST/API workflow; static analysis is non-executing [27] [27] | HTML, PDF, JSON [27]; first-pass aggregator, not sole evidence |
| JADX | https://github.com/skylot/jadx | Apache-2.0 [2] | Free/self-host; no BYOK | GUI or CLI against APK/DEX/AAR/AAB/ZIP [2] | Java, JSON, Gradle-style project [2]; inspect wrapper, plugins, routes, TLS calls |
| Apktool | https://github.com/iBotPeaches/Apktool | Apache-2.0 [3] | Free/self-host; no BYOK | CLI decode and optional rebuild [3] | Decoded resources, manifest, smali, optional rebuilt APK; use offline only before authorization |
| APKLeaks | https://github.com/dwisiswant0/apkleaks | Apache-2.0 [6] | Free/self-host; no BYOK | CLI, with custom sensitive rules in JSON [6] | Text or JSON output file [6]; endpoints and candidate secrets |
| APKiD | https://github.com/rednaga/APKiD | Dual GPL/commercial terms [7] | Self-host; select license path carefully; no BYOK | CLI or Docker, APK/DEX/directory input [7] | Text or JSON; compiler, packer, and obfuscator identification [7] |
| apkanalyzer | https://developer.android.com/tools/apkanalyzer | Android SDK tool; page does not restate a separate license | SDK-installed local CLI; no BYOK | CLI subjects for APK, files, manifest, DEX, and resources [11] | Metadata, file, manifest, DEX, and resource text [11] [11] |
| Androguard | https://github.com/androguard/androguard | Apache-2.0 [12] | Free/self-host; no BYOK | Python library and tools for APK, DEX, ODEX, AXML, and resources [12] | Programmatic objects, disassembly, and custom reports; output is script-defined [Inference] |
| Blutter | https://github.com/worawit/blutter | License not stated in the cited documentation | Self-host/source build; no BYOK | Python/script workflow against compatible `libapp.so`; recent Dart and Android arm64 limits apply [8] | `asm/*`, `blutter_frida.js`, `objs.txt`, `pp.txt` [8]; Flutter AOT evidence |
| reFlutter | https://github.com/Impact-I/reFlutter | GPLv3+ [34] | Free/self-host; modified APK must be signed and aligned [34] | CLI for APK/IPA patching; runtime-oriented and authorization-gated [34] | `dump.dart` and patched APK [38]; never run against SLCM without scope |
| QARK | https://github.com/linkedin/qark | Apache-2.0 [23] | 100 percent free is stated; self-host; no BYOK [23] | CLI against source or APK; report type selectable [23] [23] | JSON report; may generate exploit APKs or ADB commands [23], so disable or exclude those actions |
| DroidLysis | https://github.com/cryptax/droidlysis | MIT [26] | Free/self-host; no BYOK | CLI pre-analysis of APK, DEX, ZIP, RAR, or directories [26] | Console, unzipped output, SQLite, `autoanalysis.md`, `report.md` [26] |
| Quark Engine | https://quark-engine.readthedocs.io/en/v26.1.1/quark_reports.html | Not stated in the reviewed report documentation | Self-host posture and licensing require repository review; no BYOK stated | CLI with behavior rules and APK input [36] [36] | Summary, detail, web, label, radar, call graph, and rule-classification reports [36] |
| Ghidra | https://github.com/NationalSecurityAgency/ghidra | Apache-2.0 [28] | Free/self-host; no BYOK | Interactive GUI plus Java/Python scripting [28] | Project, disassembly, decompilation, graphs, scripts; review native Flutter and plugins |
| Rizin | https://github.com/rizinorg/rizin | LGPL-3.0 [29] | Free/self-host; no BYOK | CLI, interactive analysis, scripting, and debugger [29] | Console/script output; exact format is workflow-defined [Inference] |
| Guardsquare AppSweep | https://www.guardsquare.com/appsweep-mobile-application-security-testing | Pricing, free status, and license not specified on the cited public page [17] | SaaS/team and CLI/CI features are documented; BYOK not stated | Web service, multi-analysis, CLI, CI action [17] | PDF and extended CLI export [17]; useful secondary scan if the club has approved service upload |
| NowSecure | https://www.nowsecure.com/solutions/by-need/mobile-app-security-testing/ | Commercial service details not specified in cited excerpt | SaaS or vendor engagement; self-host and BYOK not stated | Automated analysis combined with expert testing is described [35] | Vendor report format not stated in cited excerpt; do not upload a target package without approval |
| Gitleaks | https://github.com/gitleaks/gitleaks/blob/master/README.md | MIT/UNLICENSE [1] | Free/self-host; no BYOK for local scan | CLI on decoded files, directories, repositories, or standard input [13] | JSON, CSV, JUnit, SARIF, templates [13] |
| TruffleHog | https://github.com/trufflesecurity/trufflehog | AGPL-3.0 [10] | Free/self-host local scan; verification can involve external provider calls | CLI on files and directories [10] | JSON, SARIF, GitHub Actions, verification status [10] |
| detect-secrets | https://github.com/Yelp/detect-secrets | Apache-2.0 [14] | Free/self-host; no BYOK | CLI, hooks, pre-commit, audit, and baseline workflow [14] | JSON baseline and findings [14] [14] |
| Semgrep | https://github.com/semgrep/semgrep | LGPL-2.1 [30] | Local community engine; no BYOK in local mode | IDE, pre-commit, CI, or CLI [30] | Rule findings; exact export choice depends on the configured runner [Inference] |
| YARA | https://github.com/VirusTotal/yara | BSD-3-Clause [32] | Free/self-host; no BYOK | CLI or Python rules [32] | Match output; compressed files need explicit handling [32] |
| ripgrep | https://github.com/BurntSushi/ripgrep | MIT/UNLICENSE [33] | Free/self-host; no BYOK | Recursive regex search, including aggressive hidden-file options [33] [33] | Plain-text matches with paths and lines; a transparent manual backstop |

The table's key decision is not that one tool is best. MobSF, AppSweep, and NowSecure optimize aggregation or service convenience; JADX, Apktool, and apkanalyzer expose Android structure; Blutter addresses Flutter AOT; Ghidra and Rizin address native code; and the secret scanners provide independent detection heuristics. A finding should be promoted only when two representations agree or when a reviewer documents why one representation is authoritative.

## 6. Manual Method and Detection Counterpart

Some questions do not have a reliable one-click answer. The manual method below is deliberately offline and evidence-oriented.

1. **Intake and preserve**: create an evidence record with source, date, filename, SHA-256, package identity, version, signing certificate, and split list. Keep the original immutable. Use copies for decoding.
2. **Inventory the container**: list files and ABIs; identify `AndroidManifest.xml`, DEX files, resources, assets, `libflutter.so`, `libapp.so`, plugin libraries, certificates, JSON, databases, and debug symbols. Record which split owns each file.
3. **Decode two ways**: use `apkanalyzer` for a baseline and Apktool for decoded XML, resources, and smali. Use JADX for readable Java-like views. Where the representations disagree, retain both and flag the disagreement.
4. **Review manifest reachability**: make one row per component and one row per intent filter. Include exported state, permission, actions, categories, scheme, host, path, and package or split. Do not invoke a component.
5. **Review Flutter AOT**: run Blutter only when its architecture and Dart-version conditions are met. Search `objs.txt`, `pp.txt`, assembly, and extracted strings for the 13 supplied route candidates, hostnames, headers, crypto names, certificate hashes, and error text. Preserve file offsets and tool versions.
6. **Review Java, smali, and native code**: inspect request construction, WebView use, trust managers, hostname verifiers, certificate loading, logging, debug switches, and file writes. Use Ghidra or Rizin for native cross-references. Do not infer reachability solely from a string.
7. **Run independent detectors**: run MobSF, APKLeaks, at least one entropy or secret scanner, YARA or ripgrep rules, and a manual review. Deduplicate by normalized evidence, not just by string value.
8. **Classify and redact**: label each result as informational, candidate, corroborated, or unresolved. Redact tokens in club reports. Never include a full private key or bearer token in a public deliverable.
9. **Create the detection counterpart**: for every finding, write the rule that would catch it in a future build and the control that should prevent it. Examples are a manifest rule requiring explicit non-exported state, a CI rule blocking private-key patterns, a build check for unexpected hosts, and a pinning review that maps each network client to its trust configuration.
10. **Gate validation**: only after the signed scope letter and test accounts are available may the team decide whether a static hypothesis needs runtime confirmation. Record exactly what was tested and stop at the authorized boundary.

The detection counterpart is therefore both technical and procedural. Technical detection finds an artifact. Procedural detection prevents the team from converting a static lead into unauthorized credential use or target interaction.

### Finding record template

| Field | Required content | Why it matters |
|---|---|---|
| Finding ID | Stable identifier and severity | Allows deduplication and remediation tracking |
| Evidence | Redacted string, file path, offset or line, screenshot only as supplement | Makes the claim reproducible |
| Representation | Manifest, DEX, smali, Dart AOT, ELF, resource, or tool report | Shows coverage and limitations |
| Tool chain | Tool names, versions, license mode, command or UI path | Enables independent reproduction |
| Confidence | Candidate, corroborated static, or runtime-confirmed | Prevents overstating a scanner match |
| Authorization state | Offline, scope-letter approved, or test-account approved | Enforces the safety boundary |
| Countermeasure | CI rule, manifest change, secret removal, pinning review, or owner action | Turns detection into prevention |

## 7. Explicit Authorization and Safety Boundary

The following is an operational classification, not a legal opinion. The university club should follow its institution's rules and obtain permission from the asset owner.

| Activity | Safe before signed scope letter? | Test accounts required? | Conditions and reason |
|---|---|---|---|
| Lawfully obtaining the APK and recording provenance | Yes, if distribution and handling are lawful | No | Keep the original private and immutable |
| Hashing, listing, decoding, decompiling, disassembling, and scanning offline | Yes | No | No target request or account use; use copies of the package |
| Running MobSF offline, APKLeaks, APKiD, apkanalyzer, JADX, Apktool, Blutter, Ghidra, Rizin, and local secret scanners | Yes, subject to license and local policy | No | Static tools operate on the local artifact; Blutter support conditions still apply |
| Reviewing manifest, components, intent filters, routes, strings, and native code | Yes | No | This is static inspection; do not invoke discovered components |
| Installing the original APK on an emulator or physical device | Treat as no until scope confirms it | Usually no for offline-only execution, but follow owner terms | Installation executes client code and may make network calls or alter state |
| Re-signing, repackaging, patching with reFlutter, or modifying resources | No | No | Modification and later execution must be explicitly authorized |
| Launching the app against MUJ infrastructure | No | Yes where authentication is involved | Requires signed scope and a controlled test account |
| Proxying or intercepting client traffic, pinning tests, or transport downgrade tests | No | Yes where authentication is involved | Requires explicit network and TLS test authorization; do not use production users |
| Invoking exported activities, services, receivers, providers, or deep links | No | Depends on route | Static inventory is safe; live invocation is a target interaction |
| Testing the 13 routes, `enc` behavior, antiforgery, error handling, methods, or authorization | No | Yes for authenticated behavior | Use only named routes and limits in the signed scope; no brute force or broad fuzzing |
| Validating a discovered token, key, or certificate against a service | No | Yes and explicit credential authorization | A candidate secret may belong to another owner or environment; report it instead |

The campaign record says the aggressive phase is gated behind a signed scope letter and two test accounts and that the campaign never authenticated. Preserve that boundary. The preauthorization deliverable should be a package-analysis report, not a live vulnerability claim.

## 8. NO-TOOL GAPS

**No complete Flutter semantic decompiler.** Blutter can provide valuable AOT artifacts under documented architecture and Dart-version conditions, but obfuscation, unsupported architectures, optimization, and plugin boundaries can leave unknowns [8] [8]. No cited tool guarantees a source-level reconstruction of every Dart class or call path.

**No static proof of pinning enforcement.** NSC files and trust-manager patterns reveal intent and possible coverage, but custom native paths, WebView choices, library behavior, and unused code can change runtime results [21]. A static report must say "pinning indicator found" or "no indicator found," not "pinning is bypassed" or "pinning is enforced," unless the authorized runtime test establishes that claim.

**No universal secret validity oracle.** Static scanners identify patterns. They do not prove that a string is live, scoped to MUJ, permitted for use, or still valid. TruffleHog's verification features can invoke external provider behavior [10], which is inappropriate for a preauthorization target report unless separately approved.

**No automatic exploitability conclusion for exported components.** The manifest can show declaration and filters, but exploitability depends on permissions, runtime guards, input handling, authentication state, and platform version. OWASP explicitly separates static manifest inspection from optional device confirmation [16].

**No automatic route-to-server authorization proof.** A path or method in Dart AOT may be dead code, used only in a different build flavor, protected by client state, or rejected by the server. [Inference] The supplied 13-route list should be correlated statically first and tested only under the signed scope.

**No single coverage score across representations.** A clean MobSF, JADX, or APKLeaks result can coexist with unresolved native or AOT evidence. The tools have different inputs and outputs, so a dashboard score cannot be treated as package-wide assurance.

**No automatic distinction between public configuration and secret material.** Cloud project identifiers, public API keys, certificate hashes, and endpoints can be intentionally distributed, while bearer tokens and private keys are sensitive. Human review and owner confirmation remain necessary.

**No static proof of the server observations from the APK.** The supplied IIS, MVC, .NET, Azure, identity, HSTS, TLS, error, method-policy, antiforgery, and `enc` observations belong to the portal campaign record. APK strings may explain how the client forms a request, but they cannot independently prove the server's response behavior.

## 9. BUILD CANDIDATES

| Candidate | Build objective | Minimum design | Safe implementation boundary | Success evidence |
|---|---|---|---|---|
| Evidence intake pack | Make every run reproducible | Hashes, split and ABI inventory, signing data, tool versions, immutable original, normalized metadata JSON | Offline only | Same artifact reproduces the same inventory |
| Flutter AOT evidence extractor | Correlate Blutter output with SLCM route candidates | Parse `objs.txt`, `pp.txt`, assembly and strings; preserve offsets; tag architecture and Dart version | Offline only | Each candidate route links to an evidence file and offset |
| Route and secret correlation graph | Avoid treating isolated strings as findings | Nodes for route, host, method, header, crypto call, secret candidate, component, and build flavor; edges require evidence | Offline only | Reviewable graph with confidence and redaction state |
| Manifest and App Link linter | Detect reachability declarations consistently | Parse components, exported state, permissions, filters, schemes, hosts, paths, and association requirements | Offline manifest parsing; public association fetch only if separately approved | Machine-readable table plus human review queue |
| Pinning evidence pack | Detect all trust paths without claiming runtime proof | Rules for NSC, trust managers, hostname verifiers, WebView, certificate resources, and native TLS imports | Static rules offline; runtime module is scope-gated | Coverage map from each network client to trust evidence |
| Multi-scanner secret normalizer | Reduce false positives | Normalize MobSF, APKLeaks, Gitleaks, TruffleHog, detect-secrets, Semgrep, YARA, and ripgrep findings; redact values | Offline and no verification calls | Deduplicated JSON/SARIF with reviewer status |
| Native and AOT review bundle | Make low-level evidence accessible to a club | Preconfigured Ghidra project, Rizin scripts, string extraction, architecture labels, and Blutter compatibility check | Offline | Analyst can reproduce cross-references without target traffic |
| Authorization-aware runner | Prevent accidental live testing | Separate offline and live profiles; live profile requires scope file, target allowlist, test-account identifier, rate limits, and stop conditions | No live profile until owner approval | Audit log proves which gate was satisfied |
| Build-time prevention rules | Turn findings into remediation | CI checks for private keys, bearer tokens, unexpected hostnames, exported components, debug flags, and unapproved certificates | Run on club test packages and approved CI | Failing build with actionable evidence and exceptions |
| SBOM and license report | Track third-party risk | Extract package and plugin names, versions, licenses, native libraries, and source provenance | Offline package and source review | Human-readable and machine-readable inventory |

The best first build candidate is the evidence intake pack plus the AOT evidence extractor. It closes the actual campaign gap without introducing live traffic. The authorization-aware runner should be built before anyone automates runtime validation, so convenience cannot silently bypass the signed scope.

## 10. Synthesis

The tools differ along four dimensions: representation, automation, authority, and operational risk. MobSF, AppSweep, and NowSecure emphasize aggregation and workflow convenience; JADX, Apktool, apkanalyzer, and Androguard expose Android structure; Blutter and reFlutter address Flutter-specific obstacles; Ghidra and Rizin provide low-level native interpretation; and the secret scanners provide independent pattern and entropy perspectives. The trade-off is breadth versus explainability: the broadest tool is not necessarily the most authoritative for a particular artifact.

The first tension is between static completeness and execution risk. Offline decoding is broad, reproducible, and low interaction, but it cannot prove that an exported component accepts attacker-controlled input or that a pin is enforced. Runtime testing answers those questions more directly but requires scope, isolation, and in some cases the two test accounts. The campaign should not solve a static evidence gap by jumping straight to live requests.

The second tension is between Flutter obfuscation and the need for actionable source mapping. Flutter states that obfuscation renames symbols but does not encrypt resources or prevent reverse engineering [40]. Blutter can expose AOT-related outputs, but compatibility limits and obfuscation can still produce unknowns [8] [8]. Therefore, the right conclusion is a coverage statement: which ABI, library, and representation were analyzed, which strings were mapped, and which areas remain unresolved.

The third tension is between detection and proof. A secret scanner is sensitive to candidate material but cannot establish credential validity. A manifest scanner can show that an activity is exported but not that it is exploitable. A static pinning rule can show a public-key hash or trust-manager implementation but not the negotiated runtime result. This distinction is especially important for SLCM_APP because the supplied campaign has not authenticated and has not performed APK work.

The fourth tension is between public information and target-specific claims. Tool documentation is public and can support the playbook. The portal's measured facts are supplied campaign observations. SLCM_APP-specific conclusions require the APK itself. [Inference] Until that package is hashed and analyzed, the strongest defensible verdict is that the assessment is incomplete, not that the client is vulnerable or secure.

## VERDICT

**Overall confidence: HIGH in the methodology and authorization boundary; LOW in any SLCM_APP-specific security conclusion because the APK has not yet been statically analyzed.**

The campaign should mark mobile client static analysis as **OPEN - evidence not collected**, not as passed or failed. The immediate, preauthorization deliverable is an offline evidence bundle containing the artifact hash and provenance, all splits and ABIs, `apkanalyzer` output, Apktool and JADX representations, MobSF HTML/PDF/JSON, APKLeaks and independent secret-scan outputs, manifest/component and App Link tables, native inventory, and Blutter output where compatible. Each result must identify the representation and confidence.

The signed scope letter is required before installation, re-signing, patching, launching, proxying, deep-link or exported-component invocation, pinning validation, API-route testing, `enc` behavior testing, or any credential validation. The two test accounts are required for authenticated behavior and must be used only within their documented limits. No production secret, user record, or unapproved route should be touched.

The final target-specific verdict after static work should use one of these precise statements: "no candidate found in analyzed representations," "candidate found and unresolved," "static evidence corroborates embedded sensitive material," or "runtime behavior confirmed under signed scope." Until then, this report supports a safe and technically complete plan, not a claim about the security of MUJ SLCM.

## References

1. *gitleaks/LICENSE at master · gitleaks/gitleaks · GitHub*. https://github.com/gitleaks/gitleaks/blob/master/LICENSE
2. *GitHub - skylot/jadx: Dex to Java decompiler · GitHub*. https://github.com/skylot/jadx
3. *GitHub - iBotPeaches/Apktool: A tool for reverse engineering Android apk files · GitHub*. https://github.com/iBotPeaches/Apktool
4. *GitHub - MobSF/Mobile-Security-Framework-MobSF: Mobile Security Framework (MobSF) is an automated, all-in-one mobile application (Android/iOS/Windows) pen-testing, malware analysis and security assessment framework capable of performing static and dynamic analysis. · GitHub*. https://github.com/MobSF/Mobile-Security-Framework-MobSF
5. *trufflehog/LICENSE at main · trufflesecurity/trufflehog · GitHub*. https://github.com/trufflesecurity/trufflehog/blob/main/LICENSE
6. *GitHub - dwisiswant0/apkleaks: Scanning APK file for URIs, endpoints & secrets. · GitHub*. https://github.com/dwisiswant0/apkleaks
7. *GitHub - rednaga/APKiD: Android Application Identifier for Packers, Protectors, Obfuscators and Oddities - PEiD for Android · GitHub*. https://github.com/rednaga/APKiD
8. *GitHub - worawit/blutter: Flutter Mobile Application Reverse Engineering Tool · GitHub*. https://github.com/worawit/blutter
9. *MASTG-TECH-0156: Reverse Engineering Flutter Applications - OWASP Mobile Application Security*. https://mas.owasp.org/MASTG/techniques/android/MASTG-TECH-0156/
10. *GitHub - trufflesecurity/trufflehog: Find, verify, and analyze leaked credentials · GitHub*. https://github.com/trufflesecurity/trufflehog
11. *apkanalyzer  |  Android Studio  |  Android Developers*. https://developer.android.com/tools/apkanalyzer
12. *GitHub - androguard/androguard: Reverse engineering and pentesting for Android applications · GitHub*. https://github.com/androguard/androguard
13. *gitleaks/README.md at master · gitleaks/gitleaks · GitHub*. https://github.com/gitleaks/gitleaks/blob/master/README.md
14. *GitHub - Yelp/detect-secrets: An enterprise friendly way of detecting and preventing secrets in code. · GitHub*. https://github.com/Yelp/detect-secrets
15. *Welcome to Androguard’s documentation¶*. https://androguard.readthedocs.io/en/latest/
16. *MASTG-TECH-0160: Enumerating Activities - OWASP Mobile Application Security*. https://mas.owasp.org/MASTG/techniques/android/MASTG-TECH-0160/
17. *Mobile Application Security Testing | AppSweep*. https://www.guardsquare.com/appsweep-mobile-application-security-testing
18. *Quark-Engine Book*. https://quark-engine.readthedocs.io/
19. *android:exported  |  Security  |  Android Developers*. https://developer.android.com/privacy-and-security/risks/android-exported
20. *MASTG-TECH-0014: Static Analysis on Android - OWASP Mobile Application Security*. https://mas.owasp.org/MASTG/techniques/android/MASTG-TECH-0014/
21. *MASTG-KNOW-0015: Certificate Pinning - OWASP Mobile Application Security*. https://mas.owasp.org/MASTG/knowledge/android/MASVS-NETWORK/MASTG-KNOW-0015/
22. *Network security configuration  |  Security  |  Android Developers*. https://developer.android.com/privacy-and-security/security-config
23. *GitHub - linkedin/qark: Tool to look for several security related Android application vulnerabilities · GitHub*. https://github.com/linkedin/qark
24. *Add Intent filters for App Links  |  App architecture  |  Android Developers*. https://developer.android.com/training/app-links/add-applinks
25. *Intents and intent filters  |  App architecture  |  Android Developers*. https://developer.android.com/guide/components/intents-filters
26. *GitHub - cryptax/droidlysis: Property extractor for Android apps · GitHub*. https://github.com/cryptax/droidlysis
27. *MobSF - Advanced Mobile Security Framework*. https://mobsf.org/
28. *GitHub - NationalSecurityAgency/ghidra: Ghidra is a software reverse engineering (SRE) framework · GitHub*. https://github.com/NationalSecurityAgency/ghidra
29. *GitHub - rizinorg/rizin: UNIX-like reverse engineering framework and command-line toolset. · GitHub*. https://github.com/rizinorg/rizin
30. *GitHub - semgrep/semgrep: Lightweight static analysis for many languages. Find bug variants with patterns that look like source code. · GitHub*. https://github.com/semgrep/semgrep
31. *semgrep/LICENSE at develop · semgrep/semgrep · GitHub*. https://github.com/semgrep/semgrep/blob/develop/LICENSE
32. *GitHub - VirusTotal/yara: The pattern matching swiss knife · GitHub*. https://github.com/VirusTotal/yara
33. *GitHub - BurntSushi/ripgrep: ripgrep recursively searches directories for a regex pattern while respecting your gitignore · GitHub*. https://github.com/BurntSushi/ripgrep
34. *reflutter · PyPI*. https://pypi.org/project/reflutter/
35. *Meet us at Black Hat 2026*. https://www.nowsecure.com/solutions/by-need/mobile-app-security-testing/
36. *Quark Report*. https://quark-engine.readthedocs.io/en/v26.1.1/quark_reports.html
37. *GitHub - Guardsquare/appsweep-action: GitHub action for AppSweep can be used to continuously integrate app scanning using AppSweep into your Android app build process · GitHub*. https://github.com/Guardsquare/appsweep-action
38. *reFlutter/README.md at main · Impact-I/reFlutter · GitHub*. https://github.com/Impact-I/reFlutter/blob/main/README.md
39. *Security with network protocols  |  Android Developers*. https://developer.android.com/privacy-and-security/security-ssl
40. *Obfuscate Dart code*. https://docs.flutter.dev/deployment/obfuscate
41. *Build and release an Android app*. https://docs.flutter.dev/deployment/android
42. *trufflehog command - github.com/trufflesecurity/trufflehog/v3 - Go Packages*. https://pkg.go.dev/github.com/trufflesecurity/trufflehog/v3
