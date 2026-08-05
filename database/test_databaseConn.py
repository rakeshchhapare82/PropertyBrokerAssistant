import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database.database import test_connection


if __name__ == "__main__":
    if test_connection():
        print("Database Connected Successfully")
    else:
        print("Database Connection Failed")