"""
To build cx_Freeze executable:

    python setup.py bdist_msi
"""
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

import PyQt5
from glob import glob
import sys, os
import os.path as osp
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('edit_table.py', base=base)
]

PY_HOME = osp.abspath(osp.join(osp.split(os.__file__)[0], os.pardir))
# C:\Anaconda2\Library\plugins\platforms
platforms_file = osp.join(PY_HOME, "Library", "plugins", 'platforms', 'qwindows.dll')
setup(name='pyqt_db',
      version = '1.0',
      description = 'Playing around with Qt5 and database widgets',
      data_files = [
        ('', glob(r'C:\Windows\SYSTEM32\msvcp100.dll')),
        ('', glob(r'C:\Windows\SYSTEM32\msvcr100.dll')),
        ('', ['example.sqlite']),
        #('platforms', glob(osp.join(PY_HOME, 'Lib\site-packages\PyQt5\plugins\platforms\windows.dll'))),
        ('platforms', [platforms_file]),
        #('images', ['images\logo.png']),
        #('images', ['images\shannon.png']),
        ],
    options = {
        'py2exe': {
            'bundle_files': 1,
            'includes': ['sip', 'PyQt5.QtCore'],
        }
        },
      executables = executables)
