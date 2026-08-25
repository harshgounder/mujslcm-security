# Identifying the Vendor Behind Manipal's SLCM

## Executive Summary

- **Layered Architecture, Not One Vendor**: The public record does not support describing MUJ SLCM as one off-the-shelf product from one vendor. The strongest model separates the student-facing MUJ web application, institutional development and support, a possible historical SAP academic core, campus-specific deployments, Microsoft identity, and the newer Salesforce modernization -> document these as separate layers rather than writing "SLCM vendor: X."

- **Direct In-House Attribution**: An official MAHE SIS route says, "Designed and Developed by Information Systems Department, Manipal Academy of Higher Education" [2]. The current SIS portal separately credits MAHE's "Department of Digital and Information Technology" [12] -> treat Manipal's internal information-technology organization as the strongest documented developer of the adjacent SIS presentation layer, while labeling its extension to MUJ SLCM as an inference.

- **SAP Is the Strongest Historical Product Lead**: A self-reported professional profile says SAP SLcM was implemented "across Manipal Education entities" in 2012 and describes configuration, migration, development, testing, deployment, and support [21]. A second profile reports configuring SAP SLcM processes at Manipal Global Education Services from 2011, including admission, calendars, module booking, records, reports, and graduation [22] -> investigate SAP as historical core ERP lineage, but do not claim that the present MUJ portal has a SAP backend without documentary confirmation.

- **MUJ Remains Unattributed**: The public MUJ page brands itself "WELCOME TO MUJ PORTAL" and exposes student and parent sign-in, but it does not publish a software-vendor credit [10]. Its captured public form uses a verification token, posts to the MUJ host, loads jQuery validation scripts, and sends password recovery to Microsoft's password-reset service [10] -> these are framework and identity clues, not proof of ERP authorship.

- **Campus Names Do Not Prove a Shared Binary**: MAHE publicly calls its main service SIS, MUJ calls its service MUJ Portal, Dubai's official site links to `slcm.manipaldubai.com`, and the Malaysia portal uses "Scholar E-Mail ID" with student and parent sign-in [12][10][14][15] -> treat SLCM as an institutional capability and naming family, not necessarily a single codebase deployed unchanged everywhere.

- **Salesforce And Deloitte Are Current Modernization Partners**: Salesforce says MAHE will modernize SLCM with Agentforce Education, Agentforce, Data 360, MuleSoft, and Tableau, while Deloitte will implement and integrate the platform [4]. MAHE says its MAGIC program began from a digital-transformation effort initiated in 2023 and initially places five AI agents inside SLCM [6] -> attribute the new MAHE transformation to Salesforce and Deloitte, not the creation of the older MUJ ASP.NET application.

- **Comviva Is A Poor Fit**: Comviva's official corporate page describes telecommunications, payments, and financial-service products such as PreTUPS, mobiquity Money, TerraPay, and YABX, but no higher-education SLCM product or Manipal deployment [26] -> eliminate Mahindra Comviva as a supported candidate unless a contract, case study, or code-level attribution emerges.

- **Manipal Technologies Is Name-Proximity, Not Attribution**: Manipal Technologies lists Education among several target sectors and describes commercial, cards, digital, financial, research, and secure business units, but its reviewed pages name no higher-education SLCM product or MUJ deployment [1][24] -> do not infer authorship merely from the shared "Manipal" name.

- **JAIN And Unikul Are False-Positive Risks**: A JAIN University case page identifies DigiiCampus as its integrated learning-management system [27]. Unikul markets a distinct Microsoft Dynamics 365-based SLCM product that can replace SAP HER or PeopleSoft, but its public overview does not name Manipal [25] -> generic use of "SLCM" is not a trademark-level identifier.

- **Decision**: The best-supported formulation is: "MUJ's visible SLCM portal appears Manipal-controlled and probably custom-developed or substantially customized; SAP SLCM is credible historical lineage elsewhere in the Manipal education ecosystem; the exact current MUJ backend vendor is not publicly established; MAHE's new modernization is Salesforce with Deloitte." Confidence is **moderate** for the MUJ custom/in-house assessment, **low** for a specifically MUJ-to-SAP backend attribution, and **high** for the 2026 MAHE Salesforce/Deloitte roles.

## Scope, Safety, And Evidence Standard

