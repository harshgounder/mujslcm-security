# Digest: w3-12-npfslcm.md

## REPORT
Source file: w3-12-npfslcm.md (MUJ SLCM and NoPaperForms evidence-bounded risk map)

## ANSWER SUMMARY
- CT shows npfslcm.jaipur.manipal.edu as certificate name_value on a record whose common name is mujslcm.jaipur.manipal.edu, Entrust OV CA, validity 2025-03-07 to 2025-12-22, logged 2025-11-16.
- admissions.jaipur.manipal.edu CNAMEs to jaipurmanipal.nopaperforms.com, which resolves through prodvpc-web-lb4-593721465.ap-south-1.elb.amazonaws.com to 65.1.79.226, 13.206.4.210, 65.0.244.41.
- SLCM = Student Life Cycle Management per MUJ ICT list; it replaced the older Academic Management System.
- "npf means NoPaperForms" is a medium-confidence inference. No MUJ or vendor source explicitly confirms the acronym.
- NoPaperForms rebranded its flagship product to Meritto on 2023-06-26; older OSINT sources use the old name.
- No credible first-hand public complaint ties a MUJ admissions failure to NoPaperForms. Reviews are mostly positive: G2 4.8/5 (21 reviews), Meritto G2 4.8/5 (20), Software Advice 4.6 (619).
- Public evidence does not prove a direct admissions-to-SLCM data pipeline, database sharing, Microsoft 365 federation, or Akamai in front.

## KEY FACTS
- https://crt.sh/?q=npfslcm.jaipur.manipal.edu&output=json - exact CT records: npfslcm as name_value, mujslcm as common name.
- https://dns.google/resolve?name=admissions.jaipur.manipal.edu&type=CNAME - direct CNAME to jaipurmanipal.nopaperforms.com, TTL 2387.
- https://dns.google/resolve?name=admissions.jaipur.manipal.edu&type=A - resolver chain to AWS ELB hostname and three IPv4s.
- https://www.ipaddress.com/website/admissions.jaipur.manipal.edu - independent DNS lookup page reporting the same CNAME target.
- https://urlscan.io/domain/admissions.jaipur.manipal.edu - domain first observed six years prior, Mumbai GeoIP, Amazon AS16509.
- http://compliance.manipal.edu/wp-content/uploads/2023/naac/Criteria-2/2_3_3-List_of_ICT_tools-2023-Edited.pdf - defines SLCM and its academic modules.
- https://mujslcm.jaipur.manipal.edu/ - login boundary with @muj.manipal.edu identity domain; no SSO protocol visible.
- http://api.ssllabs.com/api/v3/analyze?all=done&fromCache=on&host=mujslcm.jaipur.manipal.edu&maxAge=168 - point-in-time scan showing Microsoft-IIS/10.0 and ASP.NET MVC 5.3.
- http://developer.nopaperforms.com/ - vendor API docs: Lead, Opportunity, Activity, Form, Master Data, Payment, Application areas.
- https://www.meritto.com/application-automation/admission-form-payment-manager - vendor payment claims including split payment and CSV export.
- https://www.nopaperforms.com/press-release/nopaperforms-rebrands-its-flagship-product-to-meritto-signifying-expanding-platform-and-markets - documents the June 2023 rebrand.
- https://login.nopaperforms.io/privacy-policy - vendor collection statement; no MUJ-specific admissions privacy notice exists in reviewed pages.
- https://www.g2.com/products/meritto/reviews - 4.8/5 from 20 reviews with usability and reporting criticisms.
- https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/Subdomain_takeover - MDN CNAME deprovisioning guidance behind the monitoring recommendation.

## ACTIONABLE LEADS
- Set up CT and DNS monitoring: watch for npfslcm re-issuance and for drift of the admissions CNAME target.
- Request from the owner a sanctioned data-flow diagram: fields, controller and processor roles, retention, payment tokenization, SSO protocol.
- Build a passive asset register; do not test credentials, enumerate endpoints, or attempt any takeover.
- Watch the rebrand split: search both NoPaperForms and Meritto names when correlating historical records.
- Do not claim subdomain takeover: the CNAME chain currently resolves through a live-looking path.

## FLAGS
- Hudson Rock ref (11486 infostealer credentials for nopaperforms.com) sits in references but is never analyzed in the body; treat as unverified third-party claim.
- Two shodan.io host links (98.70.14.50, 20.244.94.89) appear malformed in references with no body discussion; exclude as evidence.
- One reference is a goo.gl redirect URL (Google Lens link); junk, ignore.
- CT record entered 2025-11-16 with validity starting 2025-03-07 is an unusual backdated window; do not infer issuance date from validity start.
- The admissions CNAME proves DNS routing, not data flow, contract, or database ownership.
- Microsoft 365 as SLCM identity provider is not established; the supplied premise is unverified.
- Report is AI deep-research output; all claims need independent verification.

## COVERAGE
Read 42,098 chars (351 lines), single pagination pass, EOF confirmed (truncated false).