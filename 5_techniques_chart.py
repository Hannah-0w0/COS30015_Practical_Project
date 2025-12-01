import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

# 1. CONFIGURATION
spam_folder = r"C:\Users\Hannah\Downloads\IT Security\Practical\Practical_Spam\Project_Data\Spam"
output_folder = "CSV_Results"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 2. DEFINE TECHNIQUES
techniques = {
    "HTML Obfuscation": [r"<html>", r"<font", r"<br>", r"<td>", r"<div>", r"<table>"], 
    "CSS Hiding": [r"display:\s*none", r"visibility:\s*hidden", r"font-size:\s*0", r"color:\s*#ffffff"],
    "Base64/Encoding": [r"content-transfer-encoding:\s*base64", r"quoted-printable", r"utf-7"],
    "Image-Based Spam": [r"content-type:\s*image", r"<img", r"src=\"cid:", r"\.jpg", r"\.png", r"\.gif"],
    "URL Shorteners": [r"bit\.ly", r"tinyurl", r"goo\.gl", r"owl\.li", r"deck\.ly"], 
    "Scripting/ActiveX": [r"<script>", r"javascript", r"vbscript", r"onclick", r"onload"], 
    "IP-Based Links": [r"http://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"], 
    "Urgency Triggers": [r"urgent", r"immediate", r"account", r"verify", r"suspended", r"24 hours"] 
}

results = []
print("Scanning for Evasion Techniques...")

# 3. SCAN EMAILS
if os.path.exists(spam_folder):
    for filename in os.listdir(spam_folder):
        if filename.endswith(".txt"):
            try:
                with open(os.path.join(spam_folder, filename), 'r', encoding='latin-1') as f:
                    content = f.read().lower()
                    
                detected_tech = "Plain Text" 
                
                for tech, patterns in techniques.items():
                    for pattern in patterns:
                        if re.search(pattern, content):
                            detected_tech = tech
                            break
                    if detected_tech != "Plain Text":
                        break
                
                results.append({"Filename": filename, "Technique": detected_tech})
            except:
                pass

# 4. SAVE & VISUALIZE
df = pd.DataFrame(results)

# --- NEW: SAVE THE FULL LIST ---
df.to_csv(os.path.join(output_folder, "all_technique_lists.csv"), index=False)
print(f"Saved full list to {output_folder}\\all_technique_lists.csv")

# --- SUMMARY LOGIC ---
found_counts = df['Technique'].value_counts()
all_categories = list(techniques.keys()) + ["Plain Text"]
tech_counts = found_counts.reindex(all_categories, fill_value=0).reset_index()
tech_counts.columns = ['Technique', 'Count']
tech_counts = tech_counts.sort_values(by='Count', ascending=False)

# Save Summary
tech_counts.to_csv(os.path.join(output_folder, "technique_summary.csv"), index=False)

# Chart
plt.figure(figsize=(12, 8))
ax = sns.barplot(x='Count', y='Technique', data=tech_counts, palette='coolwarm')

for i in ax.containers:
    ax.bar_label(i, padding=3)

plt.title("Detected Evasion Techniques (Including 0 Hits)", fontsize=15)
plt.xlabel("Number of Emails", fontsize=12)
plt.tight_layout()
plt.show()