import yaml
import glob
import os
import base64
import json

# Define the directory where YAML files are located
directory = '/Users/grace.lane/Documents/swagger_parse'
# Use glob to find all YAML files in the directory and subdirectories
yaml_files = glob.glob(f'{directory}/**/*.yaml', recursive=True)
# Initialize counters for total schemas and file processing count
total_schemas = 0
count = 1

def convert_to_base64(data):
    """Convert dictionary or list items to base64, excluding 'type' keys."""
    if isinstance(data, dict):
        # Recursively convert dictionary values to base64, excluding 'type' keys
        return {k: convert_to_base64(v) for k, v in data.items() if k != 'type'}
    elif isinstance(data, list):
        # Recursively convert list items to base64
        return [convert_to_base64(item) for item in data]
    elif isinstance(data, bytes):
        # Encode byte data to base64 and decode to UTF-8 string
        return base64.b64encode(data).decode('utf-8')
    else:
        # Return the data as-is if it's not a dict, list, or bytes
        return data

# Loop through each YAML file found
for yaml_file in yaml_files:
    try:
        # Open and read the YAML file
        with open(yaml_file, 'r') as file:
            api = yaml.safe_load(file)
    except Exception as e:
        # Handle errors while reading the YAML file
        print(f"Error reading {yaml_file}: {e}")
        continue

    # Extract the filename without extension to use as a base for the output directory
    yaml_filename = os.path.splitext(os.path.basename(yaml_file))[0]
    # Get the contact email from the API info, default to 'Unknown' if not found
    contact_email = api.get('info', {}).get('contact', {}).get('email', 'Unknown')
    # Derive API name from the email domain or use the filename if email is unknown
    api_name = contact_email.split('@')[-1].split('.')[0] if contact_email != 'Unknown' else yaml_filename

    # Define a directory for storing schemas related to this API
    schemas_dir = f'{directory}/{api_name}_schemas_sep'
    # Create the schemas directory if it doesn't already exist
    os.makedirs(schemas_dir, exist_ok=True)

    # Define a directory for storing schemas related to this API
    source_dir = f'{schemas_dir}/1source'
    # Create the schemas directory if it doesn't already exist
    os.makedirs(source_dir, exist_ok=True)

    # Get the schemas from the YAML file, checking both 'definitions' and 'components'
    schemas = api.get('definitions') or api.get('components', {}).get('schemas')
    if not schemas:
        # Skip the file if no schemas are found
        print(f"No schemas found in {yaml_file}")
        continue

    try:
        # Convert the schemas to base64 format
        schemas = convert_to_base64(schemas)

        # Loop through each schema and save it to a JSON file
        for schema_name, schema_info in schemas.items():
            try:
                # Define the path for the schema JSON file
                output_path = f'{source_dir}/{schema_name}.json'
                # Write the schema information to a JSON file
                with open(output_path, 'w') as outfile:
                    json.dump({schema_name: schema_info}, outfile, indent=2)
            except Exception as e:
                # Handle errors while writing the schema file
                print(f"Error writing schema file for {schema_name}: {e}")

        # Count the number of schemas processed and update the total
        num_schemas = len(schemas)
        total_schemas += num_schemas

        # Print the number of schemas processed from this file and the running total
        print(f'Number of schemas in {yaml_filename}.yaml [File no. {count}]: {num_schemas}')
        print(f'                                         Running total: {total_schemas}\n')
        count += 1  # Increment the file count
    except Exception as e:
        # Handle errors during schema processing
        print(f"Error processing schemas in {yaml_file}: {e}")

# Print the total number of schemas processed across all files
print(f'Number of total schemas in all YAML files: {total_schemas}')
