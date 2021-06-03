# Rapid Env Changelog

# 0.0.3 
- osh
    - run_process: kargs cwd get special handling, changing to abs path cmd starting with './' for Windows and POSIX uniform behavior.
    - copy_path renamed to copy
    - copy_large, and copy_large_file added

# 0.0.2
- osh : 
    - run_process 
        - in case of exception and raise_exception flag set to False, return None 
    - run_process_with_stdout 
        - added a build-in strip on the returned value
        - in case of exception and raise_exception flag set to False, return None 

# 0.0.1
- added __main__.py allowing running functions from cmd using python -m rapidenv  
  see python -m rapidenv -h for help
- docker: added docker utils support
    - rm_all, attempt removing all containers specified in docker ps -a 
- os module renamed to osh.
- osh :  
    - copy_path - mkdirs parent folder (if required), than either copy(file) or copytree(dir).
    - run_process 
        - runs the process in cwd (if specified), and waits for him to finish successfully.
        - added stdout an optional parameter
- git:add_gitignore 
    - bugfix, missing .gitignore template
    - git : add_gitignore : copy .gitignore template to path
