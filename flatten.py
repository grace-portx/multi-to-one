import os
import json

def merge_dicts(dict1, dict2):
    """Merge dict2 into dict1, combining properties."""
    for key, value in dict2.items():
        if isinstance(value, dict) and key in dict1:
            # If the value is a dictionary and the key exists in dict1, merge recursively
            dict1[key] = merge_dicts(dict1[key], value)
        elif key == 'required':
            # Combine 'required' lists from both dictionaries, ensuring no duplicates
            dict1[key] = list(set(dict1.get(key, []) + value))
        else:
            # For all other keys, simply set the value from dict2
            dict1[key] = value
    return dict1  # Return the merged dictionary

def flatten_all_of(schema):
    """Flatten 'allOf' sections in a JSON schema object."""
    if isinstance(schema, dict):
        if 'allOf' in schema:
            # Create a new dictionary to hold merged schemas
            merged_schema = {}
            for subschema in schema['allOf']:
                # Recursively flatten each subschema and merge it into the merged schema
                merged_schema = merge_dicts(merged_schema, flatten_all_of(subschema))
            # Remove 'allOf' and merge the results into the original schema
            schema.pop('allOf', None)
            schema = merge_dicts(schema, merged_schema)
        
        # Recursively process all other keys in the schema
        for key, value in schema.items():
            schema[key] = flatten_all_of(value)
    elif isinstance(schema, list):
        # Process each item in the list
        for i, item in enumerate(schema):
            schema[i] = flatten_all_of(item)
    return schema  # Return the flattened schema

def process_file(filepath, output_directory):
    """Load a JSON file, flatten it, and save the result with a new name."""
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)  # Load the JSON data from the file
    
    # Flatten the JSON data by handling 'allOf' sections
    flattened_data = flatten_all_of(data)
    
    # Generate a new filename with the 'flat_' prefix
    directory, filename = os.path.split(filepath)  # Split the file path into directory and filename
    basename, ext = os.path.splitext(filename)  # Split the filename into base name and extension
    new_filename = f'flat_{basename}{ext}'  # Create the new filename
    new_filepath = os.path.join(output_directory, new_filename)  # Construct the full output path
    
    # Write the flattened data to the new file
    with open(new_filepath, 'w', encoding='utf-8') as file:
        json.dump(flattened_data, file, indent=2)
    
def process_directory(directory, output_directory):
    """Process all JSON files in the specified directory."""
    for root, _, files in os.walk(directory):
        # Traverse the directory to find all files
        for file in files:
            if file.endswith('.json'):
                # Process only JSON files
                filepath = os.path.join(root, file)  # Get the full file path
                print(f'Processing {filepath}...')
                process_file(filepath, output_directory)  # Call the process_file function
    print('Processing complete.')  # Indicate that all files have been processed

# Define paths for input and output directories
directory_path = '/Users/grace.lane/Documents/swagger_parse/portx_schemas_sep/3removed'
output_directory = '/Users/grace.lane/Documents/swagger_parse/portx_schemas_sep/4flat'

# Ensure the output directory exists; create it if it does not
os.makedirs(output_directory, exist_ok=True)

# Start processing files in the specified directory
process_directory(directory_path, output_directory)
