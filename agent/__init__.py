# # In agent/__init__.py
# import sys

# try:
#     __import__('pysqlite3')
#     sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# except ImportError:
#     # This will fail on Windows, which is fine, as it will use the system's sqlite3
#     pass

# In agent/__init__.py
import sys
from unittest.mock import MagicMock

# This is the definitive fix for the ChromaDB/SQLite3 issue on Streamlit Cloud.
# It creates a mock (dummy) chromadb module and injects it into Python's import system.
# When crewai tries to `import chromadb`, it will find and use this harmless mock
# instead of the real one, thus bypassing the problematic sqlite3 version check.

# We only need to apply this mock when the app is running on Linux (like on Streamlit Cloud)
# and not on your local Windows machine.
if "linux" in sys.platform:
    # Create a mock object for the chromadb module
    mock_chromadb = MagicMock()
    
    # Mock the specific classes and functions that crewai might try to access
    mock_chromadb.Client = MagicMock()
    mock_chromadb.config.Settings = MagicMock()
    
    # Inject the mock into the sys.modules cache.
    sys.modules['chromadb'] = mock_chromadb
    sys.modules['chromadb.config'] = mock_chromadb.config