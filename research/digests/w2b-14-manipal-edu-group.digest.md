# Digest: w2b-14-manipal-edu-group.md

## REPORT
Source file: w2b-14-manipal-edu-group.md (Manipal Group Portals and the MUJ SLCM Boundary)

## ANSWER SUMMARY
- MAHE's ICT inventory defines SLcM as Student Life Cycle Management replacing the older Academic Management System, with attendance, internal and external marks, result publication, broadcast messages, and a student-and-parent single window.
- The MUJ portal shows student and parent login labels, @muj.manipal.edu wording, and a same-host form with an anti-forgery token; MVC-consistent, but exact versions and Akamai placement are unverified.
- IMA resolves to ICICI Manipal Academy for Banking and Insurance, a joint venture of ICICI Bank and Manipal Global Education Services; not an evidenced SLCM front end.
- CIA currently serves MAHE institutional content with an Apply Now link to apply.manipal.edu; CareerNext serves MIT and MAHE admissions and student-club pages.
- Smart Achievers (HDFC Life) and Young Achievers (Tata AIG) are program-specific EduNxt login surfaces; archived paths for Smart suggest a historical Drupal-style deployment with Seckit.
- Manipal Matters is an e-newsletter with historical WordPress paths (wp-admin, wp-content, xmlrpc.php, category and post parameters).
- No public evidence reviewed proves common SLCM code, tenant, API, or database linking any of the six portals to MUJ SLCM; the correct wording is "not publicly evidenced," not "proven separate."
- Microsoft 365 MX records and MicrosoftOnline realm responses show mail routing and identity management, but do not prove shared application SSO or data.

## KEY FACTS
- http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf - SLCM definition and module inventory baseline
- https://mujslcm.jaipur.manipal.edu/ - MUJ portal labels, form fields, and Microsoft password-reset link
- https://ima.manipal.edu/ - IMA academy identity and contact
- https://cia.manipal.edu/ - current MAHE institutional content surface
- https://careernext.manipal.edu/mitblr.html - MIT admissions content path
- https://edunxt.smartachievers.manipal.edu/ - User Login MAB surface
- https://edunxt.youngachievers.manipal.edu/ - User Login EduNxt surface
- https://manipalbfsi.com/job-ready-programs/hdfc-life-smart-achievers-program - HDFC program purpose
- https://manipalbfsi.com/job-ready-programs/tata-aig-young-achievers-program - Tata AIG program purpose
- https://slcm.manipal.edu/ - MU SLcM branding with 2017 MAHE copyright
- https://sis.manipal.edu/studloginSLCM.aspx - MAHE Information Systems login surface
- https://web.archive.org/cdx/search/cdx?url=edunxt.smartachievers.manipal.edu/*&output=json&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&collapse=urlkey - archived HDFC route and Drupal-style asset paths
- https://web.archive.org/cdx/search/cdx?url=manipalmatters.manipal.edu/*&output=json&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&collapse=urlkey - archived WordPress-era paths
- http://dns.google/resolve?name=muj.manipal.edu&type=MX - Microsoft protection MX record evidence
- http://login.microsoftonline.com/getuserrealm.srf?login=probe@jaipur.manipal.edu&xml=1 - MicrosoftOnline realm response for the Jaipur domain

## ACTIONABLE LEADS
- Ask each portal owner the exact architecture question: is the portal an SLCM client, and if so is it an API integration, SSO trust, replicated data feed, or shared database?
- Passive corroboration for the six hosts: certificate transparency, DNS records, and wayback captures for ownership and retirement timelines.
- Check whether CareerNext .html paths are static files or CMS-generated via passive header inspection, not probing.
- Confirm whether cia.manipal.edu is a redirect, reverse-proxy alias, or separate app through official redirect inventories.
- Archive the NAAC ICT PDF as the SLCM functional baseline for future comparisons.
- Record the supplied stack fingerprint as unverified assessment input until an owner-approved asset inventory confirms it.

## FLAGS
- EduNxt and WordPress path evidence is historical (2014, 2018, 2022 captures); it does not fingerprint current servers.
- MX and realm records establish Microsoft mail or identity management only; shared SSO, tenant, and database remain unproven.
- The report's negative finding is bounded: absence of public integration evidence is not proof of technical separation.
- Exact stack claims (MVC 5.3, .NET 4.x, IIS 10, Akamai) stay requester-supplied hypotheses.
- Similar branding under one parent domain must not be read as shared code or data.

## COVERAGE
43,661 chars read (file_size bytes), read to EOF, truncated=false confirmed.

DONE w2b-14-manipal-edu-group.digest.md