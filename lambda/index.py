"""
Sample AWS AppConfig Extension to scan a configuration with git-secrets

Note that this requires Python>=3.12 for the `delete_on_close`
parameter to `NamedTemporaryFile`
"""

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import base64
import json
import logging
import os
import subprocess
from tempfile import NamedTemporaryFile

logger = logging.getLogger()
logger.setLevel(os.environ.get("LOGLEVEL", "INFO"))

# git wants a $HOME
if "HOME" not in os.environ:
    os.environ["HOME"] = "/tmp"

# stop git complaining about ownership of the directory
subprocess.run(["git", "config", "--global", "--add", "safe.directory", "/run/scan"])


def lambda_handler(event, context):
    logger.debug(json.dumps(event))
    if (event_type := event.get("Type")) != "PreStartDeployment":
        logger.critical("Wrong event type %s for this function, ignoring", event_type)
        return
    if config_content_64 := event.get("Content"):
        config_content = base64.b64decode(config_content_64).decode("utf-8")
        logger.debug(f"decoded content: {config_content}")
        temp_file = None
        with NamedTemporaryFile(delete_on_close=False) as temp_file:
            filename = temp_file.name
            temp_file.write(base64.b64decode(config_content_64))
            temp_file.close()
            secrets_info = subprocess.run(
                ["git", "secrets", "--scan", filename],
                cwd="/var/run/scan",
                capture_output=True,
            )
            if secrets_info.returncode != 0:
                response = {
                    "Error": "BadRequest",
                    "Message": "A secret was detected by git-secrets",
                    "Details": [],
                }
                logger.info(json.dumps(response))
                return response
    logger.info("Configuration validated")
