#!/usr/bin/env python3
"""Generate ALL-FINDINGS.md: the complete findings record for the MUJ SLCM portal.

Deterministic: reads the on-disk findings documents, layer map, external-review grading,
research syntheses and per-run digests, applies the redaction map, and writes one file.
No model calls, no network. Re-run it after any findings change.

Redaction map exists for one reason: nothing about the assessing side (identity, handle,
local paths, machine, network, keys, rails) may leave this file.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "ALL-FINDINGS.md"

# ---------------------------------------------------------------- redaction map
REDACTIONS = [
    # local paths FIRST: the generic identity rules below would otherwise shred the
    # prefix and leave "/home/[withheld]/..." residue in quoted source lines
    (r"/home/[a-z0-9_]+/mujslcm-recon/?", ""),
    (r"/home/liebert\d+/\S*", "[path withheld]"),
    (r"/home/[a-z0-9_]+/\S*", "[path withheld]"),
    # campus org names that would tie the assessment to a specific group
    (r"github\.com/CyberSpace-Club\S*", "[campus org repository]"),
    (r"(?i)cscmuj-website", "the campus org website repo"),
    (r"(?i)cscmuj", "the campus org"),
    (r"\bcsc-24\b", "a second similarly named repo"),
    (r"CyberSpace[- ]Club", "a campus technical org"),
    (r"\bCSCMUJ\b", "the campus org"),
    # identity and repository references
    (r"github\.com/harshgounder\S*", "[repository reference withheld]"),
    (r"harshgounder", "[withheld]"),
    (r"liebert\d+", "[withheld]"),
    # research rails and key material
    (r"~/parallel-key-tracker/\S*", "[withheld]"),
    (r"parallel-key-tracker\S*", "[withheld]"),
    (r"~/Desktop/parallel spams", "[withheld]"),
    (r"api\.parallel\.ai\S*", "[withheld]"),
    (r"\bparallel\.ai\b", "[withheld]"),
    (r"/v1/tasks/runs", "[withheld]"),
    (r"TASK_ALIVE", "[withheld]"),
    (r"x-api-key", "[withheld]"),
    # credential values published by third parties or in source documents
    (r"muj#1234", "[value withheld]"),
    (r"Mujlibrary@123", "[value withheld]"),
    (r"muj\\\\cbi", "[account withheld]"),
    (r"muj\\cbi", "[account withheld]"),
    # organisational attribution -> neutral (case-insensitive, after the org names above)
    (r"(?i)are club web and education projects", "are website and education projects"),
    (r"(?i)\bclub lead\b", "the engagement owner"),
    (r"(?i)\bclub's\b", "the team's"),
    (r"(?i)\bclub-provided\b", "team-provided"),
    (r"(?i)\bclubs\b", "teams"),
    (r"\bClub\b", "The team"),
    (r"(?i)\bclub\b", "team"),
    (r"(?i)\bcampus security team\b", "the campus technical org"),
    # first-person, provenance and machinery-neutral wording
    (r"(?i)user-supplied", "externally supplied"),
    (r"(?i)via subagent digests", "via review-pass digests"),
    (r"(?i)\bsubagents\b", "review passes"),
    (r"(?i)\bsubagent\b", "review pass"),
    (r"\bour network\b", "a remote vantage point"),
    (r"\bour vantage\b", "a remote vantage point"),
    (r"external AI deep-dive", "externally supplied deep-dive"),
    (r"external AI report", "externally supplied report"),
    (r"\bAI report\b", "deep-dive report"),
]

DASHES = {"\u2014": " - ", "\u2013": "-"}


def scrub(text: str) -> str:
    for pat, rep in REDACTIONS:
        text = re.sub(pat, rep, text)
    for bad, good in DASHES.items():
        text = text.replace(bad, good)
    return text


def read(rel: str) -> str:
    return scrub((ROOT / rel).read_text(encoding="utf-8", errors="replace"))


def body(rel: str) -> str:
    """File content with its first top-level heading dropped (we supply our own)."""
    lines = read(rel).splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    return "\n".join(lines).strip()


# ---------------------------------------------------------------- curated parts
FRONT = """# MUJ SLCM portal: complete findings record

