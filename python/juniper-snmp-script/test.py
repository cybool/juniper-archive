from jnpr.junos import Device
import ipdb


with Device(host="dc-fw1") as dev:
    try:
        result = dev.rpc.retrieve_source_nat_pool_information(
            pool_name="NAT_POOL_RHEL8", logical_system="LSYS_DMZ", normalize=True
        )
        ipdb.set_trace(context=5)  # will show five lines of code

        addresses = result.xpath(".//address-available")[0].text

        # result = dev.rpc.retrieve_source_nat_pool_information(
        #     pool_name="NAT_POOL_RHEL8", logical_system="LSYS_DMZ", normalize=True
        # )
        # with open("/var/tmp/script.log", "w+", encoding="utf-8") as output_log:
        #     output_log.write(result)

        # available = result.xpath(".//address-available")[0].text
        # available_addresses = str(available.strip())
        # message = "addresses available " + available_addresses

    except TypeError:
        message = "SNMP Script failed, rpc=" + str(result)
