import pulumi
import pulumi_aws as aws

def init():
    # Create VPC
    vpc = aws.ec2.Vpc("main", cidr_block="10.0.0.0/16")

    # Internet gateway
    egress_only_igw = aws.ec2.InternetGateway("igw",
    tags ={
        "provision": "pulumi",
        "project": "common",
        "stage": pulumi.get_stack(),
    },
    vpc_id = vpc.id)

    # Attach subnets
    public_subnet1 = aws.ec2.Subnet("public-1a",
        cidr_block="10.0.1.0/24",
        tags={
            "provision":"pulumi",
            "type": "public",
            "project": "common",
            "stage": pulumi.get_stack(),
        },
        vpc_id = vpc.id)

    public_subnet2 = aws.ec2.Subnet("public-1b",
        cidr_block="10.0.2.0/24",
        tags={
            "provision":"pulumi",
            "type": "public",
            "project": "common",
            "stage": pulumi.get_stack(),
        },
        vpc_id = vpc.id)

    private_subnet1 = aws.ec2.Subnet("private-1a",
        cidr_block="10.0.3.0/24",
        tags={
            "provision":"pulumi",
            "type": "private",
            "project": "common",
            "stage": pulumi.get_stack(),
        },
        vpc_id = vpc.id)

    private_subnet2 = aws.ec2.Subnet("private-1b",
        cidr_block="10.0.4.0/24",
        tags={
            "provision":"pulumi",
            "type": "private",
            "stage": pulumi.get_stack(),
            "project": "common"
        },
        vpc_id = vpc.id)


    # NACL
    aws.ec2.NetworkAcl("main",
        egress=[{
            "action": "allow",
            "cidrBlock": public_subnet1.cidr_block,
            "fromPort": 443,
            "protocol": "tcp",
            "ruleNo": 200,
            "toPort": 443,
        }],
        ingress=[{
            "action": "allow",
            "cidrBlock": "10.3.0.0/18",
            "fromPort": 80,
            "protocol": "tcp",
            "ruleNo": 100,
            "toPort": 80,
        }],
        tags={
            "provision": "pulumi",
            "stage": pulumi.get_stack(),
            "project": "common"
        },
        vpc_id=vpc.id)

    # Route table
    rt = aws.ec2.RouteTable("routeTable",
    routes=[
        {
            "gatewayId": egress_only_igw.id,
            "cidrBlock": "0.0.0.0/0",
        }
    ],
    tags={
        "provision": "pulumi",
        "stage": pulumi.get_stack(),
        "project": "common"
    },
    vpc_id=vpc.id)

    aws.ec2.RouteTableAssociation("routeTableAssociation-publicsubnet1",
    subnet_id=public_subnet1.id,
    route_table_id = rt.id)

    aws.ec2.RouteTableAssociation("routeTableAssociation-publicsubnet2",
    subnet_id=public_subnet2.id,
    route_table_id = rt.id)

    pulumi.export("vpc_id", vpc.id)
    pulumi.export("public_subnets",[public_subnet1.id, public_subnet2.id])
    pulumi.export("private_subnets",[private_subnet1.id, private_subnet2.id])