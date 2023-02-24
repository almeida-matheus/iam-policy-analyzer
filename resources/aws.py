import boto3

class AWS:

    def __init__(self, profile=None):

        self.session = boto3.Session()
        if profile:
            self.session = boto3.Session(profile_name=profile)

        self.iam_client = self.session.client('iam')
        self.sts_client = self.session.client('sts')

    def get_available_profiles(self):
        return self.session.available_profiles

    def get_account_id(self):
        return self.sts_client.get_caller_identity().get('Account')

    def list_all_roles(self):
        all_roles = list()
        paginator = self.iam_client.get_paginator('list_roles')
        paginator_iterator = paginator.paginate()
        for page in paginator_iterator:
            for role in page['Roles']:
                all_roles.append(role)
        return all_roles
    
    def list_all_users(self):
        all_roles = list()
        paginator = self.iam_client.get_paginator('list_users')
        paginator_iterator = paginator.paginate()
        for page in paginator_iterator:
            for user in page['Users']:
                all_roles.append(user)
        return all_roles

    def simulate_policy(self, arn, actions, resources, match_all_actions):
        response = self.iam_client.simulate_principal_policy(
            PolicySourceArn=arn,
            ActionNames=actions,
            ResourceArns=resources
        )

        #? simple report - check if the principal have allowed some actions in the specific resource
        if match_all_actions: #? must contain all specified actions
            has_any_action_allowed = not(any([(r['EvalDecision'] == 'implicitDeny' or r['EvalDecision'] == 'implicitDeny') for r in response['EvaluationResults']]))
        else:
            has_any_action_allowed = any([(r['EvalDecision'] == 'allowed') for r in response['EvaluationResults']])
            # has_any_action_allowed = any([(r['EvalResourceDecision'] == 'allowed') for r in response['EvaluationResults']['ResourceSpecificResults']])
        return has_any_action_allowed