#!/usr/bin/env python
"""SNMP Script to return NAT pool available addresses inside a logical system.

:Author: Calvin Remsburg
:Contact: cremsburg.dev@gmail.com
:Date: 04/17/2022
:Version: 0.0.1
"""
import jcs  # pylint: disable=import-error

from jnpr.junos import Device  # pylint: disable=import-error


def main():
    """Primary execution of script.

    Workflow
    ---------------------------------------------------------------------------
        Receives the SNMP action type and OID by importing from jcs methods.
        Create a filter to find our available NAT addresses.
        Opens a connection to the local device API
        Request for information on our NAT source pools with RPC
            <rpc>
                <retrieve-source-nat-pool-information>
                        <pool-name>NAT_POOL_RHEL8</pool-name>
                        <logical-system>LSYS_DMZ</logical-system>
                </retrieve-source-nat-pool-information>
            </rpc>
        Store output of our RPC call to a file
    """

    snmp_action = jcs.get_snmp_action()
    snmp_oid = jcs.get_snmp_oid()

    dev = Device()
    dev.open()

    try:
        result = dev.rpc.retrieve_source_nat_pool_information(
            pool_name="NAT_POOL_RHEL8", logical_system="LSYS_DMZ", normalize=True
        )

        addresses = result.xpath(".//address-available")[0].text
        message = "addresses available " + addresses

    except TypeError:
        message = "SNMP Script failed"

    dev.close()

    jcs.syslog(
        "6",
        snmp_action,
        " received for ",
        snmp_oid,
        " - executing app.py script.",
    )

    if snmp_action == "get":
        if snmp_oid == ".1.3.6.1.4.1.2636.13.61.1.9.1.1.82":
            jcs.emit_snmp_attributes(snmp_oid, "Integer32", addresses)

    elif snmp_action == "get-next":
        if snmp_oid == ".1.3.6.1.4.1.2636.13.61.1.9.1.1":
            jcs.emit_snmp_attributes(
                ".1.3.6.1.4.1.2636.13.61.1.9.1.1.1", "Integer32", addresses
            )


if __name__ == "__main__":
    main()
