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


class TgwAttachmentAndRoute(core.Stack):

    def __init__(self, scope: core.Construct, id: str, network_stack: core.Stack, tgw_stack: core.Stack, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Transit Gateway attachment to the VPC
        self.tgw_attachment = ec2.CfnTransitGatewayAttachment(
            self,
            id=f"tgw-vpc-{kwargs['env']['region']}",
            transit_gateway_id=tgw_stack.tgw.ref,
            vpc_id=network_stack.vpc.ref,
            subnet_ids=[subnet.subnet_id for subnet in network_stack.isolated_subnets],
            tags=[core.CfnTag(key='Name', value=f"tgw-{network_stack.vpc_id}-attachment")]
        )

        # Set the default route on the subnets to the TGW
        for subnet in network_stack.vpc.isolated_subnets:
            ec2.CfnRoute(
                self,
                id='vpc_route_all_tgw',
                route_table_id=subnet.route_table.route_table_id,
                destination_cidr_block='0.0.0.0/0',
                transit_gateway_id=tgw_stack.ref
            )