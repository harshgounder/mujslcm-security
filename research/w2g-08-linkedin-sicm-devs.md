# Mapping Public SLCM and Campus-Portal Engineering Signals at MUJ

## Executive Summary

- **Direct SLCM Ownership Signal**: Public LinkedIn evidence identifies Manipal and MAHE personnel who explicitly describe SLCM support, configuration, application management, or development-team leadership, but none of the reviewed public profiles names the MUJ host `mujslcm.jaipur.manipal.edu` as their specific responsibility [9][29][14][37]. **Action:** treat these people as ecosystem leads for authorized vendor or institutional validation, not as confirmed maintainers of the MUJ instance.
- **MUJ-Local Engineering Signal**: Nitin Agarwal, Sharma Rahul, and DEVESH MEENA are publicly indexed as a Software Developer or Software Engineer at Manipal University Jaipur in Jaipur [30][39][24]. **Action:** prioritize institutional confirmation of their department and historical project scope, while avoiding the unsupported conclusion that any one of them built SLCM.
- **Strongest Technical Adjacency**: Rashmi Acharya publicly describes Software Developer work at Manipal University Manipal, requirements collection, testing, maintenance, documentation, SQL, C++, ASP.NET, and C [38]. **Action:** regard this as a historical Manipal application-development lead and a possible technology-context signal, not evidence of work on the Jaipur portal.
- **Closest Public Stack Match**: Sumanth Suvarna is publicly listed as a Dotnet Developer at MAHE Manipal and describes ASP.NET Web Forms, C#, SQL Server, stored procedures, and web application work; the indexed profile headline also lists ASP.NET MVC, Web Forms, Web API, ADO.NET, and JavaScript [41]. **Action:** use this as an ecosystem technology lead, not proof that the MUJ host uses the same stack.
- **Operational SLCM Signal**: Manju Muthamadhu publicly describes managing and supporting Student Life Cycle, admission, and other applications at MAHE Dubai, including development or enhancement, configuration, code review, UAT, production movement, monitoring, and an explicit skill set including ASP.NET MVC, ASP.NET Core, C#, and Microsoft SQL Server [37]. **Action:** this is the strongest public profile combining SLCM operations with software-engineering language, but the campus is Dubai, not Jaipur.
- **Identity Boundary**: The MUJ SLCM FAQ publicly identifies the registration URL and says that login support concerns the AMS, while the MUJ Office 365 SOP separately documents university mail ID setup, Microsoft 365 sign-in, and MFA for students and employees [20][6]. **Action:** document the identity relationship as a confirmed institutional workflow, but do not infer federation architecture or credential reuse beyond what the pages state.
- **Stack Verification Gap**: Public page content confirms the MUJ portal title, SLCM host/path, and sign-in labels, but the reviewed public sources do not independently confirm ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, or Akamai for that host [16]. **Action:** mark each supplied technology claim as unverified in this report.
- **False-Positive Risk**: Searches for the token SLCM return unrelated organizations, schools, childcare providers, and companies; searches for Manipal Technologies also return non-engineering and unrelated Manipal entities. **Action:** require three-way alignment among identity, employer/campus, and explicit SLCM or portal language before escalating a candidate.

## Scope, Ethics, and Evidence Standard

This report addresses public information only. The evidence base consists of public LinkedIn profile indexes, public institutional pages, public PDFs, and public company material. It does not use a LinkedIn login, private profile content, credentials, private contact data, password testing, exploitation, endpoint fuzzing, or attempts to bypass access controls. The MUJ SLCM landing page is treated only as a public service-identification page, not as an invitation to test the application [16].

The central analytic problem is attribution. A person can be associated with Manipal, SLCM, .NET, or a portal without being the person who built or maintains the specific Jaipur host. The report therefore uses four evidence classes. **Direct** means a profile explicitly states SLCM or Student Life Cycle responsibility and the employer is a Manipal or MAHE entity. **MUJ-local role** means the profile states a software or IT role at Manipal University Jaipur but says nothing about SLCM ownership. **Technology-adjacent** means a public profile describes relevant web technology or application work at another Manipal entity. **Context only** means the source identifies the service or an institutional process but does not identify a person.

The requested `cot_explicit` field requires a careful distinction. I cannot provide hidden private chain-of-thought. I can provide a reproducible reasoning summary: first, search exact phrases and employer combinations; second, remove unrelated SLCM entities; third, separate MUJ from MAHE-wide, Manipal, Dubai, and other-campus evidence; fourth, compare role, employer, explicit application wording, and technology terms; fifth, report unknowns rather than infer maintainership. This is an auditable method rather than a disclosure of private internal reasoning.

