# MUJ SLCM Surface Synthesis

Source: 38 digest files, /home/liebert511/mujslcm-recon/research/digests/, prefixes w2b (14), w2d (9), w3 (15). Every claim below carries its digest name. All digests read to EOF, see COVERAGE table.

## 1) INFRASTRUCTURE MAP

### Target
- **mujslcm.jaipur.manipal.edu** (primary). Role verified: SLCM student/parent portal, official registration link per FAQ (w2b-01, w3-14). Tech: Microsoft-IIS/10.0, ASP.NET MVC 5.3, ASP.NET 4.0.30319 headers (w2d-06, w3-06, w3-14); Keen theme login assets, jQuery 1.10.2 (w2b-03); 2024 scan showed IIS 8.5 and port 122, 2026 scans IIS 10 (w3-14); 2025-26 fee notice also prints :122 URL form (w2d-03). Cloud: A record 98.70.14.50, AS8075 Microsoft (w2b-01, w3-06, w3-14); 2024 address 202.131.155.150 (w3-14). Forgot Password link to passwordreset.microsoftonline.com (w2b-03, w3-14). Threat relevance: the target; Microsoft-linked recovery present, federation unproven.

### Sibling hosts
- **muj.slcm.jaipur.manipal.edu** (alternate). Role unverified: same portal family, "WELCOME TO MUJ PORTAL", @jaipur.manipal.edu context; FAQ names only the primary (w2b-01, w3-03). Tech: none confirmed, zero URLScan coverage (w2b-01). Cloud: A record 20.244.94.89, AS8075 Microsoft, Pune (w2b-01). Threat: unknown alias, migration or staging surface; no shared backend proven (w2b-01).
- **mujerp.jaipur.manipal.edu** (ERP). Role verified as Dynamics 365 Business Central sign-in, /MUJWEB/SignIn POST (w2b-02, w3-09). Tech: ms-nav layout, Business Central title (w3-09); MVC 5.3/.NET 4.x/IIS 10/Akamai unconfirmed (w2b-02, w3-09). Cloud: A record 20.244.0.229 (w3-09), Azure family unverified region (w3-09). Threat: staff/finance surface, no SLCM linkage proven (w2b-02, w3-09).
- **mujone.jaipur.manipal.edu** (HR). Role verified: "MUJ HR SYSTEM", HR/Login.aspx with employee code, DOB, captcha, policy acknowledgements, PAS Portal link to pas.muj.edu.in (w2b-02, w2b-03, w3-08). Tech: no reliable header capture, archives 2022-08-17 to 2024-08-28 (w3-08). Cloud: A record 52.172.36.15, AS8075 Microsoft, Chennai (w2b-03, w3-08). Threat: staff credential surface; third-party apps (MUJ GO, MUJstella) create phishing surface (w3-08).
- **rms.jaipur.manipal.edu** (Research Data Management System). Role verified by title and notices; not a results system (w2b-04, w3-10). Tech: Login.aspx, WebResource.axd, aspnetForm, Web Forms family (w3-10); MVC/IIS/Akamai unverified (w2b-04). Cloud: A record 202.131.155.153, AS134039 Ibus, convergentindia reverse DNS (w3-10). Threat: Outlook-credential wording exists only on central rms.manipal.edu, not Jaipur host (w3-10); login wall with @jaipur.manipal.edu (w3-10).
- **helpdesk.jaipur.manipal.edu** (ticketing). Role unverified: NXDOMAIN now, certificates logged 2026-01-08 to 2027-01-08, Entrust (w2b-05, w3-11). Tech: none observed; vendor unattributable, osTicket proven only for helpdesk.manipal.edu.my and Freshworks only for servicedesk.manipal.edu (w2b-05, w3-11). Cloud: none resolved (w2b-05). Threat: likely prepared-for-TLS asset, production status unproven (w3-11).
- **hms.manipal.edu** (Hostel Management System, MAHE). Role verified: hostel booking by block and capacity; Jaipur not on campus list (w3-07). Tech: Azure Application Gateway v2 snapshot, no origin headers (w3-07); archive paths include Authorization.aspx, Atom_PayResponse.aspx, HDFCResponse.aspx (w3-07). Cloud: A record 20.44.49.205, AS8075 Microsoft (w3-07). Threat: separate MAHE service; historic payment routes; no MUJ link, MUJ room booking never names hms (w3-07).
- **portal.manipal.edu** (EPF). Role verified: Employee Provident Fund app with user, resigned-employee, admin logins, MAHE ISD footer (w3-06). Tech: IIS 10 and ASP.NET disclosed via 403 on root (w3-06); 2022 archive served generic IIS landing page (w3-06). Cloud: A record 45.112.150.155, AS134039 Ibus (w3-06). Threat: employee surface, separate from SLCM; per-path policy difference root 403 vs reachable /epf (w3-06).
- **webmail.manipal.edu** (mail). Role unverified now: current indexed page titled "VPN Portal", Sophos strings in 2022 archive (w3-05). Tech: historical Exchange 2003 OWA (2006), OWA Light (2012), Outlook Web App (2015/2016) (w3-05). Cloud: A record 218.248.47.16, block 218.248.47.0/26 netname MAHE, covering route AS9829 BSNL-NIB (w3-05); parent domain mail is Microsoft 365 (w3-05). Threat: legacy mail/VPN surface, credential acceptance unestablished (w3-05).
- **exam.jaipur.manipal.edu** (exam). Role unverified: no official source names it (w3-01). Tech: none, URLScan/Shodan/Wayback empty, Netcraft blank (w3-01). Cloud: A record 59.91.192.229, AS9829 BSNL NIB (w3-01). Threat: low-visibility asset with unknown purpose, stack, login flow; not linked to SLCM credentials (w3-01).
- **uat.manipal.edu** (staging). Role verified as MAHE institutional frontend, marketing content, Apply Now (w3-02). Tech: Next.js asset paths, branded Error 500 fallback (w3-02). Cloud: CNAME to uat-ci-mahe-ep-bzgfhcehh0fvhafs.a01.azurefd.net, Azure Front Door, resolver 150.171.109.183 (w3-02). Threat: staging origin outside edge; origin isolation unknown, top control question (w3-02).
- **api.manipal.edu** (API). Role verified: JSON root with one opaque data string, Express (w3-03). Tech: nginx 1.18.0, Ubuntu, Node.js, Express, X-Powered-By, wildcard CORS, Let's Encrypt (w3-03). Cloud: A record 43.205.223.7, Amazon EC2 ap-south-1, AS16509 (w3-03). Threat: SLCM backing unproven, treat as separate trust zone (w3-03); nine api-labeled MAHE hosts exist (w3-03).
- **sis.manipal.edu** (MAHE SIS). Role verified: student/parent portal, studloginSLCM.aspx with date field and captcha, redirects to Fee Kart after login (w3-04, w2b-10). Tech: Web Forms .aspx, legacy routes public (w3-04). Cloud: not fingerprinted (w2b-10). Threat: separate from MUJ SLCM, no shared backend proven; payment routes collect application number, name, email, mobile (w3-04).
- **learning.onlinemanipal.com** (LMS). Role verified: D2L Brightspace tenant, "Powered by D2L Brightspace" (w2b-07, w2b-08, w3-13). Tech: CNAME muj.brightspace.com, /d2l/home/14042 (w2b-08, w3-13); learner-mahe.onlinemanipal.com CNAME manipalonline.brightspace.com (w3-13). Cloud: AWS, IPs 13.55.178.159, 15.134.178.12 (w2b-08, w3-13); D2L states AWS primary (w2b-08). Threat: SAML/Entra unverified, grade sync to SIS unknown, CVE-2021-43129 relevance unknown (w2b-08, w3-13).
- **admissions.jaipur.manipal.edu** (NoPaperForms). Role verified: CNAME to jaipurmanipal.nopaperforms.com through AWS ELB ap-south-1 (w2b-06, w3-12). Tech: vendor SaaS, Meritto rebrand June 2023 (w3-12); vendor API modules Lead, Opportunity, Activity, Form, Payment (w2b-06). Cloud: AWS (w2b-06, w3-12). Threat: fields include identity, contact, guardian, documents, payment; admission-to-SLCM bridge undisclosed (w2b-06, w3-12).
- **student.mujonline.com** (online student portal). Role unverified: sparse "Student Portal" shell with Email label and help-desk text (w2b-07). Tech: Angular-style assets, auth protocol unknown (w2b-07). Cloud: none established (w2b-07). Threat: portal auth unknown; separate from campus SLCM (w2b-07).
- **mujconnect.in** (social PWA). Role unverified: "MUJ's Own Social Place", anonymous posts, food chatbot claim; operator unnamed, no privacy policy (w2b-09). Tech: PWA manifest, Let's Encrypt cert from July 2026 (w2b-09). Cloud: A records 98.84.224.111, 18.208.88.157 (w2b-09). Threat: collects full name, username, email, avatar at register; treat as separate trust zone, possible impersonation risk (w2b-09).
- **pay-fee-online** (fee routes). Role verified as directory page: SLCM for academic fees, SpaceBasic for hostel and mess, Canara Bank transfer with MUVAN account rule (w2b-11, w2d-03). Tech: muj-payservices.nttdatapay.com/DirectPay/MUFee is unconfirmed integration lead (w2b-11). Cloud: none for gateway, gateway attribution unknown for all five vendors (w2b-11). Threat: phishing surface via published MUVAN rule and refund bands (w2b-11).

