# JSNAPY example: Validate NAT policies

[![N|Solid](https://upload.wikimedia.org/wikipedia/commons/3/31/Juniper_Networks_logo.svg)](https://junos-ansible-modules.readthedocs.io/en/stable/)

## Overview

This example will show how to use JSNAPy to make sure the expected NAT policy matches are taking place.

In addition to the Ansible playbok, this project also ships with additional tools to help you along your way. You will find a Dockerfile for running the project in an isolated environment, and an Invoke tasks file for those of us that hate typing out everything all the time.

## ⚙️ `How it works`

The data is collected from the firewalls by issuing NETCONF RPCs to retrieve the data as XML, to which Ansible will automatically translate into a dictionary for us.

There are two filter plugins for this project, which will help us transform the data and perform basic logic operations in Python.

Let's take a second to review the documentation in the `files/docs/` directory.

Name | Description
---- | -----------
[Ansible Playbook](files/docs/pb.jsnapy.firewall.nat.yaml.rst) | Validate NAT policies with JSNAPy
[Inventory file](files/docs/inventory.rst) | Inventory

## 📝 `Dependencies`

Refer to the Poetry Lock file located at [poetry.lock](poetry.lock) for detailed descriptions on each package installed.

## 🚀 `Executing the playbook`

This project provides two unique methods of executing the playbook:

[Executing with Docker](files/docs/execute_with_docker.rst) | Execute with Docker

[Executing with Python](files/docs/execute_with_python.rst) | Execute with Python

## Note for Ansible Tower / AWX users

You'll note that there is an ansible.cfg file found in the root of the project's directory, the only purpose this serves is for Ansible Tower / AWX, which will look for these files when the project syncs from Gitlab/Github/Whatever, and Tower will auto-install the packages.

The ansible.cfg file will be the definitive for each Playbook (Template) execution, so super important to keep it here.
