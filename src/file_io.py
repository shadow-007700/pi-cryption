import mmap
import os
from contextlib import contextmanager

@contextmanager
def stream_pi_data(filepath: str):
    """
    A context manager that memory-maps the Pi dataset.
    Using a context manager (the 'with' statement) ensures that our files 
    are safely closed if the program crashes or finishes.
    
    Yields:
        mmap.mmap: A memory-mapped byte array of the Pi dataset.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Error: Could not find '{filepath}'.\n"
            "Please ensure you have downloaded a Pi dataset and placed it in the /data folder."
        )

    # We must open the file in binary read-only mode ("rb") for mmap to work optimally
    file_obj = open(filepath, "rb")
    pi_mmap = None
    
    try:
        # Create the memory map. 
        # length=0 means map the entire file.
        # access=mmap.ACCESS_READ ensures we don't accidentally overwrite Pi!
        pi_mmap = mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ)
        yield pi_mmap
    finally:
        # This cleanup code runs automatically when we are done
        if pi_mmap is not None:
            pi_mmap.close()
        file_obj.close()

# --- Quick Test (You can run this file directly to test it) ---
if __name__ == "__main__":
    # Assuming you have a file named pi_50M.txt in the data folder
    test_path = "../data/pi_50M.txt"
    
    # Create a dummy file just for this quick test if it doesn't exist
    os.makedirs("../data", exist_ok=True)
    if not os.path.exists(test_path):
        with open(test_path, "wb") as f:
            f.write(b"14159265358979323846264338327950288419716939937510")
            print("Created a tiny dummy Pi file for testing.")

    # Test the mmap function
    print("Opening Pi dataset via mmap...")
    with stream_pi_data(test_path) as pi_memory_map:
        # Read the first 10 digits. Notice the 'b' prefix, it returns bytes!
        first_10_digits = pi_memory_map[:10]
        print(f"First 10 digits found: {first_10_digits.decode('ascii')}")
        print("Success! The memory-mapper is working perfectly.")