import os
from pathlib import Path

# Get the absolute path to the root 'pi-cryption' folder
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

# File paths
PI_FILE_PATH = DATA_DIR / "pi_100M.txt"
LOOKUP_FILE_PATH = DATA_DIR / "lookup.npy"

# We use 6 digits because 10^6 = 1,000,000 possible combinations.
# An array of 1,000,000 integers takes roughly 4 Megabytes of RAM.
# If we used 7 digits, it would take 40MB. 6 is the perfect balance of speed and size!
LOOKUP_DIGITS = 6