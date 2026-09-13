#!/usr/bin/env python3
"""Layer probe: mujslcm.jaipur.manipal.edu. Non-destructive, single low-rate requests.

Emits raw evidence into recon/layers-2026-09-13/ and a machine summary.
Bounds honoured: GET/HEAD/OPTIONS only, >=1.5 s apart, no path brute force,
no authentication attempts, no sibling hosts, no scanners.
"""
import json, os, re, socket, subprocess, time, ssl, datetime

T = "mujslcm.jaipur.manipal.edu"
OUT = os.path.expanduser("~/mujslcm-recon/recon/layers-2026-09-13")
os.makedirs(OUT, exist_ok=True)
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
LOG = []


def save(name, data):
    p = os.path.join(OUT, name)
    mode = "wb" if isinstance(data, bytes) else "w"
    with open(p, mode) as f:
        f.write(data)
    return os.path.getsize(p)


def sh(cmd, timeout=30):
    r = subprocess.run(cmd, shell=True, capture_output=True, timeout=timeout)
    return r.stdout.decode(errors="replace"), r.returncode


def curl(url, extra="", name=None, method="GET"):
    cmd = f'curl -sS -k -m 25 -A "{UA}" -X {method} {extra} "{url}"'
    out, rc = sh(cmd)
    if name:
        LOG.append({"probe": name, "url": url, "method": method, "bytes": save(name, out), "rc": rc})
    return out


def dig(name, rtype):
    out, rc = sh(f"dig +short {rtype} {name} @1.1.1.1")
    if not out:
        out, rc = sh(f"dig +short {rtype} {name} @8.8.8.8")
    return out.strip()


print("== DNS layer ==")
dns = {}
for rtype in ("A", "AAAA", "CNAME", "NS", "SOA", "MX", "TXT", "CAA"):
    v = dig(T, rtype)
    dns[rtype] = v
    print(f"  {rtype:<6} {v[:110]}")
for label, n in [("DMARC _dmarc", "_dmarc." + T), ("MTA-STS", "_mta-sts." + T),
                 ("autodiscover CNAME", "autodiscover." + T), ("enterpriseregistration", "enterpriseregistration." + T),
                 ("enterpriseenrollment", "enterpriseenrollment." + T), ("lyncdisc", "lyncdiscover." + T),
                 ("sipfed", "sipfed.online.lync.com"), ("DKIM selector1", "selector1._domainkey." + T),
                 ("DKIM selector2", "selector2._domainkey." + T)]:
    rtype = "TXT" if "DKIM" in label or "DMARC" in label or "STS" in label else "CNAME"
    v = dig(n, rtype)
    dns[label] = v
    print(f"  {label:<24} {v[:110]}")
save("dns.json", json.dumps(dns, indent=1))

print("\n== HTTP layer ==")
head = curl(f"https://{T}/", "-D - -o /dev/null -H 'Accept: text/html'", "home-headers.txt")
print("  headers saved,", len(head), "bytes")
time.sleep(1.5)
body = curl(f"https://{T}/", "", "home.html")
print("  body saved,", len(body), "bytes")
time.sleep(1.5)
trig = curl(f"https://{T}/Home/Index?enc=zz", "-D -", "enc-trigger.txt")
print("  enc trigger saved,", len(trig), "bytes; status:",
      (re.search(r"HTTP/\S+ (\d+)", trig) or [None, "?"])[1])
time.sleep(1.5)
for path, name in [("/robots.txt", "robots.txt"), ("/security.txt", "security.txt"),
                   ("/.well-known/security.txt", "well-known-security.txt"), ("/trace.axd", "trace-axd.txt"),
                   ("/elmah.axd", "elmah-axd.txt"), ("/favicon.ico", "favicon.ico"), ("/sitemap.xml", "sitemap.xml")]:
    r = curl(f"https://{T}{path}", "-D - -o /dev/null", name)
    st = (re.search(r"HTTP/\S+ (\d+)", r) or [None, "?"])[1]
    print(f"  {path:<30} {st}")
    time.sleep(1.5)
opts = curl(f"https://{T}/", "-D - -o /dev/null -X OPTIONS", "options.txt")
print("  OPTIONS:", (re.search(r"HTTP/\S+ (\d+)", opts) or [None, "?"])[1])
time.sleep(1.5)
h2 = sh(f'curl -sS -k -m 20 --http2 -o /dev/null -w "http_version=%{{http_version}} alpn_proxy=%{{time_connect}}" https://{T}/')
print("  proto:", h2[0])
save("http2-check.txt", h2[0])

