
package main

import (
    "encoding/xml"
    "fmt"
    "github.com/hashicorp/terraform-plugin-sdk/helper/schema"
)


// v_ is appended before every variable so it doesn't give any conflict
// with any keyword in golang. ex - interface is keyword in golang
type xmlVlansVlanVlan__Id struct {
	XMLName xml.Name `xml:"configuration"`
	Groups  struct {
		XMLName	xml.Name	`xml:"groups"`
		Name	string	`xml:"name"`
		V_vlan  struct {
			XMLName xml.Name `xml:"vlan"`
			V_name  *string  `xml:"name,omitempty"`
			V_vlan__id  *string  `xml:"vlan-id,omitempty"`
		} `xml:"vlans>vlan"`
	} `xml:"groups"`
	ApplyGroup string `xml:"apply-groups"`
}

// v_ is appended before every variable so it doesn't give any conflict
// with any keyword in golang. ex- interface is keyword in golang
func junosVlansVlanVlan__IdCreate(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
     	V_name := d.Get("name").(string)
	V_vlan__id := d.Get("vlan__id").(string)


	config := xmlVlansVlanVlan__Id{}
	config.ApplyGroup = id
	config.Groups.Name = id
	config.Groups.V_vlan.V_name = &V_name
	config.Groups.V_vlan.V_vlan__id = &V_vlan__id

    err = client.SendTransaction("", config, false)
    check(err)
    
    d.SetId(fmt.Sprintf("%s_%s", client.Host, id))
    
	return junosVlansVlanVlan__IdRead(d,m)
}

func junosVlansVlanVlan__IdRead(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
    
	config := &xmlVlansVlanVlan__Id{}

	err = client.MarshalGroup(id, config)
	check(err)
 	d.Set("name", config.Groups.V_vlan.V_name)
	d.Set("vlan__id", config.Groups.V_vlan.V_vlan__id)

	return nil
}

func junosVlansVlanVlan__IdUpdate(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
     	V_name := d.Get("name").(string)
	V_vlan__id := d.Get("vlan__id").(string)


	config := xmlVlansVlanVlan__Id{}
	config.ApplyGroup = id
	config.Groups.Name = id
	config.Groups.V_vlan.V_name = &V_name
	config.Groups.V_vlan.V_vlan__id = &V_vlan__id

    err = client.SendTransaction(id, config, false)
    check(err)
    
	return junosVlansVlanVlan__IdRead(d,m)
}

func junosVlansVlanVlan__IdDelete(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
    
    _, err = client.DeleteConfigNoCommit(id)
    check(err)

    d.SetId("")
    
	return nil
}

func junosVlansVlanVlan__Id() *schema.Resource {
	return &schema.Resource{
		Create: junosVlansVlanVlan__IdCreate,
		Read: junosVlansVlanVlan__IdRead,
		Update: junosVlansVlanVlan__IdUpdate,
		Delete: junosVlansVlanVlan__IdDelete,

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
			"vlan__id": &schema.Schema{
				Type:    schema.TypeString,
				Optional: true,
				Description:    "xpath is: config.Groups.V_vlan. IEEE 802.1q VLAN identifier for VLAN",
			},
		},
	}
}