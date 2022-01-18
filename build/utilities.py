from win32com.client import Dispatch

#checks Chrome Version and returns correct Chromedriver to use
def findChromeDriverVersion():
    ver_parser = Dispatch('Scripting.FileSystemObject')
    info = ver_parser.GetFileVersion('C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
    if info[0:2:] == '97':
        return 'chromedriver97.exe'
    elif info[0:2:] == '96':
        return 'chromedriver96.exe'
    elif info[0:2:] == '95':
        return 'chromedriver95.exe'
    elif info[0:2:] == '94':
        return 'chromedriver94.exe'
    elif info[0:2:] == '93':
        return 'chromedriver93.exe'

