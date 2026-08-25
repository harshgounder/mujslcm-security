# DIGEST-W2 — waves 2+3 synthesis (98 research reports)

Merged 2026-08-25. Pipeline: 98 reports -> 98 digests (each read to EOF,
style-gated, evidence-labelled) -> 3 domain syntheses -> this index.

## Read the three syntheses first

- research/VULN-CLASS-SYNTHESIS.md (16.2K, 35 digests: w2c-* + w2f-* +
  w2x-00): cross-cutting themes (cookie-session auth, M365 intent,
  register-number grammar, header gaps, TLS grade B, DMARC p=none,
  machineKey unproven, Akamai refuted), top leads, contradiction clusters,
  what to test first with credentials.
- research/SURFACE-SYNTHESIS.md (17.2K, 38 digests: w2b-* + w2d-* + w3-*):
  infrastructure map of 23 hosts with cloud attribution, 13 public
  data-exposure classes, 10 leads (DSpace credential exposure, NTT DATA
  Pay URL, mujconnect.in, dmsmuj API TESTING, npfslcm CT), per-host gaps.
- research/CONTEXT-SYNTHESIS.md (15.9K, 26 digests: w2e-* + w2g-*):
  precedent (IISc only verified India-university VDP; CERT-In RVDCP;
  90-day norm), vendor picture (SLCM = ecosystem label, SAP historical
  lead, Keen front end, Salesforce/Deloitte 2026 modernization), public
  footprint (KrishGoel .env.example with populated credentials top,
  vikrant500 cookies.txt, DK10WS route map, SlcmPlus), disclosure path,
  8 knowledge gaps.

Plus wave 1: research/DIGEST-W1.md (10 ultra8x reports, same discipline).

## Pipeline totals

- 110 runs launched, 109 saved (w2c-03 relaunched after server-side fail)
- 109 digests, all EOF-confirmed, zero style violations (programmatic sweep)
- 3 synthesis docs, all EOF/coverage-tabled, style-clean
- 110 replayable briefs in briefs/; launcher + watcher in scripts/

## Open items (tracked)

- Verify KrishGoel + vikrant500 artifacts (do not touch, document only)
- Confirm mujlibrary credential-like title (P0, club check with librarian)
- w2c-20 API routes: the 13-route BOLA test list is the auth-phase core
- Monitor dmsmuj, helpdesk, npfslcm reactivation (cron candidate)
- Phase 2 needs: written club authorization + 2 test accounts