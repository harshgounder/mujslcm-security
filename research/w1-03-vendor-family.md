# Tracing Manipal's SLCM Vendor, Instances, and Shared Risk

## Executive Summary

- **Historical Vendor Lineage**: The strongest public evidence identifies the historical product as **SAP Student Lifecycle Management, or SAP SLcM**. A former Manipal Global Educational Service profile says SAP SLcM was implemented "across Manipal Education entities" and describes requirements, configuration, data migration, development, testing, deployment, planning, implementation, and support [10]. A second Manipal Global profile independently lists SAP SLcM configuration for admissions, academic structure, records, reports, graduation, training, and operational support [12]. -> Treat SAP as the historically verified product vendor, while treating Manipal Global as the group implementation and support organization.

- **MUJ Maintainer Is Not Publicly Named**: No first-party page, job advertisement, or MUJ-specific employee record found in this review names the original builder or present maintainer of the Manipal University Jaipur portal. The evidence supports group-level SAP lineage and internal Manipal support, but it does not prove which team currently owns MUJ's instance. -> Record the MUJ maintainer as "not publicly established," rather than assigning it to SAP, Salesforce, Deloitte, Crucia, ITL, Jain Group, or Manipal Technologies without qualification.

- **Internal Support Is Real**: A MAHE project manager's public profile says that, from February 2022, the role included managing ERP development and leading the support-development team for the SLCM project [9]. Separately, an MIT attendance page tells users to view attendance through `slcm.manipal.edu` and credits its own design and development to MAHE's Department of Digital and Information Technology [21]. -> The evidence favors an internally supported Manipal estate, even where SAP supplied the historical product core.

- **MUJ Has Two Near-Identical Public Entrances**: `https://mujslcm.jaipur.manipal.edu/` and `https://muj.slcm.jaipur.manipal.edu/` both present "WELCOME TO MUJ PORTAL" and equivalent sign-in behavior [18][16]. Their returned HTML uses the same Keen theme paths, jQuery generation, form names, and login scripts. -> Treat them as aliases or closely coupled deployments unless Manipal states otherwise.

- **MAHE And MUJ Are Not Proven To Share A Front End**: The classic MAHE page and Dubai page share the same old-style confirmation-dialog wording [20][17], while the MUJ pair returns a different Keen-themed login application. -> A finding on `slcm.manipal.edu` should not automatically be applied to MUJ. Transfer it only after component-level confirmation.

- **Dubai Is The Closest Classic Sibling**: `https://slcm.manipaldubai.com/` links back to the Dubai institution and exposes the same "Forgot Password?", "Confirmation", "Are You Sure?", and "No" sequence found in the MAHE classic family [17]. -> Prioritize MAHE classic and Dubai for shared-template review, ahead of MUJ.

- **MAHE Is Now In A New Technology Era**: In March 2026, Salesforce announced that MAHE would modernize SLCM using Agentforce Education, Agentforce, MuleSoft, and Tableau, with Deloitte as implementation partner [6]. The announced program includes 50+ AI agents over two years and covers MAHE's 40,000+ students from 60+ nations [6]. -> Do not call Salesforce the original MUJ vendor; treat it as MAHE's current modernization platform and Deloitte as its announced implementation partner.

- **Public Code Shows Integrability, Not A Proven Breach**: A deprecated community REST wrapper documented authenticated access to marks, attendance, and profile data [14]. MUJ projects automate feedback submission or replicate login, timetable, grades, and attendance functions [3][4]. -> These projects establish accessible workflows and third-party credential-handling surfaces, but they do not establish authentication bypass, unauthorized access, or a CVE.

- **Observed Problems Are Mostly Reliability And Workflow Issues**: Public student reports include a correct password being rejected at MUJ [13] and a paid fee remaining marked as pending in SLCM [11]. -> Investigate authentication resilience and financial-system synchronization, but label these reports anecdotal rather than verified vulnerabilities.

## 1. Scope, Terminology, and Evidence Logic

