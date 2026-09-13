#!/usr/bin/env python3
"""Layer probe round 2: DNS via DoH, TLS properly, and the client asset inventory."""
import json, os, re, subprocess, time

T = "mujslcm.jaipur.manipal.edu"
OUT = os.path.expanduser("~/mujslcm-recon/recon/layers-2026-09-13")
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"


def sh(cmd, timeout=60):
    r = subprocess.run(cmd, shell=True, capture_output=True, timeout=timeout)
    return r.stdout.decode(errors="replace") + r.stderr.decode(errors="replace")


def save(name, data):
    p = os.path.join(OUT, name)
    with open(p, "wb" if isinstance(data, bytes) else "w") as f:
        f.write(data)
    return os.path.getsize(p)


def doh(name, rtype):
    cmd = (f'curl -sS -m 20 -H "accept: application/dns-json" '
           f'"https://cloudflare-dns.com/dns-query?name={name}&type={rtype}"')
    out = sh(cmd)
    try:
        d = json.loads(out)
        ans = [a.get("data") for a in d.get("Answer", [])]
        return [str(a) for a in ans]
    except Exception:
        return [f"ERR {out[:80]}"]


print("== DNS via DoH (cloudflare) ==")
dns = {}
targets = [
    (T, "A"), (T, "AAAA"), (T, "CNAME"), (T, "NS"), (T, "SOA"), (T, "MX"), (T, "TXT"), (T, "CAA"),
    (T, "HTTPS"), ("_dmarc." + T, "TXT"), ("_mta-sts." + T, "TXT"), ("_smtp._tls." + T, "TXT"),
    ("autodiscover." + T, "CNAME"), ("enterpriseregistration." + T, "CNAME"),
    ("enterpriseenrollment." + T, "CNAME"), ("lyncdiscover." + T, "CNAME"),
    ("selector1._domainkey." + T, "CNAME"), ("selector2._domainkey." + T, "CNAME"),
    ("msoid." + T, "CNAME"), ("sip." + T, "CNAME"), ("www." + T, "CNAME"),
    ("mail." + T, "CNAME"), ("vpn." + T, "CNAME"), ("portal." + T, "CNAME"),
]
for n, rtype in targets:
    v = doh(n, rtype)
    dns[f"{n}|{rtype}"] = v
    print(f"  {n:<44} {rtype:<6} {('; '.join(v))[:110]}")
    time.sleep(0.6)
save("dns-doh.json", json.dumps(dns, indent=1))

print("\n== TLS, done properly ==")
res = {}
for label, args in [
    ("tls1.3", "-tls1_3"),
    ("tls1.2", "-tls1_2"),
    ("tls1.1_seclevel0", "-tls1_1 -cipher DEFAULT@SECLEVEL=0"),
    ("tls1.0_seclevel0", "-tls1 -cipher DEFAULT@SECLEVEL=0"),
]:
    out = sh(f'echo | timeout 20 openssl s_client {args} -connect {T}:443 -servername {T} 2>&1 | '
             f'grep -m2 -E "^ *Protocol|^ *Cipher|alert|no protocols"')
    res[label] = out.strip().replace("\n", " / ")[:180]
    print(f"  {label:<18} {res[label][:150]}")
    time.sleep(1)
out = sh(f'echo | timeout 20 openssl s_client -connect {T}:443 -servername {T} 2>&1 | '
         f'grep -m1 -A3 "ALPN"')
res["alpn"] = out.strip()[:200]
print("  ALPN:", res["alpn"][:160])
out = sh(f'echo | timeout 20 openssl s_client -tls1_2 -connect {T}:443 -servername {T} 2>&1 | '
         f'grep -m1 "Cipher is"')
# full cipher list offered
res["cipher_list"] = sh(f'nmap --version >/dev/null 2>&1 && echo nmap-present || echo nmap-absent')[:40]
save("tls-v2.txt", json.dumps(res, indent=1))
print("  note: openssl 3 refuses TLS1.0/1.1 unless SECLEVEL=0; both runs above used it")

