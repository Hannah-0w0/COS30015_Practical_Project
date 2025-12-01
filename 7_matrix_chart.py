import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# 1. CONFIGURATION
data_dir = r"C:\Users\Hannah\Downloads\IT Security\Practical\Practical_Spam\Project_Data"

# 2. LOAD THE DATA
def load_data(folder_name, label):
    path = os.path.join(data_dir, folder_name)
    emails = []
    print(f"Loading {label} emails from {path}...")
    
    for filename in os.listdir(path):
        if filename.endswith(".txt"):
            file_path = os.path.join(path, filename)
            try:
                # Use latin-1 because email headers often have weird characters
                with open(file_path, 'r', encoding='latin-1') as f:
                    emails.append(f.read())
            except Exception as e:
                print(f"Skipped {filename}: {e}")
    
    # Create a table: [Email Body, Label]
    df = pd.DataFrame(emails, columns=['text'])
    df['label'] = label # 0 for Ham, 1 for Spam
    return df

# Load both folders
print("--- Step 1: Loading Data ---")
spam_df = load_data("Spam", 1) # 1 = BAD
ham_df = load_data("Ham", 0)   # 0 = GOOD

# Combine them into one big dataset
dataset = pd.concat([spam_df, ham_df], ignore_index=True)
print(f"Total Emails Loaded: {len(dataset)}")

# 3. TRAIN THE AI MODEL
print("\n--- Step 2: Training the Model ---")

# Split data: 80% for Training (Teaching), 20% for Testing (Exam)
X_train, X_test, y_train, y_test = train_test_split(dataset['text'], dataset['label'], test_size=0.2, random_state=42)

# Convert text to numbers (Bag of Words)
# This counts how many times every word appears
vectorizer = CountVectorizer()
X_train_counts = vectorizer.fit_transform(X_train)
X_test_counts = vectorizer.transform(X_test)

# Use Naive Bayes Classifier (The Standard for Spam)
model = MultinomialNB()
model.fit(X_train_counts, y_train)
print("Model trained successfully!")

# 4. EVALUATE (THE EXAM)
print("\n--- Step 3: Evaluation Results ---")
predictions = model.predict(X_test_counts)

# Calculate Accuracy
acc = accuracy_score(y_test, predictions)
print(f"ACCURACY SCORE: {acc * 100:.2f}%")

# detailed report
print("\nClassification Report:")
print(classification_report(y_test, predictions, target_names=['Ham', 'Spam']))

# 5. GENERATE CONFUSION MATRIX 
cm = confusion_matrix(y_test, predictions)

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Ham', 'Spam'], yticklabels=['Ham', 'Spam'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix (Spam Detection)')
plt.show() # This will pop up a window