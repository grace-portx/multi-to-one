import os
import json

def remove_unnecessary_lines(schema):
    if isinstance(schema, dict):
        schema = {k: remove_unnecessary_lines(v) for k, v in schema.items() if k not in ['maxLength', 'minLength']}
    elif isinstance(schema, list):
        schema = [remove_unnecessary_lines(item) for item in schema]
    return schema

def process_file(input_path, output_path):
    with open(input_path, 'r') as file:
        data = json.load(file)
    
    modified_data = remove_unnecessary_lines(data)
    
    with open(output_path, 'w') as file:
        json.dump(modified_data, file, indent=2)

def process_directory(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    for filename in os.listdir(input_directory):
        if filename.endswith('.json'):
            input_path = os.path.join(input_directory, filename)
            output_filename = f'remove_{filename}'
            output_path = os.path.join(output_directory, output_filename)
            process_file(input_path, output_path)

# Example usage
input_directory_path = '/Users/grace.lane/Documents/swagger_parse/names/derefed'
output_directory_path = '/Users/grace.lane/Documents/swagger_parse/names/removed'
process_directory(input_directory_path, output_directory_path)
