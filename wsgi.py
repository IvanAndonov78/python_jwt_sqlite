
"""
import imp
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

wsgi = imp.load_source('wsgi', 'wsgi.py')
application = wsgi.application
"""

""" also works
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from importlib.machinery import SourceFileLoader

#mymodule = SourceFileLoader('modname', '/path/to/file.py').load_module()
wsgi = SourceFileLoader('wsgi', 'src/app.py').load_module()
application = wsgi.application #yep
"""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from src.app import application
