# MUJ SLCM File Upload Risk and Defensive Priorities

## Executive Summary

- **Evidence Boundary**: MUJ's official SLCM FAQ confirms the portal URL, SLCM registration, mandatory-document questions, and credentials tied to an official Outlook identity, but it does not expose an authenticated upload page or document an upload endpoint [7]. -> Treat specific fee-proof, avatar, storage, and download-route claims as unverified until MUJ's owner validates them internally.

- **Document-Risk Concentration**: MUJ's orientation page lists marksheets, certificates, a passport photograph, Aadhaar, APAAR ID, affidavits, and a medical certificate for reporting and verification [11]. -> If any portion is uploaded, this workflow deserves the highest privacy, authorization, retention, and malware-control priority.

- **Comparative SLCM Evidence**: A third-party mirror of a December 2019 SLCM manual describes mandatory JPEG/PDF uploads of up to 2 MB, view/delete/re-upload functions, a general Files area, and a JPEG profile-picture upload of up to 250 KB [30]. -> Use these as SLCM-class assessment hypotheses, not proof of MUJ's current authenticated interface.

- **Filtering Is Not One Check**: OWASP says the declared `Content-Type` is user-provided and trivially spoofed, and that file-signature checks are also insufficient by themselves [12]. -> Decode the name once, apply a narrow extension allowlist, identify and parse the actual format, re-encode supported media, and scan or disarm content before release.

- **Filename Trust Is the Critical Boundary**: In classic ASP.NET, `HttpPostedFileBase.FileName` can contain the client's fully qualified path, while `SaveAs` accepts the destination filename supplied by application code [5][3]. -> Never combine the client filename with a storage root; generate an opaque server-side identifier and retain the display name only as escaped metadata.

- **Downloads Can Reintroduce Upload Risk**: RFC 6266 says a received filename is advisory, folder information should be discarded, and special names such as `.` and `..` should be ignored or replaced [26]. -> Resolve downloads as `authorized record ID -> server-controlled storage key`, not `request parameter -> filesystem path`.

- **Trusted Portals Can Deliver Untrusted Content**: RFC 7578 warns that multipart uploads may contain arbitrary executable content, while MIME confusion can cause a browser to interpret an apparent image as HTML and execute script [10][23]. -> Quarantine first, scan and transform second, then deliver from an isolated origin with attachment and no-sniff headers.

- **No Public Vulnerability Is Established**: The public evidence supports a high-value document workflow and relevant SLCM-class features, but it does not demonstrate a bypass, traversal flaw, malware exposure, or unauthorized data access at MUJ. -> The correct outcome is a prioritized, owner-authorized internal review, not public probing or a claim that MUJ is vulnerable.

## Scope, Safety Boundary, and Evidence Grades

This is a passive, public-information risk assessment. It does not log in, enumerate hidden routes, upload files, alter requests, test credentials, or attempt to access another person's records. The test plan below is intended only for a staging environment or an explicitly authorized MUJ assessment. No endpoint names, storage paths, or exploit payloads are invented.

The requested technology profile also needs an evidence boundary. Microsoft currently publishes `Microsoft.AspNet.Mvc` **5.3.0**, targeting .NET Framework 4.5 and compatible with higher Framework versions [28]. Microsoft lists MVC 5.x as supported and describes ASP.NET MVC as an external NuGet/Visual Studio component [32]. Those facts show that the supplied MVC 5.3/.NET 4.x combination is technically plausible; they do not prove which package is deployed on MUJ. Likewise, MUJ's FAQ refers to an "official outlook ID" [7], which is consistent with the supplied Microsoft 365 identity description but does not independently establish the tenant configuration.

| Evidence grade | Meaning in this report | Examples |
|---|---|---|
| **Confirmed public MUJ fact** | Stated on a first-party MUJ page or document | SLCM URL; Outlook-linked credentials; mandatory-document question; physical verification list [7][11] |
| **Comparative SLCM evidence** | Described in a public, third-party-hosted SLCM manual, but not verified for current MUJ | Mandatory document upload, general Files area, profile-picture upload [30] |
| **Assessment input, unverified** | Supplied in the question but not established by the retrieved first-party pages | IIS 10, Akamai, exact deployed MVC/.NET version, Microsoft 365 tenant details |
| **Explicit inference** | A defensible hypothesis derived from a workflow, clearly labeled and requiring owner validation | Staff must retrieve a file if a digital verification upload exists |

