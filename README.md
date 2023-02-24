# iam-policy-analyzer

Create a json file in the current directory containing the desired actions and resources

Example:

```json
{
    "actions": [
        "dynamodb:GetItem"
    ],
    "resources": [
        "*"
    ]
}
```

A csv file will be generated in the example format:

account      | arn                                  | name  | actions                | resource
------------ | ------------------------------------ | ----- | ---------------------- | --------
XXXXXXXXXXXX | arn:aws:iam::XXXXXXXXXXXX:role/ADMIN | ADMIN | "['dynamodb:GetItem']" | *