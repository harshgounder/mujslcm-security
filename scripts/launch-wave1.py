#!/usr/bin/env python3
"""Launch MUJ SLCM recon wave 1: 10 ultra8x deep-research runs.

Reads briefs from briefs/w1-*.txt, launches each on a task-alive key
(round-robin), writes per-run ledger JSONs to ledgers/ and a wave index
to wave1-runs.json. Fallback tiers: ultra8x -> ultra -> pro.
"""
import json, os, sys, time, urllib.request, urllib.error

BASE = "https://api.parallel.ai"
KEYS_FILE = "/home/liebert511/Desktop/parallel spams"
KEY_STATUS_FILE = "/home/liebert511/parallel-key-tracker/state/status.json"
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
BRIEFS_DIR = os.path.join(REPO, "briefs")
LEDGER_DIR = os.path.join(REPO, "ledger")
WAVE_INDEX = os.path.join(REPO, "wave1-runs.json")

OUTPUT_DESC = ("Comprehensive markdown report with inline [n] citations, exact URLs, "
               "data tables, chain-of-thought reasoning, VERDICT section with confidence, "
               "3000+ words.")


def get_alive_keys():
    keys = [l.strip() for l in open(KEYS_FILE) if l.strip()]
    try:
        status = json.load(open(KEY_STATUS_FILE))
        task_alive = [k for i, k in enumerate(keys, 1)
                      if status.get(f"key#{i:02d}", {}).get("task_alive")]
        search_alive = [k for i, k in enumerate(keys, 1)
                        if status.get(f"key#{i:02d}", {}).get("alive")]
        ordered = task_alive + [k for k in search_alive if k not in task_alive]
        if ordered:
            return ordered
    except Exception as e:
        print(f"status.json read failed ({e}), using all keys", file=sys.stderr)
    return keys


def launch(prompt, processor, name):
    candidates = get_alive_keys()
    last_err = None
    for key in candidates:
        payload = {
            "input": prompt,
            "processor": processor,
            "task_spec": {"output_schema": {"type": "text", "description": OUTPUT_DESC}},
        }
        req = urllib.request.Request(f"{BASE}/v1/tasks/runs", method="POST")
        req.add_header("x-api-key", key)
        req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, json.dumps(payload).encode(), timeout=60) as r:
                body = json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code}: {e.read().decode()[:120]}"
            if e.code == 402:
                continue
            print(f"  key ...{key[-6:]} rejected ({last_err[:80]})", file=sys.stderr)
            continue
        run_id = body.get("run_id")
        if not run_id:
            print(f"LAUNCH FAILED no run_id: {body}", file=sys.stderr)
            continue
        os.makedirs(LEDGER_DIR, exist_ok=True)
        ledger = {"name": name, "run_id": run_id, "processor": processor,
                  "key_tail": key[-6:],
                  "launched": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                  "done": False, "type": "task"}
        with open(os.path.join(LEDGER_DIR, f"{name}.json"), "w") as f:
            json.dump(ledger, f, indent=2)
        print(f"LAUNCHED {name}: run_id={run_id} processor={processor} key=...{key[-6:]}")
        return run_id
    print(f"ALL KEYS REJECTED for {name}: {last_err}", file=sys.stderr)
    return None


def launch_with_fallback(prompt, name, tiers=("ultra8x", "ultra", "pro")):
    for tier in tiers:
        print(f"\n  trying {tier} for {name}...")
        run_id = launch(prompt, tier, name)
        if run_id:
            return run_id
        print(f"  {tier} unavailable for {name}, falling back")
    print(f"  ALL TIERS FAILED for {name}")
    return None


if __name__ == "__main__":
    briefs = sorted(f for f in os.listdir(BRIEFS_DIR) if f.startswith("w1-") and f.endswith(".txt"))
    if not briefs:
        print("no briefs found", file=sys.stderr)
        sys.exit(1)
    runs = []
    for i, b in enumerate(briefs, 1):
        name = b.replace(".txt", "")
        prompt = open(os.path.join(BRIEFS_DIR, b)).read()
        print(f"\n[{i}/{len(briefs)}] {name}")
        run_id = launch_with_fallback(prompt, name)
        if run_id:
            runs.append({"name": name, "run_id": run_id, "brief": b})
        time.sleep(2)
    with open(WAVE_INDEX, "w") as f:
        json.dump(runs, f, indent=1)
    print(f"\nWAVE INDEX: {WAVE_INDEX}")
    print(f"launched {len(runs)}/{len(briefs)} runs")