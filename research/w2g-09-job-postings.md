# MUJ SLCM Job-Board OSINT: Public Evidence and Gaps

## Executive Summary

- **Direct-posting result**: The public evidence reviewed does not identify a direct Manipal University Jaipur job posting for SLCM, Manipal ERP, student-portal maintenance, or an equivalent application-support role. The strongest Naukri MUJ results are a Library Assistant listing and a Lab Technician/Instructor - 3D Lab listing, and their extracted descriptions do not mention SLCM, ERP, portal maintenance, or the requested Microsoft stack [20] [16]. **Action:** treat the requested technology profile as an uncorroborated research hypothesis, not as a job-board-confirmed architecture.
- **Portal confirmation**: The public MUJ SLCM landing page displays "WELCOME TO MUJ PORTAL" and sign-in labels including parent login [2]. **Action:** this confirms the public portal identity and user-facing scope, but not its framework, server, database, CDN, or identity provider.
- **MUJ careers signal**: The official MUJ careers page groups vacancies into academic, research, and non-academic categories and names schools and quality/compliance functions, but the inspected material does not state the requested stack or SLCM ownership [12] [12]. **Action:** monitor the official page and preserve dated snapshots when a technical vacancy appears.
- **Naukri signal**: Naukri exposes a MUJ company page and Jaipur search results, but the visible MUJ roles are not SLCM roles. The Library Assistant page lists library management, record keeping, library software, and MS Office; the 3D Lab role lists 3D CAD, additive manufacturing, and 3D printing [18] [16]. **Action:** do not infer that generic "computer skills" or "library software" means access to SLCM.
- **Indeed signal**: Indeed's public Jaipur search page is a keyword/search landing page, not evidence that Manipal University Jaipur is the employer. Its visible results include unrelated employers and roles such as sales, management, and operations; no SLCM, ERP, portal, or requested stack appears in the extracted evidence [11] [11]. **Action:** require an employer field or direct posting before attributing a role to MUJ.
- **LinkedIn signal**: The public LinkedIn query for "Manipal University Jaipur" returned zero jobs in the United States, while a broader "Manipal University IT" query returned a mixed search context rather than a direct MUJ technical vacancy [13] [17]. **Action:** regard LinkedIn as no-confirmation rather than proof that no such role exists globally; location and login/personalization limit coverage.
- **Technology result**: None of the inspected MUJ job-board or official career excerpts names ASP.NET MVC, .NET Framework, SQL Server, IIS, Microsoft 365, or a vendor for SLCM. The requested stack therefore remains unsupported by the job-posting corpus. **Action:** report each field as "not publicly stated" rather than filling it from the supplied system description.
- **Entity-separation risk**: Search results also surfaced MAHE, Manipal Dubai, Sikkim Manipal University, Manipal Technologies, Manipal Dot Net, generic ERP jobs, and unrelated universities. Those are not valid substitutes for MUJ SLCM evidence [18] [18] [6]. **Action:** keep MUJ, MAHE, Dubai, Sikkim, corporate Manipal entities, and third-party vendors in separate evidence buckets.
- **Security posture**: This report uses public pages and job-board text only. It does not test the portal, enumerate routes, attempt authentication, inspect protected content, or provide instructions for unauthorized access. **Action:** if the club needs confirmation, use responsible disclosure or obtain written authorization from the institution.

## Scope, Method, and Evidence Standard

The collection objective was narrow: identify public postings on LinkedIn, Naukri, and Indeed that explicitly connect MUJ or its student systems with SLCM, Manipal ERP, student-portal maintenance, or application-support work. Official MUJ and MAHE careers pages were used for corroboration, while public portal landing pages were used only to establish visible naming and user-facing labels. The evidence standard was deliberately conservative: a search result mentioning "Manipal University" was not treated as an employer relationship, and a technology appearing in the supplied research brief was not treated as source-confirmed.

