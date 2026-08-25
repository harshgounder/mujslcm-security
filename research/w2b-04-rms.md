## Research status: MUJ SLCM and RMS

### What is established so far

The strongest finding is that the host named `rms.jaipur.manipal.edu` publicly presents itself as a **Research Data Management System**, not as a student examination-result system. Its public page contains the title "Research Data Management System" [4], two department research-performance announcements for April and May 2025 [4], and a link to MUJ IRINS [4]. The page also displays username and password labels [4], a Chrome browser recommendation [4], and a footer crediting MSIS and ISD, Manipal Academy of Higher Education [4].

Public DNS evidence maps `rms.jaipur.manipal.edu` to `202.131.155.153` [10]. A page reached at the numeric host displayed the same type of research-performance announcements and did not present academic-result content in the supplied public text [5]. This supports an association between the hostname and the research-management presentation, but it does not independently prove network ownership, backend architecture, or that every virtual-host configuration behaves identically.

The public SLCM entry page exposes a MUJ portal sign-in interface and labels a parent-login option [2]. A separate indexed SLCM home path displays "Manipal University" and "Forgot Password?" [1]. The reviewed unauthenticated material does not expose student marks, grades, result PDFs, or a result document. This is a statement about the public material reviewed, not proof that authenticated users cannot view marks or that no private application route exists.

The official MUJ examination page states that student performance is continuously assessed using class/tutorial participation, assignments, lab work, class tests, and in-semester tests [3]. A fuller extraction also indicates that MUJ describes an examination and assessment framework, but the currently surfaced evidence does not establish that RMS stores, publishes, or retrieves those marks. No source found so far explicitly states that RMS and SLCM share a marks database or that RMS is the student-result backend.

The main Manipal RMS site provides stronger evidence about the meaning of the RMS product than the MUJ-specific host does. Its public search result refers to new RMS login access, publication, APC, conference-entry queries, grants, seed money, and open-access publication queries [7]. Another public RMS result states that existing users with login issues should check password expiry and says RMS uses the same credentials as the Outlook account [7]. These are research-administration functions and Microsoft 365 identity guidance; they are not evidence of an academic transcript or student-marks function.

The MUJ RMS search results also identify a public `Login.aspx` path [8]. The visible content returned for that path repeats research-performance announcements rather than showing a public result-document index [8]. The SLCM page's raw HTML exposes ordinary public static assets, including jQuery and validation scripts [the server-returned markup was inspected, but the raw-markup tool output is not itself a citable source]. Because the raw HTML inspection did not establish a result-fetching JavaScript call in the visible excerpt, no public script can yet be responsibly identified as fetching marks or PDFs.

### Current evidence matrix

| Question | Current finding | Evidence status | Exact public URL(s) |
|---|---|---|---|
| What does RMS publicly call itself? | Research Data Management System | Verified | https://rms.jaipur.manipal.edu/ |
| What does the MUJ RMS page visibly publish? | Research-performance announcements and an MUJ IRINS link | Verified | https://rms.jaipur.manipal.edu/ |
| Does the public RMS page visibly identify student results? | Not in the reviewed public text | Negative observation, not proof of absence | https://rms.jaipur.manipal.edu/ |
| What does SLCM publicly expose? | MUJ portal sign-in, parent-login wording, and password-recovery wording on indexed paths | Verified | https://mujslcm.jaipur.manipal.edu/ ; https://mujslcm.jaipur.manipal.edu/Home/Index |
| Are marks visible without authentication? | None were visible in the reviewed unauthenticated page content | Negative observation, not proof of absence | https://mujslcm.jaipur.manipal.edu/ |
| What IP is returned for the RMS hostname? | 202.131.155.153 | Verified by public DNS response | https://dns.google/resolve?name=rms.jaipur.manipal.edu&type=A |
| Does official MUJ examination material describe assessment? | Yes; continuous assessment includes participation, assignments, lab work, class tests, and in-semester tests | Verified | https://jaipur.manipal.edu/examination.php |
| Is an RMS-to-SLCM marks relationship explicitly documented? | Not established in the evidence gathered | Unanswered | RMS and SLCM public pages above |
| Is a public RMS result PDF format established? | No | Unanswered | No indexed RMS result PDF was found in the reviewed searches |
| Is a public result-fetching JavaScript endpoint established? | No | Unanswered | Public landing-page markup review did not establish one |

### What remains unanswered

1. **RMS publication scope.** The public landing page clearly publishes research-performance announcements and links to IRINS, but it remains unresolved whether authenticated RMS users can generate or retrieve any documents that happen to be called "results." The word "result" in the research sense, a research-performance report, an academic result, and a student grade document must not be conflated.

2. **Result PDF formats.** No defensible RMS-specific result PDF naming convention, URL pattern, page layout, metadata schema, or sample document has yet been established. Search results surfaced other Manipal result material, including entrance-exam result pages, but those are not evidence about `rms.jaipur.manipal.edu` and should not be treated as RMS artifacts.

