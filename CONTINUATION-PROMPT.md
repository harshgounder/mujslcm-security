# CONTINUATION-PROMPT.md : resume kit for the next session

Read TOP TO BOTTOM before doing anything. This document is the single
source of truth for where the mujslcm-security project stands, what was
decided and WHY, what is block, and what comes next.

Generated: 2026-08-25 (end of campaign day). Repo HEAD at generation:
f271604 (plus kit commit). Tree clean. Remote synced.

═══════════════════════════════════════════
1. MISSION
═══════════════════════════════════════════

MUJ CyberSpace club (user is 2nd-year E&CE, club member) wants to find
exploits and bugs in the official MUJ student portal, collect as much
data as parallel.ai permits, and present a credible security program
(wave-based deep-research fleet + hands-on recon + disclosure path).
ONE target: https://mujslcm.jaipur.manipal.edu. Everything is written
down, evidence-backed, and replayable. The aggressive phase is gated
behind a registrar-signed scope letter (user reports the advisor/HOD
can obtain one) plus two test accounts.

Standing conviction from the user: work must be SPECIFIC, not generic.
Two explicit critiques during the day: "too shallow, only training-data
stuff" and "you are not even aware of the tools and patterns that
exist". The answer built into this repo: every claim either has raw
evidence in recon/ or carries an UNVERIFIED/INFERENCE label; every
technique in the playbooks was actually RUN (deep-probe round) or is
packaged turnkey (authtests). Any future session that adds a method
must also add the evidence for it.

═══════════════════════════════════════════
2. REPO FACTS
═══════════════════════════════════════════

