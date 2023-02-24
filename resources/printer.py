from datetime import datetime, time
import time
import inquirer

class Printer:

    def __init__(self):
        self.start_code_time = time.time()
    
    def select_options(self, profiles):
        # todo - add option to detailed or simple report and report to resource level or not
        questions = [
            inquirer.Path(
                "file_name",
                message="json file containing the iam actions and resources for performing the scan",
                path_type=inquirer.Path.FILE,
                exists=True,
            ),
            inquirer.Checkbox(
                'profiles',
                message="select the profile/account to analyze using AWS API calls",
                choices=profiles,
                default='all',
            ),
            inquirer.Confirm(
                'match_all_actions',
                message="must it contain all iam actions and resources specified?", default=False)
        ]
        answers = inquirer.prompt(questions)
        return answers

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