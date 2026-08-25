# Digest: w2d-07-library-integration.md

## REPORT
Source file: w2d-07-library-integration.md (MUJ Library and SLCM Public Exposure Report)

## ANSWER SUMMARY
- The official library page names Koha LMS for holdings, a Web OPAC, DSpace for the institutional repository, Knimbus for off-campus access, and Turnitin for plagiarism checking.
- The official page links the Single Window Search Box at http://manipal-koha.informindia.co.in/; the destination self-identifies as the Manipal University Jaipur Library OPAC with login and password prompts and shows no student records anonymously.
- Library identity runs on physical cards: University Identity Card, Smart ID Card swiped at entry, and RFID-enabled and bar-coded ID cards for borrowing, renewal, reservation, and return.
- Circulation rules: PG and UG students borrow five books for 14 days, fines are Rs 2 per day for the first overdue week then Rs 5 per day, and unpaid overdue items block further issue; no online fine payment is documented.
- RemotLog pages describe MUJ Libraries with the MUJ email address as the username for remote resource access; no SLCM SSO or shared token is shown.
- An IP-based DSpace/JSPUI repository (20.219.59.68:8080) exposes a credential-like access instruction in its page title; the report redacts the value and treats it as an exposure incident.
- https://www.mujlibrary.live/ claims a MUJ DigiLibrary with email OTP, catalog, tracking, and renewals, but no official MUJ linkage exists; users should not submit university emails until ownership is confirmed.
- No public MUJ library API or anonymous endpoint returning student records was identified; a bounded negative, not proof of endpoint absence.

## KEY FACTS
- https://jaipur.manipal.edu/central-library.php - official library page naming Koha, Web OPAC, DSpace, Knimbus, Turnitin and linking the OPAC
- https://jaipur.manipal.edu/foa-library.php - faculty-level library page
- https://www.manipal.edu/content/dam/manipal/muj/documents/Library%20Rules-%20Ver1%20for%20Website.pdf - rules PDF: card use, fines, renewal limits, blocking
- http://manipal-koha.informindia.co.in/ - single-window OPAC entry point
- http://20.219.59.68:8080/jspui/handle/123456789/1 - repository collection page with credential-like title exposure
- http://20.219.59.68:8080/jspui/ - IP-based repository root linked from the official page
- https://muj.remotlog.com/ - RemotLog landing with resource counts and e-resource provider names
- https://jaipur-manipal-edu.muj.remotlog.com/login - RemotLog login; MUJ email as username
- https://www.mujlibrary.live/ - unverified DigiLibrary with OTP form and claimed 25,000+ books
- https://mujslcm.jaipur.manipal.edu/ - SLCM landing with no visible library link
- https://muj.slcm.jaipur.manipal.edu/ - alternate SLCM hostname, no library function visible
- https://maheblropac.koha.manipal.edu/ - MAHE Bengaluru Koha catalog; false positive control, not MUJ

## ACTIONABLE LEADS
- P0 disclosure: notify MUJ library leadership (Chief Librarian contact on central-library.php) about the credential-like repository title using redacted evidence; revoke or rotate, scrub titles and metadata, review access logs; do not test the value.
- Authorized review of OPAC borrower-account authorization with synthetic accounts: loan, renewal, fine, and blocking logic.
- Confirm ownership and canonical links for the OPAC, IP-based repository, RemotLog, and mujlibrary.live through official library channels.
- Reconcile collection counts: RemotLog reports nearly 75,000 books while mujlibrary.live claims 25,000+; label each figure by system and date.
- Verify identity boundaries: whether RFID card records, OPAC accounts, RemotLog, and SLCM share any provisioning or SSO path.
- Ask MUJ to publish an official library-systems page stating which systems are or are not connected to SLCM.

## FLAGS
- The credential-like value in the repository title is intentionally redacted in the report; reproducing or testing it is out of bounds.
- Koha attribution rests on the official page statement; the OPAC page itself does not print the Koha brand.
- mujlibrary.live ownership is unverified; treat as impersonation or squatting risk until MUJ confirms.
- RemotLog is a vendor-style subdomain with self-identification only; operator and federation unknown.
- HTTP (non-TLS) links for OPAC and repository are governance and lifecycle signals, not confirmed vulnerabilities.

## COVERAGE
49,692 chars read (file_size bytes), read to EOF, truncated=false confirmed.

DONE w2d-07-library-integration.digest.md