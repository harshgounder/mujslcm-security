# DIGEST-W1 — Wave 1 synthesis (10 ultra8x reports)

Merged 2026-08-25 from research/w1-*.md via subagent digests (each read to
EOF, coverage audit inline). w1-08 subdomain-surface pending (CT heavy).
All claims below are EVIDENCE TRIAGE: read the parent report before acting.

## Coverage audit

w1-01 39,357 (full) | w1-02 12,321 (full, THIN report, redo launched as
w2x-00) | w1-03 37,324 (full) | w1-04 40,265 (full) | w1-05 47,931 (full)
| w1-06 43,659 (full) | w1-07 37,483 (full) | w1-09 46,547 (full) |
w1-10 44,955 (full)

## Verified platform facts (cross-report consensus)

- Product: SLCM = student life-cycle management (attendance, marks,
  results, broadcasts; MAHE ICT inventory doc). NOT an LMS. Admission
  -> profile -> every student admin function.
- MUJ front-end: ASP.NET MVC 5.3 / .NET 4.x / IIS 10 on Azure central
  india (AS8075, edge IP 98.70.14.50). Form posts UserName/Password +
  EmailFor/LoginFor to "/", MVC antiforgery enforced (F1 verified).
- Legacy MAHE family: WebForms (.aspx): loginForm.aspx, GradeSheet.aspx,
  Print.aspx, WebForm1.aspx, StudentChangePassword.aspx + __VIEWSTATE/
  __EVENTVALIDATION + txtCaptcha. Different generation, same product.
- Two near-identical MUJ entrances: mujslcm.jaipur.manipal.edu and
  muj.slcm.jaipur.manipal.edu (alias/sibling; OUT OF SCOPE to touch).
- Identity: 3 Entra tenants, all Managed (no AD FS); SLCM pw = M365 pw;
  reset via passwordreset.microsoftonline.com; MFA mandatory per
  internal SOP (June 2025) yet published publicly.
- Email posture: SPF -all; DMARC p=none on all domains; Exchange Online
  MX. Spoofing possible (phishing risk to students, not a portal bug).
- Client: jQuery 1.10.2 (2013) + validate 1.11.1; Keen demo1 theme;
  X-Frame-Options only; no CSP/HSTS/nosniff (SecurityHeaders D grade,
  SSL Labs B, TLS 1.0/1.1 live, BEAST warnings).

## Highest-value findings per report

- w1-01: exact attendance route /Student/Academic/AttendanceSummaryForStudent
  (login-gated); fee split SLCM (academic, processor undisclosed) /
  SpaceBasic (hostel+mess) / NTT DATA (mess form) / Razorpay (certificates).
  First-Year-Students-Profile-Registration-Guide.pdf not extractable,
  re-OCR it. Contact tree: registrar (Dr Amit Soni, ext 102), dms@, ams@,
  it.support@, student.finance@, exam.store@, exam.helpdesk@.
- w1-02: header/exposure audit; TLS weak config; jquery CVEs range
  membership (CVE-2015-9251, CVE-2019-11358, CVE-2020-11023); no exact
  theme version; report thin (12K) so full redo launched.
- w1-03: SAP SLcM lineage (2 Manipal Global employee profiles); MAHE
  2026 Salesforce modernization (Deloitte, Agentforce, MuleSoft; MUJ not
  named); public repos model the auth flow: canaryGrapher/slcmAPI
  (archived), DK10WS/SLCM_APP (Flutter + public google-services.json),
  AddisionS/slcm-feedback-form-filler, Anushkakumar10/muj_slcm (
  Django SECRET_KEY + DEBUG=True PUBLIC).
- w1-04: NO confirmed breach anywhere in public record. Brinztech
  2026-02-18 libportal.manipal.edu leak ALLEGATION (unsubstantiated,
  tier 2). LeakRadar 59,820 manipal.edu-associated credentials (not
  attribution). CERT-In 70B: 6h incident reporting, 180d logs. URLScan:
  mujslcm NOT observed; slcm clean x2. No CVEs in NVD/Exploit-DB.
