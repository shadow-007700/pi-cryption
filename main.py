import sys
import ast
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

# Ensure python knows where the root directory is to avoid ModuleNotFoundError
sys.path.append(str(Path(__file__).parent))

# Import our custom modules
from src.encoder import encode_string
from src.decoder import decode_coordinates

console = Console()

def text_to_numbers(text: str) -> str:
    """
    Converts a standard string into a continuous sequence of 3-digit ASCII numbers.
    Example: 'A' -> ord('A') is 65 -> '065'
    """
    number_string = ""
    for char in text:
        # Get the ASCII integer value and pad it with leading zeros to make it exactly 3 digits
        number_string += f"{ord(char):03d}"
    return number_string

def numbers_to_text(number_string: str) -> str:
    """
    Takes a continuous string of numbers, chunks them by 3, and converts them back to text.
    Example: '065066' -> '065', '066' -> 'A', 'B' -> 'AB'
    """
    if len(number_string) % 3 != 0:
        raise ValueError("Decoded number string length is not a multiple of 3. Data might be corrupted.")
        
    text = ""
    # Iterate through the string in steps of 3
    for i in range(0, len(number_string), 3):
        chunk = number_string[i : i+3]
        text += chr(int(chunk))
    return text

def handle_encode():
    console.print("\n[bold cyan]--- ENCODE A MESSAGE ---[/bold cyan]")
    secret_message = Prompt.ask("[bold yellow]Enter the text you want to hide in Pi[/bold yellow]")
    
    with console.status("[bold green]Converting text to numbers...[/bold green]"):
        number_string = text_to_numbers(secret_message)
        
    console.print(f"\n[dim]Converted to numerical string: {number_string}[/dim]")
    
    try:
        with console.status("[bold green]Searching 100M digits of Pi (Greedy Binary Search)...[/bold green]"):
            coordinates = encode_string(number_string)
            
        console.print(Panel(
            f"[bold green]Success![/bold green]\n\n"
            f"[bold white]Your Coordinates:[/bold white]\n{coordinates}\n\n"
            f"[dim]Total chunks used: {len(coordinates)}[/dim]",
            title="Encryption Complete",
            border_style="green",
            expand=False
        ))
    except Exception as e:
        console.print(f"[bold red]Error during encoding:[/bold red] {e}")

def handle_decode():
    console.print("\n[bold cyan]--- DECODE A MESSAGE ---[/bold cyan]")
    console.print("[dim]Paste your coordinates list exactly as it was given (e.g., [(123, 4), (567, 8)])[/dim]")
    coords_input = Prompt.ask("[bold yellow]Enter coordinates[/bold yellow]")
    
    try:
        # Safely evaluate the string representation of the list into an actual Python list of tuples
        coordinates = ast.literal_eval(coords_input)
        
        with console.status("[bold green]Fetching chunks from the Pi database...[/bold green]"):
            recovered_numbers = decode_coordinates(coordinates)
            
        with console.status("[bold green]Converting numbers back to text...[/bold green]"):
            final_message = numbers_to_text(recovered_numbers)
            
        console.print(Panel(
            f"[bold green]Message Recovered![/bold green]\n\n"
            f"[bold white]Secret Text:[/bold white] {final_message}",
            title="Decryption Complete",
            border_style="cyan",
            expand=False
        ))
    except Exception as e:
        console.print(f"[bold red]Error during decoding. Make sure your coordinates format is exactly right![/bold red]\n[dim]{e}[/dim]")

def main():
    # Clear the terminal screen slightly and print a cool banner
    console.print("\n" * 2)
    banner = Text(" π-CRYPTION TERMINAL ", style="bold black on green", justify="center")
    console.print(banner)
    console.print("[italic green]Hide your secrets in the infinite decimals of Pi.[/italic green]\n", justify="center")
    
    while True:
        console.print("\n[bold]Select an operation:[/bold]")
        console.print("  [bold cyan]1.[/bold cyan] Encode a secret message")
        console.print("  [bold cyan]2.[/bold cyan] Decode map coordinates")
        console.print("  [bold red]3.[/bold red] Exit")
        
        choice = Prompt.ask("\n[bold yellow]Choice[/bold yellow]", choices=["1", "2", "3"])
        
        if choice == "1":
            handle_encode()
        elif choice == "2":
            handle_decode()
        else:
            console.print("\n[bold green]Shutting down π-cryption. Goodbye![/bold green]\n")
            sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[bold red]Operation cancelled by user. Exiting...[/bold red]")
        sys.exit(0)