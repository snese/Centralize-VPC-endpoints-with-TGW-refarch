from aws_cdk import core
import aws_cdk.aws_ec2 as ec2


class Vpce(core.Stack):

    def __init__(self, scope: core.Construct, id: str, network_stack: core.Stack, private_dns_enabled: bool, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc=network_stack.vpc

        # VPC Endpoint creation for SSM (3 Endpoints needed)
        ec2.InterfaceVpcEndpoint(
            self,
            "VPCe - SSM",
            service=ec2.InterfaceVpcEndpointService(
                core.Fn.sub("com.amazonaws.${AWS::Region}.ssm")
            ),
            private_dns_enabled=private_dns_enabled,
            vpc=self.vpc,
        )

        ec2.InterfaceVpcEndpoint(
            self,
            "VPCe - EC2 Messages",
            service=ec2.InterfaceVpcEndpointService(
                core.Fn.sub("com.amazonaws.${AWS::Region}.ec2messages")
            ),
            private_dns_enabled=private_dns_enabled,
            vpc=self.vpc,
        )

        ec2.InterfaceVpcEndpoint(
            self,
            "VPCe - SSM Messages",
            service=ec2.InterfaceVpcEndpointService(
                core.Fn.sub("com.amazonaws.${AWS::Region}.ssmmessages")
            ),
            private_dns_enabled=private_dns_enabled,
            vpc=self.vpc,
        )
        
        # VPC Endpoint creation for SQS
        ec2.InterfaceVpcEndpoint(
            self,
            "VPCe - SQS",
            service=ec2.InterfaceVpcEndpointService(
                core.Fn.sub("com.amazonaws.${AWS::Region}.sqs")
            ),
            private_dns_enabled=private_dns_enabled,
            vpc=self.vpc,
        )
