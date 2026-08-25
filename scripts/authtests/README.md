# AUTHTESTS — authorized testing suite (turnkey)

Run ONLY with a signed scope letter from the university (hosts, dates,
test accounts, contact) on hand. See disclosures/DISCLOSURE-LETTER.md
for the template. Everything here is safe-by-default: rate-limited,
single-threaded, evidence JSONL, benign payloads only.

## Setup

    export SLCM_USER1=your.name.2506040062   # test account 1 (student)
    export SLCM_PASS1=...
    export SLCM_USER2=...   SLCM_PASS2=...   # account 2, for IDOR diffs
    export SLCM_DRY=1                        # first run: print, send nothing

## Run order

1. python3 scripts/authtests/session-tests.py   (foundation: do cookies
   work as expected? fixation? logout?)
2. python3 scripts/authtests/role-confusion.py  (EmailFor/LoginFor
   tampering vs server authz)
3. python3 scripts/authtests/idor-sweep.py      (the big one: BOLA on
   13 routes from third-party client code; stops at first cross-user hit)
4. python3 scripts/authtests/csrf-tests.py      (token lifetime/reuse)
5. python3 scripts/authtests/upload-tests.py    (document upload surface:
   only benign files, no scripts, no executables)

## Rules baked in

- NO payloads containing scripts, SQL, or code. Benign probes only.
- NO credential stuffing, no bulk enumeration, no DoS, no data copies.
- IDOR sweep: TWO accounts only, stop on first proof, record evidence,
  do not continue deeper.
- Session fixation: your own pre-set cookie only, never steal others.
- Every request logged to recon/authtests/<label>.jsonl with timestamps.
- If anything looks live-exploitable: STOP, write the evidence, notify
  the club SPOC and the registrar contact. Do not chain exploits.

## Evidence

Each test appends JSONL lines:
{"t":..., "session":..., "test":..., "ok":..., "st":..., ...}
Bodies of interesting responses are saved next to it when a test says so.

## Out of scope even with the letter

- Other students' real accounts (only the 2 test accounts),
- payments with real money, marking/grade changes in production,
- persistence or exfiltration,
- public disclosure before the university responds.