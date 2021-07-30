from aws_cdk import core
import aws_cdk.aws_ec2 as ec2

class VpcConstruct(core.Construct):

    def __init__(self, scope: core.Construct, id: str, cidr_range: str, region: str, mazAz: int, tgw: str, has_endpoints: bool, **kwargs) -> None:
        super().__init__(scope, id)

    