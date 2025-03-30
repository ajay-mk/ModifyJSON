#!/usr/bin/env python3

import os
import json
import glob
import sys
import re
import argparse

def modify_json_files(file_pattern, path_str, new_value, mode, output_file=None):
    """
    Find and modify JSON files matching the pattern.
    
    Args:
        file_pattern (str): Pattern for matching JSON files (glob pattern)
        path_str (str): String representing the path in format "[key1][key2]..."
        new_value: The new value to set at the specified path (not used for remove mode)
        mode (str): 'add' to add keys if they don't exist, 'replace' to only modify existing keys,
                   'remove' to delete the specified path
        output_file (str): Name of the output file to save the modified JSON. If None, overwrite the original file.
    """
    # Parse the path string into keys
    path_keys = re.findall(r'\[(.*?)\]', path_str)
    if not path_keys:
        raise ValueError(f"Invalid path format: {path_str}. Expected format like '[key1][key2]'")
    
    # Find all JSON files matching the pattern
    json_files = glob.glob(file_pattern)
    
    if not json_files:
        print(f"No JSON files found matching pattern: {file_pattern}")
        return
    
    # Try to convert the new_value to int, float, bool, or None if it looks like one (only for add/replace)
    if mode != 'remove' and new_value is not None:
        try:
            if new_value.isdigit():
                new_value = int(new_value)
            elif re.match(r'^-?\d+(\.\d+)?$', new_value):
                new_value = float(new_value)
            elif new_value.lower() == 'true':
                new_value = True
            elif new_value.lower() == 'false':
                new_value = False
            elif new_value.lower() == 'null':
                new_value = None
        except (ValueError, AttributeError):
            pass  # Keep as string if conversion fails
    
    for file_path in json_files:
        try:
            # Read the JSON file
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            if mode == 'remove':
                # Special handling for removal
                if len(path_keys) == 1:
                    # Only one level - direct key removal from root
                    if path_keys[0] in data:
                        print(f"Removing key '{path_keys[0]}' from {file_path}")
                        del data[path_keys[0]]
                    else:
                        print(f"Key '{path_keys[0]}' not found in {file_path}, nothing to remove")
                else:
                    # Navigate to the parent of the key to be removed
                    current = data
                    path_exists = True
                    
                    for key in path_keys[:-1]:
                        if key not in current:
                            path_exists = False
                            print(f"Path '{path_str}' does not exist in {file_path}, nothing to remove")
                            break
                        current = current[key]
                    
                    if path_exists:
                        final_key = path_keys[-1]
                        if final_key in current:
                            print(f"Removing {path_str} from {file_path}")
                            del current[final_key]
                        else:
                            print(f"Final key '{final_key}' not found in {file_path}, nothing to remove")
            else:
                # Navigate to the path for add/replace modes
                current = data
                path_exists = True
                
                for i, key in enumerate(path_keys[:-1]):
                    if key not in current:
                        if mode == 'add':
                            # Create nested dictionaries for missing keys
                            current[key] = {}
                            print(f"Creating key '{key}' in path {path_str} in {file_path}")
                        else:  # mode == 'replace'
                            path_exists = False
                            raise KeyError(f"Path '{path_str}' does not exist in {file_path}. Key '{key}' is missing.")
                    current = current[key]
                
                # Handle the final key
                final_key = path_keys[-1]
                if final_key in current:
                    original_value = current[final_key]
                    print(f"Replacing {path_str}={original_value} with {new_value} in {file_path}")
                else:
                    if mode == 'add':
                        print(f"Adding new key {final_key} with value {new_value} in {file_path}")
                    else:  # mode == 'replace'
                        raise KeyError(f"Path '{path_str}' does not exist in {file_path}. Final key '{final_key}' is missing.")
                
                # Set the new value
                current[final_key] = new_value
            
            # Write the modified data to the output file
            output_path = output_file if output_file else file_path
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"Modified file written to: {output_path}")
        
        except KeyError as e:
            if mode == 'replace':
                print(f"Error processing {file_path}: {e}")
                raise  # Re-raise the exception to stop execution
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            raise  # Re-raise the exception to stop execution

def main():
    parser = argparse.ArgumentParser(description='Modify JSON files with add, replace, or remove operations')
    parser.add_argument('file_pattern', help='Pattern for matching JSON files (glob pattern)')
    parser.add_argument('json_path', help='Path in JSON file, format: "[key1][key2]..."')
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--add', action='store_true', help='Add keys if they don\'t exist')
    group.add_argument('--replace', action='store_true', help='Only modify existing keys (original behavior)')
    group.add_argument('--remove', action='store_true', help='Remove the specified path')
    
    # Make new_value optional only when using --remove
    parser.add_argument('new_value', nargs='?', help='New value to set at the specified path (not used with --remove)')
    
    # Add an optional argument for the output file
    parser.add_argument('--output-file', help='Name of the output file to save the modified JSON. If not provided, original files are overwritten.')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.remove and args.new_value is not None:
        print("Warning: New value argument is ignored when using --remove")
        args.new_value = None
    elif not args.remove and args.new_value is None:
        parser.error("New value is required when using --add or --replace")
    
    mode = 'remove' if args.remove else ('add' if args.add else 'replace')
    
    try:
        modify_json_files(args.file_pattern, args.json_path, args.new_value, mode, args.output_file)
        print("All files processed successfully.")
    except Exception as e:
        print(f"Process failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()