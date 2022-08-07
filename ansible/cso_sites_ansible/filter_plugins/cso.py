class FilterModule(object):

    def find_cpe(self, value, expectedvalue):
        # cpe = {}
        for each in value:
            if each['device_type'] == 'cpe':
                if expectedvalue == 'family':
                    return each['device_family_info']['family']
                elif expectedvalue == 'serial':
                    return each['device_serial_number']

    def get_tenant_sites(self, value):
        import json
        sites = []

        for each in value['tenant-sites']:
          site = {}
          for fq in each['fq_name']:
            if "OAM" in fq:
              pass
            elif "JNPR" in fq:
              pass
            else:
              site["name"] = each["fq_name"][0]
              site["uuid"] = each["uuid"]
              site["href"] = each["href"]
              sites.append(site)
        return sites

    def filters(self):
        return {
            'find_cpe': self.find_cpe,
            'get_tenant_sites': self.get_tenant_sites,
        }

