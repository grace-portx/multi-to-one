import yaml
from pprint import pprint
import glob
import os

directory = '/Users/grace.lane/Documents/swagger_parse'
yaml_files = glob.glob(f'{directory}/**/*.yaml')
total_schemas = 0
count = 0

for yaml_file in yaml_files:
  with open(yaml_file, 'r') as file:
    api = yaml.safe_load(file)

  # Get the API name from the email domain
  contact_email = api.get('info', {}).get('contact', {}).get('email', 'Unknown')
  api_name = contact_email.split('@')[-1].split('.')[0] # Extracts 'fiserv' from 'DL-NA-ESF_APServicesDesignTeam@fiserv.com'

  # Get the YAML filename without the extension for use in the schema file name
  yaml_filename = os.path.splitext(os.path.basename(yaml_file))[0]

  # Set and create directory for the API if is does not exist already
  api_dir = f'{directory}/{api_name}/{yaml_filename}'
  os.makedirs(api_dir, exist_ok=True)

  # Set and create directory for schemas if does not exist already
  schema_dir = f'{api_dir}/{yaml_filename}'
  os.makedirs(schema_dir, exist_ok=True)

  # Check the Swagger/OpenAPI version and get the schema definitions
  if 'definitions' in api:  # For Swagger 2.0
      schemas = api['definitions']
  elif 'components' in api:  # For OpenAPI 3.0
      schemas = api['components']['schemas']

  # Write each schema to a separate file
  for schema_name, schema_info in schemas.items():
      with open(f'{schema_dir}/{schema_name}.txt', 'w') as outfile:
          pprint({schema_name: schema_info}, stream=outfile)
      count += 1

  # Validate that all schemas were successfully parsed
  output_files = glob.glob(f'{api_dir}/*.txt')
  num_output = len(output_files)
  num_schemas = len(schemas)                                       # Get the number of schemas in current YAML file

  total_schemas += num_schemas

  print(f'Number of schemas in the current YAML file: {num_schemas}')
  print(f'Number of .txt files in the schema directory: {num_output}')
  print(f'Number of total schemas in all YAML files: {total_schemas}')
  print(f'Next file...........')
  # diff = num_schemas - num_output
  # if diff == 0:
  #     print(f"All {num_schemas} schemas were successfully parsed.")
  # else:
  #     print(f"{diff} schemas were not correctly parsed.")
