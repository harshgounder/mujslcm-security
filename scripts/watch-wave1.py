#!/usr/bin/env python3
"""Watch MUJ SLCM wave 1 runs.

Rules from proven parallel-api-refs:
- runs are KEY-SCOPED: status/result must use the key that LAUNCHED the run
  (other keys -> HTTP 404). Ledger stores key_tail per run.
- status live at data.run.status OR data.status OR data.state (robust chain)
- /result returns output.content, which may be a STRING or a DICT
  (structured sectioned report). Dicts are saved as JSON + flattened md.

Usage: python3 scripts/watch-wave1.py [--once]
"""
import json, os, sys, time, urllib.request

BASE = "https://api.parallel.ai"
KEYS_FILE = "/home/liebert511/Desktop/parallel spams"
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
LEDGER_DIR = os.path.join(REPO, "ledger")
RESULTS_DIR = os.path.join(REPO, "research")
WAVE_INDEXES = [os.path.join(REPO, f) for f in os.listdir(REPO)
                if f.startswith("wave") and f.endswith("-runs.json")]

ONCE = "--once" in sys.argv

_pool = [l.strip() for l in open(KEYS_FILE) if l.strip()]


def key_for_tail(tail):
    for k in _pool:
        if k.endswith(tail):
            return k
    return None


def lead_key():
    try:
        status = json.load(open("/home/liebert511/parallel-key-tracker/state/status.json"))
        for i, k in enumerate(_pool, 1):
            if status.get(f"key#{i:02d}", {}).get("task_alive"):
                return k
    except Exception:
        pass
    return _pool[0]


def get_status(run_id, key):
    req = urllib.request.Request(f"{BASE}/v1/tasks/runs/{run_id}",
                                 headers={"x-api-key": key})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read().decode())
    st = (((data.get("run") or {}).get("status") or data.get("status"))
          or data.get("state") or "")
    return str(st).lower()


def fetch_result(run_id, key):
    req = urllib.request.Request(f"{BASE}/v1/tasks/runs/{run_id}/result",
                                 headers={"x-api-key": key})
    with urllib.request.urlopen(req, timeout=600) as r:
        data = json.loads(r.read().decode())
    out = data.get("output") or {}
    return out.get("content"), out.get("basis")


def save_content(name, content):
    if isinstance(content, str):
        path = os.path.join(RESULTS_DIR, name + ".md")
        with open(path, "w") as f:
            f.write(content)
        return path, len(content)
    # dict: structured sectioned report; save raw json + flattened md
    raw = os.path.join(RESULTS_DIR, name + ".json")
    with open(raw, "w") as f:
        json.dump(content, f, indent=2)
    md = os.path.join(RESULTS_DIR, name + ".md")
    with open(md, "w") as f:
        for k, v in content.items():
            f.write(f"## {k}\n\n")
            if isinstance(v, str):
                f.write(v + "\n\n")
            else:
                f.write(json.dumps(v, indent=2) + "\n\n")
    return md, os.path.getsize(raw) + os.path.getsize(md)


def main():
    runs = []
    for idx in WAVE_INDEXES:
        try:
            runs.extend(json.load(open(idx)))
        except Exception as e:
            print(f"skip index {idx}: {e}", flush=True)
    runs = [r for r in runs if r.get("run_id")]
    os.makedirs(RESULTS_DIR, exist_ok=True)
    done = {n["name"]: True for n in runs
            if os.path.exists(os.path.join(RESULTS_DIR, n["name"] + ".md"))}
    print(f"wave has {len(runs)} runs; already saved: {len(done)}", flush=True)
    while len(done) < len(runs):
        for r in runs:
            name = r["name"]
            if name in done:
                continue
            lf = os.path.join(LEDGER_DIR, f"{name}.json")
            ld = {}
            if os.path.exists(lf):
                ld = json.load(open(lf))
            tail = ld.get("key_tail") or r.get("key_tail")
            key = key_for_tail(tail) if isinstance(tail, str) else None
            if not key:
                key = lead_key()
            try:
                st = get_status(r["run_id"], key)
            except Exception as e:
                print(f"  status error {name}: {e}", flush=True)
                continue
            print(f"  {name}: {st}", flush=True)
            if st == "completed":
                try:
                    content, _basis = fetch_result(r["run_id"], key)
                except Exception as e:
                    print(f"  FETCH FAILED {name}: {e}", flush=True)
                    continue
                if not content:
                    print(f"  empty content {name}, skipping", flush=True)
                    continue
                mp, size = save_content(name, content)
                done[name] = True
                print(f"SAVED {name}: {size} chars -> {mp}", flush=True)
                ld["done"] = True
                ld["key_tail"] = ld.get("key_tail") or r.get("key_tail") or tail or ""
                ld["completed"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")
                ld["out_chars"] = size
                json.dump(ld, open(lf, "w"), indent=2)
            elif st in ("failed", "error", "cancelled"):
                print(f"RUN FAILED {name}: {st}", flush=True)
                done[name] = True
        if ONCE:
            break
        time.sleep(60)
    print("ALL WAVE RUNS RESOLVED")


if __name__ == "__main__":
    main()