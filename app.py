#!/usr/bin/env python3
import os
from typing_extensions import TypeGuard
from stacks.vpce import Vpce
from aws_cdk import core
from stacks.networks import Network
# from stacks.ec2 import Ec2
from stacks.tgw import Tgw
# from stacks.vpce import Vpce

app = core.App()

# ap-southeast-1

## INIT
# env=core.Environment(
#     account=os.environ.get("CDK_DEPLOY_ACCOUNT", os.environ["CDK_DEFAULT_ACCOUNT"]),
#     region=os.environ.get("CDK_DEPLOY_REGION", os.environ["CDK_DEFAULT_REGION"])
# )

env={
    'region': 'ap-southeast-1',
    }

## TGW
tgw_regional_stack = Tgw(app, "tgw-stack",
        tgw_asn=64513,
        env=env
    )

## VPC & Attachment & Route

### VPC0 Shared
network_stack_0_shared = Network(app, "network-stack-0-shared",
        cidr_range="172.16.0.0/24",
        tgw_stack=tgw_regional_stack,
        has_endpoints=True,
        env=env
    )

### VPC1 Spoke
network_stack_1_spoke = Network(app, "network-stack-1-spoke",
        cidr_range="172.16.1.0/24",
        tgw_stack=tgw_regional_stack,
        has_endpoints=False,
        env=env
    )

### VPC2 Spoke
network_stack_2_spoke = Network(app, "network-stack-2-spoke",
        cidr_range="172.16.2.0/24",
        tgw_stack=tgw_regional_stack,
        has_endpoints=False,
        env=env
    )

## TODO Route53

## TODO Instances

app.synth()