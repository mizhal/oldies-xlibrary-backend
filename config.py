import platform
import locale


osname = platform.system()

if osname == "Windows":
	pass
elif osname == "Linux" :
	pass
else:
	raise "unkwown system"