Analytic rationale is presented through these evidence grades, explicit inference labels, comparison tables, and decision criteria rather than private chain-of-thought.

## MUJ's Confirmed Workflow Versus Unverified Upload Claims

MUJ's FAQ identifies itself as "Frequently Asked Questions and Contacts for SLCM Registration" and gives `https://mujslcm.jaipur.manipal.edu/` as the registration link [7]. It includes the question, "If I don't have any mandatory documents," but directs the student to Admissions rather than describing a file picker, extension rule, or upload route [7]. The same FAQ says admission details can be changed only by Admissions after verification [7]. This establishes an administrative verification workflow, not a publicly proven digital-upload implementation.

MUJ's orientation material provides the stronger data-classification signal. It says document verification begins at a specified reporting time and lists the records students must submit [11]. The list explains why this workflow should be treated as more sensitive than a generic image-sharing feature.

| MUJ document group | Publicly listed records | Security significance |
|---|---|---|
| Academic identity | Class X and XII marksheets and passing certificates; UG marksheet and passing certificate for postgraduate programs; entrance-exam scorecard [11] | Academic records require strict student-to-record authorization and auditability. |
| Enrollment status | Transfer or school-leaving certificate; migration certificate; provisional admission order [11] | Replacement, deletion, or cross-account exposure could disrupt enrollment decisions. |
| Personal identity | Passport-size photograph; Aadhaar Card; APAAR ID [11] | These records increase privacy and impersonation impact if misdelivered. |
| Declarations and health | NRI sponsor affidavit where applicable; anti-drug and anti-ragging affidavits; medical fitness certificate; gap certificate where required [11] | Some records can contain signatures, health information, and family or sponsor data. |

The public landing page itself exposes only a welcome/sign-in presentation in the extracted content [4]. Neither that page nor the FAQ proves the existence of a fee-proof upload, avatar editor, attachment API, storage bucket, or download controller. Absence from the public page does not prove absence behind authentication; it means those features must remain **unverified** in an OSINT report.

### Comparative case study: the 2019 SLCM manual

A third-party mirror, uploaded by a named user and dated December 2019, describes a related SLCM registration process [30]. It says students must upload mandatory documents, identifies "Documents Upload" as one of four registration steps, and limits scanned copies to JPEG or PDF with each file no larger than 2 MB [30]. It also describes viewing, deleting, re-uploading, and finally submitting documents [30].

The same manual describes a Files section for documents beyond the mandatory set and a profile-picture workflow limited to JPEG and 250 KB [30]. This is useful comparative evidence because it reveals likely SLCM business objects: a document type, a stored file, a view operation, a delete operation, and a final submission state. It remains lower-confidence evidence for MUJ because it is not a current MUJ-authenticated page. In particular, it does not confirm a fee-proof workflow.

**Decision-ready insight:** MUJ's document-verification process is confirmed, while the digital surfaces are only partly evidenced. The owner should begin with an authenticated feature inventory rather than assuming that routes from an older SLCM manual still exist.

## SLCM-Class Upload Surface Map

"Path" below means a business workflow, not a guessed URL. No hidden MUJ endpoint should be requested without written authorization.

| Candidate surface | Public basis | Likely operations | MUJ status | Assessment priority |
|---|---|---|---|---|
| Registration document upload | Comparative manual describes document type selection, file choice, upload, view, delete, re-upload, and submit [30] | Create, preview, replace, delete, finalize | **Inference for current MUJ** | Critical if identity documents are digital |
| General profile Files area | Comparative manual describes uploading non-mandatory files and viewing existing files [30] | Create, list, view, delete | **Inference for current MUJ** | High because accepted types may be broader |
| Profile photograph or avatar | MUJ requires a passport photograph for reporting; comparative manual describes JPEG profile-picture upload [11][30] | Upload, crop/transform, retrieve | **Inference for digital MUJ feature** | High for image-parser and browser-delivery controls |
| Fee proof or transaction attachment | Included in the requested focus, but no retrieved first-party MUJ page or comparative manual passage confirms it | Upload, review, approve/reject, retain | **Unverified** | High if present because payment fraud and privacy intersect |
| Staff verification and download | **Inference:** digital verification requires an authorized reviewer to retrieve or render the submitted record | List, preview, download, decision | **Logical dependency, not observed** | Critical for IDOR and traversal testing |
| Support, appeal, or correction attachment | Common portal design hypothesis; not established by the retrieved MUJ sources | Upload, ticket association, staff download | **Low-confidence inference** | Medium until inventory confirms it |
| Bulk administrative import | Generic lifecycle-system hypothesis; not publicly established for MUJ | Archive/spreadsheet import, validation, error report | **Low-confidence inference** | High if archives or spreadsheets are accepted |

