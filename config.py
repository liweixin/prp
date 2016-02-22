import platform

def isWindowsSystem():
    return 'Windows' in platform.system()
def isLinuxSystem():
    return 'Linux' in platform.system()

if isLinuxSystem():
    #config in linux.
    templatesPath = "templates"
    dbn = "mysql"
    db = "rogueapdetection_test"
    dbuser = "root"
    dbpw = "fishing"
if isWindowsSystem():
    #config in windows
    templatesPath = "templates"
    dbn = "mysql"
    db = "RogueAPDetection"
    dbuser = "root"
    dbpw = "liweixin"
