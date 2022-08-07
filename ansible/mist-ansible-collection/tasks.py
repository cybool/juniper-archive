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

# ---------------------------------------------------------------------------
# DOCKER PARAMETERS
# ---------------------------------------------------------------------------
DOCKER_IMG = "ghcr.io/cdot65/mist-ansible-collection"
DOCKER_TAG = "0.0.4"

# ---------------------------------------------------------------------------
# ANSIBLE GALAXY PARAMETERS
# ---------------------------------------------------------------------------
GALAXY_KEY = os.getenv("GALAXY_KEY", "")
COLLECTION_PACKAGE = f"cdot65-mist-{DOCKER_TAG}.tar.gz"

# ---------------------------------------------------------------------------
# SYSTEM PARAMETERS
# ---------------------------------------------------------------------------
PWD = os.getcwd()


# ---------------------------------------------------------------------------
# DOCKER CONTAINER BUILD
# ---------------------------------------------------------------------------
@task
def build(context):
    """Build our docker image."""
    context.run(
        f"docker build -t {DOCKER_IMG}:{DOCKER_TAG} docker/",
    )


# ---------------------------------------------------------------------------
# COLLECTIONS BUILD
# ---------------------------------------------------------------------------
@task
def collection(context):
    """Build Ansible Galaxy Collection within container."""
    context.run(
        f"docker run \
            -it \
            --rm \
            -v {PWD}/cdot65/mist:/home/mist \
            -w /home/mist/ \
            {DOCKER_IMG}:{DOCKER_TAG} \
            ansible-galaxy collection build --force",
        pty=True,
    )


@task
def install(context):
    """Build Ansible Galaxy Collection within container but install on host."""
    context.run(
        f"docker run \
            -it \
            --rm \
            -v {PWD}/cdot65/mist:/home/mist \
            -v {PWD}/docker:/home/mist/docker \
            -w /home/mist/ \
            {DOCKER_IMG}:{DOCKER_TAG} \
            ansible-galaxy collection build --force --output-path docker/ \
            && \
            ansible-galaxy collection install ./docker/cdot65-mist-0.0.4.tar.gz --force",
        pty=True,
    )


# ---------------------------------------------------------------------------
# PUBLISH ANSIBLE COLLECTION TO GALAXY
# ---------------------------------------------------------------------------
@task
def publish(context):
    """Publish our Ansible Galaxy Collection within container."""
    context.run(
        f"docker run \
            -it \
            --rm \
            -v {PWD}/cdot65/mist:/home/mist \
            -v {PWD}/docker:/home/mist/docker \
            -w /home/mist/ \
            {DOCKER_IMG}:{DOCKER_TAG} \
            ansible-galaxy collection publish ./docker/{COLLECTION_PACKAGE} --api-key={GALAXY_KEY}",
        pty=True,
    )


# ---------------------------------------------------------------------------
# DOCKER CONTAINER SHELL
# ---------------------------------------------------------------------------
@task
def shell(context):
    """Get access to the BASH shell within our container."""
    context.run(
        f"docker run -it --rm \
            -v {PWD}/cdot65/mist:/home/mist \
            -w /home/mist/ \
            {DOCKER_IMG}:{DOCKER_TAG} /bin/bash",
        pty=True,
    )


# ---------------------------------------------------------------------------
# TESTS
# ---------------------------------------------------------------------------
@task
def test(context):
    """Test the playbook by running it within the container."""
    context.run(
        f"docker run -it --rm \
            -v {PWD}/cdot65/mist:/home/mist \
            -w /home/mist/ \
            {DOCKER_IMG}:{DOCKER_TAG} sh tests/build.sh",
        pty=True,
    )


@task
def inventory(context):
    """Check out the inventory file."""
    context.run(
        f"docker run -it --rm \
            -v {PWD}/cdot65/mist:/home/mist \
            -w /home/mist/ \
            {DOCKER_IMG}:{DOCKER_TAG} cat /etc/ansible/inventory.yaml",
        pty=True,
    )
