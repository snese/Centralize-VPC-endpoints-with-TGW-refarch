#!/usr/bin/env python3
import os
from aws_cdk import core as cdk

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core
from stacks.networks import Network
from stacks.ec2 import Ec2
from stacks.tgw import Tgw, TgwAttachmentAndRoute
from stacks.vpce import Vpce

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
tgw_stack = Tgw(app, "tgw-stack",
        tgw_asn=64513,
        env=env
    )

## VPC & Attachment & Route

### VPC0 Shared
network_stack_0_shared = Network(app, "network-stack-0-shared",
        cidr_range="172.16.0.0/16",
        tgw_stack=tgw_stack,
        env=env
    )

### VPC1 Spoke
network_stack_1_spoke = Network(app, "network-stack-1-spoke",
        cidr_range="172.16.1.0/16",
        tgw_stack=tgw_stack,
        env=env
    )

### VPC2 Spoke
network_stack_2_spoke = Network(app, "network-stack-2-spoke",
        cidr_range="172.16.2.0/16",
        tgw_stack=tgw_stack,
        env=env
    )

## TODO VPCe 

## TODO Route53

## TODO Instances

app.synth()