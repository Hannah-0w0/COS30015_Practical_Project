import os

base_path = r"C:\Users\Hannah\Downloads\IT Security\Practical\Practical_Spam\Project_Data"

def rename_to_txt(directory):
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Skip files that are already .txt or system files
            if file.endswith(".txt") or file.startswith("."):
                continue
            
            old_path = os.path.join(root, file)
            new_path = os.path.join(root, file + ".txt")
            
            try:
                os.rename(old_path, new_path)
                count += 1
            except OSError as e:
                print(f"Error renaming {file}: {e}")
    
    print(f"Success! Renamed {count} files in {directory}")

# Run for both folders
rename_to_txt(os.path.join(base_path, "Spam"))
rename_to_txt(os.path.join(base_path, "Ham"))