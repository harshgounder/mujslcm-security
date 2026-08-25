# Digest: w3-01-exam-jaipur.md

## REPORT
Source file: /home/liebert511/mujslcm-recon/research/w3-01-exam-jaipur.md (AI deep-research output, claims UNVERIFIED). Topic: public evidence on `exam.jaipur.manipal.edu` in the MUJ SLCM ecosystem. Research cutoff 2026-08-25, passive non-authenticated collection.

## ANSWER SUMMARY
- Exam host network placement is the only high-confidence finding: `59.91.192.229` in `59.91.192.0/20`, AS9829, BSNL/National Internet Backbone, corroborated by Hurricane Electric, IPinfo, and Netcraft.
- No reviewed MUJ official source names `exam.jaipur.manipal.edu` or assigns any function to it; exam forms, hall tickets, results, and credentials are unverified hypotheses.
- Tension with supplied baseline: passive data puts `mujslcm.jaipur.manipal.edu` at `98.70.14.50` in Microsoft AS8075 (first seen July 2022), not Akamai; do not inherit the Akamai/ASP.NET MVC assumption.
- Credential reuse with SLCM is unverified; the SLCM FAQ ties the SLCM password to the official Outlook ID, but no document says the exam host accepts SLCM credentials.
- Public footprint is sparse: URLScan zero results, Shodan no IP record, Netcraft tech blank, Wayback CDX for the exact host returned an empty array.
- Governance is documented: Controller of Examinations, Deputy CoE, exam helpdesk and store emails, plus `it.support@jaipur.manipal.edu`; responsible disclosure should route there.
- One Reddit anecdote (SLCM password rejected) is a single unresolved support-friction case, not exam-host outage evidence.
- Verdict is Medium confidence; defensible line: low-visibility MUJ-domain asset on NIB with unknown purpose, stack, and login flow.

## KEY FACTS
- https://bgp.he.net/ip/59.91.192.229 - HE maps the IP into 59.91.192.0/20, AS9829, BSNL; core of the NIB claim.
- https://sitereport.netcraft.com/?url=http://exam.jaipur.manipal.edu - Netcraft: host to 59.91.192.229, AS9829, NIB owner; title/tech/first-seen blank; labels site non-HTTPS.
- https://ipinfo.io/59.91.192.229 - IPinfo: AS9829 NIB; geolocation Hoshiarpur, which conflicts with URLScan's Dehradun label.
- https://urlscan.io/api/v1/search/?q=domain:exam.jaipur.manipal.edu - zero scan results for the exact host.
- https://urlscan.io/domain/exam.jaipur.manipal.edu - domain summary associates host with 59.91.192.229/AS9829, no hits.
- https://www.shodan.io/host/59.91.192.229 - Shodan: no information available for the IP.
- https://jaipur.manipal.edu/examination.php - official MUJ exam page; CoE names, `exam.helpdesk@jaipur.manipal.edu`, `exam.store@jaipur.manipal.edu`.
- https://jaipur.manipal.edu/contact-university.php - MUJ campus identity, Dehmi Kalan, main phone +91 141-3999100.
- https://mujslcm.jaipur.manipal.edu/Home/Index - SLCM landing: MUJ portal, `@muj.manipal.edu`, student and parent login.
- https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - SLCM FAQ: username pattern, password "as per official outlook ID", `it.support@jaipur.manipal.edu`.
- https://jaipur.manipal.edu/img/pdf/First-Year-Students-Profile-Registration-Guide.pdf - Admissions sends SLCM credentials to personal Gmail; names the SLCM URL, never the exam host.
- https://jaipur.manipal.edu/img/pdf/exam/3.%20Manual%20Exam%20Process.pdf - exam manual: CoE decentralization, 15-day result declaration; no exam-host URL.
- https://jaipur.manipal.edu/img/pdf/exam/Student%20Examination%20Handbook%202023-24%20%2811.08.2023%29.pdf - hall ticket required as ID but download venue not stated.
- https://sitereport.netcraft.com/?url=https://mujslcm.jaipur.manipal.edu - SLCM passive report: AS8075 Microsoft, first seen July 2022, tech still loading.
- http://reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue - only directly relevant complaint: SLCM password rejected, no visible resolution.

## ACTIONABLE LEADS
- Re-run passive checks (URLScan, Shodan, Wayback CDX, Netcraft) later to detect change in the exam-host record.
- Confirm purpose, owner, and retirement status with MUJ Examination and IT via `exam.helpdesk@jaipur.manipal.edu` and `it.support@jaipur.manipal.edu`.
- Validate the supplied SLCM baseline from owner-side DNS and edge inventories; never carry Akamai/IIS claims onto the exam host.
- Have MUJ confirm TLS and HTTPS posture; Netcraft's non-HTTPS label does not prove TCP/443 closed.
- In club output, label any claim that the host serves forms, hall tickets, or results as unverified inference.

## FLAGS
- Contradiction: supplied Akamai SLCM baseline versus passive AS8075 Microsoft address; report says unresolved architecture question.
- Contradiction: IPinfo Hoshiarpur versus URLScan Dehradun geolocation; only country and network ownership are safe to state.
- Unverified: exam-host purpose, technology, login flow, HTTPS state, and any SLCM credential bridge; no first-party source names the host.
- Negative results (empty URLScan, Shodan, Wayback CDX, blank Netcraft fields) prove absent indexed evidence, not an absent service.
- Anecdote is single-user, SLCM-targeted, unresolved; not exam-host evidence.
- Hall-ticket and exam-document findings never mention the hostname; converting business artifacts into host claims is the flagged OSINT failure mode.
- References 8, 9, and 17 appear as bare URL lines; claims tied to them lean on unverified AI output.

## COVERAGE
37,148 chars read on disk (wc -m), 279/279 lines, single read pass, final page returned truncated=false, EOF confirmed; file_size 37149 bytes; digests dir exists.