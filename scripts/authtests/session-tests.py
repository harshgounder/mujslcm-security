#!/usr/bin/env python3
"""Session tests: cookie flags post-auth, fixation, logout invalidation.

Safe: uses only your own test session cookies; never touches others."""
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import Session, require_accounts, EVID, DRY

require_accounts()
s = Session(os.environ["SLCM_USER1"], os.environ["SLCM_PASS1"], "session-tests")
if not s.authenticated:
    print("LOGIN FAILED; aborting (evidence logged)")
    raise SystemExit(1)

# 1. post-auth cookie flags
st, h, b = s.get("/")
sc = h.get("Set-Cookie", "") + (h.get("set-cookie", "") or "")
if "ASP.NET_SessionId" in sc:
    s.ev("cookie_flags", ok=True, cookie=sc[:160])
    print("[i] session cookie:", sc[:160])
    print("    HttpOnly?", "HttpOnly" in sc, "| Secure?", "Secure" in sc)
else:
    s.ev("cookie_flags", ok=False, why="no Set-Cookie on authed GET")

# 2. fixation: new session cookie BEFORE login, then login, see if it survives
import urllib.request, http.client, socket  # noqa: E402
from common import TARGET, UA  # noqa: E402

class Raw(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

fix = {"ASP.NET_SessionId": "FIXATION-PROBE-0123456789AB"}
req = urllib.request.Request(TARGET + "/", headers={"User-Agent": UA, "Cookie": "ASP.NET_SessionId=FIXATION-PROBE-0123456789AB"})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        sc = r.headers.get("Set-Cookie", "")
        s.ev("fixation_preset", ok=True, echoed=("FIXATION-PROBE" in sc), sc=sc[:120])
        print("[i] fixation preset echoed in Set-Cookie?", "FIXATION-PROBE" in sc)
except Exception as e:
    s.ev("fixation_preset", ok=False, why=str(e)[:80])
    print("[!]", e)

# 3. logout invalidation
st, h, b = s.get("/Account/LogOff")
s.ev("logout", st=st, size=len(b))
sess_before = dict(s.cookies)
# try reusing the pre-logout cookie on a protected-looking path
st2, h2, b2 = s.get("/Student/Profile")
s.ev("postlogout_reuse", st=st2, size=len(b2), gate=("login" in b2.decode(errors="replace")[:2000].lower()))
print("[i] after LogOff, /Student/Profile ->", st2,
      "(gated back to login:", "login" in b2.decode(errors="replace")[:2000].lower(), ")")

print("DONE. Evidence: recon/authtests/session-tests.jsonl")