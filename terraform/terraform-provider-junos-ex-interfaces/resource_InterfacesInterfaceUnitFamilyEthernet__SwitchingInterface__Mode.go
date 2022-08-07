
package main

import (
    "encoding/xml"
    "fmt"
    "github.com/hashicorp/terraform-plugin-sdk/helper/schema"
)


// v_ is appended before every variable so it doesn't give any conflict
// with any keyword in golang. ex - interface is keyword in golang
type xmlInterfacesInterfaceUnitFamilyEthernet__SwitchingInterface__Mode struct {
	XMLName xml.Name `xml:"configuration"`
	Groups  struct {
		XMLName	xml.Name	`xml:"groups"`
		Name	string	`xml:"name"`
		V_interface  struct {
			XMLName xml.Name `xml:"interface"`
			V_name  *string  `xml:"name,omitempty"`
			V_unit  struct {
				XMLName xml.Name `xml:"unit"`
				V_name__1  *string  `xml:"name,omitempty"`
				V_ethernet__switching  struct {
					XMLName xml.Name `xml:"ethernet-switching"`
					V_interface__mode  *string  `xml:"interface-mode,omitempty"`
				} `xml:"family>ethernet-switching"`
			} `xml:"unit"`
		} `xml:"interfaces>interface"`
	} `xml:"groups"`
	ApplyGroup string `xml:"apply-groups"`
}

// v_ is appended before every variable so it doesn't give any conflict
// with any keyword in golang. ex- interface is keyword in golang
func junosInterfacesInterfaceUnitFamilyEthernet__SwitchingInterface__ModeCreate(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
     	V_name := d.Get("name").(string)
	V_name__1 := d.Get("name__1").(string)
	V_interface__mode := d.Get("interface__mode").(string)


	config := xmlInterfacesInterfaceUnitFamilyEthernet__SwitchingInterface__Mode{}
	config.ApplyGroup = id
	config.Groups.Name = id
	config.Groups.V_interface.V_name = &V_name
	config.Groups.V_interface.V_unit.V_name__1 = &V_name__1
	config.Groups.V_interface.V_unit.V_ethernet__switching.V_interface__mode = &V_interface__mode

    err = client.SendTransaction("", config, false)
    check(err)
    
    d.SetId(fmt.Sprintf("%s_%s", client.Host, id))
    
	return junosInterfacesInterfaceUnitFamilyEthernet__SwitchingInterface__ModeRead(d,m)
}

func junosInterfacesInterfaceUnitFamilyEthernet__SwitchingInterface__ModeRead(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
    
	config := &xmlInterfacesInterfaceUnitFamilyEthernet__SwitchingInterface__Mode{}

	err = client.MarshalGroup(id, config)
	check(err)
 	d.Set("name", config.Groups.V_interface.V_name)
	d.Set("name__1", config.Groups.V_interface.V_unit.V_name__1)
	d.Set("interface__mode", config.Groups.V_interface.V_unit.V_ethernet__switching.V_interface__mode)

	return nil
}

func junosInterfacesInterfaceUnitFamilyEthernet__SwitchingInterface__ModeUpdate(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
     	V_name := d.Get("name").(string)
	V_name__1 := d.Get("name__1").(string)
	V_interface__mode := d.Get("interface__mode").(string)


	config := xmlInterfacesInterfaceUnitFamilyEthernet__SwitchingInterface__Mode{}
	config.ApplyGroup = id
	config.Groups.Name = id
	config.Groups.V_interface.V_name = &V_name
	config.Groups.V_interface.V_unit.V_name__1 = &V_name__1
	config.Groups.V_interface.V_unit.V_ethernet__switching.V_interface__mode = &V_interface__mode

    err = client.SendTransaction(id, config, false)
    check(err)
    
	return junosInterfacesInterfaceUnitFamilyEthernet__SwitchingInterface__ModeRead(d,m)
}

func junosInterfacesInterfaceUnitFamilyEthernet__SwitchingInterface__ModeDelete(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
    
    _, err = client.DeleteConfigNoCommit(id)
    check(err)

    d.SetId("")
    
	return nil
}

func junosInterfacesInterfaceUnitFamilyEthernet__SwitchingInterface__Mode() *schema.Resource {
	return &schema.Resource{
		Create: junosInterfacesInterfaceUnitFamilyEthernet__SwitchingInterface__ModeCreate,
		Read: junosInterfacesInterfaceUnitFamilyEthernet__SwitchingInterface__ModeRead,
		Update: junosInterfacesInterfaceUnitFamilyEthernet__SwitchingInterface__ModeUpdate,
		Delete: junosInterfacesInterfaceUnitFamilyEthernet__SwitchingInterface__ModeDelete,

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
			"name__1": &schema.Schema{
				Type:    schema.TypeString,
				Optional: true,
				Description:    "xpath is: config.Groups.V_interface.V_unit",
			},
			"interface__mode": &schema.Schema{
				Type:    schema.TypeString,
				Optional: true,
				Description:    "xpath is: config.Groups.V_interface.V_unit.V_ethernet__switching. Type of interface mode",
			},
		},
	}
}