3. **Public scripts that fetch results.** The SLCM page uses publicly served JavaScript libraries and validation assets, but the available markup excerpt does not prove that any script calls an RMS endpoint or retrieves a PDF. A static library reference is not equivalent to a business-function endpoint. Establishing this point would require passive review of server-returned public HTML and publicly linked script files only, without submitting credentials, enumerating hidden routes, or attempting to access another user's data.

4. **SLCM marks relationship.** MUJ's examination page establishes that academic assessment exists and that multiple assessment components contribute to student performance [3]. It does not, in the evidence surfaced, name RMS as the storage or publication system. The most supportable current conclusion is that SLCM is the publicly branded student-portal entry point while RMS is publicly branded as research administration; any data-sharing relationship is an inference unless MUJ documentation explicitly connects them.

5. **Login flow detail.** Publicly observable labels establish entry points, but they do not establish a complete authenticated workflow. The RMS page shows username and password fields [4], and the SLCM page shows sign-in and parent-login labels [2]. The available public evidence does not justify documenting password-reset mechanics, token behavior, redirect targets, account-enumeration behavior, or post-login result routes.

6. **Infrastructure claims.** The IP mapping is supported by public DNS [10]. The supplied research brief mentions ASP.NET MVC 5.3, .NET Framework 4.x, IIS 10, Akamai, and Microsoft 365 identity, but the research evidence currently surfaced does not independently verify every one of those technology/version claims for the RMS host. The public RMS page's Outlook-credential guidance supports a Microsoft identity relationship for the broader RMS service [7], but it does not by itself prove a particular authentication protocol or tenant configuration for the MUJ SLCM application.

### Search strategy assessment

The first searches used the hostname, IP address, RMS, SLCM, result, PDF, login, marks, grades, and JavaScript terms. They found the RMS landing page, the RMS `Login.aspx` path, the DNS response, the SLCM landing page, the SLCM `Home/Index` path, MUJ's official examination page, the main Manipal RMS site, and an archived SLCM URL inventory. Searches for exact RMS result/PDF terms were sparse and returned unrelated or broader Manipal result material rather than an RMS-specific artifact. That scarcity is useful negative evidence for public indexing, but it is not proof that authenticated or unindexed documents do not exist.

The archived SLCM inventory is promising for understanding which public HTML, CSS, JavaScript, and image resources were historically crawlable. It should be used only to distinguish an observed public asset from a hypothesized application route. A filename or framework convention cannot establish that marks are fetched, that a PDF is generated, or that RMS is called by SLCM.

### Safe next research steps

A further pass should remain passive and should focus on authoritative public material. It should extract the official MUJ examination and research pages in full, review the archived SLCM URL inventory for explicitly named result/grade/marks paths, compare server-returned public HTML for the RMS landing page and SLCM landing page, and search MUJ's own public site for terms such as "grade card," "marksheet," "semester result," "result declaration," and "examination result." Any candidate PDF should be read only if it is publicly linked or indexed and should be checked for whether it belongs to MUJ, RMS, admissions, or another Manipal service. No credential use, password testing, route guessing, identifier enumeration, forced browsing, or access to personal result data is appropriate for this OSINT project.

## VERDICT

**Current confidence: Moderate for the system-role distinction; low-to-moderate for the unresolved data-flow questions.** The public evidence supports the conclusion that `rms.jaipur.manipal.edu` is presented as a research-management system and that `mujslcm.jaipur.manipal.edu` is presented as a student-portal login surface. The evidence does not support calling RMS a student-result publication system, does not establish an RMS result-PDF format, does not identify a public JavaScript result-fetching endpoint, and does not prove that RMS and SLCM marks are connected. Those points should remain **not established from public evidence**, rather than being filled with assumptions.

## References

1. *Manipal University*. https://mujslcm.jaipur.manipal.edu/Home/Index
2. *Manipal University*. http://mujslcm.jaipur.manipal.edu
3. *Examination - Manipal University Jaipur*. https://jaipur.manipal.edu/examination.php
4. *Manipal Academy of Higher Education - RMS*. https://rms.jaipur.manipal.edu/
5. *202.131.155.153 - RMS*. https://202.131.155.153/
6. *web.archive.org*. http://web.archive.org/cdx/search/cdx?collapse=urlkey&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&output=json&url=mujslcm.jaipur.manipal.edu/*
7. *Manipal Academy of Higher Education*. https://rms.manipal.edu/
8. *RMS - Manipal Academy of Higher Education*. https://rms.jaipur.manipal.edu/Login.aspx
9. *Directorate of Research - Manipal University Jaipur*. http://jaipur.manipal.edu/research.php
10. *dns.google*. https://dns.google/resolve?name=rms.jaipur.manipal.edu&type=A
