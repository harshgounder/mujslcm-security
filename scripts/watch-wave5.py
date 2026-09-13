#!/usr/bin/env python3
"""Watch the wave-5 fleet: fetch status/result per run with ITS launching key.

Same contract as scripts/watch-wave1.py: status and result endpoints are launch-key-scoped, results
are saved verbatim under research/, and a run that returns NOT_FOUND is retried on the next pass.
"""
import json, os, sys, time, urllib.request, urllib.error

BASEURL = "https://api.parallel.ai"
KEYS_FILE = "/home/liebert511/Desktop/parallel spams"
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
LEDGER = os.path.join(BASE, "ledger")
RESEARCH = os.path.join(BASE, "research")
os.makedirs(RESEARCH, exist_ok=True)


def keys_by_tail():
    keys = [l.strip() for l in open(KEYS_FILE) if l.strip()]
    return {k[-6:]: k for k in keys}


def api(path, key, method="GET"):
    req = urllib.request.Request(f"{BASEURL}{path}", method=method)
    req.add_header("x-api-key", key)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:200]
    except Exception as e:
        return 0, str(e)[:200]


def main():
    once = "--once" in sys.argv
    tails = keys_by_tail()
    while True:
        pending = 0
        for f in sorted(os.listdir(LEDGER)):
            if not f.startswith("w5-") or not f.endswith(".json"):
                continue
            p = os.path.join(LEDGER, f)
            led = json.load(open(p))
            if led.get("done"):
                continue
            key = tails.get(led.get("key_tail", ""))
            if not key:
                print(f"  {led['name']:<48} NO KEY for tail {led.get('key_tail')}")
                pending += 1
                continue
            st, body = api(f"/v1/tasks/runs/{led['run_id']}", key)
            state = body.get("status") if isinstance(body, dict) else str(body)[:40]
            if state in ("completed", "failed", "cancelled", "expired"):
                path = f"/v1/tasks/runs/{led['run_id']}/result"
                rs, res = api(path, key)
                if rs == 200 and isinstance(res, dict):
                    out = res.get("output", {})
                    if isinstance(out, dict):
                        out = out.get("content") or json.dumps(out)
                    text = out if isinstance(out, str) else json.dumps(out)
                    if text.strip():
                        dest = os.path.join(RESEARCH, led["name"] + ".md")
                        open(dest, "w").write(text)
                        led["done"] = True
                        led["state"] = state
                        led["chars"] = len(text)
                        json.dump(led, open(p, "w"), indent=2)
                        print(f"  SAVED {led['name']:<44} {len(text)} chars ({state})")
                        continue
                print(f"  {led['name']:<48} {state} but result fetch {rs}")
                pending += 1
            else:
                print(f"  {led['name']:<48} {state}")
                pending += 1
        print("watch pass complete")
        if once or pending == 0:
            break
        time.sleep(60)


if __name__ == "__main__":
    main()