This report uses public, passive material only. It does not log in, submit credentials, bypass access controls, enumerate protected records, scan the hosts, test vulnerabilities, or recommend unauthorized access. The relevant public sources are university pages, vendor product pages, a university compliance document, public portal presentation content, certificate and page metadata supplied in the research context, and self-reported professional profiles.

The requester supplied a starting technical characterization of `mujslcm.jaipur.manipal.edu` as ASP.NET MVC 5.3 on .NET Framework 4.x and IIS 10 behind Akamai, with Microsoft 365 identity. That characterization is treated as an investigative premise, not as independently proven vendor attribution. The captured public page does support narrower observations: its login form contains `UserName`, `Password`, `EmailFor`, `LoginFor`, and `__RequestVerificationToken` fields; it posts to the same MUJ URL; it loads jQuery validation and unobtrusive-validation scripts; and its password-reset link points to `passwordreset.microsoftonline.com` [10]. None of those facts identifies the academic ERP behind the page.

I cannot provide private chain-of-thought. Instead, the report supplies an auditable evidence trail: the observations, source quality, competing hypotheses, contradictions, inference labels, and confidence judgments needed for another analyst to reproduce or challenge the conclusion.

| Evidence class | What it can establish | What it cannot establish |
|---|---|---|
| Explicit developer footer | Who claims to have designed and developed that particular page or system | Authorship of every backend or every campus deployment |
| Vendor case study or contract | Named product, customer, scope, and implementation role | Unstated custom components or later replacements |
| Product-portfolio page | Whether a candidate sells a relevant category of software | Whether MUJ bought or deployed it |
| Portal branding and URLs | Institution, audience, naming, and visible identity flow | Database, ERP core, software owner, or integration architecture |
| Public professional profile | Credible leads about historical work and technologies | First-party institutional confirmation or present deployment state |
| Shared term such as SLCM | A common functional category | Common vendor, common codebase, or common backend |

The analytical rule is therefore conservative: explicit attribution outranks name similarity; first-party institutional evidence outranks self-reported employment evidence; and a technology fingerprint is not promoted into a product or vendor conclusion.

## What MAHE Publicly Means By SLCM

MAHE's own ICT inventory provides the clearest functional definition. It says Student Life Cycle Management, or SLCM, replaced an older Academic Management System [7]. It describes SLCM as a complete suite covering attendance, internal marks, external marks, result publication, and broadcast messages [7]. The same document calls it a single-window system for students and parents dealing with academic matters [7].

Those functions explain why many unrelated universities and suppliers use the same abbreviation. SAP's current Student Lifecycle Management product covers admissions, enrollment, courses, grading, examinations, and student self-service [23]. Unikul also calls its product SLCM and describes enrollment, examinations, evaluations, results, academic administration, and finance [25]. The matching vocabulary shows a shared higher-education problem domain, not a unique brand marker.

This distinction matters because Manipal's visible interfaces and possible academic core may have different authors. A university can build a .NET portal, authenticate through Microsoft, call a packaged student-records system, and use another vendor for analytics or workflow integration. A footer on the portal would then identify the portal author but not necessarily the package vendor. Conversely, an SAP consultant's profile could identify a core implementation while saying nothing about who built the public-facing web application.

| SLCM layer | Representative function | Best public evidence | Attribution status |
|---|---|---|---|
| Student-facing portal | Student or parent sign-in and presentation | MUJ public portal [10] | Manipal-branded; vendor not named |
| Academic process suite | Attendance, marks, results, messages | MAHE ICT inventory [7] | MAHE capability; product vendor not named |
| Main-campus SIS | Student and parent information service | MAHE SIS description [12] | MAHE internal department credited [12] |
| Historical packaged core | Admission through graduation, records, calendars, module booking | Public Manipal Global professional evidence [21][22] | SAP SLCM is credible, but not confirmed for current MUJ |
| Identity and account recovery | SAML or Microsoft password reset | MUJ page and MAHE modernization endpoint [10][16] | Microsoft identity service; not ERP authorship |
| Current transformation | Agents, integration, analytics, lifecycle unification | Salesforce and MAHE announcements [6][4] | Salesforce products; Deloitte implementation |

The decision-ready takeaway is that "SLCM" should be modeled as an ecosystem label. Asking for one vendor without first specifying portal, ERP core, identity, hosting, analytics, or implementation partner produces false confidence.

## Four Campus Names Point To A Family, Not One Deployment

