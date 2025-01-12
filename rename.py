import os
import re

def convert_to_kebab_case(name):
    """Convert a string to kebab-case."""
    # extension cha bhane hataune
    base_name = os.path.splitext(name)[0]
    
    # dot lai space ma convert garne
    base_name = base_name.replace('.', ' ')
    
    # camelCase lai space ma convert garne
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', base_name)
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1)
    
    # lowercase ma convert garne ani space lai dash ma convert garne
    kebab_case = s2.strip().lower().replace(' ', '-').replace('_', '-')
    
    # hypen ko dups hataune
    kebab_case = re.sub('-+', '-', kebab_case)
    
    # extension add garne
    if name.lower().endswith('.json'):
        kebab_case += '.json'
    
    return kebab_case

def process_directory(directory_path):
    """
    Recursively process all files and folders in the given directory.
    """
    try:
        # directory ko content haru lai list ma store garne
        items = os.listdir(directory_path)
        
        # sabai subdirectories lai process garne
        for item in items:
            full_path = os.path.join(directory_path, item)
            if os.path.isdir(full_path):
                process_directory(full_path)
                
                # paryo bhane rename garne
                new_name = convert_to_kebab_case(item)
                if new_name != item:
                    new_path = os.path.join(directory_path, new_name)
                    try:
                        os.rename(full_path, new_path)
                        print(f"Renamed directory: {full_path} -> {new_path}")
                    except OSError as e:
                        print(f"Error renaming directory {full_path}: {e}")
        
        # prpcessing goes brrrrrr
        for item in os.listdir(directory_path):  # Get fresh list after dir renames
            full_path = os.path.join(directory_path, item)
            if os.path.isfile(full_path) and item.lower().endswith('.json'):
                new_name = convert_to_kebab_case(item)
                if new_name != item:
                    new_path = os.path.join(directory_path, new_name)
                    try:
                        os.rename(full_path, new_path)
                        print(f"Renamed file: {full_path} -> {new_path}")
                    except OSError as e:
                        print(f"Error renaming file {full_path}: {e}")
                        
    except Exception as e:
        print(f"Error processing directory {directory_path}: {e}")

def main():
    directory_path = input("Enter the directory path to process: ").strip()
    
    if not os.path.isdir(directory_path):
        print(f"Error: '{directory_path}' is not a valid directory")
        return
    
    print(f"Processing directory: {directory_path}")
    process_directory(directory_path)
    print("Processing complete!")

if __name__ == "__main__":
    main()