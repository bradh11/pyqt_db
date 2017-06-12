# PyQt and Databases
Play around with a sqlite database connected to a simple PyQt gui.

## The Qt QODBC plugin
Anaconda does not ship with the ODBC plugin for QT.  Look in the directory 
`%ANACONDA_HOME%\Library\plugins\sqldrivers`

You can get the `QODBC` plugin from the Qt distribution.  You can find the
driver at `%QTDIR%\msvc2015\plugins\sqldrivers\qsqlodbc.dll`.

If you grab QT distribution compiled with the same Visual Studio version as the
Anaconda QT all you need is the `.dll`.  The driver requires basic VS libraries
like `msvcp140.dll`. 

You can copy the redistributable dlls from the Visual Studio install directory
`%VSHOME%\VC\redist\x86\Microsoft.VC140.CRT` into the Anaconda home and
everything will work.  Notice that other fundamental libraries are already in 
`C:\Anaconda2`

The depdency walker helps a bit, but not too much.  These references helped:

 - https://stackoverflow.com/questions/17023419/win-7-64-bit-dll-problems
 - https://stackoverflow.com/questions/33276790/problems-with-deploying-qt5-application-on-windows/33292008#33292008

I still don't know what is going on completely.  The `driver_test.py` test
script did not work until I copied of the redist dlls, but I remved the dll's
and the script still worked.  Also the GUI example `view_query_msaccess.py`
crashes, but the CLI examples work fine.



## Examples