The evidence ledger distinguishes four states. "Direct MUJ technical evidence" means a page identifies MUJ as employer and describes a technical role. "Related MUJ evidence" means the employer and institution are MUJ, but the role does not concern SLCM or the requested stack. "Generic/unrelated" means the page is a search landing page, a third-party vacancy, or an unrelated employer. "Other Manipal entity" means a Manipal-branded institution or company other than MUJ. This separation matters because Naukri's broad Manipal pages include Sikkim Manipal University and Manipal Technologies, while Indeed's keyword page includes unrelated Jaipur employers [18] [18] [11].

A separate limitation concerns the requested "chain-of-thought" field. I cannot provide private hidden chain-of-thought reasoning. Instead, this report gives a reproducible decision trail: query families, inclusion rules, exclusions, source URLs, extracted fields, confidence judgments, and unanswered questions. That is sufficient for a university club to audit the conclusion without exposing private internal reasoning.

The search corpus is also time-sensitive. Naukri and Indeed counts and listings change, and LinkedIn results depend on location, indexing, login state, and personalization. Therefore, the conclusion is "not found in the public corpus reviewed as of 2026-08-25," not an assertion that no internal, unindexed, expired, or recruiter-only vacancy ever existed.

## Exact Evidence Table: MUJ and Official Pages

| Source class | Exact URL | Public fact supported | SLCM/ERP or requested stack | Assessment |
|---|---|---|---|---|
| MUJ SLCM landing page | https://mujslcm.jaipur.manipal.edu/ | Page says "WELCOME TO MUJ PORTAL" and exposes sign-in and parent-login labels [2] | Not stated | Direct portal identity only |
| MUJ official careers | https://jaipur.manipal.edu/career-community.php | Page lists academic, research, and non-academic categories and MUJ departments/schools [12] | Not stated [12] | Official MUJ vacancy index, not SLCM evidence |
| MUJ career item | https://jaipur.manipal.edu/career-veiw.php?url=77%2Fapplications-now-open-for-faculty | TAPMI School of Business faculty posting [5] | Not stated [5] | MUJ, non-technical |
| MUJ career item | https://jaipur.manipal.edu/career-veiw.php?url=32%2Fapplications-now-open-for-faculty | MUJ faculty-position page [7] | Not stated [7] | MUJ, non-technical |
| MAHE vacancies | https://www.manipal.edu/mu/important-links/careers-mu/jobs-at-mahe-current-vacancies-.html | MAHE vacancies are organized under faculty, research, and non-academic categories [3] | Not stated [3] | MAHE, not MUJ |
| MAHE student portal | https://www.manipal.edu/mu/academics/student-portal.html | Public page describes student-portal registration/login and access to web services [8] | Not stated | MAHE portal context, not MUJ SLCM evidence |

The table shows what can safely be said: MUJ has a publicly visible portal branded as MUJ Portal, and MUJ has official career pages. It does not show that the portal is built with the stack in the research brief. The official career pages likewise do not identify a technical support team, vendor, or application owner in the extracted text [2] [12].

## Naukri Findings: Relevant MUJ Listings Without SLCM Disclosure

| Listing or page | Exact URL | Employer/entity | Role and public details | Requested indicators | Classification |
|---|---|---|---|---|---|
| MUJ Jaipur search page | https://www.naukri.com/manipal-university-jobs-in-jaipur | Manipal University Jaipur | Search page; visible MUJ results include Library Assistant and Lab Technician/Instructor - 3D Lab [20] [20] | No SLCM, ERP, portal maintenance, ASP.NET MVC, SQL Server, IIS, or vendor in extracted role evidence | Discovery page |
| Library Assistant | https://www.naukri.com/job-listings-library-manipal-university-jaipur-jaipur-0-to-5-years-040826029330 | Manipal University Jaipur | Jaipur; B.L.I.S/M.L.I.S; library management, record keeping, resource management; library software and MS Office [18] | No explicit SLCM, ERP, portal maintenance, or requested stack [18] | Related MUJ evidence |
| MUJ company page | https://www.naukri.com/manipal-university-jaipur-jobs-careers-4408504 | Manipal University Jaipur | The page lists two jobs, including Library Assistant and Lab Technician/Instructor - 3D Lab [16] | No requested stack or vendor [16] [16] | Related MUJ evidence |
| Lab Technician/Instructor - 3D Lab | https://www.naukri.com/manipal-university-jobs-in-jaipur | Manipal University Jaipur | Jaipur; 3D CAD modeling, DFAM, 3D printing, and 3D modeling; 5 days ago in the captured page [20] | No SLCM, ERP, portal maintenance, ASP.NET MVC, SQL Server, IIS, or vendor [20] | Direct MUJ technical evidence, but unrelated to SLCM |
| L&D Executive | https://www.naukri.com/job-listings-executive-learning-development-l-d-manipal-university-jaipur-jaipur-3-to-5-years-210726012927 | Manipal University Jaipur | Expired/search context; L&D role in Jaipur [21] | No named technology or SLCM/ERP/portal wording [21] | No usable SLCM evidence |

