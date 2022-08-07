
package main

import (
    "encoding/xml"
    "fmt"
    "github.com/hashicorp/terraform-plugin-sdk/helper/schema"
)


// v_ is appended before every variable so it doesn't give any conflict
// with any keyword in golang. ex - interface is keyword in golang
type xmlProtocolsMstpConfiguration__Name struct {
	XMLName xml.Name `xml:"configuration"`
	Groups  struct {
		XMLName	xml.Name	`xml:"groups"`
		Name	string	`xml:"name"`
		V_mstp  struct {
			XMLName xml.Name `xml:"mstp"`
			V_configuration__name  *string  `xml:"configuration-name,omitempty"`
		} `xml:"protocols>mstp"`
	} `xml:"groups"`
	ApplyGroup string `xml:"apply-groups"`
}

// v_ is appended before every variable so it doesn't give any conflict
// with any keyword in golang. ex- interface is keyword in golang
func junosProtocolsMstpConfiguration__NameCreate(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
     	V_configuration__name := d.Get("configuration__name").(string)


	config := xmlProtocolsMstpConfiguration__Name{}
	config.ApplyGroup = id
	config.Groups.Name = id
	config.Groups.V_mstp.V_configuration__name = &V_configuration__name

    err = client.SendTransaction("", config, false)
    check(err)
    
    d.SetId(fmt.Sprintf("%s_%s", client.Host, id))
    
	return junosProtocolsMstpConfiguration__NameRead(d,m)
}

func junosProtocolsMstpConfiguration__NameRead(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
    
	config := &xmlProtocolsMstpConfiguration__Name{}

	err = client.MarshalGroup(id, config)
	check(err)
 	d.Set("configuration__name", config.Groups.V_mstp.V_configuration__name)

	return nil
}

func junosProtocolsMstpConfiguration__NameUpdate(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
     	V_configuration__name := d.Get("configuration__name").(string)


	config := xmlProtocolsMstpConfiguration__Name{}
	config.ApplyGroup = id
	config.Groups.Name = id
	config.Groups.V_mstp.V_configuration__name = &V_configuration__name

    err = client.SendTransaction(id, config, false)
    check(err)
    
	return junosProtocolsMstpConfiguration__NameRead(d,m)
}

func junosProtocolsMstpConfiguration__NameDelete(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
    
    _, err = client.DeleteConfigNoCommit(id)
    check(err)

    d.SetId("")
    
	return nil
}

func junosProtocolsMstpConfiguration__Name() *schema.Resource {
	return &schema.Resource{
		Create: junosProtocolsMstpConfiguration__NameCreate,
		Read: junosProtocolsMstpConfiguration__NameRead,
		Update: junosProtocolsMstpConfiguration__NameUpdate,
		Delete: junosProtocolsMstpConfiguration__NameDelete,

        Schema: map[string]*schema.Schema{
            "resource_name": &schema.Schema{
                Type:    schema.TypeString,
                Required: true,
            },
			"configuration__name": &schema.Schema{
				Type:    schema.TypeString,
				Optional: true,
				Description:    "xpath is: config.Groups.V_mstp. Configuration name (part of MST configuration identifier)",
			},
		},
	}
}