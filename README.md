# mujslcm-security : MUJ CyberSpace Club offensive-research project

Private repo, github.com/harshgounder/mujslcm-security (owner: user).
Local clone: ~/mujslcm-recon, branch main.

## What this is

A complete, evidence-backed security-research package on ONE target:
https://mujslcm.jaipur.manipal.edu (MUJ Student Life Cycle Management
portal). Built 2026-08-25 for the CyberSpace club. Everything is
recon-grade and non-destructive: no scanners, no auth attempts, no
other hosts touched. The aggressive phase is packaged and gated behind
a signed registrar letter + two test accounts.

## Read order

1. EXEC-SUMMARY.md        the pitch doc, start here
2. findings/REAUDIT-2026-08-25.md   what a second-pass lie-hunt found and fixed
3. findings/FINDINGS-W0.md + FINDINGS-DEEPROBE.md   verified findings F1-F10
4. findings/ATTACK-SURFACE-MAP.md  the terrain
5. findings/TEST-PLAN.md + AGGRESSIVE-PLAYBOOK.md  what to test, how, in what order
6. research/DIGEST-W1.md + DIGEST-W2.md + the 3 syntheses  the 4.3M-char corpus distilled
7. scripts/authtests/README.md  the authorized-phase suite
8. disclosures/DISCLOSURE-LETTER.md  the template that unlocks it

## Numbers

- 110 parallel.ai runs launched, 109 unique reports saved (~4.3M chars)
- 109 digests, every one read-to-EOF proven, style-gated, evidence-labelled
- 3 domain syntheses (VULN-CLASS, SURFACE, CONTEXT)
- 10 verified findings (F1-F10), 1 documented error caught by reaudit (E1)
- 20/20 live rechecks confirmed in the lie-hunt
- 529 tracked files, 110 replayable briefs, 8 tooling scripts, 6 auth-phase scripts

## Verified stack (short version)

IIS 10, ASP.NET MVC 5.3, .NET Framework 4.7.4136.0, Microsoft Azure
AS8075 (98.70.14.50, NOT Akamai), Entrust DV cert (single SAN),
Entra/M365 identity (3 tenants), DMARC p=none. Verbose YSODs everywhere
(customErrors off), password echo on failed login, machineKey-protected
ReturnUrl blob, anti-CSRF cookie without Secure flag.

## Standing orders (hard rules)

- NON-DESTRUCTIVE until a signed scope letter exists. Single low-rate
  GETs, synthetic data, no scanners, no auth attempts, no sibling hosts.
- Even with the letter: no credential stuffing, no exfiltration, no DoS,
  no live payment tampering, no persistence. IDOR sweeps stop at first proof.
- Repo hygiene: never commit raw key material (ledgers hold key tails
  only), no em dashes anywhere, no AI-tell words, private repo stays private.
- Git identity: liebert511 <liebert511@users.noreply.github.com>.

## Reusing the pipeline

1. briefs/ holds 110 self-contained prompts (regenerate: python3
   scripts/gen-briefs.py; family specs in scripts/brief-specs-*.py)
2. Launch: python3 scripts/launch-waveN.py (reads briefs, round-robins
   task-alive parallel.ai keys, writes ledgers + waveN-runs.json)
3. Watch: python3 scripts/watch-wave1.py [--once] (key-scoped status/
   result fetches, dict-or-str result handling, saves to research/)
4. Digest: dispatch subagents on research/*.md with the digest contract
   (see research/digests/ samples), then synthesize
5. Verify: scripts/reaudit.py (live re-probe of every claim)
6. Execute under auth: scripts/authtests/ (SLCM_USER1/2 env contract)

## Status

Campaign complete and pushed. No active processes. Waiting on decision:
wave-5 research now, or the signed letter first (see CONTINUATION-PROMPT.md
section 9 for the decision menu).