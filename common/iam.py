import pulumi
import pulumi_aws as aws

def init():
    developers = [
        "Adrian",
        "Mark",
        "James"
    ]

    group = aws.iam.Group("developers", 
        path="/users/") 

    for developer in developers:
        user = aws.iam.User(developer,
            path = "/users/") 

        aws.iam.UserGroupMembership("membership-" + developer, 
            groups= [group.name],
            user= user.name
        )

    s3_fullaccess_for_developers = aws.iam.GroupPolicy("myDeveloperPolicy",
    group = group.id,
    policy="""{
        "Version": "2012-10-17",
        "Statement": [
            {
            "Action": [
                "s3:*"
            ],
            "Effect": "Allow",
            "Resource": "*"
            }
        ]
        }

        """)

    ec2_instance_assume_role_policy = aws.iam.get_policy_document(statements=[{
    "actions": ["sts:AssumeRole"],
    "principals": [{
        "identifiers": ["ec2.amazonaws.com"],
        "type": "Service",
        }],
    }])

    ec2_instance_role = aws.iam.Role("EC2Role",
        assume_role_policy=ec2_instance_assume_role_policy.json,
        path="/system/")

    ec2_instance_profile = aws.iam.InstanceProfile("testProfile", role=ec2_instance_role.name)
