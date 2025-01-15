#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Json Helper

A class for easier json file usage.

MIT License
TheBiemGamer (biemgamer@pm.me)
"""

import json
from typing import Union, Optional, TextIO
from pathlib import Path
from pprint import pprint
from jsonschema import validate, ValidationError

class json_file():
    def __init__(self, file: Optional[Union[Path, str]] = None):
        self.json_file: Optional[Union[Path, str]] = file

    def __enter__(self) -> "json_file":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass

    def _resolve_file(self, file: Optional[Union[Path, str]] = None) -> Union[Path, str]:
        if file:
            if self.json_file and file != self.json_file:
                return file
            return file

        if not self.json_file:
            raise ValueError("File can't be empty!")

        return self.json_file

    def _validate_file(self, file: Union[Path, str]) -> Union[Path, str]:
        file = self._resolve_file(file)
        if isinstance(file, Path):
            return Path(f"{str(file)}.json") if not str(file).endswith(".json") else file
        if isinstance(file, str):
            return f"{file}.json" if not file.endswith(".json") else file
        raise TypeError("Input file wasn't of type Path or str!")

    @property
    def data(self) -> dict:
        return self.read()

    @property
    def is_empty(self) -> bool:
        try:
            data = self.data
            return data == {} or not bool(data)
        except (FileNotFoundError, json.JSONDecodeError):
            return True

    @property
    def size(self) -> int:
        if self.json_file and Path(self.json_file).exists():
            return Path(self.json_file).stat().st_size
        raise FileNotFoundError(f"The file '{self.json_file}' doesn't exist!")

    @property
    def keys(self) -> list:
        data = self.data
        if isinstance(data, dict):
            return list(data.keys())
        raise TypeError("Data is not a dictionary!")

    @property
    def values(self) -> list:
        data = self.data
        if isinstance(data, dict):
            return list(data.values())
        raise TypeError("Data is not a dictionary!")

    @property
    def length(self) -> int:
        data = self.data
        if isinstance(data, (dict, list)):
            return len(data)
        raise TypeError("Data is not a list or a dictionary!")

    @property
    def exists(self) -> bool:
        return self.json_file and Path(self.json_file).exists()

    def read(self, file: Optional[Union[Path, str]] = None) -> dict:
        self.json_file = self._validate_file(file)
        with open(self.json_file, "r") as file_handle:
            data = json.load(file_handle)
            if isinstance(data, list) and len(data) == 1 and isinstance(data[0], dict):
                return data[0]
            return data

    def write(self, data: Union[dict, list[dict]], file: Optional[Union[Path, str]] = None) -> Union[Path, str]:
        self.json_file = self._validate_file(file)
        
        if isinstance(data, dict):
            pass
        elif isinstance(data, list):
            if not all(isinstance(item, dict) for item in data):
                raise TypeError("All items in a list must be dicts!")
        else:
            raise TypeError("Passed data must be a dictionary or a list of dictionaries!")
        
        with open(self.json_file, "w") as file_handle:
            json.dump(data, file_handle, indent=4)
            
        return self.json_file

    def append(self, data: Union[dict, list[dict]], file: Optional[Union[Path, str]] = None) -> Union[Path, str]:
        self.json_file = self._validate_file(file)
        try:
            file_data = self.data
        except (FileNotFoundError, json.JSONDecodeError):
            file_data = []

        if isinstance(file_data, list):
            file_data.append(data)
        elif isinstance(file_data, dict):
            if not isinstance(data, dict):
                raise ValueError(f"Can't append non-dict to a JSON dictionary!")
            file_data.update(data)
        else:
            raise ValueError(f"Unsupported JSON structure: {type(file_data)}")

        return self.write(file_data, self.json_file)


    def pretty_print(self) -> None:
        data = self.data
        pprint(data)

    def clear(self, file: Optional[Union[Path, str]] = None) -> Union[Path, str]:
        self.write({}, file)

    def validate_schema(self, schema: dict) -> bool:
        try:
            validate(instance=self.data, schema=schema)
            return True
        except ValidationError as e:
            print(f"Schema validation error: {e}")
            return False
