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
                raise Exception(f"'{key}' key not found in passed json file")
            if not json_content[key]:
                raise Exception(f"json file '{key}' key is completely empty")
            for i, value in enumerate(json_content[key]):
                if not value:
                    raise Exception(f"the value of position {i} of the {key} key is empty")

        for key in keys_to_validate:
            validate_fiels(key)

class System(CustomSystem):

    def __init__(self):
        self.actual_path = str(Path().resolve())
        self.ouput_path = self.actual_path+'/iam-policy-analyzer'

    def get_json_file_content(self, file_name):
        try:
            path_file = self.actual_path+'/'+file_name
            file = open(path_file, 'r')
            file_content = json.load(file)
            self.validate_json_content(file_content)
            return file_content
        except (OSError, IOError):
            raise OSError('cannot read this file: '+path_file)
        finally:
            file.close()
        
    def export_to_csv(self, file_name, item, mode='a'):
        with open(file_name, mode, encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(item)

    def create_dir(self, path, rm):
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except:
            raise OSError('cannot create directory here: '+self.actual_path)