The main MAHE campus currently presents its public service as the Student Information System. The official SIS page says it was conceived for the information needs of MAHE students and parents and provides student/parent and administrator/faculty login paths [12]. Its footer credits the Department of Digital and Information Technology [12]. A separate SIS login route carries the older or alternate attribution "Information Systems Department, Manipal Academy of Higher Education" [2].

MUJ's public host instead says "WELCOME TO MUJ PORTAL" and offers parent and student sign-in [10]. The captured page does not publish an ERP product name or vendor. Its Microsoft password-reset link and ASP.NET-style request-verification token support an identity and web-framework assessment, but they do not bridge the evidentiary gap to SAP, Salesforce, Unikul, Manipal Technologies, or another backend [10].

MAHE Dubai's official university page links its "Student Portal" to `https://slcm.manipaldubai.com/` [14]. A public professional profile from the Dubai campus separately describes responsibility for "In house applications, App's and SLCM" and leading the local IT team [20]. That language supports local operational ownership, but it neither names a product vendor nor proves that Dubai and MUJ use identical software.

The Malaysia-facing portal uses "Scholar E-Mail ID" and provides separate student and parent sign-in paths [15]. Classic MAHE SLCM points users into the Manipal institutional web estate but exposes no vendor or developer credit in the reviewed public content [11].

| Campus or context | Public name | Public URL | Identity or audience clue | What is proven |
|---|---|---|---|---|
| MAHE main campus | Student Information System, SIS | `https://sis.manipal.edu/` | Student/parent and administrator/faculty paths [12] | Internal MAHE department is credited [12] |
| MAHE classic | MU SLcM | `https://slcm.manipal.edu/` | Institutional Manipal link [11] | No public vendor credit in reviewed page [11] |
| Manipal University Jaipur | MUJ Portal | `https://mujslcm.jaipur.manipal.edu/` | Student and parent sign-in [10] | Manipal branding; vendor not disclosed |
| MAHE Dubai | Student Portal / SLCM host | `https://slcm.manipaldubai.com/` | Linked from official Dubai page [14] | Official campus relationship, not shared codebase |
| Manipal Malaysia | SLCM Student Portal | `https://student.manipal.edu.my/` | Scholar email, student and parent sign-in [15] | Campus-specific identity language |
| MAHE modernization | SLCM plus MAGIC | `https://maheslcmtech.manipal.edu/` | Redirect exposes a Microsoft tenant SAML path [16] | Microsoft authentication relationship, not ERP origin |

**Inference, moderate confidence:** The repeated functional label and related institutional domains suggest a Manipal-wide SLCM/SIS service family. They do not establish one executable, one database, one vendor contract, or one release train across all campuses.

## In-House Development And SAP Can Both Be True

The strongest direct authorship evidence is the MAHE SIS footer. One route says "Designed and Developed by Information Systems Department, Manipal Academy of Higher Education" [2]. The current SIS page credits the Department of Digital and Information Technology [12]. It is plausible that these labels represent organizational evolution or two related internal units, but no reviewed source expressly documents a rename. That relationship must therefore remain an inference.

The footer proves authorship only for the SIS page or system on which it appears. It does not expressly say that the department wrote `mujslcm.jaipur.manipal.edu`, nor does it say that every academic business rule and record resides in internally written software. The MUJ page itself gives no developer attribution [10]. Accordingly, "MAHE ISD built all SLCM everywhere" would overstate the source.

SAP nevertheless emerges as the strongest historical packaged-product lead. Adrija Sen's public professional profile says that work at Manipal Global Educational Service in 2012 involved "Implementation of SAP SLcM across Manipal Education entities" and covered requirements, configuration, master data, migration, development, testing, deployment, and support [21]. Poornima Vishwaradhya's profile reports configuring SAP SLcM at Manipal Global Education Services from March 2011, including academic structures, calendars, admission, event planning, module booking, student records, reports, and graduation [22].

A more recent MAHE project-manager profile says the person led and mentored an SLCM support-development team while managing ERP development and Microsoft Power Platform work [18]. This is consistent with an institution maintaining substantial custom software and integrations around an ERP. Because these are self-reported LinkedIn-derived records rather than MAHE contracts or SAP customer stories, they should be treated as corroborating evidence, not final proof.