### Other observed assets
- **mujslcm.manipal.edu** (parent). Unverified: A 202.131.155.151, no other records, zero URLScan/Wayback; best hypothesis orphaned or legacy (w3-14).
- **dms.jaipur.manipal.edu / dmsmuj.jaipur.manipal.edu**. Unverified current role: Wayback only, dmsmuj root 2022 read "MUJ API TESTING!", loginForm.aspx titled "MU SLcM" (w3-15); dms@ / ams@ mailboxes are verified escalation contacts in FAQ (w3-15).
- **slcm.manipal.edu** (MAHE SLcM). Verified separate brand, 2017 copyright (w2b-10, w2b-14); shared product family only, shared code/DB/identity unproven (w2b-10).
- **muj.tracmarks.com**. Unverified: MeritTrac branded login, purpose unknown (w2d-02).
- **Library assets**: manipal-koha.informindia.co.in OPAC, DSpace at 20.219.59.68:8080, muj.remotlog.com, mujlibrary.live (unverified) (w2d-07).
- **pas.muj.edu.in** (PAS Portal link from mujone), **muj.irins.org** (research profiles) (w2b-03, w3-10).

## 2) DATA-EXPOSURE HIGHLIGHTS

Public classes found, with digest names. None of these are inside the SLCM auth boundary; SLCM public surface is a login wall only (w2b-02, w2d-09).

