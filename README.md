## ModifyJSON

A simple Python script that provides functionality to modify JSON files by adding, replacing, or removing keys and values. 

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