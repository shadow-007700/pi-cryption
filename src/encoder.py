import numpy as np
from src.config import PI_FILE_PATH, LOOKUP_FILE_PATH, LOOKUP_DIGITS
from src.file_io import stream_pi_data

def get_longest_match_length(pi_mmap, start_idx, target_bytes):
    """
    Uses binary search to find exactly how long the match continues 
    at the given index in Pi.
    """
    # We already know the first LOOKUP_DIGITS (6) match perfectly
    low = LOOKUP_DIGITS
    high = len(target_bytes)
    best_length = LOOKUP_DIGITS
    
    # Binary search to find the maximum matching length
    while low <= high:
        mid = (low + high) // 2
        
        # Check if the chunk in Pi matches the chunk in our target
        if pi_mmap[start_idx : start_idx + mid] == target_bytes[:mid]:
            # It matches! So the match is AT LEAST this long. 
            best_length = mid
            # Let's see if we can go even higher
            low = mid + 1
        else:
            # It didn't match, so the actual length must be shorter
            high = mid - 1
            
    return best_length

def encode_string(target_string: str) -> list[tuple[int, int]]:
    """
    Takes a string of numbers and encodes it into a list of (index, length) tuples
    using the Pi dataset and the pre-computed lookup table.
    """
    if not target_string.isdigit():
        raise ValueError("Error: Target must only contain digits (0-9).")
        
    print("Loading fast lookup table...")
    lookup_table = np.load(LOOKUP_FILE_PATH)
    
    encoded_pairs = []
    
    print("Opening Pi dataset...")
    with stream_pi_data(str(PI_FILE_PATH)) as pi_mmap:
        
        # We work with bytes because mmap returns bytes, and it's faster
        remaining_target = target_string.encode('ascii')

        # FAILSAFE: Ensure we never get stuck in an infinite loop!
        max_iterations = len(remaining_target)
        loops = 0
        
        while remaining_target:

            loops += 1
            if loops > max_iterations:
                raise RuntimeError("Encoder caught in an infinite loop! Check indentation.")
            # EDGE CASE: What if we have fewer than 6 digits left to encode?
            # Our lookup table only works for exactly 6 digits.
            if len(remaining_target) < LOOKUP_DIGITS:
                # We fall back to a standard string search for tiny fragments
                idx = pi_mmap.find(remaining_target)
                if idx == -1:
                    raise RuntimeError("Failed to find chunk in Pi! (Dataset too small)")
                
                # Safely cast to standard python int for the final output
                encoded_pairs.append((int(idx), len(remaining_target)))
                break
                
            # THE HAPPY PATH: 6 or more digits
            prefix = remaining_target[:LOOKUP_DIGITS]
            
            # Instantly get the index of the first 6 digits from our Numpy array
            prefix_int = int(prefix)
            
            # FIX: Use .item() to safely extract a pure Python integer from the Numpy array
            idx = lookup_table[prefix_int].item()
            
            if idx == -1:
                # Fallback search if lookup table missed it
                idx = pi_mmap.find(prefix)
                if idx == -1:
                    raise RuntimeError(f"Critical Error: Chunk {prefix} not found in dataset!")
                
            # Now, use binary search to see if digits 7, 8, 9, etc., also match!
            match_len = get_longest_match_length(pi_mmap, idx, remaining_target)

            # HARD ABORT: Ensure the algorithm is mathematically forced to shrink the target
            if match_len <= 0:
                raise RuntimeError("Match length failure. Aborting to prevent hang.")
        
            # Safely cast both to standard Python integers so the decoder doesn't crash
            encoded_pairs.append((int(idx), int(match_len)))
            
            # Chop off the part we just encoded, and loop again for the rest
            remaining_target = remaining_target[match_len:]
            
    return encoded_pairs

if __name__ == "__main__":
    # Let's test it with a 15-digit number!
    secret_message = "141592653589793238" 
    
    print(f"\nTarget Number: {secret_message}")
    print(f"Length: {len(secret_message)} digits\n")
    
    coordinates = encode_string(secret_message)
    
    print("\n--- ENCODING COMPLETE ---")
    print(f"Map Coordinates: {coordinates}")
    print(f"Number of chunks needed: {len(coordinates)}")