| Hypothesis | Supporting evidence | Contradiction or limitation | Assessment |
|---|---|---|---|
| Entire ecosystem is internally written | MAHE SIS directly credits an internal department [2][12] | SAP implementation profiles describe packaged SLCM work [21][22] | Too broad |
| Entire ecosystem is standard SAP | Multiple profiles describe SAP SLcM across Manipal entities [21][22] | MUJ presents a custom Manipal portal; no MUJ-to-SAP document was found [10] | Too broad |
| Custom portal over packaged or mixed core | Internal page authorship plus SAP implementation and support-team evidence [2][18][21] | No public architecture diagram confirms the interfaces | Best historical model, but partly inferred |
| Every campus uses the same backend | Common SLCM naming and related domains | Different portal names, identity language, and campus operations [14][15][12] | Unsupported |

**Inference, moderate confidence:** Manipal likely exercised substantial internal engineering and operational control over its presentation and integration layers while using or historically using SAP SLCM in at least some Manipal Education entities. **Inference, low confidence:** MUJ specifically may share that SAP lineage, but the reviewed public record does not prove it.

## Candidate Audit: SAP Leads Historically, Named Alternatives Do Not

### SAP Student Lifecycle Management

SAP is the only mature higher-education product candidate with Manipal-specific implementation evidence in the reviewed public professional record. SAP's own page confirms that Student Lifecycle Management is an ERP product covering the student journey, admissions, enrollment, courses, grading, and examinations [23]. The Manipal-specific profiles align closely with those functions [21][22]. The limitation is source quality and scope: SAP's public product page does not list Manipal as a customer, and the profiles refer to Manipal Global or Manipal Education entities rather than explicitly to the current MUJ host.

### Manipal Technologies Limited

Manipal Technologies is a plausible candidate by corporate-name proximity and because its site lists Education among target sectors [24]. Its reviewed corporate page, however, describes commercial, cards, digital, emerging, financial, research, and secure business units, with an emphasis on transactions and communications [24]. Its Education page says the company has served that segment for decades but names no SLCM product, higher-education ERP, or MUJ deployment [1]. Shared group history or geography is not product attribution.

### Mahindra Comviva

Comviva's public portfolio is centered on communication-service providers, telecommunications platforms, digital commerce, payments, and financial services [26]. The named products include PreTUPS, mobiquity Money, TerraPay, and YABX [26]. The reviewed page names neither a university ERP nor Manipal SLCM. Comviva is therefore a weak candidate generated by acronym or corporate-association noise rather than evidence.

### JAIN or JGI

The JAIN lead also appears to arise from generic education-portal vocabulary. A current JAIN University case page says JAIN integrated DigiiCampus' learning-management system and mentions choice-based course registration [27]. That is evidence about JAIN's own environment, not Manipal's. No reviewed source connected JAIN/JGI to MUJ SLCM development, licensing, hosting, or support.

### Unikul Campus Dynamix

Unikul is a real SLCM supplier. Its overview describes a Microsoft Dynamics 365-based platform spanning enrollment, examinations, evaluations, results, academics, finance, portals, and mobile applications [25]. A product page describes an unnamed higher-education brand in Dubai Academic City that replaced SAP with Campus Dynamix for admissions, finance, examinations, and evaluation [3].

Because MAHE Dubai is in Dubai Academic City and has an SLCM portal, that customer story is a noteworthy lead. **Inference, very low confidence:** the unnamed institution could be MAHE Dubai. The source does not name the customer, while searches of the reviewed Manipal and Unikul pages produced no explicit cross-reference. It would be analytically improper to convert geographic fit into identification.

| Candidate | Has an SLCM or adjacent education product? | Manipal-specific positive evidence | Principal gap | Status |
|---|---|---|---|---|
| MAHE ISD / Digital and IT | Yes, internally credited SIS | Direct developer footer [2][12] | Footer is not on MUJ page and does not identify backend | Strong for institutional presentation layer |
| SAP Student Lifecycle Management | Yes [23] | Two professional profiles describe Manipal implementation and configuration [21][22] | No first-party MUJ contract, architecture, or current customer story | Strongest historical packaged-core candidate |
| Salesforce plus Deloitte | Yes, current education and integration platform | Explicit MAHE modernization announcement [4] | Modernization does not prove legacy MUJ authorship | Confirmed for new MAHE program |
| Unikul Campus Dynamix | Yes [25] | Unnamed Dubai Academic City customer replaced SAP [3] | Customer is not named; no MUJ link | Interesting Dubai lead, unconfirmed |
| Manipal Technologies | Education sector listed [1][24] | No product or deployment attribution found | Name proximity only | Unsupported for MUJ SLCM |
| Mahindra Comviva | Telecom and financial platforms [26] | None in reviewed sources | Product-market mismatch | Poor fit |
| JAIN/JGI | JAIN uses DigiiCampus LMS [27] | None | Different institution and platform | Unsupported |

