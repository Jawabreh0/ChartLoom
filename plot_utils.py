import matplotlib.pyplot as plt
import seaborn as sns
import inquirer
from rich.console import Console

console = Console()

def plot_chart(chart_type, df, column):
    plt.figure(figsize=(10, 6))

    if chart_type == 'bar':
        df[column].value_counts().plot(kind='bar')
        plt.title(f'Bar Plot of {column}')
        plt.xlabel(column)
        plt.ylabel('Count')
    elif chart_type == 'pie':
        df[column].value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title(f'Pie Chart of {column}')
    elif chart_type == 'line':
        df[column].value_counts().sort_index().plot(kind='line')
        plt.title(f'Line Plot of {column}')
        plt.xlabel(column)
        plt.ylabel('Count')
    elif chart_type == 'histogram':
        df[column].plot(kind='hist', bins=10)
        plt.title(f'Histogram of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
    elif chart_type == 'scatter':
        num_columns = df.select_dtypes(include='number').columns.tolist()
        if num_columns:
            scatter_y = inquirer.prompt([inquirer.List('scatter_y', message="Choose another column for Y-axis:", choices=num_columns)])['scatter_y']
            df.plot(kind='scatter', x=column, y=scatter_y)
            plt.title(f'Scatter Plot of {column} vs {scatter_y}')
            plt.xlabel(column)
            plt.ylabel(scatter_y)
        else:
            console.print(f"[red bold]Error:[/red bold] No numeric columns available for scatter plot Y-axis.")
            return
    elif chart_type == 'box':
        sns.boxplot(data=df[column])
        plt.title(f'Box Plot of {column}')
    elif chart_type == 'heatmap':
        sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
        plt.title('Heatmap of Correlations')
    
    plt.show()
