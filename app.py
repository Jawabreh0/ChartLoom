from rich.console import Console
import inquirer
from file_utils import list_csv_files
from data_utils import get_column_names
from plot_utils import plot_chart
import os
import matplotlib.pyplot as plt

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

    num_charts_prompt = [
        inquirer.List(
            'num_charts',
            message="How many charts do you want to plot (1-4)?",
            choices=['1', '2', '3', '4']
        )
    ]
    num_charts = int(inquirer.prompt(num_charts_prompt)['num_charts'])

    chart_types = []
    for i in range(num_charts):
        chart_type_prompt = [
            inquirer.List(
                f'chart_{i+1}',
                message=f"Choose the chart type for chart {i+1}:",
                choices=['bar', 'pie', 'line', 'histogram', 'scatter']
            )
        ]
        chart_type = inquirer.prompt(chart_type_prompt)[f'chart_{i+1}']
        chart_types.append(chart_type)

    fig, axes = plt.subplots(1, num_charts, figsize=(5 * num_charts, 6))

    if num_charts == 1:
        plot_chart(chart_types[0], df, analyze_based_on, axes)
    else:
        for i, chart_type in enumerate(chart_types):
            plot_chart(chart_type, df, analyze_based_on, axes[i])

    plt.tight_layout()
    plt.show()

    console.print(f"\nYou chose to analyze data based on '[green]{analyze_based_on}[/green]' and visualize it with the following chart types: {[f'[blue]{ct}[/blue]' for ct in chart_types]}.")

if __name__ == "__main__":
    run_cli_app()
