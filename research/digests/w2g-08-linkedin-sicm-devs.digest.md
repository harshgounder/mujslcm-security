# Digest: w2g-08-linkedin-sicm-devs.md

## REPORT
Source file: w2g-08-linkedin-sicm-devs.md. Mapping public LinkedIn and institutional signals to SLCM and campus-portal engineering at MUJ. People-lead inventory with four evidence classes (direct SLCM, MUJ-local role, technology-adjacent, context only) and 43 numbered references.

## ANSWER SUMMARY
- Verdict: the public OSINT search found credible Manipal SLCM and campus-portal engineering leads, but no confirmed named builder or maintainer of mujslcm.jaipur.manipal.edu. Confidence: HIGH for ecosystem mapping, LOW for exact MUJ-host personnel attribution, LOW for the supplied stack as a verified public finding.
- Direct SLCM leads: Himanshu Upadhyay (Project Manager, MAHE Udupi; led and mentored the SLCM support-development team), Poornima Vishwaradhya (SAP SLcM configuration and implementation, Manipal Global Education Services), Zeeshan Khalandar (IT Manager MAHE Dubai; in-house apps and SLCM), Manju Muthamadhu (MAHE Dubai; SLCM application management plus ASP.NET MVC, ASP.NET Core, SQL Server skills). None of the four profiles names the Jaipur host.
- MUJ-local engineering leads: Nitin Agarwal, Sharma Rahul, DEVESH MEENA listed as Software Developer or Software Engineer at Manipal University Jaipur; Rakesh Sharma as IT Engineer with Active Directory, Windows Server, DNS, DHCP, VMware skills. Indexed rows contain no SLCM, portal, or stack language.
- Technology-adjacent leads: Rashmi Acharya (Software Developer, Manipal University Manipal; SQL, C++, ASP.NET, C) and Sumanth Suvarna (Dotnet Developer, MAHE Manipal; ASP.NET MVC, Web Forms, Web API, ADO.NET). Neither is publicly tied to the Jaipur host. Lavi Chauhan is flagged as a portal/".NET MVC" false positive (bank eKYC portal, Manipal Business Solutions).
- Public MUJ pages confirm: portal page at /Home/Index with title "Manipal University", "WELCOME TO MUJ PORTAL", Parent Login, and @muj.manipal.edu labels; FAQ tying SLCM registration to AMS login terminology; Office 365 SOP (v1.0, June 2025) documenting mail setup, sign-in, and MFA.
- Stack verification gap: meta description "User login example" and title only; no framework, server, or CDN version disclosed. ASP.NET MVC 5.3, .NET 4.x, IIS 10, and Akamai remain unverified by the reviewed sources.
- Platform context: a Salesforce press release (March 2026) announces MAHE-wide collaboration to modernize SLCM; it does not establish that the MUJ host is Salesforce-based or migrated.
- False-positive discipline: the token SLCM alone returns unrelated organizations (SLCM Pvt. Ltd., schools, childcare providers); three-way alignment of identity, employer/campus, and explicit SLCM language is required before escalating a candidate.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/Home/Index - public MUJ portal page; "Manipal University" title, "WELCOME TO MUJ PORTAL", Sign In, Parent Login, @muj.manipal.edu labels.
- https://muj.slcm.jaipur.manipal.edu/ - alternate shorter host form surfaced by public search; distinct hostname worth mapping.
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - SLCM registration FAQ; connects login support with AMS terminology.
- https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf - Office 365 SOP v1.0 June 2025; M365 mail identity and MFA documented for students and employees.
- https://in.linkedin.com/in/himanshuupadhyay - Project Manager at MAHE; explicitly led support-development team for the SLCM project.
- https://linkedin.com/in/poornima-vishwaradhya-a0b95b22 - SAP SLcM configuration, master data, implementation, testing, training lead.
- https://ae.linkedin.com/in/zeeshan-khalandar-865920136 - IT Manager MAHE Dubai; SLCM among in-house applications under his IT operations.
- https://linkedin.com/in/manju-muthamadhu - MAHE Dubai ERP and Applications; SLCM operations with ASP.NET MVC, ASP.NET Core, SQL Server skills; strongest combined signal.
- https://in.linkedin.com/in/nitin-agarwal-aa9549209 - Software Developer at MUJ Jaipur; institutional validation candidate, no SLCM wording.
- https://in.linkedin.com/in/sharma-rahul-929b06218 - Software Engineer at MUJ Jaipur; validation candidate.
- https://linkedin.com/in/devesh-meena-a1a37a377 - Software Engineer at MUJ Jaipur; validation candidate.
- https://linkedin.com/in/rakesh-sharma-76890172 - IT Engineer at MUJ Jaipur; Windows/AD/VMware infrastructure adjacency.
- https://linkedin.com/in/rashmi-acharya-54900528 - historical Manipal software developer; ASP.NET, SQL, C++, C.
- https://linkedin.com/in/sumanth-suvarna-212738199 - Dotnet Developer MAHE Manipal; headline lists ASP.NET MVC, Web Forms, Web API, ADO.NET.
- http://salesforce.com/in/news/press-releases/2026/03/26/manipal-university-ai-transformation - Salesforce-MAHE SLCM modernization announcement; MAHE-wide, not MUJ-host evidence.