The important distinction is between "technical" and "SLCM technical." The 3D Lab role is technical in subject matter, but its stated technologies concern additive manufacturing, not web application operations [20]. The Library Assistant role does mention library software and MS Office, but those are functional tools in a library job, not evidence of the MUJ portal stack [18]. Inference that either role supports SLCM would be unsupported.

Naukri's broader Manipal results demonstrate why entity controls are necessary. The extracted page includes Sikkim Manipal University roles in Majhitar and a Manipal Technologies role in Udupi, each distinct from MUJ [18] [18]. These entries are useful as false-positive examples, not as vendor or staffing evidence for MUJ SLCM.

## Indeed Findings: Search-Keyword Association Is Not Employer Attribution

| Exact URL | What the page is | Visible result evidence | SLCM/stack result | Assessment |
|---|---|---|---|---|
| https://in.indeed.com/q-manipal-university%2C-jaipur-l-jaipur%2C-rajasthan-jobs.html | Public keyword/location search page [11] | Results include Foxoso Hospitality, Selenite Organisation, ATHARVA ORGANISATION, and roles such as sales and management [11] | No SLCM, ERP, student portal, ASP.NET MVC, SQL Server, IIS, Microsoft 365, team, or vendor for MUJ [11] | Generic/unrelated |
| https://in.indeed.com/q-manipal-university%2C-jaipur-l-jaipur%2C-rajasthan-jobs.html?start=10 | Second search-results page | Visible result includes High fly real estate group Associate role and sales duties [19] | No MUJ SLCM evidence | Generic/unrelated |
| https://in.indeed.com/jobs?q=Manipal+University+Jaipur | General Indeed query | Search result page, not a direct employer posting [15] | No direct MUJ technical posting identified in extracted evidence | Discovery only |

Indeed's page title and query terms can create a misleading association. A search for "Manipal University, Jaipur" does not establish that every returned employer works for MUJ, maintains its portal, or has a contractual relationship with it. The extracted result set explicitly contains unrelated employers and non-technical roles [11] [19]. That is why no Indeed result is included as a positive SLCM lead.

## LinkedIn Findings: Limited Public Visibility, No Positive Match

| Exact URL | Public result | Requested indicators | Assessment |
|---|---|---|---|
| https://www.linkedin.com/jobs/search/?keywords=Manipal%20University%20Jaipur | Page says it could not find a match for Manipal University Jaipur jobs in the United States [13] | No posting, stack, team, vendor, or SLCM wording | Negative result for that public query/location only |
| https://www.linkedin.com/jobs/search/?keywords=Manipal%20University%20IT | Broader public search context for Manipal University IT in the United States [17] | Not a direct MUJ employer posting in the extracted evidence | Mixed discovery result |
| https://www.linkedin.com/company/manipal-university-jaipur/ | Public MUJ company page was inspected [14] | No extracted direct SLCM vacancy or requested stack | No positive job evidence |

This is a weaker negative than the Naukri result because LinkedIn public pages may be location-specific, dynamic, login-gated, or incomplete. The correct conclusion is not "LinkedIn has no such role," but "the public LinkedIn pages retrieved for these queries did not expose one." Any future positive result should be captured from the direct LinkedIn job URL, with employer, location, date, and description preserved.

## Stack, Team, and Vendor Matrix