"SLCM" is overloaded. In this report, it means Manipal's Student Life Cycle Management environment, not unrelated companies whose initials are SLCM. MAHE's own documentation says Student Life Cycle Management replaced the older Academic Management System and provides attendance, internal marks, external marks, result publication, and broadcast messages as a single academic window for students and parents [5]. That functional definition anchors the product family.

Institutional boundaries matter. Manipal University Jaipur was launched in 2011 as a self-financed state private university [22]. MAHE, MUJ, Sikkim Manipal University, Dubai, and other Manipal entities are related through the wider education group, but a group relationship does not make their contracts, databases, support teams, or vulnerability status identical. The report therefore distinguishes an institution from a portal hostname and a shared business process from a shared codebase.

The evidence is classified as follows:

| Evidence class | What it can establish | What it cannot establish |
|---|---|---|
| Official institutional or vendor statement | Named platform, announced partner, intended scope, portal ownership | Undisclosed subcontractors or unannounced implementation details |
| Employee experience record | Direct implementation or support work associated with a named employer | Present contractual status or an employer's official legal position |
| Live public login page | Hostname, branding, visible workflow, page-template similarity | Backend database identity or authorization equivalence |
| Public source-code repository | Documented integrations, client behavior, technologies, limitations | Continued functionality, institutional approval, or a vulnerability by itself |
| Student forum report | A concrete user-observed symptom | Root cause, prevalence, exploitability, or official confirmation |
| Analyst inference | A bounded conclusion from multiple signals | A substitute for source-code, contract, or asset-owner confirmation |

This is the requested evidence-to-conclusion logic, not hidden chain-of-thought. Each material conclusion below states whether it is confirmed, supported, or inferred. No active probing, authentication attempt, credential use, or vulnerability exploitation was performed.

**Decision-ready insight:** The crucial analytical error to avoid is collapsing "same Manipal group," "same SAP lineage," "same SLCM name," and "same deployable code" into one claim. The public evidence supports the first three to different degrees; it does not support the fourth across every campus.

## 2. Vendor Lineage: SAP Core, Manipal Implementation, Salesforce Modernization

### The best historical answer is SAP plus Manipal Global

The most specific vendor evidence comes from people who describe implementation work. Adrija Sen's profile records work at Manipal Global Educational Service from March 2012 and says the organization implemented **SAP SLcM across Manipal Education entities** [10]. It describes the full cycle: business requirements, configuration, master-data management, data migration, development, testing, and deployment [10]. It also assigns the individual responsibility for planning, implementation, and support of SLCM modules [10].

Poornima Vishwaradhya's profile independently records work at Manipal Global Education Services from March 2011 and names **Student Life Cycle Management (SAP SLcM)** [12]. The listed configuration scope includes academic structure, calendars, admission, event planning, module booking, student master data, records, reports, and graduation, plus admissions-to-graduation support and end-user training [12]. The correspondence between SAP's named product, the module list, and MAHE's official SLCM functions is much stronger than a coincidental acronym match.

The defensible historical lineage is therefore:

| Layer | Best-supported organization | Evidence status | Precise conclusion |
|---|---|---:|---|
| Commercial product family | SAP | High | Historical Manipal staff records explicitly call the product SAP SLcM [12][10]. |
| Group implementation and support | Manipal Global Education Services / MaGE | High | Records describe cross-entity implementation, configuration, migration, development, deployment, and support [10]. |
| Current classic-estate support | Internal MAHE ERP/SLCM team | Medium-high | A MAHE project manager describes ERP development and leadership of the SLCM support-development team [9]. |
| Associated student-system development | MAHE Department of Digital and Information Technology | Medium | The MIT attendance/SIS page is credited to this department and sends attendance users to central SLCM [21]. This credit is for the SIS page, not conclusive authorship of all SLCM code. |
| MAHE modernization platform | Salesforce | High | MAHE announced Agentforce Education, Agentforce, MuleSoft, and Tableau for SLCM modernization [6]. |
| MAHE modernization integrator | Deloitte | High | Salesforce names Deloitte as implementation partner [6]. |
| MUJ-specific original builder or current contractor | Not publicly established | Low confidence in any named candidate | Group lineage is strong, but no MUJ-specific contract or ownership statement was located. |

