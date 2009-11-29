import platform

import popen2
from os.path import split, join, exists

pdf2textexe = "pdftotext"
pdf2textpath = None
pdfinfo = "pdfinfo"

if platform.uname()[0] == "Windows":
	decode_console_encoding = lambda x: x #.decode("cp1252")
	pdf2textpath = join(*split(__file__)[:-1])
	pdf2textexe = join(pdf2textpath, "pdftotext.exe")
	pdfinfo = join(pdf2textpath, "pdfinfo.exe")
	pdfextractcomment = join(pdf2textpath, "pdf-extract-comment.exe")
else:
	decode_console_encoding = lambda x: x.decode("utf8")
	pdf2textexe = "pdftotext"
	pdfinfo = "pdfinfo"