| Requested field | Public MUJ SLCM job-posting evidence found? | What the reviewed pages actually say | Safe conclusion |
|---|---|---|---|
| ASP.NET MVC | No | No inspected MUJ job page names ASP.NET MVC [12] [18] | Not publicly stated in reviewed postings |
| .NET Framework 4.x | No | No inspected MUJ job page names .NET Framework [12] [21] | Not publicly stated |
| SQL Server | No | No inspected MUJ job page names SQL Server [12] [11] | Not publicly stated |
| IIS | No | No inspected MUJ job page names IIS [12] [18] | Not publicly stated |
| Microsoft 365 identity | No | MS Office/Microsoft appears in the Library Assistant context, not as identity infrastructure [18] | Do not equate MS Office with Microsoft 365 identity |
| SLCM | Portal name only, not job requirement | MUJ page says "WELCOME TO MUJ PORTAL" [2] | Portal is publicly named; staffing/stack is not |
| Manipal ERP | No | No inspected MUJ job page names Manipal ERP [12] [11] | Not publicly stated |
| Student-portal maintenance | No | Public portal pages show user-facing labels; no maintenance vacancy was found [2] | Not publicly stated |
| Team name | No SLCM team | MUJ careers names academic schools and Quality & Compliance functions [12] [12] | No portal-operations team identified |
| Vendor | No MUJ SLCM vendor | Other search results include unrelated Manipal entities and generic vendors, which were excluded [6] [18] | Vendor unknown from this corpus |

This matrix is the principal answer to the requested requirements list. Every "No" means no source-stated evidence in the reviewed public corpus, not that the technology or team does not exist. The supplied architecture description may be accurate from another source, but it cannot be cited as a job-board finding here.

## Entity Confusion and False-Positive Analysis

Several findings could look relevant while failing the MUJ test. Manipal Dubai's public careers page links to a Dubai SLCM portal, but it is a Dubai institution and therefore does not establish MUJ ownership, staffing, or vendor identity. MAHE's SLCM page and student-portal page establish other Manipal portal contexts, but MAHE is not MUJ [8]. Sikkim Manipal University and Manipal Technologies are separately identified in Naukri results and have different locations and organizational identities [18] [18].

A second false-positive class is technology adjacency. A generic ERP job may mention ERP support, reports, or SQL Server, but unless the employer, customer, and posting text connect it to MUJ, it cannot identify the MUJ SLCM operator. Likewise, the existence of a public portal does not prove the framework inferred from a banner, URL, or browser-visible behavior. The report therefore does not convert the user's supplied "ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10 behind Akamai, Microsoft 365 identity" description into independent fact.

A third class is search-page inflation. Naukri and Indeed pages display large counts and aggregate many employers. A count is not a count of MUJ technical vacancies, and a query term is not a contract relationship. The Naukri page, for example, exposes a broad Jaipur result set, while the direct MUJ-specific evidence is limited to named roles such as Library Assistant and 3D Lab Instructor [20] [16].

## Unanswered Questions and Safe Follow-Up

| Unanswered question | Why public job-board evidence cannot answer it | Safe next step |
|---|---|---|
| Who operates MUJ SLCM? | No inspected posting names an owner or team | Ask MUJ for an official system-owner or support contact through published channels |
| Is the supplied ASP.NET MVC/.NET/IIS profile current? | No reviewed posting states it | Use authorized documentation, procurement records, or an institution-provided architecture statement |
| Is SQL Server the backing database? | No public posting states it | Do not infer from a generic Microsoft ecosystem; request confirmation from the institution |
| Is Microsoft 365 used for identity? | The reviewed page only shows public login labels; MS Office is not identity evidence [18] | Seek an official identity/integration statement |
| Is Akamai in front of the service? | The reviewed job pages do not name CDN or hosting providers | Treat as unverified in this job-board study |
| Which vendor maintains it? | No MUJ posting names a vendor; unrelated Manipal companies were excluded [6] [18] | Search public procurement/tender notices or request disclosure through proper channels |
| Was there an expired or recruiter-only posting? | Job boards can remove or personalize listings | Preserve direct URLs and dated public captures when found; do not bypass access controls |