The table shows why "SAP built MUJ SLCM" is too simple. SAP supplied the historical SLCM product family, while Manipal Global personnel configured, developed, migrated, deployed, and supported it. The visible MUJ web application may include a custom portal layer over group processes. Public evidence does not reveal how much standard SAP code, custom Manipal code, or later replacement code remains behind MUJ today.

### The 2026 program is modernization, not proof of original authorship

Salesforce's announcement says MAHE will modernize SLCM, deploy 50+ AI agents over two years, use MuleSoft to connect existing student, learning, and document systems, and use Tableau for analytics [6]. Deloitte will support deployment and integration [6]. The wording matters: existing systems are being connected and modernized. It does not say Salesforce originally built the classic portal, nor does it name MUJ as part of the contract.

Searches for the suggested alternatives - Crucia, ITL, Jain Group technology arms, and Manipal Technologies - produced no relevant public evidence connecting them to Manipal's SLCM. That is not proof of non-involvement; it means they should not be named in a lineage conclusion without new documentary evidence.

**Decision-ready insight:** For procurement, security questionnaires, and incident routing, use a three-part owner model: SAP for historical product lineage, internal Manipal teams for implementation/support, and Salesforce plus Deloitte for the announced MAHE modernization. Keep MUJ-specific contractual ownership as an open item.

## 3. Instance Map: Confirmed Hosts, Aliases, and Non-Matches

### Exact instance table

| Institution or scope | Exact public URL | Status | Visible evidence | Code-family assessment |
|---|---|---:|---|---|
| MAHE classic SLCM | `https://slcm.manipal.edu/` | Confirmed | The page links to `manipal.edu` and exposes the classic confirmation dialogue [20]. | Classic ASP.NET-style family; strongest sibling is Dubai. |
| MAHE newer portal | `https://maheslcm.manipal.edu/login/` | Confirmed public login | The page identifies a company logo and asks for a MAHE Email ID [23]. | Newer branch; consistent with, but not by itself proof of, the announced MAHE modernization. |
| MUJ primary entrance | `https://mujslcm.jaipur.manipal.edu/` | Confirmed | "WELCOME TO MUJ PORTAL," sign-in, and parent-login options [18]. | Same front-end family as the second MUJ hostname. |
| MUJ second entrance | `https://muj.slcm.jaipur.manipal.edu/` | Confirmed | The same "WELCOME TO MUJ PORTAL" heading and sign-in wording [16]. | Near-certain alias or closely coupled deployment of the MUJ application. |
| MIT Manipal | Uses `https://slcm.manipal.edu/` for attendance | Confirmed routing, not separate host | The MIT attendance page directs users to central SLCM [21]. | Consumes the MAHE central service; no separate MIT SLCM hostname was verified. |
| KMC, WGSHA, and other MAHE institutes | MAHE umbrella, exact institute-specific host not found | Supported but not instance-specific | MAHE documents SLCM as its student-and-parent academic suite [5]. | Do not count each institute as a separate deployment without a hostname or contract. |
| Manipal University Dubai | `https://slcm.manipaldubai.com/` | Confirmed | The page links to `manipaldubai.com` and shows forgot-password and confirmation controls [17]. | Strong classic-template sibling of MAHE classic. |
| Manipal University College Malaysia | `https://student.manipal.edu.my/` | Confirmed student portal; same SLCM code not proven | Separate student and parent sign-in labels, scholar email ID, username, password, and account creation [15]. | Visibly different portal framework; classify as similar lifecycle portal, not confirmed shared code. |
| Sikkim Manipal University | No public SLCM instance verified | Unknown | This review found SMU application and Online Manipal services, but no first-party SLCM host matching the Manipal classic or MUJ families. | Do not infer shared code from the Manipal name. |

The main correction to a naive instance map is that **MIT Manipal is not evidence of another deployment**. The MIT attendance page routes the user to the MAHE central host [21]. MIT is an institutional consumer of the central service, not a separately demonstrated instance.

### Login-family fingerprints

Direct comparison of the server-returned public HTML produced three clusters:

