# In agent/__init__.py
import sys

try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    # This will fail on Windows, which is fine, as it will use the system's sqlite3
    pass