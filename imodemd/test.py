import json

# Assuming the JSON data is stored in a file named 'Golden.json'
file_name = 'Second.json'

# Open the file and load the JSON data into a Python object
with open(file_name, 'r') as file:
    unique_entries_json = json.load(file)

# Define a function to convert JSON entries to a hashable format
def convert_to_hashable(entry):
    hashable_entry = {}
    for key, value in entry.items():
        if isinstance(value, list):
            hashable_entry[key] = tuple(value)  # Convert lists to tuples
        else:
            hashable_entry[key] = value
    return tuple(sorted(hashable_entry.items()))

# Extract unique entries from the loaded JSON data
unique_entries = list(set(convert_to_hashable(entry) for entry in unique_entries_json))

# Convert unique entries back to dictionary format
unique_entries_json = [dict(entry) for entry in unique_entries]

# Write the unique JSON data to another file named 'unique_data.json'
with open("unique_data.json", 'w') as f:
    json.dump(unique_entries_json, f)

print("Unique data extracted and saved to 'unique_data.json'")