The most important hidden dependency is the reviewer side. A secure upload handler can still be undermined by an unsafe previewer, download controller, office-document converter, image library, or administrative bulk processor. Therefore, inventory must follow each file from intake to every subsequent consumer, not stop at the student's form.

## Five Failure Modes Across the File Lifecycle

### 1. Extension and `Content-Type` gaps create false confidence

OWASP recommends defense in depth because no single file-validation technique is sufficient [12]. The declared `Content-Type` is supplied by the user and is trivial to spoof; it is useful only as an early consistency check [12]. A magic-byte or signature check is stronger, but OWASP also warns that it is commonly bypassed when used alone [12].

The defensive sequence should be:

| Validation stage | Required decision | Failure action |
|---|---|---|
| Name normalization | Decode once; reject control characters, separator characters, ambiguous trailing characters, reserved names, and names exceeding the business limit | Reject before storage |
| Extension allowlist | Permit only formats needed by that exact document type, such as a constrained PDF or raster-image set | Reject unsupported formats |
| Declared media type | Compare the submitted media type with the expected format, but never treat it as authoritative [12] | Record mismatch and reject |
| Signature identification | Check that bytes resemble the expected format, while recognizing that this is not a complete verdict [12] | Reject mismatch |
| Safe parsing | Fully decode with a patched, resource-limited parser; reject malformed, encrypted, or unsupported constructs according to policy | Quarantine or reject |
| Transformation | Re-encode raster images; apply CDR to supported PDF/DOCX workflows where business requirements permit [12] | Release only transformed output |
| Malware analysis | Scan in quarantine and define fail-closed behavior when the scanner is unavailable [12] | Do not publish until clean |

For an avatar, successful image decoding and server-side re-encoding should produce a fresh raster rather than retaining arbitrary metadata or active formats. For verification documents, accepting "PDF" as an extension should not mean accepting every feature a PDF can contain. For Office-like ZIP containers, both the outer package and embedded objects need policy decisions.

### 2. Classic ASP.NET metadata can become a filesystem primitive

Microsoft documents `HttpPostedFileBase.FileName` as the fully qualified name on the client, including a directory path [5]. Microsoft documents `ContentType` simply as the MIME content type of the uploaded file [14], while OWASP supplies the missing trust warning: that value is user-controlled [12]. `SaveAs(string filename)` writes the upload to the destination name chosen by application code [3].

The dangerous design is conceptual rather than framework-specific: accepting a display name, concatenating it with a directory, and passing that result into `SaveAs`, `File.Open`, `File.Delete`, or a download response. The safer model is to generate a random storage identifier, store the original name only as metadata, and make the storage key unreachable from the request. CISA specifically recommends random identifiers with associated metadata stored separately rather than using user input to name files [24].

Size controls also need coordination. Classic ASP.NET documents a default maximum request of **4 MB**, with uploads larger than **256 KB** buffered to disk by default [13]. The `HttpRuntimeSection.MaxRequestLength` value is measured in kilobytes and defaults to 4096 KB [27]. IIS `maxAllowedContentLength` is measured in bytes and defaults to **30,000,000 bytes**, approximately 28.6 MB [6]. A configuration that changes only one layer can produce inconsistent rejection, unexpected disk buffering, or poor error handling.

### 3. Filename traversal can reappear during view, delete, and download

