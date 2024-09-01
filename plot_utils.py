import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from rich.console import Console

console = Console()

def plot_chart(chart_type, df, column, ax=None):
    if ax is None:
        ax = plt.gca()  # Get the current axis if none is provided

    if chart_type == 'pie':
        counts = df[column].value_counts()
        total = counts.sum()

        def custom_autopct(pct):
            return f'{pct:.1f}%' if pct >= 2.5 else ''

        wedges, texts, autotexts = ax.pie(counts, labels=None, autopct=custom_autopct, pctdistance=0.85)
        ax.set_title(f'Pie Chart of {column}')
        ax.add_artist(plt.Circle((0, 0), 0.70, fc='white'))

        for i, (wedge, text) in enumerate(zip(wedges, autotexts)):
            pct = 100 * (wedge.theta2 - wedge.theta1) / 360
            if pct < 2.5:
                angle = (wedge.theta2 + wedge.theta1) / 2
                x = wedge.r * np.cos(np.radians(angle))
                y = wedge.r * np.sin(np.radians(angle))
                text.set_position((x, y))

        ax.legend(counts.index, bbox_to_anchor=(1.05, 1), loc='upper left')

    elif chart_type == 'bar':
        df[column].value_counts().plot(kind='bar', ax=ax)
        ax.set_title(f'Bar Plot of {column}')
        ax.set_xlabel(column)
        ax.set_ylabel('Count')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

    elif chart_type == 'line':
        counts = df[column].value_counts().sort_index()
        counts.plot(kind='line', marker='o', ax=ax)
        ax.set_title(f'Line Plot of {column}')
        ax.set_xlabel(column)
        ax.set_ylabel('Count')
        ax.set_xticks(range(len(counts.index)))
        ax.set_xticklabels(counts.index, rotation=45, ha='right')

    elif chart_type == 'histogram':
        if df[column].dtype.kind in 'if':
            df[column].plot(kind='hist', bins=10, ax=ax)
            ax.set_title(f'Histogram of {column}')
            ax.set_xlabel(column)
            ax.set_ylabel('Frequency')
        else:
            console.print(f"[red bold]Error:[/red bold] Column {column} is not numeric, cannot plot histogram.")
            return

    elif chart_type == 'scatter':
        num_columns = df.select_dtypes(include='number').columns.tolist()
        if num_columns:
            scatter_y = inquirer.prompt([inquirer.List('scatter_y', message="Choose another column for Y-axis:", choices=num_columns)])['scatter_y']
            df.plot(kind='scatter', x=column, y=scatter_y, ax=ax)
            ax.set_title(f'Scatter Plot of {column} vs {scatter_y}')
            ax.set_xlabel(column)
            ax.set_ylabel(scatter_y)
        else:
            console.print(f"[red bold]Error:[/red bold] No numeric columns available for scatter plot Y-axis.")
            return