1. The two MUJ hostnames use matching Keen theme asset paths, the same jQuery generation, matching form-control names, and matching login scripts. Combined with the identical visible headings [18][16], this is a **high-confidence inference** that they are aliases or builds from the same MUJ front-end code.

2. MAHE classic and Dubai use the same older Bootstrap-oriented, ASP.NET WebForms-style structure, including matching compatibility metadata, asset conventions, state-management markers, and confirmation-dialog language. The visible pages independently show the same confirmation sequence [20][17]. This supports a **high-confidence shared-template inference**, but it does not prove one database or identical patch state.

3. MUJ does not share the MAHE/Dubai login template. Malaysia is different again, offering a "New Here? Create an Account" path and distinct student/parent forms [15]. This weakens any group-wide same-codebase claim.

**Decision-ready insight:** The highest-value deduplication is MUJ-host A <-> MUJ-host B. The highest-value cross-campus code review is MAHE classic <-> Dubai. MAHE classic <-> MUJ should be treated as a business-lineage comparison, not assumed source-code identity.

## 4. Sister Portals and Shared Infrastructure

Manipal's public estate is a federation, not one monolithic portal. The official MAHE student-portal page links users to `https://sis.manipal.edu/index.aspx` [7]. The MIT attendance page within that SIS estate then says attendance should be viewed at `http://slcm.manipal.edu` and credits MAHE's Department of Digital and Information Technology for the SIS page [21]. This is a concrete handoff between a sister portal and SLCM.

The learning environment is also plural. MAHE's ICT inventory says KMC Mangalore faculty were trained on EduNxt, while MIM used course pages and Moodle for quizzes, assignments, and discussion forums [5]. For Manipal University Jaipur Online, D2L publicly identifies a robust D2L learning management system [8]. These are LMS systems, not proof that they share SLCM's code or authentication store.

| Sister system | Exact URL | Audience or function | Relationship to SLCM |
|---|---|---|---|
| MAHE SIS / student portal | `https://sis.manipal.edu/index.aspx` | General student web services | Official student page points here [7]; attendance page hands off to central SLCM [21]. |
| MIT attendance page | `https://sis.manipal.edu/AtdMIT.aspx` | MIT attendance entry point | Explicitly directs attendance viewing to `slcm.manipal.edu` [21]. |
| MUJ Online LMS | `https://muj.onlinemanipal.com/` | Online-program learning and student experience | D2L is publicly identified as the LMS product [8]; distinct from campus SLCM. |
| MUJ examination information | `https://jaipur.manipal.edu/examination.php` | Examination process, schedules, and notices | Public information page; no separate exam application codebase was established. |
| MAHE alumni portal | `https://manipalalumni.manipal.edu/` | Alumni ventures, entrepreneurs, gallery, and events | Separate classic portal with its own alumni navigation [24]. |
| MUJ alumni community | `https://mujalumni.in/` | MUJ alumni community and university updates | Separate MUJ-branded alumni service; it links back to MUJ material [25]. |
| Requested legacy MUJ alumni hostname | `https://alumni.jaipur.manipal.edu/` | Historical or unavailable entry point | It did not return a usable public landing page in this review; the discoverable current community is `mujalumni.in`. |
| Malaysia student portal | `https://student.manipal.edu.my/` | Student and parent access | Similar lifecycle role, but visibly different portal framework [15]. |

No standalone, first-party `timetable.manipal.edu` service was verified. Timetables may instead be delivered through SLCM, departmental pages, or apps. A public MUJ mobile project demonstrates timetable and calendar views alongside grades and attendance [4], but that is a student-built application and cannot be treated as an official sister portal.

Attendance is similarly split between official SLCM capability and third-party convenience clients. MAHE's official SLCM definition includes attendance [5], the MIT SIS page redirects attendance to SLCM [21], and public wrappers consume attendance data [14][4]. This is shared business data, but not necessarily shared application code.

**Decision-ready insight:** Identity, grades, attendance, fees, learning, examinations, and alumni services cross portal boundaries. Risk review must therefore include integrations and data synchronization, not only the SLCM login page.

## 5. Public Technology Chatter and Integration Evidence

### Case study: The central Manipal REST wrapper

