# DISCLOSURE-LETTER — draft for the registrar / IT Infra

Purpose: turn the club's recon into a documented, authorized engagement.
Send on university letterhead, signed by registrar or IT Infra head, and
keep one signed copy with the club advisor. Two test accounts (student
roles) MUST be named in the letter.

---
To: Registrar / IT Infra, Manipal University Jaipur
From: CyberSpace Club (advisor: <PROF NAME>, HOD)
Date: <DATE>
Subject: Authorized security testing of the MUJ SLCM portal (SC-<N>)

1. Scope: ONLY https://mujslcm.jaipur.manipal.edu during <START> to
   <END> (UTC). No other hosts. HTTP requests only, no payloads that
   corrupt data, no denial-of-service, no credential use beyond the two
   named test accounts below, no copying of student data beyond a
   minimal proof (1 record, redacted).

2. Method: standard web application security testing (OWASP ASVS
   level 1 to 2): authentication/session checks, authorization (IDOR),
   input validation, file upload, CSRF. All tests run from the campus
   network with the named accounts.

3. Test accounts (created by IT Infra for this engagement):
   a) <regno-1> (student), b) <regno-2> (student)

4. Contacts: club SPOC <NAME> <PHONE>, advisor <PROF NAME>, IT Infra
   <NAME> <PHONE>. Findings go ONLY to IT Infra and the registrar;
   no public disclosure without written approval. Expected timeline:
   findings report within <N> days of completion; remediation review
   in 90 days.

5. Ground rules: no persistence, no exfiltration, no payment
   transactions, no attempts on accounts other than the two named
   above. Any accidental exposure is reported immediately and not
   stored. This letter is the club's binding scope.

6. Legal: this letter documents permission under the IT Act 2000 as
   amended (sections 43, 66) for the named persons and dates above.
   Testing outside this scope is not authorized.

Signed:  _________________________ Registrar / IT Infra
Date:
---
Checklist before sending:
[x] hosts + dates + accounts + window written in
[x] advisor copy kept
[x] test accounts exist and work (login once)
[x] club SPOC + IT contact named
[x] one signed copy scanned to the repo (SECRETS: do NOT commit scans
    with signatures into a public repo; keep in club drive)