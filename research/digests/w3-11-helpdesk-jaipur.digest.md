# Digest: w3-11-helpdesk-jaipur.md

## REPORT
Source file: w3-11-helpdesk-jaipur.md (reconstructing the MUJ helpdesk host from public signals)

## ANSWER SUMMARY
- helpdesk.jaipur.manipal.edu is NXDOMAIN now. dns.google returns status 3 for both A and CNAME queries, no answer, SOA authority for manipal.edu.
- Two crt.sh certificates exist for the exact hostname, Entrust DV TLS Issuing RSA CA 2, CT entries 2026-01-08 09:35:53-54 UTC, validity 2026-01-08 to 2027-01-08. Cert IDs 23628924661 and 23628923708.
- All tested content archives are empty for the target: Internet Archive CDX and availability API, Common Crawl 2026 collections, URLScan, Mnemonic passive DNS.
- Vendor attribution is unresolved. osTicket is proven only for the separate MUCM host helpdesk.manipal.edu.my, not for the MUJ hostname.
- MUJ official FAQ and ICT documents confirm SLCM and support contacts (dms@, ams@, it.support@jaipur.manipal.edu, helpline 0141-3999100) but never mention the helpdesk hostname or a ticketing system.
- Verdict: likely MUJ-related hostname prepared for TLS around 2026-01-08; application identity, vendor, and production activation are unproven.

## KEY FACTS
- https://dns.google/resolve?name=helpdesk.jaipur.manipal.edu&type=A - current A query is NXDOMAIN, no answer.
- https://dns.google/resolve?name=helpdesk.jaipur.manipal.edu&type=CNAME - current CNAME query is NXDOMAIN, no target recovered.
- https://crt.sh/?q=%25.helpdesk.jaipur.manipal.edu&output=json - the only strong target signal: two exact-host CT records logged 2026-01-08.
- https://web.archive.org/cdx/search/cdx?url=helpdesk.jaipur.manipal.edu%2F*&output=json&fl=timestamp%2Coriginal%2Cstatuscode%2Cmimetype%2Cdigest%2Clength - empty array, no Wayback captures in tested views.
- https://archive.org/wayback/available?url=helpdesk.jaipur.manipal.edu%2F&timestamp=20260108 - no archived snapshot for the certificate date.
- https://urlscan.io/api/v1/search/?q=domain%3Ahelpdesk.jaipur.manipal.edu - zero URLScan results, total 0.
- https://api.mnemonic.no/pdns/v3/helpdesk.jaipur.manipal.edu - passive DNS count 0, empty data array.
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - official FAQ: registration link, Outlook ID password, AMS/DMS/IT Infra escalation contacts.
- https://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf - SLCM replaces AMS; attendance, marks, results, circulars; no helpdesk product named.
- https://helpdesk.manipal.edu.my/login.php - MUCM comparator with osTicket footer and Microsoft Work or School sign-in wording.
- https://www.jaipur.manipal.edu/administration-it.php - MUJ IT landscape page; Microsoft services, ERP, mixed in-house and outsourced support.
- https://urlscan.io/domain/mujslcm.jaipur.manipal.edu - SLCM scan records with IIS 10.0, AS8075 Microsoft, Azure DNS nameservers.
- https://www.onlinemanipal.com/help-center - Online Manipal help center with helpdesk@mujonline.edu.in and +91-7996 600 444.
- https://support.freshdesk.com/support/solutions/articles/37590-set-up-a-custom-portal-url-and-verify-dns - Freshdesk custom-URL capability; generic, not target evidence.

## ACTIONABLE LEADS
- Preserve cert IDs 23628924661 and 23628923708; poll crt.sh periodically for renewed certificates on the exact hostname.
- Re-run dns.google A and CNAME checks on a schedule to catch re-publication of the hostname.
- Review newly published official MUJ documents (FAQ, ICT lists, contact pages) for a direct helpdesk URL.
- Keep passive only: no login, no ticket creation, no endpoint enumeration, no origin discovery; MUJ IT policy governs information assets.
- Retain the hostname as an unresolved historical asset, not a confirmed vulnerability or ticketing platform.

## FLAGS
- Certificate existence proves CT logging only, not that a listener ever served traffic.
- NXDOMAIN at one resolver is a point-in-time observation, not proof of global DNS state or deletion cause.
- Freshdesk and Zendesk appear only as generic vendor capabilities; citing them as candidates is not target evidence.
- crt.sh exact query for mujslcm returned 404 (ref 23 in report); that is an unavailable result, not proof of absence.
- Common Crawl collection CC-MAIN-2026-18 was unavailable; it cannot count as evidence either way.
- Report is AI deep-research output; every claim needs independent verification before use.

## COVERAGE
Read 27,094 chars (204 lines), single pagination pass, EOF confirmed (truncated false).