"""Tasks for use with Invoke.

(c) 2021 Calvin Remsburg
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
from invoke import task

### ---------------------------------------------------------------------------
### DOCKER PARAMETERS
### ---------------------------------------------------------------------------
DOCKER_IMG = "registry.gitlab.com/cremsburg/juniper-automation-container"
DOCKER_TAG = "software-upgrade"

### ---------------------------------------------------------------------------
### SYSTEM PARAMETERS
### ---------------------------------------------------------------------------
PWD = os.getcwd()

### ---------------------------------------------------------------------------
### DOCKER CONTAINER BUILD
### ---------------------------------------------------------------------------
@task
def build(context):
    # Build our docker image
    context.run(
        f"docker build -t {DOCKER_IMG}:{DOCKER_TAG} files/docker/",
    )

### ---------------------------------------------------------------------------
### DOCKER CONTAINER SHELL
### ---------------------------------------------------------------------------
@task
def shell(context):
    # Get access to the BASH shell within our container
    print("Jumping into container, type exit to return to host")
    context.run(
        f"docker run -it --rm \
            -v {PWD}/files/ansible/:/home/ansible \
            -w /home/ansible/ \
            --env-file	{PWD}/files/docker/.env \
            {DOCKER_IMG}:{DOCKER_TAG} /bin/bash",
        pty=True,
    )

### ---------------------------------------------------------------------------
### UPGRADE SOFTWARE FROM WITHIN THE CONTAINER
### ---------------------------------------------------------------------------
@task
def upgrade(context):
    # Execute Ansible playbook from within the container
    context.run(
        f"docker run -it \
            --rm \
            --env-file	{PWD}/files/docker/.env \
            -v {PWD}/files/ansible/:/home/ansible \
            -w /home/ansible/ \
            {DOCKER_IMG}:{DOCKER_TAG} ansible-playbook pb.junos.upgrade.yaml",
        pty=True,
    )
