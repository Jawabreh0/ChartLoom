import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/dovec-properties.csv')

date_columns = ['flatdate', 'depositotime', 'soldtime']
for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors='coerce')

df['days_deposit_to_sold'] = (df['soldtime'] - df['depositotime']).dt.days

grouped = df.groupby('flattype').agg({
    'days_deposit_to_sold': ['mean', 'median', 'std', 'count'],
    'flattype': 'count'
}).reset_index()

grouped.columns = ['flattype', 'avg_days', 'median_days', 'std_days', 'count_deposit_to_sold', 'total_units']

fastest_selling = grouped.sort_values('median_days')

plt.figure(figsize=(15, 7))
bars = plt.bar(fastest_selling['flattype'], fastest_selling['median_days'], alpha=0.8)
plt.xlabel('Property Type')
plt.ylabel('Median Days to Sell')
plt.title('Fastest Selling Property Types in North Cyprus')
plt.xticks(rotation=45, ha='right')

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.0f}',
             ha='center', va='bottom')

plt.savefig('fastest_selling_chart.png', bbox_inches='tight')
plt.close()

plt.figure(figsize=(10, 8))
plt.pie(fastest_selling['count_deposit_to_sold'], labels=fastest_selling['flattype'], autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.title('Distribution of Fastest Selling Properties by Type')
plt.savefig('fastest_selling_pie_chart.png', bbox_inches='tight')
plt.close()

most_sold = grouped.sort_values('total_units', ascending=False)

plt.figure(figsize=(15, 7))
bars = plt.bar(most_sold['flattype'], most_sold['total_units'], alpha=0.8)
plt.xlabel('Property Type')
plt.ylabel('Total Units Sold')
plt.title('Most Sold Property Types in North Cyprus')
plt.xticks(rotation=45, ha='right')

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.0f}',
             ha='center', va='bottom')

plt.savefig('most_sold_chart.png', bbox_inches='tight')
plt.close()

plt.figure(figsize=(10, 8))
plt.pie(most_sold['total_units'], labels=most_sold['flattype'], autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.title('Distribution of Most Sold Properties by Type')
plt.savefig('most_sold_pie_chart.png', bbox_inches='tight')
plt.close()

fastest_selling.to_csv('fastest_selling_properties.csv', index=False)
most_sold.to_csv('most_sold_properties.csv', index=False)

print("Fastest Selling Property Types:")
print(fastest_selling[['flattype', 'median_days', 'count_deposit_to_sold']])

print("\nMost Sold Property Types:")
print(most_sold[['flattype', 'total_units']])

print("\nAnalysis complete. Results saved to 'fastest_selling_properties.csv' and 'most_sold_properties.csv'")
print("Visualizations saved as 'fastest_selling_chart.png', 'fastest_selling_pie_chart.png', 'most_sold_chart.png', and 'most_sold_pie_chart.png'")