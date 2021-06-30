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

## Usage
### from code
``` python
import rapidenv
```

### from command line
run as module via command line.
```commandline
renv
```
or
```commandline
python -m rapidenv
```

### cmd helpers
- mng: running manage.py 'def main()' function from project root.  
  project root located searching .git in current and parent folder recursively.
  