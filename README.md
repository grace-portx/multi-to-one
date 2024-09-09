## YAML Parsers

This section describes the parsers developed for managing large YAML files:

### multi-to-sep

This parser processes multiple YAML files and separates each schema into individual files.  
Problem: Almost every schema contains references to another schema, which cannot be accessed by the AI model, so results are not accurate.

### multi-sep-no-refs

This parser processes multiple YAML files but additionally dereferences each reference before separating into individual files.  
Problem: This one did not have any problems, but I wanted to separate the two functions.

### deref

This parser processes multiple JSON files and dereferences each reference before saving to a new directory. These JSON files come from running the **multi-to-sep** parser.  
Problem: There was unnecessary details for each different property within the schemas, such as minlength and maxlength.
