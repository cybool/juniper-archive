
// Copyright (c) 2017-2021, Juniper Networks Inc. All rights reserved.
//
// License: Apache 2.0
//
// THIS SOFTWARE IS PROVIDED BY Juniper Networks, Inc. ''AS IS'' AND ANY
// EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
// WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
// DISCLAIMED. IN NO EVENT SHALL Juniper Networks, Inc. BE LIABLE FOR ANY
// DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
// (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
// LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
// ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
// SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//

package main

import (

	gonetconf "github.com/davedotdev/go-netconf/helpers/junos_helpers"
	"github.com/hashicorp/terraform-plugin-sdk/helper/schema"
	"os"
)

// ProviderConfig is to hold client information
type ProviderConfig struct {
	*gonetconf.GoNCClient
	Host string
}

func check(err error) {
	if err != nil {
		// Some of these errors will be "normal".
		f, _ := os.OpenFile("jtaf_logging.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
		f.WriteString(err.Error() + "\n")
		f.Close()
		return
	}
}


func providerConfigure(d *schema.ResourceData) (interface{}, error) {
	config := Config{
		Host:     d.Get("host").(string),
		Port:     d.Get("port").(int),
		Username: d.Get("username").(string),
		Password: d.Get("password").(string),
		SSHKey:   d.Get("sshkey").(string),
	}

	client, err := config.Client()
	if err != nil {
		return nil, err
	}

	return &ProviderConfig{client, config.Host}, nil
}

// Provider returns a Terraform ResourceProvider.
func Provider() *schema.Provider {
	return &schema.Provider{

		Schema: map[string]*schema.Schema{
			"host": &schema.Schema{
				Type:     schema.TypeString,
				Required: true,
			},

			"port": &schema.Schema{
				Type:     schema.TypeInt,
				Required: true,
			},

			"username": &schema.Schema{
				Type:     schema.TypeString,
				Required: true,
			},

			"password": &schema.Schema{
				Type:     schema.TypeString,
				Required: true,
			},
			"sshkey": &schema.Schema{
				Type:     schema.TypeString,
				Required: true,
			},
		},

		ResourcesMap: map[string]*schema.Resource{
			"junos-ike_SecurityIkeProposalName": junosSecurityIkeProposalName(),
			"junos-ike_SecurityIkeProposalDescription": junosSecurityIkeProposalDescription(),
			"junos-ike_SecurityIkeProposalAuthentication__Method": junosSecurityIkeProposalAuthentication__Method(),
			"junos-ike_SecurityIkeProposalDh__Group": junosSecurityIkeProposalDh__Group(),
			"junos-ike_SecurityIkeProposalAuthentication__Algorithm": junosSecurityIkeProposalAuthentication__Algorithm(),
			"junos-ike_SecurityIkeProposalEncryption__Algorithm": junosSecurityIkeProposalEncryption__Algorithm(),
			"junos-ike_SecurityIkeProposalLifetime__Seconds": junosSecurityIkeProposalLifetime__Seconds(),
			"junos-ike_SecurityIkePolicyName": junosSecurityIkePolicyName(),
			"junos-ike_SecurityIkePolicyMode": junosSecurityIkePolicyMode(),
			"junos-ike_SecurityIkePolicyDescription": junosSecurityIkePolicyDescription(),
			"junos-ike_SecurityIkePolicyProposals": junosSecurityIkePolicyProposals(),
			"junos-ike_SecurityIkePolicyPre__Shared__KeyAscii__Text": junosSecurityIkePolicyPre__Shared__KeyAscii__Text(),
			"junos-ike_SecurityIkeGatewayName": junosSecurityIkeGatewayName(),
			"junos-ike_SecurityIkeGatewayAddress": junosSecurityIkeGatewayAddress(),
			"junos-ike_SecurityIkeGatewayIke__Policy": junosSecurityIkeGatewayIke__Policy(),
			"junos-ike_SecurityIkeGatewayExternal__Interface": junosSecurityIkeGatewayExternal__Interface(),
			"junos-ike_commit": junosCommit(),
	        "junos-ike_destroycommit": junosDestroyCommit(),
			},
		    ConfigureFunc: providerConfigure,
	    } 
    }
