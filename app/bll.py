import configparser
import requests
import socket

class ConfigData:
    def __init__(self, path, config):
        cp = configparser.RawConfigParser()
        configFilePath = path
        cp.read(configFilePath)

        self.zone_name = cp.get(config, 'zone_name')
        self.api_token = cp.get(config, 'api_token')
        self.interval = int(cp.get(config, 'interval'))
        self.fqdn = cp.get(config, 'fqdn')  

class ip:
    def __init__(self, name):
        self.current_ip = requests.get('https://api.ipify.org?format=json').json()["ip"]

def updateIP( api_token, zone_name, fqdn, ip):

    head = {'Authorization': 'Bearer ' + api_token}

    zone_id = requests.get("https://api.cloudflare.com/client/v4/zones?name=" + zone_name, headers=head).json()['result'][0]['id']
        
    dns_record = requests.get("https://api.cloudflare.com/client/v4/zones/" + zone_id + "/dns_records?type=A&name=" +  fqdn, headers=head).json()['result']
    
    for record in dns_record:
        if record['type'] == 'A' and record['name'] == fqdn:
            if record["content"] != ip:
                print("IP does not match, current ip: {} - cloudflare ip: {}".format(ip, record["content"]))

                data = {'type':'A', 'name': fqdn, 'content': ip, 'ttl': record['ttl'], 'proxied': record['proxied']}
                update_record = requests.put("https://api.cloudflare.com/client/v4/zones/" + zone_id + "/dns_records/"+ record["id"], headers=head, json=data).json()
                if update_record["success"] == True:
                    print("Updated cloudflare")
                else:
                    print("Failed to update cloudflare")
            else:
                print("IP does match, current ip: {}".format(ip))
