# mujslcm-security: offensive-security research on the MUJ SLCM portal

Private repo, github.com/harshgounder/mujslcm-security. Local clone `~/mujslcm-recon`, branch `main`.
Owner: the user. Built for the MUJ CyberSpace club.

Target: **https://mujslcm.jaipur.manipal.edu** (MUJ Student Life Cycle Management portal).
One target only. Nothing state-changing has ever been sent to it or to any sibling host.

## What is in here

A complete, evidence-backed research package on one application, in three layers:

1. **The campaign (2026-08-25).** 110 launches, 109 reports, 109 digests, 3 domain syntheses,
   10 verified hands-on findings, one documented error found by a reaudit, a target test plan,
   an aggressive-phase playbook, and a disclosure letter template.
2. **The live layer map (2026-09-13).** 46 targeted requests plus the current toolchain, producing
   the full stack from DNS to legal, with two hosted test instances and an identity-provider host
   discovered in the estate. Every row cites its raw capture.
3. **The gap register (2026-09-13).** The campaign graded against an external field universe, then
   25 gap-derived briefs fired to close the gaps. 25 reports, 1,186,037 chars, digested to
   472 tool rows, 84 no-tool gap rows and 47 build candidates.

## Numbers, measured from disk

| item | count |
|---|---|
| files tracked | 662 (13.3 MB) |
| launches in this repo | 135 (w1 10, w2 84, w3 15, w4 1, w5 25) |
| briefs | 134, self-contained, one per run |
| ledger files | 134, key tails only, never full keys |
| research reports and syntheses | 140 files, 5,585,870 chars |
| per-run digests | 109 |
| recon captures | 90 files, 61 of them the round 1 to 3 layer evidence |
| findings and playbooks | 8 documents plus the LAYER-MAP |
| pipeline scripts | 26 python files, including the gated auth-phase suite |

The companion catalogue repo, `byok-cyber-arsenal`, holds the external universe this work was graded
against (catalog/58), the gap register (catalog/59, 450 tool rows) and the raw deep-run outputs.

## Read order

1. `EXEC-SUMMARY.md`: the pitch, updated for the whole body of work
2. `findings/LAYER-MAP.md`: every layer that makes up the portal, L0 to L13, with corrections
3. `findings/FINDINGS-W0.md` and `findings/FINDINGS-DEEPROBE.md`: findings F1 to F10, raw evidence
4. `findings/REAUDIT-2026-08-25.md`: the second-pass lie-hunt, 20 of 20 rechecks, error E1
5. `findings/ATTACK-SURFACE-MAP.md`: the terrain, corrected
6. `findings/TEST-PLAN.md` and `findings/AGGRESSIVE-PLAYBOOK.md`: what to test, in what order
7. `research/VULN-CLASS-SYNTHESIS.md`, `SURFACE-SYNTHESIS.md`, `CONTEXT-SYNTHESIS.md`: the corpus distilled
8. `research/DIGEST-W5.md`: the gap register turned into 25 reports, deterministic parse
9. `scripts/authtests/README.md`: the suite that runs only under the letter
10. `disclosures/DISCLOSURE-LETTER.md`: the template that unlocks it

## Verified findings, at a glance

F1 verbose YSOD, four triggers, customErrors off. F2 trace.axd 403 with ELMAH 404. F3 version banners.
F4 jQuery 1.10.2. F5 credential design (M365 password, public username format). F6 password echo with a
size oracle. F7 request validation to YSOD class. F8 machineKey-protected `enc` parameter. F9 antiforgery
cookie without Secure. F10 edge posture clean at the time. E1 a route-oracle error the reaudit caught.

The 2026-09-13 layer pass added live measurements on top: the `enc` parameter resolved into a
three-stage oracle with two exception classes and two body sizes, the TLS picture corrected (TLS 1.3 is
offered; 3DES and CBC remain, no HSTS, no downgrade protection), the wafw00f WAF verdict explained as a
false positive from request validation, host-header and trust-bypass probes closed clean, and the estate
mapped to three hosting planes with `idp`, `pms`, `testerp` and `testmycampus` resolving. Corrections
E2 to E5 are recorded in the layer map.

The gap register names what the campaign never covered: XSS, SQLi, CORS, XXE, SSTI, request smuggling,
cache poisoning, race conditions, the Azure and Entra control planes, detection engineering, DPDP Act
2023, supply chain, mobile static analysis, social engineering, and the retest loop. Post-auth work is
still entirely unwritten.

## Standing orders (binding)

- Non-destructive until a signed scope letter exists. Single low-rate requests, synthetic data, no
  scanners, no auth attempts, no sibling hosts, no port sweeps beyond the two ports already published.
- With the letter: no credential stuffing, no exfiltration, no DoS, no live payment tampering, no
  persistence. IDOR sweeps stop at the first proof.
- Repo hygiene: never commit raw key material (ledgers hold tails only), no em dashes anywhere, no
  AI-tell words, the repo stays private.
- Every finding needs raw evidence on disk, and every claim is re-probed before it is restated.

## Gates and open decisions

- The authorized phase needs the signed registrar letter plus two test accounts.
- PR on the companion catalogue repo (web field universe and gap register) is open and waiting on a
  merge decision.
- One build candidate is queued for implementation, `enc_blob_classifier.py`, and needs a go order
  before any code is written. Six more sit behind it.

## Reusing the pipeline

1. `briefs/` holds every prompt. Regenerate with `python3 scripts/gen-briefs.py` (campaign) or
   `python3 scripts/gen-wave5-briefs.py` (from the gap register).
2. Launch: `python3 scripts/launch-wave5.py` style scripts read the briefs, round-robin the task-alive
   keys from `~/parallel-key-tracker/state/status.json`, and write `ledger/` plus a wave index.
3. Watch: `python3 scripts/watch-wave5.py` fetches status and result with the launching key, saves
   each report verbatim under `research/`, and never overwrites a landed file.
4. Digest: `python3 scripts/digest-w5.py` parses the reports into `research/DIGEST-W5.md` and a machine
   copy. Deterministic, no model calls.
5. Index: `python3 scripts/make-index.py` regenerates `INDEX.md` from the tracked tree. Do not hand-edit it.
6. Verify: `python3 scripts/reaudit.py` re-probes every claim it can reach.

## Status

Campaign complete, layer map complete, gap register complete, wave 5 landed and digested, all pushed.
No processes running. Waiting on the user for the PR decision and the build go order, and on the
university for the letter and the test accounts.
