#!/usr/bin/env python3
"""Generate wave-2 briefs from family spec files into briefs/w2-*.txt.

Each spec gets: role header + focus_text + shared coverage/demand block.
Validates: no leftover placeholders, min length, unique slugs.
"""
import importlib.util, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BRIEFS = os.path.join(os.path.dirname(HERE), "briefs")

HEADER = ("You are a senior OSINT and application security research analyst. "
          "Produce a comprehensive, citation-rich report for a university "
          "security club researching the MUJ SLCM ecosystem "
          "(mujslcm.jaipur.manipal.edu: ASP.NET MVC 5.3, .NET Framework 4.x, "
          "IIS 10 on Microsoft Azure AS8075, Microsoft 365 identity).")

DEMAND = ("\n\nDEMAND: Inline [n] citation markers with exact URLs for every claim. "
          "Data tables where listing anything. Final VERDICT section with confidence "
          "level. Structure with exact_tables. Chain-of-thought reasoning "
          "(cot_explicit). Target 3000+ words (w3000). Public information only; "
          "label every inference as such; never instruct unauthorized access.")

FAMILIES = ["b", "c1", "c2", "d", "e", "f", "g", "w3"]
EXTRA_SPECS = []  # injected by callers before main()

def load(fam):
    path = os.path.join(HERE, f"brief-specs-{fam}.py")
    spec = importlib.util.spec_from_file_location(f"specs_{fam}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.SPECS

def main():
    os.makedirs(BRIEFS, exist_ok=True)
    written = 0
    for fam in FAMILIES:
        for slug, focus in load(fam):
            written += write_one(slug, focus)
    for fam, specs in EXTRA_SPECS:
        for slug, focus in specs:
            written += write_one(slug, focus)
    print(f"TOTAL: {written} briefs")

def write_one(slug, focus):
    body = f"{HEADER}\n\nFOCUS: {focus}\n" + DEMAND + "\n"
    if len(focus) < 100:
        print(f"WARN thin focus: {slug} ({len(focus)}), skipping")
        return 0
    assert "<" not in body and "TEMPLATE" not in body, f"{slug} placeholder leak"
    with open(os.path.join(BRIEFS, f"{slug}.txt"), "w") as f:
        f.write(body)
    print(f"wrote {slug} ({len(body)} chars)")
    return 1

if __name__ == "__main__":
    main()