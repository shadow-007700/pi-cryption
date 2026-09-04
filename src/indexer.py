import sys
import os
import numpy as np
from pathlib import Path
from tqdm import tqdm

# This ensures we can import our other modules even if we run this script directly
sys.path.append(str(Path(__file__).parent.parent))

from src.config import PI_FILE_PATH, LOOKUP_FILE_PATH, LOOKUP_DIGITS
from src.file_io import stream_pi_data

def build_lookup_table():
    """
    Scans the Pi dataset and builds a Numpy array where the index represents 
    a 6-digit number, and the value represents its first occurrence in Pi.
    """
    total_combinations = 10 ** LOOKUP_DIGITS  # 1,000,000
    
    # Initialize a Numpy array with -1. 
    # -1 means "We haven't found this number yet."
    # We use np.int32 because our max index (50,000,000) easily fits in 32 bits, saving RAM.
    print(f"Allocating RAM for {total_combinations} combinations...")
    lookup_table = np.full(total_combinations, -1, dtype=np.int32)
    
    # Keep track of how many unique combinations we've found
    found_count = 0

    print("Opening Pi dataset...")
    with stream_pi_data(str(PI_FILE_PATH)) as pi_mmap:
        
        # Calculate how many iterations we need (Total length - 6)
        file_length = len(pi_mmap)
        max_iterations = file_length - LOOKUP_DIGITS
        
        print("Scanning Pi and building the lookup table (This might take a minute)...")
        
        # We use tqdm to give us a beautiful progress bar in the terminal
        for i in tqdm(range(max_iterations), desc="Indexing Pi"):
            
            # Grab exactly 6 bytes (e.g., b'141592')
            chunk = pi_mmap[i : i + LOOKUP_DIGITS]
            
            try:
                # Convert the byte string directly into an integer (141592)
                # This is where a decimal point in the file would crash the program!
                num_value = int(chunk)
                
            except ValueError:
                # If we hit a bad character (like a newline or dot), fail gracefully
                print(f"\n[ERROR] Found invalid character at index {i}: {chunk}")
                print("Did you make sure to remove '3.' and newlines from your dataset?")
                return

            # If the value at this index is -1, it means this is the FIRST time 
            # we are seeing this 6-digit number!
            if lookup_table[num_value] == -1:
                lookup_table[num_value] = i
                found_count += 1
                
                # OPTIMIZATION: If we found all 1,000,000 numbers, we can stop early!
                if found_count == total_combinations:
                    print("\nWow! Found all 1,000,000 combinations early! Stopping scan.")
                    break

    print(f"\nScan complete. Found {found_count} out of {total_combinations} possible 6-digit numbers.")
    print("Saving highly-optimized lookup table to disk...")
    
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(LOOKUP_FILE_PATH), exist_ok=True)
    
    # Save the numpy array to a binary .npy file for instantaneous loading later
    np.save(LOOKUP_FILE_PATH, lookup_table)
    print(f"Success! Lookup table saved to {LOOKUP_FILE_PATH}")

if __name__ == "__main__":
    build_lookup_table()