
package main

import (
    "encoding/xml"
    "fmt"
    "github.com/hashicorp/terraform-plugin-sdk/helper/schema"
)


// v_ is appended before every variable so it doesn't give any conflict
// with any keyword in golang. ex - interface is keyword in golang
type xmlProtocolsMstpBridge__Priority struct {
	XMLName xml.Name `xml:"configuration"`
	Groups  struct {
		XMLName	xml.Name	`xml:"groups"`
		Name	string	`xml:"name"`
		V_mstp  struct {
			XMLName xml.Name `xml:"mstp"`
			V_bridge__priority  *string  `xml:"bridge-priority,omitempty"`
		} `xml:"protocols>mstp"`
	} `xml:"groups"`
	ApplyGroup string `xml:"apply-groups"`
}

// v_ is appended before every variable so it doesn't give any conflict
// with any keyword in golang. ex- interface is keyword in golang
func junosProtocolsMstpBridge__PriorityCreate(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
     	V_bridge__priority := d.Get("bridge__priority").(string)


	config := xmlProtocolsMstpBridge__Priority{}
	config.ApplyGroup = id
	config.Groups.Name = id
	config.Groups.V_mstp.V_bridge__priority = &V_bridge__priority

    err = client.SendTransaction("", config, false)
    check(err)
    
    d.SetId(fmt.Sprintf("%s_%s", client.Host, id))
    
	return junosProtocolsMstpBridge__PriorityRead(d,m)
}

func junosProtocolsMstpBridge__PriorityRead(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
    
	config := &xmlProtocolsMstpBridge__Priority{}

	err = client.MarshalGroup(id, config)
	check(err)
 	d.Set("bridge__priority", config.Groups.V_mstp.V_bridge__priority)

	return nil
}

func junosProtocolsMstpBridge__PriorityUpdate(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
     	V_bridge__priority := d.Get("bridge__priority").(string)


	config := xmlProtocolsMstpBridge__Priority{}
	config.ApplyGroup = id
	config.Groups.Name = id
	config.Groups.V_mstp.V_bridge__priority = &V_bridge__priority

    err = client.SendTransaction(id, config, false)
    check(err)
    
	return junosProtocolsMstpBridge__PriorityRead(d,m)
}

func junosProtocolsMstpBridge__PriorityDelete(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
    
    _, err = client.DeleteConfigNoCommit(id)
    check(err)

    d.SetId("")
    
	return nil
}

func junosProtocolsMstpBridge__Priority() *schema.Resource {
	return &schema.Resource{
		Create: junosProtocolsMstpBridge__PriorityCreate,
		Read: junosProtocolsMstpBridge__PriorityRead,
		Update: junosProtocolsMstpBridge__PriorityUpdate,
		Delete: junosProtocolsMstpBridge__PriorityDelete,

        Schema: map[string]*schema.Schema{
            "resource_name": &schema.Schema{
                Type:    schema.TypeString,
                Required: true,
            },
			"bridge__priority": &schema.Schema{
				Type:    schema.TypeString,
				Optional: true,
				Description:    "xpath is: config.Groups.V_mstp. Priority of the bridge (in increments of 4k - 0,4k,8k,..60k)",
			},
		},
	}
}