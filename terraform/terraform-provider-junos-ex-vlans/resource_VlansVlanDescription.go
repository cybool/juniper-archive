
package main

import (
    "encoding/xml"
    "fmt"
    "github.com/hashicorp/terraform-plugin-sdk/helper/schema"
)


// v_ is appended before every variable so it doesn't give any conflict
// with any keyword in golang. ex - interface is keyword in golang
type xmlVlansVlanDescription struct {
	XMLName xml.Name `xml:"configuration"`
	Groups  struct {
		XMLName	xml.Name	`xml:"groups"`
		Name	string	`xml:"name"`
		V_vlan  struct {
			XMLName xml.Name `xml:"vlan"`
			V_name  *string  `xml:"name,omitempty"`
			V_description  *string  `xml:"description,omitempty"`
		} `xml:"vlans>vlan"`
	} `xml:"groups"`
	ApplyGroup string `xml:"apply-groups"`
}

// v_ is appended before every variable so it doesn't give any conflict
// with any keyword in golang. ex- interface is keyword in golang
func junosVlansVlanDescriptionCreate(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
     	V_name := d.Get("name").(string)
	V_description := d.Get("description").(string)


	config := xmlVlansVlanDescription{}
	config.ApplyGroup = id
	config.Groups.Name = id
	config.Groups.V_vlan.V_name = &V_name
	config.Groups.V_vlan.V_description = &V_description

    err = client.SendTransaction("", config, false)
    check(err)
    
    d.SetId(fmt.Sprintf("%s_%s", client.Host, id))
    
	return junosVlansVlanDescriptionRead(d,m)
}

func junosVlansVlanDescriptionRead(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
    
	config := &xmlVlansVlanDescription{}

	err = client.MarshalGroup(id, config)
	check(err)
 	d.Set("name", config.Groups.V_vlan.V_name)
	d.Set("description", config.Groups.V_vlan.V_description)

	return nil
}

func junosVlansVlanDescriptionUpdate(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
     	V_name := d.Get("name").(string)
	V_description := d.Get("description").(string)


	config := xmlVlansVlanDescription{}
	config.ApplyGroup = id
	config.Groups.Name = id
	config.Groups.V_vlan.V_name = &V_name
	config.Groups.V_vlan.V_description = &V_description

    err = client.SendTransaction(id, config, false)
    check(err)
    
	return junosVlansVlanDescriptionRead(d,m)
}

func junosVlansVlanDescriptionDelete(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
    
    _, err = client.DeleteConfigNoCommit(id)
    check(err)

    d.SetId("")
    
	return nil
}

func junosVlansVlanDescription() *schema.Resource {
	return &schema.Resource{
		Create: junosVlansVlanDescriptionCreate,
		Read: junosVlansVlanDescriptionRead,
		Update: junosVlansVlanDescriptionUpdate,
		Delete: junosVlansVlanDescriptionDelete,

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
			"description": &schema.Schema{
				Type:    schema.TypeString,
				Optional: true,
				Description:    "xpath is: config.Groups.V_vlan. Text description of VLANs",
			},
		},
	}
}