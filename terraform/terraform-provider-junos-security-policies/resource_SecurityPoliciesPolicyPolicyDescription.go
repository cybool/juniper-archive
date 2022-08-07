
package main

import (
    "encoding/xml"
    "fmt"
    "github.com/hashicorp/terraform-plugin-sdk/helper/schema"
)


// v_ is appended before every variable so it doesn't give any conflict
// with any keyword in golang. ex - interface is keyword in golang
type xmlSecurityPoliciesPolicyPolicyDescription struct {
	XMLName xml.Name `xml:"configuration"`
	Groups  struct {
		XMLName	xml.Name	`xml:"groups"`
		Name	string	`xml:"name"`
		V_policy  struct {
			XMLName xml.Name `xml:"policy"`
			V_from__zone__name  *string  `xml:"from-zone-name,omitempty"`
			V_to__zone__name  *string  `xml:"to-zone-name,omitempty"`
			V_policy__1  struct {
				XMLName xml.Name `xml:"policy"`
				V_name  *string  `xml:"name,omitempty"`
				V_description  *string  `xml:"description,omitempty"`
			} `xml:"policy"`
		} `xml:"security>policies>policy"`
	} `xml:"groups"`
	ApplyGroup string `xml:"apply-groups"`
}

// v_ is appended before every variable so it doesn't give any conflict
// with any keyword in golang. ex- interface is keyword in golang
func junosSecurityPoliciesPolicyPolicyDescriptionCreate(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
     	V_from__zone__name := d.Get("from__zone__name").(string)
	V_to__zone__name := d.Get("to__zone__name").(string)
	V_name := d.Get("name").(string)
	V_description := d.Get("description").(string)


	config := xmlSecurityPoliciesPolicyPolicyDescription{}
	config.ApplyGroup = id
	config.Groups.Name = id
	config.Groups.V_policy.V_from__zone__name = &V_from__zone__name
	config.Groups.V_policy.V_to__zone__name = &V_to__zone__name
	config.Groups.V_policy.V_policy__1.V_name = &V_name
	config.Groups.V_policy.V_policy__1.V_description = &V_description

    err = client.SendTransaction("", config, false)
    check(err)
    
    d.SetId(fmt.Sprintf("%s_%s", client.Host, id))
    
	return junosSecurityPoliciesPolicyPolicyDescriptionRead(d,m)
}

func junosSecurityPoliciesPolicyPolicyDescriptionRead(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
    
	config := &xmlSecurityPoliciesPolicyPolicyDescription{}

	err = client.MarshalGroup(id, config)
	check(err)
 	d.Set("from__zone__name", config.Groups.V_policy.V_from__zone__name)
	d.Set("to__zone__name", config.Groups.V_policy.V_to__zone__name)
	d.Set("name", config.Groups.V_policy.V_policy__1.V_name)
	d.Set("description", config.Groups.V_policy.V_policy__1.V_description)

	return nil
}

func junosSecurityPoliciesPolicyPolicyDescriptionUpdate(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
     	V_from__zone__name := d.Get("from__zone__name").(string)
	V_to__zone__name := d.Get("to__zone__name").(string)
	V_name := d.Get("name").(string)
	V_description := d.Get("description").(string)


	config := xmlSecurityPoliciesPolicyPolicyDescription{}
	config.ApplyGroup = id
	config.Groups.Name = id
	config.Groups.V_policy.V_from__zone__name = &V_from__zone__name
	config.Groups.V_policy.V_to__zone__name = &V_to__zone__name
	config.Groups.V_policy.V_policy__1.V_name = &V_name
	config.Groups.V_policy.V_policy__1.V_description = &V_description

    err = client.SendTransaction(id, config, false)
    check(err)
    
	return junosSecurityPoliciesPolicyPolicyDescriptionRead(d,m)
}

func junosSecurityPoliciesPolicyPolicyDescriptionDelete(d *schema.ResourceData, m interface{}) error {

	var err error
	client := m.(*ProviderConfig)

    id := d.Get("resource_name").(string)
    
    _, err = client.DeleteConfigNoCommit(id)
    check(err)

    d.SetId("")
    
	return nil
}

func junosSecurityPoliciesPolicyPolicyDescription() *schema.Resource {
	return &schema.Resource{
		Create: junosSecurityPoliciesPolicyPolicyDescriptionCreate,
		Read: junosSecurityPoliciesPolicyPolicyDescriptionRead,
		Update: junosSecurityPoliciesPolicyPolicyDescriptionUpdate,
		Delete: junosSecurityPoliciesPolicyPolicyDescriptionDelete,

        Schema: map[string]*schema.Schema{
            "resource_name": &schema.Schema{
                Type:    schema.TypeString,
                Required: true,
            },
			"from__zone__name": &schema.Schema{
				Type:    schema.TypeString,
				Optional: true,
				Description:    "xpath is: config.Groups.V_policy",
			},
			"to__zone__name": &schema.Schema{
				Type:    schema.TypeString,
				Optional: true,
				Description:    "xpath is: config.Groups.V_policy",
			},
			"name": &schema.Schema{
				Type:    schema.TypeString,
				Optional: true,
				Description:    "xpath is: config.Groups.V_policy.V_policy__1",
			},
			"description": &schema.Schema{
				Type:    schema.TypeString,
				Optional: true,
				Description:    "xpath is: config.Groups.V_policy.V_policy__1. Text description of policy",
			},
		},
	}
}