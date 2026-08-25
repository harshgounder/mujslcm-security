## REPORT (w1-03-vendor-family.md: Tracing Manipal's SLCM Vendor, Instances, and Shared Risk)

## ANSWER SUMMARY
- Historical product is SAP Student Lifecycle Management (SAP SLcM); two independent Manipal Global employee profiles name SAP SLcM implementation across Manipal Education entities (configuration, migration, development, deployment, support).
- No public evidence names MUJ's current builder or maintainer; group lineage is strong, MUJ-specific ownership is an open item.
- Internal Manipal support is real: a MAHE project manager leads the SLCM support-development team; MIT attendance routes to central slcm.manipal.edu and the SIS page is credited to MAHE Department of Digital and Information Technology.
- MUJ has two near-identical public entrances (mujslcm.jaipur.manipal.edu and muj.slcm.jaipur.manipal.edu); identical branding and matching HTML make them near-certain aliases or sibling deployments.
- MUJ does not share the MAHE classic login template; MAHE classic and Dubai share a classic-template family; Malaysia is a visibly separate framework; MIT is a consumer of the central host, not a separate instance.
- MAHE's 2026 modernization is Salesforce (Agentforce Education, Agentforce, MuleSoft, Tableau) with Deloitte as announced integrator; MUJ is not named in the announcement.
- Public code (REST wrapper, feedback auto-filler, mobile app) shows integration surfaces and third-party credential handling, not proven vulnerabilities; no CVE, SQLi, bypass, or breach was established.
- Student complaints (password rejection, pending fee after payment) are anecdotal reliability issues, not verified vulnerabilities.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/ - primary MUJ target; "WELCOME TO MUJ PORTAL" sign-in.
- https://muj.slcm.jaipur.manipal.edu/ - second MUJ entrance; near-certain alias or coupled deployment of the same front end.
- https://slcm.manipal.edu/ - MAHE classic SLCM; strongest template sibling is Dubai, not MUJ.
- https://slcm.manipaldubai.com/ - Dubai classic SLCM; same confirmation-dialog family as MAHE classic.
- http://salesforce.com/in/news/press-releases/2026/03/26/manipal-university-ai-transformation - MAHE Salesforce modernization announcement; Deloitte integrator; 50+ AI agents over two years; MUJ not named.
- http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf - official MAHE ICT inventory defining SLCM modules (attendance, internal/external marks, results, broadcasts).
- https://sis.manipal.edu/AtdMIT.aspx - MIT attendance page that routes users to central SLCM; evidence of internal estate architecture.
- https://github.com/canaryGrapher/slcmAPI - authenticated REST wrapper for marks, attendance, profile; deprecated after CAPTCHA appeared; documents stable authenticated workflows.
- https://github.com/AddisionS/slcm-feedback-form-filler - MUJ feedback form auto-filler with "All Yes"/"All No"; client-side workflow integrity risk on the MUJ form.
- https://github.com/DK10WS/SLCM_APP - third-party MUJ mobile client replicating login, timetable, grades, attendance with custom auth; credential-handling surface.
- https://www.d2l.com/en-in/why-d2l/customers/manipal-university-jaipur-online - D2L publicly identifies itself as the MUJ Online LMS; distinct from campus SLCM.
- https://linkedin.com/in/adrija-sen-91631110 - Manipal Global profile naming SAP SLcM implementation across Manipal Education entities.
- https://linkedin.com/in/poornima-vishwaradhya-a0b95b22 - second Manipal Global profile naming SAP SLcM configuration scope (admissions, academic structure, records, graduation).
- https://student.manipal.edu.my/ - Malaysia student portal; different portal framework, shared SLCM code not proven.
- https://maheslcm.manipal.edu/login/ - MAHE newer email-oriented login portal; separate from the classic and MUJ families.

## ACTIONABLE LEADS
- Operate the two MUJ hostnames as one risk domain: compare login flow, session cookies, form targets, and feedback endpoints across both aliases; confirm whether they share one auth backend.
- Component-level fingerprint comparison (asset paths, jQuery version, form names, state markers) between slcm.manipal.edu and slcm.manipaldubai.com before transferring any finding; ask for an SBOM comparison.
- Test the MUJ feedback form for server-side abuse controls (rate limits, duplicate-submission detection, response-quality gates); the auto-filler proves client-side controls only.
- Review the public student repos (slcmAPI, SLCM_APP, muj_slcm, SLCM_API) for supported endpoints, session handling patterns, and accidentally committed secrets; they model real credential workflows.
- Check https://slcm.manipal.edu/StudentChangePassword.aspx behavior (old/new/confirmation fields) and session invalidation on password change in the classic family.
- Monitor the Salesforce/Deloitte modernization for MUJ-specific announcements, new login surfaces, and MuleSoft integration endpoints; a second Salesforce SIT URL (maheslcmtech--sit.sandbox.my.site.com) sits in the references untouched.
- Use the named MAHE SLCM project manager profile (https://linkedin.com/in/himanshuupadhyay) as a routing lead for coordinated disclosure; the linkedin.com and reddit URLs are the only human contact points in the report.

## FLAGS
- SAP lineage rests on two self-reported LinkedIn-style profiles; no first-party contract or MUJ statement confirms SAP SLcM on MUJ today.
- The two-MUJ-host equivalence is inferred from static HTML similarity; not owner-confirmed.
- Salesforce announcement URL is unverified in this digest; confirm the press release exists before citing the program details.
- "Crucia, ITL, Jain Group, Manipal Technologies" candidates were searched with no results; absence is not proof of non-involvement, so absence claims are weak-negative.
- Reddit complaints are Tier 3 anecdotal; no root cause or exploitability shown.
- The report cites a Salesforce SIT sandbox login URL but never analyzes it as a surface; reachability and exposure are unverified.
- No CVE, SQL injection, authentication bypass, or breach is established anywhere in the report; any parent-level claim of one would be unsupported.

## COVERAGE (37324 chars as read, read verified to EOF, 286 lines)