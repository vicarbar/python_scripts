def format_text(text):
    # Define the output format
    output_format = '''
      {name}:
        type: {type}
        example: {example}
        description: {description}'''

    # Process each line of the input text
    output_lines = []
    for line in text.strip().split('\n'):
        # Split the line by spaces to extract the relevant parts
        parts = line.split()
        
        # Remove the words 'Mandatory' and 'Optional'
        parts = [part for part in parts if part not in ["Mandatory", "Optional", "UUID"]]
        
        # Extract the name by removing quotes and colon
        name = parts[0].replace('"', '').replace(':', '')
        
        # The type is based on the content - 'String' becomes 'string', 'Double' becomes 'number'
        type_mapping = {'String': 'string', 'Double': 'number', 'Integer': 'number'}
        type = type_mapping.get(parts[3], 'string')  # Default to string if not found
        
        # The example is the last part of the line
        example = parts[-1].replace('"', '')
        
        # The description is everything between the first and last parts
        description = ' '.join(parts[1:-2])
        
        # Format the line according to the output format and add it to the results
        output_lines.append(output_format.format(name=name, type=type, example=example, description=description))
    
    return ''.join(output_lines)

# Read the input text from the user
input_text = '''
"bffUserId": ,	Internal code to identify the user 	Mandatory 	String		"User0001"
"portalCode": ,	Code to identify the portal	Mandatory 	String		"PT001"
"consumerCode": ,	Code to identify the consumer	Mandatory 	String		"P999"
"toolActionCode": ,	Code to identify the action performed by the portal user	Mandatory 	String		"TA04"
'''.replace(",","")

# Format the text and print the output
print(format_text(input_text))
