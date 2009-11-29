'''
Created on 02/08/2009

@author: mizhal
'''

from ConfigParser import ConfigParser, NoSectionError

class IniFile(object):
    '''
    Interfaz de acceso a configuracion
    escrita en un fichero INI
    '''
    singleton = None

    def __init__(self, fname):
        '''
        Constructor
        '''
        self.parser = ConfigParser()
        self.parser.read([fname])
        self.fname = fname
        
    def put(self, name, value):
        section, option = name.split(".")[:2]
        try:
            self.parser.set(section, option, value)
        except NoSectionError, e:
            self.parser.add_section(section)
            self.parser.set(section, option, value)    
        
    def get(self, name):
        section, option = name.split(".")[:2]
        try:
            return self.parser.get(section, option)
        except:
            return None
        
    def ls(self):
        result = []
        for section in self.parser.sections():
            for item in self.parser.items(section):
                result.append(".".join([section, item[0]]))
        return result
        
    def commit(self):
        f = open(self.fname, "w")
        self.parser.write(f)
        f.close()