- **Faculty and staff directory**: name, designation, department, institutional email, phone, qualifications, external research links (LinkedIn, IRINS, ORCID, Scopus, Scholar), photos claimed; intentional per Public Self Disclosure-U1 (w2d-09, w2b-12). Contact table with 14 role mailboxes and extensions, T&P ext 751 (w2d-09). SLCM FAQ names AMS staff and extensions (Rahul Kumawat 784, Dinesh Sain 738, Rithik Chaudhary 481) (w3-15).
- **SLCM username template and example identifier**: name.registration number, example garv.2506040062, published in official FAQ (w2d-01, w2b-02, w2b-03, w2d-06). Digit split is analyst inference only (w2d-01).
- **PhD admissions result lists**: names, departments, registration mode, NFS/ABSENT status, selected candidates, Jan 2025, Jul 2024, Jan 2026 (w2d-02).
- **Applicant field schema** (admissions SaaS): identity, contact, academic, guardian, employment, uploaded documents, payment, status, refund rules (2022 manual) (w2b-06).
- **Parent OTP workflow**: OTP to registered parent mobile, unregistered numbers told to email admissions@ (w2b-13).
- **Fee artifacts**: hostel and mess amounts, refund bands, Canara Bank IFSC CNRB0003563 and MUVAN account-number construction rule, reconciliation fields UTR, holder, date, amount (w2b-11, w2d-03).
- **Placement data**: NIRF 2025 median salaries with placed-student counts, stipend range INR 15,000 to 1,25,000; conflicting third-party headlines, keep source-labelled (w2d-08).
- **Exam scheduling metadata**: timetable PDFs with course codes, dates, slots, discipline headings (w2d-04).
- **SIS payment pages**: application number, name, amount, email, mobile; receipt emailed; gateway charge table Atom/HDFC 18% GST, undated (w3-04).
- **Credential-like value in library DSpace page title** at 20.219.59.68:8080, value redacted, treated as exposure incident, P0 disclosure (w2d-07).
- **M365 tenant metadata public**: tenant 27282fdd-4c0b-4dfb-ba91-228cd83fdf71, WS-Fed and OIDC endpoints (w3-13, w3-07).
- **mujconnect.in registration**: full name, username, email, avatar, no privacy policy (w2b-09).
- **Historical webmail**: Domain\user name fields in 2006 Exchange OWA capture (w3-05), historical only.