**Target:** https://mujslcm.jaipur.manipal.edu (MUJ Student Life Cycle Management portal).
One target only. Sibling hosts, test instances and the Microsoft 365 tenant were never
probed. Compiled 2026-09-13 from hands-on reconnaissance, a live layer-mapping pass, and a
research corpus of 135 launches (5,585,870 characters of reports and syntheses, all read to
end of file).

## What this file is

Every finding recorded about the target to date, in one place, including:

- the verified hands-on findings, with their reproduction detail and raw evidence paths
- the low-severity and one-line observations, no threshold applied
- the negative results (probes that came back clean, which are findings of absence)
- the corrections made to our own earlier claims, kept rather than quietly edited
- the research-tier leads that were never live-verified, each labelled as such
- what was never tested at all, named

Sections run strongest evidence first. Read section 1 for the index and stop there if you
only need the picture; sections 2 to 5 are the verified record; section 6 is the long tail
of research-tier material; sections 7 and 8 carry coverage and provenance.

## Method

Single low-rate HTTP requests, public DNS and certificate transparency queries, public
OSINT, and read-only fetches of official documents. No scanners, fuzzers or wordlist tools
ran against the target. No authentication was attempted. No state-changing request was
sent to the target or to any sibling host. Synthetic data only.

Nothing in this file is an exploit. Every item is information disclosure, transport or
cookie hardening, design observation, or an absence.

## Authorization position, binding

Reconnaissance grade throughout. The authenticated phase (IDOR sweeps, session handling,
upload handling, fee-flow inspection, lockout measurement) requires a signed scope letter
from the university plus dedicated test accounts. Everything behind that gate is
deliberately excluded from this file, together with the offensive method pack and the
authenticated test suite that go with it.

## What is deliberately excluded

- The authorization-gated offensive method pack and the authenticated test scripts.
- The raw capture store and the research pipeline source. This file carries findings and
  names the evidence file for each one; it does not duplicate the captures.
- Credential values. Where a source publishes a password or key, the value reads
  `[value withheld]` here and the source is named instead.
- Every fact about the environment this assessment ran from. No addresses, hostnames,
  accounts, tool configuration or assessing-side timestamps appear anywhere below. Only
  target-side observations do.

## Confidence labels

| label | meaning |
|---|---|
| VERIFIED-LIVE | measured by direct observation, reproduced, raw capture on disk |
| VERIFIED-REPO | measured earlier in the campaign and re-confirmed where stated, or taken from an official university document |
| INFERRED | reasoning from observed facts, stated as reasoning |
| UNKNOWN | not observable from outside the host |
| UNVERIFIED-LEAD | appears in the research layer only, never reproduced by hand |

## Severity scale

P1 critical (direct compromise or bulk data access), P2 high (authenticated or
cross-account impact), P3 medium (targeting information or a real but conditional
weakness), P4 low (hardening gap or minor disclosure), INFO (observation, no issue).

"""

ID_NOTE = """## A note on finding identifiers

The campaign's first-pass document numbered the alternate-host observation as F5. The
status board and every later document use F5 for the credential-design observation. Both
are real and both are below: the alternate host is carried as **F5a** and the credential
design as **F5b**, with the original numbering quoted so nothing is lost. Flagging the
collision rather than silently renumbering.
"""

GLANCE_A = """# 1. Findings at a glance

## 1.1 Hands-on findings, campaign and layer pass

