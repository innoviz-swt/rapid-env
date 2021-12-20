# FUTURE

## osh
- see download.py
- kill process on port windows
"""
netstat -ano | findstr :9002
taskkill /PID 9002 /F
"""

## vs code
- list-extensions
```
code --list-extensions | % { "code --install-extension $_" }
```

## dockers
- clean dangling dockers
```
powershell -c docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
```

## vim
- clear vin info history:
```
:set viminfo='0,:0,<0,@0,f0
```
-update vimrc (/etc/vimrc or ~/.vimrc) to chdir to current (cmd and netrw)
set autochdir 
let g:netrw_keepdir=0 

