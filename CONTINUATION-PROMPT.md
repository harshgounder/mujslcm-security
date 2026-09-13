# CONTINUATION-PROMPT: read this first in a new window

Last updated 2026-09-13, after the layer pass and wave 5. Repo HEAD pushed, tree clean.
Read `README.md` second and `findings/LAYER-MAP.md` third.

## 1. State in one paragraph

A complete research package on one university portal: the August campaign (110 launches, F1 to F10, a
test plan and a gated aggressive playbook), the September layer pass (the full stack L0 to L13 measured
live, with corrections), and wave 5 (25 reports answering the 25 gaps the campaign never covered).
135 launches total in this repo, 140 report files, 5,585,870 chars of research, 662 tracked files.
Nothing has ever been sent to the target beyond single low-rate requests. The authorized phase is
packaged and waits on a signed letter plus two test accounts.

## 2. Hard rules (do not relax without the user)

- Non-destructive until the letter exists. Single low-rate requests, synthetic data, no scanners, no
  fuzzers, no auth attempts, no sibling hosts, no port sweeps beyond 80, 443 and 8080.
- With the letter: no credential stuffing, no exfiltration, no DoS, no live payment tampering, no
  persistence. IDOR sweeps stop at the first proof.
- Every finding carries raw evidence on disk, and every claim is re-probed before it is restated.
- Repo hygiene: key tails only in ledgers, no em dashes, no AI-tell words, the repo stays private.
- The scanner class (nuclei, ffuf, sqlmap, nikto, httpx) runs against labs only, never the target.
  There is a working local-lab demonstration in `recon/layers-2026-09-13/nuclei-lab.txt`.

## 3. Tool routes and their quirks

- Deep research: `POST https://api.parallel.ai/v1/tasks/runs` with `x-api-key` and
  `{"input": ..., "processor": "ultra8x"|"ultra"|"pro"}`. 202 plus a run id means accepted and funded.
  Status and result are LAUNCH-KEY SCOPED: fetch them with the key that launched the run (the ledger
  holds its tail). Result retrieval and listing are separate entitlements.
- Keys: `~/Desktop/parallel spams`, one per line, newest at the bottom. Status of record:
  `~/parallel-key-tracker/state/status.json` (tier `TASK_ALIVE` is what launches). Probe with
  `python3 ~/parallel-key-tracker/probe.py`, pick with `pick.py task`.
- Search layer: `POST /v1/search` with `{"objective": ..., "search_queries": [...]}`. Extra fields are
  rejected. Free, link-level evidence.
- Fetch: rivalsearch MCP works. The Hermes nous web tools are not configured, and direct `curl` with a
  real user agent works for liveness and for raw GitHub content.
- Local tools installed this session with no system packages touched: `wafw00f` (uv), `testssl.sh`
  (`~/.local/opt/testssl.sh`), `nuclei-templates` (`~/.local/opt/nuclei-templates`), docker images
  `instrumentisto/nmap`, `projectdiscovery/nuclei`, `projectdiscovery/httpx`.
  Quirk: testssl.sh bundles OpenSSL 1.0.2, so it reports TLS 1.3 as not offered. Use system openssl to
  confirm 1.3.

## 4. Component map

| component | file | notes |
|---|---|---|
| the read-me-first pitch | `EXEC-SUMMARY.md` | findings, limits, assets |
| the layer stack | `findings/LAYER-MAP.md` | L0 to L13, evidence per row, corrections E2 to E5 |
| findings | `findings/FINDINGS-W0.md`, `FINDINGS-DEEPROBE.md` | F1 to F10 with raw captures |
| reaudit | `findings/REAUDIT-2026-08-25.md` | 20 of 20 rechecks, error E1 |
| terrain | `findings/ATTACK-SURFACE-MAP.md` | corrected route-oracle reading |
| test plan | `findings/TEST-PLAN.md` | pre-auth done, auth phase ordered |
| aggressive playbook | `findings/AGGRESSIVE-PLAYBOOK.md` | authorization-gated techniques |
| gap register (external) | `byok-cyber-arsenal` catalog/58 and catalog/59 | 25 gaps, 450 tool rows |
| wave 5 digest | `research/DIGEST-W5.md` | 472 tool rows, 84 no-tool gaps, 47 build candidates |
| pipeline | `scripts/` | gen, launch, watch, digest, index, reaudit, probes |
| auth suite | `scripts/authtests/` | dry-run only until the letter |

## 5. History, brief

2026-08-25: recon, waves 1 to 4, digests, deep probe, reaudit, auth suite, kit written.
2026-09-13: live layer pass (46 requests, 61 new evidence files, layer map, corrections), then wave 5
(25 gap-derived briefs, all landed, digest corrected after an over-count), then the kit rewrite and
INDEX regeneration.

## 6. Open decisions (user side)

1. Merge the companion PR (web field universe and gap register) or revert the direct commit on main.
2. Go order for `enc_blob_classifier.py` (spec, opencode, audit, gates, commit). Six more build
   candidates sit behind it: role_matrix.yaml, slcm_workflow_fsm.json, razor_form_diff.json,
   safe_desync_plan.yaml, student_data_taxonomy.yml, identity_coupling_evidence.json.
3. Whether wave 6 targets the two thin areas the wave-5 reports flagged themselves.

## 7. Verify, do not trust

Run these before restating any number:

    python3 scripts/make-index.py            # INDEX must match the tree
    ls research/*.md | wc -l                 # 140
    ls ledger/*.json | wc -l                 # 134
    python3 scripts/digest-w5.py             # regenerates the wave-5 counts: 472 / 84 / 47
    grep -c '^### ' findings/LAYER-MAP.md    # layer entries present
    git log --oneline -5                     # compare with origin/main

Then live-check the two cheapest claims: the `enc` ladder (invalid base64 gives 4,942 bytes and
FormatException; valid base64 gives 5,084 bytes and CryptographicException) and the port posture
(443 open, 80 and 8080 filtered). Both are single requests. If either has changed, the layer map needs
an amendment, not a quiet edit.
