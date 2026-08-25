# Digest: w2f-11-dns-hygiene.md

## REPORT
Source file: w2f-11-dns-hygiene.md (MUJ DNS Hygiene and Spoofing Exposure Assessment)

## ANSWER SUMMARY
- `manipal.edu` uses four Azure nameservers (ns1-36 through ns4-36 across .com/.net/.org/.info). Independent checks agree all respond authoritatively on different network ranges. Good resilience.
- `jaipur.manipal.edu` is not separately delegated: NS and SOA queries return the parent `manipal.edu` SOA. Jaipur records live inside the parent zone; MUJ DNS security is a parent-zone problem.
- DNSSEC is absent: no DS at .edu, no DNSKEY, no RRSIG; Google and Verisign DNSSEC Debugger agree as of 2026-08-25. This is the top gap.
- Public AXFR is closed: HackerTarget reports Transfer failed on all four parent nameservers. Jaipur returns "no results found", not an independent refusal.
- TXT records expose a vendor map: parent has SPF for Microsoft 365, Brightspace, SendGrid, Salesforce plus Microsoft, Google, SES, Facebook, OpenAI verification markers. Jaipur has Cisco CI, Microsoft MS= markers, malformed SPF-like fragments.
- Mail auth posture: SPF hard-fail, two Microsoft DKIM selectors per domain, MX to Microsoft 365. But both DMARC policies are p=none, so exact-domain spoofing is monitored, not blocked.
- CT shows 27 unique names in the Jaipur snapshot, 25 in-namespace, spanning 2014-2026, including test labels and two external wildcard SANs.
- Verdict: MODERATE DNS and spoofing risk, HIGH confidence in observable findings.

## KEY FACTS
- https://dns.google/resolve?name=manipal.edu&type=NS - Four Azure NS answers, the authoritative topology evidence.
- https://dns.google/resolve?name=manipal.edu&type=DS - No DS answer; .edu SOA returned, DNSSEC delegation absent.
- https://dns.google/resolve?name=manipal.edu&type=DNSKEY - No DNSKEY answered, zone unsigned.
- https://dns.google/resolve?name=manipal.edu&type=RRSIG - No RRSIGs returned, no signatures.
- https://dnssec-debugger.verisignlabs.com/manipal.edu - Independent Verisign debugger confirmation of unsigned status.
- https://api.hackertarget.com/zonetransfer/?q=manipal.edu - Public AXFR check, Transfer failed on all four authoritative NS.
- https://api.hackertarget.com/zonetransfer/?q=jaipur.manipal.edu - Jaipur check returns no results, consistent with no child zone.
- https://dns.google/resolve?name=manipal.edu&type=TXT - Parent TXT map: SPF, verification markers, opaque strings.
- https://dns.google/resolve?name=jaipur.manipal.edu&type=TXT - Jaipur TXT: Cisco CI, two MS= values, malformed SPF fragments.
- https://dns.google/resolve?name=_dmarc.manipal.edu&type=TXT - Parent DMARC p=none, no rua address visible.
- https://dns.google/resolve?name=_dmarc.jaipur.manipal.edu&type=TXT - Jaipur DMARC p=none with rua to dmarc@jaipur.manipal.edu.
- https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=A - SLCM A record 98.70.14.50; direct A, no CNAME evidence for the Akamai claim.
- https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=CNAME - No CNAME answer, contradicts the supplied Akamai-fronted assumption at DNS layer.
- https://dns.google/resolve?name=manipal.edu&type=SOA - SOA with awsdns-hostmaster.amazon.com responsible name, migration residue signal.
- https://learn.microsoft.com/en-us/azure/dns/dnssec - Azure DNSSEC docs: parent DS required for validation chain.
- https://viewdns.info/dnsreport/?domain=manipal.edu - Independent NS agreement and NO GLUE note.
- https://intodns.com/manipal.edu - Second independent report of nameserver consistency across subnets.
- https://datatracker.ietf.org/doc/html/rfc7208 - RFC 7208 SPF rules, basis for judging the malformed Jaipur fragments.
- https://crt.sh/?q=%25.jaipur.manipal.edu&output=json - CT snapshot with 27 name strings and external wildcard SANs.
- https://crt.sh/?q=%25.manipal.edu - Parent CT history with api, crm, payment, online, lms, sis names.

## ACTIONABLE LEADS
- Deploy DNSSEC on the Azure-hosted `manipal.edu` zone and publish the provider DS at the .edu delegation, with rollback ownership.
- Move DMARC from p=none to quarantine then reject using aggregate report data; add rua for the parent domain.
- Build an authoritative sender register covering Outlook, Brightspace, SendGrid, Salesforce, and the direct IPv4 sender.
- Clean Jaipur TXT residue: the Brightspace-only fragment and the ip4: fragment without v=spf1 are RFC 7208-noncompliant and should be removed or corrected.
- Reconcile all 25 Jaipur CT names plus parent history against asset inventory; disposition each as current, non-production, redirect, retired, unknown.
- Verify the SLCM A record 98.70.14.50 against the Akamai premise; check origin of the awsdns-hostmaster SOA field.
- Add CAA policy for parent and Jaipur zones; both return no CAA answer.
- Monitor CT continuously for new serials, issuers, and SAN groups; report anomalies through MUJ channels.

## FLAGS
- Contradiction: report says Akamai is a supplied premise and DNS shows a direct A record with no CNAME; the Akamai-fronted architecture is not confirmed at DNS layer.
- Suspicious claim: `awsdns-hostmaster.amazon.com` SOA field implies past Route 53 use; labeled inference, needs owner confirmation.
- Unverified: DNSSEC absence is dated 2026-08-25; DNS state can change, treat as point-in-time.
- Hallucination risk: TXT verification token details are redacted on purpose; counts are claims from a single resolver query. Re-query dns.google to confirm before relying on exact values.
- The "no results found" Jaipur AXFR result must not be read as Jaipur refusing transfers; no Jaipur zone exists publicly.
- Malformed SPF fragment judgment depends on RFC 7208 interpretation; the fragment text is quoted but partly redacted.
- Verisign debugger result is cited without a saved copy; re-run before publishing findings.
- CT name classification (role labels like ERP, DMS) is inference from acronyms, not verified function.

## COVERAGE
- Chars read: 40122
- EOF confirmed: true (read_file truncated=false, 326 lines)