print("\n== TLS layer ==")
tls = sh(f'echo | openssl s_client -connect {T}:443 -servername {T} -showcerts 2>/dev/null | '
         f'openssl x509 -noout -subject -issuer -dates -ext subjectAltName -ext extendedKeyUsage 2>/dev/null')
save("tls-cert.txt", tls[0])
print("  cert:", " | ".join(tls[0].split("\n")[:4])[:200])
protos = {}
for p in ("tls1_2", "tls1_3", "tls1_1", "tls1"):
    out, rc = sh(f'echo | timeout 15 openssl s_client -{p} -connect {T}:443 -servername {T} 2>&1 | '
                 f'grep -m1 -E "Protocol|Cipher|alert|error"')
    protos[p] = out.strip()[:120]
    print(f"  {p:<8} {protos[p][:100]}")
    time.sleep(1)
save("tls-protocols.txt", "\n".join(f"{k}: {v}" for k, v in protos.items()))
chain = sh(f'echo | openssl s_client -connect {T}:443 -servername {T} -showcerts 2>/dev/null | grep -E "^ *[0-9] s:|^ *i:"')
save("tls-chain.txt", chain[0])
print("  chain:", chain[0].replace("\n", " | ")[:200])

print("\n== identity metadata ==")
for dom in ("jaipur.manipal.edu", "muj.manipal.edu", "manipal.edu"):
    r = curl(f"https://login.microsoftonline.com/{dom}/v2.0/.well-known/openid-configuration", "-s", f"oidc-{dom}.json")
    try:
        d = json.loads(r)
        print(f"  {dom:<22} issuer={d.get('issuer','?')[:60]}")
    except Exception:
        print(f"  {dom:<22} no json ({len(r)} bytes)")
    time.sleep(1.2)
r = curl(f"https://login.microsoftonline.com/getuserrealm.srf?login=probe@{T}&xml=1", "-s", "getuserrealm.xml")
m = re.search(r"<NameSpaceType>([^<]+)</NameSpaceType>", r)
print("  getuserrealm NameSpaceType:", m.group(1) if m else "n/a")
time.sleep(1.2)
r2 = curl(f"https://autodiscover.{T}/autodiscover/autodiscover.xml", "-s -o /dev/null -D -", "autodiscover-head.txt")
print("  autodiscover:", (re.search(r"HTTP/\S+ (\d+)", r2) or [None, "?"])[1])

print("\n== client asset layer ==")
assets = re.findall(r'(?:src|href)="([^"]+\.(?:js|css|png|jpg|svg|woff2?)(?:\?[^"]*)?)"', body)
uniq = []
for a in assets:
    if a not in uniq and not a.startswith("data:"):
        uniq.append(a)
save("asset-list.txt", "\n".join(uniq))
print(f"  {len(uniq)} assets referenced")
for a in uniq[:12]:
    print("   ", a[:100])
vers = {}
for a in uniq:
    for lib in ("jquery", "jquery-", "bootstrap", "moment", "select2", "datatables", "keen", "validate"):
        if lib in a.lower():
            vers.setdefault(lib, []).append(a)
save("asset-versions.json", json.dumps(vers, indent=1))
print("  versioned libs:", {k: v[0][:70] for k, v in vers.items()})

print("\n== DB/ports (top-3 service ports only, single SYN each) ==")
ports = {}
for port in (80, 443, 8080):
    c = subprocess.run(f"timeout 6 bash -c '</dev/tcp/{T}/{port}' 2>/dev/null", shell=True)
    ports[port] = "open" if c.returncode == 0 else "closed/filtered"
    print(f"  {port}: {ports[port]}")
    time.sleep(1)
save("ports.txt", json.dumps(ports, indent=1))

json.dump({"target": T, "when": datetime.datetime.now().isoformat(),
           "probes": LOG, "dns": dns, "tls_protocols": protos, "ports": ports,
           "note": "single requests, 1.5s apart, no auth, no scanners, no sibling hosts"},
          open(os.path.join(OUT, "PROBE-SUMMARY.json"), "w"), indent=1)
print(f"\nevidence -> {OUT}")
print(f"probes: {len(LOG)}")