## 3) TOP LEADS

1. Credential-like value exposed in DSpace repository page title, 20.219.59.68:8080. Evidence: P0 exposure incident, redacted (w2d-07).
2. Fee gateway muj-payservices.nttdatapay.com/DirectPay/MUFee, MUJ-branded, integration unconfirmed. Evidence: search-result lead (w2b-11).
3. mujconnect.in unattributed PWA collecting name and email with anonymity claims, no privacy policy. Evidence: page and manifest captures (w2b-09).
4. dmsmuj.jaipur.manipal.edu 2022 root "MUJ API TESTING!" plus loginForm.aspx titled MU SLcM. Evidence: Wayback captures (w3-15).
5. npfslcm.jaipur.manipal.edu in CT with common name mujslcm.jaipur.manipal.edu. Evidence: CT record 2025-11-16 (w3-12).
6. muj.slcm.jaipur.manipal.edu alternate host 20.244.94.89, zero URLScan coverage, FAQ silent. Evidence: DNS + CT + FAQ gap (w2b-01).
7. api.manipal.edu wildcard CORS and opaque root JSON; nginx 1.18.0 (EOL). Evidence: Shodan and live responses (w3-03), observation not vulnerability (w3-03).
8. helpdesk.jaipur.manipal.edu exact-host certs 2026-01-08 while DNS is NXDOMAIN. Evidence: crt.sh IDs 23628924661, 23628923708 (w3-11, w2b-05).
9. faculty-details.php?url=N sequential IDs. Evidence: passive pattern, testing requires authorization (w2d-09).
10. SIS legacy public routes /OnlinePayment01.aspx, /SLCMRTGS01.aspx, /SLCMMessChange04Blocked.aspx. Evidence: live routes with Wayback from 2013 (w3-04).

## 4) HOSTS WITH GAPS

- **mujslcm**: exact stack versions, Akamai claim (unverified everywhere), M365 or Entra federation, port :122 legacy form, backend and database, grade-to-RMS data flow (w2b-01, w2d-03, w3-14).
- **muj.slcm**: role, purpose, alias vs separate deployment, SSL SANs, migration status (w2b-01).
- **mujerp**: audience, enabled modules, tenant, credential mode, MFA status, Azure region, SLCM relation (w2b-02, w3-09).
- **mujone**: SSO role, PAS portal meaning, backend identity, mobile app ownership (w2b-03, w3-08).
- **rms**: Jaipur tenant ownership, credential protocol (Outlook claim is central-host only), CDN placement, result role (none found) (w2b-04, w3-10).
- **helpdesk**: ticketing vendor, production activation, retirement reason, split DNS (w2b-05, w3-11).
- **hms**: MUJ room-booking linkage, current payment provider, origin behind Azure gateway, legacy hostel.manipal.edu status (w3-07).
- **portal**: EPF data scope, deployment date, stack beyond IIS/ASP.NET (w3-06).
- **webmail**: current live markup, Sophos portal confirmation, legacy OWA path state, /26 announcement (w3-05).
- **exam**: purpose, owner, stack, TLS state, SLCM credential bridge (w3-01).
- **uat**: origin bypassability, service-tag and X-Azure-FDID enforcement, datastore lineage, production data presence (w3-02).
- **api**: owner, route inventory, auth policy, SLCM backing, CORS justification (w3-03).
- **sis**: meaning of date field, session internals, federation with MUJ SLCM, current payment processor (w3-04).
- **learning.onlinemanipal.com**: SAML and Entra config, IPSIS grade sync, brightness release level, CVE-2021-43129 applicability (w2b-08, w3-13).
- **admissions**: current form schema (2022 manual baseline), SLCM provisioning trigger, payment processor and tokenization (w2b-06, w3-12).
- **student.mujonline.com**: auth protocol, identity provider, ownership (w2b-07).
- **mujconnect.in**: operator legal identity, MUJ affiliation, data retention, chatbot provider (w2b-09).
- **pay-fee-online**: gateway attribution (all five vendors unknown), callback design, transaction template, receipt layout (w2b-11).
- **dms/dmsmuj**: current DNS and TLS state, DMS expansion, AMS relationship (w3-15).
- **mujslcm.manipal.edu parent**: application identity, ownership, orphan or legacy status (w3-14).