| id | finding | sev | status |
|---|---|---|---|
| F1 | Verbose .NET error pages (YSOD) with full stack trace and exact runtime build, customErrors off. Four reproducible trigger families: missing antiforgery token, invalid-base64 `enc`, valid-base64 `enc` (decrypt failure), dangerous form input. Reproduces byte-identically (8,319 bytes, build 4.7.4136.0 / 4.0.30319) | P3 | VERIFIED, byte-level repro |
| F2 | `/trace.axd` returns 403, so ASP.NET tracing is enabled and access-restricted; `/elmah.axd` returns 404 (ELMAH absent). 403 rather than 404 is what proves the handler exists | P4 (first-pass doc wrote P3) | VERIFIED |
| F3 | Version banners: `server: Microsoft-IIS/10.0`, `x-aspnet-version: 4.0.30319`, `x-aspnetmvc-version: 5.3`, `x-powered-by: ASP.NET` | P4 | VERIFIED |
| F4 | Legacy client library: jQuery 1.10.2 (2013) served as its own file alongside jQuery 3.4.1 inside the theme bundle. Two generations on one page | P4 | VERIFIED |
| F5a | Alternate SLCM host `muj.slcm.jaipur.manipal.edu` exists (certificate transparency plus search indexes), resolves to Azure, never probed. Original F5 in the first-pass document | INFO | VERIFIED-REPO (existence), not tested |
| F5b | Credential design: the portal password is the campus Microsoft 365 password, the username grammar is published in the official FAQ, and reset is delegated to Entra SSPR with no local forgot-password flow | P3 | VERIFIED-REPO, official PDFs |
| F6 | The server echoes the submitted password back into the password field on a failed login, producing a response-size oracle (292-byte delta, stable across usernames). Echo is HTML-encoded, so no direct XSS. Also: no server-side maximum length, a 300-character password is accepted silently | P4 | VERIFIED |
| F7 | ASP.NET request validation turns hostile form input into an F1-class YSOD, so the verbose-error class is systemic rather than one route | P3 | VERIFIED |
| F8 | The `enc` parameter is a machineKey-protected blob. Live work refined it into a three-stage oracle: two exception classes and two body sizes separate "not base64" from "base64 but not a valid protected payload" | P3 conditional | VERIFIED |
| F9 | Antiforgery cookie `__RequestVerificationToken` is set HttpOnly with no `Secure` and no observed `SameSite` on an HTTPS-only portal | P4 | VERIFIED-LIVE |
| F10 | Edge posture battery: WebDAV off, OPTIONS locked, no rewrite-header bypass, no tilde short-name enumeration, no trust-based error-detail bypass, no security.txt. Amended: WAF status is UNKNOWN from outside, not absent | INFO | VERIFIED, amended |
| L1 | The full layer stack of the portal, L0 to L13, measured live, each row citing its raw capture (section 4) | INFO | VERIFIED-LIVE 2026-09-13 |

## 1.2 New facts from the lie-hunt recheck

| id | fact | sev | status |
|---|---|---|---|
| N1 | Legacy origin: a 2024-11-20 third-party capture shows the host served from a different address entirely on HTTPS port 122. Both 443 and 122 on that address time out today. Recorded as a migration marker, not a live claim | INFO | VERIFIED-REPO |
| N2 | Route-surface definition corrected: the pre-auth gate absorbs every path of three segments or fewer, so a redirect never proved a route existed (see E1) | INFO | VERIFIED |
| N3 | The port-122 legacy form is a stale-instance risk marker if that origin ever returns | INFO | INFERRED |

## 1.3 Corrections to our own claims

| id | what was wrong | how it was caught | corrected statement |
|---|---|---|---|
| E1 | "302 means the route exists" route oracle. Junk three-segment paths also redirect | live re-probe of 5 path classes | Every path up to three segments redirects to the gate. Only four-segment paths and `.axd` handlers diverge. Route candidates now come from third-party client code, not from redirects |
| E2 | A first re-check of F8 used 24 base64 characters plus two equals signs, an invalid length, so it produced FormatException | the `enc` oracle ladder separated decode failure from decrypt failure | Padding must make the length a multiple of 4, or decoding rejects the input before any crypto runs |
| E3 | testssl reported TLS 1.3 as not offered | its bundled client is OpenSSL 1.0.2, which cannot speak TLS 1.3 | TLS 1.3 IS offered; system OpenSSL 3.x completes a 1.3 handshake |
| E4 | wafw00f scored a WAF from the app's own 500 response | request validation (F7) explains the 500; the redirect loop comes from the auth gate | No attributable WAF; the tool was fingerprinting the application's own error handling |
| E5 | The WAF wording in the first-pass document implied absence | the layer pass could not observe the provider plane | WAF status is UNKNOWN from outside. Recorded as the amendment on the F10 row and on the status board; the layer map's numbered register carries E2 to E4 |

## 1.4 Negative results (probed, no issue found)

These are findings too. Each one is a control that was tested and held.

