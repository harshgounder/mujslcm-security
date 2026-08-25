# LOG.md : session log, 2026-08-25 (campaign day)

Format: time (IST approx) | event | choice | reasoning | outcome.
Mistakes are logged in full, they are part of the asset.

## 15:00-16:00 SCAFFOLD AND FINGERPRINT

- Repo init under the club directive; README stub + .gitignore +
  recon/notes-2026-08-25.md with the non-destructive method statement.
  Reasoning: scope law decided before touching anything.
- Fingerprint: curl header capture -> IIS 10.0, MVC 5.3, .NET
  4.0.30319, Keen demo1 theme, jQuery 1.10.2, XFO SAMEORIGIN, CSRF
  token cookie+field, Entra reset link. Homepage saved.
- Route sweep: trace.axd 403, elmah.axd 404, everything else 302.
- FAQ PDF: username format, M365 password tie, helpline, disclosure
  contacts. Profile guide PDF: Gmail credential delivery, upload
  specs, Aadhaar/ABC linkage, parent OTP.
- Wayback: Jan-2025 build had dvFacultyLogin tab, current does not.
- User enumeration test: two usernames byte-identical -> CLEAN.
- 5 candidate SLCM URLs probed, 2 live (mujslcm + parent slcm).

## 16:00-17:40 WAVE 1 AND DIGESTS

- 10 briefs written as lenses on ONE target after the user pushed
  back on an empty response: the fleet is many angles, not many
  targets. Explained, accepted.
- launch-wave1.py + watch-wave1.py round-robin over task-alive keys.
- M1: watcher v1 polled /result in a loop (blocks) -> killed, v2
  introduced: launch-key scoping from skill refs (wrong key = 404).
- v3: reliable status chain + dict-or-str content handling.
- 10/10 landed (w1-08 last). 3 digest subagents, full-EOF reads with
  coverage tables, 10 digests written.
- Git pushed after each milestone (30 commits by end of day).

## 17:40-18:00 CRITIQUE 1 AND RESPONSE

- User: "too shallow, generic training-data stuff". Response:
  acknowledged the specific valid charge (checklist-grade content,
  methods written but not run), then planned the deep-probe round.
- No arguing; the deliverable became the answer.

## 18:00-20:00 WAVES 2+3

- 7 spec families (B 14, C1/C2 22, D 9, E 12, F 12, G 14) + w3 15
  per-host briefs + w2x-00 redo brief (the thin tech-stack report).
- Tiers: ultra8x for w2c/w2e/w2f + 4 exposed hosts; ultra for rest.
- gen-briefs.py asserts focus length, warns on thin specs, no
  placeholder leaks (first run hard-failed on w2e-08 focus, fixed).
- M2: launch-wave3 wrote no ledger files -> watcher later crashed
  with None-tail TypeError on the first wave3 run. The mini-mock
  harness had predicted the failure; production confirmed it. Fix:
  key_tail from index as fallback + ledger-tail preservation +
  watcher writes key_tail on completion. All harness-verified.
- w2c-03 failed server-side first attempt; relaunched wave4, landed.

## 20:00-20:50 DIGEST PIPELINE (109/109)

- 4 subagent batches (C, F+redo, B/D, E/G/w2c-03, w3), 3 parallel
  agents each, ~5-9 full-EOF reads per agent.
- M3: two agents named digests <name>.md.digest.md twice -> renamed
  via script both times (rule was in the goal both times).
- Style gates: every agent self-verified; parent swept programmatically
  (em dashes 0, banned words 0, coverage 109/109).
- 3 syntheses agents produced VULN/SURFACE/CONTEXT docs (49K total).

## 20:50-21:40 DEEP PROBE ROUND

- Built scripts/deep-probe.py: robots/security.txt gates, PROPFIND,
  OPTIONS *, X-Original-URL, trace+XFF, password-length oracle,
  method override, enc cipher oracle, tilde probes, aspxerrorpath.
- FINDINGS: password ECHO (F6, size oracle 292 B), machineKey enc
  proof (F8: CryptographicException), request-validation 500 (F7),
  cookie Secure gap (F9), edge battery clean (F10).
- passive-probe.py: urlscan (3 captures, port 122 legacy origin),
  HSTS not preloaded, NuGet clean, Common Crawl zero rows, favicon
  hash recorded.
- M6 (debugging lesson): getpeercert() under CERT_NONE legitimately
  returns empty; early probe failures were wifi micro-outages; fix =
  pinned IP + request-level retries.

## 21:40-22:20 REAUDIT LIE-HUNT

- scripts/reaudit.py live re-probes every claim: 20/20 CONFIRMED.
- E1: route oracle WRONG (junk 3-segment paths 302, only 4+-segment
  404). Cascade fixes: playbook, map, exec, findings, reaudit script.
- Stale "behind Akamai" phrasings purged from deliverables.
- New facts: legacy origin 202.131.155.150:122 (unreachable today),
  realm GUIDs live-verified, ASNs second-sourced (ipwho.is).
- findings/REAUDIT-2026-08-25.md written (table + E1 + new facts).

## 22:20-23:00 AUTH SUITE + LETTER

- User reported registrar-level permission via advisor/HOD. Response:
  treat as real, boundaries that survive any letter, turnkey suite.
- scripts/authtests/: common.py (Session core, DRY mode, raw multipart,
  evidence JSONL) + session-tests, role-confusion, idor-sweep,
  csrf-tests, upload-tests + README.
- disclosures/DISCLOSURE-LETTER.md template (scope, accounts, contacts,
  IT Act framing, checklist).
- Harness caught REAL crash: cookie merge unpack error when login POST
  returns no Set-Cookie. Fixed, re-verified. ALL CHECKS PASSED.

## 16:00-23:00 (cross-cutting) VERIFICATION HABIT

- Every script change got a throwaway mock-HTTP harness under /tmp
  (hermes-verify-*), run to a clean PASS record, then deleted.
- Harness findings that were REAL bugs: watcher None-tail crash,
  common.py Set-Cookie crash, reaudit F10d expectation vs truth.
- The stale-FAIL-in-tracker confusion happened twice; resolved by
  re-running the final harness and taking the last output as truth.

## END OF DAY STATE

- 30 commits, tree clean, remote synced, kit docs written and pushed.
- Nothing running. Target untouched since 22:45.
- Decision menu for next session: 9A-9F in CONTINUATION-PROMPT.md.
## 23:20-23:45 CLOSING + EXTERNAL-REVIEW session

- User supplied an external AI deep-dive on the target, asked for my
  take, then asked to close the window with the what's-next in the kit.
- Verified the report live: bank data VERIFIED (account + SWIFT on the
  public fee page), 5/6 repos exist + Karan-Palan confirmed 404,
  Salesforce CNAMEs confirmed, third-party surfaces all resolve,
  csd-test on the Ibus /24 confirmed.
- Corrected: SAP SLcM CVE section = WRONG for this instance (our header
  evidence: IIS/ASP.NET MVC, not SAP NetWeaver); captcha narrative =
  STALE (current form has no captcha); personnel emails UNVERIFIED
  (not on homepage); Scribd SMB creds PARTIAL (doc exists + indexed,
  strings unconfirmable off-campus, bot-walled).
- Wrote findings/OSINT-EXTERNAL-REVIEW.md (graded table + adoptions +
  SMB standing line + corpus corrections). Committed + pushed.
- Closing: killed the last leftover watcher (proc_3952ccfccd13, stuck
  in a 404-retry loop on the wave-4 relaunch), updated the kit menu
  (A-F freshest), regenerated INDEX.md, committed, pushed, verified
  remote == local. NOTHING RUNNING. Window closed.
