import sys
from pathlib import Path

# Ensure we can import our other modules
sys.path.append(str(Path(__file__).parent.parent))

from src.config import PI_FILE_PATH
from src.file_io import stream_pi_data

def decode_coordinates(coordinates: list[tuple[int, int]]) -> str:
    """
    Takes a list of (index, length) coordinates and reconstructs the 
    original string by fetching the exact chunks from the Pi dataset.
    """
    decoded_string = ""
    
    print("Opening Pi dataset for decryption...")
    # We use our memory-mapped file reader to jump around the 100MB file instantly
    with stream_pi_data(str(PI_FILE_PATH)) as pi_mmap:
        
        for idx, length in coordinates:
            # Slicing the mmap returns bytes, e.g., b'1415'
            chunk_bytes = pi_mmap[idx : idx + length]
            
            # Convert the bytes back to a standard Python string
            chunk_str = chunk_bytes.decode('ascii')
            
            # Append it to our final message
            decoded_string += chunk_str
            
    return decoded_string

if __name__ == "__main__":
    # Let's test it using the coordinates that would be generated for "141592653589793238"
    # (Since this is the start of Pi, it should be index 0, length 18)
    test_coordinates = [(0, 18)]
    
    print(f"\nEncrypted Coordinates: {test_coordinates}")
    
    result = decode_coordinates(test_coordinates)
    
    print("\n--- DECRYPTION COMPLETE ---")
    print(f"Recovered Message: {result}")
    
    # Let's do a more complex test with random chunks
    # Index 100 for 5 digits, and Index 9999 for 4 digits
    complex_coords = [(100, 5), (9999, 4)]
    print(f"\nTesting complex coordinates: {complex_coords}")
    print(f"Recovered Message: {decode_coordinates(complex_coords)}")