RFC 7578 tells form receivers not to use a submitted filename blindly, not to use directory information that may be present, and not to overwrite unintended files [10]. RFC 6266 makes the corresponding download-side point: filenames are advisory, path components should be stripped, and special filesystem names should be ignored or replaced [26].

A secure download design therefore uses an opaque file-record ID. The controller authorizes that record against the authenticated student, parent, staff member, program, and workflow state. Only then does server-side metadata yield a storage key. The response filename is separately sanitized for `Content-Disposition`; it never controls the file opened. The same pattern must cover preview, delete, replace, conversion, and administrator export.

Canonicalization alone is not enough if an attacker can change links or directory entries between checking and opening. Where local storage is unavoidable, the implementation should avoid shared writable directories, symbolic-link following, and separate check-then-use path operations. Prefer an object store or a storage service that opens a server-selected object directly.

### 4. Malware and active content can turn the portal into a distribution channel

RFC 7578 states that files submitted through multipart form data may contain arbitrary executable content [10]. The MIME Sniffing Standard describes the browser-side consequence: if the server considers an upload an image but the browser interprets it as HTML, attacker-controlled script may steal credentials or mount cross-site scripting attacks [23].

OWASP recommends generated filenames, storage on another server or outside the web root, least-privilege permissions, antivirus or sandbox analysis, and CDR for applicable types such as PDF and DOCX [12]. Its unrestricted-upload guidance also recommends `Content-Disposition: attachment` and `X-Content-Type-Options: nosniff` for static-file responses [15]. These controls are complementary:

| Control | Primary purpose | Important limitation |
|---|---|---|
| Quarantine | Prevent unreviewed content from becoming downloadable | Requires a clear state machine and cleanup process |
| Antivirus | Detect known or suspicious malware | A clean result is not proof that a file is harmless |
| CDR or re-encoding | Remove unsupported active features and rebuild known-safe output | May alter signatures, accessibility features, or document fidelity |
| Isolated content origin | Limit uploaded content's access to portal cookies and same-origin APIs | Must be genuinely separate and should not share authentication cookies |
| Attachment plus `nosniff` | Reduce unintended inline execution and MIME reinterpretation [15] | Does not replace safe content validation |
| Authorization on every retrieval | Prevent one student from fetching another's file | Must cover previews, thumbnails, transformed copies, and exports |

For high-value verification records, the defensible default is private storage and authenticated download, not public object URLs. If a cloud object store is used, any signed URL should be short-lived, scoped to one object and operation, and issued only after application-level authorization.

### 5. Archives, resource exhaustion, and state transitions expand the attack surface

Python's ZIP documentation warns that some ZIP APIs leave filename sanitization to the caller and specifically identifies absolute names and dot-dot components as traversal risks [16]. Its TAR documentation goes further: archives can overwrite files through absolute paths, dot-dot components, or links; built-in filters do not eliminate every danger or denial-of-service condition [17]. These warnings describe format-level hazards that apply regardless of whether the portal is written in Python or .NET.

An SLCM portal should avoid archives unless the business case is compelling. If accepted, extraction needs an isolated temporary directory, limits on entry count, total expanded bytes, nesting depth, individual-file size, filename length, CPU time, and memory. Links, devices, duplicate paths, encrypted entries, and entries outside the permitted format set should be rejected. Each extracted item then re-enters the full validation and malware pipeline as a new file.

State handling matters too. An upload should move through explicit states such as `received`, `quarantined`, `validated`, `scan-passed`, `released`, `rejected`, and `deleted`. A scanner timeout must not accidentally promote a file. A replacement should create a new version and audit event rather than silently overwriting the previous object.

## Two Path-Handling Case Studies

### GitLab 16.0.0: attachment traversal became a critical unauthenticated read

GitLab reported that CE/EE **16.0.0** contained a path-traversal issue under a specific condition: an attachment existed in a public project nested within at least five groups [18]. An unauthenticated user could then read arbitrary server files. GitLab rated the issue **CVSS 10.0** and released 16.0.1 on May 23, 2023 [18].

The lesson is not that MUJ shares GitLab's code. It is that attachment identity, nested routing, and path normalization can interact in a mature application and bypass an otherwise sensible authorization model. For SLCM, regression tests should cover nested organizational structures, renamed records, legacy attachments, alternate routes, and transformed copies.

