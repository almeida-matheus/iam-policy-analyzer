from pathlib import Path
import os
import json
import csv

class CustomSystem:

    def validate_json_content(self, json_content):
        ''' validate all required json file fields for scripting '''
        keys_to_validate = ['actions', 'resources']

        def validate_fiels(key):
            ''' check invalid values (None, empty) '''
            if not key in json_content:
                raise Exception(f"Key '{key}' not found in passed json file")
            if not json_content[key]:
                raise Exception(f"Json file '{key}' key is completely empty")
            for i, value in enumerate(json_content[key]):
                if not value:
                    raise Exception(f"The value of position {i} of the {key} key is empty")

        for key in keys_to_validate:
            validate_fiels(key)

class System(CustomSystem):

    def __init__(self):
        self.actual_path = str(Path().resolve())+'/'

    def get_json_file_content(self, file_name):
        try:
            path_file = self.actual_path + file_name
            file = open(path_file, 'r')
            file_content = json.load(file)
            self.validate_json_content(file_content)
            return file_content
        except (OSError, IOError):
            raise OSError(f'Cannot read this file: {path_file}')
        finally:
            file.close()

    def create_dir(self, path):
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except:
            raise OSError(f'Cannot create directory here: {self.actual_path}')

    def export_to_csv(self, file_name, item, mode='a'):
        path_file = self.actual_path + file_name
        try:
            with open(path_file, mode, encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(item)
        except Exception as e:
            raise Exception(f'Unable to export CSV file: {e}')