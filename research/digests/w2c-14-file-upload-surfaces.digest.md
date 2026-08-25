# Digest: w2c-14-file-upload-surfaces

## REPORT
Source file: w2c-14-file-upload-surfaces.md (327 lines, 39635 bytes). Upload risk assessment for MUJ SLCM based on public pages, a 2019 comparative manual, and OWASP/Microsoft/IETF guidance.

## ANSWER SUMMARY
- No public vulnerability is established; the MUJ FAQ confirms SLCM registration and mandatory-document questions but exposes no upload endpoint or route.
- Orientation page lists marksheets, certificates, passport photo, Aadhaar, APAAR ID, affidavits, and medical certificate; the workflow is the highest-privacy document set if any part is digitized.
- A third-party 2019 SLCM manual describes mandatory JPEG/PDF uploads up to 2 MB, view/delete/re-upload, a general Files area, and a JPEG profile picture up to 250 KB; comparative hypotheses only.
- Client filenames and declared Content-Type are untrusted: HttpPostedFileBase.FileName carries the client path, OWASP says Content-Type is spoofable; use opaque server IDs plus escaped display metadata.
- ASP.NET defaults: max request 4 MB (MaxRequestLength 4096 KB), 256 KB disk buffer threshold; IIS maxAllowedContentLength default 30,000,000 bytes; limits must be aligned per layer.
- Download side: RFC 6266 filenames are advisory; resolve as record ID to server key with re-authorization on every retrieval; serve with attachment and nosniff from an isolated origin.
- Verdict: high-priority authorized internal review; no demonstrated bypass, traversal, malware, or unauthorized access at MUJ.

## KEY FACTS
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf : SLCM FAQ; portal URL, Outlook-linked credentials, mandatory-document question, no upload route described.
- https://www.jaipur.manipal.edu/induction-orientation-program.php : mandatory document list with privacy and impersonation significance.
- https://idoc.pub/documents/slcm-mit-usermanual-x4e6zjd7v8n3 : 2019 comparative manual; 2 MB JPEG/PDF, Files area, 250 KB profile picture.
- https://mujslcm.jaipur.manipal.edu/Home/Index : public landing only; no upload surface visible.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.httppostedfilebase.filename?view=netframework-4.8.1 : FileName is the fully qualified client name including path.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.httppostedfilebase.saveas?view=netframework-4.8.1 : SaveAs writes to the application-chosen destination name.
- https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html : layered validation; Content-Type spoofing, signature limits, CDR, storage outside web root.
- https://learn.microsoft.com/en-us/iis/configuration/system.webServer/security/requestFiltering/requestLimits/ : IIS maxAllowedContentLength default around 28.6 MB.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.configuration.httpruntimesection.maxrequestlength?view=netframework-4.8.1 : HttpRuntime default 4096 KB, units in kilobytes.
- https://www.rfc-editor.org/rfc/rfc7578 : multipart forms may carry arbitrary executable content.
- https://www.rfc-editor.org/rfc/rfc6266 : received filename is advisory; discard path components and special names.
- https://mimesniff.spec.whatwg.org/ : image versus HTML misread can lead to script execution.
- https://docs.gitlab.com/releases/patches/patch-release-gitlab-16-0-1-released/ : GitLab 16.0.0 attachment traversal CVSS 10.0, unauthenticated arbitrary file read, fixed 16.0.1.
- https://nvd.nist.gov/vuln/detail/cve-2021-41773 : Apache 2.4.49 normalization flaw, RCE when CGI enabled.
- https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload : attachment content-disposition and nosniff for static file responses.

## ACTIONABLE LEADS
- Authorized staging feature inventory per role: upload, preview, download, replace, delete, export, and transformation paths.
- Negative matrix: extension and MIME mismatch, ambiguous names, image re-encode, PDF active-feature policy, request-size boundaries, archive entry and expansion budgets, cross-account opaque ID, role matrix, download headers, scanner outage fail-closed, CSRF, retention and legal hold.
- Quarantine, AV, sandbox/CDR pipeline with explicit state machine; isolated delivery origin without portal cookies.
- Align IIS, ASP.NET, and business size limits per document type; one business limit per feature.
- Governance: retention by document type, deletion propagation, reviewer access, exception approval.
- No production testing and no real student documents without written authorization.

## FLAGS
- 2019 manual is third-party, dated, and not current MUJ proof; current digital upload capability rated Medium-low.
- Fee-proof upload is unverified; no first-party MUJ page confirms it.
- MVC 5.3 is plausible via NuGet Microsoft.AspNet.Mvc 5.3.0, not proof of MUJ deployment.
- IIS 10, Akamai, and Microsoft 365 details not independently confirmed.
- GitLab and Apache cases are regression lessons, not evidence against MUJ.

## COVERAGE
Chars read: 39635 (full file to EOF, truncated false).