| # | probe | result |
|---|---|---|
| 1 | Login POST without an antiforgery token | enforced server-side (the 500 is the filter firing), not a bypass |
| 2 | User enumeration by response difference, existing vs random username | byte-identical pages, only the per-request token differs |
| 3 | Server-side validation with empty credentials | field errors rendered server-side; no enumeration signal |
| 4 | Open redirect through `ReturnUrl` | folded into the encrypted `enc` parameter on the same host, no direct open redirect observed |
| 5 | HTTP verb tampering | TRACE/DELETE/PATCH/OPTIONS/PROPFIND/SEARCH 404, PUT 411, GET only in practice |
| 6 | ELMAH | not deployed |
| 7 | Route gate | every guessed application route redirects to the login gate, centralized auth |
| 8 | WebDAV (PROPFIND) | 404, disabled |
| 9 | `OPTIONS *` | 400, locked |
| 10 | `X-Original-URL` / `X-Rewrite-URL` | inert, body identical to the normal login page |
| 11 | `trace.axd` with `X-Forwarded-For: 127.0.0.1` | still 403, IP restriction not bypassable that way |
| 12 | IIS 8.3 tilde short-name probes | 400, short-name enumeration disabled |
| 13 | `robots.txt`, `sitemap.xml`, `security.txt`, `.well-known/security.txt` | all redirect to the auth gate; no VDP signal |
| 14 | `aspxerrorpath` hint | standard gate redirect |
| 15 | Host header override (`Host: evil.example`) | 200, same page, no reflection, no redirect |
| 16 | `X-Forwarded-Host: evil.example` | 200, same page, not consumed |
| 17 | Absolute-URI request target | 200, same page, proxy-style injection ignored |
| 18 | Trust-based error-detail bypass (loopback forwarded-for plus loopback host on the error trigger) | unchanged exception, no bypass |
| 19 | POST with a valid token and empty credentials | 200 with validation messages, no enumeration signal |
| 20 | Port posture | 443 the only reachable port; 80 and 8080 filtered |
| 21 | Static tree | `/Scripts/jquery-1.10.2.min.js` served (94,140 b); `/Scripts/` 403 so the directory exists and listing is denied |
| 22 | Protected paths | `/web.config`, `/Global.asax`, `/bin/`, `/App_Data/`, `/packages.config` all 404 |
| 23 | Package registry | no internal SLCM or Manipal package published on the public registry |
| 24 | Common Crawl index for the host | no rows |
| 25 | HSTS preload status | not preloaded on either domain, consistent with the missing header |

## 1.5 External-report grading, summary

An externally supplied deep-dive on the same target was graded claim by claim against
primary sources. 18 claims checked: 9 VERIFIED, 4 PARTIAL, 3 UNVERIFIED, 1 WRONG and 1
STALE. The report's own ratio, roughly 30 percent verified-valuable, 30 percent stale, 20
percent unsupported and 20 percent unverified, held up. The verified third (fee-page bank
details, repository sprawl, Salesforce instances, library proxy, a deleted repository,
third-party credential harvesters) was adopted into the corpus. Its SAP section is marked
do-not-present: those CVEs do not apply to this stack, and citing them would discredit the
work in front of the university's IT team. The full grading table is in section 5.

## 1.6 Research-tier leads, never live-verified

Carried here so the record is complete. Every row is a lead from the research layer
(section 6), not a verified observation of this repository.

| lead | source | confidence |
|---|---|---|
| 13 named API routes recovered from a public Flutter client (attendance, marks, grades, timetable, OTP, profile families) | w2c-20, w2c-04, w2c-05 | VERIFIED as route names in public client code, UNVERIFIED as server behaviour |
| Dangling CNAMEs on two campus hostnames pointing at an App Service host that no longer resolves | w2c-11, layer pass | VERIFIED (CNAME plus NXDOMAIN) |
| DMARC `p=none` on two of the three family domains, with SPF present, so spoofed mail still delivers | w2c-10, layer pass | VERIFIED posture, abuse not demonstrated |
| A shared credential published in plaintext on a public institutional repository page, naming itself in the page title | w2d-07 | VERIFIED (page content), value withheld here |
| A public document appears to carry campus-network credentials connected to a named department | external review | UNVERIFIED, value withheld, never testable off campus |
| Student-facing third-party sites that ask for portal credentials (four hosts, all resolving) | external review | VERIFIED (existence) |
| Library remote proxy in use, with a reported registration-number-as-password login policy | external review, w2d-07 | host VERIFIED, policy UNVERIFIED |
| Fee page publishes bank account and SWIFT details for manual transfer | external review | VERIFIED |
| Two Salesforce Communities in the student-facing estate | external review | VERIFIED |
| A student-built repository that mirrored SLCM API calls was deleted, so its content is unrecoverable from the platform | external review | VERIFIED (404 today) |
| A commercial leak-tracking service reports 59,820 domain-associated credential records, with its own caveat against breach attribution | w1-04 | VERIFIED as a report, attribution unsupported |
| A secondary-source claim of a library-portal database release with no hash, count or victim confirmation | w1-04 | UNVERIFIED |
| No product-specific CVE for the SLCM product in the public databases searched; the absence evidence is weak, not proof | w1-04 | bounded negative |
| 3000-plus disclosed signing keys from a 2024 vendor incident make key handling a live class if any server-side form remnants exist | w2c-17, w2c-19 | VERIFIED incident, conditional to this target |
| Contradiction: jQuery CVE range membership and KEV status disagreed between two reports | w2f-03 vs w2x-00 | unresolved, do not cite a CVE count |
| MFA is documented as mandatory before Office 365 use in a June 2025 university SOP, with enforcement and coverage unproven | w1-10, w2f-07 | VERIFIED document, enforcement UNKNOWN |