## 5) COVERAGE TABLE

All files read in full, EOF confirmed (truncated false on every read). Chars read equals digest file size in bytes.

| Digest | Chars read | EOF |
|---|---|---|
| w2b-01-muj-slcm-alt.digest.md | 4,771 | true |
| w2b-02-mujerp.digest.md | 4,550 | true |
| w2b-03-mujone.digest.md | 5,058 | true |
| w2b-04-rms.digest.md | 3,540 | true |
| w2b-05-helpdesk.digest.md | 4,800 | true |
| w2b-06-admissions-nopaperforms.digest.md | 5,201 | true |
| w2b-07-student-mujonline.digest.md | 4,690 | true |
| w2b-08-learning-onlinemanipal.digest.md | 5,059 | true |
| w2b-09-mujconnect.digest.md | 4,527 | true |
| w2b-10-sis-manipal.digest.md | 4,737 | true |
| w2b-11-pay-fee-online.digest.md | 5,880 | true |
| w2b-12-jaipur-main-site.digest.md | 4,428 | true |
| w2b-13-parents-campus-life.digest.md | 4,724 | true |
| w2b-14-manipal-edu-group.digest.md | 4,745 | true |
| w2d-01-regnum-format.digest.md | 4,250 | true |
| w2d-02-marks-results.digest.md | 4,806 | true |
| w2d-03-fee-documents.digest.md | 5,537 | true |
| w2d-04-exam-circulars.digest.md | 5,484 | true |
| w2d-05-hostel-transport.digest.md | 5,260 | true |
| w2d-06-orientation-docs.digest.md | 4,844 | true |
| w2d-07-library-integration.digest.md | 4,563 | true |
| w2d-08-placement-data.digest.md | 4,847 | true |
| w2d-09-staff-directory.digest.md | 4,846 | true |
| w3-01-exam-jaipur.digest.md | 5,454 | true |
| w3-02-uat-manipal.digest.md | 5,261 | true |
| w3-03-api-manipal.digest.md | 5,491 | true |
| w3-04-sis-manipal-feekart.digest.md | 5,794 | true |
| w3-05-webmail-manipal.digest.md | 5,789 | true |
| w3-06-portal-manipal.digest.md | 5,278 | true |
| w3-07-hms-manipal.digest.md | 4,710 | true |
| w3-08-mujone.digest.md | 4,776 | true |
| w3-09-mujerp.digest.md | 4,244 | true |
| w3-10-rms-jaipur.digest.md | 4,492 | true |
| w3-11-helpdesk-jaipur.digest.md | 4,487 | true |
| w3-12-npfslcm.digest.md | 4,644 | true |
| w3-13-lms-brightspace-muj.digest.md | 4,516 | true |
| w3-14-mujslcm-parent-level.digest.md | 4,563 | true |
| w3-15-dms-muj.digest.md | 4,995 | true |

Total: 38 files, 185,641 chars, all EOF confirmed.