### Apache HTTP Server 2.4.49: normalization failure crossed configuration boundaries

NVD records that Apache HTTP Server **2.4.49** introduced a flaw in path normalization that could map URLs to files outside directories configured through Alias-like directives [22]. Requests could succeed where files outside those directories were not protected by the normal `require all denied` configuration, and CGI-enabled configurations could escalate the issue to remote code execution [22].

Again, this is not evidence that MUJ is affected. It demonstrates that path safety depends on both application normalization and web-server configuration. An application-level allowlist cannot compensate for executable upload directories, permissive aliases, or a download route that delegates user input to the filesystem.

## ASP.NET MVC and IIS Defensive Reference Architecture

The supplied ASP.NET MVC 5.3 description is plausible because Microsoft's package page lists version 5.3.0 for .NET Framework 4.5 or higher [28]. Deployment-specific findings still require an owner-provided software inventory. The following architecture applies if the supplied stack is accurate and remains broadly suitable if some components differ.

```text
Student or staff browser
        |
        v
CDN/WAF edge (if actually deployed)
        |
        v
IIS request-size and method controls
        |
        v
MVC authentication + authorization + anti-CSRF
        |
        v
Upload intake -> generated object ID -> private quarantine
        |                                  |
        |                                  v
        |                         type parser / re-encoder
        |                                  |
        |                                  v
        |                         AV / sandbox / CDR
        |                                  |
        v                                  v
Metadata database <------------ release decision
        |
        v
Authorized download service -> isolated delivery origin
```

ASP.NET's anti-CSRF pattern sends a session-bound token in a cookie and a second token in a hidden form value, then validates the submitted form token against the session token [31]. The page names `HtmlHelper.AntiForgeryToken` and `ValidateAntiForgeryTokenAttribute` [31]. Every state-changing upload, replacement, deletion, and final-submit action should use equivalent protection.

| Layer | Required responsibility | What it must not be trusted to do alone |
|---|---|---|
| CDN/WAF, if present | Coarse request limits, abuse throttling, bot and reputation controls | Determine whether a file is semantically safe |
| IIS | Enforce request size, disable execution in upload locations, restrict verbs and handlers | Authorize a student to a document |
| MVC controller | Authenticate, authorize, validate anti-CSRF, enforce workflow state, create opaque record ID | Parse every complex file format in-process |
| Validation worker | Identify format, parse within limits, re-encode or apply CDR | Grant business authorization |
| Malware service | Scan quarantined objects and return a recorded verdict | Serve content directly or bypass parser policy |
| Metadata database | Bind owner, document type, original display name, storage key, hash, state, retention, scanner versions, and audit history | Store a client-controlled filesystem path |
| Private object storage | Prevent execution, listing, and public access by default | Decide which portal user may download an object |
| Download controller | Re-authorize every request, select server-side object, set safe response headers | Accept a raw path from the URL or display name |

A CDN, Akamai property, or Microsoft identity provider does not validate bytes after authentication. Strong identity answers "who is requesting"; upload security separately answers "what bytes are being accepted, where do they go, and who can retrieve them." This separation is one of the most important design principles for the portal.

## Authorized Validation Matrix

The following tests should use synthetic accounts, inert files, and canary records in staging or an owner-approved test tenant. Do not use real student identity documents, live malware, production credentials, traversal toward real server files, or cross-account access without explicit written authorization.

