from rich.console import Console
import inquirer
from file_utils import list_csv_files
from data_utils import get_column_names
from plot_utils import plot_chart
import os
import matplotlib.pyplot as plt

console = Console()

def run_cli_app():
    console.print("\n\n\n\tChartLoom Data Analysis and Chart Plotting Tool \n\n\n")
    
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

    # Option prompt: Chart or Statistics
    analysis_option_prompt = [
        inquirer.List(
            'analysis_option',
            message="What would you like to do?",
            choices=['chart', 'statistics']
        )
    ]
    analysis_option = inquirer.prompt(analysis_option_prompt)['analysis_option']

    if analysis_option == 'chart':
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

    elif analysis_option == 'statistics':
        column_prompt = [
            inquirer.Checkbox(
                'columns',
                message="Choose the columns to analyze data based on:",
                choices=column_names
            )
        ]
        analyze_based_on = inquirer.prompt(column_prompt)['columns']

        top_n_prompt = [
            inquirer.List(
                'top_n',
                message="How many top results do you want to see?",
                choices=['1', '3', '5', '10']
            )
        ]
        top_n = int(inquirer.prompt(top_n_prompt)['top_n'])

        # Calculate the top N results
        grouped_df = df.groupby(analyze_based_on).size().reset_index(name='count')
        top_results = grouped_df.nlargest(top_n, 'count')

        console.print(f"\nTop {top_n} results based on {[f'[green]{col}[/green]' for col in analyze_based_on]}:")
        for i, row in enumerate(top_results.itertuples(index=False), 1):
            console.print(f"{i}. {dict(zip(analyze_based_on, row[:-1]))}: {row[-1]} times")

        # Prompt to plot the results
        plot_prompt = [
            inquirer.Confirm(
                'plot_results',
                message="Would you like to plot these results?",
                default=False
            )
        ]
        plot_results = inquirer.prompt(plot_prompt)['plot_results']

        if plot_results:
            # Choose chart type for plotting
            chart_type_prompt = [
                inquirer.List(
                    'chart_type',
                    message="Choose the chart type to plot the results:",
                    choices=['bar', 'pie', 'line', 'histogram', 'scatter']
                )
            ]
            chart_type = inquirer.prompt(chart_type_prompt)['chart_type']

            fig, ax = plt.subplots(figsize=(8, 6))
            plot_chart(chart_type, top_results, analyze_based_on, ax)
            plt.tight_layout()
            plt.show()

if __name__ == "__main__":
    run_cli_app()
