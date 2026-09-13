#!/usr/bin/env python3
"""Launch MUJ SLCM wave 5: the gap register turned into runs.

Briefs come from scripts/gen-wave5-briefs.py (source: the byok gap register). Tiers: ultra8x for
the high-value technique universes (injection, auth, authz, logic, cloud, identity, tooling,
attribution), ultra for the rest. Rotates across task-alive keys on 402, writes ledger/ and
wave5-runs.json.
"""
import json, os, sys, time, urllib.request, urllib.error

BASE = "https://api.parallel.ai"
KEYS_FILE = "/home/liebert511/Desktop/parallel spams"
KEY_STATUS_FILE = "/home/liebert511/parallel-key-tracker/state/status.json"
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
BRIEFS_DIR = os.path.join(REPO, "briefs")
LEDGER_DIR = os.path.join(REPO, "ledger")
WAVE_INDEX = os.path.join(REPO, "wave5-runs.json")

OUTPUT_DESC = ("Comprehensive markdown report with inline [n] citations, exact URLs, data tables, "
               "chain-of-thought reasoning, VERDICT section with confidence, 3000+ words.")

ULTRA8X = ("xss", "sql", "auth-session", "authz", "business-logic", "azure", "control-plane",
           "identity", "m365", "tooling", "mcp", "api-modern", "ssrf", "http-layer", "dotnet",
           "detection", "legal", "data-protection")


def tier_for(name):
    return ("ultra8x", "ultra", "pro") if any(k in name for k in ULTRA8X) else ("ultra", "pro", "pro-fast")


def get_alive_keys():
    keys = [l.strip() for l in open(KEYS_FILE) if l.strip()]
    try:
        status = json.load(open(KEY_STATUS_FILE))
        alive = [k for i, k in enumerate(keys, 1)
                 if status.get(f"key#{i:02d}", {}).get("task_alive")]
        if alive:
            return alive
    except Exception as e:
        print(f"status.json read failed ({e}), using all keys", file=sys.stderr)
    return keys


def launch(prompt, processor, name, candidates):
    last_err = None
    for key in list(candidates):
        payload = {"input": prompt, "processor": processor,
                   "task_spec": {"output_schema": {"type": "text", "description": OUTPUT_DESC}}}
        req = urllib.request.Request(f"{BASE}/v1/tasks/runs", method="POST")
        req.add_header("x-api-key", key)
        req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, json.dumps(payload).encode(), timeout=60) as r:
                if r.status not in (200, 202):
                    last_err = f"HTTP {r.status}"
                    continue
                body = json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code}: {e.read().decode()[:120]}"
            if e.code == 402:
                candidates.remove(key)
                continue
            print(f"  key ...{key[-6:]} rejected ({last_err[:80]})", file=sys.stderr)
            continue
        run_id = body.get("run_id")
        if not run_id:
            print(f"LAUNCH FAILED no run_id: {body}", file=sys.stderr)
            continue
        os.makedirs(LEDGER_DIR, exist_ok=True)
        with open(os.path.join(LEDGER_DIR, f"{name}.json"), "w") as f:
            json.dump({"name": name, "run_id": run_id, "processor": processor,
                       "key_tail": key[-6:], "launched": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                       "done": False, "type": "task"}, f, indent=2)
        print(f"LAUNCHED {name}: run_id={run_id} processor={processor} key=...{key[-6:]}")
        return run_id
    print(f"ALL POOL REJECTED for {name}: {last_err}", file=sys.stderr)
    return None


if __name__ == "__main__":
    briefs = sorted(f for f in os.listdir(BRIEFS_DIR) if f.startswith("w5-") and f.endswith(".txt"))
    if not briefs:
        print("no w5 briefs found", file=sys.stderr)
        sys.exit(1)
    pool = get_alive_keys()
    print(f"pool: {len(pool)} task-alive keys | briefs: {len(briefs)}")
    runs = []
    for i, b in enumerate(briefs, 1):
        name = b.replace(".txt", "")
        prompt = open(os.path.join(BRIEFS_DIR, b)).read()
        tiers = tier_for(name)
        print(f"\n[{i}/{len(briefs)}] {name} (tier {tiers[0]})")
        for tier in tiers:
            run_id = launch(prompt, tier, name, pool)
            if run_id:
                runs.append({"name": name, "run_id": run_id, "brief": b, "processor": tier})
                break
            print(f"  {tier} failed, next tier")
        time.sleep(1)
    json.dump(runs, open(WAVE_INDEX, "w"), indent=1)
    print(f"\nWAVE INDEX: {WAVE_INDEX}\nlaunched {len(runs)}/{len(briefs)} runs")
