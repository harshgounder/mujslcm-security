#!/usr/bin/env python3
"""Targeted layer battery: methods, cookies, well-known files, error behaviour, F8 recheck.

Single requests, >=1.5 s apart, no brute force (a fixed short list of well-known ASP.NET
paths only), no authentication attempts, no state changes.
"""
import json, os, re, subprocess, time, datetime

T = "mujslcm.jaipur.manipal.edu"
BASE = f"https://{T}"
OUT = os.path.expanduser("~/mujslcm-recon/recon/layers-2026-09-13")
os.makedirs(OUT, exist_ok=True)
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
rows = []


def req(path, method="GET", extra="", label=None, save_body=False):
    url = path if path.startswith("http") else BASE + path
    cmd = f'curl -sS -k -m 25 -A "{UA}" -X {method} {extra} -D - -o /tmp/_b "{url}"'
    r = subprocess.run(cmd, shell=True, capture_output=True)
    head = r.stdout.decode(errors="replace")
    try:
        body = open("/tmp/_b", encoding="utf-8", errors="replace").read()
    except Exception:
        body = ""
    st = (re.search(r"HTTP/\S+ (\d+)", head) or [None, "000"])[1]
    sc = re.findall(r"(?im)^set-cookie:\s*(.+)$", head)
    allow = re.findall(r"(?im)^allow:\s*(.+)$", head)
    hdr = {k.lower(): v.strip() for k, v in re.findall(r"(?im)^([a-z0-9\-]+):\s*(.+)$", head)}
    rows.append({"label": label or f"{method} {path}", "status": st, "len": len(body),
                 "set_cookie": sc, "allow": allow, "server": hdr.get("server"),
                 "x_powered_by": hdr.get("x-powered-by"), "x_aspnetmvc": hdr.get("x-aspnetmvc-version"),
                 "all_headers": sorted(hdr.keys())})
    if save_body and body:
        with open(os.path.join(OUT, re.sub(r"\W+", "_", label or path) + ".body"), "w") as f:
            f.write(body[:200000])
    print(f"  {rows[-1]['label'][:52]:<54} {st}  {len(body):>7}b  cookie={len(sc)} allow={allow}")
    time.sleep(1.6)
    return body, head


print("== HTTP method matrix ==")
for m in ("GET", "HEAD", "POST", "OPTIONS", "TRACE", "PUT", "DELETE", "PATCH", "PROPFIND", "SEARCH"):
    req("/", m, label=f"method-{m}")

print("\n== well-known and framework paths (fixed short list) ==")
for p in ("/web.config", "/app_offline.htm", "/Global.asax", "/packages.config", "/bin/", "/App_Data/",
          "/Views/", "/Scripts/", "/Home/Error", "/Account/Login", "/.git/config", "/favicon.ico"):
    req(p, label=f"path-{p.strip('/').replace('/','_') or 'root'}")

print("\n== F1 and F8 recheck ==")
req("/Home/Index?enc=zz", label="F1-invalid-base64", save_body=True)
req("/Home/Index?enc=" + "A" * 24 + "==", label="F8-valid-base64-garbage", save_body=True)

print("\n== login POST behaviour (no credentials, synthetic only) ==")
# no token, empty fields: this is the same harmless probe the campaign used (server errors, no state change)
req("/", "POST", "-H 'Content-Type: application/x-www-form-urlencoded' --data 'UserName=&Password=&LoginFor=student&EmailFor=x%40muj.manipal.edu'",
    label="POST-empty-no-token", save_body=True)

json.dump({"target": T, "when": datetime.datetime.now().isoformat(), "rows": rows,
           "note": "single requests 1.6s apart; fixed lists; no auth; no exploitation; no state change"},
          open(os.path.join(OUT, "BATTERY-SUMMARY.json"), "w"), indent=1)
print(f"\n{len(rows)} probe rows -> {OUT}/BATTERY-SUMMARY.json")
