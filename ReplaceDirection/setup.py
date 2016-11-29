from distutils.core import setup
import py2exe

setup( windows=['WindowMain.py'],
       zipfile = None,
       options = {'py2exe' : { 
                     "bundle_files": 1,
                     "dll_excludes": ["MSVCP90.dll","w9xpopen.exe"],
                     "includes": ["sip"],
                     "compressed": 1,
                     "optimize": 2,                     
                     }
                  }
 )