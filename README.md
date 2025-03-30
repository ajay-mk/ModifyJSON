## ModifyJSON

A simple Python utility for modifying JSON files with support for:
- Adding new values
- Replacing existing values
- Removing keys and values
- Handling deeply nested JSON structures using bracket notation
- Command line and programmatic interfaces
- Writing modified JSON to a new file without altering the original file

### Usage

```python
from modify_json import modify_json_files

# Example usage
modify_json_files('path/to/json/file.json', '[settings][newSetting]', '42', 'add')
```

#### Command Line Interface

The script can also be run from the command line.

```bash
python modify_json.py --add "path/to/json/file.json" "[settings][newSetting]" 42
```

#### Writing to a New File

To save the modified JSON to a new file instead of overwriting the original, use the `--output-file` option:

```bash
python modify_json.py --add "path/to/json/file.json" "[settings][newSetting]" 42 --output-file "path/to/output.json"
```

This will save the modified JSON to `path/to/output.json` without altering the original file.