The candidate audit therefore does not yield one universal vendor. It yields different credible actors at different layers and times.

## The 2023-2026 Transition Names Salesforce And Deloitte Precisely

MAHE's own MAGIC announcement says its digital-transformation program began in 2023 [6]. It says MAGIC, the MAHE Agentic Intelligent Console, is being implemented with technology partners including Microsoft, Salesforce, Deloitte, PwC, and Hitachi [6]. The initial design places five AI agents in SLCM for timetable creation, attendance management, examination planning, and performance insights [6].

Salesforce's announcement is more specific about commercial roles. MAHE will use Agentforce Education, Agentforce, Data 360, MuleSoft, and Tableau [4]. Agentforce Education is intended to unify the student lifecycle, MuleSoft will connect existing student, learning, and document systems, Tableau will deliver analytics, and Agentforce will support activities such as student queries and admissions [4]. Deloitte is explicitly the implementation partner for platform deployment and cross-system integration [4].

The word "existing" is important. Salesforce says MuleSoft will connect MAHE's existing systems rather than saying Salesforce originally built every one of them [4]. The announcement therefore supports a transition architecture: legacy or existing systems continue to matter while Salesforce products add lifecycle unification, integration, analytics, and agentic functions.

| Role | Named actor | Publicly stated scope | Attribution limit |
|---|---|---|---|
| Program owner | MAHE | MAGIC and SLCM modernization [6][4] | Does not identify every legacy component |
| Education platform and agents | Salesforce | Agentforce Education, Agentforce, Data 360 [4] | New modernization role, not proof of old MUJ authorship |
| Integration | MuleSoft | Connect student, learning, and document systems [4] | Does not identify those systems' original vendors |
| Analytics | Tableau | Dashboards and analytics [4] | Analytics layer only |
| Implementation partner | Deloitte | Deployment and integration across systems [4] | Implementation is distinct from institutional ownership |
| Identity clue | Microsoft | MUJ password reset and MAHE SAML destination [10][16] | Authentication is not the student-records product |

**Inference, high confidence:** MAHE is moving from a mixed or traditional estate toward a Salesforce-centered integration and engagement layer rather than performing a simple one-for-one replacement of a single web application.

## Passive Technical Evidence: Useful Boundaries, Not Vendor Proof

The MUJ portal capture shows a conventional server-rendered login application. Its public form contains an anti-forgery-style `__RequestVerificationToken`, username and password inputs, same-origin POST behavior, jQuery 1.10.2, jQuery Validation, and unobtrusive validation scripts [10]. Those observations are consistent with the requester's ASP.NET MVC premise, but the page capture does not establish MVC package version 5.3, .NET Framework patch level, IIS version, source-code owner, or database product.

The password-reset destination is Microsoft's online password-reset service [10]. The newer MAHE SLCM endpoint exposes a Microsoft tenant SAML URL, although the captured request failed at the tunnel rather than completing authentication [16]. These observations support Microsoft as an identity provider. They do not show that Microsoft wrote the SLCM business application.

Akamai, IIS, TLS issuance, and Microsoft 365 occupy still other layers. Even if independently confirmed, CDN or reverse-proxy routing would identify traffic delivery, IIS would identify the web server, and Microsoft 365 would identify identity or productivity services. None would answer who supplied the student-records ERP. The same separation applies to an ASP.NET front end: organizations routinely build custom portals around packaged systems.

| Observation | Defensible conclusion | Unsafe overreach to avoid |
|---|---|---|
| `__RequestVerificationToken` and unobtrusive validation [10] | Microsoft web-framework conventions are visible | "Microsoft is the SLCM ERP vendor" |
| Microsoft password-reset URL [10] | Microsoft account-recovery service is integrated | "SLCM is a Microsoft Dynamics product" |
| Microsoft SAML destination [16] | MAHE's newer endpoint uses a Microsoft identity path | "Salesforce, SAP, or Unikul is ruled in or out" |
| MUJ branding and same-origin form POST [10] | MUJ controls the visible service identity | "MUJ wrote every backend component" |
| MAHE SIS developer footer [2][12] | MAHE's internal technology department developed that SIS interface or system | "The footer proves every campus uses identical code" |
| SAP professional evidence [21][22] | SAP SLCM was implemented or configured in Manipal Education contexts | "Current MUJ definitely runs SAP" |

