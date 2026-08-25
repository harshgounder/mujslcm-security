# Digest: w2d-08-placement-data.md

## REPORT
Source file: w2d-08-placement-data.md (MUJ Placement Data and SLCM Public-Surface Assessment)

## ANSWER SUMMARY
- MUJ runs a public Directorate of Corporate Relations and Placements surface: overview, process, statistics, top recruiters, recruiter contact, and T&P team pages; recruiter-facing, not a student placement dashboard.
- The official statistics page states paid internship stipends range from INR 15,000 to INR 1,25,000 per month, but attaches no cohort, year, sample size, or methodology.
- The NIRF 2025 institution PDF (IR-O-U-0749) is the most traceable dataset: 2023-24 median salaries of INR 5,25,000 (three-year UG), INR 7,50,000 (four-year UG), INR 5,75,000 (five-year UG), INR 5,35,000 (one-year PG), and INR 6,00,000 (two-year PG), with placed-student counts per line.
- Careers360 reports 2025 headline figures (64 LPA engineering highest, 8.2 LPA engineering average, 7.6 LPA overall average, 94% placement rate, 2,100+ total offers, 1,663 unique offers); these must stay source-labelled and separate from NIRF medians.
- Third-party figures conflict: Collegedunia shows INR 88 lakhs highest while a 2022 student review on the same page reports INR 16 lakhs highest; FreeJobAlert shows INR 85 LPA highest; do not merge.
- The SLCM landing page shows student and parent sign-in with the @muj.manipal.edu label but no placement reference; placement authentication status is undetermined.
- The placement process names Placement Registration as a stage but never identifies the system; visible Apply Now and Track Application links point to the admissions domain.
- "Brochure" and "Get Placement Report" labels appear on the statistics page without any downloadable URL; leads only.

## KEY FACTS
- https://jaipur.manipal.edu/placement.php - Directorate overview and advisory scope
- https://jaipur.manipal.edu/placement-inernship.php - nine-stage process and three internship durations
- https://jaipur.manipal.edu/placement-statistics.php - stipend range and brochure or report labels
- https://jaipur.manipal.edu/placement-team-training.php - T&P team and Director Dr Sandeep Chaurasia contacts
- https://jaipur.manipal.edu/placement-contact-us.php - recruiter contact surface
- https://jaipur.manipal.edu/contact-university.php - T&P extension 751 and tpo@jaipur.manipal.edu
- https://www.nirfindia.org/nirfpdfcdn/2025/pdf/University/IR-O-U-0749.pdf - primary structured placement and median salary evidence
- https://www.careers360.com/university/manipal-university-jaipur/placement - 2025 headline statistic set
- https://collegedunia.com/college/57229-manipal-university-school-of-business-and-commerce-sbc-jaipur/placement - conflicting highest and average figures
- https://colleges.freejobalert.com/colleges/manipal-university-jaipur/placements - different latest-cycle headline set (85 LPA)
- https://www.collegedekho.com/colleges/manipal-university-placement - Udupi Manipal page, not MUJ Jaipur
- https://mujslcm.jaipur.manipal.edu/ - public login surface with no placement reference
- https://mujalumni.in/ - alumni platform described separately from T&P and SLCM
- https://jaipur.manipal.edu/nirf-home.php - NIRF index page
- https://jaipur.manipal.edu/mandatory-disclosure.php - reviewed extract shows no placement PDF link

## ACTIONABLE LEADS
- Ask T&P (tpo@jaipur.manipal.edu) for the canonical placement report or brochure URL instead of guessing filenames or probing directories.
- Archive the NIRF PDF with URL and hash as the primary placement document.
- Enforce an evidence register with source_type, reporting_year, programme_scope, metric_type, value, qualifier, and confidence fields.
- Track the discrepancy between Careers360 2025 headlines and FreeJobAlert's different cycle; reconcile with the official site when published.
- Check the admissions application flow for placement registration references (passive; it is not T&P authentication evidence).
- Authorized session testing only: determine whether Placement Registration lives inside SLCM, and whether placement uses the SLCM account.
- Include campus identity checks (city and institution match) for every collected figure.

## FLAGS
- NIRF median salary is not average package; total offers (2,100+) are not unique offers (1,663) and not placed students.
- Collegedunia figures are scoped to the School of Business and Commerce; scope loss is a stated risk.
- CollegeDekho data is for Udupi Manipal; keyword-only collection is a documented failure case.
- The Reddit "MUJ Placement Stats 2025" post is from a deleted account with no usable data.
- Stack and Microsoft 365 SSO claims are not verified; authentication status is Unknown, not same and not separate.

## COVERAGE
33,769 chars read (file_size bytes), read to EOF, truncated=false confirmed.

DONE w2d-08-placement-data.digest.md