The search corpus itself demonstrates why this discipline matters. A broad SLCM query surfaced Rahul Tomar at SLCM Pvt. Ltd., a teacher at an unrelated SLCM, and other unrelated employers before the Manipal-specific query produced direct Manipal records [s.0-s.5 from the initial SLCM result]. Inference: the string `SLCM` has low attribution value by itself. Employer, geography, role, and explicit application language must be combined.

| Evidence class | Inclusion rule | What it can support | What it cannot support |
|---|---|---|---|
| Direct SLCM | Manipal or MAHE employer plus explicit SLCM responsibility | A public lead for SLCM operations, configuration, support, or development | Ownership of the Jaipur host unless the host is named |
| MUJ-local role | MUJ employer plus software or IT role | A local engineering or IT lead | SLCM work, stack, or current employment beyond the indexed row |
| Technology-adjacent | Manipal-related employer plus explicit .NET, ASP.NET, SQL, testing, or web-app language | Technology-context lead | Deployment on `mujslcm.jaipur.manipal.edu` |
| Institutional context | Official MUJ or MAHE page/PDF | Service name, login workflow, scope, or platform direction | Named developer or maintainer |

**Decision-ready insight:** attribution confidence should be driven by explicit project wording, not by a shared employer name or a matching technology keyword.

## What the Public MUJ Pages Establish

The MUJ SLCM landing page identifies itself as `Manipal University`, displays `WELCOME TO MUJ PORTAL`, and exposes `Sign In`, `@muj.manipal.edu`, `Parent Login`, and related sign-in labels [16]. The same public page is available at `https://mujslcm.jaipur.manipal.edu/Home/Index`, while public search results also identify the shorter host form `https://muj.slcm.jaipur.manipal.edu/` [1]. These facts establish a public service surface and its institutional naming. They do not establish who wrote the code, who administers the server, or whether the host is operated by MUJ employees, a central MAHE team, a contractor, or a managed service provider.

The official MUJ FAQ calls itself `Frequently Asked Questions and Contacts for SLCM Registration` and identifies `https://mujslcm.jaipur.manipal.edu/` as the registration link [20]. It also describes an inability to log in to AMS and directs users to re-verify login credentials before using institutional support channels [20]. The wording is useful because it connects the public SLCM registration process with the term AMS, but it does not identify a software team or disclose implementation details.

The public landing-page extraction includes a raw HTML title of `Manipal University` and a generic meta description of `User login example`; it does not disclose a framework version or an origin server [16]. This is an important negative finding. A page title, login label, and HTML metadata are not sufficient to identify ASP.NET MVC, the .NET Framework version, IIS, Akamai, or an authentication protocol. Inference: the user-supplied stack description may have come from a separate authorized fingerprinting exercise, a historical observation, or internal knowledge, but it is not independently substantiated by the sources reviewed here.

| Public MUJ artifact | Exact URL | Confirmed public content | Attribution limit |
|---|---|---|---|
| SLCM landing page | https://mujslcm.jaipur.manipal.edu/Home/Index | MUJ Portal title and sign-in labels [16] | No named developer or framework version |
| SLCM registration FAQ | https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf | Registration URL, SLCM registration title, AMS login terminology [20] | No maintainer identity or source-code attribution |
| Office 365 SOP | https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf | Office 365 mail setup, university audience, sign-in and MFA workflow [6] | Does not prove SLCM federation or password reuse |

**Decision-ready insight:** the public MUJ material is enough to define the service and its user-facing identity workflow, but not enough to attribute implementation or hosting.

## Direct SLCM and Student-Life-Cycle Leads

### Himanshu Upadhyay: strongest MAHE development-management lead

The public profile for Himanshu Upadhyay lists Project Manager at Manipal Academy of Higher Education in Udupi [14]. Its experience text says that he managed ERP development work across multiple projects and led and mentored the support development team for the SLCM project [14]. The same indexed profile describes him as a Senior .NET Developer and Power Platform enthusiast [14]. This is direct evidence of a relationship to an SLCM support-development team within MAHE.

The limitation is scope. The profile says MAHE and Udupi; it does not name Manipal University Jaipur, `mujslcm.jaipur.manipal.edu`, or the supplied MUJ technology stack [14]. Inference: he is a high-value institutional lead for understanding how a Manipal SLCM support function is organized, but assigning him as the Jaipur maintainer would exceed the evidence. A university security club should use the profile to formulate an authorized question for the institution, not to contact the person about sensitive system details or treat the profile as a vulnerability indicator.

### Poornima Vishwaradhya: configuration and implementation lead

Poornima Vishwaradhya is publicly listed as Assistant Manager at Manipal Global Education Services in Bengaluru [29]. Her profile describes configuration of Student Life Cycle Management, specifically SAP SLcM processes and master data for academic structure, academic calendar, admission, audit, event planning, module booking, student master data, records management, reports, and graduation [29]. Her summary also describes requirements definition, implementation, application testing, system implementation, and training in SAP SLcM [29].