| Test area | Safe authorized test | Secure expected result |
|---|---|---|
| Feature inventory | Record each student, parent, staff, and administrator file action using owner-provided accounts | Every upload, preview, download, replace, delete, export, and conversion path is documented |
| Extension mismatch | Submit an inert file whose extension disagrees with its identified format | Rejected before release; reason logged without reflecting unsafe names |
| Declared MIME mismatch | Change only the declared type of an inert sample | Server identifies content independently and rejects inconsistency [12] |
| Ambiguous filename | Use benign names containing multiple suffixes, unusual whitespace, or Unicode confusables | Name rejected or replaced; generated storage ID unaffected |
| Image transformation | Upload a valid test image containing nonessential metadata | Released copy is a newly encoded raster with policy-compliant dimensions and metadata |
| PDF policy | Exercise benign PDFs with unsupported active or embedded features | Unsupported features are rejected or removed through approved CDR policy |
| Request-size boundary | Test just below, at, and above each documented business limit | IIS and ASP.NET limits are aligned; no partial object remains [6][27] |
| Archive budget | Use a harmless archive designed to exceed entry-count or expansion quotas | Extraction stops safely; temporary data is removed; no object is released |
| Duplicate and replacement | Upload two files with the same display name and replace one concurrently | Unique storage IDs, deterministic versioning, and complete audit events |
| Ownership authorization | Ask the owner to test one synthetic student's opaque file ID under another synthetic account | Denied on list, preview, download, thumbnail, delete, and export routes |
| Role authorization | Compare student, parent, verifier, finance, and administrator permissions defined by MUJ | Least privilege; no role inherits unrelated document access |
| Download headers | Retrieve each allowed type using a test account | Correct `Content-Type`, attachment where appropriate, `nosniff`, safe disposition name, and no portal cookies on an isolated origin [15] |
| Scanner outage | Disable the test scanner through an approved fault-injection mechanism | File remains quarantined; no fail-open release |
| CSRF | Use the approved test harness to omit or invalidate the anti-CSRF token | Upload, replace, delete, and submit actions fail [31] |
| Logging and privacy | Review test audit events and application logs | Object ID, actor, action, result, and correlation ID recorded; file contents and sensitive identity values excluded |
| Retention and deletion | Expire a synthetic record and exercise legal-hold behavior | Primary object, derivatives, cache entries, and search indexes follow the documented retention decision |

**Decision-ready insight:** A pass requires consistency across upload, processing, and every retrieval route. Testing only the initial file picker would miss the highest-impact authorization and path-handling failures.

## Prioritized Remediation Roadmap

| Priority | Action | Owner | Acceptance criterion |
|---|---|---|---|
| **P0: Before new upload exposure** | Generate storage IDs; keep all objects private and non-executable; remove raw path parameters; require authentication, authorization, and anti-CSRF; establish quarantine [12] | Application and platform teams | No client name influences a filesystem/object key; no unscanned object is downloadable |
| **P0: Before new upload exposure** | Apply document-type-specific allowlists and aligned IIS/ASP.NET/business size limits [12][6] | Application security and engineering | Negative matrix passes at every parsing layer |
| **P0: Before new upload exposure** | Re-authorize list, preview, thumbnail, download, replace, delete, and export operations | Application owner | Cross-account and cross-role synthetic tests deny consistently |
| **P1: Next controlled release** | Add safe image re-encoding, PDF/Office policy, AV, optional sandbox/CDR, and scanner-outage fail-closed behavior [12] | Security engineering | Released object has recorded parser, transformation, hash, and scan verdicts |
| **P1: Next controlled release** | Serve from an isolated origin with safe disposition and no-sniff headers [15] | Web platform team | Uploaded bytes cannot access the main portal's cookies or same-origin APIs |
| **P1: Next controlled release** | Add quotas, archive expansion budgets, parser timeouts, and temporary-file cleanup [17] | Platform and SRE teams | Resource-limit tests terminate predictably without residual data |
| **P2: Continuous assurance** | Centralize file-policy code, add regression tests, patch parsers/frameworks, rescan retained objects after intelligence updates, and rehearse malicious-file response | Engineering, SOC, and governance | Policy and telemetry cover every file consumer and derivative |
| **P2: Governance** | Define retention by document type, deletion propagation, reviewer access, exception approval, and student notification | Registrar, privacy, legal, and security | Each data class has an owner, purpose, retention period, and review cadence |

The roadmap deliberately separates containment from enhancement. CDR and sandboxing are valuable, but they cannot rescue a design that stores objects under attacker-influenced paths or allows cross-account retrieval.

## Synthesis

