import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# 1. TRAIN ON OLD DATA (The 2002 Baseline)
data_dir = r"C:\Users\Hannah\Downloads\IT Security\Practical\Practical_Spam\Project_Data"
emails = []
labels = []
print("Training Baseline Model on 2002 Data...")
for folder, label in [("Spam", 1), ("Ham", 0)]: 
    path = os.path.join(data_dir, folder)
    for filename in os.listdir(path): 
        try:
            with open(os.path.join(path, filename), 'r', encoding='latin-1') as f:
                emails.append(f.read())
                labels.append(label)
        except: pass

vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(emails)
model = MultinomialNB()
model.fit(X_train, labels)

# 2. TEST ON MODERN DATA (2024/2025)
modern_dir = r"C:\Users\Hannah\Downloads\IT Security\Practical\Practical_Spam\Project_Data\JunkEmail"
print("\nTesting Kaggle Spam Dataset...")

if not os.path.exists(modern_dir):
    print(f"CRITICAL: You need to create the folder {modern_dir} and put .txt files in it!")
else:
    for filename in os.listdir(modern_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(modern_dir, filename), 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
                # Vectorize just this one file
                vec_text = vectorizer.transform([text])
                prediction = model.predict(vec_text)[0]
                result = "DETECTED (Success)" if prediction == 1 else "MISSED (Failure)"
                print(f"File: {filename} -> {result}")