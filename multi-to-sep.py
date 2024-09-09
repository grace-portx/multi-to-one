import yaml
import glob
import os
import base64
import json

directory = '/Users/grace.lane/Documents/swagger_parse'
yaml_files = glob.glob(f'{directory}/**/*.yaml', recursive=True)
total_schemas = 0
count = 1

def convert_to_base64(data):
    if isinstance(data, dict):
        return {k: convert_to_base64(v) for k, v in data.items() if k != 'type'}
    elif isinstance(data, list):
        return [convert_to_base64(item) for item in data]
    elif isinstance(data, bytes):
        return base64.b64encode(data).decode('utf-8')
    else:
        return data

for yaml_file in yaml_files:
    try:
        with open(yaml_file, 'r') as file:
            api = yaml.safe_load(file)
    except Exception as e:
        print(f"Error reading {yaml_file}: {e}")
        continue

    yaml_filename = os.path.splitext(os.path.basename(yaml_file))[0]
    contact_email = api.get('info', {}).get('contact', {}).get('email', 'Unknown')
    api_name = contact_email.split('@')[-1].split('.')[0] if contact_email != 'Unknown' else yaml_filename

    schemas_dir = f'{directory}/{api_name}_schemas_sep'
    os.makedirs(schemas_dir, exist_ok=True)

    schemas = api.get('definitions') or api.get('components', {}).get('schemas')
    if not schemas:
        print(f"No schemas found in {yaml_file}")
        continue

    try:
        schemas = convert_to_base64(schemas)

        for schema_name, schema_info in schemas.items():
            try:
                schema_path = f'{schemas_dir}/{schema_name}.json'
                with open(schema_path, 'w') as outfile:
                    json.dump({schema_name: schema_info}, outfile, indent=2)
            except Exception as e:
                print(f"Error writing schema file for {schema_name}: {e}")

        num_schemas = len(schemas)
        total_schemas += num_schemas

        print(f'Number of schemas in {yaml_filename}.yaml [File no. {count}]: {num_schemas}')
        print(f'                                         Running total: {total_schemas}\n')
        count += 1
    except Exception as e:
        print(f"Error processing schemas in {yaml_file}: {e}")

print(f'Number of total schemas in all YAML files: {total_schemas}')
