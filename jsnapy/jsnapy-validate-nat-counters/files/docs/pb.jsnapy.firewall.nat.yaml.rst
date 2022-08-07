===========================
pb.jsnapy.firewall.nat.yaml
===========================

---------------------
Validate NAT policies
---------------------

We will be using JSNAPy to validate that NAT policy counters are not zero.

RETRIEVE NAT COUNTERS
=====================

In this first block we will retrieve the NAT counters per active policy on the device.

Authentication
--------------

There is an expectation that you pass your username/password combination. In the example above, we are executing the playbook through Ansible AWX/Tower, so authentication is taken care of for us.

The Docker execution will have an `.env` file for you to update with your username/password.

The native execution with Python will need to add the `user` and `passwd` as extra variables, or update the module accordingly, check out the [Docker](files/docs/execute_with_docker.rst) for an example

Example
-------

Here is the YAML defining our task from the playbook:

.. code-block:: yaml

    - name: "### RETRIEVE NAT COUNTERS ###"
      block:

        - name: "Request counters for NAT policies"
          juniper_junos_jsnapy:
            host: "{{ ansible_host }}"
            test_files: tests/firewall.yaml
            action: snapcheck
          register: test_firewall
          ignore_errors: True

        - name: "print test_firewall object to screen"
          debug:
            msg: "{{ test_firewall }}"
          when:
            - "test_firewall.passPercentage != 100"

Explanation
-----------

We leverage the Ansible module `juniper_junos_jsnapy` to request the execution of our test file found in the `tests/` path. 

Using the snapcheck functionality of JSNAPy allows us to perform an assertion within our test.

`ignore_errors` is set to true to allow for a device to return a failed test.

We store the output as a new object called `test_firewall`, which will be printed out to the screen if the pass percentage is not equal to 100%.

Here's an example of what `test_firewall` should look like:


PERFORM ASSERTIONS
==================

Here we will ensure that the results were 100%, using Ansible's built-in plugin for assertions.

.. code-block:: yaml

    - name: "ensure all tests passed"
      ansible.builtin.assert:
        that:
          - "test_firewall.passPercentage == 100"


