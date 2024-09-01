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
        plt.xticks(rotation=45, ha='right')  
        plt.tight_layout()
        plt.tight_layout()


    elif chart_type == 'pie':
        counts = df[column].value_counts()  
        autopct = lambda p: f'{p:.1f}%' if p >= 2.5 else ''
        plt.pie(counts, labels=None, autopct=autopct, pctdistance=0.85)
        plt.title(f'Pie Chart of {column}')
        plt.gca().add_artist(plt.Circle((0,0),0.70,fc='white'))  
        plt.legend(counts.index, bbox_to_anchor=(1.05, 1), loc='upper left')  
        plt.tight_layout()

        
    elif chart_type == 'line':
        df[column].value_counts().sort_index().plot(kind='line', marker='o')  # Add markers to highlight points
        plt.title(f'Line Plot of {column}')
        plt.xlabel(column)
        plt.ylabel('Count')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()


    elif chart_type == 'histogram':
        if df[column].dtype.kind in 'if':  # Check if the column is numeric
            df[column].plot(kind='hist', bins=10)
            plt.title(f'Histogram of {column}')
            plt.xlabel(column)
            plt.ylabel('Frequency')
        else:
            console.print(f"[red bold]Error:[/red bold] Column {column} is not numeric, cannot plot histogram.")
            return


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

    
    plt.show()
