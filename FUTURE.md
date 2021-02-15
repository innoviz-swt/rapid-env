# FUTURE

## dockers
- clean dangling dockers
```
powershell -c docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
```