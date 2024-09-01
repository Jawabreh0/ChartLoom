import os
import pandas as pd
import inquirer
import matplotlib.pyplot as plt
import seaborn as sns
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

def get_column_names(file_path):
    df = pd.read_csv(file_path)
    return df.columns.tolist(), df

def plot_chart(chart_type, df, column):
    plt.figure(figsize=(10, 6))

    if chart_type == 'bar':
        df[column].value_counts().plot(kind='bar')
        plt.title(f'Bar Plot of {column}')
    elif chart_type == 'pie':
        df[column].value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title(f'Pie Chart of {column}')
    elif chart_type == 'line':
        df[column].value_counts().sort_index().plot(kind='line')
        plt.title(f'Line Plot of {column}')
    elif chart_type == 'histogram':
        df[column].plot(kind='hist', bins=10)
        plt.title(f'Histogram of {column}')
    elif chart_type == 'scatter':
        num_columns = df.select_dtypes(include='number').columns.tolist()
        scatter_y = inquirer.prompt([inquirer.List('scatter_y', message="Choose another column for Y-axis:", choices=num_columns)])['scatter_y']
        df.plot(kind='scatter', x=column, y=scatter_y)
        plt.title(f'Scatter Plot of {column} vs {scatter_y}')
    elif chart_type == 'box':
        sns.boxplot(data=df[column])
        plt.title(f'Box Plot of {column}')
    elif chart_type == 'heatmap':
        # Only works if there are multiple numeric columns
        sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
        plt.title('Heatmap of Correlations')
    
    plt.show()

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
        file_path = os.path.join(os.getcwd(), 'data', chosen_csv_file)
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
