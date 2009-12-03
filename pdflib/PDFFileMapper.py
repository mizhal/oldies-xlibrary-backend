'''
Extractor de texto de PDF basado en pdftotext de XPDF,
utilizando el binario mediante pipes.
'''
import re
from os.path import abspath, basename

from PDF import PDF
from config import *

RE_metadata = re.compile("([^:]+)[:]\s+(.*)")
RE_integer = re.compile("([0-9]+).*")

import chardet

def decode(text):
	if isinstance(text, str):
		q = chardet.detect(text)['encoding']
		if q:
			return text.decode(q)
		else:
			return u''
	else:
		return text

class PDFFileMapper:
	def __init__(self):
		pass
		
	def words(self, pdf_object):
		return re.split("\s*", self.extractText(pdf_object.fname))
		
	def wordsInPage(self, page, pdf_object):
		return re.split("\s*", self.extractTextOfPage(pdf_object.fname, page))
		
	def loadOne(self, fname):
		new = PDF()
		new.fname = abspath(fname)
		metadata = self.parseMetadata(fname)
		
		new.title = metadata.get("title", u"")
		if new.title == u"":
			new.title = re.match("(.*)[.][^.]+", basename(fname)).groups()[0]
		
		new.author = metadata.get("author", u"")
		new.creator = metadata.get("creator", u"")
		new.creation_date = metadata.get("creationdate", None)
		new.encrypted = metadata.get("encrypted", u'no') == 'yes'
		q = re.match("([0-9]+).*",metadata.get("file_size", "-1"))
		if q:
			z = q.groups()[0]
			if z != '':
				new.file_size = int(z)
			else:
				new.file_size = -1
		else:
			new.file_size = -1
		new.keywords = metadata.get("keywords", u"").split(" ")
		new.subject = metadata.get("subject", u"")
		z = metadata.get("pages", u"-1")
		if z != '':
			new.pages = int(z)
		else:
			new.pages = -1
			
		########
		## ajuste de codigos de caracteres
		########
		new.title = decode(new.title)
		new.author = decode(new.author)
		new.creator = decode(new.creator)
		new.keywords = decode(new.keywords)
		new.subject = decode(new.subject)
		
		return new
		
	def loadMany(self, file_names):
		res = []
		for fname in file_names:
			res.append(self.loadOne(fname))
		
		return res
		
	def extractText(self, pdf_object):
		if not exists(pdf_object.fname):
			raise "File '%s' not exists"%pdf_object.fname
		pout, pin = popen2.popen2('%s "%s" -'%(pdf2textexe, pdf_object.fname))
		return decode(pout.read())
		
	def extractTextOfPage(self, pdf_object):
		if not exists(pdf_object.fname):
			raise "File '%s' not exists"%pdf_object.fname
		pout, pin = popen2.popen2('%s -f %s -l %s "%s" -'%(pdf2textexe, page, page, pdf_object.fname))
		return decode(pout.read())
		
	def extractComments(self, fname):
		pout, pin = popen2.popen2('%s "%s"'%(pdfextractcomment, fname))
		return decode(pout.read())
		
	def metadata(self, fname):
		if not exists(fname):
			raise "File '%s' not exists"%fname
		pout, pin = popen2.popen2('%s "%s"'%(pdfinfo, fname))
		return decode(pout.read())
		
	def parseMetadata(self, fname):
		''' extrae un diccionario (key - value)
		con los metadatos del PDF'''
		meta = self.metadata(fname)
		metadata = {}
		for line in meta.split("\n"):
			q = RE_metadata.match(line)
			if q:
				tag, value = q.groups()
				tag = tag.lower()
				tag = re.subn("\s+", "_", tag)[0]
				metadata[tag] = value
		return metadata
		
	def countPages(self, fname):
		return self.parseMetadata(fname)['pages']
		
		
