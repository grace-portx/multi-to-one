import os
import json

def remove_unnecessary_lines(schema):
    """Recursively remove all keys from the schema except 'description' and 'example'."""
    if isinstance(schema, dict):
        # Create a new dictionary with only 'description' and 'example' keys
        schema = {k: remove_unnecessary_lines(v) for k, v in schema.items() if k in ['description', 'example']}
    elif isinstance(schema, list):
        # Recursively process each item in the list
        schema = [remove_unnecessary_lines(item) for item in schema]
    return schema  # Return the modified schema

def process_file(input_path, output_path):
    """Load a JSON file, remove unnecessary lines, and save the modified content."""
    # Open the input JSON file and load its content
    with open(input_path, 'r') as file:
        data = json.load(file)
    
    # Remove unnecessary lines from the loaded data
    modified_data = remove_unnecessary_lines(data)
    
    # Write the modified data to the output JSON file
    with open(output_path, 'w') as file:
        json.dump(modified_data, file, indent=2)

def process_directory(input_directory, output_directory):
    """Process all JSON files in the input directory and save modified files to the output directory."""
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Iterate over all files in the input directory
    for filename in os.listdir(input_directory):
        # Process only JSON files
        if filename.endswith('.json'):
            input_path = os.path.join(input_directory, filename)  # Construct input file path
            output_filename = f'remove_{filename}'  # Define output file name
            output_path = os.path.join(output_directory, output_filename)  # Construct output file path
            process_file(input_path, output_path)  # Process the input file

# Example usage of the script
input_directory_path = '/Users/grace.lane/Documents/swagger_parse/portx_schemas_sep/1resolved'
output_directory_path = '/Users/grace.lane/Documents/swagger_parse/portx_schemas_sep/2removed'
process_directory(input_directory_path, output_directory_path)  # Start processing files in the specified directory
