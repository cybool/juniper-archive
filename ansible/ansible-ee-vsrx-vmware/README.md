# Ansible Execution Environment: vSRX on vCenter

[![N|Solid](https://camo.githubusercontent.com/5b26c37b2457faffe6e59e931542539cd79b7169e7e2b80d735825013d274a67/68747470733a2f2f75706c6f61642e77696b696d656469612e6f72672f77696b6970656469612f636f6d6d6f6e732f332f33312f4a756e697065725f4e6574776f726b735f6c6f676f2e737667)](https://juniper.net/)

## Overview

This project aims to bring the ability to deploy a Juniper vSRX on VMware vCenter through the construct of an Execution Environment.

### 🐍 `Prep your Python environment`

I have included a Poetry file for anyone saavy enough to take advantage. For the uninitiated, Poetry helps replicate Python environments between users with a single file. You'll need to have Poetry installed on your machine, for most users that will be solved with `pip install poetry`.

1. install Python dependencies

```bash
poetry install
```

2. activate environment

```bash
poetry shell
```

## 🐳 `Executing the build`

build the container image with

```bash
ansible-builder build --tag ghcr.io/cdot65/ansible-ee-vsrx-vmware:latest
```
