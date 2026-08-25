# Digest: w2g-04-twitter-x

## REPORT
Source file: w2g-04-twitter-x.md (MUJ SLCM Public-Source OSINT Report: Evidence, Gaps, and Risk Signals)

## ANSWER SUMMARY
- Direct X search pages for mujslcm, slcm.manipal, Manipal portal, and MUJ portal returned only an auth/cookie/navigation shell with no visible tweet cards; a coverage-limited negative, not proof posts do not exist.
- Four @Jaipur_Manipal post URLs were found dated Aug 15, 18, 21, 24 2026; all concern campus events or a secure-cloud training, none is an SLCM outage or security report.
- The official MUJ FAQ names https://mujslcm.jaipur.manipal.edu/ as the SLCM registration link and gives dms@jaipur.manipal.edu and ams@jaipur.manipal.edu for login trouble; the strongest attribution source in the report.
- Two public complaints exist: password rejected despite the user believing it correct (r/manipaljaipur) and fee paid but still marked pending (r/Manipal_Academics); both show relative dates "1y ago" and no resolution.
- Extension ecosystem: SLCM Feedback Auto-Fill requests access to all websites; Detain Shield claims MUJ-only attendance use. Both are publisher disclosures, not audits.
- Publicly indexed academic artifacts (2025 grade sheet, BTech transcript on Scribd) are provenance concerns, not proof of breach; preserve URLs, do not redistribute.
- Unofficial projects (muj_slcm repo, SLCM-api, MUJStella, Arcadia) must be kept separate from official assets in any asset register.
- The supplied stack (MVC 5.3, .NET 4.x, IIS 10, Akamai, M365) was not independently confirmed by this public-source pass.

## KEY FACTS
1. https://mujslcm.jaipur.manipal.edu/ - target portal, "WELCOME TO MUJ PORTAL" branding.
2. https://muj.slcm.jaipur.manipal.edu/ - alternate hostname displaying @jaipur.manipal.edu identity label.
3. https://jaipur.manipal.edu/img/pdf/FaQs-SLCM.pdf - official SLCM FAQ; registration link and support contacts.
4. https://x.com/Jaipur_Manipal/status/2091866801852613107 - Aug 24 2026 Azure secure-cloud training post; closest security-adjacent item, not a portal incident.
5. https://x.com/Jaipur_Manipal/status/2088634410635759649 - Aug 15 2026 Independence Day post; provenance only.
6. https://x.com/Jaipur_Manipal/status/2089600565877821835 - Aug 18 2026 IAESTE culinary workshop post.
7. https://x.com/Jaipur_Manipal/status/2090688741627285837 - Aug 21 2026 Pitch Fest post.
8. https://www.reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue - public login complaint, no verified root cause.
9. https://www.reddit.com/r/Manipal_Academics/comments/1lzf0ht/paid_my_fees_but_still_showing_as_pending_on_slcm - fee-status sync complaint, no resolution shown.
10. https://addons.mozilla.org/en-US/firefox/addon/slcm-feedback-auto-fill/ - extension automating feedback forms; broad all-websites permission.
11. https://chromewebstore.google.com/detail/detain-shield/mjedocjcijmphjgbfnkpceiblklpalpp - extension scoped to MUJ SLCM attendance claims.
12. https://www.scribd.com/document/983177245/Https-Mujslcm-jaipur-manipal-edustudentAcademicGradesForStudent - 2025 grade sheet artifact with SLCM-derived path in title.
13. https://github.com/Anushkakumar10/muj_slcm - repo created Jul 13 2025, zero stars, one commit, no affiliation claim.
14. https://mujstella.in/ - independent platform, expressly not affiliated with MUJ.
15. https://muj.onlinemanipal.com/notifications - official notices page; dated notices with no outage or security incident text.

## ACTIONABLE LEADS
- Monitor @Jaipur_Manipal with date-stamped records for future SLCM outage or security mentions.
- Report the Scribd artifact URLs and data categories to MUJ via dms@ or ams@; do not download, mirror, or enumerate more records.
- Treat both extensions as a trust boundary; review publisher, permissions, update history before any use on university accounts.
- Next pass should capture canonical Reddit timestamps; "1y ago" must not be converted to invented dates.
- Clarify with the owner whether mujslcm.jaipur.manipal.edu and muj.slcm.jaipur.manipal.edu are aliases or separate deployments.
- Watch unofficial projects (muj_slcm, SLCM-api, MUJStella, Arcadia) for credential handling; no testing.

## FLAGS
- X search pages showed no tweet content; any "there are no posts" statement would be unsupported.
- "1y ago" relative dates on both Reddit pages; exact dates not established.
- Scribd artifacts: how they became indexed is unknown; could be user upload, misconfiguration, or unrelated posting.
- Extension permissions and data claims are publisher disclosures, not independent audits.
- MUJStella and Arcadia are explicitly non-affiliated; do not attribute their behavior to MUJ.
- The Aug 24 training post mentions Azure security; institutional training language is not evidence of production architecture.

## COVERAGE
- Chars read: 32,908
- EOF confirmed: yes (truncated: false on final page, 229 of 229 lines)