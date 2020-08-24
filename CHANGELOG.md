# Rapid Env Changelog

# 0.1.0
- added __main__.py allowing running functions from cmd using python -m rapidenv  
  see python -m rapidenv -h for help
- docker : added docker utilities support
    - rm_all, attempt removing all containers specified in docker ps -a 
- os module renamed to osh
- osh :  copy_path - mkdirs parent folder (if required), than either copy(file) or copytree(dir).
- process : run_process 
    - runs process in cwd (if specified), and wait for him to finish successfully.
    - added stdout a optional parameter
- git:add_gitignore 
    - bug fix, missing .gitignore template
    - git : add_gitignore : copy .gitignore template to path