- Remote: https://github.com/harshgounder/mujslcm-security (PRIVATE, verified via gh api)
- Local: /home/liebert511/mujslcm-recon, branch main
- Git identity: liebert511 <liebert511@users.noreply.github.com>
- 529 tracked files (excl. .git and __pycache__), 30 commits at kit time
- .gitignore: __pycache__/, *.pyc, .env, .DS_Store, research/*.md.part
- NEVER commit: full parallel.ai keys, test-account passwords, signed
  letter scans with signatures. Ledgers hold key TAILS only (last 5-6
  chars), which is the established acceptable form.

═══════════════════════════════════════════
3. STANDING ORDERS (do not regress)
═══════════════════════════════════════════

3.1 Non-destructive testing until a signed scope letter exists.
     - Single low-rate requests (>=1s apart), synthetic data only.
     - No scanners (nuclei, nikto, wpscan...). No volume fuzzing.
     - No auth attempts. No requests to sibling hosts (muj.slcm,
       mujerp, mujone, rms, exam, uat, api.manipal.edu, hms, portal,
       sis, helpdesk, npfslcm, lms, dmsmuj, mycampus, testmycampus).
       They are OSINT-only topics.
     - No subdomain takeover claiming (mycampus/testmycampus are
       REPORT-ONLY candidates).
3.2 Even with the letter: no credential stuffing/spraying, no
     exfiltration (max 1 redacted proof record), no DoS, no real-money
     payment manipulation, no persistence, no cross-account deepening
     after first IDOR proof. State-change tests only on the club's own
     test accounts with benign values.
3.3 Repo conventions: user style rules are HARD (no em dashes, no
     AI-tell words from the 2026-08-13 directive (standard filler list, never used as prose)). Commit often, push at milestones, keep the
     remote in sync. Private repo stays private.
3.4 Parallel.ai rules: runs are LAUNCH-KEY-SCOPED (status/result must
     use the launching key, others 404). Never poll /result in a loop
     (it blocks). Ledger + wave index are the launch records.
3.5 Evidence discipline: every finding gets raw evidence (body file,
     headers, timestamps) in recon/ and a pointer in the findings doc.
     AI research output is ALWAYS labelled UNVERIFIED until re-probed.
3.6 The reaudit mindset (user-ordered): when asked to recheck, assume
     every prior capture may be wrong; re-derive from raw; document
     corrections as E-codes (E1 precedent).

═══════════════════════════════════════════
4. CURRENT STATE (counts and status)
═══════════════════════════════════════════

- Research fleet: 110 launches (wave1 10 + wave2 84 + wave3 15 + wave4
  1 relaunch), 109 unique reports saved to research/*.md, ~4.0M chars
  of reports + ~290K chars of digests. w2c-03 initially failed
  server-side, relaunched as wave4, landed 49,031 B.
- Digests: 109/109, one per report, each with REPORT/ANSWER SUMMARY/
  KEY FACTS/ACTIONABLE LEADS/FLAGS/COVERAGE sections, all read-to-EOF
  proven, all zero style violations (swept programmatically).
- Syntheses: VULN-CLASS-SYNTHESIS.md (16.2K, C+F families),
  SURFACE-SYNTHESIS.md (17.2K, B+D+w3 hosts), CONTEXT-SYNTHESIS.md
  (15.9K, E+G precedent/footprint). DIGEST-W1.md + DIGEST-W2.md index
  them.
- Verified findings: F1-F10 (see section 5). Reaudit: 20/20 live
  rechecks confirmed, 1 error found and cascade-fixed (E1 route
  oracle), stale Akamai phrasing purged from deliverables.
- Auth suite: 6 scripts + README in scripts/authtests/, all verified
  (syntax, mocked-login, dry-run full suite, evidence JSONL emission).
- Workshop status: NOTHING running. No background processes, no
  pending delegations, no cron. Target untouched since the last
  reaudit probe (~22:45). Keys idle.

═══════════════════════════════════════════
5. VERIFIED FACTS INVENTORY (F1-F10)
═══════════════════════════════════════════

F1  Verbose .NET error pages, customErrors OFF, MULTIPATH (P3):
    trigger A: POST / without __RequestVerificationToken -> HTTP 500,
    8,319 bytes, HttpAntiForgeryException, full MVC stack trace,
    ASP.NET Version:4.7.4136.0 (reproduced byte-identical in reaudit).
    trigger B: /Home/Index?enc=zz -> 500 FormatException (base64).
    trigger C: valid-base64 enc -> 500 CryptographicException, proves
    the enc blob is machineKey/DPAPI-protected (see F8).
    trigger D: password containing < or > -> 500 (ASP.NET request
    validation fires, still an error-page leak).
    Evidence: recon/mujslcm-post500.html, recon/enc500.html,
    recon/reaudit/*.
F2  trace.axd -> 403 (exists, restricted; X-Forwarded-For 127.0.0.1
    does NOT unlock). elmah.axd -> 404. (P4)
F3  Version banners on every response: IIS 10.0, X-AspNetMvc 5.3,
    X-AspNet-Version 4.0.30319, X-Powered-By ASP.NET. (P4)
F4  jQuery 1.10.2 (2013) on the login page, known XSS-class CVEs
    (2015-9251, 2019-11358, 2020-11022/11023). Client-side only.
F5  Identity design: SLCM password = Outlook/M365 password; username
    = name.regnum (example garv.2506040062 from the OFFICIAL FAQ PDF);
    credentials delivered to personal Gmail by admissions (official
    onboarding guide); reset delegates to passwordreset.microsoftonline.com.
F6  Password echo on failed login (P4): server re-renders the password
    into the input value attribute, HTML-encoded (no XSS), any length
    accepted (no server-side maxlength); size delta 8-vs-300 chars =
    292 bytes, reproduced twice. Evidence: recon/probes/pw-*.html.
F7  F1-family extension: dangerous form input -> 500 YSOD class (see F1
    trigger D). The error-page issue is systemic, not one route.
F8  ReturnUrl enc is machineKey-protected (P3 conditional): Format-
    Exception on non-base64, CryptographicException on valid base64.
    If the machineKey ever leaks publicly (GitHub), encrypted-data
    tampering and code injection become possible. Keep on the risk
    register; hunt for the key in wave 5.
F9  Anti-CSRF cookie: HttpOnly, NO Secure flag (P4). Evidence:
    recon/probes/home-headers.txt.
F10 Edge posture, ALL CLEAN (verified, no issue): PROPFIND 404 (no
    WebDAV), OPTIONS * 400, tilde 8.3 probes 400 (disabled),
    X-Original-URL/X-Rewrite-URL inert, robots/sitemap/security.txt
    302-gated (no security.txt = no VDP signal), aspxerrorpath inert.

ROUTE TRUTH (corrected, was E1): the pre-auth gate 302s EVERY <=3-
segment path (/zzz.aspx, /Content/nonexistent.css, /api/values,
/Home/zzz all 302). Only 4+-segment paths 404 (/Foo/Bar/Baz/Quux) and
.axd handlers diverge (trace 403, elmah 404). 302 does NOT prove route
existence. Route-name knowledge comes from third-party client code
(w2c-20: 13 routes) and post-auth traffic, NOT from probes.

ESTATE (second-source verified): 98.70.14.50 = AS8075 Microsoft Azure
(Pune) per ip-api AND ipwho.is; 20.244.94.89/20.244.0.229 = Azure;
52.172.36.15 = Azure south india; 59.91.192.229 = AS9829 BSNL (exam);
43.205.223.7 = AS16509 Amazon (api.manipal.edu); 202.131.155.153 =
AS134039 Ibus (rms). Three Entra realms live-verified via
openid-configuration: jaipur.manipal.edu 7d0726e8-bf4b, muj.manipal.edu
27282fdd-4c0b, manipal.edu 29bebd42-f1ff. DMARC p=none on all three.
mycampus/testmycampus CNAME -> edtech366.azurewebsites.net, A empty =
NXDOMAIN (takeover candidates, report only). uat.manipal.edu CNAME ->
uat-ci-mahe-ep-...azurefd.net (Azure Front Door). Legacy origin:
urlscan 2024-11-20 shows mujslcm on 202.131.155.150:122 (Ibus family);
both ports unreachable today; migration marker, not an active claim.

═══════════════════════════════════════════
6. TOP LEADS (evidence-labelled)
═══════════════════════════════════════════

L1  Thirteen API routes from third-party Flutter client DK10WS/
    SLCM_APP (grades, marks incl. MTE1/MTE2/CWS/ETE/PRS/Total fields,
    timetable, CGPA, OTP): BOLA/IDOR is the top auth-phase test.
    Label: VERIFIED (routes in public client code), UNVERIFIED (server
    behavior). Evidence: w2c-20 + digests.
L2  Public credential artifacts: KrishGoel repo .env.example with
    populated credentials, vikrant500 cookies.txt token artifact,
    public Firebase config (SLCM_APP), Anushkakumar10 Django SECRET_KEY
    with DEBUG=True. Verifiable on GitHub; do NOT use, document only.
L3  Library repository credential-like title exposure on mujlibrary
    (P0 club check with librarian; w2d-07).
L4  Register-number enumeration: format public (name.regnum), batch
    arithmetic bounded; stuffing is a reportable risk, never execute.
L5  Parent accounts OTP-gated (official manual); parent mobile numbers
    captured during onboarding (OTP interception class, test in
    auth phase).
L6  Fee flow split: SLCM + SpaceBasic + NTT DATA Pay + Razorpay certs;
    payment integrity as a business-logic test class (auth phase).
L7  Upload surface: onboarding requires PDF <=1MB + photo jpg <=100KB;
    upload validation tests packaged (upload-tests.py).
L8  machineKey exposure risk: enc blob proven encrypted (F8); search
    GitHub for keys in wave 5; if leak found, severity jumps to P1.
L9  Edge/WAF: direct A record to Azure, no WAF evidence, no challenge
    pages; front-door vs origin parity is a test item, do not frame as
    an Akamai bypass.
L10 Disclosed orphan assets: helpdesk (NXDOMAIN + CT certs 2026),
    npfslcm CT record, dmsmuj "MUJ API TESTING!" label; monitor
    reactivation (cron candidate).

═══════════════════════════════════════════
7. TIMELINE OF THE DAY (choices, reasoning, mistakes)
═══════════════════════════════════════════

ALL DATES 2026-08-25.
- 15:00-ish scaffold: repo created under the club directive; method
  statement written FIRST (non-destructive) because scope law matters.
- Fingerprint round: curl probes, header capture, form mapping
  (CSRF token, EmailFor/LoginFor, Keen theme, jQuery). Route sweep.
- FAQ + profile-guide PDFs pulled from the public site: identity
  format, M365 password tie, credential delivery via personal Gmail,
  upload specs. JACKPOT find, primary source.
- WAYBACK catch: old build had a Faculty login tab, current does not.
- Wave 1: 10 ultra8x briefs = 10 lenses on ONE target (explained to
  user after an empty-response pushback).
- WATCHER TECH DEBT: first watcher polled /result in a loop (blocks).
  Killed and rewrote. Second version got key scoping wrong. Third
  version correct, from skill refs. Mistake logged; never poll /result.
- 9/10 wave-1 reports landed; digest subagents (3 parallel, full-EOF
  reads with coverage tables). w1-08 ran long, digest came later.
- User critique #1: "too shallow, generic training-data stuff". Response:
  acknowledged the valid core, then built the deep-probe round (see 8)
  instead of arguing.
- Wave 2+3: 7 spec families + per-host briefs; tiered processors
  (ultra8x for C/E/F and exposed hosts), pro-fast never used.
  Launch-wave3 omitted ledger writes -> watcher later crashed with
  None-tail TypeError (the harness had predicted this failure mode in
  the mini-mock; the production crash confirmed the fix was needed,
  index key_tail fallback added). MULTIPLE harness-verified fixes.
- 109 digests: 4 subagent batches; two agents produced
  <name>.md.digest.md double extensions twice; normalized via script
  both times (agents were given the naming rule, still slipped).
- Syntheses + DIGEST-W1/W2 + EXEC-SUMMARY.
- User critique #2 (deep probe request): "go all out, tell me what you
  won't do". Delivered: methods-per-gap playbook + boundary list +
  deep-probe round: password echo oracle discovery (F6), enc oracle
  (F8), cookie audit (F9), edge-posture battery (F10), passive round
  (urlscan port 122 legacy origin, HSTS not preloaded, NuGet clean,
  Common Crawl clean).
- User: registrar-level permission claim (via advisor/HOD). Response:
  treat as real, keep boundaries that survive even a signed letter,
  build the turnkey suite + letter template.
- Lie-hunt (user-ordered): scripts/reaudit.py, 20/20 live rechecks.
  ONE REAL ERROR: E1 route oracle (302 != exists). Cascade fixes in
  four docs, stale Akamai lines purged, REAUDIT-2026-08-25.md written.
  Legacy origin + realm GUIDs added as new facts.
- Auth suite built; harness caught a real crash (Set-Cookie absent on
  login POST -> unpack error), fixed, re-verified (ALL CHECKS PASSED).
- 23:0x kit: README/INDEX/TRACKER/LOG/CONTINUATION-PROMPT.

MISTAKES WORTH REMEMBERING (so nobody repeats them):
M1 watcher v1 polled /result in a loop (blocks).
M2 watcher crash on ledger-less runs (None endswith), caught by mock
   harness BEFORE production, then hit production anyway on wave3.
M3 agents renamed digests wrongly twice (harness-ignored, fixed by script).
M4 route-oracle claim overreached (E1): corrected, cascade-fixed.
M5 Akamai assumption from an IP range guess: WRONG, Azure AS8075,
   corrected same day, purged from deliverables.
M6 cert-getpeercert() confusion during deep-probe debugging: empty
   dict under CERT_NONE is EXPECTED (verification off = no parsed
   cert), the real cause of early probe failures was wifi micro-
   outages; pinned-IP + retries solved it.
M7 write_file truncation on big payloads: DIGEST-W2 came back 217 B
   once; kept files < ~30K chars after that.

═══════════════════════════════════════════
8. HOW THE PIPELINE WORKS (reuse guide)
═══════════════════════════════════════════

Brief generation: scripts/brief-specs-{b,c1,c2,d,e,f,g,w3}.py hold
(slug, focus_text) tuples. scripts/gen-briefs.py wraps them, adds the
HEADER (verified baseline) + DEMAND blocks, validates focus length,
writes briefs/wN-*.txt. Add a family by dropping a spec file and
adding it to FAMILIES.

Launch: scripts/launch-waveN.py reads briefs, reads the key pool at
~/Desktop/parallel spams (newest keys at the BOTTOM), filters
task-alive from ~/parallel-key-tracker/state/status.json, round-robins
launches, writes ledger/<name>.json (run_id + key_tail) + waveN-runs.json.
Tiers: ultra8x for deep classes; ultra for breadth. 402 -> next key.
Retry once on transport errors.

Watch: scripts/watch-wave1.py loads ALL waveN-runs.json, uses the
ledger key_tail (or index key_tail) to scope status/result fetches,
extracts status via the reliable chain (run.status -> status -> state),
saves str content as .md and dict content as .json + flattened .md,
updates ledgers, re-verifies style. --once for a single pass.

Digest: subagent batches, 3 agents, ~5-9 reports each, contract:
read to EOF (truncated:false proven), six sections, exact URL key
facts, style gate, DONE lines. Then family syntheses, then the merge.

Verify: scripts/reaudit.py re-probes every finding LIVE and prints a
PASS/FAIL table. Run it whenever the target's behavior matters again.

Execute under auth: scripts/authtests/*, env contract in common.py
(SLCM_USER1/2, SLCM_PASS1/2, SLCM_DRY, SLCM_RATE, SLCM_TARGET,
SLCM_IP, SLCM_EVID). Dry-run first (SLCM_DRY=1) prints the plan and
sends nothing.

═══════════════════════════════════════════
9. OPEN ITEMS AND DECISION MENU
═══════════════════════════════════════════

BLOCKED (external): the aggressive phase. Needs (a) the signed scope
letter (template: disclosures/DISCLOSURE-LETTER.md; user said advisor/
HOD can get registrar sign-off), (b) two test accounts named in it.
Until those exist: recon-grade probes only, and the reaudit script is
the only live-touch tool.

OPEN (agent can do now, user must pick):
  A. Wave 5 research fleet (~15-20 briefs, ultra8x for machineKey hunt
     + legacy-origin forensics; ultra for rest). Zero prerequisites.
  B. Letter draft pre-filled with club details (advisor, SPOC, dates)
     so only the signature is missing.
  C. Disclosure-timing plan: immediate per-finding vs end-of-engagement
     report vs after remediation.
  D. Skill conversion: package the fleet pipeline (briefs -> launch ->
     watch -> digest -> synthesize -> reaudit) as a reusable skill.
  E. Cron candidate: monitor dmsmuj/helpdesk/npfslcm/reactivation and
     the target's headers for change (weekly, read-only, deliver to
     telegram if wired).
  F. Campus-wide writeup: take this package and generalize it into the
     club's "responsible security program" one-pager for exec apps.

KNOWN UNVERIFIED (do not upgrade without evidence):
  - All wave-2/3 report claims that never got a live re-probe.
  - machineKey composition (only the crypto-protected blob is proven).
  - jQuery CVE range contradiction (w2f-03 vs w2x-00: NVD ranges
    differ; resolve before any final CVE count).
  - MFA mandatory June 2025 (from public university SOP; INFERENCE).
  - Anything labeled INFERENCE in the syntheses.

═══════════════════════════════════════════
10. COMMANDS CHEAT SHEET
═══════════════════════════════════════════

cd ~/mujslcm-recon
git status && git push -q origin main          # keep remote current
python3 scripts/gen-briefs.py                   # (re)generate briefs
python3 scripts/launch-waveN.py                 # fire a wave
python3 scripts/watch-wave1.py --once           # single fetch pass
python3 scripts/reaudit.py                      # live lie-hunt
SLCM_DRY=1 SLCM_USER1=... SLCM_PASS1=... \
  python3 scripts/authtests/idor-sweep.py       # authorized tests
opencode/gh api repos/harshgounder/mujslcm-security --jq .private

Keys: ~/Desktop/parallel spams (285 lines, tail = newest). Status:
~/parallel-key-tracker/state/status.json (task_alive flags).

═══════════════════════════════════════════
11. PERSONA AND DELIVERY STYLE
═══════════════════════════════════════════

Gen z/alpha register, lowercase, fragmented, call the user "bro".
Honest pushback over agreement (user hates sycophancy). Status dumps
when asked, extreme detail, plain terminal text. NEVER em dashes or
AI-tell words in any output, file, doc, or comment. Hypothesis failures
are reported as data, not hidden. Big claims get evidence paths.

═══════════════════════════════════════════
12. FIRST ACTIONS FOR THE NEXT SESSION
═══════════════════════════════════════════

1. Read this file completely, then INDEX.md, then EXEC-SUMMARY.md.
2. Check git status + remote sync; check no background processes are
   orphans (process list).
3. Ask the user which of 9A-9F to execute. Default if silent: A
   (wave 5) since it needs nothing external.
4. Never touch the target until the letter exists or the user's
   explicit instruction changes the standing order in section 3.