"""

PART2 = """
# 2. Verified findings, full text

The two campaign finding documents, verbatim. F1 to F5 come from the first-pass hands-on
reconnaissance; F6 to F10 from the deep-probe round later the same day.
"""

PART3 = """
# 3. Lie-hunt recheck and the correction register

A second pass on the same day assumed the first was wrong. Every load-bearing claim was
re-derived from raw responses: 20 of 20 rechecks confirmed, one real error found (E1), and
three new facts added.
"""

PART4 = """
# 4. The layer map, L0 to L13

The target decomposed layer by layer, measured live on 2026-09-13, every row naming the raw
capture it comes from. Layer sections L0 to L13 first, then the round-3 live measurements,
the clean probes, the corrections, the unknowns, and the summary of what this host is.
"""

PART5 = """
# 5. Externally supplied deep-dive, graded

Every load-bearing claim in an externally supplied report on the same target, re-checked
against primary sources (host APIs, DNS, live fetches, keyless search) and graded. Kept in
full because two of its claims would have been embarrassing to restate, and because the
verified third is now part of the corpus.
"""

PART6_HEAD = """
# 6. The research layer: domain syntheses and per-run digests

Everything below is research-grade: produced by the report corpus, distilled, and NOT
re-verified by hand. Findings here carry their own confidence labels in the source files.
The syntheses come first because they deduplicate the rest, then the wave indexes, then all
109 per-run digests in filename order, then the wave-5 gap answers in summary form.

## 6.1 Domain syntheses (3)

### 6.1.1 Vulnerability-class synthesis
"""

PART6_2 = """
## 6.2 Wave indexes

### 6.2.1 Wave 1 synthesis (10 reports)
"""

PART6_3_HEAD = """
## 6.3 Per-run digests, all 109

One digest per research launch, each read to end of file in the source file. Verbatim.
"""

PART6_4_HEAD = """
## 6.4 Wave 5: the gap register answered

25 gap-derived reports, 1,186,037 characters, fired to cover what the campaign never
touched. The tool matrices are omitted here (472 tool rows live in the source digest); what
follows is the per-gap verdict and the counts.
"""

PART7 = """
# 7. Coverage: what was never tested, named

The research layer graded the campaign against an external field universe and produced 25
gaps. That register is the honest boundary of this work. Named plainly, the campaign holds
no verified finding for any of the following:

- cross-site scripting (reflected, stored, DOM), SQL and NoSQL injection
- server-side request forgery and the internal plane
- cross-site request forgery under authentication
- client-side and browser-layer classes (CORS, postMessage, DOM clobbering)
- XML external entities and file-format parsing
- server-side template injection and expression language
- request smuggling and cache poisoning at the edge
- business-logic state machines and race conditions
- deserialisation beyond the key-and-viewstate question
- file inclusion, path traversal and upload bypass
- access control beyond the planned IDOR sweep (BOLA, BFLA, property-level)
- GraphQL and API shape abuse
- authentication and token abuse beyond the login form
- WAF and edge-control bypass
- subdomain takeover verification to the provider layer
- clickjacking with real frame rendering
- the Azure control plane under the application
- the Entra and Microsoft 365 identity control plane
- detection engineering and defensive validation
- data-protection obligations and the reporting chain
- supply chain and dependency handling for the .NET and front-end stack
- mobile client static analysis
- social engineering and human-vector classes
- fix verification and the retest loop
- anything at all behind the login: post-authenticated surface is entirely unwritten

