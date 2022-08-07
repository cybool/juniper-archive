
package main

import (
    "encoding/xml"
    "fmt"
    "github.com/hashicorp/terraform-plugin-sdk/helper/schema"
)


// v_ is appended before every variable so it doesn't give any conflict
// with any keyword in golang. ex - interface is keyword in golang
type xmlProtocolsMstpInterfaceEdge struct {
	XMLName xml.Name `xml:"configuration"`
	Groups  struct {
		XMLName	xml.Name	`xml:"groups"`
		Name	string	`xml:"name"`
		V_interface  struct {
			XMLName xml.Name `xml:"interface"`
			V_name  *string  `xml:"name,omitempty"`
			V_edge  *string  `xml:"edge,omitempty"`
		} `xml:"protocols>mstp>interface"`
	} `xml:"groups"`
	ApplyGroup string `xml:"apply-groups"`
}

// v_ is appended before every variable so it doesn't give any conflict
// with any keyword in golang. ex- interface is keyword in golang
func junosProtocolsMstpInterfaceEdgeCreate(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
     	V_name := d.Get("name").(string)
	V_edge := d.Get("edge").(string)


	config := xmlProtocolsMstpInterfaceEdge{}
	config.ApplyGroup = id
	config.Groups.Name = id
	config.Groups.V_interface.V_name = &V_name
	config.Groups.V_interface.V_edge = &V_edge

    err = client.SendTransaction("", config, false)
    check(err)
    
    d.SetId(fmt.Sprintf("%s_%s", client.Host, id))
    
	return junosProtocolsMstpInterfaceEdgeRead(d,m)
}

func junosProtocolsMstpInterfaceEdgeRead(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
    
	config := &xmlProtocolsMstpInterfaceEdge{}

	err = client.MarshalGroup(id, config)
	check(err)
 	d.Set("name", config.Groups.V_interface.V_name)
	d.Set("edge", config.Groups.V_interface.V_edge)

	return nil
}

func junosProtocolsMstpInterfaceEdgeUpdate(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
     	V_name := d.Get("name").(string)
	V_edge := d.Get("edge").(string)


	config := xmlProtocolsMstpInterfaceEdge{}
	config.ApplyGroup = id
	config.Groups.Name = id
	config.Groups.V_interface.V_name = &V_name
	config.Groups.V_interface.V_edge = &V_edge

    err = client.SendTransaction(id, config, false)
    check(err)
    
	return junosProtocolsMstpInterfaceEdgeRead(d,m)
}

func junosProtocolsMstpInterfaceEdgeDelete(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
    
    _, err = client.DeleteConfigNoCommit(id)
    check(err)

    d.SetId("")
    
	return nil
}

func junosProtocolsMstpInterfaceEdge() *schema.Resource {
	return &schema.Resource{
		Create: junosProtocolsMstpInterfaceEdgeCreate,
		Read: junosProtocolsMstpInterfaceEdgeRead,
		Update: junosProtocolsMstpInterfaceEdgeUpdate,
		Delete: junosProtocolsMstpInterfaceEdgeDelete,

        Schema: map[string]*schema.Schema{
            "resource_name": &schema.Schema{
                Type:    schema.TypeString,
                Required: true,
            },
			"name": &schema.Schema{
				Type:    schema.TypeString,
				Optional: true,
				Description:    "xpath is: config.Groups.V_interface",
			},
			"edge": &schema.Schema{
				Type:    schema.TypeString,
				Optional: true,
				Description:    "xpath is: config.Groups.V_interface. Port is an edge port",
			},
		},
	}
}