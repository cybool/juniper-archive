
package main

import (
    "encoding/xml"
    "fmt"
    "github.com/hashicorp/terraform-plugin-sdk/helper/schema"
)


// v_ is appended before every variable so it doesn't give any conflict
// with any keyword in golang. ex - interface is keyword in golang
type xmlInterfacesInterface__RangeUnitFamilyEthernet__SwitchingVlanMembers struct {
	XMLName xml.Name `xml:"configuration"`
	Groups  struct {
		XMLName	xml.Name	`xml:"groups"`
		Name	string	`xml:"name"`
		V_interface__range  struct {
			XMLName xml.Name `xml:"interface-range"`
			V_name  *string  `xml:"name,omitempty"`
			V_unit  struct {
				XMLName xml.Name `xml:"unit"`
				V_name__1  *string  `xml:"name,omitempty"`
				V_vlan  struct {
					XMLName xml.Name `xml:"vlan"`
					V_members  *string  `xml:"members,omitempty"`
				} `xml:"family>ethernet-switching>vlan"`
			} `xml:"unit"`
		} `xml:"interfaces>interface-range"`
	} `xml:"groups"`
	ApplyGroup string `xml:"apply-groups"`
}

// v_ is appended before every variable so it doesn't give any conflict
// with any keyword in golang. ex- interface is keyword in golang
func junosInterfacesInterface__RangeUnitFamilyEthernet__SwitchingVlanMembersCreate(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
     	V_name := d.Get("name").(string)
	V_name__1 := d.Get("name__1").(string)
	V_members := d.Get("members").(string)


	config := xmlInterfacesInterface__RangeUnitFamilyEthernet__SwitchingVlanMembers{}
	config.ApplyGroup = id
	config.Groups.Name = id
	config.Groups.V_interface__range.V_name = &V_name
	config.Groups.V_interface__range.V_unit.V_name__1 = &V_name__1
	config.Groups.V_interface__range.V_unit.V_vlan.V_members = &V_members

    err = client.SendTransaction("", config, false)
    check(err)
    
    d.SetId(fmt.Sprintf("%s_%s", client.Host, id))
    
	return junosInterfacesInterface__RangeUnitFamilyEthernet__SwitchingVlanMembersRead(d,m)
}

func junosInterfacesInterface__RangeUnitFamilyEthernet__SwitchingVlanMembersRead(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
    
	config := &xmlInterfacesInterface__RangeUnitFamilyEthernet__SwitchingVlanMembers{}

	err = client.MarshalGroup(id, config)
	check(err)
 	d.Set("name", config.Groups.V_interface__range.V_name)
	d.Set("name__1", config.Groups.V_interface__range.V_unit.V_name__1)
	d.Set("members", config.Groups.V_interface__range.V_unit.V_vlan.V_members)

	return nil
}

func junosInterfacesInterface__RangeUnitFamilyEthernet__SwitchingVlanMembersUpdate(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
     	V_name := d.Get("name").(string)
	V_name__1 := d.Get("name__1").(string)
	V_members := d.Get("members").(string)


	config := xmlInterfacesInterface__RangeUnitFamilyEthernet__SwitchingVlanMembers{}
	config.ApplyGroup = id
	config.Groups.Name = id
	config.Groups.V_interface__range.V_name = &V_name
	config.Groups.V_interface__range.V_unit.V_name__1 = &V_name__1
	config.Groups.V_interface__range.V_unit.V_vlan.V_members = &V_members

    err = client.SendTransaction(id, config, false)
    check(err)
    
	return junosInterfacesInterface__RangeUnitFamilyEthernet__SwitchingVlanMembersRead(d,m)
}

func junosInterfacesInterface__RangeUnitFamilyEthernet__SwitchingVlanMembersDelete(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
    
    _, err = client.DeleteConfigNoCommit(id)
    check(err)

    d.SetId("")
    
	return nil
}

func junosInterfacesInterface__RangeUnitFamilyEthernet__SwitchingVlanMembers() *schema.Resource {
	return &schema.Resource{
		Create: junosInterfacesInterface__RangeUnitFamilyEthernet__SwitchingVlanMembersCreate,
		Read: junosInterfacesInterface__RangeUnitFamilyEthernet__SwitchingVlanMembersRead,
		Update: junosInterfacesInterface__RangeUnitFamilyEthernet__SwitchingVlanMembersUpdate,
		Delete: junosInterfacesInterface__RangeUnitFamilyEthernet__SwitchingVlanMembersDelete,

        Schema: map[string]*schema.Schema{
            "resource_name": &schema.Schema{
                Type:    schema.TypeString,
                Required: true,
            },
			"name": &schema.Schema{
				Type:    schema.TypeString,
				Optional: true,
				Description:    "xpath is: config.Groups.V_interface__range",
			},
			"name__1": &schema.Schema{
				Type:    schema.TypeString,
				Optional: true,
				Description:    "xpath is: config.Groups.V_interface__range.V_unit",
			},
			"members": &schema.Schema{
				Type:    schema.TypeString,
				Optional: true,
				Description:    "xpath is: config.Groups.V_interface__range.V_unit.V_vlan. Membership for this interface (name or id)",
			},
		},
	}
}