| Evidence or strategy | Mechanism | Scope | Main trade-off | Time horizon |
|---|---|---|---|---|
| MUJ public workflow | Mandatory documents and physical verification establish sensitive records and administrative decisions [11] | Confirmed process, not confirmed upload implementation | Strong relevance but limited technical visibility | Immediate inventory |
| 2019 comparative SLCM manual | Typed document upload, Files area, view/delete/re-upload, and profile-picture feature [30] | Related SLCM behavior, not current MUJ proof | Useful hypotheses can become false assumptions | Validate during owner-authorized discovery |
| OWASP defense in depth | Independent name, type, content, storage, scanning, authorization, and CSRF controls [12] | Entire file lifecycle | More processing and operational complexity | Architecture baseline |
| Opaque-ID download design | Business authorization selects server-controlled metadata and object key [12][24] | Upload, preview, download, replace, and delete | Display-name convenience must be separated from storage identity | P0 |
| GitLab case | Nested attachment routing interacted with traversal to permit unauthenticated arbitrary read [18] | Real-world application case | Shows rare route combinations can have critical impact | Regression testing |
| Apache case | Path-normalization defect crossed alias and CGI configuration boundaries [22] | Web-server and application boundary | Defense depends on both code and server configuration | Continuous hardening |

Several tensions are easy to miss. First, authenticated Microsoft identity does not make an uploaded file trustworthy. Identity reduces anonymity, but students, compromised accounts, mistaken uploads, and files acquired elsewhere can still introduce malicious or malformed content. Authorization and byte-level validation must remain independent.

Second, strict allowlists conflict with the diversity of university records. A permissive "documents" category is operationally easy but dangerous. The better approach is a narrow policy per business object: an avatar does not need the same formats as a marksheet, and a fee proof, if the feature exists, does not automatically require macro-enabled Office documents.

Third, the older manual's **2 MB** document limit and **250 KB** profile-picture limit are business constraints, while ASP.NET and IIS have separate transport defaults [30][6][27]. **Inference:** if current settings are similar, inconsistent limits could create confusing rejection or partial-processing behavior. MUJ should define one business limit per feature and configure every layer to enforce it predictably.

Fourth, preserving the student's original filename can help reviewers, but it should be metadata only. The object key, local path, cache key, and authorization decision should remain server-controlled. This reconciles usability with traversal resistance.

Finally, a CDN or WAF can reduce abuse at the edge but cannot safely parse every PDF, image, archive, or Office container, nor can it decide whether one student may retrieve another student's record. The decisive controls sit in the application, processing workers, metadata model, private storage, and download authorization service.

## VERDICT

**Verdict: High-priority internal review; no publicly demonstrated vulnerability.**

The evidence strongly supports that MUJ SLCM is connected to a sensitive registration and document-verification process [7][11]. Comparative SLCM documentation provides credible hypotheses for mandatory document uploads, a broader Files section, document retrieval and replacement, and JPEG profile images [30]. Primary standards and vendor guidance show why client filenames, declared content types, complex file formats, archive extraction, and download paths must be treated as hostile inputs [10][12][5][26].

**Confidence levels:**

| Finding | Confidence |
|---|---|
| MUJ has an SLCM registration and mandatory-document verification workflow | **High** |
| Current MUJ has some digital document-upload capability | **Medium-low**, because the public MUJ documents do not show it and the detailed upload evidence comes from an older third-party SLCM manual |
| Current MUJ has profile-picture upload | **Low to medium**, supported only as an SLCM-class comparison plus MUJ's passport-photo requirement |
| Current MUJ has a fee-proof upload | **Low / unverified** |
| Supplied MVC 5.3/.NET profile is technically plausible | **High** for plausibility, **low** for confirming MUJ's deployed version [28] |
| Supplied IIS 10, Akamai, and Microsoft 365 deployment details are exact and current | **Low / not independently confirmed** |
| Layered upload, quarantine, opaque-ID storage, strict retrieval authorization, and isolated delivery are appropriate controls | **High**, based on OWASP, IETF, CISA, Microsoft, and real-world cases |

The university security club should hand this report to MUJ's application owner and request a scoped, written-authorized staging assessment. It should not test the production portal, submit crafted files, enumerate authenticated routes, or attempt to retrieve any real student's data without explicit authorization.

## References

