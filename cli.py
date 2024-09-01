from rich.console import Console
import inquirer
from file_utils import list_csv_files
from data_utils import get_column_names
from plot_utils import plot_chart
import os 
console = Console()

def run_cli_app():
    console.print("Welcome to the [bold magenta]Apartment Sales Data Analysis CLI[/bold magenta]!", style="bold underline")
    
    csv_files = list_csv_files()
    
    if not csv_files:
        return
    
    csv_file_prompt = [
        inquirer.List(
            'csv_file',
            message="Choose the CSV file to analyze:",
            choices=csv_files
        )
    ]
    chosen_csv_file = inquirer.prompt(csv_file_prompt)['csv_file']
    
    try:
        file_path = os.path.join('data', chosen_csv_file)
        column_names, df = get_column_names(file_path)
    except FileNotFoundError:
        console.print(f"[red bold]Error:[/red bold] File '{chosen_csv_file}' not found.")
        return

    column_prompt = [
        inquirer.List(
            'column',
            message="Choose the column to analyze data based on:",
            choices=column_names
        )
    ]
    analyze_based_on = inquirer.prompt(column_prompt)['column']

    chart_type_prompt = [
        inquirer.List(
            'chart',
            message="Choose the chart type:",
            choices=['bar', 'pie', 'line', 'histogram', 'scatter', 'box', 'heatmap']
        )
    ]
    chart_type = inquirer.prompt(chart_type_prompt)['chart']

    # Plot the chart
    plot_chart(chart_type, df, analyze_based_on)

    # Final confirmation message
    console.print(f"\nYou chose to analyze data based on '[green]{analyze_based_on}[/green]' and visualize it with a '[blue]{chart_type}[/blue]' chart.")

if __name__ == "__main__":
    run_cli_app()
