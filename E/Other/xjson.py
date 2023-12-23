import json
def process_json_sequence(input_str):
    try:
        # Split the input by empty lines to separate JSON values
        json_values = input_str.split('\n\n')
        
        # Initialize the count and sequence lists
        count = 0
        seq = []

        # Process each JSON value
        for json_str in json_values:
            json_str = json_str.strip()  # Remove leading/trailing whitespace
            if json_str:  # Check if the string is not empty
                json_value = json.loads(json_str)
                seq.append(json_value)
                count += 1

        # Create the output JSON
        output = {"count": count, "seq": seq}
        list_out = seq #copy seq
        list_out.reverse() #reverse the copy
        list_out = [count] + list_out
        return [json.dumps(output),json.dumps(list_out)]

    except json.JSONDecodeError as e:
        return [f"Error: Invalid JSON input '{e.doc}'", []]