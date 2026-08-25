# Digest: w2e-05-india-erp-vendors.md

## REPORT
Source file: w2e-05-india-erp-vendors.md (MUJ SLCM and India's University ERP Risk Landscape)

## ANSWER SUMMARY
- No reviewed public source attributes MUJ SLCM to Saral, GateWay, Hexad, Simpliance, Jeewane, MasterSoft, Serosoft, Fedena, TCS iON, or Samarth.
- The named list mixes categories: Saral and MasterSoft are real education ERPs, Simpliance is compliance SaaS, Hexad shows no university ERP, GateWay and Jeewane do not resolve.
- Fedena 2.3 open-source is the only strong product-specific vulnerability record: seven findings including auth bypass and RCE, unsupported with no patches planned.
- ".NET portal" is an architectural class, not a vendor identity; historical Fedena used Ruby, Rails 2.3.5, and MySQL.
- Strong identity does not replace application authorization: Entra and phishing-resistant MFA cannot stop IDOR without per-object checks.
- Akamai protects a boundary, not the whole application; origin TLS and authorization are origin obligations.
- ".NET Framework 4.x" spans retired releases (4.5.2, 4.6, 4.6.1 retired April 2022) and 4.6.2 (listed end January 2027); the label is too broad for support decisions.
- The immediate mission should be authorized inventory, role-matrix testing, and supplier assurance, not unapproved probing.

## KEY FACTS
1. https://mujslcm.jaipur.manipal.edu/ - target portal; discloses no product or framework version.
2. http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf - MAHE document listing SLCM functions.
3. http://erp.saral.in/sch - SARAL School Soft ERP by Saral Computers, in service since 1990.
4. https://cimsstudentnewui.mastersofterp.in/ - MasterSoft student portal with credential warning text.
5. http://iitms.co.in/ - MasterSoft Education ERP for schools and higher education.
6. https://serosoft.com/solutions - Academia by Serosoft product family.
7. https://www.hexad.in/ - Hexad corporate page; no university ERP product shown.
8. https://www.aparajitha.com/products/vendor-audit - Simpliance Vendor, compliance-audit SaaS, category mismatch.
9. https://www.tcsion.com/institutions/higher-education - TCS iON higher-education suite scope.
10. https://samarth.edu.in/ - Samarth eGov digital-campus initiative.
11. https://pentest.co.uk/labs/research/fedena-school-management-software/ - seven Fedena 2.3 findings with named CVEs and remediation stance.
12. https://pentest.co.uk/labs/fedena-authentication-bypass-cve-2021-27980/ - default client-side sessions with a static public secret, admin-level access.
13. https://github.com/projectfedena/projectfedena_v2.0 - Fedena 2.0 source showing Ruby, Rails 2.3.5, MySQL.
14. https://learn.microsoft.com/en-us/lifecycle/products/microsoft-net-framework - lifecycle dates separating supported from retired 4.x releases.
15. https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html - per-object server-side authorization requirement.

## ACTIONABLE LEADS
- Ask MUJ IT for a versioned SBOM covering Windows, IIS, CLR, MVC packages, NuGet, database, Akamai configuration, and identity integration.
- Obtain contracts and data-flow diagrams to resolve GateWay, Jeewane, and Hexad attribution; wrong vendor contact is itself a risk.
- Review Entra Conditional Access exports, phishing-resistant MFA coverage, and privileged-role policies.
- Build a role-object-action matrix (student, parent, faculty, examiner, finance, helpdesk, admin) and test only in an approved tenant.
- If an exact Fedena 2.3 tenant exists anywhere, isolate and migrate; WAF mitigation was declared incomplete.
- Collect supplier assurance packs: pentest summaries, remediation SLAs, disclosure policies, subprocessor records.

## FLAGS
- All vendor attributions to MUJ are unverified; "no advisory found" is an evidence gap, not proof of safety.
- Fedena findings apply to the unsupported 2.3 open-source branch, not current Fedena and not MUJ.
- The supplied stack remains a user-supplied hypothesis; SQL Server is only an ecosystem guess.
- ViewState and machine-key discussion is reference architecture, not a MUJ finding.
- The alternate hostname muj.slcm.jaipur.manipal.edu appears in references as a portal surface; treat as unverified alias.

## COVERAGE
Chars read: 40473. EOF confirmed: yes (truncation flag false on full read).