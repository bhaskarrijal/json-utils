# JSON Scripts

Two scripts to handle JSON files organization.

## main.py
For renaming files and folders to kebab-case format. Will go through all folders recursively and rename both folders and files that need changing.

It changes stuff like:
- thisFile.json -> this-file.json
- this_file.json -> this-file.json
- ThisFile.json -> this-file.json

Just run it and enter the folder path when asked:
```
python rename.py
```

## meta.py
Generates metadata.json by scanning through directory structure. Extracts categories from folder structure and can add keywords if needed.

Run it and point it to your directory:
```
python meta.py
```

The metadata.json it generates looks like this:
```json
{
  "files": [
    {
      "filePath": "category/subcategory/file-name.json",
      "category": "category",
      "subcategory": "subcategory",
      "specialty": "",
      "name": "File Name",
      "keywords": ["keyword1", "keyword2"]  // if you add any
    }
  ]
}
```

It'll ask if you want to add keywords during the process. You can skip that part if you don't need it.