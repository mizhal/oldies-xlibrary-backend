from os import walk
from os.path import join

from exceptions import Exception

from pdflib.PDFFileMapper import PDFFileMapper

from config import adapt_filename_encoding, adapt_name

class Library:
	def __init__(self, backend = None):
		self.backend = backend
		
	def _scanDirectory(self, directory):
		pdf_load = PDFFileMapper()
		directory = adapt_filename_encoding(directory)
		for root, dirs, files in walk(directory):
			for i in files:
				if i.upper().endswith(".PDF"):
					try:
						unicode_name = adapt_name(join(root, i))
					except:
						## @todo LOG del fallo
						continue
					yield pdf_load.loadOne(unicode_name)
		
	def loadBooksFromDirectory(self, directory):
		scanner = self._scanDirectory(directory)
		
		while True:
			books = []
			try:
				for i in range(20):
					pdf = scanner.next()
					books.append(pdf)
				self.backend.saveMany(books)
			except StopIteration, e:
				self.backend.saveMany(books)
				break
	
	def ls(self, page = -1):
		if page == -1:
			for pdf in self.backend.loadAll():
				print pdf.id,":", pdf.title
		else:
			for pdf in self.backend.loadAllPaged(50*page, 50):
				print pdf.id,":", pdf.title
				
	def getBook(self, id):
		return self.backend.loadById(id)
				
	def listBooks(self, page = -1):
		if page == -1:
			return self.backend.loadAll()
		else:
			return self.backend.loadAllPaged(page*50, 50)
			
		
			
					
		
	