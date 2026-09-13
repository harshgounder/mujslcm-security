#!/usr/bin/env python3
"""Generate wave-5 briefs for mujslcm-security from the gap register.

Source of truth: the gap sections in the byok catalogue file
~/byok-cyber-arsenal/catalog/59-web-gap-mujslcm-portal.md (generated from disk), so the briefs
cannot drift from the register. Each gap becomes one brief with the campaign's existing header and
demand block, plus the live layer facts measured on 2026-09-13.
"""
import os, re

BYOK = os.path.expanduser("~/byok-cyber-arsenal/catalog/59-web-gap-mujslcm-portal.md")
REPO = os.path.expanduser("~/mujslcm-recon")
BRIEFS = os.path.join(REPO, "briefs")

HEADER = ("You are a senior web application security research analyst. Produce a comprehensive, "
          "citation-rich report for a university security club researching the MUJ SLCM portal "
          "(mujslcm.jaipur.manipal.edu: IIS 10, ASP.NET MVC 5.3, .NET Framework 4.7.4136.0, jQuery "
          "1.10.2 plus a bundled jQuery 3.4.1, on Microsoft Azure AS8075, Microsoft 365 identity, "
          "three Entra tenants, no attributable edge control, no HSTS, TLS 1.0 through 1.3 offered).")

FACTS = ("\n\nMEASURED FACTS (2026-09-13, live, non-destructive): 443 is the only reachable port. "
         "Verbose YSOD on four triggers with customErrors off. MVC antiforgery enforced; the "
         "antiforgery cookie is HttpOnly without Secure. trace.axd 403, elmah.axd 404. Two error "
         "page families (MVC 2,733 b and IIS 1,216 b). Method policy GET only (POST and PUT 411, "
         "everything else 404). The enc parameter is a three-stage oracle (invalid base64 gives "
         "FormatException at 4,942 b, valid base64 gives CryptographicException at 5,084 b, an "
         "empty value gives a third size). Host header, X-Forwarded-Host, absolute-URI and "
         "trust-based error bypass attempts all came back clean. The campaign never authenticated, "
         "and the aggressive phase is gated behind a signed scope letter plus two test accounts.")

DEMAND = ("\n\nDEMAND: Inline [n] citation markers with exact URLs for every claim. Data tables "
          "where listing anything. Final VERDICT section with confidence level. Chain-of-thought "
          "reasoning (cot_explicit). Target 3000+ words (w3000). Public information only; label "
          "every inference as such; never instruct unauthorized access. State explicitly which "
          "parts are safe to run pre-authorization and which need the letter and the test accounts.")


def gaps():
    txt = open(BYOK, encoding="utf-8").read()
    out = []
    for m in re.finditer(r"### (G-\d\d) ([^\n]+)\n\n- why it matters here: ([^\n]+)\n- campaign status: ([^\n]+)", txt):
        out.append({"gid": m.group(1), "title": m.group(2).strip(), "why": m.group(3).strip(),
                    "status": m.group(4).strip()})
    return out


def main():
    gs = gaps()
    os.makedirs(BRIEFS, exist_ok=True)
    written = 0
    for g in gs:
        slug = "w5-" + g["gid"].lower() + "-" + re.sub(r"[^a-z0-9]+", "-", g["title"].lower()).strip("-")[:48]
        focus = (f"{g['title']}. CAMPAIGN STATUS TO BEAT: {g['status']}. WHY IT MATTERS FOR THIS "
                 f"TARGET: {g['why']} Deliver: the technique universe for this class, every tool "
                 f"that performs it (name, exact URL, licence, free or self-host or BYOK, how it is "
                 f"driven, output format), the manual method where no tool exists, the detection "
                 f"counterpart, and a NO-TOOL GAPS plus BUILD CANDIDATES section.")
        body = f"{HEADER}\n\nFOCUS: {focus}{FACTS}{DEMAND}\n"
        open(os.path.join(BRIEFS, slug + ".txt"), "w").write(body)
        written += 1
        print(f"wrote {slug}.txt ({len(body)} chars)")
    print(f"TOTAL wave-5 briefs: {written}")


if __name__ == "__main__":
    main()
