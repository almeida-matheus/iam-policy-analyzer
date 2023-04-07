from datetime import datetime, time
import time
import inquirer
import os

class Printer:

    def __init__(self):
        self.start_code_time = time.time()
    
    def select_options(self, profiles):
        # todo - add option to detailed or simple report and report to resource level or not
        # todo - add custom dir - output different formats (csv, json, html, etc)
        questions = [
            inquirer.Path(
                "file_name",
                message="Json file with AWS actions and resources to check identities with these permissions",
                path_type=inquirer.Path.FILE,
                exists=True
            ),
            inquirer.Checkbox(
                'profiles',
                message="Select the profile/account to analyze using AWS API calls",
                choices=profiles,
                default='all'
            ),
            inquirer.Confirm(
                'match_all_actions',
                message="Show only identities that contain all specified AWS actions and resources?", 
                default=False
            ),
            inquirer.Text(
                'output_file_name',
                message='Output file name',
                default='report-iam-policy-analyzer.csv'
            )
        ]
        answers = inquirer.prompt(questions)
        return answers
    
    def script_header(self):
        os.system('clear||cls')
        print('---------------------------------------------------------------------')
        print('                        IAM POLICY ANALYZER                          ')
        print('---------------------------------------------------------------------')
        print('Example json file policy:')
        print('')
        print('{')
        print('  "actions": [')
        print('    "aws:Action"')
        print('  ],')
        print('  "resources": [')
        print('    "arn:aws:x:x:x:x"')
        print('  ]')
        print('}')
        print('')

    def execution_header(self, account_id, actions, resources):
        print('---------------------------------------------------------------------')
        print('Analyzing permissions of the entities of the {} AWS account'.format(account_id))
        print('---------------------------------------------------------------------')
        print('- Current Time:')
        print('  - {}'.format(str(datetime.now())))
        print('')
        print('- Input Parameters:')
        print('  - Actions:')
        for action in actions:
            print('    - {}'.format(action))
        print('  - Resources:')
        for resource in resources:
            print('    - {}'.format(resource))
        print('')
        print(' - Identified Entities:')
    
    def execution_body(self, name, resource):
        print('  - Entity Arn:')
        print('    - {}'.format(name))
        print('  - Resource:')
        print('    - {}'.format(resource))
        print('')
    
    def execution_footer(self):
        print('---------------------------------------------------------------------')
        print("Runtime in seconds: {}".format(round(time.time() - self.start_code_time,2)))
        print('---------------------------------------------------------------------')