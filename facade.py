from os.path import join, exists

import pysqlite2.dbapi2 as sqlite

from pdflib.PDFSQliteMapper import PDFSQliteMapper
from Library import Library

subsystem_dir = join("/",*__file__.split("/")[:-1])

class XLibrary:
	def openLibrary(self):
		from readini import IniFile
		config = IniFile(join(subsystem_dir, "config.ini"))
		dbfile = config.get("storage.dbfile")
		if not exists(dbfile):
			con = sqlite.Connection(dbfile)
			con.text_factory = str
			PDFSQliteMapper.flyweight = con
			ldr = PDFSQliteMapper()
			ldr.createTable()
			lib = Library(PDFSQliteMapper())
			
			dir = config.get("storage.files_rootdir")
			lib.loadBooksFromDirectory(dir)
			config.put("storage.created", "1")
			config.commit()
			return lib
		else:
			con = sqlite.Connection(dbfile)
			con.text_factory = str
			PDFSQliteMapper.flyweight = con
			ldr = PDFSQliteMapper()
			if not ldr.verifySchema():
				raise "Error: esquema no coincide"
		
			lib = Library(PDFSQliteMapper())
			
			created = config.get("storage.created") 
			if created == '0':
				dir = config.get("storage.files_rootdir")
				lib.loadBooksFromDirectory(dir)
				config.put("storage.created", "1")
				config.commit()
				return lib
			elif created == '1':
				return lib
			else:
				raise "Error de configuracion created no es 1 o 0"
			
	def closeLibrary(self, lib):
		PDFSQliteMapper.flyweight.close()
		lib = None