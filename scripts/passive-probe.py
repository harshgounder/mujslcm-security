#!/usr/bin/env python3
"""Passive intel round: urlscan, NuGet, HSTS preload, Common Crawl.
All keyless public endpoints, read-only."""
import json, urllib.request, urllib.error

def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 recon"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode(errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, (e.read().decode(errors="replace")[:400] if e.fp else "")

# A: urlscan search (no key; expect 401 -> gap note)
for q in ["domain:mujslcm.jaipur.manipal.edu", "domain:jaipur.manipal.edu"]:
    st, b = fetch(f"https://urlscan.io/api/v1/search/?q={q}")
    print(f"urlscan [{q}]: {st} {b[:160] if st != 200 else 'OK'}")
    if st == 200:
        d = json.loads(b)
        print("  results:", len(d.get("results", [])))
        for r in d.get("results", [])[:5]:
            print("   ", r.get("page", {}).get("url"), "|", r.get("task", {}).get("time"))

# B: NuGet query for slcm / manipal
for q in ["slcm", "manipal"]:
    st, b = fetch(f"https://azuresearch-usnc.nuget.org/query?q={q}&take=10")
    if st == 200:
        d = json.loads(b)
        pkgs = [p["id"] for p in d.get("data", []) if "slcm" in p["id"].lower() or "manipal" in p["id"].lower()]
        print(f"nuget [{q}]: {len(d.get('data', []))} hits, relevant: {pkgs[:8]}")
    else:
        print(f"nuget [{q}]: HTTP {st} {b[:120]}")

# C: HSTS preload status
st, b = fetch("https://hstspreload.org/api/v2/status?domain=mujslcm.jaipur.manipal.edu")
print("hstspreload:", st, b.strip()[:200])
st, b = fetch("https://hstspreload.org/api/v2/status?domain=jaipur.manipal.edu")
print("hstspreload parent:", st, b.strip()[:200])

# D: Common Crawl availability + index hits
st, b = fetch("https://index.commoncrawl.org/collinfo.json")
if st == 200:
    colls = json.loads(b)
    latest = colls[0]["id"] if colls else None
    print("cc latest collection:", latest)
    if latest:
        st2, b2 = fetch(f"https://index.commoncrawl.org/{latest}-index?url=mujslcm.jaipur.manipal.edu%2F&output=json")
        hits = [ln for ln in b2.splitlines() if ln.strip()] if st2 == 200 else []
        print(f"  cc-index mujslcm: {st2} hits={len(hits)}")
        for h in hits[:5]:
            d = json.loads(h)
            print("   ", d.get("timestamp"), d.get("status"), d.get("url"))
else:
    print("cc collinfo:", st, b[:120])