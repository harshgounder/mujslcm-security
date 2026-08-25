# Digest: w3-03-api-manipal.md

## REPORT
Source file: /home/liebert511/mujslcm-recon/research/w3-03-api-manipal.md (AI deep-research output, claims UNVERIFIED). Topic: `api.manipal.edu` exposure and its relationship to MUJ SLCM. Passive sources only.

## ANSWER SUMMARY
- Verified infrastructure: `api.manipal.edu` resolves to `43.205.223.7`; urlscan PTR and Shodan agree on Amazon EC2 ap-south-1, AS16509; Shodan records nginx 1.18.0, Ubuntu, Node.js, Express, and a Let's Encrypt cert (July 14 to October 12, 2026).
- Root behavior: HTTP 301 to HTTPS; HTTPS returns 200 JSON with one opaque `data` string; headers include `Access-Control-Allow-Origin: *` and `X-Powered-By: Express`.
- No official Swagger/OpenAPI located; the one found `api.yaml` belongs to a Vedic-Technologies physiotherapy project, a false positive.
- The SLCM relationship is unproven: no official source names `api.manipal.edu` as the MUJ SLCM backend; separate trust zones are the safe model.
- Archive shows four distinct root digests (2024-06-21, 2024-12-27, two on 2025-03-19), so the public representation changed over time.
- Community wrappers (nikeplusdash/SLCM-api, canaryGrapher/slcmAPI, manipalthetalk App-Backend) document legacy form-login scraping of `slcm.manipal.edu` with CAPTCHA; they are not current MUJ or API documentation.
- HackerTarget hostsearch lists nine API-labeled Manipal hosts; the bounded `jaipur.manipal.edu` response has no api-labeled name.
- Verdict: Moderate; the case is an API-governance and exposure concern, not a confirmed vulnerability.

## KEY FACTS
- https://dns.google/resolve?name=api.manipal.edu&type=A - A record 43.205.223.7, TTL 300.
- https://api.manipal.edu/ - HTTPS root returns JSON object with a single opaque `data` member.
- https://www.shodan.io/host/43.205.223.7 - nginx 1.18.0, Ubuntu, Node.js, Express, X-Powered-By header, wildcard CORS, Let's Encrypt cert.
- https://urlscan.io/domain/api.manipal.edu - AS16509, PTR `ec2-43-205-223-7.ap-south-1.compute.amazonaws.com`, Mumbai, CT observed 2022-04-05.
- https://api.hackertarget.com/hostsearch/?q=manipal.edu - nine API-labeled hosts (ams-api, api-convocation, api-invictus, api-mangaloreconvocation, api-mlrconv, api-summer, api-techtatva, api-timetracker, api).
- https://api.hackertarget.com/hostsearch/?q=jaipur.manipal.edu - bounded Jaipur host list with no api-labeled name.
- https://web.archive.org/cdx/search/cdx?url=api.manipal.edu%2F*&output=json&fl=timestamp,original,mimetype,statuscode,digest,length&filter=statuscode%3A200&collapse=digest - four distinct root digests, record lengths 607/717/720/718.
- https://raw.githubusercontent.com/nikeplusdash/SLCM-api/master/README.md - wrapper claims login to slcm.manipal.edu, /docs, no data storage, logout advice.
- https://raw.githubusercontent.com/nikeplusdash/SLCM-api/master/SLCM.py - requests.Session, ASP.NET fields, CAPTCHA, then profile and academics pages.
- https://raw.githubusercontent.com/canaryGrapher/slcmAPI/master/server.js - Express routes /getscores, /getattendance, /getprofile, /validateuser.
- https://github.com/Vedic-Technologies/manipal-server/blob/main/api.yaml - Swagger 2.0 physiotherapy project, false positive for SLCM attribution.
- https://mujslcm.jaipur.manipal.edu/Home/Index - MUJ portal with `@muj.manipal.edu` and parent login.
- https://muj.slcm.jaipur.manipal.edu/ - second MUJ host whose sign-in label uses `@jaipur.manipal.edu`.
- https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf - official SOP: login.microsoftonline.com, password change, MFA setup.
- https://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf - official onboarding: Admissions sends SLCM credentials to personal Gmail; parent login via mobile OTP.

## ACTIONABLE LEADS
- Internal review of `api.manipal.edu`: named owner, route and method inventory, auth policy, data schema, gateway config; compare deployed routes to source.
- Header hygiene: evaluate X-Powered-By exposure and wildcard CORS against an approved client-origin inventory.
- Reconcile the nine API-labeled hosts with cloud accounts, certificates, and owners; retire stale event systems (convocation, techtatva, invictus, summer).
- Produce a signed trust-boundary diagram for SLCM, parent OTP, Microsoft 365, and the API; do not assume federation.
- Versioned contract and change records for the root response; four digests show drift without release notes.
- nginx 1.18.0 is Shodan-tagged end-of-life; trigger an authenticated patch review, not a public exploit claim.

## FLAGS
- The supplied ASP.NET MVC/IIS/Akamai fingerprint is not corroborated; community VIEWSTATE/StudentProfile.aspx artifacts belong to legacy slcm.manipal.edu, not the MUJ portal.
- No official source proves api.manipal.edu backs SLCM; merging threat models is flagged.
- Shodan fingerprints are passive and time-bounded (last seen 2026-08-23); the report itself caps confidence by observed date.
- Wayback digests prove representation change, not semantic versions or reasons.
- CORS wildcard and header disclosure are observations, not vulnerabilities on their own.
- HackerTarget output is discovery evidence, not an authoritative CMDB.
- Reference numbering uses unusual bracket citation forms; all claims come from AI research and need verification before use.

## COVERAGE
35,260 chars read on disk (wc -m), 246/246 lines, single read pass, final page returned truncated=false, EOF confirmed; file_size 35262 bytes.