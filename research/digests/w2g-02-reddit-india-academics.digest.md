# Digest: w2g-02-reddit-india-academics.md

## REPORT
Source file: w2g-02-reddit-india-academics.md (Reddit OSINT Findings for the MUJ SLCM Ecosystem)

## ANSWER SUMMARY
- No confirmed MUJ SLCM incident was located in r/Indian_Academia or r/developersIndia; the negative result is bounded to the reviewed index.
- Manipal posts in both communities are mostly education-choice discussions (VIT vs Manipal 2021, DU vs Manipal 2026, Online BCA from MUJ).
- One out-of-scope MUJ SLCM password complaint was found in r/manipaljaipur: password rejected despite the poster believing it correct.
- The most technical item is the IITK B.Cyber Pingala report: client-side CAPTCHA and per-browser OTP limit, reported and allegedly patched with server-side validation and rate limits.
- Generic Indian education portals show recurring themes: failed logins, upload errors, an HTML-as-JSON error, Aadhaar already registered, and spam-call privacy concerns.
- The Pingala case transfers as a defensive lesson: a client-visible control must not be the sole enforcement point.
- No Reddit item in scope maps to a specific MUJ component; treat the corpus as risk themes, not findings.

## KEY FACTS
1. https://www.reddit.com/r/manipaljaipur/comments/1m6lwf2/slcm_portal_issue - out-of-scope MUJ SLCM login complaint, password rejected.
2. https://www.reddit.com/r/developersIndia/comments/1ug3qpw/ironically_the_iitk_bcyber_application_portal/ - Pingala CAPTCHA/OTP disclosure and claimed remediation.
3. https://www.reddit.com/r/Indian_Academia/comments/ny1o91/ysk_factors_to_take_into_account_while_choosing/ - 2021 VIT vs Manipal comparison, education choice only.
4. https://www.reddit.com/r/Indian_Academia/comments/1u1osy9/manipal_online_scammed_me_and_refused_to_refund/ - Manipal Online refund complaint; consumer service, not portal security.
5. https://www.reddit.com/r/developersIndia/comments/1ut6xh8/need_advice_regarding_online_manipal_university/ - Online BCA from Manipal University Jaipur discussion.
6. https://www.reddit.com/r/Indian_Academia/comments/1q2l1f9/unable_to_candidate_login_to_download_admit_card/ - UGC NET candidate login failure with password reset loop.
7. https://www.reddit.com/r/Indian_Academia/comments/1ub0ira/pmrc_portal_is_full_of_bugs_and_does_not_work_help/ - PMRC upload error returning HTML where JSON was expected.
8. https://www.reddit.com/r/Indian_Academia/comments/1npirgk/nats_portal_aadhaar_misuse_blocking_my_drdo/ - Aadhaar already registered on NATS, blocked a DRDO internship.
9. https://www.reddit.com/r/Indian_Academia/comments/1ocym4m/vidyalaxmi_portal_doesnt_have_my_institute_listed/ - PM Vidyalaxmi form coverage gap.
10. https://www.reddit.com/r/Indian_Academia/comments/1crm5bh/swayam_portal_nta_hall_ticket_download/ - Swayam/NTA navigation failure report.
11. https://www.reddit.com/r/developersIndia/comments/1cv6qy3/built_this_result_portal_for_my_university/ - result portal architecture context (ASP.NET Core, Dapper, PostgreSQL, 50k+ PDF pages).
12. https://www.reddit.com/r/developersIndia/comments/1m4qbhe/is_tcs_candstatus_inspect_portal_code_trick_true/ - TCS portal status-code inspection thread, excluded as recruitment context.
13. https://www.reddit.com/r/Indian_Academia/search.rss?q=SLCM&restrict_sr=1&sort=relevance&t=all - SLCM search feed in the requested subreddit, no result.
14. https://www.reddit.com/r/developersIndia/search.json?q=SLCM&restrict_sr=1&sort=relevance&t=all&raw_json=1 - SLCM search in developersIndia, no relevant result.
15. https://www.reddit.com/r/Indian_Academia/comments/1t2e3jg/spent_hours_just_trying_to_get_my_photo_and/ - government exam portal timeout and signature "too large" complaint.

## ACTIONABLE LEADS
- Record the r/manipaljaipur login complaint as an out-of-scope UX lead for MUJ support and provisioning review.
- Use the Pingala case as a cross-portal study for server-side CAPTCHA and OTP enforcement, rate limits, and telemetry.
- Review reset token expiry, account-state leaks in error messages, and server-side rate limits.
- Review upload workflows: content types, size bounds, file-type validation, malware scanning, and non-sensitive errors.
- Treat the Aadhaar reuse case as an identity-binding lesson for dispute, unlink, and re-verification paths; never test on MUJ without authorization.
- Do not label MUJ SLCM vulnerable on the basis of generic portal themes.

## FLAGS
- The Pingala before/after states are user-reported; no independent validation exists in the corpus.
- The negative search result is index-limited, not proof of absence.
- One reference (ref 39) pairs a deleted-comment title labeled r/HairyAssGirls with an r/Indian_Academia URL; treat the reference list as noisy.
- "Manipal Online scammed me" is a consumer complaint, not security evidence.
- The TCS thread was intentionally excluded; do not count it as university evidence.

## COVERAGE
Chars read: 35311. EOF confirmed: yes (truncation flag false on full read).