This profile is a strong direct match for business-process and implementation work, but it is not a software-maintainer match for the MUJ host. It points to SAP SLcM and Manipal Global Education Services rather than the public MUJ web portal. Inference: Poornima may be valuable for understanding institutional SLCM modules and implementation vocabulary, but the source does not justify attributing code ownership, server administration, or MUJ-specific work to her.

### Zeeshan Khalandar: IT operations lead at another Manipal campus

Zeeshan Khalandar is listed as IT Manager at Manipal Academy of Higher Education - MAHE, Dubai [9]. The profile states that he is responsible for IT operations and projects, including in-house applications, apps, and SLCM, and that he leads the IT team in Manipal Dubai [9]. This is direct public evidence linking an IT manager to SLCM operations in the Manipal ecosystem.

The campus qualifier is decisive. The profile explicitly says Manipal Dubai, not MUJ Jaipur [9]. Inference: his profile supports the proposition that campus-level IT teams may manage SLCM-related applications, but it does not establish that the same team operates the Jaipur host. It is also not evidence that the implementation is ASP.NET MVC, .NET Framework, IIS, or Akamai.

### Manju Muthamadhu: software and application-operations lead

Manju Muthamadhu is listed as Assistant Manager, ERP and Applications, with the parenthetical title Senior Software Engineer, at MAHE Dubai [37]. The profile says that the role manages and supports Student Life Cycle, Brightspace, and admission life-cycle applications [37]. It further describes development or enhancement, configuration, day-to-day operations, technical and functional requirements, code reviews, UAT, production movement, post-production testing, monitoring, and support for in-house applications [37].

The same profile lists ASP.NET, ASP.NET MVC, ASP.NET Core, Web API and microservices, Windows Services, Microsoft SQL Server, C#, HTML, CSS, Bootstrap, JavaScript, and jQuery as skills [37]. This makes Manju the closest public match to the combination of application operations, SLCM, software development, and the user's technology interests. Nevertheless, every explicit campus reference in the record is MAHE Dubai [37]. Inference: this is an ecosystem-adjacent engineering lead and a useful comparator for defensive architecture questions, not a confirmed MUJ maintainer.

| Candidate | Exact public profile URL | Listed role and employer | Direct public evidence | Scope | Confidence for MUJ host maintainership |
|---|---|---|---|---|---|
| Himanshu Upadhyay | https://linkedin.com/in/himanshuupadhyay | Project Manager, Manipal Academy of Higher Education [14] | Led and mentored support development team for SLCM project [14] | MAHE, Udupi | Low for MUJ host; high for MAHE SLCM lead |
| Poornima Vishwaradhya | https://linkedin.com/in/poornima-vishwaradhya-a0b95b22 | Assistant Manager, Manipal Global Education Services [29] | SAP SLcM configuration, master data, implementation, testing, training [29] | Manipal Global Education Services, Bengaluru | Low for MUJ host; high for SAP SLcM implementation lead |
| Zeeshan Khalandar | https://linkedin.com/in/zeeshan-khalandar-865920136 | IT Manager, MAHE Dubai [9] | In-house applications, apps, and SLCM; leads Dubai IT team [9] | MAHE Dubai | Low for MUJ host; medium-high for Dubai SLCM operations |
| Manju Muthamadhu | https://linkedin.com/in/manju-muthamadhu | Assistant Manager, ERP and Applications, MAHE Dubai [37] | Manages SLCM applications, development/enhancement, UAT, code review, production operations [37] | MAHE Dubai | Low for MUJ host; high for SLCM application-operations adjacency |

**Decision-ready insight:** the direct leads establish a distributed Manipal SLCM ecosystem, not a single publicly attributable MUJ engineering owner.

## MUJ-Localized Software and IT Profiles

The most relevant localized records are Nitin Agarwal, Sharma Rahul, DEVESH MEENA, and Rakesh Sharma. Nitin Agarwal is listed as a Software Developer at Manipal University Jaipur in Jaipur [30]. Sharma Rahul is listed as a Software Engineer at the same university and location [24]. DEVESH MEENA is likewise listed as a Software Engineer at Manipal University Jaipur in Jaipur [39]. These profiles are important because they satisfy the employer, geography, and role filters.

However, the indexed records for Nitin, Sharma Rahul, and Devesh contain only a compact employment-role statement. They do not say SLCM, Student Life Cycle Management, portal, ASP.NET, MVC, .NET Framework, IIS, Akamai, or Microsoft 365 [30][39][24]. Inference: each person is a reasonable candidate for institutional verification because of the public MUJ software role, but none can be described as a confirmed SLCM developer or maintainer.

