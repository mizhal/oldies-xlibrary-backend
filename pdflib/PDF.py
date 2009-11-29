class PDF(object):
	id = -1
	fname = None
	title = None
	author = None
	creator = None
	creation_date = None
	encrypted = None
	file_size = None
	keywords = None
	subject = None
	pages = 0
	
	has_text = 0 ## indica si hay informacion del texto o solamente es grafico
	def __init__(self):
		self.id = -1
		self.title = None
		self.fname = None
		self.author = None
		self.creator = None
		self.creation_date = None
		self.encrypted = None
		self.file_size = None
		self.keywords = None
		self.subject = None
		self.pages = 0
		self.has_text = 0
	
	def __repr__(self):
		return "<PDF id=%(id)s, title=%(title)s, author=%(author)s, creator=%(creator)s, creation_date=%(creation_date)s, encrypted=%(encrypted)s, file_size=%(file_size)s, keywords=%(keywords)s, has_text=%(has_text)s, subject=%(subject)s, pages=%(pages)s // %(fname)s>"%self.__dict__