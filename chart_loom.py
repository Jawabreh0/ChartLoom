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

def get_grouped_data(df, selected_columns):
    grouped_df = df.groupby(selected_columns).size().reset_index(name='counts')
    return grouped_df

def plot_chart(chart_type, df, column, group_columns=None):
    plt.figure(figsize=(10, 6))

    if group_columns:
        df = get_grouped_data(df, group_columns)
        column = 'counts'  # Use the 'counts' column for grouped data

    if chart_type == 'bar':
        df[column].plot(kind='bar')
        plt.title(f'Bar Plot of {column}')
    elif chart_type == 'pie':
        df[column].plot(kind='pie', autopct='%1.1f%%')
        plt.title(f'Pie Chart of {column}')
    elif chart_type == 'line':
        df[column].plot(kind='line')
        plt.title(f'Line Plot of {column}')
    elif chart_type == 'histogram':
        df[column].plot(kind='hist', bins=10)
        plt.title(f'Histogram of {column}')
    elif chart_type == 'scatter':
        num_columns = df.select_dtypes(include='number').columns.tolist()
        scatter_y = inquirer.prompt([inquirer.List('scatter_y', message="Choose another column for Y-axis:", choices=num_columns)])['scatter_y']
        df.plot(kind='scatter', x=group_columns[0], y=scatter_y)
        plt.title(f'Scatter Plot of {group_columns[0]} vs {scatter_y}')
    elif chart_type == 'box':
        sns.boxplot(data=df[column])
        plt.title(f'Box Plot of {column}')
    elif chart_type == 'heatmap':
        sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
        plt.title('Heatmap of Correlations')

    plt.show()

def run_cli_app():
    console.print("Welcome to the [bold magenta]ChartLoom Data Analysis CLI[/bold magenta]!", style="bold underline")
    
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

    group_columns_prompt = [
        inquirer.Checkbox(
            'group_columns',
            message="Choose the columns to group data by (you can select multiple):",
            choices=column_names
        )
    ]
    group_columns = inquirer.prompt(group_columns_prompt)['group_columns']

    if not group_columns:
        console.print("[red bold]Error:[/red bold] You must select at least one column to analyze.")
        return

    chart_type_prompt = [
        inquirer.List(
            'chart',
            message="Choose the chart type:",
            choices=['bar', 'pie', 'line', 'histogram', 'scatter', 'box', 'heatmap']
        )
    ]
    chart_type = inquirer.prompt(chart_type_prompt)['chart']

    # Plot the chart
    plot_chart(chart_type, df, group_columns[0], group_columns=group_columns if len(group_columns) > 1 else None)

    # Final confirmation message
    console.print(f"\nYou chose to analyze data based on '[green]{', '.join(group_columns)}[/green]' and visualize it with a '[blue]{chart_type}[/blue]' chart.")

if __name__ == "__main__":
    run_cli_app()
