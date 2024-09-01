import pandas as pd
import matplotlib.pyplot as plt

file_path = 'dovec-properties.csv' 
df = pd.read_csv(file_path)

flattype_counts = df['flattype'].value_counts()

if flattype_counts.empty:
    print("No apartments found in the dataset.")
else:
    # Plot the results
    plt.figure(figsize=(10, 6))
    flattype_counts.plot(kind='bar', color='skyblue')
    plt.title('Best Selling Apartment Types in North Cyprus')
    plt.xlabel('Apartment Type')
    plt.ylabel('Number Sold')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
