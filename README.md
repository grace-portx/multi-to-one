## YAML Parsers

This repository is a collection of the parsers developed for managing large YAML and JSON schema files:

### multi-to-sep.py

This parser processes multiple YAML files and separates each object schema into individual files.  
Problem: Almost every schema contains references to another schema, which cannot be accessed by the AI model, so results are not accurate.

### deref.py

This parser processes multiple JSON files and dereferences each reference before saving to a new directory. These JSON files come from running the **multi-to-sep** parser.  
Problem: There was unnecessary details for each different property within the schemas, such as minlength and maxlength.

### remove.py

This parser process multiple JSON files and removes unnecessary details specified in the script.
