# TEST-PLAN — MUJ SLCM (authorized club testing)

Status: PRE-AUTH phase done (recon). AUTH phase needs club test credentials.
Severity scale: P1 critical, P2 high, P3 medium, P4 low.

## Principles (from README, binding)

- Non-destructive only. No data modification, no deletion, no DoS, no
  volume spraying. Low request rates, manual pacing.
- One throwaway test account (club-provided) for all auth tests.
- Anything live-exploitable: minimal PoC on our own account, document,
  STOP, report. Never chain further.
- Every finding: repro steps, expected vs actual, evidence saved.

## Phase 1: PRE-AUTH (done — see FINDINGS-W0.md)

- F1 verbose YSOD (missing CSRF on login POST) P3
- F2 trace.axd 403 (exists, restricted) P3
- F3 version headers (IIS/ASP.NET/MVC versions exposed) P4
- F4 jQuery 1.10.2 legacy client lib P4
- F5 alternate SLCM host (intel, out of scope to test) INFO
- Clean: anti-CSRF enforced, no user enum via login response diff,
  server-side validation active, no open redirect observed (enc param),
  verbs locked, ELMAH 404, centralized auth gate.

## Phase 2: AUTH-CONTEXT (needs credentials)

Priority order (class -> test -> expected evidence):

1. IDOR sweep (P1). After login: enumerate own resources by ID:
   notifications, documents, fee receipts, timetable views, marks API.
   Try neighbor IDs. Evidence: another student's data visible.
   Where: /Student/*, /api/*, document download handlers.
2. Role/privilege boundaries (P1). EmailFor/LoginFor hidden fields:
   student vs parent vs staff. Does a student token access staff
   endpoints? Test with student account against /Staff/*-guessed URLs.
3. Session handling (P2). Session cookie flags (Secure? HttpOnly?),
   session fixation (login with pre-set ASP.NET_SessionId value),
   session timeout, concurrent sessions, logout invalidation.
4. CSRF on post-login state changes (P2). Any action without the
   __RequestVerificationToken check: profile update, settings.
   Test with token removed + cookie fixed.
5. File upload (P2). Document upload module: extension filtering,
   content-type trust, filename handling, path traversal on download.
   Upload only inert test files on our own account.
6. Fee module (P2). Only if club approved: inspect POST fields for
   tamperable amount/currency. Do NOT submit a real payment.
   Document field names from page source, no modification.
7. Rate limiting / lockout (P3). NEVER against real accounts: only our
   throwaway account, small batches (10-20 attempts), log server
   responses (lockout message? 429? nothing?).
8. Parameter tampering on own data (P3). Marks display? No write
   attempts. Only reads with modified IDs.
9. Path traversal / IIS quirks (P3). Dot-segment and backslash URL
   variants on document URLs (IIS normalization), short-name 8.3 scan
   is active-ish: keep to 10-20 requests, skip if WAF blocks.
10. Header/behavior re-checks after auth (P3). Cache-Control on
    student pages (private data caching), Referrer leakage of tokens.

## Phase 3: DISCLOSURE (fixes + report)

- All findings: repro, impact, proposed fix, screenshots/artifacts.
- Disclosure path: club lead -> university nodal officer; CC AMS team
  (dms@ / ams@jaipur.manipal.edu) and IT Infra (it.support@...);
  CERT-In only if university does not respond in 90 days.
- No public disclosure ever without written university consent.

## Out of bounds (do not touch)

- muj.slcm.jaipur.manipal.edu, mujerp, mujone, rms, helpdesk,
  admissions, any other hostname. One target only.
- slcm.manipal.edu and any sibling campus systems (reference only).
- Microsoft 365 tenant: no password resets, no MFA toggling, no
  enumeration beyond public discovery, no messaging.
- Third-party services (NoPaperForms, Brightspace, Webex): read-only.