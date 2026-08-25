#!/usr/bin/env python3
"""Upload-surface tests (benign only).

Uploading documents is part of the onboarding surface (PDF <=1MB, photo
jpg <=100KB per official guide). Tests: filename encoding, extension
case, double extension, mime mismatch, oversize. Content is ALWAYS plain
text or a tiny valid JPEG. NO scripts, NO executables, NO polyglots."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import Session, require_accounts

require_accounts()
s = Session(os.environ["SLCM_USER1"], os.environ["SLCM_PASS1"], "upload-tests")
if not s.authenticated:
    print("LOGIN FAILED; aborting")
    raise SystemExit(1)

UPLOAD_CANDIDATES = ["/Student/Document/Upload", "/Student/Profile/Upload",
                     "/Student/Photo/Upload", "/api/Student/Document/Upload"]
BLESSED = b"%PDF-1.4 test document content, benign"
JPG = bytes([0xFF, 0xD8, 0xFF, 0xE0]) + b"JFIF benign test photo" + bytes([0xFF, 0xD9])

MULTI = b"----------------------------boundary1234\r\n"

def multipart(field, filename, content, ctype):
    inner = (f'Content-Disposition: form-data; name="{field}"; filename="{filename}"\r\n'
             f"Content-Type: {ctype}\r\n\r\n").encode() + content + b"\r\n"
    body = (MULTI + b'Content-Disposition: form-data; name="fileType"\r\n\r\ndocument\r\n' + MULTI
            + inner + MULTI + b"--\r\n")
    return body, f"multipart/form-data; boundary={MULTI.decode().strip()}"

cases = [
    ("pdf_ok", "test1.pdf", BLESSED, "application/pdf"),
    ("pdf_upper", "TEST2.PDF", BLESSED, "application/pdf"),
    ("pdf_ctorsto", "test3.pdf;.txt", BLESSED, "application/pdf"),
    ("double_ext", "test4.pdf.txt", BLESSED, "text/plain"),
    ("mime_mismatch", "test5.txt", BLESSED, "application/pdf"),
    ("oversize", "big6.pdf", BLESSED + b"A" * (2 * 1024 * 1024), "application/pdf"),
    ("nullish", "test7.pdf%00.txt", BLESSED, "application/pdf"),
    ("photo_ok", "photo8.jpg", JPG, "image/jpeg"),
]

st, h, b = s.get("/Student/Document/Upload")
s.ev("upload_page", st=st, size=len(b))
print(f"[i] upload page reachable as student? st={st}")

for name, fn, content, ctype in cases:
    body, cth = multipart("file", fn, content, ctype)
    st, h, b = s.raw_post(UPLOAD_CANDIDATES[0], body, cth)
    s.ev("upload_case", case=name, filename=fn, st=st, size=len(b))
    print(f"[i] {name:16} {fn:24} -> {st}")

print("DONE. Evidence: recon/authtests/upload-tests.jsonl")
print("NOTE: raw-body uploads need a _raw_post helper; until then this")
print("script logs the prepared cases in dry mode (SLCM_DRY=1 shows them)")