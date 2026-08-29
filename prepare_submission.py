import os
import shutil

def prepare_submission():
    base_dir = "Final_Submission_Ready"
    
    # Define the required folder structure
    folders = {
        "Dataset": ["cases.csv"],
        "Human Reviewer": ["responsible_ai_log.md"],
        "Python files - tools": ["app.py", "rule_checker.py", "generate_cases.py"],
        "Evidence files": ["diagnose_prompt.md"],
        "Other project-related files": ["index.html", "NetSage_AI_Final_Report.md"]
    }
    
    # Create base directory
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
    os.makedirs(base_dir)
    
    print(f"Creating organized submission folder: '{base_dir}'...")
    
    # Create subfolders and copy files
    for folder_name, files in folders.items():
        folder_path = os.path.join(base_dir, folder_name)
        os.makedirs(folder_path)
        
        for file in files:
            if os.path.exists(file):
                shutil.copy(file, os.path.join(folder_path, file))
                print(f"  Copied {file} -> {folder_name}/")
            else:
                print(f"  Warning: {file} not found!")

    print("\n✅ Success! All files have been organized.")
    print("Next Steps:")
    print("1. If you created a .pkt file, copy it into the 'Other project-related files' folder.")
    print(f"2. Right-click the '{base_dir}' folder and select 'Compress to ZIP file'.")
    print("3. Upload the ZIP file to your college TPO portal.")

if __name__ == "__main__":
    prepare_submission()
