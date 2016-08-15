from webiopi.utils.version import PYTHON_MAJOR
from webiopi.utils import logger

if PYTHON_MAJOR >= 3:
    import configparser as parser
else:
    import ConfigParser as parser

__config__ = None

def loadConfig(configfile):
    if configfile != None:
        logger.info("Loading configuration from %s" % configfile)
        __config__ = Config(configfile)
    else:
        __config__ = Config()
    return __config__

def getConfig():
    return __config__

class Config():
    
    def __init__(self, configfile=None):
        config = parser.ConfigParser()
        config.optionxform = str
        if configfile != None:
            config.read(configfile)
        self.config = config
        self.configfile = configfile

    def get(self, section, key, default):
        if self.config.has_option(section, key):
            return self.config.get(section, key)
        return default

    def getboolean(self, section, key, default):
        if self.config.has_option(section, key):
            return self.config.getboolean(section, key)
        return default
    
    def getint(self, section, key, default):
        if self.config.has_option(section, key):
            return self.config.getint(section, key)
        return default
    
    def items(self, section):
        if self.config.has_section(section):
            return self.config.items(section)
        return {}
    
    def set(self, section, key, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, value)
        
    def unset(self, section, key):
        if self.config.has_option(section, key):
            self.config.remove_option(section, key)
            return True
        return False
        
    def save(self):
        with open(self.configfile, "w") as f:
            self.config.write(f)
    