The `canaryGrapher/slcmAPI` repository calls itself an open-source REST API for Manipal University's Student Life Cycle Management portal [14]. It says the service helps applications query SLCM data instead of directly scraping pages [14]. Documented functions include current-semester theory marks, attendance, admission-profile details, credential validation, and combined validation/data requests [14].

This is important architecture evidence. It shows that students could model stable enough authenticated workflows to expose portal data through their own API layer. It does **not** show an authorization bypass: credential validation is one of the documented operations [14]. The repository later marked itself deprecated because the login portal introduced CAPTCHA [14]. That change is evidence of an anti-automation control, not evidence that CAPTCHA can be bypassed.

### Case study: MUJ feedback automation

The `AddisionS/slcm-feedback-form-filler` extension targets MUJ's SLCM feedback form and offers "All Yes" or "All No" actions [3]. It can set every answer and automatically submit the form [3]. The project identifies itself as a Chrome or Firefox extension implemented in JavaScript, CSS, and HTML [3].

The mechanism creates a survey-integrity risk: repeated questions can be answered and submitted with little user deliberation. This is not a vulnerability in the usual confidentiality-integrity-availability sense unless a control is bypassed. It is, however, evidence that client-side workflow controls should not be relied upon to guarantee thoughtful or granular responses.

### Case study: A third-party MUJ mobile client

The public MUJ app project says it replicates and extends MUJ's SLCM functions for students and class representatives [4]. Documented functions include login, timetable and calendar, grades, GPA/CGPA, and subject-wise attendance [4]. Its stack includes Flutter/Dart, FastAPI/Python, custom email/password authentication, and Docker [4].

The security implication belongs to the third-party integration surface. A custom client that accepts institutional credentials can create credential-handling, data-retention, and support risks even when the official portal is secure. The repository does not document an official endorsement or a platform vulnerability [4]. Institutions should publish supported APIs and warn users against entering credentials into unapproved clients.

### Community and employment evidence

Student reports add reliability signals but weak root-cause evidence. One MUJ user said the portal rejected a password they believed was correct [13]. Another Manipal student reported that a paid fee remained marked as pending and received no stated resolution in the captured discussion [11]. These symptoms fit authentication failure and financial synchronization delay, respectively, but neither establishes exploitability.

No useful public job posting naming an MUJ SLCM maintainer was found. LinkedIn-style experience records were more probative: they named SAP SLcM implementation across Manipal entities [10] and an internal MAHE support-development team [9].

**Decision-ready insight:** Public chatter reveals workflow automation, integration demand, and reliability pain points. It does not support headlines such as "Manipal SLCM was hacked" or "MUJ has an authentication bypass."

## 6. Shared-Risk Implications: What Transfers and What Does Not

### Public findings and their proper classification

| Public observation | Source instance | Classification | Likely applicability elsewhere | Safe conclusion |
|---|---|---|---|---|
| Authenticated wrapper exposes marks, attendance, profile, and credential-validation workflows | MAHE/Manipal classic project | Documented API-wrapper behavior, not a proven vulnerability | Moderate for portals with equivalent workflows; unknown for MUJ implementation | Review supported APIs, session controls, rate limits, and third-party-client guidance [14]. |
| Wrapper became deprecated after CAPTCHA appeared | MAHE/Manipal classic | Defensive control and compatibility break | High only for the same classic login family; unproven for MUJ | CAPTCHA reduced the old wrapper's compatibility [14]. |
| Feedback form can be filled uniformly and auto-submitted | MUJ | Workflow-integrity concern | High for the same MUJ form reached through either MUJ alias; low for MAHE without form confirmation | Add server-side abuse controls and assess feedback quality [3]. |
| Mobile client reproduces login, timetable, grades, and attendance with custom authentication | MUJ | Third-party credential/data surface | High for MUJ users of that client; not evidence of a server flaw | Publish approved-client policy and revoke unsupported integrations if necessary [4]. |
| Correct password allegedly rejected | MUJ | Anecdotal authentication/reliability issue | High across the two MUJ aliases if they share authentication; not automatically MAHE-wide | Check identity-provider health, lockout messaging, and password-state synchronization [13]. |
| Paid fee allegedly remained pending | Unspecified Manipal SLCM context | Anecdotal data-consistency issue | Potentially relevant wherever fee and SLCM systems integrate | Monitor payment-to-ledger reconciliation and provide transaction-status tracing [11]. |
| Classic confirmation template appears on MAHE and Dubai | MAHE classic and Dubai | Shared-template fingerprint | High for UI defects and stale front-end dependencies; medium or low for backend flaws | Review both together, but verify version and patch state separately [20][17]. |
| Two MUJ hostnames expose equivalent branded login pages | MUJ | Alias/shared-deployment fingerprint | Very high between the two MUJ hosts | Treat them as one risk domain operationally until ownership confirms separation [18][16]. |
| Publicly indexed MAHE classic password-change page exists | MAHE classic | Normal exposed account workflow, not a vulnerability | Relevant only if common password components are confirmed | Its fields are old password, new password, and confirmation [26]; exposure alone proves no flaw. |

