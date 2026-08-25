# Digest: w2g-05-youtube-tutorials

## REPORT
Source file: w2g-05-youtube-tutorials.md (MUJ SLCM Public-Video OSINT Report)

## ANSWER SUMMARY
- The only clearly MUJ-SLCM-specific walkthrough located is a Facebook video by JS Group of Institutions: 1:42 duration, 142 views, dated Oct 7 2021. Metadata is confirmed; no transcript or screen inventory.
- A YouTube video (9R1mCmnhD6Y, 10:39, published Sep 5 2025, creator "dear dashu") describes a MUJ student portal and LMS walkthrough but was unavailable to the extractor; SLCM identity and screen content unverified.
- No verified MUJ-specific YouTube fee-payment, timetable, or developer-tools/network-traffic video exists in this pass; a bounded negative, not proof of absence.
- The official fee page states existing-student online payment uses https://mujslcm.jaipur.manipal.edu/ and that hostel and mess fees are paid via the SpaceBasic app.
- The official MUJ YouTube channel shows institutional and programme content only; no SLCM or portal tutorials visible in the extracted listing.
- Third-party how-to material exists (slcm.vercel.app attendance guide, MUJStella) but is expressly non-affiliated with MUJ.
- The SLCM-api repository targets slcm.manipal.edu, not mujslcm.jaipur.manipal.edu; not evidence about the MUJ host.
- Stack assertions (MVC 5.3, .NET 4.x, IIS 10, Akamai, M365) are unverified; the Microsoft identity link is only an inference from domain and federation context.

## KEY FACTS
1. https://www.facebook.com/watch/?v=3067261673486711 - MUJ-SLCM Student Portal Walkthrough, JS Group, 1:42, 142 views, Oct 7 2021.
2. https://www.youtube.com/watch?v=9R1mCmnhD6Y - MUJ student portal/LMS explainer, 10:39, Sep 5 2025; unavailable to extractor.
3. https://www.youtube.com/channel/UCFbeX4UJyd4fHTCnCVGob_Q - official MUJ YouTube channel; no tutorial listings visible.
4. https://jaipur.manipal.edu/pay-fee-online.php - fee page; SLCM URL for existing students, SpaceBasic for hostel/mess.
5. https://mujslcm.jaipur.manipal.edu/Home/Index - portal landing with MUJ PORTAL labels and @muj.manipal.edu wording.
6. https://www.jaipur.manipal.edu/time-table.php - official timetable page; no SLCM navigation tutorial extracted.
7. https://slcm.vercel.app/guides/check-attendance-muj - betterSLCM third-party attendance guide, not university-owned.
8. https://mujstella.in/ - independent student platform, expressly not affiliated.
9. https://github.com/nikeplusdash/SLCM-api - API project for slcm.manipal.edu; separate host from MUJ.
10. https://www.manipal.edu/mu/academics/student-portal.html - MAHE student portal page pointing to sis.manipal.edu; separate service label.
11. https://www.nuget.org/packages/Microsoft.AspNet.Mvc - generic package page; not host-specific MUJ evidence.
12. http://login.microsoftonline.com/getuserrealm.srf?login=probe@muj.manipal.edu&xml=1 - federation-related realm response; inference only.
13. https://www.youtube.com/watch?v=1v0QXkIpkGo - Trent University timetable walkthrough; excluded false positive.
14. https://www.reddit.com/r/manipaljaipur/comments/1uaqh0g/muj_fee_deadline - unrelated fee-deadline discussion; not a payment walkthrough.
15. https://jaipur.manipal.edu/ - MUJ main site; institutional context.

## ACTIONABLE LEADS
- Review the Facebook walkthrough manually in an ordinary browser; catalog visible screens without logging in or reproducing personal data.
- Search title variants, course and department terms, Hindi phrasing, and academic-year posts for the missing tutorial types.
- Record access dates, URLs, titles, and hashes where lawful for both videos; metadata may change.
- Use the official MUJ channel as a provenance control; do not treat third-party videos as official productions.
- If a developer-tools or network-traffic video surfaces, do not replay captured requests, tokens, or identifiers.
- Monitor the fee page for payment-channel changes between SLCM and SpaceBasic.

## FLAGS
- Facebook video evidence is title and metadata only; no transcript, so screen-level claims would be inference.
- The YouTube video was unavailable to the extractor; description claims are unverified.
- The getuserrealm lookup is an indexed probe result; it supports an enterprise identity inference, not proof of the SLCM login flow.
- The Trent University video is an excluded false positive; name collisions are a recurring risk in this topic.
- Views, durations, and dates are snapshot values and may change.
- The SpaceBasic statement comes from fee-page text; the app itself was not assessed.

## COVERAGE
- Chars read: 29,140
- EOF confirmed: yes (truncated: false on final page, 187 of 187 lines)