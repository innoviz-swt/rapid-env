# Rapid ENV
Library with helpers for rapid development environment ramp up, build and distribution. 

## SUBMODULES
* osh - operating system helpers (path copy, running processes).
* git - provides default git ignore template.
* conan - conan helpers, wrapping some [conan](https://conan.io/) command lines and flows.
* docker - docker helpers, wrapping some [docker](https://www.docker.com/) command lines and flows.

## installation
```commandline
pip install rapid-env
```

## command line support
run as module via command line.  
```
python -m rapidenv
```

## library usage 
``` python
import rapidenv
```