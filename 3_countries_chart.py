import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. CONFIGURATION
input_csv = os.path.join("CSV_Results", "trace_results.csv")
output_csv = os.path.join("CSV_Results", "country_summary.csv")

# 2. LOAD DATA
try:
    df = pd.read_csv(input_csv)
except FileNotFoundError:
    print(f"Error: Could not find {input_csv}.")
    exit()

# 3. PROCESS DATA
# Count the countries
country_counts = df['Country'].value_counts()

# Save ALL country counts to a CSV for your report table
country_counts.to_csv(output_csv, header=["Count"])
print(f"Saved country counts to {output_csv}")

# Take just the top 10 for the chart
top_countries = country_counts.head(10)

# 4. VISUALIZE
plt.figure(figsize=(12, 7))
# Create the bar plot and save it to a variable 'ax' so we can modify it
ax = sns.barplot(x=top_countries.values, y=top_countries.index, palette="viridis")

# NEW: Add the numbers to the end of each bar
for i in ax.containers:
    ax.bar_label(i, padding=3)

plt.title("Top 10 Sources of Spam (Trace Results)", fontsize=15)
plt.xlabel("Number of Emails", fontsize=12)
plt.ylabel("Country", fontsize=12)
plt.tight_layout()

print("Displaying Country Chart...")
plt.show()