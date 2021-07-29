from aws_cdk import core
import aws_cdk.aws_ec2 as ec2


class Network(core.Stack):

    def __init__(self, scope: core.Construct, id: str, cidr_range: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

       # VPC Creation
        self.vpc = ec2.Vpc(self,
            "vpc",
            max_azs=1,
            cidr=cidr_range,
            # configuration will create 1 subnet in a single AZ.
            subnet_configuration=[ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.ISOLATED,
                    name="Isolated",
                    cidr_mask=20
                    )
            ]
        )

        # VPC Endpoint creation for SSM (3 Endpoints needed)
        ec2.InterfaceVpcEndpoint(
            self,
            "VPCe - SSM",
            service=ec2.InterfaceVpcEndpointService(
                core.Fn.sub("com.amazonaws.${AWS::Region}.ssm")
            ),
            private_dns_enabled=True,
            vpc=self.vpc,
        )

        ec2.InterfaceVpcEndpoint(
            self,
            "VPCe - EC2 Messages",
            service=ec2.InterfaceVpcEndpointService(
                core.Fn.sub("com.amazonaws.${AWS::Region}.ec2messages")
            ),
            private_dns_enabled=True,
            vpc=self.vpc,
        )

        ec2.InterfaceVpcEndpoint(
            self,
            "VPCe - SSM Messages",
            service=ec2.InterfaceVpcEndpointService(
                core.Fn.sub("com.amazonaws.${AWS::Region}.ssmmessages")
            ),
            private_dns_enabled=True,
            vpc=self.vpc,
        )
