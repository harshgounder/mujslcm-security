#!/usr/bin/env python3
"""Shared core for auth-phase tests (authorized testing only).

Env contract:
  SLCM_USER1 / SLCM_PASS1 : test account 1 (student)
  SLCM_USER2 / SLCM_PASS2 : test account 2 (student, for IDOR two-account)
  SLCM_DRY=1              : print planned requests, send nothing
  SLCM_RATE               : min seconds between requests (default 1.2)
  SLCM_TARGET             : overrides the target (default mujslcm)

Safety defaults: single-threaded, rate-limited, evidence JSONL per test,
stop-on-first-cross-tenant in IDOR sweeps. Never sends payloads with
scripts; benign content only."""
import json, os, re, socket, time, http.client, urllib.request, urllib.error

TARGET = os.environ.get("SLCM_TARGET", "https://mujslcm.jaipur.manipal.edu")
IP = os.environ.get("SLCM_IP", "98.70.14.50")
RATE = float(os.environ.get("SLCM_RATE", "1.2"))
DRY = os.environ.get("SLCM_DRY", "0") == "1"
USER1 = os.environ.get("SLCM_USER1", "")
PASS1 = os.environ.get("SLCM_PASS1", "")
USER2 = os.environ.get("SLCM_USER2", "")
PASS2 = os.environ.get("SLCM_PASS2", "")
EVID = os.environ.get("SLCM_EVID", os.path.expanduser("~/mujslcm-recon/recon/authtests"))
os.makedirs(EVID, exist_ok=True)


class PinnedHTTPSConnection(http.client.HTTPSConnection):
    def connect(self):
        self.sock = socket.create_connection((IP, self.port), self.timeout)
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
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 authtest"


class Session:
    """Authenticated session with evidence logging."""

    def __init__(self, user, pw, label):
        self.user, self.pw, self.label = user, pw, label
        self.cookies = {}
        self.log = open(os.path.join(EVID, f"{label}.jsonl"), "a")
        self.authenticated = self._login() if user and pw else False

    def _req(self, method, path, data=None, extra=None):
        time.sleep(RATE if not DRY else 0.1)
        hdrs = {"User-Agent": UA}
        if self.cookies:
            hdrs["Cookie"] = "; ".join(f"{k}={v}" for k, v in self.cookies.items())
        if data is not None:
            hdrs["Content-Type"] = "application/x-www-form-urlencoded"
        if DRY:
            print(f"[dry] {method} {path} data={str(data)[:80] if data else ''}")
            return 999, {}, b""
        req = urllib.request.Request(TARGET + path, method=method,
                                     data=data.encode() if data is not None else None, headers=hdrs)
        if extra:
            for k, v in extra.items():
                req.add_header(k, v)
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, dict(r.headers), r.read()
        except urllib.error.HTTPError as e:
            return e.code, dict(e.headers), (e.read() if e.fp else b"")
        except urllib.error.URLError as e:
            return 0, {}, str(e).encode()

    def raw_post(self, path, body, content_type):
        """Raw-body POST (multipart uploads)."""
        time.sleep(RATE if not DRY else 0.1)
        hdrs = {"User-Agent": UA, "Content-Type": content_type}
        if self.cookies:
            hdrs["Cookie"] = "; ".join(f"{k}={v}" for k, v in self.cookies.items())
        if DRY:
            print(f"[dry] POST {path} multipart {len(body)} bytes, ct={content_type[:40]}")
            return 999, {}, b""
        req = urllib.request.Request(TARGET + path, data=body, headers=hdrs)
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, dict(r.headers), r.read()
        except urllib.error.HTTPError as e:
            return e.code, dict(e.headers), (e.read() if e.fp else b"")
        except urllib.error.URLError as e:
            return 0, {}, str(e).encode()

    def ev(self, name, **fields):
        rec = {"t": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "session": self.label, "test": name}
        rec.update(fields)
        self.log.write(json.dumps(rec) + "\n")
        self.log.flush()

    def _login(self):
        if DRY:
            self.ev("login", ok=True, dry=True, user=self.user[:12])
            print(f"[dry] login {self.user} (no request sent)")
            return True
        st, h, b = self._req("GET", "/")
        tok = re.search(r'name="__RequestVerificationToken"[^>]*value="([^"]+)"', b.decode(errors="replace"))
        if not tok:
            self.ev("login", ok=False, why="no token on login page")
            return False
        sc = h.get("Set-Cookie", "")
        m = re.match(r"^([^=]+)=([^;]+)", sc)
        if m:
            self.cookies[m.group(1)] = m.group(2)
        data = (f"UserName={urllib.request.quote(self.user, safe='')}"
                f"&Password={urllib.request.quote(self.pw, safe='')}"
                f"&EmailFor=student&LoginFor=Student"
                f"&__RequestVerificationToken={tok.group(1)}")
        st, h, b = self._req("POST", "/", data)
        body = b.decode(errors="replace")
        sc = h.get("Set-Cookie") or ""
        if sc:
            for piece in sc.split(","):
                kv = piece.strip().split(";")[0]
                if "=" in kv:
                    kk, vv = kv.split("=", 1)
                    self.cookies[kk] = vv
        ok = st == 200 and "Invalid" not in body[:4000] and "__RequestVerificationToken" in body
        self.ev("login", ok=ok, st=st, size=len(b), cookies=list(self.cookies))
        return ok

    def get(self, path, **kw):
        return self._req("GET", path, **kw)

    def post(self, path, data, **kw):
        return self._req("POST", path, data=data, **kw)


def require_accounts():
    if not (USER1 and PASS1):
        print("FATAL: set SLCM_USER1/SLCM_PASS1 (and USER2/PASS2 for IDOR)")
        raise SystemExit(2)
    print(f"accounts: u1={USER1[:14]}... u2={'yes' if USER2 else 'no'} dry={DRY} rate={RATE}s")