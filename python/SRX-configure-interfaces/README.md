# Configure SRX interfaces with Scrapli

[![N|Solid](https://upload.wikimedia.org/wikipedia/commons/3/31/Juniper_Networks_logo.svg)](https://junos-ansible-modules.readthedocs.io/en/stable/)

## Overview

This example will show how to configure interfaces on Juniper's SRX firewalls.

In addition to the Python script, this project also ships with additional tools to help you along your way. You will find a Dockerfile for running the project in an isolated environment, and an Invoke `tasks.py` file for those of us that hate typing out everything all the time.

## ⚙️ `How it works`

The configuration is pushed to the device using the NETCONF API on board.

Let's take a second to review the documentation in the `files/docs/` directory.

Name | Description
---- | -----------
[app_async.py](files/docs/app_async.py.rst) | Configure interface `ge-0/0/1` on our firewalls with `asyncio`

## 📝 `Dependencies`

Refer to the Poetry Lock file located at [poetry.lock](poetry.lock) for detailed descriptions on each package installed.

## 🚀 `Executing the script`

This project provides two unique methods of executing the playbook:

[Executing with Docker](files/docs/execute_with_docker.rst) | Execute with Docker

[Executing with Python](files/docs/execute_with_python.rst) | Execute with Python