The most useful next step is not more generic searching. It is a targeted, periodic watch of the MUJ official careers page and the Naukri MUJ company page, using exact role families such as application support, enterprise applications, MIS, systems administrator, and software developer. A positive lead should only enter the evidence table when the direct posting identifies MUJ and states the relevant system or duties.

## Synthesis

Across the evidence, four dimensions diverge. On **identity**, the MUJ portal is directly visible as "MUJ PORTAL," while the job corpus does not identify its operator [2]. On **scope**, the official MUJ careers page is broad and institution-wide, covering academic, research, and non-academic categories, whereas Naukri's strongest MUJ listings are function-specific and unrelated to portal operations [12] [18]. On **technology**, the user's supplied profile is detailed, but the public postings are silent; the evidence gap is therefore between system observation supplied in the brief and employment-market disclosure. On **vendor attribution**, the corpus contains multiple Manipal entities, but none safely links a vendor to MUJ SLCM [6] [18].

The non-obvious tension is that a visible and apparently important student portal can coexist with almost no public hiring language about its maintenance. That may reflect internal staffing, outsourced support, non-public requisitions, different terminology, or simply search-engine coverage. It does not distinguish among those explanations. The evidence supports only the narrower claim that public job boards did not expose the requested connection during this review.

The practical implication for a security club is methodological. Job boards are useful for organizational and technology clues only when the posting explicitly binds the employer, system, duties, and stack. They are poor evidence for an exact production architecture when the source is a search page or when the same brand spans multiple institutions. A defensible report should preserve this uncertainty rather than manufacture a vendor, team, or technology relationship from nearby results.

## VERDICT

**Finding:** No direct, publicly indexed MUJ job posting was located that explicitly mentions SLCM, Manipal ERP, student-portal maintenance, ASP.NET MVC, SQL Server, IIS, Microsoft 365 identity, a portal-operations team, or a vendor. The public MUJ SLCM page confirms only the user-facing portal name and sign-in labels [2]. The official MUJ career pages and Naukri MUJ results provide institution and role context but no requested SLCM stack disclosure [12] [18]. Indeed and LinkedIn produced no positive direct MUJ technical posting in the reviewed public results [11] [13].

**Confidence: Moderate for the bounded negative finding; low for any claim about the underlying architecture or vendor.** Confidence is moderate because multiple independent source classes and query families converged on official career pages, generic job-board pages, and unrelated results. It is not high because job boards are dynamic, indexed incompletely, and sometimes location- or login-dependent. The report should therefore be cited as "not found in the public corpus reviewed as of 2026-08-25," not as proof of nonexistence.

**Operational boundary:** all findings are from public pages. No authentication, probing, route enumeration, vulnerability testing, source-code retrieval, or access-control bypass was performed or recommended. Any follow-up involving the MUJ portal should be authorized in writing and handled through responsible disclosure.

## References and Exact URLs

| Citation IDs used | Exact URL |
|---|---|
| [2] | https://mujslcm.jaipur.manipal.edu/ |
| [12], [12] | https://jaipur.manipal.edu/career-community.php |
| [5] | https://jaipur.manipal.edu/career-veiw.php?url=77%2Fapplications-now-open-for-faculty |
| [7] | https://jaipur.manipal.edu/career-veiw.php?url=32%2Fapplications-now-open-for-faculty |
| [3] | https://www.manipal.edu/mu/important-links/careers-mu/jobs-at-mahe-current-vacancies-.html |
| [8] | https://www.manipal.edu/mu/academics/student-portal.html |
| [18], [18], [18] | https://www.naukri.com/manipal-university-jobs-in-jaipur |
| [16] | https://www.naukri.com/manipal-university-jaipur-jobs-careers-4408504 |
| [21] | https://www.naukri.com/job-listings-executive-learning-development-l-d-manipal-university-jaipur-jaipur-3-to-5-years-210726012927 |
| [11], [11] | https://in.indeed.com/q-manipal-university%2C-jaipur-l-jaipur%2C-rajasthan-jobs.html |
| [19] | https://in.indeed.com/q-manipal-university%2C-jaipur-l-jaipur%2C-rajasthan-jobs.html?start=10 |
| [15] | https://in.indeed.com/jobs?q=Manipal+University+Jaipur |
| [13] | https://www.linkedin.com/jobs/search/?keywords=Manipal%20University%20Jaipur |
| [17] | https://www.linkedin.com/jobs/search/?keywords=Manipal%20University%20IT |
| [14] | https://www.linkedin.com/company/manipal-university-jaipur/ |
| | http://manipaldubai.com/careers |
| | https://slcm.manipal.edu/ |
| [6] | https://web.manipal.net/mdn/careers/currentOpenings/applyforjob.php |

