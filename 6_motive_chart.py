import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. CONFIGURATION
# Input Folder (Raw Data)
spam_folder = r"C:\Users\Hannah\Downloads\IT Security\Practical\Practical_Spam\Project_Data\Spam"

# Output Folder (New Name)
output_folder = "CSV_Results"

# Auto-create the output folder if missing
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Created new folder: {output_folder}")


# 2. DICTIONARY OF MOTIVES & KEYWORDS
# Each motive has a list of keywords to search for
motives = {
    "Phishing (Account Theft)": ["verify", "account", "login", "password", "security", "update", "confirm", "suspended", "alert"],
    "Financial Scam (419)": ["prince", "inheritance", "transfer", "funds", "million", "dollars", "capital", "investment", "beneficiary"],
    "Malware/Ransomware": ["invoice", "receipt", "document", "attached", "file", "download", "tracking", "shipment", "pdf", "zip"],
    "Sextortion/Blackmail": ["bitcoin", "recorded", "webcam", "evidence", "wallet", "exposed", "hack", "video", "footage"],
    "Promotional/Ads": ["viagra", "pills", "casino", "free", "bonus", "winner", "offer", "click", "buy", "discount"],
    "Job Scams": ["hiring", "resume", "salary", "employment", "work from home", "part-time", "representative"]
}

results = []
print("Analyzing Motives...")


# 3. SCANNING PROCESS
if os.path.exists(spam_folder):
    for filename in os.listdir(spam_folder):
        if filename.endswith(".txt"):
            try:
                with open(os.path.join(spam_folder, filename), 'r', encoding='latin-1') as f:
                    content = f.read().lower()
                    
                detected_motive = "Uncategorized"
                for category, keywords in motives.items():
                    for word in keywords:
                        if word in content:
                            detected_motive = category
                            break
                    if detected_motive != "Uncategorized":
                        break
                
                results.append({"Filename": filename, "Motive": detected_motive})
            except Exception as e:
                pass
else:
    print(f"Error: Raw data folder not found at {spam_folder}")
    exit()

if not results:
    print("No emails found to analyze.")
    exit()


# 4. SAVE RESULTS & VISUALIZE
df = pd.DataFrame(results)

# A. Save the Raw List (Which file is what)
# Using 'r' before the string handles backslashes safely
df.to_csv(os.path.join(output_folder, "all_motive_lists.csv"), index=False)
print("Saved raw list to 'CSV_Results\\all_motive_lists.csv'")

# B. Save the COUNTS
motive_counts = df['Motive'].value_counts().reset_index()
motive_counts.columns = ['Motive', 'Count']
motive_counts.to_csv(os.path.join(output_folder, "motive_summary.csv"), index=False)
print("Saved exact numbers to 'CSV_Results\\motive_summary.csv'")

# C. Create the Chart with Numbers
plt.figure(figsize=(12, 8))

# We plot using the 'motive_counts' dataframe because it's cleaner for labels
ax = sns.barplot(x='Count', y='Motive', data=motive_counts, palette='magma')

# NEW: Add the numbers to the end of each bar
for i in ax.containers:
    ax.bar_label(i, padding=3)

plt.title("Attacker Motive Analysis (Keyword Based)", fontsize=16)
plt.xlabel("Number of Emails", fontsize=12)
plt.ylabel("Detected Motive", fontsize=12)
plt.tight_layout()

print("Displaying Motive Chart...")
plt.show()