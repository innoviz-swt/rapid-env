@echo off

rem run manage py from root folder (..\..\ -> assumes batch file in venv\Scripts relative to project root)
%~dp0\python %~dp0\..\..\manage.py %1 %2 %3 %4 %5 %6 %7 %8 %9
