import os
from rich.console import Console

console = Console()

def list_csv_files():
    data_dir = os.path.join(os.getcwd(), 'data')
    
    if not os.path.exists(data_dir):
        console.print(f"[red bold]Error:[/red bold] The 'data' directory does not exist.")
        return []
    
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    
    if not csv_files:
        console.print(f"[red bold]Error:[/red bold] No CSV files found in the 'data' directory.")
        return []
    
    return csv_files