Rakesh Sharma is listed as an IT Engineer at Manipal University Jaipur in Jaipur [40]. The indexed skills include Active Directory, Windows Server, servers, DHCP, DNS, operating systems, ITIL, VMware, antivirus, hardware, and IT service management [40]. This is a useful infrastructure-adjacency signal. It may indicate operational or support relevance, but it is not application ownership evidence. The record does not state SLCM, portal administration, IIS, or Akamai [40].

The search also surfaced a Software Development Cell profile associated with Manipal University Jaipur and a student-placement coordinator, but organizational or student profiles should not be conflated with employment as the SLCM maintainer. The public search result describes the Software Development Centre at MUJ, but it does not identify a named person responsible for the SLCM host [534 search result]. Inference: student or departmental software groups may be useful for understanding campus development culture, but they are not evidence of production ownership.

| MUJ-local lead | Exact public profile URL | Public role/employer evidence | Public technology or SLCM evidence | Assessment |
|---|---|---|---|---|
| Nitin Agarwal | https://linkedin.com/in/nitin-agarwal-aa9549209 | Software Developer, Manipal University Jaipur, Jaipur [30] | None in indexed row [30] | Medium lead for local engineering, low for SLCM attribution |
| Sharma Rahul | https://linkedin.com/in/sharma-rahul-929b06218 | Software Engineer, Manipal University Jaipur, Jaipur [24] | None in indexed row [24] | Medium lead for local engineering, low for SLCM attribution |
| DEVESH MEENA | https://linkedin.com/in/devesh-meena-a1a37a377 | Software Engineer, Manipal University Jaipur, Jaipur [39] | None in indexed row [39] | Medium lead for local engineering, low for SLCM attribution |
| Rakesh Sharma | https://linkedin.com/in/rakesh-sharma-76890172 | IT Engineer, Manipal University Jaipur, Jaipur [40] | Active Directory, Windows Server, DNS, DHCP, VMware, ITSM [40] | Medium lead for infrastructure support, low for SLCM attribution |

**Decision-ready insight:** the MUJ-local search produces names worth validating through authorized institutional channels, but public evidence does not support naming any one as the portal owner.

## Technology Keywords and Employer Hints

Rashmi Acharya is a historical Manipal software-development lead. The public profile lists Software Developer at Manipal University Manipal, describes requirements collection through testing and maintenance, and lists SQL, C++, ASP.NET, and C [38]. This is a meaningful technology signal because it connects a Manipal software role with ASP.NET and the complete requirements-to-maintenance lifecycle. It still does not mention MUJ Jaipur, SLCM, the public MUJ host, or MVC 5.3 [38]. Inference: Rashmi may help explain a historical Manipal development environment, but using her profile to identify the MUJ maintainer would be unjustified.

Sumanth Suvarna is listed as Dotnet Developer at MAHE Manipal [41]. The profile describes scalable and secure web applications using ASP.NET Web Forms and C#, SQL Server schema design, stored procedures, and complex queries [41]. The indexed headline for that MAHE profile lists ASP.NET MVC, Web Forms, SQL Server, C#, Web API, ADO.NET, and JavaScript [42]. This is the closest public technology match for a Manipal developer whose profile includes MVC terminology.

The scope caveat is again material. The public record says MAHE Manipal and describes e-commerce payment gateways, not the MUJ SLCM application [41]. Inference: Sumanth is a relevant technology-context lead, but the evidence does not connect him to `mujslcm.jaipur.manipal.edu`. Also, the presence of ASP.NET MVC in a person's skills does not prove the production host uses MVC, much less version 5.3.

Lavi Chauhan is a Software Developer at Manipal Business Solutions and publicly describes a client portal for bank eKYC lead management using .NET Core API and React; the summary includes .NET MVC, SQL Server, and Web API [43]. This is a portal-development and Manipal-employer signal, but it concerns a banking client portal rather than a university SLCM system. Inference: Lavi is a false positive for MUJ SLCM attribution but a useful example of why `portal` and `.NET MVC` keyword matches require project-specific corroboration.

| Profile | Exact URL | Employer and role | Technology keywords | Project wording | Relevance |
|---|---|---|---|---|---|
| Rashmi Acharya | https://linkedin.com/in/rashmi-acharya-54900528 | Software Developer, Manipal University Manipal [38] | SQL, C++, ASP.NET, C [38] | Requirements, testing, maintenance, documentation [38] | Historical Manipal technology lead; not MUJ-specific |
| Sumanth Suvarna | https://linkedin.com/in/sumanth-suvarna-212738199 | Dotnet Developer, MAHE Manipal [41] | ASP.NET Web Forms, C#, SQL Server; MVC/Web API and related skills [42][41] | Web applications and payment-gateway integration [41] | Strong stack adjacency; no MUJ SLCM attribution |
| Lavi Chauhan | https://linkedin.com/in/lavi-chauhan-bb002b21b | Software Developer, Manipal Business Solutions [43] | .NET MVC, .NET Core API, SQL Server, Web API, React [43] | Client portal for bank eKYC lead management [43] | Portal false positive for university SLCM |
| Manju Muthamadhu | https://linkedin.com/in/manju-muthamadhu | ERP and Applications, Senior Software Engineer, MAHE Dubai [37] | ASP.NET MVC, ASP.NET Core, C#, SQL Server, Web API [37] | SLCM application management, code review, UAT, production operations [37] | Strongest combined SLCM and software-operations adjacency; not MUJ |

