#!/bin/sh

# Copyright 2021, Calvin Remsburg
# https://twitter.com/_calvinr
#
# Licensed under the MIT license:
# https://opensource.org/licenses/MIT

ansible-galaxy collection install -r collections/requirements.yml -p /etc/ansible/collections
ansible-playbook pb.build.blueprint.yaml
