from PDF import PDF

class PDFSQliteMapper:
	''' '''
	flyweight = None ## @note apunta al "singleton" de la conexion a la base de datos
	
	FIELDS = '''id, 
		title,
		file_name,
		author,
		creator,
		creation_date,
		encrypted,
		file_size,
		keywords,
		subject,
		pages,
		has_text '''
	
	def createTable(self):
		sql = '''create table pdfs(
			id integer not null primary key autoincrement,
			title text not null,
			file_name text not null,
			author text not null,
			creator text not null,
			creation_date timestamp,
			encrypted bool,
			file_size integer,
			keywords text,
			subject text,
			pages integer,
			has_text integer
		)'''
		cur = PDFSQliteMapper.flyweight.cursor()
		cur.execute(sql)
		
	def dropTable(self):
		sql = '''drop table pdfs'''
		cur = PDFSQliteMapper.flyweight.cursor()
		cur.execute(sql)		
		
	def verifySchema(self):
		sql = "select %s from pdfs"%PDFSQliteMapper.FIELDS
		cur = PDFSQliteMapper.flyweight.cursor()
		try:
			cur.execute(sql)
			return True
		except:
			return False
	
	INSERT_SQL = """insert into pdfs(
					title,
					file_name,
					author,
					creator,
					creation_date,
					encrypted,
					file_size,
					keywords,
					subject,
					pages,
					has_text) 
				values(?,?,?,?,?,?,?,?,?,?,?);select last_insert_rowid()"""
					
	UPDATE_SQL = """update pdfs set
					title = ?,
					file_name = ?,
					author = ?,
					creator = ?,
					creation_date = ?,
					encrypted = ?,
					file_size = ?,
					keywords = ?,
					subject = ?,
					pages = ?,
					has_text = ?
				where id = ?"""
	
	def save(self, pdf):
		cur = PDFSQliteMapper.flyweight.cursor()
		if pdf.id == -1:
			for row in cur.execute(PDFSQliteMapper.INSERT_SQL , 
					(pdf.title, 
						pdf.fname,
						pdf.author,
						pdf.creator,
						pdf.creation_date,
						pdf.encrypted,
						pdf.file_size,
						",".join(pdf.keywords),
						pdf.subject,
						pdf.pages,
						pdf.has_text
					)
				):
				pdf.id = row[0]
		else:
			cur.execute(PDFSQliteMapper.UPDATE_SQL, 
					(pdf.title, 
						pdf.fname,
						pdf.author,
						pdf.creator,
						pdf.creation_date,
						pdf.encrypted,
						pdf.file_size,
						",".join(pdf.keywords),
						pdf.subject,
						pdf.pages,
						pdf.has_text,
						pdf.id
					)
				)
		
	def saveMany(self, pdfs):
		cur = PDFSQliteMapper.flyweight.cursor()
		updates = []
		for pdf in pdfs:
			if pdf.id == -1:
				for row in cur.execute(PDFSQliteMapper.INSERT_SQL , 
					(pdf.title, 
						pdf.fname,
						pdf.author,
						pdf.creator,
						pdf.creation_date,
						pdf.encrypted,
						pdf.file_size,
						",".join(pdf.keywords),
						pdf.subject,
						pdf.pages,
						pdf.has_text
					)
				):
					pdf.id = row[0]
			else:
				updates.append(( pdf.title, 
						pdf.fname,
						pdf.author,
						pdf.creator,
						pdf.creation_date,
						pdf.encrypted,
						pdf.file_size,
						",".join(pdf.keywords),
						pdf.subject,
						pdf.pages,
						pdf.has_text,
						pdf.id
					)
				)
				
		cur.executemany(PDFSQliteMapper.UPDATE_SQL,updates) 
		
	DELETE_SQL = '''delete from pdfs where id = ?'''
	def delete(self, pdf):
		cur = PDFSQliteMapper.flyweight.cursor()
		cur.execute(PDFSQliteMapper.DELETE_SQL, (pdf.id,) ) 
		pdf.id = -1
		
	def deleteMany(self, pdfs):
		cur = PDFSQliteMapper.flyweight.cursor()
		cur.executemany(PDFSQliteMapper.DELETE_SQL, 
						[(pdf.id,) for pdf in pdfs]) 
		for pdf in pdfs:
			pdf.id = -1
	
	def _loadOne(self, sql):
		cur = PDFSQliteMapper.flyweight.cursor()
		cur.execute(sql)
		row = cur.next()
		
		new = PDF()
		new.id = row[0]
		new.title = row[1]
		new.fname = row[2]
		new.author = row[3]
		new.creator = row[4]
		new.creation_date = row[5]
		new.encrypted = row[6]
		new.file_size = row[7]
		new.keywords = row[8]
		new.subject = row[9]
		new.pages = row[10]
		new.has_text = row[11]
		
		return new
		
	def _loadMany(self, sql):
		cur = PDFSQliteMapper.flyweight.cursor()
		results = []
		for row in cur.execute(sql):
			new = PDF()
			new.id = row[0]
			new.title = row[1]
			new.fname = row[2]
			new.author = row[3]
			new.creator = row[4]
			new.creation_date = row[5]
			new.encrypted = row[6]
			new.file_size = row[7]
			new.keywords = row[8]
			new.subject = row[9]
			new.pages = row[10]
			new.has_text = row[11]
			
			results.append(new)
		
		return results
		
	def _loadManyPaged(self, sql, offset, limit):
		return self._loadMany("%s limit %s offset %s"% (sql, limit, offset))
		
	def loadById(self, id):
		return self._loadOne("select %s from pdfs where id = %s"%(PDFSQliteMapper.FIELDS, id))
		
	def loadAll(self):
		return self._loadMany("select %s from pdfs"%PDFSQliteMapper.FIELDS)
		
	def loadAllPaged(self, page, size):
		return self._loadManyPaged("select %s from pdfs"%PDFSQliteMapper.FIELDS, page, size)
		
	def loadByCreationDateRange(self, start, end):
		pass
		
	def loadByEnteringDateRange(self, start, end):
		pass
		
	def loadByAuthor(self, author):
		pass
		
	def loadBySimilarity(self, partial_fullfill_pdf):
		pass
		
	def filterByTitlePrefix(self, title_prefix):
		pass
		