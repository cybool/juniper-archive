
package main

import (
    "encoding/xml"
    "fmt"
    "github.com/hashicorp/terraform-plugin-sdk/helper/schema"
)


// v_ is appended before every variable so it doesn't give any conflict
// with any keyword in golang. ex - interface is keyword in golang
type xmlProtocolsMstpMstiVlan struct {
	XMLName xml.Name `xml:"configuration"`
	Groups  struct {
		XMLName	xml.Name	`xml:"groups"`
		Name	string	`xml:"name"`
		V_msti  struct {
			XMLName xml.Name `xml:"msti"`
			V_name  *string  `xml:"name,omitempty"`
			V_vlan  *string  `xml:"vlan,omitempty"`
		} `xml:"protocols>mstp>msti"`
	} `xml:"groups"`
	ApplyGroup string `xml:"apply-groups"`
}

// v_ is appended before every variable so it doesn't give any conflict
// with any keyword in golang. ex- interface is keyword in golang
func junosProtocolsMstpMstiVlanCreate(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
     	V_name := d.Get("name").(string)
	V_vlan := d.Get("vlan").(string)


	config := xmlProtocolsMstpMstiVlan{}
	config.ApplyGroup = id
	config.Groups.Name = id
	config.Groups.V_msti.V_name = &V_name
	config.Groups.V_msti.V_vlan = &V_vlan

    err = client.SendTransaction("", config, false)
    check(err)
    
    d.SetId(fmt.Sprintf("%s_%s", client.Host, id))
    
	return junosProtocolsMstpMstiVlanRead(d,m)
}

func junosProtocolsMstpMstiVlanRead(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
    
	config := &xmlProtocolsMstpMstiVlan{}

	err = client.MarshalGroup(id, config)
	check(err)
 	d.Set("name", config.Groups.V_msti.V_name)
	d.Set("vlan", config.Groups.V_msti.V_vlan)

	return nil
}

func junosProtocolsMstpMstiVlanUpdate(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
     	V_name := d.Get("name").(string)
	V_vlan := d.Get("vlan").(string)


	config := xmlProtocolsMstpMstiVlan{}
	config.ApplyGroup = id
	config.Groups.Name = id
	config.Groups.V_msti.V_name = &V_name
	config.Groups.V_msti.V_vlan = &V_vlan

    err = client.SendTransaction(id, config, false)
    check(err)
    
	return junosProtocolsMstpMstiVlanRead(d,m)
}

func junosProtocolsMstpMstiVlanDelete(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
    
    _, err = client.DeleteConfigNoCommit(id)
    check(err)

    d.SetId("")
    
	return nil
}

func junosProtocolsMstpMstiVlan() *schema.Resource {
	return &schema.Resource{
		Create: junosProtocolsMstpMstiVlanCreate,
		Read: junosProtocolsMstpMstiVlanRead,
		Update: junosProtocolsMstpMstiVlanUpdate,
		Delete: junosProtocolsMstpMstiVlanDelete,

        Schema: map[string]*schema.Schema{
            "resource_name": &schema.Schema{
                Type:    schema.TypeString,
                Required: true,
            },
			"name": &schema.Schema{
				Type:    schema.TypeString,
				Optional: true,
				Description:    "xpath is: config.Groups.V_msti",
			},
			"vlan": &schema.Schema{
				Type:    schema.TypeString,
				Optional: true,
				Description:    "xpath is: config.Groups.V_msti. VLAN ID or VLAN ID range [1..4094]",
			},
		},
	}
}