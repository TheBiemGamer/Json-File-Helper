# JSON File Helper

A Python class for easier JSON file handling. This utility provides a streamlined interface for reading, writing, appending, and validating JSON files, along with additional helper properties and methods.

## Features

- **Read JSON files** with automatic file validation.
- **Write JSON data** (as dictionaries or lists of dictionaries) to files.
- **Append data** to existing JSON files, supporting both dictionaries and lists.
- **Clear JSON files** by resetting their content.
- **Validate JSON schema** using the `jsonschema` library.
- Access **properties** like `keys`, `values`, `length`, `is_empty`, `size`, and `exists`.
- Pretty print JSON data for better readability.

## Installation

### Automatic installation via PyPi
```bash
pip install json_file_helper
```

### Or manual installation
```bash
git clone https://github.com/your-repo/json-helper.git
cd json-helper
```

#### Install Dependencies
This module uses the `jsonschema` library. Install the requirements using `pip` or a package manager like Poetry:

```bash
pip install -r requirements.txt
```

Or with Poetry:
```bash
poetry install
```

## Usage

### Importing the Module
```python
from json_file_helper import json_file
```

### Creating an Instance
```python
from json_file_helper import json_file

# Initialize with an optional file path
jf = json_file("example.json")
```

### Methods and Properties

#### **1. Reading a JSON File**
```python
data = jf.read()
print(data)
```

Or with the data property:
```python
data = jf.data
print(data)
```

#### **2. Writing Data**
```python
jf.write({"name": "John", "age": 30})
```

#### **3. Appending Data**
Append a dictionary to a JSON dictionary or list:
```python
jf.append({"city": "New York"})
```

#### **4. Clearing a File**
```python
jf.clear()
```

#### **5. Validating Schema**
Use a JSON schema to validate the structure of your file:
```python
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"}
    },
    "required": ["name", "age"]
}
is_valid = jf.validate_schema(schema)
print(f"Is valid: {is_valid}")
```

#### **6. Pretty Print**
```python
jf.pretty_print()
```

#### **7. Accessing Properties**
```python
print(jf.keys)      # List of keys in the JSON (if it's a dictionary)
print(jf.values)    # List of values
print(jf.length)    # Number of items (for dicts or lists)
print(jf.is_empty)  # Check if the file is empty
print(jf.size)      # File size in bytes
print(jf.exists)    # Check if the file exists
```

### Using as a Context Manager
The `json_file` class can also be used with `with` statements:
```python
with json_file("example.json") as jf:
    data = jf.read()
    jf.append({"new_key": "new_value"})
```

## Requirements

- Python 3.8+
- `jsonschema` library for schema validation

## Example

Here’s a complete example:
```python
from json_file_helper import json_file

# Initialize with a file path
jf = json_file("example.json")

# Write data to the file
jf.write({"name": "Alice", "age": 25})

# Read the file
print(jf.data)

# Append new data
jf.append({"city": "London"})

# Validate schema
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"},
        "city": {"type": "string"}
    },
    "required": ["name", "age"]
}
print(jf.validate_schema(schema))

# Pretty print the file's content
jf.pretty_print()
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Author

TheBiemGamer ([biemgamer@pm.me](mailto:biemgamer@pm.me))