**Decision-ready insight:** the technology evidence supports an ecosystem-level hypothesis that Manipal-related teams have .NET and application-delivery expertise, but it cannot fingerprint or attribute the MUJ production stack.

## Identity, SLCM Scope, and Platform Direction

The MUJ Office 365 SOP is titled `How To Setup Your Office 365 Mail ID`, identifies itself as an IT Services standard operating procedure, and states Version 1.0, June 2025, for students and employees [6]. Its extraction describes navigating to Microsoft 365, signing in with a university mail identity, and configuring MFA [6]. This supports the limited claim that Microsoft 365 identity is part of the institution's documented user-account workflow.

The MUJ SLCM page shows `@muj.manipal.edu` in its sign-in labels [16]. The FAQ gives the SLCM registration URL and uses AMS terminology in its login troubleshooting instructions [20]. Together, these sources show a public relationship among MUJ, university-branded identity, and SLCM/AMS user access. They do not state that SLCM uses Microsoft Entra ID, SAML, OpenID Connect, OAuth, Active Directory federation, or any specific token flow. They also do not state that the SLCM password is the Microsoft 365 password. Inference: the identity systems may be related operationally, but the architecture must remain unknown unless the institution publishes it.

A separate official Manipal ICT document describes Student Life Cycle Management as a complete suite and states that SLCM replaced the older Academic Management System; the extracted document includes modules such as attendance, internal marks, external marks, and related academic functions [36]. This provides broader institutional context, but it should not be treated as a technical description of the Jaipur host. Similarly, Salesforce announced in March 2026 a collaboration with MAHE to modernize its SLCM platform and support an AI-driven university transformation [8]. The public announcement is MAHE-wide and does not, on the reviewed evidence, identify the MUJ host or its current implementation [8].

| Claim | Evidence status | Reason |
|---|---|---|
| MUJ has a public SLCM registration/login service | Confirmed | Official MUJ page and FAQ identify the portal and registration URL [16][20] |
| MUJ uses university-branded identity labels in the portal | Confirmed | Portal displays `@muj.manipal.edu` [16] |
| MUJ documents Microsoft 365 mail identity and MFA | Confirmed | Official Office 365 SOP covers students/employees and MFA [6] |
| SLCM definitely federates to Microsoft 365 | Not confirmed | Reviewed pages do not name federation or protocol |
| SLCM password is definitely the Microsoft 365 password | Not confirmed | Avoid inferring from general identity wording |
| MAHE has an SLCM modernization collaboration with Salesforce | Confirmed for MAHE announcement | Salesforce describes the collaboration and SLCM modernization [8] |
| MUJ host is already Salesforce-based | Not confirmed | MAHE-wide announcement does not establish MUJ host scope |

**Decision-ready insight:** identity and platform direction are moving targets; document the confirmed workflow, but do not merge MUJ, MAHE-wide, Dubai, SAP, Salesforce, and historical .NET evidence into one implementation claim.

## What Remains Unanswered

The most important unanswered question is the named maintainer or builder of `mujslcm.jaipur.manipal.edu`. The reviewed public LinkedIn records identify MUJ software and IT employees and Manipal/MAHE SLCM specialists, but no source explicitly says that a named individual built, maintains, deploys, or administers that exact host [30][39][24][40][9][14].

The second unanswered question is the exact technical stack. The public MUJ page extraction gives a title, sign-in labels, and raw HTML metadata, but no framework or server-version disclosure [16]. Search results identify the portal, but the reviewed public evidence does not independently confirm ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, or Akamai. Relevant profiles mention ASP.NET, MVC, .NET, SQL Server, and application operations at other Manipal entities, but profiles are not host fingerprints [38][37][41].

The third unanswered question is whether the MUJ portal and other Manipal SLCM instances share code, identity, deployment, or vendor ownership. The institutional sources show common terminology and organizational relationships, but they do not establish code reuse, common tenancy, common cloud infrastructure, or a shared support queue [20][36][8].

The fourth unanswered question is current employment and project timing for several profiles. LinkedIn indexes are snapshots and may omit updates, and a role at an institution does not prove current access or current responsibility. The report therefore does not publish personal emails, phone numbers, or private contact information, and it does not recommend contacting individuals for sensitive details.