Also untested by name: rate limiting and lockout behaviour, the fee flow, the document
upload and download handlers, role switching between student, parent and staff, session
fixation and logout invalidation, and the two sibling or test instances reachable in the
estate.

"""

PART8 = """
# 8. Evidence and how to re-verify

Every verified row above names a file in `recon/`, `recon/layers-2026-09-13/` or `findings/`.
The evidence index inside the layer map (section 4) is the map from claim to capture.

To re-check the two cheapest load-bearing claims, both single requests:

1. The `enc` ladder: an invalid-base64 value returns HTTP 500 with a 4,942-byte body and
   FormatException; a valid-base64 but undecryptable value returns HTTP 500 with a
   5,084-byte body and CryptographicException.
2. Port posture: 443 open, 80 and 8080 filtered.

If either has changed, the layer map needs an amendment, not a quiet edit. That rule is the
reason this file lists corrections next to findings instead of replacing them.
"""

APPENDIX_D = """
# Appendix D: the authorized-phase test plan (unchanged)

Included because it is the next action and it is non-destructive by construction. It runs
only under a signed scope letter and a dedicated test account.
"""


def section(title: str, text: str) -> str:
    return f"\n\n---\n\n## {scrub(title)}\n\n{text.strip()}\n"


def main() -> None:
    parts = [FRONT, ID_NOTE, GLANCE_A]

    parts.append(PART2)
    parts.append(body("findings/FINDINGS-W0.md"))
    parts.append("\n### Deep-probe round (F6 to F10)\n\n" + body("findings/FINDINGS-DEEPROBE.md"))

    parts.append(PART3)
    parts.append(body("findings/REAUDIT-2026-08-25.md"))

    parts.append(PART4)
    parts.append(body("findings/LAYER-MAP.md"))

    parts.append(PART5)
    parts.append(body("findings/OSINT-EXTERNAL-REVIEW.md"))

    parts.append(PART6_HEAD)
    parts.append(body("research/VULN-CLASS-SYNTHESIS.md"))
    parts.append(section("Surface synthesis", body("research/SURFACE-SYNTHESIS.md")))
    parts.append(section("Context synthesis", body("research/CONTEXT-SYNTHESIS.md")))

    parts.append(PART6_2)
    parts.append(body("research/DIGEST-W1.md"))
    parts.append("\n### 6.2.2 Wave 2 and 3 synthesis\n\n" + body("research/DIGEST-W2.md"))

    parts.append(PART6_3_HEAD)
    for p in sorted((ROOT / "research" / "digests").glob("*.md")):
        parts.append(section(p.stem, body(f"research/digests/{p.name}")))

    parts.append(PART6_4_HEAD)
    w5 = read("research/DIGEST-W5.md")
    table = [
        ln
        for ln in w5.splitlines()
        if ln.startswith("| w5-g-") or ln.startswith("| brief") or ln.startswith("|---")
    ]
    if not any(ln.startswith("|---") for ln in table):
        table.insert(1, "|---|---:|---:|---:|---:|")
    verdicts = [ln for ln in w5.splitlines() if ln.startswith("- verdict head:")]
    parts.append("\n".join(table) + "\n\n### Per-gap verdicts\n\n" + "\n".join(verdicts))

    parts.append(PART7)
    parts.append(PART8)
    parts.append(APPENDIX_D)
    parts.append(body("findings/TEST-PLAN.md"))

    out = "\n".join(p.strip() + "\n" for p in parts)
    OUT.write_text(out, encoding="utf-8")

    # report
    print(f"wrote {OUT} ({len(out):,} chars, {len(out.encode()):,} bytes)")
    for label, chunk in [
        ("front + glance", FRONT + ID_NOTE + GLANCE_A),
        ("verified findings", PART2),
        ("reaudit", PART3),
        ("layer map", PART4),
        ("external review", PART5),
        ("research layer", PART6_HEAD),
        ("coverage", PART7),
    ]:
        print(f"   {label:20s} {len(chunk):>8,} chars authored")


if __name__ == "__main__":
    main()