For a university security club, the responsible next step is documentary, not technical intrusion. Ask MUJ's authorized IT or data-protection contact for an approved architecture summary, software bill of materials, current ERP product name, implementation partner, and campus scope. Procurement records, contracts, privacy notices, and official change-management documents could resolve the remaining attribution gap without interacting with protected application functions.

## Synthesis: Ownership, Product, Operation, Identity, And Hosting Diverge

The evidence converges only when the word "vendor" is decomposed. At the presentation layer, the portals are institution-branded and the adjacent MAHE SIS expressly credits an internal department [2][12]. At the historical academic-core layer, public professional records point to SAP SLCM implementation and configuration across Manipal Education entities [21][22]. At the campus-operations layer, Dubai staff describe responsibility for in-house applications and SLCM [20]. At the current transformation layer, Salesforce supplies named products and Deloitte implements them [4]. Microsoft appears at the identity layer [10][16].

| Dimension | In-house MAHE/MUJ model | Historical SAP model | Salesforce/Deloitte modernization | Alternative-vendor model |
|---|---|---|---|---|
| Mechanism | Custom portal, SIS, support, and integration engineering | Packaged student-lifecycle processes and master data | Unified education engagement, agents, APIs, and analytics | Off-the-shelf SLCM or adjacent services |
| Best evidence | Direct MAHE developer footer [2][12] | Manipal-specific professional records [21][22] | First-party and vendor announcements [6][4] | Candidate product pages only [26][24][25] |
| Scope | Proven for MAHE SIS; inferred for MUJ portal lineage | Proven only as historical work in Manipal Education contexts | Explicitly MAHE modernization | No explicit MUJ deployment |
| Time horizon | Legacy and continuing institutional capability | Strongest evidence begins in 2011-2012 | Transformation begun in 2023, publicly detailed in 2026 | Unestablished |
| Trade-off | Custom control but institutional maintenance burden | Mature academic functions but integration complexity | Modern engagement and integration, with transition complexity | Product fit varies; attribution absent |
| Principal uncertainty | Whether MUJ used the same internal development organization | Whether current MUJ still uses SAP underneath | Exact replacement boundary and campus rollout | Whether any candidate has an undisclosed contract |

The central tension is not "in-house versus vendor." A system can be internally designed at the portal layer and externally supplied at the ERP layer. The direct ISD footer and the SAP profiles therefore do not cancel each other; they describe potentially complementary responsibilities. Salesforce's emphasis on connecting existing systems further supports, but does not prove, this mixed-estate interpretation [4].

A second tension is campus scope. The shared SLCM name suggests common institutional concepts, yet main-campus SIS, MUJ Portal, Dubai SLCM, and Malaysia's Scholar Email interface expose different names and identity language [10][14][15][12]. That divergence argues against assuming identical implementations.

A third tension is chronology. Historical SAP evidence does not identify the current MUJ backend, while the new Salesforce program does not retroactively identify the legacy portal's author. A precise report must keep those time periods separate.

## VERDICT

**Primary verdict:** The vendor or product behind the current MUJ SLCM backend is **not publicly established by the reviewed evidence**.

**Most likely architecture, explicitly labeled as inference:** `mujslcm.jaipur.manipal.edu` is probably a Manipal/MUJ-controlled custom or heavily customized web application, maintained within the institution's information-technology ecosystem. That inference rests on MUJ-specific branding and custom login behavior [10], plus direct in-house developer attribution on the adjacent MAHE SIS [2][12]. The attribution is not printed on the MUJ page itself, so the confidence is **moderate, approximately 70%**.

**Historical product verdict:** SAP Student Lifecycle Management is the **strongest evidenced packaged-core lineage** in the broader Manipal Education ecosystem. Public professional records describe SAP SLcM implementation across Manipal Education entities in 2012 and detailed SAP SLcM configuration work beginning in 2011 [21][22]. Because no first-party record ties the present MUJ host directly to SAP, confidence that SAP existed somewhere in the historical Manipal education estate is **moderate-high**, while confidence that it is the current MUJ backend is **low, approximately 30%**.