| Unanswered item | Current status | Safe resolution path |
|---|---|---|
| Named builder/maintainer of the MUJ host | Unknown | Obtain written confirmation from MUJ IT, procurement, or an authorized system owner |
| ASP.NET MVC 5.3 on the host | Not independently confirmed | Use an authorized asset inventory or approved configuration record |
| .NET Framework 4.x on the host | Not independently confirmed | Verify through approved server/application documentation |
| IIS 10 on the host | Not independently confirmed | Verify through authorized infrastructure inventory |
| Akamai in front of the host | Not independently confirmed by reviewed sources | Verify through authorized DNS/CDN account records |
| Microsoft 365 federation protocol | Unknown | Confirm with the identity owner and architecture documentation |
| Shared code between MUJ and other Manipal SLCM instances | Unknown | Confirm through contracts, repositories, or change records available to authorized staff |

**Decision-ready insight:** the public record is sufficient to create a lead list and an evidence register, but insufficient to make a personnel attribution or a definitive technical fingerprint.

## Defensive Use for a University Security Club

A security club can use these findings defensively by building an asset-and-owner matrix. The first column should contain the public service identifier and exact URL. The second should contain the institutional owner confirmed through authorized channels. The third should record application, identity, CDN, and hosting dependencies. The fourth should record evidence dates and confidence. LinkedIn leads should be placed in a `candidate contact or validation lead` column, never in an `owner` column unless the institution confirms the relationship.

A second safe use is terminology normalization. The sources use SLCM, SLcM, Student Life Cycle Management, AMS, portal, ERP, admission life cycle, and LMS in overlapping contexts [20][36][37]. A defensive inventory should map those terms to distinct services and avoid assuming that every use of SLCM identifies the same application. The unrelated search results prove that token matching alone is unreliable.

A third safe use is change-management review. Manju's public description of development or enhancement, configuration, code review, UAT, production movement, testing, and monitoring provides a useful generic control vocabulary for an authorized application-owner interview [37]. It does not reveal secrets or justify probing. A club can turn those nouns into questions such as: Is every production movement approved? Are UAT and post-production checks recorded? Are backups and restores tested? Are application and identity owners distinct? These are governance questions, not intrusion instructions.

A fourth safe use is stack uncertainty management. Instead of assuming the supplied ASP.NET MVC, .NET Framework, IIS, Akamai, and Microsoft 365 values are proven, the club should label them `reported or hypothesized` until confirmed by authorized records. This prevents an inaccurate technology assumption from driving the wrong patching, logging, or threat model. It also helps distinguish a web application concern from an identity concern and a CDN configuration concern.

| Defensive work product | Public evidence input | Required authorization boundary |
|---|---|---|
| Service inventory | MUJ portal URL and FAQ [16][20] | Confirm ownership and scope with MUJ IT |
| People-to-system lead register | MUJ and MAHE profile roles [30][39][24][9][37] | Do not treat profiles as access or ownership proof |
| Technology hypothesis register | ASP.NET/.NET/MVC/SQL terms in profiles [38][37][41] | Confirm only through approved asset/configuration records |
| Identity dependency map | MUJ sign-in label and Office 365 SOP [16][6] | Do not test credentials or infer token flows |
| Change-control checklist | Public SLCM operations language [37] | Discuss process with authorized owners only |

**Decision-ready insight:** the safest value of this OSINT is better ownership, inventory, and change-control documentation, not deeper public probing of the login service.

## Synthesis and Comparative Analysis

The evidence separates into three different operating models. The first is **institutional SLCM leadership**, represented by Himanshu and Poornima. Himanshu's profile emphasizes support-development leadership within MAHE, while Poornima's emphasizes SAP SLcM configuration, requirements, implementation, testing, and training [14][29]. Their mechanism is governance and delivery of student-life-cycle processes. Their trade-off is weak host attribution: neither profile names MUJ Jaipur.

The second is **campus IT and application operations**, represented by Zeeshan and Manju at MAHE Dubai. Zeeshan emphasizes IT operations, in-house applications, and SLCM; Manju adds software-engineering activities such as code review, UAT, production movement, monitoring, and ASP.NET MVC skills [9][37]. Their mechanism is local operational ownership. Their trade-off is geographic scope: the evidence is Dubai-specific and cannot be transferred to Jaipur by assumption.

The third is **MUJ-local role and technology adjacency**, represented by Nitin, Sharma Rahul, Devesh, Rakesh, Rashmi, and Sumanth. The first three show software roles at MUJ, Rakesh shows IT and Windows/network skills at MUJ, Rashmi shows historical Manipal ASP.NET development, and Sumanth shows MAHE .NET and ASP.NET web development [30][39][24][40][38][41]. The mechanism is a plausible labor and skills network. The trade-off is evidentiary distance from the actual host.

