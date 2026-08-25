# EXEC-SUMMARY — MUJ SLCM security research (club deliverable)

Date: 2026-08-25. Repo: github.com/harshgounder/mujslcm-security (private).
Scope: ONE target, https://mujslcm.jaipur.manipal.edu. All methods were
recon-grade, no destructive testing, no auth bypass attempts.

## What this campaign produced

- 110 parallel.ai runs launched, 109 unique reports saved (~4.3M chars)
- Every report read to EOF and digested (109 digests with evidence labels)
- 3 domain syntheses (vuln classes, surface map, context/precedent)
- Hands-on verified findings below, each with raw evidence saved in recon/
- Target-specific test plan and disclosure path (findings/TEST-PLAN.md,
  findings/AGGRESSIVE-PLAYBOOK.md)

## VERIFIED findings (evidence-backed, hands-on)

F1. Verbose .NET error pages. customErrors is off. Two independent triggers:
    POST / without CSRF token returns 500 with full MVC stack trace
    (HttpAntiForgeryException); /Home/Index?enc=zz returns 500 with
    FormatException in System.Convert.FromBase64String. Exact runtime leaked:
    .NET Framework 4.0.30319, ASP.NET 4.7.4136.0. CWE-209. Raw: recon/
    mujslcm-post500.html + enc500.html.
F2. trace.axd returns 403 (exists, restricted) while elmah.axd is 404.
    ASP.NET tracing looks enabled but access-gated. If reachable from an
    allowed network, request traces expose cookies and session IDs.
F3. Version disclosure headers on every response: IIS 10.0, MVC 5.3,
    x-powered-by ASP.NET. Aids precise exploit targeting.
F4. jQuery 1.10.2 (2013) on the login page with known XSS-class CVEs
    (CVE-2015-9251, CVE-2019-11358, CVE-2020-11022/11023). Client-side only,
    impact depends on server rendering of user data.
F5. Credential delivery by design: onboarding guide states SLCM username
    and password are sent to the student's PERSONAL Gmail by the admissions
    department, and the same password protects M365 email and SLCM. One
    credential chain, personal-mail delivery = interception and phishing
    surface. Username format name.registration-number is public knowledge
    (example garv.2506040062 in official FAQ).

## Clean tests (tested, no issue found)

- No user enumeration via login response (random vs admin usernames return
  byte-identical pages)
- Anti-CSRF filter active on login (it is what triggers F1)
- Server-side validation on empty credentials (client validation is not
  the only gate)
- elmah.axd absent; unknown routes 404; all app routes 302 to the login gate
- Verb lockdown: PUT/DELETE/PATCH/TRACE 404 or 411

## Attack surface map (topography)

- Stack: IIS 10, ASP.NET MVC 5.3 on .NET Framework 4.x, Windows, Microsoft
  Azure AS8075 central india (98.70.14.50; NOT Akamai), Entrust DV cert
  (single SAN, issued 2025-12-22), TLS 1.0/1.1 enabled (SSL Labs grade B)
- Identity: 3 separate Entra tenants (jaipur.manipal.edu = 7d0726e8-...,
  muj.manipal.edu = 27282fdd-..., manipal.edu = 29bebd42-...), all Managed,
  no AD FS. SLCM validates locally but password reset delegates to M365.
  MFA mandatory since June 2025 per official SOP.
- Email: SPF hard fail (-all), DKIM selectors present, DMARC p=none on all
  three domains. Spoofing is possible; phishing against SLCM users is the
  realistic attack chain.
- Sibling estate (OSINT only, out of testing scope): muj.slcm (second live
  SLCM host, Azure), mujerp (Business Central ERP), mujone (HR), rms
  (research data), hms (hostel, Azure App Gateway), portal (EPF), uat
  (Next.js behind Azure Front Door), api.manipal.edu (AWS EC2, Express,
  CORS *), exam (BSNL/NIB), sis (MAHE, Fee Kart), lms (Brightspace),
  admissions (NoPaperForms).
- Subdomain takeover candidates: mycampus + testmycampus.jaipur.manipal.edu
  CNAME to edtech366.azurewebsites.net which is NXDOMAIN. REPORT ONLY, do
  not claim.

## Top leads (from 109-report synthesis, evidence-labelled)

1. 13 concrete API routes (grades, marks, attendance, timetable, OTP)
   extracted from a public third-party Flutter client (DK10WS/SLCM_APP).
   BOLA/IDOR testing on those routes is the highest-value auth-phase test.
2. Public credential artifacts: KrishGoel repo .env.example with populated
   credentials, vikrant500 cookies.txt token artifact, public Firebase
   config (SLCM_APP), Anushkakumar10 Django SECRET_KEY with DEBUG=True.
3. Library repository credential-like title exposure on mujlibrary (P0
   check for the club: confirm and redact report).
4. dmsmuj "MUJ API TESTING!" hostname in CT history (labelled test,
   monitor reactivation).
5. Register-number enumeration vector: format is public, batches bounded;
   stuffing is a realistic risk; report to admins, never execute.
6. Parent login is OTP-gated per official manual; parent mobile numbers are
   captured in onboarding (OTP interception class risk to test later).
7. Fee flow split across SLCM + SpaceBasic + NTT DATA Pay + Razorpay
   (certificates): payment integrity is a business-logic test class.
8. Upload surface: onboarding requires PDF docs (max 1MB) + photo (jpg,
   100KB). File-upload validation testing belongs in the auth phase.
9. MachineKey/ViewState: MVC 5.3 with WebForms sibling hosts; YSOD proves
   verbose errors; machineKey exposure unproven but conditionally high
   impact (code injection if leaked). Check GitHub for keys.
10. Origin masking: direct A record to Azure, no WAF evidence, no challenge
    pages observed; WAF posture is unverifiable from outside.

## Disclosure path (do this BEFORE any active test beyond recon)

1. Registrar office: registrar@jaipur.manipal.edu (Dr Amit Soni,
   +91 141-3999100 ext 102) plus IT Infra it.support@jaipur.manipal.edu
   (ext 144) per official FAQ.
2. Present the recon packet above; ask for written scope: test accounts,
   listed in-scope hosts, signed authorization (IT Act 43/66 context).
3. 90-day private disclosure window; optionally report to CERT-In
   (RVDCP) after the club resolution.
4. Never publicize findings before the university responds; no press, no
   public repos with student data.

## What the club can do with this

- Present the verified recon packet and the target-specific playbook as the
  club's first deliverable (executives get a working security program, not
  a CTF demo).
- Run the auth-phase tests from findings/AGGRESSIVE-PLAYBOOK.md under
  seniors with written authorization: IDOR on the 13 API routes, upload
  validation, fee flow integrity, session fixation, role confusion
  (EmailFor/LoginFor), trace.axd from campus IP.
- Track reactivation of test-labelled hosts (dmsmuj, helpdesk, npfslcm).

## Repository map

- findings/FINDINGS-W0.md (verified), TEST-PLAN.md, AGGRESSIVE-PLAYBOOK.md,
  ATTACK-SURFACE-MAP.md, REAUDIT-2026-08-25.md (lie-hunt corrections)
- research/ 109 reports + digests/ 109 digests + 3 syntheses + DIGEST-W1/W2
- recon/ raw evidence (headers, YSOD pages, PDFs, DNS, CT, wayback)
- scripts/ launcher + watcher + brief generator (reusable for wave 4+)
- briefs/ 110 prompts (replayable)