### Where risk transfer is justified

**MUJ alias to MUJ alias:** High confidence. The pages have identical branding and strongly matching returned HTML. A client-side defect, feedback-form weakness, or login availability problem on one is likely relevant to the other because they appear to be aliases or sibling deployments.

**MAHE classic to Dubai:** Medium-high confidence for presentation-layer findings. Matching classic structures and visible dialogue language support common-template review [20][17]. Yet separate hostnames and institutional contexts could have different builds, authentication providers, databases, or patch levels. A finding must be reproduced by the owner before being considered present in both.

**MAHE classic to MUJ:** Low confidence for front-end vulnerabilities. Their public login applications belong to different template families. Historical SAP implementation across Manipal entities supports a possible common business or backend lineage [10], but that does not show current shared source code. Transfer only findings tied to a confirmed common component, protocol, or library.

**MAHE Salesforce-era portal to MUJ:** Very low confidence. The official announcement names MAHE, Salesforce products, and Deloitte [6]. It does not state that MUJ is included. A publicly visible MAHE email login [23] cannot be generalized to MUJ.

### What was not found

No public source reviewed here established a CVE, SQL injection, authentication bypass, unauthorized grade access, exposed credential set, or confirmed breach affecting these SLCM hosts. Public wrappers and visible reset pages are not vulnerabilities by themselves. Student reports are operational evidence, not security verification.

Recommended controls follow directly from the evidence:

1. Maintain one asset record per hostname, with an explicit alias field for the two MUJ entrances.
2. Record product, custom code, identity provider, database, and deployment version separately. "SLCM" is not a sufficient configuration item.
3. Compare a software bill of materials for MAHE classic and Dubai, then for the two MUJ hosts.
4. Place supported student-data APIs behind an API gateway instead of forcing third-party scraping or credential replay.
5. Use server-side anti-automation and response-quality controls for feedback workflows.
6. Publish a third-party-client policy and prohibit collection of institutional passwords by unapproved apps.
7. Monitor payment reconciliation and identity synchronization as service-level risks.
8. Keep Salesforce development and system-integration-test environments segregated, access-controlled, and out of unnecessary indexing.
9. Establish one coordinated vulnerability-disclosure channel covering MAHE, MUJ, Dubai, and related portals.

**Decision-ready insight:** Shared branding should trigger shared triage, not shared guilt. Confirm the common component before declaring a cross-instance vulnerability.

## 7. Synthesis: One Product Line, Several Application Families

The evidence converges on a product family with continuity at the business-process level and divergence at the application level.

