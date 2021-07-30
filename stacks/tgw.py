from aws_cdk import core
import aws_cdk.aws_ec2 as ec2

class Tgw(core.Stack):

    def __init__(self, scope: core.Construct, id: str, tgw_asn: int, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Transit Gateway creation
        self.tgw = ec2.CfnTransitGateway(self, id=f"tgw-vpc-{kwargs['env']['region']}",
            amazon_side_asn=tgw_asn,
            auto_accept_shared_attachments="enable",
            default_route_table_association="enable",
            default_route_table_propagation="enable",
        )
