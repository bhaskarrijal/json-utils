import os
import json
from typing import Dict, List, Optional

class MetadataGenerator:
    def __init__(self, base_dir: str):
        self.base_dir = os.path.abspath(base_dir)
        self.metadata = []
        self.manual_keywords = {}
        
    def extract_path_info(self, file_path: str) -> Dict:
        """Extract category information from file path."""
        rel_path = os.path.relpath(file_path, self.base_dir)
        parts = os.path.dirname(rel_path).split(os.sep)
        
        parts = [p for p in parts if p and p != 'management']
        
        metadata = {
            "filePath": os.path.sep.join(parts + [os.path.basename(rel_path)]),
            "category": parts[0] if parts else "",
            "subcategory": parts[1] if len(parts) > 1 else "",
            "name": ""  # Will be set below
        }
        
        name = os.path.splitext(os.path.basename(file_path))[0]
        words = name.split("-")
        processed_words = []
        for word in words:
            if '(' in word or ')' in word:
                subwords = word.split()
                processed_words.extend(w.capitalize() if not (w.startswith('(') or w.endswith(')'))
                                    else w for w in subwords)
            else:
                processed_words.append(word.capitalize())
        
        metadata["name"] = " ".join(processed_words)
        
        return metadata

    def extract_json_content(self, file_path: str) -> Optional[Dict]:
        """Extract relevant information from JSON file content."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
                
            if isinstance(content, dict):
                if 'name' in content:
                    return {'name': content['name']}
                if 'title' in content:
                    return {'name': content['title']}
                    
            return None
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None

    def process_file(self, file_path: str):
        """Process a single JSON file."""
        if 'management' in os.path.relpath(file_path, self.base_dir).split(os.sep):
            return
            
        metadata = self.extract_path_info(file_path)
        
        json_content = self.extract_json_content(file_path)
        if json_content:
            metadata.update(json_content)
            
        rel_path = os.path.relpath(file_path, self.base_dir)
        if rel_path in self.manual_keywords:
            metadata['keywords'] = self.manual_keywords[rel_path]
            
        self.metadata.append(metadata)

    def process_directory(self):
        """Recursively process the directory."""
        for root, _, files in os.walk(self.base_dir):
            for file in files:
                if file.endswith('.json') and file != 'metadata.json':
                    file_path = os.path.join(root, file)
                    self.process_file(file_path)

    def add_keywords(self, file_path: str, keywords: List[str]):
        """Add manual keywords for a specific file."""
        rel_path = os.path.relpath(file_path, self.base_dir)
        self.manual_keywords[rel_path] = keywords

    def save_metadata(self, output_file: str = 'metadata.json'):
        """Save the collected metadata to a JSON file."""
        output_path = os.path.join(self.base_dir, output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'files': self.metadata
            }, f, indent=2, ensure_ascii=False)
        print(f"Metadata saved to {output_path}")

def main():
    base_dir = input("Enter the base directory path (default: 'data'): ").strip()
    if not base_dir:
        base_dir = 'data'
    
    if not os.path.isdir(base_dir):
        print(f"Error: Directory '{base_dir}' not found!")
        return

    generator = MetadataGenerator(base_dir)
    
    print("Processing files...")
    generator.process_directory()
    
    while True:
        add_keywords = input("\nWould you like to add keywords for any file? (y/n): ").lower()
        if add_keywords != 'y':
            break
            
        print("\nProcessed files:")
        for idx, meta in enumerate(generator.metadata):
            print(f"{idx + 1}. {meta['filePath']}")
            
        try:
            file_idx = int(input("\nEnter file number: ")) - 1
            if 0 <= file_idx < len(generator.metadata):
                keywords = input("Enter keywords (comma-separated): ").split(',')
                keywords = [k.strip() for k in keywords if k.strip()]
                if keywords:
                    file_path = os.path.join(base_dir, generator.metadata[file_idx]['filePath'])
                    generator.add_keywords(file_path, keywords)
                    print("Keywords added successfully!")
            else:
                print("Invalid file number!")
        except ValueError:
            print("Invalid input!")
    
    generator.save_metadata()
    print("\nMetadata generation complete!")

if __name__ == "__main__":
    main()