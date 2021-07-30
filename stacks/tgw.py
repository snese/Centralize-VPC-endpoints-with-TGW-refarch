from aws_cdk import core
import aws_cdk.aws_ec2 as ec2

class Tgw(core.Stack):

    def __init__(self, scope: core.Construct, id: str, tgw_asn: int, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Transit Gateway creation
        self.tgw = ec2.CfnTransitGateway(
            self,
            id=f"tgw-vpc-{kwargs['env']['region']}",
            amazon_side_asn=tgw_asn,
            auto_accept_shared_attachments="enable",
            default_route_table_association="enable",
            default_route_table_propagation="enable",
        )


# # class TgwRoute(core.Stack):

#     def __init__(self, scope: core.Construct, id: str, network_stack: core.Stack, tgw_stack: core.Stack, **kwargs) -> None:
#         super().__init__(scope, id, **kwargs)

#         # Set the default route on the subnets to the TGW
#         for subnet in self.vpc.isolated_subnets:
#             ec2.CfnRoute(
#                 self,
#                 id='vpc_route_all_tgw',
#                 route_table_id=subnet.route_table.route_table_id,
#                 destination_cidr_block='0.0.0.0/0',
#                 transit_gateway_id=tgw_stack.tgw.ref
#             )