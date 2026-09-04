import sys
import pytest
from pathlib import Path

# Ensure pytest can find our root directory when it runs
sys.path.append(str(Path(__file__).parent.parent))

from src.encoder import encode_string
from src.decoder import decode_coordinates
from main import text_to_numbers, numbers_to_text

def test_text_conversion_logic():
    """
    Ensures that our ASCII text-to-number converter is completely reversible.
    If this fails, the encryption is broken before it even reaches Pi!
    """
    original_message = "Hello World! 123"
    
    # 1. Convert to numbers
    number_string = text_to_numbers(original_message)
    
    # 2. Convert back to text
    recovered_message = numbers_to_text(number_string)
    
    # 3. Assert they are exactly identical
    assert original_message == recovered_message
    
    # Assert length is correct (each char should be exactly 3 digits)
    assert len(number_string) == len(original_message) * 3

def test_pi_cryption_core_engine():
    """
    Tests the actual Pi search algorithm using a known sequence.
    '1415926535' is the first 10 digits of the floating part of Pi.
    """
    target_numbers = "1415926535"
    
    # 1. Encode the numbers
    coordinates = encode_string(target_numbers)
    
    # 2. Verify it found it at index 0 (since it's the very start of the file)
    assert coordinates[0][0] == 0
    
    # 3. Decode the coordinates
    recovered_numbers = decode_coordinates(coordinates)
    
    # 4. Verify the math holds up
    assert target_numbers == recovered_numbers

def test_end_to_end_message_encryption():
    """
    Simulates a user typing a message in the CLI, encrypting it, and decrypting it.
    """
    secret_message = "PI-CRYPTION"
    
    # Encode pipeline
    num_str = text_to_numbers(secret_message)
    coords = encode_string(num_str)
    
    # Decode pipeline
    recovered_num_str = decode_coordinates(coords)
    final_message = numbers_to_text(recovered_num_str)
    
    assert secret_message == final_message

def test_encoder_rejects_letters():
    """
    The encoder should strictly reject letters since Pi only contains digits.
    """
    with pytest.raises(ValueError, match="Target must only contain digits"):
        encode_string("ABCDEFG")

def test_decoder_rejects_corrupted_data():
    """
    The text converter expects multiples of 3. It should fail on corrupted strings.
    """
    with pytest.raises(ValueError, match="Decoded number string length is not a multiple of 3"):
        numbers_to_text("12345") # 5 digits is not divisible by 3