The non-obvious tension is that the strongest SLCM evidence and the strongest MUJ-local evidence are not the same records. The direct SLCM profiles are in MAHE Udupi, Manipal Global Education Services Bengaluru, and MAHE Dubai, while the MUJ-local engineering profiles do not mention SLCM [9][29][14][30][39][24]. This divergence may reflect incomplete LinkedIn descriptions, separate campus responsibilities, contractors, or a central support model. It does not resolve the attribution question.

A second tension concerns technology. Manju, Rashmi, and Sumanth provide real ASP.NET or .NET evidence within the wider Manipal ecosystem [37][38][41]. Yet the MUJ page itself exposes no framework version in the reviewed public material [16]. The proper conclusion is not that the supplied stack is wrong; it is that public profile and page evidence cannot independently verify it. Security decisions should therefore use a confidence label and seek authorized configuration evidence.

A third tension concerns platform modernization. The official Salesforce announcement describes MAHE collaboration to modernize SLCM [8], while public MUJ material still presents a traditional SLCM registration and AMS support workflow [20]. These facts can coexist because the announcement is MAHE-wide and the FAQ is MUJ-specific. They should not be collapsed into a claim that the Jaipur host has already migrated.

| Dimension | Institutional SLCM leads | Campus operations leads | MUJ-local and technology leads |
|---|---|---|---|
| Primary evidence | Explicit SLCM responsibilities [29][14] | Applications, SLCM, code/UAT/operations [9][37] | MUJ role or relevant technology [30][38][41] |
| Scope | MAHE or Manipal Global | MAHE Dubai | MUJ Jaipur or other Manipal entity |
| Best supported conclusion | SLCM process/support expertise | SLCM application operations expertise | Possible local engineering or stack adjacency |
| Main risk of overclaiming | Assigning MUJ ownership | Transferring Dubai scope to Jaipur | Equating a role or skill with SLCM maintainership |
| Recommended use | Authorized institutional lead | Defensive operations comparison | Validation lead and technology context |

**Decision-ready insight:** confidence rises when role, campus, application wording, and host identity align; in this dataset they align only partially, so the final attribution must remain conservative.

## VERDICT

**Verdict: The public OSINT search found credible Manipal SLCM and campus-portal engineering leads, but it did not identify a confirmed named builder or maintainer of `mujslcm.jaipur.manipal.edu`. Overall confidence in the ecosystem mapping is HIGH; confidence in exact MUJ-host personnel attribution is LOW; confidence in the supplied technical stack as an independently verified public finding is LOW.**

The highest-confidence direct SLCM leads are Himanshu Upadhyay, Poornima Vishwaradhya, Zeeshan Khalandar, and Manju Muthamadhu because their public profiles explicitly mention SLCM responsibilities at Manipal or MAHE entities [9][29][14][37]. The strongest MUJ-local engineering leads are Nitin Agarwal, Sharma Rahul, and DEVESH MEENA, with Rakesh Sharma as an IT and infrastructure-adjacent lead [30][39][24][40]. Rashmi Acharya and Sumanth Suvarna are the strongest technology-context leads for ASP.NET and .NET, but neither is publicly tied to the Jaipur host [38][41].

The report does not support naming any individual as the maintainer of the MUJ SLCM host. It also does not independently confirm ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, or Akamai from the reviewed public sources [16]. Microsoft 365 identity is documented as a MUJ institutional mail and MFA workflow, and the MUJ SLCM service uses a university-branded sign-in label, but federation protocol, token flow, and password relationship remain unknown [6][16][20].

**Recommended next step:** the university security club should provide this confidence-ranked lead register to an authorized MUJ or MAHE system owner and request confirmation of the service owner, application owner, identity owner, CDN owner, technology inventory, and current change-control process. It should not contact people to solicit credentials, test accounts, or unpublished architecture details, and it should not perform unauthorized testing of the public login service.

## References

