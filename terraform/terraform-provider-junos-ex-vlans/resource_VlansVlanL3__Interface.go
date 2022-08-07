
package main

import (
    "encoding/xml"
    "fmt"
    "github.com/hashicorp/terraform-plugin-sdk/helper/schema"
)


// v_ is appended before every variable so it doesn't give any conflict
// with any keyword in golang. ex - interface is keyword in golang
type xmlVlansVlanL3__Interface struct {
	XMLName xml.Name `xml:"configuration"`
	Groups  struct {
		XMLName	xml.Name	`xml:"groups"`
		Name	string	`xml:"name"`
		V_vlan  struct {
			XMLName xml.Name `xml:"vlan"`
			V_name  *string  `xml:"name,omitempty"`
			V_l3__interface  *string  `xml:"l3-interface,omitempty"`
		} `xml:"vlans>vlan"`
	} `xml:"groups"`
	ApplyGroup string `xml:"apply-groups"`
}

// v_ is appended before every variable so it doesn't give any conflict
// with any keyword in golang. ex- interface is keyword in golang
func junosVlansVlanL3__InterfaceCreate(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
     	V_name := d.Get("name").(string)
	V_l3__interface := d.Get("l3__interface").(string)


	config := xmlVlansVlanL3__Interface{}
	config.ApplyGroup = id
	config.Groups.Name = id
	config.Groups.V_vlan.V_name = &V_name
	config.Groups.V_vlan.V_l3__interface = &V_l3__interface

    err = client.SendTransaction("", config, false)
    check(err)
    
    d.SetId(fmt.Sprintf("%s_%s", client.Host, id))
    
	return junosVlansVlanL3__InterfaceRead(d,m)
}

func junosVlansVlanL3__InterfaceRead(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
    
	config := &xmlVlansVlanL3__Interface{}

	err = client.MarshalGroup(id, config)
	check(err)
 	d.Set("name", config.Groups.V_vlan.V_name)
	d.Set("l3__interface", config.Groups.V_vlan.V_l3__interface)

	return nil
}

func junosVlansVlanL3__InterfaceUpdate(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
     	V_name := d.Get("name").(string)
	V_l3__interface := d.Get("l3__interface").(string)


	config := xmlVlansVlanL3__Interface{}
	config.ApplyGroup = id
	config.Groups.Name = id
	config.Groups.V_vlan.V_name = &V_name
	config.Groups.V_vlan.V_l3__interface = &V_l3__interface

    err = client.SendTransaction(id, config, false)
    check(err)
    
	return junosVlansVlanL3__InterfaceRead(d,m)
}

func junosVlansVlanL3__InterfaceDelete(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
    
    _, err = client.DeleteConfigNoCommit(id)
    check(err)

    d.SetId("")
    
	return nil
}

func junosVlansVlanL3__Interface() *schema.Resource {
	return &schema.Resource{
		Create: junosVlansVlanL3__InterfaceCreate,
		Read: junosVlansVlanL3__InterfaceRead,
		Update: junosVlansVlanL3__InterfaceUpdate,
		Delete: junosVlansVlanL3__InterfaceDelete,

        Schema: map[string]*schema.Schema{
            "resource_name": &schema.Schema{
                Type:    schema.TypeString,
                Required: true,
            },
			"name": &schema.Schema{
				Type:    schema.TypeString,
				Optional: true,
				Description:    "xpath is: config.Groups.V_vlan",
			},
			"l3__interface": &schema.Schema{
				Type:    schema.TypeString,
				Optional: true,
				Description:    "xpath is: config.Groups.V_vlan. L3 interface name for this vlans",
			},
		},
	}
}