**Current transformation verdict:** Salesforce is a confirmed MAHE modernization technology provider, and Deloitte is the confirmed implementation partner [4]. Confidence in that attribution is **high, above 90%**. This finding concerns MAHE's current transformation program and should not be rewritten as "Salesforce built the legacy MUJ SLCM."

**Alternative-candidate verdict:** The reviewed evidence does not support Mahindra Comviva, Manipal Technologies, JAIN/JGI, or Unikul as the developer of the MUJ portal. Comviva's portfolio is centered on telecom and financial platforms [26]; Manipal Technologies names Education but no SLCM product [1][24]; JAIN's cited environment uses DigiiCampus [27]; and Unikul's Manipal connection remains unproven despite an intriguing unnamed Dubai customer story [3][25]. Confidence that these candidates are **currently unsupported by public evidence** is **high**; that is not the same as proving that no undisclosed contract exists.

The recommended club-safe wording is:

> "Public evidence indicates that Manipal internally developed at least its MAHE SIS layer and has operated substantial custom SLCM support and integration functions. SAP SLCM has credible historical implementation evidence across Manipal Education entities, but the current MUJ backend is not publicly confirmed. MAHE's newer SLCM modernization uses Salesforce products with Deloitte as implementation partner. No reviewed public source attributes MUJ SLCM to Comviva, Manipal Technologies, JAIN/JGI, or Unikul."

## References

1. *Education - Manipal Technologies Limited*. https://manipaltechnologies.com/education/
2. [
	SIS
](https://sis.manipal.edu/studloginSLCM.aspx)
3. *SLCM for Universities – Campus Dynamix*. https://campusdynamix.com/slcm-for-universities
4. *Manipal Academy of Higher Education Collaborates ... - Salesforce*. https://www.salesforce.com/in/news/press-releases/2026/03/26/manipal-university-ai-transformation/
5. *Future-Ready Digital Solutions & Telecom Products | Comviva*. http://comviva.com/products-solutions
6. *MAHE Introduces ‘MAGIC’ to Power AI-Driven Academic and ...*. https://www.manipal.edu/mu/news-events/mahe-introduces--magic--to-power-ai-driven-academic-and-administ.html
7. *Contents*. http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf
8. *PowerPoint Presentation*. https://www.manipal.edu/content/dam/manipal/mu/documents/MAHE%20IOE%20Annual%20Self%20Report%202025.pdf
9. *Student Portal Login- MAHE (Manipal Academy Of Higher Education)*. https://www.manipal.edu/mu/academics/student-portal.html
10. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
11. [
	MU SLcM
](https://slcm.manipal.edu/)
12. [
	SIS Portal
](https://sis.manipal.edu/)
13. *Annual Reports | Manipal Academy of Higher Education*. https://www.manipal.edu/mu/important-links/mu-annual-reports.html
14. *Manipal University Dubai | CAA-Accredited International University in UAE*. http://manipaldubai.com/
15. *Portal Framework*. https://student.manipal.edu.my/
16. *login.microsoftonline.com*. https://maheslcmtech.manipal.edu/
17. [Private entity search](parallel://private-entity-search)
18. *Himanshu Upadhyay*. https://linkedin.com/in/himanshuupadhyay
19. *Rashad Muhammed*. https://linkedin.com/in/rashad-muhammed-a6179233
20. *Zeeshan Khalandar*. https://linkedin.com/in/zeeshan-khalandar-865920136
21. *Adrija Sen*. https://linkedin.com/in/adrija-sen-91631110
22. *Poornima Vishwaradhya*. https://linkedin.com/in/poornima-vishwaradhya-a0b95b22
23. *SAP Student Lifecycle Management for SAP S/4HANA Cloud Private Edition*. http://sap.com/products/erp/student-lifecycle-management-for-sap-s4hana-cloud-private-edition.html
24. *Who We Are - Manipal Technologies Limited*. https://manipaltechnologies.com/who-we-are/
25. *Unikul - Home - Software Solutions*. https://unikul.com/overview
26. *Who We Are - Comviva*. http://comviva.com/corporate/who-we-are
27. *Jain-University*. https://digiicampus.com/jain-university
