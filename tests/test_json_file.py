import unittest, os, json
from pathlib import Path
from json_lib.json_file import json_file

class TestJsonFile(unittest.TestCase):
    def setUp(self):
        """Setup test files and data"""
        self.test_file = "test.json"
        self.test_data = {"name": "John", "age": 30, "city": "New York"}
        self.test_data_list = [{"name": "Alice"}, {"name": "Bob"}]
        self.schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "city": {"type": "string"}
            },
            "required": ["name", "age", "city"]
        }
        
    def tearDown(self):
        """Clean up files"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
            
    def test_write_and_read(self):
        """Test writng to and reading from a JSON file"""
        with json_file(self.test_file) as jf:
            jf.write(self.test_data)
            read_data = jf.read()
        self.assertEqual(read_data, self.test_data)
        
    def test_append_to_file(self):
        """Test appending to JSON file"""
        with json_file(self.test_file) as jf:
            jf.write(self.test_data)
            jf.append({"country": "USA"})
            updated_data = jf.read()
        expected_data = {"name": "John", "age": 30, "city": "New York", "country": "USA"}
        self.assertEqual(updated_data, expected_data)
        
    def test_clear_file(self):
        """Test clearing a JSON file"""
        with json_file(self.test_file) as jf:
            jf.write(self.test_data)
            jf.clear()
            is_empty = jf.is_empty
        self.assertTrue(is_empty)
        
    def test_file_properties(self):
        """Test file-related properties"""
        with json_file(self.test_file) as jf:
            jf.write(self.test_data)
            self.assertTrue(jf.exists)
            self.assertEqual(jf.size, Path(self.test_file).stat().st_size)
            self.assertEqual(jf.keys, list(self.test_data.keys()))
            
    def test_empty_file(self):
        """Test behavior when file is empty"""
        with json_file(self.test_file) as jf:
            jf.write({})
            self.assertTrue(jf.is_empty)
    
    def test_length_property(self):
        """Test the length property for dicts and lists"""
        with json_file(self.test_file) as jf:
            jf.write(self.test_data)
            self.assertEqual(jf.length, len(self.test_data))
            jf.write(self.test_data_list)
            self.assertEqual(jf.length, len(self.test_data_list))
    
    def test_invalid_append(self):
        """Test appending invalid data"""
        with json_file(self.test_file) as jf:
            jf.write(self.test_data)
            with self.assertRaises(ValueError):
                jf.append("invalid_data")
    
    def test_validate_schema(self):
        """Test schema validation"""
        with json_file(self.test_file) as jf:
            jf.write(self.test_data)
            self.assertTrue(jf.validate_schema(self.schema))
            invalid_data = {"name": "John", "city": "New York"}
            jf.write(invalid_data)
            self.assertFalse(jf.validate_schema(self.schema))
            
    def test_pretty_print(self):
        """Test pretty printing"""
        with json_file(self.test_file) as jf:
            jf.write(self.test_data)
            try:
                jf.pretty_print()
            except Exception as e:
                self.fail(f"pretty_print() raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()