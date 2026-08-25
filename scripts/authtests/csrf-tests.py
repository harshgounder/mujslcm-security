#!/usr/bin/env python3
"""CSRF tests: token lifetime, reuse, missing-token state changes.

Safe: state-change attempts are limited to profile mutation endpoints,
with benign field values, on your own test account only. No destructive
actions, no payments."""
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import Session, require_accounts

require_accounts()
s = Session(os.environ["SLCM_USER1"], os.environ["SLCM_PASS1"], "csrf-tests")
if not s.authenticated:
    print("LOGIN FAILED; aborting")
    raise SystemExit(1)

# 1. grab a fresh token pair
st, h, b = s.get("/")
tok1 = re.search(r'name="__RequestVerificationToken"[^>]*value="([^"]+)"', b.decode(errors="replace"))
tok1 = tok1.group(1) if tok1 else ""
cook1 = dict(s.cookies)
print("[i] fresh token captured:", bool(tok1))

# 2. POST a benign profile-ish update WITHOUT token (expect 500 if filter
#    runs, or acceptance if it does not)
st_n, h_n, b_n = s.post("/Student/Profile",
                        "MobileNumber=9999999999&AddressLine1=x&AddressLine2=y&City=z&PinCode=123456")
s.ev("no_token_post", st=st_n, size=len(b_n),
     ysod=("Exception" in b_n.decode(errors="replace")[:1500]))
print(f"[i] POST /Student/Profile without token -> st={st_n} "
      f"(500+exception={st_n == 500 or 'Exception' in b_n.decode(errors='replace')[:1500]})")

# 3. token REUSE across a fresh session (old token + old cookie)
import time  # noqa: E402
time.sleep(1.2)
st_r, h_r, b_r = s.post("/Student/Profile",
                        f"MobileNumber=9999999998&__RequestVerificationToken={tok1}",
                        extra={"Cookie": f"__RequestVerificationToken={cook1.get('__RequestVerificationToken', '')}"})
s.ev("token_reuse", st=st_r, size=len(b_r))
print(f"[i] reused old token+old cookie -> st={st_r}")

# 4. token in body (control)
st_q, h_q, b_q = s.post("/Student/Profile",
                        f"MobileNumber=9999999997&__RequestVerificationToken={tok1}")
s.ev("token_body", st=st_q, size=len(b_q))
print(f"[i] token in body (control) -> st={st_q}")

print("DONE. Evidence: recon/authtests/csrf-tests.jsonl")
print("NOTE: any 200 on steps 2/3 means the antiforgery filter did NOT")
print("protect that endpoint: log it as a finding.")