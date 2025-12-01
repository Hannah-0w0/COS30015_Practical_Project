import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer

# 1. CONFIGURATION
# Points to your RAW SPAM folder
data_dir = r"C:\Users\Hannah\Downloads\IT Security\Practical\Practical_Spam\Project_Data\Spam"
# Output file for the table data
output_csv = os.path.join("CSV_Results", "keyword_summary.csv")

# Check if Results folder exists
if not os.path.exists("CSV_Results"):
    os.makedirs("CSV_Results")

# 2. LOAD EMAILS
emails = []
print("Scanning spam emails for keywords...")

if os.path.exists(data_dir):
    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            try:
                path = os.path.join(data_dir, filename)
                with open(path, 'r', encoding='latin-1') as f:
                    emails.append(f.read())
            except:
                pass
else:
    print(f"Error: Folder not found at {data_dir}")
    exit()

if not emails:
    print("Error: No emails found. Check your folder path!")
    exit()

# 3. FIND TOP WORDS (Bag of Words)
# We look for the top 20 words, ignoring boring ones like "the", "and"
vectorizer = CountVectorizer(stop_words='english', max_features=20)
X = vectorizer.fit_transform(emails)

# Calculate totals
sum_words = X.sum(axis=0) 
words_freq = [(word, sum_words[0, idx]) for word, idx in vectorizer.vocabulary_.items()]
words_freq = sorted(words_freq, key = lambda x: x[1], reverse=True)

# Create DataFrame
df_plot = pd.DataFrame(words_freq, columns=['Word', 'Count'])

# Save to CSV for your report
df_plot.to_csv(output_csv, index=False)
print(f"Saved keyword counts to {output_csv}")

# 4. VISUALIZE
plt.figure(figsize=(12, 8))
# Assign the plot to 'ax' so we can label it
ax = sns.barplot(x='Count', y='Word', data=df_plot, palette='Reds_r')

# NEW: Add the numbers to the end of each bar
for i in ax.containers:
    ax.bar_label(i, padding=3)

plt.title("Top 20 Words Used by Attackers (Language Analysis)", fontsize=15)
plt.xlabel("Frequency", fontsize=12)
plt.ylabel("Keyword", fontsize=12)
plt.tight_layout()

print("Displaying Keyword Chart...")
plt.show()