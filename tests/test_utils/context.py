import os
import sys

try:
    # rapidenv installed
    import rapidenv
    __INSTALLED__ = True
except:
    # running from tests folder
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    import rapidenv
    __INSTALLED__ = False

