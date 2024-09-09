import os
import json

def remove_unnecessary_lines(schema):
    """Recursively remove specified unnecessary properties from a JSON schema."""
    if isinstance(schema, dict):
        # Create a new dictionary with only necessary keys
        schema = {k: remove_unnecessary_lines(v) for k, v in schema.items() if k not in ['maxLength', 'minLength', 'format', 'pattern']}
    elif isinstance(schema, list):
        # Process each item in the list recursively
        schema = [remove_unnecessary_lines(item) for item in schema]
    return schema  # Return the modified schema

def process_file(input_path, output_path):
    """Load a JSON file, remove unnecessary lines, and save the result to a new file."""
    with open(input_path, 'r') as file:
        data = json.load(file)  # Load the JSON data from the input file
    
    # Remove unnecessary lines from the loaded data
    modified_data = remove_unnecessary_lines(data)
    
    # Write the modified data to the output file
    with open(output_path, 'w') as file:
        json.dump(modified_data, file, indent=2)  # Save the modified JSON with indentation for readability

def process_directory(input_directory, output_directory):
    """Process all JSON files in the specified input directory and save them to the output directory."""
    # Check if the output directory exists, create it if it doesn't
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Iterate through all files in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith('.json'):
            # Construct full file paths for input and output
            input_path = os.path.join(input_directory, filename)
            output_filename = f'remove_{filename}'  # Prefix the output filename
            output_path = os.path.join(output_directory, output_filename)
            print(f'Processing {input_path}...')  # Indicate which file is being processed
            process_file(input_path, output_path)  # Process the file
    print("Processing complete.")  # Indicate that all files have been processed

# Example usage
input_directory_path = '/Users/grace.lane/Documents/swagger_parse/portx_schemas_sep/2resolved'  # Input directory
output_directory_path = '/Users/grace.lane/Documents/swagger_parse/portx_schemas_sep/3removed'  # Output directory
process_directory(input_directory_path, output_directory_path)  # Start processing the directory
