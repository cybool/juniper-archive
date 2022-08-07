#!/bin/sh

# ############################################################################
# # Several steps acheived within this script
# #   - Builds our Ansible collection
# #   - Installs our collection
# #   - Executes our Ansible Playbooks in a serial fashion
# ############################################################################
#
# Copyright 2021, Calvin Remsburg
#
# Licensed under the MIT license:
# https://opensource.org/licenses/MIT

export MIST_API_KEY="2RksylML2Xo5JzEflzK9B1AkUh0DlRdt6QCfUtlJcO39FGGgLM5tkXb8rxvGaRv79hNxnQujzkxbiQ0ThV0YueJ9Ipr4C9m1"
export MIST_ORG_ID="16c40b02-523a-414b-9e1e-1651519c747d"
export MIST_BASE_URL="https://api.mistsys.com/api/v1"
ansible-galaxy collection build --force
ansible-galaxy collection install ./cdot65-mist-0.0.4.tar.gz -p /etc/ansible/collections
cd tests/
ansible-playbook tests.yaml -vvv
# ansible-playbook site.yaml -vvv