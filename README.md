# mujslcm-recon

Security research project for the MUJ Cyberspace Club: reconnaissance and bug
hunting on https://mujslcm.jaipur.manipal.edu/ (MUJ Student Life Cycle
Management portal).

## Scope (field universe)

ONE target: **https://mujslcm.jaipur.manipal.edu/**

Everything else in this repo is evidence, not targets:

- sister instances of the same SLCM product (e.g. slcm.manipal.edu) are read
  only, for product-family intelligence. Same codebase means findings
  transfer, but we never send test traffic there.
- jaipur.manipal.edu / manipal.edu DNS and certificate transparency data is
  passive OSINT about the target's own infrastructure.
- GitHub / paste sites / web archives are read-only sources of code and
  history that mention the target.

Testing rules (club discipline, in force from day 1):

1. Non-destructive only. No data modification, no deletion, no DoS, no
   volume spraying, no automated scanners hammering the origin.
2. Low request rates. Manual and scripted probes stay far below thresholds
   that could be felt as an outage.
3. No credential guessing against real accounts. One throwaway test account
   if the club provides one, nothing else.
4. Nothing is ever published. Findings live in this private repo and go to
   the club lead / university nodal officer via the disclosure path in
   findings/.
5. If something looks live and exploitable (auth bypass, data exposure),
   verify with a minimal PoC on our own test account, document, stop, and
   report. Do not chain further.
6. Workplace consent: club task = authorized testing of this portal per the
   club's mandate. We keep evidence of scope (club brief, lead contact) in
   findings/SCOPE.md.

## Repo layout

    briefs/     research briefs (one per angle, w1 = wave 1)
    research/   parallel.ai deep-research reports (raw outputs)
    recon/      hands-on passive recon artifacts (headers, HTML, notes)
    findings/   curated findings, severity, evidence, disclosure log
    scripts/    launcher + watcher + recon helpers
    ledger/     per-run ledger JSONs
    wave1-runs.json   wave 1 run index (run_id per brief)

## Wave 1 (in flight)

10 parallel ultra8x deep-research runs, each a separate angle on the target:

| brief | angle |
|---|---|
| w1-01 | platform overview: features, login journey, integrations |
| w1-02 | tech stack: MVC 5.3, IIS 10, Keen theme, jQuery 1.10.2, headers |
| w1-03 | vendor family: SLCM product lineage, sister instances |
| w1-04 | security history: incidents, leaks, complaints |
| w1-05 | code leaks: GitHub/paste artifacts referencing the portal |
| w1-06 | student data OSINT: indexed pages, register formats, docs |
| w1-07 | mobile apps + API surfaces that talk to the portal |
| w1-08 | subdomain surface under jaipur.manipal.edu (passive data) |
| w1-09 | attack surface checklist + India disclosure framework |
| w1-10 | Entra ID / Microsoft 365 federation evidence |

## Confirmed recon so far (hands-on, 2026-08-25)

Target: https://mujslcm.jaipur.manipal.edu/

- HTTP/2, server: Microsoft-IIS/10.0, Windows .NET 4.0.30319
- ASP.NET MVC 5.3 (x-aspnetmvc-version: 5.3)
- x-powered-by: ASP.NET (version disclosure, minor)
- X-Frame-Options: SAMEORIGIN present (good) on mujslcm; absent on
  slcm.manipal.edu for comparison
- __RequestVerificationToken anti-CSRF cookie + hidden field on login (MVC
  anti-forgery)
- Login POSTs UserName + Password + hidden EmailFor/LoginFor to "/"
- Password field has no client-side min-length validation
- Redirect target after login: /Home/Index
- Keenthemes "keen" admin theme asset tree
- jQuery 1.10.2 (2013) + jquery.validate + unobtrusive on login page
- Password reset hand-off to https://passwordreset.microsoftonline.com/
  (Microsoft Entra ID tenant in use)
- robots.txt redirects to /Home/Index (no real robots policy)
- slcm.manipal.edu (MAHE instance): IIS 10.0, classic ASP.NET_SessionId
  cookie, no XFO header

## How to rerun the wave

    python3 scripts/launch-wave1.py     # launches 10 runs, ledger + index
    python3 scripts/watch-wave1.py      # polls, saves research/<name>.md

Keys: parallel.ai pool via local key tracker; launch script picks task-alive
keys only and rotates on 402.

## Status

Wave 1 launched 2026-08-25, 10/10 runs accepted. Watch: scripts/watch-wave1.py.