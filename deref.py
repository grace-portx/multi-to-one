import os
import json

def load_json_file(file_path):
    """Loads a JSON file and returns its content."""
    with open(file_path, 'r') as file:
        return json.load(file)

def resolve_references(schema, schemas_cache):
    """Resolve $ref tags in the schema with the content of the referenced files."""
    stack = [schema]
    processed_schemas = set()

    while stack:
        current = stack.pop()

        if isinstance(current, dict):
            if '$ref' in current:
                ref_paths = current['$ref']
                if not isinstance(ref_paths, list):
                    ref_paths = [ref_paths]  # Ensure ref_paths is a list

                resolved_content = {}
                for ref_path in ref_paths:
                    if ref_path.startswith('#'):
                        ref_path = ref_path[1:]  # Remove leading '#'
                        ref_parts = ref_path.split('/')
                        ref_key = ref_parts[-1]  # The key in the schema
                        ref_schema = schemas_cache.get(ref_key, {})
                        resolved_content.update(ref_schema)  # Merge with existing content
                    else:
                        # Handle external references if needed
                        pass
                
                # Replace the content of the current dict with the resolved content
                current.clear()
                current.update(resolved_content)
                if '$ref' in current:
                    del current['$ref']

            # Process dictionary values
            for key, value in current.items():
                if isinstance(value, dict) or isinstance(value, list):
                    if id(value) not in processed_schemas:
                        stack.append(value)
                        processed_schemas.add(id(value))

        elif isinstance(current, list):
            # Process list items
            for item in current:
                if isinstance(item, dict) or isinstance(item, list):
                    if id(item) not in processed_schemas:
                        stack.append(item)
                        processed_schemas.add(id(item))

    return schema

def process_schemas(schema_dir):
    """Process all JSON files in the directory and resolve $ref tags."""
    schemas_cache = {}

    # Load all schemas into cache
    for file_name in os.listdir(schema_dir):
        if file_name.endswith('.json'):
            file_path = os.path.join(schema_dir, file_name)
            schema_name = file_name.replace('.json', '')
            schemas_cache[schema_name] = load_json_file(file_path)
    
    # Resolve references in each schema
    for file_name in os.listdir(schema_dir):
        if file_name.endswith('.json'):
            file_path = os.path.join(schema_dir, file_name)
            schema = load_json_file(file_path)
            resolved_schema = resolve_references(schema, schemas_cache)
            
            # Save the resolved schema to a new file
            # Create the schemas directory if it doesn't already exist
            out_dir = schema_dir + '/1resolved/'
            os.makedirs(out_dir, exist_ok=True)
            output_file_path = os.path.join(out_dir + 'resolved_' + file_name)
            with open(output_file_path, 'w') as out_file:
                json.dump(resolved_schema, out_file, indent=2)

# Define the directory containing the JSON schema files
schema_dir = '/Users/grace.lane/Documents/swagger_parse/portx_schemas_sep/1source'
process_schemas(schema_dir)
