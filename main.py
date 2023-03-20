from resources.aws import AWS
from resources.system import System
from resources.printer import Printer

if __name__ == '__main__':
    aws = AWS()
    system = System()
    printer = Printer()

    #? display select options to user
    profiles = aws.get_available_profiles()
    profiles_plus_all = ['all'] + list(profiles)
    answers = printer.select_options(profiles_plus_all)

    #? get json file to get desired actions and resources
    desired_policy = system.get_json_file_content(answers['file_name'])

    #? prepare list of profiles (accounts) to analyze
    profiles_to_analyze = answers['profiles']
    if answers['profiles'] == ['all']:
        profiles_to_analyze = profiles      

    data_analyzed_results = list()

    for profile in profiles_to_analyze:
        aws = AWS(profile)
        account_id = aws.get_account_id()
        printer.execution_header(account_id,desired_policy['actions'],desired_policy['resources'])

        all_roles = aws.list_all_roles()
        all_users = aws.list_all_users()

        #? check all identities permissions
        for role in all_roles:
            for resource in desired_policy['resources']:
                has_perm_to_access_resource = aws.simulate_policy(role['Arn'],desired_policy['actions'],[resource],answers['match_all_actions'])
                if has_perm_to_access_resource:
                    printer.execution_body(role['Arn'],resource)
                    data_analyzed_results.append({'accountId':account_id,'arn':role['Arn'],'name':role['RoleName'],'actions':desired_policy['actions'],'resource':resource})

        for user in all_users:
            for resource in desired_policy['resources']:
                has_perm_to_access_resource = aws.simulate_policy(user['Arn'],desired_policy['actions'],[resource],answers['match_all_actions'])
                if has_perm_to_access_resource:
                    printer.execution_body(user['Arn'],resource)
                    data_analyzed_results.append({'accountId':account_id,'arn':user['Arn'],'name':user['UserName'],'actions':desired_policy['actions'],'resource':resource})

    #? export to csv format
    system.export_to_csv(answers['output_file_name'],['account','arn','name','actions','resource'], mode='w')
    for item in data_analyzed_results:
        system.export_to_csv(answers['output_file_name'],[item['accountId'],item['arn'],item['name'],item['actions'],item['resource']])
    printer.execution_footer()

    # except Exception as e:
    #     print(e)