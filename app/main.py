import time
import bll

configData = bll.ConfigData('config.cfg', 'main-config')

while True:
    ip = bll.ip(configData.fqdn)

    bll.updateIP(configData.api_token, configData.zone_name, configData.fqdn, ip.current_ip)
    print("Sleeping for {} seconds".format(configData.interval))

    time.sleep(configData.interval)