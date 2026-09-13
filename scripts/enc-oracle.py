#!/usr/bin/env python3
"""enc-parameter oracle characterisation + corrected method check.

Purpose: the campaign recorded F8 as "valid base64 enc -> CryptographicException, proving a
machineKey-protected blob". A live recheck today returned FormatException for a padded payload,
so the oracle is re-characterised from scratch. Every row is a single GET, 1.6 s apart.
"""
import json, os, re, subprocess, time, datetime

T = "mujslcm.jaipur.manipal.edu"
OUT = os.path.expanduser("~/mujslcm-recon/recon/layers-2026-09-13")
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
rows = []


def get(path, label, method="GET", data=None, save=True):
    open("/tmp/_b", "w").close()  # truncate so an empty body cannot inherit the previous one
    cmd = f'curl -sS -k -m 25 -A "{UA}" -X {method}'
    if data:
        cmd += f" -H 'Content-Type: application/x-www-form-urlencoded' --data '{data}'"
    cmd += f' -D /tmp/_h -o /tmp/_b "{path if path.startswith("http") else "https://" + T + path}"'
    r = subprocess.run(cmd, shell=True, capture_output=True)
    head = open("/tmp/_h", encoding="utf-8", errors="replace").read() if os.path.exists("/tmp/_h") else ""
    body = open("/tmp/_b", encoding="utf-8", errors="replace").read()
    st = (re.search(r"HTTP/\S+ (\d+)", head) or [None, "000"])[1]
    exc = sorted(set(re.findall(r"System\.[A-Za-z\.]+Exception", body)))[:3]
    exc = [e.replace("System.", "") for e in exc]
    hint = ""
    m = re.search(r"(Error|Exception|Description)[^<]{0,140}", body)
    if m:
        hint = re.sub(r"\s+", " ", m.group(0))[:110]
    rows.append({"label": label, "status": st, "bytes": len(body), "exceptions": exc, "hint": hint})
    if save and body:
        with open(os.path.join(OUT, "enc-" + re.sub(r"\W+", "_", label)[:40] + ".body"), "w") as f:
            f.write(body[:120000])
    print(f"  {label:<34} {st}  {len(body):>6}b  exc={','.join(exc) or '-'}  {hint[:60]}")
    time.sleep(1.6)
    return body, head


print("== enc oracle ladder ==")
get("/Home/Index", "no enc param")
get("/Home/Index?enc=", "enc empty")
get("/Home/Index?enc=z", "enc 1 char")
get("/Home/Index?enc=zz", "enc 2 chars")
get("/Home/Index?enc=AAA", "enc 3 chars (bad pad)")
get("/Home/Index?enc=AAA=", "enc valid 1 group")
get("/Home/Index?enc=AAAA", "enc valid 2 groups")
get("/Home/Index?enc=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", "enc 32 chars no pad")
get("/Home/Index?enc=" + "A" * 24 + "==", "enc 24 chars padded")
get("/Home/Index?enc=" + "A" * 21 + "==", "enc non-multiple-of-4")
get("/Home/Index?enc=AAAA-_AA", "enc url-safe chars")
get("/Home/Index?enc=%20%20%20%20", "enc whitespace")

print("\n== corrected method check (body truncated between requests) ==")
get("/", "GET /", method="GET")
get("/", "HEAD /", method="HEAD")
get("/", "OPTIONS *", method="OPTIONS")

json.dump({"target": T, "when": datetime.datetime.now().isoformat(), "rows": rows,
           "note": "enc oracle re-characterised live; single requests 1.6s apart; no credentials, "
                   "no state change, no exploitation"},
          open(os.path.join(OUT, "ENC-ORACLE.json"), "w"), indent=1)
print(f"\n-> {OUT}/ENC-ORACLE.json")
