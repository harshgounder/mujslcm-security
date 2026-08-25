# Digest: w2b-01-muj-slcm-alt.md

## REPORT
Source: w2b-01-muj-slcm-alt.md (MUJ SLCM Alternate Host OSINT Assessment)

## ANSWER SUMMARY
- Alternate host muj.slcm.jaipur.manipal.edu is a MUJ-branded SLCM-family login endpoint, same visible portal family as the primary; nothing proves dev, staging, backend, or origin role.
- A record observed: 20.244.94.89, TTL 3600; RIPEstat, ARIN, and IPinfo all attribute it to AS8075 Microsoft, prefix 20.192.0.0/10, Pune geolocation.
- Primary mujslcm.jaipur.manipal.edu resolves 98.70.14.50 in the same snapshots, also AS8075 but prefix 98.70.0.0/15.
- Official SLCM FAQ names only the primary hostname as the registration link; the alternate is not mentioned in the visible FAQ extract.
- HTML similarity (Keen theme assets, "User login example" description, Microsoft password-reset destination, EmailFor/LoginFor fields) supports a shared application family, not a shared backend or database.
- URLScan coverage asymmetry: public API search for the alternate returns zero results; the primary has a public scan record identifying 98.70.14.50.
- Email-domain text differs between pages: alternate shows @jaipur.manipal.edu, primary shows @muj.manipal.edu; report treats this as configuration or role difference, not proof of separate apps.
- The brief's "Akamai-fronted" claim was not independently verified by this pass; no target-specific Akamai DNS, header, or authoritative statement was recovered.

## KEY FACTS
- https://muj.slcm.jaipur.manipal.edu/ - alternate host; "WELCOME TO MUJ PORTAL" sign-in page, @jaipur.manipal.edu context.
- https://mujslcm.jaipur.manipal.edu/Home/Index - primary page capture; same branding and parent/student sign-in labels.
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - official FAQ; only primary URL named as SLCM registration link, AMS support, dms@ and ams@ contacts.
- https://dns.google/resolve?name=muj.slcm.jaipur.manipal.edu&type=A - observed A record 20.244.94.89.
- https://dns.google/resolve?name=mujslcm.jaipur.manipal.edu&type=A - observed A record 98.70.14.50.
- https://stat.ripe.net/data/network-info/data.json?resource=20.244.94.89 - RIPEstat maps address to AS8075, prefix 20.192.0.0/10.
- https://ipinfo.io/20.244.94.89/json - IPinfo labels AS8075 Microsoft Corporation, Pune, Maharashtra geolocation.
- https://whois.arin.net/rest/ip/20.244.94.89 - ARIN record for range 20.192.0.0/10, name MSFT, handle NET-20-192-0-0-1.
- https://urlscan.io/api/v1/search/?q=domain:muj.slcm.jaipur.manipal.edu - zero public scan results for the alternate.
- https://urlscan.io/result/019ed038-c4af-765c-9499-2da69a77e30a/ - primary public scan record identifying 98.70.14.50.
- http://mujslcm.jaipur.manipal.edu/ - primary capture showing ASP.NET-style request-verification field and EmailFor, LoginFor, UserName, Password inputs.
- https://jaipur.manipal.edu/img/pdf/Help%20document_SOP-Office-365-and-Outlook-EMail-id.pdf - MUJ M365 SOP v1.0 June 2025; mandatory MFA context, not SLCM topology.
- https://github.com/vikrant500/college_portal_web_and_dbms/tree/main/mujslcm.jaipur.manipal.edu_122 - third-party saved directory named after primary host with Home/Scripts/Keen assets; provenance unverified.
- http://github.com/Anushkakumar10/muj_slcm - third-party repo, single commit, README/requirements.txt; unverified reference.
- https://dns.google/resolve?name=muj.slcm.jaipur.manipal.edu&type=CNAME - no CNAME answer in queried snapshot.

## ACTIONABLE LEADS
- Compare server-returned HTML of both hosts across login paths (student, parent) in a passive pass to find divergence or identity-tenant hints.
- Check certificate transparency and TLS SANs for both names to test same-certificate binding.
- Ask MUJ IT to confirm what 20.244.94.89 is (App Service, VM, gateway, or shared address) and whether the alternate is production, migration, staging, or retired.
- Add both hostnames to the club asset inventory with role marked "unconfirmed"; document the canonical URL per the FAQ.
- Disclosure step: submit an asset-relationship report to MUJ with exact URLs, DNS snapshots, and timestamps; no credential or access tests.

## FLAGS
- "Akamai-fronted" for the primary is an unverified input from the brief; report explicitly declines to assert it.
- Classifying the alternate as dev/staging/backend bypasses is unsupported; report itself rejects those labels.
- GitHub directories from vikrant500 and Anushkakumar10 may be scraped content; not official MUJ repositories.
- Zero URLScan results for the alternate is a coverage difference, not proof the host is private or unused.
- Email-domain difference is ambiguous; report warns against overinterpretation.
- No vulnerability established anywhere in this report.

## COVERAGE
Chars read: 26,232. EOF confirmed: true.