## ModifyJSON

A simple Python utility for modifying JSON files with support for:
- Adding new values
- Replacing existing values
- Removing keys and values
- Handling deeply nested JSON structures using bracket notation
- Command line and programmatic interfaces

### Usage

```python
from modify_json import modify_json_files

# Example usage
modify_json_files('path/to/json/file.json', '[settings][newSetting]', '42', 'add')
```

The script can also be run from the command line. 

```bash
python modify_json.py --add "path/to/json/file.json" "[settings][newSetting]" 42
```