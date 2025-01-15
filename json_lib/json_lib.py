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
        self._file_handle: Optional[TextIO] = None

    def __enter__(self) -> "json_file":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self._file_handle:
            self._file_handle.close()

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
        file = self._validate_file(self.json_file)
        with open(file, "r") as file_handle:
            return json.load(file_handle)

    @property
    def is_empty(self) -> bool:
        try:
            data = self.data
            return not bool(data)
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
        self._file_handle = open(self.json_file, "r")
        data = json.load(self._file_handle)
        return data

    def write(self, data: Union[dict, list[dict]], file: Optional[Union[Path, str]] = None) -> Union[Path, str]:
        self.json_file = self._validate_file(file)

        if isinstance(data, list):
            try:
                data = data[0]
            except IndexError:
                raise TypeError("Passed data is not a dict or a list[dict]!")
            else:
                if not isinstance(data, dict):
                    raise TypeError("Passed data is not a dict or a list[dict]!")

        self._file_handle = open(self.json_file, "w")
        json.dump(data, self._file_handle, indent=4)

        return self.json_file

    def append(self, data: Union[dict, list[dict]], file: Optional[Union[Path, str]] = None) -> Union[Path, str]:
        self.json_file = self._validate_file(file)

        try:
            file_data = self.data
        except (FileNotFoundError, json.JSONDecodeError):
            file_data = []

        match file_data:
            case list():
                file_data.append(data)
            case dict():
                file_data.update(data)
            case _:
                raise ValueError(f"Can't append {type(file_data)} to a json file!")

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
