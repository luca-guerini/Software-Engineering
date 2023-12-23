#!/usr/bin/env python3
import json
import sys

# EFFECT: Processes a sequence of JSON values from user input and standard input.
def process_json_sequence():
    # List to store processed JSON values
    sequence = []

    # Collect manual input lines for immediate user input
    manual_input_lines = []

    try:
        # Allow manual JSON input from the command line immediately
        while True:
            try:
                # Prompt the user for input
                manual_input = input("")
            except (EOFError, KeyboardInterrupt):
                break

            # Append the manual input to the list of lines
            manual_input_lines.append(manual_input)

    except KeyboardInterrupt:
        pass  # Handle Ctrl+C to stop manual input

    # Process stdin input line by line
    for line in sys.stdin:
        line = line.strip()

        # Check if the line is not empty
        if line:
            # Append the input line to the list of lines
            manual_input_lines.append(line)

    # Combine collected input lines into a single string
    combined_input = ''.join(manual_input_lines)
    # Split the combined input into individual JSON values based on newline separators
    json_values = combined_input.split('\n')
    for json_str in json_values:
        try:
            # Attempt to parse the JSON string into a Python object
            json_value = json.loads(json_str)
            sequence.append(json_value)
        except json.JSONDecodeError:
            # Handle invalid JSON input and report errors
            sys.stderr.write(f"Error: Invalid JSON input '{json_str}'\n")
    return sequence
