import platform
import locale

import popen2
from os.path import split, join, exists

pdf2textexe = "pdftotext"
pdf2textpath = None
pdfinfo = "pdfinfo"

osname = platform.system()

if osname == "Windows":
	pdf2textpath = join(*split(__file__)[:-1])
	pdf2textexe = join(pdf2textpath, "pdftotext.exe")
	pdfinfo = join(pdf2textpath, "pdfinfo.exe")
	pdfextractcomment = join(pdf2textpath, "pdf-extract-comment.exe")
	parts = __file__.split("\\")
	decode_console_encoding = lambda x:x.decode(locale.getpreferredencoding())
	to_console_encoding = lambda x: x.encode(locale.getpreferredencoding())

elif osname == "Linux" :
	pdf2textexe = "pdftotext"
	pdfinfo = "pdfinfo"
	decode_console_encoding = lambda x: x.decode(locale.getpreferredencoding())
	to_console_encoding = lambda x: x.encode(locale.getpreferredencoding())
else:
	raise "unkwown system"