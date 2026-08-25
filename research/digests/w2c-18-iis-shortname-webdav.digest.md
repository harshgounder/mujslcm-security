# Digest: w2c-18-iis-shortname-webdav.md

## REPORT
Source: /home/liebert511/mujslcm-recon/research/w2c-18-iis-shortname-webdav.md

## ANSWER SUMMARY
- Public evidence confirms only the portal landing page with general, parent, and student sign-in paths.
- 8.3 short-name disclosure is a real IIS/NTFS risk class; MUJ affected status Unknown, not demonstrated.
- Mitigation is two-stage: stop new 8.3 creation and strip existing aliases via fsutil 8dot3name, with compatibility testing first.
- PUT 411 proves only message-framing enforcement, not WebDAV, write access, or file creation.
- OPTIONS/DELETE 404 is deliberately ambiguous under RFC 9110; cannot prove disablement.
- WebDAV requires an installed module plus per-URI inherited authoring rules; DAV header is per-resource.
- Edge attribution: externally observed status must be correlated with Akamai logs and IIS W3C logs before assigning a layer.
- Verdict: no confirmed IIS vulnerability; owner-authorized hardening review warranted.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/ : only target-specific verified fact.
- https://techcommunity.microsoft.com/blog/iis-support-blog/iis-short-name-enumeration/3951320 : tilde requests reveal 8.3 names, NtfsDisable8dot3NameCreation.
- https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/fsutil-8dot3name : query, scan, test, strip aliases; registry breakage warnings.
- https://brackish.io/2023/11/17/iis-short-file-name-enumeration : side channel works without directory listing.
- https://www.rfc-editor.org/rfc/rfc9110.html : 411 and 404 semantics, OPTIONS intermediary scope.
- https://www.rfc-editor.org/rfc/rfc4918.html : DAV header compliance classes per resource.
- https://learn.microsoft.com/en-us/iis/configuration/system.webserver/webdav/authoringrules : per-URI authoring rules, Read/Write/Source, inheritance.
- https://learn.microsoft.com/en-us/iis/publish/using-webdav/how-to-configure-webdav-with-request-filtering : applyToWebDAV treats WebDAV traffic differently.
- https://learn.microsoft.com/en-us/iis/configuration/system.webserver/security/requestfiltering/verbs : verb filtering gate.
- https://learn.microsoft.com/en-us/dotnet/api/system.web.configuration.httpruntimesection.enableversionheader?view=netframework-4.8.1 : X-AspNet-Version default true, disable for production.
- https://learn.microsoft.com/en-us/iis/configuration/system.webserver/httpprotocol/customheaders/ : X-Powered-By ASP.NET default header.
- https://learn.microsoft.com/en-us/iis/manage/configuring-security/ensure-security-isolation-for-web-sites : one pool per site, shared identity risk.
- https://learn.microsoft.com/en-us/iis/configuration/system.webServer/directoryBrowse/ : directory browsing default disabled.
- https://learn.microsoft.com/en-us/iis/configuration/system.applicationhost/sites/site/logfile/ : W3C fields for edge/origin correlation.
- https://techdocs.akamai.com/property-mgr/docs/behs : edge behaviors govern attribution decisions.

## ACTIONABLE LEADS
- Owner-side: installed IIS role services, effective webdav config, authoring rules, request filtering, handlers, app pools, NTFS 8.3 state.
- Correlate reported 411/404 with Akamai property logs and IIS sc-status, sc-substatus, Win32 status.
- Run fsutil 8dot3name query and compatibility scan before any alias cleanup; keep backups.
- Check X-Powered-By and X-AspNet-Version suppression at edge and origin.
- No 8.3 enumeration, no PUT/DELETE content tests on production; use non-production resources and disposable principals.

## FLAGS
- Report cautions MVC "5.3" label is unverified against official release pages (MVC 5.2 is the latest public release page found).
- Supplied verb observations (PUT 411, OPTIONS/DELETE 404) were not independently reproduced.
- Reference [9] login.microsoftonline.com federationmetadata URL appears in references but is not used in body claims; unverified.
- Akamai presence is requester-supplied; report found no target-specific proof.
- No target-specific 8.3 or WebDAV evidence exists in the report.

## COVERAGE
- Chars read: 41686. EOF confirmed via read_file truncated:false.