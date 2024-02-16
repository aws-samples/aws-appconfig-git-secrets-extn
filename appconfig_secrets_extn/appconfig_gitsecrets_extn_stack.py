# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from typing import cast
from aws_cdk import (
    aws_appconfig_alpha as appconfig,
    aws_lambda,
    aws_iam as iam,
    Stack,
)
from constructs import Construct


class AppconfigGitSecretsExtnStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        function = aws_lambda.DockerImageFunction(
            self,
            "gitsecrets_check_fn",
            code=aws_lambda.DockerImageCode.from_image_asset(
                "lambda",
                exclude=[".venv", ".mypy_cache", ".ruff_cache"],
                file="Dockerfile",
            ),
            # should also be fine on X86_64
            architecture=aws_lambda.Architecture.ARM_64,
            description="AppConfig Extension to check for secrets in configuration data with git-secrets",
        )

        appconfig_svc_role = iam.Role(
            self,
            "appconfig_role",
            assumed_by=cast(
                iam.IPrincipal, iam.ServicePrincipal("appconfig.amazonaws.com")
            ),
        )
        function.grant_invoke(appconfig_svc_role)

        appconfig.Extension(
            self,
            "gitsecrets_exten",
            actions=[
                appconfig.Action(
                    action_points=[appconfig.ActionPoint.PRE_START_DEPLOYMENT],
                    description="Check configuration data for secrets",
                    event_destination=appconfig.LambdaDestination(
                        cast(aws_lambda.IFunction, function)
                    ),
                ),
            ],
            extension_name="git-secrets",
            description="Checks for secrets in configuration data using the git-secrets tool",
        )
