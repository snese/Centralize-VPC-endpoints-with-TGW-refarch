from aws_cdk import (core,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_autoscaling as autoscaling,
)

class Ec2(core.Stack):

    def __init__(self, scope: core.Construct, id: str, network_stack: core.Stack, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create ServiceRole for EC2 instances; enable SSM usage
        ec2_instance_role = iam.Role(self, "Role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")],
            description="This is a custom role for assuming the SSM role"
        )

        # Create security group
        ec2_sg = ec2.SecurityGroup(
            self,
            id='test-ec2-instance-sg',
            vpc=network_stack.vpc
        )

        # Create Ingress rule to allow ping
        ec2_sg.add_ingress_rule(
            ec2.Peer.ipv4('172.16.0.0/16'),
            ec2.Port.all_icmp()
        )

        # Auto-scaling group
        asg = autoscaling.AutoScalingGroup(self, "ASG", 
            vpc=network_stack.vpc,
            role=ec2_instance_role,
            instance_type=ec2.InstanceType.of(
                instance_class=ec2.InstanceClass.BURSTABLE2,
                instance_size=ec2.InstanceSize.MICRO,
            ),
            machine_image=ec2.AmazonLinuxImage(
              generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            ),
            desired_capacity=1500,
            max_capacity=2000,
            min_capacity=1000)

        asg.add_security_group(ec2_sg)
