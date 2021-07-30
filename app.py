#!/usr/bin/env python3
import os
from aws_cdk import core
from stacks.networks import Network
from stacks.tgw import Tgw
from stacks.ec2 import Ec2

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
#### VPCe and Create Private Host Zone
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

## TODO 
# [] Route53 Associate
# [] Instances

## Instance
ec2_stack_0_shared = Ec2(app, id="instance-stack-0-shared",
        network_stack=network_stack_0_shared, 
        env=env
    )

ec2_stack_1_spoke = Ec2(app, id="instance-stack-1-spoke",
        network_stack=network_stack_1_spoke, 
        env=env
    )

ec2_stack_2_spoke = Ec2(app, id="instance-stack-2-spoke",
        network_stack=network_stack_2_spoke, 
        env=env
    )

## Add Dependency
ec2_stack_0_shared.add_dependency(network_stack_0_shared)
ec2_stack_1_spoke.add_dependency(network_stack_1_spoke)
ec2_stack_2_spoke.add_dependency(network_stack_2_spoke)

app.synth()