import pytest
import json
import os
import tempfile
import sys

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modify_json import modify_json_files

@pytest.fixture
def json_test_file():
    """Fixture to create and clean up a temporary JSON test file."""
    # Create temporary directory for test files
    test_dir = tempfile.TemporaryDirectory()
    
    # Sample JSON content for testing
    sample_json = {
        "name": "Test",
        "version": "1.0",
        "settings": {
            "debug": False,
            "timeout": 30,
            "nested": {
                "value": "original"
            }
        },
        "numbers": [1, 2, 3]
    }
    
    # Create test file
    test_file = os.path.join(test_dir.name, "test.json")
    with open(test_file, 'w') as f:
        json.dump(sample_json, f, indent=2)
    
    # Yield the file path to the test
    yield test_file
    
    # Clean up temporary directory after test completes
    test_dir.cleanup()

def read_json_file(file_path):
    """Helper function to read a JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def test_add_new_key(json_test_file):
    modify_json_files(json_test_file, "[newKey]", "new value", 'add')
    data = read_json_file(json_test_file)
    assert data["newKey"] == "new value"

def test_add_nested_key(json_test_file):
    modify_json_files(json_test_file, "[settings][newSetting]", "42", 'add')
    data = read_json_file(json_test_file)
    assert data["settings"]["newSetting"] == 42

def test_replace_existing_key(json_test_file):
    modify_json_files(json_test_file, "[version]", "2.0", 'replace')
    data = read_json_file(json_test_file)
    assert data["version"] == 2.0

def test_replace_nested_key(json_test_file):
    modify_json_files(json_test_file, "[settings][debug]", "true", 'replace')
    data = read_json_file(json_test_file)
    assert data["settings"]["debug"] is True

def test_remove_key(json_test_file):
    modify_json_files(json_test_file, "[version]", None, 'remove')
    data = read_json_file(json_test_file)
    assert "version" not in data

def test_remove_nested_key(json_test_file):
    modify_json_files(json_test_file, "[settings][timeout]", None, 'remove')
    data = read_json_file(json_test_file)
    assert "timeout" not in data["settings"]

def test_replace_nonexistent_key_fails(json_test_file):
    with pytest.raises(Exception):
        modify_json_files(json_test_file, "[nonexistent]", "value", 'replace')

def test_add_deeply_nested_key(json_test_file):
    modify_json_files(json_test_file, "[settings][nested][deeper][deepest]", "very deep", 'add')
    data = read_json_file(json_test_file)
    assert data["settings"]["nested"]["deeper"]["deepest"] == "very deep"

def test_add_and_replace_complex_number(json_test_file):
    # Test adding a complex number
    modify_json_files(json_test_file, "[complexNumber]", "1+2j", 'add')
    data = read_json_file(json_test_file)
    assert data["complexNumber"] == "1+2j"
    
    # Test replacing the complex number
    modify_json_files(json_test_file, "[complexNumber]", "3+4j", 'replace')
    data = read_json_file(json_test_file)
    assert data["complexNumber"] == "3+4j"

def test_value_type_conversion(json_test_file):
    # Test various type conversions
    modify_json_files(json_test_file, "[numericValue]", "123", 'add')
    modify_json_files(json_test_file, "[boolValue]", "true", 'add')
    modify_json_files(json_test_file, "[nullValue]", "null", 'add')
    modify_json_files(json_test_file, "[floatValue]", "3.14", 'add')
    
    data = read_json_file(json_test_file)
    
    assert data["numericValue"] == 123
    assert data["boolValue"] is True
    assert data["nullValue"] is None
    assert data["floatValue"] == 3.14

# Add a new test for the case where --add is used with existing path
def test_add_with_existing_path(json_test_file):
    # First verify the original value
    data = read_json_file(json_test_file)
    assert data["settings"]["debug"] is False
    
    # Use 'add' mode to update the existing value
    modify_json_files(json_test_file, "[settings][debug]", "true", 'add')
    
    # Verify the value was updated
    data = read_json_file(json_test_file)
    assert data["settings"]["debug"] is True