# TRACKER.md : status board (updated 2026-08-25 end of day)

## Phases

| Phase | Status | Notes |
|---|---|---|
| A scaffold + fingerprint recon | DONE | headers, routes, PDFs, DNS/CT, wayback |
| B wave 1 fleet (10 ultra8x) | DONE | 10/10 reports, digested |
| C waves 2+3 fleet (99 runs) | DONE | 109 unique saved incl. w2c-03 relaunch |
| D digest pipeline (109) | DONE | all read-to-EOF, style-gated, 3 syntheses |
| E deep probe round | DONE | F6-F10, passive round, findings doc |
| F reaudit lie-hunt | DONE | 20/20 confirmed, E1 fixed, REAUDIT doc |
| G auth suite + letter | DONE | 6 scripts verified, template ready |
| H kit (README/INDEX/TRACKER/LOG/CPROMPT) | DONE | this commit |
| I wave 5 research | QUEUED | decision A |
| J authorized execution | BLOCKED | needs signed letter + 2 test accounts |

## Fleet ledger (single source: wave*-runs.json + ledger/)

- Launches: 110 (10 + 84 + 15 + 1 relaunch)
- Unique saved reports: 109 (sizes 11,445 B to 56,898 B, total ~4.0M chars)
- Failed server-side: w2c-03 (first attempt only; relaunch saved)
- Digests: 109/109. Syntheses: 3. Style violations: 0 (swept twice).

## Findings board

| ID | Title | Sev | Status |
|---|---|---|---|
| F1 | Verbose YSOD multipath (4 triggers), customErrors off, build leak | P3 | VERIFIED, byte-identical repro |
| F2 | trace.axd 403 restricted | P4 | VERIFIED |
| F3 | Version banners (IIS/MVC/.NET/x-powered-by) | P4 | VERIFIED |
| F4 | jQuery 1.10.2 XSS-class CVEs | P4 | VERIFIED, impact conditional |
| F5 | Credential design (M365 single pw, Gmail delivery) | P3 | VERIFIED (official PDFs) |
| F6 | Password echo on failed login (+292 B size oracle) | P4 | VERIFIED, encoded, no XSS |
| F7 | Request-validation input -> F1 YSOD class | P3 | VERIFIED |
| F8 | enc = machineKey-protected blob (CryptographicException) | P3 cond | VERIFIED; key-leak = P1 |
| F9 | Anti-CSRF cookie HttpOnly, no Secure | P4 | VERIFIED |
| F10 | Edge posture battery all clean | INFO | VERIFIED |
| E1 | Route oracle error (302 != exists) | FIXED | found by reaudit, cascade-corrected |

Clean tests (no issue): no user enumeration, anti-CSRF filter active,
server-side validation active, verb lockout, no WebDAV, no tilde 8.3,
no rewrite-header bypass, XFF no trace unlock.

## Open items (decision menu)

- A wave 5 (needs nothing): machineKey hunt, legacy-origin forensics,
  port-122 story, post-login route confirmation AFTER auth, sibling
  grade cards. RECOMMENDED next.
- B letter pre-fill (club details only).
- C disclosure timing plan.
- D pipeline skill conversion.
- E reactivation monitor cron.
- F campus-wide responsible-security one-pager.

## Blocked

- J authorized execution: registrar letter (disclosures/
  DISCLOSURE-LETTER.md) + two test accounts + SLCM_USER1/2 env.
- Verified-facts changes without re-probe: prohibited by standing
  order 3.5.

## Budget/keys

- Pool: ~/Desktop/parallel spams, 285 lines (newest at bottom).
- Task-alive status: ~/parallel-key-tracker/state/status.json.
- Spend this campaign: 10 ultra8x (wave 1) + 84 mixed (wave 2) +
  15 (wave 3) + 1 relaunch. Remaining balance untouched since.