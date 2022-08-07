# Ansible Collection - cdot65.mist

[![N|Solid](https://raw.githubusercontent.com/cdot65/svg-locker-shhhhh/master/Mist-Juniper-Logo-Full-Color.png)](https://juniper.net/)

## Overview

The goal of this collection is to provide an easier way to interact with Juniper's Mist solution. While nothing will stop you from using the built-in module, you may find that working with pre-packaged modules can help simplify the development of your playbook, or it may just be easier to support as a team.

## 📋 Ansible version compatibility

Ansible has performed a significant change to their versioning lately, we will be testing with versions 2.10.x

## Batteries Included

Here is a short list of modules included within the collection, expect feature parity with the Postman Collection before this project hits `version 0.1.0`

| Name                                                                                                                                | Description                    |
| ----------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| [cdot65.mist.gateway](https://github.com/cdot65/mist-ansible-collection/blob/main/cdot65/mist/docs/cdot65.mist.gateway.rst)         | Configure SRX and 128T devices |
| [cdot65.mist.site](https://github.com/cdot65/mist-ansible-collection/blob/main/cdot65/mist/docs/cdot65.mist.site.rst)               | Manage sites                   |
| [cdot65.mist.site_groups](https://github.com/cdot65/mist-ansible-collection/blob/main/cdot65/mist/docs/cdot65.mist.site_groups.rst) | Manage site groups             |
| [cdot65.mist.wired](https://github.com/cdot65/mist-ansible-collection/blob/main/cdot65/mist/docs/cdot65.mist.wired.rst)             | Manage wired configurations    |
| [cdot65.mist.wlan](https://github.com/cdot65/mist-ansible-collection/blob/main/cdot65/mist/docs/cdot65.mist.wlan.rst)               | Manage wireless configurations |

## 🚀 Executing the playbook

After installing the collections, you can call the modules by using their full name path.

> test.yaml

```yaml
---
- name: "Gateway: create a device configuration"
  cdot65.mist.gateway:
    # mist parameters
    baseurl: "{{ mist.url }}"
    api_token: "{{ mist.token }}"
    org_id: "{{ mist.org }}"

    # srx parameters
    name: "{{ gateway_hostname }}"
    site_name: "{{ site_name }}"
    bgp_config:
      - name: "ATT"
        type: "external"
        local_as: 42551
        auth_key: "juniper123"
        export_policy: "direct"
        neighbors:
          - name: "74.51.192.0"
            neighbor_as: 42550
            export_policy: "direct"
            import_policy: ""
    additional_config_cmds:
      - "set protocols bgp group ATT local-address {{ wan_ip }}"
    state: "present"
```

Then simply run your playbook

```bash
ansible-playbook test.yaml
```

If you used Ansible Vault to encrypt your secrets, you need to append the `--ask-vault-pass` to your command.

## Very Important!

Please make sure to manage your sensative information carfully. While the modules support the parameter of `api_key`, this should never be statically entered with your token in clear text.

Here are better alternatives:

### Manage your API token as an environmental

```bash
export MIST_API_TOKEN='YOUR_PRIVATE_KEY_HERE'
```

> you can also use `MIST_API_KEY`, if you prefer

### Manage your API token as a secret with Ansible Vault

create a file to store your API token in

> vim vault.yaml

```yaml
api_token: "MY_MIST_API_TOKEN_HERE"
```

encrypt the new file

```bash
ansible-vault encrypt vault.yml
```

and now you'll need to pass your vault password when using the playbook

```bash
ansible-playbook --ask-vault-pass test.yaml
```

## Development

Want to contribute? Great!

Submit a PR and let's work on this together :D
