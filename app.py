#!/usr/bin/env python3

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import aws_cdk as cdk

from appconfig_secrets_extn.appconfig_gitsecrets_extn_stack import (
    AppconfigGitSecretsExtnStack,
)

app = cdk.App()
AppconfigGitSecretsExtnStack(app, "AppconfigGitSecretsExtnStack")

app.synth()