| Dimension | MAHE classic | MUJ | Dubai | Malaysia | MAHE modernization |
|---|---|---|---|---|---|
| Historical mechanism | Manipal SLCM with evidence of group SAP SLcM lineage | Likely related to group lineage, but exact backend unconfirmed | Classic Manipal SLCM sibling | Student/parent lifecycle portal, same product unconfirmed | Salesforce services integrating existing systems |
| Public front end | Old classic template | Keen-themed MUJ portal | Old classic template similar to MAHE | Distinct portal framework | Separate MAHE email-oriented login |
| Scope | Central MAHE service; MIT attendance routes to it [21] | MUJ students and parents [18] | Dubai institution [17] | Malaysia students and parents [15] | MAHE's multi-campus environment of 40,000+ students [6] |
| Strongest sibling | Dubai | Its second MUJ hostname | MAHE classic | None established | Existing MAHE student, learning, and document systems |
| Main public risk signal | Authenticated wrapper and legacy automation [14] | Feedback automation, third-party app, anecdotal login issue [3][4][13] | Shared-template exposure | Distinct account-creation and parent-login surface [15] | Integration, data-governance, and migration risk rather than legacy-template risk |
| Evidence limitation | Backend and patch state undisclosed | Exact vendor/maintainer undisclosed | Database and version undisclosed | SLCM identity unproven | MUJ coverage unannounced |

Three tensions are important.

First, **SAP lineage versus custom web code**: Manipal staff explicitly identify SAP SLcM [12][10], yet the public portals exhibit different front-end generations. This suggests a group product or process lineage can coexist with locally customized or replaced presentation layers. Security teams should test components, not acronyms.

Second, **centralization versus federation**: MIT attendance routes to central MAHE SLCM [21], but LMS, alumni, online learning, and MUJ services occupy separate portals [8][24][25]. The estate is centralized for some academic records and federated for other lifecycle functions. Integration failures can therefore be as consequential as application defects.

Third, **modernization versus continuity**: Salesforce and Deloitte are modernizing MAHE through Agentforce, MuleSoft, and Tableau [6], while classic hosts remain publicly visible. Migration creates a period in which old and new identity, document, learning, and student-data paths may coexist. The dominant risk changes from a single legacy application to synchronization, entitlement mapping, and retirement discipline across generations.

The failure case would be to assume that Salesforce now owns every Manipal SLCM instance or that a bug in MAHE classic automatically compromises MUJ. The opposite failure would be to ignore group lineage and investigate every host in isolation. The balanced strategy is federated asset ownership with shared component intelligence.

## VERDICT

### Direct answer

**Who built the SLCM family?** The highest-confidence historical answer is **SAP supplied the Student Lifecycle Management product family, while Manipal Global Education Services personnel implemented, configured, developed, migrated, deployed, trained users on, and supported SAP SLcM across Manipal Education entities** [12][10].

**Who maintains MUJ's portal today?** Public evidence does not identify a MUJ-specific current contractor or named maintenance team. An internal MAHE project manager reports leading an SLCM support-development team [9], and MAHE's Department of Digital and Information Technology is credited on a connected MIT attendance/SIS page [21]. Those facts support internal Manipal operational capability, but extending them specifically to MUJ is an **inference**, not a confirmed fact.

**Who is modernizing SLCM now?** For MAHE, Salesforce supplies Agentforce Education, Agentforce, MuleSoft, and Tableau, and Deloitte is the announced implementation partner [6]. The announcement does not establish MUJ's inclusion.

**Which instances share code?** The two MUJ hostnames are almost certainly aliases or the same front-end family. MAHE classic and Dubai are strong shared-template candidates. MUJ and MAHE classic do **not** expose the same login-page code family. Malaysia is a visibly separate framework. MIT Manipal uses the central MAHE host for attendance rather than a separately verified MIT SLCM deployment [21]. No first-party Sikkim SLCM instance was verified.

### Confidence table

| Finding | Confidence | Basis |
|---|---:|---|
| Historical Manipal SLCM product lineage is SAP SLcM | **High, 0.93** | Two independent Manipal Global experience records explicitly name SAP SLcM and detailed implementation work [12][10]. |
| Manipal Global acted as implementation/support organization | **High, 0.92** | Cross-entity implementation, development, deployment, training, and support are stated directly [12][10]. |
| MAHE has an internal SLCM support-development capability | **High, 0.86** | Current-style MAHE profile evidence names the SLCM support-development team [9]. |
| Exact current MUJ maintainer is publicly known | **Low, 0.25** | No MUJ-specific owner record or contract was found. |
| The two MUJ URLs share the same front-end deployment family | **Very high, 0.96** | Identical visible portal wording plus matching HTML assets and scripts [18][16]. |
| MAHE classic and Dubai share a classic template/code lineage | **High, 0.85** | Matching returned structure and visible confirmation behavior [20][17]. |
| MAHE classic and MUJ share the same public front-end codebase | **Low, 0.20** | Their returned front-end families differ materially. Historical SAP lineage is not enough to prove current source-code identity. |
| Salesforce/Deloitte modernization applies to MAHE | **Very high, 0.98** | Official vendor announcement [6]. |
| Salesforce/Deloitte modernization applies to MUJ | **Low, 0.20** | MUJ is not named in the cited announcement. |
| A confirmed publicly disclosed SLCM vulnerability was found | **Very low, 0.10** | The reviewed evidence shows wrappers, workflow automation, and reliability complaints, not a verified vulnerability or breach. |

