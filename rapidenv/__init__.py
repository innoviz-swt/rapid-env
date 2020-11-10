from . import conan
from . import osh
from . import git
from . import docker

try:
    from .version import __version__, __build__
except:
    __version__ = "0.0.0"
    __build__ = "dev"
