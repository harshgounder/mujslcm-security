# TRACKER.md: status board

Updated 2026-09-13, after the layer pass, wave 5 and the kit rewrite.

## Phases

| Phase | Status | Notes |
|---|---|---|
| A scaffold and fingerprint recon | DONE | headers, routes, PDFs, DNS, certificate transparency, wayback |
| B wave 1 fleet (10 ultra8x) | DONE | 10/10 reports, digested |
| C waves 2 and 3 fleet (99 runs) | DONE | 109 unique reports, including one relaunch |
| D digest pipeline (109) | DONE | all read to EOF, style-gated, 3 syntheses |
| E deep probe round | DONE | F6 to F10, passive round |
| F reaudit lie-hunt | DONE | 20 of 20 confirmed, E1 fixed |
| G auth suite and disclosure letter | DONE | 6 scripts dry-run verified, template ready |
| H kit (README, INDEX, TRACKER, LOG, continuation) | DONE | rewritten 2026-09-13, INDEX now generated |
| I layer mapping, live | DONE | 46 requests, 61 evidence files, LAYER-MAP L0 to L13, corrections E2 to E5 |
| J gap register and wave 5 | DONE | 25 briefs fired from the register, 25 reports, 1,186,037 chars, digested |
| K scanner toolchain, lab only | DONE | wafw00f, testssl.sh, nmap, nuclei installed; nuclei exercised on a local lab |
| L authorized execution | BLOCKED | needs the signed letter plus two test accounts |
| M build candidates | QUEUED | enc_blob_classifier.py first, six more behind it |

## Fleet ledger

Single source: `wave*-runs.json` plus `ledger/`.

- Launches: 135 (10 + 84 + 15 + 1 + 25)
- Ledger files: 134, key tails only
- Reports and syntheses on disk: 140 files, 5,585,870 chars
- Wave 5 key spread: KJ2lhZ 19, jhBOeM 5, d0rbQA 1, no 402 during the wave
- Failures: one server-side failure in wave 2, relaunched and saved
- Style violations: 0 (swept after every write)

## Findings board

| ID | Title | Sev | Status |
|---|---|---|---|
| F1 | Verbose YSOD, four triggers, customErrors off, build leak | P3 | VERIFIED, byte-level repro |
| F2 | trace.axd 403 with ELMAH 404 | P4 | VERIFIED |
| F3 | Version banners (IIS, ASP.NET, MVC, x-powered-by) | P4 | VERIFIED |
| F4 | jQuery 1.10.2 legacy client stack | P4 | VERIFIED, and confirmed live next to a bundled 3.4.1 |
| F5 | Credential design (M365 password, public username format) | P3 | VERIFIED from official PDFs |
| F6 | Password echo with a response-size oracle | P4 | VERIFIED |
| F7 | Request validation to YSOD class | P3 | VERIFIED |
| F8 | machineKey-protected `enc` parameter | P3 conditional | VERIFIED, refined into a three-stage oracle |
| F9 | Antiforgery cookie HttpOnly without Secure | P4 | VERIFIED live |
| F10 | Edge posture battery | INFO | VERIFIED at the time, amended: WAF status UNKNOWN from outside |
| L1 | Layer map: L0 to L13, live, with raw captures | INFO | VERIFIED-LIVE 2026-09-13 |
| E1 | Route oracle error (302 does not imply existence) | FIXED | caught by the reaudit |
| E2 to E5 | Corrections: my malformed F8 payload, testssl TLS 1.3 read, wafw00f false positive, WAF wording | RECORDED | in `findings/LAYER-MAP.md` |

## Closed clean (probed, no issue)

No user enumeration by response diff. Antiforgery enforced server side. Server-side validation active.
Verb policy tight, GET only in practice. No WebDAV, no tilde short names, no rewrite-header bypass,
no trust-based error-detail bypass. Host header, X-Forwarded-Host and absolute-URI targets ignored.
ELMAH absent. Ports 80 and 8080 filtered, 443 the only reachable port.

## Decision menu

- A: go order for `enc_blob_classifier.py` (spec, opencode, audit, gates, commit). RECOMMENDED.
- B: wave 6 on the thin areas the wave-5 reports flagged themselves.
- C: authorized phase once the letter and the two test accounts exist.
- D: convert the pipeline into a reusable skill.
- E: campus-wide responsible-security one-pager.
- F: keep a change monitor on the certificate and the `enc` oracle, so drift is evidence, not memory.

## Blocked

- Authorized execution: `disclosures/DISCLOSURE-LETTER.md` signed, two test accounts, `SLCM_USER1` and
  `SLCM_USER2` in the environment.
- Restating a verified fact without a fresh re-probe is prohibited by standing order.

## Budget and keys

- Pool: `~/Desktop/parallel spams`, one key per line, newest at the bottom.
- Status of record: `~/parallel-key-tracker/state/status.json`, tier `TASK_ALIVE` is the launch pool.
- Wave 5 spend: 25 runs (19 ultra, 6 ultra8x), carried mostly by one key.
- Note for the next wave: the status file was last probed 2026-09-11, so probe before a large fire.
