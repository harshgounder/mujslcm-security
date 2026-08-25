# OSINT-EXTERNAL-REVIEW.md : graded assessment of the external AI report

Date: 2026-08-25 late. Source: user-supplied external AI deep-dive on the
same target. Method: every load-bearing claim re-checked against primary
sources live (GH API, DNS, page fetches, keyless search). Verdict scale:
VERIFIED, PARTIAL, UNVERIFIED, STALE, WRONG.

## Graded claims

| # | External claim | Live check | Verdict |
|---|---|---|---|
| 1 | Scribd doc "SOP for Matlab 2018 Installation" exists and covers SMB UNC install setup | Doc indexed on Scribd (id 406368004, title matches), snippet shows RUN-command UNC instructions | PARTIAL: doc VERIFIED, exact creds (muj\cbi / muj#1234) NOT confirmable (Scribd bot-wall, search throttled) |
| 2 | Portal runs SAP SLcM, SAP CVEs 2024-42373/45284/34690 apply | Our headers: Microsoft-IIS/10.0, X-AspNet-Mvc 5.3, X-AspNet 4.0.30319, ASP.NET antiforgery. SAP NetWeaver never serves these | WRONG for this instance. SAP lineage is historical (w1-03), not current. Do NOT cite these CVEs |
| 3 | CAPTCHA bypass repos matter (L3thal14 etc.) | Current login form has ZERO captcha (captured 2026-08-25). Repos are 2021-era | STALE: no captcha to bypass today |
| 4 | canaryGrapher/slcmAPI archived | Verified via GH API: archived, pushed 2024-02 | VERIFIED |
| 5 | nikeplusdash/SLCM-api + Heroku app live | Repo exists (archived). herokuapp.com resolves; app returns 404 on / and /docs | PARTIAL: repo VERIFIED, app effectively dead (404) |
| 6 | utk3012/SLCM exists | GH API: exists, pushed 2018 | VERIFIED |
| 7 | KrishGoel/slcm-feedback-automation exists | GH API: exists, pushed 2025-04 | VERIFIED |
| 8 | Karan-Palan/web3-muj-slcm now 404 | GH API: Not Found | VERIFIED (deleted; history not confirmable) |
| 9 | fee page exposes bank details | pay-fee-online.php: Canara Bank, account 120030244406, SWIFT CNRBINBBBFD, student.finance@ all present | VERIFIED |
| 10 | Library portal muj.remotlog.com, reg-num password | DNS: AWS ELB ap-south-1 (proxy vendor). Login policy NOT independently confirmable | PARTIAL: host VERIFIED, policy unconfirmed |
| 11 | Third-party surfaces: mujstella.in, slcm.vercel.app, mujguide.in, arcadiaslcm.vercel.app | All resolve (Cloudflare/Vercel) | VERIFIED (existence) |
| 12 | student.onlinemanipal.com = Salesforce | CNAME to live.siteforce.com (Salesforce Communities) | VERIFIED |
| 13 | manipaluniversity.my.site.com exists | Resolves (Salesforce communities via Cloudflare) | VERIFIED |
| 14 | csd-test.manipal.edu/MUJ-RMS | Resolves 45.112.150.248 = Ibus /24 (our portal.manipal.edu family) | VERIFIED (host) |
| 15 | Personnel emails (Anshuman Mohanty CIO etc.) | NONE found on jaipur.manipal.edu homepage | UNVERIFIED (may exist deeper; not confirmed) |
| 16 | Sikkim Manipal 2012 pastebin breach | Not re-verifiable keylessly today | UNVERIFIED |
| 17 | No MFA for students | Consistent with all our evidence (Entra MFA SOP exists for staff; student SLCM = single password) | PARTIAL/consistent |
| 18 | Reddit complaints (login copy-paste, timeouts) | Community noise | UNVERIFIED, low value |

## Net-new intel this review adds (adopted into the corpus)

- Fee page bank data VERIFIED (account 120030244406, SWIFT CNRBINBBBFD):
  disclosure-relevant only, social-engineering angle for students.
- Deleted-repo evidence: Karan-Palan/web3-muj-slcm existed, now gone
  (404). Deleted repos are a real history risk; GitHub API cannot see
  past content without a prior capture.
- Third-party credential-processor sprawl: mujstella.in, mujguide.in,
  slcm.vercel.app, arcadiaslcm.vercel.app (all verified resolving).
  Each asks students for MUJ creds. Risk = harvesting + pan-cameral
  breach. Goes into the IT Infra advisory.
- Salesforce backbone confirmed: student.onlinemanipal.com (live.siteforce
  CNAME) and manipaluniversity.my.site.com (Cloudflare) = two Communities.
- Library remote proxy live on AWS ELB ap-south-1 (muj.remotlog.com):
  login-policy and reg-num-as-password stay UNVERIFIED until someone
  with an account checks the policy page (documented in TEST-PLAN).
- csd-test.manipal.edu resolves 45.112.150.248: same Ibus /24 as
  portal.manipal.edu. Test-labeled host in production IP space.
- External report claimed port-scanning and scanning-style checks as the
  "AGENT MODE" plan: identical items to our TEST-PLAN, no new classes.

## Standing line on the leaked SMB credentials

The Scribd doc, if it contains live campus-network credentials, is the
single most reportable OSINT item of the whole engagement. Handling:
- NEVER test the credentials, from here or from campus. A leaked
  password is still an authorization boundary; connected testing is
  illegal access even inside the club's letter (the letter scopes the
  web portal only).
- Verify the doc content on campus (Scribd is bot-walled off-campus),
  then include it in the FIRST disclosure to IT Infra with doc ID and
  captured evidence. The university can rotate the account and purge
  the document. This is the kind of finding that makes the club look
  like a security operation.
- The library reg-number-as-password pattern (if confirmed) and the
  third-party harvesters go in the same report as user-facing advisories.

## Corrections to our own corpus

- w1-07 said slcm-app.herokuapp.com "defunct": the host resolves but the
  app returns 404, so "dead in effect" stands, phrasing corrected here.
- No captcha on the CURRENT login form: all captcha-related research
  angles (w2c-06, L3thal14) should be treated as stale background, not
  current surface. Rate limiting and lockout remain untested pre-auth
  (auth-phase item, needs the letter).

## Bottom line

The external report is roughly 30 percent verified-valuable, 30 percent
stale, 20 percent unsupported (SAP CVEs), 20 percent unverified. The
verified 30 percent (bank data, repo sprawl, Salesforce instances,
library proxy, deleted repo, third-party harvesters) is real and now
adopted into the corpus. The SAP section would embarrass the club in
front of IT Infra; do not present it. The Scribd item is the one to
pursue, on campus, as evidence for the first disclosure.[truncated]