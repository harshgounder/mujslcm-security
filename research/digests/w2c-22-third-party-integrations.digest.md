# Digest: w2c-22-third-party-integrations.md

## REPORT
Source: /home/liebert511/mujslcm-recon/research/w2c-22-third-party-integrations.md

## ANSWER SUMMARY
- Microsoft 365 identity confirmed at service level via official setup SOP; account provisioning source and direction remain Unknown.
- Apex TXT on jaipur.manipal.edu shows Microsoft verification strings, Cisco Webex verification strings, SPF includes for Outlook and Brightspace mail.
- NoPaperForms is the strongest third-party attribution: official admissions page routes to admissions.jaipur.manipal.edu, CNAME to jaipurmanipal.nopaperforms.com, then AWS load balancer.
- Brightspace relation proven by SPF include and CDOE-branded tenant page; residential-campus SLCM sync is Inference, not fact.
- D2L grade-sync capability (SIS-pull, push-export, permission-scoped grade APIs) documented; no MUJ flow confirmed.
- Webex TXT proves domain verification, not claiming, licenses, SSO, or directory sync.
- SLCM names return direct A records with no CNAME; Akamai claim not corroborated by public DNS.
- Verdict: multi-vendor ecosystem with ungoverned state transitions as the top risk; no vulnerabilities found.

## KEY FACTS
- https://mujslcm.jaipur.manipal.edu/ : institutional, parent, student login paths.
- https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf : official M365 setup flow, temporary password.
- https://dns.google/resolve?name=jaipur.manipal.edu&type=TXT : Microsoft, Cisco, Brightspace SPF and verification values.
- https://jaipur.manipal.edu/admissions.php : official admissions page, Track Application and Apply Now links.
- https://dns.google/resolve?name=admissions.jaipur.manipal.edu&type=CNAME : CNAME to jaipurmanipal.nopaperforms.com.
- https://dns.google/resolve?name=admissions.jaipur.manipal.edu&type=A : resolves to AWS load-balancer name.
- http://developer.nopaperforms.com/ : API areas and Secret Key/Access Key credential model.
- https://learning.onlinemanipal.com/d2l/home/14042 : MUJ CDOE Brightspace tenant page.
- https://community.d2l.com/brightspace/kb/articles/4825-ways-to-initiate-grades-export : push and pull grade export with initiator and failure records.
- https://docs.valence.desire2learn.com/res/grade.html : grade read and write scopes, 403 on missing permission.
- https://community.d2l.com/brightspace/kb/articles/23807-about-the-ipsis-platform : IPSIS SIS import mechanism.
- https://help.webex.com/en-us/article/cd6d84/Manage-Your-Domains : verification token in DNS, verified versus claimed states.
- https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=CNAME : no CNAME answer for main SLCM name.
- https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=A : direct A record, no Akamai CNAME naming.
- https://jaipur.manipal.edu/pay-fee-online.php : SLCM fee entry, SpaceBasic hostel/mess, bank transfer channels.

## ACTIONABLE LEADS
- Owner workshop demanding one redacted artifact per seam: Entra app list, IPSIS connections, Webex domain state, NoPaperForms field map, payment reconciliation.
- Audit SPF and verification TXT entries for stale artifacts; Cisco token may be removable after verification.
- Build applicant-to-student state machine: correlation IDs, duplicate detection, failure states, reconciliation across NoPaperForms, finance, SLCM, Entra.
- Webhook design review as hypothesis only: HMAC or asymmetric signatures, idempotency keys, replay windows, constant-time compare.
- Reconcile Akamai claim with property-manager evidence; do not publish edge findings without it.
- Identity lifecycle matrix: source of truth, creation event, role mapping, deprovisioning deadline per population.

## FLAGS
- Akamai attribution contradicted by current DNS shape (direct A, no CNAME); report says DNS alone does not exclude every Akamai config.
- No MUJ webhook endpoint identified anywhere; webhook risks are labeled review hypotheses.
- Temporary-password workflow implies admin account creation but is labeled Inference.
- NoPaperForms API key custody, accepted-student handoff, and retention are undocumented; Unknown, not negative findings.
- Brightspace campus sync, Webex sync, and grade return to SLCM are all Unconfirmed or Inference per the report's evidence classes.
- Report finds no public evidence of any exploit; the risk model is governance and state-transition integrity.

## COVERAGE
- Chars read: 45130. EOF confirmed via read_file truncated:false.