from jnpr.junos import Device
from pprint import pprint
import xml.etree.ElementTree as et
import json
import xmltodict
from lxml import etree

with Device(host='dallas-leaf4', user='automation', password='juniper123',use_filter=True) as network_device:
    filter = '<route-information><route-table/></route-information>'
    try:
        route_table = network_device.rpc.get_route_information(filter_xml=filter)
        print(etree.tostring(route_table, encoding='unicode'))
    except:
        pass


# with Device(host='router.example.com', use_filter=True) as dev:
#     filter = '<interface-information><physical-interface><name/></physical-interface></interface-information>'
#     result = dev.rpc.get_interface_information(filter_xml=filter)
#     print (etree.tostring(reply, encoding='unicode'))









# # print(interface.xpath(".//address-family[normalize-space(address-family-name)='inet']/interface-address/ifa-local")[0].text")

# # for element in interface.iter():
# #     print(element)



# entry = route_table.xpath('route-table/rt/rt-destination[contains(text(), "50:00:00:0d:00:00")]/parent::*')

# to_string  = et.tostring(entry, encoding='UTF-8', method='xml')

# print(to_string)
# for each in entry:
#     data_dict = xmltodict.parse(each)
#     x = json.dumps(data_dict)
#     print(x)

# # for each in entry:
# #     print(etree.tostring(each, encoding='unicode'))

# # ip_addresses = interfaces.xpath(".//address-family[normalize-space(address-family-name)='inet']/interface-address/ifa-local")

# # for each in interfaces:
# #     print(each.text)

# # result = dev.rpc.get_interface_information(filter_xml=filter)
# # print (etree.tostring(route_table, encoding='unicode'))
