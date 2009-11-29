# -*- coding: utf-8 -*-
'''

@author: mizhal
'''
import unittest
from os import remove

import pysqlite2.dbapi2 as sqlite

from pdflib.PDFSQliteMapper import PDFSQliteMapper

from Library import Library

class Test(unittest.TestCase):
	def setUp(self):
		con = sqlite.Connection("./test-libreria.sqlite")
		con.text_factory = str
		PDFSQliteMapper.flyweight = con
		ldr = PDFSQliteMapper()
		ldr.createTable()

	def tearDown(self):
		ldr = PDFSQliteMapper()
		ldr.dropTable()
		PDFSQliteMapper.flyweight.close()
		#remove("./test-libreria.sqlite")
		
	def testBasico(self):
		dir = "/var/mik6/Mediateca/Referencia"
		
		lib = Library(PDFSQliteMapper())
		lib.loadBooksFromDirectory(dir)
		
		cur = PDFSQliteMapper.flyweight.cursor()
		cur.execute("select * from pdfs")
		print len(cur.fetchall())
			
		

if __name__ == "__main__":
    import sys;
    sys.argv = ['Test.testBasico']
    unittest.main()
