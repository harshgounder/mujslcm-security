# Digest: w2b-12-jaipur-main-site.md

## REPORT
Source file: w2b-12-jaipur-main-site.md (MUJ SLCM Public Surface and Defensive OSINT Report)

## ANSWER SUMMARY
- The official MUJ site uses a large family of human-readable .php URLs; the suffix proves the URL convention only, not a PHP runtime or the SLCM stack.
- The sitemap at https://jaipur.manipal.edu/sitemap.xml is publicly retrievable and lists institutional, academic, admission, faculty, event, compliance, and service routes.
- robots.txt disallows /admin/, /common/, and /content/ for crawlers but explicitly allows images and PDFs to be indexed.
- Public document families: /img/pdf/ (fee documents), /img/pdf/exam/ (examination handbook and timetables), /img/announcement/, and faculty-specific brochure and newsletter paths.
- The fee page names https://mujslcm.jaipur.manipal.edu/ as the student portal and SpaceBasic for hostel and mess fees; the MAHE SIS page (sis.manipal.edu) is a different institutional context.
- A second hostname, https://muj.slcm.jaipur.manipal.edu/, appears in search results with MUJ portal labels; alias or separate deployment is unproven.
- Staff pages publish names plus LinkedIn, IRINS, ORCID, Scopus, Google Scholar, and portfolio links; treated as phishing-enablement data, not proof of compromise.
- Supplied stack fingerprint (ASP.NET MVC 5.3, .NET 4.x, IIS 10, Akamai, M365) remains unverified; the report calls for a governance-first program.

## KEY FACTS
- https://jaipur.manipal.edu/robots.txt - published crawler directives; PDF and image indexing allowed
- https://jaipur.manipal.edu/sitemap.xml - declared route inventory; exact entry count not established
- https://jaipur.manipal.edu/pay-fee-online.php - SLCM link, SpaceBasic reference, bank details, finance email workflow
- https://jaipur.manipal.edu/examination.php - examination handbook and timetable PDF family under /img/pdf/exam/
- https://jaipur.manipal.edu/faculty-list.php - faculties, schools, departments, and service navigation
- https://jaipur.manipal.edu/muj-faculties.php - publicly listed teaching faculty names
- https://jaipur.manipal.edu/fosta/department-of-information-technology.php - staff profiles with external research links
- https://mujslcm.jaipur.manipal.edu/ - primary portal with "WELCOME TO MUJ PORTAL" and login labels
- https://muj.slcm.jaipur.manipal.edu/ - alternate SLCM hostname; relationship to primary unconfirmed
- https://sis.manipal.edu/index.aspx - MAHE student portal; do not attribute to MUJ
- https://learning.onlinemanipal.com/d2l/home/14042 - MUJ online education login; separate service
- https://muj.onlinemanipal.com/ - Online Manipal MUJ domain; separate identity dependency
- https://admissions.jaipur.manipal.edu/ - homepage Apply Now destination; separate admissions asset
- https://jaipur.manipal.edu/img/pdf/Annual-Fee-Payment-for-the-AY-2026-2027.pdf - public fee PDF path under /img/pdf/
- https://jaipur.manipal.edu/img/pdf/Required Transaction details.docx - fee attachment; office-document metadata risk

## ACTIONABLE LEADS
- Verify whether /admin/, /common/, and /content/ are actually inaccessible, under written authorization only; robots is crawler guidance, not access control.
- Run metadata scrubbing checks on the public PDF families: fee PDFs, exam handbook, announcement PDFs, IT compendium, program brochures.
- Passive DNS and certificate review to test the relationship between mujslcm.jaipur.manipal.edu and muj.slcm.jaipur.manipal.edu (alias vs separate deployment).
- Reconcile the sitemap against CMS and retirement records; look for legacy or orphaned routes.
- Build a canonical service catalog: hostname, service, owner, identity provider, data class, support contact, retirement status.
- Monitor the fee page for unauthorized content changes; set up dual approval and a takedown process for stale documents.

## FLAGS
- .php suffixes do not prove PHP; SLCM runtime claims need authorized evidence.
- Sitemap entry count is intentionally not claimed; the report rejected a noisy parser count.
- The alternate SLCM hostname relationship is an unverified inference; do not report as fact.
- MAHE SIS, Online Manipal, and learning.onlinemanipal.com must stay separate inventory items.
- robots disallow directives provide no confidentiality guarantees.

## COVERAGE
33,142 chars read (file_size bytes), read to EOF, truncated=false confirmed.

DONE w2b-12-jaipur-main-site.digest.md