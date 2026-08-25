# Digest: w2b-05-helpdesk.md

## REPORT
Source: w2b-05-helpdesk.md (MUJ SLCM helpdesk OSINT assessment)

## ANSWER SUMMARY
- Ticketing vendor for helpdesk.jaipur.manipal.edu is unattributable from public evidence; Freshworks is visible on servicedesk.manipal.edu and osTicket on helpdesk.manipal.edu.my, both different domains.
- Google DoH returned Status 3 with no Answer for A, AAAA, and CNAME queries; resolver observation only, not proof of permanent decommissioning.
- Certificate-transparency shows exact certificates for the name: Entrust DV TLS Issuing RSA CA 2, valid 2026-01-08 through 2027-01-08, which conflicts with weak current DNS and archive visibility.
- urlscan reports the hostname as not observed; Wayback CDX query returned an empty array; public discovery footprint is very small.
- SLCM is separate and better observed: official onboarding guide names mujslcm.jaipur.manipal.edu as the Student Life Cycle Management portal, credentials sent to personal Gmail, technical issues routed to University Helpdesk or Admissions.
- urlscan for SLCM records HTTP 200, Microsoft-IIS/10.0, ASP.NET, and a Forgot Password? link to passwordreset.microsoftonline.com; older scan shows IIS/8.5 with different IP and ASN.
- No public ticket workflow, KB article, API, or attachment route evidenced on the target; Zendesk and Freshdesk docs are comparators only.
- User reports (not official records): invalid registration number after intra-sliding, and password error despite believed-correct password.

## KEY FACTS
- https://urlscan.io/domain/helpdesk.jaipur.manipal.edu - no direct hits, nothing hosted, no incoming hits, nothing talked to the domain.
- https://dns.google/resolve?name=helpdesk.jaipur.manipal.edu&type=A - Status 3, no Answer section.
- https://dns.google/resolve?name=helpdesk.jaipur.manipal.edu&type=AAAA - Status 3, no Answer section.
- https://dns.google/resolve?name=helpdesk.jaipur.manipal.edu&type=CNAME - Status 3, no Answer section.
- https://crt.sh/?q=%25.jaipur.manipal.edu&output=json - exact helpdesk name in CT records; Entrust issuer, 2026-01-08 to 2027-01-08 validity.
- https://web.archive.org/cdx/search/cdx?url=helpdesk.jaipur.manipal.edu/*&output=json&filter=statuscode:200 - empty array, no matching 200 captures.
- https://servicedesk.manipal.edu/support/tickets/new - Freshworks visible, but a different Manipal hostname.
- https://helpdesk.manipal.edu.my/ - MUCM Helpdesk, powered by osTicket, separate domain.
- https://mujslcm.jaipur.manipal.edu/ - SLCM public surface; Sign In, Parent Login, Student Login, Forgot Password?, @muj.manipal.edu.
- https://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf - official guide; SLCM URL, one-stop academic platform, Gmail credential delivery, helpdesk/admissions escalation path.
- https://urlscan.io/result/019ed038-c4af-765c-9499-2da69a77e30a/ - SLCM scan; IIS/10.0, ASP.NET, Microsoft password-reset link, IP 98.70.14.50 AS8075.
- https://www.jaipur.manipal.edu/contact-university.php - official IT support contact it.support@jaipur.manipal.edu, extensions 778 and 300.
- https://www.onlinemanipal.com/help-center - online-program help center; helpdesk@mujonline.edu.in, +91-7996 600 444; enrolled-learner context.
- https://www.reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue - user-reported SLCM password error.
- https://www.reddit.com/r/Manipal_Academics/comments/1993mdc/slcm_login - user-reported invalid registration number after intra-sliding.
- https://developers.google.com/speed/public-dns/docs/doh/json - DoH docs; the excerpt defines Status 0 and 2 but not value 3, so the report avoids overstating NXDOMAIN.

## ACTIONABLE LEADS
- Re-run DNS checks periodically; Status 3 may reflect temporary record state, split DNS, or retirement.
- Query CT logs for other jaipur.manipal.edu subdomains to find candidate helpdesk aliases or vendor domains.
- Watch crt.sh for certificate renewal on the name; renewal timing indicates lifecycle intent.
- Use official channels (it.support@jaipur.manipal.edu) to ask the owner which ticketing product serves MUJ.
- Do not test Zendesk, Freshdesk, or osTicket routes against the target; vendor docs are comparators only.

## FLAGS
- Contradiction preserved: valid 2026-2027 certificate vs no current DNS answer; explanation (migration, retirement, split DNS) unknown.
- DoH Status 3 meaning is not defined in the cited documentation excerpt; treated as "unresolved at observation point".
- SLCM IIS/ASP.NET evidence must not be transferred to the helpdesk hostname.
- Scribd reference (SLcM MIT user manual) belongs to another Manipal SLCM context, unrelated to the MUJ target.
- urlscan "not observed" is a coverage statement, not proof of nonexistence.

## COVERAGE
Chars read: 30,166. EOF confirmed: true.