## ACTIONABLE LEADS
- Build an asset-and-owner matrix: public service URL, institutionally confirmed owner, application/identity/CDN/hosting dependencies, evidence date, confidence. Put LinkedIn names in a candidate-contact column only, never an owner column without institutional confirmation.
- Take the confidence-ranked lead register (Upadhyay, Vishwaradhya, Khalandar, Muthamadhu, then MUJ-local: Agarwal, Rahul, Meena, Sharma; technology: Acharya, Suvarna) to an authorized MUJ or MAHE system owner for confirmation of service, application, identity, CDN owners, and change-control process.
- Terminology normalization: map SLCM, SLcM, Student Life Cycle Management, AMS, portal, ERP, admission life cycle, LMS to distinct services; do not assume one application.
- Turn Manju Muthamadhu's public operations vocabulary (development, configuration, code review, UAT, production movement, monitoring) into authorized owner-interview questions about change approval, UAT records, backup/restore tests, and owner separation.
- Institutional context sources: http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf states SLCM replaced the older Academic Management System; verify the Jaipur instance history through authorized records.
- Track the Salesforce MAHE modernization announcement for migration signals, but do not probe the public login service; disclosure questions go through MUJ IT or published channels.

## FLAGS
- No profile names the Jaipur host; every maintainership inference is explicitly unsupported by the report itself. Treat all people as ecosystem leads for authorized validation.
- Reference list contains multiple same-name records (several Himanshu Upadhyay, Rakesh Sharma, Nitin Sharma, Rahul Sharma variants incl. a Red Hat SRE, a Manhattan consultant, a Pens.com director, an MIT student). URL-suffix disambiguation is required; conflation risk is high.
- Two distinct Sumanth Suvarna profile URLs are cited (212738199 and 767a82171); identity equivalence is unverified.
- Salesforce announcement is MAHE-wide; citing it as MUJ-host platform evidence would overclaim.
- The "User login example" meta description on the live portal page is a generic-template artifact, not a framework fingerprint.
- LinkedIn index snapshots may be stale; a role at an institution does not prove current access or responsibility. The report publishes no personal contact data.
- One search-derived item (Software Development Centre at MUJ, "[534 search result]") lacks a stable URL; reproducibility limited.

## COVERAGE
- File: w2g-08-linkedin-sicm-devs.md.
- 262 lines total; 41,143 bytes on disk; 41,113 chars read.
- Method: read_file offset 1, limit 2000, single call.
- EOF confirmed: final call returned truncated: false, last content line 262 equals total_lines 262.