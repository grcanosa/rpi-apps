#!/usr/bin/python3

import CloudFlare
import ipgetter

import time

MAIN_LOOP_SLEEP_SECONDS = 15*60

#ZONEID = 
APIKEY = 
EMAIL = 

NAMES = []


def update_ips_if_necessary(cf, current_ip):
	updated_names = []
	try:
		zones = cf.zones.get(params={"name":zone_name})
		zone_id = zones[0]["id"]
		params = {'match':'all', 
		  		'type':"A"}
		dns_records = cf.zones.dns_records(zone_id,params=params)
		for dns in dns_records:
			if dns["type"] = "A" and dns["name"] in NAMES:
				if dns["content"] != current_ip:
					#Update IP
					dns_record_id = dns['id']
			        dns_record = {
			            'name':dns["name"],
			            'type':"A",
			            'content':current_ip
			        }
			        try:
			            dns_record = cf.zones.dns_records.put(zone_id,
			            						 dns_record_id,
			        	   						 data=dns_record)
			            updated_names.append(dns["name"])
			        except CloudFlare.exceptions.CloudFlareAPIError as e:
			        	print("Error updating "+dns["name"])


	except CloudFlare.exceptions.CloudFlareAPIError as e:
		print("Error")

def main():
	cf = CloudFlare.CloudFlare(email=EMAIL,token=APIKEY)
	while True:
		current_ip = ipgetter.myip()
		update_ip_if_necessary(cf,current_ip)		
		time.sleep(MAIN_LOOP_SLEEP_SECONDS)



if __name__ == "__main__":
	main()