- w1-05: slashdot-level code intel: 4 GitHub repos + npm yemit automate
  SLCM flows; credentials accepted via GET-able handlers (slcmAPI);
  LeakIX 117 service records incl dev-api/dev-techtatva/dev-register;
  CertSpotter 103 manipal.edu names incl dev/uat/preprod; slcm-api.ml +
  slcm-app.herokuapp.com = historic credential-phish vectors still
  possibly live (verify).
- w1-06: biggest PUBLIC data exposure = official PhD PDFs under
  jaipur.manipal.edu/img/pdf/: awardee list (500-scale: names + reg
  numbers + theses) and shortlist PDFs (names + EMAILS + application
  numbers). Register format numeric (FAQ) contradicts 24JTEECS001 claim.
  Retired MAHE routes (Print.aspx etc.) in archives. No marks/hostel/
  fee rosters found.
- w1-07: CampusAdda (com.app.campusadda, Razorpay, OTP, deep links incl
  carpool share tokens; AASA/assetlinks verified) is the clearest native
  app surface; MUJStella (PWA+Android, unaffiliated, SLCM tracker);
  MTTN (10K+, attendance/grades, push); MUJ gym app by Gayatri Software
  (credentials+diet data). NO verified /api/ or Swagger for mujslcm.
- w1-09: FULL test playbook (see TEST-PLAN.md): IDOR method (2 accounts,
  1 variable), role confusion via EmailFor/LoginFor (server must re-
  derive role), machineKey campaign reference (Feb 2025 Microsoft blog:
  leaked machineKeys -> code injection), disclosure = registrar first,
  CERT-In RVDCP coordination, 90d window. FLAG: projectzero.google URL
  likely fabricated in that report.
- w1-10: 3 Entra tenants mapped (GUIDs + aliases above); DMARC p=none;
  SSPR two-step; SLCM fed unproven; confused-deputy risk: suffix-only
  trust across tenants; SOP PDF "For Internal Use Only" but public
  (real finding).

## Cross-cutting attack leads (for THE club report)

1. YSOD verbose errors (F1) -> customErrors misconfig: with auth creds,
   probe other error triggers for deeper leaks (connection strings,
   paths, machine names).
2. trace.axd 403 (F2): tracing enabled + restricted; Azure-level or
   IIS-level access control to test from allowed networks (club scope).
3. Legacy family teach-in: MAHE WebForms endpoints (.aspx) hint at
   what MUJ's MVC replaced; endpoint names from archives are checking
   leads IF the same app serves both (no evidence yet).
4. Public Django secret + Firebase config: if any of these prototypes
   was ever wired to live services, that is a finding class. Verify
   deployment scope before claiming anything.
5. Fee flows: multiple processors (SLCM, SpaceBasic, NTT DATA, Razorpay)
   = fragmented payment surface; tamper tests belong to auth phase.
6. Email spoofing (p=none) enables targeted "fee pending" phishing
   against students; the INR 487,000 Reddit complaint proves the hook.
7. Third-party app layer (CampusAdda deep links, MUJStella, MTTN) is
   unmanaged attack surface FROM the user side; club can demo the risk
   without touching MUJ assets.
8. Username predictability (name.regnum from public PDFs) + M365
   password = spray risk; that is a disclosure-path finding for MUJ,
   not something we execute.

## Open items

- w1-08 subdomain-surface (running)
- w2x-00 tech-stack redo (launched; w1-02 was too thin)
- Wave 2 fleet: 84 runs in flight (families B-G + redo)
- Verify: projectzero.google URL, Brinztech claim, Scribd student-list
  files, slcm-api.ml/slcm-app.herokuapp.com status, async details
- Re-OCR: First-Year-Students-Profile-Registration-Guide.pdf