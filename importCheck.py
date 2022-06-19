try:
    import rich
except ImportError:
    print("Module rich not found")
    raise ImportError("Module rich not found")

try:
    import sqlite3
except ImportError:
    print("Module sqlite3 not found")
    raise ImportError("Module sqlite3 not found")

try:
    import matplotlib
except ImportError:
    print("Module matplotlib not found")
    raise ImportError("Module matplotlib not found")

try:
    import re
except ImportError:
    print("Module re not found")
    raise ImportError("Module re not found")
