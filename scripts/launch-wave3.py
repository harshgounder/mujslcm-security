#!/usr/bin/env python3
"""Launch wave 3: 15 per-host OSINT runs. ultra8x for exposed hosts
exam/uat/api/sis, ultra for the rest."""
import json, os, sys, time, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
BRIEFS = os.path.join(REPO, "briefs")
KEYS_FILE = os.path.expanduser("~/Desktop/parallel spams")
STATUS = "/home/liebert511/parallel-key-tracker/state/status.json"
BASE = "https://api.parallel.ai/v1/tasks/runs"

U8X = {"w3-01-exam-jaipur", "w3-02-uat-manipal", "w3-03-api-manipal", "w3-04-sis-manipal-feekart"}
TIERS = ["ultra8x", "ultra", "pro"]

def load_keys():
    keys = [l.strip() for l in open(KEYS_FILE) if l.strip()]
    alive = set()
    try:
        st = json.load(open(STATUS))
        for k, v in st.items():
            if isinstance(v, dict) and (v.get("task") == "TASK_ALIVE" or v.get("tier") == "TASK_ALIVE"):
                alive.add(v.get("key_tail") or k)
    except Exception:
        pass
    # newest 2 keys may not be in status.json yet; append them as candidates
    order = keys + [k for k in keys[-2:]]
    seen = set(); out = []
    for k in order:
        if k in seen: continue
        seen.add(k); out.append(k)
    return out

def launch(prompt, processor, key):
    req = urllib.request.Request(BASE, data=json.dumps({
        "input": prompt, "processor": processor,
        "task_spec": {"output_schema": {"type": "text"}},
    }).encode(), headers={"x-api-key": key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())

SPECS_SRC = os.path.join(HERE, "brief-specs-w3.py")
ns = {}
exec(compile(open(SPECS_SRC).read(), SPECS_SRC, "exec"), ns)
SPECS = ns["SPECS"]

keys = load_keys()
ki = 0
runs = []
for n, (slug, focus) in enumerate(SPECS, 1):
    brief = os.path.join(BRIEFS, slug + ".txt")
    if not os.path.exists(brief):
        print(f"[{n}/{len(SPECS)}] {slug}: brief missing ({brief}), skip")
        continue
    prompt = open(brief).read()
    tier = "ultra8x" if slug in U8X else "ultra"
    proc = None
    for cand in TIERS[TIERS.index(tier):]:
        ok = False
        for _ in range(len(keys)):
            key = keys[ki % len(keys)]; ki += 1
            try:
                print(f"[{n}/{len(SPECS)}] {slug} (try {cand})...", flush=True)
                resp = launch(prompt, cand, key)
                runs.append({"name": slug, "run_id": resp["run_id"],
                             "interaction_id": resp.get("interaction_id", ""),
                             "processor": cand, "key_tail": key[-6:]})
                print(f"LAUNCHED {slug}: run_id={resp['run_id']} processor={cand}", flush=True)
                proc = cand; ok = True
                break
            except urllib.error.HTTPError as e:
                if e.code == 402:
                    continue
                print(f"  http {e.code}", flush=True); break
            except Exception as e:
                print(f"  err {e}", flush=True); break
        if ok: break
    if proc is None:
        print(f"FAIL {slug}: no key accepted", flush=True)
    time.sleep(0.5)

json.dump(runs, open(os.path.join(REPO, "wave3-runs.json"), "w"), indent=1)
print(f"WAVE INDEX: {os.path.join(REPO, 'wave3-runs.json')}")
print(f"launched {len(runs)}/{len(SPECS)} runs")