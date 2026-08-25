# Digest: w2b-04-rms.md

## REPORT
Source: w2b-04-rms.md (research status: MUJ SLCM and RMS)

## ANSWER SUMMARY
- rms.jaipur.manipal.edu publicly presents as a Research Data Management System, not a student examination-result system.
- Landing page shows research-performance announcements (April and May 2025), an MUJ IRINS link, username/password labels, a Chrome browser recommendation, and a footer crediting MSIS and ISD, MAHE.
- DNS maps the hostname to 202.131.155.153; the numeric host served the same research-announcement content.
- The main Manipal RMS site (rms.manipal.edu) covers login access, publication, APC, conference-entry, grants, seed money, and open-access queries, and says RMS uses the same credentials as the Outlook account.
- No public result PDF format, marks data, or result-fetching JavaScript endpoint was established; the SLCM page exposes only sign-in and parent-login labels.
- RMS-to-SLCM marks relationship is not documented; no source says RMS stores or publishes student marks.
- Note: file is a status report from a mid-research pass; it lists unanswered questions and safe next steps rather than a full verdict table.

## KEY FACTS
- https://rms.jaipur.manipal.edu/ - RMS landing; Research Data Management System title, research announcements, IRINS link.
- https://202.131.155.153/ - numeric host; same research-performance announcement type of content.
- https://rms.jaipur.manipal.edu/Login.aspx - public Login.aspx path; visible content repeats announcements, no result index.
- https://rms.manipal.edu/ - main RMS; publication, APC, conference, grants, open-access research administration functions, Outlook-credential guidance.
- https://mujslcm.jaipur.manipal.edu/ - SLCM entry; MUJ portal sign-in and parent-login option.
- https://mujslcm.jaipur.manipal.edu/Home/Index - indexed SLCM home path with "Manipal University" and "Forgot Password?".
- https://jaipur.manipal.edu/examination.php - official examination page; continuous assessment via participation, assignments, lab work, class tests, in-semester tests.
- https://dns.google/resolve?name=rms.jaipur.manipal.edu&type=A - public DNS answer 202.131.155.153.
- http://web.archive.org/cdx/search/cdx?collapse=urlkey&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&output=json&url=mujslcm.jaipur.manipal.edu/* - archived SLCM URL inventory for historical asset review.
- http://jaipur.manipal.edu/research.php - MUJ Directorate of Research page; broader research context.

## ACTIONABLE LEADS
- Review the Wayback CDX inventory of mujslcm paths for explicitly named result, grade, or marks paths.
- Compare server-returned public HTML of the RMS and SLCM landing pages in a passive pass.
- Search MUJ's own site for "grade card", "marksheet", "semester result", "result declaration", "examination result".
- Verify whether any candidate "result" PDF belongs to RMS, admissions, or another Manipal service before use.
- Keep the RMS word in quotes and always qualify it as research administration in club material.

## FLAGS
- RMS acronym conflation risk: Research Data Management System vs a guessed Result Management System.
- No indexed RMS result PDF is a bounded negative finding, not proof of absence.
- Supplied stack claims (ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai, M365 identity) unverified for this host.
- Historic crawlable assets do not prove application routes or data fetching.
- Status-report format leaves some claims open; treat all as unverified.

## COVERAGE
Chars read: 11,445. EOF confirmed: true.