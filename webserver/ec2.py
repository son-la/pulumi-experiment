import pulumi
import pulumi_aws as aws

def init():
    ami = aws.get_ami(filters=[
        {
            "name": "name",
            "values": ["ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64-server-*"],
        },
        {
            "name": "virtualization-type",
            "values": ["hvm"],
        },
    ],
    most_recent=True,
    owners=["099720109477"])

    ec2_instance = aws.ec2.Instance("dev-machine",
        ami=ami.id,
        instance_type="t3.micro",
        tags={
            "provision": "pulumi",
            "stage": pulumi.get_stack(),
            "project": "webserver"
        })