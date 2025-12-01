import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# 1. SETUP
data_dir = r"C:\Users\Hannah\Downloads\IT Security\Practical\Practical_Spam\Project_Data"
emails = []
labels = []
filenames_list = [] 

# 2. LOAD DATA (Order: Spam then Ham)
print("Loading data...")
for folder, label in [("Spam", 1), ("Ham", 0)]: 
    path = os.path.join(data_dir, folder)
    for filename in sorted(os.listdir(path)): 
        if filename.endswith(".txt"):
            try:
                with open(os.path.join(path, filename), 'r', encoding='latin-1') as f:
                    emails.append(f.read())
                    labels.append(label)
                    filenames_list.append(filename)
            except: pass

# 3. RETRAIN MODEL
print("Training model...")
X_train, X_test, y_train, y_test, files_train, files_test = train_test_split(
    emails, labels, filenames_list, test_size=0.2, random_state=42
)

vectorizer = CountVectorizer()
X_train_counts = vectorizer.fit_transform(X_train)
X_test_counts = vectorizer.transform(X_test)
model = MultinomialNB()
model.fit(X_train_counts, y_train)
predictions = model.predict(X_test_counts)

# 4. GATHER ERRORS (Dynamic Calculation)
fp_list = [] # Store False Positives here
fn_list = [] # Store False Negatives here

for text, true_lbl, pred_lbl, fname in zip(X_test, y_test, predictions, files_test):
    if true_lbl == 0 and pred_lbl == 1:
        fp_list.append((fname, text))
    elif true_lbl == 1 and pred_lbl == 0:
        fn_list.append((fname, text))

# 5. PRINT THE SUMMARY REPORT
print("\n" + "="*50)
print("       MISCLASSIFICATION REPORT")
print("="*50)
print(f"Total Emails Tested:  {len(y_test)}")
print(f"False Negatives (Spam -> Ham): {len(fn_list)}")
print(f"False Positives (Ham -> Spam): {len(fp_list)}")
print("="*50)

# 6. PRINT FALSE POSITIVE DETAILS
print("\n" + "-"*50)
print(f"DETAILS: FALSE POSITIVES ({len(fp_list)} Found)")
print("-"*50)

if fp_list:
    for fname, content in fp_list:
        print(f"FILE NAME: {fname}")
        print("CONTENT PREVIEW:")
        # Print first 3 lines
        lines = content.split('\n')
        for line in lines[:3]:
            print(line)
        print("...")
else:
    print("None found.")

# 7. PRINT FALSE NEGATIVE DETAILS (ALL OF THEM)
print("\n" + "-"*50)
print(f"DETAILS: FALSE NEGATIVES ({len(fn_list)} Found)")
print("-"*50)

if fn_list:
    for i, (fname, content) in enumerate(fn_list):
        # Format: [1] filename.txt ... content snippet ...
        # Removing newlines from content snippet to keep it on one line
        clean_content = content[:80].replace('\n', ' ').replace('\r', '')
        print(f"[{i+1}] {fname} -> {clean_content}...")
else:
    print("None found.")

# 8. SAVE RESULTS TO CSV (New Feature)
csv_path = os.path.join(data_dir, "..", "CSV_Results", "misclassification_report.csv")

# Create a list of dictionaries for the CSV
csv_data = []

# Add False Positives
for fname, content in fp_list:
    csv_data.append({
        "Type": "False Positive (Safe marked as Spam)",
        "Filename": fname,
        "Content_Snippet": content[:100].replace('\n', ' ')
    })

# Add False Negatives
for fname, content in fn_list:
    csv_data.append({
        "Type": "False Negative (Spam marked as Safe)",
        "Filename": fname,
        "Content_Snippet": content[:100].replace('\n', ' ')
    })

# Save using Pandas
if csv_data:
    df_errors = pd.DataFrame(csv_data)
    df_errors.to_csv(csv_path, index=False)
    print(f"\n[SUCCESS] Detailed error report saved to: {csv_path}")
else:
    print("\n[INFO] No errors found, so no CSV was created.")
