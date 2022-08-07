"""Tasks for use with Invoke."""

import os
from invoke import task

# DOCKER PARAMETERS
DOCKER_IMG = "ghcr.io/files/ansible-vxlan-evpn-for-campus"
DOCKER_TAG = "0.0.1"

# ANSIBLE GALAXY PARAMETERS
GALAXY_KEY = os.getenv("GALAXY_KEY", "")
COLLECTION_PACKAGE = f"cdot65-ansible-{DOCKER_TAG}.tar.gz"

# SYSTEM PARAMETERS
PWD = os.getcwd()


# DOCKER CONTAINER BUILD
@task
def build(context):
    """Build our docker image."""
    context.run(
        f"docker build -t {DOCKER_IMG}:{DOCKER_TAG} files/docker/",
    )


# CREATE VLANS
@task
def config(context):
    """Build configurations."""
    context.run(
        f"docker run \
            -it \
            --rm \
            -v {PWD}/files/ansible:/home/ansible \
            -w /home/ansible/ \
            {DOCKER_IMG}:{DOCKER_TAG} \
            ansible-playbook pb.configuration.build.yml",
        pty=True,
    )


# DOCKER CONTAINER SHELL
@task
def shell(context):
    "Jump into a container."
    context.run(
        f"docker run -it --rm \
            -v {PWD}/files/ansible:/home/ansible \
            -w /home/ansible/ \
            {DOCKER_IMG}:{DOCKER_TAG} /bin/bash",
        pty=True,
    )
