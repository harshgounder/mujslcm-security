# Digest: w2g-10-stackoverflow.md

## REPORT
Source file: w2g-10-stackoverflow.md. Stack Overflow exposure assessment for the MUJ SLCM ecosystem using the public Stack Exchange API (search/advanced, questions, answers endpoints) with literal-body validation. 28 references, all public API or question/answer pages.

## ANSWER SUMMARY
- Verdict: no direct MUJ SLCM Stack Overflow disclosure was verified in the inspected public corpus. Exact `mujslcm` search returned no question records; the hostname mujslcm.jaipur.manipal.edu appears in no retrieved title, body, image source, route, callback, or connection string.
- The two literal `slcm` matches are token collisions, not MUJ evidence: question 77021984 is a MongoDB/Mongoose aggregation question with identifiers getQCResultSLcmExcel and isSLCMQcInspection; question 53239398 is a MarkLogic error trace with a $slcm variable beside $slch and $slchr.
- Three verified Manipal ASP.NET questions: 17420085 (ASPX tabs, external image http://eduvark.com/images/Manipal-University-Application-Form.jpg, local jQuery asset paths), and 19374708 plus 19510663 (C#/ASP.NET SMTP samples with a Manipal-related Gmail sender and an "MCIS,Manipal" signature).
- SMTP sample artifacts: smtp.gmail.com, ports 587 (question 19374708) and 584 versus 587 (question 19510663), EnableSsl true, UseDefaultCredentials false, NetworkCredential construction, a connection string Data Source=BOPSERVER; Initial Catalog=Project, and a TrackingFaculty_det update keyed by FID.
- No web.config block, Microsoft 365 identity configuration, Akamai control, IIS setting, or target-host route appears in any inspected record; the supplied ASP.NET MVC 5.3 / .NET 4.x / IIS 10 / Akamai / M365 stack is not corroborated by Stack Overflow.
- The answer corpus (IDs 19375158, 19374980, 19515503, 19510816, plus 17420085 answers) adds only generic guidance: SmtpException classes, GridView iteration, async send helpers, jQuery UI and AjaxControlToolkit tabs. No answer adds a MUJ artifact.
- Confidence: High for classification of the inspected records; Moderate that the Manipal ASP.NET cluster is generic rather than MUJ-specific; Low for any global-absence claim about the public Internet, deleted posts, or private content.
- Recommended label: direct MUJ SLCM linkage not observed in inspected corpus; generic Manipal/.NET references verified; live-service impact not established.

## KEY FACTS
- https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q=mujslcm&site=stackoverflow&filter=withbody&pagesize=100 - zero literal matches; the strongest negative result in the report.
- https://stackoverflow.com/questions/17420085/creating-tabs-in-aspx-for-application-forms - ASPX tab question; only verified question with a Manipal-branded external image.
- https://stackoverflow.com/questions/19374708/exception-handling-while-send-a-mail-using-smtp-port - SMTP sample with Manipal sender, MCIS,Manipal signature, Gmail host, BOPSERVER connection string.
- https://stackoverflow.com/questions/19510663/try-catch-block-used-while-smtp-exception-need-to-display-an-error-message-in-th - repeated SMTP sample; port shown as 584 in question code and 587 in answer code.
- http://eduvark.com/images/Manipal-University-Application-Form.jpg - third-party illustrative image URL inside question 17420085; contextual, not MUJ-host evidence.
- https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q=slcm&site=stackoverflow&filter=withbody - returns the MongoDB (77021984) and MarkLogic (53239398) collisions.
- https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q=manipal&tagged=asp.net&site=stackoverflow&filter=withbody&pagesize=100 - the query that produced the three verified Manipal questions.
- https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q=manipal&tagged=asp.net-mvc&site=stackoverflow&filter=withbody&pagesize=100 - empty for the requested literal; no MVC-specific Manipal match.
- https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q=manipal&tagged=.net&site=stackoverflow&filter=withbody&pagesize=100 - no literal proper-name match after validation.
- https://api.stackexchange.com/2.3/questions/17420085;19374708;19510663;17353152?site=stackoverflow&filter=withbody - question-bodies endpoint for the candidate set (17353152 is the unrelated Node.js Twitter thread).
- https://api.stackexchange.com/2.3/questions/17420085;19374708;19510663;17353152/answers?order=desc&sort=votes&site=stackoverflow&filter=withbody&pagesize=100 - answer corpus; no target artifact added.
- https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q=manipal&tagged=iis&site=stackoverflow&filter=withbody&pagesize=100 - no literal match; no IIS evidence.
- https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q=manipal&tagged=web-config&site=stackoverflow&filter=withbody&pagesize=100 - no match; no web.config artifact anywhere in the inspected set.
- https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q=manipal&tagged=asp.net-identity&site=stackoverflow&filter=withbody&pagesize=100 - no match; no identity configuration evidence.
- http://www.asp.net/ajaxlibrary/ajaxcontroltoolkitsamplesite/tabs/tabs.aspx - ASP.NET AJAX sample link in a 17420085 answer; documentation URL, not an application endpoint.

## ACTIONABLE LEADS
- Preserve a reproducible evidence ledger per item: exact URL, query scope, retrieval date, question ID, answer IDs, matching literal, classification; record text-match confidence separately from ownership confidence.
- Code-hygiene review targets: the two SMTP posts (Gmail host, ports, NetworkCredential construction, BOPSERVER/Project connection string, TrackingFaculty_det/FID data flow). If an authorized owner identifies the source, check git history for committed secrets, rotate any real credentials, move SMTP settings to secret-backed config.
- Report the port discrepancy 584 versus 587 to the code owner as a configuration-verification cue; do not treat either public value as the live setting.
- Keep question 17420085 as a contextual reference only (image URL and local jQuery paths are client-side samples, not deployed routes).
- Education value: use the corpus as a secure-coding case study on overreading brand names; require two independent anchors (target-owned domain or organization name plus application/technology signal) before escalation.
- Owner notification path: contact through an authorized channel only; do not attempt SMTP authentication, database connection, or live probing.

## FLAGS
- Attribution is the open question: no inspected record proves the Manipal-related code belongs to MUJ SLCM; the two SMTP posts may be related, copied, or coincidental. The report calls this an inference boundary.
- Collision question IDs 77021984 and 53239398 appear without direct question URLs in the reference list; their evidence URL is the API search, so reproduction goes through the API, not a stable direct link.
- The Manipal-related Gmail address is deliberately redacted in the report prose; the full identifier exists only in the source posts. Do not reproduce it in downstream material.
- The 584 versus 587 port difference may be a transcription error, an answer correction, or an extraction artifact; the report explicitly refuses to treat it as a vulnerability.
- The Node.js question 17353152 (Twitter streaming with track:'manipal') is retained only as a search-control example and is not .NET evidence.
- Supplied stack claims stay uncorroborated: no MVC version, framework target, IIS setting, Akamai header, OAuth callback, or web.config section appears in the corpus.
- This report does not state its research run date (unlike w2g-09 and w2g-11); all negatives are corpus- and search-time-bound.

## COVERAGE
- File: w2g-10-stackoverflow.md.
- 244 lines total; 38,900 bytes on disk; 38,900 chars read.
- Method: read_file offset 1, limit 2000, single call.
- EOF confirmed: final call returned truncated: false, last content line 244 equals total_lines 244.