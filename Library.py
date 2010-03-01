from os import walk
from os.path import join

from exceptions import Exception

from pdflib.PDFFileMapper import PDFFileMapper
from pdflib.PDFSQliteMapper import PDFSQliteMapper

class Library:
	def __init__(self, backend = None):
		pass
		
	def _scanDirectory(self, directory):
		pdf_load = PDFFileMapper()
		for root, dirs, files in walk(directory):
			for i in files:
				if i.upper().endswith(".PDF"):
					yield pdf_load.loadOne(join(root, i))
		
	def loadBooksFromDirectory(self, directory):
		scanner = self._scanDirectory(directory)
		mapper = PDFSQliteMapper()
		while True:
			books = []
			try:
				for i in range(20):
					pdf = scanner.next()
					books.append(pdf)
				mapper.saveMany(books)
			except StopIteration, e:
				mapper.saveMany(books)
				break
	
	def ls(self, page = -1):
		if page == -1:
			for pdf in PDFSQliteMapper().loadAll():
				print pdf.id,":", pdf.title
		else:
			for pdf in PDFSQliteMapper().loadAllPaged(50*page, 50):
				print pdf.id,":", pdf.title
				
	def getBook(self, id):
		return PDFSQliteMapper().loadById(id)
				
	def listBooks(self, page = -1):
		if page == -1:
			return PDFSQliteMapper().loadAll()
		else:
			return PDFSQliteMapper().loadAllPaged(page*50, 50)
			
		
			
					
		
	