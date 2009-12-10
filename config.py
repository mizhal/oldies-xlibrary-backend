import platform
import locale

osname = platform.system()

if osname == "Windows":
	adapt_filename_encoding = lambda x: x.decode(locale.getpreferredencoding())
	adapt_name = lambda x:x
elif osname == "Linux" :
	adapt_filename_encoding = lambda x: x
	adapt_name = lambda x: x.decode(locale.getpreferredencoding())
else:
	raise "unkwown system"