1. [
Google Online Security Blog: Securely Hosting User Data in Modern Web Applications
](https://security.googleblog.com/2023/04/securely-hosting-user-data-in-modern.html)
2. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
3. *HttpPostedFileBase.SaveAs(String) Method (System.Web) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.httppostedfilebase.saveas?view=netframework-4.8.1
4. *Manipal University*. https://muj.slcm.jaipur.manipal.edu/
5. *HttpPostedFileBase.FileName Property (System.Web) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.httppostedfilebase.filename?view=netframework-4.8.1
6. *Request Limits &lt;requestLimits&gt; | Microsoft Learn*. https://learn.microsoft.com/en-us/iis/configuration/system.webServer/security/requestFiltering/requestLimits/
7. *Faqs Slcm*. https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf
8. [
	MU SLcM
](https://slcm.manipal.edu/)
9. *Path.GetFileName Method (System.IO) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.io.path.getfilename?view=netframework-4.8.1
10. *RFC 7578: Returning Values from Forms: multipart/form-data | RFC Editor*. https://www.rfc-editor.org/rfc/rfc7578
11. *Orientation Program 2026 - Manipal University Jaipur - Manipal University Jaipur*. https://www.jaipur.manipal.edu/induction-orientation-program.php
12. *File Upload - OWASP Cheat Sheet Series*. https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
13. *HttpPostedFile Class (System.Web) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.httppostedfile?view=netframework-4.8.1
14. *HttpPostedFileBase.ContentType Property (System.Web) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.httppostedfilebase.contenttype?view=netframework-4.8.1
15. *Unrestricted File Upload | OWASP Foundation*. https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload
16. *http://docs.python.org/3/library/zipfile.html*. http://docs.python.org/3/library/zipfile.html
17. *http://docs.python.org/3/library/tarfile.html*. http://docs.python.org/3/library/tarfile.html
18. *GitLab Critical Security Release: 16.0.1 | GitLab Docs*. https://docs.gitlab.com/releases/patches/patch-release-gitlab-16-0-1-released/
19. [CWE -

    CWE-434: Unrestricted Upload of File with Dangerous Type (4.20)
    ](https://cwe.mitre.org/data/definitions/434.html)
20. [CWE -

    CWE-409: Improper Handling of Highly Compressed Data (Data Amplification) (4.20)
    ](https://cwe.mitre.org/data/definitions/409.html)
21. *http://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/10-Business_Logic_Testing/09-Test_Upload_of_Malicious_Files*. http://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/10-Business_Logic_Testing/09-Test_Upload_of_Malicious_Files
22. *NVD - cve-2021-41773*. https://nvd.nist.gov/vuln/detail/cve-2021-41773
23. *MIME Sniffing Standard*. https://mimesniff.spec.whatwg.org/
24. *http://cisa.gov/sites/default/files/2024-05/Secure_by_Design_Alert_Eliminating_Directory_Traversal_Vulnerabilities_in_Software_508c%20%283%29.pdf*. http://cisa.gov/sites/default/files/2024-05/Secure_by_Design_Alert_Eliminating_Directory_Traversal_Vulnerabilities_in_Software_508c%20%283%29.pdf
25. [CWE -

    CWE-22: Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') (4.20)
    ](https://cwe.mitre.org/data/definitions/22.html)
26. *RFC 6266: Use of the Content-Disposition Header Field in the Hypertext Transfer Protocol (HTTP) | RFC Editor*. https://www.rfc-editor.org/rfc/rfc6266
27. *HttpRuntimeSection.MaxRequestLength Property (System.Web.Configuration) | Microsoft Learn*. https://learn.microsoft.com/en-us/dotnet/api/system.web.configuration.httpruntimesection.maxrequestlength?view=netframework-4.8.1
28. [
        NuGet Gallery
        | Microsoft.AspNet.Mvc 5.3.0
    ](https://www.nuget.org/packages/Microsoft.AspNet.Mvc/)
29. *SLcM Portal Student Registration Guide | PDF | Tab (Gui) | Test (Assessment)*. https://www.scribd.com/document/368680860/User-Manual
30. [Slcm Mit Usermanual [x4e6zjd7v8n3]](https://idoc.pub/documents/slcm-mit-usermanual-x4e6zjd7v8n3)
31. *Anti CSRF Tokens ASP.NET | OWASP Foundation*. https://owasp.org/www-community/Anti_CRSF_Tokens_ASP-NET
32. *ASP.NET official support policy | .NET*. https://dotnet.microsoft.com/en-us/platform/support/policy/aspnet