1. *Manipal University*. https://muj.slcm.jaipur.manipal.edu/
2. *Manipal University Jaipur - 71 years of legacy of Manipal ...*. https://jaipur.manipal.edu/
3. *MU SLcM*. https://slcm.manipal.edu/sendtoportal
4. *Annual Fee Payment for the Academic Year 2025-26*. https://jaipur.manipal.edu/img/pdf/Notification_Annual-Fee-Payment-AY-2025-26.pdf
5. *About MUJ - Manipal University Jaipur*. http://jaipur.manipal.edu/about-muj.php
6. *Standard Operating Procedure - Manipal University Jaipur*. https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf
7. *Manipal Academy of Higher Education - MU SLcM*. http://slcm.manipal.edu/
8. *Manipal Academy of Higher Education Collaborates with Salesforce to Advance its AI-Driven University Transformation - Salesforce*. http://salesforce.com/in/news/press-releases/2026/03/26/manipal-university-ai-transformation
9. *‏Zeeshan Khalandar‏ - ‏IT - Manager at Manipal Academy of ... LinkedIn · Zeeshan Khalandar 680+ followers*. https://ae.linkedin.com/in/zeeshan-khalandar-865920136
10. *Himanshu Upadhyay – C/C++/Python/RTOS/Avionics ... LinkedIn · Himanshu Upadhyay Ca. 400 Follower*. https://de.linkedin.com/in/himanshu-upadhyay-85a451a2
11. *‏Manipal University Dubai‏ - ‏School of Engineering and IT‏ | LinkedIn*. https://ae.linkedin.com/in/manipaldubai-soeit
12. *Nitin Sharma - Jaipur, Rajasthan, India | Professional Profile*. https://in.linkedin.com/in/nitin-sharma-3a65751b
13. *Rakesh Sharma - Director @Pens.com | AI initiatives ...*. http://linkedin.com/in/rakesh-sharma-46b21451
14. *Himanshu Upadhyay - Project Manager in Manipal Academy of ...*. https://in.linkedin.com/in/himanshuupadhyay
15. *Manav Khanna - Jaipur, Rajasthan, India | Professional ...*. https://in.linkedin.com/in/manav-khanna-3b2024218
16. *Manipal University - mujslcm.jaipur.manipal.edu*. https://mujslcm.jaipur.manipal.edu/Home/Index
17. *Rakesh Sharma R Tagore - SRE | Redhat, Oracle Linux*. http://linkedin.com/in/linuxrsharma
18. *Himanshu Upadhyay - Technical Project Manager LinkedIn · Himanshu Upadhyay Ca. 1890 Follower*. https://in.linkedin.com/in/himanshu-upadhyay-84b66572
19. *Rakesh Sharma - Principal Software Engineer @ Red Hat*. http://linkedin.com/in/rakesh-sharma-5a658a78
20. *Frequently Asked Questions and Contacts for SLCM Registration*. https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf
21. *Rahul Sharma*. http://linkedin.com/in/rahul-sharma-986a831a4
22. *NITIN SHARMA - Student at Manipal University Jaipur*. https://in.linkedin.com/in/nitin-sharma-6a82921bb
23. *Rakesh Sharma*. http://linkedin.com/in/rakesh-sharma-9450189b
24. *Sharma Rahul - Software Engineer at Manipal University Jaipur ...*. https://in.linkedin.com/in/sharma-rahul-929b06218
25. *Rahul Sharma - Assistant Professor | SAP BW Consultant ...*. https://in.linkedin.com/in/rahul-sharma-b978b693
26. *HIMANSHU UPADHYAY - Manhattan consultant | LinkedIn*. https://in.linkedin.com/in/himanshu-upadhyay-9510821a
27. *Poornima Bhat - Student at MIT, Manipal LinkedIn · Poornima Bhat 7 followers*. https://in.linkedin.com/in/poornima-bhat-5ab486154
28. *Manav Nand*. http://linkedin.com/in/manav-nand-3b125511b
29. *Poornima Vishwaradhya*. https://linkedin.com/in/poornima-vishwaradhya-a0b95b22
30. *Nitin Agarwal - Manipal University Jaipur | LinkedIn*. https://in.linkedin.com/in/nitin-agarwal-aa9549209
31. *Nitin kumar - Manipal University Jaipur | LinkedIn*. https://in.linkedin.com/in/nitin-kumar-116b58380
32. *Rakesh Sharma - Executive Director - "Improving Overall ...*. http://linkedin.com/in/rakeshsharma0110
33. *Rahul Sharma - Design engineer | LinkedIn*. https://in.linkedin.com/in/rahul-sharma-1b3673193
34. *Manav Prem Nand - Software Engineer | Ex-Infosys Intern*. http://linkedin.com/in/manav-prem-nand-aa7710266
35. *Rahul Sharma - -- | LinkedIn*. https://in.linkedin.com/in/rahul-sharma-7a2448264
36. *Contents*. http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf
37. *Manju Muthamadhu*. https://linkedin.com/in/manju-muthamadhu
38. *Rashmi Acharya*. https://linkedin.com/in/rashmi-acharya-54900528
39. *DEVESH MEENA*. https://linkedin.com/in/devesh-meena-a1a37a377
40. *rakesh sharma*. https://linkedin.com/in/rakesh-sharma-76890172
41. *Sumanth Suvarna*. https://linkedin.com/in/sumanth-suvarna-212738199
42. *Sumanth Suvarna*. https://linkedin.com/in/sumanth-suvarna-767a82171
43. *Lavi Chauhan*. https://linkedin.com/in/lavi-chauhan-bb002b21b