## References

1. [
	MU SLcM
](https://slcm.manipal.edu/)
2. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
3. *Current Job Vacancies | MAHE Careers*. https://www.manipal.edu/mu/important-links/careers-mu/jobs-at-mahe-current-vacancies-.html
4. *Online Bachelor and Master Programmes | Online Degree Programs in India | Online Manipal*. https://muj.onlinemanipal.com/
5. *Applications Now Open for Faculty Position- TAPMI School of Business | Manipal University Jaipur Career *. https://jaipur.manipal.edu/career-veiw.php?url=77%2Fapplications-now-open-for-faculty
6. *Manipal Dot Net Pvt Ltd.*. https://web.manipal.net/mdn/careers/currentOpenings/applyforjob.php
7. *Applications Now Open for Faculty Position | Manipal University Jaipur Career *. https://jaipur.manipal.edu/career-veiw.php?url=32%2Fapplications-now-open-for-faculty
8. *Student Portal Login- MAHE (Manipal Academy Of Higher Education)*. https://www.manipal.edu/mu/academics/student-portal.html
9. *Career - Manipal University Jaipur*. https://jaipur.manipal.edu/career.php
10. *Careers at MAHE | Work with Manipal University*. https://www.manipal.edu/mu/important-links/careers-mu.html
11. *2,000+ Manipal University, Jaipur जॉब, Jaipur, Rajasthan में एम्प्लायमेंट 25 अगस्त, 2026| Indeed*. http://in.indeed.com/q-manipal-university%2C-jaipur-l-jaipur%2C-rajasthan-jobs.html
12. *Career - Manipal University Jaipur Career*. https://jaipur.manipal.edu/career-community.php
13. *0 Manipal University Jaipur jobs in United States*. https://www.linkedin.com/jobs/search/?keywords=Manipal%20University%20Jaipur
14. *Manipal University Jaipur*. https://www.linkedin.com/company/manipal-university-jaipur/
15. *Manipal University Jobs, Employment in Jaipur, Rajasthan 25 अगस्त, 2026| Indeed*. https://in.indeed.com/jobs?q=Manipal+University+Jaipur
16. *Manipal University Jaipur Careers - 2 Manipal University Jaipur Jobs August 2026 - Naukri.com*. https://www.naukri.com/manipal-university-jaipur-jobs-careers-4408504
17. *Manipal University IT Jobs in United States (13 Open Roles) | LinkedIn*. https://www.linkedin.com/jobs/search/?keywords=Manipal%20University%20IT
18. *Manipal University Jobs - 12277 Manipal University Job Vacancies In August 2026 - Naukri.com*. https://www.naukri.com/manipal-university-jobs
19. *2,000+ Manipal University, Jaipur जॉब, Jaipur, Rajasthan में एम्प्लायमेंट 25 अगस्त, 2026| Indeed*. https://in.indeed.com/q-manipal-university%2C-jaipur-l-jaipur%2C-rajasthan-jobs.html?start=10
20. *Manipal University Jobs In Jaipur - 294 Manipal University Job Vacancies In Jaipur - Naukri.com*. https://www.naukri.com/manipal-university-jobs-in-jaipur
21. *Learning Executive Jobs In Jaipur - 14 Learning Executive Job Vacancies In Jaipur - Naukri.com*. https://www.naukri.com/job-listings-executive-learning-development-l-d-manipal-university-jaipur-jaipur-3-to-5-years-210726012927