**Final judgment:** Describe MUJ as part of the broader **Manipal SLCM lineage with historical SAP and Manipal Global implementation evidence**, but do not state that its current portal is the same codebase as `slcm.manipal.edu`. The strongest shared-code conclusions are **MUJ alias to MUJ alias** and **MAHE classic to Dubai template family**. For risk transfer, verify the common component before treating any public finding as applicable across campuses.

## References

1. *GitHub - Anushkakumar10/muj_slcm · GitHub*. https://github.com/Anushkakumar10/muj_slcm
2. *GitHub - AwesomeSam9523/SLCM_API*. https://github.com/AwesomeSam9523/SLCM_API
3. *GitHub - AddisionS/slcm-feedback-form-filler: This is a chrome extension that can be used to automate the process of filling feedback form on MUJ's SLCM portal · GitHub*. https://github.com/AddisionS/slcm-feedback-form-filler
4. *GitHub - DK10WS/SLCM_APP: App Version for MUJ SLCM · GitHub*. https://github.com/DK10WS/SLCM_APP
5. *http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf*. http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf
6. *http://salesforce.com/in/news/press-releases/2026/03/26/manipal-university-ai-transformation*. http://salesforce.com/in/news/press-releases/2026/03/26/manipal-university-ai-transformation
7. *Student Portal Login- MAHE (Manipal Academy Of Higher Education)*. https://www.manipal.edu/mu/academics/student-portal.html
8. *Manipal University Jaipur (Online) - D2L*. https://www.d2l.com/en-in/why-d2l/customers/manipal-university-jaipur-online
9. *Himanshu Upadhyay*. https://linkedin.com/in/himanshuupadhyay
10. *Adrija Sen*. https://linkedin.com/in/adrija-sen-91631110
11. *Paid my Fees But Still Showing as Pending on SLCM*. https://www.reddit.com/r/Manipal_Academics/comments/1lzf0ht/paid_my_fees_but_still_showing_as_pending_on_slcm
12. *Poornima Vishwaradhya*. https://linkedin.com/in/poornima-vishwaradhya-a0b95b22
13. *Slcm portal issue : r/manipaljaipur*. https://www.reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue
14. *GitHub - canaryGrapher/slcmAPI: The API for SLcM, Manipal. Get your marks, your attendance and your profile details · GitHub*. https://github.com/canaryGrapher/slcmAPI
15. *Portal Framework*. https://student.manipal.edu.my/
16. *Manipal University*. https://muj.slcm.jaipur.manipal.edu/
17. [

](https://slcm.manipaldubai.com/)
18. *Manipal University*. https://mujslcm.jaipur.manipal.edu/
19. *Login | SLCM*. https://maheslcmtech--sit.sandbox.my.site.com/login?locale=us
20. [
	MU SLcM
](https://slcm.manipal.edu/)
21. [
	SIS
](https://sis.manipal.edu/AtdMIT.aspx)
22. *http://open.ieee.org/partners/manipal-university-jaipur*. http://open.ieee.org/partners/manipal-university-jaipur
23. *maheslcm.manipal.edu*. https://maheslcm.manipal.edu/login/
24. *Alumni Portal*. https://manipalalumni.manipal.edu/
25. *Official Community of Manipal University Jaipur*. https://mujalumni.in/
26. [
	MU SLcM
](https://slcm.manipal.edu/StudentChangePassword.aspx)