print("\n== headers and body detail ==")
hdr = open(os.path.join(OUT, "home-headers.txt"), encoding="utf-8", errors="replace").read()
print("  --- response headers ---")
for line in hdr.split("\r\n" if "\r\n" in hdr else "\n"):
    if line.strip():
        print("   ", line[:150])
body = open(os.path.join(OUT, "home.html"), encoding="utf-8", errors="replace").read()
meta = re.findall(r'<meta[^>]+>', body)
print("  --- meta tags ---")
for m in meta[:12]:
    print("   ", m[:140])
print("  --- forms and fields ---")
print("   ", re.findall(r'<form[^>]*>', body)[:3])
print("   fields:", re.findall(r'name="([^"]+)"', body)[:14])
print("  --- script/style counts ---")
print("   scripts:", len(re.findall(r'<script', body)), "styles:", len(re.findall(r'rel="stylesheet"', body)))
fx = re.findall(r"(jquery[\w\.\-]*|bootstrap[\w\.\-]*|moment[\w\.\-]*|select2|datatables|blockui|sweetalert|toastr|axios|popper)", body, flags=re.I)
print("   libs in html:", sorted(set(x.lower() for x in fx)))
enc = open(os.path.join(OUT, "enc-trigger.txt"), encoding="utf-8", errors="replace").read()
print("  --- enc trigger (F1/F8 recheck) ---")
for pat in (r"ASP\.NET Version:[^;<]+", r"FormatException", r"CryptographicException", r"HttpAntiForgeryException", r"\.NET Framework Version:[^\s<]+", r"Microsoft-IIS"):
    m = re.search(pat, enc)
    print(f"   {pat[:28]:<30} {m.group(0)[:80] if m else 'not present'}")

print("\n== client bundles ==")
base = f"https://{T}"
for path, name in [("/keen/themes/keen/theme/demo1/dist/assets/plugins/global/plugins.bundle.js", "plugins.bundle.js"),
                   ("/Scripts/jquery.validate.min.js", "jquery.validate.min.js"),
                   ("/Scripts/jquery-1.10.2.min.js", "jquery-1.10.2.min.js")]:
    out = sh(f'curl -sS -k -m 40 -A "{UA}" "{base}{path}"')
    n = save(name, out)
    print(f"  {path.split('/')[-1]:<26} {n:>9} bytes")
    time.sleep(1.2)
pb = open(os.path.join(OUT, "plugins.bundle.js"), encoding="utf-8", errors="replace").read()
libs = re.findall(r"jQuery JavaScript Library v([\d\.]+)|/\*!\s*([A-Za-z0-9\.\- ]{3,40})\s*v?([\d]+\.[\d\.]+)", pb)
print("  jquery versions inside bundle:", sorted(set(re.findall(r"jQuery JavaScript Library v([\d\.]+)", pb))))
print("  versioned components in bundle (first 24):")
comp = sorted(set(f"{m[1].strip()} {m[2]}" for m in libs if m[1]))
for c in comp[:24]:
    print("    ", c)
save("bundle-components.txt", "\n".join(comp))
# source maps
maps = []
for u in ["/Scripts/jquery-1.10.2.min.js.map", "/keen/themes/keen/theme/demo1/dist/assets/plugins/global/plugins.bundle.js.map"]:
    out = sh(f'curl -sS -k -m 20 -o /dev/null -w "%{{http_code}}" -A "{UA}" "{base}{u}"')
    maps.append((u, out.strip()))
    print(f"  sourcemap {u.split('/')[-1]:<34} HTTP {out.strip()}")
    time.sleep(1)
save("sourcemaps.txt", json.dumps(maps, indent=1))

print("\n== certificate transparency (SANs that exist) ==")
ct = sh(f'curl -sS -m 40 "https://crt.sh/?q=%25.jaipur.manipal.edu&output=json"')
try:
    recs = json.loads(ct)
    names = sorted(set(n.strip() for r in recs for n in r.get("name_value", "").split("\n")))
    save("ct-names.txt", "\n".join(names))
    print(f"  CT names for *.jaipur.manipal.edu: {len(names)}")
    for n in names[:30]:
        print("   ", n)
except Exception as e:
    print("  crt.sh failed:", e, ct[:120])
