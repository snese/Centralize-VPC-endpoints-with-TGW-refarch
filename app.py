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

app = core.App()

# us-east-1
# netowrk
network_stack_us_east_1 = Network(app, "network-us-east-1",
        cidr_range="172.16.0.0/16",
        env=core.Environment(
            region="us-east-1")
    )

# ec2
ec2_stack_us_east_1 = Ec2(app, id="instance-us-east-1",
        network_stack=network_stack_us_east_1, 
        env=core.Environment(
            region="us-east-1")
    )


ec2_stack_us_east_1.add_dependency(network_stack_us_east_1)

app.synth()